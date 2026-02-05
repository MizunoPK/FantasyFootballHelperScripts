# Sync Timeout Protocol

**File:** `parallel_work/sync_timeout_protocol.md`
**Version:** 1.0
**Created:** 2026-01-17
**Purpose:** Define handling procedures when agents fail to reach sync points within expected timeframes

---

## Overview

During parallel S2 work, agents must synchronize at specific points:
- **S2 → S3 Sync Point:** All agents complete S2 before Primary runs S3
- **S4 → S5 Sync Point:** Primary completes S3/S4 before all agents proceed to S5

The **Sync Timeout Protocol** handles scenarios where agents don't reach sync points within expected timeframes.

**Who uses this:**
- **Primary Agent**: Monitors sync point readiness, handles timeouts

**When to use:**
- When waiting for agents to complete S2 (Primary ready for S3)
- When waiting for Primary to complete S3/S4 (Secondaries ready for S5)

---

## Sync Point 1: S2 → S3 (All Agents Complete S2)

### Expected Timeline

**Assumptions:**
- 3-feature epic (Primary + 2 Secondaries)
- Average S2 duration: 2-3 hours per feature
- Parallel work starts simultaneously

**Expected completion:**
- All agents should complete S2 within 3-4 hours
- Some variation expected (complex features take longer)

**Timeout thresholds:**
- **Soft timeout:** 4 hours (check status, send reminders)
- **Hard timeout:** 6 hours (escalate to user)

### Detection

**Primary agent tracks:**

1. **When did parallel S2 start?**
   - Timestamp when handoff packages generated
   - Example: 2026-01-17 10:00

2. **Current time:**
   - Example: 2026-01-17 14:30

3. **Elapsed time:**
   - Example: 4.5 hours

4. **How many agents have signaled completion?**
   - Check for completion messages in inbox
   - Example: 2/3 agents complete (Primary + Secondary-A), Secondary-B pending

### Soft Timeout Response (4 hours)

**Step 1: Check Completion Status**

**For EACH agent:**

**Read STATUS file:**
- File: `feature_{N}_{name}/STATUS`
- Check: `READY_FOR_SYNC: true` or `false`

**Read checkpoint:**
- File: `agent_checkpoints/{agent_id}.json`
- Check: `stage`, `status`, `last_checkpoint`

**Read inbox:**
- File: `agent_comms/{agent}_to_primary.md`
- Check for: Completion message

**Example results:**

| Agent | Feature | STATUS | Checkpoint Stage | Completion Message | Ready? |
|-------|---------|--------|------------------|-------------------|--------|
| Primary | Feature 01 | COMPLETE | S2.P3 | N/A (self) | YES |
| Secondary-A | Feature 02 | COMPLETE | S2.P3 | Received 14:00 | YES |
| Secondary-B | Feature 03 | IN_PROGRESS | S2.P3 | Not received | NO |

**Step 2: Identify Blockers**

**For agents NOT ready:**

**Read STATUS file blockers:**
```text
BLOCKERS: Waiting for user answer to Question 8
```

**Read checkpoint blockers:**
```json
{
  "blockers": ["User input needed for edge case handling"]
}
```

**Step 3: Send Reminder Message**

**If agent is active (checkpoint fresh) but not complete:**

**File:** `agent_comms/primary_to_secondary_b.md`

```markdown
## Message {N} (2026-01-17 14:30) ⏳ UNREAD
**Subject:** SYNC REMINDER - Waiting for S2 completion
**Action:** Please provide ETA for Feature 03 S2 completion
**Details:**
- Parallel S2 started: 2026-01-17 10:00 (4.5 hours ago)
- Feature 01 (Primary): COMPLETE
- Feature 02 (Secondary-A): COMPLETE
- Feature 03 (Secondary-B): IN_PROGRESS (you)

**Your Status:**
- Current stage: S2.P3
- Last checkpoint: 2026-01-17 14:25 (5 min ago) - ACTIVE
- Blockers: {from STATUS file}

**Next Steps:**
1. Provide ETA for S2.P3 completion
2. If blocked, escalate immediately (don't wait)
3. If need help, request assistance

**Sync Impact:**
- Cannot start S3 (Cross-Feature Sanity Check) until all features complete S2
- Other agents waiting on you

**Please respond within 30 minutes with ETA or escalation.**
```

