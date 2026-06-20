# Git Sync Rules — hosted-aiOS

> Noll risk för filförlust. Branch + PR + protected main.
> Detta ersätter tidigare "vattentäta regler" som tillät direkt push till main.

## Grundprinciper

1. **Main är skyddad.** Ingen pushar direkt till main — varken människa eller bot.
2. **Alla ändringar går via feature branch → PR → merge.**
3. **Cron gör ENDAST pull.** Aldrig `git add`, aldrig `git commit`, aldrig `git push`.
4. **Aldrig `git push --force`.**
5. **Aldrig `git reset --hard`.**

## Arbetsflöde per person

```bash
# 1. Börja från main
git checkout main
git pull origin main

# 2. Skapa feature branch (namn: <ditt-namn>/<vad-du-gör>)
git checkout -b alpe/rename-and-memory

# 3. Gör dina ändringar...

# 4. Commita och pusha din branch
git add -A
git commit -m "alpe: rename user2→Alpe + populate memory"
git push origin alpe/rename-and-memory

# 5. Öppna PR på GitHub (main ← alpe/rename-and-memory)
# 6. En annan person granskar och godkänner
# 7. Merge på GitHub
```

## Cron-synk (var 5:e minut) — ENDAST pull

```bash
#!/bin/bash
# ENDAST pull. Pushar ALDRIG.

cd /path/to/hosted-aios

# Spara osparade ändringar
git stash

# Pull med rebase
if ! git pull origin main --rebase; then
    echo "[$(date -Iseconds)] CONFLICT vid pull — avbryter" >> shared/memory/sync-log.md
    git rebase --abort
    git stash pop 2>/dev/null
    exit 1
fi

# Återställ osparade ändringar (om inga konflikter med stash)
git stash pop 2>/dev/null

echo "[$(date -Iseconds)] Pull OK" >> shared/memory/sync-log.md
```

## Vid merge-konflikt i PR

Om GitHub rapporterar merge conflict på en PR:

1. **Den som öppnade PR:en** löser konflikten lokalt:
   ```bash
   git checkout main
   git pull origin main
   git checkout alpe/min-branch
   git merge main         # eller rebase
   # ... lös konflikter ...
   git add -A
   git commit -m "merge: resolve conflicts with main"
   git push origin alpe/min-branch
   ```
2. PR:en uppdateras automatiskt. Granska och merge:a.

## GitHub branch protection (administratör sätter upp en gång)

```
Settings → Branches → Add rule → "main":
  ☑ Require a pull request before merging
  ☑ Require approvals (1)
  ☑ Dismiss stale pull request approvals when new commits are pushed
```

## Vad som synkas

- Hela `hosted-aios/` **utom:**
  - `.env` (hemliga nycklar — synkas ALDRIG)
  - `.hermes/plans/` (Hermes interna arbetsfiler)
  - `node_modules/`, `__pycache__/`, `.venv/` (genererade filer)

## Historik — varför detta ersätter gamla reglerna

Tidigare system tillät cron att auto-commita och auto-pusha direkt till main.
Problem:
- Två personer som ändrar samma fil → merge conflict → ena versionen hamnar i `.CONFLICT`-fil
- Halvfärdiga ändringar pushas automatiskt
- Ingen granskning före merge
- Ingen spårbarhet på vem som godkänt vad

Nya systemet: branches + PR:er + skyddad main. Noll risk för att ändringar "försvinner".
