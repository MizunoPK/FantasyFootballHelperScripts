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
│  WHY THESE STEPS ARE MANDATORY                                  │
│                                                                 │
│  Bugs in "simple" features have historically caused the most    │
│  rework. The iterations may feel excessive for small changes,   │
│  but they consistently catch issues that would otherwise ship.  │
│                                                                 │
│  The process feels slow, but the result is clean code that      │
│  doesn't need multiple rounds of post-merge fixes.              │
└─────────────────────────────────────────────────────────────────┘
```

**CRITICAL:** Update the README.md "Agent Status" section after completing each major step. This ensures continuity if the session is interrupted.

**Need to resume?** → See "Resuming Work Mid-Development" section below.

---

## CRITICAL RULES - READ EVERY SESSION

```
┌─────────────────────────────────────────────────────────────────┐
│  RULES YOU MUST FOLLOW (Quick Reference)                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. ALL 24 iterations are MANDATORY - no skipping               │
│  2. ALL 3 QC rounds are MANDATORY - no skipping                 │
│  3. Run tests after EVERY phase (100% pass required)            │
│  4. Update README "Agent Status" after EVERY step               │
│  5. Every new method MUST have a caller (no orphan code)        │
│  6. Verify interfaces BEFORE implementation (read actual code)  │
│  7. When confidence is LOW - STOP and resolve first             │
│  8. Execute actual scripts during QC (not just unit tests)      │
│  9. OUTPUT/INPUT ROUNDTRIP: Test output can be loaded as input  │
│                                                                 │
│  COMMON MISTAKES TO AVOID:                                      │
│  ✗ "This is simple, I'll skip iterations" → Bugs ship           │
│  ✗ "Tests pass so I'm done" → Script may not work E2E           │
│  ✗ "I created the method" → But is anything calling it?         │
│  ✗ "Interface probably works" → Read the actual class           │
│  ✗ "Output file exists" → But can consumers actually load it?   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

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
| Assuming interface matches similar class | Methods like `log_interval=10` may not exist on similar classes | **Verify interfaces against source** - read actual class definitions |
| Using getattr with silent defaults | `getattr(obj, 'attr', None)` hides missing attributes | **Use explicit attribute access** for required attributes |
| QA only at end | Bugs compound when built on broken foundation | **Incremental QA checkpoints** throughout implementation |
| Leaving "Alternative:" notes unresolved | Deferred decisions cause rework during implementation | **Resolve all alternatives** during planning phase |
| Skipping E2E script execution | Unit tests pass but script fails immediately | **Execute scripts E2E** during QC with real data |
| "Mirror X" without reading X | Spec says "mirror run_simulation.py" but only method signatures copied, not file organization | **Existing Pattern Audit** - read entire file and document ALL patterns |
| Output structure not validated against consumer | Files exist but can't be loaded by consumers | **OUTPUT/INPUT ROUNDTRIP** - write test that saves output then loads it back |

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

**Testing Assumptions (causes: tests pass but code broken):**
- [ ] "My mock accepts any arguments" → WARNING: Use spec=RealClass
- [ ] "I haven't run the actual script" → STOP: Run E2E test
- [ ] "My test only checks structure, not behavior" → WARNING: Add behavior test

**Output Assumptions (causes: output exists but unusable):**
- [ ] "I create output files but haven't checked what consumes them" → STOP: Identify consumers
- [ ] "Output file exists so the feature works" → STOP: Verify consumer can load it
- [ ] "Spec says 'same format as X' but I didn't read X's actual structure" → STOP: Read X

**"Same As X" Reference Assumptions (causes: incomplete implementation):**
- [ ] "Spec says 'same as X' and I know what that means" → STOP: Read actual X, list all files
- [ ] "I'm creating 5 files because spec says 5" → STOP: Verify by reading actual reference
- [ ] "Same structure means same file count" → STOP: It also means same internal structure and all required files

**If ANY checkbox above is checked, STOP and fix before proceeding.**

**When to Run This Checklist:**
- Before marking ANY iteration complete (1-24)
- Before each QA checkpoint during implementation
- Before each QC round (1-3)
- Before committing any code

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

### Anti-Pattern 5: Assumed Interface Matches

**Problem:** Developer assumes a class has the same interface as a similar class, without verifying.

**Example:** `AccuracySimulationManager` called `MultiLevelProgressTracker(total, configs, log_interval=10)`, but `MultiLevelProgressTracker.__init__()` doesn't accept a `log_interval` parameter (unlike `ProgressTracker`).

