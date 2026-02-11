# Known Exceptions - Prerequisites/Exit Criteria

**Purpose:** Documents files that intentionally lack formal "## Prerequisites" or "## Exit Criteria" sections

**Last Updated:** 2026-02-05

**Why This Document Exists:**
Audit Dimension D13 (Documentation Quality) checks for "## Prerequisites" and "## Exit Criteria" sections in workflow guides. However, certain file types intentionally use alternative patterns. This document prevents these files from being flagged as violations in future audits.

---

## Exception Categories

### Category A: S5 Iteration Files (14 files)

**Pattern:** Lightweight iteration guides with inline prerequisites, exit criteria inherited from parent round

**Design Rationale:**
- Iteration files are sequential steps within S5 rounds (Round 1, Round 2, Round 3)
- Prerequisites are simple: "Previous iteration complete" (stated inline)
- Exit criteria defined at round level (s5_v2_validation_loop.md consolidates all rounds)
- Formal sections would be redundant
- Files follow "router + detailed iteration" pattern for focused reference

**Missing Sections:** Prerequisites (inline instead), Exit Criteria (inherited from parent)

**Files:**

#### S5.P1 (Round 1) Iteration Files (7 files)

1. **stages/s5/s5_p1_i3_integration.md**
   - Type: Router for Iterations 5-7
   - Prerequisites: Line 8 - "**Prerequisites:** Iterations 1-4 + Gate 4a complete"
   - Exit Criteria: Inherited from s5_v2_validation_loop.md
   - Design: Navigation hub to 6 sub-iteration files

2. **stages/s5/s5_p1_i3_iter5_dataflow.md**
   - Type: Iteration 5 - End-to-End Data Flow
   - Prerequisites: Line 6 - "**Prerequisites:** Previous iterations complete"
   - Exit Criteria: Inherited from s5_v2_validation_loop.md
   - Design: Focused single-iteration guide (109 lines)

3. **stages/s5/s5_p1_i3_iter5a_downstream.md**
   - Type: Iteration 5a - Downstream Data Consumption Tracing
   - Prerequisites: Line 6 - "**Prerequisites:** Previous iterations complete"
   - Exit Criteria: Inherited from s5_v2_validation_loop.md
   - Design: Focused single-iteration guide (352 lines)

4. **stages/s5/s5_p1_i3_iter6_errorhandling.md**
   - Type: Iteration 6 - Error Handling Scenarios
   - Prerequisites: Line 6 - "**Prerequisites:** Previous iterations complete"
   - Exit Criteria: Inherited from s5_v2_validation_loop.md
   - Design: Focused single-iteration guide (132 lines)

5. **stages/s5/s5_p1_i3_iter6a_dependencies.md**
   - Type: Iteration 6a - External Dependency Final Verification
   - Prerequisites: Line 6 - "**Prerequisites:** Previous iterations complete"
   - Exit Criteria: Inherited from s5_v2_validation_loop.md
   - Design: Focused single-iteration guide (157 lines)

6. **stages/s5/s5_p1_i3_iter7_integration.md**
   - Type: Iteration 7 - Integration Gap Check
   - Prerequisites: Inline statement
   - Exit Criteria: Inherited from s5_v2_validation_loop.md
   - Design: Focused single-iteration guide

7. **stages/s5/s5_p1_i3_iter7a_compatibility.md**
   - Type: Iteration 7a - Backward Compatibility Check
   - Prerequisites: Inline statement
   - Exit Criteria: Inherited from s5_v2_validation_loop.md
   - Design: Focused single-iteration guide

#### S5.P3 (Round 3) Iteration Files (7 files)

8. **stages/s5/s5_p3_i1_preparation.md**
   - Type: Round 3 Part 1 - Preparation
   - Prerequisites: Inline statement
   - Exit Criteria: Inherited from s5_v2_validation_loop.md (Round 3 section)
   - Design: Preparation phase guide for Round 3

9. **stages/s5/s5_p3_i1_iter17_phasing.md**
   - Type: Iteration 17 - Phasing
   - Prerequisites: Inline statement
   - Exit Criteria: Inherited from s5_v2_validation_loop.md (Round 3 section)
   - Design: Focused single-iteration guide

