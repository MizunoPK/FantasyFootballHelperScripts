# Bug Fix Checklist: Wrong Data Folder

**Created:** 2025-12-31
**Status:** Stage 2 - Deep Dive

---

## Decision Tracking

| # | Question | Status | Resolution | Updated |
|---|----------|--------|------------|---------|
| 1 | IMPORTANT: Found 18 weeks (week_01 to week_18), not 17. Should we update ALL 18 weeks? | ✅ RESOLVED | YES - Update all 18 weeks (108 files: 18 × 6) | 2025-12-31 |
| 2 | Should we validate week folder naming (week_01, week_02, etc.)? | ✅ RESOLVED | NO - Trust week_* pattern, handle errors gracefully | 2025-12-31 |
| 3 | Do ALL simulation weeks have same players or can they differ? | ✅ RESOLVED | YES - Same player IDs across all weeks (verified via research R4) | 2025-12-31 |
| 4 | Should match report show per-week stats or just totals? | ✅ RESOLVED | Just totals - all weeks have same players, per-week stats redundant | 2025-12-31 |
| 5 | If a week folder has malformed JSON, fail entire operation or skip that week? | ✅ RESOLVED | FAIL entire operation - ensures consistency across all weeks | 2025-12-31 |
| 6 | Should we update other years (2021-2024) or ONLY 2025? | ✅ RESOLVED | ONLY 2025 - matches original epic scope, limits risk | 2025-12-31 |

---

## Research Questions

| # | Question | Status | Answer | Source |
|---|----------|--------|--------|--------|
| R1 | What is the actual JSON structure in simulation weeks? | ✅ RESOLVED | Direct array (no wrapper) | Read week_01/qb_data.json |
| R2 | How many week folders exist? | ✅ RESOLVED | 18 weeks (week_01 to week_18) | ls simulation/sim_data/2025/weeks/ |
| R3 | Do all weeks have all 6 position files? | ✅ RESOLVED | YES - All 18 weeks have exactly 6 files | ls all weeks |
| R4 | Are player IDs consistent across weeks? | ✅ RESOLVED | YES - Same player IDs across all weeks | Checked week_01 vs week_17 |
| R5 | What other years exist in sim_data? | ✅ RESOLVED | 2021, 2022, 2023, 2024, 2025 | ls simulation/sim_data/ |

---

## Scope Items

### Confirmed In Scope

1. ✅ Update all 18 week folders (week_01 to week_18)
2. ✅ Update all 6 position files per week (108 total files)
3. ✅ Handle direct JSON array structure (no wrapper)
4. ✅ Maintain atomic writes per file
5. ✅ Aggregate match report across weeks
6. ✅ Update unit tests for multi-week structure
7. ✅ Update epic E2E test validation
8. ✅ Update user test script verification

### Confirmed Design Decisions

9. ✅ NO week folder naming validation (trust week_* pattern)
10. ✅ Handle missing week folders gracefully (log WARNING, continue)
11. ✅ Match report shows ONLY totals (no per-week stats - redundant)
12. ✅ All weeks have same players (verified via research)
13. ✅ Malformed JSON: FAIL entire operation (all-or-nothing approach)

### Explicitly Out of Scope

- Updating other years (2024, 2026, etc.) - ONLY 2025
- Changing JSON structure (keep as direct arrays)
- Modifying non-ADP fields in player data

---

## Stage 2 Status

✅ **ALL QUESTIONS RESOLVED**
- Research questions: 5/5 resolved
- Decision questions: 6/6 resolved
- Scope items: All confirmed

**Next:** Proceed to Stage 5a (TODO Creation)
