# STAGE 5ac Part 2a: TODO Creation - Round 3 Gates 1-2 (Iterations 23, 23a)

**Part of:** Epic-Driven Development Workflow v2
**Stage:** 5ac - TODO Creation Round 3
**Sub-Stage:** Part 2a - Gates 1-2 (Integration Gap Check, Pre-Implementation Spec Audit)
**Prerequisites:** STAGE_5ac_part1 complete (Iterations 17-22)
**Next Stage:** stages/stage_5/round3_part2b_gate_3.md

---

## 🚨 MANDATORY READING PROTOCOL

**CRITICAL:** You MUST read this ENTIRE guide before starting Part 2a.

**Why this matters:**
- Part 2a contains 2 MANDATORY GATES that cannot be skipped
- Missing gates causes catastrophic implementation failures
- Iteration 23a has 5 PARTS (ALL must PASS)

**Reading Checkpoint:**
Before proceeding, you must have:
- [ ] Read this ENTIRE guide (use Read tool, not memory)
- [ ] Verified STAGE_5ac_part1 complete (Iterations 17-22)
- [ ] Verified all Part 1 outputs documented in todo.md
- [ ] Located spec.md file

**If resuming after session compaction:**
1. Check feature README.md "Agent Status" section for current iteration
2. Re-read this guide from the beginning
3. Continue from documented checkpoint

---

## Quick Start

### What is this sub-stage?

**STAGE_5ac Part 2a - Gates 1-2** is the first half of Round 3 Part 2, where you execute final integration verification and comprehensive pre-implementation spec audit through 2 critical iterations (23, 23a).

**This contains 2 mandatory gates:**
- **Gate 1:** Iteration 23 - Final Integration Gap Check
- **Gate 2:** Iteration 23a - Pre-Implementation Spec Audit (4 PARTS)

### When do you use this guide?

**Use this guide when:**
- Part 1 (STAGE_5ac_part1) complete
- All preparation iterations (17-22) done
- Ready for mandatory gates 1-2

**Do NOT use this guide if:**
- Part 1 not complete
- Any preparation iterations skipped
- Missing Part 1 outputs (phasing, traceability, mock audit)

### What are the key outputs?

1. **Final Integration Gap Check** (Iteration 23)
   - All methods have callers verified
   - No orphan code

2. **Pre-Implementation Spec Audit - 4 PARTS** (Iteration 23a - MANDATORY GATE)
   - PART 1: Completeness (all requirements have tasks)
   - PART 2: Specificity (all tasks have acceptance criteria)
   - PART 3: Interface Contracts (all dependencies verified)
   - PART 4: Integration Evidence (all methods have callers)

### Time estimate

**30-40 minutes** (2 iterations including 1 mandatory gate with 4 parts)
- Iteration 23: 10 minutes
- Iteration 23a: 20-30 minutes (4 PARTS - comprehensive)

### Workflow overview

```
STAGE_5ac Part 2a Workflow (Iterations 23, 23a)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Prerequisites Met?
  ├─ Part 1 complete (Iterations 17-22)
  ├─ Implementation phasing defined
  ├─ Algorithm traceability 100%
  └─ Mock audit complete
         │
         ▼
┌─────────────────────────────────────────────────┐
│ Iteration 23: Integration Gap Check (Final)    │
│ (Verify all methods have callers)              │
└─────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────┐
│ Iteration 23a: Pre-Implementation Spec Audit   │
│ (MANDATORY GATE - ALL 4 PARTS MUST PASS)       │
│ PART 1: Completeness                           │
│ PART 2: Specificity                            │
│ PART 3: Interface Contracts                    │
│ PART 4: Integration Evidence                   │
└─────────────────────────────────────────────────┘
         │
    [ALL 5 PARTS PASSED?]
         │
         ▼
    Part 2a COMPLETE → Proceed to Part 2b
    (stages/stage_5/round3_part2b_gate_3.md)
```

---

## Critical Rules for Part 2a

