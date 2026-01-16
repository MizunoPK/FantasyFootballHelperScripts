# Feature Specification: config_infrastructure

**Created:** 2026-01-12
**Status:** IN PROGRESS (S2.P2 - Gate 2 APPROVED, proceeding to S2.P3)
**Last Updated:** 2026-01-12

---

## Epic Intent

**Purpose:** Ground this feature in the epic's original request BEFORE technical work

**Epic Notes File:** `nfl_team_penalty_notes.txt`
**Epic Notes Re-Read:** 2026-01-12
**Feature Context:** This is Feature 01 of 2 in the nfl_team_penalty epic

---

### Problem This Feature Solves

**User's Request (lines 1, 3):**
> "Have a penalty during Add to Roster mode for specific NFL teams"
> "We'll put the following configs in league_config.json"

**Problem:** Users currently cannot configure team-specific penalties in the system. This feature creates the configuration infrastructure to store which teams to penalize and by what weight.

---

### User's Explicit Requests

1. **Config Setting: NFL_TEAM_PENALTY** (lines 5)
   > "NFL_TEAM_PENALTY = [\"LV\", \"NYJ\", \"NYG\", \"KC\"]"
   - List of team abbreviations
   - Stored in league_config.json
   - Example shows 4 teams: Raiders, Jets, Giants, Chiefs

2. **Config Setting: NFL_TEAM_PENALTY_WEIGHT** (lines 6, 8)
   > "NFL_TEAM_PENALTY_WEIGHT = 0.75"
   > "their final score would be multiplied by 0.75"
   - Multiplier weight (float)
   - Stored in league_config.json
   - Example value: 0.75 (75% of original score)

3. **Simulation Defaults** (lines 12-14)
   > "Simulation configs should look like this:"
   > "NFL_TEAM_PENALTY = []"
   > "NFL_TEAM_PENALTY_WEIGHT = 1.0"
   - All simulation config files need default values
   - Empty list = no teams penalized
   - Weight 1.0 = no penalty (100% of original score)

---

### User's Constraints

1. **User-Specific Setting** (line 10)
   > "This is a user-specific setting that will not be simulated in the simulations."
   - Config infrastructure must support DIFFERENT values for user vs. simulations
   - league_config.json = user's actual preferences
   - simulation configs = objective defaults

2. **Mode-Specific** (line 1)
   > "during Add to Roster mode"
   - Penalty only applies in Add to Roster mode (not mentioned: other modes unaffected)

