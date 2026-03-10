# S3 Prompts: Epic-Level Documentation, Testing Plans, and Approval

**Stage:** 3
**Purpose:** Epic-level testing strategy, documentation refinement, and user approval (Gate 4.5)

---

## Starting S3: Epic-Level Documentation, Testing Plans, and Approval

**User says:** "Start S3" or "Run epic-level docs and testing" or Agent detects ALL features completed S2

**Prerequisite:** ALL features have completed S2 (including S2.P2 Cross-Feature Alignment)

**Agent MUST respond:**

```markdown
I'm beginning S3 (Epic-Level Documentation, Testing Plans, and Approval).

**Guide I'm following:** stages/s3/s3_epic_planning_approval.md (from CLAUDE.md Stage Workflow table)
**Prerequisites verified:**
- [x] S2 fully complete for ALL features in EPIC_README.md (Feature Tracking all checked)
- [x] S2.P2 (Cross-Feature Alignment) complete — feature specs reconciled
- [x] epic_smoke_test_plan.md exists (initial version from S1)
- [x] Guide path matches CLAUDE.md Stage Workflow table
- [x] Read ENTIRE guide using Read tool

**The guide requires:**
- S3.P1: Create epic-level smoke test plan (integration tests across ALL features, NOT per-feature tests)
- S3.P2: Refine EPIC_README.md with feature summaries and architecture decisions
- S3.P3: Gate 4.5 — present epic plan to user, MANDATORY user approval before S4
- Each phase uses a 3-consecutive-clean Validation Loop
- SCOPE: This is epic-level work, not feature-level. Tests defined here span multiple features.

**Prerequisites I'm verifying:**
✅ ALL features show "S2 complete" in EPIC_README.md Feature Tracking:
  - Feature 01 ({name}): ✅
  - Feature 02 ({name}): ✅
  - {Continue for all features}
✅ S2.P2 (Cross-Feature Alignment) complete
✅ epic_smoke_test_plan.md exists

**Updating EPIC_README.md Agent Status:**
- Current Stage: S3 — Epic-Level Documentation, Testing Plans, and Approval
- Current Guide: stages/s3/s3_epic_planning_approval.md
- Guide Last Read: {YYYY-MM-DD HH:MM}
- Critical Rules: "Epic-level tests only (not per-feature)", "Gate 4.5 user approval mandatory"
- Next Action: S3.P1 — Review all feature test requirements, identify integration points

Starting S3.P1: Epic Testing Strategy Development...
```

---

*For prompts for other stages, see the [prompts index](../prompts_reference_v2.md)*
