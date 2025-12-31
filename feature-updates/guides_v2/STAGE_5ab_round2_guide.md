# STAGE 5ab: TODO Creation - Round 2 (Iterations 8-16)

🚨 **MANDATORY READING PROTOCOL**

**Before starting this round:**
1. Use Read tool to load THIS ENTIRE GUIDE
2. Acknowledge critical requirements (see "Critical Rules" section below)
3. Verify prerequisites (see "Prerequisites Checklist" section below)
4. Update feature README.md Agent Status with guide name + timestamp

**DO NOT proceed without reading this guide.**

**After session compaction:**
- Check feature README.md Agent Status for current iteration
- READ THIS GUIDE again (full guide, not summary)
- Continue from "Next Action" in Agent Status

---

## Quick Start

**Overview:**
- **Round 2 of 3** in the 24-iteration TODO creation process
- **Iterations 8-16** (Deep Verification)
- **Focus:** Test strategy, edge cases, re-verification of critical matrices

**Estimated Time:** 45-60 minutes
**Prerequisites:** Round 1 complete (STAGE_5aa), confidence >= MEDIUM
**Outputs:** Comprehensive test strategy, edge case handling, updated matrices

---

## Critical Rules

```
┌─────────────────────────────────────────────────────────────┐
│ CRITICAL RULES - These MUST be copied to README Agent Status │
└─────────────────────────────────────────────────────────────┘

1. ⚠️ ALL 9 iterations in Round 2 are MANDATORY (no skipping)
   - Iterations 8-16
   - Each iteration deepens verification

2. ⚠️ Execute iterations IN ORDER (not parallel, not random)
   - Later iterations depend on earlier findings

3. ⚠️ Re-verification iterations (11, 12, 14) are CRITICAL
   - Algorithm Traceability Matrix re-verify (Iteration 11)
   - E2E Data Flow re-verify (Iteration 12)
   - Integration Gap Check re-verify (Iteration 14)
   - These catch bugs introduced during Round 1 updates

4. ⚠️ Test Coverage Depth Check (Iteration 15)
   - Verify tests cover edge cases, not just happy path
   - Target: >90% coverage

5. ⚠️ STOP if confidence < Medium at Round 2 checkpoint
   - Update questions file
   - Wait for user answers
   - Do NOT proceed to Round 3

6. ⚠️ Update feature README.md Agent Status after Round 2 complete
   - Document confidence level
   - Document next action
```

---

## Prerequisites Checklist

**Verify BEFORE starting Round 2:**

□ Round 1 (STAGE_5aa) complete
□ All 8 Round 1 iterations executed (1-7 + 4a)
□ Iteration 4a PASSED (TODO Specification Audit)
□ TODO file created with:
  - All requirements covered
  - All tasks have acceptance criteria
  - Dependencies verified
  - Algorithm Traceability Matrix created
  - Integration Gap Check complete
□ Confidence level: >= MEDIUM (from Round 1 checkpoint)
□ No blockers in feature README.md Agent Status

**If any prerequisite fails:**
- ❌ STOP - Do NOT proceed with Round 2
- Return to Round 1 to complete prerequisites
- Document blocker in Agent Status

---

## Workflow Overview

```
┌──────────────────────────────────────────────────────────────┐
│              ROUND 2: Deep Verification                      │
│                    (9 Iterations)                             │
└──────────────────────────────────────────────────────────────┘

Iteration 8: Test Strategy Development
   ↓
Iteration 9: Edge Case Enumeration
   ↓
Iteration 10: Configuration Change Impact
   ↓
Iteration 11: Algorithm Traceability Matrix (Re-verify)
   ↓
Iteration 12: End-to-End Data Flow (Re-verify)
   ↓
Iteration 13: Dependency Version Check
   ↓
Iteration 14: Integration Gap Check (Re-verify)
   ↓
Iteration 15: Test Coverage Depth Check
   ↓
Iteration 16: Documentation Requirements
   ↓
ROUND 2 CHECKPOINT
   ↓
If confidence >= MEDIUM: Proceed to Round 3 (STAGE_5ac)
If confidence < MEDIUM: Update questions file, wait for user
```

