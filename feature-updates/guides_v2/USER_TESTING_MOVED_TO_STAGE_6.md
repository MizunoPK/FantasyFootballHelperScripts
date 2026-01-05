# User Testing Moved from Stage 7 to Stage 6

**Date:** 2026-01-04
**Purpose:** Document the architectural change moving user testing from Stage 7 (Epic Cleanup) to Stage 6 (Epic Final QC)

---

## Summary of Change

**BEFORE:** User testing was Step 5 in Stage 7 (Epic Cleanup), after all epic QC was complete

**AFTER:** User testing is now Step 6 in Stage 6 (Epic Final QC), immediately after QC rounds and before PR review

---

## Rationale for Change

**User testing belongs in the QC phase, not the cleanup phase:**

1. **QC is about quality validation** - user testing validates epic quality
2. **Cleanup is about finalization** - documentation, commits, archival
3. **Earlier validation is better** - catch user-reported bugs earlier in the process
4. **Logical workflow** - test → validate → review → finalize makes more sense
5. **User approval gates PR review** - user validation should come before internal PR review

---

## New Stage 6 Workflow

**Stage 6 now has 9 steps across 4 guides:**

### STAGE_6a: Epic Smoke Testing (Steps 1-2)
- Step 1: Pre-QC Verification
- Step 2: Epic Smoke Testing (4 parts)

### STAGE_6b: Epic QC Rounds (Steps 3-5)
- Step 3: QC Round 1 - Cross-Feature Integration
- Step 4: QC Round 2 - Epic Cohesion & Consistency
- Step 5: QC Round 3 - End-to-End Success Criteria

### **STAGE_6c: User Testing (Step 6) ← NEW**
- **Step 6: User Testing & Bug Fix Protocol**
  - User tests epic with real data and workflows
  - If bugs found → fix → RESTART Stage 6a
  - If no bugs → proceed to STAGE_6d

### STAGE_6d: Epic Final Review (Steps 7-9) - Renumbered from 6-8
- Step 7: Epic PR Review (11 Categories) - was Step 6
- Step 8: Validate Against Epic Request - was Step 7
- Step 9: Final Verification & README Update - was Step 8

---

## New Stage 7 Workflow

**Stage 7 now has 7 steps (down from 8):**

- Step 1: Pre-Cleanup Verification
- Step 2: Run Unit Tests
- Step 2b: Investigate Anomalies (if applicable)
- Step 3: Documentation Verification
- Step 4: Update Guides (Apply Lessons)
- ~~Step 5: User Testing~~ ← **REMOVED** (moved to Stage 6)
- Step 5: Final Commit ← was Step 6
- Step 6: Move Epic to done/ ← was Step 7
- Step 7: Final Verification & Completion ← was Step 8

---

## Files Created

### New Guide: stages/stage_6/user_testing.md

**Purpose:** Complete guide for Step 6 (User Testing & Bug Fix Protocol)

**Contents:**
- Step 6a: Ask User to Test the System
- Step 6b: Wait for User Testing Results
- Step 6c: Bug Fix Protocol (If User Found Bugs)
  - Phase 1: Document Bugs
  - Phase 2: Fix ALL Bugs
  - Phase 3: RESTART Stage 6 (from 6a)
  - Phase 4: Return to Step 6 (User Testing Again)
- Step 6d: Document User Testing Completion

**Key Requirements:**
- User testing is MANDATORY (cannot skip)
- Must wait for user response before proceeding
- ALL bugs must be fixed (cannot defer)
- Must RESTART Stage 6 after bug fixes
- Repeat until user reports "No bugs found"

---

## Files Modified

### 1. stages/stage_6/epic_qc_rounds.md
**Changes:**
- Updated "Next Steps" to proceed to "Step 6: User Testing & Bug Fix Protocol" instead of "Stage 6c: Epic PR Review"
- Two locations updated (after Round 3 Checkpoint, and in Next Steps section)

### 2. stages/stage_6/epic_final_qc.md (Router)
**Changes:**
- Updated sub-stage list from 3 to 4 guides
- Added STAGE_6c: User Testing (Step 6)
- Renumbered STAGE_6c to STAGE_6d (Epic Final Review, Steps 7-9)
- Updated Quick Navigation table
- Updated workflow diagram
- Updated total time estimate (4-6 hours → 4-7 hours)
- Updated step count (8 steps → 9 steps)
- Updated completion criteria
- Updated transition instructions between sub-stages
- Updated summary section

