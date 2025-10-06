# Simulation Parameter Injection Mechanism

**How the simulation injects test values into draft helper logic**

## Overview

The simulation **does NOT modify** the actual config files (`draft_helper_config.py`, `shared_config.py`, etc.). Instead, it uses **dependency injection** through the `config_params` dictionary that flows through the entire draft process.

## Complete Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. PARAMETER LOADING (JSON → Dictionary)                       │
└─────────────────────────────────────────────────────────────────┘
                              ↓
    run_simulation.py
    └─→ load_parameter_config('optimal_2025-10-05_14-33-13.json')
        └─→ Returns: {
              'config_name': 'optimal_...',
              'parameters': {
                'CONSISTENCY_LOW_MULTIPLIER': [1.08],
                'CONSISTENCY_MEDIUM_MULTIPLIER': [1.00],
                'CONSISTENCY_HIGH_MULTIPLIER': [0.92],
                'ADP_EXCELLENT_MULTIPLIER': [1.18],
                ... (all 23 parameters)
              }
            }

┌─────────────────────────────────────────────────────────────────┐
│ 2. COMBINATION EXPANSION (List → Single Dict)                  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
    config_optimizer.py
    └─→ expand_parameter_combinations(config['parameters'])
        └─→ Returns: [
              {
                'CONSISTENCY_LOW_MULTIPLIER': 1.08,
                'CONSISTENCY_MEDIUM_MULTIPLIER': 1.00,
                'CONSISTENCY_HIGH_MULTIPLIER': 0.92,
                'ADP_EXCELLENT_MULTIPLIER': 1.18,
                ... (23 key-value pairs)
              },
              ... (more combinations if multiple values per parameter)
            ]

┌─────────────────────────────────────────────────────────────────┐
│ 3. SIMULATION ENGINE INITIALIZATION                             │
└─────────────────────────────────────────────────────────────────┘
                              ↓
    simulation_engine.py
    └─→ DraftSimulationEngine(players_df, config_params)
        │   config_params = {
        │     'CONSISTENCY_LOW_MULTIPLIER': 1.08,
        │     'CONSISTENCY_MEDIUM_MULTIPLIER': 1.00,
        │     'CONSISTENCY_HIGH_MULTIPLIER': 0.92,
        │     'ADP_EXCELLENT_MULTIPLIER': 1.18,
        │     ... (all 23 parameters as single values)
        │   }
        │
        └─→ Stored as: self.config_params

┌─────────────────────────────────────────────────────────────────┐
│ 4. TEAM STRATEGY MANAGER CREATION (Per Draft Pick)             │
└─────────────────────────────────────────────────────────────────┘
                              ↓
    simulation_engine._make_team_pick()
    └─→ TeamStrategyManager(self.config_params, draft_teams_csv_path)
        │
        │   INJECTION POINT: config_params passed to constructor
        │
        └─→ TeamStrategyManager.__init__(config_params)

┌─────────────────────────────────────────────────────────────────┐
│ 5. PARAMETER EXTRACTION & STORAGE (Instance Variables)         │
└─────────────────────────────────────────────────────────────────┘
                              ↓
    team_strategies.py: TeamStrategyManager.__init__()
    │
    ├─→ Injury penalties extracted:
    │   self.injury_penalties = {
    │     "LOW": 0,
    │     "MEDIUM": config_params.get('INJURY_PENALTIES_MEDIUM', 25),
    │     "HIGH": config_params.get('INJURY_PENALTIES_HIGH', 50)
    │   }
    │
    ├─→ Bye penalty extracted:
    │   self.base_bye_penalty = config_params.get('BASE_BYE_PENALTY', 20)
    │
    ├─→ Draft order bonuses extracted:
    │   self.draft_order_primary_bonus = config_params.get('DRAFT_ORDER_PRIMARY_BONUS', 50)
    │   self.draft_order_secondary_bonus = config_params.get('DRAFT_ORDER_SECONDARY_BONUS', 25)
    │
    ├─→ Enhanced scoring config built:
    │   enhanced_scoring_config = {
    │     'adp_excellent_multiplier': config_params.get('ADP_EXCELLENT_MULTIPLIER', 1.15),
    │     'adp_good_multiplier': config_params.get('ADP_GOOD_MULTIPLIER', 1.08),
    │     'adp_poor_multiplier': config_params.get('ADP_POOR_MULTIPLIER', 0.92),
    │     'player_rating_excellent_multiplier': config_params.get('PLAYER_RATING_EXCELLENT_MULTIPLIER', 1.20),
    │     'player_rating_good_multiplier': config_params.get('PLAYER_RATING_GOOD_MULTIPLIER', 1.10),
    │     'player_rating_poor_multiplier': config_params.get('PLAYER_RATING_POOR_MULTIPLIER', 0.90),
    │     'team_excellent_multiplier': config_params.get('TEAM_EXCELLENT_MULTIPLIER', 1.12),
    │     'team_good_multiplier': config_params.get('TEAM_GOOD_MULTIPLIER', 1.06),
    │     'team_poor_multiplier': config_params.get('TEAM_POOR_MULTIPLIER', 0.94),
    │     'max_total_adjustment': 1.50,
    │     'min_total_adjustment': 0.70
    │   }
    │
    └─→ Consistency multipliers extracted:
        self.consistency_multipliers = {
          'LOW': config_params.get('CONSISTENCY_LOW_MULTIPLIER', 1.08),
          'MEDIUM': config_params.get('CONSISTENCY_MEDIUM_MULTIPLIER', 1.00),
          'HIGH': config_params.get('CONSISTENCY_HIGH_MULTIPLIER', 0.92)
        }

