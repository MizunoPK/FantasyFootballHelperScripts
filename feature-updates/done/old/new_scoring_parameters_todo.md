# New Scoring Parameters Implementation TODO

**Objective**: Implement 3 new scoring parameters (Temperature, Wind, Location) based on game condition data.

**Source**: `docs/research/game_conditions_scoring_implementation.md`

**Status**: VERIFIED - Ready for implementation (12/12 iterations complete)

**Important**: Keep this file updated as work progresses. If a new Claude agent needs to continue work, this file should contain all context needed.

---

## Phase 1: Configuration Updates

### 1.1 Update ConfigKeys Class
**File**: `league_helper/util/ConfigManager.py`
**Lines**: ~33-110

- [ ] Add `TEMPERATURE_SCORING = "TEMPERATURE_SCORING"` to ConfigKeys
- [ ] Add `WIND_SCORING = "WIND_SCORING"` to ConfigKeys
- [ ] Add `LOCATION_MODIFIERS = "LOCATION_MODIFIERS"` to ConfigKeys
- [ ] Add `IDEAL_TEMPERATURE = "IDEAL_TEMPERATURE"` to ConfigKeys

### 1.2 Update ConfigManager Attributes
**File**: `league_helper/util/ConfigManager.py`
**Lines**: ~175-195

- [ ] Add `self.temperature_scoring: Dict[str, Any] = {}` attribute
- [ ] Add `self.wind_scoring: Dict[str, Any] = {}` attribute
- [ ] Add `self.location_modifiers: Dict[str, float] = {}` attribute

### 1.3 Update _extract_parameters Method
**File**: `league_helper/util/ConfigManager.py`
**Lines**: ~743-917

- [ ] Extract TEMPERATURE_SCORING (optional for backwards compatibility)
- [ ] Extract WIND_SCORING (optional for backwards compatibility)
- [ ] Extract LOCATION_MODIFIERS (optional for backwards compatibility)
- [ ] Pre-calculate thresholds for TEMPERATURE_SCORING
- [ ] Pre-calculate thresholds for WIND_SCORING
- [ ] Validate IDEAL_TEMPERATURE exists in TEMPERATURE_SCORING

### 1.4 Add New Multiplier Methods
**File**: `league_helper/util/ConfigManager.py`
**After line**: ~298

- [ ] Add `get_temperature_score(temperature: int) -> float` method
  - Returns distance from ideal temperature (e.g., |temp - 60|)
- [ ] Add `get_temperature_multiplier(temp_distance: float) -> Tuple[float, str]` method
  - CRITICAL: Must use `rising_thresholds=False` (lower distance = better)
- [ ] Add `get_wind_multiplier(wind_gust: float) -> Tuple[float, str]` method
  - CRITICAL: Must use `rising_thresholds=False` (lower wind = better)
- [ ] Add `get_location_modifier(game: UpcomingGame, team: str) -> float` method

### 1.5 Update league_config.json
**File**: `data/league_config.json`

- [ ] Add TEMPERATURE_SCORING with IMPACT_SCALE, IDEAL_TEMPERATURE, THRESHOLDS, MULTIPLIERS, WEIGHT
- [ ] Add WIND_SCORING with IMPACT_SCALE, THRESHOLDS, MULTIPLIERS, WEIGHT
- [ ] Add LOCATION_MODIFIERS with HOME, AWAY, INTERNATIONAL values

### 1.6 Add WIND_AFFECTED_POSITIONS to constants.py
**File**: `league_helper/constants.py`

- [ ] Add `WIND_AFFECTED_POSITIONS = ["QB", "WR", "K"]` after OFFENSE_POSITIONS (line ~67)
- [ ] Use this constant in _apply_wind_scoring() to skip non-affected positions

### 1.7 Phase 1 Validation
- [ ] Run all unit tests: `python tests/run_all_tests.py`
- [ ] Verify ConfigManager loads new parameters correctly
- [ ] Verify backwards compatibility (configs without new params still work)

---

