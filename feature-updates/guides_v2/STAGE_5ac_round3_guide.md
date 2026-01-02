# STAGE 5ac: TODO Creation - Round 3 (Iterations 17-24 + 23a)

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
- **Round 3 of 3** in the 24-iteration TODO creation process
- **Iterations 17-24 + 23a** (Final Verification & Readiness)
- **Focus:** Implementation readiness, final gates, go/no-go decision

**Estimated Time:** 60-75 minutes
**Prerequisites:** Round 2 complete (STAGE_5ab), confidence >= MEDIUM, test coverage >90%
**Outputs:** Phased implementation plan, final verified matrices, implementation readiness decision

---

## Critical Rules

```
┌─────────────────────────────────────────────────────────────┐
│ CRITICAL RULES - These MUST be copied to README Agent Status │
└─────────────────────────────────────────────────────────────┘

1. ⚠️ ALL 9 iterations in Round 3 are MANDATORY (no skipping)
   - Iterations 17-24 + Iteration 23a
   - These are the FINAL gates before implementation

2. ⚠️ Iteration 23a (Pre-Implementation Spec Audit) has 4 MANDATORY PARTS
   - ALL 4 PARTS must PASS
   - CANNOT proceed to Stage 5b without "ALL 4 PARTS PASSED"

3. ⚠️ Iteration 24 (Implementation Readiness Protocol) is FINAL GATE
   - Go/no-go decision required
   - CANNOT proceed to Stage 5b without "GO" decision

4. ⚠️ Final verification iterations (19, 23) are CRITICAL
   - Algorithm Traceability Matrix (Final) - Iteration 19
   - Integration Gap Check (Final) - Iteration 23
   - Last chance to catch missing mappings

5. ⚠️ Mock Audit (Iteration 21) prevents interface mismatch bugs
   - Verify EACH mock matches real interface
   - Plan at least one integration test with REAL objects

6. ⚠️ Implementation Phasing (Iteration 17) is MANDATORY
   - Break implementation into phases with checkpoints
   - Prevents "big bang" integration failures

7. ⚠️ If ANY mandatory gate FAILS:
   - STOP immediately
   - Fix the failing gate
   - Re-run the failed iteration
   - Do NOT skip ahead

8. ⚠️ Update feature README.md Agent Status after Round 3 complete
   - Document Iteration 23a result (ALL 4 PARTS status)
   - Document Iteration 24 decision (GO/NO-GO)
```

---

## Prerequisites Checklist

**Verify BEFORE starting Round 3:**

□ Round 2 (STAGE_5ab) complete
□ All 9 Round 2 iterations executed (8-16)
□ Test strategy comprehensive and complete
□ Edge cases enumerated and handled
□ Algorithm Traceability Matrix updated (Round 2)
□ E2E Data Flow updated (Round 2)
□ Integration Gap Check updated (Round 2)
□ Test coverage: >90%
□ Documentation plan created
□ Confidence level: >= MEDIUM (from Round 2 checkpoint)
□ No blockers in feature README.md Agent Status

**If any prerequisite fails:**
- ❌ STOP - Do NOT proceed with Round 3
- Return to Round 2 to complete prerequisites
- Document blocker in Agent Status

---

## Workflow Overview

```
┌──────────────────────────────────────────────────────────────┐
│         ROUND 3: Final Verification & Readiness              │
│                    (9 Iterations)                             │
└──────────────────────────────────────────────────────────────┘

Iteration 17: Implementation Phasing
   ↓
Iteration 18: Rollback Strategy
   ↓
Iteration 19: Algorithm Traceability Matrix (FINAL)
   ↓
Iteration 20: Performance Considerations
   ↓
Iteration 21: Mock Audit & Integration Test Plan (CRITICAL)
   ↓
Iteration 22: Output Consumer Validation
   ↓
Iteration 23: Integration Gap Check (FINAL)
   ↓
Iteration 23a: Pre-Implementation Spec Audit (MANDATORY - 4 PARTS)
   ↓
Iteration 24: Implementation Readiness Protocol (FINAL GATE)
   ↓
If GO: Proceed to Stage 5b (Implementation)
If NO-GO: Fix blockers, re-run iteration 24
```

---

## ROUND 3: Final Verification & Readiness

### Iteration 17: Implementation Phasing

**Purpose:** Break implementation into phases for incremental validation

**Process:**

1. **Group TODO tasks into phases:**

**Phase 1: Core Data Loading (Foundation)**
- Task 1: Load ADP data
- Task 2: Add FantasyPlayer fields
- Tests: Basic loading tests

**Phase 2: Matching Logic**
- Task 3: Match players to ADP
- Tests: Matching tests

**Phase 3: Multiplier Calculation**
- Task 4: Calculate multiplier
- Tests: Calculation tests