┌─────────────────────────────────────────────────────────────────┐
│ 6. CALCULATOR INITIALIZATION (Injected Configs)                 │
└─────────────────────────────────────────────────────────────────┘
                              ↓
    team_strategies.py: TeamStrategyManager.__init__()
    │
    └─→ self.enhanced_scorer = EnhancedScoringCalculator(enhanced_scoring_config)
        │
        │   The EnhancedScoringCalculator receives the dict with simulation values
        │   and stores them internally for use in calculate_enhanced_score()
        │
        └─→ EnhancedScoringCalculator.config = enhanced_scoring_config

┌─────────────────────────────────────────────────────────────────┐
│ 7. DRAFT HELPER STRATEGY EXECUTION (Using Injected Values)     │
└─────────────────────────────────────────────────────────────────┘
                              ↓
    team_strategies.py: _draft_helper_strategy()
    │
    │   For each available player:
    │
    ├─→ STEP 1: Get base score (normalized points)
    │
    ├─→ STEP 2-4: Apply enhanced scoring
    │   └─→ self.enhanced_scorer.calculate_enhanced_score(...)
    │       │
    │       │   Uses injected values from enhanced_scoring_config:
    │       │   - ADP multipliers: 1.18, 1.08, 0.52
    │       │   - Player rating multipliers: 1.21, 1.15, 0.94
    │       │   - Team multipliers: 1.12, 1.06, 0.94
    │       │
    │       └─→ Returns: enhanced_score
    │
    ├─→ STEP 5: Apply consistency multiplier
    │   └─→ self._apply_consistency_multiplier(enhanced_score, player)
    │       │
    │       │   Uses injected values from self.consistency_multipliers:
    │       │   - LOW: 1.08
    │       │   - MEDIUM: 1.00
    │       │   - HIGH: 0.92
    │       │
    │       └─→ Returns: consistency_score
    │
    ├─→ STEP 6: Add draft order bonus
    │   └─→ self._calculate_draft_order_bonus(...)
    │       │
    │       │   Uses injected values:
    │       │   - self.draft_order_primary_bonus
    │       │   - self.draft_order_secondary_bonus
    │       │
    │       └─→ Returns: draft_bonus
    │
    ├─→ STEP 7: Subtract injury penalty
    │   └─→ Uses self.injury_penalties dict
    │       │   (injected INJURY_PENALTIES_MEDIUM, INJURY_PENALTIES_HIGH)
    │       └─→ Returns: injury_penalty
    │
    └─→ STEP 8: Subtract bye week penalty
        └─→ Uses self.base_bye_penalty
            │   (injected BASE_BYE_PENALTY)
            └─→ Returns: bye_penalty

┌─────────────────────────────────────────────────────────────────┐
│ 8. FINAL SCORE CALCULATION (All Injected Values Applied)       │
└─────────────────────────────────────────────────────────────────┘
                              ↓
    final_score = consistency_score + draft_bonus - injury_penalty - bye_penalty
    │
    │   This score was calculated using ALL simulation parameters!
    │   No config files were modified - everything came from config_params dict
    │
    └─→ Player ranked by final_score for draft selection
