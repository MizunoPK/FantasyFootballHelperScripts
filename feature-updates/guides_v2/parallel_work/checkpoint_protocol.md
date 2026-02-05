# Checkpoint Protocol

**Purpose:** Enable recovery from agent failures during parallel S2 work

**Used For:** S2 parallelization (agent crash recovery, session resumption)

**Checkpoint Files:** `agent_checkpoints/primary.json`, `agent_checkpoints/secondary_a.json`, etc.

---

## Overview

When agents work in parallel during S2, sessions can crash or lose context due to:
- Browser tab crashes
- Network disconnections
- Context window limits (conversation compaction)
- User accidentally closing session

The checkpoint system provides **recoverable state** so work can resume without starting over.

---

## Checkpoint File Format

**Location:** `agent_checkpoints/{agent_id}.json`

**Format (JSON):**
```json
{
  "agent_id": "Agent-Primary",
  "agent_type": "primary",
  "session_id": "abc123def456",
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
    "feature_01_player_json/checklist.md",
    "EPIC_README.md"
  ],
  "recovery_instructions": "Resume from S2.P2 Specification Phase. spec.md partially complete (70% done). Continue from Requirements Section 5.",
  "current_step": "Writing spec.md Requirements Section 5 (Error Handling)",
  "completed_steps": [
    "S2.P1 complete",
    "S2.P2 Phase 0: Read guide",
    "S2.P2 Phase 1: Requirements Sections 1-4 written"
  ],
  "next_steps": [
    "Complete Requirements Section 5",
    "Write Acceptance Criteria",
    "Create checklist.md questions"
  ],
  "coordination_state": {
    "last_inbox_check": "2026-01-15T14:28:00Z",
    "unread_messages": 0,
    "last_epic_readme_update": "2026-01-15T14:15:00Z",
    "last_status_update": "2026-01-15T14:15:00Z"
  }
}
```markdown

**Fields:**
- `agent_id`: Agent identifier (Agent-Primary, Secondary-A, Secondary-B)
- `agent_type`: primary or secondary
- `session_id`: Unique ID for this session (generated at start)
- `feature`: Which feature this agent owns
- `stage`: Current stage (S2.P1, S2.P2, S2.P3)
- `phase`: Human-readable phase name
- `last_checkpoint`: When this checkpoint was last updated
- `next_checkpoint_expected`: When next update expected (15 min from last)
- `status`: IN_PROGRESS, WAITING, BLOCKED, COMPLETE
- `can_resume`: Whether work can be resumed from this checkpoint
- `blockers`: Array of blocker descriptions (if any)
- `files_modified`: Files changed since last commit
- `recovery_instructions`: Human-readable resume instructions
- `current_step`: What agent is working on right now
- `completed_steps`: Steps already done
- `next_steps`: Steps to do next
- `coordination_state`: Last coordination activity timestamps

---

## Checkpoint Update Trigger Mechanism

**Important:** Checkpoints are **agent-initiated (manual)**, not automated.

**Update Triggers:**
1. **Heartbeat updates** - Agent sets 15-minute timer, manually updates checkpoint
2. **Phase completion** - Guides include checkpoint update as final step before transitioning
3. **Blocker occurrence** - When agent gets blocked, update checkpoint with blocker info
4. **Sync points** - Before/after sync points, update checkpoint

**Integration in Guides:**
- Each guide includes explicit "Update checkpoint" steps
- Guides specify WHEN to update checkpoint
- Agent executes update step as part of workflow

**Why Manual:**
- Ensures agent is actively working and aware of current state
- Agent provides accurate recovery instructions (agent knows best)
- Prevents automated updates when agent is crashed/inactive

---

## Checkpoint Creation (First Time)

**When:** Agent startup, after receiving handoff package

### Step 1: Generate Session ID

```bash
# Generate unique session ID
SESSION_ID=$(uuidgen)  # Or use timestamp: $(date +%s)
echo "Session ID: $SESSION_ID"
```markdown

### Step 2: Create Checkpoint File