**Phase 4: Score Integration**
- Task 5: Apply to scoring
- Tests: Integration tests

2. **Define phase boundaries:**
   - After each phase: Run unit tests (must pass 100%)
   - After each phase: Mini-QC checkpoint

3. **Document phasing in TODO:**

```markdown
---

## Implementation Phasing

**Phase 1: Core Data Loading**
- Tasks: 1, 2
- Tests: test_load_adp_data_*
- Checkpoint: All loading tests pass

**Phase 2: Matching Logic**
- Tasks: 3
- Tests: test_match_player_*
- Checkpoint: Matching tests pass

**Phase 3: Multiplier Calculation**
- Tasks: 4
- Tests: test_calculate_adp_*
- Checkpoint: Calculation tests pass

**Phase 4: Score Integration**
- Tasks: 5
- Tests: test_scoring_*
- Checkpoint: All integration tests pass

**Rule:** Must complete Phase N before starting Phase N+1
**Rule:** All tests must pass before proceeding to next phase

---
```

**Output:** Phased implementation plan

**Update Agent Status:**
```
Progress: Iteration 17/24 (Round 3) complete
Next Action: Iteration 18 - Rollback Strategy
```

---

### Iteration 18: Rollback Strategy

**Purpose:** Define how to rollback if implementation has critical issues

**Process:**

1. **Identify rollback points:**
   - Feature flag?
   - Git revert?
   - Config toggle?

2. **Document rollback procedure:**

```markdown
## Rollback Strategy

**If critical bug discovered in production:**

1. **Immediate rollback (Config toggle):**
   - Set config: `"enable_adp_integration": false`
   - Restart league helper
   - Result: Feature disabled, old scoring restored
   - Downtime: ~1 minute

2. **Code rollback (Git revert):**
   - `git revert <commit_hash>`
   - Remove ADP data file
   - Result: Code reverted to pre-feature state
   - Downtime: ~5 minutes

3. **Verification after rollback:**
   - Run smoke tests
   - Verify old scoring works
   - Check logs for errors
   - Compare draft recommendations to baseline

**Rollback decision criteria:**
- Critical bug: Immediate config toggle
- Data corruption: Code rollback
- Performance issue: Config toggle, investigate

**Testing rollback procedure:**
- Task: Add test_rollback_scenario()
- Verify: Feature can be cleanly disabled
- Verify: No residual state after rollback
```

**Output:** Rollback strategy documented

**Update Agent Status:**
```
Progress: Iteration 18/24 (Round 3) complete
Next Action: Iteration 19 - Algorithm Traceability Matrix (Final)
```

---

### Iteration 19: Algorithm Traceability Matrix (Final)

**Purpose:** Final verification of algorithm tracing

**⚠️ CRITICAL:** This is the LAST chance to catch missing algorithm mappings

**Process:**

1. **Review Algorithm Traceability Matrix from Iterations 4 (Round 1) and 11 (Round 2)**

2. **Final check:**
   - All algorithms from spec traced? ✅
   - All TODO tasks reference spec algorithms? ✅
   - No implementation without spec algorithm? ✅
   - All error handling algorithms included? ✅
   - All edge case algorithms included? ✅

3. **Count final mappings:**

```markdown
## Algorithm Traceability Matrix (FINAL)

**Total Algorithms Traced:** 47

**Breakdown:**
- Main algorithms (from spec): 12
- Helper algorithms: 8
- Error handling algorithms: 15
- Edge case algorithms: 12

**Verification:**
- Algorithms in spec: 12
- Algorithms in TODO: 47 (includes error handling + edge cases)
- Coverage: 100% of spec + comprehensive error handling ✅

**Final Matrix:**

| Algorithm (from spec.md) | Spec Section | Implementation Location | TODO Task | Verified |
|--------------------------|--------------|------------------------|-----------|----------|
| Load ADP data from CSV | Algorithms, step 1 | PlayerManager.load_adp_data() | Task 1 | ✅ |
| Match player to ADP ranking | Algorithms, step 2 | PlayerManager._match_player_to_adp() | Task 2 | ✅ |
| Calculate ADP multiplier | Algorithms, step 3 | PlayerManager._calculate_adp_multiplier() | Task 3 | ✅ |
| Apply multiplier to score | Algorithms, step 4 | FantasyPlayer.calculate_total_score() | Task 4 | ✅ |
| Handle player not in ADP data | Edge Cases, case 1 | PlayerManager._match_player_to_adp() | Task 2 | ✅ |
| Handle invalid ADP value | Edge Cases, case 2 | PlayerManager._calculate_adp_multiplier() | Task 3 | ✅ |
| Handle ADP file missing | Edge Cases, case 3 | PlayerManager.load_adp_data() | Task 1 | ✅ |
| Validate duplicate players | Edge Cases, implicit | PlayerManager.load_adp_data() | Task 18 | ✅ |
| Validate config ADP ranges | Edge Cases, implicit | ConfigManager._validate_adp_config() | Task 20 | ✅ |
| ... (38 more rows) ...

**✅ FINAL VERIFICATION: ALL ALGORITHMS TRACED**
```

