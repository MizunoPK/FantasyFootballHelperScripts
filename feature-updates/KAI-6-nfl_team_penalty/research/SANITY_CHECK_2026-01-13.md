# Stage 3: Cross-Feature Sanity Check

**Epic:** nfl_team_penalty (KAI-6)
**Date:** 2026-01-13
**Total Features:** 2

---

## Purpose

Systematic comparison of ALL features in this epic to identify conflicts, overlaps, and integration issues BEFORE implementation begins.

**Critical Rules:**
- Compare ALL features (not just some)
- Document ALL conflicts found (even if seem minor)
- Resolve conflicts BEFORE getting user sign-off
- User sign-off is MANDATORY

---

## Feature Summary

| Feature # | Name | Status | S2 Complete | Dependencies |
|-----------|------|--------|-------------|--------------|
| Feature 01 | config_infrastructure | S2 Complete | 2026-01-12 | None (first feature) |
| Feature 02 | score_penalty_application | S2 Complete | 2026-01-13 | Feature 01 (blocking) |

---

## Comparison Matrix

### Category 1: Data Structures

**Purpose:** Identify data structure conflicts, type mismatches, and incompatible assumptions

| Aspect | Feature 01: config_infrastructure | Feature 02: score_penalty_application | Conflict? |
|--------|-----------------------------------|---------------------------------------|-----------|
| **New data structures created** | None (uses List[str] and float) | None (uses existing structures) | ✅ No conflict |
| **Modified data structures** | ConfigManager instance variables:<br>- `self.nfl_team_penalty: List[str]`<br>- `self.nfl_team_penalty_weight: float` | Method signatures:<br>- `PlayerScoringCalculator.score_player()` +param<br>- `PlayerManager.score_player()` +param<br>- `ScoredPlayer.reasons` list +entry | ✅ No conflict |
| **Data types used** | - List[str] (team abbreviations)<br>- float (penalty weight 0.0-1.0) | - bool (nfl_team_penalty flag)<br>- Tuple[float, str] (return from _apply) | ✅ No conflict |
| **Type assumptions** | - Teams: uppercase strings (e.g., "LV")<br>- Weight: float range 0.0-1.0<br>- Validated in Feature 01 | - Teams: reads from config (assumes validated)<br>- Weight: reads from config (assumes 0.0-1.0)<br>- Flag: bool (True/False) | ✅ No conflict<br>**Alignment:** F02 correctly assumes F01 validation |
| **Data validation** | - Validates team abbreviations against ALL_NFL_TEAMS<br>- Validates weight numeric and 0.0-1.0 range<br>- Raises ValueError on invalid | - No validation (reads validated values)<br>- Trusts config validation from F01 | ✅ No conflict<br>**Pattern:** F01 validates, F02 consumes (clean separation) |
| **Edge case handling** | - Empty list [] valid<br>- Weight 0.0 valid<br>- Weight 1.0 valid<br>- Missing keys → defaults | - Empty list → no penalty applied<br>- Weight 0.0 → score becomes 0.0<br>- Weight 1.0 → score unchanged<br>- Flag False → skip Step 14 | ✅ No conflict<br>**Aligned edge cases** |

**Summary:** Zero conflicts. Feature 01 provides data structures, Feature 02 consumes them. Type assumptions fully aligned.

---

### Category 2: Interfaces & Dependencies

**Purpose:** Identify interface conflicts, dependency cycles, and integration issues

