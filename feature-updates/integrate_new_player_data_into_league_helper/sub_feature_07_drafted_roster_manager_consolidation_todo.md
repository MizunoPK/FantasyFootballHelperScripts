# Sub-Feature 7: DraftedRosterManager Consolidation - Implementation TODO

---

## 📖 Guide Reminder

**This file is governed by:** `feature-updates/guides/todo_creation_guide.md`

**Ready for implementation when:** ALL 24 iterations complete (see guide lines 87-93)

**DO NOT proceed to implementation until:**
- [ ] All 24 iterations executed individually
- [ ] Iteration 4a passed (TODO Specification Audit)
- [ ] Iteration 23a passed (Pre-Implementation Spec Audit - 4 parts)
- [ ] Iteration 24 passed (Implementation Readiness Checklist)
- [ ] Interface verification complete (copy-pasted signatures verified)
- [ ] No "Alternative:" or "May need to..." notes remain in TODO

⚠️ **If you think verification is complete, re-read guide lines 87-93 FIRST!**

⚠️ **Do NOT offer user choice to "proceed to implementation OR continue verification" - you MUST complete all 24 iterations**

---

## Iteration Progress Tracker

### Compact View (Quick Status)

```
R1: □□□□□□□ (0/7)   R2: □□□□□□□□□ (0/9)   R3: □□□□□□□□ (0/8)
```
Legend: ■ = complete, □ = pending, ▣ = in progress

**Current:** Iteration 1 (Standard Verification - Round 1)
**Confidence:** MEDIUM (needs interface verification)
**Blockers:** None

### Detailed View

| Round | Iterations | Status |
|-------|------------|--------|
| First (7) | [ ]1 [ ]2 [ ]3 [ ]4 [ ]5 [ ]6 [ ]7 | 0/7 |
| Second (9) | [ ]8 [ ]9 [ ]10 [ ]11 [ ]12 [ ]13 [ ]14 [ ]15 [ ]16 | 0/9 |
| Third (8) | [ ]17 [ ]18 [ ]19 [ ]20 [ ]21 [ ]22 [ ]23 [ ]24 | 0/8 |

**Current Iteration:** 1

---

## Protocol Execution Tracker

Track which protocols have been executed (protocols must be run at specified iterations):

| Protocol | Required Iterations | Completed |
|----------|---------------------|-----------|
| Standard Verification | 1, 2, 3, 8, 9, 10, 15, 16 | [ ]1 [ ]2 [ ]3 [ ]8 [ ]9 [ ]10 [ ]15 [ ]16 |
| Algorithm Traceability | 4, 11, 19 | [ ]4 [ ]11 [ ]19 |
| TODO Specification Audit | 4a | [ ]4a |
| End-to-End Data Flow | 5, 12 | [ ]5 [ ]12 |
| Skeptical Re-verification | 6, 13, 22 | [ ]6 [ ]13 [ ]22 |
| Integration Gap Check | 7, 14, 23 | [ ]7 [ ]14 [ ]23 |
| Fresh Eyes Review | 17, 18 | [ ]17 [ ]18 |
| Edge Case Verification | 20 | [ ]20 |
| Test Coverage Planning + Mock Audit | 21 | [ ]21 |
| Pre-Implementation Spec Audit | 23a | [ ]23a |
| Implementation Readiness | 24 | [ ]24 |
| Interface Verification | Pre-impl | [ ] |

---

## Verification Summary

- Iterations completed: 0/24 (IN PROGRESS: Iteration 1)
- Requirements from spec: 12 (NEW-124 through NEW-135)
- Requirements in TODO: 12
- Questions for user: 0 (spec complete, no user decisions required)
- Integration points identified: 3 (to be verified)

---

## 🚨 CRITICAL FINDINGS (Iteration 1)

### Finding 1: Interface Assumption Violation - player.drafted_by Does Not Exist

**Discovered During:** Iteration 1 (Standard Verification - Files and Patterns)
**Severity:** CRITICAL - Blocked implementation as originally specified
**Status:** ✅ RESOLVED - Field added to FantasyPlayer, all tests passing (2415/2415)

