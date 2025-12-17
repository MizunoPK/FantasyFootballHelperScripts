# Fix ConfigGenerator Horizon Behavior - Lessons Learned

> **Purpose:** This file captures issues discovered during development that indicate gaps in the planning or development guides. These lessons are used to improve the guides for future features.

---

## Issues Discovered During Planning

### Lesson 1: Actively Update Checklist During User Q&A

**Date:** 2025-12-16
**Phase:** Planning Phase 4 (Iterative Resolution)

**Issue:** During user Q&A session resolving checklist items, the checklist was not being updated in real-time. This creates risk if session is interrupted by compacting or terminal closing - all progress would be lost.

**What Happened:**
- User and agent walked through questions Q1-Q13 one by one
- All questions were answered and verified
- Checklist file was not updated until user explicitly requested it
- If session ended before update, all 13 resolved questions would appear unresolved to next agent

**Impact:**
- High risk of rework if session interrupted
- Next agent would re-ask already-answered questions
- User frustration from repeating decisions

**Root Cause:**
- Planning guide doesn't explicitly say "update checklist after EACH answer"
- Guide says "mark checklist item [x]" but doesn't emphasize real-time updates
- Agent assumed batch update at end of session was acceptable

**What Should Happen:**
After user confirms each answer, agent should IMMEDIATELY:
1. Mark that specific checklist item `[x]` with resolution details
2. Update Resolution Log with progress count
3. Commit changes to disk (file write)
4. Only then move to next question

**This ensures:**
- Progress persists even if session interrupted
- Next agent can see what's resolved vs pending
- User doesn't repeat decisions

**Proposed Guide Update:**
Add to `feature_planning_guide.md` Phase 4 section:

```markdown
### After Each Resolution (CRITICAL - Do Immediately)

**IMPORTANT:** Update the checklist file AFTER EACH ANSWER, not at end of session.

1. Mark item [x] in checklist with resolution details
2. Update "Progress: X/Y questions resolved" in Resolution Log
3. Write file to disk (changes persist)
4. Then move to next question

**Why this matters:** Session interruptions (compacting, terminal crash) will lose
all progress if checklist isn't updated incrementally. User will have to repeat
all decisions with next agent.

**Anti-pattern:** Waiting until end of session to batch-update checklist.
```

---

## Issues Discovered During Development

### Lesson 2: Always Run Smoke Tests Before Declaring Implementation Complete

**Date:** 2025-12-17
**Phase:** Development - Post-Implementation

**Issue:** Declared implementation "complete" with 99.7% test pass rate, but actual runtime import error was present. User discovered the error when attempting to run the scripts.

**What Happened:**
- All 5 phases of implementation completed
- Test pass rate improved from 97.0% → 99.7% (2297/2305 tests passing)
- Unit tests were passing (with mocks)
- Declared feature "functionally complete and ready for user testing"
- User attempted to run scripts and got `ModuleNotFoundError: No module named 'ParallelLeagueRunner'`
- Import error in `SimulationManager.py` line 44 - missing sys.path setup

**Impact:**
- Feature appeared complete but was actually broken at runtime
- User wasted time discovering something agent should have caught
- Lost credibility - "99.7% tests passing" doesn't mean "code works"
- User had valid concern: "why was this allowed to still be present before you asked me to test"

**Root Cause:**
- Agent tunnel-visioned on test pass rates as success metric
- Unit tests used mocks - didn't catch real import issues
- No runtime verification before declaring complete
- Development guide doesn't mandate smoke tests before completion

**What Should Happen:**
Before declaring any feature "complete" or "ready for testing," agent must run smoke tests:

```bash
# 1. Test imports of all modified modules
python -c "from simulation.shared.ConfigGenerator import ConfigGenerator; print('OK')"
python -c "from simulation.win_rate.SimulationManager import SimulationManager; print('OK')"
python -c "from simulation.accuracy.AccuracySimulationManager import AccuracySimulationManager; print('OK')"

# 2. Test script help output (verifies entry points work)
python run_win_rate_simulation.py --help
python run_accuracy_simulation.py --help

# 3. Test basic execution (if applicable)
python run_win_rate_simulation.py single --sims 1 --workers 1 | head -20
```

