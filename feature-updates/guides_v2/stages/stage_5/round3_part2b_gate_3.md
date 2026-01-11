# STAGE 5ac Part 2b: Implementation Planning - Round 3 Gate 3 (Iterations 25, 24)

**Part of:** Epic-Driven Development Workflow v2
**Stage:** 5ac - Implementation Planning Round 3
**Sub-Stage:** Part 2b - Gate 3 (Spec Validation, GO/NO-GO Decision)
**Prerequisites:** STAGE_5ac_part2a complete (Iterations 23, 23a)
**Next Stage:** stages/stage_5/implementation_execution.md

---

## 🚨 MANDATORY READING PROTOCOL

**CRITICAL:** You MUST read this ENTIRE guide before starting Part 2b.

**Why this matters:**
- Part 2b contains THE MOST CRITICAL GATE that cannot be skipped
- Iteration 25 prevents Feature 02 catastrophic bug (implementing wrong solution)
- Iteration 24 is FINAL GO/NO-GO decision

**Reading Checkpoint:**
Before proceeding, you must have:
- [ ] Read this ENTIRE guide (use Read tool, not memory)
- [ ] Verified STAGE_5ac_part2a complete (Iterations 23, 23a)
- [ ] Verified Iteration 23a ALL 4 PARTS PASSED
- [ ] Located spec.md, epic notes, epic ticket, spec summary files

**If resuming after session compaction:**
1. Check feature README.md "Agent Status" section for current iteration
2. Re-read this guide from the beginning
3. Continue from documented checkpoint

---

## Quick Start

### What is this sub-stage?

**STAGE_5ac Part 2b - Gate 3** is the final part of Round 3, where you validate spec against ALL user-validated sources and make the final GO/NO-GO implementation decision through 2 critical iterations (25, 24).

**This contains THE CRITICAL GATE:**
- **Gate 3 (Part A):** Iteration 25 - Spec Validation Against Validated Documents (CRITICAL)
- **Gate 3 (Part B):** Iteration 24 - Implementation Readiness Protocol (GO/NO-GO)

### When do you use this guide?

**Use this guide when:**
- Part 2a (STAGE_5ac_part2a) complete
- Iterations 23, 23a done (ALL 4 PARTS PASSED)
- Ready for spec validation and GO/NO-GO decision

**Do NOT use this guide if:**
- Part 2a not complete
- Iteration 23a failed (any of 4 parts)
- Missing Iteration 23a outputs

### What are the key outputs?

1. **Spec Validation Against Validated Documents** (Iteration 25 - CRITICAL GATE)
   - Spec.md verified against epic notes, epic ticket, spec summary
   - Discrepancies identified and resolved
   - Prevents Feature 02 catastrophic bug

2. **GO/NO-GO Decision** (Iteration 24 - FINAL GATE)
   - Implementation readiness assessed
   - Decision: GO or NO-GO
   - Cannot proceed to Stage 5b without GO

### Time estimate

**30-50 minutes** (2 iterations including CRITICAL gate)
- Iteration 25: 20-30 minutes (CRITICAL - spec validation)
- Iteration 24: 10 minutes (decision)

**If discrepancies found in Iteration 25:** +1-2 hours for user discussion and fixes

### Workflow overview

```
STAGE_5ac Part 2b Workflow (Iterations 25, 24)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Prerequisites Met?
  ├─ Part 2a complete (Iterations 23, 23a)
  ├─ Iteration 23a ALL 4 PARTS PASSED
  └─ No blockers
         │
         ▼
┌─────────────────────────────────────────────────┐
│ Iteration 25: Spec Validation vs Validated Docs│
│ (CRITICAL GATE - Prevents wrong implementation)│
│ Validate spec.md against:                      │
│ - Epic notes                                   │
│ - Epic ticket (user-validated)                 │
│ - Spec summary (user-validated)                │
└─────────────────────────────────────────────────┘
         │
    [Zero discrepancies?]
    ├─ YES → Proceed to Iteration 24
    └─ NO → STOP, report to user, await decision
         │
         ▼
┌─────────────────────────────────────────────────┐
│ Iteration 24: Implementation Readiness Protocol│
│ (FINAL GATE - GO/NO-GO DECISION)               │
│ Assess: Confidence, Coverage, Gates            │
│ Decision: GO or NO-GO                          │
└─────────────────────────────────────────────────┘
         │
    [Decision = GO?]
    ├─ YES → Part 2b COMPLETE → Proceed to Stage 5b
    └─ NO → Fix blockers, re-run Iteration 24
```

---

## Critical Rules for Part 2b

```
┌─────────────────────────────────────────────────────────────┐
│ CRITICAL RULES - Part 2b (Gate 3)                           │
└─────────────────────────────────────────────────────────────┘

1. ⚠️ BOTH iterations in Part 2b are MANDATORY (no skipping)
   - Iterations 25, 24 are FINAL gates
   - Skipping gates causes catastrophic failures

2. ⚠️ Iteration 25 prevents implementing wrong solution (Feature 02 bug)
   - MUST validate spec.md against ALL validated sources
   - If discrepancies found → STOP and report to user
   - User decides: restart TODO OR fix and continue
   - CANNOT proceed to Iteration 24 without passing Iteration 25

3. ⚠️ Iteration 24 requires "GO" decision to proceed
   - Cannot proceed to Stage 5b without GO
   - If NO-GO → Fix blockers, re-run Iteration 24
   - GO requires: confidence >= MEDIUM, all gates passed

4. ⚠️ Close spec.md during Iteration 25 (avoid confirmation bias)
   - Re-read epic notes independently
   - Then compare spec to ALL validated sources
   - Ask critical questions (example vs special case)

5. ⚠️ Update feature README.md Agent Status after each gate
   - Document Iteration 25 result (PASSED / discrepancies found)
   - Document Iteration 24 decision (GO/NO-GO)

6. ⚠️ If user decision required (Iteration 25) → STOP and WAIT
   - Do NOT make autonomous decisions
   - Present 3 options (restart/fix/discuss)
   - Wait for user approval

7. ⚠️ Evidence required for verification
   - Cannot just check boxes
   - Must cite specific numbers (N requirements, M tasks, etc.)
   - Provide evidence of completion
```

---

## Prerequisites

**Before starting Part 2b, verify ALL of these are true:**

