# Stage 7 Prompts: Epic Cleanup

**Stage:** 7
**Purpose:** Final verification, user testing, commit, and archival

---

## Starting Stage 7: Epic Cleanup

**User says:** "Finalize epic" or "Commit and archive" or Agent detects Stage 6 complete

**Prerequisite:** Stage 6 complete (epic smoke testing, QC rounds, PR review all passed)

**Agent MUST respond:**

```
I'm reading `stages/s7/s7_epic_cleanup.md` to ensure I properly finalize and archive the epic...

**The guide requires:**
- **Run Unit Tests** (100% pass required):
  - Execute: python tests/run_all_tests.py
  - Verify exit code = 0
  - If ANY tests fail → Fix before committing
- **Documentation Verification**:
  - EPIC_README.md complete and accurate
  - epic_lessons_learned.md contains insights from all stages
  - epic_smoke_test_plan.md reflects final implementation
  - All feature README.md files complete
- **Update Guides** (if lessons identified):
  - Review epic_lessons_learned.md "Guide Improvements Needed"
  - Update guides_v2/ files if improvements identified
  - Update CLAUDE.md if workflow changed
  - Document guide updates
- **⚠️ USER TESTING (MANDATORY GATE - BEFORE COMMIT)**:
  - Ask user to test complete system themselves
  - User reports any bugs discovered during testing
  - If bugs found → Follow bug fix protocol (Stage 2→5a→5b→5c)
  - After ALL bug fixes → RESTART Stage 6 (Epic Final QC)
  - Return to user testing after Stage 6 passes
  - Repeat until user testing passes with ZERO bugs
  - CANNOT commit without user approval
- **Final Commit and Pull Request**:
  - Review all changes (git status, git diff)
  - Stage all epic-related changes
  - Create commit with clear, descriptive message
  - Format: "{commit_type}/KAI-{number}: Complete {epic_name} epic"
  - Push branch to remote
  - Create Pull Request for user review using gh CLI
  - Wait for user to review and merge PR
  - Update EPIC_TRACKER.md after user merges
- **Move Epic to done/**:
  - Move ENTIRE epic folder: feature-updates/{epic}/ → feature-updates/done/{epic}/
  - Leave original epic request (.txt) in root for reference
  - Verify folder structure intact after move
- **Final Verification**:
  - Epic in done/ folder
  - Original request still in root
  - Git shows clean state

**Prerequisites I'm verifying:**
✅ Stage 6 complete (EPIC_README.md shows epic QC passed)
✅ No pending features or bug fixes
✅ All tests passing (verified recently)

**I'll now run unit tests to verify 100% pass rate...**

**Updating EPIC_README.md Agent Status:**
- Current Stage: Stage 7 - Epic Cleanup
- Current Guide: stages/s7/s7_epic_cleanup.md
- Guide Last Read: {YYYY-MM-DD HH:MM}
- Critical Rules: "Unit tests 100% pass before commit", "User testing MANDATORY before commit", "If bugs found → RESTART Stage 6", "Move ENTIRE epic folder", "Leave .txt in root"
- Next Action: Run python tests/run_all_tests.py

Running unit tests...
```

---

## S7.P1: Guide Update from Lessons Learned (MANDATORY)

**Trigger:** After Stage 7 STEP 3 complete (documentation verified), before final commit

**Prerequisite:** All lessons_learned.md files complete

**Agent MUST transition to S7.P1:**

```
I'm reading `stages/s7/s7_p1_guide_update_workflow.md` to apply lessons learned to guides...

**The guide requires:**
- **Analyze ALL lessons_learned.md files** from this epic:
  - epic_lessons_learned.md (epic-level lessons)
  - feature_XX_{name}/lessons_learned.md (all feature-level lessons)
- **Identify guide gaps:** For each lesson, determine which guide(s) could have prevented the issue
- **Create prioritized proposals** in GUIDE_UPDATE_PROPOSAL.md:
  - P0 (Critical): Prevents catastrophic bugs, mandatory gate gaps
  - P1 (High): Significantly improves quality, reduces major rework
  - P2 (Medium): Moderate improvements, clarifies ambiguity
  - P3 (Low): Minor improvements, cosmetic fixes
- **Get user approval INDIVIDUALLY:** Each proposal gets Approve/Modify/Reject/Discuss
- **Apply only approved changes** to guides
- **Create separate commit** for guide updates (before epic commit)

**Scope of guide updates:**
- All files in feature-updates/guides_v2/
- CLAUDE.md (root project instructions)
- Any files supporting future agents

**User approval process:**
- Each proposal presented individually with before/after
- User can: Approve (apply as-is) / Modify (provide alternative) / Reject (skip) / Discuss (ask questions)
- Agent applies only approved changes or user modifications

**Why this matters:**
- Continuous guide improvement based on real implementation experience
- Future agents benefit from lessons learned in this epic
- Systematic feedback loop: implementation → lessons → guide updates
- User has full control over guide evolution

**Prerequisites I'm verifying:**
✅ Stage 7 STEP 3 complete (documentation verified)
✅ All lessons_learned.md files complete
✅ Ready to analyze lessons and create proposal

**I'll now analyze the lessons learned from this epic and create GUIDE_UPDATE_PROPOSAL.md...**

**Updating EPIC_README.md Agent Status:**
- Current Stage: S7.P1 - Guide Update from Lessons Learned
- Current Phase: GUIDE_ANALYSIS
- Current Guide: stages/s7/s7_p1_guide_update_workflow.md
- Guide Last Read: {YYYY-MM-DD HH:MM}
- Critical Rules: "Analyze ALL lessons", "Prioritize P0-P3", "Individual approval", "Apply only approved", "Separate commit"
- Next Action: Read all lessons_learned.md files and identify guide gaps

Analyzing lessons learned...
```

**Full workflow:** See `prompts/guide_update_prompts.md` for complete prompts (presentation, approval, modifications, etc.)

---

*For prompts for other stages, see the [prompts index](../prompts_reference_v2.md)*
