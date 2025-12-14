# Feature Development Guide

This guide covers the implementation workflow for features that have completed the planning phase.

**Related Files:**
- `protocols_reference.md` - Detailed protocol definitions
- `templates.md` - File templates for TODO, questions, code changes

---

## Quick Start (6 Steps)

1. **Check prerequisites** - Feature folder exists with approved `_specs.md` and all checklist items `[x]`
2. **Create TODO file** - Use template from `templates.md`, populate from `_specs.md`
3. **Complete ALL 24 iterations** - 3 rounds (7 + 9 + 8) - **NO EXCEPTIONS, even for "simple" features**
4. **Implement changes** - Execute TODO tasks with 100% test pass rate after each phase
5. **Complete ALL 3 QC rounds** - **NO EXCEPTIONS** - then move folder to `done/`
6. **Commit changes** - Create commit with descriptive message summarizing the feature

```
┌─────────────────────────────────────────────────────────────────┐
│  WARNING: Steps 3 and 5 are MANDATORY                           │
│  Do NOT skip iterations or QC rounds for ANY reason             │
│  "Simple" features still require full verification              │
└─────────────────────────────────────────────────────────────────┘
```

**CRITICAL:** Update the README.md "Agent Status" section after completing each major step. This ensures continuity if the session is interrupted.

**Need to resume?** → See "Resuming Work Mid-Development" section below.

---

## Common Mistakes to Avoid

| Mistake | Why It's Bad | Prevention |
|---------|--------------|------------|
| Using `_notes.txt` instead of `_specs.md` | Notes are scratchwork; specs are the approved plan | **Always use `_specs.md`** as primary specification |
| Skipping iterations for "simple" features | Even simple changes have hidden complexity; bugs slip through | **Complete ALL 24 iterations** - no exceptions |
| Skipping QC rounds | Each round catches different bug types; subtle issues slip through | **Complete ALL 3 QC rounds** - no exceptions |
| "Just implementing" without verification | Miss integration gaps, dependencies, edge cases | **Never write code before iteration 24** |
| Creating orphan code | Methods exist but are never called; feature doesn't work | Use **Integration Gap Check** - every new method needs a caller |
| Simplified algorithm logic | Spec says "if X then A, else B" but code uses only A | Use **Algorithm Traceability Matrix** - match spec exactly |
| Tests pass but behavior wrong | Structure tests don't catch logic errors | Write **behavior tests** that would fail if algorithm is wrong |
| Heavy mocking hides real bugs | Mocked tests pass but real code has issues | Write **integration tests with real objects** (see Testing Anti-Patterns) |
| Output existence ≠ correctness | Files exist but contain wrong data | Write **output content validation tests** that verify file contents |
| Untested private methods | Critical logic in private methods never exercised | Test **private methods with critical logic** through their callers or directly |
| Parameter dependencies missed | Updating param A requires updating param B | Use **Parameter Dependency Check** - document and test all dependencies |
| Thinking "I know what to do" | Assumptions are often wrong; research validates | **Always research codebase** before assuming |

---

## Critical Warning: The Infrastructure Trap

```
┌─────────────────────────────────────────────────────────────────┐
│  ⚠️  THE INFRASTRUCTURE TRAP - MOST COMMON FAILURE PATTERN      │
└─────────────────────────────────────────────────────────────────┘
```

A common failure pattern that causes features to appear complete but not work:

1. Create new methods/classes with tests
2. Tests pass ✓
3. **BUT**: Methods never called from entry points
4. **RESULT**: Feature appears complete but doesn't work for users

**Example**: Created `save_optimal_configs_folder()` method, tests pass, but `SimulationManager` still calls the old `save_optimal_config()` method.

**Red Flags to Watch For:**
- "I created a new method but didn't modify any existing code to call it"
- "The tests pass but I haven't run the actual script"
- "I built the infrastructure but the manager still uses the old approach"
- "I changed the output format but entry scripts still look for the old format"

**Prevention:** The Integration Gap Check protocol (iterations 7, 14, 23) specifically catches this. Every new method MUST have:
1. A task to modify the caller
2. An entry in the Integration Matrix
3. Verification that it's in the execution path from entry point to output

