# TODO Creation Guide

This guide covers creating the TODO file through 24 verification iterations. Use this BEFORE writing any implementation code.

**Related Files:**
- `protocols/README.md` - Detailed protocol definitions
- `templates.md` - File templates for TODO and other files
- `implementation_execution_guide.md` - Next guide (after TODO creation complete)

---

## ⚠️ IMPORTANT: Sub-Feature Workflow

**If your feature uses sub-features:**
- Execute this guide **ONCE PER SUB-FEATURE** (not once for entire feature)
- Complete TODO creation for Sub-feature 1, then Implementation, then Post-Implementation
- Commit changes for Sub-feature 1
- THEN move to Sub-feature 2 and repeat this guide
- **Sequential execution only** - complete one sub-feature fully before starting next

**File naming for sub-features:**
- `{feature_name}_sub_feature_{N}_{name}_todo.md`
- `{feature_name}_sub_feature_{N}_{name}_questions.md` (if needed)

**If your feature is a single feature (no sub-features):**
- Execute this guide once
- File naming: `{feature_name}_todo.md`, `{feature_name}_questions.md`

**How to tell which approach:**
- Check for `SUB_FEATURES_README.md` in feature folder
- If exists: Use sub-feature workflow
- If not exists: Use single feature workflow

---

## Quick Start (7 Steps)

1. **Verify prerequisites** - Planning complete, specs approved, checklist all `[x]`
2. **Sub-feature analysis** (if needed) - Determine if feature should be broken up
3. **Create draft TODO** - Use template, populate from specs
4. **Complete Round 1** - Iterations 1-7 (+ 4a)
5. **Create questions file** (if needed) - Present to user, wait for answers
6. **Complete Round 2** - Iterations 8-16
7. **Complete Round 3** - Iterations 17-24 (+ 23a)

**Result:** Complete TODO file ready for implementation

**Next Step:** → Proceed to `implementation_execution_guide.md`

---

## Pre-Implementation Quick Reference Checklist

```
┌─────────────────────────────────────────────────────────────────┐
│  PRE-IMPLEMENTATION PHASE CHECKLIST                             │
│  Track progress through TODO creation (24 iterations)           │
└─────────────────────────────────────────────────────────────────┘

□ STEP 0: Sub-Feature Analysis (if needed)
  □ Determine if feature should be broken into sub-features
  □ Identify all output/logging locations if modifying output

□ STEP 1: Create draft TODO from _specs.md
  □ Use template from templates.md
  □ Include iteration tracker, phases, integration matrix
  □ ⚡ UPDATE README Agent Status: Phase=DEVELOPMENT, Step=Step 1 complete

□ STEP 2: First verification round (7 iterations + 4a)
  □ 1-3: Standard verification (files, error handling, integration)
  □ 4: Algorithm Traceability Matrix
  □ 4a: TODO Specification Audit (acceptance criteria)
  □ 5: End-to-End Data Flow
  □ 6: Skeptical Re-verification
  □ 7: Integration Gap Check (verify no "Alternative:" notes remain)
  □ ⚡ UPDATE README Agent Status: Step=Step 2 complete (7/24 iterations)

  🔄 CHECKPOINT: Re-read "READY FOR IMPLEMENTATION" checklist (lines 87-93)
     ⚠️  Round 1 complete ≠ Ready for implementation
     ⚠️  You MUST complete ALL 24 iterations before implementation
     → Continue to STEP 3 (do NOT offer user choice to skip to implementation)

□ STEP 3: Create questions file → WAIT for user answers
  □ Create questions.md if needed, OR
  □ Document "no questions - spec complete"
  □ ⚡ UPDATE README Agent Status: Step=Step 3 - Awaiting user answers

□ STEP 4: Update TODO with user answers (or skip if no questions)
  □ Integrate user decisions into TODO

□ STEP 5: Second verification round (9 iterations)
  □ 8-10: Verification with answers integrated
  □ 11: Algorithm Traceability (re-verify with answers)
  □ 12: End-to-End Data Flow (re-trace with answers)
  □ 13: Skeptical Re-verification #2
  □ 14: Integration Gap Check #2
  □ 15-16: Final preparation
  □ ⚡ UPDATE README Agent Status: Step=Step 5 complete (16/24 iterations)

  🔄 CHECKPOINT: Re-read "READY FOR IMPLEMENTATION" checklist (lines 87-93)
     ⚠️  Round 2 complete (16/24) ≠ Ready for implementation
     ⚠️  8 more iterations required (Round 3: iterations 17-24)
     → Continue to STEP 6 (do NOT declare TODO complete yet)

□ STEP 6: Third verification round (8 iterations + 23a)
  □ 17-18: Fresh Eyes Review
  □ 19: Algorithm Deep Dive (quote exact spec text)
  □ 20: Edge Case Verification
  □ 21: Test Coverage Planning + Mock Audit
  □ 22: Skeptical Re-verification #3
  □ 23: Integration Gap Check #3
  □ 23a: Pre-Implementation Spec Audit (4-part audit - MUST PASS)
  □ 24: Implementation Readiness Checklist
  □ ⚡ UPDATE README Agent Status: Step=Step 6 complete (24/24 iterations)

□ Interface Verification (before declaring complete)
  □ Verify all external dependencies against source
  □ Verify data model attributes exist
  □ Check existing usage patterns

□ READY FOR IMPLEMENTATION
  □ All 24 iterations complete
  □ Iteration 23a passed (4-part audit)
  □ Iteration 24 passed (readiness checklist)
  □ No "Alternative:" or "May need to..." notes in TODO
  □ Interface verification complete
  □ ⚡ UPDATE README Agent Status: Ready for implementation
```

**⚡ = Status Update Required**: Update README "Agent Status" section for session continuity.

---

```
┌─────────────────────────────────────────────────────────────────┐
│  ⚠️  CRITICAL: NEVER SKIP MANDATORY ITERATIONS                   │
│                                                                 │
│  Historical Evidence: Feature skipped iterations → 40% QC fail  │
│                                                                 │
│  MANDATORY means MANDATORY:                                     │
│  - You MUST execute each iteration individually                 │
│  - You MUST document specific findings for each                 │
│  - You CANNOT batch-complete iterations                         │
│  - You CANNOT mark iterations complete without doing work       │
│                                                                 │
│  Each iteration MUST produce verifiable output:                 │
│  - Iteration 1-3: List of findings with file paths              │
│  - Iteration 4: Algorithm traceability matrix (40+ mappings)    │
│  - Iteration 4a: TODO acceptance criteria audit                 │
│  - Iteration 5: End-to-end data flow diagram                    │
│  - etc.                                                         │
│                                                                 │
│  If iteration produces "no new findings", document that         │
│  explicitly. Empty output ≠ skipped iteration.                  │
│                                                                 │
│  NEVER THINK: "This is too much work for a simple feature"      │
│  ALWAYS THINK: "Simple features hide complex bugs"              │
└─────────────────────────────────────────────────────────────────┘
```

---

## CRITICAL RULES - READ EVERY SESSION

