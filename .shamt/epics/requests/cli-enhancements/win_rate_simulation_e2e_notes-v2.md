# Epic Request: Win Rate Simulation E2E Test Support

**File Location:** `.shamt/epics/requests/cli-enhancements/win_rate_simulation_e2e_notes-v2.md`

---

## Epic Overview

**Epic Name:** Win Rate Simulation E2E Test Support

**Date:** 2026-03-09

**Requested By:** User

**Epic Type:** Enhancement / Infrastructure

**Estimated Complexity:** Small

---

## Problem Statement

**What problem does this epic solve?**

`run_simulation.py` (Win Rate Simulation) lacks an `--e2e-test` flag and does not normalize the `--log-level` argument. This means the script cannot participate in the CLI integration test framework, which requires all runner scripts to expose a standardized `--e2e-test` mode that runs deterministically, exits 0, and writes output to fixed `/tmp/` paths.

**Why is this important?**

Consistent E2E test support across all runner scripts is a prerequisite for the CLI Integration Test Framework epic. Without it, automated end-to-end testing of the win rate simulation is not possible.

**Who is affected?**

Developers maintaining or testing the win rate simulation; the CLI integration test framework.

---

## Goals & Success Metrics

**Primary Goals:**
1. Add `--e2e-test` flag to `run_simulation.py`
2. In E2E mode: force `mode=single`, `sims=1`, `workers=1` for fast, deterministic execution
3. Write E2E output to a fixed path (`/tmp/win_rate_e2e_test/`)

**Success Metrics:**
- `python run_simulation.py --e2e-test` exits with code 0
- E2E run completes within 180 seconds
- Output written to `/tmp/win_rate_e2e_test/`
- No regressions in normal simulation behavior

**Out of Scope (Explicitly Not Included):**
- Changes to simulation logic or algorithms
- New simulation modes
- `--log-level` normalization (handled by other epics if needed)

---

## Requirements

### Functional Requirements

1. **E2E Test Flag**
   - Add `--e2e-test` boolean flag to the argparse CLI
   - When set, force simulation parameters to minimal values: `mode=single`, `sims=1`, `workers=1`

2. **Fixed Output Path**
   - E2E mode writes output to `/tmp/win_rate_e2e_test/` (fixed path, not `tempfile.mkdtemp()`)
   - Directory is created if it does not exist

3. **Exit Behavior**
   - E2E mode exits with code 0 on success

### Non-Functional Requirements

- **Performance:** E2E mode completes within 180 seconds
- **Reliability:** Fixed output paths enable deterministic path-based verification in tests

### Technical Requirements

- **Dependencies:** argparse (stdlib), existing simulation runner
- **Integrations:** CLI Integration Test Framework (will call this script with `--e2e-test`)
- **Technology Stack:** Python 3, existing project structure

---

## Research & Background

### Existing Solutions Analysis

**Current State:**
`run_simulation.py` has some CLI arguments but lacks `--e2e-test`. Output paths may use dynamic temp directories.

**Research Findings:**
- Other runner scripts in the project are being refactored to support `--e2e-test`
- Fixed `/tmp/` paths are required (not `tempfile.mkdtemp()`) for consistent E2E verification

**Alternative Approaches Considered:**
1. **Test via pytest mocking:** More complex, doesn't validate CLI entry point
2. **Add `--e2e-test` flag (Recommended):** Simple, consistent with project pattern

### Technical Constraints

**Known Limitations:**
- E2E mode must use minimal simulation parameters to complete within time limit

**Architectural Considerations:**
- E2E flag handling should be near the top of `run_simulation.py` before simulation dispatch

---

## Initial Feature Breakdown (Preliminary)

**Note:** This is a preliminary breakdown. S1 Discovery Phase will refine this.

**Proposed Features:**

1. **Feature 1:** E2E Test Mode
   - **Purpose:** Add `--e2e-test` flag with minimal simulation parameters and fixed output path
   - **Key Components:** argparse flag, parameter override logic, fixed `/tmp/` output path

---

## Dependencies & Risks

### External Dependencies

- **CLI Integration Test Framework:** Will invoke this script with `--e2e-test`

### Risks & Mitigation

| Risk | Impact | Probability | Mitigation Strategy |
|------|--------|-------------|---------------------|
| E2E simulation takes too long | Medium | Low | Force `sims=1`, `workers=1`, `mode=single` |
| Fixed output path conflicts with concurrent runs | Low | Low | Use unique subdirectory or accept sequential-only E2E |

---

## Timeline & Resources

**Estimated Timeline:** 0.5-1 day

**Team Members Required:**
- Developer: TBD

**Key Milestones:**
1. E2E flag implemented and tested: Day 1

---

## Implementation Considerations

### Existing Codebase Integration

**Areas of the Codebase That May Require Changes:**
- `run_simulation.py`: Add `--e2e-test` flag, parameter overrides, fixed output path logic

**New Areas That May Need Creation:**
- None expected

**Coding Practices to Follow:**
- Follow the `--e2e-test` pattern established in other refactored runner scripts
- Use fixed `/tmp/win_rate_e2e_test/` path (not `tempfile.mkdtemp()`)
- Exit 0 on success

### Testing Strategy (High-Level)

- **End-to-End Tests:** `python run_simulation.py --e2e-test` exits 0, output present in `/tmp/win_rate_e2e_test/`

---

## Open Questions

1. **Existing argparse:** Does `run_simulation.py` already have argparse, or does it need to be added from scratch?
   - **Status:** Unanswered

---

## References

- **Related Docs:** `run_simulation.py`
- **Related Epics:** CLI Integration Test Framework, League Helper CLI Refactor, Accuracy Simulation E2E
- **External Resources:** N/A

---

## Next Steps

**To proceed with this epic:**
1. User reviews this request
2. User says "Start S1 for Win Rate Simulation E2E Test Support"
3. Agent reads `.shamt/guides/stages/s1/s1_epic_planning.md`
4. Agent creates git branch and FF-{N} folder during S1
5. Agent runs S1 Discovery Phase to refine this request

**This request file remains in `.shamt/epics/requests/` until S1 creates the epic folder.**