```
┌─────────────────────────────────────────────────────────────┐
│ CRITICAL RULES - Part 2a (Gates 1-2)                        │
└─────────────────────────────────────────────────────────────┘

1. ⚠️ BOTH iterations in Part 2a are MANDATORY (no skipping)
   - Iterations 23, 23a are FINAL gates
   - Skipping gates causes catastrophic failures

2. ⚠️ Iteration 23a has 4 MANDATORY PARTS (ALL must PASS)
   - CANNOT proceed to Part 2b without "ALL 5 PARTS PASSED"
   - If ANY part fails → Fix and re-run Iteration 23a

3. ⚠️ Update feature README.md Agent Status after Iteration 23a
   - Document Iteration 23a result (ALL 4 PARTS status)
   - Document next action (Part 2b)

4. ⚠️ Evidence required for verification
   - Cannot just check boxes
   - Must cite specific numbers (N requirements, M tasks, etc.)
   - Provide evidence of completion
```

---

## Prerequisites

**Before starting Part 2a, verify ALL of these are true:**

### From Part 1 (STAGE_5ac_part1)
- [ ] Part 1 complete (Iterations 17-22)
- [ ] Implementation phasing defined (4-6 phases)
- [ ] Rollback strategy documented
- [ ] Algorithm Traceability Matrix final (40+ mappings)
- [ ] Performance assessment complete
- [ ] Mock audit complete (all mocks verified)
- [ ] Integration tests planned (at least 3)
- [ ] Output consumer validation planned

### File Access
- [ ] todo.md exists and contains all Part 1 outputs
- [ ] spec.md exists and complete

### Quality State
- [ ] Confidence level >= MEDIUM (from Round 2)
- [ ] Test coverage >90%
- [ ] No blockers

**If ANY prerequisite not met:**
- STOP - Do not proceed with Part 2a
- Return to Part 1 (STAGE_5ac_part1) to complete missing items
- Document blocker in Agent Status

---

## ROUND 3 PART 2a: Gates 1-2

### Iteration 23: Integration Gap Check (Final)

**Purpose:** Final verification - no orphan code

**⚠️ CRITICAL:** This is the LAST chance to catch orphan methods

**Why this matters:** Methods without callers = dead code → Wasted implementation effort

**Process:**

1. **Review integration matrices from earlier rounds:**
   - Iteration 7 (Round 1): Initial integration matrix
   - Iteration 14 (Round 2): Updated integration matrix

2. **Verify ALL new methods have callers:**

Count verification:
- Total new methods (all rounds): {N}
- Methods with identified callers: {M}
- ✅ PASS if M == N
- ❌ FAIL if M < N

3. **Create final integration matrix:**

```markdown
## Integration Gap Check (FINAL - Iteration 23)

**Total New Methods:** 12

**Final Verification Table:**

| New Method | Caller | Call Location | Round Added | Verified |
|------------|--------|---------------|-------------|----------|
| PlayerManager.load_adp_data() | PlayerManager.load_players() | PlayerManager.py:180 | Round 1 | ✅ |
| PlayerManager._match_player_to_adp() | PlayerManager.load_players() | PlayerManager.py:210 | Round 1 | ✅ |
| PlayerManager._calculate_adp_multiplier() | PlayerManager.load_players() | PlayerManager.py:215 | Round 1 | ✅ |
| ConfigManager.get_adp_multiplier() | PlayerManager._calculate_adp_multiplier() | PlayerManager.py:215 | Round 1 | ✅ |
| ConfigManager._validate_adp_config() | ConfigManager.__init__() | ConfigManager.py:85 | Round 2 | ✅ |
| PlayerManager._handle_duplicate_adp() | PlayerManager.load_adp_data() | PlayerManager.py:465 | Round 2 | ✅ |
| PlayerManager._create_adp_dict() | PlayerManager.load_adp_data() | PlayerManager.py:470 | Round 3 | ✅ |
| PlayerManager._normalize_player_name() | PlayerManager._match_player_to_adp() | PlayerManager.py:485 | Round 3 | ✅ |
| FantasyPlayer._format_adp_data() | FantasyPlayer.to_dict() | FantasyPlayer.py:120 | Round 2 | ✅ |
| PlayerManager._log_adp_match() | PlayerManager._match_player_to_adp() | PlayerManager.py:490 | Round 3 | ✅ |
| PlayerManager._log_adp_miss() | PlayerManager._match_player_to_adp() | PlayerManager.py:495 | Round 3 | ✅ |
| PlayerManager._get_default_multiplier() | PlayerManager._calculate_adp_multiplier() | PlayerManager.py:500 | Round 2 | ✅ |

**Verification:**
- Total new methods: 12
- Methods with callers: 12
- Integration: 100% ✅

**✅ FINAL VERIFICATION: NO ORPHAN CODE - ALL METHODS INTEGRATED**

---
```

