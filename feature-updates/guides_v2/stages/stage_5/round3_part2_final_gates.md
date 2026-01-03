# STAGE 5ac Part 2: TODO Creation - Round 3 Final Gates (Iterations 23, 23a, 25, 24)

**Part of:** Epic-Driven Development Workflow v2
**Stage:** 5ac - TODO Creation Round 3
**Sub-Stage:** Part 2 - Final Gates & GO/NO-GO Decision
**Prerequisites:** STAGE_5ac_part1 complete (Iterations 17-22)
**Next Stage:** STAGE_5b_implementation_execution_guide.md

---

## 🚨 MANDATORY READING PROTOCOL

**CRITICAL:** You MUST read this ENTIRE guide before starting Part 2.

**Why this matters:**
- Part 2 contains 3 MANDATORY GATES that cannot be skipped
- Missing gates causes catastrophic implementation failures
- Iteration 25 prevents implementing wrong solution (Feature 02 bug)
- Iteration 24 is FINAL GO/NO-GO decision

**Reading Checkpoint:**
Before proceeding, you must have:
- [ ] Read this ENTIRE guide (use Read tool, not memory)
- [ ] Verified STAGE_5ac_part1 complete (Iterations 17-22)
- [ ] Verified all Part 1 outputs documented in todo.md
- [ ] Located spec.md, EPIC_TICKET.md, SPEC_SUMMARY.md files

**If resuming after session compaction:**
1. Check feature README.md "Agent Status" section for current iteration
2. Re-read this guide from the beginning
3. Continue from documented checkpoint

---

## Quick Start

### What is this sub-stage?

**STAGE_5ac Part 2 - Final Gates** is the second half of Round 3, where you execute final validation, comprehensive spec audits, validate against user-approved documents, and make the GO/NO-GO implementation decision through 4 critical iterations (23, 23a, 25, 24).

**This contains ALL 3 mandatory gates:**
- **Gate 1:** Iteration 23a - Pre-Implementation Spec Audit (4 PARTS)
- **Gate 2:** Iteration 25 - Spec Validation Against Validated Documents
- **Gate 3:** Iteration 24 - Implementation Readiness Protocol (GO/NO-GO)

### When do you use this guide?

**Use this guide when:**
- Part 1 (STAGE_5ac_part1) complete
- All preparation iterations (17-22) done
- Ready for mandatory gates

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

3. **Spec Validation Against Validated Documents** (Iteration 25 - CRITICAL GATE)
   - Spec.md verified against epic notes, epic ticket, spec summary
   - Discrepancies identified and resolved
   - Prevents Feature 02 catastrophic bug

4. **GO/NO-GO Decision** (Iteration 24 - FINAL GATE)
   - Implementation readiness assessed
   - Decision: GO or NO-GO
   - Cannot proceed to Stage 5b without GO

### Time estimate

**60-90 minutes** (4 iterations including 3 mandatory gates)
- Iteration 23: 10 minutes
- Iteration 23a: 20-30 minutes (4 PARTS - comprehensive)
- Iteration 25: 20-30 minutes (CRITICAL - spec validation)
- Iteration 24: 10 minutes (decision)

**If discrepancies found in Iteration 25:** +1-2 hours for user discussion and fixes

### Workflow overview

```
STAGE_5ac Part 2 Workflow (Iterations 23, 23a, 25, 24)
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
    [ALL 4 PARTS PASSED?]
         │
         ▼
┌─────────────────────────────────────────────────┐
│ Iteration 25: Spec Validation vs Validated Docs│
│ (CRITICAL GATE - Prevents wrong implementation)│
│ Validate spec.md against:                      │
│ - Epic notes                                   │
│ - Epic ticket (user-validated)                 │
│ - Spec summary (user-validated)                │
└─────────────────────────────────────────────────┘
         │
    [Zero discrepancies?]
    ├─ YES → Proceed to Iteration 24
    └─ NO → STOP, report to user, await decision
         │
         ▼
┌─────────────────────────────────────────────────┐
│ Iteration 24: Implementation Readiness Protocol│
│ (FINAL GATE - GO/NO-GO DECISION)               │
│ Assess: Confidence, Coverage, Gates            │
│ Decision: GO or NO-GO                          │
└─────────────────────────────────────────────────┘
         │
    [Decision = GO?]
    ├─ YES → Part 2 COMPLETE → Proceed to Stage 5b
    └─ NO → Fix blockers, re-run Iteration 24
```

---

## Critical Rules for Part 2

```
┌─────────────────────────────────────────────────────────────┐
│ CRITICAL RULES - Part 2 (Final Gates)                       │
└─────────────────────────────────────────────────────────────┘

1. ⚠️ ALL 4 iterations in Part 2 are MANDATORY (no skipping)
   - Iterations 23, 23a, 25, 24 are FINAL gates
   - Skipping gates causes catastrophic failures

2. ⚠️ Iteration 23a has 4 MANDATORY PARTS (ALL must PASS)
   - CANNOT proceed to Iteration 25 without "ALL 4 PARTS PASSED"
   - If ANY part fails → Fix and re-run Iteration 23a

3. ⚠️ Iteration 25 prevents implementing wrong solution (Feature 02 bug)
   - MUST validate spec.md against ALL validated sources
   - If discrepancies found → STOP and report to user
   - User decides: restart TODO OR fix and continue
   - CANNOT proceed to Iteration 24 without passing Iteration 25

4. ⚠️ Iteration 24 requires "GO" decision to proceed
   - Cannot proceed to Stage 5b without GO
   - If NO-GO → Fix blockers, re-run Iteration 24
   - GO requires: confidence >= MEDIUM, all gates passed

5. ⚠️ Close spec.md during Iteration 25 (avoid confirmation bias)
   - Re-read epic notes independently
   - Then compare spec to ALL validated sources
   - Ask critical questions (example vs special case)

6. ⚠️ Update feature README.md Agent Status after each mandatory gate
   - Document Iteration 23a result (ALL 4 PARTS status)
   - Document Iteration 25 result (PASSED / discrepancies found)
   - Document Iteration 24 decision (GO/NO-GO)

7. ⚠️ If user decision required (Iteration 25) → STOP and WAIT
   - Do NOT make autonomous decisions
   - Present 3 options (restart/fix/discuss)
   - Wait for user approval

8. ⚠️ Evidence required for verification
   - Cannot just check boxes
   - Must cite specific numbers (N requirements, M tasks, etc.)
   - Provide evidence of completion
```

