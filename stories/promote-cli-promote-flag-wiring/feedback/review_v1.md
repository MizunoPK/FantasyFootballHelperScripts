# Code Review v1: promote-cli

**Reviewed:** 2026-06-11
**Story:** stories/promote-cli-promote-flag-wiring/
**Mode:** Story mode (Quick path)
**Scope:** `run_win_rate_simulation.py` (edit), `tests/root_scripts/test_run_win_rate_simulation_promote.py` (new), `tests/root_scripts/test_run_win_rate_simulation_sweep.py` (1-line test-helper edit)

---

## Plan Alignment

N/A — Quick path; the spec Build Checklist was the build contract. Build followed it step-for-step: branch from local `main`, add imports + `--promote` flag + dispatch guard/branches + `_run_promote_mode`/`_print_promotion`, update `_sweep_args` (`promote=False`), create the test file, verify. The `_sweep_args` edit — flagged in the spec as a necessary white-box touch — was made exactly as manifested (no surprise builder deviation this time).

---

## Summary

Wires the committed promotion writer to a `--promote` CLI flag with the user-chosen sweep-then-promote dispatch. Thin, single-responsibility helpers mirroring the existing `_run_sweep_mode`/`_print_summary` idiom.

**Verdict:** Approve. No blocking or concern-level findings.
**Degree of risk:** Low. The flag delegates the destructive write to the already-tested `config_promoter`; this story adds only dispatch + clean error-exit, fully covered by 8 new tests. Strategy-only and `--sweep` modes are provably unchanged (their existing tests still pass).

---

## Changed File Inventory

| File | Type | Notes |
|------|------|-------|
| `run_win_rate_simulation.py` | Edit | +2 imports, `--promote` flag, dispatch guard + two branches, `_run_promote_mode` + `_print_promotion` |
| `tests/root_scripts/test_run_win_rate_simulation_promote.py` | New | 8 tests (promote-mode unit, dispatch, flag parsing); all passing |
| `tests/root_scripts/test_run_win_rate_simulation_sweep.py` | Edit | `_sweep_args` gains `promote=False` (so its manual `Namespace` survives `main()` reading `args.promote`) |

Full suite: 2849/2849 (100%), +8.

---

## Findings by severity

**BLOCKING / CONCERN / SUGGESTION / NITPICK:** None.

---

## 16-category pass

- **Correctness** — Dispatch guard (`--endless` + `--promote` → exit 2) precedes the sweep block; non-endless `_run_sweep_mode` returns cleanly so sweep-then-promote reaches promote; all flag combinations traced in validation. ✓
- **Security** — No new external surface; delegates to the writer (read-only git probe there). ✓
- **Performance / Concurrency** — One-shot dispatch; N/A. ✓
- **Maintainability** — `_run_promote_mode`/`_print_promotion` mirror the sweep helpers; thin `main()`. ✓
- **Testing** — 8 tests: writer-invoked + full D3 report, both error paths (exit 1, no report), promote-only/sweep-then-promote(ordered)/endless-reject dispatch, flag default/present. ✓
- **Edge Cases** — Empty store → writer's `ConfigurationError` → exit 1 (covered); `--endless` rejection covered. ✓
- **Naming / Documentation** — Descriptive helper + test names; `--promote` help text states the league_config target and the endless incompatibility. ✓
- **Error Handling** — `ConfigurationError`/`FileOperationError` caught at the CLI boundary → log + non-zero exit; other exceptions propagate. ✓
- **Dependencies / Architecture** — Only adds in-repo imports; flag lives beside the sibling sweep flags. ✓
- **CSS Scope / State Ownership / Response Field Uniformity / Monitoring** — N/A / store owned by the writer / report prints exactly the writer's four-key result / `logger.error` on failure. ✓

---

## Documentation Impact Assessment

**Yes — one additive line to `.shamt-core/project-specific-files/ARCHITECTURE.md`.** The optimization data-flow (around line 260) shows the sweep producing `win_rate_sweep_results.json` but does not yet show `--promote` closing the loop into `data/configs/league_config.json`. Add a `run_win_rate_simulation.py --promote` line. (The `league_config.json` data-stores **writers** column already gained "Win-rate sim `--promote`" in the `config-promoter` story — that anticipatory entry is now fully realized by this flag, so no change needed there.) Applied in **Phase 7 (Polish)**.

---
Validated 2026-06-11 — story-mode review, no adversarial sub-agent (zero findings; risk delegated to the test-covered writer)
