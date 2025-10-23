# Strength of Schedule Implementation TODO

## Overview
Implement position-specific team defense rankings and strength of schedule multiplier for player scoring.

**ESPN API Data Sources (100% VERIFIED)**:
- ✅ Player weekly stats available (statSourceId=0 = actual, statSourceId=1 = projected)
- ✅ Schedule data available (must iterate weeks 1-18)
- ❌ Position-specific defense NOT in API (must calculate ourselves)

**Progress Tracking**: Keep this file updated after each task. Mark tasks [x] when complete.

---

## PHASE 1: API Investigation ✅ COMPLETE

All questions answered. See `updates/espn_api_investigation_results.md` for details.

- [x] ESPN API does NOT provide position-specific defense
- [x] Must calculate def_vs_qb_rank, def_vs_rb_rank, etc. from player stats
- [x] Schedule requires 18 API calls (weeks 1-18)
- [x] User confirmed all configuration decisions

---

## PHASE 2: Update Player Data Fetcher to Calculate Position-Specific Defense

### Task 2.1: Add Position-Specific Defense Calculation Method
**File**: `player-data-fetcher/espn_client.py`
**Location**: Add new method around line 900 (after `_fetch_current_week_schedule`)

- [ ] Create method `_calculate_position_defense_rankings(players, schedule, current_week)`
- [ ] **Algorithm** (from ESPN investigation):
  ```python
  def _calculate_position_defense_rankings(self, players: List[ESPNPlayerData], schedule: Dict[str, str], current_week: int) -> Dict[str, Dict[str, int]]:
      """
      Calculate position-specific defense rankings for all teams.

      Args:
          players: List of all players with weekly stats (from ESPN API)
          schedule: Dict mapping {team: opponent} for current week
          current_week: Current NFL week (1-17)

      Returns:
          Dict[team, {'def_vs_qb_rank': int, 'def_vs_rb_rank': int, ...}]
          Rankings are 1-32 where 1 = best defense (fewest points allowed)
      """
      from collections import defaultdict

      # Track points allowed by each defense to each position
      defense_stats = defaultdict(lambda: defaultdict(float))

      # For each player, accumulate points scored against their opponents
      for player in players:
          # Get all opponents this team has faced (weeks 1 to current_week-1)
          for week in range(1, current_week):
              # Get week's opponent for player's team
              week_schedule = self._get_schedule_for_week(week)  # Need to implement
              opponent_defense = week_schedule.get(player.team)

              if not opponent_defense:
                  continue

              # Get player's actual points for this week (from ESPN data)
              week_points = player.get_week_points(week)

              # Only use actual stats (week_points will be None for future weeks)
              if week_points is None or week_points <= 0:
                  if player.position != 'DST':  # DST can have negative points
                      continue

              # Accumulate points allowed by opponent's defense
              if player.position == 'QB':
                  defense_stats[opponent_defense]['vs_qb'] += week_points
              elif player.position == 'RB':
                  defense_stats[opponent_defense]['vs_rb'] += week_points
              elif player.position == 'WR':
                  defense_stats[opponent_defense]['vs_wr'] += week_points
              elif player.position == 'TE':
                  defense_stats[opponent_defense]['vs_te'] += week_points
              elif player.position == 'K':
                  defense_stats[opponent_defense]['vs_k'] += week_points

      # Rank defenses for each position (lower points allowed = better rank)
      rankings = {}
      for position in ['vs_qb', 'vs_rb', 'vs_wr', 'vs_te', 'vs_k']:
          # Sort teams by total points allowed (ascending)
          sorted_teams = sorted(
              defense_stats.items(),
              key=lambda x: x[1][position]
          )

          # Assign ranks (1 = fewest points = best defense)
          for rank, (team, stats) in enumerate(sorted_teams, 1):
              if team not in rankings:
                  rankings[team] = {}
              rankings[team][f'def_{position}_rank'] = rank

      # Fill in neutral ranks (16) for teams with no data
      all_teams = ['ARI', 'ATL', 'BAL', 'BUF', 'CAR', ...]  # All 32 teams
      for team in all_teams:
          if team not in rankings:
              rankings[team] = {
                  'def_vs_qb_rank': 16,
                  'def_vs_rb_rank': 16,
                  'def_vs_wr_rank': 16,
                  'def_vs_te_rank': 16,
                  'def_vs_k_rank': 16
              }

      return rankings
  ```
- [ ] Add logging:
  - INFO: "Calculating position-specific defense rankings for week {week}"
  - INFO: "Calculated rankings for {count} teams across 5 positions"
  - DEBUG: Individual team rankings
- [ ] Handle early season (weeks 1-3): Use neutral rank (16) for all positions
- [ ] Handle missing data: Skip invalid week_points, log at DEBUG level

**Dependencies**: Requires schedule data for all past weeks (need to store in `_fetch_full_season_schedule`)

**Test**: `tests/player-data-fetcher/test_espn_client.py` - add test for calculation logic

### Task 2.2: Store Historical Schedule Data
**File**: `player-data-fetcher/espn_client.py`

- [ ] Modify `_fetch_current_week_schedule` to also store schedule in instance variable
- [ ] Add method `_fetch_full_season_schedule()` to get weeks 1-18:
  ```python
  async def _fetch_full_season_schedule(self) -> Dict[int, Dict[str, str]]:
      """
      Fetch complete season schedule for all weeks.

      Returns:
          Dict[week_number, Dict[team, opponent]]
          Example: {1: {'KC': 'BAL', 'BAL': 'KC', ...}, 2: {...}, ...}
      """
      full_schedule = {}

      for week in range(1, 19):  # Weeks 1-18
          self.logger.info(f"Fetching schedule for week {week}/18")

          url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
          params = {
              "seasontype": 2,  # Regular season
              "week": week,
              "dates": self.settings.season
          }

          data = await self._make_request("GET", url, params=params)
          week_schedule = {}
          events = data.get('events', [])

          for event in events:
              competitors = event['competitions'][0]['competitors']
              team1 = competitors[0]['team']['abbreviation']
              team2 = competitors[1]['team']['abbreviation']

              # Normalize team names
              team1 = 'WSH' if team1 == 'WAS' else team1
              team2 = 'WSH' if team2 == 'WAS' else team2

              week_schedule[team1] = team2
              week_schedule[team2] = team1

          full_schedule[week] = week_schedule

          # Rate limiting
          await asyncio.sleep(0.2)

      return full_schedule
  ```
