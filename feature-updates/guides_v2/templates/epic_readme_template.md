# Epic Readme Template

**Filename:** `EPIC_README.md`
**Location:** `feature-updates/KAI-{N}-{epic_name}/EPIC_README.md`
**Created:** {YYYY-MM-DD}
**Updated:** Throughout all stages

**Purpose:** Central tracking document for the entire epic, containing Agent Status, progress tracker, and workflow checklists.

---

## Template

```markdown
# Epic: {epic_name}

**Created:** {YYYY-MM-DD}
**Status:** {IN PROGRESS / COMPLETE}
**Total Features:** {N}

---

## 🎯 Quick Reference Card (Always Visible)

**Current Stage:** Stage X - {stage name}
**Active Guide:** `guides_v2/{guide_name}.md`
**Last Guide Read:** {YYYY-MM-DD HH:MM}

**Stage Workflow:**
```text
S1 → S2 → S3 → S4 → [S5→S6→S7→S8] → S9 → S10
  ↓        ↓        ↓        ↓        ↓           ↓        ↓
Epic  Features  Sanity  Testing  Implementation  Epic    Done
Plan  Deep Dive  Check  Strategy  (per feature)   QC
```markdown

**You are here:** ➜ Stage {X}

**Critical Rules for Current Stage:**
1. {Rule 1 from current guide}
2. {Rule 2 from current guide}
3. {Rule 3 from current guide}
4. {Rule 4 from current guide}
5. {Rule 5 from current guide}

**Before Proceeding to Next Step:**
- [ ] Read guide: `guides_v2/{current_guide}.md`
- [ ] Acknowledge critical requirements
- [ ] Verify prerequisites from guide
- [ ] Update this Quick Reference Card

---

## Agent Status

**Debugging Active:** NO
**Last Updated:** {YYYY-MM-DD HH:MM}
**Current Stage:** Stage {X} - {stage name}
**Current Phase:** {PLANNING / IMPLEMENTATION / QC}
**Current Step:** {Specific step name - e.g., "QC Round 2 (Consistency)"}
**Current Guide:** `{guide_file_name}.md`
**Guide Last Read:** {YYYY-MM-DD HH:MM}

**Critical Rules from Guide:**
- {Rule 1 - e.g., "22 iterations mandatory, no skipping"}
- {Rule 2 - e.g., "Update Agent Status after each round"}
- {Rule 3 - e.g., "STOP if confidence < Medium"}
- {Rule 4 - e.g., "RESTART Post-Implementation if ANY issues found"}
- {Rule 5 - e.g., "Verify against ACTUAL implementation"}

**Progress:** {X/Y items complete}
**Next Action:** {Exact next task with guide step reference}
**Blockers:** {List any issues or "None"}

---

## Epic Overview

**Epic Goal:**
{Concise description of what this epic achieves - pulled from original {epic_name}.txt request}

**Epic Scope:**
{High-level scope - what's included and what's excluded}

**Key Outcomes:**
1. {Outcome 1}
2. {Outcome 2}
3. {Outcome 3}

**Original Request:** `feature-updates/{epic_name}.txt`

---

## Epic Progress Tracker

**Overall Status:** {X/Y features complete}

| Feature | S1 | S2 | S3 | S4 | S5 | S6 | S7 | S8.P1 | S8.P2 |
|---------|---------|---------|---------|---------|----------|----------|----------|----------|----------|
| feature_01_{name} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} |
| feature_02_{name} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} |
| feature_03_{name} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} |

**Legend:**
- ✅ = Complete
- ◻️ = Not started or in progress

**S9 - Epic Final QC:** {✅ COMPLETE / ◻️ NOT STARTED / 🔄 IN PROGRESS}
- Epic smoke testing passed: {✅/◻️}
- Epic QC rounds passed: {✅/◻️}
- Epic PR review passed: {✅/◻️}
- End-to-end validation passed: {✅/◻️}
- Date completed: {YYYY-MM-DD or "Not complete"}

**S10 - Epic Cleanup:** {✅ COMPLETE / ◻️ NOT STARTED / 🔄 IN PROGRESS}
- Final commits made: {✅/◻️}
- Epic moved to done/ folder: {✅/◻️}
- Date completed: {YYYY-MM-DD or "Not complete"}

---

## Feature Summary

### Feature 01: {feature_name}
**Folder:** `feature_01_{name}/`
**Purpose:** {Brief description}
**Status:** {Stage X complete}
**Dependencies:** {List other features or "None"}

### Feature 02: {feature_name}
**Folder:** `feature_02_{name}/`
**Purpose:** {Brief description}
**Status:** {Stage X complete}
**Dependencies:** {List other features or "None"}

### Feature 03: {feature_name}
**Folder:** `feature_03_{name}/`
**Purpose:** {Brief description}
**Status:** {Stage X complete}
**Dependencies:** {List other features or "None"}

{Continue for all features...}


## 🔀 Parallel Work Configuration (If Applicable)

**Skip this section if working sequentially (single agent)**

**This section tracks parallel work during S2 (Feature Deep Dives)**

### Agent Assignments

**Primary Agent:**
- **Agent ID:** {primary_agent_id}
- **Role:** Coordinator + Feature Owner
- **Assigned Feature:** feature_01_{name}
- **Responsibilities:**
  - Execute S2 for Feature 01
  - Generate handoff packages for secondaries
  - Monitor coordination channels
  - Handle escalations within 15 min SLA
  - Run S3 and S4 solo after all features complete S2

**Secondary Agents:**

| Agent ID | Role | Assigned Feature | Status | Last Checkpoint |
|----------|------|------------------|--------|----------------|
| Secondary-A | Feature Owner | feature_02_{name} | {IN_PROGRESS/COMPLETE/BLOCKED} | {timestamp} |
| Secondary-B | Feature Owner | feature_03_{name} | {IN_PROGRESS/COMPLETE/BLOCKED} | {timestamp} |
| Secondary-C | Feature Owner | feature_04_{name} | {IN_PROGRESS/COMPLETE/BLOCKED} | {timestamp} |

### Coordination Channels

**Communication Files:**
- Primary → Secondary-A: `agent_comms/primary_to_secondary_a.md`
- Secondary-A → Primary: `agent_comms/secondary_a_to_primary.md`
- Primary → Secondary-B: `agent_comms/primary_to_secondary_b.md`
- Secondary-B → Primary: `agent_comms/secondary_b_to_primary.md`
- Primary → Secondary-C: `agent_comms/primary_to_secondary_c.md`
- Secondary-C → Primary: `agent_comms/secondary_c_to_primary.md`

**Checkpoint Files:**
- Primary: `agent_checkpoints/{primary_agent_id}.json`
- Secondary-A: `agent_checkpoints/secondary_a.json`
- Secondary-B: `agent_checkpoints/secondary_b.json`
- Secondary-C: `agent_checkpoints/secondary_c.json`

**STATUS Files (per feature):**
- Feature 01: `feature_01_{name}/STATUS`
- Feature 02: `feature_02_{name}/STATUS`
- Feature 03: `feature_03_{name}/STATUS`
- Feature 04: `feature_04_{name}/STATUS`

### Sync Points

**S2 → S3 Sync Point:**
- **Status:** {NOT_REACHED / WAITING / COMPLETE}
- **All Agents Ready:** {YES/NO}
- **Verification Complete:** {YES/NO}
- **Timestamp:** {YYYY-MM-DD HH:MM or "Not reached"}

**S4 → S5 Sync Point:**
- **Status:** {NOT_REACHED / WAITING / COMPLETE}
- **Primary Completed S3/S4:** {YES/NO}
- **All Agents Notified:** {YES/NO}
- **Timestamp:** {YYYY-MM-DD HH:MM or "Not reached"}

### Coordination Status

**Current Phase:** {S2 Parallel / S3 Primary Solo / S4 Primary Solo / Sequential (post-S4)}

**Active Agents:** {N} ({primary_count} primary + {secondary_count} secondaries)

**Escalations:**

| Timestamp | From Agent | Feature | Issue | Status | Resolution Time |
|-----------|------------|---------|-------|--------|----------------|
| {timestamp} | {agent_id} | {feature} | {brief description} | {OPEN/RESOLVED} | {minutes or N/A} |

{If no escalations: "No escalations"}

**Stale Agent Checks:**

| Check Time | Agent | Last Checkpoint | Status | Action Taken |
|------------|-------|----------------|--------|--------------|
| {timestamp} | {agent_id} | {timestamp} | {ACTIVE/WARNING/STALE} | {message sent / user escalated / N/A} |

{If no stale checks needed: "All agents active"}

---

## 🔄 Per-Feature S2 Progress (Parallel Work)

**This section tracks detailed S2 progress for each feature during parallel work**

### <!-- FEATURE_01_S2_STATUS_BEGIN -->

**Feature 01: {feature_name}**
- **Agent:** Primary ({agent_id})
- **Current Phase:** {S2.P1 / S2.P2 / S2.P3 / COMPLETE}
- **Last Update:** {timestamp}
- **Blockers:** {description or "None"}
- **Ready for Sync:** {YES/NO}

### <!-- FEATURE_01_S2_STATUS_END -->

### <!-- FEATURE_02_S2_STATUS_BEGIN -->

**Feature 02: {feature_name}**
- **Agent:** Secondary-A ({agent_id})
- **Current Phase:** {S2.P1 / S2.P2 / S2.P3 / COMPLETE}
- **Last Update:** {timestamp}
- **Blockers:** {description or "None"}
- **Ready for Sync:** {YES/NO}

### <!-- FEATURE_02_S2_STATUS_END -->

### <!-- FEATURE_03_S2_STATUS_BEGIN -->

**Feature 03: {feature_name}**
- **Agent:** Secondary-B ({agent_id})
- **Current Phase:** {S2.P1 / S2.P2 / S2.P3 / COMPLETE}
- **Last Update:** {timestamp}
- **Blockers:** {description or "None"}
- **Ready for Sync:** {YES/NO}

### <!-- FEATURE_03_S2_STATUS_END -->

### <!-- FEATURE_04_S2_STATUS_BEGIN -->

**Feature 04: {feature_name}**
- **Agent:** Secondary-C ({agent_id})
- **Current Phase:** {S2.P1 / S2.P2 / S2.P3 / COMPLETE}
- **Last Update:** {timestamp}
- **Blockers:** {description or "None"}
- **Ready for Sync:** {YES/NO}

### <!-- FEATURE_04_S2_STATUS_END -->

**Note:** BEGIN/END markers allow agents to update only their sections without lock contention

---

---

## Bug Fix Summary

**Bug Fixes Created:** {N}

{If no bug fixes: "No bug fixes created yet"}

{If bug fixes exist:}

### Bug Fix 1: {name}
**Folder:** `bugfix_{priority}_{name}/`
**Priority:** {high/medium/low}
**Discovered:** {Stage X - {feature or epic level}}
**Status:** {S7 complete / In progress}
**Impact:** {Brief description of what bug affected}

{Repeat for all bug fixes...}

---

## Epic-Level Files

**Created in S1:**
- `EPIC_README.md` (this file)
- `epic_smoke_test_plan.md` - How to test the complete epic
- `epic_lessons_learned.md` - Cross-feature insights

**Feature Folders:**
- `feature_01_{name}/` - {Brief purpose}
- `feature_02_{name}/` - {Brief purpose}
- `feature_03_{name}/` - {Brief purpose}

**Bug Fix Folders (if any):**
- `bugfix_{priority}_{name}/` - {Brief description}

---

## Workflow Checklist

**S1 - Epic Planning:**
- [ ] Epic folder created
- [ ] All feature folders created
- [ ] Initial `epic_smoke_test_plan.md` created
- [ ] `EPIC_README.md` created (this file)
- [ ] `epic_lessons_learned.md` created
- [ ] Parallelization assessment completed (Step 5.8-5.9)
- [ ] User chose: {PARALLEL / SEQUENTIAL} for S2

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

**S5 - Feature Implementation:**
- [ ] Feature 1: S5→S6→S7→S8 complete
- [ ] Feature 2: S5→S6→S7→S8 complete
- [ ] Feature 3: S5→S6→S7→S8 complete
- [ ] {List all features}

**S9 - Epic Final QC:**
- [ ] Epic smoke testing passed (all 4 parts)
- [ ] Epic QC rounds passed (all 3 rounds)
- [ ] Epic PR review passed (all 11 categories)
- [ ] End-to-end validation vs original request passed

**S10 - Epic Cleanup:**
- [ ] All unit tests passing (100%)
- [ ] Documentation verified complete
- [ ] Guides updated based on lessons learned (if needed)
- [ ] Final commits made
- [ ] Epic moved to `feature-updates/done/{epic_name}/`

---

## Guide Deviation Log

**Purpose:** Track when agent deviates from guide (helps identify guide gaps)

| Timestamp | Stage | Deviation | Reason | Impact |
|-----------|-------|-----------|--------|--------|
| {YYYY-MM-DD HH:MM} | {Stage X} | {What was skipped/changed} | {Why agent deviated} | {Consequence - e.g., "QC failed, rework required"} |

**Rule:** If you deviate from guide, DOCUMENT IT HERE immediately.

{If no deviations: "No deviations from guides"}

---

## Epic Completion Summary

{This section filled out in S10}

**Completion Date:** {YYYY-MM-DD}
**Start Date:** {YYYY-MM-DD}
**Duration:** {N days}

**Features Implemented:** {N}
**Bug Fixes Created:** {N}

**Final Test Pass Rate:** {X/Y tests passing} ({percentage}%)

**Epic Location:** `feature-updates/done/{epic_name}/`
**Original Request:** `feature-updates/{epic_name}.txt`

**Key Achievements:**
- {Achievement 1}
- {Achievement 2}
- {Achievement 3}

**Lessons Applied to Guides:**
- {Guide update 1 or "None"}
- {Guide update 2 or "None"}
```