# STAGE 5ac Part 1: TODO Creation - Round 3 Preparation (Iterations 17-22)

**Part of:** Epic-Driven Development Workflow v2
**Stage:** 5ac - TODO Creation Round 3
**Sub-Stage:** Part 1 - Pre-Implementation Preparation
**Prerequisites:** STAGE_5ab complete (Round 2), confidence >= MEDIUM, test coverage >90%
**Next Stage:** STAGE_5ac_part2_final_gates_guide.md

---

## 🚨 MANDATORY READING PROTOCOL

**CRITICAL:** You MUST read this ENTIRE guide before starting Part 1.

**Why this matters:**
- Part 1 prepares all implementation prerequisites
- Missing iterations causes implementation failures
- These iterations prevent "big bang" integration issues

**Reading Checkpoint:**
Before proceeding, you must have:
- [ ] Read this ENTIRE guide (use Read tool, not memory)
- [ ] Verified STAGE_5ab complete (Round 2)
- [ ] Verified confidence level >= MEDIUM
- [ ] Verified test coverage >90%
- [ ] Located todo.md file

**If resuming after session compaction:**
1. Check feature README.md "Agent Status" section for current iteration
2. Re-read this guide from the beginning
3. Continue from documented checkpoint

---

## Quick Start

### What is this sub-stage?

**STAGE_5ac Part 1 - Preparation** is the first half of Round 3, where you prepare for implementation by defining phasing, rollback strategies, final algorithm traceability, performance optimizations, mock audits, and output validation through 6 systematic iterations (17-22).

**This is NOT final validation** - Part 2 (Iterations 23, 23a, 25, 24) handles mandatory gates and GO/NO-GO decision.

### When do you use this guide?

**Use this guide when:**
- Round 2 (STAGE_5ab) complete
- Confidence level >= MEDIUM
- Test coverage >90%
- Ready for implementation preparation

**Do NOT use this guide if:**
- Round 2 not complete
- Confidence level < MEDIUM
- Test coverage <90%
- Any blockers exist

### What are the key outputs?

1. **Implementation Phasing Plan** (Iteration 17)
   - Phases defined with checkpoints
   - Prevents "big bang" integration

2. **Rollback Strategy** (Iteration 18)
   - How to rollback if critical issues found
   - Config toggle or git revert documented

3. **Final Algorithm Traceability Matrix** (Iteration 19)
   - ALL spec algorithms mapped to TODO tasks
   - 40+ mappings typical

4. **Performance Assessment** (Iteration 20)
   - Performance impact estimated
   - Optimizations identified and tasked

5. **Mock Audit Report** (Iteration 21)
   - Every mock verified against real interface
   - Integration tests with real objects planned

6. **Output Consumer Validation** (Iteration 22)
   - Downstream consumers identified
   - Roundtrip tests planned

### Time estimate

**45-60 minutes** (6 iterations)
- Iteration 17: 5-10 minutes
- Iteration 18: 5 minutes
- Iteration 19: 10-15 minutes (comprehensive)
- Iteration 20: 10-15 minutes
- Iteration 21: 10-15 minutes (critical - mock audit)
- Iteration 22: 5-10 minutes

### Workflow overview

```
STAGE_5ac Part 1 Workflow (Iterations 17-22)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Prerequisites Met?
  ├─ Round 2 complete (STAGE_5ab)
  ├─ Confidence >= MEDIUM
  ├─ Test coverage >90%
  └─ No blockers
         │
         ▼
┌─────────────────────────────────────────┐
│ Iteration 17: Implementation Phasing   │
│ (Break into phases with checkpoints)   │
└─────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│ Iteration 18: Rollback Strategy        │
│ (Define how to rollback if needed)     │
└─────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│ Iteration 19: Algorithm Traceability   │
│ (Final verification of all mappings)   │
└─────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│ Iteration 20: Performance Assessment   │
│ (Identify bottlenecks, plan optimizations) │
└─────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│ Iteration 21: Mock Audit (CRITICAL)    │
│ (Verify mocks match real interfaces)   │
└─────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│ Iteration 22: Output Consumer Validation│
│ (Verify outputs consumable downstream) │
└─────────────────────────────────────────┘
         │
         ▼
    Part 1 COMPLETE
         │
         ▼
    Transition to Part 2
    (Read STAGE_5ac_part2_final_gates_guide.md)
```

---

## Critical Rules for Part 1

```
┌─────────────────────────────────────────────────────────────┐
│ CRITICAL RULES - Part 1 (Preparation Iterations)            │
└─────────────────────────────────────────────────────────────┘

1. ⚠️ ALL 6 iterations in Part 1 are MANDATORY (no skipping)
   - Iterations 17-22 prepare for implementation
   - Skipping iterations causes implementation failures

2. ⚠️ Implementation Phasing (Iteration 17) prevents "big bang" failures
   - Must define phases with clear checkpoints
   - Cannot implement everything at once
   - Each phase must have test validation

3. ⚠️ Algorithm Traceability (Iteration 19) is FINAL verification
   - Last chance to catch missing algorithm mappings
   - Typical: 40+ mappings (spec + error handling + edge cases)
   - ALL spec algorithms must be traced to TODO tasks

4. ⚠️ Mock Audit (Iteration 21) prevents interface mismatch bugs
   - MUST verify EACH mock matches real interface
   - Read actual source code (don't assume)
   - Plan at least 3 integration tests with REAL objects

5. ⚠️ Performance considerations (Iteration 20) identify bottlenecks early
   - Estimate performance impact
   - Identify O(n²) algorithms
   - Add optimization tasks if >20% regression expected

6. ⚠️ Update feature README.md Agent Status after each iteration
   - Document progress: "Iteration X/24 (Round 3) complete"
   - Document next action: "Iteration Y - {Name}"

7. ⚠️ Do NOT proceed to Part 2 without completing ALL 6 iterations
   - Part 2 requires these preparation outputs
   - Missing preparation causes gate failures
```

