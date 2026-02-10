# Research Notes: Feature 04 (accuracy_sim_logging)

**Feature:** accuracy_sim_logging
**Researched By:** Secondary-C
**Date:** 2026-02-06
**Epic:** KAI-8-logging_refactoring

---

## Research Summary

**Purpose:** Document findings from codebase research to inform spec.md requirements

**Scope Researched:**
- Entry point: `run_accuracy_simulation.py`
- Core modules: `simulation/accuracy/*.py` (5 files)
- Logger call inventory: 89 total calls across all files
- Current logging setup: Hardcoded file logging, CLI log level control

---

## Entry Point Analysis

### File: `run_accuracy_simulation.py`

**Current Logging Setup (lines 52-57):**
```python
DEFAULT_LOG_LEVEL = 'info'       # Default log level (overridable with --log-level flag)
LOGGING_TO_FILE = True           # True = log to file, False = log to console
LOG_NAME = "accuracy_simulation"
LOGGING_FILE = "./simulation/accuracy_log.txt"  # Log file path (only used if LOGGING_TO_FILE=True)
LOGGING_FORMAT = "detailed"      # detailed / standard / simple
```

**Key Findings:**
1. ✅ **Already has --log-level flag** (lines 216-224) - good precedent for --enable-log-file
2. ❌ **LOGGING_TO_FILE hardcoded to True** - needs CLI control
3. ✅ **Uses argparse** - --enable-log-file will integrate smoothly
4. ❌ **Hardcoded log path** `"./simulation/accuracy_log.txt"` - conflicts with Feature 01's `logs/accuracy_simulation/` structure
5. ✅ **setup_logger() called at line 229** - single integration point

**Current setup_logger() Call (line 229):**
```python
setup_logger(LOG_NAME, args.log_level.upper(), LOGGING_TO_FILE, LOGGING_FILE, LOGGING_FORMAT)
```

**Required Changes:**
1. Add `--enable-log-file` flag to argparse (after line 224)
2. Change `LOGGING_TO_FILE = True` → `LOGGING_TO_FILE = False` (line 54) - OFF by default per user requirement Q4
3. Update setup_logger() call (line 229) to:
   ```python
   setup_logger(LOG_NAME, args.log_level.upper(), args.enable_log_file, None, LOGGING_FORMAT)
   ```
   - Pass `args.enable_log_file` instead of hardcoded True
   - Pass `None` for log_file_path to let LoggingManager auto-generate path (Feature 01 integration contract)
4. Remove or comment out `LOGGING_FILE` constant (line 56) - no longer needed

**Integration Contract with Feature 01:**
- Logger name: `"accuracy_simulation"` (becomes folder name `logs/accuracy_simulation/`)
- log_file_path: `None` (let LoggingManager generate path)
- log_to_file: CLI-driven via `args.enable_log_file`

---

## Module Analysis

### File: `simulation/accuracy/AccuracySimulationManager.py`

**Logger Calls Found:** 58 calls
- `logger.info()`: 29 calls
- `logger.warning()`: 16 calls
- `logger.debug()`: 13 calls
- `logger.error()`: 0 calls

**Logger Setup (lines 35, 98):**
```python
from utils.LoggingManager import get_logger
# ...
self.logger = get_logger()  # Line 98
```

**Key Logging Patterns:**

**INFO Level (29 calls):**
- Initialization: "Initializing AccuracySimulationManager" (line 99)
- Phase transitions: "Starting weekly accuracy optimization" (line 587)
- Resume operations: "Resuming from parameter N" (lines 597, 735)
- Parameter completion summaries (lines 643, 769-770, 880-902)
- Save operations: "Saved optimal configs to..." (lines 460, 562, 701, 703, 871)

**DEBUG Level (13 calls):**
- State checks: "No intermediate folders found" (line 216)
- Validation logic: "Folder X: param Y not in parameter order" (line 253)
- Resume decisions: "All parameters complete (idx...)" (line 283)
- Cleanup operations: "Deleted: folder_name" (line 613)

**WARNING Level (16 calls):**
- Missing data: "Projected folder not found" (lines 327, 331)
- Incomplete state: "Skipping incomplete folder..." (line 262)
- Error conditions: "Failed to load intermediate results" (line 602)
- Signal handling: "Received signal N, initiating graceful shutdown" (line 172)

