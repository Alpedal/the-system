# OVERWATCH — MASTER PLAN v0.1.0

> LÄSORDNING: Denna fil först. Bot-diskussioner i BOT-FEEDBACK längst ner.
> Bas: Alpedals Dashboard-Plan.md · William + Hermes (oteOS) · 2026-06-20
>
> **Scope:** Webb-API + Webb-UI för Igris multi-user access.
> Desktop-appen (Tauri/pixel-art) är Alpedals domän — ej i denna plan.

---

## RÖSTNINGSSYSTEM

| Bot | Vikt | Roll i denna plan |
|-----|------|-------------------|
| Antigravity | 1 | Orkestrator — helhetsbedömning |
| Gemini | 1 | Research — teknikval, omvärldsanalys |
| Hermes | 1 | System audit — filstruktur, skills |
| Claude Code | 1 | Implementation — kodrealism |
| **William** | **3** | Slutgiltigt beslut |

**Format:** GODKÄNN / AVVISA / ÄNDRA med motivering.
Alla GODKÄNN = Låst. Majoritet + William OK = Låst. AVVISA = diskussion krävs.

---

## 1. NULÄGE

Igris fungerar lokalt på Alpedals RTX 3090. Ollama (qwen2.5-coder:32b).
Ingen extern access. Overwatch Dashboard är planerat men ej byggt.

**Constraint:** RTX 3090 har 24GB VRAM. qwen2.5-coder:32b tar ~19GB.
5GB kvar för embedding-modell + overhead. Multi-user = kö-system krävs.

### RÖSTOMRÅDE — 1. Nuläge
> *[Bottar: Är constraint-analysen korrekt? Saknas något?]*

---

## 2. MÅL — WEBBAPP-PROTOTYP

En prototyp som låter 2-3 användare nå Igris via webbläsare:

1. **FastAPI-server** på Alpedals maskin — proxy mot Ollama + Igris Core
2. **WebSocket** — live agent-status, GPU-telemetri
3. **Token-auth** — enkel API-nyckel per användare
4. **Webb-UI** — chattgränssnitt + agentöversikt
5. **Rate limiting** — en aktiv request åt gången (singel-GPU)

### RÖSTOMRÅDE — 2. Mål
> *[Bottar: Rätt scope för prototyp? Något som borde vara MED eller UT?]*

---

## 3. ARKITEKTUR

```
Alpedals maskin (RTX 3090)
┌─────────────────────────────────────────┐
│  Ollama :11434                           │
│    ├── qwen2.5-coder:32b (19GB VRAM)    │
│    ├── llama3.1:8b (4.9GB VRAM)         │
│    └── bge-m3:latest (1.2GB VRAM)       │
│                                          │
│  Igris Core (orchestrator)              │
│         │                                │
│  ┌──────▼──────┐                        │
│  │  FastAPI     │  ← NY: port 8000       │
│  │  /ws (live)  │                        │
│  │  /chat       │                        │
│  │  /agents     │                        │
│  │  /gpu        │                        │
│  └──────┬──────┘                        │
└─────────┼───────────────────────────────┘
          │  HTTPS (Cloudflare Tunnel)
    ┌─────┼─────┐
    ▼     ▼     ▼
  Webbläsare (William, Alpedal, +1)
```

**Tekniska val:**
- FastAPI — Python, samma miljö som Igris
- WebSocket — inbyggt i FastAPI, inget extra bibliotek
- Cloudflare Tunnel — gratis, ingen port forwarding
- SQLite — token-storage, request-kö (ingen PostgreSQL för prototyp)

### RÖSTOMRÅDE — 3. Arkitektur
> *[Bottar: Cloudflare Tunnel vs SSH tunnel vs VPN? SQLite tillräckligt?]*

---

## 4. DESIGNREGLER — WEBB-UI

Gäller ALLA vyer i webbgränssnittet. LÄS FÖRE ALLT UI-ARBETE.

### 4.1 Färger

| Roll | Värde | Användning |
|------|-------|------------|
| Bakgrund | `#0a0a12` | Huvudyta |
| Yta | `#12121e` | Kort, paneler |
| Text primär | `#e3e3e4` (Bone White) | All brödtext |
| Text sekundär | `#888` | Labels, timestamps |
| Accent | `#00d4ff` (cyan) | Länkar, aktiva element |
| Gul varning | `#ffd700` | Igris/Commander |
| Grön | `#44ff44` | Active/success |
| Röd | `#ff4444` | Error/blocked |

### 4.2 Typografi

| Roll | Typsnitt | Vikt | Storlek |
|------|---------|------|---------|
| Headers | Inter | 600 | 18-24px |
| Body | Inter | 400 | 14px |
| Code | JetBrains Mono | 400 | 13px |
| Agent-namn | Inter | 500 | 14px |

### 4.3 Anti-mönster

- ALDRIG `#FFFFFF` — använd Bone White `#e3e3e4`
- ALDRIG emojis som UI-element
- ALDRIG gradienter
- ALDRIG box-shadow på kort
- ALDRIG rundade hörn > 4px
- INGA animationer som blockerar interaktion
- INGA ljusa teman

