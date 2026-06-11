# Testing Plan: config-promoter

**Note:** Produced during Phase 3b because `.shamt-core/shamt-config.json` sets `testing: "enabled"` and this Quick-path story introduces a new test file (escalates from the inline checklist). Executed during Phase 5 (Test) by the `test-executor` persona (Haiku tier).

**Created:** 2026-06-11
**Story:** stories/config-promoter-apply-winner-to-league-config/
**Spec:** stories/config-promoter-apply-winner-to-league-config/spec.md
**Implementation Plan:** N/A (Quick path — built from spec Build Checklist)
**Path:** Quick path (risk-triggered validation — mutates the live `league_config.json`)
**Baseline:** v1
**Baseline status:** Active

---

## Test Strategy

`promote_best_combination` composes committed pure functions around two side effects — a raw-JSON read and an atomic write of `league_config.json` — plus a read-only git probe. Coverage is **unit-only**, exercised against a real `SweepResultsManager` on `tmp_path` and a `tmp_path` copy of the real `league_config.json`, with `load_valid_strategies` and the git probe patched. Per CODING_STANDARDS: pytest, tests mirror source at `tests/simulation/win_rate/test_config_promoter.py`, `class TestConfigPromoter:` with `test_<thing>_<condition>` methods, plain `assert`, `pytest.raises` / `caplog` for error and warning paths.

- **End-to-end:** N/A — no runnable CLI path in this story (the `--promote` flag is the sibling `promote-cli` story); the function is invoked directly with an injected store.
- **Integration:** the read→apply→write chain against a real `SweepResultsManager` store and a real-shaped `league_config.json` on `tmp_path` is the integration surface; `load_valid_strategies` (filesystem strategy scan) and the git probe are patched to keep the test hermetic.
- **Unit:** `simulation/win_rate/config_promoter.promote_best_combination` + helpers `_has_uncommitted_changes`, `_atomic_write_json` — all behaviors in the spec Requirements (D1–D5).
- **Test runner:** `pytest` — `python -m pytest tests/simulation/win_rate/test_config_promoter.py -vv`; full gate `python tests/run_all_tests.py`.
- **Test file conventions:** new file `tests/simulation/win_rate/test_config_promoter.py`; `class TestConfigPromoter:`; the 7 flat param names per `tests/simulation/win_rate/test_SweepResultsManager.py`'s `_param_values` helper (`DRAFT_NORMALIZATION_MAX_SCALE`, `SAME_POS_BYE_WEIGHT`, `DIFF_POS_BYE_WEIGHT`, `PRIMARY_BONUS`, `SECONDARY_BONUS`, `ADP_SCORING_WEIGHT`, `PLAYER_RATING_SCORING_WEIGHT`); the base config is a `tmp_path` **copy of the real `data/configs/league_config.json`** so structure is guaranteed; assertions on the promoted 7 params use `config_overrides.extract_draft_param_values` rather than hardcoded nested paths.
- **Project assumptions checked:** `utils/error_handler.ConfigurationError` and `FileOperationError` importable; the store is populated via `SweepResultsManager.update(strategy_id, param_values, win_rate, wins, games)` so `get_all_combinations` / `rank_combinations` see real records; `load_valid_strategies` is patched on the `config_promoter` module namespace (where it is imported), returning `([(filename, DRAFT_ORDER, name)], skipped_count)`.

**`-k` token discipline:** tokens below (`promotes_winner`, `four_keys`, `keys_preserved`, `cumulative`, `empty_store`, `strategy_absent`, `filenotfound`, `config_missing`, `dirty`, `clean`, `git_swallows`, `write_failure`) are each chosen to be **non-substrings** of the path components `win_rate` / `simulation` / `config_promoter`, so `-k` selects exactly the intended methods (pytest exits 5 — not 0 — if a `-k` matches nothing, so each step asserts ≥1 selected).

---

## Test Plan Steps

