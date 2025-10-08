# Simulation Parameter Configuration Files

This directory contains JSON configuration files that define parameter values for simulation testing.

## File Format

Each JSON file should follow this structure:

```json
{
  "config_name": "descriptive_name",
  "description": "Brief description of what this configuration tests",
  "parameters": {
    "PARAMETER_NAME": [value1, value2, ...],
    ...
  }
}
```

### Required Fields

- **config_name**: Short identifier for this configuration (used in results)
- **description**: Human-readable description of the configuration purpose
- **parameters**: Dictionary containing all 20 required simulation parameters

### Required Parameters

All configuration files must include these 20 parameters:

**Core Scoring Parameters:**
1. `NORMALIZATION_MAX_SCALE` - Normalization scale for point calculations
2. `DRAFT_ORDER_PRIMARY_BONUS` - Primary position bonus (QB, RB, WR)
3. `DRAFT_ORDER_SECONDARY_BONUS` - Secondary position bonus

**Matchup Multipliers (Starter Helper):**
4. `MATCHUP_EXCELLENT_MULTIPLIER` - Very favorable matchup multiplier
5. `MATCHUP_GOOD_MULTIPLIER` - Favorable matchup multiplier
6. `MATCHUP_NEUTRAL_MULTIPLIER` - Neutral matchup multiplier
7. `MATCHUP_POOR_MULTIPLIER` - Unfavorable matchup multiplier
8. `MATCHUP_VERY_POOR_MULTIPLIER` - Very unfavorable matchup multiplier

**Injury & Bye Penalties:**
9. `INJURY_PENALTIES_MEDIUM` - Medium injury risk penalty points
10. `INJURY_PENALTIES_HIGH` - High injury risk penalty points
11. `BASE_BYE_PENALTY` - Base bye week penalty

**ADP Adjustments:**
12. `ADP_EXCELLENT_MULTIPLIER` - Excellent ADP tier multiplier
13. `ADP_GOOD_MULTIPLIER` - Good ADP tier multiplier
14. `ADP_POOR_MULTIPLIER` - Poor ADP tier multiplier

**Player Rating Adjustments:**
15. `PLAYER_RATING_EXCELLENT_MULTIPLIER` - Excellent player rating multiplier
16. `PLAYER_RATING_GOOD_MULTIPLIER` - Good player rating multiplier
17. `PLAYER_RATING_POOR_MULTIPLIER` - Poor player rating multiplier

**Team Quality Adjustments:**
18. `TEAM_EXCELLENT_MULTIPLIER` - Excellent team quality multiplier
19. `TEAM_GOOD_MULTIPLIER` - Good team quality multiplier
20. `TEAM_POOR_MULTIPLIER` - Poor team quality multiplier

## Parameter Value Lists

Each parameter should have a list of values to test in combinations. Examples:

- **Single value**: `[100]` - Only test with value 100
- **Two values**: `[100, 120]` - Test both 100 and 120 in all combinations
- **Multiple values**: `[100, 110, 120]` - Test all three values (more combinations)

## Two-Phase Optimization

The simulation uses a two-phase optimization approach to efficiently explore the parameter space:

### Phase Selection Logic

The simulation automatically determines whether to run preliminary testing based on the number of parameter combinations:

```python
# In shared_files/configs/simulation_config.py
TOP_CONFIGS_PERCENTAGE = 0.1    # Top 10% advance to full testing
MINIMUM_TOP_CONFIGS = 10        # Minimum configs for full testing
```

**Behavior:**
1. **If total configs < MINIMUM_TOP_CONFIGS**: Skip preliminary phase entirely, run full testing on all configs
2. **If total configs >= MINIMUM_TOP_CONFIGS**: Run two-phase optimization:
   - **Preliminary Phase**: Quick testing (30 sims per config) on all combinations
   - **Full Phase**: Thorough testing (100 sims per config) on top performers