---

## Critical Warning: Testing Anti-Patterns

```
┌─────────────────────────────────────────────────────────────────┐
│  ⚠️  TESTING ANTI-PATTERNS - TESTS PASS BUT BUGS EXIST          │
└─────────────────────────────────────────────────────────────────┘
```

These patterns cause tests to pass while bugs remain undetected:

### Anti-Pattern 1: Heavy Mocking Hides Real Bugs

**Problem:** Tests mock dependencies so thoroughly that actual code paths are never executed.

**Example:** Tests mock `ConfigGenerator`, `ParallelRunner`, and `ResultsManager`. The real `_update_base_config_param` method never runs, so bugs in parameter update logic go undetected.

**Prevention:**
- Write at least ONE integration test per feature that uses **real objects** (not mocks)
- Reserve mocking for external I/O (APIs, file systems) - not internal classes
- Ask: "If I change the implementation, would this test fail?"

### Anti-Pattern 2: Output Existence Tests (Files Exist ≠ Files Correct)

**Problem:** Tests verify output files exist but don't validate their contents.

**Example:**
```python
# BAD: Only checks file exists
assert (output_path / 'config.json').exists()

# GOOD: Validates file contents
config = json.load(open(output_path / 'config.json'))
assert config['DRAFT_ORDER'][0] == expected_draft_order[0]
```

**Prevention:**
- Every output file test must include **content validation**
- Check that related fields are consistent (e.g., `DRAFT_ORDER_FILE: 3` means `DRAFT_ORDER` matches file 3)
- Verify output formats match expected schemas

### Anti-Pattern 3: Untested Private Methods with Critical Logic

**Problem:** Private methods (`_method_name`) contain critical business logic but are never tested because they're "internal."

**Example:** `_update_base_config_param` handles all parameter updates in iterative optimization but has zero test coverage.

**Prevention:**
- Identify private methods with **branching logic** (if/elif/else)
- Test through callers with specific inputs that exercise each branch
- OR test directly if logic is complex enough to warrant it

### Anti-Pattern 4: Missing Parameter Dependency Tests

**Problem:** Parameters have semantic dependencies that aren't captured in tests.

**Example:** `DRAFT_ORDER_FILE` is a pointer to a file; updating it requires also updating `DRAFT_ORDER` array. Tests don't verify this relationship.

**Prevention:**
- Document parameter dependencies explicitly in specs
- Create tests that verify: "When X changes, Y is also updated correctly"
- Use the **Parameter Dependency Checklist** below

### Parameter Dependency Checklist

When adding parameters that reference other data, verify:

```
□ Parameter has clear documentation of what it references
□ Test exists that changes the parameter and verifies dependent data updates
□ Update method handles both the parameter AND its dependencies
□ Output validation test confirms parameter and dependencies are consistent
```

**Real Example:** For `DRAFT_ORDER_FILE`:
- [x] Documentation: "Points to draft_order_possibilities/{N}_*.json file"
- [x] Test: When `DRAFT_ORDER_FILE` changes from 1 to 3, `DRAFT_ORDER` array matches file 3
- [x] Update method: `_update_base_config_param` copies both `DRAFT_ORDER_FILE` AND `DRAFT_ORDER`
- [x] Output test: Saved config has `DRAFT_ORDER` matching `DRAFT_ORDER_FILE`

---

## Critical Warning: No Skipping Iterations

```
┌─────────────────────────────────────────────────────────────────┐
│  ⚠️  NEVER SKIP ITERATIONS - NO EXCEPTIONS                       │
└─────────────────────────────────────────────────────────────────┘
```

**ALL 24 verification iterations and ALL 3 QC rounds are MANDATORY.** There are no exceptions, regardless of:

- Feature complexity ("it's a simple change")
- Time pressure ("we need this done quickly")
- Confidence level ("I already know what needs to be done")
- Feature size ("it's just a config change")

### Why Simple Features Still Need All Iterations

