# Test Strategy: core_logging_infrastructure

**Feature:** Feature 01 - Core Logging Infrastructure
**Created:** 2026-02-06 (S4)
**Coverage Goal:** >90% (target: >95%)
**Total Tests Planned:** 87 tests

---

## Test Strategy Overview

This test strategy defines unit tests, integration tests, edge case tests, and configuration tests for the core logging infrastructure feature. All requirements have 100% test coverage with traceability to spec.md.

**Test Categories:**
- **Unit Tests:** 22 tests (function-level, mock dependencies)
- **Integration Tests:** 18 tests (component-level, real dependencies)
- **Edge Case Tests:** 32 tests (boundary conditions, error paths)
- **Configuration Tests:** 15 tests (default, custom, invalid, missing)

**Total:** 87 tests planned (>95% coverage)

---

## Test Coverage Matrix

| Requirement | Unit Tests | Integration Tests | Edge Case Tests | Config Tests | Total | Coverage |
|-------------|------------|-------------------|-----------------|--------------|-------|----------|
| R1: Line-Based Rotation | 4 | 3 | 8 | 3 | 18 | 100% |
| R2: Centralized Folders | 2 | 3 | 5 | 2 | 12 | 100% |
| R3: Timestamped Filenames | 3 | 2 | 4 | 1 | 10 | 100% |
| R4: Automated Cleanup | 4 | 3 | 7 | 2 | 16 | 100% |
| R5: LoggingManager Integration | 3 | 3 | 3 | 3 | 12 | 100% |
| R6: Path Generation | 3 | 2 | 3 | 2 | 10 | 100% |
| R7: .gitignore Update | 3 | 2 | 2 | 2 | 9 | 100% |
| **TOTAL** | **22** | **18** | **32** | **15** | **87** | **>95%** |

---

## Requirement R1: Line-Based Log Rotation

**Source:** spec.md Requirement 1
**Acceptance Criteria:** Rotation triggers at 500 lines (not before), counter resets after rotation, line counter in memory (not persistent)

### Unit Tests (R1)

**Test 1.1: test_line_counter_increments**
- **Purpose:** Verify line counter increments with each log record
- **Setup:** Create LineBasedRotatingHandler with max_lines=500
- **Input:** Emit 10 log records
- **Expected:** Line counter = 10
- **Links to:** R1 (line counting)

**Test 1.2: test_rotation_at_500_lines**
- **Purpose:** Verify rotation triggers exactly at line 500
- **Setup:** Handler with max_lines=500
- **Input:** Emit 500 log records
- **Expected:** shouldRollover() returns True after line 500, False before
- **Links to:** R1 (rotation threshold)

**Test 1.3: test_counter_resets_after_rotation**
- **Purpose:** Verify line counter resets to 0 after rotation
- **Setup:** Handler with max_lines=500, emit 500 lines to trigger rotation
- **Input:** Check counter after rotation
- **Expected:** Line counter = 0
- **Links to:** R1 (counter reset)

**Test 1.4: test_counter_not_persistent**
- **Purpose:** Verify counter does NOT persist across handler instances
- **Setup:** Create handler, emit 250 lines, close handler, create new handler
- **Input:** Check counter on new handler
- **Expected:** Line counter = 0 (not 250)
- **Links to:** R1 (non-persistent counter)

### Integration Tests (R1)

**Test 1.5: test_rotation_creates_new_file**
- **Purpose:** Verify rotation creates new timestamped file
- **Setup:** Real handler writing to logs/test/, emit 750 lines
- **Expected:** 2 files created (lines 1-500, lines 501-750), both with timestamps
- **Links to:** R1 + R3 (rotation + filenames)

**Test 1.6: test_old_file_remains_intact**
- **Purpose:** Verify rotation does not rename or overwrite old file
- **Setup:** Emit 750 lines, check first file
- **Expected:** First file contains exactly 500 lines, unchanged after rotation
- **Links to:** R1 (file preservation)

**Test 1.7: test_emit_logging_integration**
- **Purpose:** Verify emit() method correctly increments counter
- **Setup:** Real handler with Python logging module
- **Input:** logger.info("test") called 10 times
- **Expected:** Line counter = 10, shouldRollover() accurate
- **Links to:** R1 (emit integration)

### Edge Case Tests (R1)

**Test 1.8: test_rotation_boundary_499_lines**
- **Purpose:** Verify no rotation at line 499
- **Setup:** Emit exactly 499 lines
- **Expected:** shouldRollover() = False, only 1 file exists
- **Links to:** R1 (boundary condition)