**Output:** Final Algorithm Traceability Matrix (40+ mappings typical)

**Update Agent Status:**
```
Progress: Iteration 19/24 (Round 3) complete
Next Action: Iteration 20 - Performance Considerations
```

---

### Iteration 20: Performance Considerations

**Purpose:** Assess performance impact and optimization needs

**Process:**

1. **Estimate performance impact:**
   - Loading ADP CSV: ~100ms (small file)
   - Matching players: ~10ms per player × 500 players = 5s
   - Calculation: negligible

2. **Identify bottlenecks:**

```markdown
## Performance Analysis

**Baseline Performance (before feature):**
- Player loading: 2.5s
- Score calculation: 0.8s
- Total startup time: 3.3s

**Estimated Performance (with feature):**
- ADP CSV loading: +0.1s
- Player matching: +5.0s (O(n²) list iteration)
- ADP multiplier calculation: +0.1s
- Total startup time: 8.5s

**Impact:** +5.2s (157% increase) ⚠️ SIGNIFICANT

**Bottleneck:** Player matching (O(n²) complexity)
```

3. **Identify optimization opportunities:**

```markdown
## Optimization Strategy

**Problem:** Matching 500 players to ADP data with list iteration is O(n²)

**Solution:** Use dict for O(1) lookup

**Before (slow):**
```python
for player in players:
    for (name, pos, adp) in adp_data:  # O(n²)
        if player.name == name and player.position == pos:
            player.adp_value = adp
            break
```

**After (fast):**
```python
# Create dict once: O(n)
adp_dict = {(name, pos): adp for (name, pos, adp) in adp_data}

# Lookup: O(1) per player, O(n) total
for player in players:
    key = (player.name, player.position)
    player.adp_value = adp_dict.get(key)
```

**Performance Improvement:**
- Matching time: 5.0s → 0.01s (500x faster)
- Total startup time: 8.5s → 3.5s (only +0.2s vs baseline)
```

4. **Add optimization tasks if needed:**

```markdown
## Task 30: Performance Optimization - ADP Lookup

**Issue:** Matching 500 players to ADP data with list iteration is O(n²)

**Optimization:** Use dict for O(1) lookup

**Implementation:**
- Create: self.adp_dict = {(name, position): adp_value}
- Lookup: adp_value = self.adp_dict.get((player.name, player.position))

**Acceptance Criteria:**
- [ ] ADP data stored in dict (not list)
- [ ] Lookup time: <1ms per player
- [ ] Total matching time: <100ms for 500 players
- [ ] Verified: No performance regression

**Test:** test_adp_lookup_performance()
```

**Output:** Performance assessment, optimization tasks if needed

**Update Agent Status:**
```
Progress: Iteration 20/24 (Round 3) complete
Next Action: Iteration 21 - Mock Audit & Integration Test Plan
```

---

### Iteration 21: Mock Audit & Integration Test Plan (CRITICAL)

**Purpose:** Verify mocks match real interfaces, plan integration tests

**⚠️ CRITICAL:** Unit tests with wrong mocks can pass while hiding bugs

**Process:**

1. **List ALL mocked dependencies in tests:**

```markdown
## Mock Audit

### Mock 1: ConfigManager.get_adp_multiplier

**Used in tests:**
- test_calculate_adp_multiplier_valid()

**Mock definition:**
```python
mock_config.get_adp_multiplier.return_value = (1.2, 95)
```

**Real interface (VERIFIED by reading source):**
```python
# league_helper/util/ConfigManager.py:234
def get_adp_multiplier(self, adp: int) -> Tuple[float, int]:
```

**Parameters:**
- Mock accepts: ANY arguments (over-mocking) ⚠️
- Real accepts: adp (int)
- ⚠️ MISMATCH: Mock too permissive

**Return value:**
- Mock returns: (1.2, 95) - Tuple[float, int] ✅
- Real returns: Tuple[float, int] ✅
- ✅ MATCH

**Fix:** Update mock to validate parameter type
```python
def mock_get_adp_multiplier(adp: int):
    assert isinstance(adp, int), "adp must be int"
    return (1.2, 95)
