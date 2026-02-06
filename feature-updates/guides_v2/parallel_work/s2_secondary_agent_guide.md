# S2 Secondary Agent Guide (Parallel Work)

**Purpose:** Guide for Secondary agents working on assigned features during parallel S2

**Role:** Feature owner (single feature)

**Stages:** S2.P1 → S2.P2 → S2.P3 (parallel with Primary and other secondaries)

---

## Overview

When you join as a Secondary agent, you'll receive a **handoff package** with your configuration. Your responsibilities:

1. **Feature Owner:** Complete S2 (Feature Deep Dive) for your assigned feature
2. **Communicator:** Report progress, ask questions, signal completion
3. **Team Player:** Coordinate via checkpoints, STATUS files, and messaging

**Time Distribution:**
- 90% Feature work (your S2 implementation)
- 10% Coordination (checkpoints, inbox checks, status updates)

**Key Principle:** You own ONE feature completely. Focus on that feature, escalate when blocked.

---

## Startup Workflow

**NEW SIMPLIFIED PROCESS:**

Handoff packages are pre-generated in feature folders by the Primary agent. User spawns you with a simple one-line command:

**User startup command:**
```text
You are a secondary agent for Feature 02 (schedule_fetcher)
```

**Your response:**
- Detect "secondary agent for Feature 02" instruction
- Read `feature_02_{name}/HANDOFF_PACKAGE.md` automatically
- Extract assignment and begin S2.P1

**Benefits:**
- No copy/paste needed (one-line instruction per agent)
- No copy/paste errors (agent reads file directly)
- Scalable (works identically for 2 or 20 features)
- Consistent startup pattern for all secondary agents

**Fallback:** If handoff package not found in feature folder, ask user to provide it manually (legacy process below).

---

### Step 1: Receive Handoff Package

**User will provide handoff package via:**

**Option A (Recommended): File-based handoff**
- User says: "You are a secondary agent for Feature 02"
- You read: `feature_02_{name}/HANDOFF_PACKAGE.md`

**Option B (Legacy): Pasted handoff**
- User pastes handoff package into your session:

```markdown
═══════════════════════════════════════════════════════════
I'm joining as a secondary agent for epic KAI-6-nfl_team_penalty.

**Configuration:**
Epic Path: C:/Users/.../KAI-6-nfl_team_penalty
My Assignment: feature_02_team_penalty
Primary Agent ID: Agent-abc123
My Agent ID: Secondary-A
Starting Stage: S2.P1 (Feature Deep Dive - Research Phase)

**Coordination:**
- Inbox: agent_comms/primary_to_secondary_a.md
- Outbox: agent_comms/secondary_a_to_primary.md
- Checkpoint: agent_checkpoints/secondary_a.json
- STATUS: feature_02_team_penalty/STATUS

**Sync Points:**
- After S2.P3 complete: Signal completion, WAIT for Primary to run S3
- After Primary completes S3: Proceed to implementation (sequential)

Begin S2.P1 now.
═══════════════════════════════════════════════════════════
```

### Step 2: Parse Configuration

**Extract from handoff package:**
- Epic path: Where epic folder is located
- Feature assignment: Which feature you own
- Agent ID: Your identifier (Secondary-A, Secondary-B, etc.)
- Coordination paths: Where to check inbox, write messages, etc.
- **Dependency Group:** Which group you belong to (if applicable)
- **Group Context:** Which previous groups you depend on (if applicable)

### Step 2.5: Understand Group Context (If Applicable)

**Check if handoff package includes group information:**

**Indicators:**
- "Dependency Group: Group 2" (or Group 3, Group 4, etc.)
- "Group Dependencies: Group 2 depends on Group 1 completing S2 first"
- "Why You're Starting Now" section explaining previous group completion
- "Group N Specs Available" with file paths to reference

**If group context present:**

**What it means:**
- Your feature is in Group N (dependent group)
- Group N-1 has already completed S2
- Your feature depends on Group N-1's specs to write its own spec
- You should reference Group N-1 spec.md files during your research

**Example:**
```markdown
**Dependency Group:** Group 2
**Group Dependencies:** Group 2 depends on Group 1 completing S2 first

**Why You're Starting Now:**
- Group 1 has completed S2 (Feature 01: core_logging_infrastructure)
- Group 1's specs are available for reference
- Your feature depends on Group 1's spec to write its own spec

**Group 1 Specs Available:**
- Feature 01: feature_01_core_logging_infrastructure/spec.md
- **Key content:** LineBasedRotatingHandler API, setup_logger() function
```

