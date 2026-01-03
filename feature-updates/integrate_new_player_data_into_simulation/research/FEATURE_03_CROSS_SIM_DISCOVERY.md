# Feature 03: Cross-Simulation Testing - Discovery Findings

**Research Date:** 2026-01-03
**Researcher:** Agent
**Grounded In:** Epic Intent (user's requests for verification and documentation)

---

## Epic Intent Summary

**User requested:** Verify both Win Rate Sim and Accuracy Sim work correctly with JSON data, update all documentation to remove CSV references

**Components user mentioned:**
- Win Rate Sim (epic line 2, 3)
- Accuracy Sim (epic line 2, 3)
- players.csv / players_projected.csv (epic line 4) - Remove references
- Week 17 verification (epic line 8) - Both sims
- "VERIFY EVERYTHING" (epic line 10)

**This research focused on:**
1. Finding all CSV references in documentation
2. Understanding how to run simulations end-to-end
3. Mapping test structure
4. Identifying documentation files to update

---

## Component 1: Player CSV References in Documentation

**User mentioned:** "No longer try to load in players.csv or players_projected.csv" (epic line 4)

**Search conducted:** `grep -r "players.csv\|players_projected.csv" simulation/`

**Found in codebase:** 9 references across 5 files

### File 1: simulation/README.md (3 references)

**Line 69:**
```
│   ├── players_projected.csv   # Season-long projections
```

**Line 348:**
```
### "No such file or directory: players_projected.csv"
```

**Line 353:**
```
# Should show: players_projected.csv, players_actual.csv, teams_week_*.csv
```

**Source:** Documentation file
**Action needed:** Update to reflect JSON structure (player_data folder with position files)

---

### File 2: simulation/win_rate/SimulationManager.py (1 reference)

**Line 180 (docstring):**
```
        - players.csv in each week folder
```

**Source:** Docstring in SimulationManager class
**Action needed:** Update to mention JSON files instead

---

### File 3: simulation/win_rate/SimulatedLeague.py (3 references)

**Line 91 (docstring):**
```
            data_folder (Path): Path to folder containing players_projected.csv,
```

**Line 340 (docstring):**
```
        Parse players.csv into dictionary format keyed by player ID.
```

**Line 346 (docstring):**
```
            filepath (Path): Path to players.csv file
```

**Source:** Docstrings in SimulatedLeague class
**Action needed:** Update docstrings (Note: Line 340 is _parse_players_csv which Feature 01 will delete)
**Evidence:** These are from deprecated _parse_players_csv method (identified in Feature 01 research)

---

### File 4: simulation/win_rate/SimulatedOpponent.py (1 reference)

**Line 77 (docstring):**
```
            projected_pm (PlayerManager): PlayerManager using players_projected.csv
```

**Source:** Docstring in SimulatedOpponent class __init__ method
**Action needed:** Update to reflect JSON usage

---

### File 5: simulation/win_rate/DraftHelperTeam.py (1 reference)

**Line 72 (docstring):**
```
            projected_pm (PlayerManager): PlayerManager using players_projected.csv
```

**Source:** Docstring in DraftHelperTeam class __init__ method
**Action needed:** Update to reflect JSON usage

---

**Summary:** 9 player CSV references found
- 3 in README.md (documentation)
- 1 in SimulationManager.py (docstring)
- 3 in SimulatedLeague.py (docstrings, incl. deprecated method)
- 1 in SimulatedOpponent.py (docstring)
- 1 in DraftHelperTeam.py (docstring)

**Note:** Features 01 and 02 identified 4 CSV references in SimulatedLeague docstrings - this research found those + 5 additional references in other files.

---

## Component 2: Simulation Entry Points

**User mentioned:** "Both the Win Rate sim and Accuracy Sim" (epic line 2, 3)

**Search conducted:** `find . -name "run_*simulation*.py"`

**Found in codebase:**

### Entry Point 1: run_win_rate_simulation.py

**Location:** Project root
**Purpose:** Runs Win Rate Simulation
**Relevance:** Need to run this end-to-end to verify JSON loading works
**Action needed:** Run with JSON data, verify no errors, compare results to CSV baseline (if available)

---

### Entry Point 2: run_accuracy_simulation.py

**Location:** Project root
**Purpose:** Runs Accuracy Simulation
**Relevance:** Need to run this end-to-end to verify JSON loading works
**Action needed:** Run with JSON data, verify no errors, compare results to CSV baseline (if available)

---

### Entry Point 3: run_draft_order_simulation.py (NOT in scope)

**Location:** Project root
**Purpose:** Runs Draft Order Simulation
**Relevance:** NOT part of this epic (user only mentioned Win Rate and Accuracy)
**Action needed:** None (out of scope)

---

**Summary:** 2 simulation entry points to test
- run_win_rate_simulation.py (in scope)
- run_accuracy_simulation.py (in scope)

---

## Component 3: Test Structure

**User constraint:** "VERIFY EVERYTHING FOR CORRECTNESS AND COMPLETENESS" (epic line 10)

**Search conducted:** `find tests -name "*.py" -type f | wc -l` and `glob tests/**/test_*simulation*.py`

**Found in codebase:**

### Test Files Overview

**Total test files:** 95 Python test files across entire project
**Simulation-specific test files:** 5 files

### Simulation Test Files:

1. **tests/simulation/test_draft_order_simulation.py** (out of scope)
2. **tests/simulation/test_manual_simulation.py**
3. **tests/simulation/test_simulation_manager.py** (Win Rate Sim)
4. **tests/integration/test_accuracy_simulation_integration.py** (Accuracy Sim)
5. **tests/integration/test_simulation_integration.py** (Win Rate Sim integration)

### Test Runner:

**File:** tests/run_all_tests.py
**Purpose:** Runs all 2,200+ tests across project
**Relevance:** Need to verify 100% pass rate after Features 01 and 02 complete
**Command:** `python tests/run_all_tests.py` (per CLAUDE.md pre-commit protocol)

---

**Summary:** Test infrastructure exists
- 5 simulation test files (4 relevant to this epic)
- run_all_tests.py runs entire test suite
- Features 01 and 02 already identified test coverage gaps (will add tests)

---

## Component 4: Documentation Files to Update

**User mentioned:** "No longer try to load in players.csv" (epic line 4 - implicit need to update docs)

**Identified files:**

1. **simulation/README.md**
   - Lines 69, 348, 353: Update data structure section
   - Update troubleshooting section
   - Update file tree diagram

2. **Simulation module docstrings** (identified from Component 1)
   - SimulationManager.py line 180
   - SimulatedLeague.py lines 91, 340, 346 (340 will be deleted by Feature 01)
   - SimulatedOpponent.py line 77
   - DraftHelperTeam.py line 72

3. **Potential additional documentation** (to verify during implementation)
   - Inline comments mentioning CSV
   - Other README files in simulation/ subdirectories

---

## Research Completeness

**Components researched:**
- ✅ Player CSV references (grep search conducted)
- ✅ Simulation entry points (found 2 in scope)
- ✅ Test structure (95 files total, 5 simulation-specific)
- ✅ Documentation files (README + docstrings)

**Evidence collected:**
- File paths: simulation/README.md, SimulationManager.py, SimulatedLeague.py, SimulatedOpponent.py, DraftHelperTeam.py
- Line numbers: All 9 CSV references documented with line numbers
- Entry points: run_win_rate_simulation.py, run_accuracy_simulation.py
- Test runner: tests/run_all_tests.py

**Ready for Phase 1.5 audit.**

---

**Next Steps:**
- Phase 1.5: Verify research completeness (MANDATORY GATE)
- STAGE_2b Phase 2: Update spec.md with findings and create requirements
- STAGE_2c Phase 3: Interactive question resolution (testing methodology, documentation scope)