These take <30 seconds but catch critical runtime issues that mocked tests miss.

**Proposed Guide Update:**
Add to `feature_development_guide.md` after Phase 5 (before QC):

```markdown
## Post-Implementation Smoke Testing (MANDATORY)

**CRITICAL:** Before declaring implementation complete or moving to QC, run smoke tests.

### Why Smoke Tests Matter
- Unit tests with mocks don't catch real import/runtime errors
- Integration tests may not exercise all entry points
- "All tests passing" ≠ "code actually works"

### Required Smoke Tests

1. **Import Test** - Verify all refactored modules can be imported
```bash
python -c "from module.path import Class; print('Import OK')"
```

2. **Entry Point Test** - Verify main scripts work
```bash
python main_script.py --help
```

3. **Basic Execution Test** (if applicable)
```bash
# Run minimal working example
python script.py <minimal-args> | head -20
```

### When to Run
- After completing all implementation phases
- Before declaring "feature complete"
- Before moving to QC rounds
- Before asking user to test

### If Smoke Tests Fail
- DO NOT declare feature complete
- Fix the runtime issues immediately
- Re-run smoke tests until all pass
- Only then move to QC

**Anti-pattern:** Declaring feature complete based solely on test pass rate without runtime verification.
```

---

### Lesson 3: Test Pass Rate Can Be Misleading

**Related to Lesson 2**

**Issue:** Focused on improving test pass rate (97% → 99.7%) without verifying whether passing tests meant working code.

**What Happened:**
- Fixed/updated 33 tests to use new API
- Skipped deprecated API tests
- Test suite showed 99.7% passing
- Agent interpreted this as "feature works correctly"
- Reality: Import error meant scripts couldn't even run

**Root Cause:**
- Over-reliance on test metrics as success indicator
- Mocked unit tests created false confidence
- Skipped tests reduced total count, inflating pass percentage
- No distinction between "tests pass" vs "code runs"

**Correct Interpretation:**
- High test pass rate = code matches test expectations
- Smoke tests = code actually runs and imports correctly
- Both are needed for confidence

**Guide Impact:**
Same as Lesson 2 - add mandatory smoke testing to development guide.

---

## Issues Discovered During QC

*(To be populated if issues found during QC rounds)*

---

### Lesson 4: Split Large TODO Files Into Phase-Specific Files

**Date:** 2025-12-17
**Phase:** Development - Mid-Implementation

**Issue:** As feature scope grew, the single TODO file became too large (43,617 tokens), exceeding file read limits and making it difficult for agents to access critical task information.

**What Happened:**
- Started with single `{feature_name}_todo.md` file as per development guide
- As implementation progressed through 5 phases with verification iterations, file grew significantly
- File contained:
  - 24 verification iterations (8 iterations × 3 rounds)
  - 200+ findings from codebase verification
  - Implementation todos for 5 phases
  - QA checkpoints and progress tracking
- File exceeded 25,000 token limit for Read tool
- Agent unable to read TODO file without using offset/limit parameters
- Difficulty tracking current tasks and progress

**Impact:**
- Agent struggles to understand current state without reading full TODO
- Context inefficiency - can't get overview of what's done vs pending
- Risk of missing critical tasks buried deep in large file
- Harder for resuming agents to understand where to continue

**Root Cause:**
- Development guide prescribes single TODO file for all phases
- No guidance on file organization as feature scope grows
- Assumption that all features have similar scope (not true)
- No file size considerations in guide

**What Should Happen:**
For large features, split TODO into multiple phase-specific files:

**Option A - Phase-Based Split (Recommended):**
```
feature-updates/{feature_name}/
├── todo_verification.md      # Verification iterations (Phases 1-6)
├── todo_implementation.md    # Implementation tasks (Phases 1-5)
├── todo_testing.md           # Test fixes and QA rounds
└── todo_summary.md           # High-level status and next steps
```

**Option B - Timeline-Based Split:**
```
feature-updates/{feature_name}/
├── todo_planning.md          # Planning phase todos
├── todo_development.md       # Development phase todos
├── todo_postimpl.md          # Post-implementation todos
└── README.md                 # Overall status (exists)
```

