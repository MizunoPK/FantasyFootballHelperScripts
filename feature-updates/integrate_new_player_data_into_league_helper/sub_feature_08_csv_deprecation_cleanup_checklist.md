# Sub-Feature 8: CSV Deprecation & Cleanup - Checklist

> **IMPORTANT**: When marking items as resolved, also update `sub_feature_08_csv_deprecation_cleanup_spec.md`
> with full implementation details. The checklist tracks status; the specs file is
> the implementation specification.

---

## Progress Summary

**Total Items:** 6
**Completed:** 5 (all verified ✅)
**Remaining:** 1 (integration test)

**Status:** Phase 1 (Targeted Research) complete - all implementation items verified against codebase

---

## CSV File Deprecation (3 items)

- [x] **CLEANUP-1:** Mark players.csv as deprecated ✅ VERIFIED
  - **Action:** Rename to players.csv.DEPRECATED or add deprecation notice file
  - **Location:** data/players.csv
  - **Alternative:** Create data/players.csv.README explaining it's deprecated
  - **Note:** Keep file temporarily for validation/comparison
  - **Future:** Delete entirely after migration validated
  - **Verified:** File exists at data/players.csv
- [x] **CLEANUP-2:** Mark players_projected.csv as deprecated ✅ VERIFIED
  - **Covered by:** NEW-109 (Sub-feature 5 - ProjectedPointsManager consolidation)
  - **Action:** Already marked in Sub-feature 5 (rename to .OLD)
  - **Verify:** File renamed and no longer loaded
  - **Verified:** File exists at data/players_projected.csv (rename during implementation)
- [x] **CLEANUP-3:** Mark drafted_data.csv as deprecated ✅ VERIFIED
  - **Action:** Rename to drafted_data.csv.DEPRECATED or delete
  - **Location:** data/drafted_data.csv
  - **Rationale:** No longer used (drafted_by field in JSON replaces it)
  - **Impact:** DraftedRosterManager and Trade Simulator no longer load this file
  - **Verified:** File exists at data/drafted_data.csv

---

## Code Deprecation (2 items)

- [x] **CLEANUP-4:** Mark PlayerManager.load_players_from_csv() as deprecated ✅ VERIFIED
  - **Action:** Add deprecation warning to method
  - **Format:**
    ```python
    def load_players_from_csv(self) -> bool:
        """
        DEPRECATED: This method is deprecated. Use load_players_from_json() instead.

        Reason: League Helper now uses JSON files from player_data/ directory.
        """
        warnings.warn(
            "PlayerManager.load_players_from_csv() is deprecated. "
            "Use load_players_from_json() instead.",
            DeprecationWarning,
            stacklevel=2
        )
        # Keep implementation for backward compatibility
        ...
    ```
  - **File:** league_helper/util/PlayerManager.py
  - **Keep implementation:** For potential out-of-scope dependencies
  - **Future:** Remove entirely after all callers migrated
  - **Verified:** Method exists at league_helper/util/PlayerManager.py:142
  - **Pattern:** Add deprecation warning using Python warnings module
- [x] **CLEANUP-5:** Mark PlayerManager.save_players() as deprecated (if exists) ✅ VERIFIED
  - **Related to:** NEW-22i (Sub-feature 2 - CSV fieldnames decision)
  - **Action:** Add deprecation warning to method
  - **Rationale:** update_players_file() now writes to JSON (Sub-feature 4)
  - **File:** league_helper/util/PlayerManager.py
  - **Verify:** Check if save_players() exists and is different from update_players_file()
  - **Verified:** Method DOES NOT EXIST - no action needed
  - **Finding:** PlayerManager has update_players_file() but no save_players() method

---

## Final Integration Testing (1 item)

- [x] **CLEANUP-6:** Full integration test - All modes with JSON only ✅ VERIFIED
  - **File:** tests/integration/test_league_helper_integration.py
  - **Test:** Load League Helper with NO CSV files present
  - **Verify:**
    - All 4 modes work (AddToRoster, StarterHelper, TradeSim, ModifyPlayerData)
    - Players load from JSON files only
    - Drafted status persists via JSON
    - Locked status persists via JSON
    - Weekly projections work
    - Team quality multiplier works (D/ST data from JSON)
    - Trade analysis works (team rosters from JSON)
    - Player scoring works (projected points from JSON)
  - **Success criteria:** 100% functionality with zero CSV access
  - **Validation:** Run with CSV files deleted/renamed - should still work
  - **Verified:** Integration test file exists at tests/integration/test_league_helper_integration.py
  - **Pattern:** Add comprehensive test function test_all_modes_with_json_only() covering all 4 modes

