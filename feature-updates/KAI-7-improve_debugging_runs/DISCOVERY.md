# Discovery Document: improve_debugging_runs

**Epic:** KAI-7 - improve_debugging_runs
**Status:** IN PROGRESS
**Time-Box:** 2-3 hours (MEDIUM epic)

---

## Epic Request Summary

User wants easier test runs for scripts, automated smoke testing, and "debugging version runs" that create log files. Goal is to enable agents to test independently without user interaction.

**Components mentioned:**
- Every mode in League helper (4 modes)
- Player data fetcher
- Win Rate Sim
- Accuracy Sim
- Historical Data fetcher (game_data_fetcher)
- Schedule Data Fetcher

**Original Request:** `improve_debugging_runs_notes.txt`

---

## Discovery Log

| Timestamp | Activity | Outcome |
|-----------|----------|---------|
| 2026-01-20 10:30 | Initialized Discovery | Epic size MEDIUM, time-box 2-3 hours |
| 2026-01-20 10:30 | Epic Analysis complete | Identified 6 component groups |
| 2026-01-20 11:00 | User answered Q1-Q4 | Debug = all features, predefined scenarios, real APIs, timestamped logs |
| 2026-01-20 11:15 | Iteration 2 research | Found 2 modes already non-interactive, 3 need wrappers |
| 2026-01-20 11:20 | Discovery Loop exit | No new questions, synthesis complete |

---

## Pending Questions

| # | Question | Context | Asked |
|---|----------|---------|-------|

---

## Resolved Questions

| # | Question | Answer | Impact | Resolved |
|---|----------|--------|--------|----------|
| 1 | What does "debugging version run" mean? | All of the above: reduced data/iterations + verbose logging + non-interactive execution | Full debug mode includes all three aspects | 2026-01-20 |
| 2 | For League Helper, what should debug mode do? | Run each mode with a predefined test scenario (e.g., Add to Roster drafts first recommended player) | Need to define test scenarios for all 5 modes | 2026-01-20 |
| 3 | Should debug runs hit real APIs? | Yes, hit real APIs - validates actual connectivity | Data fetchers will make real API calls in debug mode | 2026-01-20 |
| 4 | Where should debug logs go? | Timestamped logs (e.g., `./logs/debug_2026-01-20_103000.log`) | Create logs/ directory, timestamp each run | 2026-01-20 |

---

## Research Iterations

### Iteration 1 (2026-01-20 10:30)

**Researched:** Current state of each entry point script

**Files Examined:**
- `run_league_helper.py` (lines 1-69): Subprocess wrapper, passes DATA_FOLDER arg
- `run_win_rate_simulation.py` (lines 1-421): CLI with modes (single/full/iterative), already has --sims flag
- `run_accuracy_simulation.py` (lines 1-319): CLI with argparse, has --test-values, --baseline
- `run_game_data_fetcher.py` (lines 1-173): CLI with --season, --weeks, --output args
- `run_schedule_fetcher.py` (lines 1-64): Async fetcher, minimal args
- `run_player_fetcher.py`: Not yet examined

**Key Findings:**

1. **Win Rate Sim already has "single" mode** for quick testing:
   - `run_win_rate_simulation.py single --sims 5` runs baseline config with few simulations
   - Already produces log output

2. **Accuracy Sim has similar quick-test capability**:
   - `--test-values 3` reduces parameter grid
   - Has `--log-level debug` flag

3. **Data fetchers are NOT interactive** - they already run via CLI args:
   - Game data fetcher: `--weeks 1` limits data fetched
   - Schedule fetcher: Just runs, no reduction option

4. **League Helper is INTERACTIVE** - the main challenge:
   - Uses subprocess to run `LeagueHelperManager.py`
   - Has menu-based mode selection
   - Each mode likely has its own interactive elements

**Questions Identified:**
- How to make League Helper modes non-interactive?
- Should debug mode run a single predefined test scenario per mode?
- Where should debug logs be written?

---

### Iteration 2 (2026-01-20 11:15)

**Researched:** League Helper mode entry points and existing non-interactive patterns

**Files Examined:**
- `league_helper/LeagueHelperManager.py` (lines 140-216): Mode delegation methods
- `utils/LoggingManager.py` (lines 1-80): Existing logging infrastructure with file rotation

**Key Findings:**

1. **Two modes are already non-interactive:**
   - `show_recommended_starters()` - Just displays lineup, no user input during execution
   - `execute()` (Save Calculated Points) - Just saves, no user input

2. **Three modes are interactive:**
   - `start_interactive_mode()` (Add to Roster) - Menu-driven player selection
   - `run_interactive_mode()` (Trade Simulator) - Interactive trade building
   - `start_interactive_mode()` (Modify Player Data) - Interactive data editing

3. **Existing logging infrastructure** supports:
   - File logging with rotation
   - Multiple format levels (detailed/standard/simple)
   - Per-module logger naming