---

## Prerequisites

**Before starting Part 2, verify ALL of these are true:**

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
- [ ] Epic notes file: feature-updates/{epic}/{epic}_notes.txt
- [ ] Epic ticket: feature-updates/{epic}/EPIC_TICKET.md
- [ ] Spec summary: feature-updates/{epic}/{feature}/SPEC_SUMMARY.md

### Quality State
- [ ] Confidence level >= MEDIUM (from Round 2)
- [ ] Test coverage >90%
- [ ] No blockers

**If ANY prerequisite not met:**
- STOP - Do not proceed with Part 2
- Return to Part 1 (STAGE_5ac_part1) to complete missing items
- Document blocker in Agent Status

---

## ROUND 3 PART 2: Final Gates & GO/NO-GO

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
Progress: Iteration 23/24 (Round 3 Part 2) complete
Integration Gap Check: 12/12 methods verified (no orphans)
Next Action: Iteration 23a - Pre-Implementation Spec Audit (MANDATORY - 4 PARTS)
```

---

### Iteration 23a: Pre-Implementation Spec Audit (MANDATORY GATE - 4 PARTS)

**Purpose:** Final comprehensive audit before implementation

**⚠️ MANDATORY:** ALL 4 PARTS must PASS before proceeding to Iteration 25

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

#### Iteration 23a: Final Results

**If ALL 4 PARTS PASSED:**

```markdown
---

## ✅ Iteration 23a: Pre-Implementation Spec Audit - ALL 4 PARTS PASSED

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

**OVERALL RESULT: ✅ ALL 4 PARTS PASSED**

**Ready to proceed to Iteration 25 (Spec Validation Against Validated Documents).**

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
3. ALL 4 PARTS must PASS before proceeding

**❌ STOP - Do NOT proceed to Iteration 25 until ALL 4 PARTS PASS**

---
```

**Update Agent Status:**

**If ALL 4 PARTS PASSED:**
```markdown
Progress: Iteration 23a PASSED (ALL 4 PARTS - MANDATORY GATE)
Gate Status: ✅ PASSED
Next Action: Iteration 25 - Spec Validation Against Validated Documents
```

**If ANY part FAILED:**
```markdown
Progress: Iteration 23a FAILED - {X} parts failed
Gate Status: ❌ FAILED
Blockers: {List failing parts}
Next Action: Fix failing parts, re-run Iteration 23a
```

---

### Iteration 25: Spec Validation Against Validated Documents (CRITICAL GATE)

**Purpose:** Verify spec.md matches ALL user-validated sources BEFORE implementing

**⚠️ CRITICAL GATE:** This iteration prevents Feature 02 catastrophic bug (implementing wrong solution)

**Sources of truth (all user-validated):**
1. **Epic notes** - user's original request (feature-updates/{epic}/{epic}_notes.txt)
2. **Epic ticket** - validated in Stage 1 (feature-updates/{epic}/EPIC_TICKET.md)
3. **Spec summary** - validated in Stage 2 (feature-updates/{epic}/{feature}/SPEC_SUMMARY.md)

**Historical Context (Feature 02 Catastrophic Bug):**
- Spec.md misinterpreted epic notes line 8
- Spec stated "JSON arrays automatically handle this, NO code changes needed"
- Epic actually required week_N+1 folder logic for ALL 18 weeks
- Wrong spec trusted through 24 iterations and 7 stages
- User caught it in final review → Massive rework required

**With new validation layers:**
- Epic ticket would have stated "All 18 weeks accessible and used correctly"
- Spec summary would have shown "week N+1 offset logic applies to ALL weeks"
- Iteration 25 three-way comparison would have caught misinterpretation

**This iteration prevents implementing wrong solution.**

---

#### Process:

**STEP 1: Close spec.md and TODO.md (avoid confirmation bias)**

**⚠️ CRITICAL:** Do NOT look at spec.md or TODO.md during Steps 1-3.

Why: Confirmation bias → You'll interpret epic notes to match what you already wrote in spec.

**Close these files:**
- spec.md
- todo.md

**Keep these files open:**
- Epic notes: feature-updates/{epic}/{epic}_notes.txt
- Epic ticket: feature-updates/{epic}/EPIC_TICKET.md
- Spec summary: feature-updates/{epic}/{feature}/SPEC_SUMMARY.md

---

**STEP 2: Re-read validated documents from scratch**

**Read EACH document word-for-word, as if seeing for first time:**

```markdown
## Epic Notes Re-Reading (Independent Analysis)

**Epic file:** feature-updates/integrate_new_player_data_into_simulation/integrate_new_player_data_into_simulation_notes.txt

