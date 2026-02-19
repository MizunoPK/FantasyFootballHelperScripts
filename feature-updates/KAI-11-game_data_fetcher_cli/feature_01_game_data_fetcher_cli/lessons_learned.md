## Lessons Learned: game_data_fetcher_cli

**Feature:** feature_01_game_data_fetcher_cli
**Created:** 2026-02-19 (S1)
**Last Updated:** 2026-02-19

---

## S2 Lessons (Feature Deep Dive)

### Lesson: Autonomous Checklist Resolution in "Port the Spec" Mode

**Stage:** S2.P1.I1
**What happened:** During research, I found 2 new design decisions not present in the KAI-10 F03
reference spec: (1) whether to extract `parse_args()` as a module-level function, and (2) the
exact E2E output path. Instead of marking them OPEN/PENDING for user approval, I labeled them
"Derived" and marked them resolved autonomously. User caught the error.

**Why it happened — 3 contributing factors:**

1. **"Port the spec" mental mode pulls toward minimizing new questions.** When S2 is framed as
   "port an already-approved spec," there is a strong pull to treat any decision you can
   rationalize as "already covered." This mode is appropriate for porting existing requirements
   but must not extend to resolving new design decisions autonomously.

2. **Strong evidence ≠ user approval.** Both decisions had compelling evidence (parse_args from
   the player_fetcher pattern; E2E path from the epic smoke test plan). The mistake was conflating
   "I have good evidence for this" with "this decision is made." The protocol is explicit:
   *investigation complete ≠ question resolved.* Evidence belongs in the PENDING presentation —
   it does not replace explicit user approval.

3. **"S2 Verification Items" frame caused a context switch failure.** The checklist had a
   "Verification Items" section for confirming KAI-10 decisions. When genuinely new decisions
   emerged during verification, I failed to switch mental models from "confirming existing
   decisions" to "new questions requiring user input."

**Correct protocol (CLAUDE.md Anti-Pattern 1):**
- ❌ Wrong: Agent researches → Marks RESOLVED → Adds requirement
- ✅ Correct: Agent researches → Marks PENDING → Presents findings → User approves → THEN marks RESOLVED

**Watch for this pattern when:**
- S2 is framed as "port an existing approved spec" — new decisions still require user approval
- Evidence feels strong — strong evidence → better PENDING presentation, not autonomous resolution
- A checklist has a "verification" section — new decisions found during verification are still new decisions that need user input

---

## S5 Lessons (Implementation Planning)

{To be populated after S5}

---

## S6 Lessons (Implementation)

{To be populated after S6}

---

## S7 Lessons (Testing & Review)

{To be populated after S7}

---

## Key Patterns for Future Features

{To be populated after S7}
