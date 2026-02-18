# Research Notes: Feature 07 — league_helper_cli

**Created:** 2026-02-18 (S2.P1.I1)
**Researcher:** Secondary-F

---

## 1. Files Researched

| File | Purpose | Key Findings |
|------|---------|--------------|
| `run_league_helper.py` | Runner script | Uses subprocess to call LeagueHelperManager.py; only --enable-log-file arg |
| `league_helper/LeagueHelperManager.py` | Main entry point | 5 modes, data_path hardcoded, LOGGING_LEVEL/LOG_NAME from constants |
| `league_helper/constants.py` | CLI-configurable constants | 6 CLI-configurable + many non-CLI constants |
| `league_helper/util/ConfigManager.py` | Config loader | Loads week+season from league_config.json (NOT from constants) |
| `data/configs/league_config.json` | League config file | Contains CURRENT_NFL_WEEK=17, NFL_SEASON=2025, and all scoring params |
| `league_helper/util/PlayerManager.py` | Player management | Uses FANTASY_TEAM_NAME from constants (line 552) |
| `league_helper/modify_player_data_mode/ModifyPlayerDataModeManager.py` | Mode manager | Uses FANTASY_TEAM_NAME from constants (lines 189, 224, 226, 228) |
| `league_helper/util/FantasyTeam.py` | Fantasy team model | Uses FANTASY_TEAM_NAME from constants (line 192) |
| `league_helper/trade_simulator_mode/TradeSimulatorModeManager.py` | Trade simulator | Uses FANTASY_TEAM_NAME, MIN_WAIVER_IMPROVEMENT, NUM_TRADE_RUNNERS_UP |
| `league_helper/trade_simulator_mode/trade_analyzer.py` | Trade analysis | Uses MIN_WAIVER_IMPROVEMENT (many), MIN_TRADE_IMPROVEMENT (many) |
| `league_helper/add_to_roster_mode/AddToRosterModeManager.py` | Draft mode | Uses RECOMMENDATION_COUNT (lines 303, 308) |
| `tests/league_helper/test_LeagueHelperManager.py` | Unit tests | Tests LeagueHelperManager init with mocked managers |
| `tests/integration/test_league_helper_integration.py` | Integration tests | Exists (not fully read) |

---

## 2. CLI Constants Analysis (league_helper/constants.py)

### CLI-Configurable Constants (will become CLI args)

| Constant | Value | CLI Arg | Used In |
|----------|-------|---------|---------|
| `FANTASY_TEAM_NAME` | `"Sea Sharp"` | `--my-team-name` | PlayerManager, ModifyPlayerDataModeManager, FantasyTeam, TradeSimulatorModeManager |
| `LOGGING_LEVEL` | `'INFO'` | `--log-level` | LeagueHelperManager.main() |
| `RECOMMENDATION_COUNT` | `5` | `--recommendation-count` | AddToRosterModeManager |
| `MIN_WAIVER_IMPROVEMENT` | `0` | `--min-waiver-improvement` | TradeSimulatorModeManager, trade_analyzer |
| `NUM_TRADE_RUNNERS_UP` | `9` | `--num-runners-up` | TradeSimulatorModeManager |
| `MIN_TRADE_IMPROVEMENT` | `0` | `--min-trade-improvement` | trade_analyzer |

### Non-CLI Constants (stay in constants.py)

| Constant | Keep Reason |
|----------|-------------|
| `LOG_NAME` | Internal logger name (non-configurable) |
| `LOGGING_FORMAT` | Internal format string (non-configurable) |
| `MIN_POSITIONS` | Roster validation thresholds (not user-facing per-run) |
| `VALID_TEAMS` | Hardcoded opponent team list for trade simulator |
| `RB, WR, QB, TE, K, DST, FLEX` | Position string constants |
| `ALL_POSITIONS, OFFENSE_POSITIONS, DEFENSE_POSITIONS, WIND_AFFECTED_POSITIONS` | Position groupings |
| `POSSIBLE_BYE_WEEKS` | Algorithm constant |

---

## 3. Current Architecture (Before)

```
run_league_helper.py
  → subprocess.run(sys.executable, league_helper/LeagueHelperManager.py, *sys.argv[1:])
    → LeagueHelperManager.main()
      → argparse (--enable-log-file only)
      → data_path = base_path / "data"  # HARDCODED
      → setup_logger(constants.LOG_NAME, constants.LOGGING_LEVEL, ...)
      → LeagueHelperManager(data_path)
        → ConfigManager(data_folder)  # reads week+season from league_config.json
        → mode managers...
      → leagueHelper.start_interactive_mode()  # interactive menu loop
```

---

## 4. Target Architecture (After)

```
run_league_helper.py
  → parse args (15+ args)
  → settings_dict = create_settings_dict(args)
  → sys.path.append('league_helper/')
  → import LeagueHelperManager
  → LeagueHelperManager.main(settings_dict)  # direct import, no subprocess
    → create_settings_from_dict(settings_dict)  # builds Settings dataclass
    → setup_logger(LOG_NAME, settings.log_level, ...)
    → LeagueHelperManager(data_folder, settings)
      → ConfigManager(data_folder)  # still reads from league_config.json
      → mode managers (receive CLI params via constructor)
      → if settings.e2e_test: run_e2e_mode()
      → elif settings.mode: run_specific_mode(settings.mode)
      → else: start_interactive_mode()
```

