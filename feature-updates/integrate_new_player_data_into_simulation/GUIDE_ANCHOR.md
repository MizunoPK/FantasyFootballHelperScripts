# Guide Anchor: integrate_new_player_data_into_simulation

**Purpose:** Quick resumption guide for agents after session compaction

**Last Updated:** 2026-01-02

---

## How to Resume This Epic

If you're a new agent session resuming this epic after context window compaction:

### Step 1: Read EPIC_README.md First
```bash
Read feature-updates/integrate_new_player_data_into_simulation/EPIC_README.md
```

Look for the **Agent Status** section at the top - it tells you:
- Current stage and guide name
- Current step/iteration
- Next action to take
- Critical rules from current guide

### Step 2: Read the Current Guide
The Agent Status section specifies which guide you should be following.
**Always use the Read tool to load the ENTIRE guide** - don't work from memory.

### Step 3: Use the Phase Transition Prompt
Before proceeding, use the appropriate prompt from:
```bash
Read feature-updates/guides_v2/prompts_reference_v2.md
```

Find the prompt for "Resuming In-Progress Epic" and acknowledge critical requirements.

### Step 4: Continue from Next Action
The Agent Status "Next Action" field tells you exactly what to do next.

---

## Epic Workflow Diagram

```
Stage 1 → Stage 2 → Stage 3 → Stage 4 → Stage 5 → Stage 6 → Stage 7
  ↓         ↓         ↓         ↓         ↓         ↓         ↓
Epic    Features  Sanity   Testing   Impl     Epic      Done
Plan    Deep Dive  Check   Strategy  (5a-5e)  QC
```

**Stage 5 Sub-Stages (per feature):**
```
5a → 5b → 5c → 5d → 5e
↓     ↓     ↓     ↓     ↓
TODO  Impl  Post  Align Test
           -Impl        Plan
```

---

## Current Epic State

**Epic:** integrate_new_player_data_into_simulation
**Total Features:** 3
**Current Stage:** Stage 1 (Epic Planning)

**Features:**
1. feature_01_win_rate_sim_verification - Win Rate Sim JSON verification/cleanup
2. feature_02_accuracy_sim_verification - Accuracy Sim JSON verification/cleanup
3. feature_03_cross_simulation_testing - Integration testing and documentation

**Key Files:**
- `EPIC_README.md` - Central tracking (check Agent Status section)
- `EPIC_TICKET.md` - User-validated outcomes (immutable)
- `epic_smoke_test_plan.md` - Test scenarios (will update in Stages 4, 5e, 6)
- `epic_lessons_learned.md` - Cross-feature insights

---

## Critical Rules for This Epic

**From Epic Request:**
- Assume all previous work is incorrect or incomplete - verify everything
- Both Win Rate Sim AND Accuracy Sim must be updated
- Week 17 special handling: projected from week_17, actual from week_18
- Remove ALL CSV references and deprecated code
- 100% test pass rate required

**From Workflow:**
- ALWAYS read guide before starting stage (use Read tool for ENTIRE guide)
- Use phase transition prompts (MANDATORY)
- Update Agent Status after major steps
- Zero tech debt tolerance - fix ALL issues immediately

---

## Emergency: How to Find Your Place

**If you're completely lost:**

1. **Read EPIC_README.md** - Agent Status section is source of truth
2. **Check Guide Deviation Log** in EPIC_README.md - see if previous agent deviated
3. **Read prompts_reference_v2.md** - Find "Resuming In-Progress Epic" prompt
4. **Read current guide** specified in Agent Status
5. **Ask user** if still unclear after reading guides

**DO NOT:**
- ❌ Guess what stage you're in
- ❌ Skip reading the current guide
- ❌ Continue work without understanding context
- ❌ Start over from Stage 1 (epic structure already exists)

---

**Remember:** EPIC_README.md Agent Status survives context limits. Always read it first.