mock_config.get_adp_multiplier = mock_get_adp_multiplier
```

**Verification:** ✅ FIXED - Mock now matches real interface

---

### Mock 2: csv_utils.read_csv_with_validation

**Used in tests:**
- test_load_adp_data_success()

**Mock definition:**
```python
mock_read_csv.return_value = pd.DataFrame([...])
```

**Real interface (VERIFIED by reading source):**
```python
# utils/csv_utils.py:45
def read_csv_with_validation(
    filepath: Union[str, Path],
    required_columns: List[str],
    encoding: str = 'utf-8'
) -> pd.DataFrame:
```

**Parameters:**
- Mock accepts: ANY ✅ (uses MagicMock default)
- Real accepts: filepath, required_columns, encoding
- ✅ ACCEPTABLE: Test only uses (filepath, required_columns)

**Return value:**
- Mock returns: pd.DataFrame ✅
- Real returns: pd.DataFrame ✅
- ✅ MATCH

**Verification:** ✅ PASSED - Mock matches real interface

---

{Repeat for all mocks}
```

2. **Plan integration tests with REAL objects:**

```markdown
## Integration Test Plan (No Mocks)

**Test 1: test_adp_integration_with_real_config()**

**Purpose:** Verify ADP integration works with REAL ConfigManager

**Setup:**
- Use REAL ConfigManager (not mock)
- Use REAL league_config.json
- Use test ADP CSV file

**Steps:**
1. Load real config
2. Load ADP data
3. Match player "Patrick Mahomes, QB"
4. Calculate multiplier using REAL ConfigManager.get_adp_multiplier()
5. Verify result matches expected value from config

**Why no mocks:** Catch interface mismatches that mocks hide

**Expected Duration:** ~100ms (acceptable for integration test)

---

**Test 2: test_adp_integration_with_real_csv_utils()**

**Purpose:** Verify ADP loading works with REAL csv_utils

**Setup:**
- Use REAL csv_utils.read_csv_with_validation
- Create test CSV file in tmp_path

**Steps:**
1. Create test CSV: tmp_path / "adp_test.csv"
2. Write test data: "Name,Position,ADP\nPatrick Mahomes,QB,5\n"
3. Load using REAL csv_utils
4. Verify data loaded correctly

**Why no mocks:** Verify CSV parsing actually works

---

**Test 3: test_adp_end_to_end_real_objects()**

**Purpose:** Full E2E test with REAL objects (no mocks)

**Setup:**
- REAL ConfigManager
- REAL csv_utils
- REAL PlayerManager
- REAL FantasyPlayer

**Steps:**
1. Initialize PlayerManager with test data folder
2. Load ADP data (uses real csv_utils)
3. Load players (uses real PlayerManager)
4. Calculate scores (uses real ConfigManager)
5. Verify: All players have adp_multiplier
6. Verify: Scores reflect ADP contribution

**Why no mocks:** Prove entire feature works in real environment

**Expected Duration:** ~500ms (acceptable for E2E test)
```

3. **Add integration test tasks:**

```markdown
## Task 35: Integration Test - Real ConfigManager

**Requirement:** Test with REAL ConfigManager (not mock)

**Test:** test_adp_integration_with_real_config()

**Acceptance Criteria:**
- [ ] Uses REAL ConfigManager
- [ ] Uses REAL league_config.json
- [ ] No mocks used
- [ ] Test passes (proves real integration works)

---

## Task 36: Integration Test - Real CSV Utils

**Requirement:** Test with REAL csv_utils (not mock)

**Test:** test_adp_integration_with_real_csv_utils()

**Acceptance Criteria:**
- [ ] Uses REAL csv_utils.read_csv_with_validation
- [ ] Creates test CSV file
- [ ] No mocks used
- [ ] Test passes

---

## Task 37: Integration Test - End-to-End (No Mocks)

**Requirement:** Full E2E test with all real objects

**Test:** test_adp_end_to_end_real_objects()

**Acceptance Criteria:**
- [ ] Uses REAL ConfigManager, csv_utils, PlayerManager
- [ ] No mocks used
- [ ] All steps execute successfully
- [ ] Test proves feature works in real environment
```

**Output:** Mock audit report, integration test plan (at least 3 real-object tests)

**Update Agent Status:**
```
Progress: Iteration 21/24 (Round 3) complete
Next Action: Iteration 22 - Output Consumer Validation
```

---

### Iteration 22: Output Consumer Validation

**Purpose:** Verify outputs are consumable by downstream code

**Process:**

1. **Identify output consumers:**
   - Who uses the output from this feature?
   - Example: AddToRosterModeManager uses updated player scores

2. **Plan roundtrip tests:**