**Problem:**
The spec (lines 29-38) and research analysis (DRAFTED_ROSTER_MANAGER_ANALYSIS.md:180) assume `player.drafted_by` attribute exists in FantasyPlayer dataclass. **This attribute does NOT exist.**

**Evidence:**
1. **FantasyPlayer.py:96** - Only field is `drafted: int = 0` (0=not drafted, 1=opponent, 2=our team)
2. **FantasyPlayer.py:80-131** - Complete dataclass definition has NO `drafted_by` field
3. **FantasyPlayer.from_json():238-245** - Converts `drafted_by` (string from JSON) to `drafted` (int), **discarding team name**
4. **Spec code (line 33)**: `if player.drafted_by:` ← WRONG, this attribute doesn't exist
5. **TODO Task 1.1 (line 104)**: `if player.drafted_by:` ← WRONG, this attribute doesn't exist

**Impact:**
- **Data Loss**: JSON has `drafted_by="Team Alpha"` → FantasyPlayer only stores `drafted=1`, losing team name
- **Cannot Implement get_players_by_team()**: Need team names to return `Dict[team_name, List[FantasyPlayer]]`
- **TradeSimulatorModeManager.py:218**: Requires `team_name` to create TradeSimTeam objects - needs actual names, not int flags
- **Sub-feature 7 blocked**: Cannot proceed with current spec implementation

**Root Cause:**
Sub-feature 1 (Core Data Loading) implemented `FantasyPlayer.from_json()` to convert `drafted_by` string → `drafted` int, following the pattern from `from_dict()`. This conversion loses opponent team names.

**Solution Options:**

**Option A (RECOMMENDED):** Add `drafted_by: str = ""` field to FantasyPlayer
- **Pros**: Simple, keeps both `drafted` (int) for backward compat AND `drafted_by` (str) for team organization
- **Cons**: Adds one field to dataclass
- **Changes Required**:
  1. Add `drafted_by: str = ""` after line 96 in FantasyPlayer.py
  2. Modify `FantasyPlayer.from_json()` to populate BOTH `drafted` AND `drafted_by`
  3. Update `PlayerManager.update_players_file()` to use `drafted_by` directly
  4. Update Sub-feature 7 TODO to use `player.drafted_by` (currently correct in spec)
- **Impact**: ~10 lines changed in FantasyPlayer.py, existing code unaffected

**Option B:** PlayerManager maintains separate `Dict[int, str]` mapping player IDs to team names
- **Pros**: No FantasyPlayer changes
- **Cons**: Fragmented data, more complex, awkward API
- **Changes Required**: Add `self._drafted_by_map: Dict[int, str]` to PlayerManager
- **Impact**: More complex implementation, harder to maintain

**Option C:** Remove `drafted` field, use only `drafted_by` string
- **Pros**: Single source of truth
- **Cons**: BREAKING CHANGE for existing code checking `if player.drafted == 2`
- **Changes Required**: Search entire codebase for `player.drafted` access, replace with string checks
- **Impact**: HIGH RISK - affects multiple modules

**RESOLUTION (2025-12-29):**

✅ **FIXED:** Added `drafted_by: str = ""` field to FantasyPlayer dataclass
✅ **UPDATED:** FantasyPlayer.from_json() populates BOTH drafted (int) AND drafted_by (str)
✅ **UPDATED:** FantasyPlayer.from_dict() populates both fields for CSV compatibility
✅ **UPDATED:** PlayerManager.update_players_file() uses drafted_by with backward compatibility fallback
✅ **TESTS:** All 2415 tests passing (100%)

**Changes Made:**
- utils/FantasyPlayer.py:97 - Added `drafted_by: str = ""` field
- utils/FantasyPlayer.py:167 - from_dict() populates drafted_by
- utils/FantasyPlayer.py:274 - from_json() populates drafted_by (keeps both fields)
- league_helper/util/PlayerManager.py:515-526 - update_players_file() handles both fields with backward compatibility

**Lesson Learned:**
- Added comprehensive lesson (Lesson 3) to lessons_learned.md
- Documents traceability failure: notes mentioned drafted_by but no NEW-X requirement created
- Recommends guide updates to prevent this pattern in future

