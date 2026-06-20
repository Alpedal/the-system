# Webapp-prototyp — Igris/The System

> Skapad: 2026-06-20 | Hermes (oteOS) | För William + Alpedal
>
> Denna fil kompletterar Dashboard-Plan.md (Alpedals desktop-vision) med
> en plan för webinterface + API — så att flera användare kan nå Igris.

---

## Mappstruktur (inne i Overwatch/)

```
Overwatch/
├── Dashboard-Plan.md           ← Alpedals pixel-art desktop-vision
├── WILLIAM-COLLAB-PLAN.md      ← William + Alpedal samarbetsplan
├── WEBAPP-PROTOTYPE-PLAN.md    ← Du är här
├── sketches/                   ← UI-mockups (2-3 designvarianter)
├── spikes/                     ← Tekniska experiment
├── plans/                      ← Implementationsplaner
└── demos/                      ← Kreativa UI-demos
```

---

## Skills från oteOS som används

| # | Skill | Används i | Syfte |
|---|---|---|---|
| 1 | `sketch` | sketches/ | 2-3 HTML-mockups, jämför designvarianter |
| 2 | `spike` | spikes/ | Throwaway-experiment — validera teknik |
| 3 | `plan` | plans/ | Strukturerad implementationsplan |
| 4 | `design-systems` | sketches/ | Oteck-designregler (Bone White, typsnitt, inga emojis) |
| 5 | `pretext` | demos/ | Kreativ text/typografi i UI:t (valfritt) |

---

## Faser

### Fas 0 — Designriktning (sketch + design-systems)
Välj hur webbgränssnittet ska se ut — separat från desktop-appen.
- 3 intake-frågor → känsla, referenser, huvudhandling
- 2-3 HTML-varianter
- Head-to-head → William väljer vinnare

### Fas 1 — Teknisk validering (spike)
Testa riskfyllda tekniska frågor först.

| # | Spike | Fråga | Risk |
|---|---|---|---|
| 001 | websocket-streaming | FastAPI WS → live agent-status? | Hög |
| 002 | ollama-proxy | Proxy:a Ollama via API? | Hög |
| 003 | multi-user-tokens | API-nyckel-auth fungerar? | Medium |
| 004 | gpu-telemetri | VRAM/GPU-data streama till klient? | Medium |

### Fas 2 — Implementation (plan)
Bygg själva prototypen.
- FastAPI + WebSocket (pratar med Igris Core)
- Token-auth
- GPU-telemetri
- Webb-UI (React/Next.js eller ren HTML — beroende på sketch)

### Fas 3 — Kreativ finish (pretext, valfritt)
Unika UI-effekter — text som flödar, ASCII, animationer.

---

## Nästa steg

1. William svarar på 3 sketch-frågor → designriktning
2. Bygg 2-3 HTML-varianter i `Overwatch/sketches/`
3. William väljer vinnare → gå vidare till spikes
