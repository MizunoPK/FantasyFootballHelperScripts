# Feature 09: documentation

**Created:** 2026-01-30
**Epic:** KAI-7 improve_configurability_of_scripts
**Dependency Group:** Group 3 (depends on Groups 1 & 2 complete specs)
**Last Updated:** 2026-01-31

---

## Discovery Context

**Discovery Document:** `../DISCOVERY.md`

### This Feature's Scope (from Discovery)

**Purpose:** Update project documentation to reflect all new CLI arguments, E2E test modes, debug modes, and integration test framework across all 7 runner scripts.

**From DISCOVERY.md (lines 411-430):**
- Update README.md (Quick Start, Testing sections)
- Update ARCHITECTURE.md (Testing Architecture)
- Create docs/testing/INTEGRATION_TESTING_GUIDE.md
- Document all new arguments with examples
- Update epic workflow guides (reference integration tests in S7/S9)
- Add troubleshooting guide

### Relevant Discovery Decisions

**Comprehensive Script-Specific Argparse (Option 2 selected):**
- Each script has unique arguments from constants.py/config.py
- Universal flags: --debug, --e2e-test on all 7 scripts
- Documentation must clearly differentiate universal vs script-specific args

**E2E Behavior Varies by Script Type:**
- Simulations: Single run, 0-1 random configs, ≤3 min
- Fetchers: Real APIs with data limiting, ≤3 min
- League helper: Automated flows for all 5 modes, ≤3 min total
- Documentation must explain each script type's E2E behavior

**Debug Mode = Logging + Behavioral Changes:**
- Must document BOTH aspects (not just logging)
- Behavioral changes: fewer iterations, smaller datasets, verbose output
- Integration with --log-level precedence rules

### Relevant User Answers (from Discovery)

**User Answer Q1:** Script-specific args focusing on constants.py settings
→ Documentation must list all constants-derived arguments per script

**User Answer Q3:** E2E modes use real APIs with data limiting (not mocks)
→ Documentation must explain data limiting approach, not mock setup

**User Answer Q4:** Debug = behavioral changes + DEBUG logs
→ Documentation must clarify both logging AND behavior modifications

**User Answer Q5:** Integration tests validate exit code AND specific outcomes
→ Documentation must explain validation logic (log counts, file existence, etc.)

---

## Components Affected

### Files to Modify (3 existing files)

**1. README.md**
- **File Path:** C:/Users/kmgam/code/FantasyFootballHelperScripts/README.md
- **Current State:** 683 lines, has Quick Start (lines 68+) and Testing (lines 494-536) sections
- **Changes Required:**
  - Enhance Quick Start section with CLI argument examples for all 7 scripts
  - Add integration testing subsection to Testing section
  - Document universal vs script-specific arguments
  - Add troubleshooting guide section
- **Source:** Epic request (DISCOVERY.md line 421) + Research finding (README has no arg docs)
- **Traceability:** User explicitly requested README updates in epic notes

**2. ARCHITECTURE.md**
- **File Path:** C:/Users/kmgam/code/FantasyFootballHelperScripts/ARCHITECTURE.md
- **Current State:** Has Testing Architecture section (lines 1158+)
- **Changes Required:**
  - Enhance Testing Architecture with integration test framework overview
  - Document 7 individual test runners + master runner
  - Add integration test validation patterns section
  - Explain CLI test execution with subprocess patterns
- **Source:** Epic request (DISCOVERY.md line 422) + Research finding (no Feature 08 integration test docs)
- **Traceability:** User requested ARCHITECTURE.md updates for testing framework

**3. feature-updates/guides_v2/stages/s7/s7_p1_smoke_testing.md and s9_p1_epic_smoke_testing.md**
- **File Paths:**
  - C:/Users/kmgam/code/FantasyFootballHelperScripts/feature-updates/guides_v2/stages/s7/s7_p1_smoke_testing.md
  - C:/Users/kmgam/code/FantasyFootballHelperScripts/feature-updates/guides_v2/stages/s9/s9_p1_epic_smoke_testing.md
- **Current State:** S7 and S9 guides mention smoke testing but don't reference integration test framework
- **Changes Required:**
  - Add step to run integration test runners during S7 smoke testing
  - Reference master runner in S9 epic-level smoke testing
  - Provide integration test execution examples
- **Source:** Epic request (DISCOVERY.md line 424 "update epic workflow guides")
- **Traceability:** User specified "ensure integration test runners are used" in S7/S9

### Files to Create (1 new file)

