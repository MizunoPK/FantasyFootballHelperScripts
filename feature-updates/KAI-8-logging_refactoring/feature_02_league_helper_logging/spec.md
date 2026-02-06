# Feature Specification: league_helper_logging

**Part of Epic:** KAI-8-logging_refactoring
**Feature Number:** 02
**Created:** 2026-02-06
**Last Updated:** 2026-02-06

---

## Discovery Context

**Discovery Document:** `../DISCOVERY.md`

### This Feature's Scope (from Discovery)

**Feature 2: league_helper_logging**

**Purpose:** CLI integration and log quality improvements for league helper script

**Scope:**
- Add --enable-log-file flag to run_league_helper.py (subprocess wrapper)
- Forward flag using sys.argv[1:] to league_helper.py
- Apply DEBUG/INFO quality criteria to league_helper/ modules
- Review shared utilities: PlayerManager, ConfigManager, TeamDataManager, DraftedRosterManager, csv_utils, data_file_manager
- Update affected test assertions

**Dependencies:** Feature 1 (core infrastructure)

### Relevant Discovery Decisions

- **Solution Approach:** Subprocess wrapper uses sys.argv[1:] forwarding (Option B from Iteration 5)
- **Key Constraints:**
  - Must preserve existing script behavior when flag not provided
  - Subprocess wrapper must forward CLI arguments to target script
  - Log quality improvements must not break functionality
- **Implementation Order:** After Feature 1 (depends on LineBasedRotatingHandler)

### Relevant User Answers (from Discovery)

| Question | Answer | Impact on This Feature |
|----------|--------|----------------------|
| Q3: Log quality criteria | Agent to propose criteria | Must apply DEBUG (tracing) and INFO (user awareness) criteria from Iteration 3 |
| Q4: CLI flag default | File logging OFF by default | Flag must explicitly enable file logging, users opt-in |
| Q6: Log quality scope | System-wide (Option B) | Affects league_helper/ modules AND shared utilities used by league_helper |

### Discovery Basis for This Feature

- **Based on Finding:** Iteration 1 identified run_league_helper.py as subprocess wrapper requiring sys.argv[1:] forwarding
- **Based on User Answer:** Q6 (system-wide scope) means shared utilities need log improvements
- **Based on Finding:** Iteration 3 proposed DEBUG/INFO criteria that guide log quality improvements

---

## Feature Overview

**What:** Add CLI flag control for file logging and improve log quality in league helper modules

**Why:** Enables users to control file logging for league helper, improves debugging and runtime awareness

**Who:** Users running league helper in draft, optimizer, trade, or data editor modes

---

## Functional Requirements

{To be expanded during S2 deep dive based on thorough research}

### Requirement 1: CLI Flag Integration (Subprocess Wrapper)
**Description:** {To be detailed in S2}

**Acceptance Criteria:**
- {To be defined in S2}

**Example:**
{To be provided in S2}

### Requirement 2: Log Quality - DEBUG Level
**Description:** {To be detailed in S2}

**Acceptance Criteria:**
- {To be defined in S2}

**Example:**
{To be provided in S2}

### Requirement 3: Log Quality - INFO Level
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

**Performance:**
- {To be defined in S2}

**Maintainability:**
- Must follow project coding standards
- Must preserve existing league_helper behavior

---

## Out of Scope

**Explicitly NOT included in this feature:**
- Core infrastructure changes (Feature 1 handles this)
- Other scripts' CLI integration (Features 3-7 handle this)
- Console logging changes (only file logging affected)
- New logging frameworks (staying with Python stdlib logging)

---

## Open Questions

{To be populated during S2 deep dive - questions tracked in checklist.md}

No open questions currently - to be identified during S2 research phase.

---

## Implementation Notes

**Design Decisions from Discovery:**
- Subprocess wrapper forwards arguments using sys.argv[1:] pattern
- Shared utilities (PlayerManager, ConfigManager, etc.) handled in this feature

**Implementation Tips:**
- {To be added during S2/S5}

---

## Change Log

| Date | Changed By | What Changed | Why |
|------|------------|--------------|-----|
| 2026-02-06 | Agent | Initial spec created with Discovery Context | S1 Step 5 (Epic Structure Creation) |
