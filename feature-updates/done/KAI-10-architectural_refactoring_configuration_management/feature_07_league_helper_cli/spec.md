## Feature Spec: league_helper_cli

**Status:** APPROVED — Gate 3 passed 2026-02-18
**Last Updated:** 2026-02-18

---

## Discovery Context

**Discovery Document:** `../DISCOVERY.md`

### This Feature's Scope (from Discovery)

Wave 2 — Add comprehensive argparse (12+ args), refactor mode managers to accept parameters, E2E test mode. References Feature 01 spec for design patterns.

**Key scope items:**
- Add to run_league_helper.py: ~12 new args + 2 universal args
  - From constants.py: --my-team-name, --recommendation-count, --min-waiver-improvement, --num-runners-up, --min-trade-improvement
  - New args: --mode, --data-folder (and possibly --week, --season, --config-path)
  - Universal: --e2e-test, --log-level (NO separate --debug flag — per user decision 2026-02-18)
- Remove CLI-configurable constants from league_helper/constants.py
- Refactor internal modules to accept parameters instead of importing constants
- Implement --e2e-test mode: run all 5 modes automatically, no user prompts, ≤180 seconds total (also used for debugging)

### Relevant Discovery Decisions

- **Solution Approach:** Constructor parameter pattern; argparse defaults are single source of truth; all mode managers need refactoring
- **Key Constraints:** Largest scope of all Wave 2 features; 10+ modules import from constants; --my-team-name consistent with player_fetcher
- **Dependencies:** Feature 01 spec established design patterns (Settings dataclass, create_settings_from_dict, direct import pattern)

### Relevant User Answers (from Discovery)

| Question | Answer | Impact on This Feature |
|----------|--------|----------------------|
| league_helper team name arg naming | --my-team-name (consistent with player_fetcher) | Use --my-team-name, not --team-name |
| Documentation as separate feature? | No — integrated into S7.P3 + S10 | README.md updates handled in S7.P3 |

---

## Requirements

### REQ-01: CLI Arguments — run_league_helper.py

**Source:** Epic Request + S2 research (constants.py verified, source files read)

Add the following CLI arguments to `run_league_helper.py` via argparse:

**Universal arguments (all 7 scripts):**
| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--e2e-test` | flag | False | E2E test mode: run all 5 modes in ≤180 seconds; also used for debugging (replaces --debug) |
| `--log-level` | str | 'INFO' | Logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL |

**Note:** There is NO separate `--debug` flag. For verbose debug logging, use `--e2e-test --log-level DEBUG`. (User decision 2026-02-18, matches Feature 01 spec.)

**Script-specific arguments (from constants.py):**
| Argument | Type | Default | Source Constant Removed |
|----------|------|---------|------------------------|
| `--my-team-name` | str | 'Sea Sharp' | FANTASY_TEAM_NAME |
| `--recommendation-count` | int | 5 | RECOMMENDATION_COUNT |
| `--min-waiver-improvement` | float | 0 | MIN_WAIVER_IMPROVEMENT |
| `--num-runners-up` | int | 9 | NUM_TRADE_RUNNERS_UP |
| `--min-trade-improvement` | float | 0 | MIN_TRADE_IMPROVEMENT |

**Script-specific arguments (not from constants.py):**
| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--data-folder` | str | '../data' | Path to data directory (league_config.json, players.csv, etc.) |
| `--mode` | str | None | Mode to run: add-to-roster, starter-helper, trade-simulator, modify-player-data, save-calculated-points |
| `--week` | int | None | NFL week to analyze; overrides CURRENT_NFL_WEEK in league_config.json when provided |
| `--season` | int | None | NFL season year; overrides NFL_SEASON in league_config.json when provided |

**Backward-compatible arguments (preserved):**
| Argument | Type | Default | Note |
|----------|------|---------|------|
| `--enable-log-file` | flag | False | Pre-existing arg — preserved as-is |

**Behavior of --week / --season (RESOLVED Q1 — Option A):**
- When omitted (default None): week and season come from `league_config.json` via ConfigManager (existing behavior)
- When provided: the CLI value overrides the config file value after ConfigManager loads the config

**Not added (RESOLVED Q2):** No `--config-path` — ConfigManager auto-resolves from `--data-folder`.
**Not added (RESOLVED Q5):** No `--logging-file` — log file path auto-generated as `logs/league_helper/`, matching Feature 01 behavior.

