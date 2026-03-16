# Epic Readme Template

**Filename:** `EPIC_README.md`
**Location:** `.shamt/epics/SHAMT-{N}-{epic_name}/EPIC_README.md`
**Created:** {YYYY-MM-DD}
**Updated:** Throughout all stages

**Purpose:** Central tracking document for the entire epic, containing Agent Status, progress tracker, and workflow checklists.

---

## Template

```markdown
## Epic: {epic_name}

**Created:** {YYYY-MM-DD}
**Status:** {IN PROGRESS / COMPLETE}
**Total Features:** {N}
**Testing Approach:** {A — Smoke only | B — Integration scripts (Recommended) | C — Unit tests only | D — Both}
**Integration Test Convention:** {Language/framework, directory, naming pattern, run command — or "N/A (Option A or C)"}

---

## 🎯 Quick Reference Card (Always Visible)

**Current Stage:** Stage X - {stage name}
**Active Guide:** `.shamt/guides/{guide_name}.md`
**Last Guide Read:** {YYYY-MM-DD HH:MM}

**Stage Workflow:**
```
S1 → S2 → S3 → [S5→S6→S7→S8] → S9 → S10
  ↓        ↓        ↓        ↓           ↓        ↓
Epic  Features  Sanity  Implementation  Epic    Done
Plan  Deep Dive  Check  (per feature)   QC
```text
(S4 deprecated — Test Scope Decision moved to S5 Step 0)

**You are here:** ➜ Stage {X}

**Critical Rules for Current Stage:**
1. {Rule 1 from current guide}
2. {Rule 2 from current guide}
3. {Rule 3 from current guide}
4. {Rule 4 from current guide}
5. {Rule 5 from current guide}

**Before Proceeding to Next Step:**
- [ ] Read guide: `.shamt/guides/{current_guide}.md`
- [ ] Acknowledge critical requirements
- [ ] Verify prerequisites from guide
- [ ] Update this Quick Reference Card

---

## Agent Status

**Debugging Active:** NO
**Last Updated:** {YYYY-MM-DD HH:MM}
**Current Stage:** Stage {X} - {stage name}
**Current Phase:** {PLANNING / IMPLEMENTATION / QC}
**Current Step:** {Specific step name - e.g., "Validation Round 2 (clean counter: 1)"}
**Current Guide:** `{guide_file_name}.md`
**Guide Last Read:** {YYYY-MM-DD HH:MM}

**Critical Rules from Guide:**
- {Rule 1 - e.g., "11 dimensions mandatory, complete Validation Loop required (3 consecutive clean rounds)"}
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

**Original Request:** `.shamt/epics/requests/{epic_name}.txt`

---

## Dependencies

**Inter-Epic Dependencies:**
{List any active epics this epic depends on, or "None"}

| Dependency Epic | Reason | Re-Validation Status |
|-----------------|--------|---------------------|
| {SHAMT-N — epic name} | {Brief reason this epic's plan depends on that epic's work} | {Pending / Done — {date}} |

**Re-Validation Reminder:** If a dependency epic above completes and merges, trigger the Dependency Re-Validation protocol in `stages/s5/s5_v2_validation_loop.md` before proceeding to S6. The user should provide the PR URL or commit range for the dependency's merged changes.

---

## Epic Progress Tracker

**Overall Status:** {X/Y features complete}

| Feature | S1 | S2 | S3 | S5 | S6 | S7 | S8.P1 | S8.P2 |
|---------|---------|---------|---------|----------|----------|----------|----------|----------|
| feature_01_{name} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} |
| feature_02_{name} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} |
| feature_03_{name} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} |

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


## Feature Dependency Groups (S2 Only)

**Skip this section if:**
- All features are independent (no spec-level dependencies)
- OR user declined parallel work

**Use this section to track group-based S2 parallelization waves**

### Group Structure

**Group 1 (Foundation - S2 Wave 1):**
- Feature {N}: {name}
- Spec Dependencies: None
- S2 Workflow: Completes S2 alone FIRST

**Group 2 (Dependent - S2 Wave 2):**
- Features {N}-{M}: {names}
- Spec Dependencies: Need Group 1's spec (API reference)
- S2 Workflow: After Group 1 completes S2, all features do S2 in parallel

**Group 3+ (if needed - S2 Wave 3+):**
- Features {N}-{M}: {names}
- Spec Dependencies: Need Group 2's spec
- S2 Workflow: After Group 2 completes S2, all features do S2 in parallel

### S2 Wave Execution

**After S2 Complete:**
- Groups no longer matter
- S3: Epic-level (all features together)
- S4: Deprecated (test scope decision now at S5 Step 0)
- S5-S8: Per-feature sequential (implementation dependencies checked separately)
- S9-S10: Epic-level

### Time Savings Calculation

**S2 Time Savings:**
- Sequential S2: {N} features × 2h = {total}h
- Group-based S2: Wave 1 ({M}h) + Wave 2 parallel ({M}h) + Wave 3 parallel ({M}h) = {total}h
- Savings: {X}h ({percent}% reduction)

**Example (7 features, 2 groups):**
- Sequential: 7 × 2h = 14h
- Group-based: Wave 1 (2h) + Wave 2 parallel (2h) = 4h
- Savings: 10h (71% reduction)

---

## 🔀 Parallel Work Configuration (If Applicable)

**Skip this section if working sequentially (single agent)**

**This section tracks parallel work coordination during S2**

**Parallelization Mode:** {Group-Based / Full Parallelization / Sequential}
- **Group-Based:** Features have spec-level dependencies, execute S2 in waves
- **Full Parallelization:** All features independent, execute S2 simultaneously
- **Sequential:** Single agent, features one-by-one

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
  - Run S3 solo after all features complete S2 (S4 deprecated)

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

**S3 → S5 Sync Point:**
- **Status:** {NOT_REACHED / WAITING / COMPLETE}
- **Primary Completed S3:** {YES/NO}
- **All Agents Notified:** {YES/NO}
- **Timestamp:** {YYYY-MM-DD HH:MM or "Not reached"}

### Coordination Status

**Current Phase:** {S2 Parallel / S3 Primary Solo / Sequential (post-S3)}

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
- **Current Phase:** {S2.P1 / S2.P2 / COMPLETE}
- **Last Update:** {timestamp}
- **Blockers:** {description or "None"}
- **Ready for Sync:** {YES/NO}

### <!-- FEATURE_01_S2_STATUS_END -->

### <!-- FEATURE_02_S2_STATUS_BEGIN -->

**Feature 02: {feature_name}**
- **Agent:** Secondary-A ({agent_id})
- **Current Phase:** {S2.P1 / S2.P2 / COMPLETE}
- **Last Update:** {timestamp}
- **Blockers:** {description or "None"}
- **Ready for Sync:** {YES/NO}

### <!-- FEATURE_02_S2_STATUS_END -->

### <!-- FEATURE_03_S2_STATUS_BEGIN -->

**Feature 03: {feature_name}**
- **Agent:** Secondary-B ({agent_id})
- **Current Phase:** {S2.P1 / S2.P2 / COMPLETE}
- **Last Update:** {timestamp}
- **Blockers:** {description or "None"}
- **Ready for Sync:** {YES/NO}

### <!-- FEATURE_03_S2_STATUS_END -->

### <!-- FEATURE_04_S2_STATUS_BEGIN -->

**Feature 04: {feature_name}**
- **Agent:** Secondary-C ({agent_id})
- **Current Phase:** {S2.P1 / S2.P2 / COMPLETE}
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
- [ ] Sibling epic awareness check completed (Step 0) — dependencies recorded in ## Dependencies if any
- [ ] Epic folder created
- [ ] All feature folders created
- [ ] Initial `epic_smoke_test_plan.md` created
- [ ] `EPIC_README.md` created (this file)
- [ ] `epic_lessons_learned.md` created
- [ ] Testing Approach (A/B/C/D) set in EPIC_README and epic ticket (Step 4.6.5)
- [ ] Parallelization assessment completed (Step 5.8-5.9)
- [ ] User chose: {PARALLEL / SEQUENTIAL} for S2

**S2 - Feature Deep Dives:**
- [ ] ALL features have `spec.md` complete
- [ ] ALL features have `checklist.md` resolved
- [ ] ALL feature `README.md` files created

**S2.P2 - Cross-Feature Alignment:**
- [ ] All feature pairs compared systematically (pairwise)
- [ ] Conflicts identified and resolved
- [ ] Affected specs updated, user approved resolutions

**S3 - Epic-Level Docs, Tests, and Approval:**
- [ ] S3.P1: `epic_smoke_test_plan.md` created (integration tests across ALL features)
- [ ] S3.P2: `EPIC_README.md` refined with feature summaries and architecture notes
- [ ] S3.P3: Gate 4.5 — epic plan approved by user (mandatory before S5; S4 deprecated)

**S4 - (Deprecated):** Test Scope Decision is now Step 0 of S5.

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
- [ ] Tests passed per Testing Approach (Options C/D: unit tests 100%; Options B/D: integration scripts exit 0; Option A: none)
- [ ] Documentation verified complete
- [ ] Guides updated based on lessons learned (if needed)
- [ ] Final commits made
- [ ] Epic moved to `.shamt/epics/done/{epic_name}/`

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

**Epic Location:** `.shamt/epics/done/{epic_name}/`
**Original Request:** `.shamt/epics/requests/{epic_name}.txt`

**Key Achievements:**
- {Achievement 1}
- {Achievement 2}
- {Achievement 3}

**Lessons Applied to Guides:**
- {Guide update 1 or "None"}
- {Guide update 2 or "None"}
```