```bash
# Create checkpoint directory if needed
mkdir -p agent_checkpoints

# Create initial checkpoint
cat > agent_checkpoints/secondary_a.json <<EOF
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
  "recovery_instructions": "Just started S2.P1. No work done yet. Start from beginning of S2.P1 Research Phase guide.",
  "current_step": "Reading S2.P1 guide",
  "completed_steps": [
    "Received handoff package",
    "Verified epic path",
    "Created checkpoint file"
  ],
  "next_steps": [
    "Read S2.P1 guide",
    "Phase 0: Discovery Context Review",
    "Phase 1: Targeted Research"
  ],
  "coordination_state": {
    "last_inbox_check": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
    "unread_messages": 0,
    "last_epic_readme_update": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
    "last_status_update": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
  }
}
EOF

echo "Initial checkpoint created"
```markdown

---

## Checkpoint Update Protocol

**Frequency:** Every 15 minutes + at phase transitions

### Step 1: Read Current Checkpoint

```bash
# Read existing checkpoint
CHECKPOINT_FILE="agent_checkpoints/secondary_a.json"
CURRENT_CHECKPOINT=$(cat "$CHECKPOINT_FILE")
```markdown

### Step 2: Update Fields

```bash
# Update checkpoint with current state
cat > "$CHECKPOINT_FILE" <<EOF
{
  "agent_id": "Secondary-A",
  "agent_type": "secondary",
  "session_id": "$(echo $CURRENT_CHECKPOINT | jq -r '.session_id')",
  "feature": "feature_02_team_penalty",
  "stage": "S2.P2",
  "phase": "Specification - In Progress",
  "last_checkpoint": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "next_checkpoint_expected": "$(date -u -d "+15 minutes" +"%Y-%m-%dT%H:%M:%SZ")",
  "status": "IN_PROGRESS",
  "can_resume": true,
  "blockers": [],
  "files_modified": [
    "feature_02_team_penalty/spec.md",
    "feature_02_team_penalty/checklist.md"
  ],
  "recovery_instructions": "Resume from S2.P2 Specification Phase. spec.md is 80% complete. Complete Acceptance Criteria section, then move to checklist.md.",
  "current_step": "Writing Acceptance Criteria in spec.md",
  "completed_steps": [
    "S2.P1 complete (Research Phase)",
    "S2.P2 Phase 1: Requirements section written",
    "S2.P2 Phase 2: Integration section written"
  ],
  "next_steps": [
    "Complete Acceptance Criteria",
    "Write checklist.md questions",
    "Transition to S2.P3"
  ],
  "coordination_state": {
    "last_inbox_check": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
    "unread_messages": 0,
    "last_epic_readme_update": "$(date -u -d "-15 minutes" +"%Y-%m-%dT%H:%M:%SZ")",
    "last_status_update": "$(date -u -d "-15 minutes" +"%Y-%m-%dT%H:%M:%SZ")"
  }
}
EOF

echo "Checkpoint updated"
```markdown

### Step 3: Verify Update

```bash
# Verify checkpoint file valid JSON
if jq '.' "$CHECKPOINT_FILE" >/dev/null 2>&1; then
  echo "Checkpoint valid"
else
  echo "ERROR: Checkpoint corrupted during update"
  # Restore from backup if exists
fi
```markdown

---

## Stale Detection

**Purpose:** Identify agents that have crashed or stopped working

### Stale Thresholds

**30 minutes (Warning):**
- Primary checks all secondary checkpoints
- If `last_checkpoint` > 30 minutes ago → Send warning message
- Secondary may be slow but still working

**60 minutes (Failure):**
- If `last_checkpoint` > 60 minutes ago → Assume agent crashed
- Primary takes action (reassign feature or defer to Wave 2)

### Primary Monitoring Script

