# Sub-Feature 4: File Update Strategy - Implementation Checklist

**Purpose:** Continuous verification against spec during implementation

**Spec File:** `sub_feature_04_file_update_strategy_spec.md`

---

## Phase 1: Rewrite update_players_file() Core Logic

### Task 1.1: Read existing JSON files per position
- [ ] Method reads from `data_folder / 'player_data'`
- [ ] Reads all 6 position files (qb, rb, wr, te, k, dst)
- [ ] Uses `json.load()` to parse JSON
- [ ] Stores in List[Dict[str, Any]] structure
- **Spec:** NEW-75 (spec lines 14, 157-161)
- **File:** league_helper/util/PlayerManager.py:434
- **Verified:** ⏸️

### Task 1.2: Group players by position
- [ ] Groups `self.players` by position field
- [ ] Data structure: `Dict[str, List[FantasyPlayer]]`
- [ ] Handles all 6 positions (QB, RB, WR, TE, K, DST)
- [ ] Defensive check: skips players with None/invalid position
- **Spec:** NEW-76 (spec lines 15, 159)
- **File:** league_helper/util/PlayerManager.py
- **Verified:** ⏸️

### Task 1.3: Match players by ID for selective update
- [ ] Creates ID → FantasyPlayer lookup dict
- [ ] Pattern: `{p.id: p for p in position_players}`
- [ ] Uses integer IDs for matching
- **Spec:** NEW-77 (spec lines 16, 169-177)
- **File:** league_helper/util/PlayerManager.py
- **Verified:** ⏸️

### Task 1.4: Update ONLY drafted_by and locked fields
- [ ] Selective update: ONLY 2 fields modified in JSON dict
- [ ] drafted_by conversion logic (3 cases - see Task 2.1)
- [ ] locked written as boolean directly
- [ ] All other fields in JSON dict preserved
- **Spec:** NEW-78 (spec lines 17, 169-177)
- **File:** league_helper/util/PlayerManager.py
- **Verified:** ⏸️

### Task 1.5: Preserve all other fields during update
- [ ] projected_points array unchanged
- [ ] actual_points array unchanged
- [ ] Position-specific stats (passing, rushing, etc.) unchanged
- [ ] All other JSON fields preserved
- **Spec:** NEW-79 (spec lines 18, 175-177)
- **File:** league_helper/util/PlayerManager.py
- **Verified:** ⏸️

### Task 1.6: Write back to JSON files with atomic pattern
- [ ] Write to .tmp file first
- [ ] Use `json.dump(players_array, f, indent=2)`
- [ ] Atomic rename .tmp → .json using Path.rename()
- [ ] Return success message (str): "Player data updated successfully"
- **Spec:** NEW-80 (spec lines 19, 162-165)
- **File:** league_helper/util/PlayerManager.py
- **Verified:** ⏸️

### Task 1.7: Implement backup + temp file pattern
- [ ] Copy .json → .bak before update
- [ ] Write to .tmp file
- [ ] Atomic rename .tmp → .json
- [ ] .bak files remain for manual recovery
- **Spec:** NEW-81 (spec lines 20, 162-165)
- **File:** league_helper/util/PlayerManager.py
- **Verified:** ⏸️

### Task 1.8: Log warnings for missing files/players
- [ ] Missing file → raise FileNotFoundError (Task 3.1)
- [ ] Player in self.players not in JSON → log warning, skip
- [ ] Appropriate logging with self.logger
- **Spec:** NEW-82 (spec lines 21, 166)
- **File:** league_helper/util/PlayerManager.py
- **Verified:** ⏸️

---

## Phase 2: Field Conversion Logic

### Task 2.1: Convert drafted → drafted_by (reverse of from_json)
- [ ] drafted=0 → drafted_by=""
- [ ] drafted=2 → drafted_by=Constants.FANTASY_TEAM_NAME
- [ ] drafted=1 → DO NOT UPDATE drafted_by (preserve from JSON)
- [ ] ⚠️ CRITICAL: No drafted_by field in FantasyPlayer!
- **Spec:** NEW-83 (spec lines 22, 60-67)
- **File:** league_helper/util/PlayerManager.py
- **Verified:** ⏸️

### Task 2.2: Handle locked field (already boolean after Sub-feature 3)
- [ ] locked is already bool in FantasyPlayer
- [ ] Write boolean directly to JSON (no conversion)
- [ ] player_dict['locked'] = player.locked
- **Spec:** NEW-84 (spec lines 22, 65-67)
- **File:** league_helper/util/PlayerManager.py
- **Verified:** ⏸️

### Task 2.3: Verify drafted_by string consistency
- [ ] Uses Constants.FANTASY_TEAM_NAME (not hardcoded "Sea Sharp")
- [ ] Constants already imported as `import constants as Constants`
- [ ] No hardcoded team name strings
- **Spec:** NEW-85 (spec line 22)
- **File:** league_helper/util/PlayerManager.py
- **Verified:** ⏸️

---

## Phase 3: Error Handling

