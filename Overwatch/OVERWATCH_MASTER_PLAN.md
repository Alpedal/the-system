# OVERWATCH — MASTER PLAN v0.2.0

> LÄSORDNING: Denna fil först. En levande plan för hela the-system.
> Konsoliderad 2026-06-20 från: OVERWATCH_MASTER_PLAN v0.1.0 + WEBAPP-PROTOTYPE-PLAN + WILLIAM-COLLAB-PLAN
> Dashboard-Plan.md (Alpedals pixel-art desktop-vision) är separat — denna plan gäller webb-API + multi-user.
>
> **Scope:** Webb-API + Webb-UI för Igris multi-user access.
> **Desktop-appen (Tauri/pixel-art)** är Alpedals domän — ej i denna plan.

---

## 1. NULÄGE

Igris fungerar lokalt på Alpedals RTX 3090 (Ryzen 9 3950X, 64GB RAM). Ollama (qwen2.5-coder:32b).

**Constraint:** RTX 3090 har 24GB VRAM. qwen2.5-coder:32b tar ~19GB.
5GB kvar för embedding-modell + overhead. Multi-user = kö-system krävs.

**Vad finns redan:**
- Igris Core: orchestrator, GPU manager, contract validator, CLI
- FastAPI-skelett: health, agents, GPU endpoints — routar men ej kopplat till Igris Core
- Webb-UI prototyp (`web/`): dark dashboard med mockdata, charts, donuts
- 6 sketches i Overwatch/: 3 kasserade (001-003), 3 Solo Leveling (004-006)
- 778 skills (754 security + 14 superpowers + 7 core + 3 agent-defs)
- 83 tester (6 testfiler)
- Git: master branch, senaste commit `35e3f03`

**Saknas för multi-user:**
- WebSocket för live agent-status
- Ollama-proxy via API
- Token-auth mot riktig backend
- Queue-system för singel-GPU
- Webb-UI mot riktig data (ej mock)

---

## 2. SAMARBETE — William + Alpedal + Änner

### 2.1 Arkitekturmål

```
┌─────────────────────────────────────────────────┐
│              Superdator (Alpedal)                │
│                                                  │
│  ┌──────────┐   ┌──────────────────────────┐    │
│  │  Ollama   │   │    Igris Core             │    │
│  │  :11434   │◄──┤    (Orchestrator)         │    │
│  └──────────┘   └──────────┬───────────────┘    │
│                             │                    │
│                    ┌────────▼──────────┐         │
│                    │   Igris API        │         │
│                    │   (FastAPI :8000)  │         │
│                    └────────┬──────────┘         │
│                             │                    │
└─────────────────────────────┼────────────────────┘
                              │ HTTPS / tunnel
              ┌───────────────┼───────────────┐
              │               │               │
         ┌────▼────┐    ┌────▼────┐    ┌────▼────┐
         │ William  │    │ Alpedal │    │ Änne X  │
         │ (Web UI) │    │ (Web UI)│    │ (Web UI)│
         └─────────┘    └─────────┘    └─────────┘
```

### 2.2 Git-workflow

1. Alpedal äger `main` (superdatorn)
2. William + andra jobbar i feature-branches
3. PR → Alpedal reviewar → merge

### 2.3 SSH-nyckel (William)

```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIIxBBVHnU6mHngCPqtcns3zfpNHfOre36DwnzmJ7ABfW williamahlstrom76@gmail.com
```

---

## 3. DESIGN — SKETCHES

6 varianter finns i `Overwatch/sketches/`.

### Round 1 (kasserade — fel universum)
| # | Namn | Varför kass |
|---|------|-------------|
| 001 | Calm Editorial | Linear/Stripe — inte Solo Leveling |
| 002 | Operator Dense | Grafana-dashboard — inte Solo Leveling |
| 003 | Living Machine | Partiklar — inte Solo Leveling |

### Round 2 — Solo Leveling

