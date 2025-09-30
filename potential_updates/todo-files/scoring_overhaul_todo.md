# Scoring Overhaul Implementation TODO

## 📋 Task Overview
**Objective**: Complete scoring system overhaul for fantasy football draft helper, removing positional need calculations and implementing proper DRAFT_ORDER integration with normalization.

**Key Requirements**:
- Remove positional need scoring entirely (not just toggle)
- Implement DRAFT_ORDER round-based bonus system with static values
- Add normalization (0-100 scale) for seasonal fantasy points
- Remove matchup considerations from Add to Roster mode
- Implement proper Starter Helper scoring with matchup multipliers
- Make all multipliers configurable in simulation config
- Update all four calculation modes (Add to Roster, Waiver Optimizer, Starter Helper, Trade Simulator)

## 🎯 Master Plan

### **Phase 1: Analysis and Infrastructure Setup**
1. 🔲 **Step 1.1**: Deep analysis of current scoring system architecture
2. 🔲 **Step 1.2**: Create backup branch for rollback safety
3. 🔲 **Step 1.3**: Map all files that need modification
4. 🔲 **Step 1.4**: Design new normalization system architecture
5. 🔲 **Step 1.5**: Design DRAFT_ORDER static value system architecture

### **Phase 2: Configuration System Updates**
1. 🔲 **Step 2.1**: Update simulation config with normalization parameters:
   - `NORMALIZATION_MAX_SCALE: [80, 100, 120]` (default: 100)
