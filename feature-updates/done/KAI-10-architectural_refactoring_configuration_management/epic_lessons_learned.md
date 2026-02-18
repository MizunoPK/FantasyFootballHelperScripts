## Epic Lessons Learned: architectural_refactoring_configuration_management

**Epic Overview:** Comprehensive architectural refactoring of all 7 runner scripts from scattered/hardcoded configuration to CLI-based configuration with dependency injection, fast E2E test modes, debug support, and an integration test framework.
**Date Range:** 2026-02-18 - {end_date}
**Total Features:** 8
**Total Bug Fixes:** {N — to be filled}

---

## Purpose

This document captures:
- **Cross-feature insights** (patterns observed across multiple features)
- **Systemic issues** (problems affecting multiple features)
- **Guide improvements** (updates needed for guides_v2/)
- **Workflow refinements** (process improvements for future epics)

**This is separate from per-feature lessons_learned.md files** (which capture feature-specific insights).

---

## S1 Lessons Learned (Epic Planning)

**What Went Well:**
- Discovery Phase Validation Loop caught several issues (wave grouping error, architecture pattern error) before they propagated to feature specs
- 3-wave structure decision (Feature 01 solo → Features 02-07 parallel → Feature 08) correctly applied "design precedent" rationale
- Merging Features 01+10 (player_fetcher argparse + DI) eliminated confusing execution ordering concern
- Dropping documentation as separate feature (integrating into workflow) aligned with guides' guidance against documentation features

**What Could Be Improved:**
- {To be filled after S1 complete and S2 begins}

**Insights for Future Epics:**
- When notes describe two features with "Feature X must execute before Feature Y" ordering, often a merge is more appropriate
- Spec dependency check ("can I write complete spec without upstream output structure?") is a critical tool — apply rigorously

**Guide Improvements Needed:**
- {To be filled}

---

## S2 Lessons Learned (Feature Deep Dives)

{Lessons captured AFTER all features complete S2}

### Cross-Feature Patterns

{To be filled}

### Feature-Specific Highlights

{To be filled}

### What Went Well

{To be filled}

### What Could Be Improved

{To be filled}

### Guide Improvements Needed

**Wave splitting for design precedent — use a solo Wave 1 feature to establish patterns before parallel Wave 2.**

When an epic contains multiple similar features that share a common implementation pattern, group them so that ONE representative feature completes S2 (and ideally S5-S8) first as a solo wave, before the similar features begin their S2 in parallel.

**Why this works:**
- The first feature forces concrete decisions (class design, constructor signatures, arg naming, E2E behavior) that would otherwise be made inconsistently across 6 parallel agents
- Later features reference the Wave 1 spec and inherit those decisions rather than re-inventing them
- Checklist questions resolved in Wave 1 often don't need to be asked again in Wave 2 (e.g., Q2 "dataclass vs BaseSettings" resolved in Feature 01 applies to all other features)
- Cross-feature conflicts in S3 are greatly reduced because Wave 2 features already aligned to Wave 1 patterns

**When to apply this pattern:**
- Epic has 3+ features following the same architectural pattern (e.g., all 7 scripts getting the same DI refactoring approach)
- The pattern requires upfront decisions with multiple valid options (e.g., dataclass vs pydantic, subprocess vs direct import)
- Features are otherwise independent (no code-level dependency on each other)

**How to identify the Wave 1 feature:**
- Pick the most complex or representative example (e.g., Feature 01 had the most internal modules to refactor — 5 modules — making it the best precedent setter)
- Alternatively, pick the one the user cares most about being "right"

**What to document in Wave 1 handoff packages:**
- Explicitly list the decisions made (e.g., "dataclass chosen over pydantic", "direct import chosen over subprocess") with the rationale
- Tell Wave 2 agents to adopt these patterns unless they have a specific reason not to — and if they do, flag it as a checklist question

**Required guide update (S10.P1):**
- Add this wave-splitting strategy to `s1_epic_planning.md` Step 5 (parallelization assessment) as a named option: "Wave 1 Precedent Pattern" — one representative feature first, then parallel execution of similar features
- Update `s2_primary_agent_group_wave_guide.md` to note that Wave 2 handoff packages should explicitly reference resolved design decisions from Wave 1 (not just spec file path)

---

**Secondary agent startup UX — handoff packages should be self-locating.**

The current parallel work guides require the Primary to write a verbose one-liner startup instruction containing the full handoff package path. The user wants secondary agents to need only a minimal instruction like:

> "You are a secondary agent for epic KAI-10 for feature 02"

