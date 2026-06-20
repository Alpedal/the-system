"""WebSocket server and background broadcast worker."""

from __future__ import annotations

import asyncio
import json
import logging
from typing import Any

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter(tags=["ws"])
logger = logging.getLogger("igris.api.ws")

# Set of active WebSocket connections
active_connections: set[WebSocket] = set()

# Background broadcast worker task reference
broadcast_task: asyncio.Task | None = None


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Expose WebSocket endpoint for receiving live system updates."""
    await websocket.accept()
    active_connections.add(websocket)
    logger.info(f"WebSocket client connected. Total clients: {len(active_connections)}")
    try:
        # Keep connection open; read messages if client sends any (optional)
        while True:
            _ = await websocket.receive_text()
    except WebSocketDisconnect:
        active_connections.remove(websocket)
        logger.info(f"WebSocket client disconnected. Total clients: {len(active_connections)}")
    except Exception as e:
        logger.error(f"WebSocket connection error: {e}")
        if websocket in active_connections:
            active_connections.remove(websocket)


async def broadcast_loop(app: Any):
    """Background loop polling orchestrator state and broadcasting updates to clients."""
    logger.info("Starting WebSocket status broadcast worker.")
    previous_state_str: str | None = None

    while True:
        try:
            await asyncio.sleep(1.0)
            if not active_connections:
                continue

            orchestrator = app.state.orchestrator
            # Reload state from JSON files to capture updates from CLI or external processes
            # Run in executor to avoid blocking the main thread during disk I/O
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, orchestrator._load_state)

            # Build current state payload
            agents = [a.model_dump(mode="json") for a in orchestrator.agents.values()]
            tasks = [t.model_dump(mode="json") for t in orchestrator.tasks.values()]
            current_state = {
                "agents": agents,
                "tasks": tasks,
            }
            current_state_str = json.dumps(current_state, sort_keys=True)

            # Only broadcast if state changed
            if current_state_str != previous_state_str:
                previous_state_str = current_state_str
                # Broadcast payload to all connected clients
                payload = json.dumps({"event": "status_update", "data": current_state})
                logger.debug(f"Broadcasting status update to {len(active_connections)} clients")
                
                # Copy set to avoid modifying during iteration
                for connection in list(active_connections):
                    try:
                        await connection.send_text(payload)
                    except Exception as e:
                        logger.warning(f"Failed to send to websocket client: {e}")
                        active_connections.discard(connection)

        except asyncio.CancelledError:
            logger.info("WebSocket status broadcast worker stopped.")
            break
        except Exception as e:
            logger.error(f"Error in WebSocket status broadcast loop: {e}")


def start_broadcast_worker(app: Any) -> None:
    """Start the background status broadcast worker task."""
    global broadcast_task
    broadcast_task = asyncio.create_task(broadcast_loop(app))


def stop_broadcast_worker() -> None:
    """Cancel the background status broadcast worker task."""
    global broadcast_task
    if broadcast_task:
        broadcast_task.cancel()
        broadcast_task = None
