# Cross-Feature Sanity Check

**Date:** 2026-02-01
**Epic:** improve_configurability_of_scripts (KAI-7)
**Features Compared:** 10 features (F01-F09 + F10 missed requirement)

---

## Critical Architectural Requirement (User Decision - 2026-02-01)

**USER DECISION:** "I similarly want to ensure all scripts remove command line CLI arguments from the config/constants files"

**Applies To:** ALL features (01-10)

**Architectural Pattern (MANDATORY):**
1. **CLI-configurable constants** → Remove from config.py, defaults in argparse (runner scripts)
2. **Non-CLI constants** → Keep in config.py (internal use only)
3. **Parameter passing** → Constructor parameters (dependency injection), NOT config override

**Feature 10 sets the pattern:** Refactors Feature 01 to remove CLI constants from config.py
**Features 02-09 must follow:** Apply same pattern from the start

---

## Prerequisites Check

**All features must complete S2 before S3:**

- [x] Feature 01: S2 COMPLETE (through S7, paused at S8.P1)
- [x] Feature 02: S2 COMPLETE (waiting at Sync Point 1)
- [x] Feature 03: S2 COMPLETE (waiting at Sync Point 1)
- [x] Feature 04: S2 COMPLETE (waiting at Sync Point 1)
- [x] Feature 05: S2 COMPLETE (waiting at Sync Point 1)
- [x] Feature 06: S2 COMPLETE (waiting at Sync Point 1)
- [x] Feature 07: S2 COMPLETE (waiting at Sync Point 1)
- [x] Feature 08: S2 COMPLETE (waiting at Sync Point 1)
- [x] Feature 09: S2 COMPLETE (waiting at Sync Point 1)
- [x] Feature 10: S2 COMPLETE (2026-02-01, spec approved)

**Result:** ✅ ALL FEATURES READY FOR S3

---

## Comparison Matrix

### Category 1: Architectural Pattern Compliance

**CRITICAL:** User requires ALL scripts to follow constructor parameter pattern (not config override)

| Feature | Script | Current Pattern (if implemented) | Planned Pattern | CLI Constants in Config? | Compliance? |
|---------|--------|----------------------------------|-----------------|-------------------------|-------------|
| F01 (player_fetcher) | run_player_fetcher.py | Config override (importlib) | Constructor params (F10 refactor) | YES → will remove | ⚠️ NON-COMPLIANT (F10 fixes) |
| F02 (schedule_fetcher) | run_schedule_fetcher.py | Not yet implemented | Constructor params (planned) | TBD (check spec) | ✅ or ⚠️ TBD |
| F03 (game_data_fetcher) | run_game_data_fetcher.py | Partial argparse exists | Constructor params (planned) | TBD (check spec) | ✅ or ⚠️ TBD |
| F04 (historical_compiler) | run_historical_compiler.py | Partial argparse exists | Constructor params (planned) | TBD (check spec) | ✅ or ⚠️ TBD |
| F05 (win_rate_sim) | run_simulation.py | Partial argparse exists | Constructor params (planned) | TBD (check spec) | ✅ or ⚠️ TBD |
| F06 (accuracy_sim) | run_simulation.py (same) | Partial argparse exists | Constructor params (planned) | TBD (check spec) | ✅ or ⚠️ TBD |
| F07 (league_helper) | run_league_helper.py | No argparse | Constructor params (planned) | TBD (check spec) | ✅ or ⚠️ TBD |
| F08 (integration_tests) | N/A (test framework) | N/A | N/A | N/A | N/A |
| F09 (documentation) | N/A (docs) | N/A | N/A | N/A | N/A |
| F10 (refactor F01) | run_player_fetcher.py | Refactoring F01 | Constructor params | NO (removes all CLI) | ✅ COMPLIANT |

**Action Required:** Review Features 02-07 specs to verify they follow constructor parameter pattern

---

## Step 1: Read All Feature Specs to Extract Patterns

**Need to verify for each feature:**
1. Does spec show constructor parameter pattern or config override?
2. Does spec create/modify config.py with CLI constants?
3. Does spec show argparse defaults or config import?

