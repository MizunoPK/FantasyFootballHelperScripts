# Bugfix Notes Template

**Filename:** `notes.txt`
**Location:** `.shamt/epics/SHAMT-{N}-{epic_name}/bugfix_{priority}_{name}/notes.txt`
**Created:** When bug discovered (during any stage)

**Purpose:** User-verified description of a bug and proposed fix, created when bugs are discovered during any stage.

---

## Template

```text
BUG FIX: {name}
Priority: {high/medium/low}
Discovered: {date}
Discovered During: {Stage X - feature_name}

----

ISSUE DESCRIPTION:

{Clear description of the bug/issue}

What's wrong:
- {Symptom 1}
- {Symptom 2}
- {Symptom 3}

How discovered:
- {How the issue was found - e.g., "Validation Loop revealed...", "User reported..."}

Impact:
- {What doesn't work because of this bug}
- {Who is affected}
- {How severe}

----

ROOT CAUSE (if known):

{Analysis of why the bug exists}

Example:
- Missing null check in ConfigManager.get_rank_multiplier()
- When item has no rank data, method crashes instead of returning default

----

PROPOSED SOLUTION:

{How to fix it}

Example:
- Add null check at top of method
- Return (1.0, 50) for null/missing rank (neutral multiplier)
- Add unit test for null rank case

----

VERIFICATION PLAN:

How to verify fix works:
1. {Test scenario 1}
2. {Test scenario 2}
3. {Expected result}

----

USER NOTES:

{User can add notes, clarifications, or corrections here}
```

---

## Usage

1. Create `bugfix_{priority}_{name}/` folder in epic directory
2. Copy template content above into `notes.txt`
3. Fill in all `{placeholders}` with actual values
4. Present to user for review and approval (Step 5 in `stages/s5/s5_bugfix_workflow.md`)
5. **Immutable after user verification** — do not modify without re-presenting to user

**Priority values:** `high` (blocking progress), `medium` (important but not blocking), `low` (nice to fix)

**See:** `stages/s5/s5_bugfix_workflow.md` for complete bug fix workflow
