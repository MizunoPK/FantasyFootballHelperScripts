# STAGE 6: Epic-Level Final QC Guide

**Guide Version:** 2.0
**Last Updated:** 2025-12-30
**Prerequisites:** ALL features complete (Stage 5e), no pending bug fixes
**Next Stage:** STAGE_7_epic_cleanup_guide.md

---

## 🚨 MANDATORY READING PROTOCOL

**BEFORE starting Stage 6, you MUST:**

1. **Read this ENTIRE guide** using the Read tool
2. **Use the phase transition prompt** from `prompts_reference_v2.md` ("Starting Epic Final QC")
3. **Acknowledge critical requirements** by listing them explicitly
4. **Verify ALL prerequisites** using the checklist below
5. **Update EPIC_README.md Agent Status** to reflect Stage 6 start
6. **THEN AND ONLY THEN** begin epic-level QC

**Rationale:** Stage 6 validates the ENTIRE epic as a cohesive whole. Feature-level testing (Stage 5c) validated individual features in isolation. Epic-level testing validates:
- Cross-feature integration
- Epic-wide workflows
- End-to-end success criteria
- Architectural consistency across all features

Skipping this guide results in missing epic-level integration issues that only appear when features work together.

---

## Quick Start

**What is Stage 6?**
Epic-Level Final QC validates the ENTIRE epic end-to-end after ALL features are implemented. Unlike feature-level testing (Stage 5c), this stage focuses on epic-wide integration, cross-feature workflows, and validating against the original epic request.

**When do you use this guide?**
- After ALL features have completed Stage 5e
- No pending bug fixes
- Ready to validate epic as a whole

**Key Outputs:**
- ✅ Epic smoke testing passed (using epic_smoke_test_plan.md)
- ✅ Epic QC rounds passed (3 rounds validating epic cohesion)
- ✅ Epic PR review passed (11 categories applied to epic-wide changes)
- ✅ End-to-end validation against original epic request
- ✅ Bug fixes created for any epic-level integration issues (if discovered)
- ✅ EPIC_README.md updated with Stage 6 completion status

**Time Estimate:**
Epic-level QC typically takes 30-60 minutes for 3-feature epics, 60-120 minutes for 5+ feature epics.

**Critical Success Factors:**
1. Execute epic_smoke_test_plan.md EXACTLY as evolved (not as originally written in Stage 1)
2. Validate epic as COHESIVE WHOLE (not just sum of features)
3. Compare to ORIGINAL epic request (not intermediate specs)
4. If ANY issues discovered → Create bug fixes, RESTART Stage 6

---

## 🛑 Critical Rules

```
┌─────────────────────────────────────────────────────────────────┐
│ CRITICAL RULES FOR STAGE 6                                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ 1. ⚠️ ALL FEATURES MUST COMPLETE STAGE 5e                       │
│    - Verify EVERY feature shows "Stage 5e complete" in README   │
│    - Verify no pending features or bug fixes                    │
│    - Epic smoke test plan MUST be fully evolved                 │
│                                                                  │
│ 2. ⚠️ USE EVOLVED epic_smoke_test_plan.md (NOT ORIGINAL)        │
│    - Plan evolved through Stages 1 → 4 → 5e updates             │
│    - Reflects ACTUAL implementation (not initial assumptions)   │
│    - Contains integration scenarios added during Stage 5e       │
│                                                                  │
│ 3. ⚠️ EPIC TESTING ≠ FEATURE TESTING                            │
│    - Feature testing (5c): Tests feature in isolation           │
│    - Epic testing (6): Tests ALL features working together      │
│    - Focus: Cross-feature workflows, integration points         │
│                                                                  │
│ 4. ⚠️ VALIDATE AGAINST ORIGINAL EPIC REQUEST                    │
│    - Read the ORIGINAL {epic_name}.txt user request             │
│    - Compare implemented epic to user's initial vision          │
│    - Verify all original goals achieved                         │
│                                                                  │
│ 5. ⚠️ THREE EPIC QC ROUNDS (NO EXCEPTIONS)                      │
│    - QC Round 1: Cross-feature integration validation           │
│    - QC Round 2: Epic cohesion and consistency                  │
│    - QC Round 3: End-to-end success criteria                    │
│                                                                  │
│ 6. ⚠️ EPIC PR REVIEW (11 CATEGORIES - EPIC SCOPE)               │
│    - Same 11 categories as Stage 5c                             │
│    - Applied to EPIC-WIDE changes (not individual features)     │
│    - Focus: Architectural consistency across features           │
│                                                                  │
│ 7. ⚠️ IF ANY ISSUES → CREATE BUG FIX, RESTART STAGE 6           │
│    - Epic-level issues require bug fix workflow                 │
│    - After bug fix completes → COMPLETELY RESTART Stage 6       │
│    - Re-run: Smoke testing → QC 1 → QC 2 → QC 3 → PR review     │
│                                                                  │
│ 8. ⚠️ NO PARTIAL WORK ACCEPTED - ZERO TECH DEBT TOLERANCE      │
│    - Cannot "partially pass" Stage 6                            │
│    - Either 100% pass or RESTART - no exceptions                │
│    - Epic must meet ALL requirements from original request      │
│    - NO deferred features, NO "will add later" items            │
│    - Clean codebase - ZERO compromises, ZERO tech debt          │
│    - Document ALL issues before restarting                      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Prerequisites Checklist

**Before starting Stage 6, verify:**

### Epic Completion Status
- [ ] ALL features show "Stage 5e complete" in their README.md files
- [ ] No features in Stage 5a, 5b, 5c, 5d, or 5e (all must be done)
- [ ] No pending bug fixes (check EPIC_README.md for bug fix folders)
- [ ] All unit tests passing (100% pass rate across entire epic)

### Epic Smoke Test Plan Status
- [ ] epic_smoke_test_plan.md exists in epic root folder
- [ ] Plan shows "Last Updated" timestamp from recent Stage 5e
- [ ] Plan includes integration scenarios (added during Stage 5e)
- [ ] Plan includes cross-feature workflows (not just individual features)
- [ ] Plan includes epic success criteria (defined in Stage 4)

### Epic Documentation Status
- [ ] EPIC_README.md "Epic Progress Tracker" shows all features at 5e
- [ ] epic_lessons_learned.md contains insights from all features
- [ ] Original epic request file ({epic_name}.txt) is accessible

### Environment Readiness
- [ ] All dependencies installed (no missing imports)
- [ ] Test data available (required for smoke testing)
- [ ] Previous feature implementations verified working (re-test if unsure)

**If ANY checklist item is unchecked, STOP. Do NOT proceed to Stage 6 until all prerequisites are met.**

---

## Workflow Overview

```
STAGE 6: Epic-Level Final QC
│
├─> STEP 1: Pre-QC Verification (Verify epic ready)
│   ├─ Verify all features at Stage 5e
│   ├─ Verify no pending bug fixes
│   ├─ Read evolved epic_smoke_test_plan.md
│   └─ Read original epic request ({epic_name}.txt)
│
├─> STEP 2: Epic Smoke Testing (Execute evolved test plan)
│   ├─ Part 1: Epic-level import tests
│   ├─ Part 2: Epic-level entry point tests
│   ├─ Part 3: Epic end-to-end execution tests
│   ├─ Part 4: Cross-feature integration tests (NEW - from Stage 5e)
│   └─ Verify ALL output DATA values (not just structure)
│
├─> STEP 3: Epic QC Round 1 (Cross-Feature Integration)
│   ├─ Integration point validation
│   ├─ Data flow across features
│   ├─ Interface compatibility
│   ├─ Error propagation handling
│   └─ Document findings
│
├─> STEP 4: Epic QC Round 2 (Epic Cohesion & Consistency)
│   ├─ Code style consistency across features
│   ├─ Naming convention consistency
│   ├─ Error handling consistency
│   ├─ Architectural pattern consistency
│   └─ Document findings
│
├─> STEP 5: Epic QC Round 3 (End-to-End Success Criteria)
│   ├─ Validate against original epic request
│   ├─ Verify epic success criteria (from Stage 4)
│   ├─ User experience flow validation
│   ├─ Performance characteristics
│   └─ Document findings
│
├─> STEP 6: Epic PR Review (11 Categories - Epic Scope)
│   ├─ Apply all 11 categories to epic-wide changes
│   ├─ Focus on architectural consistency
│   ├─ Review cross-feature impacts
│   └─ Document findings
│
├─> STEP 7: Handle Issues (If any discovered)
│   ├─ Document ALL issues found
│   ├─ Create bug fixes for epic-level integration issues
│   ├─ Run bug fix through workflow (Stage 2→5a→5b→5c)
│   └─ RESTART Stage 6 (re-run ALL steps)
│
└─> STEP 8: Final Verification & README Update
    ├─ Verify all issues resolved
    ├─ Update EPIC_README.md Epic Progress Tracker
    ├─ Update epic_lessons_learned.md with Stage 6 insights
    └─ Mark Stage 6 complete in EPIC_README.md
