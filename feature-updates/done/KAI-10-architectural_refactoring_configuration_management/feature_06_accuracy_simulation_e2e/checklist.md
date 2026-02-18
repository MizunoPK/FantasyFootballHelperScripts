## Feature Checklist: accuracy_simulation_e2e

**Status:** S2.P1 COMPLETE — Gate 3 approved by user 2026-02-18
**Last Updated:** 2026-02-18

---

## Open Questions (PENDING USER ANSWERS)

*(None — all questions resolved)*

---

## Answered Questions

### Q3: Should --e2e-test override max_workers (parallel workers)?

**Answer:** Option A — keep default max_workers. `--e2e-test` only limits `parameter_order` (1 parameter) and `test_values` (1 value). Max_workers unchanged; user can pass `--max-workers 1` manually if desired.

**Source:** User answer (2026-02-18)

**Impact on spec:** REQ-01 implementation passes `max_workers=args.max_workers` unchanged — confirmed correct.

**Status:** [x] RESOLVED

---

## Answered Questions

### Q1: --log-level normalization approach — ANSWERED by Feature 01 precedent

**Answer:** Option C — `type=str.upper` + uppercase choices (best of both worlds)

**Source:** Feature 01 spec (authoritative design reference):
- choices: `['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']` (uppercase)
- default: `'INFO'` (uppercase)
- `type=str.upper` accepts lowercase input and normalizes it → zero breaking changes

**Impact on spec:** REQ-02 uses this approach. Existing test `test_existing_log_level_flag_unchanged` result changes from `'debug'` to `'DEBUG'` (minor update required).

**Status:** [x] RESOLVED

---

### Q2: --debug scope reduction — ELIMINATED (no --debug flag)

**Answer:** N/A — design correction in handoff package (2026-02-18) eliminated the --debug flag entirely.

**Source:** Handoff package design correction: "Universal args are --e2e-test and --log-level only. NO separate --debug flag."

**Developers who want verbose debug output use:** `--e2e-test --log-level DEBUG`

**Status:** [x] RESOLVED — question eliminated with --debug flag

---

## Questions That Were Pre-Answered (from Feature 01 spec or Discovery)

| Topic | Answer | Source |
|-------|--------|--------|
| No separate --debug flag | Correct — eliminated | Handoff correction 2026-02-18 + Feature 01 spec update |
| --e2e-test scope: limit parameters? | Yes — 1 parameter, 1 test value | Feature 01 E2E pattern + ≤180s constraint |
| Backward compatibility required? | Yes — all 10 existing args preserved | EPIC_TICKET.md zero regression requirement |
| --log-level: uppercase or lowercase? | Uppercase choices + type=str.upper (backward compat) | Feature 01 spec precedent |
| Constructor parameter pattern in AccuracySimulationManager? | Already implemented | S2 research — constructor takes all params |
| Config imports to remove from run_accuracy_simulation.py? | None (no config module imported) | S2 research — module uses inline constants only |
| --e2e-test completes in ≤180s? | Yes (required) | Epic Request AC-03 |
| --e2e-test requires sim_data/? | Yes — unlike API-based scripts, accuracy sim needs real historical data | S2 research — AccuracySimulationManager reads local files |
