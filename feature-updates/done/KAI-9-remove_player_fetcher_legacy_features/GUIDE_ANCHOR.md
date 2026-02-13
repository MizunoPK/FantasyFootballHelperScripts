## Guide Anchor: KAI-9 - remove_player_fetcher_legacy_features

**Created:** 2026-02-13
**Last Updated:** 2026-02-13

---

## Purpose

This file provides quick navigation to the current workflow stage after session compaction or interruption.

**🚨 CRITICAL: Read EPIC_README.md Agent Status FIRST** - This file is a backup reference only.

---

## Current Workflow Stage

**Stage:** S1 - Epic Planning
**Status:** IN PROGRESS (completing Step 5 - Epic Structure Creation)
**Next Stage:** S2 - Feature Deep Dive

**Progress:**
- [x] S1 Step 1: Git branch created (epic/KAI-9)
- [x] S1 Step 2: Epic Analysis complete
- [x] S1 Step 3: Discovery Phase complete (user approved)
- [x] S1 Step 4: Epic Ticket created and validated (user approved)
- [ ] S1 Step 5: Epic Structure Creation (IN PROGRESS)
- [ ] S1 Step 6: Transition to S2

---

## Quick Navigation

**Primary Reference:** `EPIC_README.md` → "Agent Status" section
- Contains current guide path
- Current step/iteration
- Next action
- Debugging status

**Current Guide:** `feature-updates/guides_v2/stages/s1/s1_epic_planning.md`
**Current Section:** Step 5 - Epic Structure Creation (lines 501-650)

**Feature Count:** 1 feature
**Feature 01:** `feature_01_remove_legacy_player_fetcher_features/`

---

## Discovery Phase Summary

**Status:** COMPLETE (user approved findings)
**Validation Loop:** 5 rounds (3 consecutive clean rounds achieved: Rounds 3, 4, 5)
**Questions Resolved:** 5 questions (Q0-Q4)

**Key Findings:**
1. Config values NOT yet deleted - deletion IS part of epic
2. 9 broken imports after config deletion (5 in exporter, 4 in main)
3. 9 export methods + 2 helpers to delete (~700-950 lines)
4. Locked preservation logic to remove (~100-150 lines)
5. DataFileManager accepts None parameter (no refactoring needed)
6. Settings class: 4 fields to remove + docstring update
7. Integration point: NFLProjectionsCollector.export_data() (lines 349-354)

**See:** `DISCOVERY.md` for complete research findings

---

## Epic Ticket Summary

**Status:** VALIDATED (user approved)
**File:** `EPIC_TICKET.md`

**Acceptance Criteria:** 10 items
**Success Indicators:** 7 metrics (700-950 lines removed, 9 config values deleted, etc.)
**Failure Patterns:** 8 scenarios

---

## Feature Structure Status

**Created:**
- [x] Feature folder: `feature_01_remove_legacy_player_fetcher_features/`
- [x] Feature README.md (Agent Status tracker)
- [x] Feature checklist.md (template)
- [x] Feature lessons_learned.md (template)
- [x] Epic epic_smoke_test_plan.md (placeholder)
- [x] Epic epic_lessons_learned.md (template)
- [x] Epic research/ folder with README.md
- [x] Epic GUIDE_ANCHOR.md (this file)

**Pending:**
- [ ] Update EPIC_README.md with Feature Tracking table
- [ ] Analyze feature dependencies (Step 5.7.5)
- [ ] Parallelization assessment (Steps 5.8-5.9)
- [ ] Complete S1 Step 5
- [ ] Transition to S2

---

## Important Files

**Epic-Level:**
- `EPIC_README.md` - Epic status and progress (ALWAYS READ FIRST)
- `EPIC_TICKET.md` - Acceptance criteria and success indicators
- `DISCOVERY.md` - Research findings and validation loop results
- `epic_smoke_test_plan.md` - Testing strategy (placeholder until S4)
- `epic_lessons_learned.md` - Retrospective (populated in S10)

**Feature-Level:**
- `feature_01_remove_legacy_player_fetcher_features/README.md` - Feature status
- `feature_01_remove_legacy_player_fetcher_features/checklist.md` - User questions (populated in S2)
- `feature_01_remove_legacy_player_fetcher_features/lessons_learned.md` - Feature retrospective (populated in S7.P3)

---

## Resumption Protocol

**If resuming after session compaction:**

1. **READ EPIC_README.md "Agent Status" section FIRST**
   - Check "Debugging Active" field
   - If YES, read `debugging/ISSUES_CHECKLIST.md` immediately
   - Check current guide path
   - Check current step/iteration
   - Check next action

2. **READ current guide** (path from Agent Status)
   - Use Read tool to load ENTIRE guide
   - Review current section/step
   - Verify prerequisites met

3. **READ current feature README.md** (if in S2-S8)
   - Check feature Agent Status
   - Verify feature progress
   - Check for debugging/ folder

4. **Use phase transition prompt** from `prompts_reference_v2.md`
   - Find prompt for current stage/phase
   - Acknowledge what you read
   - Update Agent Status

5. **Continue work** from exact step listed in Agent Status

**See:** `CLAUDE.md` → "Resuming In-Progress Epic Work" for complete protocol

---

## Notes

**This file is a backup reference only.**

The authoritative source is always EPIC_README.md Agent Status section, which is updated at every checkpoint and phase boundary.

If GUIDE_ANCHOR.md conflicts with EPIC_README.md, trust EPIC_README.md.