```bash
# Primary checks all secondary checkpoints every 15 minutes
check_stale_agents() {
  local NOW=$(date -u +%s)

  for CHECKPOINT in agent_checkpoints/secondary_*.json; do
    if [ ! -f "$CHECKPOINT" ]; then continue; fi

    AGENT_ID=$(jq -r '.agent_id' "$CHECKPOINT")
    LAST_CHECKPOINT=$(jq -r '.last_checkpoint' "$CHECKPOINT")
    LAST_TIMESTAMP=$(date -d "$LAST_CHECKPOINT" +%s)
    AGE_SECONDS=$((NOW - LAST_TIMESTAMP))
    AGE_MINUTES=$((AGE_SECONDS / 60))

    if [ $AGE_MINUTES -gt 60 ]; then
      echo "❌ $AGENT_ID: STALE (${AGE_MINUTES} min) - Likely crashed"
      # Take action (see Recovery Procedures)
    elif [ $AGE_MINUTES -gt 30 ]; then
      echo "⚠️ $AGENT_ID: WARNING (${AGE_MINUTES} min) - May be slow"
      # Send warning message
    else
      echo "✅ $AGENT_ID: ACTIVE (${AGE_MINUTES} min ago)"
    fi
  done
}
```markdown

### Warning Message (30 minutes)

**Primary sends to Secondary:**
```markdown
## Message X (2026-01-15 15:00) ⏳ UNREAD
**Subject:** CHECKPOINT WARNING - No Update in 30 Minutes
**Action:** Please update your checkpoint and confirm you're still working
**Details:** Your last checkpoint was at 14:30 (30 minutes ago)
         Expected checkpoint every 15 minutes
         Are you still actively working?
**Next:** Reply "Still working" and update checkpoint ASAP
**Acknowledge:** Reply immediately
```markdown

### Failure Escalation (60 minutes)

**Primary assumes crash:**
- Update EPIC_README.md: "Secondary-A: STALE (likely crashed)"
- Notify user: "Secondary-A hasn't updated checkpoint in 60 minutes"
- Decide recovery strategy (see Recovery Procedures section)

---

## Recovery Procedures

### Scenario 1: Same Agent Resumes (Session Restarted)

**Trigger:** Agent session crashed, user restarts same agent

**Steps:**
1. **User pastes handoff package again** (or says "resume")
2. **Agent checks for existing checkpoint:**
   ```bash
   CHECKPOINT="agent_checkpoints/secondary_a.json"
   if [ -f "$CHECKPOINT" ]; then
     echo "Found existing checkpoint, resuming..."
   fi
   ```markdown
3. **Agent reads checkpoint:**
   ```bash
   STAGE=$(jq -r '.stage' "$CHECKPOINT")
   RECOVERY_INSTRUCTIONS=$(jq -r '.recovery_instructions' "$CHECKPOINT")
   FILES_MODIFIED=$(jq -r '.files_modified[]' "$CHECKPOINT")

   echo "Resuming from: $STAGE"
   echo "Instructions: $RECOVERY_INSTRUCTIONS"
   echo "Modified files: $FILES_MODIFIED"
   ```markdown
4. **Agent reads modified files:**
   ```bash
   # Read each modified file to understand current state
   for FILE in $FILES_MODIFIED; do
     echo "Reading $FILE..."
     # Use Read tool
   done
   ```markdown
5. **Agent resumes work:**
   - Follow `recovery_instructions`
   - Continue from `current_step`
   - Execute remaining `next_steps`
6. **Agent updates checkpoint:**
   - New `session_id` (fresh session)
   - Same `stage`, `feature`, `agent_id`
   - Status: IN_PROGRESS (resumed)

**Example Resume Message:**
```markdown
✅ Checkpoint found! Resuming work...

**Previous Session:**
- Stage: S2.P2 (Specification)
- Last Update: 14:30 (45 minutes ago)
- Status: IN_PROGRESS

**Current State:**
- spec.md: 80% complete
- checklist.md: Started
- EPIC_README.md: Updated with progress

**Resuming from:** Writing Acceptance Criteria in spec.md

**Next Steps:**
1. Complete Acceptance Criteria section
2. Finish checklist.md questions
3. Transition to S2.P3

I'll continue where I left off...
```markdown