---

## Prerequisites

**Before starting Part 1, verify ALL of these are true:**

### From Round 2 (STAGE_5ab)
- [ ] Round 2 complete (all 9 iterations 8-16)
- [ ] Test strategy comprehensive and complete
- [ ] Edge cases enumerated and handled
- [ ] Algorithm Traceability Matrix updated (Round 2)
- [ ] E2E Data Flow updated (Round 2)
- [ ] Integration Gap Check updated (Round 2)
- [ ] Test coverage: >90%
- [ ] Documentation plan created

### Confidence & Blockers
- [ ] Confidence level: >= MEDIUM (from Round 2 checkpoint)
- [ ] No blockers in feature README.md Agent Status
- [ ] No unresolved questions in questions.md

### File Access
- [ ] todo.md exists and accessible
- [ ] spec.md complete and validated (Round 2)
- [ ] tests/ folder accessible

**If ANY prerequisite not met:**
- STOP - Do not proceed with Part 1
- Return to Round 2 (STAGE_5ab) to complete prerequisites
- Document blocker in Agent Status

---

## ROUND 3 PART 1: Preparation Iterations

### Iteration 17: Implementation Phasing

**Purpose:** Break implementation into phases for incremental validation

**Why this matters:** "Big bang" integration (implementing everything at once) causes failures. Phasing allows checkpoint validation after each phase.

**Process:**

1. **Group TODO tasks into logical phases:**

**Example Phasing:**

```markdown
## Implementation Phasing

**Phase 1: Core Data Loading (Foundation)**
- Task 1: Load ADP data from CSV
- Task 2: Add FantasyPlayer.adp_value field
- Task 3: Add FantasyPlayer.adp_rank field
- Tests: test_load_adp_data_*, test_player_fields_*
- **Checkpoint:** All loading tests pass, data structure validated

**Phase 2: Matching Logic**
- Task 4: Implement PlayerManager._match_player_to_adp()
- Task 5: Handle player not found in ADP data (edge case)
- Tests: test_match_player_*, test_unmatched_player_*
- **Checkpoint:** Matching tests pass, edge cases handled

**Phase 3: Multiplier Calculation**
- Task 6: Implement ConfigManager.get_adp_multiplier()
- Task 7: Implement PlayerManager._calculate_adp_multiplier()
- Task 8: Handle invalid ADP values (edge case)
- Tests: test_calculate_adp_*, test_invalid_adp_*
- **Checkpoint:** Calculation tests pass, all edge cases covered

**Phase 4: Score Integration**
- Task 9: Update FantasyPlayer.calculate_total_score()
- Task 10: Apply adp_multiplier to score
- Tests: test_scoring_*, test_integration_*
- **Checkpoint:** All integration tests pass, scores correct

**Phase 5: Error Handling & Edge Cases**
- Task 11: Handle ADP file missing (edge case)
- Task 12: Handle duplicate players in ADP data (edge case)
- Task 13: Validate config ADP ranges (edge case)
- Tests: test_error_*, test_edge_case_*
- **Checkpoint:** All error tests pass, graceful degradation verified

**Phase 6: Integration & Documentation**
- Task 14: Integration tests with real objects (no mocks)
- Task 15: Update documentation
- Task 16: Update league_config.json with ADP settings
- Tests: test_integration_*, test_e2e_*
- **Checkpoint:** ALL tests pass (100%), documentation complete

---

**Phasing Rules:**
1. Must complete Phase N before starting Phase N+1
2. All phase tests must pass before proceeding
3. If phase fails → Fix issues → Re-run phase tests → Proceed
4. No "skipping ahead" to later phases
```

2. **Define phase boundaries and checkpoints:**

Each phase ends with:
- **Test Validation:** All phase tests must pass
- **Mini-QC:** Quick review of phase code
- **Agent Status Update:** Document phase completion

3. **Document phasing in todo.md:**

Add phasing section to todo.md:

```markdown
---

## Implementation Phasing

[Paste phasing plan from step 1]

---
```

**Output:** Implementation phasing plan with 4-6 phases, clear checkpoints

**Update Agent Status:**
```markdown
Progress: Iteration 17/24 (Round 3 Part 1) complete
Next Action: Iteration 18 - Rollback Strategy
```

---

### Iteration 18: Rollback Strategy

**Purpose:** Define how to rollback if implementation has critical issues

**Why this matters:** Production bugs happen. Having a rollback plan enables quick recovery.

**Process:**

1. **Identify rollback mechanism:**
   - **Option 1:** Feature flag / config toggle (fastest, preferred)
   - **Option 2:** Git revert (clean, but slower)
   - **Option 3:** Disable code path (quick fix)

