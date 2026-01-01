# Feature 01: Fix Player-to-Round Assignment - Verified Interface Contracts

**Purpose:** Document ALL external interfaces verified from source code BEFORE implementation

**Verification Date:** 2025-12-31 18:00
**Stage:** 5b Step 1 (Interface Verification Protocol)

---

## Interface 1: ConfigManager.flex_eligible_positions

**Source:** league_helper/util/ConfigManager.py:221

**Type:** Instance attribute (List[str])

**Declaration:**
```python
self.flex_eligible_positions: List[str] = []
```

**Populated From:**
- Config file: league_config.json → FLEX_ELIGIBLE_POSITIONS
- Validated at startup (ConfigManager._load_config)
- Standard value: ["RB", "WR"]

**Usage in Our Code:**
- Task 1: Helper method `_position_matches_ideal()` will read this property
- Check: `if player_position in self.config.flex_eligible_positions:`

**Verified:** ✅ Interface matches TODO assumptions (List[str] attribute)

---

## Interface 2: ConfigManager.get_position_with_flex()

**Source:** league_helper/util/ConfigManager.py:313

**Signature:**
```python
def get_position_with_flex(self, position: str) -> str
```

**Parameters:**
- `position` (str): Player's natural position ("QB", "RB", "WR", "TE", "K", "DST")

**Returns:**
- str: "FLEX" if position in flex_eligible_positions, else original position
  - Example: "RB" → "FLEX" (if RB in flex_eligible_positions)
  - Example: "QB" → "QB" (QB not FLEX-eligible)

**Current Usage:**
- AddToRosterModeManager.py line 426 (BUGGY - will be REMOVED by Task 2)
- Other files may use (not affected by our change)

**Usage in Our Code:**
- Task 2: REMOVE call from line 426
- Will NOT be called by our new code (using helper method instead)

**Verified:** ✅ Interface correct - method exists and will be removed from one location

---

## Interface 3: ConfigManager.get_ideal_draft_position()

**Source:** league_helper/util/ConfigManager.py:683

**Signature:**
```python
def get_ideal_draft_position(self, round_num: int) -> str
```

**Parameters:**
- `round_num` (int): Draft round number (0-indexed)
  - Valid range: 0 to len(draft_order)-1
  - Typically: 0-14 (for 15-round draft)

**Returns:**
- str: PRIMARY position for this round
  - Returns "FLEX" if round_num is out of range
  - Example: Round 0 with {"RB": "P", "WR": "S"} → Returns "RB"

**Current Usage:**
- AddToRosterModeManager._match_players_to_rounds() (existing code, unchanged)
- Called before line 426 to get `ideal_position` variable

**Usage in Our Code:**
- UNCHANGED - Already used correctly in existing code
- Provides `ideal_position` variable for our new helper method

**Verified:** ✅ Interface correct - no changes needed

---

## Interface 4: FantasyPlayer.position

**Source:** utils/FantasyPlayer.py:92

**Type:** Instance attribute (str)

**Declaration:**
```python
position: str
```

**Values:**
- Valid positions: "QB", "RB", "WR", "TE", "K", "DST"
- Set during player creation

**Current Usage:**
- AddToRosterModeManager._match_players_to_rounds() line 426 (reading player.position)

**Usage in Our Code:**
- Task 1: Helper method reads `player.position` parameter
- Task 2: Line 426 replacement reads `player.position`

**Verified:** ✅ Interface matches TODO assumptions (str attribute)

---

## Interface 5: AddToRosterModeManager Internal Context (Line 426)

**Source:** league_helper/add_to_roster_mode/AddToRosterModeManager.py:420-434

**Context Variables in Scope:**

```python
# Line 422-434 (loop structure)
for player in available_players:
    # Line 426: BUGGY LINE (to be replaced)
    if self.config.get_position_with_flex(player.position) == ideal_position:
        # Lines 428-434: Assignment logic (UNCHANGED)
        round_assignments[round_num] = player
        available_players.remove(player)
        break
```

**Variables Available at Line 426:**
- `self` - AddToRosterModeManager instance
- `player` - FantasyPlayer object (current iteration)
- `ideal_position` - str (from get_ideal_draft_position() call earlier)
- `round_assignments` - Dict[int, FantasyPlayer] (being built)
- `available_players` - List[FantasyPlayer] (mutable list)
- `round_num` - int (outer loop variable)

**Our Replacement (Task 2):**
```python
# OLD (line 426):
if self.config.get_position_with_flex(player.position) == ideal_position:

# NEW (line 426):
if self._position_matches_ideal(player.position, ideal_position):
```

**Verified:** ✅ All variables in scope, replacement fits perfectly

---

## Assumptions vs Reality Check

| Assumption from TODO | Reality from Source Code | Match? |
|----------------------|-------------------------|--------|
| `flex_eligible_positions` is List[str] | ✅ List[str] (line 221) | ✅ MATCH |
| `get_position_with_flex()` signature | ✅ `(self, position: str) -> str` (line 313) | ✅ MATCH |
| `get_ideal_draft_position()` signature | ✅ `(self, round_num: int) -> str` (line 683) | ✅ MATCH |
| `player.position` is str attribute | ✅ `position: str` (line 92) | ✅ MATCH |
| Line 426 context has player, ideal_position | ✅ Both variables in scope (lines 422-426) | ✅ MATCH |
| Can add helper method after line 440 | ✅ After `_match_players_to_rounds()` ends | ✅ MATCH |

**All assumptions verified ✅ - Ready to proceed with implementation**

---

## Summary

**Total Interfaces Verified:** 5
**Mismatches Found:** 0
**Blocking Issues:** None

**Interface Verification Status:** ✅ COMPLETE

**Next Step:** Step 2 - Create implementation_checklist.md

---

*End of interface_contracts.md - All external interfaces verified*