**Reading now:**
- feature_02_schedule_fetcher/spec.md
- feature_03_game_data_fetcher/spec.md
- feature_04_historical_compiler/spec.md
- feature_05_win_rate_simulation/spec.md
- feature_06_accuracy_simulation/spec.md
- feature_07_league_helper/spec.md

---

## Comparison Categories (To Fill After Reading Specs)

### Category 2: Data Structures

| Feature | Data Added | Config Keys | Conflicts? |
|---------|-----------|-------------|------------|
| F01 | Settings(BaseSettings) class | 23 CLI constants | ◻️ |
| F02 | TBD | TBD | ◻️ |
| F03 | TBD | TBD | ◻️ |
| ... | ... | ... | ... |

### Category 3: Interfaces & Dependencies

| Feature | Main Module | Main() Signature | Settings Flow | Conflicts? |
|---------|------------|------------------|---------------|------------|
| F01 | player_data_fetcher_main.py | main() → main(settings_dict) | F10 refactors | ◻️ |
| F02 | TBD | TBD | TBD | ◻️ |
| ... | ... | ... | ... | ... |

### Category 4: File Locations & Naming

| Feature | Runner Script | Module Directory | Config File? | Conflicts? |
|---------|--------------|------------------|--------------|------------|
| F01 | run_player_fetcher.py | player-data-fetcher/ | config.py (refactored F10) | ◻️ |
| F02 | TBD | TBD | TBD | ◻️ |
| ... | ... | ... | ... | ... |

### Category 5: Configuration Approach

| Feature | Argparse? | Config Override? | Constructor Params? | Compliant? |
|---------|-----------|------------------|---------------------|------------|
| F01 | YES (23 args) | YES (F10 removes) | NO (F10 adds) | ⚠️ F10 fixes |
| F02 | TBD | TBD | TBD | ◻️ |
| ... | ... | ... | ... | ... |

### Category 6: Testing Assumptions

| Feature | E2E Test Mode? | Debug Mode? | Test Runner? | Conflicts? |
|---------|---------------|-------------|--------------|------------|
| F01 | YES (--e2e-test) | YES (--debug) | TBD | ◻️ |
| F02 | TBD | TBD | TBD | ◻️ |
| ... | ... | ... | ... | ... |

---

## Conflicts Identified

**To be populated during systematic comparison**

---

## Resolutions Applied

**To be populated during conflict resolution**

---

---

## CRITICAL CONFLICTS FOUND ⚠️

### Conflict 1: CLI Constants Not Removed from Config/Constants Files (HIGH SEVERITY)

**User Requirement (2026-02-01):** "I similarly want to ensure all scripts remove command line CLI arguments from the config/constants files"

**Applies To:** ALL features (01-10)

**Violation Found:**

**Feature 04 spec.md line 114:** "historical_data_compiler/constants.py (no modifications)"
- **Issue:** Constants.py contains REQUEST_TIMEOUT, RATE_LIMIT_DELAY (CLI-configurable)
- **Problem:** Spec doesn't remove these from constants.py after adding --timeout, --rate-limit-delay args
- **Impact:** Violates architectural requirement

**Suspected Violations (need verification):**
- Feature 03: May reference player-data-fetcher/config.py with CLI constants
- Feature 05: May use simulation constants.py with CLI values
- Feature 06: May use simulation constants.py with CLI values
- Feature 07: May use league_helper/constants.py with CLI values

**Root Cause:** Features 02-09 specs were created BEFORE user clarified this architectural requirement (2026-02-01)

**Resolution Required:**
1. Update ALL feature specs (02-09) to explicitly remove CLI-configurable constants from config/constants files
2. Add requirements similar to Feature 10 R8 (Handle Non-CLI Constants)
3. Refactor internal modules to accept constructor parameters (if applicable)
4. Document architectural pattern in epic-level guidelines

**Architectural Pattern (MANDATORY for ALL features):**
```
✅ CORRECT:
- CLI args defined in argparse with defaults → run_***.py
- Non-CLI constants only in config/constants.py
- Values passed via constructor parameters

❌ INCORRECT (current state of Features 03-07):
- CLI args defined in argparse
- SAME CLI values ALSO in config/constants.py (duplicate)
- Import constants at runtime (not explicit parameter passing)
```

