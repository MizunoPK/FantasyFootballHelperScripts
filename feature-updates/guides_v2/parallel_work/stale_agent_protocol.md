# Stale Agent Protocol

**File:** `parallel_work/stale_agent_protocol.md`
**Version:** 1.0
**Created:** 2026-01-17
**Purpose:** Define detection and recovery procedures for stale/crashed agents during parallel S2 work

---

## Overview

During parallel S2 work, agents may crash, hang, or become unresponsive. The **Stale Agent Protocol** ensures:
1. Early detection of inactive agents (checkpoints monitor health)
2. Systematic recovery procedures (ping → wait → escalate)
3. Minimal disruption to other agents (parallel work continues where possible)
4. State preservation through checkpoints (work not lost)

**Who uses this:**
- **Primary Agent**: Monitors all secondary agent health during coordination heartbeat
- **Secondary Agents**: Self-report status via checkpoint updates

**When to use:**
- Every 15 minutes during coordination heartbeat (preventive monitoring)
- When agent checkpoint timestamp exceeds thresholds
- When agent doesn't respond to messages within SLA

---

## Staleness Thresholds

### Warning Threshold: 30 Minutes

**Definition:** Agent's last checkpoint update is >30 minutes old

**Interpretation:**
- Agent may be working on complex task without updating
- Agent may be slow or experiencing issues
- Not yet a failure, but requires attention

**Action:** Send status check message, monitor closely

### Failure Threshold: 60 Minutes

**Definition:** Agent's last checkpoint update is >60 minutes old

**Interpretation:**
- Agent has likely crashed or hung
- Work is stalled
- Requires intervention

**Action:** Escalate to user for recovery decision

---

## Detection Protocol

### Step 1: Read Checkpoint File

**Primary agent checks each secondary agent's checkpoint file:**

**File:** `agent_checkpoints/{secondary_agent_id}.json`

**Read field:** `last_checkpoint` (timestamp)

**Example:**
```json
{
  "agent_id": "Secondary-A",
  "last_checkpoint": "2026-01-17T10:15:00Z",
  "stage": "S2.P2",
  "status": "IN_PROGRESS"
}
```markdown

### Step 2: Calculate Age

**Current time:** {now}
**Last checkpoint:** {last_checkpoint from JSON}
**Age:** {now - last_checkpoint} in minutes

**Example:**
- Current time: 2026-01-17T11:00:00Z
- Last checkpoint: 2026-01-17T10:15:00Z
- Age: 45 minutes

### Step 3: Compare to Thresholds

**Decision tree:**

```text
Age < 30 minutes → ✅ ACTIVE (no action needed)
30 ≤ Age < 60 minutes → ⚠️ WARNING (send status check)
Age ≥ 60 minutes → ❌ STALE (escalate to user)
```markdown

### Step 4: Document Check

**Update EPIC_README.md Stale Agent Checks table:**

```markdown
| Check Time | Agent | Last Checkpoint | Status | Action Taken |
|------------|-------|----------------|--------|--------------|
| 2026-01-17 11:00 | Secondary-A | 2026-01-17 10:15 (45 min ago) | WARNING | Status check sent |
```markdown

---

## Recovery Procedures

### Scenario A: WARNING Status (30-60 minutes)

**Step A.1: Send Status Check Message**

**File:** `agent_comms/primary_to_secondary_{x}.md`

**Message template:**
```markdown
## Message {N} (2026-01-17 11:00) ⏳ UNREAD
**Subject:** STATUS CHECK - Are you still active?
**Action:** Please respond within 15 minutes
**Details:**
- Your last checkpoint: 2026-01-17 10:15 (45 minutes ago)
- Current stage from checkpoint: S2.P2
- Expected: Checkpoint updates every 15 minutes

**If you're still working:**
- Update your checkpoint immediately
- Reply to this message with current status
- Continue your work

**If you encountered issues:**
- Describe the blocker
- Update STATUS file with blocker description
- I'll help resolve or escalate to user

**Response deadline:** 2026-01-17 11:15 (15 min from now)
```markdown

