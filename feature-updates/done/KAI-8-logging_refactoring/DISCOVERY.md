# Discovery Phase: logging_refactoring

**Epic:** KAI-8-logging_refactoring
**Created:** 2026-02-06
**Last Updated:** 2026-02-06
**Status:** COMPLETE

---

## Epic Request Summary

User wants to improve logging infrastructure across all major scripts with centralized log management (root-level `logs/` folder with script-specific subfolders), automated log rotation (500-line cap per file, create new file when exceeded), automated cleanup (max 50 logs per folder, auto-delete oldest), quality improvements to Debug/Info level logs, and CLI toggle for file logging on/off per script.

**Original Request:** `logging_refactoring_notes.txt`

---

## Discovery Questions

### Resolved Questions

| # | Question | Answer | Impact | Resolved |
|---|----------|--------|--------|----------|
| 1 | Should we preserve existing log file naming pattern (YYYYMMDD) or switch to full timestamps? | Use full timestamp YYYYMMDD_HHMMSS (Option B) | Log files will support multiple logs per day, more precise tracking | 2026-02-06 |
| 2 | Should line-based rotation be lazy (check on each write) or eager (pre-count lines)? | Eager - maintain counter in memory (Option B) | Better performance, requires state tracking in handler | 2026-02-06 |
| 3 | How should we handle Debug/Info log quality evaluation - what are the criteria? | Agent to propose criteria based on research | Will research logging best practices and propose evaluation framework | 2026-02-06 |
| 4 | Should CLI flag be --enable-log-file or --disable-log-file (default on/off)? | File logging OFF by default, use --enable-log-file (Option A) | Users must explicitly opt-in to file logging, avoids unwanted disk usage | 2026-02-06 |
| 5 | Are there any scripts beyond the 6 mentioned that need logging updates? | Just those 6 for now | Limits scope to: league_helper, player-data-fetcher, accuracy_sim, win_rate_sim, historical_data_compiler, schedule-data-fetcher | 2026-02-06 |
| 6 | Should log quality improvements be limited to main scripts or system-wide? | System-wide - all modules (Option B) | Broader scope, affects league_helper/, simulation/, utils/, player-data-fetcher/ modules | 2026-02-06 |
| 7 | Should counter persist across script restarts or reset? | Counter resets on restart - each script run creates new log file starting at line 0 | Simpler implementation, aligns with timestamped file-per-run model | 2026-02-06 |

### Pending Questions

{No pending questions currently}

---

## Research Findings

### Iteration 1 (2026-02-06 19:00) - Initial Reconnaissance

**Researched:** Existing logging infrastructure, main scripts, LoggingManager implementation

**Files Examined:**
- `utils/LoggingManager.py` (lines 1-174): Centralized logging manager with RotatingFileHandler (10MB, 5 backups), auto-generated timestamped paths (YYYYMMDD format), global singleton pattern
- `run_league_helper.py` (lines 1-69): Wrapper script using subprocess, no CLI arguments, no direct logging setup
- `run_player_fetcher.py` (lines 1-52): Similar wrapper pattern, subprocess-based
- `run_accuracy_simulation.py` (lines 38, 152-229): Uses setup_logger from LoggingManager, has --log-level CLI precedent, imports argparse
- `run_win_rate_simulation.py` (lines 24, 117): Uses setup_logger, hardcoded LOGGING_TO_FILE constant
- `run_schedule_fetcher.py` (line 28): Main script with async
- `run_game_data_fetcher.py` (lines 106-109): Conditional logging setup

**Key Findings:**
1. **LoggingManager exists** - Centralized logging infrastructure already in place with:
   - setup_logger() convenience function (used by all scripts)
   - RotatingFileHandler for size-based rotation (10MB default, 5 backups)
   - Auto-generated timestamped log paths with _generate_log_file_path()
   - Standard formats (DETAILED, STANDARD, SIMPLE)
   - Parameters: log_to_file, log_file_path, max_file_size, backup_count

2. **Current rotation strategy** - Size-based (10MB, 5 backups) using RotatingFileHandler
   - **Needs change**: Epic requires line-based (500 lines, 50 max files)
   - **Needs change**: Cleanup strategy (delete oldest beyond 50, not just 5 backups)

