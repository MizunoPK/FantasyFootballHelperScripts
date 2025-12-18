# Accuracy Simulation - Lessons Learned

> **PURPOSE**: This file captures issues encountered during development and QA that could have been prevented by better planning or development processes. After the feature is complete, these lessons will be used to update both guides in the `feature-updates/guides/` folder.

---

## How to Use This File

**When to add entries:**
1. During development: When you discover an edge case the planning phase should have identified
2. During development: When you find an issue that better verification would have caught
3. During QA: When testing reveals a problem the development process should have prevented
4. After user feedback: When the user reports something that wasn't working as expected

**What to capture:**
- What went wrong or was missed
- Why it happened (root cause)
- How the guides could be updated to prevent this in the future
- Specific additions or changes to recommend

---

## Lessons Learned

### Lesson 1: Insufficient Checklist Question Generation

**Date:** 2025-12-13

**What Happened:**
During Phase 2 (Investigation), the agent populated the checklist with open questions after a single pass of analysis. When the user asked "can you think of any more potential questions?", the agent identified 21 additional questions across 8 new categories that were missed in the initial pass.

**Root Cause:**
One round of thinking about checklist questions was insufficient to identify all relevant concerns. The initial pass focused on the obvious questions from the notes and immediate codebase findings, but missed:
- Scoring mode configuration questions
- Multi-season handling questions
- Parallelization & performance questions
- Logging & debugging questions
- Relationship between simulation modes
- Additional edge cases (minimum thresholds)
- Integration workflow questions

**Impact:**
Had these questions not been surfaced before implementation, they would have been discovered mid-development, causing rework or incomplete implementation.

**Recommended Guide Update:**

**Which Guide:** feature_planning_guide.md

**Section to Update:** Phase 2: Investigation, Step 2.3 (Populate the checklist with open questions)

**Recommended Change:**
Add a mandatory 3-iteration requirement for checklist question generation:

```markdown
### Step 2.3.1: Three-Iteration Question Generation (MANDATORY)

After initial checklist population, complete THREE separate iterations of question generation:

**Iteration 1:** Review initial questions and categories. For each category, ask:
- "What edge cases might apply here?"
- "What error conditions could occur?"
- "What configuration options might be needed?"

**Iteration 2:** Consider operational aspects:
- Logging and debugging needs
- Performance and parallelization
- Testing and validation approaches
- Integration with existing workflows

**Iteration 3:** Consider relationships and comparisons:
- How does this feature relate to similar existing features?
- What cross-cutting concerns exist (multi-season, multi-mode)?
- What user workflow questions remain?

Document new questions discovered in each iteration before proceeding to Phase 3.
```

---

### Lesson 2: Checklist Items Need Codebase Verification

**Date:** 2025-12-14

**What Happened:**
After generating checklist questions through 3 iterations, many questions remained that could potentially be answered by researching the existing codebase rather than asking the user. The agent should proactively search for answers before presenting questions to the user.

**Root Cause:**
The planning guide focuses on generating questions but doesn't emphasize verifying which questions can be answered through codebase research vs. which truly require user input.

**Impact:**
- User is asked questions that have obvious answers in the code
- Planning phase takes longer than necessary
- User's time is wasted on questions the agent could answer itself

**Recommended Guide Update:**

**Which Guide:** feature_planning_guide.md

**Section to Update:** Phase 2: Investigation (add new step after 2.3)

**Recommended Change:**
Add mandatory codebase verification rounds after question generation:

```markdown
### Step 2.4: Codebase Verification Rounds (MANDATORY)

After populating the checklist with questions, perform TWO verification rounds:

**Round 1: Initial Codebase Research**
For each open checklist item:
1. Search the codebase for relevant code, patterns, or existing implementations
2. If a straightforward answer exists in the code → document it and mark resolved
3. If multiple valid approaches exist → document options with code references for user decision
4. If no answer found in codebase → leave as open question for user

**Round 2: Skeptical Re-verification**
Assume all findings from Round 1 are potentially incorrect:
1. Re-search with different terms and approaches
2. Verify claims made in Round 1 are accurate
3. Check for edge cases or exceptions missed in Round 1
4. Look for contradictions between code and documentation

**Output:** Checklist should be categorized into:
- [x] Resolved via codebase research (with code references)
- [ ] Needs user decision (multiple valid approaches documented)
- [ ] Truly unknown (no answer in codebase, requires user input)
```