**Log Quality Assessment:**
- ✅ INFO: Good coverage of major operations (start, resume, completion, save)
- ✅ DEBUG: Appropriate for tracing parameter optimization logic
- ✅ WARNING: Proper use for missing data and error conditions
- ⚠️ **Potential Improvements:**
  - DEBUG: Add entry/exit for complex methods (e.g., `_find_resume_point()`, `_load_projected_data()`)
  - INFO: Add configuration summary at initialization
  - DEBUG: Add parameter value logging for test iterations

---

### File: `simulation/accuracy/AccuracyResultsManager.py`

**Logger Calls Found:** 23 calls
- `logger.info()`: 16 calls
- `logger.warning()`: 3 calls
- `logger.debug()`: 4 calls
- `logger.error()`: 0 calls

**Logger Setup (line 306):**
```python
self.logger.info(f"AccuracyResultsManager initialized: {output_dir}")
```

**Key Logging Patterns:**

**INFO Level (16 calls):**
- Initialization: "AccuracyResultsManager initialized" (line 306)
- New bests: "New best MAE for week_X" (lines 357, 367)
- Save operations: Large block at lines 433-563 with detailed save progress
- Load operations: "Loaded N intermediate configs" (line 792)

**DEBUG Level (4 calls):**
- Add result: "add_result(week_X): MAE=..." (line 347)
- Config parsing: "Loaded week_X from..." (line 785)
- Skip reasons: "Skipped filename - not accuracy format" (line 790)

**WARNING Level (3 calls):**
- Missing files: "No league_config.json found in baseline" (line 468)
- Missing folders: "Intermediate folder not found" (line 751)
- Missing baseline: "Baseline file NOT found" (line 560)

**Log Quality Assessment:**
- ✅ INFO: Excellent coverage of save/load operations with detailed progress
- ✅ DEBUG: Good tracing of result additions
- ⚠️ **Potential Improvements:**
  - DEBUG: Add entry/exit for `get_summary()` method
  - INFO: Add summary stats at initialization (baseline config count, etc.)

---

### File: `simulation/accuracy/AccuracyCalculator.py`

**Logger Calls Found:** 19 calls
- `logger.info()`: 2 calls
- `logger.warning()`: 5 calls
- `logger.debug()`: 12 calls
- `logger.error()`: 0 calls

**Logger Setup (line 77):**
```python
self.logger.debug("AccuracyCalculator initialized")
```

**Key Logging Patterns:**

**DEBUG Level (12 calls):**
- Initialization: "AccuracyCalculator initialized" (line 77)
- Calculation results: "calculate_mae: MAE=..." (line 123)
- Season aggregation: "Aggregated N players across M seasons" (line 174)
- Ranking metrics: Detailed accuracy breakdowns (lines 206, 221, 397, 438, 459, 509)
- Data availability: "Not enough X players for Y" (lines 368, 496)

**INFO Level (2 calls):**
- Season-level summaries: "Season X: projected=Y, actual=Z" (lines 227, 233)

**WARNING Level (5 calls):**
- Empty data: "No valid players for MAE calculation" (line 117)
- Missing weeks: "Week N data missing, skipping" (line 159)
- No comparisons: "No valid comparisons for position" (line 393)
- Correlation issues: "Could not calculate correlation" (lines 504, 516)

**Log Quality Assessment:**
- ✅ DEBUG: Excellent tracing of calculation logic with before/after values
- ✅ INFO: Good season-level summaries
- ✅ WARNING: Proper use for data quality issues
- ⚠️ **Potential Improvements:**
  - DEBUG: Could reduce verbosity inside tight loops (ranking metrics)
  - INFO: Add MAE thresholds (e.g., "MAE below target threshold")

---

### File: `simulation/accuracy/ParallelAccuracyRunner.py`

**Logger Calls Found:** 11 calls
- `logger.info()`: 7 calls
- `logger.warning()`: 3 calls
- `logger.error()`: 1 call
- `logger.debug()`: 0 calls

**Key Logging Patterns:**

**INFO Level (7 calls):**
- Config completion: "━━━ Config Complete: X ━━━" (lines 80-84) - 5 calls for horizons
- Start message: "Starting parallel evaluation" (line 374)
- Executor info: "Using ProcessPoolExecutor with N workers" (line 375)
- Cancellation: "All workers cancelled" (line 416)

