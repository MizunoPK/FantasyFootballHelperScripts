# Code Review Report - Feature 02

**Created:** 2026-01-03 (Stage 5b - Phase 1 - Task 6)
**Reviewer:** AI Agent (Stage 5b Implementation)
**Purpose:** Line-by-line verification of Accuracy Sim JSON loading implementation

---

## Method 1: _create_player_manager() (Lines 339-404)

### Code Review

**Lines 339-344: Method Signature**
```python
def _create_player_manager(
    self,
    config_dict: dict,
    week_data_path: Path,
    season_path: Path
) -> PlayerManager:
```
✅ **CORRECT** - Signature matches spec.md Algorithm 1

**Lines 359-363: Temp Directory Creation**
```python
temp_dir = Path(tempfile.mkdtemp(prefix="accuracy_sim_"))

# Create player_data subfolder for JSON files
player_data_dir = temp_dir / "player_data"
player_data_dir.mkdir(exist_ok=True)
```
✅ **CORRECT** - Creates temp directory with player_data/ subfolder (spec Algorithm 1 steps 1-2)

**Lines 365-373: JSON File Copying**
```python
# Copy 6 position JSON files from week folder to player_data/
position_files = ['qb_data.json', 'rb_data.json', 'wr_data.json',
                  'te_data.json', 'k_data.json', 'dst_data.json']
for filename in position_files:
    source_file = week_data_path / filename
    if source_file.exists():
        shutil.copy(source_file, player_data_dir / filename)
    else:
        self.logger.warning(f"Missing position file: {filename} in {week_data_path}")
```
✅ **CORRECT** - Copies all 6 position files (spec Algorithm 1 step 3)
✅ **CORRECT** - Handles missing files with warning (spec Edge Case 1)

**Lines 375-388: Season Data Copying**
```python
# Copy season_schedule.csv from season folder
season_schedule = season_path / "season_schedule.csv"
if season_schedule.exists():
    shutil.copy(season_schedule, temp_dir / "season_schedule.csv")

# Copy game_data.csv from season folder if exists
game_data = season_path / "game_data.csv"
if game_data.exists():
    shutil.copy(game_data, temp_dir / "game_data.csv")

# Copy team_data folder from season folder
team_data_source = season_path / "team_data"
if team_data_source.exists():
    shutil.copytree(team_data_source, temp_dir / "team_data")
```
✅ **CORRECT** - Copies season files (spec Algorithm 1 steps 4-6)

**Lines 390-393: Config File Creation**
```python
# Write config
config_path = temp_dir / "league_config.json"
with open(config_path, 'w') as f:
    json.dump(config_dict, f, indent=2)
```
✅ **CORRECT** - Writes config to temp directory (spec Algorithm 1 step 7)

**Lines 395-399: Manager Instantiation**
```python
# Create managers
config_mgr = ConfigManager(temp_dir)
schedule_mgr = SeasonScheduleManager(temp_dir)
team_data_mgr = TeamDataManager(temp_dir, config_mgr, schedule_mgr, config_mgr.current_nfl_week)
player_mgr = PlayerManager(temp_dir, config_mgr, team_data_mgr, schedule_mgr)
```
✅ **CORRECT** - Creates all required managers (spec Algorithm 1 step 8)
✅ **CORRECT** - PlayerManager will automatically call load_players_from_json() during __init__

**Lines 401-404: Temp Directory Storage & Return**
```python
# Store temp_dir for cleanup
player_mgr._temp_dir = temp_dir

return player_mgr
```
✅ **CORRECT** - Stores temp_dir for cleanup (spec Algorithm 1 step 9)
✅ **CORRECT** - Returns PlayerManager (spec Algorithm 1 step 10)

### Method 1 Verdict: ✅ PASS

**Findings:**
- All 10 algorithm steps implemented correctly
- Edge case handling present (missing file warnings)
- PlayerManager integration correct (delegation pattern)
- Temp directory cleanup mechanism in place

---

## Method 2: _load_season_data() (Lines 293-337)

### Code Review

**Lines 293-297: Method Signature**
```python
def _load_season_data(
    self,
    season_path: Path,
    week_num: int
) -> Tuple[Optional[Path], Optional[Path]]:
```
✅ **CORRECT** - Signature matches spec.md Algorithm 2

**Lines 318-323: Folder Path Calculation**
```python
# Week N folder for projections
projected_folder = season_path / "weeks" / f"week_{week_num:02d}"

# Week N+1 folder for actuals
# For week 1: use week_02, for week 17: use week_18
actual_week_num = week_num + 1
actual_folder = season_path / "weeks" / f"week_{actual_week_num:02d}"
```
✅ **CORRECT** - Calculates week_N and week_N+1 paths (spec Algorithm 2 steps 2-4)
✅ **CORRECT** - Week 17 → week_18 logic correct (17 + 1 = 18)