## Phase 2: Game Data Management

### 2.1 Create UpcomingGame Data Class
**New File**: `league_helper/util/game_data_models.py`

- [ ] Create `UpcomingGame` dataclass with fields:
  - home_team: str
  - away_team: str
  - temperature: Optional[int] (None for indoor)
  - wind_gust: Optional[int] (None for indoor)
  - indoor: bool
  - neutral_site: bool
  - country: str (default "USA")
- [ ] Add `is_home_game(team: str) -> bool` method
- [ ] Add `is_international() -> bool` method

### 2.2 Create GameDataManager Class
**New File**: `league_helper/util/GameDataManager.py`

- [ ] Create GameDataManager class
- [ ] Implement `__init__(data_folder: Path, current_week: int)` method
- [ ] Implement `_load_current_week_games(data_folder: Path)` method
  - Load game_data.csv
  - Filter to current week only
  - Index by both home_team and away_team for O(1) lookup
- [ ] Implement `get_game(team: str) -> Optional[UpcomingGame]` method
  - Returns None for bye weeks

### 2.3 Integrate GameDataManager with LeagueHelperManager
**File**: `league_helper/LeagueHelperManager.py`

- [ ] Import GameDataManager
- [ ] Initialize GameDataManager after ConfigManager
- [ ] Pass GameDataManager to PlayerManager (or directly to PlayerScoringCalculator)

### 2.4 Phase 2 Validation
- [ ] Run all unit tests: `python tests/run_all_tests.py`
- [ ] Verify GameDataManager loads game_data.csv correctly
- [ ] Verify bye week handling (get_game returns None)
- [ ] Verify indoor games have None for temperature/wind

---

## Phase 3: Scoring Integration

### 3.1 Update PlayerScoringCalculator Constructor
**File**: `league_helper/util/player_scoring.py`
**Lines**: ~59-86

- [ ] Add `game_data_manager: Optional[GameDataManager] = None` parameter
- [ ] Store as `self.game_data_manager`

### 3.2 Add New Scoring Methods
**File**: `league_helper/util/player_scoring.py`
**After line**: ~660

- [ ] Add `_apply_temperature_scoring(p: FantasyPlayer, player_score: float) -> Tuple[float, str]`
  - Step 11: Temperature bonus/penalty
  - Skip if no game data (bye week)
  - Skip if indoor game
  - Skip if no temperature data
  - **Applies to ALL positions**
  - Calculate distance from ideal, get multiplier, apply bonus
- [ ] Add `_apply_wind_scoring(p: FantasyPlayer, player_score: float) -> Tuple[float, str]`
  - Step 12: Wind bonus/penalty
  - Skip if no game data (bye week)
  - Skip if indoor game
  - Skip if no wind data
  - **ONLY applies to QB, WR, K positions** (skip RB, TE, DST)
  - Get wind multiplier, apply bonus
- [ ] Add `_apply_location_modifier(p: FantasyPlayer, player_score: float) -> Tuple[float, str]`
  - Step 13: Location bonus/penalty
  - Skip if no game data (bye week)
  - Get location modifier, apply

### 3.3 Update score_player Method Signatures (TWO FILES)

**File 1**: `league_helper/util/player_scoring.py` (PlayerScoringCalculator.score_player)
**Line**: ~318

- [ ] Add `temperature=False` parameter
- [ ] Add `wind=False` parameter
- [ ] Add `location=False` parameter
- [ ] Add Steps 11-13 in method body after Step 10

**File 2**: `league_helper/util/PlayerManager.py` (PlayerManager.score_player wrapper)
**Line**: ~558

- [ ] Add `temperature=False` parameter to signature
- [ ] Add `wind=False` parameter to signature
- [ ] Add `location=False` parameter to signature
- [ ] Pass new parameters through to `self.scoring_calculator.score_player(...)`

### 3.4 Update StarterHelperModeManager
**File**: `league_helper/starter_helper_mode/StarterHelperModeManager.py`
**Method**: `create_starting_recommendation()` at lines 365-376

