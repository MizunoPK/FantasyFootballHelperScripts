# Epic Request: Historical Compiler CLI Modernization

**File Location:** `.shamt/epics/requests/cli-enhancements/historical_compiler_cli_notes-v2.md`

---

## Epic Overview

**Epic Name:** Historical Compiler CLI Modernization

**Date:** 2026-03-09

**Requested By:** User

**Epic Type:** Enhancement / Infrastructure

**Estimated Complexity:** Small

---

## Problem Statement

**What problem does this epic solve?**

The Historical Compiler runner lacks standard CLI arguments (`--e2e-test`, `--log-level`, `--timeout`, `--rate-limit-delay`) and currently defines `REQUEST_TIMEOUT` and `RATE_LIMIT_DELAY` as constants in the source code, making them hard to override without modifying code. E2E test mode is also absent, blocking CLI integration test framework participation.

**Why is this important?**

Moving configuration to CLI arguments improves flexibility and eliminates the need to edit source files for common tuning. The `--e2e-test` flag is required for the CLI integration test framework.

**Who is affected?**

Developers running or testing the historical compiler; the CLI integration test framework.

---

## Goals & Success Metrics

**Primary Goals:**
1. Add `--e2e-test`, `--log-level`, `--timeout`, and `--rate-limit-delay` CLI arguments
2. Remove `REQUEST_TIMEOUT` and `RATE_LIMIT_DELAY` constants; source from CLI args instead
3. Add E2E test mode using a temporary directory (in this case `tempfile.TemporaryDirectory()` is acceptable for the historical compiler's E2E mode)
4. Exit 0 on E2E success

**Success Metrics:**
- Historical compiler runner accepts all four new CLI arguments
- `--timeout` and `--rate-limit-delay` override what were previously hardcoded constants
- `python [historical_compiler] --e2e-test` exits 0
- No regressions in compilation behavior

**Out of Scope (Explicitly Not Included):**
- Changes to the compilation logic itself
- New data sources

---

## Requirements

### Functional Requirements

1. **New CLI Arguments**
   - `--e2e-test`: Enable E2E test mode
   - `--log-level`: Set logging verbosity (normalized to uppercase)
   - `--timeout`: HTTP request timeout (replaces `REQUEST_TIMEOUT` constant)
   - `--rate-limit-delay`: Delay between requests (replaces `RATE_LIMIT_DELAY` constant)

2. **Remove Constants**
   - Remove `REQUEST_TIMEOUT` and `RATE_LIMIT_DELAY` from constants/source
   - Values sourced from CLI args with defaults matching previous constant values

3. **E2E Mode**
   - Uses `tempfile.TemporaryDirectory()` for temporary output (acceptable for this script)
   - Compiles a minimal dataset and exits 0

### Non-Functional Requirements

- **Flexibility:** Key timing parameters configurable without code changes
- **Testability:** E2E flag enables automated testing

### Technical Requirements

- **Dependencies:** argparse, tempfile, existing compiler logic
- **Integrations:** CLI Integration Test Framework
- **Technology Stack:** Python 3

---

## Research & Background

### Existing Solutions Analysis

**Current State:**
`REQUEST_TIMEOUT` and `RATE_LIMIT_DELAY` are defined as module-level constants. CLI arguments are limited. No E2E test mode exists.

**Research Findings:**
- Moving timing constants to CLI args allows easy overriding for different environments
- Other runner scripts in the project follow the `--e2e-test` pattern

**Alternative Approaches Considered:**
1. **Environment variables for timeout/delay:** Less discoverable than CLI args
2. **CLI args (Recommended):** Consistent with project direction, self-documenting via `--help`

### Technical Constraints

**Known Limitations:**
- `tempfile.TemporaryDirectory()` is acceptable for the historical compiler's E2E mode (unlike other scripts that require fixed `/tmp/` paths)

**Architectural Considerations:**
- Constants removal should be done with care to avoid breaking existing invocations that rely on defaults

---

## Initial Feature Breakdown (Preliminary)

**Proposed Features:**

1. **Feature 1:** CLI Argument Additions + Constants Removal
   - **Purpose:** Add `--timeout`, `--rate-limit-delay`, `--log-level`, `--e2e-test`; remove hardcoded constants
   - **Key Components:** argparse additions, constant removal, defaults matching current values

2. **Feature 2:** E2E Test Mode
   - **Purpose:** Enable automated E2E testing of the historical compiler
   - **Key Components:** `--e2e-test` flag, minimal compilation run, temp directory, exit 0

---

## Dependencies & Risks

### External Dependencies

- **CLI Integration Test Framework:** Will invoke this script with `--e2e-test`

### Risks & Mitigation

| Risk | Impact | Probability | Mitigation Strategy |
|------|--------|-------------|---------------------|
| Default value changes break existing behavior | Medium | Low | Set CLI arg defaults to exact previous constant values |
| E2E compilation fails due to missing data | Medium | Low | Use minimal test fixture data for E2E mode |

---

## Timeline & Resources

**Estimated Timeline:** 1 day

**Team Members Required:**
- Developer: TBD

**Key Milestones:**
1. CLI args added, constants removed, E2E mode implemented and tested: Day 1

---

## Implementation Considerations

### Existing Codebase Integration

**Areas of the Codebase That May Require Changes:**
- Historical compiler runner script: Add argparse, remove constants, add E2E mode
- Any module that imports `REQUEST_TIMEOUT` or `RATE_LIMIT_DELAY` from the runner: Update to receive values via parameter

**Coding Practices to Follow:**
- Defaults for `--timeout` and `--rate-limit-delay` must match previous constant values exactly
- Use `type=str.upper` for `--log-level`
- Follow CODING_STANDARDS.md

### Testing Strategy (High-Level)

- **Unit Tests:** Verify CLI args are parsed and passed correctly to compilation functions
- **End-to-End Tests:** `--e2e-test` exits 0, temp directory created and populated

---

## Open Questions

1. **Files affected:** Which modules currently import `REQUEST_TIMEOUT` and `RATE_LIMIT_DELAY`?
   - **Status:** Unanswered

---

## References

- **Related Docs:** Historical compiler runner script, `player-data-fetcher/` module
- **Related Epics:** CLI Integration Test Framework, Game Data Fetcher CLI Modernization
- **External Resources:** N/A

---

## Next Steps

**To proceed with this epic:**
1. User reviews this request
2. User says "Start S1 for Historical Compiler CLI Modernization"
3. Agent reads `.shamt/guides/stages/s1/s1_epic_planning.md`
4. Agent creates git branch and FF-{N} folder during S1
5. Agent runs S1 Discovery Phase to refine this request

**This request file remains in `.shamt/epics/requests/` until S1 creates the epic folder.**