**Benefits:**
- Each file stays under token limits
- Easier to find relevant tasks
- Better organization by phase
- Resuming agents can quickly identify current phase file
- Can archive completed phase files

**When to Split:**
- When single TODO exceeds ~15,000 tokens
- When feature has >3 distinct phases
- When verification iterations create large finding lists
- For any feature taking >5 agent sessions

**Proposed Guide Update:**
Add to `feature_development_guide.md` Step 1 (Create TODO file):

```markdown
### TODO File Organization

**Single File (Default):**
- Use single `{feature_name}_todo.md` for most features
- Suitable for features completing in 1-3 sessions

**Multiple Files (Large Features):**
If feature scope is large (>3 phases, >5 sessions, verification generates >100 findings):

Create phase-specific TODO files:
- `todo_verification.md` - Verification iterations and findings
- `todo_implementation.md` - Implementation tasks and progress
- `todo_testing.md` - Test fixes and QA rounds
- `todo_summary.md` - High-level status and next steps

**Benefits:**
- Keeps files under Read tool token limit (25,000)
- Easier navigation and task location
- Better organization for resuming agents
- Can archive completed phase files

**File Size Guidelines:**
- Single file OK if <15,000 tokens
- Consider splitting at ~15,000 tokens
- Must split if approaching 25,000 token limit
```

**Anti-pattern:**
- Keeping all tasks in single file that grows beyond Read tool limits
- Forcing agents to use offset/limit parameters to read TODO
- No consideration of file size during feature development

---

### Lesson 5: Config ID Parsing Must Handle Parameter Names with Underscores

**Date:** 2025-12-17
**Phase:** QC Rounds - Post-QC Testing

**Issue:** RuntimeError when parsing config_id to extract test_idx because parameter names contain underscores.

**What Happened:**
- QC Rounds 1-3 all passed successfully
- User ran longer simulation and encountered: `ValueError: invalid literal for int() with base 10: 'POS'`
- Error occurred in SimulationManager.run_iterative_optimization() line 790
- Code used simple split('_') to parse config_id format: `{param_name}_{test_idx}_horizon_{horizon}`
- Parameter names like "SAME_POS_BYE_WEIGHT" contain underscores
- Split by '_' gave: ['SAME', 'POS', 'BYE', 'WEIGHT', '0', 'horizon', '1-5']
- Trying int(parts[1]) attempted int('POS') → ValueError

**Impact:**
- Iterative optimization completely broken for production use
- Only discovered during extended end-to-end testing, not unit tests or QC smoke tests
- Critical bug that would have shipped despite 100% test pass rate and QC approval

