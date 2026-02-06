# Feature Specification: core_logging_infrastructure

**Part of Epic:** KAI-8-logging_refactoring
**Feature Number:** 01
**Created:** 2026-02-06
**Last Updated:** 2026-02-06

---

## Discovery Context

**Discovery Document:** `../DISCOVERY.md`

### This Feature's Scope (from Discovery)

**Feature 1: core_logging_infrastructure**

**Purpose:** Custom LineBasedRotatingHandler, centralized logs/ folder structure, 500-line rotation, max 50 files cleanup, .gitignore update

**Scope:**
- Custom LineBasedRotatingHandler (subclass logging.FileHandler)
- LoggingManager.py integration (modify setup_logger())
- logs/{script_name}/ folder structure with auto-creation
- Timestamped filenames: {script_name}-{YYYYMMDD_HHMMSS}.log
- 500-line rotation with eager counter
- Max 50 files per subfolder with oldest-file deletion
- .gitignore update to exclude logs/ folder
- Unit tests for new handler

**Dependencies:** None (foundation feature)

### Relevant Discovery Decisions

- **Solution Approach:** Custom LineBasedRotatingHandler with eager counter (in-memory line tracking)
- **Key Constraints:**
  - Must support 500-line cap per file
  - Max 50 files per subfolder with automatic oldest-file deletion
  - Counter resets on script restart (new timestamped file each run)
  - Must integrate with existing LoggingManager.py without breaking backward compatibility
- **Implementation Order:** Feature 1 is foundation - must be completed before Features 2-7

### Relevant User Answers (from Discovery)

| Question | Answer | Impact on This Feature |
|----------|--------|----------------------|
| Q1: Timestamp format | Full timestamp YYYYMMDD_HHMMSS (Option B) | Log filenames use precise timestamps supporting multiple logs per day |
| Q2: Line-based rotation approach | Eager - maintain counter in memory (Option B) | Handler tracks line count in memory for better performance |
| Q4: CLI flag default | File logging OFF by default, --enable-log-file flag (Option A) | LoggingManager setup_logger() needs enable_log_file parameter |
| Q7: Counter persistence | Counter resets on restart (new file per run) | Simpler implementation - no persistent state needed |

### Discovery Basis for This Feature

- **Based on Finding:** Iteration 2 identified no built-in line-based rotation handler in Python logging - custom handler required
- **Based on User Answer:** Q1 (full timestamps), Q2 (eager counter), Q7 (counter reset) shaped handler design
- **Based on Finding:** Iteration 6 defined LoggingManager integration approach - modify setup_logger() to instantiate LineBasedRotatingHandler when enable_log_file=True

---

## Feature Overview

**What:** Foundation logging infrastructure providing line-based rotation, centralized folder structure, and automated cleanup

**Why:** Enables all 6 scripts to use improved logging with user control, prevents disk space bloat, provides better log organization

**Who:** All Fantasy Football Helper scripts (league_helper, player-data-fetcher, accuracy_sim, win_rate_sim, historical_data_compiler, schedule_fetcher) and their end users

---

## Functional Requirements

{To be expanded during S2 deep dive based on thorough research}

### Requirement 1: Line-Based Log Rotation
**Description:** {To be detailed in S2}

**Acceptance Criteria:**
- {To be defined in S2}

**Example:**
{To be provided in S2}

### Requirement 2: Centralized Folder Structure
**Description:** {To be detailed in S2}

**Acceptance Criteria:**
- {To be defined in S2}

**Example:**
{To be provided in S2}

### Requirement 3: Automated Cleanup (Max 50 Files)
**Description:** {To be detailed in S2}

**Acceptance Criteria:**
- {To be defined in S2}

**Example:**
{To be provided in S2}

### Requirement 4: LoggingManager Integration
**Description:** {To be detailed in S2}

**Acceptance Criteria:**
- {To be defined in S2}

**Example:**
{To be provided in S2}

---

## Technical Requirements

{To be expanded during S2 deep dive}

### Algorithms

{To be defined in S2 based on deep technical research}

### Data Structures

{To be defined in S2}

### Interfaces

{To be defined in S2}

---

## Integration Points

### Integration with Features 2-7 (All Script Logging Features)

**Direction:** This feature provides TO all script logging features
**Data Passed:** LineBasedRotatingHandler class, modified setup_logger() API
**Interface:** {To be defined in S2}

**Example Flow:**
```
Feature 01 (core infrastructure)
  ↓ provides LineBasedRotatingHandler, setup_logger(enable_log_file=True)
Features 02-07 (per-script logging)
  ↓ consume handler, integrate with CLI
End Users
  ↓ control file logging via --enable-log-file flag
```

---

## Error Handling

{To be defined during S2 based on thorough research}

---

## Testing Strategy

{To be defined in S4 (Epic Testing Strategy stage)}

---

## Non-Functional Requirements

**Performance:**
- {To be defined in S2}

**Scalability:**
- {To be defined in S2}

**Reliability:**
- {To be defined in S2}

**Maintainability:**
- Must follow project coding standards (CODING_STANDARDS.md)
- Must maintain backward compatibility with existing LoggingManager usage

---

## Out of Scope

**Explicitly NOT included in this feature:**
- Script-specific CLI integration (Features 2-7 handle this)
- Log quality improvements to existing debug/info calls (Features 2-7 handle this)
- Console logging changes (only affects file logging)
- Log format changes (keeping existing formats)
- Configurable line limits per script (hardcoded 500 for all scripts)
- Log compression for archived logs
- Persistent line counter across restarts (counter resets each run)

---

## Open Questions

{To be populated during S2 deep dive - questions will be tracked in checklist.md}

No open questions currently - to be identified during S2 research phase.

---

## Implementation Notes

{To be populated during S2 deep dive and refined through S5}

**Design Decisions from Discovery:**
- Custom handler subclasses logging.FileHandler (not RotatingFileHandler) for line-based logic
- Eager counter (in-memory) for performance
- Counter resets on restart, aligns with timestamped-file-per-run model
- LoggingManager.setup_logger() gets new enable_log_file parameter (default False)

**Implementation Tips:**
- {To be added during S2/S5}

**Gotchas:**
- {To be identified during S2/S5}

---

## Change Log

| Date | Changed By | What Changed | Why |
|------|------------|--------------|-----|
| 2026-02-06 | Agent | Initial spec created with Discovery Context | S1 Step 5 (Epic Structure Creation) |
