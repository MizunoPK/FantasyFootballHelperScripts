## Feature Checklist: game_data_fetcher_cli

**Purpose:** Track resolved vs pending decisions for this feature.
**Created:** 2026-02-19 (S1)
**Last Updated:** 2026-02-19 (S2.P1.I1)
**Status:** All items resolved

---

## Open Questions

*None — all design decisions resolved.*

---

## Resolved Decisions

| # | Question | Answer | Source | Resolved |
|---|----------|--------|--------|----------|
| 1 | Should `--request-timeout` or `--rate-limit-delay` be exposed? | `--request-timeout` only (rate-limit-delay unused in code) | KAI-10 S2 | 2026-02-18 |
| 2 | Should `--data-folder`, `--validate`, `--clean` be in scope? | No — out of scope | KAI-10 S2 | 2026-02-18 |
| 3 | Which week for E2E test? | Week 1 — deterministic | KAI-10 S2 | 2026-02-18 |
| 4 | Should a `--debug` flag be added? | No — use `--e2e-test --log-level DEBUG` | KAI-10 S2 | 2026-02-18 |
| 5 | How to detect historical season after config removal? | Add `--historical-season` flag | KAI-10 S2 | 2026-02-18 |
| 6 | Should `parse_args()` be extracted as a module-level function? | Yes (Option A) — enables default-value testing in REQ-11 | User approval | 2026-02-19 |
| 7 | E2E output path: fixed path or random tmpdir? | Fixed path `/tmp/game_data_e2e_test.csv` — always use fixed paths for E2E output | User approval | 2026-02-19 |

---

## S2 Verification Items (confirmed in S2.P1.I1)

| Item | Status | Evidence |
|------|--------|---------|
| `fetch_game_data()` accepts `request_timeout` | ✅ Confirmed | KAI-10 applied; constructor + fetch_game_data() both accept `request_timeout=30` |
| No new args added to runner since KAI-10 spec | ✅ Confirmed | Still 4 args, all `default=None` — runner unchanged since KAI-10 was planned |
| `/tmp/game_data_e2e_test.csv` — no conflicts | ✅ Confirmed | Standard /tmp, hardcoded path (different from player fetcher's random tmp dir) |
| Test file naming: `test_run_game_data_fetcher.py` | ✅ Confirmed | Consistent with project convention (test_ prefix) |
