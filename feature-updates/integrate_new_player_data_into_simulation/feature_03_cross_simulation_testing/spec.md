# Feature 03: Cross-Simulation Testing and Documentation

---

## Epic Intent (User's Original Request)

**⚠️ CRITICAL:** All requirements below MUST trace back to this section.

**Problem This Feature Solves:**

This feature provides the final verification gate for the epic - ensuring both Win Rate Sim and Accuracy Sim work correctly with JSON data through comprehensive testing and documentation updates.

**Source:** Derived from epic requirements (lines 2, 10) + Stage 1 epic breakdown

---

**User's Implicit Requests (for Cross-Simulation Testing):**

1. **Both simulations must work correctly with JSON:**
   "Both the Win Rate sim and Accuracy Sim should maintain the same functionality as before they were broken by the json file introduction"
   (Source: Epic notes line 2)

   **Implication:** Need to test BOTH simulations end-to-end to verify they work correctly

2. **Verify everything for correctness:**
   "ASSUME ALL PREVIOUS WORK IS INCORRECT OR INCOMPLETE AND VERIFY EVERYTHING FOR CORRECTNESS AND COMPLETENESS"
   (Source: Epic notes line 10)

   **Implication:** Need comprehensive testing to verify Features 01 and 02 work correctly

3. **Remove CSV references:**
   "No longer try to load in players.csv or players_projected.csv"
   (Source: Epic notes line 4)

   **Implication:** Need to update documentation/code to remove all CSV references

---

**User's Constraints:**

- "Both the Win Rate sim and Accuracy Sim should maintain the same functionality as before they were broken by the json file introduction"
  (Source: Epic notes line 2 - no regressions from CSV baseline)

- "ASSUME ALL PREVIOUS WORK IS INCORRECT OR INCOMPLETE AND VERIFY EVERYTHING FOR CORRECTNESS AND COMPLETENESS"
  (Source: Epic notes line 10 - comprehensive verification required)

---

**Out of Scope (User Explicitly Excluded):**

- Changes to Win Rate Sim implementation (Feature 01 scope)
  (Source: Feature 03 depends on Feature 01 being complete)

- Changes to Accuracy Sim implementation (Feature 02 scope)
  (Source: Feature 03 depends on Feature 02 being complete)

- Changes to JSON file structure or format
  (Source: Implicit - user says "accommodate" changes, not create new format)

- New simulation features beyond maintaining existing functionality
  (Source: Epic notes line 2 - "maintain the same functionality")

---

**User's End Goal:**

"Both the Win Rate sim and Accuracy Sim should maintain the same functionality as before they were broken by the json file introduction, but now it will access data a bit differently"
(Source: Epic notes line 2)

User wants both simulations to work correctly with JSON data, with no regressions from CSV baseline, and all documentation updated to reflect the migration.

---

**Technical Components Mentioned by User:**

- **players.csv / players_projected.csv** (Epic notes line 4) - Must remove all references
- **Win Rate Sim** (Epic notes line 2, 3) - Must verify works with JSON
- **Accuracy Sim** (Epic notes line 2, 3) - Must verify works with JSON
- **Week 17 logic** (Epic notes line 8) - Must verify in both sims
- **Simulation module** (Epic notes line 1) - Code location

---

**Stage 1 Scope Derived from Epic:**

Feature 03 was created during Stage 1 epic breakdown to handle:
1. **End-to-end testing** - Run both simulations with JSON data, verify results
2. **Documentation updates** - Update all docstrings, READMEs, comments to reflect JSON migration
3. **Final verification** - Confirm zero CSV references, all tests pass, no regressions

**Source:** Stage 1 epic planning + derived requirements from epic intent

---

**Agent Verification:**

- [x] Re-read epic notes file: 2026-01-03
- [x] Re-read Feature 03 README (Stage 1 scope): 2026-01-03
- [x] Extracted exact quotes (not paraphrases)
- [x] Cited line numbers for all quotes
- [x] Identified out-of-scope items
- [x] Understand user's goal (verify both sims work, update docs, final QC gate)

---

---

## Requirements

### Requirement 1: Run End-to-End Win Rate Simulation with JSON

**Description:** Execute Win Rate Simulation using JSON data with limited weeks (quick smoke test) and verify it completes successfully without errors

**Source:** Epic Request + User Answer
**Epic Citation:** Line 2: "Both the Win Rate sim and Accuracy Sim should maintain the same functionality"
**Epic Citation:** Line 10: "VERIFY EVERYTHING FOR CORRECTNESS AND COMPLETENESS"
**User Answer:** Question 1 (Option B) - "Quick Smoke Test (Faster)"
**Traceability:** Direct user request + verification constraint + user decision for testing scope

**Implementation:**
- Run `run_win_rate_simulation.py` with JSON data for weeks 1, 10, and 17 only
- Use minimal/default configuration (skip exhaustive parameter combinations)
- Verify simulation completes without FileNotFoundError for CSV files
- Verify simulation uses JSON data from week_X folders
- Verify Week 17 logic works correctly (uses week_18 for actuals)
- Compare JSON results to CSV baseline outputs if available (win rates, optimal configs)
- Document results (focus on errors, Week 17 verification, and baseline comparison)
- Estimated time: ~5 minutes (simulation) + ~5 minutes (comparison if baseline exists)