### RÖSTOMRÅDE — 4. Designregler
> *[Bottar: Färgpalett OK? Saknas något anti-mönster?]*

---

## 5. IMPLEMENTATIONSFASER

Varje fas = Definition of Done. Nästa fas startar EFTER att föregående är GODKÄND.

### Fas 1 — API-skelett (2-3 dagar)

| # | Task | Fil(er) | Verifiering |
|---|------|---------|-------------|
| 1.1 | FastAPI-app + health endpoint | `igris/api/main.py` | `curl :8000/health` → `{"status":"ok"}` |
| 1.2 | Token-auth middleware | `igris/api/auth.py` | `curl :8000/agents` utan token → 401 |
| 1.3 | /agents endpoint (mock-data) | `igris/api/routes/agents.py` | Returnerar JSON-lista med 5 agenter |
| 1.4 | /gpu endpoint (verklig data) | `igris/api/routes/gpu.py` | Anropa nvidia-ml-py, returnera VRAM |
| 1.5 | WebSocket /ws (agent-status) | `igris/api/ws.py` | `wscat :8000/ws` → ping/pong |

**DoD Fas 1:** Alla 5 endpoints svarar. Auth nekar ogiltig token.
**Spikes som måste köras först:** 001 (websocket), 003 (auth), 004 (gpu-telemetri)

### Fas 2 — Igris-integration (3-4 dagar)

| # | Task | Fil(er) | Verifiering |
|---|------|---------|-------------|
| 2.1 | Ollama proxy — /chat endpoint | `igris/api/routes/chat.py` | Skicka prompt → få svar från qwen2.5 |
| 2.2 | Request-kö — en åt gången | `igris/api/queue.py` | 2 samtidiga requests → en köas |
| 2.3 | Live agent-status från Igris Core | `igris/api/routes/agents.py` | Ändra Igris → WS push till klient |
| 2.4 | Rate limiting per token | `igris/api/middleware/rate_limit.py` | 3 requests inom 1s → 429 |

**DoD Fas 2:** Igris svarar via API. WS pushar live-data. Kö hanterar GPU.
**Spikes som måste köras först:** 002 (ollama-proxy)

### Fas 3 — Webb-UI (4-5 dagar)

| # | Task | Fil(er) | Verifiering |
|---|------|---------|-------------|
| 3.1 | HTML/CSS-sketch (3 varianter) | `Overwatch/sketches/` | Öppna i webbläsare → välj vinnare |
| 3.2 | Bygg vinnaren (ren HTML/JS) | `igris/web/index.html` | Kommunicerar med API:t |
| 3.3 | Chattgränssnitt | `igris/web/chat.js` | Skicka meddelande → se svar streama |
| 3.4 | Agentöversikt med live-status | `igris/web/agents.js` | WS-uppdateringar syns direkt |
| 3.5 | GPU-bar i realtid | `igris/web/gpu.js` | Visar VRAM-användning live |
| 3.6 | Token-inloggning | `igris/web/auth.js` | Ange token → spara i localStorage |

**DoD Fas 3:** Användare kan logga in, chatta, se agenter, se GPU-status.
**Verktyg:** `sketch`-skillen för 3.1. Ren HTML/CSS/JS — inget ramverk i prototyp.

### Fas 4 — Exponering (1 dag)

| # | Task | Verifiering |
|---|------|-------------|
| 4.1 | Cloudflare Tunnel | `cloudflared tunnel` → HTTPS URL |
| 4.2 | Dokumentation för Alpedal | `Overwatch/plans/DEPLOY.md` |
| 4.3 | Test från Williams maskin | Öppna HTTPS URL → fungerar |

**DoD Fas 4:** William når Igris från sin dator via HTTPS.

### RÖSTOMRÅDE — 5. Faser
> *[Bottar: Är fasordningen rätt? Saknas någon task? Tidsestimat rimliga?]*

---

## 6. SPIKES — TEKNISK VALIDERING

Körs INNAN implementation. En spike per teknisk risk.

| # | Spike | Fråga | Mapp |
|---|-------|-------|------|
| 001 | websocket-streaming | FastAPI WS → pusha data till klient? | `Overwatch/spikes/001/` |
| 002 | ollama-proxy | Proxy:a anrop via FastAPI? Behålls streaming? | `Overwatch/spikes/002/` |
| 003 | multi-user-tokens | Token-generering + validering? | `Overwatch/spikes/003/` |
| 004 | gpu-telemetri | Läs nvidia-ml-py och streama? | `Overwatch/spikes/004/` |

**Spike-format:** Varje spike får `README.md` med:
- Given/When/Then
- Kod (throwaway, <100 rader)
- Verdict: VALIDATED / PARTIAL / INVALIDATED

### RÖSTOMRÅDE — 6. Spikes
> *[Bottar: Rätt spikes? Saknas någon teknisk risk?]*

---

## 7. FILSTRUKTUR — IGRI-SIDAN