```
┌─────────────────────────────────────────────────────────────────┐
│  RULES YOU MUST FOLLOW (Quick Reference)                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. ALL 24 iterations are MANDATORY - no skipping               │
│  2. Update README "Agent Status" after EVERY round              │
│  3. Every new method MUST have a caller (no orphan code)        │
│  4. Verify interfaces BEFORE planning implementation            │
│  5. When confidence is LOW - STOP and resolve first             │
│  6. Research codebase - validate all assumptions                │
│  7. Create questions file after Round 1 (or document "none")    │
│  8. Execute ALL protocols (see Protocol Quick Reference)        │
│                                                                 │
│  COMMON MISTAKES TO AVOID:                                      │
│  ✗ "This is simple, I'll skip iterations" → Bugs ship           │
│  ✗ "I know what to do" → Assumptions are wrong                  │
│  ✗ "I'll assume this method exists" → Read the actual class     │
│  ✗ "Interface probably works" → Verify against source           │
│  ✗ "Same as X means..." → Read actual file X                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Common Shortcuts to Avoid (With Consequences)

```
┌─────────────────────────────────────────────────────────────────┐
│  ⚠️  SHORTCUT DETECTION - IF YOU'RE THINKING THIS, STOP        │
└─────────────────────────────────────────────────────────────────┘
```

These are real shortcuts agents have taken. Each leads to failures:

### Shortcut #1: "I'll Skip Some Iterations - This is Simple"

❌ **Thought**: "This feature is simple, I don't need all 24 iterations"

✅ **Reality**: Simple features hide complex integration bugs. Skipping iterations = shipping broken code.

**Consequence**: QC Round 1 fails with ≥3 critical issues → full rework required

**If you think this**: STOP. Execute all 24 iterations anyway.

---

### Shortcut #2: "I Remember This Code - No Need to Read It"

❌ **Thought**: "I worked with this class before, I know its interface"

✅ **Reality**: Memory is unreliable. Classes evolve. Your assumptions are probably wrong.

**Consequence**: Runtime errors from calling non-existent methods or wrong parameters

**If you think this**: STOP. Read the actual source file right now.

---

### Shortcut #3: "I'll Verify Interfaces Later"

❌ **Thought**: "I'll assume this method exists and verify it during implementation"

✅ **Reality**: Non-existent methods mean rewriting TODO and implementation

**Consequence**: Implementation fails immediately, must return to verification

**If you think this**: STOP. Verify ALL interfaces NOW before proceeding.

---

### Shortcut #4: "Same As X Means I Don't Need to Read X"

❌ **Thought**: "Spec says 'same format as X', I know what that means"

✅ **Reality**: "Same" requires exact match - structure, fields, file count, everything

**Consequence**: Output incompatible with consumers, feature completely broken

**If you think this**: STOP. Read file X, count all files, verify exact structure.

---

### Shortcut #5: "Low Confidence is Fine - I'll Figure It Out"

❌ **Thought**: "I'm uncertain about this, but I'll proceed anyway"

✅ **Reality**: Low confidence = missing information = wrong implementation

**Consequence**: Building entirely wrong feature, complete rework required

**If you think this**: STOP. Create question for user, wait for answer.

---

### Shortcut #6: "I Can Skip TODO Spec Audit (4a and 23a)"

❌ **Thought**: "Iteration 4a and 23a are optional quality checks"

✅ **Reality**: These audits catch spec mismatches BEFORE coding

**Consequence**: Implementation won't match specs, QC fails catastrophically

**If you think this**: STOP. Execute 4a and 23a fully, must show PASSED.

---

### Shortcut #7: "Integration Matrix is Busy Work"

❌ **Thought**: "I don't need to track what calls each new method"

✅ **Reality**: Orphan code (no callers) means feature doesn't integrate

**Consequence**: Feature exists but is never executed, appears broken

**If you think this**: STOP. Complete integration matrix, verify every method has caller.

---

### Shortcut #8: "I'll Batch-Complete Multiple Iterations"

❌ **Thought**: "I can do iterations 1-7 in one pass and mark them all done"

✅ **Reality**: Each iteration has specific focus and catches different bugs

**Consequence**: Miss critical issues, verification becomes meaningless

**If you think this**: STOP. Execute each iteration individually with specific output.

---

### Shortcut #9: "Algorithm Traceability is Too Detailed"

❌ **Thought**: "I don't need to map every algorithm to exact spec text"

✅ **Reality**: Mapping ensures implementation matches specs exactly

**Consequence**: Implemented wrong algorithm, completely different behavior

**If you think this**: STOP. Create full traceability matrix (40+ mappings typical).

---

### Shortcut #10: "No Questions = I Can Skip Step 3"

❌ **Thought**: "I have no questions, so I'll skip creating questions file"

✅ **Reality**: You must document "no questions" to prove thoroughness

**Consequence**: Unclear if verification was skipped or genuinely complete

**If you think this**: STOP. Document in TODO: "No questions file needed - spec complete"

---

**REMEMBER**: Every shortcut feels like saving time. Every shortcut costs MORE time in rework.

---

## Verify Planning Phase Complete

```
┌─────────────────────────────────────────────────────────────────┐
│  ⚠️  MANDATORY: VERIFY PLANNING COMPLETE BEFORE PROCEEDING      │
└─────────────────────────────────────────────────────────────────┘
```

**BEFORE starting TODO creation**, verify planning is 100% complete:

□ Feature folder exists: `feature-updates/{feature_name}/`
□ File exists: `{feature_name}_specs.md` with approved content
□ File exists: `{feature_name}_checklist.md` with all items marked `[x]`
□ File exists: `{feature_name}_lessons_learned.md`
□ File exists: `README.md` with "Agent Status" section
□ README.md shows status: "Ready for Implementation"
□ No "Alternative:" statements remain unresolved in specs
□ No "OR" statements remain unresolved in specs
□ User has explicitly approved proceeding to implementation

**If ANY checkbox is unchecked:**
- ❌ DO NOT proceed with TODO creation
- Return to `feature_planning_guide.md` to complete planning
- Fix the incomplete items
- Re-verify this checklist

**If all checkboxes are checked:**
- ✅ Planning is complete
- ✅ Proceed with this guide (TODO Creation)
- ✅ Start with "README Agent Status Requirements" below

---

## README Agent Status Requirements (Session Continuity)

```
┌─────────────────────────────────────────────────────────────────┐
│  CRITICAL: README.md Agent Status MUST be updated at checkpoints│
└─────────────────────────────────────────────────────────────────┘
```

**Why this matters:** Session context can be compacted at any time. README.md Agent Status is the persistent state that survives compaction, allowing the next agent to continue exactly where you left off.

### When to Update

**MANDATORY update points (marked with ⚡ in this guide):**
- After Step 1, Step 2, Step 3, Step 5, Step 6
- After Interface Verification complete
- Before ending session (if interrupted)

### Template

```markdown
## Agent Status

**Last Updated:** {YYYY-MM-DD HH:MM}
**Current Phase:** DEVELOPMENT - TODO Creation
**Current Step:** Step X - {Description}
**Progress:** X/24 iterations complete
**Next Action:** {Exactly what next agent should do}
**Blockers:** {Issues or "None"}
**Notes:**
- {Key decisions}
- {Important milestones}
```

### Good Example

```markdown
## Agent Status