**Prevention:**
- Read the actual class definition before using it
- Use `spec=RealClass` in mocks: `@patch('...', spec=RealClass)` - this raises errors if you call methods that don't exist
- Reference existing usage in codebase: `grep -r "ClassName(" .` to see how others use it

### Anti-Pattern 6: "Mirror X" Without Reading X

**Problem:** Spec says "mirror run_simulation.py structure" but developer only copies obvious elements (CLI args, method names) while missing organizational patterns (constants at top, import order, file structure).

**Example:**
- Spec said: "Mirror run_simulation.py pattern"
- Developer copied: CLI arguments, mode handling, logging setup
- Developer missed: `DEFAULT_MODE`, `DEFAULT_SIMS`, `DEFAULT_WORKERS` constants at top; `PARAMETER_ORDER` defined in runner script not manager class

**Prevention:**
1. When spec says "mirror X", READ THE ENTIRE FILE X
2. Document ALL structural patterns found:
   - Constants defined at top (names, organization)
   - Import ordering and style
   - File-level docstring format
   - Function/class organization
   - Parameter passing patterns (where are things defined vs passed)
3. Create a structural comparison checklist before implementing
4. During Skeptical Re-verification: DIFF your implementation against the original

**Existing Pattern Audit Checklist (use when spec says "mirror X"):**
```
□ Read entire file X from start to finish
□ Document all constants at top of file
□ Document where key variables are defined (runner vs manager)
□ Document import organization pattern
□ Document file-level structure (docstring, constants, functions, main)
□ Create side-by-side comparison during implementation
□ Verify ALL patterns match, not just method signatures
```

### Anti-Pattern 6a: "Same Structure As X" Without Reading X's Actual Contents

**Problem:** Spec says "same structure as X" or "same format as existing" but developer interprets this abstractly instead of reading the actual file X to see exactly what it contains.

**Example (from accuracy simulation):**
- Spec said: "Same 5-JSON structure (draft_config.json + 4 week-range files)"
- Developer interpreted: "Create 5 JSON files with prediction parameters"
- What spec ACTUALLY meant: "Output folder should be usable as baseline folder"
- What baseline folders ACTUALLY contain: 6 files (league_config.json + 5 others), each with nested `{config_name, description, parameters}` structure

The developer never read an actual baseline folder to see what it contained.

**Why this happens:**
- "Same structure" seems self-explanatory, so developer doesn't verify
- Focus on the explicit count (5 files) rather than the implicit purpose (usable as baseline)
- No step in the workflow forced reading the actual reference

**Prevention - "Same As X" Verification Rule:**
```
┌─────────────────────────────────────────────────────────────────┐
│  WHEN SPEC SAYS "SAME AS X" OR "SAME STRUCTURE AS X":          │
│                                                                 │
│  1. STOP - Do not interpret abstractly                         │
│  2. READ the actual file/folder X                              │
│  3. LIST every file it contains                                │
│  4. READ each file's internal structure                        │
│  5. CREATE TODO task for each file with exact structure        │
│  6. If X is output that becomes input elsewhere:               │
│     - Identify all consumers of X                              │
│     - Verify consumer requirements match your TODO             │
└─────────────────────────────────────────────────────────────────┘
```

**Verification Checklist:**
```
□ I have READ the actual reference file/folder X (not just the spec description)
□ I can LIST every file/subfolder in X
□ I can DESCRIBE the internal structure of each file in X
□ My TODO includes a task to create EACH file with its EXACT structure
□ If X serves as input elsewhere, I've identified and verified consumer requirements
```

**Example of what should have happened:**
```markdown
Spec says: "Same 5-JSON structure as win-rate output"

Verification:
1. Read actual win-rate output folder: simulation/simulation_configs/optimal_iterative_*/
2. List files found:
   - league_config.json ← MISSED THIS
   - week1-5.json
   - week6-9.json
   - week10-13.json
   - week14-17.json
3. Read internal structure of week1-5.json:
   {
     "config_name": "...",
     "description": "...",
     "parameters": {...}
   }
4. TODO should include:
   - Task: Copy league_config.json from baseline
   - Task: Create week files with nested {config_name, description, parameters} structure
```

### Anti-Pattern 7: Silent Attribute Failures

**Problem:** Using `getattr(obj, 'attr', None)` for required attributes silently returns `None` instead of failing fast, causing downstream issues.

