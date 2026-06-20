# Alpe — Conventions & Workflows

## Kodstandard (personlig)

### Namngivning
| Typ | Format | Exempel |
|-----|--------|---------|
| Mappar/filer | `kebab-case` | `user-profile/`, `auth-service.ts` |
| Klasser/komponenter | `PascalCase` | `UserProfile`, `AuthService` |
| Funktioner/variabler | `camelCase` | `getUserById`, `isLoggedIn` |
| Konstanter/env | `UPPER_SNAKE_CASE` | `MAX_RETRIES`, `API_BASE_URL` |

### Filstruktur (projekt)
```
project-name/
├── src/
│   ├── components/
│   ├── services/
│   ├── utils/
│   └── types/
├── tests/
├── docs/
└── README.md
```

### Kodregler
- Kommentarblock överst i nya filer (syfte)
- Funktioner: en tydlig, enskild ansvarsuppgift
- Explicit över implicit — inga magic numbers, inga namnlösa booleans
- Hantera fel explicit — aldrig tyst svälja exceptions

---

## Windows-specifika workflows

### Processhantering (git-bash)
`taskkill /f` feltolkas som sökväg. Använd alltid PowerShell-wrapper:
```bash
powershell -Command "Stop-Process -Name ollama -Force"
# eller
powershell -Command "Get-Process ollama* | Stop-Process -Force"
```

### Ollama omstart
1. Stoppa via PowerShell (enligt ovan)
2. `ollama serve` i bakgrunden

### GitHub CLI
```bash
# I Git Bash:
"/c/Program Files/GitHub CLI/gh" auth login
"/c/Program Files/GitHub CLI/gh" <kommando>
```

---

## Python-konventioner

- Projekt utan `pyproject.toml`/`setup.py`: kör med `PYTHONPATH`, inte `pip install -e .`
- Exempel: `PYTHONPATH=/c/LLM python -m igris.cli.main status`
- Windows-sökvägar: `/c/...` (Git Bash), inte `C:\...`

---

## Igris-specifikt

### Desktop GUI
- PRIMÄR interface
- Streaming: "end-1c" append

### Systemprompt
- Svenska, Commander Igris-persona
- 5 filer — måste uppdateras synkront

### Delegering
- "Be Igris läsa X" = skicka till `qwen2.5-coder:32b`

---

## Obsidian Vault

**Extern vault:** `C:\Users\Liam\Documents\Obsidian Vault`
**Struktur:**
```
The-System/
├── Hermes/
│   ├── brain.md
│   └── memory.md
└── Igris/
    ├── brain.md
    ├── memory.md
    └── Igris Agents/
        └── AgentNN/
            ├── brain.md
            └── memory.md
```

---

## Claude Code

- v2.1.183 (winget)
- Shannon backend: `ANTHROPIC_BASE_URL=https://api.shannon-ai.com`
- Körs: `claude --bare`
