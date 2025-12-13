# ESPN API Response Examples

This folder contains real ESPN API response examples collected on **2025-12-13** for documentation purposes.

> **Last Verified**: 2025-12-13 - All examples freshly collected from live API endpoints.

## ⚠️ Important Notes

- These are **example responses** - actual data from ESPN API may vary
- ESPN API is **unofficial** and response structures may change without notice
- Examples have been trimmed/sanitized for documentation (limited to 3-4 entries per response)
- Some optional fields may not be present in all responses
- Use these examples as reference only, not as guaranteed API contracts

## Example Files

### `player_projection_response.json`
**Endpoint**: Player Projections (Season)
**URL**: `https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/2025/segments/0/leaguedefaults/3`
**Description**: Contains season projections for top 3 players by ownership percentage
**Use Case**: Understanding player data structure, basic player information, season statistics

**Key Fields**:
- `players[]` - Array of player objects
- `players[].player` - Player information (id, name, position, team, etc.)
- `players[].player.stats[]` - Statistics array with projections and actuals
- `players[].player.ownership` - ADP and ownership data
- `players[].player.draftRanksByRankType` - Draft rankings by scoring format

### `player_weekly_data_response.json`
**Endpoint**: Player Weekly Data
**URL**: Same as above with `scoringPeriodId=0`
**Description**: Complete weekly breakdown for a specific player (all weeks 1-18)
**Use Case**: Understanding week-by-week projections, stats array structure, statSourceId meanings

**Key Fields**:
- `players[0].player.stats[]` - Multiple entries per week (actual vs projected)
- `stats[].scoringPeriodId` - Week number (1-18)
- `stats[].statSourceId` - 0=actual results, 1=projections
- `stats[].appliedTotal` - Fantasy points (used for BOTH actual and projected)

> **⚠️ NOTE**: `projectedTotal` is deprecated. ESPN now uses `appliedTotal` for both actual results (statSourceId=0) and projections (statSourceId=1).

### `team_stats_list_response.json`
**Endpoint**: Team Stats List
**URL**: `https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams`
**Description**: List of all 32 NFL teams with basic information
**Use Case**: Getting team IDs, abbreviations, and basic metadata

**Key Fields**:
- `teams[]` - Array of team objects
- `teams[].team.id` - ESPN team ID (used in other endpoints)
- `teams[].team.abbreviation` - Team abbreviation (e.g., "KC", "NE")
- `teams[].team.displayName` - Full team name
- `teams[].team.logos[]` - Team logo URLs

### `team_stats_response.json`
**Endpoint**: Individual Team Statistics
**URL**: `https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{team_id}/statistics`
**Description**: Detailed statistics for Kansas City Chiefs (team_id=12)
**Use Case**: Understanding team performance metrics, offensive/defensive stats

**Key Fields**:
- `results.stats.categories[]` - Statistics grouped by category
- `categories[].stats[]` - Individual stat entries (name, value, displayValue)
- Important stats:
  - `totalPointsPerGame` - Offensive scoring
  - `totalYards` - Offensive yardage
  - `totalTakeaways` - Defensive metric

### `schedule_response.json`
**Endpoint**: Scoreboard/Schedule
**URL**: `https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard`
**Description**: Week 1 games for 2025 season (3 games shown)
**Use Case**: Getting weekly matchups, determining opponents, game timing

**Key Fields**:
- `events[]` - Array of game events
- `events[].competitions[0].competitors[]` - Two teams (home and away)
- `competitors[].team.id` - Team ID
- `competitors[].team.abbreviation` - Team abbreviation
- `competitors[].homeAway` - 'home' or 'away'
- `events[].status` - Game status and timing

## Using These Examples

### In Documentation
Reference these examples when:
- Explaining API response structures
- Showing field data types
- Demonstrating optional vs required fields
- Illustrating error scenarios

### In Code
Use these to:
- Develop API client code
- Create test fixtures
- Validate parsing logic
- Understand edge cases

## Collected With

- **Date**: 2025-12-13
- **Season**: 2025
- **Scoring Format**: PPR (format_id=3)
- **HTTP Client**: httpx with User-Agent header
- **Rate Limiting**: 0.2s delay between requests

## Need Fresh Examples?

To collect new examples, run the `collect_espn_examples.py` script from the project root:

```bash
python collect_espn_examples.py
```

**Note**: Script will be removed after documentation is complete.

## Questions or Issues?

These examples are for the ESPN Fantasy Football API documentation project. For questions, refer to the main ESPN API documentation in the parent `docs/` folder.
