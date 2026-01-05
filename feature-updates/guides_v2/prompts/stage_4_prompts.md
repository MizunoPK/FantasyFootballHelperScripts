# Stage 4 Prompts: Epic Testing Strategy

**Stage:** 4
**Purpose:** Epic test plan update based on feature specs

---

## Starting Stage 4: Epic Testing Strategy

**User says:** "Update epic test plan" or "Define testing strategy" or Agent detects Stage 3 complete

**Prerequisite:** Stage 3 complete (user signed off on aligned specs)

**Agent MUST respond:**

```
I'm reading `stages/stage_4/epic_testing_strategy.md` to ensure I create a comprehensive epic testing strategy...

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
- Current Guide: stages/stage_4/epic_testing_strategy.md
- Guide Last Read: {YYYY-MM-DD HH:MM}
- Critical Rules: "Update test plan (don't recreate)", "Hybrid test scenarios", "Measurable success criteria", "Plan will evolve in Stage 5e"
- Next Action: Review current epic_smoke_test_plan.md and identify updates needed

Starting test plan update...
```

---

*For prompts for other stages, see the [prompts index](../prompts_reference_v2.md)*
