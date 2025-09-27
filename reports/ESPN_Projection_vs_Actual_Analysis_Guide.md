# ESPN API: Projection vs Actual Analysis Guide

**Generated:** September 26, 2025
**Purpose:** Guide for extracting pre-game projections vs actual results from ESPN Fantasy API

## 🎯 Overview

Yes, you can absolutely get pre-game projections for past games! ESPN's API stores both projected and actual data for each week, distinguished by the `statSourceId` field.

## 🔍 Key Data Structure

ESPN stores fantasy data with these important fields:

```json
{
  "stats": [
    {
      "seasonId": 2024,
      "scoringPeriodId": 10,
      "statSourceId": 1,           // 1 = PROJECTED (pre-game)
      "projectedTotal": 18.5,      // Pre-game projection
      "appliedTotal": null         // Not set for projections
    },
    {
      "seasonId": 2024,
      "scoringPeriodId": 10,
      "statSourceId": 0,           // 0 = ACTUAL (post-game)
      "projectedTotal": 18.5,      // Original projection (preserved)
      "appliedTotal": 24.2         // Actual fantasy points scored
    }
  ]
}
```

## 📊 Data Type Identification

| Field | Value | Meaning |
|-------|-------|---------|
| `statSourceId` | `1` | **Projected data** (pre-game fantasy projections) |
| `statSourceId` | `0` | **Actual data** (post-game results) |
| `projectedTotal` | Any value | ESPN's pre-game projection |
| `appliedTotal` | `null` | No actual game played yet |
| `appliedTotal` | Number | Actual fantasy points from completed game |

## 🛠️ How to Extract Projection vs Actual

### Method 1: Get All Weeks for a Player (Recommended)

**Endpoint:**
```
GET https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/2024/segments/0/leaguedefaults/3
```

**Parameters:**
- `view=kona_player_info`
- `scoringPeriodId=0` (gets ALL weeks)
- `X-Fantasy-Filter={"players":{"filterIds":{"value":[PLAYER_ID]}}}`

**Response Analysis:**
```javascript
// Filter for specific week and data type
const projectedEntry = stats.find(s =>
  s.seasonId === 2024 &&
  s.scoringPeriodId === 10 &&
  s.statSourceId === 1  // PROJECTED
);

const actualEntry = stats.find(s =>
  s.seasonId === 2024 &&
  s.scoringPeriodId === 10 &&
  s.statSourceId === 0  // ACTUAL
);

const preGameProjection = projectedEntry?.projectedTotal;
const actualPoints = actualEntry?.appliedTotal;
const projectionAccuracy = actualPoints - preGameProjection;
```

### Method 2: Get Specific Week Data

**Endpoint:**
```
GET https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/2024/segments/0/leaguedefaults/3
```

**Parameters:**
- `view=kona_player_info`
- `scoringPeriodId=10` (specific week)
- `X-Fantasy-Filter={"players":{"filterIds":{"value":[PLAYER_ID]}}}`

## 📈 Analysis Examples

### Example 1: Projection Accuracy Analysis

```javascript
// Calculate projection accuracy for a player across a season
function calculateProjectionAccuracy(playerStats) {
  const results = [];

  // Group by week
  const weeklyData = {};
  playerStats.forEach(stat => {
    const week = stat.scoringPeriodId;
    if (!weeklyData[week]) weeklyData[week] = {};

    if (stat.statSourceId === 1) {
      weeklyData[week].projected = stat.projectedTotal;
    } else if (stat.statSourceId === 0) {
      weeklyData[week].actual = stat.appliedTotal;
    }
  });

  // Calculate accuracy for each week
  Object.entries(weeklyData).forEach(([week, data]) => {
    if (data.projected !== undefined && data.actual !== undefined) {
      const accuracy = Math.abs(data.actual - data.projected);
      const percentAccuracy = (1 - (accuracy / data.projected)) * 100;

      results.push({
        week: parseInt(week),
        projected: data.projected,
        actual: data.actual,
        difference: data.actual - data.projected,
        accuracy: percentAccuracy
      });
    }
  });

  return results;
}
```

### Example 2: Finding the Most/Least Accurate Projections