4. **If any methods without callers:**
   - Identify orphan methods
   - Determine if needed (add caller) or unnecessary (remove)
   - Update TODO accordingly

**Output:** Final integration verification (all methods have callers)

**Update Agent Status:**
```markdown
Progress: Iteration 23/24 (Round 3 Part 2a) complete
Integration Gap Check: 12/12 methods verified (no orphans)
Next Action: Iteration 23a - Pre-Implementation Spec Audit (MANDATORY - 4 PARTS)
```

---

### Iteration 23a: Pre-Implementation Spec Audit (MANDATORY GATE - 5 PARTS)

**Purpose:** Final comprehensive audit before implementation

**⚠️ MANDATORY:** ALL 5 PARTS must PASS before proceeding to Part 2b

**Why this matters:**
- PART 1 ensures all requirements have tasks
- PART 2 ensures all tasks are specific enough to implement
- PART 3 ensures external interfaces are correct
- PART 4 ensures integration evidence exists

**Failing ANY part → Implementing incomplete/wrong solution**

---

#### PART 1: Completeness Audit

**Question:** Does every requirement from spec.md have corresponding TODO tasks?

**Process:**

1. List all requirements from spec.md:
   - Main requirements
   - Edge cases
   - Error handling
   - Performance requirements
   - Documentation requirements

2. For each requirement, find corresponding TODO task(s)

3. Count coverage:
   - Requirements in spec.md: {N}
   - Requirements with TODO tasks: {M}
   - Coverage: M/N × 100%
   - ✅ PASS if coverage = 100%
   - ❌ FAIL if coverage < 100%

**Example:**

```markdown
## PART 1: Completeness Audit

**Requirements from spec.md:**

### Main Requirements
1. Load ADP data from CSV → Task 1 ✅
2. Match players to ADP rankings → Task 4 ✅
3. Calculate ADP multiplier from config → Task 6 ✅
4. Apply multiplier to player scoring → Task 9 ✅

### Edge Cases (from spec.md Edge Cases section)
5. Handle ADP file not found → Task 11 ✅
6. Handle player not in ADP data → Task 5 ✅
7. Handle invalid ADP values → Task 8 ✅
8. Handle duplicate players in ADP → Task 12 ✅

### Error Handling
9. Raise DataProcessingError for file errors → Task 11 ✅
10. Log warnings for missing players → Task 5 ✅
11. Validate config ADP ranges → Task 13 ✅

### Performance
12. Use dict for O(1) lookup → Task 30 ✅

### Documentation
13. Update league_config.json with ADP settings → Task 16 ✅
14. Add docstrings to new methods → Task 15 ✅

### Integration
15. Create integration tests with real objects → Tasks 35, 36, 37 ✅

**Verification:**
- Total requirements in spec.md: 15
- Requirements with TODO tasks: 15
- Coverage: 100% ✅

**PART 1: ✅ PASS**

---
```

**If PART 1 FAILS:**
- List missing requirements
- Add TODO tasks for missing requirements
- Re-run PART 1 until coverage = 100%

---

#### PART 2: Specificity Audit

**Question:** Does every TODO task have concrete, implementable acceptance criteria?

**Process:**

1. Review EVERY TODO task

2. For each task, verify it has:
   - Specific acceptance criteria (not vague like "make it work")
   - Implementation location (file, class, method name, approximate line)
   - Test coverage (list of test names)
   - **Category-specific tests if applicable** (e.g., if code processes QB, RB, WR → verify tests for EACH position)

3. Count specificity:
   - Total TODO tasks: {N}
   - Tasks with acceptance criteria: {M1}
   - Tasks with implementation location: {M2}
   - Tasks with test coverage: {M3}
   - Specificity: min(M1, M2, M3) / N × 100%
   - ✅ PASS if specificity = 100%
   - ❌ FAIL if specificity < 100%

**Example:**