| Aspect | Feature 01: config_infrastructure | Feature 02: score_penalty_application | Conflict? |
|--------|-----------------------------------|---------------------------------------|-----------|
| **Files modified** | - `ConfigManager.py` (3 sections)<br>- `league_config.json` (1 file)<br>- 9 simulation config JSONs | - `player_scoring.py` (3 sections)<br>- `AddToRosterModeManager.py` (1 line)<br>- `PlayerManager.py` (1 line) | ✅ No conflict<br>**Zero file overlap** |
| **Classes modified** | - ConfigKeys (add constants)<br>- ConfigManager (add attrs + extraction + validation) | - PlayerScoringCalculator (add param + step + method)<br>- PlayerManager (add param passthrough)<br>- AddToRosterModeManager (update call) | ✅ No conflict<br>**Zero class overlap** |
| **New classes created** | None | None | ✅ No conflict |
| **New methods created** | None (modifies existing `_extract_parameters`) | - `_apply_nfl_team_penalty()` (new private method) | ✅ No conflict |
| **Dependencies: F01 depends on** | - `historical_data_compiler.constants.ALL_NFL_TEAMS` (existing) | N/A | ✅ No conflict |
| **Dependencies: F02 depends on** | N/A | - Feature 01 (config infrastructure)<br>- FantasyPlayer.team attribute (existing)<br>- PlayerScoringCalculator (existing)<br>- AddToRosterModeManager (existing) | ✅ No conflict<br>**F02 correctly depends on F01** |
| **Dependency sequencing** | Must complete first (provides config) | Must wait for F01 completion (consumes config) | ✅ No conflict<br>**Spec R9 (F02): "Feature 01 MUST complete S5-S7 before Feature 02 begins S5"** |
| **Integration points** | Provides:<br>- `config.nfl_team_penalty: List[str]`<br>- `config.nfl_team_penalty_weight: float` | Consumes (read-only):<br>- `self.config.nfl_team_penalty`<br>- `self.config.nfl_team_penalty_weight` | ✅ No conflict<br>**Clean provider/consumer pattern** |
| **External dependencies** | None (uses existing constants) | None (all internal) | ✅ No conflict |

**Summary:** Zero conflicts. Perfect file/class separation. F02 correctly depends on F01 (blocking dependency). Integration points aligned.

---

### Category 3: File Locations & Naming

**Purpose:** Identify file naming conflicts, duplicate filenames, and organizational issues

| Aspect | Feature 01: config_infrastructure | Feature 02: score_penalty_application | Conflict? |
|--------|-----------------------------------|---------------------------------------|-----------|
| **New files created** | `tests/league_helper/util/test_ConfigManager_nfl_team_penalty.py` | `tests/league_helper/util/test_player_scoring_nfl_team_penalty.py` | ✅ No conflict<br>**Different filenames** |
| **Modified files (source)** | `league_helper/util/ConfigManager.py` | - `league_helper/util/player_scoring.py`<br>- `league_helper/util/PlayerManager.py`<br>- `league_helper/add_to_roster_mode/AddToRosterModeManager.py` | ✅ No conflict<br>**Zero file overlap** |
| **Modified files (config)** | - `data/configs/league_config.json`<br>- 9 simulation config JSONs | None (F01 handles all config file updates) | ✅ No conflict |
| **Modified files (tests)** | None (new test file only) | None (new test file only) | ✅ No conflict |
| **Naming conventions** | - ConfigManager pattern: `test_ConfigManager_{feature}.py`<br>- Config keys: `NFL_TEAM_PENALTY` (uppercase) | - Scoring pattern: `test_player_scoring_{feature}.py`<br>- Method: `_apply_nfl_team_penalty()` (lowercase) | ✅ No conflict<br>**Different naming contexts** |
| **File paths** | All in `league_helper/util/`, `data/configs/`, `simulation/simulation_configs/` | All in `league_helper/util/`, `league_helper/add_to_roster_mode/` | ✅ No conflict |

**Summary:** Zero conflicts. All filenames unique. No duplicate paths. Naming conventions aligned with codebase patterns.

---

### Category 4: Configuration Keys

**Purpose:** Identify duplicate config keys, conflicting defaults, and config schema issues

