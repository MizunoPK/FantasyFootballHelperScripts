# Guide Anchor: bug_fix-modify_player_data

**Created:** 2025-12-31
**Last Updated:** 2025-12-31

---

## Purpose

This file provides resumption instructions for agents after session compaction or interruption.

**When to use:**
- Session compacted (context window limit reached)
- Agent restarted/resumed
- Handoff between agent sessions

---

## Resumption Protocol

**STEP 1: Read EPIC_README.md**
- File: `feature-updates/bug_fix-modify_player_data/EPIC_README.md`
- Check the **"Agent Status"** section (top of file)
- Identify current stage, guide, and next action

**STEP 2: Use the "Resuming In-Progress Epic" prompt**
- File: `feature-updates/guides_v2/prompts_reference_v2.md`
- Find the "Resuming In-Progress Epic" prompt
- Use it to acknowledge guide and verify context

**STEP 3: Read the current guide**
- Guide name is listed in Agent Status
- Use Read tool to load the complete guide
- Verify prerequisites before continuing

**STEP 4: Continue from documented step**
- Agent Status shows exact step/iteration
- Follow guide from that point forward
- Update Agent Status after each major step

---

## Quick Reference

**Epic Name:** bug_fix-modify_player_data
**Epic Folder:** `feature-updates/bug_fix-modify_player_data/`
**Total Features:** 2 features

**Feature Folders:**
1. `feature_01_file_persistence/`
2. `feature_02_data_refresh/`

**Master Tracking:** `EPIC_README.md` (always check Agent Status first)

---

## Critical Rules

1. NEVER restart workflow - continue from documented step
2. ALWAYS read guide before proceeding
3. ALWAYS update Agent Status after major steps
4. CHECK for completed features before starting new ones

---

**END OF GUIDE ANCHOR**