**How to use group context:**

1. **During S2.P1.I1 (Discovery):**
   - Read Group N-1 spec.md files listed in handoff
   - Understand APIs/interfaces your feature will use
   - Reference these in your RESEARCH_NOTES.md

2. **During S2.P1.I2 (Checklist Resolution):**
   - Answer checklist questions with knowledge of Group N-1 APIs
   - Reference Group N-1 decisions for consistency

3. **During S2.P1.I3 (Refinement):**
   - Write your spec.md assuming Group N-1 APIs exist
   - Add traceability references to Group N-1 specs

**If NO group context present:**
- Your feature is in Group 1 OR all features are independent
- No dependencies on other features' specs
- Research and specify independently

**Group context only matters for S2** - after S2 complete, groups are irrelevant.

### Step 3: Verify Epic Exists

```bash
EPIC_PATH="C:/Users/.../KAI-6-nfl_team_penalty"

if [ ! -d "$EPIC_PATH" ]; then
  echo "ERROR: Epic path not found: $EPIC_PATH"
  exit 1
fi

echo "✅ Epic path verified: $EPIC_PATH"
```

### Step 4: Verify Feature Folder Exists

```bash
FEATURE_FOLDER="feature_02_team_penalty"

if [ ! -d "$EPIC_PATH/$FEATURE_FOLDER" ]; then
  echo "ERROR: Feature folder not found: $FEATURE_FOLDER"
  exit 1
fi

echo "✅ Feature folder verified: $FEATURE_FOLDER"
```

### Step 5: Create Coordination Infrastructure

```bash
# Create communication channels
mkdir -p "$EPIC_PATH/agent_comms"

# Create inbox (Primary writes, I read)
cat > "$EPIC_PATH/agent_comms/primary_to_secondary_a.md" <<EOF
# Messages: Primary → Secondary-A

(No messages yet)
EOF

# Create outbox (I write, Primary reads)
cat > "$EPIC_PATH/agent_comms/secondary_a_to_primary.md" <<EOF
# Messages: Secondary-A → Primary

(No messages yet)
EOF

echo "✅ Communication channels created"
```

### Step 6: Create Checkpoint File

```bash
# Create checkpoints directory
mkdir -p "$EPIC_PATH/agent_checkpoints"

# Generate session ID
SESSION_ID=$(uuidgen)  # Or: $(date +%s)

# Create initial checkpoint
cat > "$EPIC_PATH/agent_checkpoints/secondary_a.json" <<EOF
{
  "agent_id": "Secondary-A",
  "agent_type": "secondary",
  "session_id": "$SESSION_ID",
  "feature": "feature_02_team_penalty",
  "stage": "S2.P1",
  "phase": "Research Phase - Starting",
  "last_checkpoint": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "next_checkpoint_expected": "$(date -u -d "+15 minutes" +"%Y-%m-%dT%H:%M:%SZ")",
  "status": "IN_PROGRESS",
  "can_resume": true,
  "blockers": [],
  "files_modified": [],
  "recovery_instructions": "Just started S2.P1. Start from beginning of Research Phase guide.",
  "current_step": "Configuring agent from handoff package",
  "completed_steps": [
    "Received handoff package",
    "Verified epic and feature paths",
    "Created communication channels"
  ],
  "next_steps": [
    "Create checkpoint file",
    "Create STATUS file",
    "Update EPIC_README.md",
    "Begin S2.P1"
  ],
  "coordination_state": {
    "last_inbox_check": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
    "unread_messages": 0,
    "last_epic_readme_update": "never",
    "last_status_update": "never"
  }
}
EOF

echo "✅ Checkpoint file created"
```

### Step 7: Create STATUS File

```bash
# Create STATUS file
cat > "$EPIC_PATH/$FEATURE_FOLDER/STATUS" <<EOF
STAGE: S2.P1
PHASE: Research Phase
AGENT: Secondary-A
AGENT_ID: $SESSION_ID
UPDATED: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
STATUS: IN_PROGRESS
BLOCKERS: none
NEXT_ACTION: Begin S2.P1 Research Phase
READY_FOR_SYNC: false
ESTIMATED_COMPLETION: $(date -u -d "+2 hours" +"%Y-%m-%dT%H:%M:%SZ")
EOF

echo "✅ STATUS file created"
```

### Step 8: Update EPIC_README.md

**Acquire lock, update your section:**

```bash
# Acquire lock
acquire_lock "epic_readme" "$SESSION_ID" "Adding Secondary-A progress section"

# Read EPIC_README.md
# Add your progress section (between BEGIN/END markers)

# Example section to add:
```