**Real-world example:** A "simple" feature to move a config parameter from base config to week configs seemed trivial:
- Just remove from one file, add to four files
- One line change in a Python file

**What the iterations caught:**
- QC Round 2 found outdated docstring examples that would confuse future developers
- QC Round 3 found an inconsistent test fixture that could cause false positives

**Without iterations, these bugs would have been committed.**

### The False Economy of Skipping

| Skipping | Consequence |
|----------|-------------|
| "Save time by skipping iterations" | Bugs found later cost 10x more to fix |
| "Feature is too simple to need QC" | Subtle issues slip through, cause production bugs |
| "I'll just implement and test" | Miss integration gaps, orphan code, inconsistencies |

### Enforcement

- **Pre-implementation:** Complete iterations 1-24 before writing any implementation code
- **Post-implementation:** Complete QC rounds 1-3 before committing
- **No shortcuts:** Even config-only changes require full verification

---

## When to Use This Guide

Use this guide when a user says something like:
- "Prepare for updates based on {feature_name}"
- "Implement the {feature_name} feature"
- "Start development on {feature_name}"

**Prerequisites:** The user should have already completed the planning phase using `feature_planning_guide.md`. The feature folder should contain:
- `{feature_name}_specs.md` - **Primary specification** (use this for implementation)
- `{feature_name}_checklist.md` - All items should be marked [x]
- `{feature_name}_lessons_learned.md` - For capturing issues during development
- `README.md` - Status should show "Ready for Implementation"

**IMPORTANT:** Always use the `_specs.md` file as the primary specification, NOT the original `_notes.txt` scratchwork file.

---

## When You Get Stuck

| Situation | Action |
|-----------|--------|
| Can't find code pattern | Search with different terms; check imports; ask user |
| Conflicting requirements | Document conflict in TODO; ask user to clarify |
| Spec is ambiguous | Add to questions file; don't guess |
| Tests keep failing | Read error carefully; check if test or code is wrong |
| User unresponsive | Document state clearly in TODO; pause at checkpoint |
| Context window running low | Update TODO with current state; summarize progress |

---

## Communication Guidelines

How often to update the user during development:

| Phase | Communication Level | What to Report |
|-------|---------------------|----------------|
| **Verification Rounds** | Per round (not per iteration) | "Completed round 1 (7 iterations). Found X issues, updated TODO." |
| **Step 3 Questions** | Always communicate | Present questions file, wait for answers |
| **Implementation** | Per phase | "Completed phase 2. Tests passing. Moving to phase 3." |
| **QC Rounds** | Per round | "QC Round 1 complete. Found X issues, fixed Y." |
| **Blockers** | Immediately | Any issue that prevents progress |

**Do NOT:**
- Report every single iteration (too verbose)
- Stay silent for entire rounds (user loses visibility)
- Wait until end to reveal problems (fix issues early)

**DO:**
- Summarize at natural checkpoints (end of rounds, end of phases)
- Report blockers immediately
- Confirm completion of major milestones

---

## Context Window Management

When working on long features, context windows may fill up. Follow these practices:

### Proactive State Preservation

**At end of each verification round**, update the TODO file with:
```markdown
## Progress Notes

**Last Updated:** {date/time}
**Current Status:** Completed Round 1, starting Round 2
**Current Iteration:** 8
**Next Steps:** Execute iterations 8-16, then questions file
**Blockers:** None
```

### Signs Context is Running Low

- Conversation becoming very long
- User mentions session may end soon
- You're losing track of earlier decisions

### Before Context Ends

1. **Update TODO file** with current iteration and status
2. **Update Progress Notes** section with what's done vs remaining
3. **Commit any changes** to preserve work
4. **Inform user**: "I've updated the TODO file with current state. A future agent can resume from iteration X."

### What to Preserve

| Always Update | Before Session Ends |
|---------------|---------------------|
| Iteration Progress Tracker | Mark current iteration |
| Protocol Execution Tracker | Mark completed protocols |
| Integration Matrix | Add any new entries |
| Progress Notes | Current status + next steps |

---

## Resuming Work Mid-Development

