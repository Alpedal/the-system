# Alpe — Projects

## Igris — AI Orchestrator

**Sökväg:** `C:\THE SYSTEM\igris\`
**PYTHONPATH:** `C:\THE SYSTEM`
**API:** `localhost:8420` (uvicorn, OpenAI-kompatibel)

### Arkitektur
- Proxy till Ollama `qwen2.5-coder:32b`
- Endpoints: `/v1/models` + `/v1/chat/completions`
- ObsidianManager (`igris/core/obsidian_manager.py`) integrerad i `orchestrator._deploy_spawn` för auto-skapande
- Regel i `router_prompts.py`
- `OBSIDIAN_VAULT_PATH` i `.env`

### Agenter
- 7 agenter befordrade Level 0 → B-Rank
- Desktop GUI PRIMÄR (streaming: "end-1c" append)
- Systemprompt (svenska, Commander Igris-persona): 5 filer — uppdatera synkront

### Cloudflared
- `C:\Program Files (x86)\cloudflared\cloudflared.exe`
- `cloudflared tunnel --url http://localhost:8420` → trycloudflare.com

---

## North Chat — PWA

**Sökväg:** `C:\THE SYSTEM\north-chat\`
**Backend:** `:8770` (lyssnar på `0.0.0.0`)
**PWA:** `/app`
**API:** `/api/chat` (API-key auth)
**Lokal IP:** `192.168.0.148`

---

## Game Mode Watchdog

**Typ:** Cron-jobb (ID: `a3a00be76485`)
**Script:** `game_mode_watchdog.py`
**Intervall:** varje minut (`no_agent=true`)

### Beteende
1. Kollar efter `steam.exe`, `RiotClientServices.exe`, `LeagueClient.exe`
2. Om något körs → stoppar Ollama
3. Om inget körs och Ollama tidigare stoppades → startar om Ollama (`ollama serve`)
4. Flag-fil: `.game_mode_paused` i scripts/-mappen

### Ollama omstart (Windows git-bash)
```bash
# Stoppa
powershell -Command "Stop-Process -Name ollama -Force"
# Starta
ollama serve
```
