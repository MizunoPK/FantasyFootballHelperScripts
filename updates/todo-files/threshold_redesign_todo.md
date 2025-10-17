# Threshold Configuration System Redesign - TODO (v2)

**Objective:** Replace hardcoded threshold values with parameterized calculation system (BASE_POSITION, DIRECTION, STEPS).

**Status:** Planning Complete - Awaiting User Input on Formula Questions
**Created:** 2025-10-16 (v2)
**Reference:** `updates/threshold_updates.txt` (updated version)

---

## Overview

### Current System
- 5 scoring types × 4 hardcoded thresholds = 20 values
- Example: `{"VERY_POOR": 150, "POOR": 100, "GOOD": 50, "EXCELLENT": 20}`

### Target System
- 5 scoring types × 1 STEPS parameter = 5 values
- Example: `{"BASE_POSITION": 0, "DIRECTION": "DECREASING", "STEPS": 37.5}`
- BASE_POSITION and DIRECTION are fixed per scoring type
- Only STEPS varies for optimization

---

## Key Decisions Needed (See questions file)

**Critical Questions:**
1. Q1-Q5: Formula adjustments to match current thresholds
2. Recommended: Change bidirectional formula from 0.5x/1.5x to 1x/2x

**Once decided, implementation can begin.**

---

## Implementation Phases

### Phase 1: Core ConfigManager Implementation

#### Task 1.1: Add ConfigKeys Constants
**Priority:** HIGH
**Time:** 15 minutes

Add to `ConfigKeys` class:
```python
# Parameterized threshold keys
BASE_POSITION = "BASE_POSITION"
DIRECTION = "DIRECTION"
STEPS = "STEPS"

# Direction values
DIRECTION_INCREASING = "INCREASING"
DIRECTION_DECREASING = "DECREASING"
DIRECTION_BI_EXCELLENT_HI = "BI_EXCELLENT_HI"
DIRECTION_BI_EXCELLENT_LOW = "BI_EXCELLENT_LOW"

# Optional calculated field
CALCULATED = "_calculated"
```

**Files:** `league_helper/util/ConfigManager.py`

---

#### Task 1.2: Add calculate_thresholds() Method
**Priority:** HIGH
**Time:** 1-2 hours

**Implementation:**
```python
def calculate_thresholds(self, base_pos: float, direction: str, steps: float) -> Dict[str, float]:
    """
    Calculate threshold values from parameters.

    Args:
        base_pos: Base position (typically 0)
        direction: INCREASING, DECREASING, BI_EXCELLENT_HI, or BI_EXCELLENT_LOW
        steps: Step size between thresholds

    Returns:
        Dict with VERY_POOR, POOR, GOOD, EXCELLENT

    Examples:
        >>> # INCREASING (player rating)
        >>> calculate_thresholds(0, "INCREASING", 20)
        {'VERY_POOR': 20, 'POOR': 40, 'GOOD': 60, 'EXCELLENT': 80}

        >>> # DECREASING (ADP)
        >>> calculate_thresholds(0, "DECREASING", 37.5)
        {'VERY_POOR': 150, 'POOR': 112.5, 'GOOD': 75, 'EXCELLENT': 37.5}

        >>> # BI_EXCELLENT_HI (performance) - assuming 1x/2x formula
        >>> calculate_thresholds(0, "BI_EXCELLENT_HI", 0.1)
        {'VERY_POOR': -0.2, 'POOR': -0.1, 'GOOD': 0.1, 'EXCELLENT': 0.2}
    """
    self.validate_threshold_params(base_pos, direction, steps)

    if direction == self.keys.DIRECTION_INCREASING:
        return {
            self.keys.VERY_POOR: base_pos + steps,
            self.keys.POOR: base_pos + (2 * steps),
            self.keys.GOOD: base_pos + (3 * steps),
            self.keys.EXCELLENT: base_pos + (4 * steps)
        }

    elif direction == self.keys.DIRECTION_DECREASING:
        return {
            self.keys.EXCELLENT: base_pos + steps,
            self.keys.GOOD: base_pos + (2 * steps),
            self.keys.POOR: base_pos + (3 * steps),
            self.keys.VERY_POOR: base_pos + (4 * steps)
        }

    elif direction == self.keys.DIRECTION_BI_EXCELLENT_HI:
        # DECISION PENDING: Use 0.5x/1.5x (spec) or 1x/2x (matches current)
        # Using 1x/2x formula below (recommended):
        return {
            self.keys.VERY_POOR: base_pos - (steps * 2),
            self.keys.POOR: base_pos - steps,
            self.keys.GOOD: base_pos + steps,
            self.keys.EXCELLENT: base_pos + (steps * 2)
        }

    elif direction == self.keys.DIRECTION_BI_EXCELLENT_LOW:
        # Using 1x/2x formula (recommended):
        return {
            self.keys.EXCELLENT: base_pos - (steps * 2),
            self.keys.GOOD: base_pos - steps,
            self.keys.POOR: base_pos + steps,
            self.keys.VERY_POOR: base_pos + (steps * 2)
        }

    else:
        raise ValueError(f"Invalid direction: {direction}")
```

