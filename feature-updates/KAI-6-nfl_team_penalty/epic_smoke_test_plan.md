# Epic Smoke Test Plan: nfl_team_penalty

**Purpose:** Define how to validate the complete epic end-to-end

**⚠️ VERSION: STAGE 8 (Updated after Feature 01 implementation)**
- **Created:** 2026-01-12 (S1)
- **Last Updated:** 2026-01-14 (S8.P2 - after feature_01_config_infrastructure)
- **Based on:** Feature specs from S2-S3, Feature 01 ACTUAL implementation
- **Quality:** VERIFIED - Test scenarios validated against actual code
- **Next Update:** S8.P2 (after feature_02_score_penalty_application implementation)

---

## Epic Success Criteria

**The epic is successful if ALL of these measurable criteria are met:**

### Criterion 1: Config Infrastructure Works
✅ **MEASURABLE:**
- ConfigManager loads successfully with NFL team penalty settings
- `config.nfl_team_penalty` attribute exists and contains list (e.g., ["LV", "NYJ", "NYG", "KC"])
- `config.nfl_team_penalty_weight` attribute exists and contains float (e.g., 0.75)
- Values match league_config.json settings exactly

**Verification:**
```python
from league_helper.util.ConfigManager import ConfigManager
from pathlib import Path
cm = ConfigManager(Path("data/configs"))
assert hasattr(cm, 'nfl_team_penalty'), "Missing nfl_team_penalty attribute"
assert hasattr(cm, 'nfl_team_penalty_weight'), "Missing nfl_team_penalty_weight attribute"
assert cm.nfl_team_penalty == ["LV", "NYJ", "NYG", "KC"], f"Expected ['LV', 'NYJ', 'NYG', 'KC'], got {cm.nfl_team_penalty}"
assert cm.nfl_team_penalty_weight == 0.75, f"Expected 0.75, got {cm.nfl_team_penalty_weight}"
```

---

### Criterion 2: Score Penalty Applied Correctly
✅ **MEASURABLE:**
- Player from penalized team has reduced score in Add to Roster mode
- Penalty calculation: `penalized_score = original_score × penalty_weight`
- Exact mathematical verification (not just "score is lower")

**Verification:**
```python
# Create test player from penalized team
from utils.FantasyPlayer import FantasyPlayer
from league_helper.util.player_scoring import PlayerScoringCalculator

player = FantasyPlayer(name="Patrick Mahomes", team="KC", ...)  # KC is in penalty list
player.projected_points = 100.0

# Calculate score WITH penalty flag
calc = PlayerScoringCalculator(config)
scored = calc.score_player(player, team_roster=[], nfl_team_penalty=True)

# Verify penalty applied: 100 × 0.75 = 75.0
assert scored.score == 75.0, f"Expected 75.0 (100 × 0.75), got {scored.score}"
```

---

### Criterion 3: Scoring Transparency Works
✅ **MEASURABLE:**
- Scoring reasons list includes penalty reason when applied
- Reason format: `"NFL Team Penalty: {team} ({weight:.2f}x)"`
- Example: `"NFL Team Penalty: KC (0.75x)"`

**Verification:**
```python
# From Criterion 2 test above
scored = calc.score_player(player, team_roster=[], nfl_team_penalty=True)

# Verify reason string present
penalty_reasons = [r for r in scored.reasons if "NFL Team Penalty" in r]
assert len(penalty_reasons) == 1, f"Expected 1 penalty reason, got {len(penalty_reasons)}"
assert "KC" in penalty_reasons[0], f"Expected 'KC' in reason, got {penalty_reasons[0]}"
assert "0.75x" in penalty_reasons[0], f"Expected '0.75x' in reason, got {penalty_reasons[0]}"
```

---

### Criterion 4: Mode Isolation Works
✅ **MEASURABLE:**
- Add to Roster mode applies penalty (flag=True)
- Draft mode does NOT apply penalty (flag=False or default)
- Optimizer mode does NOT apply penalty (flag=False or default)
- Trade Analyzer mode does NOT apply penalty (flag=False or default)