**Example (Feature 04 Historical Compiler):**

**Current Spec (INCORRECT):**
```python
# historical_data_compiler/constants.py
REQUEST_TIMEOUT = 30  # ← CLI-configurable via --timeout, but stays in constants.py
RATE_LIMIT_DELAY = 0.2  # ← CLI-configurable via --rate-limit-delay, but stays

# run_historical_compiler.py
parser.add_argument('--timeout', type=int, default=30)  # ← Duplicate default!
```

**Should Be (CORRECT per user requirement):**
```python
# historical_data_compiler/constants.py
# REQUEST_TIMEOUT removed (now CLI-only)
# RATE_LIMIT_DELAY removed (now CLI-only)
MIN_SUPPORTED_YEAR = 2009  # ← Non-CLI constant, stays
REGULAR_SEASON_WEEKS = 18  # ← Non-CLI constant, stays

# run_historical_compiler.py
parser.add_argument('--timeout', type=int, default=30)  # ← SINGLE source of truth
parser.add_argument('--rate-limit-delay', type=float, default=0.2)

# Pass to compiler via constructor
compiler = HistoricalDataCompiler(timeout=args.timeout, rate_limit=args.rate_limit_delay)
```

---

---

## RESOLUTIONS APPLIED ✅

### Resolution 1: Architectural Pattern Compliance Across All Features

**Conflict:** Features 03, 04, 05, 07 violated epic architectural requirement (CLI constants in config/constants files)

**Action Taken:** Updated all affected feature specs to remove CLI constants from config/constants files

**Specs Updated:**

**Feature 03 (game_data_fetcher):**
- Updated Dependency 3 documentation (player-data-fetcher/config.py)
- Documented that NFL_SEASON, CURRENT_NFL_WEEK will be removed from config.py after Feature 10
- Solution: Use Feature 03's own argparse defaults (hardcoded 2025, 17) instead of importing from config.py
- File: feature_03_game_data_fetcher/spec.md (Dependency 3 section)

**Feature 04 (historical_compiler):**
- **Added:** Requirement 8 - Remove CLI-Configurable Constants from constants.py
- **Modified:** Component #2 (historical_data_compiler/constants.py) → Now shows MODIFY (remove CLI constants)
- **Removes:** REQUEST_TIMEOUT, RATE_LIMIT_DELAY from constants.py
- **Keeps:** MIN_SUPPORTED_YEAR, REGULAR_SEASON_WEEKS (non-CLI)
- File: feature_04_historical_compiler/spec.md (R8 + Components Affected)

**Feature 05 (win_rate_simulation):**
- **Added:** Requirement 8 - Remove CLI-Configurable Constants from Module
- **Removes:** LOGGING_LEVEL from module-level constants (use argparse default)
- **Clarifies:** "Convert LOGGING_LEVEL" means REMOVE constant, use argparse
- File: feature_05_win_rate_simulation/spec.md (R8)

**Feature 06 (accuracy_simulation):**
- **No changes needed** - No CLI constants in separate files
- run_accuracy_simulation.py doesn't have LOGGING_LEVEL or other CLI constants as module-level definitions
- **Status:** ✅ COMPLIANT

**Feature 07 (league_helper):**
- **Added:** Requirement 7 - Remove CLI-Configurable Constants from constants.py
- **Added:** Component #4 (league_helper/constants.py) → MODIFY (remove CLI constants)
- **Removes:** LOGGING_LEVEL, LOGGING_TO_FILE, LOGGING_FILE, RECOMMENDATION_COUNT, MIN_WAIVER_IMPROVEMENT, MIN_TRADE_IMPROVEMENT
- **Keeps:** LOG_NAME, LOGGING_FORMAT, position constants, roster rules, etc.
- File: feature_07_league_helper/spec.md (R7 + Components Affected)

**Verification:**
- All 5 feature specs updated with explicit requirements or documentation
- All specs now align with Feature 10 architectural pattern
- Single source of truth: argparse defaults in runner scripts
- Non-CLI constants remain in config/constants files with clear comments

