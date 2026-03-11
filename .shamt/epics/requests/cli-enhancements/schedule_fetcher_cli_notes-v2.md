# Epic Request: Schedule Fetcher CLI Modernization

**File Location:** `.shamt/epics/requests/cli-enhancements/schedule_fetcher_cli_notes-v2.md`

---

## Epic Overview

**Epic Name:** Schedule Fetcher CLI Modernization

**Date:** 2026-03-09

**Requested By:** User

**Epic Type:** Enhancement / Infrastructure

**Estimated Complexity:** Small

---

## Problem Statement

**What problem does this epic solve?**

The Schedule Fetcher lacks a proper argparse-based CLI. It currently hard-codes the `NFL_SEASON` constant in the source, making it necessary to edit code to change seasons. It also lacks `--e2e-test` support and standard CLI arguments, preventing it from participating in the CLI integration test framework.

**Why is this important?**

Replacing the hardcoded `NFL_SEASON` constant with a `--season` CLI argument makes the script flexible without code changes. Adding `--e2e-test` support enables automated testing of the schedule fetching pipeline.

**Who is affected?**

Developers running the schedule fetcher; the CLI integration test framework.

---

## Goals & Success Metrics

**Primary Goals:**
1. Add argparse-based CLI with `--season`, `--output-path`, `--e2e-test`, `--log-level`, and `--enable-log-file` arguments
2. Remove `NFL_SEASON` constant; source from `--season` CLI arg
3. E2E mode fetches 1 week to a fixed `/tmp/` path and exits 0

**Success Metrics:**
- `python run_schedule_fetcher.py --season 2025 --e2e-test` exits 0
- `NFL_SEASON` constant removed from source
- Season configurable via `--season` without code changes
- No regressions in schedule fetching behavior

**Out of Scope (Explicitly Not Included):**
- Changes to the schedule data source or API
- New schedule data fields

---

## Requirements

### Functional Requirements

1. **New CLI Arguments**
   - `--season`: NFL season year (replaces `NFL_SEASON` constant)
   - `--output-path`: Override default output path for schedule data
   - `--e2e-test`: Enable E2E test mode
   - `--log-level`: Set logging verbosity (normalized to uppercase)
   - `--enable-log-file`: Toggle file logging

2. **Remove NFL_SEASON Constant**
   - Remove hardcoded `NFL_SEASON` from source
   - `--season` arg with sensible default replaces it

3. **E2E Mode**
   - Fetches 1 week of schedule data
   - Writes output to `/tmp/schedule_e2e_test.csv` (fixed path)
   - Exits 0 on success

### Non-Functional Requirements

- **Flexibility:** Season configurable without source edits
- **Testability:** E2E flag enables automated testing

### Technical Requirements

- **Dependencies:** argparse (stdlib), existing fetcher logic
- **Integrations:** CLI Integration Test Framework
- **Technology Stack:** Python 3

---

## Research & Background

### Existing Solutions Analysis

**Current State:**
Schedule fetcher uses a hardcoded `NFL_SEASON` constant. No argparse CLI exists. No E2E test mode.

**Research Findings:**
- Hardcoded season constants require code changes between seasons
- Other runner scripts use `--season` as a CLI arg

**Alternative Approaches Considered:**
1. **Environment variable for season:** Less discoverable
2. **CLI arg (Recommended):** Discoverable via `--help`, consistent with project pattern

### Technical Constraints

**Known Limitations:**
- E2E mode should fetch minimal data (1 week) to avoid long test runs
- Fixed CSV output path for E2E mode enables simple file-existence verification

---

## Initial Feature Breakdown (Preliminary)

**Proposed Features:**

1. **Feature 1:** Argparse CLI + NFL_SEASON Removal
   - **Purpose:** Add full CLI argument set, remove hardcoded constant
   - **Key Components:** argparse setup, constant removal, default value

2. **Feature 2:** E2E Test Mode
   - **Purpose:** Enable automated E2E testing with fixed output
   - **Key Components:** `--e2e-test` flag, 1-week fetch, fixed `/tmp/` output

---

## Dependencies & Risks

### External Dependencies

- **CLI Integration Test Framework:** Will invoke this script with `--e2e-test`

### Risks & Mitigation

| Risk | Impact | Probability | Mitigation Strategy |
|------|--------|-------------|---------------------|
| NFL_SEASON removal breaks existing invocations | Medium | Low | Provide sensible default (current season) |
| E2E fetch fails if API is unavailable | Medium | Low | Catch and log gracefully; still exit 0 if minimal data obtained |

---

## Timeline & Resources

**Estimated Timeline:** 1 day

**Team Members Required:**
- Developer: TBD

**Key Milestones:**
1. CLI args added, constant removed, E2E mode implemented and tested: Day 1

---

## Implementation Considerations

### Existing Codebase Integration

**Areas of the Codebase That May Require Changes:**
- Schedule fetcher runner script: Add argparse, remove `NFL_SEASON`, add E2E mode
- Any callers that pass the season via another mechanism

**Coding Practices to Follow:**
- Use `type=str.upper` for `--log-level`
- Default `--season` to the current season year
- Use fixed `/tmp/schedule_e2e_test.csv` for E2E output
- Follow CODING_STANDARDS.md

### Testing Strategy (High-Level)

- **End-to-End Tests:** `python [schedule_fetcher] --e2e-test` exits 0, output at `/tmp/schedule_e2e_test.csv`

---

## Open Questions

1. **Default season:** Should `--season` default to the current calendar year or be required?
   - **Status:** Unanswered

---

## References

- **Related Docs:** Schedule fetcher runner script
- **Related Epics:** CLI Integration Test Framework, Game Data Fetcher CLI Modernization
- **External Resources:** N/A

---

## Next Steps

**To proceed with this epic:**
1. User reviews this request
2. User says "Start S1 for Schedule Fetcher CLI Modernization"
3. Agent reads `.shamt/guides/stages/s1/s1_epic_planning.md`
4. Agent creates git branch and FF-{N} folder during S1
5. Agent runs S1 Discovery Phase to refine this request

**This request file remains in `.shamt/epics/requests/` until S1 creates the epic folder.**