2. 🔲 **Step 2.2**: Update simulation config with static DRAFT_ORDER bonus ranges:
   - `DRAFT_ORDER_PRIMARY_BONUS: [40, 50, 60]` (for #1 positions)
   - `DRAFT_ORDER_SECONDARY_BONUS: [20, 25, 30]` (for secondary positions)
3. 🔲 **Step 2.3**: Update simulation config with matchup multiplier ranges:
   - `MATCHUP_EXCELLENT_MULTIPLIER: [1.15, 1.2, 1.25]` (for rank diff 15+)
   - `MATCHUP_GOOD_MULTIPLIER: [1.05, 1.1, 1.15]` (for rank diff 6-15)
   - `MATCHUP_POOR_MULTIPLIER: [0.8, 0.85, 0.9]` (for rank diff <-15)
4. 🔲 **Step 2.4**: Fix DRAFT_ORDER syntax error in draft_helper_config.py (missing comma line 49)
5. 🔲 **Step 2.5**: Update DRAFT_ORDER to use static values: {FLEX: 50, QB: 25} pattern
6. 🔲 **Step 2.6**: Add round tracking mechanism for current draft round determination

### **Phase 3: Core Scoring Engine Overhaul**
1. 🔲 **Step 3.1**: Remove all positional need calculation code from scoring_engine.py
2. 🔲 **Step 3.2**: Implement normalization system for fantasy points (0-100 scale)
3. 🔲 **Step 3.3**: Implement DRAFT_ORDER round-based bonus system
4. 🔲 **Step 3.4**: Remove matchup considerations from draft scoring
5. 🔲 **Step 3.5**: Create separate scoring methods for each mode

### **Phase 4: Individual Mode Implementation**
1. 🔲 **Step 4.1**: Implement Add to Roster Mode scoring (7 steps):
   1. Get normalized seasonal fantasy points: `(player_points / max_player_points) * normalization_scale`
   2. Apply ADP Multiplier (existing enhanced scoring)
   3. Apply Player Ranking multiplier (existing enhanced scoring)
   4. Apply Team ranking multiplier (existing enhanced scoring)
   5. Add DRAFT_ORDER bonus based on current round and position
   6. Subtract Bye Week Penalty (existing logic)
   7. Subtract Injury Penalty (existing logic)
2. 🔲 **Step 4.2**: Implement Waiver Optimizer scoring (same as Add to Roster minus DRAFT_ORDER)
3. 🔲 **Step 4.3**: Implement Trade Simulator scoring (same as Waiver Optimizer)
4. 🔲 **Step 4.4**: Implement Starter Helper scoring (3 steps):
   1. Get current week projected points (no normalization, use week-by-week system)
   2. Apply matchup multiplier: `(opponent_def_rank - team_off_rank)` → multiplier ranges
   3. Apply injury filtering: zero out if not ACTIVE or QUESTIONABLE

### **Phase 5: Matchup System for Starter Helper**
1. 🔲 **Step 5.1**: Implement matchup multiplier calculation system:
   - Formula: `rank_diff = opponent_defense_rank - player_team_offense_rank`
   - Positive diff = favorable matchup (>1.0x multiplier)
   - Negative diff = unfavorable matchup (<1.0x multiplier)
2. 🔲 **Step 5.2**: Implement multiplier ranges:
   - `rank_diff < -15`: 0.8x multiplier
   - `rank_diff -15 to -6`: 0.9x multiplier
   - `rank_diff -5 to 5`: 1.0x multiplier
   - `rank_diff 6 to 15`: 1.1x multiplier
   - `rank_diff > 15`: 1.2x multiplier
3. 🔲 **Step 5.3**: Apply multipliers only to QB, WR, RB, TE (skip K and DEF)
4. 🔲 **Step 5.4**: Remove MIN_TOTAL_ADJUSTMENT and MAX_TOTAL_ADJUSTMENT caps from ALL systems
5. 🔲 **Step 5.5**: Add extensive logging for matchup calculations

### **Phase 6: Round Tracking System**
1. 🔲 **Step 6.1**: Implement roster-to-round assignment algorithm:
   - Loop through each roster player, then each round
   - Find first unassigned round where player's position matches round's highest-value position
   - Assignment order doesn't matter - just fill slots based on position fits
2. 🔲 **Step 6.2**: Create current round determination logic:
   - Find first round not assigned to any player = current round
3. 🔲 **Step 6.3**: Integrate round tracking with DRAFT_ORDER bonus system
4. 🔲 **Step 6.4**: Add unit tests to verify roster composition always matches DRAFT_ORDER expectations

### **Phase 7: Testing and Validation** (Liberal Unit Testing as Requested)
1. 🔲 **Step 7.1**: Create comprehensive unit tests for normalization system:
   - Test normalization formula with various max scales
   - Test edge cases (zero points, max points, scale changes)
   - Document exact calculations being tested
2. 🔲 **Step 7.2**: Create comprehensive unit tests for DRAFT_ORDER bonus system:
   - Test round assignment algorithm with various roster compositions
   - Test current round determination logic
   - Test bonus point calculations for each position
   - Verify roster composition always aligns with DRAFT_ORDER expectations
3. 🔲 **Step 7.3**: Create comprehensive unit tests for matchup multiplier system:
   - Test rank difference calculations with all multiplier ranges
   - Test position filtering (QB/WR/RB/TE vs K/DEF)
   - Test edge cases and boundary conditions
4. 🔲 **Step 7.4**: Create comprehensive unit tests for each scoring mode:
   - Add to Roster: full 7-step calculation with detailed logging
   - Waiver Optimizer: verify same as Add to Roster minus DRAFT_ORDER
   - Trade Simulator: verify same as Waiver Optimizer
   - Starter Helper: verify 3-step calculation with injury filtering
5. 🔲 **Step 7.5**: Update existing tests to match new scoring behavior
6. 🔲 **Step 7.6**: Run complete test suite validation (100% pass rate required)
7. 🔲 **Step 7.7**: Execute full integration testing protocol

### **Phase 8: Documentation and Finalization**
1. 🔲 **Step 8.1**: Update all README files with new scoring explanations
2. 🔲 **Step 8.2**: Update CLAUDE.md with new architecture details
3. 🔲 **Step 8.3**: Update configuration documentation
4. 🔲 **Step 8.4**: Create new Draft_Helper_Data_Usage_Report.md
5. 🔲 **Step 8.5**: Update rules files if needed
6. 🔲 **Step 8.6**: Move scoring_overhaul.txt to done folder

## 📝 Context Notes

### **Key Decisions Made** (Based on User Clarifications):
- **Normalization Scale**: 0-N scale where N is configurable (default: 100). Formula: (player_points / max_player_points) * N
- **DRAFT_ORDER Values**: Static point values starting at 50 for #1 positions, configurable in simulation ranges
- **Matchup System**: Only for Starter Helper, formula: (Opponent_Defense_Rank - Player_Team_Offense_Rank)
  - Ranges: <-15=0.8x, -15 to -6=0.9x, -5 to 5=1.0x, 6 to 15=1.1x, 15+=1.2x
- **Positional Need**: Complete removal, not just behind toggle
- **Round Assignment**: Order doesn't matter, just fill slots based on position matches
- **Injury Filtering**: Starter Helper zeros out non-ACTIVE/QUESTIONABLE players completely
- **Multiplier Caps**: Remove MIN/MAX_TOTAL_ADJUSTMENT for ALL systems
- **Backwards Compatibility**: Clean break acceptable, no migration needed

### **Technical Approach**:
- **Modular Design**: Separate scoring methods for each mode
- **Enhanced Logging**: Extensive logging for all new scoring calculations (as requested)
- **Configuration-Driven**: All new parameters in simulation config with validation
- **Liberal Unit Testing**: Comprehensive test coverage with detailed documentation (as requested)
- **No Feature Flags**: Direct implementation step-by-step (as requested)
- **Clean Break**: No backwards compatibility concerns (as confirmed)

### **Files Requiring Modification**:
- `draft_helper/core/scoring_engine.py` (major overhaul)
- `draft_helper/draft_helper_config.py` (DRAFT_ORDER update, syntax fix)
- `draft_helper/simulation/config.py` (new parameters)
- `draft_helper/FantasyTeam.py` (round tracking system)
- All test files (updates to match new behavior)
- Documentation files (README, CLAUDE.md)

### **Dependencies**:
- Enhanced scoring system (existing, maintain integration)
- ADP and Player Ranking systems (existing, maintain integration)
- Team ranking system (existing, maintain integration)
- Bye week and injury penalty systems (existing, maintain behavior)

## 📅 Session History
### Session 1 (2025-09-29)
- **Completed**: Analysis and TODO file creation
- **Notes**: Identified all requirements from scoring_overhaul.txt and rules.txt
- **Next**: Begin Phase 1 analysis and create backup branch

## 🔄 Pre-Commit Validation Protocol
**🚨 MANDATORY FOR EVERY SINGLE STEP COMPLETION** - Execute full pre-commit validation checklist after EVERY step, not just phases:

### **WHEN TO EXECUTE**:
- ✅ After completing ANY individual step (e.g., Step 1.1, Step 2.3, Step 4.1, etc.)
- ✅ Before moving to the next step
- ✅ At any point when code changes are made
- ✅ When instructed to "validate and commit" or "commit changes"

### **MANDATORY EXECUTION STEPS** (for every single step):
1. **Copy validation checklist**: `cp tests/pre_commit_validation_checklist.md tests/temp_commit_checklist.md`
2. **Execute ALL 7 validation steps systematically**:
   - Step 1: Analyze ALL changed files (git status, git diff)
   - Step 2: Add unit tests for new functionality with proper mocking
   - Step 3: Run entire repository test suite (100% pass rate required)
   - Step 4: Execute startup validation (player data fetcher, NFL scores fetcher)
   - Step 5: Execute full integration testing (all 23 draft helper validation steps)
   - Step 6: Update documentation as needed
   - Step 7: Commit with proper format (no icons/Claude references)
3. **Cleanup temporary files**: `rm tests/temp_commit_checklist.md`

**CRITICAL**: No individual step can be considered complete without 100% validation success. This applies to EVERY step, not just phase completions.

**FAILURE PROTOCOL**: If ANY validation step fails, STOP immediately, fix the issue, and restart validation from Step 1 before proceeding to the next step.

## 📈 Progress Tracking
- **Total Steps**: 46 discrete tasks across 8 phases
- **Pre-Commit Validations**: REQUIRED after every single step (46 total validations minimum)
- **Estimated Effort**: Multi-session undertaking requiring careful coordination
- **Current Status**: Phase 1 planning complete, ready to begin implementation
- **Session Continuation**: This TODO file enables seamless continuation across Claude sessions

---

**STEP-BY-STEP VALIDATION REQUIREMENT**:
- Every ✅ marked step MUST have completed full pre-commit validation
- Document any validation failures and their resolutions in session notes
- No step can be marked complete without 100% test pass rate

**IMPORTANT**: Keep this file updated with progress after each completed step. Mark completed steps with ✅ and add session notes for context preservation.