```markdown
## Output Consumer Validation

**Output:** Updated FantasyPlayer objects with adp_multiplier

**Consumer 1: AddToRosterModeManager.get_recommendations()**

**Roundtrip Test:**
1. Run feature: Load players with ADP integration
2. Verify: Players have adp_multiplier field
3. Consumer: Call AddToRosterModeManager.get_recommendations()
4. Verify: Recommendations generated successfully
5. Verify: Recommendations use ADP-adjusted scores
6. Verify: Top recommendations have high ADP rankings (logic check)

**Test:** test_adp_output_consumed_by_draft_mode()

---

**Consumer 2: StarterHelperModeManager.get_optimal_lineup()**

**Roundtrip Test:**
1. Run feature: Load players with ADP integration
2. Verify: Roster players have adp_multiplier
3. Consumer: Call StarterHelperModeManager.get_optimal_lineup()
4. Verify: Lineup selection successful
5. Verify: Lineup scores include ADP contribution

**Test:** test_adp_output_consumed_by_starter_mode()
```

3. **Add consumer validation tasks:**

```markdown
## Task 40: Consumer Validation - Draft Mode

**Requirement:** Verify AddToRosterModeManager consumes ADP-adjusted scores

**Test:** test_adp_output_consumed_by_draft_mode()

**Acceptance Criteria:**
- [ ] Load players with ADP integration
- [ ] Call AddToRosterModeManager.get_recommendations()
- [ ] Verify recommendations use ADP-adjusted scores
- [ ] No errors in consumer code

---

## Task 41: Consumer Validation - Starter Mode

**Requirement:** Verify StarterHelperModeManager consumes ADP-adjusted scores

**Test:** test_adp_output_consumed_by_starter_mode()

**Acceptance Criteria:**
- [ ] Load roster with ADP integration
- [ ] Call StarterHelperModeManager.get_optimal_lineup()
- [ ] Verify lineup selection works
- [ ] No errors in consumer code
```

**Output:** Output consumer validation plan

**Update Agent Status:**
```
Progress: Iteration 22/24 (Round 3) complete
Next Action: Iteration 23 - Integration Gap Check (Final)
```

---

### Iteration 23: Integration Gap Check (Final)

**Purpose:** Final verification - no orphan code

**⚠️ CRITICAL:** This is the LAST chance to catch orphan methods

**Process:**

1. **Final review of integration matrix from Iterations 7 (Round 1) and 14 (Round 2)**

2. **Verify ALL new methods have callers:**

Count:
- Total new methods (all rounds): {N}
- Methods with identified callers: {M}
- ✅ PASS if M == N
- ❌ FAIL if M < N

3. **Final integration matrix:**

```markdown
## Integration Gap Check (FINAL)

**Total New Methods:** 12

| New Method | Caller | Call Location | Round Added | Verified |
|------------|--------|---------------|-------------|----------|
| load_adp_data() | PlayerManager.load_players() | PlayerManager.py:180 | Round 1 | ✅ |
| _match_player_to_adp() | PlayerManager.load_players() | PlayerManager.py:210 | Round 1 | ✅ |
| _calculate_adp_multiplier() | PlayerManager.load_players() | PlayerManager.py:215 | Round 1 | ✅ |
| _validate_adp_config() | ConfigManager.__init__() | ConfigManager.py:85 | Round 2 | ✅ |
| _handle_duplicate_adp() | load_adp_data() | PlayerManager.py:465 | Round 2 | ✅ |
| _create_adp_dict() | load_adp_data() | PlayerManager.py:470 | Round 3 | ✅ |
| ... (6 more methods) ...

**✅ FINAL VERIFICATION: NO ORPHAN CODE - ALL METHODS INTEGRATED**
```

**Output:** Final integration verification (all methods have callers)

**Update Agent Status:**
```
Progress: Iteration 23/24 (Round 3) complete
Next Action: Iteration 23a - Pre-Implementation Spec Audit (MANDATORY - 4 PARTS)
```

---

### Iteration 23a: Pre-Implementation Spec Audit (MANDATORY - 4 PARTS)

**Purpose:** Final comprehensive audit before implementation

**⚠️ MANDATORY:** ALL 4 PARTS must PASS before proceeding to Stage 5b

**PART 1: Completeness Audit**

**Question:** Does every requirement have corresponding TODO tasks?

**Process:**
1. List all requirements from spec.md
2. For each requirement, find TODO task(s)
3. Count:
   - Requirements in spec: {N}
   - Requirements with TODO tasks: {M}
   - ✅ PASS if M == N

**Example:**

```markdown
## PART 1: Completeness Audit

**Requirements from spec.md:**
1. Load ADP data from CSV → Task 1 ✅
2. Match players to ADP rankings → Task 2 ✅
3. Calculate ADP multiplier → Task 3 ✅
4. Apply multiplier to scoring → Task 4 ✅
5. Handle file not found → Task 11 ✅
6. Handle player not in ADP data → Task 2 (edge case handling) ✅
7. Handle invalid ADP values → Task 3 (edge case handling) ✅
... (15 total requirements)

**Result:**
- Requirements in spec: 15
- Requirements with TODO tasks: 15
- Coverage: 100% ✅

**PART 1: ✅ PASS**
```