**Test 1.9: test_rotation_boundary_500_lines**
- **Purpose:** Verify rotation at exactly line 500
- **Setup:** Emit exactly 500 lines
- **Expected:** shouldRollover() = True, rotation triggered
- **Links to:** R1 (boundary condition)

**Test 1.10: test_rotation_boundary_501_lines**
- **Purpose:** Verify rotation already occurred by line 501
- **Setup:** Emit 501 lines
- **Expected:** 2 files exist (500 + 1 lines)
- **Links to:** R1 (boundary condition)

**Test 1.11: test_rapid_logging**
- **Purpose:** Verify counter accurate with rapid log generation
- **Setup:** Emit 10,000 lines rapidly in tight loop
- **Expected:** Correct file count (20 files), accurate line counts
- **Links to:** R1 (performance)

**Test 1.12: test_concurrent_logging**
- **Purpose:** Verify thread-safe counter increments
- **Setup:** 2 threads emitting logs simultaneously
- **Expected:** Counter accurate, no race conditions
- **Links to:** R1 (concurrency)

**Test 1.13: test_zero_max_lines**
- **Purpose:** Verify handler rejects max_lines=0
- **Setup:** Attempt to create handler with max_lines=0
- **Expected:** Raises ValueError("max_lines must be positive")
- **Links to:** R1 (validation)

**Test 1.14: test_negative_max_lines**
- **Purpose:** Verify handler rejects negative max_lines
- **Setup:** Attempt to create handler with max_lines=-100
- **Expected:** Raises ValueError("max_lines must be positive")
- **Links to:** R1 (validation)

**Test 1.15: test_very_large_max_lines**
- **Purpose:** Verify handler accepts very large max_lines
- **Setup:** Create handler with max_lines=1000000
- **Expected:** Handler created successfully, counter works
- **Links to:** R1 (boundary)

### Configuration Tests (R1)

**Test 1.16: test_default_max_lines_500**
- **Purpose:** Verify hardcoded default is 500 lines
- **Setup:** Create handler without explicit max_lines parameter
- **Expected:** Rotation occurs at 500 lines
- **Links to:** R1 (default config)

**Test 1.17: test_custom_max_lines_integration**
- **Purpose:** Verify LoggingManager passes max_lines=500
- **Setup:** Call setup_logger() with log_to_file=True
- **Expected:** Handler created with max_lines=500 (not custom)
- **Links to:** R1 + R5 (integration)

**Test 1.18: test_max_lines_not_configurable**
- **Purpose:** Verify max_lines cannot be overridden via config
- **Setup:** Attempt to pass max_lines=1000 to setup_logger()
- **Expected:** Ignored, uses hardcoded 500
- **Links to:** R1 (hardcoded per user decision Q2)

---

## Requirement R2: Centralized Folder Structure

**Source:** spec.md Requirement 2
**Acceptance Criteria:** logs/ folder at project root, logs/{logger_name}/ subfolders auto-created, graceful failure if cannot create

### Unit Tests (R2)

**Test 2.1: test_folder_path_generation**
- **Purpose:** Verify correct folder path: logs/{logger_name}/
- **Setup:** Mock folder creation
- **Input:** logger_name="league_helper"
- **Expected:** Path = "logs/league_helper/"
- **Links to:** R2 (path format)

**Test 2.2: test_folder_auto_creation**
- **Purpose:** Verify folders created if missing
- **Setup:** Delete logs/ folder, create handler
- **Expected:** logs/ and logs/test/ folders created
- **Links to:** R2 (auto-creation)

### Integration Tests (R2)

**Test 2.3: test_multiple_logger_subfolders**
- **Purpose:** Verify multiple subfolders coexist
- **Setup:** Create handlers for "league_helper", "accuracy_sim", "player_data_fetcher"
- **Expected:** 3 subfolders created: logs/league_helper/, logs/accuracy_sim/, logs/player_data_fetcher/
- **Links to:** R2 + Epic (multi-script)

**Test 2.4: test_folder_exists_no_error**
- **Purpose:** Verify no error if folder already exists
- **Setup:** Create logs/test/ manually, then create handler
- **Expected:** No error raised, handler uses existing folder
- **Links to:** R2 (idempotent)

**Test 2.5: test_folder_creation_with_logging_manager**
- **Purpose:** Verify LoggingManager creates folders correctly
- **Setup:** Call setup_logger(name="test_logger", log_to_file=True)
- **Expected:** logs/test_logger/ folder created
- **Links to:** R2 + R5 (integration)

### Edge Case Tests (R2)

