# William + Alpedal — Samarbetsplan

> Skapad: 2026-06-20 | Hermes (oteOS) | Version 0.1.0

---

## 1. NULÄGE

Commander Igris är en lokal multi-agent AI-fabrik. Fungerar på Alpedals maskin.
Overwatch Dashboard är planerat men ej byggt.

**Saknas för gemensam tillgång:**
- Webbserver/API (endast localhost Ollama)
- Webb-UI (desktop-app planerad, ej webb)
- Multi-user stöd
- Autentisering

---

## 2. ARKITEKTURMÅL

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
                              │ HTTPS / SSH tunnel
              ┌───────────────┼───────────────┐
              │               │               │
         ┌────▼────┐    ┌────▼────┐    ┌────▼────┐
         │ William  │    │ Alpedal │    │ Kompis  │
         │ (Web UI) │    │ (Web UI)│    │ (Web UI)│
         └─────────┘    └─────────┘    └─────────┘
```

---

## 3. PRIORITERINGSORDNING

### Fas A — API + Multi-user (vecka 1-2)
- [ ] FastAPI-server på superdatorn
- [ ] WebSocket för live agent-status
- [ ] Autentisering (API-nycklar eller enkel token)
- [ ] Rate limiting per användare
- [ ] Request-kö med prioritering

### Fas B — Webb-UI (vecka 2-4)
- [ ] React/Next.js frontend (alternativt Tauri → webb-port)
- [ ] Chattgränssnitt mot Igris/The System
- [ ] Agent-översikt (status, rank, tasks)
- [ ] GPU/VRAM telemetri i realtid

### Fas C — Overwatch-integration (vecka 4-6)
- [ ] Implementera Dashboard-Plan.md mot API
- [ ] Pixel-art Throne Room
- [ ] The Gate (multi-tab chatt)
- [ ] Agent Detail-vyer

### Fas D — Optimering (löpande)
- [ ] Batcha requests för genomströmning
- [ ] KV-cache-delning mellan användare
- [ ] Prioriteringskö för GPU-tid
- [ ] Response streaming (SSE)

---

## 4. GIT-WORKFLOW

1. Alpedal äger `main`-branchen (superdatorn)
2. William + andra jobbar i feature-branches
3. PR → Alpedal reviewar → merge
4. SSH-nycklar krävs för push (se nedan)

**Williams SSH-nyckel (genererad 2026-06-20):**
```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIIxBBVHnU6mHngCPqtcns3zfpNHfOre36DwnzmJ7ABfW williamahlstrom76@gmail.com
```

---

## 5. TEKNISKA BESLUT ATT TA

1. **Webbserver:** FastAPI vs Node/Express?
2. **Frontend:** React/Next.js vs Tauri → webbexport?
3. **Realtidskommunikation:** WebSocket vs SSE?
4. **Autentisering:** Enkel API-nyckel vs OAuth/GitHub login?
5. **Databas:** SQLite (lokalt) vs PostgreSQL (för multi-user)?
6. **Exponering:** SSH tunnel vs Cloudflare Tunnel vs VPN?

---

## 6. OMEDELBARA NÄSTA STEG

1. William lägger till SSH-nyckel på GitHub
2. Alpedal lägger till @dopaminedotmd som collaborator
3. Besluta arkitekturval (punkt 5 ovan)
4. Börja Fas A — FastAPI-server

---

*Detta dokument uppdateras löpande.*
