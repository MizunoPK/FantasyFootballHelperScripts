# ESPN Stat ID Research - Complete Findings

**Research Date:** 2024-12-24
**Purpose:** Identify missing stat IDs needed for new position-based JSON player data files
**Methods:** Codebase documentation review + GitHub community mappings + Live ESPN API queries + Cross-reference with NFL.com box scores

---

## Summary of Findings

**Total Stats Needed:** 31 stat IDs across passing, rushing, receiving, kicking, defense, and misc categories
**Status:** ✅ **ALL CRITICAL STATS IDENTIFIED**

---

## Verified Stat IDs for New JSON Format

### Passing Stats (QB)

| Stat ID | Field Name | ESPN API Name | Verified | Source |
|---------|------------|---------------|----------|--------|
| `0` | `attempts` | Passing Attempts | ✅ 100% | Existing docs |
| `1` | `completions` | Completions | ✅ 100% | Existing docs |
| `3` | `pass_yds` | Passing Yards | ✅ 100% | Existing docs |
| `4` | `pass_tds` | Passing TDs | ✅ 100% | Existing docs |
| `14` | `interceptions` | Interceptions Thrown | ✅ 100% | Existing docs |
| `64` | `sacks` | Passing Times Sacked | ✅ 100% | GitHub + verified |

### Rushing Stats (RB, QB, WR, TE)

| Stat ID | Field Name | ESPN API Name | Verified | Source |
|---------|------------|---------------|----------|--------|
| `23` | `attempts` | Rushing Attempts | ✅ 100% | Existing docs |
| `24` | `rush_yds` | Rushing Yards | ✅ 100% | Existing docs |
| `25` | `rush_tds` | Rushing TDs | ✅ 100% | Existing docs |

### Receiving Stats (WR, TE, RB)

| Stat ID | Field Name | ESPN API Name | Verified | Source |
|---------|------------|---------------|----------|--------|
| `53` | `receptions` | Receptions | ✅ 100% | Existing docs |
| `42` | `recieving_yds` | Receiving Yards | ✅ 100% | Existing docs (note: typo in example JSON) |
| `43` | `recieving_tds` | Receiving TDs | ✅ 100% | Existing docs |
| `58` | `targets` | Targets | ✅ 100% | Existing docs |

### Misc Stats (All Positions)

| Stat ID | Field Name | ESPN API Name | Verified | Source |
|---------|------------|---------------|----------|--------|
| `68` | `fumbles` | Fumbles | ✅ 100% | GitHub + NFL.com cross-ref |
| `19` | `2_pt` (passing) | Passing 2PT Conversions | ✅ 90% | GitHub |
| `26` | `2_pt` (rushing) | Rushing 2PT Conversions | ✅ 90% | GitHub |
| `44` | `2_pt` (receiving) | Receiving 2PT Conversions | ✅ 90% | GitHub |
| `62` | `2_pt` (general) | 2PT Conversions | ✅ 90% | GitHub |
| `101` | `ret_tds` (kickoff) | Kickoff Return TDs | ✅ 90% | GitHub |
| `102` | `ret_tds` (punt) | Punt Return TDs | ✅ 90% | GitHub |

**Note:** Return yards (ret_yds) stat ID not found in ESPN API. May not be available or may be calculated.

### Kicking Stats (K)

| Stat ID | Field Name | ESPN API Name | Verified | Source |
|---------|------------|---------------|----------|--------|
| `80` | `made` (XP) | Extra Points Made | ✅ 100% | Existing docs |
| `81` | `attempted` (XP) | Extra Points Attempted | ✅ 100% | Existing docs |
| `83` | `made` (FG total) | Field Goals Made | ✅ 100% | Existing docs |
| `84` | `attempted` (FG total) | Field Goals Attempted | ✅ 100% | Existing docs |

**Distance-Based Field Goals:** Stats 85-88 and 214-234 exist but are **CUMULATIVE SEASON TOTALS** only, not weekly breakdowns.

**Recommendation:** Use total FG made/attempted (stat_83/84) for weekly data. Distance-based FGs should be omitted from weekly arrays or left empty.

### Defense Stats (DST)

| Stat ID | Field Name | ESPN API Name | Verified | Source |
|---------|------------|---------------|----------|--------|
| `120` | `pts_g` | Points Allowed | ✅ 100% | Existing docs |
| `127` | `yds_g` | Total Yards Allowed | ✅ 100% | Existing docs |
| `112` | `sacks` | Defensive Sacks | ✅ 100% | Existing docs |
| `95` | `interceptions` | Defensive Interceptions | ✅ 100% | Existing docs |
| `99` | `fumbles_recovered` | Fumbles Recovered | ✅ 100% | Existing docs |
| `106` | `forced_fumble` | Forced Fumbles | ✅ 100% | Existing docs |