10. **stages/s5/s5_p3_i1_iter18_rollback.md**
    - Type: Iteration 18 - Rollback
    - Prerequisites: Inline statement
    - Exit Criteria: Inherited from s5_v2_validation_loop.md (Round 3 section)
    - Design: Focused single-iteration guide

11. **stages/s5/s5_p3_i1_iter19_traceability.md**
    - Type: Iteration 19 - Traceability
    - Prerequisites: Inline statement
    - Exit Criteria: Inherited from s5_v2_validation_loop.md (Round 3 section)
    - Design: Focused single-iteration guide

12. **stages/s5/s5_p3_i1_iter20_performance.md**
    - Type: Iteration 20 - Performance
    - Prerequisites: Inline statement
    - Exit Criteria: Inherited from s5_v2_validation_loop.md (Round 3 section)
    - Design: Focused single-iteration guide

13. **stages/s5/s5_p3_i1_iter21_mockaudit.md**
    - Type: Iteration 21 - Mock Audit
    - Prerequisites: Inline statement
    - Exit Criteria: Inherited from s5_v2_validation_loop.md (Round 3 section)
    - Design: Focused single-iteration guide

14. **stages/s5/s5_p3_i1_iter22_consumers.md**
    - Type: Iteration 22 - Consumers
    - Prerequisites: Inline statement
    - Exit Criteria: Inherited from s5_v2_validation_loop.md (Round 3 section)
    - Design: Focused single-iteration guide

**Audit Action:** SKIP these files when checking D13 (Documentation Quality) - Prerequisites/Exit Criteria

---

### Category B: S5 Design and Migration Documents (2 files)

**Pattern:** Design plans and migration guides (not workflow execution guides)

**Design Rationale:**
- These are reference documents for understanding S5 v1→v2 transition
- Not part of active workflow execution path
- Provide historical context and design decisions
- Prerequisites/Exit Criteria not applicable to reference documentation

**Missing Sections:** Prerequisites, Exit Criteria

**Files:**

   - Type: Migration guide
   - Purpose: Help agents understand transition from S5 v1 (22 iterations) to S5 v2 (Validation Loop)
   - Design: Comparison tables, side-by-side workflows, FAQ format

   - Type: Design plan document
   - Purpose: Document architectural decisions for S5 v2 design
   - Design: Architecture, dimension definitions, validation loop design

**Audit Action:** SKIP these files when checking D13 (Documentation Quality) - Prerequisites/Exit Criteria

---

### Category C: Optional/Auxiliary Files (3 files)

**Pattern:** Support guides used conditionally or as reference material, not standard sequential workflows

**Design Rationale:**
- Files serve specific auxiliary purposes
- Prerequisites/exit criteria handled inline or not applicable
- Not part of standard epic workflow sequence

**Files:**

15. **stages/s3/s3_parallel_work_sync.md**
    - **Type:** Optional synchronization checklist
    - **When Used:** Only when S2 executed in parallel mode (Primary + Secondary agents)
    - **Skipped:** When S2 done sequentially (single agent)
    - **Prerequisites:** None (conditional usage based on S2 execution mode)
    - **Exit Criteria:** Inline completion verification in Step 0.2 - STATUS file checks
    - **Missing Sections:** Prerequisites (not applicable), Exit Criteria (inline instead)
    - **Design Rationale:** Conditional auxiliary workflow, not standard stage progression
    - **Audit Action:** SKIP - not a standard workflow guide

16. **stages/s4/s4_feature_testing_card.md**
    - **Type:** Quick reference card / cheat sheet
    - **Purpose:** At-a-glance iteration checklist for S4
    - **Full Guides:** References s4_feature_testing_strategy.md, s4_test_strategy_development.md
    - **Prerequisites:** Line 13 inline - "**Prerequisites:** S3 complete (Gate 4.5 passed), spec.md finalized (Gate 3 passed)"
    - **Exit Criteria:** Not applicable (reference card, not workflow)
    - **Missing Sections:** Prerequisites (inline instead), Exit Criteria (not applicable)
    - **Design Rationale:** Reference material for quick lookup, not step-by-step workflow execution
    - **Audit Action:** SKIP - reference card, not workflow guide

