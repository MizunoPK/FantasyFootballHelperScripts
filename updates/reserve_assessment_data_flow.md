# Reserve Assessment Mode - Data Flow Verification

**Purpose**: Trace complete data flow from user input to display output

**Date**: Iteration 8 - Verification Round 3

---

## End-to-End Data Flow

### 1. User Initiates Reserve Assessment Mode

**Entry Point**: `LeagueHelperManager.run()`
- User selects option "5" from main menu
- Calls `self._run_reserve_assessment_mode()`

**Data Available**:
- ✅ `self.config` (ConfigManager)
- ✅ `self.player_manager` (PlayerManager)
- ✅ `self.team_data_manager` (TeamDataManager)
- ✅ `self.season_schedule_manager` (SeasonScheduleManager)
- ✅ `self.data_folder` (Path)

---

### 2. Mode Manager Initialization

**Action**: `ReserveAssessmentModeManager.__init__()` called
```python
def __init__(self, config, player_manager, team_data_manager, season_schedule_manager, data_folder):
    self.config = config
    self.player_manager = player_manager
    self.team_data_manager = team_data_manager
    self.season_schedule_manager = season_schedule_manager
    self.data_folder = data_folder
    self.logger = get_logger()

    # Load historical data once at initialization
    self.historical_players_dict = self._load_historical_data()
```

**Data Loaded**:
- ✅ Historical players from `data_folder / 'last_season' / 'players.csv'`
- ✅ Stored in `{(name.lower(), position): FantasyPlayer}` dictionary
- ✅ Available for all subsequent operations

---

### 3. Interactive Mode Start

**Action**: `start_interactive_mode(player_manager, team_data_manager)` called
```python
def start_interactive_mode(self, player_manager, team_data_manager):
    # Update manager references (fresh data)
    self.set_managers(player_manager, team_data_manager)

    # Get recommendations
    recommendations = self.get_recommendations()

    # Display results
    # ... display logic ...
```

**Data Refreshed**:
- ✅ `player_manager` - fresh reference (in case data reloaded)
- ✅ `team_data_manager` - fresh reference

---

### 4. Get Recommendations Flow

**Action**: `get_recommendations() -> List[ScoredPlayer]`

#### Step 4.1: Get Undrafted Players
```python
undrafted_players = self.player_manager.get_player_list(drafted_vals=[0])
```
**Returns**: List[FantasyPlayer] where drafted=0

#### Step 4.2: Filter for HIGH Risk Injured Players
```python
high_risk_injured = [
    p for p in undrafted_players
    if p.get_risk_level() == "HIGH"  # INJURY_RESERVE, SUSPENSION, UNKNOWN
    and p.position not in ["K", "DST"]
    and p.fantasy_points > 0
]
```
**Returns**: Filtered list of IR candidates

#### Step 4.3: Match to Historical Data & Score
```python
scored_players = []
for current_player in high_risk_injured:
    # Match to historical data
    key = (current_player.name.lower(), current_player.position)
    historical_player = self.historical_players_dict.get(key)

    if historical_player is None:
        # Skip player (no historical data)
        self.logger.debug(f"No historical data for {current_player.name}")
        continue

    # Score the candidate
    scored_player = self._score_reserve_candidate(current_player, historical_player)
    scored_players.append(scored_player)
```

**Data Flow in Scoring**:
1. **current_player** provides: team, position, injury_status
2. **historical_player** provides: fantasy_points, player_rating, week_*_points
3. **self.config** provides: all multiplier methods
4. **self.team_data_manager** provides: team defense ranks
5. **self.season_schedule_manager** provides: future opponents

---

### 5. Scoring Algorithm Data Flow

**Action**: `_score_reserve_candidate(current_player, historical_player) -> ScoredPlayer`

#### 5.1: Normalization (Base Score)
```python
score = historical_player.fantasy_points  # e.g., 245.3
reasons = [f"Base: {score:.1f} pts (last season)"]
```
**Data Source**: ✅ historical_player.fantasy_points (from last_season/players.csv)

#### 5.2: Player Rating Multiplier
```python
if historical_player.player_rating:
    multiplier, rating = self.config.get_player_rating_multiplier(historical_player.player_rating)
    score *= multiplier
    reasons.append(f"Player Rating: {rating} ({multiplier:.2f}x)")
```
**Data Sources**:
- ✅ historical_player.player_rating (from last_season/players.csv)
- ✅ config.get_player_rating_multiplier() (from league_config.json)

#### 5.3: Team Quality Multiplier
```python
team_rank = self.team_data_manager.get_team_rank(current_player.team, current_player.position)
if team_rank:
    multiplier, rating = self.config.get_team_quality_multiplier(team_rank)
    score *= multiplier
    reasons.append(f"Team Quality: {rating} (rank {team_rank}, {multiplier:.2f}x)")
```
**Data Sources**:
- ✅ current_player.team (from current data/players.csv)
- ✅ current_player.position (from current data/players.csv)
- ✅ team_data_manager.get_team_rank() (from current data/teams_week_N.csv)
- ✅ config.get_team_quality_multiplier() (from league_config.json)