---

## ROUND 2: Deep Verification

### Iteration 8: Test Strategy Development

**Purpose:** Define comprehensive test strategy for this feature

**Process:**

1. **Categorize tests needed:**
   - Unit tests (test individual methods)
   - Integration tests (test feature as whole)
   - Edge case tests (test error scenarios)
   - Regression tests (ensure no breakage)

2. **Create test plan:**

```markdown
## Test Strategy

### Unit Tests (per-method testing)

**Test File:** tests/league_helper/util/test_PlayerManager_adp.py

1. test_load_adp_data_success()
   - Given: Valid ADP CSV exists
   - When: load_adp_data() called
   - Then: Returns list of tuples with correct data

2. test_load_adp_data_file_not_found()
   - Given: ADP CSV does not exist
   - When: load_adp_data() called
   - Then: Returns empty list, logs error

3. test_match_player_to_adp_found()
   - Given: Player exists in ADP data
   - When: _match_player_to_adp(player) called
   - Then: player.adp_value set correctly

4. test_match_player_to_adp_not_found()
   - Given: Player NOT in ADP data
   - When: _match_player_to_adp(player) called
   - Then: player.adp_value = None

5. test_calculate_adp_multiplier_valid()
   - Given: player.adp_value = 5
   - When: _calculate_adp_multiplier(player) called
   - Then: Returns multiplier from ConfigManager

6. test_calculate_adp_multiplier_none()
   - Given: player.adp_value = None
   - When: _calculate_adp_multiplier(player) called
   - Then: Returns 1.0 (neutral)

7. test_calculate_adp_multiplier_invalid()
   - Given: player.adp_value = -1
   - When: _calculate_adp_multiplier(player) called
   - Then: Returns 1.0, logs warning

---

### Integration Tests (feature-level testing)

**Test File:** tests/integration/test_adp_integration.py

1. test_adp_integration_end_to_end()
   - Given: Valid ADP CSV, player data
   - When: Load players, calculate scores
   - Then: All players have adp_multiplier, scores reflect ADP

2. test_adp_integration_with_other_features()
   - Given: ADP + Injury + Schedule features active
   - When: Calculate scores
   - Then: All multipliers applied, correct final score

---

### Edge Case Tests

1. test_empty_adp_file()
2. test_malformed_adp_csv()
3. test_duplicate_players_in_adp()
4. test_player_name_with_special_characters()

---

### Regression Tests

1. test_existing_scoring_still_works()
   - Ensure existing multipliers still applied
2. test_backward_compatibility()
   - Ensure old code still runs
```

3. **Add test tasks to TODO:**

```markdown
## Task 15: Unit Tests - ADP Data Loading

**Tests to Create:**
- test_load_adp_data_success()
- test_load_adp_data_file_not_found()
- test_load_adp_data_malformed_csv()

**Acceptance Criteria:**
- [ ] All 3 tests written
- [ ] All 3 tests pass
- [ ] Tests cover success and error paths
- [ ] Tests use fixtures for test data
```

**Output:** Comprehensive test strategy, test tasks added to TODO

**Update Agent Status:**
```
Progress: Iteration 8/16 (Round 2) complete
Next Action: Iteration 9 - Edge Case Enumeration
```

---

### Iteration 9: Edge Case Enumeration

**Purpose:** List ALL edge cases and verify they're handled in TODO

**Process:**

1. **Enumerate edge cases systematically:**

**Data Quality Edge Cases:**
- Empty file
- Malformed CSV (wrong columns, wrong format)
- Duplicate entries
- Missing values (null, empty string)
- Invalid data types

**Boundary Cases:**
- ADP = 0, 1, 500, 501 (boundary values)
- Player name = empty string, very long string
- File size = 0 bytes, very large file

**State Edge Cases:**
- File missing
- File unreadable (permissions)
- Config missing ADP multiplier ranges

**Concurrency Edge Cases:**
- Multiple threads accessing data

2. **For EACH edge case:**
   - Check if spec.md mentions it
   - Check if TODO has task for it
   - Check if test strategy covers it

3. **Add missing edge case handling to TODO**

