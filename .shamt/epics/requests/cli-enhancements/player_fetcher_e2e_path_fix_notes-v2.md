# Epic Request: Player Fetcher E2E Path Fix

**File Location:** `.shamt/epics/requests/cli-enhancements/player_fetcher_e2e_path_fix_notes-v2.md`

---

## Epic Overview

**Epic Name:** Player Fetcher E2E Path Fix

**Date:** 2026-03-09

**Requested By:** User

**Epic Type:** Bug Fix

**Estimated Complexity:** Small

---

## Problem Statement

**What problem does this epic solve?**

The player fetcher's E2E test mode uses `tempfile.mkdtemp()` to create output directories, which produces a new unique path on every run. This makes it impossible to verify E2E output with a fixed path assertion, and is inconsistent with the project-wide convention that E2E test output goes to fixed `/tmp/` paths. Additionally, this epic includes verifying that KAI-10 CLI and E2E implementation work correctly.

**Why is this important?**

The CLI Integration Test Framework depends on all runner scripts writing E2E output to known, fixed paths. Using `tempfile.mkdtemp()` breaks this assumption.

**Who is affected?**

The CLI integration test framework; developers running or verifying player fetcher E2E tests.

---

## Goals & Success Metrics

**Primary Goals:**
1. Replace `tempfile.mkdtemp()` with a fixed path (`/tmp/player_fetcher_e2e/`) in the player fetcher's E2E mode
2. Verify that KAI-10 CLI and E2E implementation is working correctly for the player fetcher

**Success Metrics:**
- Player fetcher E2E mode writes output to `/tmp/player_fetcher_e2e/` (fixed, not a random temp path)
- `python run_player_fetcher.py --e2e-test` exits 0
- CLI integration test framework can verify output at the fixed path

**Out of Scope (Explicitly Not Included):**
- Changes to fetching logic
- New CLI arguments beyond what KAI-10 already added

---

## Requirements

### Functional Requirements

1. **Fixed E2E Output Path**
   - Replace `tempfile.mkdtemp()` with `/tmp/player_fetcher_e2e/` as the E2E output directory
   - Create directory if it does not exist
   - Clean up or overwrite contents on each E2E run

2. **KAI-10 Verification**
   - Verify the existing CLI and E2E implementation for the player fetcher is correct and complete

### Non-Functional Requirements

- **Consistency:** Output path matches the project convention for E2E test output paths

### Technical Requirements

- **Dependencies:** Existing player fetcher runner script
- **Integrations:** CLI Integration Test Framework (fixed path required)
- **Technology Stack:** Python 3

---

## Research & Background

### Existing Solutions Analysis

**Current State:**
Player fetcher E2E mode uses `tempfile.mkdtemp()` which generates a random unique path like `/tmp/tmpXXXXXX/`.

**Research Findings:**
- All other runner scripts in the project use fixed `/tmp/{script_name}_e2e_test/` paths
- `tempfile.mkdtemp()` prevents path-based verification by the integration test framework

**Alternative Approaches Considered:**
1. **Keep mkdtemp(), have tests look up the path:** Complex, fragile
2. **Fixed /tmp/ path (Recommended):** Simple, consistent, reliable

### Technical Constraints

**Known Limitations:**
- Fixed path may have leftover contents from previous runs; tests should handle this gracefully

---

## Initial Feature Breakdown (Preliminary)

**Proposed Features:**

1. **Feature 1:** E2E Path Fix
   - **Purpose:** Replace `tempfile.mkdtemp()` with fixed `/tmp/player_fetcher_e2e/` path
   - **Key Components:** Path constant definition, directory creation logic

2. **Feature 2:** KAI-10 Verification
   - **Purpose:** Confirm the existing CLI and E2E implementation is correct
   - **Key Components:** Manual verification checklist, any fixes needed

---

## Dependencies & Risks

### External Dependencies

- **CLI Integration Test Framework:** Depends on this fix being complete

### Risks & Mitigation

| Risk | Impact | Probability | Mitigation Strategy |
|------|--------|-------------|---------------------|
| Previous test artifacts in fixed path cause failures | Low | Low | Clean or overwrite path at start of E2E run |

---

## Timeline & Resources

**Estimated Timeline:** 0.5 day

**Team Members Required:**
- Developer: TBD

**Key Milestones:**
1. Path fix implemented and verified: Day 1

---

## Implementation Considerations

### Existing Codebase Integration

**Areas of the Codebase That May Require Changes:**
- Player fetcher runner script: Replace `tempfile.mkdtemp()` with fixed path constant

**Coding Practices to Follow:**
- Use `/tmp/player_fetcher_e2e/` as the fixed E2E output path
- Create directory with `os.makedirs(path, exist_ok=True)`
- Follow CODING_STANDARDS.md

### Testing Strategy (High-Level)

- **End-to-End Tests:** Player fetcher E2E exits 0 and writes to `/tmp/player_fetcher_e2e/`

---

## Open Questions

1. **KAI-10 scope:** What specific aspects of the KAI-10 CLI implementation need verification?
   - **Status:** Unanswered

---

## References

- **Related Docs:** `run_player_fetcher.py`, KAI-10 epic
- **Related Epics:** CLI Integration Test Framework, League Helper CLI Refactor (KAI-10)
- **External Resources:** N/A

---

## Next Steps

**To proceed with this epic:**
1. User reviews this request
2. User says "Start S1 for Player Fetcher E2E Path Fix"
3. Agent reads `.shamt/guides/stages/s1/s1_epic_planning.md`
4. Agent creates git branch and FF-{N} folder during S1
5. Agent runs S1 Discovery Phase to refine this request

**This request file remains in `.shamt/epics/requests/` until S1 creates the epic folder.**