**Last Updated:** 2025-12-24 10:15
**Current Phase:** DEVELOPMENT - TODO Creation
**Current Step:** Step 3 - Awaiting User Answers
**Progress:** 7/24 iterations complete (Round 1 done)
**Next Action:** Wait for user answers in {name}_questions.md, then proceed to Step 5
**Blockers:** Waiting for user input on 3 questions
**Notes:**
- Completed Round 1 (iterations 1-7 + 4a)
- Algorithm Traceability Matrix: 42 mappings
- Integration Matrix complete
```

**Red Flags:** No timestamp, vague phase, no progress metric, "Continue" without specifics

---

## Pre-Flight Checklist

```
┌─────────────────────────────────────────────────────────────────┐
│  ✓ VERIFY BEFORE STARTING ANY WORK                              │
└─────────────────────────────────────────────────────────────────┘
```

Complete this checklist BEFORE starting Step 1 (TODO creation):

| Check | How to Verify | If Failed |
|-------|---------------|-----------|
| Feature folder exists | `feature-updates/{feature_name}/` is present | Run Planning Guide first |
| `_specs.md` is approved | README shows "Ready for Implementation" | Complete planning phase |
| All checklist items resolved | `_checklist.md` has all `[x]` checkboxes | Resolve pending items first |
| No "Alternative:" notes | Search `_specs.md` for "Alternative:" or "OR" | Resolve alternatives with user |
| Dependencies documented | `_specs.md` lists files to modify | Add dependency section |
| Unit tests currently pass | `python tests/run_all_tests.py` exits 0 | Fix tests before adding changes |

**Why this matters:** Starting development with incomplete planning leads to rework. Each failed check represents a gap that will surface during verification iterations, costing more time than resolving it upfront.

---

## Common Mistakes to Avoid (During Verification)

| Mistake | Why It's Bad | Prevention |
|---------|--------------|------------|
| Using `_notes.txt` instead of `_specs.md` | Notes are scratchwork; specs are the approved plan | **Always use `_specs.md`** as primary specification |
| Skipping iterations for "simple" features | Even simple changes have hidden complexity; bugs slip through | **Complete ALL 24 iterations** - no exceptions |
| "Just planning" without verification | Miss integration gaps, dependencies, edge cases | **Never skip verification iterations** |
| Creating orphan code plans | Methods planned but no caller identified | Use **Integration Gap Check** - every new method needs a caller |
| Simplified algorithm logic | Spec says "if X then A, else B" but plan uses only A | Use **Algorithm Traceability Matrix** - match spec exactly |
| Thinking "I know what to do" | Assumptions are often wrong; research validates | **Always research codebase** before assuming |
| Assuming interface matches similar class | Methods like `log_interval=10` may not exist on similar classes | **Verify interfaces against source** - read actual class definitions |
| Using getattr with silent defaults | `getattr(obj, 'attr', None)` hides missing attributes | **Use explicit attribute access** for required attributes |
| Leaving "Alternative:" notes unresolved | Deferred decisions cause rework during implementation | **Resolve all alternatives** during planning phase |
| "Mirror X" without reading X | Spec says "mirror run_simulation.py" but only method signatures copied, not file organization | **Existing Pattern Audit** - read entire file and document ALL patterns |

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

## Critical Warning: Red Flag Self-Check

```
┌─────────────────────────────────────────────────────────────────┐
│  🚩 RED FLAG CHECKLIST - STOP IF ANY OF THESE ARE TRUE         │
└─────────────────────────────────────────────────────────────────┘
```

Before proceeding past any iteration or checkpoint, verify NONE of these are true:

**Interface Assumptions (causes: method not found, wrong parameters):**
- [ ] "I assumed this method exists" → STOP: Read the actual class definition
- [ ] "I assumed these parameters are correct" → STOP: Verify against source
- [ ] "This class is similar to X, so it probably has the same methods" → STOP: Verify

**Data Model Assumptions (causes: AttributeError, silent failures):**
- [ ] "I assumed this attribute exists" → STOP: Check the dataclass/model definition
- [ ] "I used getattr with a default value" → WARNING: Verify attribute actually exists
- [ ] "I didn't verify the attribute semantics" → STOP: Check if projected vs actual, etc.

**Integration Assumptions (causes: orphan code, feature doesn't work):**
- [ ] "I haven't traced from entry point to this code" → STOP: Do entry point trace
- [ ] "I created code but haven't identified what calls it" → STOP: Add caller task
- [ ] "Alternative:" or "May need to..." notes exist in TODO → STOP: Resolve first

**"Same As X" Reference Assumptions (causes: incomplete implementation):**
- [ ] "Spec says 'same as X' and I know what that means" → STOP: Read actual X, list all files
- [ ] "I'm creating 5 files because spec says 5" → STOP: Verify by reading actual reference
- [ ] "Same structure means same file count" → STOP: It also means same internal structure and all required files

**If ANY checkbox above is checked, STOP and fix before proceeding.**

**When to Run This Checklist:**
- Before marking ANY iteration complete (1-24)
- Before each round checkpoint (7, 16, 24)
- Before proceeding to implementation

---

## Critical Warning: Testing Anti-Patterns

```
┌─────────────────────────────────────────────────────────────────┐
│  ⚠️  TESTING ANTI-PATTERNS - PLAN TESTS THAT CATCH REAL BUGS    │
└─────────────────────────────────────────────────────────────────┘
```

These patterns cause tests to pass while bugs remain undetected. **Plan to avoid these during verification:**

### Anti-Pattern 1: Heavy Mocking Hides Real Bugs

**Problem:** Tests mock dependencies so thoroughly that actual code paths are never executed.

**Prevention:**
- Write at least ONE integration test per feature that uses **real objects** (not mocks)
- Reserve mocking for external I/O (APIs, file systems) - not internal classes
- Ask: "If I change the implementation, would this test fail?"

### Anti-Pattern 2: Output Existence Tests (Files Exist ≠ Files Correct)

**Problem:** Tests verify output files exist but don't validate their contents.

**Prevention:**
- Every output file test must include **content validation**
- Check that related fields are consistent
- Verify output formats match expected schemas

### Anti-Pattern 3: Untested Private Methods with Critical Logic

**Problem:** Private methods (`_method_name`) contain critical business logic but are never tested.

**Prevention:**
- Identify private methods with **branching logic** (if/elif/else)
- Plan tests through callers with specific inputs that exercise each branch

### Anti-Pattern 4: Missing Parameter Dependency Tests

**Problem:** Parameters have semantic dependencies that aren't captured in tests.

**Prevention:**
- Document parameter dependencies explicitly in TODO
- Create tests that verify: "When X changes, Y is also updated correctly"

### Anti-Pattern 5: Assumed Interface Matches

**Problem:** Developer assumes a class has the same interface as a similar class, without verifying.

**Prevention:**
- Read the actual class definition before planning its use
- Reference existing usage in codebase: `grep -r "ClassName(" .` to see how others use it

### Anti-Pattern 6: "Mirror X" Without Reading X

**Problem:** Spec says "mirror run_simulation.py structure" but developer only copies obvious elements while missing organizational patterns.

**Prevention:**
1. When spec says "mirror X", READ THE ENTIRE FILE X
2. Document ALL structural patterns found
3. Create a structural comparison checklist before implementing

### Anti-Pattern 7: Output Structure Without Consumer Validation

**Problem:** Output files/folders are created but their structure doesn't match what consumers expect.

**Prevention - OUTPUT/INPUT ROUNDTRIP RULE:**
```
┌─────────────────────────────────────────────────────────────────┐
│  MANDATORY FOR ANY FEATURE THAT PRODUCES OUTPUT FILES:          │
│                                                                 │
│  1. Identify ALL consumers of this output                       │
│  2. Read the consumer's input validation code                   │
│  3. Plan a test that feeds output back as input                 │
│  4. Test must use REAL loader, not mocked                       │
└─────────────────────────────────────────────────────────────────┘
```

**See `protocols/README.md` for complete Testing Anti-Patterns documentation.**

---

## Why Every Iteration Matters

```
┌─────────────────────────────────────────────────────────────────┐
│  THE REASONING BEHIND 24 ITERATIONS                             │
│                                                                 │
│  Each iteration type catches different bug categories:          │
│  - Standard (1-3): File paths, patterns, error handling         │
│  - Algorithm (4,11,19): Logic matches spec exactly              │
│  - Data Flow (5,12): No orphan code, complete paths             │
│  - Skeptical (6,13,22): Challenge assumptions                   │
│  - Integration (7,14,23): Everything is actually connected      │
│                                                                 │
│  Skipping iterations doesn't save time - it moves bugs from     │
│  "caught during verification" to "caught after shipping."       │
└─────────────────────────────────────────────────────────────────┘
```

**ALL 24 verification iterations are MANDATORY.** There are no exceptions, regardless of:

- Feature complexity ("it's a simple change")
- Time pressure ("we need this done quickly")
- Confidence level ("I already know what needs to be done")
- Feature size ("it's just a config change")

### Iteration Purpose Map

Each iteration type is designed to catch a specific category of bugs. If you skip an iteration type, you WILL miss bugs in that category.

| Type | Iterations | Bug Category It Catches | Example Bug It Prevents |
|------|------------|------------------------|-------------------------|
| **Standard** | 1-3, 8-10, 15-16 | Requirements gaps, missing patterns | "Forgot to handle error case" |
| **Algorithm** | 4, 11, 19 | Logic mismatches, wrong calculations | "Used + instead of * in formula" |
| **Data Flow** | 5, 12 | Broken data pipelines, orphan code | "Data never reaches output file" |
| **Skeptical** | 6, 13, 22 | Assumption failures, interface mismatches | "Method doesn't actually exist" |
| **Integration** | 7, 14, 23 | Orphan methods, missing callers | "Built it but nothing uses it" |
| **Fresh Eyes** | 17, 18 | Missed requirements from spec | "Completely forgot section 3" |
| **Edge Case** | 20 | Boundary condition failures | "Crashes on empty input" |
| **Test Coverage** | 21 | Tests that don't catch real bugs | "Test passes with wrong code" |
| **Readiness** | 24 | Incomplete preparation | "Started coding too soon" |

### Why Simple Features Still Need All Iterations

**Real-world example:** A "simple" feature to move a config parameter from base config to week configs seemed trivial, but iterations caught:
- Outdated docstring examples that would confuse future developers
- Inconsistent test fixture that could cause false positives

**Without iterations, these bugs would have been committed.**

---

## When to Use This Guide

Use this guide when a user says something like:
- "Prepare for updates based on {feature_name}"
- "Implement the {feature_name} feature"
- "Start development on {feature_name}"

**Prerequisites:** The user should have already completed the planning phase. The feature folder should contain:
- `{feature_name}_specs.md` - **Primary specification** (use this for verification)
- `{feature_name}_checklist.md` - All items should be marked [x]
- `README.md` - Status should show "Ready for Implementation"

**IMPORTANT:** Always use the `_specs.md` file as the primary specification, NOT the original `_notes.txt` scratchwork file.

---

## When You Get Stuck

| Situation | Action |
|-----------|--------|
| Can't find code pattern | Search with different terms; check imports; ask user |
| Conflicting requirements | Document conflict in TODO; ask user to clarify |
| Spec is ambiguous | Add to questions file; don't guess |
| User unresponsive | Document state clearly in TODO; pause at checkpoint |
| Context window running low | Update TODO with current state; summarize progress |

---

## Session Start Protocol (Run Every Time)

When starting or resuming work on a feature, execute this checklist BEFORE doing anything else:

```
┌─────────────────────────────────────────────────────────────────┐
│  SESSION START CHECKLIST - COMPLETE BEFORE ANY WORK             │
│  Time to complete: ~2 minutes                                   │
│  Cost of skipping: Duplicate work, lost context, missed issues  │
└─────────────────────────────────────────────────────────────────┘