```markdown
<!-- BEGIN SECONDARY-A PROGRESS -->
## Feature 02 Progress (Secondary-A)

**Last Updated:** 2026-01-15 10:30
**Current Stage:** S2.P1 (Research Phase - Starting)
**Current Step:** Configuring agent from handoff package
**Blockers:** None
**Next Action:** Begin S2.P1 Research Phase

**S2 Progress:**
- ⏳ S2.P1 (Research Phase) - Starting
- ⏳ S2.P2 (Specification Phase) - Not Started
- ⏳ S2.P3 (Refinement Phase) - Not Started
<!-- END SECONDARY-A PROGRESS -->
```

**Release lock:**
```bash
release_lock "epic_readme"
```

### Step 9: Send Initial Message to Primary

```markdown
## Message 1 (2026-01-15 10:30) ⏳ UNREAD
**Subject:** Secondary-A Started
**Action:** I've started work on feature_02_team_penalty
**Details:** Handoff package received, configuration complete
**Next:** Beginning S2.P1 Research Phase now
**Acknowledge:** No action needed
```

### Step 10: Confirm Startup to User

```markdown
✅ Configuration verified
   Epic: KAI-6-nfl_team_penalty
   Feature: feature_02_team_penalty
   Primary: Agent-abc123
   My ID: Secondary-A

✅ Coordination channels confirmed
   Inbox: agent_comms/primary_to_secondary_a.md (created)
   Outbox: agent_comms/secondary_a_to_primary.md (created)

✅ Checkpoint system initialized
   File: agent_checkpoints/secondary_a.json (created)
   Update frequency: Every 15 minutes

✅ STATUS file initialized
   File: feature_02_team_penalty/STATUS (created)

📨 Sent initial message to Primary
   Confirmed startup

✅ Updated EPIC_README.md with my progress section

🚀 Starting S2.P1 (Feature Deep Dive - Research Phase)

Reading guide: stages/s2/s2_p1_research.md...
```

---

## S2 Work Workflow

### S2.P1: Research Phase

**Follow guide:** `stages/s2/s2_p1_research.md`

**Additional coordination steps:**

1. **Every 15 minutes:**
   - Update checkpoint
   - Check inbox
   - Update STATUS file
   - Update EPIC_README.md progress section

2. **If blocked >30 minutes:**
   - Send escalation message to Primary
   - Update STATUS: `BLOCKERS: <description>`
   - Wait for Primary response

3. **After completing S2.P1:**
   - Update checkpoint: `stage: S2.P2`
   - Update STATUS: `STAGE: S2.P2`
   - Update EPIC_README.md: S2.P1 complete
   - Proceed to S2.P2

### S2.P2: Specification Phase

**Follow guide:** `stages/s2/s2_p2_specification.md`

**Additional coordination steps:**
- Same as S2.P1 (checkpoints, inbox, status, epic readme)
- Escalate if spec ambiguities can't be resolved
- Signal if user questions needed

**After completing S2.P2:**
- Update coordination files
- Proceed to S2.P3

### S2.P3: Refinement Phase

**Follow guide:** `stages/s2/s2_p3_refinement.md`

**Additional coordination steps:**
- Same as S2.P1 and S2.P2
- Finalize spec and checklist
- Prepare for sync

**After completing S2.P3:**
- **Signal completion to Primary**
- Update STATUS: `READY_FOR_SYNC: true`
- WAIT for Primary to run S3

---

## Coordination Heartbeat (Every 15 Minutes)

### Step 1: Update Checkpoint

```bash
# Update checkpoint file
# (See checkpoint_protocol.md for details)

# Update fields:
# - last_checkpoint
# - next_checkpoint_expected
# - stage (if changed)
# - current_step
# - completed_steps (add new ones)
# - files_modified (add any new files)
# - recovery_instructions
```

### Step 2: Check Inbox

```bash
INBOX="agent_comms/primary_to_secondary_a.md"

# Check for unread messages
UNREAD_COUNT=$(grep -c "⏳ UNREAD" "$INBOX")

if [ $UNREAD_COUNT -gt 0 ]; then
  echo "You have $UNREAD_COUNT unread messages from Primary"
  # Read messages
  # Mark as READ
  # Take action
fi
```

### Step 3: Process Messages

**For each unread message:**

1. **Read message:**
   ```markdown
   Subject: User answered your question
   Action: Check feature_02/checklist.md - Question 5 answered
   ```

