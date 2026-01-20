# Scoring Categories for New Metrics

**Purpose:** Clarify which scoring category each metric falls into and verify correct implementation patterns.

**Last Updated:** 2025-12-27

---

## Scoring Category Reference

All fantasy football metrics must fall into one of three categories:

### Category 1: Static Bonus/Penalty (Fixed Values)
- **Usage:** Environmental factors affecting all players equally
- **Formula:** `adjusted_score = previous_score + FIXED_MODIFIER`
- **Example:** Location scoring (HOME = +2.0, AWAY = -2.0, INTERNATIONAL = -5.0)

### Category 2: Multiplier-Based (Intrinsic Value/Context)
- **Usage:** Stable player skills, efficiency, or team context
- **Formula:** `adjusted_score = previous_score * (base_multiplier ^ WEIGHT)`
- **Example:** Team quality, ADP, efficiency metrics

### Category 3: Impact Scale Bonus/Penalty (Circumstantial Variance)
- **Usage:** Week-to-week situational factors (matchup, schedule)
- **Formula:** `bonus = (IMPACT_SCALE * multiplier) - IMPACT_SCALE; adjusted_score = previous_score + bonus`
- **Example:** Matchup scoring, schedule strength

---

## Metric Categorization

All new metrics (M01-M11) are **Category 2 (Multiplier-Based)** because they measure stable player characteristics, efficiency, and role usage.

### High Priority Metrics

#### M01: Target Volume (WR, TE, RB)
- **Category:** 2 (Multiplier-Based)
- **Why:** Measures stable offensive role and target share - reflects player's usage pattern in offense
- **Config Pattern:** ✅ Correct (THRESHOLDS, MULTIPLIERS, WEIGHT)
- **File:** `metric-01-target-volume.md`

#### M02: QB Rushing Upside
- **Category:** 2 (Multiplier-Based)
- **Why:** Dual-threat ability is an intrinsic QB skill that remains stable across season
- **Config Pattern:** ✅ Correct (THRESHOLDS, MULTIPLIERS, WEIGHT)
- **File:** `metric-02-qb-rushing-upside.md`

#### M03: Pass Attempts Per Game (QB Volume)
- **Category:** 2 (Multiplier-Based)
- **Why:** Team offensive system/philosophy is stable context, not week-to-week variance
- **Config Pattern:** ✅ Correct (THRESHOLDS, MULTIPLIERS, WEIGHT)
- **File:** `metric-03-pass-attempts-per-game.md`

#### M04: Carries Per Game (RB Volume Floor)
- **Category:** 2 (Multiplier-Based)
- **Why:** RB's role in offense (bell cow vs committee) is stable across season
- **Config Pattern:** ✅ Correct (THRESHOLDS, MULTIPLIERS, WEIGHT)
- **File:** `metric-04-carries-per-game.md`

---

### Position-Specific Metrics

#### M05: Kicker Accuracy
- **Category:** 2 (Multiplier-Based)
- **Why:** Kicker skill/reliability is an intrinsic characteristic that's stable across season
- **Config Pattern:** ✅ Correct (THRESHOLDS, MULTIPLIERS, WEIGHT)
- **File:** `metric-05-kicker-accuracy.md`

#### M06: Completion Percentage (QB Efficiency)
- **Category:** 2 (Multiplier-Based)
- **Why:** QB accuracy is an intrinsic skill that remains relatively stable
- **Config Pattern:** ✅ Correct (THRESHOLDS, MULTIPLIERS, WEIGHT)
- **File:** `metric-06-completion-percentage.md`

#### M07: TD:INT Ratio (QB Ball Security)
- **Category:** 2 (Multiplier-Based)
- **Why:** QB decision-making and ball security is an intrinsic skill
- **Config Pattern:** ✅ Correct (THRESHOLDS, MULTIPLIERS, WEIGHT)
- **File:** `metric-07-td-int-ratio.md`

#### M08: Yards Per Carry (RB Efficiency)
- **Category:** 2 (Multiplier-Based)
- **Why:** RB efficiency (elusiveness + O-line quality) is relatively stable across season
- **Config Pattern:** ✅ Correct (THRESHOLDS, MULTIPLIERS, WEIGHT)
- **File:** `metric-08-yards-per-carry.md`

