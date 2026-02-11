# S2 Primary Agent Guide (Parallel Work)

**Purpose:** Guide for Primary agent coordinating parallel S2 work

**Role:** Coordinator + Feature 01 owner

**Stages:** S1 (solo) → S2 (parallel) → S3 (solo) → S4 (solo)

---

## Overview

When S2 parallelization is enabled, the Primary agent has **dual responsibilities**:

1. **Coordinator:** Manage parallel work, generate handoffs, monitor secondaries, handle escalations
2. **Feature 01 Owner:** Complete S2 for Feature 01 (in parallel with secondaries)

**Time Distribution:**
- 85% Feature 01 work (your S2 implementation)
- 15% Coordination (handoffs, monitoring, escalations)

**Key Principle:** Choose the **simplest/smallest feature** as Feature 01 to minimize your workload and maximize coordination capacity.

---

## Workflow Overview

```text
S1 (Solo) → Offer Parallel Work → Generate Handoffs → S2 (Parallel) → S3 (Solo) → S4 (Solo)
    ↓                                                       ↓
Feature Analysis                                    Monitor + Coordinate
Dependency Detection                                Handle Escalations
Wave Assignment                                     Run S3 when all complete
```

---

## Phase 1: S1 Epic Planning (Solo)

**Standard S1 workflow, but add:**

### Step: Analyze Features for Parallelization

**After creating all feature folders:**

1. **Count features:**
   ```bash
   FEATURE_COUNT=$(ls -d feature_* | wc -l)
   echo "Total features: $FEATURE_COUNT"
   ```

2. **Assess parallelization benefit:**
   - 2 features: Modest benefit (save 2 hours)
   - 3 features: Good benefit (save 4 hours)
   - 4+ features: High benefit (save 6+ hours)

3. **Analyze dependencies:**
   - Read epic user request
   - Identify feature dependencies
   - Determine if features can run in parallel

   **Example:**
   ```text
   Feature 01: Player JSON integration (no dependencies)
   Feature 02: Team penalty scoring (depends on Feature 01)
   Feature 03: Scoring algorithm update (no dependencies)

   Decision: Features 01 and 03 can parallelize
            Feature 02 must wait (Wave 2)
   ```

4. **Document decision:**
   ```markdown
   ## Parallel Work Assessment

   **Total Features:** 3
   **Independent Features:** 2 (Feature 01, Feature 03)
   **Dependent Features:** 1 (Feature 02 depends on Feature 01)

   **Parallelization Strategy:**
   - S2 parallelization: YES (3 features, save ~4 hours)
   - Features 01 and 03: Parallel in S2
   - Feature 02: Sequential (depends on Feature 01 for implementation)
   - Note: All features CAN do S2 in parallel (spec-level only)
   ```

---

## Phase 2: Determine Parallelization Mode

**After S1 complete, check EPIC_README.md for dependency groups:**

### Mode A: Group-Based Parallelization

**Check for group-based mode indicators:**
- EPIC_README.md has "Feature Dependency Groups (S2 Only)" section
- Multiple dependency groups documented (Group 1, Group 2, etc.)
- Groups organized by spec-level dependencies

**If group-based mode detected:**

**→ Stop here and switch to:** `parallel_work/s2_primary_agent_group_wave_guide.md`

**That guide handles:**
- Wave 1: Execute S2 for Group 1 features (solo or parallel within group)
- Wave Transition: Generate handoffs for Group 2 after Group 1 S2 complete
- Wave 2: Coordinate Group 2 parallel work
- Additional Waves: Repeat for Group 3+ if needed
- Wave Completion: Final S2.P2 across ALL features, transition to S3

**Do NOT continue with this guide** if you're in group-based mode. This guide assumes all features can parallelize simultaneously (no dependency groups).

---

### Mode B: Full Parallelization (No Groups)

**Check for full parallelization indicators:**
- All features independent (no spec-level dependencies)
- OR EPIC_README.md says "All features independent - Single S2 wave"
- OR EPIC_README.md has "Feature Dependency Groups (S2 Only)" section with ONLY Group 1

**If full parallelization mode confirmed:**

**→ Continue with this guide** (rest of the phases below)

**This guide handles:**
- Generate handoffs for all features immediately (no waves)
- All features execute S2 in parallel simultaneously
- Coordinate all secondary agents together
- Run S2.P2 after all features complete
- Transition to S3

---

## Phase 3: Offer Parallel Work to User

**After S1 complete and Mode B (full parallelization) confirmed:**

### Step 1: Prepare Offering Message

