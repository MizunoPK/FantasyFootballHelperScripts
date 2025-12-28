# Add Bye Week to Player Data - Implementation Checklist

**Purpose:** Continuous spec verification during implementation

**Created:** 2025-12-26

---

## Spec Requirements Verification

Track which spec requirements are satisfied by implementation:

| Spec Reference | Requirement | Implemented | Verified |
|----------------|-------------|-------------|----------|
| specs.md:12-14 | Add bye_week to player-data-fetcher JSON | [x] | [x] |
| specs.md:16-19 | Add bye_week to historical compiler JSON | [x] | [x] |
| specs.md:94-99 | Field placement: after "position", before "injury_status" | [x] | [x] |
| specs.md:101-106 | Data type: Optional[int], no transformation | [x] | [x] |
| specs.md:22-29 | Output format example (bye_week: 6 or null) | [x] | [x] |

---

## Task 1.1: Add bye_week to Player-Data-Fetcher

**File:** `player-data-fetcher/player_data_exporter.py`
**Method:** `_prepare_position_json_data()` (lines 479-535)

### Acceptance Criteria Checklist

- [x] **REQ-1:** Field added to json_data dictionary
  - [x] Exact location: After line 498 ("position"), before line 499 ("injury_status")
  - [x] Exact code: `"bye_week": player.bye_week,`
  - [x] Example output verified: `"bye_week": 6` or `"bye_week": null`
  - [x] NOT: `"byeWeek"` or `"bye"` ❌

- [x] **REQ-2:** Field placement matches CSV column order
  - [x] Order verified: id → name → team → position → **bye_week** → injury_status
  - [x] NOT: Placed at end or wrong position ❌

- [x] **REQ-3:** Data type is integer or null
  - [x] Uses `player.bye_week` directly (Optional[int])
  - [x] JSON auto-converts None → null
  - [x] Example valid: `"bye_week": 14` or `"bye_week": null`
  - [x] NOT: `"bye_week": "14"` (string) or `""` (empty string) ❌

- [x] **REQ-4:** No transformation or rounding
  - [x] Implementation: Assign attribute directly
  - [x] NOT: `round(player.bye_week)` or any processing ❌

### Post-Implementation Verification

- [x] Code change matches TODO exactly
- [x] Specs.md requirement satisfied (lines 12-14)
- [x] No deviation from planned implementation

---

## Task 2.1: Add bye_week to Historical Compiler

**File:** `historical_data_compiler/json_exporter.py`
**Method:** `_build_player_json_object()` (lines 286-349)

### Acceptance Criteria Checklist

- [x] **REQ-1:** Field added to player_obj dictionary
  - [x] Exact location: After line 341 ("position"), before line 342 ("injury_status")
  - [x] Exact code: `"bye_week": player_data.bye_week,`
  - [x] Example output verified: `"bye_week": 14` or `"bye_week": null`
  - [x] NOT: `"byeWeek"` or `"bye"` ❌

- [x] **REQ-2:** Field placement matches CSV column order
  - [x] Order verified: id → name → team → position → **bye_week** → injury_status
  - [x] NOT: Placed at end or wrong position ❌

- [x] **REQ-3:** Data type is integer or null
  - [x] Uses `player_data.bye_week` directly (Optional[int])
  - [x] JSON auto-converts None → null
  - [x] Example valid: `"bye_week": 7` or `"bye_week": null`
  - [x] NOT: String or empty string ❌

- [x] **REQ-4:** No transformation or rounding
  - [x] Implementation: Assign attribute directly
  - [x] NOT: Processing or formatting ❌

- [x] **REQ-5:** Consistency with internal usage
  - [x] Note: Code already uses player_data.bye_week internally (lines 327-331)
  - [x] Verification: Same attribute used for JSON export
  - [x] NOT: Using different source ❌

### Post-Implementation Verification

- [x] Code change matches TODO exactly
- [x] Specs.md requirement satisfied (lines 16-19)
- [x] No deviation from planned implementation

---

## Unit Tests

- [x] All existing tests pass (100%) - **2,369/2,369 tests passed**
- [x] player-data-fetcher tests pass (17/17)
- [x] historical_data_compiler tests pass (14/14)

---

## QA Checkpoints

### QA Checkpoint 1: Player-Data-Fetcher JSON Export

- [ ] Test command executed: `python run_player_fetcher.py`
- [ ] Unit tests pass (100%)
- [ ] JSON files generated in `data/player_data/`
- [ ] All 6 position files contain bye_week (QB, RB, WR, TE, K, DST)
- [ ] bye_week appears after "position", before "injury_status"
- [ ] bye_week values are integers or null (not strings)
- [ ] bye_week values match CSV export (spot-check 5-10 players)

### QA Checkpoint 2: Historical Compiler JSON Export

- [ ] Test command executed: `python compile_historical_data.py --year 2024` or check existing files
- [ ] Unit tests pass (100%)
- [ ] JSON files in `simulation/sim_data/{year}/weeks/week_{NN}/` contain bye_week
- [ ] All 6 position files contain bye_week (QB, RB, WR, TE, K, DST)
- [ ] bye_week appears after "position", before "injury_status"
- [ ] bye_week values are integers or null
- [ ] bye_week values consistent with CSV exports

---

## Final Verification

- [ ] All spec requirements implemented
- [ ] All acceptance criteria met
- [ ] All unit tests passing
- [ ] All QA checkpoints passed
- [ ] No deviations from specs or TODO
- [ ] Ready for post-implementation QC

---

## Notes

Track any deviations, issues, or lessons learned during implementation:

(Add notes here as implementation progresses)
