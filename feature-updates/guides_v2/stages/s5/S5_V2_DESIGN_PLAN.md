# S5 Version 2: Validation Loop Integration Plan

**Created:** 2026-02-09
**Purpose:** Redesign S5 Implementation Planning using Validation Loop protocol
**Target:** Reduce from 22 iterations to single comprehensive validation loop
**Quality:** Maintain all 150+ unique checks, improve thoroughness

---

## 🎯 EXECUTIVE SUMMARY

### Current State (S5 v1)
- **Structure:** 22 iterations across 3 rounds
- **Time:** 9-11 hours
- **Issues:** Redundant re-verifications, no systematic validation, potential for skipped checks

### Proposed State (S5 v2)
- **Structure:** 2-phase approach with Validation Loop
- **Time:** 4.5-7 hours typical (6-8 rounds), worst case 6-8 hours (10 rounds)
- **Benefits:** Systematic validation, no skipped checks, quality guarantee through 3 consecutive clean rounds

---

## 📐 S5 V2 ARCHITECTURE

### Phase 1: Draft Creation (60-90 minutes)
**Goal:** Create initial implementation_plan.md with all required sections

**Process:**
1. **Use template:** Copy `templates/implementation_plan_template.md` to feature folder
2. **Add implementation tasks:** For each spec.md requirement, create task with basic acceptance criteria
3. **Map dependencies (quick pass):** List external dependencies, defer detailed interface verification to validation loop
4. **Create algorithm traceability matrix (initial):** Map spec algorithms to tasks, aim for 70% coverage minimum
5. **Document data flow (initial):** High-level flow diagram showing entry → processing → output
6. **List error cases and edge cases (initial):** Enumerate obvious errors/edges, defer deep analysis to validation loop

**Output:** Draft implementation_plan.md with all 11 dimension sections present (quality: ~70%)

**Critical Rule:** This is a DRAFT. Quality bar = "all sections exist with reasonable content." The Validation Loop will systematically refine to 99%+.

**Draft Quality Threshold (When to Stop Phase 1):**
- All 11 dimension sections created in implementation_plan.md
- At least 70% of spec requirements have tasks
- At least 70% of algorithms mapped
- Known gaps documented (will be caught in validation loop)
- Time limit: Stop at 90 minutes even if only 70% complete

---

### Phase 2: Validation Loop (3.5-6 hours, typically 6-8 rounds)
**Goal:** Iteratively refine implementation_plan.md until it passes all criteria

**Process:**
- Apply Validation Loop Protocol (3 consecutive clean rounds required)
- Each round validates implementation_plan.md against 11 validation dimensions
- Fix ALL issues found before next round
- Exit when 3 consecutive rounds find zero issues
- Typical: Rounds 1-3 find issues (decreasing), Rounds 4-6 clean (exit at round 6)
- Worst case: Up to 10 rounds before escalation

**Output:** Validated implementation_plan.md (quality: 99%+)

**After Validation Loop:** Present implementation_plan.md to user for Gate 5 (User Approval) before proceeding to S6

---

## 🔍 THE 11 VALIDATION DIMENSIONS

Each validation round checks implementation_plan.md against these 11 dimensions:

**📍 Where Evidence Goes:**
- **All evidence artifacts go IN implementation_plan.md** (not separate files)
- Each dimension section in implementation_plan.md contains its evidence
- Example: "Algorithm Traceability Matrix" is a section in implementation_plan.md
- Validation Loop Log (separate file) tracks rounds/issues, NOT evidence artifacts

### **Dimension 1: Requirements Completeness**
**What to Check:**
- [ ] Every spec.md requirement has implementation task(s)
- [ ] No orphan tasks (all tasks trace to spec requirements)
- [ ] No scope creep (no tasks for unrequested features)
- [ ] Task numbering sequential with no gaps

**Evidence Required:**
- Requirement-to-task mapping table showing 100% coverage

---

