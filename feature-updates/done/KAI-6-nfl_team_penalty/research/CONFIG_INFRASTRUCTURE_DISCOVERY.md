# Research Discovery: config_infrastructure

**Feature:** Feature 01 - config_infrastructure
**Epic:** nfl_team_penalty
**Research Date:** 2026-01-12
**Research Phase:** S2.P1 - Targeted Research

---

## Epic Intent Summary

User wants to add two config settings to league_config.json:
- `NFL_TEAM_PENALTY`: List of team abbreviations (e.g., ["LV", "NYJ", "NYG", "KC"])
- `NFL_TEAM_PENALTY_WEIGHT`: Multiplier weight (e.g., 0.75)

These settings allow users to penalize players from specific NFL teams. Simulations must use defaults (empty list, 1.0 weight) to remain objective.

---

## Component 1: ConfigManager

**User mentioned:** Not explicitly mentioned, but implied by "put the following configs in league_config.json" (epic notes line 3)

**Found in codebase:**
- **File:** `league_helper/util/ConfigManager.py`
- **Lines:** 33-122 (ConfigKeys class), 124-227 (ConfigManager class definition), 849-1094 (_load_config and _extract_parameters methods)

**How it works today:**

### 1. ConfigKeys Class (lines 33-122)
Defines constants for all config keys:
```python
class ConfigKeys:
    # Top Level Keys
    CONFIG_NAME = "config_name"
    DESCRIPTION = "description"
    PARAMETERS = "parameters"

    # Parameter Keys
    CURRENT_NFL_WEEK = "CURRENT_NFL_WEEK"
    NFL_SEASON = "NFL_SEASON"
    # ... many more
    MAX_POSITIONS = "MAX_POSITIONS"
    FLEX_ELIGIBLE_POSITIONS = "FLEX_ELIGIBLE_POSITIONS"
```

**Pattern identified:** All config keys are defined as class constants in ConfigKeys

### 2. ConfigManager.__init__() (lines 160-226)
- Initializes instance variables for each config setting
- Calls `self._load_config()` at end

**Pattern identified:** Each config setting has a corresponding instance variable

### 3. ConfigManager._load_config() (lines 849-918)
- Loads JSON from config file path (line 875-876)
- Validates config structure (line 883)
- Extracts parameters dict (line 888)
- Calls `self._extract_parameters()` (line 917)

**Config file locations:**
- **New structure:** `data/configs/league_config.json` (checked first, line 182-187)
- **Legacy structure:** `data/league_config.json` (fallback, line 189-192)

### 4. ConfigManager._extract_parameters() (lines 945-1094)
- Defines **required_params** list (lines 948-966)
- Extracts each setting from `self.parameters` dict:
  ```python
  self.current_nfl_week = self.parameters[self.keys.CURRENT_NFL_WEEK]
  ```
- For **optional parameters**, uses `.get()` with defaults:
  ```python
  self.schedule_scoring = self.parameters.get(self.keys.SCHEDULE_SCORING, {default_dict})
  ```

**Pattern identified for new config settings:**
1. Add key constants to ConfigKeys class
2. Add instance variable in __init__
3. Decide: required (add to required_params list) or optional (use .get() with default)
4. Extract setting in _extract_parameters()

---

## Component 2: league_config.json Structure

**User mentioned:** "We'll put the following configs in league_config.json" (epic notes line 3)

**Found in codebase:**
- **File:** `data/configs/league_config.json`
- **Lines:** 1-300+ (full JSON structure)

**Current structure (excerpt from lines 1-100):**
```json
{
  "config_name": "Optimal Base Config (20251210_024739)",
  "description": "Optimized base parameters for all weeks",
  "parameters": {
    "CURRENT_NFL_WEEK": 17,
    "NFL_SEASON": 2025,
    "NFL_SCORING_FORMAT": "ppr",
    "DRAFT_NORMALIZATION_MAX_SCALE": 163,
    "SAME_POS_BYE_WEIGHT": 0.07,
    "DIFF_POS_BYE_WEIGHT": 0.01,
    "INJURY_PENALTIES": {
      "LOW": 0,
      "MEDIUM": 0,
      "HIGH": 0
    },
    "DRAFT_ORDER_BONUSES": {
      "PRIMARY": 67,
      "SECONDARY": 69
    },
    "MAX_POSITIONS": {
      "QB": 2,
      "RB": 4,
      "WR": 4,
      "FLEX": 1,
      "TE": 2,
      "K": 1,
      "DST": 1
    },
    "FLEX_ELIGIBLE_POSITIONS": [
      "RB",
      "WR"
    ]
  }
}
```

