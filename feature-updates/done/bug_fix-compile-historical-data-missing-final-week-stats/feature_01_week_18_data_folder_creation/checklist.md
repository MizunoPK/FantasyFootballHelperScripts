# Feature 01: week_18_data_folder_creation - Planning Checklist

**Part of Epic:** bug_fix-compile-historical-data-missing-final-week-stats
**Last Updated:** 2025-12-31 12:03

**Purpose:** Track open questions and decisions for this feature

**Instructions:**
- [ ] = Open question (needs user answer)
- [x] = Resolved (answer documented below)

---

## Open Questions

### Question 1: Implementation Approach for Week 18 Creation

**Status:** [x] RESOLVED - Option B selected

**Context:**
The compile script uses `REGULAR_SEASON_WEEKS = 17` constant to control folder creation. We need to create a week_18 folder, but I need your guidance on the approach.

**Options:**

**Option A: Modify REGULAR_SEASON_WEEKS constant to 18**
- Change `constants.py` line 88: `REGULAR_SEASON_WEEKS = 18`
- Pros: Simple, automatically creates week_18 everywhere
- Cons: May affect other parts of the system that depend on this constant
- Risk: UNKNOWN - need to search codebase for all uses of REGULAR_SEASON_WEEKS

**Option B: Add separate VALIDATION_WEEKS constant**
- Keep `REGULAR_SEASON_WEEKS = 17` (semantically correct - NFL has 17 weeks)
- Add new `VALIDATION_WEEKS = 18` for data compilation
- Update folder creation to use VALIDATION_WEEKS
- Pros: Semantically clearer, doesn't change existing constant
- Cons: Two constants to maintain, slightly more complex

**Option C: Special case in folder creation only**
- Keep `REGULAR_SEASON_WEEKS = 17`
- Add explicit week_18 folder creation after the loop
- Pros: Minimal changes, clear special-case handling
- Cons: Not as clean, week_18 handled differently

**My Recommendation:**
I recommend **Option B** (separate VALIDATION_WEEKS constant) because:
- Semantically correct: NFL regular season IS 17 weeks
- Week 18 folder is for validation/actuals only, not a "regular season week"
- Clearer intent in code
- Safer: doesn't risk breaking other parts that use REGULAR_SEASON_WEEKS

**Question for you:**
Which option do you prefer? (A, B, C, or suggest different approach)

**Impact on Implementation:**
- Option A: 2 file changes (constants.py, maybe others if issues found)
- Option B: 3 file changes (constants.py, compile_historical_data.py, weekly_snapshot_generator.py)
- Option C: 2 file changes (compile_historical_data.py, weekly_snapshot_generator.py)

---

### Question 2: Week 18 Snapshot Data Content

**Status:** [x] RESOLVED - Option A selected

**Context:**
Week 18 folder will contain data for validation of week 17 performance. I need clarity on what data it should contain.

**Options:**

**Option A: All actuals through week 17, NO projections**
- Week 18 `players.csv`: Actual points for weeks 1-17, no projected data
- Week 18 `players_projected.csv`: Same as players.csv (all actuals, no projections)
- Reasoning: Season is over, no future weeks to project
- Simplest for simulation validation

**Option B: Follow normal pattern (actuals 1-17, projections 18+)**
- Week 18 `players.csv`: Actuals 1-17, projected 0.0 for week 18+ (no games exist)
- Week 18 `players_projected.csv`: Follow normal point-in-time projection logic
- Reasoning: Maintains consistency with other week folders
- More complex, but consistent

**Option C: Minimal validation data only**
- Week 18 folder contains only actual week 17 results
- Simpler files, just enough for validation
- Reasoning: Week 18 is special-purpose, doesn't need full snapshot format

**My Recommendation:**
I recommend **Option A** (all actuals, no projections) because:
- Season is over after week 17 - no future weeks to project
- Simplest for simulation to use (just read actual values)
- Still maintains file format compatibility (same CSV columns)
- Clear semantics: week_18 = final actuals

**Question for you:**
Which option do you prefer? (A, B, C, or suggest different approach)

**Impact on Implementation:**
- Option A: Modify `_generate_week_snapshot()` to handle week 18 as special case (all actuals)
- Option B: No special logic needed, week 18 follows normal pattern
- Option C: New simplified file format (more changes, less consistency)

---

### Question 3: File Format for Week 18

**Status:** [x] RESOLVED - Option A selected