### **Dimension 2: Interface & Dependency Verification**
**What to Check:**
- [ ] All external dependencies identified
- [ ] Every dependency interface verified from ACTUAL source code
- [ ] Method signatures documented with line numbers
- [ ] No assumed interfaces (all copy-pasted from source)
- [ ] Data structure modifications verified as feasible
- [ ] No naming conflicts with existing code

**Evidence Required:**
- Dependency verification table with file:line references

---

### **Dimension 3: Algorithm Traceability**
**What to Check:**
- [ ] EVERY spec algorithm mapped to implementation task
- [ ] Typical: 40+ mappings (main + helper + edge case + error)
- [ ] Each algorithm includes exact spec quote
- [ ] Implementation location specified (file, method, ~line)
- [ ] Matrix completeness verified (count matches)

**Evidence Required:**
- Algorithm Traceability Matrix with 40+ mappings

---

### **Dimension 4: Task Specification Quality** (EMBEDS Gate 3a)
**What to Check:**
- [ ] Every task has requirement reference
- [ ] Every task has acceptance criteria checklist (3+ items)
- [ ] Every task has implementation location (file, method, line)
- [ ] Every task has dependencies documented
- [ ] Every task has test names specified
- [ ] No vague tasks ("handle", "process", "update" without details)

**Evidence Required:**
- 100% of tasks pass specification audit checklist

---

### **Dimension 5: Data Flow & Consumption**
**What to Check:**
- [ ] Entry points identified
- [ ] Complete data flow traced step-by-step
- [ ] **CRITICAL:** Every data load operation has downstream CONSUMPTION verified
- [ ] Data transformations at each step documented
- [ ] No gaps in data flow
- [ ] Output points verified

**Evidence Required:**
- Data flow diagram showing entry → transformations → consumption → output

---

### **Dimension 6: Error Handling & Edge Cases**
**What to Check:**
- [ ] ALL error scenarios enumerated
- [ ] Error handling strategy for each (graceful degradation)
- [ ] ALL edge cases enumerated (data quality, boundary, state, concurrency)
- [ ] Every edge case has handling strategy
- [ ] Every error/edge case has test coverage

**Evidence Required:**
- Error handling table (10+ error scenarios typical)
- Edge case table (15+ edge cases typical)

---

### **Dimension 7: Integration & Compatibility**
**What to Check:**
- [ ] **Integration Gap Check:** Every new method has identified caller
- [ ] No orphan code (code written but never called)
- [ ] Call chains traced end-to-end
- [ ] **Backward Compatibility:** Works with old data formats
- [ ] Migration path documented if breaking changes
- [ ] Configuration compatibility verified

**Evidence Required:**
- Integration verification table (method → caller → call site)
- Backward compatibility analysis

---

### **Dimension 8: Test Coverage Quality**
**What to Check:**
- [ ] Test strategy references S4's test_strategy.md
- [ ] Tests cover ALL code categories/types (e.g., all player positions)
- [ ] Success paths: 100% coverage
- [ ] Failure paths: 100% coverage
- [ ] Edge cases: >90% coverage
- [ ] **Resume/Persistence tests:** Old data format handling verified
- [ ] Overall coverage: >90%

**Evidence Required:**
- Test coverage analysis table showing >90% total coverage

---

### **Dimension 9: Performance & Dependencies**
**What to Check:**
- [ ] Performance impact estimated (baseline vs with feature)
- [ ] Bottlenecks identified (O(n²) algorithms flagged)
- [ ] If regression >20%: optimization tasks added
- [ ] Python package dependencies listed
- [ ] Version compatibility checked (requirements.txt)
- [ ] Configuration changes documented (backward compatible)

**Evidence Required:**
- Performance analysis (baseline → estimated → optimized)
- Dependency version table

---

### **Dimension 10: Implementation Readiness**
**What to Check:**
- [ ] Implementation phased into 4-6 logical phases
- [ ] Each phase has checkpoint and test validation
- [ ] Rollback strategy documented for each phase
- [ ] ALL mocks verified against real interfaces (read source code)
- [ ] 3+ integration tests with REAL objects (no mocks) planned
- [ ] Output consumers validated (format, structure, units)
- [ ] Documentation tasks added (docstrings, ARCHITECTURE.md, etc.)