**Pattern identified:**
- Top-level: config_name, description, parameters
- All settings nested under "parameters" key
- Mix of simple values (int, float, string) and complex objects (dicts, lists)

**Where to add new settings:**
Add `NFL_TEAM_PENALTY` and `NFL_TEAM_PENALTY_WEIGHT` under "parameters" key.

**User's example values (epic notes lines 5-6):**
```json
"NFL_TEAM_PENALTY": ["LV", "NYJ", "NYG", "KC"],
"NFL_TEAM_PENALTY_WEIGHT": 0.75
```

---

## Component 3: Simulation Config Files

**User mentioned:** "Simulation configs should look like this:" (epic notes line 12)

**Found in codebase:**
- **Location:** `simulation/simulation_configs/*/league_config.json`
- **Count:** 9 config files total

**All simulation config files:**
1. `simulation/simulation_configs/accuracy_intermediate_00_NORMALIZATION_MAX_SCALE/league_config.json`
2. `simulation/simulation_configs/accuracy_intermediate_01_TEAM_QUALITY_SCORING_WEIGHT/league_config.json`
3. `simulation/simulation_configs/accuracy_intermediate_02_TEAM_QUALITY_MIN_WEEKS/league_config.json`
4. `simulation/simulation_configs/accuracy_intermediate_03_PERFORMANCE_SCORING_WEIGHT/league_config.json`
5. `simulation/simulation_configs/accuracy_intermediate_04_PERFORMANCE_SCORING_STEPS/league_config.json`
6. `simulation/simulation_configs/accuracy_intermediate_05_PERFORMANCE_MIN_WEEKS/league_config.json`
7. `simulation/simulation_configs/accuracy_optimal_2025-12-23_06-51-56/league_config.json`
8. `simulation/simulation_configs/intermediate_01_DRAFT_NORMALIZATION_MAX_SCALE/league_config.json`
9. `simulation/simulation_configs/optimal_iterative_20260104_080756/league_config.json`

**All must be updated with defaults:**
```json
"NFL_TEAM_PENALTY": [],
"NFL_TEAM_PENALTY_WEIGHT": 1.0
```

**Rationale (epic notes line 10):**
> "This is a user-specific setting that will not be simulated in the simulations."

---

## Component 4: Team Abbreviations

**User mentioned:** Team abbreviation format in example: "LV", "NYJ", "NYG", "KC" (epic notes line 5)

**Found in codebase:**
- **File:** `historical_data_compiler/constants.py`
- **Lines:** 43-48

**Canonical list of all 32 NFL teams:**
```python
ALL_NFL_TEAMS: List[str] = [
    'ARI', 'ATL', 'BAL', 'BUF', 'CAR', 'CHI', 'CIN', 'CLE',
    'DAL', 'DEN', 'DET', 'GB', 'HOU', 'IND', 'JAX', 'KC',
    'LAC', 'LAR', 'LV', 'MIA', 'MIN', 'NE', 'NO', 'NYG',
    'NYJ', 'PHI', 'PIT', 'SEA', 'SF', 'TB', 'TEN', 'WSH'
]
```

**Usage in player data:**
- **File:** `data/player_data/qb_data.json` (and all other position files)
- **Field:** `"team": "BUF"` (2-3 letter abbreviation)

**Validation requirement:**
- NFL_TEAM_PENALTY values must be in ALL_NFL_TEAMS list
- Prevents typos like "LV " (trailing space) or "lv" (lowercase)

---

## Component 5: Validation Patterns

**User mentioned:** Not explicitly, but validation is standard practice

**Found in codebase:**
- **File:** `league_helper/util/ConfigManager.py`
- **Method:** `validate_threshold_params()` (lines 715-753)

**Existing validation patterns:**

### Pattern 1: Type Checking (line 1085-1086)
```python
if not isinstance(self.draft_order, list):
    raise ValueError("DRAFT_ORDER must be a list")
```

### Pattern 2: Range Validation (lines 733-735)
```python
if steps <= 0:
    self.logger.error(f"STEPS must be positive, got {steps}")
    raise ValueError(f"STEPS must be positive, got {steps}")
```

### Pattern 3: Allowed Values Validation (lines 749-751)
```python
valid_dirs = [self.keys.DIRECTION_INCREASING, self.keys.DIRECTION_DECREASING, ...]
if direction not in valid_dirs:
    self.logger.error(f"DIRECTION must be one of {valid_dirs}, got '{direction}'")
    raise ValueError(f"DIRECTION must be one of {valid_dirs}, got '{direction}'")
```

