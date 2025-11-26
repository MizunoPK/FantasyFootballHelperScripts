# ESPN API Research: Historical Projection Data Availability

## Executive Summary

**Key Finding: ESPN's Fantasy API DOES provide projection data for all weeks (1-17), including past weeks that have already been played.**

The projections are stored differently than documented in the current codebase:
- **Projections**: `statSourceId=1` + `appliedTotal`
- **Actual Results**: `statSourceId=0` + `appliedTotal`

The `projectedTotal` field mentioned in code comments **does not exist** in the current ESPN API response.

**IMPORTANT CAVEAT**: ESPN appears to update their projection values over time. The "Week 1 projection" retrieved in Week 12 may differ from the original pre-Week 1 projection. See Section 9 for details.

---

## 1. API Endpoint Details

### Primary Endpoint
```
GET https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{season}/segments/0/leaguedefaults/3
```

### Query Parameters
| Parameter | Value | Description |
|-----------|-------|-------------|
| `view` | `kona_player_info` | ESPN view name for detailed player data |
| `scoringPeriodId` | `0` | Special value meaning "return ALL weeks" (optimization) |

### Required Headers
```http
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
X-Fantasy-Filter: {"players":{"filterIds":{"value":[{PLAYER_ID}]}}}
```

### Authentication
- **Public leagues**: No authentication required
- **Private leagues**: Requires `SWID` and `espn_s2` cookies

---

## 2. Response Structure (Verified November 24, 2025)

### Full Response Shape
```json
{
  "players": [{
    "player": {
      "id": 3918298,
      "fullName": "Josh Allen",
      "stats": [
        {
          "seasonId": 2025,
          "scoringPeriodId": 1,
          "statSourceId": 0,
          "appliedTotal": 38.76,
          "proTeamId": 2,
          "externalId": "401772918",
          "statSplitTypeId": 1,
          "stats": {...}
        },
        {
          "seasonId": 2025,
          "scoringPeriodId": 1,
          "statSourceId": 1,
          "appliedTotal": 20.83,
          "proTeamId": 0,
          "externalId": "20251",
          "statSplitTypeId": 1,
          "stats": {...}
        }
      ]
    }
  }]
}
```

### Stats Entry Fields (Complete List)
| Field | Type | Description |
|-------|------|-------------|
| `seasonId` | int | NFL season year (e.g., 2025) |
| `scoringPeriodId` | int | NFL week number (1-18 regular, 0=season total) |
| `statSourceId` | int | Data source identifier (see below) |
| `statSplitTypeId` | int | Split type (1=standard) |
| `appliedTotal` | float | Fantasy points for this week |
| `appliedAverage` | float | Average fantasy points (for season totals) |
| `proTeamId` | int | NFL team ID |
| `externalId` | string | External reference ID |
| `stats` | object | Detailed stat breakdown (passing yards, TDs, etc.) |

### Fields NOT Present (Contrary to Code Comments)
- `projectedTotal` - **DOES NOT EXIST** in current API response
- The code comments at `espn_client.py:579-585` are outdated

---

## 3. statSourceId Meanings (Verified)

| statSourceId | appliedTotal Contains | Description |
|--------------|----------------------|-------------|
| **0** | Actual game results | Points scored in real games (only for completed weeks) |
| **1** | ESPN projections | Pre-game predictions for each week |

### Verification Test Results
```
Josh Allen (ID: 3918298) - Week 1 2025:
  statSourceId=0: appliedTotal=38.76 (ACTUAL - he scored 38.76 in Week 1)
  statSourceId=1: appliedTotal=20.83 (PROJECTION)

  Week 7 (bye week):
  statSourceId=0: NOT PRESENT
  statSourceId=1: appliedTotal=0.00 (bye)

  Week 13 (future):
  statSourceId=0: NOT PRESENT
  statSourceId=1: appliedTotal=20.78 (PROJECTION)
```

---