**Lines 326-328: Projected Folder Check**
```python
# Both folders must exist
if not projected_folder.exists():
    self.logger.warning(f"Projected folder not found: {projected_folder}")
    return None, None
```
✅ **CORRECT** - Checks projected folder exists (spec Algorithm 2 step 5)

**Lines 330-335: Actual Folder Check**
```python
if not actual_folder.exists():
    self.logger.warning(
        f"Actual folder not found: {actual_folder} "
        f"(needed for week {week_num} actuals)"
    )
    return None, None
```
⚠️ **NEEDS UPDATE** - Currently returns (None, None) when actual folder missing
📝 **Action Required:** Task 11 will change to return (projected_folder, projected_folder) for fallback (Requirement 7 alignment)

**Line 337: Return Statement**
```python
return projected_folder, actual_folder
```
✅ **CORRECT** - Returns tuple of paths (spec Algorithm 2 step 7)

### Method 2 Verdict: ⚠️ NEEDS UPDATE (Task 11)

**Findings:**
- Week_N+1 logic correct (lines 318-323)
- Week 17 → week_18 logic correct
- **Edge case handling needs alignment with Win Rate Sim** (Task 11 will fix)
- Current behavior: Skip week if actual folder missing
- Required behavior: Fallback to projected folder (align with Feature 01)

---

## Method 3: _evaluate_config_weekly() (Lines 412-533)

### Code Review

**Lines 412-416: Method Signature**
```python
def _evaluate_config_weekly(
    self,
    config_dict: dict,
    week_range: Tuple[int, int]
) -> AccuracyResult:
```
✅ **CORRECT** - Signature matches spec.md Algorithm 3

**Lines 435-445: Week Loop & Two-Manager Pattern**
```python
for week_num in range(start_week, end_week + 1):
    projected_path, actual_path = self._load_season_data(season_path, week_num)
    if not projected_path or not actual_path:
        # Skip if either folder missing
        continue

    # Create TWO player managers:
    # 1. projected_mgr (from week_N folder) for projections
    # 2. actual_mgr (from week_N+1 folder) for actuals
    projected_mgr = self._create_player_manager(config_dict, projected_path, season_path)
    actual_mgr = self._create_player_manager(config_dict, actual_path, season_path)
```
✅ **CORRECT** - Loops through weeks (spec Algorithm 3 step 2a)
✅ **CORRECT** - Creates two PlayerManagers per week (spec Algorithm 3 steps 2a.iii-iv)
✅ **CORRECT** - projected_mgr from week_N, actual_mgr from week_N+1

**Lines 447-478: Projection Calculation**
```python
try:
    projections = {}
    actuals = {}
    player_data = []  # Player metadata for ranking metrics

    # Calculate and set max weekly projection for this week's normalization
    # This is required before scoring with use_weekly_projection=True
    max_weekly = projected_mgr.calculate_max_weekly_projection(week_num)
    projected_mgr.scoring_calculator.max_weekly_projection = max_weekly

    # Get projections from week_N folder (projected_mgr)
    for player in projected_mgr.players:
        # Get scored player with projected points
        # Use same flags as StarterHelperModeManager with
        # use_weekly_projection=True for weekly projections
        scored = projected_mgr.score_player(
            player,
            use_weekly_projection=True,  # Weekly projection
            adp=False,
            player_rating=False,
            team_quality=True,
            performance=True,
            matchup=True,
            schedule=False,
            bye=False,
            injury=False,
            temperature=True,
            wind=True,
            location=True
        )
        if scored:
            projections[player.id] = scored.projected_points
```
✅ **CORRECT** - Calculates projections from projected_mgr (spec Algorithm 3 step 2a.v)
✅ **CORRECT** - Uses score_player() for projection calculation (not direct array access)

**Lines 480-497: Actual Extraction**
```python
    # Get actuals from week_N+1 folder (actual_mgr)
    # week_N+1 has actual_points[N-1] populated (week N complete)
    for player in actual_mgr.players:
        # Get actual points for this specific week (from actual_points array)
        # Array index: week 1 = index 0, week N = index N-1
        if 1 <= week_num <= 17 and len(player.actual_points) >= week_num:
            actual = player.actual_points[week_num - 1]
            if actual is not None and actual > 0:
                actuals[player.id] = actual

                # Match with projection by player ID
                if player.id in projections:
                    player_data.append({
                        'name': player.name,
                        'position': player.position,
                        'projected': projections[player.id],
                        'actual': actual
                    })
```
✅ **CORRECT** - Extracts actuals from actual_mgr (spec Algorithm 3 step 2a.v)
✅ **CORRECT** - Array indexing: `actual_points[week_num - 1]` (spec Requirement 5)
⚠️ **NEEDS UPDATE** - Array bounds check at line 485 (Task 11 will change to default 0.0)
⚠️ **NEEDS UPDATE** - Null check at line 487 may exclude valid 0.0 values (Task 11 alignment)

