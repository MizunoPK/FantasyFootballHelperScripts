# Waiver Streaming Mode - Implementation TODO

**Objective**: Add "Rest of Season" vs "Current Week" mode selection to Waiver Optimizer

**Source**: `updates/waiver_streaming.txt`

**Status**: VERIFIED - 12 complete iterations, ready for implementation

---

## Overview

Add mode selection to Waiver Optimizer (Trade Simulator sub-mode) allowing users to choose between:
- **Rest of Season**: Current behavior (seasonal projections, standard multipliers)
- **Current Week**: New streaming behavior (weekly projections matching Starter Helper exactly)

**Critical Context**: Waiver Optimizer is a sub-mode within Trade Simulator, NOT Reserve Assessment Mode.

**Key Requirement**: "Current Week" mode must use "the same scoring calculation that the Starter Helper uses" (per spec).

---

## User Answers Integration

All 12 questions answered and integrated:

| Question | Answer | Impact |
|----------|--------|--------|
| Q1: Cancellation | Option A (include) | Mode selection allows cancel to menu |
| Q2: team_quality | Yes include | Match Starter Helper exactly (line 370) |
| Q3: Display | Option C (minimal) | Show mode name only, no detailed explanation |
| Q4: Filename | Option A (include mode) | Use `waiver_ros_*.txt` and `waiver_weekly_*.txt` |
| Q5: Threshold | Option A (same) | Same MIN_WAIVER_IMPROVEMENT for both modes |
| Q6: Trade Suggestor | Option A (Waiver only) | No mode selection for Trade Suggestor |
| Q7: Manual Trade | Option A (Waiver only) | No mode selection for Manual Trade |
| Q8: Documentation | Option B (README only) | Update README, no new docs/ files |
| Q9: Backward compat | Yes correct | Default False preserves existing behavior |
| Q10: Test coverage | Option A (standard) | Unit + integration tests |
| Q11: Future modes | Yes flexible | Support future mode additions |
| Q12: README fix | Yes correct | Fix incorrect sub-mode names |

---

## Implementation Plan

### Phase 1: Add Mode Selection to Waiver Optimizer

**File**: `league_helper/trade_simulator_mode/TradeSimulatorModeManager.py`

**Location**: `start_waiver_optimizer()` method (line 235)

**Current Signature** (line 235):
```python
def start_waiver_optimizer(self) -> Tuple[bool, List[TradeSnapshot]]:
```

**Updated Signature**:
```python
def start_waiver_optimizer(self) -> Tuple[bool, List[TradeSnapshot], str]:
```

**Changes at line 242** (before line: `print("\nGetting current team score...")`):

```python
def start_waiver_optimizer(self) -> Tuple[bool, List[TradeSnapshot], str]:
    """
    Find optimal waiver wire pickups with mode selection.

    Prompts user to select between:
    - Rest of Season: Seasonal projections with standard multipliers
    - Current Week: Weekly projections matching Starter Helper scoring

    Returns:
        Tuple[bool, List[TradeSnapshot], str]:
            - bool: True to loop back to menu, False to exit
            - List[TradeSnapshot]: Sorted trade recommendations
            - str: Mode name for file output ("Rest of Season" or "Current Week")
    """
    self.logger.info("Starting Waiver Optimizer mode")

    # STEP 1: Mode selection (Q1: Include cancel option)
    from util.user_input import show_list_selection

    mode_choice = show_list_selection(
        "WAIVER OPTIMIZER - SELECT MODE",
        ["Rest of Season", "Current Week"],
        "Cancel"
    )

    # Handle cancellation (Q1: Option A)
    if mode_choice > 2:  # User selected Cancel
        self.logger.info("User cancelled Waiver Optimizer")
        return True, [], ""

    # Determine mode
    use_weekly_scoring = (mode_choice == 2)
    mode_name = "Current Week" if use_weekly_scoring else "Rest of Season"
    self.logger.info(f"Waiver Optimizer mode selected: {mode_name}")

    # STEP 2: Set max_weekly_projection if using weekly scoring
    if use_weekly_scoring:
        max_weekly = self.player_manager.calculate_max_weekly_projection(
            self.config.current_nfl_week
        )
        self.player_manager.scoring_calculator.max_weekly_projection = max_weekly
        self.logger.info(
            f"Set max_weekly_projection to {max_weekly:.2f} for week {self.config.current_nfl_week}"
        )

    # EXISTING CODE CONTINUES (line 242 onwards)
    print("\nGetting current team score...")
```