### Pattern 4: Required Fields Validation (lines 1089-1094)
```python
required_positions = ['QB', 'RB', 'WR', 'TE', 'K', 'DST', 'FLEX']
missing_positions = [pos for pos in required_positions if pos not in self.max_positions]
if missing_positions:
    error_msg = f"MAX_POSITIONS missing required positions: {', '.join(missing_positions)}"
    self.logger.error(error_msg)
    raise ValueError(error_msg)
```

**Validation needed for new settings:**
1. **NFL_TEAM_PENALTY**:
   - Must be a list
   - All values must be strings
   - All values must be in ALL_NFL_TEAMS

2. **NFL_TEAM_PENALTY_WEIGHT**:
   - Must be a float (or int convertible to float)
   - Must be in range 0.0 to 1.0 (inclusive)

---

## Existing Test Patterns

**Found in codebase:**
- **File:** `tests/league_helper/util/test_ConfigManager_*.py` (multiple test files)
- **Examples:**
  - `test_ConfigManager_max_positions.py` - Tests MAX_POSITIONS validation
  - `test_ConfigManager_thresholds.py` - Tests threshold validation
  - `test_ConfigManager_flex_eligible_positions.py` - Tests list validation

**Test pattern observed:**
1. Create test config JSON (with/without settings)
2. Initialize ConfigManager with test config
3. Assert settings loaded correctly OR ValueError raised
4. Verify error messages are descriptive

---

## Interface Dependencies

**Classes this feature will interact with:**

1. **ConfigManager** (`league_helper/util/ConfigManager.py`)
   - Add new config keys to ConfigKeys class
   - Add new instance variables
   - Add extraction logic in _extract_parameters()
   - Add validation logic

2. **FantasyPlayer** (`utils/FantasyPlayer.py`)
   - Has `.team` attribute with team abbreviation
   - Feature 02 will read this attribute (not Feature 01)

3. **Test files**
   - Will need new test file: `test_ConfigManager_nfl_team_penalty.py`
   - Tests for valid/invalid values
   - Tests for optional vs required behavior

---

## Edge Cases Identified

1. **Empty penalty list**: Should work without errors (no penalties applied)
2. **Penalty weight = 1.0**: No penalty (100% of original score)
3. **Penalty weight = 0.0**: Complete penalty (0% of original score)
4. **Invalid team abbreviations**: Should raise ValueError
5. **Duplicate team abbreviations**: Should be allowed (no harm, just redundant)
6. **Penalty weight > 1.0**: Should raise ValueError (boost, not penalty)
7. **Penalty weight < 0.0**: Should raise ValueError (negative multiplier invalid)
8. **Missing keys in simulation configs**: Config should still load (optional)
9. **Config file without new keys**: Backward compatibility (existing configs work)

---

## Research Completeness

**Components researched:**
- [x] ConfigManager class structure and patterns
- [x] league_config.json file structure and location
- [x] Simulation config files (count and locations)
- [x] Team abbreviations (canonical list)
- [x] Validation patterns (existing examples)
- [x] Test patterns (existing examples)

**Files read:**
- [x] `league_helper/util/ConfigManager.py` (lines 1-1094)
- [x] `data/configs/league_config.json` (lines 1-100)
- [x] `historical_data_compiler/constants.py` (lines 1-50)
- [x] `data/player_data/qb_data.json` (sample)

**Evidence collected:**
- File paths cited: 5 key files
- Line numbers noted: 15+ specific locations
- Code snippets copied: 8 examples
- Method signatures documented: 4 methods

---

## Questions for Specification Phase

1. **Optional vs Required**: Should NFL_TEAM_PENALTY and NFL_TEAM_PENALTY_WEIGHT be optional (backward compatible) or required?
   - **Recommendation**: Optional with defaults (empty list, 1.0) for backward compatibility

2. **Validation strictness**: Should we validate team abbreviations against ALL_NFL_TEAMS?
   - **Recommendation**: Yes, prevents typos

3. **Weight range**: Should weight be restricted to 0.0-1.0?
   - **Recommendation**: Yes, per epic intent ("penalty" = reduction, not boost)

4. **Case sensitivity**: Should team abbreviations be case-insensitive?
   - **Recommendation**: No, keep uppercase only (matches existing data)

---

**Research Phase Complete - Ready for Specification Phase (S2.P2)**