**Lines 499-505: Storage & Cleanup**
```python
    week_projections[week_num] = projections
    week_actuals[week_num] = actuals
    player_data_by_week[week_num] = player_data

finally:
    self._cleanup_player_manager(projected_mgr)
    self._cleanup_player_manager(actual_mgr)
```
✅ **CORRECT** - Stores projections/actuals (spec Algorithm 3 step 2a.v)
✅ **CORRECT** - Cleanup in finally block (spec Algorithm 3 step 2a.v Finally)

**Lines 507-533: MAE Calculation & Aggregation**
```python
# Calculate MAE for this season's week range
result = self.accuracy_calculator.calculate_weekly_mae(
    week_projections, week_actuals, week_range
)

# Calculate ranking metrics for this season
overall_metrics, by_position = self.accuracy_calculator.calculate_ranking_metrics_for_season(player_data_by_week)
result.overall_metrics = overall_metrics
result.by_position = by_position
...
# Aggregate across seasons (including ranking metrics)
return self.accuracy_calculator.aggregate_season_results(season_results)
```
✅ **CORRECT** - Calculates MAE (spec Algorithm 3 step 2b)
✅ **CORRECT** - Aggregates across seasons (spec Algorithm 3 steps 3-4)

### Method 3 Verdict: ⚠️ NEEDS UPDATE (Task 11)

**Findings:**
- Two-manager pattern correct
- Projection calculation correct (via score_player)
- Array indexing correct (`[week_num - 1]`)
- **Array bounds handling needs alignment** (Task 11 will fix)
- **Null/zero handling may need adjustment** (Task 11 will align)
- Cleanup logic correct (finally block)

---

## Overall Code Review Summary

### Methods Reviewed: 3/3

| Method | Status | Issues Found | Action Required |
|--------|--------|--------------|-----------------|
| `_create_player_manager()` | ✅ PASS | None | None |
| `_load_season_data()` | ⚠️ NEEDS UPDATE | Missing folder fallback | Task 11 |
| `_evaluate_config_weekly()` | ⚠️ NEEDS UPDATE | Array bounds handling | Task 11 |

### Key Findings

**✅ Working Correctly:**
1. PlayerManager integration (temp directory pattern)
2. JSON file copying (6 position files)
3. Week_N+1 logic (week_N for projected, week_N+1 for actual)
4. Week 17 logic (uses week_17 + week_18)
5. Two-manager pattern (projected_mgr + actual_mgr)
6. Array indexing (`[week_num - 1]`)
7. Cleanup mechanism (finally block)

**⚠️ Needs Alignment (Task 11):**
1. Missing week_N+1 folder behavior:
   - Current: Return (None, None), skip week
   - Required: Return (projected, projected), use fallback
   - Location: _load_season_data() lines 330-335

2. Array bounds handling:
   - Current: Check length, skip player if too short
   - Required: Default to 0.0 if too short, include player
   - Location: _evaluate_config_weekly() line 485

### Code Review Result: ⚠️ PARTIAL PASS

**Verdict:**
- Core implementation is **CORRECT** ✅
- Edge case handling needs **ALIGNMENT** with Win Rate Sim (Task 11)
- No critical bugs found
- No architectural issues
- PlayerManager integration working as designed

**Next Steps:**
1. ✅ Complete Task 6 (Code Review) - DONE
2. Proceed to Task 7 (Manual Testing)
3. Proceed to Task 11 (Edge Case Alignment)

---

## Task 6 Completion

**Acceptance Criteria Review:**
- [x] Line-by-line review of `_create_player_manager()` (lines 339-404)
- [x] Line-by-line review of `_load_season_data()` (lines 293-337)
- [x] Line-by-line review of `_evaluate_config_weekly()` (lines 412-533)
- [x] Verify JSON file copying logic correct ✅
- [x] Verify PlayerManager integration correct ✅
- [x] Verify array extraction logic correct ✅
- [x] Verify temp directory cleanup logic correct ✅
- [x] Document all findings in verification report ✅ (this document)
- [x] Confirm: PlayerManager correctly loads JSON in simulation context ✅

**Task 6 Status:** ✅ COMPLETE

**Findings:** Implementation is fundamentally correct. Edge case alignment (Task 11) will finalize compatibility with Win Rate Sim.
