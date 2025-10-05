# CONSISTENCY/VOLATILITY SCORING IMPLEMENTATION TODO

**Objective**: Implement consistency/volatility analysis across all fantasy helper modes (Draft Helper and Starter Helper) to differentiate between reliable weekly performers and boom/bust players.

**Scope**: 4 modes total
- Draft Helper: Add to Roster, Waiver Optimizer, Trade Simulator
- Starter Helper: Weekly Lineup Optimization

**Source**: `/potential_updates/consistency_volatility_scoring.txt`

**Progress Tracking**: Update checkboxes as tasks are completed. Keep this file current so any Claude agent can resume work.

---

## PHASE 1: CONSISTENCY CALCULATOR FOUNDATION

### 1.1 Create ConsistencyCalculator Class
- [ ] **1.1.1**: Create `shared_files/consistency_calculator.py`
  - [ ] Implement `ConsistencyCalculator` class with `__init__(logger=None)`
  - [ ] Implement `calculate_consistency_score(player: FantasyPlayer) -> Dict[str, Any]` method
    - ⚠️ CRITICAL: Only use weeks < CURRENT_NFL_WEEK (not weeks 1-17, only past weeks)
    - Extract weekly projections for weeks that have occurred
    - Filter out None values (missing weeks)
    - Calculate mean_points, std_dev, coefficient_of_variation (CV)
    - Categorize volatility: LOW (CV < 0.3), MEDIUM (0.3-0.6), HIGH (CV > 0.6)
    - Return dict with: mean_points, std_dev, coefficient_of_variation, volatility_category
  - [ ] Handle edge cases:
    - All weeks same points (CV = 0, should be LOW)
    - Missing weeks (filter out None values)
    - Insufficient data (< 3 weeks): return MEDIUM category (add MINIMUM_WEEKS_FOR_CONSISTENCY = 3 config)
    - Zero mean points (avoid division by zero, return MEDIUM)
    - Very high variance (CV > 1.0, categorize as HIGH)
  - [ ] Add module docstring explaining CV calculation and volatility categories

- [ ] **1.1.2**: Create unit tests `shared_files/tests/test_consistency_calculator.py`
  - [ ] Test CV calculation with known data (verify math)
  - [ ] Test volatility categorization (LOW/MEDIUM/HIGH thresholds)
  - [ ] Test edge case: all weeks same points (CV = 0)
  - [ ] Test edge case: missing weeks (None values filtered)
  - [ ] Test edge case: single week of data
  - [ ] Test edge case: zero mean points (division by zero)
  - [ ] Test edge case: very high variance (CV > 1.0)
  - [ ] Verify all tests pass: `python -m pytest shared_files/tests/test_consistency_calculator.py -v`

- [ ] **1.1.3**: Validate Phase 1.1 (MANDATORY - DO NOT SKIP)
  - [ ] **STOP**: Ensure codebase is in testable, functional state
  - [ ] Run: `python run_pre_commit_validation.py`
  - [ ] Verify exit code 0 (all validations pass)
  - [ ] **If exit code is 1 (failures)**:
    - STOP immediately
    - Fix all failing tests/issues
    - Re-run `python run_pre_commit_validation.py`
    - Do NOT proceed until exit code is 0
  - [ ] **Only after exit code 0**: Commit changes
  - [ ] Commit message: "Complete Phase 1.1: Add ConsistencyCalculator class with unit tests"
  - [ ] **Checkpoint**: Codebase is now in validated state, safe to proceed to Phase 2

---

## PHASE 2: CONFIGURATION SETUP

### 2.1 Add Consistency Configuration
- [ ] **2.1.1**: Update `shared_files/configs/draft_helper_config.py`
  - [ ] Add `ENABLE_CONSISTENCY_SCORING = True` toggle
  - [ ] Add universal consistency multipliers:
    ```python
    CONSISTENCY_MULTIPLIERS = {
        'LOW': 1.08,      # CV < 0.3 (consistent)
        'MEDIUM': 1.00,   # 0.3 <= CV <= 0.6 (moderate)
        'HIGH': 0.92      # CV > 0.6 (volatile)
    }
    ```
  - [ ] Add CV thresholds:
    ```python
    CONSISTENCY_CV_LOW_THRESHOLD = 0.3    # Below this = LOW volatility
    CONSISTENCY_CV_HIGH_THRESHOLD = 0.6   # Above this = HIGH volatility
    ```
  - [ ] Add `CONSISTENCY_WEIGHT = 1.0` tuning parameter (optional, for future use)
  - [ ] Add `MINIMUM_WEEKS_FOR_CONSISTENCY = 3` (minimum weeks required for CV calculation)
  - [ ] Add docstring explaining consistency scoring configuration
  - [ ] Note: Only weeks < CURRENT_NFL_WEEK are used for ALL players

- [ ] **2.1.2**: Validate Phase 2.1 (MANDATORY - DO NOT SKIP)
  - [ ] **STOP**: Ensure codebase is in testable, functional state
  - [ ] Run: `python run_pre_commit_validation.py`
  - [ ] Verify configuration loads without errors
  - [ ] Verify exit code 0 (all validations pass)
  - [ ] **If exit code is 1 (failures)**:
    - STOP immediately
    - Fix all failing tests/issues (likely config validation errors)
    - Re-run `python run_pre_commit_validation.py`
    - Do NOT proceed until exit code is 0
  - [ ] **Only after exit code 0**: Commit changes
  - [ ] Commit message: "Complete Phase 2.1: Add consistency scoring configuration"
  - [ ] **Checkpoint**: Codebase is now in validated state, safe to proceed to Phase 3