#### M09: Yards Per Reception (WR/TE Efficiency)
- **Category:** 2 (Multiplier-Based)
- **Why:** Deep threat ability vs possession receiver role is an intrinsic player characteristic
- **Config Pattern:** ✅ Correct (THRESHOLDS_WR, THRESHOLDS_TE, MULTIPLIERS, WEIGHT)
- **File:** `metric-09-yards-per-reception.md`

#### M10: Catch Rate (WR/TE/RB Reliability)
- **Category:** 2 (Multiplier-Based)
- **Why:** Receiver reliability (hands, route running) is an intrinsic skill
- **Config Pattern:** ✅ Correct (THRESHOLDS, MULTIPLIERS, WEIGHT)
- **File:** `metric-10-catch-rate.md`

#### M11: RB Receiving Workload (Pass-Catching Role)
- **Category:** 2 (Multiplier-Based)
- **Why:** RB's pass-catching role is a stable offensive usage pattern
- **Config Pattern:** ✅ Correct (THRESHOLDS, MULTIPLIERS, WEIGHT)
- **File:** `metric-11-rb-receiving-workload.md`

#### M12: QB Quality (Pass-Catcher Context)
- **Category:** 2 (Multiplier-Based)
- **Why:** Team QB quality is stable context that elevates or limits pass-catchers' value
- **Config Pattern:** ✅ Correct (THRESHOLDS, MULTIPLIERS, POSITION_WEIGHTS)
- **File:** `metric-12-qb-quality.md`

---

## Bonus Metric

#### M17: Target Share Trend (Rolling Window Analysis)
- **Category:** 2 (Multiplier-Based)
- **Why:** Emerging/fading role is still a player-specific characteristic, not matchup-dependent
- **Config Pattern:** ✅ Correct (THRESHOLDS, MULTIPLIERS, WEIGHT)
- **File:** `metric-17-target-share-trend.md`

---

## Why NOT Category 3 (Impact Scale)?

**Question:** Why aren't volume metrics (Target Volume, Carries Per Game) Category 3?

**Answer:** While volume can vary by game script, these metrics measure **season-long usage patterns** not **week-to-week matchup variance**:

- **Category 3 (Matchup):** "This week, my RB faces a tough run defense" → Changes every week based on opponent
- **Category 2 (Volume):** "My RB is a bell cow with 20 carries/game" → Stable role regardless of opponent

Volume metrics reflect **coaching decisions about player role**, which remain stable across the season, not situational factors that change weekly.

---

## Why NOT Category 1 (Static)?

**Question:** Why aren't these static bonuses that affect everyone equally?

**Answer:** These metrics vary **between players** based on individual skills and roles:

- **Category 1 (Location):** "All players at home get +2.0 pts" → Same for everyone in that situation
- **Category 2 (Efficiency):** "This RB has 5.8 YPC vs another with 3.5 YPC" → Player-specific skill

Static bonuses are environment-only, while these metrics capture player-specific value.

---

## Configuration Verification

All 11 metrics use the correct **Category 2 (Multiplier-Based)** config structure:

```json
{
  "[METRIC_NAME]_SCORING": {
    "ENABLED": true,
    "THRESHOLDS": {
      "EXCELLENT": [value],
      "GOOD": [value],
      "AVERAGE": [value]
    },
    "MULTIPLIERS": {
      "EXCELLENT": 1.05,
      "GOOD": 1.025,
      "AVERAGE": 1.0,
      "POOR": 0.975,
      "VERY_POOR": 0.95
    },
    "WEIGHT": [1.0 - 3.0],
    "MIN_GAMES": [3-10],
    "DESCRIPTION": "[Brief description]"
  }
}
```

**✅ All metrics verified** - No changes needed to existing feature request files.

---

## Summary

- **Total Metrics:** 12 (+ 1 bonus metric M17)
- **Category 1 (Static):** 0 metrics
- **Category 2 (Multiplier):** 13 metrics (100%)
- **Category 3 (Impact Scale):** 0 metrics

**Conclusion:** All new player-skill and efficiency metrics correctly use the multiplier-based pattern to reflect intrinsic player value and stable context.

---

**See Also:**
- `feature-updates/guides/METRIC_REQUEST_TEMPLATE.md` - Complete scoring category documentation
- `docs/scoring/04_team_quality_multiplier.md` - Example Category 2 implementation
- `docs/scoring/06_matchup_multiplier.md` - Example Category 3 implementation
- `docs/scoring/13_location_scoring.md` - Example Category 1 implementation
