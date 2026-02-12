# Epic Ticket: logging_refactoring

**Created:** 2026-02-06
**Status:** VALIDATED

---

## Description

This epic transforms the logging infrastructure across all major scripts by implementing line-based log rotation (500 lines per file), centralized log organization (logs/ folder with script-specific subfolders), and automated cleanup (max 50 logs per script). Users gain explicit control over file logging through a CLI flag (--enable-log-file, OFF by default), and log quality is systematically improved across the entire codebase to provide better debugging traces and runtime awareness without overwhelming the logs.

---

## Acceptance Criteria (Epic-Level)

**The epic is successful when ALL of these are true:**

- [ ] All 6 scripts (league_helper, player-data-fetcher, accuracy_sim, win_rate_sim, historical_data_compiler, schedule_fetcher) support --enable-log-file CLI flag with file logging OFF by default
- [ ] Log files are created in centralized logs/{script_name}/ subfolders (e.g., logs/league_helper/, logs/accuracy_sim/)
- [ ] Log files use timestamped naming format: {script_name}-{YYYYMMDD_HHMMSS}.log
- [ ] Log rotation occurs automatically at 500 lines per file (new timestamped file created when threshold reached)
- [ ] Each script subfolder maintains maximum 50 log files, automatically deleting oldest when limit exceeded
- [ ] logs/ folder is added to .gitignore (log files not committed to repository)
- [ ] DEBUG level logs across all modules enable tracing of data flow and function execution without overwhelming the logs
- [ ] INFO level logs across all modules provide runtime awareness of script progress and outcomes without implementation details
- [ ] All unit tests pass (100% pass rate, including updated test assertions for log changes)
- [ ] Epic smoke testing passes for all 6 scripts with --enable-log-file flag enabled

---

## Success Indicators

**Measurable metrics that show epic succeeded:**

- CLI coverage: 6/6 scripts support --enable-log-file flag (100%)
- Rotation accuracy: Log files cap at exactly 500 lines before creating new file
- Cleanup accuracy: No script subfolder exceeds 50 log files after extended usage
- Folder organization: All logs created in logs/{script_name}/ structure, no scattered logs
- Log quality: DEBUG logs enable tracing, INFO logs provide user awareness (verified through systematic audit)
- Test coverage: 100% test pass rate maintained across all 2200+ tests
- Backward compatibility: Scripts work identically with file logging disabled (default behavior)

---

## Failure Patterns (How We'd Know Epic Failed)

**These symptoms indicate the epic FAILED its goals:**

❌ Scripts crash or error when --enable-log-file flag is used
❌ Log files created outside logs/{script_name}/ subfolders (scattered in project root or other locations)
❌ Log rotation creates files with non-sequential timestamps or skips rotation (files exceed 500 lines)
❌ Script subfolders accumulate >50 log files without cleanup (disk space bloat)
❌ DEBUG logs are too verbose (overwhelming, unreadable) or too sparse (can't trace execution)
❌ INFO logs contain implementation details instead of user-relevant progress
❌ Test suite fails due to log changes breaking assertions (tests not updated properly)
❌ Subprocess wrappers (run_league_helper.py, run_player_fetcher.py) don't forward --enable-log-file to target scripts
❌ File logging enabled by default (user must opt-in, not opt-out)

---

## Scope Boundaries

✅ **In Scope (What IS included):**
- LineBasedRotatingHandler custom logging handler with 500-line rotation
- Centralized logs/{script_name}/ folder structure with auto-creation
- Timestamped log filenames (YYYYMMDD_HHMMSS format)
- Max 50 files per subfolder with automatic oldest-file deletion
- --enable-log-file CLI flag for all 6 scripts (OFF by default)
- Subprocess wrapper argument forwarding (run_league_helper.py, run_player_fetcher.py)
- System-wide log quality improvements (DEBUG/INFO criteria applied to 939 calls across 60 files)
- .gitignore update to exclude logs/ folder
- Unit tests for new handler and updated test assertions

❌ **Out of Scope (What is NOT included):**
- Console logging changes (only file logging affected)
- Log level changes (keeping existing DEBUG/INFO/WARNING/ERROR/CRITICAL)
- New logging frameworks (staying with Python stdlib logging)
- Log format changes beyond quality improvements
- Persistent line counter across script restarts (counter resets each run)
- Centralized log viewing/analysis tools (potential future epic)
- Log compression for archived logs (not requested)
- Configurable line limits per script (hardcoded 500 for now)

---

## User Validation

**This section filled out by USER - agent presents ticket and asks user to verify/approve**

**User comments:**
Epic ticket approved as written. All acceptance criteria, success indicators, failure patterns, and scope boundaries match expectations.

**User approval:** YES
**Approved by:** User
**Approved date:** 2026-02-06

---

## Notes

**Why this ticket matters:**
This ticket serves as the source of truth for epic-level outcomes. It's created BEFORE folder structure to ensure agent understands WHAT the epic achieves. During Iteration 21 (Spec Validation Against Validated Documents), each feature's spec.md will be validated against both epic notes AND this ticket to catch misinterpretation.

**Counter reset design:**
Each script execution creates a fresh timestamped log file starting at line 0. This aligns with the per-run logging model and simplifies implementation (no persistent counter state needed).

**Log quality scope:**
System-wide improvements affect 939 logger.debug/info calls across 60 files. Shared utility modules (PlayerManager, ConfigManager, etc.) will be improved as part of the per-script features based on primary usage patterns.
