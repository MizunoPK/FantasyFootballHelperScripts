---
Last Updated: 2026-08-08
Update History:
  - 2026-08-08: Mode C refresh after framework import — replaced retired ticket-stage references (`/dt7-review`, `/dt8-polish`) with the current six-stage delivery ownership model and preserved the review-altitude distinction: `/du5-review` runs the full 16-category gate on each unit, `/dt5-review` runs the narrowed cross-unit missed-requirements + cleanup sweep (including Documentation Impact & Currency), and `/du6-polish` applies per-unit fixes
  - 2026-06-16: Initial creation (project initialization)
  - 2026-06-16: Populated all sections from repository research (slug: populate-shamt-project-docs)
  - 2026-06-21: Win-rate sweep convergence and flag updates (slug: sweep-driver-rewire)
  - 2026-07-15: Align to master template after framework import — corrected stale Shamt phase numbers (Review→Phase 7, Polish→Phase 8) in How to Update (slug: project-doc-master-alignment)
  - 2026-07-27: Mode C refresh after framework import — one structural fix: added the missing falsified-clause Update Trigger from the current coding-standards template. No body drift: the section set still matches the template, and the cited `reference/review_categories.md` (work-root-relative, i.e. `.shamt-core/reference/`) still exists and is still 16 categories
  - 2026-08-02: T88 test-subprocess-calls-lack-timeout-hang-guard — added the **Subprocess timeouts** convention to §"Test Runner and Test Conventions": every test shelling out to a project runner passes an explicit integer `timeout=` as the last kwarg, sized as a hang bound rather than a performance budget, with `TimeoutExpired` left to propagate (no handler). Codifies the shape 11 sites already used and 14 did not (slug: T88-test-subprocess-calls-lack-timeout-hang-guard)
  - 2026-08-05: Mode C refresh after the project's conversion to `flow_track: delivery` — re-pointed the frontmatter `How to Update` block and the Purpose's consumer list off the retired Engineer flow onto `/dt3-design` + `/du1-spec` (research) and the 16-category sweep run by `/du5-review` + `/dt7-review`. The `test-executor` persona reference is unchanged and still correct — personas are generated for every layout and survived the conversion. No convention content changed; the cited `reference/review_categories.md` still resolves and is still 16 categories
Update Triggers: |
  Update this document when:
  - A new coding pattern emerges that should be standard across the codebase
  - The team agrees on a new convention (naming, file layout, fixture pattern, etc.)
  - Linting or formatting rules change
  - A recurring code-review finding becomes a pattern worth codifying as a rule
  - Test conventions change (runner, file naming, assertion style, fixture model)
  - When adding an entry, re-read this document's own overview/status/summary prose and flag any clause the new entry falsifies; re-run until a clean pass.
How to Update: |
  Open a delivery ticket (or a framework-update proposal if this is a shamt-core change), follow the
  delivery track, and amend the relevant sections of this file. `/du5-review` (per unit) and
  `/dt5-review` (cross-unit) flag whether a change implies an update; `/du6-polish` applies
  per-unit documentation fixes and re-validates. `/update-project-doc` is the direct route for a doc-only edit.
  Run `/validate-artifact .shamt-core/project-specific-files/CODING_STANDARDS.md` after substantive edits.
  Keep `Last Updated` current and add an `Update History` entry with the triggering ticket/unit or
  proposal slug.
---

# Project Coding Standards

**Purpose:** Define project conventions for consistent code reviews and new code. This project runs the **delivery track** (`flow_track: delivery`), so it is consulted by `/dt3-design`'s ticket-scope research and each unit's `/du1-spec`, by the Naming / Documentation / Architecture categories in `/du5-review`'s per-unit 16-category sweep, and by `/dt5-review`'s narrowed cross-unit missed-requirements + cleanup sweep (including Documentation Impact & Currency; see `reference/review_categories.md`). The `test-executor` persona also consults it when writing or interpreting tests.

---

## Test Runner and Test Conventions