**Step 4: Wait for Response**

**Set timer:** 30 minutes

**During wait:**
- Continue monitoring checkpoint freshness
- Process any other messages
- Update EPIC_README.md with sync status

**Step 5: Evaluate Response**

**If agent responds with ETA:**
- ✅ Document ETA
- Wait until ETA expires
- If ETA reasonable (< 2 hours): Continue waiting
- If ETA unreasonable (> 2 hours): Escalate to user

**If agent reports blocker:**
- Address blocker if within Primary's scope (answer question, clarify requirement)
- If blocker requires user: Escalate immediately
- Update agent with resolution

**If NO response after 30 minutes:**
- Check checkpoint staleness
- If stale (> 30 min): Follow stale agent protocol
- If active but no response: Proceed to hard timeout

### Hard Timeout Response (6 hours)

**Step 1: Document Timeout**

**Update EPIC_README.md:**

```markdown
## Sync Points

**S2 → S3 Sync Point:**
- **Status:** TIMEOUT (6+ hours elapsed)
- **Started:** 2026-01-17 10:00
- **Timeout:** 2026-01-17 16:00
- **Ready:** 2/3 agents (Feature 01, Feature 02 complete; Feature 03 pending)
- **User Escalated:** YES (2026-01-17 16:00)
```

**Step 2: Escalate to User**

**Message to user:**

```markdown
🕒 **SYNC TIMEOUT - S2 → S3**

**Situation:**
Parallel S2 work started 6 hours ago. Not all features have completed S2.

**Timeline:**
- Started: 2026-01-17 10:00
- Expected completion: 3-4 hours (by 14:00)
- Soft timeout: 4 hours (14:00) - reminder sent
- Hard timeout: 6 hours (16:00) - NOW

**Completion Status:**

| Agent | Feature | Status | Blockers | ETA |
|-------|---------|--------|----------|-----|
| Primary | Feature 01 | ✅ COMPLETE | None | N/A |
| Secondary-A | Feature 02 | ✅ COMPLETE | None | N/A |
| Secondary-B | Feature 03 | ⏳ IN_PROGRESS | {blocker description} | {ETA or "No response"} |

**Agent Health:**
- Secondary-B checkpoint: {timestamp} ({age} minutes ago)
- Secondary-B last message: {timestamp}
- Agent appears: {ACTIVE / STALE / UNKNOWN}

**Impact:**
- Cannot start S3 (Cross-Feature Sanity Check) until Feature 03 completes S2
- Features 01 and 02 are blocked waiting

**Recovery Options:**

**Option 1: Continue Waiting (if agent active with ETA)**
- Reasonable if: Agent provided recent ETA < 1 hour
- Recommendation: Wait until ETA, then escalate if missed
- Risk: Delays entire epic by wait time

**Option 2: Investigate Blocker (if specific blocker identified)**
- I can: Answer questions, provide clarifications within my scope
- User must: Answer user preference questions, resolve spec ambiguities
- Recommendation: If blocker is user question, answer now to unblock

**Option 3: Abort Parallel Work for Feature 03**
- I (Primary) take over Feature 03
- Complete Feature 03 S2 sequentially
- Delays S3 start but guarantees progress
- Recommendation: If agent stale or no clear ETA

**Option 4: Proceed to S3 with 2 Features (risky)**
- Run S3 comparing only Features 01-02
- Feature 03 completes S2 independently
- Re-run S3 after Feature 03 done to catch conflicts
- Recommendation: ONLY if Feature 03 is isolated/independent
- Risk: May find conflicts in second S3 pass requiring rework

**What would you like me to do?**
```

