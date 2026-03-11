# Epic Request: League Helper CLI Refactor

**File Location:** `.shamt/epics/requests/cli-enhancements/league_helper_cli_notes-v2.md`

---

## Epic Overview

**Epic Name:** League Helper CLI Refactor

**Date:** 2026-03-09

**Requested By:** User

**Epic Type:** Enhancement / Infrastructure

**Estimated Complexity:** Large

---

## Problem Statement

**What problem does this epic solve?**

`run_league_helper.py` currently launches the league helper by spawning a subprocess that calls itself, rather than directly invoking the underlying logic via import. It also lacks a proper argparse-based CLI and has no end-to-end (`--e2e-test`) test mode. This makes the script harder to test, harder to configure, and inconsistent with the emerging CLI pattern being adopted across all runner scripts.

**Why is this important?**

Standardizing the runner script improves testability (E2E mode), configurability (all parameters as CLI args), and maintainability (no subprocess self-calls). It also enables a future CLI integration test framework that requires all runner scripts to expose an `--e2e-test` flag.

**Who is affected?**

Developers running or testing the league helper; users who invoke the script from the command line; the CLI integration test framework epic (depends on this).

---

## Goals & Success Metrics

**Primary Goals:**
1. Replace subprocess self-invocation with direct module import
2. Add argparse-based CLI with all configurable parameters as named arguments
3. Add `--e2e-test` flag that runs all 5 modes deterministically, exits 0, and writes output to fixed `/tmp/` paths
4. Add `--log-level` argument with standard log level choices
5. Use a `@dataclass Settings` pattern to pass configuration through the application

**Success Metrics:**
- `python run_league_helper.py --help` shows all available arguments
- `python run_league_helper.py --e2e-test` exits with code 0 and completes within 180 seconds
- All 5 modes (add_to_roster, starter_helper, trade_simulator, modify_player_data, save_calculated_points) execute in E2E mode
- No regressions in existing functionality

**Out of Scope (Explicitly Not Included):**
- Changes to the underlying league helper logic
- New modes or features beyond CLI refactoring
- Changes to data files or configuration schemas

---

## Requirements

### Functional Requirements

1. **Argparse CLI**
   - Add named arguments for all configurable parameters: `--e2e-test`, `--log-level`, `--my-team-name`, `--recommendation-count`, `--min-waiver-improvement`, `--num-runners-up`, `--min-trade-improvement`, `--data-folder`, `--mode`, `--week`, `--season`, `--enable-log-file`
   - All arguments should have sensible defaults matching current behavior

2. **E2E Test Mode**
   - `--e2e-test` flag forces deterministic execution across all 5 modes
   - Output written to fixed `/tmp/` paths (not `tempfile.mkdtemp()`)
   - Exits with code 0 on success
   - Completes within 180 seconds

3. **Settings Dataclass**
   - Introduce a `@dataclass Settings` to hold all configuration, replacing scattered variable assignments
   - Settings populated from CLI args and/or defaults

4. **Direct Import**
   - Remove subprocess self-call pattern
   - Invoke league helper logic via direct Python import

### Non-Functional Requirements

- **Performance:** E2E test mode completes within 180 seconds
- **Maintainability:** Settings object centralizes all configuration in one place
- **Testability:** `--e2e-test` flag enables automated testing of the full pipeline

### Technical Requirements

- **Dependencies:** argparse (stdlib), dataclasses (stdlib), existing league_helper modules
- **Integrations:** All 5 league helper modes must be callable in E2E mode
- **Technology Stack:** Python 3, existing project structure

---

## Research & Background

### Existing Solutions Analysis

**Current State:**
`run_league_helper.py` uses `subprocess.run([sys.executable, __file__, ...])` to re-invoke itself with different arguments. Configuration is passed as command-line arguments to the subprocess.

**Research Findings:**
- Subprocess self-invocation is fragile, harder to test, and adds process overhead
- Other runner scripts in the project are being refactored to use argparse + direct imports
- A `@dataclass Settings` pattern provides type-safe, documented configuration passing

**Alternative Approaches Considered:**
1. **Keep subprocess pattern, add E2E flag only:** Low effort but doesn't fix underlying issues
2. **Full argparse + direct import + dataclass (Recommended):** Consistent with project direction, fully testable

### Technical Constraints

**Known Limitations:**
- E2E mode must produce deterministic output (no random data fetching)
- Fixed `/tmp/` paths in E2E mode (not `tempfile.mkdtemp()`) to enable path-based verification