| Dimension | 004 Solo System | 005 Solo HUD | 006 Shadow Commander |
|-----------|----------------|-------------|---------------------|
| Kärna | System-rutor + stat-block | Gaming HUD + inventory | Shadow Army fantasy |
| Layout | Chat vänster + sidepanel | 3-kolumn: inventory/chat/stats | Sidebar soldater + transmissioner |
| Färg | Blå neon (#6366f1) | Lila/violett (#8b5cf6) | Violet + guld |
| Agent-visning | Rankad lista (S/A/B) | Inventory slots 2x grid | Soldatlista med klass |
| Chatt | System-popups | Command prompt (> ) | Transmissioner |
| GPU | Sidepanel | Stats-panel | "MANA" bar |
| Level | Stats (STR/AGI/INT/PER) | HP/MP bars + LVL badge | Rank S · LV.23 |
| Quest | Quest-logg | Miniquests | Dagliga ordrar |
| Känsla | Manhwa-läsarens UI | RPG-spelarens UI | Jinwoo's krigsrum |

**Rekommendation:** 004 Solo System som bas. Låna HP/MP-bars från 005 och transmissioner från 006.

### Designregler (gäller ALLT webb-UI)

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

**Anti-mönster:** ALDRIG `#FFFFFF`, ALDRIG emojis som UI-element, ALDRIG gradienter, ALDRIG box-shadow, ALDRIG rundade hörn > 4px, INGA animationer som blockerar, INGA ljusa teman.

---

## 4. SPIKES — TEKNISK VALIDERING

Körs INNAN implementation. En spike per teknisk risk.

| # | Spike | Fråga | Risk | Mapp |
|---|-------|-------|------|------|
| 001 | websocket-streaming | FastAPI WS → pusha data till klient? | Hög | `Overwatch/spikes/001/` |
| 002 | ollama-proxy | Proxy:a Ollama via API? Behålls streaming? | Hög | `Overwatch/spikes/002/` |
| 003 | multi-user-tokens | Token-generering + validering funkar? | Medium | `Overwatch/spikes/003/` |
| 004 | gpu-telemetri | Läs nvidia-ml-py och streama? | Medium | `Overwatch/spikes/004/` |

**Spike-format:** Varje spike får `README.md` med:
- Given/When/Then
- Kod (throwaway, <100 rader)
- Verdict: VALIDATED / PARTIAL / INVALIDATED

---

## 5. IMPLEMENTATIONSFASER

Varje fas = Definition of Done. Nästa fas startar EFTER att föregående är klar.

### Fas 1 — API-skelett (KLAR — kräver review)

| # | Task | Fil(er) | Status |
|---|------|---------|--------|
| 1.1 | FastAPI-app + health endpoint | `igris/api/main.py`, `routes/health.py` | KLAR |
| 1.2 | Token-auth middleware | `igris/api/auth.py` | KLAR |
| 1.3 | /agents endpoint (mock-data) | `igris/api/routes/agents.py` | KLAR |
| 1.4 | /gpu endpoint (nvidia-ml-py) | `igris/api/routes/gpu.py` | KLAR |
| 1.5 | WebSocket /ws | `igris/api/ws.py` | SAKNAS |

**TODO:** WS saknas. Auth och data måste verifieras mot Igris Core.

### Fas 2 — Igris-integration (NÄSTA)

| # | Task | Fil(er) | Verifiering |
|---|------|---------|-------------|
| 2.1 | Ollama proxy — /chat endpoint | `igris/api/routes/chat.py` | Skicka prompt → få svar från qwen2.5 |
| 2.2 | Request-kö — en åt gången | `igris/api/queue.py` | 2 samtidiga requests → en köas |
| 2.3 | Live agent-status från Igris Core | `igris/api/routes/agents.py` | Ändra Igris → WS push till klient |
| 2.4 | Rate limiting per token | `igris/api/middleware/rate_limit.py` | 3 requests inom 1s → 429 |

**DoD Fas 2:** Igris svarar via API. WS pushar live-data. Kö hanterar GPU.

### Fas 3 — Webb-UI mot riktig data

| # | Task | Fil(er) | Verifiering |
|---|------|---------|-------------|
| 3.1 | Välj design (004/005/006) | - | William öppnar + väljer |
| 3.2 | Bygg vinnaren (ren HTML/JS) | `igris/web/` | Kommunicerar med API:t |
| 3.3 | Chattgränssnitt | `igris/web/chat.js` | Skicka meddelande → se svar streama |
| 3.4 | Agentöversikt med live-status | `igris/web/agents.js` | WS-uppdateringar syns direkt |
| 3.5 | GPU-bar i realtid | `igris/web/gpu.js` | Visar VRAM-användning live |
| 3.6 | Token-inloggning | `igris/web/auth.js` | Ange token → spara i localStorage |

**DoD Fas 3:** Användare kan logga in, chatta, se agenter, se GPU-status.

### Fas 4 — Exponering (1 dag)

| # | Task | Verifiering |
|---|------|-------------|
| 4.1 | Tunnel (Tailscale/Cloudflare) | HTTPS URL fungerar |
| 4.2 | Dokumentation för Alpedal | `Overwatch/plans/DEPLOY.md` |
| 4.3 | Test från Williams maskin | Öppna HTTPS URL → fungerar |

---

## 6. FILSTRUKTUR — IGRI-SIDAN

```
igris/
├── api/                       # FastAPI-server
│   ├── __init__.py
│   ├── main.py                # FastAPI-app + router
│   ├── auth.py                # Token-validering
│   ├── state.py               # Orchestrator state
│   ├── queue.py               # Request-kö (NY)
│   ├── ws.py                  # WebSocket (SAKNAS)
│   ├── middleware/
│   │   └── rate_limit.py      # Rate limiting (NY)
│   └── routes/
│       ├── agents.py          # /agents (finns)
│       ├── chat.py            # /chat — Ollama-proxy (NY)
│       ├── gpu.py             # /gpu — telemetri (finns)
│       └── health.py          # /health (finns)
├── web/                       # Webb-UI (statiskt)
│   ├── index.html             # Dashboard (finns — mockdata)
│   ├── styles.css             # Dark theme (finns)
│   └── app.js                 # Frontend-logik (finns — mockdata)
└── ... (core/, models/, cli/ — ORÖRDA)
```

**Regel:** Inga ändringar i `igris/core/`, `igris/models/`, `igris/cli/`.
API:t är en READ-ONLY proxy + WebSocket — modifierar inte Igris interna state.

---

## 7. BEROENDEN

```
fastapi>=0.115
uvicorn[standard]>=0.34
websockets>=14
httpx>=0.27
```

Inga Node.js-beroenden — Webb-UI är ren HTML/CSS/JS.

---

## 8. DESIGNBESLUT

| # | Fråga | Val | Status |
|---|-------|-----|--------|
| 1 | Webbserver | FastAPI | Låst |
| 2 | Frontend | Ren HTML/JS vs React | Öppen — avgörs av sketch |
| 3 | Realtid | WebSocket vs SSE | Öppen — spike 001 avgör |
| 4 | Auth | API-nycklar | Låst för prototyp |
| 5 | Exponering | Tailscale vs Cloudflare | Öppen |

---

## ÄNDRINGSLOGG

| Datum | Vem | Ändring | Syfte |
|-------|-----|---------|-------|
| 2026-06-20 | Hermes | v0.2.0 | Konsoliderad från 3 planer + Dashboard-Plan referens |

---

## BOT-FEEDBACK (för röstningssystem)

```
### RÖST: [BOT] — [DATUM]
| Sektion | Röst | Motivering |
|---------|------|------------|
| X. Rubrik | GODKÄNN/AVVISA/ÄNDRA | Text |
```