**Evidence Required:**
- Implementation phasing plan (4-6 phases)
- Mock audit report (all mocks verified)
- Integration test plan (3+ real-object tests)

---

### **Dimension 11: Spec Alignment & Cross-Validation** (EMBEDS Gate 12a)
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
- Cross-dimension validation checklist showing all D1-D10 pass

**Note:** This dimension validates spec alignment and confirms all other dimensions are complete. It does NOT re-check D1-D10 content (already validated in those dimensions).

**⚠️ If spec.md discrepancies found:**
- STOP validation loop immediately
- Document all discrepancies found
- Report to user with question: "Should I update spec.md or implementation_plan.md?"
- After user decision and fixes: RESTART validation loop from Round 1 (spec changes invalidate prior validation)

---

## 🔄 VALIDATION LOOP EXECUTION

### Round Structure

Each round follows this pattern:

```
┌─────────────────────────────────────────────────────────────┐
│                    VALIDATION ROUND N                        │
└─────────────────────────────────────────────────────────────┘

1. Take 2-5 minute break (clear mental model from previous round)

2. Re-read ENTIRE implementation_plan.md
   - Use Read tool (no working from memory)
   - Fresh perspective, assume everything is wrong

3. Check ALL 11 dimensions systematically
   - Use different reading patterns each round
   - Document every issue found (no matter how minor)

4. Report findings: "Round N: X issues found across Y dimensions"

5. If X > 0:
   - Fix ALL issues immediately (no deferring)
   - Update implementation_plan.md
   - RESET consecutive clean counter to 0
   - Proceed to Round N+1

6. If X = 0:
   - Increment consecutive clean counter
   - If counter = 3: EXIT (PASSED)
   - If counter < 3: Proceed to Round N+1
```

### Reading Patterns (Vary by Round)

**Round 1: Sequential + Dimension 1-4 Focus**
- Read implementation_plan.md top to bottom
- Focus on: Requirements, Interfaces, Algorithms, Task Quality
- Check sections exist and are structured correctly

**Round 2: Reverse + Dimension 5-8 Focus**
- Read implementation_plan.md bottom to top
- Focus on: Data Flow, Errors, Integration, Tests
- Look for gaps and inconsistencies

**Round 3: Random Spot-Checks + Dimension 9-11 Focus**
- Random spot-check 5-10 tasks
- Focus on: Performance, Implementation Prep, Spec Alignment
- Verify consistency across plan

**Round 4+: Alternate Patterns**
- Round 4: Sequential again (fresh eyes on whole document)
- Round 5: Focus on recent changes (did fixes introduce issues?)
- Round 6: Cross-section validation (do all sections align?)
- Round 7+: Deep dive into previously clean dimensions

### Example Execution

```text
DRAFT CREATION: 90 minutes
- Created implementation_plan.md with all 11 dimensions
- Quality estimate: ~70% (known gaps but structure complete)

ROUND 1: Dimension scan (30 min)
Issues found: 12
- Dimension 1: Missing 2 requirements (spec.md lines 45, 67)
- Dimension 3: Algorithm matrix only 28 mappings (need 40+)
- Dimension 4: 5 tasks have vague acceptance criteria
- Dimension 5: Data consumption not verified for 3 load operations
- Dimension 7: 2 methods have no identified caller
Action: Fix all 12 issues → Round 2

ROUND 2: Reverse read (35 min)
Issues found: 8
- Dimension 6: Missing error handling for FileNotFoundError
- Dimension 8: Resume/persistence tests not planned
- Dimension 9: Performance analysis shows O(n²) but no optimization plan
- Dimension 10: Mock audit incomplete (only 3 of 5 mocks verified)
Action: Fix all 8 issues → Round 3

ROUND 3: Spot-checks (25 min)
Issues found: 3
- Dimension 11: spec.md contradicts epic notes on error handling
- Dimension 4: Task 15 acceptance criteria not measurable
- Dimension 7: Backward compatibility analysis missing migration path
Action: Fix all 3 issues → Round 4 (RESET counter to 0)

ROUND 4: Full sequential read (30 min)
Issues found: 0
Clean count: 1
Action: Proceed to Round 5

ROUND 5: Fresh perspective (25 min)
Issues found: 0
Clean count: 2
Action: Proceed to Round 6

ROUND 6: Final validation (25 min)
Issues found: 0
Clean count: 3 ✅
Result: PASSED (3 consecutive clean rounds)

TOTAL TIME: 90 min draft + 170 min validation = 4h 20min
QUALITY: 99%+ (validated by 6 rounds, 3 consecutive clean)
```

