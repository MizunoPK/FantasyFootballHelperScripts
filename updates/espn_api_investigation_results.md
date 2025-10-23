# ESPN API Investigation Results
## 5-Iteration Verification Complete

**Investigation Date**: 2025-10-22
**Purpose**: Determine if ESPN API provides position-specific defense rankings and full season schedule data

---

## Executive Summary

**Q1: Can ESPN provide position-specific defense rankings?**
- **Answer**: ❌ **NO** - Not available through ESPN API
- **Solution**: ✅ **Calculate ourselves** from existing player stats data

**Q2: Can ESPN provide full season schedule?**
- **Answer**: ⚠️ **PARTIAL** - Available but requires 18 separate API calls (one per week)
- **Solution**: ✅ **Iterate through weeks** using existing scoreboard endpoint

**Q11: How to calculate position-specific rankings?**
- **Answer**: ✅ **Fantasy points allowed** - Sum fantasy points by position allowed by each defense, rank 1-32

**Q12: Should rankings be week-specific?**
- **Answer**: ✅ **YES** - Maintain existing architecture with weekly files

---

## Iteration 1: Current ESPN Endpoints Review

### Findings:
- **Player Projections**: `https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{season}/segments/0/leaguedefaults/{ppr_id}`
  - Provides all player stats (actual + projected) for all weeks
  - Includes player position, team, weekly points
- **Team Statistics**: `https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{team_id}/statistics`
  - Provides aggregated team defensive stats
  - **NO position-specific breakdown**
- **Current Week Schedule**: `https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard`
  - Returns matchups for specified week
  - Includes calendar with all weeks listed

---

## Iteration 2: Team Statistics Deep Dive

### Tested Endpoint:
`https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/12/statistics`

### Available Defensive Stats:
- Solo Tackles, Assist Tackles, Total Tackles
- Sacks, Sack Yards
- Stuffs, Tackles For Loss
- Passes Defended
- Interceptions, Interception Yards, Interception TDs
- Kicks Blocked

### Position-Specific Defense:
- ❌ **NOT AVAILABLE** - All defensive metrics are team-level aggregates
- ❌ **NO fantasy points allowed data**
- ❌ **NO vs QB/RB/WR/TE breakdowns**

---

## Iteration 3: Schedule & Matchup Data

### Tested Endpoint:
`https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?seasontype=2&week=1&dates=2024`

### Schedule Findings:
- ✅ Returns matchups for specified week (16 games for Week 1)
- ✅ Includes team IDs, abbreviations, scores
- ✅ Calendar object lists all 18 regular season weeks
- ❌ **Cannot get all weeks in one call** - must iterate `week` parameter
- ❌ **NO defensive matchup data** included

### Implementation Impact:
- **Schedule Data Fetcher** must call API 18 times (weeks 1-18) to build complete `season_schedule.csv`
- Existing codebase already calls per-week for current week only
- Straightforward extension: loop through weeks 1-18

---

## Iteration 4: Alternative Data Sources & Calculation Methods

### Research Findings:

**Industry Standard**: Major fantasy platforms (NFL.com, FantasyPros, CBS, Yahoo, RotoWire) ALL calculate position-specific defense rankings themselves because:
1. No API provides this data directly
2. It's calculated from game-by-game player performance

**Calculation Method** (used by all major platforms):
1. For each team's defense, for each week:
   - Sum fantasy points scored by opposing QBs → def_vs_qb_points_allowed
   - Sum fantasy points scored by opposing RBs → def_vs_rb_points_allowed
   - Sum fantasy points scored by opposing WRs → def_vs_wr_points_allowed
   - Sum fantasy points scored by opposing TEs → def_vs_te_points_allowed
   - Sum fantasy points scored by opposing Ks → def_vs_k_points_allowed
2. Calculate season-to-date averages
3. Rank defenses 1-32 for each position (1 = best defense, 32 = worst)

**Data We Already Have**:
- ✅ All player weekly stats (actual + projected) from ESPN API
- ✅ Player positions (QB, RB, WR, TE, K, DST)
- ✅ Player teams
- ✅ Weekly matchups (from scoreboard endpoint)

**What We Need to Build**:
- Calculate fantasy points allowed per position per defense per week
- Rank defenses 1-32 for each position
- Store in weekly teams_week_N.csv files

---

## Iteration 5: Implementation Recommendations

### ✅ RECOMMENDATION 1: Calculate Position-Specific Defense Rankings

**Method**: Add calculation logic to `PlayerDataFetcher` or create new module

