"""
Spike 001 — WebSocket-streaming server.
A minimal FastAPI app with a /ws WebSocket endpoint that pushes
a numbered message every second.
"""

import asyncio
import logging

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("server")

app = FastAPI()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    logger.info("Client connected")
    try:
        counter = 0
        while True:
            counter += 1
            msg = f"ping-{counter} @ {asyncio.get_event_loop().time():.3f}"
            await websocket.send_text(msg)
            logger.info("Sent: %s", msg)
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        logger.info("Client disconnected")
    except Exception as exc:
        logger.error("WebSocket error: %s", exc)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=9876, log_level="info")