---

**PART 2: Specificity Audit**

**Question:** Does every TODO task have concrete acceptance criteria?

**Process:**
1. Review every TODO task
2. Verify each has:
   - Specific acceptance criteria (not vague)
   - Implementation location (file, method, line)
   - Test coverage (test names)
   - **Category-specific tests** (if code processes multiple types/positions)
3. **Verify position-specific/category-specific tests:**
   - If code processes multiple categories (e.g., positions, file types, data sources)
   - Ensure tests explicitly cover EACH category
   - Example: If updating 6 positions, verify tests for QB, RB, WR, TE, K, DST
4. Count:
   - Total tasks: {N}
   - Tasks with acceptance criteria: {M}
   - ✅ PASS if M == N

**Example:**

```markdown
## PART 2: Specificity Audit

**Reviewing all TODO tasks:**

Task 1: load_adp_data()
- ✅ Has acceptance criteria (6 items)
- ✅ Has implementation location (PlayerManager.py:450)
- ✅ Has test coverage (3 tests listed)

Task 2: _match_player_to_adp()
- ✅ Has acceptance criteria (5 items)
- ✅ Has implementation location (PlayerManager.py:480)
- ✅ Has test coverage (4 tests listed)

... (43 total tasks)

**Result:**
- Total tasks: 43
- Tasks with acceptance criteria: 43
- Tasks with implementation location: 43
- Tasks with test coverage: 43
- Specificity: 100% ✅

**PART 2: ✅ PASS**
```

---

**PART 3: Interface Contracts Audit**

**Question:** Are all external interfaces verified against source code?

**Process:**
1. List all external dependencies
2. For each dependency:
   - Verify interface READ from actual source code (not assumed)
   - Verify method signature copied correctly
   - Verify return types match
3. Count:
   - Total external dependencies: {N}
   - Dependencies verified from source: {M}
   - ✅ PASS if M == N

**Example:**

```markdown
## PART 3: Interface Contracts Audit

**External Dependencies:**

1. ConfigManager.get_adp_multiplier
   - ✅ Verified from source: ConfigManager.py:234
   - ✅ Signature copied: `def get_adp_multiplier(self, adp: int) -> Tuple[float, int]`
   - ✅ Return type matches: Tuple[float, int]
   - ✅ Used in: Task 3

2. csv_utils.read_csv_with_validation
   - ✅ Verified from source: csv_utils.py:45
   - ✅ Signature copied: `def read_csv_with_validation(...) -> pd.DataFrame`
   - ✅ Return type matches: pd.DataFrame
   - ✅ Used in: Task 1

3. FantasyPlayer class
   - ✅ Verified from source: FantasyPlayer.py:15
   - ✅ Can add fields: adp_value, adp_multiplier
   - ✅ No conflicts found
   - ✅ Used in: Tasks 2, 3, 4

... (8 total dependencies)

**Result:**
- Total external dependencies: 8
- Dependencies verified from source: 8
- Verification: 100% ✅

**PART 3: ✅ PASS**
```

---

**PART 4: Integration Evidence Audit**

**Question:** Does every new method have identified caller?

**Process:**
1. List all new methods/functions
2. For each method:
   - Verify caller identified
   - Verify call location documented
   - Verify execution path traced
3. Count:
   - New methods: {N}
   - Methods with callers: {M}
   - ✅ PASS if M == N

**Example:**

```markdown
## PART 4: Integration Evidence Audit

**New Methods:**

1. PlayerManager.load_adp_data()
   - ✅ Caller: PlayerManager.load_players()
   - ✅ Call location: PlayerManager.py:180
   - ✅ Execution path: run_league_helper.py → LeagueHelperManager → PlayerManager.load_players() → load_adp_data()

2. PlayerManager._match_player_to_adp()
   - ✅ Caller: PlayerManager.load_players()
   - ✅ Call location: PlayerManager.py:210 (in loop)
   - ✅ Execution path: load_players() → for player in players → _match_player_to_adp(player)

3. PlayerManager._calculate_adp_multiplier()
   - ✅ Caller: PlayerManager.load_players()
   - ✅ Call location: PlayerManager.py:215
   - ✅ Execution path: load_players() → _calculate_adp_multiplier(player)

... (12 total new methods)

**Result:**
- New methods: 12
- Methods with callers: 12
- Integration: 100% ✅

**PART 4: ✅ PASS**
```

---

**FINAL RESULTS:**