### From Part 2a (STAGE_5ac_part2a)
- [ ] Part 2a complete (Iterations 23, 23a)
- [ ] Integration Gap Check complete (no orphan code)
- [ ] Iteration 23a ALL 4 PARTS PASSED
  - PART 1: Completeness (100%)
  - PART 2: Specificity (100%)
  - PART 3: Interface Contracts (100%)
  - PART 4: Integration Evidence (100%)

### File Access
- [ ] implementation_plan.md exists and contains all Part 1 and Part 2a outputs
- [ ] spec.md exists and complete
- [ ] Epic notes file: feature-updates/{epic}/{epic}_notes.txt
- [ ] Epic ticket: feature-updates/{epic}/EPIC_TICKET.md
- [ ] Spec summary: feature-updates/{epic}/{feature}/SPEC_SUMMARY.md

### Quality State
- [ ] Confidence level >= MEDIUM (from Round 2)
- [ ] Test coverage >90%
- [ ] No blockers

**If ANY prerequisite not met:**
- STOP - Do not proceed with Part 2b
- Return to Part 2a to complete missing items
- Document blocker in Agent Status

---

## ROUND 3 PART 2b: Gate 3 (Spec Validation & GO/NO-GO)

### Iteration 25: Spec Validation Against Validated Documents (CRITICAL GATE)

**Purpose:** Verify spec.md matches ALL user-validated sources BEFORE implementing

**⚠️ CRITICAL GATE:** This iteration prevents Feature 02 catastrophic bug (implementing wrong solution)

**Sources of truth (all user-validated):**
1. **Epic notes** - user's original request (feature-updates/{epic}/{epic}_notes.txt)
2. **Epic ticket** - validated in Stage 1 (feature-updates/{epic}/EPIC_TICKET.md)
3. **Spec summary** - validated in Stage 2 (feature-updates/{epic}/{feature}/SPEC_SUMMARY.md)

**Historical Context (Feature 02 Catastrophic Bug):**
- Spec.md misinterpreted epic notes line 8
- Spec stated "JSON arrays automatically handle this, NO code changes needed"
- Epic actually required week_N+1 folder logic for ALL 18 weeks
- Wrong spec trusted through 24 iterations and 7 stages
- User caught it in final review → Massive rework required

**With new validation layers:**
- Epic ticket would have stated "All 18 weeks accessible and used correctly"
- Spec summary would have shown "week N+1 offset logic applies to ALL weeks"
- Iteration 25 three-way comparison would have caught misinterpretation

**This iteration prevents implementing wrong solution.**

---

#### Process:

**STEP 1: Close spec.md and implementation_plan.md (avoid confirmation bias)**

**⚠️ CRITICAL:** Do NOT look at spec.md or implementation_plan.md during Steps 1-3.

Why: Confirmation bias → You'll interpret epic notes to match what you already wrote in spec.

**Close these files:**
- spec.md
- implementation_plan.md

**Keep these files open:**
- Epic notes: feature-updates/{epic}/{epic}_notes.txt
- Epic ticket: feature-updates/{epic}/EPIC_TICKET.md
- Spec summary: feature-updates/{epic}/{feature}/SPEC_SUMMARY.md

---

**STEP 2: Re-read validated documents from scratch**

**Read EACH document word-for-word, as if seeing for first time:**

```markdown
## Epic Notes Re-Reading (Independent Analysis)

**Epic file:** feature-updates/integrate_new_player_data_into_simulation/integrate_new_player_data_into_simulation_notes.txt

**Line-by-line analysis:**

**Line 1:** "Update simulations to use JSON files instead of CSV"
- Literal meaning: Change file format from CSV to JSON
- Scope: Data loading changes required
- Implementation: Read JSON instead of CSV

**Lines 3-6:** "Load JSON from simulation/sim_data/YYYY/weeks/week_NN/ folders"
- Literal meaning: Week-based folder structure exists
- Scope: File path construction changes required
- Implementation: Build paths like "simulation/sim_data/2021/weeks/week_01/"

**Line 8:** "use week_17 folders for projected_points, then look at actual_points array in week_18 folders"
- Literal meaning: Week 17 uses TWO folders (week_17 for projected, week_18 for actual)
- **CRITICAL QUESTION:** Is week 17 special, or is this an EXAMPLE of a pattern?
- **Need evidence:** Check if pattern applies to ALL weeks or just week 17
- **Hypothesis 1:** Week 17 is special case (only week 17 needs week 18)
- **Hypothesis 2:** Week 17 is EXAMPLE of pattern (week N needs week N+1 for ALL weeks)

**Question to resolve:** Which hypothesis is correct?
- Evidence needed: Manual inspection of week_01, week_02 JSON files
- Check: Does week_01 have actual_points[0] = 0.0? (would mean week_01 needs week_02)

[Continue for ALL lines in epic notes...]

---

## Epic Ticket Re-Reading

**File:** feature-updates/integrate_new_player_data_into_simulation/EPIC_TICKET.md

**Acceptance Criteria section:**
- "All 18 weeks of data are accessible and used correctly"
- **Key insight:** Says "ALL 18 weeks" (not "weeks 17-18")
- **Implication:** Pattern applies to ALL weeks, not just 17

---

## Spec Summary Re-Reading

**File:** feature-updates/integrate_new_player_data_into_simulation/feature_01_win_rate_sim_json_integration/SPEC_SUMMARY.md

**Technical Changes section:**
- "Week offset logic: week N loads projected from week_N folder, actual from week_N+1 folder"
- **Key insight:** Explicitly states "week N" and "week N+1" (pattern, not special case)
- **Implication:** All weeks follow week_N+1 pattern

---
```

---

**STEP 3: Ask critical questions about epic interpretation**

**For EACH epic requirement, ask:**

- [ ] Is this an EXAMPLE of a general pattern, or a SPECIAL CASE?
- [ ] What is the LITERAL meaning vs my interpretation?
- [ ] What evidence would prove/disprove my interpretation?
- [ ] Did I make assumptions, or verify with code/data?

**Example (Feature 02 Analysis):**

