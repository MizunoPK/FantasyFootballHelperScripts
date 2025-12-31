# Guides V2 - Overarching Plan

## Purpose

This plan outlines the complete restructuring of the feature development workflow based on lessons learned from v1 guides. The v2 guides will provide a clearer, more manageable process that better aligns with real-world development needs.

---

## Recent Updates

**Stage 5 Sub-stages Added (Latest Change):**
- **Stage 5d** (NEW): **Cross-Feature Spec Alignment Check (Post-Implementation)**
  - After EACH feature completes, review ALL remaining (unimplemented) feature specs
  - Compare specs against **actual implementation** (not just the plan)
  - Update specs based on real insights from implementation
  - Prevents spec drift as implementation reveals reality
  - Catches cascading changes before implementing dependent features

- **Stage 5e** (NEW): **Epic Testing Plan Reassessment**
  - After EACH feature completes, reassess epic_smoke_test_plan.md
  - Update test scenarios based on **actual implementation**
  - Add newly discovered integration points
  - Keep testing plan current throughout implementation (not frozen after Stage 4)
  - Ensures Stage 6 final QC tests reflect reality

**Why this matters:** Plans change during implementation. Actual code reveals insights that specs couldn't predict. Stage 5d keeps remaining feature specs aligned with reality. Stage 5e keeps the epic testing plan current as features are actually built.

---

**Previous Update - Stage Renumbering:**
- **Stage 3** (was "Reserved"): Now **Cross-Feature Sanity Check**
- **Stage 4** (NEW): **Re-evaluate Epic-Level Testing Strategy**
  - Review initial test plan created in Stage 1
  - Update based on findings from deep dives (Stage 2) and sanity check (Stage 3)
  - Identify integration points between features
  - Define epic-level test scenarios with actual knowledge (not assumptions)
  - Ensures testing strategy reflects reality discovered during planning

**Why this matters:** Initial epic test plan (Stage 1) is based on assumptions before deep diving into features. After completing all deep dives and alignment checks, we have real knowledge about how features interact. Stage 4 updates the testing strategy to reflect this reality.

---

## Key Problems with V1 Guides

1. **Terminology confusion**: "Sub-features" vs "Features" was unclear
2. **Overly complex phase tracking**: SUB_FEATURES_PHASE_TRACKER with 800+ checkpoints became unwieldy
3. **No epic-level planning**: Jumped straight into sub-feature breakdown without higher-level vision
4. **Premature commitment**: All planning done upfront before any implementation feedback
5. **Missing PR review step**: QC rounds didn't include thorough code review checklist
6. **No bug fix workflow**: No clear process for handling issues discovered during implementation
7. **Rigid structure**: All features had to complete planning before any implementation could start
8. **Lessons learned applied too late**: Guide updates happened after epic completion instead of incrementally

---

## Terminology Changes (V1 → V2)

| V1 Term | V2 Term | Description |
|---------|---------|-------------|
| `{name}.txt` in feature-updates/ | **Epic Request** | Initial user scratchwork describing the overall need |
| `{name}/` folder | **Epic** | Top-level folder containing all related work |
| Sub-feature | **Feature** | Individual component/step within an epic |
| Feature | **Epic** | The overarching body of work |

**Example Structure:**
```
feature-updates/
├── improve_draft_helper.txt           ← Epic Request (user notes)
├── improve_draft_helper/              ← Epic (folder)
│   ├── EPIC_README.md                ← Epic-level tracking
│   ├── epic_smoke_test_plan.md       ← How to test the full epic (updated in Stages 4, 5e)
│   ├── epic_lessons_learned.md       ← Cross-feature patterns and systemic insights
│   ├── feature_01_adp_integration/   ← Feature 1
│   │   ├── spec.md
│   │   ├── checklist.md
│   │   ├── lessons_learned.md
│   │   ├── todo.md
│   │   ├── implementation_checklist.md
│   │   ├── code_changes.md
│   │   └── README.md
│   ├── feature_02_rating_system/     ← Feature 2
│   ├── feature_03_injury_updates/    ← Feature 3
│   └── bugfix_high_auth_error/       ← Bug fix (if any)
```

---

## V2 Workflow Overview (7 Stages)

### Stage 1: Epic Planning
- Create epic folder structure
- Analyze epic request and codebase
- **Agent proposes feature breakdown** (user confirms/modifies)
- Create feature folders (spec, checklist, lessons learned, README per feature)
- Create epic-level README with tracking
- Plan epic-level smoke test and QC strategy

### Stage 2: Feature Deep Dives
- Loop through each feature sequentially
- Flesh out spec file using deep dive guide
- **NEW: Compare to already-completed feature specs** for alignment
- **If new scope discovered → evaluate if return to Stage 1 needed** (see criteria below)
- Complete ALL deep dives (including newly discovered features) before Stage 3
- Keep epic README updated with progress

**"New Scope" vs "Expanded Scope" Decision Criteria:**

When deep dive reveals additional work, determine:

**RETURN TO STAGE 1 (Epic Planning) - Add New Feature:**
- ✅ Work is **independent subsystem** (can be developed/tested separately)
- ✅ Work requires **3+ major components** not in current feature's scope
- ✅ Work has **different dependencies** than current feature (blocks/blocked by different features)
- ✅ Work addresses **different aspect** of epic request (not just more of same work)
- ✅ Work could **fail independently** without affecting current feature
- ✅ Work represents **20+ new checklist items**
- **Example:** During "Player Data Loading" deep dive, discover need for "Data Validation Service" (separate subsystem, different components, independent failure modes) → ADD NEW FEATURE

**HANDLE WITHIN STAGE 2 (Expanded Scope) - Update Current Feature:**
- ✅ Work is **extension** of current feature's functionality
- ✅ Work uses **same components** already identified in current feature
- ✅ Work has **same dependencies** as current feature
- ✅ Work is **directly related** to current feature's core purpose
- ✅ Work cannot **function independently** (tightly coupled to current feature)
- ✅ Work represents **<20 new checklist items**
- **Example:** During "Player Data Loading" deep dive, discover need for error handling, retry logic, progress logging → UPDATE CURRENT FEATURE SPEC

**When Uncertain:**
1. Ask: "Could this work be delivered in a separate release?"
   - YES → New feature (return to Stage 1)
   - NO → Expanded scope (update current feature)
2. Ask: "Does this work affect >50% of current feature's components?"
   - NO (affects small subset) → New feature
   - YES (affects most components) → Expanded scope
3. Ask: "If this work fails QC, should we still ship the current feature?"
   - YES → New feature (independent)
   - NO → Expanded scope (tightly coupled)

**Process for New Feature:**
1. Document discovery in current feature's README
2. Update epic EPIC_README.md: Note new feature discovered
3. Return to Stage 1: Create new feature folder, initial spec
4. Update epic structure (feature numbering, dependencies)
5. Continue with remaining Stage 2 deep dives (including new feature)

### Stage 3: Cross-Feature Sanity Check
- Systematically compare all feature specs
- Ensure requirements are aligned across features
- Resolve conflicts and inconsistencies
- Get user sign-off on complete plan

### Stage 4: Re-evaluate Epic-Level Testing Strategy
- Review initial epic smoke test plan (created in Stage 1)
- Update based on findings from deep dives (Stage 2) and sanity check (Stage 3)
- **Identify integration points** between features that need testing
- **Define epic-level test scenarios** that validate cross-feature workflows
- **Specify success criteria** for epic completion
- Document updated strategy in epic_smoke_test_plan.md
- Ensures testing strategy reflects actual implementation plan (not initial assumptions)

### Stage 5: Feature Implementation (Sequential)
For each feature:
- **5a: TODO Creation** (verification iterations)
- **5b: Implementation** (coding)
- **5c: Post-Implementation**
  - Smoke testing (3 parts)
  - QC rounds (3 rounds)
  - **NEW: PR Review Checklist** (11 categories)
  - Review lessons learned → **Update guides immediately**
  - **NO moving to done/ folder** (stays in epic until Stage 7)
  - **If issues found → COMPLETELY RESTART POST-IMPLEMENTATION (5c)**
- **5d: Cross-Feature Spec Alignment Check (Post-Implementation)**
  - Sequentially review ALL remaining (not-yet-implemented) feature specs
  - Compare against **actual implementation** of just-completed feature
  - Update specs if implementation revealed changes/insights
  - Ensures remaining features align with reality (not outdated plans)
  - Mark any features needing significant rework (see criteria below)

  **"Significant Rework" Criteria:**
  - **Return to Stage 5a (TODO):** Spec changes require >3 new TODO tasks, or algorithm changes significantly
  - **Return to Stage 2 (Deep Dive):** Spec assumptions fundamentally wrong, core approach needs redesign
  - **Return to Stage 1 (Epic Planning):** Feature should be split into 2+ features, or feature no longer needed
  - **Minor Updates (continue):** Spec clarifications requiring ≤3 TODO task adjustments, no algorithm changes

- **5e: Epic Testing Plan Reassessment**
  - Review epic_smoke_test_plan.md
  - Update based on **actual implementation** of just-completed feature
  - Add/modify test scenarios based on real integration points discovered
  - Keep testing plan current as epic evolves
  - Ensures Stage 6 tests reflect reality

**Bug Fix Workflow:**
- If user reports issue/missing scope during Stage 5:
  1. Create bug fix folder (marked high priority)
  2. Create notes.txt with issue description
  3. User verifies/updates notes
  4. Update epic documentation for resumability
  5. Run bug fix through ALL stages (deep dive → implementation → post-impl)
  6. Return to previously interrupted feature
- Bug fixes follow same process as features but marked high priority

### Stage 6: Epic-Level Final QC
- After ALL features complete
- Run full epic smoke test (from epic_smoke_test_plan.md)
- Run epic-level QC rounds
- Run epic-level PR review
- Validate end-to-end based on original epic request
- Create bug fixes for any issues discovered

### Stage 7: Epic Cleanup
- Final commits
- Move entire epic folder to done/

---

## Guide Files Needed (V2)

### Stage 1 Guides
1. **STAGE_1_epic_planning_guide.md**
   - How to analyze epic request
   - How to propose feature breakdown
   - Creating epic folder structure
   - Creating epic README with tracking
   - Planning epic-level smoke test/QC

### Stage 2 Guides
2. **STAGE_2_feature_deep_dive_guide.md** (adapted from v1)
   - Deep dive for individual feature
   - **NEW: Cross-feature alignment check** (compare to already-completed feature specs)
   - **NEW: Scope discovery evaluation** (new feature vs expanded scope criteria)
     - Independent subsystem? Different dependencies? 20+ items? → New feature (return to Stage 1)
     - Extension of current feature? Same components? <20 items? → Expanded scope (update spec)
   - Handling scope creep (return to epic planning when needed)
   - Updating epic README with progress and discoveries

### Stage 3 Guides
3. **STAGE_3_cross_feature_sanity_check_guide.md**
   - Systematic spec comparison
   - Conflict resolution
   - Final alignment verification

### Stage 4 Guides
4. **STAGE_4_epic_testing_strategy_guide.md** (NEW)
   - Reviewing initial test plan
   - Updating based on deep dive findings
   - Identifying integration points between features
   - Defining epic-level test scenarios
   - Specifying epic success criteria

### Stage 5 Guides
5. **Stage 5a TODO Creation** (split into 3 rounds)
   - **STAGE_5aa_round1_guide.md**: Iterations 1-7 + 4a (Requirements, dependencies, algorithms)
   - **STAGE_5ab_round2_guide.md**: Iterations 8-16 (Test strategy, edge cases, re-verification)
   - **STAGE_5ac_round3_guide.md**: Iterations 17-24 + 23a (Phasing, final gates, readiness)

6. **STAGE_5b_implementation_execution_guide.md** (adapted from v1)
   - Coding workflow
   - Continuous spec verification
   - Mini-QC checkpoints

7. **Stage 5c Post-Implementation** (split into 3 guides)
   - **STAGE_5ca_smoke_testing_guide.md**: Smoke testing protocol (3 parts)
   - **STAGE_5cb_qc_rounds_guide.md**: QC rounds (3 rounds) + restart protocol
   - **STAGE_5cc_final_review_guide.md**: PR Review (11 categories) + lessons learned

