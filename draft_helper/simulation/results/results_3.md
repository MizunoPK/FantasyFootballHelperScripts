# Draft Simulation Results

**Analysis Date**: 2025-09-24T20:42:45.357023
**Total Configurations Tested**: 297
**Total Simulations Run**: 14850

## 🏆 Optimal Configuration

**Configuration Parameters:**
- `INJURY_PENALTIES_MEDIUM`: 15
- `INJURY_PENALTIES_HIGH`: 30
- `POS_NEEDED_SCORE`: 65
- `PROJECTION_BASE_SCORE`: 100
- `BASE_BYE_PENALTY`: 5
- `DRAFT_ORDER_WEIGHTS`: 1.2

**Performance Metrics:**
- **Win Percentage**: 60.7%
- **Average Total Points**: 2148.6
- **Points Per Game**: 126.4
- **Score Consistency**: 8.9
- **Average Ranking**: 4.1
- **Simulations**: 50

## 📊 Top 10 Configurations

| Rank | Win % | Total Pts | PPG | Consistency | Key Parameters |
|------|-------|-----------|-----|-------------|----------------|
| 1 | 60.7% | 2149 | 126.4 | 8.9 | MEDIUM=15, HIGH=30, SCORE=65 |
| 2 | 58.0% | 2157 | 126.9 | 8.4 | MEDIUM=10, HIGH=40, SCORE=65 |
| 3 | 56.8% | 2152 | 126.6 | 7.9 | MEDIUM=20, HIGH=35, SCORE=65 |
| 4 | 56.8% | 2143 | 126.1 | 8.2 | MEDIUM=20, HIGH=20, SCORE=60 |
| 5 | 56.5% | 2136 | 125.7 | 8.6 | MEDIUM=10, HIGH=30, SCORE=65 |
| 6 | 56.2% | 2137 | 125.7 | 8.3 | MEDIUM=20, HIGH=45, SCORE=65 |
| 7 | 55.9% | 2144 | 126.1 | 8.9 | MEDIUM=20, HIGH=40, SCORE=65 |
| 8 | 55.5% | 2145 | 126.2 | 9.0 | MEDIUM=5, HIGH=30, SCORE=60 |
| 9 | 55.3% | 2139 | 125.8 | 7.9 | MEDIUM=20, HIGH=25, SCORE=60 |
| 10 | 55.2% | 2150 | 126.5 | 8.2 | MEDIUM=20, HIGH=30, SCORE=65 |

## 🔍 Parameter Analysis

### INJURY_PENALTIES_MEDIUM

- **25**: 50.8% win rate
- **5**: 50.8% win rate
- **20**: 50.3% win rate
- **15**: 50.1% win rate
- **10**: 49.9% win rate
- **30**: 49.7% win rate
- **0**: 44.7% win rate

### INJURY_PENALTIES_HIGH

- **50**: 51.4% win rate
- **25**: 51.2% win rate
- **40**: 51.1% win rate
- **45**: 50.2% win rate
- **30**: 49.9% win rate
- **35**: 49.8% win rate
- **20**: 49.6% win rate
- **15**: 48.5% win rate
- **55**: 47.4% win rate

### POS_NEEDED_SCORE

- **85**: 50.5% win rate
- **65**: 50.4% win rate
- **70**: 50.2% win rate
- **60**: 50.0% win rate
- **45**: 49.6% win rate
- **50**: 49.6% win rate
- **75**: 49.4% win rate
- **55**: 49.4% win rate
- **80**: 48.2% win rate

### PROJECTION_BASE_SCORE

- **115**: 53.4% win rate
- **70**: 51.4% win rate
- **80**: 51.3% win rate
- **105**: 50.9% win rate
- **85**: 50.3% win rate
- **95**: 50.1% win rate
- **100**: 50.0% win rate
- **90**: 49.8% win rate
- **110**: 49.5% win rate
- **75**: 49.2% win rate

### BASE_BYE_PENALTY

- **0**: 50.8% win rate
- **5**: 50.8% win rate
- **30**: 50.6% win rate
- **20**: 50.2% win rate
- **15**: 50.1% win rate
- **10**: 49.7% win rate
- **25**: 48.9% win rate

### DRAFT_ORDER_WEIGHTS

- **1.2**: 51.8% win rate
- **1.1**: 51.5% win rate
- **1.0**: 50.1% win rate
- **0.9**: 49.8% win rate
- **0.8**: 49.0% win rate

## 📈 Performance Distribution

### Win Percentage Statistics
- **Mean**: 50.1%
- **Median**: 50.5%
- **Range**: 40.8% - 60.7%
- **Standard Deviation**: 0.030

## 📋 Statistical Summary

- **Performance Improvement Range**: 19.9%
- **Configurations Above 50% Win Rate**: 162
- **Configurations Above 60% Win Rate**: 1
- **Configurations Above 70% Win Rate**: 0

## 💡 Key Insights

1. **Configuration optimization can significantly improve draft performance**
2. **Best configuration achieved 19.9% better win rate than worst**
3. **0.3% of configurations achieved >60% win rate**
4. **Parameter tuning has measurable impact on draft success**

## 🎯 Recommendations

**Use the optimal configuration parameters identified above for best results.**

**Key parameter adjustments:**
- Set `INJURY_PENALTIES_MEDIUM` to `15`
- Set `INJURY_PENALTIES_HIGH` to `30`
- Set `POS_NEEDED_SCORE` to `65`
- Set `PROJECTION_BASE_SCORE` to `100`
- Set `BASE_BYE_PENALTY` to `5`
- Set `DRAFT_ORDER_WEIGHTS` to `1.2`

**Monitor these high-impact parameters:**
- `INJURY_PENALTIES_MEDIUM` (impact range: 6.1%)
- `PROJECTION_BASE_SCORE` (impact range: 4.2%)
- `INJURY_PENALTIES_HIGH` (impact range: 4.0%)