3. **Script patterns vary**:
   - Some use subprocess wrappers (run_league_helper.py, run_player_fetcher.py)
   - Some are direct entry points (run_accuracy_simulation.py, run_win_rate_simulation.py)
   - run_accuracy_simulation.py has --log-level CLI argument (good precedent)
   - Most use hardcoded LOGGING_TO_FILE constants (need CLI toggle)

4. **Log file organization** - Currently scattered (each script may specify own path)
   - **Needs change**: Epic requires centralized `logs/` folder with script subfolders

5. **Timestamp format** - Currently YYYYMMDD (daily rotation pattern)
   - **Question**: Epic says "timestamped .log file" - keep YYYYMMDD or use YYYYMMDD_HHMMSS?

6. **Test coverage exists** - tests/utils/test_LoggingManager.py needs updates

**Questions Identified:**
- Q1: Timestamp format (YYYYMMDD vs full timestamp)?
- Q2: Line-based rotation implementation (lazy vs eager)?
- Q3: Debug/Info log quality criteria?
- Q4: CLI flag default (enable vs disable)?
- Q5: Script coverage completeness?
- Q6: Log quality scope (main scripts vs system-wide)?

---

### Iteration 2 (2026-02-06 19:15) - Handler Research & Script Mapping

**Researched:** Line-based rotation implementation approaches, script mapping confirmation, log quality scope

**Files Examined:**
- `utils/LoggingManager.py` (lines 95-143): Current RotatingFileHandler implementation (maxBytes/backupCount), _generate_log_file_path uses YYYYMMDD format
- Python logging.handlers: Available handlers include RotatingFileHandler (size-based), TimedRotatingFileHandler (time-based), but no built-in line-based handler
- `compile_historical_data.py`: Confirmed as historical_data_compiler script
- System-wide log scan: 939 logger.debug/info calls across 60 files

**Key Findings:**
1. **Custom handler needed** - No built-in line-based rotation handler in Python logging
   - Must subclass logging.Handler or extend RotatingFileHandler
   - Eager counter implementation: Track line count in memory, rotate when threshold reached
   - Need to handle counter persistence across restarts (or reset per session)

2. **Script mapping confirmed**:
   - league_helper → run_league_helper.py (subprocess wrapper)
   - player-data-fetcher → run_player_fetcher.py (subprocess wrapper)
   - accuracy_sim → run_accuracy_simulation.py (direct entry, has --log-level precedent)
   - win_rate_sim → run_win_rate_simulation.py (direct entry)
   - historical_data_compiler → compile_historical_data.py (direct entry, 17 debug/info calls)
   - schedule-data-fetcher → run_schedule_fetcher.py (async main)

3. **Log quality scope is significant** - System-wide affects:
   - 60 files with debug/info logging
   - 939 total logger.debug/info calls
   - Modules: league_helper/ (10+ managers), simulation/ (accuracy + win_rate), utils/, player-data-fetcher/, historical_data_compiler/

4. **Timestamp format change** - Need to update _generate_log_file_path:
   - Current: `{name}_{YYYYMMDD}.log` (e.g., PlayerManager_20260206.log)
   - New: `{name}_{YYYYMMDD_HHMMSS}.log` (e.g., league_helper-20260206_143522.log)

5. **Folder structure** - Need to implement:
   - Root: `logs/` folder
   - Subfolders: `logs/league_helper/`, `logs/player-data-fetcher/`, etc.
   - Max 50 logs per subfolder, delete oldest

**Questions Identified:**
- None (user answers covered these areas)

---

### Iteration 3 (2026-02-06 19:20) - Log Quality Criteria Proposal

**Researched:** Logging best practices, existing log patterns in codebase, quality evaluation framework

**Sample Log Patterns Examined:**
- Examined existing debug/info logs across multiple modules
- Patterns vary: Some verbose, some minimal, inconsistent formatting
- Examples of good patterns: Entry/exit tracing, data values, error context
- Examples of poor patterns: Redundant messages, missing context, overly verbose loops

**Key Findings:**