2. **Document rollback procedure:**

```markdown
## Rollback Strategy

**If critical bug discovered after implementation:**

### Option 1: Config Toggle (Recommended - 1 minute downtime)

**Procedure:**
1. Open `data/league_config.json`
2. Set: `"enable_adp_integration": false`
3. Restart league helper: `python run_league_helper.py`
4. Verify: Old scoring restored (check recommendations.csv)

**Rollback Time:** ~1 minute
**Impact:** Feature disabled, old behavior restored

---

### Option 2: Git Revert (Complete rollback - 5 minutes)

**Procedure:**
1. Identify commit hash: `git log --oneline` (find "feat/KAI-X: Add ADP integration")
2. Revert commit: `git revert <commit_hash>`
3. Remove ADP data file: `rm data/player_data/adp_data.csv`
4. Run tests: `python tests/run_all_tests.py` (verify clean revert)
5. Restart league helper

**Rollback Time:** ~5 minutes
**Impact:** Code reverted to pre-feature state

---

### Option 3: Code Path Disable (Emergency - 30 seconds)

**Procedure:**
1. Open `league_helper/util/PlayerManager.py`
2. Find: `if self.config.enable_adp_integration:`
3. Change to: `if False:  # EMERGENCY ROLLBACK`
4. Restart league helper

**Rollback Time:** ~30 seconds
**Impact:** ADP code path disabled, old behavior restored

---

**Rollback Decision Criteria:**
- **Critical bug (data corruption, crashes):** Use Option 1 or 2
- **Performance issue:** Use Option 1, investigate later
- **Minor bug (cosmetic issue):** Create bug fix, no rollback needed

**Testing Rollback:**
- Task 18: Add test_feature_can_be_disabled()
  - Verify: Setting enable_adp_integration=false works
  - Verify: No residual state after rollback
  - Verify: Old scoring behavior restored

---
```

3. **Add rollback test task if needed:**

```markdown
## Task 18: Test Feature Rollback

**Requirement:** Verify feature can be cleanly disabled

**Test:** test_feature_can_be_disabled()

**Acceptance Criteria:**
- [ ] Set config.enable_adp_integration = False
- [ ] Run scoring
- [ ] Verify: Old behavior restored (no ADP multiplier applied)
- [ ] Verify: No errors or warnings
- [ ] Verify: No residual ADP data in output
```

**Output:** Rollback strategy documented, rollback test task added

**Update Agent Status:**
```markdown
Progress: Iteration 18/24 (Round 3 Part 1) complete
Next Action: Iteration 19 - Algorithm Traceability Matrix (Final)
```

---

### Iteration 19: Algorithm Traceability Matrix (Final)

**Purpose:** Final verification that ALL algorithms from spec are mapped to TODO tasks

**⚠️ CRITICAL:** This is the LAST chance to catch missing algorithm mappings before implementation

**Why this matters:** Missing algorithm mappings mean features not implemented → user finds bugs in final review → massive rework

**Process:**

1. **Review previous traceability matrices:**
   - Iteration 4 (Round 1): Initial algorithm tracing
   - Iteration 11 (Round 2): Updated with test details

2. **Final verification checklist:**
   - [ ] All main algorithms from spec traced to TODO tasks?
   - [ ] All error handling algorithms traced?
   - [ ] All edge case algorithms traced?
   - [ ] All helper algorithms identified and traced?
   - [ ] No TODO tasks without spec algorithm reference?

3. **Count and verify coverage:**

```markdown
## Algorithm Traceability Matrix (FINAL - Iteration 19)

**Summary:**
- Total algorithms in spec.md: 12 (main algorithms)
- Total algorithms in TODO: 47 (includes helpers + error handling + edge cases)
- Coverage: 100% of spec + comprehensive error handling ✅

**Breakdown:**
- Main algorithms (from spec): 12
- Helper algorithms: 8
- Error handling algorithms: 15
- Edge case algorithms: 12

**Final Matrix:**

| Algorithm (from spec.md) | Spec Section | Implementation Location | TODO Task | Status |
|--------------------------|--------------|------------------------|-----------|--------|
| Load ADP data from CSV | Algorithms, step 1 | PlayerManager.load_adp_data() | Task 1 | ✅ Traced |
| Match player to ADP ranking | Algorithms, step 2 | PlayerManager._match_player_to_adp() | Task 4 | ✅ Traced |
| Calculate ADP multiplier | Algorithms, step 3 | ConfigManager.get_adp_multiplier() | Task 6 | ✅ Traced |
| Calculate adp_multiplier value | Algorithms, step 3 | PlayerManager._calculate_adp_multiplier() | Task 7 | ✅ Traced |
| Apply multiplier to score | Algorithms, step 4 | FantasyPlayer.calculate_total_score() | Task 9 | ✅ Traced |
| Handle player not in ADP data | Edge Cases, case 1 | PlayerManager._match_player_to_adp() | Task 5 | ✅ Traced |
| Handle invalid ADP value | Edge Cases, case 2 | PlayerManager._calculate_adp_multiplier() | Task 8 | ✅ Traced |
| Handle ADP file missing | Edge Cases, case 3 | PlayerManager.load_adp_data() | Task 11 | ✅ Traced |
| Validate duplicate players in ADP | Edge Cases, implicit | PlayerManager.load_adp_data() | Task 12 | ✅ Traced |
| Validate config ADP ranges | Edge Cases, implicit | ConfigManager._validate_adp_config() | Task 13 | ✅ Traced |
| Log ADP integration activity | Logging, implicit | PlayerManager (all methods) | Task 15 | ✅ Traced |
| Update config with ADP settings | Configuration, implicit | league_config.json update | Task 16 | ✅ Traced |

