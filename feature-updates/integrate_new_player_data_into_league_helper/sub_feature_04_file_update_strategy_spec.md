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

## Verification Findings (From Deep Dive)

### Current Implementation

**update_players_file() location:** league_helper/util/PlayerManager.py:349-391
- **Current behavior:** Writes ALL fields to players.csv
- **Lines 370-379:** Defines fieldnames array with all 17 week_N_points columns
- **Lines 383-390:** Uses csv.DictWriter to write all player data
- **Complete rewrite required:** Switch from CSV to selective JSON updates

### Callers Identified

**4 total calls to update_players_file():**
1. **AddToRosterModeManager.py:194** - After drafting a player
2. **ModifyPlayerDataModeManager.py:250** - After adding player
3. **ModifyPlayerDataModeManager.py:307** - After dropping player
4. **ModifyPlayerDataModeManager.py:405** - After toggling lock status

**All callers:** Modify drafted_by or locked status, then call update_players_file()

### Error Handling Pattern Verified

**Pattern from PlayerManager.py:244-248:**
```python
except PermissionError:
    self.logger.error(f"Error: Permission denied accessing file {self.file_str}")
    return []
```
- **For structural issues:** Log error, raise or return with clear message
- **For data issues:** Log warning, skip, continue

### Field Conversion Requirements

**drafted → drafted_by (reverse of Sub-feature 1 from_json()):**
- drafted=0 → ""
- drafted=2 → "Sea Sharp" (FANTASY_TEAM_NAME)
- drafted=1 → player.drafted_by (hybrid approach maintains team name)

**locked (after Sub-feature 3):**
- locked field is already boolean in FantasyPlayer
- Write boolean directly to JSON (no conversion needed)

### Decisions Resolved

**NEW-78: Missing position file handling** ✅ RESOLVED (2025-12-28)
- **Decision:** Option B - Raise FileNotFoundError (fail fast)
- **Rationale:**
  - Consistent with Decision 9 (loading policy - fail fast for structural issues)
  - Maintains ownership boundaries (player-data-fetcher creates files, League Helper updates)
  - Prevents creating incomplete data (files need stats/projections, not just drafted_by/locked)
  - Clear error messages guide proper fix (re-run player-data-fetcher)
  - Missing files indicate real problems that should be fixed, not masked
- **Implementation:**
  ```python
  # In update_players_file() for each position:
  json_path = data_folder / 'player_data' / f'{position}_data.json'
  if not json_path.exists():
      raise FileNotFoundError(
          f"{position}_data.json not found in player_data/ directory. "
          f"Please run player-data-fetcher to create missing position files."
      )
  ```

**NEW-82: Performance optimization** ✅ RESOLVED (2025-12-28)
- **Decision:** Option B - Write all 6 files every time (no dirty tracking)
- **Rationale:**
  - Simple implementation - no tracking state needed
  - Performance impact minimal (6 files ~150KB total, 50-150ms on SSD)
  - Low frequency operation (1-10 calls per session, not per second)
  - Atomic consistency - all files stay in sync
  - Fewer bugs - no dirty state to manage
  - Backup strategy consistent - all 6 files have .bak at same state
- **Implementation:**
  ```python
  # Always iterate through all 6 positions
  for position in ['qb', 'rb', 'wr', 'te', 'k', 'dst']:
      # Load, update, save - regardless of whether this position changed
      update_position_file(position, players_by_position[position])
  ```

**NEW-89: Rollback strategy on failure** ✅ RESOLVED (2025-12-28)
- **Decision:** Option A - No automatic rollback (partial update acceptable)
- **Rationale:**
  - Simple implementation - no complex rollback logic needed
  - Rare scenario - file write failures uncommon in desktop app
  - Visible failure - error raised immediately, user aware of problem
  - Manual recovery available - .bak files exist for all 6 positions
  - Partial progress valuable - if 3 of 6 files written, better than losing all
  - Retry possible - user can retry operation after fixing underlying issue
  - Avoids rollback edge cases - what if rollback itself fails?
- **Implementation:**
  ```python
  # No try/except around entire loop - let errors propagate
  for position in ['qb', 'rb', 'wr', 'te', 'k', 'dst']:
      backup_file(position)  # Create .bak
      write_temp_file(position)  # Write .tmp
      atomic_rename(position)  # Rename .tmp to .json
      # If any step fails, raise error immediately
      # Previously written files stay updated
      # .bak files remain for manual recovery
  ```
- **Error handling:** Raise error immediately on failure with clear message
- **Recovery:** User can manually restore from .bak files or retry operation

### All Decisions Complete

All 3 user decisions for Sub-feature 4 resolved (2025-12-28):
- ✅ NEW-78: Missing position file → Fail fast with FileNotFoundError
- ✅ NEW-82: Performance optimization → Write all 6 files every time (simple)
- ✅ NEW-89: Rollback strategy → No automatic rollback (manual recovery from .bak)

### Round-Trip Compatibility

**Verified dependencies:**
- Sub-feature 1: from_json() loads ALL fields (projected_points, actual_points, nested stats)
- Sub-feature 2: Arrays preserved (not touched by selective update)
- Sub-feature 3: locked is boolean in both FantasyPlayer and JSON
- **This sub-feature:** Only drafted_by and locked updated

**Round-trip flow:**
1. from_json() loads ALL fields → FantasyPlayer objects
2. League Helper modifies only drafted/locked during gameplay
3. update_players_file() writes back ONLY drafted_by/locked
4. from_json() reloads ALL fields → stats unchanged

**Conclusion:** Selective update preserves all player-data-fetcher data

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
