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

## Example Files

### baseline_parameters.json
Contains all conservative/default values (single value per parameter). Use this for baseline performance testing.

### parameter_template.json
Template showing the expected format with all 20 parameters. Use this as a starting point for creating new configurations.

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