- [ ] Store as `self.full_season_schedule` in `_parse_espn_data`
- [ ] Use in `_calculate_position_defense_rankings`

### Task 2.3: Update TeamData Model
**File**: `utils/TeamData.py`
**Location**: Lines 18-36 (TeamData class)

- [ ] Add new fields to TeamData dataclass:
  ```python
  @dataclass
  class TeamData:
      team: str
      offensive_rank: Optional[int] = None
      defensive_rank: Optional[int] = None
      opponent: Optional[str] = None  # ← KEEP FOR NOW (removed in Phase 3)

      # NEW: Position-specific defense rankings
      def_vs_qb_rank: Optional[int] = None
      def_vs_rb_rank: Optional[int] = None
      def_vs_wr_rank: Optional[int] = None
      def_vs_te_rank: Optional[int] = None
      def_vs_k_rank: Optional[int] = None
  ```
- [ ] Update `from_dict` method (line 38) to handle new fields:
  ```python
  def_vs_qb_rank=_safe_int_conversion(data.get('def_vs_qb_rank'), None),
  def_vs_rb_rank=_safe_int_conversion(data.get('def_vs_rb_rank'), None),
  def_vs_wr_rank=_safe_int_conversion(data.get('def_vs_wr_rank'), None),
  def_vs_te_rank=_safe_int_conversion(data.get('def_vs_te_rank'), None),
  def_vs_k_rank=_safe_int_conversion(data.get('def_vs_k_rank'), None)
  ```
- [ ] Update `to_dict` method (line 55) to include new fields
- [ ] Update `save_teams_to_csv` (line 230) column order:
  ```python
  df = df[['team', 'offensive_rank', 'defensive_rank', 'opponent',
           'def_vs_qb_rank', 'def_vs_rb_rank', 'def_vs_wr_rank',
           'def_vs_te_rank', 'def_vs_k_rank']]
  ```

**Test**: `tests/utils/test_TeamData.py` - update tests for new fields

### Task 2.4: Integrate Position Defense Calculation into Exporter
**File**: `player-data-fetcher/player_data_exporter.py`
**Location**: Around line 463 (`export_teams_csv`)

- [ ] Update `export_teams_csv` to pass position defense rankings:
  ```python
  # Extract team data with position-specific defense rankings
  teams = extract_teams_from_rankings(
      fantasy_players,
      self.team_rankings,  # Has offensive_rank, defensive_rank
      self.current_week_schedule,
      self.position_defense_rankings  # NEW parameter
  )
  ```
- [ ] Add `set_position_defense_rankings()` method to DataExporter:
  ```python
  def set_position_defense_rankings(self, rankings: dict):
      """Set position-specific defense rankings from ESPN client"""
      self.position_defense_rankings = rankings
      self.logger.info(f"Position defense rankings set for {len(rankings)} teams")
  ```
- [ ] Update `extract_teams_from_rankings` in utils/TeamData.py to accept and use position rankings

**File**: `utils/TeamData.py`
- [ ] Update `extract_teams_from_rankings` signature (line 189):
  ```python
  def extract_teams_from_rankings(
      players: List['FantasyPlayer'],
      team_rankings: dict,
      schedule_data: dict = None,
      position_defense_rankings: dict = None  # NEW
  ) -> List[TeamData]:
  ```
- [ ] Apply position rankings to TeamData objects:
  ```python
  position_ranks = position_defense_rankings.get(team, {}) if position_defense_rankings else {}

  team_data_map[team] = TeamData(
      team=team,
      offensive_rank=team_ranking_data.get('offensive_rank', None),
      defensive_rank=team_ranking_data.get('defensive_rank', None),
      opponent=opponent,
      def_vs_qb_rank=position_ranks.get('def_vs_qb_rank', None),
      def_vs_rb_rank=position_ranks.get('def_vs_rb_rank', None),
      def_vs_wr_rank=position_ranks.get('def_vs_wr_rank', None),
      def_vs_te_rank=position_ranks.get('def_vs_te_rank', None),
      def_vs_k_rank=position_ranks.get('def_vs_k_rank', None)
  )
  ```

### Task 2.5: Call Position Defense Calculation in Main Flow
**File**: `player-data-fetcher/player_data_fetcher_main.py`

- [ ] After fetching players, call position defense calculation:
  ```python
  # Fetch full season schedule
  full_schedule = await espn_client._fetch_full_season_schedule()

  # Calculate position-specific defense rankings
  position_defense_rankings = espn_client._calculate_position_defense_rankings(
      players=projection_data.players,
      schedule=full_schedule,
      current_week=CURRENT_NFL_WEEK
  )

  # Pass to exporter
  exporter.set_position_defense_rankings(position_defense_rankings)
  ```

### Task 2.6: Validation Checkpoint
- [ ] Run ALL unit tests: `python tests/run_all_tests.py`
- [ ] Verify 100% pass rate
- [ ] Manually test player fetcher: `python run_player_fetcher.py`
- [ ] Verify teams.csv has new columns with ranks
- [ ] Commit changes

---

## PHASE 3: Create Schedule Data Fetcher

### Task 3.1: Create ScheduleFetcher Script
**File**: `schedule-data-fetcher/ScheduleFetcher.py` (NEW FILE)

