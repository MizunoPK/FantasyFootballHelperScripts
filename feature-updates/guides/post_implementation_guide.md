# Post-Implementation Guide

This guide covers quality control, validation, and completion. Use this AFTER implementation is complete.

**Related Files:**
- `implementation_execution_guide.md` - Previous guide (execute TODO)
- `protocols_reference.md` - Detailed protocol definitions
- `templates.md` - File templates

---

## Quick Start (7 Steps)

1. **Run all unit tests** - 100% pass rate required
2. **Execute Requirement Verification Protocol** - Verify every spec line addressed
3. **Execute Smoke Testing Protocol** (MANDATORY) - Import, entry point, execution tests
4. **Complete QC Round 1** - Initial review + script monitoring
5. **Complete QC Round 2** - Deep verification + semantic diff
6. **Complete QC Round 3** - Final skeptical review
7. **Lessons learned and completion** - Review, update guides, move to done/, commit

**Result:** Feature validated and ready for production

**Next Step:** Move folder to `feature-updates/done/` and commit changes

---

## Post-Implementation Phase Quick Reference Checklist

```
┌─────────────────────────────────────────────────────────────────┐
│  POST-IMPLEMENTATION PHASE CHECKLIST                            │
│  Track progress through QC, smoke testing, and completion       │
└─────────────────────────────────────────────────────────────────┘

□ STEP 1: Run All Unit Tests
  □ Execute: python tests/run_all_tests.py
  □ 100% pass rate required
  □ Fix any failures before proceeding

□ STEP 2: Execute Requirement Verification Protocol
  □ Re-read specs.md line by line
  □ Re-read question answers (if exist)
  □ Verify Algorithm Traceability Matrix
  □ Verify Integration Evidence
  □ ⚡ UPDATE README Agent Status: Phase=POST-IMPLEMENTATION

□ STEP 3: Execute Smoke Testing Protocol (MANDATORY)
  □ Part 1: Import Test
    □ Test all module imports
    □ Verify no ImportError or AttributeError
  □ Part 2: Entry Point Test
    □ Test --help displays correctly
    □ Test argument parsing handles errors gracefully
  □ Part 3: Execution Test (30-60 seconds minimum)
    □ Run with real data end-to-end
    □ Verify output values in expected range
    □ Check logs for WARNING/ERROR messages (must be empty)
    □ Verify all expected output components created
    □ Compare to baseline/working reference

□ STEP 4: Quality Control Round 1 (Initial Review)
  □ Code follows project conventions
  □ All files have proper docstrings
  □ Code matches specs structurally
  □ Tests use real objects (not excessive mocking)
  □ Output file tests validate CONTENT
  □ Runner scripts tested with --help and E2E
  □ Test ALL execution modes (not just --help)
  □ Interfaces verified against actual classes
  □ Document findings in code_changes.md
  □ ⚡ UPDATE README Agent Status: Step=QC Round 1 complete

□ STEP 5: Quality Control Round 2 (Deep Verification)
  □ Baseline comparison (if similar feature exists)
  □ Output validation (values in expected range)
  □ No regressions (new feature doesn't break existing)
  □ Log quality (no unexpected WARNING/ERROR)
  □ Semantic diff check (intentional vs accidental changes)
  □ Edge cases handled
  □ Error handling complete
  □ Documentation matches implementation
  □ Document findings in code_changes.md
  □ ⚡ UPDATE README Agent Status: Step=QC Round 2 complete

□ STEP 6: Quality Control Round 3 (Final Skeptical Review)
  □ Re-read specs.md final time
  □ Re-read question answers final time
  □ Re-check Algorithm Traceability Matrix
  □ Re-check Integration Matrix
  □ Re-run smoke test final time
  □ Compare final output to test plan in specs
  □ Review all lessons_learned entries
  □ Final check: Feature actually complete and working?
  □ Document findings in code_changes.md
  □ ⚡ UPDATE README Agent Status: Step=QC Round 3 complete

□ STEP 7: Review Lessons Learned
  □ Read lessons_learned.md
  □ Identify patterns and root causes
  □ Identify guide updates needed
  □ Create guide update recommendations
  □ Present summary to user
  □ Wait for user approval
  □ Apply approved updates to guides

□ STEP 8: Completion Checklist
  □ All unit tests passing (100%)
  □ Smoke testing protocol completed
  □ Requirement Verification Protocol completed
  □ QC Round 1, 2, 3 all completed and passed
  □ All issues fixed and verified
  □ Lessons learned reviewed
  □ Guide updates identified and approved
  □ Approved guide updates applied
  □ code_changes.md complete (all 3 QC rounds)
  □ implementation_checklist.md shows all verified
  □ README.md Agent Status updated to "Complete"

□ STEP 9: Move to Done
  □ Move folder: feature-updates/{name}/ → feature-updates/done/{name}/
  □ ⚡ UPDATE README Agent Status: Phase=COMPLETE

□ STEP 10: Commit Changes
  □ Descriptive commit message with feature summary
  □ Do NOT include "Generated with Claude Code" footer
  □ Verify commit created
  □ Verify all changes included

□ FEATURE COMPLETE
```

**⚡ = Status Update Required**: Update README "Agent Status" section for session continuity.

**QC Pass Criteria:**
- Round 1: <3 critical issues, >80% requirements met
- Round 2: All findings from Round 1 resolved
- Round 3: Zero issues found (skeptical fresh review)

---

## Verify Implementation Complete

```
┌─────────────────────────────────────────────────────────────────┐
│  ⚠️  MANDATORY: VERIFY IMPLEMENTATION COMPLETE BEFORE QC        │
└─────────────────────────────────────────────────────────────────┘
```

**BEFORE starting QC**, verify implementation is 100% complete:

□ All TODO tasks marked `[x]` in `{feature_name}_todo.md`
□ File exists: `{feature_name}_implementation_checklist.md`
□ Implementation checklist shows: "All requirements verified"
□ File exists: `{feature_name}_code_changes.md` with all changes documented
□ All mini-QC checkpoints in TODO show: "PASSED"
□ All unit tests passing: `python tests/run_all_tests.py` exits with code 0
□ No uncommitted code changes (or all changes committed as WIP)
□ README.md Agent Status shows: "Implementation complete - Ready for QC"

**If ANY checkbox is unchecked:**
- ❌ DO NOT start QC
- Return to `implementation_execution_guide.md` to complete implementation
- Fix the incomplete items
- Re-verify this checklist

**If all checkboxes are checked:**
- ✅ Implementation is complete
- ✅ Proceed with this guide (Post-Implementation)
- ✅ Start with "Post-Implementation Phase Quick Reference Checklist" above

---

## Prerequisites Checklist

```
┌─────────────────────────────────────────────────────────────────┐
│  ✓ VERIFY BEFORE STARTING QC                                    │
└─────────────────────────────────────────────────────────────────┘
```

Complete this checklist BEFORE starting post-implementation steps:

| Check | How to Verify | If Failed |
|-------|---------------|-----------|
| All TODO tasks complete | All tasks marked `[x]` | Complete remaining tasks |
| Implementation checklist complete | All requirements checked off | Complete remaining requirements |
| All unit tests pass | `python tests/run_all_tests.py` exits 0 | Fix failing tests |
| All mini-QC checkpoints passed | Check TODO for checkpoint status | Complete failed checkpoints |
| code_changes.md updated | File contains all changes made | Document all changes |
| No uncommitted code changes | `git status` shows clean or staged only | Commit or stash changes |

**Why this matters:** Starting QC with incomplete implementation wastes time.

---

## README Agent Status Requirements (Session Continuity)

```
┌─────────────────────────────────────────────────────────────────┐
│  CRITICAL: README.md Agent Status tracks QC progress            │
└─────────────────────────────────────────────────────────────────┘
```

**Why critical during QC:** QC has 3 mandatory rounds plus smoke testing. Agent Status must track which rounds are complete and what issues remain.

### When to Update