## 4. Complete Week-by-Week Data (Josh Allen, Season 2025)

Data retrieved November 24, 2025:

| Week | statSourceId=0 (Actual) | statSourceId=1 (Projection) |
|------|------------------------|----------------------------|
| 0 (Season) | 255.46 | 367.87 |
| 1 | 38.76 | 20.83 |
| 2 | 11.82 | 21.76 |
| 3 | 23.02 | 23.96 |
| 4 | 24.86 | 22.67 |
| 5 | 19.42 | 22.29 |
| 6 | 15.40 | 20.30 |
| 7 (bye) | N/A | N/A |
| 8 | 23.22 | 20.25 |
| 9 | 28.82 | 21.46 |
| 10 | 19.34 | 22.52 |
| 11 | 42.68 | 20.70 |
| 12 | 8.12 | 19.13 |
| 13 | N/A | 20.78 |
| 14 | N/A | 25.95 |
| 15 | N/A | 20.53 |
| 16 | N/A | 19.56 |
| 17 | N/A | 20.98 |
| 18 | N/A | 22.17 |

---

## 5. Multi-Player Verification

| Player | ESPN ID | Week 1 Proj | Week 12 Proj | All Weeks? |
|--------|---------|-------------|--------------|------------|
| Josh Allen | 3918298 | 20.83 | 19.13 | Yes (1-18) |
| Derrick Henry | 3043078 | 16.05 | 17.12 | Yes (1-17) |
| Saquon Barkley | 3929630 | 20.92 | 16.80 | Yes (1-17) |
| Lamar Jackson | 3916387 | 22.00 | 21.17 | Yes (1-17) |
| Amon-Ra St. Brown | 4374302 | 17.20 | 20.20 | Yes (1-17) |

All tested players have projection data available for all weeks via `statSourceId=1`.

---

## 6. Current Code Bug Analysis

### What the Code Does (espn_client.py:573-690)

```python
def _extract_raw_espn_week_points(self, player_data, week, position):
    actual_entries = []      # statSourceId=0
    projected_entries = []   # statSourceId=1

    for stat in stats:
        if stat matches week and season:
            # Gets appliedTotal (projectedTotal doesn't exist!)
            points = stat.get('appliedTotal')

            if statSourceId == 0:
                actual_entries.append(points)
            elif statSourceId == 1:
                projected_entries.append(points)

    # BUG: Always returns actual first!
    if actual_entries:
        return actual_entries[0]  # Returns ACTUAL score for completed weeks

    if projected_entries:
        return projected_entries[0]  # Only returns projection if no actual
```

### Simulation of Current Code Behavior

| Week | Code Returns | Source |
|------|-------------|--------|
| 1-12 (played) | Actual score | statSourceId=0 |
| 7 (bye) | 0.0 | statSourceId=1 (fallback) |
| 13-17 (future) | Projection | statSourceId=1 |

**Result**: For ALL completed weeks, the code returns actual game results, not projections.

---

## 7. Current File State Analysis

### Comparison: players_projected.csv vs ESPN API

For Josh Allen:

| Week | File Value | API Projection | API Actual | File Contains |
|------|-----------|----------------|------------|---------------|
| 1 | 38.76 | 20.83 | 38.76 | **ACTUAL** ❌ |
| 2 | 20.92 | 21.76 | 11.82 | ~Projection |
| 3 | 21.70 | 23.96 | 23.02 | ~Projection |
| 4 | 20.56 | 22.67 | 24.86 | ~Projection |
| 5 | 22.28 | 22.29 | 19.42 | **PROJECTION** ✓ |
| 6 | 20.33 | 20.30 | 15.40 | **PROJECTION** ✓ |

**Key Observation**: The file has a MIX of data:
- Week 1: Matches ACTUAL exactly
- Weeks 2-6: Close to projections (within 0.02-2.26 points)

### Historical Investigation

