# Epic Ticket: improve_configurability_of_scripts

**Created:** 2026-01-28
**Status:** VALIDATED

---

## Description

This epic transforms all runner scripts from hard-coded, interactive-only systems into fully configurable, testable command-line tools. Each of the 7 runner scripts will accept command-line arguments to control behavior, support debug logging mode, and provide fast end-to-end test modes (~3 minutes each) for integration testing. The epic delivers a comprehensive integration test framework with per-script test runners and a master test runner that validates all argument combinations, enabling confident testing during epic development workflows and future maintenance.

---

## Acceptance Criteria (Epic-Level)

**The epic is successful when ALL of these are true:**

- [ ] All 7 runner scripts accept command-line arguments (run_league_helper.py, run_player_fetcher.py, run_schedule_fetcher.py, run_win_rate_simulation.py, run_accuracy_simulation.py, run_game_data_fetcher.py, compile_historical_data.py)
- [ ] Each runner script has `--debug` flag that enables debug-level logging throughout the module
- [ ] Each runner script has `--e2e-test` mode that completes full end-to-end run in ≤3 minutes
- [ ] League helper has `--mode` and `--submode` arguments that skip interactive prompts and run specific flows
- [ ] All simulation runners have E2E test modes with minimal iterations/test values
- [ ] 7 individual integration test runners exist (one per script) that test multiple argument combinations
- [ ] Master integration test runner (`tests/integration/run_all_integration_tests.py`) executes all 7 test runners
- [ ] All integration tests pass/fail based on presence of errors (exit code 0 = pass, non-zero = fail)
- [ ] Documentation updated with argument descriptions, E2E mode usage, and integration test workflows
- [ ] Epic workflow guides (S7/S9) reference integration test runners for testing stages

---

## Success Indicators

**Measurable metrics that show epic succeeded:**

- Runner coverage: 7/7 scripts enhanced with arguments (100%)
- Argument coverage: Each script has ≥3 configurable arguments (--debug, --e2e-test minimum)
- E2E performance: All E2E modes complete in ≤3 minutes (180 seconds)
- Integration test coverage: 7 individual + 1 master = 8 total test runners
- Test pass rate: 100% of integration tests pass on first S9 epic testing run
- Documentation completeness: All new arguments documented with examples
- Debug logging: All 7 scripts emit debug logs when `--debug` flag used
- League helper modes: 4 modes + submodes all accessible via arguments (no interactive prompts in E2E)

---

## Failure Patterns (How We'd Know Epic Failed)

**These symptoms indicate the epic FAILED its goals:**

❌ Any runner script still requires interactive input when arguments provided
❌ E2E test modes take >5 minutes (too slow for rapid testing)
❌ Integration test runners fail due to internal errors (not legitimate bugs)
❌ League helper E2E mode skips modes/submodes instead of testing them
❌ Debug logging produces no output or same output as info level
❌ Arguments don't actually change behavior (cosmetic only)
❌ Integration tests pass even when scripts have errors (false positives)
❌ Master test runner doesn't actually run all individual runners
❌ Documentation missing or unclear about how to use new arguments
❌ Unit test pass rate drops below 100% due to epic changes

---

## Scope Boundaries

✅ **In Scope (What IS included):**
- Adding argparse to all 7 runner scripts
- Creating E2E test modes for all scripts (≤3 min execution)
- Adding debug logging support across all modules
- Creating 7 individual integration test runners
- Creating 1 master integration test runner
- Updating README.md, ARCHITECTURE.md, and creating testing guide
- Updating epic workflow guides to reference integration tests
- League helper argument support for modes, submodes, config paths
- Simulation E2E modes with reduced iterations/test values
- All argument validation and error handling

❌ **Out of Scope (What is NOT included):**
- Modifying scoring algorithms or business logic
- Adding new features to league helper modes (only making existing features testable)
- Changing simulation algorithms (only making them configurable)
- Modifying data fetching API logic (only adding configuration)
- Creating web UI or graphical interface
- Performance optimizations beyond E2E test mode requirements
- Automated CI/CD integration (manual test runner execution only)
- Supporting configuration files (command-line arguments only)

---

## User Validation

**This section filled out by USER - agent presents ticket and asks user to verify/approve**

**User comments:**


**User approval:** YES
**Approved by:** User
**Approved date:** 2026-01-28

---

## Notes

**Why this ticket matters:**
This ticket validates agent understanding of epic outcomes BEFORE creating folder structure. It focuses on WHAT the epic achieves (fully configurable scripts with E2E testing) rather than HOW it's implemented (argparse details, test framework design). During S5 Iteration 25 (Spec Validation), each feature's spec.md will be validated against this ticket to ensure alignment with epic-level goals.

**Epic complexity:**
This is a LARGE epic (9 features, 7 scripts, 8 test runners) that requires careful sequencing. Each script is unique, so implementing one feature per script allows lessons learned to be applied progressively from simple scripts (player fetcher) to complex scripts (league helper).

**Outcome-focused approach:**
- Epic ticket describes WHAT (configurable scripts, E2E modes, integration tests), not HOW (argparse structure, test framework architecture)
- Allows agent to research each script's unique needs in S2
- Prevents premature specification before understanding script-specific requirements
