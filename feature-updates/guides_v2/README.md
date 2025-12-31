# Feature Development Workflow v2 - Guide System Overview

**Version:** 2.0
**Last Updated:** 2025-12-30
**Purpose:** Complete guide system for epic-driven feature development

---

## Quick Start

**Starting a new epic?** → Read `STAGE_1_epic_planning_guide.md`

**Resuming after session compaction?** → Check EPIC_README.md "Agent Status" section, read the guide listed there

**Looking for a specific guide?** → See "Guide Index" section below

---

## What is the v2 Workflow?

The v2 workflow is a **7-stage epic-driven development process** designed to:
- Break large projects into manageable epics
- Ensure thorough planning before coding
- Maintain alignment across multiple features
- Prevent guide abandonment through mandatory prompts
- Enable resumability through explicit status tracking

**Key Philosophy:**
- **Epic-first thinking:** Top-level work unit is an "epic" (collection of features)
- **Systematic validation:** Multiple QC checkpoints prevent issues
- **Continuous alignment:** Specs updated as implementation reveals reality
- **Iterative testing:** Test plan evolves with implementation
- **Mandatory prompts:** Phase transitions require explicit acknowledgment

---

## The 7 Stages

```
STAGE 1: Epic Planning
   ↓
   Create epic folder structure
   Propose feature breakdown (user approves)
   Create initial epic_smoke_test_plan.md

STAGE 2: Feature Deep Dives (Loop per feature)
   ↓
   Flesh out spec.md for each feature
   Interactive question resolution
   Compare to completed features

STAGE 3: Cross-Feature Sanity Check
   ↓
   Systematic pairwise comparison
   Resolve conflicts
   User sign-off on aligned specs

STAGE 4: Epic Testing Strategy
   ↓
   Update epic_smoke_test_plan.md based on specs
   Identify integration points
   Define epic success criteria

STAGE 5: Feature Implementation (Loop per feature)
   ├─ 5a: TODO Creation (24 verification iterations)
   ├─ 5b: Implementation (coding with continuous verification)
   ├─ 5c: Post-Implementation (smoke testing + 3 QC rounds + PR review)
   ├─ 5d: Cross-Feature Alignment (update remaining feature specs)
   └─ 5e: Epic Testing Plan Update (update based on actual implementation)

STAGE 6: Epic-Level Final QC
   ↓
   Execute evolved epic_smoke_test_plan.md
   3 epic-level QC rounds
   Validate against original epic request

STAGE 7: Epic Cleanup
   ↓
   Run unit tests (100% pass)
   User testing (MANDATORY)
   If bugs found → Fix & RESTART Stage 6
   Commit changes
   Move epic to done/ folder
```

---

## Guide Index

**Which guide should I read?**

| When to Use | Guide File | Purpose |
|-------------|------------|---------|
| Starting a new epic | `STAGE_1_epic_planning_guide.md` | Analyze request, propose features, create structure |
| Planning a feature | `STAGE_2_feature_deep_dive_guide.md` | Detailed planning for one feature |
| All features planned | `STAGE_3_cross_feature_sanity_check_guide.md` | Validate alignment, resolve conflicts, get user sign-off |
| Features aligned | `STAGE_4_epic_testing_strategy_guide.md` | Update test plan based on specs |
| Ready to implement (Round 1) | `STAGE_5aa_round1_guide.md` | Iterations 1-7 + 4a: Requirements, dependencies, algorithms |
| Round 1 complete | `STAGE_5ab_round2_guide.md` | Iterations 8-16: Test strategy, edge cases, re-verification |
| Round 2 complete | `STAGE_5ac_round3_guide.md` | Iterations 17-24 + 23a: Phasing, final gates, readiness |
| TODOs complete (24 iterations) | `STAGE_5b_implementation_execution_guide.md` | Implement feature with continuous verification |
| Implementation done (Smoke Testing) | `STAGE_5ca_smoke_testing_guide.md` | Part 1: Import, Part 2: Entry Point, Part 3: E2E (verify DATA VALUES) |
| Smoke testing passed (QC Rounds) | `STAGE_5cb_qc_rounds_guide.md` | Round 1: Basic validation, Round 2: Deep verification, Round 3: Final review |
| QC rounds passed (Final Review) | `STAGE_5cc_final_review_guide.md` | PR review (11 categories), lessons learned, final verification |
| QC passed | `STAGE_5d_post_feature_alignment_guide.md` | Update remaining feature specs based on actual code |
| Alignment updated | `STAGE_5e_post_feature_testing_update_guide.md` | Update epic test plan based on implementation |
| All features done | `STAGE_6_epic_final_qc_guide.md` | Validate entire epic end-to-end |
| Epic QC passed | `STAGE_7_epic_cleanup_guide.md` | User testing, finalize, commit, archive |
| Bug discovered | `STAGE_5_bug_fix_workflow_guide.md` | Handle bugs during epic development |
| Need templates | `templates_v2.md` | File templates for epics, features, bug fixes |
| Starting a stage | `prompts_reference_v2.md` | MANDATORY prompts for phase transitions |

