# STAGE 6c: Epic Final Review Guide

**Part of:** Epic-Driven Development Workflow v2
**Stage:** 6 - Epic-Level Final QC
**Sub-Stage:** 6c - Epic Final Review (Steps 6-8)
**Prerequisites:** STAGE_6b complete (all 3 QC rounds passed)
**Next Stage:** STAGE_7_epic_cleanup_guide.md

---

## 🚨 MANDATORY READING PROTOCOL

**CRITICAL:** You MUST read this ENTIRE guide before starting Stage 6c work.

**Why this matters:**
- Stage 6c is the FINAL VALIDATION before epic completion
- Missing steps here means shipping incomplete or incorrect epic
- Thoroughness prevents post-completion issues

**Reading Checkpoint:**
Before proceeding, you must have:
- [ ] Read this ENTIRE guide (use Read tool, not memory)
- [ ] Verified STAGE_6b complete (all 3 QC rounds passed)
- [ ] Verified no pending issues or bug fixes
- [ ] Located epic_lessons_learned.md file

**If resuming after session compaction:**
1. Check EPIC_README.md "Agent Status" section for current step
2. Re-read this guide from the beginning
3. Continue from documented checkpoint

---

## Quick Start

### What is this sub-stage?

**STAGE_6c - Epic Final Review** is the final validation phase of Stage 6, where you apply an epic-level PR review checklist, handle any discovered issues through bug fixes, and perform final verification before declaring the epic complete.

**This is NOT feature-level review** - Stage 5c already reviewed individual features. This focuses on:
- Epic-wide architectural consistency
- Cross-feature code quality
- Epic scope and completeness
- Final validation against original request

### When do you use this guide?

**Use this guide when:**
- STAGE_6b is complete (all 3 QC rounds passed)
- Epic smoke testing passed (STAGE_6a)
- Ready for final epic-level PR review and validation
- All features completed Stage 5e

**Do NOT use this guide if:**
- STAGE_6a smoke testing not complete
- STAGE_6b QC rounds not complete
- Any features still in Stage 5b implementation
- Pending bug fixes not yet completed

### What are the key outputs?

1. **Epic PR Review Results** (documented in epic_lessons_learned.md)
   - 11 categories reviewed at epic level
   - All categories must pass (no failures)

2. **Bug Fixes (if issues found)**
   - Bug fix folders created for any issues
   - Stage 6 RESTARTED after bug fixes

3. **Final Verification**
   - All Stage 6 steps confirmed complete
   - epic_lessons_learned.md updated
   - EPIC_README.md marked complete

4. **Stage 6 Completion**
   - Ready to proceed to Stage 7 (Epic Cleanup)

### Time estimate

**60-90 minutes** (if no issues found)
- Epic PR Review: 30-45 minutes
- Final Verification: 15-30 minutes
- Documentation updates: 15 minutes

**+2-4 hours per bug fix** (if issues found, includes Stage 6 restart)

### Workflow overview

```
STAGE_6c Workflow (Steps 6-8)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Prerequisites Met?
  ├─ STAGE_6b complete (3 QC rounds passed)
  ├─ No pending issues
  └─ All tests passing (100%)
         │
         ▼
┌─────────────────────────────────────┐
│ STEP 6: Epic PR Review              │
│ (11 Categories - Epic Scope)        │
└─────────────────────────────────────┘
         │
         ├─ Correctness (epic level)
         ├─ Code Quality (epic level)
         ├─ Comments & Documentation
         ├─ Code Organization
         ├─ Testing (epic level)
         ├─ Security (epic level)
         ├─ Performance (epic level)
         ├─ Error Handling (epic level)
         ├─ Architecture (CRITICAL)
         ├─ Backwards Compatibility
         └─ Scope & Changes
         │
         ▼
    Any Issues Found?
    ├─ YES → STEP 7 (Handle Issues)
    │         │
    │         ├─ Document all issues
    │         ├─ Create bug fixes
    │         └─ RESTART Stage 6
    │
    └─ NO → STEP 8 (Final Verification)
              │
              ├─ Verify all issues resolved
              ├─ Update EPIC_README.md
              ├─ Update epic_lessons_learned.md
              └─ Mark Stage 6 complete
              │
              ▼
        Stage 6 COMPLETE
              │
              ▼
        Ready for Stage 7
```

---

## Critical Rules for Stage 6c

```
┌─────────────────────────────────────────────────────────────┐
│ CRITICAL RULES - Stage 6c (Epic Final Review)               │
└─────────────────────────────────────────────────────────────┘

1. ⚠️ Epic-level PR review focuses on CROSS-FEATURE concerns
   - Feature-level review already done in Stage 5c
   - Focus: Architectural consistency, cross-feature impacts
   - Don't repeat feature-level checks

2. ⚠️ ALL 11 categories are MANDATORY
   - Cannot skip categories
   - All categories must PASS (no exceptions)
   - If ANY category fails → create bug fix

3. ⚠️ If issues found, you MUST RESTART Stage 6
   - After bug fixes complete
   - RESTART from STAGE_6a (smoke testing)
   - Cannot partially continue Stage 6

4. ⚠️ Validate against ORIGINAL epic request
   - Not against evolved specs
   - Re-read {epic_name}.txt file
   - Verify user's stated goals achieved

5. ⚠️ Zero tolerance for architectural inconsistencies
   - Design patterns must be consistent across features
   - Code style must be uniform
   - Error handling must be consistent

6. ⚠️ 100% test pass rate required
   - All unit tests must pass
   - No "expected failures"
   - Fix ALL test failures before marking complete

7. ⚠️ Document EVERYTHING in epic_lessons_learned.md
   - PR review results
   - Issues found (if any)
   - Stage 6 insights
   - Improvements for future epics

8. ⚠️ Cannot proceed to Stage 7 without completion
   - All 8 steps of Stage 6 must be complete
   - No pending issues or bug fixes
   - EPIC_README.md must show Stage 6 complete
```

---

## Prerequisites

**Before starting Stage 6c, verify ALL of these are true:**

### From STAGE_6b (QC Rounds)
- [ ] QC Round 1 (Cross-Feature Integration): ✅ PASSED
- [ ] QC Round 2 (Epic Cohesion & Consistency): ✅ PASSED
- [ ] QC Round 3 (End-to-End Success Criteria): ✅ PASSED
- [ ] STAGE_6b completion documented in EPIC_README.md

### From STAGE_6a (Smoke Testing)
- [ ] Epic smoke testing Part 1 (Import Tests): ✅ PASSED
- [ ] Epic smoke testing Part 2 (Entry Point Tests): ✅ PASSED
- [ ] Epic smoke testing Part 3 (E2E Execution Tests): ✅ PASSED
- [ ] Epic smoke testing Part 4 (Cross-Feature Integration Tests): ✅ PASSED

### Feature Completion
- [ ] All features completed Stage 5e (Post-Feature Testing Update)
- [ ] No features currently in Stage 5b (Implementation)
- [ ] No pending feature work

### Quality Gates
- [ ] All unit tests passing (100% pass rate)
- [ ] No known bugs or issues
- [ ] All previous bug fixes (if any) completed Stage 5c

### Documentation
- [ ] epic_lessons_learned.md exists and accessible
- [ ] EPIC_README.md shows STAGE_6b complete
- [ ] Original {epic_name}.txt file located

**If ANY prerequisite not met:**
- STOP - Do not proceed with Stage 6c
- Complete missing prerequisites first
- Return to appropriate stage (6a or 6b)

---

## STEP 6: Epic PR Review (11 Categories - Epic Scope)

### Overview

**Objective:** Apply PR review checklist to epic-wide changes with focus on architectural consistency.

**Critical Note:** This is the SAME 11-category checklist from Stage 5c, but applied to:
- Epic-wide changes (not individual features)
- Architectural consistency across features
- Cross-feature impacts

**NOT a repeat of feature-level review** - Focus on what's different when features work together.

### Step 6.1: Correctness (Epic Level)

**Focus:** Do all features implement requirements correctly AND work correctly together?

**Validation Checklist:**
- [ ] All features implement their requirements correctly (per specs)
- [ ] Cross-feature workflows produce correct results
- [ ] Integration points function correctly (no data corruption)
- [ ] No logic errors in epic-wide flows
- [ ] Edge cases handled correctly across feature boundaries

**How to verify:**
```python
# Example: Verify cross-feature workflow correctness
# Epic: Improve Draft Helper (ADP + Matchup + Performance)

# 1. Verify Feature 01 (ADP) correctness
from feature_01.adp_manager import ADPManager
adp_mgr = ADPManager()
multiplier, rank = adp_mgr.get_adp_data("Patrick Mahomes")
assert 0.5 <= multiplier <= 1.5, "ADP multiplier out of valid range"
assert rank > 0, "ADP rank invalid"

# 2. Verify Feature 02 (Matchup) correctness
from feature_02.matchup_manager import MatchupManager
matchup_mgr = MatchupManager()
difficulty = matchup_mgr.get_matchup_difficulty("Patrick Mahomes", week=5)
assert 0.5 <= difficulty <= 1.5, "Matchup difficulty out of valid range"

# 3. Verify INTEGRATION correctness
from league_helper.util.FantasyPlayer import FantasyPlayer
player = FantasyPlayer("Patrick Mahomes", "QB", 300.0)
# Apply both multipliers
final_score = player.score * multiplier * difficulty
# Verify final score makes sense
assert 150 <= final_score <= 600, f"Final score {final_score} unrealistic"
```

