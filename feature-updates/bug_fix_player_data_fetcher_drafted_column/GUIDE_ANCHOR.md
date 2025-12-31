# GUIDE ANCHOR: bug_fix_player_data_fetcher_drafted_column

**Purpose:** Resumption instructions after session compaction

**Last Updated:** 2025-12-30 (Stage 1 complete)

---

## 🚨 CRITICAL: Read This First

If you are a new agent resuming this epic after session compaction:

1. **READ EPIC_README.md** - Check "Agent Status" section at top
2. **READ THE GUIDE** listed in "Current Guide" field
3. **USE THE PROMPT** from `guides_v2/prompts_reference_v2.md` for current stage
4. **CONTINUE from** "Next Action" in Agent Status

**DO NOT:**
- ❌ Start a new stage without reading guide
- ❌ Skip phase transition prompts
- ❌ Assume you know workflow from memory

---

## Current Epic Status

**Last Agent Status (from EPIC_README.md):**
- Current Stage: Stage 1 - Epic Planning (COMPLETE)
- Next Stage: Stage 2 - Feature Deep Dives
- Next Guide: `STAGE_2_feature_deep_dive_guide.md`

---

## Epic Workflow Reference

```
Stage 1 → Stage 2 → Stage 3 → Stage 4 → Stage 5 → Stage 6 → Stage 7
  ↓         ↓         ↓         ↓         ↓         ↓         ↓
Epic    Features  Sanity   Testing   Impl     Epic      Done
Plan    Deep Dive  Check   Strategy  (5a-5e)  QC
```

**Current Position:** Stage 1 complete, ready for Stage 2

---

## Feature List

1. **feature_01_update_data_models_and_field_migration** - Migrate from drafted:int to drafted_by:str
2. **feature_02_disable_deprecated_csv_exports** - Remove creation of deprecated CSV files

**Implementation Order:** Feature 1 → Feature 2 (Feature 2 depends on Feature 1)

---

## Quick Links

- **EPIC_README.md** - Master epic tracking and Agent Status
- **epic_smoke_test_plan.md** - How to test complete epic
- **epic_lessons_learned.md** - Cross-feature insights
- **Feature 01 README.md** - feature_01_update_data_models_and_field_migration/README.md
- **Feature 02 README.md** - feature_02_disable_deprecated_csv_exports/README.md

---

## Resumption Checklist

When resuming after session compaction:

- [ ] Read EPIC_README.md Agent Status
- [ ] Read current guide from guides_v2/
- [ ] Use phase transition prompt from prompts_reference_v2.md
- [ ] Update Agent Status in EPIC_README.md with "Guide Last Read" timestamp
- [ ] Continue from "Next Action"

**If Agent Status shows "WAIT for user approval" - DO NOT PROCEED. Wait for user response.**