**Line-by-line analysis:**

**Line 1:** "Update simulations to use JSON files instead of CSV"
- Literal meaning: Change file format from CSV to JSON
- Scope: Data loading changes required
- Implementation: Read JSON instead of CSV

**Lines 3-6:** "Load JSON from simulation/sim_data/YYYY/weeks/week_NN/ folders"
- Literal meaning: Week-based folder structure exists
- Scope: File path construction changes required
- Implementation: Build paths like "simulation/sim_data/2021/weeks/week_01/"

**Line 8:** "use week_17 folders for projected_points, then look at actual_points array in week_18 folders"
- Literal meaning: Week 17 uses TWO folders (week_17 for projected, week_18 for actual)
- **CRITICAL QUESTION:** Is week 17 special, or is this an EXAMPLE of a pattern?
- **Need evidence:** Check if pattern applies to ALL weeks or just week 17
- **Hypothesis 1:** Week 17 is special case (only week 17 needs week 18)
- **Hypothesis 2:** Week 17 is EXAMPLE of pattern (week N needs week N+1 for ALL weeks)

**Question to resolve:** Which hypothesis is correct?
- Evidence needed: Manual inspection of week_01, week_02 JSON files
- Check: Does week_01 have actual_points[0] = 0.0? (would mean week_01 needs week_02)

[Continue for ALL lines in epic notes...]

---

## Epic Ticket Re-Reading

**File:** feature-updates/integrate_new_player_data_into_simulation/EPIC_TICKET.md

**Acceptance Criteria section:**
- "All 18 weeks of data are accessible and used correctly"
- **Key insight:** Says "ALL 18 weeks" (not "weeks 17-18")
- **Implication:** Pattern applies to ALL weeks, not just 17

---

## Spec Summary Re-Reading

**File:** feature-updates/integrate_new_player_data_into_simulation/feature_01_win_rate_sim_json_integration/SPEC_SUMMARY.md

**Technical Changes section:**
- "Week offset logic: week N loads projected from week_N folder, actual from week_N+1 folder"
- **Key insight:** Explicitly states "week N" and "week N+1" (pattern, not special case)
- **Implication:** All weeks follow week_N+1 pattern

---
```

---

**STEP 3: Ask critical questions about epic interpretation**

**For EACH epic requirement, ask:**

- [ ] Is this an EXAMPLE of a general pattern, or a SPECIAL CASE?
- [ ] What is the LITERAL meaning vs my interpretation?
- [ ] What evidence would prove/disprove my interpretation?
- [ ] Did I make assumptions, or verify with code/data?

**Example (Feature 02 Analysis):**

```markdown
## Critical Questions - Epic Line 8 Analysis

**Epic line 8:** "use week_17 folders for projected_points, then look at actual_points array in week_18 folders"

**Question 1:** Is week 17 special, or is this an example?
- **Original spec interpretation:** Week 17 is special case ❌ WRONG
- **Correct interpretation:** Week 17 is EXAMPLE of pattern ALL weeks follow ✅
- **Evidence:** Epic ticket says "ALL 18 weeks", spec summary says "week N+1" pattern

**Question 2:** Why would week 17 need week 18 folder?
- **Original spec assumption:** "JSON arrays handle this automatically" ❌ WRONG
- **Correct answer:** week_N folder has actual_points[N-1] = 0.0 (week not complete yet)
- **Evidence:** Should have manually inspected week_01, week_02 JSON files
  - week_01/players.json: actual_points[0] = 0.0 (week 1 not complete in week 1)
  - week_02/players.json: actual_points[0] = 33.6 (week 1 complete in week 2)

**Question 3:** Does this pattern apply to other weeks?
- **Original spec says:** Not mentioned (assumed no) ❌ WRONG
- **Reality:** YES - week_01 needs week_02, week_02 needs week_03, etc. ✅
- **Evidence:**
  - Epic ticket: "ALL 18 weeks" (not just 17)
  - Spec summary: "week N+1 offset applies to ALL weeks"
  - Manual data inspection confirms pattern

**Conclusion:** Spec.md interpreted epic line as "week 17 special case" when it was actually an EXAMPLE of "week N+1 pattern for ALL weeks"

---
```

---

**STEP 4: Compare epic notes/ticket/summary with spec.md**

**NOW open spec.md and compare EACH claim against ALL THREE validated sources:**

```markdown
## Three-Way Comparison: Epic Notes + Epic Ticket + Spec Summary vs Spec.md

### Requirement 1: Week folder logic

**Epic notes say (line 8):**
> "use week_17 folders for projected_points, then look at actual_points array in week_18 folders"

**Epic ticket says (Acceptance Criteria):**
> "All 18 weeks of data are accessible and used correctly"

**Spec summary says (Technical Changes):**
> "Week offset logic: week N loads projected from week_N folder, actual from week_N+1 folder"

**Spec.md says (Section: "Week 17/18 Logic Clarification"):**
> "JSON arrays already handle this. NO special handling needed. No code changes required."

**Match?** ❌ NO - Major discrepancy

**Discrepancy Analysis:**
- Epic notes: Shows week_17 → week_18 pattern (example, not special case)
- Epic ticket: Explicitly states "ALL 18 weeks" (not just 17/18)
- Spec summary: Correctly interprets as "week N+1 offset for ALL weeks"
- Spec.md: CONTRADICTS summary - says "NO special handling" and "No code changes"

