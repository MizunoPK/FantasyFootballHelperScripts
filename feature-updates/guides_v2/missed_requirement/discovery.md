# PHASE 1: Discovery & User Decision

**Purpose:** Identify missing requirement and get user decision on approach

**When to Use:** Missing requirement discovered at any point after first Stage 5 starts

**Previous Phase:** None (entry point from any workflow stage)

**Next Phase:** PHASE 2 (Planning) - See `missed_requirement/planning.md`

---

## Triggered When

**Missing requirement can be discovered during ANY stage after first Stage 5 starts:**

**During Feature Implementation (Stage 5):**
- Stage 5a (TODO creation): Realize missing scope while planning implementation
- Stage 5b (Implementation): Discover forgotten functionality while coding
- Stage 5c (Smoke Testing): Find missing requirement during Part 1/2/3 tests
- Stage 5c (QC Rounds): Discover missing scope during Round 1/2/3

**During Debugging:**
- While investigating issues: Realize root cause is missing functionality
- After fixing bugs: Discover the fix revealed missing scope

**During Epic-Level Work (Stage 6/7):**
- Phase 6.1 (Epic Smoke Testing): Find missing integration between features
- Phase 6.2 (Epic QC Rounds): Discover missing epic-level functionality
- Stage 7 (User Testing): User reports missing functionality that was in original intent

**User Reports:**
- User explicitly requests missing functionality
- User identifies gap in original epic scope

---

## Step 1: Discover Missing Requirement

**Example scenarios:**

### Example 1: Discovered during implementation
```
Currently: feature_02_projection_system (Stage 5b - Implementation)

Discovery: We forgot to include player injury status tracking
- Projections should account for injury status
- This was in original epic intent but not in any feature spec
- Solution is clear: Need injury status field + API integration
```

### Example 2: Discovered during QA
```
Currently: feature_03_performance_tracker (Stage 5c - QC Round 2)

Discovery: We forgot to add export functionality
- Users need to export performance reports to CSV
- This was in original epic but not in any feature
- Solution is clear: Add CSV export utility
```

### Example 3: Discovered during debugging
```
Currently: Debugging issue_01_null_scoring (feature_01/debugging/)

Discovery: Root cause is missing validation layer
- Players without position data should be validated earlier
- This functionality was assumed to exist but doesn't
- Solution is clear: Need input validation feature
```

### Example 4: Discovered during epic testing
```
Currently: Epic QC Round 1 (Phase 6.2)

Discovery: Missing integration between features
- feature_02 and feature_04 need shared caching layer
- This integration point wasn't planned in any feature
- Solution is clear: Need caching infrastructure feature
```

---

## Step 2: Present Options to User

**Use this template to present the missed requirement:**

```markdown
I've discovered a missed requirement that needs to be addressed:

## Missed Requirement: {Brief description}

**Discovered during:** {Current stage and feature}

**What's missing:**
{Clear description of missing scope}

**Why it's needed:**
{Impact of not having this functionality}

**Estimated complexity:**
{Small / Medium / Large}

---

## Options for Handling

**OPTION 1: Create New Feature**
- Create feature_{XX}_{name}/ folder
- Full spec.md and checklist.md created
- Decide where in sequence it should be implemented
- Pros: Clean separation, clear scope
- Cons: Adds to epic feature count

**OPTION 2: Update Unstarted Feature**
Available unstarted features:
- feature_03_performance_tracker (not started yet)
- feature_04_matchup_analysis (not started yet)

Which feature should include this requirement?
- Pros: Keeps feature count stable, logical grouping
- Cons: Feature scope increases

---

## Recommended Approach

{Agent recommendation based on scope and cohesion}

**Reasoning:**
{Why this approach makes sense}

---

What would you like to do?
1. Create new feature (Option 1)
2. Update unstarted feature (Option 2) - which feature?
3. Skip for now (document and address later)
4. Other approach
```

**Wait for user response**

---

## Step 3: Determine Priority & Sequence (If Creating New Feature)

**If user chooses to create NEW feature, determine sequence position:**

### Ask user about priority

