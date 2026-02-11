# S2 Handoff Package Template

**Purpose:** Template for generating handoff packages for secondary agents in S2 parallelization

**Usage:** Primary agent fills in placeholders (marked with `{...}`) and provides to user

---

## Handoff Package Format

```markdown
═══════════════════════════════════════════════════════════
I'm joining as a secondary agent for epic {EPIC_NAME}.

**Configuration:**
Epic Path: {EPIC_PATH}
My Assignment: {FEATURE_FOLDER}
Primary Agent ID: {PRIMARY_AGENT_ID}
My Agent ID: {SECONDARY_AGENT_ID}
Starting Stage: S2.P1 (Feature Deep Dive - Research Phase)

**Coordination:**
- Inbox: agent_comms/primary_to_{secondary_id}.md (check before every action)
- Outbox: agent_comms/{secondary_id}_to_primary.md (send updates)
- Checkpoint: agent_checkpoints/{secondary_id}.json (update every 15 min)
- STATUS: {FEATURE_FOLDER}/STATUS (update at phase transitions)

**Sync Points:**
- After S2.P3 complete: Signal completion, WAIT for Primary to run S3
- After Primary completes S3: Proceed to implementation (sequential in S2 plan)

Begin S2.P1 now.
═══════════════════════════════════════════════════════════
```

---

## Example (Filled In)

```markdown
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
- After Primary completes S3: Proceed to implementation (sequential in S2 plan)

Begin S2.P1 now.
═══════════════════════════════════════════════════════════
```

---

## Placeholder Mapping

| Placeholder | Description | Example |
|-------------|-------------|---------|
| `{EPIC_NAME}` | Epic folder name (KAI-N-name format) | KAI-6-nfl_team_penalty |
| `{EPIC_PATH}` | Full absolute path to epic folder | C:/Users/.../KAI-6-nfl_team_penalty |
| `{FEATURE_FOLDER}` | Feature folder name assigned to this secondary | feature_02_team_penalty |
| `{PRIMARY_AGENT_ID}` | Primary agent's unique ID | Agent-abc123 |
| `{SECONDARY_AGENT_ID}` | This secondary agent's ID | Secondary-A, Secondary-B, etc. |
| `{secondary_id}` | Lowercase agent ID for file names | secondary_a, secondary_b, etc. |

---

## Generation Code (Primary Agent)

```bash
generate_s2_handoff_package() {
  local EPIC_NAME=$1           # e.g. "KAI-6-nfl_team_penalty"
  local EPIC_PATH=$2           # e.g. "C:/Users/.../KAI-6-nfl_team_penalty"
  local FEATURE_FOLDER=$3      # e.g. "feature_02_team_penalty"
  local PRIMARY_AGENT_ID=$4    # e.g. "Agent-abc123"
  local SECONDARY_AGENT_ID=$5  # e.g. "Secondary-A"

  # Lowercase agent ID for filenames
  local SECONDARY_ID_LOWER=$(echo "$SECONDARY_AGENT_ID" | tr '[:upper:]' '[:lower:]' | sed 's/-/_/g')

  cat <<EOF
═══════════════════════════════════════════════════════════
I'm joining as a secondary agent for epic $EPIC_NAME.

**Configuration:**
Epic Path: $EPIC_PATH
My Assignment: $FEATURE_FOLDER
Primary Agent ID: $PRIMARY_AGENT_ID
My Agent ID: $SECONDARY_AGENT_ID
Starting Stage: S2.P1 (Feature Deep Dive - Research Phase)

**Coordination:**
- Inbox: agent_comms/primary_to_$SECONDARY_ID_LOWER.md (check before every action)
- Outbox: agent_comms/${SECONDARY_ID_LOWER}_to_primary.md (send updates)
- Checkpoint: agent_checkpoints/$SECONDARY_ID_LOWER.json (update every 15 min)
- STATUS: $FEATURE_FOLDER/STATUS (update at phase transitions)

**Sync Points:**
- After S2.P3 complete: Signal completion, WAIT for Primary to run S3
- After Primary completes S3: Proceed to implementation (sequential in S2 plan)

Begin S2.P1 now.
═══════════════════════════════════════════════════════════
EOF
}

## Usage:
generate_s2_handoff_package \
  "KAI-6-nfl_team_penalty" \
  "C:/Users/kmgam/code/FantasyFootballHelperScripts/feature-updates/KAI-6-nfl_team_penalty" \
  "feature_02_team_penalty" \
  "Agent-abc123" \
  "Secondary-A"
```

