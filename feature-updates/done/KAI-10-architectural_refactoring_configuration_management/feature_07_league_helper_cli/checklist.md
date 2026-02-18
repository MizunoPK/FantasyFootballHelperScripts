# Checklist: Feature 07 — league_helper_cli

**Status:** APPROVED — Gate 3 passed 2026-02-18
**Created:** 2026-02-18

---

## Resolved Questions

### [x] Q1: Should --week and --season be added as CLI args to override league_config.json?

**Answer:** Option A — Add `--week` and `--season` as CLI args that override `league_config.json` values.

**Spec impact:** Added `--week INT` (default None) and `--season INT` (default None) to REQ-01. None = use config file value; non-None = override config file value. Added `week: int | None` and `season: int | None` to Settings dataclass.

**Status:** RESOLVED (User Answer 2026-02-18)

---

### [x] Q2: Should --config-path be added as a separate CLI arg?

**Answer:** Option B — `--data-folder` only. No `--config-path`. ConfigManager auto-finds `league_config.json` from the data folder.

**Spec impact:** Removed `--config-path` from REQ-01 pending list. No Settings field for config_path.

**Status:** RESOLVED (User Answer 2026-02-18)

---

### [x] Q3: Should --enable-log-file be kept as-is, or renamed to --logging-to-file?

**Answer:** Option A — Keep `--enable-log-file` as-is. Matches Feature 01 behavior. Backward compatible.

**Spec impact:** REQ-01 backward-compatible args table already lists `--enable-log-file` — no change needed.

**Status:** RESOLVED (User Answer 2026-02-18)

---

### [x] Q4: E2E mode — how should interactive user input be bypassed?

**Answer:** Option A — Each mode manager implements a non-interactive `execute_e2e()` method. LeagueHelperManager calls them in sequence during E2E mode.

**Spec impact:** REQ-07 E2E implementation approach updated to Option A.

**Status:** RESOLVED (User Answer 2026-02-18)

---

### [x] Q5: Should --logging-file (log file path) be added?

**Answer:** Option B — Auto-generate only. No `--logging-file`. Matches Feature 01 behavior.

**Spec impact:** `--logging-file` not added to REQ-01. Log file path remains auto-generated as `logs/league_helper/`.

**Status:** RESOLVED (User Answer 2026-02-18)
