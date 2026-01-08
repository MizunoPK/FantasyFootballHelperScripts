# Fantasy Football Helper Scripts - Claude Code Guidelines

## 🚨 CRITICAL: TRUST FILE STATE OVER CONVERSATION SUMMARIES

**ALWAYS prioritize actual file contents over conversation summaries when determining project state:**

1. **Check README.md files FIRST** - These contain the authoritative current status
2. **Verify with actual source code** - Check what's actually implemented
3. **Read Agent Status sections** - These are updated to reflect true current state
4. **Conversation summaries can be outdated** - Files are the source of truth

**Example workflow:**
- User says "proceed" → Read current README.md Agent Status → Determine actual next step
- Don't assume conversation summary reflects current file state
- Always verify implementation status by checking actual code files

---

## Quick Start for New Agents

**FIRST**: Read `ARCHITECTURE.md` for complete architectural overview, system design, and implementation details.

**SECOND**: Read `README.md` for project overview, installation instructions, and usage guide.

**THIS FILE**: Contains workflow rules, coding standards, and commit protocols.

---

## Project-Specific Rules

### Epic-Driven Development Workflow (v2)

**Note:** CLAUDE_EPICS.md is kept as a separate portable file for copying to other projects. The complete content is also inlined below to ensure all agents always have these instructions loaded.

---

## Epic-Driven Development Workflow (v2)

The v2 workflow is a **7-stage epic-driven development process** for managing large projects:

**Workflow Overview:**
```
Stage 1: Epic Planning → Stage 2: Feature Deep Dives → Stage 3: Cross-Feature Sanity Check →
Stage 4: Epic Testing Strategy → Stage 5: Feature Implementation (5a→5b→5c→5d→5e per feature) →
Stage 6: Epic-Level Final QC → Stage 7: Epic Cleanup
```

**Terminology:**
- **Epic** = Top-level work unit (collection of related features)
- **Feature** = Individual component within an epic
- **KAI Number** = Unique epic identifier (tracked in EPIC_TRACKER.md)
- User creates `{epic_name}.txt` → Agent creates `KAI-{N}-{epic_name}/` folder with multiple `feature_XX_{name}/` folders

---

## 🚨 MANDATORY: Phase Transition Protocol

**When transitioning between ANY stage, you MUST:**

1. **READ the guide FIRST** - Use Read tool to load the ENTIRE guide for that stage
2. **ACKNOWLEDGE what you read** - Use the phase transition prompt from `feature-updates/guides_v2/prompts_reference_v2.md`
3. **VERIFY prerequisites** - Check prerequisites checklist in guide
4. **UPDATE Agent Status** - Update EPIC_README.md or feature README.md with current guide + timestamp
5. **THEN proceed** - Follow the guide step-by-step

**Phase transition prompts are MANDATORY for:**
- Starting any of the 7 stages (1, 2, 3, 4, 5a, 5b, 5c, 5d, 5e, 6, 7)
- Starting Stage 5a rounds (Round 1, 2, 3)
- Starting Stage 5c phases (Smoke Testing, QC Rounds, Final Review)
- Creating missed requirements or entering debugging protocol
- Resuming after session compaction

**See:** `feature-updates/guides_v2/prompts_reference_v2.md` → Complete prompt library

**Why this matters:** Reading the guide first ensures you don't miss mandatory steps. The prompt acknowledgment confirms you understand requirements. Historical evidence: 40% guide abandonment rate without mandatory prompts.

**Example prompts:** See `prompts_reference_v2.md` for phase transition examples

---

## Stage 1: When User Says "Help Me Develop {epic-name}"

**Trigger phrases:** "Help me develop...", "I want to plan...", "Let's work on..."

**Prerequisites:** User has created `feature-updates/{epic_name}.txt` with initial scratchwork notes.

**🚨 FIRST ACTION:** Use the "Starting Stage 1" prompt from `feature-updates/guides_v2/prompts_reference_v2.md`

**Workflow:**
1. READ: `stages/stage_1/epic_planning.md`
2. Assign KAI number from EPIC_TRACKER.md
3. Create git branch (see Git Branching Workflow below)
4. Analyze epic, propose feature breakdown (user confirms)
5. Create epic folder structure: `KAI-{N}-{epic_name}/` with `feature_XX_{name}/` folders
6. Create epic files: `EPIC_README.md`, `epic_smoke_test_plan.md`, `epic_lessons_learned.md`
7. Create feature files: `README.md`, `spec.md`, `checklist.md`, `lessons_learned.md`