---

## PHASE 3: DRAFT HELPER INTEGRATION

### 3.1 Initialize Consistency Calculator in Draft Helper
- [ ] **3.1.1**: Update `draft_helper/draft_helper.py` `__init__` method
  - [ ] Add after existing calculator initializations:
    ```python
    # Initialize consistency calculator
    try:
        from shared_files.consistency_calculator import ConsistencyCalculator
        self.consistency_calculator = ConsistencyCalculator(logger=self.logger)
        self.logger.info("Consistency calculator initialized")
    except Exception as e:
        self.logger.warning(f"Failed to initialize consistency calculator: {e}")
        self.consistency_calculator = None
    ```
  - [ ] Verify placement after `self.positional_ranking_calculator` initialization

- [ ] **3.1.2**: Update `score_player()` method in `draft_helper.py`
  - [ ] Add `consistency_calculator` parameter to scoring_engine call:
    ```python
    def score_player(self, p):
        return self.scoring_engine.score_player(
            p,
            enhanced_scorer=self.enhanced_scorer,
            team_data_loader=self.team_data_loader,
            positional_ranking_calculator=self.positional_ranking_calculator,
            consistency_calculator=self.consistency_calculator  # ← ADD THIS
        )
    ```

- [ ] **3.1.3**: Update `score_player_for_trade()` method in `draft_helper.py`
  - [ ] Add `consistency_calculator` parameter to scoring_engine call:
    ```python
    def score_player_for_trade(self, player):
        return self.scoring_engine.score_player_for_trade(
            player,
            positional_ranking_calculator=self.positional_ranking_calculator,
            enhanced_scorer=self.enhanced_scorer,
            team_data_loader=self.team_data_loader,
            consistency_calculator=self.consistency_calculator  # ← ADD THIS
        )
    ```

- [ ] **3.1.4**: Validate Phase 3.1 (MANDATORY - DO NOT SKIP)
  - [ ] **STOP**: Ensure codebase is in testable, functional state
  - [ ] Run: `python run_pre_commit_validation.py`
  - [ ] Verify Draft Helper starts without errors
  - [ ] Verify exit code 0 (all validations pass)
  - [ ] **If exit code is 1 (failures)**:
    - STOP immediately
    - Check for import errors, initialization errors
    - Fix all failing tests/issues
    - Re-run `python run_pre_commit_validation.py`
    - Do NOT proceed until exit code is 0
  - [ ] **Only after exit code 0**: Commit changes
  - [ ] Commit message: "Complete Phase 3.1: Initialize consistency calculator in Draft Helper"
  - [ ] **Checkpoint**: Draft Helper now has consistency calculator, validated and functional

### 3.2 Update score_player() in Scoring Engine (Add to Roster Mode)
- [ ] **3.2.1**: Update `draft_helper/core/scoring_engine.py` `score_player()` method
  - [ ] Add `consistency_calculator=None` parameter to method signature
  - [ ] After step 4 (enhanced scoring), add step 5 (consistency):
    ```python
    # STEP 5: Apply CONSISTENCY multiplier (universal across positions)
    if consistency_calculator:
        consistency_result = consistency_calculator.calculate_consistency_score(p)
        volatility_category = consistency_result['volatility_category']

        # Get universal multiplier (same for all positions)
        from shared_files.configs.draft_helper_config import CONSISTENCY_MULTIPLIERS
        consistency_multiplier = CONSISTENCY_MULTIPLIERS.get(volatility_category, 1.0)

        consistency_score = enhanced_score * consistency_multiplier
        self.logger.debug(
            f"Step 5 - After consistency for {p.name}: {consistency_score:.2f} "
            f"({volatility_category} volatility, CV={consistency_result['coefficient_of_variation']:.3f}, "
            f"{consistency_multiplier:.2f}x)"
        )
    else:
        consistency_score = enhanced_score
    ```
  - [ ] Renumber subsequent steps: DRAFT_ORDER becomes step 6, bye penalty becomes step 7, injury penalty becomes step 8
  - [ ] Update method docstring to reflect 8-step scoring system

- [ ] **3.2.2**: Update display logic to show volatility category
  - [ ] Find where player recommendations are displayed in Draft Helper
  - [ ] Add volatility category display: `[LOW volatility]`, `[MEDIUM volatility]`, `[HIGH volatility]`
  - [ ] Format example: `1. Kareem Hunt (RB, CLE) - Score: 94.05 [LOW volatility]`
  - [ ] Apply to: Add to Roster recommendations, Waiver Optimizer, Trade Simulator

- [ ] **3.2.3**: Create integration tests `draft_helper/tests/test_scoring_engine_consistency.py`
  - [ ] Test `score_player()` with consistency_calculator (Add to Roster mode)
  - [ ] Verify consistent player (CV < 0.3) scores higher than volatile (CV > 0.6)
  - [ ] Test with/without consistency_calculator parameter (graceful degradation)
  - [ ] Test universal application across positions (QB, RB, WR, TE, K, DST)
  - [ ] Test insufficient weeks (< 3) defaults to MEDIUM category
  - [ ] Verify all tests pass: `python -m pytest draft_helper/tests/test_scoring_engine_consistency.py -v`

