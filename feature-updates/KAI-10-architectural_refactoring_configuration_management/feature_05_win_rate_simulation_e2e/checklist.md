## Feature Checklist: win_rate_simulation_e2e

**Purpose:** Questions requiring user input before spec can be finalized (Gate 3)
**Guide note:** Agent NEVER marks [x] — only user marks items after Gate 3 approval

---

## Questions

### Q1: Season selection for --e2e-test mode

**Context:** E2E mode forces `mode='single'` + `sims=1`. The single mode calls `run_single_config_test(season='2025')`. In 2026+, only 2026+ data may exist in `simulation/sim_data/`.

- Option A: Keep hardcoded '2025' ← **SELECTED**
- Option B: Auto-detect most recent available season

**User Answer:** A — Keep '2025' hardcoded (matches existing single mode behavior)
**Impact on spec:** REQ-03 uses `season='2025'` for E2E single run (unchanged from current behavior)

| Status | ANSWERED |
|--------|----------|

---

### Q2: Graceful skip behavior when E2E data is missing

**Context:** E2E mode needs a baseline config folder + sim_data. CI environments may not have these.

- Option A: Graceful skip (exit 0 + info message) ← **SELECTED**
- Option B: Preserve exit 1 error

**User Answer:** A — Graceful skip (exit 0 + info message) when baseline config or sim_data missing
**Impact on spec:** REQ-03 — E2E mode checks for data presence first; if missing, logs info and exits 0

| Status | ANSWERED |
|--------|----------|

---

## Gate 3 Approval

[x] User approves spec.md and checklist.md — APPROVED 2026-02-18
