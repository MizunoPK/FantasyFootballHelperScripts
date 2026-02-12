# Group-Based S2 Parallelization: Intended Flow & Guide Gaps

**Created:** 2026-02-06
**Purpose:** Document the intended workflow for group-based S2 parallelization and identify guide gaps preventing proper implementation
**Epic Context:** KAI-8-logging_refactoring (7 features, 2 dependency groups)

---

## Executive Summary

**Problem Identified:** Current guides document parallel S2 work but assume all features can parallelize simultaneously. When features have spec-level dependencies (Feature B needs Feature A's spec to write its own), the guides don't properly handle group-based waves.

**Intended Flow:** Features are organized into dependency groups during S1. Each group completes ALL of S2 before the next group starts. Within each group, features execute S2 in parallel.

**Impact of Gaps:** Agents attempt to parallelize all features simultaneously, causing blocking dependencies and workflow confusion.

---

## Intended Workflow (Step-by-Step)

### Phase 1: S1 Epic Planning - Group Identification

**Step 5.7.5: Feature Dependency Analysis**

**When:** After creating all feature folders, before parallelization offering

**Agent Actions:**

1. **Analyze each feature for dependencies:**
   ```
   For each feature:
     - Does this feature need other features' SPECS to write its own spec?
       → Spec-level dependency (matters for S2 parallelization)
     - Does this feature need other features' IMPLEMENTATION to build its code?
       → Implementation dependency (matters for S5-S8, NOT S2)
   ```

2. **Organize features into groups:**
   ```
   Group 1 (Foundation):
     - Features with NO spec-level dependencies
     - Can research and specify independently
     - Example: Core infrastructure, foundational modules

   Group 2 (Dependent):
     - Features that need Group 1's specs as reference
     - Must wait for Group 1 to complete S2
     - Example: Features that integrate with Group 1's APIs

   Group 3 (if needed):
     - Features that need Group 2's specs
     - Must wait for Group 2 to complete S2
   ```

3. **Example (KAI-8 Logging Epic):**
   ```markdown
   ## Feature Dependency Groups (S2 Only)

   **Group 1 (Foundation - S2 Wave 1):**
   - Feature 01: core_logging_infrastructure
   - Spec Dependencies: None
   - Why first: Defines LineBasedRotatingHandler API that Group 2 needs to reference

   **Group 2 (Scripts - S2 Wave 2):**
   - Feature 02: league_helper_logging
   - Feature 03: player_data_fetcher_logging
   - Feature 04: accuracy_sim_logging
   - Feature 05: win_rate_sim_logging
   - Feature 06: historical_data_compiler_logging
   - Feature 07: schedule_fetcher_logging
   - Spec Dependencies: Need Feature 01's spec (setup_logger API, folder structure)
   - Why second: Must know Group 1's API to write their integration specs

   **S2 Workflow:**
   - Group 1 completes S2 (S2.P1 + S2.P2) first
   - Group 2 starts S2 after Group 1 finishes
   - Within Group 2: all 6 features do S2 in parallel

   **After S2:**
   - Groups no longer matter
   - S3: Epic-level (all features together)
   - S4+: Sequential or epic-level per stage
   ```

4. **Decision criteria for groups:**
   - **Spec-level dependency = different group**
   - **Implementation dependency only = same group** (doesn't affect S2)
   - **No dependencies = Group 1** (can parallelize freely)

---

### Phase 2: S1 Epic Planning - Parallelization Offering

**Step 5.9: Offer Parallel Work to User**

**When:** After group identification, before S1 completion

**Agent Actions:**

1. **Calculate time savings WITH groups:**
   ```
   Sequential S2 (all 7 features):
   - Feature 01: 2 hours
   - Feature 02: 2 hours
   - Feature 03: 2 hours
   - Feature 04: 2 hours
   - Feature 05: 2 hours
   - Feature 06: 2 hours
   - Feature 07: 2 hours
   Total: 14 hours

   Group-Based Parallel S2:
   - Group 1 (Feature 01): 2 hours
   - Group 2 (Features 02-07 in parallel): 2 hours
   Total: 4 hours

   TIME SAVINGS: 10 hours (71% reduction)
   ```

2. **Present offering with group explanation:**
   ```markdown
   🚀 PARALLEL WORK OPPORTUNITY

   I've identified 7 features organized into 2 dependency groups:

   **Group 1 (Foundation):**
   - Feature 01: core_logging_infrastructure
   - No dependencies, completes S2 first

   **Group 2 (Scripts):**
   - Features 02-07: All script logging features
   - Depend on Feature 01's spec (need to know API)
   - Can parallelize with each other once Group 1 done

   **Sequential approach:**
   - All 7 features one-by-one: 14 hours

   **Group-based parallel approach:**
   - Group 1 completes S2: 2 hours
   - Group 2 does S2 in parallel (6 features): 2 hours
   - Total: 4 hours

   **TIME SAVINGS: 10 hours (71% reduction in S2 time)**

   **Workflow:**
   1. I complete S2 for Feature 01 (Group 1)
   2. After Group 1 done → I spawn 6 secondary agents for Group 2
   3. All 6 Group 2 features do S2 simultaneously
   4. After all S2 complete → I run S3 (epic-level)

   Would you like to:
   1. ✅ Enable group-based parallel work (I'll coordinate)
   2. ❌ Continue sequential (I'll do all 7 one-by-one)
   3. ❓ Discuss approach
   ```

3. **Handle user response:**
   - **Option 1 (Enable):** Proceed to group-based S2 workflow
   - **Option 2 (Sequential):** Standard sequential S2 (no parallelization)
   - **Option 3 (Discuss):** Answer questions, clarify groups, re-present

---

### Phase 3: S1 Completion - Transition to S2

**Step 6: Transition to S2**

**When:** S1 complete, ready to start S2

**Agent Actions:**

**Scenario A: Group-Based Parallel S2**

```markdown
✅ S1 Complete! Transitioning to S2 with group-based parallelization.

**Workflow:**
1. Starting with Group 1 (Feature 01)
2. I'll complete S2 for Feature 01 first (S2.P1 + S2.P2)
3. After Group 1 S2 complete → I'll spawn 6 secondary agents
4. Group 2 (Features 02-07) will do S2 in parallel
5. After all S2 complete → I'll run S3

**Next Action:** Beginning S2.P1 for Feature 01 (Group 1)
```

**Scenario B: Sequential S2**

```markdown
✅ S1 Complete! Transitioning to S2 (sequential mode).

**Workflow:**
1. Feature 01 S2 (2 hours)
2. Feature 02 S2 (2 hours)
3. [Continue for all 7 features...]

**Next Action:** Beginning S2.P1 for Feature 01
```

---

### Phase 4: S2 Execution - Group 1 (Wave 1)

**Who:** Primary agent (solo)

**Steps:**

1. **Execute S2.P1 for Feature 01:**
   - Read S2.P1 guide
   - Complete research phase
   - Update Feature 01 README.md Agent Status
   - Update EPIC_README.md progress

2. **Execute S2.P2 for Feature 01:**
   - Read S2.P2 guide
   - Write spec.md with traceability
   - Create checklist.md
   - Resolve questions with user (Gate 3)
   - Complete S2 for Feature 01

3. **Mark Group 1 Complete:**
   ```markdown
   ## EPIC_README.md Update

   **Group 1 S2 Status:** ✅ COMPLETE
   - Feature 01: S2 complete at 2026-02-06 14:30

   **Group 2 S2 Status:** ⏳ READY TO START
   - Features 02-07: Waiting for secondary agents

   **Next Action:** Generate handoff packages for Group 2 (6 secondary agents)
   ```

---

### Phase 5: S2 Execution - Group 2 Handoff (Wave 2 Prep)

**Who:** Primary agent

**Steps:**

1. **Generate handoff packages for Group 2:**
   ```bash
   # Create handoff packages for 6 features (02-07)
   generate_handoff_for_secondary_a  # Feature 02
   generate_handoff_for_secondary_b  # Feature 03
   generate_handoff_for_secondary_c  # Feature 04
   generate_handoff_for_secondary_d  # Feature 05
   generate_handoff_for_secondary_e  # Feature 06
   generate_handoff_for_secondary_f  # Feature 07
   ```

2. **Present handoff packages to user:**
   ```markdown
   🚀 Group 1 complete! Ready to spawn Group 2 secondary agents.

   **Group 1 Results:**
   - Feature 01 S2: Complete ✅
   - Time: 2 hours

   **Group 2 Setup:**
   - 6 secondary agents needed (one per feature)
   - All 6 will do S2 simultaneously
   - Estimated time: 2 hours (parallel)

   **Instructions:**
   Please open 6 new Claude Code sessions and paste these handoff packages:

   [Handoff package for Secondary-A (Feature 02)]
   [Handoff package for Secondary-B (Feature 03)]
   [Handoff package for Secondary-C (Feature 04)]
   [Handoff package for Secondary-D (Feature 05)]
   [Handoff package for Secondary-E (Feature 06)]
   [Handoff package for Secondary-F (Feature 07)]
   ```

3. **Wait for secondary agents to start:**
   - Monitor agent_checkpoints/ for startup signals
   - Verify all 6 secondaries initialized
   - Proceed to coordination phase

---

### Phase 6: S2 Execution - Group 2 Parallel Work (Wave 2)

**Who:** Primary agent (coordinator) + 6 secondary agents (workers)

**Primary Agent Responsibilities:**

1. **Monitor secondary agents (every 15 min):**
   - Check inboxes for escalations
   - Check STATUS files for blockers
   - Check checkpoints for staleness
   - Respond to escalations within 15 min

2. **Update sync status:**
   ```markdown
   ## Sync Status (EPIC_README.md)

   **Current Wave:** Group 2 (Features 02-07)
   **Status:** IN PROGRESS (6 agents working)

   | Feature | Agent | S2.P1 Status | S2.P2 Status |
   |---------|-------|--------------|--------------|
   | 02 | Secondary-A | ✅ Complete | 🔄 In Progress |
   | 03 | Secondary-B | 🔄 In Progress | ⏳ Not Started |
   | 04 | Secondary-C | ✅ Complete | ✅ Complete |
   | 05 | Secondary-D | 🔄 In Progress | ⏳ Not Started |
   | 06 | Secondary-E | ✅ Complete | 🔄 In Progress |
   | 07 | Secondary-F | 🔄 In Progress | ⏳ Not Started |
   ```

3. **Handle escalations:**
   - Secondary asks user question → Primary asks user → responds to secondary
   - Secondary blocked → Primary investigates → provides guidance
   - Secondary stale → Primary sends warning → escalates if needed

**Secondary Agent Responsibilities:**

1. **Execute S2.P1 for assigned feature:**
   - Follow S2 secondary agent guide
   - Complete research, spec, checklist
   - Update checkpoints every 15 min
   - Escalate to Primary if blocked

2. **Complete S2.P2:**
   - Mark READY_FOR_SYNC in STATUS file
   - Wait for Primary to run S2.P2 (cross-feature alignment)
   - DO NOT proceed to S3

---

### Phase 7: S2 Completion - All Groups Done

**Who:** Primary agent (solo)

**Steps:**

1. **Verify all features complete S2:**
   ```bash
   # Check all STATUS files
   grep "STAGE: S2.P2" feature_*/STATUS
   grep "READY_FOR_SYNC: true" feature_*/STATUS

   # Expected output:
   # feature_01/STATUS:STAGE: S2.P2
   # feature_01/STATUS:READY_FOR_SYNC: true
   # feature_02/STATUS:STAGE: S2.P2
   # feature_02/STATUS:READY_FOR_SYNC: true
   # [... for all 7 features]
   ```

2. **Run S2.P2 (Cross-Feature Alignment) for ALL features:**
   - Read S2.P2 guide
   - Pairwise comparison of all 7 specs
   - Check for conflicts, overlaps, gaps
   - Update specs if needed
   - Validation Loop (3 consecutive clean rounds)

3. **Mark S2 Complete:**
   ```markdown
   ## EPIC_README.md Update

   **S2 Status:** ✅ COMPLETE (all features)

   **Group 1 Results:**
   - Feature 01: Completed 2026-02-06 14:30

   **Group 2 Results:**
   - Feature 02: Completed 2026-02-06 16:15
   - Feature 03: Completed 2026-02-06 16:20
   - Feature 04: Completed 2026-02-06 16:10
   - Feature 05: Completed 2026-02-06 16:25
   - Feature 06: Completed 2026-02-06 16:18
   - Feature 07: Completed 2026-02-06 16:22

   **Total S2 Time:** 4 hours (from 12:30 to 16:30)
   **Time Saved:** 10 hours (vs 14 hours sequential)

   **Next Stage:** S3 (Cross-Feature Sanity Check)
   ```

4. **Notify user and secondary agents:**
   - User: S2 complete, proceeding to S3
   - Secondaries: S2 complete, you can close sessions or wait

---

### Phase 8: S3+ Execution - Groups No Longer Matter

**Who:** Primary agent (solo)

**Key Point:** After S2 complete, groups are irrelevant. Workflow continues normally:

- **S3:** Epic-level (all features together) - sanity check, testing strategy
- **S4:** Per-feature sequential (no groups) - test planning
- **S5-S8:** Per-feature sequential (no groups) - implementation
- **S9-S10:** Epic-level (all features together) - QC and cleanup

**Groups exist ONLY for S2 parallelization waves.**

---

## Guide Gaps Identified

### Gap 1: S1 Step 5.7.5 - Feature Dependency Analysis

**Location:** `feature-updates/guides_v2/stages/s1/s1_epic_planning.md` (Line 576-603)

**Current Content:**
```markdown
### Step 5.7.5: Analyze Feature Dependencies

**For EACH feature:**
1. **Spec Dependencies:** Does this feature need other features' specs to write its own?
2. **Implementation Dependencies:** Does this feature need other features' code before implementation?

**Workflow:** Each group completes full S2->S3->S4 cycle before next group starts
```

**Problem:**
- ❌ Line 600 says "full S2->S3->S4 cycle" (WRONG)
- ❌ Doesn't explain what spec-level dependencies mean for S2
- ❌ Doesn't explain group-based S2 waves
- ❌ Doesn't clarify when groups matter vs don't matter

**Required Fix:**
```markdown
### Step 5.7.5: Analyze Feature Dependencies

**Purpose:** Identify spec-level dependencies to determine S2 wave order

**For EACH feature:**
1. **Spec Dependencies (matters for S2):**
   - Does this feature need other features' SPECS to write its own spec?
   - Example: Feature B needs to know Feature A's API to write integration spec
   - → Creates S2 dependency (Feature A must complete S2 before Feature B starts)

2. **Implementation Dependencies (matters for S5-S8, NOT S2):**
   - Does this feature need other features' CODE to build its implementation?
   - Example: Feature B calls Feature A's functions
   - → Creates S5 dependency (Feature A must complete S5-S8 before Feature B starts)

**Organize into Groups:**

**Group 1 (Foundation):**
- Features with NO spec-level dependencies
- Can research and specify independently
- Will complete S2 first

**Group 2 (Dependent on Group 1):**
- Features that need Group 1's specs as reference
- Must wait for Group 1 to complete S2
- Will do S2 in parallel with each other once Group 1 done

**Group 3+ (if needed):**
- Features that need Group 2's specs
- Continue wave pattern

**Document in EPIC_README.md:**

```markdown
## Feature Dependency Groups (S2 Only)

**Group 1 (Foundation - S2 Wave 1):**
- Feature 01: {name}
- Spec Dependencies: None
- S2 Workflow: Completes S2 alone FIRST

**Group 2 (Dependent - S2 Wave 2):**
- Features 02-07: {names}
- Spec Dependencies: Need Group 1's spec (API reference)
- S2 Workflow: After Group 1 completes S2, all features do S2 in parallel

**After S2:**
- Groups no longer matter
- S3: Epic-level (all features together)
- S4: Per-feature sequential
- S5-S8: Per-feature sequential (implementation dependencies checked separately)
- S9-S10: Epic-level

**S2 Time Savings:**
- Sequential S2: {N} features × 2h = {total}h
- Group-based S2: Wave 1 ({M}h) + Wave 2 parallel ({M}h) = {total}h
- Savings: {X}h ({percent}% reduction)
```

**Decision Criteria:**
- **Spec-level dependency → Different group** (affects S2 parallelization)
- **Implementation dependency only → Same group** (doesn't affect S2)
- **No dependencies → Group 1** (can parallelize freely)

**If all features independent:** Note "All features independent - Single S2 wave"
```

**Priority:** HIGH - This is the foundation for group-based parallelization

---

### Gap 2: S1 Step 5.9 - Parallelization Offering Template

**Location:** `feature-updates/guides_v2/stages/s1/s1_epic_planning.md` (Line 646-676)

**Current Content:**
```markdown
**Sequential:** {N} features x 2 hours S2 each = {total} hours
**Parallel:** All {N} features simultaneously = 2 hours
**Savings:** {savings} hours ({percent}% reduction)

**Coordination:** You'll open {N-1} additional sessions, I'll coordinate via files
```

**Problem:**
- ❌ Assumes all features parallelize simultaneously (ignores groups)
- ❌ Doesn't explain group-based wave sequencing
- ❌ Doesn't mention when Group 2 starts (after Group 1 done)

**Required Fix:**
```markdown
### Offering Template (Group-Based Parallel)

**Use when:** Epic has dependency groups

```markdown
🚀 PARALLEL WORK OPPORTUNITY

I've identified {N} features organized into {M} dependency groups:

**Group 1 (Foundation):**
- Feature {X}: {name}
- No dependencies, completes S2 first

**Group 2 (Dependent):**
- Features {Y}-{Z}: {names}
- Depend on Group 1's spec (need API reference)
- Can parallelize with each other once Group 1 done

**Sequential approach:**
- All {N} features one-by-one: {total} hours

**Group-based parallel approach:**
- Group 1 completes S2: {M} hours
- Group 2 does S2 in parallel ({K} features): {M} hours
- Total: {total} hours

**TIME SAVINGS: {X} hours ({percent}% reduction in S2 time)**

**Workflow:**
1. I complete S2 for Group 1 (Feature {X})
2. After Group 1 done → I spawn {K} secondary agents for Group 2
3. All {K} Group 2 features do S2 simultaneously
4. After all S2 complete → I run S3 (epic-level)

**Coordination:**
- You'll open {K} additional Claude Code sessions (when Group 1 done)
- I'll coordinate all agents via files
- Group 1 completes before Group 2 starts (dependency requirement)

Would you like to:
1. ✅ Enable group-based parallel work (I'll coordinate)
2. ❌ Continue sequential (I'll do all {N} one-by-one)
3. ❓ Discuss approach
```

### Offering Template (No Groups - All Independent)

**Use when:** All features have no dependencies

```markdown
🚀 PARALLEL WORK OPPORTUNITY

I've identified {N} features with no dependencies - all can parallelize!

**Sequential approach:**
- All {N} features one-by-one: {total} hours

**Parallel approach:**
- All {N} features simultaneously: 2 hours

**TIME SAVINGS: {X} hours ({percent}% reduction in S2 time)**

**Workflow:**
1. I spawn {N-1} secondary agents immediately
2. I work on Feature 01, secondaries work on Features 02-{N}
3. All {N} features do S2 simultaneously
4. After all S2 complete → I run S3 (epic-level)

**Coordination:**
- You'll open {N-1} additional Claude Code sessions
- I'll coordinate all agents via files

Would you like to:
1. ✅ Enable parallel work (I'll coordinate)
2. ❌ Continue sequential (I'll do all {N} one-by-one)
3. ❓ Discuss approach
```
```

**Priority:** HIGH - User-facing communication about groups

---

### Gap 3: S1 Step 6 - Transition to S2 with Groups

**Location:** `feature-updates/guides_v2/stages/s1/s1_epic_planning.md` (Line 677-695)

**Current Content:**
```markdown
### Step 6.2: Update Agent Status for S2

Update Agent Status: Current Phase "DEEP_DIVE", Current Guide "stages/s2/s2_p1_research.md", Next Action "Read S2.P1 guide and begin research for feature_01_{name}".
```

**Problem:**
- ❌ Doesn't handle group-based transition logic
- ❌ No instructions for which group starts first
- ❌ No mention of when to spawn secondaries (after Group 1 vs immediately)

**Required Fix:**
```markdown
### Step 6.2: Update Agent Status for S2

**Determine S2 Workflow:**

**Scenario A: Group-Based Parallel S2** (epic has dependency groups)
- Update Agent Status:
  - Current Phase: "DEEP_DIVE_GROUP_1"
  - Current Guide: "stages/s2/s2_p1_spec_creation_refinement.md"
  - Next Action: "Read S2.P1 guide and begin research for Feature {X} (Group 1)"
  - Groups: "Group 1 first, Group 2 after Group 1 S2 complete"

**Scenario B: All Features Independent Parallel** (no dependency groups)
- Skip to parallel work setup (generate handoffs immediately)
- Follow: `parallel_work/s2_primary_agent_guide.md`

**Scenario C: Sequential S2** (user declined parallel work)
- Update Agent Status:
  - Current Phase: "DEEP_DIVE"
  - Current Guide: "stages/s2/s2_p1_spec_creation_refinement.md"
  - Next Action: "Read S2.P1 guide and begin research for feature_01_{name}"

### Step 6.3: Announce Transition to User

**For Group-Based Parallel:**
```markdown
✅ S1 Complete! Transitioning to S2 with group-based parallelization.

**Groups:**
- Group 1 (Foundation): Feature {X}
- Group 2 (Dependent): Features {Y}-{Z}

**Workflow:**
1. Starting with Group 1 (Feature {X})
2. I'll complete S2 for Feature {X} first (S2.P1 + S2.P2)
3. After Group 1 S2 complete → I'll spawn {K} secondary agents
4. Group 2 ({K} features) will do S2 in parallel
5. After all S2 complete → I'll run S3

**Estimated Time:**
- Group 1 S2: 2 hours
- Group 2 S2 (parallel): 2 hours
- Total: 4 hours (vs {X} hours sequential)

**Next Action:** Beginning S2.P1 for Feature {X} (Group 1)
```

**For All Independent Parallel:**
```markdown
✅ S1 Complete! Transitioning to S2 with full parallelization.

**All {N} features are independent - can parallelize immediately!**

I'll now generate handoff packages for {N-1} secondary agents...
```

**For Sequential:**
```markdown
✅ S1 Complete! Transitioning to S2 (sequential mode).

I'll work through all {N} features one-by-one, starting with Feature 01.

**Next Action:** Beginning S2.P1 for Feature 01
```
```

**Priority:** HIGH - Critical workflow transition point

---

### Gap 4: S2 Router Guide - Group Wave Check

**Location:** `feature-updates/guides_v2/stages/s2/s2_feature_deep_dive.md` (Line 35-81)

**Current Content:**
```markdown
## 🔀 Parallel Work Check (FIRST PRIORITY)

### Are You a Secondary Agent?
[Standard secondary agent check...]

### Are You Primary Agent in Parallel Mode?
[Standard primary agent check...]

### Are You in Sequential Mode?
[Standard sequential check...]
```

**Problem:**
- ❌ Doesn't check for group-based parallelization
- ❌ No mention of wave sequencing
- ❌ Assumes all features parallelize simultaneously

**Required Fix:**
```markdown
## 🔀 Parallel Work Check (FIRST PRIORITY)

**Before proceeding with S2 phases, check your mode:**

### Are You a Secondary Agent?

[Existing content stays the same...]

### Are You Primary Agent in Group-Based Parallel Mode?

**Check for group-based parallelization:**
- EPIC_README.md has "Feature Dependency Groups (S2 Only)" section
- Multiple dependency groups documented (Group 1, Group 2, etc.)
- Currently working on Group N features

**If Group-Based Parallel:**

**→ Go to:** `parallel_work/s2_primary_agent_group_wave_guide.md` (NEW GUIDE)

**Group Wave Workflow:**
1. Complete S2 for Group 1 features first
2. After Group 1 S2 complete → generate handoffs for Group 2
3. Coordinate Group 2 parallel work
4. After all groups complete S2 → run S2.P2 (cross-feature alignment)
5. Proceed to S3

**Within each group:** Follow standard parallel coordination

### Are You Primary Agent in Full Parallel Mode?

**Check for full parallelization (no groups):**
- All features independent (no spec-level dependencies)
- OR EPIC_README.md says "All features independent - Single S2 wave"
- Generated handoffs for all features immediately

**→ Go to:** `parallel_work/s2_primary_agent_guide.md`

[Existing primary agent content...]

### Are You in Sequential Mode?

[Existing content stays the same...]
```

**New Guide Needed:** `parallel_work/s2_primary_agent_group_wave_guide.md`

**Priority:** HIGH - Entry point for S2 execution

---

### Gap 5: S2 Primary Agent Guide - Group Wave Management

**Location:** `feature-updates/guides_v2/parallel_work/s2_primary_agent_guide.md`

**Current Content:**
- Only covers single-wave parallelization (all features simultaneously)
- No mention of dependency groups
- No wave sequencing protocol

**Required Addition:**

**New Section (after Phase 1):**

```markdown
## Phase 2: Determine Parallelization Mode

**Check EPIC_README.md for groups:**

### Mode A: Group-Based Parallelization

**If:** EPIC_README.md has "Feature Dependency Groups (S2 Only)" section with multiple groups

**Then:** Follow group wave workflow:

1. **Wave 1: Group 1 (Foundation)**
   - Complete S2 for all Group 1 features FIRST
   - Solo work (no secondaries yet)
   - Update EPIC_README.md: "Group 1 S2 Status: ✅ COMPLETE"

2. **Wave 2: Group 2 (Dependent)**
   - After Group 1 complete → generate handoffs for Group 2
   - Spawn secondary agents for all Group 2 features
   - Coordinate Group 2 parallel work
   - Follow standard coordination protocols

3. **Wave 3+: Additional Groups (if any)**
   - Repeat wave pattern for each group
   - Each wave waits for previous wave to complete S2

4. **After All Waves Complete:**
   - Run S2.P2 (cross-feature alignment) across ALL features
   - Proceed to S3

**See:** `parallel_work/s2_primary_agent_group_wave_guide.md` for detailed workflow

### Mode B: Full Parallelization (No Groups)

**If:** All features independent OR EPIC_README.md says "Single S2 wave"

**Then:** Follow standard parallel workflow:
- Generate handoffs for all features immediately
- All features do S2 simultaneously
- No wave sequencing needed

**See:** Rest of this guide (s2_primary_agent_guide.md)
```

**Priority:** HIGH - Primary agent workflow split point

---

### Gap 6: NEW GUIDE NEEDED - Group Wave Management

**New Guide:** `feature-updates/guides_v2/parallel_work/s2_primary_agent_group_wave_guide.md`

**Purpose:** Detailed workflow for Primary agent managing group-based S2 waves

**Required Sections:**

1. **Overview:**
   - What group-based parallelization means
   - When to use this guide
   - Wave sequencing concept

2. **Wave 1: Foundation Group:**
   - Execute S2 for all Group 1 features (solo)
   - Complete S2.P1 + S2.P2 for Group 1
   - Mark Group 1 complete in EPIC_README.md
   - Verify Group 1 specs are ready for Group 2 reference

3. **Wave Transition: Group 1 → Group 2:**
   - Generate handoff packages for Group 2 features
   - Present handoffs to user
   - Wait for secondary agents to start
   - Initialize coordination infrastructure

4. **Wave 2: Dependent Group:**
   - Coordinate Group 2 parallel work
   - Monitor secondary agents
   - Handle escalations
   - Run S2.P2 after all Group 2 complete S2.P1

5. **Additional Waves (if needed):**
   - Repeat wave pattern for Group 3+
   - Each wave waits for previous wave S2 completion

6. **Wave Completion:**
   - All groups complete S2
   - Run S2.P2 across ALL features
   - Proceed to S3

**Priority:** CRITICAL - Missing guide blocks group-based parallelization

---

### Gap 7: S2 Secondary Agent Guide - No Group Awareness

**Location:** `feature-updates/guides_v2/parallel_work/s2_secondary_agent_guide.md`

**Current Content:**
- Secondary agents execute S2 for assigned feature
- No awareness of which group they belong to
- No information about dependency groups

**Problem:**
- ❌ Secondaries don't know they're in Group 2 (dependent on Group 1)
- ❌ Can't explain to user why they started after Group 1

**Required Fix:**

**Add to handoff package template:**

```markdown
## Handoff Package for Secondary Agent {ID}

**Feature Assignment:** Feature {N}: {name}
**Dependency Group:** Group {M}
**Group Dependencies:** Group {M} depends on Group {M-1} completing S2 first

**Why You're Starting Now:**
- Group {M-1} has completed S2
- Group {M-1}'s specs are available for reference (see: feature_{X}/spec.md)
- Your feature can now be specified with knowledge of Group {M-1}'s APIs

**Your Task:**
1. Execute S2.P1 for Feature {N}
2. Reference Group {M-1} specs as needed (file paths: feature_{X}/spec.md)
3. Mark complete and wait for Primary to run S2.P2
```

**Priority:** MEDIUM - Improves secondary agent understanding, not blocking

---

### Gap 8: Decision Tree Guide - Missing

**New Guide Needed:** `feature-updates/guides_v2/reference/s2_parallelization_decision_tree.md`

**Purpose:** Help agents decide parallelization mode based on dependencies

**Required Sections:**

1. **Decision Tree Flowchart:**
   ```
   START: Features created in S1
      ↓
   Q: Does epic have 3+ features?
      NO → Sequential S2 (no parallelization)
      YES → Continue
      ↓
   Q: User accepted parallel work offering?
      NO → Sequential S2
      YES → Continue
      ↓
   Q: Do any features have spec-level dependencies?
      NO → Full Parallelization (all features simultaneously)
      YES → Group-Based Parallelization
      ↓
   Group-Based Parallelization:
      - Organize features into dependency groups
      - Each group completes S2 before next group starts
      - Within each group: features parallelize with each other
   ```

2. **Dependency Type Identification:**
   - What is a spec-level dependency? (Feature B needs Feature A's spec to write its own)
   - What is an implementation dependency? (Feature B calls Feature A's code)
   - Which type affects S2 parallelization? (Spec-level only)

3. **Group Assignment Examples:**
   - Example 1: All independent features (Single wave)
   - Example 2: Foundation + dependent features (2 waves)
   - Example 3: Cascading dependencies (3+ waves)

4. **Common Mistakes:**
   - Confusing implementation dependencies with spec-level dependencies
   - Assuming all features can parallelize (ignoring dependencies)
   - Creating unnecessary groups (over-splitting)

**Priority:** MEDIUM - Reference guide for complex cases

---

## Summary of Required Changes

### Critical Priority (Blocking Group-Based Parallelization):

1. **S1 Line 600 correction:** Change "S2->S3->S4 cycle" to "S2 only"
2. **S1 Step 5.7.5 expansion:** Add group-based dependency analysis workflow
3. **S1 Step 5.9 expansion:** Add group-based parallelization offering template
4. **S1 Step 6 expansion:** Add group-based S2 transition logic
5. **S2 Router Guide update:** Add group wave check and routing
6. **NEW GUIDE:** `s2_primary_agent_group_wave_guide.md` (group wave management)

### High Priority (Improves Understanding):

7. **S2 Primary Agent Guide update:** Add parallelization mode determination
8. **S2 Secondary Agent Guide update:** Add group awareness to handoff packages

### Medium Priority (Reference/Documentation):

9. **NEW GUIDE:** `s2_parallelization_decision_tree.md` (decision framework)
10. **CLAUDE.md update:** Add group-based parallelization summary to S2 section

---

## Testing the Intended Flow

**Test Case: KAI-8 Logging Epic (Current)**

**Features:**
- Feature 01: core_logging_infrastructure (foundation)
- Features 02-07: Script-specific logging (dependent on 01)

**Expected Flow:**
1. S1 identifies 2 groups (Group 1: F01, Group 2: F02-07)
2. S1 offers group-based parallel work (save 10 hours)
3. User accepts
4. S2 Wave 1: Primary completes S2 for Feature 01 (2 hours)
5. Primary generates 6 handoff packages for Features 02-07
6. User spawns 6 secondary agents
7. S2 Wave 2: All 6 Group 2 features do S2 in parallel (2 hours)
8. Primary runs S2.P2 across all 7 features (20 min)
9. Primary proceeds to S3 (groups no longer matter)

**Actual Flow (Without Guide Updates):**
- S1 Step 5.7.5 says "S2->S3->S4 cycle" (WRONG)
- Agent proposes parallel work for all 7 simultaneously (WRONG)
- User catches error and corrects agent
- Agent confused about group workflow

**With Guide Updates:**
- S1 Step 5.7.5 correctly identifies 2 groups and S2-only scope
- S1 Step 5.9 offers group-based parallelization with correct workflow
- S2 Router guides Primary to group wave guide
- Group wave guide orchestrates Wave 1 → Wave 2 → S2.P2 → S3
- Flow completes correctly without user intervention

---

## Conclusion

The intended group-based S2 parallelization flow is well-defined but not documented in the guides. The gaps identified prevent agents from properly executing this flow without user intervention.

**Immediate Action Items:**
1. Fix S1 Line 600 (5 minutes)
2. Expand S1 Steps 5.7.5, 5.9, and 6 (30 minutes)
3. Create `s2_primary_agent_group_wave_guide.md` (2 hours)
4. Update S2 Router Guide (20 minutes)
5. Update S2 Primary Agent Guide parallelization section (30 minutes)

**Total Estimated Time:** ~3.5 hours to fully document group-based parallelization

**Impact:** Enables agents to correctly handle dependency-based S2 parallelization without user intervention, saving 10+ hours per epic with dependency groups.