**Example:**

```markdown
## Task 18: Edge Case - Duplicate Players in ADP Data

**Edge Case:** ADP CSV contains duplicate player entries

**Handling:**
- load_adp_data() should:
  - Detect duplicates during loading
  - Log warning: "Duplicate player in ADP data: {name}, keeping first occurrence"
  - Keep first occurrence, skip subsequent

**Acceptance Criteria:**
- [ ] Duplicate detection implemented
- [ ] Warning logged for duplicates
- [ ] First occurrence retained
- [ ] No crash on duplicates

**Test:** test_load_adp_data_duplicates()
```

**Output:** Complete edge case catalog, all cases handled

**Update Agent Status:**
```
Progress: Iteration 9/16 (Round 2) complete
Next Action: Iteration 10 - Configuration Change Impact
```

---

### Iteration 10: Configuration Change Impact

**Purpose:** Assess impact on league_config.json and ensure backward compatibility

**Process:**

1. **Identify config changes:**
   - New keys added?
   - Existing keys modified?
   - Example: Adding "adp_multiplier_ranges" section

2. **Verify backward compatibility:**
   - What happens if new keys missing?
   - Do we have defaults?

**Example:**

```markdown
## Configuration Impact Assessment

**New Config Keys:**
- `adp_multiplier_ranges`: Dict mapping ADP ranges to multipliers

**Backward Compatibility:**
- **If key missing:** Use default multiplier (1.0 for all players)
- **Migration needed:** No (graceful degradation)
- **User action required:** Optional (feature disabled if not configured)

**Default Values:**
```python
DEFAULT_ADP_MULTIPLIER_RANGES = {
    "1-10": 1.2,
    "11-50": 1.1,
    "51-150": 1.0,
    "151-300": 0.95,
    "301-500": 0.9
}
```

**Config Validation:**
- Task: Add config validation in ConfigManager
- Check: "adp_multiplier_ranges" is dict
- Check: All values are floats
- Fallback: Use defaults if invalid
```

3. **Add config migration tasks to TODO if needed**

```markdown
## Task 20: Config Validation - ADP Multiplier Ranges

**Requirement:** Validate ADP config or use defaults

**Implementation:**
- Add: ConfigManager._validate_adp_config()
- Check: "adp_multiplier_ranges" exists and is valid
- Fallback: Use DEFAULT_ADP_MULTIPLIER_RANGES if invalid/missing

**Acceptance Criteria:**
- [ ] Validation method created
- [ ] Invalid config detected and logged
- [ ] Defaults used as fallback
- [ ] No crash on missing config
```

**Output:** Config impact assessment, migration tasks if needed

**Update Agent Status:**
```
Progress: Iteration 10/16 (Round 2) complete
Next Action: Iteration 11 - Algorithm Traceability Matrix (Re-verify)
```

---

### Iteration 11: Algorithm Traceability Matrix (Re-verify)

**Purpose:** Re-verify ALL algorithms still traced after Round 1 updates

**⚠️ CRITICAL:** Round 1 may have added error handling algorithms not in original matrix

**Process:**

1. **Review Algorithm Traceability Matrix from Iteration 4 (Round 1)**

2. **Check for new algorithms added during Round 1:**
   - Error handling logic
   - Edge case handling
   - Data validation

3. **Update matrix with any new algorithms:**

**Example of new algorithm discovered:**

| Algorithm (from spec.md) | Spec Section | Implementation Location | TODO Task | Verified |
|--------------------------|--------------|------------------------|-----------|----------|
| Validate duplicate players | Edge Cases, implicit | PlayerManager.load_adp_data() | Task 18 | ✅ |
| Validate config ADP ranges | Edge Cases, implicit | ConfigManager._validate_adp_config() | Task 20 | ✅ |

4. **Verify matrix is STILL complete:**
   - Count algorithms in spec + new edge cases: {N}
   - Count rows in matrix: {N}
   - ✅ All algorithms traced

**Output:** Updated Algorithm Traceability Matrix (should be larger than Round 1 version)

**Update Agent Status:**
```
Progress: Iteration 11/16 (Round 2) complete
Next Action: Iteration 12 - End-to-End Data Flow (Re-verify)
```