17. **stages/s4/s4_test_strategy_development.md**
    - **Type:** Detailed iteration guide (Iterations 1-3)
    - **Purpose:** Deep-dive instructions for S4 Iterations 1-3
    - **Prerequisites:** Handled in MANDATORY READING PROTOCOL (line 8) - "Verify S4 router guide already read, Verify prerequisites complete (S3 done, Gate 4.5 passed)"
    - **Exit Criteria:** HAS formal "## Exit Criteria" section at line 768
    - **Missing Sections:** Prerequisites (handled in MANDATORY READING PROTOCOL instead of separate h2 section)
    - **Design Rationale:** Prerequisites verification integrated into reading protocol for consistency
    - **Audit Action:** SKIP for Prerequisites check (has Exit Criteria, Prerequisites in protocol)
    - **Note:** This is an audit FALSE POSITIVE - file has Exit Criteria but was flagged by Round 2 audit

---

## How to Use This Document

### For Future Audits

**When running D13 (Documentation Quality) Prerequisites/Exit Criteria checks:**

1. **Generate violation list** using automated pattern search
2. **Cross-reference with this document** before flagging as issues
3. **Filter out known exceptions** (17 files total)
4. **Investigate remaining violations** as potential real issues

**Example Audit Workflow:**
```bash
# Step 1: Find files missing Prerequisites
for file in stages/*/*.md; do
  grep -q "^## Prerequisites" "$file" || echo "$file"
done > missing_prereqs.txt

# Step 2: Filter out known exceptions
# Remove lines matching: s5/s5_p1_i3_*, s5/s5_p3_i1_*, s3/s3_parallel_work_sync.md, s4/s4_feature_testing_card.md, s4/s4_test_strategy_development.md
grep -v -E "(s5_p1_i3_|s5_p3_i1_|s3_parallel_work_sync|s4_feature_testing_card|s4_test_strategy_development)" missing_prereqs.txt > real_violations.txt

# Step 3: Investigate remaining files
wc -l real_violations.txt  # Should be low count
```

### For Guide Authors

**When creating new iteration guides in S5:**
- Use inline prerequisites: "**Prerequisites:** Previous iterations complete"
- Rely on parent round guide for exit criteria
- Follow established pattern (see Category A files above)
- File size: Keep focused and lightweight (100-400 lines)

**When creating auxiliary/optional guides:**
- Consider if Prerequisites/Exit Criteria apply
- If guide is conditional or reference material, inline may be appropriate
- Add entry to this document if creating new exception pattern

**When creating standard workflow guides:**
- **DO include formal "## Prerequisites" section** (h2 level)
- **DO include formal "## Exit Criteria" section** (h2 level)
- Exceptions are rare - default to formal sections

---

## Audit History

**Round 2 (2026-02-05):** Identified 34 files missing Prerequisites/Exit Criteria
**Round 3 (2026-02-05):** Investigated all 34 files, categorized as:
- 4 real issues (fixed)
- 30 intentional exceptions (documented here)

**Known Audit Tools:**
- D13 dimension automated checks
- audit/scripts/pre_audit_checks.sh

**Future Updates:**
- Add new exceptions as patterns emerge
- Update category descriptions if design patterns change
- Maintain audit tool compatibility

---

## Summary Statistics

**Total Known Exceptions:** 19 files

**By Category:**
- Category A (S5 Iteration Files): 14 files
- Category B (S5 Design/Migration Documents): 2 files
- Category C (Optional/Auxiliary): 3 files

**Missing Sections:**
- Missing Prerequisites only: 5 files (s5 iterations 5, 5a, 6, 6a, 7 with inline statements)
- Missing Exit Criteria only: 3 files (s3_parallel_work_sync, s4_feature_testing_card, s4_test_strategy_development)
- Missing BOTH: 11 files (remaining s5 iteration files + 2 design docs)

**Design Patterns:**
- Router + Iteration: 14 files (S5 structure)
- Design/Migration Reference: 2 files (S5 v1→v2 documentation)
- Optional/Conditional: 1 file (s3_parallel_work_sync)
- Reference Material: 2 files (s4_feature_testing_card, s4_test_strategy_development)

---

**Last Verified:** 2026-02-05 (Round 3 audit)
**Next Review:** When new stage/iteration guides added, or if D13 check patterns change

