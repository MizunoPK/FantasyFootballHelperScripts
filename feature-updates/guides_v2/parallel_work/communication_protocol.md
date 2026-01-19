# Communication Protocol

**Purpose:** Enable agent-to-agent messaging without EPIC_README.md conflicts during parallel S2 work

**Used For:** S2 parallelization (escalations, updates, coordination)

**Channel Files:** `agent_comms/primary_to_secondary_a.md`, `agent_comms/secondary_a_to_primary.md`, etc.

---

## Overview

When multiple agents work in parallel during S2, they need to communicate for:
- **Escalations** (Secondary asks Primary for help)
- **Updates** (Primary notifies Secondary of changes)
- **Coordination** (Sync status, blockers, completion signals)

Using EPIC_README.md for messaging would require constant lock acquisition and create contention. Instead, we use **dedicated communication channel files** for each agent pair.

---

## Channel Structure

**Directory:** `agent_comms/`

**Files (for 3-agent epic):**
```
agent_comms/
├── primary_to_secondary_a.md    # Inbox for Secondary-A (Primary writes, Secondary-A reads)
├── secondary_a_to_primary.md    # Outbox from Secondary-A (Secondary-A writes, Primary reads)
├── primary_to_secondary_b.md    # Inbox for Secondary-B (Primary writes, Secondary-B reads)
└── secondary_b_to_primary.md    # Outbox from Secondary-B (Secondary-B writes, Primary reads)
```