```markdown
## Critical Questions - Epic Line 8 Analysis

**Epic line 8:** "use week_17 folders for projected_points, then look at actual_points array in week_18 folders"

**Question 1:** Is week 17 special, or is this an example?
- **Original spec interpretation:** Week 17 is special case ❌ WRONG
- **Correct interpretation:** Week 17 is EXAMPLE of pattern ALL weeks follow ✅
- **Evidence:** Epic ticket says "ALL 18 weeks", spec summary says "week N+1" pattern

**Question 2:** Why would week 17 need week 18 folder?
- **Original spec assumption:** "JSON arrays handle this automatically" ❌ WRONG
- **Correct answer:** week_N folder has actual_points[N-1] = 0.0 (week not complete yet)
- **Evidence:** Should have manually inspected week_01, week_02 JSON files
  - week_01/players.json: actual_points[0] = 0.0 (week 1 not complete in week 1)
  - week_02/players.json: actual_points[0] = 33.6 (week 1 complete in week 2)

**Question 3:** Does this pattern apply to other weeks?
- **Original spec says:** Not mentioned (assumed no) ❌ WRONG
- **Reality:** YES - week_01 needs week_02, week_02 needs week_03, etc. ✅
- **Evidence:**
  - Epic ticket: "ALL 18 weeks" (not just 17)
  - Spec summary: "week N+1 offset applies to ALL weeks"
  - Manual data inspection confirms pattern

**Conclusion:** Spec.md interpreted epic line as "week 17 special case" when it was actually an EXAMPLE of "week N+1 pattern for ALL weeks"

---
```

---

**STEP 4: Compare epic notes/ticket/summary with spec.md**

**NOW open spec.md and compare EACH claim against ALL THREE validated sources:**

```markdown
## Three-Way Comparison: Epic Notes + Epic Ticket + Spec Summary vs Spec.md

### Requirement 1: Week folder logic

**Epic notes say (line 8):**
> "use week_17 folders for projected_points, then look at actual_points array in week_18 folders"

**Epic ticket says (Acceptance Criteria):**
> "All 18 weeks of data are accessible and used correctly"

**Spec summary says (Technical Changes):**
> "Week offset logic: week N loads projected from week_N folder, actual from week_N+1 folder"

**Spec.md says (Section: "Week 17/18 Logic Clarification"):**
> "JSON arrays already handle this. NO special handling needed. No code changes required."

**Match?** ❌ NO - Major discrepancy

**Discrepancy Analysis:**
- Epic notes: Shows week_17 → week_18 pattern (example, not special case)
- Epic ticket: Explicitly states "ALL 18 weeks" (not just 17/18)
- Spec summary: Correctly interprets as "week N+1 offset for ALL weeks"
- Spec.md: CONTRADICTS summary - says "NO special handling" and "No code changes"

**Which sources are user-validated?**
- Epic ticket: ✅ User-validated in Stage 1
- Spec summary: ✅ User-validated in Stage 2
- Spec.md: ❌ NOT validated yet

**Conclusion:** Spec.md is WRONG (contradicts TWO user-validated sources)

**Evidence spec.md is wrong:**
- Manual data inspection: week_01 has actual_points[0] = 0.0, week_02 has actual_points[0] = 33.6
- Pattern applies to ALL weeks, not just 17
- User approved spec summary with "week N+1 offset applies to ALL weeks"
- Code changes ARE required to load week_N+1 for actuals

**Impact:** Spec.md conclusion is catastrophically WRONG
- Spec says "no code changes" when week_N+1 logic required for ALL weeks
- If implemented as spec states → All actuals would be 0.0 → Feature fails completely

---

### Requirement 2: Data structure

**Epic notes say (lines 10-15):**
> [Quote from epic notes]

**Epic ticket says:**
> [Quote from acceptance criteria]

**Spec summary says:**
> [Quote from technical changes]

**Spec.md says:**
> [Quote from spec]

**Match?** ✅ YES / ❌ NO

**Analysis:**
- [Are all four sources aligned?]
- [If not aligned, which are user-validated?]
- [Spec.md is correct/wrong because...]

[Continue for ALL requirements...]

---
```

**Critical insight:** If spec.md contradicts VALIDATED documents (epic ticket or spec summary), spec.md is WRONG.

Epic ticket and spec summary were approved by user → They are source of truth.

---

**STEP 5: Document ALL discrepancies (even minor)**

```markdown
## Spec Discrepancies Found

### Discrepancy 1: Week offset logic

**Epic notes say (line 8):**
> "use week_17 folders for projected_points, then look at actual_points array in week_18 folders"

**Epic ticket says (Acceptance Criteria):**
> "All 18 weeks of data are accessible and used correctly"

**Spec summary says (Technical Changes):**
> "Week offset logic: week N loads projected from week_N folder, actual from week_N+1 folder"

**Spec.md says (Section "Week 17/18 Logic"):**
> "JSON arrays already handle this. NO special handling needed. No code changes required."

**Why spec.md is wrong:**
- Epic notes show week_N + week_N+1 pattern (week_17 → week_18 is example, not special case)
- Epic ticket explicitly states "ALL 18 weeks" (not just 17/18)
- Spec summary correctly interprets as "week N+1 offset" pattern for ALL weeks
- Spec.md contradicts BOTH validated documents (epic ticket + spec summary)
- Spec.md concluded "no code changes" when pattern requires week_N+1 logic for ALL weeks

**Evidence spec.md is wrong:**
- Manual data inspection: week_01 has actual_points[0] = 0.0, week_02 has actual_points[0] = 33.6
- Pattern confirmed: week_01 needs week_02, week_02 needs week_03, etc.
- User approved spec summary with "week N+1 offset applies to ALL weeks"
- Code changes ARE required to implement week_N+1 folder loading

**Impact on TODO:**
- TODO currently missing tasks for week_N+1 folder loading
- TODO missing tasks for dual folder logic (projected from week_N, actual from week_N+1)
- If implemented as-is: All actuals would be 0.0 → Feature completely non-functional

**Severity:** 🔴 CRITICAL - Feature would fail completely

---

### Discrepancy 2: [Name if any]

[Document ALL additional discrepancies]

---
```

---

**STEP 6: IF ANY DISCREPANCIES FOUND → STOP and report to user**

**🛑 STOP IMMEDIATELY - Do NOT proceed to Iteration 24**

**Report to user:**

