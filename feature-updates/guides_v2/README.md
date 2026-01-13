# Feature Development Workflow v2 - Guide System Overview

**Version:** 2.0
**Last Updated:** 2025-12-30
**Purpose:** Complete guide system for epic-driven feature development

---

## Quick Start

**Starting a new epic?** → Read `stages/s1/s1_epic_planning.md`

**Resuming after session compaction?** → Check EPIC_README.md "Agent Status" section, read the guide listed there

**Looking for a specific guide?** → See "Guide Index" section below

---

## What is the v2 Workflow?

The v2 workflow is a **10-stage epic-driven development process** designed to:
- Break large projects into manageable epics
- Ensure thorough planning before coding
- Maintain alignment across multiple features
- Prevent guide abandonment through mandatory prompts
- Enable resumability through explicit status tracking

**Key Philosophy:**
- **Epic-first thinking:** Top-level work unit is an "epic" (collection of features)
- **Systematic validation:** Multiple QC checkpoints prevent issues
- **Continuous alignment:** Specs updated as implementation reveals reality
- **Continuous testing:** Test plan evolves with implementation
- **Mandatory prompts:** Phase transitions require explicit acknowledgment

---

## The 10 Stages

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

STAGES 5-8: Feature Loop (Repeat for each feature)
   ↓
STAGE 5: Implementation Planning
   ├─ 28 verification iterations across 3 rounds
   ├─ Gate 4a: TODO Specification Audit (Round 1)
   ├─ Gate 7a: Backward Compatibility Check (Round 1)
   ├─ Gate 23a: Pre-Implementation Spec Audit (Round 3)
   ├─ Gate 24: GO/NO-GO Decision (Round 3)
   └─ Gate 25: Spec Validation Check (Round 3)
   ↓
STAGE 6: Implementation Execution
   ├─ Create implementation_checklist.md
   ├─ Implement from implementation_plan.md
   ├─ Continuous verification and mini-QC checkpoints
   └─ 100% test pass required
   ↓
STAGE 7: Implementation Testing & Review
   ├─ S7.P1: Smoke Testing (3 parts - MANDATORY GATE)
   ├─ S7.P2: QC Rounds (3 rounds with restart protocol)
   └─ S7.P3: Final Review (PR review, lessons learned)
   ↓
STAGE 8: Post-Feature Alignment
   ├─ S8.P1: Cross-Feature Spec Alignment (update remaining features)
   ├─ S8.P2: Epic Testing Plan Reassessment (update test plan)
   └─ Loop back to S5 for next feature OR proceed to S9
   ↓
STAGE 9: Epic-Level Final QC
   ├─ S9.P1: Epic Smoke Testing
   ├─ S9.P2: Epic QC Rounds (3 rounds)
   ├─ S9.P3: User Testing (MANDATORY - must report "no bugs found")
   └─ S9.P4: Epic Final Review
   ↓
STAGE 10: Epic Cleanup
   ├─ Run unit tests (100% pass required)
   ├─ S10.P1: Guide Updates (MANDATORY)
   │   └─ Analyze lessons → Create proposals (P0-P3) → User approves → Apply
   ├─ Commit epic changes
   ├─ Create PR
   └─ Move epic to done/ folder
