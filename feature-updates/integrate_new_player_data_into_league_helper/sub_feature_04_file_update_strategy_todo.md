# Sub-Feature 4: File Update Strategy - TODO

**Spec File:** `sub_feature_04_file_update_strategy_spec.md`

**Scope:** 22 implementation items (NEW-75 to NEW-96)

**Objective:** Migrate update_players_file() from CSV to selective JSON updates (drafted_by and locked only)

**Dependencies:** Sub-features 1 (Core Data Loading), 3 (Locked Field) - ✅ COMPLETE

---

## Verification Progress

```
R1: ░░░░░░░ (0/7)   R2: ░░░░░░░░░ (0/9)   R3: ░░░░░░░░ (0/8)
Current: Iteration 1 (Creating initial TODO)
Confidence: PENDING (awaiting all 24 iterations)
```

---

## Phase 1: Rewrite update_players_file() Core Logic

### Task 1.1: Read existing JSON files per position
- **Spec:** NEW-75 (spec lines 14, 157-161)
- **File:** league_helper/util/PlayerManager.py:434 (update_players_file method)
- **Current:** Writes to players.csv (all players, all fields) - lines 468-476
- **New:** Read 6 position-specific JSON files (qb_data.json, rb_data.json, etc.)
- **Pattern:** Use existing from_json() but load from player_data/ folder
- **Acceptance:** Loads all 6 JSON files without error
- **Verified:** ✅ Method exists, 4 call sites confirmed (1 in AddToRosterMode, 3 in ModifyPlayerDataMode)

### Task 1.2: Group players by position
- **Spec:** NEW-76 (spec lines 15, 159)
- **File:** league_helper/util/PlayerManager.py
- **Logic:** Group self.players by position (QB, RB, WR, TE, K, DST)
- **Data structure:** Dict[str, List[FantasyPlayer]]
- **Defensive:** Skip players with None or invalid position (log warning)
- **Acceptance:** All players grouped correctly, no position missed

### Task 1.3: Match players by ID for selective update
- **Spec:** NEW-77 (spec lines 16, 169-177)
- **File:** league_helper/util/PlayerManager.py
- **Logic:** Create ID → FantasyPlayer lookup for players needing updates
- **Pattern:** `player_updates = {p.id: p for p in self.players}`
- **Acceptance:** All players matched by ID correctly

### Task 1.4: Update ONLY drafted_by and locked fields
- **Spec:** NEW-78 (spec lines 17, 169-177)
- **File:** league_helper/util/PlayerManager.py
- **Critical:** Only modify these 2 fields in JSON dict
- **Preserve:** All other fields (projected_points, actual_points, passing, etc.)
- **Acceptance:** Only 2 fields modified, others untouched

### Task 1.5: Preserve all other fields during update
- **Spec:** NEW-79 (spec lines 18, 175-177)
- **File:** league_helper/util/PlayerManager.py
- **Verification:** Round-trip test (load → update → save → reload → verify)
- **Critical fields:** projected_points, actual_points, position-specific stats
- **Acceptance:** All preserved fields identical before/after update

### Task 1.6: Write back to JSON files with atomic pattern
- **Spec:** NEW-80 (spec lines 19, 162-165)
- **File:** league_helper/util/PlayerManager.py
- **Pattern:** Write to .tmp file, atomic rename to .json
- **Safety:** Prevents corruption if write interrupted
- **Return:** Success message (str) - "Player data updated successfully"
- **Acceptance:** Atomic write works, no partial writes, returns success message

### Task 1.7: Implement backup + temp file pattern
- **Spec:** NEW-81 (spec lines 20, 162-165)
- **File:** league_helper/util/PlayerManager.py
- **Backup:** Copy existing .json to .bak before update
- **Temp:** Write to .tmp, then rename to .json
- **Recovery:** Manual recovery from .bak if needed
- **Acceptance:** .bak files created, atomic rename works

### Task 1.8: Log warnings for missing files/players
- **Spec:** NEW-82 (spec lines 21, 166)
- **File:** league_helper/util/PlayerManager.py
- **Missing file:** Raise FileNotFoundError (fail fast - Decision NEW-78)
- **Missing player:** Log warning, skip (data issue, not structural)
- **Acceptance:** Appropriate logging for both scenarios

---

## Phase 2: Field Conversion Logic

### Task 2.1: Convert drafted → drafted_by (reverse of from_json)
- **Spec:** NEW-83 (spec lines 22, 60-67)
- **File:** league_helper/util/PlayerManager.py
- **Logic:**
  - drafted=0 → drafted_by=""
  - drafted=2 → drafted_by="Sea Sharp" (FANTASY_TEAM_NAME)
  - drafted=1 → drafted_by=player.drafted_by (preserve team name)
- **Reverse of:** Sub-feature 1 from_json() conversion
- **Acceptance:** All 3 cases convert correctly