**Example:** Code used `getattr(player, 'actual_points', None)` but `FantasyPlayer` has `week_N_points` attributes instead. All players were silently skipped as "invalid" with no error.

**Prevention:**
- Use explicit attribute access for required attributes (fails fast)
- If using `getattr` with default, log a warning when default is used
- Verify attribute names exist in the dataclass/model definition before writing code

### Anti-Pattern 8: Parameter Optimization Without Flag Activation

**Problem:** Optimizing configuration parameters that have no effect because their corresponding feature flags are disabled in method calls.

**Example:** The accuracy simulation optimized 17 parameters including TEMPERATURE_WEIGHT, WIND_WEIGHT, MATCHUP_WEIGHT, etc. But the `score_player()` call used all defaults:
```python
scored = player_mgr.score_player(player)  # All defaults!
```

The defaults had `temperature=False`, `wind=False`, `matchup=False`, so 11 of 17 parameters had **no effect** - they were optimized but never used in the actual calculation!

**Why this happens:**
- Spec says "optimize these parameters" without specifying how they're activated
- Developer assumes parameters are always applied, not realizing they require flags
- No verification that method call signature enables the features being tested

**Prevention Checklist:**
```
□ For each parameter being optimized:
  □ Identify the method that uses this parameter
  □ Check if that method has an enable flag for this parameter
  □ Verify the enable flag is set to True in all call sites
  □ Compare call signature to similar features (e.g., StarterHelper for weekly scoring)
□ Create test that verifies parameter changes affect output
  □ If changing parameter X doesn't change the result, the flag is likely disabled
```

**Verification during implementation:**
When implementing parameter optimization, add a sanity check test:
```python
def test_parameter_actually_affects_output(self):
    """Verify that optimized parameters actually change results."""
    # Run with default parameter value
    result_default = calculate_with_config(DEFAULT_VALUE)

    # Run with different parameter value
    result_changed = calculate_with_config(DIFFERENT_VALUE)

    # If results are identical, the parameter isn't being used!
    assert result_default != result_changed, \
        f"Parameter change had no effect - check if feature flag is enabled"
```

### Anti-Pattern 9: Output Structure Without Consumer Validation

**Problem:** Output files/folders are created but their structure doesn't match what consumers (input loaders, other scripts) expect. Files exist and tests pass, but the output is unusable.

**Example:** Accuracy simulation created `accuracy_optimal_*/` folders with:
- `draft_config.json` (raw parameters, wrong structure)
- Missing `league_config.json` entirely

But the spec said these folders should be usable as **baseline folders** for future runs. The baseline loader expected:
- `league_config.json` (must exist)
- `draft_config.json`, `week1-5.json`, etc. (with `config_name`, `description`, `parameters` nested structure)

The output files existed and contained valid JSON, but they couldn't be used as baseline input because:
1. Missing required file (`league_config.json`)
2. Wrong internal structure (flat vs nested)

**Why this happens:**
- Output code written in isolation without checking how it will be consumed
- Tests verify "file exists" but not "file is usable as input"
- Spec says "output same structure as X" but developer doesn't verify against actual X

**Prevention - OUTPUT/INPUT ROUNDTRIP RULE:**
```
┌─────────────────────────────────────────────────────────────────┐
│  MANDATORY FOR ANY FEATURE THAT PRODUCES OUTPUT FILES:          │
│                                                                 │
│  1. Identify ALL consumers of this output                       │
│  2. Read the consumer's input validation code                   │
│  3. Write a test that feeds output back as input                │
│  4. Test must use REAL loader, not mocked                       │
└─────────────────────────────────────────────────────────────────┘
```

**Verification Checklist:**
```
□ List all consumers of this output:
  □ Consumer 1: _____ (e.g., "find_baseline_config() in run_accuracy_simulation.py")
  □ Consumer 2: _____ (e.g., "ConfigGenerator.__init__() loads baseline folder")
□ For each consumer, verify:
  □ What files does it expect? (Read the actual code)
  □ What structure within those files? (Read the actual loading code)
  □ What validation does it perform? (Read error handling)
□ Write roundtrip test:
  □ Save output using new code
  □ Load output using real consumer code (not mocked)
  □ Verify loaded data matches what was saved
```