Nya filer att skapa i `igris/`:

```
igris/
├── api/                       ← NY: FastAPI-server
│   ├── __init__.py
│   ├── main.py                ← FastAPI-app + router
│   ├── auth.py                ← Token-validering
│   ├── queue.py               ← Request-kö
│   ├── ws.py                  ← WebSocket-hantering
│   ├── middleware/
│   │   └── rate_limit.py      ← Rate limiting
│   └── routes/
│       ├── agents.py          ← /agents
│       ├── chat.py            ← /chat (Ollama-proxy)
│       └── gpu.py             ← /gpu (telemetri)
├── web/                       ← NY: Webb-UI (statiskt)
│   ├── index.html
│   ├── chat.js
│   ├── agents.js
│   ├── gpu.js
│   └── auth.js
└── ... (befintliga filer orörda)
```

Inga ändringar i `igris/core/`, `igris/models/`, `igris/cli/`.
API:t är en READ-ONLY proxy + WebSocket — modifierar inte Igris interna state.

### RÖSTOMRÅDE — 7. Filstruktur
> *[Bottar: Korrekt separation? Någon fil som borde ligga annorlunda?]*

---

## 8. BEROENDEN

Nya Python-paket (läggs i `igris/requirements.txt`):

```
fastapi>=0.115
uvicorn[standard]>=0.34
websockets>=14
python-jose[cryptography]>=3.3   # JWT-tokens
```

Inga nya Node.js-beroenden — Webb-UI är ren HTML/CSS/JS.

### RÖSTOMRÅDE — 8. Beroenden
> *[Bottar: python-jose rätt val för JWT? Alternativ?]*

---

## 9. DESIGNBESLUT — ATT TA

Frågor som måste besvaras innan Fas 1 startar:

| # | Fråga | Alternativ | Låst? |
|---|-------|------------|-------|
| 1 | Webbserver | FastAPI (vald) vs Node/Express | Låst |
| 2 | Frontend | Ren HTML/JS vs React | Öppen |
| 3 | Realtid | WebSocket (vald) vs SSE | Låst |
| 4 | Auth | API-nycklar (vald) vs OAuth | Låst |
| 5 | Exponering | Cloudflare Tunnel vs SSH tunnel | Öppen |

### RÖSTOMRÅDE — 9. Designbeslut
> *[Bottar: Är de "låsta" besluten rätt? Vilken av de öppna frågorna bör vi driva?]*

---

## BOT-FEEDBACK

> *[Alla bottar: lämna era röster och kommentarer här. Använd formatet nedan.]*
>
> ```
> ### RÖST: [BOT-NAMN] — [DATUM]
> | Sektion | Röst | Motivering / Ändringsförslag |
> |---------|------|------------------------------|
> | X. Rubrik | GODKÄNN / AVVISA / ÄNDRA | Text |
> ```

<!-- BOT-FEEDBACK START -->

### RÖST: Gemini — 2026-06-20
| Sektion | Röst | Motivering / Ändringsförslag |
|---------|------|------------------------------|
| 1. Nuläge | ÄNDRA | VRAM-kalkylen stämmer för qwen2.5:32b, men diagrammet i sektion 3 inkluderar `llama3.1:8b`. Alla tre samtidigt överskrider 24GB. Llama3.1 bör köras på CPU eller bytas mot mindre modell. |
| 2. Mål | GODKÄNN | Bra scope för prototyp. Rate-limiting på en aktiv request i taget är nödvändigt för singel-GPU. |
| 3. Arkitektur | ÄNDRA | Föreslår Tailscale istället för Cloudflare Tunnel. Tailscale är säkrare, har lägre latens (P2P) och kräver ingen publik exponering för 2-3 betrodda användare. |
| 4. Designregler | GODKÄNN | Restriktiva regler är utmärkta för att hålla prototypen snabb, responsiv och enkel att bygga utan ramverk. |
| 5. Faser | GODKÄNN | Logisk uppdelning och rimliga estimat (10-13 dagar totalt). Bra fokus på spikes först. |
| 6. Spikes | ÄNDRA | Lägg till en spike för VRAM-belastning/contention för att verifiera hur Ollama reagerar vid samtidiga LLM/embedding-anrop. |
| 7. Filstruktur | GODKÄNN | Ren separation av api och web utan att störa core. |
| 8. Beroenden | ÄNDRA | Byt `python-jose` mot `PyJWT`. `python-jose` är föråldrat och ej underhållet. `PyJWT` är standard och underhålls aktivt. |
| 9. Designbeslut | ÄNDRA | Lås frontend till ren HTML/JS. Överväg SSE istället för WebSocket för telemetri (enklare, auto-reconnect). Prioritera Tailscale framför Cloudflare. |

<!-- BOT-FEEDBACK SLUT -->

---

## ÄNDRINGSLOGG

| Datum | Bot | Ändring | Syfte |
|-------|-----|---------|-------|
| 2026-06-20 | Hermes | Skapad | Första utkast från Alpedals Dashboard-Plan.md |
