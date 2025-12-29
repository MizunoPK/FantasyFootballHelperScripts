# Sub-Feature 7: DraftedRosterManager Consolidation

## Objective
Consolidate DraftedRosterManager functionality into PlayerManager (eliminates 680+ lines of fuzzy matching code).

## Dependencies
**Prerequisites:** Sub-feature 1 (Core Data Loading)
**Blocks:** None

## Scope (12 items)
- NEW-124 to NEW-135: DraftedRosterManager consolidation

**From checklist:**
- NEW-124: Add get_players_by_team() method to PlayerManager
- NEW-125: Add comprehensive docstrings
- NEW-126: Add error handling
- NEW-127: Remove DraftedRosterManager import from TradeSimulatorModeManager
- NEW-128: Simplify _initialize_team_data() method
- NEW-129: Update docstrings in TradeSimulatorModeManager
- NEW-130 to NEW-131: Add deprecation warnings to DraftedRosterManager
- NEW-132 to NEW-135: Testing

## Key Implementation

**90% of DraftedRosterManager becomes obsolete** - JSON drafted_by field eliminates need for fuzzy matching.

**Add to PlayerManager:**
```python
def get_players_by_team(self) -> Dict[str, List[FantasyPlayer]]:
    """Organize players by their fantasy team."""
    teams = {}
    for player in self.all_players:
        if player.drafted_by:  # Non-empty = drafted
            if player.drafted_by not in teams:
                teams[player.drafted_by] = []
            teams[player.drafted_by].append(player)
    return teams
```

**Update TradeSimulatorModeManager (lines 209-219):**
```python
# OLD:
drafted_data_csv = self.data_folder / 'drafted_data.csv'
roster_manager = DraftedRosterManager(str(drafted_data_csv), Constants.FANTASY_TEAM_NAME)
if roster_manager.load_drafted_data():
    self.team_rosters = roster_manager.get_players_by_team(all_players)

# NEW:
self.team_rosters = self.player_manager.get_players_by_team()
```

## Success Criteria
- [ ] 3 roster methods added to PlayerManager
- [ ] TradeSimulatorModeManager updated (2 files)
- [ ] DraftedRosterManager marked deprecated
- [ ] Trade analysis working with new approach

See `research/DRAFTED_ROSTER_MANAGER_ANALYSIS.md` for complete analysis.

---

## Verification Findings (From Deep Dive)

**Codebase Locations Verified:**

1. **PlayerManager (league_helper/util/PlayerManager.py)**
   - Module structure: lines 1-50
   - Class documentation follows Google Style (lines 1-31)
   - Logging pattern: get_logger() from utils.LoggingManager (line 47)
   - **Ready for:** Adding get_players_by_team() method (~10 lines)

2. **TradeSimulatorModeManager (league_helper/trade_simulator_mode/TradeSimulatorModeManager.py)**
   - Class definition: line 67
   - DraftedRosterManager import: line 45 (TO BE REMOVED)
   - Class docstring: lines 68-88 (references drafted_data.csv - TO BE UPDATED)
   - _initialize_team_data() method: lines 200-224
   - Current code at lines 209-219 matches checklist OLD code exactly
   - **Pattern:** Direct replacement of DraftedRosterManager with PlayerManager.get_players_by_team()

3. **DraftedRosterManager (utils/DraftedRosterManager.py)**
   - Module docstring: lines 1-20 (TO BE UPDATED with deprecation notice)
   - Class definition: lines 34-60
   - **Action:** Add module-level deprecation notice and method-level warnings
   - **Import needed:** `import warnings` for DeprecationWarning

4. **Test Files Verified:**
   - tests/league_helper/util/test_PlayerManager_scoring.py (exists - add new test class)
   - tests/league_helper/trade_simulator_mode/test_trade_simulator.py (exists - add new test class)
   - tests/integration/ (directory exists - add new integration test)
   - tests/utils/test_DraftedRosterManager.py (exists - add deprecation notice)

**Implementation Approach:**

1. **Phase 1:** Add get_players_by_team() to PlayerManager
   - Simple dictionary grouping pattern (standard Python)
   - Filter on `player.drafted_by` (non-empty = drafted)
   - ~10 lines total
   - Google Style docstring with examples

2. **Phase 2:** Update TradeSimulatorModeManager
   - Remove line 45 import
   - Replace lines 209-219 with single line: `self.team_rosters = self.player_manager.get_players_by_team()`
   - Update class docstring to reference JSON drafted_by field instead of CSV

3. **Phase 3:** Deprecate DraftedRosterManager
   - Add module-level deprecation notice (lines 1-20)
   - Add warnings.warn() calls in __init__, load_drafted_data, apply_drafted_state_to_players, get_players_by_team
   - Keep file for backward compatibility (player-data-fetcher uses it)

4. **Phase 4:** Testing
   - Add TestPlayerManagerRosterMethods class to test_PlayerManager_scoring.py
   - Add TestTradeSimulatorRosterIntegration class to test_trade_simulator.py
   - Add test_trade_simulator_json_roster_loading() to test_league_helper_integration.py
   - Add deprecation notice to test_DraftedRosterManager.py

**Complexity Assessment:**
- **Risk:** LOW - Simple code changes, single caller to update
- **Lines Changed:** ~30 lines of new code, ~10 lines removed, ~680 lines marked obsolete
- **Testing:** 4 new test classes/functions required (comprehensive coverage)

**No User Decisions Required** - All items are implementation tasks with clear specifications.