**Reference Implementation:** Feature 10 spec.md R8 serves as pattern for all features

---

## Final Compliance Status

| Feature | CLI Constants Issue | Resolution Applied | Status |
|---------|---------------------|-------------------|--------|
| F01 | Config override pattern | Feature 10 refactors | ✅ Will be compliant |
| F02 | None (no config file) | N/A | ✅ COMPLIANT |
| F03 | Imports from player-data-fetcher/config.py | Use own argparse defaults | ✅ UPDATED |
| F04 | CLI constants in constants.py | R8 added - remove constants | ✅ UPDATED |
| F05 | LOGGING_LEVEL module constant | R8 added - remove constant | ✅ UPDATED |
| F06 | None | N/A | ✅ COMPLIANT |
| F07 | CLI constants in constants.py | R7 added - remove constants | ✅ UPDATED |
| F08 | N/A (test framework) | N/A | ✅ N/A |
| F09 | N/A (documentation) | N/A | ✅ N/A |
| F10 | Refactoring F01 | Pattern established | ✅ REFERENCE |

**Total Features:** 10
**Violations Found:** 4 (Features 03, 04, 05, 07)
**Violations Resolved:** 4
**Compliant Features:** 10/10 ✅

---

## Additional Conflicts Checked

### Category 2: Data Structures - NO CONFLICTS ✅
- All features add different data/arguments
- No field name conflicts
- No type conflicts

### Category 3: Interfaces & Dependencies - NO CONFLICTS ✅
- Feature 03 dependency on player-data-fetcher/config.py documented and resolved
- All other dependencies are on non-CLI constants only

### Category 4: File Locations - NO CONFLICTS ✅
- Each feature modifies its own files
- No overlapping file modifications

### Category 5: Testing Assumptions - NO CONFLICTS ✅
- All features use --debug and --e2e-test flags consistently
- Test patterns aligned

---

## Step 3.2: Consistency Verification Loop ✅

**After updating specs, verified resolutions don't create new conflicts:**

### Verification 1: Feature 03 Changes
- ✅ No modifications to player-data-fetcher/config.py (only removes imports)
- ✅ Becomes independent of Feature 01/10
- ✅ No cross-feature conflicts

### Verification 2: Feature 04 Changes
- ⚠️ **NEW CONFLICT FOUND:** http_client.py uses REQUEST_TIMEOUT, RATE_LIMIT_DELAY as default parameters
- ✅ **RESOLVED:** Updated spec - http_client.py modified to hardcode defaults (30.0, 0.3)
- ✅ Component #3 changed from "no modifications" to "MODIFY"

### Verification 3: Features 05 & 06
- ✅ Modify different files (no shared code)
- ✅ No conflicts

### Verification 4: Feature 07 Changes
- ⚠️ **NEW CONFLICT FOUND:** Mode managers have 45+ references to Constants (RECOMMENDATION_COUNT, MIN_WAIVER_IMPROVEMENT, MIN_TRADE_IMPROVEMENT)
- ✅ **RESOLVED:** Updated R7 to REQUIRE mode manager refactoring (constructor parameters)
- ⚠️ **SCOPE IMPACT:** Feature 07 expanded from MEDIUM to LARGE

**New Conflicts Found:** 2
**New Conflicts Resolved:** 2
**Final Status:** All conflicts resolved, all specs consistent ✅

---

## Scope Impact Summary

| Feature | Original Scope | Post-S3 Scope | Change | Reason |
|---------|---------------|---------------|--------|--------|
| F03 | SMALL | SMALL | None | Documentation only |
| F04 | SMALL | SMALL+ | Minor | http_client.py modification |
| F05 | MEDIUM | MEDIUM | None | As planned |
| F07 | MEDIUM | LARGE | +Major | 45+ mode manager references |

---

## Status

**Current Step:** Consistency loop complete ✅
**Total Conflicts:** 6 (4 original + 2 from verification)
**Total Resolved:** 6
**Specs Updated:** 4 features with verification fixes
**Next Step:** User approval of S3 results + scope increases
**Then:** Proceed to S4 (Epic Testing Strategy)