```markdown
## ⚠️ ITERATION 25 FAILED - Spec Misalignment with Validated Documents

**User Decision Required**

I completed Iteration 25 (Spec Validation Against Validated Documents) and found discrepancies between spec.md and the user-validated sources (epic notes, epic ticket, spec summary).

**Discrepancies Found:** [X]

---

### Discrepancy 1: [Name]

**Epic notes say:**
> [Quote from epic notes with line number]

**Epic ticket says:**
> [Quote from epic ticket - acceptance criteria]

**Spec summary says:**
> [Quote from spec summary - technical changes]

**Spec.md says:**
> [Quote from spec.md with section reference]

**Why spec.md is wrong:**
- [Explain which validated sources align]
- [Explain why spec.md contradicts them]
- [Evidence from code/data inspection]

**Impact if we implement current TODO:**
- [What would happen - be specific]
- [Which implementation tasks are affected]

**Severity:** 🔴 CRITICAL / 🟡 MODERATE / 🟢 MINOR

---

[Repeat for each discrepancy]

---

### How Would You Like to Proceed?

**Option A (Recommended): Fix spec, restart TODO iterations**

**Steps:**
1. Update spec.md to match epic requirements
2. Restart Stage 5a from Iteration 1 (regenerate TODO from correct spec)
3. Re-run all 25 iterations with corrected spec
4. Ensures TODO matches actual epic intent

**Rationale:** Current TODO is based on wrong spec. Starting fresh with correct spec is safer than trying to patch TODO.

**Time:** ~4-6 hours to re-run Stage 5a with correct spec

---

**Option B: Fix spec and TODO manually, continue to implementation**

**Steps:**
1. Update spec.md to match epic requirements
2. Manually update TODO.md tasks to reflect correct spec
3. Continue to Iteration 24 (Implementation Readiness)

**Rationale:** Faster than Option A, but riskier (may miss subtle dependencies from wrong spec)

**Time:** ~1-2 hours to fix spec and TODO

**Risk:** TODO may still have subtle errors from being based on wrong spec initially

---

**Option C: Discuss discrepancies first**

**Steps:**
1. Review each discrepancy together
2. Clarify epic intent
3. Decide on spec updates
4. Then choose Option A or B

**Rationale:** Best if epic requirements are ambiguous or discrepancies are unclear

**Time:** ~30 minutes discussion + Option A or B time

---

**My Recommendation:** Option A (restart TODO iterations)

**Reason:** [X] discrepancies found, including [Y] CRITICAL severity. Current TODO is based on fundamentally wrong understanding of epic requirements. Restarting with correct spec prevents implementing wrong solution that would require massive rework after user testing.

**Cost:** 4-6 hours to re-run Stage 5a
**Benefit:** Prevents implementing completely wrong feature → Saves days/weeks of rework

---

**Question for user:** Which option do you prefer?

**IMPORTANT: I will NOT proceed to Iteration 24 or Stage 5b until you decide and spec is corrected.**

---
```

**Wait for user decision - DO NOT make this choice autonomously.**

---

**STEP 7: Execute user's choice**

**If user chooses Option A (restart TODO iterations):**

```markdown
## User Decision: Restart TODO Iterations

**Actions:**
1. Update spec.md based on epic re-validation findings
2. Document spec changes in spec.md changelog section
3. Archive current TODO.md as TODO_ARCHIVE_{date}.md
4. Return to Stage 5aa Iteration 1
5. Re-run all iterations (1-25) with corrected spec
6. Mark Iteration 25 status: "SPEC FIXED - Restarting TODO creation"

**Next Action:** Read stages/stage_5/round1_todo_creation.md to restart TODO creation

---
```

**If user chooses Option B (fix and continue):**

```markdown
## User Decision: Fix Spec and TODO, Continue

**Actions:**
1. Update spec.md based on epic re-validation findings
2. Manually update TODO.md to fix affected tasks
3. Review TODO for any missed implications of spec changes
4. Document risk in TODO.md: "RISK: Spec corrected in Iteration 25, TODO updated manually (not regenerated)"
5. Proceed to Iteration 24 (Implementation Readiness)
6. Mark Iteration 25 status: "SPEC FIXED - TODO patched manually, continuing"

**Next Action:** Continue to Iteration 24 (with caution)

---
```

**If user chooses Option C (discuss first):**

```markdown
## User Decision: Discuss Discrepancies

**Actions:**
1. Have conversation about each discrepancy
2. Get user clarification on epic intent
3. Update spec.md based on clarifications
4. Return to this step and choose Option A or B
5. Mark Iteration 25 status: "Discussing discrepancies with user"

**Next Action:** Discuss discrepancies with user

---
```

---

**STEP 8: IF ZERO DISCREPANCIES → Document validation**

**If spec.md matches ALL validated sources perfectly:**

```markdown
---

## ✅ Iteration 25: Spec Validation Against Validated Documents - PASSED

**Validation Date:** {YYYY-MM-DD}

**Validated sources verified:**
- Epic notes: feature-updates/{epic}/{epic}_notes.txt
- Epic ticket: feature-updates/{epic}/EPIC_TICKET.md
- Spec summary: feature-updates/{epic}/{feature}/SPEC_SUMMARY.md

**Requirements verified:** {N} (all requirements compared across all sources)

**Discrepancies found:** 0 ✅

**Spec alignment:** 100% with ALL three validated sources

**Validation method:**
1. Closed spec.md before re-reading epic (avoided confirmation bias)
2. Re-read epic notes word-for-word independently
3. Re-read epic ticket (user-validated outcomes from Stage 1)
4. Re-read spec summary (user-validated feature outcomes from Stage 2)
5. Compared each requirement across all FOUR documents
6. Asked critical questions (example vs special case, literal vs interpreted)
7. Verified with code/data inspection where applicable

**Critical findings:**
- ✅ All spec.md claims align with epic notes
- ✅ All spec.md claims align with epic ticket acceptance criteria
- ✅ All spec.md claims align with spec summary technical changes
- ✅ All interpretations verified with evidence (no assumptions)
- ✅ No discrepancies between spec.md and any validated source

**Example verifications performed:**
- Epic line 8 "week_17 → week_18": Verified as pattern (not special case) via epic ticket "ALL 18 weeks"
- Epic line 5 "JSON format": Verified actual JSON structure by inspecting sample files
- Epic line 10 "projected vs actual": Verified distinction exists in JSON arrays

**RESULT: ✅ Spec.md is correct and aligned with ALL validated sources**

**Confidence:** HIGH - Safe to proceed to implementation

**Ready to proceed to Iteration 24 (Implementation Readiness Protocol).**

---
```