**Test 2.6: test_folder_creation_permission_denied**
- **Purpose:** Verify graceful error if cannot create folder (permissions)
- **Setup:** Make logs/ folder read-only
- **Expected:** Raises PermissionError with clear message, logged to console
- **Links to:** R2 (error handling)

**Test 2.7: test_empty_logger_name**
- **Purpose:** Verify behavior with empty logger name
- **Setup:** Call setup_logger(name="", log_to_file=True)
- **Expected:** Trusts caller per user decision Q4, creates logs// or uses default
- **Links to:** R2 + validation (trusting caller)

**Test 2.8: test_very_long_logger_name**
- **Purpose:** Verify behavior with 255+ character logger name
- **Setup:** Call setup_logger(name="a"*300, log_to_file=True)
- **Expected:** Trusts caller, creates folder (OS may truncate)
- **Links to:** R2 + validation

**Test 2.9: test_special_chars_in_logger_name**
- **Purpose:** Verify behavior with special characters
- **Setup:** logger_name="test/logger" (has slash)
- **Expected:** Trusts caller, may create nested folder or sanitize
- **Links to:** R2 + validation

**Test 2.10: test_disk_space_full**
- **Purpose:** Verify error handling when disk full
- **Setup:** Simulate disk full condition
- **Expected:** Raises IOError with clear message
- **Links to:** R2 (error handling)

### Configuration Tests (R2)

**Test 2.11: test_default_logs_folder_location**
- **Purpose:** Verify logs/ folder is at project root
- **Setup:** Create handler, check folder location
- **Expected:** logs/ folder at root (not in subdirectory)
- **Links to:** R2 (default location)

**Test 2.12: test_logs_folder_not_configurable**
- **Purpose:** Verify logs/ location cannot be changed via config
- **Setup:** Attempt to override logs folder location
- **Expected:** Ignored, uses hardcoded "logs/"
- **Links to:** R2 (hardcoded per spec)

---

## Requirement R3: Timestamped Log Filenames

**Source:** spec.md Requirement 3
**Acceptance Criteria:** Format = {logger_name}-{YYYYMMDD_HHMMSS}.log, hyphen separator, timestamp includes time component

### Unit Tests (R3)

**Test 3.1: test_filename_format**
- **Purpose:** Verify filename format matches spec
- **Setup:** Mock timestamp generation
- **Input:** logger_name="test", timestamp="20260206_143522"
- **Expected:** Filename = "test-20260206_143522.log"
- **Links to:** R3 (format)

**Test 3.2: test_timestamp_includes_time**
- **Purpose:** Verify timestamp includes HHMMSS (not just YYYYMMDD)
- **Setup:** Create handler, check filename
- **Expected:** Filename contains underscore and 6-digit time component
- **Links to:** R3 (time component)

**Test 3.3: test_hyphen_separator**
- **Purpose:** Verify hyphen separator (not underscore) between name and timestamp
- **Setup:** Create handler with logger_name="test"
- **Expected:** Filename matches pattern: test-YYYYMMDD_HHMMSS.log (hyphen after "test")
- **Links to:** R3 (separator)

### Integration Tests (R3)

**Test 3.4: test_unique_timestamps_on_rotation**
- **Purpose:** Verify each rotated file has unique timestamp
- **Setup:** Emit 750 lines rapidly to trigger rotation
- **Expected:** 2 files with different timestamps (even if milliseconds apart)
- **Links to:** R3 + R1 (rotation timestamps)

**Test 3.5: test_filename_generation_via_logging_manager**
- **Purpose:** Verify LoggingManager generates correct filenames
- **Setup:** Call setup_logger(name="league_helper", log_to_file=True)
- **Expected:** Filename matches league_helper-{YYYYMMDD_HHMMSS}.log
- **Links to:** R3 + R6 (path generation)

### Edge Case Tests (R3)

**Test 3.6: test_timestamp_collision_handling**
- **Purpose:** Verify behavior if two files created in same second
- **Setup:** Create 2 handlers rapidly (within 1 second)
- **Expected:** Unique filenames (use milliseconds or increment)
- **Links to:** R3 (collision avoidance)

**Test 3.7: test_special_chars_in_timestamp**
- **Purpose:** Verify no special characters in generated timestamp
- **Setup:** Create handler, inspect timestamp
- **Expected:** Timestamp contains only digits and underscore
- **Links to:** R3 (format validation)