```markdown
---

## ✅ Iteration 23a: Pre-Implementation Spec Audit

**Audit Date:** {YYYY-MM-DD}

**PART 1 - Completeness:** ✅ PASS
- Requirements: 15
- With TODO tasks: 15
- Coverage: 100%

**PART 2 - Specificity:** ✅ PASS
- TODO tasks: 43
- With acceptance criteria: 43
- Specificity: 100%

**PART 3 - Interface Contracts:** ✅ PASS
- External dependencies: 8
- Verified from source: 8
- Verification: 100%

**PART 4 - Integration Evidence:** ✅ PASS
- New methods: 12
- With callers: 12
- Integration: 100%

**OVERALL RESULT: ✅ ALL 4 PARTS PASSED**

**Ready to proceed to Iteration 24 (Implementation Readiness Protocol).**

---
```

**If ANY part FAILS:**
- ❌ STOP - Do NOT proceed to Iteration 24
- Fix failing part
- Re-run iteration 23a
- Document in Agent Status: "Iteration 23a FAILED - fixing {part}"

**Update Agent Status:**
```
Progress: Iteration 23a PASSED (ALL 4 PARTS - critical gate)
Next Action: Iteration 24 - Implementation Readiness Protocol (FINAL GATE)
```

---

### Iteration 24: Implementation Readiness Protocol (FINAL GATE)

**Purpose:** Final go/no-go decision before implementation

**⚠️ FINAL GATE:** Cannot proceed to Stage 5b without "GO" decision

**Process:**

1. **Final checklist:**

```markdown
## Implementation Readiness Checklist

**Spec Verification:**
- [x] spec.md complete (no TBD sections)
- [x] All algorithms documented
- [x] All edge cases defined
- [x] All dependencies identified

**TODO Verification:**
- [x] TODO file created: feature_{N}_{name}_todo.md
- [x] All requirements have tasks
- [x] All tasks have acceptance criteria
- [x] Implementation locations specified
- [x] Test coverage defined
- [x] Implementation phasing defined

**Iteration Completion:**
- [x] All 24 iterations complete (Rounds 1, 2, 3)
- [x] Iteration 4a PASSED (TODO Specification Audit)
- [x] Iteration 23a PASSED (ALL 4 PARTS)
- [x] No iterations skipped

**Confidence Assessment:**
- [x] Confidence level: HIGH / MEDIUM
- [x] All questions resolved (or documented)
- [x] No critical unknowns

**Integration Verification:**
- [x] Algorithm Traceability Matrix complete (47 mappings)
- [x] Integration Gap Check complete (no orphan code - 12 methods verified)
- [x] Interface Verification complete (8 dependencies verified from source)
- [x] Mock Audit complete (mocks match real interfaces)

**Quality Gates:**
- [x] Test coverage: >90%
- [x] Performance impact: Acceptable (<+1s vs baseline)
- [x] Rollback strategy: Defined
- [x] Documentation plan: Complete
- [x] All mandatory audits PASSED
- [x] No blockers

**DECISION:** ✅ GO / ❌ NO-GO

**If GO:**
- Proceed to Stage 5b (Implementation Execution)
- Document approval in feature README.md

**If NO-GO:**
- List blockers
- Fix blockers
- Re-run iteration 24
```

2. **Make go/no-go decision:**

**✅ GO if:**
- All checklist items checked
- Confidence >= MEDIUM
- All mandatory audits PASSED (iterations 4a, 23a)
- Iteration 23a: ALL 4 PARTS PASSED

**❌ NO-GO if:**
- Any checklist item unchecked
- Confidence < MEDIUM
- Any mandatory audit FAILED
- Any critical blocker

3. **Document decision:**

**If GO:**

```markdown
---

## ✅ Iteration 24: Implementation Readiness - GO

**Date:** {YYYY-MM-DD}
**Confidence:** HIGH / MEDIUM
**Iterations Complete:** 24/24 (all rounds)
**Mandatory Audits:** ALL PASSED
  - Iteration 4a: PASSED
  - Iteration 23a: ALL 4 PARTS PASSED

**Quality Metrics:**
- Algorithm mappings: 47
- Integration verification: 12/12 methods
- Interface verification: 8/8 dependencies
- Test coverage: 95%
- Performance impact: +0.2s (acceptable)

**DECISION: ✅ READY FOR IMPLEMENTATION**

**Next Stage:** Stage 5b (Implementation Execution)

**Proceed to Stage 5b using STAGE_5b_implementation_execution_guide.md**

---
```

**If NO-GO:**