**Files:** `league_helper/util/ConfigManager.py`

**Testing:**
- Unit tests for all 4 direction types
- Verify formulas match current thresholds (once STEPS finalized)
- Test caching behavior

---

#### Task 1.3: Add validate_threshold_params() Method
**Priority:** HIGH
**Time:** 30 minutes

**Implementation:**
```python
def validate_threshold_params(self, base_pos: float, direction: str, steps: float) -> bool:
    """Validate threshold parameters."""
    import math

    # STEPS must be positive
    if steps <= 0:
        self.logger.error(f"STEPS must be positive, got {steps}")
        raise ValueError(f"STEPS must be positive, got {steps}")

    # Must be finite
    if not math.isfinite(base_pos) or not math.isfinite(steps):
        self.logger.error("BASE_POSITION and STEPS must be finite")
        raise ValueError("BASE_POSITION and STEPS must be finite")

    # DIRECTION must be valid
    valid_dirs = [
        self.keys.DIRECTION_INCREASING,
        self.keys.DIRECTION_DECREASING,
        self.keys.DIRECTION_BI_EXCELLENT_HI,
        self.keys.DIRECTION_BI_EXCELLENT_LOW
    ]
    if direction not in valid_dirs:
        self.logger.error(f"DIRECTION must be one of {valid_dirs}, got '{direction}'")
        raise ValueError(f"DIRECTION must be one of {valid_dirs}, got '{direction}'")

    return True
```

**Error Handling Pattern:** Follow ConfigManager pattern - log error before raising ValueError

**Files:** `league_helper/util/ConfigManager.py`

---

#### Task 1.4: Add Threshold Caching
**Priority:** MEDIUM
**Time:** 30 minutes

**Implementation:**
```python
def __init__(self, data_folder: Path):
    # ... existing code ...
    self._threshold_cache: Dict[Tuple, Dict[str, float]] = {}

def calculate_thresholds(self, base_pos: float, direction: str, steps: float,
                         scoring_type: str = "") -> Dict[str, float]:
    # Check cache first
    cache_key = (scoring_type, base_pos, direction, steps)
    if cache_key in self._threshold_cache:
        return self._threshold_cache[cache_key]

    # ... calculation code ...

    # Store in cache
    self._threshold_cache[cache_key] = thresholds
    return thresholds
```

**Files:** `league_helper/util/ConfigManager.py`

---

#### Task 1.5: Update _extract_parameters() to Pre-Calculate Thresholds
**Priority:** HIGH
**Time:** 1 hour

**Implementation:**
```python
def _extract_parameters(self) -> None:
    # ... existing code ...

    # Pre-calculate parameterized thresholds if needed
    for scoring_type in [self.keys.ADP_SCORING, self.keys.PLAYER_RATING_SCORING,
                         self.keys.TEAM_QUALITY_SCORING, self.keys.PERFORMANCE_SCORING,
                         self.keys.MATCHUP_SCORING]:
        scoring_dict = self.parameters[scoring_type]
        thresholds_config = scoring_dict[self.keys.THRESHOLDS]

        # Check if parameterized
        if self.keys.BASE_POSITION in thresholds_config:
            # Calculate and add to thresholds dict
            calculated = self.calculate_thresholds(
                thresholds_config[self.keys.BASE_POSITION],
                thresholds_config[self.keys.DIRECTION],
                thresholds_config[self.keys.STEPS],
                scoring_type
            )

            # Add calculated values to thresholds for direct access
            thresholds_config[self.keys.VERY_POOR] = calculated[self.keys.VERY_POOR]
            thresholds_config[self.keys.POOR] = calculated[self.keys.POOR]
            thresholds_config[self.keys.GOOD] = calculated[self.keys.GOOD]
            thresholds_config[self.keys.EXCELLENT] = calculated[self.keys.EXCELLENT]
```

**Benefit:** `_get_multiplier()` can continue using direct access, no changes needed.

**Files:** `league_helper/util/ConfigManager.py`

