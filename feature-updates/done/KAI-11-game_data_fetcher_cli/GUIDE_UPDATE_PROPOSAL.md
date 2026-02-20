# Guide Update Proposal - KAI-11-game_data_fetcher_cli

**Epic:** KAI-11-game_data_fetcher_cli
**Date:** 2026-02-20
**Agent:** claude-sonnet-4-6
**Total Proposals:** 4 (0 critical, 2 high, 2 medium, 0 low)

---

## Summary

**Lessons Learned Count:**
- Epic-level: 2 lessons (E2E fixed paths pattern, S9 shortcut guide improvement)
- Feature-level: 5 lessons across 1 feature (S2 autonomous resolution, S5 known gaps, S6 dependency removal, S7 positive outcomes ×2)
- Total: 7 lessons analyzed — 4 actionable, 3 non-actionable (positive outcomes / domain-specific)

**Guide Gaps Identified:**
- 0 critical gaps (P0)
- 2 high-priority improvements (P1)
- 2 medium-priority improvements (P2)
- 0 low-priority improvements (P3)

**Non-Actionable Lessons (filtered out):**
- S7 positive outcome: "Thorough S5/S6 makes S7 fast" — process confirmation, no guide gap
- S7 insight: "E2E test mode is fast sanity check" — domain-specific tip, not a guide gap
- E2E fixed paths pattern — domain-specific to runner scripts, already captured in epic_lessons_learned.md

**Recommended Action:** Review P1 proposals first (highest value); P2 proposals are worth applying but less urgent

---

## P0: Critical Fixes (Must Review)

*No P0 proposals for this epic.*

---

## P1: High Priority (Strongly Recommended)

### Proposal P1-1: S9 Single-Feature Epic Shortcut

**Lesson Learned:**
> "For single-feature epics, S9.P1 (epic smoke testing) and S9.P2 (epic validation loop) are largely redundant with S7.P1 and S7.P2: The code hasn't changed between S7 and S9, there are no other features to integrate (Part 4 cross-feature is N/A), and S9.P1 would re-run the same 3-part smoke test as S7.P1. S9.P3 remains mandatory — user testing is the genuine value-add of S9 and cannot be replicated by the agent regardless of feature count."

**Source File:** `epic_lessons_learned.md` — "Guide Improvements Identified: S9 Shortcut"

**Root Cause:**
The S9 router guide routes ALL epics to S9.P1 → S9.P2 → S9.P3 → S9.P4 unconditionally. For single-feature epics with no cross-feature integration, S9.P1 and S9.P2 duplicate S7.P1 and S7.P2 exactly (same code, same scenarios, no new integration points). An agent following the guide would spend 3-6 hours re-running validation that was already completed in S7.

**Affected Guide(s):**
- `stages/s9/s9_epic_final_qc.md` — Section: "Quick Navigation" and "Sub-Stage Breakdown"

**Current State (BEFORE):**
```markdown
## Quick Navigation

**Use this table to find the right guide:**

| Current Phase | Guide to Read | Time Estimate |
|---------------|---------------|---------------|
| Starting S9 | `stages/s9/s9_p1_epic_smoke_testing.md` | 60-90 min |
| S9.P1: Epic Smoke Testing | `stages/s9/s9_p1_epic_smoke_testing.md` | 45-75 min |
| S9.P2: Validation Loop | `stages/s9/s9_p2_epic_qc_rounds.md` | 2-4 hours |
| S9.P3: User Testing | `stages/s9/s9_p3_user_testing.md` | Variable |
| S9.P4: Epic Final Review | `stages/s9/s9_p4_epic_final_review.md` | 1.5-2 hours |
```

