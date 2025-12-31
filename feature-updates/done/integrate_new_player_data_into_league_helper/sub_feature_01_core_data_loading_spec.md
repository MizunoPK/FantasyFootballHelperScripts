# Sub-Feature 1: Core Data Loading

## Objective

Implement the foundation for loading player data from JSON files instead of CSV. This includes:
- Creating `FantasyPlayer.from_json()` method
- Implementing `PlayerManager.load_players_from_json()` method
- Adding all position-specific stat fields to FantasyPlayer
- Establishing basic data loading patterns

## Dependencies

**Prerequisites:** None - this is the foundation

**Blocks:** Sub-features 2, 4, 7 (Weekly Data, File Updates, DraftedRosterManager)

## Scope

### Checklist Items (29 total)

**Research Findings (Phase 1):**
- ✅ Existing pattern uses `safe_int_conversion()` and `safe_float_conversion()` helpers
- ✅ from_dict() at FantasyPlayer.py:158-194 shows the pattern to follow
- ✅ load_players_from_csv() at PlayerManager.py:142-219 shows loading pattern
- ✅ FANTASY_TEAM_NAME constant at constants.py:19 ("Sea Sharp")
- ✅ JSON structure confirmed in data/player_data/ files

## Checklist Items (29 total)

**From Core Data Loading (NEW-1 to NEW-19):**
- NEW-5: Remove 17 week_N_points fields (moved to Sub-feature 2)
- NEW-6: Add projected_points: List[float] field
- NEW-7: Add actual_points: List[float] field
- NEW-12: Load projected_points array from JSON
- NEW-13: Load actual_points array from JSON
- NEW-14: Validate arrays have exactly 17 elements (pad if needed)
- NEW-15: Handle missing arrays (default to [0.0] * 17)

**Position-Specific Stats (NEW-31 to NEW-40):**
- NEW-31: Add `passing: Optional[Dict[str, List[float]]]` to FantasyPlayer
- NEW-32: Add `rushing: Optional[Dict[str, List[float]]]` to FantasyPlayer
- NEW-33: Add `receiving: Optional[Dict[str, List[float]]]` to FantasyPlayer
- NEW-34: Add `misc: Optional[Dict[str, List[float]]]` to FantasyPlayer (QB/RB/WR/TE only)
- NEW-35: Add `extra_points: Optional[Dict[str, List[float]]]` to FantasyPlayer (K only)
- NEW-36: Add `field_goals: Optional[Dict[str, List[float]]]` to FantasyPlayer (K only)
- NEW-37: Add `defense: Optional[Dict[str, List[float]]]` to FantasyPlayer (DST only)
- NEW-38: Load nested stats in from_json() (direct dict copy)
- NEW-39: Write nested stats in to_json() (preserve during round-trip)
- NEW-40: Test round-trip preservation: load → modify → save → reload → verify stats intact

**Scope Clarifications (NEW-41 to NEW-44):**
- NEW-41: Confirm simulation module is OUT OF SCOPE ✅ RESOLVED
- NEW-42: Confirm DraftedRosterManager is IN SCOPE ✅ RESOLVED (covered in Sub-feature 7)
- NEW-43: Document simulation incompatibility if read-only properties implemented
- NEW-44: Position-specific field policy ✅ RESOLVED (all Optional, no validation)

**PlayerManager JSON Loading:**
- NEW-1: Grep for all direct weekly field access (moved to Sub-feature 2)
- NEW-2: Grep for dynamic attribute access (moved to Sub-feature 2)
- NEW-3: Grep for dictionary access (moved to Sub-feature 2)
- NEW-4: Identify all modules accessing weekly data (moved to Sub-feature 2)

**Additional Items:**
- Create `FantasyPlayer.from_json()` classmethod
- Create `PlayerManager.load_players_from_json()` method
- Handle JSON parsing errors (fail fast for malformed, skip players with missing required fields)
- Implement field mapping (id conversion, drafted_by → drafted, locked boolean → int temporarily)

## Verification Findings (From Deep Dive)

### Existing Patterns Identified

**Safe Conversion Helpers (FantasyPlayer.py:20-76):**
- `safe_int_conversion(value, default)` - Handles None, empty string, invalid values
- `safe_float_conversion(value, default)` - Handles None, empty string, invalid values
- **Usage:** Use these for all type conversions from JSON (matches existing pattern)

**CSV Loading Pattern (PlayerManager.py:142-219):**
- Two-tier error handling:
  - **Structural issues** (FileNotFoundError, PermissionError): `logger.error()` + return [] (fail fast)
  - **Data issues** (bad player row): `logger.warning()` + skip + continue (graceful)
- Post-loading logic:
  - Calculate `max_projection` during loop (line 219)
  - Call `load_team()` after all players loaded (line 266)
  - Update `scoring_calculator.max_projection` (line 234)
- **Recommendation:** Follow same pattern for JSON loading

**from_dict() Pattern (FantasyPlayer.py:158-194):**
- Uses `.get()` with defaults for Optional fields
- Uses safe_int_conversion/safe_float_conversion for all numeric fields
- **Recommendation:** from_json() should follow this pattern exactly

