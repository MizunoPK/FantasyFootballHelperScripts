# Add Bye Week to Player Data - Implementation TODO

---

## 📖 Guide Reminder

**This file is governed by:** `feature-updates/guides/todo_creation_guide.md`

**Ready for implementation when:** ALL 24 iterations complete (see guide lines 87-93)

**✅ ALL PRE-IMPLEMENTATION REQUIREMENTS MET:**
- [x] All 24 iterations executed individually
- [x] Iteration 4a passed (TODO Specification Audit)
- [x] Iteration 23a passed (Pre-Implementation Spec Audit - 4 parts)
- [x] Iteration 24 passed (Implementation Readiness Checklist)
- [x] Interface verification complete (copy-pasted signatures verified)
- [x] No "Alternative:" or "May need to..." notes remain in TODO

⚠️ **If you think verification is complete, re-read guide lines 87-93 FIRST!**

⚠️ **Do NOT offer user choice to "proceed to implementation OR continue verification" - you MUST complete all 24 iterations**

---

## Iteration Progress Tracker

### Compact View (Quick Status)

```
R1: ■■■■■■■ (7/7)   R2: ■■■■■■■■■ (9/9)   R3: ■■■■■■■■ (8/8)   Extra: ■■ (2/2)
```
Legend: ■ = complete, □ = pending, ▣ = in progress

**Status:** ✅ ALL 24 ITERATIONS COMPLETE (+ 2 extra audits)
**Confidence:** VERY HIGH
**Blockers:** None
**Next:** Interface Verification (pre-implementation)

### Detailed View

| Round | Iterations | Status |
|-------|------------|--------|
| First (7) | [x]1 [x]2 [x]3 [x]4 [x]5 [x]6 [x]7 | 7/7 |
| Second (9) | [x]8 [x]9 [x]10 [x]11 [x]12 [x]13 [x]14 [x]15 [x]16 | 9/9 |
| Third (8) | [x]17 [x]18 [x]19 [x]20 [x]21 [x]22 [x]23 [x]24 | 8/8 |
| Extra | [x]4a [x]23a | 2/2 |

**All iterations complete!** Ready for Interface Verification.

---

## Protocol Execution Tracker

Track which protocols have been executed (protocols must be run at specified iterations):

| Protocol | Required Iterations | Completed |
|----------|---------------------|-----------|
| Standard Verification | 1, 2, 3, 8, 9, 10, 15, 16 | [x]1 [x]2 [x]3 [x]8 [x]9 [x]10 [x]15 [x]16 |
| Algorithm Traceability | 4, 11, 19 | [x]4 [x]11 [x]19 |
| TODO Specification Audit | 4a | [x]4a |
| End-to-End Data Flow | 5, 12 | [x]5 [x]12 |
| Skeptical Re-verification | 6, 13, 22 | [x]6 [x]13 [x]22 |
| Integration Gap Check | 7, 14, 23 | [x]7 [x]14 [x]23 |
| Fresh Eyes Review | 17, 18 | [x]17 [x]18 |
| Edge Case Verification | 20 | [x]20 |
| Test Coverage Planning + Mock Audit | 21 | [x]21 |
| Pre-Implementation Spec Audit | 23a | [x]23a |
| Implementation Readiness | 24 | [x]24 |
| Interface Verification | Pre-impl | [x] ✅ 2025-12-26 |

---

## Verification Summary

- Iterations completed: 24/24 + 2 extra = 26/26 ✅ ALL COMPLETE
- Verification rounds: 3/3 (Round 1: 7 iterations, Round 2: 9 iterations, Round 3: 8 iterations)
- Extra audits: 2/2 (4a: TODO Specification Audit, 23a: Pre-Implementation Spec Audit)
- Requirements from spec: 2 (add bye_week to 2 JSON export methods)
- Requirements in TODO: 2
- Questions for user: 0 (spec complete)
- Integration points identified: 2 (2 methods to modify)

---

## Phase 1: Add bye_week to Player-Data-Fetcher JSON Export

