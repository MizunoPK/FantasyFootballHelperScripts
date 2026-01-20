# Feature Specification: league_helper_debug

**Feature:** 02 - league_helper_debug
**Epic:** KAI-7 - improve_debugging_runs
**Status:** DRAFT (pending S2 deep dive)
**Estimated Size:** MEDIUM

---

## Purpose

Add non-interactive debug mode for all 5 League Helper modes, enabling automated smoke testing without user input.

---

## Discovery Context

**Based on Discovery findings:**
- League Helper has 5 modes (not 4 as originally stated) (Iteration 1)
- 2 modes already non-interactive: Starter Helper, Save Calculated Points (Iteration 2)
- 3 modes need non-interactive wrappers: Add to Roster, Trade Simulator, Modify Player Data (Iteration 2)
- User wants predefined test scenarios per mode (Q2 answer)
- Debug runs must hit real APIs (Q3 answer)
- Performance constraint: must complete in under 5 minutes

**Key design decisions from Discovery:**
- Add `--debug` flag to `run_league_helper.py`
- Each mode runs a predefined test scenario
- No user input required during debug execution

---

## Scope

### In Scope
- `--debug` flag for `run_league_helper.py`
- Non-interactive wrapper methods for each mode:
  - **Add to Roster:** Display top recommendations (skip actual drafting)
  - **Starter Helper:** Display optimal lineup (already non-interactive)
  - **Trade Simulator:** Run predefined test trade evaluation
  - **Modify Player Data:** Skip or read-only validation
  - **Save Calculated Points:** Execute (already non-interactive)
- Integration with debug_infrastructure (Feature 01)
- Verbose logging during debug execution

### Out of Scope
- Changes to normal (non-debug) mode behavior
- Mock player data
- Interactive debugging

---

## Requirements

{To be refined during S2 deep dive}

### R1: Debug Flag
- Add `--debug` argument to `run_league_helper.py`
- When flag present, run in non-interactive debug mode

### R2: Add to Roster Debug
- Initialize mode managers
- Display top N recommended players for current draft position
- Log recommendations to debug log
- Exit without user input

### R3: Starter Helper Debug
- Run `show_recommended_starters()` (already non-interactive)
- Log optimal lineup to debug log

### R4: Trade Simulator Debug
- Define predefined test trade scenario
- Evaluate trade and display results
- Exit without user input

### R5: Modify Player Data Debug
- Skip or perform read-only validation
- Log player data status

### R6: Save Calculated Points Debug
- Run `execute()` (already non-interactive)
- Log completion status

---

## Dependencies

- Feature 01 (debug_infrastructure) - for logging utilities and configuration

---

## Acceptance Criteria

{To be refined during S2 deep dive}

- [ ] `python run_league_helper.py --debug` runs without user input
- [ ] All 5 modes execute in debug mode
- [ ] Debug log file created with mode execution details
- [ ] Normal mode (`python run_league_helper.py`) still works as before
- [ ] Debug run completes in under 5 minutes

---

## Technical Notes

{To be populated during S5 implementation planning}

**Files likely to be modified:**
- `run_league_helper.py` - Add --debug flag and routing
- `league_helper/LeagueHelperManager.py` - Add debug mode methods
- Possibly individual mode managers for debug-specific logic