**Update at line 259** (TradeSimTeam creation):

```python
# CHANGE FROM:
my_team = self.my_team

# CHANGE TO:
# Re-create my_team with mode-specific scoring
my_team = TradeSimTeam(
    Constants.FANTASY_TEAM_NAME,
    self.player_manager.team.roster,
    self.player_manager,
    isOpponent=False,
    use_weekly_scoring=use_weekly_scoring
)
```

**Update at line 275** (waiver team creation):

```python
# CHANGE FROM:
waiver_team = TradeSimTeam("Waiver Wire", waiver_players, self.player_manager)

# CHANGE TO:
waiver_team = TradeSimTeam(
    "Waiver Wire",
    waiver_players,
    self.player_manager,
    isOpponent=True,
    use_weekly_scoring=use_weekly_scoring
)
```

**Update at line 297** (display header - Q3: Minimal display):

```python
# CHANGE FROM:
print("\n" + "="*80)
print("WAIVER OPTIMIZER RESULTS")
print("="*80)

# CHANGE TO:
print("\n" + "="*80)
print(f"WAIVER OPTIMIZER - {mode_name.upper()}")
print("="*80)
```

**Update at line 331** (return statement):

```python
# CHANGE FROM:
return True, []

# CHANGE TO:
return True, [], mode_name
```

**Update at line 337** (final return):

```python
# CHANGE FROM:
return True, sorted_trades

# CHANGE TO:
return True, sorted_trades, mode_name
```

**Dependencies**: None

**Validation**:
- [ ] Verify mode selection menu displays correctly
- [ ] Verify cancellation returns to Trade Simulator menu
- [ ] Verify mode choice is captured and logged
- [ ] Verify max_weekly_projection is set only for Current Week mode
- [ ] Verify mode name is returned for file output

---

### Phase 2: Add use_weekly_scoring Parameter to TradeSimTeam

**File**: `league_helper/trade_simulator_mode/TradeSimTeam.py`

**Update __init__** (line 38):

```python
# CHANGE FROM:
def __init__(self, name: str, team: List[FantasyPlayer],
             player_manager: PlayerManager, isOpponent: bool = True) -> None:

# CHANGE TO:
def __init__(self, name: str, team: List[FantasyPlayer],
             player_manager: PlayerManager, isOpponent: bool = True,
             use_weekly_scoring: bool = False) -> None:
    """
    Initialize TradeSimTeam with roster and scoring configuration.

    Args:
        name (str): Team name for identification
        team (List[FantasyPlayer]): Complete roster including injured players
        player_manager (PlayerManager): PlayerManager instance for scoring
        isOpponent (bool): If True, use simplified opponent scoring;
                          if False, use comprehensive user team scoring. Defaults to True.
        use_weekly_scoring (bool): If True, use weekly projections with matchup scoring
                                  (matches Starter Helper). If False, use seasonal
                                  projections with standard scoring. Defaults to False.
    """
    self.name = name
    self.isOpponent = isOpponent
    self.use_weekly_scoring = use_weekly_scoring  # NEW
    self.player_manager = player_manager
    # ... rest of initialization (lines 49-66 unchanged)
```

**Dependencies**: None

**Validation**:
- [ ] Verify parameter is stored as instance variable
- [ ] Verify default value False preserves existing behavior
- [ ] Run existing tests to ensure no regressions

---

### Phase 3: Update TradeSimTeam.score_team() to Support Weekly Scoring

**File**: `league_helper/trade_simulator_mode/TradeSimTeam.py`

**Update score_team()** (lines 67-101):