**Step 3: Wait for User Decision**

**Update Agent Status:**
```markdown
**Blockers:** SYNC TIMEOUT - Waiting for user decision on Feature 03 completion
**Next Action:** User to choose recovery option (1-4)
```

**Pause S3 work:** Cannot proceed until decision made

**Step 4: Execute User's Choice**

**If Option 1 (Continue Waiting):**
- Set new timeout based on ETA
- Monitor agent closely
- If new timeout missed, escalate again with stronger recommendation to abort

**If Option 2 (Investigate Blocker):**
- Address blocker (answer question, clarify spec)
- Notify agent: "Blocker resolved: {resolution}"
- Set 1-hour timeout for completion after blocker resolved
- If timeout missed, escalate with Option 3 recommendation

**If Option 3 (Abort Parallel for Feature 03):**
- Send message to Secondary-B: "Primary taking over Feature 03, please pause work"
- Wait for acknowledgment (15 min)
- Primary reads Feature 03 checkpoint
- Primary completes Feature 03 S2 sequentially
- Update EPIC_README.md: Parallel mode downgraded to partial

**If Option 4 (Proceed to S3 with 2 Features):**
- **HIGH RISK - User explicitly chose this**
- Document decision in EPIC_README.md
- Run S3 comparing Features 01-02 only
- Mark Feature 03 as "Deferred from S3 pass 1"
- After Feature 03 completes S2:
  - Re-run S3 pairwise comparison: Feature 03 vs Feature 01, Feature 03 vs Feature 02
  - Resolve any conflicts found
  - Update specs as needed

---

## Sync Point 2: S4 → S5 (Primary Completes S3/S4)

### Expected Timeline

**Assumptions:**
- S3: 30-60 minutes (cross-feature sanity check)
- S4: 30-45 minutes (epic testing strategy update)
- Total: 1-2 hours for Primary to complete both

**Timeout thresholds:**
- **Soft timeout:** 2 hours (secondary agents check status)
- **Hard timeout:** 3 hours (secondary agents escalate to user)

### Detection

**Secondary agents track:**

1. **When did S3 start?**
   - Timestamp from Primary's notification: "S3 starting now"
   - Example: 2026-01-17 15:00

2. **Current time:**
   - Example: 2026-01-17 17:30

3. **Elapsed time:**
   - Example: 2.5 hours

4. **Has Primary signaled S4 complete?**
   - Check inbox for "S4 complete - proceed to S5" message
   - Example: No message received

### Soft Timeout Response (2 hours)

**Step 1: Check Primary's Status**

**Read Primary's checkpoint:**
- File: `agent_checkpoints/{primary_agent_id}.json`
- Check: `stage`, `last_checkpoint`

**Example:**
```json
{
  "agent_id": "Primary",
  "stage": "S4",
  "phase": "Updating epic_smoke_test_plan.md",
  "last_checkpoint": "2026-01-17T17:15:00Z",
  "status": "IN_PROGRESS"
}
```

**Checkpoint age:** 15 minutes (ACTIVE)

**Step 2: Send Status Check**

**File:** `agent_comms/secondary_a_to_primary.md`

```markdown
## Message {N} (2026-01-17 17:00) ⏳ UNREAD
**Subject:** STATUS CHECK - S4 completion ETA?
**Action:** Please provide ETA for S4 completion
**Details:**
- S3/S4 started: 2026-01-17 15:00 (2 hours ago)
- Expected duration: 1-2 hours
- Your checkpoint shows: S4 in progress (last update 15 min ago)

**We are ready:**
- Feature 02 (Secondary-A): Waiting to proceed to S5
- Feature 03 (Secondary-B): Waiting to proceed to S5

**Request:**
- ETA for S4 completion?
- Any blockers we should know about?

**No urgency** - just checking in. Reply when convenient.
```

**Step 3: Wait for Response**

**Set timer:** 30 minutes

