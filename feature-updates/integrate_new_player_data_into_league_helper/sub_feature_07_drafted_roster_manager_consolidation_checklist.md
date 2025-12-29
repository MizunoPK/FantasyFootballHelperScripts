# Sub-Feature 7: DraftedRosterManager Consolidation - Checklist

> **IMPORTANT**: When marking items as resolved, also update `sub_feature_07_drafted_roster_manager_consolidation_spec.md`
> with full implementation details. The checklist tracks status; the specs file is
> the implementation specification.

---

## Progress Summary

**Total Items:** 12
**Completed:** 12 (all verified ✅)
**Remaining:** 0

**Status:** Phase 1 (Targeted Research) complete - all implementation items verified against codebase

---

## Analysis & Strategy (1 item - RESOLVED)

- [x] **NEW-42:** Confirm DraftedRosterManager is IN SCOPE ✅ RESOLVED
  - **Decision:** IN SCOPE - Major simplification opportunity
  - **Approach:** Add 3 roster organization methods to PlayerManager (not create new file)
  - **Finding:** 90% of DraftedRosterManager code (680+ lines) becomes obsolete with JSON drafted_by field
  - **Rationale:** Complex fuzzy matching no longer needed - data already correct in JSON
  - **Impact:** TradeSimulatorModeManager needs update, DraftedRosterManager deprecated
  - **Benefit:** Much simpler code, natural location for methods, no CSV dependency
  - **See:** DRAFTED_ROSTER_MANAGER_ANALYSIS.md for complete details

---

## Phase 1: Add Methods to PlayerManager (3 items)

- [x] **NEW-124:** Add get_players_by_team() method to PlayerManager ✅ VERIFIED
  - **Purpose:** Get all players grouped by fantasy team
  - **Signature:** `def get_players_by_team(self) -> Dict[str, List[FantasyPlayer]]`
  - **Returns:** Dictionary mapping team name → list of players on that team
  - **Logic:** Filter players with non-empty drafted_by field, group by team name
  - **File:** league_helper/util/PlayerManager.py (~10 lines)
  - **Implementation:**
    ```python
    def get_players_by_team(self) -> Dict[str, List[FantasyPlayer]]:
        """
        Get all players grouped by their fantasy team.

        Returns:
            Dict mapping team name to list of players on that team.
            Empty string keys are excluded (undrafted players).
        """
        teams = {}
        for player in self.players:
            if player.drafted_by:  # Non-empty = drafted
                if player.drafted_by not in teams:
                    teams[player.drafted_by] = []
                teams[player.drafted_by].append(player)
        return teams
    ```
  - **Verified:** PlayerManager class structure confirmed at league_helper/util/PlayerManager.py:1-50
  - **Pattern:** Standard dictionary grouping pattern used throughout codebase
- [x] **NEW-125:** Add comprehensive docstrings to new PlayerManager methods ✅ VERIFIED
  - **Document:** That this replaces DraftedRosterManager functionality
  - **Explain:** drafted_by field usage and filtering logic
  - **Provide:** Usage examples for each method
  - **Note:** No fuzzy matching needed (data already correct)
  - **File:** league_helper/util/PlayerManager.py
  - **Verified:** Existing PlayerManager docstrings follow Google Style (lines 1-31)
  - **Pattern:** See PlayerManager module docstring for comprehensive examples
- [x] **NEW-126:** Add error handling to new PlayerManager methods ✅ VERIFIED
  - **Handle:** Empty player lists (return empty dict, no error)
  - **Handle:** None values in drafted_by (treat as "" - undrafted)
  - **Log:** Warnings for unexpected states (if any discovered)
  - **File:** league_helper/util/PlayerManager.py
  - **Verified:** Standard error handling pattern confirmed throughout PlayerManager
  - **Pattern:** Use get_logger() from utils.LoggingManager (imported at line 47)

---

## Phase 2: Update Trade Simulator (3 items)

- [x] **NEW-127:** Remove DraftedRosterManager import from TradeSimulatorModeManager ✅ VERIFIED
  - **Line:** trade_simulator_mode/TradeSimulatorModeManager.py:45
  - **OLD:** `from utils.DraftedRosterManager import DraftedRosterManager`
  - **REMOVE:** This import entirely
  - **NEW:** No new import needed (already has PlayerManager reference)
  - **File:** league_helper/trade_simulator_mode/TradeSimulatorModeManager.py
  - **Verified:** Import exists at line 45 exactly as specified