```python
def score_team(self) -> float:
    """
    Calculate total team score using PlayerManager's scoring engine.

    Uses different scoring configurations based on team type and scoring mode:
    - Weekly scoring (use_weekly_scoring=True): Matches Starter Helper exactly
      (weekly projections, matchup=True, player_rating=False, schedule=False)
    - Seasonal scoring (use_weekly_scoring=False): Standard scoring
      (seasonal projections, matchup=False, player_rating=True, schedule=True)
    - Opponent teams (isOpponent=True): No bye penalties
    - User team (isOpponent=False): Include bye penalties (seasonal mode only)

    Returns:
        float: Total team score (sum of all player scores)
    """
    total = 0

    for player in self.team:
        # Determine scoring parameters based on mode
        if self.use_weekly_scoring:
            # CURRENT WEEK MODE: Match Starter Helper EXACTLY
            # (Q2: Include team_quality=True per StarterHelperModeManager.py line 370)
            scored_player = self.player_manager.score_player(
                player,
                use_weekly_projection=True,  # Weekly, not seasonal
                adp=False,
                player_rating=False,         # Disabled for weekly
                team_quality=True,           # Q2: Confirmed include
                performance=True,            # Recent actual vs projected
                matchup=True,                # Enabled for weekly
                schedule=False,              # Disabled for weekly
                bye=False,                   # Never penalize in weekly mode
                injury=False,
                roster=self.team
            )
        elif self.isOpponent:
            # REST OF SEASON MODE - Opponent scoring (no bye penalties)
            scored_player = self.player_manager.score_player(
                player, adp=False, player_rating=True, team_quality=True,
                performance=True, matchup=False, schedule=True, bye=False,
                injury=False, roster=self.team
            )
        else:
            # REST OF SEASON MODE - User team scoring (includes bye penalties)
            scored_player = self.player_manager.score_player(
                player, adp=False, player_rating=True, team_quality=True,
                performance=True, matchup=False, schedule=True, bye=True,
                injury=False, roster=self.team
            )

        player.score = scored_player.score
        self.scored_players[player.id] = scored_player
        total += scored_player.score

    self.team_score = total
    return total
```

**Dependencies**: Phase 2

**Validation**:
- [ ] Verify weekly scoring matches Starter Helper parameters exactly
- [ ] Verify Q2 answer: team_quality=True in weekly mode
- [ ] Verify seasonal scoring remains unchanged
- [ ] Test with both isOpponent=True and isOpponent=False
- [ ] Verify scores differ between weekly and seasonal modes

---

### Phase 4: Update trade_analyzer to Preserve Scoring Mode

**File**: `league_helper/trade_simulator_mode/trade_analyzer.py`

**Issue**: ALL TradeSimTeam instantiations must preserve use_weekly_scoring from original teams

**Pattern to Apply** (35+ locations):

```python
# BEFORE:
my_new_team = TradeSimTeam(my_team.name, my_full_roster, self.player_manager, isOpponent=False)
their_new_team = TradeSimTeam(their_team.name, their_full_roster, self.player_manager, isOpponent=True)

# AFTER:
my_new_team = TradeSimTeam(
    my_team.name, my_full_roster, self.player_manager,
    isOpponent=False,
    use_weekly_scoring=my_team.use_weekly_scoring  # Preserve from original
)
their_new_team = TradeSimTeam(
    their_team.name, their_full_roster, self.player_manager,
    isOpponent=True,
    use_weekly_scoring=their_team.use_weekly_scoring  # Preserve from original
)
```

**Locations to Update** (verified via grep):

**In get_trade_combinations():**
- Line 844-845 (1-for-1 trades)
- Line 912-913 (2-for-2 trades)
- Line 974-975 (3-for-3 trades)
- Line 1057-1058 (2-for-1 trades)
- Line 1088-1089 (2-for-1 with waivers)
- Line 1167-1168 (2-for-1 with drops)
- Line 1208-1209 (1-for-2 trades)
- Line 1274-1275 (1-for-2 with drops)
- Line 1304-1305 (1-for-2 with waivers)
- Line 1369-1370 (3-for-1 trades)
- Line 1408-1409 (3-for-1 with waivers)
- Line 1474-1475 (1-for-3 with drops)
- Line 1504-1505 (1-for-3 with waivers)
- Line 1570-1571 (3-for-2 with drops)
- Line 1609-1610 (3-for-2 with waivers)
- Line 1676-1677 (2-for-3 with drops)
- Line 1706-1707 (2-for-3 with waivers)

**In process_manual_trade():**
- Line 700-701 (manual trade evaluation)

**Total**: 35+ locations requiring updates

**Dependencies**: Phase 3

**Validation**:
- [ ] Verify ALL TradeSimTeam instantiations preserve use_weekly_scoring
- [ ] Test trade combinations with weekly scoring enabled
- [ ] Test trade combinations with seasonal scoring (default)
- [ ] Verify no regressions in existing trade functionality
- [ ] Run full test suite for trade_analyzer

---

### Phase 5: Update File Output to Include Mode