**Verification:**
```python
# Same player from penalized team ("KC")
player = FantasyPlayer(name="Patrick Mahomes", team="KC", ...)
player.projected_points = 100.0

# Add to Roster mode (penalty enabled)
scored_roster = calc.score_player(player, team_roster=[], nfl_team_penalty=True)
assert scored_roster.score == 75.0, "Add to Roster mode should apply penalty"

# Draft mode (penalty disabled)
scored_draft = calc.score_player(player, team_roster=[], nfl_team_penalty=False)
assert scored_draft.score == 100.0, "Draft mode should NOT apply penalty"

# Or use default (no parameter = False)
scored_default = calc.score_player(player, team_roster=[])
assert scored_default.score == 100.0, "Default should NOT apply penalty"
```

---

### Criterion 5: Non-Penalized Teams Unchanged
✅ **MEASURABLE:**
- Player from non-penalized team shows unchanged score
- Scoring reasons do NOT include penalty reason
- Empty reason string for penalty step

**Verification:**
```python
# Player from non-penalized team (e.g., "SF" not in penalty list)
player_sf = FantasyPlayer(name="Brock Purdy", team="SF", ...)
player_sf.projected_points = 100.0

# Even with penalty flag enabled
scored_sf = calc.score_player(player_sf, team_roster=[], nfl_team_penalty=True)

# Verify NO penalty applied
assert scored_sf.score == 100.0, f"Non-penalized team should have unchanged score, got {scored_sf.score}"

# Verify NO penalty reason
penalty_reasons = [r for r in scored_sf.reasons if "NFL Team Penalty" in r]
assert len(penalty_reasons) == 0, f"Non-penalized team should have no penalty reason, got {penalty_reasons}"
```

---

### Criterion 6: Config Validation Works
✅ **MEASURABLE:**
- Invalid team abbreviation raises ValueError
- Weight > 1.0 raises ValueError
- Weight < 0.0 raises ValueError
- Wrong type (string weight, non-list teams) raises ValueError

**Verification:**
```python
import json
from pathlib import Path

# Test 1: Invalid team abbreviation
test_config_invalid_team = {
    "parameters": {
        "NFL_TEAM_PENALTY": ["INVALID", "KC"],
        "NFL_TEAM_PENALTY_WEIGHT": 0.75
    }
}
# Write to temp file, attempt load
# Expected: ValueError with message "invalid team abbreviations"

# Test 2: Weight > 1.0
test_config_high_weight = {
    "parameters": {
        "NFL_TEAM_PENALTY": ["KC"],
        "NFL_TEAM_PENALTY_WEIGHT": 1.5
    }
}
# Expected: ValueError with message "must be between 0.0 and 1.0"

# Test 3: Weight < 0.0
test_config_neg_weight = {
    "parameters": {
        "NFL_TEAM_PENALTY": ["KC"],
        "NFL_TEAM_PENALTY_WEIGHT": -0.5
    }
}
# Expected: ValueError with message "must be between 0.0 and 1.0"
```

---

### Criterion 7: Simulation Configs Use Defaults
✅ **MEASURABLE:**
- All 9 simulation config files contain NFL_TEAM_PENALTY = []
- All 9 simulation config files contain NFL_TEAM_PENALTY_WEIGHT = 1.0
- Simulations remain objective (no team bias)

**Verification:**
```bash
# Check all 9 simulation configs
for config in simulation/simulation_configs/*/league_config.json; do
  echo "Checking $config"
  grep '"NFL_TEAM_PENALTY": \[\]' "$config" || echo "FAIL: Missing or wrong NFL_TEAM_PENALTY"
  grep '"NFL_TEAM_PENALTY_WEIGHT": 1.0' "$config" || echo "FAIL: Missing or wrong NFL_TEAM_PENALTY_WEIGHT"
done
```