8. **STAGE_5d_post_feature_alignment_guide.md** (NEW - Stage 5d)
   - Reviewing all remaining feature specs after implementation
   - Comparing specs to actual implementation (not just plan)
   - Updating specs based on real insights
   - Identifying features needing rework
   - Maintaining alignment throughout implementation

9. **STAGE_5e_post_feature_testing_update_guide.md** (NEW - Stage 5e)
   - Reassessing epic_smoke_test_plan.md after each feature
   - Updating test scenarios based on actual implementation
   - Adding integration points discovered during implementation
   - Keeping testing plan current and accurate

10. **STAGE_5_bug_fix_workflow_guide.md** (NEW)
    - When to create bug fix
    - Bug fix folder structure
    - Notes.txt creation and user verification
    - Pausing current work and resuming after fix
    - High priority marking

### Stage 6 Guides
11. **STAGE_6_epic_final_qc_guide.md** (NEW)
    - **Epic-level smoke testing** (distinct from feature-level)
      - Feature smoke testing (Stage 5c): Tests individual feature in isolation
      - Epic smoke testing (Stage 6): Tests ENTIRE epic end-to-end with all features integrated
      - Focus: Cross-feature integration, workflows spanning multiple features, epic success criteria
      - Uses: epic_smoke_test_plan.md (evolved through Stages 1, 4, 5e)
    - Epic-level QC rounds (validates epic as a whole, not individual features)
    - Epic-level PR review (reviews epic-wide changes, architectural consistency)
    - End-to-end validation against original epic request
    - Bug fix creation for epic-level integration issues

### Stage 7 Guides
12. **STAGE_7_epic_cleanup_guide.md** (NEW)
    - Final commit checklist
    - Moving epic to done/
    - Documentation verification

### Support Files
13. **templates_v2.md** (updated)
    - Epic README template
    - Feature folder templates
    - Epic smoke test plan template
    - Bug fix folder templates

14. **prompts_reference_v2.md** (updated)
    - Stage transition prompts
    - Feature breakdown presentation
    - Cross-feature alignment prompts
    - Bug fix creation prompts
    - Post-feature alignment prompts (Stage 5d)
    - Post-feature testing update prompts (Stage 5e)

15. **README.md** (overview of v2 workflow)

---

## Template File Specifications

**The templates_v2.md file MUST include these templates with specified sections:**

### 1. Epic README Template (EPIC_README.md)

**Sections required:**
```markdown
# Epic: {epic_name}

## 🎯 Quick Reference Card (Always Visible)

**Current Stage:** Stage X - {stage name}
**Active Guide:** `guides_v2/{guide_name}.md`
**Last Guide Read:** {timestamp}

**Stage Workflow:**
Stage 1 → Stage 2 → Stage 3 → Stage 4 → Stage 5 → Stage 6 → Stage 7
  ↓         ↓         ↓         ↓         ↓         ↓         ↓
Epic    Features  Sanity   Testing   Impl     Epic      Done
Plan    Deep Dive  Check   Strategy  (5a-5e)  QC

**You are here:** ➜ Stage {X}

**Critical Rules for Current Stage:**
1. {Rule 1}
2. {Rule 2}
3. {Rule 3}

**Before Proceeding to Next Step:**
□ Read guide: `guides_v2/{current_guide}.md`
□ Acknowledge critical requirements
□ Verify prerequisites
□ Update this Quick Reference Card

---

## Agent Status

**Last Updated:** {YYYY-MM-DD HH:MM}
**Current Phase:** {PLANNING/TODO_CREATION/IMPLEMENTATION/POST_IMPLEMENTATION}
**Current Step:** {Specific step name}
**Current Guide:** {guide_file_name.md}
**Guide Last Read:** {YYYY-MM-DD HH:MM}
**Critical Rules from Guide:**
- {Rule 1 - e.g., "24 iterations mandatory, no skipping"}
- {Rule 2 - e.g., "Update Agent Status after each round"}
- {Rule 3 - e.g., "STOP if confidence < Medium"}

**Progress:** {X/Y items complete}
**Next Action:** {Exact next task + guide reference}
**Blockers:** {Issues or "None"}

---

## Epic Overview

**Epic Request:** `{epic_name}.txt`
**Created:** {date}
**Features:** {N} features identified

**Purpose:** {Brief description of epic goals from epic request}

---

## Feature Tracking

| # | Feature Name | Stage 2 Complete | Stage 5e Complete | Notes |
|---|--------------|------------------|-------------------|-------|
| 1 | feature_01_{name} | [x] / [ ] | [x] / [ ] | {status/notes} |
| 2 | feature_02_{name} | [x] / [ ] | [x] / [ ] | {status/notes} |
| ... | ... | ... | ... | ... |

**Stage 2 Complete:** Spec fleshed out from deep dive
**Stage 5e Complete:** Feature implementation fully complete

---

## Bug Fix Tracking

| # | Bug Fix Name | Priority | Status | Notes |
|---|--------------|----------|--------|-------|
| 1 | bugfix_high_{name} | high | Stage 5c | {current work} |
| ... | ... | ... | ... | ... |

---

## Guide Deviation Log

**Purpose:** Track when agent deviates from guide (helps identify guide gaps)

| Timestamp | Phase | Deviation | Reason | Impact |
|-----------|-------|-----------|--------|--------|
| {timestamp} | {phase} | {what was skipped/changed} | {why} | {consequence} |

**Rule:** If you deviate from guide, DOCUMENT IT HERE immediately.

---

## Epic Completion Checklist

**Stage 1 - Epic Planning:**
- [ ] Epic folder created
- [ ] All feature folders created
- [ ] Initial epic_smoke_test_plan.md created
- [ ] EPIC_README.md created

**Stage 2 - Feature Deep Dives:**
- [ ] ALL features have spec.md complete
- [ ] ALL features have checklist.md resolved

**Stage 3 - Cross-Feature Sanity Check:**
- [ ] All specs compared systematically
- [ ] Conflicts resolved
- [ ] User sign-off obtained

**Stage 4 - Epic Testing Strategy:**
- [ ] epic_smoke_test_plan.md updated
- [ ] Integration points identified
- [ ] Epic success criteria defined

**Stage 5 - Feature Implementation:**
- [ ] Feature 1: 5a→5b→5c→5d→5e complete
- [ ] Feature 2: 5a→5b→5c→5d→5e complete
- [ ] ... (all features)

**Stage 6 - Epic Final QC:**
- [ ] Epic smoke testing passed
- [ ] Epic QC rounds passed
- [ ] Epic PR review passed
- [ ] End-to-end validation passed

**Stage 7 - Epic Cleanup:**
- [ ] Final commits made
- [ ] Epic moved to done/ folder
```

---

### 2. Feature README Template (feature_XX_{name}/README.md)

**Sections required:**
```markdown
# Feature: {feature_name}

## Feature Context

**Part of Epic:** {epic_name}
**Feature Number:** {N}
**Created:** {date}

**Purpose:** {Brief description of what this feature does}

**Dependencies:**
- **Depends on:** {List features this depends on, or "None"}
- **Required by:** {List features that depend on this, or "Unknown yet"}

---

## Agent Status

**Last Updated:** {YYYY-MM-DD HH:MM}
**Current Phase:** {PLANNING/TODO_CREATION/IMPLEMENTATION/POST_IMPLEMENTATION}
**Current Step:** {Specific step - e.g., "Iteration 12/24"}
**Progress:** {X/Y items complete}
**Next Action:** {Exact next task}
**Blockers:** {Issues or "None"}

---

## Files in This Feature

- `spec.md` - Feature specification (requirements, algorithms, data structures)
- `checklist.md` - Open questions → Resolved decisions
- `todo.md` - Implementation task list (after 24 iterations)
- `implementation_checklist.md` - Continuous spec verification during coding
- `code_changes.md` - Documentation of all code changes made
- `lessons_learned.md` - Issues encountered and solutions
- `research/` - Research documents (if any)

---

## Feature Completion Checklist

**Stage 2 (Deep Dive):**
- [ ] spec.md created and complete
- [ ] checklist.md all items resolved
- [ ] Compared to other feature specs
- [ ] Updated epic EPIC_README.md

**Stage 5a (TODO Creation):**
- [ ] 24 verification iterations complete
- [ ] Iteration 4a: TODO Specification Audit PASSED
- [ ] Iteration 23a: Pre-Implementation Spec Audit (ALL 4 PARTS PASSED)
- [ ] Iteration 24: Implementation Readiness PASSED
- [ ] todo.md created

**Stage 5b (Implementation):**
- [ ] All TODO tasks complete
- [ ] All unit tests passing (100%)
- [ ] implementation_checklist.md all verified
- [ ] code_changes.md updated

**Stage 5c (Post-Implementation):**
- [ ] Smoke testing (3 parts) passed
- [ ] QC Round 1 passed
- [ ] QC Round 2 passed
- [ ] QC Round 3 passed
- [ ] PR Review (11 categories) passed
- [ ] lessons_learned.md updated

**Stage 5d (Cross-Feature Alignment):**
- [ ] Reviewed all remaining feature specs
- [ ] Updated specs based on actual implementation
- [ ] No significant rework needed for other features

**Stage 5e (Epic Testing Plan Update):**
- [ ] epic_smoke_test_plan.md reviewed
- [ ] Test scenarios updated
- [ ] Integration points added
```

---

### 3. Epic Smoke Test Plan Template (epic_smoke_test_plan.md)

**Sections required:**
```markdown
# Epic Smoke Test Plan: {epic_name}

**Purpose:** Define how to validate the complete epic end-to-end

**Created:** {date} (Stage 1)
**Last Updated:** {date} (Stage X)

---

## Epic Success Criteria

**The epic is successful if:**

1. {Measurable criterion 1}
   - Example: "All 6 position files (QB, RB, WR, TE, K, DST) created in data/player_data/"
2. {Measurable criterion 2}
   - Example: "Each position file contains >100 players with complete stats"
3. {Measurable criterion 3}
   - Example: "Draft helper mode loads all player data without errors"

---

## Specific Commands/Scenarios

**These tests MUST be run every time:**

### Test 1: {Test Name}
```bash
{exact command to run}
```
**Expected result:** {what should happen}
**Failure indicates:** {what's wrong if this fails}

### Test 2: {Test Name}
```bash
{exact command to run}
```
**Expected result:** {what should happen}
**Failure indicates:** {what's wrong if this fails}

{Continue for all specific commands...}

---

## High-Level Test Categories

**Agent creates specific test scenarios for these categories:**

### Category 1: Cross-Feature Integration
**What to test:** {description}
**Agent will create scenarios for:**
- {Integration point 1 discovered during implementation}
- {Integration point 2 discovered during implementation}

### Category 2: Error Handling
**What to test:** {description}
**Agent will create scenarios for:**
- {Error path 1 discovered during implementation}
- {Error path 2 discovered during implementation}

### Category 3: Edge Cases
**What to test:** {description}
**Agent will create scenarios for:**
- {Edge case 1 discovered during implementation}
- {Edge case 2 discovered during implementation}

{Continue for all categories...}

---

## Update Log

**Track when and why this plan was updated:**

| Date | Stage | What Changed | Why |
|------|-------|--------------|-----|
| {date} | Stage 1 | Initial plan created | Epic planning |
| {date} | Stage 4 | Updated based on deep dives | Discovered {N} integration points |
| {date} | Stage 5e (Feature 1) | Added test for {X} | Feature 1 implementation revealed {Y} |
| ... | ... | ... | ... |

**Current version is informed by:**
- Stage 1: Initial assumptions
- Stage 4: Deep dive findings (Stages 2-3)
- Stage 5e updates: {List features that have updated this plan}
```

---

### 4. Bug Fix Notes Template (bugfix_{priority}_{name}/notes.txt)

**Sections required:**
```
BUG FIX: {name}
Priority: {high/medium/low}
Discovered: {date}
Discovered During: {which stage/feature}

---

ISSUE DESCRIPTION:

{Clear description of the bug/issue}

What's wrong:
- {Symptom 1}
- {Symptom 2}

How discovered:
- {How the issue was found - e.g., "QC Round 2 revealed...", "User reported..."}

Impact:
- {What doesn't work because of this bug}

---

ROOT CAUSE (if known):

{Analysis of why the bug exists}

---

PROPOSED SOLUTION:

{How to fix it}

Changes needed:
- {File/module 1: what needs to change}
- {File/module 2: what needs to change}

---

USER NOTES:

{User adds their own notes, corrections, or additional context here}
```