**1. docs/testing/INTEGRATION_TESTING_GUIDE.md**
- **File Path:** C:/Users/kmgam/code/FantasyFootballHelperScripts/docs/testing/INTEGRATION_TESTING_GUIDE.md
- **Parent Directory:** docs/testing/ (does NOT exist, needs creation)
- **Purpose:** Comprehensive guide for running and interpreting integration tests
- **Content Structure:**
  - Overview of integration test framework
  - How to run individual test runners (7 scripts)
  - How to run master test runner
  - How to interpret validation results (exit codes + outcome checks)
  - Troubleshooting common issues
  - Adding new integration tests
- **Source:** Epic request (DISCOVERY.md line 423)
- **Traceability:** User explicitly requested integration testing guide
- **Size Estimate:** ~200-300 lines

---

## Requirements

### R1: Update README.md Quick Start Section

**Source:** Epic Request (DISCOVERY.md line 421) + User Answer Q1

**Description:** Enhance Quick Start section to document CLI arguments for all 7 runner scripts.

**Detailed Implementation:**

1. **For EACH of the 7 scripts, add argument documentation:**
   - Script name and purpose
   - Universal arguments (--debug, --e2e-test, --log-level)
   - Script-specific arguments (from Features 01-07 specs)
   - Usage examples (normal mode, debug mode, E2E mode)
   - Expected outputs

2. **Organize by script category:**
   - **Data Fetchers** (Features 01-02, 03-04): player, schedule, game_data, historical
   - **Simulations** (Features 05-06): win_rate, accuracy
   - **League Helper** (Feature 07): mode selection, E2E flows

3. **Document argument sources:**
   - Universal arguments: --debug, --e2e-test (all scripts)
   - Script-specific from constants.py/config.py (cite feature specs)

4. **Include 3 examples per script:**
   - **Normal mode:** Basic usage with most common arguments
   - **Debug mode:** --debug flag with behavioral changes explained
   - **E2E test mode:** --e2e-test flag with ≤3 min execution

**Traceability:**
- Epic requested "update README.md... document all new arguments" (DISCOVERY.md line 421)
- User Answer Q1: Script-specific args from constants.py (must document all discovered args)
- User Answer Q3: E2E behavior varies by type (must document differences)
- User Answer Q4: Debug = logging + behavioral (must clarify both)

**Content Sources:**
- Feature 01 spec.md: player_fetcher arguments (11 script-specific + 3 universal)
- Feature 02 spec.md: schedule_fetcher arguments (5 total)
- Feature 03 spec.md: game_data_fetcher arguments (8 total)
- Feature 04 spec.md: historical_compiler arguments (9 total)
- Feature 05 spec.md: win_rate_simulation arguments (10+ existing + E2E flag)
- Feature 06 spec.md: accuracy_simulation arguments (8+ existing + E2E flag)
- Feature 07 spec.md: league_helper arguments (9 total including mode selection)

**Implementation Steps:**
1. Read all 7 feature specs to extract argument lists
2. Group arguments: universal (3) vs script-specific (varies)
3. Write Quick Start subsection for each script
4. Add examples with expected outputs
5. Cross-reference with Features 01-07 specs for accuracy

**Acceptance Criteria:**
- All 60+ arguments documented with descriptions
- 3 examples per script (normal, debug, E2E)
- Universal vs script-specific clearly differentiated
- Examples show realistic usage patterns

---

### R2: Update README.md Testing Section

**Source:** Epic Request (DISCOVERY.md line 421) + Derived Requirement

**Description:** Add integration testing subsection to Testing section (lines 494-536) documenting integration test framework from Feature 08.

**Detailed Implementation:**

1. **Add "Integration Testing" subsection** after existing "Unit Testing" subsection:
   - Overview of integration test framework (7 individual + 1 master runner)
   - Purpose: Validate CLI arguments work correctly with subprocess execution
   - Validation approach: Exit codes + specific outcome checks

2. **Document how to run integration tests:**
   - Individual test runners: `pytest tests/integration/test_<feature>_cli.py`
   - Master runner: `python tests/integration/run_all_integration_tests.py`
   - Expected output: Pass/fail status per test, summary at end

3. **Explain validation logic** (per User Answer Q5):
   - Exit code validation (0 = success, non-zero = failure)
   - Specific outcome validation (log patterns, file existence, data formats)
   - Timeout checks (E2E mode must complete ≤180 seconds)

**Traceability:**
- Epic requested "update README.md... Testing sections" (DISCOVERY.md line 421)
- User Answer Q5: Tests check exit code AND outcomes (must explain validation)
- Derived: Testing section must include integration tests (logically necessary for completeness)

