# Sub-Feature 8: CSV Deprecation & Cleanup

## Objective
Deprecate old CSV files and loading methods. Complete final integration testing.

## Dependencies
**Prerequisites:** ALL other sub-features (1-7)
**Blocks:** None (final cleanup)

## Scope (6 items)
- NEW-20 to NEW-29: CSV removal (distributed across other sub-features)

**From checklist:**
- NEW-20: Mark load_players_from_csv() as deprecated
- NEW-21: Add deprecation warnings
- NEW-27: Remove CSV loading from main entry points
- NEW-28: Mark players.csv as deprecated
- NEW-29: Mark players_projected.csv as deprecated
- Integration testing items (NEW-118 to NEW-123)

## Key Implementation

**Deprecate methods:**
```python
def load_players_from_csv(self) -> bool:
    """
    DEPRECATED: Use load_players_from_json() instead.

    This method loads player data from the old players.csv format.
    It is maintained for backward compatibility only.

    Deprecated: 2025-12-27
    Remove in: Next major version
    """
    self.logger.warning(
        "load_players_from_csv() is deprecated. "
        "Use load_players_from_json() instead. "
        "CSV support will be removed in future version."
    )
    # ... existing implementation ...
```

**Mark CSV files:**
```bash
# Rename files to indicate deprecation
mv data/players.csv data/players.csv.DEPRECATED
mv data/players_projected.csv data/players_projected.csv.DEPRECATED
mv data/drafted_data.csv data/drafted_data.csv.DEPRECATED

# Or add README.txt in data/ folder explaining deprecation
```

**Integration Tests:**
- Full League Helper workflow with JSON loading
- All 4 modes tested (AddToRoster, StarterHelper, TradeSimulator, ModifyPlayerData)
- SMOKE TESTING PROTOCOL (3 parts)
- 100% test pass rate (2,200+ tests)
- No CSV dependencies remaining

## Success Criteria
- [ ] All CSV loading methods deprecated
- [ ] CSV files marked as deprecated
- [ ] All League Helper modes working with JSON
- [ ] Full test suite passing (100%)
- [ ] SMOKE TESTING complete
- [ ] 3 QC rounds complete

## Final Validation
- Run full test suite: `python tests/run_all_tests.py`
- Run each League Helper mode manually
- Verify no references to players.csv, players_projected.csv, drafted_data.csv
- Verify all data loading from JSON
- Complete lessons learned review
- Move feature folder to `done/`
