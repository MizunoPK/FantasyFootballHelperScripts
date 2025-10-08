# JSON Parameter System

This document describes the JSON-based parameter system used for fantasy football scoring calculations across DraftHelper, StarterHelper, and Simulation systems.

## Overview

All scoring parameters are stored in `parameters.json` files and loaded dynamically at runtime. This allows for easy parameter tuning, A/B testing, and simulation optimization without modifying code.

## Parameter File Location

**Default**: `shared_files/parameters.json`

**Simulation**: `draft_helper/simulation/parameters/parameter_runs/` (generated combinations)

## Loading Parameters

### DraftHelper
```python
from draft_helper.draft_helper import DraftHelper
helper = DraftHelper(parameter_json_path='shared_files/parameters.json')
```

### StarterHelper
```python
from starter_helper.starter_helper import StarterHelper
helper = StarterHelper(parameter_json_path='shared_files/parameters.json')
```

### Accessing Parameters
```python
from shared_files.parameter_json_manager import ParameterJsonManager
params = ParameterJsonManager('shared_files/parameters.json')

# Attribute access
print(params.NORMALIZATION_MAX_SCALE)  # 100.0

# Dictionary access
print(params['BASE_BYE_PENALTY'])  # 28.85

# Nested structure
print(params.INJURY_PENALTIES['HIGH'])  # 78.22
```

## Parameter Definitions

All parameters are **required** and must be present in the JSON file. Missing parameters will cause the system to exit with a clear error message.

### 1. Normalization Parameters

#### NORMALIZATION_MAX_SCALE
- **Type**: float
- **Range**: 50.0 - 200.0
- **Description**: Maximum scale value for normalizing fantasy points (0-100 scale by default)
- **Effect**: Higher values compress score differences; lower values expand them
- **Example**: 100.0 (default)

### 2. Draft Order Bonus Parameters

#### DRAFT_ORDER_PRIMARY_BONUS
- **Type**: float
- **Range**: 0.0 - 100.0
- **Description**: Bonus points for drafting priority position in a round
- **Effect**: Incentivizes drafting high-value positions (e.g., FLEX in round 1)
- **Example**: 74.76

#### DRAFT_ORDER_SECONDARY_BONUS
- **Type**: float
- **Range**: 0.0 - 100.0
- **Description**: Bonus points for drafting secondary priority position in a round
- **Effect**: Provides secondary incentives (e.g., QB in round 1)
- **Example**: 38.57

**Note**: DRAFT_ORDER structure in config defines which positions get P/S bonuses per round.

### 3. Bye Week Penalty

#### BASE_BYE_PENALTY
- **Type**: float
- **Range**: 0.0 - 100.0
- **Description**: Penalty points for drafting players with overlapping bye weeks
- **Effect**: Only applies in draft mode; encourages bye week diversity
- **Example**: 28.85

### 4. Injury Penalties (Nested Structure)

#### INJURY_PENALTIES
- **Type**: dict with keys: LOW, MEDIUM, HIGH
- **Range**: 0.0 - 100.0 per level
- **Description**: Penalty points based on injury risk level
- **Effect**:
  - LOW: No penalty (healthy players)
  - MEDIUM: Moderate penalty (questionable, probable)
  - HIGH: Heavy penalty (out, IR, doubtful)
- **Structure**:
```json
"INJURY_PENALTIES": {
  "LOW": 0,
  "MEDIUM": 4.68,
  "HIGH": 78.22
}
```
- **Trade Mode**: Can be toggled off for roster players via `APPLY_INJURY_PENALTY_TO_ROSTER`

### 5. ADP (Average Draft Position) Multipliers

#### ADP_EXCELLENT_MULTIPLIER
- **Type**: float
- **Range**: 0.5 - 2.0
- **Description**: Multiplier for players with excellent ADP (1-50)
- **Effect**: Boosts highly-drafted players
- **Example**: 1.08 (+8% boost)

#### ADP_GOOD_MULTIPLIER
- **Type**: float
- **Range**: 0.5 - 2.0
- **Description**: Multiplier for players with good ADP (51-100)
- **Effect**: Slight boost for mid-tier players
- **Example**: 1.08 (+8% boost)

#### ADP_POOR_MULTIPLIER
- **Type**: float
- **Range**: 0.5 - 2.0
- **Description**: Multiplier for players with poor ADP (101+)
- **Effect**: Penalty for late-drafted players
- **Example**: 0.92 (-8% penalty)

### 6. Player Rating Multipliers

#### PLAYER_RATING_EXCELLENT_MULTIPLIER
- **Type**: float
- **Range**: 0.5 - 2.0
- **Description**: Multiplier for elite players (rating 70+)
- **Effect**: Significantly boosts star players
- **Example**: 1.15 (+15% boost)

#### PLAYER_RATING_GOOD_MULTIPLIER
- **Type**: float
- **Range**: 0.5 - 2.0
- **Description**: Multiplier for good players (rating 50-69)
- **Effect**: Moderate boost for solid players
- **Example**: 1.15 (+15% boost)

