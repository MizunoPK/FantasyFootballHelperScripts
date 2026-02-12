# Research Notes: Feature 02 (league_helper_logging)

**Created:** 2026-02-06
**Feature:** league_helper_logging
**Epic:** KAI-8-logging_refactoring

---

## Research Summary

Completed targeted research for league_helper CLI integration and log quality improvements. Research focused on subprocess wrapper structure, main entry point logging setup, logging constants, CLI precedents, and log quality scope.

**Total Research Time:** ~25 minutes
**Files Examined:** 8 key files
**Code Locations Identified:** Exact lines for all modifications

---

## 1. Subprocess Wrapper Research (run_league_helper.py)

**File:** `/run_league_helper.py`

**Current Implementation:**
- Lines 48-52: subprocess.run() with hardcoded arguments
- Arguments: [sys.executable, str(league_helper_script), DATA_FOLDER]
- No CLI argument forwarding

**Key Findings:**
- Subprocess wrapper calls `league_helper/LeagueHelperManager.py` with DATA_FOLDER argument
- Currently no CLI argument parsing in run_league_helper.py
- Discovery Iteration 5 recommended sys.argv[1:] forwarding (Option B)

**Required Changes:**
1. Import argparse (add to imports)
2. Create ArgumentParser with --enable-log-file flag
3. Parse arguments: args = parser.parse_args()
4. Forward all CLI args to subprocess: `subprocess.run([sys.executable, script, DATA_FOLDER] + sys.argv[1:])`
   - Alternative: Forward only --enable-log-file if present

**Implementation Decision Needed:**
- Q1: Should wrapper forward ALL args via sys.argv[1:] or filter to known args?
  - Option A: Forward all (sys.argv[1:]) - simpler, future-proof
  - Option B: Forward only --enable-log-file - explicit, prevents unexpected args
  - Recommended: Option A (aligns with Discovery Iteration 5)

**Integration with Target Script:**
- LeagueHelperManager.py main() will receive --enable-log-file flag
- main() needs argparse to parse and use flag

---

## 2. Main Entry Point Research (LeagueHelperManager.py)

**File:** `/league_helper/LeagueHelperManager.py`

**Current Logging Setup (lines 192-211):**
```python
def main():
    setup_logger(constants.LOG_NAME, constants.LOGGING_LEVEL, constants.LOGGING_TO_FILE, constants.LOGGING_FILE, constants.LOGGING_FORMAT)

    base_path = Path(__file__).parent.parent
    data_path = base_path / "data"

    leagueHelper = LeagueHelperManager(data_path)
    leagueHelper.start_interactive_mode()
```

**Key Findings:**
- Line 205: setup_logger() called with hardcoded constants from constants.py
- No argparse integration (main() takes no arguments)
- Currently no CLI argument parsing
- Uses get_logger() throughout class (line 70) - no direct setup_logger() calls in __init__

**Required Changes:**
1. Import argparse at top of file
2. Add ArgumentParser to main() with --enable-log-file flag
3. Parse arguments: args = parser.parse_args()
4. Wire flag to setup_logger: `log_to_file=args.enable_log_file`
5. Replace constants.LOGGING_TO_FILE with args.enable_log_file

**CLI Precedent:**
- run_accuracy_simulation.py (lines 154-229) has excellent --log-level example:
  - parser = argparse.ArgumentParser(...)
  - parser.add_argument('--log-level', choices=[...], default=DEFAULT_LOG_LEVEL, help=...)
  - args = parser.parse_args()
  - setup_logger(LOG_NAME, args.log_level.upper(), LOGGING_TO_FILE, ...)
- Can adapt this pattern for --enable-log-file (action='store_true')

**Implementation Pattern:**
```python
# Add to imports
import argparse

def main():
    parser = argparse.ArgumentParser(description="Fantasy Football League Helper")
    parser.add_argument(
        '--enable-log-file',
        action='store_true',
        default=False,
        help='Enable file logging (logs written to logs/league_helper/)'
    )
    args = parser.parse_args()

    # Modify setup_logger call
    setup_logger(
        constants.LOG_NAME,
        constants.LOGGING_LEVEL,
        log_to_file=args.enable_log_file,  # Use CLI flag instead of constants.LOGGING_TO_FILE
        log_file_path=None,  # Let Feature 01's LoggingManager generate path
        log_format=constants.LOGGING_FORMAT
    )

    # Rest of main() unchanged
    base_path = Path(__file__).parent.parent
    data_path = base_path / "data"

    leagueHelper = LeagueHelperManager(data_path)
    leagueHelper.start_interactive_mode()
```