### Scenario 2: New Agent Takes Over (Reassignment)

**Trigger:** Original agent crashed and won't resume, Primary assigns new agent

**Steps:**
1. **Primary creates new handoff package:**
   - Same feature assignment
   - Note: "Resuming work from crashed agent"
   - Include checkpoint file path
2. **User pastes handoff in NEW session:**
   ```text
   I'm taking over feature_02_team_penalty from crashed Secondary-A.

   Checkpoint File: agent_checkpoints/secondary_a.json
   Resume from: S2.P2 Specification Phase
   ```markdown
3. **New agent reads checkpoint:**
   - Same as Scenario 1
   - Understands where previous agent left off
4. **New agent creates NEW checkpoint file:**
   ```bash
   # Rename old checkpoint to archive
   mv agent_checkpoints/secondary_a.json \
      agent_checkpoints/secondary_a_crashed_$(date +%s).json

   # Create new checkpoint for new agent
   # (Could be Secondary-C or reuse Secondary-A ID)
   ```markdown
5. **New agent resumes work:**
   - Same feature, same stage
   - Fresh session_id
   - Continues from checkpoint instructions

### Scenario 3: Restart Feature from Scratch (Last Resort)

**Trigger:** Checkpoint corrupted OR minimal work done (< 30 min)

**Steps:**
1. **Primary decides:** "Feature 02 has minimal progress, restart"
2. **Primary archives checkpoint:**
   ```bash
   mv agent_checkpoints/secondary_a.json \
      agent_checkpoints/secondary_a_aborted_$(date +%s).json
   ```markdown
3. **Primary generates fresh handoff package:**
   - Same as original
   - No checkpoint reference
4. **New agent starts from S2.P1:**
   - Fresh start
   - No recovery needed
   - Creates new checkpoint

---

## Checkpoint Backup Strategy

**Automatic Backups:**

```bash
# Before updating checkpoint, create backup
backup_checkpoint() {
  local CHECKPOINT_FILE=$1
  local BACKUP_DIR="agent_checkpoints/backups"

  mkdir -p "$BACKUP_DIR"

  # Create timestamped backup
  local TIMESTAMP=$(date +%Y%m%d_%H%M%S)
  cp "$CHECKPOINT_FILE" "$BACKUP_DIR/$(basename $CHECKPOINT_FILE .json)_$TIMESTAMP.json"

  # Keep only last 10 backups
  ls -t "$BACKUP_DIR"/$(basename $CHECKPOINT_FILE .json)_*.json | tail -n +11 | xargs rm -f
}

# Usage:
backup_checkpoint "agent_checkpoints/secondary_a.json"
# Now safe to update checkpoint
```markdown

**Recovery from Backup:**

```bash
# If checkpoint corrupted, restore from latest backup
restore_checkpoint() {
  local CHECKPOINT_FILE=$1
  local BACKUP_DIR="agent_checkpoints/backups"

  # Find latest backup
  local LATEST_BACKUP=$(ls -t "$BACKUP_DIR"/$(basename $CHECKPOINT_FILE .json)_*.json | head -n 1)

  if [ -f "$LATEST_BACKUP" ]; then
    echo "Restoring from backup: $LATEST_BACKUP"
    cp "$LATEST_BACKUP" "$CHECKPOINT_FILE"
    echo "Checkpoint restored"
  else
    echo "ERROR: No backup found"
    return 1
  fi
}
```markdown

---

## Integration with Guides

### In S2.P1, S2.P2, S2.P3 Guides

**Add checkpoint update steps:**

```markdown
### Step X: Update Checkpoint (Every 15 Minutes)

**Set a 15-minute timer and update checkpoint:**

1. **Update checkpoint file:** `agent_checkpoints/{your_agent_id}.json`

2. **Update these fields:**
   - `last_checkpoint`: Current timestamp
   - `next_checkpoint_expected`: +15 minutes
   - `stage`: Current stage (S2.P1, S2.P2, S2.P3)
   - `current_step`: What you're working on right now
   - `completed_steps`: Add any newly completed steps
   - `files_modified`: Add any files you've edited
   - `recovery_instructions`: Update instructions for resuming

3. **Verify checkpoint valid:**
   ```bash
   jq '.' agent_checkpoints/{your_agent_id}.json
   ```markdown

4. **Backup checkpoint** (optional but recommended)

5. **Reset 15-minute timer** for next checkpoint
```markdown

