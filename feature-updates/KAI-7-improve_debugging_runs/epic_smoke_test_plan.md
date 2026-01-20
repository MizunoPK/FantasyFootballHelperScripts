# Epic Smoke Test Plan: improve_debugging_runs

**Epic:** KAI-7 - improve_debugging_runs
**Created:** 2026-01-20
**Last Updated:** 2026-01-20

---

## Overview

This document defines how to smoke test the complete epic after all features are implemented.

---

## Pre-Test Checklist

Before running smoke tests:
- [ ] All unit tests pass (`python tests/run_all_tests.py`)
- [ ] All three features implemented
- [ ] `./logs/` directory exists (or will be created)

---

## Smoke Test Procedure

### Test 1: Individual Debug Flags

**Purpose:** Verify each script's --debug flag works independently.

```bash
# Test each script individually
python run_league_helper.py --debug
python run_win_rate_simulation.py --debug
python run_accuracy_simulation.py --debug
python run_player_fetcher.py --debug
python run_game_data_fetcher.py --debug
python run_schedule_fetcher.py --debug
```

**Expected Results:**
- [ ] Each script runs without user input prompts
- [ ] Each script creates a log file in `./logs/`
- [ ] Each script exits with code 0 on success
- [ ] Each script completes in under 60 seconds

### Test 2: Unified Debug Runner

**Purpose:** Verify the unified runner executes all components.

```bash
python run_debug_tests.py
```

**Expected Results:**
- [ ] All 6 components are executed
- [ ] Summary report displayed at end
- [ ] Exit code 0 if all pass
- [ ] Total execution time under 5 minutes
- [ ] Log files created for each component

### Test 3: Normal Mode Regression

**Purpose:** Verify normal (non-debug) mode still works.

```bash
# Verify normal mode isn't broken (interactive test)
python run_league_helper.py
# Should show interactive menu as before
```

**Expected Results:**
- [ ] Normal mode shows interactive menu
- [ ] No debug logging unless --debug flag provided

---

## Success Criteria

| Criteria | Target |
|----------|--------|
| All individual --debug flags work | 6/6 pass |
| Unified runner executes all | 6/6 components |
| Log files created | 6 files in ./logs/ |
| Performance constraint met | < 5 minutes total |
| Normal mode unaffected | Works as before |

---

## Failure Handling

If any smoke test fails:
1. Document the failure in debugging/ folder
2. Fix the issue
3. Re-run ALL smoke tests from the beginning
4. Do not proceed to S10 until all tests pass
