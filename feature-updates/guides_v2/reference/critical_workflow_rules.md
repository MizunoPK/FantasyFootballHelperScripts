# Critical Workflow Rules

**Status:** Reference document for S2/S4/S6 stages
**Last Updated:** 2026-02-10
**Usage:** Copied to README Agent Status during workflow execution

---

## Critical Rules

```text
┌─────────────────────────────────────────────────────────────┐
│ CRITICAL RULES - These MUST be copied to README Agent Status │
└─────────────────────────────────────────────────────────────┘

1. ⚠️ ONE question at a time (NEVER batch questions)
   - Ask question
   - Wait for user answer
   - Update spec/checklist IMMEDIATELY
   - Evaluate for new questions
   - Then ask next question

1.5. ⚠️ INVESTIGATION COMPLETE ≠ QUESTION RESOLVED
   - Agent investigates → Status: PENDING USER APPROVAL
   - User explicitly approves → Status: RESOLVED
   - NEVER mark questions as resolved without explicit approval
   - Research findings ≠ User approval

   WRONG: Investigate → Mark RESOLVED → Add requirement
   CORRECT: Investigate → Mark PENDING → User approves →
            Mark RESOLVED → Add requirement

2. ⚠️ Update spec.md and checklist.md IMMEDIATELY after each answer
   - Do NOT batch updates
   - Keep files current in real-time
   - Document user's exact answer or paraphrase

3. ⚠️ If checklist grows >35 items, STOP and propose split
   - Trigger: More than 35 checklist items
   - Action: Propose splitting into multiple features
   - Requirement: Get user approval before splitting
   - If approved: Return to S1 to create new features

4. ⚠️ Cross-feature alignment is MANDATORY (not optional)
   - Compare to ALL features with "S2 Complete"
   - Look for: Conflicts, duplicates, incompatible assumptions
   - Resolve conflicts before proceeding
   - Document alignment verification

5. ⚠️ Acceptance criteria require USER APPROVAL (mandatory gate)
   - Create "Acceptance Criteria" section in spec.md
   - List EXACT files, structures, behaviors
   - Present to user for approval
   - Wait for explicit approval
   - Document approval timestamp

6. ⚠️ Every user answer creates new requirement with traceability
   - Source: "User Answer to Question N (checklist.md)"
   - Add to spec.md immediately
   - Update checklist to mark question resolved
```

---

## Usage Instructions

**When to copy these rules:**
- Beginning of S2.P2 (Specification Phase)
- Beginning of S2.P3 (Refinement Phase)
- Beginning of S4 (Feature Testing Strategy)
- Beginning of S6 (Execution)

**Where to copy:**
- Feature README.md → Agent Status section → "Critical Rules from Current Guide"
- Keep rules visible during execution for reference

**Why these rules matter:**
- Prevent common anti-patterns (batching questions, marking RESOLVED prematurely)
- Ensure user approval gates are respected
- Maintain traceability and real-time documentation
- Prevent scope creep (>35 item trigger)

---

**Referenced by:**
- `stages/s2/s2_p2_specification.md`
- `stages/s2/s2_p2_5_spec_validation.md`
- `stages/s2/s2_p3_refinement.md`
- `stages/s4/s4_feature_testing_strategy.md`
- `stages/s6/s6_execution.md`

---

*End of critical_workflow_rules.md*
