# Move Player Rating to League Config

## Objective

Reclassify PLAYER_RATING_SCORING from a week-specific prediction parameter to a base draft strategy parameter by:
1. Moving it from WEEK_SPECIFIC_PARAMS to BASE_CONFIG_PARAMS in ResultsManager
2. Adding it to win-rate simulation's PARAMETER_ORDER
3. Ensuring config files reflect the new structure (league_config.json has it, week*.json don't)

---

## High-Level Requirements

### 1. Parameter List Updates
- **ResultsManager.py (lines 255-265)**: Remove PLAYER_RATING_SCORING from WEEK_SPECIFIC_PARAMS
- **ResultsManager.py (lines 239-252)**: Add PLAYER_RATING_SCORING to BASE_CONFIG_PARAMS
- **run_win_rate_simulation.py (lines 54-63)**: Add PLAYER_RATING_SCORING_WEIGHT to PARAMETER_ORDER

### 2. Config File Structure (Automatic via Save Logic)
Once PLAYER_RATING_SCORING is in BASE_CONFIG_PARAMS:
- **Win-rate simulation saves**: Will automatically put it in league_config.json (uses _extract_base_params)
- **Accuracy simulation saves**: Will automatically exclude it from week*.json (uses _extract_week_params)
- **Existing configs**: Will be updated when win-rate sim runs and saves next optimal config

### 3. No Changes Needed to League Helper
- **ConfigManager**: Already loads from both league_config.json AND horizon files
- **Merge logic**: Week/draft configs override base params (line 968: `self.parameters.update(prediction_params)`)
- **Result**: ConfigManager will find PLAYER_RATING_SCORING in league_config.json, works same as before

---

## Resolved Implementation Details

### Current State Analysis

**File Locations:**
- `simulation/shared/ResultsManager.py`:
  - Line 239-252: BASE_CONFIG_PARAMS list (12 parameters)
  - Line 255-265: WEEK_SPECIFIC_PARAMS list (9 parameters, including PLAYER_RATING_SCORING)
  - Line 267-288: _extract_base_params() - filters to BASE_CONFIG_PARAMS
  - Line 290-311: _extract_week_params() - filters to WEEK_SPECIFIC_PARAMS

**Why PLAYER_RATING_SCORING Should Move:**
1. **Usage Pattern**:
   - AddToRosterModeManager line 285: `player_rating=True` (ONLY mode that uses it)
   - StarterHelperModeManager line 409: `player_rating=False` (weekly mode disables it)
   - TradeSimTeam lines 98, 110, 117: Uses it for season predictions, not weekly

2. **Current Optimization**:
   - Win-rate PARAMETER_ORDER (run_win_rate_simulation.py lines 54-63): Does NOT include PLAYER_RATING
   - Accuracy PARAMETER_ORDER (run_accuracy_simulation.py lines 79-96): Does NOT include PLAYER_RATING
   - **Result**: Parameter is defined but NOT optimized by either simulation!

3. **Config Structure**:
   - data/configs/league_config.json: Does NOT contain PLAYER_RATING_SCORING
   - data/configs/week1-5.json line 6-18: HAS PLAYER_RATING_SCORING
   - **Problem**: Wrong location for a draft-only parameter

### How ConfigManager Loads Configs

**Loading Flow** (ConfigManager._load_config, lines 901-976):
1. Load `league_config.json` into `self.parameters`
2. Extract CURRENT_NFL_WEEK from base params
3. If `use_draft_config=True` (Add to Roster Mode):
   - Load `draft_config.json` parameters
4. If `use_draft_config=False` (other modes):
   - Load week-specific config (week1-5.json, etc.)
5. Merge prediction params over base: `self.parameters.update(prediction_params)` (line 968)

**Key Insight**: ConfigManager checks both locations and merges. Moving PLAYER_RATING_SCORING to league_config.json is safe because:
- Draft mode loads draft_config.json which can override if needed
- Weekly modes load week*.json which won't have it (correct - they don't use it)
- Fallback: If not in week config, league_config.json value is used

### Implementation Steps

**Step 1: Update ResultsManager.py**

Move PLAYER_RATING_SCORING from WEEK_SPECIFIC_PARAMS to BASE_CONFIG_PARAMS:

```python
# Line 239-252: Add PLAYER_RATING_SCORING here
BASE_CONFIG_PARAMS = [
    'CURRENT_NFL_WEEK',
    'NFL_SEASON',
    'NFL_SCORING_FORMAT',
    'SAME_POS_BYE_WEIGHT',
    'DIFF_POS_BYE_WEIGHT',
    'INJURY_PENALTIES',
    'DRAFT_ORDER_BONUSES',
    'DRAFT_ORDER_FILE',
    'DRAFT_ORDER',
    'MAX_POSITIONS',
    'FLEX_ELIGIBLE_POSITIONS',
    'ADP_SCORING',
    'PLAYER_RATING_SCORING'  # ← ADD THIS
]

# Line 255-265: Remove PLAYER_RATING_SCORING from here
WEEK_SPECIFIC_PARAMS = [
    'NORMALIZATION_MAX_SCALE',
    # 'PLAYER_RATING_SCORING',  # ← REMOVE THIS
    'TEAM_QUALITY_SCORING',
    'PERFORMANCE_SCORING',
    'MATCHUP_SCORING',
    'SCHEDULE_SCORING',
    'TEMPERATURE_SCORING',
    'WIND_SCORING',
    'LOCATION_MODIFIERS'
]
```

