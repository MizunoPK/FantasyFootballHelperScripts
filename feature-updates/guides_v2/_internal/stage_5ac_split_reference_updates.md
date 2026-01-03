# STAGE_5ac Split - Reference Updates Checklist

## Completed
✅ STAGE_5ac_part1_preparation_guide.md created (Iterations 17-22)
✅ STAGE_5ac_part2_final_gates_guide.md created (Iterations 23, 23a, 25, 24)
✅ STAGE_5ac_round3_guide.md converted to router
✅ STAGE_5ac_round3_guide_ORIGINAL_BACKUP.md (renamed original)

## Remaining Updates Needed

### 1. STAGE_5ab_round2_guide.md

**Location 1 - Line 105:** Critical Decisions Summary
```markdown
# CURRENT:
  - ✅ Proceed to Round 3 (STAGE_5ac_round3_guide.md)

# UPDATE TO:
  - ✅ Proceed to Round 3 Part 1 (STAGE_5ac_part1_preparation_guide.md)
```

**Location 2 - Line 944:** Round 2 checkpoint example
```markdown
# CURRENT:
**Next Guide:** STAGE_5ac_round3_guide.md

# UPDATE TO:
**Next Guide:** STAGE_5ac_part1_preparation_guide.md
```

**Location 3 - Lines 1100-1113:** Next Round section
```markdown
# CURRENT:
📖 **READ:** `STAGE_5ac_round3_guide.md`
🎯 **GOAL:** Final verification & readiness - implementation phasing, mock audit, final gates
⏱️ **ESTIMATE:** 60-75 minutes

**Round 3 will:**
- Plan implementation phasing (Iteration 17)
- Define rollback strategy (Iteration 18)
- Final algorithm/data flow/integration verification (Iterations 19, 23)
- Performance considerations (Iteration 20)
- Mock audit & integration test plan (Iteration 21)
- Pre-Implementation Spec Audit - ALL 4 PARTS (Iteration 23a - MANDATORY)
- Implementation Readiness Protocol (Iteration 24 - FINAL GATE)

# UPDATE TO:
📖 **READ:** `STAGE_5ac_part1_preparation_guide.md` (Round 3 Part 1)
🎯 **GOAL:** Preparation iterations - implementation phasing, rollback strategy, algorithm traceability (final), performance, mock audit
⏱️ **ESTIMATE:** 60-90 minutes for Part 1, then 1.5-2.5 hours for Part 2

**Round 3 is split into 2 parts:**

**Part 1 - Preparation (Iterations 17-22):**
- Plan implementation phasing (Iteration 17)
- Define rollback strategy (Iteration 18)
- Final algorithm traceability matrix (Iteration 19)
- Performance considerations (Iteration 20)
- Mock audit & integration test plan (Iteration 21)
- Output consumer validation (Iteration 22)

**Part 2 - Final Gates (Iterations 23, 23a, 25, 24):**
- Integration gap check (Iteration 23)
- Pre-Implementation Spec Audit - ALL 4 PARTS (Iteration 23a - MANDATORY)
- Spec Validation Against Validated Documents (Iteration 25 - CRITICAL GATE)
- Implementation Readiness Protocol (Iteration 24 - FINAL GO/NO-GO)
```

---

### 2. prompts_reference_v2.md

**Location 1 - Line 243:** Stage 5a round list
```markdown
# CURRENT:
- **STAGE_5aa_round1_guide.md** - Round 1: Iterations 1-7 + 4a (START HERE)
- **STAGE_5ab_round2_guide.md** - Round 2: Iterations 8-16
- **STAGE_5ac_round3_guide.md** - Round 3: Iterations 17-24 + 23a

# UPDATE TO:
- **STAGE_5aa_round1_guide.md** - Round 1: Iterations 1-7 + 4a (START HERE)
- **STAGE_5ab_round2_guide.md** - Round 2: Iterations 8-16
- **STAGE_5ac_part1_preparation_guide.md** - Round 3 Part 1: Iterations 17-22
- **STAGE_5ac_part2_final_gates_guide.md** - Round 3 Part 2: Iterations 23, 23a, 25, 24
```

**Location 2 - Lines 356-409:** Replace "Starting Stage 5a: TODO Creation (Round 3)" with TWO prompts:

**Prompt 1: Starting Stage 5ac Part 1**
```markdown
### Starting Stage 5ac Part 1: TODO Creation (Round 3 - Preparation)

**User says:** Agent detects Round 2 complete (16/24 iterations done, confidence >= MEDIUM, test coverage >90%)

**Prerequisite:** Round 2 complete (STAGE_5ab), confidence >= MEDIUM, test coverage >90%

**Note:** Round 3 is split into 2 parts for better navigation:
- **STAGE_5ac_part1_preparation_guide.md** - Iterations 17-22 (START HERE)
- **STAGE_5ac_part2_final_gates_guide.md** - Iterations 23, 23a, 25, 24

**Agent MUST respond:**

\`\`\`
I'm reading `STAGE_5ac_part1_preparation_guide.md` to ensure I follow all 6 preparation iterations in Round 3 Part 1...

**The guide requires:**
- **Part 1: 6 preparation iterations** (NO SKIPPING):
  - Iteration 17: Implementation Phasing
  - Iteration 18: Rollback Strategy
  - Iteration 19: Algorithm Traceability Matrix (Final)
  - Iteration 20: Performance Considerations
  - Iteration 21: Mock Audit & Integration Test Plan (CRITICAL)
  - Iteration 22: Output Consumer Validation
- **Implementation Phasing** (Iteration 17):
  - Break implementation into 5-6 phases with checkpoints
  - Prevents "big bang" integration failures
- **Mock Audit** (Iteration 21 - CRITICAL):
  - Verify EACH mock matches real interface (READ actual source code)
  - Plan at least 3 integration tests with REAL objects (NO MOCKS)
  - Prevents unit tests passing with wrong mocks
- **Performance Optimization** (Iteration 20):
  - Identify O(n²) algorithms, optimize to O(n)
  - Document performance requirements

**Why Round 3 Part 1 matters:**
- Preparation iterations ensure implementation is well-planned
- Final algorithm traceability prevents missing requirements
- Mock audit prevents interface mismatch bugs

**Prerequisites I'm verifying:**
✅ Round 2 complete (16/24 iterations)
✅ Test coverage: >90%
✅ Confidence: >= MEDIUM (from Round 2 checkpoint)
✅ Algorithm Traceability Matrix updated (Round 2)
✅ Integration Gap Check updated (Round 2)

**I'll now proceed with Round 3 Part 1 (iterations 17-22).**

**Updating feature README Agent Status:**
- Current Phase: TODO_CREATION
- Current Guide: STAGE_5ac_part1_preparation_guide.md
- Guide Last Read: {YYYY-MM-DD HH:MM}
- Critical Rules: "6 preparation iterations mandatory", "Iteration 21: Verify mocks against ACTUAL source code", "Integration tests must use REAL objects"
- Progress: 16/24 total iterations complete (starting Round 3 Part 1)
- Next Action: Begin iteration 17 - Implementation Phasing

Starting iteration 17...
\`\`\`
```