- [ ] Create directory: `schedule-data-fetcher/`
- [ ] Create main fetcher class (mirror PlayerDataFetcher structure):
  ```python
  """
  Schedule Data Fetcher

  Fetches complete NFL season schedule from ESPN API and exports to season_schedule.csv.
  Uses same async HTTP patterns as PlayerDataFetcher for consistency.
  """

  import asyncio
  from pathlib import Path
  import csv
  from utils.LoggingManager import setup_logger

  class ScheduleFetcher:
      def __init__(self, output_path: Path):
          self.output_path = output_path
          self.logger = setup_logger(name="ScheduleFetcher", level="INFO")

      async def fetch_full_schedule(self, season: int) -> Dict[int, Dict[str, str]]:
          """Fetch schedule for weeks 1-18"""
          # Same logic as espn_client._fetch_full_season_schedule
          pass

      def export_to_csv(self, schedule: Dict[int, Dict[str, str]]):
          """
          Export season_schedule.csv with schema:
          week,team,opponent
          1,KC,BAL
          1,BAL,KC
          5,KC,     # Bye week (empty opponent)
          """
          with open(self.output_path, 'w', newline='') as f:
              writer = csv.writer(f)
              writer.writerow(['week', 'team', 'opponent'])

              for week in sorted(schedule.keys()):
                  for team, opponent in sorted(schedule[week].items()):
                      opponent_str = opponent if opponent else ''
                      writer.writerow([week, team, opponent_str])
  ```
- [ ] Add error handling and logging (match PlayerDataFetcher patterns)
- [ ] Add rate limiting (0.2s between calls)

### Task 3.2: Create Run Script
**File**: `run_schedule_fetcher.py` (NEW FILE at root level)

- [ ] Create entry point:
  ```python
  """
  Run Schedule Data Fetcher

  Usage: python run_schedule_fetcher.py
  """

  import asyncio
  from pathlib import Path
  from schedule-data-fetcher.ScheduleFetcher import ScheduleFetcher
  from config import NFL_SEASON

  async def main():
      output_path = Path(__file__).parent / "data" / "season_schedule.csv"
      fetcher = ScheduleFetcher(output_path)

      schedule = await fetcher.fetch_full_schedule(NFL_SEASON)
      fetcher.export_to_csv(schedule)

      print(f"Schedule exported to {output_path}")

  if __name__ == "__main__":
      asyncio.run(main())
  ```

### Task 3.3: Create Tests
**File**: `tests/schedule-data-fetcher/test_ScheduleFetcher.py` (NEW FILE)

- [ ] Create test directory
- [ ] Add tests for schedule fetching (with mocked API)
- [ ] Add tests for CSV export
- [ ] Test bye week handling (empty opponent)

### Task 3.4: Validation Checkpoint
- [ ] Run ALL unit tests: `python tests/run_all_tests.py`
- [ ] Verify 100% pass rate
- [ ] Manually run: `python run_schedule_fetcher.py`
- [ ] Verify `data/season_schedule.csv` created with correct schema
- [ ] Commit changes

---

## PHASE 4: Create SeasonScheduleManager

### Task 4.1: Implement SeasonScheduleManager Class
**File**: `league_helper/util/SeasonScheduleManager.py` (NEW FILE)

- [ ] Create manager class:
  ```python
  """
  Season Schedule Manager

  Manages full season NFL schedule data from season_schedule.csv.
  Provides helper methods for looking up opponents and future games.
  """

  from pathlib import Path
  from typing import Optional, List, Dict
  from utils.LoggingManager import get_logger
  from utils.csv_utils import read_csv_with_validation

  class SeasonScheduleManager:
      def __init__(self, data_folder: Path):
          self.logger = get_logger()
          self.logger.debug("Initializing Season Schedule Manager")

          # Load season_schedule.csv
          self.schedule_file = data_folder / 'season_schedule.csv'
          self.schedule_cache: Dict[tuple, str] = {}  # {(team, week): opponent}

          try:
              self._load_schedule()
              self.logger.debug(f"Loaded {len(self.schedule_cache)} schedule entries")
          except FileNotFoundError:
              self.logger.warning(f"season_schedule.csv not found at {self.schedule_file}")
              self.schedule_cache = {}
          except Exception as e:
              self.logger.error(f"Error loading schedule: {e}")
              self.schedule_cache = {}

      def _load_schedule(self):
          """Load schedule from CSV into cache"""
          df = read_csv_with_validation(self.schedule_file, required_columns=['week', 'team', 'opponent'])

          for _, row in df.iterrows():
              week = int(row['week'])
              team = row['team']
              opponent = row['opponent']

              # Empty string = bye week
              opponent = opponent if opponent and opponent.strip() else None

              self.schedule_cache[(team, week)] = opponent

      def get_opponent(self, team: str, week: int) -> Optional[str]:
          """
          Get opponent for a team in a specific week.

          Returns:
              Opponent abbreviation or None (bye week or not found)
          """
          if week < 1 or week > 17:
              self.logger.debug(f"Invalid week number: {week}")
              return None

          opponent = self.schedule_cache.get((team, week))

          if opponent is None:
              self.logger.debug(f"No opponent found for {team} in week {week}")

          return opponent

      def get_future_opponents(self, team: str, current_week: int) -> List[str]:
          """
          Get list of future opponents (excluding bye weeks).

          Args:
              team: Team abbreviation
              current_week: Current NFL week

          Returns:
              List of opponent abbreviations for weeks current_week+1 through 17
              (excludes bye weeks)
          """
          future_opponents = []

          for week in range(current_week + 1, 18):  # Weeks current+1 to 17
              opponent = self.get_opponent(team, week)
              if opponent:  # Skip None (bye weeks)
                  future_opponents.append(opponent)

          return future_opponents

      def get_remaining_schedule(self, team: str, current_week: int) -> Dict[int, Optional[str]]:
          """
          Get remaining schedule including bye weeks.

          Returns:
              Dict mapping week -> opponent (None for bye weeks)
          """
          remaining = {}

          for week in range(current_week + 1, 18):
              remaining[week] = self.get_opponent(team, week)

          return remaining

      def is_schedule_available(self) -> bool:
          """Returns True if schedule data loaded successfully"""
          return len(self.schedule_cache) > 0
  ```
- [ ] Add type hints for all methods
- [ ] Add docstrings in Google style

### Task 4.2: Create Tests
**File**: `tests/league_helper/util/test_SeasonScheduleManager.py` (NEW FILE)

