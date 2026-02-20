## Discovery Phase: game_data_fetcher_cli

**Epic:** KAI-11-game_data_fetcher_cli
**Created:** 2026-02-19
**Last Updated:** 2026-02-19
**Status:** COMPLETE

---

## Epic Request Summary

Refactor `run_game_data_fetcher.py` to add universal CLI args (`--e2e-test`, `--log-level`) and
script-specific args (`--request-timeout`, `--historical-season`), remove the `os.chdir()`
anti-pattern and `config` imports, wire log-level to `setup_logger()`, and implement E2E test mode
(Week 1 only, ≤180s, writes to /tmp). This was Feature 03 in KAI-10 — its S2 spec is fully
complete with all design decisions resolved.

**Original Request:** `feature-updates/requests/cli-enhancements/game_data_fetcher_cli_notes.txt`

---

## Discovery Questions

### Resolved Questions

All design decisions were resolved in KAI-10 S2. No new questions arose during Discovery.

| # | Question | Answer | Impact | Resolved |
|---|----------|--------|--------|----------|
| 1 | Should `--request-timeout` or `--rate-limit-delay` be exposed? | `--request-timeout` only; `rate_limit_delay` is imported but unused in code | REQ-10 adds only `--request-timeout` | 2026-02-18 (KAI-10) |
| 2 | Should `--data-folder`, `--validate`, `--clean` be in scope? | No — follow DISCOVERY scope strictly | Not in spec | 2026-02-18 (KAI-10) |
| 3 | Which week for E2E test? | Week 1 — deterministic, reliable historical data | E2E mode fetches `weeks=[1]` | 2026-02-18 (KAI-10) |
| 4 | Should a `--debug` flag be added? | No — `--e2e-test --log-level DEBUG` serves that purpose | No `--debug` arg | 2026-02-18 (KAI-10) |
| 5 | How to detect historical season after config removal? | Add `--historical-season` flag explicitly | REQ-09 adds `--historical-season` | 2026-02-18 (KAI-10) |

### Pending Questions

None. Discovery is complete.

---

## Research Findings

### Iteration 1 (2026-02-19) — Core code review

**Researched:** `run_game_data_fetcher.py` and `player-data-fetcher/game_data_fetcher.py`

**Files Examined:**
- `run_game_data_fetcher.py` (lines 1-174): Current runner state
- `player-data-fetcher/game_data_fetcher.py` (lines 49-80, 519-560): Module state post-KAI-10

**Key Findings:**
- Runner has 4 existing args: `--season` (default None), `--output` (default None), `--weeks`, `--current-week` (default None)
- `os.chdir(fetcher_dir)` called before imports (line 97); `os.chdir(original_cwd)` in finally block (line 169) — anti-pattern confirmed
- `from config import NFL_SEASON, CURRENT_NFL_WEEK` inside try block (line 105) — config import confirmed
- Config fallbacks in place: `season = args.season if args.season else NFL_SEASON` (line 112)
- Historical detection: `if args.season and args.season < NFL_SEASON` (line 116) — implicit year comparison
- `setup_logger("game_data_fetcher", "INFO", ...)` — hardcoded "INFO" (line 109)
- `fetch_game_data()` call does NOT pass `request_timeout` currently (line 143-148)
- `game_data_fetcher.py` `__init__` already accepts `request_timeout: int = 30, rate_limit_delay: float = 0.2` (KAI-10 REQ-09 ✅)
- `fetch_game_data()` function accepts `request_timeout: int = 30` (KAI-10 REQ-09 ✅)

**Questions Identified:** None — all confirmed exactly as KAI-10 spec describes.

---

### Iteration 2 (2026-02-19) — Test file review

**Researched:** Existing test structure for runner scripts

**Files Examined:**
- `tests/root_scripts/test_root_scripts.py` (full file): Root script tests
- `tests/root_scripts/` directory listing: What files exist

**Key Findings:**
- No `test_run_game_data_fetcher.py` exists — must be created from scratch
- `test_root_scripts.py` has no `TestRunGameDataFetcher` class
- Pattern from `TestRunPlayerFetcher` (lines 95-113): Tests check for `parse_args`, `create_settings_dict`, and absence of `subprocess` — structural tests, not execution tests
- The KAI-10 Feature 01 runner refactoring used a dedicated test file: `tests/root_scripts/test_run_player_fetcher.py` — same approach expected here
- `TestRootScriptsIntegration.test_all_scripts_import_required_modules` checks `run_player_fetcher.py` for `subprocess, sys, Path, os` — `run_game_data_fetcher.py` is NOT in that check list (not checked automatically)

**Questions Identified:** None.

---

### Iteration 3 (2026-02-19) — KAI-10 spec validation — FINAL

**Researched:** Verified KAI-10 Feature 03 spec against current code state

**Files Examined:**
- `feature-updates/done/KAI-10-.../feature_03_game_data_fetcher_cli/spec.md`: Approved spec (Gate 3, 2026-02-18)
- Cross-checked each REQ against observed code state

**Key Findings:**
- REQ-01 (add `--e2e-test`, `--log-level`): Not yet implemented ✅ needs work
- REQ-02 (hardcoded defaults for `--season`=2025, `--current-week`=17): Not yet implemented ✅ needs work
- REQ-03 (remove config import): Not yet implemented ✅ needs work
- REQ-04 (remove os.chdir): Not yet implemented ✅ needs work
- REQ-05 (wire --log-level to setup_logger): Not yet implemented ✅ needs work
- REQ-06 (E2E mode: weeks=[1], output=/tmp/game_data_e2e_test.csv): Not yet implemented ✅ needs work
- REQ-07 (--log-level behavior: choices, case-sensitive): Not yet implemented ✅ needs work
- REQ-08 (backward compatibility): Verified — no-args behavior stays identical after refactor
- REQ-09 (--historical-season flag): Not yet implemented ✅ needs work
- REQ-10 (--request-timeout): Not yet implemented ✅ needs work; `fetch_game_data()` already accepts it ✅
- All design decisions from KAI-10 S2 are directly applicable — no drift detected