### At Phase Transitions

```markdown
### Step X: Complete S2.P1 (Transition to S2.P2)

1. **Final checkpoint update:**
   - Update `stage`: "S2.P2"
   - Update `phase`: "Specification - Starting"
   - Update `completed_steps`: Add "S2.P1 complete"
   - Update `next_steps`: S2.P2 tasks
   - Update `recovery_instructions`: "Resume from beginning of S2.P2"

2. **Verify checkpoint saved:**
   ```bash
   jq '.stage' agent_checkpoints/{your_agent_id}.json
   # Should show: "S2.P2"
   ```markdown

3. **Proceed to S2.P2**
```markdown

---

## Error Handling

### Error 1: Checkpoint File Missing

```bash
# If checkpoint file doesn't exist when it should
if [ ! -f "agent_checkpoints/secondary_a.json" ]; then
  echo "WARNING: Checkpoint file missing"
  echo "Creating fresh checkpoint from current state..."
  # Create checkpoint using current known state
fi
```markdown

### Error 2: Checkpoint File Corrupted (Invalid JSON)

```bash
# If checkpoint is not valid JSON
if ! jq '.' "agent_checkpoints/secondary_a.json" >/dev/null 2>&1; then
  echo "ERROR: Checkpoint corrupted"
  echo "Attempting to restore from backup..."
  restore_checkpoint "agent_checkpoints/secondary_a.json"

  if [ $? -ne 0 ]; then
    echo "No backup available, creating fresh checkpoint"
    # Create checkpoint from scratch
  fi
fi
```markdown

### Error 3: Checkpoint Too Old (Stale Agent)

```bash
# If checkpoint is >60 minutes old
LAST_CHECKPOINT=$(jq -r '.last_checkpoint' "agent_checkpoints/secondary_a.json")
LAST_TIMESTAMP=$(date -d "$LAST_CHECKPOINT" +%s)
NOW=$(date -u +%s)
AGE_MINUTES=$(( (NOW - LAST_TIMESTAMP) / 60 ))

if [ $AGE_MINUTES -gt 60 ]; then
  echo "ERROR: Checkpoint is $AGE_MINUTES minutes old"
  echo "Agent likely crashed. Requires recovery procedure."
  # Escalate to Primary
fi
```

---

## Performance Characteristics

**Checkpoint Overhead:**
- Create checkpoint: <1 second (JSON write)
- Update checkpoint: <1 second (JSON rewrite)
- Read checkpoint: <1 second (JSON read)
- Backup checkpoint: <1 second (file copy)
- **Total per heartbeat: ~2 seconds**

**Total Coordination Overhead (including checkpoints):**
- Heartbeat every 15 min: 2 seconds
- Check inbox: 3 seconds
- Update STATUS: 1 second
- **Total: ~6 seconds per heartbeat**

**For 3-feature epic (2.5 hours parallel work):**
- 10 heartbeats × 6 seconds = 60 seconds = 1 minute
- **Checkpoint overhead: <1% of parallel time** ✅

---

## Summary

**Checkpoint protocol provides:**
- ✅ Recoverable state (resume after crash)
- ✅ Stale detection (identify crashed agents)
- ✅ Recovery procedures (same agent, new agent, restart)
- ✅ Minimal overhead (<1% of parallel time)
- ✅ Automatic backups (last 10 checkpoints)

**Best practices:**
- Update checkpoint every 15 minutes (heartbeat)
- Update at phase transitions
- Include clear recovery instructions
- Backup before updating
- Verify checkpoint valid JSON after update
- Primary monitors all checkpoints for staleness

**Next:** See `stale_agent_protocol.md` for detailed stale detection and recovery workflows