---

**Critical Question Checklist:**

Before marking Iteration 25 complete, answer these:

**Epic Interpretation:**
- [ ] Did I close spec.md before re-reading epic notes? (avoid confirmation bias)
- [ ] Did I read epic notes word-for-word (not skimming)?
- [ ] For each epic line, did I ask: "Is this EXAMPLE or SPECIAL CASE?"
- [ ] Did I distinguish between LITERAL meaning vs my INTERPRETATION?

**Spec Alignment:**
- [ ] Did I compare EVERY spec requirement with epic notes + epic ticket + spec summary?
- [ ] Did I document ALL discrepancies (even minor ones)?
- [ ] For each discrepancy, did I identify which sources are user-validated?
- [ ] Did I assess severity (CRITICAL/MODERATE/MINOR)?

**Assumption Detection:**
- [ ] Did I make assumptions, or verify with evidence?
- [ ] Can I trace every spec claim to epic/ticket/summary OR code inspection?
- [ ] If spec says "automatically handles", did I verify with data inspection?
- [ ] If spec interprets epic line as "special case", did I check if it's a pattern?

**Feature 02 Prevention:**
- [ ] Did I check if patterns (week-based logic, etc.) apply to ALL cases or just one?
- [ ] Did I manually inspect data files mentioned in epic?
- [ ] If epic shows example (week_17 → week_18), did I check if pattern generalizes?
- [ ] Did I avoid saying "automatically handles" without verifying?

**User Reporting (if discrepancies):**
- [ ] If ANY discrepancies found → STOPPED and reported to user?
- [ ] Did I provide 3 options (restart/fix/discuss)?
- [ ] Did I recommend an option with clear rationale?
- [ ] Am I WAITING for user decision (not proceeding autonomously)?

**Validation Confidence (if zero discrepancies):**
- [ ] Can I confidently say spec is correct and matches ALL validated sources?
- [ ] Would I stake feature success on spec accuracy?
- [ ] If I had to bet money, would I bet spec matches epic intent perfectly?

---

**🔄 After Iteration Checkpoint - questions.md Review:**

After completing this iteration, check if you have questions or found answers:

1. **If you discovered NEW uncertainties during this iteration:**
   - Add them to `questions.md` with context
   - Format: Question, context, impact on implementation

2. **If you found ANSWERS to existing questions in questions.md:**
   - Update questions.md to mark question as answered
   - Document the answer and source

3. **If no new questions and no answers found:**
   - No action needed, proceed to next iteration

**Note:** This is a quick check (1-2 minutes). questions.md will be presented to user at Gate 5.

**Update Agent Status:**

**If discrepancies found:**
```markdown
Progress: Iteration 25 FAILED - [X] spec discrepancies found
Gate Status: ❌ BLOCKED
Blockers: Spec/epic misalignment - awaiting user decision
Next Action: WAITING FOR USER - Cannot proceed until spec corrected
```

**If zero discrepancies:**
```markdown
Progress: Iteration 25 PASSED - Spec verified against all validated sources
Gate Status: ✅ PASSED
Next Action: Iteration 24 - Implementation Readiness Protocol (FINAL GATE)
```

---

**Why This Iteration Matters:**

**Feature 02 Example:**
- **Without Iteration 25:** Wrong spec trusted → wrong TODO (missing week_N+1 logic) → wrong implementation (all actuals = 0.0) → user caught in final review → massive rework
- **With Iteration 25:** Spec re-validated against epic ticket + spec summary → discrepancy found → spec corrected → TODO regenerated → correct implementation

**Prevention:** Catches spec interpretation errors BEFORE implementing wrong solution

**Cost:** 20-30 minutes to re-read epic and validate spec
**Benefit:** Prevents days/weeks of implementing wrong feature + rework

---

### Iteration 24: Implementation Readiness Protocol (FINAL GATE)

**Purpose:** Final go/no-go decision before implementation

**⚠️ FINAL GATE:** Cannot proceed to Stage 5b without "GO" decision

**Why this matters:** Last checkpoint to verify everything is ready → GO decision means implementation will succeed

---

#### Process:

**STEP 1: Final readiness checklist**

```markdown
## Implementation Readiness Checklist

**Spec Verification:**
- [x] spec.md complete (no TBD sections)
- [x] All algorithms documented
- [x] All edge cases defined
- [x] All dependencies identified
- [x] Spec validated against epic notes/ticket/summary (Iteration 25 PASSED)

**Implementation Plan Verification:**
- [x] implementation_plan.md created with all sections
- [x] All requirements have implementation tasks
- [x] All tasks have acceptance criteria
- [x] Implementation locations specified
- [x] Test coverage defined
- [x] Implementation phasing defined (Iteration 17)
- [x] Rollback strategy defined (Iteration 18)

**Iteration Completion:**
- [x] All 25 iterations complete (Rounds 1, 2, 3)
- [x] Round 1: Iterations 1-7 + 4a complete
- [x] Round 2: Iterations 8-16 complete
- [x] Round 3 Part 1: Iterations 17-22 complete
- [x] Round 3 Part 2: Iterations 23, 23a, 25, 24 in progress
- [x] No iterations skipped

**Mandatory Gates:**
- [x] Iteration 4a PASSED (TODO Specification Audit)
- [x] Iteration 23a PASSED (ALL 4 PARTS - Pre-Implementation Spec Audit)
- [x] Iteration 25 PASSED (Spec Validation - zero discrepancies)

**Confidence Assessment:**
- [x] Confidence level: HIGH / MEDIUM (must be >= MEDIUM)
- [x] All questions resolved (or documented in questions.md)
- [x] No critical unknowns
- [x] Comfortable with implementation scope

**Integration Verification:**
- [x] Algorithm Traceability Matrix complete (47 mappings typical)
- [x] Integration Gap Check complete (no orphan code - all methods have callers)
- [x] Interface Verification complete (all dependencies verified from source)
- [x] Mock Audit complete (mocks match real interfaces)

**Quality Gates:**
- [x] Test coverage: >90%
- [x] Performance impact: Acceptable (<+20% regression)
- [x] Rollback strategy: Defined
- [x] Documentation plan: Complete
- [x] All mandatory audits PASSED
- [x] No blockers

**DECISION:** ✅ GO / ❌ NO-GO

---
```

---

**STEP 2: Make go/no-go decision**