□ 1. Read feature's README.md
     → Check "Agent Status" and "WHERE AM I RIGHT NOW?" sections
     → Note current phase and step

□ 2. Read TODO file (if exists)
     → Check Iteration Progress Tracker
     → Check Progress Notes section for last activity

□ 3. Read _lessons_learned.md
     → Note any issues to avoid repeating

□ 4. Run baseline test
     → python tests/run_all_tests.py
     → Must pass before making any changes

□ 5. Update README status
     → Add: "Session resumed at {time}, continuing from {step}"

□ 6. Continue from documented step
     → Do NOT restart the workflow
     → Pick up exactly where previous work left off
```

**Why This Matters:**
- Without this checklist, you may restart work that's already done
- Previous decisions may be lost or contradicted
- Issues that were already identified may be missed
- Time is wasted re-discovering context that was already documented

---

## Resuming Work Mid-Verification

If you're picking up verification work started by a previous agent:

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
   | "24 iterations complete" | Ready for Implementation | Proceed to implementation_execution_guide.md |

3. **Read supporting files:**
   - `{feature_name}_specs.md` - The specification (source of truth)
   - `{feature_name}_questions.md` - User's answers (if exists)
   - `README.md` - Agent Status section

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
│ STEP 0: Sub-Feature Analysis (if complex)                      │
│         Determine if feature should be broken into sub-features │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 1: Create Draft TODO                                       │
│         Read _specs.md → Create {feature_name}_todo.md          │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 2: First Verification Round (7 iterations + 4a)            │
│         1-3: Standard verification                              │
│         4: Algorithm Traceability Matrix                        │
│         4a: TODO Specification Audit                            │
│         5: End-to-End Data Flow                                 │
│         6: Skeptical Re-verification                            │
│         7: Integration Gap Check                                │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 3: Create Questions File (or skip if none)                 │
│         Create {feature_name}_questions.md                      │
│         WAIT for user answers (or skip if no questions)         │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 4: Update TODO with Answers (or skip if no questions)     │
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
│ STEP 6: Third Verification Round (8 iterations + 23a)           │
│         17-18: Fresh Eyes Review                                │
│         19: Algorithm Deep Dive                                 │
│         20: Edge Case Verification                              │
│         21: Test Coverage Planning + Mock Audit                 │
│         22: Skeptical Re-verification #3                        │
│         23: Integration Gap Check #3                            │
│         23a: Pre-Implementation Spec Audit                      │
│         24: Implementation Readiness Checklist                  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
                  READY FOR IMPLEMENTATION
          → Proceed to implementation_execution_guide.md
```

---

## Step-by-Step Workflow

### STEP 0: Sub-Feature Analysis (MANDATORY for complex features)

**BEFORE creating TODO files**, analyze whether the feature should be broken into sub-features.

#### When to Break Into Sub-Features

Break features into sub-features if ANY of these apply:
- Feature has 10+ distinct implementation tasks
- Feature spans multiple systems or components
- Feature has clear phases (e.g., core logic → optimization → testing)
- Feature has natural dependencies (Task A must complete before Task B)
- Feature would take multiple days/weeks to implement
- Feature scope is "comprehensive fix" or "complete rewrite"

#### How to Identify Sub-Features

Look for natural groupings:
1. **By component**: Each major class/module is a sub-feature
2. **By phase**: Setup → Implementation → Optimization → Testing
3. **By dependency**: Core fixes → New features → Performance → Validation
4. **By priority**: Critical path → Nice-to-have → Polish

#### Special Planning for Output/Logging Sub-Features

**LESSON FROM: ranking_accuracy_metrics**

When planning sub-features that modify output formatting or logging:

**Before finalizing the TODO**, perform a comprehensive search for ALL output locations:

1. **Grep for logging methods:**
   ```bash
   grep -r "self.logger.info" path/to/module.py
   grep -r "print" path/to/module.py
   ```
   List ALL matches, not just obvious ones

2. **Check for:**
   - Direct logging (logger.info, logger.warning, logger.debug)
   - Print statements (if any)
   - Console output via write() or sys.stdout
   - Progress bars or status updates
   - Summary/report generation methods
   - Parameter display methods

3. **Common patterns to search:**
   - "_log", "log_", "print_", "display_", "show_", "report_", "summary_"
   - Methods that take "verbose" or "quiet" parameters
   - Methods called at end of loops or processes
   - Methods with "format" or "display" in their names

4. **Verify completeness:**
   - Run the script and observe ALL console output
   - Compare against your list of logging locations
   - If output appears that's not in your list → missing location
   - Check both success and error code paths

**Why:** Output formatting requires consistency. If one logging method shows new format but another doesn't, users get confused. Finding all locations upfront prevents QC issues.

**Verification Checklist:**
```
□ Searched for all logger.info/warning/debug calls
□ Searched for all print statements
□ Searched for all display/show/report methods
□ Ran script to observe actual output locations
□ Listed ALL output locations in TODO
□ Created task for EACH output location to update
```

#### Sub-Feature Structure

Each sub-feature gets its own TODO file:
- `01_[name]_todo.md` - Phase 1 (highest priority/dependency)
- `02_[name]_todo.md` - Phase 2 (depends on Phase 1)
- `03_[name]_todo.md` - Phase 3 (depends on Phase 2)
- etc.

**Each TODO file follows the full 24-iteration structure** independently.

---

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

**⚡ UPDATE README Agent Status:** Phase=DEVELOPMENT, Step=Step 1 complete

---

### STEP 2: First Verification Round (7 Iterations + 4a)

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
| 4a | TODO Specification Audit | Verify TODO items have acceptance criteria from specs (MANDATORY) |
| 5 | End-to-End Data Flow | Trace each requirement from entry point to output |
| 6 | Skeptical Re-verification | Assume nothing is correct; re-verify all claims |
| 7 | Integration Gap Check | Verify every new method has a caller task |