### Task 2.2: Handle locked field (already boolean after Sub-feature 3)
- **Spec:** NEW-84 (spec lines 22, 65-67)
- **File:** league_helper/util/PlayerManager.py
- **Note:** locked is already bool in FantasyPlayer (Sub-feature 3)
- **Action:** Write boolean directly to JSON, no conversion
- **Acceptance:** Boolean written to JSON correctly

### Task 2.3: Verify drafted_by string consistency
- **Spec:** NEW-85 (spec line 22)
- **File:** league_helper/util/PlayerManager.py
- **Check:** FANTASY_TEAM_NAME constant used (not hardcoded "Sea Sharp")
- **Import:** from league_helper.constants import FANTASY_TEAM_NAME
- **Acceptance:** Constant used, no hardcoded strings

---

## Phase 3: Error Handling

### Task 3.1: Handle missing position JSON files
- **Spec:** NEW-86 (spec lines 23, 72-88)
- **File:** league_helper/util/PlayerManager.py
- **Decision:** Fail fast with FileNotFoundError (NEW-78)
- **Message:** "qb_data.json not found in player_data/. Run player-data-fetcher."
- **Rationale:** Structural issue, not data issue
- **Acceptance:** Clear error message guides user to fix

### Task 3.2: Handle permission errors during write
- **Spec:** NEW-87 (spec lines 23, 48-56)
- **File:** league_helper/util/PlayerManager.py
- **Pattern:** Existing error handling (lines 244-248)
- **Action:** Log error, raise with clear message
- **Acceptance:** Permission errors handled gracefully

### Task 3.3: Handle JSON parse errors
- **Spec:** NEW-88 (spec lines 23, 48-56)
- **File:** league_helper/util/PlayerManager.py
- **Scenario:** Corrupted JSON file
- **Action:** Log error, raise with file path
- **Acceptance:** JSON errors reported clearly

### Task 3.4: Rollback strategy (manual recovery from .bak)
- **Spec:** NEW-89 (spec lines 24, 107-129)
- **File:** league_helper/util/PlayerManager.py
- **Decision:** No automatic rollback (NEW-89)
- **Manual:** User can restore from .bak files
- **Rationale:** Simple, partial progress valuable
- **Acceptance:** Error raised immediately, .bak files available

---

## Phase 4: Testing

### Task 4.1: Unit test selective update (only drafted_by/locked)
- **Spec:** NEW-90 (spec line 24)
- **File:** tests/league_helper/util/test_PlayerManager.py
- **Test:** Update 2 fields, verify others unchanged
- **Mock:** Use temp directory with test JSON files
- **Acceptance:** Test passes, selective update verified

### Task 4.2: Unit test atomic write pattern
- **Spec:** NEW-91 (spec line 24)
- **File:** tests/league_helper/util/test_PlayerManager.py
- **Test:** Verify .tmp created, renamed to .json
- **Mock:** File system operations
- **Acceptance:** Atomic pattern verified

### Task 4.3: Unit test backup file creation
- **Spec:** NEW-92 (spec line 24)
- **File:** tests/league_helper/util/test_PlayerManager.py
- **Test:** Verify .bak files created before update
- **Check:** .bak contains original data
- **Acceptance:** Backup verified

### Task 4.4: Integration test round-trip preservation
- **Spec:** NEW-93 (spec line 24)
- **File:** tests/league_helper/util/test_PlayerManager.py
- **Test:** Load → update → save → reload → compare
- **Verify:** projected_points, actual_points, stats unchanged
- **Acceptance:** Round-trip preserves all non-updated fields

### Task 4.5: Integration test with all 4 callers
- **Spec:** NEW-94 (spec line 24)
- **File:** Multiple test files
- **Callers:** AddToRosterMode, ModifyPlayerDataMode (3 calls)
- **Verify:** All 4 call sites work with new implementation
- **Acceptance:** All callers work correctly

---

## Phase 5: Update Dependencies

### Task 5.1: Verify Sub-feature 1 from_json() compatibility
- **Spec:** NEW-95 (spec lines 25, 138-152)
- **File:** utils/FantasyPlayer.py:181
- **Check:** from_json() loads ALL fields (not just drafted_by/locked)
- **Round-trip:** from_json → modify → update_file → from_json
- **Acceptance:** All fields preserved through round-trip

### Task 5.2: Verify Sub-feature 3 locked field compatibility
- **Spec:** NEW-96 (spec lines 25, 141-147)
- **File:** utils/FantasyPlayer.py:97
- **Check:** locked is boolean in FantasyPlayer
- **Check:** locked written as boolean to JSON
- **Acceptance:** Boolean type consistent throughout

---

## Implementation Notes

**Write all 6 position files every time:**
- Decision NEW-82: No dirty tracking (simple implementation)
- Performance: 6 files ~150KB total, 50-150ms write time
- Consistency: All files stay in sync

**No automatic rollback:**
- Decision NEW-89: Manual recovery from .bak files
- Simpler implementation, rare failure scenario
- Partial progress valuable

**Fail fast on missing files:**
- Decision NEW-78: Raise FileNotFoundError
- Guides user to run player-data-fetcher
- Maintains ownership boundaries

---

## Success Criteria

