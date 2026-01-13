# Feature Checklist Template

**Filename:** `checklist.md`
**Location:** `feature-updates/KAI-{N}-{epic_name}/feature_XX_{name}/checklist.md`
**Created:** S2 (Feature Deep Dive)

**Purpose:** Track unresolved questions and decisions that require user input. Agent creates questions during S2, user provides answers, agent updates spec.md accordingly.

**🚨 CRITICAL: Agents CANNOT mark items as resolved autonomously. Only user can confirm resolution.**

---

## Template

```markdown
# Feature Checklist: {feature_name}

**Part of Epic:** {epic_name}
**Created:** {YYYY-MM-DD}
**Last Updated:** {YYYY-MM-DD HH:MM}
**Status:** {🔄 PENDING USER REVIEW / ✅ USER APPROVED}

---

## Purpose

This checklist contains **questions and decisions that require user input**.

**Agent creates questions during S2 research. User reviews and answers ALL questions. Only after user approval can S5 begin.**

**Format:**
- `[ ]` = Question pending user answer
- `[x]` = User provided answer (agent updated spec.md)

**🚨 AGENTS: You CANNOT mark items `[x]` yourself. Create questions, wait for user to answer.**

---

## Functional Questions

**Instructions for agents:** List questions about feature scope, requirements, behavior. DO NOT attempt to answer them yourself.

**Example questions:**
- [ ] **Q1:** Should this feature handle edge case X, or is it out of scope?
  - **Context:** {Explain why this is uncertain}
  - **User Answer:** {Leave blank - user will answer}
  - **Impact on spec.md:** {What section will be updated based on answer}

- [ ] **Q2:** When behavior Y happens, should we do A or B?
  - **Context:** {Explain the two approaches}
  - **User Answer:** {Leave blank}
  - **Impact on spec.md:** {What will change}

{Agents: Add your functional questions here using the format above}

---

## Technical Questions

**Instructions for agents:** List questions about algorithms, data structures, implementation approach. DO NOT make technical decisions autonomously.

**Example questions:**
- [ ] **Q3:** Should we use approach A (faster but more memory) or approach B (slower but less memory)?
  - **Context:** {Explain trade-offs}
  - **User Answer:** {Leave blank}
  - **Impact on spec.md:** {Algorithm section will specify chosen approach}

{Agents: Add your technical questions here}

---

## Integration Questions

**Instructions for agents:** List questions about how this feature integrates with existing systems. DO NOT assume integration points.

**Example questions:**
- [ ] **Q4:** Should this feature call existing method X, or create a new integration point?
  - **Context:** {Explain existing method X and why uncertain}
  - **User Answer:** {Leave blank}
  - **Impact on spec.md:** {Components Affected section}

{Agents: Add your integration questions here}

---

## Error Handling Questions

**Instructions for agents:** List questions about error scenarios and handling strategy. DO NOT define error handling autonomously.

**Example questions:**
- [ ] **Q5:** When error X occurs, should we fail silently, log warning, or raise exception?
  - **Context:** {Explain when error X can occur}
  - **User Answer:** {Leave blank}
  - **Impact on spec.md:** {Error handling section}

{Agents: Add your error handling questions here}

---

## Testing Questions

**Instructions for agents:** List questions about test strategy, coverage requirements. DO NOT decide test approach autonomously.

**Example questions:**
- [ ] **Q6:** Do you want unit tests only, or also integration tests for this feature?
  - **Context:** {Explain complexity and testing needs}
  - **User Answer:** {Leave blank}
  - **Impact on spec.md:** {Testing section or epic_smoke_test_plan.md}

{Agents: Add your testing questions here}

---

## Open Questions (Uncategorized)

**Instructions for agents:** Any other questions that don't fit above categories.

- [ ] **Q7:** {Your question}
  - **Context:** {Why this is uncertain}
  - **User Answer:** {Leave blank}
  - **Impact on spec.md:** {What will be updated}

{Agents: Add any other questions here}

---

## Dependencies & Blockers

**Instructions for agents:** List dependencies on other features or external systems that need verification.

- [ ] **DEP1:** {Dependency description - e.g., "Feature 02 must expose method X for this to work"}
  - **Verification Needed:** {What user needs to confirm}
  - **User Confirmation:** {Leave blank}
  - **If blocked:** {What happens if this dependency isn't available}

{Agents: Add dependencies requiring user verification here}

---

## Checklist Status

**Total Questions:** {N}
**User Answered:** {X}
**Pending User Input:** {Y}

**Status:** {🔄 PENDING USER REVIEW / ✅ USER APPROVED}

**If PENDING:**
- **Next Action:** Agent presents checklist to user for review (Gate 2 - User Checklist Approval)
- **User must answer ALL questions before S5 can begin**

**If APPROVED:**
- **User Approval Date:** {YYYY-MM-DD HH:MM}
- **spec.md updated:** ✅ All answers incorporated into specification
- **Ready for S5:** ✅ Can proceed to Implementation Planning

---

## User Approval Section
*This section is filled out after user reviews and approves*

**User Reviewed:** {YYYY-MM-DD HH:MM}
**User Approval:** {✅ APPROVED / 🔄 REVISIONS REQUESTED}

**User Comments:**
{Any additional guidance or context from user}

**Revisions Requested (if any):**
- {Revision 1}
- {Revision 2}

**Final Approval:** {✅ APPROVED - proceed to S5 / ⏳ Awaiting revisions}

---

**Remember:** This checklist exists to PREVENT autonomous agent decisions. If you're uncertain, ADD A QUESTION. Don't research and decide yourself—that's what caused the problem we're fixing.
```

---

## Usage Instructions for Agents

**During S2 (Feature Deep Dive):**

1. **Create checklist.md** at start of S2
2. **As you research the feature, ADD QUESTIONS** (not decisions)
3. **DO NOT mark items `[x]`** - only user can do this
4. **DO NOT attempt to resolve questions yourself** - research to understand the question, not answer it
5. **After spec.md is written, review for uncertainties** - add any missed questions to checklist
6. **Present checklist to user** using the "User Checklist Approval" prompt
7. **Wait for user to answer ALL questions**
8. **After user approval, update spec.md** with user's answers
9. **Mark items `[x]` based on user confirmation** (not your own judgment)
10. **Proceed to S5** only after checklist shows ✅ USER APPROVED

**Key Principle:** Checklist is for QUESTIONS you need answered, not DECISIONS you've made.

**If you find yourself writing:**
- ❌ "Decision: We'll use approach X" → Wrong, this should be a question
- ❌ "[x] Algorithm defined" → Wrong, did user confirm it?
- ✅ "[ ] Q1: Should we use algorithm A or B?" → Correct format

---

## What Changed from Previous Template

**OLD Template (Autonomous Resolution):**
- Agents marked items `[x]` based on their research
- Checklist had "resolved decisions" that user never saw
- No user approval gate
- Agents made autonomous choices

**NEW Template (User Approval Required):**
- Agents create QUESTIONS only
- User must answer every question
- Gate 2: User Checklist Approval required
- Zero autonomous resolution
- Clear user visibility into all uncertainties

---

**See also:** `prompts/stage_2_prompts.md` for "User Checklist Approval" prompt