**Sub-feature 7 can now proceed** - Interface verified, spec code is correct

---

## Phase 1: Add Roster Methods to PlayerManager

### Task 1.1: Add get_players_by_team() method (NEW-124)
- **File:** `league_helper/util/PlayerManager.py`
- **Location:** After existing methods (around line 880+)
- **Spec Reference:** Lines 29-38
- **Tests:** `tests/league_helper/util/test_PlayerManager_scoring.py`
- **Status:** [ ] Not started

**Implementation details:**
```python
def get_players_by_team(self) -> Dict[str, List[FantasyPlayer]]:
    """
    Organize players by their fantasy team.

    Returns dict of {team_name: [player1, player2, ...]} for all drafted players.
    Players with empty drafted_by field are excluded (not drafted).

    Returns:
        Dict[str, List[FantasyPlayer]]: Dictionary mapping team names to player lists
    """
    teams = {}
    for player in self.all_players:
        if player.drafted_by:  # Non-empty = drafted
            if player.drafted_by not in teams:
                teams[player.drafted_by] = []
            teams[player.drafted_by].append(player)
    return teams
```

**Acceptance Criteria:**
- [ ] Method signature matches exactly (return type Dict[str, List[FantasyPlayer]])
- [ ] Filters on player.drafted_by (non-empty string = drafted)
- [ ] Returns dictionary with team names as keys
- [ ] Excludes players where drafted_by is empty string
- [ ] Google Style docstring with examples
- [ ] Unit test verifies correct grouping

### Task 1.2: Add comprehensive docstrings (NEW-125)
- **File:** `league_helper/util/PlayerManager.py`
- **Status:** [ ] Not started

**Implementation details:**
- Add Returns section describing dict structure
- Add example usage showing how to iterate results
- Document that empty drafted_by = not drafted
- Include note about FANTASY_TEAM_NAME constant for user's team

**Acceptance Criteria:**
- [ ] Google Style docstring complete
- [ ] Returns section describes dict[str, list] structure
- [ ] Examples show iteration pattern
- [ ] Edge cases documented (empty drafted_by)

### Task 1.3: Add error handling (NEW-126)
- **File:** `league_helper/util/PlayerManager.py`
- **Status:** [ ] Not started

**Implementation details:**
- Graceful handling if self.all_players is None or empty
- Return empty dict {} instead of crashing
- Log warning if no players loaded

**Acceptance Criteria:**
- [ ] Returns empty dict if all_players is None
- [ ] Returns empty dict if all_players is empty list
- [ ] No crashes on edge cases
- [ ] Warning logged if no players available

### QA CHECKPOINT 1: PlayerManager Methods Added
- **Status:** [ ] Not started
- **Expected outcome:** PlayerManager has get_players_by_team() method working correctly
- **Test command:** `python -m pytest tests/league_helper/util/test_PlayerManager_scoring.py::TestPlayerManagerRosterMethods -v`
- **Verify:**
  - [ ] Unit tests pass
  - [ ] Method returns correct dict structure
  - [ ] Filters drafted players correctly
  - [ ] Edge cases handled (empty all_players)
- **If checkpoint fails:** STOP, fix issue, document in lessons learned, then re-run

---

## Phase 2: Update TradeSimulatorModeManager

### Task 2.1: Remove DraftedRosterManager import (NEW-127)
- **File:** `league_helper/trade_simulator_mode/TradeSimulatorModeManager.py`
- **Location:** Line 45
- **Status:** [ ] Not started

**Implementation details:**
- Remove line 45: `from utils.DraftedRosterManager import DraftedRosterManager`
- Verify no other imports of DraftedRosterManager in file

**Acceptance Criteria:**
- [ ] Line 45 removed
- [ ] No other DraftedRosterManager imports remain
- [ ] File still imports correctly after removal

### Task 2.2: Simplify _initialize_team_data() method (NEW-128)
- **File:** `league_helper/trade_simulator_mode/TradeSimulatorModeManager.py`
- **Location:** Lines 209-219 (method at lines 200-224)
- **Spec Reference:** Lines 40-50
- **Status:** [ ] Not started

