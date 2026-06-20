"""Rate limiting middleware enforcing request limits per token."""

from __future__ import annotations

import time
from collections import defaultdict
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Enforces a rate limit of 3 requests per 1 second per API token."""

    def __init__(self, app, limit: int = 3, window_seconds: float = 1.0):
        super().__init__(app)
        self.limit = limit
        self.window_seconds = window_seconds
        # In-memory store: { token/IP: [timestamp1, timestamp2, ...] }
        self.history: dict[str, list[float]] = defaultdict(list)

    async def dispatch(self, request: Request, call_next) -> Response:
        # Skip rate limiting for WebSocket requests to prevent connection upgrade blocking
        if request.scope.get("type") == "websocket" or request.url.path == "/ws":
            return await call_next(request)

        # Resolve client identifier: token (from Authorization header) or IP
        auth_header = request.headers.get("authorization", "")
        token = auth_header.partition(" ")[2] if auth_header else ""
        identifier = token if token else (request.client.host if request.client else "unknown")

        now = time.time()
        # Clean up old timestamps
        history = self.history[identifier]
        history[:] = [t for t in history if now - t < self.window_seconds]

        if len(history) >= self.limit:
            return JSONResponse(
                status_code=429,
                content={"detail": "Too Many Requests. Limit is 3 requests per second."},
                headers={"Retry-After": "1"},
            )

        history.append(now)
        response = await call_next(request)
        return response
