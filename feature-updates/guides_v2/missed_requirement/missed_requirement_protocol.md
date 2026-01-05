# Missed Requirement Protocol (Router)

**Purpose:** Handle missing scope/requirements discovered after Stage 5 begins by treating them as real features - either creating a new feature or updating an unstarted one - then temporarily returning to planning stages to maintain epic coherence.

**When to Use:** Missing requirement discovered at ANY point after first Stage 5 starts - you know WHAT needs to be built (just forgot to include it in the original spec)

**When NOT to Use:**
- Unknown bugs requiring investigation - use debugging/debugging_protocol.md instead
- Missing scope discovered BEFORE any feature enters Stage 5 - just update specs directly during Stage 2/3/4

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
   - Critical Rules: "Get user approval first", "Return to Stage 2/3/4", "Update epic docs"
   - Next Action: Present options to user (new feature vs update unstarted)

3. **Get user approval** before creating/updating features

4. **THEN AND ONLY THEN** proceed with missed requirement handling

---

## Quick Start

**What is this protocol?**
Missed Requirement Protocol treats missing scope as real features - either creating new features or updating unstarted ones - then temporarily returning to Stage 2/3/4 planning to maintain epic-level coherence before resuming implementation work.

**When do you use this protocol?**
- Missing requirement discovered at ANY point after first Stage 5 starts:
  - During Stage 5a (TODO creation)
  - During Stage 5b (Implementation)
  - During Stage 5c (QA - smoke testing, QC rounds)
  - During debugging protocol (while investigating issues)
  - During Stage 6 (Epic-level testing)
  - During Stage 7 (User testing)
