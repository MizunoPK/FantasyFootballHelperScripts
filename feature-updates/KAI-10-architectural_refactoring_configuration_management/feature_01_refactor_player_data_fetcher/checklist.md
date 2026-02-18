## Feature Checklist: refactor_player_data_fetcher

**Status:** ✅ ALL RESOLVED (S2.P1.I2 complete — all 4 questions answered)
**Last Updated:** 2026-02-18

---

## Instructions

- Questions are listed in priority order (highest impact first)
- Agent NEVER marks [x] autonomously — only user approval triggers resolution
- Each question resolved one at a time with user confirmation

---

## Open Questions

### Q1: Architecture — Subprocess vs Direct Import?

**Status:** ✅ RESOLVED

**User Answer:** A — Replace subprocess with direct import

**Decision:** `run_player_fetcher.py` will replace `subprocess.run()` + `os.chdir()` with direct Python import and `asyncio.run(player_data_fetcher_main.main(settings_dict))`. Single argparse location in runner. Add `player-data-fetcher/` to `sys.path`; remove `os.chdir()`.

---

### Q2: Keep pydantic BaseSettings or switch to simple dataclass?

**Status:** ✅ RESOLVED

**User Answer:** B — Switch to simple dataclass

**Decision:** Replace `Settings(BaseSettings)` with a `@dataclass`. Remove `pydantic_settings` dependency for settings. `create_settings_from_dict(args_dict)` builds the dataclass from the dict passed by the runner. Env var override (NFL_PROJ_*) is intentionally dropped.

---

### Q3: E2E mode — disable --load-drafted-data to avoid file-not-found?

**Status:** ✅ RESOLVED

**User Answer:** C — E2E mode uses drafted file if present, skips gracefully if not

**Decision:** In E2E mode, if `--load-drafted-data` is True but the drafted data file doesn't exist, skip loading silently (no error). If file exists, load it normally. This applies in E2E mode only — outside E2E, a missing file still raises FileNotFoundError as before.

---

### Q4: fantasy_points_calculator.py hardcoded default season?

**Status:** ✅ RESOLVED

**User Answer:** B — Use current year from datetime

**Decision:** Change default to `season: int = datetime.datetime.now().year`. Remove `from config import NFL_SEASON`. The normal caller (ESPNClient) always passes `season=self.settings.season` explicitly; this default only applies to direct instantiation (e.g., in tests).

---

## Resolved Questions

### Q1: Architecture — Subprocess vs Direct Import?
**Answer:** A — Replace subprocess with direct import
**Impact:** run_player_fetcher.py drops subprocess.run() + os.chdir(); imports player_data_fetcher_main directly; calls asyncio.run(main(settings_dict))

### Q2: Keep pydantic BaseSettings or switch to simple dataclass?
**Answer:** B — Switch to simple dataclass
**Impact:** Settings(BaseSettings) → @dataclass Settings; remove pydantic_settings dependency; create_settings_from_dict() builds from args dict; env var override (NFL_PROJ_*) dropped

### Q3: E2E mode — disable --load-drafted-data to avoid file-not-found?
**Answer:** C — Use file if present, skip gracefully if not
**Impact:** In E2E mode: if load_drafted_data=True but file missing → skip silently. Outside E2E: missing file still raises FileNotFoundError. No hidden override of user's flag value.

---

### Q4: fantasy_points_calculator.py hardcoded default season?
**Answer:** B — Use current year from datetime
**Impact:** `season: int = datetime.datetime.now().year`; remove `from config import NFL_SEASON`; caller (ESPNClient) still passes explicit value

---

## Questions No Longer Needed

{None}