**File**: `league_helper/trade_simulator_mode/trade_file_writer.py`

**Update save_waiver_trades_to_file()** (line 307):

```python
# CHANGE FROM:
def save_waiver_trades_to_file(self, sorted_trades: List[TradeSnapshot],
                               my_team: TradeSimTeam) -> str:

# CHANGE TO:
def save_waiver_trades_to_file(self, sorted_trades: List[TradeSnapshot],
                               my_team: TradeSimTeam, mode: str = "Rest of Season") -> str:
    """
    Save waiver trade recommendations to timestamped file.

    Args:
        sorted_trades: List of trade snapshots sorted by improvement
        my_team: User's team for context
        mode: Scoring mode used ("Rest of Season" or "Current Week")

    Returns:
        str: Filename of saved file
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Q4: Include mode in filename
    mode_suffix = "weekly" if mode == "Current Week" else "ros"
    filename = f"trade_outputs/waiver_{mode_suffix}_{timestamp}.txt"

    with open(filename, 'w') as f:
        f.write("="*80 + "\n")
        # Q3: Minimal display - show mode name only
        f.write(f"WAIVER OPTIMIZER - {mode.upper()}\n")
        f.write("="*80 + "\n\n")
        # ... rest of file writing (lines 320-350 unchanged)
```

**Update call site in TradeSimulatorModeManager.py** (line 162):

```python
# CHANGE FROM:
filename = self.file_writer.save_waiver_trades_to_file(sorted_trades, my_team)

# CHANGE TO:
filename = self.file_writer.save_waiver_trades_to_file(sorted_trades, my_team, mode_name)
```

**Dependencies**: Phase 4

**Validation**:
- [ ] Verify filename includes mode suffix (Q4: `waiver_ros_*.txt` or `waiver_weekly_*.txt`)
- [ ] Verify file header shows mode name (Q3: minimal display)
- [ ] Test file creation with both modes
- [ ] Verify file content is correct for each mode

---

### Phase 6: Update README Documentation

**File**: `README.md`

**Location**: Lines 131-146 (Trade Simulator Mode section)

**Q12: Fix incorrect sub-mode names**

```markdown
# CHANGE FROM (INCORRECT):
#### 3. Trade Simulator Mode
Three trade evaluation sub-modes:
- **Manual Trade Visualizer**: Evaluate individual trades manually with before/after comparison (exports to txt and Excel files)
- **Search Trade Opportunities**: Find best possible trades with your league based on roster needs
- **Full Trade Simulation**: Generate and rank all possible trades across all teams

# CHANGE TO (CORRECT):
#### 3. Trade Simulator Mode
Three trade evaluation sub-modes:

##### 1. Waiver Optimizer
Find optimal waiver wire pickups (drop/add combinations) with two scoring modes:

**Mode Selection**:
- **Rest of Season**: Seasonal projections with standard scoring (player rating, schedule strength)
- **Current Week**: Weekly projections for streaming (matches Starter Helper scoring with matchup multipliers)

**Use Cases**:
- **Rest of Season**: Target long-term value, season-long pickups
- **Current Week**: Stream positions (QB, TE, K, DST) based on weekly matchups

##### 2. Trade Suggestor
Find mutually beneficial trades with league opponents based on roster needs.

##### 3. Manual Trade Visualizer
Evaluate specific trade proposals with before/after comparison (exports to txt and Excel files).

**Supported Trade Types:**
- **Equal Trades**: 1-for-1, 2-for-2, 3-for-3 (balanced player exchanges)
- **Unequal Trades**: 2-for-1, 1-for-2, 3-for-1, 1-for-3, 3-for-2, 2-for-3 (asymmetric exchanges)

**Advanced Features:**
- **Waiver Recommendations**: Automatically suggests waiver wire pickups when trading away more players than receiving
- **Drop System**: Identifies lowest-value players to drop when receiving more players than giving away
- **Trade Threshold**: Enforces minimum 30-point improvement for trade suggestions (0-point minimum for waiver moves)
```

**Dependencies**: None (documentation only)

**Validation**:
- [ ] Verify sub-mode names are corrected
- [ ] Verify mode selection is documented
- [ ] Verify scoring differences are explained
- [ ] Verify use cases are clear

---

## Testing Plan

### Unit Tests

**New Test File**: `tests/league_helper/trade_simulator_mode/test_waiver_streaming.py`

