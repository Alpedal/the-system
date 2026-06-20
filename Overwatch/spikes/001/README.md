# Spike 001 — WebSocket-streaming

**Mål:** Testa om FastAPI kan pusha data till klient via WebSocket.

---

## Test

**Given** en FastAPI-app med en WebSocket-endpoint (`/ws`) som skickar ett meddelande varje sekund  
**When** en klient ansluter och väntar på 3 meddelanden  
**Then** klienten tar emot 3 `ping-{n}`-meddelanden med ~1 sekunds mellanrum

### Resultat

```
=== Spike 001 — WebSocket Streaming Test ===
  Target: ws://127.0.0.1:9876/ws
  Expect: 3 messages

  [1] ping-1 @ 41317.921
  [2] ping-2 @ 41318.937
  [3] ping-3 @ 41319.953
  ✓ Received 3/3 messages

  Verdict: VALIDATED
  Outcome: PASS
  Received: 3 messages
=== Done ===
```

**Verdict:** **VALIDATED** ✅ – WebSocket streaming works. FastAPI pushar data i realtid.

---

## Implementation

| Fil            | Beskrivning                                   |
|----------------|-----------------------------------------------|
| `server.py`    | FastAPI-app med `/ws` WebSocket-endpoint      |
| `test_client.py` | Ansluter, tar emot 3 meddelanden, rapporterar |
| `README.md`    | Denna fil                                     |

## Körinstruktioner

```bash
cd Overwatch/spikes/001

# Starta servern (background)
uv run python server.py &

# Kör testet
uv run python test_client.py
```

**Stödet:** FastAPI + websockets + uvicorn.