**Implementation details:**
OLD CODE (lines 209-219):
```python
drafted_data_csv = self.data_folder / 'drafted_data.csv'
roster_manager = DraftedRosterManager(str(drafted_data_csv), Constants.FANTASY_TEAM_NAME)
if roster_manager.load_drafted_data():
    self.team_rosters = roster_manager.get_players_by_team(all_players)
```

NEW CODE (single line):
```python
self.team_rosters = self.player_manager.get_players_by_team()
```

**Acceptance Criteria:**
- [ ] Lines 209-219 replaced with single line
- [ ] Uses self.player_manager.get_players_by_team()
- [ ] No reference to drafted_data.csv
- [ ] No DraftedRosterManager instantiation
- [ ] self.team_rosters assigned correctly

### Task 2.3: Update docstrings in TradeSimulatorModeManager (NEW-129)
- **File:** `league_helper/trade_simulator_mode/TradeSimulatorModeManager.py`
- **Location:** Class docstring (lines 68-88)
- **Status:** [ ] Not started

**Implementation details:**
- Update docstring to reference JSON drafted_by field instead of drafted_data.csv
- Remove CSV file path references
- Update method docstrings if they mention DraftedRosterManager

**Acceptance Criteria:**
- [ ] Class docstring updated (no CSV references)
- [ ] References JSON drafted_by field
- [ ] Method docstrings updated if needed
- [ ] Consistent with new approach

### QA CHECKPOINT 2: TradeSimulatorModeManager Updated
- **Status:** [ ] Not started
- **Expected outcome:** Trade simulator uses PlayerManager for roster organization
- **Test command:** `python -m pytest tests/league_helper/trade_simulator_mode/test_trade_simulator.py::TestTradeSimulatorRosterIntegration -v`
- **Verify:**
  - [ ] Unit tests pass
  - [ ] Trade simulator loads rosters correctly
  - [ ] No references to DraftedRosterManager
  - [ ] No references to drafted_data.csv
- **If checkpoint fails:** STOP, fix issue, document in lessons learned, then re-run

---

## Phase 3: Deprecate DraftedRosterManager

### Task 3.1: Add module-level deprecation notice (NEW-130)
- **File:** `utils/DraftedRosterManager.py`
- **Location:** Lines 1-20 (module docstring)
- **Status:** [ ] Not started

**Implementation details:**
Add comprehensive deprecation notice to module docstring:
```python
"""
Drafted Roster Manager

⚠️ DEPRECATED - DO NOT USE IN NEW CODE ⚠️

This module has been DEPRECATED as of Sub-Feature 7 (DraftedRosterManager Consolidation).
All functionality has been consolidated into PlayerManager.get_players_by_team().

MIGRATION PATH:
===============
Old Code (DEPRECATED):
    from utils.DraftedRosterManager import DraftedRosterManager
    roster_manager = DraftedRosterManager(drafted_csv, FANTASY_TEAM_NAME)
    if roster_manager.load_drafted_data():
        teams = roster_manager.get_players_by_team(all_players)

New Code (USE THIS):
    teams = player_manager.get_players_by_team()
    # Returns: {team_name: [player1, player2, ...]}

REASON FOR DEPRECATION:
=======================
- JSON drafted_by field eliminates need for separate CSV file
- PlayerManager already loads drafted_by data
- Eliminates 680+ lines of fuzzy matching code
- Simpler, faster, more maintainable

BACKWARD COMPATIBILITY:
=======================
This file remains for compatibility with player-data-fetcher module.
League Helper should NOT use this class.
"""
```

**Acceptance Criteria:**
- [ ] Module docstring updated with full deprecation notice
- [ ] Migration path documented
- [ ] Reason for deprecation explained
- [ ] Backward compatibility note added

### Task 3.2: Add DeprecationWarning to methods (NEW-131)
- **File:** `utils/DraftedRosterManager.py`
- **Location:** Key methods (__init__, load_drafted_data, get_players_by_team)
- **Status:** [ ] Not started

