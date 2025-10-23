# Threshold Redesign - Questions and Clarifications (v2)

**Purpose:** Clarify implementation details for the updated threshold system redesign.

**Status:** Awaiting User Input
**Created:** 2025-10-16
**Reference:** `updates/threshold_updates.txt` (updated version)

---

## Key Changes from Previous Specification

The new specification is much simpler:
1. **BASE_POSITION = 0** for all scoring types (no longer varies by type)
2. **Different formulas:** Uses 1x, 2x, 3x, 4x multipliers (instead of 0x, 1x, 2x, 3x)
3. **Bidirectional uses 0.5x and 1.5x** (instead of 1x and 2x)

---

## Critical Questions

### Q1: Current Thresholds Don't Match New Formula
**Context:** Current thresholds and new formula produce different values.

**Current ADP_SCORING thresholds:**
```
VERY_POOR: 150
POOR: 100
GOOD: 50
EXCELLENT: 20
```

**Using new formula (BASE_POSITION=0, DIRECTION=DECREASING, STEPS=30):**
```
EXCELLENT = 0 + 30 = 30
GOOD = 0 + 60 = 60
POOR = 0 + 90 = 90
VERY_POOR = 0 + 120 = 120
```

**Question:** Should we:
- [ ] A: Use the new formula values (30, 60, 90, 120) and accept the behavioral change
- [X] B: Adjust STEPS to better match current values (STEPS=37.5 → E=37.5, G=75, P=112.5, VP=150)
- [ ] C: Use non-zero BASE_POSITION to match current thresholds better

**Impact:** Changes threshold values, potentially affects scoring behavior and results.

**Recommendation:** Option B (adjust STEPS) to maintain similar behavior while gaining formula benefits.

---

### Q2: Current PLAYER_RATING Doesn't Match Formula
**Current PLAYER_RATING_SCORING thresholds:**
```
VERY_POOR: 20
POOR: 40
GOOD: 60
EXCELLENT: 80
```

**Using new formula (BASE_POSITION=0, DIRECTION=INCREASING, STEPS=20):**
```
VERY_POOR = 0 + 20 = 20 ✓ (matches!)
POOR = 0 + 40 = 40 ✓ (matches!)
GOOD = 0 + 60 = 60 ✓ (matches!)
EXCELLENT = 0 + 80 = 80 ✓ (matches!)
```

**Question:** This one actually matches! Should we keep STEPS=20 for PLAYER_RATING?
- [X] Yes - Keep STEPS=20 (perfect match)

**Recommendation:** Yes, STEPS=20 is perfect.

---

### Q3: Current TEAM_QUALITY Doesn't Match Formula
**Current TEAM_QUALITY_SCORING thresholds:**
```
VERY_POOR: 25
POOR: 18
GOOD: 10
EXCELLENT: 5
```

**Using new formula (BASE_POSITION=0, DIRECTION=DECREASING, STEPS=7):**
```
EXCELLENT = 0 + 7 = 7
GOOD = 0 + 14 = 14
POOR = 0 + 21 = 21
VERY_POOR = 0 + 28 = 28
```

**Difference:**
- Current: E=5, G=10, P=18, VP=25
- Formula: E=7, G=14, P=21, VP=28

**Question:** Should we:
- [ ] A: Use new formula values (accept the 2-4 point shift)
- [X] B: Adjust STEPS to match better (STEPS=6.25 → E=6.25, G=12.5, P=18.75, VP=25)
- [ ] C: Use BASE_POSITION=1.5 with STEPS=6.25 to get closer

**Recommendation:** Option A (use new formula) - the shift is small and simplifies to STEPS=7.

---

### Q4: Current PERFORMANCE Doesn't Match Formula
**Current PERFORMANCE_SCORING thresholds:**
```
VERY_POOR: -0.2
POOR: -0.1
GOOD: 0.1
EXCELLENT: 0.2
```

**Using new formula (BASE_POSITION=0, DIRECTION=BI_EXCELLENT_HI, STEPS=0.1):**
```
VERY_POOR = 0 - (0.1 * 1.5) = -0.15
POOR = 0 - (0.1 * 0.5) = -0.05
GOOD = 0 + (0.1 * 0.5) = 0.05
EXCELLENT = 0 + (0.1 * 1.5) = 0.15
```

**Difference:**
- Current: VP=-0.2, P=-0.1, G=0.1, E=0.2
- Formula: VP=-0.15, P=-0.05, G=0.05, E=0.15

**Question:** Should we:
- [ ] A: Use new formula values (narrower bands: ±0.15 instead of ±0.2)
- [ ] B: Use STEPS=0.133 to match current exactly (VP=-0.2, P=-0.067, G=0.067, E=0.2) - awkward
- [X] C: Use STEPS=0.1 but change formula to use 2x instead of 1.5x (VP=-0.2, P=-0.1, G=0.1, E=0.2) - perfect match!

**Recommendation:** Option C - Change bidirectional formula to use 1x and 2x instead of 0.5x and 1.5x. This matches current thresholds perfectly and is conceptually simpler.

---

### Q5: Current MATCHUP Doesn't Match Formula
**Current MATCHUP_SCORING thresholds:**
```
VERY_POOR: -15
POOR: -6
GOOD: 6
EXCELLENT: 15
```

**Using new formula (BASE_POSITION=0, DIRECTION=BI_EXCELLENT_HI, STEPS=6):**
```
VERY_POOR = 0 - (6 * 1.5) = -9
POOR = 0 - (6 * 0.5) = -3
GOOD = 0 + (6 * 0.5) = 3
EXCELLENT = 0 + (6 * 1.5) = 9
```