**Test runner:** `pytest` (>= 8), driven through the project script `tests/run_all_tests.py` (which shells out to pytest per file and enforces a 100% pass rate). `pytest-asyncio` is used for async tests; `psutil` for performance/memory tests.

**Run command:** `python tests/run_all_tests.py` (the canonical full-suite gate). Equivalent direct invocation: `.venv/bin/python -m pytest tests/ -m "not live_api"`.

**Test file naming:** `test_<module>.py` — e.g. source `league_helper/util/PlayerManager.py` → test `tests/league_helper/util/test_PlayerManager*.py`. A single source module may be split across several `test_<module>_<aspect>.py` files (e.g. `test_PlayerManager_scoring.py`).

**Test directory layout:** All tests live under `tests/`, mirroring the source tree (`tests/league_helper/util/`, `tests/simulation/`, `tests/player_data_fetcher/`, …). Additional buckets: `tests/integration/`, `tests/unit/`, `tests/root_scripts/`, and `tests/fixtures/` (committed offline fixtures). `tests/conftest.py` inserts the project root onto `sys.path` so tests import modules the same way the apps do (e.g. `from utils.FantasyPlayer import FantasyPlayer`).

**Assertion style:** Plain `assert` (pytest native). No assertion wrappers.

**Fixture / setup patterns:** `@pytest.fixture` functions, typically defined at the top of each test file under a `# FIXTURES` banner. Tests are grouped into `class Test<Subject>:` classes and follow the **Arrange-Act-Assert** structure (see the template in `tests/README.md`). Committed JSON/CSV fixtures for offline runs live under `tests/fixtures/` (`espn_api/`, `historical/`, `player_data/`, `league/`).

**Mocking conventions:** `unittest.mock` (`Mock`, `MagicMock`, `patch`) from the standard library. Mock external dependencies (network clients, filesystem where appropriate) to isolate the unit under test. For ESPN network behavior specifically, prefer the **record/replay fixture seam** (`ESPN_FIXTURE_DIR`) over ad-hoc HTTP mocks where an integration-level test is intended.

**Test markers:** Declared in `pytest.ini` — `live_api` (requires live ESPN access) and `offline` (runs fully offline). The default suite runs with `-m "not live_api"`, so **the full default test run never touches the network.** Mark any network-dependent test `@pytest.mark.live_api`.

**Subprocess timeouts:** Any test that shells out to a project runner (`subprocess.run([...])`) **must** pass an explicit integer `timeout=` as the **last keyword argument** — a bare literal, matching the established `timeout=60` / `timeout=120` sites under `tests/integration/` and `tests/simulation/`. No named constant, wrapper, or helper. The value is a **hang bound, not a performance budget**: size it well above the observed runtime (≈10× or more) so a loaded machine cannot flake the suite, and let `subprocess.TimeoutExpired` propagate — pytest reports it under the failing test's nodeid, naming both the command and the bound, so **no `try`/`except TimeoutExpired` wrapper is added**. `tests/run_all_tests.py` carries the same guard at the runner altitude (`timeout=300` per discovered file, `timeout=900` on the `--single` whole-suite path), which bounds a hang in a test that does *not* shell out.

**Test data:** Synthetic or committed-fixture data only — never live-fetched data baked into a test. Player/league fixtures are small hand-built JSON/CSV under `tests/fixtures/`.

**Coverage expectations:** The enforced gate is a **strict 100% pass rate** (`tests/run_all_tests.py` exits non-zero if any test fails). There is **no line-coverage tool or threshold** configured. New behavior should be accompanied by tests covering the happy path, edge cases (None, empty collections, boundary values), and error conditions, per the existing suite's style.

---

## Verification-Assertion Conventions

Conventions for the **verification steps in an implementation plan** — the checks a builder runs to
prove a step landed. Added 2026-08-05 from ticket D8's defect log
(`.shamt-core/tickets/D8-*/plan_defect_log.md`), where **seven** separate plan defects were checks
that *could not fail* or *always failed*. A check that cannot fail is worse than no check: it reports
green.