2. **Take action:**
   - Read updated file
   - Update your work accordingly
   - Reply if acknowledgment requested

3. **Mark as READ:**
   ```bash
   # Change ⏳ UNREAD to ✅ READ
   sed -i 's/⏳ UNREAD/✅ READ/' "$INBOX"
   ```

4. **Reply if needed:**
   ```markdown
   ## Message 2 (TIMESTAMP) ⏳ UNREAD
   **Subject:** Re: User answered question
   **Action:** Spec updated with user's answer
   **Details:** Updated spec.md with penalty application approach
   **Next:** Continuing with S2.P2
   **Acknowledge:** No action needed
   ```

### Step 4: Update STATUS File

```bash
# Update STATUS file
cat > "feature_02_team_penalty/STATUS" <<EOF
STAGE: S2.P2
PHASE: Specification Phase - In Progress
AGENT: Secondary-A
AGENT_ID: $SESSION_ID
UPDATED: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
STATUS: IN_PROGRESS
BLOCKERS: none
NEXT_ACTION: Writing spec.md Acceptance Criteria section
READY_FOR_SYNC: false
ESTIMATED_COMPLETION: $(date -u -d "+1 hour" +"%Y-%m-%dT%H:%M:%SZ")
EOF
```

### Step 5: Update EPIC_README.md (if progress changed)

**Acquire lock, update your section:**

```markdown
<!-- BEGIN SECONDARY-A PROGRESS -->
## Feature 02 Progress (Secondary-A)

**Last Updated:** 2026-01-15 12:30
**Current Stage:** S2.P2 (Specification Phase - In Progress)
**Current Step:** Writing spec.md Acceptance Criteria
**Blockers:** None
**Next Action:** Complete Acceptance Criteria, create checklist.md

**S2 Progress:**
- ✅ S2.P1 (Research Phase) - Complete
- 🔄 S2.P2 (Specification Phase) - In Progress (70% done)
- ⏳ S2.P3 (Refinement Phase) - Not Started
<!-- END SECONDARY-A PROGRESS -->
```

**Release lock**

### Step 6: Set 15-Minute Timer

```bash
# Set timer for next heartbeat
echo "Next heartbeat in 15 minutes"
# (Manually set reminder or continue work)
```

---

## Escalation Workflow

### When to Escalate