**Context:**
Other week folders contain both CSV and JSON files. Week 18 should maintain consistency, but I want to confirm.

**Options:**

**Option A: Full format (CSV + JSON, all positions)**
- Generate same files as other weeks:
  - `players.csv`
  - `players_projected.csv`
  - `qb_data.json`, `rb_data.json`, `wr_data.json`, `te_data.json`, `k_data.json`, `dst_data.json`
- Pros: Complete consistency, no special cases in file reading
- Cons: More files (but script already generates them)

**Option B: CSV only**
- Generate only CSV files
- Skip JSON generation for week 18
- Pros: Simpler, week 18 is validation-only
- Cons: Inconsistent with other weeks

**Option C: Minimal (one file with actuals)**
- Single file with week 17 actual results
- Pros: Smallest footprint
- Cons: Breaks format consistency, requires special reading logic

**My Recommendation:**
I recommend **Option A** (full format) because:
- Compile script already supports both CSV and JSON via flags
- No additional complexity - just generate one more week
- Maintains perfect consistency with weeks 1-17
- Future-proof if other tools need week 18 data

**Question for you:**
Which option do you prefer? (A, B, C)

**Impact on Implementation:**
- Option A: No special logic, week 18 uses same file generation
- Option B: Add flag to skip JSON for week 18
- Option C: New file format, new generation logic

---

## Resolved Questions

### Question 1: Implementation Approach for Week 18 Creation
- [x] **RESOLVED:** Option B - Add separate VALIDATION_WEEKS constant

**User's Answer:** "b"

**Implementation Impact:**
- Keep `REGULAR_SEASON_WEEKS = 17` (semantically correct - NFL regular season)
- Add new constant: `VALIDATION_WEEKS = 18` in `constants.py`
- Update `create_output_directories()` to use `VALIDATION_WEEKS` for folder creation loop
- Update `generate_all_weeks()` to use `VALIDATION_WEEKS` for snapshot generation loop
- Week 18 folder will be created and populated like weeks 1-17, but represents validation data

**Files to modify:**
1. `historical_data_compiler/constants.py` - Add VALIDATION_WEEKS = 18
2. `compile_historical_data.py` - Use VALIDATION_WEEKS in create_output_directories()
3. `historical_data_compiler/weekly_snapshot_generator.py` - Use VALIDATION_WEEKS in generate_all_weeks()

### Question 2: Week 18 Snapshot Data Content
- [x] **RESOLVED:** Option A - All actuals through week 17, NO projections

**User's Answer:** "A"

**Implementation Impact:**
- Week 18 `players.csv`: Contains actual points for weeks 1-17 ONLY (no projections)
- Week 18 `players_projected.csv`: Same as players.csv (all actuals, no projections)
- Season is over after week 17, so no future weeks to project
- Simplest for simulation validation - just read actual values
- Maintains file format compatibility (same CSV columns as other weeks)

**Code changes needed:**
- Modify `_generate_week_snapshot()` to detect week 18
- For week 18: Use actual points for all weeks 1-17, no projected data
- Both players.csv and players_projected.csv will be identical for week 18
- Special case: `if current_week == 18: use all actuals, no projections`

### Question 3: File Format for Week 18
- [x] **RESOLVED:** Option A - Full format (CSV + JSON, all positions)

**User's Answer:** "A"

**Implementation Impact:**
- Week 18 generates same files as weeks 1-17:
  - `players.csv`
  - `players_projected.csv`
  - `qb_data.json`, `rb_data.json`, `wr_data.json`, `te_data.json`, `k_data.json`, `dst_data.json`
- Complete consistency with other week folders
- No special file format logic needed
- Compile script's GENERATE_CSV and GENERATE_JSON flags apply to week 18 same as other weeks

**Code changes needed:**
- NO special logic needed for file format
- Week 18 uses same file generation as weeks 1-17
- `json_exporter.py` will automatically work for week 18 (no changes needed)

---

## Checklist Status

**Open Questions:** 0
**Resolved Questions:** 3
**Blocking Questions:** None (all questions resolved)

**Next Action:** Evaluate for new questions, then proceed to Phase 4 (Scope Adjustment)

---

## Notes

- All 3 questions are interconnected
- Question 1 answer affects implementation complexity
- Question 2 affects spec.md data structure section
- Question 3 affects testing strategy
- Will update spec.md immediately after each question is answered