#### 5.4: Performance/Consistency Multiplier
```python
# Extract weekly points from historical data
weekly_points = []
for week in range(1, 18):
    week_attr = f'week_{week}_points'
    if hasattr(historical_player, week_attr):
        points = getattr(historical_player, week_attr)
        if points is not None and float(points) > 0:
            weekly_points.append(float(points))

if len(weekly_points) >= 3:
    mean_points = statistics.mean(weekly_points)
    std_dev = statistics.stdev(weekly_points) if len(weekly_points) > 1 else 0.0
    cv = std_dev / mean_points if mean_points > 0 else 0.0

    multiplier, rating = self.config.get_performance_multiplier(cv)
    score *= multiplier
    reasons.append(f"Performance: {rating} ({multiplier:.2f}x)")
```
**Data Sources**:
- ✅ historical_player.week_1_points through week_17_points (from last_season/players.csv)
- ✅ config.get_performance_multiplier() (from league_config.json)

#### 5.5: Schedule Multiplier
```python
schedule_value = self._calculate_schedule_value(current_player)
if schedule_value is not None:
    multiplier, rating = self.config.get_schedule_multiplier(schedule_value)
    score *= multiplier
    reasons.append(f"Schedule: {rating} (avg opp def rank: {schedule_value:.1f}, {multiplier:.2f}x)")
```
**Data Sources**:
- ✅ current_player.team (from current data/players.csv)
- ✅ season_schedule_manager.get_future_opponents() (from current data/season_schedule.csv)
- ✅ team_data_manager.get_team_defense_vs_position_rank() (from current data/teams_week_N.csv)
- ✅ config.get_schedule_multiplier() (from league_config.json)

#### 5.6: Return ScoredPlayer
```python
return ScoredPlayer(player=current_player, score=score, reason=reasons)
```
**Output**: ScoredPlayer object with final score and reasoning

---

### 6. Ranking and Filtering

**Action**: Sort and take top 15
```python
scored_players.sort(key=lambda sp: sp.score, reverse=True)
return scored_players[:15]
```

**Output**: Top 15 reserve candidates by potential value

---

### 7. Display Output

**Action**: Display recommendations to user
```python
print("\n" + "="*50)
print("RESERVE ASSESSMENT - High-Value Injured Players")
print("="*50)
print(f"\nFound {len(recommendations)} reserve candidates on injury reserve:")

for i, sp in enumerate(recommendations, 1):
    print(f"{i}. {sp}")  # ScoredPlayer.__str__() handles formatting

input("\nPress Enter to return to Main Menu...")
```

**Output**: User sees ranked list with scoring breakdown

---

## Data Source Summary

| Data Element | Source File | Load Time | Component |
|--------------|-------------|-----------|-----------|
| Current season players | data/players.csv | Startup | PlayerManager |
| Current team ranks | data/teams_week_N.csv | Startup | TeamDataManager |
| Current schedule | data/season_schedule.csv | Startup | SeasonScheduleManager |
| Historical players | data/last_season/players.csv | Mode init | ReserveAssessmentModeManager |
| Scoring config | data/league_config.json | Startup | ConfigManager |

---

## Dependency Chain Verification

✅ **All dependencies verified as available**:
1. LeagueHelperManager has all 5 managers initialized
2. ReserveAssessmentModeManager receives all needed managers
3. All scoring data sources exist and are accessible
4. All multiplier methods exist in ConfigManager
5. All team/schedule methods exist in respective managers

---

## Edge Cases Data Flow

### Case 1: Player has no historical data
**Flow**:
- Lookup in historical_players_dict returns None
- Player is skipped with debug log
- Does not appear in recommendations
- **No error, graceful skip** ✅

### Case 2: Player missing player_rating (historical)
**Flow**:
- Check `if historical_player.player_rating:` returns False
- Skip that multiplier, don't add to reasons
- Score continues with remaining multipliers
- **No error, partial scoring** ✅

### Case 3: Player has < 3 weeks of historical data
**Flow**:
- weekly_points list has < 3 elements
- Performance multiplier skipped
- Score continues with remaining multipliers
- **No error, partial scoring** ✅

### Case 4: Player has no future opponents (end of season)
**Flow**:
- get_future_opponents() returns empty list
- _calculate_schedule_value() returns None
- Schedule multiplier skipped
- Score continues with remaining multipliers
- **No error, partial scoring** ✅

### Case 5: No eligible players found
**Flow**:
- get_recommendations() returns empty list
- Display shows "No reserve candidates found."
- Returns to main menu
- **No error, informative message** ✅

---

## Verification Result

✅ **COMPLETE DATA FLOW VERIFIED**
- All data sources identified and confirmed to exist
- All dependencies available and accessible
- All edge cases handled gracefully
- No blocking issues or missing data paths
- Ready for implementation
