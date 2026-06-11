# Spec: config-promoter

**Created:** 2026-06-11
**Story:** stories/config-promoter-apply-winner-to-league-config/
**Path:** Quick path (default) — risk-triggered validation (mutates the live `league_config.json`)
**Status:** Validated — awaiting Gate 2b approval
**Baseline:** v1
**Baseline status:** Active

Parent Feature: config-auto-promotion · Parent Epic: win-rate-multi-param-sweep

---

## Ticket Summary

- The promotion writer: rank the sweep store, take the #1 combination, resolve the winning strategy's `DRAFT_ORDER`, apply it + the 7 params onto the live `league_config.json` via `apply_draft_overrides` (other keys preserved), and write atomically (tmp→rename); warn if the config has uncommitted git changes.
- Acceptance: promotes the top combination's `DRAFT_ORDER` + 7 params; preserves all other keys; atomic write; empty-store error; dirty-state warning; unit tests.
- Consumed by `promote-cli` (the `--promote` flag).

---

## Problem Summary

After a sweep, the operator wants to land the best `(strategy + params)` combination into the live config in one step. This story delivers that writer: read the accumulated sweep results, pick the highest cumulative-win-rate combination, and write it into `data/configs/league_config.json` — atomically and preserving every other key — with a git dirty-state warning since recovery is git-based.

---

## Proposed Architecture

New module `simulation/win_rate/config_promoter.py` (snake_case utility):

```python
def promote_best_combination(
    store, data_folder: Path,
    config_path: Path = Path("data/configs/league_config.json"),
) -> Dict[str, Any]: ...
```