---

## Key Improvements from v1

### 1. Clearer Hierarchy
- **v1:** Confused "feature" and "sub-feature" terminology
- **v2:** Clear hierarchy: Epic → Features → (no sub-levels)

### 2. Epic-First Thinking
- **v1:** Feature-centric (hard to manage multi-feature projects)
- **v2:** Epic-centric (natural grouping, better organization)

### 3. Mandatory Phase Transition Prompts
- **v1:** Agents often skipped reading guides (40% guide abandonment)
- **v2:** MANDATORY prompts prove guide was read, list critical requirements

### 4. Continuous Alignment
- **v1:** Specs written upfront, never revisited
- **v2:** Stage 5d updates specs after each feature implementation

### 5. Iterative Test Planning
- **v1:** Test plan written once, never updated
- **v2:** Test plan evolves: Stage 1 (placeholder) → Stage 4 (based on specs) → Stage 5e (based on implementation) → Stage 6 (execute)

### 6. Epic-Level vs Feature-Level Distinction
- **v1:** Same QC process for features and entire project
- **v2:** Clear distinction between feature-level (Stage 5c) and epic-level (Stage 6) testing

### 7. Bug Fix Integration
- **v1:** Unclear how to handle bugs discovered mid-epic
- **v2:** Dedicated bug fix workflow (Stage 2→5a→5b→5c) with priority handling

### 8. 24 Verification Iterations
- **v1:** Generic TODO creation
- **v2:** Systematic 24-iteration verification catching 40% more issues

---

## File Structure

### Epic Folder Structure
```
feature-updates/
├── {epic_name}.txt                    ← Original user request (stays in root)
├── {epic_name}/                       ← Epic folder (all work here)
│   ├── EPIC_README.md                ← Master tracking, Quick Reference Card, Agent Status
│   ├── epic_smoke_test_plan.md       ← How to test complete epic (evolves through stages)
│   ├── epic_lessons_learned.md       ← Cross-feature insights
│   │
│   ├── feature_01_{name}/            ← Feature 1
│   │   ├── README.md                 ← Feature status, Agent Status
│   │   ├── spec.md                   ← PRIMARY specification
│   │   ├── checklist.md              ← Tracks resolved vs pending decisions
│   │   ├── todo.md                   ← Implementation task list (Stage 5a)
│   │   ├── questions.md              ← Questions for user (Stage 5a)
│   │   ├── implementation_checklist.md ← Continuous verification (Stage 5b)
│   │   ├── code_changes.md           ← Documentation of changes (Stage 5b)
│   │   ├── lessons_learned.md        ← Feature-specific insights
│   │   └── research/                 ← Research documents (if needed)
│   │
│   ├── feature_02_{name}/            ← Feature 2 (same structure)
│   │
│   └── bugfix_{priority}_{name}/     ← Bug fix (if discovered)
│       ├── notes.txt                 ← User-verified issue description
│       ├── spec.md                   ← Fix requirements
│       ├── checklist.md
│       ├── todo.md
│       ├── implementation_checklist.md
│       ├── code_changes.md
│       └── lessons_learned.md
│
├── done/                              ← Completed epics moved here
│   └── {epic_name}/                  ← Complete epic folder (Stage 7)
│
└── guides_v2/                        ← THIS folder (guides for workflow)
    ├── README.md                     ← This file (workflow overview)
    ├── STAGE_1_epic_planning_guide.md
    ├── STAGE_2_feature_deep_dive_guide.md
    ├── ... (all stage guides)
    ├── templates_v2.md               ← File templates
    └── prompts_reference_v2.md       ← Phase transition prompts
```

---

## Getting Started with an Epic

### Step 1: User Creates Initial Request

User creates `feature-updates/{epic_name}.txt` with initial scratchwork:

```
Epic Request: Improve Draft Helper System

Goals:
- Integrate ADP data for market wisdom
- Add matchup-based projections
- Track player performance vs projections

Initial Thoughts:
- Need to fetch ADP data from somewhere
- Matchup data probably needs NFL schedule
- Performance tracking needs historical data

Questions:
- Should ADP be manually updated or auto-fetched?
- How many weeks of history for performance tracking?
```