---

### Iteration 12: End-to-End Data Flow (Re-verify)

**Purpose:** Re-verify data flow is still complete after Round 1 updates

**Process:**

1. **Review E2E Data Flow from Iteration 5 (Round 1)**

2. **Check for new data transformations added during Round 1:**
   - Config validation step
   - Duplicate handling
   - Error recovery paths

3. **Update flow diagram if needed:**

```markdown
## End-to-End Data Flow: ADP Integration (Updated)

**Entry Point:**
data/rankings/adp.csv (CSV file)
   ↓
**Step 0: Config Validation (NEW - Task 20)**
ConfigManager._validate_adp_config() validates ADP ranges
Returns: Valid config or defaults
   ↓
**Step 1: Load (Task 1)**
PlayerManager.load_adp_data() reads CSV
- Handles: File not found, malformed CSV, duplicates
Returns: List[Tuple[str, str, int]] (Name, Position, ADP)
   ↓
**Step 2: Match (Task 2)**
PlayerManager._match_player_to_adp(player) matches player to ADP data
- Handles: Player not found in ADP data
Sets: player.adp_value (int or None)
   ↓
**Step 3: Calculate (Task 3)**
PlayerManager._calculate_adp_multiplier(player) calculates multiplier
- Handles: Invalid ADP value, missing config
Sets: player.adp_multiplier (float)
   ↓
**Step 4: Apply (Task 4)**
FantasyPlayer.calculate_total_score() multiplies score
Returns: total_score (float) with ADP contribution
   ↓
**Output:**
Updated player score used in draft recommendations
```

4. **Verify no gaps in updated flow:**
   - Config validated before loading ✅
   - Error handling paths traced ✅
   - All data transformations documented ✅

**Output:** Updated data flow diagram

**Update Agent Status:**
```
Progress: Iteration 12/16 (Round 2) complete
Next Action: Iteration 13 - Dependency Version Check
```

---

### Iteration 13: Dependency Version Check

**Purpose:** Verify all external dependencies are available and compatible

**Process:**

1. **List Python package dependencies:**
   - pandas (for CSV reading)
   - numpy (if used)
   - Standard library (csv, json, pathlib)

2. **Check versions in requirements.txt:**

```markdown
## Dependency Version Check

### pandas
- **Required:** >= 1.3.0
- **Current (requirements.txt):** 1.5.3
- **Compatibility:** ✅ Compatible

### csv (standard library)
- **Required:** Python 3.8+
- **Current:** Python 3.11
- **Compatibility:** ✅ Compatible

### pathlib (standard library)
- **Required:** Python 3.4+
- **Current:** Python 3.11
- **Compatibility:** ✅ Compatible
```

3. **Verify compatibility:**
   - All dependencies available ✅
   - Version conflicts: None ✅
   - New dependencies needed: None ✅

**Output:** Dependency compatibility report

**Update Agent Status:**
```
Progress: Iteration 13/16 (Round 2) complete
Next Action: Iteration 14 - Integration Gap Check (Re-verify)
```

---

### Iteration 14: Integration Gap Check (Re-verify)

**Purpose:** Re-verify no orphan methods after Round 2 additions

**Process:**

1. **Review Integration Matrix from Iteration 7 (Round 1)**

2. **Check for new methods added in Round 2:**
   - Config validation methods
   - Error handling helpers
   - Edge case handlers

**Example of new method discovered:**

```markdown
### Method: ConfigManager._validate_adp_config()

**Caller:** ConfigManager.__init__() (existing method)
**Integration Point:** Line ~85 in __init__()
**Call Signature:** `self._validate_adp_config()`
**Verified:** ✅ Method will be called on initialization

**Call Chain:**
run_league_helper.py
   → LeagueHelperManager.__init__()
   → ConfigManager.__init__()
   → ConfigManager._validate_adp_config() ← NEW METHOD

**Orphan Check:** ✅ NOT ORPHANED
```

3. **Verify all methods have callers:**

Count:
- New methods (Round 1 + Round 2): {N}
- Methods with callers: {M}
- ✅ PASS if M == N