---

## 📊 COMPARISON: V1 vs V2

### Time Comparison

| Aspect | S5 V1 (Current) | S5 V2 (Proposed) | Savings |
|--------|-----------------|------------------|---------|
| **Structure** | 22 iterations, 3 rounds | 11 dimensions, 1 loop | Simpler |
| **Typical Time** | 9-11 hours | 4.5-7 hours (6-8 rounds) | 35-50% |
| **Worst Case** | 9-11 hours | 6-8 hours (10 rounds) | 20-35% |
| **Quality Checks** | Sequential, skip possible | Systematic, skip impossible | Higher |
| **Exit Criteria** | Complete all iterations | 3 consecutive clean rounds | Stricter |

### Quality Comparison

| Quality Metric | S5 V1 | S5 V2 |
|----------------|-------|-------|
| **Checks Performed** | 150+ (if all done correctly) | 150+ (enforced by loop) |
| **Verification Method** | Agent self-reports completion | 3 consecutive clean rounds prove quality |
| **Issue Detection** | Single pass per iteration | Multiple passes until clean |
| **Fix Quality** | Fixes not re-verified | Fixes verified in subsequent rounds |
| **Confidence Level** | Subjective (agent estimates) | Objective (3 clean rounds) |

### Process Comparison

| Process Aspect | S5 V1 | S5 V2 |
|----------------|-------|-------|
| **Redundant Work** | 3x Algorithm Traceability, 3x Integration Gap | None (consolidated into dimensions) |
| **Re-verification** | Separate iterations 11-14 | Automatic (every round checks all dimensions) |
| **Issue Deferral** | Possible to defer and continue | Impossible (must fix before next round) |
| **Stopping Criteria** | Finish all 22 iterations | 3 consecutive rounds with zero issues |
| **Quality Guarantee** | "I checked everything" | "3 independent validations found nothing" |

---

## 🚀 IMPLEMENTATION PLAN

### Phase 1: Create Validation Loop Guide (4-6 hours)

**Deliverable:** `s5_v2_validation_loop.md` (estimated 600-800 lines)

**Content:**
1. Overview (what S5 v2 is, how it differs from v1) - 50 lines
2. Phase 1: Draft Creation (detailed step-by-step) - 100 lines
3. Phase 2: Validation Loop (detailed process) - 100 lines
4. The 11 Validation Dimensions (full checklists with examples) - 250 lines
5. Round-by-round patterns (what to check when, with examples) - 100 lines
6. Example execution (detailed like above) - 80 lines
7. Common issues and fixes - 60 lines
8. Anti-patterns to avoid - 40 lines
9. Exit criteria and quality metrics - 50 lines

**Time Estimate Rationale:** 600+ line comprehensive guide with detailed checklists and examples = 4-6 hours to write and validate

### Phase 2: Create Validation Loop Template (30 minutes)

**Deliverable:** `VALIDATION_LOOP_LOG_S5_template.md`