### Task 1.1: Add bye_week field to JSON export in player-data-fetcher
- **File:** `player-data-fetcher/player_data_exporter.py`
- **Method:** `_prepare_position_json_data()` (lines 479-535)
- **Similar to:** CSV export pattern in `historical_data_compiler/player_data_fetcher.py:94`
- **Tests:** `tests/player-data-fetcher/test_player_data_exporter.py`
- **Status:** [ ] Not started

**ACCEPTANCE CRITERIA (from specs.md):**

✓ **REQ-1:** Field added to json_data dictionary (specs.md:12-14)
  - **Exact location:** Insert new line after line 498 ("position"), before line 499 ("injury_status")
  - **Exact code:** `"bye_week": player.bye_week,`
  - **Example output:** `"bye_week": 6` or `"bye_week": null`
  - **NOT:** `"byeWeek"` or `"bye"` or any other field name ❌

✓ **REQ-2:** Field placement matches CSV column order (specs.md:94-99, 171-176)
  - **Order:** id → name → team → position → **bye_week** → injury_status → ...
  - **Verification:** Field appears after "position", before "injury_status" in JSON output
  - **NOT:** Placed at end of object or in wrong position ❌

✓ **REQ-3:** Data type is integer or null (specs.md:101-106)
  - **Type:** Use `player.bye_week` directly (Optional[int])
  - **Python handling:** json.dump() converts None → null automatically
  - **Example valid:** `"bye_week": 14` or `"bye_week": null`
  - **NOT:** `"bye_week": "14"` (string) or `"bye_week": ""` (empty string) ❌

✓ **REQ-4:** No transformation or rounding (specs.md:101-106)
  - **Implementation:** Assign attribute directly, no formatting
  - **NOT:** `round(player.bye_week)` or any processing ❌

**VERIFICATION CHECKLIST:**
- [ ] Field name exactly "bye_week" (not byeWeek or bye)
- [ ] Appears between "position" and "injury_status"
- [ ] Uses player.bye_week (no transformation)
- [ ] JSON shows integer or null (not string)
- [ ] All 6 position files (QB, RB, WR, TE, K, DST) have the field

**Reference:** Spec lines 12-14, 92-106

### QA CHECKPOINT 1: Verify JSON Export Contains bye_week
- **Status:** [ ] Not started
- **Expected outcome:** Generated JSON files contain bye_week field for all positions
- **Test command:** `python run_player_fetcher.py` (run player fetcher and check output)
- **Verify:**
  - [ ] Unit tests pass (100%)
  - [ ] JSON files generated in `data/player_data/`
  - [ ] All position files (QB, RB, WR, TE, K, DST) contain bye_week field
  - [ ] bye_week appears after "position", before "injury_status"
  - [ ] bye_week values are integers or null (not strings)
  - [ ] bye_week values match CSV export (spot-check 5-10 players)
- **If checkpoint fails:** STOP, fix issue, document in lessons learned, then re-run

---

## Phase 2: Add bye_week to Historical Data Compiler JSON Export

### Task 2.1: Add bye_week field to JSON export in historical_data_compiler
- **File:** `historical_data_compiler/json_exporter.py`
- **Method:** `_build_player_json_object()` (lines 286-349)
- **Similar to:** player-data-fetcher pattern (Task 1.1)
- **Tests:** `tests/historical_data_compiler/test_json_exporter.py`
- **Status:** [ ] Not started

**ACCEPTANCE CRITERIA (from specs.md):**

✓ **REQ-1:** Field added to player_obj dictionary (specs.md:16-19)
  - **Exact location:** Insert new line after line 341 ("position"), before line 342 ("injury_status")
  - **Exact code:** `"bye_week": player_data.bye_week,`
  - **Example output:** `"bye_week": 14` or `"bye_week": null`
  - **NOT:** `"byeWeek"` or `"bye"` or any other field name ❌

✓ **REQ-2:** Field placement matches CSV column order (specs.md:94-99, 171-176)
  - **Order:** id → name → team → position → **bye_week** → injury_status → ...
  - **Verification:** Field appears after "position", before "injury_status" in JSON output
  - **NOT:** Placed at end of object or in wrong position ❌

