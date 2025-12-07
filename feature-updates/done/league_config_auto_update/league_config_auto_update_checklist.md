# League Config Auto Update - Checklist

## Open Questions

### Architecture Questions

- [x] **Q1: Extend existing method or create new one?**
  - ~~Option A: Extend `update_league_config()`~~
  - **Option B: Create new `update_configs_folder()` method in ResultsManager** ✓
  - ~~Option C: Create utility function in separate file~~

- [x] **Q2: Should week files also preserve any parameters?**
  - **Option A: No preservation** ✓ (only MATCHUP→SCHEDULE mapping needed)

### Validation Questions

- [x] **Q3: What if optimal file is missing expected sections?**
  - **Option B: Log warning, use existing values** ✓

- [x] **Q4: Should performance_metrics be stripped from updated files?**
  - **Option B: Keep performance_metrics** ✓ (preserve for reference)

### Edge Case Questions

- [x] **Q5: What if original data/configs/ files don't exist?**
  - **Option A: Create from optimal files** ✓ (no preservation possible on first run)

- [x] **Q6: Confirm INJURY_PENALTIES should be preserved**
  - **Yes, preserve** ✓ (user-maintained setting, never overwritten)

---

## Resolution Log

| Question | Resolution | Date | Notes |
|----------|------------|------|-------|
| Q1 | New `update_configs_folder()` in ResultsManager | 2025-12-06 | Keeps existing method, adds orchestration method |
| Q2 | No preservation for week files | 2025-12-06 | Only MATCHUP→SCHEDULE mapping needed |
| Q3 | Log warning, use existing | 2025-12-06 | Graceful degradation if MATCHUP_SCORING missing |
| Q4 | Keep performance_metrics | 2025-12-06 | Preserve in updated files for reference |
| Q5 | Create from optimal | 2025-12-06 | If target files don't exist, copy optimal directly |
| Q6 | Yes, preserve INJURY_PENALTIES | 2025-12-06 | User-maintained setting, never overwritten |
