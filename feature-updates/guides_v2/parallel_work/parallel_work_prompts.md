# Parallel Work Prompts

**File:** `parallel_work/parallel_work_prompts.md`
**Version:** 1.0
**Created:** 2026-01-17
**Purpose:** Phase transition prompts for S2 parallel work scenarios

---

## Overview

This file contains **mandatory acknowledgment prompts** for parallel work during S2. These prompts ensure agents:
- Read the appropriate guide before starting parallel work
- Understand their role (Primary or Secondary)
- Follow coordination protocols correctly
- Acknowledge critical requirements

**Integration:** These prompts supplement the main `prompts_reference_v2.md` file.

---

## Prompt 1: Primary Agent - Starting Parallel S2

**When to use:** After S1 complete, user approved parallel work, handoff packages generated

**Acknowledgment required:** Yes (MANDATORY)

---

### Prompt Text

```markdown
═══════════════════════════════════════════════════════════
I'm starting S2 (Feature Deep Dives) in PARALLEL MODE as Primary Agent.

**My Role:** Coordinator + Feature 01 Owner

**Configuration:**
- Epic: {epic_name}
- Total Features: {N}
- My Assignment: feature_01_{name}
- Secondary Agents: {N-1} (Features 02-{N})

**Handoff Packages Generated:**
- {N-1} handoff packages created in agent_comms/
- User will spawn secondary agents using these packages

**Time Allocation:**
- 85% feature work (Feature 01 S2)
- 15% coordination (every 15 minutes)

**Coordination Infrastructure:**
- Checkpoints: agent_checkpoints/
- Messages: agent_comms/
- STATUS files: Per feature
- Locks: .epic_locks/

**I acknowledge these critical requirements:**

✅ I will coordinate every 15 minutes:
   - Update my checkpoint
   - Check ALL secondary inboxes
   - Process escalations within 15-minute SLA
   - Monitor checkpoint staleness (30 min warning, 60 min failure)
   - Update EPIC_README.md with lock protocol

✅ I will run S3 and S4 SOLO after all features complete S2

✅ I will verify sync point before S3:
   - All completion messages received
   - All STATUS files: READY_FOR_SYNC = true
   - All checkpoints fresh and WAITING_FOR_SYNC

✅ I will handle escalations within 15-minute SLA

✅ I will follow stale agent protocol if any agent exceeds thresholds

**Next Action:** Wait for secondary agents to send startup messages, then begin S2.P1 for Feature 01

**Reading Guide:** parallel_work/s2_primary_agent_guide.md
═══════════════════════════════════════════════════════════
```

---

## Prompt 2: Secondary Agent - Joining Parallel S2

**When to use:** User spawns you with handoff package content

**Acknowledgment required:** Yes (MANDATORY)

---

### Prompt Text

```markdown
═══════════════════════════════════════════════════════════
I'm joining as Secondary Agent for epic {epic_name}.

**My Role:** Feature Owner (single feature)

**Configuration:**
Epic Path: {epic_path}
My Assignment: {feature_folder}
Primary Agent ID: {primary_agent_id}
My Agent ID: {secondary_agent_id}
Starting Stage: S2.P1 (Feature Deep Dive - Research Phase)

**Time Allocation:**
- 90% feature work (my assigned feature S2)
- 10% coordination (every 15 minutes)

**Coordination Channels:**
- My Inbox: agent_comms/primary_to_{secondary_id}.md
- My Outbox: agent_comms/{secondary_id}_to_primary.md
- My Checkpoint: agent_checkpoints/{secondary_id}.json
- My STATUS: {feature_folder}/STATUS

**I acknowledge these critical requirements:**

✅ I will complete 10-step startup workflow:
   1. Parse handoff configuration
   2. Verify epic and feature paths
   3. Create communication channels
   4. Create checkpoint file
   5. Create STATUS file
   6. Update EPIC_README.md (with lock)
   7. Send initial message to Primary
   8. Confirm startup to user
   9. Begin S2.P1
   10. Set 15-minute coordination timer

✅ I will coordinate every 15 minutes:
   - Update checkpoint
   - Check inbox for Primary messages
   - Update STATUS file
   - Update EPIC_README.md (with lock)

✅ I will escalate blockers to Primary within 15 minutes

✅ After completing S2.P3, I will:
   - Send completion message to Primary
   - Update STATUS: READY_FOR_SYNC = true
   - Update checkpoint: WAITING_FOR_SYNC
   - WAIT for Primary to run S3 (do NOT proceed myself)

✅ I will NOT run S3 or S4 myself - Primary runs these solo

**Next Action:** Execute 10-step startup workflow, then begin S2.P1

**Reading Guide:** parallel_work/s2_secondary_agent_guide.md
═══════════════════════════════════════════════════════════
```