```markdown
---

## ❌ Iteration 24: Implementation Readiness - NO-GO

**Date:** {YYYY-MM-DD}
**Confidence:** LOW
**Blockers:**
1. {Blocker 1 description}
2. {Blocker 2 description}

**DECISION: ❌ NOT READY FOR IMPLEMENTATION**

**Next Actions:**
1. Fix blocker 1: {action}
2. Fix blocker 2: {action}
3. Re-run iteration 24 after fixes

**Do NOT proceed to Stage 5b until GO decision achieved.**

---
```

**Output:** Go/no-go decision, readiness documented

**Update Agent Status:**

```markdown
## Agent Status

**Last Updated:** {YYYY-MM-DD HH:MM}
**Current Phase:** TODO_CREATION
**Current Step:** Round 3 complete (24/24 total iterations)
**Current Guide:** STAGE_5ac_round3_guide.md
**Guide Last Read:** {YYYY-MM-DD HH:MM}

**Progress:** All 24 iterations complete
**Iteration 4a:** PASSED
**Iteration 23a:** ALL 4 PARTS PASSED
**Iteration 24 Decision:** ✅ GO / ❌ NO-GO

**Confidence Level:** {HIGH / MEDIUM / LOW}
**Next Action:** {Read Stage 5b guide / Fix blockers}
**Blockers:** {None / List blockers}
```

---

## Completion Criteria

**Round 3 (and Stage 5a) is complete when ALL of these are true:**

□ All 9 iterations executed (17-24 + 23a) in order
□ Iteration 23a PASSED (ALL 4 PARTS of Pre-Implementation Spec Audit)
□ Iteration 24 decision: ✅ GO
□ TODO file complete with:
  - Implementation phasing defined
  - Rollback strategy documented
  - Performance optimization included
  - Mock audit complete
  - Final Algorithm Traceability Matrix (40+ mappings)
  - Final Integration Gap Check (all methods have callers)
  - Consumer validation planned
□ Feature README.md updated:
  - Agent Status: Phase = IMPLEMENTATION
  - Next Action = Read Stage 5b guide
  - Iteration 23a result = ALL 4 PARTS PASSED
  - Iteration 24 result = GO

**If any item unchecked:**
- ❌ Round 3 is NOT complete
- ❌ Do NOT proceed to Stage 5b
- Complete missing items first

---

## Common Mistakes to Avoid

```
┌────────────────────────────────────────────────────────────┐
│ "If You're Thinking This, STOP" - Anti-Pattern Detection  │
└────────────────────────────────────────────────────────────┘

❌ "Iteration 23a Part 1 passed, I'll skip Parts 2-4"
   ✅ STOP - ALL 4 PARTS must PASS (not just some)

❌ "My confidence is medium-low but I'll mark it as GO"
   ✅ STOP - GO requires confidence >= MEDIUM

❌ "I'll skip implementation phasing, seems unnecessary"
   ✅ STOP - Iteration 17 is MANDATORY

❌ "Mock audit seems tedious, I'll skip it"
   ✅ STOP - Iteration 21 prevents interface mismatch bugs

❌ "Final verification iterations (19, 23) are redundant"
   ✅ STOP - These catch bugs from earlier rounds

❌ "I'll proceed to Stage 5b with NO-GO decision"
   ✅ STOP - Cannot proceed without GO decision

❌ "I'll mark GO even though checklist has unchecked items"
   ✅ STOP - ALL checklist items must be checked for GO

❌ "Let me start coding now, I'm ready"
   ✅ STOP - Must document GO decision and update Agent Status first
```

---

## Prerequisites for Stage 5b

**Before transitioning to Stage 5b, verify:**

□ Round 3 completion criteria ALL met
□ All 24 iterations complete (Rounds 1, 2, 3)
□ Iteration 4a: PASSED
□ Iteration 23a: ALL 4 PARTS PASSED
□ Iteration 24: ✅ GO decision
□ TODO file complete and ready
□ Feature README.md shows:
  - Iteration 23a: ALL 4 PARTS PASSED
  - Iteration 24: GO
  - Agent Status: Phase = IMPLEMENTATION
  - Next Action = Read Stage 5b guide

**If any prerequisite fails:**
- ❌ Do NOT transition to Stage 5b
- Complete Stage 5a missing items

---

## Next Stage

**After completing Round 3 with GO decision:**

📖 **READ:** `STAGE_5b_implementation_execution_guide.md`
🎯 **GOAL:** Implement all TODO tasks with continuous spec verification
⏱️ **ESTIMATE:** Varies by feature complexity

**Stage 5b will:**
- Implement TODO tasks phase by phase
- Run unit tests after EVERY phase (100% pass required)
- Keep spec.md VISIBLE during implementation
- Create implementation_checklist.md for continuous verification
- Execute implementation with Algorithm Traceability Matrix as guide

**Remember:** Use the phase transition prompt from `prompts_reference_v2.md` when starting Stage 5b.

---

*End of STAGE_5ac_round3_guide.md*