If you're picking up development work started by a previous agent:

1. **Read the TODO file first**: `feature-updates/{feature_name}/{feature_name}_todo.md`
   - Check "Iteration Progress Tracker" to see which iteration you're on
   - Look for tasks marked `[ ]` (pending) vs `[x]` (complete)

2. **Determine current stage:**
   | TODO State | Current Stage | Next Action |
   |------------|---------------|-------------|
   | No TODO file exists | Pre-Step 1 | Create draft TODO from specs |
   | "First Round: X/7 iterations" | Step 2 | Continue verification iterations |
   | "Questions file created" | Step 3 | Check if user answered; if yes, go to Step 4 |
   | "Second Round: X/9 iterations" | Step 5 | Continue verification iterations |
   | "Third Round: X/8 iterations" | Step 6 | Continue verification iterations |
   | "24 iterations complete" | Implementation | Execute TODO tasks |
   | All tasks complete | Post-implementation | Run QC rounds, verify requirements |

3. **Read supporting files:**
   - `{feature_name}_specs.md` - The specification (source of truth)
   - `{feature_name}_questions.md` - User's answers (if exists)
   - `{feature_name}_code_changes.md` - What's already been implemented

4. **Check test status:**
   ```bash
   python tests/run_all_tests.py
   ```

5. **Continue from current stage** - Don't restart verification rounds

---

## Workflow Overview

```
PRE-IMPLEMENTATION (24 verification iterations total)
┌─────────────────────────────────────────────────────────────────┐
│ STEP 1: Create Draft TODO                                       │
│         Read _specs.md → Create {feature_name}_todo.md          │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 2: First Verification Round (7 iterations)                 │
│         1-3: Standard verification                              │
│         4: Algorithm Traceability Matrix                        │
│         5: End-to-End Data Flow                                 │
│         6: Skeptical Re-verification                            │
│         7: Integration Gap Check                                │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 3: Create Questions File                                   │
│         Create {feature_name}_questions.md                      │
│         WAIT for user answers                                   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 4: Update TODO with Answers                                │
│         Integrate user decisions into plan                      │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 5: Second Verification Round (9 iterations)                │
│         8-10: Verification with answers                         │
│         11: Algorithm Traceability                              │
│         12: End-to-End Data Flow                                │
│         13: Skeptical Re-verification                           │
│         14: Integration Gap Check                               │
│         15-16: Final preparation                                │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 6: Third Verification Round (8 iterations)                 │
│         17-18: Fresh Eyes Review                                │
│         19: Algorithm Deep Dive                                 │
│         20: Edge Case Verification                              │
│         21: Test Coverage Planning                              │
│         22: Skeptical Re-verification #3                        │
│         23: Integration Gap Check #3                            │
│         24: Implementation Readiness Checklist                  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
IMPLEMENTATION
┌─────────────────────────────────────────────────────────────────┐
│ Execute TODO tasks                                              │
│ Update {feature_name}_code_changes.md incrementally             │
│ Run tests after each phase (100% pass required)                 │
└─────────────────────────────────────────────────────────────────┘
                              ↓
POST-IMPLEMENTATION
┌─────────────────────────────────────────────────────────────────┐
│ 1. Run all unit tests (100% pass required)                      │
│ 2. Execute Requirement Verification Protocol                    │
│ 3. Complete 3 Quality Control Review Rounds                     │
│ 4. Review Lessons Learned → Update guides                       │
│ 5. Move folder to feature-updates/done/                         │
│ 6. Commit changes with descriptive message                      │
└─────────────────────────────────────────────────────────────────┘
```

---

## Agent Quick Reference Checklist