```markdown
## PART 2: Specificity Audit

**Reviewing all TODO tasks:**

### Task 1: Load ADP data from CSV
- ✅ Has acceptance criteria (6 specific items):
  - [ ] Method loads data/player_data/adp_data.csv
  - [ ] Returns DataFrame with columns: Name, Position, ADP
  - [ ] Validates required columns exist
  - [ ] Handles file not found (raises DataProcessingError)
  - [ ] Handles empty file (raises DataProcessingError)
  - [ ] Logs successful load
- ✅ Has implementation location: PlayerManager.load_adp_data() (PlayerManager.py:~450)
- ✅ Has test coverage:
  - test_load_adp_data_success()
  - test_load_adp_data_file_not_found()
  - test_load_adp_data_empty_file()

### Task 4: Match player to ADP ranking
- ✅ Has acceptance criteria (5 specific items):
  - [ ] Creates dict: {(name, position): adp_value}
  - [ ] Matches player using (player.name, player.position)
  - [ ] Sets player.adp_value if match found
  - [ ] Uses None if no match (handled in Task 5)
  - [ ] Logs match success/failure
- ✅ Has implementation location: PlayerManager._match_player_to_adp() (PlayerManager.py:~480)
- ✅ Has test coverage:
  - test_match_player_success()
  - test_match_player_not_found()
  - test_match_player_case_insensitive()
  - test_match_player_multiple_positions()

[Continue for all 43 tasks...]

**Verification Summary:**
- Total TODO tasks: 43
- Tasks with acceptance criteria: 43
- Tasks with implementation location: 43
- Tasks with test coverage: 43
- Specificity: 100% ✅

**PART 2: ✅ PASS**

---
```

**Category-Specific Test Verification:**

If code processes multiple categories (positions, file types, data sources), verify tests for EACH:

```markdown
**Category-Specific Tests Verified:**

**Task 4: Match player to ADP ranking**
- Processes positions: QB, RB, WR, TE, K, DST
- Tests verified:
  - test_match_player_qb() ✅
  - test_match_player_rb() ✅
  - test_match_player_wr() ✅
  - test_match_player_te() ✅
  - test_match_player_k() ✅
  - test_match_player_dst() ✅
- All 6 positions covered ✅
```

**If PART 2 FAILS:**
- List tasks with missing criteria/location/tests
- Update tasks with specific acceptance criteria
- Re-run PART 2 until specificity = 100%

---

#### PART 3: Interface Contracts Audit

**Question:** Are all external interfaces verified against actual source code?

**Why this matters:** Assumed interfaces cause bugs → Must READ actual source code

**Process:**

1. List all external dependencies (classes/functions from other modules)

2. For EACH dependency:
   - ✅ Read actual source code (use Read tool)
   - ✅ Copy exact method signature
   - ✅ Verify parameter types
   - ✅ Verify return type
   - ✅ Document source location (file:line)

3. Count verification:
   - Total external dependencies: {N}
   - Dependencies verified from source: {M}
   - Verification: M/N × 100%
   - ✅ PASS if verification = 100%
   - ❌ FAIL if verification < 100%

**Example:**

```markdown
## PART 3: Interface Contracts Audit

**External Dependencies:**

### Dependency 1: ConfigManager.get_adp_multiplier

**Verification Steps:**
1. Read source: `Read league_helper/util/ConfigManager.py`
2. Found at: ConfigManager.py:234

**Actual Signature (copied from source):**
```python
def get_adp_multiplier(self, adp: int) -> Tuple[float, int]:
    """Returns (multiplier, rank) based on ADP value.

    Args:
        adp (int): ADP ranking value

    Returns:
        Tuple[float, int]: (multiplier, rank)
    """
```

**Interface Verification:**
- ✅ Method exists: ConfigManager.get_adp_multiplier
- ✅ Parameters: adp (int)
- ✅ Return type: Tuple[float, int]
- ✅ Used in: Task 6 (PlayerManager._calculate_adp_multiplier)
- ✅ TODO matches actual interface

---

### Dependency 2: csv_utils.read_csv_with_validation

**Verification Steps:**
1. Read source: `Read utils/csv_utils.py`
2. Found at: csv_utils.py:45

**Actual Signature (copied from source):**
```python
def read_csv_with_validation(
    filepath: Union[str, Path],
    required_columns: List[str],
    encoding: str = 'utf-8'
) -> pd.DataFrame:
    """Reads CSV and validates required columns exist."""