**Implementation details:**
- Add `import warnings` at top of file
- Add warnings.warn() calls in __init__, load_drafted_data, get_players_by_team, apply_drafted_state_to_players
- Example:
```python
def __init__(self, drafted_data_csv: str, fantasy_team_name: str):
    warnings.warn(
        "DraftedRosterManager is deprecated. Use PlayerManager.get_players_by_team() instead.",
        DeprecationWarning,
        stacklevel=2
    )
    # ... existing code ...
```

**Acceptance Criteria:**
- [ ] warnings module imported
- [ ] DeprecationWarning in __init__
- [ ] DeprecationWarning in load_drafted_data
- [ ] DeprecationWarning in get_players_by_team
- [ ] DeprecationWarning in apply_drafted_state_to_players
- [ ] stacklevel=2 for correct caller identification

### QA CHECKPOINT 3: Deprecation Complete
- **Status:** [ ] Not started
- **Expected outcome:** DraftedRosterManager shows deprecation warnings
- **Test command:** `python -c "from utils.DraftedRosterManager import DraftedRosterManager; DraftedRosterManager('test.csv', 'Team')"`
- **Verify:**
  - [ ] DeprecationWarning displayed
  - [ ] File still functional (backward compatibility)
  - [ ] Warning message clear and actionable
- **If checkpoint fails:** STOP, fix issue, document in lessons learned, then re-run

---

## Phase 4: Testing

### Task 4.1: Add TestPlayerManagerRosterMethods class (NEW-132)
- **File:** `tests/league_helper/util/test_PlayerManager_scoring.py`
- **Location:** New class at end of file
- **Status:** [ ] Not started

**Implementation details:**
- Test get_players_by_team() with various scenarios:
  - Players with drafted_by set
  - Players with empty drafted_by (should be excluded)
  - Multiple teams
  - Single team
  - No players drafted (empty dict)
- Use mock player objects with drafted_by field
- Verify dict structure and contents

**Acceptance Criteria:**
- [ ] TestPlayerManagerRosterMethods class added
- [ ] Tests drafted players grouped correctly
- [ ] Tests undrafted players excluded
- [ ] Tests multiple teams handled
- [ ] Tests edge case: no players drafted
- [ ] Tests edge case: all_players None/empty
- [ ] All tests pass

### Task 4.2: Add TestTradeSimulatorRosterIntegration class (NEW-133)
- **File:** `tests/league_helper/trade_simulator_mode/test_trade_simulator.py`
- **Location:** New class
- **Status:** [ ] Not started

**Implementation details:**
- Test TradeSimulatorModeManager uses PlayerManager.get_players_by_team()
- Mock PlayerManager with get_players_by_team() method
- Verify team_rosters populated correctly
- Test that DraftedRosterManager is NOT instantiated

**Acceptance Criteria:**
- [ ] TestTradeSimulatorRosterIntegration class added
- [ ] Mocks PlayerManager correctly
- [ ] Tests team_rosters assignment
- [ ] Tests DraftedRosterManager not used
- [ ] All tests pass

### Task 4.3: Add integration test (NEW-134)
- **File:** `tests/integration/test_league_helper_integration.py`
- **Location:** New test function
- **Status:** [ ] Not started

**Implementation details:**
- Add test_trade_simulator_json_roster_loading() function
- Test full flow: JSON data → PlayerManager → TradeSimulatorModeManager
- Verify rosters loaded from JSON drafted_by field (not CSV)
- Use real PlayerManager (not mock)

**Acceptance Criteria:**
- [ ] test_trade_simulator_json_roster_loading() added
- [ ] Uses real PlayerManager with JSON data
- [ ] Verifies rosters loaded correctly
- [ ] No CSV file access
- [ ] Test passes

### Task 4.4: Add deprecation notice to DraftedRosterManager tests (NEW-135)
- **File:** `tests/utils/test_DraftedRosterManager.py`
- **Location:** Module docstring
- **Status:** [ ] Not started