---

### 5. GUIDE_ANCHOR Template (GUIDE_ANCHOR.md in each epic folder)

**Sections required:**
```markdown
# GUIDE ANCHOR - READ THIS AFTER SESSION COMPACTION

**If you're resuming work on this epic after session compaction:**

1. **You are in:** {epic_name}
2. **Read FIRST:** `EPIC_README.md` (especially "Agent Status" and "Quick Reference Card")
3. **Current Stage:** Stage {X} - {name}
4. **Active Guide:** `feature-updates/guides_v2/{guide_name}.md`
5. **You MUST read the active guide before continuing**

**Do NOT:**
- ❌ Assume you know what to do
- ❌ Continue from memory
- ❌ Skip reading the guide
- ❌ Use "common sense" instead of documented process

**DO:**
- ✅ Read EPIC_README.md Agent Status
- ✅ Read the active guide (use Read tool)
- ✅ Acknowledge critical requirements from guide
- ✅ Verify prerequisites before proceeding
- ✅ Update Agent Status after reading guide

**Critical Workflow Reference:**

Stage 1: Epic Planning (STAGE_1_epic_planning_guide.md)
  ↓
Stage 2: Feature Deep Dives (STAGE_2_feature_deep_dive_guide.md) - Loop per feature
  ↓
Stage 3: Cross-Feature Sanity Check (STAGE_3_cross_feature_sanity_check_guide.md)
  ↓
Stage 4: Epic Testing Strategy (STAGE_4_epic_testing_strategy_guide.md)
  ↓
Stage 5: Feature Implementation (Loop per feature)
  5a: TODO Creation
      - Round 1 (STAGE_5aa_round1_guide.md)
      - Round 2 (STAGE_5ab_round2_guide.md)
      - Round 3 (STAGE_5ac_round3_guide.md)
  5b: Implementation (STAGE_5b_implementation_execution_guide.md)
  5c: Post-Implementation
      - Smoke Testing (STAGE_5ca_smoke_testing_guide.md)
      - QC Rounds (STAGE_5cb_qc_rounds_guide.md)
      - Final Review (STAGE_5cc_final_review_guide.md)
  5d: Cross-Feature Alignment (STAGE_5d_post_feature_alignment_guide.md)
  5e: Testing Plan Update (STAGE_5e_post_feature_testing_update_guide.md)
  ↓
Stage 6: Epic Final QC (STAGE_6_epic_final_qc_guide.md)
  ↓
Stage 7: Epic Cleanup (STAGE_7_epic_cleanup_guide.md)

**Find current stage in Agent Status → Read corresponding guide**
```

---

## Example Phase Transition Prompts

**Purpose:** These examples show the exact format and style agents should use when transitioning between stages. These will be expanded into the complete `prompts_reference_v2.md` guide.

**Critical Requirements:**
1. Agent MUST read the guide FIRST (use Read tool)
2. Agent MUST acknowledge what they read (list critical requirements)
3. Agent MUST verify prerequisites
4. Agent MUST update README Agent Status
5. THEN AND ONLY THEN proceed with the phase

---

### Example 1: Starting Stage 5a Round 1 (TODO Creation)

**User says:** "Prepare for updates based on feature_01_adp_integration"

**Note:** Stage 5a is split into 3 rounds. This example shows starting Round 1.

**Agent MUST respond:**

```
I'm reading `STAGE_5aa_round1_guide.md` to ensure I follow all 8 iterations in Round 1...

**The guide requires:**
- **Round 1: 8 MANDATORY iterations** (NO SKIPPING):
  - Iterations 1-7 + iteration 4a (TODO Specification Audit)
- **Iteration 4a is a MANDATORY GATE**:
  - Every TODO task MUST have acceptance criteria
  - Cannot proceed to Round 2 without PASSING iteration 4a
- **Algorithm Traceability Matrix** (iteration 4):
  - Map EVERY algorithm in spec.md to exact code location
  - Typical matrix has 40+ mappings
- **Integration Gap Check** (iteration 7):
  - Verify all new methods have identified CALLERS
  - No orphan code allowed
- **Interface Verification Protocol**:
  - READ actual source code for every dependency
- **STOP if confidence < Medium at Round 1 checkpoint**:
  - Create questions.md with unresolved questions
  - Wait for user answer before Round 2

**Prerequisites I'm verifying:**
✅ spec.md exists and is complete
✅ checklist.md all items resolved
✅ Stage 4 (Epic Testing Strategy) complete
✅ epic_smoke_test_plan.md updated

**I'll now begin iteration 1: Requirements Coverage Check...**

**Updating README Agent Status:**
- Current Phase: TODO_CREATION_ROUND_1
- Current Guide: STAGE_5aa_round1_guide.md
- Guide Last Read: 2025-12-30 15:23
- Critical Rules: "8 iterations mandatory", "Iteration 4a MANDATORY GATE", "STOP if confidence < Medium"
- Progress: 0/8 iterations complete (Round 1)
- Next Action: Iteration 1 - Requirements Coverage Check

Starting iteration 1...
```

**Why this format works:**
- Proves agent READ the guide (lists specific requirements)
- Verifies prerequisites (prevents starting when blocked)
- Updates Agent Status (ensures persistence through compaction)
- Clear next action (agent knows exactly what to do)

---

### Example 2: Starting Stage 5c Phase 1 (Smoke Testing)

**User says:** "Run QC" or "Validate the implementation"

**Agent MUST respond:**

```
I'm reading `STAGE_5ca_smoke_testing_guide.md` to ensure I follow the 3-part smoke testing protocol...

**The guide requires:**
- **Part 1: Import Test** (verify module loads without errors)
- **Part 2: Entry Point Test** (verify script starts correctly)
- **Part 3: E2E Execution Test** (CRITICAL - verify OUTPUT DATA VALUES)
  - Run feature with REAL data (not mocks)
  - **Verify ACTUAL DATA VALUES** (not just file existence)
  - BAD: assert Path("output.csv").exists()  # Structure only
  - GOOD: assert df['projected_points'].sum() > 0  # Data values
- **Re-Reading Checkpoints** - After Part 2 and Part 3
- **MANDATORY GATE** - All 3 parts must pass to proceed to QC rounds

**Prerequisites I'm verifying:**
✅ Stage 5b (Implementation) complete
✅ All TODO tasks marked done
✅ All unit tests passing (100% pass rate)
✅ code_changes.md updated
✅ implementation_checklist.md all verified

**I'll now begin with Part 1: Import Test...**

**Updating README Agent Status:**
- Current Phase: POST_IMPLEMENTATION_SMOKE_TESTING
- Current Guide: STAGE_5ca_smoke_testing_guide.md
- Guide Last Read: 2025-12-30 15:30
- Critical Rules: "3 parts MANDATORY", "Verify DATA VALUES not structure", "GATE before QC rounds"
- Progress: 0/3 parts complete
- Next Action: Smoke Test Part 1 - Import test

Running import test for feature_01_adp_integration...
```

**Why this format works:**
- Lists critical protocols (smoke testing, QC rounds, restart rule)
- Verifies implementation is actually complete
- Shows understanding of "no partial work" rule
- Clear starting point (smoke test part 1)

---

### Example 3: Starting Stage 2 (Feature Deep Dive)

**User says:** "Help me develop the improve_draft_helper feature" (after Stage 1 epic planning complete)

**Agent MUST respond:**

```
I'm reading `STAGE_2_feature_deep_dive_guide.md` to ensure I follow the complete deep dive workflow...

**The guide requires:**
- Phase 1: Targeted research (ONLY for this feature's scope, not entire epic)
- Phase 2: Update spec.md and checklist.md with findings
- **Phase 3: Interactive question resolution**
  - **ONE question at a time** (Lesson learned: don't batch questions)
  - Update spec/checklist after EACH answer
  - Evaluate for new questions after each resolution
- Phase 4: Feature complete + **dynamic scope adjustment check**
  - If scope grew significantly (>35 checklist items), propose split into additional features
  - Return to Stage 1 (Epic Planning) to add new features if needed
- Phase 5: Next feature or cross-feature alignment review
- **All research documents go in research/ folder**
- **NEW SCOPE DISCOVERY:** If deep dive reveals entirely new work not in original epic → return to Stage 1, add feature, update epic structure

**Prerequisites I'm verifying:**
✅ Stage 1 (Epic Planning) complete
✅ Epic folder structure created
✅ Feature folder `feature_01_adp_integration/` exists
✅ Initial spec.md created (from Stage 1)
✅ Initial checklist.md created (empty or with preliminary items)
✅ epic_smoke_test_plan.md exists (initial version)

**I'll now proceed with Phase 1: Targeted Research for feature_01_adp_integration...**

**Updating Epic EPIC_README.md Agent Status:**
- Current Phase: DEEP_DIVE
- Current Guide: STAGE_2_feature_deep_dive_guide.md
- Guide Last Read: 2025-12-30 15:15
- Critical Rules: "One question at a time", "Research goes in research/ folder", "If scope >35 items, propose split"
- Next Action: Phase 1 - Targeted research for ADP integration feature

Starting targeted research...
```

**Why this format works:**
- Shows understanding of "one question at a time" rule
- References research/ folder organization
- Acknowledges dynamic scope adjustment (can return to Stage 1)
- Updates epic-level README (not just feature README)

---

### Example 4: Resuming After Session Compaction

**Agent resumes work on in-progress epic**

**Agent MUST respond:**

```
I found an in-progress epic: `improve_draft_helper/`

**🚨 FIRST: Reading EPIC_README.md for exact status...**

**Agent Status from EPIC_README:**
- Current Phase: TODO_CREATION_ROUND_2
- Current Step: Iteration 12/24 (Round 2, iteration 5/9)
- Current Guide: STAGE_5ab_round2_guide.md
- Guide Last Read: 2025-12-29 14:30
- Critical Rules from README: "9 iterations in Round 2", "Re-verification iterations critical", "STOP if confidence < Medium"
- Progress: Round 1 complete (8/8), Round 2 in progress (4/9)
- Next Action: Begin iteration 12 - E2E Data Flow (Re-verify)
- Blockers: None

**I'm now re-reading `STAGE_5ab_round2_guide.md` to ensure I continue correctly...**

**The guide requires:**
- 24 mandatory iterations (currently at iteration 11/24, starting Round 2)
- Round 2: Iterations 8-16 (I'm at iteration 12)
- Iteration 12 focus: Test Coverage Depth Check (verify tests cover edge cases, failure modes)
- Update todo.md after each iteration
- Create questions file if blockers arise
- STOP if confidence < Medium

**Verification before continuing:**
✅ todo.md exists (from Round 1)
✅ Iterations 1-11 marked complete in todo.md
✅ No questions file (no blockers from Round 1)
✅ spec.md and checklist.md exist

**I'll continue from where the previous agent left off: Iteration 12 - Test Coverage Depth Check**

**Updating README Agent Status with re-read timestamp:**
- Guide Last Read: 2025-12-30 15:35 (RE-READ after session compaction)

Starting iteration 12...
```

**Why this format works:**
- Reads EPIC_README.md FIRST (persistent state)
- Re-reads the guide even though previous agent already read it
- Verifies exactly where to continue (iteration 12, not just "Round 2")
- Updates Agent Status with re-read timestamp (proves guide was loaded)
- Clear continuation point (no duplication of previous work)

---

### Key Patterns in All Examples

**Every phase transition prompt MUST include:**

1. **"I'm reading `{guide_name}.md`..."** - Proves agent is loading the guide
2. **"The guide requires:"** - Lists 5-10 critical requirements from the guide
3. **"Prerequisites I'm verifying:"** - Checklist of prerequisites with ✅/❌ status
4. **"I'll now proceed with..."** - Clear statement of first action
5. **"Updating README Agent Status:"** - Shows Agent Status fields being updated

**Format rules:**
- Use bullet points for requirements (easier to scan after compaction)
- Use ✅/❌ for prerequisite verification (visual clarity)
- Include specific numbers (24 iterations, 3 parts, 11 categories) - proves reading
- Quote critical rules that appear in guide ("STOP if confidence < Medium")
- Reference file names (spec.md, todo.md) - shows understanding of structure
- Include timestamp for "Guide Last Read" field