```

**Critical Decision Points:**
- **After Step 2:** If smoke testing fails → Fix issues, RESTART Step 2
- **After Steps 3-5:** If QC rounds find issues → Document, create bug fixes, RESTART Stage 6
- **After Step 6:** If PR review finds issues → Document, create bug fixes, RESTART Stage 6
- **After Step 7:** If bug fixes created → RESTART Stage 6 (all steps)

---

## Detailed Workflow

### STEP 1: Pre-QC Verification

**Objective:** Verify epic is ready for Stage 6 validation.

**Actions:**

**1a. Verify All Features Complete**

Read EPIC_README.md "Epic Progress Tracker" section:

```markdown
## Epic Progress Tracker
| Feature | Stage 1 | Stage 2 | Stage 3 | Stage 4 | Stage 5a | Stage 5b | Stage 5c | Stage 5d | Stage 5e |
|---------|---------|---------|---------|---------|----------|----------|----------|----------|----------|
| feature_01_adp_integration | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| feature_02_matchup_system | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| feature_03_performance_tracker | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
```

**Verify:** EVERY feature shows ✅ in Stage 5e column.

**If ANY feature is incomplete:**
- STOP Stage 6
- Complete the incomplete feature first
- Return to Stage 6 when ALL features at 5e

**1b. Verify No Pending Bug Fixes**

Check epic folder for any `bugfix_{priority}_{name}/` folders:

```bash
ls feature-updates/{epic_name}/
```

**If bug fix folders exist:**
- Check their README.md for completion status
- If incomplete → Complete bug fix first
- If complete → Verify they're at Stage 5c (bug fixes don't do 5d/5e)

**1c. Read Evolved Epic Smoke Test Plan**

Use Read tool to load `epic_smoke_test_plan.md`:

```markdown
# Epic Smoke Test Plan: {epic_name}

**Last Updated:** Stage 5e (feature_03_performance_tracker) - 2025-12-30

## Update History
| Stage | Feature | Date | Changes Made |
|-------|---------|------|--------------|
| 1 | (initial) | 2025-12-15 | Created placeholder test plan |
| 4 | (all features) | 2025-12-20 | Updated based on deep dive findings |
| 5e | feature_01 | 2025-12-25 | Added ADP integration scenarios |
| 5e | feature_02 | 2025-12-28 | Added matchup system cross-checks |
| 5e | feature_03 | 2025-12-30 | Added performance tracking E2E tests |
```

**Verify:**
- Plan shows "Last Updated" from RECENT Stage 5e (not Stage 1 or 4)
- Update History table shows ALL features contributed updates
- Test scenarios reflect ACTUAL implementation (not original assumptions)

**1d. Read Original Epic Request**

Use Read tool to load `{epic_name}.txt` (the user's original request):

**Example:**
```
Epic Request: Improve Draft Helper System

Goals:
- Integrate ADP data for market wisdom
- Add matchup-based projections
- Track player performance vs projections

Expected Outcome:
User can make better draft decisions by seeing:
1. Market consensus (ADP)
2. Matchup difficulty
3. Historical accuracy of projections
```

**Why this matters:** Stage 6 validates against THIS original vision, not intermediate specs that may have evolved.

---

### STEP 2: Epic Smoke Testing

**Objective:** Execute evolved epic_smoke_test_plan.md to verify epic works end-to-end.

**Critical Distinction:**
- **Feature smoke testing (Stage 5c):** Tests individual feature in isolation
- **Epic smoke testing (Stage 6):** Tests ALL features working together as a cohesive system

**Actions:**

**2a. Part 1: Epic-Level Import Tests**

Test that all new modules can be imported together:

```python
# Execute EACH import test from epic_smoke_test_plan.md
python -c "from feature_01 import AdpIntegration; from feature_02 import MatchupSystem; from feature_03 import PerformanceTracker"
```

**Expected:** No import errors, no circular dependencies.

**If imports fail:**
- Document exact error
- Fix import issues
- Re-run Part 1

**2b. Part 2: Epic-Level Entry Point Tests**

Test that epic-level entry points start correctly:

```bash
# Example from epic_smoke_test_plan.md
python run_league_helper.py --mode draft --help
python run_league_helper.py --mode analysis --help
```

**Expected:** Help text displays, no crashes, correct options shown.

**2c. Part 3: Epic End-to-End Execution Tests**

Execute epic-level workflows with REAL data:

**Example Scenario (from epic_smoke_test_plan.md):**
```bash
# Scenario 1: Complete draft workflow with all features
python run_league_helper.py --mode draft --week 1 --iterations 10

