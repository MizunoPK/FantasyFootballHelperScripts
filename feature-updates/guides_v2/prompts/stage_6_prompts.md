# Stage 9 Prompts: Epic Final QC

**Stage:** 6
**Purpose:** Epic-level testing and validation

---

## Starting Stage 9: Epic Final QC

**User says:** "Run epic QC" or "Validate the entire epic" or Agent detects ALL features complete Stage 5e

**Prerequisite:** ALL features complete Stage 5e, no pending bug fixes

**Agent MUST respond:**

```
I'm reading `stages/s9/s6_p1_epic_smoke_testing.md` to ensure I validate the entire epic end-to-end...

**The guide requires:**
- **Epic Smoke Testing** (distinct from feature-level testing):
  - Part 1: Epic-level import tests (all features together)
  - Part 2: Epic-level entry point tests
  - Part 3: Epic E2E execution tests (complete workflows with REAL data)
  - Part 4: Cross-feature integration tests (features working together)
  - **CRITICAL:** Verify OUTPUT DATA VALUES (not just structure)
- **Epic-Level QC Rounds** (3 rounds):
  - Round 1: Cross-Feature Integration Validation
  - Round 2: Epic Cohesion & Consistency
  - Round 3: End-to-End Success Criteria
- **Epic PR Review** (11 categories at EPIC scope):
  - Focus: Architectural consistency across features
  - Review epic-wide changes (not individual features)
- **Validation Against Original Epic Request**:
  - Read ORIGINAL {epic_name}.txt file
  - Verify epic achieves user's goals
  - Validate expected outcomes delivered
- **Use EVOLVED epic_smoke_test_plan.md**:
  - Plan updated in Stages 1 → 4 → 5e (all features)
  - Reflects ACTUAL implementation (not assumptions)
- **QC RESTART if ANY issues**:
  - Create bug fixes for issues
  - COMPLETELY RESTART Stage 9 after bug fixes

**Critical Distinction:**
- Feature testing (Stage 5c): Tests feature in ISOLATION
- Epic testing (Stage 9): Tests ALL features TOGETHER

**Prerequisites I'm verifying:**
✅ ALL features show "Stage 5e complete" in EPIC_README.md
  - Feature 01 ({name}): ✅
  - Feature 02 ({name}): ✅
  - {Continue for all features}
✅ No pending bug fixes
✅ epic_smoke_test_plan.md shows recent Stage 5e updates
✅ All unit tests passing (100%)

**I'll now execute the evolved epic_smoke_test_plan.md...**

**Updating EPIC_README.md Agent Status:**
- Current Stage: S9.P1 - Epic Smoke Testing
- Current Guide: stages/s9/s6_p1_epic_smoke_testing.md
- Guide Last Read: {YYYY-MM-DD HH:MM}
- Critical Rules: "Use EVOLVED test plan", "Verify OUTPUT DATA VALUES", "4-part smoke testing", "Cross-feature integration", "RESTART if ANY part fails"
- Next Action: Execute Step 1 - Pre-QC Verification

Starting epic smoke testing...
```

---

*For prompts for other stages, see the [prompts index](../prompts_reference_v2.md)*