3. **Team Preference Strategy** (line 10)
   > "to reflect the user's team preferences and perferred strategy"
   - This is intentionally subjective (user's preference, not objective data)

---

### Out of Scope (What User Explicitly Excluded)

- **Applying the penalty to scores** - Epic request describes what penalty DOES (line 8: "final score would be multiplied"), but IMPLEMENTING that multiplication is Feature 02's responsibility
- **Validation logic** - User didn't mention validation requirements (assumption: need to add)
- **Team abbreviation format** - User showed examples but didn't specify validation rules

---

### User's End Goal

**Quote (lines 1, 10):**
> "Have a penalty during Add to Roster mode for specific NFL teams"
> "to reflect the user's team preferences and perferred strategy"

**End Goal:** Allow users to express team preferences through configuration, so players from disfavored teams are automatically penalized during draft recommendations.

---

### Technical Components Mentioned by User

1. **league_config.json** (line 3)
   - Primary config file for user's settings
   - Contains NFL_TEAM_PENALTY and NFL_TEAM_PENALTY_WEIGHT

2. **Simulation configs** (line 12)
   - Separate config files for simulations
   - Need to store default values (empty list, 1.0 weight)

3. **Team abbreviations** (line 5)
   - Format: 2-3 letter codes ("LV", "NYJ", "NYG", "KC")
   - Standard NFL team abbreviations

4. **Add to Roster mode** (line 1)
   - Context where penalty applies
   - Not mentioned: ConfigManager integration (assumption)

---

### Agent Verification

- [x] Epic notes file re-read on 2026-01-12
- [x] All quotes verified with line citations
- [x] User explicit requests vs. agent assumptions identified
- [x] Out-of-scope items documented
- [x] Technical components mentioned by user extracted

**Assumptions Identified (not mentioned in epic):**
- ConfigManager class name (need to research actual config system)
- Validation requirements (weight range, valid team abbreviations)
- Config loading mechanism (how ConfigManager reads these settings)
- Where simulation configs are located

---

## Original Purpose (from S1)

Add NFL team penalty configuration settings to the config system, allowing users to specify which NFL teams to penalize and by what weight multiplier.

---

## Original Scope (from S1)

- Add `NFL_TEAM_PENALTY` (list of team abbreviations) to ConfigManager
- Add `NFL_TEAM_PENALTY_WEIGHT` (multiplier float) to ConfigManager
- Update league_config.json with user's team preferences
- Update all simulation config files with default values (empty list, 1.0 weight)
- Add config validation (weight must be 0.0-1.0, teams must be valid abbreviations)

---

## Dependencies

- **Depends on:** None
- **Blocks:** Feature 02 (score_penalty_application)

---

---

## Components Affected

### 1. ConfigKeys Class (ConfigManager.py)

**File:** `league_helper/util/ConfigManager.py`
**Lines to modify:** 74-75 (after FLEX_ELIGIBLE_POSITIONS constant)

**Source:** Derived Requirement
**Derivation:** ConfigManager pattern requires all config keys defined as class constants in ConfigKeys (observed pattern from lines 33-122). User requested adding configs to league_config.json (epic notes line 3), which requires corresponding ConfigKeys constants.

**Changes needed:**
```python
# Add after FLEX_ELIGIBLE_POSITIONS = "FLEX_ELIGIBLE_POSITIONS" (line 74)
NFL_TEAM_PENALTY = "NFL_TEAM_PENALTY"
NFL_TEAM_PENALTY_WEIGHT = "NFL_TEAM_PENALTY_WEIGHT"
```

---

### 2. ConfigManager Class Instance Variables (__init__)

**File:** `league_helper/util/ConfigManager.py`
**Lines to modify:** 220-221 (after self.flex_eligible_positions initialization)

**Source:** Derived Requirement
**Derivation:** ConfigManager pattern requires typed instance variable for each config setting (observed pattern from lines 194-221). User requested two config settings (epic notes lines 5-6), which require corresponding instance variables.

**Changes needed:**
```python
# Add after self.flex_eligible_positions: List[str] = [] (line 221)
self.nfl_team_penalty: List[str] = []
self.nfl_team_penalty_weight: float = 1.0
```

---

### 3. ConfigManager._extract_parameters() Method

**File:** `league_helper/util/ConfigManager.py`
**Lines to modify:** 1056-1057 (after flex_eligible_positions extraction)

**Source:** Derived Requirement
**Derivation:** ConfigManager pattern requires extracting each setting from self.parameters dict in _extract_parameters() method (observed pattern from lines 974-1057). User requested config values be loaded (epic notes line 3), which requires extraction logic.

**Changes needed:**
```python
# Add after self.flex_eligible_positions = self.parameters[...] (line 1057)
# Optional parameters with defaults (for backward compatibility)
self.nfl_team_penalty = self.parameters.get(
    self.keys.NFL_TEAM_PENALTY, []
)
self.nfl_team_penalty_weight = self.parameters.get(
    self.keys.NFL_TEAM_PENALTY_WEIGHT, 1.0
)
```

**Note:** Using `.get()` with defaults makes these OPTIONAL parameters (backward compatible with existing configs that don't have these keys). Pattern follows SCHEDULE_SCORING (line 994), TEMPERATURE_SCORING (line 1008), WIND_SCORING (line 1027).

---

### 4. Validation Logic (new method or inline)

**File:** `league_helper/util/ConfigManager.py`
**Location:** After extraction in _extract_parameters() method

**Source:** Derived Requirement
**Derivation:** Existing config settings have validation (observed pattern lines 1062-1132). Without validation, invalid values could cause silent failures or incorrect behavior. User didn't mention validation, but it's necessary for robustness.

**Changes needed:**
```python
# Validate NFL_TEAM_PENALTY (list of valid team abbreviations)
if not isinstance(self.nfl_team_penalty, list):
    raise ValueError("NFL_TEAM_PENALTY must be a list")

# Validate each team abbreviation against ALL_NFL_TEAMS
# (import from historical_data_compiler.constants)
invalid_teams = [
    team for team in self.nfl_team_penalty
    if team not in ALL_NFL_TEAMS
]
if invalid_teams:
    raise ValueError(
        f"NFL_TEAM_PENALTY contains invalid team abbreviations: {', '.join(invalid_teams)}"
    )

# Validate NFL_TEAM_PENALTY_WEIGHT (float, range 0.0-1.0)
if not isinstance(self.nfl_team_penalty_weight, (int, float)):
    raise ValueError("NFL_TEAM_PENALTY_WEIGHT must be a number")

if not (0.0 <= self.nfl_team_penalty_weight <= 1.0):
    raise ValueError(
        f"NFL_TEAM_PENALTY_WEIGHT must be between 0.0 and 1.0, got {self.nfl_team_penalty_weight}"
    )
```

---

### 5. league_config.json (User's Config)

**File:** `data/configs/league_config.json`
**Location:** Under "parameters" object

**Source:** Epic Request (epic notes lines 3, 5-6)
> "We'll put the following configs in league_config.json"
> "NFL_TEAM_PENALTY = [\"LV\", \"NYJ\", \"NYG\", \"KC\"]"
> "NFL_TEAM_PENALTY_WEIGHT = 0.75"

**Changes needed:**
```json
{
  "parameters": {
    ...existing settings...,
    "NFL_TEAM_PENALTY": ["LV", "NYJ", "NYG", "KC"],
    "NFL_TEAM_PENALTY_WEIGHT": 0.75
  }
}
```

---

### 6. Simulation Config Files (9 files)

**Files:** All files in `simulation/simulation_configs/*/league_config.json`
**Count:** 9 config files
**Location:** Under "parameters" object in each

**Source:** Epic Request (epic notes lines 12-14)
> "Simulation configs should look like this:"
> "NFL_TEAM_PENALTY = []"
> "NFL_TEAM_PENALTY_WEIGHT = 1.0"

**Changes needed (for ALL 9 files):**
```json
{
  "parameters": {
    ...existing settings...,
    "NFL_TEAM_PENALTY": [],
    "NFL_TEAM_PENALTY_WEIGHT": 1.0
  }
}
```

**Rationale (epic notes line 10):**
> "This is a user-specific setting that will not be simulated in the simulations."

---

### 7. Test File (new file to create)

**File:** `tests/league_helper/util/test_ConfigManager_nfl_team_penalty.py`

**Source:** Derived Requirement
**Derivation:** All ConfigManager config settings have dedicated test files (observed pattern: test_ConfigManager_max_positions.py, test_ConfigManager_flex_eligible_positions.py). New config settings require test coverage for robustness.

**Test scenarios needed:**
- Load config with valid NFL_TEAM_PENALTY and NFL_TEAM_PENALTY_WEIGHT
- Load config without keys (defaults: [], 1.0)
- Validate invalid team abbreviations (should raise ValueError)
- Validate weight outside 0.0-1.0 range (should raise ValueError)
- Validate weight = 0.0 (valid edge case)
- Validate weight = 1.0 (valid edge case)
- Validate empty penalty list (valid edge case)

---

## Requirements

### Requirement 1: Add NFL_TEAM_PENALTY Config Key

**Description:** Add NFL_TEAM_PENALTY constant to ConfigKeys class

**Source:** Epic Request (epic notes lines 3, 5)
> "We'll put the following configs in league_config.json"
> "NFL_TEAM_PENALTY = [\"LV\", \"NYJ\", \"NYG\", \"KC\"]"

**Traceability:** User explicitly requested this config setting name and format

**Implementation:**
- Add `NFL_TEAM_PENALTY = "NFL_TEAM_PENALTY"` to ConfigKeys class (after line 74)
- Follows existing pattern for all config keys

**Edge cases:** None (simple constant definition)

---

### Requirement 2: Add NFL_TEAM_PENALTY_WEIGHT Config Key

**Description:** Add NFL_TEAM_PENALTY_WEIGHT constant to ConfigKeys class

**Source:** Epic Request (epic notes lines 3, 6)
> "We'll put the following configs in league_config.json"
> "NFL_TEAM_PENALTY_WEIGHT = 0.75"

**Traceability:** User explicitly requested this config setting name and value format

**Implementation:**
- Add `NFL_TEAM_PENALTY_WEIGHT = "NFL_TEAM_PENALTY_WEIGHT"` to ConfigKeys class (after NFL_TEAM_PENALTY)
- Follows existing pattern for all config keys

**Edge cases:** None (simple constant definition)

---

### Requirement 3: Initialize Instance Variables with Defaults

**Description:** Add typed instance variables for both config settings in ConfigManager.__init__()

**Source:** Derived Requirement
**Derivation:** ConfigManager pattern requires instance variable for each config (observed lines 194-221). Without instance variables, settings cannot be accessed by other classes.

**Implementation:**
```python
self.nfl_team_penalty: List[str] = []
self.nfl_team_penalty_weight: float = 1.0
```

**Default values:**
- nfl_team_penalty: Empty list (no teams penalized)
- nfl_team_penalty_weight: 1.0 (no penalty multiplier effect)

**Edge cases:** None (initialization only)

---

### Requirement 4: Extract Config Values from Parameters Dict

**Description:** Extract NFL_TEAM_PENALTY and NFL_TEAM_PENALTY_WEIGHT from self.parameters dict

**Source:** Derived Requirement
**Derivation:** ConfigManager pattern requires extraction logic in _extract_parameters() (observed lines 974-1057). Without extraction, config values remain in dict and aren't accessible via instance variables.

**Implementation:**
```python
self.nfl_team_penalty = self.parameters.get(self.keys.NFL_TEAM_PENALTY, [])
self.nfl_team_penalty_weight = self.parameters.get(self.keys.NFL_TEAM_PENALTY_WEIGHT, 1.0)
```

**Pattern used:** Optional parameters with `.get()` and defaults (same as SCHEDULE_SCORING line 994, TEMPERATURE_SCORING line 1008)

**Backward compatibility:** Existing configs without these keys will use defaults ([], 1.0) without errors

**Edge cases:**
- Config file missing keys → use defaults
- Config file has keys → use provided values

---

### Requirement 5: Validate NFL_TEAM_PENALTY is a List

**Description:** Verify NFL_TEAM_PENALTY is a list type

**Source:** Derived Requirement
**Derivation:** ConfigManager validates all list-based settings (observed line 1085 for DRAFT_ORDER). Without type validation, incorrect types cause runtime errors later.

**Implementation:**
```python
if not isinstance(self.nfl_team_penalty, list):
    raise ValueError("NFL_TEAM_PENALTY must be a list")
```

**Pattern used:** Same as DRAFT_ORDER validation (line 1085-1086)

**Edge cases:**
- User provides string instead of list → ValueError with clear message
- User provides None → ValueError
- User provides empty list → valid (no penalty)

---

### Requirement 6: Validate Team Abbreviations Against ALL_NFL_TEAMS

**Description:** Verify all team abbreviations in NFL_TEAM_PENALTY are valid 32 NFL teams

**Source:** Derived Requirement
**Derivation:** User provided example with standard team abbreviations (epic notes line 5: "LV", "NYJ", "NYG", "KC"). Without validation, typos like "LV " (trailing space) or "lv" (lowercase) cause silent failures when Feature 02 tries to match against player.team values.

**Implementation:**
```python
from historical_data_compiler.constants import ALL_NFL_TEAMS

invalid_teams = [team for team in self.nfl_team_penalty if team not in ALL_NFL_TEAMS]
if invalid_teams:
    raise ValueError(
        f"NFL_TEAM_PENALTY contains invalid team abbreviations: {', '.join(invalid_teams)}"
    )
```

**Canonical team list:** ALL_NFL_TEAMS from historical_data_compiler/constants.py (32 teams)

**Edge cases:**
- User provides "lv" (lowercase) → ValueError (case sensitive)
- User provides "LV " (trailing space) → ValueError
- User provides "CHIEFS" (full name) → ValueError (must be abbreviation)
- Empty list → valid (no validation needed)

---

### Requirement 7: Validate NFL_TEAM_PENALTY_WEIGHT is Numeric

**Description:** Verify NFL_TEAM_PENALTY_WEIGHT is a float or int

**Source:** Derived Requirement
**Derivation:** User provided numeric example (epic notes line 6: 0.75). Without type validation, incorrect types (e.g., string "0.75") cause errors during score multiplication in Feature 02.

**Implementation:**
```python
if not isinstance(self.nfl_team_penalty_weight, (int, float)):
    raise ValueError("NFL_TEAM_PENALTY_WEIGHT must be a number")
```

**Pattern used:** Similar to threshold validation (lines 738-740 check isfinite)

**Edge cases:**
- User provides string "0.75" → ValueError
- User provides None → ValueError
- User provides int (e.g., 1) → valid (converts to float)

---

### Requirement 8: Validate NFL_TEAM_PENALTY_WEIGHT Range (0.0-1.0)

**Description:** Verify NFL_TEAM_PENALTY_WEIGHT is between 0.0 and 1.0 inclusive

**Source:** Derived Requirement
**Derivation:** Epic request describes "penalty" (epic notes lines 1, 8: "penalty", "multiplied by 0.75"). Penalties reduce scores, implying weight ≤ 1.0. Weight > 1.0 would be a boost, not a penalty. Weight < 0.0 would be invalid (negative multiplier).

**Implementation:**
```python
if not (0.0 <= self.nfl_team_penalty_weight <= 1.0):
    raise ValueError(
        f"NFL_TEAM_PENALTY_WEIGHT must be between 0.0 and 1.0, got {self.nfl_team_penalty_weight}"
    )
```

**Pattern used:** Similar to steps > 0 validation (line 733-735)

**Edge cases:**
- Weight = 0.0 → valid (complete penalty, 0% of score)
- Weight = 1.0 → valid (no penalty, 100% of score)
- Weight = 1.5 → ValueError (boost, not penalty)
- Weight = -0.5 → ValueError (negative invalid)

---

### Requirement 9: Update league_config.json with User's Team Penalties

**Description:** Add NFL_TEAM_PENALTY and NFL_TEAM_PENALTY_WEIGHT to user's config file

**Source:** Epic Request (epic notes lines 3, 5-6)
> "We'll put the following configs in league_config.json"
> "NFL_TEAM_PENALTY = [\"LV\", \"NYJ\", \"NYG\", \"KC\"]"
> "NFL_TEAM_PENALTY_WEIGHT = 0.75"

**Traceability:** User explicitly provided example values to use

**Implementation:**
Add to data/configs/league_config.json under "parameters" object:
```json
"NFL_TEAM_PENALTY": ["LV", "NYJ", "NYG", "KC"],
"NFL_TEAM_PENALTY_WEIGHT": 0.75
```

**Edge cases:** None (direct user request)

---

### Requirement 10: Update All Simulation Configs with Defaults

**Description:** Add NFL_TEAM_PENALTY and NFL_TEAM_PENALTY_WEIGHT with default values to all 9 simulation config files

**Source:** Epic Request (epic notes lines 12-14)
> "Simulation configs should look like this:"
> "NFL_TEAM_PENALTY = []"
> "NFL_TEAM_PENALTY_WEIGHT = 1.0"

**Traceability:** User explicitly specified simulation configs must use defaults (empty list, 1.0 weight)

**Rationale (epic notes line 10):**
> "This is a user-specific setting that will not be simulated in the simulations."

**Implementation:**
For each of the 9 simulation config files in `simulation/simulation_configs/*/league_config.json`, add:
```json
"NFL_TEAM_PENALTY": [],
"NFL_TEAM_PENALTY_WEIGHT": 1.0
```

**Files to update:**
1. accuracy_intermediate_00_NORMALIZATION_MAX_SCALE/league_config.json
2. accuracy_intermediate_01_TEAM_QUALITY_SCORING_WEIGHT/league_config.json
3. accuracy_intermediate_02_TEAM_QUALITY_MIN_WEEKS/league_config.json
4. accuracy_intermediate_03_PERFORMANCE_SCORING_WEIGHT/league_config.json
5. accuracy_intermediate_04_PERFORMANCE_SCORING_STEPS/league_config.json
6. accuracy_intermediate_05_PERFORMANCE_MIN_WEEKS/league_config.json
7. accuracy_optimal_2025-12-23_06-51-56/league_config.json
8. intermediate_01_DRAFT_NORMALIZATION_MAX_SCALE/league_config.json
9. optimal_iterative_20260104_080756/league_config.json

**Edge cases:** None (direct user request)

---

### Requirement 11: Create Unit Tests for New Config Settings

**Description:** Create comprehensive unit tests for NFL_TEAM_PENALTY and NFL_TEAM_PENALTY_WEIGHT validation

**Source:** Derived Requirement
**Derivation:** All ConfigManager settings have dedicated test files (observed pattern). Without tests, config validation cannot be verified and regressions can occur.

**Test file:** `tests/league_helper/util/test_ConfigManager_nfl_team_penalty.py`

**Test scenarios:**
1. Load config with valid settings
2. Load config without settings (test defaults)
3. Invalid team abbreviation → ValueError
4. Weight > 1.0 → ValueError
5. Weight < 0.0 → ValueError
6. Weight = 0.0 → valid
7. Weight = 1.0 → valid
8. Empty penalty list → valid
9. NFL_TEAM_PENALTY not a list → ValueError
10. NFL_TEAM_PENALTY_WEIGHT not numeric → ValueError

**Edge cases:** All validation edge cases covered by tests

---

## Data Structures

### Input: league_config.json

**Structure:**
```json
{
  "config_name": "Optimal Base Config",
  "description": "User configuration",
  "parameters": {
    "NFL_TEAM_PENALTY": ["LV", "NYJ", "NYG", "KC"],
    "NFL_TEAM_PENALTY_WEIGHT": 0.75,
    ...other parameters...
  }
}
```

**Field types:**
- `NFL_TEAM_PENALTY`: List[str] - List of 2-3 letter uppercase team abbreviations
- `NFL_TEAM_PENALTY_WEIGHT`: float - Multiplier between 0.0 and 1.0

**Validation rules:**
- NFL_TEAM_PENALTY: Must be list, all values in ALL_NFL_TEAMS (32 teams)
- NFL_TEAM_PENALTY_WEIGHT: Must be numeric, range 0.0-1.0 inclusive

---

### Internal: ConfigManager Instance

**Attributes:**
- `self.nfl_team_penalty: List[str]` - Loaded from config or default []
- `self.nfl_team_penalty_weight: float` - Loaded from config or default 1.0

**Access pattern:**
```python
config = ConfigManager(data_folder)
penalized_teams = config.nfl_team_penalty  # ["LV", "NYJ", "NYG", "KC"]
penalty_weight = config.nfl_team_penalty_weight  # 0.75
```

**Usage:** Feature 02 will read these values to determine which players to penalize

---

### Output: None (Config Loading Only)

This feature only loads and validates config values. Feature 02 will consume these values to apply penalties to player scores.

---

## Algorithms

### Algorithm 1: Config Loading and Validation

**Pseudocode:**
```python
def _extract_parameters(self):
    # Extract values with defaults (backward compatible)
    self.nfl_team_penalty = self.parameters.get("NFL_TEAM_PENALTY", [])
    self.nfl_team_penalty_weight = self.parameters.get("NFL_TEAM_PENALTY_WEIGHT", 1.0)

    # Validate NFL_TEAM_PENALTY
    if not isinstance(self.nfl_team_penalty, list):
        raise ValueError("NFL_TEAM_PENALTY must be a list")

    invalid_teams = [team for team in self.nfl_team_penalty if team not in ALL_NFL_TEAMS]
    if invalid_teams:
        raise ValueError(f"Invalid team abbreviations: {', '.join(invalid_teams)}")

    # Validate NFL_TEAM_PENALTY_WEIGHT
    if not isinstance(self.nfl_team_penalty_weight, (int, float)):
        raise ValueError("NFL_TEAM_PENALTY_WEIGHT must be a number")

    if not (0.0 <= self.nfl_team_penalty_weight <= 1.0):
        raise ValueError(f"Weight must be 0.0-1.0, got {self.nfl_team_penalty_weight}")
```

**Edge case handling:**
- Missing keys → use defaults ([], 1.0)
- Invalid types → raise ValueError with descriptive message
- Invalid values → raise ValueError with specific constraint violated
- Empty penalty list → valid (no penalties applied)
- Weight at boundaries (0.0, 1.0) → valid

---

## Dependencies

### This Feature Depends On:

1. **historical_data_compiler.constants.ALL_NFL_TEAMS**
   - **Status:** Exists (historical_data_compiler/constants.py line 43-48)
   - **Purpose:** Canonical list of 32 NFL team abbreviations for validation
   - **Usage:** Import to validate NFL_TEAM_PENALTY values

### This Feature Blocks:

1. **Feature 02: score_penalty_application**
   - **Status:** Awaiting this feature's completion
   - **Purpose:** Reads nfl_team_penalty and nfl_team_penalty_weight from ConfigManager to apply penalties
   - **Dependency:** Cannot apply penalties without config infrastructure

### This Feature is Independent Of:

1. **All other epic features** (this is the only feature in epic besides Feature 02)

---

## Acceptance Criteria

**Feature:** Feature 01 - config_infrastructure
**Status:** Awaiting user approval
**Created:** 2026-01-12

---

### 1. Behavior Changes

**New Functionality:**
- ConfigManager can now load NFL_TEAM_PENALTY (list of team abbreviations) from config files
- ConfigManager can now load NFL_TEAM_PENALTY_WEIGHT (penalty multiplier) from config files
- ConfigManager validates team abbreviations against canonical list of 32 NFL teams
- ConfigManager validates penalty weight is numeric and within 0.0-1.0 range
- Invalid config values raise ValueError with descriptive error messages

**Modified Functionality:**
- None (purely additive changes)

**No Changes To:**
- Existing config settings behavior
- Config file loading mechanism
- Other ConfigManager functionality

---

### 2. Files Modified

**New Files Created (1):**
1. `tests/league_helper/util/test_ConfigManager_nfl_team_penalty.py`
   - Purpose: Unit tests for new config settings
   - Test count: ~10 test cases (valid/invalid scenarios)

**Existing Files Modified (11):**

1. `league_helper/util/ConfigManager.py`
   - Lines ~74-75: Add NFL_TEAM_PENALTY and NFL_TEAM_PENALTY_WEIGHT constants to ConfigKeys class
   - Lines ~220-221: Add instance variables with type hints and defaults
   - Lines ~1056-1057: Add extraction logic using .get() with defaults
   - After line 1057: Add validation logic (type checks, range checks, team abbreviation validation)
   - Import: Add ALL_NFL_TEAMS from historical_data_compiler.constants

2. `data/configs/league_config.json`
   - Add under "parameters": NFL_TEAM_PENALTY: ["LV", "NYJ", "NYG", "KC"]
   - Add under "parameters": NFL_TEAM_PENALTY_WEIGHT: 0.75

3-11. **9 Simulation Config Files** (all get same defaults):
   - `simulation/simulation_configs/accuracy_intermediate_00_NORMALIZATION_MAX_SCALE/league_config.json`
   - `simulation/simulation_configs/accuracy_intermediate_01_TEAM_QUALITY_SCORING_WEIGHT/league_config.json`
   - `simulation/simulation_configs/accuracy_intermediate_02_TEAM_QUALITY_MIN_WEEKS/league_config.json`
   - `simulation/simulation_configs/accuracy_intermediate_03_PERFORMANCE_SCORING_WEIGHT/league_config.json`
   - `simulation/simulation_configs/accuracy_intermediate_04_PERFORMANCE_SCORING_STEPS/league_config.json`
   - `simulation/simulation_configs/accuracy_intermediate_05_PERFORMANCE_MIN_WEEKS/league_config.json`
   - `simulation/simulation_configs/accuracy_optimal_2025-12-23_06-51-56/league_config.json`
   - `simulation/simulation_configs/intermediate_01_DRAFT_NORMALIZATION_MAX_SCALE/league_config.json`
   - `simulation/simulation_configs/optimal_iterative_20260104_080756/league_config.json`
   - Add to each: NFL_TEAM_PENALTY: [], NFL_TEAM_PENALTY_WEIGHT: 1.0

---

### 3. Data Structures

**New Data Structures:**
- None (uses existing list and float types)

**Modified ConfigManager Instance:**
```python
class ConfigManager:
    # New instance variables
    self.nfl_team_penalty: List[str]  # Default: []
    self.nfl_team_penalty_weight: float  # Default: 1.0
```

**Config File Schema Changes:**
```json
{
  "parameters": {
    "NFL_TEAM_PENALTY": ["LV", "NYJ", "NYG", "KC"],  // NEW: List of team abbreviations
    "NFL_TEAM_PENALTY_WEIGHT": 0.75  // NEW: Penalty multiplier (0.0-1.0)
  }
}
```

---

### 4. API/Interface Changes

**New Public API:**
```python
# ConfigManager instance attributes (accessible after initialization)
config.nfl_team_penalty: List[str]  # Team abbreviations to penalize
config.nfl_team_penalty_weight: float  # Penalty multiplier (0.0-1.0)
```

**Example Usage (Feature 02 will use this):**
```python
config = ConfigManager(data_folder)
penalized_teams = config.nfl_team_penalty  # ["LV", "NYJ", "NYG", "KC"]
penalty_weight = config.nfl_team_penalty_weight  # 0.75
```

**Modified Interfaces:**
- None (purely additive)

**Backward Compatibility:**
- ✅ MAINTAINED: Existing configs without new keys load successfully (use defaults)
- ✅ MAINTAINED: All existing ConfigManager functionality unchanged

---

### 5. Testing

**Test File:** `test_ConfigManager_nfl_team_penalty.py`

**Test Scenarios (10 total):**
1. Load config with valid NFL_TEAM_PENALTY and NFL_TEAM_PENALTY_WEIGHT
2. Load config without new keys (test defaults: [], 1.0)
3. Invalid team abbreviation (e.g., "INVALID") → ValueError
4. Lowercase team abbreviation (e.g., "lv") → ValueError
5. Team abbreviation with trailing space (e.g., "LV ") → ValueError
6. Weight > 1.0 (e.g., 1.5) → ValueError
7. Weight < 0.0 (e.g., -0.5) → ValueError
8. Weight = 0.0 → Valid (complete penalty)
9. Weight = 1.0 → Valid (no penalty)
10. Empty penalty list [] → Valid (no penalties)

**Coverage Target:** 100% coverage of new code (validation logic, extraction logic)

**Edge Cases Tested:**
- Boundary values (0.0, 1.0)
- Empty list (valid case)
- Invalid types (string instead of list, string instead of number)
- Invalid values (out of range, not in canonical team list)

---

### 6. Dependencies

**This Feature Depends On:**
- `historical_data_compiler.constants.ALL_NFL_TEAMS` (existing, line 43-48)
  - Canonical list of 32 NFL team abbreviations
  - Used for validation

**This Feature Blocks:**
- Feature 02: score_penalty_application
  - Cannot apply penalties without config infrastructure
  - Feature 02 will read config.nfl_team_penalty and config.nfl_team_penalty_weight

**External Dependencies:**
- None (no new external libraries)

---

### 7. Edge Cases & Error Handling

**Edge Cases Handled:**
1. **Missing config keys** → Use defaults ([], 1.0) without error
2. **Empty penalty list** → Valid (no penalties applied)
3. **Weight = 0.0** → Valid (complete penalty, 0% of score remains)
4. **Weight = 1.0** → Valid (no penalty effect, 100% of score remains)
5. **Duplicate teams in list** → Allowed (redundant but harmless)

**Error Conditions:**
1. **NFL_TEAM_PENALTY not a list** → ValueError: "NFL_TEAM_PENALTY must be a list"
2. **Invalid team abbreviation** → ValueError: "NFL_TEAM_PENALTY contains invalid team abbreviations: {list}"
3. **Weight not numeric** → ValueError: "NFL_TEAM_PENALTY_WEIGHT must be a number"
4. **Weight > 1.0** → ValueError: "NFL_TEAM_PENALTY_WEIGHT must be between 0.0 and 1.0, got {value}"
5. **Weight < 0.0** → ValueError: "NFL_TEAM_PENALTY_WEIGHT must be between 0.0 and 1.0, got {value}"

**Error Message Quality:**
- All error messages are descriptive
- All error messages include the invalid value
- All error messages explain the constraint

---

### 8. Documentation

**User-Facing Documentation:**
- None required (config infrastructure, not user-facing feature)
- Feature 02 will add user documentation for the penalty system

**Developer Documentation:**
- Code comments in validation logic (explain range/validation rationale)
- Docstrings not needed (follows existing ConfigManager pattern of no docstrings)

**Config File Comments:**
- league_config.json: No inline comments (JSON doesn't support comments)
- README update: Not needed (config self-documenting via key names)

---

### 9. User Approval

**Approval Status:** [x] APPROVED ✅

**Approval Timestamp:** 2026-01-12

**Approval Notes:** User approved acceptance criteria on 2026-01-12 with no modifications requested.

---

## Notes

Specification completed in S2.P2 (Specification Phase). All requirements have traceability (Epic Request or Derived). S2.P3 (Refinement Phase) Phases 3-5 skipped (zero questions, first feature). Ready for user approval.