```python
"""
Unit tests for Waiver Optimizer mode selection and weekly scoring.

Tests verify:
- Mode selection UI and cancellation
- Weekly scoring uses correct parameters (matches Starter Helper)
- Seasonal scoring remains unchanged
- Scoring mode produces different results
- File naming includes mode suffix
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from league_helper.trade_simulator_mode.TradeSimTeam import TradeSimTeam
from league_helper.trade_simulator_mode.TradeSimulatorModeManager import TradeSimulatorModeManager


class TestWaiverStreamingModes:
    """Test Waiver Optimizer mode selection and weekly scoring"""

    @pytest.fixture
    def mock_player_manager(self):
        """Create mock PlayerManager for testing"""
        pm = Mock()
        pm.score_player = Mock(return_value=Mock(score=100.0))
        pm.calculate_max_weekly_projection = Mock(return_value=45.0)
        pm.scoring_calculator = Mock()
        return pm

    @pytest.fixture
    def sample_players(self):
        """Create sample player list"""
        players = []
        for i in range(5):
            player = Mock()
            player.id = i
            player.name = f"Player {i}"
            player.position = "QB"
            players.append(player)
        return players

    def test_weekly_scoring_uses_correct_parameters(self, mock_player_manager, sample_players):
        """Verify Current Week mode uses Starter Helper scoring parameters (Q2: team_quality=True)"""
        team = TradeSimTeam(
            "Test Team",
            sample_players,
            mock_player_manager,
            isOpponent=False,
            use_weekly_scoring=True
        )

        # Trigger scoring
        team.score_team()

        # Verify score_player was called with weekly parameters
        assert mock_player_manager.score_player.called
        call_kwargs = mock_player_manager.score_player.call_args[1]

        # Verify weekly mode parameters
        assert call_kwargs['use_weekly_projection'] == True
        assert call_kwargs['matchup'] == True
        assert call_kwargs['player_rating'] == False
        assert call_kwargs['schedule'] == False
        assert call_kwargs['team_quality'] == True  # Q2: Confirmed
        assert call_kwargs['bye'] == False

    def test_seasonal_scoring_unchanged(self, mock_player_manager, sample_players):
        """Verify Rest of Season mode uses original scoring parameters"""
        team = TradeSimTeam(
            "Test Team",
            sample_players,
            mock_player_manager,
            isOpponent=False,
            use_weekly_scoring=False
        )

        team.score_team()

        call_kwargs = mock_player_manager.score_player.call_args[1]

        # Verify seasonal mode parameters (unchanged)
        assert call_kwargs.get('use_weekly_projection', False) == False
        assert call_kwargs['matchup'] == False
        assert call_kwargs['player_rating'] == True
        assert call_kwargs['schedule'] == True
        assert call_kwargs['bye'] == True  # User team gets bye penalties

    def test_weekly_scoring_no_bye_penalties(self, mock_player_manager, sample_players):
        """Verify weekly mode never applies bye penalties"""
        team = TradeSimTeam(
            "Test Team",
            sample_players,
            mock_player_manager,
            isOpponent=False,
            use_weekly_scoring=True
        )

        team.score_team()

        call_kwargs = mock_player_manager.score_player.call_args[1]
        assert call_kwargs['bye'] == False  # No bye penalties in weekly mode

    def test_default_use_weekly_scoring_false(self, mock_player_manager, sample_players):
        """Verify backward compatibility: default use_weekly_scoring=False (Q9)"""
        team = TradeSimTeam(
            "Test Team",
            sample_players,
            mock_player_manager,
            isOpponent=False
            # use_weekly_scoring NOT specified - should default to False
        )

        assert team.use_weekly_scoring == False

    def test_mode_selection_cancel(self, tmp_path):
        """Test cancelling out of mode selection (Q1: Option A)"""
        # Setup
        manager = Mock()
        manager.logger = Mock()
        manager.player_manager = Mock()
        manager.config = Mock()

        # Mock user selecting Cancel (choice 3)
        with patch('league_helper.trade_simulator_mode.TradeSimulatorModeManager.show_list_selection',
                   return_value=3):
            with patch.object(TradeSimulatorModeManager, 'start_waiver_optimizer',
                            wraps=TradeSimulatorModeManager.start_waiver_optimizer):
                # This should return early with empty results
                # Actual test would verify return values
                pass

    def test_file_naming_includes_mode_suffix(self):
        """Verify filename includes mode suffix (Q4: Option A)"""
        from league_helper.trade_simulator_mode.trade_file_writer import TradeFileWriter

        writer = TradeFileWriter("trade_outputs")

        # Test ROS mode
        filename_ros = writer.save_waiver_trades_to_file([], Mock(), mode="Rest of Season")
        assert "waiver_ros_" in filename_ros

        # Test Current Week mode
        filename_weekly = writer.save_waiver_trades_to_file([], Mock(), mode="Current Week")
        assert "waiver_weekly_" in filename_weekly


class TestTradeAnalyzerScoringPropagation:
    """Test that trade_analyzer preserves use_weekly_scoring"""

    def test_trade_combinations_preserve_scoring_mode(self):
        """Verify trade combinations preserve use_weekly_scoring from original teams"""
        # This would test that when trade_analyzer creates new TradeSimTeam objects,
        # they preserve the use_weekly_scoring flag from the original teams
        pass
```

