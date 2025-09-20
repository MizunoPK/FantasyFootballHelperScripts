# Shared Variables Consolidation TODO

## 🎯 **OBJECTIVE**
Move commonly used variables (NFL season, current week, etc.) from individual script config files to a centralized shared_variables file to ensure consistency across all scripts.

## 📋 **TASKS TO COMPLETE**

### Phase 1: Investigation and Planning ✅
- [x] **1.1** Read the objective from prompts/shared_variables_update.txt
- [x] **1.2** Search for CURRENT_NFL_WEEK and NFL_SEASON variables across codebase
- [x] **1.3** Identify all script config files that contain these variables
- [x] **1.4** Create this comprehensive TODO file with progress tracking

### Phase 2: Variable Discovery ✅
- [x] **2.1** Review all config files to identify variables for consolidation:
  - [x] `starter_helper/starter_helper_config.py`
  - [x] `player-data-fetcher/player_data_fetcher_config.py`
  - [x] `nfl-scores-fetcher/nfl_scores_fetcher_config.py`
  - [x] `draft_helper/draft_helper_config.py`
- [x] **2.2** Document exact variables found and their current values
- [x] **2.3** Confirm with user which variables to move before proceeding

**USER DECISION**: Consolidate 3 core variables only:
- CURRENT_NFL_WEEK (set to 3)
- NFL_SEASON (set to 2025)
- NFL_SCORING_FORMAT (set to "ppr")
- Keep position constants in individual configs
- Add to existing shared_config.py file

### Phase 3: Shared Variables File Setup ✅
- [x] **3.1** Update shared_config.py file in project root (used existing file)
- [x] **3.2** Add discovered variables with proper documentation
- [x] **3.3** Include validation logic for the shared variables (delegated to individual scripts)
- [x] **3.4** Add configuration comments and usage guidance

### Phase 4: Update Individual Config Files ✅
- [x] **4.1** Update starter_helper/starter_helper_config.py to import from shared_config
- [x] **4.2** Update player-data-fetcher/player_data_fetcher_config.py to import from shared_config
- [x] **4.3** Update nfl-scores-fetcher config to import from shared_config (with compatibility mapping)
- [x] **4.4** Draft helper doesn't use these variables (confirmed)
- [x] **4.5** Remove duplicate variable definitions from individual files

### Phase 5: Update Import Statements ✅
- [x] **5.1** All scripts automatically use new shared location through config imports
- [x] **5.2** Test files use config imports, so they automatically get shared variables
- [x] **5.3** Constants files updated to import from shared_config

### Phase 6: Testing and Validation ✅
- [x] **6.1** Run complete unit test suite - **ALL 241 TESTS PASS**
- [x] **6.2** Test each main script to verify functionality:
  - [x] run_player_data_fetcher.py (config import works)
  - [x] run_starter_helper.py (works correctly, shows week 3)
  - [x] run_draft_helper.py (works correctly)
  - [x] run_nfl_scores_fetcher.py (config import works, week now 3 instead of 2)
- [x] **6.3** No import errors or broken references found
- [x] **6.4** Existing unit tests continue to work (no new tests needed)

### Phase 7: Documentation Updates ✅
- [x] **7.1** Update README.md to reflect new shared variables location
- [x] **7.2** Update CLAUDE.md with new configuration guidance
- [x] **7.3** Individual module README files don't need changes (config-specific)
- [x] **7.4** Update configuration documentation in shared_config.py

### Phase 8: Final Verification ✅
- [x] **8.1** Final complete test suite run - **ALL 241 TESTS PASS**
- [x] **8.2** Functional testing of all main scripts - **ALL WORKING**
- [x] **8.3** Weekly update process simplified to single location
- [x] **8.4** No temporary files to clean up

---

## 📊 **VARIABLES DISCOVERED**

### ✅ **Core Variables to Consolidate (CONFIRMED)**:

1. **CURRENT_NFL_WEEK**: Found in multiple files - MUST consolidate
   - `starter_helper/starter_helper_config.py`: `CURRENT_NFL_WEEK = 3`
   - `player-data-fetcher/player_data_fetcher_config.py`: `CURRENT_NFL_WEEK = 3`
   - `nfl-scores-fetcher/nfl_scores_fetcher_config.py`: `NFL_SCORES_CURRENT_WEEK = 2` (different value!)
   - **Usage**: Weekly projections, lineup optimization, data fetching
   - **Critical**: This is THE most important variable to centralize for weekly updates

2. **NFL_SEASON**: Found in multiple files - SHOULD consolidate
   - `starter_helper/starter_helper_config.py`: `NFL_SEASON = 2025`
   - `player-data-fetcher/player_data_fetcher_config.py`: `NFL_SEASON = 2025`
   - `nfl-scores-fetcher/nfl_scores_fetcher_config.py`: `NFL_SCORES_SEASON = 2025`
   - **Usage**: ESPN API calls, data validation, file naming
   - **Changes**: Annually (start of each season)

3. **NFL_SCORING_FORMAT**: Found in multiple files - SHOULD consolidate
   - `starter_helper/starter_helper_config.py`: `NFL_SCORING_FORMAT = "ppr"`
   - `player-data-fetcher/player_data_fetcher_config.py`: `NFL_SCORING_FORMAT = "ppr"`
   - **Usage**: Fantasy points calculations, ESPN API configuration
   - **Changes**: Rarely (if league changes scoring system)

### 🤔 **Additional Variables to Consider**:

4. **Position Constants**: Found in multiple files - COULD consolidate
   - `starter_helper/starter_helper_config.py`: `RB, WR, QB, TE, K, DST, FLEX = 'RB', 'WR', 'QB', 'TE', 'K', 'DST', 'FLEX'`
   - `draft_helper/draft_helper_config.py`: `RB, WR, QB, TE, K, DST, FLEX = 'RB', 'WR', 'QB', 'TE', 'K', 'DST', 'FLEX'`
   - **Usage**: Position validation, lineup requirements
   - **Changes**: Never (standardized NFL positions)

5. **FLEX_ELIGIBLE_POSITIONS**: Found in multiple files - COULD consolidate
   - `starter_helper/starter_helper_config.py`: `FLEX_ELIGIBLE_POSITIONS = [RB, WR]`
   - `draft_helper/draft_helper_config.py`: `FLEX_ELIGIBLE_POSITIONS = [RB, WR]`
   - **Usage**: FLEX position validation
   - **Changes**: Never (league rule)

### ⚠️ **Issue Found**:
- **Week inconsistency**: NFL Scores Fetcher has `NFL_SCORES_CURRENT_WEEK = 2` while others have `CURRENT_NFL_WEEK = 3`
- **This proves the need for centralization!**

---

## 🔄 **PROGRESS TRACKING**
**Last Updated**: Task completed successfully
**Current Phase**: ✅ **COMPLETED** - All phases finished
**Final Status**: All objectives achieved with 100% test success rate

## ⚠️ **IMPORTANT NOTES**
- This TODO file should be updated with progress after each significant step
- New Claude agents should read this file first to understand current status
- All changes must maintain 100% unit test pass rate (241/241 tests)
- Weekly update process must remain simple and centralized
- Configuration validation must be preserved

## 🎯 **SUCCESS CRITERIA** ✅ **ALL ACHIEVED**
- [x] All NFL season and week variables centralized in shared_config.py
- [x] All 241 unit tests continue to pass
- [x] All 4 main scripts function correctly
- [x] Documentation updated to reflect new structure
- [x] Weekly update process is simplified (single location to update)

## 🏆 **FINAL ACHIEVEMENTS**
- **✅ Week Inconsistency Fixed**: NFL Scores Fetcher now uses week 3 (was 2) - unified with other scripts
- **✅ Single Update Location**: `CURRENT_NFL_WEEK` now updated in one place instead of 3+ locations
- **✅ Zero Regressions**: All 241 tests still pass after major config restructuring
- **✅ Improved Documentation**: Clear guidance on centralized weekly update process
- **✅ Backwards Compatibility**: NFL Scores Fetcher retains old variable names via mapping