- [ ] Create test fixtures with mock season_schedule.csv
- [ ] Test loading schedule data
- [ ] Test `get_opponent` (various teams and weeks)
- [ ] Test `get_future_opponents` (excludes bye weeks)
- [ ] Test `get_remaining_schedule` (includes bye weeks)
- [ ] Test error handling (missing file, invalid week)

### Task 4.3: Validation Checkpoint
- [ ] Run ALL unit tests: `python tests/run_all_tests.py`
- [ ] Verify 100% pass rate
- [ ] Commit changes

---

## PHASE 5: Integrate SeasonScheduleManager into League Helper

### Task 5.1: Update LeagueHelperManager
**File**: `league_helper/LeagueHelperManager.py`
**Location**: Around line 78 (where managers are created)

- [ ] Create SeasonScheduleManager instance:
  ```python
  # Initialize managers
  self.team_data_manager = TeamDataManager(data_folder)
  self.season_schedule_manager = SeasonScheduleManager(data_folder)  # NEW
  self.player_manager = PlayerManager(data_folder, self.config, self.team_data_manager, self.season_schedule_manager)  # Updated
  ```

### Task 5.2: Update PlayerManager Constructor
**File**: `league_helper/util/PlayerManager.py`
**Location**: Line 81 (`__init__`)

- [ ] Add season_schedule_manager parameter:
  ```python
  def __init__(
      self,
      data_folder: Path,
      config: ConfigManager,
      team_data_manager: TeamDataManager,
      season_schedule_manager: SeasonScheduleManager  # NEW
  ) -> None:
      self.logger = get_logger()
      self.logger.debug("Initializing Player Manager")

      self.config = config
      self.team_data_manager = team_data_manager
      self.season_schedule_manager = season_schedule_manager  # Store
      self.projected_points_manager = ProjectedPointsManager(config)

      # Pass to scoring calculator (updated below)
      self.scoring_calculator = PlayerScoringCalculator(
          config,
          self.projected_points_manager,
          0.0,
          team_data_manager,  # NEW
          season_schedule_manager,  # NEW
          config.current_nfl_week  # NEW
      )
  ```
- [ ] Update docstring

### Task 5.3: Update PlayerScoringCalculator Constructor
**File**: `league_helper/util/player_scoring.py`
**Location**: Line 53 (`__init__`)

- [ ] Add parameters:
  ```python
  def __init__(
      self,
      config: ConfigManager,
      projected_points_manager: ProjectedPointsManager,
      max_projection: float,
      team_data_manager: TeamDataManager,  # NEW
      season_schedule_manager: SeasonScheduleManager,  # NEW
      current_nfl_week: int  # NEW
  ) -> None:
      self.config = config
      self.projected_points_manager = projected_points_manager
      self.max_projection = max_projection
      self.team_data_manager = team_data_manager  # Store
      self.season_schedule_manager = season_schedule_manager  # Store
      self.current_nfl_week = current_nfl_week  # Store
      self.logger = get_logger()
  ```
- [ ] Update all test files that create PlayerScoringCalculator

**Files to update**:
- `tests/league_helper/util/test_player_scoring.py` (line 131)
- `tests/league_helper/util/test_PlayerManager_scoring.py` (line 239)

### Task 5.4: Validation Checkpoint
- [ ] Run ALL unit tests: `python tests/run_all_tests.py`
- [ ] Fix any broken tests due to signature changes
- [ ] Verify 100% pass rate
- [ ] Commit changes

---

## PHASE 6: Update Matchup Scoring (Position-Specific Defense) ✅ COMPLETE

### Task 6.1: Add Helper Method to TeamDataManager ✅
**File**: `league_helper/util/TeamDataManager.py`
**Location**: Add around line 100 (after `get_team_defensive_rank`)

- [x] Add position-specific defense rank getter:
  ```python
  def get_team_defense_vs_position_rank(self, team: str, position: str) -> Optional[int]:
      """
      Get team's defense ranking against a specific position.

      Args:
          team: Team abbreviation
          position: Player position (QB, RB, WR, TE, K, DST, DEF, D/ST)

      Returns:
          Position-specific defense rank (1-32) or None if not found
      """
      team_data = self.team_data_cache.get(team)
      if not team_data:
          return None

      # Check if position is defense (use overall defensive rank)
      from constants import DEFENSE_POSITIONS
      if position in DEFENSE_POSITIONS:
          return team_data.defensive_rank

      # Return position-specific rank
      position_rank_map = {
          'QB': team_data.def_vs_qb_rank,
          'RB': team_data.def_vs_rb_rank,
          'WR': team_data.def_vs_wr_rank,
          'TE': team_data.def_vs_te_rank,
          'K': team_data.def_vs_k_rank
      }

      rank = position_rank_map.get(position)

      if rank is None:
          self.logger.warning(f"No position-specific defense rank for {team} vs {position}")

      return rank
  ```
- [x] Add docstring with examples

### Task 6.2: Update get_rank_difference Method ✅
**File**: `league_helper/util/TeamDataManager.py`
**Location**: Lines 155-231

- [x] Update signature to accept position:
  ```python
  def get_rank_difference(self, team: str, position: str) -> int:
      """
      Calculate matchup quality using position-specific defense rankings.

      Args:
          team: Offensive team abbreviation
          position: Player position (determines which defense rank to use)

      Returns:
          Rank difference: opponent_defense_rank - team_offense_rank
          (Positive = favorable matchup, Negative = tough matchup)
      """
      # Get opponent
      opponent = self.get_team_opponent(team)
      if not opponent:
          return 0

      # Get team's offensive rank
      team_off_rank = self.get_team_offensive_rank(team)
      if team_off_rank is None:
          return 0

      # Get opponent's position-specific defense rank
      opp_def_rank = self.get_team_defense_vs_position_rank(opponent, position)
      if opp_def_rank is None:
          return 0

      # Calculate rank difference
      rank_diff = opp_def_rank - team_off_rank

      self.logger.debug(
          f"Matchup for {team} {position}: "
          f"Off rank {team_off_rank} vs {opponent} Def rank {opp_def_rank} "
          f"= {rank_diff:+d}"
      )

      return rank_diff
  ```

