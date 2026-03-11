# Epic Request: Accuracy Simulation E2E Test Support

**File Location:** `.shamt/epics/requests/cli-enhancements/accuracy_simulation_e2e_notes-v2.md`

---

## Epic Overview

**Epic Name:** Accuracy Simulation E2E Test Support

**Date:** 2026-03-09

**Requested By:** User

**Epic Type:** Enhancement / Infrastructure

**Estimated Complexity:** Small

---

## Problem Statement

**What problem does this epic solve?**

The Accuracy Simulation runner lacks an `--e2e-test` flag, and its `--log-level` argument is not normalized to uppercase. Without the E2E flag, the script cannot participate in the CLI integration test framework. The log-level normalization issue can cause unexpected behavior when lowercase values are passed.

**Why is this important?**

Consistent E2E test support and correct argument normalization are prerequisites for the CLI Integration Test Framework. All runner scripts must support `--e2e-test` for automated testing.

**Who is affected?**

Developers maintaining or testing the accuracy simulation; the CLI integration test framework.

---

## Goals & Success Metrics

**Primary Goals:**
1. Add `--e2e-test` flag to the accuracy simulation runner
2. In E2E mode: use 1 parameter variation and 1 test value for fast, deterministic execution
3. Write E2E output to a fixed path (`/tmp/accuracy_sim_e2e_test/`)
4. Normalize `--log-level` to uppercase with `CRITICAL` added to the valid choices

**Success Metrics:**
- `python run_simulation.py --e2e-test` (accuracy sim variant) exits with code 0
- E2E run completes within 180 seconds
- `--log-level debug` treated same as `--log-level DEBUG`
- No regressions in normal simulation behavior

**Out of Scope (Explicitly Not Included):**
- Changes to simulation logic or accuracy evaluation algorithms
- New accuracy parameters

---

## Requirements

### Functional Requirements

1. **E2E Test Flag**
   - Add `--e2e-test` boolean flag
   - In E2E mode: use 1 parameter variation, 1 test value, minimal player set

2. **Fixed Output Path**
   - E2E mode writes to `/tmp/accuracy_sim_e2e_test/` (fixed, not `tempfile.mkdtemp()`)

3. **Log Level Normalization**
   - `--log-level` argument uses `type=str.upper` to normalize input
   - Valid choices include: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`

### Non-Functional Requirements

- **Performance:** E2E mode completes within 180 seconds
- **Reliability:** Fixed output paths enable deterministic verification

### Technical Requirements

- **Dependencies:** argparse (stdlib), existing accuracy sim runner
- **Integrations:** CLI Integration Test Framework
- **Technology Stack:** Python 3, existing project structure

---

## Research & Background

### Existing Solutions Analysis

**Current State:**
The accuracy simulation runner has some CLI arguments but lacks `--e2e-test`. `--log-level` may accept values without normalization.

**Research Findings:**
- Using `type=str.upper` on argparse arguments is the idiomatic way to normalize case
- Other runner scripts in the project are being refactored to follow this pattern

**Alternative Approaches Considered:**
1. **Add .upper() call in body:** Works but less clean than `type=str.upper`
2. **type=str.upper in argparse (Recommended):** Idiomatic, validated at parse time

### Technical Constraints

**Known Limitations:**
- E2E mode must complete within time limit; use minimal parameter/value counts
- CRITICAL log level should be available for suppressing all output in tests

**Architectural Considerations:**
- E2E handling should occur before the main simulation dispatch loop

---

## Initial Feature Breakdown (Preliminary)

**Proposed Features:**

1. **Feature 1:** E2E Test Mode + Log Level Fix
   - **Purpose:** Add E2E flag with minimal execution, fix log level normalization
   - **Key Components:** argparse additions, parameter override logic, fixed output path

---

## Dependencies & Risks

### External Dependencies

- **CLI Integration Test Framework:** Will invoke this script with `--e2e-test`

### Risks & Mitigation

| Risk | Impact | Probability | Mitigation Strategy |
|------|--------|-------------|---------------------|
| Minimal E2E params produce insufficient coverage | Low | Low | Verify at least one full accuracy pass completes |

---

## Timeline & Resources

**Estimated Timeline:** 0.5-1 day

**Team Members Required:**
- Developer: TBD

**Key Milestones:**
1. E2E flag and log level fix implemented and tested: Day 1

---

## Implementation Considerations

### Existing Codebase Integration

**Areas of the Codebase That May Require Changes:**
- Accuracy simulation runner script: Add `--e2e-test` flag, log level normalization, fixed output path

**Coding Practices to Follow:**
- Use `type=str.upper` for log level argument
- Use fixed `/tmp/accuracy_sim_e2e_test/` path
- Follow pattern from other E2E-enabled runner scripts

### Testing Strategy (High-Level)

- **End-to-End Tests:** Accuracy sim runner with `--e2e-test` exits 0, output present in expected path
- **Unit Tests:** `--log-level debug` normalizes to `DEBUG`

---

## Open Questions

1. **Runner script name:** Is the accuracy simulation run via a separate script or a mode flag on `run_simulation.py`?
   - **Status:** Unanswered

---

## References

- **Related Docs:** Accuracy simulation runner script
- **Related Epics:** CLI Integration Test Framework, Win Rate Simulation E2E, Position-Specific Accuracy Sim Evaluations
- **External Resources:** N/A

---

## Next Steps

**To proceed with this epic:**
1. User reviews this request
2. User says "Start S1 for Accuracy Simulation E2E Test Support"
3. Agent reads `.shamt/guides/stages/s1/s1_epic_planning.md`
4. Agent creates git branch and FF-{N} folder during S1
5. Agent runs S1 Discovery Phase to refine this request

**This request file remains in `.shamt/epics/requests/` until S1 creates the epic folder.**