**Next:** Stage 2 (Feature Deep Dives)

---

## Stage 2-4: Planning & Testing Strategy

**Stage 2: Feature Deep Dives** (Loop through ALL features)
- **READ:** `stages/stage_2/feature_deep_dive.md`
- Flesh out `spec.md` for each feature with detailed requirements
- Interactive question resolution (ONE question at a time)
- Compare to already-completed features for alignment
- Dynamic scope adjustment (if scope >35 items, propose split)

**Stage 2b.5: Specification Validation** (After each feature spec)
- **READ:** `stages/stage_2/phase_2b5_specification_validation.md`
- Assume everything in spec is wrong, validate with deep research
- Self-resolve checklist questions through additional codebase investigation
- Only leave genuine unknowns or multi-approach decisions for user
- Expected impact: 50-70% reduction in user questions

**Stage 3: Cross-Feature Sanity Check** (After ALL features planned)
- **READ:** `stages/stage_3/cross_feature_sanity_check.md`
- Systematic pairwise comparison of all feature specs
- Resolve conflicts and inconsistencies
- Get user sign-off on complete plan

**Stage 4: Epic Testing Strategy** (Update test plan)
- **READ:** `stages/stage_4/epic_testing_strategy.md`
- Update `epic_smoke_test_plan.md` based on deep dive findings
- Identify integration points between features
- Define epic success criteria

**Next:** Stage 5 (Feature Implementation - first feature)

---

## Stage 5: Feature Implementation (Loop per feature: 5a→5b→5c→5d→5e)

**Stage 5a: TODO Creation** (24 verification iterations across 3 rounds)

**🚨 FIRST ACTION:** Use the "Starting Stage 5a Round 1" prompt from `prompts_reference_v2.md`

- **Round 1:** READ `stages/stage_5/round1_todo_creation.md` (Iterations 1-7 + 4a MANDATORY GATE)
- **Round 2:** READ `stages/stage_5/round2_todo_creation.md` (Iterations 8-16, >90% test coverage required)
- **Round 3:** READ `stages/stage_5/round3_todo_creation.md` (Router to Part 1/Part 2, Iterations 17-24 + 23a MANDATORY GATE, GO/NO-GO decision)
- Create `todo.md` and `questions.md`

**Stage 5b: Implementation Execution**

**🚨 FIRST ACTION:** Use the "Starting Stage 5b" prompt from `prompts_reference_v2.md`

- READ: `stages/stage_5/implementation_execution.md`
- Keep spec.md visible, continuous verification, mini-QC checkpoints, 100% test pass required

**Stage 5c: Post-Implementation** (4 phases - smoke testing, QC rounds, final review, commit)

**🚨 FIRST ACTION:** Use the "Starting Stage 5c Smoke Testing" prompt from `prompts_reference_v2.md`

- **Phase 1:** READ `stages/stage_5/smoke_testing.md` - Import/Entry Point/E2E tests (MANDATORY GATE)
  - If issues found → Enter debugging protocol → LOOP BACK to Stage 5ca Part 1
- **Phase 2:** READ `stages/stage_5/qc_rounds.md` - 3 QC rounds
  - If ANY issues → Enter debugging protocol → LOOP BACK to Stage 5ca Part 1 (NOT mid-QC)
- **Phase 3:** READ `stages/stage_5/final_review.md` - PR review, lessons learned, zero tech debt tolerance
- **Phase 4:** **COMMIT FEATURE** - Commit source code changes for this feature only (feature-level commits)

**Stage 5d: Cross-Feature Spec Alignment** (After feature completes)

**🚨 FIRST ACTION:** Use the "Starting Stage 5d" prompt from `prompts_reference_v2.md`

- READ: `stages/stage_5/post_feature_alignment.md`
- Update remaining feature specs based on completed feature implementation

**Stage 5e: Epic Testing Plan Reassessment** (After Stage 5d)

**🚨 FIRST ACTION:** Use the "Starting Stage 5e" prompt from `prompts_reference_v2.md`

- READ: `stages/stage_5/post_feature_testing_update.md`
- Reassess epic_smoke_test_plan.md after each feature completion

**Repeat Stage 5 (5a→5b→5c→5d→5e) for EACH feature**

---

## Stage 6-7: Epic Finalization

