"""
Spike 001 — WebSocket-streaming client.
Connects to /ws, receives messages, and validates they arrive.
"""

import asyncio
import json
import sys

try:
    import websockets
except ImportError:
    print("FAIL: websockets library not installed — run: uv add websockets")
    sys.exit(1)

SERVER_URL = "ws://127.0.0.1:9876/ws"
EXPECTED_COUNT = 3   # how many messages to wait for
TIMEOUT = 15         # seconds


async def run_test() -> dict:
    result = {"outcome": "??", "received": 0, "messages": []}

    try:
        async with asyncio.timeout(TIMEOUT):
            async with websockets.connect(SERVER_URL) as ws:
                for i in range(EXPECTED_COUNT):
                    msg = await ws.recv()
                    result["messages"].append(str(msg))
                    result["received"] += 1
                    print(f"  [{result['received']}] {msg}")

    except asyncio.TimeoutError:
        result["outcome"] = "TIMEOUT"
        print(f"  ✗ Timed out after {TIMEOUT}s (got {result['received']} msgs)")
    except Exception as exc:
        result["outcome"] = f"ERROR: {exc}"
        print(f"  ✗ Connection error: {exc}")
    else:
        result["outcome"] = "PASS" if result["received"] >= EXPECTED_COUNT else "PARTIAL"
        print(f"  ✓ Received {result['received']}/{EXPECTED_COUNT} messages")

    return result


def verdict_from(result: dict) -> str:
    if result["outcome"] == "PASS" and result["received"] >= 1:
        return "VALIDATED"
    if result["received"] > 0:
        return "PARTIAL"
    return "INVALIDATED"


if __name__ == "__main__":
    print("=== Spike 001 — WebSocket Streaming Test ===")
    print(f"  Target: {SERVER_URL}")
    print(f"  Expect: {EXPECTED_COUNT} messages\n")
    r = asyncio.run(run_test())
    v = verdict_from(r)
    print(f"\n  Verdict: {v}")
    print(f"  Outcome: {r['outcome']}")
    print(f"  Received: {r['received']} messages")
    print("=== Done ===")