**Content Sources:**
- Feature 08 spec.md: Integration test framework structure, 7 runners + master
- Feature 08 spec.md R5: Per-file summary output with pass/fail counts

**Implementation Steps:**
1. Read Feature 08 spec.md to extract integration test details
2. Write Integration Testing subsection (~50-80 lines)
3. Include code examples for running tests
4. Document expected outputs and validation logic

**Acceptance Criteria:**
- Integration Testing subsection added to README.md Testing section
- Master runner execution documented with example
- Validation logic explained (exit code + outcome checks)
- Cross-references Feature 08 implementation

---

### R3: Update ARCHITECTURE.md Testing Architecture Section

**Source:** Epic Request (DISCOVERY.md line 422)

**Description:** Enhance Testing Architecture section (lines 1158+) to document integration test framework from Feature 08.

**Detailed Implementation:**

1. **Add "Integration Test Framework" subsection:**
   - Overview: 7 individual CLI test runners + 1 master runner
   - Purpose: E2E validation of CLI argument handling via subprocess
   - Structure: tests/integration/ directory with test_<feature>_cli.py files

2. **Document test runner architecture:**
   - Individual runners: Test single script with multiple argument combinations
   - Master runner: Orchestrates all 7 runners, reports aggregate results
   - Validation patterns: subprocess.run() execution + outcome verification

3. **Explain CLI testing approach:**
   - Use subprocess.run() to execute scripts as user would
   - Validate exit codes (0 = success)
   - Validate specific outcomes (log counts, file existence, data formats)
   - Use --e2e-test flag to limit execution time (≤3 min)

4. **Add directory tree diagram** showing tests/integration/ structure:
   ```
   tests/integration/
   ├── test_player_fetcher_cli.py
   ├── test_schedule_fetcher_cli.py
   ├── test_game_data_fetcher_cli.py
   ├── test_historical_compiler_cli.py
   ├── test_league_helper_cli.py
   ├── test_simulation_integration.py (enhanced with CLI tests)
   ├── test_accuracy_simulation_integration.py (enhanced with CLI tests)
   └── run_all_integration_tests.py (master runner)
   ```

**Traceability:**
- Epic requested "update ARCHITECTURE.md... testing architecture" (DISCOVERY.md line 422)
- Derived: Architecture doc must explain integration test framework structure

**Content Sources:**
- Feature 08 spec.md: Complete integration test framework details
- Feature 08 spec.md R1: 7 CLI test runners specification
- Feature 08 spec.md R6: Master runner specification

**Implementation Steps:**
1. Read Feature 08 spec.md for framework architecture details
2. Write Integration Test Framework subsection (~100-150 lines)
3. Add directory tree diagram
4. Document validation patterns with code examples

**Acceptance Criteria:**
- Integration Test Framework subsection added to ARCHITECTURE.md
- Directory tree diagram shows all 8 test files
- Validation patterns documented with code examples
- Cross-references Feature 08 integration test implementation

---

### R4: Create docs/testing/INTEGRATION_TESTING_GUIDE.md

**Source:** Epic Request (DISCOVERY.md line 423)

**Description:** Create comprehensive integration testing guide with examples, troubleshooting, and maintenance instructions.

**Detailed Implementation:**

