# Stage 3 Prompts: Cross-Feature Sanity Check

**Stage:** 3
**Purpose:** Cross-feature validation and alignment

---

## Starting Stage 3: Cross-Feature Sanity Check

**User says:** "Review all features" or "Run cross-feature sanity check" or Agent detects ALL features completed Stage 2

**Prerequisite:** ALL features have completed Stage 2 (all feature README.md files show "Stage 2 complete")

**Agent MUST respond:**

```
I'm reading `stages/s3/s3_cross_feature_sanity_check.md` to ensure I perform systematic cross-feature validation...

**The guide requires:**
- Systematic pairwise comparison of ALL feature specs
- Interface validation between features
- Dependency graph creation and cycle detection
- Conflict resolution with user clarification
- **MANDATORY user sign-off** before proceeding to Stage 4
- NO SKIPPING comparisons (N×N matrix approach)
- Document conflicts and resolutions

**Prerequisites I'm verifying:**
✅ ALL features show "Stage 2 complete" in their README.md files
  - Feature 01 ({name}): ✅
  - Feature 02 ({name}): ✅
  - {Continue for all features}
✅ All feature spec.md files exist
✅ All feature checklist.md files resolved

**I'll now proceed with systematic pairwise comparison...**

**Updating EPIC_README.md Agent Status:**
- Current Stage: Stage 3 - Cross-Feature Sanity Check
- Current Guide: stages/s3/s3_cross_feature_sanity_check.md
- Guide Last Read: {YYYY-MM-DD HH:MM}
- Critical Rules: "Pairwise comparison mandatory", "User sign-off required", "No skipping comparisons"
- Next Action: Create Feature Comparison Matrix and begin pairwise validation

Starting cross-feature analysis...
```

---

*For prompts for other stages, see the [prompts index](../prompts_reference_v2.md)*