**Difference:**
- Current: VP=-15, P=-6, G=6, E=15
- Formula: VP=-9, P=-3, G=3, E=9

**Question:** Should we:
- [ ] A: Use STEPS=10 with current formula (VP=-15, P=-5, G=5, E=15) - close but not exact
- [ ] B: Use STEPS=6 but change formula to 1x/2.5x (VP=-15, P=-6, G=6, E=15) - perfect match but awkward multiplier
- [X] C: Use STEPS=7.5 with 1x/2x formula (VP=-15, P=-7.5, G=7.5, E=15) - matches VP/E, smoother P/G
- [ ] D: Use new formula values (narrower bands)

**Recommendation:** If we adopt the 1x/2x formula for bidirectional (per Q4), then Option C with STEPS=7.5 gives VP=-15, P=-7.5, G=7.5, E=15. Close to current, cleaner multipliers.

---

## Recommended Formula Adjustment

Based on Q4 and Q5, I recommend changing the **BI_EXCELLENT_HI** and **BI_EXCELLENT_LOW** formulas to use **1x and 2x** instead of 0.5x and 1.5x:

**BI_EXCELLENT_HI** (revised):
```
VERY_POOR = BASE_POSITION - (STEPS * 2)
POOR = BASE_POSITION - (STEPS * 1)
GOOD = BASE_POSITION + (STEPS * 1)
EXCELLENT = BASE_POSITION + (STEPS * 2)
```

**BI_EXCELLENT_LOW** (revised):
```
EXCELLENT = BASE_POSITION - (STEPS * 2)
GOOD = BASE_POSITION - (STEPS * 1)
POOR = BASE_POSITION + (STEPS * 1)
VERY_POOR = BASE_POSITION + (STEPS * 2)
```

**Benefits:**
- Simpler multipliers (1x, 2x vs. 0.5x, 1.5x)
- Matches PERFORMANCE exactly with STEPS=0.1
- Matches MATCHUP closely with STEPS=7.5 (VP=-15, P=-7.5, G=7.5, E=15)
- Conceptually cleaner (symmetric around BASE_POSITION)

---

## Summary of Recommended STEPS Values

If we adopt the 1x/2x formula for bidirectional:

| Scoring Type | BASE_POSITION | DIRECTION | STEPS | Result Thresholds |
|--------------|---------------|-----------|-------|-------------------|
| ADP_SCORING | 0 | DECREASING | 37.5 | E=37.5, G=75, P=112.5, VP=150 |
| PLAYER_RATING | 0 | INCREASING | 20 | VP=20, P=40, G=60, E=80 |
| TEAM_QUALITY | 0 | DECREASING | 7 | E=7, G=14, P=21, VP=28 |
| PERFORMANCE | 0.0 | BI_EXCELLENT_HI | 0.1 | VP=-0.2, P=-0.1, G=0.1, E=0.2 |
| MATCHUP | 0 | BI_EXCELLENT_HI | 7.5 | VP=-15, P=-7.5, G=7.5, E=15 |

**Alternatives:**
- Accept formula as-is (0.5x/1.5x) and new threshold values
- Use non-zero BASE_POSITION to match current thresholds better

---

## Medium Priority Questions

### Q6: Simulation STEPS Ranges
**Context:** Spec provides test ranges for STEPS optimization.

**Question:** Should simulation test ranges be:
- [X] A: Centered around recommended STEPS (e.g., ADP: 30-45 if using STEPS=37.5)
- [ ] B: Use spec ranges as-is (ADP: 20-40) even if recommended STEPS changes

**Recommendation:** Option A - center ranges around actual recommended STEPS.

---

### Q7: Migration Strategy for Existing Configs
**Context:** Existing configs have hardcoded thresholds that don't match formula.

**Question:** How should we migrate?
- [ ] A: Calculate STEPS to match existing thresholds as closely as possible
- [X] B: Use recommended STEPS and accept threshold changes
- [ ] C: Provide migration warning showing before/after thresholds

**Recommendation:** Option C - Calculate matching STEPS, but show warning with before/after comparison.

---

### Q8: Backward Compatibility
**Context:** Should we support loading old hardcoded threshold configs?

**Question:**
- [ ] A: Support both formats (detect and handle appropriately)
- [X] B: Require migration before loading
- [ ] C: Auto-migrate on load (one-time conversion)

**Recommendation:** Option A - Support both formats for gradual migration.

---

## Low Priority Questions

### Q9: Calculated Thresholds Display
**Question:** Should we include calculated thresholds in config files for transparency?
```json
"THRESHOLDS": {
    "BASE_POSITION": 0,
    "DIRECTION": "DECREASING",
    "STEPS": 37.5,
    "_calculated": {
        "VERY_POOR": 150,
        "POOR": 112.5,
        "GOOD": 75,
        "EXCELLENT": 37.5
    }
}
```

**Recommendation:** Yes for optimal configs, optional for generated configs.
Sure go ahead and do this

---

### Q10: Validation Strictness
**Question:** Should we validate that calculated thresholds make sense (e.g., no negative values for ADP)?

**Recommendation:** Yes - add scoring-type-specific validation rules.
Yes

---

## Next Steps

1. **User answers Q1-Q5** (critical formula questions)
2. **Finalize formula** (0.5x/1.5x or 1x/2x for bidirectional)
3. **Finalize recommended STEPS** values
4. Create TODO file with implementation plan
5. Create code changes tracking document
6. Begin implementation

---

## Notes

- New specification is much simpler than previous version
- Main challenge is matching current threshold values with new formula
- Bidirectional formula adjustment (1x/2x) would help significantly
- All BASE_POSITION = 0 simplifies implementation
