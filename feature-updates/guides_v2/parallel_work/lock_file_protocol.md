# Lock File Protocol

**Purpose:** Prevent race conditions when multiple agents update shared epic-level files during parallel S2 work

**Used For:** S2 parallelization (documentation-only files)

**Lock Files:** `.epic_locks/epic_readme.lock`, `.epic_locks/epic_smoke_test_plan.lock`

---

## Overview

When multiple agents work in parallel during S2, they need to update shared files like `EPIC_README.md`. Without coordination, simultaneous writes would cause:
- Lost updates (one agent's changes overwrite another's)
- Merge conflicts in git
- Inconsistent file state

The lock file system provides **atomic file-based locking** to serialize access to shared files.

---

## Lock File Format

**Location:** `.epic_locks/{file_name}.lock`

**Format (JSON):**
```json
{
  "holder": "Agent-Primary",
  "holder_id": "abc123",
  "acquired_at": "2026-01-15T14:30:00Z",
  "operation": "Updating S2.P2 progress",
  "expires_at": "2026-01-15T14:35:00Z",
  "auto_release": true
}
```

**Fields:**
- `holder`: Human-readable agent identifier (Agent-Primary, Secondary-A, Secondary-B)
- `holder_id`: Unique session ID for the agent
- `acquired_at`: ISO 8601 timestamp when lock was acquired
- `operation`: Description of what the agent is doing (for debugging)
- `expires_at`: When lock automatically expires (timeout)
- `auto_release`: Whether lock auto-releases on timeout (always true)

---

## Lock Acquisition Protocol

### Step 1: Check if Lock Exists

```bash
# Check if lock file exists
if [ -f .epic_locks/epic_readme.lock ]; then
  echo "Lock exists, checking if expired..."
fi
```

### Step 2: Read Lock File (if exists)

```bash
# Read lock file
LOCK_CONTENT=$(cat .epic_locks/epic_readme.lock)

# Parse expiry time
EXPIRES_AT=$(echo $LOCK_CONTENT | jq -r '.expires_at')

# Get current time
CURRENT_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Compare times
if [ "$CURRENT_TIME" > "$EXPIRES_AT" ]; then
  echo "Lock expired, can acquire"
  LOCK_EXPIRED=true
else
  echo "Lock still valid, must wait"
  LOCK_EXPIRED=false
fi
```

### Step 3: Wait or Acquire

**If lock exists and NOT expired:**
```bash
echo "Lock held by $(echo $LOCK_CONTENT | jq -r '.holder')"
echo "Operation: $(echo $LOCK_CONTENT | jq -r '.operation')"
echo "Waiting 5 seconds..."
sleep 5
# Retry from Step 1
```

**If lock expired:**
```bash
echo "Lock expired, removing stale lock"
rm .epic_locks/epic_readme.lock
# Proceed to Step 4
```

**If lock doesn't exist:**
```bash
# Proceed to Step 4
```

### Step 4: Create Lock File

```bash
# Calculate expiry (5 minutes from now)
EXPIRES_AT=$(date -u -d "+5 minutes" +"%Y-%m-%dT%H:%M:%SZ")

# Create lock file
cat > .epic_locks/epic_readme.lock <<EOF
{
  "holder": "Agent-Primary",
  "holder_id": "abc123",
  "acquired_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "operation": "Updating S2.P2 progress",
  "expires_at": "$EXPIRES_AT",
  "auto_release": true
}
EOF

echo "Lock acquired successfully"
```

### Step 5: Verify Acquisition

**Important:** Due to race conditions, verify you actually acquired the lock:

```bash
# Wait 100ms to ensure file system settled
sleep 0.1

# Re-read lock file
LOCK_HOLDER=$(cat .epic_locks/epic_readme.lock | jq -r '.holder_id')

if [ "$LOCK_HOLDER" == "abc123" ]; then
  echo "Lock verified, proceeding with operation"
else
  echo "Lock acquired by another agent, retrying"
  # Retry from Step 1
fi
```

---

## Performing Locked Operation

**Once lock acquired:**

```bash
# Perform the operation
# Example: Update EPIC_README.md
echo "Updating EPIC_README.md..."

# Edit file (use Edit tool or bash)
# ... make changes ...

# Save changes
echo "Changes saved"
```

**Operation Guidelines:**
- **Keep locked time minimal** (under 30 seconds ideal)
- **Don't wait for user input** while holding lock
- **Don't run long operations** (like full codebase searches)
- **Release lock immediately** after file updated

---

## Lock Release Protocol

### Step 1: Delete Lock File

```bash
# Remove lock file
rm .epic_locks/epic_readme.lock

echo "Lock released"
```

### Step 2: Verify Release

```bash
# Verify lock file gone
if [ ! -f .epic_locks/epic_readme.lock ]; then
  echo "Lock release verified"
else
  echo "ERROR: Lock file still exists!"
  # This shouldn't happen, investigate
fi
```

---

## Lock Timeout Behavior

**Timeout Duration:** 5 minutes (generous buffer for EPIC_README updates)