**Document results:**
```markdown
### Correctness (Epic Level): ✅ PASS

**Validated:**
- All 3 features implement requirements correctly
- Cross-feature workflow (ADP + Matchup → Final Score) correct
- Integration points produce correct data (verified with assertions)
- Edge cases tested: Missing ADP data → graceful degradation
- Logic flow verified: Base score → ADP multiplier → Matchup multiplier → Final score

**Issues Found:** None
```

**If issues found:** Document and proceed to Step 7 (Handle Issues)

---

### Step 6.2: Code Quality (Epic Level)

**Focus:** Is code quality consistent across all features?

**Validation Checklist:**
- [ ] Code quality consistent across all features (same standards applied)
- [ ] No duplicate code between features that should be shared
- [ ] Abstractions appropriate for epic complexity
- [ ] Readability consistent across epic
- [ ] No feature has significantly lower quality than others

**How to verify:**
```bash
# 1. Check for code duplication across features
# Look for similar functions/classes that should be extracted

# Example: Both Feature 01 and Feature 02 have `load_csv()` methods
# Should be extracted to utils/csv_utils.py

# 2. Review code complexity across features
# All features should have similar complexity levels

# 3. Check for inconsistent abstractions
# Example: Feature 01 uses classes, Feature 02 uses functions only
# Should be consistent (all classes or all functions)
```

**Document results:**
```markdown
### Code Quality (Epic Level): ✅ PASS

**Validated:**
- Code quality consistent across all 3 features
- Shared utilities extracted (csv_utils.py, error_handler.py)
- Abstractions consistent: All features use Manager classes
- Readability consistent: Same docstring style, naming conventions
- No features significantly lower quality

**Issues Found:** None
```

**Common issues to look for:**
- Feature 01 uses detailed docstrings, Feature 02 has minimal docs → Inconsistent
- Feature 01 has 100-line functions, Feature 02 has 10-line functions → Quality variance
- Both features duplicate CSV loading code → Should extract to utils

---

### Step 6.3: Comments & Documentation (Epic Level)

**Focus:** Is epic-level documentation complete and integration points documented?

**Validation Checklist:**
- [ ] Epic-level documentation complete (EPIC_README.md)
- [ ] Cross-feature interactions documented
- [ ] Integration points documented (interfaces, data flow)
- [ ] Epic success criteria documented
- [ ] User-facing documentation updated (if applicable)

**How to verify:**
```markdown
# 1. Check EPIC_README.md completeness
- Epic overview present
- Feature list complete
- Integration points documented
- Epic success criteria listed

# 2. Check integration point documentation
# Example: Feature 01 → Feature 02 interface

# In feature_01/README.md:
## Public Interfaces
- `get_adp_data(player_name: str) -> Tuple[float, int]`
  - Returns: (multiplier, adp_rank)
  - Used by: Feature 02 (Matchup System)
  - Contract: multiplier in [0.5, 1.5], rank > 0

# In feature_02/README.md:
## Dependencies
- Feature 01: Consumes `get_adp_data()` for ADP multiplier
  - Expected: Tuple[float, int]
  - Fallback: If unavailable, uses default multiplier 1.0
```

**Document results:**
```markdown
### Comments & Documentation (Epic Level): ✅ PASS

**Validated:**
- EPIC_README.md complete (epic overview, feature list, integration points)
- Cross-feature interactions documented in both feature READMEs
- Integration points documented with contracts (types, ranges, fallbacks)
- Epic success criteria documented in epic_smoke_test_plan.md
- No user-facing docs needed (internal epic)

**Issues Found:** None
```

---

### Step 6.4: Code Organization & Refactoring (Epic Level)

**Focus:** Is feature organization consistent and epic folder structure logical?

**Validation Checklist:**
- [ ] Feature organization consistent (same folder structure)
- [ ] Shared utilities extracted (not duplicated across features)
- [ ] Epic folder structure logical and navigable
- [ ] No refactoring opportunities missed (DRY violations)
- [ ] Feature boundaries clean (no circular dependencies)

**How to verify:**
```bash
# 1. Check feature folder structure consistency
feature_01_win_rate_sim_json_integration/
  ├── README.md
  ├── spec.md
  ├── checklist.md
  ├── todo.md
  ├── code_changes.md
  └── lessons_learned.md

feature_02_accuracy_sim_json_integration/
  ├── README.md
  ├── spec.md
  ├── checklist.md
  ├── todo.md
  ├── code_changes.md
  └── lessons_learned.md

# Structure consistent? ✅

# 2. Check for shared utilities
# Both features load JSON data → Should use shared JSONLoader

# 3. Check for circular dependencies
# Feature 01 imports Feature 02 → Feature 02 imports Feature 01 → ❌ CIRCULAR
```

**Document results:**
```markdown
### Code Organization & Refactoring (Epic Level): ✅ PASS

**Validated:**
- Feature folder structure consistent (same files in all features)
- Shared utilities extracted (utils/json_loader.py used by all features)
- Epic folder structure logical (features/, research/, EPIC_README.md)
- No DRY violations (checked for duplicate code)
- No circular dependencies (dependency graph is acyclic)

**Issues Found:** None
```

---

### Step 6.5: Testing (Epic Level)

**Focus:** Do epic-level integration tests exist and all tests pass?

**Validation Checklist:**
- [ ] Epic-level integration tests exist (test cross-feature scenarios)
- [ ] Cross-feature scenarios tested (not just individual features)
- [ ] All unit tests passing (100% pass rate)
- [ ] Test coverage adequate for epic (not just features)
- [ ] Integration test failures caught during development

**How to verify:**
```bash
# 1. Run all tests
python tests/run_all_tests.py

# Expected output:
# ============================= test session starts ==============================
# collected 2247 items
#
# tests/unit/test_adp_manager.py ................                          [  1%]
# tests/unit/test_matchup_manager.py ................                      [  2%]
# tests/integration/test_epic_integration.py ....                          [ 99%]
# ============================== 2247 passed in 45.32s ===========================

# 2. Check for epic-level integration tests
# tests/integration/test_epic_integration.py should exist and test cross-feature workflows

# 3. Verify test coverage for integration points
# Coverage should include: Feature 01 → Feature 02 → Feature 03 flow
```

**Document results:**
```markdown
### Testing (Epic Level): ✅ PASS

**Validated:**
- Epic-level integration tests exist (tests/integration/test_epic_integration.py)
- Cross-feature scenarios tested (ADP + Matchup + Performance workflow)
- All 2247 unit tests passing (100% pass rate)
- Test coverage adequate: 92% overall, 87% for integration points
- Integration tests cover: Data flow, error propagation, edge cases

**Issues Found:** None
```

**If test failures:**
```markdown
### Testing (Epic Level): ❌ FAIL

**Issues Found:**
- 3 integration tests failing in test_epic_integration.py
- Error: AssertionError: Final score calculation incorrect
- Root cause: Feature 02 not applying ADP multiplier correctly

**Action Required:** Create bug fix (proceed to Step 7)
```

---

### Step 6.6: Security (Epic Level)

**Focus:** Are there security vulnerabilities in epic workflows?

**Validation Checklist:**
- [ ] No security vulnerabilities in epic workflows
- [ ] Input validation consistent across features
- [ ] No sensitive data exposed (logs, error messages, outputs)
- [ ] Error messages don't leak internals
- [ ] File operations secure (no path traversal, injection)

**How to verify:**
```python
# 1. Check input validation across features
# All features should validate inputs consistently

# Example: Feature 01 validates player names
def get_adp_data(player_name: str) -> Tuple[float, int]:
    if not player_name:
        raise ValueError("Player name required")
    if not isinstance(player_name, str):
        raise TypeError("Player name must be string")
    # ... proceed

# Feature 02 should validate similarly
def get_matchup_difficulty(player_name: str, week: int) -> float:
    if not player_name:
        raise ValueError("Player name required")  # ✅ Consistent
    if not isinstance(player_name, str):
        raise TypeError("Player name must be string")  # ✅ Consistent
    # ... proceed

# 2. Check for sensitive data leaks
# Error messages should not expose file paths, DB credentials, etc.

# 3. Check file operations
# Ensure no path traversal: player_name = "../../etc/passwd"
```

**Document results:**
```markdown
### Security (Epic Level): ✅ PASS

**Validated:**
- No security vulnerabilities identified in epic workflows
- Input validation consistent across all features (TypeError, ValueError for invalid inputs)
- No sensitive data exposed (checked logs, error messages, CSV outputs)
- Error messages user-friendly (no internal paths or stack traces)
- File operations secure (validated paths, no injection risks)

**Issues Found:** None
```

---

### Step 6.7: Performance (Epic Level)

**Focus:** Is epic performance acceptable and no regressions from baseline?