**Helper Algorithms Identified:**
| Helper Algorithm | Implementation Location | TODO Task | Status |
|------------------|------------------------|-----------|--------|
| Parse ADP CSV columns | PlayerManager._parse_adp_csv() | Task 2 | ✅ Traced |
| Normalize player names | PlayerManager._normalize_name() | Task 3 | ✅ Traced |
| Create ADP lookup dict | PlayerManager._create_adp_dict() | Task 4 | ✅ Traced |
| Validate ADP data types | PlayerManager._validate_adp_data() | Task 2 | ✅ Traced |
| Get default multiplier | PlayerManager._get_default_multiplier() | Task 5 | ✅ Traced |
| Log ADP match success | PlayerManager._log_adp_match() | Task 15 | ✅ Traced |
| Log ADP match failure | PlayerManager._log_adp_miss() | Task 15 | ✅ Traced |
| Format ADP for output | FantasyPlayer._format_adp_data() | Task 14 | ✅ Traced |

**Error Handling Algorithms:**
| Error Scenario | Algorithm | TODO Task | Status |
|----------------|-----------|-----------|--------|
| ADP file not found | Raise DataProcessingError with clear message | Task 11 | ✅ Traced |
| ADP file empty | Raise DataProcessingError | Task 11 | ✅ Traced |
| ADP CSV missing columns | Raise DataProcessingError | Task 2 | ✅ Traced |
| Player not in ADP data | Use default multiplier 1.0, log warning | Task 5 | ✅ Traced |
| ADP value invalid (negative) | Use default multiplier 1.0, log warning | Task 8 | ✅ Traced |
| ADP value invalid (too high) | Use default multiplier 1.0, log warning | Task 8 | ✅ Traced |
| Duplicate players in ADP | Keep first occurrence, log warning | Task 12 | ✅ Traced |
| Config missing ADP settings | Use default ranges, log warning | Task 13 | ✅ Traced |
| Config ADP ranges invalid | Use default ranges, log error | Task 13 | ✅ Traced |
| Player name mismatch | Try normalized match, log debug | Task 3 | ✅ Traced |
| ... (5 more error scenarios) ... | ... | ... | ... |

**✅ FINAL VERIFICATION: ALL ALGORITHMS TRACED (47/47 = 100%)**
```

4. **If any algorithms missing from TODO:**
   - Add tasks for missing algorithms
   - Update spec if algorithm was discovered during TODO creation
   - Document in Agent Status: "Added tasks for X missing algorithms"

**Output:** Final Algorithm Traceability Matrix with 40+ mappings (typical)

**Update Agent Status:**
```markdown
Progress: Iteration 19/24 (Round 3 Part 1) complete
Final Algorithm Traceability: 47 algorithms traced (100% coverage)
Next Action: Iteration 20 - Performance Considerations
```

---

### Iteration 20: Performance Considerations

**Purpose:** Assess performance impact and identify optimization needs

**Why this matters:** Performance regressions discovered post-implementation require rework. Planning optimizations now prevents this.

**Process:**

1. **Estimate baseline performance (before feature):**
   - Measure current startup time, operation time
   - Document in performance analysis

2. **Estimate feature performance impact:**
   - Analyze algorithmic complexity
   - Estimate time for each operation
   - Calculate total impact

3. **Example Performance Analysis:**

```markdown
## Performance Analysis (Iteration 20)

**Baseline Performance (before feature):**
- Player loading: 2.5s (500 players from CSV)
- Score calculation: 0.8s (500 players)
- Total startup time: 3.3s

**Estimated Performance (with feature):**
- ADP CSV loading: +0.1s (small file, 500 rows)
- Player matching: +5.0s ⚠️ (O(n²) list iteration - 500 × 500 comparisons)
- ADP multiplier calculation: +0.1s (simple arithmetic)
- Total startup time: 8.5s

**Performance Impact:** +5.2s (157% increase) ⚠️ SIGNIFICANT REGRESSION

**Bottleneck Identified:** Player matching to ADP data

**Current Algorithm (O(n²)):**
```python
# O(n²) - slow for 500 players
for player in players:  # 500 iterations
    for (name, pos, adp) in adp_data:  # 500 iterations each
        if player.name == name and player.position == pos:
            player.adp_value = adp
            break
```

**Total comparisons:** 500 × 500 = 250,000 comparisons
**Estimated time:** 250,000 × 20µs = 5.0s ⚠️

---

## Optimization Strategy

**Problem:** O(n²) algorithm for player matching

**Solution:** Use dict for O(1) lookup → O(n) total complexity