**Content:**
```markdown
# S5 Implementation Planning: Validation Loop Log

**Feature:** {feature_name}
**Started:** {timestamp}

## Draft Creation Phase

**Time:** {duration}
**Output:** implementation_plan.md v0.1 (draft)
**Sections Created:** [list all 11 dimensions]

---

## Validation Loop Rounds

### Round 1: {timestamp}

**Reading Pattern:** Sequential, Dimensions 1-4 focus
**Time:** {duration}

**Issues Found:** {count}

| Dimension | Issue | Fix |
|-----------|-------|-----|
| Dimension 1 | Missing requirement R5 | Added task 12 for R5 |
| Dimension 3 | Algorithm matrix incomplete | Added 12 mappings |
| ... | ... | ... |

**All issues fixed:** ✅
**Clean count:** 0 → RESET
**Next:** Round 2

---

### Round 2: {timestamp}

**Reading Pattern:** Reverse, Dimensions 5-8 focus
**Time:** {duration}

**Issues Found:** {count}
[... same structure ...]

---

### Round N: {timestamp}

**Issues Found:** 0 ✅
**Clean count:** 3 consecutive clean rounds
**Status:** PASSED

---

## Final Metrics

**Total Rounds:** {N}
**Total Time:** {duration}
**Issues Found Total:** {count across all rounds}
**Final Quality:** 99%+ (validated by 3 consecutive clean rounds)

---
```

### Phase 3: Update Reference Documents (1 hour)

**Files to Update:**

1. **CLAUDE.md**
   - Update S5 description: "S5 v2: Validation Loop-based Implementation Planning"
   - Update time estimate: "5-7 hours (typical)"
   - Update workflow diagram to show 2-phase approach

2. **EPIC_WORKFLOW_USAGE.md**
   - Add S5 v2 section explaining new approach
   - Update S4→S5→S6 transition workflow
   - Add example validation loop execution

3. **prompts_reference_v2.md**
   - Update "Starting S5" prompt to reference v2 workflow
   - Add prompts for:
     - Starting Draft Creation Phase
     - Starting Validation Loop
     - Reporting Round Results
     - Exiting Validation Loop

4. **mandatory_gates.md**
   - Update Gate 3a and Gate 12a to note they're "embedded" in S5 v2
   - Clarify that Gate 5 (User Approval) remains separate

### Phase 4: Create Migration Guide (1 hour)

**Deliverable:** `S5_V1_TO_V2_MIGRATION.md`

**Content:**
- Side-by-side comparison of v1 vs v2
- What changed and why
- How to use v2 guides
- When to use v1 vs v2 (transition period)
- FAQ for agents switching from v1 to v2

### Phase 5: Pilot Test (1 feature, ~6 hours)

**Process:**
1. Select next feature for implementation (after current work done)
2. Run S5 v2 with validation loop
3. Track time and quality metrics
4. Document lessons learned
5. Refine guides based on findings

**Success Criteria:**
- Time: 5-7 hours (vs 9-11 hours with v1)
- Quality: 3 consecutive clean rounds achieved
- Agent feedback: Clearer workflow, less redundancy
- No missed checks (all 11 dimensions validated)

### Phase 6: Full Rollout (Documentation update, 2 hours)

**Actions:**
1. Mark S5 v1 guides as "DEPRECATED - Use S5 v2"
2. Update README.md in guides_v2/ to feature S5 v2
3. Add S5_V2_DESIGN_PLAN.md to reference/ folder
4. Update stage overview diagram
5. Announce change in CHANGELOG.md

---

## 🔧 FURTHER OPTIMIZATION OPPORTUNITIES

**⏱️ TIMING:** These optimizations are for FUTURE iteration (after pilot test), NOT part of initial S5 v2 rollout.

### Additional Consolidation (Optional - V2.1 Future Enhancement)

**Could merge Dimensions 9-10 into 8:**
- Dimension 8: "Test, Performance & Implementation Prep"
- Combines: Test coverage + Performance + Dependencies + Implementation phases
- Rationale: All relate to "how will we build and verify this"
- Saves: Cognitive overhead of switching between dimensions
- **Result: 11 dimensions → 9 dimensions**

**Could merge Dimensions 1-2:**
- Dimension 1: "Requirements & Dependencies"
- Combines: Requirements coverage + Interface verification
- Rationale: Both verify "what we're building" is correct
- **Result: 9 dimensions → 8 dimensions**