- [ ] **3.2.4**: Validate Phase 3.2 (MANDATORY - DO NOT SKIP)
  - [ ] **STOP**: Ensure codebase is in testable, functional state
  - [ ] Run: `python run_pre_commit_validation.py`
  - [ ] Manually test Add to Roster mode shows consistency-adjusted recommendations
  - [ ] Verify volatility category displays correctly: `[LOW volatility]`, etc.
  - [ ] Verify exit code 0 (all validations pass)
  - [ ] **If exit code is 1 (failures)**:
    - STOP immediately
    - Fix all failing tests (scoring engine, integration tests, etc.)
    - Re-run `python run_pre_commit_validation.py`
    - Do NOT proceed until exit code is 0
  - [ ] **Only after exit code 0**: Commit changes
  - [ ] Commit message: "Complete Phase 3.2: Add consistency scoring to score_player (Add to Roster)"
  - [ ] **Checkpoint**: Add to Roster mode now uses consistency scoring, fully validated

### 3.3 Update score_player_for_trade() in Scoring Engine (Waiver/Trade Modes)
- [ ] **3.3.1**: Update `draft_helper/core/scoring_engine.py` `score_player_for_trade()` method
  - [ ] Add `consistency_calculator=None` parameter to method signature
  - [ ] After step 4 (enhanced scoring), add step 5 (consistency):
    ```python
    # STEP 5: Apply CONSISTENCY multiplier (universal, same as Add to Roster)
    if consistency_calculator:
        consistency_result = consistency_calculator.calculate_consistency_score(player)
        volatility_category = consistency_result['volatility_category']

        # Get universal multiplier (same for all positions)
        from shared_files.configs.draft_helper_config import CONSISTENCY_MULTIPLIERS
        consistency_multiplier = CONSISTENCY_MULTIPLIERS.get(volatility_category, 1.0)

        consistency_score = enhanced_score * consistency_multiplier
        self.logger.debug(
            f"Step 5 - After consistency for {player.name}: {consistency_score:.2f} "
            f"({volatility_category} volatility, CV={consistency_result['coefficient_of_variation']:.3f}, "
            f"{consistency_multiplier:.2f}x)"
        )
    else:
        consistency_score = enhanced_score
    ```
  - [ ] Renumber subsequent steps: bye penalty becomes step 6, injury penalty becomes step 7
  - [ ] Update method docstring to reflect 7-step scoring system
  - [ ] NOTE: No DRAFT_ORDER bonus in this method (trade/waiver mode)

- [ ] **3.3.2**: Update display logic for Waiver/Trade modes (if different from 3.2.2)
  - [ ] Verify volatility category shows in Waiver Optimizer player listings
  - [ ] Verify volatility category shows in Trade Simulator player listings
  - [ ] Use same format: `[LOW volatility]`, `[MEDIUM volatility]`, `[HIGH volatility]`

- [ ] **3.3.3**: Update integration tests in `test_scoring_engine_consistency.py`
  - [ ] Test `score_player_for_trade()` with consistency_calculator (Waiver/Trade mode)
  - [ ] Verify both methods apply same consistency multipliers
  - [ ] Verify consistent player scores higher in trade mode
  - [ ] Test with/without consistency_calculator parameter
  - [ ] Verify all tests pass: `python -m pytest draft_helper/tests/test_scoring_engine_consistency.py -v`

- [ ] **3.3.4**: Validate Phase 3.3 (MANDATORY - DO NOT SKIP)
  - [ ] **STOP**: Ensure codebase is in testable, functional state
  - [ ] Run: `python run_pre_commit_validation.py`
  - [ ] Manually test Waiver Optimizer mode applies consistency to recommendations
  - [ ] Manually test Trade Simulator mode uses consistency in score comparisons
  - [ ] Verify volatility category displays in both modes
  - [ ] Verify exit code 0 (all validations pass)
  - [ ] **If exit code is 1 (failures)**:
    - STOP immediately
    - Fix all failing tests
    - Re-run `python run_pre_commit_validation.py`
    - Do NOT proceed until exit code is 0
  - [ ] **Only after exit code 0**: Commit changes
  - [ ] Commit message: "Complete Phase 3.3: Add consistency scoring to score_player_for_trade (Waiver/Trade)"
  - [ ] **Checkpoint**: Draft Helper fully integrated with consistency, all 3 modes validated

---

## PHASE 4: STARTER HELPER INTEGRATION

### 4.1 Initialize Consistency Calculator in Starter Helper
- [ ] **4.1.1**: Update `starter_helper/lineup_optimizer.py` `__init__` method
  - [ ] Add after matchup calculator initialization:
    ```python
    # Initialize consistency calculator
    try:
        from shared_files.consistency_calculator import ConsistencyCalculator
        self.consistency_calculator = ConsistencyCalculator(logger=self.logger)
        self.logger.info("Consistency calculator initialized")
    except Exception as e:
        self.logger.warning(f"Failed to initialize consistency calculator: {e}")
        self.consistency_calculator = None
    ```

