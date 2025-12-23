# D/ST Team Quality Fix - Implementation TODO

**Feature:** Fix D/ST team quality multiplier to use fantasy points scored instead of points allowed
**Status:** Pre-Implementation (24 iterations pending)
**Created:** 2025-12-21

---

## Iteration Progress Tracker

Track verification iteration completion:

**First Round (7 iterations):**
- [x] 1. Files & Patterns (Standard)
- [x] 2. Error Handling (Standard)
- [x] 3. Integration Points (Standard)
- [x] 4. Algorithm Mapping (Algorithm Traceability)
- [x] 5. Data Flow Trace (End-to-End Data Flow)
- [x] 6. Assumption Check (Skeptical Re-verification)
- [x] 7. Caller Check (Integration Gap Check)

**Second Round (9 iterations):**
- [x] 8. Answer Integration (Standard)
- [x] 9. Answer Verification (Standard)
- [x] 10. Dependency Check (Standard)
- [x] 11. Algorithm Re-verify (Algorithm Traceability)
- [x] 12. Data Flow Re-trace (End-to-End Data Flow)
- [x] 13. Assumption Re-check (Skeptical Re-verification)
- [x] 14. Caller Re-check (Integration Gap Check)
- [x] 15. Final Preparation (Standard)
- [x] 16. Integration Checklist (Standard)

**Third Round (8 iterations):**
- [x] 17. Fresh Eyes #1 (Fresh Eyes Review) - **CRITICAL GAP FOUND**
- [x] 18. Fresh Eyes #2 (Fresh Eyes Review)
- [x] 19. Algorithm Deep Dive (Algorithm Traceability)
- [x] 20. Edge Cases (Edge Case Verification)
- [x] 21. Test Planning (Test Coverage Planning + Mock Audit)
- [x] 22. Final Assumption Check (Skeptical Re-verification) - **INVALID ASSUMPTION FOUND**
- [x] 23. Final Caller Check (Integration Gap Check)
- [x] 24. Readiness Check (Implementation Readiness) - **BLOCKER IDENTIFIED**

---

## Protocol Execution Tracker

- [x] Algorithm Traceability Matrix (iteration 4) - Complete
- [x] End-to-End Data Flow (iteration 5) - Complete
- [x] Skeptical Re-verification (iteration 6) - Complete
- [x] Integration Gap Check (iteration 7) - Complete
- [x] Algorithm Traceability Matrix (iteration 11) - Complete
- [x] End-to-End Data Flow (iteration 12) - Complete
- [x] Skeptical Re-verification (iteration 13) - Complete
- [x] Integration Gap Check (iteration 14) - Complete
- [x] Algorithm Traceability Matrix (iteration 19) - Complete
- [x] Skeptical Re-verification (iteration 22) - Invalid assumption found
- [x] Integration Gap Check (iteration 23) - Complete
- [x] Fresh Eyes Review (iterations 17, 18) - Critical gap found
- [x] Edge Case Verification (iteration 20) - Complete
- [x] Test Coverage Planning (iteration 21) - Complete
- [x] Implementation Readiness (iteration 24) - Blocker identified

---

## Progress Notes

**Last Updated:** 2025-12-21 (Third Verification Round complete - BLOCKER FOUND)
**Current Status:** Iterations 1-24 complete, CRITICAL GAP identified
**Current Iteration:** 24/24 complete
**Next Steps:** Resolve blocker, update TODO with missing Phase 1.0
**Blockers:** ❌ TeamDataManager needs to load players.csv for D/ST data (implementation detail missing)

**Baseline Test Status:** 2221/2225 tests passing (99.8%)
- 4 pre-existing failures in accuracy simulation (unrelated to this feature)
- Will ensure no new test failures introduced

**First Round Findings:**
- Verified TeamDataManager._rank_offensive() pattern (lines 205-217) - perfect template for _rank_dst_fantasy()
- Confirmed players.csv has week_1_points through week_17_points columns
- Identified PlayerManager.load_players_from_csv() modification point (lines 199-202)
- Verified data flow from CSV → TeamDataManager → PlayerManager → ScoringCalculator
- All assumptions validated against codebase
- No orphan code risk - both new methods have identified callers

