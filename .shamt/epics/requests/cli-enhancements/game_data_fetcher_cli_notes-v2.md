# Epic Request: Game Data Fetcher CLI Modernization

**File Location:** `.shamt/epics/requests/cli-enhancements/game_data_fetcher_cli_notes-v2.md`

---

## Epic Overview

**Epic Name:** Game Data Fetcher CLI Modernization

**Date:** 2026-03-09

**Requested By:** User

**Epic Type:** Enhancement / Infrastructure

**Estimated Complexity:** Small

---

## Problem Statement

**What problem does this epic solve?**

`run_scores_fetcher.py` (Game Data Fetcher) lacks standard CLI arguments for key parameters (`--e2e-test`, `--log-level`, `--request-timeout`, `--historical-season`) and uses `os.chdir()` to manage paths, which is fragile. It also imports config from a module that may not be necessary. These issues make the script harder to test, configure, and maintain.

**Why is this important?**

Standardizing the CLI and removing `os.chdir()` makes the script portable, testable, and consistent with other refactored runner scripts. The `--e2e-test` flag is required for CLI integration test framework participation.

**Who is affected?**

Developers maintaining or testing the game data fetcher; the CLI integration test framework.

---

## Goals & Success Metrics

**Primary Goals:**
1. Add `--e2e-test`, `--log-level`, `--request-timeout`, and `--historical-season` CLI arguments
2. Remove `os.chdir()` calls; use absolute paths constructed relative to script location
3. Remove unnecessary config module import
4. Add E2E test mode with fixed output path

**Success Metrics:**
- `python run_scores_fetcher.py --e2e-test` exits with code 0
- All parameters configurable via CLI without editing source code
- No `os.chdir()` calls remain
- No regressions in data fetching behavior

**Out of Scope (Explicitly Not Included):**
- Changes to the data fetching logic itself
- New data sources or endpoints

---

## Requirements

### Functional Requirements

1. **New CLI Arguments**
   - `--e2e-test`: Enable E2E test mode
   - `--log-level`: Set logging verbosity (normalized to uppercase)
   - `--request-timeout`: Override default HTTP request timeout
   - `--historical-season`: Specify the season year to fetch

2. **Remove os.chdir()**
   - Replace `os.chdir()` with absolute path construction using `os.path.dirname(__file__)` or similar
   - All file I/O paths should be absolute and computed without changing the working directory

3. **Remove Config Import**
   - Remove unnecessary config module import; use CLI args and sensible defaults instead

4. **E2E Mode**
   - Fetch minimal data (e.g., 1 week) to a fixed `/tmp/` path
   - Exit 0 on success

### Non-Functional Requirements

- **Portability:** Script works regardless of the calling working directory
- **Testability:** `--e2e-test` flag enables automated testing

### Technical Requirements

- **Dependencies:** argparse, existing fetcher logic
- **Integrations:** CLI Integration Test Framework
- **Technology Stack:** Python 3, existing project structure

---

## Research & Background

### Existing Solutions Analysis

**Current State:**
`run_scores_fetcher.py` uses `os.chdir()` for path management and hard-codes some configuration. CLI arguments are limited.

**Research Findings:**
- `os.chdir()` changes the process working directory globally, which can break other relative paths
- Using `os.path.dirname(os.path.abspath(__file__))` provides a stable base for absolute paths
- Other runner scripts are adopting argparse + absolute paths as the standard

**Alternative Approaches Considered:**
1. **Keep os.chdir(), add args only:** Doesn't fix portability
2. **Full argparse + absolute paths (Recommended):** Portable and testable

### Technical Constraints

**Known Limitations:**
- E2E mode must use a real or minimal fetch to verify the pipeline works end-to-end

**Architectural Considerations:**
- Path construction should happen once at startup and be passed through as configuration

---

## Initial Feature Breakdown (Preliminary)

**Proposed Features:**

1. **Feature 1:** CLI Argument Additions
   - **Purpose:** Add `--e2e-test`, `--log-level`, `--request-timeout`, `--historical-season`
   - **Key Components:** argparse setup, defaults matching current behavior

2. **Feature 2:** Path Management Cleanup
   - **Purpose:** Remove `os.chdir()`, use absolute paths throughout
   - **Key Components:** Path construction from `__file__`, update all I/O calls

---

## Dependencies & Risks

### External Dependencies

- **CLI Integration Test Framework:** Will invoke this script with `--e2e-test`

### Risks & Mitigation

| Risk | Impact | Probability | Mitigation Strategy |
|------|--------|-------------|---------------------|
| os.chdir() removal breaks existing callers | Medium | Low | Audit all relative path usage before removing |

---

## Timeline & Resources

**Estimated Timeline:** 1 day

**Team Members Required:**
- Developer: TBD

**Key Milestones:**
1. CLI args added, os.chdir() removed, E2E mode tested: Day 1

---

## Implementation Considerations

### Existing Codebase Integration

**Areas of the Codebase That May Require Changes:**
- `run_scores_fetcher.py`: Add argparse, remove os.chdir(), remove config import, add E2E mode

**Coding Practices to Follow:**
- Use absolute paths, never `os.chdir()`
- Use `type=str.upper` for `--log-level`
- Fixed `/tmp/` paths for E2E output
- Follow CODING_STANDARDS.md

### Testing Strategy (High-Level)

- **End-to-End Tests:** `python run_scores_fetcher.py --e2e-test` exits 0, output in expected path

---

## Open Questions

1. **Minimum E2E fetch:** What is the minimum data fetch needed to verify the pipeline works?
   - **Status:** Unanswered

---

## References

- **Related Docs:** `run_scores_fetcher.py`
- **Related Epics:** CLI Integration Test Framework, League Helper CLI Refactor
- **External Resources:** N/A

---

## Next Steps

**To proceed with this epic:**
1. User reviews this request
2. User says "Start S1 for Game Data Fetcher CLI Modernization"
3. Agent reads `.shamt/guides/stages/s1/s1_epic_planning.md`
4. Agent creates git branch and FF-{N} folder during S1
5. Agent runs S1 Discovery Phase to refine this request

**This request file remains in `.shamt/epics/requests/` until S1 creates the epic folder.**
