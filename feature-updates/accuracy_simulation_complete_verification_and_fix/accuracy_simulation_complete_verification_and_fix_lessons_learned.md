# Accuracy Simulation Complete Verification and Fix - Lessons Learned

> **Purpose:** This file captures issues discovered during development that indicate gaps in the planning or development guides. These lessons are used to improve the guides for future features.

---

## Issues Discovered During Planning

### Issue 1: Agent Prematurely Marked Checklist Items as Resolved

**What happened:**
During Phase 2 (Deep Investigation), the agent performed codebase verification and marked 13 checklist items as `[x]` resolved without user review. The agent should have only provided research findings and recommendations, leaving all items as `[ ]` until the user explicitly reviews and approves the findings.

**Impact:**
- User had to request re-review of all "resolved" items
- Created false impression that 30% of questions were already answered
- Required rework to mark items as "NEEDS REVIEW"

**Root cause:**
The feature_planning_guide.md doesn't explicitly state that agents should NOT mark items as complete during codebase verification - only that they should "populate the checklist with findings."

**Proposed guide update:**
Add explicit instruction to feature_planning_guide.md Phase 2 (CODEBASE VERIFICATION):

```markdown
**CRITICAL: DO NOT mark any checklist items as [x] during codebase verification.**

Your role is to:
- Research the codebase
- Document findings in the Resolution Log
- Provide recommendations
- Leave ALL items as [ ] for user review

Only the USER can mark items as [x] after reviewing your findings.
```

**Lesson learned:**
Agents should treat codebase verification as research/recommendation phase, not decision-making phase. All checklist items remain `[ ]` until user explicitly approves the findings during Phase 4 iterative resolution.

---

### Issue 2: Specs File Not Updated Incrementally During Phase 4

**What happened:**
During Phase 4 (Iterative Resolution), the agent resolved all 44 checklist questions with the user but failed to update the specs file incrementally as each question was answered. The specs file retained the original "Open Questions for User" section and outdated "Implementation Strategy" until the user explicitly asked if the specs were updated. This required a bulk update at the end to add all resolved decisions.

**Impact:**
- Specs file became out of sync with checklist progress
- "Open Questions" section remained unchanged despite all questions being resolved
- If session had been interrupted, the next agent would have incomplete specs
- Required retrospective bulk update instead of incremental updates

**Root cause:**
The feature_planning_guide.md Phase 4 instructions say "Update _specs.md with the resolved detail" but don't emphasize doing this IMMEDIATELY after each resolution. The agent interpreted this as "update specs eventually" rather than "update specs now before moving to next question."

**Proposed guide update:**
Strengthen the Phase 4 instruction in feature_planning_guide.md (around line 740-757):

```markdown
### When user provides an answer

1. **Acknowledge** the answer
2. **IMMEDIATELY update both files:**
   - **Update `_specs.md`** with the resolved detail in the appropriate section
   - **Mark checklist item `[x]`** in `_checklist.md` with resolution summary
3. **Update `README.md`** if the answer affects scope or key context

**CRITICAL:** Update BOTH files after EACH answer, not at end of session.
- Specs should never contain "Open Questions" that have been resolved
- If a question in specs is answered, move it from "Open Questions" to "Resolved Implementation Decisions"
- This ensures continuity if session is interrupted

**Anti-pattern:** Updating only checklist during Phase 4, leaving specs outdated
```

**Why this matters:**
The specs file is the PRIMARY implementation reference (per feature_development_guide.md: "Read `{feature_name}_specs.md` as the primary specification"). If it contains outdated "Open Questions" sections or missing resolved decisions, the implementation phase starts with incomplete information.

**Lesson learned:**
During Phase 4 question resolution, agents must update BOTH the checklist AND specs files after each answer. The checklist tracks what's resolved vs pending, but the specs file must contain the full implementation details for each resolved item. These updates should happen immediately, not batched at end of session.

---

## Issues Discovered During Development

### Issue 3: Sub-Feature Breakdown Should Be Standard Practice

**What happened:**
During the development phase preparation, the user requested breaking the large feature into 5 separate TODO files (one per sub-feature/phase) instead of creating a single monolithic TODO file. This was done as a user-initiated adjustment rather than being the default approach from the feature_development_guide.md.