### Task 6.3: Update PlayerManager to Pass Position ✅
**File**: `league_helper/util/PlayerManager.py`
**Location**: Lines 202-206 (where matchup_score is calculated)

- [x] Update matchup_score calculation:
  ```python
  # Calculate matchup score using position-specific defense
  player.matchup_score = self.team_data_manager.get_rank_difference(
      player.team,
      player.position  # Changed from is_def
  )
  ```

### Task 6.4: Update Tests ✅
**Files**:
- `tests/league_helper/util/test_TeamDataManager.py`
- `tests/league_helper/util/test_PlayerManager.py`

- [x] Update mock TeamData fixtures to include position-specific ranks
- [x] Test `get_team_defense_vs_position_rank` for each position
- [x] Test `get_rank_difference` with position parameter
- [x] Verify QB uses def_vs_qb_rank
- [x] Verify RB uses def_vs_rb_rank
- [x] Verify WR uses def_vs_wr_rank
- [x] Verify TE uses def_vs_te_rank
- [x] Verify K uses def_vs_k_rank
- [x] Verify DST uses overall defensive_rank

### Task 6.5: Validation Checkpoint ✅
- [x] Run ALL unit tests: `python tests/run_all_tests.py`
- [x] Verify 100% pass rate (1893/1893 tests passed)
- [ ] Commit changes

---

## PHASE 7: Implement Schedule Scoring Configuration

### Task 7.1: Add SCHEDULE_SCORING to league_config.json
**File**: `data/league_config.json`
**Location**: After MATCHUP_SCORING (around line 154)

- [ ] Add configuration:
  ```json
  "MATCHUP_SCORING": {
    ... existing ...
  },
  "SCHEDULE_SCORING": {
    "THRESHOLDS": {
      "BASE_POSITION": 16,
      "DIRECTION": "INCREASING",
      "STEPS": 8
    },
    "MULTIPLIERS": {
      "VERY_POOR": 0.95,
      "POOR": 0.975,
      "GOOD": 1.025,
      "EXCELLENT": 1.05
    },
    "WEIGHT": 1.0
  }
  ```
- [ ] **Explanation**:
  - BASE_POSITION: 16 = middle of 32 teams
  - DIRECTION: INCREASING = higher avg rank (worse defenses) = better for player
  - STEPS: 8 = roughly quarters of rankings (32/4)
  - MULTIPLIERS: Same pattern as ADP/Rating
  - WEIGHT: 1.0 = starting weight (will be optimized by simulation)

### Task 7.2: Update ConfigManager
**File**: `league_helper/util/ConfigManager.py`
**Location**: Add after `get_matchup_multiplier` (around line 270)

- [ ] Add property for schedule_scoring:
  ```python
  @property
  def schedule_scoring(self):
      return self.parameters.get(self.keys.SCHEDULE_SCORING, {})
  ```
- [ ] Add method (around line 280):
  ```python
  def get_schedule_multiplier(self, schedule_value):
      """
      Get schedule multiplier based on average future opponent defense rank.

      Args:
          schedule_value: Average defense rank of future opponents (1-32)
                         Higher rank = worse defenses = easier schedule = higher multiplier

      Returns:
          Tuple (multiplier, rating_label)
      """
      return self._get_multiplier(
          self.schedule_scoring,
          schedule_value,
          rising_thresholds=True  # Higher rank = better schedule
      )
  ```
- [ ] Update ConfigKeys class to add SCHEDULE_SCORING constant

### Task 7.3: Update Tests
**File**: `tests/league_helper/util/test_ConfigManager.py`

- [ ] Add tests for schedule multiplier
- [ ] Test various schedule values (1, 8, 16, 24, 32)
- [ ] Verify rising_thresholds behavior
- [ ] Test missing config handling

### Task 7.4: Validation Checkpoint
- [ ] Run ALL unit tests: `python tests/run_all_tests.py`
- [ ] Verify 100% pass rate
- [ ] Commit changes

---

## PHASE 8: Implement Schedule Scoring Logic

### Task 8.1: Add Schedule Calculation Method
**File**: `league_helper/util/player_scoring.py`
**Location**: Add around line 280 (before score_player method)

- [ ] Implement calculation:
  ```python
  def _calculate_schedule_value(self, player: FantasyPlayer) -> Optional[float]:
      """
      Calculate schedule strength value based on future opponents.

      **USER DECISION**: Minimum 2 future games required (Q6)
      **USER DECISION**: End of season returns None (Q7)

      Args:
          player: Player to calculate schedule for

      Returns:
          Average defense rank of future opponents (1-32)
          Higher rank = easier schedule (facing worse defenses)
          None if insufficient future games (< 2)
      """
      # Get future opponents
      future_opponents = self.season_schedule_manager.get_future_opponents(
          player.team,
          self.current_nfl_week
      )

      if not future_opponents:
          self.logger.debug(f"{player.name}: No future games (end of season)")
          return None

      # Get position-specific defense ranks for each opponent
      defense_ranks = []
      for opponent in future_opponents:
          rank = self.team_data_manager.get_team_defense_vs_position_rank(
              opponent,
              player.position
          )
          if rank is not None:
              defense_ranks.append(rank)

      # USER DECISION Q6: Require minimum 2 future games
      if len(defense_ranks) < 2:
          self.logger.debug(
              f"{player.name}: Insufficient future games ({len(defense_ranks)}) "
              f"for schedule calculation (minimum 2 required)"
          )
          return None

      # Calculate average defense rank
      avg_rank = sum(defense_ranks) / len(defense_ranks)

      self.logger.debug(
          f"{player.name} schedule: {len(defense_ranks)} future games, "
          f"avg defense rank: {avg_rank:.1f}"
      )

      return avg_rank
  ```

### Task 8.2: Add Schedule Multiplier Application Method
**File**: `league_helper/util/player_scoring.py`
**Location**: Add after `_apply_matchup_multiplier` (around line 420)