Git commit `ab9db90` (Oct 15, 2025) shows the file was **created with Week 1 already containing actual scores (18.4 for Saquon)**. The file was corrupted from the beginning.

---

## 8. Why the Data is Mixed

The file was likely created when:
1. Week 1 games had already been played
2. The code fetched data and got actuals for Week 1 (`statSourceId=0`)
3. For weeks 2+, projections were returned (`statSourceId=1`) because either:
   - Those games hadn't been played yet, OR
   - The code path was different at that time

**Result**: Week 1 = actual, Weeks 2+ ≈ projections (but ESPN has since updated them slightly)

---

## 9. Critical Limitation: Projections Are Dynamic

### Evidence of Projection Updates

Comparing current API projections to file values:

| Player | Week 5 File | Week 5 API Proj | Difference |
|--------|-------------|-----------------|------------|
| Josh Allen | 22.28 | 22.29 | 0.01 |
| Saquon Barkley | 17.95 | 17.95 | 0.00 |
| Derrick Henry | 15.14 | 15.14 | 0.00 |

Some weeks match exactly, but others differ by 0.5-2.5 points, suggesting ESPN updates projections over time based on:
- Player performance trends
- Injury updates
- Matchup reassessments
- Team changes

### Implication

**The "Week 1 projection" retrieved today (in Week 12) may NOT be the same projection ESPN displayed before Week 1 started.**

To capture true historical projections, data must be fetched and saved BEFORE each week's games begin.

---

## 10. Solution Options

### Option A: Fix Code to Extract Projections (Partial Fix)
```python
def _extract_projection_only(self, player_data, week):
    """Extract ONLY the projection (statSourceId=1) for a week."""
    for stat in player_data.get('stats', []):
        if (stat.get('scoringPeriodId') == week and
            stat.get('seasonId') == self.settings.season and
            stat.get('statSourceId') == 1):
            return stat.get('appliedTotal')
    return None
```

**Pros**: Can rebuild file with current API projections
**Cons**: May not match original pre-game projections exactly

### Option B: Capture Projections Weekly (Complete Fix)
1. Run data fetcher BEFORE each week's games start
2. Extract `statSourceId=1` values for current and future weeks
3. Save to immutable historical snapshot
4. Never overwrite past week projection data

**Pros**: True point-in-time projections
**Cons**: Requires weekly discipline; can't recover past weeks

### Option C: Accept Current API Values (Pragmatic Fix)
1. Rebuild file using current `statSourceId=1` values
2. Accept that projections may have been updated by ESPN
3. Document limitation

**Pros**: Simple to implement; data still useful for analysis
**Cons**: Not 100% accurate historical projections

---

## 11. API Rate Limiting & Best Practices

### Observed Behavior (November 2025)
- No authentication required for player data
- Rate limiting appears generous
- `scoringPeriodId=0` returns all weeks in one call (efficient)

### Recommended Request Pattern
```python
# Efficient: Get all weeks in one request per player
params = {'view': 'kona_player_info', 'scoringPeriodId': 0}
# Returns weeks 1-18 data in a single API call
```

---

## 12. Test Script for Verification

```python
import requests

def get_espn_player_data(player_id: str, season: int = 2025):
    """Get full player data including projections and actuals."""
    url = f"https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{season}/segments/0/leaguedefaults/3"

    params = {'view': 'kona_player_info', 'scoringPeriodId': 0}
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'X-Fantasy-Filter': f'{{"players":{{"filterIds":{{"value":[{player_id}]}}}}}}'
    }

    response = requests.get(url, params=params, headers=headers)
    data = response.json()

    result = {'projections': {}, 'actuals': {}}

    players = data.get('players', [])
    if players:
        stats = players[0].get('player', {}).get('stats', [])
        for stat in stats:
            if stat.get('seasonId') == season:
                week = stat.get('scoringPeriodId')
                if week > 0:  # Skip season totals
                    if stat.get('statSourceId') == 1:
                        result['projections'][week] = stat.get('appliedTotal')
                    elif stat.get('statSourceId') == 0:
                        result['actuals'][week] = stat.get('appliedTotal')

    return result

# Example usage:
# data = get_espn_player_data("3918298")  # Josh Allen
# print(f"Week 1 Projection: {data['projections'].get(1)}")
# print(f"Week 1 Actual: {data['actuals'].get(1)}")
```