**Optimized Algorithm (O(n)):**
```python
# O(n) - fast for 500 players
# Create dict once: O(n)
adp_dict = {(name, pos): adp_value for (name, pos, adp_value) in adp_data}

# Lookup: O(1) per player, O(n) total
for player in players:  # 500 iterations
    key = (player.name, player.position)
    player.adp_value = adp_dict.get(key)  # O(1) lookup
```

**Total operations:** 500 + 500 = 1,000 operations
**Estimated time:** 1,000 × 10µs = 0.01s ✅

**Performance Improvement:** 5.0s → 0.01s (500x faster!)

**New Total Startup Time:** 3.3s + 0.1s + 0.01s + 0.1s = 3.5s
**Final Impact:** +0.2s (6% increase) ✅ ACCEPTABLE

---

## Performance Optimization Tasks

**Task 30: Performance Optimization - ADP Lookup Dict**

**Requirement:** Use dict for O(1) ADP lookup instead of O(n²) list iteration

**Implementation:**
- Create: `self.adp_dict = {(name, position): adp_value}`
- Lookup: `adp_value = self.adp_dict.get((player.name, player.position))`

**Acceptance Criteria:**
- [ ] ADP data stored in dict (not list iteration)
- [ ] Lookup time: <1ms per player
- [ ] Total matching time: <100ms for 500 players
- [ ] Verified: No performance regression vs baseline

**Test:** test_adp_lookup_performance()
- Measure: Time to match 500 players
- Assert: Time < 100ms
- Assert: Dict used (not list)

---
```

4. **Add optimization tasks to todo.md if needed:**
   - If regression >20% → Add optimization tasks
   - If regression <20% → Document but no tasks needed

**Output:** Performance analysis, optimization tasks (if regression >20%)

**Update Agent Status:**
```markdown
Progress: Iteration 20/24 (Round 3 Part 1) complete
Performance Impact: +0.2s after optimization (6% acceptable)
Next Action: Iteration 21 - Mock Audit & Integration Test Plan
```

---

### Iteration 21: Mock Audit & Integration Test Plan (CRITICAL)

**Purpose:** Verify mocks match real interfaces, plan integration tests with real objects

**⚠️ CRITICAL:** Unit tests with wrong mocks can pass while hiding interface mismatch bugs

**Why this matters:**
- Mocks that don't match real interfaces → Tests pass but feature fails
- Integration tests with real objects → Prove feature works in real environment

**Process:**

1. **List ALL mocked dependencies in unit tests:**

Review test files and identify every mocked class/function.

2. **For EACH mock, verify against real interface:**

```markdown
## Mock Audit (Iteration 21)

### Mock 1: ConfigManager.get_adp_multiplier

**Used in tests:** test_calculate_adp_multiplier_valid()

**Mock definition:**
```python
# In test file
mock_config.get_adp_multiplier.return_value = (1.2, 95)
```

**Real interface verification:**

Step 1: Read actual source code
```bash
# Read real implementation
Read league_helper/util/ConfigManager.py
# Found at line 234
```

Step 2: Verify real signature
```python
# Real interface from ConfigManager.py:234
def get_adp_multiplier(self, adp: int) -> Tuple[float, int]:
    """Returns (multiplier, rank) based on ADP value.

    Args:
        adp (int): ADP ranking value

    Returns:
        Tuple[float, int]: (multiplier, rank)
    """
    # implementation...
```

Step 3: Compare mock to real
- **Mock accepts:** ANY arguments (over-mocking) ⚠️
- **Real accepts:** adp (int)
- **⚠️ PARAMETER MISMATCH:** Mock too permissive, doesn't validate type

- **Mock returns:** (1.2, 95) - Tuple[float, int] ✅
- **Real returns:** Tuple[float, int] ✅
- **✅ RETURN TYPE MATCH**

**Issue Found:** Mock doesn't validate parameter type

**Fix:** Update mock to validate parameters
```python
def mock_get_adp_multiplier(adp: int):
    assert isinstance(adp, int), "adp must be int"
    assert adp > 0, "adp must be positive"
    return (1.2, 95)

mock_config.get_adp_multiplier = mock_get_adp_multiplier
```

**Verification:** ✅ FIXED - Mock now matches real interface

**Action:** Update test file with fixed mock

---

### Mock 2: csv_utils.read_csv_with_validation

**Used in tests:** test_load_adp_data_success()

**Mock definition:**
```python
mock_read_csv.return_value = pd.DataFrame([...])
```

**Real interface verification:**

Step 1: Read actual source
```bash
Read utils/csv_utils.py
# Found at line 45
```

Step 2: Verify real signature
```python
# Real interface from csv_utils.py:45
def read_csv_with_validation(
    filepath: Union[str, Path],
    required_columns: List[str],
    encoding: str = 'utf-8'
) -> pd.DataFrame:
    """Reads CSV and validates required columns exist."""
```

Step 3: Compare mock to real
- **Mock accepts:** ANY (uses MagicMock default) ✅
- **Real accepts:** filepath, required_columns, encoding (optional)
- **✅ ACCEPTABLE:** Test only uses (filepath, required_columns)

- **Mock returns:** pd.DataFrame ✅
- **Real returns:** pd.DataFrame ✅
- **✅ RETURN TYPE MATCH**

**Verification:** ✅ PASSED - Mock matches real interface

---

### Mock 3: [Continue for ALL mocks in test suite]

[Repeat mock audit for each dependency]

