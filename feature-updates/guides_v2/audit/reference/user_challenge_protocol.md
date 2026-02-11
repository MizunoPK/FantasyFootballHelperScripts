# User Challenge Protocol

**Purpose:** How to respond when user challenges audit findings or completeness
**Audience:** Agents conducting audits (especially Stage 5 Loop Decision)
**Last Updated:** 2026-02-05

---

## Table of Contents

1. [Core Principle](#core-principle)
2. [Common Challenge Types](#common-challenge-types)
3. [Response Protocols](#response-protocols)
4. [Loop-Back Procedure](#loop-back-procedure)
5. [Evidence Collection](#evidence-collection)
6. [Learning from Challenges](#learning-from-challenges)

---

## Core Principle

### User Challenges Are Usually Correct

```text
┌─────────────────────────────────────────────────────────────────┐
│  🚨 CRITICAL: When user challenges you, THEY ARE USUALLY RIGHT  │
│                                                                  │
│  DO NOT:                                                         │
│  ❌ Defend your findings                                        │
│  ❌ Argue about completeness                                    │
│  ❌ Explain why your audit was thorough                         │
│                                                                  │
│  DO:                                                             │
│  ✅ Acknowledge the challenge                                   │
│  ✅ Immediately loop back to Round 1                            │
│  ✅ Use completely different patterns                           │
│  ✅ Assume you missed something significant                     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Why User Challenges Matter

**Historical Evidence from audit_overview.md:**
> "Premature completion claims: 3 times (each time, 50+ more issues found)"
> "User challenges: 3 ('are you sure?', 'did you actually make fixes?', 'assume everything is wrong')"

**Pattern:**
- Agent claimed audit complete
- User expressed doubt
- Agent re-audited
- Found 50+ additional issues each time

**Lesson:** User skepticism = red flag you missed something

---

## Common Challenge Types

### Challenge Type 1: "Are you sure?"

**What it means:**
- User doubts completeness
- Likely sees patterns you missed
- Your confidence may be overestimated

**Example Scenarios:**
```text
User: "Are you sure you checked all the files?"
User: "Are you sure there are no more instances?"
User: "You really found zero issues in Round 3?"
```

**What triggered it:**
- Too few issues found (user expected more)
- Round completed too quickly (seemed rushed)
- Verification seemed superficial
- Historical knowledge (user knows area is problematic)

**Appropriate Response:**
```markdown
You're right to question this. I will immediately loop back to Round 1 with:

1. **Completely different patterns** - I'll use pattern variations I didn't try
2. **Different search order** - I'll search folders in different sequence
3. **Manual reading** - I'll spot-read 20+ random files
4. **Assumption of error** - I'll assume I missed something significant

Starting Round [N+1] now.
```

**DO NOT say:**
- "I'm confident in my findings"
- "I checked thoroughly"
- "I used multiple patterns"
- Any defensive response

---

### Challenge Type 2: "Did you actually make fixes?"

**What it means:**
- User doesn't see evidence of changes
- Verification may be incomplete
- Fix plan may not have been executed

**Example Scenarios:**
```text
User: "Did you actually make fixes or just report them?"
User: "I still see the same issues in the files"
User: "Can you show me before/after evidence?"
```

**What triggered it:**
- No git commits shown
- No file changes visible
- Verification report has counts but no examples
- User spot-checked file, still sees issue

**Appropriate Response:**
```markdown
You're absolutely right - let me provide concrete evidence.

**Files Modified (with before/after examples):**

**File 1:** path/to/file.md
- **Before:** [exact line before fix]
- **After:** [exact line after fix]

**File 2:** path/to/file.md
- **Before:** [exact line before fix]
- **After:** [exact line after fix]

[Repeat for 5-10 examples showing actual changes]

**Git Commits:**
```bash
git log --oneline | head -5
[show actual commits with audit fixes]
```

**Verification:**
```bash
# Re-run discovery pattern
grep -rn "pattern" --include="*.md" .
# Output: [show zero or documented remaining instances]
```text

If you cannot provide this evidence, loop back immediately.
```

**DO NOT say:**
- "I already showed this"
- "Check the verification report"
- Assume user will trust claimed fixes

---

### Challenge Type 3: "Assume everything is wrong"

**What it means:**
- User wants adversarial mindset
- Previous rounds were too optimistic
- Need fresh eyes with zero assumptions

**Example Scenarios:**
```text
User: "Assume everything is wrong and re-audit"
User: "Start from scratch with zero trust"
User: "Question every finding from previous rounds"
```

**What triggered it:**
- Multiple rounds found issues (no clean round yet)
- User lost confidence in audit methodology
- User knows codebase has systemic issues
- Previous audits were incomplete

**Appropriate Response:**
```markdown
Understood. Restarting audit with adversarial mindset:

**New Audit Approach:**

1. **Assume all files have errors** - Check EVERY file, no skipping
2. **Question previous findings** - Re-verify issues marked "fixed"
3. **Use new patterns** - Don't rely on previous search strategies
4. **Manual validation** - Read files directly, not just grep
5. **Zero confidence threshold** - Won't exit until 5+ consecutive clean rounds

**Starting Round 1 (Fresh Start):**
[Begin discovery with completely new approach]
```

**DO NOT:**
- Reference previous rounds' findings
- Assume any previous work was correct
- Use same patterns as before

---

### Challenge Type 4: "I found an issue you missed"

**What it means:**
- User found concrete evidence audit was incomplete
- Specific blind spot in your methodology
- Need to understand why you missed it

**Example Scenarios:**
```text
User: "You missed this file: [path/to/file.md]"
User: "Line 45 of README.md still has old notation"
User: "The templates folder wasn't checked"
```

**What triggered it:**
- User spot-checked files
- User knows specific problem area
- User testing workflow, found broken reference

**Appropriate Response:**
```markdown
Thank you for finding that. You're absolutely correct.

**Issue Confirmed:**
- File: [file user mentioned]
- Line: [line user mentioned]
- Pattern: [pattern user found]
- Status: MISSED in my audit

**Root Cause Analysis:**
Why did I miss this?
- [ ] Pattern wasn't in my search list
- [ ] File/directory wasn't in search scope
- [ ] Context analysis incorrectly marked as intentional
- [ ] Verification was incomplete
- [ ] Other: [specific reason]

**Corrective Action:**
1. Fix the specific issue immediately
2. Search for similar issues (same pattern, same location type)
3. Loop back to Round 1 with expanded patterns
4. Add user-found pattern to search list
5. Document blind spot to prevent recurrence

**Starting expanded audit now.**
```

**DO NOT:**
- Minimize the finding ("it's just one issue")
- Explain why you missed it (excuses)
- Fix only that one issue without broader search

---

## Response Protocols

### Protocol A: Immediate Loop Back

**When to use:**
- Any challenge type 1, 3, or 4
- User expresses doubt
- User questions completeness

**Procedure:**
```text
1. Acknowledge challenge immediately
   ↓
2. Do NOT defend findings
   ↓
3. Reset to Round 1, Sub-Round 1.1
   ↓
4. Use completely different patterns
   ↓
5. Assume previous audit missed significant issues
   ↓
6. Document what you'll do differently
```

### Protocol B: Provide Evidence First, Then Loop

**When to use:**
- Challenge type 2 ("did you make fixes?")
- User wants proof of work done

**Procedure:**
```text
1. Provide concrete before/after examples
   ↓
2. Show git commits with actual changes
   ↓
3. Re-run verification commands showing results
   ↓
4. Ask: "Does this evidence address your concern?"
   ↓
5. If user still has doubts → Loop back (Protocol A)
```

### Protocol C: Targeted Fix + Full Re-Audit

**When to use:**
- Challenge type 4 (user found specific issue)
- Concrete evidence of missed item

**Procedure:**
```text
1. Fix the specific issue user found
   ↓
2. Search for similar issues (same pattern/location)
   ↓
3. Root cause analysis (why missed?)
   ↓
4. Document blind spot
   ↓
5. Loop back with expanded patterns
```

---

## Loop-Back Procedure

### How to Loop Back After Challenge

**Step 1: Clear Context (5-10 minutes)**
```text
- Close all files from previous rounds
- Clear mental model of what was "already checked"
- Take short break
- Approach as if first time auditing
```

**Step 2: Analyze What Was Missed**
```text
- Review challenge specifics
- Identify blind spot category:
  ✓ Pattern variation not searched
  ✓ File/directory not in scope
  ✓ Context analysis error (false negative)
  ✓ Verification incomplete
  ✓ Assumption of correctness
```

**Step 3: Design New Approach**
```text
- Add new patterns addressing blind spot
- Expand search scope
- Add manual validation steps
- Increase verification rigor
```

**Step 4: Document Changes**
```markdown
## Round [N+1] - Post-Challenge

**Challenge Received:** [Type of challenge]
**Specific Issue:** [What user found/questioned]

**Blind Spot Identified:**
- [Why previous audit missed this]

**New Approach:**
1. [Pattern 1 - not used in previous rounds]
2. [Pattern 2 - not used in previous rounds]
3. [Pattern 3 - not used in previous rounds]
4. [Manual validation - files to manually read]
5. [Expanded scope - directories to include]

**Goal:** Find issues previous rounds missed
```

**Step 5: Execute Round N+1**
```text
- Start at Sub-Round 1.1 (Core Dimensions)
- Use new patterns designed in Step 3
- Assume EVERYTHING has errors
- Document ALL findings (even if seem minor)
- Provide evidence at each stage
```

---

## Evidence Collection

### What Constitutes Good Evidence

**Strong Evidence:**
✅ Before/after file diffs showing exact changes
✅ Git commit hashes with actual modifications
✅ Command output showing zero matches after fixes
✅ Screenshots of file contents (if helpful)
✅ Spot-check results from 10+ random files

**Weak Evidence:**
❌ "I checked and it's fixed"
❌ "Verification passed"
❌ "Zero issues found"
❌ Counts without examples
❌ Claims without proof

### Evidence Template

```markdown
## Evidence for [Issue Category]

**Pattern:** [Search pattern used]
**Files Checked:** [Number and list]

### Before Fixes

**Discovery Results:**
```bash
$ grep -rn "pattern" --include="*.md" .
file1.md:10: [match content]
file2.md:25: [match content]
[... showing N_found matches]
```
**Total Found:** N_found instances

### Fixes Applied

**Example 1:**
- **File:** file1.md:10
- **Before:** `old content`
- **After:** `new content`

**Example 2:**
- **File:** file2.md:25
- **Before:** `old content`
- **After:** `new content`

[Show 5-10 concrete examples]

### After Fixes (Verification)

**Verification Results:**
```bash
$ grep -rn "pattern" --include="*.md" .
[zero output OR documented intentional cases]
```
**Total Remaining:** 0 (or N with explanations)

### Git Evidence

```bash
$ git log --oneline | grep -i audit
abc123 feat/audit: Apply Round 3 fixes - notation standardization (70 files)
def456 feat/audit: Apply Round 2 fixes - file paths (15 files)
```markdown

### Spot-Check Results

**Random files checked:** 12 files
- file_1.md ✅ No issues
- file_2.md ✅ No issues
- file_3.md ✅ No issues
[... all clean]
```

---

## Learning from Challenges

### Post-Challenge Analysis

**After completing loop-back round, document:**

```markdown
## Challenge Post-Mortem - Round [N]

**Challenge Type:** [1, 2, 3, or 4]
**What User Found/Questioned:** [Specific concern]

**What I Missed:**
- [Specific issue or blind spot]

**Why I Missed It:**
- [ ] Pattern variation not in search list
- [ ] File/directory excluded from scope
- [ ] Incorrectly analyzed context (false negative)
- [ ] Insufficient verification
- [ ] Overconfidence in previous round
- [ ] Working from memory instead of re-reading
- [ ] Other: [specific reason]

**How Loop-Back Round Addressed It:**
- Added patterns: [list new patterns]
- Expanded scope: [what was added]
- Increased rigor: [what changed]

**Issues Found in Loop-Back:**
- N new issues discovered
- [Summary of findings]

**Lesson Learned:**
[What to do differently in future audits]

**Prevention:**
[How to avoid this blind spot in future Round 1 discovery]
```

### Common Blind Spots (Learn from These)

| Blind Spot | Why It Happens | Prevention |
|------------|----------------|------------|
| Root files not checked | Focus on stages/ directory only | Always check README.md, EPIC_WORKFLOW_USAGE.md, prompts_reference_v2.md |
| Pattern variations missed | Used exact match only | Always check variations: punctuation, spacing, case |
| Context analysis errors | Assumed historical without markers | Require explicit markers for intentional exceptions |
| Template files skipped | Assumed placeholders acceptable | Verify templates have correct placeholders, not errors |
| Verification superficial | Re-ran same patterns | Use pattern variations + manual spot-checks |
| Overconfidence bias | Previous round seemed thorough | Always assume you missed something |

---

## Response Decision Tree

```text
User Challenge Received
         ↓
    ┌────┴────┐
    │         │
  Type?    Specific
   1,3      or 2,4?
    │         │
    ↓         ↓
Protocol A  Protocol B/C
(Loop Back) (Evidence +
            Loop Back)
    │         │
    └────┬────┘
         ↓
  Round N+1 (Fresh Start)
         ↓
  New patterns + Expanded scope
         ↓
  Assume previous audit incomplete
         ↓
  Continue until 3 consecutive clean
         ↓
  Present results to user
         ↓
  If challenged again → Repeat
```

---

## Key Reminders

### DO:
✅ Acknowledge challenge immediately
✅ Loop back without defending
✅ Use completely different patterns
✅ Provide concrete evidence
✅ Assume you missed something
✅ Document blind spots
✅ Learn from each challenge

### DON'T:
❌ Defend your findings
❌ Argue about thoroughness
❌ Make excuses for missing items
❌ Minimize user concerns
❌ Re-use same patterns
❌ Trust previous round's conclusions
❌ Get discouraged by challenges

---

## See Also

- **Stage 5 Loop Decision:** `stages/stage_5_loop_decision.md` - Exit criteria and loop conditions
- **Audit Overview:** `audit_overview.md` - "User Skepticism is Healthy" section
- **Fresh Eyes Guide:** `audit_overview.md` - "How to Achieve Fresh Eyes" section
- **Confidence Calibration:** `reference/confidence_calibration.md` - Assessing audit completeness