**Second Round Findings:**
- MIN_WEEKS default: 5 weeks (ConfigManager.get_team_quality_min_weeks(), line 482)
- All dependencies verified: DEFENSE_POSITIONS, week_N_points, team_defensive_rank
- Complete data flow traced: CSV → FantasyPlayer objects → TeamDataManager rankings → PlayerManager conditional → player_scoring.py
- Algorithm mapping confirmed: all spec algorithms map to existing patterns
- Integration points verified: _calculate_rankings() calls new method, PlayerManager uses getter
- No implementation blockers - ready for Third Round verification

**Third Round Findings:**
- ❌ **CRITICAL GAP**: TeamDataManager doesn't load players.csv, only team_data/*.csv
- ❌ **MISSING IMPLEMENTATION**: Phase 1.3 says "Calculate D/ST weekly scores from players.csv" but HOW is not specified
- ✅ **DATA VERIFIED**: D/ST entries exist in players.csv (format: "Texans D/ST", position="DST", week_N_points columns)
- ❌ **INVALID ASSUMPTION**: TeamDataManager can access D/ST data without loading players.csv
- ✅ **INITIALIZATION ORDER**: TeamDataManager.__init__() runs BEFORE PlayerManager loads players
- ❌ **BLOCKER**: Need to add method to load D/ST player data from players.csv into TeamDataManager
- ✅ **SOLUTION**: Add _load_dst_player_data() method to TeamDataManager (Phase 1.0)
- ✅ All edge cases covered, all algorithms mapped, all tests planned
- ⚠️ **NOT READY FOR IMPLEMENTATION** until blocker resolved

---

## Implementation Summary

**Objective:** Fix D/ST team quality multiplier to rank D/ST units by fantasy points scored (not points allowed to opponents)

**Key Decisions from Planning:**
1. Solution: Option 1 - Add D/ST-specific ranking calculation
2. Data Model: Reuse existing `team_defensive_rank` attribute (no new attribute needed)
3. For D/ST: `team_defensive_rank` = D/ST fantasy rank
4. For others: `team_defensive_rank` = defensive rank (unchanged)
5. Calculation: Eager (with other rankings at init), follow offensive pattern (descending)
6. Edge cases: Skip bye weeks (None/0), neutral rank 16 until MIN_WEEKS met
7. Testing: Full test suite (10 tests)
8. Documentation: All updates (scoring docs, ARCHITECTURE.md, inline docstrings)

---

## Files to Modify

### Production Code (2 files)

**1. league_helper/util/TeamDataManager.py**
- Add `self.dst_player_data: Dict[str, List[Optional[float]]] = {}` to __init__ ⚠️ **NEW**
- Add `_load_dst_player_data()` method to load D/ST weekly scores from players.csv ⚠️ **NEW**
- Add `self.dst_fantasy_ranks: Dict[str, int] = {}` to __init__
- Add `_rank_dst_fantasy()` method (similar to `_rank_offensive()`)
- Add `get_team_dst_fantasy_rank(team)` getter
- Update `_set_neutral_rankings()` to include D/ST
- Update `_calculate_rankings()` to calculate dst_totals from dst_player_data ⚠️ **UPDATED**
- Update `_calculate_rankings()` to call `_rank_dst_fantasy(dst_totals)`

**2. league_helper/util/PlayerManager.py**
- Modify `load_players()` to set `team_defensive_rank` differently for D/ST positions
- For D/ST: use `get_team_dst_fantasy_rank()`
- For others: use `get_team_defensive_rank()` (unchanged)

### Tests (1 file + new tests)

**3. tests/league_helper/util/test_PlayerManager_scoring.py**
- Update existing test at line 737 to use dst_fantasy_rank for D/ST

**4. tests/league_helper/util/test_TeamDataManager.py** (new tests)
- 6 new unit tests for D/ST ranking calculation

**5. tests/league_helper/util/test_PlayerManager_DST.py** (new file)
- 4 new integration tests for D/ST team quality

### Documentation (2 files)

**6. docs/scoring/04_team_quality_multiplier.md**
- Add D/ST-specific section explaining different metric

**7. ARCHITECTURE.md**
- Document new TeamDataManager methods

---

## Implementation Phases

### Phase 1: TeamDataManager - D/ST Ranking Infrastructure