---

## Mock Audit Summary

**Total Mocks Audited:** 5
**Mocks with Issues:** 1 (ConfigManager.get_adp_multiplier)
**Fixes Required:** 1 (update mock to validate parameters)

**✅ All mock issues fixed, audit PASSED**

---
```

3. **Plan integration tests with REAL objects (no mocks):**

```markdown
## Integration Test Plan (No Mocks)

**Purpose:** Prove feature works with REAL objects (not mocks)

**Why no mocks:** Catch interface mismatches that mocks hide

---

### Integration Test 1: test_adp_integration_with_real_config()

**Purpose:** Verify ADP integration works with REAL ConfigManager

**Setup:**
- Use REAL ConfigManager (not mock)
- Use REAL league_config.json
- Use test ADP CSV file in tmp_path

**Steps:**
1. Create test config file: `tmp_path / "league_config.json"`
2. Initialize REAL ConfigManager(data_folder=tmp_path)
3. Load ADP data from test CSV
4. Match player "Patrick Mahomes, QB"
5. Call REAL ConfigManager.get_adp_multiplier(adp=5)
6. Verify result matches expected (multiplier, rank) from config

**Acceptance Criteria:**
- [ ] Uses REAL ConfigManager (no mocks)
- [ ] Uses REAL league_config.json
- [ ] No mocks used anywhere
- [ ] Test passes (proves real integration works)

**Expected Duration:** ~100ms (acceptable for integration test)

---

### Integration Test 2: test_adp_integration_with_real_csv_utils()

**Purpose:** Verify ADP loading works with REAL csv_utils

**Setup:**
- Use REAL csv_utils.read_csv_with_validation
- Create test CSV file in tmp_path

**Steps:**
1. Create test CSV: `tmp_path / "adp_test.csv"`
2. Write test data: "Name,Position,ADP\nPatrick Mahomes,QB,5\n"
3. Call REAL csv_utils.read_csv_with_validation(filepath, required_columns)
4. Verify DataFrame loaded correctly
5. Verify columns exist: Name, Position, ADP

**Acceptance Criteria:**
- [ ] Uses REAL csv_utils (no mocks)
- [ ] Creates real CSV file
- [ ] No mocks used
- [ ] Test proves CSV parsing works

**Expected Duration:** ~50ms

---

### Integration Test 3: test_adp_end_to_end_real_objects()

**Purpose:** Full E2E test with ALL real objects (comprehensive)

**Setup:**
- REAL ConfigManager
- REAL csv_utils
- REAL PlayerManager
- REAL FantasyPlayer
- NO MOCKS ANYWHERE

**Steps:**
1. Initialize PlayerManager with test data folder
2. Load ADP data (uses REAL csv_utils)
3. Load players (uses REAL PlayerManager)
4. Calculate scores (uses REAL ConfigManager.get_adp_multiplier())
5. Verify: All players have adp_value set
6. Verify: All players have adp_rank set
7. Verify: Scores reflect ADP contribution
8. Verify: Top-ranked player (ADP=1) has highest multiplier

**Acceptance Criteria:**
- [ ] NO MOCKS used anywhere in test
- [ ] All objects are real implementations
- [ ] All steps execute successfully
- [ ] Test proves entire feature works end-to-end

**Expected Duration:** ~500ms (acceptable for E2E test)

---
```

4. **Add integration test tasks to todo.md:**

```markdown
## Task 35: Integration Test - Real ConfigManager

**Requirement:** Test ADP integration with REAL ConfigManager (no mocks)

**Test:** test_adp_integration_with_real_config()

**Acceptance Criteria:**
- [ ] Uses REAL ConfigManager
- [ ] Uses REAL league_config.json
- [ ] No mocks used
- [ ] Test passes (proves real integration works)

---

## Task 36: Integration Test - Real CSV Utils

**Requirement:** Test ADP loading with REAL csv_utils (no mocks)

**Test:** test_adp_integration_with_real_csv_utils()

**Acceptance Criteria:**
- [ ] Uses REAL csv_utils.read_csv_with_validation
- [ ] Creates test CSV file
- [ ] No mocks used
- [ ] Test passes

---

## Task 37: Integration Test - End-to-End (No Mocks)

**Requirement:** Full E2E test with ALL real objects

**Test:** test_adp_end_to_end_real_objects()

**Acceptance Criteria:**
- [ ] Uses REAL ConfigManager, csv_utils, PlayerManager
- [ ] NO mocks used anywhere
- [ ] All steps execute successfully
- [ ] Test proves feature works in real environment

---
```

**Output:**
- Mock audit report (all mocks verified)
- Integration test plan (at least 3 real-object tests)
- Tasks added for integration tests

**Update Agent Status:**
```markdown
Progress: Iteration 21/24 (Round 3 Part 1) complete
Mock Audit: 5 mocks audited, 1 issue fixed
Integration Tests: 3 real-object tests planned
Next Action: Iteration 22 - Output Consumer Validation
```

---

### Iteration 22: Output Consumer Validation

**Purpose:** Verify feature outputs are consumable by downstream code

**Why this matters:** Feature can work in isolation but fail when consumed by other modules → Integration failures

**Process:**

1. **Identify output consumers:**

```markdown
## Output Consumer Analysis