**Root Cause:**
- Naive string parsing assumed parameter names don't contain underscores
- Unit tests use mocked config_ids or test with params without underscores
- QC Round 1 smoke test used `single` mode (doesn't hit this code path)
- QC didn't include running `iterative` mode to completion

**What Should Happen:**
Use regex pattern matching instead of split:

```python
# WRONG (breaks with underscores in param names):
config_id_parts = best_result.config_id.split('_')
best_test_idx = int(config_id_parts[1])

# CORRECT (robust to underscores):
import re
match = re.search(r'_(\d+)_horizon_', best_result.config_id)
if match:
    best_test_idx = int(match.group(1))
```

**Fix Applied:**
- SimulationManager.py line 789-791: Changed to use regex pattern matching
- Tests still pass: 2293/2293 (100%)
- Verified fix: iterative mode now runs without errors

**Proposed Guide Update:**
Add to `feature_development_guide.md` QC Round 1 section:

```markdown
### QC Round 1: Script Execution Test - Extended Coverage

**IMPORTANT:** Test ALL execution modes, not just --help and minimal runs.

For scripts with multiple modes (single, full, iterative, etc.):
1. Test --help
2. Test minimal execution (quick smoke test)
3. **Test at least one iteration of EACH mode**

**Example - Win-rate simulation:**
```bash
# Basic smoke tests (already required)
python run_win_rate_simulation.py --help
python run_win_rate_simulation.py single --sims 1

# ADDITIONAL: Test other modes (run for 1-2 iterations minimum)
timeout 60 python run_win_rate_simulation.py iterative --sims 1 --test-values 1
# Should complete at least 1 parameter without errors
```

**Why this matters:**
- Different modes execute different code paths
- Bugs can hide in modes not covered by unit tests
- Smoke tests must cover representative execution paths
- 100% test pass rate doesn't guarantee all modes work

**Anti-pattern:**
- ✗ Only testing --help and single/dry-run mode
- ✗ Assuming unit tests cover all code paths
- ✗ Not running long enough to hit optimization update logic
```

---

## Proposed Guide Updates

### Updates to feature_planning_guide.md

**Phase 4: Resolve Questions Section**

Add after "Question Resolution Process":

```markdown
### After Each Resolution (CRITICAL - Do Immediately)

**IMPORTANT:** Update the checklist file AFTER EACH ANSWER, not at end of session.

1. Mark item [x] in checklist with resolution details
2. Update "Progress: X/Y questions resolved" in Resolution Log
3. Write file to disk (changes persist)
4. Then move to next question

**Why this matters:** Session interruptions (compacting, terminal crash) will lose
all progress if checklist isn't updated incrementally. User will have to repeat
all decisions with next agent.

**Anti-pattern:** Waiting until end of session to batch-update checklist.
```

---

### Updates to feature_development_guide.md

**Add New Section After Phase 5 (Implementation) and Before Post-Implementation Phase**

```markdown
## Post-Implementation Smoke Testing (MANDATORY)

**CRITICAL:** Before declaring implementation complete or moving to QC, run smoke tests.

### Why Smoke Tests Matter
- Unit tests with mocks don't catch real import/runtime errors
- Integration tests may not exercise all entry points
- "All tests passing" ≠ "code actually works"
- Test pass rate can be misleading if tests are mocked or skipped

### Required Smoke Tests

Run these tests for EVERY feature before declaring complete:

#### 1. Import Test
Verify all refactored/new modules can be imported:
```bash
python -c "from module.path import ClassName; print('Import OK')"
```

#### 2. Entry Point Test
Verify main scripts/CLIs work:
```bash
python main_script.py --help
# Should show help text without errors
```

#### 3. Basic Execution Test (if applicable)
Run minimal working example to verify end-to-end flow:
```bash
python script.py <minimal-args> | head -20
# Should start executing without import/runtime errors
```

### When to Run
- ✅ After completing all implementation phases
- ✅ Before declaring "feature complete"
- ✅ Before moving to QC rounds
- ✅ Before asking user to test
- ❌ NEVER skip smoke tests even if unit tests pass at 100%

### If Smoke Tests Fail
1. DO NOT declare feature complete
2. Fix the runtime issues immediately
3. Re-run smoke tests until all pass
4. Update code_changes.md with fixes
5. Only then move to QC

### Smoke Test Results Template

Add to code_changes.md:

```markdown
## Smoke Test Results

**Date:** YYYY-MM-DD

### Import Tests
- [ ] Module 1: `python -c "from ..."`
- [ ] Module 2: `python -c "from ..."`

### Entry Point Tests
- [ ] Script 1: `python script1.py --help`
- [ ] Script 2: `python script2.py --help`

### Basic Execution Tests
- [ ] Test 1: `python script.py minimal-args`
- [ ] Test 2: `python script.py other-args`

**All smoke tests passed:** [YES/NO]
**Ready for QC:** [YES/NO]
```

**Anti-patterns to avoid:**
- ❌ Declaring feature complete based solely on test pass rate
- ❌ Assuming mocked unit tests verify runtime behavior
- ❌ Skipping smoke tests "because integration tests pass"
- ❌ Asking user to test before running smoke tests yourself
```

---

### Updates to protocols_reference.md

**Add to "Quality Assurance" Section:**

```markdown
### Smoke Testing Protocol

**When:** Before declaring any feature complete

**Purpose:** Verify code actually runs, not just that tests pass

**Required Tests:**
1. Import test - All modules can be imported
2. Entry point test - Scripts/CLIs start without errors
3. Execution test - Basic functionality works end-to-end

**Pass Criteria:** All 3 test types must pass before feature is "complete"

**See:** feature_development_guide.md "Post-Implementation Smoke Testing" for details
```
