# Sub-Feature 1: Core Data Loading - Checklist

> **IMPORTANT**: When marking items as resolved, also update `sub_feature_01_core_data_loading_spec.md`
> with full implementation details. The checklist tracks status; the specs file is
> the implementation specification.

---

## Progress Summary

**Total Items:** 29
**Completed:** 11 (4 scope + 7 verification)
**Remaining:** 18 (implementation tasks)

---

## FantasyPlayer Field Updates (7 items)

- [ ] **NEW-5:** Remove 17 `week_N_points` fields from FantasyPlayer dataclass (moved to Sub-feature 2)
- [ ] **NEW-6:** Add `projected_points: List[float]` field (default: [0.0] * 17)
- [ ] **NEW-7:** Add `actual_points: List[float]` field (default: [0.0] * 17)
- [ ] **NEW-12:** Load `projected_points` array from JSON in from_json()
- [ ] **NEW-13:** Load `actual_points` array from JSON in from_json()
- [x] **NEW-14:** Validate arrays have exactly 17 elements (pad if needed) ✅ VERIFIED
  - **Pattern from codebase:** Lenient approach - no strict validation found in existing code
  - **Recommendation:** Pad if too short, truncate if too long, log warning for mismatches
  - **Rationale:** Matches existing lenient pattern (skip bad data with warnings, don't fail)
  - **Implementation:** `(array + [0.0] * 17)[:17]` - simple one-liner
- [x] **NEW-15:** Handle missing arrays (default to [0.0] * 17) ✅ VERIFIED
  - **Pattern from codebase:** Use .get() with sensible defaults (FantasyPlayer.py:156, 168)
  - **Recommendation:** `data.get('projected_points', [0.0] * 17)`
  - **Rationale:** Matches existing pattern - missing Optional fields default to safe values
  - **No error:** Player can load with zero projections (degraded but usable)

---

## Position-Specific Stats Fields (10 items)

- [ ] **NEW-31:** Add `passing: Optional[Dict[str, List[float]]]` to FantasyPlayer
- [ ] **NEW-32:** Add `rushing: Optional[Dict[str, List[float]]]` to FantasyPlayer
- [ ] **NEW-33:** Add `receiving: Optional[Dict[str, List[float]]]` to FantasyPlayer
- [ ] **NEW-34:** Add `misc: Optional[Dict[str, List[float]]]` to FantasyPlayer (QB/RB/WR/TE only)
- [ ] **NEW-35:** Add `extra_points: Optional[Dict[str, List[float]]]` to FantasyPlayer (K only)
- [ ] **NEW-36:** Add `field_goals: Optional[Dict[str, List[float]]]` to FantasyPlayer (K only)
- [ ] **NEW-37:** Add `defense: Optional[Dict[str, List[float]]]` to FantasyPlayer (DST only)
- [ ] **NEW-38:** Load nested stats in from_json() (direct dict copy using .get())
- [ ] **NEW-39:** Write nested stats in to_json() (preserve during round-trip) - DEFERRED to Sub-feature 4
- [ ] **NEW-40:** Test round-trip preservation: load → modify → save → reload → verify stats intact

---

## Scope Clarifications (4 items)

- [x] **NEW-41:** Confirm simulation module is OUT OF SCOPE ✅ RESOLVED
  - **Decision:** OUT OF SCOPE - Simulation will be migrated in separate future features
  - **Impact:** 9 locations to update (League Helper + utils only, not 17)
- [x] **NEW-42:** Confirm DraftedRosterManager is IN SCOPE ✅ RESOLVED (covered in Sub-feature 7)
  - **Decision:** IN SCOPE - Will be deprecated and consolidated into PlayerManager
- [x] **NEW-43:** Document simulation incompatibility if read-only properties implemented ✅ N/A
  - **Decision:** Not applicable - using regular fields + helper methods (hybrid approach per Decision 2)
  - **No read-only properties:** drafted and drafted_by are regular fields, kept synchronized
- [x] **NEW-44:** Position-specific field policy ✅ RESOLVED
  - **Decision:** NO VALIDATION - All Optional fields, no position checks
  - **Rationale:** Trust data source, validate at usage time in future features

---

## FantasyPlayer.from_json() Method Creation (5 items)

- [ ] **CORE-1:** Create `FantasyPlayer.from_json()` classmethod
  - Convert id from string to int
  - Handle drafted_by → drafted conversion (0/1/2)
  - Handle locked boolean → int conversion (temporary - Sub-feature 3 changes to boolean)
  - Calculate fantasy_points (sum of projected_points)
  - Load all position-specific nested stats as Optional
- [x] **CORE-2:** Implement required field validation (id, name, position) ✅ VERIFIED
  - **Pattern from codebase:** Check required fields, raise ValueError (PlayerManager.py:166)
  - **Recommendation:**
    ```python
    if 'id' not in data or 'name' not in data or 'position' not in data:
        raise ValueError(f"Missing required field in player data: {data}")
    ```
  - **Rationale:** Matches existing pattern - structural issues fail fast with clear message
  - **Logging:** ValueError bubbles up to caller which logs it (PlayerManager pattern)
- [x] **CORE-3:** Implement array validation ✅ VERIFIED (same as NEW-14)
  - **See NEW-14** for complete verification
  - **Implementation:** Pad/truncate with `(array + [0.0] * 17)[:17]`
  - **Logging:** Optional - could log warning if `len(array) != 17` before padding
  - **Decision:** Log warnings? (Minor - can decide during implementation)
- [x] **CORE-4:** Implement Optional field handling ✅ VERIFIED
  - **Pattern from codebase:** `.get(key)` returns None if missing (FantasyPlayer.py throughout)
  - **Recommendation:** `passing = data.get('passing')` - simple, Pythonic
  - **Rationale:** Dict.get() automatically returns None, no default needed for Optional fields
  - **No errors:** Missing position-specific stats are fine (optional per NEW-44)
- [ ] **CORE-5:** Add comprehensive docstring
  - Document all parameters
  - Document all conversions
  - Document error conditions
  - Provide usage example

---

## PlayerManager.load_players_from_json() Method Creation (3 items)

- [ ] **CORE-6:** Create `PlayerManager.load_players_from_json()` method
  - Load all 6 position files (qb_data.json through dst_data.json)
  - Parse JSON structure (position key wrapper + array)
  - Call FantasyPlayer.from_json() for each player
  - Combine all positions into self.players list
- [x] **CORE-7:** Implement error handling ✅ VERIFIED
  - **Pattern from codebase:** PlayerManager.py:236-250 shows two-tier approach:
    - **Structural issues** (FileNotFoundError, JSONDecodeError): `logger.error()` + raise or return []
    - **Data issues** (bad player row): `logger.warning()` + skip + continue
  - **Recommendation for Sub-feature 1:**
    - Missing player_data/ directory: `raise FileNotFoundError` (fail fast per Decision 9)
    - Malformed JSON: `raise JSONDecodeError` (fail fast)
    - Bad player data (ValueError from from_json()): `logger.warning()` + skip player
    - Missing position file: `logger.warning()` + skip position (graceful)
  - **Rationale:** Matches existing two-tier pattern
- [x] **CORE-8:** Implement post-loading logic ✅ VERIFIED
  - **Pattern from codebase:** PlayerManager.py:219-234 shows post-load calculations
  - **Verified steps:**
    1. Calculate max_projection: Track max during loop (line 219)
    2. Call load_team(): After all players loaded (line 266)
    3. Update scoring_calculator.max_projection (line 234)
  - **Logging pattern:** INFO level for success (line 184: "Warning:" prefix means WARNING level)
  - **Recommendation:** Follow same pattern - calculate during load, update after
  - **Message format:** `self.logger.info(f"Loaded {len(qb_players)} players from qb_data.json")`

---

## Testing (Unit Tests - 6 items)

- [ ] **TEST-1:** Test FantasyPlayer.from_json() with complete QB data
  - All fields populated
  - Verify all conversions correct
  - Verify nested stats loaded
- [ ] **TEST-2:** Test FantasyPlayer.from_json() with partial data
  - Missing Optional fields
  - Verify defaults applied
  - Verify no errors
- [ ] **TEST-3:** Test FantasyPlayer.from_json() array handling
  - Array padding (15 elements → 17)
  - Array truncation (20 elements → 17)
  - Missing arrays (default to [0.0] * 17)
- [ ] **TEST-4:** Test FantasyPlayer.from_json() error cases
  - Missing required field (raises ValueError)
  - Invalid id format
  - Invalid JSON structure
- [ ] **TEST-5:** Test PlayerManager.load_players_from_json() success path
  - All 6 position files load
  - Players combined correctly
  - max_projection calculated
  - load_team() called
- [ ] **TEST-6:** Test PlayerManager.load_players_from_json() error handling
  - Missing player_data directory (raises FileNotFoundError)
  - Malformed JSON (raises JSONDecodeError)
  - Missing position file (logs warning, continues)
  - Invalid player data (skips player, logs warning)

---

## Success Criteria

✅ **All items above completed**
✅ **All unit tests passing (100%)**
✅ **No week_N_points references in new code**
✅ **Round-trip preservation test passing**
✅ **Integration test with League Helper passing**

---

## Notes

- `locked` boolean → int conversion is temporary (Sub-feature 3 changes to boolean)
- `drafted_by` stored as string but `drafted` int maintained (hybrid approach per Decision 2)
- Sub-feature 2 depends on projected_points/actual_points fields being loaded
- Sub-feature 4 depends on from_json() being complete
- Sub-feature 7 depends on basic JSON loading working