---

## 3. Logging Constants Research (constants.py)

**File:** `/league_helper/constants.py`

**Current Configuration (lines 21-28):**
- LOGGING_LEVEL = 'INFO'
- LOGGING_TO_FILE = False (hardcoded, will be CLI-driven)
- LOG_NAME = "league_helper"
- LOGGING_FILE = './data/log.txt' (old path, Feature 01 auto-generates)
- LOGGING_FORMAT = 'detailed'

**Key Findings:**
- LOGGING_TO_FILE currently hardcoded to False (line 25)
- LOGGING_FILE path is old format (will be replaced by logs/league_helper/league_helper-{timestamp}.log)
- Constants used by LeagueHelperManager.main() (line 205)

**Required Changes:**
- LOGGING_TO_FILE: Keep constant (now serves as fallback default) but NOT used after CLI integration
- LOGGING_FILE: No changes needed (Feature 01 ignores this when log_file_path=None)
- Alternative: Mark LOGGING_TO_FILE as deprecated in comments

**Integration Decision:**
- Q2: Should we deprecate LOGGING_TO_FILE constant or keep as fallback?
  - Option A: Keep as fallback (if no CLI arg, use constant)
  - Option B: Remove constant (always use CLI arg, default False)
  - Recommended: Option A (backward compatibility if script called without CLI)

---

## 4. Integration with Feature 01

**Feature 01 Provides:**
- LineBasedRotatingHandler (line-based rotation, 500 lines, max 50 files)
- Modified setup_logger() signature (same as before, no breaking changes)
- Auto-generated log paths: logs/{logger_name}/{logger_name}-{timestamp}.log
- Integration contracts:
  1. Logger name = folder name (use "league_helper" consistently)
  2. log_file_path=None (let LoggingManager generate path)
  3. log_to_file from CLI (wire --enable-log-file flag)

**Integration Point:**
- LeagueHelperManager.main() line 205: setup_logger() call
- Current: setup_logger(constants.LOG_NAME, constants.LOGGING_LEVEL, constants.LOGGING_TO_FILE, constants.LOGGING_FILE, constants.LOGGING_FORMAT)
- New: setup_logger(constants.LOG_NAME, constants.LOGGING_LEVEL, args.enable_log_file, None, constants.LOGGING_FORMAT)

**Contract Compliance:**
- ✅ Logger name = "league_helper" (matches folder name logs/league_helper/)
- ✅ log_file_path=None (let Feature 01 generate logs/league_helper/league_helper-{timestamp}.log)
- ✅ log_to_file from CLI (args.enable_log_file)

---

## 5. Log Quality Scope

**Research Method:** Grepped for logger.debug/info calls in league_helper/

**Findings:**
- **Total:** 316 logger.debug/info calls across 17 files
- **Breakdown:**
  - LeagueHelperManager.py: 18 calls
  - util/player_scoring.py: 27 calls
  - util/PlayerManager.py: 18 calls
  - util/ConfigManager.py: 21 calls
  - util/TeamDataManager.py: 11 calls
  - util/FantasyTeam.py: 37 calls
  - Mode managers (4 files): 78 calls total
  - Other utils: 106 calls total

**File List (17 files):**
1. LeagueHelperManager.py
2. util/player_scoring.py
3. save_calculated_points_mode/SaveCalculatedPointsManager.py
4. util/PlayerManager.py
5. util/ConfigManager.py
6. util/TeamDataManager.py
7. util/FantasyTeam.py
8. reserve_assessment_mode/ReserveAssessmentModeManager.py
9. util/DraftedDataWriter.py
10. util/GameDataManager.py
11. util/SeasonScheduleManager.py
12. add_to_roster_mode/AddToRosterModeManager.py
13. modify_player_data_mode/ModifyPlayerDataModeManager.py
14. trade_simulator_mode/TradeSimulatorModeManager.py
15. starter_helper_mode/StarterHelperModeManager.py
16. trade_simulator_mode/trade_analyzer.py
17. trade_simulator_mode/trade_file_writer.py