### Step 2: User Starts Epic Planning

User says: **"Help me develop the improve_draft_helper epic"**

### Step 3: Agent Reads STAGE_1 Guide

Agent MUST use phase transition prompt:

```
I'm reading `STAGE_1_epic_planning_guide.md` to ensure I follow the complete epic planning workflow...

**The guide requires:**
- Phase 1: Analyze epic request and codebase reconnaissance
- Phase 2: Propose feature breakdown to user (user MUST approve)
- Phase 3: Create epic folder structure
- ... (list critical requirements)

**Prerequisites I'm verifying:**
✅ Epic request file exists: `feature-updates/improve_draft_helper.txt`
✅ Epic request contains user's initial notes
✅ Epic scope is clear from request

**I'll now proceed with Phase 1...**
```

### Step 4: Agent Follows Guide Step-by-Step

Agent executes Stage 1 phases:
1. Analyzes request and performs reconnaissance
2. Proposes feature breakdown (user approves: 3 features)
3. Creates epic folder with 3 feature folders
4. Creates initial epic_smoke_test_plan.md
5. Creates EPIC_README.md with Quick Reference Card
6. Creates epic_lessons_learned.md

### Step 5: Continue Through Stages

Agent continues through all 7 stages for the complete epic lifecycle.

---

## Critical Concepts

### Mandatory Reading Protocol

**EVERY TIME an agent starts a stage, they MUST:**
1. Use Read tool to load the ENTIRE guide
2. Use phase transition prompt from `prompts_reference_v2.md`
3. List critical requirements (proves they read the guide)
4. Verify prerequisites
5. Update README Agent Status
6. THEN proceed with the stage

**Why this matters:**
- Prevents guide abandonment (documented 40% failure rate without prompts)
- Ensures agent understands requirements
- Creates accountability
- Enables resumability through status tracking

---

### Agent Status Tracking

**Every README.md (epic and feature) has "Agent Status" section:**

```markdown
## Agent Status

**Last Updated:** 2025-12-30 15:23
**Current Phase:** TODO_CREATION
**Current Step:** Iteration 12/24
**Current Guide:** STAGE_5aa_round1_guide.md
**Guide Last Read:** 2025-12-30 15:20
**Critical Rules from Guide:**
- 24 iterations mandatory, no skipping
- STOP if confidence < Medium
- Update Agent Status after each round
**Progress:** 12/24 iterations complete
**Next Action:** Begin iteration 13 - Dependency Verification
**Blockers:** None
```

**Purpose:**
- Survives session compaction
- Enables resumability
- Shows exact state for future agents
- Lists critical rules for current stage

---

### Quick Reference Card

**Every EPIC_README.md has "Quick Reference Card" at top:**

```markdown
## 🎯 Quick Reference Card (Always Visible)

**Current Stage:** Stage 5a - TODO Creation
**Active Guide:** `guides_v2/STAGE_5aa_round1_guide.md`
**Last Guide Read:** 2025-12-30 15:20

**Stage Workflow:**
Stage 1 → Stage 2 → Stage 3 → Stage 4 → Stage 5 → Stage 6 → Stage 7
  ↓         ↓         ↓         ↓         ↓         ↓         ↓
Epic    Features  Sanity   Testing   Impl     Epic      Done
Plan    Deep Dive  Check   Strategy  (5a-5e)  QC

**You are here:** ➜ Stage 5a

**Critical Rules for Current Stage:**
1. 24 verification iterations mandatory (NO SKIPPING)
2. STOP if confidence < Medium
3. Create questions.md if blockers arise
4. Update Agent Status after each round
5. Algorithm Traceability Matrix required (iterations 4, 11, 19)

**Before Proceeding to Next Step:**
□ Read guide: `guides_v2/STAGE_5aa_round1_guide.md` (start with Round 1)
□ Acknowledge critical requirements
□ Verify prerequisites
□ Update this Quick Reference Card
```

**Purpose:**
- Always visible (top of README)
- Shows current stage and guide
- Lists critical rules for THIS stage
- Reminds agent to read guide
- Provides workflow context

---

### Epic Progress Tracker

**EPIC_README.md includes table tracking ALL features:**

```markdown
## Epic Progress Tracker

| Feature | Stage 1 | Stage 2 | Stage 3 | Stage 4 | Stage 5a | Stage 5b | Stage 5c | Stage 5d | Stage 5e |
|---------|---------|---------|---------|---------|----------|----------|----------|----------|----------|
| feature_01_adp_integration | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| feature_02_matchup_system | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 🔄 | ◻️ | ◻️ |
| feature_03_performance_tracker | ✅ | ✅ | ✅ | ✅ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ |

**Legend:** ✅ = Complete | 🔄 = In Progress | ◻️ = Not Started
```