**Anti-patterns to avoid:**
- ❌ "I'm familiar with the process" - NEVER acceptable
- ❌ "I know what to do" - Must read guide
- ❌ "Following the usual workflow" - Must list specific requirements
- ❌ Generic acknowledgment - Must be specific to THIS guide's requirements
- ❌ Skipping prerequisite verification - Must verify before proceeding

---

**These examples will be expanded into complete prompts_reference_v2.md with:**
- Planning phase prompts (Stages 1-4)
- Implementation phase prompts (Stages 5a-5e)
- QC phase prompts (Stages 6-7)
- Bug fix prompts
- Problem situation prompts (when stuck, tests failing, etc.)
- User interaction prompts (presenting options, asking clarification)

---

## Stage-to-Guide Quick Reference

**Use this table to quickly identify which guide to read for each stage/sub-stage:**

| Stage | Sub-stage | Guide File | Quick Purpose |
|-------|-----------|------------|---------------|
| **1** | - | `STAGE_1_epic_planning_guide.md` | Analyze epic request, propose feature breakdown, create epic structure |
| **2** | - | `STAGE_2_feature_deep_dive_guide.md` | Flesh out spec.md for each feature, compare to completed features |
| **3** | - | `STAGE_3_cross_feature_sanity_check_guide.md` | Compare all specs systematically, resolve conflicts, get user sign-off |
| **4** | - | `STAGE_4_epic_testing_strategy_guide.md` | Update epic smoke test plan based on deep dive findings |
| **5** | **5a** | 3 rounds (see below) | 24 verification iterations, create todo.md with complete task list |
| **5** | **5aa** | `STAGE_5aa_round1_guide.md` | Round 1: Iterations 1-7 + 4a (Requirements, dependencies, algorithms) |
| **5** | **5ab** | `STAGE_5ab_round2_guide.md` | Round 2: Iterations 8-16 (Test strategy, edge cases, re-verification) |
| **5** | **5ac** | `STAGE_5ac_round3_guide.md` | Round 3: Iterations 17-24 + 23a (Phasing, final gates, readiness) |
| **5** | **5b** | `STAGE_5b_implementation_execution_guide.md` | Implement feature with continuous spec verification |
| **5** | **5c** | 3 phases (see below) | Post-implementation validation (smoke testing, QC rounds, PR review) |
| **5** | **5ca** | `STAGE_5ca_smoke_testing_guide.md` | Smoke Testing: 3 parts (import, entry point, E2E with DATA VALUES) |
| **5** | **5cb** | `STAGE_5cb_qc_rounds_guide.md` | QC Rounds: 3 rounds (basic, deep, final) with restart protocol |
| **5** | **5cc** | `STAGE_5cc_final_review_guide.md` | Final Review: PR review (11 categories) + lessons learned |
| **5** | **5d** | `STAGE_5d_post_feature_alignment_guide.md` | Review remaining feature specs, update based on actual implementation |
| **5** | **5e** | `STAGE_5e_post_feature_testing_update_guide.md` | Update epic_smoke_test_plan.md based on completed feature |
| **5** | **(bug)** | `STAGE_5_bug_fix_workflow_guide.md` | Handle bugs discovered during implementation |
| **6** | - | `STAGE_6_epic_final_qc_guide.md` | Epic-level smoke testing, QC, PR review, end-to-end validation |
| **7** | - | `STAGE_7_epic_cleanup_guide.md` | Final commits, move epic to done/ folder |
| **-** | - | `templates_v2.md` | Templates for all epic and feature files |
| **-** | - | `prompts_reference_v2.md` | Phase transition prompts (MUST use when starting stages) |
| **-** | - | `README.md` | Overview of v2 workflow, guide index |

**Stage Flow:**
```
Stage 1 → Stage 2 (loop per feature) → Stage 3 → Stage 4 →
Stage 5 (loop per feature: 5a→5b→5c→5d→5e) → Stage 6 → Stage 7
```

**When to use which guide:**
- **Starting a new epic?** → Read STAGE_1_epic_planning_guide.md
- **Planning a feature?** → Read STAGE_2_feature_deep_dive_guide.md
- **Ready to implement?** → Read STAGE_5aa_round1_guide.md (then 5ab, 5ac)
- **Finished a feature?** → Read STAGE_5d_post_feature_alignment_guide.md then STAGE_5e_post_feature_testing_update_guide.md
- **Bug discovered?** → Read STAGE_5_bug_fix_workflow_guide.md
- **All features done?** → Read STAGE_6_epic_final_qc_guide.md
- **After session compaction?** → Check README Agent Status for current stage, read corresponding guide

---

## Key Improvements in V2

### 1. Clearer Hierarchy
- **Epic** (top level) → **Features** (implementation units)
- No more confusion between "feature" and "sub-feature"

### 2. Epic-Level Tracking
- Epic README maintains high-level progress
- Two checkpoints per feature:
  - ✅ Spec fleshed out from deep dive
  - ✅ Feature implementation complete
- Epic-level smoke test plan created upfront

### 3. Iterative Discovery
- Deep dives can uncover new features → return to planning
- No need to know all features upfront
- Allows for adaptive planning based on learning

### 4. Cross-Feature Alignment
- **During deep dive**: Compare new feature spec to completed ones
- **Stage 3**: Systematic sanity check across all features
- Prevents conflicts discovered late in implementation

### 5. Adaptive Epic Testing Strategy
- **Stage 1**: Create initial epic smoke test plan based on assumptions
- **Stage 4**: Re-evaluate and update based on actual deep dive findings
- **Stage 5e**: Update after EACH feature completes (based on actual implementation)
- **Stage 6**: Execute final testing using evolved plan
- Identify integration points between features revealed during planning
- Define realistic epic-level test scenarios (not guesswork)
- Ensures testing strategy reflects reality, not initial assumptions

**Epic Testing Plan Evolution Timeline:**
```
Stage 1 (Epic Planning)
   │
   ├─> CREATE epic_smoke_test_plan.md
   │   • Based on: Initial analysis of epic request
   │   • Quality: Assumptions and guesses
   │   • Content: High-level categories, rough scenarios
   │   • Purpose: Placeholder for future updates
   │
   ↓
Stage 2 (Feature Deep Dives)
   │  [Plan does NOT change during deep dives]
   │  [Findings accumulate for Stage 4 update]
   │
   ↓
Stage 3 (Cross-Feature Sanity Check)
   │  [Plan does NOT change during sanity check]
   │  [Alignment findings inform Stage 4 update]
   │
   ↓
Stage 4 (Epic Testing Strategy Re-evaluation) ⚡ MAJOR UPDATE
   │
   ├─> UPDATE epic_smoke_test_plan.md
   │   • Based on: ALL feature specs (post-deep-dive), cross-feature alignment findings
   │   • Quality: Real knowledge (not assumptions)
   │   • Content: Specific test scenarios, integration points between features
   │   • Changes: Add specific commands, define success criteria, identify cross-feature dependencies
   │   • Purpose: Concrete testing strategy ready for validation as features are built
   │
   ↓
Stage 5 (Feature Implementation - Loop per feature)
   │
   ├─> Feature 1: 5a → 5b → 5c → 5d → 5e
   │                                   │
   │                                   └─> UPDATE epic_smoke_test_plan.md ⚡ INCREMENTAL
   │                                       • Based on: ACTUAL implementation of Feature 1
   │                                       • Changes: Add/modify test scenarios based on real code
   │                                       • Content: New integration points discovered during implementation
   │                                       • Purpose: Keep plan current with reality
   │
   ├─> Feature 2: 5a → 5b → 5c → 5d → 5e
   │                                   │
   │                                   └─> UPDATE epic_smoke_test_plan.md ⚡ INCREMENTAL
   │                                       • Based on: ACTUAL implementation of Feature 2
   │                                       • Changes: Add scenarios for Feature 1 ↔ Feature 2 integration
   │
   ├─> Feature N: 5a → 5b → 5c → 5d → 5e
   │                                   │
   │                                   └─> UPDATE epic_smoke_test_plan.md ⚡ INCREMENTAL
   │                                       • Based on: ACTUAL implementation of Feature N
   │                                       • Result: Plan now reflects ENTIRE epic as actually built
   │
   ↓
Stage 6 (Epic Final QC)
   │
   ├─> EXECUTE epic_smoke_test_plan.md ✅ FINAL TESTING
   │   • Use: Fully evolved plan (Stage 1 → 4 → 5e updates)
   │   • Quality: Reflects actual implementation (not original assumptions)
   │   • Purpose: Validate epic end-to-end with realistic test scenarios
   │
   ↓
Stage 7 (Epic Cleanup)
   └─> Move epic (including evolved test plan) to done/

Legend:
⚡ = Update checkpoint
✅ = Execution checkpoint
```

**Why this evolution matters:**

1. **Stage 1 (Initial)**: Plan created with ZERO implementation knowledge
   - Based on user's epic request (often vague)
   - Educated guesses about what to test
   - High-level categories without specifics

2. **Stage 4 (Major Update)**: Plan updated with DEEP DIVE knowledge
   - Based on detailed feature specs (post-planning)
   - Knows what features will do and how they interact
   - Can define specific test scenarios
   - Still hasn't seen actual code (implementation may differ from plan)

3. **Stage 5e (Incremental Updates)**: Plan updated with IMPLEMENTATION knowledge
   - Based on ACTUAL CODE (not just specs)
   - Discovers integration points specs didn't predict
   - Identifies edge cases implementation revealed
   - Adds test scenarios for real behavior (not assumed behavior)
   - **Example**: Spec said "Feature 1 outputs JSON" but implementation revealed "JSON has nested structure that Feature 3's parser can't handle" → Add integration test

4. **Stage 6 (Execution)**: Plan is now ACCURATE and COMPLETE
   - Reflects epic as actually built (not as originally imagined)
   - Tests validate real integration points (not assumed ones)
   - Success criteria match actual implementation capabilities

**Without this evolution:** Stage 6 would test against Stage 1 assumptions (outdated by 4 stages of learning)

### 6. PR Review Integration
- **11-category code review checklist**:
  1. Correctness and Logic
  2. Code Quality and Readability
  3. Comments and Documentation
  4. Refactoring Concerns
  5. Testing
  6. Security
  7. Performance
  8. Error Handling
  9. Architecture and Design
  10. Compatibility and Integration
  11. Scope and Focus
- Simulates real Tech Lead PR review
- Catches issues QC rounds miss

### 7. Post-Implementation Restart Protocol
- **CRITICAL RULE**: If ANY issues found in:
  - Smoke testing
  - QC rounds (1, 2, or 3)
  - PR review checklist
- Then **COMPLETELY RESTART POST-IMPLEMENTATION STAGE**
- Ensures high quality before moving to next feature

### 8. Bug Fix Workflow
- Clear process for handling issues discovered during implementation
- High priority marking
- Proper documentation for resuming previous work
- Bug fixes go through full workflow (deep dive → impl → post-impl)

### 9. Immediate Guide Updates
- Lessons learned reviewed after EACH feature's post-implementation
- Guides updated incrementally (not waiting until epic completion)
- Continuous process improvement within the epic

### 10. No Premature "Done" Folder
- Features stay in epic folder until Stage 7
- Allows for epic-level integration testing
- Easier to create bug fixes without moving files back

### 11. Epic-Level Final QC (Stage 6)
- After all features complete, validate ENTIRE epic end-to-end
- Ensures features integrate correctly
- Validates against original epic request (not just individual feature specs)

**Epic vs Feature Smoke Testing - Critical Distinction:**