1. **Proposed Log Quality Evaluation Criteria:**

   **DEBUG Level Criteria:**
   - **Purpose**: Enable developers to trace data flow and function execution
   - **Quality Metrics**:
     - ✅ Function entry/exit with parameters (not excessive - only for complex flows)
     - ✅ Data transformations with before/after values
     - ✅ Conditional branch taken (which if/else path executed)
     - ✅ Loop iterations for critical operations (with throttling for large loops)
     - ❌ NOT every single variable assignment
     - ❌ NOT logging inside tight loops without throttling
     - ❌ NOT redundant messages (e.g., "entering function" + "starting process" for same thing)

   **INFO Level Criteria:**
   - **Purpose**: Provide runtime awareness of script execution progress and outcomes
   - **Quality Metrics**:
     - ✅ Script start/complete with configuration
     - ✅ Major phase transitions (e.g., "Starting data fetch", "Beginning analysis")
     - ✅ Significant outcomes (e.g., "Processed 150 players", "Simulation complete: 10 leagues")
     - ✅ User-relevant warnings (e.g., "Using cached data from yesterday")
     - ❌ NOT implementation details (that's DEBUG)
     - ❌ NOT every function call
     - ❌ NOT technical jargon without context

2. **Evaluation Process per File:**
   - Review each debug/info call in context
   - Apply criteria checklist
   - Mark for: KEEP (good), UPDATE (needs improvement), REMOVE (redundant/excessive)
   - Propose specific improvements

3. **Expected Impact:**
   - 939 log calls across 60 files
   - Estimate: 60-70% KEEP, 20-25% UPDATE, 10-15% REMOVE
   - Focus on high-traffic modules first (PlayerManager, simulation managers)

4. **Test Coverage:**
   - Log quality improvements will affect test assertions
   - May need to update test files that check log output
   - Estimated 10-20 test files affected

**Questions Identified:**
- None

---

### Iteration 4 (2026-02-06 19:25) - Solution Design

**Researched:** Implementation approaches for line-based rotation, folder structure, CLI integration

**Key Findings:**

1. **Implementation approach determined:**
   - Line-based rotation handler as subclass of logging.Handler
   - Centralized log folder structure in LoggingManager
   - CLI flag integration via argparse in each script
   - System-wide log quality audit as separate feature

2. **No new questions identified** - Ready for Validation Loop

---

### Iteration 5 (2026-02-06 19:35) - Validation Round 1 Fixes

**Researched:** .gitignore structure, subprocess wrapper CLI integration, counter persistence

**Files Examined:**
- `.gitignore` (lines 1-30): Simple structure with project-specific exclusions, easy to add `logs/` entry
- `run_league_helper.py` (lines 40-69): subprocess.run() with hardcoded arguments [sys.executable, script, DATA_FOLDER], no CLI forwarding

**Key Findings:**

1. **.gitignore update straightforward:**
   - Current: List of folders/patterns to exclude
   - Action: Add `logs/` entry (single line addition)
   - No conflicts with existing patterns

2. **Subprocess wrapper integration requires modification:**
   - Current: Wrappers pass only DATA_FOLDER to target scripts
   - Need: Forward --enable-log-file flag from wrapper to target
   - Options:
     - Option A: Add argparse to wrappers, parse --enable-log-file, append to subprocess args
     - Option B: Forward all sys.argv[1:] from wrapper to target (simpler, more flexible)
   - Recommended: Option B (forward all args) - simpler, future-proof

3. **Counter persistence clarified with user (Q7):**
   - User confirmed: Counter resets on restart, new log file per script run
   - Design: Each script execution creates fresh timestamped log file starting at line 0
   - Aligns with timestamped filename pattern (YYYYMMDD_HHMMSS)

4. **Log quality estimates:**
   - Marked as rough estimates based on typical patterns
   - Actual percentages will vary after systematic audit
   - Not critical for planning (implementation will determine actual changes)

**Questions Identified:**
- None (Q7 resolved by user)

---

### Iteration 6 (2026-02-06 19:40) - Validation Round 2 Fix

**Researched:** Handler integration mechanism with LoggingManager

**Key Findings:**

1. **LineBasedRotatingHandler integration with LoggingManager:**
   - **Approach:** Modify LoggingManager.setup_logger() to instantiate LineBasedRotatingHandler when log_to_file=True
   - **Current code** (lines 95-115): Creates RotatingFileHandler directly in setup_logger()
   - **New design:** Replace RotatingFileHandler instantiation with LineBasedRotatingHandler
   - **Parameters:** LineBasedRotatingHandler(log_file_path, max_lines=500, max_files=50, script_name=name)
   - **Backward compatibility:** Existing callers don't need changes (setup_logger() signature unchanged)
   - **Integration point:** LoggingManager is single integration point (centralized)

2. **Data flow for line-based rotation:**
   - Script calls setup_logger(name, log_to_file=True)
   - LoggingManager creates LineBasedRotatingHandler with script-specific subfolder (logs/{script_name}/)
   - Handler tracks line count internally
   - On 500-line threshold: Close file, create new timestamped file, reset counter
   - On new file creation: Check folder, delete oldest if >50 files exist

3. **API contract:**
   - LineBasedRotatingHandler inherits from logging.FileHandler
   - Implements emit() method to track lines and rotate
   - Implements _rotate() method to create new file
   - Implements _cleanup_old_files() method to enforce 50-file limit

**Questions Identified:**
- None

---

## Solution Options

### Option 1: Custom LineBasedRotatingHandler

**Description:** Create custom logging handler that tracks line count and rotates based on 500-line threshold with max 50 files cleanup.

**Implementation:**
- Subclass logging.FileHandler (not RotatingFileHandler)
- Maintain line counter in memory (reset each session)
- On each emit(), increment counter, check threshold
- If threshold exceeded, close current file, create new timestamped file
- Implement cleanup: scan folder, delete oldest if >50 files

**Pros:**
- Complete control over rotation logic
- Eager counter in memory (fast)
- Can implement exact 500-line behavior
- Folder-based cleanup (max 50 files)

**Cons:**
- More code to write and test
- Need to handle edge cases (file I/O errors, permission issues)
- Counter resets on restart (by design)

**Effort Estimate:** MEDIUM (2-3 days for handler + tests)

**Fit Assessment:** EXCELLENT - Matches all requirements (line-based, eager counter, max 50 cleanup, timestamped files)

---

### Option 2: Wrapper Around RotatingFileHandler

**Description:** Keep RotatingFileHandler but add wrapper logic to convert line count to approximate byte size.

**Implementation:**
- Calculate average bytes per line (~100-150 bytes)
- Convert 500 lines to ~75KB max file size
- Use RotatingFileHandler with maxBytes=75000
- Still need custom cleanup for 50-file limit (backupCount only keeps 5)

**Pros:**
- Leverage existing handler code
- Less custom code

**Cons:**
- Imprecise (lines vary in length)
- Doesn't meet exact 500-line requirement
- Still need custom cleanup logic
- More complex workaround than clean solution

**Effort Estimate:** MEDIUM (workaround complexity offsets code reuse)

**Fit Assessment:** POOR - Doesn't meet exact 500-line requirement, imprecise approximation

---

### Option 3: Modify LoggingManager to Use New Handler

**Description:** Update LoggingManager.setup_logger() to accept rotation_type parameter ('size', 'line', 'time') and create appropriate handler.

**Implementation:**
- Add rotation_type parameter to setup_logger()
- Create factory method to instantiate correct handler type
- For 'line': use LineBasedRotatingHandler (Option 1)
- Maintain backward compatibility (default 'size')

**Pros:**
- Flexible for future needs
- Backward compatible
- Clean API

**Cons:**
- More complex than needed for current scope
- Over-engineering for single use case

**Effort Estimate:** MEDIUM-HIGH

**Fit Assessment:** GOOD - Clean design but may be over-engineered

---

### Option Comparison Summary

| Option | Effort | Fit | Recommended |
|--------|--------|-----|-------------|
| Custom LineBasedRotatingHandler | MEDIUM | EXCELLENT | YES |
| Wrapper Around RotatingFileHandler | MEDIUM | POOR | NO |
| Flexible rotation_type Parameter | MEDIUM-HIGH | GOOD | NO (over-engineered) |

---

---

## Recommended Approach

**Recommendation:** Custom LineBasedRotatingHandler with centralized log folder structure and system-wide log quality improvements

**Rationale:**
- User confirmed full timestamp format (Q1: YYYYMMDD_HHMMSS)
- User confirmed eager counter in memory (Q2: Option B)
- User confirmed counter resets per script run (Q7: new file each run)
- User confirmed opt-in file logging (Q4: OFF by default, --enable-log-file)
- User confirmed system-wide log quality scope (Q6: all modules)
- Solution Option 1 provides exact 500-line behavior (validated in Iteration 2, 6)
- Centralized integration via LoggingManager minimizes changes (validated in Iteration 6)

**Key Design Decisions:**
1. **Custom LineBasedRotatingHandler** - Subclass logging.FileHandler, track lines eagerly, rotate at 500
2. **Folder structure** - logs/{script_name}/ subfolders, auto-created by handler
3. **Cleanup strategy** - On each rotation, check folder, delete oldest if >50 files
4. **CLI integration** - Add --enable-log-file to all 6 scripts, subprocess wrappers forward sys.argv[1:]
5. **Log quality** - Apply DEBUG/INFO criteria (Iteration 3) to 939 calls across 60 files, systematic KEEP/UPDATE/REMOVE audit
6. **.gitignore** - Add single line `logs/` entry

---

## Scope Definition

### In Scope

**1. LoggingManager Infrastructure:**
- Create LineBasedRotatingHandler class (subclass logging.FileHandler)
- Modify LoggingManager.setup_logger() to instantiate new handler
- Implement folder structure: logs/{script_name}/
- Implement timestamped filenames: {script_name}-{YYYYMMDD_HHMMSS}.log
- Implement 500-line rotation with eager counter
- Implement max 50 files cleanup (delete oldest)

**2. CLI Integration (6 scripts):**
- Add --enable-log-file flag to: run_league_helper.py, run_player_fetcher.py, run_accuracy_simulation.py, run_win_rate_simulation.py, compile_historical_data.py, run_schedule_fetcher.py
- Modify subprocess wrappers (run_league_helper.py, run_player_fetcher.py) to forward CLI args via sys.argv[1:]
- Default behavior: File logging OFF (user must opt-in)

**3. Log Quality Improvements (System-Wide):**
- Apply DEBUG/INFO criteria to 939 logger.debug/info calls across 60 files
- Systematic audit: Mark each call KEEP/UPDATE/REMOVE
- Focus on high-traffic modules: PlayerManager, simulation managers, league_helper managers
- Update test assertions affected by log changes (estimated 10-20 test files)

**4. .gitignore Update:**
- Add `logs/` folder to .gitignore (single line)

**5. Testing:**
- Unit tests for LineBasedRotatingHandler (rotation logic, cleanup, counter)
- Update tests/utils/test_LoggingManager.py
- Verify 100% test pass rate

### Out of Scope

- Log level changes (keeping existing DEBUG/INFO/WARNING/ERROR/CRITICAL levels)
- New logging frameworks (staying with Python stdlib logging)
- Console logging changes (only file logging affected)
- Log format changes beyond quality improvements
- Persistent counter across restarts (counter resets per run)

### Deferred (Future Work)

- Centralized log viewing/analysis tool (potential future epic)
- Log compression for archived logs (nice-to-have, not requested)
- Configurable line limits per script (currently hardcoded 500)

---

## Proposed Feature Breakdown

**Total Features:** 7
**Implementation Order:** Feature 1 first (foundation), then Features 2-7 can proceed in parallel

**Note:** Testing is integrated into standard epic workflow (S4 Epic Testing Strategy, S7 Testing, S9 Epic Final QC, S10 100% pass rate), not a separate feature.

### Feature 1: core_logging_infrastructure

**Purpose:** Core logging infrastructure with line-based rotation, folder structure, and cleanup

**Scope:**
- Create LineBasedRotatingHandler class (subclass logging.FileHandler)
- Modify LoggingManager.setup_logger() integration
- Implement logs/{script_name}/ folder structure
- Implement timestamped filenames (YYYYMMDD_HHMMSS)
- Implement 500-line rotation with eager counter
- Implement max 50 files cleanup
- Update .gitignore with logs/ entry
- Unit tests for handler (rotation, cleanup, counter)

**Dependencies:** None (foundation feature)

**Discovery Basis:**
- Based on Q1 (full timestamps), Q2 (eager counter), Q7 (counter reset per run)
- Based on Iteration 2 (no built-in line-based handler)
- Based on Iteration 6 (integration via LoggingManager.setup_logger())
- Based on Solution Option 1 (Custom LineBasedRotatingHandler recommended)

**Estimated Size:** MEDIUM

---

### Feature 2: league_helper_logging

**Purpose:** CLI integration and log quality improvements for league_helper script

**Scope:**
- Add --enable-log-file flag to run_league_helper.py
- Modify subprocess wrapper to forward sys.argv[1:]
- Apply DEBUG/INFO criteria to league_helper/ modules logs
- Review and improve logs in: LeagueHelperManager, AddToRosterModeManager, StarterHelperModeManager, TradeSimulatorModeManager, ModifyPlayerDataModeManager, and all util/ managers
- Update affected test assertions

**Dependencies:** Feature 1 (core infrastructure)

**Discovery Basis:**
- Based on Iteration 2 (run_league_helper.py is subprocess wrapper)
- Based on Iteration 3 (log quality criteria)
- Based on Iteration 5 (subprocess wrapper forwarding)

**Estimated Size:** MEDIUM

---

### Feature 3: player_data_fetcher_logging

**Purpose:** CLI integration and log quality improvements for player-data-fetcher script

**Scope:**
- Add --enable-log-file flag to run_player_fetcher.py
- Modify subprocess wrapper to forward sys.argv[1:]
- Apply DEBUG/INFO criteria to player-data-fetcher/ modules logs
- Review and improve logs in: player_data_fetcher_main, espn_client, player_data_exporter, progress_tracker, game_data_fetcher
- Update affected test assertions

**Dependencies:** Feature 1 (core infrastructure)

**Discovery Basis:**
- Based on Iteration 2 (run_player_fetcher.py is subprocess wrapper)
- Based on Iteration 3 (log quality criteria)
- Based on Iteration 5 (subprocess wrapper forwarding)

**Estimated Size:** SMALL-MEDIUM

---

### Feature 4: accuracy_sim_logging

**Purpose:** CLI integration and log quality improvements for accuracy simulation script

**Scope:**
- Add --enable-log-file flag to run_accuracy_simulation.py (already has --log-level precedent)
- Apply DEBUG/INFO criteria to simulation/accuracy/ modules logs
- Review and improve logs in: AccuracySimulationManager, AccuracyCalculator, AccuracyResultsManager, ParallelAccuracyRunner
- Update affected test assertions

**Dependencies:** Feature 1 (core infrastructure)

**Discovery Basis:**
- Based on Iteration 1 (run_accuracy_simulation.py has argparse precedent)
- Based on Iteration 2 (direct entry script)
- Based on Iteration 3 (log quality criteria)

**Estimated Size:** SMALL-MEDIUM

---

### Feature 5: win_rate_sim_logging

**Purpose:** CLI integration and log quality improvements for win rate simulation script

**Scope:**
- Add --enable-log-file flag to run_win_rate_simulation.py
- Apply DEBUG/INFO criteria to simulation/win_rate/ modules logs
- Review and improve logs in: SimulationManager, SimulatedLeague, DraftHelperTeam, SimulatedOpponent, ParallelLeagueRunner
- Update affected test assertions

**Dependencies:** Feature 1 (core infrastructure)

**Discovery Basis:**
- Based on Iteration 1 (run_win_rate_simulation.py uses hardcoded LOGGING_TO_FILE)
- Based on Iteration 2 (direct entry script)
- Based on Iteration 3 (log quality criteria)

**Estimated Size:** SMALL-MEDIUM

---

### Feature 6: historical_data_compiler_logging

**Purpose:** CLI integration and log quality improvements for historical data compiler script

**Scope:**
- Add --enable-log-file flag to compile_historical_data.py
- Apply DEBUG/INFO criteria to historical_data_compiler/ modules logs
- Review and improve logs in: json_exporter, player_data_fetcher, weekly_snapshot_generator, game_data_fetcher, http_client, schedule_fetcher
- Update affected test assertions

**Dependencies:** Feature 1 (core infrastructure)

**Discovery Basis:**
- Based on Iteration 2 (compile_historical_data.py confirmed as historical_data_compiler)
- Based on Iteration 3 (log quality criteria)

**Estimated Size:** SMALL-MEDIUM

---

### Feature 7: schedule_fetcher_logging

**Purpose:** CLI integration and log quality improvements for schedule fetcher script

**Scope:**
- Add --enable-log-file flag to run_schedule_fetcher.py (async main)
- Apply DEBUG/INFO criteria to schedule-data-fetcher/ modules logs
- Review and improve logs in: ScheduleFetcher and related modules
- Update affected test assertions

**Dependencies:** Feature 1 (core infrastructure)

**Discovery Basis:**
- Based on Iteration 1 (run_schedule_fetcher.py is async main)
- Based on Iteration 3 (log quality criteria)

**Estimated Size:** SMALL

---

### Shared Utility Modules

**Note:** Log quality improvements for shared utility modules (utils/, simulation/shared/) will be distributed across Features 2-7 based on which scripts use them most. For example:
- PlayerManager, ConfigManager, TeamDataManager → Feature 2 (league_helper)
- ResultsManager, ConfigGenerator → Features 4-5 (simulations)
- DraftedRosterManager, csv_utils, data_file_manager → Feature 2 (league_helper primary user)

---

## Testing Strategy

Testing will be handled through standard epic workflow stages (not a separate feature):

**S4 - Epic Testing Strategy:**
- Define test plan for LineBasedRotatingHandler (rotation logic, cleanup, counter)
- Define test plan for CLI integration (flag parsing, wrapper forwarding)
- Define test plan for log quality changes (functionality preserved)

**S7 - Feature Testing:**
- Per-feature smoke testing and QC rounds
- Unit tests for LineBasedRotatingHandler
- Update tests/utils/test_LoggingManager.py
- Update test assertions affected by log changes (10-20 files)

**S9 - Epic Final QC:**
- End-to-end smoke testing all 6 scripts with --enable-log-file
- Verify log files created in correct folders
- Verify 500-line rotation works
- Verify max 50 files cleanup works
- Verify log quality improvements don't break functionality

**S10 - Epic Cleanup:**
- 100% unit test pass rate verification (MANDATORY)
- All tests passing before PR creation

---

## Discovery Log

| Timestamp | Activity | Outcome |
|-----------|----------|---------|
| 2026-02-06 19:00 | Initialized Discovery | Epic size MEDIUM, time-box 2-3 hours |
| 2026-02-06 19:05 | Initial research complete | Documented findings, identified 6 questions |
| 2026-02-06 19:10 | User answered all 6 questions | Full timestamps, eager rotation, propose criteria, opt-in logging, 6 scripts, system-wide quality |
| 2026-02-06 19:15 | Iteration 2 complete | Handler research, script mapping confirmed, scope quantified (939 calls, 60 files) |
| 2026-02-06 19:20 | Iteration 3 complete | Log quality criteria proposed (DEBUG: tracing, INFO: user awareness) |
| 2026-02-06 19:25 | Iteration 4 complete | Solution options documented, ready for Validation Loop |
| 2026-02-06 19:30 | Validation Round 1 started | Sequential read, identified 4 issues |
| 2026-02-06 19:35 | Iteration 5 complete | Fixed all Round 1 issues, Q7 answered by user |
| 2026-02-06 19:40 | Iteration 6 complete | Fixed Round 2 integration gap |
| 2026-02-06 19:45 | Validation Round 3 complete | First clean round, counter = 1 |
| 2026-02-06 19:48 | Validation Round 4 complete | Second clean round, counter = 2 |
| 2026-02-06 19:50 | Validation Round 5 complete | Third clean round, Validation Loop PASSED |
| 2026-02-06 19:52 | S1.P3.3 Synthesis complete | Recommended Approach, Scope Definition, Feature Breakdown documented |
| 2026-02-06 19:55 | Feature breakdown revised | Changed from 3 to 7 features (1 core + 6 per-script) per user feedback |
| 2026-02-06 19:56 | S1.P3.4 User approval received | Discovery Phase COMPLETE, proceeding to S1 Step 4 |

---

## Validation Loop Rounds

### Round 1 (2026-02-06 19:30-19:35)

**Reading Pattern:** Sequential read (top to bottom) + completeness check

**Issues Found:** 4 (Missing research, Integration gap, Unverified assumptions x2)

**Issues Fixed:**
1. ✅ .gitignore update researched - straightforward single-line addition
2. ✅ Subprocess wrapper CLI integration explored - forward sys.argv[1:] (Option B recommended)
3. ✅ Counter persistence verified with user (Q7) - resets on restart, new file per run
4. ✅ Log quality estimates marked as rough estimates (not critical assumptions)

**Clean Round Counter:** 0 (issues found, counter reset after fixes)

---

### Round 2 (2026-02-06 19:40-19:45)

**Reading Pattern:** Reverse order (bottom to top) + integration verification

**Issues Found:** 1 (Integration gap)

**Issues Fixed:**
1. ✅ LineBasedRotatingHandler → LoggingManager integration documented in Iteration 6 - Modify setup_logger() to instantiate handler, parameters defined, data flow clarified, API contract specified

**Clean Round Counter:** 0 (issue found, counter reset after fix)

---

### Round 3 (2026-02-06 19:45)

**Reading Pattern:** Random spot-checks (5 epic requirements) + alignment verification

**Spot-Checked Requirements:**
1. logs folder structure → Research complete (Iterations 2, 6)
2. 500-line cap → Research complete (Iterations 2, 6, Option 1)
3. max 50 logs cleanup → Research complete (Iterations 2, 6, Option 1)
4. CLI toggle → Research complete (Iterations 1, 5, Q4)
5. Log quality evaluation → Research complete (Iteration 3, Q6)

**Alignment Verification:**
- ✅ All mandatory research complete
- ✅ No over-researching (scope appropriate to requirements)
- ✅ Epic intent preserved (all components addressed)
- ✅ All 7 user questions resolved
- ✅ Ready to proceed to specification

**Issues Found:** 0

**Clean Round Counter:** 1 (first consecutive clean round!)

---

### Round 4 (2026-02-06 19:48)

**Reading Pattern:** Thematic clustering (group related sections) + cross-reference validation

**Themes Validated:**
1. Handler & Rotation → All aspects researched, cross-references consistent
2. Scripts & CLI Integration → Complete, no gaps
3. Log Quality → Self-contained, criteria defined
4. Integration Points → All documented

**Cross-Reference Check:**
- ✅ All Q&A answers traced to iterations
- ✅ Solution options reference supporting research
- ✅ No orphaned or contradictory research

**Issues Found:** 0

**Clean Round Counter:** 2 (second consecutive clean round!)

---

### Round 5 (2026-02-06 19:50) - FINAL

**Reading Pattern:** Final comprehensive sweep + exit readiness verification

**Exit Criteria Verified:**
- ✅ 3 consecutive rounds with zero issues (Rounds 3, 4, 5)
- ✅ All epic components researched
- ✅ All 7 user questions answered
- ✅ Zero unverified assumptions
- ✅ All integration points documented
- ✅ Ready to proceed to specification

**Issues Found:** 0

**Clean Round Counter:** 3 (THREE CONSECUTIVE CLEAN ROUNDS - VALIDATION LOOP COMPLETE!)

---

**Validation Loop Status:** ✅ PASSED (3 consecutive clean rounds achieved)
**Next Step:** S1.P3.3 Synthesis (fill Recommended Approach, Scope Definition, Feature Breakdown)

---

## User Approval

**Discovery Approved:** YES
**Approved Date:** 2026-02-06
**Approved By:** User

**Approval Notes:**
User approved 7-feature breakdown (1 core infrastructure + 6 per-script features). Each per-script feature includes CLI integration and log quality improvements for that script's modules. Shared utilities distributed across features based on primary usage.