| Aspect | Feature 01: config_infrastructure | Feature 02: score_penalty_application | Conflict? |
|--------|-----------------------------------|---------------------------------------|-----------|
| **New config keys added** | - `NFL_TEAM_PENALTY`<br>- `NFL_TEAM_PENALTY_WEIGHT` | None (reads keys from F01) | ✅ No conflict |
| **Config key types** | - `NFL_TEAM_PENALTY`: List[str]<br>- `NFL_TEAM_PENALTY_WEIGHT`: float | Reads same types from config | ✅ No conflict |
| **Config key defaults** | - `NFL_TEAM_PENALTY`: [] (empty list)<br>- `NFL_TEAM_PENALTY_WEIGHT`: 1.0 (no penalty) | Assumes same defaults if missing | ✅ No conflict |
| **league_config.json values** | User-specific:<br>- `["LV", "NYJ", "NYG", "KC"]`<br>- `0.75` | Reads user-specific values | ✅ No conflict |
| **Simulation config values** | Default (objective):<br>- `[]` (empty)<br>- `1.0` (no penalty) | Simulations use flag=False (skip penalty) | ✅ No conflict<br>**Defense in depth: JSON defaults + flag defaults** |
| **Config validation** | - Type checks (list, numeric)<br>- Range checks (0.0-1.0)<br>- Team abbreviation checks (ALL_NFL_TEAMS) | Trusts F01 validation | ✅ No conflict<br>**F02 safely assumes validated values** |
| **Backward compatibility** | Uses `.get()` with defaults (old configs work) | Parameter defaults to False (old code works) | ✅ No conflict<br>**Both features backward compatible** |

**Summary:** Zero conflicts. F01 owns config keys, F02 reads them. Validation happens in F01 only (clean separation). Defaults aligned.

---

### Category 5: Algorithms & Logic

**Purpose:** Identify algorithmic conflicts, calculation order issues, and logical inconsistencies

| Aspect | Feature 01: config_infrastructure | Feature 02: score_penalty_application | Conflict? |
|--------|-----------------------------------|---------------------------------------|-----------|
| **Core algorithm** | Config loading and validation:<br>1. Extract from JSON with `.get()`<br>2. Validate type (isinstance)<br>3. Validate values (range/team check)<br>4. Raise ValueError on invalid | Penalty application:<br>1. Check if team in penalty list<br>2. If yes, multiply score by weight<br>3. Return (new_score, reason) or (score, "")<br>4. Add reason to list, log | ✅ No conflict<br>**Different responsibilities** |
| **Execution order** | Config loading happens FIRST (during ConfigManager instantiation) | Scoring happens LATER (during Add to Roster mode, after config loaded) | ✅ No conflict<br>**F01 runs before F02 (correct sequence)** |
| **Calculation dependencies** | Independent (loads config only) | Depends on config values from F01 | ✅ No conflict<br>**F02 correctly depends on F01 output** |
| **Side effects** | - Raises ValueError on invalid config<br>- Logs config loading (if enabled) | - Modifies player_score (multiplication)<br>- Adds reason string<br>- Logs debug message | ✅ No conflict<br>**Non-overlapping side effects** |
| **Mode isolation** | None (config loaded for all modes) | Isolated to Add to Roster mode only (flag=True) | ✅ No conflict<br>**F02 correctly implements mode isolation** |
| **Timing in scoring flow** | N/A (config loading, not scoring) | Step 14 (after all 13 existing steps) | ✅ No conflict |
| **Conditional logic** | - If key missing → use default<br>- If value invalid → raise error | - If flag False → skip Step 14<br>- If team not in list → no penalty<br>- If team in list → apply penalty | ✅ No conflict<br>**Clear conditionals, no overlap** |

**Summary:** Zero conflicts. F01 loads/validates config, F02 uses config values. Execution order correct. Side effects non-overlapping.

---

### Category 6: Testing Assumptions

**Purpose:** Identify conflicting test assumptions, duplicate test scenarios, and integration test gaps