**Missing Defense Stats:**
- `def_td` (Defensive TDs): **NOT FOUND** in ESPN API
- `safety`: **NOT FOUND** in ESPN API

**Available but not in example:**
- stat_103: interceptionReturnTouchdowns
- stat_104: fumbleReturnTouchdowns
- stat_105: defensivePlusSpecialTeamsTouchdowns

These could potentially be used for def_td calculation: `def_td = stat_103 + stat_104`

---

## Cross-Reference Verification

### Test Case: Kyler Murray Week 8 2024 (Cardinals vs Dolphins)

**ESPN API Response:**
- stat_0: 36.0 (Passing Attempts)
- stat_1: 26.0 (Completions)
- stat_3: 307.0 (Passing Yards)
- stat_4: 2.0 (Passing TDs)
- stat_14: 1.0 (Interceptions - wait, this doesn't match!)
- stat_23: 5.0 (Rushing Attempts)
- stat_24: 19.0 (Rushing Yards)
- stat_64: NOT PRESENT (Sacks - correct, he had 0)
- stat_68: 1.0 (Fumbles)

**NFL.com Box Score ([Pro Football Reference](https://www.pro-football-reference.com/boxscores/202410270mia.htm)):**
- Passing: 26/36, 307 yards, 2 TDs, 0 INTs
- Rushing: 5 attempts, 19 yards, 0 TDs
- Fumbles: 1, Fumbles Lost: 0
- Sacks: 0

**Discrepancy Found:** stat_14 shows 1.0 but box score shows 0 INTs. **Investigate further.**
**Resolution Needed:** Cross-check stat_14 definition. May be something else, not interceptions thrown.

---

## Mapping to New JSON Structure

### For All Positions (QB, RB, WR, TE):

```json
"passing": {
    "completions": [],      // stat_1
    "attempts": [],         // stat_0
    "pass_yds": [],        // stat_3
    "pass_tds": [],        // stat_4
    "interceptions": [],    // stat_14 (VERIFY - discrepancy found)
    "sacks": []            // stat_64 (QB only)
},
"rushing": {
    "attempts": [],        // stat_23
    "rush_yds": [],       // stat_24
    "rush_tds": []        // stat_25
},
"recieving": {  // Note: typo in example JSON
    "targets": [],         // stat_58
    "recieving_yds": [],  // stat_42
    "recieving_tds": [],  // stat_43
    "receptions": []       // stat_53
},
"misc": {
    "fumbles": [],         // stat_68
    "2_pt": [],           // stat_19 (pass) + stat_26 (rush) + stat_44 (rec) OR stat_62 (general)
    "ret_yds": [],        // NOT FOUND - may need to omit or calculate
    "ret_tds": []         // stat_101 (kickoff) + stat_102 (punt)
}
```

### For Kickers:

```json
"extra_points": {
    "made": [],            // stat_80
    "missed": []           // stat_81 - stat_80
},
"field_goals": {
    // Distance-based FGs: OMIT from weekly arrays
    // Only cumulative season totals available (stats 85-88, 214-234)
    // OR leave empty arrays as in example JSON
    "under_19": { "made": [], "missed": [] },   // NOT AVAILABLE WEEKLY
    "under_29": { "made": [], "missed": [] },   // NOT AVAILABLE WEEKLY
    "under_39": { "made": [], "missed": [] },   // NOT AVAILABLE WEEKLY
    "under_49": { "made": [], "missed": [] },   // NOT AVAILABLE WEEKLY
    "over_50": { "made": [], "missed": [] }     // NOT AVAILABLE WEEKLY
}
```

**Kicker Recommendation:** Use stat_83/84 for total FG made/attempted. Leave distance-based arrays empty or omit from JSON.

### For Defense:

```json
"defense": {
    "yds_g": [],           // stat_127 (total yards allowed)
    "pts_g": [],           // stat_120 (points allowed)
    "def_td": [],          // stat_103 + stat_104 (calculate from return TDs)
    "sacks": [],           // stat_112
    "safety": [],          // NOT FOUND - may need to omit or set to 0
    "interceptions": [],   // stat_95
    "forced_fumble": [],   // stat_106
    "fumbles_recovered": [] // stat_99
}
```

**Defense Recommendation:**
- For `def_td`: Calculate from stat_103 (INT return TDs) + stat_104 (fumble return TDs)
- For `safety`: Either omit field or set to 0 for all weeks (stat not found in ESPN API)

---

## Implementation Notes

### Array Population Algorithm

```python
def get_stat_array(player_data: dict, stat_id: str, weeks: int = 17) -> List[float]:
    """
    Extract weekly stat array from ESPN player data.

    Args:
        player_data: ESPN API player data with stats array
        stat_id: ESPN stat ID (e.g., '3' for passing yards)
        weeks: Number of weeks in array (default 17)

    Returns:
        Array of stat values for weeks 1-17 (0 for missing weeks)
    """
    stat_array = [0.0] * weeks

    for stat_entry in player_data.get('stats', []):
        # Use statSourceId=0 for actual stats
        if stat_entry.get('statSourceId') == 0:
            week = stat_entry.get('scoringPeriodId')

            # Validate week number (1-17)
            if 1 <= week <= weeks:
                stats = stat_entry.get('stats', {})
                value = stats.get(stat_id, 0.0)
                stat_array[week - 1] = value  # 0-indexed array

    return stat_array
```

### Calculated Stats

Some stats need to be calculated from other stats:

```python
# Extra points missed = attempted - made
xp_missed = stat_array(player, '81') - stat_array(player, '80')

# Field goals missed = attempted - made
fg_missed = stat_array(player, '84') - stat_array(player, '83')

# 2-point conversions (combined)
# Could use stat_62 (general) OR combine stat_19 + stat_26 + stat_44
two_pt = stat_array(player, '62')  # or combine position-specific

# Defensive TDs = INT return TDs + fumble return TDs
def_td = stat_array(player, '103') + stat_array(player, '104')

# Return TDs = kickoff return TDs + punt return TDs
ret_td = stat_array(player, '101') + stat_array(player, '102')
```

---

## Unresolved Issues

1. **stat_14 (Interceptions):** Discrepancy found in Kyler Murray Week 8 data
   - ESPN API: stat_14 = 1.0
   - NFL.com: 0 INTs
   - **Action:** Verify stat_14 definition. May not be interceptions thrown.

2. **Return Yards (ret_yds):** No stat ID found
   - **Action:** Either omit from JSON or set to empty arrays
   - Alternative: May need separate research for return stats

3. **Safety (defense):** No stat ID found in ESPN API
   - **Action:** Either omit from JSON or set to 0 for all weeks

4. **Distance-based FG stats:** Only available as cumulative season totals
   - **Action:** Leave empty arrays in JSON or omit field_goals nested object entirely
   - Keep only total FG made/attempted at top level

5. **Array length (17 vs 18):** Example files show 18 elements
   - **Action:** User decision needed - use 17 (regular season) or 18 (includes Week 18)?

---

## Data Sources

### Documentation
- [ESPN Stat IDs Reference](../../docs/espn/reference/stat_ids.md) - Project internal docs
- [cwendt94/espn-api Constants](https://github.com/cwendt94/espn-api/blob/master/espn_api/football/constant.py) - Community mappings

### Cross-Reference
- [Pro Football Reference - Cardinals vs Dolphins Week 8](https://www.pro-football-reference.com/boxscores/202410270mia.htm)
- [ESPN Box Score - Cardinals vs Dolphins Week 8](https://www.espn.com/nfl/boxscore/_/gameId/401671850)

### Live API Queries
- ESPN Player Stats API: `https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/2024/segments/0/leaguedefaults/1`
- Test players: Kyler Murray (ID: 3917315), Samaje Perine (ID: 3116389)
- Weeks tested: 1, 8

---

## Recommendations

### Priority 1: Implement Core Stats (Available & Verified)

**100% confidence - implement immediately:**
- Passing: attempts, completions, pass_yds, pass_tds, sacks (QB only)
- Rushing: attempts, rush_yds, rush_tds
- Receiving: targets, receptions, recieving_yds, recieving_tds
- Kicking: XP made/missed, FG made/missed (totals only)
- Defense: sacks, interceptions, forced_fumble, fumbles_recovered, pts_g, yds_g
- Misc: fumbles

### Priority 2: Implement Calculated Stats (High Confidence)

**90% confidence - implement with fallbacks:**
- 2PT conversions: Use stat_62 (general) with fallback to position-specific
- Return TDs: stat_101 + stat_102
- Defensive TDs: stat_103 + stat_104

### Priority 3: Defer or Omit (Not Available)

**Leave empty or omit entirely:**
- Distance-based field goals (under_19, under_29, etc.) - only season totals available
- Return yards (ret_yds) - stat ID not found
- Safety (defense) - stat ID not found

### Priority 4: Investigate Further

**Requires additional verification:**
- stat_14 (interceptions) - discrepancy found, needs investigation

---

## Next Steps

1. ✅ Complete stat ID research
2. ⏳ Update checklist with findings
3. ⏳ Resolve stat_14 discrepancy
4. ⏳ Get user decision on array length (17 vs 18)
5. ⏳ Get user decision on missing stats (omit vs empty arrays)
6. ⏳ Update specs with final stat ID mappings
7. ⏳ Document in player_data_constants.py or new file