- [ ] Implement multiplier:
  ```python
  def _apply_schedule_multiplier(self, player: FantasyPlayer, player_score: float) -> Tuple[float, str]:
      """
      Apply schedule strength multiplier based on future opponent difficulty.

      Args:
          player: Player to score
          player_score: Current score before schedule adjustment

      Returns:
          Tuple (new_score, reason_string)
      """
      # Calculate schedule value
      schedule_value = self._calculate_schedule_value(player)

      if schedule_value is None:
          return player_score, ""

      # Get multiplier and rating
      multiplier, rating = self.config.get_schedule_multiplier(schedule_value)

      # Apply multiplier
      new_score = player_score * multiplier
      reason = f"Schedule: {rating} (avg opp def rank: {schedule_value:.1f})"

      self.logger.debug(
          f"{player.name}: Schedule multiplier {multiplier:.3f} "
          f"({schedule_value:.1f} avg rank) -> {player_score:.2f} to {new_score:.2f}"
      )

      return new_score, reason
  ```

### Task 8.3: Update score_player Method Signature
**File**: `league_helper/util/player_scoring.py`
**Location**: Line 284 (method signature)

**USER DECISION Q9**: schedule=True (ENABLED BY DEFAULT)

- [ ] Add schedule parameter:
  ```python
  def score_player(
      self,
      p: FantasyPlayer,
      team_roster: List[FantasyPlayer],
      use_weekly_projection=False,
      adp=False,
      player_rating=True,
      team_quality=True,
      performance=True,
      matchup=False,
      schedule=True,  # ← USER DECISION: Default TRUE (unlike adp/matchup)
      draft_round=-1,
      bye=True,
      injury=True,
      roster: Optional[List[FantasyPlayer]] = None
  ) -> ScoredPlayer:
  ```
- [ ] Update docstring to document schedule parameter

### Task 8.4: Integrate Schedule Multiplier into Scoring Pipeline
**File**: `league_helper/util/player_scoring.py`
**Location**: Inside score_player method (around line 340, after matchup)

- [ ] Add schedule multiplier step:
  ```python
  # Step 6: Matchup Multiplier (opponent strength)
  if matchup:
      player_score, reason = self._apply_matchup_multiplier(p, player_score)
      if reason:
          score_reasons.append(reason)

  # Step 7: Schedule Multiplier (future opponent difficulty) - NEW
  if schedule:
      player_score, reason = self._apply_schedule_multiplier(p, player_score)
      if reason:
          score_reasons.append(reason)

  # Step 8: Draft Order Bonus (was Step 7)
  ...
  ```
- [ ] Update step numbers in comments (7→8, 8→9, 9→10)

### Task 8.5: Update PlayerManager Wrapper
**File**: `league_helper/util/PlayerManager.py`
**Location**: Line 518 (score_player wrapper)

- [ ] Add schedule parameter:
  ```python
  def score_player(
      self,
      player: FantasyPlayer,
      draft_round=-1,
      use_weekly_projection=False,
      adp=False,
      player_rating=True,
      team_quality=True,
      performance=True,
      matchup=False,
      schedule=True,  # NEW: Default TRUE
      bye=True,
      injury=True
  ) -> ScoredPlayer:
      """Score a player using the 9-step algorithm (now 10 steps with schedule)"""
      return self.scoring_calculator.score_player(
          player,
          self.team.roster,
          use_weekly_projection=use_weekly_projection,
          adp=adp,
          player_rating=player_rating,
          team_quality=team_quality,
          performance=performance,
          matchup=matchup,
          schedule=schedule,  # Pass through
          draft_round=draft_round,
          bye=bye,
          injury=injury,
          roster=self.team.roster
      )
  ```

### Task 8.6: Add Tests
**File**: `tests/league_helper/util/test_player_scoring.py`

- [ ] Create mock SeasonScheduleManager fixture
- [ ] Create mock TeamDataManager with position-specific ranks
- [ ] Test `_calculate_schedule_value`:
  - Easy schedule (avg rank 25) = high value
  - Hard schedule (avg rank 5) = low value
  - No future games = None
  - < 2 future games = None
- [ ] Test `_apply_schedule_multiplier`:
  - Verify multiplier applied correctly
  - Verify reason string format
- [ ] Test score_player with schedule=True vs schedule=False

### Task 8.7: Validation Checkpoint
- [ ] Run ALL unit tests: `python tests/run_all_tests.py`
- [ ] Fix any broken tests
- [ ] Verify 100% pass rate
- [ ] Commit changes

---

## PHASE 9: Integrate Schedule Scoring into Add to Roster Mode

**USER DECISION Q8**: Enable schedule scoring for Add to Roster mode ✅

### Task 9.1: Verify Default Behavior
**File**: `league_helper/add_to_roster_mode/AddToRosterModeManager.py`
**Location**: Line 282 (score_player call)

- [ ] Verify current call (should already use schedule=True default):
  ```python
  scored_player = self.player_manager.score_player(
      player,
      draft_round=draft_round,
      adp=True,
      player_rating=True,
      team_quality=True,
      performance=True,
      matchup=True,
      # schedule=True is default, no need to specify
      bye=True,
      injury=True
  )
  ```
- [ ] **OPTIONAL**: Make explicit for clarity:
  ```python
  schedule=True,  # Explicitly enable schedule scoring
  ```

### Task 9.2: Update Tests
**File**: `tests/league_helper/add_to_roster_mode/test_AddToRosterModeManager.py`

- [ ] Verify schedule scoring is enabled in tests
- [ ] Add test that recommendations reflect schedule difficulty

### Task 9.3: Validation Checkpoint
- [ ] Run ALL unit tests: `python tests/run_all_tests.py`
- [ ] Verify 100% pass rate
- [ ] Manually test Add to Roster mode
- [ ] Commit changes

---

## PHASE 10: Integrate Schedule Scoring into Trade Modes

**USER DECISION Q8**: Enable schedule scoring for ALL Trade modes ✅

### Task 10.1: Update TradeSimTeam
**File**: `league_helper/trade_simulator_mode/TradeSimTeam.py`
**Location**: Lines 86, 89 (score_player calls)