**If Primary responds:**
- ✅ Document ETA
- Continue waiting
- Update other secondaries with ETA

**If NO response after 30 minutes:**
- Check checkpoint staleness
- If stale: Proceed to hard timeout
- If active: Wait another 30 minutes (total 1 hour)

### Hard Timeout Response (3 hours)

**Step 1: Verify Primary Staleness**

**Check checkpoint age:**
- > 30 minutes = WARNING
- > 60 minutes = STALE

**Step 2: Escalate to User**

**Secondary agent messages user:**

```markdown
🕒 **SYNC TIMEOUT - S4 → S5**

**Situation:**
Primary agent started S3/S4 three hours ago. Have not received completion signal.

**Timeline:**
- S3/S4 started: 2026-01-17 15:00
- Expected completion: 1-2 hours (by 17:00)
- Soft timeout: 2 hours (17:00) - status check sent
- Hard timeout: 3 hours (18:00) - NOW

**Primary Status:**
- Last checkpoint: {timestamp} ({age} minutes ago)
- Current stage: {stage from checkpoint}
- Agent appears: {ACTIVE / STALE}

**Secondary Agents Waiting:**
- Secondary-A (Feature 02): Completed S2, ready for S5
- Secondary-B (Feature 03): Completed S2, ready for S5

**Recovery Options:**

**Option 1: Continue Waiting (if Primary active)**
- Wait another hour
- Check staleness every 15 minutes
- Recommendation: If Primary checkpoint is fresh (< 15 min)

**Option 2: New Agent Runs S3/S4 (if Primary stale)**
- Spawn new Primary agent to complete S3/S4
- Reads stale checkpoint for context
- Completes S3/S4, then notifies secondaries
- Recommendation: If Primary checkpoint > 60 minutes old

**What would you like me to do?**

**Note:** I (Secondary-A) cannot proceed to S5 without S3/S4 complete. S3/S4 require epic-level view that only Primary has.
```

**Step 3: Wait for User Decision**

**Update Agent Status:**
```markdown
**Blockers:** SYNC TIMEOUT (S4 → S5) - Waiting for user decision
**Next Action:** User to choose recovery option
```

---

## Prevention Best Practices

### For All Agents

1. **Provide ETAs proactively**
   - If you're taking longer than expected, send ETA update
   - Don't wait for reminder message

2. **Escalate blockers immediately**
   - If user input needed, escalate within 15 minutes (not hours)
   - Don't let blockers cause sync timeouts

3. **Update checkpoints frequently**
   - Every 15 minutes during active work
   - Helps others distinguish "working" from "stale"

4. **Communicate delays early**
   - If complex feature will exceed expected time, notify Primary ASAP
   - Allows Primary to adjust expectations or offer help

### For Primary Agent

1. **Set realistic expectations**
   - Tell secondaries expected S3/S4 duration
   - Update if taking longer than expected

2. **Monitor soft timeouts**
   - Check sync readiness at 4-hour mark (don't wait for 6)
   - Early intervention prevents hard timeouts

3. **Offer assistance before escalating**
   - If secondary blocked, try to help
   - Escalate to user only if blocker requires user input

---

## Summary

**Sync Point 1 (S2 → S3):**
- Soft timeout: 4 hours (send reminder)
- Hard timeout: 6 hours (escalate to user)
- Recovery: Wait, investigate blocker, Primary takes over, or proceed with partial

**Sync Point 2 (S4 → S5):**
- Soft timeout: 2 hours (send status check)
- Hard timeout: 3 hours (escalate to user)
- Recovery: Wait or spawn new Primary agent

**Key Principle:** Communicate early and often to prevent timeouts

**See Also:**
- `parallel_work/stale_agent_protocol.md` - Handling crashed/hung agents
- `parallel_work/communication_protocol.md` - Message formats and channels
- `parallel_work/s2_parallel_protocol.md` - Overall parallel work workflow

---

**End of Sync Timeout Protocol**