### 3. stages/stage_7/epic_cleanup.md
**Changes APPLIED:**
- ✅ Removed Step 5: User Testing & Bug Fix Protocol
- ✅ Renumbered Steps 6-8 to Steps 5-7
- ✅ Updated workflow overview diagram
- ✅ Updated Quick Navigation table (8 steps → 7 steps)
- ✅ Updated critical decision points
- ✅ Updated Critical Rules section (Rule 4 and Rule 11)
- ✅ Updated prerequisites (Stage 6 must include user testing passed)
- ✅ Updated completion criteria (moved user testing to Stage 6 section)
- ✅ Updated summary (removed user testing, updated critical success factors)

---

## Impact on Other Files

### Files that likely need updates:

1. **CLAUDE.md**
   - Update Stage 6 description
   - Update Stage 7 description
   - Update workflow overview

2. **stages/stage_6/epic_final_review.md**
   - Steps should be renumbered from 6-8 to 7-9
   - References to "Step 6" should become "Step 7"
   - etc.

3. **prompts_reference_v2.md and prompt files**
   - Stage 6 prompts may need updating
   - Stage 7 prompts may need updating

4. **epic_lessons_learned_template.md**
   - Stage 6 section should mention user testing

5. **epic_readme_template.md**
   - Stage 6 progress tracker should include Step 6 (User Testing)

6. **Reference cards**
   - stage_6_reference_card.md
   - stage_7_reference_card.md

---

## Implementation Status

**✅ COMPLETED:**
- Created stages/stage_6/user_testing.md
- Updated stages/stage_6/epic_qc_rounds.md
- Updated stages/stage_6/epic_final_qc.md (router)
- Updated stages/stage_7/epic_cleanup.md (removed user testing, renumbered steps)

**❌ NOT YET STARTED:**
- stages/stage_6/epic_final_review.md (renumber steps 6-8 to 7-9)
- CLAUDE.md (update workflow descriptions)
- Prompt files
- Template files
- Reference cards
- Any other files that reference Stage 6 or Stage 7 step numbers

---

## Verification Checklist

**To complete this change, verify:**

- [ ] All Stage 6 guides reference Step 6 as "User Testing"
- [ ] All Stage 6 guides reference Steps 7-9 (not 6-8) for Epic Final Review
- [ ] Stage 7 guide has steps 1-7 (not 1-8)
- [ ] Stage 7 guide does not mention user testing
- [ ] CLAUDE.md reflects updated Stage 6 and Stage 7
- [ ] All prompts updated for Stage 6 and Stage 7
- [ ] All templates updated
- [ ] All reference cards updated
- [ ] Workflow diagrams updated
- [ ] Step counts correct everywhere (Stage 6: 9 steps, Stage 7: 7 steps)

---

## Benefits of This Change

1. **Better workflow logic**
   - User testing validates quality (belongs in QC stage)
   - Cleanup focuses on finalization (no validation)

2. **Earlier bug detection**
   - User finds bugs earlier in process
   - Less rework after commit preparation

3. **Clearer quality gates**
   - Stage 6 = ALL quality validation (smoke, QC, user, PR review)
   - Stage 7 = Finalization only (guides, commit, archive)

4. **User approval before internal review**
   - User validates epic works
   - Then team does PR review
   - More logical sequence

5. **Consistent with feature workflow**
   - Features have user-facing testing in Stage 5c
   - Epics have user-facing testing in Stage 6
   - Both in the QC phase, not cleanup

---

## Migration Notes

**For in-progress epics:**

If an epic is currently in Stage 7 Step 5 (User Testing under old workflow):
1. Complete user testing as-is
2. If bugs found, follow old workflow (fix bugs, restart Stage 6, return to Stage 7 Step 5)
3. Do NOT apply new workflow mid-epic

**For new epics:**

Starting fresh with new workflow:
1. Stage 6 now includes user testing as Step 6
2. Stage 7 no longer includes user testing
3. Follow new guide structure

---

*End of USER_TESTING_MOVED_TO_STAGE_6.md*
