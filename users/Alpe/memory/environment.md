# Alpe — Environment

## Hårdvara

| Komponent | Spec |
|-----------|------|
| GPU | NVIDIA RTX 3090 (24 GB VRAM) |
| RAM | 64 GB DDR4 |
| CPU | (ej specificerad) |
| OS | Windows 11 |

## Lokal AI

| Tjänst | Detalj |
|--------|--------|
| Ollama | `localhost:11434` |
| Primär modell | `qwen2.5-coder:32b` (via Igris API proxy) |
| Igris API | `localhost:8420` (uvicorn, OpenAI-kompatibel) |
| Igris API endpoints | `/v1/models`, `/v1/chat/completions` |
| Cloudflared tunnel | `cloudflared tunnel --url http://localhost:8420` → trycloudflare.com |

## Viktiga sökvägar

| Vad | Sökväg |
|-----|--------|
| Igris | `C:\THE SYSTEM\igris\` |
| PYTHONPATH | `C:\THE SYSTEM` |
| North Chat | `C:\THE SYSTEM\north-chat\` |
| North Chat backend | `:8770` (0.0.0.0), PWA `/app` |
| North Chat API | `/api/chat` (API-key auth) |
| Lokal IP | `192.168.0.148` |
| Hermes scripts | `~/AppData/Local/hermes/scripts/` |
| Cloudflared binary | `C:\Program Files (x86)\cloudflared\cloudflared.exe` |

## Verktyg installerade

| Verktyg | Installation | Sökväg/Notering |
|---------|-------------|-----------------|
| GitHub CLI | winget | `C:\Program Files\GitHub CLI\gh` (ej i PATH) |
| Claude Code | winget (v2.1.183) | `claude --bare` |
| Python | 3.11.15 | |
| uv | installerad | Pakethanterare |
| Obsidian vault | | `C:\Users\Liam\Documents\Obsidian Vault` |

## Shannon-backend (Claude Code)

| Inställning | Värde |
|-------------|-------|
| ANTHROPIC_BASE_URL | `https://api.shannon-ai.com` |
| Nyckel | i `~/.bashrc` |

## Övrigt

- Git Bash (MSYS) används som terminal — POSIX-syntax, inte PowerShell
- Python-projekt utan byggsystem körs med `PYTHONPATH`, inte `pip install -e .`
- Windows process management i git-bash: `taskkill /f` feltolkas som sökväg — använd PowerShell-wrapper