- [ ] **4.1.2**: Validate Phase 4.1 (MANDATORY - DO NOT SKIP)
  - [ ] **STOP**: Ensure codebase is in testable, functional state
  - [ ] Run: `python run_pre_commit_validation.py`
  - [ ] Verify Starter Helper starts without errors
  - [ ] Verify exit code 0 (all validations pass)
  - [ ] **If exit code is 1 (failures)**:
    - STOP immediately
    - Check for import/initialization errors in Starter Helper
    - Fix all failing tests/issues
    - Re-run `python run_pre_commit_validation.py`
    - Do NOT proceed until exit code is 0
  - [ ] **Only after exit code 0**: Commit changes
  - [ ] Commit message: "Complete Phase 4.1: Initialize consistency calculator in Starter Helper"
  - [ ] **Checkpoint**: Starter Helper has consistency calculator, validated and functional

### 4.2 Update calculate_adjusted_score() Method
- [ ] **4.2.1**: Update `starter_helper/lineup_optimizer.py` `calculate_adjusted_score()` method
  - [ ] Add `player: Optional[FantasyPlayer] = None` parameter to method signature
  - [ ] Add `consistency_calculator=None` parameter to method signature
  - [ ] After step 1 (base projected_points), add step 2 (consistency):
    ```python
    # STEP 2: Apply CONSISTENCY multiplier (universal, same as Draft Helper)
    if consistency_calculator and player:
        consistency_result = consistency_calculator.calculate_consistency_score(player)
        volatility_category = consistency_result['volatility_category']

        # Get universal multiplier (same for all positions)
        from shared_files.configs.draft_helper_config import CONSISTENCY_MULTIPLIERS
        consistency_multiplier = CONSISTENCY_MULTIPLIERS.get(volatility_category, 1.0)

        adjusted_score = adjusted_score * consistency_multiplier

        # Add to reasons if adjustment applied
        if consistency_multiplier != 1.0:
            cv = consistency_result['coefficient_of_variation']
            reasons.append(f"Consistency: {consistency_multiplier:.2f}x (CV={cv:.3f})")
    ```
  - [ ] Renumber subsequent steps: matchup becomes step 3, injury becomes step 4
  - [ ] Update method docstring to reflect 4-step scoring system
  - [ ] ⚠️ CRITICAL: Consistency applied BEFORE matchup and BEFORE injury

- [ ] **4.2.2**: Update display logic for Starter Helper
  - [ ] Verify volatility category appears in starter lineup display
  - [ ] Use same format as Draft Helper: `[LOW volatility]`, `[MEDIUM volatility]`, `[HIGH volatility]`
  - [ ] Should appear alongside reason string in player display

- [ ] **4.2.3**: Validate Phase 4.2 (MANDATORY - DO NOT SKIP)
  - [ ] **STOP**: Ensure codebase is in testable, functional state
  - [ ] Run: `python run_pre_commit_validation.py`
  - [ ] Verify exit code 0 (all validations pass)
  - [ ] **If exit code is 1 (failures)**:
    - STOP immediately
    - Check calculate_adjusted_score integration
    - Fix all failing tests
    - Re-run `python run_pre_commit_validation.py`
    - Do NOT proceed until exit code is 0
  - [ ] **Only after exit code 0**: Commit changes
  - [ ] Commit message: "Complete Phase 4.2: Update calculate_adjusted_score with consistency step"
  - [ ] **Checkpoint**: Starter Helper scoring method updated, validated

### 4.3 Update create_starting_recommendation() Method
- [ ] **4.3.1**: Update `starter_helper/lineup_optimizer.py` `create_starting_recommendation()` method
  - [ ] ⚠️ NOTE: User confirmed existing infrastructure handles FantasyPlayer objects
  - [ ] Verify player_data is already a FantasyPlayer object (or can be easily converted)
  - [ ] Update `calculate_adjusted_score()` call to pass new parameters:
    ```python
    adjusted_score, reason = self.calculate_adjusted_score(
        projected_points, injury_status, bye_week,
        player_team=player_data['team'],
        player_position=player_data['position'],
        player=player,  # ← ADD THIS
        consistency_calculator=self.consistency_calculator  # ← ADD THIS
    )
    ```

- [ ] **4.3.2**: Create integration tests `starter_helper/tests/test_lineup_optimizer_consistency.py`
  - [ ] Test `calculate_adjusted_score()` with consistency_calculator
  - [ ] Verify consistent player scores higher than volatile player
  - [ ] Verify consistency applied BEFORE matchup multiplier
  - [ ] Verify consistency doesn't interfere with injury zeroing (applied BEFORE injury check)
  - [ ] Test with/without consistency_calculator parameter (graceful degradation)
  - [ ] Verify all tests pass: `python -m pytest starter_helper/tests/test_lineup_optimizer_consistency.py -v`