| Aspect | Feature 01: config_infrastructure | Feature 02: score_penalty_application | Conflict? |
|--------|-----------------------------------|---------------------------------------|-----------|
| **Test file names** | `test_ConfigManager_nfl_team_penalty.py` | `test_player_scoring_nfl_team_penalty.py` | ✅ No conflict<br>**Different files** |
| **Test scope** | Config loading and validation only | Scoring logic and penalty application only | ✅ No conflict<br>**Clear separation** |
| **Valid input scenarios** | - Valid teams + valid weight<br>- Missing keys (defaults)<br>- Empty list (valid)<br>- Weight 0.0/1.0 (boundaries) | - Team in list + flag True (penalty applied)<br>- Team not in list (no penalty)<br>- Flag False (skip penalty)<br>- Empty list (no penalty) | ✅ No conflict<br>**F02 tests assume F01 validation works** |
| **Invalid input scenarios** | - Invalid team abbreviations → ValueError<br>- Weight > 1.0 → ValueError<br>- Weight < 0.0 → ValueError<br>- Wrong types → ValueError | None (assumes F01 validated values) | ✅ No conflict<br>**F01 owns validation testing** |
| **Edge case testing** | - Empty list []<br>- Weight 0.0<br>- Weight 1.0<br>- Missing keys | - Empty list [] → no penalty<br>- Weight 0.0 → score becomes 0.0<br>- Weight 1.0 → score unchanged<br>- Flag False → skip | ✅ No conflict<br>**Complementary edge cases** |
| **Integration assumptions** | Assumes ConfigManager loads correctly | Assumes config values validated by F01 | ✅ No conflict<br>**F02 trusts F01** |
| **Simulation testing** | Tests that simulation configs load with defaults ([], 1.0) | Tests that simulations work after adding parameter (backward compatibility check) | ✅ No conflict<br>**Complementary simulation tests** |
| **Mode isolation testing** | N/A (config infrastructure) | Tests that penalty only applies in Add to Roster mode (flag True), not other modes | ✅ No conflict |
| **Coverage targets** | 100% of validation logic, extraction logic | 100% of _apply_nfl_team_penalty method, Step 14 conditional | ✅ No conflict<br>**Non-overlapping code coverage** |

**Summary:** Zero conflicts. Test files separate. F01 tests validation, F02 tests application. Edge cases complementary. Integration assumptions aligned.

---

## Conflict Summary

### Total Conflicts Found: 0

**Category 1: Data Structures** - ✅ 0 conflicts (6/6 aspects aligned)
**Category 2: Interfaces & Dependencies** - ✅ 0 conflicts (9/9 aspects aligned)
**Category 3: File Locations & Naming** - ✅ 0 conflicts (6/6 aspects aligned)
**Category 4: Configuration Keys** - ✅ 0 conflicts (7/7 aspects aligned)
**Category 5: Algorithms & Logic** - ✅ 0 conflicts (7/7 aspects aligned)
**Category 6: Testing Assumptions** - ✅ 0 conflicts (9/9 aspects aligned)

---

## Alignment Strengths

### 1. Clean Separation of Concerns
- **Feature 01:** Config infrastructure (loading, validation, storage)
- **Feature 02:** Score application (consumption, calculation, transparency)
- **Zero overlap in responsibilities**

### 2. Perfect Provider/Consumer Pattern
- **Feature 01 provides:** Validated config values (read-only access)
- **Feature 02 consumes:** Config values (trusts validation)
- **No circular dependencies**

### 3. Zero File Overlap
- Feature 01: ConfigManager.py, config JSON files
- Feature 02: player_scoring.py, AddToRosterModeManager.py, PlayerManager.py
- **No file modified by both features**

### 4. Aligned Type Assumptions
- Both features agree: teams are uppercase strings, weight is float 0.0-1.0
- Feature 01 validates, Feature 02 trusts validation
- **Zero type conflicts**

### 5. Correct Dependency Sequencing
- Feature 02 spec explicitly states: "Feature 01 MUST complete S5-S7 before Feature 02 begins S5"
- Blocking dependency correctly documented in both specs
- **No risk of implementation conflicts**