**Which sources are user-validated?**
- Epic ticket: ✅ User-validated in Stage 1
- Spec summary: ✅ User-validated in Stage 2
- Spec.md: ❌ NOT validated yet

**Conclusion:** Spec.md is WRONG (contradicts TWO user-validated sources)

**Evidence spec.md is wrong:**
- Manual data inspection: week_01 has actual_points[0] = 0.0, week_02 has actual_points[0] = 33.6
- Pattern applies to ALL weeks, not just 17
- User approved spec summary with "week N+1 offset applies to ALL weeks"
- Code changes ARE required to load week_N+1 for actuals

**Impact:** Spec.md conclusion is catastrophically WRONG
- Spec says "no code changes" when week_N+1 logic required for ALL weeks
- If implemented as spec states → All actuals would be 0.0 → Feature fails completely

---

### Requirement 2: Data structure

**Epic notes say (lines 10-15):**
> [Quote from epic notes]

**Epic ticket says:**
> [Quote from acceptance criteria]

**Spec summary says:**
> [Quote from technical changes]

**Spec.md says:**
> [Quote from spec]

**Match?** ✅ YES / ❌ NO

**Analysis:**
- [Are all four sources aligned?]
- [If not aligned, which are user-validated?]
- [Spec.md is correct/wrong because...]

[Continue for ALL requirements...]

---
```

**Critical insight:** If spec.md contradicts VALIDATED documents (epic ticket or spec summary), spec.md is WRONG.

Epic ticket and spec summary were approved by user → They are source of truth.

---

**STEP 5: Document ALL discrepancies (even minor)**

```markdown
## Spec Discrepancies Found

### Discrepancy 1: Week offset logic

**Epic notes say (line 8):**
> "use week_17 folders for projected_points, then look at actual_points array in week_18 folders"

**Epic ticket says (Acceptance Criteria):**
> "All 18 weeks of data are accessible and used correctly"

**Spec summary says (Technical Changes):**
> "Week offset logic: week N loads projected from week_N folder, actual from week_N+1 folder"

**Spec.md says (Section "Week 17/18 Logic"):**
> "JSON arrays already handle this. NO special handling needed. No code changes required."

**Why spec.md is wrong:**
- Epic notes show week_N + week_N+1 pattern (week_17 → week_18 is example, not special case)
- Epic ticket explicitly states "ALL 18 weeks" (not just 17/18)
- Spec summary correctly interprets as "week N+1 offset" pattern for ALL weeks
- Spec.md contradicts BOTH validated documents (epic ticket + spec summary)
- Spec.md concluded "no code changes" when pattern requires week_N+1 logic for ALL weeks

**Evidence spec.md is wrong:**
- Manual data inspection: week_01 has actual_points[0] = 0.0, week_02 has actual_points[0] = 33.6
- Pattern confirmed: week_01 needs week_02, week_02 needs week_03, etc.
- User approved spec summary with "week N+1 offset applies to ALL weeks"
- Code changes ARE required to implement week_N+1 folder loading

**Impact on TODO:**
- TODO currently missing tasks for week_N+1 folder loading
- TODO missing tasks for dual folder logic (projected from week_N, actual from week_N+1)
- If implemented as-is: All actuals would be 0.0 → Feature completely non-functional

**Severity:** 🔴 CRITICAL - Feature would fail completely

---

### Discrepancy 2: [Name if any]

[Document ALL additional discrepancies]

---
```

---

**STEP 6: IF ANY DISCREPANCIES FOUND → STOP and report to user**

**🛑 STOP IMMEDIATELY - Do NOT proceed to Iteration 24**

**Report to user:**

```markdown
## ⚠️ ITERATION 25 FAILED - Spec Misalignment with Validated Documents

**User Decision Required**

I completed Iteration 25 (Spec Validation Against Validated Documents) and found discrepancies between spec.md and the user-validated sources (epic notes, epic ticket, spec summary).

**Discrepancies Found:** [X]

---

### Discrepancy 1: [Name]

**Epic notes say:**
> [Quote from epic notes with line number]

**Epic ticket says:**
> [Quote from epic ticket - acceptance criteria]

**Spec summary says:**
> [Quote from spec summary - technical changes]

**Spec.md says:**
> [Quote from spec.md with section reference]

**Why spec.md is wrong:**
- [Explain which validated sources align]
- [Explain why spec.md contradicts them]
- [Evidence from code/data inspection]

**Impact if we implement current TODO:**
- [What would happen - be specific]
- [Which TODO tasks are affected]

**Severity:** 🔴 CRITICAL / 🟡 MODERATE / 🟢 MINOR

---

[Repeat for each discrepancy]

---

### How Would You Like to Proceed?

**Option A (Recommended): Fix spec, restart TODO iterations**

**Steps:**
1. Update spec.md to match epic requirements
2. Restart Stage 5a from Iteration 1 (regenerate TODO from correct spec)
3. Re-run all 25 iterations with corrected spec
4. Ensures TODO matches actual epic intent

**Rationale:** Current TODO is based on wrong spec. Starting fresh with correct spec is safer than trying to patch TODO.

**Time:** ~4-6 hours to re-run Stage 5a with correct spec

---

**Option B: Fix spec and TODO manually, continue to implementation**

**Steps:**
1. Update spec.md to match epic requirements
2. Manually update TODO.md tasks to reflect correct spec
3. Continue to Iteration 24 (Implementation Readiness)

**Rationale:** Faster than Option A, but riskier (may miss subtle dependencies from wrong spec)

**Time:** ~1-2 hours to fix spec and TODO

