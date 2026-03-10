# Sync Guide System

This directory contains the three guides that govern how Shamt improvements flow between projects and the master repo.

---

## Guides in This Directory

| Guide | Purpose |
|-------|---------|
| `separation_rule.md` | Defines what belongs in shared guides vs project-specific configs — the core rule that keeps Shamt generic |
| `export_workflow.md` | How to contribute an improvement from your project back to master (via PR) |
| `import_workflow.md` | What to do after running the import script — validation steps to keep your project consistent |

---

## The Full Sync Cycle

```
You improve a shared guide
        |
        v
Document in .shamt/CHANGES.md
        |
        v
Run audit on modified files (mandatory pre-flight)
        |
        v
Run export script
        |
        v
Open PR to shamt-ai-dev
        |
        v
Master maintainer reviews + runs audit on merged files
        |
        v
PR merged to master
        |
        v
Other projects: run import script
        |
        v
Import script fetches, copies, writes last_sync.conf
        |
        v
Agent runs import validation (this guide)
        |
        v
Project is up to date
```

**Export path:** `export_workflow.md`
**Import path:** `import_workflow.md`
**What to export:** `separation_rule.md`

---

## When to Import

Import at the start of a new epic, or if your guides feel stale. Check `.shamt/last_sync.conf` to see when you last synced, then run the import script if an update seems warranted:

```bash
bash .shamt/scripts/import/import.sh
# or on Windows:
# & ".shamt\scripts\import\import.ps1"
```

---

## Common Issues

**Scripts fail with "Master directory not found":**
Your `.shamt/shamt_master_path.conf` is stale — the master repo has moved or you're on a different machine. Update the file with the current path to your local `shamt-ai-dev` clone:

```bash
echo "/path/to/shamt-ai-dev" > .shamt/shamt_master_path.conf
```

See the Common Situations sections of `export_workflow.md` and `import_workflow.md` for more detail.
