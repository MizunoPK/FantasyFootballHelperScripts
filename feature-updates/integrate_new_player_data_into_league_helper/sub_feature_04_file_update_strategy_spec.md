# Sub-Feature 4: File Update Strategy

## Objective
Migrate `update_players_file()` from writing to CSV to selective JSON updates (drafted_by and locked only).

## Dependencies
**Prerequisites:** Sub-features 1, 3 (Core Data Loading, Locked Field)
**Blocks:** None (independent feature)

## Scope (22 items)
- NEW-75 to NEW-96: update_players_file migration

**From checklist:**
- NEW-75: Read existing JSON files
- NEW-76: Group players by position
- NEW-77: Match players by ID
- NEW-78: Update ONLY drafted_by and locked fields
- NEW-79: Preserve all other fields
- NEW-80: Write back to JSON files
- NEW-81: Use backup + temp file pattern
- NEW-82: Log warnings for missing files/players
- NEW-83 to NEW-85: Field conversion logic
- NEW-86 to NEW-89: Error handling
- NEW-90 to NEW-94: Testing
- NEW-95 to NEW-96: Dependency updates

## Key Implementation

**Algorithm:**
```python
def update_players_file(self) -> str:
    # 1. Group players by position (QB, RB, WR, TE, K, DST)
    # 2. For each position:
    #    - Read existing JSON file
    #    - Create backup (.bak)
    #    - Update only drafted_by and locked fields
    #    - Write to temp file
    #    - Atomic rename temp → actual
    # 3. Return success message
```

**Selective Update Pattern:**
```python
for player_dict in players_array:
    if player_id in player_updates:
        updated_player = player_updates[player_id]
        # Update ONLY these two fields
        player_dict['drafted_by'] = updated_player.drafted_by
        player_dict['locked'] = updated_player.locked
        # All other fields preserved (projected_points, passing, etc.)
```

## Success Criteria
- [ ] update_players_file() writes to JSON
- [ ] Only drafted_by and locked updated
- [ ] All other fields preserved
- [ ] Atomic write pattern working
- [ ] Round-trip preservation test passing

See `research/` for complete implementation details.
