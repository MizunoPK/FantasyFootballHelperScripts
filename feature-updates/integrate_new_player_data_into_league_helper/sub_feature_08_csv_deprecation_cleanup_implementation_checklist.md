# Sub-Feature 8: CSV Deprecation & Cleanup - Implementation Checklist

**Instructions**: Check off EACH requirement as you implement it. Do NOT batch-check.

## From Spec & Traceability Matrix:

### ⚠️ CRITICAL IMPLEMENTATION SEQUENCE

**MUST follow this exact order:**
1. **Phase 2 FIRST** (Tasks 2.1-2.4) - Update code to use JSON
2. **Phase 1 SECOND** (Tasks 1.1-1.3) - Rename CSV files
3. **Phase 3 THIRD** (Task 3.1) - Integration testing

**Rationale:** If CSV files are renamed BEFORE entry points are updated, League Helper will fail on startup!

---

### Phase 2: Code Deprecation & Main Entry Point Update (4 tasks) - ✅ COMPLETE

- [x] **Task 2.1**: Add deprecation warning to load_players_from_csv()
      Spec: sub_feature_08_spec.md lines 87-91, checklist CLEANUP-4
      File: league_helper/util/PlayerManager.py line 143
      Implementation: Add warnings.warn() with DeprecationWarning, stacklevel=2
      Verified: [x] Matches spec exactly

- [x] **Task 2.2**: Verify save_players() doesn't exist (no action needed)
      Spec: checklist CLEANUP-5
      Implementation: grep verification confirms method doesn't exist
      Verified: [x] No action needed (method doesn't exist)

- [x] **Task 2.3**: Change PlayerManager.__init__() to use load_players_from_json() (NEW-27 - CRITICAL)
      Spec: NEW-27 "Remove CSV loading from main entry points"
      File: league_helper/util/PlayerManager.py line 139 (was 138)
      Implementation: Change self.load_players_from_csv() → self.load_players_from_json()
      Verified: [x] Matches spec exactly

- [x] **Task 2.4**: Change reload_player_data() to use load_players_from_json() (NEW-27 - CRITICAL)
      Spec: NEW-27 "Remove CSV loading from main entry points"
      File: league_helper/util/PlayerManager.py line 599 (was 582)
      Implementation: Change self.load_players_from_csv() → self.load_players_from_json()
      Implementation: Update docstring (line 589): "from CSV file" → "from JSON files"
      Implementation: Update log message (line 593): "from CSV file" → "from JSON files"
      Verified: [x] Matches spec exactly

**After Phase 2:** Run unit tests - ✅ COMPLETE (1021/1021 in-scope tests passing)

---

### Phase 1: CSV File Deprecation (2 tasks) - ✅ COMPLETE

- [x] **Task 1.1**: Rename players.csv to players.csv.DEPRECATED
      Spec: sub_feature_08_spec.md lines 82-86, checklist CLEANUP-1
      File: data/players.csv
      Implementation: bash `mv data/players.csv data/players.csv.DEPRECATED`
      Verified: [x] File renamed successfully (114516 bytes)

- [x] **Task 1.2**: Verify players_projected.csv already marked (Sub-feature 5)
      Spec: checklist CLEANUP-2
      File: data/players_projected.csv.OLD
      Implementation: Verify file exists (already renamed by Sub-feature 5)
      Verified: [x] File exists as .OLD (114405 bytes)

- [x] **Task 1.3**: ~~Rename drafted_data.csv~~ **SKIPPED - Still Active**
      Spec: sub_feature_08_spec.md lines 85-86, checklist CLEANUP-3
      **CORRECTION:** drafted_data.csv still used by player-data-fetcher
      - League Helper now uses `drafted_by` field in JSON (Sub-feature 3)
      - Player-data-fetcher still writes to drafted_data.csv
      - File remains active, NOT deprecated
      Verified: [x] Confirmed file still needed by player-data-fetcher

**After Phase 1:** Smoke tests - ✅ COMPLETE (19/19 integration tests passing)

---

### Phase 3: Integration Testing (1 task) - ✅ COMPLETE

- [x] **Task 3.1**: Add comprehensive integration test for all modes with JSON only
      Spec: sub_feature_08_spec.md lines 92-97, checklist CLEANUP-6
      File: tests/integration/test_league_helper_integration.py
      Implementation: Added TestCSVDeprecation.test_all_modes_with_json_only() function
      Tests:
        - Removes CSV files to simulate production after deprecation
        - Verifies player_data folder exists with JSON files
        - Initializes LeagueHelperManager with JSON-only loading
        - Tests all 4 modes: Add to Roster, Starter Helper, Trade Simulator, Modify Player Data
        - Confirms no CSV files accessed during execution
      Verified: [x] Test passes (20/20 integration tests passing)

**After Phase 3:** Integration tests - ✅ COMPLETE (20/20 passing, 100% in-scope pass rate)

---

## Continuous Verification (Check every 5-10 minutes):

- [ ] "Did I consult specs.md in last 5 minutes?"
- [ ] "Can I point to exact spec line this code satisfies?"
- [ ] "Working from documentation, not memory?"
- [ ] "Checked off requirement in implementation checklist?"

**Last Updated:** 2025-12-30 (Implementation in progress)