**Risk:** TODO may still have subtle errors from being based on wrong spec initially

---

**Option C: Discuss discrepancies first**

**Steps:**
1. Review each discrepancy together
2. Clarify epic intent
3. Decide on spec updates
4. Then choose Option A or B

**Rationale:** Best if epic requirements are ambiguous or discrepancies are unclear

**Time:** ~30 minutes discussion + Option A or B time

---

**My Recommendation:** Option A (restart TODO iterations)

**Reason:** [X] discrepancies found, including [Y] CRITICAL severity. Current TODO is based on fundamentally wrong understanding of epic requirements. Restarting with correct spec prevents implementing wrong solution that would require massive rework after user testing.

**Cost:** 4-6 hours to re-run Stage 5a
**Benefit:** Prevents implementing completely wrong feature → Saves days/weeks of rework

---

**Question for user:** Which option do you prefer?

**IMPORTANT: I will NOT proceed to Iteration 24 or Stage 5b until you decide and spec is corrected.**

---
```

**Wait for user decision - DO NOT make this choice autonomously.**

---

**STEP 7: Execute user's choice**

**If user chooses Option A (restart TODO iterations):**

```markdown
## User Decision: Restart TODO Iterations

**Actions:**
1. Update spec.md based on epic re-validation findings
2. Document spec changes in spec.md changelog section
3. Archive current TODO.md as TODO_ARCHIVE_{date}.md
4. Return to Stage 5aa Iteration 1
5. Re-run all iterations (1-25) with corrected spec
6. Mark Iteration 25 status: "SPEC FIXED - Restarting TODO creation"

**Next Action:** Read STAGE_5aa_round1_guide.md to restart TODO creation

---
```

**If user chooses Option B (fix and continue):**

```markdown
## User Decision: Fix Spec and TODO, Continue

**Actions:**
1. Update spec.md based on epic re-validation findings
2. Manually update TODO.md to fix affected tasks
3. Review TODO for any missed implications of spec changes
4. Document risk in TODO.md: "RISK: Spec corrected in Iteration 25, TODO updated manually (not regenerated)"
5. Proceed to Iteration 24 (Implementation Readiness)
6. Mark Iteration 25 status: "SPEC FIXED - TODO patched manually, continuing"

**Next Action:** Continue to Iteration 24 (with caution)

---
```

**If user chooses Option C (discuss first):**

```markdown
## User Decision: Discuss Discrepancies

**Actions:**
1. Have conversation about each discrepancy
2. Get user clarification on epic intent
3. Update spec.md based on clarifications
4. Return to this step and choose Option A or B
5. Mark Iteration 25 status: "Discussing discrepancies with user"

**Next Action:** Discuss discrepancies with user

---
```

---

**STEP 8: IF ZERO DISCREPANCIES → Document validation**

**If spec.md matches ALL validated sources perfectly:**

```markdown
---

## ✅ Iteration 25: Spec Validation Against Validated Documents - PASSED

**Validation Date:** {YYYY-MM-DD}

**Validated sources verified:**
- Epic notes: feature-updates/{epic}/{epic}_notes.txt
- Epic ticket: feature-updates/{epic}/EPIC_TICKET.md
- Spec summary: feature-updates/{epic}/{feature}/SPEC_SUMMARY.md

**Requirements verified:** {N} (all requirements compared across all sources)

**Discrepancies found:** 0 ✅

**Spec alignment:** 100% with ALL three validated sources

**Validation method:**
1. Closed spec.md before re-reading epic (avoided confirmation bias)
2. Re-read epic notes word-for-word independently
3. Re-read epic ticket (user-validated outcomes from Stage 1)
4. Re-read spec summary (user-validated feature outcomes from Stage 2)
5. Compared each requirement across all FOUR documents
6. Asked critical questions (example vs special case, literal vs interpreted)
7. Verified with code/data inspection where applicable

**Critical findings:**
- ✅ All spec.md claims align with epic notes
- ✅ All spec.md claims align with epic ticket acceptance criteria
- ✅ All spec.md claims align with spec summary technical changes
- ✅ All interpretations verified with evidence (no assumptions)
- ✅ No discrepancies between spec.md and any validated source

**Example verifications performed:**
- Epic line 8 "week_17 → week_18": Verified as pattern (not special case) via epic ticket "ALL 18 weeks"
- Epic line 5 "JSON format": Verified actual JSON structure by inspecting sample files
- Epic line 10 "projected vs actual": Verified distinction exists in JSON arrays

**RESULT: ✅ Spec.md is correct and aligned with ALL validated sources**

**Confidence:** HIGH - Safe to proceed to implementation

**Ready to proceed to Iteration 24 (Implementation Readiness Protocol).**