**✅ GO if:**
- All checklist items checked ✅
- Confidence >= MEDIUM
- All 3 mandatory gates PASSED:
  - Iteration 4a: PASSED
  - Iteration 23a: ALL 4 PARTS PASSED
  - Iteration 25: PASSED (zero discrepancies)
- No blockers
- Ready to implement

**❌ NO-GO if:**
- Any checklist item unchecked
- Confidence < MEDIUM
- Any mandatory gate FAILED
- Any critical blocker exists
- Uncertainty about implementation

---

**STEP 3: Document decision**

**If GO:**

```markdown
---

## ✅ Iteration 24: Implementation Readiness - GO DECISION

**Date:** {YYYY-MM-DD}
**Confidence:** HIGH / MEDIUM
**Iterations Complete:** 25/25 (all rounds complete)

**Mandatory Audits:**
- Iteration 4a (Round 1): ✅ PASSED
- Iteration 23a (Round 3): ✅ ALL 4 PARTS PASSED
- Iteration 25 (Round 3): ✅ PASSED (spec verified against epic notes/ticket/summary - zero discrepancies)

**Quality Metrics:**
- Algorithm mappings: 47
- Integration verification: 12/12 methods have callers
- Interface verification: 8/8 dependencies verified from source
- Test coverage: 95%
- Performance impact: +0.2s (acceptable)

**Preparation Complete:**
- Implementation phasing: 5 phases defined
- Rollback strategy: Config toggle + git revert documented
- Mock audit: All mocks verified, 3 integration tests planned
- Consumer validation: 3 consumers verified

**DECISION: ✅ READY FOR IMPLEMENTATION**

**Next Stage:** Stage 5b (Implementation Execution)

**Proceed using:** stages/stage_5/implementation_execution.md

**Reminder:** Keep spec.md VISIBLE during implementation, use Algorithm Traceability Matrix as guide, run tests after EVERY phase.

---
```

**If NO-GO:**

```markdown
---

## ❌ Iteration 24: Implementation Readiness - NO-GO DECISION

**Date:** {YYYY-MM-DD}
**Confidence:** LOW
**Blockers:** {X}

**Mandatory Audits:**
- Iteration 4a: ✅ PASSED / ❌ FAILED
- Iteration 23a: ✅ ALL 4 PARTS PASSED / ❌ {X} PARTS FAILED
- Iteration 25: ✅ PASSED / ❌ FAILED (discrepancies found)

**Blockers Found:**
1. {Blocker 1 description}
   - Impact: {HIGH/MEDIUM/LOW}
   - Fix: {What needs to be done}

2. {Blocker 2 description}
   - Impact: {HIGH/MEDIUM/LOW}
   - Fix: {What needs to be done}

**DECISION: ❌ NOT READY FOR IMPLEMENTATION**

**Next Actions:**
1. Fix blocker 1: {specific action}
2. Fix blocker 2: {specific action}
3. Re-run affected iterations if needed
4. Re-run Iteration 24 after fixes
5. Must achieve GO decision before proceeding

**Do NOT proceed to Stage 5b until GO decision achieved.**

---
```

---

**🔄 After Iteration Checkpoint - questions.md Review:**

After completing this iteration, check if you have questions or found answers:

1. **If you discovered NEW uncertainties during this iteration:**
   - Add them to `questions.md` with context
   - Format: Question, context, impact on implementation

2. **If you found ANSWERS to existing questions in questions.md:**
   - Update questions.md to mark question as answered
   - Document the answer and source

3. **If no new questions and no answers found:**
   - No action needed, proceed to next iteration

**Note:** This is a quick check (1-2 minutes). questions.md will be presented to user at Gate 5.

**Update Agent Status:**

**If GO:**
```markdown
## Agent Status

**Last Updated:** {YYYY-MM-DD HH:MM}
**Current Phase:** IMPLEMENTATION (ready to start)
**Current Step:** Round 3 complete (25/25 total iterations)
**Current Guide:** stages/stage_5/round3_part2b_gate_3.md (COMPLETE)
**Guide Last Read:** {YYYY-MM-DD HH:MM}

**Progress:** All 25 iterations complete ✅

**Mandatory Gates:**
- Iteration 4a: ✅ PASSED
- Iteration 23a: ✅ ALL 4 PARTS PASSED
- Iteration 25: ✅ PASSED (zero discrepancies)
- Iteration 24 Decision: ✅ GO

**Confidence Level:** {HIGH / MEDIUM}
**Next Stage:** Stage 5b (Implementation Execution)
**Next Action:** Read stages/stage_5/implementation_execution.md
**Blockers:** None
```

**If NO-GO:**
```markdown
## Agent Status

**Last Updated:** {YYYY-MM-DD HH:MM}
**Current Phase:** IMPLEMENTATION_PLANNING
**Current Step:** Round 3 - Iteration 24 (NO-GO)
**Current Guide:** stages/stage_5/round3_part2b_gate_3.md
**Guide Last Read:** {YYYY-MM-DD HH:MM}

**Progress:** Iteration 24 returned NO-GO decision

**Mandatory Gates:**
- Iteration 4a: {Status}
- Iteration 23a: {Status}
- Iteration 25: {Status}
- Iteration 24 Decision: ❌ NO-GO

**Confidence Level:** {LOW / MEDIUM}
**Blockers:** {List blockers}
**Next Action:** Fix blockers, re-run Iteration 24
```

---

## Part 2b Completion Criteria

**Part 2b (and Round 3 and Stage 5a) is COMPLETE when ALL of these are true:**

### Both Iterations Complete
- [ ] Iteration 25: Spec Validation - PASSED (zero discrepancies)
- [ ] Iteration 24: Implementation Readiness - GO DECISION

### Mandatory Gates Passed
- [ ] Gate 3 (Part A - Iteration 25): Spec verified against all validated sources (zero discrepancies)
- [ ] Gate 3 (Part B - Iteration 24): GO decision

### Documentation Updated
- [ ] implementation_plan.md v3.0 contains all Part 2b outputs
- [ ] feature README.md Agent Status shows:
  - Iteration 25: PASSED (zero discrepancies)
  - Iteration 24: GO
  - Phase: IMPLEMENTATION
  - Next Action: Read Stage 5b guide

### Quality Verified
- [ ] Confidence level >= MEDIUM
- [ ] No blockers
- [ ] All checklists 100% complete

