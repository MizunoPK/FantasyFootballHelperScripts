# Draft Simulation Results

**Analysis Date**: 2025-09-24T09:26:48.139063
**Total Configurations Tested**: 1398
**Total Simulations Run**: 13980

## 🏆 Optimal Configuration

**Configuration Parameters:**
- `INJURY_PENALTIES_MEDIUM`: 0
- `INJURY_PENALTIES_HIGH`: 30
- `POS_NEEDED_SCORE`: 65
- `PROJECTION_BASE_SCORE`: 90
- `BASE_BYE_PENALTY`: 20
- `DRAFT_ORDER_WEIGHTS`: 1.0

**Performance Metrics:**
- **Win Percentage**: 70.0%
- **Average Total Points**: 2185.1
- **Points Per Game**: 128.5
- **Score Consistency**: 7.3
- **Average Ranking**: 2.6
- **Simulations**: 10

## 📊 Top 10 Configurations

| Rank | Win % | Total Pts | PPG | Consistency | Key Parameters |
|------|-------|-----------|-----|-------------|----------------|
| 1 | 70.0% | 2185 | 128.5 | 7.3 | MEDIUM=0, HIGH=30, SCORE=65 |
| 2 | 68.8% | 2181 | 128.3 | 8.1 | MEDIUM=15, HIGH=45, SCORE=75 |
| 3 | 68.2% | 2182 | 128.3 | 8.0 | MEDIUM=15, HIGH=40, SCORE=65 |
| 4 | 65.9% | 2178 | 128.1 | 7.6 | MEDIUM=20, HIGH=35, SCORE=70 |
| 5 | 65.9% | 2174 | 127.9 | 7.0 | MEDIUM=15, HIGH=30, SCORE=60 |
| 6 | 65.9% | 2172 | 127.8 | 9.0 | MEDIUM=25, HIGH=35, SCORE=75 |
| 7 | 65.3% | 2180 | 128.2 | 7.6 | MEDIUM=10, HIGH=40, SCORE=65 |
| 8 | 65.3% | 2174 | 127.9 | 7.4 | MEDIUM=25, HIGH=35, SCORE=75 |
| 9 | 65.3% | 2169 | 127.6 | 8.5 | MEDIUM=10, HIGH=30, SCORE=65 |
| 10 | 64.7% | 2167 | 127.5 | 7.6 | MEDIUM=25, HIGH=25, SCORE=65 |

## 🔍 Parameter Analysis

### INJURY_PENALTIES_MEDIUM

- **0**: 52.5% win rate
- **15**: 50.7% win rate
- **35**: 50.4% win rate
- **10**: 49.9% win rate
- **25**: 49.8% win rate
- **20**: 49.4% win rate
- **30**: 48.7% win rate
- **5**: 48.0% win rate

### INJURY_PENALTIES_HIGH

- **60**: 51.8% win rate
- **25**: 50.6% win rate
- **20**: 50.3% win rate
- **45**: 50.1% win rate
- **30**: 50.0% win rate
- **35**: 49.9% win rate
- **40**: 49.7% win rate
- **50**: 49.4% win rate
- **15**: 49.0% win rate
- **55**: 48.4% win rate

### POS_NEEDED_SCORE

- **90**: 51.1% win rate
- **50**: 51.0% win rate
- **60**: 50.3% win rate
- **45**: 50.2% win rate
- **85**: 50.2% win rate
- **80**: 50.0% win rate
- **95**: 49.9% win rate
- **75**: 49.8% win rate
- **65**: 49.6% win rate
- **70**: 49.5% win rate
- **55**: 48.4% win rate

### PROJECTION_BASE_SCORE

- **120**: 50.4% win rate
- **100**: 50.1% win rate
- **95**: 49.9% win rate
- **110**: 49.8% win rate
- **130**: 49.8% win rate
- **85**: 49.7% win rate
- **115**: 49.7% win rate
- **90**: 49.6% win rate
- **125**: 49.5% win rate
- **105**: 49.1% win rate
- **75**: 48.8% win rate
- **80**: 48.4% win rate
- **135**: 47.9% win rate

### BASE_BYE_PENALTY

- **25**: 51.2% win rate
- **0**: 50.6% win rate
- **5**: 50.1% win rate
- **10**: 49.8% win rate
- **20**: 49.6% win rate
- **30**: 49.6% win rate
- **15**: 49.3% win rate

### DRAFT_ORDER_WEIGHTS

- **0.8**: 50.5% win rate
- **1.2**: 50.0% win rate
- **0.9**: 49.9% win rate
- **1.0**: 49.9% win rate
- **1.1**: 49.2% win rate

## 📈 Performance Distribution

### Win Percentage Statistics
- **Mean**: 49.9%
- **Median**: 50.0%
- **Range**: 28.2% - 70.0%
- **Standard Deviation**: 0.065

## 📋 Statistical Summary

- **Performance Improvement Range**: 41.8%
- **Configurations Above 50% Win Rate**: 673
- **Configurations Above 60% Win Rate**: 64
- **Configurations Above 70% Win Rate**: 0

## 💡 Key Insights

1. **Configuration optimization can significantly improve draft performance**
2. **Best configuration achieved 41.8% better win rate than worst**
3. **4.6% of configurations achieved >60% win rate**
4. **Parameter tuning has measurable impact on draft success**

## 🎯 Recommendations

**Use the optimal configuration parameters identified above for best results.**

**Key parameter adjustments:**
- Set `INJURY_PENALTIES_MEDIUM` to `0`
- Set `INJURY_PENALTIES_HIGH` to `30`
- Set `POS_NEEDED_SCORE` to `65`
- Set `PROJECTION_BASE_SCORE` to `90`
- Set `BASE_BYE_PENALTY` to `20`
- Set `DRAFT_ORDER_WEIGHTS` to `1.0`

**Monitor these high-impact parameters:**
- `INJURY_PENALTIES_MEDIUM` (impact range: 4.6%)
- `INJURY_PENALTIES_HIGH` (impact range: 3.4%)
- `POS_NEEDED_SCORE` (impact range: 2.7%)
