# S4 Prompts: Epic Testing Strategy

**Stage:** 4
**Purpose:** Epic test plan update based on feature specs

---

## Starting S4: Epic Testing Strategy

**User says:** "Update epic test plan" or "Define testing strategy" or Agent detects S3 complete

**Prerequisite:** S3 complete (user signed off on aligned specs)

**Agent MUST respond:**

```markdown
I'm reading `stages/s4/s4_feature_testing_strategy.md` to ensure I create a comprehensive epic testing strategy...

**The guide requires:**
- Review initial epic_smoke_test_plan.md (created in S1)
- Update test plan based on S2-3 findings:
  - Integration points identified in S3
  - Actual feature implementations (not assumptions)
  - Cross-feature workflows that need testing
- Define epic success criteria (measurable)
- Create hybrid test scenarios:
  - Specific commands/scenarios (concrete tests to always run)
  - High-level categories (flexible areas for S8.P2/6 updates)
- Identify data quality checks (verify VALUES not just structure)
- Plan evolves: S1 (placeholder) → S4 (based on specs) → S8.P2 (based on implementation)

**Prerequisites I'm verifying:**
✅ S3 complete (EPIC_README.md shows user sign-off)
✅ All feature specs aligned
✅ Integration points documented
✅ epic_smoke_test_plan.md exists (from S1)

**I'll now review the existing test plan and update based on Stages 2-3 findings...**

**Updating EPIC_README.md Agent Status:**
- Current Stage: S4 - Epic Testing Strategy
- Current Guide: stages/s4/s4_feature_testing_strategy.md
- Guide Last Read: {YYYY-MM-DD HH:MM}
- Critical Rules: "Update test plan (don't recreate)", "Hybrid test scenarios", "Measurable success criteria", "Plan will evolve in S8.P2"
- Next Action: Review current epic_smoke_test_plan.md and identify updates needed

Starting test plan update...
```

---

## Gate 4.5: Epic Test Plan Approval (MANDATORY)

**Trigger:** Agent completes S4 test plan update (s4_feature_testing_strategy.md)

**Agent MUST present to user:**

```bash
🚨 **Gate 4.5: Epic Test Plan Approval Required**

I've updated the epic testing strategy in `epic_smoke_test_plan.md` based on the feature specs from Stages 2-3.

**Summary of epic_smoke_test_plan.md:**
- **Success Criteria:** {N} measurable criteria defined
- **Test Scenarios:** {N} specific test scenarios identified
- **Integration Points:** {N} cross-feature integration points documented
- **Data Quality Checks:** Verify VALUES (not just structure)
- **Concrete Commands:** Specific commands and expected outputs documented

**Key test scenarios include:**
1. {Scenario 1 summary - one sentence}
2. {Scenario 2 summary - one sentence}
3. {Scenario 3 summary - one sentence}
...

**Why approval is needed now:**
- I need to know EXACTLY how to test this work BEFORE creating implementation plans (S5)
- Test requirements will guide how I structure implementation tasks and test strategy
- Changes to test plan are cheap now, expensive after S5 validation loop completes

**Please review `epic_smoke_test_plan.md` and:**
- ✅ Approve if test strategy looks correct
- ❌ Request changes if test strategy needs adjustment

**Questions to consider:**
- Do the success criteria measure what matters to you?
- Are the test scenarios comprehensive enough?
- Are there additional integration points I should test?
- Do the data quality checks verify the right values?

**I cannot proceed to S5 (Implementation Planning) without your approval.**
```

**After user approves:**

```bash
✅ **Gate 4.5 PASSED - Epic Test Plan Approved**

**Updating EPIC_README.md:**
- Marking Gate 4.5 as ✅ PASSED
- Adding user approval timestamp to epic_smoke_test_plan.md

**What this means:**
- I now know EXACTLY how to test this work
- Implementation plans (S5) will be designed with these test requirements in mind
- Test strategy will guide implementation approach

**Next: S5 (Feature Implementation)**

Now that I know EXACTLY how to test this work (user-approved test plan), I'll transition to S5 to begin implementation planning for the first feature.

Following `stages/s5/s5_v2_validation_loop.md` to create comprehensive implementation plan using 2-phase validation loop approach (Draft Creation + Validation Loop with 18 dimensions).
```

---

*For prompts for other stages, see the [prompts index](../prompts_reference_v2.md)*