# Verify OUTPUT DATA VALUES (not just "file exists"):
# - ADP multipliers applied to all players (feature 01)
# - Matchup difficulty reflected in scores (feature 02)
# - Performance tracking initialized (feature 03)
```

**Critical:** Verify DATA VALUES, not just structure:
- ✅ GOOD: `assert df['adp_multiplier'].between(0.5, 1.5).all()`
- ❌ BAD: "File exists, looks good"

**Execute ALL scenarios** from epic_smoke_test_plan.md.

**2d. Part 4: Cross-Feature Integration Tests**

Execute integration scenarios added during Stage 5e:

**Example Integration Scenario:**
```markdown
### Scenario 7: ADP + Matchup Integration
**Added:** Stage 5e (feature_02_matchup_system)

**What to test:** Verify ADP multipliers don't override matchup difficulty

**How to test:**
1. Run draft mode with both features enabled
2. Find player with high ADP (top 10) facing tough matchup
3. Verify final score shows BOTH effects

**Expected result:**
- Player with ADP=5 (mult≈1.2) + tough matchup (mult≈0.8)
- Final score = base * 1.2 * 0.8 ≈ base * 0.96
```

**Why this matters:** Integration scenarios test feature INTERACTIONS, not individual features.

**If smoke testing finds issues:**
- Document ALL failures
- Fix issues
- RESTART Step 2 (re-run ALL parts)

**Output:** Document results:
```markdown
## Epic Smoke Testing Results (Stage 6)

**Date:** 2025-12-30
**Status:** ✅ PASSED

**Part 1 (Import Tests):** ✅ All imports successful
**Part 2 (Entry Points):** ✅ All entry points start correctly
**Part 3 (E2E Tests):** ✅ All 5 epic scenarios passed with correct data values
**Part 4 (Integration Tests):** ✅ All 3 integration scenarios passed

**Issues Found:** None
```

---

### STEP 3: Epic QC Round 1 (Cross-Feature Integration)

**Objective:** Validate integration points between features work correctly.

**Focus Areas:**

**3a. Integration Point Validation**

Review integration points identified in Stage 4 epic_smoke_test_plan.md:

**Example Integration Points:**
- Feature 01 (ADP) provides `adp_multiplier` → Feature 02 (Matchup) consumes it
- Feature 02 (Matchup) provides `matchup_difficulty` → Feature 03 (Performance) logs it
- Feature 03 (Performance) provides `accuracy_score` → Feature 01 (ADP) adjusts confidence

**Validation Questions:**
- ✅ Do integration points use correct interfaces?
- ✅ Is data passed in expected format?
- ✅ Are edge cases handled (missing data, None values, etc.)?
- ✅ Do features gracefully degrade if dependency unavailable?

**3b. Data Flow Across Features**

Trace data flow through a complete epic workflow:

**Example Trace (Draft Workflow):**
```
User Input (player name, week)
  ↓
Feature 01: Fetch ADP data → Calculate adp_multiplier
  ↓
Feature 02: Fetch matchup data → Calculate matchup_difficulty
  ↓
Feature 03: Fetch historical data → Calculate accuracy_score
  ↓
Combined Scoring: base_score * adp_mult * matchup_mult * accuracy_adj
  ↓
Output: Ranked draft recommendations
```

**Validation:**
- ✅ Trace ACTUAL code paths (not assumed flows)
- ✅ Verify data transformations at each step
- ✅ Check for data loss or corruption between features

**3c. Interface Compatibility**

Review interfaces between features:

**Example Interface Review:**
```python
# Feature 01 provides:
def get_adp_multiplier(player_name: str, position: str) -> Tuple[float, int]:
    """Returns (multiplier, adp_rank)"""

# Feature 02 consumes:
def calculate_matchup_score(player: FantasyPlayer, adp_data: Tuple[float, int]) -> float:
    """Expects (multiplier, rank) tuple"""
```

**Validation:**
- ✅ Type signatures match between provider and consumer
- ✅ Return values documented and understood by consumers
- ✅ Error handling for invalid inputs

**3d. Error Propagation Handling**

Test error propagation across features:

**Example Error Scenario:**
```python
# What happens if Feature 01 fails to fetch ADP data?
# - Does Feature 02 crash?
# - Does epic gracefully degrade?
# - Is error message helpful to user?
```

**Validation:**
- ✅ Errors don't cascade (one feature failure ≠ epic failure)
- ✅ Error messages identify which feature failed
- ✅ Epic continues with degraded functionality (if possible)

**3e. Document Findings**

Create section in epic_lessons_learned.md:

```markdown
## Stage 6 - QC Round 1 Findings (Cross-Feature Integration)

**Integration Points Reviewed:** 5
**Issues Found:** 0
**Status:** ✅ PASSED

**Integration Point Summary:**
- Feature 01 → Feature 02: adp_multiplier passed correctly
- Feature 02 → Feature 03: matchup_difficulty logged correctly
- Feature 03 → Feature 01: accuracy_score adjusts confidence correctly
- All error cases handled gracefully
- No cascade failures observed
```

**If issues found:**
- Document ALL issues
- Create bug fixes
- RESTART Stage 6 after fixes

---

### STEP 4: Epic QC Round 2 (Epic Cohesion & Consistency)

**Objective:** Validate epic maintains consistency across all features.

**Focus Areas:**

**4a. Code Style Consistency**

Review code style across ALL feature implementations:

**Consistency Checks:**
- ✅ Naming conventions consistent (e.g., all use `get_*` for getters)
- ✅ File organization consistent (all features use same structure)
- ✅ Import style consistent (all use same import format)
- ✅ Docstring style consistent (all use Google-style or same format)

**Example Inconsistency:**
```python
# Feature 01 uses:
def get_adp_multiplier(player_name):

# Feature 02 uses:
def fetch_matchup_difficulty(player_name):

# Inconsistency: "get_" vs "fetch_" for similar operations
```

**4b. Naming Convention Consistency**

Review naming across features:

**Consistency Checks:**
- ✅ Similar concepts use similar names (e.g., all use `player_name` not mixed with `player_id`)
- ✅ Abbreviations consistent (e.g., `adp` always lowercase, not mixed with `ADP`)
- ✅ File naming consistent (all features use `{name}_manager.py` or similar)

**4c. Error Handling Consistency**

Review error handling patterns:

**Consistency Checks:**
- ✅ All features use same error classes (e.g., `FantasyFootballError`)
- ✅ Error messages follow same format
- ✅ Logging level consistent for similar error types
- ✅ Error context provided consistently

**Example:**
```python
# Feature 01:
raise DataProcessingError(f"ADP data not found for {player_name}")

# Feature 02:
raise DataProcessingError(f"Matchup data not found for {player_name}")

# Feature 03:
raise DataProcessingError(f"Performance data not found for {player_name}")

# ✅ Consistent: Same error class, same message format
```

**4d. Architectural Pattern Consistency**

Review architectural patterns:

**Consistency Checks:**
- ✅ All features use same design patterns (e.g., Manager pattern)
- ✅ Data access patterns consistent (all use CSV utils or all use direct file access)
- ✅ Configuration access consistent (all use ConfigManager)
- ✅ Testing approach consistent (all use same test structure)

**4e. Document Findings**

Update epic_lessons_learned.md:

```markdown
## Stage 6 - QC Round 2 Findings (Epic Cohesion & Consistency)

