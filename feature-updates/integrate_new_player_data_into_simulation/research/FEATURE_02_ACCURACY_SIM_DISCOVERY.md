# Feature 02: Accuracy Simulation JSON Verification - Discovery Findings

**Research Date:** 2026-01-03
**Researcher:** Agent
**Grounded In:** Epic Intent (user's explicit requests)

---

## Epic Intent Summary

**User requested:** Update Accuracy Sim to use JSON player data, verify correctness, remove CSV references

**Components user mentioned:**
- Accuracy Sim (epic line 2, 3)
- players.csv / players_projected.csv (epic line 4) - Remove references
- week_X folders with JSON files (epic line 5)
- drafted_by, locked, projected_points, actual_points fields (epic line 6)
- Week 17 logic verification (epic line 8)

**This research focused on user-mentioned components ONLY.**

---

## Key Architectural Difference from Win Rate Sim

**CRITICAL FINDING:** Accuracy Sim uses a **fundamentally different data loading approach** than Win Rate Sim:

- **Win Rate Sim:** Direct JSON parsing (`_parse_players_json()` method in SimulatedLeague.py)
- **Accuracy Sim:** Uses **PlayerManager** from league_helper (which already migrated to JSON)

**Implication:** Accuracy Sim does NOT need to parse JSON directly. It delegates to PlayerManager, which loads JSON via `load_players_from_json()`.

---

## Components Identified

### Component 1: AccuracySimulationManager (Core Orchestration)

**User mentioned:** "Accuracy Sim" (epic line 2, 3)

**Found in codebase:**
- File: `simulation/accuracy/AccuracySimulationManager.py`
- Class definition: Line 57
- Key method: `_create_player_manager()` at lines 339-404

**Method signature (actual from source):**
```python
def _create_player_manager(
    self,
    config_dict: dict,
    week_data_path: Path,
    season_path: Path
) -> PlayerManager:
    """
    Create a PlayerManager with the given configuration.

    Args:
        config_dict: Configuration dictionary
        week_data_path: Path to week folder containing position JSON files
        season_path: Path to season folder containing season_schedule.csv, team_data/

    Returns:
        PlayerManager: Configured player manager
    """
```

**How it works today:**
1. Creates temporary directory with tempfile.mkdtemp() (line 359)
2. Creates `player_data/` subfolder (lines 362-363)
3. **Copies 6 JSON files** from week folder to player_data/ (lines 365-373):
   - qb_data.json, rb_data.json, wr_data.json, te_data.json, k_data.json, dst_data.json
4. Copies season_schedule.csv, game_data.csv, team_data/ from season folder
5. Creates PlayerManager instance (line 399)
6. PlayerManager loads JSON files via `load_players_from_json()` (not shown in this file)

**Relevance to this feature:**
- **Already uses JSON** (not CSV)
- User wants to verify this is correct (epic line 10: "ASSUME INCORRECT, VERIFY EVERYTHING")
- Need to verify JSON file copying is correct
- Need to verify PlayerManager loads JSON correctly in simulation context

---

### Component 2: Week_N+1 Logic (_load_season_data)

**User mentioned:** "use the week_17 folders...look at...week_18 folders" (epic line 8)

**Found implementation:**
- File: `simulation/accuracy/AccuracySimulationManager.py`
- Lines: 293-337
- Method: `_load_season_data()`

**Code structure (actual):**
```python
def _load_season_data(
    self,
    season_path: Path,
    week_num: int
) -> Tuple[Optional[Path], Optional[Path]]:
    """
    Load data paths for a specific week in a season.

    For accuracy calculations, we need TWO week folders:
    - week_N folder: Contains projected_points for week N
    - week_N+1 folder: Contains actual_points for week N

    This is because week_N folder represents data "as of" week N's start,
    so week N's actual results aren't known until week N+1.
    """
    # Week N folder for projections
    projected_folder = season_path / "weeks" / f"week_{week_num:02d}"

    # Week N+1 folder for actuals
    # For week 1: use week_02, for week 17: use week_18
    actual_week_num = week_num + 1
    actual_folder = season_path / "weeks" / f"week_{actual_week_num:02d}"

    # Both folders must exist
    if not projected_folder.exists():
        self.logger.warning(f"Projected folder not found: {projected_folder}")
        return None, None

    if not actual_folder.exists():
        self.logger.warning(f"Actual folder not found: {actual_folder}")
        return None, None

    return projected_folder, actual_folder
```

**Pattern observed:**
- For week N: loads week_N folder (projected) and week_N+1 folder (actual)
- For week 17 specifically: loads week_17 folder (projected) and week_18 folder (actual)
- **This already implements the user's requested Week 17 logic!**

**Verification needed:**
- Confirm week_18 folder exists with real week 17 data
- Confirm this pattern is used correctly in _evaluate_config_weekly()

---

### Component 3: Two-PlayerManager Pattern (_evaluate_config_weekly)

**User mentioned:** "This means we'll likely need two Player Managers - one for the N week and one for the N+1 week" (epic line 8)

**Found implementation:**
- File: `simulation/accuracy/AccuracySimulationManager.py`
- Lines: 412-533
- Method: `_evaluate_config_weekly()`

**Code structure (actual from lines 441-505):**
```python
# Create TWO player managers:
# 1. projected_mgr (from week_N folder) for projections
# 2. actual_mgr (from week_N+1 folder) for actuals
projected_mgr = self._create_player_manager(config_dict, projected_path, season_path)
actual_mgr = self._create_player_manager(config_dict, actual_path, season_path)

try:
    projections = {}
    actuals = {}

    # Get projections from week_N folder (projected_mgr)
    for player in projected_mgr.players:
        scored = projected_mgr.score_player(
            player,
            use_weekly_projection=True,
            # ... scoring flags ...
        )
        if scored:
            projections[player.id] = scored.projected_points

    # Get actuals from week_N+1 folder (actual_mgr)
    # week_N+1 has actual_points[N-1] populated (week N complete)
    for player in actual_mgr.players:
        # Get actual points for this specific week (from actual_points array)
        # Array index: week 1 = index 0, week N = index N-1
        if 1 <= week_num <= 17 and len(player.actual_points) >= week_num:
            actual = player.actual_points[week_num - 1]
            if actual is not None and actual > 0:
                actuals[player.id] = actual

finally:
    self._cleanup_player_manager(projected_mgr)
    self._cleanup_player_manager(actual_mgr)
```

**Pattern observed:**
- Creates TWO PlayerManagers per week (exactly as user anticipated)
- Projected manager: from week_N folder → calculates scored projected_points
- Actual manager: from week_N+1 folder → extracts actual_points[week_num - 1] from array
- **This already implements the two-manager pattern user mentioned!**

**Critical line (486):**
```python
actual = player.actual_points[week_num - 1]
```

**Verification needed:**
- Confirm array indexing is correct (week 1 = index 0, week 17 = index 16)
- Confirm week_N+1 folder has actual_points[week_num - 1] populated
- Confirm Week 17 specifically: week_18 folder has actual_points[16] populated

---

### Component 4: PlayerManager (Delegated JSON Loading)

**User mentioned:** "json files" (epic line 5), "player_data folder with positional json files" (epic line 1)

**Found in codebase:**
- File: `league_helper/util/PlayerManager.py` (NOT in simulation folder)
- Already migrated to JSON (per epic notes line 1: "recent effort updated the league helper")
- Method: `load_players_from_json()` (not shown in this research - already verified in league_helper)

**How Accuracy Sim uses it:**
1. Copies JSON files from week folder to temp `player_data/` directory
2. Creates PlayerManager instance with temp directory path
3. PlayerManager automatically loads JSON files from player_data/
4. Accuracy Sim accesses loaded players via `player_mgr.players`

**Relevance to this feature:**
- Accuracy Sim does NOT parse JSON directly
- Delegates to PlayerManager (which is already JSON-aware)
- Different from Win Rate Sim (which has direct parsing)

---

## CSV References Found

**Search conducted:** `grep -r "players.csv\|players_projected.csv" simulation/accuracy/`

**Results:** NO references to players.csv or players_projected.csv found

**CSV references that DO exist (and are fine):**
- `import csv` - Python library (line 22, AccuracySimulationManager.py)
- `season_schedule.csv` - Season schedule file (lines 375-378)
- `game_data.csv` - Game data file (lines 380-383)

**Conclusion:** Accuracy Sim does NOT load players.csv or players_projected.csv. Uses JSON only.

---

## Existing Test Patterns

**Found test pattern in:** `tests/integration/test_accuracy_simulation_integration.py`

**Pattern observed:**
- Creates mock historical season with JSON files (lines 58-100)
- Helper function `build_points_array()` creates 17-element arrays (lines 96-100)
- Tests JSON-based workflow (not CSV)
- Tests week_N+1 logic implicitly

**Test coverage verification needed:**
- Does test cover Week 17 specifically?
- Does test verify array extraction correctness?
- Does test verify two-manager pattern?

---

## Edge Cases Identified

**From reading existing code:**

1. **Missing JSON file** → How handled?
   - Line 370-373: Logs warning if position file missing
   - Continues processing (doesn't crash)
   - Need to verify this is correct behavior

2. **Missing week_N+1 folder** → How handled?
   - Lines 330-335: Logs warning if actual_folder missing
   - Returns (None, None)
   - Calling code skips this week (line 438-439)
   - Need to verify this is correct behavior (should Week 17 have this fallback?)

3. **actual_points array bounds** → How handled?
   - Line 485: Checks `len(player.actual_points) >= week_num`
   - Only uses actual if array is long enough
   - Need to verify this is correct (should it default to 0.0 like Win Rate Sim?)

---

## Research Completeness

**Components researched:**
- ✅ AccuracySimulationManager class (READ source code lines 1-890)
- ✅ _create_player_manager() method (READ lines 339-404)
- ✅ _load_season_data() method (READ lines 293-337)
- ✅ _evaluate_config_weekly() method (READ lines 412-533)
- ✅ CSV reference search (grep for CSV files)
- ✅ Test patterns (READ test file lines 1-100)

**Evidence collected:**
- File paths: simulation/accuracy/AccuracySimulationManager.py, ParallelAccuracyRunner.py, tests/integration/test_accuracy_simulation_integration.py
- Line numbers: All key methods documented with line ranges
- Actual code snippets: Copied method signatures and key logic

**Ready for Phase 1.5 audit.**

---

**Next Steps:**
- Phase 1.5: Verify research completeness (MANDATORY GATE)
- STAGE_2b Phase 2: Update spec.md with findings and create requirements
- STAGE_2c Phase 3: Interactive question resolution (determine what to verify vs assume correct)