---

### Lesson 3: Architectural Decisions Deferred as "Implementation Details"

**Date:** 2025-12-14

**What Happened:**
During implementation, Task 6.1a (Update LeagueHelperManager to pass `use_draft_config`) was marked as "DEFERRED - Requires user decision on refactoring approach." However, this decision should have been made during planning, not deferred to implementation.

The task was identified during Iteration 7 (Integration Gap Check #1), but the note just documented alternatives without escalating it as a question requiring user input:
- "Note: May need to refactor - currently ConfigManager is created once at startup"
- "Alternative: Create separate ConfigManager for Add to Roster Mode, or reload config when entering mode"

**Root Cause:**
1. **Architectural decisions treated as implementation details** - The question of "how should Add to Roster Mode get its config" affects behavior (which config file is used), not just code structure. This should have been flagged for user decision during planning.

2. **Verification protocols didn't catch it** - The Integration Gap Check protocol found the gap but didn't require resolving ambiguities before marking complete. Alternatives were documented but no decision was made.

3. **No questions file created** - The TODO noted "No questions file needed - spec is complete" despite an unresolved architectural question existing.

4. **"Alternative:" notes not treated as blockers** - When multiple valid approaches are documented with "Alternative:", this should trigger a mandatory user question, not be left as an open item.

**Impact:**
- Implementation was marked "complete" with an unresolved architectural question
- User had to discover the deferred decision post-implementation
- The decision still needs to be made, causing additional back-and-forth

**Recommended Guide Update:**

**Which Guide:** feature_development_guide.md

**Section to Update:** Verification protocols (all iterations that check integration)

**Recommended Change:**
Add a mandatory check for unresolved alternatives:

```markdown
### Integration Gap Check - Additional Requirement

Before marking an integration gap check complete, verify:

1. **No "Alternative:" notes remain unresolved** - If multiple valid approaches exist for any task:
   - Document the options with pros/cons
   - Create a question in the questions file
   - DO NOT proceed past verification until user decides

2. **No "May need to..." notes remain** - Phrases like "may need to refactor" indicate uncertainty that must be resolved:
   - Investigate to determine if refactoring IS needed
   - If yes, document the approach and get user approval
   - If no, remove the note and document why not needed

3. **All DEFERRED items have valid deferral reasons** - Valid reasons to defer:
   - "Will be created when X runs" (file generation)
   - "Low priority, not blocking" (documentation)

   Invalid reasons to defer:
   - "Requires user decision" (should have been asked during planning)
   - "Multiple approaches possible" (should have been decided during planning)
```

---

### Lesson 5: Mocked Dependencies Hide Interface Mismatches

**Date:** 2025-12-15

**What Happened:**
During E2E testing, the simulation failed with:
```
TypeError: MultiLevelProgressTracker.__init__() got an unexpected keyword argument 'log_interval'
```

The `AccuracySimulationManager` called `MultiLevelProgressTracker(total_params, configs_per_param, log_interval=10)`, but `MultiLevelProgressTracker.__init__()` doesn't accept a `log_interval` parameter.

**Root Cause:**
1. **Assumed interface match** - The developer assumed `MultiLevelProgressTracker` had the same interface as `ProgressTracker` (which does have `log_interval`).

2. **Mocking hid the mismatch** - Unit tests mocked `MultiLevelProgressTracker`, so the invalid parameter was never validated against the real class signature.

3. **No type checking at integration boundary** - The code didn't verify that the parameters being passed matched the actual class interface.

**Why Unit Tests Didn't Catch It:**
```python
# In the unit test:
@patch('simulation.accuracy.AccuracySimulationManager.MultiLevelProgressTracker')
def test_run_ros_optimization(self, mock_progress):
    # Mock accepts ANY arguments - doesn't validate signature!
    manager.run_ros_optimization()
```

**Fix Applied:**
Removed the invalid `log_interval=10` parameter from both calls in `AccuracySimulationManager.py`.

---

### Lesson 6: Multiple Interface Mismatches Indicate Insufficient Implementation Review

**Date:** 2025-12-15

**What Happened:**
After fixing Lesson 5, E2E testing revealed another error:
```
AttributeError: 'ConfigGenerator' object has no attribute 'generate_configs_for_parameter'
```

The `AccuracySimulationManager` was calling three methods that don't exist on `ConfigGenerator`:
1. `generate_configs_for_parameter(param_idx)` - doesn't exist
2. `update_baseline(config_dict)` - doesn't exist
3. `reset_to_original_baseline()` - doesn't exist

The actual ConfigGenerator interface uses:
- `generate_iterative_combinations(param_name, base_config)` - takes param name and config dict
- `baseline_config` attribute - direct access, manually track and update

**Root Cause:**
1. **Implementation written without reading the actual interface** - The AccuracySimulationManager code assumed an API that was never implemented in ConfigGenerator.

2. **Unit tests mocked the dependency** - Tests for AccuracySimulationManager created mock ConfigGenerator objects that accepted any method call.

3. **No reference to existing usage** - The win-rate SimulationManager shows the correct pattern for using ConfigGenerator, but the accuracy implementation didn't follow that pattern.

**Fix Applied:**
Rewrote `run_ros_optimization` and `run_weekly_optimization` to:
- Use `generate_iterative_combinations(param_name, current_base_config)`
- Track `current_base_config` locally and deep copy it when updating
- Import `copy` module for `copy.deepcopy()`

**Recommended Guide Update:**

**Which Guide:** feature_development_guide.md

**Section to Update:** Implementation Phase

**Recommended Change:**
Add reference implementation requirement:

```markdown
### Implementation Phase - Reference Existing Usage

Before implementing new code that uses existing modules:

1. **Find existing usage examples** - Search codebase for how other code uses the same class/module
2. **Read the actual method signatures** - Not just docstrings, check the real `def` lines
3. **Verify against existing tests** - See how the class is used in its own unit tests
4. **Create one unmocked integration point** - At least one test should call the real dependency

Example: If using ConfigGenerator in new code:
- Search: `grep -r "config_generator\." simulation/`
- Find: SimulationManager.py shows correct usage pattern
- Copy the pattern, not invent new method names
```

---

### Lesson 7: Consolidate Related Interface Errors

**Date:** 2025-12-15

**What Happened:**
After fixing Lesson 6 (ConfigGenerator methods), another interface mismatch was found:
```
AttributeError: 'MultiLevelProgressTracker' object has no attribute 'update'
```

The code called `progress.update(param_idx, config_idx)` but `MultiLevelProgressTracker` has `update_inner(completed)` and `next_outer()`, not a generic `update()`.

**Root Cause:**
Same root cause as Lessons 5 and 6 - mocked dependencies hid interface mismatches. This is the third such error in the same file.

**Fix Applied:**
Switched from `MultiLevelProgressTracker` to the simpler `ProgressTracker` which has the `update()` method, as the accuracy simulation doesn't need two-level progress tracking.

**Key Observation:**
Three interface mismatches in one class (`AccuracySimulationManager`) indicate the entire class was written without verifying the actual interfaces of its dependencies. This suggests the development process had a systemic gap, not just one-off mistakes.

**Recommended Guide Update:**

**Which Guide:** feature_development_guide.md

**Section to Update:** Implementation Phase

**Recommended Change:**
Add a pre-implementation interface verification step:

```markdown
### Pre-Implementation - Interface Verification

Before writing code that uses existing classes, perform interface verification:

1. **List all external dependencies** the new class will use
2. **For each dependency:**
   - Read the class definition (not just mocks)
   - List the methods and their signatures
   - Note required vs optional parameters
3. **Create a "dependency interface" document** listing:
   - Class name
   - Methods to be used
   - Expected parameters
4. **Verify against source** before writing implementation

This prevents writing code that assumes non-existent interfaces.
```

**Recommended Guide Update:**

**Which Guide:** feature_development_guide.md

**Section to Update:** Implementation Verification

**Recommended Change:**
Add interface verification requirement:

```markdown
### Implementation Verification - Interface Compatibility

When calling methods/constructors from other modules:

1. **Read the actual interface** - Don't assume based on similar classes
2. **Check the signature in the source** - Not just the test mocks
3. **Verify parameter names match** - Especially for keyword arguments
4. **Add smoke tests that don't mock dependencies** - At least one test should call the real classes together

If mocking a class for unit tests:
- Consider adding a spec to the mock: `@patch('...', spec=RealClass)`
- This will raise errors if you call methods that don't exist
```

---

### Lesson 9: QA Rounds Must Happen Throughout Development, Not Just at End

**Date:** 2025-12-15

**What Happened:**
Two full QC sessions passed without finding issues, yet the user encountered immediate failures when running the script:
1. Missing `season_schedule.csv` and `team_data/` in temp directory
2. `actual_points` attribute doesn't exist on FantasyPlayer

Both issues would have been caught by a single real E2E execution: `python run_accuracy_simulation.py --mode ros`

**Root Cause:**
1. **QA deferred to the end** - All 24 verification iterations and 3 QC rounds happened after implementation was "complete"
2. **QC relied on mocked tests** - Unit tests passed but mocked the exact dependencies that had bugs
3. **No incremental E2E testing** - The runner script was never executed with real data until the user tried it
4. **"Works in theory" accepted as "works"** - Code review and reasoning replaced actual execution

**The Pattern of Failure:**
```
Implementation Phase:
  - Write _create_player_manager() ← Bug introduced (missing season files)
  - Write _evaluate_config_ros() ← Bug introduced (wrong attribute name)
  - Write unit tests with mocks ← Bugs hidden
  - [NO E2E TEST HERE]

QC Round 1: Unit tests pass, --help works ← Bugs still hidden
QC Round 2: Same checks ← Bugs still hidden
QC Round 3: Same checks ← Bugs still hidden

User runs script → Both bugs immediately surface
```

**What Should Have Happened:**
```
Implementation Phase:
  - Write _create_player_manager()
  - Write _evaluate_config_ros()
  - [E2E TEST: Run with one season of real data]
  - ❌ "No valid players" → Fix attribute bug immediately
  - ❌ "season_schedule.csv not found" → Fix file copying immediately
  - Continue implementation with known-working foundation

QC Rounds: Verify edge cases, performance, error handling
```

**Key Insight:**
QA at the end can only verify that bugs still exist. QA during development catches bugs when they're introduced, before more code is built on broken foundations.

**Recommended Guide Update:**

**Which Guide:** feature_development_guide.md

**Section to Update:** TODO File Creation (Phase 3) and Implementation Phase

**Recommended Change:**
Add incremental QA checkpoints to the development process:

```markdown
### Phase 3: TODO File Creation - QA Checkpoint Planning

When creating the TODO file, identify QA checkpoints after each major phase:

1. **For each implementation phase, add a QA checkpoint task:**
   - "QA Checkpoint: [Phase Name]"
   - List what can be tested at this point
   - List expected outcomes (not just "tests pass")

2. **QA Checkpoint Requirements:**
   - Run all existing unit tests
   - Run E2E test with real data (whatever is testable so far)
   - Verify output is meaningful (non-zero values, expected format)
   - Document any issues found before proceeding

3. **Example TODO structure:**
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

4. **QA Checkpoint Failure Protocol:**
   - STOP development
   - Fix the issue before proceeding
   - Re-run checkpoint to verify fix
   - Document what went wrong in lessons learned

### Implementation Phase - Incremental QA

After completing each TODO phase:

1. **Run the QA checkpoint defined in the TODO**
2. **Verify expected outcomes are met** (not just "no errors")
3. **If checkpoint fails:**
   - Fix immediately (don't defer)
   - Understand why unit tests didn't catch it
   - Add tests to prevent regression
4. **Only proceed to next phase after checkpoint passes**

**Why This Matters:**
- Bugs caught at introduction are 10x easier to fix
- Later code won't be built on broken foundations
- QC rounds at the end verify polish, not basic functionality
- User never sees "it doesn't work at all" failures
```

---

### Lesson 8: Verify Data Model Attributes Match Implementation Assumptions

**Date:** 2025-12-15

**What Happened:**
After fixing temp directory file copying issues, the accuracy simulation still showed "No valid players for MAE calculation" with MAE=0.0000 and player_count=0. Investigation revealed:

```python
# Code assumed this attribute existed:
actual_total = getattr(player, 'actual_points', None)

# But FantasyPlayer dataclass has:
fantasy_points: float = 0.0      # Total (often projected)
week_1_points: Optional[float]   # Actual week 1 points
week_2_points: Optional[float]   # Actual week 2 points
# ... through week_17_points
```

The `actual_points` attribute doesn't exist in `FantasyPlayer`. The actual season totals must be computed by summing `week_N_points` attributes.

**Root Cause:**
1. **Assumed attribute naming** - The developer assumed players would have an `actual_points` attribute without verifying the actual dataclass definition.

2. **Silent failure path** - The code used `getattr(player, 'actual_points', None)` which returns `None` when the attribute doesn't exist, causing all players to be silently skipped as "invalid" rather than raising an error.

3. **No data model verification step** - The development process didn't include checking the actual data model attributes against implementation assumptions.

4. **Misleading error message** - "No valid players" suggested a data loading problem when the actual issue was an attribute name mismatch.

**Fix Applied:**
Changed the actual points calculation to sum week_N_points:

```python
# Get actual season total by summing week_N_points
actual_total = 0.0
has_any_week = False
for week_num in range(1, 18):
    week_attr = f'week_{week_num}_points'
    if hasattr(player, week_attr):
        week_val = getattr(player, week_attr)
        if week_val is not None:
            actual_total += week_val
            has_any_week = True

if has_any_week and actual_total > 0:
    actuals[player.id] = actual_total
```

**Result After Fix:**
```
Aggregated MAE: 59.9838 from 1868 players across 3 seasons
```

**Recommended Guide Update:**

**Which Guide:** feature_development_guide.md

**Section to Update:** Implementation Phase

**Recommended Change:**
Add data model verification requirement:

```markdown
### Implementation Phase - Data Model Verification

Before writing code that accesses attributes on data models (dataclasses, domain objects):

1. **Read the actual class definition** - Not just usage examples
2. **List all attributes you plan to access** with their expected types
3. **Verify each attribute exists** in the actual class definition
4. **Check attribute semantics** - Does `fantasy_points` mean projected or actual?
5. **Avoid silent failure patterns** like `getattr(obj, 'attr', None)` for required attributes:
   - Use explicit attribute access to fail fast
   - Or check `hasattr()` and log when missing

**Data Model Checklist:**
- [ ] Read the dataclass/model definition (not just tests)
- [ ] Verified all accessed attributes exist
- [ ] Understood semantic meaning of each attribute
- [ ] Used fail-fast patterns for required attributes
```

---

### Lesson 4: Unit Tests Alone Don't Catch Integration Failures

**Date:** 2025-12-15

**What Happened:**
Two runtime errors occurred when the user ran `run_accuracy_simulation.py` for the first time:

1. **Logging configuration error:** `TypeError: unsupported operand type(s) for /: 'NoneType' and 'str'` - The script had `LOGGING_TO_FILE = False` but didn't define `LOGGING_FILE` or `LOGGING_FORMAT`, causing `setup_logger()` to fail.

2. **Folder vs file path error:** `ConfigGenerator requires a folder path, not a file` - The `find_baseline_config()` function returned a file path (`optimal_*/week1-5.json`) when `ConfigGenerator` expected a folder path.

**Root Cause:**
1. **No unit tests for runner scripts** - `run_accuracy_simulation.py` had no tests. It was created by copying patterns from other scripts but incompletely.

2. **Mocking hid the path type mismatch** - Unit tests for `AccuracySimulationManager` mocked the config path parameter, so the mismatch between what `find_baseline_config()` returned and what `ConfigGenerator` expected was never caught.

3. **No actual script execution during verification** - The 24 verification iterations and 3 QC rounds relied entirely on unit tests. The runner script was never actually executed to verify it works end-to-end.

4. **Docstring mismatch with architecture** - `find_baseline_config()` docstring said "Path to baseline config JSON" (a file), but the folder-based config architecture requires folder paths. This inconsistency wasn't caught.

**Impact:**
- User encountered immediate failures when trying to use the feature
- Errors were basic initialization failures, not edge cases
- Undermines confidence in the QA process

**Recommended Guide Update:**

**Which Guide:** feature_development_guide.md

**Section to Update:** QC Review Rounds (Phase 6)

**Recommended Change:**
Add mandatory end-to-end script execution as part of QC:

```markdown
### QC Round 1 - Additional Requirement: Script Execution Test

Before completing QC Round 1, if the feature includes a runner script (run_*.py):

1. **Execute the script with --help** to verify argument parsing works
2. **Execute the script in dry-run mode** (if available) or with minimal input
3. **Execute the script end-to-end** with real data:
   - Not mocked dependencies
   - Not simulated paths
   - Actual file system interactions
4. **Verify the script completes without errors** before proceeding

If a dry-run mode doesn't exist and end-to-end execution would take too long:
- Add a --dry-run flag to the script
- Or create a minimal integration test that executes the script subprocess

**Scripts without execution tests must not pass QC.**

**When E2E tests reveal errors:**
1. Fix the immediate error
2. Before continuing, perform root cause analysis:
   - Why was this error created in the first place?
   - Why wasn't it caught during unit testing?
   - Why wasn't it caught during verification iterations?
3. Document findings in the lessons learned file with:
   - Specific process gaps that allowed the error
   - Recommended guide updates to prevent recurrence
4. Only proceed after documenting the lesson
```

**Which Guide:** feature_development_guide.md

**Section to Update:** Verification Protocol - Implementation Verification

**Recommended Change:**
Add requirement for runner script unit tests:

```markdown
### Implementation Verification - Runner Script Requirements

For any new runner script (run_*.py) created:

1. **Create unit tests in tests/root_scripts/** that verify:
   - Argument parsing (all flags, defaults, invalid inputs)
   - Configuration discovery/loading
   - Error handling for missing files/folders
   - Integration with the main module

2. **Verify logging configuration is complete:**
   - All required constants defined (LOG_NAME, LOGGING_LEVEL, LOGGING_TO_FILE, LOGGING_FILE, LOGGING_FORMAT)
   - setup_logger() called with correct parameters
   - Test that script runs with LOGGING_TO_FILE=True and LOGGING_TO_FILE=False

3. **Verify path handling:**
   - Check docstrings match actual behavior (folder vs file)
   - Verify returned paths have correct type (is_dir() vs is_file())
   - Test with user-provided paths, not just auto-discovered paths
```

---

## Summary of Recommended Updates

After development and QA are complete, use this summary to update the guides:

| Guide | Section | Change Type | Description |
|-------|---------|-------------|-------------|
| feature_planning_guide.md | Phase 2, Step 2.3 | Add | Mandatory 3-iteration question generation process |
| feature_planning_guide.md | Phase 2, Step 2.4 | Add | Mandatory codebase verification rounds (2 passes) |
| feature_development_guide.md | Verification protocols | Add | Mandatory check for unresolved alternatives before completing integration gap checks |
| feature_development_guide.md | QC Round 1 | Add | Mandatory end-to-end script execution test |
| feature_development_guide.md | QC Round 1 | Add | Mandatory root cause analysis and lessons learned documentation when E2E errors found |
| feature_development_guide.md | Implementation Verification | Add | Runner script unit test requirements (argument parsing, logging, path handling) |
| feature_development_guide.md | Implementation Verification | Add | Interface compatibility verification (read actual interfaces, use spec= in mocks) |
| feature_development_guide.md | Implementation Phase | Add | Reference existing usage before implementing new code that uses existing modules |
| feature_development_guide.md | Implementation Phase | Add | Pre-implementation interface verification (list dependencies, read actual interfaces) |
| feature_development_guide.md | Implementation Phase | Add | Data model verification (read dataclass definitions, verify attribute existence) |
| feature_development_guide.md | TODO File Creation (Phase 3) | Add | QA checkpoint planning - identify testable milestones with expected outcomes |
| feature_development_guide.md | Implementation Phase | Add | Incremental QA - run checkpoints after each phase, fix before proceeding |

---

## Guide Update Status

- [x] All lessons documented
- [x] Recommendations reviewed with user
- [x] feature_planning_guide.md updated (2025-12-15)
  - Added Step 2.3.1: Three-Iteration Question Generation (MANDATORY)
  - Added Step 2.4: Codebase Verification Rounds (MANDATORY)
  - Updated Agent Quick Reference Checklist with new steps
- [x] feature_development_guide.md updated (2025-12-15)
  - Added Anti-Pattern 5: Assumed Interface Matches
  - Added Anti-Pattern 6: Silent Attribute Failures
  - Added Pre-Implementation: Interface and Data Model Verification (MANDATORY)
  - Added Reference Existing Usage (MANDATORY)
  - Added Incremental QA Checkpoints (MANDATORY)
  - Added Integration Gap Check - Additional Requirements
  - Added QC Round 1: Script Execution Test (MANDATORY)
  - Updated Common Mistakes to Avoid table with 5 new entries
  - Updated QC Round Checklist with interface/attribute verification
- [ ] Updates verified by user