**Example roundtrip test:**
```python
def test_output_folder_usable_as_baseline(self, manager, tmp_path):
    """Verify output folder can be used as baseline for next run."""
    # Save optimal configs
    optimal_path = manager.save_optimal_configs()

    # Try to use as baseline (this is what find_baseline_config returns)
    required_files = ['league_config.json', 'week1-5.json', 'week6-9.json',
                      'week10-13.json', 'week14-17.json']
    for f in required_files:
        assert (optimal_path / f).exists(), f"Missing required file: {f}"

    # Verify ConfigGenerator can load it (real loader, not mocked)
    config_gen = ConfigGenerator(optimal_path, parameter_order=PARAM_ORDER)
    assert config_gen.baseline_config is not None
    assert 'parameters' in config_gen.baseline_config
```

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

**ALL 24 verification iterations and ALL 3 QC rounds are MANDATORY.** There are no exceptions, regardless of:

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

**Reading the table:** If you skip the "Skeptical" iterations (6, 13, 22), you will miss "Assumption failures, interface mismatches" bugs. The example "Method doesn't actually exist" is a real bug that occurred when this iteration type was skipped.

---

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

### What Success Looks Like

The process may feel slow, but the results speak for themselves.

**Success Example: Accuracy Simulation Feature**
```
Planning Phase:
- 2 sessions, 35+ checklist items identified
- 3 API questions resolved with user
- Dependency map revealed integration complexity early

Development Phase:
- 24 iterations completed across 3 rounds
- Iteration 7 (Integration Gap Check) found 2 orphan methods
- Iteration 21 (Test Coverage) identified mock interface mismatch
- 0 questions needed after first round - spec was thorough

Implementation:
- 4 phases with QA checkpoints
- All checkpoints passed first try
- E2E test ran successfully on first attempt

QC Rounds:
- Round 1: Found 1 docstring inconsistency
- Round 2: Found 1 semantic diff issue (whitespace change)
- Round 3: Clean pass

Result: Feature merged with zero post-merge bugs.
```

**Contrast: What Rushing Looks Like**
```
"Simple" config parameter move - skipped iterations:
- Implemented quickly, tests passed
- Post-merge: User reported feature not working
- Root cause: Orphan method - never called from entry point
- Fix required: 2 additional sessions to debug and fix
- Total time: 3x longer than following the process would have taken
```

**The Math:**
- Full process: ~4-6 hours for medium feature
- Rushed process + debugging: ~8-12 hours
- Full process catches bugs at $X cost
- Rushed process catches bugs at $10X cost (debugging is expensive)

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

## Quick Commands Reference

Common commands you'll need during development:

```bash
# Run all tests (REQUIRED before any commit)
python tests/run_all_tests.py

# Check git status
git status

# View unstaged changes
git diff

# View staged changes
git diff --staged

# Search for method callers
grep -r "method_name(" .

# Search for class usage
grep -r "ClassName" . --include="*.py"

# View recent commits (for rollback targets)
git log --oneline -10

# Revert all uncommitted changes
git checkout -- .

# Run a specific test file
python -m pytest tests/path/to/test_file.py -v

# Run feature script with help
python run_feature.py --help

# Run feature script E2E (minimal mode)
python run_feature.py --mode test --iterations 1
```

**File Operations (use tools, not bash):**
- Read files: Use the `Read` tool
- Search files by name: Use the `Glob` tool
- Search file contents: Use the `Grep` tool
- Edit files: Use the `Edit` tool

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

### User Communication Protocol

**MANDATORY communication points:**

| Trigger | Action | Template |
|---------|--------|----------|
| After each verification round (7, 16, 24) | Present Round Summary | See prompts_reference.md |
| When blocked on a decision | Ask for clarification | "I need your input on {X} before proceeding..." |
| When scope seems to be changing | Ask for approval | "I found {X} could be added. Should I include it?" |
| When E2E tests fail | Report with analysis | "E2E test failed: {error}. Root cause: {analysis}. Fix: {plan}" |
| Before implementing anything new | Confirm approach | "I'm about to implement {X} using {approach}. Proceeding..." |
| When interface verification finds issues | Report discrepancies | "Interface mismatch found: expected {X}, actual {Y}" |

**Communication Checklist (run at each checkpoint):**
```
□ Did I complete a verification round? → Present Round Summary
□ Am I blocked? → Report blocker immediately
□ Did I add tasks not in original spec? → Ask about scope
□ Did tests fail? → Report with root cause
□ Is context running low? → Start Session Handoff
```