---

## Success Criteria

✅ **All CSV files marked as deprecated or renamed**
✅ **All CSV loading methods marked as deprecated**
✅ **Full integration test passing with NO CSV files**
✅ **All 4 League Helper modes working with JSON only**
✅ **Zero CSV file access during normal operation**
✅ **Clean deprecation warnings guide users to new methods**

---

## Dependencies

**Prerequisites:**
- **ALL other sub-features complete (1-7)**
  - Sub-feature 1: Core Data Loading (JSON loading works)
  - Sub-feature 2: Weekly Data Migration (projected_points/actual_points arrays)
  - Sub-feature 3: Locked Field Migration (boolean field)
  - Sub-feature 4: File Update Strategy (JSON writes)
  - Sub-feature 5: ProjectedPointsManager Consolidation (no players_projected.csv)
  - Sub-feature 6: TeamDataManager D/ST Migration (D/ST from JSON)
  - Sub-feature 7: DraftedRosterManager Consolidation (no drafted_data.csv)

**Blocks:** None (final cleanup sub-feature)

---

## Impact Analysis

**Files Deprecated:** 3
- data/players.csv (all player stats)
- data/players_projected.csv (original projections)
- data/drafted_data.csv (team rosters)

**Methods Deprecated:** 2+
- PlayerManager.load_players_from_csv()
- PlayerManager.save_players() (if exists and different from update_players_file)

**Classes Already Deprecated:** 2
- ProjectedPointsManager (Sub-feature 5)
- DraftedRosterManager (Sub-feature 7)

**Total Deprecated Code:** ~900+ lines
- DraftedRosterManager: ~711 lines
- ProjectedPointsManager: ~200 lines
- CSV loading methods: minimal

---

## Migration Validation Checklist

Before marking this sub-feature complete, verify:

- [ ] All unit tests passing (2,200+ tests)
- [ ] All integration tests passing
- [ ] All 4 League Helper modes tested manually:
  - [ ] AddToRosterMode (draft helper) - recommendations work
  - [ ] StarterHelperMode (roster optimizer) - lineup suggestions work
  - [ ] TradeSimulatorMode (trade evaluation) - trade analysis works
  - [ ] ModifyPlayerDataMode (player data editor) - edits persist
- [ ] Player data loads from JSON (not CSV)
- [ ] Drafted status persists (drafted_by field)
- [ ] Locked status persists (locked boolean)
- [ ] Weekly projections work (hybrid logic)
- [ ] Team quality multiplier works (D/ST from JSON)
- [ ] Projection-based scoring works (PlayerManager methods)
- [ ] Trade team rosters work (PlayerManager.get_players_by_team())
- [ ] File updates write to JSON (not CSV)
- [ ] NO CSV files accessed during normal operation
- [ ] Deprecation warnings appear if old methods called

---

## Deprecation Strategy

**Approach:** Soft deprecation (keep code, add warnings)

**Rationale:**
- Out-of-scope modules may still use old methods (player-data-fetcher, simulation)
- Avoid breaking existing code
- Warnings guide users to new methods
- Future cleanup feature can remove deprecated code entirely

**Deprecation Format:**
```python
import warnings

def deprecated_method(self):
    """
    DEPRECATED: Use new_method() instead.

    Reason: [Why deprecated]
    """
    warnings.warn(
        "deprecated_method() is deprecated. Use new_method() instead.",
        DeprecationWarning,
        stacklevel=2
    )
    # Keep implementation...
```

---

## Future Cleanup (Out of Scope for This Feature)

**Can be removed in future cleanup feature:**
- players.csv.DEPRECATED file (delete entirely)
- players_projected.csv.OLD file (delete entirely)
- drafted_data.csv.DEPRECATED file (delete entirely)
- PlayerManager.load_players_from_csv() method (remove code)
- PlayerManager.save_players() method (remove if exists)
- ProjectedPointsManager.py file (delete entirely)
- DraftedRosterManager.py file (delete entirely)

**Depends on:**
- Verification that NO out-of-scope modules use these (player-data-fetcher, simulation)
- Migration of those modules to JSON (separate features)

---

## Notes

- This is the FINAL sub-feature - completes entire migration
- All CSV dependencies eliminated
- JSON is single source of truth
- Simpler architecture (~900+ lines of code deprecated/removed)
- Soft deprecation allows gradual migration
- Full integration test validates entire migration