```

**Visual Diagrams:** See `diagrams/workflow_diagrams.md` for ASCII art diagrams of complete workflow, S5 detail, and debugging protocol integration.

---

## Guide Index

**Which guide should I read?**

| When to Use | Guide File | Purpose |
|-------------|------------|---------|
| Starting a new epic | `stages/s1/s1_epic_planning.md` | Analyze request, propose features, create structure |
| Planning a feature (start) | `stages/s2/s2_feature_deep_dive.md` | Router: Links to S2.P1, S2.P2, S2.P3 guides |
| S2.P1 (Research) | `stages/s2/s2_p1_research.md` | Epic intent extraction, targeted research, audit |
| S2.P2 (Specification) | `stages/s2/s2_p2_specification.md` | Spec with traceability, alignment check |
| S2.P3 (Refinement) | `stages/s2/s2_p3_refinement.md` | Questions, scope, alignment, user approval |
| All features planned | `stages/s3/s3_cross_feature_sanity_check.md` | Validate alignment, resolve conflicts, get user sign-off |
| Features aligned | `stages/s4/s4_epic_testing_strategy.md` | Update test plan based on specs |
| Ready to implement (Round 1) | `stages/s5/s5_p1_planning_round1.md` | Iterations 1-7 + 4a: Requirements, dependencies, algorithms |
| Round 1 complete | `stages/s5/s5_p2_planning_round2.md` | Iterations 8-16: Test strategy, edge cases, re-verification |
| Round 2 complete | `stages/s5/s5_p3_planning_round3.md` | Router: Links to Part 1/Part 2a/Part 2b sub-stages |
| Round 3 preparation phase | `stages/s5/s5_p3_planning_round3.md` | Iterations 17-22: Phasing, rollback, algorithm (final), performance, mock audit |
| Round 3 gates phase (Part 2a) | `stages/s5/5.1.3.2_round3_part2a.md` | Iterations 23, 23a: Integration Gap + Pre-Impl Spec Audit |
| Round 3 gates phase (Part 2b) | `stages/s5/5.1.3.3_round3_part2b.md` | Iterations 25, 24: Spec Validation + GO/NO-GO |
| Implementation planning complete (28 iterations) | `stages/s6/s6_execution.md` | Implement feature with continuous verification |
| Implementation done (Smoke Testing) | `stages/s7/s7_p1_smoke_testing.md` | Part 1: Import, Part 2: Entry Point, Part 3: E2E (verify DATA VALUES) |
| Smoke testing passed (QC Rounds) | `stages/s7/s7_p2_qc_rounds.md` | Round 1: Basic validation, Round 2: Deep verification, Round 3: Final review |
| QC rounds passed (Final Review) | `stages/s7/s7_p3_final_review.md` | PR review (11 categories), lessons learned, final verification |
| QC passed | `stages/s8/s8_p1_cross_feature_alignment.md` | Update remaining feature specs based on actual code |
| Alignment updated | `stages/s8/s8_p2_epic_testing_update.md` | Update epic test plan based on implementation |
| All features done (Router) | `stages/s9/s9_epic_final_qc.md` | Router: Links to epic smoke/qc/review sub-stages |
| All features done (Smoke) | `stages/s9/s9_p1_epic_smoke_testing.md` | Validate entire epic end-to-end (start with smoke testing) |
| Epic smoke passed (QC) | `stages/s9/s9_p2_epic_qc_rounds.md` | 3 rounds of epic-level QC |
| Epic QC passed (Final Review) | `stages/s9/s9_p4_epic_final_review.md` | Final epic validation before cleanup |
| Epic review passed | `stages/s10/s10_epic_cleanup.md` | User testing, finalize, commit, archive |
| Documentation verified (S10 Step 3) | `stages/s10/s10_p1_guide_update_workflow.md` | Apply lessons learned to guides (P0-P3 prioritization) |
| Guide updates applied | `templates/guide_update_proposal_template.md` | Template for presenting guide changes to user |
| Missed requirement (known solution) | `missed_requirement/missed_requirement_protocol.md` | Handle missing features during epic development |
| Issues during QC/Smoke testing | `debugging/debugging_protocol.md` | Integrated debugging protocol with loop-back to testing |
| Need templates | `templates/TEMPLATES_INDEX.md` | File templates for epics, features, missed requirements, debug sessions |
| Starting a stage | `prompts_reference_v2.md` | MANDATORY prompts for phase transitions |
| Need term definition | `reference/glossary.md` | Complete glossary of workflow terms (alphabetical index) |
| Avoiding mistakes | `reference/common_mistakes.md` | Summary of anti-patterns across all stages |
| Creating/updating guides | `reference/naming_conventions.md` | Hierarchical notation rules, file naming, header formatting |

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
- **v2:** S8.P1 updates specs after each feature implementation

### 5. Continuous Test Planning
- **v1:** Test plan written once, never updated
- **v2:** Test plan evolves: S1 (placeholder) → S4 (based on specs) → S8.P2 (based on implementation) → S9 (execute)

### 6. Epic-Level vs Feature-Level Distinction
- **v1:** Same QC process for features and entire project
- **v2:** Clear distinction between feature-level (S7) and epic-level (S9) testing

### 7. Debugging Protocol Integration
Integrated debugging protocol with QC/Smoke testing, loop-back mechanism, feature vs epic separation

### 8. 28 Verification Iterations
Systematic 28-iteration planning process creating implementation_plan.md (~400 lines) + implementation_checklist.md (~50 lines)

---

## File Structure

### 🔢 KAI Numbering System

**CRITICAL:** All epic folders MUST include KAI number for unique identification.

**Format:** `feature-updates/KAI-{N}-{epic_name}/`

**Examples:**
- `feature-updates/KAI-1-improve_draft_helper/`
- `feature-updates/KAI-2-add_player_validation/`
- `feature-updates/KAI-3-integrate_new_data_source/`

**Why KAI numbers:**
- Ensures unique folder names (prevents conflicts)
- Matches git branch naming (`epic/KAI-1`)
- Enables quick epic identification
- Tracked in `feature-updates/EPIC_TRACKER.md`

**When assigned:** S1 Step 1.0c (before creating epic folder)

**Original Request File:** `feature-updates/{epic_name}.txt` (no KAI number - stays in root for reference)

---

### Epic Folder Structure
```
feature-updates/
├── {epic_name}.txt                        ← Original user request (stays in root)
├── KAI-{N}-{epic_name}/                   ← Epic folder (all work here, includes KAI number)
│   ├── EPIC_README.md                     ← Master tracking, Quick Reference Card, Agent Status
│   ├── epic_smoke_test_plan.md       ← How to test complete epic (evolves through stages)
│   ├── epic_lessons_learned.md       ← Cross-feature insights
│   │
│   ├── feature_01_{name}/            ← Feature 1
│   │   ├── README.md                 ← Feature status, Agent Status
│   │   ├── spec.md                   ← PRIMARY specification
│   │   ├── checklist.md              ← Tracks resolved vs pending decisions
│   │   ├── implementation_plan.md    ← Implementation build guide (~400 lines, S5, user-approved)
│   │   ├── questions.md              ← Questions for user (S5)
│   │   ├── implementation_checklist.md ← Progress tracking (~50 lines, S6)
│   │   ├── code_changes.md           ← Documentation of changes (S6)
│   │   ├── lessons_learned.md        ← Feature-specific insights
│   │   ├── research/                 ← Research documents (if needed)
│   │   └── debugging/                ← Created when issues found in QC/Smoke testing
│   │       ├── ISSUES_CHECKLIST.md   ← Master checklist of all issues
│   │       ├── issue_01_{name}.md    ← Investigation history per issue
│   │       ├── issue_02_{name}.md
│   │       ├── investigation_rounds.md ← Meta-tracker for rounds
│   │       ├── code_changes.md       ← All fixes for this feature
│   │       └── diagnostic_logs/      ← Log files from investigation
│   │
│   ├── feature_02_{name}/            ← Feature 2 (same structure)
│   │
│   ├── debugging/                    ← Epic-level debugging (for S9/7 issues)
│   │   ├── ISSUES_CHECKLIST.md       ← Epic-level issue tracking
│   │   ├── issue_01_{name}.md
│   │   ├── investigation_rounds.md
│   │   ├── code_changes.md
│   │   └── diagnostic_logs/
│   │
│
├── done/                              ← Completed epics moved here
│   └── KAI-{N}-{epic_name}/          ← Complete epic folder (S10, includes KAI number)
│
└── guides_v2/                        ← THIS folder (guides for workflow)
    ├── README.md                     ← This file (workflow overview)
    ├── prompts_reference_v2.md       ← Prompts router (MANDATORY)
    ├── EPIC_WORKFLOW_USAGE.md        ← Comprehensive usage guide
    │
    ├── prompts/                      ← Phase transition prompts (split by stage)
    │   ├── stage_1_prompts.md
    │   ├── stage_2_prompts.md
    │   ├── stage_3_prompts.md
    │   ├── stage_4_prompts.md
    │   ├── stage_5_prompts.md
    │   ├── stage_6_prompts.md
    │   ├── stage_7_prompts.md
    │   ├── special_workflows_prompts.md
    │   └── problem_situations_prompts.md
    │
    ├── debugging/                    ← Debugging protocol (cross-stage)
    │   ├── debugging_protocol.md     ← Router (phases 1-5)
    │   ├── discovery.md              ← Phase 1: Issue discovery & checklist
    │   ├── investigation.md          ← Phase 2: Investigation rounds
    │   ├── resolution.md             ← Phase 3 & 4: Solution & user verification
    │   └── loop_back.md              ← Phase 5: Loop back to testing
    │
    ├── missed_requirement/           ← Missed requirement protocol (cross-stage)
    │   ├── missed_requirement_protocol.md  ← Router (overview & decision tree)
    │   ├── discovery.md              ← Phase 1: Discovery & user decision
    │   ├── planning.md               ← Phase 2: S2 deep dive
    │   ├── realignment.md            ← Phase 3 & 4: S3/4 alignment
    │   └── stage_6_7_special.md      ← Special case: Discovery during epic testing
    │
    ├── stages/                       ← Core workflow guides
    │   ├── stage_1/
    │   │   └── s1_epic_planning.md
    │   ├── stage_2/
    │   │   ├── s2_feature_deep_dive.md          ← Router (links to S2.P1/2.2/2.3)
    │   │   ├── s2_p1_research.md           ← S2.P1 (Research)
    │   │   ├── s2_p2_specification.md      ← S2.P2 (Specification)
    │   │   └── s2_p3_refinement.md         ← S2.P3 (Refinement)
    │   ├── stage_3/
    │   │   └── s3_cross_feature_sanity_check.md
    │   ├── stage_4/
    │   │   └── s4_epic_testing_strategy.md
    │   ├── stage_5/
    │   │   ├── s5_p1_planning_round1.md         ← Implementation planning Round 1
    │   │   ├── s5_p2_planning_round2.md         ← Implementation planning Round 2
    │   │   ├── s5_p3_planning_round3.md         ← Round 3 router (links to 5.1.3.2/5.1.3.3)
    │   │   ├── 5.1.3.2_round3_part2a.md     ← Round 3 Part 2a (Gates 1-2)
    │   │   ├── 5.1.3.3_round3_part2b.md     ← Round 3 Part 2b (Gate 3)
    │   │   ├── s5_p4_execution.md
    │   │   ├── phase_5.3_post_implementation.md  ← Post-impl router
    │   │   ├── s5_p5_smoke_testing.md      ← Post-impl smoke testing
    │   │   ├── s5_p6_qc_rounds.md          ← Post-impl QC rounds
    │   │   ├── s5_p7_final_review.md       ← Post-impl final review
    │   │   ├── s5_p8_cross_feature_alignment.md
    │   │   └── s5_p9_epic_testing_update.md
    │   ├── stage_6/
    │   │   ├── s6_epic_final_qc.md                  ← Router (links to smoke/qc/review)
    │   │   ├── s6_p1_epic_smoke_testing.md   ← Epic smoke testing
    │   │   ├── s6_p2_epic_qc_rounds.md       ← Epic QC rounds
    │   │   ├── s6_p3_user_testing.md         ← User testing
    │   │   └── s6_p4_epic_final_review.md    ← Epic final review
    │   └── stage_7/
    │       └── s7_epic_cleanup.md
    │
    ├── reference/                    ← Reference materials
    │   ├── mandatory_gates.md
    │   ├── stage_2_reference_card.md
    │   ├── stage_5_reference_card.md
    │   ├── spec_validation.md
    │   ├── hands_on_data_inspection.md
    │   └── stage_7/
    │       ├── commit_message_examples.md
    │       ├── epic_completion_template.md
    │       └── lessons_learned_examples.md
    │
    ├── templates/                    ← File templates
    │   └── TEMPLATES_INDEX.md
    │
    └── _internal/                    ← Internal tracking docs
        ├── guide_optimization_phase2_checklist.md
        ├── priority_4_reference_cards_completion.md
        ├── stage_5ac_split_completion.md
        └── stage_5ac_split_reference_updates.md
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
I'm reading `stages/s1/s1_epic_planning.md` to ensure I follow the complete epic planning workflow...