- [ ] Verify/update opponent scoring (line 86):
  ```python
  scored_player = self.player_manager.score_player(
      player,
      player_rating=True,
      team_quality=True,
      performance=True,
      schedule=True  # Explicitly enable (or rely on default)
  )
  ```
- [ ] Verify/update user scoring (line 89):
  ```python
  scored_player = self.player_manager.score_player(
      player,
      player_rating=True,
      team_quality=True,
      performance=True,
      schedule=True  # Explicitly enable (or rely on default)
  )
  ```

### Task 10.2: Update trade_analyzer
**File**: `league_helper/trade_simulator_mode/trade_analyzer.py`
**Location**: Line 254 (score_player call)

- [ ] Verify/update scoring:
  ```python
  scored_player = self.player_manager.score_player(
      player,
      player_rating=True,
      team_quality=True,
      performance=True,
      schedule=True  # Explicitly enable (or rely on default)
  )
  ```

### Task 10.3: Update Tests
**Files**:
- `tests/league_helper/trade_simulator_mode/test_TradeSimTeam.py`
- `tests/league_helper/trade_simulator_mode/test_trade_analyzer.py`

- [ ] Update mock score_player calls to handle schedule parameter
- [ ] Add tests verifying schedule scoring is enabled

### Task 10.4: Validation Checkpoint
- [ ] Run ALL unit tests: `python tests/run_all_tests.py`
- [ ] Verify 100% pass rate
- [ ] Manually test Trade Simulator mode
- [ ] Commit changes

---

## PHASE 11: Disable Schedule Scoring in StarterHelperMode

**USER DECISION Q8**: Do NOT enable schedule scoring for StarterHelperMode ⚠️

**CRITICAL**: Since schedule=True is the new default, StarterHelperMode must EXPLICITLY set schedule=False

### Task 11.1: Update StarterHelperMode
**File**: `league_helper/starter_helper_mode/StarterHelperModeManager.py`
**Location**: Line 364 (score_player call)

- [ ] **EXPLICITLY disable** schedule scoring:
  ```python
  scored_player = self.player_manager.score_player(
      player,
      use_weekly_projection=True,  # Weekly lineup optimization
      schedule=False,  # EXPLICIT: No schedule scoring for weekly decisions
      matchup=True,  # Keep matchup scoring (current week opponent)
      performance=True,
      player_rating=True,
      team_quality=True,
      bye=True,
      injury=True
  )
  ```
- [ ] **Rationale**: StarterHelperMode focuses on THIS WEEK's lineup decisions
  - Matchup scoring (current week opponent) = RELEVANT ✅
  - Schedule scoring (future weeks) = NOT RELEVANT ❌
  - Must explicitly set schedule=False to override the new default

### Task 11.2: Update Tests
**File**: `tests/league_helper/starter_helper_mode/test_StarterHelperModeManager.py`

- [ ] Verify schedule=False is set in score_player calls
- [ ] Add test confirming schedule scoring is NOT applied
- [ ] Verify matchup scoring IS still applied (current week)

### Task 11.3: Validation Checkpoint
- [ ] Run ALL unit tests: `python tests/run_all_tests.py`
- [ ] Verify 100% pass rate
- [ ] Manually test Starter Helper mode
- [ ] Verify lineup recommendations don't consider future schedule
- [ ] Commit changes

---

## PHASE 12: Update Simulation System

**USER DECISION Q10**: Keep aligned with other patterns ✅

### Task 12.1: Add Schedule Scoring to ConfigGenerator
**File**: `simulation/ConfigGenerator.py`
**Location**: Find where ADP_SCORING and PLAYER_RATING_SCORING are generated

- [ ] Add SCHEDULE_SCORING parameter generation:
  ```python
  # Existing patterns:
  # ADP: STEPS=[20-50], WEIGHT=[0.5-3.0]
  # PLAYER_RATING: STEPS=[10-40], WEIGHT=[0.5-3.0]

  # NEW: SCHEDULE_SCORING
  SCHEDULE_STEPS_OPTIONS = [4, 6, 8, 10, 12]
  SCHEDULE_WEIGHT_OPTIONS = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]

  for steps in SCHEDULE_STEPS_OPTIONS:
      for weight in SCHEDULE_WEIGHT_OPTIONS:
          config['SCHEDULE_SCORING'] = {
              'THRESHOLDS': {
                  'BASE_POSITION': 16,  # Fixed
                  'DIRECTION': 'INCREASING',  # Fixed
                  'STEPS': steps
              },
              'MULTIPLIERS': {
                  'VERY_POOR': 0.95,
                  'POOR': 0.975,
                  'GOOD': 1.025,
                  'EXCELLENT': 1.05
              },
              'WEIGHT': weight
          }
          yield config
  ```

### Task 12.2: Update Simulation Tests
**File**: `tests/simulation/test_ConfigGenerator.py`

- [ ] Add tests for schedule parameter generation
- [ ] Verify schedule configs included in combinations

### Task 12.3: Update DraftHelperTeam and SimulatedOpponent
**Files**:
- `simulation/DraftHelperTeam.py`
- `simulation/SimulatedOpponent.py`

- [ ] Verify schedule scoring enabled during simulation
- [ ] Check that schedule flag is passed correctly

### Task 12.4: Validation Checkpoint
- [ ] Run ALL unit tests: `python tests/run_all_tests.py`
- [ ] Verify 100% pass rate
- [ ] Run small simulation test
- [ ] Commit changes

---

## PHASE 13: Remove 'opponent' Column from teams.csv

**NOTE**: This is done AFTER all other phases to avoid breaking changes

### Task 13.1: Update TeamData Model
**File**: `utils/TeamData.py`

- [ ] Remove opponent field from TeamData (line 35):
  ```python
  @dataclass
  class TeamData:
      team: str
      offensive_rank: Optional[int] = None
      defensive_rank: Optional[int] = None
      # opponent: Optional[str] = None  ← REMOVE THIS LINE

      # Position-specific defense rankings
      def_vs_qb_rank: Optional[int] = None
      ...
  ```
