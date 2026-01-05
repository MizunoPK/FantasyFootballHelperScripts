# Stage 2 Prompts: Feature Deep Dive

**Stage:** 2
**Purpose:** Feature specification and requirement clarification

---

## Starting Stage 2: Feature Deep Dive

**User says:** "Help me develop the {feature_name} feature" or "Let's work on feature_01"

**Prerequisite:** Stage 1 complete (epic folder and feature folders created)

**Agent MUST respond:**

```
I'm reading `stages/stage_2/feature_deep_dive.md` to ensure I follow the complete deep dive workflow...

**The guide requires:**
- **🚨 CRITICAL: NEVER MAKE ASSUMPTIONS**
  - Do NOT assume requirements, methodologies, or behavior
  - ASK USER via checklist.md questions BEFORE asserting in spec.md
  - Only document requirements after explicit user confirmation
  - If uncertain → create question, do NOT assume answer
- Phase 1: Targeted research (ONLY for THIS feature's scope, not entire epic)
- Phase 2: Update spec.md and checklist.md with findings
  - Only write CONFIRMED information in spec.md (not assumptions)
  - Uncertain items go in checklist.md as questions
- Phase 3: Interactive question resolution
  - ONE question at a time (Lesson learned: don't batch questions)
  - Update spec/checklist after EACH answer
  - Evaluate for new questions after each resolution
- Phase 4: Feature complete + dynamic scope adjustment check
  - If feature grew >30% in complexity → Propose split into 2 features
  - If new dependencies discovered → Create new features if needed
- Phase 5: **Compare to completed feature specs** (if any features already done)
  - Ensure alignment with previous features
  - Maintain consistency in approach
- Checklist.md ALL items must be resolved (marked [x]) before Stage 2 complete

**Prerequisites I'm verifying:**
✅ Epic folder exists: `feature-updates/{epic_name}/`
✅ Feature folder exists: `feature_{NN}_{name}/`
✅ Stage 1 complete (EPIC_README.md shows Stage 1 complete)

**I'll now proceed with Phase 1 (Targeted Research for THIS feature only)...**

**Updating feature README Agent Status:**
- Current Phase: PLANNING
- Current Guide: stages/stage_2/feature_deep_dive.md
- Guide Last Read: {YYYY-MM-DD HH:MM}
- Critical Rules: "NEVER assume - confirm with user first", "Targeted research only", "ONE question at a time", "Only confirmed info in spec.md", "Checklist all [x] required"
- Next Action: Begin targeted research for {feature_name}

Starting Phase 1...
```

---

*For prompts for other stages, see the [prompts index](../prompts_reference_v2.md)*