**The guide requires:**
- Step 1: Analyze epic request and codebase reconnaissance
- Step 2: Propose feature breakdown to user (user MUST approve)
- Step 3: Create epic folder structure
- ... (list critical requirements)

**Prerequisites I'm verifying:**
✅ Epic request file exists: `feature-updates/improve_draft_helper.txt`
✅ Epic request contains user's initial notes
✅ Epic scope is clear from request

**I'll now proceed with Phase 1...**
```

### Step 4: Agent Follows Guide Step-by-Step

Agent executes S1 phases:
1. Analyzes request and performs reconnaissance
2. Proposes feature breakdown (user approves: 3 features)
3. Creates epic folder with 3 feature folders
4. Creates initial epic_smoke_test_plan.md
5. Creates EPIC_README.md with Quick Reference Card
6. Creates epic_lessons_learned.md

### Step 5: Continue Through Stages

Agent continues through all 10 stages for the complete epic lifecycle.

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
**Current Phase:** IMPLEMENTATION_PLANNING
**Current Step:** Iteration 12/24
**Current Guide:** stages/s5/s5_p1_planning_round1.md
**Guide Last Read:** 2025-12-30 15:20
**Critical Rules from Guide:**
- 28 iterations mandatory, no skipping
- STOP if confidence < Medium
- Update Agent Status after each round
**Progress:** 12/28 iterations complete
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

**Current Stage:** S5 - Implementation Planning
**Active Guide:** `guides_v2/stages/s5/s5_p1_planning_round1.md`
**Last Guide Read:** 2025-12-30 15:20

**Stage Workflow:**
S1 → S2 → S3 → S4 → S5 → S9 → S10
  ↓         ↓         ↓         ↓         ↓         ↓         ↓
Epic    Features  Sanity   Testing   Impl     Epic      Done
Plan    Deep Dive  Check   Strategy  (5a-5e)  QC

**You are here:** ➜ S5

**Critical Rules for Current Stage:**
1. 24 verification iterations mandatory (NO SKIPPING)
2. STOP if confidence < Medium
3. Create questions.md if blockers arise
4. Update Agent Status after each round
5. Algorithm Traceability Matrix required (iterations 4, 11, 19)

**Before Proceeding to Next Step:**
□ Read guide: `guides_v2/stages/s5/s5_p1_planning_round1.md` (start with Round 1)
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

| Feature | S1 | S2 | S3 | S4 | S5 | S6 | S7 | S8.P1 | S8.P2 |
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
S1 (Initial):
- Placeholder scenarios
- High-level categories
- Based on assumptions (NO code yet)

S4 (After Deep Dives):
- Updated with integration points from S3
- Specific scenarios based on specs
- Still based on PLANS (not implementation)

S8.P2 (After Each Feature):
- Updated with ACTUAL implementation details
- New integration scenarios discovered
- Reflects REALITY (not assumptions)

S9 (Execution):
- Execute EVOLVED test plan
- Tests reflect actual epic as built
- High quality because based on reality
```