**Proposed Change (AFTER):**
```markdown
## Quick Navigation

**Use this table to find the right guide:**

| Current Phase | Guide to Read | Time Estimate |
|---------------|---------------|---------------|
| Starting S9 | `stages/s9/s9_p1_epic_smoke_testing.md` | 60-90 min |
| S9.P1: Epic Smoke Testing | `stages/s9/s9_p1_epic_smoke_testing.md` | 45-75 min |
| S9.P2: Validation Loop | `stages/s9/s9_p2_epic_qc_rounds.md` | 2-4 hours |
| S9.P3: User Testing | `stages/s9/s9_p3_user_testing.md` | Variable |
| S9.P4: Epic Final Review | `stages/s9/s9_p4_epic_final_review.md` | 1.5-2 hours |

### Single-Feature Epic Shortcut

**If the epic has exactly 1 feature AND no cross-feature integration exists:**

> Skip S9.P1 and S9.P2. Proceed directly to S9.P3 (User Testing).

**Why:** S9.P1 and S9.P2 are redundant for single-feature epics:
- Code has not changed since S7 (no new integration)
- S9.P1 would re-run the same smoke test as S7.P1
- S9.P2 would re-run the same QC loop as S7.P2
- Part 4 (cross-feature integration) is N/A by definition

**S9.P3 remains mandatory** — user testing is the genuine value-add of S9 and cannot be
replicated by the agent, regardless of feature count.

**Apply this shortcut ONLY when:**
- ✅ Epic has exactly 1 feature
- ✅ No cross-feature workflows to verify

**Do NOT skip S9.P1 and S9.P2 when:**
- ❌ Epic has 2+ features
- ❌ Cross-feature integration points exist (even for 1-feature epics that touch shared modules)
```

**Rationale:**
Adding the shortcut prevents agents from spending 3-6 hours re-running validation already completed in S7. The condition is specific and safe — only applies when there's truly nothing new to validate at the epic level.

**Impact Assessment:**
- **Who benefits:** Agents working on single-feature epics (common for targeted refactoring epics like KAI-11)
- **When it helps:** Every single-feature epic; saves 3-6 hours per epic
- **Severity if unfixed:** High — agents waste 3-6 hours re-running redundant validation on every single-feature epic

**User Decision:** [ ] Approve  [ ] Modify  [ ] Reject  [ ] Discuss

**User Feedback/Modifications:**
```json
{User writes response here}
```

---

### Proposal P1-2: "Port the Spec" Mental Mode Trigger Warning

**Lesson Learned:**
> "'Port the spec' mental mode pulls toward minimizing new questions. When S2 is framed as 'port an already-approved spec,' there is a strong pull to treat any decision you can rationalize as 'already covered.' This mode is appropriate for porting existing requirements but must not extend to resolving new design decisions autonomously."

**Source File:** `feature_01_game_data_fetcher_cli/lessons_learned.md` — "S2 Lessons: Autonomous Checklist Resolution in Port the Spec Mode"

**Root Cause:**
The S2 spec creation guide already has strong autonomous-resolution prevention rules (PENDING USER APPROVAL protocol). However, there's a specific trigger condition — "porting an existing approved spec" — that creates a particular cognitive frame making violations more likely. When the task is framed as "verifying" existing decisions rather than "making new decisions," agents misclassify genuinely new decisions as verifications. The existing anti-pattern documentation doesn't call out this trigger explicitly.

**Affected Guide(s):**
- `stages/s2/s2_p1_spec_creation_refinement.md` — Section: autonomous resolution prevention protocol (around lines 126-155)

**Current State (BEFORE):**
```markdown
- **CRITICAL:** Do NOT mark [x] autonomously
...
**This protocol prevents autonomous question resolution:**
...
4. Agent presents findings → Status: PENDING USER APPROVAL
```
*(No mention of the "Port the Spec" trigger or the verification-vs-new-decision failure mode)*