**MANDATORY update points:**
- After Smoke Testing complete
- After QC Round 1 complete
- After QC Round 2 complete
- After QC Round 3 complete
- When issues found (before fixing)
- After all issues fixed

### Template for Post-Implementation Phase

```markdown
## Agent Status

**Last Updated:** {YYYY-MM-DD HH:MM}
**Current Phase:** POST-IMPLEMENTATION
**Current Step:** QC Round X
**Progress:** {Rounds complete}
**Next Action:** {Specific next QC step}
**Blockers:** {Issues or "None"}
**Notes:**
- Smoke Testing: {PASSED/FAILED/Not run}
- QC Round 1: {PASSED/IN PROGRESS/Not started} - X issues found, Y fixed
- QC Round 2: {PASSED/IN PROGRESS/Not started} - X issues found, Y fixed
- QC Round 3: {PASSED/IN PROGRESS/Not started} - X issues found, Y fixed
```

### Good Example

```markdown
## Agent Status

**Last Updated:** 2025-12-24 18:30
**Current Phase:** POST-IMPLEMENTATION
**Current Step:** QC Round 2 - Deep Verification
**Progress:** Smoke test + Round 1 complete, Round 2 in progress
**Next Action:** Complete baseline comparison and semantic diff check for Round 2
**Blockers:** None
**Notes:**
- Smoke Testing: PASSED (all 3 parts)
- QC Round 1: PASSED - 2 minor issues found and fixed
  - Issue 1: Missing docstring in helper method - FIXED
  - Issue 2: Output validation test needed content check - FIXED
- QC Round 2: IN PROGRESS - started 18:15
  - Baseline comparison: Complete (matches win_rate_simulation output format)
  - Semantic diff: In progress
- Tests: 100% pass rate maintained
```

**Red Flags:** No round status, no issue tracking, vague "QC in progress"

---

## CRITICAL RULES - READ BEFORE QC

```
┌─────────────────────────────────────────────────────────────────┐
│  RULES FOR POST-IMPLEMENTATION (Quick Reference)                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. ALL 3 QC rounds are MANDATORY - no skipping                 │
│  2. Smoke testing is MANDATORY - no exceptions                  │
│  3. Test ALL execution modes, not just --help                   │
│  4. Verify output CONTENT, not just file existence              │
│  5. Compare to baseline/similar features                        │
│  6. Check logs for WARNING/ERROR messages                       │
│  7. Fix issues IMMEDIATELY when found                           │
│  8. Document all issues in lessons_learned.md                   │
│  9. Update README Agent Status after each round                 │
│                                                                 │
│  COMMON MISTAKES TO AVOID:                                      │
│  ✗ "Tests pass so I'm done" → Run smoke tests and QC            │
│  ✗ "Just check --help" → Run full E2E with real data            │
│  ✗ "File exists so it's right" → Validate file contents         │
│  ✗ "Skip QC for simple features" → QC is mandatory always       │
│  ✗ "QC Round 1 in background = smoke test" → These are different│
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Critical Warning: Smoke Testing Cannot Be Skipped

```
┌─────────────────────────────────────────────────────────────────┐
│  ⚠️ CRITICAL: SMOKE TESTING CANNOT BE SKIPPED                   │
│                                                                 │
│  LESSON FROM: ranking_accuracy_metrics                         │
│                                                                 │
│  Before declaring any feature complete, you MUST perform       │
│  smoke testing (Step 3 below).                                  │
│                                                                 │
│  COMMON MISTAKE: Starting a script in background during        │
│  QC Round 1 is NOT smoke testing.                              │
│                                                                 │
│  Smoke testing requires:                                       │
│  1. Dedicated execution test phase (not just background)       │
│  2. Verification of actual results (not just "script started") │
│  3. Checking output files contain expected data                │
│  4. End-to-end workflow validation with real data              │
│                                                                 │
│  CONSEQUENCE OF SKIPPING: You will ship broken features.       │
│  All QC can pass while feature is completely non-functional    │
│  due to integration issues, configuration problems, missing    │
│  wiring between components, or data flow breaks.               │
│                                                                 │
│  RULE: If you haven't explicitly run the 3-part smoke testing  │
│  protocol (Import Test, Entry Point Test, Execution Test)      │
│  and verified results, the feature is NOT complete.            │
│  No exceptions.                                                │
└─────────────────────────────────────────────────────────────────┘
```

---

## Common Shortcuts to Avoid (With Consequences)

```
┌─────────────────────────────────────────────────────────────────┐
│  ⚠️  SHORTCUT DETECTION - IF YOU'RE THINKING THIS, STOP        │
└─────────────────────────────────────────────────────────────────┘
```

These are real shortcuts agents have taken during QC. Each leads to shipping broken features:

### Shortcut #1: "Tests Pass = Feature Complete"

❌ **Thought**: "All unit tests pass, feature must be working"

✅ **Reality**: Unit tests don't validate E2E integration or real-world usage

**Consequence**: Ship feature that fails in real usage, discovered by user

**If you think this**: STOP. Run full smoke testing protocol (all 3 parts).

---

### Shortcut #2: "Just Test --help is Enough"

❌ **Thought**: "I'll run --help to verify the script works"

✅ **Reality**: --help tests argument parsing, not functionality

**Consequence**: Feature appears to work but breaks during real execution

**If you think this**: STOP. Run E2E execution test with real data for 30-60 seconds.

---

### Shortcut #3: "Output File Exists = Success"

❌ **Thought**: "File was created, so the feature works correctly"

✅ **Reality**: File existence ≠ correct content. Could be empty or garbage.

**Consequence**: Feature produces invalid output, breaks downstream consumers

**If you think this**: STOP. Open and validate CONTENT of output files.

---

### Shortcut #4: "Skip QC for Simple Features"

❌ **Thought**: "This is a simple feature, doesn't need 3 QC rounds"

✅ **Reality**: Simple features still have integration bugs. QC is always mandatory.

**Consequence**: Ship bugs that QC would have caught

**If you think this**: STOP. Complete ALL 3 QC rounds, every feature, every time.

---

### Shortcut #5: "Background Script Run = Smoke Test"

❌ **Thought**: "I started the script in background during QC Round 1, that counts as smoke test"

✅ **Reality**: Smoke testing requires dedicated validation of results

**Consequence**: Feature broken but QC passes because smoke test was skipped

**If you think this**: STOP. Execute Step 3 (Smoke Testing Protocol) explicitly.

---

### Shortcut #6: "QC Round 1 Found Nothing = Skip Round 2 & 3"

❌ **Thought**: "Round 1 found no issues, I can skip the other rounds"

✅ **Reality**: Each round has different focus. All 3 required.

**Consequence**: Miss issues that only deeper rounds catch

**If you think this**: STOP. Complete Rounds 2 and 3. All rounds are mandatory.

---

### Shortcut #7: "Logs Look Fine = No Need to grep"

❌ **Thought**: "I scrolled through logs, didn't see errors"

✅ **Reality**: Visual scan misses warnings buried in output

**Consequence**: Ship feature with warnings indicating problems

**If you think this**: STOP. Run `grep -i warning` and `grep -i error` on logs.

---

### Shortcut #8: "I'll Fix This Issue Later"

❌ **Thought**: "Found a small issue, I'll document it and fix later"

✅ **Reality**: Later never comes. Issue ships to production.

**Consequence**: Known bugs in production, user discovers them

**If you think this**: STOP. Fix issue NOW before proceeding.

---

### Shortcut #9: "Don't Need Baseline Comparison"

❌ **Thought**: "I don't need to compare to similar existing features"

✅ **Reality**: Baseline comparison catches inconsistencies and regressions

**Consequence**: Feature behaves differently than similar features, confusing UX

**If you think this**: STOP. Find similar feature, compare behavior side-by-side.

---

### Shortcut #10: "Partial Smoke Test is Fine"

❌ **Thought**: "I ran Part 1 (import test), that's good enough"

✅ **Reality**: Import working ≠ execution working. Need all 3 parts.

**Consequence**: Feature imports but fails during execution

**If you think this**: STOP. Complete ALL 3 smoke test parts (import, entry point, execution).

---

**REMEMBER**: Post-implementation shortcuts = shipping broken features to users.

---

## Step 1: Run All Unit Tests

```bash
python tests/run_all_tests.py
```

**Requirements:**
- 100% pass rate required
- If any tests fail, FIX THEM before proceeding
- Do not proceed to Step 2 until all tests pass

**If tests fail:**
1. Read the error messages carefully
2. Determine if the test is wrong or the code is wrong
3. Fix the issue
4. Re-run all tests
5. Only proceed when all tests pass

---

## Step 2: Execute Requirement Verification Protocol

```
╔═════════════════════════════════════════════════════════════════╗
║  🛑 CRITICAL: NO PARTIAL OR INCOMPLETE WORK ACCEPTED           ║
╠═════════════════════════════════════════════════════════════════╣
║                                                                 ║
║  ALL requirements from specs.md MUST be fully implemented.     ║
║                                                                 ║
║  There is NO "acceptable partial" category.                    ║
║  There is NO "placeholder for future work" category.           ║
║  There is NO "structure correct, data pending" category.       ║
║                                                                 ║
║  EXAMPLES OF UNACCEPTABLE "PARTIAL" WORK:                      ║
║  ❌ "Stat arrays created but filled with zeros"                ║
║  ❌ "File structure correct but data extraction pending"       ║
║  ❌ "Method exists but returns placeholder values"             ║
║  ❌ "Feature works but core data is wrong/missing"             ║
║                                                                 ║
║  IF ANY REQUIREMENT IS NOT FULLY IMPLEMENTED:                  ║
║  → Feature is INCOMPLETE                                       ║
║  → QC FAILS immediately                                        ║
║  → Return to implementation phase                              ║
║  → Do not proceed to next QC round                             ║
║                                                                 ║
║  RULE: If the feature cannot achieve its PRIMARY USE CASE      ║
║  with the current implementation, it is INCOMPLETE.            ║
║                                                                 ║
║  Example from real failure:                                    ║
║  - Position JSON files created ✓                               ║
║  - File structure correct ✓                                    ║
║  - All stat arrays filled with zeros ✗                         ║
║  - Result: Feature is USELESS (cannot view player stats)       ║
║  - This should have FAILED QC, not passed as "partial"         ║
║                                                                 ║
║  VERIFICATION QUESTION:                                        ║
║  "Can a user achieve the feature's primary purpose with        ║
║   this implementation?"                                        ║
║                                                                 ║
║  If answer is NO → Feature is INCOMPLETE → QC FAILS            ║
║                                                                 ║
╚═════════════════════════════════════════════════════════════════╝
```

See `protocols_reference.md` → Requirement Verification Protocol for detailed steps.

**Quick Summary:**

1. **Re-read specs.md line by line**
   - For each requirement, verify it was implemented
   - Check implementation against spec exactly

2. **Re-read question answers** (if questions file exists)
   - For each answer, verify the decision was implemented correctly

3. **Verify Algorithm Traceability Matrix**
   - For each algorithm in specs, verify code matches exactly
   - Compare logic: if spec says "if X then A, else B", code must do same

4. **Verify Integration Evidence**
   - For each new method, verify it's called from entry point
   - Trace execution path from CLI → output

**Output:** Verification report confirming all requirements addressed.

---

## Step 3: Execute Smoke Testing Protocol (MANDATORY - CRITICAL GATE)

**CRITICAL:** Smoke testing is the FINAL validation before feature completion. Unit tests alone are NOT sufficient.

### Why Smoke Testing Is Critical

**Real-world evidence:** In the accuracy simulation feature, smoke testing discovered **10 critical bugs** that passed 2296 unit tests (100% pass rate):
- Type mismatches between modules
- Import path errors
- Data structure assumptions
- API interface mismatches
- Method name errors

**All 10 bugs were found ONLY during smoke testing** - unit tests passed perfectly.

---

### ⚠️ CRITICAL LESSON: 100% Passing Unit Tests DOES NOT Guarantee Correct Behavior

**Real-world case study (Historical Data Fetcher feature, 2025-12-26):**

**Situation:**
- ✅ All 2,369 unit tests passed (100%)
- ✅ All integration tests passed
- ✅ All mini-QC checkpoints passed
- ❌ **Smoke testing revealed CRITICAL bug: All output files missing 80% of required data**

**The Problem:**
- JSON files had perfect structure (all field names, correct array lengths, correct types)
- JSON files were MISSING all position-specific statistics (passing, rushing, receiving, kicking, defense)
- This was a complete **SPEC VIOLATION** that would cause silent data quality failure in production
- Users would get files that LOOK correct but contain WRONG DATA

**Root Cause: Mock Brittleness**

Tests used mocks that returned the wrong structure:
```python
# Mock returned (what test expected):
mock.return_value = {'passing': {'completions': [...], 'attempts': [...]}}