- [ ] **4.3.3**: Validate Phase 4.3 (MANDATORY - DO NOT SKIP)
  - [ ] **STOP**: Ensure codebase is in testable, functional state
  - [ ] Run: `python run_pre_commit_validation.py`
  - [ ] Manually test Weekly Lineup Optimization mode uses consistency in starter picks
  - [ ] Verify volatility category displays correctly
  - [ ] Verify exit code 0 (all validations pass)
  - [ ] **If exit code is 1 (failures)**:
    - STOP immediately
    - Fix all failing tests
    - Re-run `python run_pre_commit_validation.py`
    - Do NOT proceed until exit code is 0
  - [ ] **Only after exit code 0**: Commit changes
  - [ ] Commit message: "Complete Phase 4.3: Integrate consistency into create_starting_recommendation"
  - [ ] **Checkpoint**: Starter Helper fully integrated, all 4 modes now have consistency scoring

---

## PHASE 5: SIMULATION INTEGRATION

### 5.1 Add Consistency Parameters to Simulation Config
- [ ] **5.1.1**: Update `shared_files/configs/simulation_config.py`
  - [ ] Add consistency parameters to `FINE_GRAIN_OFFSETS`:
    ```python
    'CONSISTENCY_LOW_MULTIPLIER': [-0.05, -0.02, 0, 0.02, 0.05],
    'CONSISTENCY_HIGH_MULTIPLIER': [-0.05, -0.02, 0, 0.02, 0.05],
    'CONSISTENCY_CV_LOW_THRESHOLD': [-0.05, -0.02, 0, 0.02, 0.05],
    'CONSISTENCY_CV_HIGH_THRESHOLD': [-0.05, -0.02, 0, 0.02, 0.05],
    ```
  - [ ] Add to `FINE_GRAIN_BOUNDS`:
    ```python
    'CONSISTENCY_LOW_MULTIPLIER': (1.0, 1.15),
    'CONSISTENCY_HIGH_MULTIPLIER': (0.85, 1.0),
    'CONSISTENCY_CV_LOW_THRESHOLD': (0.2, 0.4),
    'CONSISTENCY_CV_HIGH_THRESHOLD': (0.5, 0.7),
    ```

- [ ] **5.1.2**: Create baseline parameter JSON file
  - [ ] Create `draft_helper/simulation/parameters/consistency_baseline.json`:
    ```json
    {
        "CONSISTENCY_LOW_MULTIPLIER": [1.05, 1.08],
        "CONSISTENCY_HIGH_MULTIPLIER": [0.92, 0.95],
        "CONSISTENCY_CV_LOW_THRESHOLD": [0.25, 0.30],
        "CONSISTENCY_CV_HIGH_THRESHOLD": [0.55, 0.60]
    }
    ```

- [ ] **5.1.3**: Validate Phase 5.1 (MANDATORY - DO NOT SKIP)
  - [ ] **STOP**: Ensure codebase is in testable, functional state
  - [ ] Run: `python run_pre_commit_validation.py`
  - [ ] Verify simulation config loads without errors
  - [ ] Verify exit code 0 (all validations pass)
  - [ ] **If exit code is 1 (failures)**:
    - STOP immediately
    - Check simulation config validation
    - Fix all failing tests/issues
    - Re-run `python run_pre_commit_validation.py`
    - Do NOT proceed until exit code is 0
  - [ ] **Only after exit code 0**: Commit changes
  - [ ] Commit message: "Complete Phase 5.1: Add consistency parameters to simulation config"
  - [ ] **Checkpoint**: Simulation config ready for testing, validated

---

## PHASE 6: DOCUMENTATION UPDATES

### 6.1 Update CLAUDE.md
- [ ] **6.1.1**: Update Draft Helper scoring section
  - [ ] Update "Add to Roster (7 steps)" to "Add to Roster (8 steps)"
  - [ ] Add step 5: "Apply CONSISTENCY multiplier"
  - [ ] Update "Trade/Waiver (6 steps)" to "Trade/Waiver (7 steps)"
  - [ ] Add step 5: "Apply CONSISTENCY multiplier (same as Add to Roster)"
  - [ ] Add note: "Consistency scoring applies universally across all positions"

- [ ] **6.1.2**: Update Starter Helper scoring section
  - [ ] Update "Starter Helper (3 steps)" to "Starter Helper (4 steps)"
  - [ ] Add step 2: "Apply CONSISTENCY multiplier"
  - [ ] Add note: "Consistency applied BEFORE matchup and BEFORE injury check"

- [ ] **6.1.3**: Add Consistency Scoring subsection
  - [ ] Add section under "## Scoring Systems"
  - [ ] Explain CV (coefficient of variation) calculation
  - [ ] Document volatility categories: LOW (CV < 0.3), MEDIUM (0.3-0.6), HIGH (CV > 0.6)
  - [ ] Document universal multipliers: LOW (1.08x), MEDIUM (1.00x), HIGH (0.92x)
  - [ ] Note that all 4 modes use consistency: Add to Roster, Waiver Optimizer, Trade Simulator, Weekly Lineup

- [ ] **6.1.4**: Update configuration section
  - [ ] Add `CONSISTENCY_MULTIPLIERS` to draft_helper_config documentation
  - [ ] Add `CONSISTENCY_CV_LOW_THRESHOLD` and `CONSISTENCY_CV_HIGH_THRESHOLD`
  - [ ] Add `ENABLE_CONSISTENCY_SCORING` toggle