**Purpose:**
- See entire epic status at a glance
- Identify which features are complete
- Track progress across all features
- Helps decide next actions

---

### Test Plan Evolution

**epic_smoke_test_plan.md evolves through stages:**

```
Stage 1 (Initial):
- Placeholder scenarios
- High-level categories
- Based on assumptions (NO code yet)

Stage 4 (After Deep Dives):
- Updated with integration points from Stage 3
- Specific scenarios based on specs
- Still based on PLANS (not implementation)

Stage 5e (After Each Feature):
- Updated with ACTUAL implementation details
- New integration scenarios discovered
- Reflects REALITY (not assumptions)

Stage 6 (Execution):
- Execute EVOLVED test plan
- Tests reflect actual epic as built
- High quality because based on reality
```

**Purpose:**
- Test plan stays current
- Reflects actual implementation
- Stage 6 tests are realistic and effective

---

## Common Workflows

### Workflow 1: Starting a New Epic

1. User creates `{epic_name}.txt` with initial notes
2. User says: "Help me develop {epic_name}"
3. Agent reads `STAGE_1_epic_planning_guide.md`
4. Agent uses phase transition prompt
5. Agent analyzes request + reconnaissance
6. Agent proposes feature breakdown → User approves
7. Agent creates epic folder structure
8. Agent creates initial epic files (README, test plan, lessons learned)
9. **Stage 1 complete**

---

### Workflow 2: Implementing a Feature

1. Agent completes Stages 1-4 (epic planning, feature deep dives, sanity check, testing strategy)
2. User says: "Implement feature_01"
3. Agent reads `STAGE_5aa_round1_guide.md`
4. Agent executes 24 verification iterations
5. Agent creates `todo.md` and `questions.md`
6. **Stage 5a complete**
7. Agent reads `STAGE_5b_implementation_execution_guide.md`
8. Agent implements feature with continuous verification
9. **Stage 5b complete**
10. Agent reads `STAGE_5ca_smoke_testing_guide.md`
11. Agent runs smoke testing (3 parts - MANDATORY GATE)
12. Agent reads `STAGE_5cb_qc_rounds_guide.md`
13. Agent runs 3 QC rounds (restart protocol if issues found)
14. Agent reads `STAGE_5cc_final_review_guide.md`
15. Agent runs PR review (11 categories) and captures lessons learned
16. **Stage 5c complete**
17. Agent reads `STAGE_5d_post_feature_alignment_guide.md`
18. Agent updates remaining feature specs
19. **Stage 5d complete**
20. Agent reads `STAGE_5e_post_feature_testing_update_guide.md`
21. Agent updates epic_smoke_test_plan.md
22. **Stage 5e complete** → Feature done!

---

### Workflow 3: Handling a Bug

1. Agent discovers bug during Stage 5c (QC)
2. Agent presents bug to user for approval
3. User approves bug fix creation
4. Agent reads `STAGE_5_bug_fix_workflow_guide.md`
5. Agent creates `bugfix_{priority}_{name}/` folder
6. Agent creates `notes.txt` → User verifies
7. Agent updates EPIC_README.md (pauses current work)
8. Agent runs bug fix through: Stage 2 → 5a → 5b → 5c
9. Bug fix complete
10. Agent returns to paused work (resumes Stage 5c where it left off)

---

### Workflow 4: Resuming After Session Compaction

1. Session compacts during Stage 5a (iteration 12/24)
2. New agent spawned
3. Agent reads EPIC_README.md "Agent Status"
4. Agent sees: Current Guide = `STAGE_5ab_round2_guide.md`, Current Step = "Iteration 12/24"
5. Agent reads `STAGE_5ab_round2_guide.md` (full guide, Round 2)
6. Agent uses "Resuming After Compaction" prompt
7. Agent acknowledges requirements for Stage 5a
8. Agent continues from Iteration 13 (picks up where previous agent left off)

---

## FAQ

### Q: Do I need to read the guide every time I start a stage?

**A: YES.** This is MANDATORY.

Even if you've read it before, you MUST re-read when:
- Starting a new stage
- Resuming after session compaction
- Creating a bug fix

**Why:** Context window limits mean you don't have the guide in memory. Re-reading ensures you don't miss critical requirements.

---

### Q: Can I skip the phase transition prompts?

**A: NO.** Phase transition prompts are MANDATORY.

Without prompts:
- 40% guide abandonment rate (documented)
- No proof guide was read
- No accountability for requirements
- Breaks resumability

**Always use prompts from `prompts_reference_v2.md`.**