- [ ] Add `temperature=True` to score_player call
- [ ] Add `wind=True` to score_player call
- [ ] Add `location=True` to score_player call
- [ ] Update docstring to mention game condition scoring (lines 350-357)

### 3.5 Phase 3 Validation
- [ ] Run all unit tests: `python tests/run_all_tests.py`
- [ ] Verify scoring steps 11-13 are applied in Starter Helper mode
- [ ] Verify scoring steps 11-13 are NOT applied in Add to Roster mode
- [ ] Manual test with actual game data

---

## Phase 4: Simulation Integration (Full Integration per User Answer Q2)

### 4.1 Game Data for Simulation
**Files**:
- `simulation/sim_data/game_data.csv` - Already contains 2024 historical data (verified)

- [ ] Verify simulation game_data.csv has all weeks 1-17 for 2024 season
- [ ] Ensure CSV format matches expected columns

### 4.2 Update DraftHelperTeam.set_weekly_lineup() for GameDataManager
**File**: `simulation/DraftHelperTeam.py` (lines 158-188)

- [ ] Create GameDataManager at start of set_weekly_lineup(week) method
  - GameDataManager needs `current_week` parameter which changes each call
  - GameDataManager loads only that week's game data from CSV
- [ ] Pass GameDataManager to PlayerManager (via setter or update constructor chain)
- [ ] Current flow: DraftHelperTeam → StarterHelperModeManager → optimize_lineup() → score_player()
- [ ] GameDataManager must be accessible by PlayerScoringCalculator for _apply_temperature/wind/location

### 4.2b Consider GameDataManager Design for Week-by-Week Loading
**Files**:
- `league_helper/util/GameDataManager.py` (new)

- [ ] GameDataManager should support loading ALL weeks at init, then filter by current_week
  - OR: Accept week parameter in get_game() method
  - Recommendation: Load all weeks once, filter by week in get_game()
  - This avoids re-reading CSV 16+ times per simulation

### 4.3 Update ConfigGenerator
**File**: `simulation/ConfigGenerator.py`

- [ ] Add TEMPERATURE parameters to PARAM_DEFINITIONS:
  - TEMPERATURE_IMPACT_SCALE: (30.0, 80.0)
  - TEMPERATURE_SCORING_WEIGHT: (0.5, 2.0)
- [ ] Add WIND parameters to PARAM_DEFINITIONS:
  - WIND_IMPACT_SCALE: (40.0, 100.0)
  - WIND_SCORING_WEIGHT: (0.5, 2.0)
- [ ] Add LOCATION parameters to PARAM_DEFINITIONS:
  - LOCATION_HOME: (0, 5)
  - LOCATION_AWAY: (-5, 0)
  - LOCATION_INTERNATIONAL: (-10, -2)
- [ ] Update PARAMETER_ORDER list
- [ ] Update THRESHOLD_FIXED_PARAMS for new scoring types
- [ ] Update generate_all_parameter_value_sets()
- [ ] Update _extract_combination_from_config()
- [ ] Update create_config_dict()

### 4.4 Update DraftHelperTeam
**File**: `simulation/DraftHelperTeam.py`

- [ ] Ensure GameDataManager is passed to PlayerManager
- [ ] StarterHelperModeManager (used by DraftHelperTeam) will inherit game condition scoring
- [ ] Weekly lineup optimization must use game conditions

### 4.5 Phase 4 Validation
- [ ] Run all unit tests: `python tests/run_all_tests.py`
- [ ] Verify simulation can generate configs with new parameters
- [ ] Run small simulation to verify no crashes
- [ ] Verify game conditions affect weekly scores in simulation

---

## Phase 5: Testing

### 5.1 Create Unit Tests for UpcomingGame
**New File**: `tests/league_helper/util/test_game_data_models.py`

- [ ] Test UpcomingGame dataclass creation
- [ ] Test is_home_game() with home team
- [ ] Test is_home_game() with away team
- [ ] Test is_international() with USA game
- [ ] Test is_international() with England game
- [ ] Test is_international() with Germany game
- [ ] Test is_international() with Brazil game