**1.0 Load D/ST player data from players.csv** ⚠️ **CRITICAL - MISSING FROM ORIGINAL PLAN**
- [ ] Add `self.dst_player_data: Dict[str, List[Optional[float]]] = {}` to `__init__` (after line 79)
- [ ] Add `_load_dst_player_data()` method after `_load_team_data()` (after line 102)
- [ ] Load players.csv and filter for position == "DST"
- [ ] Extract week_1_points through week_17_points for each team
- [ ] Store in dict: `{"HOU": [8.0, 5.0, 7.0, ...], "DEN": [16.0, -5.0, 8.0, ...], ...}`
- [ ] Call `_load_dst_player_data()` in `__init__` before `_calculate_rankings()` (after line 87)
- Location: `league_helper/util/TeamDataManager.py`
- Pattern: Similar to `_load_team_data()` but for D/ST player data only
- **Why needed**: TeamDataManager doesn't have access to players.csv, which contains D/ST weekly scores

**1.1 Add D/ST ranking dictionary**
- [ ] Add `self.dst_fantasy_ranks: Dict[str, int] = {}` to `__init__` (after line 82)
- Location: `league_helper/util/TeamDataManager.py`
- Pattern: Same as `self.offensive_ranks` and `self.defensive_ranks`

**1.2 Update neutral rankings**
- [ ] Add `self.dst_fantasy_ranks[team] = 16` to `_set_neutral_rankings()` (after line 199)
- Location: `league_helper/util/TeamDataManager.py:195-203`
- Purpose: Set neutral rank 16 for D/ST when current_week <= MIN_WEEKS

**1.3 Implement _rank_dst_fantasy() method**
- [ ] Add method after `_rank_defensive()` (after line 231)
- [ ] Calculate D/ST weekly scores from players.csv
- [ ] Use rolling window (same MIN_WEEKS as offensive/defensive)
- [ ] Skip bye weeks (None or 0 values)
- [ ] Include negative scores in calculation
- [ ] Sort descending (more points = rank 1, like offensive)
- Location: `league_helper/util/TeamDataManager.py` (new method ~line 232)
- Pattern: Follow `_rank_offensive()` structure (lines 205-217)

**1.4 Implement get_team_dst_fantasy_rank() getter**
- [ ] Add method after `get_team_defensive_rank()` (after line 275)
- [ ] Return `self.dst_fantasy_ranks.get(team)`
- [ ] Returns Optional[int] (None if team not found)
- Location: `league_helper/util/TeamDataManager.py` (new method ~line 276)
- Pattern: Match `get_team_offensive_rank()` signature (lines 264-266)

**1.5 Update _calculate_rankings() to call _rank_dst_fantasy()**
- [ ] Calculate `dst_totals` dict from `self.dst_player_data` using rolling window (after line 183)
- [ ] Loop through each team in dst_player_data
- [ ] Extract week_N_points for weeks in rolling window (tq_start_week to end_week)
- [ ] Skip None and 0 values (bye weeks)
- [ ] Sum points and count games: `dst_totals[team] = (total, games)`
- [ ] Add call to `self._rank_dst_fantasy(dst_totals)` after defensive ranking (after line 187)
- Location: `league_helper/util/TeamDataManager.py:104-193`
- Pattern: Similar to offensive_totals calculation but from dst_player_data instead of team_weekly_data

**1.6 QA Checkpoint: TeamDataManager D/ST ranking**
- [ ] Run TeamDataManager tests: `python -m pytest tests/league_helper/util/test_TeamDataManager.py -v`
- [ ] Verify dst_fantasy_ranks populated with 32 teams
- [ ] Verify Houston D/ST rank is in range 1-6 (EXCELLENT tier)
- [ ] Expected: All tests pass, no WARNING/ERROR logs

---

### Phase 2: PlayerManager - Conditional Rank Assignment

**2.1 Modify load_players() for D/ST conditional ranking**
- [ ] Find `team_defensive_rank` assignment (line ~202)
- [ ] Add conditional: if position in Constants.DEFENSE_POSITIONS
- [ ] For D/ST: `player.team_defensive_rank = self.team_data_manager.get_team_dst_fantasy_rank(player.team)`
- [ ] For others: keep existing `get_team_defensive_rank()` call
- [ ] Add comment explaining semantic difference
- Location: `league_helper/util/PlayerManager.py:199-202`

**2.2 QA Checkpoint: PlayerManager rank assignment**
- [ ] Run PlayerManager tests: `python -m pytest tests/league_helper/util/test_PlayerManager_scoring.py -v`
- [ ] Verify D/ST players get dst_fantasy_rank
- [ ] Verify non-D/ST players still get defensive_rank
- [ ] Expected: Existing tests may fail (test at line 737 needs update), fix in Phase 3