**Anti-patterns to avoid:**
- "I'll just implement this and tell them later" → Always communicate BEFORE major decisions
- "This is obvious, no need to mention" → When in doubt, communicate
- "I'll batch up all my questions" → Ask blockers immediately, batch only non-blocking questions

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
   - Before starting a complex implementation phase
   - After completing a major milestone (all iterations done)
   - Before E2E testing that might reveal multiple issues

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
□ Any uncommitted code changes committed
□ Integration Matrix updated with any new entries discovered
□ Summary message sent to user:
  "Session ending. State preserved:
   - Current: {iteration/phase}
   - Next: {what to do next}
   - TODO file updated at: {timestamp}
   A future agent can resume by reading the README Agent Status."
```

**Why This Matters:** Without proper handoff, the next agent may:
- Restart from the beginning (wasting previous work)
- Miss context about decisions made
- Make contradictory choices

### What to Preserve

| Always Update | Before Session Ends |
|---------------|---------------------|
| Iteration Progress Tracker | Mark current iteration |
| Protocol Execution Tracker | Mark completed protocols |
| Integration Matrix | Add any new entries |
| Progress Notes | Current status + next steps |
| README Agent Status | Phase, Step, Next Action |

### Context Window Emergency Protocol

If context runs out DURING implementation (mid-task):

1. **STOP** the current task immediately
2. **Commit** any working code (even partial) with message: "WIP: {task description} - session handoff"
3. **Update TODO** to mark task as "IN PROGRESS - partial completion"
4. **Document** in Progress Notes exactly where you stopped:
   ```
   EMERGENCY HANDOFF:
   - Task: 2.3 - Implement AccuracyCalculator
   - Progress: Method signatures done, MAE calculation partial
   - Next: Complete _calculate_error() method starting line 145
   - File state: Compiles but tests will fail until complete
   ```
5. **Inform user** of the partial state

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
│         21: Test Coverage Planning + Mock Audit                 │
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
| **Test Coverage Planning + Mock Audit** | 21 | Plan behavior tests; verify mocks match reality | `protocols_reference.md` |
| **Implementation Readiness** | 24 | Final checklist before coding | `protocols_reference.md` |
| **Verification Failure** | When needed | Force re-verification after implementation issues | `protocols_reference.md` |
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

**Integration Gap Check - Additional Requirements:**

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

**Why this matters:** Deferring architectural decisions to implementation causes rework. Decisions like "how should Add to Roster Mode get its config" affect behavior, not just code structure - these must be resolved during planning.

**Output:** TODO file with 7 iterations complete, all protocols executed, ready for questions.

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

**Why This Matters:** Without checkpoint summaries:
- Agents don't reflect on what they learned
- Scope creep goes undetected
- Confidence isn't calibrated against reality

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

### Pre-Implementation: Rollback Point Planning

Before starting implementation, identify natural rollback points. This makes it safer to advance because you know how to retreat.

**Step 1: Identify Reversible Checkpoints**

List the natural stopping points where you can safely roll back:
```
| Checkpoint | Description | Rollback Command |
|------------|-------------|------------------|
| Clean state | Before any changes | git checkout -- . |
| Phase 1 complete | Core classes created | git checkout {phase1_commit} |
| Phase 2 complete | Integration wired up | git checkout {phase2_commit} |
```

**Step 2: Identify "Point of No Return" Changes**

Some changes are harder to reverse. Identify these early:
- Database schema changes
- API contract changes (if external consumers exist)
- Config file format changes that affect other tools
- File/folder structure changes that affect other scripts

**Step 3: Plan Commit Strategy**

- Commit after each phase completes successfully
- Use descriptive commit messages that explain the checkpoint
- Consider WIP commits for long phases: "WIP: Phase 2 - integration partial"

**Rollback Commands Reference:**
```bash
# Revert all uncommitted changes
git checkout -- .

# Revert to specific commit (keeps history)
git revert HEAD