**Step A.2: Wait 15 Minutes**

**Set timer:** 15 minutes from message send time

**During wait:**
- Continue with Primary's own feature work
- Check other secondaries' health
- Process any incoming messages

**Step A.3: Check for Response**

**After 15 minutes, check inbox:**

**File:** `agent_comms/secondary_{x}_to_primary.md`

**Look for:**
- New message from secondary
- Acknowledgment of status check
- Updated checkpoint timestamp

**If response received:**
- ✅ Agent is active, warning resolved
- Document in EPIC_README.md: "Status: ACTIVE (responded to check)"
- Continue normal coordination

**If NO response received:**
- Age is now 60+ minutes (WARNING → STALE)
- Proceed to Scenario B

---

### Scenario B: STALE Status (60+ minutes)

**Step B.1: Mark Agent as Stale**

**Update EPIC_README.md:**

```markdown
## Coordination Status

**Stale Agents Detected:**

| Agent | Feature | Last Checkpoint | Age | Status | User Notified |
|-------|---------|----------------|-----|--------|---------------|
| Secondary-A | feature_02_{name} | 2026-01-17 10:15 | 75 min | STALE | YES (2026-01-17 11:30) |
```markdown

**Step B.2: Escalate to User**

**Message to user:**

```markdown
🚨 **STALE AGENT DETECTED**

**Agent:** Secondary-A
**Assigned Feature:** Feature 02 ({feature_name})
**Last Checkpoint:** 2026-01-17 10:15 (75 minutes ago)
**Last Known Stage:** S2.P2 (Specification Phase)

**Timeline:**
- 10:15: Last checkpoint update
- 11:00: WARNING detected (45 min old)
- 11:00: Status check message sent
- 11:15: No response received
- 11:30: STALE status confirmed (75 min old)

**Current Situation:**
- Agent has not updated checkpoint for 75 minutes
- Agent did not respond to status check within 15 min SLA
- Likely crashed or session compacted
- Work on Feature 02 is stalled

**Recovery Options:**

**Option 1: Resume Same Agent (if agent returns)**
- Same agent ID can resume from checkpoint
- Checkpoint shows: S2.P2 in progress, 80% done
- Agent reads checkpoint and continues where left off
- Recommended if: Agent session compacted but will return

**Option 2: New Agent Takes Over (if agent not returning)**
- New agent assigned with fresh Agent ID
- Reads stale agent's checkpoint for context
- Continues Feature 02 from S2.P2
- Recommended if: Agent crashed and won't return

**Option 3: Primary Takes Over Feature 02**
- I (Primary) absorb Feature 02 into my workload
- Continue sequentially instead of parallel
- Longer total time but guaranteed progress
- Recommended if: Cannot spawn new agent

**What would you like me to do?**
```markdown

**Step B.3: Wait for User Decision**

**Update Agent Status:**
```markdown
**Blockers:** Waiting for user decision on stale agent recovery (Secondary-A, Feature 02)
**Next Action:** User to choose recovery option
```markdown

**Pause Feature 02 work:** Cannot proceed until recovery decision made

**Continue other work:**
- Primary continues Feature 01
- Other secondaries (Secondary-B, Secondary-C) continue their features
- Parallel work partially continues

---

### Scenario C: Agent Resumes (Same Agent)

**User chose Option 1: Resume same agent**

**Step C.1: Verify Agent Return**

**Wait for agent to:**
- Send message: "I'm back, resuming from checkpoint"
- Update checkpoint with fresh timestamp
- Update STATUS file

**Step C.2: Agent Reads Checkpoint**

**Agent (Secondary-A) reads:**

**File:** `agent_checkpoints/secondary_a.json`

**Checkpoint shows:**
```json
{
  "agent_id": "Secondary-A",
  "stage": "S2.P2",
  "current_step": "Writing Acceptance Criteria in spec.md",
  "files_modified": ["spec.md", "checklist.md"],
  "recovery_instructions": "Resume from S2.P2, 80% done. Complete Acceptance Criteria section."
}
```markdown