---

### Phase 3: Tests - Update Existing + Add New

**3.1 Update existing test (line 737)**
- [ ] Rename: `test_team_quality_defense_uses_defensive_rank` → `test_team_quality_defense_uses_dst_fantasy_rank`
- [ ] Change: Set `test_player.team_dst_fantasy_rank = 3` (not team_defensive_rank)
- [ ] Verify: DST position uses rank 3 (EXCELLENT multiplier)
- Location: `tests/league_helper/util/test_PlayerManager_scoring.py:737-746`

**3.2 Add Unit Tests for TeamDataManager** (6 tests)
- [ ] test_rank_dst_fantasy_calculates_correctly
- [ ] test_rank_dst_fantasy_handles_bye_weeks
- [ ] test_rank_dst_fantasy_handles_negative_scores
- [ ] test_rank_dst_fantasy_missing_team_returns_none
- [ ] test_rank_dst_fantasy_uses_rolling_window
- [ ] test_rank_dst_fantasy_neutral_early_season
- Location: `tests/league_helper/util/test_TeamDataManager.py` (add to existing file)

**3.3 Add Integration Tests** (4 tests)
- [ ] test_dst_uses_dst_fantasy_rank_not_defensive_rank
- [ ] test_offensive_players_unchanged
- [ ] test_houston_dst_gets_excellent_rating (real data verification)
- [ ] test_all_dst_teams_have_rankings
- Location: New file `tests/league_helper/util/test_PlayerManager_DST.py` OR add to existing test file

**3.4 QA Checkpoint: All tests pass**
- [ ] Run all tests: `python tests/run_all_tests.py`
- [ ] Expected: 100% pass rate (no new failures beyond pre-existing 4)
- [ ] Verify Houston D/ST test passes with EXCELLENT rating

---

### Phase 4: Documentation