```
□ PRE-IMPLEMENTATION
  □ STEP 1: Create draft TODO from _specs.md
    □ ⚡ UPDATE README Agent Status: Phase=DEVELOPMENT, Step=Step 1 complete
  □ STEP 2: First verification round (7 iterations)
    □ 1-3: Standard verification (read, question, research, update)
    □ 4: Algorithm Traceability Matrix
    □ 5: End-to-End Data Flow
    □ 6: Skeptical Re-verification
    □ 7: Integration Gap Check
    □ ⚡ UPDATE README Agent Status: Step=Step 2 complete (7/24 iterations)
  □ STEP 3: Create questions file → WAIT for user answers
    □ ⚡ UPDATE README Agent Status: Step=Step 3 - Awaiting user answers
  □ STEP 4: Update TODO with user answers
  □ STEP 5: Second verification round (9 iterations)
    □ 8-10: Verification with answers
    □ 11: Algorithm Traceability
    □ 12: End-to-End Data Flow
    □ 13: Skeptical Re-verification
    □ 14: Integration Gap Check
    □ 15-16: Final preparation
    □ ⚡ UPDATE README Agent Status: Step=Step 5 complete (16/24 iterations)
  □ STEP 6: Third verification round (8 iterations)
    □ 17-18: Fresh Eyes Review
    □ 19: Algorithm Deep Dive (Algorithm Traceability)
    □ 20: Edge Case Verification
    □ 21: Test Coverage Planning
    □ 22: Skeptical Re-verification #3
    □ 23: Integration Gap Check #3
    □ 24: Implementation Readiness Checklist
    □ ⚡ UPDATE README Agent Status: Step=Step 6 complete (24/24 iterations)
  □ Create {feature_name}_code_changes.md

□ IMPLEMENTATION
  □ Execute TODO tasks phase by phase
  □ Update code_changes.md after each change
  □ Update lessons_learned.md when issues found
  □ Run tests after each phase (100% pass required)
  □ ⚡ UPDATE README Agent Status: Step=Implementation complete

□ POST-IMPLEMENTATION
  □ Run all unit tests: python tests/run_all_tests.py
  □ Execute Requirement Verification Protocol
    □ ⚡ UPDATE README Agent Status: Phase=POST-IMPLEMENTATION
  □ Quality Control Round 1: Initial review
    □ ⚡ UPDATE README Agent Status: Step=QC Round 1 complete
  □ Quality Control Round 2: Deep verification
    □ ⚡ UPDATE README Agent Status: Step=QC Round 2 complete
  □ Quality Control Round 3: Final skeptical review
    □ ⚡ UPDATE README Agent Status: Step=QC Round 3 complete
  □ Review lessons_learned.md → Propose guide updates
  □ Get user approval for guide updates
  □ Apply approved updates to guides
  □ Move folder to feature-updates/done/
    □ ⚡ UPDATE README Agent Status: Phase=COMPLETE
  □ Commit changes with descriptive message
```

**⚡ = Status Update Required**: These steps update the README "Agent Status" section to ensure session continuity.

---

## Complete Iteration Reference

Use this table to know exactly what to do at each iteration:

| # | Name | Type | Protocol | Focus |
|---|------|------|----------|-------|
| 1 | Files & Patterns | Standard | - | What files need modification? What patterns exist? |
| 2 | Error Handling | Standard | - | What error handling needed? What logging? |
| 3 | Integration Points | Standard | - | What integration points? What test mocking? |
| 4 | Algorithm Mapping | Special | Algorithm Traceability | Map spec algorithms → code locations |
| 5 | Data Flow Trace | Special | End-to-End Data Flow | Trace entry point → output |
| 6 | Assumption Check | Special | Skeptical Re-verification | Challenge all assumptions |
| 7 | Caller Check | Special | Integration Gap Check | Verify every method has a caller |
| 8 | Answer Integration | Standard | - | Re-verify with user answers |
| 9 | Answer Verification | Standard | - | Continue answer integration |
| 10 | Dependency Check | Standard | - | Verify dependencies and imports |
| 11 | Algorithm Re-verify | Special | Algorithm Traceability | Re-verify algorithms with answers |
| 12 | Data Flow Re-trace | Special | End-to-End Data Flow | Re-trace with answers integrated |
| 13 | Assumption Re-check | Special | Skeptical Re-verification | Challenge answer interpretations |
| 14 | Caller Re-check | Special | Integration Gap Check | Final caller verification |
| 15 | Final Preparation | Standard | - | Finalize task details |
| 16 | Integration Checklist | Standard | - | Create integration checklist |
| 17 | Fresh Eyes #1 | Special | Fresh Eyes Review | Re-read spec as if first time |
| 18 | Fresh Eyes #2 | Special | Fresh Eyes Review | Continue fresh perspective review |
| 19 | Algorithm Deep Dive | Special | Algorithm Traceability | Quote exact spec text; verify match |
| 20 | Edge Cases | Special | Edge Case Verification | Each edge case has task + test |
| 21 | Test Planning | Special | Test Coverage Planning | Plan behavior tests; avoid Testing Anti-Patterns |
| 22 | Final Assumption Check | Special | Skeptical Re-verification | Final assumption challenge |
| 23 | Final Caller Check | Special | Integration Gap Check | Final orphan code check |
| 24 | Readiness Check | Special | Implementation Readiness | Final checklist before coding |