**Architectural Considerations:**
- Settings dataclass should be defined in the runner script or a shared settings module
- Mode execution in E2E mode should use test/mock data to avoid live API calls

---

## Initial Feature Breakdown (Preliminary)

**Note:** This is a preliminary breakdown. S1 Discovery Phase will refine this.

**Proposed Features:**

1. **Feature 1:** Argparse CLI Setup
   - **Purpose:** Replace ad-hoc argument passing with proper argparse CLI
   - **Key Components:** Argument definitions, help text, defaults, type validation

2. **Feature 2:** Settings Dataclass
   - **Purpose:** Centralize all configuration in a typed `@dataclass Settings` object
   - **Key Components:** Dataclass definition, population from CLI args, passing through call stack

3. **Feature 3:** Direct Import Refactor
   - **Purpose:** Remove subprocess self-invocation, call league helper logic directly
   - **Key Components:** Import restructuring, entry point cleanup

4. **Feature 4:** E2E Test Mode
   - **Purpose:** Enable automated end-to-end testing of all 5 modes
   - **Key Components:** `--e2e-test` flag, deterministic execution, fixed output paths, exit code 0

---

## Dependencies & Risks

### External Dependencies

- **CLI Integration Test Framework epic:** Depends on this epic being completed first

### Risks & Mitigation

| Risk | Impact | Probability | Mitigation Strategy |
|------|--------|-------------|---------------------|
| Subprocess removal breaks existing callers | High | Medium | Audit all callers before removing subprocess pattern |
| E2E mode data dependencies (live API) | Medium | Medium | Use test/fixture data in E2E mode |
| Settings dataclass breaks existing mode entry points | Medium | Low | Ensure dataclass fields match all existing parameters |

---

## Timeline & Resources

**Estimated Timeline:** 3-5 days

**Team Members Required:**
- Developer: TBD

**Key Milestones:**
1. Argparse + Settings dataclass: Day 1-2
2. Direct import refactor: Day 2-3
3. E2E mode implementation and testing: Day 4-5

---

## Implementation Considerations

### Existing Codebase Integration

**Areas of the Codebase That May Require Changes:**
- `run_league_helper.py`: Complete refactor — argparse, dataclass, direct import, E2E mode
- League helper mode entry points (5 modes): May need updates to accept Settings object instead of parsed args
- Any callers of `run_league_helper.py` via subprocess

**New Areas That May Need Creation:**
- Settings dataclass (may live in runner or a shared module)
- E2E test data or fixtures (if live data cannot be used)

**Coding Practices to Follow:**
- Follow argparse pattern established in other refactored runner scripts
- Use `@dataclass` with type hints for Settings
- Use LoggingManager, not print(), for logging
- Follow CODING_STANDARDS.md (type hints, docstrings, error_context())
- E2E output paths must use fixed `/tmp/` paths, not `tempfile.mkdtemp()`

### Testing Strategy (High-Level)

- **Unit Tests:** Test argparse argument parsing; test Settings dataclass construction from args
- **Integration Tests:** Test each of the 5 modes can be invoked via the refactored entry point
- **End-to-End Tests:** `python run_league_helper.py --e2e-test` exits 0 and produces expected output files in `/tmp/`

---

## Open Questions

1. **Settings dataclass location:** Should it live in `run_league_helper.py` or a shared module used by multiple runner scripts?
   - **Status:** Unanswered

2. **E2E test data:** What test data should be used for E2E mode — existing fixture files or a minimal synthetic dataset?
   - **Status:** Unanswered

---

## References

- **Related Docs:** `run_league_helper.py`, existing runner scripts for pattern reference
- **Related Epics:** CLI Integration Test Framework (depends on this), Win Rate Simulation E2E, Accuracy Simulation E2E, Schedule Fetcher CLI, Game Data Fetcher CLI, Historical Compiler CLI
- **External Resources:** Python argparse docs, Python dataclasses docs

---

## Next Steps

**To proceed with this epic:**
1. User reviews this request
2. User says "Start S1 for League Helper CLI Refactor"
3. Agent reads `.shamt/guides/stages/s1/s1_epic_planning.md`
4. Agent creates git branch and FF-{N} folder during S1
5. Agent runs S1 Discovery Phase to refine this request

**This request file remains in `.shamt/epics/requests/` until S1 creates the epic folder.**