**Stage 6: Epic-Level Final QC** (After ALL features complete)

**🚨 FIRST ACTION:** Use the "Starting Stage 6" prompt from `prompts_reference_v2.md`

- READ: `stages/stage_6/epic_final_qc.md`
- Execute epic_smoke_test_plan.md, 3 QC rounds, validate against epic request
- If issues found → Enter debugging protocol → LOOP BACK to Stage 6a (Epic Smoke Testing)

**Stage 7: Epic Cleanup** (After Stage 6 passes)

**🚨 FIRST ACTION:** Use the "Starting Stage 7" prompt from `prompts_reference_v2.md`

- READ: `stages/stage_7/epic_cleanup.md`
- Run unit tests (100% pass), user testing (MANDATORY GATE - ZERO bugs required)
- If user finds bugs → Add to epic debugging/ISSUES_CHECKLIST.md → Enter debugging protocol → LOOP BACK to Stage 6a
- Commit, merge to main, update EPIC_TRACKER.md, move to done/

---

## Missed Requirement Protocol

If missing scope/requirements discovered at ANY point after first Stage 5 starts (and you KNOW the solution):

**🚨 FIRST ACTION:** Use the "Creating Missed Requirement" prompt from `prompts_reference_v2.md`

- **READ:** `missed_requirement/missed_requirement_protocol.md`
- **When to use:** Missing scope discovered at ANY time (implementation, QA, debugging, epic testing, user testing), solution is KNOWN
- **Before Stage 5:** Just update specs directly during Stage 2/3/4
- **Two options:** Create new `feature_{XX}_{name}/` folder OR update unstarted feature
- **User decides:** Which approach + priority (high/medium/low)
- **Pause current work** → Return to planning stages
- **Stage 2** (Deep Dive): Flesh out new/updated feature spec
- **Stage 3** (Sanity Check): Re-align ALL features (not just new one)
- **Stage 4** (Test Strategy): Update epic_smoke_test_plan.md
- **Resume paused work** → Implement new/updated feature when its turn comes in sequence
- **Full Stage 5** (5a → 5b → 5c → 5d → 5e) when feature gets implemented
- **Priority determines sequence:** high = before current, medium = after current, low = at end
- **Special case:** If discovered during Stage 6/7 → Complete all features → **RESTART epic testing from Stage 6a**

---

## Debugging Protocol

**INTEGRATED WITH QC/SMOKE TESTING** - When issues discovered with UNKNOWN root cause:

**🚨 FIRST ACTION:** Use the "Starting Debugging Protocol" prompt from `prompts_reference_v2.md`

- **READ:** `debugging/debugging_protocol.md`
- **When to use:** Issues discovered during QC/Smoke testing with unknown root cause requiring investigation

**File Structure:**
- Feature-level issues: `feature_XX_{name}/debugging/` folder
- Epic-level issues: `KAI-{N}-{epic_name}/debugging/` folder
- Contains: ISSUES_CHECKLIST.md, issue_XX_{name}.md files, investigation_rounds.md, code_changes.md, process_failure_analysis.md (NEW), guide_update_recommendations.md (NEW), lessons_learned.md

**Workflow Integration:**
1. **Issue Discovery** - During Smoke Testing (Stage 5ca/6a) or QC Rounds (Stage 5cb/6b), add issues to ISSUES_CHECKLIST.md
2. **Enter Debugging Protocol** - Work through checklist systematically
3. **Systematic Root Cause Analysis (NEW)** - After ALL issues resolved, analyze why bugs got through process and generate guide updates
4. **Loop Back to Testing** - RESTART testing from beginning (not mid-testing)
5. **Zero Issues Required** - Cannot proceed to next stage with any open issues

**5-Phase Process:**
- Phase 1: Issue Discovery & Checklist Update
- Phase 2: Investigation (Round 1 → Code Tracing, Round 2 → Hypothesis, Round 3 → Testing)
- Phase 3: Solution Design & Implementation
- Phase 4: User Verification (MANDATORY - user must confirm each fix)
- Phase 5: Loop Back to Testing (includes systematic root cause analysis)

**Key Requirements:**
- **Issue-centric tracking:** Each issue has dedicated file with investigation history
- **Max 5 investigation rounds** per issue before user escalation
- **Feature vs Epic separation:** Feature bugs vs epic integration bugs tracked separately
- **User testing integration:** Stage 7 user-reported bugs → epic checklist → loop back to Stage 6 (NOT Stage 7)
- **Resumability:** investigation_rounds.md preserves state across session compaction