**Feature Output:** Updated FantasyPlayer objects with:
- player.adp_value (int): ADP ranking
- player.adp_rank (int): Rank in ADP list
- player.adp_multiplier (float): Score multiplier from ADP

**Downstream Consumers:**

1. **AddToRosterModeManager.get_recommendations()**
   - Consumes: FantasyPlayer objects with adp_multiplier
   - Usage: Generates draft recommendations sorted by score
   - Impact: Must handle players with adp_multiplier applied

2. **StarterHelperModeManager.get_optimal_lineup()**
   - Consumes: Roster FantasyPlayer objects with adp_multiplier
   - Usage: Selects optimal lineup based on scores
   - Impact: Must use ADP-adjusted scores for lineup decisions

3. **TradeAnalyzerModeManager.analyze_trade()**
   - Consumes: FantasyPlayer objects for trade analysis
   - Usage: Compares player values
   - Impact: Should use ADP-adjusted scores for trade value

---
```

2. **Plan roundtrip validation tests:**

```markdown
## Output Consumer Validation Tests

### Consumer 1: AddToRosterModeManager (Draft Mode)

**Roundtrip Test:** test_adp_output_consumed_by_draft_mode()

**Steps:**
1. Load players with ADP integration (REAL PlayerManager)
2. Verify: Players have adp_value, adp_rank, adp_multiplier set
3. Call: AddToRosterModeManager.get_recommendations() with ADP-enabled players
4. Verify: Recommendations generated successfully (no errors)
5. Verify: Recommendations use ADP-adjusted scores
6. Verify: Top recommendations include high-ADP players (logic check)
7. Verify: Low-ADP players ranked lower

**Expected Behavior:** Draft recommendations prioritize high-ADP players

**Acceptance Criteria:**
- [ ] Consumer code runs without errors
- [ ] Recommendations use adp_multiplier in scoring
- [ ] Top 10 recommendations include players with ADP <20
- [ ] No AttributeError or KeyError

---

### Consumer 2: StarterHelperModeManager (Starter Mode)

**Roundtrip Test:** test_adp_output_consumed_by_starter_mode()

**Steps:**
1. Load roster players with ADP integration
2. Verify: Roster players have adp_multiplier set
3. Call: StarterHelperModeManager.get_optimal_lineup()
4. Verify: Lineup selection successful (no errors)
5. Verify: Lineup scores include ADP contribution
6. Verify: Optimal lineup selects high-ADP players when scores close

**Expected Behavior:** Lineup optimizer uses ADP-adjusted scores

**Acceptance Criteria:**
- [ ] Consumer code runs without errors
- [ ] Lineup scores reflect adp_multiplier
- [ ] No AttributeError or KeyError

---

### Consumer 3: TradeAnalyzerModeManager (Trade Mode)

**Roundtrip Test:** test_adp_output_consumed_by_trade_analyzer()

**Steps:**
1. Load players with ADP integration
2. Create mock trade: Give player A, Receive player B
3. Call: TradeAnalyzerModeManager.analyze_trade()
4. Verify: Trade analysis successful (no errors)
5. Verify: Trade value uses ADP-adjusted scores
6. Verify: Analysis shows "fair" when ADP values similar

**Expected Behavior:** Trade analysis uses ADP-adjusted values

**Acceptance Criteria:**
- [ ] Consumer code runs without errors
- [ ] Trade values reflect adp_multiplier
- [ ] No AttributeError or KeyError

---
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
- [ ] Verify top recommendations include high-ADP players
- [ ] No errors in consumer code

---

## Task 41: Consumer Validation - Starter Mode

**Requirement:** Verify StarterHelperModeManager consumes ADP-adjusted scores

**Test:** test_adp_output_consumed_by_starter_mode()

**Acceptance Criteria:**
- [ ] Load roster with ADP integration
- [ ] Call StarterHelperModeManager.get_optimal_lineup()
- [ ] Verify lineup selection works
- [ ] Verify lineup scores include ADP contribution
- [ ] No errors in consumer code

---

## Task 42: Consumer Validation - Trade Analyzer

**Requirement:** Verify TradeAnalyzerModeManager consumes ADP-adjusted scores

**Test:** test_adp_output_consumed_by_trade_analyzer()

**Acceptance Criteria:**
- [ ] Load players with ADP integration
- [ ] Call TradeAnalyzerModeManager.analyze_trade()
- [ ] Verify trade analysis works
- [ ] Verify trade values use ADP-adjusted scores
- [ ] No errors in consumer code