**The governing rule: an expected value is OBSERVED, never reasoned about.** Run the command, take
its output, put that in the plan. Every defect below came from predicting an output instead.

- **`grep -c` expecting `0` must carry `|| true`.** `grep` **exits 1** when it matches nothing, so a
  zero-expectation check fails the build on success.
- **`grep -c` counts LINES, not occurrences.** Two matches on one line count as `1`. Derive the number
  by running it.
- **Use `git diff HEAD`, not bare `git diff`,** in any check that may run after the build has staged
  files — a bare `git diff` goes empty (and therefore vacuously green) once anything is staged.
- **Anchored patterns must be tested against real indentation.** `grep '^foo'` finds nothing if the
  line is indented.
- **Heredocs sit at column 0, outside indented fences.** A `<<'PY'` inside an indented checklist item
  cannot be closed by its terminator.
- **Embedded file content needs a 4-backtick outer fence** when the content itself contains
   3-backtick blocks, or it truncates mid-file.
- **A before/after capture is a BUILDER step, not a verification step.** Verification runs post-build,
  where the "before" state no longer exists. Either persist the baseline during the build, or express
  the check post-hoc as an assertion about the exact expected end state.
- **Prefer an exact-set assertion over a diff against a captured baseline** where both are possible —
  it needs no state carried across the build and fails on both additions and removals.

## Measurement and Comparison Conventions

Ticket D8's record was corrected across **six** validation rounds, and **every** finding was a premise
or convention error — never arithmetic. One rule would have prevented all of them:

> **Every quantitative claim states the population it was measured over and the convention applied,
> and two numbers are compared only when those match.**

Concretely, from the defects that occurred:

- **State the population inline, not by context.** A figure quoted in a section whose population was
  named three paragraphs earlier will be copied elsewhere without it.
- **The population rule must be valid for every member being compared.** D8's headline claim was
  false because a top-N-*by-ADP* population is meaningless for a season whose ADP is on a different
  scale — the arithmetic was right and the selection was not.
- **Carry the convention with the number, every time.** Coverage figures differ by ~5 points between
  bye-included and bye-excluded; a threshold taken from one band and applied under the other is
  silently wrong.
- **Two numbers may only be compared when their denominators are the same kind of thing.** `85` of 798
  compiled players and `91` of 1,128 raw API rows are not comparable, and as a rate they invert.
- **Count records, not names,** unless deduplication is the intent — and say which. A name-keyed dict
  silently dropped two genuine duplicate-name players.
- **A claim of change over time needs two like-for-like measurements**, not one measurement plus an
  inference.

## Test Discrimination

- **A test claiming to cover a guard should be mutation-checked**: delete the guard and confirm the
  test fails. Two D8 tests asserting a zero-denominator guard passed with the guard removed — the
  surrounding arithmetic already produced the same answer, so the tests were tautologies.
- **Assert inside a measured corridor, never at its edge.** `< 0.16 + 1e-9` against an exact `0.16` is
  an equality in disguise; it passes for the wrong reason and fails on a trivial data shift.
- **If no in-domain input can distinguish a guard's presence, say so** and correct the documents that
  claim it is tested. Do not construct an out-of-domain input to manufacture a passing test.

## File Naming and Organization

File naming for modules is **mixed/transitional** — two conventions coexist, and a module's name does *not* reliably indicate whether it holds a class:

| Element | Convention | Example |
|---------|------------|---------|
| `PascalCase.py` module | Common for many core class modules — especially the older `*Manager`/model/data classes | `FantasyPlayer.py`, `PlayerManager.py`, `ConfigManager.py`, `LeagueHelperManager.py`, `ScheduleFetcher.py` |
| `snake_case.py` module | Used for utility/functional modules **and** for many (often newer) single-class modules | utility/functional: `error_handler.py`, `csv_utils.py`, `user_input.py`, `config_promoter.py`; single-class: `player_scoring.py` (`PlayerScoringCalculator`), `trade_analyzer.py` (`TradeAnalyzer`), `upcoming_game_model.py` (`UpcomingGame`) |
| Package directory | `snake_case/` | `league_helper/`, `player_data_fetcher/`, `simulation/win_rate/`, `add_to_roster_mode/` |
| Runner entry point (repo root) | `run_<thing>.py` (or `compile_*` / `validate_*`) | `run_league_helper.py`, `run_win_rate_simulation.py`, `compile_historical_data.py` |
| Test files | `test_<module>.py` (optionally `test_<module>_<aspect>.py`) | `test_PlayerManager_scoring.py` |

There is no enforced "PascalCase ⇔ class module" rule; newer code (e.g. `simulation/win_rate/`, `league_helper/trade_simulator_mode/`) trends toward `snake_case` even for single-class modules. **Guidance for new files:** match the prevailing style of the package and neighboring files you are editing. Do not rename existing files to chase consistency.

**File organization rules:**
- One primary class per module is the norm; group its tightly-coupled helpers in the same file.
- Group related functionality into packages with `__init__.py`; modes live under `league_helper/<mode>_mode/`, simulation engines under `simulation/<engine>/`.
- Keep cross-cutting helpers in `utils/` (logging, errors, CSV I/O, shared models) so any component can import them without coupling to a feature package.
- Entry points stay thin at the repo root and delegate into a package `main()` — see Common Patterns.

---

## Language Conventions

**Language(s):** Python 3.13+ (developed/tested on 3.13–3.14). Follow **PEP 8** as the baseline style.

### Naming

| Element | Convention | Example |
|---------|------------|---------|
| Variables | `snake_case` | `player_count`, `current_nfl_week` |
| Functions / methods | `snake_case` | `get_logger()`, `load_players()`, `_get_current_round()` |
| Internal / "private" helpers | leading underscore | `_parse_test_results()`, `_match_players_to_rounds()` |
| Classes / Types / dataclasses | `PascalCase` | `FantasyPlayer`, `ConfigManager`, `ErrorContext` |
| Constants | `UPPER_SNAKE_CASE` | `MAX_POSITIONS`, `FANTASY_TEAM_NAME`, `VALIDATION_WEEKS` |
| Config keys (in `league_config.json`) | `UPPER_SNAKE_CASE` for scoring params; nested objects for grouped settings | `MATCHUP_SCORING.IMPACT_SCALE`, `SAME_POS_BYE_WEIGHT` |
| Pydantic models | `PascalCase`, suffix by role where helpful | `PlayerDataModel`, game-data models in `*_models.py` |

### Function and Module Shape

- Single-purpose functions; extract a helper rather than growing a function past what reads clearly on one screen. Underscore-prefix helpers that are internal to a module/class.
- Modules group one class (or one cohesive set of functions) plus directly-supporting helpers; if a module accretes unrelated responsibilities, split it into the relevant package.
- Entry-point runners (`run_*.py`) parse args and call a package `main()`; they do not hold business logic.

### Imports

Group imports **stdlib → third-party → local**, in that order. Use absolute imports rooted at the package (e.g. `from utils.LoggingManager import get_logger`, `from simulation.win_rate.strategy_loader import load_valid_strategies`); tests rely on `conftest.py` having added the project root to `sys.path`.

```python
# Standard library
import argparse
import asyncio
from pathlib import Path
from typing import List, Optional

# Third-party
import httpx
import pandas as pd
from pydantic import BaseModel

# Local
from utils.LoggingManager import get_logger
from utils.FantasyPlayer import FantasyPlayer
```

---

## Lint and Format

**No automated linter or formatter is configured for this project.** There is no `pyproject.toml`, `ruff`, `black`, `flake8`, `mypy`, `.editorconfig`, or `.pre-commit-config.yaml` checked in.

