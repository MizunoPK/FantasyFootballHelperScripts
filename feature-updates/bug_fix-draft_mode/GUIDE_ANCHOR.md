# GUIDE ANCHOR: bug_fix-draft_mode

**Purpose:** Ensure agents can resume correctly after session compaction

**Last Updated:** 2025-12-31 15:40

---

## 🔄 Resuming After Session Compaction

**If you're a new agent resuming this epic after session compaction:**

1. **READ EPIC_README.md FIRST** - Check the "Agent Status" section at the top
2. **Identify current stage** - Agent Status tells you exactly where we are
3. **READ THE CURRENT GUIDE** - Use Read tool to load the ENTIRE guide (not summary)
4. **Use the resumption prompt** - Found in `guides_v2/prompts_reference_v2.md`
5. **Continue from "Next Action"** - Agent Status tells you exact next step

**DO NOT:**
- ❌ Restart the workflow from Stage 1
- ❌ Skip reading the current guide (must read FULL guide)
- ❌ Assume you know what to do next without checking Agent Status
- ❌ Proceed without using the resumption prompt

---

## Current Epic Status

**Epic Name:** bug_fix-draft_mode
**Epic Type:** fix (bug fix)
**Git Branch:** fix/KAI-1
**KAI Number:** 1

**Current Stage:** Stage 1 - Epic Planning (Phase 4 - Epic Structure Creation)
**Current Guide:** `guides_v2/STAGE_1_epic_planning_guide.md`
**Guide Last Read:** 2025-12-31 15:30

**Next Action:** Complete Phase 4, then transition to Stage 2 (Feature Deep Dive)

---

## Epic Workflow Reference

```
Stage 1 → Stage 2 → Stage 3 → Stage 4 → Stage 5 → Stage 6 → Stage 7
  ↓         ↓         ↓         ↓         ↓         ↓         ↓
Epic    Features  Sanity   Testing   Impl     Epic      Done
Plan    Deep Dive  Check   Strategy  (5a-5e)  QC

YOU ARE HERE: ➜ Stage 1 (Phase 4)
```

**Stage 1 Phases:**
1. Initial Setup (git branch, epic folder) ✅
2. Epic Analysis (understand bug) ✅
3. Feature Breakdown Proposal (user approval) ✅
4. Epic Structure Creation (files, folders) 🔄 IN PROGRESS
5. Transition to Stage 2 ⏳ PENDING

---

## Epic Features

**Total Features:** 1

1. **feature_01_fix_player_round_assignment**
   - Fix FLEX position matching logic in _match_players_to_rounds()
   - Status: Stage 1 (planning)
   - Folder: `feature_01_fix_player_round_assignment/`

---

## Critical Files Location

**Epic-Level Files:**
- `EPIC_README.md` - Master tracking (ALWAYS CHECK THIS FIRST)
- `epic_smoke_test_plan.md` - Testing strategy (placeholder in Stage 1)
- `epic_lessons_learned.md` - Cross-feature insights
- `GUIDE_ANCHOR.md` - This file (resumption instructions)
- `research/` - Shared research folder

**Feature Folders:**
- `feature_01_fix_player_round_assignment/` - Feature 1 files

**Guides Location:**
- `../guides_v2/` - All workflow guides
- `../guides_v2/prompts_reference_v2.md` - MANDATORY resumption prompts

---

## Key Context for Resumption

**Bug Description:**
Add to Roster mode's `_match_players_to_rounds()` method incorrectly converts RB/WR to "FLEX" before matching, preventing them from matching RB-ideal or WR-ideal rounds. This causes incorrect [EMPTY SLOT] displays even when roster is full.

**Root Cause:**
Line 426 in AddToRosterModeManager.py uses `get_position_with_flex()` which converts RB→"FLEX" and WR→"FLEX", preventing native position matches.

**Expected Fix:**
Allow RB/WR to match BOTH their native position AND FLEX rounds, while QB/TE/K/DST match only exact positions.

**User Approval:** ✅ Received for 1-feature breakdown

---

## Mandatory Reading After Compaction

**If resuming after session compaction, you MUST:**

1. Read `EPIC_README.md` Agent Status section
2. Read the guide specified in Agent Status (FULL guide, not summary)
3. Use the resumption prompt from `guides_v2/prompts_reference_v2.md`
4. Update Agent Status with new "Guide Last Read" timestamp
5. Continue from the "Next Action" in Agent Status

**Resumption Prompt Location:**
`../guides_v2/prompts_reference_v2.md` → "Resuming In-Progress Epic" section

---

## Emergency Recovery

**If you're confused or don't know where to start:**

1. **READ THIS ENTIRE FILE** (you're doing that now ✅)
2. **READ EPIC_README.md** - Look for "Agent Status" at the top
3. **READ THE CURRENT GUIDE** - Agent Status tells you which guide
4. **ASK USER IF STILL UNCLEAR** - Better to ask than to restart incorrectly

**DO NOT restart from Stage 1 unless epic folder is completely empty.**

---

**Last Updated:** 2025-12-31 15:40
**Updated By:** Agent during Stage 1 Phase 4 (Epic Structure Creation)