**Purpose:**
- Test plan stays current
- Reflects actual implementation
- S9 tests are realistic and effective

---

## Common Workflows

### Workflow 1: Starting a New Epic

1. User creates `{epic_name}.txt` with initial notes
2. User says: "Help me develop {epic_name}"
3. Agent reads `stages/s1/s1_epic_planning.md`
4. Agent uses phase transition prompt
5. Agent analyzes request + reconnaissance
6. Agent proposes feature breakdown → User approves
7. Agent creates epic folder structure
8. Agent creates initial epic files (README, test plan, lessons learned)
9. **S1 complete**

---

### Workflow 2: Implementing a Feature

1. Agent completes Stages 1-4 (epic planning, feature deep dives, sanity check, testing strategy)
2. User says: "Implement feature_01"
3. Agent reads `stages/s5/s5_p1_planning_round1.md`
4. Agent executes 24 verification iterations across 3 rounds
5. Agent creates `implementation_plan.md` (~400 lines) and `questions.md`
6. **User approves implementation_plan.md** (MANDATORY CHECKPOINT)
7. **S5 complete**
8. Agent reads `stages/s6/s6_execution.md`
9. Agent creates `implementation_checklist.md` (~50 lines) from implementation_plan.md tasks
10. Agent implements feature using implementation_plan.md as PRIMARY reference (spec.md provides context)
11. **S6 complete**
12. Agent reads `stages/s7/s7_p1_smoke_testing.md`
13. Agent runs smoke testing (3 parts - MANDATORY GATE)
14. Agent reads `stages/s7/s7_p2_qc_rounds.md`
15. Agent runs 3 QC rounds (restart protocol if issues found)
16. Agent reads `stages/s7/s7_p3_final_review.md`
17. Agent runs PR review (11 categories) and captures lessons learned
18. **S7 complete**
19. Agent reads `stages/s8/s8_p1_cross_feature_alignment.md`
20. Agent updates remaining feature specs
21. **S8.P1 complete**
22. Agent reads `stages/s8/s8_p2_epic_testing_update.md`
23. Agent updates epic_smoke_test_plan.md
24. **S8.P2 complete** → Feature done!

