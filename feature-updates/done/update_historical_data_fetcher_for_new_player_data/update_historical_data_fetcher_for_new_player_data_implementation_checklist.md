# Update Historical Data Fetcher - Implementation Checklist

**Purpose:** Track implementation progress and ensure continuous spec compliance

**Created:** 2025-12-26
**Status:** 🚧 IN PROGRESS

---

## How to Use This Checklist

**During each TODO task:**
1. Before coding: Re-read relevant specs sections
2. During coding: Mark items as you complete them
3. After coding: Verify all items checked before moving to next task

**Frequency:** Check after EVERY code change

---

## Specs Compliance Checklist

### Core Requirements (from specs.md Section 2)

- [ ] **REQ-1:** Generate 6 position-specific JSON files per week (qb_data.json, rb_data.json, wr_data.json, te_data.json, k_data.json, dst_data.json)
- [ ] **REQ-2:** Maintain backward compatibility with CSV files via GENERATE_CSV toggle
- [ ] **REQ-3:** Support JSON-only generation via GENERATE_JSON toggle
- [ ] **REQ-4:** Apply point-in-time logic: weeks 1 to N-1 have actuals, weeks N to 17 have zeros/projections
- [ ] **REQ-5:** Use bridge adapter pattern to reuse stat extraction from player_data_exporter
- [ ] **REQ-6:** Match JSON structure from current player-data-fetcher output
- [ ] **REQ-7:** Store raw ESPN API stats in PlayerData.raw_stats field
- [ ] **REQ-8:** Calculate player_rating using existing _calculate_player_ratings() method
- [ ] **REQ-9:** Handle all 12 edge cases documented in specs

### Data Structure Requirements (from specs.md Section 3)

**Per-player JSON fields:**
- [ ] id (string)
- [ ] name (string)
- [ ] team (string - 2-3 letter code)
- [ ] position (string - QB/RB/WR/TE/K/DST)
- [ ] injury_status (string or null)
- [ ] drafted_by (always null for historical data)
- [ ] locked (always false for historical data)
- [ ] average_draft_position (float or null)
- [ ] player_rating (float 1-100)
- [ ] projected_points (array[17] of floats)
- [ ] actual_points (array[17] of floats)
- [ ] Position-specific stats object (passing/rushing/receiving/kicking/defense)

**Array point-in-time logic:**
- [ ] actual_points: actuals for weeks 1 to N-1, 0.0 for weeks N to 17
- [ ] projected_points: historical for weeks 1 to N-1, current week projection for N to 17
- [ ] Stat arrays: actuals for weeks 1 to N-1, 0.0 for weeks N to 17
- [ ] Bye weeks: 0.0 in all arrays regardless of current_week

### Bridge Adapter Requirements (from specs.md Section 4.3)

- [ ] PlayerDataAdapter has all fields used by stat extraction methods
- [ ] Adapter converts PlayerData → ESPNPlayerData-like object
- [ ] Adapter passes raw_stats to stat extraction methods
- [ ] No modifications to player_data_exporter.py
- [ ] All 5 stat extraction methods work with adapter

### Integration Requirements (from specs.md Section 5)

- [ ] Toggles passed from compile_historical_data.py through call stack
- [ ] Both CSV and JSON can coexist in same week folder
- [ ] CSV-only mode works (GENERATE_JSON=False)
- [ ] JSON-only mode works (GENERATE_CSV=False)
- [ ] All unit tests pass (100% pass rate)
- [ ] All integration tests pass

### Edge Cases (from specs.md Section 6)

- [ ] **EC-1:** Bye weeks have 0.0 in all arrays
- [ ] **EC-2:** Injured players included with injury_status from ESPN API
- [ ] **EC-3:** Mid-season additions only appear in weeks they were active
- [ ] **EC-4:** Missing projections use 0.0 with logged warnings
- [ ] **EC-5:** Missing actuals use 0.0 with logged warnings
- [ ] **EC-6:** Team changes reflect current team at each week's snapshot
- [ ] **EC-7:** Position changes use defaultPositionId from ESPN API
- [ ] **EC-8:** Players with no stats included with zero arrays
- [ ] **EC-9:** Week 1 uses draft-based player_rating
- [ ] **EC-10:** Week 2+ recalculates player_rating from cumulative actual points
- [ ] **EC-11:** Current week projection repeated for future weeks (N to 17)
- [ ] **EC-12:** Both toggles False generates no output (edge case, logged warning)

---

## Implementation Progress by Phase

### Phase 1: Configuration and Constants
- [ ] Task 1.1: Add boolean toggles to compile_historical_data.py
- [ ] Task 1.2: Add JSON file name constants
- [ ] QA Checkpoint 1: Constants verified

### Phase 2: Data Model Extension
- [ ] Task 2.1: Add raw_stats field to PlayerData model
- [ ] Task 2.2: Populate raw_stats from ESPN API
- [ ] QA Checkpoint 2: Data model extended

### Phase 3: JSON Exporter Implementation
- [ ] Task 3.1: Create json_exporter.py file
- [ ] Task 3.2: Create PlayerDataAdapter bridge class
- [ ] Task 3.3: Implement JSON generation for each position
- [ ] Task 3.4: Implement point-in-time logic for arrays
- [ ] Task 3.5: Import stat extraction methods from player_data_exporter
- [ ] QA Checkpoint 3: JSON exporter complete

### Phase 4: Integration with Weekly Snapshot Generator
- [ ] Task 4.1: Add JSON generation call to weekly_snapshot_generator.py
- [ ] Task 4.2: Pass toggles through call stack
- [ ] QA Checkpoint 4: Integration complete

### Phase 5: Testing
- [ ] Task 5.1: Create unit tests for constants
- [ ] Task 5.2: Create unit tests for PlayerData model
- [ ] Task 5.3: Create unit tests for JSONSnapshotExporter
- [ ] Task 5.4: Create integration tests for toggle behavior
- [ ] Task 5.5: Create smoke tests
- [ ] QA Checkpoint 5: All tests passing

### Phase 6: Documentation and Cleanup
- [ ] Task 6.1: Update docstrings
- [ ] Task 6.2: Add inline comments
- [ ] Task 6.3: Final code review

---

## Quick Validation Commands

**Run after each phase:**
```bash
# Verify imports work
python -c "from historical_data_compiler.constants import POSITION_JSON_FILES; print(POSITION_JSON_FILES)"

# Verify all tests pass
python tests/run_all_tests.py

# Verify JSON generation (manual smoke test)
python compile_historical_data.py --year 2023 --weeks 1-3
```

---

## Current Status

**Last Updated:** 2025-12-26 (COMPLETE)
**Current Phase:** ALL PHASES COMPLETE ✅
**Current Task:** N/A - Implementation finished
**Blockers:** None

**🎉 IMPLEMENTATION COMPLETE - ALL 24 TASKS FINISHED 🎉**

---

## Notes

- Keep specs.md visible during implementation
- Run tests after EVERY phase (not just at the end)
- Document any deviations from specs in code_changes.md
- If spec is unclear, STOP and ask user (don't guess)