```

## Key Mechanism: Dependency Injection

### What Does NOT Happen ❌

The simulation **DOES NOT**:
- Modify `draft_helper_config.py`
- Modify `shared_config.py`
- Modify `starter_helper_config.py`
- Use `setattr()` on config modules
- Import and patch config values globally

### What DOES Happen ✅

The simulation **DOES**:
1. Load parameters from JSON file into a dictionary
2. Pass that dictionary (`config_params`) to `DraftSimulationEngine`
3. Pass that same dictionary to `TeamStrategyManager` constructor
4. Extract values with `.get()` and store as instance variables
5. Use those instance variables during scoring calculations

## Code Example: Parameter Flow

### Starting Point (JSON File)
```json
{
  "parameters": {
    "CONSISTENCY_LOW_MULTIPLIER": [1.08],
    "ADP_EXCELLENT_MULTIPLIER": [1.18]
  }
}
```

### Step 1: Load to Dictionary
```python
# main_simulator.py
config = load_parameter_config('optimal_2025-10-05_14-33-13.json')
# config['parameters'] = {'CONSISTENCY_LOW_MULTIPLIER': [1.08], 'ADP_EXCELLENT_MULTIPLIER': [1.18]}
```

### Step 2: Expand Combinations
```python
# config_optimizer.py
combinations = expand_parameter_combinations(config['parameters'])
# combinations[0] = {'CONSISTENCY_LOW_MULTIPLIER': 1.08, 'ADP_EXCELLENT_MULTIPLIER': 1.18}
```

### Step 3: Pass to Engine
```python
# parallel_runner.py
config_params = combinations[0]  # Single dict for one test configuration
engine = DraftSimulationEngine(players_df, config_params)
# engine.config_params = {'CONSISTENCY_LOW_MULTIPLIER': 1.08, 'ADP_EXCELLENT_MULTIPLIER': 1.18}
```

### Step 4: Create Strategy Manager
```python
# simulation_engine.py: _make_team_pick()
strategy_manager = TeamStrategyManager(self.config_params, draft_teams_csv_path)
# Passes config_params dict to constructor
```

### Step 5: Extract and Store
```python
# team_strategies.py: TeamStrategyManager.__init__()
def __init__(self, config_params: Dict[str, Any], draft_teams_csv_path: Optional[str] = None):
    # Extract consistency multipliers
    self.consistency_multipliers = {
        'LOW': config_params.get('CONSISTENCY_LOW_MULTIPLIER', 1.08),    # Gets 1.08
        'MEDIUM': config_params.get('CONSISTENCY_MEDIUM_MULTIPLIER', 1.00),
        'HIGH': config_params.get('CONSISTENCY_HIGH_MULTIPLIER', 0.92)
    }

    # Extract enhanced scoring params
    enhanced_scoring_config = {
        'adp_excellent_multiplier': config_params.get('ADP_EXCELLENT_MULTIPLIER', 1.15),  # Gets 1.18
        'adp_good_multiplier': config_params.get('ADP_GOOD_MULTIPLIER', 1.08),
        # ... etc
    }

    # Initialize calculator with injected config
    self.enhanced_scorer = EnhancedScoringCalculator(enhanced_scoring_config)
```

### Step 6: Use During Scoring
```python
# team_strategies.py: _apply_consistency_multiplier()
def _apply_consistency_multiplier(self, base_score: float, player: FantasyPlayer) -> float:
    result = consistency_calc.calculate_consistency_score(player)
    category = result['volatility_category']  # e.g., 'LOW'

    # Use the injected value from constructor!
    multiplier = self.consistency_multipliers.get(category, 1.0)  # Gets 1.08 for LOW

    return base_score * multiplier  # 100.0 * 1.08 = 108.0
```

## Why This Design?

### Isolation
- Each simulation test runs with its own parameter set
- No global state pollution
- Parallel simulations can run different configs simultaneously

### Immutability
- Original config files never touched
- Safe to run multiple simulations without conflicts
- Easy to reproduce exact test conditions

### Flexibility
- Can test any parameter combination
- Easy to swap between baseline and optimized values
- Simple to add new parameters

## Comparison: Production vs Simulation

### Production Draft Helper

```python
# draft_helper.py (production)
from shared_files.configs import draft_helper_config

# Uses config module constants directly:
injury_penalty = draft_helper_config.INJURY_PENALTIES[player.injury_status]
consistency_mult = draft_helper_config.CONSISTENCY_MULTIPLIERS[category]
```

### Simulation Draft Helper

```python
# team_strategies.py (simulation)
# Constructor receives config_params dict:
def __init__(self, config_params: Dict[str, Any]):
    self.injury_penalties = {
        "MEDIUM": config_params.get('INJURY_PENALTIES_MEDIUM', 25),
        "HIGH": config_params.get('INJURY_PENALTIES_HIGH', 50)
    }
    self.consistency_multipliers = {
        'LOW': config_params.get('CONSISTENCY_LOW_MULTIPLIER', 1.08),
        'MEDIUM': config_params.get('CONSISTENCY_MEDIUM_MULTIPLIER', 1.00),
        'HIGH': config_params.get('CONSISTENCY_HIGH_MULTIPLIER', 0.92)
    }

# Uses instance variables instead of config module:
injury_penalty = self.injury_penalties[player.injury_status]
consistency_mult = self.consistency_multipliers[category]
```

## Summary

The simulation uses **pure dependency injection** via dictionaries:

1. **JSON → Dict**: Parameters loaded from file
2. **Dict → Engine**: Passed to simulation engine
3. **Engine → Strategy**: Passed to strategy manager
4. **Strategy → Storage**: Extracted and stored as instance variables
5. **Storage → Calculation**: Used during scoring

**No config files are ever modified!** Everything flows through the `config_params` dictionary from the JSON file down to the individual scoring calculations.

This design allows the simulation to test thousands of parameter combinations while keeping the production config files (`draft_helper_config.py`, etc.) completely untouched.
