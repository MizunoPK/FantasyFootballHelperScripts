# S3: Cross-Feature Sanity Check
## Parallel Work Sync Verification (Optional)

**When to use:** Only when S2 was executed in parallel mode (Primary + Secondary agents)

**Skip this:** If S2 was done sequentially (single agent)

**Purpose:** Verify all secondary agents completed S2 properly before Primary begins S3

**Time:** 15-20 minutes

---

---

### Step 0.1: Check Completion Messages

**For EACH secondary agent:**

1. **Read inbox file:**
   - File: `agent_comms/secondary_{x}_to_primary.md`
   - Look for: Final completion message with "S2 complete - ready for sync"

2. **Verify message contents:**
   - Completion timestamp exists
   - Feature number and name match
   - Blockers: none
   - Files modified list included

**If ANY secondary has NOT sent completion message:**
- ❌ STOP - S3 cannot proceed
- Send message to secondary: "Status check - are you complete with S2?"
- Wait for response (allow 15 minutes)
- If no response after 15 min → escalate to user (stale agent)

---

### Step 0.2: Verify STATUS Files

**For EACH feature (including yours):**

1. **Read STATUS file:**
   - File: `feature_{N}_{name}/STATUS`

2. **Verify required fields:**
   - `STAGE: S2.P3`
   - `STATUS: COMPLETE`
   - `READY_FOR_SYNC: true`
   - `BLOCKERS: none`

**If ANY feature shows different status:**
- ❌ STOP - S3 cannot proceed
- Check which agent owns that feature
- Send message: "Your STATUS file shows {actual_status}, expected COMPLETE. Please verify."
- Wait for clarification

---

### Step 0.3: Verify Checkpoints

**For EACH secondary agent:**

1. **Read checkpoint file:**
   - File: `agent_checkpoints/{secondary_agent_id}.json`

2. **Verify checkpoint fields:**
   - `status: "WAITING_FOR_SYNC"`
   - `stage: "S2.P3"`
   - `ready_for_next_stage: true`
   - `last_checkpoint` within last 30 minutes (not stale)

**Staleness check:**
- If `last_checkpoint` > 30 minutes ago → ⚠️ Warning (agent may have crashed)
- If `last_checkpoint` > 60 minutes ago → ❌ Failure (agent definitely stale)

**If stale agent detected:**
- Send message to secondary: "Checkpoint stale ({minutes} min old). Are you still active?"
- Wait 15 minutes for response
- If no response → escalate to user
- See: `parallel_work/stale_agent_protocol.md` for recovery

---

### Step 0.4: Verify Feature Specs Complete

**For EACH feature:**

1. **Read feature spec:**
   - File: `feature_{N}_{name}/spec.md`

2. **Verify required sections exist:**
   - Discovery Context
   - Requirements (with traceability)
   - Components Affected
   - Data Structures
   - Algorithms
   - Dependencies
   - Acceptance Criteria (with user approval checkbox marked [x])

3. **Verify checklist complete:**
   - File: `feature_{N}_{name}/checklist.md`
   - All questions marked `[x]` (resolved)
   - User approval documented

**If ANY feature has incomplete spec:**
- ❌ STOP - S3 cannot proceed
- Identify which agent owns that feature
- Send message: "Feature {N} spec incomplete. Missing: {sections}. Please complete S2."
- Wait for completion

---

### Step 0.5: Document Sync Verification

**After all verifications pass:**

Create sync verification record in `epic/research/S3_SYNC_VERIFICATION_{DATE}.md`:

```markdown
# S3 Sync Verification

**Date:** {YYYY-MM-DD HH:MM}
**Epic:** {epic_name}
**Parallel Mode:** Yes (Primary + {N} secondaries)

---

## Verification Results

### Completion Messages
- [x] Secondary-A (Feature 02): Received {timestamp}
- [x] Secondary-B (Feature 03): Received {timestamp}
- [x] Secondary-C (Feature 04): Received {timestamp}

### STATUS Files
- [x] Feature 01: COMPLETE, READY_FOR_SYNC: true
- [x] Feature 02: COMPLETE, READY_FOR_SYNC: true
- [x] Feature 03: COMPLETE, READY_FOR_SYNC: true
- [x] Feature 04: COMPLETE, READY_FOR_SYNC: true

### Checkpoints
- [x] Secondary-A: WAITING_FOR_SYNC, last update {timestamp} ({minutes} min ago)
- [x] Secondary-B: WAITING_FOR_SYNC, last update {timestamp} ({minutes} min ago)
- [x] Secondary-C: WAITING_FOR_SYNC, last update {timestamp} ({minutes} min ago)

### Feature Specs
- [x] Feature 01: All sections complete, user approved
- [x] Feature 02: All sections complete, user approved
- [x] Feature 03: All sections complete, user approved
- [x] Feature 04: All sections complete, user approved

---

## Sync Status

**Result:** ✅ ALL AGENTS READY FOR SYNC

**Issues Found:** None

**Next Action:** Proceed to S3 Step 1 (Prepare Comparison Matrix)

**Timestamp:** {YYYY-MM-DD HH:MM}
```

**If sync verification fails:**
- Document which verifications failed
- Update Agent Status: `BLOCKERS: Waiting for {agent} to complete {task}`
- Do NOT proceed to S3 comparison until all verifications pass

---

### Step 0.6: Notify Secondary Agents

**After sync verification passes:**

**For EACH secondary agent:**

1. **Send notification message:**
   - File: `agent_comms/primary_to_secondary_{x}.md`
   - Message:
     ```markdown
     ## Message {N} ({TIMESTAMP}) ⏳ UNREAD
     **Subject:** S3 Starting - Sync Point Reached
     **Action:** All features verified complete, S3 beginning now
     **Details:** 
     - All {N} features completed S2 successfully
     - Sync verification passed
     - Primary now running S3 (Cross-Feature Sanity Check)
     - You should WAIT - do NOT proceed to S3
     
     **Next:** After S3 completes, you'll receive notification to proceed to S4
     **Acknowledge:** No action needed, this is informational only
     ```

2. **Update coordination tracker:**
   - Document notification sent
   - Timestamp for audit trail

---

### Verification Complete

**After Step 0.6:**
- ✅ All secondary agents verified complete
- ✅ All feature specs ready for comparison
- ✅ Sync verification documented
- ✅ Secondary agents notified

**Proceed to:** Step 1 (Prepare Comparison Matrix)

**See:** `parallel_work/s2_parallel_protocol.md` → Phase 7 for S3 coordination details

---