**Sample Log Patterns (PlayerManager.py lines 108-457):**
- DEBUG: "Initializing Player Manager" (line 108)
- DEBUG: "Players CSV path: {path}" (line 132)
- DEBUG: "Player Manager initialized with {N} players, {M} on roster" (line 141)
- DEBUG: "Loaded {N} players from {file}" (line 300)
- DEBUG: "Loaded {N} players from {position_file}" (line 369)
- DEBUG: "Total players loaded: {N}" (line 378)
- DEBUG: "Week {week} max projection (cached): {value} pts" (line 411)
- DEBUG: "Week {week} max projection (calculated): {value} pts" (line 424)

**Quality Evaluation (Preliminary):**
- Most logs follow good DEBUG patterns: data values, counts, initialization
- Need systematic audit against Discovery Iteration 3 criteria
- Estimated KEEP: 70%, UPDATE: 20%, REMOVE: 10% (to be verified during implementation)

**Log Quality Criteria from Discovery (Iteration 3):**

**DEBUG Level:**
- ✅ Function entry/exit with parameters (not excessive - only for complex flows)
- ✅ Data transformations with before/after values
- ✅ Conditional branch taken
- ❌ NOT every variable assignment
- ❌ NOT logging inside tight loops without throttling

**INFO Level:**
- ✅ Script start/complete with configuration
- ✅ Major phase transitions
- ✅ Significant outcomes
- ❌ NOT implementation details
- ❌ NOT every function call

---

## 6. Test Coverage Research

**Integration Test:**
- File: `/tests/integration/test_league_helper_integration.py`
- Creates temp data folder with test CSVs
- Tests end-to-end workflows (draft, starter helper, trade simulator, mode transitions)
- No log-related assertions observed (lines 1-100 examined)

**Impact Assessment:**
- Log quality improvements unlikely to affect integration tests (no log assertions)
- CLI flag changes won't affect tests (tests use LeagueHelperManager class directly, not subprocess)
- May need to verify tests still pass after log changes (functional behavior unchanged)

**Decision:**
- Q3: Should we add log capture to integration tests for verification?
  - Option A: Yes - verify log output matches expected patterns
  - Option B: No - focus on functional behavior, logs are implementation detail
  - Recommended: Option B (keep tests focused on functionality)

---

## 7. Mode Managers Identified

**Mode Managers (6 total, from Glob results):**
1. add_to_roster_mode/AddToRosterModeManager.py
2. starter_helper_mode/StarterHelperModeManager.py
3. trade_simulator_mode/TradeSimulatorModeManager.py
4. modify_player_data_mode/ModifyPlayerDataModeManager.py
5. reserve_assessment_mode/ReserveAssessmentModeManager.py (not in Discovery, exists)
6. save_calculated_points_mode/SaveCalculatedPointsManager.py (not in Discovery, exists)

**Utility Managers (6+ total):**
1. util/PlayerManager.py
2. util/ConfigManager.py
3. util/TeamDataManager.py
4. util/SeasonScheduleManager.py
5. util/GameDataManager.py
6. util/ProjectedPointsManager.py

**Discovery Mentioned vs Actual:**
- Discovery mentioned: LeagueHelperManager, AddToRosterModeManager, StarterHelperModeManager, TradeSimulatorModeManager, ModifyPlayerDataModeManager
- Actual: 2 additional mode managers exist (ReserveAssessmentModeManager, SaveCalculatedPointsManager)
- Discovery mentioned: PlayerManager, ConfigManager, TeamDataManager, DraftedRosterManager, csv_utils, data_file_manager
- Actual: Some utilities mentioned not found, but additional ones exist (SeasonScheduleManager, GameDataManager, ProjectedPointsManager)

**Implementation Decision:**
- Q4: Should log quality audit include all 6 mode managers or only 4 mentioned in Discovery?
  - Option A: All 6 mode managers (comprehensive)
  - Option B: Only 4 from Discovery (scope-limited)
  - Recommended: Option A (system-wide scope per Q6, Discovery may be incomplete)

---

## 8. CLI Flag Design

**From run_accuracy_simulation.py precedent (lines 154-229):**
```python
parser = argparse.ArgumentParser(description="...")
parser.add_argument(
    '--log-level',
    choices=['debug', 'info', 'warning', 'error'],
    default=DEFAULT_LOG_LEVEL,
    help='Logging level ...'
)
args = parser.parse_args()
setup_logger(LOG_NAME, args.log_level.upper(), LOGGING_TO_FILE, ...)
```

