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

## Key Implementation

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