✓ **REQ-3:** Data type is integer or null (specs.md:101-106)
  - **Type:** Use `player_data.bye_week` directly (Optional[int])
  - **Python handling:** json.dump() converts None → null automatically
  - **Example valid:** `"bye_week": 7` or `"bye_week": null`
  - **NOT:** `"bye_week": "7"` (string) or `"bye_week": ""` (empty string) ❌

✓ **REQ-4:** No transformation or rounding (specs.md:101-106)
  - **Implementation:** Assign attribute directly, no formatting
  - **NOT:** `round(player_data.bye_week)` or any processing ❌

✓ **REQ-5:** Consistency with internal usage (specs.md:95-98)
  - **Note:** Code already uses player_data.bye_week internally (lines 327-331)
  - **Verification:** Same attribute used for JSON export
  - **NOT:** Using different source or calculation ❌

**VERIFICATION CHECKLIST:**
- [ ] Field name exactly "bye_week" (not byeWeek or bye)
- [ ] Appears between "position" and "injury_status"
- [ ] Uses player_data.bye_week (no transformation)
- [ ] JSON shows integer or null (not string)
- [ ] All 6 position files (QB, RB, WR, TE, K, DST) have the field
- [ ] Consistent with internal usage (lines 327-331)

**Reference:** Spec lines 16-19, 92-106

### QA CHECKPOINT 2: Verify Historical JSON Export Contains bye_week
- **Status:** [ ] Not started
- **Expected outcome:** Historical JSON files contain bye_week field
- **Test command:** `python compile_historical_data.py --year 2024` or check existing files in simulation/sim_data/
- **Verify:**
  - [ ] Unit tests pass (100%)
  - [ ] JSON files in `simulation/sim_data/{year}/weeks/week_{NN}/` contain bye_week
  - [ ] All position files (QB, RB, WR, TE, K, DST) contain bye_week field
  - [ ] bye_week appears after "position", before "injury_status"
  - [ ] bye_week values are integers or null
  - [ ] bye_week values are consistent with CSV exports
- **If checkpoint fails:** STOP, fix issue, document in lessons learned, then re-run

---

## Interface Contracts (Verified Pre-Implementation)

### ESPNPlayerData (player-data-fetcher)
- **Attribute:** `bye_week` - Bye week number (1-17) for player's team
- **Type:** `Optional[int]`
- **Source:** `player-data-fetcher/player_data_models.py:40`
- **Exact signature:** `bye_week: Optional[int] = None`
- **Note:** Populated from season_schedule.csv, not ESPN API
- **Verified:** [x] ✅ 2025-12-26

### PlayerData (historical_data_compiler)
- **Attribute:** `bye_week` - Bye week number (1-17) for player's team
- **Type:** `Optional[int]`
- **Source:** `historical_data_compiler/player_data_fetcher.py:76`
- **Exact signature:** `bye_week: Optional[int] = None`
- **Note:** Already used internally (lines 327-331) to zero out bye week indices
- **Verified:** [x] ✅ 2025-12-26

### FantasyPlayer (utils)
- **Attribute:** `bye_week` - Bye week number (1-17) for player's team
- **Type:** `Optional[int]`
- **Source:** `utils/FantasyPlayer.py:94`
- **Exact signature:** `bye_week: Optional[int] = None`
- **Note:** Used by player-data-fetcher (_prepare_position_json_data method)
- **Verified:** [x] ✅ 2025-12-26

### Quick E2E Validation Plan
- **Minimal test command:** Read a generated JSON file and verify bye_week field exists
- **Expected result:** Field present, integer or null, correct placement in object
- **Run before:** Full implementation begins
- **Status:** [ ] Not run

---

## Integration Matrix

| Modified Method | File | Called By | Caller File:Line | Backwards Compatible? |
|-----------------|------|-----------|------------------|-----------------------|
| _prepare_position_json_data() | player_data_exporter.py | _export_single_position_json() | player_data_exporter.py:445 | ✅ YES - Adding dict field |
| _build_player_json_object() | json_exporter.py | generate_position_json() | json_exporter.py:398 | ✅ YES - Adding dict field |

