# Epic Ticket: improve_debugging_runs

**Epic:** KAI-7
**Created:** 2026-01-20
**Status:** PENDING VALIDATION

---

## Description

Create automated debug/test runs for all major scripts in the Fantasy Football Helper project. The goal is to enable agents (and users) to quickly smoke test each component without manual interaction, generating timestamped log files for validation.

**What this epic delivers:**
- A `--debug` flag on all run_*.py scripts that triggers reduced-scope, verbose execution
- Non-interactive test scenarios for League Helper's 5 modes
- A unified `run_debug_tests.py` script that runs all components and reports pass/fail status
- Timestamped log files in `./logs/` directory for each debug run

---

## Acceptance Criteria

1. **Individual Debug Flags Work**
   - [ ] `python run_league_helper.py --debug` runs all 5 modes non-interactively
   - [ ] `python run_win_rate_simulation.py --debug` runs single config with minimal iterations
   - [ ] `python run_accuracy_simulation.py --debug` runs with minimal test values
   - [ ] `python run_player_fetcher.py --debug` fetches limited data with verbose logging
   - [ ] `python run_game_data_fetcher.py --debug` fetches single week with verbose logging
   - [ ] `python run_schedule_fetcher.py --debug` runs with verbose logging

2. **Unified Runner Works**
   - [ ] `python run_debug_tests.py` executes all components sequentially
   - [ ] Summary report shows pass/fail for each component
   - [ ] Exit code 0 if all pass, non-zero if any fail

3. **Logging Works**
   - [ ] Each debug run creates timestamped log file in `./logs/`
   - [ ] Log files contain verbose output showing execution progress
   - [ ] Log format: `debug_YYYY-MM-DD_HHMMSS_{component}.log`

4. **Non-Interactive Execution**
   - [ ] All debug runs complete without requiring user input
   - [ ] League Helper modes execute predefined test scenarios
   - [ ] Agent can run `python run_debug_tests.py` and validate results from log files

5. **Performance Constraint**
   - [ ] Each individual component debug run completes in under 5 minutes
   - [ ] Full unified debug run (`run_debug_tests.py`) completes in under 5 minutes total
   - [ ] Simulation debug runs use minimal iterations to meet time constraint

---

## Success Indicators

| Indicator | Target | Measurement |
|-----------|--------|-------------|
| All components have --debug flag | 6/6 scripts | Count scripts with flag |
| Unified runner executes all | 6/6 components | Runner output shows all ran |
| Log files created | 1 per component per run | Check ./logs/ directory |
| Non-interactive execution | 0 prompts | Run completes without input() calls |
| Exit codes meaningful | 0=pass, non-zero=fail | Verify return codes |
| Full debug run under 5 minutes | < 300 seconds | Time unified runner execution |

---

## Failure Patterns

These would indicate the epic is NOT complete:

1. **Hanging execution** - Any debug run waits for user input
2. **Missing logs** - Debug run completes but no log file created
3. **Silent failures** - Component fails but exit code is 0
4. **Incomplete coverage** - Unified runner skips components
5. **Broken normal mode** - Adding --debug flag breaks normal (non-debug) execution
6. **Timeout exceeded** - Any debug run takes longer than 5 minutes (especially simulations)

---

## Out of Scope (Explicitly Excluded)

- Mock data support (debug runs will hit real APIs)
- GUI or visual debugging tools
- Integration with pytest or other test frameworks
- Performance benchmarking or timing metrics
- Historical debug result storage

---

## Features

| # | Feature | Size | Purpose |
|---|---------|------|---------|
| 1 | debug_infrastructure | SMALL | Shared utilities, logging setup, configuration |
| 2 | league_helper_debug | MEDIUM | Non-interactive debug mode for 5 League Helper modes |
| 3 | unified_debug_runner | MEDIUM | Single script to run all debug tests |

---

## Discovery Reference

This epic ticket is based on findings documented in `DISCOVERY.md`, including:
- 2 research iterations
- 4 user questions resolved
- Solution approach: Combined --debug flags + unified runner