**Prompt 2: Starting Stage 5ac Part 2**
```markdown
### Starting Stage 5ac Part 2: TODO Creation (Round 3 - Final Gates)

**User says:** Agent detects Round 3 Part 1 complete (22/24 iterations done)

**Prerequisite:** Round 3 Part 1 complete (STAGE_5ac_part1), Iterations 17-22 done

**Agent MUST respond:**

\`\`\`
I'm reading `STAGE_5ac_part2_final_gates_guide.md` to ensure I follow all 4 final gate iterations in Round 3 Part 2...

**The guide requires:**
- **Part 2: 4 final gate iterations containing ALL 3 MANDATORY GATES**:
  - Iteration 23: Integration Gap Check (Final)
  - Iteration 23a: Pre-Implementation Spec Audit (MANDATORY GATE - 4 PARTS)
  - Iteration 25: Spec Validation Against Validated Documents (CRITICAL GATE)
  - Iteration 24: Implementation Readiness Protocol (FINAL GATE - GO/NO-GO)
- **Iteration 23a (Pre-Implementation Spec Audit) has 4 MANDATORY PARTS**:
  - Part 1: Completeness Audit (Coverage = 100%)
  - Part 2: Specificity Audit (Specificity = 100%)
  - Part 3: Interface Contracts Audit (Verification = 100%)
  - Part 4: Integration Evidence Audit (Integration = 100%)
  - ALL 4 PARTS must show 100% metrics with evidence (cite specific numbers)
- **Iteration 25 (Spec Validation) - CRITICAL GATE**:
  - Close spec.md first (avoid confirmation bias)
  - Re-read validated documents independently: epic notes + epic ticket + spec summary
  - Three-way comparison: spec.md vs all three validated sources
  - IF ANY DISCREPANCIES → STOP and report to user with 3 options
  - Prevents catastrophic bugs (Feature 02 bug: spec misinterpreted epic notes)
- **Iteration 24 (Implementation Readiness) - FINAL GATE**:
  - GO/NO-GO decision required
  - CANNOT proceed to Stage 5b without "GO" decision
  - GO requires: confidence >= MEDIUM, all gates PASSED, all checklists complete

**Why Round 3 Part 2 matters:**
- Contains ALL 3 mandatory gates that CANNOT be skipped
- Evidence-based verification (must cite specific numbers, provide proof)
- Three-way validation prevents implementing wrong solution
- GO/NO-GO framework prevents implementing with incomplete planning

**Prerequisites I'm verifying:**
✅ Round 3 Part 1 complete (22/24 iterations)
✅ Implementation phasing defined
✅ Rollback strategy documented
✅ Algorithm traceability matrix complete (final)
✅ Mock audit complete (all mocks verified against real interfaces)
✅ Integration test plan created (at least 3 tests with REAL objects)

**I'll now proceed with Round 3 Part 2 (iterations 23, 23a, 25, 24).**

**Updating feature README Agent Status:**
- Current Phase: TODO_CREATION
- Current Guide: STAGE_5ac_part2_final_gates_guide.md
- Guide Last Read: {YYYY-MM-DD HH:MM}
- Critical Rules: "3 MANDATORY GATES (23a, 25, 24) - CANNOT skip", "Evidence-based verification (cite numbers)", "Close spec.md before Iteration 25", "User decision required if discrepancies"
- Progress: 22/24 total iterations complete (starting Round 3 Part 2)
- Next Action: Begin iteration 23 - Integration Gap Check (Final)

Starting iteration 23...
\`\`\`
```

---

### 3. README.md

**Location 1 - Line 103:** Quick reference table
```markdown
# CURRENT:
| Round 2 complete | `STAGE_5ac_round3_guide.md` | Iterations 17-24 + 23a: Phasing, final gates, readiness |

# UPDATE TO (3 rows):
| Round 2 complete | `STAGE_5ac_round3_guide.md` | Router: Links to Part 1/Part 2 sub-stages |
| Round 3 preparation phase | `STAGE_5ac_part1_preparation_guide.md` | Iterations 17-22: Phasing, rollback, algorithm (final), performance, mock audit |
| Round 3 final gates phase | `STAGE_5ac_part2_final_gates_guide.md` | Iterations 23, 23a, 25, 24: 3 mandatory gates, GO/NO-GO |
```

**Location 2 - Line 201:** File structure tree
```markdown
# CURRENT:
    ├── STAGE_5ac_round3_guide.md                 ← TODO creation Round 3

# UPDATE TO:
    ├── STAGE_5ac_round3_guide.md                 ← TODO creation Round 3 (router)
    ├── STAGE_5ac_part1_preparation_guide.md      ← Round 3 Part 1: Preparation
    ├── STAGE_5ac_part2_final_gates_guide.md      ← Round 3 Part 2: Final Gates
```

---

### 4. EPIC_WORKFLOW_USAGE.md

**Search for:** References to STAGE_5ac_round3_guide.md
**Update:** Change to STAGE_5ac_part1_preparation_guide.md (for starting Round 3)
**Add:** Mention of Part 2 guide for final gates

---

### 5. STAGE_5_bug_fix_workflow_guide.md

**Search for:** References to Round 3 or STAGE_5ac
**Update:** Clarify that bug fixes follow same TODO creation process but use split guides

---

## Notes

- The router guide (STAGE_5ac_round3_guide.md) now serves as navigation hub
- Original guide backed up as STAGE_5ac_round3_guide_ORIGINAL_BACKUP.md
- All references should point to Part 1 for starting Round 3
- Part 2 references only appear when transitioning from Part 1 to Part 2
- Maintains consistency with STAGE_2 and STAGE_6 split patterns