**NOTE:** Current runner uses subprocess pattern. **Following Feature 01 precedent:** Replace subprocess with direct import — `run_league_helper.py` adds `league_helper/` to `sys.path`, imports `LeagueHelperManager`, and calls `main(settings_dict)`. Remove `subprocess.run()`.

---

### REQ-02: Architecture — runner → main() settings flow

**Source:** Epic Request (Constructor Parameter Pattern) + Feature 01 design precedent

The settings flow must follow Feature 01's established pattern:

```python
# run_league_helper.py
settings_dict = create_settings_dict(args)  # Build dict from parsed args
sys.path.append(str(league_helper_dir))
import LeagueHelperManager
LeagueHelperManager.main(settings_dict)
```

**Sub-requirements:**
- REQ-02a: `main()` in `LeagueHelperManager.py` must accept `settings_dict: dict | None = None`
- REQ-02b: When `settings_dict` is None, `main()` runs its own argparse to build defaults (backward compatibility for direct `python LeagueHelperManager.py` invocation)
- REQ-02c: `create_settings_dict(args)` in `run_league_helper.py` creates dict with all arg values from parsed argparse namespace
- REQ-02d: `create_settings_from_dict(args_dict)` in `LeagueHelperManager.py` builds the Settings dataclass from the dict (see REQ-03)

---

### REQ-03: LeagueHelperManager.py — Settings dataclass

**Source:** Epic Request (DI pattern) + Feature 01 design precedent

Following Feature 01's `@dataclass Settings` pattern:

```python
@dataclass
class Settings:
    my_team_name: str = 'Sea Sharp'
    log_level: str = 'INFO'
    recommendation_count: int = 5
    min_waiver_improvement: float = 0
    num_runners_up: int = 9
    min_trade_improvement: float = 0
    data_folder: str = '../data'
    mode: str | None = None
    week: int | None = None       # None = use league_config.json value (RESOLVED Q1)
    season: int | None = None     # None = use league_config.json value (RESOLVED Q1)
    e2e_test: bool = False
    enable_log_file: bool = False
    # NO config_path field — --data-folder sufficient (RESOLVED Q2)
    # NO debug field — no --debug flag in this epic
```

`create_settings_from_dict(args_dict: dict) -> Settings` function builds Settings from the dict:
```python
def create_settings_from_dict(args_dict: dict) -> Settings:
    return Settings(
        my_team_name=args_dict['my_team_name'],
        log_level=args_dict['log_level'],
        # ... all fields mapped
    )
```

---

### REQ-04: league_helper/constants.py — Remove CLI-configurable constants

**Source:** Epic Request ("Zero CLI constants in config files") + S2 research

**Remove from league_helper/constants.py:**
1. `FANTASY_TEAM_NAME` → default moved to Settings dataclass / argparse default
2. `LOGGING_LEVEL` → replaced by universal --log-level
3. `RECOMMENDATION_COUNT` → default moved to Settings dataclass / argparse default
4. `MIN_WAIVER_IMPROVEMENT` → default moved to Settings dataclass / argparse default
5. `NUM_TRADE_RUNNERS_UP` → default moved to Settings dataclass / argparse default
6. `MIN_TRADE_IMPROVEMENT` → default moved to Settings dataclass / argparse default

**Keep in league_helper/constants.py:**
- `LOG_NAME` — internal logger name (non-configurable)
- `LOGGING_FORMAT` — internal log format (non-configurable)
- `MIN_POSITIONS` — roster validation thresholds (not CLI-appropriate)
- `VALID_TEAMS` — hardcoded trade opponent team list (not CLI-appropriate)
- `RB, WR, QB, TE, K, DST, FLEX` — position string constants
- `ALL_POSITIONS, OFFENSE_POSITIONS, DEFENSE_POSITIONS, WIND_AFFECTED_POSITIONS` — position groupings
- `POSSIBLE_BYE_WEEKS` — algorithm constant

---

### REQ-05: LeagueHelperManager.py — Pass settings to mode managers

**Source:** Epic Request (DI pattern) + S2 research (FANTASY_TEAM_NAME propagation chain)

`LeagueHelperManager.__init__` must accept settings and pass CLI-configurable values to each mode manager:

```python
def __init__(self, data_folder: Path, settings: Settings):
    # ...
    self.add_to_roster_mode_manager = AddToRosterModeManager(
        self.config, self.player_manager, self.team_data_manager,
        recommendation_count=settings.recommendation_count
    )
    self.trade_simulator_mode_manager = TradeSimulatorModeManager(
        data_folder, self.player_manager, self.config,
        my_team_name=settings.my_team_name,
        min_waiver_improvement=settings.min_waiver_improvement,
        num_runners_up=settings.num_runners_up,
        min_trade_improvement=settings.min_trade_improvement
    )
    # Starter Helper, Modify Player Data, Save Calculated Points modes:
    # only need my_team_name if they use it (research found Modify Player Data does)
```

---

### REQ-06: Internal modules — Remove direct constants imports for CLI-configurable values

**Source:** Epic Request + S2 research (import chain verified)

**PlayerManager.py:**
- Line 552: `player_dict['drafted_by'] = Constants.FANTASY_TEAM_NAME`
- Change: Accept `my_team_name: str` as constructor parameter; use `self.my_team_name`

**ModifyPlayerDataModeManager.py:**
- Lines 189, 224, 226, 228: Multiple uses of `Constants.FANTASY_TEAM_NAME`
- Change: Accept `my_team_name: str` as constructor parameter; use `self.my_team_name`

**FantasyTeam.py:**
- Line 192: `player.drafted_by = Constants.FANTASY_TEAM_NAME`
- Change: Accept `my_team_name: str` as constructor parameter; store as `self.my_team_name`; use in `draft_player()` instead of `Constants.FANTASY_TEAM_NAME`
- FantasyTeam is constructed in: `PlayerManager.py` (line 440), `FantasyTeam.py` itself (line 671 — internal copy), and `trade_analyzer.py` (lines 112, 173, 419). All call sites must pass `my_team_name`.

**TradeSimulatorModeManager.py:**
- Lines 210, 282: `Constants.FANTASY_TEAM_NAME`
- Lines 272, 591-597: `Constants.MIN_WAIVER_IMPROVEMENT`
- Lines 342, 502: `Constants.NUM_TRADE_RUNNERS_UP`
- Change: Accept these as constructor parameters

**trade_analyzer.py:**
- 12+ references to `Constants.MIN_WAIVER_IMPROVEMENT` and `Constants.MIN_TRADE_IMPROVEMENT`
- Change: Accept as constructor parameters or function arguments

**AddToRosterModeManager.py:**
- Lines 303, 308: `Constants.RECOMMENDATION_COUNT`
- Change: Accept `recommendation_count: int` as constructor parameter

**All modules:** Remove `from constants import ...` or `import constants as Constants` for CLI-configurable values only. Keep imports for non-CLI constants (positions, etc.).

---

### REQ-07: E2E Test Mode (--e2e-test)

**Source:** Epic Request (Section 3: E2E Test Modes) + EPIC_TICKET.md AC-03 + User decision (2026-02-18)

`--e2e-test` serves two purposes: E2E testing AND debugging during development. There is no separate `--debug` flag.

When `--e2e-test` flag is set:
- Run all 5 interactive modes automatically without user prompts
- Must complete in ≤180 seconds total
- Exit code 0 on success
- No errors in output
- Each mode runs with reduced/debug-sized parameters (recommendation_count=2, num_runners_up=1)

For verbose debug output during development: use `--e2e-test --log-level DEBUG`

**E2E mode implementation approach (RESOLVED Q4 — Option A):**
- Each of the 5 mode managers must implement a non-interactive `execute_e2e()` method
- `LeagueHelperManager` calls each mode's `execute_e2e()` in sequence when `--e2e-test` is set
- No mocking of user input functions — `execute_e2e()` runs without any interactive prompts

**Graceful skip when data missing in E2E mode (S2.P2 cross-feature alignment — 2026-02-18):**
Consistent with Feature 05 and Feature 06 E2E patterns: if required data files are not present, exit gracefully rather than crashing.
```python
if args.e2e_test:
    data_folder = Path(args.data_folder)
    config_path = data_folder / 'league_config.json'
    if not config_path.exists():
        logger.info(f"E2E test mode: league_config.json not found at {config_path} — skipping (exit 0)")
        sys.exit(0)
```
Exit code 0, log an info-level message, no traceback. This prevents CI failures in environments that have not yet run the data collection scripts.