**WARNING Level (3 calls):**
- Missing data: "Projected folder not found" (line 235)
- Path issues: "sim_data_path.parent does not exist" (line 239)
- Missing files: "Missing position file" (line 275)

**ERROR Level (1 call):**
- Execution failure: "Config evaluation failed" (line 406)

**Log Quality Assessment:**
- ✅ INFO: Good parallel execution progress tracking
- ✅ ERROR: Proper exception logging with exc_info=True
- ⚠️ **Potential Improvements:**
  - DEBUG: Add worker activity tracing (which worker processing which config)
  - DEBUG: Add queue depth monitoring
  - INFO: Add completion rate statistics (X/Y configs evaluated)

---

## Logger Call Inventory Summary

| Module | Total | INFO | DEBUG | WARNING | ERROR |
|--------|-------|------|-------|---------|-------|
| AccuracySimulationManager | 58 | 29 | 13 | 16 | 0 |
| AccuracyResultsManager | 23 | 16 | 4 | 3 | 0 |
| AccuracyCalculator | 19 | 2 | 12 | 5 | 0 |
| ParallelAccuracyRunner | 11 | 7 | 0 | 3 | 1 |
| **TOTAL** | **111** | **54** | **29** | **27** | **1** |

**Distribution Analysis:**
- INFO: 48.6% - Good coverage of major operations
- DEBUG: 26.1% - Reasonable tracing detail
- WARNING: 24.3% - Proper use for data quality issues
- ERROR: 0.9% - Only in ParallelAccuracyRunner (exception handling)

---

## Log Quality Improvement Opportunities

### High Priority (Apply During S6)

**1. AccuracySimulationManager:**
- Add DEBUG entry/exit for `_find_resume_point()` (complex resume logic)
- Add INFO configuration summary at initialization (baseline, num params, test values)
- Add DEBUG parameter value logging for each test iteration

**2. ParallelAccuracyRunner:**
- Add DEBUG worker activity tracing (which worker processing which config)
- Add INFO completion rate statistics (X/Y configs evaluated)

**3. All modules:**
- Review DEBUG calls inside loops - ensure not excessive (throttle if needed)
- Add INFO script start/complete with full configuration

### Medium Priority (Consider During S6)

**4. AccuracyCalculator:**
- Reduce DEBUG verbosity inside tight loops (ranking metrics)
- Add DEBUG data transformation tracing (before/after projected points)

**5. AccuracyResultsManager:**
- Add DEBUG entry/exit for `get_summary()` method
- Add INFO summary stats at initialization

### Low Priority (Optional)