---

### Workflow 3a: Handling a Missed Requirement (Known Solution - Can Happen Anytime)

**Can be discovered during:** Implementation (5a/5b/5c), QA, Debugging, Epic Testing (6a/6b/6c), User Testing (7)

1. Agent discovers missing scope at ANY point after first S5 starts
2. Agent presents TWO options to user:
   - Option 1: Create new feature_{XX}_{name}/
   - Option 2: Update unstarted feature to include requirement
3. User decides which approach + priority (high/medium/low) + sequence position (if new)
4. Agent reads `missed_requirement/missed_requirement_protocol.md`
5. Agent pauses current work, updates EPIC_README with paused status
6. Agent returns to planning stages:
   - **S2:** Flesh out new/updated feature spec (full deep dive)
   - **S3:** Re-align ALL features (cross-feature sanity check)
   - **S4:** Update epic_smoke_test_plan.md
7. Planning complete → Agent resumes paused work
8. New/updated feature waits its turn in implementation sequence
9. When its turn comes: Implement through full S5 (5a → 5b → 5c → 5d → 5e)
10. **SPECIAL CASE - If discovered during S9/7:**
    - Complete ALL remaining features first
    - Implement new/updated feature
    - **RESTART epic testing from S9.P1 Step 1** (loop-back mechanism)