4. **Update integration matrix:**

| New Method | Caller | Call Location | Verified |
|------------|--------|---------------|----------|
| load_adp_data() | PlayerManager.load_players() | PlayerManager.py:180 | ✅ |
| _match_player_to_adp() | PlayerManager.load_players() | PlayerManager.py:210 | ✅ |
| _calculate_adp_multiplier() | PlayerManager.load_players() | PlayerManager.py:215 | ✅ |
| _validate_adp_config() | ConfigManager.__init__() | ConfigManager.py:85 | ✅ |

**Output:** Updated integration matrix

**Update Agent Status:**
```
Progress: Iteration 14/16 (Round 2) complete
Next Action: Iteration 15 - Test Coverage Depth Check
```

---

### Iteration 15: Test Coverage Depth Check

**Purpose:** Verify tests cover edge cases, failure modes, not just happy path

**Process:**

1. **Review test strategy from Iteration 8**

2. **For EACH method/function, verify test coverage:**

```markdown
## Test Coverage Analysis

### Method: PlayerManager.load_adp_data()

**Coverage:**
- ✅ Success path: test_load_adp_data_success()
- ✅ Failure path: test_load_adp_data_file_not_found()
- ✅ Edge case: test_load_adp_data_malformed_csv()
- ✅ Edge case: test_load_adp_data_duplicates()
- ✅ Boundary: test_load_adp_data_empty_file()

**Coverage Score:** 5/5 paths = 100% ✅

---

### Method: PlayerManager._match_player_to_adp()

**Coverage:**
- ✅ Success path: test_match_player_to_adp_found()
- ✅ Failure path: test_match_player_to_adp_not_found()
- ✅ Edge case: test_match_player_special_characters()
- ⚠️ Missing: test_match_player_case_sensitivity()

**Coverage Score:** 3/4 paths = 75% ⚠️

**Action:** Add test_match_player_case_sensitivity() to TODO
```

3. **Calculate overall coverage:**

```markdown
## Overall Test Coverage

**Methods to test:** 8
**Methods with tests:** 8
**Method coverage:** 100% ✅

**Test paths analyzed:** 40
**Test paths covered:** 38
**Path coverage:** 95% ✅

**Coverage by category:**
- Success paths: 100% ✅
- Failure paths: 100% ✅
- Edge cases: 90% ⚠️
- Boundary values: 95% ✅

**Missing coverage:**
- test_match_player_case_sensitivity() (Task 21 - NEW)
- test_calculate_adp_multiplier_extreme_values() (Task 22 - NEW)

**Overall: ✅ PASS (>90% coverage)**
```

4. **Add missing test tasks to TODO:**

```markdown
## Task 21: Unit Test - Case Sensitivity

**Test:** test_match_player_case_sensitivity()

**Purpose:** Verify player matching handles case differences

**Test Cases:**
- "Patrick Mahomes" vs "patrick mahomes" → Should match
- "PATRICK MAHOMES" vs "Patrick Mahomes" → Should match

**Acceptance Criteria:**
- [ ] Test written
- [ ] Test passes
- [ ] Case-insensitive matching verified
```

**Output:** Test coverage report (>90% required)

**Update Agent Status:**
```
Progress: Iteration 15/16 (Round 2) complete
Next Action: Iteration 16 - Documentation Requirements
```

---

### Iteration 16: Documentation Requirements

**Purpose:** Ensure adequate documentation for this feature

**Process:**

1. **List documentation needed:**
   - Docstrings for new methods
   - README updates (if user-facing)
   - ARCHITECTURE.md updates (if architectural change)
   - Comments for complex logic

2. **Identify methods needing docstrings:**