**Top Config Selection:**
- Uses the **maximum** of `TOP_CONFIGS_PERCENTAGE` and `MINIMUM_TOP_CONFIGS`
- Example: With 50 total configs and 10% threshold:
  - Percentage: 50 × 0.1 = 5 configs
  - Minimum: 10 configs
  - **Result**: Tests top 10 configs (uses minimum since it's higher)

**Example Scenarios:**
- **8 total configs**: Skips preliminary, runs 100 simulations on all 8 configs
- **20 total configs**: Runs 30 simulations on all 20, then 100 simulations on top 10
- **200 total configs**: Runs 30 simulations on all 200, then 100 simulations on top 20 (10%)

### Phase Details

1. **Preliminary Phase**: Tests all combinations from your parameter JSON
2. **Fine-Grain Phase**: For top performers, generates additional variations using fine-grain offsets (optional)

### Enabling/Disabling Fine-Grain Phase

In `shared_files/configs/simulation_config.py`:

```python
ENABLE_FINE_GRAIN_OFFSETS = True   # Enable fine-grain variations (slower, more thorough)
ENABLE_FINE_GRAIN_OFFSETS = False  # Disable (faster, only test top configs as-is)
```

**When to disable:**
- Quick testing during development
- Limited time available
- Preliminary phase already found good configurations
- Just want to validate top configs with more simulations

**When to enable:**
- Final optimization runs
- Exploring parameter sensitivities
- Need to find absolute best configuration
- Have time for thorough testing

### Configuration

Fine-grain offsets are defined in `shared_files/configs/simulation_config.py`:

- **FINE_GRAIN_OFFSETS**: Offset values to add/subtract from top configs
- **FINE_GRAIN_BOUNDS**: Min/max limits for each parameter

Example from `simulation_config.py`:
```python
FINE_GRAIN_OFFSETS = {
    'INJURY_PENALTIES_MEDIUM': [-10, -5, 0, 5, 10],  # 5 variations
    'INJURY_PENALTIES_HIGH': [-15, -10, -5, 0, 5, 10, 15],  # 7 variations
    ...
}
```

### How It Works

If a top config has `INJURY_PENALTIES_MEDIUM = 25`, the fine-grain phase will test:
- `25 + (-10) = 15`
- `25 + (-5) = 20`
- `25 + 0 = 25` (original)
- `25 + 5 = 30`
- `25 + 10 = 35`

All values are clamped to their defined bounds in `FINE_GRAIN_BOUNDS`.

### Customizing Offsets

To customize fine-grain exploration:

1. Edit `shared_files/configs/simulation_config.py`
2. Modify `FINE_GRAIN_OFFSETS` for the parameters you want to explore more/less
3. Update `FINE_GRAIN_BOUNDS` if you need different value ranges

**Tips:**
- More offsets = more thorough testing but longer runtime
- Always include `0` to test the original top config value
- Use symmetric ranges (e.g., `[-5, 0, 5]`) for balanced exploration
- Scale offsets based on parameter magnitude (small offsets for 0-2 range, larger for 0-100 range)

## Example Files

### baseline_parameters.json
Contains all conservative/default values (single value per parameter). Use this for baseline performance testing.

### parameter_template.json
Template showing the expected format with all 20 parameters. Use this as a starting point for creating new configurations.

### demo_test.json
Quick validation test with baseline values. Use this to verify simulation infrastructure works end-to-end.

### phase1_iteration2_injury_bye_focus.json
**CURRENT OPTIMIZATION FILE** - Focused test of high-impact injury and bye penalty parameters (27 combinations). This is the next configuration to run in the optimization strategy.

### exhaustive_3value_test.json ⚠️
**REFERENCE ONLY - DO NOT EXECUTE**

This file documents the complete parameter space with 3 reasonable values for each of the 20 parameters.

**Why this file exists:**
- Documents reasonable value ranges for all parameters
- Serves as reference when designing focused tests
- Demonstrates why exhaustive testing is infeasible

**Why NOT to run this:**
- Creates 3^20 = **3,486,784,401 combinations** (3.5 billion)
- Would take **66 million years** at 10 minutes per simulation
- Even at 1 second per simulation, would take **110 years**
- Would require **~350 TB** of storage for all results

**Use this file for:**
- Reference when creating new configurations
- Understanding parameter value bounds
- Documenting the "reasonable range" for each parameter
- Educational purposes to understand computational constraints

**Instead of running this, use:**
- Phased testing approach (test parameter groups sequentially)
- Focus on high-impact parameters first (injury/bye penalties)
- Current optimization files like `phase1_iteration2_injury_bye_focus.json`

## Usage

Run simulations with a configuration file:

```bash
python run_simulation.py draft_helper/simulation/parameters/baseline_parameters.json
```

## Simulation Optimization Workflow

1. User runs simulation: `python run_simulation.py parameters/iteration_1.json`
2. Simulation completes and generates timestamped results file
3. User notifies Claude: "new simulation result file is ready"
4. Claude analyzes results and updates execution tracker
5. Claude generates next parameter JSON based on optimization strategy
6. Repeat

## Creating New Configurations

1. Copy `parameter_template.json` to a new file
2. Update `config_name` and `description`
3. Modify parameter values to test
4. Ensure all 20 parameters are present
5. Run simulation with new configuration

## Tips

- Start with baseline configuration to establish performance benchmark
- Test one parameter group at a time for clearer insights
- Use 2-value lists `[baseline, aggressive]` for efficient testing
- Document findings in execution tracker after each run
- Follow the phased optimization strategy for systematic testing
