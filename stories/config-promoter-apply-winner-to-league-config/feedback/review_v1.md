# Code Review v1: config-promoter

**Reviewed:** 2026-06-11
**Story:** stories/config-promoter-apply-winner-to-league-config/
**Mode:** Story mode (Quick path)
**Scope:** `simulation/win_rate/config_promoter.py` (new), `tests/simulation/win_rate/test_config_promoter.py` (new)

---

## Plan Alignment

N/A — Quick path; the Build Checklist in `spec.md` was the build contract (no `implementation_plan.md`). Build followed it: branch from local `main` (D5), create the module + test file, verify. The two created files match the spec's Code Shapes and Build Checklist exactly.

---

## Summary

The promotion writer lands the top-ranked sweep combination into the live `league_config.json`. Implementation composes the committed pieces (`rank_combinations`, `apply_draft_overrides`, `load_valid_strategies`) around a raw-JSON read and an atomic write, with a read-only git dirty-state warning. All spec Requirements and Design Decisions (D1–D5) are realized.

**Verdict:** Approve. No blocking or concern-level findings.
**Degree of risk:** Low. It mutates a git-tracked file via an atomic write; the prior config is recoverable via `git checkout`. The destructive surface is bounded (only `DRAFT_ORDER` + 7 params change) and fully covered by tests including the write-failure path.

---

## Changed File Inventory

| File | Type | Notes |
|------|------|-------|
| `simulation/win_rate/config_promoter.py` | New module | `promote_best_combination` + `_resolve_draft_order`, `_read_config`, `_has_uncommitted_changes`, `_atomic_write_json` |
| `tests/simulation/win_rate/test_config_promoter.py` | New tests | `TestConfigPromoter` — 12 methods, all passing; full suite 2841/2841 |

---

## Findings by severity

**BLOCKING:** None.
**CONCERN:** None.
**SUGGESTION:** None material — the module is small, single-responsibility, and mirrors the established `SweepResultsManager._save` atomic-write idiom.
**NITPICK:** None.

---

## 16-category pass

- **Correctness** — Ranks `n=1`, takes `[0]` (safe: `combinations` is non-empty past the guard, so `rank_combinations` yields ≥1 row). Winner's `DRAFT_ORDER` resolved by exact filename match; the stored `param_values` are exactly the 7 keys `apply_draft_overrides` requires. ✓
- **Security** — Git probe is read-only (`git status --porcelain`); no shell string interpolation (argument list form); no secrets. ✓
- **Performance** — One store read, one strategy scan, one file write; negligible. ✓
- **Maintainability** — Four small private helpers; clear docstrings; reuses committed components rather than duplicating logic. ✓
- **Testing** — 12 unit tests cover happy path, preservation, cumulative-vs-best ranking, four error paths (all assert no write), git warn/clean/graceful, and write-failure (FileOperationError + tmp cleanup). ✓
- **Edge Cases** — Empty store, strategy absent, no strategy files (`FileNotFoundError`→`ConfigurationError`), missing/corrupt config, git missing, write failure — all handled and tested. ✓
- **Naming** — `promote_best_combination` and helpers are descriptive; underscore-prefixed privates. ✓
- **Documentation** — Module + function docstrings with `Author:`, `Raises:` sections. ✓
- **Error Handling** — Single consistent `ConfigurationError` for all pre-write failures (no write); `FileOperationError` for write failures; both from the project hierarchy. ✓
- **Concurrency** — N/A — single-shot CLI-invoked writer; atomic rename is the only shared-resource touch. ✓
- **Dependencies** — Only stdlib (`json`, `subprocess`, `pathlib`, `typing`) + in-repo modules. ✓
- **Architecture** — Lives beside its siblings under `simulation/win_rate/`; snake_case utility module per CODING_STANDARDS. ✓
- **CSS Scope** — N/A.
- **State Ownership** — `store` injected (not constructed here), keeping the writer testable and the CLI owning store lifecycle. ✓
- **Response Field Uniformity** — Returns exactly the four documented keys. ✓
- **Monitoring** — `logger.info` on success (what was promoted + win rate/games), `logger.warning` on dirty state. ✓

---

## Documentation Impact Assessment

**Yes — `.shamt-core/project-specific-files/ARCHITECTURE.md` update required.** The win-rate sim becomes a new **writer** of the `data/configs/league_config.json` data store. The data-stores table's Writers column currently reads "Operator; Accuracy sim `--promote`" and must gain "Win-rate sim `--promote`". This was flagged in the spec (Review Prevention — Infrastructure) and is applied in **Phase 7 (Polish)**.

> Note: the user-facing `--promote` CLI flag is the sibling `promote-cli` story; this story delivers only the writer. The ARCHITECTURE wording "`--promote`" anticipates that flag, which is correct as the data-flow entry point.

---
Validated 2026-06-11 — story-mode review, no adversarial sub-agent (zero findings; risk surface fully test-covered)
