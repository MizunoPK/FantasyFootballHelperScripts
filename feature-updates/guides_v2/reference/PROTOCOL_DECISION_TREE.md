# Protocol Decision Tree

When you discover an issue or gap during epic development, use this decision tree to determine which protocol to follow.

---

## 🔀 Decision Flowchart

```text
Issue/Gap Discovered
│
├─ Question 1: Do you know the SOLUTION?
│  │
│  ├─ YES → Is it a NEW requirement the user didn't ask for?
│  │  │
│  │  ├─ YES → MISSED REQUIREMENT PROTOCOL
│  │  │  Example: "We need to add email validation"
│  │  │  → Create feature_{XX}_{name}/ folder
│  │  │  → User decides priority
│  │  │  → Return to S2 for planning
│  │  │
│  │  └─ NO → Just implement it (regular work)
│  │     Example: "Refactor this method"
│  │     → Not a missing requirement, just implementation detail
│  │
│  └─ NO → Requires investigation?
│     │
│     ├─ YES → DEBUGGING PROTOCOL
│     │  Example: "Player scores are incorrect but we don't know why"
│     │  → Create debugging/ISSUES_CHECKLIST.md
│     │  → Investigation rounds (Phase 2)
│     │  → Root cause analysis (Phase 4b)
│     │
│     └─ NO → Ask user for clarification
│        Example: "Should we handle this edge case?"
│        → Add to questions.md
│        → Wait for user answer
```markdown

---

## Quick Reference Table

| Situation | Protocol | Key Indicators |
|-----------|----------|----------------|
| **Known solution + NEW requirement** | Missed Requirement | User didn't request it, you're adding scope |
| **Unknown root cause** | Debugging | Need investigation to understand the problem |
| **Known solution + NOT new requirement** | Regular Work | Implementation detail, code quality improvement |
| **Need user input** | Ask User | Unclear requirements, multiple valid approaches |

---

## Detailed Scenario Examples

### Scenario 1: Empty Player Name Bug

**Discovery:** During QC testing, system crashes when player name is empty

**Analysis:**
- Do we know the solution? → **NO** (need to investigate why it crashes)
- Requires investigation? → **YES**

**Decision:** ✅ **DEBUGGING PROTOCOL**

**Reasoning:**
- Root cause unknown (could be validation missing, could be null pointer, could be data structure issue)
- Need investigation rounds to find root cause
- Phase 4b will identify which stage should have caught this

**Actions:**
1. Create `debugging/ISSUES_CHECKLIST.md` (feature-level or epic-level)
2. Add issue to checklist: "Player name validation crash"
3. Enter Debugging Protocol Phase 2 (Investigation)
4. Trace code to find crash location
5. Identify root cause through hypothesis testing
6. Implement fix (Phase 3)
7. Get user verification (Phase 4)
8. Perform root cause analysis (Phase 4b - MANDATORY)
9. Loop back to testing (Phase 5)

---

### Scenario 2: Forgot Email Validation

**Discovery:** During implementation, realize spec didn't include email validation

**Analysis:**
- Do we know the solution? → **YES** (add email regex validation)
- Is it a NEW requirement? → **YES** (not in original spec)

**Decision:** ✅ **MISSED REQUIREMENT PROTOCOL**

**Reasoning:**
- Solution is known (email validation)
- User didn't ask for it originally
- Need user to confirm this requirement
- Return to S2 to plan properly

**Actions:**
1. STOP current work
2. Use "Creating Missed Requirement" prompt from `prompts_reference_v2.md`
3. READ: `missed_requirement/missed_requirement_protocol.md`
4. Present options to user:
   - Create new `feature_XX_email_validation/` folder
   - OR add to existing unstarted feature
5. User decides: approach + priority (high/medium/low)
6. Return to S2 (Deep Dive) for new/updated feature
7. Return to S3 (Sanity Check) to re-align ALL features
8. Return to S4 (Test Strategy) to update epic test plan
9. Resume paused work
10. Implement new/updated feature when its turn comes

