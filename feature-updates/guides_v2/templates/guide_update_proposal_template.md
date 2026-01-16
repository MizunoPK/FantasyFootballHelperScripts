# Guide Update Proposal - KAI-{N}-{epic_name}

**Epic:** KAI-{N}-{epic_name}
**Date:** {YYYY-MM-DD}
**Agent:** Claude Sonnet 4.5
**Total Proposals:** {N} ({P0} critical, {P1} high, {P2} medium, {P3} low)

---

## Summary

**Lessons Learned Count:**
- Epic-level: {N} lessons
- Feature-level: {N} lessons across {N} features
- Total: {N} lessons analyzed

**Guide Gaps Identified:**
- {N} critical gaps (P0)
- {N} high-priority improvements (P1)
- {N} medium-priority improvements (P2)
- {N} low-priority improvements (P3)

**Recommended Action:** Review all proposals, prioritize P0 and P1 for approval

---

## P0: Critical Fixes (Must Review)

### Proposal P0-1: {Short descriptive title}

**Lesson Learned:**
> "{Direct quote from lessons_learned.md}"

**Source File:** `{epic or feature}/lessons_learned.md` - Lesson #{N}

**Root Cause:**
{Why this issue occurred - be specific about what was missing/unclear in guides}

**Affected Guide(s):**
- `{path/to/guide.md}` - Section: "{section name}" (Lines {start}-{end})

**Current State (BEFORE):**
```markdown
{Current text from guide - exact quote with line numbers}
```

**Proposed Change (AFTER):**
```markdown
{Proposed new text - show complete replacement or addition}
```

**Rationale:**
{How this specific change prevents future agents from encountering the same issue}

**Impact Assessment:**
- **Who benefits:** {Which agents/stages benefit from this change}
- **When it helps:** {Specific situations where this guidance is needed}
- **Severity if unfixed:** Critical - {specific bad outcome that will occur}

**User Decision:** [ ] Approve  [ ] Modify  [ ] Reject  [ ] Discuss

**User Feedback/Modifications:**
```
{User writes alternative approach, questions, or modifications here}
```

---

### Proposal P0-2: {Title}

{Repeat same structure for each P0 proposal}

---

## P1: High Priority (Strongly Recommended)

### Proposal P1-1: {Short descriptive title}

**Lesson Learned:**
> "{Direct quote from lessons_learned.md}"

**Source File:** `{epic or feature}/lessons_learned.md` - Lesson #{N}

**Root Cause:**
{Why this issue occurred}

**Affected Guide(s):**
- `{path/to/guide.md}` - Section: "{section name}" (Lines {start}-{end})

**Current State (BEFORE):**
```markdown
{Current text from guide}
```

**Proposed Change (AFTER):**
```markdown
{Proposed new text}
```

**Rationale:**
{How this change prevents future issues}

**Impact Assessment:**
- **Who benefits:** {Which agents/stages}
- **When it helps:** {Specific situations}
- **Severity if unfixed:** High - {moderate bad outcome}

**User Decision:** [ ] Approve  [ ] Modify  [ ] Reject  [ ] Discuss

**User Feedback/Modifications:**
```
{User writes response here}
```

---

### Proposal P1-2: {Title}

{Repeat structure...}

---

## P2: Medium Priority (Consider)

### Proposal P2-1: {Short descriptive title}

**Lesson Learned:**
> "{Direct quote from lessons_learned.md}"

**Source File:** `{epic or feature}/lessons_learned.md` - Lesson #{N}

**Root Cause:**
{Why this issue occurred}

**Affected Guide(s):**
- `{path/to/guide.md}` - Section: "{section name}" (Lines {start}-{end})

**Current State (BEFORE):**
```markdown
{Current text from guide}
```

**Proposed Change (AFTER):**
```markdown
{Proposed new text}
```

**Rationale:**
{How this change improves clarity or efficiency}

**Impact Assessment:**
- **Who benefits:** {Which agents/stages}
- **When it helps:** {Specific situations}
- **Severity if unfixed:** Medium - {minor confusion or inefficiency}

**User Decision:** [ ] Approve  [ ] Modify  [ ] Reject  [ ] Discuss

**User Feedback/Modifications:**
```
{User writes response here}
```

---

### Proposal P2-2: {Title}

{Repeat structure...}

---

## P3: Low Priority (Nice-to-Have)

### Proposal P3-1: {Short descriptive title}

**Lesson Learned:**
> "{Direct quote from lessons_learned.md}"

**Source File:** `{epic or feature}/lessons_learned.md` - Lesson #{N}

**Root Cause:**
{Why this minor issue occurred}

**Affected Guide(s):**
- `{path/to/guide.md}` - Section: "{section name}" (Lines {start}-{end})

**Current State (BEFORE):**
```markdown
{Current text from guide}
```

**Proposed Change (AFTER):**
```markdown
{Proposed new text}
```

**Rationale:**
{How this minor change improves guide quality}

**Impact Assessment:**
- **Who benefits:** {Which agents/stages}
- **When it helps:** {Specific situations}
- **Severity if unfixed:** Low - {cosmetic or very minor issue}

**User Decision:** [ ] Approve  [ ] Modify  [ ] Reject  [ ] Discuss

**User Feedback/Modifications:**
```
{User writes response here}
```

---

### Proposal P3-2: {Title}

{Repeat structure...}

---

## User Approval Summary

**Instructions:**
1. Review each proposal individually (start with P0, then P1, P2, P3)
2. Mark your decision in "User Decision" checkbox: Approve / Modify / Reject / Discuss
3. For "Modify", provide alternative text in "User Feedback/Modifications" section
4. For "Discuss", ask questions or request clarification in "User Feedback/Modifications" section
5. Agent will apply only approved changes (or your modifications)

**Guidelines:**
- **P0 (Critical):** Strongly recommended - prevents major bugs or misinterpretations
- **P1 (High):** Recommended - significantly improves quality or reduces rework
- **P2 (Medium):** Consider - moderate improvements, clarifies ambiguity
- **P3 (Low):** Optional - minor improvements, cosmetic fixes

**Approval Statistics:**
- Total proposals: {N}
- P0 proposals: {N} (critical)
- P1 proposals: {N} (high)
- P2 proposals: {N} (medium)
- P3 proposals: {N} (low)

**After User Review:**
- Approved: {N}
- Modified: {N}
- Rejected: {N}
- Pending discussion: {N}

**Next Steps:**
- [ ] Agent applies approved changes to guides
- [ ] Agent applies user modifications to guides
- [ ] Agent creates separate commit for guide updates
- [ ] Agent updates `reference/guide_update_tracking.md` with applied changes
- [ ] Agent updates `guide-updates.txt` if any items addressed
- [ ] Agent proceeds with epic commit (S10 Step 7)

---

**Last Updated:** {YYYY-MM-DD HH:MM}
