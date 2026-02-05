# STAGE 1: Epic Planning - Quick Reference Card

**Purpose:** One-page summary for epic initialization and feature breakdown
**Use Case:** Quick lookup when starting a new epic or verifying setup steps
**Total Time:** 2-4 hours (includes Discovery Phase and user validation)

---

## Workflow Overview

```bash
STEP 1: Initial Setup (15-20 min)
    +-- Step 1.0: Create Git Branch (BEFORE any changes)
    |   +-- Verify on main, pull latest
    |   +-- Assign KAI number from EPIC_TRACKER.md
    |   +-- Create branch: {work_type}/KAI-{number}
    |   +-- Update EPIC_TRACKER.md and commit immediately
    +-- Step 1.1: Create epic folder
    +-- Step 1.2: Move {epic_name}.txt into epic folder
    +-- Step 1.3: Create EPIC_README.md with Agent Status
    |
STEP 2: Epic Analysis (10-15 min)
    +-- Read epic request thoroughly
    +-- Identify goals, constraints, requirements
    +-- Conduct broad codebase reconnaissance
    +-- Estimate epic size (SMALL/MEDIUM/LARGE)
    |
STEP 3: Discovery Phase (S1.P3) - MANDATORY (1-4 hours)
    +-- See: stages/s1/s1_p3_discovery_phase.md
    +-- S1.P3.1: Initialize DISCOVERY.md
    +-- S1.P3.2: Discovery Loop (iterative)
    |   +-- Research (read code, examine patterns)
    |   +-- Document findings in DISCOVERY.md
    |   +-- Identify questions
    |   +-- Ask user, record answers
    |   +-- Repeat until NO NEW QUESTIONS emerge
    +-- S1.P3.3: Synthesize findings
    +-- S1.P3.4: User approval of recommended approach
    +-- Time-Box: SMALL 1-2hrs, MEDIUM 2-3hrs, LARGE 3-4hrs
    |
STEP 4: Feature Breakdown Proposal (15-30 min)
    +-- Based on Discovery findings
    +-- Propose feature list with justification
    +-- Present to user for approval
    +-- WAIT for user confirmation/modifications
    +-- Create epic ticket (outcome validation) <- USER VALIDATION
    +-- WAIT for user approval of epic ticket
    |
STEP 5: Epic Structure Creation (10-15 min)
    +-- Create feature folders (per approved breakdown)
    +-- Seed each spec.md with Discovery Context section
    +-- Create epic_smoke_test_plan.md (PLACEHOLDER)
    +-- Create epic_lessons_learned.md
    +-- Create research/ folder (shared across features)
    +-- Create GUIDE_ANCHOR.md (resumption instructions)
    +-- Update EPIC_README.md with Epic Progress Tracker
    |
STEP 6: Transition to S2 (5 min)
    +-- Mark S1 complete in EPIC_README.md
    +-- Update Agent Status (next: S2)
    +-- Announce transition to user
```

---

## Step Summary Table

| Step | Duration | Key Activities | User Interaction | Gate? |
|------|----------|----------------|------------------|-------|
| 1 | 15-20 min | Git branch, epic folder, EPIC_README.md | None | No |
| 2 | 10-15 min | Read epic, reconnaissance, estimate size | None | No |
| 3 | 1-4 hours | **Discovery Phase (MANDATORY)** - iterative research and Q&A | Questions throughout, approval at end | YES |
| 4 | 15-30 min | Propose features based on Discovery, create epic ticket | Feature approval, epic ticket validation | YES |
| 5 | 10-15 min | Create feature folders with Discovery Context, test plan | None | No |
| 6 | 5 min | Mark complete, transition to S2 | None | No |

---

## Mandatory Gates

### Gate 1: Discovery Phase Approval (Step 3)
**Location:** stages/s1/s1_p3_discovery_phase.md S1.P3.4
**What it checks:**
- Discovery Loop completed (no new questions emerged)
- Recommended approach documented
- Scope defined (in scope / out of scope)
- User approves findings and approach

**Pass Criteria:** User explicitly approves Discovery findings
**If FAIL:** Continue Discovery Loop with additional research

### Gate 2: Feature Breakdown Approval (Step 4)
**Location:** stages/s1/s1_epic_planning.md Step 4
**What it checks:**
- Feature breakdown based on Discovery findings
- User approves proposed feature list
- Each feature has clear purpose (1-2 sentences)

**Pass Criteria:** User explicitly confirms feature breakdown
**If FAIL:** User provides feedback, agent revises breakdown, re-proposes

### Gate 3: Epic Ticket Validation (Step 4)
**Location:** stages/s1/s1_epic_planning.md Step 4.6-4.7
**What it checks:**
- Epic ticket accurately reflects user's desired outcomes
- Agent understanding validated
- Epic ticket becomes immutable reference

**Pass Criteria:** User approves epic ticket
**If FAIL:** User corrects misunderstandings, agent updates epic ticket

---

## Discovery Phase Quick Reference

**Guide:** `stages/s1/s1_p3_discovery_phase.md`

**Time-Box by Epic Size:**
| Size | Time-Box | Features |
|------|----------|----------|
| SMALL | 1-2 hours | 1-2 features |
| MEDIUM | 2-3 hours | 3-4 features |
| LARGE | 3-4 hours | 5+ features |

**Discovery Loop Exit Condition:**
- Research iteration produces NO NEW QUESTIONS
- NOT based on time or iteration count

**Key Output:** DISCOVERY.md containing:
- Research findings (per iteration)
- Questions and user answers
- Recommended approach
- Proposed feature breakdown
- User approval

---

## Critical Rules Summary