**Step 2: Update run_win_rate_simulation.py**

Add PLAYER_RATING_SCORING_WEIGHT to PARAMETER_ORDER (after line 62):

```python
# Line 54-63: Add PLAYER_RATING_SCORING_WEIGHT here
PARAMETER_ORDER = [
    # Bye Week Penalties
    'SAME_POS_BYE_WEIGHT',
    'DIFF_POS_BYE_WEIGHT',
    # Draft Order Bonuses
    'PRIMARY_BONUS',
    'SECONDARY_BONUS',
    # ADP Scoring
    'ADP_SCORING_WEIGHT',
    # Player Rating Scoring (used by draft mode)
    'PLAYER_RATING_SCORING_WEIGHT',  # ← ADD THIS
]
```

**Step 3: Verify ConfigGenerator**

No changes needed! ConfigGenerator already:
- Imports BASE_CONFIG_PARAMS and WEEK_SPECIFIC_PARAMS from ResultsManager (line 61-62)
- Has PLAYER_RATING_SCORING_WEIGHT in PARAM_DEFINITIONS (line 113)
- Has mapping from PLAYER_RATING_SCORING_WEIGHT → PLAYER_RATING_SCORING section (line 213)
- Generates test values for it (line 653)

Once ResultsManager is updated, ConfigGenerator automatically adapts.

**Step 4: Test Migration**

After changes, when win-rate simulation runs:
- Saves will use _extract_base_params which now includes PLAYER_RATING_SCORING
- league_config.json will contain PLAYER_RATING_SCORING
- week*.json will NOT contain it (correct)

---

## Implementation Notes

### Files to Modify
- `simulation/shared/ResultsManager.py` - Move PLAYER_RATING_SCORING between lists (2 line changes)
- `run_win_rate_simulation.py` - Add PLAYER_RATING_SCORING_WEIGHT to PARAMETER_ORDER (1 line add)

### Files That Auto-Adapt (No Changes Needed)
- `simulation/shared/ConfigGenerator.py` - Imports lists from ResultsManager
- `league_helper/util/ConfigManager.py` - Loads from both locations, merges correctly
- All mode managers - Use ConfigManager, don't care where param comes from

### Testing Strategy
1. **Unit tests**: Update tests that verify WEEK_SPECIFIC_PARAMS and BASE_CONFIG_PARAMS lists
2. **Integration test**: Run win-rate simulation, verify PLAYER_RATING_SCORING in league_config.json
3. **Draft mode test**: Run AddToRosterMode, verify it still loads PLAYER_RATING_SCORING correctly
4. **Weekly mode test**: Verify weekly modes don't try to use PLAYER_RATING_SCORING

### Migration Path for Existing Configs

**No manual migration needed!** When win-rate simulation runs next:
1. Loads existing optimal config (has PLAYER_RATING_SCORING in week files)
2. Uses it as baseline
3. Optimizes (now including PLAYER_RATING_SCORING_WEIGHT)
4. Saves new optimal config:
   - _extract_base_params() includes PLAYER_RATING_SCORING → goes to league_config.json
   - _extract_week_params() excludes PLAYER_RATING_SCORING → removed from week*.json

---

## Dependency Map

### Module Dependencies

```
┌──────────────────────────────────────────────────────────────────────┐
│ run_win_rate_simulation.py (entry point)                             │
│     │                                                                │
│     ▼                                                                │
│ SimulationManager (win_rate/SimulationManager.py)                    │
│     │                                                                │
│     ├──► ConfigGenerator (shared/ConfigGenerator.py)                 │
│     │         └──► ResultsManager.BASE_CONFIG_PARAMS (MODIFIED)      │
│     │         └──► ResultsManager.WEEK_SPECIFIC_PARAMS (MODIFIED)    │
│     │                                                                │
│     └──► ResultsManager (shared/ResultsManager.py)                   │
│               └──► _extract_base_params() (uses BASE_CONFIG_PARAMS)  │
│               └──► _extract_week_params() (uses WEEK_SPECIFIC_PARAMS)│
│                                                                      │
│ League Helper Modes (league_helper/)                                 │
│     │                                                                │
│     └──► ConfigManager (util/ConfigManager.py)                       │
│               └──► Loads league_config.json (base params)            │
│               └──► Loads draft_config.json or week*.json             │
│               └──► Merges prediction over base                       │
└──────────────────────────────────────────────────────────────────────┘
```

### Data Flow

```
Simulation Run:
   ▼
ConfigGenerator.generate_test_configs()
   ▼
SimulationManager.run_optimization()
   ▼
ResultsManager.save_optimal_configs_folder()
   ├──► _extract_base_params() → league_config.json (PLAYER_RATING_SCORING here)
   └──► _extract_week_params() → week*.json (PLAYER_RATING_SCORING NOT here)

League Helper Load:
   ▼
ConfigManager.__init__(use_draft_config=True for draft mode)
   ▼
_load_config()
   ├──► Load league_config.json (has PLAYER_RATING_SCORING)
   └──► Load draft_config.json (may override PLAYER_RATING_SCORING)
   ▼
parameters.update(draft_params)  # Merge
   ▼
_extract_parameters()  # Sets self.player_rating_scoring
   ▼
AddToRosterModeManager uses it for scoring
```

---

## Status: PLANNING - Ready for Checklist Resolution

All major questions resolved through codebase research. Next: populate checklist with detailed verification items.