#### PLAYER_RATING_POOR_MULTIPLIER
- **Type**: float
- **Range**: 0.5 - 2.0
- **Description**: Multiplier for poor players (rating <50)
- **Effect**: Penalty for low-rated players
- **Example**: 0.90 (-10% penalty)

### 7. Team Quality Multipliers

#### TEAM_EXCELLENT_MULTIPLIER
- **Type**: float
- **Range**: 0.5 - 2.0
- **Description**: Multiplier for players on excellent teams (top offensive ranking)
- **Effect**: Boosts players on high-powered offenses
- **Example**: 1.06 (+6% boost)

#### TEAM_GOOD_MULTIPLIER
- **Type**: float
- **Range**: 0.5 - 2.0
- **Description**: Multiplier for players on good teams (mid-tier offenses)
- **Effect**: Slight boost for above-average teams
- **Example**: 1.06 (+6% boost)

#### TEAM_POOR_MULTIPLIER
- **Type**: float
- **Range**: 0.5 - 2.0
- **Description**: Multiplier for players on poor teams (bottom offenses)
- **Effect**: Penalty for weak offensive environments
- **Example**: 0.94 (-6% penalty)

### 8. Consistency Multipliers (Volatility-Based)

#### CONSISTENCY_LOW_MULTIPLIER
- **Type**: float
- **Range**: 0.5 - 2.0
- **Description**: Multiplier for consistent players (CV < 0.3)
- **Effect**: Rewards players with reliable week-to-week performance
- **Example**: 1.08 (+8% boost)
- **CV**: Coefficient of Variation = std_dev / mean

#### CONSISTENCY_MEDIUM_MULTIPLIER
- **Type**: float
- **Range**: 0.5 - 2.0
- **Description**: Multiplier for average consistency players (CV 0.3-0.6)
- **Effect**: Neutral - no adjustment
- **Example**: 1.00 (no change)

#### CONSISTENCY_HIGH_MULTIPLIER
- **Type**: float
- **Range**: 0.5 - 2.0
- **Description**: Multiplier for volatile players (CV > 0.6)
- **Effect**: Penalizes boom-or-bust players
- **Example**: 0.92 (-8% penalty)

**Note**: Consistency scoring can be toggled via `ENABLE_CONSISTENCY_SCORING` in config.

### 9. Matchup Multipliers (Starter Helper Only)

#### MATCHUP_EXCELLENT_MULTIPLIER
- **Type**: float
- **Range**: 0.5 - 2.0
- **Description**: Multiplier for excellent matchups (offense rank - defense rank > 10)
- **Effect**: Boosts players facing weak defenses
- **Example**: 1.20 (+20% boost)

#### MATCHUP_GOOD_MULTIPLIER
- **Type**: float
- **Range**: 0.5 - 2.0
- **Description**: Multiplier for good matchups (rank difference 5-10)
- **Effect**: Moderate boost for favorable matchups
- **Example**: 1.10 (+10% boost)

#### MATCHUP_NEUTRAL_MULTIPLIER
- **Type**: float
- **Range**: 0.5 - 2.0
- **Description**: Multiplier for neutral matchups (rank difference -5 to 5)
- **Effect**: No adjustment for even matchups
- **Example**: 1.00 (no change)

#### MATCHUP_POOR_MULTIPLIER
- **Type**: float
- **Range**: 0.5 - 2.0
- **Description**: Multiplier for poor matchups (rank difference -10 to -5)
- **Effect**: Penalty for tough matchups
- **Example**: 0.90 (-10% penalty)

#### MATCHUP_VERY_POOR_MULTIPLIER
- **Type**: float
- **Range**: 0.5 - 2.0
- **Description**: Multiplier for very poor matchups (rank difference < -10)
- **Effect**: Heavy penalty for elite defenses
- **Example**: 0.80 (-20% penalty)

**Note**: Matchup multipliers only apply to QB, RB, WR, TE (not K, DST).

## Example Parameter File

```json
{
  "config_name": "optimal_2025-10-05",
  "description": "Optimized parameters from simulation run",
  "parameters": {
    "NORMALIZATION_MAX_SCALE": 100.0,
    "DRAFT_ORDER_PRIMARY_BONUS": 74.76,
    "DRAFT_ORDER_SECONDARY_BONUS": 38.57,
    "BASE_BYE_PENALTY": 28.85,
    "INJURY_PENALTIES": {
      "LOW": 0,
      "MEDIUM": 4.68,
      "HIGH": 78.22
    },
    "ADP_EXCELLENT_MULTIPLIER": 1.08,
    "ADP_GOOD_MULTIPLIER": 1.08,
    "ADP_POOR_MULTIPLIER": 0.92,
    "PLAYER_RATING_EXCELLENT_MULTIPLIER": 1.15,
    "PLAYER_RATING_GOOD_MULTIPLIER": 1.15,
    "PLAYER_RATING_POOR_MULTIPLIER": 0.90,
    "TEAM_EXCELLENT_MULTIPLIER": 1.06,
    "TEAM_GOOD_MULTIPLIER": 1.06,
    "TEAM_POOR_MULTIPLIER": 0.94,
    "CONSISTENCY_LOW_MULTIPLIER": 1.08,
    "CONSISTENCY_MEDIUM_MULTIPLIER": 1.00,
    "CONSISTENCY_HIGH_MULTIPLIER": 0.92,
    "MATCHUP_EXCELLENT_MULTIPLIER": 1.20,
    "MATCHUP_GOOD_MULTIPLIER": 1.10,
    "MATCHUP_NEUTRAL_MULTIPLIER": 1.00,
    "MATCHUP_POOR_MULTIPLIER": 0.90,
    "MATCHUP_VERY_POOR_MULTIPLIER": 0.80
  }
}
```

