# S2 Primary Agent Guide: Group-Based Wave Management

**Guide Version:** 1.0
**Last Updated:** 2026-02-06
**Purpose:** Guide Primary agents through group-based S2 parallelization with dependency waves

---

## Table of Contents

1. [When to Use This Guide](#when-to-use-this-guide)
2. [Overview: Group-Based S2 Parallelization](#overview-group-based-s2-parallelization)
3. [Wave Sequencing Concept](#wave-sequencing-concept)
4. [Complete Workflow Summary](#complete-workflow-summary)
5. [Phase 1: Wave 1 Execution (Foundation Group)](#phase-1-wave-1-execution-foundation-group)
6. [Phase 2: Wave Transition (Group 1 → Group 2)](#phase-2-wave-transition-group-1--group-2)
7. [Phase 3: Wave 2 Execution (Dependent Group)](#phase-3-wave-2-execution-dependent-group)
8. [Phase 4: Additional Waves (Group 3+)](#phase-4-additional-waves-group-3)
9. [Phase 5: Wave Completion](#phase-5-wave-completion)
10. [Coordination Infrastructure](#coordination-infrastructure)
11. [Monitoring and Escalations](#monitoring-and-escalations)
12. [Troubleshooting](#troubleshooting)
13. [Examples](#examples)

---

## When to Use This Guide

**Use this guide when ALL of these apply:**

✅ You're the Primary agent coordinating S2 parallelization
✅ EPIC_README.md has "Feature Dependency Groups (S2 Only)" section
✅ Multiple dependency groups exist (Group 1, Group 2, etc.)
✅ User accepted group-based parallel work offering in S1

**DO NOT use this guide if:**
- All features are independent (use `s2_primary_agent_guide.md` instead)
- User declined parallel work (use sequential S2 workflow)
- You're a Secondary agent (use `s2_secondary_agent_guide.md` instead)

---

## Overview: Group-Based S2 Parallelization

### What is Group-Based Parallelization?

**Problem it solves:**
Some features have **spec-level dependencies** - they need other features' specs to write their own. Example: Feature B integrates with Feature A's API and needs to know the API specification before writing its integration spec.

**Solution:**
Organize features into **dependency groups** based on spec-level dependencies. Each group completes S2 in **waves**:
- **Wave 1:** Group 1 (foundation features) completes S2 first
- **Wave 2:** Group 2 (dependent features) starts S2 after Group 1 done, all features parallelize
- **Wave 3+:** Continue pattern if more groups exist

### Key Differences from Full Parallelization

| Aspect | Group-Based | Full Parallelization |
|--------|-------------|---------------------|
| **When** | Features have spec dependencies | All features independent |
| **Waves** | Multiple waves (sequential groups) | Single wave (all at once) |
| **Secondaries** | Spawn AFTER Group 1 complete | Spawn immediately |
| **Dependencies** | Group 2 needs Group 1's specs | No dependencies |
| **Complexity** | Higher (wave management) | Lower (single coordination) |

### Why Groups Matter Only for S2

**Spec-level dependencies affect RESEARCH and SPECIFICATION:**
- Feature B needs to read Feature A's spec.md to understand API
- Must wait for Feature A's S2 to complete before starting Feature B's S2

**Implementation dependencies affect S5-S8, NOT S2:**
- Feature B calls Feature A's code functions
- Both can research/specify in parallel during S2
- Dependency enforced later during implementation (S5-S8)

**After S2 complete:** Groups no longer matter (S3 is epic-level, S4+ is sequential)

---

## Wave Sequencing Concept

### Dependency Wave Pattern

```yaml
START: All features identified in S1
  ↓
WAVE 1: Group 1 (Foundation)
  - Features with NO spec-level dependencies
  - Primary agent works solo
  - Completes S2.P1 + S2.P2 for all Group 1 features
  - Output: Group 1 spec.md files available
  ↓
WAVE TRANSITION: Group 1 → Group 2
  - Primary generates handoff packages for Group 2
  - User spawns secondary agents (one per Group 2 feature)
  - Coordination infrastructure initialized
  ↓
WAVE 2: Group 2 (Dependent on Group 1)
  - Features that need Group 1's specs
  - ALL Group 2 features execute S2 in parallel
  - Primary coordinates, monitors, handles escalations
  - Completes S2.P1 for all Group 2 features
  - Primary runs S2.P2 for Group 2 features
  ↓
WAVE 3+: Additional Groups (if needed)
  - Repeat wave pattern
  - Each wave waits for previous wave's S2 completion
  ↓
WAVE COMPLETION: All Groups Done
  - Primary runs S2.P2 across ALL features (final alignment)
  - Groups no longer matter
  - Proceed to S3 (epic-level)
```

### Time Savings Example

**SHAMT-8 Logging Epic: 7 Features, 2 Groups**

**Sequential S2:**
```text
Feature 01: 2 hours
Feature 02: 2 hours
Feature 03: 2 hours
Feature 04: 2 hours
Feature 05: 2 hours
Feature 06: 2 hours
Feature 07: 2 hours
Total: 14 hours
```

**Group-Based Parallel S2:**
```text
Wave 1 (Group 1):
  - Feature 01: 2 hours (solo)

Wave 2 (Group 2):
  - Features 02-07: 2 hours (all parallel)

Total: 4 hours
TIME SAVED: 10 hours (71% reduction)
```

---

## Complete Workflow Summary

**Your role:** Primary agent coordinating all waves

**Phases:**

1. **Wave 1 Execution:** Complete S2 for Group 1 (solo work)
2. **Wave Transition:** Generate handoffs, spawn secondaries for Group 2
3. **Wave 2 Execution:** Coordinate Group 2 parallel work
4. **Additional Waves:** Repeat for Group 3+ if needed
5. **Wave Completion:** S2.P2 across ALL features, proceed to S3

**Key Responsibilities:**
- Execute S2 solo for Group 1
- Generate handoff packages between waves
- Coordinate secondary agents during Group 2+ waves
- Monitor progress, handle escalations
- Run S2.P2 after each group and at completion
- Maintain EPIC_README.md with wave status

---

## Phase 1: Wave 1 Execution (Foundation Group)

### Purpose

Complete S2 for all Group 1 features (foundation) before dependent groups can start.

### Prerequisites

✅ S1 complete with dependency groups documented
✅ EPIC_README.md has "Feature Dependency Groups (S2 Only)" section
✅ User accepted group-based parallel work offering
✅ Agent Status updated for Group 1 S2 execution

### Step-by-Step Workflow

#### Step 1.1: Identify Group 1 Features

Read EPIC_README.md "Feature Dependency Groups (S2 Only)" section:

```markdown
**Group 1 (Foundation - S2 Wave 1):**
- Feature 01: core_logging_infrastructure
- Spec Dependencies: None
- S2 Workflow: Completes S2 alone FIRST
```

**Extract:**
- List of Group 1 features (usually 1-3 features)
- No spec-level dependencies
- These define APIs/infrastructure that Group 2+ will reference

#### Step 1.2: Execute S2 for Each Group 1 Feature

**For EACH feature in Group 1:**

1. **Update Agent Status:**
   ```markdown
   **Agent Status:**
   - Last Updated: 2026-02-06 10:00
   - Current Stage: S2.P1 (Wave 1 - Group 1)
   - Current Feature: Feature 01 (core_logging_infrastructure)
   - Current Step: Executing S2.P1.I1 (Discovery)
   - Next Action: Read S2.P1 guide and begin research
   - Current Guide: stages/s2/s2_p1_spec_creation_refinement.md
   - Group: Group 1 (Foundation)
   ```

2. **Execute S2.P1 (3 iterations):**
   - **Read:** `stages/s2/s2_p1_spec_creation_refinement.md`
   - **I1:** Discovery (research, RESEARCH_NOTES.md, embed Gates 1 & 2)
   - **I2:** Checklist Resolution (user answers, embed Gate 3)
   - **I3:** Refinement & Alignment (polish spec, finalize)
   - **Output:** spec.md, checklist.md (user-approved)

3. **Update EPIC_README.md:**
   ```markdown
   ## S2 Wave Status

   **Wave 1 (Group 1):** 🔄 IN PROGRESS
   - Feature 01: ✅ S2.P1 Complete (2026-02-06 12:00)

   **Wave 2 (Group 2):** ⏳ WAITING (needs Group 1 S2 completion)
   ```

4. **Repeat for all Group 1 features** (if multiple features in Group 1)

**Note:** If Group 1 has multiple features, you can parallelize them (follow `s2_primary_agent_guide.md` for Group 1 only). Most commonly, Group 1 has 1-2 features.

#### Step 1.3: Run S2.P2 for Group 1

**After all Group 1 features complete S2.P1:**

1. **Read:** `stages/s2/s2_p2_cross_feature_alignment.md`
2. **Execute:** Pairwise comparison of Group 1 specs
3. **Validation Loop:** 3 consecutive clean rounds (zero deferred issues)
4. **Output:** Aligned specs for Group 1

**Note:** This S2.P2 run is ONLY for Group 1 features. You'll run S2.P2 again later for Group 2, and finally across ALL features at wave completion.

#### Step 1.4: Mark Group 1 S2 Complete

Update EPIC_README.md:

```markdown
## S2 Wave Status

**Wave 1 (Group 1):** ✅ COMPLETE (2026-02-06 14:00)
- Feature 01: ✅ S2 Complete (spec.md ready)
- Output: Group 1 specs available for Group 2 reference

**Wave 2 (Group 2):** 🚀 READY TO START
- Features 02-07: Waiting for handoff packages
- Dependencies satisfied: Group 1 S2 complete

**Next Action:** Generate handoff packages for Group 2 (6 secondary agents)
```

Update Agent Status:

```markdown
**Agent Status:**
- Last Updated: 2026-02-06 14:00
- Current Stage: S2 (Wave Transition)
- Current Step: Group 1 S2 complete, preparing Group 2 handoffs
- Next Action: Generate handoff packages for Group 2 features (02-07)
- Group 1 Status: ✅ COMPLETE
- Group 2 Status: ⏳ READY TO START
```

**Checkpoint Verification:**
- [ ] All Group 1 features have spec.md (user-approved)
- [ ] All Group 1 features have checklist.md (user-answered)
- [ ] S2.P2 validation complete for Group 1 (3 clean rounds)
- [ ] EPIC_README.md updated with Group 1 complete status
- [ ] Agent Status updated for wave transition

---

## Phase 2: Wave Transition (Group 1 → Group 2)

### Purpose

Generate handoff packages for Group 2 features and spawn secondary agents.

### Prerequisites

✅ Group 1 S2 complete (all features have spec.md)
✅ EPIC_README.md marked Group 1 complete
✅ Agent Status updated for wave transition

### Step-by-Step Workflow

#### Step 2.1: Identify Group 2 Features

Read EPIC_README.md "Feature Dependency Groups (S2 Only)" section:

```markdown
**Group 2 (Dependent - S2 Wave 2):**
- Features 02-07: All script logging features
- Spec Dependencies: Need Group 1's spec (API reference)
- S2 Workflow: After Group 1 completes S2, all features do S2 in parallel
```

**Extract:**
- List of Group 2 features (e.g., Features 02-07 = 6 features)
- Dependencies on Group 1 (they need Group 1's spec.md files)
- These features can parallelize with each other (no inter-dependencies within Group 2)

#### Step 2.2: Generate Handoff Packages

**For EACH feature in Group 2:**

**Follow:** `parallel_work/s2_primary_agent_guide.md` → "Phase 3: Generate Handoff Packages"

**Template with GROUP AWARENESS:**

```markdown
I'm joining as a secondary agent to help with S2 parallelization for the {epic_name} epic.

## Agent Configuration

**My Agent ID:** Secondary-{LETTER} (A/B/C/D/E/F...)
**My Feature Assignment:** Feature {N}: {name}
**My Role:** Execute S2.P1 (3 iterations), then wait for Primary to run S2.P2
**Dependency Group:** Group 2 (Dependent on Group 1)

## Group Context

**Why I'm Starting Now:**
- Group 1 has completed S2 (Feature 01: core_logging_infrastructure)
- Group 1's specs are available for reference
- My feature depends on Group 1's spec to write its own spec
- I can now specify my feature with knowledge of Group 1's APIs

**Group 1 Specs Available:**
- Feature 01: feature_01_core_logging_infrastructure/spec.md
- **Key content:** LineBasedRotatingHandler API, setup_logger() function, folder structure

**Group 2 Features (parallel with me):**
- Feature 02: [module]_logging (Secondary-A - me)
- Feature 03: api_client_logging (Secondary-B)
- Feature 04: data_processor_logging (Secondary-C)
- Feature 05: report_generator_logging (Secondary-D)
- Feature 06: cache_manager_logging (Secondary-E)
- Feature 07: scheduler_logging (Secondary-F)

## My Task

**Execute S2.P1 for Feature {N}:**
1. Read guide: `stages/s2/s2_p1_spec_creation_refinement.md`
2. Execute 3 iterations: Discovery, Checklist Resolution, Refinement
3. Reference Group 1 specs as needed (file path: feature_01_*/spec.md)
4. Mark complete in STATUS file
5. **STOP after S2.P1** - Wait for Primary to run S2.P2
6. Follow coordination protocols (checkpoints every 15 min, check inbox, update STATUS)

**What to Read:**
- `parallel_work/s2_secondary_agent_guide.md` (my complete workflow)
- `feature_{N}_{name}/HANDOFF.md` (feature-specific context)

**Coordination:**
- Update checkpoints/ every 15 minutes
- Check inbox/ for messages from Primary
- Update STATUS file at phase transitions
- Escalate to Primary if blocked

## Epic Context

[Include same epic context as standard handoff: EPIC_README.md summary, Discovery Context, feature list, etc.]

## Getting Started

**First actions:**
1. Read `parallel_work/s2_secondary_agent_guide.md` (your complete guide)
2. Read `feature_{N}_{name}/HANDOFF.md` (feature-specific setup)
3. Read Group 1 specs: `feature_01_*/spec.md` (understand dependencies)
4. Update Agent Status in `feature_{N}_{name}/README.md`
5. Begin S2.P1.I1 (Discovery)

**Remember:** You're in Group 2, which depends on Group 1's S2 completion. Group 1 is done, so you can proceed with full knowledge of their APIs.
```

**Key additions for group-based handoffs:**
- "Dependency Group: Group 2"
- "Why I'm Starting Now" section explaining Group 1 completion
- "Group 1 Specs Available" with file paths
- "Group 2 Features (parallel with me)" showing all Group 2 features

#### Step 2.3: Present Handoffs to User

**Create presentation message:**

````markdown
🚀 Group 1 S2 Complete! Ready to spawn Group 2 secondary agents.

## Wave 1 Results (Group 1)

✅ **Feature 01: core_logging_infrastructure**
- S2 Complete: 2026-02-06 14:00
- Time: 2 hours
- Output: spec.md ready (defines LineBasedRotatingHandler API)

## Wave 2 Setup (Group 2)

**Group 2 features ready to start:**
- Feature 02: [module]_logging
- Feature 03: api_client_logging
- Feature 04: data_processor_logging
- Feature 05: report_generator_logging
- Feature 06: cache_manager_logging
- Feature 07: scheduler_logging

**Dependencies satisfied:**
- All Group 2 features need Feature 01's spec (API reference)
- Feature 01 spec.md is complete and available
- Group 2 can now specify their features with API knowledge

**Parallelization:**
- 6 secondary agents needed (one per feature)
- All 6 will execute S2 simultaneously
- Estimated time: 2 hours (parallel execution)

**Total S2 Time:** 4 hours (Wave 1: 2h + Wave 2: 2h) vs 14 hours sequential

---

## Instructions for Wave 2

**Please open 6 new Claude Code sessions and give each one this minimal startup instruction:**

### Secondary-A: Feature 02
~~~text
You are a secondary agent for SHAMT-{N} for feature 02
~~~

### Secondary-B: Feature 03
~~~text
You are a secondary agent for SHAMT-{N} for feature 03
~~~

[Continue for all Group 2 features, incrementing the feature number each time...]

Each agent will automatically locate the epic folder, find their `feature_XX_{name}/HANDOFF_PACKAGE.md`, and self-configure. No copy-paste of handoff content needed.

---

**After spawning all 6 agents:**
- They'll update agent_checkpoints/ to signal startup
- I'll monitor progress every 15 minutes
- I'll handle any escalations from agent_comms/
- After all 6 complete S2.P1 → I'll run S2.P2
- Then we proceed to S3 (groups no longer matter)

**Let me know when you've spawned all 6 agents and I'll begin coordination.**
````

#### Step 2.4: Wait for Secondary Agent Startup

**Monitor coordination infrastructure:**

1. **Check agent_checkpoints/ for startup signals:**
   ```bash
   ls -lt agent_checkpoints/

   # Expected files (one per secondary, .json extension):
   # secondary_a.json (Feature 02)
   # secondary_b.json (Feature 03)
   # secondary_c.json (Feature 04)
   # secondary_d.json (Feature 05)
   # secondary_e.json (Feature 06)
   # secondary_f.json (Feature 07)
   ```

   > **Path Note:** All coordination paths are relative to the epic folder (not `parallel_work/coordination/`).
   > Checkpoint files use `.json` extension. Communication files are flat `.md` files in `agent_comms/`.
   > See CLAUDE.md "S2 Parallel Work Structure Rules" for canonical structure.

2. **Verify all secondaries initialized:**
   - Each checkpoint file should have "Status: STARTUP" or "Status: IN_PROGRESS"
   - Last updated within last 5 minutes
   - Assigned feature matches expected feature

3. **Update EPIC_README.md once all agents started:**
   ```markdown
   ## S2 Wave Status

   **Wave 1 (Group 1):** ✅ COMPLETE

   **Wave 2 (Group 2):** 🔄 IN PROGRESS (6 agents working)
   - Feature 02: Secondary-A 🔄 S2.P1 in progress
   - Feature 03: Secondary-B 🔄 S2.P1 in progress
   - Feature 04: Secondary-C 🔄 S2.P1 in progress
   - Feature 05: Secondary-D 🔄 S2.P1 in progress
   - Feature 06: Secondary-E 🔄 S2.P1 in progress
   - Feature 07: Secondary-F 🔄 S2.P1 in progress

   **Last Sync:** 2026-02-06 14:30
   ```

**Proceed to Phase 3 once all agents initialized.**

---

## Phase 3: Wave 2 Execution (Dependent Group)

### Purpose

Coordinate Group 2 secondary agents executing S2.P1 in parallel.

### Prerequisites

✅ All Group 2 secondary agents spawned and initialized
✅ Coordination infrastructure active (checkpoints, inboxes, STATUS files)
✅ EPIC_README.md updated with Wave 2 in-progress status

### Step-by-Step Workflow

#### Step 3.1: Monitor Secondary Agent Progress

**Follow:** `parallel_work/s2_primary_agent_guide.md` → "Phase 4: Coordinate Secondary Agents"

**🚨 PRIMARY AGENT MONITORING SCOPE — READ BEFORE MONITORING:**

```text
What to check during Wave 2 monitoring:
✅ agent_checkpoints/*.json timestamps (is agent active / not stale?)
✅ STATUS files in each feature folder (is agent making progress?)
✅ agent_comms/ for escalation messages addressed TO Primary

What NOT to check (these are secondary agent responsibilities):
❌ feature_XX_*/checklist.md — secondary handles their own Q&A with user
❌ feature_XX_*/spec.md drafts — secondary writes their own spec

Primary MUST NOT:
- Read secondary agents' checklist.md files to gather their open questions
- Present secondary checklist questions to the user on their behalf
- Intervene in a secondary's Q&A workflow unless the secondary explicitly escalates

Only case where Primary relays a secondary question:
Secondary sends an escalation message to agent_comms/ (e.g., agent_comms/secondary_a_to_primary.md)
→ Primary reads it → Primary presents the escalation to the user.
This is the ONLY permitted relay path.
```

**Every 15 minutes:**

1. **Check all agent checkpoints:**
   ```bash
   cat agent_checkpoints/*.json
   ```

   **Verify:**
   - Timestamps within last 20 minutes (agents not stale)
   - Status shows progress (STARTUP → IN_PROGRESS → READY_FOR_SYNC)
   - No blockers reported

2. **Check agent_comms/ for escalations addressed to Primary:**
   ```bash
   ls agent_comms/
   cat agent_comms/secondary_*_to_primary.md
   ```

   **If messages found:**
   - Read message, assess escalation
   - Respond within 15 minutes
   - Provide guidance or ask user questions

3. **Update sync status in EPIC_README.md:**
   ```markdown
   ## S2 Wave Status - Wave 2 Progress

   **Last Sync:** 2026-02-06 15:00

   | Feature | Agent | S2.P1.I1 | S2.P1.I2 | S2.P1.I3 | Status |
   |---------|-------|----------|----------|----------|--------|
   | 02 | Secondary-A | ✅ | ✅ | 🔄 | In Progress |
   | 03 | Secondary-B | ✅ | 🔄 | ⏳ | In Progress |
   | 04 | Secondary-C | ✅ | ✅ | ✅ | Ready for S2.P2 |
   | 05 | Secondary-D | ✅ | ✅ | 🔄 | In Progress |
   | 06 | Secondary-E | ✅ | ✅ | ✅ | Ready for S2.P2 |
   | 07 | Secondary-F | ✅ | 🔄 | ⏳ | In Progress |
   ```

4. **Handle escalations as needed:**
   - Explicit blockers (via agent_comms/): Investigate, ask user if needed, relay resolution to secondary
   - Technical blockers: Investigate, provide guidance
   - Stale agents: Send warning via agent_comms/, escalate to user if no response
   - **Do NOT relay routine checklist Q&A** — secondaries handle their own user questions

#### Step 3.2: Wait for All Group 2 Features to Complete S2.P1

**Exit condition:** All Group 2 features have:
- ✅ S2.P1.I1 complete (Discovery)
- ✅ S2.P1.I2 complete (Checklist Resolution with user approval)
- ✅ S2.P1.I3 complete (Refinement)
- ✅ STATUS file: `STAGE: S2.P1` and `READY_FOR_SYNC: true`
- ✅ spec.md and checklist.md exist and are user-approved

**Verification:**

```bash
# Check all Group 2 STATUS files
grep "READY_FOR_SYNC" feature_0[2-7]_*/STATUS

# Expected output (all true):
# feature_02_[module]_logging/STATUS:READY_FOR_SYNC: true
# feature_03_api_client_logging/STATUS:READY_FOR_SYNC: true
# feature_04_data_processor_logging/STATUS:READY_FOR_SYNC: true
# feature_05_report_generator_logging/STATUS:READY_FOR_SYNC: true
# feature_06_cache_manager_logging/STATUS:READY_FOR_SYNC: true
# feature_07_scheduler_logging/STATUS:READY_FOR_SYNC: true
```

#### Step 3.3: Run S2.P2 for Group 2

**After all Group 2 features complete S2.P1:**

1. **Announce to secondary agents:**
   ```markdown
   # Message to all Group 2 inboxes

   🎉 All Group 2 features have completed S2.P1!

   I'm now running S2.P2 (Cross-Feature Alignment) for Group 2 features.

   **Your status:** WAITING for S2.P2 completion
   **What I'm doing:** Pairwise comparison of all Group 2 specs (Features 02-07)
   **Estimated time:** 20-30 minutes
   **Next step:** After S2.P2 → I'll check if more groups exist or proceed to wave completion

   You can close your session or wait for final updates.
   ```

2. **Execute S2.P2 for Group 2:**
   - **Read:** `stages/s2/s2_p2_cross_feature_alignment.md`
   - **Scope:** Pairwise comparison of Group 2 features ONLY (Features 02-07)
   - **Process:** Compare each pair, check for conflicts/overlaps/gaps
   - **Validation Loop:** 3 consecutive clean rounds (zero deferred issues)
   - **Output:** Aligned Group 2 specs

3. **Update EPIC_README.md:**
   ```markdown
   ## S2 Wave Status

   **Wave 1 (Group 1):** ✅ COMPLETE

   **Wave 2 (Group 2):** ✅ COMPLETE (2026-02-06 16:30)
   - Feature 02: ✅ S2 Complete
   - Feature 03: ✅ S2 Complete
   - Feature 04: ✅ S2 Complete
   - Feature 05: ✅ S2 Complete
   - Feature 06: ✅ S2 Complete
   - Feature 07: ✅ S2 Complete

   **Wave 3:** ⏳ (check if more groups exist)
   ```

**Proceed to Phase 4 if more groups exist, otherwise skip to Phase 5.**

---

## Phase 4: Additional Waves (Group 3+)

### Purpose

Handle epics with 3+ dependency groups (rare but possible).

### When This Applies

**Check EPIC_README.md "Feature Dependency Groups (S2 Only)" section:**
- If Group 3, Group 4, etc. documented → Continue with additional waves
- If only Group 1 and Group 2 → Skip to Phase 5

### Workflow

**Repeat Phases 2-3 for each additional group:**

1. **Wave Transition (Group N → Group N+1):**
   - Identify Group N+1 features
   - Generate handoff packages with Group N context
   - Present to user, spawn secondary agents
   - Wait for startup

2. **Wave Execution (Group N+1):**
   - Monitor secondary agents
   - Handle escalations
   - Wait for S2.P1 completion
   - Run S2.P2 for Group N+1

3. **Update EPIC_README.md after each wave:**
   ```markdown
   **Wave 3 (Group 3):** ✅ COMPLETE (2026-02-06 18:30)
   - Feature 08: ✅ S2 Complete
   - Feature 09: ✅ S2 Complete
   ```

**Continue until all groups complete S2.**

---

## Phase 5: Wave Completion

### Purpose

Finalize S2 across ALL features and prepare for S3 transition.

### Prerequisites

✅ All dependency groups complete S2 (Wave 1, Wave 2, Wave 3+)
✅ All features have spec.md and checklist.md (user-approved)
✅ S2.P2 run for each group individually

### Step-by-Step Workflow

#### Step 5.1: Run Final S2.P2 Across ALL Features

**Purpose:** Cross-group alignment (ensure Group 1 + Group 2 + Group 3+ specs align)

1. **Read:** `stages/s2/s2_p2_cross_feature_alignment.md`

2. **Execute S2.P2 across ALL features:**
   - **Scope:** Pairwise comparison of ALL features (Group 1 + Group 2 + Group 3+)
   - **Example:** For SHAMT-8 (7 features), compare all pairs:
     - Feature 01 ↔ Feature 02
     - Feature 01 ↔ Feature 03
     - [Continue for all 21 pairs in 7-feature epic]
   - **Process:** Check for conflicts, overlaps, gaps across groups
   - **Validation Loop:** 3 consecutive clean rounds (zero deferred issues)

3. **Why this matters:**
   - Earlier S2.P2 runs were INTRA-group (within Group 1, within Group 2)
   - This S2.P2 run is INTER-group (across all groups)
   - Catches cross-group issues (e.g., Group 2 feature conflicts with another Group 2 feature based on Group 1 spec)

**Output:** All specs aligned across entire epic

#### Step 5.2: Verify S2 Completion for Epic

**Checklist:**

- [ ] All features have spec.md (user-approved via Gate 3)
- [ ] All features have checklist.md (user-answered)
- [ ] S2.P2 validation complete across ALL features (3 clean rounds)
- [ ] No deferred issues remaining
- [ ] All secondary agents notified of completion

**Verification commands:**

```bash
# Check all features have spec.md
ls feature_*/spec.md

# Check all STATUS files show S2 complete
grep "STAGE:" feature_*/STATUS

# Check no features have unresolved issues
grep "ISSUES:" feature_*/STATUS | grep -v "ISSUES: 0"
```

#### Step 5.3: Update EPIC_README.md with S2 Summary

```markdown
## S2 Status: ✅ COMPLETE (All Features)

### Wave Summary

**Wave 1 (Group 1):**
- Feature 01: core_logging_infrastructure
- Completed: 2026-02-06 14:00
- Time: 2 hours (solo work)

**Wave 2 (Group 2):**
- Features 02-07: All script logging features
- Completed: 2026-02-06 16:30
- Time: 2 hours (6 agents in parallel)

**Final S2.P2 (Cross-Group Alignment):**
- Scope: All 7 features
- Completed: 2026-02-06 17:00
- Validation: 3 consecutive clean rounds

### Time Savings

- **Sequential S2:** 14 hours (7 features × 2h each)
- **Group-Based Parallel S2:** 4 hours (Wave 1: 2h + Wave 2: 2h parallel)
- **TIME SAVED:** 10 hours (71% reduction)

### Next Stage

**S3: Epic-Level Docs, Tests, and Approval**
- Groups no longer matter (all features participate equally)
- Primary agent runs S3 solo
- Guide: `stages/s3/s3_epic_planning_approval.md`
```

#### Step 5.4: Notify Secondary Agents

**Send message to all Group 2+ agent inboxes:**

```markdown
🎉 S2 Complete for Epic!

## Summary

**All features have completed S2:**
- Group 1 (Feature 01): ✅ Complete
- Group 2 (Features 02-07): ✅ Complete

**Final S2.P2 (cross-group alignment):** ✅ Complete
- All specs aligned across entire epic
- Validation Loop: 3 consecutive clean rounds passed

## Your Status

**You can now:**
1. ✅ Close your session (your work is complete for S2)
2. 🔄 Wait for S3/S4 if you'd like to observe (I'll run solo)
3. 💬 Ask questions if needed

**What happens next:**
- I'll run S3 (Epic-Level Docs, Tests, and Approval) - Epic-level, all features together
- I'll run S4 (Testing Strategy) - Per-feature sequential
- S5-S8: Implementation (per-feature sequential, no parallelization)
- S9-S10: Epic QC and cleanup

**Groups no longer matter after S2.** All features are now equal participants in remaining stages.

**Thank you for your work on S2! Feature {N} spec looks great.**

---

**If you have questions or noticed any issues, please add to your inbox for me to review.**
```

#### Step 5.5: Update Agent Status for S3 Transition

```markdown
**Agent Status:**
- Last Updated: 2026-02-06 17:00
- Current Stage: S2 → S3 Transition
- Current Step: All features complete S2, preparing for S3
- Next Action: Read S3 guide and begin Epic-Level Testing Strategy (S3.P1)
- Current Guide: stages/s3/s3_epic_planning_approval.md
- S2 Status: ✅ COMPLETE (all features, all groups)
- Groups: No longer matter (S3 is epic-level)
```

#### Step 5.6: Transition to S3

**Announce to user:**

```markdown
✅ **S2 Complete for {epic_name} Epic!**

## Results

**7 features completed S2 in 4 hours** (vs 14 hours sequential)

**Group-Based Parallelization Success:**
- Wave 1 (Group 1): 1 feature, 2 hours solo
- Wave 2 (Group 2): 6 features, 2 hours parallel
- Final alignment: 20 minutes
- **Time saved: 10 hours (71% reduction)**

**Deliverables:**
- ✅ All 7 features have spec.md (user-approved)
- ✅ All 7 features have checklist.md (user-answered)
- ✅ Cross-group alignment complete (3 clean validation rounds)
- ✅ Zero deferred issues

**Secondary agents:** Notified of completion, can close sessions

---

## Next Stage: S3 (Epic-Level Docs, Tests, and Approval)

**S3 is epic-level** - all features participate, no parallelization, no groups

**What I'll do:**
1. S3.P1: Create epic smoke test plan (integration tests across all features)
2. S3.P2: Refine EPIC_README.md with feature summaries and architecture decisions
3. S3.P3: Gate 4.5 — get user approval of epic plan before S4

**Estimated time:** 1-2 hours

**Proceeding to S3 now...**

**Then:**
- Read `stages/s3/s3_epic_planning_approval.md`
- Execute S3 workflow (epic-level, solo work)
- Groups no longer matter
```

---

## Coordination Infrastructure

### File Structure

**Location:** Epic root folder (alongside `feature_XX_*` folders)

```text
{epic_root}/                              ← e.g., SHAMT-10-refactoring/
├── .epic_locks/                          ← Lock files (Primary creates)
├── agent_comms/                          ← Flat .md files only (no subdirs)
│   ├── primary_to_secondary_a.md        ← Primary → Secondary-A messages
│   ├── secondary_a_to_primary.md        ← Secondary-A → Primary escalations
│   ├── primary_to_secondary_b.md
│   └── secondary_b_to_primary.md
├── agent_checkpoints/                    ← Flat .json files only (no subdirs)
│   ├── secondary_a.json                 ← Secondary-A status
│   ├── secondary_b.json                 ← Secondary-B status
│   └── ...
├── feature_01_{name}/
├── feature_02_{name}/
└── ...
```

> **🚨 Structure Rules:**
> - `agent_comms/` = flat `.md` files only — NO subdirectories
> - `agent_checkpoints/` = flat `.json` files only — NO subdirectories
> - Primary creates ALL directories; secondaries create FILES only

### Checkpoint Format

**File:** `agent_checkpoints/secondary_a.json`

```json
{
  "agent_id": "Secondary-A",
  "feature": "feature_02_[module]_logging",
  "group": "Group 2",
  "status": "IN_PROGRESS",
  "current_phase": "S2.P1.I2",
  "last_updated": "2026-02-06T15:30:00",
  "blocker": null,
  "next_checkpoint": "2026-02-06T15:45:00"
}
```

**Primary checks:** Every 15 minutes, verify all checkpoints updated within last 20 minutes

### Communication Format

**Secondary escalates to Primary:** `agent_comms/secondary_a_to_primary.md`

```markdown
**From:** Secondary-A
**Feature:** Feature 02 ([module]_logging)
**Timestamp:** 2026-02-06 15:35
**Type:** BLOCKER
**Urgency:** HIGH

## Blocker

Feature 02 cannot proceed — spec conflict with Group 1 output:
Feature 01 spec defines the logging API as synchronous,
but Feature 02 requires async calls for performance.

**Requested Action:** Clarify with user which approach takes precedence.
```

**Primary responds to Secondary:** `agent_comms/primary_to_secondary_a.md`

```markdown
**To:** Secondary-A
**Feature:** Feature 02 ([module]_logging)
**Timestamp:** 2026-02-06 15:40

## Response

User decided: Use async logging (Feature 01 spec will be updated).
Proceed with async approach in Feature 02 spec.

**Action:** Update your spec accordingly and resume S2.P1.I2
```

> **🚨 RELAY PROHIBITION:** Secondary agents handle their own checklist questions directly with the user.
> Primary ONLY receives escalations for genuine blockers (spec conflicts, technical ambiguities
> that block all paths). Do NOT relay routine checklist Q&A through Primary.

---

## Monitoring and Escalations

### Primary Agent Responsibilities

**Every 15 minutes:**

1. **Check all checkpoints** for freshness (< 20 min old)
2. **Check all secondary inboxes** for escalations
3. **Update sync_status.md** with current progress
4. **Respond to escalations** within 15 minutes

**Escalation Types:**

| Type | Response Time | Action |
|------|--------------|--------|
| BLOCKER | 15 min | Investigate, provide guidance or escalate to user |
| STALE_CHECKPOINT | 20 min | Send warning to secondary via agent_comms/ |
| SPEC_CONFLICT | 15 min | Document conflict, get user decision, relay to secondary |
| ERROR | Immediate | Investigate, escalate to user if needed |

> **Note:** Secondary agents do NOT escalate routine checklist questions — they ask the user directly.
> Primary only receives escalations for blockers that prevent all paths forward.

### Secondary Agent Responsibilities

**Every 15 minutes:**

1. **Update checkpoint file** (`agent_checkpoints/secondary_X.json`) with current status
2. **Check agent_comms/** for messages from Primary
3. **Escalate to Primary** via `agent_comms/secondary_X_to_primary.md` if blocked

**When to escalate to Primary:**
- Spec conflict with Group 1 feature that blocks your spec
- Technical ambiguity that prevents ALL paths forward (not just one option)
- Notice error in Group 1 spec that affects your feature design

**Handle directly with user (do NOT escalate to Primary):**
- Checklist questions that need user input
- Clarifications about your specific feature's scope
- Routine design decisions within your feature

---

## Troubleshooting

### Issue: Secondary Agent Not Updating Checkpoints

**Symptoms:**
- Checkpoint file not updated in > 20 minutes
- Agent appears stalled

**Actions:**

1. **Send warning via agent_comms/** (`agent_comms/primary_to_secondary_X.md`):
   ```markdown
   ⚠️ CHECKPOINT STALE WARNING

   Your checkpoint hasn't updated in 25 minutes. Are you still working?

   Please update agent_checkpoints/secondary_X.json within 5 minutes or I'll escalate to user.
   ```

2. **Wait 5 minutes for response**

3. **If no response → Escalate to user:**
   ```markdown
   ⚠️ Secondary-A (Feature 02) appears stalled - no checkpoint updates for 30 minutes.

   **Options:**
   1. Check if Secondary-A session is still active
   2. Spawn replacement secondary agent with same handoff package
   3. Switch to sequential mode for Feature 02 (I'll take over)

   What would you like to do?
   ```

### Issue: Cross-Group Spec Conflict During Final S2.P2

**Symptoms:**
- During final S2.P2 (cross-group alignment), discover conflict between groups
- Example: Group 2 feature assumes API not defined in Group 1 spec

**Actions:**

1. **Document conflict:**
   ```markdown
   🚨 CROSS-GROUP CONFLICT DETECTED

   **Feature 03 (Group 2) spec assumes:**
   - setup_logger() accepts 'rotation_size' parameter

   **Feature 01 (Group 1) spec defines:**
   - setup_logger() does NOT have 'rotation_size' parameter

   **Impact:** Feature 03 spec is incompatible with Feature 01 API
   ```

2. **Determine fix location:**
   - **Option A:** Update Group 1 spec (add parameter to API)
   - **Option B:** Update Group 2 spec (remove assumption, use different approach)

3. **Ask user which option:**
   ```markdown
   I found a cross-group spec conflict during final S2.P2 alignment.

   [Describe conflict]

   **Options:**
   1. Update Feature 01 spec (add rotation_size parameter to API)
   2. Update Feature 03 spec (use different approach without rotation_size)

   Which option should I take?
   ```

4. **After user decision:**
   - Update appropriate spec(s)
   - Re-run Validation Loop round for affected features
   - Continue S2.P2 until clean

### Issue: User Wants to Add Feature Mid-S2

**Symptoms:**
- User requests new Feature 08 after Wave 1 complete but Wave 2 in progress

**Actions:**

1. **Determine feature dependencies:**
   - Does Feature 08 depend on Group 1? → Add to Group 2
   - Does Feature 08 depend on Group 2? → Create Group 3
   - Does Feature 08 have no dependencies? → Add to Group 1 (requires restarting Wave 1)

2. **If adding to Group 2 (most common):**
   ```markdown
   I can add Feature 08 to Group 2 (currently in progress).

   **Process:**
   1. Create feature_08_{name}/ folder
   2. Generate handoff package for Secondary-G
   3. You spawn Secondary-G agent
   4. Secondary-G joins Wave 2 (in progress)

   **Impact:** Minimal - one more agent in coordination pool

   Should I proceed?
   ```

3. **If adding to new Group 3:**
   ```markdown
   Feature 08 depends on Group 2 specs, so I'll create Group 3.

   **Process:**
   1. Let Group 2 complete Wave 2 S2
   2. After Wave 2 done → Create Wave 3 for Feature 08
   3. Generate handoff, spawn Secondary-G
   4. Execute Wave 3 S2

   **Impact:** Adds one more wave (2 hours)

   Should I proceed?
   ```

---

## Examples

### Example 1: SHAMT-8 Logging Epic (2 Groups, 7 Features)

**Setup:**
- **Group 1:** Feature 01 (core_logging_infrastructure)
- **Group 2:** Features 02-07 (all script logging)
- **Total features:** 7
- **Dependency:** Group 2 needs Group 1's LineBasedRotatingHandler API

**Timeline:**

| Time | Event |
|------|-------|
| 12:00 | S1 complete, transition to S2 Wave 1 |
| 12:00-14:00 | Wave 1: Primary executes S2 for Feature 01 (solo) |
| 14:00 | Feature 01 S2 complete, generate 6 handoff packages |
| 14:15 | User spawns 6 secondary agents (Secondary-A through Secondary-F) |
| 14:15-16:30 | Wave 2: All 6 Group 2 features execute S2.P1 in parallel |
| 16:30 | All Group 2 features complete S2.P1 |
| 16:30-16:50 | Primary runs S2.P2 for Group 2 (pairwise comparison) |
| 16:50-17:10 | Primary runs final S2.P2 across ALL 7 features (cross-group alignment) |
| 17:10 | S2 complete, transition to S3 |

**Results:**
- **Sequential time:** 14 hours (7 × 2h)
- **Parallel time:** 4 hours (Wave 1: 2h + Wave 2: 2h)
- **Savings:** 10 hours (71%)

### Example 2: Hypothetical 3-Group Epic (15 Features)

**Setup:**
- **Group 1:** Features 01-03 (core infrastructure) - independent
- **Group 2:** Features 04-10 (modules using Group 1 APIs) - depend on Group 1
- **Group 3:** Features 11-15 (integrations using Group 2 modules) - depend on Group 2
- **Total features:** 15

**Timeline:**

| Wave | Features | Mode | Time | Dependencies |
|------|----------|------|------|--------------|
| Wave 1 | 01-03 (3) | Parallel | 2h | None (Group 1 can parallelize internally) |
| Wave 2 | 04-10 (7) | Parallel | 2h | Need Group 1 specs |
| Wave 3 | 11-15 (5) | Parallel | 2h | Need Group 2 specs |
| Final S2.P2 | All 15 | Solo | 30m | Cross-group alignment |

**Results:**
- **Sequential time:** 30 hours (15 × 2h)
- **Parallel time:** 6.5 hours (3 waves × 2h + 30m alignment)
- **Savings:** 23.5 hours (78%)

---

## Summary

**Group-based S2 parallelization enables:**
- ✅ Dependency management (spec-level dependencies respected)
- ✅ Parallel execution (within each group)
- ✅ Time savings (60-70% reduction for typical 2-group epics)
- ✅ Clean workflow (groups only matter for S2, not S3+)

**Primary agent responsibilities:**
- Execute Wave 1 solo for Group 1
- Generate handoffs and spawn secondaries for Group 2+
- Coordinate each wave's parallel work
- Run S2.P2 after each wave and at completion
- Transition to S3 when all groups complete S2

**Critical rules:**
- Groups exist ONLY for S2 parallelization
- Each group completes S2 before next group starts
- Within each group, features parallelize freely
- After S2 complete, groups no longer matter (S3 is epic-level)
- Spec-level dependencies affect S2, implementation dependencies affect S5-S8

**For additional guidance:**
- Full parallelization (no groups): `s2_primary_agent_guide.md`
- Secondary agent workflow: `s2_secondary_agent_guide.md`
- Sequential S2: `s2_feature_deep_dive.md` (router) → phase guides