---

## User Workflow

1. **Primary generates handoff packages** (one per secondary agent)
2. **Primary presents packages to user** with copy-paste instructions
3. **User opens new Claude Code sessions** (one per secondary agent)
4. **User copies handoff package** into each new session
5. **Secondary agent self-configures** from handoff package
6. **Secondary agent begins S2.P1** immediately

---

## Secondary Agent Self-Configuration

**When secondary agent receives handoff package:**

1. **Parse configuration:**
   - Extract epic path
   - Extract feature assignment
   - Extract agent ID
   - Extract coordination file paths

2. **Verify paths exist:**
   ```bash
   # Verify epic folder exists
   if [ ! -d "$EPIC_PATH" ]; then
     echo "ERROR: Epic path not found: $EPIC_PATH"
     exit 1
   fi

   # Verify feature folder exists
   if [ ! -d "$EPIC_PATH/$FEATURE_FOLDER" ]; then
     echo "ERROR: Feature folder not found"
     exit 1
   fi
   ```

3. **Create coordination infrastructure:**
   ```bash
   # Create agent_comms directory if needed
   mkdir -p "$EPIC_PATH/agent_comms"

   # Create inbox file
   cat > "$EPIC_PATH/agent_comms/primary_to_secondary_a.md" <<EOF
## Messages: Primary → Secondary-A

(No messages yet)
EOF

   # Create outbox file
   cat > "$EPIC_PATH/agent_comms/secondary_a_to_primary.md" <<EOF
## Messages: Secondary-A → Primary

(No messages yet)
EOF
   ```

4. **Create checkpoint file:**
   ```bash
   # Create checkpoints directory if needed
   mkdir -p "$EPIC_PATH/agent_checkpoints"

   # Create initial checkpoint
   # (See checkpoint_protocol.md for format)
   ```

5. **Create STATUS file:**
   ```bash
   # Create STATUS file
   cat > "$EPIC_PATH/$FEATURE_FOLDER/STATUS" <<EOF
STAGE: S2.P1
PHASE: Research Phase
AGENT: $SECONDARY_AGENT_ID
AGENT_ID: $(uuidgen)
UPDATED: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
STATUS: IN_PROGRESS
BLOCKERS: none
NEXT_ACTION: Begin S2.P1 Research Phase
READY_FOR_SYNC: false
ESTIMATED_COMPLETION: $(date -u -d "+2 hours" +"%Y-%m-%dT%H:%M:%SZ")
EOF
   ```

6. **Update EPIC_README.md:**
   - Acquire lock
   - Add secondary agent to Agent Assignment table
   - Create secondary agent progress section
   - Release lock

7. **Send initial message to Primary:**
   ```markdown
   ## Message 1 (TIMESTAMP) ⏳ UNREAD
   **Subject:** Secondary Agent Started
   **Action:** I've started work on FEATURE_FOLDER
   **Details:** Handoff package received and configuration complete
   **Next:** Beginning S2.P1 Research Phase now
   **Acknowledge:** No action needed
   ```

8. **Begin S2.P1:**
   - Read guide: `stages/s2/s2_p1_research.md`
   - Follow guide steps
   - Update checkpoint every 15 min
   - Check inbox every 15 min

---

## Notes

- Handoff package is **copy-paste ready** (no manual editing by user)
- All configuration is **auto-populated by Primary**
- Secondary agent **self-configures from package**
- **Minimal user effort** (just paste and go)
- Package can be **reused if agent crashes** (same configuration)