**Key Principle:**
- **One writer, one reader per file** → Zero conflicts
- Primary writes to `primary_to_secondary_a.md` (Secondary-A's inbox)
- Secondary-A writes to `secondary_a_to_primary.md` (Primary's outbox from A)
- No lock files needed (single writer per file)

---

## Message Format

**File Format:** Markdown (human-readable, easy to edit)

**Structure:**
```markdown
# Messages: Primary → Secondary-A

## Message 5 (2026-01-15 15:30) ✅ READ
**Subject:** S3 Complete - Proceed to Implementation
**Action:** I've completed S3 (Cross-Feature Sanity Check)
**Details:** No conflicts found with your feature
**Next:** Implementation remains sequential in this plan - I'll start Feature 01
**Acknowledge:** Reply when you understand

## Message 4 (2026-01-15 14:00) ✅ READ
**Subject:** User answered your question
**Action:** Check feature_02/checklist.md - Question 5 answered
**Next:** Complete S2.P3, then signal completion
**Acknowledge:** Reply when S2.P3 complete

## Message 3 (2026-01-15 12:30) ⏳ UNREAD
**Subject:** Proceeding with Feature 01
**Action:** I'm starting S2.P2 for Feature 01
**Details:** No blockers currently
**Next:** Continue your S2 work
**Acknowledge:** No action needed

## Message 2 (2026-01-15 11:45) ✅ READ
**Subject:** Response to escalation
**Action:** Re: your question about team rankings
**Details:** User clarified: Use existing team_rankings.csv file (Option A)
**Next:** Update your spec.md with this approach
**Acknowledge:** Reply when updated

## Message 1 (2026-01-15 10:30) ✅ READ
**Subject:** Handoff Package Received
**Action:** I see you've started S2 for Feature 02
**Details:** Looking forward to coordinating with you!
**Next:** Proceed with S2.P1, reach out if you need anything
**Acknowledge:** Reply to confirm you're online
```

**Message Fields:**
- **Message Number:** Sequential (Message 1, 2, 3, ...)
- **Timestamp:** When message was sent (YYYY-MM-DD HH:MM)
- **Read Status:** ✅ READ or ⏳ UNREAD
- **Subject:** Brief description (1 line)
- **Action:** What the recipient should do
- **Details:** Additional context
- **Next:** Next steps
- **Acknowledge:** How to acknowledge (reply, action, or "no action needed")

---

## Message Sending Protocol

### Step 1: Determine Channel

**Primary sending to Secondary-A:**
- File: `agent_comms/primary_to_secondary_a.md` (Secondary-A's inbox)

**Secondary-A sending to Primary:**
- File: `agent_comms/secondary_a_to_primary.md` (Primary's inbox from A)

### Step 2: Read Current File

```bash
# Read existing messages
CHANNEL_FILE="agent_comms/primary_to_secondary_a.md"
CURRENT_CONTENT=$(cat "$CHANNEL_FILE")
```

### Step 3: Determine Next Message Number

```bash
# Count existing messages
LAST_MSG_NUM=$(grep -c "^## Message" "$CHANNEL_FILE")
NEXT_MSG_NUM=$((LAST_MSG_NUM + 1))
```

### Step 4: Append New Message

```bash
# Prepend new message (newest at top)
TIMESTAMP=$(date +"%Y-%m-%d %H:%M")
NEW_MESSAGE="
## Message $NEXT_MSG_NUM ($TIMESTAMP) ⏳ UNREAD
**Subject:** Your subject here
**Action:** What recipient should do
**Details:** Additional context
**Next:** Next steps
**Acknowledge:** How to acknowledge

"

# Prepend to file (insert after header)
# Read header
HEADER="# Messages: Primary → Secondary-A\n\n"

# Write new content
echo -e "$HEADER$NEW_MESSAGE$CURRENT_CONTENT" > "$CHANNEL_FILE"
```

### Step 5: Notify Recipient (Optional)

**In STATUS file or EPIC_README.md:**
- Update: "NEW MESSAGE in inbox"
- Recipient checks inbox on next coordination cycle (every 15 min)

---

## Message Reading Protocol

### Step 1: Check Inbox

**Secondary-A checking inbox:**
```bash
INBOX="agent_comms/primary_to_secondary_a.md"

# Check for unread messages
UNREAD_COUNT=$(grep -c "⏳ UNREAD" "$INBOX")

if [ $UNREAD_COUNT -gt 0 ]; then
  echo "You have $UNREAD_COUNT unread messages"
else
  echo "No unread messages"
fi
```

### Step 2: Read Messages

```bash
# Read inbox file
cat "$INBOX"

# Identify unread messages (look for ⏳ UNREAD)
# Read each message content
```

### Step 3: Mark as Read

**After reading a message, mark it as read:**

```bash
# Replace ⏳ UNREAD with ✅ READ for Message 5
sed -i 's/## Message 5 (.*) ⏳ UNREAD/## Message 5 \1 ✅ READ/' "$INBOX"
```

**Using Edit tool:**
```
old_string: "## Message 5 (2026-01-15 15:30) ⏳ UNREAD"
new_string: "## Message 5 (2026-01-15 15:30) ✅ READ"
```

### Step 4: Take Action

**Based on message content:**
- If escalation response → Apply guidance
- If update notification → Acknowledge receipt
- If sync signal → Update own status

### Step 5: Reply (if needed)

**If message says "Acknowledge: Reply when done":**
- Send reply message to outbox
- Example: Secondary-A replies to Primary

```bash
# Secondary-A sending reply to Primary
OUTBOX="agent_comms/secondary_a_to_primary.md"

# Append reply
# (Use same protocol as "Message Sending" above)
```

---

## Message Inbox Check Frequency

**When to check inbox:**

1. **Every 15 minutes** (coordination heartbeat)
2. **Before starting each S2 phase** (P1, P2, P3)
3. **After checkpoint update** (every 15 min aligns)
4. **When blocked** (before escalating, check if Primary sent guidance)
5. **At sync points** (before signaling completion)

**Recommended Workflow:**
```markdown
### Coordination Heartbeat (Every 15 Minutes)

1. Update checkpoint file
2. Check inbox for new messages
3. Read and mark messages as read
4. Take action on urgent messages
5. Reply to messages requiring acknowledgment
6. Resume work
```

---

## Common Message Types

### Type 1: Escalation Request (Secondary → Primary)

**Scenario:** Secondary blocked, needs help

```markdown
## Message 3 (2026-01-15 11:30) ⏳ UNREAD
**Subject:** ESCALATION - Spec Ambiguity in Feature 02
**Action:** Please help resolve spec ambiguity
**Details:** Spec says "integrate with team rankings" but unclear if this means:
  A) Use existing team_rankings.csv file
  B) Fetch fresh data from NFL API
  C) Both (use CSV as cache, update from API)

Attempted:
  - Read team_rankings.csv structure
  - Checked nfl-scores-fetcher/ code
  - Reviewed Feature 01 spec for clues

Stuck For: 25 minutes
**Next:** Awaiting your guidance or user clarification
**Acknowledge:** Reply with decision or "escalating to user"
```

### Type 2: Escalation Response (Primary → Secondary)

**Scenario:** Primary responds with guidance

```markdown
## Message 6 (2026-01-15 11:45) ⏳ UNREAD
**Subject:** Re: ESCALATION - Spec Ambiguity
**Action:** Use existing team_rankings.csv file (Option A)
**Details:** I asked the user. They confirmed:
  - Use team_rankings.csv as the data source
  - No need to fetch from NFL API for this feature
  - Feature 01 already handles CSV loading, you can reuse that

**Next:** Update your spec.md with this approach, proceed with S2.P2
**Acknowledge:** Reply when spec.md updated and you've unblocked
```

### Type 3: User Question Result (Primary → Secondary)

**Scenario:** User answered Secondary's question

```markdown
## Message 4 (2026-01-15 14:00) ⏳ UNREAD
**Subject:** User answered your question
**Action:** Check feature_02/checklist.md - Question 5 answered
**Details:** User said: "Yes, apply penalty to all offensive players on team"
**Next:** Update spec.md with this requirement, complete S2.P3
**Acknowledge:** Reply when updated
```

### Type 4: Sync Status Update (Any → Any)

**Scenario:** Agent signals completion

```markdown
## Message 7 (2026-01-15 14:25) ⏳ UNREAD
**Subject:** S2.P3 Complete for Feature 02
**Action:** I've completed S2 for Feature 02
**Details:**
- spec.md complete (all requirements documented)
- checklist.md all items resolved
- README.md updated with S2 completion

Blockers: None
**Next:** Ready for S3 (Cross-Feature Sanity Check)
**Acknowledge:** No action needed, proceed when all features ready
```

### Type 5: Coordination Update (Primary → Secondary)

**Scenario:** Primary notifies about epic-level work

```markdown
## Message 8 (2026-01-15 15:00) ⏳ UNREAD
**Subject:** S3 Complete - No Conflicts Found
**Action:** I've completed S3 (Cross-Feature Sanity Check)
**Details:** Reviewed all 3 feature specs, found:
  - No requirement conflicts
  - No overlaps
  - No gaps
  - All features aligned with epic

**Next:** Implementation remains sequential in this plan - I'll start Feature 01 S5
**Acknowledge:** No action needed, you can idle or close session
```

### Type 6: Blocker Notification (Secondary → Primary)

**Scenario:** Secondary is blocked but not escalating yet

```markdown
## Message 2 (2026-01-15 12:15) ⏳ UNREAD
**Subject:** Temporarily Blocked - Investigating
**Action:** FYI: I'm blocked on integration point
**Details:** Trying to understand how Feature 02 integrates with Feature 01
         Reading Feature 01 spec.md to clarify
         Will escalate if can't resolve in 15 minutes
**Next:** Investigating, will update shortly
**Acknowledge:** No action needed unless I escalate
```

### Type 7: Blocker Resolved (Secondary → Primary)

**Scenario:** Secondary unblocked themselves

```markdown
## Message 4 (2026-01-15 12:30) ⏳ UNREAD
**Subject:** Blocker Resolved - Resuming Work
**Action:** I resolved my blocker
**Details:** Found integration point in Feature 01 spec.md
         Clear now how to integrate team penalty with roster
**Next:** Resuming S2.P2 implementation
**Acknowledge:** No action needed
```

---

## Message Archiving

**When to archive:**
- After sync point complete (S2 → S3 transition)
- All messages have been read and actioned
- No pending acknowledgments

**Archive Process:**
```bash
# Move messages to archive
mkdir -p agent_comms/archive
TIMESTAMP=$(date +"%Y%m%d_%H%M")

# Archive Primary → Secondary-A messages
mv agent_comms/primary_to_secondary_a.md \
   agent_comms/archive/primary_to_secondary_a_$TIMESTAMP.md

# Create fresh inbox
cat > agent_comms/primary_to_secondary_a.md <<EOF
# Messages: Primary → Secondary-A

(No messages yet)
EOF
```

**Benefits:**
- Clean inbox for next wave or epic
- Historical record preserved
- Reduced file size for active channels

---

## Inbox Management Best Practices

**For Primary (Coordinator):**
- Check all secondary inboxes every 15 minutes
- Prioritize escalation messages (respond within 15 min)
- Batch non-urgent messages (respond within 1 hour)
- Archive messages after sync points

**For Secondary Agents:**
- Check inbox every 15 minutes
- Read all unread messages immediately
- Mark messages as read after processing
- Reply to messages requiring acknowledgment
- Don't wait for messages (continue work unless blocked)

---

## Integration with Guides

### In S2.P1, S2.P2, S2.P3 Guides

**Add inbox check steps:**

```markdown
### Step X: Coordination Heartbeat

**Every 15 minutes during S2 work:**

1. **Update checkpoint:**
   - Update `agent_checkpoints/{agent_id}.json`
   - Include current phase, status, next action

2. **Check inbox:**
   - Read `agent_comms/primary_to_{agent_id}.md` (if Secondary)
   - Read `agent_comms/secondary_{x}_to_primary.md` (if Primary, check all)
   - Look for ⏳ UNREAD messages

3. **Process messages:**
   - Read each unread message
   - Mark as ✅ READ
   - Take action if required
   - Reply if acknowledgment needed

4. **Update STATUS:**
   - Update `feature_XX/STATUS` with current state
   - Include any blockers from messages

5. **Resume work:**
   - Continue S2 phase work
   - Set timer for next 15-minute check
```

### Escalation Workflow Integration

```markdown
### When Blocked (>30 minutes)

1. **Check inbox first:**
   - Maybe Primary already sent guidance
   - Read all unread messages

2. **If no guidance in inbox, send escalation:**
   - Compose escalation message
   - Append to `agent_comms/{agent_id}_to_primary.md`
   - Update STATUS file: `BLOCKERS: <description>`
   - Update EPIC_README.md section: "BLOCKED - Escalation needed"

3. **Wait for response:**
   - Check inbox every 5 minutes (urgent)
   - Primary responds within 15-60 minutes
   - Process response when received

4. **Acknowledge and resume:**
   - Mark Primary's response as ✅ READ
   - Send acknowledgment reply
   - Update STATUS: `BLOCKERS: none`
   - Resume work
```

---

## Error Handling

### Error 1: Inbox File Missing

```bash
# If inbox doesn't exist, create it
INBOX="agent_comms/primary_to_secondary_a.md"

if [ ! -f "$INBOX" ]; then
  echo "WARNING: Inbox file missing, creating..."
  mkdir -p agent_comms
  cat > "$INBOX" <<EOF
# Messages: Primary → Secondary-A

(No messages yet)
EOF
fi
```

### Error 2: Inbox File Corrupted

```bash
# If inbox is not valid markdown or empty
if [ ! -s "$INBOX" ]; then
  echo "ERROR: Inbox file empty or corrupted"
  echo "Creating backup and reinitializing..."

  # Backup corrupt file
  cp "$INBOX" "$INBOX.backup.$(date +%s)"

  # Reinitialize
  cat > "$INBOX" <<EOF
# Messages: Primary → Secondary-A

(Inbox was reinitialized due to corruption)
EOF
fi
```

### Error 3: Message Number Conflict

```bash
# If two agents try to send message with same number
# This shouldn't happen (one writer per file), but if it does:
# Use timestamp to disambiguate

# Example: Message 5 (2026-01-15 14:00) and Message 5 (2026-01-15 14:01)
# Both exist → renumber second one to Message 6
```

---

## Performance Characteristics

**Message Overhead:**
- Send message time: <1 second (file append)
- Read message time: <1 second (file read)
- Mark as read time: <1 second (sed replace or Edit)
- **Total per message: ~3 seconds**

**Coordination Overhead:**
- Check inbox every 15 min: 3 seconds
- Process 1-2 messages: 6 seconds
- Reply to 1 message: 3 seconds
- **Total per heartbeat: ~12 seconds**

**Total Coordination Overhead (3-feature epic):**
- 2.5 hours parallel work = 10 heartbeats
- 10 heartbeats × 12 seconds = 120 seconds = 2 minutes
- **Messaging overhead: ~1% of parallel time** ✅ (well under 10% target)

---

## Summary

**Communication protocol provides:**
- ✅ Zero-conflict messaging (one writer per file)
- ✅ Human-readable format (markdown)
- ✅ Clear message history (all messages preserved)
- ✅ Read receipts (⏳ UNREAD → ✅ READ)
- ✅ Minimal overhead (~1% of parallel time)

**Best practices:**
- Check inbox every 15 minutes
- Respond to escalations within 15 minutes (Primary)
- Mark messages as read immediately after processing
- Reply to messages requiring acknowledgment
- Archive messages after sync points

**Next:** See `checkpoint_protocol.md` for agent recovery system
