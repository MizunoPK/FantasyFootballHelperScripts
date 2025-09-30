# Starter Helper Scoring Overhaul - TODO File

**Objective**: Fix the starter_helper's scoring calculations to align with the requirements specified in scoring_overhaul.txt

**Status**: In Progress
**Created**: 2025-09-30
**Last Updated**: 2025-09-30

---

## 📋 **OVERVIEW**

Based on analysis of the current starter_helper implementation vs scoring_overhaul.txt requirements, the starter_helper is implementing a **completely different scoring system** than specified. This TODO outlines the systematic fixes needed.

### **Current Problems Found**:
1. ❌ Uses positional ranking adjustments instead of required matchup multipliers
2. ❌ Uses point-based injury penalties instead of binary active/inactive (zero out)
3. ❌ Includes bye week penalties that aren't required for Starter Helper
4. ❌ Applies matchup adjustments to K/DST when it should only apply to QB/RB/WR/TE
5. ❌ Missing configurable matchup multiplier system

### **Required Implementation** (from scoring_overhaul.txt lines 40-43):
```
Starter Helper:
1. Get the projected points for the player on the current week
2. Apply the Match Up multiplier
3. Subtract the Injury Penalty (zero out non-ACTIVE/QUESTIONABLE players)
```

---

## 🎯 **PHASE 1: CONFIGURATION SYSTEM SETUP**

### **Phase 1.1: Create Matchup Multiplier Configuration** ⏳
- [ ] **1.1.1**: Add matchup multiplier configuration to `starter_helper/starter_helper_config.py`
  - [ ] Add `MATCHUP_MULTIPLIERS` dictionary with rank difference ranges
  - [ ] Add `MATCHUP_ENABLED_POSITIONS = ['QB', 'RB', 'WR', 'TE']`
  - [ ] Add configuration validation for new settings
  - [ ] Document the new configuration options
- [ ] **1.1.2**: Update simulation config (`draft_helper/simulation/config.py`)
  - [ ] Verify matchup multiplier parameters are properly defined
  - [ ] Add any missing simulation parameters for matchup system
- [ ] **1.1.3**: Create unit tests for new configuration
  - [ ] Test matchup multiplier config loading
  - [ ] Test validation of new config parameters
  - [ ] Test edge cases and invalid configurations

**🚨 MANDATORY**: Execute full pre-commit validation after Phase 1 completion

---

## 🎯 **PHASE 2: INJURY SYSTEM OVERHAUL**

### **Phase 2.1: Replace Point-Based Injury System with Binary System** ⏳
- [ ] **2.1.1**: Update injury handling logic in `lineup_optimizer.py`
  - [ ] Modify `calculate_adjusted_score()` to zero out non-ACTIVE/QUESTIONABLE players
  - [ ] Remove point-based `INJURY_PENALTIES` subtraction
  - [ ] Implement binary check: if not in ['ACTIVE', 'QUESTIONABLE'] then score = 0
- [ ] **2.1.2**: Update injury penalty configuration
  - [ ] Keep `INJURY_PENALTIES` for other modes, add new binary system for starter_helper
  - [ ] Add `STARTER_HELPER_ACTIVE_STATUSES = ['ACTIVE', 'QUESTIONABLE']`
  - [ ] Document the difference between starter_helper and other modes
- [ ] **2.1.3**: Update unit tests for new injury system
  - [ ] Modify existing injury penalty tests in `test_lineup_optimizer.py`
  - [ ] Add tests for binary injury system (active/questionable vs zero)
  - [ ] Test edge cases with various injury statuses

**🚨 MANDATORY**: Execute full pre-commit validation after Phase 2 completion

---

## 🎯 **PHASE 3: REMOVE BYE WEEK PENALTIES**

### **Phase 3.1: Remove Bye Week Logic from Starter Helper** ⏳
- [ ] **3.1.1**: Remove bye week penalty logic from `calculate_adjusted_score()`
  - [ ] Remove `BYE_WEEK_PENALTY` subtraction
  - [ ] Remove bye week parameter from scoring calculation
  - [ ] Keep bye week tracking for display purposes only