1. **Create docs/testing/ directory** (currently doesn't exist per research findings)

2. **Create INTEGRATION_TESTING_GUIDE.md with sections:**

   **Section 1: Overview** (~30 lines)
   - What integration tests validate (CLI argument handling, subprocess execution)
   - When to run integration tests (before commits, during S7/S9 testing)
   - Integration test vs unit test differences

   **Section 2: Running Integration Tests** (~80 lines)
   - How to run individual test runners (7 scripts)
   - How to run master test runner
   - Command-line examples with expected outputs
   - Interpreting test results (exit codes, validation messages)

   **Section 3: Test Structure** (~60 lines)
   - How individual test runners are organized
   - Parametrized test patterns (multiple argument combinations)
   - Validation logic (exit code + specific outcomes)
   - Use of --e2e-test flag for speed

   **Section 4: Adding New Integration Tests** (~50 lines)
   - When to add new tests (new CLI arguments, new behaviors)
   - Test naming conventions
   - Validation pattern templates
   - Updating master runner

   **Section 5: Troubleshooting** (~80 lines)
   - Common issues and solutions
   - Test timeout issues (E2E mode >180 sec)
   - Exit code failures (non-zero)
   - Outcome validation failures (log patterns, file checks)
   - Debugging subprocess execution

**Traceability:**
- Epic requested "create docs/testing/INTEGRATION_TESTING_GUIDE.md with examples and troubleshooting" (DISCOVERY.md line 423)
- User Answer Q5: Tests validate exit code AND outcomes (guide must explain this)

**Content Sources:**
- Feature 08 spec.md: Complete integration test framework specification
- Feature 08 spec.md R7: Precedence rules and argument validation
- Features 01-07 specs: CLI argument lists and E2E behaviors

**Implementation Steps:**
1. Create docs/testing/ directory
2. Write INTEGRATION_TESTING_GUIDE.md (~300 lines total)
3. Include code examples from Feature 08 spec
4. Add troubleshooting scenarios from common test failures

**Acceptance Criteria:**
- docs/testing/ directory created
- INTEGRATION_TESTING_GUIDE.md created with 5 sections
- Code examples for running tests included
- Troubleshooting guide with 5+ common scenarios
- Cross-references Features 01-08 implementations

---

### R5: Update Epic Workflow Guides (S7 and S9)

**Source:** Epic Request (DISCOVERY.md line 424 "update epic workflow guides")

**Description:** Reference integration test runners in S7/S9 workflow guides to ensure they're used during smoke testing and QC.

**Detailed Implementation:**

1. **Update stages/s7/s7_p1_smoke_testing.md:**
   - Add step to run master integration test runner during S7.P1 smoke testing
   - Document expected outcome (all tests pass)
   - Reference INTEGRATION_TESTING_GUIDE.md for troubleshooting

2. **Update stages/s9/s9_p1_epic_smoke_testing.md:**
   - Add step to run master integration test runner during S9.P1 epic smoke testing
   - Document epic-level integration test validation
   - Reference INTEGRATION_TESTING_GUIDE.md for interpretation

3. **Content to add (both guides):**
   ```markdown
   ### Integration Test Validation (NEW - from KAI-7)

   **Run master integration test runner:**
   ```bash
   python tests/integration/run_all_integration_tests.py
   ```

   **Expected outcome:**
   - Exit code: 0 (all tests pass)
   - All 7 script tests report PASS
   - Total execution time: <15 minutes

   **If failures occur:**
   - Read test output for specific failure details
   - See docs/testing/INTEGRATION_TESTING_GUIDE.md for troubleshooting
   - Fix failing tests before proceeding to next phase
   ```

**Traceability:**
- Epic requested "update epic workflow guides... ensure integration test runners are used" (DISCOVERY.md line 424)
- Derived: S7/S9 smoke testing must include integration test validation (logically necessary)

**Content Sources:**
- Feature 08 spec.md: Master runner specification and expected outputs
- Epic workflow guides: Existing S7/S9 smoke testing structure

**Implementation Steps:**
1. Read s7_p1_smoke_testing.md and s9_p1_epic_smoke_testing.md current content
2. Identify insertion point for integration test validation step
3. Write integration test validation step (~20 lines per guide)
4. Cross-reference INTEGRATION_TESTING_GUIDE.md for troubleshooting

**Acceptance Criteria:**
- s7_p1_smoke_testing.md updated with integration test step
- s9_p1_epic_smoke_testing.md updated with integration test step
- Both guides reference INTEGRATION_TESTING_GUIDE.md
- Expected outcomes documented (exit code 0, all pass)

---

## Dependencies

### Feature Dependencies

**Blockers (must complete BEFORE this feature):**
- ✅ **Feature 08** (integration_test_framework) - S2 COMPLETE, S3 COMPLETE, S4 COMPLETE
  - Why: Need integration test framework spec to document
  - Status: Complete as of 2026-01-31
  - Source: DISCOVERY.md line 406 "Dependencies: Features 01-07 (need all scripts enhanced)"

**References (specs needed for content):**
- ✅ **Features 01-07** (all runner scripts) - S2 COMPLETE, S3 COMPLETE, S4 COMPLETE
  - Why: Need CLI argument lists from specs to document in README
  - Status: Complete as of 2026-01-30
  - Source: User Answer Q1 (script-specific args from constants)

### Data Dependencies

**Content Sources:**
- Feature 01 spec.md: player_fetcher arguments, E2E behavior, debug mode
- Feature 02 spec.md: schedule_fetcher arguments, E2E behavior, debug mode
- Feature 03 spec.md: game_data_fetcher arguments, E2E behavior, debug mode
- Feature 04 spec.md: historical_compiler arguments, E2E behavior, debug mode
- Feature 05 spec.md: win_rate_simulation arguments, E2E behavior, debug mode
- Feature 06 spec.md: accuracy_simulation arguments, E2E behavior, debug mode
- Feature 07 spec.md: league_helper arguments, mode selection, E2E flows
- Feature 08 spec.md: Integration test framework structure, validation logic

### File Dependencies

**Existing Files to Modify:**
- README.md (exists, 683 lines)
- ARCHITECTURE.md (exists, Testing Architecture section at lines 1158+)
- feature-updates/guides_v2/stages/s7/s7_p1_smoke_testing.md (exists)
- feature-updates/guides_v2/stages/s9/s9_p1_epic_smoke_testing.md (exists)

**New Files to Create:**
- docs/testing/ directory (does NOT exist)
- docs/testing/INTEGRATION_TESTING_GUIDE.md (new file, ~300 lines)

---

## Acceptance Criteria

**Feature 09 is COMPLETE when ALL of these are true:**

1. ✅ **README.md Updated:**
   - Quick Start section enhanced with CLI argument examples for all 7 scripts
   - Testing section includes Integration Testing subsection
   - Universal vs script-specific arguments clearly differentiated
   - 3 examples per script (normal, debug, E2E mode)
   - All 60+ arguments documented with descriptions

2. ✅ **ARCHITECTURE.md Updated:**
   - Testing Architecture section includes Integration Test Framework subsection
   - Directory tree diagram shows all 8 test files (7 individual + 1 master)
   - Validation patterns documented with code examples
   - Subprocess execution approach explained

3. ✅ **Integration Testing Guide Created:**
   - docs/testing/ directory created
   - INTEGRATION_TESTING_GUIDE.md created with 5 sections (~300 lines)
   - Running tests documented with examples
   - Troubleshooting guide with 5+ scenarios
   - Adding new tests documented

4. ✅ **Epic Workflow Guides Updated:**
   - s7_p1_smoke_testing.md includes integration test validation step
   - s9_p1_epic_smoke_testing.md includes integration test validation step
   - Both reference INTEGRATION_TESTING_GUIDE.md for troubleshooting

5. ✅ **All Content Accurate:**
   - All CLI arguments match Features 01-07 specs (no missing/incorrect args)
   - Integration test framework matches Feature 08 spec
   - E2E behaviors correctly documented per script type
   - Debug mode explains both logging AND behavioral changes

6. ✅ **Cross-References Valid:**
   - All feature spec references accurate (correct requirement numbers)
   - All file path references accurate (correct line numbers)
   - All guide references accurate (correct section names)

7. ✅ **User Approval:**
   - User reviews all documentation updates
   - User approves documentation completeness and accuracy

---

## Cross-Feature Alignment (S2.P3 Phase 5)

**Compared To:** Features 01-08 (all S2/S3/S4 COMPLETE)

**Alignment Status:** ✅ No conflicts

**Analysis:**

**Component Overlap:** NONE
- Feature 09 modifies: README.md, ARCHITECTURE.md, workflow guides
- Features 01-08 modify: Runner scripts, test files, constants
- No overlapping files (documentation vs implementation)

**Dependency Relationship:** One-way dependency (09 → 01-08)
- Feature 09 DEPENDS ON Features 01-08 (reads their specs for documentation content)
- Features 01-08 do NOT depend on Feature 09
- Integration: Documentation follows implementation (correct sequencing)

**Content Accuracy Validation:**
- R1 arguments must match Features 01-07 specs (validation: during S6 implementation)
- R2-R3 integration tests must match Feature 08 spec (validation: during S6 implementation)
- Acceptance criterion #5 requires: "All CLI arguments match Features 01-07 specs (no missing/incorrect args)"

**Conflicts Found:** Zero

**Changes Made:** None required (no conflicts to resolve)

**Critical Implementation Note:**
During S6, MUST cross-reference:
- Feature 01-07 specs for argument lists (R1)
- Feature 08 spec for integration test framework details (R2-R3)
- Any discrepancies = block implementation, return to S2 for clarification

**Verified By:** Agent
**Date:** 2026-01-31
**Compared Features:** 8 (Features 01-08)

---

**User Approval:** [x] APPROVED

**Approved By:** User
**Approved Date:** 2026-01-31 11:10
**Gate 3 Status:** ✅ PASSED

---

**Spec Version:** 2.0 (Enhanced from Secondary-H minimal spec)
**Last Enhanced:** 2026-01-31
**S2.P3 Phase 5:** COMPLETE (zero conflicts with Features 01-08)