---

### Workflow 3b: Debugging Issues During QC/Smoke Testing (Integrated Loop-Back)

**During Feature-Level Testing (S10.P1/S10.P2):**

1. Agent runs Smoke Testing Part 3 (E2E) → Issues found
2. Agent creates `feature_XX_{name}/debugging/` folder
3. Agent creates ISSUES_CHECKLIST.md, adds all discovered issues
4. Agent updates feature README.md Agent Status (entering debugging)
5. Agent reads `debugging/debugging_protocol.md`
6. **Step 1:** Issue Discovery - Update checklist with issue details
7. **Step 2:** Investigation (PER ISSUE) - Run investigation rounds:
   - Round 1: Code Tracing (identify 2-3 suspicious areas)
   - Round 2: Hypothesis Formation (max 3 testable hypotheses)
   - Round 3: Diagnostic Testing (confirm root cause with evidence)
   - Repeat rounds if needed (max 5 rounds per issue)
8. **Step 3:** Solution Design & Implementation (per issue, with tests)
9. **Step 4:** User Verification (MANDATORY - user confirms each issue fixed)
10. After ALL issues resolved → **Step 5: Loop Back to Smoke Testing Part 1**
11. Agent re-runs ALL smoke tests (Part 1, 2, 3) from beginning
12. If NEW issues found → Back to Phase 1 (add to checklist)
13. If ZERO issues → Proceed to S7.P2

