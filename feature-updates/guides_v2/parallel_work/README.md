# Parallel Work System - S2 Feature Planning

**Purpose:** Coordinate multiple agents working on S2 feature planning in parallel

**When to use:** Epics with 3+ features (40-60% time reduction for S2 phase)

---

## Quick Navigation

### Master Protocol
- **[s2_parallel_protocol.md](s2_parallel_protocol.md)** - Complete overview with 9-phase workflow

### Agent Guides
- **[s2_primary_agent_guide.md](s2_primary_agent_guide.md)** - Primary agent workflow (coordinator + Feature 01)
- **[s2_secondary_agent_guide.md](s2_secondary_agent_guide.md)** - Secondary agent workflow (feature owner)

### Infrastructure Protocols
- **[lock_file_protocol.md](lock_file_protocol.md)** - File locking for shared resources
- **[communication_protocol.md](communication_protocol.md)** - Agent-to-agent messaging
- **[checkpoint_protocol.md](checkpoint_protocol.md)** - Crash recovery and staleness detection

### Recovery Protocols
- **[stale_agent_protocol.md](stale_agent_protocol.md)** - Handling crashed/hung agents
- **[sync_timeout_protocol.md](sync_timeout_protocol.md)** - Sync point timeout handling

### Templates
- **[templates/handoff_package_s2_template.md](templates/handoff_package_s2_template.md)** - Secondary agent handoff
- **[templates/feature_status_template.txt](templates/feature_status_template.txt)** - STATUS file format
- **[templates/epic_readme_template.md](templates/epic_readme_template.md)** - EPIC_README with parallel sections

---

## System Overview

**Agent Roles:**
- **Primary Agent:** Coordinator + Feature 01 owner (85% feature work, 15% coordination)
- **Secondary Agent:** Feature owner only (90% feature work, 10% coordination)

**Coordination Mechanisms:**
- Checkpoints (every 15 minutes) - Crash recovery + staleness detection
- Communication (file-based messaging) - Async agent-to-agent messaging
- STATUS Files (per feature) - Quick status check
- Locks (shared files) - Prevent race conditions

**Sync Points:**
- Sync Point 1 (S2 → S3): All agents complete S2, Primary runs S3 solo
- Sync Point 2 (S4 → S5): Primary completes S4, all agents continue to S5

---

## Quick Start

**For Primary Agent:**
1. Read [s2_primary_agent_guide.md](s2_primary_agent_guide.md)
2. Generate handoff packages for secondaries
3. Execute S2 for Feature 01 while coordinating

**For Secondary Agent:**
1. Read [s2_secondary_agent_guide.md](s2_secondary_agent_guide.md)
2. Receive handoff package from Primary
3. Execute S2 for assigned feature

---

## Integration with Workflow

**S1 Step 5.8-5.9:** Offer parallel work (if 3+ features)
**S1 Final Step:** Generate handoffs (if parallel enabled)
**S2 Router:** Detects Primary vs Secondary role
**S3 Start:** Sync verification
**S4 End:** Notify secondaries to proceed

**Note:** Parallel work is OPTIONAL - workflow works identically in sequential mode.

---

**See:** Master protocol for complete details and decision guides.
