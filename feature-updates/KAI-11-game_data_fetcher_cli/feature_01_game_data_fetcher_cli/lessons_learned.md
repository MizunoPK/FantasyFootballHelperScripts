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

### Lesson: Validation Loop Draft Section Gaps Are Normal — Fix Immediately

**Stage:** S5.P2 Validation Loop Round 1
**What happened:** Round 1 found a missing "Data Flow & Consumption" section (D5). The Known
Gaps section in the draft mentioned it but it wasn't resolved before the Validation Loop.

**Why it happened:** Draft phase focuses on populating all sections — the Known Gap was noted
but not fixed in Phase 1 Draft Creation.

**Correct protocol:** Fix ALL known gaps before entering Validation Loop. If a gap is noted in
Phase 1 as "may need more detail," treat it as mandatory for Phase 2 — add it in Round 1 (fix
immediately), reset clean counter to 0, and continue.

**Outcome:** Fixed in Round 1 (adding 7-step Data Flow section + Data Consumers table). Rounds
2, 3, and 4 were all clean (3 consecutive = PASSED). No restart needed.

---

## S6 Lessons (Implementation)

### Lesson: Removing a Dependency Requires Removing ALL Code That Uses It (Not Just the Import)

**Stage:** S6 Phase 1 (Task 2)
**What happened:** Task 2's AC was `grep "NFL_SEASON" run_game_data_fetcher.py` returns empty.
After removing `from config import NFL_SEASON, CURRENT_NFL_WEEK`, the old historical detection
block (`if args.season and args.season < NFL_SEASON:`) still referenced `NFL_SEASON`, which
would cause a `NameError` at runtime.

**Solution:** Remove the ENTIRE old historical detection block in Phase 1 (not just the import).
The replacement logic (`if args.historical_season:`) was added in Phase 3 (Task 4). The
intermediate state was safe because Phase 1/2 checkpoints only test `import` and `--help` (not
`main()`).

**Pattern to remember:** When removing a config/module dependency (X) in Phase N:
1. Remove the import of X (obvious)
2. ALSO remove ALL code that references X (critical!)
3. The replacement code for X goes in the appropriate later phase

**Watch for this when:** A variable is imported from config and also used in conditional logic
(not just as a function argument). Both the import AND the conditional must be removed together.

---

## S7 Lessons (Testing & Review)

### Lesson: Thorough S5/S6 Execution Makes S7 Fast

**Stage:** S7 overall
**What happened:** S7.P1 smoke testing passed cleanly (no failures). S7.P2 validation loop
passed in exactly 3 rounds (0 issues found). S7.P3 PR review passed in exactly 3 rounds
(0 issues found).

**Why:** The S5 validation loop caught the only plan gap (D5 Data Flow) before implementation.
S6 followed the phased implementation plan precisely, verifying at each phase checkpoint. By
the time S7 began, the implementation was already validated at every stage.

**Pattern:** Time invested in S5 validation (4 rounds, caught 1 issue) and S6 phased execution
(4 checkpoints) produces clean S7 quality gates. The validation loop approach works.

### Lesson: E2E Test Mode Is a Fast Sanity Check (8 seconds for week 1)

**Stage:** S7.P1 Part 3
**What happened:** `--e2e-test` ran in ~8 seconds (well under the ≤180s spec limit).

**Insight:** The E2E test mode is valuable for quick sanity checks during development, not just
formal testing. It's fast enough to run multiple times (2 E2E runs during S7.P1 alone).

---

## Key Patterns for Future Features

### Pattern 1: parse_args(argv=None) at Module Level
Extract argparse into a module-level function (not inside `main()`). This enables unit tests
to call `parse_args([])` directly and verify defaults without subprocess or mocking.
Reference: `run_player_fetcher.py` and now `run_game_data_fetcher.py`.

### Pattern 2: Phased Implementation with Intermediate State Safety
When removing a feature and replacing it with another:
- Phase N: Remove OLD code (including ALL references, not just imports)
- Phase N+k: Add NEW replacement code
- Phase checkpoints N through N+k-1: Test only what's stable (e.g., `--help`, import)
- Phase checkpoint N+k: Run full suite (replacement is now in place)

### Pattern 3: Historical vs. Config Dependency Removal
When a runner script uses config values as defaults (`NFL_SEASON`, `CURRENT_NFL_WEEK`):
1. Make argparse the single source of truth (hardcode defaults in argparse)
2. Remove config import completely
3. Replace implicit comparisons (`args.season < NFL_SEASON`) with explicit flags (`--historical-season`)
This pattern produces self-documenting CLI scripts and enables easy testing.

### Pattern 4: S9 Shortcut for Single-Feature Epics
For epics with only 1 feature, S9.P1 (epic smoke testing) and S9.P2 (epic validation loop) are
largely redundant with S7.P1 and S7.P2 — the code hasn't changed, there are no other features
to integrate, and Part 4 (cross-feature integration) is N/A.

**Recommended skip for single-feature epics:** Go directly from S8 → S9.P3 (user testing).
S9.P3 (user testing) is the genuine value-add of S9 and cannot be replicated by the agent.

**When this applies:** Epic has exactly 1 feature AND no cross-feature workflows existed to test.
**When to still run full S9:** Epic has 2+ features OR there are integration points worth re-testing.