# Real method returned (actual format):
return {'completions': [...], 'attempts': [...]}  # Flat dict, not nested!

# Test checked:
if 'passing' in stats:  # PASSED with mock, FAILED with real data
```

**Why Unit Tests Passed:**
- Mocks returned what the test EXPECTED
- Test verified the mock matched expectations
- Real integration never tested until smoke test

**Key Insight: Mocks test YOUR expectations, not REALITY**

### What Smoke Testing Catches That Unit Tests Miss

1. **Mock assumption failures** - Mocks can have wrong structure/format
2. **Data quality issues** - Wrong data (not just missing fields)
3. **Integration problems** - Real method calls reveal incompatibilities
4. **Silent failures** - Code runs without errors but produces incorrect output
5. **Structural mismatches** - Bridge adapters, wrappers assume wrong formats

### The Bottom Line

**DO NOT SKIP SMOKE TESTING** - It is the ONLY way to verify real-world behavior with actual execution.

**Required approach:**
1. ✅ Write comprehensive unit tests (catch logic bugs)
2. ✅ Write integration tests (catch module interaction bugs)
3. ✅ **EXECUTE SMOKE TESTS WITH REAL DATA** (catch everything else)

All three are mandatory. Unit tests alone will miss critical production failures.

---

### The 3-Part Smoke Testing Protocol

#### Part 1: Import Test

**Purpose:** Verify all modules import successfully without errors

```bash
# For new module
python -c "import path.to.new.module"

# For modified modules
python -c "import existing.module"

# For runner scripts
python run_feature.py --version  # or similar non-destructive command
```

**Expected:** No ImportError, no AttributeError, clean exit

**If import fails:**
1. Read the error message
2. Fix the import issue (missing dependency, circular import, etc.)
3. Re-run import test
4. Only proceed when imports work

#### Part 2: Entry Point Test

**Purpose:** Verify script starts without immediate crashes

```bash
# Test help/usage
python run_feature.py --help

# Test argument parsing
python run_feature.py --invalid-arg  # Should show error, not crash
```

**Expected:**
- Help message displays correctly
- Invalid arguments handled gracefully
- No crashes, no stack traces for normal usage errors

**If entry point fails:**
1. Read the error
2. Fix the argument parsing or initialization
3. Re-run entry point test
4. Only proceed when entry point works

#### Part 3: Execution Test

**Purpose:** Verify feature works end-to-end with real data

**Minimum Requirements:**
1. **Run with real data** - no mocks, no fixtures
2. **Run end-to-end** - from CLI to output files
3. **Run for sufficient duration** - at least 30-60 seconds
4. **Verify all outputs** - check file contents, not just existence
5. **Check logs** - look for warnings or unexpected behavior

**Example:**
```bash
# Run feature with minimal but real workload
python run_feature.py --mode test --iterations 2 --sims 10

# Wait for completion (30-60 seconds minimum)

# Check outputs exist
ls output_folder/

# Check output contents
cat output_folder/result.json  # Verify structure and values