---

#### Task 1.6: Write Unit Tests
**Priority:** HIGH
**Time:** 2-3 hours

**Test Coverage:**
- `test_calculate_thresholds_increasing()` - PLAYER_RATING case
- `test_calculate_thresholds_decreasing()` - ADP case
- `test_calculate_thresholds_bi_excellent_hi()` - PERFORMANCE case
- `test_calculate_thresholds_bi_excellent_low()` - edge case
- `test_validate_threshold_params_valid()`
- `test_validate_threshold_params_invalid_steps()`
- `test_validate_threshold_params_invalid_direction()`
- `test_threshold_caching()`
- `test_extract_parameters_calculates_thresholds()`
- `test_backward_compatibility_legacy_format()`

**Files:** `tests/league_helper/util/test_ConfigManager_thresholds.py` (new file)

**Phase 1 Success Criteria:**
- ✅ All new tests pass
- ✅ All existing tests pass (100%)
- ✅ Thresholds calculated correctly
- ✅ Backward compatibility maintained

---

### Phase 2: Config File Migration

#### Task 2.1: Backup Existing Configs
**Priority:** CRITICAL
**Time:** 5 minutes

```bash
mkdir -p data/config_backups
cp data/league_config.json data/config_backups/league_config_backup_$(date +%Y%m%d_%H%M%S).json
```

---

#### Task 2.2: Migrate league_config.json
**Priority:** HIGH
**Time:** 30 minutes

**Manual migration** (5 scoring types):

**ADP_SCORING:**
```json
"THRESHOLDS": {
    "BASE_POSITION": 0,
    "DIRECTION": "DECREASING",
    "STEPS": 37.5
}
```

**PLAYER_RATING_SCORING:**
```json
"THRESHOLDS": {
    "BASE_POSITION": 0,
    "DIRECTION": "INCREASING",
    "STEPS": 20
}
```

**TEAM_QUALITY_SCORING:**
```json
"THRESHOLDS": {
    "BASE_POSITION": 0,
    "DIRECTION": "DECREASING",
    "STEPS": 6.25
}
```

**PERFORMANCE_SCORING:**
```json
"THRESHOLDS": {
    "BASE_POSITION": 0.0,
    "DIRECTION": "BI_EXCELLENT_HI",
    "STEPS": 0.1
}
```

**MATCHUP_SCORING:**
```json
"THRESHOLDS": {
    "BASE_POSITION": 0,
    "DIRECTION": "BI_EXCELLENT_HI",
    "STEPS": 7.5
}
```

**Validation:**
- Run full test suite after migration
- Verify calculated thresholds are close to original values

---

#### Task 2.3: Update Test Fixtures
**Priority:** HIGH
**Time:** 1-2 hours

**Files to update:**
- All test files with hardcoded config dictionaries
- `tests/league_helper/util/test_PlayerManager_scoring.py` (lines 69-160)
- `tests/league_helper/trade_simulator_mode/test_manual_trade_visualizer.py`
- `tests/league_helper/starter_helper_mode/test_StarterHelperModeManager.py`
- `tests/simulation/test_config_generator.py`

**Validation:**
- All tests pass with new format

---

#### Task 2.4: Handle CONSISTENCY_SCORING (Deprecated)
**Priority:** MEDIUM
**Time:** 15 minutes

**Decision:** CONSISTENCY_SCORING is deprecated but still exists in code for backward compatibility.

**Action:**
- Do NOT migrate CONSISTENCY_SCORING in league_config.json
- Keep it as hardcoded thresholds if it exists
- _extract_parameters() should skip it in the threshold calculation loop

**Rationale:** Deprecated feature should not be updated with new system

**Files:** `league_helper/util/ConfigManager.py`

---

### Phase 3: ConfigGenerator Updates

#### Task 3.1: Add THRESHOLD_FIXED_PARAMS Constant
**Priority:** HIGH
**Time:** 15 minutes

```python
THRESHOLD_FIXED_PARAMS = {
    "ADP_SCORING": {
        "BASE_POSITION": 0,
        "DIRECTION": "DECREASING"
    },
    "PLAYER_RATING_SCORING": {
        "BASE_POSITION": 0,
        "DIRECTION": "INCREASING"
    },
    "TEAM_QUALITY_SCORING": {
        "BASE_POSITION": 0,
        "DIRECTION": "DECREASING"
    },
    "PERFORMANCE_SCORING": {
        "BASE_POSITION": 0.0,
        "DIRECTION": "BI_EXCELLENT_HI"
    },
    "MATCHUP_SCORING": {
        "BASE_POSITION": 0,
        "DIRECTION": "BI_EXCELLENT_HI"
    }
}
```