### 6. Complementary Edge Case Handling
- Feature 01: Tests empty list, boundaries (0.0, 1.0), invalid values
- Feature 02: Tests same edge cases from application perspective
- **Comprehensive coverage across features**

### 7. Defense in Depth (Simulation Compatibility)
- Feature 01: Simulation configs use defaults ([], 1.0)
- Feature 02: Simulations use flag=False (skip penalty)
- **Double protection: JSON defaults + code defaults**

---

## Integration Verification

### F01 → F02 Data Flow

```
Feature 01 (Config Infrastructure):
  ConfigManager loads league_config.json
  → Extracts NFL_TEAM_PENALTY = ["LV", "NYJ", "NYG", "KC"]
  → Extracts NFL_TEAM_PENALTY_WEIGHT = 0.75
  → Validates (team check, weight range)
  → Stores in self.nfl_team_penalty, self.nfl_team_penalty_weight

Feature 02 (Score Application):
  AddToRosterModeManager calls score_player(nfl_team_penalty=True)
  → PlayerScoringCalculator.score_player() executes Steps 1-13
  → Step 14: if nfl_team_penalty:
      → _apply_nfl_team_penalty(player, score)
      → Checks if player.team in self.config.nfl_team_penalty
      → If yes: score *= self.config.nfl_team_penalty_weight
      → Returns (new_score, reason)
  → Reason added to ScoredPlayer.reasons list
  → User sees reduced score in Add to Roster recommendations
```

**Data flow verification:** ✅ Complete, no breaks, all integration points aligned

---

## Risk Assessment

### Implementation Risks

**Risk 1: Timing Dependency**
- **Description:** F02 cannot be implemented until F01 is complete
- **Mitigation:** Spec R9 (F02) explicitly requires F01 S5-S7 complete before F02 S5 starts
- **Status:** ✅ Documented and enforced

**Risk 2: Type Mismatch**
- **Description:** F02 might expect different types than F01 provides
- **Mitigation:** Both specs agree on List[str] and float types, F01 validates
- **Status:** ✅ No risk (types aligned)

**Risk 3: Validation Gap**
- **Description:** F02 might receive invalid values if F01 validation incomplete
- **Mitigation:** F01 validates all edge cases (type, range, team abbreviations)
- **Status:** ✅ No risk (comprehensive validation)

**Risk 4: Mode Isolation Failure**
- **Description:** Penalty might accidentally apply to other modes
- **Mitigation:** F02 uses explicit flag (default False), only Add to Roster sets True
- **Status:** ✅ No risk (flag-based isolation + test coverage)

**Risk 5: Simulation Breakage**
- **Description:** Simulations might break after adding parameter
- **Mitigation:** Backward compatible (default False), simulation configs have defaults
- **Status:** ✅ No risk (F02 Requirement 9 addresses this)

### Overall Risk Level: **LOW**

All risks mitigated through:
- Explicit dependency documentation
- Type alignment verification
- Comprehensive validation in F01
- Flag-based mode isolation
- Backward compatibility design

---

## Recommendations

### 1. Proceed to S4 (Epic Testing Strategy)
- **Reason:** Zero conflicts found across all 6 categories
- **Confidence:** HIGH (44/44 aspects aligned)
- **Blockers:** None

### 2. Maintain Feature Sequencing
- **Requirement:** Feature 01 S5-S7 MUST complete before Feature 02 S5 starts
- **Enforcement:** S5 guide will verify F01 completion before allowing F02 to start
- **Critical:** Do NOT start F02 implementation until F01 is fully done (all tests passing, committed)

### 3. Integration Testing During S6 (Epic Final QC)
- **Scenario 1:** End-to-end flow (config load → scoring → recommendations)
- **Scenario 2:** User changes penalty list → scores update correctly
- **Scenario 3:** Simulations unaffected (no penalty applied)
- **Add to:** epic_smoke_test_plan.md during S4