### 5.2 Create Unit Tests for GameDataManager
**New File**: `tests/league_helper/util/test_GameDataManager.py`

- [ ] Test initialization with valid game_data.csv
- [ ] Test initialization with missing game_data.csv (graceful handling)
- [ ] Test get_game() returns correct game for home team
- [ ] Test get_game() returns correct game for away team
- [ ] Test get_game() returns None for bye week team
- [ ] Test get_game() returns None for unknown team
- [ ] Test current week filtering (only loads current week)
- [ ] Test indoor game detection (temperature/wind are None)
- [ ] Test international game detection

### 5.3 Create Unit Tests for ConfigManager New Methods
**File**: `tests/league_helper/util/test_ConfigManager.py` (add to existing)

- [ ] Test get_temperature_score() with various temperatures
- [ ] Test get_temperature_multiplier() thresholds
- [ ] Test get_wind_multiplier() thresholds
- [ ] Test get_location_modifier() for home game
- [ ] Test get_location_modifier() for away game
- [ ] Test get_location_modifier() for international game
- [ ] Test get_location_modifier() for neutral site USA
- [ ] Test backwards compatibility (config without new params)

### 5.4 Create Unit Tests for PlayerScoringCalculator New Methods
**File**: `tests/league_helper/util/test_player_scoring.py` (add to existing)

- [ ] Test _apply_temperature_scoring() with outdoor game (all positions)
- [ ] Test _apply_temperature_scoring() with indoor game (skipped)
- [ ] Test _apply_temperature_scoring() with bye week (skipped)
- [ ] Test _apply_wind_scoring() with QB (applied)
- [ ] Test _apply_wind_scoring() with WR (applied)
- [ ] Test _apply_wind_scoring() with K (applied)
- [ ] Test _apply_wind_scoring() with RB (skipped - not wind-affected position)
- [ ] Test _apply_wind_scoring() with TE (skipped - not wind-affected position)
- [ ] Test _apply_wind_scoring() with DST (skipped - not wind-affected position)
- [ ] Test _apply_wind_scoring() with indoor game (skipped)
- [ ] Test _apply_wind_scoring() with bye week (skipped)
- [ ] Test _apply_location_modifier() with home game
- [ ] Test _apply_location_modifier() with away game
- [ ] Test _apply_location_modifier() with international game
- [ ] Test _apply_location_modifier() with bye week (skipped)
- [ ] Test score_player() with all new flags enabled

### 5.5 Update Integration Tests
**File**: `tests/integration/test_league_helper_integration.py` (add to existing)

- [ ] Test full scoring flow with game conditions
- [ ] Test StarterHelperMode with game conditions enabled

### 5.6 Phase 5 Validation
- [ ] Run ALL unit tests: `python tests/run_all_tests.py`
- [ ] Verify 100% pass rate
- [ ] All new tests pass

---

## Phase 6: Documentation

### 6.1 Create New Documentation Files
**Directory**: `docs/scoring/`

- [ ] Create `11_temperature_scoring.md`
- [ ] Create `12_wind_scoring.md`
- [ ] Create `13_location_modifier.md`

### 6.2 Update Existing Documentation
**Files**:
- [ ] Update `docs/scoring/README.md` with Steps 11-13
- [ ] Update `README.md` if user-facing features changed
- [ ] Update `CLAUDE.md` with new module references
- [ ] Update `ARCHITECTURE.md` with GameDataManager

### 6.3 Phase 6 Validation
- [ ] All documentation accurate and complete
- [ ] Run final test suite: `python tests/run_all_tests.py`

---

## Phase 7: Final Verification

### 7.1 Requirement Verification Protocol
- [ ] Re-read `updates/new_scoring_parameters.txt`
- [ ] Re-read `docs/research/game_conditions_scoring_implementation.md`
- [ ] Verify ALL requirements implemented
- [ ] Mark each requirement as DONE or MISSING

