# Protocols Reference

This file contains detailed protocol definitions referenced by the Feature Development Guide. Use this as a reference when executing specific protocols during verification iterations.

---

## Quick Protocol Lookup

| Protocol | When to Execute | Section |
|----------|-----------------|---------|
| Standard Verification | Iterations 1-3, 8-10, 15-16 | [Link](#standard-verification-protocol) |
| Algorithm Traceability Matrix | Iterations 4, 11, 19 | [Link](#algorithm-traceability-matrix-protocol) |
| End-to-End Data Flow | Iterations 5, 12 | [Link](#end-to-end-data-flow-protocol) |
| Skeptical Re-verification | Iterations 6, 13, 22 | [Link](#skeptical-re-verification-protocol) |
| Integration Gap Check | Iterations 7, 14, 23 | [Link](#integration-gap-check-protocol) |
| Fresh Eyes Review | Iterations 17, 18 | [Link](#fresh-eyes-review-protocol) |
| Edge Case Verification | Iteration 20 | [Link](#edge-case-verification-protocol) |
| Test Coverage Planning | Iteration 21 | [Link](#test-coverage-planning-protocol) |
| Implementation Readiness | Iteration 24 | [Link](#implementation-readiness-protocol) |
| Requirement Verification | Before marking complete | [Link](#requirement-verification-protocol) |
| Quality Control Review | After implementation | [Link](#quality-control-review-protocol) |
| Lessons Learned | Ongoing + before completion | [Link](#lessons-learned-protocol) |
| Guide Update | After QA complete | [Link](#guide-update-protocol) |
| Pre-commit Validation | Before any commit | [Link](#pre-commit-validation-protocol) |

---

## Core Verification Protocols

### Standard Verification Protocol

**Purpose:** Systematic verification through reading, questioning, researching, and updating.

**Execute during:** Iterations 1-3, 8-10, 15-16

**Steps:**

1. **Re-read source documents**
   - `{feature_name}_specs.md` (line by line)
   - Current TODO file
   - User answers (if iterations 8+)

2. **Ask focus questions for this iteration:**

   | Iteration | Focus Questions |
   |-----------|-----------------|
   | 1 | What files need modification? What patterns exist in codebase? |
   | 2 | What error handling is needed? What logging should be added? |
   | 3 | What integration points exist? What mocking needed for tests? |
   | 8 | How do user answers change the plan? Any new tasks needed? |
   | 9 | Are dependencies correctly identified? Any imports missing? |
   | 10 | Is the task breakdown granular enough? Any tasks too large? |
   | 15 | Are all file paths confirmed? Any placeholders remaining? |
   | 16 | Is the integration checklist complete? Ready to implement? |

3. **Research codebase**
   - Use Glob/Grep to find relevant code
   - Look for similar implementations
   - Find test patterns to follow
   - Verify file paths exist

4. **Update TODO file**
   - Add missing requirements discovered
   - Add specific file paths with line numbers
   - Add code references for patterns to follow
   - Mark iteration complete in tracker

**Output:** Updated TODO file with iteration marked complete.

---

### Skeptical Re-verification Protocol

**Purpose:** Challenge all assumptions and re-validate all claims with fresh codebase research.

**Execute during:** Iterations 6, 13, and 22

**Steps:**

1. **Question Everything** - Assume nothing written so far is accurate:
   - Is the file path I documented actually correct? (Verify with Read/Glob)
   - Does that method I referenced actually exist? (Verify with Grep)
   - Is that pattern I identified actually used? (Re-search codebase)
   - Are my assumptions about data flow correct? (Re-trace through code)
   - Did I misunderstand the original requirement? (Re-read specification)

2. **Fresh Codebase Validation:**
   - Re-search for ALL file paths mentioned in TODO
   - Re-verify ALL method names and line numbers
   - Re-validate ALL code patterns claimed
   - Re-check ALL dependencies and imports

3. **Requirement Re-Verification:**
   - Re-read original specification word-by-word
   - Re-read user question answers (if applicable)
   - List requirements again from scratch
   - Compare new list against TODO
   - Identify discrepancies or misinterpretations

4. **Document Results:**
   - Add "Skeptical Re-Verification Results" section to TODO
   - List what was verified as correct
   - List what was found to be incorrect and corrected
   - Document confidence level in current plan

---

### Integration Gap Check Protocol

**Purpose:** Ensure all new code will actually be called from entry points (no orphan code).

**Execute during:** Iterations 7, 14, and 23

**Steps:**

1. **Create Integration Matrix:**
   ```
   | New Component | File | Called By | Caller File:Line | Caller Modification Task |
   |---------------|------|-----------|------------------|--------------------------|
   | save_configs_folder() | ResultsManager.py | run_iterative() | SimulationManager.py:261 | Task 4.2 |
   ```

2. **Verify Caller Modifications in TODO:**
   - For each row in the matrix, confirm a TODO task exists to modify the caller
   - If missing → add the task immediately
   - Flag with warning if integration was previously overlooked

3. **Check for Orphan Code:**
   - Any new component without a caller = orphan code
   - Either add caller modification task OR remove the orphan component

4. **Verify Entry Point Coverage:**
   - For each entry point affected by requirements
   - Trace through to output
   - Confirm all new code is in the execution path

5. **Check Entry Script File Discovery** (if output format changes):
   - List all `run_*.py` scripts that auto-detect files
   - Verify glob patterns match new output format
   - Add TODO tasks for any entry script updates needed

---

### Algorithm Traceability Matrix Protocol

**Purpose:** Ensure spec algorithms are implemented exactly, including all conditional logic.

**Execute during:** Iterations 4, 11, and 19

**Steps:**

1. **For each calculation, formula, or algorithm in the spec:**
   - Extract the EXACT logic from the spec (quote it word-for-word)
   - Document which code file/method will implement it
   - Note any conditional logic (e.g., "if week < X then A, else B")

2. **Create matrix in TODO file:**
   ```
   | Spec Section | Algorithm Description | Code Location | Conditional Logic |
   |--------------|----------------------|---------------|-------------------|
   | Lines 158-186 | projected week columns | generator.py | week < X: historical, week >= X: current |
   | Lines 241-276 | player_rating calc | generator.py | week 1: draft rank, week 2+: cumulative |
   ```

3. **Verify during implementation:**
   - Each algorithm has a matching code location
   - Conditional branches match spec exactly
   - No "simplified" implementations that ignore spec conditions

---

### End-to-End Data Flow Protocol

**Purpose:** Trace complete path from user action to system output; identify integration points.

**Execute during:** Iterations 5 and 12

**Steps:**

1. **Identify Entry Points:**
   - List ALL user-facing scripts (run_*.py files)
   - List ALL manager classes that orchestrate operations
   - For EACH requirement, identify which entry point triggers it

2. **Trace Data Flow:**
   - For EACH requirement, document the complete path:
     ```
     Entry: run_simulation.py
       → SimulationManager.run_iterative_optimization()
       → ResultsManager.save_optimal_config()  ← CURRENT
       → ResultsManager.save_optimal_configs_folder()  ← REQUIRED
     ```
   - Identify WHERE in the flow the new code fits
   - Identify WHAT existing code needs to change

3. **Document Integration Points:**
   - For EACH new method/class, document:
     - What file it will be in
     - What existing method will CALL it
     - What line in the caller needs to change
   - Add these as explicit TODO tasks

4. **Verify No Orphan Code:**
   - Review each new component planned
   - Confirm each has a caller identified
   - If any new code has no caller → add integration task

---

### Fresh Eyes Review Protocol

**Purpose:** Re-read specification with fresh perspective to catch missed requirements.

**Execute during:** Iterations 17 and 18

**Steps:**

1. **Clear mental state**
   - Pretend you haven't read the spec before
   - Set aside all assumptions from previous iterations
   - Approach with beginner's mindset

2. **Read spec from start to finish**
   - Read `{feature_name}_specs.md` word by word
   - Note anything that seems unclear or incomplete
   - Mark any requirements you don't remember seeing in TODO

3. **List all requirements fresh**
   - Write requirements from scratch based on this reading
   - Don't reference your TODO while doing this
   - Number each requirement

4. **Compare to TODO**
   - Match fresh list against existing TODO tasks
   - Identify any requirements missing from TODO
   - Identify any TODO tasks not tied to requirements

5. **Document findings**
   - Add missed requirements to TODO immediately
   - Remove or question orphan tasks
   - Note confidence level in completeness

**Output:** Updated TODO with any missed requirements added.

---

### Edge Case Verification Protocol

**Purpose:** Ensure every edge case has both a task and a test.

**Execute during:** Iteration 20

**Steps:**

1. **List all edge cases from spec**
   - Search spec for words like: "if", "when", "unless", "except", "edge", "special"
   - List conditions: empty data, missing fields, zero values, max values
   - List states: bye weeks, injuries, trades, new players

2. **For each edge case, verify:**
   - [ ] Task exists in TODO to handle this case
   - [ ] Test planned that specifically tests this case
   - [ ] Expected behavior documented

3. **Create edge case matrix:**
   ```
   | Edge Case | TODO Task | Test Planned | Expected Behavior |
   |-----------|-----------|--------------|-------------------|
   | Empty roster | Task 3.2 | test_empty_roster | Return empty list |
   | Bye week | Task 4.1 | test_bye_week_handling | Score = 0, not null |
   ```

4. **Fill gaps**
   - Add tasks for unhandled edge cases
   - Add tests for untested edge cases

**Output:** Complete edge case matrix with no gaps.

---

### Test Coverage Planning Protocol

**Purpose:** Plan behavior tests that would fail if algorithm is wrong.

**Execute during:** Iteration 21

**Steps:**

1. **For each algorithm in spec:**
   - Identify the calculation or logic
   - Define expected input → output pairs
   - Define what WRONG implementation would produce

2. **Design tests that catch wrong implementations:**
   ```
   GOOD: test_player_rating_week2_uses_cumulative_points()
         - Input: Week 2, player with 20pts week 1
         - Expected: Rating based on cumulative
         - Would catch: Code using single week points

   BAD: test_player_rating_exists()
         - Only checks field exists
         - Would NOT catch: Wrong calculation
   ```

3. **For each conditional in spec:**
   - Test both branches
   - Test boundary conditions
   - Test that wrong branch would fail

4. **Document test plan:**
   ```
   | Algorithm | Test Name | Input | Expected | Catches |
   |-----------|-----------|-------|----------|---------|
   | Week scoring | test_week_2_cumulative | W2, 20pts | cumulative | single-week bug |
   ```

**Output:** Test plan with behavior tests for all algorithms.

---

### Implementation Readiness Protocol

**Purpose:** Final checklist before starting to write code.

**Execute during:** Iteration 24

**Steps:**

1. **Verify all iterations complete:**
   - [ ] Iterations 1-23 marked complete in tracker
   - [ ] All protocol results documented
   - [ ] No pending items in any round

2. **Verify TODO completeness:**
   - [ ] Every spec requirement has a task
   - [ ] Every task has file path and line numbers
   - [ ] Every new method has caller modification task
   - [ ] Integration matrix is complete

3. **Verify test readiness:**
   - [ ] Test file locations identified
   - [ ] Test patterns from codebase documented
   - [ ] Behavior tests planned (not just structure tests)

4. **Final confidence check:**
   - [ ] No "TBD" or "TODO" placeholders in plan
   - [ ] No questions waiting for answers
   - [ ] No ambiguous requirements remaining

5. **Create implementation order:**
   - List tasks in dependency order
   - Mark which tests to write first
   - Identify rollback points

**Output:** "READY TO IMPLEMENT" or list of blockers.

---

### The Infrastructure Trap

A common failure pattern:
1. Create new methods/classes with tests
2. Tests pass
3. **BUT**: Methods never called from entry points
4. **RESULT**: Feature appears complete but doesn't work for users

**Example**: Created `save_optimal_configs_folder()` but `SimulationManager` still calls `save_optimal_config()`.

### Red Flags to Watch For

- "I created a new method but didn't modify any existing code to call it"
- "The tests pass but I haven't run the actual script"
- "I built the infrastructure but the manager still uses the old approach"
- "I changed the output format but entry scripts still look for the old format"

---

## Post-Implementation Protocols

### Requirement Verification Protocol

**Purpose:** Final verification before marking objective complete.

**Execute:** After all implementation work appears complete, before moving to done/.

**Steps:**

**Step 1: Re-read Original Requirements File**
- Open and read EVERY LINE of the specification file: `feature-updates/{feature_name}/{feature_name}_specs.md`
- Create a checklist of EVERY requirement mentioned (numbered or implied)
- For each requirement, verify it has been implemented
- Mark each requirement as DONE or MISSING

**Step 2: Re-read Question Answers File**
- Open and read EVERY ANSWER in `feature-updates/{feature_name}/{feature_name}_questions.md`
- Create a checklist of EVERY answer that implies implementation work
- For each answer, verify the implementation matches what was answered
- Mark each answer as IMPLEMENTED or NOT IMPLEMENTED

**Step 3: Search Codebase for Implementation**
- Use Grep/Glob tools to search for evidence of each requirement
- Verify files were actually modified as required
- Check that new files were created if specified
- Confirm no placeholder code or TODOs remain

**Step 3.5: Algorithm Verification (CRITICAL)**

For each algorithm/calculation in the spec, verify the implementation matches **exactly**:

1. **Extract Algorithm from Spec**:
   - Quote the exact algorithm description from the original spec file
   - Note any conditional logic (if/else, week-specific, position-specific)
   - Identify edge cases mentioned in the spec

2. **Read Implementation Code**:
   - Open the file that implements this algorithm
   - Read the actual code line-by-line
   - Compare each condition and calculation to the spec

3. **Verify Logic Matches**:
   - For each conditional in the spec, find the corresponding code condition
   - For each calculation formula, verify the code implements it correctly
   - Check that edge cases are handled as specified

4. **Create Algorithm Verification Matrix**:
   ```
   | Spec Line | Algorithm | Code File:Line | Spec Says | Code Does | Match? |
   |-----------|-----------|----------------|-----------|-----------|--------|
   | 158-186 | projected weeks | generator.py:195 | week >= X: use projection | uses projection | YES |
   | 241-276 | player_rating | generator.py:147 | week 2+: cumulative | copies same rating | NO - MISMATCH |
   ```

5. **Fix Mismatches Immediately**:
   - Any MISMATCH requires immediate correction
   - Re-verify after fixing
   - Update tests to cover the algorithm behavior

**Common Algorithm Verification Failures**:
- Spec says "recalculate per iteration" but code calculates once
- Spec says "use value A for condition X, value B for condition Y" but code uses same value
- Spec describes conditional logic but code uses simplified unconditional logic
- Spec mentions edge cases but code doesn't handle them

**Step 4: Verify End-to-End Integration**
- For each NEW method/function created:
  - Search codebase to find what CALLS this method
  - If nothing calls it → INTEGRATION MISSING
  - Verify the caller is in the execution path from entry point
- For each requirement:
  - Trace from entry point (run_*.py) to output
  - Verify the new code is in the execution path
  - Run the actual script to confirm behavior (not just unit tests)
- Create integration evidence:
  ```
  Requirement: "Simulation outputs folders"
  New Method: save_optimal_configs_folder()
  Called By: SimulationManager.run_iterative_optimization() line 261
  Entry Point: run_simulation.py --mode iterative
  Verified: Running script produces folder output
  ```

**Step 5: Identify Missing Requirements**
- If ANY requirement is MISSING or NOT IMPLEMENTED or INTEGRATION MISSING:
  - STOP immediately
  - Update the TODO file
  - Document ALL missing requirements and integration gaps
  - Implement missing requirements before proceeding
  - Re-run this verification protocol

**Step 6: Document Verification**
- Add a "Requirements Verification" section to the code changes file
- List each requirement and its implementation status
- Include file paths and line numbers as evidence
- Confirm 100% requirement coverage

### Acceptance Criteria

- ALL requirements from original file implemented (100% coverage)
- ALL question answers reflected in implementation
- NO missing functionality or partial implementations
- Evidence of implementation exists in codebase
- All unit tests pass (100%)
- Manual testing confirms functionality works
- ALL new methods have identified callers (no orphan code)
- Integration verified from entry point to output
- Actual scripts run and produce expected behavior
- Minimum 3 quality control review rounds completed
- Lessons learned reviewed and guide updates applied

---

### Quality Control Review Protocol

**Purpose:** Catch issues through multiple independent review rounds.

**Execute:** After implementation appears complete, minimum 3 rounds required.

```
┌─────────────────────────────────────────────────────────────────┐
│  ALL 3 QC ROUNDS ARE MANDATORY - NO EXCEPTIONS                  │
│  Do NOT skip rounds for "simple" features or time pressure      │
│  Each round catches different issue types                       │
└─────────────────────────────────────────────────────────────────┘
```

**Round 1: Initial Quality Review**
1. Re-read the specification file (`{feature_name}_specs.md`)
2. Re-read the TODO file (`{feature_name}_todo.md`)
3. Re-read the code changes file (`{feature_name}_code_changes.md`)
4. Cross-reference all three documents
5. Identify any discrepancies, missing items, or incorrect implementations
6. Document findings and fix any issues found

**Round 2: Deep Verification Review**
1. With fresh perspective, repeat the same review process
2. Focus on algorithm correctness and edge cases
3. Verify conditional logic matches spec exactly
4. Check that tests actually validate the behavior (not just structure)
5. Document findings and fix any issues found

**Round 3: Final Skeptical Review**
1. Assume previous reviews missed something
2. Re-read spec with "adversarial" mindset - actively look for gaps
3. Verify every algorithm, calculation, and conditional
4. Confirm all requirements have corresponding tests
5. Document final verification status

### What to Check in Each Round

| Document | What to Verify |
|----------|---------------|
| Original Requirements | Every line has been addressed |
| TODO File | All tasks marked complete, no orphan items |
| Code Changes | All changes documented, line numbers accurate |
| Algorithm Logic | Conditional logic matches spec exactly |
| Test Coverage | Behavior tests exist (not just structure tests) |

### Round Documentation

After each round, document in the code changes file:
```
## Quality Control Round [N]
- Reviewed: [date/time]
- Issues Found: [list or "None"]
- Issues Fixed: [list or "N/A"]
- Status: PASSED / ISSUES FOUND (fixed)
```

### Why 3 Rounds? (And Why You Cannot Skip Any)

Experience shows that:
- Round 1 catches obvious issues
- Round 2 catches algorithm/logic issues missed in Round 1
- Round 3 catches subtle issues that require "adversarial" thinking

**Real-world example:** A "simple" config parameter move:
- Round 1: Verified all requirements met
- Round 2: Found outdated docstring examples that would confuse developers
- Round 3: Found inconsistent test fixture that could cause false test passes

**Each round catches issues the previous rounds missed. Skipping any round allows bugs to ship.**

---

### Lessons Learned Protocol

**Purpose:** Capture issues that could have been prevented by better planning or development processes.

**Execute:** Throughout development and QA, continuously.

**When to Update the Lessons Learned File:**

Update `{feature_name}_lessons_learned.md` whenever:

1. **During Verification Iterations**: You discover an edge case that should have been identified during planning
2. **During Implementation**: You find an issue that better verification would have caught
3. **During QA/Testing**: Tests reveal a problem the development process should have prevented
4. **After User Feedback**: The user reports something that wasn't working as expected
5. **During Quality Control Rounds**: You find issues that slipped through previous verification

**What to Capture:**

For each lesson, document:
- **What Happened**: The specific issue or problem discovered
- **Root Cause**: Why this was missed during planning or development
- **Impact**: How this affected the feature or required rework
- **Recommended Guide Update**: Specific changes to make to the planning or development guides

**Example Entry:**

```markdown
### Lesson 1: Missing Edge Case for Bye Week Handling

**Date:** 2024-12-06

**What Happened:**
During QA testing, discovered that the player data was returning 0 points for bye weeks, but the downstream calculation was treating 0 as "no data" instead of "bye week".

**Root Cause:**
The planning phase checklist didn't include a specific question about how bye weeks should be distinguished from missing data.

**Impact:**
Required rework of the data structure to add a `bye_week` flag, and modification of 3 downstream functions.

**Recommended Guide Update:**

**Which Guide:** feature_planning_guide.md

**Section to Update:** Checklist Template - Edge Cases

**Recommended Change:**
Add to the Edge Cases section:
- [ ] **Bye week handling:** How to distinguish bye weeks from missing/zero data?
```

**Mandatory Lessons Learned Triggers:**

You MUST add an entry when:
- A bug is found during QA that wasn't caught by the verification iterations
- The user reports the feature isn't working as expected
- An algorithm implementation doesn't match the spec (caught during review)
- An integration point was missed (orphan code created)
- Tests pass but actual behavior is wrong

---

### Guide Update Protocol

**Purpose:** Update planning and development guides based on lessons learned.

**Execute:** After all QA is complete, before moving folder to done/.

**Steps:**

**Step 1: Review Lessons Learned File**
1. Read through all entries in `{feature_name}_lessons_learned.md`
2. Identify which entries have actionable guide updates
3. Group updates by target guide (planning vs development)

**Step 2: Discuss Updates with User**
Present a summary to the user:
> "Based on lessons learned during this feature's development, I recommend the following updates to the guides:
>
> **Planning Guide Updates:**
> - {summary of changes}
>
> **Development Guide Updates:**
> - {summary of changes}
>
> Would you like me to apply these updates?"

**Step 3: Apply Updates**
After user approval:
1. Update `feature-updates/guides/feature_planning_guide.md` with approved changes
2. Update `feature-updates/guides/feature_development_guide.md` with approved changes
3. Mark the "Guide Update Status" section in lessons learned as complete

**Step 4: Document in Lessons Learned**
Update the "Guide Update Status" checklist:
```markdown
## Guide Update Status

- [x] All lessons documented
- [x] Recommendations reviewed with user
- [x] feature_planning_guide.md updated
- [x] feature_development_guide.md updated
- [x] Updates verified by user
```

---

### Pre-commit Validation Protocol

**Purpose:** Ensure code quality before every commit.

**Execute:** At completion of EVERY phase, step, or significant change.

**When to Execute:**
- After completing ANY phase step
- Before moving to the next phase or step
- When instructed to "validate and commit" or "commit changes"
- At any major milestone or completion point
- Before asking user for validation to proceed

**Steps:**

**1. Run Unit Tests (MANDATORY)**

```bash
python tests/run_all_tests.py
```

- 100% pass rate required
- Exit code 0 = safe to commit
- Exit code 1 = DO NOT COMMIT

**2. Analyze Changes**

```bash
git status
git diff
```

- Review ALL changed files
- Understand impact of changes

**3. Add/Update Unit Tests**

- Add tests for new functionality in `tests/` directory
- Follow test structure: `tests/module_path/test_FileName.py`
- Use proper mocking to isolate functionality
- Ensure tests follow Arrange-Act-Assert pattern

**Algorithm Behavior Tests (CRITICAL):**
- For each algorithm/calculation in the spec, write tests that verify:
  - The calculation produces expected output for known inputs
  - Conditional logic works correctly (test both branches)
  - Edge cases are handled as specified
- **Structure tests don't catch algorithm bugs** - a file can exist with wrong logic
- Write tests that would FAIL if the algorithm is implemented incorrectly

**4. Manual Testing (if applicable)**

```bash
python run_league_helper.py   # League helper mode
python run_player_fetcher.py  # Player data fetcher
python run_simulation.py      # Simulation system
```

**5. Update Documentation**
- Update README.md if functionality changed
- Update CLAUDE.md if workflow or architecture changed
- Update module-specific documentation as needed

**6. Commit Standards**
- Format: "Brief description of change"
- Keep under 50 characters when possible
- NO emojis or icons
- Do NOT include "Generated with Claude Code" footer

### Failure Protocol

- **If ANY test fails**: STOP immediately, fix the issue, re-run tests
- **If unit tests fail**: Fix failing tests, ensure 100% pass rate before proceeding
- **No exceptions**: Cannot proceed to next phase without 100% test success
- **Cannot commit**: Do NOT commit code with failing tests

---

## Integration Checklist Template

Use this template when verifying integration during iterations 7, 14, and 23:

```markdown
## Integration Verification

### New Component: [ClassName.method_name()]
- [ ] Method implemented
- [ ] Unit tests pass
- [ ] Called from: [CallerClass.caller_method()]
- [ ] Caller modified to use new method
- [ ] Entry point tested: [script_name.py]
- [ ] Output verified: [expected output description]
```

---

## Related Files

| File | Purpose |
|------|---------|
| `feature_development_guide.md` | Core workflow (references these protocols) |
| `feature_planning_guide.md` | Planning phase workflow |
| `templates.md` | File templates for features |
| `README.md` | Guide overview |