---

## Key Principles

- **Epic-first thinking**: Top-level work unit is an epic (collection of features)
- **Mandatory reading protocol**: ALWAYS read guide before starting stage
- **Phase transition prompts**: MANDATORY acknowledgment (proves guide was read)
- **Continuous alignment**: Stage 5d updates specs after each feature
- **Iterative testing**: Test plan evolves (Stage 1 → 4 → 5e → 6)
- **Epic vs feature distinction**: Feature testing (5c) vs epic testing (6) are different
- **24 verification iterations**: All mandatory (across 3 rounds in Stage 5a)
- **QC restart protocol**: If ANY issues → restart completely
- **No skipping stages**: All stages have dependencies, must complete in order
- **100% test pass**: Required before commits and stage transitions
- **Zero tech debt tolerance**: Fix ALL issues immediately (no deferrals)

See `feature-updates/guides_v2/README.md` for complete workflow overview and guide index.

---

## Resuming In-Progress Epic Work

**BEFORE starting any epic-related work**, check for in-progress epics:

1. **Check for active epic folders:** Look in `feature-updates/` for any folders (excluding `done/` and `guides_v2/`)

2. **If found, use the "Resuming In-Progress Epic" prompt** from `feature-updates/guides_v2/prompts_reference_v2.md`

3. **READ THE EPIC_README.md FIRST:** Check the "Agent Status" section at the top with:
   - Current stage and guide
   - Current step/iteration
   - Next action to take
   - Critical rules from current guide

4. **READ THE CURRENT GUIDE:** Use Read tool to load the guide listed in Agent Status

5. **Continue from where previous agent left off** - Don't restart the workflow

**Why this matters:** Session compaction can interrupt agents mid-workflow. EPIC_README.md Agent Status survives context window limits and provides exact resumption point.

---

## Workflow Guides Location

**All guides:** `feature-updates/guides_v2/`

**Directory Structure:**
- `stages/` - Core workflow guides (stage_1 through stage_7)
- `reference/` - Reference cards and supporting materials
- `templates/` - File templates for epics, features, bug fixes
- `_internal/` - Internal tracking and completion documents

**Key Files:**
- README.md - Workflow overview and guide index
- prompts_reference_v2.md - MANDATORY phase transition prompts
- EPIC_WORKFLOW_USAGE.md - Comprehensive usage guide

---

## Git Branching Workflow

**All epic work must be done on feature branches** (not directly on main).

### Branch Management

**When starting an epic (Stage 1):**

1. **Verify you're on main:**
   ```bash
   git checkout main
   ```

2. **Pull latest changes:**
   ```bash
   git pull origin main
   ```

3. **Assign KAI number:**
   - Check `feature-updates/EPIC_TRACKER.md` for next available number
   - Update EPIC_TRACKER.md with new epic in "Active Epics" table

4. **Determine work type:**
   - `epic` - Work with multiple features (most epics)
   - `feat` - Work with single feature only
   - `fix` - Bug fix work

5. **Create and checkout branch:**
   ```bash
   git checkout -b {work_type}/KAI-{number}
   ```

**During epic work (Stages 1-6):**
- All work happens on the epic branch
- Commits use format: `{commit_type}/KAI-{number}: {message}`
  - `commit_type` is either `feat` or `fix` (NOT `epic`)
  - `feat` - Feature-related commits
  - `fix` - Bug fix commits
- Commit at normal times (currently Stage 7 Step 6)

**When completing an epic (Stage 7):**

1. **Commit changes on branch** (after user testing passes)

2. **Merge to main:**
   ```bash
   git checkout main
   git pull origin main
   git merge {work_type}/KAI-{number}
   ```

3. **Push to origin:**
   ```bash
   git push origin main
   ```

4. **Update EPIC_TRACKER.md:**
   - Move epic from "Active" to "Completed" table
   - Add epic detail section with commits
   - Increment "Next Available Number"

5. **Delete branch (optional):**
   ```bash
   git branch -d {work_type}/KAI-{number}
   ```

### Branch Naming Convention

**Format:** `{work_type}/KAI-{number}` (epic/feat/fix tracked in EPIC_TRACKER.md)
**Examples:** `epic/KAI-1`, `feat/KAI-2`, `fix/KAI-3`