### Step 1: Happy path — promotes the winning combination; returns exactly four keys
**Type:** unit
**File:** `tests/simulation/win_rate/test_config_promoter.py`
**Invocation:** `python -m pytest tests/simulation/win_rate/test_config_promoter.py -k "promotes_winner or four_keys" -vv`
**Pass criterion:** All selected tests pass (≥1 selected). Covers: with a store holding the winning combination (a strategy filename + the 7 param values) and `load_valid_strategies` patched to return that strategy's sentinel `DRAFT_ORDER`, after `promote_best_combination` the `tmp_path` config's `DRAFT_ORDER` equals the winner's list verbatim and `extract_draft_param_values(promoted)` equals the stored `param_values`; and the returned dict has **exactly** the keys `{strategy_id, param_values, win_rate, games}` (no more, no fewer), with values drawn from the winning ranked row.
**Expected test methods:** `test_promotes_winner_draft_order_and_params`, `test_returns_exactly_four_keys`.
**Covers:** spec Requirements — functional bullets 1, 6; Acceptance Criteria 1–3; D3, D4.

---

### Step 2: Key preservation and cumulative-win-rate ranking
**Type:** unit
**File:** `tests/simulation/win_rate/test_config_promoter.py`
**Invocation:** `python -m pytest tests/simulation/win_rate/test_config_promoter.py -k "keys_preserved or cumulative" -vv`
**Pass criterion:** All selected tests pass (≥1 selected). Covers: (a) every `league_config.json` key other than `DRAFT_ORDER` and the 7 params (`config_name`, `description`, and `parameters` keys such as `CURRENT_NFL_WEEK`, `NFL_SEASON`, `MAX_POSITIONS`, `FLEX_ELIGIBLE_POSITIONS`, `INJURY_PENALTIES`) is byte-identical to the base copy after promotion; (b) given two combinations — A with a high single-run `best_win_rate` but lower **cumulative** rate (e.g. `update(0.9, 9, 10)` then `update(0.0, 0, 10)` → cumulative 0.45, best 0.9) and B with higher cumulative (`update(0.6, 6, 10)` → cumulative 0.6) under a distinct strategy filename — B is the one promoted (its `DRAFT_ORDER` lands), proving ranking uses cumulative `total_wins/total_games`, not `best_win_rate`.
**Expected test methods:** `test_other_keys_preserved`, `test_ranks_by_cumulative_not_best`.
**Covers:** spec Requirements — functional bullet 1 (preservation); Evidence (rank_combinations cumulative); D2, D4; Acceptance Criteria 3.

---

### Step 3: Error paths converge to ConfigurationError with no write
**Type:** unit
**File:** `tests/simulation/win_rate/test_config_promoter.py`
**Invocation:** `python -m pytest tests/simulation/win_rate/test_config_promoter.py -k "empty_store or strategy_absent or filenotfound or config_missing" -vv`
**Pass criterion:** All selected tests pass (≥1 selected). Each raises `ConfigurationError` and leaves the target untouched: (a) **empty store** (`get_all_combinations` → `{}`) raises and the base config copy is unchanged; (b) **winning `strategy_id` absent** from the patched `load_valid_strategies` list (linear-search miss) raises and no write occurs; (c) `load_valid_strategies` patched to **raise `FileNotFoundError`** is caught and re-raised as `ConfigurationError`, no write; (d) **missing `config_path`** (point at a non-existent file) raises `ConfigurationError` (wrapping `FileNotFoundError`/`JSONDecodeError`) and creates no file. "No write" is asserted by comparing the config file's bytes before vs. after (cases a–c) or asserting the path still does not exist (case d).
**Expected test methods:** `test_empty_store_raises_no_write`, `test_strategy_absent_raises_no_write`, `test_load_strategies_filenotfound_raises_no_write`, `test_config_missing_raises_no_write`.
**Covers:** spec Requirements — functional bullets 2, 3; D2.

---