**Escalate to Primary when:**
- User questions needed (you can't answer from codebase)
- Spec ambiguities (can't resolve from existing docs)
- Integration concerns (affects other features)
- Blocked >30 minutes (can't make progress)
- Major technical decisions (architecture-level)

**Don't escalate for:**
- Implementation approach choices (decide yourself)
- Code structure decisions (your feature, your choice)
- Test design (decide yourself)
- Minor clarifications (check codebase first)

### Escalation Message Template

```markdown
## Message X (TIMESTAMP) ⏳ UNREAD
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
**Acknowledge:** Reply with decision or "escalating to user"
```

### After Escalating

1. **Update STATUS:**
   ```text
   BLOCKERS: Escalated to Primary - waiting for spec clarification
   ```

2. **Update checkpoint:**
   ```json
   "blockers": ["Spec ambiguity: team rankings integration approach"],
   "status": "BLOCKED"
   ```

3. **Update EPIC_README.md:**
   ```markdown
   **Blockers:** ESCALATION - Awaiting Primary response on spec ambiguity
   ```

4. **Wait for Primary response:**
   - Check inbox every 5 minutes (urgent)
   - Primary responds within 15-60 minutes

5. **When response received:**
   - Read response
   - Mark as READ
   - Take action
   - Send acknowledgment
   - Update STATUS: `BLOCKERS: none`
   - Resume work

---

## Completion Signal

### After Completing S2.P3

**Step 1: Finalize All Files**
- spec.md complete
- checklist.md complete
- README.md updated
- All coordination files updated

**Step 2: Update STATUS**
```text
STAGE: S2.P3
PHASE: Refinement - Complete
STATUS: COMPLETE
READY_FOR_SYNC: true
NEXT_ACTION: Waiting for Primary to run S3
```

**Step 3: Update Checkpoint**
```json
"stage": "S2.P3",
"phase": "Refinement - Complete",
"status": "COMPLETE",
"can_resume": false,
"recovery_instructions": "S2 complete for this feature. Waiting for Primary S3."
```

**Step 4: Update EPIC_README.md**
```markdown
<!-- BEGIN SECONDARY-A PROGRESS -->
## Feature 02 Progress (Secondary-A)

**Last Updated:** 2026-01-15 14:25
**Current Stage:** S2.P3 (COMPLETE)
**Current Step:** Waiting for Primary to run S3
**Blockers:** None
**Next Action:** Awaiting S3 completion

**S2 Progress:**
- ✅ S2.P1 (Research Phase) - Complete
- ✅ S2.P2 (Specification Phase) - Complete
- ✅ S2.P3 (Refinement Phase) - Complete
<!-- END SECONDARY-A PROGRESS -->
```

**Step 5: Send Completion Message**
```markdown
## Message X (2026-01-15 14:25) ⏳ UNREAD
**Subject:** S2.P3 Complete for Feature 02
**Status:** feature_02_team_penalty S2 complete
**Files Ready:**
- spec.md (complete, all requirements documented)
- checklist.md (all items resolved)
- README.md (updated with S2 completion)

**Blockers:** None
**Ready for S3:** Yes
**Awaiting:** Your S3 Cross-Feature Sanity Check
**Acknowledge:** No action needed, proceed when all features ready
```

---

## Waiting for Primary (After S2 Complete)

### Step 1: Enter Waiting State

**Your S2 work is done, now wait for Primary to:**
- Complete their Feature 01 S2
- Wait for other secondaries to complete
- Run S3 (Cross-Feature Sanity Check)
- Run S4 (Epic Testing Strategy)

### Step 2: Monitor Inbox

**Check inbox every 15 minutes:**
- Primary may send updates
- Primary will signal when S3/S4 complete

### Step 3: When Primary Signals S3/S4 Complete

**Primary sends message:**
```markdown
Subject: S3 and S4 Complete - Implementation Sequential
Status: All planning complete
Next: Implementation (S5-S8) will be sequential
```

**Your action:**
- Mark message as READ
- Understand next steps
- **For S2 plan:** Implementation is sequential (you can close session or idle)

### Step 4: Optional: Close Session

**If implementation is sequential:**
- Your work is done for parallel phase
- You can close this session
- Primary will handle S5-S8 for all features

**OR keep session open:**
- If you want to monitor progress
- Primary may send updates
- But no active work required from you

---

## Common Scenarios

### Scenario 1: You're Blocked, Need User Input

1. Check codebase first (try to answer yourself)
2. If can't answer in 30 min → escalate
3. Send escalation message
4. Update STATUS, checkpoint, EPIC_README
5. Wait for Primary response (check inbox every 5 min)
6. When response comes → acknowledge, resume

### Scenario 2: Primary Asks You to Update Something

1. Receive message: "Update spec.md with X"
2. Read message, understand request
3. Make update
4. Reply: "Updated, resuming work"
5. Mark message as READ
6. Continue

### Scenario 3: You Complete S2 Before Others

1. Signal completion
2. Update all coordination files
3. Enter waiting state
4. Monitor inbox
5. Wait for Primary to signal S3 complete

### Scenario 4: Session Crashes Mid-Work

1. User restarts session
2. User pastes handoff package again (or says "resume")
3. You check for existing checkpoint
4. Read checkpoint: "Resume from S2.P2, 80% done"
5. Read modified files (spec.md, checklist.md)
6. Resume from current step
7. Update checkpoint with new session_id

---

## Tools and References

**Lock File System:** See `lock_file_protocol.md`
**Communication:** See `communication_protocol.md`
**Checkpoints:** See `checkpoint_protocol.md`
**Escalation:** See PLAN_S2_PARALLELIZATION.md "Escalation Protocol" section

---

## Summary Checklist

**Startup:**
- [ ] Received handoff package
- [ ] Verified epic and feature paths
- [ ] Created communication channels
- [ ] Created checkpoint file
- [ ] Created STATUS file
- [ ] Updated EPIC_README.md
- [ ] Sent initial message to Primary

**During S2:**
- [ ] Working on S2.P1 → S2.P2 → S2.P3
- [ ] Updating checkpoint every 15 min
- [ ] Checking inbox every 15 min
- [ ] Updating STATUS file every 15 min
- [ ] Updating EPIC_README.md when progress changes
- [ ] Escalating when blocked >30 min

**Completion:**
- [ ] S2.P3 complete
- [ ] spec.md finalized
- [ ] checklist.md finalized
- [ ] All coordination files updated
- [ ] Completion message sent to Primary
- [ ] Entered waiting state

**After S3/S4:**
- [ ] Received S3/S4 complete message from Primary
- [ ] Understood next steps
- [ ] Closed session or idling (depending on plan)

**Next:** If S5-S8 parallelization also enabled, await new handoff package for implementation phase