```javascript
// Find weeks where projections were most off
function findProjectionOutliers(accuracyData) {
  const sorted = accuracyData.sort((a, b) =>
    Math.abs(b.difference) - Math.abs(a.difference)
  );

  return {
    mostInaccurate: sorted[0],           // Biggest miss
    mostAccurate: sorted[sorted.length - 1], // Closest prediction
    avgAccuracy: sorted.reduce((sum, item) => sum + item.accuracy, 0) / sorted.length
  };
}
```

## 🗃️ Historical Data Availability

### Seasons Available:
- **2024 Season:** Complete projection vs actual data ✅
- **2023 Season:** Complete projection vs actual data ✅
- **2022 Season:** Complete projection vs actual data ✅
- **2021+ Seasons:** Available but may have different data structure

### Week Ranges:
- **Regular Season:** Weeks 1-18
- **Playoff Season:** Weeks 19-22 (limited data)

## 📋 Postman Collection Usage

I've added two new requests to the Postman collection:

### 1. "Historical Projection vs Actual Analysis"
- **Season:** 2024 (completed season)
- **Scope:** All weeks for a player
- **Purpose:** Get complete projection vs actual dataset

### 2. "Specific Past Week - Projection vs Actual"
- **Season:** 2024
- **Week:** Week 10 (example)
- **Purpose:** Get detailed data for a single week

## 🔧 Testing Steps

1. **Import the updated Postman collection**

2. **Get a valid player ID:**
   - Run "Get All Players (Find Player IDs)"
   - Copy an `id` from the response (e.g., for a top player)

3. **Test historical data:**
   - Update `player_id` variable with the valid ID
   - Run "Historical Projection vs Actual Analysis"
   - Look for multiple stat entries per week with different `statSourceId` values

4. **Analyze the response:**
   ```json
   {
     "players": [
       {
         "player": {
           "id": 12345,
           "firstName": "Player",
           "lastName": "Name",
           "stats": [
             {
               "seasonId": 2024,
               "scoringPeriodId": 1,
               "statSourceId": 1,        // PROJECTION
               "projectedTotal": 15.8,
               "appliedTotal": null
             },
             {
               "seasonId": 2024,
               "scoringPeriodId": 1,
               "statSourceId": 0,        // ACTUAL
               "projectedTotal": 15.8,   // Preserved original projection
               "appliedTotal": 22.4      // What actually happened
             }
           ]
         }
       }
     ]
   }
   ```

## 📊 Analysis Opportunities

### Player Performance Analysis:
- **Consistency:** Which players most often exceed/miss projections?
- **Boom/Bust:** Identify high-variance players
- **Trends:** Do projections get more/less accurate as season progresses?

### Position Analysis:
- **QB vs RB vs WR:** Which positions have most accurate projections?
- **Game Script Dependency:** Which positions are most affected by game flow?

### Matchup Analysis:
- **Opponent Defense:** How do tough matchups affect projection accuracy?
- **Home/Away:** Do projections account for home field advantage?

### Fantasy Strategy:
- **Waiver Pickups:** Find consistently undervalued players
- **Trade Analysis:** Identify overvalued players to trade away
- **Start/Sit:** Use historical accuracy to weight current projections

## ⚠️ Important Notes

### Data Reliability:
- **2024 data is most reliable** (complete season)
- **Current season (2025)** may have limited historical projection data
- **Older seasons** may have different API response structures

### Rate Limiting:
- ESPN APIs are public but implement rate limiting
- Include proper delays between requests
- Use the `User-Agent` header as shown in examples

### Data Interpretation:
- `projectedTotal` represents ESPN's pre-game projection
- `appliedTotal` is the actual fantasy points scored
- Both values use the same scoring system (PPR, Standard, etc.)

## 🎯 Conclusion

ESPN's API provides excellent historical data for projection vs actual analysis. The key is understanding the `statSourceId` field and how ESPN structures the data. With this information, you can build powerful analysis tools to:

- Evaluate projection accuracy
- Identify player trends and patterns
- Make more informed fantasy decisions
- Build predictive models based on historical performance

The updated Postman collection provides ready-to-use examples for getting started with this analysis immediately.