**Precedence rule:** `--e2e-test` overrides `--mode` (runs all modes, not just one)

---

### REQ-08: --log-level behavior

**Source:** Epic Request (universal argument spec)

- `--log-level` accepts: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Default: INFO
- No separate `--debug` flag — for DEBUG logging, use `--log-level DEBUG`

---

### REQ-09: Backward Compatibility

**Source:** Derived requirement (zero regression requirement from EPIC_TICKET.md)

- Running `python run_league_helper.py` (no args) must behave identically to current behavior
- Running `python run_league_helper.py --enable-log-file` must preserve existing behavior
- Running `python league_helper/LeagueHelperManager.py` (direct invocation, no args) must still work
- All 2,744+ existing unit tests must pass after refactoring

---

### REQ-10: Update Tests

**Source:** S2 research (test_LeagueHelperManager.py uses `LeagueHelperManager(data_folder)`)

When `LeagueHelperManager.__init__` signature changes to accept `settings`, update:
- `tests/league_helper/test_LeagueHelperManager.py`: Update constructor calls to pass Settings (or mock settings)
- Any other tests that construct LeagueHelperManager directly

**Note:** tests/integration/test_league_helper_integration.py — assess for impact once constructor signature is finalized.

---

## Acceptance Criteria

- [ ] `python run_league_helper.py --help` displays all 12 arguments
- [ ] `python run_league_helper.py --e2e-test` runs all 5 modes and exits 0 in ≤180 seconds
- [ ] `python run_league_helper.py --e2e-test --log-level DEBUG` enables DEBUG logging during E2E run
- [ ] `python run_league_helper.py --my-team-name "My Team"` uses "My Team" as the fantasy team name throughout
- [ ] `python run_league_helper.py --week 10` overrides league_config.json CURRENT_NFL_WEEK with 10
- [ ] `python run_league_helper.py --recommendation-count 3` shows 3 recommendations in Add to Roster mode
- [ ] `python run_league_helper.py` (no args) behavior identical to current (backward compatible)
- [ ] `python run_league_helper.py --enable-log-file` enables file logging (backward compatible)
- [ ] `python league_helper/LeagueHelperManager.py` (direct invocation, no args) still works
- [ ] `grep -r "subprocess" run_league_helper.py` returns empty
- [ ] `grep "FANTASY_TEAM_NAME\|RECOMMENDATION_COUNT\|MIN_WAIVER_IMPROVEMENT\|NUM_TRADE_RUNNERS_UP\|MIN_TRADE_IMPROVEMENT\|LOGGING_LEVEL" league_helper/constants.py` returns empty
- [ ] `pytest tests/` reports all 2,744+ passed, 0 failed

---

## Open Scope Questions

All resolved — see `checklist.md`.

---

## Files to Modify

| File | Change Type | Complexity |
|------|-------------|------------|
| `run_league_helper.py` | Refactor (subprocess→import, add argparse) | Medium |
| `league_helper/LeagueHelperManager.py` | Refactor (Settings dataclass, main() signature, settings flow) | High |
| `league_helper/constants.py` | Remove 6 CLI-configurable constants | Low |
| `league_helper/util/PlayerManager.py` | Add constructor param (my_team_name) | Medium |
| `league_helper/modify_player_data_mode/ModifyPlayerDataModeManager.py` | Add constructor param (my_team_name) | Medium |
| `league_helper/util/FantasyTeam.py` | Add param (my_team_name) | Low-Medium |
| `league_helper/trade_simulator_mode/TradeSimulatorModeManager.py` | Add constructor params (my_team_name, min_waiver_improvement, num_runners_up) | Medium |
| `league_helper/trade_simulator_mode/trade_analyzer.py` | Add params (min_waiver_improvement, min_trade_improvement) | High (12+ changes) |
| `league_helper/add_to_roster_mode/AddToRosterModeManager.py` | Add constructor param (recommendation_count) | Low-Medium |
| `tests/league_helper/test_LeagueHelperManager.py` | Update constructor calls to pass Settings | Low-Medium |

**Total: ~10 files to modify** (largest refactor scope in Wave 2)
