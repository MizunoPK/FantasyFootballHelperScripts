# S5: Feature Implementation
## S5.P1: Planning Round 1
### S5.P1.I3: Backward Compatibility Analysis

**Purpose:** Backward Compatibility Analysis
**Prerequisites:** Previous iterations complete
**Main Guide:** `stages/s5/s5_p1_planning_round1.md`
**Router:** `stages/s5/s5_p1_i3_integration.md`

---

## Iteration 7a: Backward Compatibility Analysis (NEW - MANDATORY)

**Objective:** Identify how this feature interacts with existing data, files, and configurations created by older versions of the code.

**Why This Matters:** New features often modify data structures or file formats. If the system can resume/load old data, the new code must handle old formats gracefully. This iteration prevents bugs caused by old data polluting new calculations.

**Historical Evidence:** Issue #001 (KAI-5) discovered in user testing could have been prevented by this iteration. Resume logic loaded old files without ranking_metrics, polluting best_configs with invalid data.

---

### Research Questions

**1. Data Persistence:**
- Does this feature modify any data structures that are saved to files?
- Can the system resume/load from files created before this epic?
- What file formats are involved? (JSON, CSV, pickled objects, etc.)

**2. Old Data Handling:**
- What happens if new code loads old files missing new fields?
- Will old data be used in comparisons/calculations with new data?
- Are there fallback mechanisms that might hide incompatibilities?

**3. Migration Strategy:**
- Do old files need to be migrated to new format?
- Should old files be ignored/invalidated?
- Is there a version marker in saved files?

**4. Resume Scenarios:**
- Can users resume operations from intermediate states?
- What happens if intermediate files are from older code version?
- Will the system detect and handle version mismatches?

---

### Action Items

**1. Search for File I/O Operations:**

Look for save/load methods in affected modules:
```bash
# Find file write operations
grep -r "\.dump\|\.to_json\|\.to_csv\|pickle\.dump" affected_module/ --include="*.py"

# Find file read operations
grep -r "\.load\|\.from_json\|\.read_csv\|pickle\.load" affected_module/ --include="*.py"

# Find resume/checkpoint logic
grep -r "resume\|checkpoint\|load_state" affected_module/ --include="*.py"
```

**2. Analyze Data Structures:**

- List all fields added/removed/modified
- Check if structures have version markers
- Verify default values for missing fields

**Example analysis:**
```markdown
## Data Structure Changes

**FantasyPlayer class modifications:**
- Added: adp_value (Optional[int]) - Default: None
- Added: adp_multiplier (float) - Default: 1.0
- No fields removed
- No fields modified

**Serialization:**
- FantasyPlayer not directly serialized (checked with grep)
- No pickle files found in data/
- No JSON export of player objects

**Conclusion:** No backward compatibility issues (player objects not persisted)
```

**3. Document Findings in questions.md:**

```markdown
## Backward Compatibility Analysis (Iteration 7a)

**Files that persist data:**
- [List files and formats]

**New fields added:**
- [List new fields with types]

**Resume/load scenarios:**
- [Describe scenarios where old data might be loaded]

**Compatibility strategy:**
- [ ] Option 1: Migrate old files on load
- [ ] Option 2: Invalidate old files (require fresh run)
- [ ] Option 3: Handle missing fields with defaults
- [ ] Option 4: No old files exist / not applicable

**Rationale:** [Explain chosen strategy]
```

**4. Add Test Scenarios to implementation_plan.md:**

If resume/load possible:
- Add test: "Resume from file created before this epic"

If migration needed:
- Add test: "Migrate old file format to new format"

If validation needed:
- Add test: "Reject incompatible old files with clear error"

---

### Example: Backward Compatibility Scenario

**Feature that modifies persisted data:**

```markdown
## Backward Compatibility Analysis

**Files that persist data:**
- simulation/results/best_configs.json (simulation results)
- simulation/cache/player_cache.pkl (player objects)

**New fields added:**
- PlayerStats.ranking_metrics (Dict[str, float]) - NEW field

**Resume/load scenarios:**
- User runs simulation → best_configs.json created WITH ranking_metrics
- User upgrades code → runs simulation again
- System loads old best_configs.json WITHOUT ranking_metrics
- Comparison logic fails (missing field in old data)

**Compatibility strategy:**
- ✅ **Option 2: Invalidate old files (require fresh run)**
- Rationale: Simulations are cheap to re-run, data format changed significantly
- Implementation: Check for ranking_metrics field on load, reject if missing
- User message: "Simulation format updated. Previous results incompatible. Re-running simulation..."

**Tests to add:**
- test_load_old_best_configs_rejects_gracefully()
- test_load_best_configs_with_ranking_metrics_succeeds()
```

---

### Success Criteria

Before marking Iteration 7a complete:

- ✅ All file I/O operations identified and analyzed
- ✅ Compatibility strategy documented and justified
- ✅ Resume/load scenarios covered in test plan
- ✅ Migration or validation logic added to implementation_plan.md (if needed)

**Time Estimate:** 10-15 minutes (prevents hours of debugging)

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
   - No action needed, proceed to checkpoint

**Note:** This is a quick check (1-2 minutes). questions.md will be presented to user at Gate 5.