### 4. No Spec Changes Needed
- **Reason:** Zero conflicts means specs are already aligned
- **Action:** Proceed with existing specs (no modifications)
- **Verification:** Both specs approved by user (F01: 2026-01-12, F02: 2026-01-13)

---

## Step 3 (Conflict Resolution)

**Status:** ✅ SKIPPED (zero conflicts to resolve)

**Justification:** Comprehensive 6-category comparison found zero conflicts across 44 aspects. No resolution needed.

---

## Step 4 (Plan Summary)

### Epic Implementation Plan

**Epic Goal:** Add NFL team penalty system to Add to Roster mode

**Feature Breakdown:**
1. **Feature 01 (config_infrastructure):** Add config settings to ConfigManager
2. **Feature 02 (score_penalty_application):** Apply penalty in scoring algorithm

**Implementation Sequence:**
```
S4 (Epic Testing Strategy)
  ↓
S5-S7 (Feature 01)
  - S5: Implementation planning (28 iterations)
  - S6: Implementation execution (all code + tests)
  - S7: Post-implementation (smoke test + 3 QC rounds + commit)
  ↓
S5-S7 (Feature 02)
  - S5: Implementation planning (28 iterations)
  - S6: Implementation execution (all code + tests)
  - S7: Post-implementation (smoke test + 3 QC rounds + commit)
  ↓
S8 (Epic Final QC)
  - Execute epic_smoke_test_plan.md
  - 3 QC rounds (restart if ANY issues)
  - User testing (MANDATORY - must report zero bugs)
  ↓
S9 (Epic Cleanup)
  - Run all unit tests (100% pass required)
  - S9.5: Guide updates (analyze lessons, create GUIDE_UPDATE_PROPOSAL.md, user approval, apply)
  - Create PR
  - Merge after user approval
  - Update EPIC_TRACKER.md
  - Move epic to done/ folder
```

**Critical Gates:**
- ✅ Gate 3 (F01): User approved checklist (2026-01-12)
- ✅ Gate 3 (F02): User approved checklist (2026-01-13)
- ⏳ Gate 4.5: User must approve epic_smoke_test_plan.md (S4)
- ⏳ Gate 5 (F01): User must approve implementation_plan.md (S5a)
- ⏳ Gate 5 (F02): User must approve implementation_plan.md (S5a)
- ⏳ User Testing: Must report zero bugs before S9 (S8 Step 6)

**Integration Points:**
1. Feature 01 provides: `config.nfl_team_penalty`, `config.nfl_team_penalty_weight`
2. Feature 02 consumes: Same config attributes (read-only)
3. Data flow: ConfigManager → PlayerScoringCalculator → AddToRosterModeManager → User

**Success Criteria:**
- All unit tests pass (100%)
- User can configure penalty list and weight in league_config.json
- Add to Roster mode shows reduced scores for penalized teams
- Other modes unaffected (draft, optimizer, trade)
- Simulations remain objective (use defaults [], 1.0)
- Scoring reasons show penalty transparency ("NFL Team Penalty: LV (0.75x)")

---

## Step 5 (User Sign-Off)

**Status:** ⏳ PENDING (awaiting user approval)

**Ready for user review:** ✅ YES

**User must confirm:**
1. Zero conflicts found across 6 categories (44/44 aspects aligned)
2. Feature 01 → Feature 02 sequencing is correct
3. Integration points are clear
4. Risk assessment is acceptable
5. Proceed to S4 (Epic Testing Strategy)

**User approval required before proceeding to S4**

---

## Notes

**S3 Analysis Duration:** Approximately 45 minutes (comprehensive 6-category comparison)

**Confidence Level:** HIGH
- Both features have user-approved specs (Gate 4)
- Zero file overlaps
- Zero class overlaps
- Zero type conflicts
- Dependencies clearly documented
- Integration points verified

**Key Finding:** This epic demonstrates excellent feature decomposition. Feature 01 and Feature 02 have perfect separation of concerns with clean provider/consumer pattern.
