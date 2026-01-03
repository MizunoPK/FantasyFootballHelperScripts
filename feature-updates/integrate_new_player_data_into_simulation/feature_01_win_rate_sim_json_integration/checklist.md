# Feature 01: Win Rate Simulation JSON Integration - Planning Checklist

**Status:** ✅ ALL QUESTIONS RESOLVED (via codebase investigation)
**Created:** 2026-01-01 (Stage 2 Deep Dive)
**Last Updated:** 2026-01-01

---

## Resolution Summary

All 7 questions answered through codebase investigation. No user input required.

**See:** `research/CODEBASE_INVESTIGATION_FINDINGS.md` for complete findings.

---

## Resolved Questions

### ✅ Question 1: Week-Specific Array Index Mapping

**Answer:** Index 0 = Week 1, Index 1 = Week 2, ..., Index 16 = Week 17 (17 elements total)

**Evidence:**
- `historical_data_compiler/constants.py:88` - REGULAR_SEASON_WEEKS = 17
- `historical_data_compiler/json_exporter.py:305-328` - Array building logic with bye_idx = week - 1
- Actual JSON files have 17 elements confirmed

**Impact:** `_parse_players_json()` will use `projected_points[week_num - 1]` to extract week-specific values

---

### ✅ Question 2: Data Extraction Timing

**Answer:** Extract week-specific values DURING parsing (return single values like CSV)

**Rationale:**
- Maintains consistent interface with current `_parse_players_csv()`
- Keeps `_load_week_data()` unchanged
- JSON arrays contain week-specific logic already

**Impact:** `_parse_players_json(week_folder, week_num)` signature includes week_num parameter

---

### ✅ Question 3: Shared Directory Structure

**Answer:** Create `player_data/` subfolder in shared directories, copy 6 JSON files

**Evidence:**
- PlayerManager hardcodes: `player_data_dir = self.data_folder / 'player_data'` (PlayerManager.py:327)
- Cannot modify PlayerManager (shared with league helper)

**Impact:** `_create_shared_data_dir()` must create `shared_dir/player_data/` and copy JSON files there

---

### ✅ Question 4: PlayerManager Compatibility

**Answer:** PlayerManager DOES hardcode `player_data/` - we must create this folder structure

**Evidence:**
- PlayerManager.py:327, 342 show hardcoded path
- Simulation passes `shared_dir` as data_folder
- Files must be at `shared_dir/player_data/{position}_data.json`

**Impact:** No PlayerManager modifications needed - structure shared dirs correctly

---

### ✅ Question 5: Error Handling - Missing JSON Files

**Answer:** Different behavior for validation vs runtime

**Implementation:**
- **Validation:** Fail loud (raise FileNotFoundError) if ANY of 6 JSON files missing
- **Runtime:** Log warning and skip week (current CSV behavior)

**Impact:** `_validate_season_structure()` checks all 6 files, `_preload_week_data()` logs warnings

---

### ✅ Question 6: Field Type Conversion

**Answer:** NO conversion needed - FantasyPlayer.from_json() handles types correctly

**Evidence:**
- FantasyPlayer.py:250 - `locked = data.get('locked', False)` loads boolean directly
- FantasyPlayer.py:240 - `drafted_by = data.get('drafted_by', '')` loads string directly

**Impact:** No type conversion logic needed in simulation code

---

### ✅ Question 7: Array Length Validation

**Answer:** Arrays have 17 elements - FantasyPlayer.from_json() pads/truncates

**Evidence:**
- FantasyPlayer.py:235-237 - from_json() handles validation:
  ```python
  projected_points = (projected_points + [0.0] * 17)[:17]
  actual_points = (actual_points + [0.0] * 17)[:17]
  ```

**Impact:** No additional validation needed in simulation code

---

## Implementation Checklist

**Changes Required:**
- [x] Confirm array indexing (week_num - 1)
- [x] Confirm data extraction approach (during parsing)
- [x] Confirm shared directory structure (player_data/ subfolder)
- [x] Confirm PlayerManager compatibility (no mods needed)
- [x] Confirm error handling strategy (validation vs runtime)
- [x] Confirm field type handling (no conversion needed)
- [x] Confirm array validation approach (rely on FantasyPlayer)

**Ready for spec.md update:** ✅

---

**Next Step:** Update spec.md with concrete implementation details from findings
