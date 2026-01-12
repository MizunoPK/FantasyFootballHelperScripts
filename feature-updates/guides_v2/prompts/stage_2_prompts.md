# Stage 2 Prompts: Feature Deep Dive

**Stage:** 2
**Purpose:** Feature specification and requirement clarification

---

## Starting Stage 2: Feature Deep Dive

**User says:** "Help me develop the {feature_name} feature" or "Let's work on feature_01"

**Prerequisite:** Stage 1 complete (epic folder and feature folders created)

**Agent MUST respond:**

```
I'm reading `stages/s2/s2_feature_deep_dive.md` to ensure I follow the complete deep dive workflow...

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
✅ Epic folder exists: `feature-updates/KAI-{N}-{epic_name}/`
✅ Feature folder exists: `feature_{NN}_{name}/`
✅ Stage 1 complete (EPIC_README.md shows Stage 1 complete)

**I'll now proceed with Phase 1 (Targeted Research for THIS feature only)...**

**Updating feature README Agent Status:**
- Current Phase: PLANNING
- Current Guide: stages/s2/s2_feature_deep_dive.md
- Guide Last Read: {YYYY-MM-DD HH:MM}
- Critical Rules: "NEVER assume - confirm with user first", "Targeted research only", "ONE question at a time", "Only confirmed info in spec.md", "Checklist all [x] required"
- Next Action: Begin targeted research for {feature_name}

Starting Phase 1...
```

---

## User Checklist Approval (Gate 2 - 🚨 MANDATORY)

**User says:** Agent detects Phase 2.5 complete (Spec-to-Epic Alignment Check PASSED) OR user asks "what's in the checklist?"

**Prerequisite:** Phase 2.5 (Spec-to-Epic Alignment Check) PASSED, checklist.md created with questions

**🚨 MANDATORY CHECKPOINT - USER MUST ANSWER ALL CHECKLIST QUESTIONS BEFORE PROCEEDING**

**Agent MUST respond:**

```
Phase 2.5 (Spec-to-Epic Alignment Check) has passed. I've created checklist.md with {N} questions that need your input before we can proceed to implementation planning.

**This is Gate 2 (User Checklist Approval) - a mandatory checkpoint to ensure you see all uncertainties before implementation.**

**Checklist Summary:**
- Functional Questions: {count}
- Technical Questions: {count}
- Integration Questions: {count}
- Error Handling Questions: {count}
- Testing Questions: {count}
- Dependencies & Blockers: {count}

**Total Questions:** {N}

**File Location:** `feature-updates/KAI-{N}-{epic_name}/feature_{XX}_{name}/checklist.md`

**How this works:**
1. You review each question in checklist.md
2. Each question has:
   - **Context:** Why this is uncertain
   - **User Answer:** (blank - you fill this in)
   - **Impact on spec.md:** What will be updated based on your answer
3. You provide answers (all at once or one at a time - your choice)
4. I update spec.md based on your answers
5. Once all {N} questions are answered, we proceed to implementation planning

**Why this matters:**
- You see ALL uncertainties before implementation planning starts
- You make ALL decisions (I don't make assumptions)
- Early approval is cheap to change; implementation changes are expensive
- This ensures we're aligned before writing a detailed implementation plan

**What format works best for you?**
- Option A: Review checklist.md and provide all {N} answers at once
- Option B: Go through questions one at a time interactively
- Option C: Ask me to clarify any questions first, then provide answers

Please let me know how you'd like to proceed.
```

**After user provides answers:**

```
Thank you for answering {Q#}. I'm updating spec.md to incorporate your answer...

[Agent updates spec.md with user's answer, marks item [x] in checklist.md]

Updated spec.md section: {section_name}
Updated checklist.md: Question {Q#} marked [x] with your answer documented

{If more questions remain:}
{N-1} questions remaining. {Ask for next answer or wait based on user's chosen format}

{If all questions answered:}
All {N} questions answered! ✅

Gate 2 (User Checklist Approval) status: ✅ PASSED

I'm documenting your approval in checklist.md...

**Next Steps:**
- spec.md has been updated with all your answers
- checklist.md shows all questions resolved (0 pending)
- Ready to proceed to Stage 5a (Implementation Planning)

Would you like me to proceed to Stage 5a, or would you like to review the updated spec.md first?
```

---

*For prompts for other stages, see the [prompts index](../prompts_reference_v2.md)*