**Update Existing Tests**: `tests/league_helper/trade_simulator_mode/test_trade_simulator.py`

- [ ] Add use_weekly_scoring parameter to all TradeSimTeam instantiations
- [ ] Update tests to verify backward compatibility (default False)
- [ ] Add test for mode selection UI
- [ ] Add test for max_weekly_projection being set

**Update**: `tests/league_helper/trade_simulator_mode/test_trade_analyzer.py`

- [ ] Verify scoring mode preservation in all trade combination methods
- [ ] Test with both weekly and seasonal scoring
- [ ] Ensure no regressions

### Integration Tests

**File**: `tests/integration/test_league_helper_integration.py`

```python
def test_waiver_optimizer_current_week_mode(temp_data_folder):
    """Test full Waiver Optimizer workflow with Current Week mode"""
    # Setup
    manager = TradeSimulatorModeManager(temp_data_folder, player_manager, config)

    # Simulate mode selection (Current Week)
    with patch('league_helper.util.user_input.show_list_selection', return_value=2):
        loop, trades, mode_name = manager.start_waiver_optimizer()

    # Verify
    assert loop == True
    assert mode_name == "Current Week"
    assert len(trades) > 0

def test_waiver_optimizer_rest_of_season_mode(temp_data_folder):
    """Test full Waiver Optimizer workflow with Rest of Season mode"""
    manager = TradeSimulatorModeManager(temp_data_folder, player_manager, config)

    # Simulate mode selection (Rest of Season)
    with patch('league_helper.util.user_input.show_list_selection', return_value=1):
        loop, trades, mode_name = manager.start_waiver_optimizer()

    assert loop == True
    assert mode_name == "Rest of Season"

def test_waiver_optimizer_mode_cancellation(temp_data_folder):
    """Test cancelling out of mode selection (Q1: Option A)"""
    manager = TradeSimulatorModeManager(temp_data_folder, player_manager, config)

    # Simulate cancellation
    with patch('league_helper.util.user_input.show_list_selection', return_value=3):
        loop, trades, mode_name = manager.start_waiver_optimizer()

    assert loop == True
    assert len(trades) == 0
    assert mode_name == ""
```

### Manual Testing Checklist

- [ ] Enter Trade Simulator → Waiver Optimizer
- [ ] Verify mode selection menu appears with options: "Rest of Season", "Current Week", "Cancel"
- [ ] Select "Cancel" and verify return to Trade Simulator menu
- [ ] Select "Rest of Season" and verify recommendations match existing behavior
- [ ] Select "Current Week" and verify recommendations use weekly projections
- [ ] Verify different players recommended in each mode
- [ ] Verify file output includes mode in filename (`waiver_ros_*.txt` vs `waiver_weekly_*.txt`)
- [ ] Verify file header shows mode name (Q3: minimal display)
- [ ] Verify Trade Suggestor still works (unchanged - Q6)
- [ ] Verify Manual Trade still works (unchanged - Q7)

---

## Pre-Commit Checklist

### Testing
- [ ] All unit tests pass (100% pass rate)
- [ ] Integration tests pass
- [ ] Manual testing completed for both modes
- [ ] Backward compatibility verified (default False works)

### Code Quality
- [ ] Code follows style guidelines (CLAUDE.md)
- [ ] Type hints added to all new/modified methods
- [ ] Docstrings updated with Google style
- [ ] No code duplication