**Note:** This feature modifies existing methods only. Both modifications add a new field to a dictionary, which is backwards compatible with all callers.

---

## Algorithm Traceability Matrix

**Iteration 4 Complete** - Comprehensive mapping of all spec requirements to code:

| Spec Section | Requirement | Code Location | Implementation | Status |
|--------------|-------------|---------------|----------------|--------|
| specs.md:12-14 | Add bye_week to player-data-fetcher JSON | player_data_exporter.py:498-499 | Insert `"bye_week": player.bye_week,` after "position" line | [ ] |
| specs.md:16-19 | Add bye_week to historical compiler JSON | json_exporter.py:341-342 | Insert `"bye_week": player_data.bye_week,` after "position" line | [ ] |
| specs.md:94-99 | Field placement order | Both locations | Between "position" and "injury_status" | [ ] |
| specs.md:101-106 | Data type: Optional[int] | Both locations | Use attribute directly, no transformation | [ ] |
| specs.md:22-29 | Example JSON output with bye_week=6 | Both export methods | Output: `"bye_week": 6` or `"bye_week": null` | [ ] |
| specs.md:84-90 | Data source verification | player_data_fetcher_main.py:125-174 | Already implemented - _derive_bye_weeks_from_schedule() | ✅ Verified |
| specs.md:95-96 | Bye week data already in PlayerData model | player_data_models.py:40, player_data_fetcher.py:76 | Attribute exists: `bye_week: Optional[int] = None` | ✅ Verified |
| specs.md:184-201 | Integration: Simulation consumes JSON | simulation/*.py | Backwards compatible - adding field doesn't break consumers | ✅ Verified |
| specs.md:170-175 | Testing: Compare JSON to CSV | QA checkpoints | Spot-check: JSON bye_week matches CSV bye_week | [ ] |
| specs.md:177-182 | Testing: Verify all positions | QA checkpoints | Check QB, RB, WR, TE, K, DST files all have bye_week | [ ] |

**Total Mappings:** 10
**Verified Pre-Implementation:** 3
**To Implement:** 7

**No complex algorithms** - This is a straightforward field addition with no conditional logic or transformations.

---

## Data Flow Traces

### Requirement: Add bye_week to Player-Data-Fetcher JSON
```
Entry: run_player_fetcher.py
  → player_data_fetcher_main.py main()
  → NFLProjectionsCollector.export_data()
  → DataExporter.export_position_json_files()
  → DataExporter._export_single_position_json()
  → DataExporter._prepare_position_json_data()  ← MODIFY HERE
  → json.dump(json_data, file)
  → Output: data/player_data/{position}_data.json
```

### Requirement: Add bye_week to Historical Compiler JSON
```
Entry: compile_historical_data.py
  → generate_weekly_snapshots()
  → WeeklySnapshotGenerator._generate_week_snapshot()
  → generate_json_snapshots() [from json_exporter.py]
  → JSONSnapshotExporter.generate_position_json()
  → JSONSnapshotExporter._build_player_json_object()  ← MODIFY HERE
  → json.dump(json_objects, file)
  → Output: simulation/sim_data/{year}/weeks/week_{NN}/{position}_data.json
```

---

## Verification Gaps

Document any gaps found during iterations here:

### Round 1 Findings (Iterations 1-7)
- **No gaps identified** - All verifications passed
- Integration check (iteration 7):
  - `_prepare_position_json_data()` has 1 caller: `_export_single_position_json()` (line 445)
  - `_build_player_json_object()` has 1 caller: `generate_position_json()` (line 398)
  - Both modifications backwards compatible (adding field to dict)
  - No missing integration points
- All critical details verified correct (iteration 6)
- Data flow traces complete and accurate (iteration 5)
- Algorithm traceability matrix comprehensive (iteration 4)
- TODO specification audit passed (iteration 4a)

### Round 2 Findings (Iterations 8-16)
- **Minor corrections made:**
  - Iteration 12: Player-data-fetcher data flow trace corrected (was missing intermediate steps)
  - Iteration 14: Integration Matrix enhanced with caller information and backwards compatibility confirmation
  - Iteration 16: QA Checkpoint 2 test command corrected (compile_historical_data.py not run_historical_data_compiler.py)
- **Verifications passed:**
  - Iterations 8-10: Standard verification (spec coverage, consistency, edge cases)
  - Iteration 11: Algorithm traceability re-verified (10 mappings still complete)
  - Iteration 13: Skeptical re-verification (line numbers, acceptance criteria, Python considerations)
  - Iteration 15: Final comprehensive check (file paths, spec references)

### Round 3 Findings (Iterations 17-24)
- **Iteration 17 (Fresh Eyes Review #1):**
  - Minor improvement: Clarified "between line X and Y" to "Insert new line after line X, before line Y" for both tasks
  - All other sections verified clear and unambiguous
- **Iteration 18 (Fresh Eyes Review #2):**
  - Found outdated progress tracking (Detailed View, Protocol Tracker, Verification Summary, Progress Notes)
  - Updated all progress tracking to reflect actual state (iteration 17 complete, 18 in progress)
  - No ambiguities found in task specifications or acceptance criteria
- **Iteration 19 (Algorithm Deep Dive #3):**
  - Verified all 10 mappings in Algorithm Traceability Matrix remain accurate
  - Cross-referenced every spec section (lines 10-201) against TODO mappings - all covered
  - Confirmed no complex algorithms (simple dict field addition, no loops/conditionals)
  - 3 mappings pre-verified (data source, models, integration), 7 pending implementation
- **Iteration 20 (Edge Case Verification):**
  - Verified 10 edge cases: all covered in TODO
  - Normal values, None/null, all positions (QB-DST), mid-season team changes, invalid values
  - Null vs empty string correctly specified (JSON uses null, CSV uses "")
  - Dict ordering, trailing commas, backwards compatibility all verified
  - No missing edge case handling
- **Iteration 21 (Test Coverage Planning + Mock Audit):**
  - Verified unit tests exist for both methods (test_player_data_exporter.py, test_json_exporter.py)
  - Identified existing tests that need updates (test_build_player_json_object_structure line 243)
  - Mock strategy verified: Use tmp_path, test fixtures, real file I/O (not mocked)
  - QA checkpoints provide integration testing
  - Test coverage adequate - no gaps identified
- **Iteration 22 (Skeptical Re-verification #3):**
  - Verified all critical details against source code
  - File paths, line numbers, method names, attribute names all CORRECT
  - Field naming convention verified (snake_case: "bye_week" not "byeWeek")
  - Exact code to insert verified with trailing commas
  - Insertion points verified (after "position", before "injury_status")
  - QA checkpoint commands exist (run_player_fetcher.py, compile_historical_data.py)
  - Confidence level: VERY HIGH
- **Iteration 23 (Integration Gap Check #3):**
  - Verified all direct callers (1 caller per method - no hidden callers)
  - Verified all indirect consumers (simulation uses JSON, league helper doesn't)
  - Backwards compatibility triple-confirmed (additive change, Python ignores extra dict keys)
  - No side effects, no ripple effects, no breaking changes
  - Integration Matrix complete and accurate
- **Iteration 23a (Pre-Implementation Spec Audit - 4 parts):**
  - Part 1 (Completeness): All spec requirements in TODO ✓ (10 requirements mapped)
  - Part 2 (Ambiguity): No vague language, all instructions definitive ✓
  - Part 3 (Context): All prerequisites and assumptions documented ✓
  - Part 4 (Blockers): No implementation blockers identified ✓
  - All 4 parts passed - TODO is implementation-ready
- **Iteration 24 (Implementation Readiness Checklist - 12 criteria):**
  - ✓ All 24 iterations complete (+ 2 extra audits)
  - ✓ All 10 verification protocols executed
  - ✓ Algorithm Traceability Matrix complete (10 mappings)
  - ✓ TODO Specification Audit passed (iteration 4a)
  - ✓ Pre-Implementation Spec Audit passed (iteration 23a)
  - ✓ No ambiguous notes or blockers
  - ✓ Interface contracts documented
  - ✓ Integration points identified (2 methods, 2 callers)
  - ✓ Test coverage planned
  - ✓ Data flow traces complete
  - ✓ All verification gaps resolved
  - ✓ Confidence level: VERY HIGH
  - **Result: READY FOR IMPLEMENTATION**
- **Interface Verification (Pre-Implementation Protocol):**
  - Verified ESPNPlayerData.bye_week: `bye_week: Optional[int] = None` (player_data_models.py:40) ✓
  - Verified PlayerData.bye_week: `bye_week: Optional[int] = None` (player_data_fetcher.py:76) ✓
  - Verified FantasyPlayer.bye_week: `bye_week: Optional[int] = None` (FantasyPlayer.py:94) ✓
  - Verified _prepare_position_json_data() signature (player: FantasyPlayer) ✓
  - Verified _build_player_json_object() signature (player_data: PlayerData) ✓
  - Verified insertion points (lines 498-499, 341-342) ✓
  - Verified attribute access patterns (player.bye_week, player_data.bye_week) ✓
  - **All interfaces match TODO documentation exactly**

---

## Skeptical Re-verification Results

### Round 1 (Iteration 6)
- **Verified correct:**
  - File paths and line numbers (player_data_exporter.py:479-535, json_exporter.py:286-349)
  - Method names (_prepare_position_json_data, _build_player_json_object)
  - Attribute names (player.bye_week, player_data.bye_week)
  - Data model types (FantasyPlayer.bye_week: Optional[int], PlayerData.bye_week: Optional[int])
  - Field placement (after "position", before "injury_status" per specs.md:167)
  - No transformations needed (JSON auto-converts None → null)
  - Specs alignment (100% match to specs.md:12-13, 17-18, 22-29)
- **Corrections made:** None - all details verified correct
- **Confidence level:** HIGH - Source code verification confirms all TODO details

### Round 2 (Iteration 13)
- **Verified correct:**
  - Corrected data flow trace re-verified (complete call chain accurate)
  - Line numbers still current (498-499, 341-342 verified via grep)
  - Acceptance criteria unambiguous (field placement clear)
  - Python dict ordering preserved (insertion order maintained in 3.7+)
  - Trailing commas specified in "exact code" examples
- **Corrections made:** None - all details from Round 1 corrections still accurate
- **Confidence level:** HIGH - Two rounds of verification confirm TODO accuracy

### Round 3 (Iteration 22)
- **Verified correct:**
  - File paths: player-data-fetcher/player_data_exporter.py, historical_data_compiler/json_exporter.py
  - Line numbers: 498-499 (player_data_exporter), 341-342 (json_exporter) - re-verified via Read
  - Method names: _prepare_position_json_data (line 479), _build_player_json_object (line 286)
  - Attribute names: player.bye_week (line 40), player_data.bye_week (line 76)
  - Data types: Optional[int] = None (both models)
  - Field naming: "bye_week" (snake_case, consistent with existing fields)
  - Exact code: `"bye_week": player.bye_week,` and `"bye_week": player_data.bye_week,` (with commas)
  - QA commands: run_player_fetcher.py, compile_historical_data.py --year 2024
- **Corrections made:** None - all details accurate on third verification
- **Confidence level:** VERY HIGH - Three rounds of source code verification confirm 100% accuracy

---

## Progress Notes

Keep this section updated for session continuity:

**Last Updated:** 2025-12-26 (Interface Verification complete)
**Current Status:** ✅ ALL VERIFICATION COMPLETE - READY FOR IMPLEMENTATION
**Next Steps:** Proceed to implementation phase - execute TODO tasks 1.1 and 2.1
**Blockers:** None

**Verification Complete Summary:**
- ✅ 24 mandatory iterations (100%)
- ✅ 2 extra audits (4a, 23a)
- ✅ Interface Verification (3 interfaces + 2 methods + insertion points)
- ✅ Total: 27 verification steps complete
- ✅ Confidence: VERY HIGH