**Files:** `simulation/ConfigGenerator.py`

---

#### Task 3.2: Add STEPS_RANGES Constant
**Priority:** HIGH
**Time:** 15 minutes

```python
STEPS_RANGES = {
    "ADP_SCORING": [30, 35, 37.5, 40, 45],           # Centered on 37.5
    "PLAYER_RATING_SCORING": [12, 16, 20, 24, 28],   # Centered on 20
    "TEAM_QUALITY_SCORING": [4, 5, 6, 7, 8, 9, 10],  # Centered on 7
    "PERFORMANCE_SCORING": [0.05, 0.08, 0.10, 0.12, 0.15, 0.18, 0.20],  # Centered on 0.10
    "MATCHUP_SCORING": [4, 6, 7.5, 9, 12]            # Centered on 7.5
}
```

**Files:** `simulation/ConfigGenerator.py`

---

#### Task 3.3: Add STEPS Parameters to PARAM_DEFINITIONS
**Priority:** HIGH
**Time:** 15 minutes

```python
PARAM_DEFINITIONS = {
    # Existing parameters (unchanged)
    'NORMALIZATION_MAX_SCALE': (10.0, 50.0, 150.0),
    # ... etc ...

    # NEW: Threshold STEPS parameters
    'ADP_SCORING_STEPS': (5.0, 30.0, 45.0),
    'PLAYER_RATING_SCORING_STEPS': (4.0, 12.0, 28.0),
    'TEAM_QUALITY_SCORING_STEPS': (2.0, 4.0, 10.0),
    'PERFORMANCE_SCORING_STEPS': (0.03, 0.05, 0.20),
    'MATCHUP_SCORING_STEPS': (2.0, 4.0, 12.0),
}
```

**Files:** `simulation/ConfigGenerator.py`

---

#### Task 3.4: Update create_config_dict() to Apply STEPS
**Priority:** HIGH
**Time:** 1 hour

```python
def create_config_dict(self, combination: Dict[str, float]) -> dict:
    # ... existing code ...

    # Apply threshold STEPS parameters
    for scoring_type in ["ADP_SCORING", "PLAYER_RATING_SCORING", ...]:
        steps_param = f"{scoring_type}_STEPS"

        if steps_param in combination:
            fixed = self.THRESHOLD_FIXED_PARAMS[scoring_type]
            params[scoring_type]['THRESHOLDS'] = {
                'BASE_POSITION': fixed['BASE_POSITION'],
                'DIRECTION': fixed['DIRECTION'],
                'STEPS': combination[steps_param]
            }

    return config
```

**Files:** `simulation/ConfigGenerator.py`

---

#### Task 3.5: Update ConfigGenerator Tests
**Priority:** HIGH
**Time:** 1-2 hours

- Update test configs to use new format
- Test STEPS generation
- Verify parameter count (9 → 14)

**Files:** `tests/simulation/test_config_generator.py`

---

### Phase 4: Testing & Documentation

#### Task 4.1: Run Full Test Suite
**Priority:** CRITICAL
**Time:** 10 minutes

```bash
python -m pytest tests/ -v
```

**Success:** 318/318 tests passing (100%)

---

#### Task 4.2: Update simulation/README.md
**Priority:** MEDIUM
**Time:** 30 minutes

- Document new threshold system
- Update parameter count (9 → 14)
- Add STEPS optimization examples

**Files:** `simulation/README.md`

---

#### Task 4.3: Manual Testing
**Priority:** MEDIUM
**Time:** 30 minutes

- Run league helper with new config
- Verify threshold behavior is correct
- Check logs for any issues

---

## Timeline Estimate

**Phase 1 (Core):** 6-8 hours
**Phase 2 (Migration):** 2-3 hours
**Phase 3 (ConfigGenerator):** 2-3 hours
**Phase 4 (Testing/Docs):** 2 hours

**Total:** 12-16 hours (~2 days of focused work)

---

## Checklist

### Pre-Implementation
- [ ] User answers formula questions (Q1-Q5)
- [ ] Finalize bidirectional formula (0.5x/1.5x or 1x/2x)
- [ ] Finalize recommended STEPS values

### Phase 1: Core
- [ ] Add ConfigKeys constants
- [ ] Implement calculate_thresholds()
- [ ] Implement validate_threshold_params()
- [ ] Add threshold caching
- [ ] Update _extract_parameters()
- [ ] Write unit tests (100% coverage)
- [ ] All existing tests pass