### Epic Folder Naming Convention

**Format:** `feature-updates/KAI-{N}-{epic_name}/`
**Examples:**
- `feature-updates/KAI-1-improve_draft_helper/`
- `feature-updates/KAI-3-integrate_new_player_data_into_simulation/`

**Original Request File:** `feature-updates/{epic_name}.txt` (no KAI number)
**Why include KAI number:** Ensures unique folder names, matches branch naming, enables quick identification

### Commit Message Convention

**Format:** `{commit_type}/KAI-{number}: {message}` (feat or fix)
**Example:** `feat/KAI-1: Add ADP integration to PlayerManager`
**Rules:** Brief (100 chars), no emojis, imperative mood, all features in epic use same KAI number

### EPIC_TRACKER.md Management

**Location:** `feature-updates/EPIC_TRACKER.md`
**Updates:** Stage 1 (add to Active table), Stage 7 (move to Completed, add details), after commits (track for docs)

---

## Pre-Commit Protocol

**MANDATORY BEFORE EVERY COMMIT**

**When the user requests to commit changes:**

### STEP 1: Run Unit Tests (REQUIRED)

**PROJECT-SPECIFIC: Update this command for your project**
```bash
python tests/run_all_tests.py
```

**Test Requirements:**
- All unit tests must pass (100% pass rate)
- Exit code 0 = safe to commit, 1 = DO NOT COMMIT
- **Only proceed to commit if all tests pass**

### STEP 2: If Tests Pass, Review ALL Changes

**⚠️ CRITICAL: Include ALL modified source code files**
```bash
git status  # Check ALL modified files
git diff    # Review changes
```

**Common mistake:** Missing test files that were updated to use new interfaces