See `protocols/README.md` for detailed protocol steps.

---

#### Iteration 4a: TODO Specification Audit (MANDATORY)

**Purpose:** Ensure every TODO item has enough detail to implement WITHOUT re-reading specs.

**Critical Question:** "Can someone implement each TODO item correctly WITHOUT re-reading specs?"

If answer is NO for ANY item, the TODO is incomplete.

**Process:**

For EACH TODO item in implementation phases:

1. **Read corresponding spec section(s)**
2. **Extract EXACT requirements:**
   - Data structures (with examples)
   - Required fields (with types)
   - Constraints (array lengths, null handling, etc.)
   - Spec line references
3. **Add Acceptance Criteria section** with:
   - ✓ Each requirement as a checkable item
   - Example of correct output
   - Anti-example of common mistake
   - Spec reference for verification
4. **Self-audit:**
   - [ ] "Can I implement this without re-reading specs?" (YES required)
   - [ ] "Do I know what the output should look like?" (YES required)
   - [ ] "Do I know what NOT to do?" (YES required)

**Red Flags** (means TODO item needs more detail):

- ⛔ "Transform to [vague description]" without showing structure
- ⛔ "Build [thing]" without listing required fields
- ⛔ "Add [feature]" without expected output example
- ⛔ "Handle [case]" without specifying correct behavior
- ⛔ Missing spec references
- ⛔ No examples of correct output

**TODO Item Quality Template:**

```markdown
- [ ] X.X: [Task name]

  ACCEPTANCE CRITERIA (from specs.md):

  ✓ REQUIREMENT 1: [Exact specification]
    - Spec: specs.md lines X-Y
    - Example: [correct output]
    - NOT: [common mistake] ❌

  ✓ REQUIREMENT 2: [Exact specification]
    ...

  VERIFICATION:
  - [ ] Passes check 1
  - [ ] Passes check 2
```

**Completion Criteria:**

- [ ] Every TODO item has Acceptance Criteria section
- [ ] Every criteria has spec reference
- [ ] Every criteria has example or anti-example
- [ ] Self-audit passes for all items

**Output:** TODO file with all items having detailed acceptance criteria.

---

#### Integration Gap Check - Additional Requirements

Before marking an integration gap check complete, verify:

1. **No "Alternative:" notes remain unresolved** - If multiple valid approaches exist for any task:
   - Document the options with pros/cons
   - Create a question in the questions file
   - DO NOT proceed past verification until user decides

2. **No "May need to..." notes remain** - Phrases like "may need to refactor" indicate uncertainty that must be resolved:
   - Investigate to determine if refactoring IS needed
   - If yes, document the approach and get user approval
   - If no, remove the note and document why not needed

3. **All DEFERRED items have valid deferral reasons:**
   - **Valid reasons:** "Will be created when X runs" (file generation), "Low priority, not blocking" (documentation)
   - **Invalid reasons:** "Requires user decision" (should have been asked during planning), "Multiple approaches possible" (should have been decided during planning)

**Why this matters:** Deferring architectural decisions to implementation causes rework.

**Output:** TODO file with 7 iterations complete, all protocols executed.

**⚡ UPDATE README Agent Status:** Step=Step 2 complete (7/24 iterations)

---

### Round Checkpoint Summary (MANDATORY after iterations 7, 16, 24)

After completing each verification round, create a checkpoint summary:

```markdown
## Round {N} Checkpoint Summary

**Completed:** {date/time}
**Iterations:** {X-Y} complete

### Key Findings
- {What was learned about the codebase}
- {Important patterns discovered}
- {Dependencies identified}

### Gaps Identified
- {What's still unclear}
- {What needs user input}
- {What needs more research}

### Scope Assessment
- Original scope items: {count}
- Items added during this round: {list any additions}
- Items removed/deferred: {list any removals}
- **Scope creep detected?** {Yes/No} - {if yes, document and ask user}

### Confidence Level
- **Level:** {High/Medium/Low}
- **Justification:** {why this confidence level}
- **Risks:** {what could still go wrong}

### Ready For
- {Next phase: questions / round 2 / implementation}
```

**Why This Matters:** Without checkpoint summaries, agents lose context and may make contradictory decisions.

