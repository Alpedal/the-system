"""Token authentication for the Igris API."""

from __future__ import annotations

import os

from fastapi import Header, HTTPException, status


DEFAULT_API_TOKEN = "igris-dev-token"


def get_api_token() -> str:
    """Return the configured API token.

    The prototype uses a single shared token so it can be deployed without a
    database. Production token storage can replace this function later.
    """
    return os.getenv("IGRIS_API_TOKEN", DEFAULT_API_TOKEN)


def require_api_token(authorization: str | None = Header(default=None)) -> str:
    """Validate the Authorization header and return the token."""
    expected = get_api_token()
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="missing authorization token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or token != expected:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid authorization token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return token