- **Style:** follow **PEP 8** and match the surrounding file's existing style by hand (naming, import grouping, docstrings, type hints as described in this document).
- **The single enforced quality gate is the test suite** (`python tests/run_all_tests.py`, 100% pass), run via `run_pre_commit_validation.py` before committing.
- There is **no formatter to run before commit** — keep diffs clean and consistent with neighboring code manually.

(If lint/format tooling is adopted later, update this section and the relevant `Update Triggers`.)

---

## Documentation

### Code Comments

**When to comment:**
- Non-obvious WHY: a hidden constraint, a subtle scoring invariant, a workaround for a specific ESPN-API quirk, or surprising behavior.
- Complex algorithms (e.g. the positional-slot draft assignment, the scoring multiplier steps) where intent is not visible from the code alone.

**When not to comment:**
- Restating what the code does (`i += 1  # increment i`).
- Narrating the current change/task.

### Docstrings

**Required for:** public functions/methods, classes, and module-level entry points. Modules start with a module docstring (title + short description + `Author:` line, per the existing files).

**Format:** **Google-style** docstrings (`Args:` / `Returns:` / `Raises:`), with type hints on signatures. This is the dominant style across `utils/`, `league_helper/`, and the fetcher packages.

```python
def load_players(filepath: Path, position: Optional[str] = None) -> List[FantasyPlayer]:
    """Load players from a CSV file.

    Args:
        filepath: Path to the players CSV file.
        position: Optional position filter (QB, RB, WR, TE, K, DST).

    Returns:
        The loaded player objects.

    Raises:
        FileNotFoundError: If the CSV file does not exist.
    """
```

---

## Error Handling

The project centralizes error handling in `utils/error_handler.py`, which defines a custom exception hierarchy rooted at `FantasyFootballError` (subclasses include `ConfigurationError`, `FileOperationError`, etc.), an `ErrorContext` dataclass, retry/decorator helpers, and `contextmanager`-based context handling.

**Do:**
- Raise/catch the project's specific exception types (`FantasyFootballError` subclasses), not bare `Exception`, where a domain error is meaningful.
- Attach context (operation, component, IDs) via `ErrorContext` when raising, so logs are debuggable.
- Use the `utils/error_handler.py` helpers (context managers, retry decorators) rather than re-implementing try/except + backoff inline.
- Use context managers for resource cleanup (file handles, etc.).
- For transient network calls in the fetchers, use the established retry mechanism (`tenacity` / the error-handler retry helper) with exponential backoff.

**Don't:**
- Swallow exceptions silently.
- Use exceptions for normal control flow.
- Catch without logging or re-raising.

**Project specifics:**
- **Logging:** always go through `utils/LoggingManager.py` (`setup_logger(name, ...)` to configure, `get_logger()` to obtain the module logger). Use `DEBUG` for detail, `INFO` for progress/milestones, `WARNING`/`ERROR` for problems. Console-only by default; file logging is opt-in per script via `--enable-log-file` (logs rotate under `logs/<script>/`).
- **Log/error message wording:** include the actual function/operation name and relevant IDs/values so a message is traceable to its source.
- **No sensitive data** in logs (the data is public, but keep messages free of noise/secrets regardless).

---

## Security Defaults

Scope note: this is a local, single-user toolkit with no server, auth, tenancy, or database (see `ARCHITECTURE.md` → Security Posture). The applicable defaults are:

- **No secrets in the repo.** The external APIs (ESPN, Open-Meteo) are public and unauthenticated; do not introduce committed keys/tokens. If a credentialed source is ever added, route it through env/`.env` (`python-dotenv`), never a literal.
- **Validate external input at the boundary** with `pydantic` models before trusting fetched/scraped API payloads. Internal, already-validated values do not need re-validation.
- **No regulated or personal data** belongs in logs, exports, fixtures, or commit history. The data is public NFL stats plus the user's own league rosters.
- **Respect the file-writer boundaries** in `ARCHITECTURE.md` → Data Stores: only `--promote` paths and Modify-Player-Data mode write the live config/player files. Do not add incidental writers to those files.
- **SQL/HTML injection do not apply** (no database, no rendered HTML surface). The relevant injection-analogue is malformed API payloads — hence the pydantic validation rule above.