**Proposed Change (AFTER):**
Add after the existing autonomous resolution protocol:
```markdown
**⚠️ "Port the Spec" Mode Warning:**
When S2 is framed as "porting an existing approved spec" (e.g., carrying forward a KAI-N spec to a successor epic), be extra vigilant about autonomous resolution. This framing creates a pull toward treating any new decision as "already covered." Watch for:
- Checklist items labeled "Verification Items" that expose genuinely NEW decisions during research
- Decisions where you have "strong evidence" from existing patterns — strong evidence → better PENDING presentation, NOT autonomous resolution
- Any design decision not explicitly decided in the source spec (even if you can rationalize it from the source)

**The rule remains unchanged:** Any new decision requires PENDING → User approval → RESOLVED. The "verification" framing does not change this protocol.
```

**Rationale:**
The existing anti-pattern is well-documented, but the specific "Port the Spec" trigger is not called out. Adding this warning directly prevents the failure mode from recurring in successor epics that explicitly "port" a previous spec.

**Impact Assessment:**
- **Who benefits:** Agents working on successor epics that port existing approved specs (common in refactoring chains like KAI-10 → KAI-11)
- **When it helps:** Any S2 framed as "port the previous spec" or "verify existing decisions"
- **Severity if unfixed:** High — autonomous resolution of new decisions can introduce unreviewed design choices into the spec; was caught and corrected but added friction

**User Decision:** [ ] Approve  [ ] Modify  [ ] Reject  [ ] Discuss

**User Feedback/Modifications:**
```json
{User writes response here}
```

---

## P2: Medium Priority (Consider)

### Proposal P2-1: Fix ALL Known Gaps BEFORE Entering Validation Loop

**Lesson Learned:**
> "Round 1 found a missing 'Data Flow & Consumption' section (D5). The Known Gaps section in the draft mentioned it but it wasn't resolved before the Validation Loop. Correct protocol: Fix ALL known gaps before entering Validation Loop. If a gap is noted in Phase 1 as 'may need more detail,' treat it as mandatory for Phase 2 — add it in Round 1 (fix immediately), reset clean counter to 0, and continue."

**Source File:** `feature_01_game_data_fetcher_cli/lessons_learned.md` — "S5 Lessons: Validation Loop Draft Section Gaps Are Normal — Fix Immediately"

**Root Cause:**
The S5 guide describes Phase 1 (Draft Creation) quality target as "~70% complete with known gaps OK." This is intentional — Phase 1 drafts are not expected to be perfect. However, the guide doesn't explicitly say that Known Gaps documented in Phase 1 MUST be resolved before entering Phase 2 (Validation Loop). An agent can reasonably interpret "known gaps OK" as meaning gaps can persist into the loop.

**Affected Guide(s):**
- `stages/s5/s5_v2_validation_loop.md` — Section: Phase 1 → Phase 2 transition (around line 191-405)

**Current State (BEFORE):**
```markdown
**Quality Target:** ~70% complete (structure exists, major content present, known gaps OK)
...
**Quality Expectation:** ~70% complete with known gaps
```
*(No explicit instruction that Known Gaps must be resolved before starting Phase 2)*

**Proposed Change (AFTER):**
Add at the Phase 1 → Phase 2 transition:
```markdown
**🚨 Before entering Phase 2 (Validation Loop):**
Review your Phase 1 Known Gaps section. ANY gap documented as "may need more detail" or
"to be added" MUST be resolved NOW — before Round 1 begins.

Why: If a Known Gap reaches Round 1, it becomes a Round 1 issue. Round 1 will not be clean.
This is fine (fix-and-continue protocol handles it), but it's more efficient to fix gaps
at the Phase 1/Phase 2 boundary than inside the loop.

The "known gaps OK" target means gaps are expected during Phase 1 drafting — not that
gaps are acceptable when you START the loop.
```

**Rationale:**
This clarifies the Phase 1/Phase 2 boundary behavior. The fix-and-continue protocol handles the case where gaps reach Round 1, but adding this note prevents an easily-avoidable extra round.

