# Player Data Fetcher - New Data Format - Implementation Checklist

**Instructions**: Check off EACH requirement as you implement it. Do NOT batch-check.

**Created:** 2024-12-24
**Status:** IN PROGRESS

---

## Phase 1: Infrastructure Setup

### Task 1.1: Config Settings
- [ ] REQ-1.1.1: Add CREATE_POSITION_JSON = True to config.py
      Spec: specs.md Decision 1 | USER_DECISIONS_SUMMARY.md Decision 1
      Implemented in: ___
      Verified: ___

- [ ] REQ-1.1.2: Add POSITION_JSON_OUTPUT = "../data/player_data" to config.py
      Spec: specs.md lines 60-61
      Implemented in: ___
      Verified: ___

- [ ] REQ-1.1.3: Update player_data_exporter.py imports to include new constants
      Spec: TODO Task 1.1 dependencies
      Implemented in: ___
      Verified: ___

### Task 1.2: DraftedRosterManager Method
- [ ] REQ-1.2.1: Add get_team_name_for_player() method with correct signature
      Spec: USER_DECISIONS_SUMMARY.md Decision 10, lines 156-172
      Implemented in: ___
      Verified: ___

- [ ] REQ-1.2.2: Method uses drafted_players dict for O(1) lookup
      Spec: USER_DECISIONS_SUMMARY.md Decision 10
      Implemented in: ___
      Verified: ___

- [ ] REQ-1.2.3: Method normalizes player key same as apply_drafted_state_to_players()
      Spec: specs.md Round 3 research
      Implemented in: ___
      Verified: ___

### QA Checkpoint 1: Infrastructure Ready
- [ ] Config settings exist and are accessible
- [ ] DraftedRosterManager method works correctly
- [ ] Unit tests pass for new method
- [ ] Manual testing: method returns correct values

---

## Phase 2: Core Export Logic

### Task 2.1: export_position_json_files() Method
- [ ] REQ-2.1.1: Async method that exports all 6 position files
      Spec: specs.md lines 14-19
      Implemented in: ___
      Verified: ___

- [ ] REQ-2.1.2: Uses asyncio.gather() for parallel export
      Spec: specs.md Reusable Pattern 1
      Implemented in: ___
      Verified: ___

- [ ] REQ-2.1.3: Checks CREATE_POSITION_JSON config before running
      Spec: Decision 1
      Implemented in: ___
      Verified: ___

- [ ] REQ-2.1.4: Creates output folder if doesn't exist
      Spec: specs.md output location
      Implemented in: ___
      Verified: ___

### Task 2.2: _export_single_position_json() Helper
- [ ] REQ-2.2.1: Filters players by position correctly
      Spec: specs.md lines 14-19
      Implemented in: ___
      Verified: ___

- [ ] REQ-2.2.2: Transforms each player to JSON structure
      Spec: specs.md Complete Data Structures section
      Implemented in: ___
      Verified: ___

- [ ] REQ-2.2.3: Wraps in position-specific root key
      Spec: specs.md example files analysis
      Implemented in: ___
      Verified: ___

- [ ] REQ-2.2.4: Saves to timestamped file using DataFileManager
      Spec: specs.md Reusable Pattern 3
      Implemented in: ___
      Verified: ___

### Task 2.3: _prepare_position_json_data() Transformation
- [ ] REQ-2.3.1: All common fields populated correctly
      Spec: specs.md lines 24-35
      Implemented in: ___
      Verified: ___

- [ ] REQ-2.3.2: drafted_by uses get_team_name_for_player()
      Spec: Decision 10
      Implemented in: ___
      Verified: ___

- [ ] REQ-2.3.3: locked is boolean (not 0/1)
      Spec: Transformation table
      Implemented in: ___
      Verified: ___

- [ ] REQ-2.3.4: projected_points array has exactly 17 elements
      Spec: Decision 2
      Implemented in: ___
      Verified: ___

- [ ] REQ-2.3.5: actual_points uses statSourceId=0 for past, 0 for future
      Spec: Decision 5, Decision 8
      Implemented in: ___
      Verified: ___

- [ ] REQ-2.3.6: Position-specific stat arrays included
      Spec: specs.md Complete Data Structures
      Implemented in: ___
      Verified: ___

- [ ] REQ-2.3.7: Stat arrays use correct stat IDs
      Spec: specs.md ESPN Stat ID Mappings
      Implemented in: ___
      Verified: ___

- [ ] REQ-2.3.8: Non-DST positions do NOT include ret_yds/ret_tds
      Spec: Decision 6
      Implemented in: ___
      Verified: ___

- [ ] REQ-2.3.9: Field goal structure simplified to made/missed only
      Spec: Decision 7
      Implemented in: ___
      Verified: ___

- [ ] REQ-2.3.10: All field names use correct spelling
      Spec: Decision 3, Decision 4
      Implemented in: ___
      Verified: ___

### Task 2.4: Stat Extraction Helpers
- [ ] REQ-2.4.1: _extract_weekly_stat_array() returns exactly 17 elements
      Spec: Decision 2, Decision 11
      Implemented in: ___
      Verified: ___

