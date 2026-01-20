# Epic: improve_debugging_runs

**Created:** 2026-01-20
**Status:** IN PROGRESS
**Total Features:** TBD (after Discovery)

---

## Quick Reference Card (Always Visible)

**Current Stage:** Stage 1 - Epic Planning
**Active Guide:** `guides_v2/stages/s1/s1_epic_planning.md`
**Last Guide Read:** 2026-01-20 09:00

**Stage Workflow:**
```
S1 → S2 → S3 → S4 → [S5→S6→S7→S8] → S9 → S10
  ↓        ↓        ↓        ↓        ↓           ↓        ↓
Epic  Features  Sanity  Testing  Implementation  Epic    Done
Plan  Deep Dive  Check  Strategy  (per feature)   QC
```

**You are here:** S1 (Epic Planning) - Step 1 (Initial Setup)

**Critical Rules for Current Stage:**
1. Discovery Phase is MANDATORY - cannot create feature folders without it
2. Discovery Loop continues until NO NEW QUESTIONS emerge
3. User approves Discovery before feature folders are created
4. Create epic ticket and get user validation before folder creation
5. Update Agent Status after EACH major step

**Before Proceeding to Next Step:**
- [x] Read guide: `guides_v2/stages/s1/s1_epic_planning.md`
- [x] Acknowledge critical requirements
- [x] Verify prerequisites from guide
- [ ] Update this Quick Reference Card

---

## Agent Status

**Last Updated:** 2026-01-20 09:00
**Current Stage:** Stage 1 - Epic Planning
**Current Phase:** PLANNING
**Current Step:** Step 1 - Initial Setup (in progress)
**Current Guide:** `stages/s1/s1_epic_planning.md`
**Guide Last Read:** 2026-01-20 09:00

**Critical Rules from Guide:**
- Discovery is MANDATORY for every epic
- Discovery Loop continues until no new questions
- User answers questions throughout Discovery
- Feature folders NOT created until Discovery approved
- Update Agent Status after EACH major step

**Progress:** 1/6 steps in progress (Initial Setup)
**Next Action:** Complete Step 1, then proceed to Step 2 (Epic Analysis)
**Blockers:** None

---

## Epic Overview

**Epic Goal:**
Create automated debug/test runs for each script to make smoke testing easier, particularly enabling agents to test independently without user interaction.

**Epic Scope:**
Create debugging versions of all major scripts that can run non-interactively with log output.

**Key Outcomes:**
1. Automated test runs that create log files
2. Non-interactive smoke testing for all major components
3. Agents can validate functionality independently

**Original Request:** `improve_debugging_runs_notes.txt`

---

## Epic Progress Tracker

**Overall Status:** 0/TBD features complete

| Feature | S1 | S2 | S3 | S4 | S5 | S6 | S7 | S8.P1 | S8.P2 |
|---------|---------|---------|---------|---------|----------|----------|----------|----------|----------|
| TBD after Discovery | - | - | - | - | - | - | - | - | - |

**S9 - Epic Final QC:** Not Started
**S10 - Epic Cleanup:** Not Started

---

## Feature Summary

{Features will be defined after Discovery Phase}

---

## Bug Fix Summary

**Bug Fixes Created:** 0

No bug fixes created yet

---

## Epic-Level Files

**Created in S1:**
- `EPIC_README.md` (this file)
- `epic_smoke_test_plan.md` - TBD
- `epic_lessons_learned.md` - TBD
- `DISCOVERY.md` - TBD (created in Step 3)

**Feature Folders:**
{TBD after Discovery}

---

## Workflow Checklist

**S1 - Epic Planning:**
- [x] Git branch created (epic/KAI-7)
- [x] EPIC_TRACKER.md updated
- [x] Epic folder created
- [x] `EPIC_README.md` created (this file)
- [ ] DISCOVERY.md created and user-approved
- [ ] Feature breakdown approved
- [ ] Epic ticket created and validated
- [ ] Feature folders created
- [ ] `epic_smoke_test_plan.md` created
- [ ] `epic_lessons_learned.md` created

**S2 - Feature Deep Dives:**
- [ ] ALL features have `spec.md` complete
- [ ] ALL features have `checklist.md` resolved
- [ ] ALL feature `README.md` files created

**S3 - Cross-Feature Sanity Check:**
- [ ] All specs compared systematically
- [ ] Conflicts resolved
- [ ] User sign-off obtained

**S4 - Epic Testing Strategy:**
- [ ] `epic_smoke_test_plan.md` updated based on deep dives
- [ ] Integration points identified
- [ ] Epic success criteria defined

**S5-S8 - Feature Implementation:**
{TBD after features defined}

**S9 - Epic Final QC:**
- [ ] Epic smoke testing passed
- [ ] Epic QC rounds passed
- [ ] Epic PR review passed
- [ ] End-to-end validation passed

**S10 - Epic Cleanup:**
- [ ] All unit tests passing (100%)
- [ ] Documentation verified complete
- [ ] Guides updated based on lessons learned
- [ ] Final commits made
- [ ] Epic moved to `feature-updates/done/`

---

## Guide Deviation Log

**Purpose:** Track when agent deviates from guide

| Timestamp | Stage | Deviation | Reason | Impact |
|-----------|-------|-----------|--------|--------|

No deviations from guides

---

## Epic Completion Summary

{This section filled out in S10}
