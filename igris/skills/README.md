# Igris Agent Capabilities & Caveman System

Detta bibliotek innehåller agentfärdigheter (skills) samt det kirurgiska kodändringsverktyget **Caveman Ultra**.

---

## 1. Caveman Ultra (`caveman.py`)

**Caveman Ultra** är ett Igris-native sök- och ersätt-verktyg designat för B-Rank och A-Rank agenter. Det är konstruerat för att utföra exakta, minimala och säkra kodändringar utan att skriva över hela filer (vilket sparar kontext och förhindrar oavsiktliga regressioner).

### Funktioner
- **Exakt sök/ersätt**: Hittar specifika kodblock och ersätter dem kirurgiskt.
- **Automatisk säkerhetskopiering**: Sparar originalfilen under `.igris/backups/` innan några ändringar skrivs.
- **Dry-run (Förhandsgranskning)**: Genererar och visar en standard-diff utan att faktiskt modifiera filen.
- **Test-hooks**: Kör automatiskt integrationstester efter en lyckad patch.
- **Rollback**: Kan rulla tillbaka den senaste patchen eller alla utförda patchar i sessionen.

### Användning i Python
```python
from igris.skills.caveman import CavemanUltra

# Initiera Caveman med test-hook
caveman = CavemanUltra()

# Utför en kirurgisk ändring
result = caveman.patch(
    file_path="igris/api/main.py",
    old_string="app = FastAPI()",
    new_string="app = FastAPI(title='Igris')"
)

if result.success:
    print(f"Diff genererad:\n{result.diff}")
else:
    print(f"Fel vid patch: {result.error}")
```

---

## 2. Caveman-komprimering (Core Skill)

Caveman-komprimering är en prompt-teknik för att korta ner LLM-utdata och minska tokenanvändningen med upp till **65-75%** utan att förlora teknisk precision.

### Nivåer av komprimering

| Nivå | Beskrivning | Exempel |
|---|---|---|
| `lite` | Tar bort utfyllnadsord, behåller hela meningar. Professionellt och stramt. | "New object reference is created. Use `useMemo` to cache." |
| `full` | Standard. Tar bort artiklar (den, det, en), korta fragment tillåtna. | "New object ref. Use `useMemo` to cache." |
| `ultra` | Extrema fragment, CA-pilar för kausalitet, förkortningar. | "Obj ref → new. `useMemo`." |

---

## 3. Tillgängliga Core Skills

Core-mappen (`igris/skills/core/`) innehåller färdigheter för utvecklarautomatisering:

1. **`changelog-generator`**: Analyserar git-logg och skriver conventional commits till `CHANGELOG.md` automatiskt. (100% automation)
2. **`git-commit-writer`**: Läser staged diffs och genererar conventional commits med mänsklig verifiering av scope/avsikt. (95% automation)
3. **`pr-description-writer`**: Jämför brancher (`git diff main...HEAD`) och genererar PR-beskrivningar med placeholder för affärskontext. (85% automation)
4. **`caveman-stats`**: Läser tokenförbrukning direkt från sessionsloggen.
5. **`caveman-review`**: Granskar kodfiler och ger strukturerad feedback på formatet `fil:rad: 🔴/🟡/🔵`.

---

## 4. Benchmarks & Prestanda

I våra interna tester av Caveman-komprimering såg vi följande minskning av token-kostnader per session:

- **Tokens skickade (input)**: ~20% minskning genom optimerade prompt-mallar.
- **Tokens mottagna (output)**: ~70% minskning genom att helt eliminera artighetsfraser och utfyllnadstext.
- **Svarshastighet (Time-to-first-token)**: Förbättrad med ~30% då kortare svar genereras snabbare av den lokala modellen.