**Calculate time savings:**
```text
Sequential S2:
- Feature 01: 2 hours
- Feature 02: 2 hours
- Feature 03: 2 hours
Total: 6 hours

Parallel S2:
- All 3 features: 2 hours (max of 2, 2, 2)
Total: 2 hours

TIME SAVINGS: 4 hours (67% reduction in S2 time)
```

### Step 2: Present Offering

**Use template from `prompts_reference_v2.md`:**

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

### Step 3: Handle User Response

**If user chooses Option 1 (Enable parallel work):**
- Proceed to Phase 3 (Generate Handoffs)

**If user chooses Option 2 (Sequential):**
- Continue with standard sequential S2 workflow
- No parallelization

**If user chooses Option 3 (Discuss):**
- Answer questions about:
  - How parallelization works
  - What user needs to do
  - Time savings calculation
  - Coordination overhead
- Re-present offering after discussion

---

## Phase 4: Generate Handoff Packages

**When user accepts parallel work:**

### Step 1: Create Coordination Infrastructure (Primary Only)

**🚨 CRITICAL:** Primary agent creates ALL coordination infrastructure. Secondaries ONLY create their own checkpoint/STATUS files.

```bash
# Create ALL coordination directories (Primary only)
mkdir -p .epic_locks
mkdir -p agent_comms
mkdir -p agent_checkpoints

echo "✅ Coordination infrastructure created (Primary)"
```

**Rules:**
- ✅ Primary creates directories
- ✅ Secondaries create FILES (their checkpoint.json and STATUS)
- ❌ DO NOT create subdirectories under agent_comms/ or agent_checkpoints/
- ❌ DO NOT create parallel_work/ or agent_comms/inboxes/ or agent_comms/coordination/

### Step 1.5: Validate Structure

```bash
# Run validation script to ensure structure is correct
bash feature-updates/guides_v2/parallel_work/scripts/validate_structure.sh .

# Expected output: ✅ PASSED - structure valid
# If errors found, fix before proceeding
```

### Step 1.6: Create Your Own STATUS File