---
```

---

**Critical Question Checklist:**

Before marking Iteration 25 complete, answer these:

**Epic Interpretation:**
- [ ] Did I close spec.md before re-reading epic notes? (avoid confirmation bias)
- [ ] Did I read epic notes word-for-word (not skimming)?
- [ ] For each epic line, did I ask: "Is this EXAMPLE or SPECIAL CASE?"
- [ ] Did I distinguish between LITERAL meaning vs my INTERPRETATION?

**Spec Alignment:**
- [ ] Did I compare EVERY spec requirement with epic notes + epic ticket + spec summary?
- [ ] Did I document ALL discrepancies (even minor ones)?
- [ ] For each discrepancy, did I identify which sources are user-validated?
- [ ] Did I assess severity (CRITICAL/MODERATE/MINOR)?

**Assumption Detection:**
- [ ] Did I make assumptions, or verify with evidence?
- [ ] Can I trace every spec claim to epic/ticket/summary OR code inspection?
- [ ] If spec says "automatically handles", did I verify with data inspection?
- [ ] If spec interprets epic line as "special case", did I check if it's a pattern?

**Feature 02 Prevention:**
- [ ] Did I check if patterns (week-based logic, etc.) apply to ALL cases or just one?
- [ ] Did I manually inspect data files mentioned in epic?
- [ ] If epic shows example (week_17 → week_18), did I check if pattern generalizes?
- [ ] Did I avoid saying "automatically handles" without verifying?

**User Reporting (if discrepancies):**
- [ ] If ANY discrepancies found → STOPPED and reported to user?
- [ ] Did I provide 3 options (restart/fix/discuss)?
- [ ] Did I recommend an option with clear rationale?
- [ ] Am I WAITING for user decision (not proceeding autonomously)?

**Validation Confidence (if zero discrepancies):**
- [ ] Can I confidently say spec is correct and matches ALL validated sources?
- [ ] Would I stake feature success on spec accuracy?
- [ ] If I had to bet money, would I bet spec matches epic intent perfectly?

---

**Update Agent Status:**

**If discrepancies found:**
```markdown
Progress: Iteration 25 FAILED - [X] spec discrepancies found
Gate Status: ❌ BLOCKED
Blockers: Spec/epic misalignment - awaiting user decision
Next Action: WAITING FOR USER - Cannot proceed until spec corrected
```

**If zero discrepancies:**
```markdown
Progress: Iteration 25 PASSED - Spec verified against all validated sources
Gate Status: ✅ PASSED
Next Action: Iteration 24 - Implementation Readiness Protocol (FINAL GATE)
```

---

**Why This Iteration Matters:**

**Feature 02 Example:**
- **Without Iteration 25:** Wrong spec trusted → wrong TODO (missing week_N+1 logic) → wrong implementation (all actuals = 0.0) → user caught in final review → massive rework
- **With Iteration 25:** Spec re-validated against epic ticket + spec summary → discrepancy found → spec corrected → TODO regenerated → correct implementation

**Prevention:** Catches spec interpretation errors BEFORE implementing wrong solution

**Cost:** 20-30 minutes to re-read epic and validate spec
**Benefit:** Prevents days/weeks of implementing wrong feature + rework

---

### Iteration 24: Implementation Readiness Protocol (FINAL GATE)

**Purpose:** Final go/no-go decision before implementation

**⚠️ FINAL GATE:** Cannot proceed to Stage 5b without "GO" decision

**Why this matters:** Last checkpoint to verify everything is ready → GO decision means implementation will succeed

---

#### Process:

**STEP 1: Final readiness checklist**

```markdown
## Implementation Readiness Checklist

**Spec Verification:**
- [x] spec.md complete (no TBD sections)
- [x] All algorithms documented
- [x] All edge cases defined
- [x] All dependencies identified
- [x] Spec validated against epic notes/ticket/summary (Iteration 25 PASSED)

**TODO Verification:**
- [x] TODO file created: todo.md
- [x] All requirements have tasks
- [x] All tasks have acceptance criteria
- [x] Implementation locations specified
- [x] Test coverage defined
- [x] Implementation phasing defined (Iteration 17)
- [x] Rollback strategy defined (Iteration 18)

**Iteration Completion:**
- [x] All 25 iterations complete (Rounds 1, 2, 3)
- [x] Round 1: Iterations 1-7 + 4a complete
- [x] Round 2: Iterations 8-16 complete
- [x] Round 3 Part 1: Iterations 17-22 complete
- [x] Round 3 Part 2: Iterations 23, 23a, 25, 24 in progress
- [x] No iterations skipped

**Mandatory Gates:**
- [x] Iteration 4a PASSED (TODO Specification Audit)
- [x] Iteration 23a PASSED (ALL 4 PARTS - Pre-Implementation Spec Audit)
- [x] Iteration 25 PASSED (Spec Validation - zero discrepancies)

**Confidence Assessment:**
- [x] Confidence level: HIGH / MEDIUM (must be >= MEDIUM)
- [x] All questions resolved (or documented in questions.md)
- [x] No critical unknowns
- [x] Comfortable with implementation scope

**Integration Verification:**
- [x] Algorithm Traceability Matrix complete (47 mappings typical)
- [x] Integration Gap Check complete (no orphan code - all methods have callers)
- [x] Interface Verification complete (all dependencies verified from source)
- [x] Mock Audit complete (mocks match real interfaces)

**Quality Gates:**
- [x] Test coverage: >90%
- [x] Performance impact: Acceptable (<+20% regression)
- [x] Rollback strategy: Defined
- [x] Documentation plan: Complete
- [x] All mandatory audits PASSED
- [x] No blockers

**DECISION:** ✅ GO / ❌ NO-GO

---
```

---

**STEP 2: Make go/no-go decision**

**✅ GO if:**
- All checklist items checked ✅
- Confidence >= MEDIUM
- All 3 mandatory gates PASSED:
  - Iteration 4a: PASSED
  - Iteration 23a: ALL 4 PARTS PASSED
  - Iteration 25: PASSED (zero discrepancies)
- No blockers
- Ready to implement

**❌ NO-GO if:**
- Any checklist item unchecked
- Confidence < MEDIUM
- Any mandatory gate FAILED
- Any critical blocker exists
- Uncertainty about implementation

---

**STEP 3: Document decision**

**If GO:**

```markdown
---

