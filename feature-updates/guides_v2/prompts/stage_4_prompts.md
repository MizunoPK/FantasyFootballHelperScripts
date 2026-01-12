# Stage 4 Prompts: Epic Testing Strategy

**Stage:** 4
**Purpose:** Epic test plan update based on feature specs

---

## Starting Stage 4: Epic Testing Strategy

**User says:** "Update epic test plan" or "Define testing strategy" or Agent detects Stage 3 complete

**Prerequisite:** Stage 3 complete (user signed off on aligned specs)

**Agent MUST respond:**

```
I'm reading `stages/s4/s4_epic_testing_strategy.md` to ensure I create a comprehensive epic testing strategy...

**The guide requires:**
- Review initial epic_smoke_test_plan.md (created in Stage 1)
- Update test plan based on Stage 2-3 findings:
  - Integration points identified in Stage 3
  - Actual feature implementations (not assumptions)
  - Cross-feature workflows that need testing
- Define epic success criteria (measurable)
- Create hybrid test scenarios:
  - Specific commands/scenarios (concrete tests to always run)
  - High-level categories (flexible areas for Stage 5e/6 updates)
- Identify data quality checks (verify VALUES not just structure)
- Plan evolves: Stage 1 (placeholder) → Stage 4 (based on specs) → Stage 5e (based on implementation)

**Prerequisites I'm verifying:**
✅ Stage 3 complete (EPIC_README.md shows user sign-off)
✅ All feature specs aligned
✅ Integration points documented
✅ epic_smoke_test_plan.md exists (from Stage 1)

**I'll now review the existing test plan and update based on Stages 2-3 findings...**

**Updating EPIC_README.md Agent Status:**
- Current Stage: Stage 4 - Epic Testing Strategy
- Current Guide: stages/s4/s4_epic_testing_strategy.md
- Guide Last Read: {YYYY-MM-DD HH:MM}
- Critical Rules: "Update test plan (don't recreate)", "Hybrid test scenarios", "Measurable success criteria", "Plan will evolve in Stage 5e"
- Next Action: Review current epic_smoke_test_plan.md and identify updates needed

Starting test plan update...
```

---

## Gate 4.5: Epic Test Plan Approval (MANDATORY)

**Trigger:** Agent completes Step 6.1 of s4_epic_testing_strategy.md (test plan updated)

**Agent MUST present to user:**

```
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
- I need to know EXACTLY how to test this work BEFORE creating implementation plans (Stage 5a)
- Test requirements will guide how I structure implementation tasks and test strategy
- Changes to test plan are cheap now, expensive after 28 verification iterations

**Please review `epic_smoke_test_plan.md` and:**
- ✅ Approve if test strategy looks correct
- ❌ Request changes if test strategy needs adjustment

**Questions to consider:**
- Do the success criteria measure what matters to you?
- Are the test scenarios comprehensive enough?
- Are there additional integration points I should test?
- Do the data quality checks verify the right values?

**I cannot proceed to Stage 5a (Implementation Planning) without your approval.**
```

**After user approves:**

```
✅ **Gate 4.5 PASSED - Epic Test Plan Approved**

**Updating EPIC_README.md:**
- Marking Gate 4.5 as ✅ PASSED
- Adding user approval timestamp to epic_smoke_test_plan.md

**What this means:**
- I now know EXACTLY how to test this work
- Implementation plans (Stage 5a) will be designed with these test requirements in mind
- Test strategy will guide implementation approach

**Next: Stage 5 (Feature Implementation)**

Now that I know EXACTLY how to test this work (user-approved test plan), I'll transition to Stage 5a to begin implementation planning for the first feature.

Following `stages/s5/s5_p1_planning_round1.md` (Round 1) to create comprehensive implementation plan with 28 verification iterations across 3 rounds.
```

---

*For prompts for other stages, see the [prompts index](../prompts_reference_v2.md)*
