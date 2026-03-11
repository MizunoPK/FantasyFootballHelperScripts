# Epic Request: CLI Integration Test Framework

**File Location:** `.shamt/epics/requests/cli-enhancements/integration_test_framework_notes-v2.md`

---

## Epic Overview

**Epic Name:** CLI Integration Test Framework

**Date:** 2026-03-09

**Requested By:** User

**Epic Type:** Infrastructure / Testing

**Estimated Complexity:** Medium

---

## Problem Statement

**What problem does this epic solve?**

There is no automated framework for end-to-end testing of the project's CLI runner scripts. Each runner script (league helper, win rate simulation, accuracy simulation, game data fetcher, historical compiler, player fetcher, schedule fetcher) operates independently with no shared test harness. Regressions in any runner can go undetected until manual testing.

**Why is this important?**

A CLI integration test framework enables automated validation that all runner scripts start correctly, execute their E2E mode successfully, and exit cleanly. This provides a safety net for changes to runner scripts and catches integration regressions early.

**Who is affected?**

Developers making changes to any runner script; CI/CD pipelines that want automated validation.

---

## Goals & Success Metrics

**Primary Goals:**
1. Create a master test runner that invokes all CLI runner scripts with `--e2e-test`
2. Verify each script exits with code 0
3. Verify each script produces expected output in the correct `/tmp/` location
4. Create individual test files for each runner script
5. Produce a comprehensive test guide

**Success Metrics:**
- Master runner executes all CLI script E2E tests in sequence
- All tests pass with 0 failures when all runner scripts are properly refactored
- Test framework is runnable via a single command
- Guide documents how to add tests for new scripts

**Out of Scope (Explicitly Not Included):**
- Unit testing of individual business logic modules (separate concern)
- Performance/load testing
- Testing of data correctness (only CLI entry point and exit code)

---

## Requirements

### Functional Requirements

1. **Master Test Runner**
   - Single entry point that runs all CLI integration tests in sequence
   - Reports pass/fail per script and overall result
   - Usable from command line: `python tests/integration/run_all_cli_tests.py`

2. **Per-Script Test Files**
   - Individual test file for each runner script
   - Tests: script starts, `--e2e-test` exits 0, expected output files created
   - Invokes scripts via `subprocess.run()` with `--e2e-test` flag

3. **Test Guide**
   - Documentation explaining how the framework works
   - How to add tests for new CLI scripts
   - How to run tests locally and in CI

4. **Enhanced Existing Tests** (if applicable)
   - Update any existing E2E-adjacent tests to use the new framework

### Non-Functional Requirements

- **Dependencies:** This epic requires all individual CLI refactor epics to be completed first
- **Reliability:** Tests must be deterministic and repeatable
- **Maintainability:** Adding a new script's tests should require minimal boilerplate

### Technical Requirements

- **Dependencies:** `subprocess` (stdlib), all CLI runner scripts with `--e2e-test` support
- **Integrations:** All 6+ runner scripts (league helper, win rate sim, accuracy sim, game data fetcher, historical compiler, player fetcher, schedule fetcher)
- **Technology Stack:** Python 3, pytest or unittest

---

## Research & Background

### Existing Solutions Analysis

**Current State:**
No CLI integration test framework exists. Some runner scripts have been refactored to support `--e2e-test`, but there is no harness that coordinates their testing.

**Research Findings:**
- Using `subprocess.run()` with `--e2e-test` is the recommended pattern for testing CLI entry points
- The framework should check exit codes and optionally verify output file presence
- All runner scripts must support `--e2e-test` before this framework can be meaningful

**Alternative Approaches Considered:**
1. **Pytest subprocess fixtures:** Works but heavier setup
2. **Simple subprocess.run() harness (Recommended):** Simple, explicit, easy to understand

### Technical Constraints

**Known Limitations:**
- This epic cannot be implemented until all runner scripts have `--e2e-test` support
- Tests depend on `/tmp/` output paths being fixed and consistent across runner scripts

**Architectural Considerations:**
- Test files should mirror the structure of the source runner scripts they test
- Master runner should be runnable standalone without pytest if possible

---

## Initial Feature Breakdown (Preliminary)