**If ALL items checked:**
- Part 2b is COMPLETE
- Round 3 is COMPLETE
- Stage 5a is COMPLETE
- Ready to proceed to Stage 5b (Implementation)
- Read stages/stage_5/implementation_execution.md

**If ANY item unchecked:**
- STOP - Do not proceed to Stage 5b
- Complete missing items
- Re-verify completion criteria

---

## Step 3: Present Implementation Plan to User for Approval (🚨 MANDATORY STEP)

**After Iteration 24 returns GO decision, you MUST present implementation_plan.md to user for approval before proceeding to Stage 5b.**

**This is Gate 5 - User Approval of Implementation Plan (from mandatory_gates.md)**

### Why This Step Exists

**From Proposal Goals:**
- User sees full implementation plan before coding starts
- User can request changes early (cheap to fix in planning, expensive to fix in code)
- Creates shared understanding of implementation strategy
- Addresses guide-updates.txt #3: "Show expected changes, get approval"

**This is NOT optional** - it's a MANDATORY checkpoint per mandatory_gates.md.

---

### Process

**1. Use the "User Approval of Implementation Plan" prompt** from `prompts/stage_5_prompts.md`

**2. Check questions.md status and present plan with any remaining questions:**

**First, check if questions.md exists and has open questions:**

**If questions.md has open questions:**

```
Stage 5a (Implementation Planning) is complete. I've created implementation_plan.md v3.0 (~400 lines) with comprehensive implementation details.

**However, I have {N} open questions in questions.md that need your input before finalizing the plan.**

**Open Questions Summary:**
- {Count by category: algorithm questions, integration questions, edge case questions, etc.}

**File Locations:**
- Implementation plan: `feature-updates/KAI-{N}-{epic_name}/feature_{XX}_{name}/implementation_plan.md`
- Open questions: `feature-updates/KAI-{N}-{epic_name}/feature_{XX}_{name}/questions.md`

**Please review questions.md and answer the {N} open questions.**

**After you answer the questions:**
- I will update implementation_plan.md based on your answers
- I'll ask if you want me to restart the iteration process (Rounds 1-3) with this new information
- If you don't want to restart, I'll present the implementation_plan.md for final approval

**How to provide answers:**
- You can answer all {N} questions at once
- Or go through them one at a time interactively
- Just let me know which you prefer
```

**After user answers questions:**

1. Update implementation_plan.md based on user answers
2. Mark questions as answered in questions.md
3. Ask restart confirmation:

```
Thank you for answering the {N} questions. I've updated implementation_plan.md to incorporate your answers.

**Would you like me to restart the iteration process (Rounds 1-3) with this new information?**

**If you say "yes" (restart iterations):**
- I'll loop back to Round 1 (Iteration 1) with the updated knowledge
- Re-run all 24 iterations incorporating your answers
- This ensures the plan is fully refined with your input
- Time estimate: ~3-4 hours to re-run all iterations

**If you say "no" (proceed with current plan):**
- I'll present implementation_plan.md v3.0 for your final approval
- We proceed to Stage 5b (Implementation) after you approve
- Faster path, but plan may not reflect full implications of your answers

**What would you prefer?**
```

**If user says "yes" (restart):**
- Return to Stage 5aa Round 1 Iteration 1
- READ: stages/stage_5/round1_todo_creation.md
- Re-run all 24 iterations with updated knowledge
- Present plan again at Gate 5

**If user says "no" (proceed):**
- Continue to present plan below (skip to "If no open questions" section)

---

**If no open questions in questions.md OR user chose "no" after answering:**

```
Stage 5a (Implementation Planning) is complete. I've created implementation_plan.md v3.0 (~400 lines) with:

**Key Sections:**
- Implementation Tasks (mapped to spec.md requirements)
- Component Dependencies Matrix
- Algorithm Traceability Matrix
- Test Strategy (>90% coverage)
- Edge Cases and Error Handling
- Implementation Phasing (5-6 checkpoints)
- Performance Considerations
- Mock Audit Results
- Integration Test Plan

**File Location:** `feature-updates/KAI-{N}-{epic_name}/feature_{XX}_{name}/implementation_plan.md`

**Please review implementation_plan.md and confirm:**
1. Implementation approach makes sense
2. Phasing is reasonable (5-6 checkpoints)
3. Test coverage is adequate (>90%)
4. No missing requirements

**Say "approved" to proceed to Stage 5b (Implementation), or request changes.**

**Note:** This is your opportunity to adjust the implementation approach before code is written. Once approved, I'll create implementation_checklist.md and begin coding.
```

**3. Wait for user response:**

**If user says "approved" or equivalent:**
- ✅ Document approval in Agent Status
- ✅ Update Part 2b completion with approval timestamp
- ✅ Proceed to "Prerequisites for Next Stage" section below
- ✅ Move to Stage 5b (Implementation Execution)

**If user requests changes:**
- ❌ DO NOT proceed to Stage 5b
- 📝 Revise implementation_plan.md based on user feedback
- 🔄 Re-run affected iterations from Stage 5a if structural changes needed
- 🔄 Re-run Iteration 24 (Implementation Readiness) after revisions
- 🔄 Re-submit plan for user approval
- ⏸️ Cannot proceed without explicit user approval

**4. Document approval in implementation_plan.md:**

Add to end of implementation_plan.md:

```markdown
---

## User Approval

**Approval Status:** ✅ APPROVED
**Approved By:** User
**Approval Date:** {YYYY-MM-DD HH:MM}
**Approved Version:** v3.0

**User Comments:** {Any comments or conditions from user, or "None - approved as-is"}

---

**STATUS:** ✅ APPROVED - Ready for Stage 5b (Implementation Execution)
```

**5. Update Agent Status:**

```markdown
### User Approval (Gate 5)
- ✅ implementation_plan.md v3.0 presented to user
- ✅ User approval received: {YYYY-MM-DD HH:MM}
- ✅ Gate 5: PASSED
```

---

### Agent Status Update (After Approval)