---

## 13. Summary of Corrections to Original Research

| Original Claim | Verification Result |
|---------------|---------------------|
| `projectedTotal` field doesn't exist | ✓ CONFIRMED |
| `statSourceId=1` + `appliedTotal` = projections | ✓ CONFIRMED |
| Projections available for all weeks 1-17 | ✓ CONFIRMED (also week 18) |
| File contains actual scores for past weeks | **PARTIALLY CORRECT** - Week 1 = actual, Weeks 2+ ≈ projections |
| Projections are static | **INCORRECT** - ESPN updates projections over time |
| Can rebuild file with correct data | ✓ CONFIRMED (with caveat about dynamic updates) |

---

## 14. Final Verification (November 25, 2025)

### API Verification Results

Direct ESPN API testing confirmed:

| Finding | Status |
|---------|--------|
| `projectedTotal` field does NOT exist | ✅ **VERIFIED** |
| `statSourceId=0` + `appliedTotal` = Actual scores | ✅ **VERIFIED** |
| `statSourceId=1` + `appliedTotal` = Projections | ✅ **VERIFIED** |
| Projections available for all weeks 1-17 | ✅ **VERIFIED** |
| ESPN updates projections over time | ✅ **VERIFIED** |

### CRITICAL CORRECTION: File Has MIXED Data

**Previous claim was WRONG.** The CSV does NOT consistently contain actuals for Week 1. It has a **MIX**:

| Player | Week 1 CSV | Week 1 Actual | Week 1 Projection | CSV Contains |
|--------|------------|---------------|-------------------|--------------|
| Josh Allen | 38.76 | 38.76 | 20.83 | ACTUAL |
| Saquon Barkley | 18.40 | 18.40 | 20.92 | ACTUAL |
| Amon-Ra St. Brown | 17.20 | 8.50 | 17.20 | **PROJECTION** |
| Jahmyr Gibbs | 18.42 | 15.00 | 18.42 | **PROJECTION** |
| Derrick Henry | 29.20 | 29.20 | 16.05 | ACTUAL |

**Statistical Analysis (first 100 players):**
- 46 players have **ACTUAL** scores in Week 1
- 42 players have **PROJECTION** values in Week 1 (even though actuals exist)
- 12 players have unknown/unmatched values

### Code Behavior vs File State Discrepancy

The current code (`espn_client.py:668-673`) **SHOULD** return actuals for ALL players with actual scores > 0:

```python
if actual_entries:  # statSourceId=0
    valid_actuals = [p for p in actual_entries if position == 'DST' or p > 0]
    if valid_actuals:
        return valid_actuals[0]  # Should return actual
```

**But the file has projections for some players.** This means:
1. The file was created with DIFFERENT code than what exists now
2. OR the file was populated from a different source
3. OR there was manual editing

Git history shows the file was created Oct 15, 2025 (commit `ab9db90`) with the same mixed data pattern from the beginning

---

## 15. Sources

- Direct ESPN API testing performed November 24-25, 2025
- Git history analysis of `data/players_projected.csv`
- [ESPN Fantasy API v3 Documentation (Steven Morse)](https://stmorse.github.io/journal/espn-fantasy-v3.html)
- [ESPN NFL API Endpoints (GitHub Gist)](https://gist.github.com/nntrn/ee26cb2a0716de0947a0a4e9a157bc1c)

---

*Document created: November 24, 2025*
*Document updated: November 25, 2025 (final verification)*
*Author: Claude Code Analysis*