# View recent commits for rollback targets
git log --oneline -10
```

**Why this matters:** Knowing how to retreat makes it safer to advance. If implementation fails, you can quickly return to a known-good state.

---

### Pre-Implementation: Interface and Data Model Verification (MANDATORY)

Before writing any implementation code, complete these verification steps:

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

**Why this matters:** Three interface mismatches in one class indicates the class was written without verifying actual interfaces. This catches bugs BEFORE implementation rather than during E2E testing.

**Interface Verification Checklist:**
```
□ All external dependencies listed
□ Each dependency's methods verified against source code
□ Parameter names and types confirmed
□ Return values documented
□ Data model attributes verified to exist
□ Attribute semantics understood (not assumed)
```

### Reference Existing Usage (MANDATORY)

Before implementing code that uses existing modules:

1. **Find existing usage examples**: `grep -r "module_name\." .`
2. **Read actual method signatures**: Check the real `def` lines, not just docstrings
3. **Verify against existing tests**: See how the class is used in its own unit tests
4. **Copy the pattern**: Don't invent new method names that might not exist

**Example:**
```bash
# Before using ConfigGenerator in new code:
grep -r "config_generator\." simulation/
# Find: SimulationManager.py shows correct usage pattern
# Use that pattern, don't assume different methods exist
```

### Standard Implementation Steps

1. **Create code changes file**: `{feature_name}_code_changes.md`
   - Use template from `templates.md`

2. **Verify dependency ordering**: Before implementing, ensure TODO tasks are correctly ordered:

   **Dependency Ordering Checklist:**
   ```
   □ Data models/classes created before code that uses them
   □ Utility functions created before callers
   □ Tests created after implementations they test
   □ Configuration changes before code that reads config
   □ No circular dependencies between tasks
   ```

   **How to verify:**
   - For each TODO task, ask: "What must exist before I can implement this?"
   - If dependency exists as a later task, reorder
   - If dependency doesn't exist in TODO, add it

3. **Execute TODO tasks phase by phase**
   - Update code_changes.md after EACH change
   - Run tests after EACH phase
   - 100% pass rate required at all times
   - **Consider Test-First for algorithms**: Write failing tests before implementing calculation logic (see `protocols_reference.md` → Test-First Implementation Principle)

4. **Update lessons_learned.md when issues found**
   - Any edge case missed during planning
   - Any verification failure
   - Any user-reported issue

### Incremental QA Checkpoints (MANDATORY)

QA must happen THROUGHOUT development, not just at the end.

**TODO File Structure with Checkpoints:**
```
Phase 1: Core Implementation
- [ ] 1.1 Implement AccuracyCalculator
- [ ] 1.2 Implement AccuracyResultsManager
- [ ] 1.3 QA CHECKPOINT: Test calculators with real player data
      Expected: MAE > 0, player_count > 0 for test data

Phase 2: Integration
- [ ] 2.1 Implement AccuracySimulationManager
- [ ] 2.2 Wire up to runner script
- [ ] 2.3 QA CHECKPOINT: Run script end-to-end
      Expected: Script completes, outputs written to disk
```

**QA Checkpoint Requirements:**
1. Run all existing unit tests
2. Run E2E test with real data (whatever is testable so far)
3. Verify output is meaningful (non-zero values, expected format)
4. Document any issues found before proceeding

**QA Checkpoint Failure Protocol:**
1. **STOP development**
2. **Fix the issue** before proceeding
3. **Re-run checkpoint** to verify fix
4. **Document** what went wrong in lessons learned
5. **Only proceed** after checkpoint passes

**Why this matters:** QA at the end can only verify that bugs still exist. QA during development catches bugs when they're introduced, before more code is built on broken foundations.

---

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

**QC Round 1: Script Execution Test - Extended Coverage (MANDATORY)**

**IMPORTANT:** Test ALL execution modes, not just --help and minimal runs.

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

**Scripts without execution tests must not pass QC.**

**When E2E tests reveal errors:**
1. Fix the immediate error
2. Before continuing, perform root cause analysis:
   - Why was this error created in the first place?
   - Why wasn't it caught during unit testing?
   - Why wasn't it caught during verification iterations?
3. Document findings in the lessons learned file
4. Only proceed after documenting the lesson

**QC Round Checklist (verify during each round):**
```
□ Tests use real objects where possible (not excessive mocking)
□ Output file tests validate CONTENT, not just existence
□ Private methods with branching logic are tested through callers
□ Parameter dependencies are tested (changing A also updates B)
□ At least one integration test runs the actual feature end-to-end
□ Runner scripts execute successfully with --help
□ Runner scripts execute successfully end-to-end with real data
□ Interfaces verified against actual class definitions (not assumed)
□ Data model attributes verified to exist (not assumed)
```

Document each round in code_changes.md:
```
## Quality Control Round [N]
- Reviewed: [date/time]
- Script Execution Tests: [--help passed, E2E passed with output X]
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