## ✅ Iteration 24: Implementation Readiness - GO DECISION

**Date:** {YYYY-MM-DD}
**Confidence:** HIGH / MEDIUM
**Iterations Complete:** 25/25 (all rounds complete)

**Mandatory Audits:**
- Iteration 4a (Round 1): ✅ PASSED
- Iteration 23a (Round 3): ✅ ALL 4 PARTS PASSED
- Iteration 25 (Round 3): ✅ PASSED (spec verified against epic notes/ticket/summary - zero discrepancies)

**Quality Metrics:**
- Algorithm mappings: 47
- Integration verification: 12/12 methods have callers
- Interface verification: 8/8 dependencies verified from source
- Test coverage: 95%
- Performance impact: +0.2s (acceptable)

**Preparation Complete:**
- Implementation phasing: 5 phases defined
- Rollback strategy: Config toggle + git revert documented
- Mock audit: All mocks verified, 3 integration tests planned
- Consumer validation: 3 consumers verified

**DECISION: ✅ READY FOR IMPLEMENTATION**

**Next Stage:** Stage 5b (Implementation Execution)

**Proceed using:** STAGE_5b_implementation_execution_guide.md

**Reminder:** Keep spec.md VISIBLE during implementation, use Algorithm Traceability Matrix as guide, run tests after EVERY phase.

---
```

**If NO-GO:**

```markdown
---

## ❌ Iteration 24: Implementation Readiness - NO-GO DECISION

**Date:** {YYYY-MM-DD}
**Confidence:** LOW
**Blockers:** {X}

**Mandatory Audits:**
- Iteration 4a: ✅ PASSED / ❌ FAILED
- Iteration 23a: ✅ ALL 4 PARTS PASSED / ❌ {X} PARTS FAILED
- Iteration 25: ✅ PASSED / ❌ FAILED (discrepancies found)

**Blockers Found:**
1. {Blocker 1 description}
   - Impact: {HIGH/MEDIUM/LOW}
   - Fix: {What needs to be done}

2. {Blocker 2 description}
   - Impact: {HIGH/MEDIUM/LOW}
   - Fix: {What needs to be done}

**DECISION: ❌ NOT READY FOR IMPLEMENTATION**

**Next Actions:**
1. Fix blocker 1: {specific action}
2. Fix blocker 2: {specific action}
3. Re-run affected iterations if needed
4. Re-run Iteration 24 after fixes
5. Must achieve GO decision before proceeding

**Do NOT proceed to Stage 5b until GO decision achieved.**

---
```

---

**Update Agent Status:**

**If GO:**
```markdown
## Agent Status

**Last Updated:** {YYYY-MM-DD HH:MM}
**Current Phase:** IMPLEMENTATION (ready to start)
**Current Step:** Round 3 complete (25/25 total iterations)
**Current Guide:** STAGE_5ac_part2_final_gates_guide.md (COMPLETE)
**Guide Last Read:** {YYYY-MM-DD HH:MM}

**Progress:** All 25 iterations complete ✅

**Mandatory Gates:**
- Iteration 4a: ✅ PASSED
- Iteration 23a: ✅ ALL 4 PARTS PASSED
- Iteration 25: ✅ PASSED (zero discrepancies)
- Iteration 24 Decision: ✅ GO

**Confidence Level:** {HIGH / MEDIUM}
**Next Stage:** Stage 5b (Implementation Execution)
**Next Action:** Read STAGE_5b_implementation_execution_guide.md
**Blockers:** None
```

**If NO-GO:**
```markdown
## Agent Status

**Last Updated:** {YYYY-MM-DD HH:MM}
**Current Phase:** TODO_CREATION
**Current Step:** Round 3 - Iteration 24 (NO-GO)
**Current Guide:** STAGE_5ac_part2_final_gates_guide.md
**Guide Last Read:** {YYYY-MM-DD HH:MM}

**Progress:** Iteration 24 returned NO-GO decision

**Mandatory Gates:**
- Iteration 4a: {Status}
- Iteration 23a: {Status}
- Iteration 25: {Status}
- Iteration 24 Decision: ❌ NO-GO