**Purpose:** Prevent infinite locks if agent crashes mid-operation

**Important Clarifications:**

1. **Timeout does NOT interrupt ongoing operations**
   - If agent is actively working, operation completes normally
   - Agent completes the file update and releases lock normally
   - Timeout is a safety mechanism, not an interruption

2. **Auto-release mechanism:**
   - Timeout only allows NEW lock acquisition if original holder vanished
   - Another agent can't "steal" a lock while holder is actively working
   - Lock expiry = permission for others to acquire, not forced release

3. **Best practice:**
   - Set timeout to 2-3x typical operation duration
   - EPIC_README.md update typically takes 30 seconds
   - 5 minute timeout provides 10x buffer (very conservative)

**Example Timeline:**
```text
14:30:00 - Agent-Primary acquires lock (expires 14:35:00)
14:30:15 - Agent-Primary starts editing EPIC_README.md
14:30:45 - Agent-Primary finishes editing (30 seconds total)
14:30:46 - Agent-Primary releases lock

Lock never timed out because operation completed in 30s (well under 5 min)
```

**Timeout Scenario:**
```text
14:30:00 - Agent-Primary acquires lock (expires 14:35:00)
14:30:15 - Agent-Primary crashes mid-operation
14:35:01 - Secondary-A tries to acquire lock
14:35:01 - Secondary-A sees lock expired, deletes stale lock
14:35:02 - Secondary-A acquires new lock
14:35:05 - Secondary-A performs operation
14:35:10 - Secondary-A releases lock

Timeout allowed recovery from crashed agent
```

---

## Lock Files in S2 Parallelization

### Lock 1: EPIC_README.md

**File:** `.epic_locks/epic_readme.lock`

**Used For:**
- Updating agent progress sections
- Updating Agent Assignment table
- Updating Sync Status section

**Frequency:**
- After completing each S2 phase (P1, P2, P3)
- Every 15 minutes (heartbeat update)
- When blockers occur
- At sync points

**Typical Duration:** 20-30 seconds

### Lock 2: epic_smoke_test_plan.md

**File:** `.epic_locks/epic_smoke_test_plan.lock`

**Used For:**
- Updating test plan in S4 (Primary only in S2 plan)
- Not heavily used in S2 parallelization (S4 is sequential)

**Frequency:**
- Only during S4 (Primary only)

**Typical Duration:** 60-90 seconds

---

## Lock Retry Logic

**Recommended Retry Strategy:**

```bash
acquire_lock() {
  local LOCK_FILE=$1
  local AGENT_ID=$2
  local OPERATION=$3
  local MAX_RETRIES=60  # 5 minutes total wait time
  local RETRY_DELAY=5   # 5 seconds between retries

  for i in $(seq 1 $MAX_RETRIES); do
    # Try to acquire lock
    if try_acquire_lock "$LOCK_FILE" "$AGENT_ID" "$OPERATION"; then
      echo "Lock acquired after $i attempts"
      return 0
    fi

    # Lock not acquired, wait and retry
    echo "Retry $i/$MAX_RETRIES: Lock held by another agent"
    sleep $RETRY_DELAY
  done

  # Max retries exceeded
  echo "ERROR: Could not acquire lock after $MAX_RETRIES attempts"
  echo "This indicates a stuck lock or heavy contention"
  return 1
}
```

**Escalation:**
- If unable to acquire lock after 5 minutes (60 retries), escalate to Primary
- Primary investigates: Is holder still active? Is lock truly needed?
- Primary can manually delete lock if holder crashed

---

## Sectioned EPIC_README.md (Reduces Lock Contention)

**Problem:** If all agents update EPIC_README.md frequently, lock contention increases

**Solution:** Each agent owns a section, reduces conflicts

**Structure:**
```markdown
<!-- BEGIN PRIMARY PROGRESS -->
... Primary's content ...
<!-- END PRIMARY PROGRESS -->

<!-- BEGIN SECONDARY-A PROGRESS -->
... Secondary-A's content ...
<!-- END SECONDARY-A PROGRESS -->
```

**Benefits:**
- Agents edit different sections = less chance of actual conflict
- Lock still required (file-level), but contention reduced
- Git handles sectioned edits cleanly

**See:** `epic_readme_sectioning.md` for complete sectioning protocol

---

## Common Lock Scenarios

### Scenario 1: Simple Update (No Contention)

```text
Agent-Primary wants to update EPIC_README.md
  → Acquires lock (no other agents holding it)
  → Updates progress section (25 seconds)
  → Releases lock
  → Success
```

### Scenario 2: Contention (Another Agent Holding Lock)

```text
Secondary-A wants to update EPIC_README.md
  → Tries to acquire lock
  → Sees lock held by Agent-Primary (expires in 2 min)
  → Waits 5 seconds
  → Retries: lock still held
  → Waits 5 seconds
  → Retries: lock released
  → Acquires lock
  → Updates progress section (20 seconds)
  → Releases lock
  → Success (took 30 seconds due to wait)
```

### Scenario 3: Expired Lock (Crashed Agent)