The secondary agent should be able to derive everything from that alone:
1. Look up KAI-10 in `feature-updates/` to find the epic folder
2. Find the `feature_02_*/HANDOFF_PACKAGE.md` by matching the feature number
3. Read the handoff package to get full context and instructions
4. Proceed with S2.P1 as directed

**Required guide update (S10.P1):**
- Update `parallel_work/s2_primary_agent_guide.md` and `s2_primary_agent_group_wave_guide.md`: the "Present Handoffs to User" step should instruct Primary to give user a SHORT instruction per secondary ("You are a secondary agent for KAI-{N} for feature {X}"), not a full handoff package paste
- Update `parallel_work/s2_secondary_agent_guide.md`: add "Getting Started" step 0 — if given only minimal startup instruction (epic + feature number), first action is to locate and read `feature_XX_*/HANDOFF_PACKAGE.md` before doing anything else
- The HANDOFF_PACKAGE.md files (stored in each feature folder) remain the full context document — they just don't need to be pasted verbatim at startup

---

**Checklist question presentation — always provide a recommended answer.**

When agents present checklist questions to the user during S2.P1.I2 (Checklist Resolution), they frequently omit a recommendation and instead present all options neutrally. This forces the user to make a decision without the agent's analysis of the tradeoffs.

**The correct pattern:**
- Agent researches the options and evaluates tradeoffs
- Agent presents all options with pros/cons
- Agent explicitly states which option they recommend and why
- Agent asks the user to make the final decision (never autonomous resolution)

**Example of wrong behavior:**
> Q1: Should we use direct import or subprocess?
> - Option A: Direct import
> - Option B: Subprocess
> Which do you prefer?

**Example of correct behavior:**
> Q1: Should we use direct import or subprocess?
> - **Option A (Recommended):** Direct import — matches DISCOVERY.md pattern, simpler code, no working directory issues
> - Option B: Subprocess — keeps runner isolated but adds complexity and subprocess overhead
> I recommend Option A. What is your decision?

**Why this matters:**
- The agent has already done the research; withholding a recommendation wastes the user's time
- A recommendation doesn't remove user agency — the user still makes the call
- Agents that present options without a recommendation are not fully completing their analysis work

**Required guide update (S10.P1):**
- Update `s2_p1_spec_creation_refinement.md` S2.P1.I2 step: explicitly require agents to state a recommendation with rationale for EACH checklist question before asking for user decision
- Update checklist.md template to include a "Recommendation:" field under each question

---

**Parallel work guide coordination paths are outdated — do not match CLAUDE.md rules.**

The parallel work guides (`s2_primary_agent_group_wave_guide.md`, `s2_primary_agent_guide.md`) reference a coordination directory structure under `parallel_work/coordination/` with this layout:

```
parallel_work/coordination/
├── agent_checkpoints/   (checkpoint .md files)
└── inboxes/
    ├── from_primary/
    ├── from_secondary_a/
    └── from_secondary_b/
```

**CLAUDE.md mandates a different structure** (and overrides guide content):
```
{epic_folder}/
├── .epic_locks/          (lock files)
├── agent_comms/          (flat .md files, NO subdirectories)
└── agent_checkpoints/    (flat .json files, NO .md extension)
```

Key conflicts between guide and CLAUDE.md:
1. Guide uses `parallel_work/coordination/` as base — CLAUDE.md uses epic folder directly
2. Guide uses per-agent inbox subdirectories (`inboxes/from_secondary_a/`) — CLAUDE.md prohibits subdirectories under `agent_comms/`
3. Guide checkpoint files use `.md` extension — CLAUDE.md mandates `.json` extension

