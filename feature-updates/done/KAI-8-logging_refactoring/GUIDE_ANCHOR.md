# Guide Anchor: logging_refactoring

**Epic:** KAI-8-logging_refactoring
**Created:** 2026-02-06 (S1)
**Last Updated:** 2026-02-06 (S1)

---

## Purpose

This file ensures agents can resume correctly after session compaction or context window limits. It provides quick navigation to the current stage and active guide.

**When to use this file:**
- Session compacts and agent needs to resume work
- Multiple agents working on epic (parallel S2)
- User returns to epic after time away
- Agent starts work on in-progress epic

---

## Current Stage Identification

**Current Stage:** S1 (Epic Planning)
**Stage Status:** COMPLETING
**Current Phase:** S1 Step 5 (Epic Structure Creation)
**Date Last Updated:** 2026-02-06

**Next Stage:** S2 (Feature Deep Dive) for Feature 01

---

## Active Guide

**Current Guide:** `feature-updates/guides_v2/stages/s1/s1_epic_planning.md`
**Guide Last Read:** 2026-02-06 20:05
**Current Step:** S1 Step 5 complete, proceeding to S1 Step 6 (Transition to S2)

**Next Guide:** `feature-updates/guides_v2/stages/s2/s2_feature_deep_dive.md` (after S1 complete)

---

## Resumption Instructions for Agents

**If resuming this epic, follow these steps:**

1. **Read EPIC_README.md Agent Status section FIRST**
   - Location: `feature-updates/KAI-8-logging_refactoring/EPIC_README.md`
   - Check "Agent Status" section for current step and guide

2. **Check for active debugging**
   - Look for `debugging/` folder in epic or feature folders
   - If exists, read `debugging/ISSUES_CHECKLIST.md` FIRST
   - Active debugging takes priority over Agent Status

3. **Read the current guide listed in Agent Status**
   - Use Read tool to load ENTIRE guide
   - Find the current step/iteration from Agent Status
   - Continue from that point

4. **Use phase transition prompt from prompts_reference_v2.md**
   - Location: `feature-updates/guides_v2/prompts_reference_v2.md`
   - Find prompt for current stage/phase
   - Acknowledge what you read, verify prerequisites, update Agent Status

5. **DO NOT restart workflow from beginning**
   - EPIC_README.md Agent Status survives context compaction
   - Resume from exact point where previous agent left off

---

## Workflow Reference Diagram

```
S1 → S2 → S3 → S4 → [S5→S6→S7→S8] → S9 → S10
 ↓        ↓        ↓        ↓        ↓           ↓        ↓
Epic  Features  Sanity  Testing  Implementation  Epic    Done
Plan  Deep Dive  Check  Strategy  (per feature)   QC
```

**You are here:** ➜ S1 (completing) → Next: S2 for Feature 01

---

## Key Epic Files

**Epic-Level (in epic root):**
- `EPIC_README.md` - Central tracking, Agent Status (CHECK THIS FIRST)
- `EPIC_TICKET.md` - User-validated epic outcomes (IMMUTABLE after validation)
- `DISCOVERY.md` - Discovery Phase findings (user-approved)
- `epic_smoke_test_plan.md` - Epic testing plan (updated in S4, S8.P2)
- `epic_lessons_learned.md` - Cross-feature insights
- `GUIDE_ANCHOR.md` - This file (resumption guidance)
- `research/` - Research documents folder

**Feature-Level (per feature folder):**
- `README.md` - Feature tracking, Agent Status
- `spec.md` - Requirements (seeded with Discovery Context)
- `checklist.md` - User questions and decisions
- `lessons_learned.md` - Feature-specific insights
- `implementation_plan.md` - Created in S5 (user-approved)
- `implementation_checklist.md` - Created in S6 (progress tracking)

---

## Critical Rules for Current Stage

**S1 Critical Rules:**
1. CREATE GIT BRANCH BEFORE ANY CHANGES (Step 1.0) ✅ COMPLETE
2. DISCOVERY PHASE IS MANDATORY (Step 3) ✅ COMPLETE
3. DISCOVERY LOOP UNTIL 3 CONSECUTIVE CLEAN ITERATIONS ✅ COMPLETE
4. USER MUST APPROVE feature breakdown before creating epic ticket ✅ COMPLETE
5. CREATE EPIC TICKET and get user validation (Steps 4.6-4.7) ✅ COMPLETE

**S1 Status:**
- Git branch: epic/KAI-8 ✅
- Discovery Phase: COMPLETE (user approved) ✅
- Epic ticket: VALIDATED (user approved) ✅
- Epic structure: COMPLETING (Step 5 in progress)

---

## Notes

**This file is updated at stage transitions** to reflect current stage, guide, and resumption instructions. Check EPIC_README.md Agent Status for most current information.

**Version:** S1
**Next Update:** After S1 → S2 transition
