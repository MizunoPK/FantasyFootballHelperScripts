# DraftedRosterManager Migration Analysis

**Date:** 2025-12-27
**Purpose:** Analyze DraftedRosterManager changes needed with drafted_by in JSON instead of drafted_data.csv

---

## Current State

### File: `utils/DraftedRosterManager.py` (711 lines)

**Purpose:** Manages drafted player data across fantasy teams

**Current Workflow:**
1. Load `drafted_data.csv` (format: "Player Name POS - TEAM", "Fantasy Team")
2. Normalize player names for fuzzy matching
3. Apply drafted state to FantasyPlayer objects (`.drafted = 0/1/2`)
4. Organize players by fantasy team

**Used By:**
- ✅ **League Helper:** `trade_simulator_mode/TradeSimulatorModeManager.py:209-214`
- ❌ **player-data-fetcher:** `player_data_exporter.py` (OUT OF SCOPE)

---

## Current Usage in Trade Simulator

**TradeSimulatorModeManager.py:209-214:**
```python
# Load drafted_data.csv
roster_manager = DraftedRosterManager(str(drafted_data_csv), Constants.FANTASY_TEAM_NAME)

if roster_manager.load_drafted_data():
    # Organize players by team using fuzzy matching
    self.team_rosters = roster_manager.get_players_by_team(all_players)

    self.logger.info(f"Organized players into {len(self.team_rosters)} team rosters")
```

**What it does:**
- Loads drafted_data.csv
- Fuzzy matches CSV entries to FantasyPlayer objects
- Returns `Dict[team_name, List[FantasyPlayer]]`

---

## New State (With JSON drafted_by)

### What Changes

**Before (CSV):**
- drafted_data.csv contains team assignments
- Need to fuzzy match CSV entries to players
- Apply `.drafted = 0/1/2` based on team