### Task 3.1: Handle missing position JSON files
- [ ] Check file exists before reading
- [ ] Raise FileNotFoundError with clear message
- [ ] Message: "{position}_data.json not found in player_data/. Run player-data-fetcher."
- [ ] Fail fast (don't create missing files)
- **Spec:** NEW-86 (spec lines 23, 72-88)
- **File:** league_helper/util/PlayerManager.py
- **Verified:** ⏸️

### Task 3.2: Handle permission errors during write
- [ ] Catch PermissionError during file operations
- [ ] Log error with self.logger.error()
- [ ] Raise with clear message
- [ ] Pattern matches existing error handling
- **Spec:** NEW-87 (spec lines 23, 48-56)
- **File:** league_helper/util/PlayerManager.py
- **Verified:** ⏸️

### Task 3.3: Handle JSON parse errors
- [ ] Catch json.JSONDecodeError
- [ ] Log error with file path
- [ ] Raise with clear message
- [ ] Helps identify corrupted files
- **Spec:** NEW-88 (spec lines 23, 48-56)
- **File:** league_helper/util/PlayerManager.py
- **Verified:** ⏸️

### Task 3.4: Rollback strategy (manual recovery from .bak)
- [ ] No automatic rollback (by design)
- [ ] .bak files available for manual recovery
- [ ] Error raised immediately on failure
- [ ] Partial progress preserved
- **Spec:** NEW-89 (spec lines 24, 107-129)
- **File:** league_helper/util/PlayerManager.py
- **Verified:** ⏸️

---

## Phase 4: Testing

### Task 4.1: Unit test selective update (only drafted_by/locked)
- [ ] Test updates only 2 fields
- [ ] Verify other fields unchanged
- [ ] Use temp directory with test JSON files
- **Spec:** NEW-90 (spec line 24)
- **File:** tests/league_helper/util/test_PlayerManager.py
- **Verified:** ⏸️

### Task 4.2: Unit test atomic write pattern
- [ ] Verify .tmp file created
- [ ] Verify atomic rename .tmp → .json
- [ ] Mock/verify file system operations
- **Spec:** NEW-91 (spec line 24)
- **File:** tests/league_helper/util/test_PlayerManager.py
- **Verified:** ⏸️

### Task 4.3: Unit test backup file creation
- [ ] Verify .bak files created before update
- [ ] Verify .bak contains original data
- [ ] Test recovery from .bak
- **Spec:** NEW-92 (spec line 24)
- **File:** tests/league_helper/util/test_PlayerManager.py
- **Verified:** ⏸️

### Task 4.4: Integration test round-trip preservation
- [ ] Load → update → save → reload → compare
- [ ] Verify projected_points unchanged
- [ ] Verify actual_points unchanged
- [ ] Verify position-specific stats unchanged
- **Spec:** NEW-93 (spec line 24)
- **File:** tests/league_helper/util/test_PlayerManager.py
- **Verified:** ⏸️

### Task 4.5: Integration test with all 4 callers
- [ ] Test AddToRosterModeManager.py:194
- [ ] Test ModifyPlayerDataModeManager.py:250
- [ ] Test ModifyPlayerDataModeManager.py:307
- [ ] Test ModifyPlayerDataModeManager.py:405
- [ ] All callers work with new JSON-based implementation
- **Spec:** NEW-94 (spec line 24)
- **File:** Multiple test files
- **Verified:** ⏸️

---

## Phase 5: Dependency Verification

### Task 5.1: Verify Sub-feature 1 from_json() compatibility
- [x] from_json() loads ALL fields (not just drafted_by/locked)
- [x] Round-trip: from_json → modify → update_file → from_json
- [x] All fields preserved through round-trip
- **Spec:** NEW-95 (spec lines 25, 138-152)
- **File:** utils/FantasyPlayer.py:181
- **Verified:** ✅ Via test_round_trip_preservation_only_drafted_locked_updated
  - Test loads players via from_json() (called by load_players_from_json())
  - Test modifies drafted and locked
  - Test saves via update_players_file()
  - Test reloads via from_json()
  - Test verifies ALL fields preserved (projected_points, actual_points, passing, rushing, misc)
  - Confirms from_json() loads ALL fields and update_players_file() preserves them

### Task 5.2: Verify Sub-feature 3 locked field compatibility
- [x] locked is boolean in FantasyPlayer
- [x] locked written as boolean to JSON
- [x] Type consistency throughout
- **Spec:** NEW-96 (spec lines 25, 141-147)
- **File:** utils/FantasyPlayer.py:97
- **Verified:** ✅ Via both test cases
  - test_round_trip_preservation: locked=True written and read back correctly
  - test_selective_update_preserves_opponent_team_name: locked=True preserved through round-trip
  - Code: `player_dict['locked'] = updated_player.locked` (line 523 in PlayerManager.py)
  - Confirms boolean type consistency (Sub-feature 3 migration complete)

---

## Continuous Verification Questions

Ask every 5-10 minutes:
- "Did I consult spec in last 5 minutes?" → Check spec lines
- "Can I point to exact spec line this code satisfies?" → Reference NEW-XX
- "Working from spec, not memory?" → Re-read spec section
- "Checked off requirement in this checklist?" → Mark [x]

---

## Critical Interface Finding

**⚠️ drafted_by field does NOT exist in FantasyPlayer!**

**Corrected conversion logic (Task 2.1):**
```python
if player.drafted == 0:
    player_dict['drafted_by'] = ""
elif player.drafted == 2:
    player_dict['drafted_by'] = Constants.FANTASY_TEAM_NAME
# elif player.drafted == 1: DON'T update drafted_by, preserve from JSON
```

This maintains opponent team names by not overwriting them (hybrid approach per spec line 63).
