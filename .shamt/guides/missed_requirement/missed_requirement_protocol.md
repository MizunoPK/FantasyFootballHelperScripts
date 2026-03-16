# Missed Requirement Protocol (Router)

**Purpose:** Handle missing scope/requirements discovered after S5 begins by treating them as real features - either creating a new feature or updating an unstarted one - then temporarily returning to planning stages to maintain epic coherence.

**When to Use:** Missing requirement discovered at ANY point after first S5 starts - you know WHAT needs to be built (just forgot to include it in the original spec)

**When NOT to Use:**
- Unknown bugs requiring investigation - use debugging/debugging_protocol.md instead
- Missing scope discovered BEFORE any feature enters S5 - just update specs directly during S2/3/4

---

## Table of Contents

- [When to Use This Protocol vs Debugging Protocol](#🔀-when-to-use-this-protocol-vs-debugging-protocol)
- [Mandatory Reading Protocol](#🚨-mandatory-reading-protocol)
- [Quick Start](#quick-start)
- [Critical Rules](#🛑-critical-rules)
- [Missed Requirement Handling Phases (Overview)](#missed-requirement-handling-phases-overview)
- [File Structure](#file-structure)
- [Which Phase Should I Use?](#which-phase-should-i-use)
- [Common Scenarios](#common-scenarios)
- [Summary](#summary)

---

## 🔀 When to Use This Protocol vs Debugging Protocol

**Use MISSED REQUIREMENT PROTOCOL when:**
- ✅ Solution is KNOWN (you know what needs to be added)
- ✅ It's a NEW requirement (user didn't ask for it originally)
- ✅ User needs to confirm and prioritize

**Use DEBUGGING PROTOCOL when:**
- ✅ Solution is UNKNOWN (requires investigation)
- ✅ Root cause needs to be found
- ✅ Issue discovered during testing

**Quick Test:**
- If you can write a complete spec.md for the solution → Missed Requirement
- If you need to investigate why something isn't working → Debugging Protocol

**See:** CLAUDE.md → "Decision Tree: Which Protocol to Use?" for detailed decision tree with examples

---

## 🚨 MANDATORY READING PROTOCOL

**BEFORE handling a missed requirement, you MUST:**

1. **Use the phase transition prompt** from `prompts/special_workflows_prompts.md`
   - Find "Creating Missed Requirement" prompt
   - Acknowledge requirements

2. **Update README Agent Status** with:
   - Current Phase: MISSED_REQUIREMENT_HANDLING
   - Current Guide: missed_requirement/missed_requirement_protocol.md
   - Guide Last Read: {YYYY-MM-DD HH:MM}
   - Critical Rules: "Get user approval first", "Return to S2/3/4", "Update epic docs"
   - Next Action: Present options to user (new feature vs update unstarted)

3. **Get user approval** before creating/updating features

4. **THEN AND ONLY THEN** proceed with missed requirement handling

---

## Quick Start

**What is this protocol?**
Missed Requirement Protocol treats missing scope as real features - either creating new features or updating unstarted ones - then temporarily returning to S2/3/4 planning to maintain epic-level coherence before resuming implementation work.

**When do you use this protocol?**
- Missing requirement discovered at ANY point after first S5 starts:
  - During S5 (Implementation Planning)
  - During S6 (Implementation)
  - During S7 (QA - smoke testing, QC rounds)
  - During debugging protocol (while investigating issues)
  - During S9 (Epic-level testing)
  - During S10 (User testing)
- You KNOW what needs to be built (solution is clear, just wasn't in original spec)
- Need to add missing functionality as a proper feature
- Example: "We forgot to add item attribute status tracking"

**When NOT to use this protocol?**
- Unknown bugs requiring investigation (use debugging/debugging_protocol.md instead)
- Example: "Item scores are sometimes wrong but we don't know why"
- Missing scope discovered BEFORE any feature enters S5 (just update specs directly during S2/3/4)

**Key Outputs:**
- ✅ New feature created OR unstarted feature updated
- ✅ Feature spec fleshed out (S2)
- ✅ All features re-aligned (S3)
- ✅ Epic smoke test plan updated (S3.P1) + Test Scope Decision done at S5 Step 0 (S4 deprecated)
- ✅ Epic documentation updated for resumability
- ✅ Ready to resume previous work
- ✅ New/updated feature implemented when its turn comes in sequence

**Time Estimate:**
Varies by requirement complexity (1-3 hours for planning stages typical)

**Exit Condition:**
Missed requirement handling is complete when the new/updated feature has been planned (S2/3/4 complete), epic docs updated, and previous work resumed. The feature itself gets implemented later when its turn comes in the implementation sequence.

---

## 🛑 Critical Rules

```bash
1. ⚠️ CAN BE USED AT ANY TIME AFTER FIRST STAGE 5 STARTS
   - Before any feature enters S5: Just update specs directly during S2/3/4
   - After first feature enters S5: Use this protocol for epic coherence
   - Can be discovered during: Implementation, QA, debugging, epic testing, user testing
   - Maintains epic coherence through re-alignment

2. ⚠️ TWO OPTIONS: NEW FEATURE OR UPDATE UNSTARTED
   - Agent presents BOTH options to user
   - User decides which approach
   - If new feature: Decide sequence position
   - If update unstarted: Which feature to update

3. ⚠️ ALWAYS RETURN TO STAGE 2/3 (S4 deprecated)
   - S2: Flesh out new/updated feature spec
   - S3: Epic-Level Docs, Tests, and Approval (ALL features)
   - S4 deprecated — Test Scope Decision now in S5 Step 0 (check Testing Approach in EPIC_README)
   - Maintains epic-level alignment

4. ⚠️ SEQUENCE MATTERS FOR NEW FEATURES
   - High priority: Insert BEFORE current feature
   - Medium priority: Insert AFTER current feature
   - Low priority: Insert at END of feature list
   - Update Epic Progress Tracker with new sequence

5. ⚠️ UPDATE EPIC DOCS FOR RESUMABILITY
   - Document current work state before pausing
   - Update EPIC_README with missed requirement handling status
   - Add to Missed Requirement Tracking table
   - Future agent must know where to resume

6. ⚠️ FEATURE GETS IMPLEMENTED IN SEQUENCE
   - Don't implement immediately after planning
   - Resume paused work first
   - New/updated feature waits its turn
   - Implement when it comes up in Epic Progress Tracker

7. ⚠️ SAME RIGOR AS ALL FEATURES
   - Full S2 deep dive
   - Full S3 re-alignment (all features)
   - Full S4 test plan update
   - When implemented: Full S5 (S5 → S6 → S7 → S8)
   - No shortcuts
```

---

## Missed Requirement Handling Phases (Overview)

The missed requirement protocol consists of 4 phases (plus special case):

### PHASE 1: Discovery & User Decision
**See:** `missed_requirement/discovery.md`

**Purpose:** Identify missing requirement and get user decision on approach

**Key Activities:**
- Discover missing requirement (can happen during any stage after first S5)
- Present two options to user (create new feature OR update unstarted feature)
- Get user decision on approach
- Get user decision on priority/sequence (if new feature)
- Document paused work state

**Output:** User decision + paused work documented

---

### PHASE 2: Planning (S2 Deep Dive)
**See:** `missed_requirement/planning.md`

**Purpose:** Create/update feature spec through S2 deep dive

**Key Activities:**
- Pause current work
- Create new feature folder OR update unstarted feature folder
- Run S2 deep dive for new/updated feature
- Flesh out spec.md and checklist.md
- Update epic documentation

**Output:** Complete spec.md and checklist.md for new/updated feature

---

### PHASE 3 & 4: Realignment (S3 & 4)
**See:** `missed_requirement/realignment.md`

**Purpose:** Re-align ALL features and update epic test plan

**Key Activities:**
- S3: Epic-Level Docs, Tests, and Approval (ALL features, not just new/updated)
- Resolve conflicts between features
- S3.P1: Update epic_smoke_test_plan.md with scenarios for new/updated feature
- S4 deprecated — Test Scope Decision in S5 Step 0 (use Testing Approach from EPIC_README)
- Update Epic Progress Tracker
- Update EPIC_README with new sequence

**Output:** All features aligned + epic test plan updated

---

### PHASE 5: Resume Previous Work
**See:** `missed_requirement/realignment.md` (final section)

**Purpose:** Resume paused work from documented resume point

**Key Activities:**
- Verify feature spec unchanged (or document changes)
- Resume at documented step
- Update README Agent Status
- Continue with paused work

**Output:** Previous work resumed successfully

---

### SPECIAL CASE: Discovery During Epic Testing (S9/S10)
**See:** `missed_requirement/s9_s10_special.md`

**Purpose:** Handle missed requirements discovered during epic testing with special restart protocol

**Key Activities:**
- Complete planning (S2/3/4) as usual
- Complete ALL remaining features (entire S5 sequence)
- Implement new/updated feature (full S5)
- **RESTART epic-level testing from S9.P1 Step 1**

**Output:** Epic testing restarted with new feature included

**Why different:** New feature changes epic integration, previous epic test results invalid

---

## File Structure

### Epic-Level Tracking

```bash
epic_name/
├── EPIC_README.md                     ← Missed Requirement Tracking table
│   └── ## Missed Requirements Handled
│       | # | Name | Option | Priority | Created | Implemented | Status |
│
├── feature_01_player_integration/     ← Original features
├── feature_02_projection_system/
├── feature_03_performance_tracker/    ← May be updated with missed req
├── feature_04_matchup_analysis/
└── feature_05_injury_tracking/        ← New feature from missed req
```

**No separate requirement_{priority}_{name}/ folders:**
- Missed requirements are real features
- Get proper `feature_{XX}_{name}/` folders
- Or update existing unstarted `feature_XX_{name}/` folders

---

## Which Phase Should I Use?

**Use this decision tree to navigate to the right guide:**

```bash
Just discovered missing requirement?
└─ Read missed_requirement/discovery.md (PHASE 1)
   └─ Present options to user, get decision

User decided approach, need to plan?
└─ Read missed_requirement/planning.md (PHASE 2)
   └─ S2 deep dive for new/updated feature

Planning complete, need to align features?
└─ Read missed_requirement/realignment.md (PHASE 3 & 4)
   └─ S3 re-alignment → Resume work (S4 deprecated — test scope at S5 Step 0)

Discovered during S9 or S10?
└─ Read missed_requirement/s9_s10_special.md (SPECIAL CASE)
   └─ Complete all features → Restart epic testing
```

---

## Common Scenarios

### Scenario 1: Discovered During Feature Implementation (S6)

**Actions:**
1. Use discovery.md to present options to user
2. User decides: Create new feature (medium priority)
3. Use planning.md for S2 deep dive
4. Use realignment.md for S3 + resume
5. New feature implemented after current feature completes

---

### Scenario 2: Discovered During Validation Loop (S7.P2)

**Actions:**
1. Use discovery.md to present options to user
2. User decides: Update unstarted feature_03
3. Use planning.md to update feature_03 spec
4. Use realignment.md for S3 + resume
5. Resume Validation Loop where left off
6. feature_03 implemented later with added scope

---

### Scenario 3: Discovered During Epic Testing (S9.P2)

**Actions:**
1. Use discovery.md to present options to user
2. Use planning.md for S2 deep dive
3. Use realignment.md for S3
4. **Use s9_s10_special.md for special restart protocol**
5. Complete all remaining features
6. Implement new/updated feature
7. **RESTART epic testing from S9.P1 Step 1**

---

## Summary

**Missed Requirement Protocol handles forgotten scope by:**

1. **Discovery:** Present two options (new feature vs update unstarted)
2. **Planning:** Full S2 deep dive for new/updated feature
3. **Realignment:** S3 re-alignment (S4 deprecated — test scope at S5 Step 0)
4. **Resume:** Continue paused work
5. **Implementation:** Feature implemented later in sequence

**Special Case:**
- If discovered during S9/S10: Complete all features → Restart epic testing from S9.P1

**Key Principle:** Missed requirements are REAL features - treated with same rigor, proper planning, epic alignment

**Sub-Guides:**
- `missed_requirement/discovery.md` - Discovery & user decision
- `missed_requirement/planning.md` - S2 deep dive
- `missed_requirement/realignment.md` - S2.P2 + S3 realignment + resume
- `missed_requirement/s9_s10_special.md` - Epic testing special case

---

**READ THE APPROPRIATE SUB-GUIDE FOR DETAILED INSTRUCTIONS**

*End of missed_requirement/missed_requirement_protocol.md (Router)*