---

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
╔═════════════════════════════════════════════════════════════════╗
║  🛑 🛑 🛑 MANDATORY STOP - WAIT FOR USER ANSWERS 🛑 🛑 🛑       ║
╠═════════════════════════════════════════════════════════════════╣
║                                                                 ║
║  CRITICAL GATE: Do NOT proceed to Step 4 until user provides   ║
║  answers to ALL questions in the questions file.               ║
║                                                                 ║
║  VERIFICATION QUESTIONS (All must be YES):                      ║
║  □ Have I created a questions file with all uncertainties?     ║
║  □ Have I presented this file to the user?                     ║
║  □ Have I RECEIVED answers from the user?                      ║
║  □ Are ALL questions answered (no "TBD" or "pending")?         ║
║                                                                 ║
║  CONSEQUENCES OF PROCEEDING WITHOUT ANSWERS:                   ║
║  ❌ You will implement based on wrong assumptions              ║
║  ❌ You will waste hours building the wrong thing              ║
║  ❌ You will need to redo the entire implementation            ║
║  ❌ User will be frustrated by rework                          ║
║                                                                 ║
║  ACTION REQUIRED:                                              ║
║  1. Present questions file to user                             ║
║  2. Wait for user to provide answers                           ║
║  3. Only proceed when ALL answers received                     ║
║                                                                 ║
╚═════════════════════════════════════════════════════════════════╝
```

**If you have NO questions:**
1. Inform the user: "I've completed the first verification round (7 iterations) and have no questions - the spec is clear and complete."
2. Skip Step 4 (no answers to integrate)
3. Proceed directly to Step 5 (Second Verification Round)
4. Note in TODO: "No questions file needed - spec was complete"

**Output:** Questions file created and presented to user, OR confirmation that no questions exist.

**⚡ UPDATE README Agent Status:** Step=Step 3 - Awaiting user answers (or skip to Step 5 if no questions)

---

### STEP 4: Update TODO with Answers

Integrate user's answers into the TODO:
- Update chosen approaches
- Add new tasks from answers
- Adjust priorities

**Output:** TODO file updated with user decisions integrated.

---

```
╔═════════════════════════════════════════════════════════════════╗
║  ⏸️  SELF-AUDIT CHECKPOINT: After Round 1 (Iterations 1-7)      ║
╠═════════════════════════════════════════════════════════════════╣
║                                                                 ║
║  PAUSE HERE. Answer these questions honestly:                  ║
║                                                                 ║
║  Process Compliance:                                           ║
║  □ Did I execute ALL 7 iterations individually?                ║
║  □ Did I execute iteration 4a (TODO Spec Audit)?               ║
║  □ Did each iteration produce specific findings?               ║
║  □ Did I update the Iteration Progress Tracker?                ║
║  □ Did I document "no new findings" if applicable?             ║
║                                                                 ║
║  Quality Checks:                                               ║
║  □ Have I verified ALL interfaces against actual code?         ║
║  □ Is the Algorithm Traceability Matrix complete (40+ items)?  ║
║  □ Does iteration 4a show PASSED?                              ║
║  □ Have I created questions for ALL uncertainties?             ║
║  □ Did I check Integration Matrix (all methods have callers)?  ║
║                                                                 ║
║  Red Flags (If YES to any, STOP and fix):                      ║
║  □ Did I batch-complete multiple iterations?                   ║
║  □ Did I work from memory instead of reading actual files?     ║
║  □ Did I assume methods exist without verification?            ║
║  □ Are there "Alternative:" or "TBD" notes unresolved?         ║
║  □ Is my confidence LOW on any aspect?                         ║
║                                                                 ║
║  If ANY Process Compliance checkbox is unchecked OR            ║
║  ANY Red Flag is checked:                                      ║
║  → STOP: Return and complete the missing work                  ║
║  → Do NOT proceed to Round 2                                   ║
║                                                                 ║
║  If all Process Compliance boxes checked AND                   ║
║  no Red Flags:                                                 ║
║  → Proceed to STEP 3 (Questions) or STEP 5 (Round 2)           ║
║                                                                 ║
╚═════════════════════════════════════════════════════════════════╝
```

---

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

**⚡ UPDATE README Agent Status:** Step=Step 5 complete (16/24 iterations)

---

```
╔═════════════════════════════════════════════════════════════════╗
║  ⏸️  SELF-AUDIT CHECKPOINT: After Round 2 (Iterations 8-16)     ║
╠═════════════════════════════════════════════════════════════════╣
║                                                                 ║
║  PAUSE HERE. Answer these questions honestly:                  ║
║                                                                 ║
║  Process Compliance:                                           ║
║  □ Did I execute ALL 9 iterations (8-16) individually?         ║
║  □ Did I integrate user answers into TODO?                     ║
║  □ Did each iteration produce specific findings?               ║
║  □ Did I update the Iteration Progress Tracker to 16/24?       ║
║  □ Did I re-verify Algorithm Traceability with answers?        ║
║                                                                 ║
║  Quality Checks:                                               ║
║  □ Does End-to-End Data Flow reflect user decisions?           ║
║  □ Have I resolved ALL questions from Round 1?                 ║
║  □ Is Integration Matrix updated with new methods?             ║
║  □ Did iteration 11 update traceability matrix?                ║
║  □ Did iteration 12 update data flow with answers?             ║
║                                                                 ║
║  Red Flags (If YES to any, STOP and fix):                      ║
║  □ Are there still unresolved "Alternative:" notes?            ║
║  □ Did I skip re-verifying with user answers?                  ║
║  □ Is my confidence MEDIUM or LOW on any aspect?               ║
║  □ Are there new questions that arose but not documented?      ║
║  □ Did I skip iterations 11-14 protocols?                      ║
║                                                                 ║
║  If ANY Process Compliance checkbox is unchecked OR            ║
║  ANY Red Flag is checked:                                      ║
║  → STOP: Return and complete the missing work                  ║
║  → Do NOT proceed to Round 3                                   ║
║                                                                 ║
║  If all Process Compliance boxes checked AND                   ║
║  no Red Flags:                                                 ║
║  → Proceed to STEP 6 (Round 3 - Final verification)            ║
║                                                                 ║
╚═════════════════════════════════════════════════════════════════╝
```

---

### STEP 6: Third Verification Round (8 Iterations + 23a)

| Iteration | Focus | Action |
|-----------|-------|--------|
| 17-18 | Fresh Eyes Review | Re-read spec as if first time |
| 19 | Algorithm Deep Dive | Quote exact spec text; verify code matches |
| 20 | Edge Case Verification | Each edge case has task + test |
| 21 | Test Coverage Planning | Plan behavior tests; check for Testing Anti-Patterns |
| 22 | Skeptical Re-verification #3 | Final assumption challenge |
| 23 | Integration Gap Check #3 | Final orphan code check |
| 23a | Pre-Implementation Spec Audit | 4-part fresh-eyes audit (MANDATORY) |
| 24 | Implementation Readiness | Final checklist before coding (REQUIRES 23a PASS) |

---

#### Iteration 23a: Pre-Implementation Spec Audit (MANDATORY)

**CRITICAL**: This is the final checkpoint before implementation begins.

**Purpose:** Comprehensive spec-to-TODO audit with fresh eyes

**Mindset:** Pretend you're a QA reviewer who's never seen this feature before. You have:
- ✅ The specs.md file
- ✅ The TODO.md file
- ❌ NO OTHER CONTEXT

**Your job:** Find every mismatch, missing detail, and vague instruction.

**Four-Part Audit:**

### Part 1: Spec Coverage Audit (Completeness)

For EACH section in specs.md:

1. Read spec section (e.g., "Section 2: Common Player Fields")
2. Extract all requirements from that section (list them)
3. Find corresponding TODO items that implement those requirements
4. Verify each requirement has:
   - [ ] A TODO item that addresses it
   - [ ] Acceptance criteria that matches the spec exactly
   - [ ] Spec line reference
   - [ ] Example of correct output

Red flags:
- ⛔ Spec requirement with no TODO item
- ⛔ TODO item exists but no acceptance criteria
- ⛔ Acceptance criteria doesn't match spec
- ⛔ No example showing what "correct" looks like

### Part 2: TODO Clarity Audit (Actionability)

For EACH TODO item:

1. Cover up the specs.md file (pretend you can't see it)
2. Read ONLY the TODO item
3. Ask: "Could I implement this correctly right now?"
4. If NO, identify what's missing

Red flags:
- ⛔ "Transform to..." without showing structure
- ⛔ "Build..." without listing components
- ⛔ "Include all..." without enumerating
- ⛔ No examples of correct output

### Part 3: Data Structure Audit (Exactness)

For EACH data structure mentioned in specs:

1. Find the structure in specs
2. Find corresponding TODO item
3. Verify TODO shows EXACT structure (same fields, nesting, types, arrays)

Red flags:
- ⛔ Structure described in words, not shown
- ⛔ Field names differ from spec
- ⛔ Missing required fields

### Part 4: Mapping Audit (Correctness)

For EACH mapping in specs (e.g., ESPN stat IDs to fields):

1. Find mapping table in specs
2. Find corresponding TODO item
3. Verify TODO includes complete mapping

Red flags:
- ⛔ Mapping mentioned but not shown
- ⛔ Incomplete mapping

**Completion Criteria:**

All four audits must pass:

- [ ] **Part 1 (Coverage):** Every spec requirement has TODO item with acceptance criteria
- [ ] **Part 2 (Clarity):** Every TODO item is implementable without reading specs
- [ ] **Part 3 (Structure):** Every data structure in specs is shown exactly in TODO
- [ ] **Part 4 (Mapping):** Every mapping in specs is documented in TODO

**If ANY audit fails:**
1. Document all findings
2. Update TODO with missing details
3. Re-run audit until all parts pass
4. **DO NOT proceed to Iteration 24** until audit passes

**Historical Evidence:** This iteration would have caught all 8 issues found in post-implementation QC.

**Output:** Audit report with pass/fail for all 4 parts, list of required fixes before implementation.

---

⚠️ **CRITICAL CHECKPOINT**: Iteration 23a is the final quality gate.

**Prerequisites for Iteration 24:**
- Iteration 23a (Pre-Implementation Spec Audit) MUST pass with 0 failures
- If audit failed, implementation is NOT ready regardless of other factors
- DO NOT proceed to implementation until all 4 audit parts pass

---

**After 24 iterations complete:** TODO should be comprehensive and ready for implementation.

**Output:** Complete TODO with all 24 iterations done, "READY TO IMPLEMENT" confirmed.

**⚡ UPDATE README Agent Status:** Step=Step 6 complete (24/24 iterations) - Ready for implementation

---

```
╔═════════════════════════════════════════════════════════════════╗
║  ⏸️  SELF-AUDIT CHECKPOINT: After Round 3 (Iterations 17-24)    ║
╠═════════════════════════════════════════════════════════════════╣
║                                                                 ║
║  CRITICAL PAUSE. This is your LAST checkpoint before coding.   ║
║  Answer these questions honestly:                              ║
║                                                                 ║
║  Process Compliance:                                           ║
║  □ Did I execute ALL 8 iterations (17-24) individually?        ║
║  □ Did I execute iteration 23a (Pre-Implementation Audit)?     ║
║  □ Does iteration 23a show ALL 4 PARTS PASSED?                ║
║  □ Did I execute iteration 24 (Implementation Readiness)?      ║
║  □ Does iteration 24 show confidence level: HIGH?              ║
║                                                                 ║
║  Quality Checks:                                               ║
║  □ Did I re-read specs with fresh eyes (iteration 17-18)?      ║
║  □ Is Algorithm Traceability complete with spec line quotes?   ║
║  □ Have I verified ALL edge cases have tasks + tests?          ║
║  □ Did I run Mock Audit (iteration 21)?                        ║
║  □ Is Integration Matrix 100% complete (no orphan methods)?    ║
║                                                                 ║
║  Critical Verification:                                        ║
║  □ Is there ZERO "Alternative:", "TBD", "uncertain" in TODO?   ║
║  □ Is there ZERO "May need to..." notes in TODO?               ║
║  □ Can I answer "what to build" for EVERY task?                ║
║  □ Do I know EXACTLY where each new method will be called?     ║
║  □ Is my confidence HIGH on implementation approach?           ║
║                                                                 ║
║  Red Flags (If YES to any, STOP and fix):                      ║
║  □ Did iteration 23a have ANY failures?                        ║
║  □ Is my confidence MEDIUM or LOW?                             ║
║  □ Are there unresolved assumptions or uncertainties?          ║
║  □ Did I skip Fresh Eyes Review (17-18)?                       ║
║  □ Did I skip Mock Audit (21)?                                 ║
║                                                                 ║
║  If ANY Process Compliance checkbox is unchecked OR            ║
║  ANY Red Flag is checked:                                      ║
║  → STOP: Do NOT proceed to Interface Verification              ║
║  → Return and complete the missing work                        ║
║  → You are NOT ready for implementation                        ║
║                                                                 ║
║  If all Process Compliance boxes checked AND                   ║
║  all Quality Checks passed AND                                 ║
║  no Red Flags:                                                 ║
║  → Proceed to Interface Verification Protocol                  ║
║  → Then review Exit Criteria before leaving this guide         ║
║                                                                 ║
╚═════════════════════════════════════════════════════════════════╝
```

---

## Interface Verification Protocol (MANDATORY before implementation)

Before declaring TODO complete, verify all external dependencies:

**Step 1: List All External Dependencies**
For each class the new code will use, document:
- Class name
- Methods to be called
- Expected parameters (including types)
- Return values

**Step 2: Verify Interfaces Against Source**
For each dependency:
1. Read the actual class definition (not just mocks or docstrings)
2. Verify method signatures match your expectations
3. Check required vs optional parameters
4. Look for existing usage patterns: `grep -r "ClassName(" .`

**Step 3: Verify Data Model Attributes**
For each data model (dataclass, domain object) you'll access:
1. Read the actual class definition
2. List all attributes you plan to use
3. Verify each attribute exists in the definition
4. Check attribute semantics (e.g., does `fantasy_points` mean projected or actual?)

**Why this matters:** Interface mismatches cause bugs DURING implementation. Catch them beforehand.

### CRITICAL: Copy-Paste Requirement for Method Signatures

**DO NOT** verify interfaces from memory or documentation. **ALWAYS:**

**1. Open Actual Source File**
   - Navigate to the module containing the interface
   - Find the exact class/function definition
   - Scroll to the method you're calling

**2. Copy Exact Signature**
   ```python
   # EXAMPLE: Verifying DataFileManager.save_json_data()
   # From utils/data_file_manager.py line 365:
   def save_json_data(self, data: Any, prefix: str,
                      create_latest: bool = True, **json_kwargs) -> Tuple[Path, Optional[Path]]:
   ```

**3. Compare to Your Usage**
   ```python
   # YOUR CODE:
   file_path, _ = manager.save_json_data(output_data, prefix, create_latest=False)
   #                                      ^^^^^^^^^  ^^^^^^
   #                                      1st param  2nd param

   # SIGNATURE:
   def save_json_data(self, data: Any, prefix: str, ...)
   #                        ^^^^^^^^^  ^^^^^^^^^^^
   #                        1st param  2nd param

   # ✅ MATCH: output_data is data, prefix is prefix
   ```

**4. Check Return Type**
   - Signature returns: `Tuple[Path, Optional[Path]]`
   - Your code expects: tuple unpacking with 2 elements
   - ✅ Compatible

**Red Flags (DO NOT PROCEED if any are true):**
- [ ] Parameter order doesn't match signature
- [ ] Parameter types incompatible
- [ ] Return type incompatible
- [ ] Required parameters missing
- [ ] Method doesn't exist in source

**Why This Matters:**
In the player-data-fetcher-new-data-format feature, Bug #1 was caused by assuming parameter order without verification. The code called `save_json_data(prefix, data)` but the actual signature is `save_json_data(data, prefix)`. This made the entire feature non-functional despite 100% unit test pass rate (unit tests mocked the dependency, so incorrect call succeeded in tests but failed in production).

**Interface Verification Checklist:**
```
□ All external dependencies listed
□ Each dependency's methods verified against source code
□ EACH method signature COPY-PASTED from source (not assumed from memory)
□ Parameter order verified by side-by-side comparison
□ Parameter names and types confirmed
□ Return values documented and compatible with usage
□ Data model attributes verified to exist
□ Attribute semantics understood (not assumed)
```

---

## Complete Iteration Reference

Use this table to know exactly what to do at each iteration:

| # | Name | Type | Protocol | Focus |
|---|------|------|----------|-------|
| 1 | Files & Patterns | Standard | - | What files need modification? What patterns exist? |
| 2 | Error Handling | Standard | - | What error handling needed? What logging? |
| 3 | Integration Points | Standard | - | What integration points? What test mocking? |
| 4 | Algorithm Mapping | Special | Algorithm Traceability | Map spec algorithms → code locations |
| 4a | TODO Spec Audit | Special | TODO Specification Audit | Verify TODO items self-contained |
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
| 23a | Pre-Impl Spec Audit | Special | Pre-Implementation Audit | 4-part fresh-eyes spec coverage audit |
| 24 | Readiness Check | Special | Implementation Readiness | Final checklist before coding |

---

## Protocol Quick Reference

| Protocol | Iterations | Purpose | Details |
|----------|------------|---------|---------|
| **Standard Verification** | 1-3, 8-10, 15-16 | Read → Question → Research → Update | See `protocols/README.md` |
| **Algorithm Traceability** | 4, 11, 19 | Ensure spec logic matches code exactly | `protocols/README.md` |
| **TODO Specification Audit** | 4a | Ensure TODO items are self-contained | See Iteration 4a section above |
| **End-to-End Data Flow** | 5, 12 | Trace entry point → output; no orphan code | `protocols/README.md` |
| **Skeptical Re-verification** | 6, 13, 22 | Assume nothing; re-verify all claims | `protocols/README.md` |
| **Integration Gap Check** | 7, 14, 23 | Every new method has a caller | `protocols/README.md` |
| **Fresh Eyes Review** | 17, 18 | Re-read spec with fresh perspective | `protocols/README.md` |
| **Edge Case Verification** | 20 | Every edge case has task + test | `protocols/README.md` |
| **Test Coverage Planning** | 21 | Plan behavior tests; verify mocks match reality | `protocols/README.md` |
| **Pre-Implementation Audit** | 23a | 4-part spec-to-TODO audit | See Iteration 23a section above |
| **Implementation Readiness** | 24 | Final checklist before coding | `protocols/README.md` |

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
- Pre-Implementation Audit (23a): All 4 parts documented with pass/fail

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

### When to Start Handoff

**Start the handoff process when ANY of these triggers occur:**

1. **Context indicators:**
   - You've been working for 15+ iterations without a natural break
   - User mentions "running out of time" or "session ending"
   - You notice you're losing track of earlier decisions
   - The conversation feels "heavy" (lots of back-and-forth)

2. **Proactive triggers:**
   - Before starting a complex verification round
   - After completing a major milestone (all iterations done)
   - Before user questions that might require multiple iterations

**Don't wait until context runs out - start early!**

### Session Handoff Checklist (MANDATORY)

When context is running low or session is ending, complete this checklist:

```
┌─────────────────────────────────────────────────────────────────┐
│  SESSION HANDOFF CHECKLIST                                       │
│  Complete ALL items before session ends                          │
└─────────────────────────────────────────────────────────────────┘

