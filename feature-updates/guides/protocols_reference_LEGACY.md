# Protocols Reference

This file contains detailed protocol definitions referenced by the Feature Development Guide. Use this as a reference when executing specific protocols during verification iterations.

---

## Quick Protocol Lookup

| Protocol | When to Execute | Section |
|----------|-----------------|---------|
| **Cheat Sheet** | Quick reference during development | [Link](#protocol-quick-reference-cheat-sheet) |
| **Verification Failure** | When any iteration finds issues | [Link](#verification-failure-protocol) |
| Standard Verification | Iterations 1-3, 8-10, 15-16 | [Link](#standard-verification-protocol) |
| Algorithm Traceability Matrix | Iterations 4, 11, 19 | [Link](#algorithm-traceability-matrix-protocol) |
| TODO Specification Audit | Iteration 4a (NEW) | [Link](#todo-specification-audit-protocol) |
| End-to-End Data Flow | Iterations 5, 12 | [Link](#end-to-end-data-flow-protocol) |
| Skeptical Re-verification | Iterations 6, 13, 22 | [Link](#skeptical-re-verification-protocol) |
| Integration Gap Check | Iterations 7, 14, 23 | [Link](#integration-gap-check-protocol) |
| Fresh Eyes Review | Iterations 17, 18 | [Link](#fresh-eyes-review-protocol) |
| Pre-Implementation Spec Audit | Iteration 23a (NEW) | [Link](#pre-implementation-spec-audit-protocol) |
| Edge Case Verification | Iteration 20 | [Link](#edge-case-verification-protocol) |
| Test Coverage Planning + Mock Audit | Iteration 21 | [Link](#test-coverage-planning-protocol) |
| Implementation Readiness | Iteration 24 | [Link](#implementation-readiness-protocol) |
| Interface Verification | Before implementation | [Link](#interface-verification-protocol) |
| Smoke Testing | Before declaring complete | [Link](#smoke-testing-protocol) |
| Requirement Verification | Before marking complete | [Link](#requirement-verification-protocol) |
| Quality Control Review | After implementation | [Link](#quality-control-review-protocol) |
| Lessons Learned | Ongoing + before completion | [Link](#lessons-learned-protocol) |
| Guide Update | After QA complete | [Link](#guide-update-protocol) |
| Pre-commit Validation | Before any commit | [Link](#pre-commit-validation-protocol) |

---

## Protocol Quick Reference (Cheat Sheet)

Use this table for fast lookup during development:

| Iteration | Protocol | Key Action | Output |
|-----------|----------|------------|--------|
| 1-3 | Standard | Read → Question → Research → Update | TODO updates |
| 4 | Algorithm Traceability | Map spec algorithms to code locations | Traceability Matrix |
| 4a | TODO Specification Audit | Add acceptance criteria to TODO items | TODO with criteria |
| 5 | End-to-End Data Flow | Trace entry → output | Data Flow Traces |
| 6 | Skeptical Re-verification | Challenge ALL assumptions | Verification Results |
| 7 | Integration Gap Check | Every method needs a caller | Integration Matrix |
| 8-10 | Standard | Re-verify with user answers | TODO updates |
| 11 | Algorithm Traceability | Re-verify algorithms with answers | Matrix updates |
| 12 | End-to-End Data Flow | Re-trace with answers | Trace updates |
| 13 | Skeptical Re-verification | Challenge answer interpretations | Verification Results |
| 14 | Integration Gap Check | Final caller verification | Matrix updates |
| 15-16 | Standard | Final preparation | Integration checklist |
| 17-18 | Fresh Eyes | Re-read spec as if first time | Gap identification |
| 19 | Algorithm Deep Dive | Quote exact spec text | Algorithm verification |
| 20 | Edge Case | Each edge case → task + test | Edge case matrix |
| 21 | Test Coverage + Mock Audit | Plan behavior tests, audit mocks | Test plan |
| 22 | Skeptical Re-verification | Final assumption challenge | Confidence assessment |
| 23 | Integration Gap Check | Final orphan code check | Clean matrix |
| 23a | Pre-Implementation Spec Audit | 4-part fresh-eyes audit: Coverage, Clarity, Structure, Mapping | Audit report |
| 24 | Implementation Readiness | Final go/no-go checklist (REQUIRES 23a PASS) | READY or BLOCKED |

---

## Anti-Pattern Gallery

Visual examples of what NOT to do. Learn from these common mistakes.

### Anti-Pattern 1: The Orphan Method

**What happened:**
```python
# Created this method...
class ResultsManager:
    def save_optimal_configs_folder(self):
        """Save configs to folder structure."""
        # Great implementation!
        self._create_folder_structure()
        self._write_config_files()
        return folder_path

# But forgot to update the caller...
class SimulationManager:
    def run_iterative(self):
        # ... simulation logic ...

        # Still calls the old method!
        self.results_manager.save_optimal_config()  # ← OLD METHOD

        # Should call:
        # self.results_manager.save_optimal_configs_folder()  # ← NEW METHOD
```

**Result:** Feature "complete" but doesn't work for users. Tests pass because they test the new method in isolation.

**How to catch:** Integration Gap Check (iterations 7, 14, 23) - verify every new method has a caller in the Integration Matrix.

---

### Anti-Pattern 2: The Interface Assumption

**What happened:**
```python
# Assumed the interface was:
class AccuracyCalculator:
    def calculate_score(self, player, week):
        return player.actual_points  # ← Assumed this attribute exists

# But the actual FantasyPlayer class has:
class FantasyPlayer:
    # actual_points doesn't exist!
    week_1_points: float
    week_2_points: float
    # ... week_3 through week_17 ...

    # Must use: sum([getattr(self, f'week_{i}_points', 0) for i in range(1, 18)])
```

**Result:** `AttributeError: 'FantasyPlayer' object has no attribute 'actual_points'` at runtime.

**How to catch:** Interface Verification Protocol - read actual class definitions with the Read tool before implementing. Don't trust similar class patterns.

---

### Anti-Pattern 3: The Mock Mask

**What happened:**
```python
# Test with heavy mocking...
@patch('module.ConfigGenerator')
def test_simulation(mock_gen):
    # Mock accepts ANY arguments!
    mock_gen.return_value.generate.return_value = []

    manager = SimulationManager()
    result = manager.run()

    # Test passes! But...

# Real interface is different:
class ConfigGenerator:
    def generate_iterative_combinations(self, param_name: str, base_config: dict):
        # Different method name! Different parameters!
        pass
```

**Result:** Tests pass, production crashes with `AttributeError: 'ConfigGenerator' object has no attribute 'generate'`.

**How to catch:** Mock Audit (iteration 21) - verify mocks match real interfaces. Use `spec=RealClass` in `@patch` decorators.

---

### Anti-Pattern 4: The Silent Default

**What happened:**
```python
# Code silently handles missing attributes:
def process_players(players):
    results = []
    for player in players:
        actual = getattr(player, 'actual_points', None)  # ← Silent default
        if actual is not None:
            results.append(player)
    return results

# But 'actual_points' never exists on any player!
# Result: Empty results list, no error, no warning
```

**Result:** Feature runs but produces empty/wrong output. No error messages to debug.

**How to catch:**
- Use explicit attribute access for required attributes (fails fast)
- Add logging when default values are used
- Verify attribute names exist in class definitions

---

### Anti-Pattern 5: The Existence Test

**What happened:**
```python
# Test only checks file exists:
def test_output_generation():
    manager.run_simulation()

    # BAD: Only checks existence
    assert (output_path / 'config.json').exists()
    assert (output_path / 'results.csv').exists()
    # Tests pass!

# But the files contain:
# config.json: {}  ← Empty!
# results.csv: "header\n"  ← No data!
```

**Result:** Tests pass but output is useless.

**How to catch:** Write content validation tests:
```python
# GOOD: Validates content
config = json.load(open(output_path / 'config.json'))
assert 'DRAFT_ORDER' in config
assert len(config['DRAFT_ORDER']) == 12

results = pd.read_csv(output_path / 'results.csv')
assert len(results) > 0
assert results['score'].mean() > 0
```

---

### Anti-Pattern 6: The Partial Mirror

**What happened:**
```python
# Spec said: "Mirror run_simulation.py structure"

# Developer created run_accuracy_simulation.py with:
# ✓ Same CLI arguments (--mode, --baseline, --output, etc.)
# ✓ Same mode handling (ros, weekly, both)
# ✓ Same logging setup
# ✓ Same error handling

# But MISSED these patterns from run_simulation.py:

# 1. Constants at top of file:
DEFAULT_MODE = 'both'
DEFAULT_SIMS = 100
DEFAULT_WORKERS = 4
PARAMETER_ORDER = [...]  # ← Defined here, not in manager class!

# 2. Where PARAMETER_ORDER is defined:
# In run_simulation.py: PARAMETER_ORDER at line 56
# In AccuracySimulationManager.py: ACCURACY_PARAMETER_ORDER at line 62  # ← WRONG LOCATION
```

**Result:** Inconsistent code organization. Required post-implementation refactoring to move constants to runner script.

**How to catch:** Mirror Pattern Verification (added to Skeptical Re-verification Protocol):
1. When spec says "mirror X", read ENTIRE file X
2. Document ALL organizational patterns (constants, where vars defined, file structure)
3. Compare your implementation against these patterns
4. Don't just copy obvious elements (CLI args) - copy everything

---

### Anti-Pattern Recognition Checklist

Before marking any implementation complete, verify NONE of these patterns are present:

```
□ Every new method has a caller (not orphan)
□ Every interface call verified against actual class definition
□ Mocks use spec=RealClass or are verified against real interface
□ No getattr with silent defaults on required attributes
□ Output tests validate content, not just existence
□ If spec said "mirror X", ALL patterns from X are matched (not just obvious ones)
```

---

## Common Failure Patterns by Phase

Use this reference to anticipate and prevent failures at each workflow stage:

### Planning Phase Failures

| Pattern | Symptoms | Prevention |
|---------|----------|------------|
| **Vague specs** | "Handle errors appropriately" with no details | Require specific error messages and behaviors |
| **Missing edge cases** | Only happy path documented | Ask "what if X is empty/null/invalid?" |
| **Unresolved alternatives** | "Option A OR Option B" in specs | Force choice before development |
| **Assumed interfaces** | "Call the save method" without verification | Verify exact method signatures |
| **Scope creep** | Requirements expand during planning | Document explicit in-scope/out-of-scope |

### Verification Phase Failures

| Pattern | Symptoms | Prevention |
|---------|----------|------------|
| **Rushing iterations** | "This is simple, skip to 24" | Complete ALL iterations - complexity hides |
| **Interface assumptions** | "Similar class X has this method" | Read actual class definitions |
| **Data model assumptions** | "Object probably has this attribute" | Verify attributes exist and semantics |
| **Orphan code planning** | Tasks create methods but no callers | Integration Gap Check (7, 14, 23) |
| **Mock-first thinking** | "I'll mock this and figure it out later" | Verify real interfaces during planning |

### Implementation Phase Failures

| Pattern | Symptoms | Prevention |
|---------|----------|------------|
| **Wrong dependency order** | Import errors, undefined classes | Verify dependency ordering before coding |
| **Test-last approach** | "I'll add tests after it works" | Write tests alongside or before code |
| **QA-at-end only** | All bugs discovered in final QC | Incremental QA checkpoints |
| **Silent failures** | Code runs but produces wrong output | Output content validation tests |
| **Breaking unrelated tests** | Changes cascade unexpectedly | Run full test suite after each phase |

### QC Phase Failures

| Pattern | Symptoms | Prevention |
|---------|----------|------------|
| **Existence testing only** | "File exists" but content wrong | Content validation in tests |
| **Mock masking** | Heavy mocking hides real bugs | At least one integration test with real objects |
| **Skipping E2E execution** | Unit tests pass, script fails | Always execute scripts end-to-end |
| **Ignoring warnings** | Deprecation/type warnings dismissed | Address all warnings before completion |

**How to use this table:** Before each phase transition, review the relevant failure patterns and verify none are present.

---

## Verification Failure Protocol

**Purpose:** Handle issues discovered during any verification iteration.

**When a verification iteration finds a gap or issue:**

1. **STOP** - Do not continue to the next iteration
2. **Document** the gap in the TODO file under a "Verification Gaps" section:
   ```
   ## Verification Gaps (Iteration X)
   - [GAP-1] Missing task for {description}
   - [GAP-2] Orphan method {name} has no caller
   ```
3. **Assess severity:**
   - **Critical** (blocks implementation): Missing caller, wrong interface, algorithm mismatch
   - **Non-critical** (can be fixed during implementation): Missing test, documentation gap
4. **For Critical gaps:**
   - Add task to TODO immediately
   - Mark iteration as "INCOMPLETE - gaps found"
   - Re-run iteration after fixing
5. **For Non-critical gaps:**
   - Add task to TODO
   - Note in Progress Notes: "Non-critical gap found, task added"
   - Continue to next iteration
6. **Update confidence level** based on gaps found

**Example:**
```
Iteration 7 (Integration Gap Check):
- Found: save_optimal_config() method has no caller
- Severity: CRITICAL
- Action: Added Task 4.2 to modify SimulationManager
- Status: Re-running iteration 7 after fix
```

---

## Mandatory Stop Points

These situations REQUIRE stopping and asking the user before proceeding. Do NOT proceed past these points without user input.

```
┌─────────────────────────────────────────────────────────────────┐
│  STOP AND ASK - These situations require user input             │
└─────────────────────────────────────────────────────────────────┘
```

| Situation | Why Stop | What to Ask |
|-----------|----------|-------------|
| **Confidence is LOW** at any iteration | Low confidence = high bug risk | "I have low confidence because {X}. Should I investigate more or proceed?" |
| **Found unresolved alternative** in spec | Ambiguity causes wrong implementation | "The spec mentions both A and B. Which should I use?" |
| **Test failure** you can't quickly fix | May indicate design problem | "Tests are failing because {X}. Options: (1) fix Y, (2) change approach. Which do you prefer?" |
| **Scope seems to be expanding** | Scope creep is expensive | "This change would also require {X}. Is that in scope?" |
| **Interface doesn't match expectation** | May need spec update | "Expected method {X}, but found {Y}. Should I update the plan?" |
| **E2E script produces unexpected output** | May indicate misunderstanding | "Script runs but output is {X} instead of {Y}. Is this expected?" |
| **Missing data source** for a requirement | Can't implement without data | "Requirement {X} needs data from {Y}, but I can't find it. Where should I look?" |
| **Conflicting requirements** discovered | Both can't be satisfied | "Requirements A and B conflict because {X}. Which takes priority?" |
| **New edge case** discovered during implementation | May need spec clarification | "Found edge case: {X}. How should this be handled?" |
| **Architecture decision** with multiple valid approaches | User preference matters | "I can implement this with {A} or {B}. Here are trade-offs: ... Which do you prefer?" |

**How to Stop:**
1. Document the situation clearly in TODO or questions file
2. Present the issue to the user with context
3. Offer options when possible (don't just say "I'm stuck")
4. Wait for user response before proceeding

**Anti-pattern:** "I'll make a decision and tell them later"
- This causes rework when your guess was wrong
- Always ask BEFORE implementing when uncertain

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

4. **"Same As X" Reference Verification (MANDATORY if spec references existing files/folders)**
   When the spec says "same as X", "same structure as X", "mirror X", or "like existing Y":
   - **READ the actual file/folder X** - do not interpret abstractly
   - **LIST every file** contained in X
   - **READ internal structure** of each file in X
   - **CREATE explicit TODO tasks** for each file with exact structure
   - **VERIFY consumer requirements** if X serves as input elsewhere

   **Red flag:** If your TODO says "create same format as X" but you haven't actually read X, STOP and read it now.

5. **Update TODO file**
   - Add missing requirements discovered
   - Add specific file paths with line numbers
   - Add code references for patterns to follow
   - Mark iteration complete in tracker

5. **Scope Creep Check (EVERY iteration)**
   Before marking the iteration complete, ask yourself:
   - "Am I adding tasks that weren't in the original spec?"
   - "Am I expanding the feature beyond what was requested?"
   - "Am I adding 'nice to have' items that weren't required?"

   **If YES to any:**
   - Document the potential addition
   - Mark it as "SCOPE QUESTION" in TODO
   - Ask user before including: "I found {X} could be improved. Should I include this in scope, or defer to a future feature?"

   **Valid additions (don't need user approval):**
   - Tasks required to implement spec items (discovered dependencies)
   - Error handling for spec requirements
   - Tests for spec requirements

   **Invalid additions (need user approval):**
   - "While I'm here, I could also..."
   - "This would be better if we also..."
   - "The codebase would benefit from..."

**Output:** Updated TODO file with iteration marked complete.

---

### Skeptical Re-verification Protocol

**Purpose:** Challenge all assumptions and re-validate all claims with fresh codebase research.

> *Rationale: Assumptions are the root cause of most bugs. "I assumed this method existed" and "I assumed this attribute was available" cause runtime crashes. This protocol forces you to verify, not assume.*

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

4. **Mirror Pattern Verification** (if spec says "mirror X" or "similar to X"):
   - Read ENTIRE file X from start to finish
   - Document ALL organizational patterns:
     - Constants at top of file (what constants, what order)
     - Where key variables are defined (runner script vs manager class)
     - Import organization
     - File structure (docstring, constants, functions, main block)
   - Compare your TODO against these patterns
   - If patterns don't match, update TODO to match

   **Why this matters:** "Mirror run_simulation.py" was interpreted as "copy the CLI args and mode handling" but missed:
   - `DEFAULT_MODE`, `DEFAULT_SIMS`, `DEFAULT_WORKERS` constants at top
   - `PARAMETER_ORDER` defined in runner script, not manager class

   These omissions required post-implementation fixes.

5. **Method Call Parameter Verification** (if feature optimizes or uses configurable parameters):
   - For each parameter the feature optimizes/uses:
     - Identify the method that applies this parameter
     - Check if that method has an enable flag for the parameter
     - Verify the method call has that flag set to True
   - Compare method call signature to similar/consuming features:
     - If feature "optimizes weekly scoring", compare to StarterHelperModeManager
     - If feature "optimizes draft scoring", compare to AddToRosterModeManager
   - Add test that parameter changes actually affect output

   **Why this matters:** The accuracy simulation optimized 17 parameters but called `score_player(player)` with all default flags. Defaults had `temperature=False`, `wind=False`, `matchup=False`, so 11 of 17 parameters had **no effect** - they were optimized but never used!

   **Verification test to add:**
   ```python
   def test_parameter_changes_affect_output(self):
       result1 = calculate_with_config(param_value=10)
       result2 = calculate_with_config(param_value=100)
       assert result1 != result2, "Parameter change had no effect - check flags"
   ```

6. **Document Results:**
   - Add "Skeptical Re-Verification Results" section to TODO
   - List what was verified as correct
   - List what was found to be incorrect and corrected
   - Document confidence level in current plan

7. **Confidence Calibration:**
   Use these criteria to set your confidence level:

   | Level | Criteria |
   |-------|----------|
   | **High** | All file paths verified to exist, all method signatures confirmed, no assumptions remaining, similar patterns found in codebase |
   | **Medium** | Most paths verified, some method signatures assumed based on patterns, 1-2 minor assumptions remaining |
   | **Low** | Multiple paths unverified, method signatures based on documentation only, significant assumptions remaining |

   **Detailed Confidence Criteria:**

   | Area | High Confidence | Medium Confidence | Low Confidence |
   |------|-----------------|-------------------|----------------|
   | **File Paths** | All verified with Read/Glob | Most verified, 1-2 assumed | Multiple unverified |
   | **Method Signatures** | All confirmed from source | Most confirmed, some from docs | Based on docs/patterns only |
   | **Integration Points** | All callers identified and verified | Most callers known | Callers unclear |
   | **Data Flow** | Complete trace from entry to output | Most steps traced | Significant gaps |
   | **Similar Patterns** | Found and referenced in codebase | Found similar, not exact | No similar patterns |
   | **Edge Cases** | All identified and documented | Most identified | Several unknown |

   **Example Evidence for High Confidence:**
   ```
   Confidence: HIGH
   - File path: simulation/shared/ConfigGenerator.py (verified with Read)
   - Method: generate_iterative_combinations() at line 145 (read actual definition)
   - Caller: SimulationManager.run_iterative_optimization() at line 261 (verified with Grep)
   - Similar pattern: SimulationManager already calls generate_full_combinations() same way
   ```

   **Example Evidence for Medium Confidence:**
   ```
   Confidence: MEDIUM
   - File path: simulation/shared/ConfigGenerator.py (verified)
   - Method: generate_iterative_combinations() (signature inferred from docstring)
   - Caller: SimulationManager (likely run_iterative_optimization, need to verify)
   - Assumption: Return type matches existing generate_* methods
   ```

   **Example Evidence for Low Confidence:**
   ```
   Confidence: LOW - DO NOT PROCEED
   - File path: Assumed to be in simulation/ folder
   - Method: Described in architecture docs but not found in code
   - Caller: Unknown - need to investigate where this fits
   - Multiple assumptions about parameter types and return values
   ```

   **Confidence Level Actions:**
   - **High:** Proceed to next iteration
   - **Medium:** Note assumptions explicitly, proceed cautiously, plan to verify during implementation
   - **Low:** **STOP** - Resolve uncertainties before proceeding. Low confidence at iteration 24 = DO NOT implement.

   **If confidence is Low:** Do NOT proceed to implementation. Return to verification and resolve uncertainties first.

---

### Integration Gap Check Protocol

**Purpose:** Ensure all new code will actually be called from entry points (no orphan code).

> *Rationale: The #1 cause of "feature complete but doesn't work" is orphan code - methods that exist, have tests, but are never called from the actual entry point. This protocol catches that pattern.*

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

6. **Cross-Feature Impact Check:**
   Before marking integration complete, verify no unintended impacts on existing features:

   a. **List all files modified** (from TODO's "Files to Modify" section)

   b. **For each modified file, identify:**
      - What OTHER features use this file?
      - What callers besides your new code use modified methods?
      - Use: `grep -r "modified_method\(" .` to find all callers

   c. **For each affected feature:**
      - Do existing tests still pass? (They should if run after each phase)
      - Does behavior change for existing use cases?
      - If behavior changes intentionally, document it
      - If behavior changes unintentionally, fix it

   d. **Create impact matrix if multiple features affected:**
      ```
      | Modified File | Other Features Using It | Impact | Mitigation |
      |---------------|------------------------|--------|------------|
      | PlayerManager.py | Trade Mode, Starter Mode | None - added new method | N/A |
      | ConfigManager.py | All modes | Changed return type | Updated all callers |
      ```

   **Why this matters:** Features don't exist in isolation. Changes can have ripple effects that aren't caught by the feature's own tests.

7. **Check for Unresolved Alternatives (CRITICAL):**
   - Search TODO for "Alternative:" notes - these indicate unresolved decisions
   - Search TODO for "May need to..." phrases - these indicate uncertainty
   - For each unresolved item:
     - Document the options with pros/cons
     - Create a question in the questions file
     - DO NOT proceed past verification until user decides

   **Valid deferral reasons:**
   - "Will be created when X runs" (file generation)
   - "Low priority, not blocking" (documentation)

   **Invalid deferral reasons (must resolve NOW):**
   - "Requires user decision" → Should have been asked during planning
   - "Multiple approaches possible" → Should have been decided during planning

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

### TODO Specification Audit Protocol

**Purpose:** Ensure every TODO item has enough detail to implement WITHOUT re-reading specs. This prevents implementation drift where code is written from memory instead of specifications.

**Execute during:** Iteration 4a (immediately after Algorithm Traceability Matrix)

**Historical Context:** Added after feature implementation passed all 24 iterations but failed QC Round 1 with 40% failure rate. Root cause: TODO items were too vague, causing agent to implement from memory instead of specs.

**Steps:**

1. **For EACH TODO item in implementation phases:**
   - Read corresponding spec section(s) line-by-line
   - Extract EXACT requirements (data structures, field lists, constraints, examples)
   - Add "ACCEPTANCE CRITERIA" section to the TODO item with:
     - ✓ Each specific requirement as checkable item
     - Example of correct output from specs
     - Anti-example of common mistake
     - Spec line reference for verification

2. **Self-audit each TODO item:**
   - [ ] "Can I implement this without re-reading specs?" (YES required)
   - [ ] "Do I know what the output should look like?" (YES required)
   - [ ] "Do I know what NOT to do?" (YES required)
   - If answer is NO to any → add more detail from specs

3. **Red flags to watch for:**
   - ⛔ "Transform to [vague description]" without showing structure
   - ⛔ "Build [thing]" without listing required fields
   - ⛔ "Add [feature]" without expected output example
   - ⛔ "Handle [case]" without specifying correct behavior
   - ⛔ Missing spec references
   - ⛔ No examples of correct output

4. **Quality template for TODO items:**
   ```
   - [ ] X.X: [Task name]

     ACCEPTANCE CRITERIA (from specs.md):

     ✓ REQUIREMENT 1: [Exact specification]
       - Spec: specs.md lines X-Y
       - Example: [correct output]
       - NOT: [common mistake] ❌

     ✓ REQUIREMENT 2: [Exact specification]
       - Spec: specs.md lines A-B
       - Example: [correct output]
       - NOT: [common mistake] ❌

     VERIFICATION:
     - [ ] Passes check 1
     - [ ] Passes check 2
   ```

5. **Completion criteria:**
   - [ ] Every TODO item has Acceptance Criteria section
   - [ ] Every criteria has spec reference
   - [ ] Every criteria has example or anti-example
   - [ ] Self-audit passes for all items

**Example - GOOD TODO item:**
```
- [ ] Build JSON output

  ACCEPTANCE CRITERIA (from specs.md):

  ✓ Root structure must be {"qb_data": [...]} (spec line 24)
    Example: {"qb_data": [player1, player2]}
    NOT: {"position": "QB", "players": [...]} ❌

  ✓ Each player must have 11 fields (spec lines 44-56):
    id (number), name, team, position, injury_status,
    drafted_by, locked, average_draft_position,
    player_rating, projected_points, actual_points
    NOT: Missing any fields ❌

  ✓ Arrays must be 17 elements (spec line 58-65)
    Example: [null, null, 23.4, 18.7, ...]
    NOT: Variable length arrays ❌
```

**Example - BAD TODO item:**
```
- [ ] Build JSON output
  - Create JSON structure
  - Include all fields
  - Handle arrays correctly
```
(Too vague - will lead to implementation from memory)

**Key Insight:** The TODO must be SELF-CONTAINED with all details from specs embedded as acceptance criteria. If implementing requires re-reading specs to know what "correct" looks like, the TODO has failed its purpose.

**Output:** TODO file with all items having detailed acceptance criteria extracted from specs.

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

5. **Weekly Mode Integration Check (for features with weekly projections):**
   - If feature uses `use_weekly_projection=True`, verify:
     - [ ] `calculate_max_weekly_projection(week_num)` is called BEFORE scoring
     - [ ] Result is assigned to `scoring_calculator.max_weekly_projection`
     - [ ] This initialization happens for EVERY week evaluated (not just once)
   - Compare to working reference: `StarterHelperModeManager` lines 452-453
   - Add TODO task: "Verify weekly projection initialization matches StarterHelperMode pattern"

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

3. **"Same As X" Language Audit (CRITICAL)**
   Search spec for these phrases and verify each one:
   - "same as", "same structure as", "same format as"
   - "like existing", "mirror", "follow pattern of"
   - "similar to", "matches", "consistent with"

   For EACH match found:
   - Have you actually READ the referenced file/folder X?
   - Can you list EVERY file in X?
   - Is there a TODO task for EACH file with its EXACT structure?
   - If X serves as input elsewhere, have you verified consumer requirements?

   **If ANY answer is "no", this is a missed requirement - add to TODO immediately.**

4. **List all requirements fresh**
   - Write requirements from scratch based on this reading
   - Don't reference your TODO while doing this
   - Number each requirement

5. **Compare to TODO**
   - Match fresh list against existing TODO tasks
   - Identify any requirements missing from TODO
   - Identify any TODO tasks not tied to requirements

6. **Document findings**
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

**Purpose:** Plan behavior tests that would fail if algorithm is wrong, and audit mocks to ensure they match real interfaces.

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

5. **Mock Audit (CRITICAL):**
   For each mocked dependency in the test plan:

   a. **List all mocked classes/methods:**
      ```
      | Mock | Real Class | Real Method | Signature Verified? |
      |------|------------|-------------|---------------------|
      | mock_config_gen | ConfigGenerator | generate_iterative_combinations | [ ] |
      | mock_progress | ProgressTracker | update | [ ] |
      ```

   b. **Verify each mock matches real interface:**
      - Read the actual class definition
      - Compare mock method calls to real method signatures
      - Verify parameter names and types match
      - Flag any mismatches for correction

   c. **Check for over-mocking:**
      - If mock accepts ANY arguments, it won't catch interface mismatches
      - Consider using `spec=RealClass` in `@patch` decorators
      - Example: `@patch('module.ClassName', spec=ClassName)`

   d. **Plan at least one integration test:**
      - Identify which test can use REAL objects instead of mocks
      - This test should exercise the actual integration path
      - Document: "Integration test X uses real ConfigGenerator and ProgressTracker"

   **Mock Audit Checklist:**
   ```
   □ All mocked dependencies listed
   □ Each mock's interface verified against real class
   □ At least one integration test planned with real objects
   □ Tests using spec= where appropriate
   □ No tests that would pass with wrong interface
   ```

6. **Output Consumer Validation (MANDATORY for features producing output files):**

   a. **Identify all outputs and their consumers:**
      ```
      | Output | Consumer | Consumer Location | Roundtrip Test |
      |--------|----------|-------------------|----------------|
      | accuracy_optimal_*/ | find_baseline_config | run_accuracy_sim.py | test_output_as_baseline |
      | accuracy_optimal_*/ | ConfigGenerator | shared/ConfigGenerator.py | test_output_as_baseline |
      ```

   b. **Plan roundtrip test for each output/consumer pair:**
      - Test MUST save output using new code
      - Test MUST load output using REAL consumer (not mocked)
      - Test MUST verify loaded data is usable

   c. **Example roundtrip test:**
      ```python
      def test_optimal_folder_usable_as_baseline(self, manager):
          """Verify output folder can be loaded as baseline for next run."""
          # Save output
          output_path = manager.save_optimal_configs()

          # Verify all required files exist
          required = ['league_config.json', 'draft_config.json', 'week1-5.json', ...]
          for f in required:
              assert (output_path / f).exists()

          # Load using REAL consumer (not mocked)
          config_gen = ConfigGenerator(output_path, parameter_order=...)
          assert config_gen.baseline_config is not None
      ```

   **Output Consumer Checklist:**
   ```
   □ All output files/folders identified
   □ All consumers of each output identified
   □ Roundtrip test planned for each output
   □ Roundtrip test uses REAL consumers, not mocks
   □ Test verifies output is actually usable, not just exists
   ```

**Output:** Test plan with behavior tests for all algorithms AND verified mock interfaces AND output consumer validation.

### Test Naming Convention

Use descriptive test names that explain what is being tested, under what conditions, and what should happen.

**Format:** `test_{unit}_{scenario}_{expected_behavior}`

**Good Examples:**
```python
# Clear: explains what, when, and expected outcome
def test_mae_calculation_with_bye_week_players_excludes_zero_actual():
    """MAE should exclude players with 0 actual points (bye weeks)."""
    pass

def test_player_rating_week_one_uses_draft_rank():
    """Week 1 player rating should use draft rank, not points."""
    pass

def test_config_save_with_empty_config_raises_validation_error():
    """Saving empty config should raise ValidationError."""
    pass

def test_parallel_runner_with_single_thread_completes_successfully():
    """Runner should work correctly even with thread_count=1."""
    pass
```

**Bad Examples:**
```python
# Vague: doesn't explain scenario or expected behavior
def test_mae():  # What about MAE? What scenario?
    pass

def test_player_rating():  # Which aspect? Which week?
    pass

def test_save():  # Save what? What should happen?
    pass

def test_1():  # Completely meaningless
    pass
```

**Why good names matter:**
- Test failures are immediately understandable: "test_mae_calculation_with_bye_week_players_excludes_zero_actual FAILED" tells you exactly what broke
- Tests serve as documentation: reading test names explains feature behavior
- Encourages thinking about edge cases: naming forces you to articulate the scenario

**Naming Checklist:**
```
□ Test name includes the unit being tested (method/class)
□ Test name includes the scenario/condition
□ Test name includes expected behavior/outcome
□ Test name is readable as a sentence when prefixed with "Verify that..."
```

---

### Test-First Implementation Principle

When possible, write tests BEFORE implementation:

**The Test-First Workflow:**
1. **Write failing test** that describes expected behavior
2. **Run test** - confirm it fails (red)
3. **Implement code** to make test pass
4. **Run test** - confirm it passes (green)
5. **Refactor** if needed, keeping tests green

**Benefits:**
- Forces you to think about behavior before code structure
- Naturally creates behavior tests (not structure tests)
- Catches "tests pass but behavior wrong" issues
- Documents expected behavior before implementation

**When to Use Test-First:**
- New methods with calculcations or algorithms
- New classes with business logic
- Edge case handling
- Any code where "what should happen" is clearer than "how to implement"

**When Test-First May Not Apply:**
- Simple data classes with no logic
- Boilerplate code (imports, setup)
- Integration code where the test requires the implementation to exist

**Test-First Checklist:**
```
□ Expected behavior documented in test name
□ Test runs and FAILS before implementation
□ Implementation makes test pass
□ Additional edge case tests added
□ Refactoring doesn't break tests
```

**Example:**
```python
# STEP 1: Write failing test FIRST
def test_mae_calculation_excludes_zero_actual_points():
    """MAE should exclude players with 0 actual points (bye weeks)."""
    players = [
        Player(projected=10.0, actual=12.0),  # Include
        Player(projected=15.0, actual=0.0),   # Exclude (bye week)
        Player(projected=8.0, actual=10.0),   # Include
    ]
    calculator = AccuracyCalculator()
    mae = calculator.calculate_mae(players)
    # Expected: (|10-12| + |8-10|) / 2 = (2 + 2) / 2 = 2.0
    assert mae == 2.0  # NOT (2 + 15 + 2) / 3 = 6.33

# STEP 2: Run test - it fails (AccuracyCalculator doesn't exist yet)
# STEP 3: Implement AccuracyCalculator.calculate_mae()
# STEP 4: Run test - it passes
# STEP 5: Add more edge case tests
```

---

### Pre-Implementation Spec Audit Protocol

**Purpose:** Comprehensive spec-to-TODO audit with fresh eyes to catch all mismatches, missing details, and vague instructions before implementation begins. This is the final quality gate before code is written.

**Execute during:** Iteration 23a (immediately after Integration Gap Check, before Implementation Readiness)

**Historical Context:** Added after feature implementation passed all 24 iterations but failed QC Round 1 with 40% failure rate. This audit would have caught ALL 8 issues found in QC (wrong structure, missing fields, incorrect mappings) BEFORE any code was written.

**Critical Mindset:** Pretend you're a QA reviewer who's never seen this feature before. You have:
- ✅ The specs.md file
- ✅ The TODO.md file
- ❌ NO OTHER CONTEXT

Your job: Find every mismatch, missing detail, and vague instruction.

**Four-Part Audit:**

#### Part 1: Spec Coverage Audit (Completeness)

For EACH section in specs.md:

1. **Read spec section** (e.g., "Section 2: Common Player Fields")
2. **Extract all requirements** from that section (list them individually)
3. **Find corresponding TODO items** that implement those requirements
4. **Verify each requirement has:**
   - [ ] A TODO item that addresses it
   - [ ] Acceptance criteria that matches the spec exactly
   - [ ] Spec line reference
   - [ ] Example of correct output

**Red flags:**
- ⛔ Spec requirement with no TODO item
- ⛔ TODO item exists but no acceptance criteria
- ⛔ Acceptance criteria doesn't match spec
- ⛔ No example showing what "correct" looks like

**Example audit finding:**
```
SPEC SECTION: Common Player Fields (specs.md lines 44-56)

Requirements extracted:
1. id (number) - converted from string
2. name (string)
3. team (string)
4. position (string)
5. injury_status (string)
6. drafted_by (string)
7. locked (boolean)
8. average_draft_position (number or null)
9. player_rating (number or null)
10. projected_points (array[17])
11. actual_points (array[17])

TODO items found:
- Phase 4.3: Build position JSON

Acceptance criteria in TODO:
- "Include all fields" ❌ VAGUE
- No list of 11 fields ❌ INCOMPLETE
- No types specified ❌ MISSING
- No spec reference ❌ MISSING

STATUS: ❌ FAIL - TODO incomplete
ACTION REQUIRED: Add all 11 fields with types and spec reference
```

#### Part 2: TODO Clarity Audit (Actionability)

For EACH TODO item:

1. **Cover up the specs.md file** (pretend you can't see it)
2. **Read ONLY the TODO item**
3. **Ask: "Could I implement this correctly right now?"**
4. **If NO, identify what's missing:**
   - Missing data structure?
   - Missing field list?
   - Missing constraints (array length, type, etc.)?
   - Missing examples?
   - Ambiguous wording?

**Red flags:**
- ⛔ "Transform to..." without showing structure
- ⛔ "Build..." without listing components
- ⛔ "Include all..." without enumerating
- ⛔ "Handle..." without specifying behavior
- ⛔ No examples of correct output
- ⛔ No anti-examples of common mistakes

#### Part 3: Data Structure Audit (Exactness)

For EACH data structure mentioned in specs:

1. **Find the structure in specs** (e.g., JSON root structure)
2. **Find corresponding TODO item**
3. **Verify TODO shows EXACT structure:**
   - Same field names
   - Same nesting
   - Same types
   - Same array lengths
   - Same null handling

**Red flags:**
- ⛔ Structure described in words, not shown
- ⛔ Field names differ from spec
- ⛔ Nesting level differs
- ⛔ Missing required fields
- ⛔ Wrong types

#### Part 4: Mapping Audit (Correctness)

For EACH mapping in specs (e.g., ESPN stat IDs to fields):

1. **Find mapping table in specs**
2. **Find corresponding TODO item**
3. **Verify TODO includes complete mapping:**
   - All source values listed
   - All target values listed
   - Transformation logic specified
   - Edge cases handled

**Red flags:**
- ⛔ Mapping mentioned but not shown
- ⛔ Incomplete mapping (some items missing)
- ⛔ No transformation logic
- ⛔ No edge case handling

**Completion Criteria:**

All four audits must pass:

- [ ] **Part 1 (Coverage):** Every spec requirement has TODO item with acceptance criteria
- [ ] **Part 2 (Clarity):** Every TODO item is implementable without reading specs
- [ ] **Part 3 (Structure):** Every data structure in specs is shown exactly in TODO
- [ ] **Part 4 (Mapping):** Every mapping in specs is documented in TODO

**If ANY audit fails:**
1. Document all findings in audit report
2. Update TODO with missing details from specs
3. Re-run audit until all parts pass
4. **DO NOT proceed to Iteration 24** until audit passes

**Audit Output Template:**

```markdown
## Iteration 23a: Pre-Implementation Spec Audit

**Audit Date:** [Date]
**Auditor Mindset:** Fresh eyes, never seen this feature before

### Part 1: Spec Coverage Audit
- [ ] Section 1 (File Structure): X requirements, Y TODO items ✅/❌
- [ ] Section 2 (Common Fields): X requirements, Y TODO items ✅/❌
- [ ] Section 3 (Position Stats): X requirements, Y TODO items ✅/❌
...

**Findings:**
1. [Issue found]
2. [Issue found]

**Status:** ✅ PASS / ❌ FAIL (X issues found)

### Part 2: TODO Clarity Audit
- [ ] Phase 1: All items actionable without specs? ✅/❌
- [ ] Phase 2: All items actionable without specs? ✅/❌
...

**Findings:**
1. [Vague item]
2. [Missing details]

**Status:** ✅ PASS / ❌ FAIL (X items need clarification)

### Part 3: Data Structure Audit
- [ ] Root JSON structure matches specs exactly? ✅/❌
- [ ] Player object structure matches specs exactly? ✅/❌
- [ ] Stat structure matches specs exactly? ✅/❌
...

**Findings:**
1. [Structure mismatch]
2. [Missing fields]

**Status:** ✅ PASS / ❌ FAIL (X mismatches found)

### Part 4: Mapping Audit
- [ ] ESPN stat ID mappings complete? ✅/❌
- [ ] drafted (0/1/2) → drafted_by mapping complete? ✅/❌
- [ ] locked (0/1) → boolean mapping complete? ✅/❌
...

**Findings:**
1. [Missing mapping]
2. [Incomplete mapping]

**Status:** ✅ PASS / ❌ FAIL (X mappings incomplete)

### OVERALL AUDIT RESULT: ✅ PASS / ❌ FAIL

**Total Issues Found:** X

**Actions Required Before Implementation:**
1. [Fix 1]
2. [Fix 2]
...

**Ready for Iteration 24 (Implementation Readiness)?** ✅ YES / ❌ NO
```

**Key Insight:** The audit must be done with "fresh eyes" - pretending you've never seen the feature before. This forces you to rely ONLY on the TODO, which reveals gaps that familiarity would hide.

**What This Audit Would Have Caught:**

Historical evidence from feature that failed QC Round 1:
- ✅ Wrong root structure (Structure Audit Part 3)
- ✅ Missing 3 common fields (Coverage Audit Part 1)
- ✅ Wrong stat structure (Structure Audit Part 3)
- ✅ Wrong stat mappings (Mapping Audit Part 4)
- ✅ Missing field types (Clarity Audit Part 2)
- ✅ Vague acceptance criteria (Clarity Audit Part 2)

**Result:** Would have prevented all rework, saved 2+ hours of implementation time.

**Output:** Audit report with pass/fail for all 4 parts, list of required fixes before implementation.

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

## Pre-Implementation Protocols

### Interface Verification Protocol

**Purpose:** Verify all dependency interfaces and data model attributes before writing implementation code.

**Execute:** Before starting any implementation work, after iteration 24.

**Steps:**

**Step 1: List All External Dependencies**
For each class the new code will use, document:
```
| Dependency | File | Methods to Call | Verified? |
|------------|------|-----------------|-----------|
| ConfigGenerator | shared/ConfigGenerator.py | generate_iterative_combinations() | [ ] |
| ProgressTracker | shared/ProgressTracker.py | update(), complete() | [ ] |
| PlayerManager | util/PlayerManager.py | load_players(), get_player() | [ ] |
```

**Step 2: Verify Interfaces Against Source**

**CRITICAL: Copy-Paste Requirement**

DO NOT verify interfaces from memory or documentation. ALWAYS:

1. **Open Actual Source File**
   - Navigate to the module containing the interface
   - Find the exact class/function definition
   - Scroll to the method you're calling

2. **Copy Exact Signature**
   ```python
   # EXAMPLE: Verifying DataFileManager.save_json_data()
   # From utils/data_file_manager.py line 365:
   def save_json_data(self, data: Any, prefix: str,
                      create_latest: bool = True, **json_kwargs) -> Tuple[Path, Optional[Path]]:
   ```

3. **Compare to Your Usage**
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

4. **Check Return Type**
   - Signature returns: `Tuple[Path, Optional[Path]]`
   - Your code expects: tuple unpacking with 2 elements
   - ✅ Compatible

5. **Verify method signatures match expectations:**
   ```
   Expected: generate_configs_for_parameter(param_idx)
   Actual:   generate_iterative_combinations(param_name, base_config)
   MISMATCH! → Update expectations to match actual
   ```

6. **Check required vs optional parameters**

7. **Look for existing usage patterns:** `grep -r "dependency_name\." .`

**Red Flags (DO NOT PROCEED if any are true):**
- [ ] Parameter order doesn't match signature
- [ ] Parameter types incompatible
- [ ] Return type incompatible
- [ ] Required parameters missing
- [ ] Method doesn't exist in source

**Why This Matters:**
Bug example from real feature: Called `save_json_data(prefix, data)` instead of `save_json_data(data, prefix)` because parameter order was assumed from memory. Unit tests mocked the dependency, so incorrect call succeeded in tests but failed in production.

**Step 3: Verify Data Model Attributes**
For each data model (dataclass, domain object) you'll access:
```
| Model | File | Attributes Needed | Exists? | Semantics |
|-------|------|-------------------|---------|-----------|
| FantasyPlayer | util/FantasyPlayer.py | actual_points | [ ] | Total actual season points |
| FantasyPlayer | util/FantasyPlayer.py | week_1_points | [x] | Week 1 actual points |
```

1. Read the actual class definition
2. List all attributes you plan to use
3. Verify each attribute exists in the definition
4. Check attribute semantics (e.g., does `fantasy_points` mean projected or actual?)

**Step 4: Document Interface Contracts**
Create a summary of verified interfaces:
```markdown
## Interface Contracts (Verified)

### ConfigGenerator
- Method: `generate_iterative_combinations(param_name: str, base_config: dict) -> Iterator[dict]`
- Source: simulation/shared/ConfigGenerator.py:145
- Existing usage: SimulationManager.py:180

### FantasyPlayer
- Attribute: `week_N_points` (N=1-17) - actual points for week N
- Attribute: `fantasy_points` - projected total points
- Note: NO `actual_points` attribute - must sum week_N_points
- Source: league_helper/util/FantasyPlayer.py:15
```

**Interface Verification Checklist:**
```
□ All external dependencies listed
□ Each dependency's methods verified against source code
□ Method signatures COPY-PASTED from source (not verified from memory)
□ Parameter order verified by side-by-side comparison
□ Parameter names and types confirmed
□ Return values documented
□ Data model attributes verified to exist
□ Attribute semantics understood (not assumed)
□ Interface contracts documented in TODO file
□ Quick E2E validation planned (minimal script run to verify interfaces)
```

**Step 5: Plan Quick E2E Validation**
Before implementation, plan a minimal E2E test to validate interfaces:
1. Identify the simplest possible E2E path through the new code
2. Plan to run this BEFORE writing all implementation code
3. This catches interface mismatches early, not after days of development

**Example:**
```
Quick E2E Plan:
1. Create minimal AccuracyCalculator with just calculate_mae()
2. Run: python -c "from accuracy import AccuracyCalculator; ac = AccuracyCalculator(); print(ac.calculate_mae([]))"
3. Expected: Should return 0.0 or raise clear error
4. If import fails: Interface mismatch detected early
```

**Output:** Interface contract documentation in TODO file, all dependencies verified, quick E2E plan documented.

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

```
╔═════════════════════════════════════════════════════════════════╗
║  🛑 CRITICAL: 100% COMPLETION REQUIRED - NO EXCEPTIONS         ║
╠═════════════════════════════════════════════════════════════════╣
║                                                                 ║
║  There is NO "acceptable partial" category.                    ║
║  There is NO "we'll finish it later" exception.                ║
║  There is NO "structure is done, data is pending" loophole.    ║
║                                                                 ║
║  EVERY requirement MUST be FULLY implemented.                  ║
║  EVERY data field MUST contain REAL data (not zeros/nulls).   ║
║  EVERY feature MUST achieve its PRIMARY USE CASE.              ║
║                                                                 ║
║  IF ANY REQUIREMENT IS INCOMPLETE:                             ║
║  → Requirement Verification FAILS                              ║
║  → Return to implementation immediately                        ║
║  → Complete ALL missing requirements                           ║
║  → Re-run verification from Step 1                             ║
║                                                                 ║
╚═════════════════════════════════════════════════════════════════╝
```

**Required for PASS:**

- ✅ ALL requirements from original file implemented (100% coverage)
- ✅ ALL question answers reflected in implementation
- ✅ NO missing functionality or partial implementations
- ✅ NO placeholder data (zeros, nulls, empty arrays where real data required)
- ✅ NO "TODO: implement later" comments in production code
- ✅ Evidence of implementation exists in codebase
- ✅ All unit tests pass (100%)
- ✅ Manual testing confirms functionality works
- ✅ Feature achieves its PRIMARY USE CASE completely
- ✅ ALL new methods have identified callers (no orphan code)
- ✅ Integration verified from entry point to output
- ✅ Actual scripts run and produce expected behavior
- ✅ Minimum 3 quality control review rounds completed
- ✅ Lessons learned reviewed and guide updates applied

**Automatic FAIL conditions:**

- ❌ Any requirement marked "partial" or "incomplete"
- ❌ Any data field with placeholder values (zeros, nulls) where real data expected
- ❌ Feature cannot achieve primary use case with current implementation
- ❌ Any "future work" or "pending" items that block core functionality

---

### Smoke Testing Protocol

**When:** Before declaring any feature complete

**Purpose:** Verify code actually runs, not just that tests pass

**Required Tests:**
1. Import test - All modules can be imported
2. Entry point test - Scripts/CLIs start without errors
3. Execution test - Basic functionality works end-to-end

**Pass Criteria:** All 3 test types must pass before feature is "complete"

**See:** feature_development_guide.md "Post-Implementation Smoke Testing" for details

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

**Round 1: Script Execution Test (MANDATORY)**

If the feature includes a runner script (`run_*.py`), you MUST:

1. **Execute the script with --help** to verify argument parsing works:
   ```bash
   python run_feature.py --help
   # Should display help text without errors
   ```

2. **Execute the script in dry-run mode** (if available) or with minimal input:
   ```bash
   python run_feature.py --mode test --iterations 1
   # Should complete without crashing
   ```

3. **Execute the script end-to-end** with real data:
   - Not mocked dependencies
   - Not simulated paths
   - Actual file system interactions
   ```bash
   python run_feature.py --mode full
   # Should produce expected output files
   ```

4. **Verify output:**
   - Check output files exist
   - Check output content is valid (non-zero values, correct format)
   - Check no error messages in output

**Scripts without execution tests must not pass QC Round 1.**

**When E2E tests reveal errors:**
1. Fix the immediate error
2. Before continuing, perform root cause analysis:
   - Why was this error created in the first place?
   - Why wasn't it caught during unit testing?
   - Why wasn't it caught during verification iterations?
3. Document findings in the lessons learned file
4. Only proceed after documenting the lesson

Then proceed with document review:
5. Re-read the specification file (`{feature_name}_specs.md`)
6. Re-read the TODO file (`{feature_name}_todo.md`)
7. Re-read the code changes file (`{feature_name}_code_changes.md`)
8. Cross-reference all three documents
9. Identify any discrepancies, missing items, or incorrect implementations
10. Document findings and fix any issues found

**Round 2: Deep Verification Review**
1. With fresh perspective, repeat the same review process
2. Focus on algorithm correctness and edge cases
3. Verify conditional logic matches spec exactly
4. Check that tests actually validate the behavior (not just structure)
5. Execute **Semantic Diff Check** (see below)
6. Document findings and fix any issues found

**Semantic Diff Check (Round 2):**

Before completing Round 2, verify changes are minimal and intentional:

1. **Run `git diff` and review each change:**
   - Are there whitespace-only changes? → Remove them
   - Are there reformatting changes unrelated to the feature? → Remove them
   - Are there "while I'm here" improvements? → Should have been scoped earlier

2. **For each changed file, verify:**
   ```
   □ File was listed in TODO's "Files to Modify" section
   □ If NOT listed, document why it needed changes
   □ Changes are minimal - only what's needed for the feature
   ```

3. **Check for scope creep in code:**
   - Did you refactor code that didn't need refactoring?
   - Did you add logging/comments beyond what was specified?
   - Did you "improve" adjacent code that was working fine?

4. **If unexpected changes exist:**
   - Either remove them (revert to original)
   - Or document why they were necessary and get user approval

**Why this matters:** Minimal diffs are:
- Easier to review (less noise)
- Easier to rollback (fewer side effects)
- Less likely to cause merge conflicts
- Easier to understand in git history

**Round 3: Final Skeptical Review**
1. Assume previous reviews missed something
   > *Rationale: Confirmation bias causes us to see what we expect. Round 3 exists specifically to counteract this - actively look for what's WRONG, not what's right.*
2. Re-read spec with "adversarial" mindset - actively look for gaps
   > *Rationale: If you look for problems, you'll find them. If you look for confirmation that everything works, you'll miss issues.*
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

## Rollback Protocol

Use when implementation fails and changes need to be undone:

```
┌─────────────────────────────────────────────────────────────────┐
│  ROLLBACK PROTOCOL - WHEN IMPLEMENTATION FAILS                  │
└─────────────────────────────────────────────────────────────────┘
```

**When to Use:**
- Tests fail after implementation and cannot be fixed quickly
- Implementation reveals fundamental spec issues
- User requests abandoning current approach
- Breaking changes to unrelated functionality discovered

**Rollback Steps:**

1. **Document the Failure**
   - Add entry to `_lessons_learned.md` explaining:
     - What was attempted
     - What failed and why
     - What was learned
   - Capture specific error messages or test failures

2. **Revert Changes**
   ```bash
   # View changes to decide what to revert
   git diff

   # Option A: Revert all uncommitted changes
   git checkout -- .

   # Option B: Revert specific files
   git checkout -- path/to/file.py

   # Option C: If already committed, revert to previous commit
   git revert HEAD
   ```

3. **Verify Clean State**
   - Run `python tests/run_all_tests.py` - must pass
   - Verify no orphan changes remain with `git status`

4. **Update Feature Status**
   - Update README.md "Agent Status" to indicate rollback
   - Move feature back to appropriate phase if needed
   - Document what needs to be re-planned

5. **Notify User**
   - Explain what was rolled back
   - Present options for next steps:
     - Re-plan with different approach
     - Abandon feature
     - Address underlying issue first

**Prevention:** Most rollbacks indicate insufficient verification. If rollback is needed, consider whether:
- Pre-flight checklist was completed
- All 24 verification iterations were thorough
- Interface verification caught the issue

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