**Files to verify:**
1. `simulation/simulation_configs/accuracy_intermediate_00_NORMALIZATION_MAX_SCALE/league_config.json`
2. `simulation/simulation_configs/accuracy_intermediate_01_TEAM_QUALITY_SCORING_WEIGHT/league_config.json`
3. `simulation/simulation_configs/accuracy_intermediate_02_TEAM_QUALITY_MIN_WEEKS/league_config.json`
4. `simulation/simulation_configs/accuracy_intermediate_03_PERFORMANCE_SCORING_WEIGHT/league_config.json`
5. `simulation/simulation_configs/accuracy_intermediate_04_PERFORMANCE_SCORING_STEPS/league_config.json`
6. `simulation/simulation_configs/accuracy_intermediate_05_PERFORMANCE_MIN_WEEKS/league_config.json`
7. `simulation/simulation_configs/accuracy_optimal_2025-12-23_06-51-56/league_config.json`
8. `simulation/simulation_configs/intermediate_01_DRAFT_NORMALIZATION_MAX_SCALE/league_config.json`
9. `simulation/simulation_configs/optimal_iterative_20260104_080756/league_config.json`

---

### Criterion 8: Edge Cases Handled
✅ **MEASURABLE:**
- Empty penalty list ([]) works without errors
- Penalty weight = 0.0 produces score of 0.0
- Penalty weight = 1.0 produces unchanged score
- Missing config keys use defaults (backward compatibility)

**Verification:**
```python
# Test 1: Empty penalty list
config.nfl_team_penalty = []
scored = calc.score_player(player_kc, team_roster=[], nfl_team_penalty=True)
assert scored.score == 100.0, "Empty penalty list should not apply penalty"

# Test 2: Weight = 0.0 (complete penalty)
config.nfl_team_penalty = ["KC"]
config.nfl_team_penalty_weight = 0.0
scored = calc.score_player(player_kc, team_roster=[], nfl_team_penalty=True)
assert scored.score == 0.0, "Weight 0.0 should produce score 0.0"

# Test 3: Weight = 1.0 (no effect)
config.nfl_team_penalty_weight = 1.0
scored = calc.score_player(player_kc, team_roster=[], nfl_team_penalty=True)
assert scored.score == 100.0, "Weight 1.0 should not change score"

# Test 4: Missing config keys (backward compatibility)
# Config file without NFL_TEAM_PENALTY keys should load successfully
# and use defaults ([], 1.0)
```

---

### Criterion 9: All Unit Tests Pass
✅ **MEASURABLE:**
- `test_ConfigManager_nfl_team_penalty.py` passes (100%)
- `test_player_scoring_nfl_team_penalty.py` passes (100%)
- All existing tests still pass (no regressions)
- Exit code 0 from `python tests/run_all_tests.py`

**Verification:**
```bash
python tests/run_all_tests.py
# Expected: All tests pass, exit code 0
```

---

### Criterion 10: Integration Points Work
✅ **MEASURABLE:** (from S3 Cross-Feature Sanity Check)
- Feature 01 provides: `config.nfl_team_penalty` (List[str]), `config.nfl_team_penalty_weight` (float)
- Feature 02 consumes: Same config attributes (read-only)
- Data flow: ConfigManager → PlayerScoringCalculator → AddToRosterModeManager
- No circular dependencies
- Zero file overlaps between features

**Verification:**
```python
# End-to-end integration test
from league_helper.add_to_roster_mode.AddToRosterModeManager import AddToRosterModeManager

# Initialize Add to Roster mode with penalty config
manager = AddToRosterModeManager(data_folder=Path("data/configs"))

# Get recommendations (should apply penalty internally)
recommendations = manager.get_recommendations(position="QB", current_round=3)

# Verify penalized team players have reduced scores
penalized_teams = manager.config.nfl_team_penalty  # ["LV", "NYJ", "NYG", "KC"]
for rec in recommendations:
    if rec.player.team in penalized_teams:
        # Score should be reduced (cannot verify exact value without baseline,
        # but can verify penalty reason present)
        assert any("NFL Team Penalty" in r for r in rec.reasons), \
            f"Player {rec.player.name} from {rec.player.team} should have penalty reason"
```

---

## Specific Test Scenarios

**These tests MUST be run for epic-level validation:**

---

### Test Scenario 1: Config Loading and Validation

**Purpose:** Verify Feature 01 loads and validates config settings correctly

**Pre-condition:** league_config.json contains NFL_TEAM_PENALTY and NFL_TEAM_PENALTY_WEIGHT