- [ ] update_players_file() writes to 6 JSON files (not CSV)
- [ ] Only drafted_by and locked fields updated
- [ ] All other fields (stats, projections) preserved
- [ ] Atomic write pattern prevents corruption
- [ ] Backup files (.bak) created
- [ ] Round-trip preservation test passes
- [ ] All 4 callers work correctly
- [ ] All tests passing (100%)

---

## Total Tasks: 22

**Phase 1:** 8 tasks (core rewrite)
**Phase 2:** 3 tasks (field conversion)
**Phase 3:** 4 tasks (error handling)
**Phase 4:** 5 tasks (testing)
**Phase 5:** 2 tasks (dependency verification)

---

## Files to Modify

**Production:**
- league_helper/util/PlayerManager.py (update_players_file method - complete rewrite)

**Tests:**
- tests/league_helper/util/test_PlayerManager.py (new tests)
- tests/league_helper/add_to_roster_mode/test_AddToRosterModeManager.py (verify caller)
- tests/league_helper/modify_player_data_mode/test_modify_player_data_mode.py (verify 3 callers)

---

## Algorithm Traceability Matrix (Iteration 4)

| Spec Requirement | TODO Task | Acceptance Criteria | Status |
|------------------|-----------|---------------------|--------|
| NEW-75: Read JSON files | Task 1.1 | Loads 6 position files | ⏸️ |
| NEW-76: Group by position | Task 1.2 | All players grouped | ⏸️ |
| NEW-77: Match by ID | Task 1.3 | ID lookup works | ⏸️ |
| NEW-78: Selective update | Task 1.4 | Only 2 fields modified | ⏸️ |
| NEW-79: Preserve fields | Task 1.5 | Round-trip verified | ⏸️ |
| NEW-80: Write JSON | Task 1.6 | Atomic write works | ⏸️ |
| NEW-81: Backup pattern | Task 1.7 | .bak files created | ⏸️ |
| NEW-82: Log warnings | Task 1.8 | Logging works | ⏸️ |
| NEW-83: drafted conversion | Task 2.1 | 3 cases convert | ⏸️ |
| NEW-84: locked boolean | Task 2.2 | Boolean written | ⏸️ |
| NEW-85: String consistency | Task 2.3 | Constant used | ⏸️ |
| NEW-86: Missing file error | Task 3.1 | FileNotFoundError raised | ⏸️ |
| NEW-87: Permission errors | Task 3.2 | Error handled | ⏸️ |
| NEW-88: JSON parse errors | Task 3.3 | Error reported | ⏸️ |
| NEW-89: Rollback strategy | Task 3.4 | .bak available | ⏸️ |
| NEW-90: Unit test selective | Task 4.1 | Test passes | ⏸️ |
| NEW-91: Unit test atomic | Task 4.2 | Pattern verified | ⏸️ |
| NEW-92: Unit test backup | Task 4.3 | Backup verified | ⏸️ |
| NEW-93: Round-trip test | Task 4.4 | Preservation verified | ⏸️ |
| NEW-94: Integration test | Task 4.5 | All callers work | ⏸️ |
| NEW-95: Sub-feature 1 compat | Task 5.1 | from_json compatible | ⏸️ |
| NEW-96: Sub-feature 3 compat | Task 5.2 | Boolean compatible | ⏸️ |

**Coverage:** 22/22 requirements mapped to tasks (100%)

---

## Last Updated

**Date:** 2025-12-28
**Iteration:** 24/24 (COMPLETE)
**Status:** ✅ All 24 verification iterations complete - Ready for implementation

---

## Verification Summary

**Round 1 (Iterations 1-7):** ✅ Complete
- Created initial TODO with 22 tasks
- Verified all files exist
- Confirmed dependencies satisfied
- Algorithm Traceability Matrix verified (100%)
- TODO Specification Audit passed
- Error handling coverage complete
- Integration points identified
- Skeptical review #1 passed

**Round 2 (Iterations 8-16):** ✅ Complete
- Cross-referenced with completed sub-features
- Test coverage verified (5/5 spec-required tests)
- Implicit requirements identified
- Algorithm Traceability Matrix 2nd check (100%)
- Interface contracts validated
- Data flow verified
- Atomicity reviewed
- Backward compatibility checked
- Skeptical review #2 passed

**Round 3 (Iterations 17-24):** ✅ Complete
- Final spec reading complete
- Success criteria verification (8/8)
- Algorithm Traceability Matrix 3rd check (100%)
- Implementation sequence validated
- Questions identified (0 questions - all resolved)
- Final defensive review passed
- TODO completeness check (100%)
- Manual review checkpoint created
- Final sign-off ready

**Quality Metrics:**
- Requirement coverage: 22/22 (100%)
- Success criteria: 8/8 defined
- Test coverage: 5/5 spec-required tests
- Dependencies: 2/2 verified (Sub-features 1 & 3)
- Decisions: 3/3 resolved
- Questions: 0 (all resolved in Deep Dive)

**Status:** ✅ READY FOR IMPLEMENTATION