### Phase 2: Migration
- [ ] Backup league_config.json
- [ ] Migrate league_config.json
- [ ] Update test fixtures
- [ ] All tests pass with new format

### Phase 3: ConfigGenerator
- [ ] Add THRESHOLD_FIXED_PARAMS
- [ ] Add STEPS_RANGES
- [ ] Update PARAM_DEFINITIONS
- [ ] Update create_config_dict()
- [ ] Update ConfigGenerator tests
- [ ] All simulation tests pass

### Phase 4: Final
- [ ] Run full test suite (100%)
- [ ] Update documentation
- [ ] Manual testing
- [ ] File cleanup

---

## Current Status

**Overall:** 0% (Awaiting formula decisions)

**Blockers:** Need user answers to Q1-Q5 in questions file

**Next Step:** Review questions file, finalize formula and STEPS values

---

## Notes

- Much simpler than previous specification
- Main challenge: matching current thresholds with new formula
- Recommend 1x/2x for bidirectional (instead of 0.5x/1.5x)
- All BASE_POSITION = 0 simplifies implementation significantly
- Backward compatibility maintained throughout

---

## Verification Summary

**Verification Protocol Executed:** 2025-10-16

**Iterations Completed:** 3 complete iterations of read-question-research-update

**Requirements Added After Initial Draft:**
1. Q8 backward compatibility requirement (user selected "B - Require migration")
2. Test file pattern identified: `tests/league_helper/util/test_*.py` structure
3. ConfigGenerator threshold handling (currently doesn't handle thresholds, needs addition)
4. Test fixture update requirement for `test_PlayerManager_scoring.py` and other test files with hardcoded configs
5. Task 2.4 added: Handle CONSISTENCY_SCORING (deprecated) - skip migration
6. Error handling pattern: Must log before raising ValueError (ConfigManager convention)
7. TEAM_QUALITY STEPS corrected from 7 to 6.25 (per user's Q3 answer)

**Key Codebase Patterns Identified:**
1. ConfigGenerator uses deep copy pattern: `config = copy.deepcopy(self.baseline_config)`
2. Test fixtures use JSON string literals for configs (see `test_PlayerManager_scoring.py:42-162`)
3. ConfigManager uses `_extract_parameters()` pattern for post-load processing (ConfigManager.py:238)
4. Pytest fixtures pattern for creating test data folders and mock objects
5. No existing threshold calculation code - clean slate for implementation
6. Error handling: `self.logger.error(msg)` THEN `raise ValueError(msg)`
7. Validation pattern: Check required fields, log missing, raise ValueError with list

**Critical Dependencies:**
1. Task 1.5 depends on Tasks 1.2 and 1.3 (needs calculate_thresholds and validate methods)
2. Task 1.6 depends on all Phase 1 tasks (testing implementation)
3. Task 2.2 depends on Phase 1 completion (config migration needs working calculation)
4. Task 2.3 depends on Task 2.2 (test fixtures must match migrated format)
5. Task 2.4 can be done with Task 2.2 (simple - skip CONSISTENCY_SCORING in loop)
6. Phase 3 depends on Phase 2 (ConfigGenerator needs new format to be working)

**Risk Areas:**
1. Breaking existing tests during Phase 2 migration (230+ tests to maintain)
2. Test fixture formats hardcoded in ~12 test files
3. User answered Q7="B" (accept changes) but Q8="B" (require migration) - potential conflict resolved: support both formats via if/else
4. TEAM_QUALITY uses STEPS=6.25 per user decision (corrected in TODO)
5. 15 files import ConfigManager - all must continue working without changes (✅ pre-calculation solves this)
6. CONSISTENCY_SCORING deprecated - added Task 2.4 to handle it (skip migration)

**Files Importing ConfigManager (15 total):**
- league_helper/trade_simulator_mode/TradeSimulatorModeManager.py
- league_helper/util/PlayerManager.py
- league_helper/LeagueHelperManager.py
- league_helper/add_to_roster_mode/AddToRosterModeManager.py
- league_helper/starter_helper_mode/StarterHelperModeManager.py
- league_helper/util/FantasyTeam.py
- simulation/SimulatedLeague.py
- simulation/DraftHelperTeam.py
- simulation/SimulatedOpponent.py
- tests/league_helper/util/test_PlayerManager_scoring.py
- tests/league_helper/trade_simulator_mode/test_manual_trade_visualizer.py
- tests/league_helper/starter_helper_mode/test_StarterHelperModeManager.py
- (+ 3 documentation files)