**Note:** This is a preliminary breakdown. S1 Discovery Phase will refine this.

**Proposed Features:**

1. **Feature 1:** Master Test Runner
   - **Purpose:** Single entry point for running all CLI integration tests
   - **Key Components:** Test orchestration, pass/fail reporting, exit code aggregation

2. **Feature 2:** Per-Script Test Files
   - **Purpose:** Individual, focused test files for each runner script
   - **Key Components:** subprocess.run() invocations, exit code assertions, output file checks

3. **Feature 3:** Test Guide
   - **Purpose:** Documentation for running, maintaining, and extending the framework
   - **Key Components:** Usage instructions, adding new tests, CI integration guidance

---

## Dependencies & Risks

### External Dependencies

- **League Helper CLI Refactor:** Must be completed before testing league helper
- **Win Rate Simulation E2E:** Must be completed before testing win rate sim
- **Accuracy Simulation E2E:** Must be completed before testing accuracy sim
- **Game Data Fetcher CLI:** Must be completed before testing game data fetcher
- **Historical Compiler CLI:** Must be completed before testing historical compiler
- **Player Fetcher E2E Path Fix:** Must be completed before testing player fetcher
- **Schedule Fetcher CLI:** Must be completed before testing schedule fetcher

### Risks & Mitigation

| Risk | Impact | Probability | Mitigation Strategy |
|------|--------|-------------|---------------------|
| One runner not yet refactored blocks framework | Medium | Medium | Make each test conditional on script availability |
| E2E tests take too long combined | Medium | Low | Set timeout per test, parallelize if needed |
| Flaky output file assertions | Low | Low | Only assert file existence, not content |

---

## Timeline & Resources

**Estimated Timeline:** 2-3 days (after all prerequisite CLI epics complete)

**Team Members Required:**
- Developer: TBD

**Key Milestones:**
1. Master runner + per-script test files: Day 1-2
2. Test guide written: Day 2-3
3. All tests passing: Day 3

---

## Implementation Considerations

### Existing Codebase Integration

**Areas of the Codebase That May Require Changes:**
- `tests/` directory: Add new `integration/` subdirectory with test files and master runner

**New Areas That May Need Creation:**
- `tests/integration/` directory
- One test file per runner script (~5-7 files)
- `tests/integration/run_all_cli_tests.py` master runner
- `tests/integration/README.md` or guide document

**Coding Practices to Follow:**
- Use `subprocess.run()` with `--e2e-test` flag for all invocations
- Check exit code (assert == 0 for success)
- Optionally verify output files in expected `/tmp/` paths
- Follow existing test file naming conventions in `tests/`
- Follow CODING_STANDARDS.md

### Testing Strategy (High-Level)

- **Integration Tests:** This epic IS the integration test layer — each test file invokes a script E2E
- **Meta-testing:** The master runner itself should be runnable and exit 0 when all sub-tests pass

---

## Open Questions

1. **Test framework:** Should tests use pytest, unittest, or plain Python assertions?
   - **Status:** Unanswered

2. **Parallel execution:** Should runner script tests run sequentially or in parallel?
   - **Status:** Unanswered

3. **CI integration:** Should the master runner be integrated into the CI pipeline as part of this epic?
   - **Status:** Unanswered

---

## References

- **Related Docs:** `tests/` directory structure
- **Related Epics:** All CLI refactor epics (prerequisite), League Helper CLI Refactor, Win Rate Simulation E2E, Accuracy Simulation E2E, Game Data Fetcher CLI, Historical Compiler CLI, Player Fetcher E2E Path Fix, Schedule Fetcher CLI
- **External Resources:** Python subprocess docs, pytest docs

---

## Next Steps

**To proceed with this epic:**
1. User reviews this request
2. Ensure all prerequisite CLI epics are complete
3. User says "Start S1 for CLI Integration Test Framework"
4. Agent reads `.shamt/guides/stages/s1/s1_epic_planning.md`
5. Agent creates git branch and FF-{N} folder during S1
6. Agent runs S1 Discovery Phase to refine this request

**This request file remains in `.shamt/epics/requests/` until S1 creates the epic folder.**