**Step C.3: Agent Resumes Work**

**Agent continues from checkpoint:**
- Uses "Resuming In-Progress Epic" prompt (from prompts_reference_v2.md)
- Reads S2.P2 guide
- Continues from "current_step" in checkpoint
- Updates checkpoint immediately to mark active

**Step C.4: Primary Verifies Resume**

**Primary checks:**
- New checkpoint timestamp (should be fresh)
- Message from agent confirming resume
- STATUS file updated

**If verification passes:**
- ✅ Agent successfully resumed
- Update EPIC_README.md: "Stale agent recovered, work resumed"
- Continue normal coordination

---

### Scenario D: New Agent Takes Over

**User chose Option 2: New agent takes over**

**Step D.1: User Spawns New Agent**

**User creates new agent session with handoff:**

```markdown
I'm taking over Feature 02 ({feature_name}) from a stale agent.

**Configuration:**
Epic Path: {epic_path}
My Assignment: feature_02_{name}
Primary Agent ID: {primary_id}
My Agent ID: Secondary-A-New
Starting Stage: S2.P2 (resuming from stale agent's checkpoint)

**Previous Agent:**
- Agent ID: Secondary-A (stale)
- Last checkpoint: agent_checkpoints/secondary_a.json
- Work completed: S2.P1 complete, S2.P2 80% done

**Recovery Instructions:**
1. Read stale agent's checkpoint for context
2. Read S2.P2 guide
3. Continue from "current_step" in checkpoint
4. Create NEW checkpoint file: agent_checkpoints/secondary_a_new.json
5. Update feature_02/STATUS with new agent ID
6. Send message to Primary confirming takeover

Begin now.
```markdown

**Step D.2: New Agent Reads Stale Checkpoint**

**New agent reads (for context only):**

