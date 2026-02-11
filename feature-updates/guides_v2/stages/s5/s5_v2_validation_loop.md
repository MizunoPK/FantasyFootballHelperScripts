# S5 v2: Implementation Planning with Validation Loop

**Extends:** Master Validation Loop Protocol
**See:** `reference/validation_loop_master_protocol.md`

**Stage:** S5 (Implementation Planning)
**Version:** 2.1 (Updated to extend master protocol)
**Created:** 2026-02-09
**Last Updated:** 2026-02-10
**Status:** Active (replaces S5 v1 22-iteration workflow)

---

## Table of Contents

1. [🎯 OVERVIEW](#-overview)
   - [What is S5 v2?](#what-is-s5-v2)
   - [How S5 v2 Differs from S5 v1](#how-s5-v2-differs-from-s5-v1)
   - [When to Use This Guide](#when-to-use-this-guide)
   - [Relationship to Master Validation Loop Protocol](#relationship-to-master-validation-loop-protocol)
1. [📐 THE TWO-PHASE APPROACH](#-the-two-phase-approach)
1. [🚀 PHASE 1: DRAFT CREATION](#-phase-1-draft-creation)
   - [Step-by-Step Process](#step-by-step-process)
1. [Task 1: Load ADP Data](#task-1-load-adp-data)
1. [Task 6: Create CLI Flag Tests (R1)](#task-6-create-cli-flag-tests-r1)
1. [Component Dependencies](#component-dependencies)
1. [Algorithm Traceability Matrix](#algorithm-traceability-matrix)
1. [Data Flow](#data-flow)
1. [Error Handling](#error-handling)
1. [Edge Cases](#edge-cases)
   - [Draft Creation Exit Criteria](#draft-creation-exit-criteria)
1. [🔄 PHASE 2: VALIDATION LOOP](#-phase-2-validation-loop)
   - [Validation Loop Protocol](#validation-loop-protocol)
   - [Round Structure](#round-structure)
   - [The 11 Implementation Planning Dimensions](#the-11-implementation-planning-dimensions)
   - [Round-by-Round Reading Patterns](#round-by-round-reading-patterns)
   - [Example Validation Loop Execution](#example-validation-loop-execution)
1. [🛑 SPECIAL CASES & PROTOCOLS](#-special-cases-protocols)
   - [If Validation Loop Exceeds 10 Rounds](#if-validation-loop-exceeds-10-rounds)
   - [If spec.md Discrepancies Found (Dimension 11)](#if-specmd-discrepancies-found-dimension-11)
   - [If Draft Quality <70% After 90 Minutes](#if-draft-quality-70-after-90-minutes)
1. [⚠️ COMMON ISSUES & FIXES](#-common-issues-fixes)
   - [Issue 1: "Can't find all algorithms in spec"](#issue-1-cant-find-all-algorithms-in-spec)
   - [Issue 2: "Interface verification taking too long"](#issue-2-interface-verification-taking-too-long)
   - [Issue 3: "Fixes introducing new issues"](#issue-3-fixes-introducing-new-issues)
   - [Issue 4: "Validation loop stuck at 8-9 rounds"](#issue-4-validation-loop-stuck-at-8-9-rounds)
   - [Issue 5: "Unsure if something is an issue"](#issue-5-unsure-if-something-is-an-issue)
1. [🚫 ANTI-PATTERNS TO AVOID](#-anti-patterns-to-avoid)
   - [❌ Anti-Pattern 1: "Working from Memory"](#-anti-pattern-1-working-from-memory)
   - [❌ Anti-Pattern 2: "Deferring Minor Issues"](#-anti-pattern-2-deferring-minor-issues)
   - [❌ Anti-Pattern 3: "Stopping at 3 Rounds Total"](#-anti-pattern-3-stopping-at-3-rounds-total)
   - [❌ Anti-Pattern 4: "Batching Fixes"](#-anti-pattern-4-batching-fixes)
   - [❌ Anti-Pattern 5: "Skipping Re-Reading After Small Fix"](#-anti-pattern-5-skipping-re-reading-after-small-fix)
   - [❌ Anti-Pattern 6: "Saying 'Efficiently' or 'Quickly'"](#-anti-pattern-6-saying-efficiently-or-quickly)
1. [✅ EXIT CRITERIA & QUALITY METRICS](#-exit-criteria-quality-metrics)
   - [Validation Loop Exit Criteria](#validation-loop-exit-criteria)
   - [Gate 5: User Approval](#gate-5-user-approval)
   - [Quality Metrics](#quality-metrics)
1. [📊 TRACKING & DOCUMENTATION](#-tracking-documentation)
   - [Update Agent Status](#update-agent-status)
   - [Validation Loop Log](#validation-loop-log)
1. [🎓 LESSONS LEARNED & BEST PRACTICES](#-lessons-learned-best-practices)
   - [Best Practice 1: Trust the Process](#best-practice-1-trust-the-process)
   - [Best Practice 2: Fresh Eyes Are Critical](#best-practice-2-fresh-eyes-are-critical)
   - [Best Practice 3: Conservative Issue Flagging](#best-practice-3-conservative-issue-flagging)
   - [Best Practice 4: One Dimension Can Affect Others](#best-practice-4-one-dimension-can-affect-others)
   - [Best Practice 5: Use Different Reading Patterns](#best-practice-5-use-different-reading-patterns)
1. [📚 REFERENCE](#-reference)
1. [Summary](#summary)

---

## Prerequisites

**Before starting S5 v2:**

- [ ] S4 complete - epic_smoke_test_plan.md updated, test_strategy.md created for this feature
- [ ] Feature spec.md complete (all sections filled, no TBD)
- [ ] Feature checklist.md resolved (all user questions answered, Gate 3 passed)
- [ ] S5 v2 template available: `templates/implementation_plan_template.md`
- [ ] Feature README.md exists with Agent Status section

**If any prerequisite missing:**
- ❌ Do NOT start S5 - Return to complete missing prerequisites

---

## Overview

### What is S5 v2?

S5 v2 is a **validation loop-based approach** to implementation planning that systematically refines `implementation_plan.md` through iterative validation rounds until it meets all quality criteria.

**Key Innovation:** Instead of 22 sequential iterations, S5 v2 uses a **2-phase approach**:
1. **Phase 1:** Create draft implementation_plan.md (60-90 min, ~70% quality)
2. **Phase 2:** Validation Loop refines to 99%+ quality (3.5-6 hours, 6-8 rounds typical)

**Exit Criteria:** 3 consecutive validation rounds finding zero issues

---

### How S5 v2 Differs from S5 v1

| Aspect | S5 v1 (Old) | S5 v2 (New) |
|--------|-------------|-------------|
| **Structure** | 22 iterations, 3 rounds | 11 dimensions, 1 validation loop |
| **Time** | 9-11 hours | 4.5-7 hours (35-50% savings) |
| **Redundancy** | 3x Algorithm Traceability, 3x Integration Gap | Zero (consolidated into dimensions) |
| **Quality** | Subjective (agent self-reports) | Objective (3 consecutive clean rounds) |
| **Verification** | Single pass per iteration | Multiple passes until clean |
| **Issue Deferral** | Possible to defer | Impossible (must fix before next round) |

---

### When to Use This Guide

**Use S5 v2 when:**
- Starting implementation planning after S4 complete (Epic Testing Strategy approved)
- Creating implementation_plan.md for a new feature
- All spec.md requirements finalized and user-approved (Gate 3 passed)

---

### Relationship to Master Validation Loop Protocol

**S5 v2 extends the Master Validation Loop Protocol** with implementation planning-specific dimensions.

**Validation Structure:**
- **7 Master Dimensions** (universal, always checked) - from `reference/validation_loop_master_protocol.md`
- **11 Implementation Planning Dimensions** (S5-specific, detailed below)
- **Total:** 18 dimensions checked every validation round

**How Master Dimensions Apply in S5 Context:**

| Master Dimension | How It Applies to implementation_plan.md |
|------------------|------------------------------------------|
| **D1: Empirical Verification** | All interfaces verified from actual source code (file:line), no assumed method signatures |
| **D2: Completeness** | All spec.md requirements have tasks, all test_strategy.md tests have creation tasks, all 11 sections present |
| **D3: Internal Consistency** | No contradictions between tasks, algorithms, data flow, or test coverage |
| **D4: Traceability** | Every task traces to spec requirement or test category, every algorithm traces to spec section |
| **D5: Clarity & Specificity** | Task acceptance criteria are specific and measurable (no vague "handle X properly") |
| **D6: Upstream Alignment** | Plan matches spec.md requirements exactly (no scope creep, no missing requirements) |
| **D7: Standards Compliance** | Follows implementation_plan_template.md structure and project coding standards |

**The 11 S5 Dimensions (below) provide the detailed implementation planning checklists** that operationalize these master dimensions in the context of creating implementation_plan.md.

**Core Validation Process:** Same as master protocol - 3 consecutive clean rounds required, zero deferred issues, fresh eyes every round.

---

## 📐 THE TWO-PHASE APPROACH

```text
┌─────────────────────────────────────────────────────────────┐
│                    PHASE 1: DRAFT CREATION                   │
│                       (60-90 minutes)                         │
└─────────────────────────────────────────────────────────────┘
                              ↓
    Create implementation_plan.md with all 11 sections
    Quality target: 70% (structure + major content present)
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                  PHASE 2: VALIDATION LOOP                    │
│                    (3.5-6 hours, 6-8 rounds)                 │
└─────────────────────────────────────────────────────────────┘
                              ↓
    Round 1: Find ~12 issues → Fix all → Round 2
    Round 2: Find ~8 issues → Fix all → Round 3
    Round 3: Find ~3 issues → Fix all → Round 4
    Round 4: Find 0 issues (clean count = 1)
    Round 5: Find 0 issues (clean count = 2)
    Round 6: Find 0 issues (clean count = 3) ✅ PASSED
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    GATE 5: USER APPROVAL                     │
│                       (5-10 minutes)                          │
└─────────────────────────────────────────────────────────────┘
                              ↓
                        PROCEED TO S6
```

---

## 🚀 PHASE 1: DRAFT CREATION

**Goal:** Create implementation_plan.md with all 11 dimension sections present

**Time:** 60-90 minutes

**Quality Target:** ~70% complete (structure exists, major content present, known gaps OK)

---

### Step-by-Step Process

#### **Step 1: Setup (5 minutes)**

1. **Copy template:**
   ```bash
   cp templates/implementation_plan_template.md feature_XX_{name}/implementation_plan.md
   ```

2. **Open files for reference:**
   - Feature spec.md (requirements source)
   - Feature checklist.md (verify all resolved)
   - S4 test_strategy.md (test coverage reference)

3. **Create Validation Loop Log:**
   ```bash
   cp templates/VALIDATION_LOOP_LOG_S5_template.md feature_XX_{name}/VALIDATION_LOOP_LOG.md
   ```

#### **Step 2: Requirements → Tasks (15-20 minutes)**

**Goal:** Create implementation tasks for all spec.md requirements **AND test_strategy.md tests**

**🚨 CRITICAL: Test Creation Tasks are MANDATORY**

Historical evidence from KAI-8 Feature 04 shows test creation tasks missing from implementation plan caused 56 tests to be missing until S7.P3 PR review (2-4 hour rework). **Test creation is implementation work**, not verification work.

**Process:**
1. **Read spec.md completely**
2. **Read test_strategy.md completely** (S4 output)
3. For EACH requirement in spec.md:
   - Create a FEATURE TASK in implementation_plan.md
   - Add requirement reference (which spec section)
   - Add basic acceptance criteria (2-3 items minimum)
   - Note file/method location (approximate is OK for draft)
4. For EACH test category in test_strategy.md:
   - Create a TEST CREATION TASK in implementation_plan.md
   - Reference test category (e.g., "R1 CLI Flag Integration - 8 tests")
   - Add test file path and test names
   - Include acceptance: "All [N] tests implemented and passing"

**Example Feature Task (Draft Quality):**
```markdown
## Task 1: Load ADP Data

**Requirement:** spec.md "Objective" - Load ADP rankings from CSV

**Acceptance Criteria:**
- [ ] Load data from data/rankings/adp.csv
- [ ] Return list of player rankings
- [ ] Handle file not found gracefully

**Location:** league_helper/util/PlayerManager.py (~line 450)
```

**Example Test Task (Draft Quality):**
```markdown
## Task 6: Create CLI Flag Tests (R1)

**Requirement:** test_strategy.md Category 1 - CLI Flag Integration (8 tests)

**Acceptance Criteria:**
- [ ] All 8 tests from test_strategy.md implemented (tests 1.1-1.8)
- [ ] Tests in tests/root_scripts/test_run_<feature>.py
- [ ] All tests passing (100% pass rate)

**Test Names:** test_argparse_has_flag, test_flag_default_false, test_flag_with_value_true, test_flag_action_store_true, test_existing_flags_unchanged, test_combined_flags_work, test_help_text_describes_flag, test_constant_changed_to_false
```

**Draft Quality Bar:**
- At least 70% of spec requirements have feature tasks
- At least 70% of test_strategy.md tests have test creation tasks
- Acceptance criteria exist (even if incomplete)
- Approximate locations OK

#### **Step 3: Dependencies Quick Pass (10-15 minutes)**

**Goal:** List external dependencies (defer detailed verification to validation loop)

**Process:**
1. Scan tasks for external method calls
2. List dependencies in "Component Dependencies" section
3. Quick note: file and approximate method name
4. **Do NOT verify interfaces yet** (validation loop will do this)

**Example (Draft Quality):**
```markdown
## Component Dependencies

1. **ConfigManager.get_adp_multiplier()**
   - Used in: Task 3
   - File: league_helper/util/ConfigManager.py
   - Purpose: Get ADP score multiplier

2. **csv_utils.read_csv_with_validation()**
   - Used in: Task 1
   - File: utils/csv_utils.py
   - Purpose: Read CSV with column validation
```

#### **Step 4: Algorithm Traceability (Initial) (15-20 minutes)**

**Goal:** Map spec algorithms to tasks (aim for 70% coverage minimum)

**Process:**
1. Extract algorithms from spec.md "Algorithms" section
2. Create table mapping algorithm → task
3. Include main algorithms and obvious helpers
4. **Defer edge case algorithms to validation loop**

**Example (Draft Quality):**
```markdown
## Algorithm Traceability Matrix

| Algorithm (from spec) | Spec Section | Implementation Task |
|----------------------|--------------|---------------------|
| Load ADP from CSV | Algorithms step 1 | Task 1 |
| Match player to ADP | Algorithms step 2 | Task 2 |
| Calculate multiplier | Algorithms step 3 | Task 3 |
| Apply to score | Algorithms step 4 | Task 4 |
```

**Draft Quality Bar:**
- 70% of spec algorithms mapped (major ones covered)
- Helper algorithms can be added in validation loop

#### **Step 5: Data Flow (Initial) (10-15 minutes)**

**Goal:** High-level flow diagram showing data movement

**Process:**
1. Identify entry point (where data enters)
2. List major transformations
3. Identify output point
4. **Defer detailed consumption verification to validation loop**

**Example (Draft Quality):**
```markdown
## Data Flow

**Entry:** data/rankings/adp.csv
  ↓
**Load:** Task 1 reads CSV → List of rankings
  ↓
**Match:** Task 2 matches players → Sets player.adp_value
  ↓
**Calculate:** Task 3 calculates multiplier → Sets player.adp_multiplier
  ↓
**Apply:** Task 4 applies to score → Updated total_score
  ↓
**Output:** Modified player scores used in draft recommendations
```

#### **Step 6: Error Cases & Edge Cases (Initial) (10-15 minutes)**

**Goal:** Enumerate obvious errors and edge cases

**Process:**
1. List obvious errors (file not found, malformed data)
2. List obvious edge cases (empty file, duplicate entries)
3. **Defer comprehensive enumeration to validation loop**

**Example (Draft Quality):**
```markdown
## Error Handling

1. File not found: Return empty list, log warning
2. Malformed CSV: Skip invalid rows, log warning
3. Player not in ADP: Set adp_value = None

## Edge Cases

1. Empty ADP file: All players get default multiplier
2. Duplicate players: Use first occurrence
3. Invalid ADP values: Clamp to valid range (1-500)
```text

**Draft Quality Bar:**
- 5-10 error scenarios identified
- 5-10 edge cases identified
- Handling strategies present (even if brief)

#### **Step 7: Create Remaining Sections (10-15 minutes)**

**Goal:** Create placeholder sections for remaining dimensions

**Process:**
1. **Test Strategy:** Reference S4's test_strategy.md
2. **Integration:** Note major integration points (defer verification)
3. **Performance:** Note if any O(n²) algorithms present
4. **Implementation Phases:** Rough 4-6 phase breakdown
5. **Spec Alignment:** Note validated sources exist

**Draft Quality Bar:**
- All 11 dimension sections exist in implementation_plan.md
- Placeholder content present (will be refined in validation loop)

---

### Draft Creation Exit Criteria

**Stop Phase 1 when ANY of these true:**

1. **Time limit reached:** 90 minutes elapsed (stop even if only 70% complete)
2. **Minimum content present:**
   - ✅ All 11 dimension sections exist
   - ✅ 70%+ of spec requirements have tasks
   - ✅ 70%+ of algorithms mapped
   - ✅ Basic error/edge cases listed

**Quality Expectation:** ~70% complete with known gaps

**Next Action:** Update Agent Status, proceed to Phase 2 (Validation Loop)

---

## 🔄 PHASE 2: VALIDATION LOOP

**Goal:** Iteratively refine implementation_plan.md until it passes all criteria

**Time:** 3.5-6 hours (typically 6-8 rounds)

**Quality Target:** 99%+ complete (3 consecutive clean rounds)

---

### Validation Loop Protocol

**Master Protocol:** See `reference/validation_loop_master_protocol.md`

**S5 Context:** Validating implementation_plan.md against 18 dimensions (7 master + 11 implementation planning)

**Exit Criteria:** 3 consecutive rounds finding ZERO issues

---

### Round Structure

Each round follows this pattern:

```
1. BREAK (2-5 minutes)
   - Clear mental model from previous round
   - Take actual break (don't work from memory)

2. RE-READ ENTIRE implementation_plan.md
   - Use Read tool (no working from memory)
   - Assume everything is wrong (fresh skepticism)

3. CHECK ALL 18 DIMENSIONS
   - 7 master dimensions (always checked)
   - 11 implementation planning dimensions (context-specific)
   - Systematically validate against each dimension
   - Use reading pattern for this round
   - Document EVERY issue found (no matter how minor)

4. REPORT FINDINGS
   - Count issues by dimension
   - Report: "Round N: X issues found across Y dimensions"

5. FIX OR CONTINUE
   - If X > 0: Fix ALL issues immediately → Round N+1, RESET counter
   - If X = 0: Increment clean counter → Check if 3 consecutive clean
```text

---

### The 11 Implementation Planning Dimensions

**These dimensions extend the 7 master dimensions** with implementation planning-specific checks.

**Every validation round checks:**
- ✅ All 7 master dimensions (Empirical Verification, Completeness, Internal Consistency, Traceability, Clarity & Specificity, Upstream Alignment, Standards Compliance)
- ✅ All 11 implementation planning dimensions (detailed below)
- **Total:** 18 dimensions per round

**📍 WHERE EVIDENCE GOES:**
- All evidence artifacts go IN implementation_plan.md
- Each dimension = section in implementation_plan.md
- Validation Loop Log tracks rounds/issues, NOT evidence

---

#### **Dimension 1: Requirements Completeness**

**What to Check:**
- [ ] Every spec.md requirement has implementation task(s)
- [ ] **🚨 CRITICAL: Every test_strategy.md test category has test creation task(s)**
- [ ] No orphan tasks (all tasks trace to spec requirements OR test_strategy.md)
- [ ] No scope creep (no tasks for unrequested features)
- [ ] Task numbering sequential with no gaps
- [ ] Every task cites which spec section OR test category it implements
- [ ] **Test task count matches test_strategy.md test count** (e.g., if test_strategy.md has 58 tests across 7 categories, implementation_plan.md should have ≥7 test creation tasks covering all 58 tests)

**Evidence Required:**
- Requirement-to-task mapping table showing 100% coverage (spec.md)
- **Test-to-task mapping table showing 100% coverage (test_strategy.md)**

**Example Issue (Feature Requirements):**
- "Missing requirement: spec.md line 67 'Handle player name matching' has no task"

**Example Issue (Test Requirements - NEW):**
- "Missing test creation: test_strategy.md Category 1 (8 CLI flag tests) has no implementation task"
- "Test count mismatch: test_strategy.md specifies 58 tests, but implementation_plan.md tasks only cover 42 tests (16 missing)"

**How to Fix:**
- Add Task X implementing the missing requirement
- **Add Test Creation Task Y for missing test category**
- Update requirement mapping table
- **Update test mapping table to show all test_strategy.md tests covered**

**Historical Evidence:**
- KAI-8 Feature 04: 56 tests missing from implementation plan caused 2-4 hour rework in S7.P3
- Root cause: S5 didn't create test creation tasks (only feature implementation tasks)
- Fix: Dimension 1 now validates BOTH feature tasks AND test creation tasks

---

#### **Dimension 2: Interface & Dependency Verification**

**What to Check:**
- [ ] All external dependencies identified
- [ ] Every dependency interface verified from ACTUAL source code
- [ ] Method signatures documented with file:line references
- [ ] No assumed interfaces (all copy-pasted from source)
- [ ] Data structure modifications verified as feasible
- [ ] No naming conflicts with existing code

**Evidence Required:**
- Dependency verification table with file:line references

**Example Issue:**
- "ConfigManager.get_adp_multiplier() assumed to return float, but actual signature (line 234) returns Tuple[float, int]"

**How to Fix:**
- Read actual source code: `league_helper/util/ConfigManager.py:234`
- Copy exact method signature to implementation_plan.md
- Update Task 3 to handle tuple return value

---

#### **Dimension 3: Algorithm Traceability**

**What to Check:**
- [ ] EVERY spec algorithm mapped to implementation task
- [ ] Typical: 40+ mappings (main + helper + edge case + error)
- [ ] Each algorithm includes exact spec quote
- [ ] Implementation location specified (file, method, ~line)
- [ ] Matrix completeness verified (count spec algorithms = count matrix rows)

**Evidence Required:**
- Algorithm Traceability Matrix with 40+ mappings

**Example Issue:**
- "Algorithm matrix has 28 mappings, but spec.md has 42 algorithms (missing 14)"

**How to Fix:**
- Re-read spec.md "Algorithms" section completely
- Add missing mappings to matrix
- Include helper algorithms and error handling algorithms

---

#### **Dimension 4: Task Specification Quality** (EMBEDS Gate 3a)

**What to Check:**
- [ ] Every task has requirement reference (which spec section)
- [ ] Every task has acceptance criteria checklist (3+ items)
- [ ] Every task has implementation location (file, method, line)
- [ ] Every task has dependencies documented (what it needs)
- [ ] Every task has test names specified
- [ ] No vague tasks ("handle", "process", "update" without details)

**Evidence Required:**
- 100% of tasks pass specification audit

**Example Issue:**
- "Task 5 acceptance criteria vague: 'Handle errors well' → Should specify error codes, logging, recovery"

**How to Fix:**
- Rewrite Task 5 acceptance criteria:
  - [ ] Catch FileNotFoundError, log warning, return empty list
  - [ ] Catch ValueError on invalid ADP, log warning, use default
  - [ ] All errors logged to feature logger

---

#### **Dimension 5: Data Flow & Consumption**

**What to Check:**
- [ ] Entry points identified (where data enters system)
- [ ] Complete data flow traced step-by-step
- [ ] **CRITICAL:** Every data load operation has downstream CONSUMPTION verified
- [ ] Data transformations at each step documented
- [ ] No gaps in data flow
- [ ] Output points verified (where data exits system)

**Evidence Required:**
- Data flow diagram: entry → transformations → consumption → output

**Example Issue:**
- "Task 1 loads ADP data, but no task shows HOW this data is consumed in calculations"

**How to Fix:**
- Add consumption verification to data flow section
- Document: "Task 2 consumes ADP data by calling get_adp_value() for each player"
- Verify consumption in Task 2 acceptance criteria

---

#### **Dimension 6: Error Handling & Edge Cases**

**What to Check:**
- [ ] ALL error scenarios enumerated (data quality, state, external)
- [ ] Error handling strategy for each (graceful degradation)
- [ ] ALL edge cases enumerated (boundary, null, empty, duplicate)
- [ ] Every edge case has handling strategy
- [ ] Every error/edge case has test coverage planned

**Evidence Required:**
- Error handling table (10+ scenarios typical)
- Edge case table (15+ cases typical)

**Example Issue:**
- "Missing error case: What if ConfigManager.get_adp_multiplier() raises exception?"

**How to Fix:**
- Add error case: "ConfigManager.get_adp_multiplier() raises KeyError if config missing"
- Add handling: "Catch KeyError, log error, use default multiplier 1.0"
- Add test: test_calculate_adp_multiplier_missing_config()

---

#### **Dimension 7: Integration & Compatibility**

**What to Check:**
- [ ] **Integration Gap Check:** Every new method has identified caller
- [ ] No orphan code (code written but never called)
- [ ] Call chains traced end-to-end (entry point → exit point)
- [ ] **Backward Compatibility:** Works with old data formats
- [ ] Migration path documented if breaking changes
- [ ] Configuration compatibility verified (old configs work)

**Evidence Required:**
- Integration verification table (method → caller → call site)
- Backward compatibility analysis

**Example Issue:**
- "New method _calculate_adp_multiplier() has no identified caller"

**How to Fix:**
- Identify caller: Task 2 (_match_player_to_adp) will call this
- Update integration table showing call chain
- OR remove method if truly not needed

---

#### **Dimension 8: Test Coverage Quality**

**What to Check:**
- [ ] Test strategy references S4's test_strategy.md (don't duplicate)
- [ ] Tests cover ALL code categories/types (e.g., all player positions)
- [ ] Success paths: 100% coverage
- [ ] Failure paths: 100% coverage
- [ ] Edge cases: >90% coverage
- [ ] **Resume/Persistence tests:** Old data format handling verified
- [ ] Overall coverage: >90%

**Evidence Required:**
- Test coverage analysis table showing >90% total coverage

**Example Issue:**
- "Test coverage 85% - missing tests for case-insensitive player matching"

**How to Fix:**
- Add test: test_match_player_case_insensitive()
- Verify coverage now >90%

---

#### **Dimension 9: Performance & Dependencies**

**What to Check:**
- [ ] Performance impact estimated (baseline vs with feature)
- [ ] Bottlenecks identified (O(n²) algorithms flagged)
- [ ] If regression >20%: optimization tasks added
- [ ] Python package dependencies listed
- [ ] Version compatibility checked (requirements.txt)
- [ ] Configuration changes documented (backward compatible)

**Evidence Required:**
- Performance analysis (baseline → estimated → optimized if needed)
- Dependency version table

**Example Issue:**
- "O(n²) player matching will cause 5.0s regression (>20% threshold)"

**How to Fix:**
- Add optimization task: Use dict for O(1) lookup instead of nested loops
- Document optimized performance: <0.1s (acceptable)

---

#### **Dimension 10: Implementation Readiness**

**What to Check:**
- [ ] Implementation phased into 4-6 logical phases
- [ ] Each phase has checkpoint and test validation
- [ ] Rollback strategy documented for each phase
- [ ] ALL mocks verified against real interfaces (read source code)
- [ ] 3+ integration tests with REAL objects (no mocks) planned
- [ ] Output consumers validated (format, structure, units match)
- [ ] Documentation tasks added (docstrings, ARCHITECTURE.md, etc.)

**Evidence Required:**
- Implementation phasing plan (4-6 phases with checkpoints)
- Mock audit report (all mocks verified)
- Integration test plan (3+ real-object tests)

**Example Issue:**
- "No implementation phasing - 'big bang' approach risks failure"

**How to Fix:**
- Break into phases:
  - Phase 1: Data loading + tests
  - Phase 2: Matching logic + tests
  - Phase 3: Calculation + tests
  - Phase 4: Integration + tests

---

#### **Dimension 11: Spec Alignment & Cross-Validation** (EMBEDS Gate 12a)

**What to Check:**
- [ ] spec.md validated against epic notes (no contradictions)
- [ ] spec.md validated against EPIC_TICKET.md (all epic requirements reflected)
- [ ] spec.md validated against SPEC_SUMMARY.md (summary matches detail)
- [ ] Zero discrepancies found
- [ ] **Cross-Dimension Validation (Gate 12a):**
  - All dimensions 1-10 have passed (no outstanding issues)
  - All evidence artifacts present in implementation_plan.md
  - Plan is implementation-ready (confidence >= MEDIUM)

**Evidence Required:**
- Spec validation report documenting zero discrepancies
- Cross-dimension checklist showing all D1-D10 pass

**Example Issue:**
- "spec.md says 'use default multiplier 1.0' but epic notes say 'use neutral multiplier 0.0'"

**How to Fix:**
- STOP validation loop immediately
- Report discrepancy to user
- Question: "Should spec.md or epic notes be correct?"
- After user clarifies: Update spec.md OR implementation_plan.md
- **RESTART validation loop from Round 1** (spec change invalidates prior validation)

---

### Round-by-Round Reading Patterns

**Vary patterns each round to catch different issue types**

**Every round checks all 18 dimensions (7 master + 11 implementation planning), but with varying focus areas:**

#### **Round 1: Sequential + Requirements/Interfaces Focus**
- Read implementation_plan.md top to bottom
- Primary focus: Master D1-D4 + Implementation D1-D4 (Requirements, Interfaces, Algorithms, Task Quality)
- Check: Sections exist and structured correctly, all requirements mapped, interfaces verified
- Pattern: Line-by-line completeness check

#### **Round 2: Reverse + Data Flow/Testing Focus**
- Read implementation_plan.md bottom to top
- Primary focus: Master D5-D7 + Implementation D5-D8 (Data Flow, Errors, Integration, Tests)
- Check: Gaps and inconsistencies in data handling and test coverage
- Pattern: Reverse reading catches issues missed in forward read

#### **Round 3: Spot-Checks + Quality/Alignment Focus**
- Random spot-check 5-10 tasks
- Primary focus: Implementation D9-D11 + Master D6 (Performance, Implementation Prep, Spec Alignment)
- Check: Consistency across plan, upstream alignment
- Pattern: Sample validation (not exhaustive)

#### **Round 4+: Alternate Patterns**
- **Round 4:** Sequential again (fresh eyes on whole document, all 18 dimensions)
- **Round 5:** Focus on recent changes (did fixes introduce issues?)
- **Round 6:** Cross-section validation (do all sections align? master dimensions + implementation dimensions)
- **Round 7+:** Deep dive into previously clean dimensions

---

### Example Validation Loop Execution

```text
DRAFT CREATION: 90 minutes
- Created implementation_plan.md with all 11 dimensions
- Quality estimate: ~70%

─────────────────────────────────────────────────────────
ROUND 1: Sequential read, D1-4 focus (30 min)
─────────────────────────────────────────────────────────
Issues found: 12

Dimension 1:
- Missing requirement: spec.md line 45 (player name normalization)
- Missing requirement: spec.md line 67 (case-insensitive matching)

Dimension 2:
- ConfigManager.get_adp_multiplier() interface not verified
- csv_utils.read_csv_with_validation() parameters assumed

Dimension 3:
- Algorithm matrix only 28 mappings, need 40+
- Missing error handling algorithms

Dimension 4:
- Task 3 acceptance criteria vague ("handle multiplier")
- Task 7 has no test names specified
- Task 9 implementation location not specified

Action: Fix all 12 issues → implementation_plan.md updated
Clean count: RESET to 0
Next: Round 2

─────────────────────────────────────────────────────────
ROUND 2: Reverse read, D5-8 focus (35 min)
─────────────────────────────────────────────────────────
Issues found: 8

Dimension 5:
- Task 1 loads data, but consumption not verified
- Data flow missing transformation step (normalization)

Dimension 6:
- Missing error: What if ADP CSV has wrong columns?
- Edge case not handled: Empty string player names

Dimension 8:
- Resume/persistence tests not planned
- Test coverage 85% (need >90%)

Dimension 9:
- O(n²) matching algorithm identified, no optimization plan

Action: Fix all 8 issues → implementation_plan.md updated
Clean count: RESET to 0
Next: Round 3

─────────────────────────────────────────────────────────
ROUND 3: Spot-checks, D9-11 focus (25 min)
─────────────────────────────────────────────────────────
Issues found: 3

Dimension 11:
- spec.md contradicts epic notes on error handling approach

Dimension 4:
- Task 15 acceptance criteria still not measurable

Dimension 7:
- Backward compatibility analysis missing migration path

Action: Fix all 3 issues → implementation_plan.md updated
Clean count: RESET to 0
Next: Round 4

─────────────────────────────────────────────────────────
ROUND 4: Sequential read, all dimensions (30 min)
─────────────────────────────────────────────────────────
Issues found: 0 ✅

All 18 dimensions validated:

**Master Dimensions (7):**
✅ Master D1: Empirical Verification - All interfaces verified from source code
✅ Master D2: Completeness - All sections present, all requirements mapped
✅ Master D3: Internal Consistency - No contradictions found
✅ Master D4: Traceability - All tasks trace to requirements/tests
✅ Master D5: Clarity & Specificity - All acceptance criteria measurable
✅ Master D6: Upstream Alignment - Matches spec.md exactly
✅ Master D7: Standards Compliance - Follows template structure

**Implementation Planning Dimensions (11):**
✅ D1: All requirements mapped (spec + tests)
✅ D2: All interfaces verified from source
✅ D3: 42 algorithm mappings complete
✅ D4: All tasks specific with acceptance criteria
✅ D5: Data consumption verified
✅ D6: 12 errors, 18 edge cases documented
✅ D7: All methods have callers, backward compat verified
✅ D8: Test coverage 92%
✅ D9: Performance optimized, <1% regression
✅ D10: 5 implementation phases, mocks audited
✅ D11: Spec aligned with epic notes

Clean count: 1 consecutive clean round
Next: Round 5

─────────────────────────────────────────────────────────
ROUND 5: Focus on recent changes (25 min)
─────────────────────────────────────────────────────────
Issues found: 0 ✅

Checked all fixes from Rounds 1-3:
- Requirement additions didn't introduce scope creep
- Interface verifications are accurate
- Algorithm mappings complete
- Task specifications are specific
- No new issues introduced by fixes

Clean count: 2 consecutive clean rounds
Next: Round 6

─────────────────────────────────────────────────────────
ROUND 6: Cross-section validation (25 min)
─────────────────────────────────────────────────────────
Issues found: 0 ✅

Verified consistency across all sections:
- Requirements → Algorithms → Tasks all aligned
- Dependencies → Integration → Tests all consistent
- Performance → Implementation phases coherent
- No contradictions between sections

Clean count: 3 consecutive clean rounds ✅
Status: PASSED

─────────────────────────────────────────────────────────
VALIDATION LOOP COMPLETE
─────────────────────────────────────────────────────────

Total time: 90 min draft + 170 min validation = 4h 20min
Total rounds: 6
Total issues fixed: 23
Final quality: 99%+ (validated by 3 consecutive clean rounds)

Next: Present implementation_plan.md to user (Gate 5)
```

---

## 🛑 SPECIAL CASES & PROTOCOLS

### If Validation Loop Exceeds 10 Rounds

**Problem:** Still finding issues after 10 rounds (max limit reached)

**Action:**
1. STOP the validation loop
2. Document all issues found in last 3 rounds
3. Escalate to user with summary:
   - "I've completed 10+ rounds of validation"
   - "Issues continue to be found: [describe pattern]"
   - "Possible causes: [architecture issue? scope too large? unclear requirements?]"
   - "I need guidance on how to proceed"
4. Await user decision

**User Options:**
- Adjust scope (remove some requirements)
- Return to S2 (spec needs refinement)
- Override validation (accept current state)
- Provide additional context/clarification

---

### If spec.md Discrepancies Found (Dimension 11)

**Problem:** spec.md contradicts epic notes, EPIC_TICKET.md, or SPEC_SUMMARY.md

**Action:**
1. STOP validation loop immediately
2. Document ALL discrepancies found
3. Report to user with question:
   - "Found discrepancy between spec.md and [source]"
   - "spec.md says: [X]"
   - "[source] says: [Y]"
   - "Which should be correct?"
4. Await user decision
5. After user clarifies: Update spec.md OR implementation_plan.md
6. **RESTART validation loop from Round 1** (spec changes invalidate prior validation)

**Why restart is required:** Spec changes ripple through requirements, algorithms, tasks. Must re-validate everything.

---

### If Draft Quality <70% After 90 Minutes

**Problem:** Phase 1 time limit reached but draft quality below 70%

**Action:**
1. STOP Phase 1 at 90 minutes (do not extend)
2. Document draft quality: "X% complete after 90 min"
3. Proceed to Phase 2 anyway
4. Validation loop will catch missing content (that's its purpose)

**Why this works:** Validation loop systematically finds gaps. Better to start validating at 70% than spend extra time polishing draft to 85%.

---

## ⚠️ COMMON ISSUES & FIXES

### Issue 1: "Can't find all algorithms in spec"

**Symptom:** Algorithm matrix only 20-30 mappings, but need 40+

**Cause:** Only mapped main algorithms, missed helpers, edge cases, error handling

**Fix:**
- Re-read spec.md "Algorithms" section completely
- Look for implicit algorithms (error handling, validation, normalization)
- Check "Edge Cases" section for algorithm variations
- Check "Error Handling" section for recovery algorithms

---

### Issue 2: "Interface verification taking too long"

**Symptom:** Spending >30 minutes verifying interfaces in validation round

**Cause:** Trying to verify too thoroughly in single round

**Fix:**
- In Round 1: Verify 3-5 most critical interfaces
- In Round 2: Verify next 3-5 interfaces
- In Round 3: Verify remaining interfaces
- Don't block on interface verification - spread across rounds

---

### Issue 3: "Fixes introducing new issues"

**Symptom:** Round 4 finds issues in sections that were clean in Round 3

**Cause:** Normal! Fixes can introduce new issues. That's why we need 3 consecutive clean rounds.

**Fix:**
- This is expected behavior, not a problem
- Keep fixing issues and re-validating
- Counter resets when issues found (by design)
- Eventually, fixes won't introduce new issues → 3 clean rounds → exit

---

### Issue 4: "Validation loop stuck at 8-9 rounds"

**Symptom:** Approaching 10 round limit, still finding issues

**Cause:** May indicate fundamental problem (unclear requirements, wrong approach)

**Fix:**
- Before Round 10: Ask yourself "What pattern do I see in recent issues?"
- If same dimension keeps failing: Root cause may be spec clarity issue
- If issues scattered: May need to slow down and be more thorough
- At Round 10: Escalate to user (don't force to continue)

---

### Issue 5: "Unsure if something is an issue"

**Symptom:** Found something that might be wrong, but not sure if it counts as issue

**Cause:** Unclear validation criteria

**Fix:**
- **If in doubt, call it an issue**
- Better to flag and fix than miss a real issue
- Validation loop will catch if fix was unnecessary (next round will be clean)
- Conservative approach: assume everything is wrong until proven right

---

## 🚫 ANTI-PATTERNS TO AVOID

### ❌ Anti-Pattern 1: "Working from Memory"

**Wrong:** "I remember I checked this in Round 1, so I'll skip it in Round 2"

**Right:** Re-read ENTIRE implementation_plan.md every round using Read tool

**Why:** Memory-based validation misses issues. Fresh eyes each round catches what memory overlooks.

---

### ❌ Anti-Pattern 2: "Deferring Minor Issues"

**Wrong:** "This is a minor typo, I'll fix it later" (mark as low priority, continue)

**Right:** Fix ALL issues immediately before next round, no matter how minor

**Why:** "Later" never comes. Small issues compound. Validation loop requires zero deferred issues.

---

### ❌ Anti-Pattern 3: "Stopping at 3 Rounds Total"

**Wrong:** "I've done 3 rounds (found 5, 3, 1 issues), I'm done"

**Right:** Need 3 CONSECUTIVE CLEAN rounds (might be rounds 4-5-6, or 6-7-8)

**Why:** Exit criteria is 3 consecutive rounds with ZERO issues, not 3 rounds total.

---

### ❌ Anti-Pattern 4: "Batching Fixes"

**Wrong:** "I'll note all issues from Rounds 1-3, then fix them all at once"

**Right:** Fix all issues from Round N immediately before Round N+1

**Why:** Fixes from Round 1 might change what you find in Round 2. Can't batch.

---

### ❌ Anti-Pattern 5: "Skipping Re-Reading After Small Fix"

**Wrong:** "I only changed one line, I don't need to re-read everything"

**Right:** Re-read ENTIRE implementation_plan.md every round (fixes can introduce new issues)

**Why:** One-line fix in Dimension 1 might create issue in Dimension 7 (integration). Must check everything.

---

### ❌ Anti-Pattern 6: "Saying 'Efficiently' or 'Quickly'"

**Wrong:** "I'll efficiently complete this validation round"

**Right:** Follow every step systematically, checking all dimensions

**Why:** "Efficiently" is code for "cutting corners." Validation loop exists to prevent mistakes from cutting corners.

---

## Exit Criteria

### Validation Loop Exit Criteria

**Can ONLY exit when ALL true:**

1. ✅ 3 consecutive rounds found ZERO issues each
2. ✅ Rounds N-2, N-1, and N all found zero issues
3. ✅ All 18 dimensions validated in final 3 rounds (7 master + 11 implementation planning)
4. ✅ All evidence artifacts present in implementation_plan.md
5. ✅ Confidence level >= MEDIUM
6. ✅ implementation_plan.md version incremented (v0.1 draft → v1.0 validated)

**If ANY criterion fails:** Continue validation loop

---

### Gate 5: User Approval

**After validation loop passes:**

1. **Update implementation_plan.md:**
   - Add validation completion timestamp
   - Add "Validated: 3 consecutive clean rounds (rounds X, Y, Z)"
   - Increment version to v1.0

2. **Present to user:**
   - Use prompt from `prompts_reference_v2.md` → "S5 Complete - Implementation Plan Approval"
   - Highlight key sections (tasks, phasing, test strategy)
   - Request explicit approval

3. **Wait for user response:**
   - If approved: Document approval timestamp, proceed to S6
   - If changes requested: Make changes, re-validate affected dimensions, re-submit

4. **Document approval:**
   - Add "User Approved: [timestamp] by [user]" to implementation_plan.md
   - Update feature README.md Agent Status: "S5 complete, S6 ready"

---

### Quality Metrics

**Success indicators:**
- ✅ Validation loop completed in 6-8 rounds (typical)
- ✅ Total time 4.5-7 hours (draft + validation + user approval)
- ✅ Zero deferred issues (all issues fixed)
- ✅ 3 consecutive clean rounds achieved
- ✅ User approval obtained on first submission

**Warning signs:**
- ⚠️ 10 rounds without 3 clean (escalate to user)
- ⚠️ >8 hours total (may indicate scope too large)
- ⚠️ User requests major changes (may need to restart S2)

---

## 📊 TRACKING & DOCUMENTATION

### Update Agent Status

**After Phase 1 (Draft Creation):**
```markdown
**Stage:** S5 (Implementation Planning)
**Phase:** Phase 2 - Validation Loop
**Progress:** Draft created (70% quality), starting validation
**Last Updated:** [timestamp]
**Current Guide:** stages/s5/s5_v2_validation_loop.md
**Next Action:** Begin validation Round 1
```

**After Each Validation Round:**
```markdown
**Stage:** S5 (Implementation Planning)
**Phase:** Phase 2 - Validation Loop
**Progress:** Round N complete, X issues found and fixed
**Clean Count:** Y consecutive clean rounds
**Last Updated:** [timestamp]
**Next Action:** Round N+1 validation
```

**After Validation Loop Passes:**
```markdown
**Stage:** S5 (Implementation Planning)
**Phase:** Gate 5 - User Approval
**Progress:** Validation loop passed (3 consecutive clean rounds)
**Quality:** 99%+ (rounds X, Y, Z clean)
**Last Updated:** [timestamp]
**Next Action:** Present implementation_plan.md for user approval
```

---

### Validation Loop Log

**Use template:** `VALIDATION_LOOP_LOG_S5_template.md`

**Track for each round:**
- Timestamp
- Reading pattern used
- Issues found (by dimension)
- Fixes applied
- Clean count status
- Next action

**Why this matters:** If session interrupted, log shows exactly where to resume.

---

## 🎓 LESSONS LEARNED & BEST PRACTICES

### Best Practice 1: Trust the Process

**Lesson:** If you find 15 issues in Round 1, don't panic. This is normal and expected.

**Why:** Draft was only 70% quality. Validation loop designed to systematically find and fix all issues.

**Action:** Fix all 15 issues, continue to Round 2. Issues will decrease each round.

---

### Best Practice 2: Fresh Eyes Are Critical

**Lesson:** Taking a 2-5 minute break between rounds significantly improves issue detection.

**Why:** Mental model from previous round creates blind spots. Break clears the model.

**Action:** Actually take the break. Don't rush. Quality > speed.

---

### Best Practice 3: Conservative Issue Flagging

**Lesson:** When in doubt, flag it as an issue. Better to over-flag than under-flag.

**Why:** If it's not really an issue, next round will be clean anyway. If it IS an issue and you skip it, you might never catch it.

**Action:** Assume everything is wrong until proven right.

---

### Best Practice 4: One Dimension Can Affect Others

**Lesson:** Fixing issue in Dimension 3 (Algorithms) might create issue in Dimension 7 (Integration).

**Why:** Dimensions are interconnected. That's why we validate ALL dimensions EVERY round.

**Action:** Never assume fixing one dimension won't affect others. Always re-validate everything.

---

### Best Practice 5: Use Different Reading Patterns

**Lesson:** Reading the same way every round causes pattern blindness. Vary the pattern.

**Why:** Forward reading catches some issues, reverse reading catches others, spot-checks catch still others.

**Action:** Follow suggested reading patterns for each round (sequential, reverse, spot-check, etc.)

---

## 📚 REFERENCE

**Related Guides:**
- `reference/validation_loop_master_protocol.md` - Master validation loop protocol (7 universal dimensions)
- `prompts_reference_v2.md` - Phase transition prompts
- `templates/implementation_plan_template.md` - Starting template
- `templates/VALIDATION_LOOP_LOG_S5_template.md` - Tracking template

**Next Stage:**
- After Gate 5 approval: `stages/s6/s6_execution.md`

---

## Summary

**S5 v2 Validation Loop:**
- **Extends:** Master Validation Loop Protocol (7 universal dimensions)
- **Adds:** 11 implementation planning-specific dimensions
- **Total:** 18 dimensions checked every round
- **Process:** 3 consecutive clean rounds required
- **Time:** 4.5-7 hours (draft + validation + user approval)
- **Quality:** 99%+ implementation-ready plan

**Key Principle:**
> "Every implementation plan must be validated against both universal quality dimensions (empirical verification, completeness, consistency, traceability, clarity, alignment, standards) AND implementation-specific dimensions (requirements coverage, interface verification, algorithm traceability, task quality, data flow, error handling, integration, test coverage, performance, implementation readiness, spec alignment) before proceeding to execution."

---

**This guide is complete and ready for use. Begin with Phase 1: Draft Creation when S4 is complete and spec.md is finalized.**