---

### Scenario 3: Refactor Long Method

**Discovery:** During implementation, notice method is 200 lines long

**Analysis:**
- Do we know the solution? → **YES** (break into smaller methods)
- Is it a NEW requirement? → **NO** (implementation detail)

**Decision:** ✅ **Just implement it (regular work)**

**Reasoning:**
- Not a missing requirement (just code quality)
- Not a bug requiring investigation
- Part of normal implementation process

**Actions:**
1. Extract helper methods
2. Add appropriate docstrings
3. Update tests if needed
4. Continue with implementation

---

### Scenario 4: Unclear Edge Case

**Discovery:** During planning, unsure if we should handle negative ADP values

**Analysis:**
- Do we know the solution? → **NO** (need user input)
- Requires investigation? → **NO** (need clarification)

**Decision:** ✅ **Add to questions.md, ask user**

**Reasoning:**
- Not a bug (hasn't been implemented yet)
- Not a missing requirement (unclear if it should exist)
- Need user decision before proceeding

**Actions:**
1. Add question to `questions.md` or `checklist.md`:
   ```markdown
   ## Edge Case: Negative ADP Values

   **Context:** ADP values are typically 1-300, but some data sources may have negative values.

   **Question:** Should we handle negative ADP values? Options:
   - Reject as invalid (validation error)
   - Treat as "undrafted" (ADP = 999)
   - Use absolute value
   - Other?

   **Impact on spec.md:**
   - Validation section will specify ADP range
   - Error handling for invalid ADP values
   ```
2. Wait for user answer
3. Update spec.md based on user's decision
4. Continue with implementation

---

## Common Mistakes and Corrections

### ❌ Mistake: Treating Known Issues as Unknown

**Scenario:** You know a method needs refactoring but enter Debugging Protocol

**Problem:** Wastes time on unnecessary investigation

**Correction:** If you know the solution AND it's not a new requirement → Just implement it

---

### ❌ Mistake: Implementing New Requirements Without User Approval

**Scenario:** You add email validation without checking if user wants it

**Problem:** Adds unauthorized scope, may not align with user's goals

**Correction:** If it's a NEW requirement → Use Missed Requirement Protocol, get user approval

---

### ❌ Mistake: Guessing at Requirements

**Scenario:** Unsure about edge case handling, so you guess "probably reject as invalid"

**Problem:** Assumptions may be wrong, leading to rework

**Correction:** If unclear → Add to questions.md, ask user for clarification

---

### ❌ Mistake: Skipping Root Cause Analysis

**Scenario:** Bug fixed, moving on without understanding why it happened

**Problem:** Similar bugs will recur, workflow not improved

**Correction:** ALWAYS do Phase 4b (Root Cause Analysis) after fixing bugs

---

## Protocol Reference Links

**Missed Requirement Protocol:**
- Guide: `feature-updates/guides_v2/missed_requirement/missed_requirement_protocol.md`
- Prompt: See "Creating Missed Requirement" in `prompts_reference_v2.md`

**Debugging Protocol:**
- Guide: `feature-updates/guides_v2/debugging/debugging_protocol.md`
- Prompt: See "Starting Debugging Protocol" in `prompts_reference_v2.md`

**Questions Management:**
- S2: Add to `checklist.md` (QUESTION-ONLY format)
- S5: Add to `questions.md` (if NEW questions arise during iterations)

---

## When in Doubt

**If you're unsure which protocol to use:**

1. **Check:** Is it a bug with unknown root cause?
   - YES → Debugging Protocol
   - NO → Continue to step 2

2. **Check:** Is it a new requirement the user didn't ask for?
   - YES → Missed Requirement Protocol
   - NO → Continue to step 3

3. **Check:** Do you know what to do?
   - YES → Just implement it (regular work)
   - NO → Ask user for clarification

**Golden Rule:** When in doubt, ask the user. It's better to get clarification than to make incorrect assumptions.