---

## Protocol Quick Reference

| Protocol | Iterations | Purpose | Details |
|----------|------------|---------|---------|
| **Standard Verification** | 1-3, 8-10, 15-16 | Read → Question → Research → Update | See below |
| **Algorithm Traceability** | 4, 11, 19 | Ensure spec logic matches code exactly | `protocols_reference.md` |
| **End-to-End Data Flow** | 5, 12 | Trace entry point → output; no orphan code | `protocols_reference.md` |
| **Skeptical Re-verification** | 6, 13, 22 | Assume nothing; re-verify all claims | `protocols_reference.md` |
| **Integration Gap Check** | 7, 14, 23 | Every new method has a caller | `protocols_reference.md` |
| **Fresh Eyes Review** | 17, 18 | Re-read spec with fresh perspective | `protocols_reference.md` |
| **Edge Case Verification** | 20 | Every edge case has task + test | `protocols_reference.md` |
| **Test Coverage Planning** | 21 | Plan behavior tests; avoid anti-patterns | See "Testing Anti-Patterns" section above |
| **Implementation Readiness** | 24 | Final checklist before coding | `protocols_reference.md` |
| **Requirement Verification** | Before complete | 100% spec coverage | `protocols_reference.md` |
| **Quality Control Review** | After implementation | 3 rounds minimum | `protocols_reference.md` |

---

## Iteration Completion Checklist

Complete this checklist at the end of **every** iteration before moving to the next:

```
□ TODO file updated with findings from this iteration
□ Iteration marked complete in Progress Tracker (e.g., [x]5)
□ Protocol results documented (if special iteration - see table above)
```

**For special iterations**, also verify:
- Algorithm Traceability (4, 11, 19): Matrix updated with new mappings
- Skeptical Re-verification (6, 13, 22): Results section added to TODO
- Integration Gap Check (7, 14, 23): Integration Matrix updated

---

## Step-by-Step Workflow

### STEP 1: Create Draft TODO File

Create `feature-updates/{feature_name}/{feature_name}_todo.md` from the specification.

**Use template from:** `templates.md` → TODO File Template

**Include:**
- Iteration Progress Tracker (for tracking 24 iterations)
- High-level phases and tasks
- Anticipated file modifications
- Testing requirements
- Integration Matrix (empty, to be filled during iterations)

**Output:** TODO file created with initial structure from spec.

### STEP 2: First Verification Round (7 Iterations)

**Standard Iteration Process (1-3):**

Each standard iteration follows this pattern:

1. **Re-read source documents**
   - `{feature_name}_specs.md` (line by line)
   - Your current TODO file

2. **Ask self-clarifying questions**
   | Iteration | Focus Questions |
   |-----------|-----------------|
   | 1 | What files need modification? What patterns exist? |
   | 2 | What error handling is needed? What logging? |
   | 3 | What integration points? What mocking for tests? |

3. **Research codebase**
   - Use Glob/Grep to find relevant code
   - Look for similar implementations
   - Find test patterns to follow

4. **Update TODO file**
   - Add missing requirements
   - Add specific file paths
   - Add code references
   - Mark iteration complete in tracker

**Special Iterations:**