- [x] **NEW-128:** Simplify _initialize_team_data() method ✅ VERIFIED
  - **Lines:** trade_simulator_mode/TradeSimulatorModeManager.py:209-219
  - **OLD:**
    ```python
    # Load drafted_data.csv via DraftedRosterManager
    roster_manager = DraftedRosterManager(self.data_folder)
    roster_manager.load_drafted_data()
    self.team_rosters = roster_manager.get_players_by_team()
    ```
  - **NEW:**
    ```python
    # Get team rosters directly from PlayerManager (uses drafted_by field)
    self.team_rosters = self.player_manager.get_players_by_team()
    ```
  - **Remove:** Lines about loading drafted_data.csv
  - **Remove:** DraftedRosterManager instantiation
  - **Simpler:** Just one line instead of fuzzy matching logic
  - **File:** league_helper/trade_simulator_mode/TradeSimulatorModeManager.py
  - **Verified:** Current code at lines 209-219 matches OLD code exactly
  - **Pattern:** Direct method call replaces CSV loading and fuzzy matching
- [x] **NEW-129:** Update docstrings in TradeSimulatorModeManager ✅ VERIFIED
  - **Lines:** trade_simulator_mode/TradeSimulatorModeManager.py:68-88
  - **OLD:** References loading drafted_data.csv (line 77: "data_folder (Path): Path to data directory containing drafted_data.csv")
  - **NEW:** Explain using drafted_by field from JSON data via PlayerManager
  - **Document:** No more CSV dependency, simpler approach
  - **File:** league_helper/trade_simulator_mode/TradeSimulatorModeManager.py
  - **Verified:** Class docstring at lines 68-88 references drafted_data.csv

---

## Phase 3: Deprecate Old Code (2 items)

- [x] **NEW-130:** Add deprecation warning to DraftedRosterManager ✅ VERIFIED
  - **File:** utils/DraftedRosterManager.py:1-20 (module docstring at top)
  - **Action:** Add DEPRECATED notice with migration instructions
  - **Format:**
    ```python
    """
    DEPRECATED: This module is deprecated as of [date].

    Use PlayerManager methods instead:
    - PlayerManager.get_players_by_team() - replaces get_players_by_team()
    - PlayerManager.get_all_team_names() - replaces get_all_team_names()
    - PlayerManager.get_team_stats() - replaces get_team_stats()

    Reason: JSON drafted_by field eliminates need for complex fuzzy matching
    against drafted_data.csv. PlayerManager already has all player data.

    90% of this class (680+ lines of fuzzy matching) is now obsolete.
    """
    ```
  - **Keep file:** For player-data-fetcher compatibility (out of scope module)
  - **Future:** Remove in separate cleanup feature (Sub-feature 8 or later)
  - **Verified:** Current module docstring at utils/DraftedRosterManager.py:1-20
  - **Pattern:** Standard Python deprecation notice format
- [x] **NEW-131:** Add deprecation warnings to DraftedRosterManager methods ✅ VERIFIED
  - **Methods:** __init__, load_drafted_data, apply_drafted_state_to_players, get_players_by_team
  - **Action:** Log deprecation warnings directing users to PlayerManager methods
  - **Format:** `warnings.warn("DraftedRosterManager.load_drafted_data() is deprecated. Use PlayerManager.get_players_by_team() instead.", DeprecationWarning)`
  - **File:** utils/DraftedRosterManager.py
  - **Verified:** Class structure confirmed at utils/DraftedRosterManager.py:34-60
  - **Pattern:** Use Python warnings module (needs import: `import warnings`)

---

## Phase 4: Testing (4 items)

- [x] **NEW-132:** Add tests for new PlayerManager roster methods ✅ VERIFIED
  - **File:** tests/league_helper/util/test_PlayerManager_scoring.py (add new test class)
  - Test get_players_by_team() with various scenarios:
    - Multiple teams with players
    - Single team
    - No drafted players (empty dict)
    - All players on one team
    - Player with empty drafted_by (excluded from results)
  - Test handling of None values in drafted_by (treat as undrafted)
  - Verify correct grouping and filtering
  - Test with realistic team names ("Sea Sharp", "Fishoutawater", etc.)
  - **Verified:** Test file exists at tests/league_helper/util/test_PlayerManager_scoring.py
  - **Pattern:** Add new test class TestPlayerManagerRosterMethods following existing structure