**Consistency Areas Reviewed:** 4 (code style, naming, error handling, architecture)
**Issues Found:** 1 (minor naming inconsistency)
**Status:** ⚠️ MINOR ISSUES (fixed before proceeding)

**Findings:**
- Code style: Consistent across all features ✅
- Naming conventions: Minor inconsistency in "get_" vs "fetch_" (fixed) ⚠️
- Error handling: Consistent error classes and formats ✅
- Architecture: All features use Manager pattern consistently ✅

**Actions Taken:**
- Renamed fetch_matchup_difficulty to get_matchup_difficulty
- Re-ran unit tests (100% pass)
```

**If MAJOR issues found:**
- Document ALL issues
- Create bug fixes
- RESTART Stage 6 after fixes

**If MINOR issues found:**
- Fix immediately
- Re-run affected tests
- Document fixes
- Continue to Step 5 (no restart needed)

---

### STEP 5: Epic QC Round 3 (End-to-End Success Criteria)

**Objective:** Validate epic achieves original goals and meets success criteria.

**Focus Areas:**

**5a. Validate Against Original Epic Request**

Re-read original {epic_name}.txt request:

**Example Request:**
```
Epic Request: Improve Draft Helper System

Goals:
- Integrate ADP data for market wisdom ← Did we achieve this?
- Add matchup-based projections ← Did we achieve this?
- Track player performance vs projections ← Did we achieve this?

Expected Outcome:
User can make better draft decisions by seeing:
1. Market consensus (ADP) ← Is this visible in output?
2. Matchup difficulty ← Is this visible in output?
3. Historical accuracy of projections ← Is this visible in output?
```

**Validation:**
- ✅ Read EACH goal from original request
- ✅ Verify implementation achieves goal
- ✅ Check expected outcomes are delivered
- ✅ Compare user's vision to actual implementation

**Create validation table:**

| Original Goal | Achieved? | Evidence |
|---------------|-----------|----------|
| Integrate ADP data | ✅ YES | Feature 01 implemented, tested in Stage 5c, ADP multipliers visible in output |
| Add matchup projections | ✅ YES | Feature 02 implemented, matchup difficulty shown in recommendations |
| Track performance | ✅ YES | Feature 03 implemented, accuracy scores logged and displayed |

**5b. Verify Epic Success Criteria (from Stage 4)**

Re-read epic_smoke_test_plan.md "Epic Success Criteria" section:

**Example Success Criteria:**
```markdown
## Epic Success Criteria

**Must Have:**
1. Draft recommendations include ADP multipliers
2. Matchup difficulty reflected in final scores
3. Performance tracking data persisted to CSV

4. Cross-feature integration: All 3 features work together
5. User can see all 3 data sources in output
6. Performance comparison shows accuracy trends
```

**CRITICAL:** ALL success criteria are REQUIRED. If a criterion was in the original epic request or spec, it MUST be met 100%. There are NO "nice to have" or "optional" requirements - everything in the spec is mandatory.

**Validation:**
- ✅ Verify ALL success criteria met (100% required)
- ⚠️ If ANY criterion not met → Create bug fix OR get user approval to remove from scope
- ❌ Do NOT leave requirements unimplemented and "documented for future"

**5c. User Experience Flow Validation**

Execute COMPLETE user workflows:

**Example User Workflow:**
```bash
# User Story: Draft a quarterback for Week 5

1. User runs: python run_league_helper.py --mode draft --position QB --week 5
2. System displays:
   - Player rankings
   - ADP ranks (feature 01)
   - Matchup difficulty (feature 02)
   - Historical accuracy (feature 03)
3. User selects player
4. System provides recommendation with all data sources visible
```

**Validation:**
- ✅ Workflow is SMOOTH (no confusing steps)
- ✅ Output is CLEAR (user understands all data)
- ✅ Errors are HELPFUL (user knows what to fix)
- ✅ Performance is ACCEPTABLE (no long waits)

**5d. Performance Characteristics**

Test performance with realistic data:

**Example Performance Tests:**
```bash
# Test with full dataset (all players, all weeks)
time python run_league_helper.py --mode draft --week 5

# Expected: < 5 seconds for full draft recommendation
```

**Validation:**
- ✅ Epic completes in acceptable time
- ✅ No memory issues with full dataset
- ✅ No performance regressions from baseline (before epic)

**5e. Document Findings**

Update epic_lessons_learned.md:

```markdown
## Stage 6 - QC Round 3 Findings (End-to-End Success Criteria)

**Original Goals Validated:** 3/3 ✅
**Success Criteria Met:** 6/6 ✅
**Status:** ✅ PASSED

**Original Goal Validation:**
- Goal 1 (ADP integration): ✅ Fully achieved
- Goal 2 (Matchup projections): ✅ Fully achieved
- Goal 3 (Performance tracking): ✅ Fully achieved

**Success Criteria Met:**
- Criterion 1 (ADP in recommendations): ✅ Met
- Criterion 2 (Matchup in scores): ✅ Met
- Criterion 3 (Performance tracking CSV): ✅ Met
- Criterion 4 (Cross-feature integration): ✅ Met
- Criterion 5 (All data visible): ✅ Met
- Criterion 6 (Accuracy trends): ✅ Met

**CRITICAL RULE:** ALL success criteria must be met 100%. If any criterion cannot be met, get user approval to remove it from scope - do NOT leave it unimplemented.