## Scoring Flow

### DraftHelper - Add to Roster (8 steps)
1. **Normalize** fantasy points (0-NORMALIZATION_MAX_SCALE)
2. **ADP multiplier** (excellent/good/poor based on draft position)
3. **Player rating multiplier** (excellent/good/poor based on player quality)
4. **Team quality multiplier** (excellent/good/poor based on team offense)
5. **Consistency multiplier** (LOW/MEDIUM/HIGH based on CV)
6. **Draft order bonus** (position-specific per round from DRAFT_ORDER)
7. **Bye week penalty** (BASE_BYE_PENALTY for overlapping bye weeks)
8. **Injury penalty** (LOW/MEDIUM/HIGH from INJURY_PENALTIES)

### DraftHelper - Trade/Waiver (7 steps)
Same as above **without** Draft Order bonus (step 6)

### StarterHelper (4 steps)
1. **Base projections** from weekly CSV data
2. **Matchup multiplier** (based on offense vs defense rankings)
3. **Consistency multiplier** (LOW/MEDIUM/HIGH based on CV)
4. **Binary injury filter** (zero out non-ACTIVE/QUESTIONABLE players)

## Creating Custom Parameter Files

1. **Copy the template**:
```bash
cp shared_files/parameters.json shared_files/custom_parameters.json
```

2. **Edit values** (maintain all 22 parameters):
```json
{
  "config_name": "my_custom_config",
  "description": "Custom parameter set for testing",
  "parameters": {
    "NORMALIZATION_MAX_SCALE": 120.0,
    "DRAFT_ORDER_PRIMARY_BONUS": 60.0,
    ...
  }
}
```

3. **Validate** by loading in Python:
```python
from shared_files.parameter_json_manager import ParameterJsonManager
params = ParameterJsonManager('shared_files/custom_parameters.json')
# If no errors, parameters are valid
```

4. **Use in scripts**:
```python
helper = DraftHelper(parameter_json_path='shared_files/custom_parameters.json')
```

## Simulation Parameter Sets

For simulation optimization, parameter files are organized in:
- **parameter_sets/**: Multi-value parameter configurations (arrays for each param)
- **parameter_runs/**: Generated single-value combinations (one file per run)

See `draft_helper/simulation/README.md` for simulation workflow details.

## Validation

ParameterJsonManager validates on load:
- ✅ All 22 parameters present
- ✅ Correct types (float for all except INJURY_PENALTIES dict)
- ✅ Valid ranges per parameter
- ✅ Nested INJURY_PENALTIES structure (LOW, MEDIUM, HIGH keys)
- ❌ Exits with clear error if validation fails

## Troubleshooting

**Error: "Missing required parameter: X"**
- Add the missing parameter to your JSON file with a valid value

**Error: "INJURY_PENALTIES must be a dict with keys: LOW, MEDIUM, HIGH"**
- Ensure INJURY_PENALTIES uses nested structure (not flat INJURY_PENALTIES_HIGH)

**Error: "Parameter X out of valid range"**
- Check parameter value is within the documented range

**Error: "Configuration file not found"**
- Verify file path is correct and file exists
- Use absolute paths or paths relative to script location

## Best Practices

1. **Always keep a backup** of working parameters.json
2. **Document changes** in config_name and description fields
3. **Test with small changes** before large parameter sweeps
4. **Use simulation** to optimize parameters systematically
5. **Validate immediately** after editing JSON files
6. **Version control** parameter files that produce good results

## Parameter Tuning Tips

- **Multipliers near 1.0**: Subtle adjustments (1.05 = +5%)
- **Bonuses**: Impact absolute scores, test in 5-10 point increments
- **Penalties**: Balance risk vs reward, start conservative
- **Consistency**: Tune based on whether you want floor or ceiling
- **Matchup**: Higher values = more week-to-week variance in recommendations

## Related Files

- `shared_files/parameter_json_manager.py` - Parameter loading and validation
- `shared_files/configs/draft_helper_config.py` - Non-parameter draft settings
- `shared_files/configs/starter_helper_config.py` - Non-parameter starter settings
- `draft_helper/simulation/parameter_loader.py` - Simulation parameter loading

---

**Last Updated**: October 2025
**Total Parameters**: 22 (INJURY_PENALTIES counts as 1 nested dict)