- [ ] **3.1.2**: Update unit tests to reflect bye week removal
  - [ ] Remove bye week penalty tests from `test_lineup_optimizer.py`
  - [ ] Update tests that expect bye week penalties
  - [ ] Ensure bye week display still works (for informational purposes)

**🚨 MANDATORY**: Execute full pre-commit validation after Phase 3 completion

---

## 🎯 **PHASE 4: IMPLEMENT MATCHUP MULTIPLIER SYSTEM**

### **Phase 4.1: Create Matchup Calculator** ⏳
- [ ] **4.1.1**: Create new `MatchupCalculator` class
  - [ ] Create `starter_helper/matchup_calculator.py`
  - [ ] Implement rank difference calculation logic
  - [ ] Implement multiplier application based on rank differences
  - [ ] Add proper error handling and logging
- [ ] **4.1.2**: Define matchup multiplier ranges
  - [ ] Implement rank difference thresholds (excellent, good, neutral, poor, very poor)
  - [ ] Make thresholds configurable in starter_helper_config.py
  - [ ] Add validation for multiplier ranges
- [ ] **4.1.3**: Create comprehensive unit tests for MatchupCalculator
  - [ ] Test rank difference calculations
  - [ ] Test multiplier application logic
  - [ ] Test position filtering (QB/RB/WR/TE only)
  - [ ] Test edge cases and error conditions

### **Phase 4.2: Integrate Matchup System into LineupOptimizer** ⏳
- [ ] **4.2.1**: Replace PositionalRankingCalculator with MatchupCalculator
  - [ ] Remove `positional_ranking_calculator` from `LineupOptimizer.__init__()`
  - [ ] Add `matchup_calculator` initialization
  - [ ] Update `calculate_adjusted_score()` to use new matchup system
- [ ] **4.2.2**: Update position filtering logic
  - [ ] Only apply matchup multipliers to QB, RB, WR, TE
  - [ ] Bypass matchup adjustments for K and DST
  - [ ] Maintain original projected points for non-eligible positions
- [ ] **4.2.3**: Update all method signatures and calls
  - [ ] Remove positional ranking parameters from method calls
  - [ ] Add matchup-related parameters as needed
  - [ ] Update error handling and logging messages

**🚨 MANDATORY**: Execute full pre-commit validation after Phase 4 completion

---

## 🎯 **PHASE 5: UPDATE UNIT TESTS**

### **Phase 5.1: Comprehensive Test Updates** ⏳
- [ ] **5.1.1**: Update `test_lineup_optimizer.py`
  - [ ] Replace positional ranking tests with matchup multiplier tests
  - [ ] Update injury penalty tests to reflect new binary system
  - [ ] Remove bye week penalty tests
  - [ ] Add comprehensive matchup system tests
- [ ] **5.1.2**: Update `test_starter_helper.py`
  - [ ] Update integration tests to reflect new scoring system
  - [ ] Test complete scoring flow: base points → matchup → injury
  - [ ] Verify position filtering works correctly
- [ ] **5.1.3**: Create new test files as needed
  - [ ] Create `test_matchup_calculator.py` with comprehensive coverage
  - [ ] Add performance tests for new scoring system
  - [ ] Add integration tests with real data scenarios

### **Phase 5.2: Test Data and Mocking** ⏳
- [ ] **5.2.1**: Create test data for matchup scenarios
  - [ ] Mock team ranking data for matchup calculations
  - [ ] Create test cases covering all multiplier ranges
  - [ ] Add edge cases for rank difference calculations
- [ ] **5.2.2**: Update existing mocks and fixtures
  - [ ] Update positional ranking mocks to matchup mocks
  - [ ] Ensure all tests use new scoring system expectations
  - [ ] Verify test isolation and independence

**🚨 MANDATORY**: Execute full pre-commit validation and run ALL repository tests after Phase 5 completion

---

## 🎯 **PHASE 6: DOCUMENTATION UPDATES**

### **Phase 6.1: Update Configuration Documentation** ⏳
- [ ] **6.1.1**: Update `CLAUDE.md`
  - [ ] Document new starter_helper scoring system (3-step process)
  - [ ] Update "Fantasy Points Calculation System" section
  - [ ] Remove references to old positional ranking in starter_helper
  - [ ] Add matchup multiplier configuration guide
