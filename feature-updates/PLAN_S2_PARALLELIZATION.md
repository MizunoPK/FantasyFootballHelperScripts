# Implementation Plan: S2 Parallelization Only

**Version:** 1.0
**Date:** 2026-01-15
**Scope:** Enable parallel feature deep dives (S2 only)
**Risk Level:** LOW (documentation only, no code conflicts)

---

## Executive Summary

**Objective:** Enable multiple agents to work on S2 (Feature Deep Dives) simultaneously, reducing epic planning time by 40-60% for epics with 3+ features.

**Scope:** S2 parallelization ONLY - features are researched and specified in parallel
- ✅ S2: Feature Deep Dives (parallel)
- ❌ S5-S8: Feature Implementation (remains sequential)

**Time Savings Example (3-feature epic):**
```
Sequential S2:
- Feature 1: 2 hours
- Feature 2: 2 hours
- Feature 3: 2 hours
Total: 6 hours

Parallel S2:
- All 3 features: 2 hours (max of 2, 2, 2)
Total: 2 hours

SAVINGS: 4 hours (67% reduction in S2 time)
```

**Epic-Level Time Savings:**
```
Sequential Epic (3 features):
S1: 2h | S2: 6h | S3: 1h | S4: 1h | S5-S8: 15h | S9: 2h | S10: 1h
Total: 28 hours

Parallel S2 Epic (3 features):
S1: 2h | S2: 2h | S3: 1h | S4: 1h | S5-S8: 15h | S9: 2h | S10: 1h
Total: 24 hours

SAVINGS: 4 hours (14% epic-level reduction)
```

**Why S2 Only First:**
1. **Lower Risk** - Documentation only (no code conflicts)
2. **Lower Complexity** - No git branch management needed
3. **Fast Validation** - Test coordination mechanisms with minimal stakes
4. **High Value** - 2-3 hours savings per feature
5. **Foundation** - Proves coordination infrastructure for future S5-S8

**Risk Level:** LOW
- No code merge conflicts (documentation only)
- Shared files are sectioned (minimal conflicts)
- Communication via dedicated channels
- Checkpoint system prevents lost work

**Implementation Time:** 6-8 hours (guide creation + testing)

**Pilot Approach:** Test with 2-feature epic before broad rollout

---

## Table of Contents

