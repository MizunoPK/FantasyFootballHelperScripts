# TODO: Overhaul players_projected.csv Creation

**Objective**: Overhaul the player-data-fetcher to correctly create players_projected.csv with projection-only data

**Status**: ALL ITERATIONS COMPLETE - Ready for Implementation

**Reference Documents**:
- `updates/players_projected_overhaul.txt` - Original specification
- `docs/research/players_projected_implementation_analysis.md` - Implementation analysis
- `docs/research/espn_api_historical_projections_research.md` - ESPN API research

---

## User Answers Summary

| Question | Answer |
|----------|--------|
| Q1: Data Model Structure | **Option B** - Use dictionary `projected_weeks: Dict[int, Optional[float]]` |
| Q2: FantasyPlayer Updates | **Option A** - Skip FantasyPlayer, access directly from ESPNPlayerData |
| Q3: fantasy_points_calculator.py | **Option A** - Update to use correct ESPN API structure |
| Q4: players.csv Behavior | **Maintain current behavior** - Keep smart fallback logic |

---

## Phase 1: Player Data Model Updates

### 1.1 Update ESPNPlayerData Model
- **File**: `player-data-fetcher/player_data_models.py` (lines 25-89)
- **Task**: Add dictionary field to store projected week values
- **Implementation**:
  ```python
  # Add import at top
  from typing import Dict, List, Optional

  # Add to ESPNPlayerData class after line 71 (after updated_at)
  projected_weeks: Dict[int, float] = Field(default_factory=dict)

  # Add these methods after get_all_weekly_points() (after line 89)
  def set_week_projected(self, week: int, points: float):
      """Set projected points for a specific week (fantasy regular season weeks 1-17 only)"""
      if 1 <= week <= 17:
          self.projected_weeks[week] = points

  def get_week_projected(self, week: int) -> Optional[float]:
      """Get projected points for a specific week (fantasy regular season weeks 1-17 only)"""
      if 1 <= week <= 17:
          return self.projected_weeks.get(week)
      return None

  def get_all_weekly_projected(self) -> Dict[int, Optional[float]]:
      """Get all weekly projected points as a dictionary (weeks 1-17 only)"""
      return {week: self.projected_weeks.get(week) for week in range(1, 18)}
  ```
- **Test file**: `tests/player-data-fetcher/test_player_data_models.py`

---

## Phase 2: ESPN Client Modifications

### 2.1 Update _extract_raw_espn_week_points() Method
- **File**: `player-data-fetcher/espn_client.py` (lines 573-690)
- **Task**: Add `source_type` parameter to control extraction behavior
- **Changes**:
  1. Add `source_type: str = 'smart'` parameter to method signature (line 573)
  2. Modify logic to respect source_type:
     - `'smart'`: Current behavior (actual if available, fallback to projection)
     - `'actual'`: Only return statSourceId=0 entries
     - `'projection'`: Only return statSourceId=1 entries
  3. Remove `projectedTotal` fallback (lines 645-653) - this field doesn't exist

### 2.2 Modify _populate_weekly_projections() Method
- **File**: `player-data-fetcher/espn_client.py` (lines 533-571)
- **Current code** (lines 555-568):
  ```python
  for week in range(1, end_week + 1):
      espn_points = self._extract_raw_espn_week_points(all_weeks_data, week, position)
      if espn_points is not None and (espn_points > 0 or position == 'DST'):
          player_data.set_week_points(week, espn_points)
      else:
          player_data.set_week_points(week, 0.0)
  ```
- **New code**:
  ```python
  for week in range(1, end_week + 1):
      # Get smart value for week_N_points (actual for past, projection for future)
      smart_points = self._extract_raw_espn_week_points(all_weeks_data, week, position, 'smart')
      if smart_points is not None and (smart_points > 0 or position == 'DST'):
          player_data.set_week_points(week, smart_points)
      else:
          player_data.set_week_points(week, 0.0)

      # NEW: Also get projection-only value for projected_weeks dictionary
      projected_points = self._extract_raw_espn_week_points(all_weeks_data, week, position, 'projection')
      if projected_points is not None and (projected_points > 0 or position == 'DST'):
          player_data.set_week_projected(week, projected_points)
      else:
          player_data.set_week_projected(week, 0.0)
  ```

### 2.3 Fix Incorrect Code Comments
- **File**: `player-data-fetcher/espn_client.py`
- **Lines to fix**:
  - Line 458: Remove `projectedTotal` from example response
  - Line 500: Remove `projectedTotal` reference
  - Line 514: Remove `projectedTotal` reference
  - Lines 579-585: Update docstring to remove `projectedTotal` mentions
  - Lines 590, 592: Remove priority mentions of `projectedTotal`
  - Lines 634, 645-653: Remove `projectedTotal` fallback code entirely

### 2.4 Update fantasy_points_calculator.py
- **File**: `player-data-fetcher/fantasy_points_calculator.py`
- **Lines to fix**:
  - Line 10: Update docstring to remove `projectedTotal`
  - Line 37: Update config comment
  - Lines 113, 137, 144-146: Update logic comments
  - Lines 154-161: Remove `projectedTotal` fallback logic
  - Lines 170-172: Remove `projectedTotal` fallback
  - Lines 216, 219-220: Remove `projectedTotal` extraction