- **`store`** (injected `SweepResultsManager`) + `data_folder` (for strategy resolution) + `config_path` (the live config) — the CLI constructs the store and calls this.
- Flow:
  1. `combinations = store.get_all_combinations()`; if empty → `ConfigurationError("No sweep combinations to promote …")` (no write).
  2. `best = rank_combinations(combinations, n=1)[0]` — the top by cumulative win rate. Take `best["strategy_id"]` and `best["param_values"]` (already the 7 flat param names, as stored). No min-sample guard (Gate 2a) — promote the #1.
  3. Resolve the winner's `DRAFT_ORDER`: call `strategies, _ = load_valid_strategies(data_folder)` (no `strategy_filter` — fetch the full list, then **linear-search** the triples for `filename == strategy_id`). If the search finds no match → `ConfigurationError(f"Winning strategy {strategy_id} not found among valid strategies")`. Note: with a non-empty store the empty-store guard (step 1) has already passed, so strategy files normally exist; if `load_valid_strategies` itself raises `FileNotFoundError` (every strategy file deleted/invalid since the sweep), catch it and re-raise as `ConfigurationError` so the promoter surfaces a single, consistent error type and writes nothing.
  4. Read the live config raw: `base_config = json.load(open(config_path))` (raw JSON, **not** `ConfigManager` — preserves the exact file structure / all keys). Wrap the read in `try/except (FileNotFoundError, json.JSONDecodeError)` → re-raise as `ConfigurationError(f"Cannot read config {config_path}: …")` so a missing or corrupt config surfaces the same single error type and writes nothing.
  5. `new_config = apply_draft_overrides(base_config, draft_order, best["param_values"])` — sets `DRAFT_ORDER` + the 7 params, preserves everything else (deep-copies the base).
  6. **Git dirty-state warning** (Gate 2a — warn-and-proceed): if `config_path` has uncommitted git changes (`git status --porcelain <path>`, read-only), `logger.warning(...)` that the overwrite will lose uncommitted edits (git can't recover those) — then proceed.
  7. **Atomic write** (`_atomic_write_json`): write `new_config` to a `.tmp` sibling (`json.dump`, `indent=2` to match the file), then `replace()` onto `config_path`. Wrap the whole sequence in `try/except (OSError, PermissionError)` → re-raise as `FileOperationError` (mirrors `SweepResultsManager._save`); the tmp→replace sequence means a mid-write failure leaves `config_path` untouched (no half-written config), and the `except` removes the orphaned `.tmp` (`tmp.unlink(missing_ok=True)`) before re-raising so no stray file is left in `data/configs/`.
  8. Return a dict with **exactly** these four keys — `{"strategy_id": …, "param_values": …, "win_rate": …, "games": …}` (taken from the winning ranked row; no other fields) — for the CLI to report; log what was promoted.

**Pros:** reuses the committed pieces (`rank_combinations`, `apply_draft_overrides`, `load_valid_strategies`); raw-JSON read/write preserves the file exactly; atomic write prevents a half-written config; the git warning surfaces (without blocking) the one loss git can't undo.
**Cons:** improves on the accuracy sim's `propagate_to_configs` (non-atomic, no warning) rather than sharing it — accepted (different store/shape; the accuracy sim is untouched).

---

## Proposed Code Flow

```text
promote-cli (--promote)
   store = SweepResultsManager(data_folder / "win_rate_sweep_results.json")
   result = promote_best_combination(store, data_folder, config_path)
        combos = store.get_all_combinations()            # empty -> ConfigurationError
        best = rank_combinations(combos, 1)[0]            # top by cumulative win rate
        draft_order = (winning strategy's DRAFT_ORDER via load_valid_strategies)
        base = json.load(league_config.json)
        new = apply_draft_overrides(base, draft_order, best.param_values)
        if dirty(league_config.json): logger.warning(...)   # warn-and-proceed
        atomic_write(new, league_config.json)               # tmp -> replace
        return {strategy_id, param_values, win_rate, games}
```

---

## Design Diagram

**Diagram: N/A —** single writer function composing committed components; the new-writer relationship is captured in the ARCHITECTURE data-stores table (Doc Impact below).

---

## Key Design Decisions

| ID | Decision | Summary |
|----|----------|---------|
| D1 | Warn-and-proceed on dirty config | If `league_config.json` has uncommitted git changes, log a warning (the overwrite loses uncommitted edits — git can't recover those) and proceed. No block/force (Gate 2a). |
| D2 | No min-sample guard | Promote the #1 by cumulative win rate regardless of sample size (Gate 2a — the operator reviewed the ranked summary). Empty store is still an error. |
| D3 | Raw-JSON read/write + atomic | Read/write `league_config.json` as raw JSON (preserve exact structure/keys), apply via `apply_draft_overrides`, write atomically (tmp→rename). `ConfigManager` is **not** used (it would merge/transform). |
| D4 | Reuse, don't reinvent | `rank_combinations` (best), `apply_draft_overrides` (apply + preserve), `load_valid_strategies` (winner's `DRAFT_ORDER`) — all committed; `store` injected. |
| D5 | Branch from local `main` (documented exception) | Story branches in this epic are cut from **local `main`**, not the fetched `origin/main`, by user direction. Rationale: local `main` is ahead of `origin/main` by this epic's committed sweep stories (`config_overrides`, `param_value_generation`, `CombinationEvaluator`, `SweepResultsManager`, `sweep_summary`, `SweepTournament`, `budget_sizing`, `strategy_loader`, `--sweep` CLI) plus FF-7; this story's `apply_draft_overrides`/`rank_combinations`/`load_valid_strategies` dependencies exist **only** on local `main`. Branching from `origin/main` would omit them and break the build. Nothing is pushed unless the user explicitly asks. Supersedes the global "branch from fetched remote development branch" invariant for this epic only. |

---

## Requirements

**Functional:**
- [ ] `promote_best_combination(store, data_folder, config_path)` writes the #1 combination (highest cumulative win rate) into `config_path`: the winning strategy's `DRAFT_ORDER` and the 7 params, via `apply_draft_overrides`, with every other key preserved.
- [ ] The winning `DRAFT_ORDER` is resolved by linear-searching `load_valid_strategies(data_folder)`'s triples for `filename == strategy_id`; a missing match — or a `FileNotFoundError` from `load_valid_strategies` (no valid strategy files) — surfaces as `ConfigurationError` with no write.
- [ ] An empty store → `ConfigurationError` and **no write**. A missing/corrupt `config_path` (FileNotFoundError / JSONDecodeError on read) → `ConfigurationError` and **no write** (single consistent error type).
- [ ] The write is atomic (tmp-file → `replace`) and produces valid JSON (2-space indent); `OSError`/`PermissionError` during the write are wrapped as `FileOperationError`, and a mid-write failure leaves `config_path` untouched.
- [ ] A pre-write read-only git dirty-state check on `config_path` logs a warning when uncommitted changes exist, then proceeds (warn-and-proceed).
- [ ] Returns a dict with **exactly** the four keys `strategy_id`, `param_values`, `win_rate`, `games` (from the winning ranked row; no extra fields) describing what was promoted.

**Non-functional:**
- [ ] Matches CODING_STANDARDS (snake_case utility module, module docstring w/ `Author:`, type hints, `get_logger`, `ConfigurationError`/`FileOperationError` from the error hierarchy). The git check (`_has_uncommitted_changes`) runs `git status --porcelain <path>` read-only inside `try/except` and returns `False` on **any** failure (git missing, not a repo, non-zero exit, `subprocess` error) — never crashing the promotion; a `False` result simply skips the warning.

---

## Test Strategy

- **Test kinds in scope:** unit. A real `SweepResultsManager` on `tmp_path` (populated via `update`), a `tmp_path` `league_config.json`, with `load_valid_strategies` and the git-check patched.
- **New test files needed:** `tests/simulation/win_rate/test_config_promoter.py` — promotes the top combination's `DRAFT_ORDER` + 7 params; preserves all other keys; ranks by cumulative win rate (not `best_win_rate`); atomic write → valid JSON reloads; empty-store → `ConfigurationError` + no write; strategy-not-found (linear-search miss) → `ConfigurationError` + no write; `load_valid_strategies` raising `FileNotFoundError` → `ConfigurationError` + no write; missing/corrupt `config_path` → `ConfigurationError` + no write; dirty-state → warning logged + still writes; clean-state → no warning; `_has_uncommitted_changes` swallows a `subprocess`/git failure and returns `False` (no crash); the returned dict has exactly the four keys; a `replace()`/write failure raises `FileOperationError`, leaves `config_path` untouched, and removes the `.tmp` (no orphan).
- **Project conventions:** pytest, `class TestConfigPromoter:`, `tmp_path`, `unittest.mock.patch` for `load_valid_strategies` + the git-check helper. Run `python -m pytest tests/simulation/win_rate/test_config_promoter.py -vv` + full gate.

**Escalation:** introduces a new test file → testing escalates to a full `testing_plan.md` (via `/e3b-write-testing-plan`).

---

## Review Prevention Gates

| Surface | Applies? | Requirement / Prevention | Evidence |
|---------|----------|--------------------------|----------|
| Regulated / sensitive data | No | Public NFL config scalars. | — |
| Tenant isolation | No | Single-operator local tool. | ARCHITECTURE.md |
| Auth / route contract | No | No server/route. | ARCHITECTURE.md |
| Database read/write | No | No DB; reads/writes the local `league_config.json`. | ARCHITECTURE.md |
| Infrastructure / deployment | Yes | **New writer of the live `data/configs/league_config.json`** (a destructive, git-recoverable edit). Prevention: atomic write (no half-written config); read-only git dirty-state warning (surfaces the uncommitted-edit loss git can't undo); only `DRAFT_ORDER` + the 7 params change, all other keys preserved (`apply_draft_overrides`). ARCHITECTURE data-stores writers column gains "Win-rate sim `--promote`" (Documentation Impact, Review/Polish). | D1, D3; feature `Architecture impact` flag |
| Frontend safety | No | No frontend. | — |
| Testing / test data | Yes | New unit tests (`tmp_path` config + store; patched git-check). | Test Strategy |
| Removed/weakened checks | No | Purely additive; no existing check removed. | — |

---

## Out of Scope

- The `--promote` CLI flag — `promote-cli` (it constructs the store + calls this writer).
- The sweep / tournament / summary / store — committed; reused/read here.
- Per-week-range config promotion; any param beyond the 7; the accuracy sim's promotion (untouched).

---

## Open Questions

*(None — D1 (warn-and-proceed) and D2 (no guard) resolved at Gate 2a; interface/empty-store resolved by the architect, D3–D4.)*

---

## Evidence

### Research Findings
- `simulation/win_rate/SweepResultsManager.get_all_combinations()` — `{combo_key: {strategy_id, param_values, best_win_rate, total_wins, total_games, total_runs, last_run}}`; `param_values` are the 7 flat names (as the tournament stored them).
- `simulation/win_rate/sweep_summary.rank_combinations(combinations, n)` — ranked by cumulative win rate (`total_wins/total_games`), tie-broken by games then key; `rank_combinations(combos, 1)[0]` is the winner. Each row carries `strategy_id`, `param_values`, `win_rate` (cumulative), `games`.
- `simulation/win_rate/config_overrides.apply_draft_overrides(base_config, draft_order, param_values)` — deep-copies, sets `DRAFT_ORDER` + the 7 params at precision, preserves all other keys. The stored `param_values` (7 flat names) are directly usable.
- `simulation/win_rate/strategy_loader.load_valid_strategies(data_folder)` — returns `([(filename, DRAFT_ORDER, name)], skipped_count)`; match `filename == strategy_id` for the winner's `DRAFT_ORDER`.
- `data/configs/league_config.json` — `{config_name, description, parameters: {…}}`, 2-space indent; read/write raw to preserve structure.
- `simulation/accuracy/AccuracyResultsManager.propagate_to_configs` — the existing promotion precedent: preserves user-maintained keys but writes via plain `open(path, 'w')` (non-atomic, no warning). This story improves write-safety (atomic + git warning) and is the win-rate-side analogue; the accuracy sim is untouched.
- `utils/error_handler.ConfigurationError` — for empty store / strategy-not-found.

### Architecture And Standards Notes
- CODING_STANDARDS: snake_case utility module (`config_promoter.py`); module docstring + `Author:`; type hints; `get_logger`; error hierarchy; tests mirror source; 100% pass gate; `subprocess` read-only for the git check (graceful if git missing).
- ARCHITECTURE.md: `league_config.json` data-stores row writers = "Operator; Accuracy sim `--promote`" → gains "Win-rate sim `--promote`" (Documentation Impact, applied in Review/Polish).

### Review Prevention Evidence
- Infrastructure (new live-config writer) + Testing surfaces apply. The destructive edit is git-recoverable; mitigations are atomic write + the dirty-state warning + key preservation.

---

## Code Shapes

- `simulation/win_rate/config_promoter.py` (NEW) — `promote_best_combination(store, data_folder, config_path=…) -> Dict[str, Any]` + small helpers `_has_uncommitted_changes(path) -> bool` (read-only `git status --porcelain` in `try/except` → `False` on any failure) and `_atomic_write_json(data, path)` (tmp→replace; `OSError`/`PermissionError` → `FileOperationError`; `except` unlinks the orphaned `.tmp` before re-raising).
- `simulation/win_rate/sweep_summary.rank_combinations` / `config_overrides.apply_draft_overrides` / `strategy_loader.load_valid_strategies` — reused.
- `utils/error_handler.ConfigurationError`, `utils/error_handler.FileOperationError`; `utils/LoggingManager.get_logger`.

---

## Build Checklist

0. BRANCH - per **D5** (documented exception — branch from local `main`, not `origin/main`, to retain this epic's committed sweep dependencies): `git checkout main && git checkout -b feature/config-promoter/kai`. If the branch exists, stop and report.
1. CREATE `simulation/win_rate/config_promoter.py` - module docstring (`Author: Kai Mizuno`); imports (`json`, `subprocess`, `pathlib.Path`, `typing.Any`/`Dict`; `get_logger`; `ConfigurationError`, `FileOperationError`; `rank_combinations`, `apply_draft_overrides`, `load_valid_strategies`); `promote_best_combination` per D1–D5 + the two helpers (`_has_uncommitted_changes` read-only + `try/except`→`False`; `_atomic_write_json` tmp→replace with `OSError`/`PermissionError`→`FileOperationError`).
2. CREATE `tests/simulation/win_rate/test_config_promoter.py` - `class TestConfigPromoter:` with the Test Strategy cases (real store on `tmp_path`; patched `load_valid_strategies` + git-check; mirrors `testing_plan.md`; Phase 5 executes).
3. VERIFY - `python -m pytest tests/simulation/win_rate/test_config_promoter.py -vv` → all pass.

---

## Review Prevention Checklist

- [ ] Infrastructure: atomic write + git dirty-state warning + key preservation for the live-config write (Build step 1); ARCHITECTURE writers-column update flagged for Review/Polish (Documentation Impact).
- [ ] Testing: new unit tests under `tests/simulation/win_rate/` (`tmp_path` config + store) — Build step 2 / Phase 5.
- [ ] No regulated/tenant/auth/DB/frontend/removed-check obligation applies — N/A reasons recorded above.

---

## Verification

- [ ] `python -m pytest tests/simulation/win_rate/test_config_promoter.py -vv` passes.
- [ ] Full gate `python tests/run_all_tests.py` passes (no regression).
- [ ] Manual smoke: with a tmp `league_config.json` + a store holding 2 combinations, `promote_best_combination` writes the higher-cumulative-win-rate combo's `DRAFT_ORDER` + 7 params, leaves other keys intact, and the file is valid JSON; an empty store raises and writes nothing.

---

## Post-Build Review

**Plan Alignment:** N/A - Quick path used spec Build Checklist instead of implementation_plan.md.

**Findings:** [Pending Build.]

---
Validated 2026-06-11 — 5 rounds, 1 adversarial sub-agent confirmed