**Why this was better:**
- Each TODO file covers a focused, cohesive sub-feature (Core Fixes, Tournament Rewrite, Parallel Processing, CLI & Logging, Testing & Validation)
- Each sub-feature can complete all 24 verification iterations independently
- Clear dependencies between sub-features (Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5)
- Easier to track progress within each phase
- Allows for incremental completion and validation
- Reduces cognitive load - agent focuses on one sub-feature at a time
- Natural breakpoints for QA checkpoints between phases
- More manageable scope per TODO file (3-6 tasks vs 20+ tasks)

**Impact of not having this as default:**
- Agent initially assumed single TODO file approach
- Required user intervention to suggest sub-feature breakdown
- If user hadn't suggested it, would have created unwieldy monolithic TODO
- Missed opportunity to apply this pattern from the start

**Root cause:**
The feature_development_guide.md doesn't provide guidance on when or how to break features into sub-features. It assumes a single TODO file per feature, regardless of feature size or complexity.

**Proposed guide update:**
Add new section to feature_development_guide.md before "Step 1: Create TODO file":

```markdown
## Step 0: Sub-Feature Analysis (MANDATORY for complex features)

**BEFORE creating TODO files**, analyze whether the feature should be broken into sub-features.

### When to Break Into Sub-Features

Break features into sub-features if ANY of these apply:
- Feature has 10+ distinct implementation tasks
- Feature spans multiple systems or components
- Feature has clear phases (e.g., core logic → optimization → testing)
- Feature has natural dependencies (Task A must complete before Task B)
- Feature would take multiple days/weeks to implement
- Feature scope is "comprehensive fix" or "complete rewrite"

### How to Identify Sub-Features

Look for natural groupings:
1. **By component**: Each major class/module is a sub-feature
2. **By phase**: Setup → Implementation → Optimization → Testing
3. **By dependency**: Core fixes → New features → Performance → Validation
4. **By priority**: Critical path → Nice-to-have → Polish

### Sub-Feature Structure

Each sub-feature gets its own TODO file:
- `01_[name]_todo.md` - Phase 1 (highest priority/dependency)
- `02_[name]_todo.md` - Phase 2 (depends on Phase 1)
- `03_[name]_todo.md` - Phase 3 (depends on Phase 2)
- etc.

**Each TODO file follows the full 24-iteration structure** independently.

### Example: Large Feature Breakdown

**Bad (monolithic):**
- `accuracy_simulation_complete_fix_todo.md` with 20+ tasks

**Good (sub-features):**
- `01_core_fixes_todo.md` (3 tasks - prerequisite fixes)
- `02_tournament_rewrite_todo.md` (5 tasks - core feature)
- `03_parallel_processing_todo.md` (4 tasks - performance)
- `04_cli_logging_todo.md` (3 tasks - observability)
- `05_testing_validation_todo.md` (6 tasks - QA)

Each sub-feature:
- Completes all 24 verification iterations
- Has QA checkpoint
- Can be validated independently
- Builds on previous sub-features
```

**Lesson learned:**
For complex features, ALWAYS start by identifying sub-features and creating separate TODO files for each. Each sub-feature should be cohesive, focused, and follow the full 24-iteration verification process. This should be the DEFAULT approach for any feature with 10+ tasks, not an optional optimization.

**Action needed:**
Update feature_development_guide.md to make sub-feature analysis a mandatory first step (Step 0) before creating TODO files.

---

### Issue 5: Sub-Features Should Complete Full Feature Workflow

**What happened:**
During Phase 1 (Core Fixes) implementation, the user clarified that sub-features should be treated like full independent features - going through all POST-IMPLEMENTATION phases (QC rounds, requirement verification, lessons learned review) and committing after each sub-feature completes. Only the "move to done/" step should be skipped until all sub-features are complete.

**Why this matters:**
- Each sub-feature represents a complete, testable unit of work
- Committing after each sub-feature provides:
  - Incremental progress tracking in git history
  - Safe rollback points if later sub-features have issues
  - Clear attribution of which changes belong to which sub-feature
  - Ability to pause/resume between sub-features without losing work
- Full QC process per sub-feature catches bugs early (e.g., Phase 1 QC Round 3 found logic ordering bug)
- Requirement verification ensures each sub-feature is complete before moving to next

**Current gap in guides:**
The sub-feature breakdown guidance (Issue 3) doesn't explicitly state that each sub-feature should complete the full feature workflow. Without this clarity, agents might skip POST-IMPLEMENTATION steps for sub-features, treating them as "just tasks" rather than complete features.

**Proposed guide update:**
Add to the sub-feature section in feature_development_guide.md:

```markdown
## Sub-Feature Workflow

**CRITICAL: Each sub-feature follows the COMPLETE feature workflow:**

1. **Pre-implementation:**
   - Create TODO file with 24 verification iterations
   - Complete all 3 verification rounds (7+9+8 iterations)
   - Interface verification

2. **Implementation:**
   - Execute all tasks in TODO
   - Update code_changes.md incrementally
   - Run tests after each phase

3. **Post-implementation:**
   - Run all unit tests (100% pass required)
   - Execute Requirement Verification Protocol
   - Complete 3 QC rounds
   - Review lessons learned
   - **Commit changes** with descriptive message

4. **What to skip:**
   - Do NOT move folder to done/ (wait until all sub-features complete)
   - All other steps are MANDATORY

**Sub-feature commit message format:**
```bash
git commit -m "Phase N ({sub-feature-name}): {brief description}

- Change 1
- Change 2
- Change 3"
```

**Example:**
```
Phase 1 (Core Fixes): Fix is_better_than() and ROS saving

- Fix is_better_than() to reject player_count=0 configs
- Fix ROS intermediate saving to save once per parameter
- Create test fixtures for unit/integration tests
- Add 3 unit tests for edge cases
```

This ensures:
- Each sub-feature is fully validated before proceeding
- Git history shows incremental progress
- Bugs caught early (within sub-feature scope)
- Safe rollback points between sub-features
```

**Impact of not following this:**
- Missing QC rounds = bugs slip through (Phase 1 QC Round 3 caught critical logic bug)
- No commits = losing work if session interrupted
- No requirement verification = incomplete sub-features
- Treating sub-features as "tasks" instead of "features"

**Lesson learned:**
Sub-features ARE features - just with dependencies and grouped scope. Each sub-feature should complete the full feature development workflow (all verification iterations + all POST-IMPLEMENTATION steps + commit), with only the "move to done/" step deferred until the parent feature is complete.

**Action needed:**
Update feature_development_guide.md Step 0 (Sub-Feature Analysis) to explicitly state that each sub-feature completes the full workflow and gets committed independently.

---

## Issues Discovered During QC

### Issue 4: Logic Ordering Bug in is_better_than() - QC Round 3

**What happened:**
During QC Round 3 skeptical review of Phase 1 (Core Fixes), discovered that is_better_than() checked `other is None` BEFORE checking `self.player_count == 0`. This logic ordering allowed an invalid config (player_count=0) to return True when compared to None, meaning it could become the first "best" config even though it's invalid.

**Impact:**
- Invalid configs could be saved as "best" if they were first to be evaluated
- Bug would have been subtle and hard to debug in production
- Would have corrupted optimization results silently

**How it was caught:**
QC Round 3 "Final Skeptical Review" protocol asks agents to trace through logic with fresh eyes. Specifically asked: "What if `other is None` AND `self.player_count == 0`?" This revealed the edge case.

**Root cause:**
- Initial implementation added player_count=0 check after the `other is None` check
- Didn't trace through all edge case combinations during initial implementation
- Unit tests written only covered standard cases, not the edge case of invalid config vs None

**Fix applied:**
Reordered checks to validate `self.player_count == 0` FIRST (before checking `other is None`):
```python
# BEFORE (BUG):
if other is None:
    return True  # Returns True even if self.player_count == 0!
if self.player_count == 0 or other.player_count == 0:
    return False

# AFTER (FIXED):
if self.player_count == 0:
    return False  # Check invalid state FIRST
if other is None:
    return True  # Now safe - we know self is valid
if other.player_count == 0:
    return False
```

**New test added:**
`test_is_better_than_zero_vs_none()` - Verifies invalid config doesn't beat None

**Why QC caught this but verification didn't:**
- Verification iterations focus on "does code match spec"
- QC rounds focus on "what edge cases could break this"
- QC Round 3 specifically asks "trace through with fresh eyes"
- Skeptical questioning revealed the gap

**Proposed guide update:**
None needed - existing QC Round 3 protocol worked correctly. The issue proves why QC rounds are mandatory even after 24 verification iterations.

**Lesson learned:**
- Logic ordering matters when dealing with multiple validation states
- Always check invalid/error states BEFORE checking for missing values (None)
- QC Round 3 "fresh eyes" review is not optional - it catches bugs that verification misses
- Edge case testing should consider combinations: invalid vs None, invalid vs valid, invalid vs invalid

**Impact on guides:**
This validates the existing 3 QC round requirement. Without QC Round 3, this bug would have been committed.

---

## Proposed Guide Updates

*(To be populated based on lessons learned)*