```markdown
Priority and sequence for new feature:

## Priority Level
- **High:** Blocks other features / Critical for epic
- **Medium:** Important but not blocking
- **Low:** Nice-to-have / Can be last

What priority level? {User input}

## Sequence Position
Current epic sequence:
1. feature_01_adp_integration (COMPLETE)
2. feature_02_projection_system (IN PROGRESS - Stage 5b)
3. feature_03_performance_tracker (NOT STARTED)
4. feature_04_matchup_analysis (NOT STARTED)

Where should the new feature go?
- **BEFORE feature_02** (high priority - blocks current feature)
- **AFTER feature_02** (medium priority - after current feature)
- **After feature_03** (lower priority)
- **At END** (low priority - implement last)

What sequence position? {User input}
```

### Priority & sequence decision matrix

| Priority | Sequence Position | Implementation Timing |
|----------|------------------|----------------------|
| **High** | BEFORE current feature | Next after current feature pauses (or immediately if blocks current) |
| **Medium** | AFTER current feature | After current feature completes |
| **Low** | At END of feature list | Last feature to implement |

**Example - High Priority:**
```
Currently: feature_02 (Stage 5b)
New feature: feature_05_injury_tracking (high priority)

Sequence update:
1. feature_01 ✅ COMPLETE
2. feature_05 ← INSERT HERE (high priority, needed by feature_02)
3. feature_02 🔄 PAUSED (resume after feature_05 completes)
4. feature_03 ◻️ NOT STARTED
5. feature_04 ◻️ NOT STARTED

Action: After planning, implement feature_05 immediately, THEN resume feature_02
```

**Example - Medium Priority:**
```
Currently: feature_02 (Stage 5b)
New feature: feature_05_injury_tracking (medium priority)

Sequence update:
1. feature_01 ✅ COMPLETE
2. feature_02 🔄 PAUSED (resume now, complete normally)
3. feature_05 ← INSERT HERE (medium priority, after current)
4. feature_03 ◻️ NOT STARTED
5. feature_04 ◻️ NOT STARTED

Action: Resume feature_02 now, implement feature_05 after feature_02 completes
```

**Example - Low Priority:**
```
Currently: feature_02 (Stage 5b)
New feature: feature_05_injury_tracking (low priority)

Sequence update:
1. feature_01 ✅ COMPLETE
2. feature_02 🔄 PAUSED (resume now)
3. feature_03 ◻️ NOT STARTED
4. feature_04 ◻️ NOT STARTED
5. feature_05 ← INSERT AT END (low priority, implement last)

Action: Resume feature_02, implement features in order, feature_05 is last
```

---

## Step 4: Confirm with User (If Updating Unstarted Feature)

**If user chooses to update UNSTARTED feature:**

```markdown
You've chosen to update feature_{XX}_{name}

This will:
- Add new scope to feature_{XX}'s spec.md
- Update feature_{XX}'s checklist.md
- May increase implementation time
- Feature still implemented in its current sequence position

Proceed? {User confirms}
```

### Updating unstarted feature impact

| Original Feature | Updated Feature | Impact |
|-----------------|----------------|---------|
| feature_03_performance_tracker | feature_03_performance_tracker + injury tracking | Scope increases, stays in same sequence position |
| feature_04_matchup_analysis | feature_04_matchup_analysis + injury tracking | Scope increases, stays in same sequence position |

**Sequence position unchanged:**
- Feature keeps its original position
- Just has more scope when implemented
- May take longer to implement (document in spec)

---

## Step 5: Document Current Work State

### Update current feature's README.md (if pausing work)

**Template:**

```markdown
## Agent Status (PAUSED - Missed Requirement Handling)

**Last Updated:** {YYYY-MM-DD HH:MM}
**Status:** PAUSED for missed requirement: {requirement_name}
**Paused At:** {Current stage and step}

**Missed Requirement Action:**
- {Creating new feature_05_injury_tracking} OR {Updating feature_03_performance_tracker}
- Returning to Stage 2/3/4 for planning
- Will resume this feature after planning complete

**Resume Instructions:**
When planning complete:
1. Verify this feature's spec still valid after alignment
2. Resume at: {Exact step where paused}
3. Context: {Brief context of what was being done}

**Context at Pause:**
{Document current state, progress, any important context}
```

---

## Step 6: Update EPIC_README.md