```

**Interface Verification:**
- ✅ Function exists: csv_utils.read_csv_with_validation
- ✅ Parameters: filepath, required_columns, encoding (optional)
- ✅ Return type: pd.DataFrame
- ✅ Used in: Task 1 (PlayerManager.load_adp_data)
- ✅ TODO calls with (filepath, required_columns) - valid

---

### Dependency 3: FantasyPlayer class

**Verification Steps:**
1. Read source: `Read league_helper/util/FantasyPlayer.py`
2. Found at: FantasyPlayer.py:15

**Actual Class Definition:**
```python
class FantasyPlayer:
    def __init__(self, name: str, position: str, score: float):
        self.name = name
        self.position = position
        self.score = score
        # ... other fields
```

**Interface Verification:**
- ✅ Class exists: FantasyPlayer
- ✅ Can add fields: adp_value, adp_rank, adp_multiplier (no conflicts)
- ✅ Has method: calculate_total_score() (line 85)
- ✅ Used in: Tasks 2, 3, 9
- ✅ TODO field additions are valid

---

[Continue for all 8 dependencies...]

**Verification Summary:**
- Total external dependencies: 8
- Dependencies verified from source: 8
- Verification: 100% ✅

**Dependencies Verified:**
1. ConfigManager.get_adp_multiplier ✅
2. csv_utils.read_csv_with_validation ✅
3. FantasyPlayer class ✅
4. error_handler.error_context ✅
5. error_handler.DataProcessingError ✅
6. LoggingManager.get_logger ✅
7. Path (from pathlib) ✅
8. pd.DataFrame (from pandas) ✅

**PART 3: ✅ PASS**

---
```

**If PART 3 FAILS:**
- List unverified dependencies
- Read actual source code for each
- Verify interfaces match TODO assumptions
- Fix mismatches
- Re-run PART 3 until verification = 100%

---

#### PART 4: Integration Evidence Audit

**Question:** Does every new method have an identified caller?

**Why this matters:** Methods without callers = orphan code → Integration failures

**Process:**

1. List all new methods/functions being created

2. For EACH method:
   - ✅ Identify caller (which method calls this)
   - ✅ Document call location (file:line)
   - ✅ Verify execution path from entry point

3. Count integration:
   - Total new methods: {N}
   - Methods with identified callers: {M}
   - Integration: M/N × 100%
   - ✅ PASS if integration = 100%
   - ❌ FAIL if integration < 100%

**Example:**

```markdown
## PART 4: Integration Evidence Audit

**New Methods:**

### Method 1: PlayerManager.load_adp_data()
- ✅ Caller: PlayerManager.load_players()
- ✅ Call location: PlayerManager.py:180
- ✅ Execution path:
  - run_league_helper.py → LeagueHelperManager → PlayerManager.load_players() → load_adp_data()
- ✅ Integration verified

---

### Method 2: PlayerManager._match_player_to_adp()
- ✅ Caller: PlayerManager.load_players()
- ✅ Call location: PlayerManager.py:210 (in player loop)
- ✅ Execution path:
  - load_players() → for player in players → _match_player_to_adp(player)
- ✅ Integration verified

---

### Method 3: PlayerManager._calculate_adp_multiplier()
- ✅ Caller: PlayerManager.load_players()
- ✅ Call location: PlayerManager.py:215
- ✅ Execution path:
  - load_players() → _calculate_adp_multiplier(player)
- ✅ Integration verified

---

### Method 4: ConfigManager.get_adp_multiplier()
- ✅ Caller: PlayerManager._calculate_adp_multiplier()
- ✅ Call location: PlayerManager.py:~505
- ✅ Execution path:
  - _calculate_adp_multiplier() → self.config.get_adp_multiplier(adp)
- ✅ Integration verified

---

[Continue for all 12 new methods...]

**Verification Summary:**
- Total new methods: 12
- Methods with identified callers: 12
- Integration: 100% ✅

**New Methods Verified:**
1. PlayerManager.load_adp_data() ✅
2. PlayerManager._match_player_to_adp() ✅
3. PlayerManager._calculate_adp_multiplier() ✅
4. ConfigManager.get_adp_multiplier() ✅
5. ConfigManager._validate_adp_config() ✅
6. PlayerManager._handle_duplicate_adp() ✅
7. PlayerManager._create_adp_dict() ✅
8. PlayerManager._normalize_player_name() ✅
9. FantasyPlayer._format_adp_data() ✅
10. PlayerManager._log_adp_match() ✅
11. PlayerManager._log_adp_miss() ✅
12. PlayerManager._get_default_multiplier() ✅

**PART 4: ✅ PASS**

---
```