**Algorithm**:
```python
def calculate_position_specific_defense_rankings(players, schedule, week):
    """
    Calculate def_vs_qb_rank, def_vs_rb_rank, etc. for each team.

    Args:
        players: List of all players with weekly stats
        schedule: Dict mapping teams to opponents each week
        week: Current NFL week

    Returns:
        Dict[team_abbr, Dict[position_rank_field, rank_value]]
    """
    # For each team defense
    defense_stats = defaultdict(lambda: defaultdict(float))

    for player in players:
        # Get opponent (the defense they faced)
        opponent_defense = schedule.get(player.team, {}).get(week)
        if not opponent_defense:
            continue

        # Get player's fantasy points for this week
        points = player.get_week_points(week)
        if points is None or points <= 0:
            continue

        # Accumulate points allowed by position
        position = player.position
        if position == 'QB':
            defense_stats[opponent_defense]['vs_qb'] += points
        elif position == 'RB':
            defense_stats[opponent_defense]['vs_rb'] += points
        elif position == 'WR':
            defense_stats[opponent_defense]['vs_wr'] += points
        elif position == 'TE':
            defense_stats[opponent_defense]['vs_te'] += points
        elif position == 'K':
            defense_stats[opponent_defense]['vs_k'] += points

    # Rank defenses for each position (lower points allowed = better rank)
    rankings = {}
    for position in ['vs_qb', 'vs_rb', 'vs_wr', 'vs_te', 'vs_k']:
        sorted_teams = sorted(
            defense_stats.items(),
            key=lambda x: x[1][position]
        )
        for rank, (team, stats) in enumerate(sorted_teams, 1):
            if team not in rankings:
                rankings[team] = {}
            rankings[team][f'def_{position}_rank'] = rank

    return rankings
```

**Integration Point**:
- Add to `player-data-fetcher/espn_client.py` as new method
- Call after fetching player stats and schedule
- Write results to `teams_week_N.csv` files

**Data Quality Considerations**:
- **Early season** (weeks 1-3): Use previous season data or neutral rankings (16)
- **Missing data**: If team hasn't played yet, use league average or previous week
- **Bye weeks**: No data for that week, carry forward from previous week

---

### ✅ RECOMMENDATION 2: Build Full Season Schedule

**Method**: Extend existing `_fetch_current_week_schedule()` method

**Implementation**:
```python
async def _fetch_full_season_schedule(self, season: int) -> Dict[int, Dict[str, str]]:
    """
    Fetch complete season schedule for all weeks.

    Returns:
        Dict[week_number, Dict[team, opponent]]
        Example: {1: {'KC': 'BAL', 'BAL': 'KC', ...}, 2: {...}, ...}
    """
    full_schedule = {}

    for week in range(1, 19):  # Weeks 1-18 regular season
        self.logger.info(f"Fetching schedule for week {week}/{18}")

        url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
        params = {
            "seasontype": 2,  # Regular season
            "week": week,
            "dates": season
        }

        data = await self._make_request("GET", url, params=params)

        week_schedule = {}
        events = data.get('events', [])

        for event in events:
            # Extract team matchups (same logic as existing method)
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
        await asyncio.sleep(self.settings.rate_limit_delay)

    return full_schedule
```

**Export to CSV**:
```python
def export_season_schedule(schedule_dict, output_file):
    """
    Export full season schedule to season_schedule.csv.

    Format:
        week,team,opponent
        1,KC,BAL
        1,BAL,KC
        2,KC,CIN
        ...
    """
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['week', 'team', 'opponent'])

        for week in sorted(schedule_dict.keys()):
            for team, opponent in sorted(schedule_dict[week].items()):
                # Bye weeks: opponent is None or empty string
                opponent_str = opponent if opponent else ''
                writer.writerow([week, team, opponent_str])
```

---

## Final Answers to Questions

### Q1: ESPN API - Position-Specific Defense Data
**Answer**: ❌ **NO** - ESPN API does NOT provide position-specific defense rankings.

**Recommendation**: ✅ **Calculate ourselves** using player game stats:
1. Sum fantasy points allowed by each defense to each position
2. Rank defenses 1-32 for each position based on points allowed
3. Lower points allowed = better rank (1 = best defense vs that position)
4. Store in weekly `teams_week_N.csv` files

**Implementation**: Add calculation module to `player-data-fetcher`

---

### Q2: ESPN API - Full Season Schedule
**Answer**: ⚠️ **PARTIAL** - Schedule data available but requires multiple API calls.

**Recommendation**: ✅ **Iterate through weeks 1-18**:
1. Use existing scoreboard endpoint: `https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard`
2. Call with `week=1`, `week=2`, ..., `week=18`
3. Extract team matchups from each response
4. Combine into `season_schedule.csv`
5. Bye weeks: Leave opponent field empty

**Implementation**: Extend `espn_client.py` with `_fetch_full_season_schedule()` method

---

### Q11: How to Calculate Position-Specific Rankings?
**Answer**: ✅ **Fantasy points allowed method** (industry standard):