```markdown
## Documentation Plan

### Methods Needing Docstrings

1. **PlayerManager.load_adp_data()**
   - Brief: Load ADP rankings from CSV file
   - Args: None (uses self.data_folder)
   - Returns: List[Tuple[str, str, int]]
   - Raises: None (graceful error handling)
   - Example: Internal usage only

2. **PlayerManager._match_player_to_adp()**
   - Brief: Match player to ADP ranking
   - Args: player (FantasyPlayer)
   - Returns: None (sets player.adp_value)
   - Raises: None
   - Example: Internal usage only

3. **PlayerManager._calculate_adp_multiplier()**
   - Brief: Calculate ADP score multiplier
   - Args: player (FantasyPlayer)
   - Returns: float (multiplier)
   - Raises: None
   - Example: Internal usage only

4. **ConfigManager._validate_adp_config()**
   - Brief: Validate ADP configuration or use defaults
   - Args: None
   - Returns: None (updates self.config)
   - Raises: None
   - Example: Internal usage only
```

3. **Identify documentation files needing updates:**

```markdown
### Documentation Files to Update

**README.md:**
- ❌ No updates needed (internal feature, not user-facing)

**ARCHITECTURE.md:**
- ✅ Update needed: Add ADP integration to scoring algorithm section
- Section: "Scoring Algorithm" → "Step 2: ADP Multiplier"

**docs/scoring/02_adp_multiplier.md:**
- ✅ NEW FILE needed: Document ADP multiplier algorithm
- Include: Formula, configuration, examples

**CLAUDE.md:**
- ❌ No updates needed (no workflow changes)
```

4. **Add documentation tasks to TODO:**

```markdown
## Task 25: Documentation - Method Docstrings

**Requirement:** Add Google-style docstrings to all new methods

**Methods to Document:**
- load_adp_data()
- _match_player_to_adp()
- _calculate_adp_multiplier()
- _validate_adp_config()

**Acceptance Criteria:**
- [ ] All 4 methods have docstrings
- [ ] Docstrings include: Brief description, Args, Returns, Raises, Example
- [ ] Docstrings follow Google style guide

---

## Task 26: Documentation - ARCHITECTURE.md Update

**Requirement:** Document ADP integration in architecture guide

**Updates:**
- Section: "Scoring Algorithm"
- Add: "Step 2: ADP Multiplier" subsection
- Content: How ADP data is loaded and applied

**Acceptance Criteria:**
- [ ] New subsection added
- [ ] Flow diagram updated
- [ ] Example provided

---

## Task 27: Documentation - Create docs/scoring/02_adp_multiplier.md

**Requirement:** Create comprehensive ADP multiplier documentation

**Sections:**
- Overview
- Algorithm
- Configuration
- Examples
- Edge cases

**Acceptance Criteria:**
- [ ] File created
- [ ] All sections complete
- [ ] Examples provided
- [ ] Consistent with other scoring docs
```

**Output:** Documentation plan, documentation tasks added

**Update Agent Status:**
```
Progress: Round 2 complete (9/9 iterations)
Next Action: Round 2 checkpoint - evaluate confidence
```

---

## ROUND 2 CHECKPOINT

**After completing Iteration 16:**

1. **Update Agent Status:**

```markdown
## Agent Status

**Last Updated:** {YYYY-MM-DD HH:MM}
**Current Phase:** TODO_CREATION
**Current Step:** Round 2 complete (9/9 iterations), evaluating confidence
**Current Guide:** STAGE_5ab_round2_guide.md
**Guide Last Read:** {YYYY-MM-DD HH:MM}
**Critical Rules from Guide:**
- 9 iterations mandatory (Round 2)
- STOP if confidence < Medium
- Re-verification iterations complete

**Progress:** Round 2 complete (16/24 total iterations)
**Confidence Level:** {HIGH / MEDIUM / LOW}
**Next Action:** {Update questions file / Proceed to Round 3}
**Blockers:** {List any uncertainties or "None"}
```

2. **Evaluate Confidence:**

**Ask yourself:**
- Are all test strategies comprehensive? (HIGH/MEDIUM/LOW)
- Are all edge cases covered? (HIGH/MEDIUM/LOW)
- Is test coverage >90%? (YES/NO)
- Overall confidence: {HIGH/MEDIUM/LOW}

3. **If confidence < MEDIUM:**

**STOP - Update questions file:**

Update existing `feature_{N}_{name}_questions.md` or create if doesn't exist:

```markdown
# Feature {N}: {Name} - Questions for User (Updated)

**Updated After:** Round 2 (Iteration 16)
**Confidence Level:** LOW / MEDIUM
**Reason:** {Why confidence is low}

---

{Add new questions discovered during Round 2}
```

**Update Agent Status:**
```
Blockers: Waiting for user answers to questions file
Next Action: Wait for user responses, then update TODO based on answers
```

**WAIT for user answers. Do NOT proceed to Round 3.**

4. **If confidence >= MEDIUM:**

**Proceed to Round 3:**

```markdown
✅ Round 2 complete (9/9 iterations)

**Confidence Level:** HIGH / MEDIUM
**Test Coverage:** {X}% (>90% required)
**Questions:** None (or documented in questions file)

**Proceeding to Round 3 (Iterations 17-24 + 23a).**

**Next Guide:** STAGE_5ac_round3_guide.md
```

---

## Completion Criteria

**Round 2 is complete when ALL of these are true:**

□ All 9 iterations executed (8-16) in order
□ Test strategy comprehensive (unit, integration, edge, regression)
□ Edge cases enumerated and handled
□ Algorithm Traceability Matrix updated (re-verified)
□ E2E Data Flow updated (re-verified)
□ Integration Gap Check updated (re-verified)
□ Test coverage >90%
□ Documentation plan created
□ Feature README.md updated:
  - Agent Status: "Round 2 complete"
  - Confidence level documented
  - Test coverage documented

**If any item unchecked:**
- ❌ Round 2 is NOT complete
- Complete missing items before proceeding

---

## Common Mistakes to Avoid

```
┌────────────────────────────────────────────────────────────┐
│ "If You're Thinking This, STOP" - Anti-Pattern Detection  │
└────────────────────────────────────────────────────────────┘

❌ "I'll skip re-verification iterations (11, 12, 14)"
   ✅ STOP - Re-verification catches bugs from Round 1 updates

❌ "Test coverage is 85%, close enough"
   ✅ STOP - Iteration 15 requires >90% coverage

❌ "I enumerated most edge cases, that's sufficient"
   ✅ STOP - Iteration 9 requires ALL edge cases

❌ "Algorithm matrix looks the same as Round 1"
   ✅ STOP - Round 1 likely added algorithms (error handling, etc.)

❌ "My confidence is medium-low, but I'll proceed to Round 3"
   ✅ STOP - Create/update questions file, wait for answers

❌ "Documentation can wait until after implementation"
   ✅ STOP - Iteration 16 plans documentation NOW

❌ "Config validation seems optional"
   ✅ STOP - Iteration 10 requires backward compatibility check

❌ "Let me skip to Round 3 now"
   ✅ STOP - Evaluate confidence at checkpoint first
```

---

## Prerequisites for Round 3 (STAGE_5ac)

**Before transitioning to Round 3, verify:**

□ Round 2 completion criteria ALL met
□ All 9 iterations executed (8-16)
□ Test coverage: >90%
□ Confidence level: >= MEDIUM
□ Feature README.md shows:
  - Round 2 complete (16/24 total)
  - Test coverage documented
  - Confidence: HIGH or MEDIUM
  - Next Action: Read STAGE_5ac guide

**If any prerequisite fails:**
- ❌ Do NOT transition to Round 3
- Complete Round 2 missing items

---

## Next Round

**After completing Round 2:**

📖 **READ:** `STAGE_5ac_round3_guide.md`
🎯 **GOAL:** Final verification & readiness - implementation phasing, mock audit, final gates
⏱️ **ESTIMATE:** 60-75 minutes

**Round 3 will:**
- Plan implementation phasing (Iteration 17)
- Define rollback strategy (Iteration 18)
- Final algorithm/data flow/integration verification (Iterations 19, 23)
- Performance considerations (Iteration 20)
- Mock audit & integration test plan (Iteration 21)
- Pre-Implementation Spec Audit - ALL 4 PARTS (Iteration 23a - MANDATORY)
- Implementation Readiness Protocol (Iteration 24 - FINAL GATE)

**Remember:** Use the phase transition prompt from `prompts_reference_v2.md` when starting Round 3.

---

*End of STAGE_5ab_round2_guide.md*