**Constants (league_helper/constants.py:19):**
- `FANTASY_TEAM_NAME = "Sea Sharp"` - Used for drafted_by conversion
- **Usage:** drafted_by == FANTASY_TEAM_NAME → drafted = 2

### Array Validation Strategy (Verified)

**Pattern from codebase:** Lenient approach - no strict validation found in existing code
- **Recommendation:** Pad if too short, truncate if too long, log warning for mismatches
- **Rationale:** Matches existing lenient pattern (skip bad data with warnings, don't fail)
- **Implementation:** `(array + [0.0] * 17)[:17]` - simple one-liner
- **Source:** PlayerManager.py:236-250 shows skip-with-warning pattern

### Error Handling Patterns (Verified)

**Required Field Validation (PlayerManager.py:166):**
```python
if 'id' not in data or 'name' not in data or 'position' not in data:
    raise ValueError(f"Missing required field in player data: {data}")
```
- **Rationale:** Structural issues fail fast with clear message
- **Logging:** ValueError bubbles up to caller which logs it

**Optional Field Handling (FantasyPlayer.py throughout):**
- `.get(key)` returns None if missing - simple, Pythonic
- No default needed for Optional fields
- **Example:** `passing = data.get('passing')` - automatically returns None

**Post-Loading Calculations (PlayerManager.py:219-234):**
1. Track max_projection during loop
2. Call load_team() after all players loaded
3. Update scoring_calculator.max_projection
- **Message format:** `self.logger.info(f"Loaded {len(qb_players)} players from qb_data.json")`

### JSON Structure (Verified in data/player_data/)

**Format:**
```json
{
  "qb_data": [
    {
      "id": "12345",
      "name": "Patrick Mahomes",
      "team": "KC",
      "position": "QB",
      "locked": false,
      "drafted_by": "",
      "projected_points": [25.3, 28.1, ...],
      "actual_points": [0.0, 0.0, ...],
      "passing": {
        "completions": [22.5, 24.1, ...],
        "attempts": [35.2, 38.5, ...],
        ...
      }
    }
  ]
}
```

**Key observations:**
- Position key wrapper: `{"qb_data": [...]}`
- id stored as string (needs conversion to int)
- locked is boolean (loaded directly - Sub-feature 3 updates comparisons to use is_locked())
- drafted_by is string (needs conversion to drafted int: 0/1/2 for hybrid approach)
- Arrays are 17 elements each
- Nested stats are Optional (may not exist for all positions)

## Implementation Details

### FantasyPlayer.from_json()

```python
@classmethod
def from_json(cls, data: Dict[str, Any]) -> 'FantasyPlayer':
    """
    Create FantasyPlayer instance from JSON dictionary.

    Args:
        data: Dictionary from JSON player data

    Returns:
        FantasyPlayer instance

    Raises:
        ValueError: If required field missing (id, name, position)
    """
    # Required fields
    if 'id' not in data or 'name' not in data or 'position' not in data:
        raise ValueError(f"Missing required field in player data: {data}")

    # Convert id from string to int (use safe conversion for robustness)
    player_id = safe_int_conversion(data.get('id'), 0)

    # Load arrays with validation
    projected_points = data.get('projected_points', [0.0] * 17)
    actual_points = data.get('actual_points', [0.0] * 17)

    # Pad/truncate to exactly 17 elements
    projected_points = (projected_points + [0.0] * 17)[:17]
    actual_points = (actual_points + [0.0] * 17)[:17]

    # Convert drafted_by to drafted int
    drafted_by = data.get('drafted_by', '')
    if drafted_by == '':
        drafted = 0
    elif drafted_by == FANTASY_TEAM_NAME:  # "Sea Sharp"
        drafted = 2
    else:
        drafted = 1

    # Load locked as boolean (Sub-feature 3 will update comparisons to use is_locked())
    locked = data.get('locked', False)

    # Calculate fantasy_points (NOT in JSON)
    fantasy_points = sum(projected_points)

    # Load position-specific nested stats (all Optional)
    passing = data.get('passing')
    rushing = data.get('rushing')
    receiving = data.get('receiving')
    misc = data.get('misc')
    extra_points = data.get('extra_points')
    field_goals = data.get('field_goals')
    defense = data.get('defense')

    return cls(
        id=player_id,
        name=data.get('name'),
        team=data.get('team'),
        position=data.get('position'),
        bye_week=data.get('bye_week'),
        fantasy_points=fantasy_points,
        drafted=drafted,
        locked=locked,
        average_draft_position=data.get('average_draft_position'),
        player_rating=data.get('player_rating'),
        injury_status=data.get('injury_status', 'ACTIVE'),
        projected_points=projected_points,
        actual_points=actual_points,
        # Position-specific stats
        passing=passing,
        rushing=rushing,
        receiving=receiving,
        misc=misc,
        extra_points=extra_points,
        field_goals=field_goals,
        defense=defense
    )
```

### PlayerManager.load_players_from_json()

```python
def load_players_from_json(self) -> bool:
    """
    Load all players from position-specific JSON files.

    Replaces load_players_from_csv().

    Returns:
        True if successful, False otherwise

    Raises:
        FileNotFoundError: If player_data directory doesn't exist
        JSONDecodeError: If JSON file is malformed
    """
    player_data_dir = self.data_folder / 'player_data'

    # Verify directory exists (fail fast)
    if not player_data_dir.exists():
        raise FileNotFoundError(
            f"Player data directory not found: {player_data_dir}\n"
            "Run player-data-fetcher to generate JSON files."
        )

    all_players = []
    position_files = [
        'qb_data.json', 'rb_data.json', 'wr_data.json',
        'te_data.json', 'k_data.json', 'dst_data.json'
    ]

    for position_file in position_files:
        filepath = player_data_dir / position_file

        # Skip missing files with warning
        if not filepath.exists():
            self.logger.warning(f"Position file not found: {position_file}")
            continue

        try:
            # Load and parse JSON
            with open(filepath, 'r') as f:
                json_data = json.load(f)

            # Extract position key (e.g., "qb_data")
            position_key = position_file.replace('.json', '')
            players_array = json_data.get(position_key, [])

            # Convert each player
            for player_data in players_array:
                try:
                    player = FantasyPlayer.from_json(player_data)
                    all_players.append(player)
                except ValueError as e:
                    # Skip player with missing required fields
                    self.logger.warning(f"Skipping invalid player: {e}")
                    continue

            self.logger.info(f"Loaded {len(players_array)} players from {position_file}")

        except json.JSONDecodeError as e:
            # Malformed JSON - fail fast
            self.logger.error(f"Malformed JSON in {position_file}: {e}")
            raise

    # Store and return
    self.players = all_players
    self.logger.info(f"Total players loaded: {len(self.players)}")

    # Calculate max_projection
    if self.players:
        self.max_projection = max(p.fantasy_points for p in self.players)

    # Load team roster (drafted == 2)
    self.load_team()

    return True
```

## Testing Requirements

### Unit Tests

**Test FantasyPlayer.from_json():**
- Load QB with all fields populated
- Load RB with partial fields (verify Optional fields = None)
- Load K without passing/rushing stats (verify position-specific handling)
- Load DST with defense stats
- Verify id conversion (string → int)
- Verify drafted_by conversion (string → 0/1/2)
- Verify locked conversion (boolean → 0/1)
- Verify fantasy_points calculation (sum of projected_points)
- Verify array padding (15 elements → 17 with zeros)
- Verify array truncation (20 elements → 17)
- Test missing required field (raises ValueError)

**Test PlayerManager.load_players_from_json():**
- Load all 6 position files successfully
- Handle missing position file (log warning, continue)
- Handle malformed JSON (raise JSONDecodeError)
- Handle missing player_data directory (raise FileNotFoundError)
- Verify all players combined into single list
- Verify max_projection calculated
- Verify load_team() called

**Test Round-Trip Preservation:**
- Load player from JSON
- Verify all nested stats preserved
- Modify drafted/locked
- Save to JSON (will be implemented in Sub-feature 4)
- Reload
- Verify all stats still intact (passing, rushing, etc.)

### Integration Tests

**Test Full Loading Workflow:**
- Start League Helper
- Load players from JSON
- Verify all 4 modes can access player data
- Verify no crashes or errors
- Verify player counts match expected

## Success Criteria

✅ **Core Functionality:**
- [ ] FantasyPlayer.from_json() creates instances from JSON dictionaries
- [ ] PlayerManager.load_players_from_json() loads all 6 position files
- [ ] All position-specific stat fields added to FantasyPlayer
- [ ] fantasy_points calculated correctly (sum of projected_points)
- [ ] All type conversions working (id, drafted_by, locked)

✅ **Error Handling:**
- [ ] Missing player_data directory raises FileNotFoundError
- [ ] Malformed JSON raises JSONDecodeError
- [ ] Missing required field skips player with warning
- [ ] Missing position file logs warning and continues

✅ **Testing:**
- [ ] All unit tests passing (100%)
- [ ] Round-trip preservation test passing
- [ ] Integration test with League Helper passing

✅ **Code Quality:**
- [ ] No week_N_points references in new code
- [ ] Comprehensive docstrings on new methods
- [ ] Error messages are clear and actionable

## Notes

**Field Handling:**
- `locked` loaded as boolean directly (Sub-feature 3 updates comparisons to use is_locked() method)
- `drafted_by` stored as string but `drafted` int also maintained (hybrid approach per Decision 2)

**Out of Scope:**
- CSV loading (deprecated in Sub-feature 8)
- Simulation module updates (separate future feature)
- DraftedDataWriter updates (Sub-feature 7)

**Dependencies for Next Sub-Features:**
- Sub-feature 2 (Weekly Data) depends on projected_points/actual_points fields being loaded
- Sub-feature 4 (File Updates) depends on from_json() being complete
- Sub-feature 7 (DraftedRosterManager) depends on basic JSON loading working