- You KNOW what needs to be built (solution is clear, just wasn't in original spec)
- Need to add missing functionality as a proper feature
- Example: "We forgot to add player injury status tracking"

**When NOT to use this protocol?**
- Unknown bugs requiring investigation (use debugging/debugging_protocol.md instead)
- Example: "Player scores are sometimes wrong but we don't know why"
- Missing scope discovered BEFORE any feature enters Stage 5 (just update specs directly during Stage 2/3/4)

**Key Outputs:**
- ✅ New feature created OR unstarted feature updated
- ✅ Feature spec fleshed out (Stage 2)
- ✅ All features re-aligned (Stage 3)
- ✅ Epic test plan updated (Stage 4)
- ✅ Epic documentation updated for resumability
- ✅ Ready to resume previous work
- ✅ New/updated feature implemented when its turn comes in sequence

**Time Estimate:**
Varies by requirement complexity (1-3 hours for planning stages typical)

**Exit Condition:**
Missed requirement handling is complete when the new/updated feature has been planned (Stage 2/3/4 complete), epic docs updated, and previous work resumed. The feature itself gets implemented later when its turn comes in the implementation sequence.

---

## 🛑 Critical Rules

```
1. ⚠️ CAN BE USED AT ANY TIME AFTER FIRST STAGE 5 STARTS
   - Before any feature enters Stage 5: Just update specs directly during Stage 2/3/4
   - After first feature enters Stage 5: Use this protocol for epic coherence
   - Can be discovered during: Implementation, QA, debugging, epic testing, user testing
   - Maintains epic coherence through re-alignment

2. ⚠️ TWO OPTIONS: NEW FEATURE OR UPDATE UNSTARTED
   - Agent presents BOTH options to user
   - User decides which approach
   - If new feature: Decide sequence position
   - If update unstarted: Which feature to update

3. ⚠️ ALWAYS RETURN TO STAGE 2/3/4
   - Stage 2: Flesh out new/updated feature spec
   - Stage 3: Cross-feature sanity check (ALL features)
   - Stage 4: Update epic testing strategy
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
   - Full Stage 2 deep dive
   - Full Stage 3 sanity check (all features)
   - Full Stage 4 test plan update
   - When implemented: Full Stage 5 (5a → 5b → 5c → 5d → 5e)
   - No shortcuts
```

---

## Missed Requirement Handling Phases (Overview)

The missed requirement protocol consists of 4 phases (plus special case):

### PHASE 1: Discovery & User Decision
**See:** `missed_requirement/discovery.md`

**Purpose:** Identify missing requirement and get user decision on approach

**Key Activities:**
- Discover missing requirement (can happen during any stage after first Stage 5)
- Present two options to user (create new feature OR update unstarted feature)
- Get user decision on approach
- Get user decision on priority/sequence (if new feature)
- Document paused work state

**Output:** User decision + paused work documented

---

### PHASE 2: Planning (Stage 2 Deep Dive)
**See:** `missed_requirement/planning.md`

**Purpose:** Create/update feature spec through Stage 2 deep dive

**Key Activities:**
- Pause current work
- Create new feature folder OR update unstarted feature folder
- Run Stage 2 deep dive for new/updated feature
- Flesh out spec.md and checklist.md
- Update epic documentation

**Output:** Complete spec.md and checklist.md for new/updated feature

---

### PHASE 3 & 4: Realignment (Stage 3 & 4)
**See:** `missed_requirement/realignment.md`

**Purpose:** Re-align ALL features and update epic test plan

**Key Activities:**
- Stage 3: Cross-feature sanity check (ALL features, not just new/updated)
- Resolve conflicts between features
- Stage 4: Update epic_smoke_test_plan.md
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

### SPECIAL CASE: Discovery During Epic Testing (Stage 6/7)
**See:** `missed_requirement/stage_6_7_special.md`

**Purpose:** Handle missed requirements discovered during epic testing with special restart protocol

**Key Activities:**
- Complete planning (Stage 2/3/4) as usual
- Complete ALL remaining features (entire Stage 5 sequence)
- Implement new/updated feature (full Stage 5)
- **RESTART epic-level testing from Stage 6a Step 1**

**Output:** Epic testing restarted with new feature included

**Why different:** New feature changes epic integration, previous epic test results invalid

---

## File Structure

### Epic-Level Tracking

```
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

```
Just discovered missing requirement?
└─ Read missed_requirement/discovery.md (PHASE 1)
   └─ Present options to user, get decision

User decided approach, need to plan?
└─ Read missed_requirement/planning.md (PHASE 2)
   └─ Stage 2 deep dive for new/updated feature

Planning complete, need to align features?
└─ Read missed_requirement/realignment.md (PHASE 3 & 4)
   └─ Stage 3 sanity check + Stage 4 test plan update → Resume work

Discovered during Stage 6 or 7?
└─ Read missed_requirement/stage_6_7_special.md (SPECIAL CASE)
   └─ Complete all features → Restart epic testing
```

---

## Common Scenarios

### Scenario 1: Discovered During Feature Implementation (Stage 5b)

**Actions:**
1. Use discovery.md to present options to user
2. User decides: Create new feature (medium priority)
3. Use planning.md for Stage 2 deep dive
4. Use realignment.md for Stage 3/4 + resume
5. New feature implemented after current feature completes

---

### Scenario 2: Discovered During QC Rounds (Stage 5cb)

**Actions:**
1. Use discovery.md to present options to user
2. User decides: Update unstarted feature_03
3. Use planning.md to update feature_03 spec
4. Use realignment.md for Stage 3/4 + resume
5. Resume QC rounds where left off
6. feature_03 implemented later with added scope

---

### Scenario 3: Discovered During Epic Testing (Stage 6b)

**Actions:**
1. Use discovery.md to present options to user
2. Use planning.md for Stage 2 deep dive
3. Use realignment.md for Stage 3/4
4. **Use stage_6_7_special.md for special restart protocol**
5. Complete all remaining features
6. Implement new/updated feature
7. **RESTART epic testing from Stage 6a Step 1**

---

## Summary

**Missed Requirement Protocol handles forgotten scope by:**

1. **Discovery:** Present two options (new feature vs update unstarted)
2. **Planning:** Full Stage 2 deep dive for new/updated feature
3. **Realignment:** Stage 3 sanity check + Stage 4 test plan update
4. **Resume:** Continue paused work
5. **Implementation:** Feature implemented later in sequence

**Special Case:**
- If discovered during Stage 6/7: Complete all features → Restart epic testing from Stage 6a

**Key Principle:** Missed requirements are REAL features - treated with same rigor, proper planning, epic alignment

**Sub-Guides:**
- `missed_requirement/discovery.md` - Discovery & user decision
- `missed_requirement/planning.md` - Stage 2 deep dive
- `missed_requirement/realignment.md` - Stage 3/4 alignment + resume
- `missed_requirement/stage_6_7_special.md` - Epic testing special case

---

**READ THE APPROPRIATE SUB-GUIDE FOR DETAILED INSTRUCTIONS**

*End of missed_requirement/missed_requirement_protocol.md (Router)*