---

## Prompt 3: Coordination Heartbeat (Primary)

**When to use:** Every 15 minutes during S2.P1, S2.P2, or S2.P3

**Acknowledgment required:** No (procedural reminder)

---

### Prompt Text

```json
[15-minute timer expired - coordination heartbeat]

Pausing Feature 01 work for coordination (< 10% time overhead)...

**Coordination Checklist:**

1. ☐ Update my checkpoint (agent_checkpoints/primary.json)
2. ☐ Check ALL secondary inboxes:
   - agent_comms/secondary_a_to_primary.md
   - agent_comms/secondary_b_to_primary.md
   - agent_comms/secondary_c_to_primary.md
3. ☐ Process any escalations (15-minute SLA)
4. ☐ Check ALL STATUS files for blockers
5. ☐ Verify checkpoint staleness (30 min warning, 60 min failure)
6. ☐ Update EPIC_README.md (acquire lock first)
7. ☐ Set next 15-minute timer

**Escalation Processing:**
- If escalation found: Attempt to resolve (answer question, clarify spec)
- If requires user: Escalate to user immediately
- If resolved: Send response message to secondary
- Response SLA: Within 15 minutes

**Staleness Check:**
- If checkpoint age > 30 min: Send status check message
- If checkpoint age > 60 min: Escalate to user (stale agent protocol)

Coordination complete. Resuming Feature 01 work...
```

---

## Prompt 4: Coordination Heartbeat (Secondary)

**When to use:** Every 15 minutes during S2.P1, S2.P2, or S2.P3

**Acknowledgment required:** No (procedural reminder)

---

### Prompt Text

```json
[15-minute timer expired - coordination heartbeat]

Pausing feature work for coordination (< 10% time overhead)...

**Coordination Checklist:**

1. ☐ Update my checkpoint (agent_checkpoints/{my_id}.json)
2. ☐ Check my inbox (agent_comms/primary_to_{my_id}.md)
3. ☐ Process any messages from Primary
4. ☐ Update my STATUS file ({feature}/STATUS)
5. ☐ Update EPIC_README.md my section (acquire lock first)
6. ☐ Set next 15-minute timer

**If blocked >15 minutes:**
- Send escalation message to Primary
- Update STATUS: BLOCKERS = description
- Update checkpoint: "blockers": ["description"]
- Wait for Primary response (SLA: 15 minutes)

Coordination complete. Resuming feature work...
```

---

## Prompt 5: Sync Point Verification (Primary, before S3)

**When to use:** After Primary completes Feature 01 S2.P3, before starting S3

**Acknowledgment required:** Yes (MANDATORY GATE)

---

### Prompt Text

```markdown
═══════════════════════════════════════════════════════════
Feature 01 S2 complete. Verifying sync point before S3...

**Sync Point:** S2 → S3 (All Agents Complete S2)

**I acknowledge this is a MANDATORY GATE - cannot proceed to S3 without passing all verifications:**

**Verification 1: Completion Messages**
☐ Check agent_comms/secondary_a_to_primary.md for completion message
☐ Check agent_comms/secondary_b_to_primary.md for completion message
☐ Check agent_comms/secondary_c_to_primary.md for completion message

**Verification 2: STATUS Files**
☐ Read feature_02/STATUS - verify READY_FOR_SYNC: true
☐ Read feature_03/STATUS - verify READY_FOR_SYNC: true
☐ Read feature_04/STATUS - verify READY_FOR_SYNC: true

**Verification 3: Checkpoints**
☐ Read agent_checkpoints/secondary_a.json - verify WAITING_FOR_SYNC + fresh
☐ Read agent_checkpoints/secondary_b.json - verify WAITING_FOR_SYNC + fresh
☐ Read agent_checkpoints/secondary_c.json - verify WAITING_FOR_SYNC + fresh

**Verification 4: Feature Specs**
☐ Read feature_02/spec.md - verify Acceptance Criteria approved
☐ Read feature_03/spec.md - verify Acceptance Criteria approved
☐ Read feature_04/spec.md - verify Acceptance Criteria approved

**If ALL verifications pass:**
- Create sync verification document: epic/research/S3_SYNC_VERIFICATION_{date}.md
- Notify all secondaries: "S3 starting now"
- Proceed to S3

**If ANY verification fails:**
- Document which verification failed
- Update Agent Status: BLOCKERS = description
- Follow appropriate recovery protocol:
  - Missing completion message: Wait or send reminder
  - Stale checkpoint: Follow stale agent protocol
  - Incomplete spec: Send message to agent

**Reading Guide:** stages/s3/s3_cross_feature_sanity_check.md (Sync Verification section)
═══════════════════════════════════════════════════════════
```