1. [Scope Definition](#scope-definition)
2. [Architecture](#architecture)
3. [Implementation Phases](#implementation-phases)
4. [Guide Changes Required](#guide-changes-required)
5. [Coordination Mechanisms](#coordination-mechanisms)
6. [User Experience Flow](#user-experience-flow)
7. [Risk Analysis](#risk-analysis)
8. [Success Metrics](#success-metrics)
9. [Pilot Plan](#pilot-plan)
10. [Rollout Strategy](#rollout-strategy)

---

## Scope Definition

### In Scope

**Parallelizable Work:**
- ✅ S2.P1: Research Phase (all features simultaneously)
- ✅ S2.P2: Specification Phase (all features simultaneously)
- ✅ S2.P3: Refinement Phase (all features simultaneously)

**Coordination Infrastructure:**
- ✅ Lock file system (.epic_locks/)
- ✅ Communication channels (agent_comms/)
- ✅ Checkpoint system (agent_checkpoints/)
- ✅ STATUS files per feature
- ✅ Handoff package generator
- ✅ Sectioned EPIC_README.md

**Agent Roles:**
- ✅ Primary Agent (coordinates, owns Feature 01)
- ✅ Secondary Agent(s) (owns Feature 02, 03, etc.)

### Out of Scope

**Sequential Work (Unchanged):**
- ❌ S1: Epic Planning (remains Primary only)
- ❌ S3: Cross-Feature Sanity Check (remains Primary only)
- ❌ S4: Epic Testing Strategy (remains Primary only)
- ❌ S5-S8: Feature Implementation Loop (remains sequential)
- ❌ S9: Epic Final QC (remains Primary only)
- ❌ S10: Epic Cleanup (remains Primary only)

**Not Implemented:**
- ❌ Git branch management (not needed for S2)
- ❌ Code merge protocol (no code in S2)
- ❌ Test suite coordination (no tests in S2)
- ❌ Dynamic wave reorganization (deferred to S5-S8 parallelization)

### Sync Points

**Mandatory Synchronization:**

**Sync Point 1: After S1 → Before S2**
- Primary completes S1 (Epic Planning)
- Primary offers parallel work to user
- If accepted: Primary generates handoff packages
- User starts secondary agent session(s)
- All agents claim their features

**Sync Point 2: After S2 → Before S3**
- All agents complete S2.P3 for assigned features
- Status: WAITING until all features complete
- Timeout: 2 hours from first completion
- If timeout: Defer slow features to Wave 2
- Once all ready: Primary proceeds with S3

**Sync Point 3: After S3 → Before S5**
- Primary completes S3 (Cross-Feature Sanity Check)
- Primary completes S4 (Epic Testing Strategy)
- Primary signals release: "S3 and S4 complete"
- Secondary agents transition to feature implementation
- **NOTE:** Implementation remains sequential in this plan

---

## Architecture

### Directory Structure

```
feature-updates/KAI-N-epic_name/
├── EPIC_README.md                 # Sectioned (agents own sections)
├── epic_smoke_test_plan.md
├── epic_lessons_learned.md
│
├── .epic_locks/                   # Lock files (NEW)
│   ├── epic_readme.lock
│   └── epic_smoke_test_plan.lock
│
├── agent_comms/                   # Communication channels (NEW)
│   ├── primary_to_secondary_a.md
│   ├── secondary_a_to_primary.md
│   ├── primary_to_secondary_b.md
│   └── secondary_b_to_primary.md
│
├── agent_checkpoints/             # Checkpoint files (NEW)
│   ├── primary.json
│   ├── secondary_a.json
│   └── secondary_b.json
│
├── feature_01_player_json/
│   ├── STATUS                     # Status file (NEW)
│   ├── README.md
│   ├── spec.md
│   ├── checklist.md
│   ├── implementation_plan.md
│   └── lessons_learned.md
│
├── feature_02_team_penalty/
│   ├── STATUS                     # Status file (NEW)
│   ├── README.md
│   ├── spec.md
│   ├── checklist.md
│   └── lessons_learned.md
│
└── feature_03_scoring_update/
    ├── STATUS                     # Status file (NEW)
    ├── README.md
    ├── spec.md
    ├── checklist.md
    └── lessons_learned.md
```

### Agent Coordination Model

```
┌─────────────────────────────────────────────────────────┐
│                    PRIMARY AGENT                        │
│  - Owns Feature 01                                      │
│  - Coordinates parallel work                            │
│  - Owns epic-level files                                │
│  - Runs S1, S3, S4, S9, S10                            │
│  - Monitors secondary agents                            │
└─────────────────────────────────────────────────────────┘
          │                                   │
          │ handoff package                   │ handoff package
          ▼                                   ▼
┌──────────────────────────┐    ┌──────────────────────────┐
│   SECONDARY AGENT A      │    │   SECONDARY AGENT B      │
│  - Owns Feature 02       │    │  - Owns Feature 03       │
│  - Works on S2 only      │    │  - Works on S2 only      │
│  - Reports via comms/    │    │  - Reports via comms/    │
│  - Escalates to Primary  │    │  - Escalates to Primary  │
└──────────────────────────┘    └──────────────────────────┘

All agents work simultaneously on S2:
- Primary: S2 for Feature 01
- Secondary A: S2 for Feature 02
- Secondary B: S2 for Feature 03

After S2 complete → Sync → Primary runs S3 alone
```

---

## Implementation Phases

### Phase 1: Core Infrastructure (3-4 hours)

**Deliverables:**

1. **Lock File System**
   - Guide: `parallel_work/lock_file_protocol.md`
   - Functions: acquire_lock(), release_lock()
   - Lock files: epic_readme.lock, epic_smoke_test_plan.lock

2. **Communication Channels**
   - Guide: `parallel_work/communication_protocol.md`
   - Channel files: primary_to_secondary_X.md, secondary_X_to_primary.md
   - Message format templates

3. **Checkpoint System**
   - Guide: `parallel_work/checkpoint_protocol.md`
   - Checkpoint file format (JSON)
   - Update frequency: Every 15 minutes
   - Stale detection: 30/60 minute timeouts

4. **STATUS Files**
   - Template: `templates/feature_status_template.txt`
   - Format: Key-value pairs
   - Updated at: Phase transitions, checkpoints

5. **Handoff Package Generator**
   - Template: `templates/handoff_package_template.md`
   - Auto-populated with: epic path, feature assignment, agent IDs

**Testing:**
- Create mock epic with 2 features
- Test lock acquisition/release
- Test communication channel read/write
- Test checkpoint creation/update
- Test handoff package generation

**Exit Criteria:**
- All infrastructure components working
- Documentation complete
- Templates tested

---

### Phase 2: S2 Workflow Integration (2-3 hours)

**Deliverables:**

1. **S1 Guide Updates**
   - File: `stages/s1/s1_epic_planning.md`
   - Add: Feature dependency analysis
   - Add: Parallel work assessment
   - Add: User prompt for parallel work option

2. **S2 Guide Updates**
   - Files: `stages/s2/*.md` (router + 3 sub-phases)
   - Add: Agent role check (Primary vs Secondary)
   - Add: Communication protocol integration
   - Add: Checkpoint update instructions
   - Add: Secondary agent entry points

3. **S3 Guide Updates**
   - File: `stages/s3/s3_cross_feature_sanity_check.md`
   - Add: Verification that all features completed S2
   - Add: Sync status check
   - Add: Handling of deferred features (if timeout)

4. **Primary Agent Guide**
   - File: `parallel_work/s2_primary_agent_guide.md`
   - Responsibilities: Coordination, monitoring, S3 execution
   - Workflow: Offer parallel work → generate handoffs → monitor → run S3

5. **Secondary Agent Guide**
   - File: `parallel_work/s2_secondary_agent_guide.md`
   - Responsibilities: S2 execution for assigned feature only
   - Workflow: Startup → claim feature → execute S2 → signal complete

**Testing:**
- Walk through S1 → S2 transition
- Verify handoff package works
- Test S2.P1, P2, P3 with agent role awareness
- Test S2 → S3 sync

**Exit Criteria:**
- All guides updated and consistent
- Agent role logic correct
- Sync points clearly defined

---

### Phase 3: EPIC_README Sectioning (1 hour)

**Deliverables:**

1. **EPIC_README Template Update**
   - File: `templates/epic_readme_template.md`
   - Add: BEGIN/END section markers
   - Add: Agent Assignment table
   - Add: Sync Status section

2. **Sectioning Protocol**
   - Guide: `parallel_work/epic_readme_sectioning.md`
   - Rules: Agents only edit their sections
   - Conflict resolution: Primary has override

**Example Structure:**
```markdown
# Epic KAI-6: NFL Team Penalty Scoring

## Quick Reference Card
[Epic-level - Primary only]

## Agent Assignment Table
[Primary updates - shows all agents and features]

<!-- BEGIN PRIMARY PROGRESS -->
## Feature 01 Progress (Primary)
**Last Updated:** 2026-01-15 14:30
**Current Stage:** S2.P2
**Next Action:** Complete spec.md
<!-- END PRIMARY PROGRESS -->

<!-- BEGIN SECONDARY-A PROGRESS -->
## Feature 02 Progress (Secondary-A)
**Last Updated:** 2026-01-15 14:25
**Current Stage:** S2.P1
**Next Action:** Research Phase
<!-- END SECONDARY-A PROGRESS -->

## Sync Status
[Primary updates - shows sync point status]

## Epic Progress Tracker
[Primary updates after S3]
```

**Testing:**
- Create sectioned EPIC_README.md
- Test concurrent edits to different sections
- Verify git handles sections cleanly

**Exit Criteria:**
- Template complete
- Sectioning protocol documented
- No merge conflicts when agents edit different sections

---

### Phase 4: User Experience (1 hour)

**Deliverables:**

1. **Parallel Work Offering Prompt**
   - File: `prompts/parallel_work_prompts.md`
   - Template for Primary to offer parallel work
   - Shows time savings calculation
   - Three options: Enable, Sequential, Discuss

2. **Handoff Package Format**
   - Template refined and tested
   - Copy-paste ready
   - Includes all configuration

3. **Secondary Agent Startup Prompt**
   - Secondary agent recognizes handoff package
   - Self-configures from package
   - Confirms setup to user

4. **Sync Point User Communication**
   - Primary notifies user at sync points
   - Shows progress (2 of 3 complete)
   - Indicates wait time or timeout action

**Testing:**
- Run through full user flow
- Copy-paste handoff package
- Verify user-facing messages clear

**Exit Criteria:**
- User experience smooth
- Handoff package works reliably
- User communication clear

---

### Phase 5: Safety & Recovery (1-2 hours)

**Deliverables:**

1. **Stale Agent Detection**
   - Guide: `parallel_work/stale_agent_protocol.md`
   - 30 min warning, 60 min failure
   - Primary monitors secondary agents

2. **Recovery Procedures**
   - Guide: `parallel_work/recovery_procedures.md`
   - Checkpoint-based resume
   - Reassignment to new agent
   - Restart feature from S2

3. **Timeout-Based Sync**
   - Guide: `parallel_work/sync_timeout_protocol.md`
   - 2-hour timeout from first completion
   - Defer slow features to Wave 2

4. **Error Handling**
   - Lock file expiry (automatic)
   - Communication channel errors
   - Checkpoint file corruption

**Testing:**
- Simulate agent crash (checkpoint recovery)
- Simulate slow agent (timeout sync)
- Simulate lock expiry

**Exit Criteria:**
- All failure modes handled
- Recovery procedures documented
- Timeout mechanisms tested

---

## Guide Changes Required

### New Guides (8 files)

| File | Purpose | Size | Priority |
|------|---------|------|----------|
| `parallel_work/s2_parallel_protocol.md` | Complete S2 parallel protocol | ~2000 lines | P0 |
| `parallel_work/s2_primary_agent_guide.md` | Primary agent responsibilities | ~800 lines | P0 |
| `parallel_work/s2_secondary_agent_guide.md` | Secondary agent workflow | ~600 lines | P0 |
| `parallel_work/lock_file_protocol.md` | Lock acquisition/release | ~400 lines | P0 |
| `parallel_work/communication_protocol.md` | Agent messaging | ~500 lines | P0 |
| `parallel_work/checkpoint_protocol.md` | Checkpoint system | ~500 lines | P0 |
| `parallel_work/stale_agent_protocol.md` | Stale detection/recovery | ~400 lines | P1 |
| `parallel_work/sync_timeout_protocol.md` | Sync timeout handling | ~300 lines | P1 |

**Total New Content:** ~5,500 lines

---

### Updated Guides (6 files)

| File | Changes | Priority |
|------|---------|----------|
| `stages/s1/s1_epic_planning.md` | Add: Dependency analysis, parallel work offering | P0 |
| `stages/s2/s2_feature_deep_dive.md` | Add: Agent role routing | P0 |
| `stages/s2/s2_p1_research.md` | Add: Checkpoint updates, communication checks | P0 |
| `stages/s2/s2_p2_specification.md` | Add: Checkpoint updates, communication checks | P0 |
| `stages/s2/s2_p3_refinement.md` | Add: Completion signal, sync preparation | P0 |
| `stages/s3/s3_cross_feature_sanity_check.md` | Add: Sync status verification | P0 |

**Estimated Changes:** ~1,500 lines (updates to existing)

---

### Template Updates (3 files)

| File | Changes | Priority |
|------|---------|----------|
| `templates/epic_readme_template.md` | Add: Sectioning, Agent Assignment, Sync Status | P0 |
| `templates/feature_readme_template.md` | No changes needed | - |
| `templates/handoff_package_template.md` | New template for secondary agent setup | P0 |

**Estimated Changes:** ~500 lines

---

### Supporting Files (3 files)

| File | Changes | Priority |
|------|---------|----------|
| `EPIC_WORKFLOW_USAGE.md` | Add: S2 parallel work section (~1000 lines) | P0 |
| `CLAUDE.md` | Add: Parallel work quick reference (~300 lines) | P0 |
| `prompts/parallel_work_prompts.md` | New: Phase transition prompts for parallel work | P0 |

**Estimated Changes:** ~1,300 lines

---

**TOTAL GUIDE EFFORT:**
- New guides: ~5,500 lines
- Updated guides: ~1,500 lines
- Templates: ~500 lines
- Supporting: ~1,300 lines
- **TOTAL: ~8,800 lines**

**Estimated Time:** 6-8 hours (at ~1,000-1,500 lines/hour)

---

## Coordination Mechanisms

### Lock File System

**Purpose:** Prevent race conditions when updating shared files

**Implementation:**
```
.epic_locks/
  ├── epic_readme.lock
  └── epic_smoke_test_plan.lock
```

**Lock File Format:**
```json
{
  "holder": "Agent-Primary",
  "holder_id": "abc123",
  "acquired_at": "2026-01-15T14:30:00Z",
  "operation": "Updating S2 progress",
  "expires_at": "2026-01-15T14:35:00Z",
  "auto_release": true
}
```

**Protocol:**
1. Agent attempts to acquire lock
2. If lock exists and not expired → wait 5 seconds, retry
3. If lock expired → delete lock, acquire new
4. If lock available → create lock file
5. Perform operation (e.g., update EPIC_README.md)
6. Release lock (delete lock file)

**Timeout:** 5 minutes per operation (prevents infinite locks)

**Lock Timeout Behavior:**
- **Purpose:** Timeout prevents infinite locks if agent crashes mid-operation
- **Important:** Timeout does NOT interrupt ongoing operations
- **Mechanism:** If agent is actively working, operation completes normally
- **Auto-release:** Timeout only allows new lock acquisition if original holder vanished
- **Best Practice:** Set timeout to 2-3x typical operation duration (generous buffer)
- **Example:** EPIC_README.md update typically takes 30 seconds → 5 minute timeout provides 10x buffer

**Used For:**
- EPIC_README.md updates
- epic_smoke_test_plan.md updates (S4 only in this plan)

---

### Communication Channels

**Purpose:** Agent-to-agent messaging without EPIC_README.md conflicts

**Structure:**
```
agent_comms/
  ├── primary_to_secondary_a.md    # Inbox for Secondary-A
  ├── secondary_a_to_primary.md    # Outbox from Secondary-A
  ├── primary_to_secondary_b.md    # Inbox for Secondary-B
  └── secondary_b_to_primary.md    # Outbox from Secondary-B
```

**Message Format:**
```markdown
# Messages: Primary → Secondary-A

## Message 3 (2026-01-15 14:35) ✅ READ
**Subject:** S3 Complete - Proceed to Implementation
**Action:** I've completed S3 (Cross-Feature Sanity Check)
**Details:** No conflicts found with your feature
**Next:** Implementation remains sequential in this plan - I'll start Feature 01
**Acknowledge:** Reply when you understand

## Message 2 (2026-01-15 12:00) ✅ READ
**Subject:** User answered your question
**Action:** Check feature_02/checklist.md - Question 5 answered
**Next:** Complete S2.P3, then signal completion
**Acknowledge:** Reply when S2.P3 complete
```

**Protocol:**
1. Agent checks inbox before every action
2. Agent marks messages as READ with ✅
3. Agent replies in corresponding outbox
4. Messages archived after sync point

**Benefits:**
- Zero conflicts (separate files)
- Clear message direction
- Easy to track read status

---

### Checkpoint System

**Purpose:** Enable recovery from agent failures

**Structure:**
```
agent_checkpoints/
  ├── primary.json
  ├── secondary_a.json
  └── secondary_b.json
```

**Checkpoint Format:**
```json
{
  "agent_id": "Agent-Primary",
  "agent_type": "primary",
  "session_id": "abc123",
  "feature": "feature_01_player_json",
  "stage": "S2.P2",
  "phase": "Specification",
  "last_checkpoint": "2026-01-15T14:30:00Z",
  "next_checkpoint_expected": "2026-01-15T14:45:00Z",
  "status": "IN_PROGRESS",
  "can_resume": true,
  "blockers": [],
  "files_modified": [
    "feature_01_player_json/spec.md",
    "feature_01_player_json/checklist.md"
  ],
  "recovery_instructions": "Resume from S2.P2 Specification Phase, spec.md partially complete"
}
```

**Update Frequency:**
- After completing each S2 phase (P1, P2, P3)
- Every 15 minutes (heartbeat)
- Before/after sync points

**Update Trigger Mechanism:**
- **Agent-initiated (manual):** Checkpoints are updated by agent action, not automated
- **Integration in guides:** Each guide includes explicit "Update checkpoint" steps
- **Heartbeat updates:** Agent sets 15-minute timer, manually updates checkpoint
- **Phase completion:** Guides include checkpoint update as final step before transitioning
- **Why manual:** Ensures agent is actively working and aware of current state

**Stale Detection:**
- **30 minutes:** Warning (Primary sends message)
- **60 minutes:** Failure (Primary takes action)

**Recovery Options:**
1. Primary resumes work (reads checkpoint, continues)
2. New secondary agent takes over (reads checkpoint)
3. Restart feature from S2.P1 (if minimal work done)

---

### STATUS Files

**Purpose:** Quick status checks without reading EPIC_README.md

**Location:** `feature_XX_name/STATUS`

**Format (plain text):**
```
STAGE: S2.P2
PHASE: Specification
AGENT: Agent-Primary
AGENT_ID: abc123
UPDATED: 2026-01-15T14:30:00Z
STATUS: IN_PROGRESS
BLOCKERS: none
NEXT_ACTION: Complete spec.md requirements section
READY_FOR_SYNC: false
ESTIMATED_COMPLETION: 2026-01-15T15:00:00Z
```

**Benefits:**
- One file per feature (no conflicts)
- Easy to parse (simple key-value)
- Git tracks changes automatically
- Primary can scan all STATUS files at once

**Updated:**
- After completing each S2 phase
- At checkpoints (every 15 min)
- When blockers occur
- When ready for sync

---

### Sectioned EPIC_README.md

**Purpose:** Prevent merge conflicts when multiple agents update

**Structure:**
```markdown
# Epic KAI-6: NFL Team Penalty Scoring

## Quick Reference Card
[Epic-level content - Primary owns]

## Agent Assignment Table

| Feature | Agent | Status | Started | Last Update |
|---------|-------|--------|---------|-------------|
| feature_01 | Primary | S2.P2 | 10:00 | 14:30 |
| feature_02 | Secondary-A | S2.P1 | 10:30 | 14:25 |
| feature_03 | Secondary-B | S2.P1 | 11:00 | 14:20 |

<!-- BEGIN PRIMARY PROGRESS -->
## Feature 01 Progress (Primary)

**Last Updated:** 2026-01-15 14:30
**Current Stage:** S2.P2 (Specification Phase)
**Current Step:** Writing spec.md requirements
**Blockers:** None
**Next Action:** Complete requirements section, move to checklist

**S2 Progress:**
- ✅ S2.P1 (Research Phase) - Complete
- 🔄 S2.P2 (Specification Phase) - In Progress
- ⏳ S2.P3 (Refinement Phase) - Not Started
<!-- END PRIMARY PROGRESS -->

<!-- BEGIN SECONDARY-A PROGRESS -->
## Feature 02 Progress (Secondary-A)

**Last Updated:** 2026-01-15 14:25
**Current Stage:** S2.P1 (Research Phase)
**Current Step:** Targeted research
**Blockers:** None
**Next Action:** Complete research, move to S2.P2

**S2 Progress:**
- 🔄 S2.P1 (Research Phase) - In Progress
- ⏳ S2.P2 (Specification Phase) - Not Started
- ⏳ S2.P3 (Refinement Phase) - Not Started
<!-- END SECONDARY-A PROGRESS -->

<!-- BEGIN SECONDARY-B PROGRESS -->
## Feature 03 Progress (Secondary-B)

**Last Updated:** 2026-01-15 14:20
**Current Stage:** S2.P1 (Research Phase)
**Current Step:** Epic intent extraction
**Blockers:** None
**Next Action:** Begin targeted research

**S2 Progress:**
- 🔄 S2.P1 (Research Phase) - In Progress (early)
- ⏳ S2.P2 (Specification Phase) - Not Started
- ⏳ S2.P3 (Refinement Phase) - Not Started
<!-- END SECONDARY-B PROGRESS -->

## Sync Status

**Current Sync Point:** After S2 → Before S3
**Status:** WAITING (0 of 3 features complete)
**Timeout:** 2 hours from first completion
**Next Action:** All agents complete S2.P3, then Primary runs S3
```

**Rules:**
- Agent ONLY edits content between their BEGIN/END markers
- Primary can edit any section
- Agent Assignment and Sync Status: Primary only

**Benefits:**
- Minimal merge conflicts (agents own sections)
- Clear ownership
- Git handles cleanly

---

### Escalation Protocol

**Purpose:** Define when and how Secondary agents escalate to Primary

**When Secondary Escalates to Primary:**
- User questions that require domain knowledge or project context
- Specification ambiguities that can't be resolved from codebase
- Integration concerns with other features
- Blockers that prevent progress >30 minutes
- Cross-feature coordination needs

**Escalation Process:**
1. Secondary documents issue in feature's checklist.md or communication channel
2. Secondary updates STATUS file: `BLOCKERS: <description>`
3. Secondary sends message via communication channel with:
   - Clear description of blocker
   - What was already tried
   - Specific help needed
4. Secondary signals "BLOCKED - Escalation needed" in EPIC_README.md section
5. Primary responds within 15 minutes (or 1 hour if in deep work on own feature)
6. Primary either:
   - Provides guidance directly via communication channel
   - Handles user interaction if user input needed
   - Updates affected files if changes required
7. Secondary acknowledges resolution and resumes work

**What Secondary Can Decide Alone:**
- Implementation approach choices (within spec boundaries)
- Code structure and organization decisions
- Test design and coverage approaches
- Minor clarifications obtainable from codebase reading
- Local refactoring within feature scope
- Documentation formatting and style

**What Requires Primary Escalation:**
- Spec changes or requirement additions
- User questions about business logic or priorities
- Cross-feature coordination or integration points
- Changes to epic-level files (epic_smoke_test_plan.md)
- Dependency conflicts or timing issues
- Major technical decisions affecting other features

**Escalation SLA:**
- Primary checks communication channels every 15 minutes
- Primary responds to escalations within 15 minutes during active work
- Primary responds within 1 hour maximum if in deep work session
- If Primary unavailable >1 hour, secondary updates checkpoint with blocker state

**Example Escalation Message:**
```markdown
# Messages: Secondary-A → Primary

## Message 2 (2026-01-15 11:30)
**Subject:** ESCALATION - Spec Ambiguity in Feature 02
**Blocker:** Unable to proceed with S2.P2
**Issue:** Spec says "integrate with team rankings" but unclear if this means:
  A) Use existing team_rankings.csv file
  B) Fetch fresh data from NFL API
  C) Both (use CSV as cache, update from API)
**Attempted:**
  - Read team_rankings.csv structure
  - Checked nfl-scores-fetcher/ code
  - Reviewed Feature 01 spec for clues
**Stuck For:** 25 minutes
**Need:** User clarification on data source approach
**Blocked Since:** 11:05
**Urgency:** HIGH (blocking S2.P2 requirements section)
```

---

### Primary Agent Workload Management

**Purpose:** Guide Primary's balance between coordination duties and Feature 01 implementation

**Primary's Dual Role:**
1. **Coordinator:** Merge reviews, messaging, sync management, escalation handling
2. **Feature Owner:** Implements Feature 01 (S2 for their assigned feature)

**Time Allocation Strategy:**

**Priority Order:**
1. **Escalations (Highest Priority):** Respond within 15 minutes
2. **Sync Management:** Monitor STATUS files, update EPIC_README.md sync status
3. **Communication:** Check inbox, respond to messages
4. **Feature 01 Work:** S2 work during idle coordination time

**Feature Assignment Best Practice:**
- Primary should own the **simplest/smallest feature** as Feature 01
- This minimizes Primary's implementation workload
- Frees more time for coordination responsibilities
- Reduces bottleneck risk

**Workload Balance Approach:**
1. **Work in time blocks:**
   - 15-minute coordination checks (STATUS files, messages, escalations)
   - 45-minute deep work blocks on Feature 01
   - Interrupt deep work only for urgent escalations

2. **During S2 parallel work:**
   - Start Feature 01 S2 work immediately (parallel with secondaries)
   - Check coordination every 15 minutes
   - Respond to escalations immediately
   - Complete Feature 01 S2 during the parallel window

3. **If coordination demands spike:**
   - Pause Feature 01 work temporarily
   - Focus on unblocking secondary agents
   - Resume Feature 01 after coordination settles

4. **At sync points:**
   - Stop Feature 01 work
   - Focus entirely on coordination (checking all complete, updating sync status)
   - Run S3 alone (no parallel work)

**Example Timeline (3-feature epic, Wave 1):**
```
10:00-10:15: S1 complete, generate handoff packages
10:15-10:30: All agents start S2 (Primary on Feature 01)
10:30-10:35: Secondary-A escalates → Primary responds (5 min)
10:35-11:30: Primary works on Feature 01 S2.P1 (55 min deep work)
11:30-11:35: Primary checks coordination (STATUS files, messages)
11:35-12:30: Primary works on Feature 01 S2.P2 (55 min deep work)
12:30-12:35: Primary checks coordination
12:35-13:30: Primary works on Feature 01 S2.P3 (55 min deep work)
13:30-13:35: Primary completes Feature 01, signals completion
13:35-14:00: Wait for secondary agents (monitor STATUS files)
14:00-14:30: Secondary-A and Secondary-B complete S2
14:30-15:30: Primary runs S3 alone (Cross-Feature Sanity Check)
15:30-16:00: Primary runs S4 (Epic Testing Strategy)
```

**Key Principles:**
- **Coordination always takes priority** over own feature work
- **Never let secondary agents block** for >15 minutes
- **Choose simplest feature** to minimize own implementation time
- **Use waiting time productively** (during sync, work on coordination tasks)
- **Set clear expectations** with secondary agents on response times

**Coordination Overhead Target:**
- <10% of total parallel time
- For 3-feature epic: ~15 minutes coordination per 2.5 hours = 10%
- Includes: Lock operations, message responses, STATUS checks, sync management

---

## User Experience Flow

### Step 1: Primary Offers Parallel Work (After S1)

**Primary Agent says:**
```markdown
✅ S1 (Epic Planning) complete!

I've identified 3 features for this epic:
- feature_01: Player JSON integration (2 hours S2)
- feature_02: Team penalty scoring (2 hours S2)
- feature_03: Scoring algorithm update (2 hours S2)

🚀 PARALLEL WORK OPPORTUNITY

I can enable parallel work for S2 (Feature Deep Dives), reducing planning time:

**Sequential approach:**
- Feature 1 S2: 2 hours
- Feature 2 S2: 2 hours
- Feature 3 S2: 2 hours
Total: 6 hours

**Parallel approach:**
- All 3 features S2: 2 hours (simultaneously)
Total: 2 hours

TIME SAVINGS: 4 hours (67% reduction in S2 time)

**DEPENDENCIES:**
- feature_02 depends on feature_01 (for implementation only)
- All features can be researched/specified in parallel

**COORDINATION:**
- You'll need to open 2 additional Claude Code sessions
- I'll coordinate all agents via EPIC_README.md
- Implementation (S5-S8) remains sequential in this plan

Would you like to:
1. ✅ Enable parallel work for S2 (I'll provide setup instructions)
2. ❌ Continue sequential (I'll do all features one by one)
3. ❓ Discuss parallelization approach
```

**User selects Option 1**

---

### Step 2: Primary Generates Handoff Packages

**Primary Agent says:**
```markdown
Great! I'll set up parallel work for S2.

📋 SETUP INSTRUCTIONS

You'll need to open 2 new Claude Code sessions (one for each secondary agent).

**For each new session:**
1. Open a new terminal/window
2. Navigate to the project: cd /path/to/project
3. Start Claude Code in the new window
4. Copy-paste the handoff package below

---

🚀 SECONDARY AGENT A - HANDOFF PACKAGE

Copy the entire block below and paste into NEW Claude Code session #1:

═══════════════════════════════════════════════════════════
I'm joining as a secondary agent for epic KAI-6-nfl_team_penalty.

**Configuration:**
Epic Path: C:/Users/kmgam/code/FantasyFootballHelperScripts/feature-updates/KAI-6-nfl_team_penalty
My Assignment: feature_02_team_penalty
Primary Agent ID: Agent-abc123
My Agent ID: Secondary-A
Starting Stage: S2.P1 (Feature Deep Dive - Research Phase)

**Coordination:**
- Inbox: agent_comms/primary_to_secondary_a.md (check before every action)
- Outbox: agent_comms/secondary_a_to_primary.md (send updates)
- Checkpoint: agent_checkpoints/secondary_a.json (update every 15 min)
- STATUS: feature_02_team_penalty/STATUS (update at phase transitions)

**Sync Points:**
- After S2.P3 complete: Signal completion, WAIT for Primary to run S3
- After Primary completes S3: I'll proceed to implementation (sequential)

Begin S2.P1 now.
═══════════════════════════════════════════════════════════

---

🚀 SECONDARY AGENT B - HANDOFF PACKAGE

Copy the entire block below and paste into NEW Claude Code session #2:

═══════════════════════════════════════════════════════════
I'm joining as a secondary agent for epic KAI-6-nfl_team_penalty.

**Configuration:**
Epic Path: C:/Users/kmgam/code/FantasyFootballHelperScripts/feature-updates/KAI-6-nfl_team_penalty
My Assignment: feature_03_scoring_update
Primary Agent ID: Agent-abc123
My Agent ID: Secondary-B
Starting Stage: S2.P1 (Feature Deep Dive - Research Phase)

**Coordination:**
- Inbox: agent_comms/primary_to_secondary_b.md (check before every action)
- Outbox: agent_comms/secondary_b_to_primary.md (send updates)
- Checkpoint: agent_checkpoints/secondary_b.json (update every 15 min)
- STATUS: feature_03_scoring_update/STATUS (update at phase transitions)

**Sync Points:**
- After S2.P3 complete: Signal completion, WAIT for Primary to run S3
- After Primary completes S3: I'll proceed to implementation (sequential)

Begin S2.P1 now.
═══════════════════════════════════════════════════════════

---

**After pasting both packages:**
- Secondary agents will self-configure and begin S2
- I'll monitor their progress via STATUS files and checkpoints
- All agents will work on S2 simultaneously
- When all complete S2, I'll run S3

Ready to start? Please paste the handoff packages in the new sessions.
```

**User copies packages and pastes into new sessions**

---

### Step 3: Secondary Agents Start Work

**Secondary Agent A (in new session):**
```markdown
✅ Configuration verified
   Epic: KAI-6-nfl_team_penalty
   Feature: feature_02_team_penalty
   Primary: Agent-abc123
   My ID: Secondary-A

✅ Coordination channels confirmed
   Inbox: agent_comms/primary_to_secondary_a.md (checking...)
   Outbox: agent_comms/secondary_a_to_primary.md (creating...)

✅ Checkpoint system initialized
   File: agent_checkpoints/secondary_a.json (creating...)
   Update frequency: Every 15 minutes

✅ STATUS file initialized
   File: feature_02_team_penalty/STATUS (creating...)

📨 Checking inbox for messages from Primary...
   No messages yet.

✅ Updating EPIC_README.md with my progress...
   [Acquires lock]
   [Updates SECONDARY-A PROGRESS section]
   [Releases lock]

🚀 Starting S2.P1 (Feature Deep Dive - Research Phase)

Reading guide: stages/s2/s2_p1_research.md...

The guide requires:
- Phase 0: Epic Intent Extraction
- Phase 1: Targeted Research
- Phase 1.5: Research Completeness Audit (MANDATORY GATE)

Prerequisites verified:
✅ feature_02_team_penalty folder exists
✅ spec.md template created in S1
✅ checklist.md template created in S1

I'll now proceed with Phase 0: Epic Intent Extraction for feature_02...
```

**Secondary Agent B starts similarly**

---

### Step 4: Parallel Work in Progress

**Primary monitors via STATUS files:**

```bash
# Primary checks all STATUS files
cat feature_01_player_json/STATUS
cat feature_02_team_penalty/STATUS
cat feature_03_scoring_update/STATUS

# Primary sees:
# Feature 01: S2.P2 (Primary working)
# Feature 02: S2.P1 (Secondary-A working)
# Feature 03: S2.P1 (Secondary-B working)
```

**All agents work simultaneously:**
- Primary completes S2 for Feature 01
- Secondary-A completes S2 for Feature 02
- Secondary-B completes S2 for Feature 03

**Each agent:**
- Updates their section in EPIC_README.md (using locks)
- Updates their STATUS file
- Updates their checkpoint file every 15 min
- Checks inbox for messages

---

### Step 5: Sync Point - All Features Complete S2

**Feature 01 completes first (14:00)**

Primary updates EPIC_README.md:
```markdown
## Sync Status

**Current Sync Point:** After S2 → Before S3
**Status:** WAITING (1 of 3 complete)
**Started Waiting:** 2026-01-15 14:00
**Timeout:** 2026-01-15 16:00 (2 hours)
**Next Action:** Waiting for features 02 and 03 to complete S2.P3

| Feature | Agent | S2.P3 Complete | Timestamp | Wave |
|---------|-------|----------------|-----------|------|
| feature_01 | Primary | ✅ YES | 14:00 | Wave 1 |
| feature_02 | Secondary-A | ⏳ IN PROGRESS | - | Wave 1 |
| feature_03 | Secondary-B | ⏳ IN PROGRESS | - | Wave 1 |
```

**Feature 02 completes (14:25)**

Secondary-A signals completion:
```markdown
# Messages: Secondary-A → Primary

## Message 1 (2026-01-15 14:25)
**Subject:** S2.P3 Complete for Feature 02
**Status:** feature_02_team_penalty S2 complete
**Files Ready:**
- spec.md (complete, all requirements documented)
- checklist.md (all items resolved)
- README.md (updated with S2 completion)

**Blockers:** None
**Ready for S3:** Yes
**Awaiting:** Your S3 Cross-Feature Sanity Check
```

Primary updates sync status:
```markdown
| Feature | Agent | S2.P3 Complete | Timestamp | Wave |
|---------|-------|----------------|-----------|------|
| feature_01 | Primary | ✅ YES | 14:00 | Wave 1 |
| feature_02 | Secondary-A | ✅ YES | 14:25 | Wave 1 |
| feature_03 | Secondary-B | ⏳ IN PROGRESS | - | Wave 1 |
```

**Feature 03 completes (14:30)**

Secondary-B signals completion similarly.

Primary updates sync status:
```markdown
| Feature | Agent | S2.P3 Complete | Timestamp | Wave |
|---------|-------|----------------|-----------|------|
| feature_01 | Primary | ✅ YES | 14:00 | Wave 1 |
| feature_02 | Secondary-A | ✅ YES | 14:25 | Wave 1 |
| feature_03 | Secondary-B | ✅ YES | 14:30 | Wave 1 |

**All features complete! Proceeding to S3.**
```

---

### Step 6: Primary Runs S3 Alone

**Primary notifies user:**
```markdown
✅ All 3 features completed S2!

**Completion Summary:**
- Feature 01: Completed at 14:00 (Primary)
- Feature 02: Completed at 14:25 (Secondary-A)
- Feature 03: Completed at 14:30 (Secondary-B)

**Total S2 Time:** 2.5 hours (from 10:00 to 14:30, max of parallel work)
**Time Saved:** 3.5 hours (vs 6 hours sequential)

🔄 Now running S3 (Cross-Feature Sanity Check)

I'll review all 3 specs for conflicts, overlaps, and gaps...

Reading guide: stages/s3/s3_cross_feature_sanity_check.md...
```

**Primary notifies secondary agents:**

To Secondary-A:
```markdown
## Message 2 (2026-01-15 14:35)
**Subject:** S2 Sync Complete - I'm Running S3
**Status:** All features completed S2
**Next:** I'm running S3 (Cross-Feature Sanity Check) alone
**Your Action:** WAIT - No action needed from you right now
**ETA:** S3 will take ~1 hour, then I'll proceed to S4
**Note:** Implementation (S5-S8) will be sequential in this plan
```

To Secondary-B: Similar message

---

### Step 7: After S3/S4 - Return to Sequential

**Primary completes S3 and S4:**
```markdown
✅ S3 (Cross-Feature Sanity Check) complete - No conflicts found
✅ S4 (Epic Testing Strategy) complete - Test plan updated

📢 Notification to Secondary Agents

S3 and S4 are complete. No issues found with any feature specs.

**Next Steps:**
- Implementation (S5-S8) will be SEQUENTIAL in this plan
- I (Primary) will implement Feature 01 first
- After Feature 01 complete → I'll implement Feature 02
- After Feature 02 complete → I'll implement Feature 03

**Your Sessions:**
- You can close your secondary agent sessions now
- Or keep them open (they'll remain idle during S5-S8)
- I'll handle all implementation work

Thank you for the parallel work during S2! We saved 3.5 hours.

**S2 Parallel Work Results:**
- Time: 2.5 hours (vs 6 hours sequential)
- Savings: 3.5 hours (58% reduction)
- Issues: None
- Coordination overhead: ~15 minutes (10%)

I'll now proceed with S5 (Implementation Planning) for Feature 01...
```

**Epic continues sequentially from this point**

---

## Risk Analysis

### Risk 1: EPIC_README.md Conflicts
- **Likelihood:** MEDIUM
- **Impact:** MEDIUM (slows coordination)
- **Mitigation:**
  - ✅ Sectioned EPIC_README.md (agents own sections)
  - ✅ Lock files (atomic operations)
  - ✅ STATUS files reduce EPIC_README.md updates
- **Residual Risk:** **LOW**

### Risk 2: Communication Channel Failures
- **Likelihood:** LOW
- **Impact:** MEDIUM (agents miss messages)
- **Mitigation:**
  - ✅ Simple file-based channels (robust)
  - ✅ Agents check inbox before every action
  - ✅ Primary monitors checkpoint heartbeats
- **Residual Risk:** **VERY LOW**

### Risk 3: Secondary Agent Session Failure
- **Likelihood:** MEDIUM
- **Impact:** MEDIUM (blocks S2 progress)
- **Mitigation:**
  - ✅ Checkpoint files preserve work
  - ✅ Stale detection (30/60 min)
  - ✅ Primary can resume or reassign
  - ✅ Work on disk, not lost
- **Residual Risk:** **LOW**

### Risk 4: Sync Point Timeout
- **Likelihood:** LOW
- **Impact:** LOW (can defer feature)
- **Mitigation:**
  - ✅ 2-hour timeout (generous)
  - ✅ Defer slow features to Wave 2
  - ✅ Primary can proceed with partial epic
- **Residual Risk:** **VERY LOW**

### Risk 5: User Confusion
- **Likelihood:** MEDIUM
- **Impact:** MEDIUM (poor UX)
- **Mitigation:**
  - ✅ Handoff package (copy-paste)
  - ✅ Clear instructions
  - ⚠️ Still requires opening multiple sessions
- **Residual Risk:** **MEDIUM** (acceptable)

### Risk 6: Quality Divergence
- **Likelihood:** LOW (for S2)
- **Impact:** LOW (caught in S3)
- **Mitigation:**
  - ✅ Same guides for all agents
  - ✅ S3 validates all specs (Primary reviews)
  - ✅ Documentation only (no code quality issues)
- **Residual Risk:** **VERY LOW**

### Risk 7: Coordination Overhead
- **Likelihood:** MEDIUM
- **Impact:** LOW (reduces time savings)
- **Mitigation:**
  - ✅ Automated checks (lock files, STATUS)
  - ✅ Clear protocols
  - ✅ Target: <10% overhead
- **Residual Risk:** **LOW**
- **Measured:** 15 min overhead / 150 min saved = 10% (at target)

### Overall Risk Profile: **LOW**

S2 parallelization is low-risk because:
- Documentation only (no code conflicts)
- Shared files are sectioned
- S3 provides validation checkpoint
- Checkpoint system prevents lost work

---

## Success Metrics

### Time Savings Metrics

**Target:** 40-60% reduction in S2 time

**Measurement:**
```markdown
## S2 Parallel Work Results

**Epic:** KAI-6-nfl_team_penalty
**Features:** 3

**Sequential Baseline (calculated):**
- Feature 01 S2: 2 hours
- Feature 02 S2: 2 hours
- Feature 03 S2: 2 hours
Total: 6 hours

**Parallel Actual:**
- Start: 10:00
- Feature 01 complete: 14:00 (2 hours)
- Feature 02 complete: 14:25 (2.42 hours)
- Feature 03 complete: 14:30 (2.5 hours)
Max: 2.5 hours

**Time Saved:** 3.5 hours (58% reduction)

**Coordination Overhead:**
- Lock operations: ~5 minutes
- Communication: ~5 minutes
- Sync coordination: ~5 minutes
Total: ~15 minutes (10% of parallel time)

**Net Savings:** 3.35 hours (56% net reduction)
```

### Quality Metrics

**Target:** No increase in S3 issues found

**Measurement:**
```markdown
## Quality Comparison

**Baseline (Sequential S2 - last 3 epics):**
- S3 issues found: 2-3 per epic (conflicts, overlaps)
- Spec completeness: 95%
- Checklist resolution: 100%

**Parallel S2 (this epic):**
- S3 issues found: 2 (within normal range)
- Spec completeness: 95%
- Checklist resolution: 100%

**Conclusion:** No quality degradation
```

### Coordination Efficiency

**Target:** <10% coordination overhead

**Measurement:**
```markdown
## Coordination Breakdown

**Lock Operations:**
- EPIC_README.md updates: 15 lock cycles
- Average lock time: 10 seconds
- Total: 2.5 minutes

**Communication:**
- Messages sent: 8
- Average time per message: 30 seconds
- Total: 4 minutes

**Checkpoint Updates:**
- Updates: 18 (every 15 min + phase transitions)
- Average time: 15 seconds
- Total: 4.5 minutes

**Sync Coordination:**
- STATUS checks: 10
- Sync status updates: 3
- Total: 3 minutes

**Total Coordination Time:** 14 minutes
**Total Parallel Time:** 150 minutes (2.5 hours)
**Overhead:** 9.3% ✅ (below 10% target)
```

### User Satisfaction

**Target:** Users opt-in when offered

**Measurement:**
- Number of times parallel work offered: X
- Number of times user accepted: Y
- Opt-in rate: Y/X (target: >50%)
- User feedback: Survey after epic completion

---

## Pilot Plan

### Pilot Scope

**Epic Selection Criteria:**
- 2-3 features (not too complex)
- Features have minimal dependencies
- User available for ~4 hours (parallel S2 + sequential S5-S8)

**Recommended Pilot Epic:**
- Next small enhancement epic
- 2 features (simpler than 3)
- Low-risk functionality changes

### Pilot Phases

**Phase 1: Setup (30 minutes)**
1. Create pilot epic folder structure
2. Initialize all coordination infrastructure:
   - .epic_locks/
   - agent_comms/
   - agent_checkpoints/
3. Test lock acquisition/release manually
4. Test communication channel read/write

**Phase 2: S1 (1.5 hours)**
1. Primary completes S1 (Epic Planning)
2. Primary identifies 2 features
3. Primary analyzes dependencies
4. Primary generates handoff package
5. User reviews handoff package format

**Phase 3: S2 Parallel (2 hours)**
1. User opens new session, pastes handoff package
2. Secondary agent self-configures
3. Both agents work on S2 simultaneously:
   - Primary: Feature 01 S2
   - Secondary: Feature 02 S2
4. Monitor coordination:
   - Lock file usage
   - Communication messages
   - Checkpoint updates
   - STATUS file updates
5. Both complete S2.P3
6. Sync point triggers

**Phase 4: S3/S4 (1 hour)**
1. Primary runs S3 alone
2. Secondary agent waits (idle)
3. Primary runs S4
4. Primary notifies secondary agent of completion

**Phase 5: Retrospective (30 minutes)**
1. Measure time savings
2. Measure coordination overhead
3. Identify issues/pain points
4. Document lessons learned
5. Update guides based on findings

### Pilot Success Criteria

**Must Pass:**
- [ ] Time savings ≥40% for S2
- [ ] Coordination overhead ≤15%
- [ ] Zero data loss (checkpoints work)
- [ ] Zero merge conflicts in EPIC_README.md
- [ ] All agents complete S2 successfully

**Should Pass:**
- [ ] User finds handoff package easy to use
- [ ] Secondary agent setup takes <5 minutes
- [ ] Communication channels work reliably
- [ ] Stale detection works (test by killing agent)

**Nice to Have:**
- [ ] User opts to use parallel work again
- [ ] Coordination overhead <10%
- [ ] Time savings >50%

### Pilot Contingencies

**If coordination overhead >15%:**
- Analyze where time is spent
- Optimize lock operations
- Reduce STATUS file update frequency
- Simplify communication protocol

**If handoff package is confusing:**
- Simplify package format
- Add more explicit instructions
- Create visual guide for user

**If EPIC_README.md conflicts occur:**
- Verify sectioning works
- Check lock file implementation
- Increase lock timeout if needed

**If agent failure recovery fails:**
- Test checkpoint file format
- Verify recovery procedure
- Document edge cases

---

## Rollout Strategy

### Stage 1: Internal Validation (1 week)

**Actions:**
1. Complete pilot (as described above)
2. Fix any issues identified
3. Update guides based on lessons
4. Run second pilot with 3-feature epic

**Exit Criteria:**
- 2 successful pilots
- All must-pass criteria met
- User comfortable with workflow
- Guides accurate and complete

---

### Stage 2: Limited Rollout (2 weeks)

**Actions:**
1. Offer parallel work for all new epics with 3+ features
2. Collect metrics for each epic:
   - Time savings
   - Coordination overhead
   - Quality metrics (S3 issues)
   - User satisfaction
3. Monitor for issues
4. Iterate on guides

**Exit Criteria:**
- 5+ successful parallel epics
- Consistent time savings (40-60%)
- Low coordination overhead (<10%)
- No quality degradation
- Positive user feedback

---

### Stage 3: Full Rollout (ongoing)

**Actions:**
1. Make parallel work default for epics with 3+ features
2. Offer for epics with 2 features (optional)
3. Continue collecting metrics
4. Optimize based on data

**Monitoring:**
- Track success rate (% of parallel epics completed)
- Average time savings across all epics
- Average coordination overhead
- Common failure modes
- User opt-in rate

---

### Stage 4: Continuous Improvement (ongoing)

**Actions:**
1. Monthly review of parallel work metrics
2. Identify bottlenecks
3. Update guides based on lessons learned
4. Consider advanced features:
   - Auto-parallelization suggestions
   - Dynamic agent assignment
   - Parallel S5-S8 (future)

---

## Appendix A: File Structure Reference

```
feature-updates/KAI-N-epic_name/
├── EPIC_README.md                 # Sectioned for parallel work
├── epic_smoke_test_plan.md
├── epic_lessons_learned.md
│
├── .epic_locks/                   # NEW - Lock files
│   ├── epic_readme.lock
│   └── epic_smoke_test_plan.lock
│
├── agent_comms/                   # NEW - Communication channels
│   ├── primary_to_secondary_a.md
│   ├── secondary_a_to_primary.md
│   ├── primary_to_secondary_b.md
│   └── secondary_b_to_primary.md
│
├── agent_checkpoints/             # NEW - Checkpoint files
│   ├── primary.json
│   ├── secondary_a.json
│   └── secondary_b.json
│
├── feature_01_player_json/
│   ├── STATUS                     # NEW - Quick status
│   ├── README.md
│   ├── spec.md
│   ├── checklist.md
│   ├── implementation_plan.md
│   └── lessons_learned.md
│
├── feature_02_team_penalty/
│   ├── STATUS                     # NEW
│   └── [same structure as feature_01]
│
└── feature_03_scoring_update/
    ├── STATUS                     # NEW
    └── [same structure as feature_01]
```

---

## Appendix B: Implementation Checklist

### Phase 1: Core Infrastructure
- [ ] Create lock file protocol guide
- [ ] Implement lock acquisition/release functions
- [ ] Create communication protocol guide
- [ ] Implement message channel templates
- [ ] Create checkpoint protocol guide
- [ ] Implement checkpoint file format
- [ ] Create STATUS file template
- [ ] Create handoff package template
- [ ] Test all infrastructure components

### Phase 2: S2 Workflow Integration
- [ ] Update S1 guide (parallel work offering)
- [ ] Update S2 router guide (agent role routing)
- [ ] Update S2.P1 guide (checkpoint integration)
- [ ] Update S2.P2 guide (checkpoint integration)
- [ ] Update S2.P3 guide (completion signal)
- [ ] Update S3 guide (sync verification)
- [ ] Create Primary Agent guide
- [ ] Create Secondary Agent guide
- [ ] Test S2 workflow end-to-end

### Phase 3: EPIC_README Sectioning
- [ ] Update EPIC_README template (sections)
- [ ] Add Agent Assignment table
- [ ] Add Sync Status section
- [ ] Create sectioning protocol guide
- [ ] Test concurrent edits to sections

### Phase 4: User Experience
- [ ] Create parallel work offering prompt
- [ ] Refine handoff package format
- [ ] Create secondary agent startup prompt
- [ ] Create sync point notifications
- [ ] Test full user flow

### Phase 5: Safety & Recovery
- [ ] Implement stale agent detection
- [ ] Create recovery procedures guide
- [ ] Implement timeout-based sync
- [ ] Create error handling guide
- [ ] Test failure scenarios

### Phase 6: Documentation
- [ ] Update EPIC_WORKFLOW_USAGE.md
- [ ] Update CLAUDE.md
- [ ] Create prompts reference
- [ ] Create FAQ section
- [ ] Create troubleshooting guide

### Phase 7: Testing
- [ ] Run pilot with 2-feature epic
- [ ] Collect metrics
- [ ] Identify issues
- [ ] Update guides
- [ ] Run pilot with 3-feature epic

### Phase 8: Rollout
- [ ] Complete Stage 1 (validation)
- [ ] Complete Stage 2 (limited rollout)
- [ ] Complete Stage 3 (full rollout)
- [ ] Begin Stage 4 (continuous improvement)

---

**END OF S2 PARALLELIZATION PLAN**