**6. General:**
- Consider adding ERROR level for critical failures (currently only 1 ERROR call)
- Consider standardizing message formats (some use "━━━" decoration, others don't)

---

## Integration Points with Feature 01

**Feature 01 Provides:**
- `LineBasedRotatingHandler` class (500-line rotation, 50-file cleanup)
- Modified `setup_logger()` function with `log_to_file` parameter
- `logs/{script_name}/` folder structure (auto-created)
- Timestamped filenames: `{script_name}-{YYYYMMDD_HHMMSS}.log`

**Feature 04 Must Follow Integration Contracts:**

**Contract 1: Logger Name = Folder Name**
- Current: `LOG_NAME = "accuracy_simulation"` (line 55 in run_accuracy_simulation.py)
- Result: `logs/accuracy_simulation/` folder created
- ✅ **Compliant** - consistent naming

**Contract 2: log_file_path = None**
- Current: `LOGGING_FILE = "./simulation/accuracy_log.txt"` (line 56)
- Required: Pass `None` to let LoggingManager auto-generate path
- ❌ **Must Change** - remove hardcoded path

**Contract 3: log_to_file Driven by CLI**
- Current: `LOGGING_TO_FILE = True` (hardcoded, line 54)
- Required: `log_to_file=args.enable_log_file` (CLI-driven)
- ❌ **Must Change** - add --enable-log-file flag, wire to setup_logger()

---

## Test Impact Analysis

**Test Files to Review:**
```bash
tests/simulation/accuracy/
├── test_AccuracyCalculator.py
├── test_AccuracyResultsManager.py
├── test_AccuracySimulationManager.py
└── test_ParallelAccuracyRunner.py
```

**Potential Test Updates:**

**1. Logger Mock Assertions:**
- Tests may assert specific logger.info/debug/warning calls
- New logs added = assertions need updating
- Log format changes = assertion strings need updating

**2. setup_logger() Call Assertions:**
- Tests may verify setup_logger() called with specific args
- Signature change (LOGGING_FILE → None) = update assertions
- New parameter (enable_log_file) = update test mocks

**3. CLI Argument Tests:**
- Add tests for --enable-log-file flag parsing
- Verify default=False behavior
- Verify flag=True enables file logging

**4. Integration Tests:**
- Verify logs/ folder created (not simulation/accuracy_log.txt)
- Verify timestamped filenames generated
- Verify 500-line rotation works

---

## Code Locations for Implementation

**Files to Modify:**

1. **run_accuracy_simulation.py**
   - Line 54: Change `LOGGING_TO_FILE = True` → `LOGGING_TO_FILE = False`
   - Line 56: Remove or comment `LOGGING_FILE = "./simulation/accuracy_log.txt"`
   - After line 224: Add --enable-log-file argument to argparse
   - Line 229: Update setup_logger() call:
     ```python
     # OLD:
     setup_logger(LOG_NAME, args.log_level.upper(), LOGGING_TO_FILE, LOGGING_FILE, LOGGING_FORMAT)

     # NEW:
     setup_logger(LOG_NAME, args.log_level.upper(), args.enable_log_file, None, LOGGING_FORMAT)
     ```

2. **simulation/accuracy/AccuracySimulationManager.py**
   - Review 58 logger calls for quality improvements (per above recommendations)
   - Add DEBUG entry/exit for complex methods
   - Add INFO configuration summary at initialization

3. **simulation/accuracy/ParallelAccuracyRunner.py**
   - Review 11 logger calls for quality improvements
   - Add DEBUG worker activity tracing
   - Add INFO completion rate statistics

4. **simulation/accuracy/AccuracyCalculator.py**
   - Review 19 logger calls for quality improvements
   - Check for excessive DEBUG in loops
   - Add data transformation tracing

5. **simulation/accuracy/AccuracyResultsManager.py**
   - Review 23 logger calls for quality improvements
   - Add DEBUG entry/exit for key methods

**Files to Create/Update (Tests):**
- `tests/simulation/accuracy/test_accuracy_cli_logging.py` (NEW - CLI flag tests)
- Update existing tests for logger mock assertions

---

## Open Questions for checklist.md

**Q1:** Should we update ALL 111 logger calls for quality, or focus on high-priority improvements only?
- Option A: Update all (comprehensive, but time-consuming)
- Option B: High-priority only (faster, addresses main issues)
- **Recommendation:** Option B (high-priority) - ~20-30 log statements

**Q2:** Should ParallelAccuracyRunner add DEBUG worker activity tracing (which worker processing which config)?
- May be verbose with 8 workers × hundreds of configs
- Useful for debugging parallel execution issues
- **Recommendation:** Yes, but with throttling (log every Nth config, not every single one)

**Q3:** Should we standardize message decoration (some use "━━━", others don't)?
- Current mix: ParallelAccuracyRunner uses "━━━", others use plain text
- **Recommendation:** Keep existing styles (cosmetic, low priority)

**Q4:** Should we add ERROR-level logging for critical failures beyond ParallelAccuracyRunner?
- Current: Only 1 ERROR call across all modules
- Missing: Initialization failures, file I/O errors
- **Recommendation:** Add ERROR for critical failures (e.g., baseline config load failure)

---

## Completion Checklist

- [x] Researched entry point (run_accuracy_simulation.py)
- [x] Researched core modules (5 files in simulation/accuracy/)
- [x] Documented logger call inventory (111 total calls)
- [x] Identified integration contracts with Feature 01
- [x] Documented code locations for implementation
- [x] Identified test impact
- [x] Created open questions for checklist.md
- [ ] Draft spec.md with requirements (NEXT)
- [ ] Create checklist.md with questions (NEXT)
- [ ] Run Validation Loop (NEXT)

---

**End of Research Notes**