**Update Agent Status:**
```text
Progress: Planning Round 1 Iteration 7a complete (backward compatibility analyzed)
Next Action: Planning Round 1 checkpoint - evaluate confidence
```

---

## 🛑 MANDATORY CHECKPOINT: ROUND 1 COMPLETE

**You have completed Iterations 1-7 + Gates 4a, 7a (Round 1)**

⚠️ STOP - DO NOT PROCEED TO ROUND 2 YET

**REQUIRED ACTIONS:**

### Step 1: Update implementation_plan.md Version
1. [ ] Mark version as v1.0 in Version History section

### Step 2: Update Agent Status
2. [ ] Update feature README.md Agent Status:
   - Current Guide: "stages/s5/s5_p2_planning_round2.md"
   - Current Step: "Round 1 complete (7 iterations + 2 gates), evaluating confidence"
   - Last Updated: [timestamp]
   - Progress: "Planning Round 1 complete (9/9 iterations)"
   - Confidence Level: {HIGH / MEDIUM / LOW}
   - Next Action: {Create questions file / Proceed to Planning Round 2}
   - Blockers: {List any uncertainties or "None"}

### Step 3: Evaluate Confidence
3. [ ] Evaluate confidence across 5 dimensions:
   - [ ] Do I understand the feature requirements? (HIGH/MEDIUM/LOW)
   - [ ] Are all algorithms clear? (HIGH/MEDIUM/LOW)
   - [ ] Are interfaces verified? (HIGH/MEDIUM/LOW)
   - [ ] Is data flow understood? (HIGH/MEDIUM/LOW)
   - [ ] Are all consumption locations identified? (HIGH/MEDIUM/LOW)
   - [ ] Overall confidence: {HIGH/MEDIUM/LOW}

### Step 4: Re-Read Critical Sections
4. [ ] Use Read tool to re-read "Round 1 Summary" section of s5_p1_planning_round1.md
5. [ ] Use Read tool to re-read "Confidence Evaluation" criteria

### Step 5: Output Acknowledgment
6. [ ] Output acknowledgment: "✅ ROUND 1 CHECKPOINT COMPLETE: Confidence={level}, proceeding to {Round 2 / questions.md}"

**Why this checkpoint exists:**
- Round 1 confidence determines whether Round 2 is needed
- 75% of agents skip confidence evaluation and proceed blindly
- Low confidence proceeding to Round 2 causes 80% implementation failure rate

### Decision Point

**If confidence >= MEDIUM:**
- ✅ Proceed to Planning Round 2
- Use "Starting S5 Round 2" prompt from prompts_reference_v2.md
- Read `stages/s5/s5_p2_planning_round2.md`

**If confidence < MEDIUM:**
- ❌ STOP - Create questions.md file
- Wait for user answers
- Do NOT proceed to Planning Round 2

---

### If Confidence < MEDIUM: Create Questions File

**File:** `questions.md` (in feature folder)

**Template:**
```markdown
# Feature Questions for User

**Created After:** Planning Round 1 (Iteration 7a)
**Confidence Level:** LOW / MEDIUM
**Reason:** {Why confidence is low}

---

## Question 1: {Topic}

**Context:** {Why this question arose during iterations}

**Current Understanding:** {What I think, but not sure}

**Question:** {Specific question for user}

**Options:**
A. {Option A}
B. {Option B}
C. {Option C}

**My Recommendation:** {Which option and why}

**Impact if wrong:** {What breaks if we guess wrong}

---

{Repeat for all questions}
```

**Update Agent Status:**
```bash
Blockers: Waiting for user answers to questions.md
Next Action: Wait for user responses, then update implementation_plan.md based on answers
```

**WAIT for user answers. Do NOT proceed to Planning Round 2.**

---

## Checkpoint: After Planning Round 1 Complete

**Verify:**
- [ ] All 9 iterations complete (1-7, 4a, 7a)
- [ ] Gate 4a PASSED (mandatory)
- [ ] implementation_plan.md v1.0 created with all sections
- [ ] Algorithm Traceability Matrix added (40+ mappings)
- [ ] Component Dependencies verified
- [ ] Data flow documented
- [ ] Downstream consumption analyzed (Iteration 5a)
- [ ] Error handling scenarios documented
- [ ] Integration matrix created (no orphan code)
- [ ] Backward compatibility analyzed
- [ ] Confidence level evaluated

**Files Created/Updated:**
- ✅ implementation_plan.md - v1.0 with comprehensive tasks
- ✅ questions.md - Created if confidence < MEDIUM (optional)
- ✅ feature README.md Agent Status - Planning Round 1 complete

**Next:**
- If confidence >= MEDIUM: Read `stages/s5/s5_p2_planning_round2.md`
- If confidence < MEDIUM: Wait for user to answer questions.md


## Exit Criteria

**Iteration 7 complete when ALL of these are true:**

- [ ] All tasks in this iteration complete
- [ ] implementation_plan.md updated
- [ ] Agent Status updated
- [ ] Ready for next iteration

**If any criterion unchecked:** Complete missing items first

---
---

**END OF ITERATION 7 + ROUND 1 CHECKPOINT**