### Add to Missed Requirement Tracking table

```markdown
## Missed Requirement Tracking

| # | Requirement | Action | Priority | Status | Created | Notes |
|---|-------------|--------|----------|--------|---------|-------|
| 1 | Player injury tracking | New feature_05 | High | Stage 2 | 2026-01-04 | Inserting after feature_02 |
```

### Update Current Status section

```markdown
## Current Status

**Last Updated:** {YYYY-MM-DD HH:MM}

**Missed Requirement Handling:**
- Requirement: Player injury tracking
- Action: Creating new feature_05_injury_tracking
- Priority: High
- Sequence: Insert after feature_02 (before feature_03)
- Currently: Returning to Stage 2 for planning

**Paused Work:**
- feature_02_projection_system: Paused at Stage 5b Phase 3
  - Resume point: After planning complete, continue Phase 3
  - Agent Status saved: README.md in feature_02/ folder
```

### Update Epic Progress Tracker (if creating new feature)

```markdown
## Epic Progress Tracker

| Feature | Stage 2 | Stage 3 | Stage 4 | Stage 5a | Stage 5b | Stage 5c | Stage 5d | Stage 5e |
|---------|---------|---------|---------|----------|----------|----------|----------|----------|
| feature_01_adp_integration | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| feature_02_projection_system | ✅ | ✅ | ✅ | ✅ | 🔄 | ◻️ | ◻️ | ◻️ |
| feature_03_performance_tracker | ✅ | ✅ | ✅ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ |
| feature_04_matchup_analysis | ✅ | ✅ | ✅ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ |
| feature_05_injury_tracking (NEW) | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ |

**Implementation Sequence (Updated):**
1. feature_01 ✅ COMPLETE
2. feature_02 🔄 PAUSED at Stage 5b
3. feature_05 ◻️ NOT STARTED (INSERTED - high priority)
4. feature_03 ◻️ NOT STARTED
5. feature_04 ◻️ NOT STARTED

**Next after feature_02 resumes and completes:** feature_05 (then feature_03, then feature_04)
```

---

## Decision Summary

**Before proceeding to PHASE 2, verify:**

**If creating NEW feature:**
- [ ] User approved creating new feature
- [ ] Priority determined (high/medium/low)
- [ ] Sequence position determined
- [ ] Feature number assigned (feature_{XX})
- [ ] Current work paused and documented (if applicable)
- [ ] EPIC_README.md updated with new sequence
- [ ] Missed Requirement Tracking table updated

**If updating UNSTARTED feature:**
- [ ] User approved updating specific feature
- [ ] User confirmed which feature to update
- [ ] Current work paused and documented (if applicable)
- [ ] EPIC_README.md updated with missed req tracking
- [ ] Note made that feature scope increased

---

## Common Scenarios

### Scenario 1: High priority new feature (blocks current work)

**Actions:**
1. Present options to user
2. User chooses: Create new feature (high priority)
3. Assign next feature number (feature_05)
4. Sequence: Insert BEFORE current feature
5. Pause current feature
6. Document paused state
7. Update EPIC_README with new sequence
8. **Next:** Planning (PHASE 2) for feature_05

---

### Scenario 2: Medium priority new feature (after current)

**Actions:**
1. Present options to user
2. User chooses: Create new feature (medium priority)
3. Assign next feature number (feature_05)
4. Sequence: Insert AFTER current feature
5. Current feature continues (not paused)
6. Update EPIC_README with new sequence
7. **Next:** Planning (PHASE 2) for feature_05 while current feature continues

---

### Scenario 3: Update unstarted feature

**Actions:**
1. Present options to user
2. User chooses: Update feature_03
3. Current work continues or pauses (based on context)
4. Update EPIC_README tracking
5. **Next:** Planning (PHASE 2) to update feature_03 spec

---

## Next Steps

**After completing PHASE 1 (Discovery & User Decision):**

✅ User decision made (new feature vs update unstarted)
✅ Priority and sequence determined (if new feature)
✅ Current work state documented (if paused)
✅ EPIC_README.md updated

**Next:** Read `missed_requirement/planning.md` for PHASE 2 (Planning - Stage 2 Deep Dive)

---

**END OF PHASE 1 GUIDE**