```markdown
## Agent Status

**Last Updated:** {YYYY-MM-DD HH:MM}
**Current Phase:** IMPLEMENTATION (ready to start)
**Current Step:** Stage 5a COMPLETE (user-approved)
**Current Guide:** stages/stage_5/round3_part2b_gate_3.md (COMPLETE)
**Guide Last Read:** {YYYY-MM-DD HH:MM}

**Progress:** All 25 iterations complete ✅

**Mandatory Gates:**
- Iteration 4a: ✅ PASSED
- Iteration 23a: ✅ ALL 4 PARTS PASSED
- Iteration 25: ✅ PASSED (zero discrepancies)
- Iteration 24 Decision: ✅ GO
- **Gate 5 (User Approval): ✅ PASSED** ({YYYY-MM-DD HH:MM})

**implementation_plan.md:** v3.0 user-approved
**Confidence Level:** {HIGH / MEDIUM}
**Next Stage:** Stage 5b (Implementation Execution)
**Next Action:** Read stages/stage_5/implementation_execution.md
**Blockers:** None
```

---

### Common Mistake to Avoid

**❌ MISTAKE: "I'll skip user approval, plan looks good"**

**Why this is wrong:**
- User approval is Gate 5 - MANDATORY per mandatory_gates.md
- User needs to see implementation approach before coding starts
- This is #3 priority item from guide-updates.txt
- Skipping approval violates core workflow principle

**What to do instead:**
- ✅ ALWAYS present implementation_plan.md to user
- ✅ WAIT for explicit user approval
- ✅ Document approval in plan and Agent Status
- ✅ Only proceed to Stage 5b after approval

---

**After user approval is documented, proceed to "Prerequisites for Next Stage" section below.**

---

## Common Mistakes to Avoid

### ❌ MISTAKE 1: "I'll skip Iteration 25, spec looks fine"

**Why this is wrong:**
- Iteration 25 prevents Feature 02 catastrophic bug
- Spec can be wrong even if it "looks fine"
- Three-way validation catches interpretation errors

**What to do instead:**
- ✅ ALWAYS execute Iteration 25
- ✅ Close spec.md before re-reading epic
- ✅ Compare spec to ALL validated sources
- ✅ Ask critical questions

---

### ❌ MISTAKE 2: "Spec has minor discrepancy, I'll ignore it"

**Why this is wrong:**
- "Minor" discrepancies often indicate larger misunderstandings
- User-validated sources (epic ticket, spec summary) are truth
- Ignoring discrepancies = implementing wrong solution

**What to do instead:**
- ✅ Document ALL discrepancies (even minor)
- ✅ Report to user with 3 options
- ✅ WAIT for user decision
- ✅ Do NOT proceed autonomously

---

### ❌ MISTAKE 3: "Confidence is LOW but I'll mark GO anyway"

**Why this is wrong:**
- GO requires confidence >= MEDIUM
- LOW confidence = missing information or unclear requirements
- Implementing with LOW confidence = failures during implementation

**What to do instead:**
- ✅ Mark NO-GO if confidence < MEDIUM
- ✅ Identify what's causing low confidence
- ✅ Fix confidence issues (ask user, research more, etc.)
- ✅ Only mark GO when confidence >= MEDIUM

---

### ❌ MISTAKE 4: "I'll proceed to Stage 5b with NO-GO decision"

**Why this is wrong:**
- NO-GO means NOT READY for implementation
- Blockers exist that will cause implementation failures
- Cannot skip fixing blockers

**What to do instead:**
- ✅ If NO-GO → Fix ALL blockers
- ✅ Re-run affected iterations
- ✅ Re-run Iteration 24 until GO achieved
- ✅ Only proceed to Stage 5b with GO decision

---

## Prerequisites for Next Stage

**Before proceeding to Stage 5b (Implementation Execution), verify:**

### Part 2b Completion
- [ ] BOTH iterations complete (25, 24)
- [ ] Iteration 25: PASSED (zero discrepancies)
- [ ] Iteration 24: GO DECISION

### Overall Stage 5a Completion
- [ ] All 25 iterations complete (Rounds 1, 2, 3)
- [ ] All mandatory gates PASSED:
  - Iteration 4a: PASSED
  - Iteration 23a: ALL 4 PARTS PASSED
  - Iteration 25: PASSED
  - Iteration 24: GO
  - **Gate 5 (User Approval): PASSED**
- [ ] implementation_plan.md v3.0 complete with all outputs from all rounds
- [ ] **implementation_plan.md v3.0 presented to user and APPROVED**
- [ ] User approval documented in implementation_plan.md and Agent Status
- [ ] Confidence >= MEDIUM
- [ ] No blockers

### Documentation
- [ ] feature README.md shows Stage 5a complete
- [ ] Agent Status shows Gate 5 (User Approval): PASSED with timestamp
- [ ] Agent Status shows next action: "Read Stage 5b guide"

**Only proceed to Stage 5b when ALL items checked.**

**Next stage:** stages/stage_5/implementation_execution.md

---

## Summary

**STAGE_5ac Part 2b - Gate 3 (Spec Validation & GO/NO-GO) executes the MOST CRITICAL validations:**

**Key Activities:**
1. **Spec Validation (Iteration 25 - CRITICAL):** Validate spec against ALL user-approved sources (prevents Feature 02 bug)
2. **Implementation Readiness (Iteration 24 - GO/NO-GO):** Final decision to proceed or fix blockers
3. **User Approval (Gate 5 - MANDATORY):** Present implementation_plan.md to user for approval before coding

**Critical Outputs:**
- Spec validation (zero discrepancies with validated sources)
- GO/NO-GO decision (must be GO to proceed)
- User approval of implementation_plan.md (Gate 5)

**Mandatory Gates:**
- Gate 3 Part A (Iteration 25): Zero discrepancies with validated sources
- Gate 3 Part B (Iteration 24): GO decision
- **Gate 5 (User Approval): User explicitly approves implementation_plan.md**

**Success Criteria:**
- Both iterations complete
- All gates PASSED (Iteration 25, Iteration 24, Gate 5 User Approval)
- User explicitly approved implementation_plan.md
- Confidence >= MEDIUM
- Ready for implementation

**Next Stage:** stages/stage_5/implementation_execution.md - Implement tasks from implementation_plan.md with continuous verification

**Remember:** Part 2b contains THE FINAL quality gates before implementation. Iteration 25 prevents catastrophic bugs by catching spec misinterpretations. Gate 5 (User Approval) ensures user sees and approves the implementation approach before code is written. Trust the process - complete ALL iterations, pass ALL gates, get user approval.

---

**END OF STAGE 5ac PART 2b GUIDE**
