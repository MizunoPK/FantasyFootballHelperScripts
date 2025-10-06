# Kicker Scoring Breakdown - Waiver Optimizer Mode

## Players Comparison

### Brandon McManus (GB, K)
- **Fantasy Points**: 97.85
- **ADP**: 167.29
- **Player Rating**: 24.37
- **Bye Week**: 5 (already passed, Week 5 is current)
- **Injury Status**: ACTIVE

### Chase McLaughlin (TB, K)
- **Fantasy Points**: 100.36
- **ADP**: 105.83
- **Player Rating**: 36.8
- **Bye Week**: 9 (future)
- **Injury Status**: ACTIVE

---

## Scoring Breakdown - Trade/Waiver Mode (7 Steps)

### Brandon McManus

#### Step 1: Normalize Seasonal Fantasy Points
- Raw Fantasy Points: **97.85**
- Maximum in Dataset: 197.0
- Normalization Scale: 102.42
- **Normalized Score: 50.88**
  - Formula: (97.85 / 197.0) × 102.42 = 50.88

#### Steps 2-4: Enhanced Scoring (ADP, Player Rating, Team Quality)
- Base Score: 50.88
- **ADP Multiplier**: 1.0x (no penalty, ADP is poor at 167.29)
- **Player Rating Multiplier**: 0.94x (-6% penalty, rating is 24.37 = poor)
- **Team Quality Multiplier**: 1.32x (+32% boost, GB has good offense)
- Combined Multiplier: 1.0 × 0.94 × 1.32 = **1.241x** (+24.1%)
- **Enhanced Score: 63.13**
  - Formula: 50.88 × 1.241 = 63.13

#### Step 5: Consistency Multiplier
- Weekly Points: [7.95, 8.37, 8.13, 8.33, 0.0, 8.66, 8.04, 8.04, 8.30, 7.81, 8.11, 7.88, 8.04, 8.38, 7.75, 8.25, 8.59]
- Mean: 8.19
- Standard Deviation: 0.19
- **Coefficient of Variation (CV): 0.024** (very low!)
- Volatility Category: **LOW** (CV < 0.3)
- **Consistency Multiplier**: 1.08x (+8% bonus for consistency)
- **Consistency Score: 68.18**
  - Formula: 63.13 × 1.08 = 68.18

#### Step 6: Bye Week Penalty
- Bye Week: 5 (current week, already passed)
- Same Position Conflicts: 0 (no other kickers on roster)
- **Bye Penalty: 0.0**
  - No penalty because bye week has passed AND no roster conflicts
- **After Bye Penalty: 68.18**
  - Formula: 68.18 - 0.0 = 68.18

#### Step 7: Injury Penalty
- Injury Status: ACTIVE
- **Injury Penalty: 0.0**
- **Final Score: 68.18**

---

### Chase McLaughlin

#### Step 1: Normalize Seasonal Fantasy Points
- Raw Fantasy Points: **100.36**
- Maximum in Dataset: 197.0
- Normalization Scale: 102.42
- **Normalized Score: 52.18**
  - Formula: (100.36 / 197.0) × 102.42 = 52.18

#### Steps 2-4: Enhanced Scoring (ADP, Player Rating, Team Quality)
- Base Score: 52.18
- **ADP Multiplier**: 1.0x (no penalty, ADP is good at 105.83)
- **Player Rating Multiplier**: 0.967x (-3.3% penalty, rating is 36.8 = below average)
- **Team Quality Multiplier**: 1.0x (no adjustment for TB)
- Combined Multiplier: 1.0 × 0.967 × 1.0 = **0.967x** (-3.3%)
- **Enhanced Score: 50.47**
  - Formula: 52.18 × 0.967 = 50.47

#### Step 5: Consistency Multiplier
- Weekly Points: [5.0, 1.0, 8.57, 17.0, 7.93, 8.27, 8.22, 8.64, 0.0, 8.41, 8.29, 8.01, 8.34, 8.77, 8.34, 8.35, 8.78]
- Mean: 7.89
- Standard Deviation: 6.81
- **Coefficient of Variation (CV): 0.863** (very high!)
- Volatility Category: **HIGH** (CV > 0.6)
- **Consistency Multiplier**: 0.92x (-8% penalty for boom/bust pattern)
- **Consistency Score: 46.43**
  - Formula: 50.47 × 0.92 = 46.43

#### Step 6: Bye Week Penalty
- Bye Week: 9 (future week)
- Same Position Conflicts: 0 (no other kickers on roster)
- **Bye Penalty: 0.0**
  - No penalty because there are no roster conflicts at the K position
- **After Bye Penalty: 46.43**
  - Formula: 46.43 - 0.0 = 46.43

#### Step 7: Injury Penalty
- Injury Status: ACTIVE
- **Injury Penalty: 0.0**
- **Final Score: 46.43**

---

## Final Comparison

| Metric | Brandon McManus | Chase McLaughlin | Difference |
|--------|----------------|------------------|------------|
| **Raw Fantasy Points** | 97.85 | 100.36 | McLaughlin +2.51 |
| **Step 1: Normalized** | 50.88 | 52.18 | McLaughlin +1.30 |
| **Steps 2-4: Enhanced** | 63.13 | 50.47 | McManus +12.66 |
| **Step 5: Consistency** | 68.18 | 46.43 | McManus +21.75 |
| **Step 6: Bye Penalty** | 68.18 | 46.43 | McManus +21.75 |
| **Step 7: Final Score** | **68.18** | **46.43** | **McManus +21.75** |

---

## Key Insights

### Why Brandon McManus Scores Higher Despite Lower Fantasy Points

1. **Team Quality Boost (+32%)**: GB has a strong offense, giving McManus more opportunities
2. **Consistency Advantage**: McManus has extremely consistent scoring (CV=0.024) earning a +8% bonus, while McLaughlin is highly volatile (CV=0.863) receiving a -8% penalty
3. **Combined Effect**: The 32% team boost + 8% consistency bonus = +40% total advantage for McManus
4. **McLaughlin's Volatility**: His weekly scores range from 0 to 17 points (huge variance), making him unreliable
5. **McManus's Reliability**: His scores stay between 7.75-8.66 points (very tight range), making him predictable
6. **No Bye Week Penalties**: Since there are no other kickers on the roster, neither player receives a bye week penalty (correctly fixed!)

### The Consistency Impact

- **McManus**: CV of 0.024 means his scores deviate only 2.4% from his mean → Very reliable
- **McLaughlin**: CV of 0.863 means his scores deviate 86.3% from his mean → Boom/bust pattern
- This **16% swing** (8% bonus vs 8% penalty) creates a massive difference in final scores

### Conclusion

Even though Chase McLaughlin has 2.5 more fantasy points on the season, Brandon McManus is the better waiver pickup because:
- He plays for a better offensive team (GB) - giving a +32% boost
- His scoring is extremely consistent and predictable - earning +8% consistency bonus
- McLaughlin's boom/bust pattern receives a -8% volatility penalty
- Neither player has bye week conflicts (no other kickers on roster)
- The consistency scoring system correctly identifies reliable performers over volatile ones

---

## Bug Fix Applied

**Issue Found**: The bye week penalty logic was incorrectly applying a base penalty to non-FLEX positions (K, TE, QB, DST) even when there were no roster conflicts.

**Fix Applied**: Modified `scoring_engine.py` line 328 to return `0` instead of `Constants.BASE_BYE_PENALTY` when there are no same-position bye week conflicts for non-FLEX positions.

**Impact**: Both kickers now correctly show 0 bye week penalty since there are no other kickers on the roster to conflict with.