□ TODO file updated with current iteration number
□ Progress Notes section updated with:
  - Current status (what's done)
  - Next steps (what remains)
  - Any blockers or decisions needed
□ README Agent Status section updated with:
  - Current Phase
  - Current Step
  - Next Action
□ Integration Matrix updated with any new entries discovered
□ Summary message sent to user:
  "Session ending. State preserved:
   - Current: {iteration/phase}
   - Next: {what to do next}
   - TODO file updated at: {timestamp}
   A future agent can resume by reading the README Agent Status."
```

**Why This Matters:** Without proper handoff, the next agent may restart from the beginning or miss context.

---

## Communication Guidelines

How often to update the user during verification:

| Phase | Communication Level | What to Report |
|-------|---------------------|----------------|
| **Verification Rounds** | Per round (not per iteration) | "Completed round 1 (7 iterations). Found X issues, updated TODO." |
| **Step 3 Questions** | Always communicate | Present questions file, wait for answers |
| **Blockers** | Immediately | Any issue that prevents progress |

**Do NOT:**
- Report every single iteration (too verbose)
- Stay silent for entire rounds (user loses visibility)
- Wait until end to reveal problems (fix issues early)

**DO:**
- Summarize at natural checkpoints (end of rounds)
- Report blockers immediately
- Confirm completion of major milestones

### User Communication Protocol

**MANDATORY communication points:**

| Trigger | Action | Template |
|---------|--------|----------|
| After each verification round (7, 16, 24) | Present Round Summary | See prompts_reference.md |
| When blocked on a decision | Ask for clarification | "I need your input on {X} before proceeding..." |
| When scope seems to be changing | Ask for approval | "I found {X} could be added. Should I include it?" |
| When interface verification finds issues | Report discrepancies | "Interface mismatch found: expected {X}, actual {Y}" |

**Communication Checklist (run at each checkpoint):**
```
□ Did I complete a verification round? → Present Round Summary
□ Am I blocked? → Report blocker immediately
□ Did I add tasks not in original spec? → Ask about scope
□ Is context running low? → Start Session Handoff
```

---

## Quick Commands Reference

Common commands you'll need during verification:

```bash
# Run all tests (to verify baseline)
python tests/run_all_tests.py

# Search for method callers
grep -r "method_name(" .

# Search for class usage
grep -r "ClassName" . --include="*.py"

# Find existing usage patterns
grep -r "ModuleName\." .
```

**File Operations (use tools, not bash):**
- Read files: Use the `Read` tool
- Search files by name: Use the `Glob` tool
- Search file contents: Use the `Grep` tool
- Edit files: Use the `Edit` tool

---

```
╔═════════════════════════════════════════════════════════════════╗
║  🛑 🛑 🛑 CRITICAL STOP - BEFORE PROCEEDING TO CODE 🛑 🛑 🛑    ║
╠═════════════════════════════════════════════════════════════════╣
║                                                                 ║
║  You are about to transition from VERIFICATION to CODING.      ║
║  This is a ONE-WAY GATE. Do NOT proceed unless 100% ready.     ║
║                                                                 ║
║  MANDATORY VERIFICATION QUESTIONS (All must be YES):           ║
║                                                                 ║
║  □ Have I completed ALL 24 iterations?                         ║
║  □ Did iteration 4a (TODO Spec Audit) PASS?                    ║
║  □ Did iteration 23a (Pre-Implementation Audit) PASS all 4?    ║
║  □ Did iteration 24 (Implementation Readiness) show HIGH?      ║
║  □ Are ALL interfaces verified against ACTUAL code?            ║
║  □ Is the Integration Matrix 100% complete?                    ║
║  □ Have I received answers to ALL questions?                   ║
║  □ Is there ZERO "TODO:", "TBD", or "uncertain" in TODO?       ║
║                                                                 ║
║  SELF-VERIFICATION QUESTION:                                   ║
║  "If I start coding right now, do I know EXACTLY what to       ║
║   build, how to build it, and where it fits in the codebase?"  ║
║                                                                 ║
║  CONSEQUENCES OF PROCEEDING WHEN NOT READY:                    ║
║  ❌ You will write code that doesn't match specs               ║
║  ❌ You will need to redo implementation multiple times        ║
║  ❌ QC will fail and you'll return to verification             ║
║  ❌ You will waste days building the wrong thing               ║
║  ❌ User will lose confidence in the development process       ║
║                                                                 ║
║  RULE: If you answer "NO" or "UNCERTAIN" to ANY question       ║
║  above, you MUST NOT proceed to coding. Return to the          ║
║  appropriate iteration and resolve the issue.                  ║
║                                                                 ║
╚═════════════════════════════════════════════════════════════════╝
```

---

## Exit Criteria - Ready to Leave This Guide

```
┌─────────────────────────────────────────────────────────────────┐
│  EXIT CRITERIA: Complete ALL items before proceeding           │
└─────────────────────────────────────────────────────────────────┘
```

**You may ONLY proceed to `implementation_execution_guide.md` when ALL of the following are true:**

✅ **Iteration Completion:**
- [ ] All 24 iterations marked `[x]` in Iteration Progress Tracker
- [ ] Iteration 4a (TODO Specification Audit) shows: **PASSED**
- [ ] Iteration 23a (Pre-Implementation Spec Audit) shows: **ALL 4 PARTS PASSED**
- [ ] Iteration 24 (Implementation Readiness) shows: **PASSED**

✅ **Documentation Complete:**
- [ ] Interface Verification section shows: **COMPLETE**
- [ ] Integration Matrix shows: **COMPLETE** (all new methods have callers)
- [ ] Algorithm Traceability Matrix shows: **COMPLETE**
- [ ] Round Checkpoint Summary created after iterations 7, 16, and 24

✅ **Questions Resolved:**
- [ ] Questions file created and user answered, **OR**
- [ ] Documented in TODO: "No questions needed - spec complete"

✅ **No Unresolved Items:**
- [ ] Zero "Alternative:" notes remain in TODO
- [ ] Zero "May need to..." notes remain in TODO
- [ ] Zero TODO items have "[PENDING]" or "[UNRESOLVED]" markers

✅ **Readiness Confirmed:**
- [ ] TODO file contains exact phrase: **"READY TO IMPLEMENT"**
- [ ] README.md Agent Status updated to: **"Ready for Implementation"**
- [ ] README.md shows next action: "Proceed to implementation_execution_guide.md"

**Self-Verification Question (answer honestly):**

> "If a different agent read ONLY the TODO file (without seeing specs), could they implement this feature correctly?"

- **YES** → You may proceed ✅
- **NO** → Return to Iteration 4a and 23a, add missing details ❌
- **UNSURE** → You're not ready, add more acceptance criteria ❌

**If ANY checkbox above is unchecked:**
- ❌ DO NOT proceed to implementation
- Complete the missing item(s)
- Re-verify this entire checklist
- Only proceed when 100% complete

**When ALL checkboxes are checked and verification passes:**
- ✅ Update README Agent Status: "Proceeding to Implementation Phase"
- ✅ Close this guide
- ✅ Open `implementation_execution_guide.md`
- ✅ Begin with "Verify TODO Creation Complete" section

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
| **Implementation Guide** | After this guide - to execute the TODO | `implementation_execution_guide.md` |
| **Post-Implementation Guide** | After implementation - QC and validation | `post_implementation_guide.md` |
| **Protocols Reference** | Detailed protocol definitions | `protocols/README.md` |
| **Templates** | File templates for features | `templates.md` |
| **Prompts Reference** | Conversation prompts for user discussions | `prompts_reference.md` |
| **Guides README** | Overview of all guides | `README.md` |

### Transition Points

**From Planning Guide → This guide:**
- Planning complete: all checklist items `[x]`
- User says "Prepare for updates based on {feature_name}"

**This guide → Implementation Guide:**
- All 24 iterations complete
- Iteration 24 (Implementation Readiness) passed
- Interface verification complete
- User approves proceeding to implementation

**Back to Planning Guide:**
- If major scope changes discovered
- If new requirements need user decisions

---

*This guide assumes planning is complete. If starting a new feature, use `feature_planning_guide.md` first.*