**Validation Checklist:**
- [ ] Epic performance acceptable (meets user expectations)
- [ ] No performance regressions from baseline (pre-epic)
- [ ] Cross-feature calls optimized (no N+1 queries)
- [ ] No performance bottlenecks in integration points
- [ ] Performance tested with realistic data volumes

**How to verify:**
```python
# 1. Measure epic-level performance
import time
start = time.time()

# Run epic workflow (e.g., draft with all features)
# python run_league_helper.py --mode draft --week 5 --iterations 10

end = time.time()
epic_time = end - start
print(f"Epic execution time: {epic_time:.2f}s")

# 2. Compare to baseline (pre-epic)
baseline_time = 2.5  # seconds (from Stage 1 epic notes)
regression = (epic_time - baseline_time) / baseline_time * 100
print(f"Performance change: {regression:+.1f}%")

# Acceptable if: regression < 20% OR epic_time < 5s

# 3. Check for N+1 queries
# Example BAD: Loading ADP data for each player in loop
for player in players:
    adp_data = get_adp_data(player.name)  # ❌ N queries

# Example GOOD: Batch load ADP data
adp_data_map = get_all_adp_data()  # ✅ 1 query
for player in players:
    adp_data = adp_data_map.get(player.name)
```

**Document results:**
```markdown
### Performance (Epic Level): ✅ PASS

**Validated:**
- Epic execution time: 3.2s (baseline: 2.5s, +28% regression)
- Regression acceptable: <5s threshold met
- Cross-feature calls optimized: Batch loading implemented for ADP and Matchup data
- No N+1 queries identified
- Performance tested with 200 players (realistic volume)

**Performance Breakdown:**
- Feature 01 (ADP): 0.8s
- Feature 02 (Matchup): 1.2s
- Feature 03 (Performance): 0.5s
- Integration overhead: 0.7s (acceptable)

**Issues Found:** None
```

**If performance issues:**
```markdown
### Performance (Epic Level): ❌ FAIL

**Issues Found:**
- Epic execution time: 12.5s (baseline: 2.5s, +400% regression)
- Root cause: N+1 queries in Feature 02 (loading matchup data per player)

**Action Required:** Create bug fix to batch load matchup data (proceed to Step 7)
```

---

### Step 6.8: Error Handling (Epic Level)

**Focus:** Is error handling consistent and do errors propagate correctly between features?