4. **Simulations have existing debug-friendly modes:**
   - Win Rate: `single --sims 1` already does single-config test
   - Accuracy: `--test-values 1` already reduces grid

**Questions Identified:** None - have clear picture of implementation approach.

---

## Solution Options

### Option 1: Unified Debug Runner Script

**Description:** Single `run_debug_tests.py` script that orchestrates all component debug runs sequentially.

**Pros:**
- Single command runs everything
- Centralized logging and reporting
- Easy for agents to use

**Cons:**
- All-or-nothing approach
- Longer total runtime

**Effort Estimate:** MEDIUM

### Option 2: Per-Component Debug Flags

**Description:** Add `--debug` flag to each existing run_*.py script.

**Pros:**
- Granular control
- Minimal new files
- Leverages existing scripts

**Cons:**
- Must remember different commands per component
- No unified reporting

**Effort Estimate:** MEDIUM

### Option 3: Combined Approach

**Description:** Add `--debug` flags to individual scripts AND create unified runner that calls them.

**Pros:**
- Flexibility (run all or run one)
- Unified reporting available
- Individual testing possible

**Cons:**
- More code to maintain
- Some duplication

**Effort Estimate:** MEDIUM-HIGH

---

## Recommended Approach

**Recommendation:** Option 3 - Combined Approach

**Rationale:**
- User wants agents to test independently (supports unified runner)
- User wants component-level testing (supports individual flags)
- Existing CLI patterns support adding flags
- Maximum flexibility for different use cases

**Key Design Decisions:**
1. **Debug flag convention:** `--debug` or `--smoke-test` on all run_*.py scripts
2. **Unified runner:** `run_debug_tests.py` calls all components
3. **Timestamped logs:** `./logs/debug_YYYY-MM-DD_HHMMSS.log`
4. **League Helper non-interactive wrappers:** New methods that skip user input
5. **Success criteria:** Exit code 0 = pass, non-zero = fail

---

## Scope Definition

### In Scope
- `--debug` flag for all 6 component types
- Unified `run_debug_tests.py` script
- Non-interactive test scenarios for League Helper modes
- Timestamped debug log files in `./logs/`
- Reduced iterations/data for all debug runs
- Verbose logging during debug runs
- Exit code reporting (0 = success)
- **Performance constraint: Full debug run under 5 minutes** (especially important for simulations)

### Out of Scope
- Mock data support (real APIs will be used)
- GUI or visual debugging tools
- Comprehensive test framework integration
- Performance benchmarking

### Deferred (Future Work)
- Mock data option for offline testing
- Parallel debug execution
- Debug result database/history

---

## Proposed Feature Breakdown

**Total Features:** 3
**Implementation Order:** Sequential (Feature 1 first, then 2, then 3)

### Feature 1: debug_infrastructure

**Purpose:** Shared debug utilities, logging setup, and configuration used by all debug runs.

**Scope:**
- `utils/debug_utils.py` - Debug logging setup, timestamped log creation
- Debug configuration constants (iterations, verbosity)
- Common success/failure detection patterns
- Exit code handling utilities

**Dependencies:** None (foundation feature)

**Discovery Basis:**
- Based on Finding: Existing LoggingManager supports file logging (Iteration 2)
- Based on User Answer: Timestamped logs requested (Q4)

**Estimated Size:** SMALL

### Feature 2: league_helper_debug

**Purpose:** Non-interactive debug mode for all 5 League Helper modes.

**Scope:**
- `--debug` flag for `run_league_helper.py`
- Non-interactive wrapper methods for each mode:
  - Add to Roster: Display recommendations (skip actual drafting)
  - Starter Helper: Display optimal lineup (already non-interactive)
  - Trade Simulator: Run predefined test trade scenario
  - Modify Player Data: Skip (read-only debug)
  - Save Calculated Points: Execute (already non-interactive)
- Debug logging integration

**Dependencies:** Feature 1 (debug_infrastructure)

**Discovery Basis:**
- Based on Finding: 2 modes already non-interactive, 3 need wrappers (Iteration 2)
- Based on User Answer: Predefined test scenarios per mode (Q2)

**Estimated Size:** MEDIUM

### Feature 3: unified_debug_runner

**Purpose:** Single script that runs all debug tests and reports results.

**Scope:**
- `run_debug_tests.py` - Orchestrates all debug runs
- `--debug` flags added to simulation and fetcher scripts
- Calls each component with debug flags
- Aggregates results and generates summary report
- Exit code 0 if all pass, non-zero if any fail

**Dependencies:** Features 1 and 2

**Discovery Basis:**
- Based on User Answer: All-in-one debug mode requested (Q1 = "all of the above")
- Based on Finding: Simulations already have reduced-run modes (Iteration 1)

**Estimated Size:** MEDIUM

---

## User Approval

**Discovery Approved:** YES
**Approved Date:** 2026-01-20
**Approved By:** User

**Approval Notes:**
User approved recommended approach (combined --debug flags + unified runner) and 3-feature breakdown.

---