| Iteration | Protocol | Action |
|-----------|----------|--------|
| 4 | Algorithm Traceability | Create matrix mapping spec algorithms to code locations |
| 5 | End-to-End Data Flow | Trace each requirement from entry point to output |
| 6 | Skeptical Re-verification | Assume nothing is correct; re-verify all claims |
| 7 | Integration Gap Check | Verify every new method has a caller task |

See `protocols_reference.md` for detailed protocol steps.

**Output:** TODO file with 7 iterations complete, all protocols executed, ready for questions.

### STEP 3: Create Questions File (or Skip if None)

After 7 iterations, assess whether you have questions for the user.

**If you HAVE questions:**
1. Create `{feature_name}_questions.md` using template from `templates.md`
2. Include for each question:
   - Context section explaining WHY question arose
   - Clear, answerable question
   - At least 2 options with pros/cons
   - Agent recommendation with justification
   - Space for user answer

```
┌─────────────────────────────────────────────────────────────────┐
│  🛑 STOP HERE - WAIT FOR USER ANSWERS                           │
│                                                                 │
│  Do NOT proceed to Step 4 until user provides answers.         │
│  Present questions file to user and wait for their input.      │
└─────────────────────────────────────────────────────────────────┘
```

**If you have NO questions:**
1. Inform the user: "I've completed the first verification round (7 iterations) and have no questions - the spec is clear and complete."
2. Skip Step 4 (no answers to integrate)
3. Proceed directly to Step 5 (Second Verification Round)
4. Note in TODO: "No questions file needed - spec was complete"

**Output:** Questions file created and presented to user, OR confirmation that no questions exist.

### STEP 4: Update TODO with Answers

Integrate user's answers into the TODO:
- Update chosen approaches
- Add new tasks from answers
- Adjust priorities

**Output:** TODO file updated with user decisions integrated.

### STEP 5: Second Verification Round (9 Iterations)

| Iterations | Focus |
|------------|-------|
| 8-10 | Standard verification with user answers integrated |
| 11 | Algorithm Traceability (re-verify algorithms with answers) |
| 12 | End-to-End Data Flow (re-trace with answers) |
| 13 | Skeptical Re-verification (verify answer interpretation) |
| 14 | Integration Gap Check (final review) |
| 15-16 | Final preparation, create integration checklist |

**Output:** TODO file with 16 iterations complete, integration checklist created.

### STEP 6: Third Verification Round (8 Iterations)

| Iteration | Focus | Action |
|-----------|-------|--------|
| 17-18 | Fresh Eyes Review | Re-read spec as if first time |
| 19 | Algorithm Deep Dive | Quote exact spec text; verify code matches |
| 20 | Edge Case Verification | Each edge case has task + test |
| 21 | Test Coverage Planning | Plan behavior tests; check for Testing Anti-Patterns |
| 22 | Skeptical Re-verification #3 | Final assumption challenge |
| 23 | Integration Gap Check #3 | Final orphan code check |
| 24 | Implementation Readiness | Final checklist before coding |

**After 24 iterations:** TODO should be comprehensive and ready for implementation.

**Output:** Complete TODO with all 24 iterations done, "READY TO IMPLEMENT" confirmed.

---

## Implementation Phase

1. **Create code changes file**: `{feature_name}_code_changes.md`
   - Use template from `templates.md`

2. **Execute TODO tasks phase by phase**
   - Update code_changes.md after EACH change
   - Run tests after EACH phase
   - 100% pass rate required at all times

3. **Update lessons_learned.md when issues found**
   - Any edge case missed during planning
   - Any verification failure
   - Any user-reported issue

---

## Post-Implementation Phase

### 1. Run All Unit Tests

```bash
python tests/run_all_tests.py
```

100% pass rate required.

### 2. Execute Requirement Verification Protocol

See `protocols_reference.md` for detailed steps.

**Key checks:**
- Every spec line addressed
- Every question answer implemented
- Algorithm verification matrix complete
- Integration evidence documented

### 3. Complete 3 Quality Control Rounds

See `protocols_reference.md` for detailed steps.