**Verify all source files are included:**
- [ ] Main source files (*.py in league_helper/, simulation/, etc.)
- [ ] ALL test files that were modified (tests/**/*.py)
- [ ] Configuration files if modified (data/*.json, data/*.csv)

### STEP 3: Stage and Commit Changes

1. Analyze all changes with `git status` and `git diff`
2. **Verify ALL modified source files are included** (main code AND test files)
3. Update documentation if functionality changed
4. Stage and commit with clear, concise message
5. Follow commit standards:
   - Format: `{commit_type}/KAI-{number}: {message}`
   - Brief, descriptive messages (100 chars or less)
   - No emojis or subjective prefixes
   - commit_type is `feat` or `fix`
   - List major changes in body

### STEP 4: If Tests Fail

- **STOP** - Do NOT commit
- Fix failing tests (including pre-existing failures from other epics)
- Re-run tests
- Only commit when all tests pass (exit code 0)

**Note:** It is acceptable to fix pre-existing test failures during Stage 7 to achieve 100% pass rate.

**Do NOT skip validation**: 100% test pass rate is mandatory

---

## Critical Rules Summary

### Always Required

✅ **Read guide before starting stage** (use Read tool for ENTIRE guide)
✅ **Use phase transition prompts** from `prompts_reference_v2.md`
✅ **Verify prerequisites** before proceeding
✅ **Update Agent Status** in README files at checkpoints
✅ **100% unit test pass rate** before commits and stage transitions
✅ **Fix ALL issues immediately** (zero tech debt tolerance)
✅ **User testing approval** before final commit (Stage 7)

### Never Allowed

❌ **Skip stages** (all stages have dependencies)
❌ **Skip iterations** in Stage 5a (all 24 mandatory)
❌ **Defer issues for "later"** (fix immediately)
❌ **Skip QC restart** when issues found
❌ **Commit without running tests**
❌ **Commit without user testing approval** (Stage 7)

### Quality Gates

**🛑 MANDATORY GATES (cannot proceed without passing):**
- Iteration 4a: TODO Specification Audit (Stage 5a Round 1)
- Iteration 23a: Pre-Implementation Spec Audit (Stage 5a Round 3)
- Smoke Testing: Part 3 must pass before QC rounds (Stage 5c)
- User Testing: Must pass before commit (Stage 7)

---

## Additional Resources

**Primary references:**
- **EPIC_WORKFLOW_USAGE.md**: Comprehensive usage guide with setup, patterns, FAQs
- **prompts_reference_v2.md**: All phase transition prompts (MANDATORY)
- **templates_v2.md**: File templates for epic, feature, and bug fix folders
- **README.md**: Guide index and quick reference
- **PLAN.md**: Complete workflow specification

---

**Remember:** This workflow exists to ensure quality, completeness, and maintainability. Follow it rigorously, learn from each epic, and continuously improve the guides based on lessons learned.

## Current Project Structure

**Core Scripts:** `run_league_helper.py`, `run_simulation.py`, `run_player_fetcher.py`, `run_scores_fetcher.py`

**Main Modules:**
- `league_helper/` - 4 interactive modes (draft, optimizer, trade, data editor) + utilities
- `simulation/` - Parameter optimization through league simulation
- `player-data-fetcher/` - API data collection
- `nfl-scores-fetcher/` - NFL scores and team rankings
- `utils/` - Shared utilities (logging, error handling, CSV I/O)
- `tests/` - 2,200+ tests (100% pass rate required)
- `data/` - League config, player stats, team rankings
- `docs/scoring/` - 10-step scoring algorithm documentation
- `feature-updates/` - Epic-driven development (see CLAUDE_EPICS.md)

**See:** `ARCHITECTURE.md` for complete architectural details, `README.md` for installation/usage.

---

## Coding Standards & Conventions

### Import Organization
```python
# Standard library (alphabetical)
import csv, json
from pathlib import Path
from typing import Dict, List, Optional, Any

# Third-party (alphabetical)
import pandas as pd

# Local with sys.path manipulation
import sys
sys.path.append(str(Path(__file__).parent.parent))
from utils.LoggingManager import get_logger
```

**Rules:** Use `Path` for file operations, `sys.path.append()` for relative imports, type hints required

### Error Handling
```python
from utils.error_handler import error_context, DataProcessingError

# Use context managers for error tracking
with error_context("operation_name", component="module_name") as ctx:
    if error_condition:
        raise DataProcessingError("Error message", context=ctx)
```

### Logging Standards
```python
from utils.LoggingManager import setup_logger, get_logger

logger = setup_logger(name="module", level="INFO")  # Setup once
logger = get_logger()  # Use in modules

# Levels: debug, info, warning, error (with exc_info=True)
```

### Docstring Format (Google Style)
```python
def method_name(self, param1: Type, param2: Optional[Type] = None) -> ReturnType:
    """Brief one-line description.

    Args:
        param1 (Type): Description
        param2 (Optional[Type]): Description with default

    Returns:
        ReturnType: Description of return value
    """
```

### Type Hinting
```python
from typing import Dict, List, Optional, Union
from pathlib import Path

def process_data(filepath: Union[str, Path],
                 options: Optional[Dict[str, Any]] = None) -> Tuple[bool, str]:
    pass
```

### CSV Operations
```python
from utils.csv_utils import read_csv_with_validation, write_csv_with_backup

df = read_csv_with_validation(filepath, required_columns=['id', 'name'])
write_csv_with_backup(df, filepath, create_backup=True)
```

### Configuration Access
```python
from util.ConfigManager import ConfigManager

config = ConfigManager(data_folder)
multiplier, rating = config.get_adp_multiplier(adp_val)
```

### Naming Conventions
- **Classes**: `PascalCase` (PlayerManager, ConfigManager)
- **Functions/Methods**: `snake_case` (load_players, get_score)
- **Constants**: `UPPER_SNAKE_CASE` (RECOMMENDATION_COUNT, LOGGING_LEVEL)
- **Private**: `_leading_underscore` (_validate_config)
- **Modules**: `snake_case` (error_handler.py, csv_utils.py)

### Path Handling
```python
from pathlib import Path

base_path = Path(__file__).parent
config_file = base_path / "data" / "league_config.json"
with open(str(config_file), 'r') as f:  # Convert to string when needed
    pass
```

### Testing Standards

**Test Suite:** 2,200+ tests (100% pass rate required before commits)
- **Unit Tests:** Test individual functions/classes in isolation, mock dependencies
- **Integration Tests:** Test cross-module workflows (25 tests)

**Test Execution:**
```bash
# Run all tests (REQUIRED before commits)
python tests/run_all_tests.py

# Run specific file/class
python -m pytest tests/path/test_file.py::TestClass -v
```

**Requirements:**
- Test file structure mirrors source code
- Use pytest fixtures for reusable test data
- Mock external dependencies (files, APIs, datetime)
- AAA pattern (Arrange, Act, Assert)
- Tests must be independent (no shared state)

**See:** `tests/README.md` for complete testing guidelines and examples.