**🚨 CRITICAL:** Feature 01 (Primary's feature) needs a STATUS file too.

```bash
# Create STATUS file for Feature 01
cat > "feature_01_{name}/STATUS" <<EOF
STAGE: S2.P1
PHASE: Research Phase
AGENT: Primary
AGENT_ID: $(uuidgen)
UPDATED: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
STATUS: IN_PROGRESS
BLOCKERS: none
NEXT_ACTION: Begin S2.P1 Research Phase
READY_FOR_SYNC: false
ESTIMATED_COMPLETION: $(date -u -d "+2 hours" +"%Y-%m-%dT%H:%M:%SZ")
EOF

echo "✅ STATUS file created for Feature 01"
```

**Rule:** ALL features need STATUS files, including Feature 01 (Primary's feature).

### Step 2: Determine Secondary Agent Assignments

**For 3-feature epic:**
- Primary: Feature 01
- Secondary-A: Feature 02
- Secondary-B: Feature 03

**Secondary Agent IDs:**
- Use alphabetical: Secondary-A, Secondary-B, Secondary-C, etc.
- Lowercase for filenames: secondary_a, secondary_b, etc.

### Step 3: Generate and Save Handoff Packages

**Use template from `templates/handoff_package_s2_template.md`:**

**For each secondary feature:**

1. Generate handoff content
2. **Save to feature folder** (not agent_comms/)
3. Present simplified startup instruction to user

**Example for 3-feature epic:**

```bash
# For Secondary-A (Feature 02)
# Generate handoff content (use template)
# Then save to feature folder:
cat > "feature_02_{name}/HANDOFF_PACKAGE.md" <<EOF
═══════════════════════════════════════════════════════════
HANDOFF PACKAGE - Secondary Agent A
═══════════════════════════════════════════════════════════

**Epic:** KAI-6-nfl_team_penalty
**Feature Assignment:** feature_02_team_penalty
**Primary Agent ID:** Agent-Primary-abc123
**Your Agent ID:** Secondary-A
**Starting Stage:** S2.P1 (Feature Deep Dive - Research Phase)

[... full handoff content from template ...]
EOF

# For Secondary-B (Feature 03)
cat > "feature_03_{name}/HANDOFF_PACKAGE.md" <<EOF
[... handoff content for Secondary-B ...]
EOF

echo "✅ Handoff packages saved to feature folders"
```

**Rule:** Handoff packages saved in feature folders, NOT in `agent_comms/`.

**Benefit:** Secondary agents can find them automatically by reading `feature_XX_{name}/HANDOFF_PACKAGE.md`

### Step 4: Present Simplified Startup Instructions to User

**NEW SIMPLIFIED PROCESS:** Handoff packages are pre-saved in feature folders. User just spawns agents with one-line instructions.

```markdown
Great! I'll set up parallel work for S2.

📋 SETUP INSTRUCTIONS

You'll need to open 2 new Claude Code sessions (one for each secondary agent).

**For each new session:**
1. Open a new terminal/window
2. Navigate to the project: cd /path/to/project
3. Start Claude Code in the new window
4. Enter the one-line startup command below

---

🚀 SECONDARY AGENT A STARTUP

In NEW Claude Code session #1, enter:

```text
You are a secondary agent for Feature 02
```

The agent will automatically read `feature_02_{name}/HANDOFF_PACKAGE.md` and self-configure.

---

🚀 SECONDARY AGENT B STARTUP

In NEW Claude Code session #2, enter:

```text
You are a secondary agent for Feature 03
```text

The agent will automatically read `feature_03_{name}/HANDOFF_PACKAGE.md` and self-configure.

---

**Benefits:**
- ✅ No copy-paste errors
- ✅ Scalable (works for 2 or 20 features)
- ✅ Consistent startup for all secondaries
- ✅ Handoff packages stored in feature folders for audit trail

**After secondary agents start:**
- They'll self-configure and begin S2
- I'll monitor their progress via STATUS files and checkpoints
- All agents will work on S2 simultaneously
- When all complete S2, I'll run S3

Ready to start? Please enter the startup commands in the new sessions.
```

### Step 5: Wait for Secondary Agents to Start

**Monitor for secondary agent startup:**

```bash
# Check if secondary agents created checkpoints
while true; do
  if [ -f agent_checkpoints/secondary_a.json ] && \
     [ -f agent_checkpoints/secondary_b.json ]; then
    echo "Both secondary agents started!"
    break
  fi
  echo "Waiting for secondary agents to start..."
  sleep 5
done
```

**Once both started:**
- Proceed to Phase 4 (Parallel S2 Work)

---

## Phase 5: Parallel S2 Work

**You now have dual responsibilities:**

### Responsibility 1: Feature 01 Implementation

**Work on your feature (S2.P1 → S2.P2 → S2.P3):**

1. **Execute S2.P1 for Feature 01:**
   - Follow guide: `stages/s2/s2_p1_spec_creation_refinement.md`
   - Complete research phase
   - Update checkpoint every 15 min
   - Update EPIC_README.md progress section
   - Update STATUS file

2. **Execute S2.P2 for Feature 01:**
   - Follow guide: `stages/s2/s2_p2_specification.md`
   - Write spec.md
   - Create checklist.md
   - Update checkpoint, EPIC_README, STATUS

3. **Execute S2.P3 for Feature 01:**
   - Follow guide: `stages/s2/s2_p3_refinement.md`
   - Refine spec
   - Finalize checklist
   - Complete S2 for Feature 01

**Work in 45-minute blocks:**
- 45 min: Deep work on Feature 01
- 15 min: Coordination (check inboxes, update status, respond to escalations)
- Repeat

### Responsibility 2: Coordination

**Every 15 minutes:**

1. **Check Inboxes:**
   ```bash
   # Check messages from Secondary-A
   grep "⏳ UNREAD" agent_comms/secondary_a_to_primary.md

   # Check messages from Secondary-B
   grep "⏳ UNREAD" agent_comms/secondary_b_to_primary.md
   ```

2. **Read Unread Messages:**
   - Read each unread message
   - Identify escalations (ESCALATION in subject)
   - Identify blockers
   - Identify completion signals

3. **Respond to Escalations:**
   - **Within 15 minutes for escalations**
   - Handle user questions
   - Provide guidance
   - Update affected files if needed
   - Send response message

4. **Check STATUS Files:**
   ```bash
   # Check all feature STATUS files
   cat feature_01_player_json/STATUS
   cat feature_02_team_penalty/STATUS
   cat feature_03_scoring_update/STATUS

   # Look for blockers
   grep "BLOCKERS:" feature_*/STATUS
   ```

5. **Check Checkpoints:**
   ```bash
   # Check for stale agents (>30 min old)
   check_stale_agents  # (See checkpoint_protocol.md)
   ```

6. **Update Sync Status:**
   - Count completed features
   - Update EPIC_README.md Sync Status section
   - Signal if all features ready

### Escalation Handling Workflow

**When you receive an escalation message:**

1. **Read escalation:**
   ```markdown
   Subject: ESCALATION - Spec Ambiguity
   Issue: Unclear if feature should use CSV or API
   ```

2. **Determine action:**
   - Can you answer from your knowledge? → Respond directly
   - Need user input? → Ask user, then respond

3. **If asking user:**
   ```markdown
   [To user in THIS session]

   Secondary-A has a question about Feature 02:
   - Spec says "integrate with team rankings"
   - Should they:
     A) Use existing team_rankings.csv file
     B) Fetch fresh data from NFL API
     C) Both (use CSV as cache, update from API)

   Which approach?
   ```

4. **After user answers:**
   ```markdown
   [Send message to Secondary-A]

   ## Message X (TIMESTAMP) ⏳ UNREAD
   **Subject:** Re: ESCALATION - Spec Ambiguity
   **Action:** Use existing team_rankings.csv file (Option A)
   **Details:** User confirmed: Use team_rankings.csv as data source
   **Next:** Update your spec.md with this approach, proceed with S2.P2
   **Acknowledge:** Reply when spec.md updated
   ```

5. **Wait for acknowledgment:**
   - Secondary-A replies confirming they've updated spec
   - Mark their reply as READ
   - Continue monitoring

### Workload Balance Example

**Timeline (3-feature epic, 2.5 hours parallel work):**

```text
10:00-10:15: Generate handoff packages, wait for secondary agents
10:15-11:00: Feature 01 S2.P1 work (45 min)
11:00-11:15: Coordination (check inboxes, STATUS files) (15 min)
11:15-12:00: Feature 01 S2.P2 work (45 min)
12:00-12:15: Coordination + escalation response (15 min)
12:15-13:00: Feature 01 S2.P2 continued (45 min)
13:00-13:15: Coordination (15 min)
13:15-14:00: Feature 01 S2.P3 work (45 min)
14:00-14:15: Feature 01 complete, coordination (15 min)
14:15-14:30: Wait for Secondary-A and Secondary-B to complete
14:30: All features complete S2

Total: 2.5 hours
- Feature 01 work: ~3 hours (normal S2 time)
- Coordination: ~30 min (20% overhead, within target)
```

---

## Phase 6: Sync Point - All Features Complete S2

**When all features complete S2.P3:**

### Step 1: Verify Completion

```bash
# Check all STATUS files
for STATUS_FILE in feature_*/STATUS; do
  STAGE=$(grep "^STAGE:" "$STATUS_FILE" | cut -d' ' -f2)
  READY=$(grep "^READY_FOR_SYNC:" "$STATUS_FILE" | cut -d' ' -f2)

  echo "$(basename $(dirname $STATUS_FILE)): $STAGE, Ready: $READY"
done

# All should show:
# feature_01: S2.P3, Ready: true
# feature_02: S2.P3, Ready: true
# feature_03: S2.P3, Ready: true
```

### Step 2: Update Sync Status

**Acquire lock and update EPIC_README.md:**

```markdown
## Sync Status

**Current Sync Point:** After S2 → Before S3
**Status:** ALL COMPLETE (3 of 3 features)
**Timestamp:** 2026-01-15 14:30

| Feature | Agent | S2.P3 Complete | Timestamp |
|---------|-------|----------------|-----------|
| feature_01 | Primary | ✅ YES | 14:00 |
| feature_02 | Secondary-A | ✅ YES | 14:25 |
| feature_03 | Secondary-B | ✅ YES | 14:30 |

**All features complete! Proceeding to S3.**
```

### Step 3: Notify User and Secondary Agents

**To user:**
```markdown
✅ All 3 features completed S2!

**Completion Summary:**
- Feature 01: Completed at 14:00 (Primary)
- Feature 02: Completed at 14:25 (Secondary-A)
- Feature 03: Completed at 14:30 (Secondary-B)

**Total S2 Time:** 2.5 hours (from 10:00 to 14:30)
**Time Saved:** 3.5 hours (vs 6 hours sequential)

🔄 Now running S3 (Cross-Feature Sanity Check)

I'll review all 3 specs for conflicts, overlaps, and gaps...
```

**To Secondary-A and Secondary-B:**
```markdown
## Message X (2026-01-15 14:35) ⏳ UNREAD
**Subject:** S2 Sync Complete - I'm Running S3
**Status:** All features completed S2
**Next:** I'm running S3 (Cross-Feature Sanity Check) alone
**Your Action:** WAIT - No action needed from you right now
**ETA:** S3 will take ~1 hour, then I'll proceed to S4
**Note:** Implementation (S5-S8) will be sequential in this plan
**Acknowledge:** No action needed
```

---

## Phase 7: S3 Cross-Feature Sanity Check (Solo)

**Run S3 alone (no parallel work):**

1. **Follow guide:** `stages/s3/s3_epic_planning_approval.md`

2. **Review all specs:**
   - Read spec.md for all 3 features
   - Check for conflicts
   - Check for overlaps
   - Check for gaps
   - Verify alignment with epic

3. **Update specs if issues found:**
   - Make corrections
   - Document conflicts resolved
   - Ensure consistency

4. **Complete S3:**
   - Document findings
   - Update EPIC_README.md
   - Signal S3 complete

---

## Phase 8: S4 Epic Testing Strategy (Solo)

**Run S4 alone:**

1. **Follow guide:** `stages/s4/s4_epic_testing_strategy.md`

2. **Update epic_smoke_test_plan.md:**
   - Add test scenarios for all features
   - Include cross-feature tests
   - Document dependencies

3. **Complete S4:**
   - Signal S4 complete

---

## Phase 9: Notify Secondary Agents of S3/S4 Completion

**Send final message to secondaries:**

```markdown
## Message X (2026-01-15 15:30) ⏳ UNREAD
**Subject:** S3 and S4 Complete - Implementation Sequential
**Status:** S3 (Cross-Feature Sanity Check) and S4 (Epic Testing) complete
**Findings:** No conflicts found with any feature specs
**Next Steps:**
- Implementation (S5-S8) will be SEQUENTIAL in this plan
- I (Primary) will implement Feature 01 first
- After Feature 01 → I'll implement Feature 02
- After Feature 02 → I'll implement Feature 03

**Your Sessions:**
- You can close your secondary agent sessions now
- Or keep them open (they'll remain idle during S5-S8)
- I'll handle all implementation work

Thank you for the parallel work during S2! We saved 3.5 hours.

**S2 Parallel Work Results:**
- Time: 2.5 hours (vs 6 hours sequential)
- Savings: 3.5 hours (58% reduction)
- Issues: None
- Coordination overhead: ~30 minutes (20%)

I'll now proceed with S5 (Implementation Planning) for Feature 01...
```

---

## Common Scenarios

### Scenario 1: Secondary Agent Escalates with User Question

**Workflow:**
1. Receive escalation message from Secondary-A
2. Read escalation: "User clarification needed"
3. Ask user in YOUR session
4. User responds
5. Send response to Secondary-A
6. Secondary-A acknowledges and resumes

**Timeline:** 5-15 minutes (depends on user response time)

### Scenario 2: Secondary Agent is Blocked (Not Escalating Yet)

**Workflow:**
1. Check STATUS file: `BLOCKERS: Investigating integration point`
2. Check inbox: Message says "Temporarily blocked, investigating"
3. Monitor: If not resolved in 15 min, check on them
4. If >30 min blocked: Send proactive message offering help

### Scenario 3: Secondary Agent Goes Stale (30 min no checkpoint)

**Workflow:**
1. Detect stale: Checkpoint >30 min old
2. Send warning message
3. Wait 5 min for response
4. If no response in 30 more min (60 total): Assume crashed
5. Decide: Defer feature to Wave 2 OR restart new secondary agent

### Scenario 4: You Complete Feature 01 First

**Workflow:**
1. Complete S2.P3 for Feature 01
2. Update STATUS: `READY_FOR_SYNC: true`
3. Update Sync Status: "1 of 3 complete"
4. Continue monitoring secondary agents
5. Wait for all to complete before S3

---

## Tools and References

**Lock File System:** See `lock_file_protocol.md`
**Communication:** See `communication_protocol.md`
**Checkpoints:** See `checkpoint_protocol.md`
**Escalation:** See PLAN_S2_PARALLELIZATION.md "Escalation Protocol" section
**Workload Management:** See PLAN_S2_PARALLELIZATION.md "Primary Workload Management" section

---

## Summary Checklist

**Before S2 Starts:**
- [ ] S1 complete
- [ ] Features analyzed for parallelization
- [ ] Offered parallel work to user
- [ ] User accepted
- [ ] Handoff packages generated
- [ ] User pasted packages in new sessions
- [ ] Secondary agents started (checkpoints created)

**During S2 Parallel Work:**
- [ ] Working on Feature 01 (45-min blocks)
- [ ] Checking inboxes every 15 min
- [ ] Responding to escalations within 15 min
- [ ] Monitoring STATUS files every 15 min
- [ ] Monitoring checkpoints for staleness
- [ ] Updating own checkpoint every 15 min

**After S2 Complete:**
- [ ] All features READY_FOR_SYNC
- [ ] Sync Status updated
- [ ] Notified user of completion
- [ ] Notified secondary agents
- [ ] Proceeding to S3 (solo)
- [ ] S3 complete
- [ ] S4 complete
- [ ] Notified secondary agents of S3/S4 completion

**Next:** Proceed to sequential implementation (S5-S8) for all features