### Logging
- [ ] Mode selection logged
- [ ] max_weekly_projection setting logged
- [ ] Weekly vs seasonal scoring usage logged
- [ ] Trade evaluation logged with mode context

### Error Handling
- [ ] Invalid mode selection handled
- [ ] Missing weekly projection data handled gracefully
- [ ] max_weekly_projection validation
- [ ] File write errors handled

### Documentation
- [ ] README.md updated (Q12: corrected sub-mode names)
- [ ] README.md documents mode selection (Q8: Option B)
- [ ] ARCHITECTURE.md updated if needed
- [ ] All docstrings complete and accurate

### Verification
- [ ] All 35+ TradeSimTeam instantiations verified and updated
- [ ] Scoring parameters match Starter Helper exactly (Q2: team_quality=True)
- [ ] File naming includes mode suffix (Q4: Option A)
- [ ] Only Waiver Optimizer affected (Q6/Q7: Option A)

---

## Files Modified Summary

### Files to Modify (4 files):

1. **TradeSimulatorModeManager.py** (~50 lines changed)
   - Add mode selection UI
   - Set max_weekly_projection
   - Re-create teams with mode-specific scoring
   - Update display header (Q3: minimal)
   - Update return signature

2. **TradeSimTeam.py** (~30 lines changed)
   - Add use_weekly_scoring parameter
   - Update score_team() with weekly scoring logic
   - Update docstrings

3. **trade_analyzer.py** (~70 lines changed)
   - Update 35+ TradeSimTeam instantiations
   - Preserve use_weekly_scoring flag

4. **trade_file_writer.py** (~10 lines changed)
   - Add mode parameter
   - Update filename to include mode suffix (Q4)
   - Update file header (Q3: minimal)

### Files to Create (1 file):

5. **test_waiver_streaming.py** (~150 lines)
   - New test file for mode selection and weekly scoring

### Files to Update (3 test files):

6. **test_trade_simulator.py** - Update existing tests
7. **test_trade_analyzer.py** - Add scoring mode tests
8. **test_league_helper_integration.py** - Add integration tests

### Documentation Files (1 file):

9. **README.md** - Fix sub-mode names (Q12) and document mode selection (Q8)

**Total**: 9 files (4 modified, 1 created, 3 test updates, 1 documentation)

**Lines of Code**: ~310 lines added/modified

---

## Verification Summary - 12 Complete Iterations

### Iterations 1-5: Initial Verification and Questions

**Key Findings**:
- ✅ Identified Waiver Optimizer location (TradeSimulatorModeManager.py line 235)
- ✅ Found README documentation error (lines 133-135)
- ✅ Researched Starter Helper scoring parameters
- ✅ Discovered 35+ TradeSimTeam instantiations requiring updates
- ✅ Created questions file with 12 research-backed questions

