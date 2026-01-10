# Investigation Rounds Tracker

**Epic:** KAI-5-add_k_dst_ranking_metrics_support
**Created:** 2026-01-09

---

## Active Investigations

| Issue # | Issue Name | Current Round | Status |
|---------|------------|---------------|--------|
| 001 | incomplete_simulation_results | Round 1 Complete | Diagnostic logging added - ready for verification |

---

## Investigation Round Details

### Issue 001 - Round 1: Code Tracing
**Start Time:** 2026-01-09 (approximately 30 minutes)
**Status:** Complete - Hypothesis formed, diagnostic logging added
**Objective:** Trace code flow to identify where ranking_metrics are lost

**Findings:**
1. Found invalid 'ros' key in horizon_map (minor bug, doesn't affect ranking_metrics)
2. Found resume logic doesn't load ranking_metrics from old files
3. Found comparison logic requires BOTH configs to have metrics
4. Formed hypothesis: Old configs (loaded from Dec 23 files) don't have ranking_metrics → cause new configs to be compared via MAE fallback → new configs with metrics rejected

**Diagnostic Logging Added:**
- `load_intermediate_results()`: Log if ranking_metrics present in loaded files
- `add_result()`: Log overall_metrics status for new and current best configs
- `is_better_than()`: Log which comparison path taken (metrics vs MAE)
- `save_intermediate_results()`: Log if ranking_metrics being saved or missing

**Next Step:** Run simulation with diagnostic logging to verify hypothesis

---

## Completed Investigations

(None yet - Round 1 complete, awaiting verification)

---

## Investigation Statistics

**Total Investigations:** 1 active, 0 complete
**Average Rounds per Issue:** N/A (first round)
**Total Investigation Time:** ~30 minutes (Round 1)