- [x] **NEW-133:** Test TradeSimulatorModeManager with new PlayerManager methods ✅ VERIFIED
  - **File:** tests/league_helper/trade_simulator_mode/test_trade_simulator.py (add new test class)
  - Verify _initialize_team_data() works with PlayerManager.get_players_by_team()
  - Verify team_rosters populated correctly (Dict[str, List[FantasyPlayer]])
  - Verify all team names captured
  - Test with various roster configurations:
    - Multiple teams with different roster sizes
    - User team ("Sea Sharp") vs opponent teams
    - Empty teams (no players drafted)
  - **Verified:** Test file exists at tests/league_helper/trade_simulator_mode/test_trade_simulator.py
  - **Pattern:** Add new test class TestTradeSimulatorRosterIntegration following existing structure
- [x] **NEW-134:** Integration test - Trade Simulator workflow ✅ VERIFIED
  - **File:** tests/integration/test_league_helper_integration.py (add new test)
  - Load players from JSON (with drafted_by values set)
  - Initialize Trade Simulator mode
  - Verify team rosters organized correctly via PlayerManager
  - Verify trade analysis works with new approach
  - Execute sample trade and verify calculations
  - Compare results with old DraftedRosterManager approach (validation)
  - **Verified:** Integration test directory exists at tests/integration/
  - **Pattern:** Add test_trade_simulator_json_roster_loading() following existing integration test patterns
- [x] **NEW-135:** Mark DraftedRosterManager tests as deprecated ✅ VERIFIED
  - **File:** tests/utils/test_DraftedRosterManager.py
  - Add deprecation notices to test file
  - Keep tests passing for backward compatibility (out-of-scope modules may use)
  - Add comment: "These tests maintained for compatibility. Use PlayerManager tests instead."
  - Document that PlayerManager methods should be tested going forward
  - **Verified:** Test file exists at tests/utils/test_DraftedRosterManager.py
  - **Pattern:** Add module docstring deprecation notice at top of file

---

## Success Criteria

✅ **3 roster organization methods added to PlayerManager**
✅ **TradeSimulatorModeManager uses PlayerManager methods (not DraftedRosterManager)**
✅ **DraftedRosterManager marked as deprecated**
✅ **All unit tests passing (100%)**
✅ **Integration tests verify Trade Simulator workflow unchanged**
✅ **~680 lines of fuzzy matching code obsolete**
✅ **No CSV dependency for roster organization**

---

## Dependencies

**Prerequisites:**
- Sub-feature 1 complete (drafted_by field loaded from JSON, players in PlayerManager)

**Uses:**
- drafted_by field (from Decision 2 - stores team name as string)
- PlayerManager.players list (all players with drafted_by values)

---

## Impact Analysis

**Files Modified:** 2
- league_helper/util/PlayerManager.py (add 3 roster organization methods)
- league_helper/trade_simulator_mode/TradeSimulatorModeManager.py (remove DraftedRosterManager, simplify _initialize_team_data)

**Files Deprecated:** 1
- utils/DraftedRosterManager.py (~711 lines - mark deprecated, keep for out-of-scope compatibility)

**Data Files Affected:**
- drafted_data.csv (no longer loaded or used)

**Complexity Reduction:**
- DraftedRosterManager: 711 lines with complex fuzzy matching
- New approach: ~10 lines in PlayerManager (simple filtering and grouping)
- **Savings:** ~680 lines of obsolete code

**Risk:** LOW
- Simple filtering logic
- Natural location (PlayerManager already has all player data)
- Only 1 caller to update (TradeSimulatorModeManager)
- Simpler code = fewer bugs

**Benefits:**
- No fuzzy matching needed (data already correct in JSON)
- No CSV dependency (single source of truth: JSON)
- Natural location (PlayerManager has player data)
- Simpler code (easier to maintain)
- Eliminates entire class (reduced complexity)

---

## Why This Works

**OLD Approach (DraftedRosterManager):**
1. Load drafted_data.csv (player names + team names)
2. Load players.csv (player stats)
3. Fuzzy match names between files (complex, error-prone)
4. Handle name mismatches (680+ lines of logic)
5. Build team rosters dictionary

**NEW Approach (PlayerManager):**
1. Load JSON files (already have drafted_by field)
2. Filter players where drafted_by != ""
3. Group by drafted_by value
4. Done! (~10 lines)

**Key Insight:** JSON drafted_by field eliminates need for fuzzy matching.

---

## Notes

- See DRAFTED_ROSTER_MANAGER_ANALYSIS.md for complete analysis
- 90% of DraftedRosterManager becomes obsolete with JSON drafted_by field
- Natural consolidation - PlayerManager is the right place for these methods
- Keep DraftedRosterManager file for out-of-scope module compatibility
- Remove DraftedRosterManager entirely in Sub-feature 8 or later cleanup feature
