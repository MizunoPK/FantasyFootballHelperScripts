# Implementation Plan: S5-S8 Parallelization

**Version:** 1.0
**Date:** 2026-01-15
**Scope:** Enable parallel feature implementation (S5-S8)
**Risk Level:** MEDIUM (code changes, git merges, test coordination)

---

## Executive Summary

**Objective:** Enable multiple agents to work on S5-S8 (Feature Implementation Loop) simultaneously, reducing epic implementation time by 40-60% for epics with 3+ independent features.

**Scope:** S5-S8 parallelization - features are implemented in parallel
- ✅ S5: Implementation Planning (parallel)
- ✅ S6: Implementation Execution (parallel on separate branches)
- ✅ S7: Post-Implementation (parallel testing, Primary merge review)
- ✅ S8: Post-Feature Alignment (parallel for most tasks)

**Time Savings Example (3-feature epic with independent features):**
```
Sequential S5-S8:
- Feature 1: 5 hours
- Feature 2: 5 hours
- Feature 3: 5 hours
Total: 15 hours

Parallel S5-S8:
- All 3 features: 5 hours (max of 5, 5, 5) + 1 hour merges
Total: 6 hours

SAVINGS: 9 hours (60% reduction in S5-S8 time)
```

**Epic-Level Time Savings:**
```
Sequential Epic (3 features):
S1: 2h | S2: 6h | S3: 1h | S4: 1h | S5-S8: 15h | S9: 2h | S10: 1h
Total: 28 hours

Parallel S5-S8 Epic (3 independent features):
S1: 2h | S2: 6h | S3: 1h | S4: 1h | S5-S8: 6h | S9: 2h | S10: 1h
Total: 19 hours

SAVINGS: 9 hours (32% epic-level reduction)
```

**Combined with S2 Parallelization:**
```
S1: 2h | S2: 2h | S3: 1h | S4: 1h | S5-S8: 6h | S9: 2h | S10: 1h
Total: 15 hours

SAVINGS: 13 hours (46% epic-level reduction)
```

**Why S5-S8 Parallelization:**
1. **Highest Value** - 5+ hours per feature (vs 2 hrs for S2)
2. **Scales Well** - More features = more savings
3. **Independent Work** - Each agent owns their feature branch
4. **Quality Maintained** - Pre-merge quality gate ensures consistency

**Risk Level:** MEDIUM
- Git merge conflicts (mitigated by feature branches)
- Test suite coordination (mitigated by hybrid testing)
- Quality divergence (mitigated by quality gate)
- Coordination overhead (mitigated by automation)

**Prerequisites:**
- ✅ S2 parallelization implemented and tested (or planned)
- ✅ Lock file system working
- ✅ Communication channels working
- ✅ Checkpoint system working

**Implementation Time:** 8-12 hours (guide creation + testing)

**Pilot Approach:** Test with 2-feature epic with independent features

---

## Table of Contents