**User Experience:**
- Workflow smooth and intuitive ✅
- Output clear and comprehensive ✅
- Performance acceptable (3.2s for full draft) ✅
```

**If success criteria NOT met:**
- Document which criteria failed
- Determine if this is acceptable (ask user if unclear)
- If NOT acceptable → Create bug fixes, RESTART Stage 6

---

### STEP 6: Epic PR Review (11 Categories - Epic Scope)

**Objective:** Apply PR review checklist to epic-wide changes with focus on architectural consistency.

**Critical Note:** This is the SAME 11-category checklist from Stage 5c, but applied to:
- Epic-wide changes (not individual features)
- Architectural consistency across features
- Cross-feature impacts

**PR Review Categories:**

**6a. Correctness (Epic Level)**
- ✅ All features implement requirements correctly
- ✅ Cross-feature workflows produce correct results
- ✅ Integration points function correctly
- ✅ No logic errors in epic-wide flows

**6b. Code Quality (Epic Level)**
- ✅ Code quality consistent across all features
- ✅ No duplicate code between features that should be shared
- ✅ Abstractions appropriate for epic complexity
- ✅ Readability consistent across epic

**6c. Comments & Documentation (Epic Level)**
- ✅ Epic-level documentation complete (EPIC_README.md)
- ✅ Cross-feature interactions documented
- ✅ Integration points documented
- ✅ Epic success criteria documented

**6d. Code Organization & Refactoring (Epic Level)**
- ✅ Feature organization consistent
- ✅ Shared utilities extracted (not duplicated)
- ✅ Epic folder structure logical
- ✅ No refactoring opportunities missed

**6e. Testing (Epic Level)**
- ✅ Epic-level integration tests exist
- ✅ Cross-feature scenarios tested
- ✅ All unit tests passing (100%)
- ✅ Test coverage adequate for epic

**6f. Security (Epic Level)**
- ✅ No security vulnerabilities in epic workflows
- ✅ Input validation consistent across features
- ✅ No sensitive data exposed
- ✅ Error messages don't leak internals

**6g. Performance (Epic Level)**
- ✅ Epic performance acceptable
- ✅ No performance regressions from baseline
- ✅ Cross-feature calls optimized
- ✅ No N+1 queries or similar issues

**6h. Error Handling (Epic Level)**
- ✅ Error handling consistent across features
- ✅ Errors propagate correctly between features
- ✅ User-facing errors helpful
- ✅ Epic degrades gracefully on errors

**6i. Architecture (Epic Level - CRITICAL)**
- ✅ Epic architecture coherent
- ✅ Feature separation appropriate
- ✅ Interfaces between features clean
- ✅ No architectural inconsistencies
- ✅ Design patterns applied consistently
- ✅ Epic maintainable and extensible

**6j. Backwards Compatibility (Epic Level)**
- ✅ Epic doesn't break existing functionality
- ✅ Migration path clear (if breaking changes)
- ✅ Deprecated features handled correctly
- ✅ Version compatibility maintained

**6k. Scope & Changes (Epic Level)**
- ✅ Epic scope matches original request
- ✅ No scope creep (undocumented features)
- ✅ All changes necessary for epic
- ✅ No unrelated changes included

**Document PR Review Results:**

```markdown
## Stage 6 - Epic PR Review (11 Categories)

**Date:** 2025-12-30
**Reviewer:** Claude Agent
**Epic:** improve_draft_helper

**Review Results:**

| Category | Status | Notes |
|----------|--------|-------|
| 1. Correctness | ✅ PASS | All cross-feature workflows correct |
| 2. Code Quality | ✅ PASS | Consistent quality across features |
| 3. Comments & Docs | ✅ PASS | Epic-level docs complete |
| 4. Organization | ✅ PASS | Consistent structure, utilities extracted |
| 5. Testing | ✅ PASS | Epic integration tests exist and pass |
| 6. Security | ✅ PASS | No vulnerabilities identified |
| 7. Performance | ✅ PASS | 3.2s for full draft (acceptable) |
| 8. Error Handling | ✅ PASS | Consistent error handling, graceful degradation |
| 9. Architecture | ✅ PASS | Coherent architecture, clean interfaces |
| 10. Compatibility | ✅ PASS | No breaking changes, existing features work |
| 11. Scope | ✅ PASS | Scope matches original request |

**Overall Status:** ✅ APPROVED

**Issues Found:** 0
**Recommendations:** None
```

**If ANY category fails:**
- Document specific issues
- Create bug fixes for failures
- RESTART Stage 6 after fixes

---

### STEP 7: Handle Issues (If Any Discovered)

**Objective:** Create bug fixes for any epic-level integration issues discovered during Stage 6.

**7a. Document ALL Issues**

If ANY issues discovered in Steps 2-6, document comprehensively:

```markdown
## Stage 6 Issues Found

**Date:** 2025-12-30

**Issue 1: Cross-Feature Data Type Mismatch**
- **Discovered In:** QC Round 1 (Integration Point Validation)
- **Description:** Feature 01 returns adp_multiplier as float, Feature 02 expects Tuple[float, int]
- **Impact:** HIGH - Integration point fails
- **Root Cause:** Interface changed during Feature 02 implementation, Feature 01 not updated
- **Fix Required:** Update Feature 01 to return (multiplier, rank) tuple

**Issue 2: Inconsistent Error Messages**
- **Discovered In:** QC Round 2 (Consistency Check)
- **Description:** Feature 01 uses "Player not found", Feature 02 uses "No player data"
- **Impact:** LOW - User confusion
- **Root Cause:** Different developers (agents) implemented features
- **Fix Required:** Standardize error messages across features
```

**7b. Create Bug Fixes**

For EACH issue, create a bug fix using the bug fix workflow:

**Use STAGE_5_bug_fix_workflow_guide.md:**

1. Present issue to user (get approval to create bug fix)
2. Create bugfix_high_{name}/ folder in epic directory
3. Create notes.txt with issue description
4. User verifies notes
5. Update EPIC_README.md to show Stage 6 paused for bug fix
6. Run bug fix through workflow: Stage 2 → 5a → 5b → 5c
7. Bug fix stays in epic folder (doesn't move to done/)

**Priority Determination:**
- **high:** Issue breaks epic functionality → Interrupt Stage 6 immediately
- **medium:** Issue affects quality but not functionality → Complete current step first
- **low:** Issue is cosmetic or minor → Document for future (don't create bug fix during Stage 6)

**7c. RESTART Stage 6 After Bug Fixes**

After ALL bug fixes complete:

**CRITICAL:** You MUST COMPLETELY RESTART Stage 6

**Restart Protocol:**
1. Mark all Stage 6 steps as "incomplete" in EPIC_README.md
2. Re-run STEP 2 (Epic Smoke Testing) - all 4 parts
3. Re-run STEP 3 (QC Round 1)
4. Re-run STEP 4 (QC Round 2)
5. Re-run STEP 5 (QC Round 3)
6. Re-run STEP 6 (Epic PR Review)

**Why COMPLETE restart?**
- Bug fixes may have affected areas already checked
- Cannot assume previous QC results still valid
- Ensures epic-level quality maintained

**Document restart:**

```markdown
## Stage 6 Restart Log

**Restart Date:** 2025-12-30
**Reason:** 2 bug fixes completed (bugfix_high_interface_mismatch, bugfix_medium_error_messages)

**Restart Actions:**
- ✅ Re-ran Epic Smoke Testing (all 4 parts) - PASSED
- ✅ Re-ran QC Round 1 - PASSED
- ✅ Re-ran QC Round 2 - PASSED
- ✅ Re-ran QC Round 3 - PASSED
- ✅ Re-ran Epic PR Review - PASSED

**Result:** Stage 6 complete after restart
```

---

### STEP 8: Final Verification & README Update

**Objective:** Verify Stage 6 complete, update epic documentation.

**8a. Verify All Issues Resolved**

Review Stage 6 documentation:

**Verification Checklist:**
- [ ] Epic smoke testing passed (all 4 parts)
- [ ] QC Round 1 passed (no integration issues)
- [ ] QC Round 2 passed (no consistency issues)
- [ ] QC Round 3 passed (success criteria met)
- [ ] Epic PR review passed (all 11 categories)
- [ ] NO pending issues or bug fixes
- [ ] ALL tests passing (100% pass rate)

**If ANY item unchecked:**
- STOP - Stage 6 is NOT complete
- Address remaining issues
- Re-run affected steps

**8b. Update EPIC_README.md Epic Progress Tracker**

Mark Stage 6 complete:

```markdown
## Epic Progress Tracker

