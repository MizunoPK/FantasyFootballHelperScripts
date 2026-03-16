# Integration Test Script Pattern

**Purpose:** Conventions for automated E2E integration test scripts used when epic Testing Approach is B or D
**Applies To:** Options B (integration scripts only) and D (both unit tests and integration scripts)
**Last Updated:** 2026-03-12

---

## Overview

Integration test scripts are runnable artifacts that validate a feature end-to-end against real or real-like data. They are the primary testing mechanism for Options B and D epics, replacing the manual smoke testing process from S7.P1 Part 3.

**Key principle:** The script is the contract. Pass = exit code 0, fail = non-zero exit code. Downstream gates (S7, S9, S10) check exit code only — no custom output parsing.

---

## When to Create

- **S6, Phase 1 only:** Create the integration test script skeleton at the end of Phase 1 (Step 3.5)
- **S8.P2:** Add/update assertions based on discoveries during implementation
- One script per feature; all scripts must be runnable independently and collectively

---

## Discovery: Integration Test Convention

Before creating any script, discover (or confirm) the project's test conventions. This is done once per epic and recorded in EPIC_README under `Integration Test Convention:`.

**Discovery order:**

**Step 0: Check EPIC_README first.** If `Integration Test Convention:` is already populated (set by a prior feature in this epic), use it. Do not re-run discovery.

**Step 1: Existing integration tests.** Search the codebase for integration test files:
```bash
find . -name "*integration*" -o -name "*e2e*" -o -name "*smoke*" | grep -v __pycache__
```
If found, examine:
- Language and framework used
- Directory structure
- File naming convention
- Assertion style
- How they are invoked

New scripts must follow this pattern exactly.

**Step 2: Existing tests of any kind.** If no integration tests exist, check for unit tests or other tests to determine the project's language and framework. Follow the same language/framework; the structure can be adapted for integration scope.

**Step 3: No tests exist.** Ask the user:
> "Where should integration tests live in this project, and which language/framework should they use?"

Record the answer in EPIC_README under `Integration Test Convention:` before creating any test files.

**The `Integration Test Convention:` field records:**
- Language and framework (e.g., `Python/pytest`, `Python/stdlib unittest`, `bash/bats`)
- Directory location (e.g., `tests/integration/`, `test/`, `epics/{epic}/integration_tests/`)
- File naming convention (e.g., `test_{feature}_integration.py`, `{feature}_e2e_test.py`)
- How to run all scripts (e.g., `pytest tests/integration/`, `bash run_tests.sh`)

---

## Required Coverage

Regardless of framework, every integration test script must cover these four areas:

1. **Feature execution** — invoke the feature's entry point end-to-end (no mocking)
2. **Output structure** — verify expected output files exist and have required fields
3. **Output values** — verify data values are correct, non-empty, and non-uniform
4. **Integration points** — verify cross-feature data dependencies are satisfied

---

## Structure (Python/pytest example)

This is an illustrative example only. Follow the project's actual framework and conventions.

```python
# Integration test: {feature_name}
# Location: {from EPIC_README Integration Test Convention}
# Run: {from EPIC_README Integration Test Convention}

def test_feature_execution():
    """Feature runs end-to-end without error."""
    # Invoke entry point; assert exit code 0 or no exception

def test_output_structure():
    """Output files exist and have required fields."""
    # Assert expected output files exist
    # Assert required columns/keys present

def test_output_values():
    """Output data values are correct (not placeholders, not uniform)."""
    # Assert values in expected ranges
    # Assert non-uniform distribution (algorithm ran, not default-filled)

def test_integration_points():
    """Cross-feature integration points are satisfied."""
    # Assert downstream data structures updated correctly
```

---

## Key Conventions

**1. Exit code is the contract.**
Pass = exit code 0, fail = non-zero. Scripts are invoked by S7, S9, and S10 gates by checking exit code. No custom output parsing is needed.

**2. Use real or real-like data, never mocks.**
Scripts must run against the project's actual data directory or a representative subset. If the data is too large for CI, use a subset that still exercises the full code path.

**3. Assert values, not existence.**
File presence alone is not sufficient. Assert that values are in expected ranges, are not placeholders (e.g., not all 0.0 or "N/A"), and show variance across records.

**4. Scripts are additive, not replaced.**
When S8.P2 discovers new integration points or behavior changes, assertions are added to the existing script. The script grows as the feature matures; it is not replaced each iteration.

**5. Language and framework follow the project.**
Use whatever the project already uses. If the project has no tests at all, use the same language as the main codebase unless the user specifies otherwise.

**6. Location and naming follow the project.**
Use the `Integration Test Convention:` field recorded in EPIC_README. One script per feature; all scripts runnable independently and runnable together for epic-level validation (S9).

---

## Skeleton Creation (S6 Phase 1 — Step 3.5)

At the end of S6 Phase 1, create the integration test script skeleton:

1. Read `Integration Test Convention:` from EPIC_README
2. Create the script file in the correct location with the correct naming
3. Scaffold the four required test functions with placeholder assertions (all initially failing)
4. Add the assertion list drafted in S5 Step 0 as comments or TODO markers
5. Commit the skeleton alongside Phase 1 implementation code

**The skeleton will have failing assertions at creation — this is intentional.** Fill in real assertions as implementation progresses through phases.

---

## Running Scripts

### Single script
```bash
# pytest
pytest tests/integration/test_{feature}_integration.py -v

# Python stdlib
python tests/integration/test_{feature}_integration.py

# bash
bash integration_tests/{feature}_e2e_test.sh
```

### All scripts (S9/S10)

Use the invocation method that matches the project's framework from `Integration Test Convention:`:

```bash
# pytest (all integration tests)
pytest tests/integration/ -v

# bash scripts (fail fast)
for script in integration_tests/*.sh; do
    bash "$script" || exit 1
done

# Python stdlib (fail fast)
for script in integration_tests/test_*_e2e.py; do
    python "$script" || exit 1
done
```

The S9 and S10 guides reference the specific command recorded in `Integration Test Convention:` in EPIC_README — not a generic example from this file.

---

## Anti-Patterns

**❌ Mocking external dependencies**
Integration scripts should exercise the full stack. Mocking defeats the purpose.

**❌ Testing only file existence**
`assert os.path.exists(output_file)` is insufficient. Assert values inside the file.

**❌ Uniform value assertions**
`assert len(results) > 0` does not catch a bug that fills all results with the same default value. Assert variance: `assert len(set(results)) > 1`.

**❌ Creating a new script for each S8.P2 update**
Add assertions to the existing script. One script per feature.

**❌ Hardcoding paths that differ across environments**
Use relative paths or project config conventions. Scripts should run on any machine with the project set up.

---

## Related Guides

- `stages/s5/s5_v2_validation_loop.md` — Step 0: Test Scope Decision, drafts initial assertion list
- `stages/s6/s6_execution.md` — Step 3.5: Create integration script skeleton (Options B/D, Phase 1 only)
- `stages/s7/s7_p1_smoke_testing.md` — Part 3: Run integration script instead of manual process (Options B/D)
- `stages/s8/s8_p2_epic_testing_update.md` — Step 3b: Maintain/update integration script
- `stages/s9/s9_p1_epic_smoke_testing.md` — Part 4: Run all integration scripts at epic level (Options B/D)
- `stages/s10/s10_epic_cleanup.md` — Step 2c / Gate 7.1b: Run all integration scripts before commit

---

*End of integration_test_script_pattern.md*