**Validation Checklist:**
- [ ] Error handling consistent across features (same error classes, patterns)
- [ ] Errors propagate correctly between features (not swallowed)
- [ ] User-facing errors helpful and actionable
- [ ] Epic degrades gracefully on errors (doesn't crash entire system)
- [ ] Error logging consistent (same format, level)

**How to verify:**
```python
# 1. Check error class consistency
# Feature 01:
from utils.error_handler import DataProcessingError
raise DataProcessingError("ADP data not found")

# Feature 02:
from utils.error_handler import DataProcessingError  # ✅ Same error class
raise DataProcessingError("Matchup data not found")

# 2. Check error propagation
# Feature 01 error should propagate to Feature 02
try:
    adp_data = get_adp_data("NonexistentPlayer")
except DataProcessingError as e:
    # Feature 02 should catch and handle
    logger.warning(f"ADP unavailable: {e}")
    # Use default multiplier
    adp_data = (1.0, 999)

# 3. Check user-facing error messages
# GOOD: "Player 'John Doe' not found in ADP data. Using default ranking."
# BAD: "KeyError: 'John Doe' at line 342 in adp_manager.py"

# 4. Check graceful degradation
# If Feature 01 fails, Feature 02 should still work (with defaults)
```

**Document results:**
```markdown
### Error Handling (Epic Level): ✅ PASS

**Validated:**
- Error handling consistent across features (all use DataProcessingError from utils.error_handler)
- Errors propagate correctly: Feature 01 errors caught by Feature 02, logged, and handled gracefully
- User-facing errors helpful: "Player not found in ADP data. Using default ranking."
- Graceful degradation tested: Feature 01 failure doesn't crash epic (defaults used)
- Error logging consistent: All features use logger.warning() for non-critical errors

**Error Scenarios Tested:**
- Missing ADP data → Default multiplier 1.0 used
- Missing matchup data → Default difficulty 1.0 used
- Invalid player name → Clear error message shown to user

**Issues Found:** None
```

---

### Step 6.9: Architecture (Epic Level - CRITICAL)

**Focus:** Is epic architecture coherent and design patterns applied consistently?

**THIS IS THE MOST IMPORTANT CATEGORY FOR EPIC-LEVEL REVIEW**

**Validation Checklist:**
- [ ] Epic architecture coherent (clear design, not ad-hoc)
- [ ] Feature separation appropriate (not too coupled, not too fragmented)
- [ ] Interfaces between features clean (well-defined contracts)
- [ ] No architectural inconsistencies (e.g., Feature 01 uses classes, Feature 02 uses functions)
- [ ] Design patterns applied consistently (e.g., Manager pattern, Factory pattern)
- [ ] Epic maintainable and extensible (easy to add features)

**How to verify:**
```python
# 1. Check architectural consistency
# All features should follow same architectural pattern

# Feature 01:
class ADPManager:
    def __init__(self, data_folder: Path):
        self.data_folder = data_folder

    def get_adp_data(self, player_name: str) -> Tuple[float, int]:
        # ...

# Feature 02:
class MatchupManager:  # ✅ Same Manager pattern
    def __init__(self, data_folder: Path):
        self.data_folder = data_folder

    def get_matchup_difficulty(self, player_name: str, week: int) -> float:
        # ...

# Feature 03:
class PerformanceTracker:  # ✅ Consistent
    def __init__(self, data_folder: Path):
        self.data_folder = data_folder

    def track_performance(self, player_name: str, actual_score: float):
        # ...

# 2. Check interface design
# Interfaces should be clean and well-defined

# GOOD:
def get_adp_data(player_name: str) -> Tuple[float, int]:
    """Clean interface: single responsibility, clear contract"""

# BAD:
def get_adp_data_and_maybe_matchup_if_available(player_name: str, week: Optional[int] = None) -> Union[float, Tuple[float, int], Dict[str, Any]]:
    """Unclear interface: multiple responsibilities, ambiguous return type"""

# 3. Check feature coupling
# Features should be loosely coupled (depend on interfaces, not implementations)

# GOOD: Feature 02 depends on interface
from feature_01.interfaces import IADPProvider
adp_provider: IADPProvider = get_adp_provider()
multiplier = adp_provider.get_multiplier("Patrick Mahomes")

# BAD: Feature 02 depends on implementation
from feature_01.adp_manager import ADPManager
adp_mgr = ADPManager()  # ❌ Tightly coupled
multiplier = adp_mgr.get_adp_data("Patrick Mahomes")[0]

# 4. Check design pattern consistency
# All features should use same patterns (Manager, Factory, Strategy, etc.)
```

**Document results:**
```markdown
### Architecture (Epic Level): ✅ PASS

**Validated:**
- Epic architecture coherent: Manager pattern applied consistently across all features
- Feature separation appropriate: Each feature has single responsibility, clear boundaries
- Interfaces clean: All methods have clear contracts (type hints, docstrings)
- Architectural consistency: All features use Manager classes with same initialization pattern
- Design patterns consistent: Manager pattern for business logic, Factory pattern for object creation
- Maintainability: Easy to add new features (follow same Manager pattern)

**Architectural Patterns Identified:**
- Manager Pattern: ADPManager, MatchupManager, PerformanceTracker
- Dependency Injection: Managers accept data_folder in __init__
- Error Context: All managers use error_handler.error_context()
- Graceful Degradation: Features provide defaults when dependencies unavailable

**Issues Found:** None
```

**If architectural issues:**
```markdown
### Architecture (Epic Level): ❌ FAIL

**Issues Found:**
- Architectural inconsistency: Feature 01 uses Manager class, Feature 02 uses standalone functions
- Tight coupling: Feature 02 directly imports Feature 01 implementation (not interface)
- Design pattern inconsistency: Feature 01 uses Factory pattern, Feature 02 has no pattern

**Action Required:** Create bug fix to refactor Feature 02 to Manager pattern (proceed to Step 7)
```

---

### Step 6.10: Backwards Compatibility (Epic Level)

**Focus:** Does epic break existing functionality?

**Validation Checklist:**
- [ ] Epic doesn't break existing functionality (pre-epic code still works)
- [ ] Migration path clear (if breaking changes necessary)
- [ ] Deprecated features handled correctly (warnings, docs)
- [ ] Version compatibility maintained (if applicable)
- [ ] Existing tests still pass (not just new epic tests)

**How to verify:**
```python
# 1. Run existing tests (pre-epic)
# All tests that existed before epic should still pass

python -m pytest tests/unit/test_player_manager.py -v
# All tests pass? ✅

# 2. Test existing workflows (pre-epic functionality)
# Epic should not break users who don't use new features

# Example: User runs draft without using new ADP feature
python run_league_helper.py --mode draft --week 5
# Should still work as before epic? ✅

# 3. Check for breaking changes
# Example: Did epic change existing CSV column names?
# Before epic: 'score' column
# After epic: 'final_score' column ❌ BREAKING CHANGE

# 4. Check for deprecation warnings
# If deprecating old features, should warn user
import warnings
warnings.warn("Old ADP format deprecated. Use new format.", DeprecationWarning)
```

**Document results:**
```markdown
### Backwards Compatibility (Epic Level): ✅ PASS

**Validated:**
- Epic doesn't break existing functionality (all pre-epic tests pass)
- No breaking changes to existing APIs or data formats
- Existing workflows still work (draft mode without new features)
- No deprecated features in this epic
- Version compatibility maintained (no version bumps required)

**Backwards Compatibility Tests:**
- Existing unit tests: 2200/2200 passing ✅
- Existing integration tests: 25/25 passing ✅
- Pre-epic draft workflow: Works without new features ✅
- Pre-epic CSV format: Unchanged (new columns added, not replaced) ✅

**Issues Found:** None
```

---

### Step 6.11: Scope & Changes (Epic Level)

**Focus:** Does epic scope match original request with no undocumented features?

**Validation Checklist:**
- [ ] Epic scope matches original request (from {epic_name}.txt)
- [ ] No scope creep (undocumented features added)
- [ ] All changes necessary for epic (no unrelated changes)
- [ ] No unrelated changes included (bug fixes, refactoring unrelated to epic)
- [ ] Epic goals achieved (validated in QC Round 3)

**How to verify:**
```markdown
# 1. Re-read original epic request
# Read {epic_name}.txt file from feature-updates/

# 2. Compare epic scope to original request
# Create validation table:

| Original Request | Implemented | Evidence | Scope Creep? |
|------------------|-------------|----------|--------------|
| Integrate ADP data | ✅ YES | Feature 01 | NO |
| Add matchup projections | ✅ YES | Feature 02 | NO |
| Track performance | ✅ YES | Feature 03 | NO |
| (NOT requested: Refactor PlayerManager) | ✅ YES | Code changes | ⚠️ YES - SCOPE CREEP |

# 3. Check for unrelated changes
# Example: Epic about draft helper but also refactored trade analyzer ❌

# 4. Verify all changes necessary
# Every code change should trace back to epic requirements
```

**Document results:**
```markdown
### Scope & Changes (Epic Level): ✅ PASS

**Validated:**
- Epic scope matches original request (3 features requested, 3 features delivered)
- No scope creep identified (no undocumented features)
- All changes necessary for epic (traced back to requirements)
- No unrelated changes (no bug fixes or refactoring outside epic scope)
- Epic goals achieved (validated in QC Round 3)

**Scope Validation Table:**
| Original Goal | Delivered | Evidence |
|---------------|-----------|----------|
| Integrate ADP data | ✅ YES | Feature 01: ADPManager, adp_data.json |
| Add matchup projections | ✅ YES | Feature 02: MatchupManager, matchup_data.json |
| Track performance vs projections | ✅ YES | Feature 03: PerformanceTracker, performance_tracking.csv |

**Code Changes Analysis:**
- 47 files changed (all related to epic features)
- 0 unrelated changes identified
- 0 scope creep items identified

**Issues Found:** None
```

---

### Step 6.12: Document PR Review Results

**After reviewing all 11 categories, document results in epic_lessons_learned.md:**

```markdown
## Stage 6c - Epic PR Review (11 Categories)

**Date:** 2025-01-02
**Reviewer:** Claude Agent
**Epic:** integrate_new_player_data_into_simulation

**Review Results:**

| Category | Status | Notes |
|----------|--------|-------|
| 1. Correctness | ✅ PASS | All cross-feature workflows correct, integration points verified |
| 2. Code Quality | ✅ PASS | Consistent quality across features, shared utilities extracted |
| 3. Comments & Docs | ✅ PASS | Epic-level docs complete, integration points documented |
| 4. Organization | ✅ PASS | Consistent structure, utilities extracted, no circular deps |
| 5. Testing | ✅ PASS | Epic integration tests exist, 100% test pass rate (2247 tests) |
| 6. Security | ✅ PASS | No vulnerabilities, consistent input validation |
| 7. Performance | ✅ PASS | 3.2s for full workflow (acceptable), no N+1 queries |
| 8. Error Handling | ✅ PASS | Consistent error handling, graceful degradation |
| 9. Architecture | ✅ PASS | Coherent architecture, Manager pattern consistent, clean interfaces |
| 10. Compatibility | ✅ PASS | No breaking changes, existing features work |
| 11. Scope | ✅ PASS | Scope matches original request, no scope creep |

**Overall Status:** ✅ APPROVED

**Issues Found:** 0

**Recommendations:** None - Epic ready for Stage 7 (Epic Cleanup)
```

**If ANY category fails:**
```markdown
**Overall Status:** ❌ REJECTED

**Issues Found:** 2

**Issue 1:** Architectural inconsistency (Category 9: Architecture)
- Feature 01 uses Manager pattern, Feature 02 uses standalone functions
- Requires refactoring Feature 02 to match pattern

**Issue 2:** Performance regression (Category 7: Performance)
- Epic execution time 12.5s (baseline 2.5s, +400%)
- Root cause: N+1 queries in Feature 02

**Next Action:** Create bug fixes for both issues, then RESTART Stage 6
```

---

## STEP 7: Handle Issues (If Any Discovered)

### Overview

**Objective:** Create bug fixes for any epic-level integration issues discovered during Step 6 (Epic PR Review).

**When to use this step:**
- ANY category in Step 6 failed
- Issues discovered during PR review
- Critical issues require immediate fixing

**When to SKIP this step:**
- All 11 categories passed in Step 6
- No issues discovered
- Epic ready for final verification (proceed to Step 8)

### Step 7.1: Document ALL Issues

If ANY issues discovered in Step 6, document comprehensively in epic_lessons_learned.md:

```markdown
## Stage 6c Issues Found

**Date:** 2025-01-02

**Issue 1: Architectural Inconsistency**
- **Discovered In:** Step 6.9 (Epic PR Review - Architecture)
- **Description:** Feature 01 uses Manager class pattern, Feature 02 uses standalone functions
- **Impact:** HIGH - Architectural inconsistency makes epic hard to maintain
- **Root Cause:** Different agents implemented features with different patterns
- **Fix Required:** Refactor Feature 02 to Manager pattern (MatchupManager class)
- **Priority:** high

**Issue 2: Performance Regression**
- **Discovered In:** Step 6.7 (Epic PR Review - Performance)
- **Description:** Epic execution time 12.5s (baseline 2.5s, +400% regression)
- **Impact:** HIGH - Unacceptable performance for user
- **Root Cause:** N+1 queries in Feature 02 (loading matchup data per player in loop)
- **Fix Required:** Implement batch loading for matchup data
- **Priority:** high

**Issue 3: Inconsistent Error Messages**
- **Discovered In:** Step 6.8 (Epic PR Review - Error Handling)
- **Description:** Feature 01 uses "Player not found", Feature 02 uses "No player data"
- **Impact:** LOW - User confusion but not functional
- **Root Cause:** Different error message templates
- **Fix Required:** Standardize error messages to "Player '{name}' not found in {feature} data"
- **Priority:** medium
```

### Step 7.2: Determine Bug Fix Priorities

**Priority Levels:**

**high:** Issue breaks epic functionality OR unacceptable quality
- Epic won't work correctly
- User-facing failures
- Architectural inconsistencies
- Security vulnerabilities
- Performance regressions >100%
- **Action:** Interrupt Stage 6 immediately, create bug fix

**medium:** Issue affects quality but not functionality
- Inconsistencies (error messages, code style)
- Minor performance issues (<100% regression)
- Incomplete documentation
- **Action:** Complete current step, then create bug fix

**low:** Issue is cosmetic or minor
- Code style nitpicks
- Optional refactoring
- Nice-to-have improvements
- **Action:** Document for future, don't create bug fix during Stage 6

**Example prioritization:**
```markdown
## Issue Prioritization

**HIGH priority (create bug fixes now):**
- Issue 1: Architectural inconsistency → bugfix_high_architecture_inconsistency
- Issue 2: Performance regression → bugfix_high_performance_regression

**MEDIUM priority (create bug fixes after high):**
- Issue 3: Inconsistent error messages → bugfix_medium_error_messages

**LOW priority (document only, no bug fix):**
- None identified
```

### Step 7.3: Present Issues to User

**Before creating bug fixes, present issues to user and get approval:**

**User presentation template:**
```markdown
I found [number] issues during Stage 6c Epic PR Review that require bug fixes:

**ISSUE 1: Architectural Inconsistency (HIGH priority)**
- **Problem:** Feature 01 uses Manager class pattern, Feature 02 uses standalone functions
- **Impact:** Architectural inconsistency makes epic hard to maintain
- **Fix:** Refactor Feature 02 to Manager pattern (MatchupManager class)
- **Estimated time:** 2-3 hours (bug fix workflow: Stage 2 → 5a → 5b → 5c)

**ISSUE 2: Performance Regression (HIGH priority)**
- **Problem:** Epic execution time 12.5s (baseline 2.5s, +400% regression)
- **Impact:** Unacceptable performance for user
- **Fix:** Implement batch loading for matchup data in Feature 02
- **Estimated time:** 1-2 hours

After fixing these issues, I'll need to RESTART Stage 6 from the beginning (STAGE_6a smoke testing) to ensure the fixes didn't introduce new issues.

Should I proceed with creating these bug fixes?
```

**Wait for user approval before proceeding.**

### Step 7.4: Create Bug Fixes Using Bug Fix Workflow

**For EACH issue, create a bug fix using STAGE_5_bug_fix_workflow_guide.md:**

**Step-by-step process:**

1. **Create bug fix folder:**
   ```
   bugfix_high_architecture_inconsistency/
   ├── notes.txt
   ├── README.md
   ├── spec.md
   ├── checklist.md
   ├── todo.md
   ├── code_changes.md
   └── lessons_learned.md
   ```

2. **Create notes.txt with issue description:**
   ```markdown
   # Bug Fix: Architectural Inconsistency in Feature 02

   **Issue:** Feature 01 uses Manager class pattern, Feature 02 uses standalone functions
   **Impact:** HIGH - Architectural inconsistency makes epic hard to maintain
   **Root Cause:** Different agents implemented features with different patterns
   **Fix:** Refactor Feature 02 to Manager pattern (create MatchupManager class)

   **Evidence:**
   - Feature 01: ADPManager class (feature_01/adp_manager.py)
   - Feature 02: standalone functions get_matchup_difficulty(), load_matchup_data()

   **Fix Requirements:**
   - Create MatchupManager class
   - Move standalone functions to class methods
   - Update imports in consuming code
   - Update tests
   ```

3. **User verifies notes:**
   Present notes.txt to user, get approval

4. **Update EPIC_README.md to show Stage 6 paused:**
   ```markdown
   ## Agent Status
   **Current Stage:** Stage 6c - Epic Final Review
   **Status:** PAUSED (bug fix in progress)
   **Paused At:** Step 7 (Handle Issues)
   **Last Updated:** 2025-01-02 14:30

   **Bug Fixes In Progress:**
   - bugfix_high_architecture_inconsistency (Stage 5a - TODO Creation)
   - bugfix_high_performance_regression (queued)

   **Next Action:** Complete bug fixes, then RESTART Stage 6 from STAGE_6a
   ```

5. **Run bug fix through workflow:**
   - **Stage 2 (Deep Dive):** Understand issue, create spec
   - **Stage 5a (TODO Creation):** Create implementation plan
   - **Stage 5b (Implementation):** Fix the issue
   - **Stage 5c (Post-Implementation):** Smoke test, QC, PR review

6. **Bug fix stays in epic folder (doesn't move to done/)**

7. **Repeat for all high and medium priority issues**

### Step 7.5: RESTART Stage 6 After Bug Fixes

**CRITICAL:** You MUST COMPLETELY RESTART Stage 6 after ALL bug fixes complete.

**Why COMPLETE restart?**
- Bug fixes may have affected areas already checked
- Cannot assume previous QC results still valid
- Ensures epic-level quality maintained
- Integration changes may have ripple effects

**Restart Protocol:**

1. **Mark all Stage 6 steps as "incomplete" in EPIC_README.md**

2. **Re-run STAGE_6a (Epic Smoke Testing):**
   - Part 1: Epic-Level Import Tests
   - Part 2: Epic-Level Entry Point Tests
   - Part 3: Epic End-to-End Execution Tests
   - Part 4: Cross-Feature Integration Tests

3. **Re-run STAGE_6b (Epic QC Rounds):**
   - QC Round 1: Cross-Feature Integration
   - QC Round 2: Epic Cohesion & Consistency
   - QC Round 3: End-to-End Success Criteria

4. **Re-run STAGE_6c (Epic Final Review):**
   - STEP 6: Epic PR Review (all 11 categories)
   - STEP 7: Handle Issues (if new issues found)
   - STEP 8: Final Verification

**Document restart in epic_lessons_learned.md:**

```markdown
## Stage 6 Restart Log

**Restart Date:** 2025-01-02
**Reason:** 2 bug fixes completed (bugfix_high_architecture_inconsistency, bugfix_high_performance_regression)

**Bug Fixes Completed:**
1. bugfix_high_architecture_inconsistency: Refactored Feature 02 to Manager pattern
2. bugfix_high_performance_regression: Implemented batch loading for matchup data

**Restart Actions:**
- ✅ Re-ran STAGE_6a: Epic Smoke Testing (all 4 parts) - PASSED
- ✅ Re-ran STAGE_6b: QC Round 1 (Cross-Feature Integration) - PASSED
- ✅ Re-ran STAGE_6b: QC Round 2 (Epic Cohesion & Consistency) - PASSED
- ✅ Re-ran STAGE_6b: QC Round 3 (End-to-End Success Criteria) - PASSED
- ✅ Re-ran STAGE_6c: Epic PR Review (all 11 categories) - PASSED
- ✅ All unit tests passing (100% - 2247 tests)

**Result:** Stage 6 complete after restart (no new issues found)
```

**Update EPIC_README.md Agent Status after restart:**
```markdown
## Agent Status
**Current Stage:** Stage 6c - Epic Final Review
**Status:** ✅ COMPLETE (after restart)
**Completed:** 2025-01-02 16:00
**Last Updated:** 2025-01-02 16:00

**Stage 6 Summary:**
- Epic smoke testing: ✅ PASSED (after restart)
- QC rounds (3): ✅ ALL PASSED (after restart)
- Epic PR review: ✅ PASSED (after restart)
- Issues found: 2 (both fixed via bug fixes)
- Stage 6 restarts: 1 (after bug fixes)

**Next Stage:** STAGE_7_epic_cleanup_guide.md
**Next Action:** Read STAGE_7_epic_cleanup_guide.md to begin epic cleanup
```

---

## STEP 8: Final Verification & README Update

### Overview

**Objective:** Verify Stage 6c complete, all issues resolved, update epic documentation.

**When to use this step:**
- Step 6 (Epic PR Review) passed (all 11 categories)
- Step 7 (Handle Issues) complete OR skipped (no issues)
- Ready to mark Stage 6 complete

### Step 8.1: Verify All Issues Resolved

**Review Stage 6 documentation to confirm ALL issues resolved:**

**Verification Checklist:**
- [ ] Epic smoke testing passed (all 4 parts) - from STAGE_6a
- [ ] QC Round 1 passed (no integration issues) - from STAGE_6b
- [ ] QC Round 2 passed (no consistency issues) - from STAGE_6b
- [ ] QC Round 3 passed (success criteria met) - from STAGE_6b
- [ ] Epic PR review passed (all 11 categories) - from STAGE_6c Step 6
- [ ] NO pending issues or bug fixes
- [ ] ALL tests passing (100% pass rate)

**How to verify:**

```bash
# 1. Run all tests to confirm 100% pass rate
python tests/run_all_tests.py

# Expected output:
# ============================== 2247 passed in 45.32s ===========================
# Exit code: 0 ✅

# 2. Check EPIC_README.md for pending issues
# Should show: "No pending issues or bug fixes"

# 3. Check epic_lessons_learned.md for unresolved issues
# All issues should have "Status: RESOLVED" or not be listed

# 4. Verify bug fix folders (if any) completed Stage 5c
# bugfix_high_*/README.md should show "Stage 5c: COMPLETE"
```

**If ANY item unchecked:**
- STOP - Stage 6 is NOT complete
- Address remaining issues
- Re-run affected steps
- Do NOT proceed to Step 8.2

**Document verification:**
```markdown
## Stage 6c Final Verification

**Date:** 2025-01-02 16:00

**Verification Results:**
- ✅ Epic smoke testing passed (all 4 parts)
- ✅ QC Round 1 passed (no integration issues)
- ✅ QC Round 2 passed (no consistency issues)
- ✅ QC Round 3 passed (success criteria met 100%)
- ✅ Epic PR review passed (all 11 categories)
- ✅ NO pending issues or bug fixes
- ✅ ALL tests passing (2247/2247 tests, 100% pass rate)

**Result:** Stage 6 verification PASSED - Ready to mark complete
```

### Step 8.2: Update EPIC_README.md Epic Progress Tracker

**Mark Stage 6 complete in EPIC_README.md:**

```markdown
## Epic Progress Tracker

**Stage 1 - Epic Planning:** ✅ COMPLETE
**Stage 2 - Feature Deep Dives:** ✅ COMPLETE
**Stage 3 - Cross-Feature Sanity Check:** ✅ COMPLETE
**Stage 4 - Epic Testing Strategy:** ✅ COMPLETE
**Stage 5 - Feature Implementation:** ✅ COMPLETE
  - Feature 01: ✅ COMPLETE
  - Feature 02: ✅ COMPLETE

**Stage 6 - Epic Final QC:** ✅ COMPLETE
- STAGE_6a (Epic Smoke Testing): ✅ COMPLETE
- STAGE_6b (Epic QC Rounds): ✅ COMPLETE
- STAGE_6c (Epic Final Review): ✅ COMPLETE
- Epic smoke testing passed: ✅
- Epic QC rounds passed: ✅ (Rounds 1, 2, 3)
- Epic PR review passed: ✅ (11 categories)
- End-to-end validation passed: ✅
- Issues found: 2 (both resolved via bug fixes)
- Stage 6 restarts: 1 (after bug fixes)
- Date completed: 2025-01-02

**Stage 7 - Epic Cleanup:** [ ] PENDING
```

### Step 8.3: Update epic_lessons_learned.md

**Add Stage 6c insights to epic_lessons_learned.md:**

```markdown
## Stage 6c Lessons Learned (Epic Final Review)

**Date:** 2025-01-02

**What Went Well:**
- Epic PR review systematic (11 categories covered comprehensively)
- Architectural consistency check caught Manager pattern inconsistency
- Performance category identified N+1 query regression early
- Bug fix workflow smooth (Stage 2 → 5a → 5b → 5c)
- Stage 6 restart after bug fixes ensured quality maintained

**What Could Be Improved:**
- Architectural pattern should be enforced in Stage 2 (spec should mandate Manager pattern)
- Performance baseline should be measured in Stage 1 (not assumed)
- Could have caught architectural inconsistency in Stage 5d (cross-feature alignment)

**Issues Found & Resolved:**
1. **Architectural Inconsistency:** Feature 02 used standalone functions instead of Manager pattern
   - Fixed: Refactored to MatchupManager class
   - Prevention: Add "Architecture Pattern" to Stage 2 spec template
2. **Performance Regression:** N+1 queries in Feature 02 (+400% regression)
   - Fixed: Implemented batch loading for matchup data
   - Prevention: Add performance testing to Stage 5c smoke testing

**Insights for Future Epics:**
- Establish architectural patterns early (Stage 2 deep dives)
- Document patterns in EPIC_README.md for all agents to follow
- Measure performance baseline in Stage 1 (include in epic notes)
- Add "Architecture" section to feature spec.md template
- Review architectural consistency after EACH feature (Stage 5d)

**Guide Improvements Needed:**
- STAGE_2 guide: Add "Architecture Pattern" section to spec template
- STAGE_5c guide: Add performance baseline comparison to smoke testing
- STAGE_5d guide: Add architectural pattern consistency check

**Stage 6c Statistics:**
- Epic PR Review time: 45 minutes
- Issues found: 2 (both high priority)
- Bug fixes created: 2
- Bug fix time: 4 hours total
- Stage 6 restart time: 2 hours
- Total Stage 6 time: 8.5 hours (including restarts)

**Key Takeaway:** Epic-level PR review is CRITICAL for catching architectural inconsistencies that feature-level reviews miss. The 11-category checklist provides comprehensive coverage.
```

### Step 8.4: Update EPIC_README.md Agent Status

**Mark Stage 6c complete and prepare for Stage 7:**

```markdown
## Agent Status

**Last Updated:** 2025-01-02 16:15
**Current Stage:** Stage 6c - Epic Final Review
**Status:** ✅ COMPLETE

**Stage 6 Summary:**
- STAGE_6a (Epic Smoke Testing): ✅ PASSED
- STAGE_6b (Epic QC Rounds): ✅ PASSED (Rounds 1, 2, 3)
- STAGE_6c (Epic Final Review): ✅ PASSED
- Epic PR review: ✅ PASSED (11 categories)
- Issues found: 2 (both fixed via bug fixes)
- Bug fixes completed: 2
- Stage 6 restarts: 1 (after bug fixes)
- All tests passing: ✅ (2247/2247 tests)
- Result: Epic ready for cleanup and move to done/

**Next Stage:** STAGE_7_epic_cleanup_guide.md
**Next Action:** Read STAGE_7_epic_cleanup_guide.md to begin final epic cleanup
```

### Step 8.5: Completion Indicator

**Stage 6c is COMPLETE when ALL of these are true:**

- ✅ All 3 steps finished (6, 7, 8)
- ✅ Epic PR review passed (all 11 categories)
- ✅ All issues resolved (bug fixes complete OR no issues found)
- ✅ No pending issues or bug fixes
- ✅ EPIC_README.md Epic Progress Tracker updated (Stage 6 marked complete)
- ✅ epic_lessons_learned.md updated with Stage 6c insights
- ✅ EPIC_README.md Agent Status shows Stage 6c complete
- ✅ All tests passing (100% pass rate)
- ✅ Ready to proceed to Stage 7

**If ANY item not complete:**
- STOP - Do not proceed to Stage 7
- Complete missing items
- Re-verify all completion criteria

**When ALL items complete:**
- Stage 6 is COMPLETE
- Proceed to Stage 7 (Epic Cleanup)
- Read STAGE_7_epic_cleanup_guide.md

---

## Re-Reading Checkpoints

**You MUST re-read this guide when:**

### 1. After Session Compaction
- Conversation compacted while in Stage 6c
- Re-read to restore context
- Check EPIC_README.md Agent Status to see which step you're on
- Continue from documented checkpoint

### 2. After Creating Bug Fixes
- Bug fixes created during Step 7
- Re-read "STEP 7: Handle Issues" section
- Remember: MUST RESTART Stage 6 after bug fixes (from STAGE_6a)
- Re-read STAGE_6a and STAGE_6b guides for restart

### 3. After Extended Break (>24 hours)
- Returning to epic after break
- Re-read guide to refresh requirements
- Verify prerequisites still met (tests passing, no new issues)

### 4. When Encountering Confusion
- Unsure about next step
- Re-read workflow overview and current step
- Check EPIC_README.md for current status

### 5. Before Starting Epic PR Review (Step 6)
- Re-read all 11 category descriptions
- Refresh focus areas for each category
- Ensure thorough coverage (don't rush)

**Re-Reading Protocol:**
1. Use Read tool to load ENTIRE guide
2. Find current step in EPIC_README.md Agent Status
3. Read "Workflow Overview" section
4. Read current step's detailed workflow
5. Proceed with renewed understanding

---

## Completion Criteria

**Stage 6c is COMPLETE when ALL of the following are true:**

### Epic PR Review (Step 6)
- [ ] All 11 categories reviewed: ✅ PASSED
  - [ ] 1. Correctness (Epic Level): ✅ PASS
  - [ ] 2. Code Quality (Epic Level): ✅ PASS
  - [ ] 3. Comments & Documentation (Epic Level): ✅ PASS
  - [ ] 4. Code Organization & Refactoring (Epic Level): ✅ PASS
  - [ ] 5. Testing (Epic Level): ✅ PASS
  - [ ] 6. Security (Epic Level): ✅ PASS
  - [ ] 7. Performance (Epic Level): ✅ PASS
  - [ ] 8. Error Handling (Epic Level): ✅ PASS
  - [ ] 9. Architecture (Epic Level - CRITICAL): ✅ PASS
  - [ ] 10. Backwards Compatibility (Epic Level): ✅ PASS
  - [ ] 11. Scope & Changes (Epic Level): ✅ PASS
- [ ] PR review results documented in epic_lessons_learned.md

### Handle Issues (Step 7 - if applicable)
- [ ] All issues documented (if any found)
- [ ] Bug fixes created for all high/medium priority issues (if any)
- [ ] Bug fixes completed Stage 5c (if any created)
- [ ] Stage 6 RESTARTED after bug fixes (if any created)
- [ ] All steps re-run and passed after restart

### Final Verification (Step 8)
- [ ] All issues resolved (no pending issues or bug fixes)
- [ ] All unit tests passing (100% - 2247/2247 tests)
- [ ] EPIC_README.md Epic Progress Tracker updated (Stage 6 marked complete)
- [ ] epic_lessons_learned.md updated with Stage 6c insights
- [ ] EPIC_README.md Agent Status shows Stage 6c complete

### Overall Stage 6 Completion
- [ ] STAGE_6a complete (Epic Smoke Testing passed)
- [ ] STAGE_6b complete (QC Rounds 1, 2, 3 passed)
- [ ] STAGE_6c complete (Epic PR Review passed, issues resolved)
- [ ] Original epic goals validated and achieved (from STAGE_6b QC Round 3)
- [ ] Ready to proceed to Stage 7

**DO NOT proceed to Stage 7 until ALL completion criteria are met.**

---

## Common Mistakes to Avoid

### ❌ MISTAKE 1: "Repeating feature-level PR review at epic level"

**Why this is wrong:**
- Stage 5c already did feature-level PR review for each feature
- Stage 6c focuses on EPIC-WIDE concerns (cross-feature impacts)
- Repeating feature-level checks wastes time

**What to do instead:**
- ✅ Focus on epic-wide architectural consistency
- ✅ Review cross-feature impacts (not individual features)
- ✅ Validate design patterns applied consistently
- ✅ Check for duplicated code BETWEEN features (not within)

**Example:**
```
BAD: Reviewing Feature 01's code quality in isolation
GOOD: Comparing code quality ACROSS all features (consistency check)

BAD: Checking if Feature 01 has unit tests
GOOD: Checking if epic-level integration tests exist (cross-feature scenarios)
```

---

### ❌ MISTAKE 2: "Fixing issues inline and continuing Stage 6"

**Why this is wrong:**
- Bug fixes may affect areas already checked in Stage 6
- Cannot assume previous QC results still valid
- Partial Stage 6 completion creates gaps in validation

**What to do instead:**
- ✅ Document ALL issues in epic_lessons_learned.md
- ✅ Create bug fixes using bug fix workflow (Stage 2 → 5a → 5b → 5c)
- ✅ COMPLETELY RESTART Stage 6 after fixes (from STAGE_6a)
- ✅ Re-run ALL steps (smoke testing, QC 1-3, PR review)

**Example:**
```
BAD:
- Find architectural issue in Step 6.9
- Fix it with quick code change
- Continue to Step 8 (Final Verification)

GOOD:
- Find architectural issue in Step 6.9
- Document in epic_lessons_learned.md
- Create bugfix_high_architecture_inconsistency/
- Run bug fix through Stage 2 → 5a → 5b → 5c
- RESTART Stage 6 from STAGE_6a (smoke testing)
- Re-run STAGE_6a, 6b, 6c (all steps)
- Only then proceed to Stage 7
```

---

### ❌ MISTAKE 3: "Skipping Architecture category review"

**Why this is wrong:**
- Architecture (Step 6.9) is the MOST IMPORTANT category for epic-level review
- Architectural inconsistencies cause long-term maintainability issues
- Missing this check means shipping brittle epic

**What to do instead:**
- ✅ Spend EXTRA time on Architecture category (Step 6.9)
- ✅ Verify design patterns consistent across ALL features
- ✅ Check for architectural inconsistencies (Manager vs functions, classes vs modules)
- ✅ Validate interfaces between features are clean

**Example:**
```
BAD:
✅ Correctness: PASS
✅ Code Quality: PASS
✅ Architecture: PASS (didn't check, assumed consistent)

GOOD:
✅ Correctness: PASS (verified cross-feature workflows)
✅ Code Quality: PASS (checked consistency across features)
✅ Architecture: PASS (verified Manager pattern used in ALL features)
  - Feature 01: ADPManager ✅
  - Feature 02: MatchupManager ✅
  - Feature 03: PerformanceTracker ✅
  - Design pattern: Manager pattern used consistently ✅
```

---

### ❌ MISTAKE 4: "Comparing to specs instead of original epic request"

**Why this is wrong:**
- Specs evolved during implementation (may have scope creep)
- Specs may have deviated from user's original vision
- Step 6.11 (Scope & Changes) validates against USER'S GOALS, not intermediate specs

**What to do instead:**
- ✅ Re-read ORIGINAL {epic_name}.txt file
- ✅ Validate against user's stated goals (from epic notes)
- ✅ Verify expected outcomes delivered (from user's perspective)
- ✅ Check for scope creep (features not in original request)

**Example:**
```
BAD:
- Check if Feature 01 matches feature_01/spec.md ✅
- Mark Scope & Changes as PASS

GOOD:
- Re-read integrate_new_player_data_into_simulation.txt
- User requested: "Integrate ADP data" ✅
- User requested: "Add matchup projections" ✅
- User requested: "Track performance" ✅
- Epic delivered all 3 ✅
- No undocumented features added ✅
- Mark Scope & Changes as PASS
```

---

### ❌ MISTAKE 5: "Accepting low priority issues instead of creating bug fixes"

**Why this is wrong:**
- "Low priority" issues accumulate and degrade epic quality
- Architectural inconsistencies labeled "low" are often HIGH impact
- Deferring issues means they may never get fixed

**What to do instead:**
- ✅ Use priority determination correctly:
  - **HIGH:** Breaks functionality, security, architecture, performance >100% regression
  - **MEDIUM:** Affects quality (consistency, error messages, minor performance)
  - **LOW:** Cosmetic only (comments, variable names)
- ✅ Create bug fixes for HIGH and MEDIUM issues
- ✅ Only defer LOW issues (truly cosmetic)

**Example:**
```
BAD:
Issue: Feature 01 uses Manager pattern, Feature 02 uses functions
Priority: low (it works, just inconsistent)
Action: Document, don't fix

GOOD:
Issue: Feature 01 uses Manager pattern, Feature 02 uses functions
Priority: HIGH (architectural inconsistency, maintainability impact)
Action: Create bugfix_high_architecture_inconsistency
```

---

### ❌ MISTAKE 6: "Not documenting PR review results"

**Why this is wrong:**
- Future agents can't see what was reviewed
- Can't prove epic was thoroughly reviewed
- Lessons learned lost (can't improve process)

**What to do instead:**
- ✅ Document PR review results in epic_lessons_learned.md (Step 6.12)
- ✅ Include: Date, reviewer, epic name, all 11 categories, status, notes
- ✅ If issues found: Document issues, bug fixes created, restart log
- ✅ Update EPIC_README.md with review completion

**Example:**
```
BAD:
- Complete PR review mentally
- Mark Step 6 as complete
- Proceed to Step 8

GOOD:
- Complete PR review (all 11 categories)
- Document results in epic_lessons_learned.md:
  ## Stage 6c - Epic PR Review (11 Categories)
  **Date:** 2025-01-02
  **Overall Status:** ✅ APPROVED
  **Issues Found:** 0
- Update EPIC_README.md: "Epic PR review: ✅ PASSED"
- Proceed to Step 8
```

---

### ❌ MISTAKE 7: "Proceeding to Stage 7 with pending issues"

**Why this is wrong:**
- Stage 7 is final cleanup (commits, merge to main, move to done/)
- Cannot commit epic with known issues
- User will find issues after "completion"

**What to do instead:**
- ✅ Verify NO pending issues before Step 8 (Final Verification)
- ✅ All bug fixes must be COMPLETE (Stage 5c)
- ✅ Stage 6 must be RESTARTED after bug fixes
- ✅ Only proceed to Stage 7 when verification checklist 100% complete

**Example:**
```
BAD:
Step 8.1: Verification Checklist
- ✅ Epic smoke testing passed
- ✅ QC rounds passed
- ✅ Epic PR review passed
- ⚠️ 1 pending bug fix (bugfix_high_performance - Stage 5b)
- ✅ Tests passing
→ Proceed to Stage 7 anyway

GOOD:
Step 8.1: Verification Checklist
- ✅ Epic smoke testing passed
- ✅ QC rounds passed
- ✅ Epic PR review passed
- ⚠️ 1 pending bug fix (bugfix_high_performance - Stage 5b)
→ STOP - Cannot proceed
→ Complete bug fix (finish Stage 5c)
→ RESTART Stage 6 from STAGE_6a
→ Re-run all steps
→ Re-verify checklist (all items ✅)
→ Then proceed to Stage 7
```

---

## Real-World Example

### Example: Epic Final Review for "Improve Draft Helper" Epic

**Context:**
- Epic: Improve Draft Helper
- Features: 3 (ADP Integration, Matchup System, Performance Tracking)
- STAGE_6a complete: Epic smoke testing passed
- STAGE_6b complete: QC Rounds 1, 2, 3 passed
- Now starting STAGE_6c: Epic Final Review

---

**STEP 6: Epic PR Review (11 Categories)**

**Step 6.1: Correctness (Epic Level)**

```python
# Verify cross-feature workflow correctness
from feature_01.adp_manager import ADPManager
from feature_02.matchup_manager import MatchupManager
from league_helper.util.FantasyPlayer import FantasyPlayer

# Test integration correctness
adp_mgr = ADPManager(data_folder=Path("data"))
matchup_mgr = MatchupManager(data_folder=Path("data"))

player = FantasyPlayer("Patrick Mahomes", "QB", 300.0)
adp_mult, adp_rank = adp_mgr.get_adp_data("Patrick Mahomes")
matchup_diff = matchup_mgr.get_matchup_difficulty("Patrick Mahomes", week=5)

final_score = player.score * adp_mult * matchup_diff
# Verify: 300 * 1.2 * 0.9 = 324
assert 320 <= final_score <= 330, "Integration calculation incorrect"
```

**Result:** ✅ PASS (all cross-feature workflows correct)

---

**Step 6.9: Architecture (Epic Level - CRITICAL)**

```python
# Check architectural consistency
# Feature 01:
class ADPManager:  # ✅ Manager pattern
    def __init__(self, data_folder: Path):
        self.data_folder = data_folder

# Feature 02:
def get_matchup_difficulty(player_name: str, week: int) -> float:  # ❌ Standalone function
    # ...

# Feature 03:
class PerformanceTracker:  # ✅ Manager pattern
    def __init__(self, data_folder: Path):
        self.data_folder = data_folder
```

**Result:** ❌ FAIL - Architectural inconsistency

**Issue:** Feature 02 uses standalone functions instead of Manager pattern

---

**Step 6.12: Document PR Review Results**

```markdown
## Stage 6c - Epic PR Review (11 Categories)

**Date:** 2025-01-02
**Reviewer:** Claude Agent
**Epic:** improve_draft_helper

**Review Results:**

| Category | Status | Notes |
|----------|--------|-------|
| 1. Correctness | ✅ PASS | Cross-feature workflows correct |
| 2. Code Quality | ✅ PASS | Consistent quality across features |
| 3. Comments & Docs | ✅ PASS | Epic-level docs complete |
| 4. Organization | ✅ PASS | Consistent structure |
| 5. Testing | ✅ PASS | Epic integration tests exist, 100% pass |
| 6. Security | ✅ PASS | No vulnerabilities |
| 7. Performance | ✅ PASS | 3.2s (acceptable) |
| 8. Error Handling | ✅ PASS | Consistent, graceful degradation |
| 9. Architecture | ❌ FAIL | Feature 02 uses functions instead of Manager pattern |
| 10. Compatibility | ✅ PASS | No breaking changes |
| 11. Scope | ✅ PASS | Matches original request |

**Overall Status:** ❌ REJECTED

**Issues Found:** 1

**Issue 1: Architectural Inconsistency (Category 9: Architecture)**
- Feature 01 and 03 use Manager pattern, Feature 02 uses standalone functions
- Impact: HIGH - Architectural inconsistency
- Fix Required: Refactor Feature 02 to MatchupManager class

**Next Action:** Create bug fix, then RESTART Stage 6
```

---

**STEP 7: Handle Issues**

**Step 7.1: Document Issues**

```markdown
## Stage 6c Issues Found

**Date:** 2025-01-02

**Issue 1: Architectural Inconsistency in Feature 02**
- **Discovered In:** Step 6.9 (Epic PR Review - Architecture)
- **Description:** Feature 02 uses standalone functions, Features 01 and 03 use Manager pattern
- **Impact:** HIGH - Architectural inconsistency makes epic hard to maintain
- **Root Cause:** Different implementation approach for Feature 02
- **Fix Required:** Refactor Feature 02 to MatchupManager class
- **Priority:** high
```

**Step 7.2: Determine Priority**

```markdown
## Issue Prioritization

**HIGH priority (create bug fixes now):**
- Issue 1: Architectural inconsistency → bugfix_high_architecture_inconsistency
```

**Step 7.3: Present to User**

```markdown
I found 1 issue during Stage 6c Epic PR Review that requires a bug fix:

**ISSUE 1: Architectural Inconsistency (HIGH priority)**
- **Problem:** Feature 02 uses standalone functions instead of Manager pattern
- **Impact:** Architectural inconsistency makes epic hard to maintain
- **Fix:** Refactor Feature 02 to MatchupManager class
- **Estimated time:** 2-3 hours (Stage 2 → 5a → 5b → 5c)

After fixing, I'll RESTART Stage 6 from STAGE_6a.

Should I proceed?
```

**Step 7.4: Create Bug Fix**

```
bugfix_high_architecture_inconsistency/
├── notes.txt ("Refactor Feature 02 to Manager pattern")
├── spec.md (bug fix specification)
├── todo.md (refactoring tasks)
├── code_changes.md (actual code changes)
└── lessons_learned.md (what we learned)
```

**Run through:** Stage 2 → 5a → 5b → 5c (bug fix complete)

**Step 7.5: RESTART Stage 6**

```markdown
## Stage 6 Restart Log

**Restart Date:** 2025-01-02
**Reason:** 1 bug fix completed (bugfix_high_architecture_inconsistency)

**Bug Fix:** Refactored Feature 02 to MatchupManager class

**Restart Actions:**
- ✅ Re-ran STAGE_6a: Epic Smoke Testing (all 4 parts) - PASSED
- ✅ Re-ran STAGE_6b: QC Round 1 - PASSED
- ✅ Re-ran STAGE_6b: QC Round 2 - PASSED
- ✅ Re-ran STAGE_6b: QC Round 3 - PASSED
- ✅ Re-ran STAGE_6c: Epic PR Review (all 11 categories) - PASSED
  - Architecture category now PASSED (all features use Manager pattern)

**Result:** Stage 6 complete after restart (no new issues)
```

---

**STEP 8: Final Verification**

**Step 8.1: Verify All Issues Resolved**

```markdown
## Stage 6c Final Verification

**Date:** 2025-01-02 16:00

**Verification Results:**
- ✅ Epic smoke testing passed
- ✅ QC Round 1 passed
- ✅ QC Round 2 passed
- ✅ QC Round 3 passed
- ✅ Epic PR review passed (all 11 categories, including Architecture)
- ✅ NO pending issues or bug fixes
- ✅ ALL tests passing (2247/2247 tests)

**Result:** Stage 6 verification PASSED
```

**Step 8.2: Update EPIC_README.md**

```markdown
## Epic Progress Tracker

**Stage 6 - Epic Final QC:** ✅ COMPLETE
- Epic smoke testing passed: ✅
- Epic QC rounds passed: ✅ (Rounds 1, 2, 3)
- Epic PR review passed: ✅ (11 categories)
- Issues found: 1 (architectural inconsistency - resolved)
- Bug fixes completed: 1
- Stage 6 restarts: 1 (after bug fix)
- Date completed: 2025-01-02
```

**Step 8.3: Update epic_lessons_learned.md**

```markdown
## Stage 6c Lessons Learned (Epic Final Review)

**What Went Well:**
- Architectural consistency check caught Manager pattern inconsistency
- Bug fix workflow smooth (2-3 hours to refactor Feature 02)
- Stage 6 restart ensured quality maintained

**Issues Found & Resolved:**
1. **Architectural Inconsistency:** Feature 02 used standalone functions instead of Manager pattern
   - Fixed: Refactored to MatchupManager class
   - Prevention: Add "Architecture Pattern" to Stage 2 spec template

**Insights for Future Epics:**
- Establish architectural patterns early (Stage 2)
- Document patterns in EPIC_README.md
- Review architectural consistency after EACH feature (Stage 5d)
```

**Step 8.4: Update Agent Status**

```markdown
## Agent Status

**Current Stage:** Stage 6c - Epic Final Review
**Status:** ✅ COMPLETE
**Completed:** 2025-01-02 16:15

**Stage 6 Summary:**
- Epic PR review: ✅ PASSED (11 categories)
- Issues found: 1 (architectural inconsistency - resolved)
- Bug fixes completed: 1
- Stage 6 restarts: 1
- All tests passing: ✅ (2247/2247)

**Next Stage:** STAGE_7_epic_cleanup_guide.md
```

---

## Prerequisites for Next Stage

**Before proceeding to Stage 7 (Epic Cleanup), verify:**

### Stage 6c Completion
- [ ] STEP 6 (Epic PR Review) complete: All 11 categories PASSED
- [ ] STEP 7 (Handle Issues) complete OR skipped (no issues)
- [ ] STEP 8 (Final Verification) complete: All verification items checked

### Overall Stage 6 Completion
- [ ] STAGE_6a complete (Epic Smoke Testing passed)
- [ ] STAGE_6b complete (QC Rounds 1, 2, 3 passed)
- [ ] STAGE_6c complete (Epic PR Review passed, issues resolved)
- [ ] No pending issues or bug fixes
- [ ] All bug fix folders (if any) show Stage 5c complete

### Documentation Complete
- [ ] epic_lessons_learned.md updated with Stage 6c insights
- [ ] EPIC_README.md Epic Progress Tracker shows Stage 6 complete
- [ ] EPIC_README.md Agent Status shows Stage 6c complete
- [ ] PR review results documented

### Quality Gates Passed
- [ ] All unit tests passing (100% - 2247/2247 tests)
- [ ] Original epic goals validated (from STAGE_6b QC Round 3)
- [ ] Epic success criteria met
- [ ] End-to-end workflows validated

**Only proceed to Stage 7 when ALL items are checked.**

**Next stage:** STAGE_7_epic_cleanup_guide.md
**Next action:** Read STAGE_7_epic_cleanup_guide.md to begin epic cleanup

---

## Summary

**Stage 6c - Epic Final Review is the final validation before epic completion:**

**Key Activities:**
1. **Epic PR Review (Step 6):** Apply 11-category checklist to epic-wide changes
   - Focus: Architectural consistency, cross-feature impacts, epic scope
   - Critical category: Architecture (Step 6.9)
   - Document results in epic_lessons_learned.md

2. **Handle Issues (Step 7):** Create bug fixes for any discovered issues
   - Document all issues comprehensively
   - Create bug fixes using bug fix workflow
   - RESTART Stage 6 from STAGE_6a after fixes

3. **Final Verification (Step 8):** Confirm Stage 6 complete
   - Verify all issues resolved
   - Update EPIC_README.md (Epic Progress Tracker, Agent Status)
   - Update epic_lessons_learned.md with insights

**Critical Distinctions:**
- **Feature-level PR review (Stage 5c):** Reviews individual features in isolation
- **Epic-level PR review (Stage 6c):** Reviews cross-feature consistency, architectural cohesion, epic scope

**Success Criteria:**
- Epic PR review passed (all 11 categories)
- All issues resolved (bug fixes complete OR no issues)
- No pending issues or bug fixes
- All tests passing (100%)
- Original epic goals achieved
- Ready to proceed to Stage 7

**Common Pitfalls:**
- Repeating feature-level review instead of epic-level
- Fixing issues inline instead of using bug fix workflow
- Skipping Architecture category review (most important)
- Comparing to specs instead of original epic request
- Accepting issues instead of creating bug fixes
- Not documenting PR review results
- Proceeding to Stage 7 with pending issues

**Next Stage:** STAGE_7_epic_cleanup_guide.md - Final commits, merge to main, move epic to done/

**Remember:** Stage 6c is the LAST CHANCE to catch epic-level issues before shipping. Thoroughness here prevents post-completion rework and ensures epic delivers on user's vision.

---

**END OF STAGE 6c GUIDE**