### Step 4: Git dirty-state warning, clean-state silence, graceful probe, and write-failure safety
**Type:** unit
**File:** `tests/simulation/win_rate/test_config_promoter.py`
**Invocation:** `python -m pytest tests/simulation/win_rate/test_config_promoter.py -k "dirty or clean or git_swallows or write_failure" -vv`
**Pass criterion:** All selected tests pass (≥1 selected). Covers: (a) with `_has_uncommitted_changes` patched `True`, a `WARNING` is logged (`caplog`) **and** the config is still written (warn-and-proceed, D1); (b) with it patched `False`, no warning is logged and the config is written; (c) `_has_uncommitted_changes` invoked with `subprocess.run` patched to raise (git missing / error) returns `False` and does not propagate — exercised by calling the helper directly; (d) with the atomic write forced to fail (patch `Path.replace` — or `json.dump` — to raise `OSError`), `promote_best_combination` raises `FileOperationError`, the original config copy is byte-unchanged, and **no orphaned `.tmp`** file remains beside `config_path`.
**Expected test methods:** `test_dirty_state_warns_and_writes`, `test_clean_state_no_warning`, `test_git_swallows_subprocess_failure`, `test_write_failure_wraps_and_cleans_tmp`.
**Covers:** spec Requirements — functional bullets 4, 5; non-functional bullet (git graceful + FileOperationError + tmp cleanup); D1, D5.

---

### Step 5: Full module file + regression gate
**Type:** unit
**File:** `tests/simulation/win_rate/test_config_promoter.py`
**Invocation:** `python -m pytest tests/simulation/win_rate/test_config_promoter.py -vv` then `python tests/run_all_tests.py`
**Pass criterion:** The module file passes in full (no test outside Steps 1–4 left unrun), and the full project suite reports a 100% pass rate (no regression introduced by the new module/import). Pre-existing working-tree deletions of `data/historical_data/2025/*` are unrelated and must not cause failures.
**Covers:** spec Verification bullets 1–2; CODING_STANDARDS 100%-pass commit gate.

---

## Shared Setup / Teardown

N/A — each step is self-contained. Per-test fixtures build a real `SweepResultsManager` on `tmp_path`, copy the real `data/configs/league_config.json` to a `tmp_path` target, and patch `load_valid_strategies` + `_has_uncommitted_changes` (or `subprocess.run`) inline. No services, DB, network, or env vars; the real `league_config.json` is read only as a source to copy, never written.

---

## Results Log

| Step | Status | Run at | Evidence | Notes |
|------|--------|--------|----------|-------|
| 1 | PASS | 2026-06-11 | `2 passed, 10 deselected` | promotes_winner / four_keys |
| 2 | PASS | 2026-06-11 | `2 passed, 10 deselected` | keys_preserved / cumulative |
| 3 | PASS | 2026-06-11 | `4 passed, 8 deselected` | empty_store / strategy_absent / filenotfound / config_missing |
| 4 | PASS | 2026-06-11 | `4 passed, 8 deselected` | dirty / clean / git_swallows / write_failure |
| 5 | PASS | 2026-06-11 | file `12 passed`; full suite `2841/2841 (100%)` | pre-existing working-tree deletions caused no failures |

**Status values:** `PENDING`, `PASS`, `FAIL`, `BLOCKED`. Phase 5 blocks until every step is `PASS` (the Phase-5 blocking rule — no exceptions or documented deferrals).

---

## Failure Diagnosis

[Populated only on failure.]

---

## Open Questions

*(None — test design follows the spec Test Strategy directly; every case maps to a spec Requirement / Design Decision.)*

---

## Validation

Validated via Pattern 1. Dimensions:

- **Step clarity** — each step has an exact `pytest -k` invocation, named expected methods, and a binary pass criterion.
- **Executability** — commands resolve in the project's pytest environment; the only state is `tmp_path` fixtures built per-test (Shared Setup = N/A); patched seams (`load_valid_strategies`, git probe) keep the run hermetic.
- **Verification completeness** — every spec Requirement maps to a step: functional 1 (apply + preserve) → Steps 1–2; functional 2–3 (error types, no write) → Step 3; functional 4 (git warning) → Step 4; functional 5 (clean-state/graceful/atomic/tmp-cleanup) → Step 4; functional 6 (exact-four-key return) → Step 1; spec Verification → Step 5. Cumulative-ranking (D2) and key-preservation get a dedicated method each in Step 2.

Exit: risk-triggered (live-config mutation) → primary clean round + 1 adversarial sub-agent confirmation.

---
Validated 2026-06-11 — 1 round, 1 adversarial sub-agent confirmed
