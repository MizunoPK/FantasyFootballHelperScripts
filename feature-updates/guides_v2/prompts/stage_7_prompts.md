# Stage 7 Prompts: Epic Cleanup

**Stage:** 7
**Purpose:** Final verification, user testing, commit, and archival

---

## Starting Stage 7: Epic Cleanup

**User says:** "Finalize epic" or "Commit and archive" or Agent detects Stage 6 complete

**Prerequisite:** Stage 6 complete (epic smoke testing, QC rounds, PR review all passed)

**Agent MUST respond:**

```
I'm reading `stages/stage_7/epic_cleanup.md` to ensure I properly finalize and archive the epic...

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
- **Final Commit**:
  - Review all changes (git status, git diff)
  - Stage all epic-related changes
  - Create commit with clear, descriptive message
  - Format: "Complete {epic_name} epic" with features listed in body
  - Push to remote (if user requests)
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
- Current Guide: stages/stage_7/epic_cleanup.md
- Guide Last Read: {YYYY-MM-DD HH:MM}
- Critical Rules: "Unit tests 100% pass before commit", "User testing MANDATORY before commit", "If bugs found → RESTART Stage 6", "Move ENTIRE epic folder", "Leave .txt in root"
- Next Action: Run python tests/run_all_tests.py

Running unit tests...
```

---

*For prompts for other stages, see the [prompts index](../prompts_reference_v2.md)*