---

## Performance Defaults

- **Parallelize the heavy simulation workloads** via the existing runner abstractions (`ParallelLeagueRunner`, `ParallelAccuracyRunner`) and the `--workers` / `--max-workers` flags; prefer processes (`ProcessPoolExecutor`) for CPU-bound replay to bypass the GIL, as the accuracy engine does by default.
- **Load files once, operate in memory.** The player pool and historical corpus are small; avoid re-reading the same CSV/JSON repeatedly inside a loop.
- **Use `pandas` vectorized operations** for bulk CSV processing rather than per-row Python loops where it is hotter code.
- **Use async + `tenacity` retries** for the fetcher network paths; batch/limit ESPN requests rather than issuing one synchronous call per player in a tight loop.
- **Mind `--sims`** in simulations: it is the dominant cost knob and trades statistical stability against wall time. The win-rate sweep runs to convergence; `--sims` sets the sample size per evaluation and `--num-values` controls the grid density per draft-side parameter.
- N+1 query / DB-index guidance does not apply (no database).

---

## Common Code Patterns

### Pattern 1: Thin runner → package `main()`

**When to use:** Every executable script at the repo root.

**Example:**
```python
# run_league_helper.py
from league_helper.LeagueHelperManager import main

if __name__ == "__main__":
    main()
```
The runner only parses args (when it has any) and delegates; business logic lives in the package. Scripts must be run **from the project root** so relative data paths and imports resolve.

### Pattern 2: Module logger via LoggingManager

**When to use:** Any module that logs.

**Example:**
```python
from utils.LoggingManager import get_logger

logger = get_logger()

def do_work():
    logger.info("Starting work")
    logger.debug("Detail: %s", value)
```
Entry points call `setup_logger(name, log_level=..., enable_log_file=...)` once at startup; everything else uses `get_logger()`.

### Pattern 3: Config-driven scoring via ConfigManager

**When to use:** Anything that needs league/scoring parameters.

**Example:**
```python
from pathlib import Path
from league_helper.util.ConfigManager import ConfigManager

config = ConfigManager(Path("data"))        # loads data/configs/league_config.json + active week override
scale = config.matchup_scoring["IMPACT_SCALE"]   # grouped params exposed as lowercased attributes
min_weeks = config.get_parameter("TEAM_QUALITY_MIN_WEEKS", default=4)  # generic accessor w/ default
```
Never hard-code scoring constants — read them from `ConfigManager` (grouped-param attributes, the typed `get_*` accessors, or `get_parameter`) so simulation-tuned values flow through (`--promote`).

---

## Review Quick Checklist

When reviewing code in this project, check for:

- [ ] Follows naming conventions (snake_case identifiers; file name matches the package's prevailing PascalCase-or-snake_case style)
- [ ] Has Google-style docstrings + type hints on public functions/classes
- [ ] Tests added/updated under the mirrored `tests/` path; full suite still 100% passing; network tests marked `live_api`
- [ ] Error handling uses `utils/error_handler.py` patterns and the `FantasyFootballError` hierarchy
- [ ] Logging goes through `utils/LoggingManager.py` (correct level; no sensitive/noisy output)
- [ ] Scoring/league values read from `ConfigManager`, not hard-coded
- [ ] Respects file-writer boundaries (no new incidental writers to live config/player files)
- [ ] No new committed secrets; external payloads validated with pydantic at the boundary
- [ ] Consistent with PEP 8 and surrounding style (no formatter to fall back on)

The full 16-category review framework lives in `reference/review_categories.md`. This checklist is the project-specific fast pass.

---

*Template for project `.shamt-core/project-specific-files/CODING_STANDARDS.md` in Shamt. Header metadata block above is required — the framework-update audit reads it.*

---
Validated 2026-08-08 — 1 rounds, 1 adversarial sub-agent confirmed (sha256:6770720f381cd545) (Mode C refresh: current delivery review ownership)