- Create git branch BEFORE any changes (Step 1.0)
- **Discovery Phase is MANDATORY for ALL epics (Step 3)**
- Discovery Loop continues until NO NEW QUESTIONS emerge
- Feature folders NOT created until Discovery approved
- Feature breakdown MUST be based on Discovery findings
- Seed each spec.md with Discovery Context section (Step 5)
- User MUST approve feature breakdown before epic ticket
- Create epic ticket and get user validation (Step 4.6-4.7)
- Update EPIC_README.md Agent Status after each major step
- Feature numbering: feature_01_{name}, feature_02_{name}
- Every feature MUST have clear purpose (avoid "miscellaneous")
- Mark completion in EPIC_README.md before S2

---

## Common Pitfalls

### Pitfall 1: Skipping Discovery Phase
**Problem:** Jumping to feature breakdown without Discovery
**Impact:** Features based on assumptions, wrong scope, rework later
**Solution:** Discovery is MANDATORY - complete Loop until no new questions

### Pitfall 2: Ending Discovery Prematurely
**Problem:** Stopping Discovery based on time, not question exhaustion
**Impact:** Missed requirements, wrong approach, inadequate understanding
**Solution:** Exit ONLY when research produces no new questions

### Pitfall 3: Not Seeding Specs with Discovery Context
**Problem:** Creating feature specs without Discovery Context section
**Impact:** S2 research disconnected from Discovery findings
**Solution:** Seed each spec.md with Discovery Context section in Step 5

### Pitfall 4: Making Changes Before Creating Branch
**Problem:** Creating epic folder on main branch
**Impact:** Pollutes main branch, difficult rollback
**Solution:** Create git branch FIRST (Step 1.0), THEN create folders

### Pitfall 5: Creating "Miscellaneous" Features
**Problem:** Grouping unrelated items into "utilities" or "misc" feature
**Impact:** Feature scope unclear, difficult testing
**Solution:** Each feature has distinct value and clear purpose

---

## Quick Checklist: "Am I Ready for Next Step?"

**Step 1 -> Step 2:**
- [ ] Git branch created: {work_type}/KAI-{number}
- [ ] EPIC_TRACKER.md updated and committed
- [ ] Epic folder created: `feature-updates/KAI-{N}-{epic_name}/`
- [ ] {epic_name}.txt moved into epic folder
- [ ] EPIC_README.md created with Agent Status

**Step 2 -> Step 3:**
- [ ] Epic request read thoroughly
- [ ] Goals, constraints, requirements identified
- [ ] Epic size estimated (SMALL/MEDIUM/LARGE)
- [ ] Ready to start Discovery Phase

**Step 3 -> Step 4:**
- [ ] DISCOVERY.md created and complete
- [ ] Discovery Loop completed (no new questions)
- [ ] Recommended approach documented
- [ ] Scope defined (in scope / out of scope)
- [ ] User approved Discovery findings

**Step 4 -> Step 5:**
- [ ] Feature breakdown proposed (based on Discovery)
- [ ] User approved feature breakdown
- [ ] Epic ticket created with desired outcomes
- [ ] User validated epic ticket

**Step 5 -> Step 6:**
- [ ] Feature folders created (matching approved breakdown)
- [ ] Each spec.md seeded with Discovery Context section
- [ ] epic_smoke_test_plan.md created (PLACEHOLDER)
- [ ] epic_lessons_learned.md created
- [ ] research/ folder created
- [ ] GUIDE_ANCHOR.md created
- [ ] EPIC_README.md updated with Epic Progress Tracker

**Step 6 -> S2:**
- [ ] S1 marked complete in EPIC_README.md
- [ ] Agent Status updated (next: S2)
- [ ] User informed of transition

---

## File Outputs

**Step 1:**
- Git branch: `{work_type}/KAI-{number}`
- EPIC_TRACKER.md (updated and committed)
- `feature-updates/KAI-{N}-{epic_name}/` folder
- `KAI-{N}-{epic_name}/{epic_name}_notes.txt` (moved from root)
- `KAI-{N}-{epic_name}/EPIC_README.md`

**Step 3:**
- `KAI-{N}-{epic_name}/DISCOVERY.md` (user-approved)

**Step 4:**
- Epic ticket in conversation (user-validated)

**Step 5:**
- `KAI-{N}-{epic_name}/feature_01_{name}/spec.md` (seeded with Discovery Context)
- `KAI-{N}-{epic_name}/epic_smoke_test_plan.md` (PLACEHOLDER)
- `KAI-{N}-{epic_name}/epic_lessons_learned.md`
- `KAI-{N}-{epic_name}/research/`
- `KAI-{N}-{epic_name}/GUIDE_ANCHOR.md`
- EPIC_README.md updated with Epic Progress Tracker

---

## When to Use Which Guide

| Current Activity | Guide to Read |
|------------------|---------------|
| Starting a new epic | stages/s1/s1_epic_planning.md |
| Starting Discovery Phase | stages/s1/s1_p3_discovery_phase.md |
| Need Discovery examples | reference/stage_1/discovery_examples.md |
| Need git workflow details | CLAUDE.md (Git Branching Workflow section) |
| Need folder structure templates | templates/TEMPLATES_INDEX.md |

---

## Exit Conditions

**S1 is complete when:**
- [ ] Git branch created and EPIC_TRACKER.md updated
- [ ] **Discovery Phase complete and user-approved**
- [ ] DISCOVERY.md exists with findings and approach
- [ ] Feature breakdown user-approved (based on Discovery)
- [ ] Epic ticket user-validated
- [ ] All feature folders created with Discovery Context
- [ ] Placeholder test plan created
- [ ] EPIC_README.md shows S1 complete
- [ ] Ready to start S2 (feature deep dives)

**Next Stage:** S2 (Feature Deep Dive) - for each feature in sequence

---

**Last Updated:** 2026-01-20