---

## 5. Week/Season Source — Critical Finding

`CURRENT_NFL_WEEK` and `NFL_SEASON` come from `data/configs/league_config.json`, NOT from `constants.py`. ConfigManager reads and validates them at startup.

**Implication:** `--week` and `--season` are not in `constants.py`. Discovery.md notes them as potential CLI args. Research says they need to exist to allow CLI override of config file values.

**Open Question (Q1):** Should `--week` and `--season` override `league_config.json` values, or are they only set via the config file?

---

## 6. Five Interactive Modes

| Mode | Menu Text | Class | Directory |
|------|-----------|-------|-----------|
| 1 | Add to Roster | `AddToRosterModeManager` | `add_to_roster_mode/` |
| 2 | Starter Helper | `StarterHelperModeManager` | `starter_helper_mode/` |
| 3 | Trade Simulator | `TradeSimulatorModeManager` | `trade_simulator_mode/` |
| 4 | Modify Player Data | `ModifyPlayerDataModeManager` | `modify_player_data_mode/` |
| 5 | Save Calculated Projected Points | `SaveCalculatedPointsManager` | `save_calculated_points_mode/` |

**Note:** `reserve_assessment_mode/` directory exists but is NOT imported from any Python files — it is an orphaned/experimental directory. Will not be included in scope.

**Interactive input:** Modes use `show_list_selection()` from `util/user_input.py`. E2E mode must bypass interactive inputs.

---

## 7. Internal Module Refactoring Scope

### FANTASY_TEAM_NAME propagation chain

```
constants.FANTASY_TEAM_NAME
  → PlayerManager.py (line 552): player_dict['drafted_by'] = Constants.FANTASY_TEAM_NAME
  → ModifyPlayerDataModeManager.py (lines 189, 224, 226, 228): many uses
  → FantasyTeam.py (line 192): player.drafted_by = Constants.FANTASY_TEAM_NAME
  → TradeSimulatorModeManager.py (lines 210, 282): many uses
```

### MIN_WAIVER_IMPROVEMENT / MIN_TRADE_IMPROVEMENT

```
constants.MIN_WAIVER_IMPROVEMENT + constants.MIN_TRADE_IMPROVEMENT
  → trade_analyzer.py: ~12 references each
  → TradeSimulatorModeManager.py: ~3 references
```

### Refactoring approach

All mode managers that use CLI-configurable constants will receive these as constructor parameters. The values flow from:
```
CLI args → settings_dict → Settings dataclass → LeagueHelperManager → mode manager constructors
```

---

## 8. Existing Tests

- `tests/league_helper/test_LeagueHelperManager.py`: Tests `LeagueHelperManager.__init__(data_folder)`. Tests use mocked ConfigManager, PlayerManager, etc. Will need update when constructor signature changes.
- `tests/integration/test_league_helper_integration.py`: Integration tests (not fully read; need assessment for impact).

---

## 9. Gate 1 Evidence (Research Completeness)

- **Category 1 (EXACT files/classes to modify with line numbers):** ✅
  - `run_league_helper.py` (lines 63-66: subprocess call)
  - `league_helper/LeagueHelperManager.py` (lines 221: constants.LOGGING_LEVEL; lines 228: hardcoded data_path)
  - `league_helper/util/PlayerManager.py` (line 552: FANTASY_TEAM_NAME)
  - `league_helper/modify_player_data_mode/ModifyPlayerDataModeManager.py` (lines 189, 224, 226, 228)
  - `league_helper/util/FantasyTeam.py` (line 192)
  - `league_helper/trade_simulator_mode/TradeSimulatorModeManager.py` (lines 210, 272, 282, 342, 502, 591-597)
  - `league_helper/trade_simulator_mode/trade_analyzer.py` (12+ references)
  - `league_helper/add_to_roster_mode/AddToRosterModeManager.py` (lines 303, 308)
  - `league_helper/constants.py` (remove 6 CLI-configurable constants)

- **Category 2 (READ source code — actual method signatures):** ✅
  - Read `LeagueHelperManager.__init__(data_folder: Path)`
  - Read `LeagueHelperManager.main()` (no params currently)
  - Read `ConfigManager.__init__(data_folder: Path)`

- **Category 3 (Verified data structures from source):** ✅
  - `league_config.json` contains `CURRENT_NFL_WEEK` and `NFL_SEASON` (NOT constants.py)
  - 6 CLI-configurable constants confirmed in constants.py
  - 5 mode managers confirmed in LeagueHelperManager

- **Category 4 (Reviewed DISCOVERY.md for context):** ✅
  - Finding 3 confirms 6 CLI-configurable constants + additional args
  - Wave 2 structure confirmed
  - --my-team-name naming confirmed (Q3 answer from Discovery)