**QC Round Checklist (verify during each round):**
```
□ Tests use real objects where possible (not excessive mocking)
□ Output file tests validate CONTENT, not just existence
□ Private methods with branching logic are tested through callers
□ Parameter dependencies are tested (changing A also updates B)
□ At least one integration test runs the actual feature end-to-end
```

Document each round in code_changes.md:
```
## Quality Control Round [N]
- Reviewed: [date/time]
- Testing Anti-Patterns Checked: [list which were verified]
- Issues Found: [list or "None"]
- Issues Fixed: [list or "N/A"]
- Status: PASSED / ISSUES FOUND (fixed)
```

### 4. Review Lessons Learned

1. Read `{feature_name}_lessons_learned.md`
2. Identify guide updates needed
3. Present summary to user
4. Apply approved updates to guides

### 5. Move to Done

Move entire folder: `feature-updates/{feature_name}/` → `feature-updates/done/{feature_name}/`

### 6. Commit Changes

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
Add simulation optimizations: shared data dirs, runner reuse

- Implement shared read-only data directories (80% I/O reduction)
- Reuse ParallelLeagueRunner across seasons
- Add ProcessPoolExecutor support for true parallelism
```

---

## Enforcement Rules

```
┌─────────────────────────────────────────────────────────────────┐
│  These rules are MANDATORY and NON-NEGOTIABLE                   │
│  NO EXCEPTIONS for "simple" features or time pressure           │
└─────────────────────────────────────────────────────────────────┘
```

| Rule | Requirement | Cannot Skip Because... |
|------|-------------|------------------------|
| **24 Iterations** | Must complete all 3 verification rounds (7 + 9 + 8) | "Simple" features still have hidden complexity |
| **Data Flow** | Must execute iterations 5, 12 | Integration gaps are invisible without tracing |
| **Skeptical Review** | Must execute iterations 6, 13, 22 | Assumptions cause bugs; verify everything |
| **Integration Check** | Must execute iterations 7, 14, 23 | Orphan code passes tests but doesn't work |
| **Algorithm Traceability** | Must create matrix for all calculations | Simplified logic causes subtle bugs |
| **Questions File** | Must create after first verification round (or document "no questions") | Unstated assumptions cause rework |
| **100% Test Pass** | Cannot commit or proceed with failing tests | Broken tests mean broken code |
| **3 QC Rounds** | Must complete ALL 3 rounds before marking done | Each round catches different issue types |
| **Lessons Learned** | Must review and apply guide updates | Prevents repeating mistakes |
| **No Orphan Code** | Every new method must have a caller | Untested integration = broken feature |
| **No Assumptions** | Research codebase to validate approach | Assumptions are often wrong |
| **No Testing Anti-Patterns** | Test behavior, not just structure | Structure tests miss logic bugs |

### Violation Response

**If ANY rule is violated:**
1. **STOP** immediately
2. **Go back** to the skipped step
3. **Complete** the skipped work fully
4. **Re-validate** all subsequent work
5. **Document** in lessons learned why the skip was attempted

**There is no "catch up later" - skipped work must be completed before proceeding.**

---

## Related Guides

| Guide | When to Use | Link |
|-------|-------------|------|
| **Planning Guide** | Before this guide - for new features | `feature_planning_guide.md` |
| **Protocols Reference** | Detailed protocol definitions | `protocols_reference.md` |
| **Templates** | File templates for features | `templates.md` |
| **Prompts Reference** | Conversation prompts for user discussions | `prompts_reference.md` |
| **Guides README** | Overview of all guides | `README.md` |

### Transition Points

**From Planning Guide → This guide:**
- Planning complete: all checklist items `[x]`
- User says "Prepare for updates based on {feature_name}"

**Back to Planning Guide:**
- If major scope changes discovered
- If new requirements need user decisions

**After completing this guide:**
- Move folder to `feature-updates/done/{feature_name}/`
- All tests passing (100%)
- Lessons learned reviewed and guide updates applied
- Changes committed with descriptive message

---

*This guide assumes planning is complete. If starting a new feature, use `feature_planning_guide.md` first.*