**Stage 6 - Epic Final QC:** ✅ COMPLETE
- Epic smoke testing passed: ✅
- Epic QC rounds passed: ✅
- Epic PR review passed: ✅
- End-to-end validation passed: ✅
- Date completed: 2025-12-30
```

**8c. Update epic_lessons_learned.md**

Add Stage 6 insights:

```markdown
## Stage 6 Lessons Learned (Epic Final QC)

**What Went Well:**
- Epic smoke test plan (evolved through Stage 5e) was comprehensive
- Integration points well-defined made QC easier
- Consistent architecture across features simplified review

**What Could Be Improved:**
- Could have caught interface mismatch earlier with better Stage 5d alignment
- Need stronger typing to prevent type mismatches

**Insights for Future Epics:**
- Establish interface contracts early (Stage 2 deep dives)
- Review integration points after EACH feature (Stage 5d)
- Run mini epic smoke tests after each feature (don't wait for Stage 6)

**Guide Improvements Needed:**
- None identified - Stage 6 guide worked well
```

**8d. Mark Stage 6 Complete in EPIC_README.md**

Update "Agent Status" section:

```markdown
## Agent Status

**Last Updated:** 2025-12-30 15:45
**Current Stage:** Stage 6 - Epic Final QC
**Status:** ✅ COMPLETE
**Next Stage:** STAGE_7_epic_cleanup_guide.md

**Stage 6 Summary:**
- Epic smoke testing: ✅ PASSED
- QC rounds (3): ✅ ALL PASSED
- Epic PR review: ✅ PASSED
- Issues found: 2 (both fixed via bug fixes)
- Result: Epic ready for cleanup and move to done/

**Next Action:** Read STAGE_7_epic_cleanup_guide.md
```

**Completion Indicator:**

Stage 6 is COMPLETE when:
- ✅ All 8 steps finished
- ✅ No pending issues or bug fixes
- ✅ EPIC_README.md updated
- ✅ epic_lessons_learned.md updated
- ✅ Ready to proceed to Stage 7

---

## Re-Reading Checkpoints

**You MUST re-read this guide when:**

1. **After Session Compaction**
   - Conversation compacted while in Stage 6
   - Re-read to restore context
   - Check EPIC_README.md Agent Status to see which step you're on

2. **After Creating Bug Fixes**
   - Bug fixes created during Stage 6
   - Re-read "STEP 7: Handle Issues" section
   - Remember: MUST RESTART Stage 6 after bug fixes

3. **After Extended Break (>24 hours)**
   - Returning to epic after break
   - Re-read guide to refresh requirements
   - Verify prerequisites still met

4. **When Encountering Confusion**
   - Unsure about next step
   - Re-read workflow overview and current step
   - Check EPIC_README.md for current status

5. **Before Starting Each QC Round**
   - Re-read the specific QC round section
   - Refresh focus areas for that round
   - Ensure thorough coverage

**Re-Reading Protocol:**
1. Use Read tool to load ENTIRE guide
2. Find current step in EPIC_README.md Agent Status
3. Read "Workflow Overview" section
4. Read current step's detailed workflow
5. Proceed with renewed understanding

---

## Completion Criteria

**Stage 6 is COMPLETE when ALL of the following are true:**

### Epic Smoke Testing
- [ ] Part 1 (Import Tests): ✅ PASSED
- [ ] Part 2 (Entry Point Tests): ✅ PASSED
- [ ] Part 3 (E2E Execution Tests): ✅ PASSED with correct data values
- [ ] Part 4 (Cross-Feature Integration Tests): ✅ PASSED

### QC Rounds
- [ ] QC Round 1 (Cross-Feature Integration): ✅ PASSED
- [ ] QC Round 2 (Epic Cohesion & Consistency): ✅ PASSED
- [ ] QC Round 3 (End-to-End Success Criteria): ✅ PASSED

### Epic PR Review
- [ ] All 11 categories reviewed: ✅ PASSED
- [ ] Architectural consistency validated: ✅ PASSED
- [ ] No issues requiring bug fixes

### Documentation
- [ ] epic_lessons_learned.md updated with Stage 6 insights
- [ ] EPIC_README.md Epic Progress Tracker updated
- [ ] EPIC_README.md Agent Status shows Stage 6 complete

### Bug Fixes (if any)
- [ ] All bug fixes created and completed (Stage 5c)
- [ ] Stage 6 RESTARTED after bug fixes
- [ ] All steps re-run and passed

### Final Verification
- [ ] All unit tests passing (100%)
- [ ] No pending issues
- [ ] Original epic goals validated and achieved
- [ ] Ready to proceed to Stage 7

**DO NOT proceed to Stage 7 until ALL completion criteria are met.**

---

## Common Mistakes to Avoid

**Anti-Pattern Recognition:**

### ❌ MISTAKE 1: "Features passed Stage 5c, epic testing is redundant"

**Why this is wrong:**
- Feature-level testing (5c) validates features in ISOLATION
- Epic-level testing (6) validates features TOGETHER
- Integration issues only appear when features interact

**What to do instead:**
- ✅ Execute epic smoke testing THOROUGHLY
- ✅ Focus on cross-feature workflows
- ✅ Test integration points explicitly

---

### ❌ MISTAKE 2: "Using original epic_smoke_test_plan.md from Stage 1"

**Why this is wrong:**
- Stage 1 plan based on ASSUMPTIONS (no code yet)
- Plan evolved through Stage 4 (deep dive findings) and Stage 5e (actual implementation)
- Original plan likely outdated and inaccurate

**What to do instead:**
- ✅ Use EVOLVED epic_smoke_test_plan.md
- ✅ Check "Last Updated" timestamp (should be recent Stage 5e)
- ✅ Verify plan includes integration scenarios

---

### ❌ MISTAKE 3: "Checking file existence instead of data values"

**Why this is wrong:**
- File can exist but contain incorrect data
- Structure can be correct but values wrong
- Smoke testing must verify ACTUAL DATA

**What to do instead:**
- ✅ Open files and check data values
- ✅ Verify calculations are correct
- ✅ Assert specific value ranges (e.g., `assert df['score'].between(0, 500).all()`)

---

### ❌ MISTAKE 4: "Skipping QC rounds because smoke testing passed"

**Why this is wrong:**
- Smoke testing validates functionality
- QC rounds validate quality, consistency, and success criteria
- Different focus areas, both mandatory

**What to do instead:**
- ✅ Execute ALL 3 QC rounds
- ✅ Don't combine rounds
- ✅ Document findings from each round separately

---

### ❌ MISTAKE 5: "Fixing issues and continuing Stage 6"

**Why this is wrong:**
- Bug fixes may affect areas already checked
- Cannot assume previous QC results still valid
- Partial Stage 6 completion creates gaps

**What to do instead:**
- ✅ Create bug fixes using bug fix workflow
- ✅ COMPLETELY RESTART Stage 6 after fixes
- ✅ Re-run ALL steps (smoke testing, QC 1-3, PR review)

---

### ❌ MISTAKE 6: "Comparing to specs instead of original epic request"

**Why this is wrong:**
- Specs evolved during implementation
- Specs may have deviated from user's original vision
- Stage 6 validates against USER'S GOALS, not intermediate specs

**What to do instead:**
- ✅ Re-read ORIGINAL {epic_name}.txt file
- ✅ Validate against user's stated goals
- ✅ Verify expected outcomes delivered

---

### ❌ MISTAKE 7: "Applying PR review at feature level"

**Why this is wrong:**
- Stage 5c already did feature-level PR review
- Stage 6 PR review focuses on EPIC-WIDE concerns
- Missing architectural consistency across features

**What to do instead:**
- ✅ Focus on epic-wide architectural consistency
- ✅ Review cross-feature impacts
- ✅ Validate design patterns applied consistently

---

### ❌ MISTAKE 8: "Moving features to done/ folder after Stage 6"

**Why this is wrong:**
- Individual features stay in epic folder until Stage 7
- Epic moved to done/ as a WHOLE (not piecemeal)
- Keeps epic together for final verification

**What to do instead:**
- ✅ Leave all features in epic folder
- ✅ Complete Stage 7 (epic cleanup)
- ✅ Move ENTIRE epic folder to done/ in Stage 7

---

## Real-World Examples

### Example 1: Epic Smoke Testing with Integration Scenarios

**Scenario:** Testing "Improve Draft Helper" epic with 3 features (ADP, Matchup, Performance)

**Step 2c: E2E Execution Test**

```bash
# Scenario from epic_smoke_test_plan.md:
python run_league_helper.py --mode draft --week 5 --iterations 10 > output.txt
```

**Verification (GOOD):**
```python
# Read output and verify DATA VALUES
import pandas as pd
df = pd.read_csv('data/draft_recommendations.csv')

# Feature 01 (ADP) - verify multipliers applied
assert df['adp_multiplier'].between(0.5, 1.5).all(), "ADP multipliers out of range"
assert df['adp_rank'].notna().all(), "Missing ADP ranks"

# Feature 02 (Matchup) - verify difficulty calculated
assert df['matchup_difficulty'].between(0.5, 1.5).all(), "Matchup difficulty out of range"

# Feature 03 (Performance) - verify tracking data
perf_df = pd.read_csv('data/performance_tracking.csv')
assert len(perf_df) > 0, "Performance tracking not initialized"

# Integration - verify both features affect final score
player_with_both = df[(df['adp_rank'] < 10) & (df['matchup_difficulty'] < 0.9)].iloc[0]
expected_score = player_with_both['base_score'] * player_with_both['adp_multiplier'] * player_with_both['matchup_difficulty']
assert abs(player_with_both['final_score'] - expected_score) < 0.1, "Integration not working"
```

**Why this is good:**
- Verifies ACTUAL DATA VALUES (not just "file exists")
- Tests integration (both features affect final score)
- Asserts specific conditions
- Catches integration issues

---

### Example 2: QC Round 1 - Integration Point Validation

**Scenario:** Validating Feature 01 → Feature 02 integration point

**Integration Point:**
```python
# Feature 01 provides:
def get_adp_data(player_name: str) -> Tuple[float, int]:
    """Returns (multiplier, adp_rank)"""
    return (1.25, 15)

# Feature 02 consumes:
def calculate_final_score(player, adp_data):
    multiplier, rank = adp_data
    return player.base_score * multiplier
```

**Validation (GOOD):**
```python
# Test integration point with actual code
from feature_01.adp_manager import get_adp_data
from feature_02.matchup_manager import calculate_final_score

# Test happy path
adp_data = get_adp_data("Patrick Mahomes")
assert isinstance(adp_data, tuple), "Interface broken - not returning tuple"
assert len(adp_data) == 2, "Interface broken - wrong tuple length"

# Test consumption
from league_helper.util.FantasyPlayer import FantasyPlayer
player = FantasyPlayer("Patrick Mahomes", "QB", 300.0)
score = calculate_final_score(player, adp_data)
assert score > 0, "Integration produces invalid score"

# Test error case
try:
    adp_data = get_adp_data("NonexistentPlayer")
except DataProcessingError as e:
    # Expected - verify error message helpful
    assert "not found" in str(e).lower()
```

**Why this is good:**
- Tests with ACTUAL code (not assumed interfaces)
- Verifies interface contract (type, structure)
- Tests error cases
- Validates integration produces correct results

---

### Example 3: QC Round 3 - Original Epic Request Validation

**Scenario:** Validating epic achieves original goals

**Original Request (epic_name.txt):**
```
Epic Request: Improve Draft Helper System

Goals:
1. Integrate ADP data for market wisdom
2. Add matchup-based projections
3. Track player performance vs projections

Expected Outcome:
User can make better draft decisions by seeing:
- Market consensus (ADP)
- Matchup difficulty
- Historical accuracy of projections
```

**Validation (GOOD):**

Create validation table:

| Original Goal | Achieved? | Evidence | Gap (if any) |
|---------------|-----------|----------|--------------|
| 1. Integrate ADP data | ✅ YES | Feature 01 implemented, ADP multipliers in output, adp_rank column present | None |
| 2. Add matchup projections | ✅ YES | Feature 02 implemented, matchup_difficulty in output | None |
| 3. Track performance | ✅ YES | Feature 03 implemented, performance_tracking.csv created, accuracy_score calculated | None |
| Expected: Show market consensus | ✅ YES | Output includes `adp_rank` column (e.g., "Rank: 15") | None |
| Expected: Show matchup difficulty | ✅ YES | Output includes `matchup_difficulty` (e.g., "0.85 (Tough)") | None |
| Expected: Show historical accuracy | ⚠️ PARTIAL | Accuracy score calculated but not shown in draft output | Shows in separate report, not inline |

**Actions:**
- 3 core goals: ✅ Fully achieved
- 2 expected outcomes: ✅ Fully achieved
- 1 expected outcome: ⚠️ Partially achieved (accuracy not inline)

**Decision:** Ask user if partial achievement acceptable or needs bug fix:
- Option 1: Accept as-is (accuracy available in separate report)
- Option 2: Create bug fix to show accuracy inline in draft output

**Why this is good:**
- Compares to ORIGINAL request (not evolved specs)
- Validates EACH stated goal
- Identifies gaps transparently
- Asks user for decision on partial achievement

---

### Example 4: Handling Issues Found During Stage 6

**Scenario:** QC Round 1 finds integration issue

**Issue Found:**
```markdown
## Stage 6 Issue: Interface Type Mismatch

**Discovered In:** QC Round 1 (Step 3a - Integration Point Validation)

**Description:**
Feature 01 returns `adp_multiplier` as `float`
Feature 02 expects `adp_data` as `Tuple[float, int]`
Integration fails when Feature 02 tries to unpack: `multiplier, rank = adp_data`

**Root Cause:**
During Feature 02 implementation (Stage 5b), interface was enhanced to include rank
Feature 01 was not updated (should have been caught in Stage 5d alignment)

**Impact:** HIGH - Epic smoke testing will fail on cross-feature scenarios

**Fix Required:**
Update Feature 01 `get_adp_multiplier()` to return tuple `(multiplier, rank)`
```

**Actions Taken (GOOD):**

1. **Present to user:**
   "I found an integration issue during Stage 6 QC Round 1. Feature 01 and Feature 02 have incompatible interfaces. This needs a bug fix before Stage 6 can complete. Should I create a bug fix?"

2. **Create bug fix folder:**
   ```
   bugfix_high_adp_interface_mismatch/
   ├── notes.txt
   ├── spec.md
   ├── checklist.md
   ├── todo.md
   ├── code_changes.md
   ├── lessons_learned.md
   └── README.md
   ```

3. **Update EPIC_README.md:**
   ```markdown
   ## Agent Status
   **Status:** Stage 6 PAUSED for bug fix (bugfix_high_adp_interface_mismatch)
   **Paused At:** QC Round 1 (Integration Point Validation)
   **Next Action:** Complete bug fix, then RESTART Stage 6
   ```

4. **Run bug fix through workflow:**
   - Stage 2 (Deep Dive): Understand interface mismatch
   - Stage 5a (TODO): Create fix tasks
   - Stage 5b (Implementation): Update Feature 01 interface
   - Stage 5c (Post-Impl): Smoke test, QC, PR review

5. **RESTART Stage 6:**
   ```markdown
   ## Stage 6 Restart Log
   **Date:** 2025-12-30
   **Reason:** Bug fix bugfix_high_adp_interface_mismatch completed

   **Restart Actions:**
   - ✅ Re-ran Epic Smoke Testing (Part 1-4) - PASSED
   - ✅ Re-ran QC Round 1 - PASSED (interface issue fixed)
   - ✅ Re-ran QC Round 2 - PASSED
   - ✅ Re-ran QC Round 3 - PASSED
   - ✅ Re-ran Epic PR Review - PASSED

   **Result:** Stage 6 complete after restart
   ```

**Why this is good:**
- Issue documented comprehensively
- User informed and approved bug fix
- EPIC_README.md updated for resumability
- Bug fix followed full workflow (not shortcut)
- Stage 6 COMPLETELY RESTARTED (not partially continued)
- Restart documented

---

## README Agent Status Update Requirements

**Update EPIC_README.md Agent Status section at these checkpoints:**

### Checkpoint 1: Starting Stage 6
```markdown
**Current Stage:** Stage 6 - Epic Final QC
**Status:** IN PROGRESS
**Current Step:** Pre-QC Verification
**Last Updated:** 2025-12-30 10:00
**Next Action:** Read epic_smoke_test_plan.md, verify all features at Stage 5e
```

### Checkpoint 2: After Smoke Testing
```markdown
**Current Stage:** Stage 6 - Epic Final QC
**Status:** IN PROGRESS
**Current Step:** QC Round 1 (Cross-Feature Integration)
**Last Updated:** 2025-12-30 10:30
**Progress:** Smoke testing ✅ PASSED
**Next Action:** Validate integration points between features
```

### Checkpoint 3: After QC Rounds
```markdown
**Current Stage:** Stage 6 - Epic Final QC
**Status:** IN PROGRESS
**Current Step:** Epic PR Review (11 Categories)
**Last Updated:** 2025-12-30 11:30
**Progress:**
- Smoke testing ✅ PASSED
- QC Round 1 ✅ PASSED
- QC Round 2 ✅ PASSED
- QC Round 3 ✅ PASSED
**Next Action:** Execute epic-level PR review
```

### Checkpoint 4: Issue Found (Bug Fix Required)
```markdown
**Current Stage:** Stage 6 - Epic Final QC
**Status:** PAUSED (bug fix in progress)
**Paused At:** QC Round 1 (Integration Point Validation)
**Last Updated:** 2025-12-30 11:00
**Bug Fix:** bugfix_high_adp_interface_mismatch (Stage 5b)
**Next Action:** Complete bug fix, then RESTART Stage 6
```

### Checkpoint 5: Stage 6 Complete
```markdown
**Current Stage:** Stage 6 - Epic Final QC
**Status:** ✅ COMPLETE
**Completed:** 2025-12-30 15:00
**Summary:**
- Epic smoke testing: ✅ PASSED
- QC rounds (3): ✅ ALL PASSED
- Epic PR review: ✅ PASSED
- Issues found: 2 (both fixed via bug fixes)
- Stage 6 restarts: 1 (after bug fixes)
**Next Stage:** STAGE_7_epic_cleanup_guide.md
**Next Action:** Read STAGE_7_epic_cleanup_guide.md to begin final cleanup
```

---

## Prerequisites for Next Stage

**Before proceeding to Stage 7 (Epic Cleanup), verify:**

### Stage 6 Completion
- [ ] ALL 8 steps of Stage 6 complete
- [ ] Epic smoke testing passed (all 4 parts)
- [ ] QC rounds 1, 2, 3 all passed
- [ ] Epic PR review passed (all 11 categories)
- [ ] No pending issues or bug fixes

### Documentation Complete
- [ ] epic_lessons_learned.md updated with Stage 6 insights
- [ ] EPIC_README.md shows Stage 6 complete
- [ ] All bug fix folders (if any) show Stage 5c complete

### Quality Gates Passed
- [ ] All unit tests passing (100%)
- [ ] Original epic goals validated
- [ ] Epic success criteria met
- [ ] End-to-end workflows validated

**Only proceed to Stage 7 when ALL items are checked.**

---

## Summary

**Stage 6 - Epic-Level Final QC validates the ENTIRE epic as a cohesive whole:**

**Key Activities:**
1. Execute evolved epic_smoke_test_plan.md (not original)
2. Run 3 epic-level QC rounds (integration, consistency, success criteria)
3. Apply PR review to epic-wide changes (11 categories)
4. Validate against original epic request
5. Create bug fixes for any issues, RESTART Stage 6

**Critical Distinctions:**
- **Feature testing (5c):** Tests features in isolation
- **Epic testing (6):** Tests features working together, integration points, cross-feature workflows

**Success Criteria:**
- Epic smoke testing passed (all 4 parts with correct data values)
- 3 QC rounds passed (no integration/consistency/success issues)
- Epic PR review passed (all 11 categories)
- Original epic goals achieved
- No pending issues or bug fixes

**Common Pitfalls:**
- Using original test plan instead of evolved plan
- Checking file existence instead of data values
- Skipping QC rounds ("smoke testing is enough")
- Continuing after finding issues (must RESTART after bug fixes)
- Comparing to specs instead of original epic request

**Next Stage:** STAGE_7_epic_cleanup_guide.md - Final commits and move epic to done/

**Remember:** Stage 6 is the FINAL VALIDATION before epic completion. Thoroughness here prevents post-completion issues and ensures epic delivers on user's original vision.

---

**END OF STAGE 6 GUIDE**
