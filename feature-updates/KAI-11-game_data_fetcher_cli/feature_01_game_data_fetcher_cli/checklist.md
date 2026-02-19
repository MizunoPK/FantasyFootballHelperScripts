## Feature Checklist: game_data_fetcher_cli

**Purpose:** Track resolved vs pending decisions for this feature.
**Created:** 2026-02-19 (S1)
**Status:** Empty — will populate in S2

---

## Open Questions

{No open questions — all design decisions resolved in KAI-10 S2.
S2 will verify nothing has changed and confirm final checklist.}

---

## Resolved Decisions

| # | Question | Answer | Source | Resolved |
|---|----------|--------|--------|----------|
| 1 | Should `--request-timeout` or `--rate-limit-delay` be exposed? | `--request-timeout` only (rate-limit-delay unused in code) | KAI-10 S2 | 2026-02-18 |
| 2 | Should `--data-folder`, `--validate`, `--clean` be in scope? | No — out of scope | KAI-10 S2 | 2026-02-18 |
| 3 | Which week for E2E test? | Week 1 — deterministic | KAI-10 S2 | 2026-02-18 |
| 4 | Should a `--debug` flag be added? | No — use `--e2e-test --log-level DEBUG` | KAI-10 S2 | 2026-02-18 |
| 5 | How to detect historical season after config removal? | Add `--historical-season` flag | KAI-10 S2 | 2026-02-18 |

---

## S2 Verification Items

{Items for S2 to confirm before finalizing spec:}

- [ ] Verify `fetch_game_data()` signature still accepts `request_timeout` (KAI-10 REQ-09)
- [ ] Verify no new args added to `run_game_data_fetcher.py` since KAI-10 spec
- [ ] Verify E2E output path `/tmp/game_data_e2e_test.csv` doesn't conflict with anything
- [ ] Confirm test file naming convention: `test_run_game_data_fetcher.py`