**Impact Assessment:**
- **Who benefits:** All agents doing S5 v2 Implementation Planning
- **When it helps:** The Phase 1 → Phase 2 transition; saves 1 round per plan
- **Severity if unfixed:** Medium — adds 1 extra round to the validation loop when known gaps aren't fixed first; minor inefficiency but no quality impact (the loop catches it anyway)

**User Decision:** [ ] Approve  [ ] Modify  [ ] Reject  [ ] Discuss

**User Feedback/Modifications:**
```json
{User writes response here}
```

---

### Proposal P2-2: Dependency Removal Must Remove ALL Code References (Not Just Import)

**Lesson Learned:**
> "Task 2's AC was `grep 'NFL_SEASON' run_game_data_fetcher.py` returns empty. After removing `from config import NFL_SEASON, CURRENT_NFL_WEEK`, the old historical detection block (`if args.season and args.season < NFL_SEASON:`) still referenced `NFL_SEASON`, which would cause a `NameError` at runtime. Pattern to remember: When removing a config/module dependency (X) in Phase N: 1. Remove the import of X (obvious), 2. ALSO remove ALL code that references X (critical!), 3. The replacement code for X goes in the appropriate later phase."

**Source File:** `feature_01_game_data_fetcher_cli/lessons_learned.md` — "S6 Lessons: Removing a Dependency Requires Removing ALL Code That Uses It"

**Root Cause:**
The S6 guide doesn't have a specific checklist item for dependency removal tasks that alerts agents to also remove all downstream code that references the removed dependency. The `NameError` would only appear at runtime (not at import time), making it easy to miss during phase checkpoints that only test `--help`.

**Affected Guide(s):**
- `stages/s6/s6_execution.md` — Section: dependency removal tasks or implementation checkpoints

**Current State (BEFORE):**
*(No specific guidance for dependency removal tasks beyond implementing the task as specified)*

**Proposed Change (AFTER):**
Add a note to the S6 execution guide's task implementation section:
```markdown
**Dependency Removal Tasks:** When a task removes an import or dependency (X):
1. Remove the import statement (obvious)
2. ALSO remove ALL code that references X — conditionals, comparisons, function calls (critical!)
3. Replacement code for X goes in the appropriate later phase/task
4. Phase checkpoint: grep for the removed name to verify ALL references gone

If only the import is removed but referencing code remains, the code will fail at runtime
with a NameError — not at import time, so `--help` checkpoints won't catch it.
```

**Rationale:**
Adds a runtime-vs-import-time distinction and the grep verification step. Prevents a subtle class of bugs where partial removal leaves dangling references that only fail at runtime.

**Impact Assessment:**
- **Who benefits:** All agents implementing phased dependency removal (e.g., removing config imports, replacing module dependencies)
- **When it helps:** Any S6 task that removes an import and replaces it with inline values or different logic
- **Severity if unfixed:** Medium — causes runtime NameError that only appears when actually running the code, not during import or --help checkpoints; could fail silently in edge-case code paths

**User Decision:** [ ] Approve  [ ] Modify  [ ] Reject  [ ] Discuss

**User Feedback/Modifications:**
```json
{User writes response here}
```

---

## P3: Low Priority (Nice-to-Have)

*No P3 proposals for this epic.*

---

## User Approval Summary

**Instructions:**
1. Review each proposal individually (start with P1, then P2)
2. Mark your decision: Approve / Modify / Reject / Discuss
3. For "Modify", provide alternative text in the Feedback section
4. For "Discuss", ask questions; agent will re-present for final decision

**Guidelines:**
- **P1 (High):** Recommended — significantly reduces rework or confusion for future epics
- **P2 (Medium):** Consider — moderate improvements, clarifies edge cases in guides

**Approval Statistics:**
- Total proposals: 4
- P1 proposals: 2 (high)
- P2 proposals: 2 (medium)

**After User Review:**
- Approved: 4 (P1-1, P1-2, P2-1, P2-2)
- Modified: 0
- Rejected: 0

---

**Last Updated:** 2026-02-20