### 7.2 Final Testing
- [ ] Run complete test suite: `python tests/run_all_tests.py`
- [ ] Manual test League Helper with Starter Helper mode
- [ ] Verify game conditions affect player scores correctly

### 7.3 Cleanup
- [ ] Move `updates/new_scoring_parameters.txt` to `updates/done/`
- [ ] Delete questions file (if created)
- [ ] Create/finalize code changes documentation

---

## Verification Summary

### First Verification Round (Iterations 1-5)
- Iterations completed: 5/5
- Requirements added after draft:
  - Phase 3.4 now specifies exact location in StarterHelperModeManager where flags need adding
  - PlayerManager.score_player() must also be updated (wrapper method)
  - Simulation's DraftHelperTeam uses StarterHelperModeManager which will inherit the changes
- Key patterns identified:
  - `_get_multiplier()` at ConfigManager.py:922 with `rising_thresholds` parameter
  - DECREASING direction formula: E=base+1s, G=base+2s, P=base+3s, VP=base+4s
  - Additive scoring: `bonus = (IMPACT_SCALE * multiplier) - IMPACT_SCALE` (player_scoring.py:527-558)
  - PlayerScoringCalculator initialized at PlayerManager.py:114-121
- Risk areas:
  - GameDataManager needs to be passed through: LeagueHelperManager → PlayerManager → PlayerScoringCalculator
  - Simulation also needs GameDataManager for weekly scoring
  - game_data.csv has empty cells for indoor games (not "None", just empty)
- Questions identified: See `updates/new_scoring_parameters_questions.md`
- Skeptical re-verification corrections: None needed, all file paths and patterns verified

### Second Verification Round (Iterations 6-12)
- Iterations completed: 7/7
- Question answers integrated:
  - Q1: Option 1 - GameDataManager added to constructor (LeagueHelperManager → PlayerManager → PlayerScoringCalculator)
  - Q2: Option 1 - Full simulation integration (simulation uses game conditions for weekly scoring)
  - Q3: Option 1 - All disabled by default (temperature=False, wind=False, location=False)
  - Q4: Custom - Wind ONLY affects QB, WR, K; Temperature affects ALL positions
  - Q5: Option 1 - get_location_modifier() in ConfigManager
  - Q6: Option 1 - Two separate test files
  - Q7: Option 1 - Silent defaults for backwards compatibility
- Confidence level: HIGH
- Key findings from second round:
  - DraftHelperTeam.set_weekly_lineup() creates StarterHelperModeManager per-week (lines 181-185)
  - Simulation game_data.csv has 272 games covering weeks 1-18 (2024 season)
  - WIND_AFFECTED_POSITIONS constant needed in constants.py
  - PlayerManager.score_player() wrapper at line 558 needs signature update
  - create_starting_recommendation() at StarterHelperModeManager lines 365-376 is exact update location

---

## Notes

### Key Files
- `league_helper/util/ConfigManager.py` - Configuration management
- `league_helper/util/player_scoring.py` - 10-step (soon 13-step) scoring algorithm
- `league_helper/LeagueHelperManager.py` - Main orchestrator
- `simulation/ConfigGenerator.py` - Parameter optimization
- `data/game_data.csv` - Game condition data

### Dependencies
- FantasyPlayer has `team` attribute for game matching
- TeamDataManager handles team rankings
- SeasonScheduleManager handles schedules and bye weeks

### Important Patterns
1. ConfigManager uses `_get_multiplier()` with `rising_thresholds` parameter
2. Additive bonuses use formula: `bonus = (IMPACT_SCALE * multiplier) - IMPACT_SCALE`
3. Scoring methods return `Tuple[float, str]` (new_score, reason)
4. New scoring parameters are OPTIONAL in config for backwards compatibility

### Risks
- ConfigManager threshold calculation with DECREASING direction
- Simulation integration may require GameDataManager to work with historical data
- Indoor/outdoor detection depends on game_data.csv data quality