**Implementation details:**
- Add note to module docstring explaining tests remain for backward compatibility
- Explain that League Helper should NOT use DraftedRosterManager
- Keep tests functional (don't delete)

**Acceptance Criteria:**
- [ ] Deprecation note added to test file
- [ ] Explains tests remain for compatibility
- [ ] Tests still pass (not deleted)

### QA CHECKPOINT 4: All Tests Pass
- **Status:** [ ] Not started
- **Expected outcome:** Full test suite passes with new roster approach
- **Test command:** `python tests/run_all_tests.py`
- **Verify:**
  - [ ] All unit tests pass (100%)
  - [ ] All integration tests pass
  - [ ] New tests for roster methods pass
  - [ ] Trade simulator tests pass
  - [ ] No regressions detected
- **If checkpoint fails:** STOP, fix issue, document in lessons learned, then re-run

---

## Interface Contracts (To Be Verified Pre-Implementation)

### PlayerManager
- **Method:** `get_players_by_team(self) -> Dict[str, List[FantasyPlayer]]`
- **Source:** NEW METHOD - to be added
- **Verified:** [ ] (verify during Interface Verification Protocol)

### FantasyPlayer
- **Attribute:** `drafted_by` - Fantasy team name (empty string = not drafted)
- **Type:** str
- **Source:** `utils/FantasyPlayer.py` or `league_helper/util/FantasyPlayer.py`
- **Note:** Empty string means not drafted, non-empty means drafted
- **Verified:** [ ] (verify actual attribute exists and semantics)

### TradeSimulatorModeManager
- **Attribute:** `player_manager` - PlayerManager instance
- **Type:** PlayerManager
- **Source:** `league_helper/trade_simulator_mode/TradeSimulatorModeManager.py`
- **Existing usage:** Throughout class methods
- **Verified:** [ ] (verify self.player_manager exists)

### Quick E2E Validation Plan
- **Minimal test command:**
  ```python
  from league_helper.util.PlayerManager import PlayerManager
  from pathlib import Path
  pm = PlayerManager(config, Path('data'))
  pm.load_players_from_json()
  teams = pm.get_players_by_team()
  print(f"Teams: {list(teams.keys())}")
  ```
- **Expected result:** Dict with team names as keys, player lists as values
- **Run before:** Full implementation begins
- **Status:** [ ] Not run | [ ] Passed | [ ] Failed (fix before proceeding)

---

## Integration Matrix

| New Component | File | Called By | Caller File:Line | Caller Modification Task |
|---------------|------|-----------|------------------|--------------------------|
| get_players_by_team() | PlayerManager.py | _initialize_team_data() | TradeSimulatorModeManager.py:209-219 | Task 2.2 |

---

## Algorithm Traceability Matrix

(To be populated during Iteration 4)

| Spec Section | Algorithm Description | Code Location | Conditional Logic |
|--------------|----------------------|---------------|-------------------|
| Lines 32-36 | Filter players by drafted_by field | PlayerManager.py:get_players_by_team() | if player.drafted_by |
| Lines 29-37 | Group players into dict by team | PlayerManager.py:get_players_by_team() | Dictionary accumulation |
| Lines 40-50 | Replace DraftedRosterManager with PlayerManager call | TradeSimulatorModeManager.py:209-219 | Direct replacement |

---

## Data Flow Traces

(To be populated during Iteration 5)

### Requirement: Trade Simulator Roster Loading
```
Entry: run_league_helper.py (trade simulator mode)
  → LeagueHelperManager.run()
  → TradeSimulatorModeManager.__init__()
  → TradeSimulatorModeManager._initialize_team_data()
  → PlayerManager.get_players_by_team()  ← NEW
  → Output: self.team_rosters populated
```

---

## Verification Gaps

Document any gaps found during iterations here:

(None yet - will be populated during iterations 1-24)

---

## Skeptical Re-verification Results

### Round 1 (Iteration 6)
- **Status:** Not yet executed
- **Verified correct:** (to be filled)
- **Corrections made:** (to be filled)
- **Confidence level:** (to be assessed)

### Round 2 (Iteration 13)
- **Status:** Not yet executed

### Round 3 (Iteration 22)
- **Status:** Not yet executed

---

## Progress Notes

Keep this section updated for session continuity:

**Last Updated:** 2025-12-28 (TODO creation started)
**Current Status:** Draft TODO created, starting Round 1 verification (Iteration 1)
**Next Steps:** Execute Standard Verification (Iteration 1) - verify files exist, patterns correct
**Blockers:** None - ready to begin iterations