**After (JSON):**
- `drafted_by` field already in JSON player data
- Values: `""` (not drafted), `"Sea Sharp"` (user's team), `"Team Alpha"` (opponent)
- No matching needed - data is already correct

---

## Impact Analysis

### Methods in DraftedRosterManager

**OBSOLETE (no longer needed):**

1. ✅ **`load_drafted_data()`** (lines 65-124)
   - Purpose: Load and parse drafted_data.csv
   - **Replacement:** Data already loaded in JSON
   - **Action:** Can be removed

2. ✅ **`apply_drafted_state_to_players()`** (lines 211-263)
   - Purpose: Set `.drafted = 0/1/2` on players via fuzzy matching
   - **Line 255:** `matched_player.drafted = drafted_value` ← THE CRITICAL LINE
   - **Replacement:** `drafted_by` already set when loading JSON
   - **Action:** Can be removed

3. ✅ **`_normalize_player_info()`** (lines 302-334)
   - Purpose: Normalize strings for fuzzy matching
   - **Replacement:** Not needed (no fuzzy matching)
   - **Action:** Can be removed

4. ✅ **`_extract_player_components()`** (lines 336-382)
   - Purpose: Parse "Name POS - TEAM" format
   - **Replacement:** Not needed (no CSV parsing)
   - **Action:** Can be removed

5. ✅ **`_find_original_info_for_key()`** (lines 477-482)
   - Purpose: Map normalized key back to original CSV string
   - **Replacement:** Not needed (no CSV)
   - **Action:** Can be removed

6. ✅ **`_create_player_lookup()`** (lines 484-528)
   - Purpose: Build lookup indexes for fuzzy matching
   - **Replacement:** Not needed (no matching)
   - **Action:** Can be removed

7. ✅ **`_find_matching_player()`** (lines 530-591)
   - Purpose: Fuzzy match CSV entry to player
   - **Replacement:** Not needed (no matching)
   - **Action:** Can be removed

8. ✅ **`_find_defense_match()`** (lines 593-657)
   - Purpose: Special defense fuzzy matching
   - **Replacement:** Not needed (no matching)
   - **Action:** Can be removed

9. ✅ **`_validate_player_match()`** (lines 659-667)
   - Purpose: Validate fuzzy match results
   - **Replacement:** Not needed (no matching)
   - **Action:** Can be removed

10. ✅ **`_fuzzy_match_player()`** (lines 669-710)
    - Purpose: Fallback fuzzy matching with similarity scoring
    - **Replacement:** Not needed (no matching)
    - **Action:** Can be removed

11. ✅ **Helper methods for matching** (lines 384-475)
    - `_get_team_abbr_from_name()`, `_similarity_score()`, `_positions_equivalent()`,
      `_teams_equivalent()`, `_normalize_team_abbr()`, `_match_dst_by_team_abbr()`
    - **Replacement:** Not needed (no matching)
    - **Action:** Can be removed

**STILL USEFUL (can be simplified):**

1. ⚠️ **`get_players_by_team()`** (lines 154-209)
   - **Current:** Loads CSV, fuzzy matches, organizes by team (complex: 55 lines)
   - **New:** Just filter and group players by `drafted_by` field (simple: ~10 lines)
   - **Action:** SIMPLIFY drastically

2. ⚠️ **`get_team_name_for_player()`** (lines 265-296)
   - **Current:** Normalize player info, lookup in CSV dict (complex: 32 lines)
   - **New:** Just return `player.drafted_by` (trivial: 1 line)
   - **Action:** SIMPLIFY to one-liner

3. ✅ **`get_stats()`** (lines 126-143)
   - **Current:** Stats about loaded CSV data
   - **New:** Stats about players with `drafted_by != ""`
   - **Action:** SIMPLIFY (no CSV dependency)

4. ✅ **`get_all_team_names()`** (lines 145-152)
   - **Current:** Unique team names from CSV
   - **New:** Unique non-empty `drafted_by` values
   - **Action:** SIMPLIFY (no CSV dependency)

---

## Migration Options

### Option A: Deprecate Entire Class ✅ RECOMMENDED

**Approach:** Replace DraftedRosterManager with simple helper functions

**Rationale:**
- 90% of code becomes obsolete (fuzzy matching no longer needed)
- Remaining functionality is trivial (filtering/grouping)
- No need for a full class when simple functions suffice
- Cleaner, more maintainable code

**Replacement Implementation:**

```python
# Add to: league_helper/util/PlayerManager.py

def get_players_by_team(self) -> Dict[str, List[FantasyPlayer]]:
    """
    Organize players by their fantasy team.

    Returns:
        Dict[team_name, List[FantasyPlayer]] for all drafted players

    Note:
        Replaces DraftedRosterManager.get_players_by_team().
        Uses drafted_by field from JSON data (no CSV loading or fuzzy matching).
    """
    teams = {}
    for player in self.all_players:
        if player.drafted_by:  # Non-empty = drafted
            if player.drafted_by not in teams:
                teams[player.drafted_by] = []
            teams[player.drafted_by].append(player)
    return teams

def get_all_team_names(self) -> Set[str]:
    """
    Get set of all unique fantasy team names.

    Returns:
        Set of team names with drafted players
    """
    return {p.drafted_by for p in self.all_players if p.drafted_by}

def get_team_stats(self) -> Dict[str, int]:
    """
    Get statistics about drafted players.

    Returns:
        Dict with total_players, user_team_players, other_team_players
    """
    drafted_players = [p for p in self.all_players if p.drafted_by]
    user_team_count = sum(1 for p in drafted_players if p.drafted_by == self.my_team_name)

    return {
        "total_players": len(drafted_players),
        "user_team_players": user_team_count,
        "other_team_players": len(drafted_players) - user_team_count
    }
```

**Usage in TradeSimulatorModeManager:**

```python
# OLD (lines 206-219):
drafted_data_csv = self.data_folder / 'drafted_data.csv'
roster_manager = DraftedRosterManager(str(drafted_data_csv), Constants.FANTASY_TEAM_NAME)

if roster_manager.load_drafted_data():
    self.team_rosters = roster_manager.get_players_by_team(all_players)
else:
    self.logger.error("Failed to load drafted data")
    self.team_rosters = {}

# NEW (simplified):
# Players already have drafted_by from JSON - just organize them via PlayerManager
self.team_rosters = self.player_manager.get_players_by_team()
```

**Benefits:**
- ✅ Much simpler code (~30 lines vs 711 lines in DraftedRosterManager)
- ✅ No CSV dependency
- ✅ No fuzzy matching complexity
- ✅ Faster (no matching overhead)
- ✅ More maintainable
- ✅ Natural location (PlayerManager already manages players)
- ✅ No new file needed

**Drawbacks:**
- ⚠️ Breaking change for player-data-fetcher (out of scope anyway)
- ⚠️ Need to update TradeSimulatorModeManager call site

---

### Option B: Simplify Existing Class

**Approach:** Keep DraftedRosterManager but gut most methods

**Implementation:**

```python
class DraftedRosterManager:
    """
    DEPRECATED: Use roster_utils functions instead.

    Kept for backward compatibility during migration.
    Now just a thin wrapper around player.drafted_by field access.
    """

    def __init__(self, csv_path: str, my_team_name: str):
        """Initialize (csv_path ignored - for backward compatibility)."""
        self.my_team_name = my_team_name
        self.logger = get_logger()

    def load_drafted_data(self) -> bool:
        """DEPRECATED: Data already loaded from JSON. Returns True for compatibility."""
        self.logger.warning("load_drafted_data() is deprecated - data loaded from JSON")
        return True

    def get_players_by_team(self, players: List[FantasyPlayer]) -> Dict[str, List[FantasyPlayer]]:
        """Organize players by their fantasy team using drafted_by field."""
        teams = {}
        for player in players:
            if player.drafted_by:
                if player.drafted_by not in teams:
                    teams[player.drafted_by] = []
                teams[player.drafted_by].append(player)
        return teams

    def get_team_name_for_player(self, player: FantasyPlayer) -> str:
        """Get fantasy team name for a player."""
        return player.drafted_by

    # ... other methods removed
```

**Benefits:**
- ✅ Backward compatible (same interface)
- ✅ No changes to TradeSimulatorModeManager

**Drawbacks:**
- ⚠️ Technical debt (keeping unnecessary class)
- ⚠️ Misleading API (constructor takes csv_path but doesn't use it)
- ⚠️ Confusing (load_drafted_data() doesn't actually load anything)

---

## Recommendation

**Option A: Add Methods to PlayerManager** ✅

**Implementation Plan:**

1. **Add roster organization methods to PlayerManager**
2. **Update TradeSimulatorModeManager** to use PlayerManager methods
3. **Mark DraftedRosterManager as deprecated** (add deprecation warning)
4. **Update tests** to test new PlayerManager methods
5. **Document migration** in code comments

**Files to Update:**
- ✅ **UPDATE:** `league_helper/util/PlayerManager.py` (add 3 new methods, ~30 lines)
- ✅ **UPDATE:** `league_helper/trade_simulator_mode/TradeSimulatorModeManager.py` (lines 209-219)
- ⚠️ **DEPRECATE:** `utils/DraftedRosterManager.py` (mark as deprecated, remove in future)
- ✅ **UPDATE:** `tests/league_helper/util/test_PlayerManager.py` (add tests for new methods)

**Benefits:**
- Eliminates 680+ lines of obsolete code
- Much simpler, more maintainable
- Natural fit - PlayerManager already manages player organization
- No new file needed - methods go where they belong
- Clearer intent (no fuzzy matching confusion)
- Faster execution (no matching overhead)

---

## Breaking Changes

**For OUT OF SCOPE code (player-data-fetcher):**
- `player-data-fetcher/player_data_exporter.py` uses DraftedRosterManager
- Will need separate migration when player-data-fetcher is updated
- Not a concern for this feature (League Helper only)

**For IN SCOPE code (League Helper):**
- TradeSimulatorModeManager needs minor update (lines 209-219)
- Change from DraftedRosterManager to roster_utils functions
- Simpler, fewer lines of code

---

## Implementation Checklist (NEW-124 through NEW-135)

### Phase 1: Add Methods to PlayerManager (3 items)

- [ ] **NEW-124:** Add `get_players_by_team()` method to PlayerManager
  - Returns Dict[team_name, List[FantasyPlayer]]
  - Filters players by non-empty drafted_by field
  - Groups players by their fantasy team
  - **File:** league_helper/util/PlayerManager.py (~10 lines)

- [ ] **NEW-125:** Add comprehensive docstrings to new PlayerManager methods
  - Document that this replaces DraftedRosterManager functionality
  - Explain drafted_by field usage
  - Provide usage examples
  - **File:** league_helper/util/PlayerManager.py

- [ ] **NEW-126:** Add error handling to new PlayerManager methods
  - Handle empty player lists
  - Handle None values in drafted_by
  - Log warnings for unexpected states
  - **File:** league_helper/util/PlayerManager.py

### Phase 2: Update Trade Simulator (3 items)

- [ ] **NEW-127:** Remove DraftedRosterManager import from TradeSimulatorModeManager
  - **Line:** trade_simulator_mode/TradeSimulatorModeManager.py:45
  - **OLD:** `from utils.DraftedRosterManager import DraftedRosterManager`
  - **NEW:** No new import needed (already has PlayerManager)

- [ ] **NEW-128:** Simplify _initialize_team_data() method
  - **Lines:** trade_simulator_mode/TradeSimulatorModeManager.py:209-219
  - **OLD:** Create DraftedRosterManager, load CSV, call get_players_by_team()
  - **NEW:** Call self.player_manager.get_players_by_team() directly
  - **Remove:** Lines about loading drafted_data.csv and DraftedRosterManager instantiation

- [ ] **NEW-129:** Update docstrings in TradeSimulatorModeManager
  - **Lines:** trade_simulator_mode/TradeSimulatorModeManager.py:178-190
  - **OLD:** References loading drafted_data.csv and fuzzy matching
  - **NEW:** Explain using drafted_by field from JSON data via PlayerManager

### Phase 3: Deprecate Old Code (2 items)

- [ ] **NEW-130:** Add deprecation warning to DraftedRosterManager
  - **File:** utils/DraftedRosterManager.py:1-20 (module docstring)
  - **Action:** Add DEPRECATED notice with migration instructions
  - **Keep file:** For player-data-fetcher compatibility (out of scope)
  - **Future:** Remove in separate cleanup feature

- [ ] **NEW-131:** Add deprecation warnings to DraftedRosterManager methods
  - **Methods:** __init__, load_drafted_data, apply_drafted_state_to_players
  - **Action:** Log warnings directing users to PlayerManager methods
  - **File:** utils/DraftedRosterManager.py

### Phase 4: Testing (4 items)

- [ ] **NEW-132:** Add tests for new PlayerManager roster methods
  - **File:** tests/league_helper/util/test_PlayerManager.py
  - Test get_players_by_team() with various scenarios
  - Test handling of empty drafted_by values
  - Test with multiple teams and edge cases
  - Verify correct grouping and filtering

- [ ] **NEW-133:** Test TradeSimulatorModeManager with new PlayerManager methods
  - **File:** tests/league_helper/trade_simulator_mode/test_TradeSimulatorModeManager.py
  - Verify _initialize_team_data() works with PlayerManager methods
  - Verify team_rosters populated correctly
  - Verify all team names captured

- [ ] **NEW-134:** Integration test - Trade Simulator workflow
  - **File:** tests/integration/test_league_helper_integration.py
  - Load players from JSON (with drafted_by values)
  - Initialize Trade Simulator
  - Verify team rosters organized correctly via PlayerManager
  - Verify trade analysis works with new approach

- [ ] **NEW-135:** Mark DraftedRosterManager tests as deprecated
  - **File:** tests/utils/test_DraftedRosterManager.py
  - Add deprecation notices
  - Keep tests passing for backward compatibility
  - Document that PlayerManager methods should be used instead

---

## Summary

**Current:** 711-line class with complex fuzzy matching (90% obsolete)

**Recommended:** Add 3 simple methods to PlayerManager (~30 lines) using drafted_by field

**Impact:** 2 files to update in League Helper (PlayerManager, TradeSimulatorModeManager)

**Benefit:** Eliminates 680+ lines of obsolete code, much simpler and faster, methods in logical location

**Risk:** LOW (simple change, well-tested, clear migration path)