- [ ] **6.1.5**: Validate Phase 6.1 (MANDATORY - DO NOT SKIP)
  - [ ] **STOP**: Ensure codebase is in testable, functional state
  - [ ] Verify CLAUDE.md is accurate and complete
  - [ ] Run: `python run_pre_commit_validation.py`
  - [ ] Verify exit code 0 (all validations pass)
  - [ ] **If exit code is 1 (failures)**:
    - STOP immediately
    - Fix all failing tests/issues
    - Re-run `python run_pre_commit_validation.py`
    - Do NOT proceed until exit code is 0
  - [ ] **Only after exit code 0**: Commit changes
  - [ ] Commit message: "Complete Phase 6.1: Update CLAUDE.md with consistency scoring documentation"
  - [ ] **Checkpoint**: Documentation updated, validated

### 6.2 Update Module README Files
- [ ] **6.2.1**: Update `shared_files/README.md` (if exists)
  - [ ] Add ConsistencyCalculator class documentation
  - [ ] Explain CV calculation and usage

- [ ] **6.2.2**: Update `draft_helper/README.md` (if exists)
  - [ ] Document consistency scoring integration
  - [ ] Note 8-step Add to Roster and 7-step Waiver/Trade scoring

- [ ] **6.2.3**: Update `starter_helper/README.md` (if exists)
  - [ ] Document consistency scoring integration
  - [ ] Note 4-step Weekly Lineup scoring

- [ ] **6.2.4**: Validate Phase 6.2 (MANDATORY - DO NOT SKIP)
  - [ ] **STOP**: Ensure codebase is in testable, functional state
  - [ ] Verify all README files are accurate
  - [ ] Run: `python run_pre_commit_validation.py`
  - [ ] Verify exit code 0 (all validations pass)
  - [ ] **If exit code is 1 (failures)**:
    - STOP immediately
    - Fix all failing tests/issues
    - Re-run `python run_pre_commit_validation.py`
    - Do NOT proceed until exit code is 0
  - [ ] **Only after exit code 0**: Commit changes
  - [ ] Commit message: "Complete Phase 6.2: Update module README files"
  - [ ] **Checkpoint**: All documentation complete, validated

---

## PHASE 7: END-TO-END VALIDATION

### 7.1 Manual Testing - All Four Modes
- [ ] **7.1.1**: Test Add to Roster mode (Draft Helper)
  - [ ] Run Draft Helper, select "Add to Roster"
  - [ ] Add a consistent player (low variance in weekly projections)
  - [ ] Verify player receives consistency boost in score
  - [ ] Check debug logs show consistency multiplier and CV
  - [ ] Document: Player name, CV, multiplier applied, score difference

- [ ] **7.1.2**: Test Waiver Optimizer mode (Draft Helper)
  - [ ] Run Draft Helper, select "Waiver Optimizer"
  - [ ] Verify consistency affects trade recommendations
  - [ ] Check that consistent players rank higher than volatile players with same projections
  - [ ] Verify debug logs show consistency calculations
  - [ ] Document: Trade recommendations, consistency impact

- [ ] **7.1.3**: Test Trade Simulator mode (Draft Helper)
  - [ ] Run Draft Helper, select "Trade Simulator"
  - [ ] Simulate a trade involving consistent vs volatile player
  - [ ] Verify consistency affects score comparisons
  - [ ] Verify roster score reflects consistency adjustments
  - [ ] Document: Trade simulation results, consistency impact

- [ ] **7.1.4**: Test Weekly Lineup Optimization (Starter Helper)
  - [ ] Run Starter Helper
  - [ ] Verify consistency appears in adjusted_score calculations
  - [ ] Check reason strings show "Consistency: X.XXx (CV=X.XXX)"
  - [ ] Verify consistent players rank higher for same projected points
  - [ ] Verify consistency applied BEFORE matchup and BEFORE injury
  - [ ] Document: Lineup selections, consistency impact

- [ ] **7.1.5**: Cross-mode consistency verification
  - [ ] Select same player in all 4 modes
  - [ ] Verify same CV and volatility category across all modes
  - [ ] Verify same multiplier applied across all modes
  - [ ] Document: Player name, CV, category, multiplier consistency

- [ ] **7.1.6**: Validate Phase 7.1 (MANDATORY - DO NOT SKIP)
  - [ ] **STOP**: Ensure codebase is in testable, functional state
  - [ ] Create validation report document: `potential_updates/consistency_validation_report.md`
  - [ ] Include all test results and documentation from 7.1.1-7.1.5
  - [ ] Run: `python run_pre_commit_validation.py`
  - [ ] Verify exit code 0 (all validations pass)
  - [ ] **If exit code is 1 (failures)**:
    - STOP immediately
    - Fix all failing tests/issues
    - Re-run `python run_pre_commit_validation.py`
    - Do NOT proceed until exit code is 0
  - [ ] **Only after exit code 0**: Commit changes
  - [ ] Commit message: "Complete Phase 7.1: End-to-end manual validation of all modes"
  - [ ] **Checkpoint**: Manual validation complete, all modes tested

### 7.2 Final Repository Validation
- [ ] **7.2.1**: Run complete test suite
  - [ ] Execute: `python run_pre_commit_validation.py`
  - [ ] Verify exit code 0 (all validations pass)
  - [ ] Verify 100% test pass rate across all modules
  - [ ] If any failures, fix and re-run