**During Epic-Level Testing (S9.P1/6b):**

1. Agent runs Epic Smoke Testing → Issues found
2. Agent creates `{epic_name}/debugging/` folder (EPIC-LEVEL, not feature)
3. Follow same 5-phase process as above
4. After ALL issues resolved → **Loop back to S9.P1 Step 1 (Epic Smoke Testing)**
5. If user finds bugs during S10 testing → Add to epic debugging/ISSUES_CHECKLIST.md → Loop back to S9.P1

**Key Differences from v1:**
- Debugging folder WITHIN features/epics (not separate)
- ALWAYS loop back to START of testing (not mid-testing)
- Feature vs epic separation for issue tracking
- User testing bugs loop to S9.P1 (NOT S10)

---

### Workflow 4: Resuming After Session Compaction

1. Session compacts during S5 (iteration 12/24)
2. New agent spawned
3. Agent reads EPIC_README.md "Agent Status"
4. Agent sees: Current Guide = `stages/s5/s5_p2_planning_round2.md`, Current Step = "Iteration 12/24"
5. Agent reads `stages/s5/s5_p2_planning_round2.md` (full guide, Round 2)
6. Agent uses "Resuming After Compaction" prompt
7. Agent acknowledges requirements for S5
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

### Q: Do I really need 28 iterations for implementation planning?

**A: YES.** All 28 iterations are MANDATORY.

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

**Feature-Level Testing (S7):**
- Tests ONE feature in ISOLATION
- Verifies feature meets its spec
- Smoke testing for this feature only
- QC rounds for this feature only

**Epic-Level Testing (S9):**
- Tests ALL features TOGETHER
- Verifies epic as cohesive whole
- Cross-feature integration tests
- Epic-wide workflows
- Validates against original epic request

**Both are required. Different focus areas.**

---

### Q: When should I enter debugging protocol vs just fixing it?

**Enter debugging protocol when:**
- Issues discovered during Smoke Testing (S10.P1/6a) or QC Rounds (S10.P2/6b)
- Root cause is UNKNOWN (requires investigation)
- Issue affects multiple files or components
- Multiple related issues discovered
- User reports bugs during S10 testing

**Just fix it directly when:**
- Typo or obvious mistake during implementation (S6)
- Single-line fix with known cause
- No investigation needed
- <10 minutes to fix
- Issue found during code review (before testing stages)

**Debugging protocol = INTEGRATED with testing stages, not separate workflow**

---

### Q: What happens if a feature grows too large during S2?

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
- Committing (S10)
- Moving to next phase (S6 → S7)
- Completing QC (S7 or S9)

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
1. Read `templates/TEMPLATES_INDEX.md` for correct structure
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
- Clear 10-stage process for epic development
- Mandatory reading and prompts to prevent guide abandonment
- Explicit status tracking for resumability
- Continuous alignment as implementation reveals reality
- Continuous test planning that evolves with implementation
- Distinction between feature-level and epic-level validation

**Key Files:**
- **This README:** Workflow overview, guide index, getting started
- **Stage Guides (12):** Detailed workflows for each stage
- **templates/TEMPLATES_INDEX.md:** File templates for all epic/feature files
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