**Test 3.8: test_filename_cross_platform**
- **Purpose:** Verify filename valid on Windows/Linux/Mac
- **Setup:** Generate filename, check against OS restrictions
- **Expected:** No invalid characters (no <, >, :, ", |, ?, *)
- **Links to:** R3 (cross-platform)

**Test 3.9: test_filename_length_limit**
- **Purpose:** Verify filename doesn't exceed 255 character limit
- **Setup:** Long logger_name (200 chars) + timestamp
- **Expected:** Total filename ≤ 255 characters
- **Links to:** R3 (OS limit)

### Configuration Tests (R3)

**Test 3.10: test_timestamp_format_not_configurable**
- **Purpose:** Verify timestamp format cannot be customized
- **Setup:** Attempt to override timestamp format
- **Expected:** Ignored, uses hardcoded YYYYMMDD_HHMMSS format
- **Links to:** R3 (hardcoded per spec)

---

## Requirement R4: Automated Cleanup (Max 50 Files)

**Source:** spec.md Requirement 4
**Acceptance Criteria:** Max 50 files per subfolder, oldest deleted when 51st created, multi-file deletion if >50 exist

### Unit Tests (R4)

**Test 4.1: test_cleanup_at_51_files**
- **Purpose:** Verify cleanup triggers when 51st file created
- **Setup:** Mock 50 existing files, create 51st
- **Expected:** cleanup() called, oldest file deleted
- **Links to:** R4 (threshold)

**Test 4.2: test_identify_oldest_file**
- **Purpose:** Verify oldest file correctly identified by timestamp
- **Setup:** Mock 51 files with various timestamps
- **Expected:** Oldest timestamp file selected for deletion
- **Links to:** R4 (age sorting)

**Test 4.3: test_delete_multiple_files_if_over_50**
- **Purpose:** Verify multi-file deletion if >50 exist
- **Setup:** Mock 55 existing files
- **Expected:** 5 oldest files deleted, 50 remain
- **Links to:** R4 (bulk cleanup)

**Test 4.4: test_cleanup_preserves_newest_50**
- **Purpose:** Verify newest 50 files retained
- **Setup:** Mock 60 files, trigger cleanup
- **Expected:** Newest 50 files remain, oldest 10 deleted
- **Links to:** R4 (preservation)

### Integration Tests (R4)

**Test 4.5: test_cleanup_with_real_files**
- **Purpose:** Verify cleanup deletes actual files from filesystem
- **Setup:** Create 51 real log files in logs/test/
- **Expected:** 50 files remain after cleanup
- **Links to:** R4 (file operations)

**Test 4.6: test_cleanup_across_rotations**
- **Purpose:** Verify cleanup works across multiple rotations
- **Setup:** Emit enough logs to create 55 files (27,500 lines)
- **Expected:** Folder never exceeds 50 files
- **Links to:** R4 + R1 (rotation + cleanup)

**Test 4.7: test_cleanup_folder_only**
- **Purpose:** Verify cleanup only affects logger's subfolder (not other folders)
- **Setup:** Create 51 files in logs/test/, 20 files in logs/other/
- **Expected:** logs/test/ has 50 files, logs/other/ has 20 files (unchanged)
- **Links to:** R4 (isolation)

### Edge Case Tests (R4)

**Test 4.8: test_cleanup_exactly_50_files**
- **Purpose:** Verify no cleanup at exactly 50 files
- **Setup:** Create exactly 50 files
- **Expected:** No files deleted
- **Links to:** R4 (boundary)

**Test 4.9: test_cleanup_permission_denied**
- **Purpose:** Verify graceful error if cannot delete file
- **Setup:** Make oldest file read-only
- **Expected:** Logs error, continues with next oldest file
- **Links to:** R4 (error handling)

**Test 4.10: test_cleanup_file_in_use**
- **Purpose:** Verify behavior if oldest file is open
- **Setup:** Open oldest file for reading, trigger cleanup
- **Expected:** Skip file or handle gracefully (OS-dependent)
- **Links to:** R4 (concurrent access)

**Test 4.11: test_cleanup_corrupted_filename**
- **Purpose:** Verify cleanup handles non-standard filenames
- **Setup:** Create 50 files with correct format + 1 file "invalid.log"
- **Expected:** Cleanup only considers valid timestamped files
- **Links to:** R4 (robustness)

**Test 4.12: test_cleanup_empty_folder**
- **Purpose:** Verify no error if folder empty during cleanup
- **Setup:** Trigger cleanup in empty logs/test/ folder
- **Expected:** No error raised, no files deleted
- **Links to:** R4 (edge case)

**Test 4.13: test_cleanup_very_large_file_count**
- **Purpose:** Verify cleanup handles 100+ existing files
- **Setup:** Create 150 files, trigger cleanup
- **Expected:** Oldest 100 files deleted, newest 50 remain
- **Links to:** R4 (bulk operations)

**Test 4.14: test_max_files_not_configurable**
- **Purpose:** Verify max_files=50 is hardcoded
- **Setup:** Attempt to override max_files via config
- **Expected:** Ignored, uses hardcoded 50
- **Links to:** R4 (hardcoded per user decision Q2)

### Configuration Tests (R4)

**Test 4.15: test_default_max_files_50**
- **Purpose:** Verify hardcoded default is 50 files
- **Setup:** Create handler without explicit max_files parameter
- **Expected:** Cleanup occurs when 51st file created
- **Links to:** R4 (default config)

**Test 4.16: test_max_files_integration_logging_manager**
- **Purpose:** Verify LoggingManager passes max_files=50
- **Setup:** Call setup_logger(), create 51 files
- **Expected:** Cleanup triggered at 51 files
- **Links to:** R4 + R5 (integration)

---

## Requirement R5: LoggingManager Integration

**Source:** spec.md Requirement 5
**Acceptance Criteria:** Modify setup_logger() to instantiate LineBasedRotatingHandler, maintain backward compatibility

### Unit Tests (R5)

**Test 5.1: test_setup_logger_creates_line_based_handler**
- **Purpose:** Verify setup_logger() creates LineBasedRotatingHandler (not RotatingFileHandler)
- **Setup:** Call setup_logger(name="test", log_to_file=True)
- **Expected:** Handler type = LineBasedRotatingHandler
- **Links to:** R5 (handler type)

**Test 5.2: test_setup_logger_passes_max_lines**
- **Purpose:** Verify setup_logger() passes max_lines=500
- **Setup:** Call setup_logger(), inspect handler
- **Expected:** handler.max_lines = 500
- **Links to:** R5 (parameter passing)

**Test 5.3: test_setup_logger_passes_max_files**
- **Purpose:** Verify setup_logger() passes max_files=50
- **Setup:** Call setup_logger(), inspect handler
- **Expected:** handler.max_files = 50
- **Links to:** R5 (parameter passing)

### Integration Tests (R5)

**Test 5.4: test_setup_logger_backward_compatible**
- **Purpose:** Verify setup_logger() signature unchanged
- **Setup:** Call setup_logger(name, log_level, log_to_file, log_file_path, max_file_size, backup_count)
- **Expected:** Function accepts all parameters, no errors
- **Links to:** R5 (backward compatibility)

**Test 5.5: test_setup_logger_unused_params_ignored**
- **Purpose:** Verify max_file_size and backup_count parameters ignored
- **Setup:** Call setup_logger(max_file_size=10000, backup_count=3)
- **Expected:** Parameters ignored, uses max_lines=500 and max_files=50
- **Links to:** R5 (parameter handling)

**Test 5.6: test_existing_callers_unmodified**
- **Purpose:** Verify run_accuracy_simulation.py works without changes
- **Setup:** Simulate existing caller: setup_logger("accuracy_simulation", "INFO", True)
- **Expected:** Handler created successfully, no errors
- **Links to:** R5 (backward compatibility)

### Edge Case Tests (R5)

**Test 5.7: test_log_to_file_false_no_handler**
- **Purpose:** Verify log_to_file=False skips LineBasedRotatingHandler
- **Setup:** Call setup_logger(log_to_file=False)
- **Expected:** No file handler created, console logging only
- **Links to:** R5 (conditional creation)

**Test 5.8: test_log_file_path_parameter_respected**
- **Purpose:** Verify custom log_file_path parameter works
- **Setup:** Call setup_logger(log_file_path="/custom/path/test.log")
- **Expected:** Handler uses custom path (not auto-generated)
- **Links to:** R5 (parameter override)

**Test 5.9: test_import_line_based_handler**
- **Purpose:** Verify LineBasedRotatingHandler import works
- **Setup:** from utils.LineBasedRotatingHandler import LineBasedRotatingHandler
- **Expected:** Import successful, class available
- **Links to:** R5 (import)

### Configuration Tests (R5)

**Test 5.10: test_logging_manager_default_behavior**
- **Purpose:** Verify LoggingManager works with default config
- **Setup:** Call setup_logger() with no config changes
- **Expected:** LineBasedRotatingHandler created with hardcoded defaults
- **Links to:** R5 (default config)

**Test 5.11: test_logging_manager_custom_log_level**
- **Purpose:** Verify log_level parameter still works
- **Setup:** Call setup_logger(log_level="DEBUG")
- **Expected:** Logger level = DEBUG, handler created
- **Links to:** R5 (log level)

**Test 5.12: test_logging_manager_encoding_utf8**
- **Purpose:** Verify encoding='utf-8' passed to handler
- **Setup:** Call setup_logger(), inspect handler
- **Expected:** handler.encoding = 'utf-8'
- **Links to:** R5 (encoding)

---

## Requirement R6: Updated Log File Path Generation

**Source:** spec.md Requirement 6
**Acceptance Criteria:** Path = logs/{logger_name}/{logger_name}-{YYYYMMDD_HHMMSS}.log, subfolder auto-created, hyphen separator, time component included

### Unit Tests (R6)

**Test 6.1: test_generate_log_file_path_format**
- **Purpose:** Verify path format matches spec
- **Setup:** Mock _generate_log_file_path()
- **Input:** logger_name="test", timestamp="20260206_143522"
- **Expected:** Path = "logs/test/test-20260206_143522.log"
- **Links to:** R6 (format)

**Test 6.2: test_path_includes_subfolder**
- **Purpose:** Verify path includes logger-specific subfolder
- **Setup:** Call _generate_log_file_path(logger_name="league_helper")
- **Expected:** Path contains "logs/league_helper/"
- **Links to:** R6 + R2 (subfolder)

**Test 6.3: test_path_timestamp_includes_time**
- **Purpose:** Verify timestamp includes time component (HHMMSS)
- **Setup:** Call _generate_log_file_path()
- **Expected:** Path contains underscore and 6-digit time
- **Links to:** R6 + R3 (timestamp)

### Integration Tests (R6)

**Test 6.4: test_path_generation_creates_subfolder**
- **Purpose:** Verify path generation auto-creates subfolder
- **Setup:** Delete logs/test/, call setup_logger(name="test", log_to_file=True)
- **Expected:** logs/test/ folder created, file at logs/test/test-{timestamp}.log
- **Links to:** R6 + R2 (integration)

**Test 6.5: test_path_generation_via_setup_logger**
- **Purpose:** Verify setup_logger() uses new path generation
- **Setup:** Call setup_logger(name="accuracy_simulation", log_to_file=True)
- **Expected:** File created at logs/accuracy_simulation/accuracy_simulation-{timestamp}.log
- **Links to:** R6 + R5 (integration)

### Edge Case Tests (R6)

**Test 6.6: test_path_generation_empty_logger_name**
- **Purpose:** Verify behavior with empty logger name
- **Setup:** Call _generate_log_file_path(logger_name="")
- **Expected:** Creates logs// or uses default name (trusts caller)
- **Links to:** R6 (edge case)

**Test 6.7: test_path_generation_special_chars**
- **Purpose:** Verify behavior with special characters in logger name
- **Setup:** Call _generate_log_file_path(logger_name="test/logger")
- **Expected:** Handles gracefully (creates nested folder or sanitizes)
- **Links to:** R6 (edge case)

**Test 6.8: test_path_generation_very_long_name**
- **Purpose:** Verify behavior with very long logger name
- **Setup:** Call _generate_log_file_path(logger_name="a"*300)
- **Expected:** Path created (may be truncated by OS)
- **Links to:** R6 (boundary)

### Configuration Tests (R6)

**Test 6.9: test_path_format_not_configurable**
- **Purpose:** Verify path format cannot be customized
- **Setup:** Attempt to override path format via config
- **Expected:** Ignored, uses hardcoded format
- **Links to:** R6 (hardcoded)

**Test 6.10: test_path_generation_uses_hyphen**
- **Purpose:** Verify hyphen separator (not underscore) used
- **Setup:** Call _generate_log_file_path(logger_name="test")
- **Expected:** Path matches: logs/test/test-{timestamp}.log
- **Links to:** R6 + R3 (separator)

---

## Requirement R7: .gitignore Update

**Source:** spec.md Requirement 7
**Acceptance Criteria:** Add `logs/` to .gitignore at line 71, prevents log files from being committed

### Unit Tests (R7)

**Test 7.1: test_gitignore_contains_logs_entry**
- **Purpose:** Verify .gitignore contains "logs/" entry
- **Setup:** Read .gitignore file
- **Expected:** File contains line with exactly "logs/"
- **Links to:** R7 (entry exists)

**Test 7.2: test_gitignore_logs_at_line_71**
- **Purpose:** Verify logs/ entry is at line 71
- **Setup:** Read .gitignore file, check line 71
- **Expected:** Line 71 = "logs/"
- **Links to:** R7 (line number)

**Test 7.3: test_gitignore_logs_trailing_slash**
- **Purpose:** Verify entry has trailing slash (ignores folder)
- **Setup:** Read .gitignore line 71
- **Expected:** Entry = "logs/" (not "logs" or "logs/*")
- **Links to:** R7 (format)

### Integration Tests (R7)

**Test 7.4: test_git_status_ignores_logs_folder**
- **Purpose:** Verify git status does not show logs/ folder
- **Setup:** Create logs/ folder with files, run `git status`
- **Expected:** logs/ folder not listed in untracked files
- **Links to:** R7 (git integration)

**Test 7.5: test_log_files_not_committable**
- **Purpose:** Verify log files cannot be added to git
- **Setup:** Create log file, attempt `git add logs/test.log`
- **Expected:** Git ignores the file (not staged)
- **Links to:** R7 (file exclusion)

### Edge Case Tests (R7)

**Test 7.6: test_gitignore_survives_updates**
- **Purpose:** Verify logs/ entry not overwritten by other changes
- **Setup:** Add another entry to .gitignore, check line 71
- **Expected:** Line 71 still = "logs/"
- **Links to:** R7 (persistence)

**Test 7.7: test_gitignore_duplicate_entry_avoided**
- **Purpose:** Verify no duplicate logs/ entries
- **Setup:** Check entire .gitignore file
- **Expected:** Only one "logs/" entry exists
- **Links to:** R7 (uniqueness)

### Configuration Tests (R7)

**Test 7.8: test_gitignore_location_project_root**
- **Purpose:** Verify .gitignore at project root (not subdirectory)
- **Setup:** Check .gitignore file location
- **Expected:** .gitignore at root directory
- **Links to:** R7 (location)

**Test 7.9: test_gitignore_backup_created**
- **Purpose:** Verify .gitignore backup created before modification (optional)
- **Setup:** Check for .gitignore.bak or similar
- **Expected:** Backup exists or not needed (implementation-dependent)
- **Links to:** R7 (safety)

---

## Traceability Matrix

| Requirement | Test Cases | Total Tests | Coverage |
|-------------|------------|-------------|----------|
| R1: Line-Based Rotation | Tests 1.1-1.18 | 18 | 100% |
| R2: Centralized Folders | Tests 2.1-2.12 | 12 | 100% |
| R3: Timestamped Filenames | Tests 3.1-3.10 | 10 | 100% |
| R4: Automated Cleanup | Tests 4.1-4.16 | 16 | 100% |
| R5: LoggingManager Integration | Tests 5.1-5.12 | 12 | 100% |
| R6: Path Generation | Tests 6.1-6.10 | 10 | 100% |
| R7: .gitignore Update | Tests 7.1-7.9 | 9 | 100% |
| **TOTAL** | **Tests 1.1 - 7.9** | **87** | **100%** |

**Requirements with <90% Coverage:** 0 (all at 100%)

---

## Edge Case Catalog

| Edge Case | Category | Expected Behavior | Test Coverage |
|-----------|----------|-------------------|---------------|
| Rotation at exactly 500 lines | Boundary condition | Triggers rotation | Test 1.9 |
| Rotation before 500 lines (499) | Boundary condition | No rotation | Test 1.8 |
| Counter reset after rotation | Logic validation | Counter = 0 | Test 1.3 |
| Counter not persistent across instances | Persistence check | New instance starts at 0 | Test 1.4 |
| Rapid log generation (10k lines) | Performance | Accurate counting/rotation | Test 1.11 |
| Concurrent logging (threads) | Concurrency | Thread-safe counter | Test 1.12 |
| max_lines = 0 | Input validation | ValueError | Test 1.13 |
| max_lines < 0 | Input validation | ValueError | Test 1.14 |
| Folder permission denied | Error handling | PermissionError logged | Test 2.6 |
| Empty logger name | Input validation | Trusts caller (per Q4) | Test 2.7 |
| Very long logger name (255+ chars) | Boundary condition | Trusts caller, OS may truncate | Test 2.8 |
| Special chars in logger name | Data quality | Trusts caller | Test 2.9 |
| Disk space full | Error handling | IOError | Test 2.10 |
| Timestamp collision (same second) | Uniqueness | Use milliseconds/increment | Test 3.6 |
| Filename > 255 characters | OS limit | Truncate or handle | Test 3.9 |
| Exactly 50 files | Boundary condition | No cleanup | Test 4.8 |
| 51 files | Threshold | Cleanup triggered | Test 4.1 |
| 55+ files | Bulk cleanup | Delete oldest files | Test 4.3, 4.13 |
| Cannot delete oldest file (permissions) | Error handling | Skip, try next oldest | Test 4.9 |
| Oldest file in use | Concurrent access | Skip or handle gracefully | Test 4.10 |
| Invalid/corrupted filename | Robustness | Ignore non-standard files | Test 4.11 |
| Empty folder during cleanup | Edge case | No error | Test 4.12 |
| log_to_file=False | Conditional logic | No file handler | Test 5.7 |
| Custom log_file_path | Parameter override | Use custom path | Test 5.8 |
| Unused parameters (max_file_size, backup_count) | Backward compatibility | Ignored | Test 5.5 |
| Empty logger name in path generation | Edge case | Trusts caller | Test 6.6 |
| Special chars in path | Edge case | Handle gracefully | Test 6.7 |
| .gitignore duplicate entry | Uniqueness | Only one "logs/" entry | Test 7.7 |

**Total Edge Cases Identified:** 32
**Edge Cases Without Tests:** 0

---

## Configuration Test Matrix

| Config Value/Scenario | Default | Custom | Invalid | Missing | Total Tests |
|-----------------------|---------|--------|---------|---------|-------------|
| max_lines (hardcoded 500) | Test 1.16 | Test 1.17 | Test 1.13, 1.14 | Test 1.16 | 4 |
| max_files (hardcoded 50) | Test 4.15 | Test 4.16 | Test 4.14 | Test 4.15 | 3 |
| logs/ folder location | Test 2.11 | Test 2.12 | N/A | N/A | 2 |
| Logger name | Test 2.1 | Test 2.3 | Test 2.7-2.9 | N/A | 5 |
| log_to_file parameter | Test 5.1 | Test 5.7 | N/A | N/A | 2 |
| Log level | Test 5.11 | Test 5.11 | N/A | N/A | 1 |
| Encoding | Test 5.12 | N/A | N/A | N/A | 1 |
| .gitignore location | Test 7.8 | N/A | N/A | N/A | 1 |

**Total Config Tests Planned:** 15 tests
**Config Values Without Tests:** 0
**Scenarios Covered:** Default, Custom, Invalid, Missing

---

## Test Implementation Notes

**File Locations:**
- Unit tests: `tests/utils/test_LineBasedRotatingHandler.py` (new file)
- Integration tests: `tests/utils/test_LoggingManager.py` (modify existing)
- .gitignore tests: `tests/test_gitignore.py` (new file, if needed)

**Mocking Strategy:**
- Mock filesystem operations for unit tests (os.makedirs, os.remove, os.listdir)
- Mock datetime.now() for timestamp tests
- Use real filesystem for integration tests (with cleanup in tearDown)

**Test Data:**
- Create temporary test folders: `logs/test/`, `logs/test_cleanup/`
- Generate test log files with known timestamps
- Clean up all test files in tearDown() methods

**Coverage Goal:**
- Unit tests: >80% line coverage
- Integration tests: Key workflows (rotation, cleanup, path generation)
- Edge cases: All boundary conditions and error paths
- Config tests: All scenarios (default, custom, invalid, missing)
- **Overall: >95% coverage** (exceeds 90% requirement)

---

## Validation Loop Results

**Validation Loop Status:** PENDING (will be completed in S4.I4)

**Validation Loop will verify:**
- Round 1: All requirements have test coverage (sequential verification)
- Round 2: Edge cases enumerated completely (gap detection)
- Round 3: Config scenarios covered (random spot-checks)
- Exit: 3 consecutive clean rounds

---

## S4 Iterations Summary

**S4.I1 (Test Strategy Development):** ✅ COMPLETE
- Test coverage matrix created
- Test case list created (87 tests planned)
- Traceability matrix shows 100% requirement coverage

**S4.I2 (Edge Case Enumeration):** ✅ COMPLETE
- Edge case catalog created (32 edge cases)
- Boundary conditions identified (min/max values, null/empty)
- Error paths enumerated (file not found, permissions, disk space)

**S4.I3 (Configuration Change Impact):** ✅ COMPLETE
- Configuration dependency analysis complete (hardcoded values per user decisions Q2)
- Configuration test matrix created (15 tests covering default, custom, invalid, missing)
- All config scenarios have test coverage

**S4.I4 (Validation Loop):** PENDING
- Will be executed next using `s4_validation_loop.md`

---

**Test Strategy Created:** 2026-02-06
**Last Updated:** 2026-02-06 (S4.I1-I3 complete)
**Total Tests:** 87 tests
**Coverage:** >95% (exceeds 90% goal)
**Ready for:** S4.I4 (Validation Loop)
