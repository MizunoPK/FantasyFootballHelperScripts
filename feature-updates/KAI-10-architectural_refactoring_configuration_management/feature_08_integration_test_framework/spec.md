## Feature Spec: integration_test_framework

## Discovery Context

**Discovery Document:** `../DISCOVERY.md`

### This Feature's Scope (from Discovery)

Wave 3 — Create 7 CLI integration test runners + master runner + INTEGRATION_TESTING_GUIDE.md. Requires all 7 feature specs complete.

**Key scope items:**
- Create 5 new CLI test files:
  - test_player_fetcher_cli.py
  - test_schedule_fetcher_cli.py
  - test_game_data_fetcher_cli.py
  - test_historical_compiler_cli.py
  - test_league_helper_cli.py
- Enhance 2 existing simulation test files:
  - test_simulation_integration.py (add TestWinRateSimulationCLI class)
  - test_accuracy_simulation_integration.py (add TestAccuracySimulationCLI class)
- Create master runner: run_all_integration_tests.py
- Create INTEGRATION_TESTING_GUIDE.md (~300 lines, 5 sections)
- Each test runner validates: exit codes + specific outcomes (log messages, output files, data values)
- 3-5 argument combinations tested per script
- All tests use --e2e-test mode (≤180 seconds per script)

### Relevant Discovery Decisions

- **Solution Approach:** Integration tests use subprocess to invoke each runner with CLI args; assert exit code 0 and specific outcomes
- **Key Constraints:** All 7 feature specs must be complete before this feature's S2 (needs to know CLI args and E2E behavior per script); INTEGRATION_TESTING_GUIDE.md is this feature's documentation deliverable
- **Dependencies:** Wave 3 — depends on all 7 feature specs (Features 01-07) being complete

### Relevant User Answers (from Discovery)

| Question | Answer | Impact on This Feature |
|----------|--------|----------------------|
| Documentation as separate feature? | No — INTEGRATION_TESTING_GUIDE.md is this feature's deliverable | Create guide in S7.P3 as part of this feature |
| Testing strictness for E2E timeout | Warn only (network variability) | Tests warn but don't fail on >180s timeout |

---

## Feature Requirements

{To be completed in S2}