- [ ] **6.1.2**: Update `starter_helper/README.md` (if exists)
  - [ ] Document new scoring methodology
  - [ ] Update configuration examples
  - [ ] Add troubleshooting guide for matchup system
- [ ] **6.1.3**: Update inline code documentation
  - [ ] Add comprehensive docstrings to new MatchupCalculator
  - [ ] Update existing docstrings to reflect new system
  - [ ] Add examples and usage patterns in comments

### **Phase 6.2: Update Configuration Guides** ⏳
- [ ] **6.2.1**: Update quick configuration guide in `starter_helper_config.py`
  - [ ] Document new matchup multiplier settings
  - [ ] Update frequently modified settings section
  - [ ] Add configuration examples for different strategies
- [ ] **6.2.2**: Update simulation configuration documentation
  - [ ] Document new matchup parameters in simulation config
  - [ ] Update parameter range explanations
  - [ ] Add guidance for tuning matchup multipliers

**🚨 MANDATORY**: Execute full pre-commit validation after Phase 6 completion

---

## 🎯 **PHASE 7: INTEGRATION TESTING & VALIDATION**

### **Phase 7.1: Comprehensive System Testing** ⏳
- [ ] **7.1.1**: Test complete starter_helper workflow
  - [ ] Run starter_helper with new scoring system
  - [ ] Verify lineup recommendations are reasonable
  - [ ] Test with various injury statuses and matchup scenarios
- [ ] **7.1.2**: Test integration with draft_helper
  - [ ] Verify integrated starter_helper (menu option 6) works with new system
  - [ ] Test trade simulator integration if applicable
  - [ ] Ensure no regression in other draft_helper functions
- [ ] **7.1.3**: Performance and accuracy testing
  - [ ] Benchmark new scoring system performance
  - [ ] Validate matchup calculations against expected results
  - [ ] Test with large roster datasets

### **Phase 7.2: Regression Testing** ⏳
- [ ] **7.2.1**: Run all existing integration tests
  - [ ] Execute `draft_helper_validation_checklist.md` steps
  - [ ] Verify FLEX system still works correctly
  - [ ] Test CSV data persistence
- [ ] **7.2.2**: Verify other modules unaffected
  - [ ] Test player_data_fetcher startup and execution
  - [ ] Test nfl_scores_fetcher startup and execution
  - [ ] Ensure shared files and utilities still work

**🚨 MANDATORY**: Execute COMPLETE pre-commit validation checklist including ALL 23 integration test steps

---

## 🎯 **PHASE 8: CLEANUP & FINALIZATION**

### **Phase 8.1: Remove Deprecated Code** ⏳
- [ ] **8.1.1**: Remove unused positional ranking code
  - [ ] Remove positional ranking imports from `lineup_optimizer.py`
  - [ ] Clean up unused configuration parameters
  - [ ] Remove deprecated test code and mocks
- [ ] **8.1.2**: Update imports and dependencies
  - [ ] Clean up unused imports throughout starter_helper module
  - [ ] Update requirements if new dependencies added
  - [ ] Verify no circular imports introduced

### **Phase 8.2: Final Validation & Documentation** ⏳
- [ ] **8.2.1**: Final comprehensive testing
  - [ ] Run complete test suite (100% pass rate required)
  - [ ] Execute all integration tests
  - [ ] Verify startup validation for all core modules
- [ ] **8.2.2**: Update final documentation
  - [ ] Create or update `Draft_Helper_Data_Usage_Report.md` reflecting changes
  - [ ] Document performance impact of new scoring system
  - [ ] Add troubleshooting guide for common issues
- [ ] **8.2.3**: Move objective to completion
  - [ ] Move `scoring_overhaul.txt` to `potential_updates/done/` folder
  - [ ] Archive this TODO file with completion status
  - [ ] Update project status documentation

**🚨 MANDATORY**: Execute final complete pre-commit validation and user notification

---

## ✅ **CLARIFICATIONS RECEIVED FROM USER**

All questions have been answered via `scoring_overhaul_clarification_questions.md`:

1. **Matchup Data Source**: ✅ Use existing `teams.csv` with offensive_rank, defensive_rank, and opponent columns
   - Data structure: `team,offensive_rank,defensive_rank,opponent`
   - Already populated with ranks 1-32 and current week opponent matchups
   - Use existing TeamDataLoader and extend as needed

2. **Rank Difference Thresholds**: ✅ Formula: `(Opponent Defensive Rank) - (Player's Team Offensive Rank)`
   - Excellent: >=15 = 1.2x multiplier
   - Good: 6 to 14 = 1.1x multiplier
   - Neutral: -5 to 5 = 1.0x multiplier
   - Poor: -14 to -6 = 0.9x multiplier
   - Very Poor: <=-15 = 0.8x multiplier

3. **Opponent Team Detection**: ✅ Already in `teams.csv` as `opponent` column
   - Updated weekly to reflect current matchups
   - No additional data source needed

4. **Backward Compatibility**: ✅ Clean break acceptable, no need for feature flags or migration

5. **Configuration Location**: ✅ Add to `starter_helper_config.py` and simulation config ranges

6. **Additional Requirements**:
   - ✅ Normalization: 0-N scale (default 100), configurable for simulation
   - ✅ Binary Injury: Zero out non-ACTIVE/QUESTIONABLE players
   - ✅ Bye Weeks: Already 0.0 in player data, no additional logic needed
   - ✅ Extensive Logging: Add detailed logging for debugging
   - ✅ Liberal Unit Testing: Comprehensive test coverage required

---

## 🚨 **CRITICAL REMINDERS**

### **Pre-Commit Validation Protocol**
- ✅ **MANDATORY** after every phase completion
- ✅ Copy `tests/pre_commit_validation_checklist.md` to `tests/temp_commit_checklist.md`
- ✅ Execute ALL 7 validation steps systematically
- ✅ 100% test pass rate required before proceeding
- ✅ Full integration testing (all 23 steps) required
- ✅ Startup validation for core modules required

### **Testing Requirements**
- ✅ ALL repository tests must pass (not just starter_helper tests)
- ✅ Unit tests, integration tests, and startup validation all required
- ✅ No exceptions or skipping of tests allowed
- ✅ Each phase must leave repository in testable, functional state

### **Documentation Requirements**
- ✅ Update all relevant documentation as changes are made
- ✅ Include examples and configuration guides
- ✅ Update troubleshooting and FAQ sections
- ✅ Maintain consistency across all documentation files

---

## 📊 **PROGRESS TRACKING**

**Keep this section updated as work progresses:**

- [🔄] Phase 1: Configuration System Setup - ✅ IN PROGRESS
  - [✅] 1.1.1: Added matchup multiplier configuration to `starter_helper_config.py`
    - Added `MATCHUP_MULTIPLIERS` dictionary with 5 rank difference ranges
    - Added `MATCHUP_ENABLED_POSITIONS = [QB, RB, WR, TE]`
    - Added `STARTER_HELPER_ACTIVE_STATUSES = ['ACTIVE', 'QUESTIONABLE']`
    - Documentation added for formula: (Opponent Defense Rank) - (Team Offense Rank)
  - [ ] 1.1.2: Update validation for new configuration
  - [ ] 1.1.3: Update simulation config with parameter ranges
  - [ ] 1.1.4: Create unit tests for new configuration

- [ ] Phase 2: Injury System Overhaul - ⏳ Not Started
- [ ] Phase 3: Remove Bye Week Penalties - ⏳ Not Started
- [ ] Phase 4: Implement Matchup Multiplier System - ⏳ Not Started
- [ ] Phase 5: Update Unit Tests - ⏳ Not Started
- [ ] Phase 6: Documentation Updates - ⏳ Not Started
- [ ] Phase 7: Integration Testing & Validation - ⏳ Not Started
- [ ] Phase 8: Cleanup & Finalization - ⏳ Not Started

**Last Progress Update**: 2025-09-30 - Phase 1 started, matchup configuration added to starter_helper_config.py

---

**⚠️ IMPORTANT**: This TODO file must be kept up to date with progress. Update status, mark completed items, and add any new discoveries or requirements as work progresses. Future Claude sessions will rely on this file for continuity.