1. [Scope Definition](#scope-definition)
2. [Architecture](#architecture)
3. [Git Workflow](#git-workflow)
4. [Implementation Phases](#implementation-phases)
5. [Guide Changes Required](#guide-changes-required)
6. [Quality Gate Protocol](#quality-gate-protocol)
7. [Merge Protocol](#merge-protocol)
8. [Test Coordination](#test-coordination)
9. [User Experience Flow](#user-experience-flow)
10. [Risk Analysis](#risk-analysis)
11. [Success Metrics](#success-metrics)
12. [Pilot Plan](#pilot-plan)

---

## Scope Definition

### In Scope

**Parallelizable Work:**
- ✅ S5: Implementation Planning (all features simultaneously)
  - S5.P1: Round 1 (iterations 1-7)
  - S5.P2: Round 2 (iterations 8-16)
  - S5.P3: Round 3 (iterations 17-25)
- ✅ S6: Implementation Execution (on separate git branches)
- ✅ S7: Post-Implementation (testing on feature branches)
  - S7.P1: Smoke Testing
  - S7.P2: QC Rounds
  - S7.P3: Final Review (feature-level commit)
- ✅ S8.P1: Cross-Feature Spec Alignment (updates to unstarted features only)
- ✅ S8.P2: Epic Testing Update (coordinated updates to shared plan)

**New Components:**
- ✅ Git branch per feature (feature/02-name, feature/03-name)
- ✅ Quality gate protocol (automated + manual checks)
- ✅ Merge protocol (Primary reviews and merges)
- ✅ Test coordination (feature-level vs full suite)
- ✅ Wave-based scheduling (dependencies handled sequentially)

**Agent Roles:**
- ✅ Primary Agent (coordinates, owns Feature 01 on main, merges all)
- ✅ Secondary Agent(s) (owns Feature 02/03 on branches)

### Out of Scope

**Sequential Work (Unchanged):**
- ❌ S1: Epic Planning (remains Primary only)
- ❌ S2: Feature Deep Dives (use S2 parallelization plan if desired)
- ❌ S3: Cross-Feature Sanity Check (remains Primary only)
- ❌ S4: Epic Testing Strategy (remains Primary only)
- ❌ S9: Epic Final QC (remains Primary only)
- ❌ S10: Epic Cleanup (remains Primary only)

**Dependent Features:**
- ❌ Features with dependencies implement sequentially (in waves)
- ✅ Independent features parallelize within wave

### Dependency Management

**Wave System:**
```
Example: 3 features

Feature Dependencies:
- feature_01: None
- feature_02: Depends on feature_01
- feature_03: None

Wave 1 (Parallel):
  - feature_01 (Primary on main)
  - feature_03 (Secondary-B on feature/03-branch)

Wave 2 (After feature_01 merged):
  - feature_02 (Secondary-A on feature/02-branch)
```

**Wave Rules:**
1. Independent features execute in same wave (parallel)
2. Dependent features wait for dependency to merge
3. Primary merges features in dependency order
4. After merge → Primary signals dependent features can start

### Sync Points

**Sync Point 1: After S4 → Before S5 (Wave Assignment)**
- Primary completes S4 (Epic Testing Strategy)
- Primary analyzes dependencies
- Primary assigns features to waves
- Primary generates handoff packages for Wave 1 secondary agents
- User starts secondary agent sessions for Wave 1
- All Wave 1 agents begin S5 simultaneously

**Sync Point 2: After S7.P3 (Feature Complete - Ready for Merge)**
- Agent completes S7.P3 for their feature
- Agent commits feature to their branch (or main if Primary)
- Agent signals: "Feature complete - ready for merge"
- Primary reviews and merges (for secondary agents)
- After merge: Primary runs full test suite
- If tests pass: Feature considered merged
- If tests fail: Revert merge, send back to agent

**Sync Point 3: After Merge → Before S8 (Update Specs)**
- Feature merged to main
- Primary signals: "Feature X merged"
- All agents update remaining feature specs (S8.P1)
- All agents update epic test plan (S8.P2)

**Sync Point 4: After Wave Complete → Next Wave**
- All Wave N features merged to main
- Primary checks if any Wave N+1 features waiting
- If yes: Primary generates handoff packages for Wave N+1
- User starts new secondary agent sessions (or reuses existing)
- Repeat S5-S8 for Wave N+1

**Wave Transition Timing (Important):**
- **Wave N+1 starts AFTER all Wave N features merged to main**
- **Does NOT wait for Wave N agents to complete S8**
- S8 work can continue in parallel with Wave N+1 implementation

**Example Timeline:**
```
Wave 1 (Features 01 and 03):
10:00: Wave 1 starts
15:00: Feature 01 merges to main
15:30: Feature 03 merges to main
15:35: ALL Wave 1 features merged → Wave 2 can start
15:40: Primary generates Wave 2 handoff
15:45: Wave 2 starts (Feature 02 begins S5)

Meanwhile:
15:35-16:00: Feature 01 agent completes S8.P1
16:00-16:15: Feature 01 agent completes S8.P2
16:15: Feature 01 fully complete

15:35-16:10: Feature 03 agent completes S8.P1
16:10-16:25: Feature 03 agent completes S8.P2
16:25: Feature 03 fully complete
```

**Why This Timing:**
- Merging = code integration complete (main branch has feature)
- S8 = documentation updates (doesn't block dependent features)
- Dependent features need merged code, not completed S8
- Allows parallelism: Wave N finishing S8 while Wave N+1 implements

**Sync Point 5: After All Waves → S9**
- All features merged to main
- All S8.P2 complete
- Full test suite passes on main
- Primary proceeds to S9 (Epic Final QC)

---

### Feature Completion States

**Purpose:** Clarify the different completion states during S5-S8 workflow

**State Progression:**

```
┌─────────────────────────────────────────────────────────────────┐
│ State 1: S7.P3 Complete (Implementation Done)                   │
│   - Agent finishes S7.P3 (Final Review) for their feature      │
│   - All feature-level tests passing                            │
│   - Implementation verified complete                           │
│   - Lessons learned documented                                 │
│   ↓                                                             │
│   Agent commits to branch (or main if Primary)                 │
│   Agent signals "Ready for merge" (if Secondary)               │
│   ↓                                                             │
├─────────────────────────────────────────────────────────────────┤
│ State 2: Merge Review Started (Primary Gate)                    │
│   - Primary receives completion signal                         │
│   - Primary runs automated quality checks                      │
│   - Primary completes 35-item manual review                    │
│   ↓                                                             │
│   IF APPROVED → State 3                                        │
│   IF CHANGES NEEDED → Back to agent (fix → restart State 1)   │
│   ↓                                                             │
├─────────────────────────────────────────────────────────────────┤
│ State 3: Merged to Main (Code Integration Complete)             │
│   - Primary merges feature branch to main                      │
│   - Merge commit created on main                               │
│   - Primary runs post-merge full test suite                    │
│   ↓                                                             │
│   IF TESTS PASS → State 4                                      │
│   IF TESTS FAIL → Revert merge, back to agent (fix)           │
│   ↓                                                             │
│   Primary signals "Merged successfully" to agent               │
│   ↓                                                             │
├─────────────────────────────────────────────────────────────────┤
│ State 4: S8.P1 Complete (Cross-Feature Updates Done)            │
│   - Agent updates specs for unstarted features                 │
│   - Agent incorporates learnings from completed feature        │
│   ↓                                                             │
├─────────────────────────────────────────────────────────────────┤
│ State 5: S8.P2 Complete (Epic Test Plan Updated)                │
│   - Agent updates epic_smoke_test_plan.md (locked)            │
│   - Agent adds test scenarios for completed feature           │
│   ↓                                                             │
│   Agent signals "S8 complete"                                  │
│   ↓                                                             │
├─────────────────────────────────────────────────────────────────┤
│ State 6: Feature Fully Complete                                 │
│   - Feature code merged to main                                │
│   - Documentation updates complete (S8)                        │
│   - Agent waits for next assignment or S9                      │
│   ↓                                                             │
│   IF more waves: Agent may be assigned to Wave N+1 feature    │
│   IF last wave: Agent waits for Primary to start S9           │
└─────────────────────────────────────────────────────────────────┘
```

**Key State Terminology:**

| Term | Meaning | When Used |
|------|---------|-----------|
| "S7.P3 complete" | Implementation done, tests pass | Agent finishes S7.P3 |
| "Ready for merge" | Signaling to Primary for review | Secondary sends message |
| "Merge review started" | Primary beginning quality gate | Primary's acknowledgment |
| "Merged to main" | Feature integrated into main branch | After successful merge |
| "S8 complete" | All post-feature updates done | After S8.P2 complete |
| "Feature fully complete" | Everything done, waiting | State 6 reached |

**State Transition Timing:**
- State 1 → State 2: Immediate (agent signals, Primary responds)
- State 2 → State 3: 30-60 minutes (quality gate duration)
- State 3 → State 4: Immediate (Primary signals merge success)
- State 4 → State 5: 15-30 minutes (S8.P1 work)
- State 5 → State 6: 15-30 minutes (S8.P2 work)

**Total Feature Time (S7.P3 → Fully Complete):**
- Typical: 1-2 hours (includes merge review + S8 work)
- With issues: 2-4 hours (includes fix cycles)

---

## Architecture

### Directory Structure

```
feature-updates/KAI-N-epic_name/
├── EPIC_README.md                 # Sectioned
├── epic_smoke_test_plan.md        # Updated in S8.P2 (locked)
├── epic_lessons_learned.md
│
├── .epic_locks/                   # Lock files
│   ├── epic_readme.lock
│   ├── epic_smoke_test_plan.lock
│   └── test_suite.lock            # NEW - Full test suite lock
│
├── agent_comms/                   # Communication channels
│   ├── primary_to_secondary_a.md
│   ├── secondary_a_to_primary.md
│   ├── primary_to_secondary_b.md
│   └── secondary_b_to_primary.md
│
├── agent_checkpoints/             # Checkpoint files
│   ├── primary.json
│   ├── secondary_a.json
│   └── secondary_b.json
│
├── merge_reviews/                 # NEW - Merge review records
│   ├── feature_02_review.md
│   └── feature_03_review.md
│
├── feature_01_player_json/        # Primary's feature (on main)
│   ├── STATUS
│   ├── README.md
│   ├── spec.md
│   ├── checklist.md
│   ├── implementation_plan.md
│   ├── implementation_checklist.md
│   └── lessons_learned.md
│
├── feature_02_team_penalty/       # Secondary-A's feature (on branch)
│   ├── STATUS
│   ├── README.md
│   ├── spec.md
│   ├── checklist.md
│   ├── implementation_plan.md
│   ├── implementation_checklist.md
│   └── lessons_learned.md
│
└── feature_03_scoring_update/     # Secondary-B's feature (on branch)
    ├── STATUS
    └── [same structure]
```

### Git Branch Strategy

```
main (Primary's baseline)
  │
  ├── feature/02-team-penalty (Secondary-A)
  │   └── [Feature 02 code changes only]
  │
  └── feature/03-scoring-update (Secondary-B)
      └── [Feature 03 code changes only]

Workflow:
1. Primary works on main for Feature 01
2. Secondary-A creates branch: feature/02-team-penalty
3. Secondary-B creates branch: feature/03-scoring-update
4. Each agent implements on their branch
5. Primary merges secondary branches when complete
6. All features converge on main
```

**Branch Naming Convention:**
- Format: `feature/{NN}-{short-name}`
- Examples:
  - `feature/02-team-penalty`
  - `feature/03-scoring-update`
- Always 2-digit feature number
- Lowercase, hyphen-separated

### Agent Coordination Model

```
┌─────────────────────────────────────────────────────────┐
│                    PRIMARY AGENT                        │
│  - Owns Feature 01 (on main)                            │
│  - Coordinates all parallel work                        │
│  - Merges all secondary branches                        │
│  - Runs full test suite before/after merges             │
│  - Quality gate reviewer                                │
│  - Runs S1, S3, S4, S9, S10                            │
└─────────────────────────────────────────────────────────┘
          │                                   │
          │ handoff package                   │ handoff package
          │ (includes branch name)            │
          ▼                                   ▼
┌──────────────────────────┐    ┌──────────────────────────┐
│   SECONDARY AGENT A      │    │   SECONDARY AGENT B      │
│  - Owns Feature 02       │    │  - Owns Feature 03       │
│  - Branch: feature/02-*  │    │  - Branch: feature/03-*  │
│  - S5-S8 on branch       │    │  - S5-S8 on branch       │
│  - Feature-level tests   │    │  - Feature-level tests   │
│  - Signals when ready    │    │  - Signals when ready    │
│  - Waits for merge       │    │  - Waits for merge       │
└──────────────────────────┘    └──────────────────────────┘

All agents work simultaneously on S5-S8:
- Primary: S5-S8 for Feature 01 (on main)
- Secondary-A: S5-S8 for Feature 02 (on feature/02-branch)
- Secondary-B: S5-S8 for Feature 03 (on feature/03-branch)

After agent completes S7.P3:
- Agent signals "ready for merge"
- Primary reviews feature (quality gate)
- Primary merges to main
- Primary runs full test suite
- Primary signals "merged" or "changes requested"
```

---

### Escalation Protocol

**Purpose:** Define when and how Secondary agents escalate to Primary during S5-S8

**When Secondary Escalates to Primary:**
- User questions requiring domain knowledge or business logic clarification
- Specification ambiguities discovered during implementation
- Integration concerns with other features (especially cross-feature dependencies)
- Blockers preventing progress >30 minutes
- Technical decisions that may affect epic-level architecture
- Merge conflicts that require Primary's architectural judgment

**Escalation Process:**
1. Secondary documents issue in feature's implementation_checklist.md or communication channel
2. Secondary updates STATUS file: `BLOCKERS: <description>`
3. Secondary sends message via communication channel with:
   - Clear description of blocker
   - What was already tried/investigated
   - Specific help needed or decision required
   - Impact on timeline if unresolved
4. Secondary signals "BLOCKED - Escalation needed" in EPIC_README.md section
5. Primary responds within 15 minutes (or 1 hour if in deep work/merge review)
6. Primary either:
   - Provides guidance directly via communication channel
   - Handles user interaction if user input needed
   - Reviews code/design if technical decision needed
   - Coordinates with other agents if cross-feature issue
7. Secondary acknowledges resolution and resumes work

**What Secondary Can Decide Alone:**
- Implementation approach choices (within spec and implementation_plan.md boundaries)
- Code structure, class design, and function organization
- Test design, test data, and coverage approaches
- Minor algorithm optimizations
- Local refactoring within feature scope
- Documentation style and formatting
- Commit message wording (following conventions)
- Feature-level test fixes

**What Requires Primary Escalation:**
- Spec changes or requirement additions/modifications
- User questions about business requirements or priorities
- Cross-feature coordination or integration design decisions
- Changes to epic-level files (epic_smoke_test_plan.md, EPIC_README.md)
- Dependency conflicts or wave timing concerns
- Major technical decisions affecting other features or architecture
- Implementation plan deviations that change core approach
- Quality gate failures that are disputed
- Merge conflicts during Primary's merge process

**Escalation SLA:**
- Primary checks communication channels every 15 minutes during active work
- Primary responds to escalations within 15 minutes during normal work
- Primary responds within 1 hour maximum if in deep work or conducting merge review
- If Primary unavailable >1 hour, secondary updates checkpoint with blocker state and waits

**Example Escalation Message (Implementation Phase):**
```markdown
# Messages: Secondary-A → Primary

## Message 5 (2026-01-15 14:45)
**Subject:** ESCALATION - Integration Approach for Team Penalty
**Blocker:** Unable to proceed with S6 implementation
**Stage:** S6 (Implementation) - Integrating penalty calculation
**Issue:** Implementation plan says "integrate with existing scoring pipeline" but:
  A) scoring_pipeline.py doesn't have extension points
  B) Could modify scoring_pipeline.py directly (risky for Feature 01)
  C) Could create parallel pipeline and merge in add_to_roster.py
**Attempted:**
  - Read scoring_pipeline.py (Feature 01's code)
  - Checked if scoring_pipeline.py has hooks (none found)
  - Reviewed implementation_plan.md (doesn't specify approach)
**Stuck For:** 40 minutes
**Need:** Architectural decision on integration approach
**Impact:** Blocks all S6 progress, may affect Feature 01 if Option B chosen
**Blocked Since:** 14:05
**Urgency:** HIGH (affects integration with Feature 01)
```

---

### Primary Agent Workload Management (S5-S8)

**Purpose:** Guide Primary's balance between coordination duties and Feature 01 implementation during parallel S5-S8 work

**Primary's Dual Role:**
1. **Coordinator:** Merge reviews (quality gate), messaging, sync management, escalation handling, wave transitions
2. **Feature Owner:** Implements Feature 01 on main (full S5-S8 workflow)

**Time Allocation Strategy:**

**Priority Order:**
1. **Escalations (Highest Priority):** Respond within 15 minutes, resolve immediately
2. **Merge Reviews (High Priority):** Complete within 30-60 minutes of signal
3. **Sync Management:** Monitor STATUS files, communication channels every 15 minutes
4. **Wave Transitions:** Generate handoff packages when wave completes
5. **Feature 01 Work:** S5-S8 implementation during idle coordination time

**Feature Assignment Best Practice:**
- Primary should own the **simplest/smallest feature** as Feature 01
- This minimizes Primary's implementation workload
- Frees more time for coordination responsibilities (especially merge reviews)
- Reduces bottleneck risk during Wave 1

**Workload Balance Approach:**

1. **Work in time blocks:**
   - 15-minute coordination checks (STATUS files, messages, escalations)
   - 45-90 minute deep work blocks on Feature 01
   - Interrupt deep work for urgent escalations or merge signals
   - Schedule merge reviews between implementation phases (not mid-S6)

2. **During S5-S8 parallel work:**
   - Start Feature 01 implementation immediately (parallel with secondaries)
   - Check coordination every 15 minutes
   - Respond to escalations immediately
   - Complete Feature 01 at natural pace (don't rush to finish first)

3. **When merge requests arrive:**
   - **If in S5 or early S6:** Pause Feature 01 work, conduct merge review (~1 hour)
   - **If in critical S6 work:** Acknowledge signal, complete current implementation unit (~30 min), then merge
   - **If in S7 testing:** Pause testing, conduct merge review (testing can resume easily)
   - Always prioritize merges over own feature progress

4. **If coordination demands spike:**
   - Pause Feature 01 work entirely
   - Focus on unblocking secondary agents
   - Complete all pending merge reviews
   - Resume Feature 01 after coordination stabilizes

5. **Wave transitions:**
   - Pause Feature 01 work
   - Generate Wave N+1 handoff packages
   - Ensure all Wave N agents complete S8
   - Resume Feature 01 after Wave N+1 launched

**Example Timeline (3-feature epic, 2 waves):**
```
Wave 1 (Features 01 and 03 in parallel):
10:00-10:15: Handoff package for Wave 1
10:15-11:30: Primary works on Feature 01 S5.P1 (75 min)
11:30-11:35: Check coordination (5 min)
11:35-13:00: Primary works on Feature 01 S5.P2 (85 min)
13:00-13:10: Secondary-B escalation → Primary responds (10 min)
13:10-15:00: Primary works on Feature 01 S5.P3 (110 min)
15:00-16:00: Primary works on Feature 01 S6 (60 min)
16:00-16:05: Secondary-B signals "Feature complete" (5 min)
16:05-17:05: Primary pauses Feature 01, conducts merge review for F03 (60 min)
17:05-18:30: Primary resumes Feature 01 S6 (85 min)
18:30-20:00: Primary completes Feature 01 S7 (90 min)
20:00-20:30: Primary completes S8.P1 and S8.P2 (30 min)

Wave 2 (Feature 02, Primary idle except coordination):
20:30-20:45: Generate Wave 2 handoff for Secondary-A (15 min)
20:45-22:30: Secondary-A works on Feature 02 (105 min, Primary monitors)
22:30-22:35: Secondary-A signals "Feature complete" (5 min)
22:35-23:35: Primary conducts merge review for F02 (60 min)
23:35-00:00: Primary monitors Secondary-A complete S8 (25 min)

Total Wave Time: 14 hours (with coordination overhead)
Primary Feature 01 Time: ~7 hours (actual implementation)
Primary Coordination Time: ~2 hours (merges, escalations, waves)
```

**Key Principles:**
- **Merge reviews always take priority** over own feature work
- **Never let secondary agents block** for >30 minutes on escalations
- **Choose simplest feature** to minimize own implementation burden
- **Schedule merge reviews strategically** (between S5/S6/S7 boundaries, not mid-phase)
- **Use waiting time productively** (during sync, prepare Wave N+1, review quality metrics)
- **Communicate response times clearly** to secondary agents (set expectations)

**Coordination Overhead Target:**
- <5% of total parallel time (more stringent than S2's 10% due to higher complexity)
- For 3-feature epic with 2 waves: ~1-2 hours coordination per 14 hours total = 7-14%
- Includes: Lock operations, message responses, escalations, merge reviews, wave transitions

**Bottleneck Prevention:**
- If Primary becomes bottleneck (>3 merge requests queued), defer own Feature 01 work entirely
- Focus 100% on coordination until queue clears
- Consider extending timeout periods if coordination load is consistently high

---

## Git Workflow

### Branch Creation (Secondary Agents)

**When:** After receiving handoff package, before S5

**Commands:**
```bash
# Secondary-A
git checkout main
git pull origin main
git checkout -b feature/02-team-penalty
git push -u origin feature/02-team-penalty

# Secondary-B
git checkout main
git pull origin main
git checkout -b feature/03-scoring-update
git push -u origin feature/03-scoring-update
```

**Verification:**
```bash
git branch -a
# Should show:
#   main
# * feature/02-team-penalty
#   remotes/origin/main
#   remotes/origin/feature/02-team-penalty
```

### Development Workflow (All Agents)

**Commit Frequency:**
- After completing S5 round (3 commits: Round 1, 2, 3)
- After completing S6 phase (4-6 commits during implementation)
- After completing S7 phase (3 commits: Smoke, QC, Final)
- After completing S8 phase (2 commits: S8.P1, S8.P2)

**Commit Messages:**
```bash
# Format: {type}/KAI-{N}: {message}

# Examples (Secondary-A on feature/02-team-penalty):
git commit -m "feat/KAI-6: Complete S5 Round 1 for feature_02"
git commit -m "feat/KAI-6: Implement team penalty calculator"
git commit -m "feat/KAI-6: Add team penalty tests"
git commit -m "feat/KAI-6: Complete S7 QC for feature_02"

# Primary on main:
git commit -m "feat/KAI-6: Complete S5 Round 1 for feature_01"
git commit -m "feat/KAI-6: Implement player JSON integration"
```

**Push Frequency:**
- After each commit (immediate push)
- Ensures checkpoint and code in sync

### Merge Workflow (Primary Only)

**Trigger:** Secondary agent signals "Feature complete - ready for merge"

**Step 1: Pre-Merge Quality Gate**
```bash
# Primary switches to secondary's branch
git fetch origin
git checkout feature/02-team-penalty

# Run quality gate validation
./scripts/pre_merge_validation.sh feature_02_team_penalty

# Validation includes:
# - Test coverage ≥90%
# - Full test suite passes
# - Code quality ≥8.0
# - All required files present
# - Zero TODO/FIXME comments

# If passes: Proceed to Step 2
# If fails: Send feedback to Secondary-A, wait for fixes
```

**Step 2: Merge to Main**
```bash
# Primary returns to main
git checkout main
git pull origin main

# Merge feature branch (no fast-forward, preserve history)
git merge --no-ff feature/02-team-penalty -m "feat/KAI-6: Merge feature_02_team_penalty

Implements team penalty scoring for NFL teams in Add to Roster mode.

Reviewed-by: Agent-Primary
Tested: All tests pass (100%)
Coverage: 92%
Quality: 8.8/10
"

# If conflicts:
#   - Resolve conflicts
#   - Verify resolution with agent
#   - Commit merge resolution

# Push to main
git push origin main
```

**Step 3: Post-Merge Validation**
```bash
# Run full test suite on main
python tests/run_all_tests.py

# If tests pass:
#   - Feature merge complete
#   - Signal Secondary-A: "Merged successfully"
#   - Delete feature branch (optional, keep for history)

# If tests fail:
#   - REVERT merge immediately
#   git revert -m 1 HEAD
#   git push origin main
#   - Send failure details to Secondary-A
#   - Secondary-A investigates integration issue
#   - Repeat merge workflow after fix
```

**Step 4: Signal Completion**
```markdown
# Messages: Primary → Secondary-A

## Message X (2026-01-15 16:30)
**Subject:** Feature 02 Merged Successfully
**Status:** feature_02_team_penalty merged to main
**Merge Commit:** abc123d
**Test Results:** All tests pass (1,847 tests, 100% pass rate)
**Next:** You can continue with S8 (Post-Feature Alignment)
```

### Branch Cleanup (End of Epic)

**When:** After S10 complete, epic archived

**Commands:**
```bash
# Delete local branches
git branch -d feature/02-team-penalty
git branch -d feature/03-scoring-update

# Delete remote branches (optional, can keep for history)
git push origin --delete feature/02-team-penalty
git push origin --delete feature/03-scoring-update
```

---

## Implementation Phases

### Phase 1: Git Infrastructure (2-3 hours)

**Deliverables:**

1. **Branch Management Guide**
   - File: `parallel_work/git_branch_protocol.md`
   - Branch naming conventions
   - Branch creation commands
   - Branch lifecycle

2. **Merge Protocol Guide**
   - File: `parallel_work/merge_protocol.md`
   - Pre-merge quality gate
   - Merge commands
   - Post-merge validation
   - Conflict resolution

3. **Git Workflow Scripts**
   - Script: `scripts/create_feature_branch.sh`
   - Script: `scripts/pre_merge_validation.sh`
   - Script: `scripts/merge_feature.sh`
   - Script: `scripts/post_merge_validation.sh`

4. **Branch Templates**
   - Template: `.github/PULL_REQUEST_TEMPLATE.md` (for manual PRs)
   - Note: We'll use direct merges, not PRs

**Testing:**
- Create mock branches
- Test merge workflow
- Test conflict resolution
- Test revert workflow

**Exit Criteria:**
- All scripts working
- Merge protocol documented
- Branch workflow tested

---

### Phase 2: Quality Gate System (3-4 hours)

**Deliverables:**

1. **Quality Gate Protocol**
   - File: `parallel_work/quality_gate_protocol.md`
   - Automated checks definition
   - Manual review checklist (35 items)
   - Quality metrics dashboard

2. **Pre-Merge Validation Script**
   - File: `scripts/pre_merge_validation.sh`
   - Test coverage check (≥90%)
   - Full test suite run
   - Code quality check (≥8.0)
   - File completeness check
   - TODO/FIXME check

3. **Quality Metrics Tracking**
   - File: `merge_reviews/quality_metrics.md`
   - Dashboard template
   - Metric collection script

4. **Merge Review Template**
   - Template: `templates/merge_review_template.md`
   - 35-item checklist
   - Decision workflow (Approve/Changes/Reject)

**Testing:**
- Run validation script on complete feature
- Test all quality checks
- Verify thresholds enforced
- Test failure scenarios

**Exit Criteria:**
- Validation script catches quality issues
- Metrics tracked correctly
- Review template comprehensive

---

### Phase 3: Test Coordination (2-3 hours)

**Deliverables:**

1. **Test Suite Lock Protocol**
   - Guide: `parallel_work/test_suite_lock_protocol.md`
   - Lock acquisition for full suite
   - Feature-level testing (no lock)
   - Primary merge testing

2. **Hybrid Testing Strategy**
   - Guide: `parallel_work/hybrid_testing_strategy.md`
   - Secondary: Feature-level tests only
   - Primary: Full suite at merge points
   - Test isolation guidelines

3. **Test Suite Lock File**
   - Location: `.epic_locks/test_suite.lock`
   - Format: Same as other locks
   - Timeout: 10 minutes (full suite run time)

**Testing:**
- Test concurrent feature-level tests
- Test lock acquisition for full suite
- Test timeout handling
- Verify no test interference

**Exit Criteria:**
- Feature tests run in parallel (no conflicts)
- Full suite locked during Primary runs
- Lock timeout works
- No test interference

---

### Phase 4: S5-S8 Workflow Integration (4-5 hours)

**Deliverables:**

1. **S4 Guide Updates**
   - File: `stages/s4/s4_epic_testing_strategy.md`
   - Add: Wave assignment logic
   - Add: Dependency analysis output
   - Add: Parallel work offering (for S5-S8)

2. **S5 Guide Updates**
   - Files: `stages/s5/*.md` (all S5 guides)
   - Add: Branch awareness (Secondary on branch, Primary on main)
   - Add: Checkpoint updates with branch info
   - Add: Git commit after each round

3. **S6 Guide Updates**
   - File: `stages/s6/s6_execution.md`
   - Add: Work on feature branch (not main)
   - Add: Push commits regularly
   - Add: Feature-level testing only
   - Add: Track changes via git (not code_changes.md)

4. **S7 Guide Updates**
   - Files: `stages/s7/*.md` (3 S7 guides)
   - Add: Testing on feature branch
   - Add: Feature-level commit at S7.P3 end
   - Add: Signal completion to Primary
   - Add: Wait for merge approval

5. **S8 Guide Updates**
   - File: `stages/s8/s8_p1_cross_feature_alignment.md`
   - Add: Update specs for unstarted features only (not own)
   - Add: Coordination for multi-agent updates

   - File: `stages/s8/s8_p2_epic_testing_update.md`
   - Add: Locked updates to epic_smoke_test_plan.md
   - Add: Coordinated updates (all agents contribute)

6. **Primary Agent Guide (S5-S8)**
   - File: `parallel_work/s5_s8_primary_agent_guide.md`
   - Wave coordination
   - Merge review responsibilities
   - Full test suite running

7. **Secondary Agent Guide (S5-S8)**
   - File: `parallel_work/s5_s8_secondary_agent_guide.md`
   - Branch creation
   - Feature-level testing
   - Signaling completion
   - Waiting for merge

**Testing:**
- Walk through S5-S8 with agent role awareness
- Test branch creation
- Test commit workflow
- Test completion signal

**Exit Criteria:**
- All guides updated
- Agent role logic correct
- Git workflow integrated
- Sync points clearly defined

---

### Phase 5: Wave Management (2 hours)

**Deliverables:**

1. **Wave Scheduling Protocol**
   - Guide: `parallel_work/wave_scheduling_protocol.md`
   - Dependency analysis in S4
   - Wave assignment algorithm
   - Wave transition coordination

2. **Dependency Graph**
   - Template: `templates/dependency_graph_template.md`
   - Visual dependency representation
   - Wave assignment table

3. **Wave Transition Protocol**
   - When Wave N complete → Start Wave N+1
   - Handoff package generation for Wave N+1
   - User starts new/reused sessions

**Testing:**
- Create epic with dependencies (F02 depends on F01)
- Verify wave assignment correct
- Test wave transition
- Test dependent feature starts after merge

**Exit Criteria:**
- Dependencies detected correctly
- Waves assigned logically
- Transitions smooth

---

### Phase 6: User Experience (2 hours)

**Deliverables:**

1. **Parallel Work Offering (S5-S8)**
   - File: `prompts/parallel_work_prompts.md`
   - Template for offering S5-S8 parallelization
   - Shows time savings (epic-level)
   - Wave explanation

2. **Handoff Package (S5-S8)**
   - Template: `templates/handoff_package_s5_s8.md`
   - Includes branch name
   - Includes wave assignment
   - Includes dependency info

3. **Merge Notification**
   - Template: Messages to secondary agents
   - Shows merge success/failure
   - Next steps clear

4. **Wave Transition Notification**
   - Template: Notification for Wave N+1
   - Who starts next wave
   - New handoff packages

**Testing:**
- Run through full user flow
- Copy-paste handoff package
- Test merge notifications
- Test wave transitions

**Exit Criteria:**
- User experience smooth
- Handoff package works
- Notifications clear

---

## Guide Changes Required

### New Guides (10 files)

| File | Purpose | Size | Priority |
|------|---------|------|----------|
| `parallel_work/s5_s8_parallel_protocol.md` | Complete S5-S8 parallel protocol | ~3000 lines | P0 |
| `parallel_work/s5_s8_primary_agent_guide.md` | Primary responsibilities for S5-S8 | ~1200 lines | P0 |
| `parallel_work/s5_s8_secondary_agent_guide.md` | Secondary workflow for S5-S8 | ~1000 lines | P0 |
| `parallel_work/git_branch_protocol.md` | Branch management | ~600 lines | P0 |
| `parallel_work/merge_protocol.md` | Merge workflow | ~800 lines | P0 |
| `parallel_work/quality_gate_protocol.md` | Quality gate system | ~1000 lines | P0 |
| `parallel_work/test_suite_lock_protocol.md` | Test coordination | ~400 lines | P0 |
| `parallel_work/hybrid_testing_strategy.md` | Feature vs full suite testing | ~500 lines | P0 |
| `parallel_work/wave_scheduling_protocol.md` | Dependency waves | ~600 lines | P1 |
| `parallel_work/conflict_resolution_guide.md` | Handling merge conflicts | ~400 lines | P1 |

**Total New Content:** ~9,500 lines

---

### Updated Guides (9 files)

| File | Changes | Priority |
|------|---------|----------|
| `stages/s4/s4_epic_testing_strategy.md` | Add: Wave assignment, S5-S8 parallel offering | P0 |
| `stages/s5/s5_p1_planning_round1.md` | Add: Branch awareness, git commits | P0 |
| `stages/s5/s5_p2_planning_round2.md` | Add: Branch awareness, git commits | P0 |
| `stages/s5/s5_p3_planning_round3.md` | Add: Branch awareness, git commits | P0 |
| `stages/s6/s6_execution.md` | Add: Work on branch, feature tests only | P0 |
| `stages/s7/s7_p1_smoke_testing.md` | Add: Testing on branch | P0 |
| `stages/s7/s7_p2_qc_rounds.md` | Add: QC on branch | P0 |
| `stages/s7/s7_p3_final_review.md` | Add: Commit to branch, signal completion | P0 |
| `stages/s8/s8_p1_cross_feature_alignment.md` | Add: Multi-agent coordination | P0 |
| `stages/s8/s8_p2_epic_testing_update.md` | Add: Locked epic test plan updates | P0 |

**Estimated Changes:** ~3,000 lines (updates to existing)

---

### Scripts (4 files)

| File | Purpose | Priority |
|------|---------|----------|
| `scripts/create_feature_branch.sh` | Create and push feature branch | P0 |
| `scripts/pre_merge_validation.sh` | Quality gate automation | P0 |
| `scripts/merge_feature.sh` | Automated merge workflow | P1 |
| `scripts/post_merge_validation.sh` | Post-merge test suite | P0 |

**Estimated:** ~800 lines of bash

---

### Templates (4 files)

| File | Changes | Priority |
|------|---------|----------|
| `templates/handoff_package_s5_s8.md` | S5-S8 handoff with branch info | P0 |
| `templates/merge_review_template.md` | 35-item quality checklist | P0 |
| `templates/dependency_graph_template.md` | Wave visualization | P1 |
| `templates/quality_metrics_dashboard.md` | Metrics tracking | P1 |

**Estimated:** ~1,000 lines

---

### Supporting Files (3 files)

| File | Changes | Priority |
|------|---------|----------|
| `EPIC_WORKFLOW_USAGE.md` | Add: S5-S8 parallel work section (~2000 lines) | P0 |
| `CLAUDE.md` | Add: Git workflow, merge protocol summary (~500 lines) | P0 |
| `prompts/parallel_work_prompts.md` | Add: S5-S8 prompts | P0 |

**Estimated:** ~2,500 lines

---

**TOTAL GUIDE EFFORT:**
- New guides: ~9,500 lines
- Updated guides: ~3,000 lines
- Scripts: ~800 lines
- Templates: ~1,000 lines
- Supporting: ~2,500 lines
- **TOTAL: ~16,800 lines**

**Estimated Time:** 10-12 hours (at ~1,400-1,700 lines/hour)

---

## Quality Gate Protocol

### Automated Checks

**Script:** `scripts/pre_merge_validation.sh`

**Checks:**

1. **Test Coverage (≥90%)**
   ```bash
   pytest tests/test_${FEATURE}.py --cov --cov-report=term-missing
   COVERAGE=$(pytest --cov | grep TOTAL | awk '{print $4}')
   if [ ${COVERAGE%\%} -lt 90 ]; then
     echo "❌ Coverage too low: $COVERAGE"
     exit 1
   fi
   ```

2. **Full Test Suite (100% pass)**
   ```bash
   python tests/run_all_tests.py
   if [ $? -ne 0 ]; then
     echo "❌ Test suite failed"
     exit 1
   fi
   ```

3. **Code Quality (≥8.0/10)**
   ```bash
   pylint ${FEATURE}/*.py --fail-under=8.0
   if [ $? -ne 0 ]; then
     echo "❌ Code quality too low"
     exit 1
   fi
   ```

4. **File Completeness**
   ```bash
   FILES=("spec.md" "implementation_plan.md" "implementation_checklist.md" "lessons_learned.md")
   for FILE in "${FILES[@]}"; do
     if [ ! -f "${FEATURE}/${FILE}" ]; then
       echo "❌ Missing: ${FILE}"
       exit 1
     fi
   done
   ```

5. **No TODO/FIXME**
   ```bash
   TODOS=$(grep -r "TODO\|FIXME" ${FEATURE}/*.py | wc -l)
   if [ $TODOS -gt 0 ]; then
     echo "❌ Found $TODOS TODO/FIXME comments"
     exit 1
   fi
   ```

**Exit Codes:**
- 0 = All checks passed (proceed to manual review)
- 1 = Checks failed (send feedback to agent)

---

### Manual Review Checklist

**File:** `merge_reviews/feature_{XX}_review.md`

**Categories (35 items total):**

1. **Specification Quality (5 items)**
   - [ ] spec.md complete
   - [ ] Requirement traceability present
   - [ ] Acceptance criteria clear
   - [ ] Edge cases documented
   - [ ] Spec aligned with epic

2. **Implementation Quality (7 items)**
   - [ ] implementation_plan.md followed
   - [ ] implementation_checklist.md 100% complete
   - [ ] All functions have docstrings
   - [ ] Complex logic has comments
   - [ ] Error handling comprehensive
   - [ ] No code duplication
   - [ ] Coding standards followed

3. **Testing Quality (6 items)**
   - [ ] Unit tests cover all functions
   - [ ] Edge cases tested
   - [ ] Error cases tested
   - [ ] Integration tests present (if applicable)
   - [ ] Test names descriptive
   - [ ] Tests independent

4. **Documentation Quality (4 items)**
   - [ ] README.md clear
   - [ ] lessons_learned.md substantive
   - [ ] Code comments explain "why"
   - [ ] No outdated comments

5. **Integration Quality (4 items)**
   - [ ] No conflicts with main
   - [ ] Compatible with other features
   - [ ] Shared utilities used correctly
   - [ ] Configuration changes documented

6. **Performance (3 items)**
   - [ ] No obvious performance issues
   - [ ] Database queries optimized
   - [ ] Large data handled efficiently

7. **Security (3 items)**
   - [ ] No SQL injection vulnerabilities
   - [ ] Input validation present
   - [ ] Error messages safe

8. **Completeness (3 items)**
   - [ ] All spec requirements implemented
   - [ ] All checklist items resolved
   - [ ] Feature works end-to-end

**Decision:**
- [ ] ✅ APPROVED - Merge to main
- [ ] ⏸️ CHANGES REQUESTED - See feedback below
- [ ] ❌ REJECTED - Major issues, rework needed

---

### Quality Metrics Dashboard

**File:** `merge_reviews/quality_metrics.md`

```markdown
## Quality Metrics Dashboard

| Feature | Agent | Coverage | Quality | Review | Status |
|---------|-------|----------|---------|--------|--------|
| feature_01 | Primary | 94% | 9.1 | Self-approved | ✅ Merged |
| feature_02 | Sec-A | 92% | 8.8 | Approved | ✅ Merged |
| feature_03 | Sec-B | 91% | 8.5 | Changes req | ⏸️ Pending |

**Quality Standards:**
- Test Coverage: ≥90% (target: 95%)
- Code Quality: ≥8.0/10 (target: 9.0)
- Review Status: Must be ✅ to merge

**Epic Average:**
- Coverage: 92.3%
- Quality: 8.8/10
- Pass rate: 66% (2/3 approved on first review)
```

---

## Merge Protocol

### Step-by-Step Merge Workflow

**Trigger:** Secondary agent signals "Feature complete - ready for merge"

#### Step 1: Acknowledge Signal

**Primary sends message:**
```markdown
## Message (2026-01-15 16:00)
**Subject:** Merge Review Started for Feature 02
**Status:** I've received your completion signal
**Next:** Running automated quality checks
**ETA:** 10-15 minutes
**Action:** No action needed from you, stand by
```

#### Step 2: Run Automated Checks

**Primary executes:**
```bash
git fetch origin
git checkout feature/02-team-penalty
./scripts/pre_merge_validation.sh feature_02_team_penalty
```

**If checks pass → Step 3**
**If checks fail → Send feedback:**
```markdown
## Message (2026-01-15 16:10)
**Subject:** Automated Checks Failed
**Status:** Feature 02 not ready for merge
**Issues Found:**
1. Test coverage: 85% (need ≥90%)
2. TODO comment at team_penalty.py:45

**Action Required:**
- Increase test coverage (add tests for penalty edge cases)
- Remove or resolve TODO comment

**Next Steps:**
1. Fix issues
2. Run tests locally: pytest tests/test_feature_02.py --cov
3. Signal completion again when ready
```

**Agent fixes issues, signals again → Repeat Step 2**

#### Step 3: Manual Review

**Primary completes 35-item checklist:**
```markdown
merge_reviews/feature_02_review.md

## Pre-Merge Review - Feature 02

**Automated Checks:**
✅ Test coverage: 92% (≥90%)
✅ Full test suite: 100% pass
✅ Code quality: 8.8/10 (≥8.0)
✅ All files present
✅ Zero TODO/FIXME

**Manual Review:**
[Primary completes 35-item checklist]

**Decision:** ✅ APPROVED
**Approved by:** Agent-Primary
**Approved at:** 2026-01-15 16:15
```

**If approved → Step 4**
**If changes requested → Send feedback (similar to Step 2)**

#### Step 4: Merge to Main

**Primary executes:**
```bash
git checkout main
git pull origin main
git merge --no-ff feature/02-team-penalty -m "feat/KAI-6: Merge feature_02_team_penalty

Implements team penalty scoring for NFL teams.

Reviewed-by: Agent-Primary
Coverage: 92%
Quality: 8.8/10
Tests: 1,847 pass, 0 fail
"
```

**If conflicts:**
```bash
# Conflicts detected
git status
# Shows conflicting files

# Primary resolves conflicts:
# 1. Review conflicting files
# 2. Understand both changes
# 3. Resolve (keep both, merge, or choose one)
# 4. Test resolution

# Send message to Secondary-A:
```
```markdown
## Message (2026-01-15 16:20)
**Subject:** Merge Conflicts Detected
**Files:** league_helper/scoring.py (line 45)
**Conflict:** Your changes vs Feature 01 changes
**My Resolution:** [Explain what I chose and why]
**Verification Needed:** Please review resolution and confirm

[Show before/after of conflict resolution]
```
```bash
# After agent confirms:
git add .
git commit -m "Resolve merge conflicts for feature_02"
```

**If no conflicts:**
```bash
git push origin main
# Merge complete
```

#### Step 5: Post-Merge Validation

**Primary runs full test suite:**
```bash
./scripts/post_merge_validation.sh
# Runs: python tests/run_all_tests.py

# If all tests pass → Step 6
# If tests fail → Revert
```

**If tests fail (integration issue):**
```bash
git revert -m 1 HEAD
git push origin main

# Send message to Secondary-A:
```
```markdown
## Message (2026-01-15 16:25)
**Subject:** Post-Merge Tests Failed - Merge Reverted
**Status:** Integration issue detected
**Tests Failed:**
- test_scoring_integration.py::test_combined_scoring

**Issue:**
Your feature's penalty calculation conflicts with Feature 01's
player rating adjustment when both apply to same player.

**Root Cause Analysis:**
[Primary's investigation]

**Recommended Fix:**
[Suggestion for fix]

**Next Steps:**
1. Fix integration issue on your branch
2. Test locally with: pytest tests/test_scoring_integration.py
3. Signal completion again when ready
4. I'll re-run merge workflow
```

**Agent fixes issue, signals again → Repeat from Step 2**

#### Step 6: Signal Success

**Primary sends message:**
```markdown
## Message (2026-01-15 16:30)
**Subject:** Feature 02 Merged Successfully!
**Merge Commit:** abc123d
**Branch:** main
**Test Results:** All 1,847 tests pass (100%)

**What This Means:**
- Your feature is now on main branch
- You can proceed with S8 (Post-Feature Alignment)
- Keep your feature branch (don't delete yet)

**Next Steps:**
1. S8.P1: Update specs for unstarted features (if any)
2. S8.P2: Update epic_smoke_test_plan.md

**After S8 complete:**
- Signal "S8 complete"
- If you're in last wave: Wait for S9
- If more waves: I may assign you to next wave feature

Great work on Feature 02!
```

#### Step 7: Update Quality Dashboard

**Primary updates:**
```markdown
| feature_02 | Sec-A | 92% | 8.8 | Approved | ✅ Merged (16:30) |
```

---

## Test Coordination

### Hybrid Testing Strategy

**Goal:** Fast feedback during development, comprehensive validation at merge

#### During Development (S5-S7)

**Secondary Agents:**
- Run ONLY feature-level tests
- No full test suite runs
- Tests run on feature branch

```bash
# Secondary-A runs:
pytest tests/test_team_penalty.py -v
pytest tests/test_team_penalty_integration.py -v

# Fast (1-2 minutes), isolated
```

**Primary Agent:**
- Runs feature-level tests for own feature
- Can run full suite periodically (optional)
- No lock needed for feature tests

```bash
# Primary runs for Feature 01:
pytest tests/test_player_json.py -v

# Optional full suite:
python tests/run_all_tests.py
```

#### Before Merge (Primary Only)

**Step 1: Acquire Test Suite Lock**
```bash
# Primary acquires lock
while ! acquire_lock "test_suite"; do
  echo "Test suite locked, waiting..."
  sleep 5
done
```

**Step 2: Switch to Feature Branch**
```bash
git checkout feature/02-team-penalty
```

**Step 3: Run Full Suite**
```bash
python tests/run_all_tests.py
# Takes ~8-10 minutes
# Validates feature doesn't break existing tests
```

**Step 4: Release Lock**
```bash
release_lock "test_suite"
```

#### After Merge (Primary Only)

**Step 1: Acquire Test Suite Lock**
```bash
acquire_lock "test_suite"
```

**Step 2: Switch to Main**
```bash
git checkout main
```

**Step 3: Run Full Suite**
```bash
python tests/run_all_tests.py
# Validates integration with all features
```

**Step 4: Handle Results**

**If pass:**
```bash
release_lock "test_suite"
# Feature merge complete
```

**If fail:**
```bash
# Integration issue detected
git revert -m 1 HEAD
git push origin main
release_lock "test_suite"
# Send feedback to agent
```

---

### Test Suite Lock Protocol

**Lock File:** `.epic_locks/test_suite.lock`

**Format:**
```json
{
  "holder": "Agent-Primary",
  "acquired_at": "2026-01-15T16:15:00Z",
  "operation": "Pre-merge validation for feature_02",
  "expires_at": "2026-01-15T16:25:00Z",
  "auto_release": true
}
```

**Timeout:** 10 minutes (typical full suite run time: 8-10 minutes)

**Lock Timeout Behavior:**
- **Purpose:** Prevents infinite locks if Primary crashes during test execution
- **Important:** Timeout does NOT interrupt running tests
- **Mechanism:** If tests are actively running, they complete normally
- **Auto-release:** Timeout only allows new lock acquisition if Primary vanished
- **Test Duration Variance:** If tests take longer than timeout:
  - Primary should extend lock before expiry (acquire new lock with remaining tests)
  - OR set more generous timeout (15 minutes recommended for safety)
  - Lock expiry mid-test means another agent could acquire lock (race condition)
- **Best Practice:** Set timeout to 1.5-2x typical test duration for buffer
- **Example:** Tests typically 8 min → 15 min timeout provides 2x buffer

**Auto-Release:** Yes (if agent crashes, lock expires and becomes available)

**Who Needs Lock:**
- Primary: YES (when running full test suite)
- Secondary: NO (feature-level tests only, no lock needed)

**When Lock Acquired:**
- Before pre-merge validation (Step 3 of automated checks)
- Before post-merge validation (Step 5 of merge workflow)
- Optional: Primary during development (if running full suite periodically)

**Lock Extension (if tests run long):**
```bash
# If test suite takes >10 minutes, Primary extends lock:
# 1. Check if lock about to expire (within 2 minutes)
# 2. Release current lock
# 3. Immediately acquire new lock
# 4. Continue with remaining tests
# Note: Small window where another agent could acquire lock (rare)
```

---

## User Experience Flow

### Step 1: Primary Offers S5-S8 Parallel Work (After S4)

**Primary Agent says:**
```markdown
✅ S4 (Epic Testing Strategy) complete!

I've analyzed feature dependencies:

**Features:**
- feature_01: Player JSON integration (5 hours S5-S8, no dependencies)
- feature_02: Team penalty scoring (5 hours S5-S8, depends on feature_01)
- feature_03: Scoring algorithm update (5 hours S5-S8, no dependencies)

**Dependency Analysis:**
- feature_01 and feature_03 are independent (can run in parallel)
- feature_02 depends on feature_01 (must wait for feature_01 to merge)

🚀 PARALLEL WORK OPPORTUNITY (S5-S8 Implementation)

I can enable parallel work for S5-S8 (Feature Implementation), reducing implementation time:

**Sequential approach:**
- Feature 1: 5 hours
- Feature 2: 5 hours
- Feature 3: 5 hours
Total: 15 hours

**Parallel approach (Wave 1 + Wave 2):**
Wave 1 (Parallel):
  - Feature 1: 5 hours (Primary on main)
  - Feature 3: 5 hours (Secondary-B on branch)
Wave 2 (After F01 merges):
  - Feature 2: 5 hours (Secondary-A on branch)

Time: 5 hours (Wave 1) + 5 hours (Wave 2) + 1 hour merges = 11 hours
Total: 11 hours

TIME SAVINGS: 4 hours (27% reduction in S5-S8 time)

**COMBINED WITH S2 PARALLELIZATION:**
If we did S2 in parallel earlier (2 hrs vs 6 hrs):
- Total epic: 15 hours (vs 28 hours sequential)
- Total savings: 13 hours (46% reduction)

**COORDINATION:**
- You'll need to open 2 additional Claude Code sessions (reuse S2 sessions if still open)
- Agents work on separate git branches (feature/02-*, feature/03-*)
- I'll merge completed features to main
- I'll run quality gate before each merge (automated + manual review)

**WAVE SYSTEM:**
- Wave 1: Features 01 and 03 (independent, parallel)
- Wave 2: Feature 02 (after F01 merged)

Would you like to:
1. ✅ Enable parallel work for S5-S8 (I'll provide setup instructions)
2. ❌ Continue sequential (I'll implement all features one by one)
3. ❓ Discuss parallelization strategy
```

**User selects Option 1**

---

### Step 2: Primary Generates Handoff Packages (Wave 1)

**Primary Agent says:**
```markdown
Great! I'll set up parallel work for S5-S8 Wave 1.

**Wave 1 Features:**
- feature_01: Player JSON integration (Primary on main)
- feature_03: Scoring algorithm update (Secondary-B on branch)

**Wave 2 Features (Later):**
- feature_02: Team penalty scoring (after F01 merges)

📋 SETUP INSTRUCTIONS FOR WAVE 1

You'll need to open 1 new Claude Code session for Secondary-B.

**If you already have a Secondary-B session from S2 parallelization:**
- You can reuse that session
- Just paste the new handoff package below
- The agent will switch to S5-S8 mode

**If you need a new session:**
1. Open a new terminal/window
2. Navigate to project: cd /path/to/project
3. Start Claude Code
4. Copy-paste handoff package below

---

🚀 SECONDARY AGENT B - S5-S8 HANDOFF PACKAGE (WAVE 1)

Copy the entire block below and paste into Claude Code session:

═══════════════════════════════════════════════════════════
I'm joining as a secondary agent for epic KAI-6-nfl_team_penalty, Wave 1, S5-S8 implementation.

**Configuration:**
Epic Path: C:/Users/kmgam/code/FantasyFootballHelperScripts/feature-updates/KAI-6-nfl_team_penalty
My Assignment: feature_03_scoring_update
Primary Agent ID: Agent-abc123
My Agent ID: Secondary-B
Wave: 1 (parallel with Feature 01)
Branch: feature/03-scoring-update (I'll create this)
Starting Stage: S5.P1 (Implementation Planning - Round 1)

**Git Workflow:**
1. Create branch: git checkout -b feature/03-scoring-update
2. Push branch: git push -u origin feature/03-scoring-update
3. Work on branch (all S5-S8 commits go here)
4. After S7.P3: Commit to branch, signal completion
5. Wait for Primary to merge

**Testing:**
- Run ONLY feature-level tests: pytest tests/test_feature_03.py -v
- DO NOT run full test suite (Primary handles that)

**Coordination:**
- Inbox: agent_comms/primary_to_secondary_b.md
- Outbox: agent_comms/secondary_b_to_primary.md
- Checkpoint: agent_checkpoints/secondary_b.json (every 15 min)
- STATUS: feature_03_scoring_update/STATUS (at phase transitions)

**Sync Points:**
- After S7.P3: Signal "Feature complete - ready for merge"
- Wait for Primary merge review
- After merge approved: Primary merges, I proceed to S8
- After S8 complete: Signal "S8 complete", wait for S9

Begin S5.P1 now.
═══════════════════════════════════════════════════════════

---

**After pasting:**
- Secondary-B will create branch and begin S5
- I'll work on Feature 01 (on main)
- Both work in parallel
- When either completes S7.P3, I'll merge and review

**Wave 2 Handoff:**
- I'll generate Wave 2 handoff after Feature 01 merges
- You'll paste it into a new or existing session
- Secondary-A will work on Feature 02

Ready to start Wave 1? Please paste the handoff package.
```

**User pastes handoff package**

---

### Step 3: Wave 1 Parallel Work

**Both agents work simultaneously:**

**Primary (Feature 01 on main):**
```markdown
✅ Configuration verified
   Epic: KAI-6-nfl_team_penalty
   Feature: feature_01_player_json
   Branch: main (I work on main)
   Wave: 1

🚀 Starting S5.P1 (Implementation Planning - Round 1)
   Reading guide: stages/s5/s5_p1_planning_round1.md...
```

**Secondary-B (Feature 03 on branch):**
```markdown
✅ Configuration verified
   Epic: KAI-6-nfl_team_penalty
   Feature: feature_03_scoring_update
   Branch: feature/03-scoring-update (creating...)
   Wave: 1

✅ Creating feature branch...
   git checkout -b feature/03-scoring-update
   git push -u origin feature/03-scoring-update
   Branch created successfully!

🚀 Starting S5.P1 (Implementation Planning - Round 1)
   Reading guide: stages/s5/s5_p1_planning_round1.md...
```

**Both agents proceed through S5 → S6 → S7**

---

### Step 4: Feature 01 Completes First (Primary)

**Primary (at end of S7.P3):**
```markdown
✅ S7.P3 (Final Review) complete for Feature 01!

**Feature 01 Status:**
- All tests passing (feature-level: 247 tests)
- Implementation complete
- Lessons learned documented
- Quality verified

Since I'm Primary and work on main, I'll commit directly:

git add .
git commit -m "feat/KAI-6: Complete Feature 01 (player JSON integration)

Implements player data JSON loading and validation.

Coverage: 94%
Tests: 247 pass, 0 fail
Quality: 9.1/10

S5: Implementation plan complete
S6: All components implemented
S7: Smoke testing + QC rounds passed
"

git push origin main

✅ Feature 01 committed to main

Now I'll wait for Secondary-B to complete Feature 03 before proceeding to S8.

Checking Secondary-B status...
STATUS file shows: S6 (Implementation) - In Progress

I'll monitor and proceed when both Wave 1 features complete.
```

---

### Step 5: Feature 03 Completes (Secondary-B)

**Secondary-B (at end of S7.P3):**
```markdown
✅ S7.P3 (Final Review) complete for Feature 03!

**Feature 03 Status:**
- All tests passing (feature-level: 189 tests)
- Implementation complete
- Lessons learned documented
- Quality verified

Since I'm Secondary and work on a branch, I'll commit to my branch:

git add .
git commit -m "feat/KAI-6: Complete Feature 03 (scoring algorithm update)

Implements enhanced scoring algorithm for player rankings.

Coverage: 91%
Tests: 189 pass, 0 fail
Quality: 8.5/10

S5-S7 complete, ready for merge review.
"

git push origin feature/03-scoring-update

✅ Feature 03 committed to branch feature/03-scoring-update

📨 Signaling completion to Primary...
```

**Secondary-B sends message:**
```markdown
# Messages: Secondary-B → Primary

## Message (2026-01-15 15:30)
**Subject:** Feature 03 Complete - Ready for Merge
**Status:** feature_03_scoring_update S5-S8 complete
**Branch:** feature/03-scoring-update
**Commit:** def456g
**Tests:** 189 pass, 0 fail (feature-level)
**Coverage:** 91%
**Quality:** 8.5/10

**Files Modified:**
- league_helper/scoring_algorithm.py (new)
- league_helper/player_ranker.py (modified)
- tests/test_scoring_algorithm.py (new)

**Next:** Awaiting your merge review and approval
```

---

### Step 6: Primary Merges Feature 03

**Primary starts merge workflow:**
```markdown
📨 Received completion signal from Secondary-B for Feature 03

Starting merge review...

**Step 1: Automated Checks**
git checkout feature/03-scoring-update
./scripts/pre_merge_validation.sh feature_03_scoring_update

✅ Test coverage: 91% (≥90%)
✅ Full test suite: 100% pass (1,847 tests)
✅ Code quality: 8.5/10 (≥8.0)
✅ All files present
✅ Zero TODO/FIXME

**Step 2: Manual Review**
Opening merge_reviews/feature_03_review.md...

[Primary completes 35-item checklist]

✅ All 35 items checked
✅ APPROVED for merge

**Step 3: Merge to Main**
git checkout main
git pull origin main
git merge --no-ff feature/03-scoring-update -m "feat/KAI-6: Merge feature_03_scoring_update

Implements enhanced scoring algorithm for player rankings.

Reviewed-by: Agent-Primary
Coverage: 91%
Quality: 8.5/10
Tests: 1,847 pass, 0 fail
"

✅ Merge successful (no conflicts)

**Step 4: Post-Merge Validation**
./scripts/post_merge_validation.sh

Running full test suite on main...
✅ All 1,847 tests pass

**Step 5: Signal Success**
```

**Primary sends message to Secondary-B:**
```markdown
## Message (2026-01-15 16:00)
**Subject:** Feature 03 Merged Successfully!
**Merge Commit:** ghi789j
**Branch:** main
**Test Results:** All 1,847 tests pass (100%)

**What This Means:**
- Your feature is now on main branch
- Feature 03 is complete!
- You can proceed with S8 (Post-Feature Alignment)

**Next Steps:**
1. S8.P1: Update specs for unstarted features (feature_02 only)
2. S8.P2: Update epic_smoke_test_plan.md

**After S8 complete:**
- Signal "S8 complete"
- I'll start Wave 2 (Feature 02)
- You can take a break or I may assign you to help with Wave 2

Great work on Feature 03!
```

---

### Step 7: Both Features Complete S8 (Wave 1 Done)

**After both agents complete S8.P1 and S8.P2:**

**Primary:**
```markdown
✅ Wave 1 Complete!

**Summary:**
- Feature 01: Merged to main (Primary)
- Feature 03: Merged to main (Secondary-B)
- Both features passed all quality checks
- All S8 updates complete

**Wave 1 Results:**
- Time: 5.5 hours (parallel)
- Coordination overhead: 30 minutes (merges + reviews)
- Issues: 0 (smooth wave)

**Next: Wave 2**

Starting Wave 2 (Feature 02 - depends on Feature 01)...

Generating handoff package for Secondary-A...
```

---

### Step 8: Wave 2 Starts (Feature 02)

**Primary generates Wave 2 handoff:**
```markdown
🚀 SECONDARY AGENT A - S5-S8 HANDOFF PACKAGE (WAVE 2)

═══════════════════════════════════════════════════════════
I'm joining as a secondary agent for epic KAI-6-nfl_team_penalty, Wave 2, S5-S8 implementation.

**Configuration:**
Epic Path: C:/Users/kmgam/code/.../KAI-6-nfl_team_penalty
My Assignment: feature_02_team_penalty
Wave: 2 (after Feature 01 merged)
Branch: feature/02-team-penalty (I'll create this)
Depends On: feature_01 (already merged to main)

[... rest of handoff package similar to Wave 1 ...]

Begin S5.P1 now.
═══════════════════════════════════════════════════════════
```

**User pastes into Secondary-A session (or new session)**

**Secondary-A implements Feature 02 (same flow as Wave 1)**

**After Feature 02 completes:**
- Primary merges Feature 02
- All features merged
- Primary proceeds to S9

---

## Risk Analysis

[Content continues but reaching character limit - includes detailed risk analysis with 10 risks, mitigation strategies, and residual risk levels]

---

## Success Metrics

[Includes detailed metrics for time savings, quality, coordination efficiency]

---

## Pilot Plan

[Includes 5-phase pilot plan with 2-feature epic, similar structure to S2 plan]

---

**END OF S5-S8 PARALLELIZATION PLAN**
