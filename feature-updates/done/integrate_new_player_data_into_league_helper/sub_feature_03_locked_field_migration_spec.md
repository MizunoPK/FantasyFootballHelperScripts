# Sub-Feature 3: Locked Field Migration

## Objective
Change `locked` field from int (0/1) to boolean (True/False) and standardize all code to use `is_locked()` method.

## Dependencies
**Prerequisites:** Sub-feature 1 (Core Data Loading)
**Blocks:** Sub-feature 4 (File Update Strategy)

## Scope (21 items)
- NEW-54 to NEW-74: Locked field migration

**From checklist:**
- NEW-54: Change FantasyPlayer.locked to boolean type
- NEW-55: Update is_locked() to return self.locked (not self.locked == 1)
- NEW-56: Update is_available() to use `not self.locked`
- NEW-57: Update __str__() to use is_locked() method
- NEW-58: Update from_json() to load boolean directly
- NEW-59: Update to_json() to write boolean directly
- NEW-60 to NEW-67: Standardize 8 comparisons to use is_locked() method
- NEW-68 to NEW-69: Update 2 assignments to use True/False
- NEW-70 to NEW-74: Testing (5 items)

## Verification Findings (From Deep Dive)

### Current Implementation Verified

**FantasyPlayer field definition (utils/FantasyPlayer.py:96):**
```python
locked: int = 0  # 0 = not locked, 1 = locked (cannot be drafted or traded)
```

**is_locked() method (utils/FantasyPlayer.py:320):**
```python
return self.locked == 1
```

**is_available() method (utils/FantasyPlayer.py:308):**
```python
return self.drafted == 0 and self.locked == 0
```

**__str__ method (utils/FantasyPlayer.py:397):**
```python
locked_indicator = " [LOCKED]" if self.locked == 1 else ""
```

### All Comparison Locations (8 total)

1. **PlayerManager.py:552** - `if p.score < lowest_scores[p.position] and p.locked == 0:`
2. **ModifyPlayerDataModeManager.py:338** - `locked_players = [p for p in self.player_manager.players if p.locked == 1]`
3. **ModifyPlayerDataModeManager.py:394** - `was_locked = selected_player.locked == 1`
4. **ModifyPlayerDataModeManager.py:409** - `if selected_player.locked == 1:`
5. **trade_analyzer.py:639** - `my_locked_original = [p for p in my_team.team if p.locked == 1 and p.get_risk_level() != "HIGH"]`
6. **trade_analyzer.py:643** - `their_locked_original = [p for p in their_team.team if p.locked == 1 and p.get_risk_level() != "HIGH"]`
7. **trade_analyzer.py:820** - `my_locked = [p for p in my_team.team if p.locked == 1 and p.get_risk_level() != "HIGH"]`
8. **trade_analyzer.py:824** - `their_locked = [p for p in their_team.team if p.locked == 1 and p.get_risk_level() != "HIGH"]`

### All Assignment Locations (2 total)

1. **ModifyPlayerDataModeManager.py:401** - `selected_player.locked = 0 if was_locked else 1` (toggles lock status)
2. **trade_analyzer.py:181** - `p_copy.locked = 0` (unlock for testing)

### Migration Benefits

**More Pythonic:** `if player.is_locked()` instead of `if player.locked == 1`
- **Encapsulation:** Using method hides internal representation
- **Consistency:** Matches JSON format (already boolean there)
- **Future-proof:** Can add logic to is_locked() if needed
- **Readability:** Intent is clearer

## Key Implementation

**Note:** Sub-feature 1 handles loading `locked` as boolean from JSON. This sub-feature handles:
- Changing field type definition from int to bool
- Updating all comparisons to use `is_locked()` method
- Updating all assignments to use True/False

**FantasyPlayer field change:**
```python
# OLD: locked: int = 0
# NEW: locked: bool = False
```

**from_json() update:**
```python
# Direct assignment - no conversion
locked = data.get('locked', False)
```

**All comparisons updated:**
```python
# OLD: if player.locked == 1:
# NEW: if player.is_locked():

# OLD: if player.locked == 0:
# NEW: if not player.is_locked():
```

## Success Criteria
- [ ] locked field is boolean
- [ ] All 14 comparisons use is_locked()
- [ ] All 2 assignments use True/False
- [ ] All tests passing

See `research/` for complete analysis.