| Aspect | Feature Smoke Testing (Stage 5c) | Epic Smoke Testing (Stage 6) |
|--------|----------------------------------|------------------------------|
| **Scope** | Single feature in isolation | All features integrated together |
| **Purpose** | Verify feature works independently | Verify features work together |
| **Test Plan** | Feature-specific test scenarios | epic_smoke_test_plan.md (evolved) |
| **Focus** | Feature implementation correctness | Cross-feature integration, workflows |
| **Example** | "Feature 1 creates JSON output" | "Feature 3 can parse Feature 1's JSON" |
| **Success** | Feature meets its spec.md | Epic achieves original epic request goals |
| **Failures** | Feature bugs (code doesn't match spec) | Integration bugs (features conflict) |
| **When Run** | After implementing ONE feature | After implementing ALL features |

**Why both are needed:**
- **Feature smoke testing** catches feature-level bugs early (before building dependent features)
- **Epic smoke testing** catches integration bugs that only appear when features work together
- **Example failure caught ONLY by epic smoke testing:**
  - Feature 1 creates player_data.json with field "position" (lowercase)
  - Feature 2 reads player_data.json expecting field "Position" (capitalized)
  - Both features pass their own smoke tests (Feature 1 creates file, Feature 2 reads file)
  - Epic smoke test fails when Feature 2 tries to read Feature 1's actual output

### 12. Continuous Spec Alignment During Implementation (Stage 5d)
- **NEW**: After each feature completes, review ALL remaining feature specs
- Compare specs to **actual implementation** (not just original plan)
- Update remaining specs based on insights from completed implementation
- Prevents spec drift as implementation reveals reality
- Catches cascading changes early (before implementing dependent features)

### 13. Living Epic Testing Plan (Stage 5e)
- **NEW**: Reassess epic_smoke_test_plan.md after EACH feature completion
- Update test scenarios based on **actual implementation**
- Add newly discovered integration points
- Testing plan evolves with epic (not frozen after Stage 4)
- Ensures Stage 6 final QC tests reflect current reality

---

## Post-Implementation Enhancement: PR Review Checklist

**NEW 11-Category Code Review** (added to post_implementation_guide.md):

### 1. Correctness and Logic
- Does the code accomplish what it claims to do?
- Logic errors, off-by-one errors, incorrect conditionals?
- Edge cases and boundary conditions handled?
- Null/undefined handling appropriate?

### 2. Code Quality and Readability
- Easy to understand without excessive mental overhead?
- Names (variables, functions, classes) descriptive and consistent?
- Code appropriately modular, or functions doing too much?
- Unnecessary complexity that could be simplified?

### 3. Comments and Documentation
- Comments explaining "why" rather than restating "what"?
- Public APIs and complex logic adequately documented?
- Stale or misleading comments?
- PR description explains the change adequately?

### 4. Refactoring Concerns
- Change introduce duplication that should be abstracted?
- Opportunities to improve existing code touched by this change?
- Change consistent with existing patterns in the codebase?

### 5. Testing
- Sufficient unit/integration tests for new functionality?
- Tests cover edge cases and failure modes?
- Existing tests still valid, or do they need updates?

### 6. Security
- Input validation and sanitization
- Authentication/authorization checks
- Exposure of sensitive data (logs, errors, responses)
- Injection vulnerabilities (SQL, XSS, command injection)

### 7. Performance
- Inefficient algorithms or data structures?
- Unnecessary database queries or N+1 problems?
- Memory leaks or resource cleanup?
- Impact on latency-sensitive paths?

### 8. Error Handling
- Errors caught and handled appropriately?
- Error messages helpful for debugging?
- Logging sufficient but not excessive?

### 9. Architecture and Design
- Change fit the overall system architecture?
- Dependencies flowing in the right direction?
- Appropriate separation of concerns?

### 10. Compatibility and Integration
- Backwards compatibility with existing clients/APIs?
- Database migration safety?
- Configuration changes and their rollout?
- Dependencies: are new ones justified? Are versions appropriate?

### 11. Scope and Focus
- Does the PR do one thing well, or is it mixing concerns?
- Are unrelated changes sneaking in?

**Restart Rule**: If ANY issues found → COMPLETELY RESTART POST-IMPLEMENTATION STAGE

---

## File Organization

### Epic-Level Files
```
feature-updates/{epic_name}/
├── EPIC_README.md                     # High-level tracking and status
├── epic_smoke_test_plan.md            # How to test the complete epic (updated in Stages 4, 5e)
├── epic_lessons_learned.md            # Cross-feature patterns and systemic insights
├── feature_{N}_{name}/                # Individual features
└── bugfix_{priority}_{name}/          # Bug fixes (if any)
```

### Feature-Level Files
```
feature_{N}_{name}/
├── README.md                          # Feature context and status
├── spec.md                            # Detailed requirements
├── checklist.md                       # Open questions → resolved
├── todo.md                            # Implementation tracking
├── implementation_checklist.md        # Continuous spec verification
├── code_changes.md                    # What was changed
├── lessons_learned.md                 # Feature-specific lessons
└── research/                          # Research documents (if needed)
```

### Bug Fix Files
**Location:** Inside epic folder (e.g., `feature-updates/{epic_name}/bugfix_{priority}_{name}/`)

```
bugfix_{priority}_{name}/
├── notes.txt                          # Issue description (user-verified)
├── spec.md                            # Fix requirements
├── checklist.md                       # Same as features
├── todo.md                            # Same as features
├── implementation_checklist.md        # Same as features
├── code_changes.md                    # Same as features
└── lessons_learned.md                 # Same as features
```

**Priority levels:** `high`, `medium`, `low`

**Naming example:** `bugfix_high_authentication_error/`

### Bug Fix Stage Workflow

**IMPORTANT:** Bug fixes follow a SIMPLIFIED workflow compared to features.

**Bug fixes go through these stages:**

1. **Bug Fix Creation (when discovered):**
   - User reports issue or agent discovers bug during any stage
   - Create `bugfix_{priority}_{name}/` folder in epic directory
   - Create `notes.txt` with issue description
   - User verifies/updates notes.txt

2. **Stage 2 (Deep Dive) - Adapted for bug fix:**
   - Create `spec.md` for bug fix (what needs to be fixed, root cause, solution)
   - Create `checklist.md` (usually shorter than features)
   - Create `lessons_learned.md`
   - Update epic EPIC_README.md to track bug fix

3. **Stage 5a (TODO Creation):**
   - Follow STAGE_5aa_round1_guide.md → Round 1 (iterations 1-7 + 4a)
   - Follow STAGE_5ab_round2_guide.md → Round 2 (iterations 8-16)
   - Follow STAGE_5ac_round3_guide.md → Round 3 (iterations 17-24 + 23a)
   - 24 verification iterations total (same as features)
   - Create `todo.md`

4. **Stage 5b (Implementation):**
   - Follow STAGE_5b_implementation_execution_guide.md
   - Implement the fix
   - Create `implementation_checklist.md`
   - Create `code_changes.md`

5. **Stage 5c (Post-Implementation):**
   - Follow STAGE_5ca_smoke_testing_guide.md → Smoke testing (3 parts)
   - Follow STAGE_5cb_qc_rounds_guide.md → QC rounds (1, 2, 3)
   - Follow STAGE_5cc_final_review_guide.md → PR Review (11 categories)
   - If ANY issues → RESTART Post-Implementation from smoke testing

**Bug fixes SKIP these epic-level stages:**
- ❌ Stage 1 (Epic Planning) - epic already planned
- ❌ Stage 3 (Cross-Feature Sanity Check) - not needed for single bug fix
- ❌ Stage 4 (Epic Testing Strategy) - not needed for single bug fix
- ❌ Stage 5d (Cross-Feature Alignment) - bug fix doesn't affect other feature specs
- ❌ Stage 5e (Epic Testing Plan Update) - handled in Stage 5c for bug fix
- ❌ Stage 6 (Epic Final QC) - bug fix has own QC in Stage 5c
- ❌ Stage 7 (Epic Cleanup) - bug fix stays with epic until epic moves to done/

**After bug fix completion:**
- Bug fix folder stays in epic directory
- Agent returns to previously interrupted work
- Epic continues from where it left off

**Priority handling:**
- `high` priority: Interrupt current work immediately
- `medium` priority: Complete current sub-stage, then switch to bug fix
- `low` priority: Complete current feature, then switch to bug fix

---

## Stage Transition Flow

```
Epic Request (.txt file)
    ↓
STAGE 1: Epic Planning
    ├─ Analyze request + codebase
    ├─ Propose feature breakdown (agent → user confirms)
    ├─ Create epic folder structure
    ├─ Create feature folders
    └─ Plan INITIAL epic-level smoke test/QC (will be updated in Stage 4)
    ↓
STAGE 2: Feature Deep Dives (Loop ALL features)
    ├─ Deep dive feature 1 → spec.md
    ├─ Compare to completed features (alignment)
    ├─ If new scope → return to Stage 1, add feature
    ├─ Deep dive feature 2 → spec.md
    ├─ Compare to feature 1 (alignment)
    ├─ ... continue for all features
    └─ Update epic README as progress is made
    ↓
STAGE 3: Cross-Feature Sanity Check
    ├─ Compare all spec files systematically
    ├─ Resolve conflicts
    └─ User sign-off on complete plan
    ↓
STAGE 4: Re-evaluate Epic-Level Testing Strategy
    ├─ Review initial test plan (from Stage 1)
    ├─ Update based on deep dive findings
    ├─ Identify integration points between features
    ├─ Define epic-level test scenarios
    ├─ Specify epic success criteria
    └─ Update epic_smoke_test_plan.md
    ↓
STAGE 5: Feature Implementation (Loop, Sequential)
    ├─ Feature 1:
    │   ├─ 5a: TODO Creation (verification iterations)
    │   ├─ 5b: Implementation (coding)
    │   ├─ 5c: Post-Implementation:
    │   │   ├─ Smoke testing (3 parts)
    │   │   ├─ QC rounds (1, 2, 3)
    │   │   ├─ PR Review (11 categories)
    │   │   ├─ If ANY issues → RESTART Post-Implementation (5c)
    │   │   └─ Review lessons → Update guides NOW
    │   ├─ 5d: Cross-Feature Spec Alignment Check:
    │   │   ├─ Review ALL remaining (unimplemented) feature specs
    │   │   ├─ Compare specs to ACTUAL implementation (not plan)
    │   │   ├─ Update specs based on real insights
    │   │   └─ Mark features needing significant rework
    │   └─ 5e: Epic Testing Plan Reassessment:
    │       ├─ Review epic_smoke_test_plan.md
    │       ├─ Update based on actual implementation
    │       ├─ Add integration points discovered
    │       └─ Keep testing plan current
    ├─ Feature 2: (same 5a→5b→5c→5d→5e process)
    ├─ ... continue for all features
    └─ Bug Fix Workflow (if issues discovered):
        ├─ Create bug fix folder
        ├─ Create notes.txt (user verifies)
        ├─ Update epic docs for resumability
        ├─ Run bug fix through ALL stages (1-5)
        └─ Return to interrupted feature
    ↓
STAGE 6: Epic-Level Final QC
    ├─ Epic smoke testing (from epic_smoke_test_plan.md)
    ├─ Epic QC rounds
    ├─ Epic PR review
    ├─ End-to-end validation vs epic request
    └─ Bug fixes for any issues
    ↓
STAGE 7: Epic Cleanup
    ├─ Final commits
    └─ Move epic to done/
```

---

## Cross-Stage Dependencies

**CRITICAL:** Stages have dependencies. Do NOT start a stage until its prerequisites are met.

| Stage | Cannot Start Until... | Blocking On... | Provides To... |
|-------|----------------------|----------------|----------------|
| **1** | Epic request (.txt file) exists | User creates epic request | Stage 2 (epic folder, feature folders, initial test plan) |
| **2** | Stage 1 complete:<br>- Epic folder created<br>- All feature folders created<br>- Initial test plan drafted | Stage 1 completion | Stage 3 (all feature specs for comparison) |
| **3** | ALL Stage 2 deep dives complete:<br>- Every feature has spec.md<br>- Every checklist resolved | ALL features planned | Stage 4 (aligned specs, user sign-off) |
| **4** | Stage 3 complete:<br>- User signed off on specs<br>- No unresolved conflicts | Stage 3 user approval | Stage 5 (updated test plan, success criteria) |
| **5a** | Stage 4 complete:<br>- Specs finalized<br>- Test plan updated | Stage 4 completion | Stage 5b (TODO with 24 iterations verified) |
| **5b** | Stage 5a complete:<br>- 24 iterations passed<br>- Iteration 23a: ALL 4 PARTS PASSED<br>- Iteration 24: READY TO IMPLEMENT | Stage 5a verification | Stage 5c (implementation code) |
| **5c** | Stage 5b complete:<br>- All TODO tasks done<br>- All tests passing (100%) | Stage 5b implementation | Stage 5d (QC-passed feature) |
| **5d** | Stage 5c complete:<br>- Smoke testing passed<br>- QC rounds 1,2,3 passed<br>- PR review passed | Stage 5c QC | Stage 5e (updated feature specs) |
| **5e** | Stage 5d complete:<br>- Remaining specs updated | Stage 5d alignment | Next feature's Stage 5a (updated test plan) |
| **6** | ALL features complete Stage 5e:<br>- No pending features<br>- No pending bug fixes | ALL features done | Stage 7 (epic QC passed) |
| **7** | Stage 6 complete:<br>- Epic smoke testing passed<br>- Epic QC passed<br>- Epic PR review passed | Stage 6 epic QC | done/ folder (completed epic) |

**Key Rules:**

1. **Stage 2 is per-feature, must complete ALL before Stage 3**
   - Don't start Stage 3 after completing first feature's deep dive
   - Wait until ALL features have completed deep dives

2. **Stage 3 requires user sign-off before Stage 4**
   - Agent cannot proceed without explicit user approval
   - User reviews aligned specs and approves plan

3. **Stage 5 is per-feature, loops sequentially**
   - Complete 5a→5b→5c→5d→5e for Feature 1
   - Then start 5a→5b→5c→5d→5e for Feature 2
   - Do NOT implement multiple features in parallel

4. **Stage 5a cannot start without Stage 4 complete**
   - Even though Stage 5 is per-feature, FIRST feature needs Stage 4 done
   - Test plan must be finalized before ANY implementation

5. **Stage 5c RESTART breaks the flow**
   - If ANY issues in smoke/QC/PR review → restart 5c completely
   - Do NOT proceed to 5d until 5c passes cleanly
   - Restart means re-run smoke testing, QC 1, QC 2, QC 3, PR review

6. **Stage 6 cannot start if ANY feature incomplete**
   - Check epic EPIC_README.md for feature completion status
   - Verify all features show "Stage 5e complete"
   - Verify no pending bug fixes

**Common Mistakes:**

❌ **Starting Stage 3 after first feature deep dive** → Wait for ALL features
❌ **Starting Stage 5a before Stage 4 complete** → Test plan must be updated first
❌ **Proceeding to Stage 5d after fixing Stage 5c issues** → Must RESTART 5c completely
❌ **Starting Stage 6 with incomplete features** → ALL features must complete 5e
❌ **Skipping user sign-off in Stage 3** → User MUST approve before Stage 4

**Dependency Check Protocol:**

Before starting ANY stage, verify:
1. Check the dependency table above
2. Verify "Cannot Start Until..." conditions are met
3. Check README Agent Status for completion markers
4. If unsure, READ the epic EPIC_README.md

---

## Migration Strategy (V1 → V2)

### For In-Progress Epics Using V1
1. **Identify current state** in v1 workflow
2. **Map to v2 stage**:
   - V1 Planning Phase → V2 Stages 1-4 (epic planning, deep dives, sanity check, testing strategy)
   - V1 TODO Creation → V2 Stage 5a
   - V1 Implementation → V2 Stage 5b
   - V1 Post-Implementation → V2 Stage 5c (add PR review)
3. **Restructure files** if needed (rename sub-features → features)
4. **Create epic README** if missing
5. **Continue with v2 workflow** from mapped stage

### For New Epics
- Start fresh with v2 guides
- No legacy constraints

---

## Success Criteria for V2 Guides

### Clarity
- ✅ Clear terminology (Epic → Features, no confusion)
- ✅ One guide per stage (no overlapping guides)
- ✅ Obvious next steps at each transition

### Manageability
- ✅ Epic-level tracking shows high-level progress
- ✅ Features can be worked on one at a time
- ✅ No 800+ checkpoint trackers
- ✅ Simple status updates (spec done? feature done?)

### Flexibility
- ✅ New features can be added during deep dives
- ✅ Bug fixes have clear workflow
- ✅ Epic plan adapts to discovery

### Quality
- ✅ Cross-feature alignment checks prevent conflicts
- ✅ PR review checklist catches issues QC misses
- ✅ Restart protocol ensures high quality
- ✅ Epic-level final QC validates end-to-end

### Continuous Improvement
- ✅ Lessons learned applied after each feature (not waiting for epic completion)
- ✅ Guides updated incrementally
- ✅ Process improves throughout the epic

---

## Next Steps

1. **Create guide files** (15 guides total)
2. **Create template files** (epic and feature templates)
3. **Create prompt references** (stage transitions)
4. **Test v2 workflow** on a small epic
5. **Iterate based on feedback**
6. **Migrate v1 to v2** once validated

---

## Resolved Decisions

✅ **Bug fix folder structure** (Resolved)
- Bug fixes live inside the epic folder as `bugfix_{priority}_{name}/`
- Priority levels: `high`, `medium`, `low`
- Keeps all related work together for epic-level integration testing
- Easier to manage without moving files back from done/ folder

✅ **Epic smoke test plan granularity** (Resolved)
- **Hybrid approach**: Combination of specific commands/scenarios AND high-level categories
- **Specific commands/scenarios**: Concrete, predefined tests that should always be run
  - Example: `python run_feature.py --mode test --iterations 5`
  - Example: "Verify all 6 position files are created in data/player_data/"
- **High-level categories**: Flexible areas where agent creates new scenarios as needed
  - Example: "Cross-feature integration testing" (agent determines specific tests during Stage 5e/6)
  - Example: "Error handling validation" (agent creates scenarios based on actual implementation)
- **Benefits**:
  - Provides concrete structure and known critical tests
  - Allows flexibility for agent to adapt tests based on actual implementation
  - Tests evolve with epic (Stages 4, 5e) while maintaining core validation

✅ **Lessons learned structure** (Resolved)
- **Both per-feature AND epic-level**
- **Per-feature**: `feature_{N}_{name}/lessons_learned.md`
  - Captures issues specific to that feature's implementation
  - Documents feature-specific insights and gotchas
- **Epic-level**: `epic_lessons_learned.md` (in epic root folder)
  - Captures cross-feature patterns and systemic issues
  - Documents epic-wide insights applicable to all features
  - Aggregates common themes from individual feature lessons
- **Benefits**:
  - Feature-level lessons inform that feature's implementation and similar features
  - Epic-level lessons identify systemic patterns to update guides
  - Prevents duplication while maintaining granularity

✅ **Guide update timing** (Resolved)
- **After each feature completion** (incremental updates)
- Timing: During Stage 5c (post-implementation), after lessons learned review
- Process:
  1. Review feature's lessons_learned.md
  2. Identify guide improvements needed
  3. Update relevant guides immediately
  4. Document changes in epic_lessons_learned.md
- **Benefits**:
  - Guides improve throughout epic (not waiting until end)
  - Later features benefit from earlier features' lessons
  - Continuous process improvement
  - Prevents forgetting insights discovered weeks ago

---

## Critical Details from V1 to Carry Over

**IMPORTANT:** The following protocols and details from v1 guides are ESSENTIAL and MUST be included in v2 guides. These represent lessons learned from 40% QC failure rates and production bugs.

### Stage 5a: TODO Creation Guide - Critical Protocols

**24 Verification Iterations (MANDATORY - NO SKIPPING)**

The v2 todo_creation_guide.md MUST include:

1. **Algorithm Traceability Matrix** (Iterations 4, 11, 19)
   - Map every algorithm in spec to exact code location
   - Quote exact spec text → verify exact code match
   - Typical matrix has 40+ mappings
   - Prevents implementing wrong algorithm

2. **TODO Specification Audit** (Iteration 4a)
   - Verify EVERY TODO task has acceptance criteria
   - No vague tasks like "implement feature"
   - Each task must be verifiable
   - Example: "Create player_stats.json with fields: name, position, points (NOT just 'create JSON file')"

3. **Pre-Implementation Spec Audit** (Iteration 23a - 4-part audit)
   - Part 1: Completeness (all requirements have tasks)
   - Part 2: Specificity (all tasks have concrete acceptance criteria)
   - Part 3: Interface Contracts (all method signatures verified against source)
   - Part 4: Integration Evidence (all new methods have identified callers)
   - **MUST show "ALL 4 PARTS PASSED"** before proceeding to implementation

4. **Mock Audit** (Iteration 21)
   - List all mocked dependencies
   - Verify EACH mock matches real interface (read actual source code)
   - Check for over-mocking (mocks that accept ANY arguments won't catch bugs)
   - Plan at least one integration test with REAL objects (not mocks)
   - **Critical lesson:** Unit tests with wrong mocks can pass while hiding bugs

5. **Integration Gap Check** (Iterations 7, 14, 23)
   - For EVERY new method: identify caller
   - No orphan code (methods with no callers)
   - Trace execution path: CLI → new method → output
   - **Critical rule:** "If nothing calls it, it's not integrated"

6. **End-to-End Data Flow** (Iteration 5, 12)
   - Trace data from entry point → through all transformations → to output
   - Identify where data is created, modified, consumed
   - Prevents "data exists but wrong format" bugs

7. **Output Consumer Validation** (Iteration 21)
   - Identify ALL consumers of feature's outputs
   - Plan roundtrip tests: Create output → Load with REAL consumer → Verify usable
   - **Example:** If feature creates JSON, test loading JSON with actual consuming code
   - Prevents "output structure correct but unusable" bugs

8. **Interface Verification Protocol** (Before implementation)
   - For EVERY external dependency: READ actual source code
   - COPY-PASTE exact method signatures (don't rely on memory)
   - Verify parameter names, types, return values
   - Check existing usage patterns in codebase
   - **Critical rule:** "Never assume interface - always verify"

**Why these matter:** Historical evidence shows skipping iterations leads to 40% QC failure rate. Each protocol catches specific bug categories that slip through other checks.

---

### Stage 5b: Implementation Execution Guide - Critical Protocols

**Continuous Spec Verification (MANDATORY)**

The v2 implementation_execution_guide.md MUST emphasize:

1. **Keep specs.md VISIBLE at all times**
   - Not just "consult when needed"
   - Literally open in editor while coding
   - Check every 5-10 minutes: "Did I consult specs recently?"

2. **Dual verification for EVERY requirement**
   - BEFORE implementing: Read requirement in spec
   - AFTER implementing: Verify code matches spec
   - Update implementation_checklist.md in real-time

3. **Mini-QC Checkpoints** (After each major phase)
   - Not same as final QC - lightweight validation during implementation
   - Verify: Tests pass, spec requirements met, no regressions
   - **Critical rule:** "Fix issues NOW, not during final QC"

4. **Implementation Checklist** (Continuous tracking)
   - Create from TODO requirements
   - Check off requirements AS YOU IMPLEMENT (not batched at end)
   - Prevents "forgot to implement requirement X"

5. **Configuration Change Checkpoint** (When config.py or league_config.json modified)
   - Special protocol for config changes
   - Verify backward compatibility
   - Check all consumers of config
   - Document migration path

6. **No Coding from Memory**
   - **Critical mistake:** "I remember what the spec said"
   - Memory degrades in minutes
   - Always consult actual spec text before coding
   - Historical evidence: Memory-based coding leads to spec violations

**Why these matter:** Implementation without continuous verification caused 10 critical bugs that passed 2,296 unit tests. Continuous verification catches issues immediately (not after QC).

---

### Stage 5c: Post-Implementation Guide - Critical Protocols

**Smoke Testing Protocol (3 Parts - MANDATORY GATE)**

The v2 post_implementation_guide.md MUST include detailed smoke testing:

1. **Part 1: Import Test**
   ```bash
   python -c "import new.module"
   ```
   - Verifies module loads without errors
   - Catches: Import errors, circular dependencies, missing dependencies

2. **Part 2: Entry Point Test**
   ```bash
   python run_feature.py --help
   python run_feature.py --invalid-arg  # Should error gracefully
   ```
   - Verifies script starts correctly
   - Catches: Argument parsing errors, initialization crashes

3. **Part 3: E2E Execution Test**
   ```bash
   python run_feature.py --mode test  # Or actual execution
   ```
   - Execute feature end-to-end with REAL data
   - Verify outputs created AND contain correct data
   - **Critical distinction:** Not just "file exists" - verify FILE CONTENT is correct
   - Catches: Data quality issues, integration bugs, mock assumption failures

**Why smoke testing is critical:** Real-world case: Feature passed 2,369 unit tests (100%) but smoke testing revealed output files missing 80% of required data. **Mocks test expectations, not reality.**

**Requirement Verification Protocol**

1. **NO PARTIAL WORK ACCEPTED**
   - ❌ "File structure correct but data pending"
   - ❌ "Method exists but returns placeholder values"
   - ❌ "Stat arrays created but filled with zeros"
   - **Rule:** If feature cannot achieve primary use case, it's INCOMPLETE

2. **Data Quality Verification** (Not just structure)
   - Verify OUTPUT DATA VALUES are correct (not just fields exist)
   - Example: If spec says "player passing yards", verify actual yards (not zeros)
   - Check value ranges (no negative yards, no impossibly high values)
   - **Critical lesson:** Structure can be perfect while data is completely wrong

3. **Output Location Verification**
   - Verify outputs created in EXACT location specified in spec
   - Verify file names match spec exactly
   - Verify all expected outputs exist (count files)

**QC Restart Protocol**

- **CRITICAL RULE:** If ANY issues found in smoke testing, QC rounds, or PR review:
  - ❌ Do NOT just fix and continue
  - ✅ Fix issues THEN **COMPLETELY RESTART POST-IMPLEMENTATION**
  - Re-run smoke testing (Part 1, 2, 3)
  - Re-run QC Round 1 (fresh review)
  - Re-run QC Round 2 (deep verification)
  - Re-run QC Round 3 (skeptical review)
  - Re-run PR Review (11 categories)

**Why restart matters:** Fixes can introduce new bugs. Full restart ensures complete validation.

**3 QC Rounds (Detailed Focus)**

The v2 guide MUST detail what each round focuses on:

1. **QC Round 1: Basic Validation**
   - All unit tests pass (100% required)
   - Code matches spec structurally
   - Tests use real objects (not excessive mocking)
   - Output file tests validate CONTENT (not just existence)
   - Runner scripts tested with --help AND E2E
   - Test ALL execution modes (not just --help)
   - Interfaces verified against actual classes

2. **QC Round 2: Deep Verification**
   - Baseline comparison (if similar feature exists)
   - Output validation (values in expected range, no zeros/nulls where data expected)
   - No regressions (new feature doesn't break existing)
   - Log quality (no unexpected WARNING/ERROR in logs)
   - Semantic diff check (intentional vs accidental changes)
   - Edge cases handled
   - Error handling complete
   - Documentation matches implementation

3. **QC Round 3: Final Skeptical Review**
   - Re-read specs.md with fresh eyes
   - Re-read question answers
   - Re-check Algorithm Traceability Matrix
   - Re-check Integration Matrix
   - Re-run smoke test final time
   - Compare final output to test plan in specs
   - Final question: "Is feature actually complete and working?"

**Pass Criteria:**
- Round 1: <3 critical issues, >80% requirements met
- Round 2: All Round 1 findings resolved
- Round 3: Zero issues found (skeptical fresh review)

---

### Session Continuity: README Agent Status

**CRITICAL for context window limits**

All v2 guides MUST include README.md Agent Status update requirements:

**Purpose:** When session compaction occurs or agents switch, Agent Status is the ONLY way to resume work correctly.

**Mandatory Update Points:**
- After each TODO round (iterations 1-7, 8-16, 17-24)
- After smoke testing complete
- After each QC round (1, 2, 3)
- When blocked on an issue
- Before ending session (if work in progress)
- After each feature in Stage 5 (before Stage 5d, 5e)

**Template:**
```markdown
## Agent Status

**Last Updated:** {YYYY-MM-DD HH:MM}
**Current Phase:** {PLANNING/TODO_CREATION/IMPLEMENTATION/POST_IMPLEMENTATION}
**Current Step:** {Specific step name}
**Progress:** {X/Y items complete}
**Next Action:** {Exact next task to do}
**Blockers:** {Issues or "None"}
**Notes:**
- {Relevant status details}
```

**Why critical:** Session compaction mid-workflow loses context. Agent Status provides persistent state that survives context limits.

---

### Additional Critical Details

**Test-First Workflow** (When possible)

Include in v2 implementation_execution_guide.md:

1. Write failing test BEFORE implementation
2. Run test - confirm it fails (red)
3. Implement code to make test pass
4. Run test - confirm it passes (green)
5. Refactor if needed, keeping tests green

**Benefits:**
- Forces thinking about behavior before code structure
- Creates behavior tests (not structure tests)
- Catches "tests pass but behavior wrong"
- Documents expected behavior

**Configuration Change Protocol**

Include in v2 implementation_execution_guide.md:

When modifying config.py or league_config.json:
1. Verify backward compatibility
2. Check ALL consumers of config
3. Document migration path
4. Add validation for new config fields
5. Update config tests

**Baseline Comparison Protocol**

Include in v2 post_implementation_guide.md (QC Round 2):

If similar feature exists in codebase:
1. Identify similar feature
2. Compare file structure
3. Compare data format
4. Compare integration patterns
5. Document intentional differences
6. Verify new feature matches codebase patterns

**Semantic Diff Check**

Include in v2 post_implementation_guide.md (QC Round 2):

Review git diff:
1. **Intentional changes:** Expected from feature implementation
2. **Accidental changes:** Formatting, whitespace, unrelated code
3. Flag accidental changes for cleanup
4. Verify no unintended side effects

**Log Quality Verification**

Include in v2 post_implementation_guide.md (QC Round 2):

Run feature and check logs:
1. No unexpected WARNING messages
2. No ERROR messages (unless testing error paths)
3. Log messages are helpful (not cryptic)
4. No excessive logging (log spam)
5. Sensitive data not logged

---

## Additional Improvements for V2

**Based on v1 experience, these improvements should be added:**

### 1. Session Handoff Protocol (NEW)

**Problem:** V1 didn't handle context window limits explicitly

**Solution:** Add to ALL v2 guides:
- Update README Agent Status BEFORE hitting token limits
- Document exact next step in "Next Action" field
- List any blockers or pending decisions
- Commit WIP code with descriptive message
- Note which files are mid-edit

### 2. Cross-Phase Dependencies (NEW)

**Problem:** V1 guides treated phases as independent

**Solution:** Add dependency maps to v2 guides:
- TODO creation depends on: Complete specs, checklist, interface verification
- Implementation depends on: 24 iterations complete, interfaces verified
- Post-implementation depends on: All TODO tasks complete, tests passing

### 3. Confidence Tracking (NEW)

**Problem:** V1 agents proceeded with low confidence leading to wrong implementations

**Solution:** Add confidence checkpoints:
- After each TODO iteration: Rate confidence (High/Medium/Low)
- If confidence is LOW: STOP, create question, wait for answer
- Never proceed with <Medium confidence
- Document confidence level in TODO

### 4. Anti-Pattern Detection (NEW - from protocols/anti_patterns.md)

**Include in v2 guides:**

Common anti-patterns agents fall into:
- "I remember the spec" → Consult actual spec now
- "Tests pass so it's right" → Verify against specs
- "I'll verify during QC" → Verify NOW
- "This is simple, skip iterations" → Execute all iterations anyway
- "Low confidence is fine" → STOP, resolve uncertainty first

**Add "If you're thinking this, STOP" sections to guides**

### 5. Verification Failure Protocol (NEW)

**From protocols/verification_failure.md:**

When verification fails:
1. Document exact failure
2. Root cause analysis (why did verification fail?)
3. Fix the issue (code or spec)
4. Re-run verification
5. Update lessons learned
6. Consider guide updates

**Don't just "fix and move on" - understand WHY verification failed**

---

## Guide Structure Recommendations

**Based on v1 structure, v2 guides should include:**

### Every guide should have:
1. **Quick Start** (5 steps or less)
2. **Quick Reference Checklist** (visual workflow)
3. **Critical Rules** (boxed, prominent)
4. **Common Shortcuts to Avoid** (with consequences)
5. **Prerequisites Checklist** (verify before starting)
6. **README Agent Status Requirements** (when to update)
7. **"If you're thinking this, STOP" sections** (anti-patterns)
8. **Real-world examples** (good vs bad)

### Visual Elements:
- Box important rules with ┌─────┐ borders
- Use ⚠️ for critical warnings
- Use ✅/❌ for do/don't examples
- Use 🔄 for checkpoint reminders
- Use ⚡ for status update requirements

### Length:
- Quick Reference: 1-2 pages
- Full Guide: As detailed as needed
- NO guide should say "see other guide for details" without providing summary

---

## Guide Adherence Strategy (Preventing "Off-Script" Behavior)

**CRITICAL PROBLEM:** V1 agents frequently stopped following guides after session compaction, leading to skipped steps, wrong workflows, and quality failures.

**ROOT CAUSES:**
1. Session compaction removes guide context from working memory
2. No enforcement mechanism to ensure guide is loaded
3. Agents default to "common sense" instead of documented process
4. No verification that agent actually read the guide
5. Guide references get buried in conversation history

### Solution: Multi-Layer Guide Enforcement

**Layer 1: Mandatory Guide Reading Protocol**

Add to EVERY phase transition in CLAUDE.md and guides:

```markdown
🚨 MANDATORY BEFORE PROCEEDING:

1. **READ the guide file**: `feature-updates/guides_v2/{guide_name}.md`
   - You MUST use the Read tool to load the COMPLETE guide
   - Reading the guide is NOT optional
   - Do NOT proceed from memory or assumptions

2. **ACKNOWLEDGE what you read**: State out loud:
   "I have read {guide_name}.md. The guide requires:
   - [List 3-5 critical requirements from the guide]
   - [List any mandatory checkpoints or iterations]
   - [Note any STOP conditions or blockers]"

3. **VERIFY prerequisite completion**:
   - Check all prerequisites from guide's "Prerequisites Checklist"
   - Do NOT start this phase if prerequisites incomplete
   - Document prerequisite verification in README Agent Status

4. **ONLY THEN proceed** with the phase

❌ NEVER say: "I'm familiar with the process" or "I remember the steps"
✅ ALWAYS: Read the actual guide file, acknowledge requirements, verify prerequisites
```

**Enforcement in CLAUDE.md:**

Add to feature-updates workflow section:

```markdown
## 🚨 CRITICAL RULE: Guide Reading Protocol

**BEFORE starting ANY phase (Stage 1-7, or sub-stages 5a-5e):**

1. ✅ **MUST READ** the guide file using Read tool
2. ✅ **MUST ACKNOWLEDGE** 3-5 critical requirements from guide
3. ✅ **MUST VERIFY** prerequisites complete
4. ✅ **MUST UPDATE** README Agent Status with guide name and acknowledgment

**This is MANDATORY, not optional.**

If you find yourself thinking:
- "I know what to do" → STOP, read the guide
- "I remember the process" → STOP, read the guide
- "This is similar to before" → STOP, read the guide
- "Let me just start quickly" → STOP, read the guide

**After session compaction:** The FIRST action is to check README Agent Status for current phase, then READ the corresponding guide.
```

---

**Layer 2: Guide Summary in README Agent Status**

Modify Agent Status template to include guide adherence:

```markdown
## Agent Status

**Last Updated:** {YYYY-MM-DD HH:MM}
**Current Phase:** {PLANNING/TODO_CREATION/etc}
**Current Step:** {Specific step name}
**Current Guide:** {guide_file_name.md}
**Guide Last Read:** {YYYY-MM-DD HH:MM}
**Critical Rules from Guide:**
- {Rule 1 - e.g., "24 iterations mandatory, no skipping"}
- {Rule 2 - e.g., "Update Agent Status after each round"}
- {Rule 3 - e.g., "STOP if confidence < Medium"}

**Progress:** {X/Y items complete}
**Next Action:** {Exact next task + guide reference}
**Blockers:** {Issues or "None"}
```

**Why this works:** After session compaction, Agent Status is the ONLY persistent context. Including guide name + critical rules keeps them visible.

---

**Layer 3: Quick Reference Card in Epic README**

Every epic's EPIC_README.md should include at top:

```markdown
# Epic: {epic_name}

## 🎯 Quick Reference Card (Always Visible)

**Current Stage:** Stage X - {stage name}
**Active Guide:** `guides_v2/{guide_name}.md`
**Last Guide Read:** {timestamp}

**Stage Workflow:**
Stage 1 → Stage 2 → Stage 3 → Stage 4 → Stage 5 → Stage 6 → Stage 7
  ↓         ↓         ↓         ↓         ↓         ↓         ↓
Epic    Features  Sanity   Testing   Impl     Epic      Done
Plan    Deep Dive  Check   Strategy  (5a-5e)  QC

**You are here:** ➜ Stage {X}

**Critical Rules for Current Stage:**
1. {Rule 1}
2. {Rule 2}
3. {Rule 3}

**Before Proceeding to Next Step:**
□ Read guide: `guides_v2/{current_guide}.md`
□ Acknowledge critical requirements
□ Verify prerequisites
□ Update this Quick Reference Card

---

[Rest of README...]
```

**Why this works:** Quick Reference Card is at TOP of README (most likely to survive compaction). Visual workflow shows where we are.

---

**Layer 4: Periodic Guide Re-Reading Checkpoints**

Add to all Stage 5 guides (TODO creation, implementation, post-implementation):

```markdown
## 🔄 Mandatory Re-Reading Checkpoints

**CHECKPOINT 1:** After completing Round 1 (or Phase 1, or QC Round 1)
- Re-read "Critical Rules" section of this guide
- Verify you're still following all mandatory protocols
- Update README Agent Status with re-read timestamp

**CHECKPOINT 2:** After completing Round 2 (or Phase 2, or QC Round 2)
- Re-read "Common Shortcuts to Avoid" section
- Confirm you haven't fallen into any anti-patterns
- Update README Agent Status

**CHECKPOINT 3:** Before declaring complete
- Re-read "Completion Criteria" section
- Verify ALL criteria met (not just most)
- Re-read "Prerequisites for Next Phase"

**Why this matters:** Memory degrades. Re-reading keeps you aligned with documented process.
```

---

**Layer 5: Guide Comprehension Verification**

Add verification questions at start of critical phases:

**In todo_creation_guide.md:**

```markdown
## Guide Comprehension Verification

Before starting TODO creation, answer these questions (proves you read the guide):

1. How many verification iterations are MANDATORY? {Answer: 24}
2. What happens at Iteration 4a? {Answer: TODO Specification Audit}
3. What must Iteration 23a show before proceeding? {Answer: ALL 4 PARTS PASSED}
4. If confidence is LOW, what should you do? {Answer: STOP, create question, wait for answer}
5. What is the QC failure rate for skipping iterations? {Answer: 40%}

**Document your answers in README Agent Status** to prove guide comprehension.

If you cannot answer these questions without re-reading the guide, you haven't read it carefully enough.
```

**Why this works:** Forces active reading. Agent must engage with guide content to answer questions. Answers in Agent Status prove comprehension.

---

**Layer 6: CLAUDE.md Phase Transition Enforcement**

Update the feature-updates workflow section in CLAUDE.md:

```markdown
## 🚨 Phase Transition Protocol (MANDATORY)

**EVERY TIME** you transition between phases or stages:

1. **Identify transition:**
   - Starting Stage 1? → Read STAGE_1_epic_planning_guide.md
   - Starting Stage 2? → Read STAGE_2_feature_deep_dive_guide.md
   - Starting Stage 3? → Read STAGE_3_cross_feature_sanity_check_guide.md
   - Starting Stage 4? → Read STAGE_4_epic_testing_strategy_guide.md
   - Starting Stage 5a Round 1? → Read STAGE_5aa_round1_guide.md
   - Starting Stage 5a Round 2? → Read STAGE_5ab_round2_guide.md
   - Starting Stage 5a Round 3? → Read STAGE_5ac_round3_guide.md
   - Starting Stage 5b? → Read STAGE_5b_implementation_execution_guide.md
   - Starting Stage 5c Smoke Testing? → Read STAGE_5ca_smoke_testing_guide.md
   - Starting Stage 5c QC Rounds? → Read STAGE_5cb_qc_rounds_guide.md
   - Starting Stage 5c Final Review? → Read STAGE_5cc_final_review_guide.md
   - Starting Stage 5d? → Read STAGE_5d_post_feature_alignment_guide.md
   - Starting Stage 5e? → Read STAGE_5e_post_feature_testing_update_guide.md
   - Starting Stage 6? → Read STAGE_6_epic_final_qc_guide.md
   - Starting Stage 7? → Read STAGE_7_epic_cleanup_guide.md

2. **Use Read tool** to load the ENTIRE guide

3. **Use phase transition prompt** from prompts_reference_v2.md
   - Find the appropriate "Starting {Phase Name}" prompt
   - Speak it out loud (acknowledge requirements)
   - List critical requirements from guide

4. **Update README Agent Status**:
   - Current Guide: {guide_name}
   - Guide Last Read: {timestamp}
   - Critical Rules from Guide: {list 3-5}

5. **Verify prerequisites** from guide's checklist

6. **THEN AND ONLY THEN** proceed with the phase

**NEVER skip this protocol.** It takes 2-3 minutes but prevents hours of rework.

**After session compaction:**
- First action: Read README Agent Status
- Second action: Identify current phase/stage
- Third action: READ THE GUIDE for that phase/stage
- Fourth action: Continue where previous agent left off
```

---

**Layer 7: Guide Anchors (Keep in Context)**

Create a `GUIDE_ANCHOR.md` file in each epic folder:

```markdown
# GUIDE ANCHOR - READ THIS AFTER SESSION COMPACTION

**If you're resuming work on this epic after session compaction:**

1. **You are in:** {epic_name}
2. **Read FIRST:** `EPIC_README.md` (especially "Agent Status" and "Quick Reference Card")
3. **Current Stage:** Stage {X} - {name}
4. **Active Guide:** `feature-updates/guides_v2/{guide_name}.md`
5. **You MUST read the active guide before continuing**

**Do NOT:**
- ❌ Assume you know what to do
- ❌ Continue from memory
- ❌ Skip reading the guide
- ❌ Use "common sense" instead of documented process

**DO:**
- ✅ Read EPIC_README.md Agent Status
- ✅ Read the active guide (use Read tool)
- ✅ Acknowledge critical requirements from guide
- ✅ Verify prerequisites before proceeding
- ✅ Update Agent Status after reading guide

**Critical Workflow Reference:**

Stage 1: Epic Planning (STAGE_1_epic_planning_guide.md)
  ↓
Stage 2: Feature Deep Dives (STAGE_2_feature_deep_dive_guide.md) - Loop per feature
  ↓
Stage 3: Cross-Feature Sanity Check (STAGE_3_cross_feature_sanity_check_guide.md)
  ↓
Stage 4: Epic Testing Strategy (STAGE_4_epic_testing_strategy_guide.md)
  ↓
Stage 5: Feature Implementation (Loop per feature)
  5a: TODO Creation
      - Round 1 (STAGE_5aa_round1_guide.md)
      - Round 2 (STAGE_5ab_round2_guide.md)
      - Round 3 (STAGE_5ac_round3_guide.md)
  5b: Implementation (STAGE_5b_implementation_execution_guide.md)
  5c: Post-Implementation
      - Smoke Testing (STAGE_5ca_smoke_testing_guide.md)
      - QC Rounds (STAGE_5cb_qc_rounds_guide.md)
      - Final Review (STAGE_5cc_final_review_guide.md)
  5d: Cross-Feature Alignment (STAGE_5d_post_feature_alignment_guide.md)
  5e: Testing Plan Update (STAGE_5e_post_feature_testing_update_guide.md)
  ↓
Stage 6: Epic Final QC (STAGE_6_epic_final_qc_guide.md)
  ↓
Stage 7: Epic Cleanup (STAGE_7_epic_cleanup_guide.md)

**Find current stage in Agent Status → Read corresponding guide**
```

**Why this works:** Explicit instructions for post-compaction resumption. Visual workflow makes it obvious which guide to read.

---

**Layer 8: Guide Deviation Detection**

Add to templates_v2.md for README.md:

```markdown
## Guide Deviation Log

**Purpose:** Track when agent deviates from guide (helps identify guide gaps)

| Timestamp | Phase | Deviation | Reason | Impact |
|-----------|-------|-----------|--------|--------|
| 2025-12-30 14:23 | Stage 5a | Skipped iteration 12 | "Seemed redundant" | QC failed, rework required |
| {timestamp} | {phase} | {what was skipped/changed} | {why} | {consequence} |

**Rule:** If you deviate from guide, DOCUMENT IT HERE immediately.
**Post-Implementation:** Review this log during lessons learned.
```

**Why this works:** Makes deviations explicit and traceable. Helps identify guide improvements.

---

## Implementation in V2 Guides

**Every v2 guide MUST include:**

1. **At the very top (before Quick Start):**
   ```markdown
   # {Guide Name}

   🚨 **MANDATORY READING PROTOCOL**

   **Before starting this phase:**
   1. Use Read tool to load THIS ENTIRE GUIDE
   2. Acknowledge critical requirements (see "Critical Rules" section)
   3. Verify prerequisites (see "Prerequisites Checklist" section)
   4. Update README Agent Status with guide name + timestamp

   **DO NOT proceed without reading this guide.**

   **After session compaction:**
   - Check README Agent Status for current phase
   - READ THIS GUIDE again (full guide, not summary)
   - Continue from "Next Action" in Agent Status
   ```

2. **Critical Rules section (boxed, prominent):**
   - List 5-10 CRITICAL rules that MUST be followed
   - These get copied to README Agent Status
   - Use visual markers (⚠️, ❌, ✅)

3. **Prerequisites Checklist:**
   - Must verify BEFORE starting phase
   - Includes file existence checks
   - Includes completion status checks

4. **Periodic Re-Reading Checkpoints:**
   - After major milestones within the phase
   - Re-read specific sections to stay aligned

5. **Completion Criteria:**
   - Clear, verifiable checklist
   - No ambiguity about when phase is done

---

## Guide File Naming Convention

To make it OBVIOUS which guide to read:

```
guides_v2/
├── STAGE_1_epic_planning_guide.md
├── STAGE_2_feature_deep_dive_guide.md
├── STAGE_3_cross_feature_sanity_check_guide.md
├── STAGE_4_epic_testing_strategy_guide.md
├── STAGE_5aa_round1_guide.md
├── STAGE_5ab_round2_guide.md
├── STAGE_5ac_round3_guide.md
├── STAGE_5b_implementation_execution_guide.md
├── STAGE_5ca_smoke_testing_guide.md
├── STAGE_5cb_qc_rounds_guide.md
├── STAGE_5cc_final_review_guide.md
├── STAGE_5d_post_feature_alignment_guide.md
├── STAGE_5e_post_feature_testing_update_guide.md
├── STAGE_5_bug_fix_workflow_guide.md
├── STAGE_6_epic_final_qc_guide.md
├── STAGE_7_epic_cleanup_guide.md
├── templates_v2.md
├── prompts_reference_v2.md
└── README.md
```

**Why this works:** File name includes STAGE number. Agent can't be confused about which guide to use.

---

## Enforcement Checklist for V2

When creating v2 guides, verify each guide includes:

□ "MANDATORY READING PROTOCOL" at top
□ Phase transition prompt from prompts_reference_v2.md referenced
□ Critical Rules section (5-10 rules, boxed)
□ Prerequisites Checklist
□ README Agent Status update requirements (when to update)
□ Periodic re-reading checkpoints
□ Guide comprehension verification questions
□ Completion criteria (clear, verifiable)
□ "If you're thinking this, STOP" anti-pattern sections
□ Real-world examples (good vs bad)

---

## Summary: Multi-Layer Defense Against Guide Abandonment

**Layer 1:** Mandatory reading protocol at phase start
**Layer 2:** Guide summary in README Agent Status (survives compaction)
**Layer 3:** Quick Reference Card at top of epic README
**Layer 4:** Periodic re-reading checkpoints within phases
**Layer 5:** Guide comprehension verification questions
**Layer 6:** CLAUDE.md phase transition enforcement
**Layer 7:** GUIDE_ANCHOR.md for post-compaction resumption
**Layer 8:** Guide deviation log (tracks when agent goes off-script)

**Result:** Agent CANNOT proceed without reading guide. Guide adherence is enforced at multiple levels. Session compaction doesn't cause guide abandonment because guide name + critical rules are in Agent Status.

---

*This plan will guide the creation of all v2 guide files and templates.*