- [ ] Update from_dict (remove opponent line)
- [ ] Update to_dict (remove opponent line)
- [ ] Update save_teams_to_csv column order (remove opponent)

### Task 13.2: Update TeamDataManager
**File**: `league_helper/util/TeamDataManager.py`

- [ ] Update `get_team_opponent` to use SeasonScheduleManager:
  ```python
  def get_team_opponent(self, team: str) -> Optional[str]:
      """Get current week opponent from season schedule"""
      # Use SeasonScheduleManager instead of TeamData
      return self.season_schedule_manager.get_opponent(team, self.current_nfl_week)
  ```
- [ ] Add season_schedule_manager and current_nfl_week to __init__

### Task 13.3: Update Tests
- [ ] Update all mock TeamData to not include opponent
- [ ] Verify all tests still pass

### Task 13.4: Validation Checkpoint
- [ ] Run ALL unit tests: `python tests/run_all_tests.py`
- [ ] Verify 100% pass rate
- [ ] Commit changes

---

## PHASE 14: Documentation and Final Testing

### Task 14.1: Update README.md
**File**: `README.md`

- [ ] Document new features:
  - Position-specific defense rankings
  - Strength of schedule scoring
  - season_schedule.csv file
- [ ] Document updated teams.csv structure
- [ ] Document new script: run_schedule_fetcher.py
- [ ] Update usage examples

### Task 14.2: Update CLAUDE.md
**File**: `CLAUDE.md`

- [ ] Add SeasonScheduleManager to utilities section
- [ ] Add schedule-data-fetcher to project structure
- [ ] Update data files section
- [ ] Document schedule scoring workflow

### Task 14.3: Update ARCHITECTURE.md
**File**: `ARCHITECTURE.md`

- [ ] Document schedule scoring architecture
- [ ] Document SeasonScheduleManager design
- [ ] Update data flow diagrams

### Task 14.4: Final Comprehensive Testing
- [ ] Run ALL unit tests: `python tests/run_all_tests.py`
- [ ] Verify 100% pass rate (MANDATORY)
- [ ] Manually test all modes:
  - [ ] Add to Roster mode
  - [ ] Starter Helper mode (verify schedule=False)
  - [ ] Trade Simulator mode
  - [ ] Modify Player Data mode
- [ ] Test data fetchers:
  - [ ] `python run_player_fetcher.py`
  - [ ] `python run_schedule_fetcher.py`
  - [ ] Verify CSV outputs
- [ ] Test simulation: `python run_simulation.py`
- [ ] Verify schedule scoring impacts all modes correctly

### Task 14.5: Create Code Changes Documentation
**File**: `updates/strength_of_schedule_code_changes.md` (NEW)

- [ ] Document all file modifications
- [ ] Include before/after code snippets
- [ ] Document rationale for each change
- [ ] Include line numbers and file paths
- [ ] Verify files that were checked but not modified

### Task 14.6: Final Commit and Cleanup
- [ ] Final commit of documentation
- [ ] Review all changes: `git status`, `git diff`
- [ ] Ensure no debug code or TODOs remain
- [ ] Run requirement verification protocol (rules.txt)
- [ ] Move strength_of_schedule.txt to updates/done/
- [ ] Move strength_of_schedule_code_changes.md to updates/done/
- [ ] Delete strength_of_schedule_questions.md
- [ ] Delete strength_of_schedule_todo.md (this file)

---

## Summary of Changes

### New Files Created (7):
1. `schedule-data-fetcher/ScheduleFetcher.py`
2. `run_schedule_fetcher.py`
3. `league_helper/util/SeasonScheduleManager.py`
4. `data/season_schedule.csv`
5. `tests/schedule-data-fetcher/test_ScheduleFetcher.py`
6. `tests/league_helper/util/test_SeasonScheduleManager.py`
7. `updates/strength_of_schedule_code_changes.md`

### Files Modified (13):
1. `player-data-fetcher/espn_client.py`
2. `player-data-fetcher/player_data_exporter.py`
3. `player-data-fetcher/player_data_fetcher_main.py`
4. `utils/TeamData.py`
5. `league_helper/util/PlayerManager.py`
6. `league_helper/util/player_scoring.py`
7. `league_helper/util/ConfigManager.py`
8. `league_helper/util/TeamDataManager.py`
9. `league_helper/LeagueHelperManager.py`
10. `league_helper/starter_helper_mode/StarterHelperModeManager.py` (NEW - explicitly disable schedule)
11. `data/league_config.json`
12. `simulation/ConfigGenerator.py`
13. All test files (updated for new parameters)

### Data Schema Changes:
- **teams.csv**: Added 5 columns, removed opponent
- **season_schedule.csv**: New file with week, team, opponent

### Configuration Changes:
- **league_config.json**: Added SCHEDULE_SCORING section

---

## Verification Summary

**Total Verification Iterations**: 9 (6 initial + 3 additional)

**ESPN API Data Sources (VERIFIED)**:
- ✅ Player weekly stats: Available with statSourceId (0=actual, 1=projected)
- ✅ Schedule data: Available via scoreboard endpoint (18 calls needed)
- ❌ Position-specific defense: NOT in API, must calculate

**Data Models (VERIFIED)**:
- ✅ ESPNPlayerData has week_1_points through week_17_points
- ✅ FantasyPlayer has week_1_points through week_17_points
- ✅ TeamData structure confirmed

**Dependency Injection (VERIFIED)**:
- ✅ Complete chain: LeagueHelperManager → PlayerManager → PlayerScoringCalculator
- ✅ Injection points identified for SeasonScheduleManager

**Export Flow (VERIFIED)**:
- ✅ DataExporter writes to data/teams.csv via save_teams_to_csv
- ✅ extract_teams_from_rankings pattern confirmed

**Implementation Readiness**: ✅ ALL CLEAR
- ✅ All 20 requirements mapped to specific tasks
- ✅ All user answers integrated
- ✅ All code locations identified with line numbers
- ✅ All patterns researched and documented
- ✅ All dependencies validated
- ✅ No open questions remaining

**Ready to Begin Phase 2** ✅