**Steps:**
1. Read league_config.json and verify JSON structure
2. Load ConfigManager
3. Verify config attributes exist and have correct values
4. Test validation with invalid values

**Commands:**
```bash
# Verify JSON structure
python -c "
import json
with open('data/configs/league_config.json') as f:
    data = json.load(f)
    print('NFL_TEAM_PENALTY:', data['parameters'].get('NFL_TEAM_PENALTY'))
    print('NFL_TEAM_PENALTY_WEIGHT:', data['parameters'].get('NFL_TEAM_PENALTY_WEIGHT'))
"

# Load ConfigManager and verify
python -c "
from league_helper.util.ConfigManager import ConfigManager
from pathlib import Path
cm = ConfigManager(Path('data/configs'))
print('Teams:', cm.nfl_team_penalty)
print('Weight:', cm.nfl_team_penalty_weight)
assert cm.nfl_team_penalty == ['LV', 'NYJ', 'NYG', 'KC']
assert cm.nfl_team_penalty_weight == 0.75
print('✅ Config loading PASSED')
"
```

**Expected Results:**
- ✅ JSON contains `"NFL_TEAM_PENALTY": ["LV", "NYJ", "NYG", "KC"]`
- ✅ JSON contains `"NFL_TEAM_PENALTY_WEIGHT": 0.75`
- ✅ ConfigManager loads without errors
- ✅ `cm.nfl_team_penalty` == `["LV", "NYJ", "NYG", "KC"]`
- ✅ `cm.nfl_team_penalty_weight` == `0.75`