- [ ] **7.2.2**: Startup validation for all scripts
  - [ ] Test: `timeout 10 python run_player_data_fetcher.py`
  - [ ] Test: `timeout 10 python run_nfl_scores_fetcher.py`
  - [ ] Test: `timeout 10 python run_draft_helper.py` (should reach menu)
  - [ ] Test: `timeout 10 python run_starter_helper.py` (should process or prompt)
  - [ ] Verify all start without import/config errors

- [ ] **7.2.3**: Interactive integration tests
  - [ ] Run full draft_helper validation:
    ```bash
    echo -e "2\nHunt\n1\nexit\n3\n\n4\nHunt\n1\nHampton\n1\nexit\n1\n1\n5\n15\n16\n3\n\n5\n15\n16\n6\n\n7\n4\n8\n" | python run_draft_helper.py
    ```
  - [ ] Verify all 23 steps complete successfully
  - [ ] Verify CSV persistence, FLEX system, point calculations
  - [ ] Verify all 7 menu options functional

- [ ] **7.2.4**: Final commit (MANDATORY - DO NOT SKIP)
  - [ ] **STOP**: Ensure codebase is in testable, functional state
  - [ ] Review all changes: `git status`, `git diff`
  - [ ] Ensure no debug/temp files staged
  - [ ] Run: `python run_pre_commit_validation.py` one final time
  - [ ] Verify exit code 0 (all validations pass)
  - [ ] **If exit code is 1 (failures)**:
    - STOP immediately
    - Fix all failing tests/issues
    - Re-run `python run_pre_commit_validation.py`
    - Do NOT proceed until exit code is 0
  - [ ] **Only after exit code 0**: Commit changes
  - [ ] Commit message: "Complete Phase 7.2: Final validation - consistency scoring implementation complete"
  - [ ] **Checkpoint**: Implementation complete and fully validated, ready for simulation testing

---

## PHASE 8: SIMULATION BASELINE TESTING (MANDATORY)

### 8.1 Baseline Simulation - Consistency OFF
- [ ] **8.1.1**: Disable consistency scoring
  - [ ] Set `ENABLE_CONSISTENCY_SCORING = False` in draft_helper_config.py
  - [ ] Create baseline params JSON (or use existing)
  - [ ] Run simulation: `python run_simulation.py [baseline_params.json]`
  - [ ] Record detailed results:
    - Win rate for draft_helper strategy
    - Average points per week
    - Roster composition (consistent vs volatile players)
    - Position distribution
  - [ ] Save results file location

### 8.2 Baseline Simulation - Consistency ON (Conservative)
- [ ] **8.2.1**: Enable consistency with conservative multipliers
  - [ ] Set `ENABLE_CONSISTENCY_SCORING = True` in draft_helper_config.py
  - [ ] Use conservative multipliers: LOW=1.05, MEDIUM=1.00, HIGH=0.95
  - [ ] Create consistency params JSON: `consistency_conservative.json`
  - [ ] Run simulation: `python run_simulation.py consistency_conservative.json`
  - [ ] Record detailed results (same metrics as 8.1.1)

### 8.3 Baseline Simulation - Consistency ON (Moderate)
- [ ] **8.3.1**: Enable consistency with moderate multipliers
  - [ ] Set multipliers: LOW=1.08, MEDIUM=1.00, HIGH=0.92
  - [ ] Create consistency params JSON: `consistency_moderate.json`
  - [ ] Run simulation: `python run_simulation.py consistency_moderate.json`
  - [ ] Record detailed results (same metrics as 8.1.1)

### 8.4 Analysis and Tuning
- [ ] **8.4.1**: Compare all three simulation results
  - [ ] Calculate win rate differences:
    - Conservative vs OFF
    - Moderate vs OFF
    - Conservative vs Moderate
  - [ ] Analyze roster composition changes
  - [ ] Identify optimal multiplier values
  - [ ] Document findings in detailed report

- [ ] **8.4.2**: Create comprehensive validation report
  - [ ] Create `potential_updates/consistency_validation_report.md`
  - [ ] Include all simulation results with tables/charts
  - [ ] Document win rate impacts
  - [ ] Provide multiplier recommendations
  - [ ] Note any unexpected behaviors or edge cases

- [ ] **8.4.3**: Run final validation with optimal settings (MANDATORY - DO NOT SKIP)
  - [ ] **STOP**: Ensure codebase is in testable, functional state
  - [ ] Update config with optimal multiplier values (if different from moderate)
  - [ ] Run: `python run_pre_commit_validation.py`
  - [ ] Verify exit code 0 (all validations pass)
  - [ ] **If exit code is 1 (failures)**:
    - STOP immediately
    - Fix all failing tests/issues
    - Re-run `python run_pre_commit_validation.py`
    - Do NOT proceed until exit code is 0
  - [ ] **Only after exit code 0**: Commit changes
  - [ ] Commit message: "Complete Phase 8: Simulation testing and tuning - consistency scoring validated"
  - [ ] **Checkpoint**: Optimal settings determined, simulation complete, ready for cleanup

---

## PHASE 9: CLEANUP AND COMPLETION

### 9.1 Final Cleanup
- [ ] **9.1.1**: Remove temporary files
  - [ ] Delete any test/debug files created during development
  - [ ] Remove temp checklists: `rm tests/temp_*.md`
  - [ ] Verify no `.pyc` or `__pycache__` files staged