# Check logs for issues
grep -i warning output.log  # Should be empty or expected warnings only
grep -i error output.log  # Should be empty
```

**ENHANCED VALIDATION CHECKLIST:**

#### 1. Output Validation (Not Just "Does It Run")
- [ ] Values are in expected range (compare to baseline/known results)
- [ ] Results vary appropriately (not all zeros, not all identical)
- [ ] All expected components produce output (e.g., all 5 horizons, not just 1)
- [ ] Counts/metrics match expectations (player counts, iteration counts)
- [ ] **Compare to baseline**: Run should produce similar results to previous optimal config

#### 2. Log Analysis (Active Checking)
- [ ] `grep -i warning output.log` → Should be empty (or only expected warnings)
- [ ] `grep -i error output.log` → Should be empty
- [ ] Config/parameter identification is clear (can you tell what's being tested?)
- [ ] Progress updates are meaningful (not stuck at 0% or showing nonsense)
- [ ] Summary information is complete (all expected metrics reported)

#### 3. User Experience Validation
- [ ] Ctrl+C exits cleanly (<2 seconds, no zombie processes)
- [ ] Progress updates regularly (not stuck for minutes)
- [ ] ETA estimates are reasonable (within 2x of actual time)
- [ ] Output is readable and informative (user can understand what's happening)
- [ ] Error messages are actionable (tell user what to fix)

#### 4. Comparison to Working Reference
- [ ] Run similar existing feature side-by-side (e.g., run_win_rate_simulation.py)
- [ ] Compare logging patterns (do they follow same style?)
- [ ] Compare initialization (does new feature set up state like reference?)
- [ ] Compare progress display (similar format and updates?)
- [ ] **Spot check**: Pick a specific integration point from planning and verify it works

#### 5. Output Location Verification (MANDATORY)

**Purpose:** Verify files are in EXACT location specified in specs, not just "somewhere"

**Step 1: Identify Spec Output Location**
```markdown
# From specs.md:
**Output Location:** /data/player_data/
**File Pattern:** new_{position}_data_*.json
**File Count:** 6 files (QB, RB, WR, TE, K, DST)
```

**Step 2: Verify Correct Location Has Files**
```bash
# Use exact spec path
ls data/player_data/new_*_data_*.json

# Expected result:
# - Lists 6 files (or exact count from spec)
# - All files from latest run
# - No error message

# Verify count
ls data/player_data/new_*_data_*.json | wc -l
# Expected: 6
```

**Step 3: Verify Wrong Locations Have NO Files**
```bash
# Check other plausible locations
ls player-data-fetcher/data/new_*_data_*.json 2>&1
# Expected: "No such file or directory"

ls data/new_*_data_*.json 2>&1
# Expected: "No such file or directory" (if spec says player_data/ subfolder)

# Add any other locations that might be confused
```

**Step 4: Verify Log Messages Show Correct Paths**
```bash
# Grep logs for file paths
grep "Exported.*to\|Created.*file\|Saved.*to" output.log

# Expected patterns in paths:
# ✅ Contains: "data/player_data/" or "../data/player_data/"
# ❌ Should NOT contain: "player-data-fetcher/data/" (if that's wrong location)
```

**Step 5: Use Absolute Paths to Eliminate Ambiguity**
```bash
# Get absolute path of created files
realpath data/player_data/new_qb_data_*.json

# Expected result should match:
# {PROJECT_ROOT}/data/player_data/new_qb_data_TIMESTAMP.json

# NOT:
# {PROJECT_ROOT}/player-data-fetcher/data/...
```

**Step 6: Verify Exact Filename Pattern (CRITICAL)**
```bash
# Compare actual filenames to spec-defined pattern

# From specs.md:
# **Filenames:** qb_data.json, rb_data.json, wr_data.json, te_data.json, k_data.json, dst_data.json
# (or whatever pattern is specified)

# List actual filenames
ls data/player_data/

# Expected results (example):
# qb_data.json
# rb_data.json
# wr_data.json
# te_data.json
# k_data.json
# dst_data.json

# ❌ BAD (if spec says NO timestamps):
# qb_data_20251224_133017.json
# rb_data_20251224_133017.json