**4.1 Update scoring documentation**
- [ ] Add "D/ST-Specific Team Quality" section to `docs/scoring/04_team_quality_multiplier.md`
- [ ] Explain why D/ST uses fantasy points scored vs points allowed
- [ ] Add Houston D/ST example (9.34 ppg → rank #2 → EXCELLENT)
- [ ] Document semantic shift in team_defensive_rank for D/ST

**4.2 Update ARCHITECTURE.md**
- [ ] Document `_rank_dst_fantasy()` in TeamDataManager section
- [ ] Document `get_team_dst_fantasy_rank()` getter
- [ ] Note semantic difference in team_defensive_rank by position

**4.3 Add inline docstrings**
- [ ] Docstring for `_rank_dst_fantasy()` (explain difference from defensive_rank)
- [ ] Docstring for `get_team_dst_fantasy_rank()` (note fantasy points metric)
- [ ] Comment in PlayerManager.load_players() (explain conditional logic)

---

## Testing Requirements

### Unit Tests (6 tests - TeamDataManager)
1. **test_rank_dst_fantasy_calculates_correctly**: Verify ranking with known data
2. **test_rank_dst_fantasy_handles_bye_weeks**: Skip None/0 values
3. **test_rank_dst_fantasy_handles_negative_scores**: Include negatives in average
4. **test_rank_dst_fantasy_missing_team_returns_none**: None for non-existent team
5. **test_rank_dst_fantasy_uses_rolling_window**: Only MIN_WEEKS counted
6. **test_rank_dst_fantasy_neutral_early_season**: Rank 16 when current_week <= MIN_WEEKS

### Integration Tests (4 tests - PlayerManager)
7. **test_dst_uses_dst_fantasy_rank_not_defensive_rank**: Verify D/ST uses new rank
8. **test_offensive_players_unchanged**: QB/RB/WR/TE/K still use offensive_rank
9. **test_houston_dst_gets_excellent_rating**: Houston #2 → EXCELLENT (real data)
10. **test_all_dst_teams_have_rankings**: All 32 teams get rank or None

### Test Requirements
- [ ] 100% pass rate maintained (no new failures)
- [ ] All edge cases covered (bye weeks, negatives, missing data, early season)
- [ ] Real data validation (Houston D/ST)
- [ ] Regression prevention (non-D/ST unchanged)

---

## Integration Matrix

Tracking integration between components:

| New Method | Called By | Verified |
|------------|-----------|----------|
| TeamDataManager._rank_dst_fantasy() | TeamDataManager._calculate_rankings() | [ ] |
| TeamDataManager.get_team_dst_fantasy_rank() | PlayerManager.load_players() | [ ] |

**Verification Evidence:**
- [ ] Call in _calculate_rankings() added (Phase 1.5)
- [ ] Call in load_players() added (Phase 2.1)
- [ ] No orphan methods (all new methods have callers)

---

## Algorithm Traceability Matrix

Mapping specification algorithms to code:

| Spec Algorithm | Code Location | Verified |
|----------------|---------------|----------|
| "D/ST ranked by fantasy points scored" | TeamDataManager._rank_dst_fantasy() | [ ] |
| "Skip bye weeks (None or 0)" | _rank_dst_fantasy() loop condition | [ ] |
| "Include negative scores" | _rank_dst_fantasy() summation | [ ] |
| "Sort descending (more = rank 1)" | _rank_dst_fantasy() sort | [ ] |
| "Neutral rank 16 until MIN_WEEKS" | _set_neutral_rankings() | [ ] |
| "For D/ST: use fantasy rank" | PlayerManager.load_players() conditional | [ ] |
| "For others: use defensive rank" | PlayerManager.load_players() else clause | [ ] |

---

## Edge Cases

| Edge Case | Task | Test |
|-----------|------|------|
| Bye week (None value) | Skip in _rank_dst_fantasy() | test_rank_dst_fantasy_handles_bye_weeks |
| Bye week (0 value) | Skip in _rank_dst_fantasy() | test_rank_dst_fantasy_handles_bye_weeks |
| Negative D/ST score | Include in total | test_rank_dst_fantasy_handles_negative_scores |
| Missing team data | Return None | test_rank_dst_fantasy_missing_team_returns_none |
| Early season (week < MIN_WEEKS) | Neutral rank 16 | test_rank_dst_fantasy_neutral_early_season |
| Rolling window | Only count MIN_WEEKS | test_rank_dst_fantasy_uses_rolling_window |

---

## Dependencies

**External Classes Used:**
- `Constants.DEFENSE_POSITIONS` (read only)
- `ConfigManager.get_team_quality_min_weeks()` (existing)
- `FantasyPlayer.team_defensive_rank` (existing attribute, repurposed)
- `FantasyPlayer.week_N_points` (existing attributes)
- `FantasyPlayer.position` (existing attribute)

**No new dependencies added** - all required infrastructure exists.

---

## Rollback Plan

**Checkpoint Strategy:**
- Commit after Phase 1 complete: "Phase 1: TeamDataManager D/ST ranking infrastructure"
- Commit after Phase 2 complete: "Phase 2: PlayerManager conditional rank assignment"
- Commit after Phase 3 complete: "Phase 3: Tests updated and new tests added"
- Commit after Phase 4 complete: "Phase 4: Documentation updated"

**Rollback Commands:**
```bash
# View recent commits
git log --oneline -10

# Revert to specific phase
git checkout <commit-hash>

# Revert all uncommitted changes
git checkout -- .
```

**Point of No Return:** None - all changes are additive, no breaking changes to existing APIs.

---

## Success Criteria

**Must be true before marking complete:**
- [ ] Houston D/ST gets EXCELLENT or GOOD rating (not VERY_POOR)
- [ ] All 32 NFL teams have dst_fantasy_rank calculated (or None if missing)
- [ ] Non-D/ST positions (QB, RB, WR, TE, K) behavior unchanged
- [ ] All 10 new tests pass
- [ ] No new test failures (maintain 2221/2225 baseline)
- [ ] Documentation updated (scoring docs, ARCHITECTURE.md, docstrings)
- [ ] No WARNING or ERROR logs during ranking calculation
- [ ] Code follows existing patterns (offensive ranking structure)

---

## Notes

**Key Implementation Insight:** By reusing `team_defensive_rank` instead of adding a new attribute, we:
- Avoid data model changes (no FantasyPlayer modification)
- Avoid player_scoring.py changes (already uses team_defensive_rank for D/ST)
- Simplify implementation (fewer files to modify)

**Semantic Shift:** `team_defensive_rank` means different things based on position:
- For D/ST: "How good is this team's D/ST at scoring fantasy points?"
- For others: "How good is this team's defense at limiting opponent points?"

This is acceptable because these are position-specific metrics that don't need cross-position comparison.