**If PART 4 FAILS:**
- List methods without callers (orphans)
- Determine if needed (add caller) or unnecessary (remove from TODO)
- Re-run PART 4 until integration = 100%

---

## PART 5: Design Decision Scrutiny

**Objective:** Challenge all "for backward compatibility" or "fallback" design decisions

**Checklist:**

- [ ] **Identify all fallback mechanisms:**
  - Search spec.md for: "fallback", "backward compatibility", "default to", "if not available"
  - List all conditional logic that handles missing/incomplete data

- [ ] **For each fallback, ask:**
  - **Why is fallback needed?** (Old data? Partial data? Error recovery?)
  - **What happens when fallback is used?** (Degraded accuracy? Silent failure?)
  - **Can old and new data be compared?** (If yes, what's the comparison logic?)
  - **Could fallback hide bugs?** (Old data appearing valid when it's not)

- [ ] **Challenge the design:**
  - **Is fallback actually safer than failing fast?**
  - **Should incompatible data be rejected instead?**
  - **Does fallback create mixed-mode comparison problems?**

- [ ] **Document in spec.md:**
  ```markdown
  ## Design Decision: [Fallback Name]

  **Rationale:** [Why fallback is needed]
  **Behavior:** [What happens when triggered]
  **Risks:** [Potential issues with this design]
  **Mitigation:** [How risks are addressed]
  **Alternative Considered:** [Why we didn't fail fast / reject old data]
  ```

**Red Flags (require extra scrutiny):**

- ❌ Fallback allows comparing data WITH new metrics vs WITHOUT new metrics
- ❌ "Backward compatibility" mentioned but no version detection logic
- ❌ Missing fields handled silently (no logging/warning)
- ❌ Resume logic populates production data structures with old data

**Example:**

**Bad Design (can cause bugs):**
```python
# Fallback to MAE for backward compatibility
if self.overall_metrics and other.overall_metrics:
    return self.overall_metrics.pairwise_accuracy > other.overall_metrics.pairwise_accuracy
return self.mae < other.mae  # Problem: Allows invalid comparisons
```

**Better Design:**
```python
# Reject configs without metrics as invalid
if not self.overall_metrics:
    return False  # Cannot be "best"
if not other.overall_metrics:
    return True   # Replace invalid with valid
return self.overall_metrics.pairwise_accuracy > other.overall_metrics.pairwise_accuracy
```

**Success Criteria:**

- ✅ All fallback mechanisms identified and documented
- ✅ Each fallback has documented rationale, risks, and mitigation
- ✅ No fallback allows mixed-mode comparisons (old vs new data)
- ✅ Incompatible data is either migrated, rejected, or isolated (not mixed)

**PART 5: ✅ PASS** (if all criteria met)

---

#### Iteration 23a: Final Results

**If ALL 5 PARTS PASSED:**

```markdown
---

## ✅ Iteration 23a: Pre-Implementation Spec Audit - ALL 5 PARTS PASSED

**Audit Date:** {YYYY-MM-DD}

**PART 1 - Completeness:** ✅ PASS
- Requirements in spec.md: 15
- Requirements with TODO tasks: 15
- Coverage: 100%

**PART 2 - Specificity:** ✅ PASS
- Total TODO tasks: 43
- Tasks with acceptance criteria: 43
- Tasks with implementation location: 43
- Tasks with test coverage: 43
- Specificity: 100%

**PART 3 - Interface Contracts:** ✅ PASS
- External dependencies: 8
- Dependencies verified from source: 8
- Verification: 100%

**PART 4 - Integration Evidence:** ✅ PASS
- New methods: 12
- Methods with identified callers: 12
- Integration: 100%

**OVERALL RESULT: ✅ ALL 5 PARTS PASSED**

**Ready to proceed to Part 2b (Iteration 25 - Spec Validation).**

---
```

**If ANY part FAILED:**

```markdown
---

## ❌ Iteration 23a: Pre-Implementation Spec Audit - FAILED

**Audit Date:** {YYYY-MM-DD}

**PART 1 - Completeness:** ✅ PASS / ❌ FAIL
**PART 2 - Specificity:** ✅ PASS / ❌ FAIL
**PART 3 - Interface Contracts:** ✅ PASS / ❌ FAIL
**PART 4 - Integration Evidence:** ✅ PASS / ❌ FAIL

**Failing Parts:**
- [List parts that failed]

**Issues Found:**
- [List specific issues for each failing part]

**Actions Required:**
1. Fix issues in failing parts
2. Re-run Iteration 23a
3. ALL 5 PARTS must PASS before proceeding

**❌ STOP - Do NOT proceed to Part 2b until ALL 4 PARTS PASS**

---
```

**Update Agent Status:**

**If ALL 5 PARTS PASSED:**
```markdown
Progress: Iteration 23a PASSED (ALL 4 PARTS - MANDATORY GATE)
Gate Status: ✅ PASSED
Next Action: Read stages/stage_5/round3_part2b_gate_3.md for Part 2b
```

**If ANY part FAILED:**
```markdown
Progress: Iteration 23a FAILED - {X} parts failed
Gate Status: ❌ FAILED
Blockers: {List failing parts}
Next Action: Fix failing parts, re-run Iteration 23a
```

---

## Part 2a Completion Criteria

**Part 2a is COMPLETE when ALL of these are true:**

### Both Iterations Complete
- [ ] Iteration 23: Integration Gap Check (Final) complete
- [ ] Iteration 23a: Pre-Implementation Spec Audit - ALL 5 PARTS PASSED

### Mandatory Gate Passed
- [ ] Gate 2 (Iteration 23a): ALL 5 PARTS PASSED

### Documentation Updated
- [ ] todo.md contains all Part 2a outputs
- [ ] feature README.md Agent Status shows:
  - Iteration 23a: ALL 5 PARTS PASSED
  - Next Action: Read Part 2b guide

### Quality Verified
- [ ] No blockers
- [ ] All checklists 100% complete

**If ALL items checked:**
- Part 2a is COMPLETE
- Ready to proceed to Part 2b
- Read stages/stage_5/round3_part2b_gate_3.md

**If ANY item unchecked:**
- STOP - Do not proceed to Part 2b
- Complete missing items
- Re-verify completion criteria

---

## Common Mistakes to Avoid

### ❌ MISTAKE 1: "Iteration 23a Part 1 passed, I'll skip Parts 2-4"

**Why this is wrong:**
- ALL 5 PARTS must PASS (not just some)
- Each part catches different issues
- Skipping parts = incomplete validation

**What to do instead:**
- ✅ Execute ALL 4 PARTS of Iteration 23a
- ✅ Document results for each part
- ✅ Only proceed when ALL 5 PARTS PASSED

---

### ❌ MISTAKE 2: "I'll just check boxes without providing evidence"

**Why this is wrong:**
- Evidence is required for verification
- Cannot just say "15/15" without showing the 15 requirements
- Checkbox completion is not enough

**What to do instead:**
- ✅ Cite specific numbers (N requirements, M tasks)
- ✅ List examples of what was verified
- ✅ Provide evidence tables (as shown in examples)
- ✅ Show your work

---

## Prerequisites for Next Stage

**Before proceeding to Part 2b (round3_part2b_gate_3.md), verify:**

### Part 2a Completion
- [ ] BOTH iterations complete (23, 23a)
- [ ] Integration gap check: No orphan code
- [ ] Iteration 23a: ALL 5 PARTS PASSED

### Documentation
- [ ] feature README.md shows Part 2a complete
- [ ] Agent Status shows next action: "Read Part 2b guide"

**Only proceed to Part 2b when ALL items checked.**

**Next stage:** stages/stage_5/round3_part2b_gate_3.md

---

## Summary

**STAGE_5ac Part 2a - Gates 1-2 executes the first two critical gates:**

**Key Activities:**
1. **Integration Gap Check (Iteration 23):** Verify all methods have callers (no orphan code)
2. **Pre-Implementation Spec Audit (Iteration 23a - 4 PARTS):** Comprehensive audit of completeness, specificity, interfaces, integration

**Critical Outputs:**
- Integration verification (all methods integrated)
- Spec audit results (ALL 5 PARTS must PASS)

**Mandatory Gate:**
- Gate 2 (Iteration 23a): ALL 5 PARTS PASSED

**Success Criteria:**
- Both iterations complete
- Gate PASSED
- Ready for Part 2b

**Next Stage:** stages/stage_5/round3_part2b_gate_3.md - Spec validation and GO/NO-GO decision

**Remember:** Part 2a contains critical quality gates. Thoroughness here prevents implementation failures. Complete ALL iterations, pass ALL gates.

---

**END OF STAGE 5ac PART 2a GUIDE**