- [ ] **9.1.2**: Final repository state check
  - [ ] Run: `git status` (should be clean or only expected changes)
  - [ ] Run: `python run_pre_commit_validation.py` (final validation)
  - [ ] Verify exit code 0

### 9.2 Move to Done
- [ ] **9.2.1**: Move source file to done folder
  - [ ] `mv potential_updates/consistency_volatility_scoring.txt potential_updates/done/`
  - [ ] Verify file moved successfully

- [ ] **9.2.2**: Archive TODO file
  - [ ] Add completion timestamp to top of this file
  - [ ] Add final summary: total phases, total time, key outcomes
  - [ ] Keep this file in `todo-files/` for reference

- [ ] **9.2.3**: Final commit (MANDATORY - DO NOT SKIP)
  - [ ] **STOP**: Ensure codebase is in final testable, functional state
  - [ ] Run: `python run_pre_commit_validation.py` for absolute final validation
  - [ ] Verify exit code 0 (all validations pass)
  - [ ] **If exit code is 1 (failures)**:
    - STOP immediately
    - Fix all failing tests/issues
    - Re-run `python run_pre_commit_validation.py`
    - Do NOT proceed until exit code is 0
  - [ ] **Only after exit code 0**: Commit changes
  - [ ] Commit message: "Complete consistency/volatility scoring implementation - moved to done"
  - [ ] **🎉 COMPLETE**: Consistency/volatility scoring fully implemented, tested, and validated

---

## SUCCESS CRITERIA

### Required for Completion:
- [x] ConsistencyCalculator class implemented and tested
- [x] Configuration added to draft_helper_config.py
- [x] Draft Helper integration complete (3 methods updated)
- [x] Starter Helper integration complete (2 methods updated)
- [x] All unit tests passing (100% pass rate)
- [x] All integration tests passing
- [x] Manual validation complete for all 4 modes
- [x] Documentation updated (CLAUDE.md, README files)
- [x] Simulation parameters added
- [x] All pre-commit validations passing

### Quality Checks:
- [ ] All 4 modes apply identical consistency logic
- [ ] Same CV and multiplier for same player across all modes
- [ ] Consistency applied at correct step in each scoring method
- [ ] Starter Helper applies consistency BEFORE matchup and injury
- [ ] Graceful degradation when consistency_calculator is None
- [ ] No performance degradation (consistency calculation is fast)

---

## NOTES

**⚠️ CRITICAL REMINDERS:**
1. **MANDATORY VALIDATION AFTER EVERY PHASE**: Run `python run_pre_commit_validation.py` after completing each phase
2. **TESTABLE STATE REQUIREMENT**: Each phase must leave the codebase in a fully testable and functional state
3. **COMMIT BEFORE PROCEEDING**: Only commit and move to next phase if validation passes with exit code 0
4. **NO BROKEN STATES**: If validation fails, fix issues and re-run validation before proceeding
5. Update THREE scoring methods (score_player, score_player_for_trade, calculate_adjusted_score)
6. Test ALL FOUR modes (Add to Roster, Waiver Optimizer, Trade Simulator, Weekly Lineup)
7. Consistency must apply identical logic across all modes
8. Starter Helper: consistency BEFORE matchup BEFORE injury
9. Simulation testing (Phase 8) is MANDATORY - prioritize it, no cut corners

**Key Implementation Decisions (from questions file):**
- ✅ Use existing FantasyPlayer infrastructure - just analyze data in objects
- ✅ Only use weeks < CURRENT_NFL_WEEK for ALL players (not just rookies)
- ✅ Minimum 3 weeks required for CV calculation, default to MEDIUM if insufficient
- ✅ Display format: `[LOW volatility]`, `[MEDIUM volatility]`, `[HIGH volatility]` in ALL modes
- ✅ Show volatility category when listing players with scores (all modes)
- ✅ Simulation testing is NOT optional - must complete Phase 8

**Phase Completion Protocol (MANDATORY FOR EVERY PHASE):**
1. **Complete all tasks** in the phase
2. **Ensure testable state**: Code must be functional, no broken imports/syntax errors
3. **Run validation**: Execute `python run_pre_commit_validation.py`
4. **Check exit code**:
   - Exit code 0 = SUCCESS, proceed to commit
   - Exit code 1 = FAILURE, STOP and fix issues
5. **Fix if needed**: If validation fails, fix ALL issues and re-run validation
6. **Commit only after success**: Only commit when exit code is 0
7. **Move to next phase**: Safe to proceed only after successful commit

**Progress Tracking:**
- Update checkboxes as tasks complete
- Keep notes on any deviations or issues encountered
- Document any new questions in consistency_volatility_scoring_questions.md (if needed)
- **NEVER skip validation**: Every phase must pass pre-commit validation before proceeding

**Estimated Total Time:** 7.5-9.5 hours
- Phase 1: 1.5 hours (calculator + tests)
- Phase 2: 0.5 hours (config)
- Phase 3: 2.5 hours (Draft Helper integration + tests)
- Phase 4: 2 hours (Starter Helper integration + tests)
- Phase 5: 0.5 hours (simulation config)
- Phase 6: 1 hour (documentation)
- Phase 7: 1.5 hours (validation)
- Phase 8: 0.5-2 hours (optional simulation testing)
