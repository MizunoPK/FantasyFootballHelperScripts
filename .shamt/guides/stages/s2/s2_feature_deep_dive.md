# S2: Feature Planning Guide (ROUTER)

🚨 **IMPORTANT: This guide has been redesigned**

**This is a routing guide.** The complete S2 workflow is now split across two phases:

- **S2.P1 (Spec Creation and Refinement):** 3 iterations - Discovery, Checklist Resolution, Refinement (embeds Gates 1, 2, includes Gate 3)
- **S2.P2 (Cross-Feature Alignment):** Pairwise comparison (Primary agent only)

**📖 Read the appropriate phase guide based on your current phase.**

---

## 🚨 MANDATORY READING PROTOCOL

**Before taking any S2 action — including when resuming a prior session:**
1. Read this ENTIRE routing guide
2. Check EPIC_README.md Agent Status for current mode (parallel/sequential) and current phase
3. Use the Parallel Work Check (Section 1 below) to determine your routing path

---

## Table of Contents

1. [🔀 Parallel Work Check (FIRST PRIORITY)](#-parallel-work-check-first-priority)
2. [📖 Terminology Note](#-terminology-note)
3. [Prerequisites](#prerequisites)
4. [Quick Navigation](#quick-navigation)
5. [Overview](#overview)
6. [Sub-Stage Breakdown](#sub-stage-breakdown)
7. [Workflow Through Sub-Stages](#workflow-through-sub-stages)
8. [Mandatory Gates](#mandatory-gates)
9. [Critical Rules (Same Across All Sub-Stages)](#critical-rules-same-across-all-sub-stages)
10. [How to Use This Router Guide](#how-to-use-this-router-guide)
11. [Exit Criteria](#exit-criteria)
12. [Next Stage](#next-stage)
13. [Why S2 Was Split](#why-s2-was-split)
14. [Frequently Asked Questions](#frequently-asked-questions)
15. [Summary](#summary)

---

## 🔀 Parallel Work Check (FIRST PRIORITY)

**Before proceeding with S2 phases, check if you're in parallel work mode:**

### Are You a Secondary Agent?

**Check for handoff package:**
- If you received a handoff package (starts with "I'm joining as a secondary agent...")
- OR if your most recent message contains "My Agent ID: Secondary-A/B/C"
- **THEN:** You're a Secondary agent in parallel mode

**→ Go to:** `parallel_work/s2_secondary_agent_guide.md`
- Complete startup configuration
- Execute S2.P1 for your assigned feature (3 iterations)
- **STOP after S2.P1** - Do NOT proceed to S2.P2
- Wait for Primary to run S2.P2 and S3
- Follow coordination protocols (checkpoints, inbox, STATUS)
- **Do NOT continue with this router guide**

### Are You Primary Agent in Group-Based Parallel Mode?

**Check for group-based parallelization:**
- EPIC_README.md has "Feature Dependency Groups (S2 Only)" section
- Multiple dependency groups documented (Group 1, Group 2, etc.)
- User accepted group-based parallel work offering in S1
- Currently working on Group N features

**→ Go to:** `parallel_work/s2_primary_agent_group_wave_guide.md` (Group Wave Management)

**Group Wave Workflow:**
1. Complete S2 for Group 1 features first (solo work)
2. After Group 1 S2 complete → generate handoffs for Group 2
3. Coordinate Group 2 parallel work (secondary agents)
4. Repeat for additional groups if needed
5. After all groups complete S2 → run S2.P2 across ALL features
6. Proceed to S3 (groups no longer matter)

**Within each group:** Follow standard parallel coordination
**Use this router guide ONLY for phase navigation**

### Are You Primary Agent in Full Parallel Mode?

**Check for full parallelization (no groups):**
- All features independent (no spec-level dependencies)
- OR EPIC_README.md says "All features independent - Single S2 wave"
- User accepted parallel work offering in S1
- Generated handoffs for all features immediately

**→ Go to:** `parallel_work/s2_primary_agent_guide.md`
- Follow Primary workflow for parallel S2
- Work on Feature 01 using S2.P1 guide (3 iterations)
- Coordinate secondary agents (monitor, escalations, sync)
- After all features complete S2.P1 → run S2.P2 alone
- After S2 complete → run S3 alone (S4 deprecated)
- **Use this router guide ONLY for phase navigation**

### Are You in Sequential Mode?

**Indicators:**
- No handoff package received
- User declined parallel work (or wasn't offered)
- Only you working on epic
- Working on features one at a time

**→ Continue below** with standard S2 workflow
- Use this router guide to navigate between phases
- Execute S2.P1 → S2.P2 for each feature (or feature group)

---

## 📖 Terminology Note

**S2 is split into two phases:**
- **S2.P1:** Spec Creation and Refinement (guide: `s2_p1_spec_creation_refinement.md`)
  - 3 iterations: I1 (Discovery), I2 (Checklist Resolution), I3 (Refinement & Alignment)
  - Embeds Gates 1 & 2, includes Gate 3 (User Checklist Approval)
- **S2.P2:** Cross-Feature Alignment (guide: `s2_p2_cross_feature_alignment.md`)
  - Pairwise comparison with Validation Loop
  - Primary agent only (secondary agents wait)

**Naming:** Uses hierarchical notation (S2.P1, S2.P2) with iterations (S2.P1.I1, S2.P1.I2, S2.P1.I3)

---

## Prerequisites

**Before starting S2 for any feature:**

- [ ] S1 (Epic Planning) completed for this epic
- [ ] DISCOVERY.md created and user-approved
- [ ] Feature folder created with spec.md containing Discovery Context section
- [ ] checklist.md file exists (may be empty)
- [ ] Feature README.md has Agent Status section
- [ ] EPIC_README.md Feature Tracking table lists this feature

**If any prerequisite fails:**
- Return to S1 to complete missing items
- Do NOT proceed with S2 until all prerequisites met

---

## Quick Navigation

**Use this table to find the right guide:**

| Current Phase | Guide to Read | Time Estimate |
|---------------|---------------|---------------|
| Starting S2 | `stages/s2/s2_p1_spec_creation_refinement.md` | 2.25-4 hours |
| S2.P1.I1: Feature-Level Discovery | `stages/s2/s2_p1_spec_creation_refinement.md` | 60-90 min |
| S2.P1.I2: Checklist Resolution | `stages/s2/s2_p1_spec_creation_refinement.md` | 45-90 min |
| S2.P1.I3: Refinement & Alignment | `stages/s2/s2_p1_spec_creation_refinement.md` | 30-60 min |
| S2.P2: Cross-Feature Alignment | `stages/s2/s2_p2_cross_feature_alignment.md` | 20-60 min |

---

## Overview

**What is S2?**
Feature Planning is where you research each feature, create detailed specifications with requirement traceability, resolve questions with user, validate alignment, and get user approval (Gate 3).

**Total Time Estimate:** 2.25-4 hours per feature (2 phases, 3 iterations in P1, 3 gates)


**Exit Condition:** S2 is complete for a feature when spec has user-approved acceptance criteria (Gate 3 passed), Gates 1 & 2 passed via Validation Loops, and cross-feature alignment verified (S2.P2)

---

## Sub-Stage Breakdown

### S2.P1: Spec Creation and Refinement (2.25-4 hours)

**Guide:** `stages/s2/s2_p1_spec_creation_refinement.md`

**What it covers (3 iterations):**

**I1 — Feature-Level Discovery (60-90 min):**
- Read Discovery Context (review DISCOVERY.md, note integration points)
- Reference previously completed features for alignment and pattern consistency
- Targeted Research (find exact files/classes to modify, read implementations, verify library compatibility)
- Draft initial spec.md with requirements and traceability
- Research Completeness Audit (Gate 1 embedded — MANDATORY)

**I2 — Checklist Resolution (45-90 min):**
- Resolve all checklist questions with user ONE at a time
- Update spec.md in real-time after each answer

**I3 — Refinement & Alignment (30-60 min):**
- Dynamic Scope Adjustment (split feature if checklist >35 items)
- Cross-feature comparison with completed features
- Spec-to-Epic Alignment Check (Gate 2 embedded — MANDATORY)
- Acceptance Criteria creation + User Approval (Gate 3)

**Key Outputs:**
- spec.md: Discovery Context, requirements with traceability, acceptance criteria (user approved)
- checklist.md: All questions resolved (zero open items)
- epic/research/{FEATURE_NAME}_DISCOVERY.md: Research findings

**When complete:** S2.P1 complete — Secondary agents STOP here, Primary proceeds to S2.P2

---

### S2.P2: Cross-Feature Alignment (20-60 min)

**Guide:** `stages/s2/s2_p2_cross_feature_alignment.md`

**What it covers:**
- Pairwise comparison of all features' specs for conflicts and duplication
- Validation Loop for systematic cross-feature checks
- **Primary agent only** — secondary agents wait after S2.P1

**Key Outputs:**
- Cross-feature conflicts resolved and documented
- Shared patterns and interfaces identified
- EPIC_README.md Feature Tracking updated

**When complete:** S2 is COMPLETE for the epic → proceed to S3

---

## Workflow Through Sub-Stages

```text
┌──────────────────────────────────────────────────────────────┐
│                   S2 Workflow                                │
└──────────────────────────────────────────────────────────────┘

Start Feature Deep Dive
          │
          ▼
    ┌──────────────────────────────────────────────────┐
    │  S2.P1: Spec Creation and Refinement (2.25-4h)  │
    │                                                  │
    │  I1 — Feature-Level Discovery (60-90 min)        │
    │    • Read Discovery Context                      │
    │    • Reference completed features                │
    │    • Targeted Research                           │
    │    • Draft spec.md with traceability             │
    │    • Research Audit ← GATE 1                     │
    │                    ↓                             │
    │  I2 — Checklist Resolution (45-90 min)           │
    │    • Resolve questions ONE at a time             │
    │    • Update spec.md in real-time                 │
    │                    ↓                             │
    │  I3 — Refinement & Alignment (30-60 min)         │
    │    • Scope Adjustment (split if >35 items)       │
    │    • Cross-feature comparison                    │
    │    • Spec-to-Epic Alignment Check ← GATE 2       │
    │    • Acceptance Criteria + User Approval ← GATE 3│
    └──────────────────────────────────────────────────┘
          │
          ▼ (Secondary agents STOP here)
    ┌──────────────────────────────────────────────────┐
    │  S2.P2: Cross-Feature Alignment (20-60 min)      │
    │  [Primary agent only]                            │
    │    • Pairwise comparison across all features     │
    │    • Validation Loop for cross-feature checks    │
    └──────────────────────────────────────────────────┘
          │
          ▼
    S2 COMPLETE
          │
          ▼
    [More features?]
     │           │
    YES         NO
     │           │
     ▼           ▼
  Next        S3
 Feature
 S2.P1
```

---

## Mandatory Gates

**S2 has THREE mandatory gates that cannot be skipped:**

### Gate 1: Research Completeness Audit (S2.P1.I1)

**Purpose:** Verify research was thorough enough to avoid "should have known" checklist questions

**Pass Criteria:**
- Can cite EXACT files/classes that will be modified (with line numbers)
- Have READ source code (not just searched)
- Can cite actual method signatures from source
- Have searched for similar features and READ their implementation
- Have READ actual data files (not just assumed format)
- Have reviewed DISCOVERY.md in this phase

**If fail:**
- Return to I1 targeted research
- Conduct additional research
- Collect missing evidence
- Re-run audit

**Cannot proceed to S2.P1.I2 without passing this gate.**

---

### Gate 2: Spec-to-Epic Alignment Check (S2.P1.I3)

**Purpose:** Verify spec accurately reflects Discovery findings (no scope creep, no missing requirements)

**Pass Criteria:**
- Every requirement traces back to epic request OR user answer OR logical derivation
- No requirements with "assumption" as source
- No scope creep (adding things user didn't ask for)
- No missing requirements (user asked but not in spec)
- All requirements have cited sources

**If fail:**
- Remove scope creep items (move to checklist as questions)
- Add missing requirements from epic
- Fix requirement sources (Epic/User Answer/Derived)
- Re-run alignment check

**Cannot complete I3 (Refinement & Alignment) without passing this gate.**

---

### Gate 3: User Approval (S2.P1.I3)

**Purpose:** Get explicit user sign-off on acceptance criteria before implementation planning

**Pass Criteria:**
- Acceptance Criteria section created in spec.md
- User has reviewed acceptance criteria
- User explicitly approved (said "yes", "approved", "looks good", etc.)
- Approval checkbox marked [x]
- Approval timestamp documented

**If fail:**
- Update spec based on user feedback
- Re-present acceptance criteria
- Wait for approval again

**Cannot proceed to S3 without user approval.**

---

## Critical Rules (Same Across All Sub-Stages)

```text
┌─────────────────────────────────────────────────────────────┐
│ CRITICAL RULES - Apply to ALL sub-stages                    │
└─────────────────────────────────────────────────────────────┘

1. ⚠️ ALWAYS start I1 with Discovery Context Review
   - Review DISCOVERY.md for epic-level findings
   - Verify spec has Discovery Context section

2. ⚠️ Research MUST be thorough BEFORE creating checklist
   - Gate 1 (Research Completeness Audit in I1) is MANDATORY
   - Evidence required: file paths, line numbers, code snippets

3. ⚠️ NEVER MAKE ASSUMPTIONS - CONFIRM WITH USER FIRST
   - Do NOT assume requirements or behavior
   - ASK USER via checklist.md questions
   - Spec assertions MUST be traced to sources

4. ⚠️ Every requirement MUST have traceability
   - Source: Epic Request (cite line)
   - Source: User Answer (cite question)
   - Source: Derived Requirement (explain derivation)
   - If source is "assumption" → add to checklist as question

5. ⚠️ ONE question at a time (don't batch questions)
   - Ask question
   - Wait for user answer
   - Update spec/checklist immediately
   - Then ask next question

6. ⚠️ Targeted research for THIS feature ONLY
   - Do NOT deep dive into other features yet
   - Keep research focused on current feature's scope

7. ⚠️ All research documents go in epic's research/ folder
   - NOT in feature folder
   - Shared across all features

8. ⚠️ If checklist grows >35 items, propose split
   - Too large to implement systematically
   - Get user approval before splitting
```

---

## How to Use This Router Guide

### If you're starting S2:

**READ:** `stages/s2/s2_p1_spec_creation_refinement.md`

**Use the phase transition prompt** from `prompts_reference_v2.md`:
```markdown
I'm starting S2.P1 (Spec Creation and Refinement) for Feature {N}: {Name}.

I acknowledge:
- This guide covers all 3 iterations: I1 (Discovery), I2 (Checklist Resolution), I3 (Refinement & Alignment)
- I must review DISCOVERY.md (I1 step 1) for epic-level context
- Gate 1 (Research Audit) is embedded in I1 — cannot proceed to I2 without passing
- Gate 2 (Spec-to-Epic Alignment) and Gate 3 (User Approval) are in I3
- Research must be targeted (THIS feature only, not entire epic)

Ready to begin I1: Feature-Level Discovery.
```

---

### If you're resuming mid-S2:

**Check feature README.md Agent Status** to see current phase:

```markdown
**Current Phase:** DEEP_DIVE
**Current Step:** Phase {N} - {Description}
```

**Then read the appropriate guide:**
- **Mid-S2.P1 (any iteration — I1, I2, or I3):** Read `stages/s2/s2_p1_spec_creation_refinement.md`
- **Mid-S2.P2:** Read `stages/s2/s2_p2_cross_feature_alignment.md`

**Continue from "Next Action" in Agent Status.**

---

### If you're transitioning between phases:

**After completing S2.P1 (Gate 3 passed — user approved acceptance criteria):**
- Update feature README.md Agent Status: "S2.P1 complete, starting S2.P2"
- **If Primary agent:** READ `stages/s2/s2_p2_cross_feature_alignment.md` (full guide)
- **If Secondary agent:** STOP — wait for Primary to complete S2.P2 and notify you
- Use phase transition prompt from `prompts_reference_v2.md`

**After completing S2.P2:**
- S2 is COMPLETE for the epic
- Update EPIC_README.md Feature Tracking table
- Proceed to S3 (Epic-Level Docs, Tests, and Approval)

---

## Exit Criteria

**S2 is complete for THIS feature when ALL of these are true:**

- [ ] **All S2 phases complete (S2.P1 iterations 1-3, S2.P2 alignment):**
  - I1: Discovery Context reviewed, targeted research complete
  - I1: Gate 1 (Research Completeness Audit) PASSED
  - I1: Spec & Checklist drafted with traceability
  - I2: All checklist questions resolved (ONE at a time)
  - I3: Scope validated (split if >35 items)
  - I3: Cross-feature alignment complete
  - I3: Gate 2 (Spec-to-Epic Alignment Check) PASSED
  - I3: Gate 3 — User APPROVED acceptance criteria
  - S2.P2: Pairwise comparison complete (Primary agent)

- [ ] **Files complete:**
  - spec.md: Discovery Context section, requirements with traceability, acceptance criteria (user approved)
  - checklist.md: All questions resolved
  - README.md: S2 marked complete
  - epic/research/{FEATURE_NAME}_DISCOVERY.md: Research findings

- [ ] **Epic updated:**
  - EPIC_README.md Feature Tracking: "[x]" for this feature's S2

- [ ] **All gates passed:**
  - ✅ Gate 1 (S2.P1.I1): Research Completeness Audit
  - ✅ Gate 2 (S2.P1.I3): Spec-to-Epic Alignment Check
  - ✅ Gate 3 (S2.P1.I3): User Approval of acceptance criteria

---

## Next Stage

**If more features remain:**
- Begin S2 for next feature
- Start with S2.P1 (Spec Creation and Refinement)
- Repeat all iterations

**If ALL features complete S2:**
- Transition to S3 (Epic-Level Docs, Tests, and Approval)

📖 **READ:** `stages/s3/s3_epic_planning_approval.md`

---

## Why S2 Was Split

### Problems with Original Monolithic Guide (2,348 lines):

1. **Token inefficiency:** Agents loaded entire guide even when working on single phase
2. **Navigation difficulty:** Hard to find specific phase content in 2,348 line document
3. **Context dilution:** Important phase-specific rules buried in massive guide
4. **Checkpoint confusion:** Unclear when to re-read guide vs continue

### Benefits of Split Guides:

1. **Significant token reduction per phase:**
   - Agents load only the guide for their current phase (S2.P1 or S2.P2)
   - `s2_p1_spec_creation_refinement.md` replaces the original 2,348-line monolithic guide
   - `s2_p2_cross_feature_alignment.md` is a focused, separate guide for the cross-feature phase

2. **Clear phase boundaries:**
   - Natural breakpoints at mandatory gates
   - Each guide has focused critical rules
   - Obvious transition points

3. **Improved navigation:**
   - Agents read only relevant phase content
   - Faster guide comprehension
   - Easier to resume after session compaction

4. **Better mandatory reading protocol:**
   - Clear "read this guide" instruction per phase
   - Phase-specific acknowledgment prompts
   - Reduced guide abandonment

---

## Frequently Asked Questions

**Q: Do I need to read both phase guides?**
A: You read `s2_p1_spec_creation_refinement.md` once and work through all 3 iterations (I1 → I2 → I3). After S2.P1 is done, the Primary agent reads `s2_p2_cross_feature_alignment.md` for S2.P2.

**Q: Can I skip a phase?**
A: No. S2.P1 (all 3 iterations) and S2.P2 (Primary agent) are both mandatory. The structure doesn't change workflow requirements, just organization.

**Q: What if I'm resuming mid-stage?**
A: Check feature README.md Agent Status for current phase, then read the guide for that phase.

**Q: Do the mandatory gates change?**
A: No. Still 3 gates: Gate 1 in S2.P1.I1 (Research Completeness Audit), Gate 2 in S2.P1.I3 (Spec-to-Epic Alignment Check), Gate 3 in S2.P1.I3 (User Approval of acceptance criteria).

**Q: Where does the Spec-to-Epic Alignment Check happen?**
A: In S2.P1.I3 (Refinement & Alignment) — Gate 2 is embedded in I3 of `s2_p1_spec_creation_refinement.md`.

**Q: Can I reference the original guide?**
A: The original monolithic guide has been removed. Use `s2_p1_spec_creation_refinement.md` (all spec work, 3 iterations) and `s2_p2_cross_feature_alignment.md` (cross-feature phase).

---

## Summary

**S2 has two phases:**

1. **stages/s2/s2_p1_spec_creation_refinement.md** — S2.P1: Spec Creation and Refinement (I1 → I2 → I3, embeds Gates 1 & 2, includes Gate 3)
2. **stages/s2/s2_p2_cross_feature_alignment.md** — S2.P2: Cross-Feature Alignment (Primary agent only)

**Workflow:** S2.P1 (3 iterations) → S2.P2 (pairwise comparison) → S3

**Start here:** `stages/s2/s2_p1_spec_creation_refinement.md` (unless resuming mid-stage)

---

*End of stages/s2/s2_feature_deep_dive.md (ROUTER)*