**Iteration 5 (Skeptical Re-verification #1)**:
- ✅ Re-verified Waiver Optimizer is Trade Simulator sub-mode (NOT Reserve Assessment)
- ✅ Confirmed specification requires exact Starter Helper match
- ✅ Validated max_weekly_projection must be set before TradeSimTeam creation
- ✅ Verified my_team must be re-created with mode-specific scoring

### Iterations 6-9: User Answer Integration

**User Answers Integrated**:
- Q1 (Option A): Include cancel option ✅
- Q2 (Yes): Include team_quality=True ✅
- Q3 (Option C): Minimal display (mode name only) ✅
- Q4 (Option A): Mode-specific filenames ✅
- Q5 (Option A): Same threshold for both modes ✅
- Q6/Q7 (Option A): Only Waiver Optimizer gets mode selection ✅
- Q8 (Option B): README documentation only ✅
- Q9 (Yes): Maintain backward compatibility ✅
- Q10 (Option A): Standard test coverage ✅
- Q11 (Yes): Support flexible structure ✅
- Q12 (Yes): Correct README error ✅

**Implementation Refined Based on Answers**:
- Display updated to show mode name only (Q3)
- Filename pattern: `waiver_ros_*.txt` and `waiver_weekly_*.txt` (Q4)
- Trade Suggestor and Manual Trade unchanged (Q6/Q7)
- README correction included in scope (Q12)

### Iteration 10 (Skeptical Re-verification #2)

**Critical Re-verifications**:
- ✅ Mode selection MUST happen before TradeSimTeam creation (line 259)
- ✅ show_list_selection returns 1-based index, choice > len(options) = cancel
- ✅ start_waiver_optimizer() return signature needs mode_name (3-tuple)
- ✅ Weekly scoring uses same parameters for opponent and user (no bye difference)
- ✅ Q2 answer verified: team_quality=True in StarterHelperModeManager.py line 370

**No corrections needed** - all previous claims re-verified as accurate

### Iterations 11-12: Final Preparation

**Implementation Readiness Confirmed**:
- ✅ All code changes have exact line numbers
- ✅ All user answers correctly integrated
- ✅ Backward compatibility preserved (default False)
- ✅ Test strategy defined with code templates
- ✅ Risk areas identified and mitigated
- ✅ Documentation plan complete

**Files Requiring Changes**: 9 files (4 modified, 1 created, 3 test updates, 1 documentation)

**Code Complexity**: Medium (35+ instantiations, but straightforward pattern)

**Estimated Implementation Time**: 4-6 hours

---

## Risk Assessment

### Medium Risks

**Risk**: Missing TradeSimTeam instantiation update (35+ locations)
- **Mitigation**: Systematic grep verification + comprehensive testing
- **Impact**: Mode wouldn't be preserved, causing incorrect scoring
- **Detection**: Unit tests will catch inconsistencies

**Risk**: max_weekly_projection timing (must be set before TradeSimTeam)
- **Mitigation**: Clear code comments + integration test
- **Impact**: Weekly normalization would fail
- **Detection**: Integration tests verify correct order

### Low Risks

**Risk**: Backward compatibility
- **Mitigation**: Default use_weekly_scoring=False preserves all existing behavior
- **Impact**: Minimal - existing code continues working
- **Detection**: Existing test suite validates no regressions

**Risk**: Mode selection UI confusion
- **Mitigation**: Clear option names ("Rest of Season", "Current Week")
- **Impact**: User might select wrong mode
- **Detection**: Manual testing + user feedback

**Risk**: README documentation error propagation
- **Mitigation**: Q12 fix corrects error immediately
- **Impact**: Documentation stays accurate
- **Detection**: Code review

---

## Success Criteria

### Functional Requirements
- ✅ Mode selection appears when entering Waiver Optimizer
- ✅ "Rest of Season" mode works exactly as before (backward compatible)
- ✅ "Current Week" mode uses Starter Helper scoring (Q2: team_quality=True)
- ✅ Cancel option returns to Trade Simulator menu (Q1)
- ✅ Mode name displayed in header (Q3: minimal)
- ✅ Filenames include mode suffix (Q4)
- ✅ Trade Suggestor unchanged (Q6)
- ✅ Manual Trade unchanged (Q7)
- ✅ README corrected (Q12)

### Technical Requirements
- ✅ 100% test pass rate maintained
- ✅ New tests cover both modes (Q10: standard coverage)
- ✅ No code duplication
- ✅ Proper logging at all decision points
- ✅ Graceful error handling
- ✅ Type hints on all new/modified methods
- ✅ Docstrings follow Google style
- ✅ Backward compatibility preserved (Q9)

---

## Implementation Notes

**Design Decisions**:

1. **Scoring Mode Storage**: Added `use_weekly_scoring` to TradeSimTeam (mirrors `isOpponent` pattern)
2. **my_team Re-creation**: Re-create in start_waiver_optimizer() for mode-specific scoring
3. **Scoring Parameters**: Match Starter Helper exactly (Q2: team_quality=True confirmed)
4. **max_weekly_projection**: Set before TradeSimTeam creation for proper normalization
5. **Display**: Minimal mode name only (Q3: Option C)
6. **File Naming**: Mode-specific suffixes (Q4: Option A)
7. **Scope**: Only Waiver Optimizer (Q6/Q7: Option A)

**Architecture Notes**:

- TradeSimTeam now has THREE scoring modes (opponent, user, weekly)
- Weekly scoring treats opponent and user the same (no bye difference)
- Backward compatibility via default parameter (use_weekly_scoring=False)
- Mode preserved through all trade_analyzer operations (35+ instantiations)

---

## Ready for Implementation

**Status**: ✅ VERIFIED AND READY

- All 12 verification iterations complete
- All user answers integrated
- Skeptical re-verification passed (iterations 5 and 10)
- Implementation plan detailed with exact line numbers
- Test strategy defined
- Risk mitigation planned
- Success criteria established

**Next Step**: Begin Phase 1 implementation
