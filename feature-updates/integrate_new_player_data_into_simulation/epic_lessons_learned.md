# Epic: integrate_new_player_data_into_simulation - Lessons Learned

**Purpose:** Document cross-feature patterns and systemic insights from this epic

---

## Planning Phase Lessons (Stages 1-4)

### Stage 1: Epic Planning

**Lessons from Phase 2 Analysis:**
- JSON migration happened very recently (2025-12-30), only 3 days old at epic start
- Partial implementation already exists but user flagged as "buggy and incomplete"
- Need to verify all existing work rather than assume it's correct
- SimulatedLeague already has _parse_players_json(), AccuracySimulationManager already copies JSON files
- Week 17 fix already implemented in code (week_num_for_actual parameter)

**Key Decision:** Framed as verification/cleanup epic rather than greenfield implementation

{More lessons will be added as Stages 2-4 progress}

---

## Implementation Phase Lessons (Stage 5)

{Will be populated during Stage 5 as features are implemented}

---

## QC Phase Lessons (Stage 6)

### Bug Fix Protocol: Reset to Stage 6 After Fixes

**Lesson:** When bugs are discovered during Stage 6 (Epic Final QC) or Stage 7 (User Testing), after ALL bug fixes are complete, you MUST restart from the beginning of Stage 6.

**Why this is critical:**
- Bug fixes change the codebase
- Changes may introduce new integration issues
- Changes may affect cross-feature interactions
- Stage 6 validates the ENTIRE epic as a whole
- Cannot assume partial Stage 6 results are still valid

**Correct Protocol:**
1. Bugs discovered during Stage 6 or Stage 7 user testing
2. Create bug fix(es) using bug fix workflow (Stage 2 → 5a → 5b → 5c)
3. After ALL bug fixes complete (all reach Stage 5c)
4. **RESTART Stage 6 completely from the beginning:**
   - Re-run epic smoke testing (all 4 parts)
   - Re-run epic QC rounds (all 3 rounds)
   - Re-run epic PR review (all 11 categories)
   - Validate against original epic request
5. If Stage 6 finds MORE bugs → repeat cycle
6. Only proceed to Stage 7 when Stage 6 passes with ZERO issues

**Wrong Approach (DO NOT DO THIS):**
- ❌ "Bug fix was small, let's just continue Stage 6 from where we left off"
- ❌ "Only re-test the parts affected by the bug fix"
- ❌ "Skip epic smoke testing, just re-run QC rounds"
- ❌ "Bug fix passed its own tests, that's good enough"

**Applied in this epic:**
- Discovered 4 bugs during Stage 7 user testing (unicode error, missing single mode, max projection 0.0, zero variance)
- Created 4 separate bug fixes: bugfix_high_unicode_error, bugfix_medium_restore_single_mode, bugfix_medium_max_projection_zero, bugfix_medium_zero_variance
- After ALL 4 bug fixes complete → Will RESTART Stage 6 from beginning
- This ensures full epic integration is validated with all fixes applied

**Documentation references:**
- Stage 7 guide: stages/stage_7/epic_cleanup.md (Step 5: Bug Fix Protocol)
- Bug fix guide: stages/stage_5/bugfix_workflow.md
- Both guides clearly state: After bug fixes → RESTART Stage 6

{More Stage 6 lessons will be added as Stage 6 executes}

---

## Guide Improvements Identified

{Track guide gaps/improvements discovered during this epic}

| Guide File | Issue | Proposed Fix | Status |
|------------|-------|--------------|--------|
| (none yet) | (will track as issues discovered) | (proposed solutions) | Pending/Done |

---

## Cross-Feature Patterns

{Will be populated as patterns emerge across features}

**Common patterns identified:**
- TBD

**Anti-patterns to avoid:**
- TBD

---

## Epic-Specific Insights

**What made this epic unique:**
- Verification/cleanup of partial work instead of new implementation
- Two different simulation architectures (Win Rate: direct parsing, Accuracy: via PlayerManager)
- Recent transition period (CSV just deprecated 3 days before epic start)

**What we'd do differently:**
- TBD (will populate during/after epic)