**In practice during this epic:**
- Agents used `agent_comms/secondary_a_to_primary.md` (flat file, correct per CLAUDE.md)
- No checkpoint `.json` files were created by agents (structure existed but wasn't used heavily)
- The validate_structure.sh script validated the CLAUDE.md-compliant structure

**Required guide update (S10.P1):**
- Update `s2_primary_agent_guide.md` and `s2_primary_agent_group_wave_guide.md`: replace all `parallel_work/coordination/` path references with correct paths (`.epic_locks/`, `agent_comms/`, `agent_checkpoints/` directly under epic folder)
- Update checkpoint format examples to use `.json` extension
- Update inbox examples to show flat files in `agent_comms/` (not nested subdirectory structure)
- Update the monitoring `ls`/`cat` commands in the guide to use correct paths

---

**Primary agent should NOT relay secondary checklist questions to the user — secondaries handle their own Q&A.**

During Wave 2 monitoring, the Primary agent collected open questions from secondary agents' checklist.md files and began presenting them to the user. This is incorrect behavior.

**The correct pattern:**
- Secondary agents present their own checklist questions directly to the user during S2.P1.I2
- Primary agent's job during Wave 2 is to monitor progress (checkpoint freshness), handle escalations, and wait
- Primary should only relay to the user if a secondary explicitly escalates via `agent_comms/` requesting Primary to forward a question
- Reading secondary checklists to gather questions and presenting them unprompted bypasses the secondary's own workflow

**Required guide update (S10.P1):**
- Update `s2_primary_agent_group_wave_guide.md` Phase 3 monitoring section: explicitly state that Primary reads checkpoints for freshness/blockers only, does NOT read checklist.md files to relay questions, and only intervenes when secondary sends an escalation message to `agent_comms/`

---

## S3 Lessons Learned (Cross-Feature Sanity Check)

**What Went Well:**
{To be filled}

**What Could Be Improved:**
{To be filled}

**Conflicts Discovered:**
{To be filled}

**Insights for Future Epics:**
{To be filled}

**Guide Improvements Needed:**
{To be filled}

---

## S4 Lessons Learned (Epic Testing Strategy)

**What Went Well:**
{To be filled}

**What Could Be Improved:**
{To be filled}

**epic_smoke_test_plan.md Evolution:**
{To be filled}

**Guide Improvements Needed:**
{To be filled}

---

## S5 Lessons Learned (Feature Implementation)

{Capture lessons AFTER EACH feature completes S8.P2}

### Feature 01 (refactor_player_data_fetcher) — Stages S5 through S8

{To be filled after Feature 01 completes}

---

### Feature 02 (schedule_fetcher_cli) — Stages S5 through S8

{To be filled after Feature 02 completes}

---

### Feature 03 (game_data_fetcher_cli) — Stages S5 through S8

{To be filled after Feature 03 completes}

---

### Feature 04 (historical_compiler_cli) — Stages S5 through S8

{To be filled after Feature 04 completes}

---

### Feature 05 (win_rate_simulation_e2e) — Stages S5 through S8

{To be filled after Feature 05 completes}

---

### Feature 06 (accuracy_simulation_e2e) — Stages S5 through S8

{To be filled after Feature 06 completes}

---

### Feature 07 (league_helper_cli) — Stages S5 through S8

{To be filled after Feature 07 completes}

---

### Feature 08 (integration_test_framework) — Stages S5 through S8

{To be filled after Feature 08 completes}

---

### Cross-Feature Implementation Patterns

{To be filled after multiple features complete}

---

### Debugging Insights Across Features

**Total Debugging Sessions:** {N} features required debugging

**Common Bug Patterns:**
{To be filled}

**Common Process Gaps:**
{To be filled}

**Most Impactful Guide Updates:**
{To be filled}

**Testing Insights:**
{To be filled}

---

### Guide Improvements Needed from S5

{To be filled after features complete}

---

## S9 Lessons Learned (Epic Final QC)

**What Went Well:**
{To be filled}

**What Could Be Improved:**
{To be filled}

**Epic-Level Issues Found:**
{To be filled}

**epic_smoke_test_plan.md Effectiveness:**
{To be filled}

**Guide Improvements Needed:**
{To be filled}

---

## S10 Lessons Learned (Epic Cleanup)

**What Went Well:**
{To be filled}

**What Could Be Improved:**
{To be filled}

**Documentation Quality:**
{To be filled}

**Guide Improvements Needed:**
{To be filled}

---

## Cross-Epic Insights

{High-level insights applicable beyond this epic}

**Systemic Patterns:**
{To be filled}

**Workflow Refinements:**
{To be filled}

**Tool/Process Improvements:**
{To be filled}

---

## Recommendations for Future Epics

{To be filled after S10}

---

## Guide Updates Applied

{Track which guides were updated based on lessons from THIS epic}

**Guides Updated:**
{To be filled in S10.P1}

**CLAUDE.md Updates:**
{To be filled in S10.P1}

**Date Applied:** {YYYY-MM-DD}

---

## Metrics

**Epic Duration:** {N} days
**Features:** 8
**Bug Fixes:** {N}
**Tests Added:** {N}
**Files Modified:** {N}
**Lines of Code Changed:** ~{N}

**Stage Durations:**
- S1: {N} days
- S2: {N} days (all features)
- S3: {N} days
- S4: {N} days
- S5: {N} days (all features)
- S9: {N} days
- S10: {N} days

**QC Restart Count:**
- S7 restarts: {N} (across all features)
- S9 restarts: {N}

**Test Pass Rates:**
- Final pass rate: {percentage}% ({X}/{Y} tests)
- Tests added by this epic: {N}