- [ ] REQ-2.4.2: _extract_passing_stats() returns all 6 passing stats
      Spec: specs.md ESPN Stat ID Mappings
      Implemented in: ___
      Verified: ___

- [ ] REQ-2.4.3: _extract_rushing_stats() returns all 3 rushing stats
      Spec: specs.md ESPN Stat ID Mappings
      Implemented in: ___
      Verified: ___

- [ ] REQ-2.4.4: _extract_receiving_stats() returns all 4 receiving stats
      Spec: specs.md ESPN Stat ID Mappings, Decision 3
      Implemented in: ___
      Verified: ___

- [ ] REQ-2.4.5: _extract_misc_stats() handles return stats conditionally
      Spec: Decision 6
      Implemented in: ___
      Verified: ___

- [ ] REQ-2.4.6: _extract_kicking_stats() simplified structure
      Spec: Decision 7
      Implemented in: ___
      Verified: ___

- [ ] REQ-2.4.7: _extract_defense_stats() returns all 10 defense stats
      Spec: specs.md ESPN Stat ID Mappings
      Implemented in: ___
      Verified: ___

- [ ] REQ-2.4.8: All helpers use Decision 11 (missing stats = 0)
      Spec: Decision 11
      Implemented in: ___
      Verified: ___

### Task 2.5: _get_actual_points_array() Method
- [ ] REQ-2.5.1: Returns array with exactly 17 elements
      Spec: Decision 2
      Implemented in: ___
      Verified: ___

- [ ] REQ-2.5.2: Uses actual stats for past weeks
      Spec: Decision 5, Decision 8
      Implemented in: ___
      Verified: ___

- [ ] REQ-2.5.3: Uses 0 for future weeks
      Spec: Decision 9
      Implemented in: ___
      Verified: ___

- [ ] REQ-2.5.4: Never includes null values
      Spec: Decision 11
      Implemented in: ___
      Verified: ___

### QA Checkpoint 2: Export Logic Complete
- [ ] All 6 position files created
- [ ] JSON structure matches specs
- [ ] All arrays have 17 elements
- [ ] No null values in arrays
- [ ] Non-DST files don't have ret_yds/ret_tds
- [ ] Field goal structure simplified
- [ ] Correct spelling ("receiving", "two_pt")
- [ ] Unit tests pass

---

## Phase 3: Integration

### Task 3.1: Main Workflow Integration
- [ ] REQ-3.1.1: Call export_position_json_files() if enabled
      Spec: Workflow integration
      Implemented in: ___
      Verified: ___

- [ ] REQ-3.1.2: Log file paths created
      Spec: Logging requirements
      Implemented in: ___
      Verified: ___

---

## Phase 4: Testing

### Task 4.1: DraftedRosterManager Tests
- [ ] Test: Player drafted by team 1 returns team name
- [ ] Test: Player drafted by MY_TEAM_NAME returns MY_TEAM_NAME
- [ ] Test: Free agent (drafted=0) returns empty string
- [ ] Test: Player not in drafted_data.csv returns empty string
- [ ] Test: Player with special characters normalizes and finds match

### Task 4.2: Position JSON Export Tests
- [ ] Test: export_position_json_files() creates all 6 files
- [ ] Test: CREATE_POSITION_JSON=False: no files created
- [ ] Test: Each position has correct structure
- [ ] Test: Arrays all have 17 elements
- [ ] Test: No null values in arrays
- [ ] Test: Non-DST positions don't have ret_yds/ret_tds
- [ ] Test: Field goals simplified (no distance breakdown)
- [ ] Test: Correct spelling ("receiving", "two_pt")
- [ ] Test: drafted_by field correct
- [ ] Test: locked is boolean (not 0/1)

### Task 4.3: Integration Test
- [ ] Test: Full workflow with CREATE_POSITION_JSON=True
- [ ] Test: All 6 position files created
- [ ] Test: Files can be loaded as JSON
- [ ] Test: Structure matches specs
- [ ] Test: Spot-check player data accuracy

### Task 4.4: Manual QC Validation
- [ ] All arrays have exactly 17 elements
- [ ] Unplayed weeks (Week 17) have 0 values
- [ ] QB: Check 3-5 players against internet sources
- [ ] RB: Check 3-5 players against internet sources
- [ ] WR: Check 3-5 players against internet sources
- [ ] TE: Check 3-5 players against internet sources
- [ ] K: Check 3-5 players against internet sources
- [ ] DST: Check 3-5 players against internet sources
- [ ] Week 1 and Week 16 data verified
- [ ] Week 17 is all zeros (not yet played)

### QA Checkpoint 3: All Tests Pass
- [ ] All unit tests pass (100% pass rate)
- [ ] Integration tests pass
- [ ] Manual QC complete
- [ ] No test failures

---

## Verification Log

| Requirement | Spec Location | Implementation | Verified? | Matches Spec? | Notes |
|-------------|---------------|----------------|-----------|---------------|-------|
| (To be filled in as implementation progresses) |

---

## Notes

- Keep specs.md VISIBLE at all times during coding
- Verify EACH requirement BEFORE implementing
- Verify EACH requirement AFTER implementing
- Update this checklist IMMEDIATELY after each requirement
- Run tests after EVERY phase
- Document deviations immediately in lessons_learned.md