---

## Phase 3: Exporter Modifications

### 3.1 Rewrite export_projected_points_data() Method
- **File**: `player-data-fetcher/player_data_exporter.py` (lines 521-632)
- **Remove**: `current_nfl_week` parameter
- **Remove**: File existence check and update logic
- **New implementation**:
  ```python
  async def export_projected_points_data(self, data: ProjectionData) -> str:
      """
      Export players_projected.csv with projection-only data.

      Creates file from scratch using statSourceId=1 projection values
      for ALL weeks 1-17. Does NOT require existing file.

      Args:
          data: ProjectionData containing player projections with projected_weeks populated

      Returns:
          str: Path to the created players_projected.csv file
      """
      try:
          projected_file_path = Path(__file__).parent.parent / "data" / "players_projected.csv"

          # Ensure directory exists
          projected_file_path.parent.mkdir(parents=True, exist_ok=True)

          # Build rows directly from ESPNPlayerData projected_weeks dictionary
          rows = []
          for player in data.players:
              row = {'id': player.id, 'name': player.name}
              for week in range(1, 18):
                  row[f'week_{week}_points'] = player.get_week_projected(week) or 0.0
              rows.append(row)

          df = pd.DataFrame(rows)

          # Write to CSV (full recreation)
          async with aiofiles.open(str(projected_file_path), mode='w', newline='', encoding='utf-8') as f:
              await f.write(df.to_csv(index=False))

          self.logger.info(f"Exported {len(df)} players to players_projected.csv (full recreation)")
          return str(projected_file_path)

      except Exception as e:
          self.logger.error(f"Error exporting players_projected.csv: {e}")
          raise
  ```

### 3.2 Update Method Call
- **File**: `player-data-fetcher/player_data_fetcher_main.py` (lines 354-357)
- **Current**: `await self.exporter.export_projected_points_data(data, self.settings.current_nfl_week)`
- **New**: `await self.exporter.export_projected_points_data(data)`

### 3.3 Historical Data Saving
- **Status**: NO CHANGES NEEDED (already includes players_projected.csv)

---

## Phase 4: Testing

### 4.1 Unit Tests for Model Changes
- **File**: `tests/player-data-fetcher/test_player_data_models.py`
- **Add new test class**: `TestESPNPlayerDataProjectedWeeks`

### 4.2 Unit Tests for ESPN Client Changes
- **File**: `tests/player-data-fetcher/test_espn_client.py`
- **Add tests for**: `source_type` parameter

### 4.3 Unit Tests for Exporter Changes
- **File**: `tests/player-data-fetcher/test_player_data_exporter.py`
- **Update/add tests for**: New `export_projected_points_data()` behavior

### 4.4 Unit Tests for Fantasy Points Calculator
- **File**: `tests/player-data-fetcher/test_fantasy_points_calculator.py`
- **Update tests** that reference `projectedTotal`

---

## Phase 5: Documentation Updates

### 5.1 Update Code Documentation
- All modified files get updated docstrings

### 5.2 Update Research Documents
- Update after implementation complete

---

## Phase 6: Final Validation

### 6.1 Run All Unit Tests
- **Command**: `python tests/run_all_tests.py`
- **Requirement**: 100% pass rate

### 6.2 Manual Verification
- Run `python run_player_fetcher.py`
- Check output files

### 6.3 Commit and Cleanup
- Move update files to `updates/done/`

---

## Verification Summary

**All 12 Iterations Complete**

### Files to Modify:
1. `player-data-fetcher/player_data_models.py` - Add projected_weeks dict and methods
2. `player-data-fetcher/espn_client.py` - Add source_type param, fix comments, remove projectedTotal
3. `player-data-fetcher/fantasy_points_calculator.py` - Remove projectedTotal references
4. `player-data-fetcher/player_data_exporter.py` - Rewrite export_projected_points_data()
5. `player-data-fetcher/player_data_fetcher_main.py` - Update method call

### Test Files to Update:
1. `tests/player-data-fetcher/test_player_data_models.py`
2. `tests/player-data-fetcher/test_espn_client.py`
3. `tests/player-data-fetcher/test_player_data_exporter.py`
4. `tests/player-data-fetcher/test_fantasy_points_calculator.py`

### Key Implementation Notes:
- Use `projected_weeks: Dict[int, float]` dictionary (not individual fields)
- Access ESPNPlayerData directly in exporter (skip FantasyPlayer)
- Keep smart fallback behavior for players.csv (per Q4 answer)
- Remove ALL `projectedTotal` references (field doesn't exist in ESPN API)

---

## Progress Tracking

### Completed:
- ✅ Draft TODO file
- ✅ Iterations 1-5 (First verification round)
- ✅ Questions file created
- ✅ User answers received
- ✅ Iterations 6-12 (Second verification round)
- ✅ TODO finalized with implementation details

### Ready For:
- Implementation