**Success Criteria:**
- Simulation runs to completion without errors
- No CSV file errors (FileNotFoundError)
- Week 17 data correctly loaded from week_18
- Key outputs generated (no need to validate all intermediate calculations)
- Results match CSV baseline if available (win rates within reasonable tolerance)

---

### Requirement 2: Run End-to-End Accuracy Simulation with JSON

**Description:** Execute Accuracy Simulation using JSON data with limited weeks (quick smoke test) and verify it completes successfully without errors

**Source:** Epic Request + User Answer
**Epic Citation:** Line 2: "Both the Win Rate sim and Accuracy Sim should maintain the same functionality"
**Epic Citation:** Line 10: "VERIFY EVERYTHING FOR CORRECTNESS AND COMPLETENESS"
**User Answer:** Question 1 (Option B) - "Quick Smoke Test (Faster)"
**Traceability:** Direct user request + verification constraint + user decision for testing scope

**Implementation:**
- Run `run_accuracy_simulation.py` with JSON data for weeks 1, 10, and 17 only
- Use minimal/default configuration (skip exhaustive parameter combinations)
- Verify simulation completes without FileNotFoundError for CSV files
- Verify simulation uses JSON data through PlayerManager
- Verify Week 17 logic works correctly (uses week_18 for actuals)
- Compare JSON results to CSV baseline outputs if available (MAE scores, optimal configs)
- Document results (focus on errors, Week 17 verification, and baseline comparison)
- Estimated time: ~5 minutes (simulation) + ~5 minutes (comparison if baseline exists)

**Success Criteria:**
- Simulation runs to completion without errors
- No CSV file errors (FileNotFoundError)
- Week 17 data correctly loaded from week_18
- Key outputs generated (accuracy metrics calculated)
- Results match CSV baseline if available (MAE scores within reasonable tolerance)

---

### Requirement 3: Verify All Unit Tests Pass

**Description:** Run complete test suite (2,200+ tests) and verify 100% pass rate

**Source:** User Constraint
**Epic Citation:** Line 10: "VERIFY EVERYTHING FOR CORRECTNESS AND COMPLETENESS"
**Traceability:** Comprehensive verification requirement

**Implementation:**
- Run `python tests/run_all_tests.py`
- Verify exit code 0 (100% pass rate)
- Document any test failures
- Verify simulation tests specifically pass
- No regressions from Features 01 and 02 changes

**Success Criteria:**
- All 2,200+ tests pass (100% pass rate)
- Exit code 0
- No test failures related to JSON migration
- Simulation integration tests pass

---

### Requirement 4: Update simulation/README.md

**Description:** Comprehensively update simulation module README to remove all CSV references, add detailed JSON structure documentation, and ensure accuracy and completeness

**Source:** Epic Request + User Answer
**Epic Citation:** Line 4: "No longer try to load in players.csv or players_projected.csv"
**User Answer:** Question 3 (Option B) - "Comprehensive Updates (Most Thorough)"
**Traceability:** Direct user request + user decision for documentation scope

**Implementation:**

**Part 1: Remove CSV References (3 locations)**
- Line 69: Change file tree diagram to show player_data/ folder with JSON files
- Line 348: Update troubleshooting section (change "players_projected.csv" error to JSON equivalent)
- Line 353: Update file listing examples to show JSON files

**Part 2: Add Detailed JSON Structure Documentation**
- Add comprehensive section explaining JSON file structure:
  - 6 position files per week (QB.json, RB.json, WR.json, TE.json, K.json, DST.json)
  - Location: data/player_data/week_X/ folders
  - Array fields: drafted_by, locked, projected_points, actual_points (17 elements each)
  - Week_N+1 pattern: For week N, load projected from week_N, actual from week_N+1

**Part 3: Add CSV → JSON Migration Guide**
- Add section explaining transition from CSV to JSON (dated 2025-12-30)
- Document key differences: single CSV files → per-position JSON files
- Document field structure change: single columns → 17-element arrays
- Note: Migration already complete, guide for historical context

**Part 4: Update All Examples**
- Update file tree diagram to show player_data/ structure
- Update all code examples to use JSON file paths
- Update troubleshooting scenarios with JSON-specific errors

**Part 5: Comprehensive Accuracy Review**
- Review entire README for outdated information
- Verify all instructions accurate for JSON-based workflow
- Update any stale references to old data structures

**Files Affected:**
- simulation/README.md (comprehensive rewrite of data structure sections)

**Success Criteria:**
- Zero references to players.csv or players_projected.csv
- Detailed JSON structure section added
- CSV → JSON migration guide added
- All examples updated to use JSON
- Troubleshooting section comprehensive and accurate
- File tree diagram shows player_data/ folder structure
- Entire README reviewed and verified accurate

---

### Requirement 5: Update Simulation Docstrings

