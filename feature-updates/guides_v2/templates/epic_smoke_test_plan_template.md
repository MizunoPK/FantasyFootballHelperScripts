# Epic Smoke Test Plan Template

**Filename:** `epic_smoke_test_plan.md`
**Location:** `feature-updates/KAI-{N}-{epic_name}/epic_smoke_test_plan.md`
**Created:** {YYYY-MM-DD} (Stage 1)
**Updated:** Stage 4 (Epic Testing Strategy), Stage 5e (after each feature)

**Purpose:** Defines how to validate the complete epic end-to-end with specific test scenarios and success criteria.

---

## Template

```markdown
# Epic Smoke Test Plan: {epic_name}

**Purpose:** Define how to validate the complete epic end-to-end

**Created:** {YYYY-MM-DD} (Stage 1)
**Last Updated:** {YYYY-MM-DD} (Stage {X})

---

## Epic Success Criteria

**The epic is successful if:**

1. {Measurable criterion 1}
   - Example: "All 6 position files (QB, RB, WR, TE, K, DST) created in data/player_data/"

2. {Measurable criterion 2}
   - Example: "Each position file contains >100 players with complete stats"

3. {Measurable criterion 3}
   - Example: "Draft recommendations include ADP multipliers and matchup difficulty"

4. {Measurable criterion 4}
   - Example: "Performance tracking data persisted to CSV with accuracy scores"

{Add 3-7 measurable success criteria}

**Epic is considered SUCCESSFUL when ALL criteria above are met.**

---

## Update History

**Track when and why this plan was updated:**

| Date | Stage | Feature | What Changed | Why |
|------|-------|---------|--------------|-----|
| {YYYY-MM-DD} | Stage 1 | (initial) | Initial plan created | Epic planning based on assumptions |
| {YYYY-MM-DD} | Stage 4 | (all features) | Updated based on deep dives | Discovered {N} integration points, refined scenarios |
| {YYYY-MM-DD} | Stage 5e | feature_01 | Added ADP integration scenarios | Feature 1 implementation revealed specific multiplier ranges |
| {YYYY-MM-DD} | Stage 5e | feature_02 | Added matchup cross-check scenarios | Feature 2 integration with Feature 1 needs validation |
| {YYYY-MM-DD} | Stage 5e | feature_03 | Added performance tracking E2E tests | Feature 3 implementation added CSV persistence |

**Current version is informed by:**
- Stage 1: Initial assumptions
- Stage 4: Deep dive findings (Stages 2-3)
- Stage 5e updates: {List features that have updated this plan}

---

## Test Scenarios

**Instructions for Agent:**
- Execute EACH scenario listed below
- Verify ACTUAL DATA VALUES (not just "file exists")
- Document results in Stage 6

---

### Part 1: Epic-Level Import Tests

**Purpose:** Verify all epic modules can be imported together

**Scenario 1: Import All Epic Modules**
```python
python -c "from feature_01.{module} import {Class1}; from feature_02.{module} import {Class2}; from feature_03.{module} import {Class3}"
```

**Expected Result:**
- No import errors
- No circular dependency errors
- All modules load successfully

---

### Part 2: Epic-Level Entry Point Tests

**Purpose:** Verify epic-level entry points start correctly

**Scenario 2: Epic Entry Point Help**
```bash
python run_{epic_main}.py --help
```

**Expected Result:**
- Help text displays correctly
- All expected options shown
- No crashes or errors

**Scenario 3: Epic Entry Point Validation**
```bash
python run_{epic_main}.py --mode {mode1} --option {value}
```

**Expected Result:**
- Entry point starts without errors
- Correct mode activated
- Expected output format

---

### Part 3: Epic End-to-End Execution Tests

**Purpose:** Execute complete epic workflows with REAL data

**Scenario 4: Complete Epic Workflow ({workflow_name})**
```bash
python run_{epic_main}.py --mode {mode} --week {N} --iterations {N}
```

**Expected Result:**
- Command completes successfully (exit code 0)
- Output files created: {list expected files}
- **DATA VERIFICATION (CRITICAL):**
  - File 1: {specific data check - e.g., "df['adp_multiplier'].between(0.5, 1.5).all()"}
  - File 2: {specific data check - e.g., "len(df) > 100"}
  - File 3: {specific data check - e.g., "df['final_score'].notna().all()"}

**Scenario 5: Epic Workflow with Edge Case ({edge_case_name})**
```bash
python run_{epic_main}.py --mode {mode} --{edge_case_flag}
```

**Expected Result:**
- {Expected behavior for edge case}
- Error handling graceful (if expected to fail)
- {Specific validation checks}

{Add 3-5 end-to-end execution test scenarios}

---

### Part 4: Cross-Feature Integration Tests

**Purpose:** Test feature interactions and integration points

**Scenario 6: Feature 01 ↔ Feature 02 Integration**

**Added:** Stage 5e (feature_02_{name})

**What to test:** Verify Feature 01 data correctly consumed by Feature 02

**How to test:**
1. {Step 1 - e.g., "Run Feature 01 to generate ADP data"}
2. {Step 2 - e.g., "Run Feature 02 with ADP data enabled"}
3. {Step 3 - e.g., "Verify both features' effects in final output"}

**Expected result:**
- Feature 01 output: {specific data - e.g., "adp_multiplier calculated for all players"}
- Feature 02 consumption: {specific check - e.g., "final_score reflects both ADP and matchup"}
- Integration point: {specific validation - e.g., "adp_multiplier * matchup_difficulty applied correctly"}

**Scenario 7: Feature 01 ↔ Feature 03 Integration**

**Added:** Stage 5e (feature_03_{name})

**What to test:** Verify Feature 03 tracks Feature 01 data

**How to test:**
1. {Step 1}
2. {Step 2}
3. {Step 3}

**Expected result:**
- {Specific expected outcome}
- {Data validation checks}

**Scenario 8: Three-Way Integration (Features 01, 02, 03)**

**Added:** Stage 5e (feature_03_{name})

**What to test:** Verify all three features work together cohesively

**How to test:**
1. {Step 1 - complete workflow using all features}
2. {Step 2 - verify each feature's contribution}
3. {Step 3 - validate final output}

**Expected result:**
- {Expected final outcome}
- {Data validations showing all three features contributed}

{Add integration scenarios for each feature interaction}

---

## High-Level Test Categories

**Instructions for Agent:**
- These categories are FLEXIBLE - create specific scenarios as needed during Stage 5e/6
- Base scenarios on ACTUAL implementation (not assumptions)

---

### Category 1: Error Handling Validation

**What to test:** Epic handles errors gracefully across all features

**Agent will create scenarios for:**
- Missing data files (each feature)
- Invalid input parameters
- API failures (if applicable)
- Cross-feature error propagation

---

### Category 2: Performance Validation

**What to test:** Epic performance acceptable with realistic data

**Agent will create scenarios for:**
- Full dataset processing time (< {N} seconds)
- Memory usage with large datasets
- No performance regressions from baseline

---

### Category 3: Edge Cases

**What to test:** Epic handles edge cases correctly

**Agent will create scenarios for:**
- {Edge case 1 discovered during implementation}
- {Edge case 2 discovered during implementation}
- {Edge case 3 discovered during implementation}

{Add more categories as needed}

---

## Execution Checklist (For Stage 6)

**Part 1: Import Tests**
- [ ] Scenario 1: Import All Epic Modules - {✅ PASSED / ❌ FAILED}

**Part 2: Entry Point Tests**
- [ ] Scenario 2: Epic Entry Point Help - {✅ PASSED / ❌ FAILED}
- [ ] Scenario 3: Epic Entry Point Validation - {✅ PASSED / ❌ FAILED}

**Part 3: E2E Execution Tests**
- [ ] Scenario 4: Complete Epic Workflow - {✅ PASSED / ❌ FAILED}
- [ ] Scenario 5: Epic Workflow with Edge Case - {✅ PASSED / ❌ FAILED}
- [ ] {Additional scenarios...}

**Part 4: Cross-Feature Integration Tests**
- [ ] Scenario 6: Feature 01 ↔ Feature 02 - {✅ PASSED / ❌ FAILED}
- [ ] Scenario 7: Feature 01 ↔ Feature 03 - {✅ PASSED / ❌ FAILED}
- [ ] Scenario 8: Three-Way Integration - {✅ PASSED / ❌ FAILED}
- [ ] {Additional integration scenarios...}

**Overall Status:** {ALL PASSED / FAILURES - See details above}

---

## Notes

{Optional section for additional context, gotchas, or testing notes}

**Testing Environment:**
- {Required data files}
- {Required configuration}
- {Prerequisites for testing}

**Known Issues:**
- {Issue 1 and workaround}
- {Or: "None"}
```