**File:** `agent_checkpoints/secondary_a.json` (stale agent's checkpoint)

**Uses to understand:**
- What work was completed
- What was in progress
- Where to resume from

**Step D.3: New Agent Creates Fresh Checkpoint**

**New agent creates:**

**File:** `agent_checkpoints/secondary_a_new.json`

```json
{
  "agent_id": "Secondary-A-New",
  "session_id": "xyz789",
  "feature": "feature_02_team_penalty",
  "stage": "S2.P2",
  "last_checkpoint": "2026-01-17T12:00:00Z",
  "status": "IN_PROGRESS",
  "can_resume": true,
  "previous_agent": "Secondary-A",
  "recovery_notes": "Took over from stale agent at S2.P2, resuming Acceptance Criteria section"
}
```markdown

**Step D.4: Update Coordination Channels**

**New agent updates:**

**EPIC_README.md:**
```markdown
| Agent ID | Role | Assigned Feature | Status | Last Checkpoint |
|----------|------|------------------|--------|----------------|
| Secondary-A-New | Feature Owner | feature_02_{name} | IN_PROGRESS | 2026-01-17 12:00 |
```markdown

**Communication files (rename):**
- Old: `agent_comms/primary_to_secondary_a.md`
- New: `agent_comms/primary_to_secondary_a_new.md`
- Copy old messages for context, continue fresh

**STATUS file:**
```text
AGENT: Secondary-A-New
AGENT_ID: xyz789
```markdown

**Step D.5: New Agent Sends Confirmation**

**File:** `agent_comms/secondary_a_new_to_primary.md`

**Message:**
```markdown
## Message 1 (2026-01-17 12:00) ⏳ UNREAD
**Subject:** New agent taking over Feature 02
**Action:** I've successfully taken over from stale agent
**Details:**
- Previous agent: Secondary-A (stale at 2026-01-17 10:15)
- Reviewed checkpoint: S2.P2 in progress, Acceptance Criteria 80% done
- Created fresh checkpoint: agent_checkpoints/secondary_a_new.json
- Updated EPIC_README.md and STATUS file

**Current Status:**
- Resuming S2.P2 from Acceptance Criteria section
- ETA to complete S2.P2: 30 minutes
- No blockers

**Acknowledge:** Please confirm you received this takeover notification
```markdown

**Step D.6: Primary Acknowledges**

**Primary verifies:**
- New checkpoint file exists and is fresh
- EPIC_README.md updated
- Communication channels updated

**Primary sends acknowledgment:**

**File:** `agent_comms/primary_to_secondary_a_new.md`

```markdown
## Message 1 (2026-01-17 12:05) ⏳ UNREAD
**Subject:** Takeover confirmed
**Action:** Continue with Feature 02 S2.P2
**Details:**
- Confirmed new checkpoint file created
- Confirmed EPIC_README.md updated
- Feature 02 work can proceed

**Next:** Complete S2.P2, signal when ready for S2.P3

**Acknowledge:** No action needed
```markdown

---

### Scenario E: Primary Takes Over

**User chose Option 3: Primary absorbs Feature 02**

**Step E.1: Update Work Mode**

**EPIC_README.md:**
```markdown
## Parallel Work Configuration

**Status:** PARTIAL PARALLEL (downgraded from full parallel)

**Primary Agent:**
- Assigned Features: feature_01_{name}, feature_02_{name} (absorbed from stale Secondary-A)

**Secondary Agents:**
- Secondary-B: feature_03_{name} (continues parallel)
- Secondary-C: feature_04_{name} (continues parallel)
```

**Step E.2: Primary Reads Stale Checkpoint**

**Primary reads:**

**File:** `agent_checkpoints/secondary_a.json`

**For context:**
- S2.P2 in progress, 80% done
- Acceptance Criteria section needs completion

**Step E.3: Primary Completes Feature 02**

**Primary works sequentially:**
1. Complete Feature 01 S2 (primary's original assignment)
2. Then start/resume Feature 02 S2 from checkpoint
3. Continue coordination with Secondary-B and Secondary-C in parallel

**Time impact:**
- Feature 02 no longer parallel
- Total epic time increases (lost parallelization benefit for Feature 02)
- But work guaranteed to complete

---

## Prevention Best Practices

### For Secondary Agents

1. **Update checkpoint every 15 minutes religiously**
   - Set actual timer, don't rely on memory
   - Even if "not much progress", update timestamp

2. **Before session compaction warning:**
   - Update checkpoint immediately
   - Send message to Primary: "Session compacting soon, checkpoint updated"

3. **If blocked, communicate early:**
   - Don't wait 30 minutes to report blocker
   - Send escalation immediately when stuck

4. **Self-monitor checkpoint age:**
   - If you notice your last update was >15 min ago, update now
   - Don't wait for Primary to catch it

### For Primary Agent

1. **Check all secondary checkpoints every 15 minutes**
   - Part of coordination heartbeat
   - Don't skip staleness checks

2. **Send status check at 30 min (not 60 min):**
   - Early intervention increases recovery success
   - Agent may just be focused, not stale

3. **Document all checks:**
   - Helps user understand timeline if escalation needed
   - Shows due diligence

4. **Keep work flowing:**
   - Don't block all work on one stale agent
   - Other secondaries and Primary continue
   - Only blocked feature stops

---

## Summary

**Detection:**
- 30 minutes = WARNING (send status check)
- 60 minutes = STALE (escalate to user)

**Recovery:**
- Same agent resumes from checkpoint (preferred)
- New agent takes over from checkpoint (if original won't return)
- Primary absorbs feature (fallback)

**Key Principle:** Checkpoints enable recovery with minimal work loss

**See Also:**
- `parallel_work/checkpoint_protocol.md` - Checkpoint format and update frequency
- `parallel_work/s2_parallel_protocol.md` - Overall parallel work workflow
- `parallel_work/communication_protocol.md` - How to send messages to agents

---

**End of Stale Agent Protocol**