**Description:** Comprehensively update all simulation module docstrings to remove CSV references, document JSON usage pattern, and ensure clarity and accuracy

**Source:** Epic Request + User Answer
**Epic Citation:** Line 4: "No longer try to load in players.csv or players_projected.csv"
**User Answer:** Question 3 (Option B) - "Comprehensive Updates (Most Thorough)"
**Traceability:** Direct user request + user decision for documentation scope

**Implementation:**

**Part 1: Update CSV References (6 locations)**
- **SimulationManager.py line 180:** Update to mention JSON files in week folders
  - Change from: "players.csv in each week folder"
  - Change to: "6 position JSON files (QB, RB, WR, TE, K, DST) in player_data/week_X folders"

- **SimulatedLeague.py line 91:** Update data_folder parameter description
  - Change from: "Path to folder containing players_projected.csv"
  - Change to: "Path to data folder containing player_data/ with JSON files for each week"

- **SimulatedLeague.py line 346:** Will be deleted by Feature 01 (deprecated _parse_players_csv method)
  - Verify deletion during Feature 01 implementation

- **SimulatedOpponent.py line 77:** Update projected_pm parameter description
  - Change from: "PlayerManager using players_projected.csv"
  - Change to: "PlayerManager using JSON files from player_data/ folder"

- **DraftHelperTeam.py line 72:** Update projected_pm parameter description
  - Change from: "PlayerManager using players_projected.csv"
  - Change to: "PlayerManager using JSON files from player_data/ folder"

**Part 2: Ensure Comprehensive Documentation**
- Review all updated docstrings for clarity
- Add details about JSON structure where helpful (array indexing, week_N+1 pattern)
- Verify docstrings match actual implementation
- Ensure consistent terminology across all files

**Files Affected:**
- simulation/win_rate/SimulationManager.py (1 reference)
- simulation/win_rate/SimulatedLeague.py (2 references - 1 will be deleted by Feature 01)
- simulation/win_rate/SimulatedOpponent.py (1 reference)
- simulation/win_rate/DraftHelperTeam.py (1 reference)

**Success Criteria:**
- All docstrings updated to reflect JSON usage
- No references to players.csv or players_projected.csv in active code
- Docstrings accurately and comprehensively describe PlayerManager JSON loading
- Consistent terminology used across all docstrings
- Clear explanations of JSON structure where relevant

---

### Requirement 6: Verify Zero CSV References Remain

**Description:** Search entire simulation/ directory and verify no player CSV file references remain

**Source:** Epic Request
**Epic Citation:** Line 4: "No longer try to load in players.csv or players_projected.csv"
**Traceability:** Direct user request

**Implementation:**
- Run: `grep -r "players\.csv\|players_projected\.csv" simulation/`
- Verify zero results (or only game_data.csv, season_schedule.csv - not player files)
- Check inline comments for CSV mentions
- Verify deprecated code removed by Feature 01

**Success Criteria:**
- Zero player CSV file references in simulation/ directory
- Only legitimate CSV files mentioned (game_data, season_schedule)
- Grep search returns zero player CSV results

---

**Requirements Summary:**

Total Requirements: 6
- ✅ Requirement 1: Epic request (line 2, 10) - Run Win Rate Sim end-to-end
- ✅ Requirement 2: Epic request (line 2, 10) - Run Accuracy Sim end-to-end
- ✅ Requirement 3: User constraint (line 10) - Verify all tests pass
- ✅ Requirement 4: Epic request (line 4) - Update simulation/README.md
- ✅ Requirement 5: Epic request (line 4) - Update simulation docstrings
- ✅ Requirement 6: Epic request (line 4) - Verify zero CSV references

All requirements traced to sources.

---

## Testing Strategy

**Three-Part Verification:**

### Part 1: End-to-End Simulation Testing
- Run Win Rate Simulation with JSON data
- Run Accuracy Simulation with JSON data
- Verify both complete without errors
- Compare results to CSV baseline (if available)
- Document any differences or issues

### Part 2: Unit Test Verification
- Run complete test suite: `python tests/run_all_tests.py`
- Verify 100% pass rate (2,200+ tests)
- Check simulation-specific tests pass
- Document any failures

### Part 3: Documentation Verification
- Search for remaining CSV references: `grep -r "players\.csv\|players_projected\.csv" simulation/`
- Verify zero player CSV references found
- Review updated documentation for accuracy
- Verify all docstrings updated

---

## Completion Criteria

**This feature is complete when:**

- [ ] Win Rate Simulation runs successfully with JSON data (no errors)
- [ ] Accuracy Simulation runs successfully with JSON data (no errors)
- [ ] All 2,200+ unit tests pass (100% pass rate)
- [ ] simulation/README.md updated (3 CSV references removed)
- [ ] All docstrings updated (6 CSV references removed)
- [ ] Grep search shows zero player CSV references in simulation/
- [ ] Week 17 logic verified in both simulations
- [ ] Results match or exceed CSV baseline (if available)
- [ ] Documentation accurately reflects JSON structure
