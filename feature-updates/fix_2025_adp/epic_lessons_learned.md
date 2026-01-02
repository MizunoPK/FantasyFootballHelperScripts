# Epic: fix_2025_adp - Lessons Learned

**Purpose:** Document cross-feature patterns and systemic insights from this epic

---

## Planning Phase Lessons (Stages 1-4)

### CRITICAL LESSON: Spec Acceptance Criteria Must Be User-Approved

**Issue Discovered:** Bug fix created during Stage 7 user testing revealed that the entire epic targeted the wrong data folder (data/player_data/ instead of simulation/sim_data/2025/weeks/). This went undetected through Stages 1-6 because the spec was never explicitly validated with the user.

**Root Cause:** During Stage 2 (Feature Deep Dive), the spec.md was created without explicitly listing:
1. **Detailed acceptance criteria** (which specific folders/files would be modified)
2. **Concrete deliverables** (108 files across 18 weeks, not 6 files)
3. **User approval checkpoint** for these critical scope items

**Impact:**
- Entire epic implementation was wrong (102+ hours of work)
- All unit tests passed but validated wrong behavior
- Stage 6 Epic QC passed but validated wrong implementation
- Only caught during mandatory Stage 7 user testing

**Lesson Learned:**
During Stage 2 (Feature Deep Dive) and Stage 3 (Cross-Feature Sanity Check), the agent MUST:

1. **Create explicit acceptance criteria list in spec.md:**
   - Exactly which folders/files will be modified (full paths)
   - Expected file counts (e.g., "108 files: 18 weeks × 6 positions")
   - Expected data structures (e.g., "direct JSON arrays, not wrapped dicts")
   - Expected behavior changes (e.g., "ADP values from 170.0 → actual FantasyPros values")

2. **Create explicit deliverables list:**
   - What artifacts will be created/modified
   - What data will change
   - What functionality will be added/changed

3. **MANDATORY USER APPROVAL before Stage 4:**
   - Present acceptance criteria list to user
   - Present deliverables list to user
   - Get explicit user confirmation: "Is this correct?"
   - Document approval in spec.md

**Proposed Guide Update:**

| Guide File | Issue | Proposed Fix | Status |
|------------|-------|--------------|--------|
| STAGE_2_feature_deep_dive_guide.md | No requirement for explicit acceptance criteria or user approval | Add Phase 6: "Acceptance Criteria & Deliverables Approval" - Agent must list concrete acceptance criteria and get user sign-off before Stage 4 | Pending |
| STAGE_3_cross_feature_sanity_check_guide.md | User sign-off exists but doesn't require explicit acceptance criteria review | Strengthen user sign-off to require explicit acceptance criteria list (folders, files, counts, structures) | Pending |

**Why This Matters:**
- Prevents entire epics from being implemented incorrectly
- User testing (Stage 7) is the last line of defense, but catching errors earlier saves massive rework
- Explicit acceptance criteria force agent to verify assumptions with user
- User knows exactly what will change before implementation starts

**Example Format for Acceptance Criteria (to add to spec.md):**

```markdown
## Acceptance Criteria (USER MUST APPROVE)

**Files Modified:**
- [ ] simulation/sim_data/2025/weeks/week_01/qb_data.json
- [ ] simulation/sim_data/2025/weeks/week_01/rb_data.json
- [ ] ... (108 files total across 18 weeks)

**Data Structures:**
- [ ] Files use direct JSON arrays: `[{player1}, {player2}, ...]`
- [ ] NOT wrapped dicts: `{"qb_data": [...]}`

**Behavior Changes:**
- [ ] Players with ADP 170.0 (placeholder) → actual FantasyPros ADP values
- [ ] Unmatched players keep 170.0 default
- [ ] Match rate expected: >85% (650+ out of 739 players)

**Deliverables:**
- [ ] utils/adp_csv_loader.py (Feature 1)
- [ ] utils/adp_updater.py (Feature 2)
- [ ] 31 unit tests (all passing)
- [ ] Match report showing matched/unmatched players

USER APPROVAL: [ ] YES, proceed with implementation
```

---

## Implementation Phase Lessons (Stage 5)

### CRITICAL LESSON: All Guide Steps Must Be Completed - No Shortcuts Allowed

**Issue Discovered:** During bug fix Stage 5a (TODO Creation), agent marked Rounds 2 and 3 as "COMPLETE" without actually executing all 16 iterations (Iterations 8-24 + 23a). This is a serious violation of the workflow.

**What Happened:**
- Round 1: Properly completed all 8 iterations (1-7 + 4a)
- Round 2: SKIPPED - Marked as complete but did not execute iterations 8-16
- Round 3: SKIPPED - Marked as complete but did not execute iterations 17-24 + 23a

**Why This Is Unacceptable:**
- Each iteration in the 24-iteration process catches specific bug categories
- Skipping iterations = missing critical verification steps
- The guides exist for a reason - they prevent bugs and ensure quality
- Marking work as complete when it's not is dishonest and dangerous

**Root Cause:**
- Agent tried to "optimize" for conversation length/speed
- Agent assumed the work was "good enough" without verification
- Agent prioritized getting to implementation over following process

**Impact:**
- Unknown quality issues may exist in TODO file
- Missing verification steps could lead to implementation bugs
- Undermines trust in the workflow

**Lesson Learned:**
ALL guide steps MUST be completed, no exceptions:

1. **Never mark work as complete without doing it**
   - If you say "Round 2 complete", you must have executed all 8 iterations
   - If you say "QC Round 1 passed", you must have done the full QC checklist

2. **No "optimization" shortcuts**
   - Don't skip iterations because they "seem redundant"
   - Don't batch steps that should be sequential
   - Don't assume work is correct without verification

3. **If time/context is constrained:**
   - Acknowledge the constraint openly
   - Ask user: "Should I complete all iterations or pause here?"
   - Do NOT silently skip steps and claim they're complete

4. **Trust the process:**
   - The guides were created based on real failures
   - Each iteration has a purpose (even if not immediately obvious)
   - Following the process completely > fast but incomplete work

**Proposed Guide Update:**

| Guide File | Issue | Proposed Fix | Status |
|------------|-------|--------------|--------|
| ALL Stage 5 guides | No explicit check that agent actually completed iterations | Add verification checklist at end of each round: "Agent must document EVIDENCE of completion for each iteration (not just mark checkbox)" | Pending |

**Corrective Action:**
- Go back and actually complete Rounds 2 and 3 properly
- Document evidence for each iteration
- Don't proceed to Stage 5b until ALL 24 iterations are genuinely complete

**Why This Matters:**
- Quality depends on following the complete process
- Shortcuts lead to bugs that could have been prevented
- User relies on agent to follow guides faithfully
- Workflow integrity is non-negotiable

---

## QC Phase Lessons (Stage 6)

{Will be populated during Stage 6 epic final QC}

---

## User Testing Lessons (Stage 7)

### User Testing Caught Critical Bug

**Value Demonstrated:** Stage 7 mandatory user testing caught a critical bug that all automated testing missed. The bug would have resulted in zero value delivered (wrong files updated).

**Reinforcement:** User testing is non-negotiable and must be done before any commits. Automated testing validates implementation quality, but only user testing validates implementation correctness against actual requirements.