# ❌ BAD (if spec says simple names):
# new_qb_data_latest.json
# new_rb_data_latest.json
```

**Filename Pattern Verification:**
```bash
# Check for timestamps when they shouldn't exist
ls data/player_data/*_2025*.json 2>&1
# Expected: "No such file or directory" (if spec says no timestamps)

# Check for "latest" suffix when it shouldn't exist
ls data/player_data/*_latest.json 2>&1
# Expected: "No such file or directory" (if spec says no latest suffix)

# Verify exact filenames match spec
for file in qb_data.json rb_data.json wr_data.json te_data.json k_data.json dst_data.json; do
  if [ ! -f "data/player_data/$file" ]; then
    echo "MISSING: $file"
  fi
done
# Expected: No output (all files exist with exact names)
```

**Why Filename Pattern Matters:**
Real bug example: Spec said filenames should be `qb_data.json, rb_data.json, etc.` (simple names, no timestamps). Implementation created `new_qb_data_20251224_133017.json` files. Files were in correct LOCATION but wrong PATTERN. This makes downstream consumers harder to implement (must find latest timestamp instead of reading fixed filename).

**Common Filename Issues:**
- Timestamps added when spec says "simple names that get overwritten"
- Prefix/suffix variations (new_, _latest, _v2)
- Case sensitivity (QBData.json vs qb_data.json)
- Extension variations (.json vs .JSON vs .txt)

**Location Verification Checklist:**
- [ ] Files exist in correct spec location
- [ ] File count matches spec
- [ ] **Filenames match EXACT pattern from spec** (no timestamps/prefixes/suffixes if not specified)
- [ ] NO files in wrong locations
- [ ] Log messages show correct paths
- [ ] Absolute paths confirm correct directories

**Red Flags (Feature NOT Ready):**
- [ ] Files found in location other than spec location
- [ ] File count doesn't match spec
- [ ] **Filenames have timestamps when spec says "simple names"**
- [ ] **Filenames have prefixes/suffixes not in spec**
- [ ] Log messages show unexpected paths
- [ ] Absolute paths reveal wrong directories

**Why This Matters:**
Real bug example: Spec said `/data/player_data/`, but files went to `player-data-fetcher/data/`. QC Rounds 1-2 verified "files exist" ✅ but didn't verify "files in CORRECT location" ❌. QC Round 3 caught it by explicitly checking both locations. This is a spec violation that would have shipped to production.

**Common Mistake:**
```markdown
# ❌ INSUFFICIENT:
"I ran the script and files were created. ✅"

# ✅ REQUIRED:
"I verified all 6 files are in data/player_data/ ✅"
"I verified NO files are in player-data-fetcher/data/ ✅"
"Log messages show ../data/player_data/ paths ✅"
```

**Prevention:**
Don't assume "files created" means "files in right place". Always verify:
1. Correct location HAS the files
2. Wrong locations DON'T have the files
3. Log paths match spec location

#### 6. Data Quality Verification (MANDATORY)

**Purpose:** Verify output data has correct SEMANTICS, not just correct STRUCTURE

```
╔═════════════════════════════════════════════════════════════════╗
║  🛑 CRITICAL: VALIDATE DATA MEANING, NOT JUST STRUCTURE        ║
╠═════════════════════════════════════════════════════════════════╣
║                                                                 ║
║  Code can run without errors and produce files with correct    ║
║  structure (field names, array lengths, types) but contain     ║
║  WRONG DATA (zeros, duplicates, incorrect semantics).          ║
║                                                                 ║
║  Structure validation is NOT sufficient.                       ║
║  Data quality validation is MANDATORY.                         ║
║                                                                 ║
║  REAL EXAMPLE:                                                 ║
║  ✅ Files created (structure check passed)                     ║
║  ✅ Arrays have 17 elements (structure check passed)           ║
║  ✅ All field names correct (structure check passed)           ║
║  ❌ All stat arrays filled with zeros (DATA QUALITY FAIL)      ║
║  ❌ projected_points same as actual_points (DATA QUALITY FAIL) ║
║                                                                 ║
║  Result: Feature shipped but completely useless.               ║
║                                                                 ║
╚═════════════════════════════════════════════════════════════════╝
```

**Data Quality Validation Checklist:**

**Step 1: Identify Critical Data Fields**
- List all data fields that must contain REAL data (not zeros/nulls/placeholders)
- Identify fields where semantics matter (e.g., projected vs actual)
- Flag any arrays that should have non-zero values for completed time periods

**Step 2: Spot-Check Against External Source**
```bash
# Example: Player statistics feature
# Pick one well-known entity to validate

# From output file (e.g., Josh Allen in qb_data.json):
{
  "name": "Josh Allen",
  "actual_points": [38.76, 11.82, 23.02, ...],
  "projected_points": [25.5, 24.8, 26.2, ...],
  "passing": {
    "yards": [232, 180, 258, 0, 215, ...],
    "tds": [2, 0, 2, 0, 1, ...]
  }
}

# Verify against external source:
# 1. Go to ESPN.com/NFL/Players/Josh Allen
# 2. Check Week 1 stats
# 3. Confirm passing yards = 232 (or close)
# 4. Confirm passing TDs = 2
# 5. Confirm actual_points ≈ 38.76

# Expected: Values match within reasonable tolerance
```

**Step 3: Verify Data Semantics**
```bash
# Example: Projected vs Actual Points
# projected_points = what player was EXPECTED to score (pre-game)
# actual_points = what player ACTUALLY scored (post-game)

# For COMPLETED weeks, these should be DIFFERENT:
grep -A 2 '"projected_points"' qb_data.json | head -5
grep -A 2 '"actual_points"' qb_data.json | head -5

# RED FLAG: If arrays are identical for completed weeks
# This means feature is using wrong data source

# Spot check one player:
# projected_points[0] should NOT equal actual_points[0] (unless lucky guess)
```

**Step 4: Check for Placeholder Zeros**
```bash
# Example: Statistical arrays should have non-zero values

# Bad pattern (all zeros):
"passing": {
  "yards": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
}

# Good pattern (real data + future zeros):
"passing": {
  "yards": [232, 180, 258, 0, 215, 280, 0, 323, 342, 225, 366, 145, 189, 342, 295, 160, 0]
}
# Note: 0 at index 3 = bye week (expected)
# Note: 0 at index 16 = Week 17 not yet played (expected)

# Validation:
cat qb_data.json | jq '.[0].passing.yards'
# Should see mix of non-zero values and zeros (not all zeros)
```

**Step 5: Validate Time-Based Data Patterns**
```bash
# Example: Historical vs Future Data

# For current week 16 (example):
# - Weeks 1-16: Should have real data (completed weeks)
# - Week 17: Should have zeros or projections (future week)

# Check that PAST data exists:
cat qb_data.json | jq '.[0].actual_points[0:15]' | grep -v "0.0" | wc -l
# Expected: Most values non-zero (allows for bye weeks)

# Check that FUTURE data is zero or projected:
cat qb_data.json | jq '.[0].actual_points[16]'
# Expected: 0.0 (Week 17 not yet played)
```

**Step 6: Verify Field Uniqueness**
```bash
# Example: Fields that should be different

# projected_points vs actual_points (should differ for completed weeks)
diff <(cat qb_data.json | jq '.[0].projected_points[0:10]') \
     <(cat qb_data.json | jq '.[0].actual_points[0:10]')
# Expected: Many differences (not identical arrays)

# Player stats should vary by player
diff <(cat qb_data.json | jq '.[0].actual_points') \
     <(cat qb_data.json | jq '.[1].actual_points')
# Expected: Different values (not all players identical)
```

**Data Quality Verification Pass Criteria:**
- [ ] Spot-checked at least one well-known entity against external source (ESPN, official stats)
- [ ] Verified data semantics match spec (projected ≠ actual for completed periods)
- [ ] Confirmed no unexpected placeholder zeros in historical data
- [ ] Validated time-based patterns (past has data, future is zero/projected)
- [ ] Verified fields that should differ are actually different
- [ ] All critical data fields contain real, meaningful values

**Data Quality Verification Fail Criteria:**
- [ ] Spot-check reveals data doesn't match external source
- [ ] Fields with different semantics contain identical data
- [ ] Historical data filled with placeholder zeros
- [ ] All players have identical stats (copy-paste error)
- [ ] Projected and actual values are identical for all completed weeks

**Why This Matters:**
Real bug example: Position JSON files passed all structural tests (files exist, correct location, 17 elements per array, correct field names) but contained:
- All stat arrays with zeros (should have real ESPN stats)
- projected_points identical to actual_points (should be different data sources)
- Result: Feature technically works but produces useless output

This would have been caught by spot-checking one player's Week 1 stats against ESPN website.

**When Data Quality Check Fails:**
1. Feature is INCOMPLETE (not just buggy)
2. Return to implementation phase
3. Implement missing data extraction
4. Re-run ALL unit tests (ensure 100% pass)
5. Re-run smoke test from Part 1
6. Document lesson learned

---

**Expected results (all must be true):**
- ✅ Script runs without crashes
- ✅ All expected output files created with correct structure
- ✅ Output contains valid, non-zero values in expected ranges
- ✅ Logs show expected progression (parameter updates, new bests, etc.)
- ✅ **No WARNING or ERROR messages** (grep for them!)
- ✅ **Output matches test plan from planning phase** (check Testing & Validation section from specs)

**If smoke test finds bugs:**
1. Fix the bug
2. Re-run ALL unit tests (ensure 100% pass rate maintained)
3. Re-run smoke test
4. Repeat until clean pass
5. **Root cause analysis:** Why didn't unit tests catch this?
6. Document in lessons_learned.md

### Common Bug Types Found During Smoke Testing

Based on real features, smoke testing catches:
- Type mismatches between modules (unit tests mock these away)
- Import path errors (unit tests import directly)
- Data structure assumptions (unit tests use simplified fixtures)
- API interface changes (unit tests use old mocks)
- Environment-specific issues (paths, file structure)
- Integration bugs (component A calls component B incorrectly)

**These bugs are INVISIBLE to unit tests because:**
- Unit tests mock external dependencies
- Unit tests use simplified test data
- Unit tests test components in isolation
- Unit tests don't exercise full data flow

### Anti-Patterns to Avoid

❌ "All tests pass, must be working" - WRONG
✅ "All tests pass AND smoke test passes" - CORRECT

❌ "Just run --help and call it done" - WRONG
✅ "Run end-to-end with real data for 60 seconds" - CORRECT

❌ "Smoke test failed, but I'll fix it later" - WRONG
✅ "Smoke test failed, stop everything and fix it now" - CORRECT

**Output:** Smoke test report confirming all 3 parts passed.

---

## Step 4: Quality Control Round 1 (Initial Review)

See `protocols_reference.md` → Quality Control Review Protocol for detailed steps.

**QC Round 1 Focus:**
- Initial code review
- Documentation review
- Script execution monitoring (NOT smoke testing - already done)
- Basic structural checks

**QC Round 1 Checklist:**
- [ ] Code follows project conventions
- [ ] All files have proper docstrings
- [ ] Code matches specs structurally
- [ ] Tests use real objects where possible (not excessive mocking)
- [ ] Output file tests validate CONTENT, not just existence
- [ ] Private methods with branching logic are tested
- [ ] At least one integration test runs feature end-to-end
- [ ] Runner scripts tested with --help
- [ ] Runner scripts tested E2E with real data
- [ ] Interfaces verified against actual class definitions
- [ ] Data model attributes verified to exist

**Script Execution During QC Round 1:**

**IMPORTANT:** Test ALL execution modes, not just --help.

If the feature includes a runner script (`run_*.py`), you MUST:

1. **Execute the script with --help** to verify argument parsing works
2. **Execute the script in dry-run mode** (if available) or with minimal input
3. **Execute the script end-to-end** with real data:
   - Not mocked dependencies
   - Not simulated paths
   - Actual file system interactions
4. **For scripts with multiple modes** (single, full, iterative, etc.):
   - Test at least one iteration of EACH mode
   - Don't assume unit tests cover all code paths
   - Different modes execute different code paths

**Example:**
```bash
# Basic tests
python run_feature.py --help
python run_feature.py single --sims 1

# Test other modes (run for 1-2 iterations minimum)
timeout 60 python run_feature.py iterative --sims 1 --test-values 1
# Should complete at least 1 parameter without errors
```

**Why this matters:**
- Different modes execute different code paths
- Bugs can hide in modes not covered by unit tests
- Smoke tests must cover representative execution paths

**When E2E tests reveal errors:**
1. Fix the immediate error
2. Perform root cause analysis:
   - Why was this error created?
   - Why wasn't it caught during unit testing?
   - Why wasn't it caught during verification iterations?
3. Document findings in lessons_learned.md
4. Only proceed after documenting the lesson

### QC Round 1 Pass/Fail Criteria

**Pass Criteria:**
- <3 critical issues found
- >80% of requirements met correctly
- All critical structural elements match specs

**Fail Criteria (indicates implementation process not followed):**
- ≥3 critical issues found
- <80% of requirements met correctly
- Fundamental structural mismatches with specs

**If QC Round 1 FAILS:**

```
╔═════════════════════════════════════════════════════════════════╗
║  🛑 🛑 🛑 QC ROUND 1 FAILED - CRITICAL PROCESS FAILURE 🛑 🛑 🛑 ║
╠═════════════════════════════════════════════════════════════════╣
║                                                                 ║
║  QC Round 1 failure (≥3 critical issues OR <80% requirements   ║
║  met) indicates the implementation process was NOT followed.   ║
║                                                                 ║
║  ROOT CAUSE ANALYSIS (Identify which failed):                  ║
║  □ Specs were not consulted during implementation?             ║
║  □ Continuous spec verification was skipped?                   ║
║  □ TODO acceptance criteria were incomplete?                   ║
║  □ Pre-implementation audit passed incorrectly?                ║
║  □ Mini-QC checkpoints were skipped or rushed?                 ║
║                                                                 ║
║  CONSEQUENCES:                                                 ║
║  - Implementation does not match specs                         ║
║  - Major rework required                                       ║
║  - Process credibility compromised                             ║
║                                                                 ║
║  MANDATORY REMEDIATION:                                        ║
║  1. STOP all QC rounds immediately                             ║
║  2. Return to implementation_execution_guide.md                ║
║  3. Re-implement with STRICT spec verification:                ║
║     • Keep specs.md visible at ALL times                       ║
║     • Verify EACH requirement BEFORE implementing              ║
║     • Verify EACH requirement AFTER implementing               ║
║     • Mini-QC after EACH major component                       ║
║  4. Document root cause in lessons_learned.md                  ║
║  5. Only re-run QC Round 1 after ALL issues fixed              ║
║                                                                 ║
║  IMPORTANT: QC is for finding MINOR issues, not FUNDAMENTAL    ║
║  problems. Fundamental problems mean verification failed.      ║
║                                                                 ║
╚═════════════════════════════════════════════════════════════════╝
```

**QC is for finding MINOR issues, not FUNDAMENTAL problems.**

If QC finds fundamental problems (wrong structure, missing major requirements, incorrect mappings), this means verification process failed, not just implementation.

**Output:** QC Round 1 report in code_changes.md with issues found/fixed.

**⚡ UPDATE README Agent Status:** Step=QC Round 1 complete

---

```
╔═════════════════════════════════════════════════════════════════╗
║  ⏸️  SELF-AUDIT CHECKPOINT: After QC Round 1                    ║
╠═════════════════════════════════════════════════════════════════╣
║                                                                 ║
║  PAUSE before proceeding to Round 2. Answer honestly:          ║
║                                                                 ║
║  Round 1 Completion:                                           ║
║  □ Did I complete ALL items in QC Round 1 Checklist?           ║
║  □ Did I test ALL execution modes (not just --help)?           ║
║  □ Did I verify interfaces against actual class definitions?   ║
║  □ Did I validate output file CONTENT (not just existence)?    ║
║  □ Did I run the script end-to-end with real data?             ║
║                                                                 ║
║  Documentation:                                                ║
║  □ Have I documented findings in code_changes.md?              ║
║  □ Did I update lessons_learned.md for any issues found?       ║
║  □ Did I update README Agent Status to "QC Round 1 complete"?  ║
║                                                                 ║
║  Issue Resolution:                                             ║
║  □ Have I FIXED all issues found (not just documented)?        ║
║  □ Did I re-run tests after fixes?                             ║
║  □ Did I verify fixes actually work?                           ║
║                                                                 ║
║  Pass Criteria Check:                                          ║
║  □ Did I find <3 critical issues?                              ║
║  □ Are >80% of requirements met correctly?                     ║
║  □ Does code match specs structurally?                         ║
║                                                                 ║
║  Red Flags (If YES to any, DO NOT proceed to Round 2):         ║
║  □ Found ≥3 critical issues (Round 1 FAILED - see protocol)    ║
║  □ <80% requirements met (Round 1 FAILED)                      ║
║  □ Skipped end-to-end execution testing                        ║
║  □ Only tested --help, not actual functionality                ║
║  □ Checked file existence but not content                      ║
║  □ Have unfixed issues remaining                               ║
║                                                                 ║
║  If Round 1 FAILED (≥3 issues OR <80% requirements):           ║
║  → DO NOT proceed to Round 2                                   ║
║  → Follow QC Round 1 Failure Protocol above                    ║
║  → Return to implementation phase                              ║
║                                                                 ║
║  If all checks passed AND no red flags:                        ║
║  → Proceed to QC Round 2 (Deep Verification)                   ║
║                                                                 ║
╚═════════════════════════════════════════════════════════════════╝
```

---

## Step 5: Quality Control Round 2 (Deep Verification)

**QC Round 2 Focus:**
- Deep dive into implementation details
- Semantic diff checking (whitespace vs logic changes)
- Cross-reference with specs
- Baseline comparison (if similar feature exists)

**QC Round 2 Checklist:**
- [ ] **Baseline comparison:** If similar feature exists, compare outputs side-by-side
- [ ] **Output validation:** Results are in expected range (not all zeros, not nonsense)
- [ ] **No regressions:** New feature doesn't break or degrade existing features
- [ ] **Log quality:** No unexpected WARNING/ERROR messages in output
- [ ] **Semantic diff:** Changes are intentional, not accidental
- [ ] **Edge cases:** All edge cases from specs are handled
- [ ] **Error handling:** All error conditions from specs are handled
- [ ] **Documentation:** All docstrings match implementation

**Semantic Diff Check:**

Run `git diff` and analyze each change:
- Is this change intentional or accidental?
- Does this change match a requirement in specs?
- Is this whitespace-only or logic change?
- Are there unintended side effects?

**If issues found:**
1. Fix the issue
2. Re-run all unit tests
3. Re-run smoke test
4. Document in lessons_learned.md
5. Continue QC Round 2

**Output:** QC Round 2 report in code_changes.md with issues found/fixed.

**⚡ UPDATE README Agent Status:** Step=QC Round 2 complete

---

```
╔═════════════════════════════════════════════════════════════════╗
║  ⏸️  SELF-AUDIT CHECKPOINT: After QC Round 2                    ║
╠═════════════════════════════════════════════════════════════════╣
║                                                                 ║
║  PAUSE before final round. Answer honestly:                    ║
║                                                                 ║
║  Round 2 Completion:                                           ║
║  □ Did I complete ALL items in QC Round 2 Checklist?           ║
║  □ Did I perform baseline comparison (if applicable)?          ║
║  □ Did I run semantic diff check on all changes?               ║
║  □ Did I validate output values are in expected range?         ║
║  □ Did I check for regressions to existing features?           ║
║                                                                 ║
║  Deep Verification:                                            ║
║  □ Did I grep logs for WARNING messages?                       ║
║  □ Did I grep logs for ERROR messages?                         ║
║  □ Did I verify all edge cases are handled?                    ║
║  □ Did I verify all error conditions are handled?              ║
║  □ Did I cross-reference with specs.md?                        ║
║                                                                 ║
║  Documentation:                                                ║
║  □ Have I documented Round 2 findings in code_changes.md?      ║
║  □ Did I update lessons_learned.md for any new issues?         ║
║  □ Did I update README Agent Status to "QC Round 2 complete"?  ║
║                                                                 ║
║  Issue Resolution:                                             ║
║  □ Have ALL issues from Round 1 been resolved?                 ║
║  □ Have ALL issues from Round 2 been fixed?                    ║
║  □ Did I re-run tests after fixes?                             ║
║  □ Did I re-run smoke test after fixes?                        ║
║                                                                 ║
║  Red Flags (If YES to any, DO NOT proceed to Round 3):         ║
║  □ Skipped baseline comparison when similar feature exists     ║
║  □ Skipped semantic diff analysis                              ║
║  □ Didn't grep for WARNING/ERROR in logs                       ║
║  □ Have unfixed issues from Round 1 or 2                       ║
║  □ Found new critical issues in Round 2                        ║
║                                                                 ║
║  If any red flags present:                                     ║
║  → DO NOT proceed to Round 3                                   ║
║  → Fix all remaining issues                                    ║
║  → Re-run Round 2 verification                                 ║
║                                                                 ║
║  If all checks passed AND no red flags:                        ║
║  → Proceed to QC Round 3 (Final Skeptical Review)              ║
║                                                                 ║
╚═════════════════════════════════════════════════════════════════╝
```

---

## Step 6: Quality Control Round 3 (Final Skeptical Review)

**QC Round 3 Focus:**
- Final skeptical review with fresh eyes
- Challenge all assumptions
- Verify nothing was missed
- Final comparison to specs

**QC Round 3 Mindset:**

Pretend you're a skeptical reviewer who doesn't trust the previous rounds. Your job is to find what was missed.

**QC Round 3 Checklist:**
- [ ] Re-read specs.md one final time - anything missed?
- [ ] Re-read question answers - all decisions implemented?
- [ ] Re-check Algorithm Traceability Matrix - all algorithms correct?
- [ ] Re-check Integration Matrix - all methods have callers?
- [ ] Re-run smoke test one final time
- [ ] Compare final output to test plan in specs
- [ ] Review all lessons_learned entries - all addressed?
- [ ] Final check: Is feature actually complete and working?

**If issues found:**
1. Fix the issue (this should be rare by Round 3)
2. Re-run all unit tests
3. Re-run smoke test
4. Document in lessons_learned.md
5. **Consider:** If Round 3 found major issues, what did Rounds 1-2 miss?

**Output:** QC Round 3 report in code_changes.md with final status.

**⚡ UPDATE README Agent Status:** Step=QC Round 3 complete

---

## Step 7: Review Lessons Learned

1. **Read `{feature_name}_lessons_learned.md`**
   - Review all issues encountered
   - Identify patterns
   - Determine root causes

2. **Identify guide updates needed**
   - Which issues could have been prevented by better guides?
   - What new protocols or checklists would help?
   - What examples or warnings would prevent recurrence?

3. **Create guide update recommendations:**

```markdown
## Recommended Guide Updates

### Guide: {guide_name}

**Issue:** {description of issue from lessons learned}
**Recommendation:** {specific change to guide}
**Justification:** {why this would prevent the issue}

### Guide: {another_guide}

...
```

4. **Present summary to user:**

```
Lessons Learned Review Complete:
- {N} issues encountered during development
- {N} issues were process failures (could have been prevented)
- {N} issues were genuine unknowns (need spec clarification)

Recommended Guide Updates:
- {guide_name}: {brief description}
- {guide_name}: {brief description}

Should I apply these updates to the guides?
```

5. **Wait for user approval**

6. **Apply approved updates to guides**

---

## Step 8: Completion Checklist

```
┌─────────────────────────────────────────────────────────────────┐
│  ✓ FINAL CHECKLIST BEFORE MARKING COMPLETE                      │
└─────────────────────────────────────────────────────────────────┘

□ All unit tests passing (100% pass rate)
□ Smoke testing protocol completed (all 3 parts passed)
□ Requirement Verification Protocol completed
□ QC Round 1 completed (pass criteria met)
□ QC Round 2 completed (pass criteria met)
□ QC Round 3 completed (pass criteria met)
□ All issues found during QC fixed and verified
□ Lessons learned reviewed
□ Guide updates identified and approved by user
□ Approved guide updates applied
□ code_changes.md complete with all 3 QC rounds documented
□ implementation_checklist.md shows all requirements verified
□ README.md Agent Status updated to "Complete"
```

**Only proceed to Step 9 when ALL items are checked.**

---

## Step 9: Move to Done

Move entire folder: `feature-updates/{feature_name}/` → `feature-updates/done/{feature_name}/`

```bash
# Windows
move feature-updates\{feature_name} feature-updates\done\{feature_name}

# Linux/Mac
mv feature-updates/{feature_name} feature-updates/done/{feature_name}
```

**⚡ UPDATE README Agent Status:** Phase=COMPLETE

---

## Step 10: Commit Changes

Create a commit with a descriptive message summarizing the feature:

```bash
git add -A
git commit -m "Add {feature_name}: {brief description of what was implemented}"
```

**Commit message guidelines:**
- Start with action verb (Add, Implement, Create, etc.)
- Include feature name
- Briefly describe what was added/changed
- Keep under 50 characters for subject line
- Add body with bullet points for major changes if needed

**Example:**
```
Add accuracy simulation mode

- Implement AccuracySimulationManager for prediction accuracy tracking
- Add 5 accuracy metrics (MAE, RMSE, R², bias, correlation)
- Create run_accuracy_simulation.py entry point
- Add comprehensive unit tests (100% pass rate)
```

**Do NOT include:**
- "Generated with Claude Code" footer
- Co-author tag
- Emojis or subjective language

**After commit:**
- Verify commit created: `git log --oneline -1`
- Verify all changes included: `git status` (should be clean)

---

## Session Handoff (If Context Running Low)

When context is running low or session is ending during QC, complete this checklist:

```
┌─────────────────────────────────────────────────────────────────┐
│  SESSION HANDOFF CHECKLIST                                       │
│  Complete ALL items before session ends                          │
└─────────────────────────────────────────────────────────────────┘

□ Document current QC round status in code_changes.md
□ List any issues found but not yet fixed
□ Update README Agent Status section with:
  - Current Phase: POST-IMPLEMENTATION
  - Current Step: QC Round {N} (in progress/complete)
  - Next Action: {what remains}
□ Commit any fixes made so far
□ Update Progress Notes:
  - Current status (which rounds complete)
  - Issues found/fixed
  - Next steps (what remains)
□ Summary message sent to user:
  "Session ending. QC progress preserved:
   - Completed: {rounds/steps}
   - In progress: {current round}
   - Issues found: {count}
   - Issues fixed: {count}
   - Next: {what to do next}
   - All state documented in README Agent Status."
```

---

## Communication Guidelines

How often to update the user during post-implementation:

| Phase | Communication Level | What to Report |
|-------|---------------------|----------------|
| **Requirement Verification** | When complete | "All requirements verified against specs." |
| **Smoke Testing** | When complete | "Smoke test passed. Feature works E2E." |
| **QC Rounds** | Per round | "QC Round 1 complete. Found X issues, fixed Y." |
| **Issues Found** | Immediately | "Found issue: {description}. Fixing..." |
| **Blockers** | Immediately | Any issue that prevents completion |

**Do NOT:**
- Stay silent during long QC rounds
- Wait until end to reveal issues
- Skip reporting smoke test results

**DO:**
- Report each round completion
- Report issues as they're found
- Confirm when all QC passes

---

## Resuming Work Mid-QC

If you're picking up QC work started by a previous agent:

1. **Read README.md Agent Status** - See which QC round you're on
2. **Read code_changes.md** - See QC rounds completed and issues found
3. **Read lessons_learned.md** - See issues documented
4. **Run all unit tests** - Verify baseline: `python tests/run_all_tests.py`
5. **Check for uncommitted fixes** - `git status`
6. **Continue from current round** - Pick up exactly where left off

**Determine current state:**
| README Status | Current State | Next Action |
|---------------|--------------|-------------|
| "QC Round 1 in progress" | Mid-Round 1 | Complete Round 1 checklist |
| "QC Round 1 complete" | Round 1 done | Start Round 2 |
| "QC Round 2 in progress" | Mid-Round 2 | Complete Round 2 checklist |
| "QC Round 2 complete" | Round 2 done | Start Round 3 |
| "QC Round 3 in progress" | Mid-Round 3 | Complete Round 3 checklist |
| "QC Round 3 complete" | All QC done | Review lessons learned |

---

## Quick Commands Reference

Common commands you'll need during post-implementation:

```bash
# Run all tests
python tests/run_all_tests.py

# Run specific test file
python -m pytest tests/path/to/test_file.py -v

# Smoke test - import
python -c "import path.to.module"

# Smoke test - entry point
python run_feature.py --help

# Smoke test - execution
python run_feature.py --mode test --iterations 2

# Check for warnings in logs
grep -i warning output.log

# Check for errors in logs
grep -i error output.log

# View git diff
git diff

# View git status
git status

# Commit changes
git add -A
git commit -m "Feature complete: {description}"

# View recent commits
git log --oneline -5

# Move folder to done
move feature-updates\{name} feature-updates\done\{name}  # Windows
mv feature-updates/{name} feature-updates/done/{name}     # Linux/Mac
```

---

## Exit Criteria: Ready to Complete Feature

```
┌─────────────────────────────────────────────────────────────────┐
│  ⚠️  BEFORE MOVING TO DONE/ AND COMMITTING                      │
│  Verify ALL criteria below are met                             │
└─────────────────────────────────────────────────────────────────┘
```

**DO NOT mark feature complete until ALL of these criteria are met:**

### 1. Testing Complete

□ All unit tests passing (100% pass rate)
  - `python tests/run_all_tests.py` exits with code 0
  - No skipped tests
  - No flaky tests

□ Smoke Testing Protocol complete (all 3 parts passed)
  - Part 1: Import Test passed
  - Part 2: Entry Point Test passed
  - Part 3: Execution Test passed (30-60 seconds minimum)
  - All outputs validated (content, not just existence)
  - No WARNING/ERROR messages in logs

### 2. Quality Control Complete

□ QC Round 1 completed and passed
  - Pass criteria met (<3 critical issues, >80% requirements met)
  - All findings documented in code_changes.md
  - All issues fixed and verified

□ QC Round 2 completed and passed
  - Deep verification complete
  - Baseline comparison done (if applicable)
  - Semantic diff checked
  - All findings documented in code_changes.md
  - All issues fixed and verified

□ QC Round 3 completed and passed
  - Final skeptical review complete
  - Zero critical issues found
  - All findings documented in code_changes.md
  - Feature confirmed working end-to-end

### 3. Verification Complete

□ Requirement Verification Protocol completed
  - Every line of specs.md verified addressed
  - Every question answer verified implemented
  - Algorithm Traceability Matrix verified
  - Integration Evidence verified

□ All execution modes tested
  - Not just --help, but real E2E execution
  - All modes tested (single, full, iterative, etc.)
  - Output validated against expected values

### 4. Documentation Complete

□ code_changes.md contains all 3 QC round reports
  - QC Round 1 findings and fixes documented
  - QC Round 2 findings and fixes documented
  - QC Round 3 findings and fixes documented

□ implementation_checklist.md shows all requirements verified

□ lessons_learned.md reviewed and complete
  - All issues documented
  - Root causes identified
  - Guide update recommendations created

□ README.md Agent Status updated to "Complete"

### 5. Feature Ready for Production

□ Feature works end-to-end with real data
□ All output files contain valid, expected data
□ No regressions to existing features
□ Error handling complete and tested
□ Edge cases handled
□ Logs are clean (no unexpected warnings/errors)

### 6. Lessons Learned & Guide Updates

□ Lessons learned reviewed with user
□ Guide update recommendations presented to user
□ User approval received for guide updates
□ Approved guide updates applied

### Self-Verification Questions

**Ask yourself these questions. If ANY answer is "no" or "uncertain", DO NOT proceed:**

1. **"Has this feature been tested end-to-end with real data, and does it produce the expected results?"**
   - If uncertain → Re-run smoke test and validate output
   - If no → Fix and re-test

2. **"Have all 3 QC rounds been completed with proper documentation of findings?"**
   - If uncertain → Review code_changes.md for all 3 round reports
   - If no → Complete missing QC rounds

3. **"If I ran this feature right now, would it work correctly without errors?"**
   - If uncertain → Run it and validate
   - If no → Fix the issues

4. **"Have I compared the output to the test plan in specs.md and confirmed it matches?"**
   - If uncertain → Re-read specs Test Plan section and compare
   - If no → Validate output matches expectations

5. **"Are there any known issues, TODOs, or 'fix later' items remaining?"**
   - If yes → Fix them now before completing
   - If uncertain → Search codebase for TODO comments

### Proceed or Stop?

```
╔═════════════════════════════════════════════════════════════════╗
║  🛑 🛑 🛑 FINAL GATE - BEFORE MARKING COMPLETE 🛑 🛑 🛑         ║
╠═════════════════════════════════════════════════════════════════╣
║                                                                 ║
║  This is the FINAL verification before marking feature         ║
║  complete. Once you move to done/ and commit, you are          ║
║  declaring this feature PRODUCTION READY.                      ║
║                                                                 ║
║  FINAL VERIFICATION (All must be CHECKED):                     ║
║  □ All exit criteria checkboxes above are checked              ║
║  □ All 5 self-verification questions answered "YES"            ║
║  □ Feature works end-to-end with real data                     ║
║  □ No known issues, bugs, or "fix later" items                 ║
║  □ User would be satisfied with this feature                   ║
║                                                                 ║
║  CONSEQUENCES OF PREMATURE COMPLETION:                         ║
║  ❌ Broken feature shipped to production                       ║
║  ❌ User discovers bugs after "completion"                     ║
║  ❌ Loss of confidence in development process                  ║
║  ❌ Rework required after "done"                               ║
║                                                                 ║
║  IF ALL CRITERIA CHECKED:                                      ║
║  ✅ Feature is complete and validated                          ║
║  ✅ Proceed to Step 9 (Move to done/)                          ║
║  ✅ Then Step 10 (Commit changes)                              ║
║                                                                 ║
║  IF ANY CRITERIA UNCHECKED:                                    ║
║  ❌ DO NOT move to done/                                       ║
║  ❌ DO NOT commit                                              ║
║  ❌ Complete missing criteria                                  ║
║  ❌ Re-verify this checklist                                   ║
║                                                                 ║
╚═════════════════════════════════════════════════════════════════╝
```

---

## Related Guides

| Guide | When to Use | Link |
|-------|-------------|------|
| **Implementation Guide** | Previous guide - execute TODO | `implementation_execution_guide.md` |
| **TODO Creation Guide** | If major issues - return to verification | `todo_creation_guide.md` |
| **Planning Guide** | If scope changes significantly | `feature_planning_guide.md` |
| **Protocols Reference** | Detailed protocol definitions | `protocols_reference.md` |
| **Templates** | File templates | `templates.md` |
| **Prompts Reference** | Conversation prompts | `prompts_reference.md` |
| **Guides README** | Overview of all guides | `README.md` |

### Transition Points

**From Implementation Guide → This guide:**
- All TODO tasks complete
- All tests passing
- All mini-QC checkpoints passed

**This guide → Complete:**
- All 3 QC rounds passed
- Smoke testing passed
- Lessons learned reviewed
- Folder moved to done/
- Changes committed

**Back to Implementation Guide:**
- If QC Round 1 fails (≥3 critical issues)
- If fundamental issues found

---

*This guide assumes implementation is complete. If implementation is not complete, use `implementation_execution_guide.md` first.*