**Failure Indicators:**
- ❌ KeyError → JSON missing keys (Feature 01 didn't update config file)
- ❌ AttributeError → ConfigManager missing attributes (Feature 01 didn't add instance variables)
- ❌ Value mismatch → Extraction logic incorrect

---

### Test Scenario 2: Score Penalty Application (Penalized Team)

**Purpose:** Verify Feature 02 applies penalty correctly to penalized team players

**Pre-condition:** Player from penalized team (e.g., "KC")

**Steps:**
1. Create test player from penalized team with known projected points
2. Calculate score WITH penalty flag enabled
3. Verify score equals (original × weight)
4. Verify penalty reason in reasons list

**Commands:**
```python
from utils.FantasyPlayer import FantasyPlayer
from league_helper.util.player_scoring import PlayerScoringCalculator
from league_helper.util.ConfigManager import ConfigManager
from pathlib import Path

# Load config
cm = ConfigManager(Path('data/configs'))
calc = PlayerScoringCalculator(cm)

# Create test player (Patrick Mahomes, KC)
player = FantasyPlayer(
    name="Patrick Mahomes",
    position="QB",
    team="KC",  # KC is in penalty list
    projected_points=100.0
)

# Calculate score WITH penalty
scored = calc.score_player(
    player,
    team_roster=[],
    nfl_team_penalty=True  # Enable penalty
)

# Verify penalty applied
expected_score = 100.0 * 0.75  # 75.0
print(f"Score: {scored.score} (expected: {expected_score})")
assert abs(scored.score - expected_score) < 0.01, f"Score mismatch: {scored.score} != {expected_score}"

# Verify penalty reason
penalty_reasons = [r for r in scored.reasons if "NFL Team Penalty" in r]
print(f"Penalty reasons: {penalty_reasons}")
assert len(penalty_reasons) == 1, f"Expected 1 penalty reason, got {len(penalty_reasons)}"
assert "KC" in penalty_reasons[0], f"Expected 'KC' in reason"
assert "0.75x" in penalty_reasons[0], f"Expected '0.75x' in reason"

print("✅ Score penalty application PASSED")
```

**Expected Results:**
- ✅ `scored.score` == 75.0 (100.0 × 0.75)
- ✅ `scored.reasons` contains `"NFL Team Penalty: KC (0.75x)"`
- ✅ No errors during execution

**Failure Indicators:**
- ❌ Score == 100.0 → Penalty not applied
- ❌ Score != 75.0 → Incorrect calculation
- ❌ No penalty reason → Transparency broken

---

### Test Scenario 3: Score Penalty NOT Applied (Non-Penalized Team)

**Purpose:** Verify Feature 02 does NOT apply penalty to non-penalized team players

**Pre-condition:** Player from non-penalized team (e.g., "SF")

**Steps:**
1. Create test player from non-penalized team
2. Calculate score WITH penalty flag enabled
3. Verify score unchanged
4. Verify NO penalty reason in reasons list

**Commands:**
```python
# Same setup as Scenario 2, but different team
player_sf = FantasyPlayer(
    name="Brock Purdy",
    position="QB",
    team="SF",  # SF NOT in penalty list
    projected_points=100.0
)

# Calculate score WITH penalty flag enabled
scored_sf = calc.score_player(
    player_sf,
    team_roster=[],
    nfl_team_penalty=True  # Flag enabled but team not in list
)

# Verify NO penalty applied
print(f"Score: {scored_sf.score} (expected: 100.0)")
assert scored_sf.score == 100.0, f"Non-penalized team should have unchanged score"

# Verify NO penalty reason
penalty_reasons = [r for r in scored_sf.reasons if "NFL Team Penalty" in r]
print(f"Penalty reasons: {penalty_reasons}")
assert len(penalty_reasons) == 0, f"Non-penalized team should have no penalty reason"

print("✅ Non-penalized team unchanged PASSED")
```

**Expected Results:**
- ✅ `scored_sf.score` == 100.0 (unchanged)
- ✅ `scored_sf.reasons` does NOT contain penalty reason
- ✅ No errors during execution

**Failure Indicators:**
- ❌ Score != 100.0 → Penalty incorrectly applied
- ❌ Penalty reason present → Logic error

---

### Test Scenario 4: Mode Isolation (Draft Mode Does NOT Apply Penalty)

**Purpose:** Verify penalty only applies in Add to Roster mode, not other modes

**Pre-condition:** Player from penalized team (e.g., "KC")

**Steps:**
1. Create test player from penalized team
2. Calculate score WITHOUT penalty flag (default)
3. Verify score unchanged
4. Verify this is how draft mode behaves

**Commands:**
```python
# Same player from penalized team
player_kc = FantasyPlayer(
    name="Patrick Mahomes",
    position="QB",
    team="KC",  # KC is in penalty list
    projected_points=100.0
)

# Calculate score WITHOUT penalty flag (default behavior)
scored_draft = calc.score_player(
    player_kc,
    team_roster=[]
    # nfl_team_penalty NOT specified → defaults to False
)

# Verify NO penalty applied (draft mode behavior)
print(f"Score: {scored_draft.score} (expected: 100.0)")
assert scored_draft.score == 100.0, f"Draft mode should NOT apply penalty"

# Verify NO penalty reason
penalty_reasons = [r for r in scored_draft.reasons if "NFL Team Penalty" in r]
assert len(penalty_reasons) == 0, f"Draft mode should have no penalty reason"

print("✅ Mode isolation PASSED")
```

**Expected Results:**
- ✅ `scored_draft.score` == 100.0 (penalty NOT applied)
- ✅ No penalty reason in `scored_draft.reasons`
- ✅ Other modes (optimizer, trade) behave the same way

**Failure Indicators:**
- ❌ Score == 75.0 → Penalty incorrectly applied to draft mode
- ❌ Penalty cannot be disabled → Mode isolation broken

---

### Test Scenario 5: End-to-End Add to Roster Mode

**Purpose:** Verify complete workflow with penalty in Add to Roster mode

**Pre-condition:** league_config.json has penalty settings, player data loaded

**Steps:**
1. Launch league helper
2. Select Add to Roster mode
3. View recommendations for position (e.g., QB)
4. Verify penalized team players have reduced scores
5. Verify scoring reasons show penalty transparency

**Commands:**
```bash
# Interactive E2E test (manual verification)
python run_league_helper.py
# Select: Add to Roster
# Enter position: QB
# Check recommendations for KC/NYJ/LV/NYG players
# Verify: Reduced scores + "NFL Team Penalty" in reasons
```

**Expected Results:**
- ✅ Add to Roster mode launches successfully
- ✅ QB recommendations displayed
- ✅ Patrick Mahomes (KC) shows reduced score
- ✅ Scoring reasons include "NFL Team Penalty: KC (0.75x)"
- ✅ Non-penalized QB (e.g., Brock Purdy, SF) shows normal score
- ✅ Program exits cleanly

**Failure Indicators:**
- ❌ Import error → Module integration issue
- ❌ Penalized players show normal scores → Penalty not applied
- ❌ No penalty reason displayed → Transparency broken
- ❌ Crash during execution → Runtime error

---

### Test Scenario 6: Config Validation (Invalid Values)

**Purpose:** Verify Feature 01 validation rejects invalid config values

**Pre-condition:** Ability to create temporary config files

**Steps:**
1. Create temp config with invalid team abbreviation
2. Attempt to load ConfigManager
3. Verify ValueError raised with descriptive message
4. Repeat for weight > 1.0, weight < 0.0

**Commands:**
```python
import json
import tempfile
from pathlib import Path
from league_helper.util.ConfigManager import ConfigManager

# Test 1: Invalid team abbreviation
temp_dir = Path(tempfile.mkdtemp())
temp_config = temp_dir / "league_config.json"

invalid_config = {
    "config_name": "Test Config",
    "description": "Invalid team test",
    "parameters": {
        "NFL_TEAM_PENALTY": ["INVALID_TEAM", "KC"],
        "NFL_TEAM_PENALTY_WEIGHT": 0.75
    }
}

with open(temp_config, 'w') as f:
    json.dump(invalid_config, f)

try:
    cm = ConfigManager(temp_dir)
    print("❌ FAILED: Should have raised ValueError for invalid team")
except ValueError as e:
    assert "invalid team abbreviations" in str(e).lower(), f"Wrong error message: {e}"
    print(f"✅ PASSED: Invalid team rejected with message: {e}")

# Test 2: Weight > 1.0
invalid_config['parameters']['NFL_TEAM_PENALTY'] = ["KC"]
invalid_config['parameters']['NFL_TEAM_PENALTY_WEIGHT'] = 1.5

with open(temp_config, 'w') as f:
    json.dump(invalid_config, f)

try:
    cm = ConfigManager(temp_dir)
    print("❌ FAILED: Should have raised ValueError for weight > 1.0")
except ValueError as e:
    assert "between 0.0 and 1.0" in str(e).lower(), f"Wrong error message: {e}"
    print(f"✅ PASSED: High weight rejected with message: {e}")

# Test 3: Weight < 0.0
invalid_config['parameters']['NFL_TEAM_PENALTY_WEIGHT'] = -0.5

with open(temp_config, 'w') as f:
    json.dump(invalid_config, f)

try:
    cm = ConfigManager(temp_dir)
    print("❌ FAILED: Should have raised ValueError for weight < 0.0")
except ValueError as e:
    assert "between 0.0 and 1.0" in str(e).lower(), f"Wrong error message: {e}"
    print(f"✅ PASSED: Negative weight rejected with message: {e}")

print("✅ Config validation PASSED")
```

**Expected Results:**
- ✅ Invalid team → ValueError with "invalid team abbreviations"
- ✅ Weight > 1.0 → ValueError with "between 0.0 and 1.0"
- ✅ Weight < 0.0 → ValueError with "between 0.0 and 1.0"
- ✅ All error messages are descriptive

**Failure Indicators:**
- ❌ No error raised → Validation not working
- ❌ Wrong error type → Incorrect exception handling
- ❌ Vague error message → Poor user experience

---

### Test Scenario 7: Simulation Compatibility (Backward Compatibility)

**Purpose:** Verify simulations continue working after adding parameter

**Pre-condition:** Simulation configs have defaults ([], 1.0), simulation tests exist

**Steps:**
1. Run existing simulation tests
2. Verify AccuracySimulationManager works (doesn't pass parameter → uses default False)
3. Verify ParallelAccuracyRunner works (doesn't pass parameter → uses default False)
4. Verify simulation results unchanged from baseline

**Commands:**
```bash
# Run simulation tests (should pass without modification)
python tests/simulation/test_accuracy_simulation.py
python tests/simulation/test_parallel_runner.py

# Expected: All tests pass, exit code 0
```

**Expected Results:**
- ✅ Simulation tests pass (100%)
- ✅ No errors from missing parameter
- ✅ Simulation results unchanged (no penalty applied)
- ✅ ConfigManager loads simulation configs successfully

**Failure Indicators:**
- ❌ TypeError: missing parameter → Backward compatibility broken
- ❌ Tests fail → Regression introduced
- ❌ Different results → Penalty incorrectly applied to simulations

---

### Test Scenario 8: All Unit Tests Pass

**Purpose:** Verify all tests pass (existing + new)

**Pre-condition:** All features implemented, test files created

**Steps:**
1. Run full test suite
2. Verify 100% pass rate
3. Verify new test files included

**Commands:**
```bash
# Run all tests
python tests/run_all_tests.py

# Check for new test files
ls tests/league_helper/util/test_ConfigManager_nfl_team_penalty.py
ls tests/league_helper/util/test_player_scoring_nfl_team_penalty.py
```

**Expected Results:**
- ✅ All tests pass (exit code 0)
- ✅ New test files present
- ✅ No regressions in existing tests
- ✅ Coverage includes new code (config loading, penalty application)

**Failure Indicators:**
- ❌ Any test fails → Must fix before merging
- ❌ Missing test files → Incomplete implementation
- ❌ Regression in existing tests → Introduced bug

---

## Integration Points Identified

*From S3 Cross-Feature Sanity Check (SANITY_CHECK_2026-01-13.md)*

### Integration Point 1: ConfigManager → PlayerScoringCalculator

**Features Involved:** Feature 01, Feature 02
**Type:** Data provider/consumer relationship
**Flow:**
- Feature 01 (config_infrastructure): ConfigManager loads and validates config values
- Feature 02 (score_penalty_application): PlayerScoringCalculator reads config values

**Data Passed:**
- `config.nfl_team_penalty: List[str]` (e.g., ["LV", "NYJ", "NYG", "KC"])
- `config.nfl_team_penalty_weight: float` (e.g., 0.75)

**Test Need:** Verify PlayerScoringCalculator can access config attributes (Scenario 2)

---

### Integration Point 2: PlayerScoringCalculator → AddToRosterModeManager

**Features Involved:** Feature 02
**Type:** Mode-specific behavior
**Flow:**
- AddToRosterModeManager calls PlayerScoringCalculator.score_player() with `nfl_team_penalty=True`
- Other modes (draft, optimizer, trade) call with `nfl_team_penalty=False` or default

**Data Passed:**
- Boolean flag: `nfl_team_penalty` (True for Add to Roster, False for others)

**Test Need:** Verify mode isolation (Scenario 4, 5)

---

### Integration Point 3: FantasyPlayer.team → Penalty Check

**Features Involved:** Feature 02
**Type:** Data attribute access
**Flow:**
- PlayerScoringCalculator reads `player.team` attribute
- Checks if `player.team in config.nfl_team_penalty`
- Applies penalty if match found

**Data Passed:**
- `player.team: str` (e.g., "KC", "SF")

**Test Need:** Verify team check logic (Scenario 2, 3)

---

### Integration Point 4: league_config.json → ConfigManager

**Features Involved:** Feature 01
**Type:** File I/O and JSON parsing
**Flow:**
- ConfigManager reads league_config.json
- Extracts NFL_TEAM_PENALTY and NFL_TEAM_PENALTY_WEIGHT from "parameters" object
- Validates values

**Data Passed:**
- JSON structure with config keys

**Test Need:** Verify config loading (Scenario 1)

---

### Integration Point 5: Simulation Configs → Backward Compatibility

**Features Involved:** Feature 01, Feature 02
**Type:** Default value handling
**Flow:**
- Simulation configs have defaults ([], 1.0)
- ConfigManager loads successfully
- PlayerScoringCalculator parameter defaults to False
- Simulations unaffected (no penalty applied)

**Data Passed:**
- Default values from Feature 01
- Default parameter from Feature 02

**Test Need:** Verify simulation compatibility (Scenario 7)

---

## High-Level Test Categories

**Agent will create additional scenarios for these categories during S8.P2 (after each feature implementation):**

### Category 1: Error Handling and Edge Cases

**What to test:** Graceful handling of unusual inputs
**Known scenarios:**
- Empty penalty list (Criterion 8)
- Boundary weights (0.0, 1.0)
- Missing config keys (backward compatibility)

**S8.P2 will add:** Additional edge cases discovered during implementation

---

### Category 2: Performance and Scalability

**What to test:** Epic doesn't slow down significantly
**Known concerns:**
- Penalty check is O(n) where n = penalty list length (typically 4 teams)
- Minimal performance impact expected

**S8.P2 will add:** Performance benchmarks after implementation

---

### Category 3: User Experience

**What to test:** Feature is intuitive and transparent
**Known scenarios:**
- Scoring reasons clearly show penalty (Criterion 3)
- Config validation provides helpful error messages (Scenario 6)

**S8.P2 will add:** User experience feedback after manual testing

---

## Update Log

| Date | Stage | What Changed | Why |
|------|-------|--------------|-----|
| 2026-01-12 | S1 | Initial placeholder plan created | Epic planning - assumptions only |
| 2026-01-13 | S4 | **MAJOR UPDATE** - Replaced with concrete test plan | Based on feature specs (S2) and cross-feature sanity check (S3) |
| 2026-01-14 | S8.P2 | Verified against Feature 01 actual implementation - No changes needed | Feature 01 (config_infrastructure) implementation matches S4 plan exactly. All test scenarios remain accurate. |

**S4 changes:**
- Replaced 5 placeholder scenarios with 8 specific test scenarios
- Added 10 measurable success criteria (was vague)
- Identified 5 integration points between features (from S3)
- Added concrete Python/bash commands and expected outputs
- Added data quality checks (verify VALUES: scores = 75.0, reasons = "NFL Team Penalty: KC (0.75x)")
- Documented failure indicators for each test
- Added integration point documentation from S3 cross-feature analysis

**S8.P2 verification (Feature 01 - 2026-01-14):**
- Reviewed actual ConfigManager.py implementation (lines 76-77, 227-228, 1067-1101)
- Verified ConfigKeys constants: NFL_TEAM_PENALTY, NFL_TEAM_PENALTY_WEIGHT
- Verified instance variables: nfl_team_penalty (List[str]), nfl_team_penalty_weight (float)
- Verified .get() extraction pattern with defaults ([], 1.0) for backward compatibility
- Verified validation logic:
  - List type validation (line 1075-1078)
  - Team abbreviation validation against ALL_NFL_TEAMS (1080-1088)
  - Weight type validation (1091-1095)
  - Weight range validation 0.0-1.0 (1097-1101)
- **Result:** All S4 test scenarios remain accurate - implementation matches spec exactly
- **New scenarios added:** NONE (config-only feature, no unexpected behaviors discovered)

**Current version is informed by:**
- S1: Initial assumptions from epic request
- S4: Feature specs (S2) and approved cross-feature sanity check (S3)
- **S8.P2 (Feature 01): Actual ConfigManager implementation** ← YOU ARE HERE
- S8.P2 (Feature 02): (Pending) Will update after feature_02 implementation

**Next update:** S8.P2 (after feature_02_score_penalty_application completes)

---

## User Approval

**Status:** ✅ APPROVED (Gate 4.5 - PASSED)

**Approved:** 2026-01-13
**User response:** "approved proceed to S5"

**User approved:**
- ✅ Test scenarios are comprehensive enough
- ✅ Success criteria measure the right things
- ✅ Integration points are correct
- ✅ Data quality checks verify the right values

**Gate 4.5:** PASSED - Ready to proceed to S5 (Implementation Planning)

---

## Notes

**Key improvements from S1 to S4:**
- **Specificity:** Replaced "verify penalty works" with exact calculation checks (score = 100 × 0.75 = 75.0)
- **Measurability:** Success criteria are now verifiable with assertions
- **Integration awareness:** Documented 5 integration points from S3 analysis
- **Data quality:** Verify VALUES not just structure (scores, reason strings, config values)
- **Commands:** Concrete Python/bash commands ready to execute

**This plan will evolve:**
- S8.P2 will add implementation-specific tests after each feature completes
- S8.P2 will update based on actual code (not just specs)
- Final version in S9 (Epic Final QC) will be most comprehensive