---
```

**Output:** Output consumer validation plan with roundtrip tests

**Update Agent Status:**
```markdown
Progress: Iteration 22/24 (Round 3 Part 1) complete
Consumer Validation: 3 consumers identified, roundtrip tests planned
Part 1 COMPLETE - Ready for Part 2
Next Action: Read STAGE_5ac_part2_final_gates_guide.md
```

---

## Part 1 Completion Criteria

**Part 1 is COMPLETE when ALL of these are true:**

### All 6 Iterations Complete
- [ ] Iteration 17: Implementation Phasing plan created
- [ ] Iteration 18: Rollback Strategy documented
- [ ] Iteration 19: Algorithm Traceability Matrix final (40+ mappings)
- [ ] Iteration 20: Performance assessment complete, optimizations planned
- [ ] Iteration 21: Mock audit complete, integration tests planned
- [ ] Iteration 22: Output consumer validation planned

### Documentation Updated
- [ ] todo.md contains implementation phasing
- [ ] todo.md contains rollback strategy
- [ ] todo.md contains final algorithm traceability matrix
- [ ] todo.md contains performance optimization tasks (if needed)
- [ ] todo.md contains integration test tasks (at least 3)
- [ ] todo.md contains consumer validation tasks

### Agent Status Updated
- [ ] feature README.md Agent Status shows: "Part 1 complete, ready for Part 2"
- [ ] Progress documented: "Iteration 22/24 (Round 3 Part 1) complete"
- [ ] Next action set: "Read STAGE_5ac_part2_final_gates_guide.md"

**If ALL items checked:**
- Part 1 is COMPLETE
- Proceed to Part 2 (Final Gates)
- Read STAGE_5ac_part2_final_gates_guide.md

**If ANY item unchecked:**
- STOP - Do not proceed to Part 2
- Complete missing iterations
- Re-verify completion criteria

---

## Common Mistakes to Avoid

### ❌ MISTAKE 1: "Skipping Implementation Phasing (Iteration 17)"

**Why this is wrong:**
- "Big bang" integration (all at once) causes failures
- No incremental validation checkpoints
- Hard to debug when everything fails

**What to do instead:**
- ✅ Define 4-6 logical phases
- ✅ Add checkpoint validation after each phase
- ✅ Document phasing in todo.md

---

### ❌ MISTAKE 2: "Not verifying mocks against real interfaces (Iteration 21)"

**Why this is wrong:**
- Mocks that don't match real interfaces → Tests pass but code fails
- Interface changes not caught by tests
- False sense of security

**What to do instead:**
- ✅ Read ACTUAL source code for each mocked dependency
- ✅ Verify parameter types match
- ✅ Verify return types match
- ✅ Fix mock mismatches immediately

**Example:**
```
BAD: Assume mock is correct
GOOD: Read utils/csv_utils.py:45, verify signature matches mock
```

---

### ❌ MISTAKE 3: "Skipping integration tests with real objects"

**Why this is wrong:**
- Only unit tests with mocks → Don't prove feature works
- Interface mismatches not caught
- Integration failures discovered late

**What to do instead:**
- ✅ Plan at least 3 integration tests with REAL objects
- ✅ NO MOCKS in integration tests
- ✅ Test proves feature works in real environment

---

### ❌ MISTAKE 4: "Not optimizing performance bottlenecks (Iteration 20)"

**Why this is wrong:**
- Performance regression >20% → User complaints
- Optimization post-implementation harder
- May require architectural changes

**What to do instead:**
- ✅ Estimate performance impact
- ✅ Identify O(n²) algorithms
- ✅ Plan optimizations if regression >20%
- ✅ Add optimization tasks to todo.md

**Example:**
```
O(n²) player matching → 5.0s (unacceptable)
O(n) dict lookup → 0.01s (acceptable)
```

---

## Prerequisites for Next Stage

**Before proceeding to Part 2 (STAGE_5ac_part2_final_gates_guide.md), verify:**

### Part 1 Completion
- [ ] ALL 6 iterations complete (17-22)
- [ ] Implementation phasing defined
- [ ] Rollback strategy documented
- [ ] Algorithm traceability 100%
- [ ] Performance optimized (if needed)
- [ ] Mocks audited and fixed
- [ ] Integration tests planned
- [ ] Output consumers validated

### Documentation
- [ ] todo.md updated with all Part 1 outputs
- [ ] feature README.md Agent Status shows Part 1 complete

### Readiness
- [ ] No blockers
- [ ] Confidence level still >= MEDIUM
- [ ] Ready for mandatory gates (Part 2)

**Only proceed to Part 2 when ALL items checked.**

**Next stage:** STAGE_5ac_part2_final_gates_guide.md

---

## Summary

**STAGE_5ac Part 1 - Preparation prepares all prerequisites for implementation:**

**Key Activities:**
1. **Implementation Phasing (Iteration 17):** Break into phases with checkpoints
2. **Rollback Strategy (Iteration 18):** Define how to rollback if needed
3. **Algorithm Traceability (Iteration 19):** Final verification (40+ mappings)
4. **Performance Assessment (Iteration 20):** Identify bottlenecks, optimize
5. **Mock Audit (Iteration 21):** Verify mocks match real interfaces, plan integration tests
6. **Output Consumer Validation (Iteration 22):** Verify outputs consumable downstream

**Critical Outputs:**
- Implementation phasing plan (prevents "big bang" failures)
- Final algorithm traceability (100% coverage)
- Mock audit report (interface mismatches fixed)
- Integration test plan (at least 3 real-object tests)
- Performance optimization plan (if regression >20%)

**Success Criteria:**
- All 6 iterations complete
- No missing algorithm mappings
- All mocks verified
- Integration tests planned
- Ready for mandatory gates (Part 2)

**Next Stage:** STAGE_5ac_part2_final_gates_guide.md - Final validation and GO/NO-GO decision

**Remember:** Part 1 preparation prevents implementation failures. Thoroughness here saves massive rework later.

---

**END OF STAGE 5ac PART 1 GUIDE**