**Final Optimized Structure: 8 Validation Dimensions**

1. **Requirements & Dependencies** (was D1 + D2)
2. **Algorithm Traceability** (was D3)
3. **Task Specification Quality** (was D4, embeds Gate 3a)
4. **Data Flow & Consumption** (was D5)
5. **Error Handling & Edge Cases** (was D6)
6. **Integration & Compatibility** (was D7)
7. **Test, Performance & Implementation** (was D8 + D9 + D10)
8. **Spec Alignment & Cross-Validation** (was D11, embeds Gate 12a)

**Time Impact:** Could reduce validation rounds by 10-15% (fewer dimensions to check)

**Recommendation:** Start with 11 dimensions, optimize to 8 after pilot test if beneficial.

---

## 📈 SUCCESS METRICS FOR S5 V2

### Quantitative Metrics

**Time Efficiency:**
- Target: 4.5-7 hours typical (vs 9-11 hours in v1)
- Worst case: 6-8 hours (vs 9-11 hours in v1)
- Measurement: Track actual time per feature
- Success: 35%+ reduction on average

**Quality Assurance:**
- Target: 3 consecutive clean rounds (zero issues)
- Measurement: Count of issues found in final 3 rounds
- Success: Zero issues in final 3 rounds for all features

**Issue Detection:**
- Target: Catch 100% of planning issues before S6
- Measurement: Issues found in S7 that should have been caught in S5
- Success: <5% of S7 issues are S5 planning failures

### Qualitative Metrics

**Agent Experience:**
- Clearer process (know what to check, when)
- Less redundancy (no 3x re-verification)
- Higher confidence (3 clean rounds prove quality)

**User Experience:**
- Faster time to implementation (S5 → S6 transition)
- Higher implementation success rate (fewer bugs in S6)
- Better documentation quality (validated 6+ times)

### Rollback Criteria

**If S5 v2 doesn't work, revert to v1 if:**
- Takes >8 hours consistently (minimal time savings)
- Validation loop gets stuck (>10 rounds without 3 clean)
- Quality issues increase (more bugs escape to S7)
- Agent feedback is negative (confusing, frustrating)

---

## ❓ FAQ

### Q: Won't the Validation Loop take longer than separate iterations?

**A:** No, because:
- V1 has 3x redundant re-verifications (Iterations 11-14, 19)
- V2 validates everything once per round (no redundancy)
- V1 requires 22 iterations regardless of quality
- V2 exits after 3 clean rounds (could be rounds 4-6, or 6-8)
- Typical: 90min draft + (6-8 rounds × 25-30 min validation) = 4.5-5.5 hours vs 9-11 hours in v1

### Q: What if I find issues in Round 10?

**A:** Escalate to user per Validation Loop Protocol:
- Document pattern of issues
- Ask user to assess: architecture issue? scope issue? misunderstanding?
- User decides: adjust scope, override validation, return to S2, etc.

### Q: How do I know which dimension an issue belongs to?

**A:** Issues can span multiple dimensions:
- Missing requirement → Dimension 1 (Requirements)
- Missing algorithm for that requirement → Dimension 3 (Algorithms)
- Missing task for that algorithm → Dimension 4 (Task Quality)
- Fix all three aspects, count as 3 issues in same round

### Q: Can I skip dimensions that passed in previous rounds?

**A:** No:
- Must check ALL 11 dimensions EVERY round
- Fixes in one dimension can introduce issues in others
- Example: Adding error handling (D6) might miss integration (D7)
- Validation Loop protocol requires checking everything each round

### Q: What counts as "consecutive clean"?

**A:** Rounds N-2, N-1, and N all found zero issues:
- Round 5: 1 issue → Round 6 resets counter to 0
- Round 6: 0 issues → Count = 1 clean
- Round 7: 0 issues → Count = 2 clean
- Round 8: 0 issues → Count = 3 clean → PASSED ✅

### Q: How do I know when the draft is "good enough" to start validation loop?