**Confidence Level:** {LOW / MEDIUM}
**Blockers:** {List blockers}
**Next Action:** Fix blockers, re-run Iteration 24
```

---

## Part 2 Completion Criteria

**Part 2 (and Round 3) is COMPLETE when ALL of these are true:**

### All 4 Iterations Complete
- [ ] Iteration 23: Integration Gap Check (Final) complete
- [ ] Iteration 23a: Pre-Implementation Spec Audit - ALL 4 PARTS PASSED
- [ ] Iteration 25: Spec Validation - PASSED (zero discrepancies)
- [ ] Iteration 24: Implementation Readiness - GO DECISION

### Mandatory Gates Passed
- [ ] Gate 1 (Iteration 23a): ALL 4 PARTS PASSED
- [ ] Gate 2 (Iteration 25): Spec verified against all validated sources (zero discrepancies)
- [ ] Gate 3 (Iteration 24): GO decision

### Documentation Updated
- [ ] todo.md contains all Part 2 outputs
- [ ] feature README.md Agent Status shows:
  - Iteration 23a: ALL 4 PARTS PASSED
  - Iteration 25: PASSED (zero discrepancies)
  - Iteration 24: GO
  - Phase: IMPLEMENTATION
  - Next Action: Read Stage 5b guide

### Quality Verified
- [ ] Confidence level >= MEDIUM
- [ ] No blockers
- [ ] All checklists 100% complete

**If ALL items checked:**
- Part 2 is COMPLETE
- Round 3 is COMPLETE
- Stage 5a is COMPLETE
- Ready to proceed to Stage 5b (Implementation)
- Read STAGE_5b_implementation_execution_guide.md

**If ANY item unchecked:**
- STOP - Do not proceed to Stage 5b
- Complete missing items
- Re-verify completion criteria

---

## Common Mistakes to Avoid

### ❌ MISTAKE 1: "Iteration 23a Part 1 passed, I'll skip Parts 2-4"

**Why this is wrong:**
- ALL 4 PARTS must PASS (not just some)
- Each part catches different issues
- Skipping parts = incomplete validation

**What to do instead:**
- ✅ Execute ALL 4 PARTS of Iteration 23a
- ✅ Document results for each part
- ✅ Only proceed when ALL 4 PARTS PASSED

---

### ❌ MISTAKE 2: "I'll skip Iteration 25, spec looks fine"

**Why this is wrong:**
- Iteration 25 prevents Feature 02 catastrophic bug
- Spec can be wrong even if it "looks fine"
- Three-way validation catches interpretation errors

**What to do instead:**
- ✅ ALWAYS execute Iteration 25
- ✅ Close spec.md before re-reading epic
- ✅ Compare spec to ALL validated sources
- ✅ Ask critical questions

---

### ❌ MISTAKE 3: "Spec has minor discrepancy, I'll ignore it"

**Why this is wrong:**
- "Minor" discrepancies often indicate larger misunderstandings
- User-validated sources (epic ticket, spec summary) are truth
- Ignoring discrepancies = implementing wrong solution

**What to do instead:**
- ✅ Document ALL discrepancies (even minor)
- ✅ Report to user with 3 options
- ✅ WAIT for user decision
- ✅ Do NOT proceed autonomously

---

### ❌ MISTAKE 4: "Confidence is LOW but I'll mark GO anyway"

**Why this is wrong:**
- GO requires confidence >= MEDIUM
- LOW confidence = missing information or unclear requirements
- Implementing with LOW confidence = failures during implementation

**What to do instead:**
- ✅ Mark NO-GO if confidence < MEDIUM
- ✅ Identify what's causing low confidence
- ✅ Fix confidence issues (ask user, research more, etc.)
- ✅ Only mark GO when confidence >= MEDIUM

---

### ❌ MISTAKE 5: "I'll proceed to Stage 5b with NO-GO decision"

**Why this is wrong:**
- NO-GO means NOT READY for implementation
- Blockers exist that will cause implementation failures
- Cannot skip fixing blockers

**What to do instead:**
- ✅ If NO-GO → Fix ALL blockers
- ✅ Re-run affected iterations
- ✅ Re-run Iteration 24 until GO achieved
- ✅ Only proceed to Stage 5b with GO decision

---

## Prerequisites for Next Stage

**Before proceeding to Stage 5b (Implementation Execution), verify:**

### Part 2 Completion
- [ ] ALL 4 iterations complete (23, 23a, 25, 24)
- [ ] Integration gap check: No orphan code
- [ ] Iteration 23a: ALL 4 PARTS PASSED
- [ ] Iteration 25: PASSED (zero discrepancies)
- [ ] Iteration 24: GO DECISION

### Overall Stage 5a Completion
- [ ] All 25 iterations complete (Rounds 1, 2, 3)
- [ ] All mandatory gates PASSED:
  - Iteration 4a: PASSED
  - Iteration 23a: ALL 4 PARTS PASSED
  - Iteration 25: PASSED
  - Iteration 24: GO
- [ ] todo.md complete with all outputs from all rounds
- [ ] Confidence >= MEDIUM
- [ ] No blockers

### Documentation
- [ ] feature README.md shows Stage 5a complete
- [ ] Agent Status shows next action: "Read Stage 5b guide"

**Only proceed to Stage 5b when ALL items checked.**

**Next stage:** STAGE_5b_implementation_execution_guide.md

---

## Summary

**STAGE_5ac Part 2 - Final Gates & GO/NO-GO executes the most critical validations:**

**Key Activities:**
1. **Integration Gap Check (Iteration 23):** Verify all methods have callers (no orphan code)
2. **Pre-Implementation Spec Audit (Iteration 23a - 4 PARTS):** Comprehensive audit of completeness, specificity, interfaces, integration
3. **Spec Validation (Iteration 25 - CRITICAL):** Validate spec against ALL user-approved sources (prevents Feature 02 bug)
4. **Implementation Readiness (Iteration 24 - GO/NO-GO):** Final decision to proceed or fix blockers

**Critical Outputs:**
- Integration verification (all methods integrated)
- Spec audit results (ALL 4 PARTS must PASS)
- Spec validation (zero discrepancies with validated sources)
- GO/NO-GO decision (must be GO to proceed)

**Mandatory Gates (ALL must PASS):**
- Gate 1 (Iteration 23a): ALL 4 PARTS PASSED
- Gate 2 (Iteration 25): Zero discrepancies
- Gate 3 (Iteration 24): GO decision

**Success Criteria:**
- All 4 iterations complete
- All 3 gates PASSED
- Confidence >= MEDIUM
- Ready for implementation

**Next Stage:** STAGE_5b_implementation_execution_guide.md - Implement TODO tasks with continuous verification

**Remember:** Part 2 contains the FINAL quality gates before implementation. Thoroughness here prevents catastrophic implementation failures. Trust the process - complete ALL iterations, pass ALL gates.

---

**END OF STAGE 5ac PART 2 GUIDE**