**Proposed Design for --enable-log-file:**
```python
parser = argparse.ArgumentParser(description="Fantasy Football League Helper")
parser.add_argument(
    '--enable-log-file',
    action='store_true',
    default=False,
    help='Enable file logging (logs written to logs/league_helper/ with 500-line rotation, max 50 files)'
)
args = parser.parse_args()
setup_logger(LOG_NAME, LOGGING_LEVEL, args.enable_log_file, None, LOGGING_FORMAT)
```

**Key Differences:**
- action='store_true' (boolean flag, not value argument)
- default=False (opt-in per Discovery Q4)
- log_file_path=None (Feature 01 auto-generates path)

---

## 9. Open Questions for User (Preliminary)

**Q1: Subprocess wrapper argument forwarding**
- Should run_league_helper.py forward ALL args (sys.argv[1:]) or only --enable-log-file?
- Recommendation: ALL args (simpler, aligns with Discovery)

**Q2: LOGGING_TO_FILE constant deprecation**
- Keep as fallback default or remove entirely?
- Recommendation: Keep as fallback (backward compatibility)

**Q3: Integration test log assertions**
- Add log capture to integration tests?
- Recommendation: No (keep tests functional, not implementation-focused)

**Q4: Log quality audit scope**
- Include all 6 mode managers or only 4 from Discovery?
- Recommendation: All 6 (comprehensive, matches Discovery Q6 system-wide intent)

**Q5: LOG_NAME consistency**
- Verify "league_helper" (not "LeagueHelper" or "league-helper") for folder naming?
- Recommendation: Use "league_helper" (matches constants.py line 26, Feature 01 contract)

---

## 10. Implementation Checklist (Initial Draft)

**Changes Required:**

**File 1: run_league_helper.py**
- [ ] Import argparse
- [ ] Create ArgumentParser with --enable-log-file flag
- [ ] Parse arguments
- [ ] Forward sys.argv[1:] to subprocess (or filter to known args - pending Q1)

**File 2: league_helper/LeagueHelperManager.py**
- [ ] Import argparse
- [ ] Add ArgumentParser to main() with --enable-log-file flag
- [ ] Parse arguments
- [ ] Wire args.enable_log_file to setup_logger() log_to_file parameter
- [ ] Change log_file_path to None (Feature 01 auto-generates)

**File 3: league_helper/constants.py** (Optional - pending Q2)
- [ ] Add deprecation comment to LOGGING_TO_FILE (if keeping)
- [ ] OR remove LOGGING_TO_FILE constant (if not keeping)

**File 4-20: Log Quality Improvements (17 files, 316 calls)**
- [ ] Systematic audit of all 316 logger.debug/info calls
- [ ] Apply Discovery Iteration 3 criteria
- [ ] Mark KEEP/UPDATE/REMOVE for each call
- [ ] Implement updates

**File N: tests/** (TBD based on Q3)
- [ ] Verify integration tests still pass
- [ ] Update any test assertions affected by log changes (if any exist)

---

## 11. Code Locations Summary

**Key Files to Modify:**

| File | Lines | Changes |
|------|-------|---------|
| run_league_helper.py | 48-52 | Add argparse, forward CLI args |
| league_helper/LeagueHelperManager.py | 205 | Add argparse, wire flag to setup_logger |
| league_helper/constants.py | 25, 27 | Optional deprecation or removal |
| 17 league_helper files | 316 locations | Log quality improvements |

**Integration Points:**
- LeagueHelperManager.main() line 205: setup_logger() call (primary integration with Feature 01)
- run_league_helper.py line 48-52: subprocess.run() args (CLI forwarding)

---

## 12. References

**Feature 01 Spec:**
- File: `feature_01_core_logging_infrastructure/spec.md`
- Key sections: Integration Points (lines 625-675), Interfaces (lines 462-625)

**Discovery Context:**
- File: `../DISCOVERY.md`
- Key sections: Feature 2 scope (lines 471-489), Log quality criteria (lines 144-166)

**CLI Precedent:**
- File: `/run_accuracy_simulation.py`
- Key sections: Lines 27 (import argparse), 154-224 (parser setup), 229 (setup_logger)

**Logging Constants:**
- File: `/league_helper/constants.py`
- Key sections: Lines 21-28 (logging configuration)

---

**Research Complete:** 2026-02-06 21:25
**Next Steps:** Draft spec.md and checklist.md based on research findings