---

### Q: What if I'm stuck or encountering errors?

**A: Use the problem situation prompts.**

See `prompts_reference_v2.md` → "Problem Situation Prompts" section for:
- When tests are failing
- When stuck or blocked
- When confidence < Medium

**Never guess. Always ask for help when blocked.**

---

### Q: Do I really need 24 iterations for TODO creation?

**A: YES.** All 24 iterations are MANDATORY.

**Data shows:**
- Shortcuts cause 40% QC failure rate
- Each iteration catches different issue types
- Complexity hides in details
- Iterations 4, 11, 19 (Traceability Matrix) catch 30% of issues
- Iteration 21 (Mock Audit) catches another 15%
- Iteration 23a (Pre-Implementation Audit) catches 20%

**NO SKIPPING ITERATIONS.**

---

### Q: What's the difference between epic-level and feature-level testing?

**Feature-Level Testing (Stage 5c):**
- Tests ONE feature in ISOLATION
- Verifies feature meets its spec
- Smoke testing for this feature only
- QC rounds for this feature only

**Epic-Level Testing (Stage 6):**
- Tests ALL features TOGETHER
- Verifies epic as cohesive whole
- Cross-feature integration tests
- Epic-wide workflows
- Validates against original epic request

**Both are required. Different focus areas.**

---

### Q: When should I create a bug fix vs just fixing it?

**Create a bug fix when:**
- Bug discovered during QC (Stage 5c or 6)
- Issue affects multiple files
- Root cause requires investigation
- User reports an issue
- Fix requires >30 minutes

**Just fix it directly when:**
- Typo or obvious mistake
- Single-line fix
- No investigation needed
- <10 minutes to fix

**When in doubt, create a bug fix.** Better to follow the process.

---

### Q: What happens if a feature grows too large during Stage 2?

**If feature grows >30% in complexity during deep dive:**
1. STOP the deep dive
2. Propose splitting into 2+ features
3. Get user approval
4. Create new feature folders
5. Redistribute scope
6. Update epic EPIC_README.md

**This is called "Dynamic Scope Adjustment" and is encouraged.**

---

## Troubleshooting

### Problem: "I don't know which guide to read"

**Solution:**
1. Check EPIC_README.md "Agent Status" section
2. Look at "Current Guide" field
3. Read that guide

**If Agent Status not updated:**
1. Check Epic Progress Tracker (see which stage features are at)
2. Determine current stage from tracker
3. Read corresponding guide from Guide Index above

---

### Problem: "Tests are failing and I can't proceed"

**Solution:**
1. Do NOT proceed with failing tests
2. Use "When Tests Are Failing" prompt from `prompts_reference_v2.md`
3. Fix ALL test failures
4. Re-run tests until exit code = 0 (100% pass)
5. THEN proceed

**100% test pass rate is MANDATORY before:**
- Committing (Stage 7)
- Moving to next phase (Stage 5b → 5c)
- Completing QC (Stage 5c or 6)

---

### Problem: "User hasn't responded to my question"

**Solution:**
1. Document question in `questions.md`
2. Update README Agent Status with "Blockers: Waiting for user answer to question X"
3. STOP work on this feature
4. If other features available, work on those
5. If no other work, wait for user response

**Do NOT guess or assume. Wait for clarification.**

---

### Problem: "Epic folder structure doesn't match templates"

**Solution:**
1. Read `templates_v2.md` for correct structure
2. Create missing files/folders
3. Update EPIC_README.md with correct file list
4. Verify structure matches templates before proceeding

**Every epic MUST have:**
- EPIC_README.md
- epic_smoke_test_plan.md
- epic_lessons_learned.md
- At least one feature folder

---

## Summary

**The v2 workflow provides:**
- Clear 7-stage process for epic development
- Mandatory reading and prompts to prevent guide abandonment
- Explicit status tracking for resumability
- Continuous alignment as implementation reveals reality
- Iterative test planning that evolves with implementation
- Distinction between feature-level and epic-level validation

**Key Files:**
- **This README:** Workflow overview, guide index, getting started
- **Stage Guides (12):** Detailed workflows for each stage
- **templates_v2.md:** File templates for all epic/feature files
- **prompts_reference_v2.md:** MANDATORY prompts for phase transitions

**Remember:**
- Always READ the guide before starting a stage
- Always USE the phase transition prompt
- Always VERIFY prerequisites
- Always UPDATE Agent Status
- Never SKIP iterations or steps
- Never GUESS when blocked - ask for help

**For detailed workflows, read the stage-specific guides listed in the Guide Index above.**

---

**Welcome to the v2 workflow. Let's build great features systematically!**