```text
Secondary-B wants to update EPIC_README.md
  → Tries to acquire lock
  → Sees lock held by Secondary-A (expired 30 seconds ago)
  → Determines Secondary-A likely crashed
  → Deletes stale lock
  → Acquires new lock
  → Updates progress section (22 seconds)
  → Releases lock
  → Success
  → Reports to Primary: "Secondary-A may have crashed (stale lock detected)"
```

### Scenario 4: Heavy Contention (All 3 Agents)

```text
All agents complete S2.P1 simultaneously:
  - Primary tries to acquire lock → succeeds → updates (25s) → releases
  - Secondary-A tries to acquire → waits → acquires → updates (20s) → releases
  - Secondary-B tries to acquire → waits → acquires → updates (23s) → releases

Total time: 68 seconds (serialized updates)
If no lock: Would have merge conflict or lost updates
```

---

## Lock Debugging

### Check Lock Status

```bash
# See who holds lock
if [ -f .epic_locks/epic_readme.lock ]; then
  echo "Lock held by:"
  cat .epic_locks/epic_readme.lock | jq '.holder, .operation, .expires_at'
else
  echo "Lock available"
fi
```

### Check Lock Age

```bash
# How long has lock been held?
ACQUIRED=$(cat .epic_locks/epic_readme.lock | jq -r '.acquired_at')
CURRENT=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
echo "Lock acquired at: $ACQUIRED"
echo "Current time: $CURRENT"

# Calculate duration (manual comparison)
```

### Force Release Lock (DANGER)

**Only use if:**
- Holder agent has crashed and cannot release
- Lock is blocking all progress
- Primary has verified holder is gone

```bash
# DANGER: Only Primary should do this
echo "Force releasing lock held by $(cat .epic_locks/epic_readme.lock | jq -r '.holder')"
rm .epic_locks/epic_readme.lock
echo "Lock force-released"
```

---

## Integration with Guides

### In S2.P1, S2.P2, S2.P3 Guides

**Add lock protocol steps:**

```markdown
### Step X: Update EPIC_README.md Progress

1. **Acquire lock:**
   ```
   acquire_lock "epic_readme" "$AGENT_ID" "Updating S2.P1 progress"
   ```markdown

2. **Update your section:**
   - Edit EPIC_README.md
   - Update only your section (between BEGIN/END markers)
   - Update status, next action, blockers

3. **Release lock:**
   ```
   release_lock "epic_readme"
   ```markdown

4. **Verify update:**
   - Re-read EPIC_README.md
   - Confirm your section updated correctly
```

---

## Performance Characteristics

**Lock Overhead:**
- Acquire time (no contention): <1 second
- Acquire time (contention): 5-30 seconds (depends on wait)
- Operation time: 20-60 seconds (typical file update)
- Release time: <1 second
- **Total overhead: ~5-10 seconds per update**

**Coordination Overhead Target:** <10% of parallel time
- For 3-feature epic (2.5 hours parallel work)
- Expected lock operations: ~15 (5 per agent)
- Time per lock: ~30 seconds average
- **Total lock time: 7.5 minutes = 5% overhead** ✅

**Scalability:**
- 2 agents: Minimal contention (~5% overhead)
- 3 agents: Low contention (~10% overhead)
- 4+ agents: Moderate contention (~15-20% overhead)
- Recommendation: Max 4 agents in parallel for S2

---

## Error Handling

### Error 1: Lock File Corrupted

```bash
# If lock file is not valid JSON
if ! jq '.' .epic_locks/epic_readme.lock >/dev/null 2>&1; then
  echo "ERROR: Lock file corrupted"
  echo "Deleting corrupt lock"
  rm .epic_locks/epic_readme.lock
  # Retry acquisition
fi
```

### Error 2: Unable to Create Lock File

```bash
# If lock creation fails
if ! cat > .epic_locks/epic_readme.lock <<EOF ...; then
  echo "ERROR: Cannot create lock file"
  echo "Check directory exists: .epic_locks/"
  echo "Check permissions"
  exit 1
fi
```

### Error 3: Lock Held Too Long

```bash
# If lock held >5 minutes and still not expired
# This indicates timeout is too generous or operation too slow
echo "WARNING: Lock held for >5 minutes"
echo "Investigate holder: $(cat .epic_locks/epic_readme.lock | jq -r '.holder')"
echo "Operation: $(cat .epic_locks/epic_readme.lock | jq -r '.operation')"
# Escalate to Primary
```

---

## Summary

**Lock file protocol provides:**
- ✅ Race condition prevention
- ✅ Automatic stale lock cleanup (timeout)
- ✅ Minimal overhead (~5-10% of parallel work time)
- ✅ Simple file-based implementation (no external dependencies)
- ✅ Clear ownership and debugging

**Best practices:**
- Acquire lock immediately before operation
- Keep locked time minimal (<30 seconds)
- Release lock immediately after operation
- Use sectioned files to reduce contention
- Set timeout to 2-3x typical operation duration
- Never hold lock while waiting for user input

**Next:** See `communication_protocol.md` for agent-to-agent messaging