**Questions Identified:** None. Three consecutive clean iterations. Discovery Loop complete.

---

## Solution Options

Only one viable option — identical to KAI-10 Feature 01 pattern:

### Option A: KAI-10 Player Fetcher Pattern (argparse + sys.path only)

**Description:**
Add argparse args, replace config fallbacks with hardcoded defaults, remove `os.chdir`,
remove config import, wire `--log-level` to `setup_logger()`, implement E2E mode inline.

**Pros:**
- Identical pattern to KAI-10 Feature 01 (already established precedent)
- All design decisions pre-resolved in KAI-10 S2
- Minimal scope — 2 files total

**Cons:**
- None for this scope

**Effort Estimate:** LOW

**Fit Assessment:** GOOD — directly specified in approved KAI-10 S2 spec

### Option Comparison Summary

| Option | Effort | Fit | Recommended |
|--------|--------|-----|-------------|
| Option A: KAI-10 Pattern | LOW | GOOD | YES |

---

## Recommended Approach

**Recommendation:** Option A — KAI-10 Player Fetcher Pattern

**Rationale:**
- KAI-10 Feature 01 established exact design precedents for this class of refactoring
- All 10 requirements in the KAI-10 spec are directly applicable
- E2E output path `/tmp/game_data_e2e_test.csv` already decided
- `fetch_game_data()` already accepts `request_timeout` — runner just needs to pass it

**Key Design Decisions:**
- No `--debug` flag: `--e2e-test --log-level DEBUG` serves that purpose
- E2E output: `/tmp/game_data_e2e_test.csv` (avoids contaminating `data/game_data.csv`)
- `--historical-season` flag: explicit replacement for implicit year-comparison logic
- `--rate-limit-delay`: NOT added (imported but unused in game_data_fetcher.py)
- Argparse defaults are the single source of truth (`--season` → 2025, `--current-week` → 17)

---

## Scope Definition

### In Scope

- Add `--e2e-test` flag (weeks=[1], output=/tmp/game_data_e2e_test.csv, ≤180s)
- Add `--log-level` str arg (choices: DEBUG/INFO/WARNING/ERROR/CRITICAL, default INFO)
- Add `--request-timeout` int arg (default 30)
- Add `--historical-season` flag (sets current_week=18)
- Remove `os.chdir(fetcher_dir)` and `os.chdir(original_cwd)` — keep sys.path only
- Remove `from config import NFL_SEASON, CURRENT_NFL_WEEK`
- Fix `--season` default: None → 2025
- Fix `--current-week` default: None → 17
- Wire `--log-level` to `setup_logger()`
- Pass `request_timeout` to `fetch_game_data()`
- Remove implicit year-comparison historical detection
- Create `tests/root_scripts/test_run_game_data_fetcher.py` (new file)

### Out of Scope

- `--data-folder` — not in original design
- `--validate` — not in original design
- `--clean` — not in original design
- `--rate-limit-delay` — unused in game_data_fetcher.py code
- `--debug` — no debug flag in this epic; `--e2e-test --log-level DEBUG` serves that purpose
- Documentation updates (README.md, ARCHITECTURE.md) — handled in S7.P3

### Deferred (Future Work)

- Integration test framework — separate epic (integration_test_framework_notes.txt)

---

## Proposed Feature Breakdown

**Total Features:** 1
**Implementation Order:** Sequential (only 1 feature)

### Feature 1: game_data_fetcher_cli

**Purpose:** Refactor `run_game_data_fetcher.py` to add 4 CLI args, remove 2 anti-patterns, wire
log-level, implement E2E mode, and create the test file.

**Scope:**
- Modify `run_game_data_fetcher.py`: add 4 args, remove os.chdir, remove config import, fix defaults, wire log-level, implement E2E mode
- Create `tests/root_scripts/test_run_game_data_fetcher.py`: tests for all new CLI args

**Dependencies:** None (KAI-10 already modified `game_data_fetcher.py`)

**Discovery Basis:**
- Based on: KAI-10 Feature 03 approved spec (Gate 3, 2026-02-18)
- All 10 requirements confirmed applicable from code inspection

**Estimated Size:** SMALL (2 files, well-defined requirements)

---

## Feature Dependency Diagram

```
feature_01_game_data_fetcher_cli  (no dependencies)
```

---

## Discovery Log

| Timestamp | Activity | Outcome |
|-----------|----------|---------|
| 2026-02-19 | Initialized Discovery | Created DISCOVERY.md |
| 2026-02-19 | Iteration 1: Read run_game_data_fetcher.py + game_data_fetcher.py | Confirmed all anti-patterns; KAI-10 REQ-09 applied; 0 new questions |
| 2026-02-19 | Iteration 2: Read test_root_scripts.py | No existing test file; 0 new questions |
| 2026-02-19 | Iteration 3: KAI-10 spec validation | All 10 REQs confirmed applicable; 0 new questions |
| 2026-02-19 | Synthesis complete | Option A recommended; 1 feature |
| 2026-02-19 | Presenting to user | Awaiting approval |

---

## User Approval

**Discovery Approved:** YES
**Approved Date:** 2026-02-19
**Approved By:** User

**Approval Notes:** Approved in full — Discovery findings, recommended approach, scope, and 1-feature breakdown all approved.

---

## Post-Discovery Updates

No post-Discovery updates.