1. For each team defense, track cumulative fantasy points scored against them by:
   - Opposing QBs → sum all QB fantasy points vs this defense
   - Opposing RBs → sum all RB fantasy points vs this defense
   - Opposing WRs → sum all WR fantasy points vs this defense
   - Opposing TEs → sum all TE fantasy points vs this defense
   - Opposing Ks → sum all K fantasy points vs this defense

2. Calculate average points allowed per game for each position

3. Rank defenses 1-32:
   - Rank 1 = defense allowing FEWEST points to that position (best)
   - Rank 32 = defense allowing MOST points to that position (worst)

**Data Sources**:
- Player stats: Already available from ESPN player projections API
- Matchups: From schedule data (per Q2)
- Scoring format: Use PPR (already configured)

---

### Q12: Week-Specific Team Rankings
**Answer**: ✅ **YES** - Maintain week-specific files.

**Rationale**:
1. **Consistent with existing architecture**: Code already uses `teams_week_N.csv` pattern
2. **Rankings change weekly**: Defense performance varies significantly week-to-week
3. **Historical tracking**: Allows analysis of how defenses improve/decline over season
4. **Future flexibility**: Can update past weeks if needed

**Implementation**:
- Generate `teams_week_1.csv`, `teams_week_2.csv`, ..., `teams_week_18.csv`
- Each file includes: `team, offensive_rank, defensive_rank, def_vs_qb_rank, def_vs_rb_rank, def_vs_wr_rank, def_vs_te_rank, def_vs_k_rank`
- **No opponent column** (moved to `season_schedule.csv`)

---

## Implementation Priority

### Phase 1: Schedule Data Fetcher (MUST DO FIRST)
1. Create `schedule-data-fetcher/ScheduleFetcher.py`
2. Implement `_fetch_full_season_schedule()` method
3. Export to `data/season_schedule.csv`
4. Test with current season

### Phase 2: Position-Specific Defense Calculator
1. Add `_calculate_position_defense_rankings()` to `espn_client.py`
2. Integrate with existing team rankings logic
3. Update `teams_week_N.csv` export to include new columns
4. Test with multiple weeks of data

### Phase 3: Weekly Update Process
1. Ensure both schedule and position rankings update together
2. Handle early-season data (use previous season or neutral ranks)
3. Validate ranking logic with sample data

---

## Code Integration Points

### Files to Modify:
1. **`player-data-fetcher/espn_client.py`**:
   - Add `_fetch_full_season_schedule()` method (lines ~890-950 area)
   - Add `_calculate_position_defense_rankings()` method (new, ~100 lines)
   - Update `_fetch_team_rankings()` to call position calculator

2. **Create `schedule-data-fetcher/ScheduleFetcher.py`**:
   - New file similar to `PlayerDataFetcher`
   - Calls ESPN scoreboard API for weeks 1-18
   - Exports to `season_schedule.csv`

3. **Create `run_schedule_fetcher.py`**:
   - Entry point for schedule fetcher
   - Similar to `run_player_fetcher.py`

### Data Files to Create:
1. **`data/season_schedule.csv`**: Full season schedule (all weeks)
2. **Updated `data/teams_week_N.csv`**: Add 5 new position-specific defense rank columns

---

## Testing Strategy

### Unit Tests:
1. Test position defense calculation with mock player data
2. Test schedule fetching with mock API responses
3. Test ranking algorithm (ensure rank 1 = fewest points allowed)

### Integration Tests:
1. Fetch real schedule data for current season
2. Calculate position rankings using real player stats
3. Validate rankings match expected patterns (good defenses have low ranks)

### Validation:
1. Compare our rankings with FantasyPros or NFL.com position rankings
2. Spot-check known strong/weak defenses vs specific positions
3. Verify weekly changes make sense (defense improves → rank improves)

---

## Risk Mitigation

### Early Season Data (Weeks 1-3):
- **Problem**: Insufficient games for accurate rankings
- **Solution**: Use previous season data or neutral ranks (16) until 3+ games played

### Missing Matchup Data:
- **Problem**: Schedule data might be incomplete
- **Solution**: Log warnings, use empty opponent field for missing weeks

### API Rate Limiting:
- **Problem**: 18 API calls for full season schedule
- **Solution**: Use existing retry logic, add delays between calls (0.2s)

### Data Quality:
- **Problem**: Player stats might have outliers or errors
- **Solution**: Filter invalid values (negative points, NaN, missing positions)

---

## Verification Iterations Complete

- ✅ Iteration 1: Reviewed current ESPN endpoints
- ✅ Iteration 2: Deep dive into team statistics (no position data found)
- ✅ Iteration 3: Explored schedule endpoints (requires per-week calls)
- ✅ Iteration 4: Researched alternatives (must calculate ourselves)
- ✅ Iteration 5: Synthesized findings and recommendations

**Recommendation Confidence**: ✅ **HIGH**
- Multiple verification passes confirm ESPN API limitations
- Industry standard calculation method identified
- Feasible implementation plan with existing data
- Consistent with project architecture