**A:** Use these thresholds:
- **Minimum:** All 11 dimension sections exist in implementation_plan.md with some content
- **Coverage:** At least 70% of spec requirements have tasks
- **Depth:** At least 70% of algorithms mapped in matrix
- **Time:** Maximum 90 minutes for draft creation (stop even if only 70%)
- **Quality:** Expect ~70% completeness - validation loop will systematically refine to 99%+

**Don't over-invest in draft quality:**
- Draft = "structure exists, major content present, known gaps OK"
- Validation loop will catch everything systematically
- Better to have 70% draft and start validating than 95% draft with no validation

### Q: Can I parallelize dimension checks?

**A:** Within a round, check dimensions in suggested order but you don't need to complete D1 before starting D2:
- **During a round:** Check all 11 dimensions as you read implementation_plan.md (document issues from any dimension as you find them)
- **Between rounds:** Must fix ALL issues from Round N before starting Round N+1 (cannot parallelize rounds)
- **Reading patterns:** "Focus on dimensions 1-4" means "pay extra attention to these" not "only check these"
- **All dimensions checked every round:** Even if focusing on D1-D4, still validate D5-D11 exist and are consistent

**Clarification:**
- Round = single pass through implementation_plan.md checking ALL dimensions
- Within that pass, find issues across all dimensions as you encounter them
- After round, fix all issues found, then start next round

---

## 🎓 LESSONS FROM V1 THAT INFORMED V2

### What Worked in V1
✅ Comprehensive checks (150+ unique verifications)
✅ Mandatory gates preventing progression with known issues
✅ Structured approach (not ad-hoc planning)
✅ Documentation of interfaces from actual source code
✅ Algorithm traceability matrix (prevents missing implementations)

### What Didn't Work in V1
❌ 3x redundant re-verifications (Iterations 11-14, 19)
❌ Sequential iterations without systematic validation
❌ No mechanism to verify fixes didn't introduce new issues
❌ Possible to skip iterations or defer issues
❌ Subjective quality assessment (agent self-reports)

### How V2 Addresses V1 Issues
✅ Consolidated dimensions (no redundancy)
✅ Systematic validation loop (nothing skipped)
✅ Every fix re-verified in subsequent rounds
✅ Impossible to defer (must fix before next round)
✅ Objective quality metric (3 consecutive clean rounds)

---

## 🚦 GO/NO-GO DECISION FOR V2 ROLLOUT

### ✅ GO if:
- [ ] Validation loop guide created and reviewed
- [ ] Template created
- [ ] Reference docs updated
- [ ] Pilot test successful (4.5-7 hours, 3 clean rounds achieved)
- [ ] Agent feedback positive (clearer, less redundant)
- [ ] User approves v2 approach

### ❌ NO-GO if:
- [ ] Pilot test fails (>8 hours or quality issues)
- [ ] Validation loop gets stuck (>10 rounds)
- [ ] Agent finds v2 confusing or frustrating
- [ ] Quality metrics worse than v1
- [ ] User prefers v1 approach

---

## 📝 NEXT STEPS

### Immediate (Current Agent)
1. **Review this plan** - Get user approval for S5 v2 approach
2. **Create validation loop guide** - Current agent implements Phase 1 (s5_v2_validation_loop.md)
3. **Create template** - Current agent implements Phase 2 (VALIDATION_LOOP_LOG_S5_template.md)
4. **Update references** - Current agent implements Phase 3 (CLAUDE.md, etc.)

### Future (After Current Epic Complete)
5. **Pilot test** - Next agent runs S5 v2 on next feature
6. **Iterate** - Current or next agent refines guides based on pilot findings
7. **Full rollout** - Deploy to all future features (update README, mark v1 deprecated)

**Division of Labor:**
- **Current agent (me):** Create guides, templates, update docs (Phases 1-3) = ~6-8 hours
- **Next agent:** Pilot test using new guides (Phase 5) = ~6 hours
- **Either agent:** Iterate and deploy (Phases 6-7) = ~2 hours

---

**This design plan is ready for review and approval. Upon approval, I (current agent) will begin implementation of Phases 1-3.**