---

## Prompt 6: Stale Agent Detected (Primary)

**When to use:** Checkpoint age exceeds 60 minutes during coordination heartbeat

**Acknowledgment required:** No (escalation procedure)

---

### Prompt Text

```markdown
🚨 STALE AGENT DETECTED

**Agent:** {agent_id}
**Feature:** {feature_folder}
**Last Checkpoint:** {timestamp} ({age} minutes ago)
**Last Known Stage:** {stage from checkpoint}
**Threshold Exceeded:** 60 minutes (FAILURE)

**Timeline:**
- {checkpoint_time}: Last checkpoint update
- {warning_time}: WARNING detected (30 min), status check sent
- {warning_time + 15 min}: No response received
- {now}: STALE confirmed (60+ min)

**Following stale agent protocol...**

**Escalating to user with recovery options:**

1. Resume Same Agent (if agent returns)
   - Agent reads checkpoint and continues
   - Recommended if: Session compacted

2. New Agent Takes Over
   - New agent reads checkpoint for context
   - Creates fresh checkpoint
   - Recommended if: Agent crashed

3. Primary Takes Over Feature
   - I absorb feature into my workload
   - Sequential instead of parallel
   - Recommended if: Cannot spawn new agent

**User decision required to proceed.**

**Guide:** parallel_work/stale_agent_protocol.md
```

---

## Prompt 7: Sync Timeout (Primary at S2→S3)

**When to use:** Waiting for secondaries to complete S2, exceeded time threshold

**Acknowledgment required:** No (escalation procedure)

---

### Prompt Text

```bash
🕒 SYNC TIMEOUT - S2 → S3

**Situation:** Parallel S2 work started {elapsed_hours} hours ago. Not all features have completed S2.

**Thresholds:**
- Soft timeout: 4 hours (reminder sent at {time})
- Hard timeout: 6 hours (NOW - escalating)

**Completion Status:**

| Agent | Feature | Status | Blockers | ETA |
|-------|---------|--------|----------|-----|
| Primary | Feature 01 | ✅ COMPLETE | None | N/A |
| Secondary-A | Feature 02 | ✅ COMPLETE | None | N/A |
| Secondary-B | Feature 03 | ⏳ IN_PROGRESS | {blockers} | {ETA} |

**Following sync timeout protocol...**

**Escalating to user with recovery options:**

1. Continue Waiting (if agent active with reasonable ETA)
2. Investigate Blocker (if specific blocker identified)
3. Abort Parallel for Late Feature (Primary takes over)
4. Proceed to S3 with Completed Features (risky - may need second S3 pass)

**User decision required to proceed.**

**Guide:** parallel_work/sync_timeout_protocol.md
```

---

## Prompt 8: Sync Timeout (Secondary at S4→S5)

**When to use:** Waiting for Primary to complete S3/S4, exceeded time threshold

**Acknowledgment required:** No (escalation procedure)

---

### Prompt Text

```bash
🕒 SYNC TIMEOUT - S4 → S5

**Situation:** Primary started S3/S4 {elapsed_hours} hours ago. Have not received completion signal.

**Thresholds:**
- Soft timeout: 2 hours (status check sent at {time})
- Hard timeout: 3 hours (NOW - escalating)

**Primary Status:**
- Last checkpoint: {timestamp} ({age} minutes ago)
- Current stage: {stage from checkpoint}
- Agent appears: {ACTIVE / STALE}

**Following sync timeout protocol...**

**Escalating to user with recovery options:**

1. Continue Waiting (if Primary active with fresh checkpoint)
2. New Agent Runs S3/S4 (if Primary stale)

**Note:** I cannot proceed to S5 without S3/S4 complete. S3/S4 require epic-level view that only Primary has.

**User decision required to proceed.**

**Guide:** parallel_work/sync_timeout_protocol.md
```

---

## Summary: Prompt Usage

**Primary Agent Prompts:**
1. Starting Parallel S2 (after S1, before S2.P1)
2. Coordination Heartbeat (every 15 minutes during S2)
3. Sync Point Verification (before S3)
4. Stale Agent Detected (if checkpoint > 60 min)
5. Sync Timeout at S2→S3 (if features not done)

**Secondary Agent Prompts:**
1. Joining Parallel S2 (startup from handoff)
2. Coordination Heartbeat (every 15 minutes during S2)
3. Sync Timeout at S4→S5 (if Primary delayed)

**Integration:**
- These prompts are referenced in parallel work guides
- Use in addition to standard prompts from `prompts_reference_v2.md`
- All "I acknowledge" prompts are MANDATORY (agents must use them)

---

**End of Parallel Work Prompts**
