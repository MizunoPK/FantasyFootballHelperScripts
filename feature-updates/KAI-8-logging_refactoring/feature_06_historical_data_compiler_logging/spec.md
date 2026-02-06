# Feature Specification: historical_data_compiler_logging

**Part of Epic:** KAI-8-logging_refactoring
**Feature Number:** 06
**Created:** 2026-02-06
**Last Updated:** 2026-02-06

---

## Discovery Context

**Discovery Document:** `../DISCOVERY.md`

### This Feature's Scope (from Discovery)

**Feature 6: historical_data_compiler_logging**

**Purpose:** CLI integration and log quality improvements for historical data compiler script

**Scope:**
- Add --enable-log-file flag to compile_historical_data.py
- Apply DEBUG/INFO criteria to historical_data_compiler/ modules logs
- Review and improve logs in: json_exporter, player_data_fetcher, weekly_snapshot_generator, game_data_fetcher, http_client, schedule_fetcher
- Update affected test assertions

**Dependencies:** Feature 1 (core infrastructure)

### Relevant Discovery Decisions

- **Solution Approach:** Direct entry script (compile_historical_data.py)
- **Key Constraints:**
  - Must preserve existing script behavior when flag not provided
  - Log quality improvements must not break functionality
  - Multiple submodules need log quality attention
- **Implementation Order:** After Feature 1 (depends on LineBasedRotatingHandler)

### Relevant User Answers (from Discovery)

| Question | Answer | Impact on This Feature |
|----------|--------|----------------------|
| Q2: Rotation approach | Eager counter | Handler integration from Feature 1 |
| Q3: Log quality criteria | Agent to propose criteria | Must apply DEBUG (tracing) and INFO (user awareness) criteria |
| Q4: CLI flag default | File logging OFF by default | Flag must explicitly enable file logging |
| Q5: Script coverage | Just those 6 scripts | Confirms historical_data_compiler in scope (compile_historical_data.py) |
| Q6: Log quality scope | System-wide (Option B) | Affects historical_data_compiler/ submodules |

### Discovery Basis for This Feature

- **Based on Finding:** Iteration 2 confirmed compile_historical_data.py is the historical_data_compiler script
- **Based on Finding:** Iteration 2 identified 17 debug/info calls in historical_data_compiler/
- **Based on Finding:** Iteration 3 proposed DEBUG/INFO criteria that guide log quality improvements

---

## Feature Overview

**What:** Add CLI flag control for file logging and improve log quality in historical data compiler modules

**Why:** Enables users to control file logging for historical data compilation, improves debugging and runtime awareness

**Who:** Users running compile_historical_data.py to build historical datasets

---

## Functional Requirements

{To be expanded during S2 deep dive based on thorough research}

### Requirement 1: CLI Flag Integration (Direct Entry)
**Description:** {To be detailed in S2}

**Acceptance Criteria:**
- {To be defined in S2}

**Example:**
{To be provided in S2}

### Requirement 2: Log Quality - DEBUG Level
**Description:** {To be detailed in S2}

**Acceptance Criteria:**
- {To be defined in S2}

### Requirement 3: Log Quality - INFO Level
**Description:** {To be detailed in S2}

**Acceptance Criteria:**
- {To be defined in S2}

---

## Technical Requirements

{To be expanded during S2 deep dive}

---

## Integration Points

### Integration with Feature 1 (Core Infrastructure)

**Direction:** This feature consumes FROM Feature 1
**Data Passed:** LineBasedRotatingHandler, setup_logger(enable_log_file=True)
**Interface:** {To be defined in S2}

---

## Error Handling

{To be defined during S2 based on thorough research}

---

## Testing Strategy

{To be defined in S4 (Epic Testing Strategy stage)}

---

## Non-Functional Requirements

**Maintainability:**
- Must follow project coding standards
- Must preserve existing historical_data_compiler behavior

---

## Out of Scope

**Explicitly NOT included in this feature:**
- Core infrastructure changes (Feature 1)
- Other scripts' CLI integration (Features 2-5, 7)
- Console logging changes (only file logging affected)

---

## Open Questions

{To be populated during S2 deep dive - questions tracked in checklist.md}

---

## Implementation Notes

**Design Decisions from Discovery:**
- Direct entry script with multiple submodules needing log quality attention
- Submodules listed in Discovery: json_exporter, player_data_fetcher, weekly_snapshot_generator, game_data_fetcher, http_client, schedule_fetcher

---

## Change Log

| Date | Changed By | What Changed | Why |
|------|------------|--------------|-----|
| 2026-02-06 | Agent | Initial spec created with Discovery Context | S1 Step 5 (Epic Structure Creation) |
