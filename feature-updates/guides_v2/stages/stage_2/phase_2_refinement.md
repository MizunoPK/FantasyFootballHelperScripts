# STAGE 2c: Refinement Phase Guide

🚨 **MANDATORY READING PROTOCOL**

**Before starting this phase:**
1. Use Read tool to load THIS ENTIRE GUIDE
2. Acknowledge critical requirements (see "Critical Rules" section below)
3. Verify prerequisites (see "Prerequisites Checklist" section below)
4. Update feature README.md Agent Status with guide name + timestamp

**DO NOT proceed without reading this guide.**

**After session compaction:**
- Check feature README.md Agent Status for current phase
- READ THIS GUIDE again (full guide, not summary)
- Continue from "Next Action" in Agent Status

---

## Quick Start

**What is this phase?**
Refinement Phase is where you resolve all open questions through interactive dialogue (ONE at a time), adjust scope if needed, align with completed features, and get user approval on acceptance criteria. This phase ensures the spec is complete, validated, and ready for implementation.

**When do you use this guide?**
- STAGE_2b (Specification Phase) complete
- spec.md has Epic Intent section and requirement traceability
- checklist.md has open questions
- Phase 2.5 (Spec-to-Epic Alignment Check) passed

**Key Outputs:**
- ✅ All checklist questions resolved (zero open items)
- ✅ Spec updated in real-time after each answer
- ✅ Feature scope validated (not too large, properly scoped)
- ✅ Cross-feature alignment complete (no conflicts with other features)
- ✅ Acceptance criteria created and user-approved

**Time Estimate:**
1-2 hours per feature (depends on number of questions and feature complexity)

**Exit Condition:**
Refinement Phase is complete when all checklist questions are resolved, scope is validated, cross-feature alignment is done, and user has approved acceptance criteria

---

## Critical Rules

```
┌─────────────────────────────────────────────────────────────┐
│ CRITICAL RULES - These MUST be copied to README Agent Status │
└─────────────────────────────────────────────────────────────┘

1. ⚠️ ONE question at a time (NEVER batch questions)
   - Ask question
   - Wait for user answer
   - Update spec/checklist IMMEDIATELY
   - Evaluate for new questions
   - Then ask next question

2. ⚠️ Update spec.md and checklist.md IMMEDIATELY after each answer
   - Do NOT batch updates
   - Keep files current in real-time
   - Document user's exact answer or paraphrase

3. ⚠️ If checklist grows >35 items, STOP and propose split
   - Trigger: More than 35 checklist items
   - Action: Propose splitting into multiple features
   - Requirement: Get user approval before splitting
   - If approved: Return to Stage 1 to create new features

4. ⚠️ Cross-feature alignment is MANDATORY (not optional)
   - Compare to ALL features with "Stage 2 Complete"
   - Look for: Conflicts, duplicates, incompatible assumptions
   - Resolve conflicts before proceeding
   - Document alignment verification

5. ⚠️ Acceptance criteria require USER APPROVAL (mandatory gate)
   - Create "Acceptance Criteria" section in spec.md
   - List EXACT files, structures, behaviors
   - Present to user for approval
   - Wait for explicit approval
   - Document approval timestamp

6. ⚠️ Every user answer creates new requirement with traceability
   - Source: "User Answer to Question N (checklist.md)"
   - Add to spec.md immediately
   - Update checklist to mark question resolved
```

---

## Critical Decisions Summary

**This phase has ONE critical decision point:**

### Decision Point: Phase 6 - User Approval (MANDATORY)

**Question:** Does user approve acceptance criteria?
- **If YES:** Mark approval timestamp, proceed to mark feature complete
- **If NO:** Update spec based on feedback, re-present for approval
- **Impact:** Cannot proceed to Stage 3 or implementation without user approval

---

## Prerequisites Checklist

**Before starting Refinement Phase (STAGE_2c), verify:**

□ **STAGE_2b complete:**
  - Phase 2 complete: spec.md has Epic Intent section, requirements with traceability
  - Phase 2 complete: checklist.md exists with open questions
  - Phase 2.5 complete: Spec-to-Epic Alignment Check PASSED
  - spec.md has valid sources for all requirements (Epic/User Answer/Derived)

□ **Files exist and are current:**
  - feature_{N}_{name}/spec.md exists with Epic Intent section
  - feature_{N}_{name}/checklist.md exists with questions
  - feature_{N}_{name}/README.md has Agent Status

□ **Research foundation exists:**
  - epic/research/{FEATURE_NAME}_DISCOVERY.md exists (from Phase 1)
  - Research completeness audit passed (Phase 1.5)

□ **Agent Status updated:**
  - Last guide: STAGE_2b_specification_phase_guide.md
  - Current phase: Ready to start Phase 3 (Interactive Question Resolution)

**If any prerequisite fails:**
- ❌ Do NOT start Refinement Phase
- Complete missing prerequisites first
- Return to STAGE_2b if Phase 2.5 not passed

---

## Phase 3: Interactive Question Resolution

**Goal:** Resolve ALL checklist questions ONE AT A TIME

**⚠️ CRITICAL:** This is the heart of the refinement phase. Do NOT batch questions. Ask one, wait, update, then ask next.

---

### Step 3.1: Select Next Question

**Priority order:**
1. **Blocking questions** - Must be answered before other questions make sense
2. **High-impact questions** - Affect algorithm or data structure design
3. **Low-impact questions** - Implementation details

**Example blocking question:** "What format is the ADP data in?" (affects all other decisions)

**Example high-impact question:** "Should we use fuzzy matching or exact matching for player names?"

**Example low-impact question:** "What should the log message say when ADP data loads?"

**How to identify priority:**
- Read all open questions in checklist.md
- Identify dependencies (some questions depend on others)
- Start with questions that unlock other questions

---

### Step 3.2: Ask ONE Question

**Format:**

```markdown
I have a question about Feature {N} ({Name}):

## Question {N}: {Title}

**Context:** {Why this matters, what we're trying to accomplish}

**Options:**

A. **{Option A}**
   - Pros: {benefits}
   - Cons: {drawbacks}

B. **{Option B}**
   - Pros: {benefits}
   - Cons: {drawbacks}

C. **{Option C}**
   - Pros: {benefits}
   - Cons: {drawbacks}

**My recommendation:** Option {X} because {reason}

**What do you prefer?** (or suggest a different approach)
```

**Best practices:**
- Provide 2-4 well-defined options
- Include pros/cons for each option
- Give your recommendation with reasoning
- Allow user to suggest alternative
- Keep context brief but informative

**Example:**

```markdown
I have a question about Feature 01 (ADP Integration):

## Question 3: Player Name Matching Strategy

**Context:** When matching players from ADP data to our player list, we need to handle name variations (e.g., "A.J. Brown" vs "AJ Brown").

**Options:**

A. **Exact match only (strict)**
   - Pros: Simple, fast, no false positives
   - Cons: Will miss players with name variations

B. **Fuzzy matching (Levenshtein distance)**
   - Pros: Handles variations, fewer missing players
   - Cons: Potential false positives, slower

C. **Name normalization then exact match**
   - Pros: Balanced approach, handles common variations
   - Cons: Need to maintain normalization rules

**My recommendation:** Option C because it handles most real-world cases (initials, spacing) while avoiding false positives from fuzzy matching.

**What do you prefer?**
```

---

### Step 3.3: WAIT for User Answer

⚠️ **STOP HERE - Do NOT proceed without user answer**

**Do NOT:**
- Ask multiple questions in one message
- Proceed to next question while waiting
- Make assumptions about what user will choose
- Continue working on other phases

**DO:**
- Wait for user response
- Be ready to answer follow-up questions
- Be ready to present additional options if user asks

**Update Agent Status:**
```markdown
**Last Updated:** {YYYY-MM-DD HH:MM}
**Current Phase:** DEEP_DIVE
**Current Step:** Phase 3 - Waiting for answer to Question {N}
**Current Guide:** STAGE_2c_refinement_phase_guide.md
**Guide Last Read:** {YYYY-MM-DD HH:MM}
**Critical Rules from Guide:**
- ONE question at a time
- Update immediately after answer
- Wait for user before proceeding

**Progress:** {M}/{N} questions resolved
**Next Action:** Wait for user answer to Question {current_question_number}
**Blockers:** Waiting for user input on {question_topic}
```

---

### Step 3.4: Update Spec & Checklist Immediately

**After user answers**, update files IMMEDIATELY (before asking next question):

**Update checklist.md:**
```markdown
### Question {N}: {Title}
- [x] **RESOLVED:** {User's choice}

**User's Answer:**
{Paste user's exact answer or paraphrase}

**Implementation Impact:**
- {How this affects the implementation}
- {What needs to be added to spec}
- {Any new questions this creates}
```

**Update spec.md:**

Add requirement with new source:

```markdown
### Requirement {N}: {Name}

**Description:** {What this requirement does}

**Source:** User Answer to Question {N} (checklist.md)
**Traceability:** User confirmed preference on {date}

**Implementation:**
{Details based on user's answer}

**Technical Details:**
- {Specific implementation notes}
- {Edge cases to handle}
- {Dependencies or prerequisites}
```

**Example:**

In checklist.md:
```markdown
### Question 3: Player Name Matching Strategy
- [x] **RESOLVED:** Option C - Name normalization then exact match

**User's Answer:**
"Let's go with option C. Normalize initials (remove periods and spaces) and convert to lowercase before matching."

**Implementation Impact:**
- Add name normalization function to PlayerManager
- Apply normalization to both ADP data and player list
- Match after normalization
- Need to handle edge cases: multiple middle initials, Jr./Sr. suffixes
```

In spec.md:
```markdown
### Requirement 5: Player Name Matching with Normalization

**Description:** Match players from ADP data to player list using name normalization followed by exact string matching

**Source:** User Answer to Question 3 (checklist.md)
**Traceability:** User confirmed Option C on 2025-01-02

**Implementation:**
- Create name normalization function:
  - Remove periods from initials
  - Remove all whitespace
  - Convert to lowercase
  - Handle suffixes (Jr., Sr., III, etc.)
- Apply normalization to both data sources before matching
- Perform exact string match after normalization
- Log unmatched players for manual review

**Technical Details:**
- Function signature: normalize_player_name(name: str) -> str
- Location: utils/player_matching.py (new file)
- Called from: PlayerManager.load_adp_data()
```

---

### Step 3.5: Evaluate for New Questions

**After updating files, ask:**
- Did this answer create NEW questions?
- Did this answer resolve OTHER questions?
- Do we need clarification on any part of the answer?

**Examples:**

**New questions created:**
- User chose fuzzy matching → NEW QUESTION: "What threshold should we use?" (add to checklist)
- User chose CSV format → NEW QUESTION: "Where should CSV file be located?" (add to checklist)

**Other questions resolved:**
- User chose Option A → Questions 5 and 7 are now N/A (mark as resolved with note)
- User provided implementation details → Question 4 is implicitly answered (mark as resolved)

**Update checklist.md if new questions arose:**
```markdown
### Question {N+1}: {New Question} (NEW - from Q{N} answer)
- [ ] **OPEN**

**Context:** User answered Q{N} with {answer}, which creates need to clarify {new_topic}

**Depends on:** Question {N} (resolved)
```

**Mark other questions resolved if applicable:**
```markdown
### Question 5: {Title}
- [x] **RESOLVED:** N/A (user's answer to Q3 made this unnecessary)

**Reason:** User chose Option C in Q3, which includes handling for this scenario
```

---

### Step 3.6: Repeat Until ALL Questions Resolved

Continue asking questions ONE AT A TIME until checklist shows:

```markdown
**Checklist Status:** 0 open questions, {N} resolved
```

**After each question, follow this cycle:**
1. Ask ONE question (Step 3.2)
2. Wait for answer (Step 3.3)
3. Update spec & checklist immediately (Step 3.4)
4. Evaluate for new questions (Step 3.5)
5. Select next question (Step 3.1)
6. Repeat

**Update Agent Status after each question:**
```markdown
**Progress:** Phase 3 - Question {M}/{N} answered ({M} resolved, {remaining} open)
**Next Action:** Ask Question {M+1}
**Blockers:** None
```

**When all questions resolved:**
```markdown
**Progress:** Phase 3 - COMPLETE (all {N} questions resolved)
**Next Action:** Phase 4 - Dynamic Scope Adjustment
**Blockers:** None
```

---

## Phase 4: Dynamic Scope Adjustment

**Goal:** Ensure feature scope is reasonable and properly categorized

**⚠️ CRITICAL:** Features with >35 checklist items become unmaintainable. Split if needed.

---

### Step 4.1: Count Checklist Items

**Count all resolved and open items in checklist.md:**

```bash
# Count checklist items
# Open items: lines with "- [ ]"
# Resolved items: lines with "- [x]"
# Total items: sum of both
```

**Document the count:**
```markdown
**Checklist Item Count:** {total} items ({resolved} resolved, {open} open)
```

---

### Step 4.2: Evaluate Feature Size

**Decision tree:**

**If checklist has >35 items:**
- ✋ **STOP** - Feature is too large
- Action: Propose split into multiple features
- Requirement: Get user approval before splitting
- Next: Step 4.3 (Propose Split)

**If checklist has 20-35 items:**
- ✅ **OK** - Feature is appropriately sized
- Action: Document as "medium complexity"
- Next: Step 4.4 (Check for New Work)

**If checklist has <20 items:**
- ✅ **OK** - Feature is reasonably sized
- Action: Document as "straightforward"
- Next: Step 4.4 (Check for New Work)

**Update Agent Status:**
```markdown
**Progress:** Phase 4 - Scope evaluation ({total} checklist items)
**Next Action:** {Propose split / Check for new work}
**Blockers:** None
```

---

### Step 4.3: Propose Feature Split (If >35 Items)

**If checklist >35 items, present split proposal to user:**

```markdown
## Feature Scope Analysis: {Feature Name}

**Current Status:**
- Checklist items: {total} items
- Threshold: 35 items (maximum for maintainability)
- **Assessment:** ⚠️ Feature is too large

**Why This Matters:**
- Features with >35 items are difficult to implement systematically
- Testing becomes complex (too many edge cases)
- Higher risk of bugs and missed requirements

**Proposed Split:**

I recommend splitting this into {N} separate features:

**Feature {N}a: {Name}**
- Scope: {What this covers}
- Checklist items: ~{count} items
- Rationale: {Why this is a logical grouping}

**Feature {N}b: {Name}**
- Scope: {What this covers}
- Checklist items: ~{count} items
- Rationale: {Why this is a logical grouping}

**Dependencies:**
- Feature {N}a should be implemented first
- Feature {N}b depends on {N}a completing
- No circular dependencies

**Next Steps If Approved:**
1. Return to Stage 1 to create new feature folders
2. Split spec.md and checklist.md into separate features
3. Update epic EPIC_README.md with new features
4. Continue Stage 2 for each new feature

**Do you approve this split?** (or suggest alternative grouping)
```

**If user approves split:**
- Document approval in current feature README.md
- Return to Stage 1 (Epic Planning) to restructure
- Create new feature folders
- Split spec and checklist content
- Update epic EPIC_README.md
- Resume Stage 2 for each new feature

**If user rejects split:**
- Document user decision to keep as single feature
- Note in feature README.md: "User approved large scope ({total} items)"
- Proceed to Step 4.4
- Be aware of increased implementation complexity

---

### Step 4.4: Check for New Work Discovered

**During question resolution, you may have discovered new work not in original epic:**

**Ask yourself:**
- Did user answers reveal additional subsystems not mentioned in epic?
- Did we uncover integration points requiring new features?
- Did we discover data sources or algorithms beyond original scope?

**Decision tree for new work:**

**Option A: New work is independent subsystem**
- Example: "We need a new CSV parser module"
- Example: "We need a player name matching library"
- **Action:** Propose as NEW FEATURE (separate from current feature)
- **Rationale:** Independent subsystems should be their own features
- **Next:** Present to user, if approved return to Stage 1

**Option B: New work extends current feature**
- Example: "We need to add logging to ADP loader"
- Example: "We need error handling for missing data"
- **Action:** Add to current feature's spec (expanded scope)
- **Rationale:** These are implementation details, not separate features
- **Next:** Update spec.md and checklist.md, continue with current feature

**Option C: No new work discovered**
- **Action:** Document "No scope creep identified"
- **Next:** Proceed to Phase 5

**If Option A (New Feature), present to user:**

```markdown
## New Work Discovered: {Name}

**What We Found:**
During question resolution, we discovered: {description of new work}

**Current Feature:**
Feature {N}: {Name}
- Original scope: {brief description}

**New Work:**
{New work description}

**Assessment:**
This new work is an independent subsystem that should be its own feature because:
- {Reason 1: e.g., "Can be developed and tested independently"}
- {Reason 2: e.g., "Will be reused by multiple features"}
- {Reason 3: e.g., "Has its own data sources and interfaces"}

**Recommendation:**
Create new Feature {M}: {New Feature Name}
- Scope: {What it covers}
- Dependencies: {What it depends on / what depends on it}

**Impact on Current Feature:**
- Current feature will DEPEND on new feature
- Should implement new feature first
- Current feature's checklist will be reduced by ~{count} items

**Do you want to create this as a separate feature?** (or keep in current feature)
```

**If user approves new feature:**
- Return to Stage 1 to create new feature folder
- Update epic EPIC_README.md
- Note dependency in current feature spec.md
- Continue Stage 2 for both features

**If user wants to keep in current feature:**
- Document decision in current feature README.md
- Update spec.md and checklist.md with expanded scope
- Continue with current feature

**If Option B (Expanded Scope), document in spec.md:**

Add new requirements to spec.md:
```markdown
### Requirement {N}: {New Requirement}

**Description:** {What this requirement does}

**Source:** Derived Requirement (discovered during question resolution)
**Traceability:** Emerged from answering Question {M} - user specified {context}

**Implementation:** {Details}
```

Update checklist.md if new questions arose:
```markdown
### Question {N}: {New Question} (NEW - from expanded scope)
- [ ] **OPEN**

**Context:** Expanded scope requires clarification on {topic}
```

**Update Agent Status:**
```markdown
**Progress:** Phase 4 - COMPLETE (scope validated, no split needed)
**Next Action:** Phase 5 - Cross-Feature Alignment
**Blockers:** None
```

---

## Phase 5: Cross-Feature Alignment

**Goal:** Compare this feature's spec to all completed features, resolve conflicts

**⚠️ CRITICAL:** This prevents features from having incompatible assumptions or duplicate work.

**Skip if:** This is the FIRST feature in the epic (no other features to compare to)

---

### Step 5.1: Identify Completed Features

**Check epic EPIC_README.md Feature Tracking table:**

Look for features with "Stage 2 Complete" marked [x]:

```markdown
| Feature | Name | Stage 2 Complete | Stage 5 Complete |
|---------|------|------------------|------------------|
| 01      | ADP Integration | [x] | [ ] |
| 02      | Matchup Ratings | [ ] | [ ] |  ← Current feature
| 03      | Trade Analyzer  | [ ] | [ ] |
```

**In this example:**
- Feature 01 has Stage 2 Complete = [x]
- Feature 02 (current) is finishing Stage 2
- Must compare Feature 02 to Feature 01

**Document:**
```markdown
**Features to Compare:**
- Feature 01: ADP Integration (completed Stage 2)

**Current Feature:**
- Feature 02: Matchup Ratings
```

**If this is the first feature:**
```markdown
**Features to Compare:** None (this is first feature)

**Action:** Skip Phase 5 (Cross-Feature Alignment)
**Next:** Phase 6 (Acceptance Criteria & User Approval)
```

---

### Step 5.2: Compare Specs Systematically

**For EACH completed feature, perform pairwise comparison:**

**Read completed feature's spec.md:**
- Use Read tool to load entire spec
- Focus on: Components Affected, Data Structures, Requirements, Algorithms

**Create comparison document:**

`epic/research/ALIGNMENT_{current_feature}_vs_{other_feature}.md`:

```markdown
# Alignment Check: Feature {N} vs Feature {M}

**Date:** {YYYY-MM-DD}
**Current Feature:** Feature {N}: {Name}
**Comparison Target:** Feature {M}: {Name} (Stage 2 Complete)

---

## Comparison Categories

### 1. Components Affected

**Feature {N} modifies:**
- {Component 1}
- {Component 2}
- {Component 3}

**Feature {M} modifies:**
- {Component A}
- {Component B}
- {Component C}

**Overlap Analysis:**
- ✅ No overlap (different components)
- ⚠️ Both modify {Component X} (potential conflict)
  - Feature {N} assumption: {what current feature assumes}
  - Feature {M} assumption: {what other feature assumes}
  - **Conflict?** {YES/NO}
  - **Resolution:** {How to resolve}

---

### 2. Data Structures

**Feature {N} introduces/modifies:**
- {Data structure 1}
- {Data structure 2}

**Feature {M} introduces/modifies:**
- {Data structure A}
- {Data structure B}

**Overlap Analysis:**
- ✅ No overlap (different data structures)
- ⚠️ Both use {Data X}
  - Feature {N} expects format: {format description}
  - Feature {M} expects format: {format description}
  - **Conflict?** {YES/NO}
  - **Resolution:** {How to resolve}

---

### 3. Requirements

**Feature {N} requirements:**
- {Requirement 1}
- {Requirement 2}

**Feature {M} requirements:**
- {Requirement A}
- {Requirement B}

**Overlap Analysis:**
- ✅ No duplicate requirements
- ⚠️ Similar requirement: {description}
  - Feature {N}: {how it's implemented}
  - Feature {M}: {how it's implemented}
  - **Duplicate work?** {YES/NO}
  - **Resolution:** {Combine into shared utility / keep separate}

---

### 4. Assumptions

**Feature {N} assumptions:**
- {Assumption 1}
- {Assumption 2}

**Feature {M} assumptions:**
- {Assumption A}
- {Assumption B}

**Compatibility Check:**
- ✅ Compatible assumptions
- ⚠️ Incompatible assumptions:
  - Feature {N} assumes: {assumption}
  - Feature {M} assumes: {conflicting assumption}
  - **Impact:** {What breaks if both are true}
  - **Resolution:** {How to resolve}

---

### 5. Integration Points

**Does Feature {N} depend on Feature {M}?**
- {YES/NO}
- If YES: {What dependency, how to handle}

**Does Feature {M} depend on Feature {N}?**
- {YES/NO}
- If YES: {What dependency, implementation order}

**Circular dependency?**
- {YES/NO}
- If YES: **CRITICAL** - Must resolve before implementation

---

## Summary

**Total Conflicts Found:** {count}

**Critical Conflicts (must resolve):**
1. {Conflict 1}
   - Resolution: {How to fix}
2. {Conflict 2}
   - Resolution: {How to fix}

**Minor Conflicts (nice to resolve):**
1. {Conflict 3}
   - Resolution: {How to fix}

**No Conflicts:**
- {Category} - No overlap

**Action Items:**
- [ ] Update Feature {N} spec.md: {what to change}
- [ ] Update Feature {M} spec.md: {what to change} (requires revisiting completed feature)
- [ ] Document resolution in both features

**Alignment Status:** {PASS / CONFLICTS FOUND}
```

---

### Step 5.3: Resolve Conflicts

**For EACH conflict found:**

**Option A: Update current feature (Feature N)**
- Modify spec.md to align with completed feature
- Update checklist.md if new questions arise
- Document change with reason

**Option B: Update completed feature (Feature M)**
- **CAUTION:** Completed feature may already be in implementation
- Check if other feature is in Stage 5 (implementation)
- If yes, coordinate changes with implementation
- If no (only Stage 2 complete), update its spec

**Option C: Create shared utility**
- If both features need same functionality
- Create new Feature X: Shared Utility
- Both features depend on Feature X
- Return to Stage 1 to create new feature

**Document resolution:**

Update current feature's spec.md:
```markdown
### Cross-Feature Alignment Notes

**Feature {M} Alignment ({Date}):**
- Conflict: {Description}
- Resolution: {What we changed}
- Impact: {How this affects implementation}
```

Update alignment document:
```markdown
**Conflict 1: RESOLVED**
- Original conflict: {description}
- Resolution chosen: {Option A/B/C}
- Changes made:
  - Feature {N}: {what changed}
  - Feature {M}: {what changed}
- Verified by: Agent
- Date: {YYYY-MM-DD}
```

---

### Step 5.4: Get User Confirmation on Conflicts (If Any)

**If CRITICAL conflicts found, present to user:**

```markdown
## Cross-Feature Alignment: Conflicts Found

I compared Feature {N} ({Current}) to Feature {M} ({Completed}) and found {count} conflicts:

### Conflict 1: {Name}

**Issue:**
- Feature {N} assumes: {assumption 1}
- Feature {M} assumes: {assumption 2}
- These are incompatible because: {reason}

**Impact:**
- {What breaks if not resolved}

**Proposed Resolution:**
{Recommended fix}

**Alternatives:**
{Other options}

---

### Conflict 2: {Name}

{Same format}

---

**My Recommendation:**
{Overall recommendation for resolving conflicts}

**Do you approve this resolution?** (or suggest alternative)
```

**If user approves resolution:**
- Update spec.md and checklist.md
- Document approval in alignment report
- Update completed feature if needed
- Continue to Step 5.5

**If user suggests alternative:**
- Update spec.md with user's approach
- Document user decision
- Continue to Step 5.5

**If NO conflicts found:**
- Document "Zero conflicts with Feature {M}"
- No user confirmation needed
- Continue to Step 5.5

---

### Step 5.5: Document Alignment Verification

**Create summary in current feature's spec.md:**

```markdown
## Cross-Feature Alignment

**Compared To:**
- Feature {M}: {Name} (Stage 2 Complete) - {Date}

**Alignment Status:** ✅ No conflicts / ⚠️ Conflicts resolved

**Details:**
{Brief summary of comparison}

**Changes Made:**
{Any changes to this spec based on alignment}

**Verified By:** Agent
**Date:** {YYYY-MM-DD}
```

**Update Agent Status:**
```markdown
**Progress:** Phase 5 - COMPLETE (aligned with {N} features, {M} conflicts resolved)
**Next Action:** Phase 6 - Acceptance Criteria & User Approval
**Blockers:** None
```

---

## Phase 6: Acceptance Criteria & User Approval

**Goal:** Create user-facing summary of what this feature will do, get explicit approval

**⚠️ CRITICAL:** This is a MANDATORY gate. Cannot proceed to Stage 3 without user approval.

**Why this matters:**
- User needs to understand EXACTLY what will be implemented
- This is the last chance to adjust before implementation planning
- User approval locks the spec (changes after this require returning to Stage 2)

---

### Step 6.1: Create Acceptance Criteria Section

**Add to spec.md (near the end, before any appendices):**

```markdown
---

## Acceptance Criteria (USER MUST APPROVE)

**Feature {N}: {Name}**

When this feature is complete, the following will be true:

### Behavior Changes

**New Functionality:**
1. {Exact new behavior 1}
   - Example: "User can run `python run_simulation.py --use-adp` and simulation will incorporate ADP data"
2. {Exact new behavior 2}
   - Example: "PlayerManager will load ADP data from data/adp/fantasy_pros_adp.csv on initialization"

**Modified Functionality:**
1. {What changes in existing behavior}
   - Before: {How it works now}
   - After: {How it will work}

**No Changes:**
- {What explicitly does NOT change}
- Example: "Draft mode UI will not change"

---

### Files Modified

**New Files Created:**
1. `{path/to/new_file.py}`
   - Purpose: {What this file does}
   - Exports: {Classes/functions it provides}

2. `{path/to/another_file.py}`
   - Purpose: {What this file does}

**Existing Files Modified:**
1. `{path/to/existing_file.py}`
   - Lines modified: Approximately {range}
   - Changes: {Summary of changes}
   - Methods added: {List new methods}
   - Methods modified: {List modified methods}

**Data Files:**
1. `{path/to/data_file.csv}` (NEW)
   - Format: {Column structure}
   - Source: {Where data comes from}

---

### Data Structures

**New Data Structures:**
1. `{ClassName}` class
   - Location: {file path}
   - Fields: {List fields}
   - Purpose: {What it represents}

**Modified Data Structures:**
1. `{ExistingClass}` class
   - New fields: {List new fields}
   - Modified fields: {List modified fields}

---

### API/Interface Changes

**New Public Methods:**
1. `{ClassName}.{method_name}({params}) -> {return_type}`
   - Purpose: {What it does}
   - Parameters: {Describe each param}
   - Returns: {Describe return value}

**Modified Public Methods:**
1. `{ClassName}.{method_name}({params})`
   - Change: {What's different}
   - Backward compatible: {YES/NO}

**No API Changes:**
- {What methods/classes do NOT change}

---

### Testing

**New Tests:**
- Unit tests: ~{count} tests for new functionality
- Integration tests: {count} tests for feature interactions
- Test files: `tests/{path}/test_{feature}.py`

**Test Coverage:**
- Target: 100% coverage for new code
- Edge cases covered: {List key edge cases}

---

### Dependencies

**This Feature Depends On:**
- {Feature X} (must be implemented first)
- {Library Y} (must be installed)

**Features That Depend On This:**
- {Feature Z} (blocks until this completes)

**External Dependencies:**
- {Data source / API / file format}

---

### Edge Cases & Error Handling

**Edge Cases Handled:**
1. {Edge case 1}
   - Behavior: {How it's handled}
2. {Edge case 2}
   - Behavior: {How it's handled}

**Error Conditions:**
1. {Error condition 1}
   - User sees: {Error message}
   - System does: {Fallback behavior}

---

### Documentation

**User-Facing Documentation:**
- README.md updated with: {What sections}
- Examples added: {What examples}

**Developer Documentation:**
- Docstrings added to: {Which files}
- Architecture docs updated: {Which docs}

---

## User Approval

- [ ] **I approve these acceptance criteria**

**Approval Timestamp:** {YYYY-MM-DD HH:MM} (to be filled after approval)

**Approval Notes:**
{Any clarifications or modifications requested by user}
```

---

### Step 6.2: Present to User for Approval

**Message to user:**

```markdown
## Feature {N} ({Name}) - Ready for Approval

I've completed the deep dive for Feature {N}. Here's a summary:

**Spec Status:**
- All {N} checklist questions resolved
- Cross-feature alignment complete (compared to {M} features)
- Scope validated ({item_count} checklist items)

**What This Feature Will Do:**

{Brief 2-3 sentence summary}

**Impact:**
- Files modified: {count} new, {count} modified
- API changes: {summary}
- Dependencies: {summary}

**Full Details:**

Please review the "Acceptance Criteria" section in spec.md:
`feature-updates/{epic_name}/feature_{N}_{name}/spec.md`

**Acceptance Criteria Section includes:**
- Exact behavior changes
- All files that will be modified
- Data structure changes
- API/interface changes
- Testing approach
- Edge cases and error handling

**Next Steps:**

If you approve these acceptance criteria:
- I'll mark the approval checkbox and timestamp
- I'll mark Feature {N} as "Stage 2 Complete" in epic tracking
- I'll proceed to next feature (if any) or Stage 3 (Cross-Feature Sanity Check)

If you want changes:
- Let me know what to modify
- I'll update the spec and re-present for approval

**Do you approve these acceptance criteria?**
```

---

### Step 6.3: WAIT for User Approval

⚠️ **STOP HERE - Do NOT proceed without explicit user approval**

**Do NOT:**
- Mark feature complete without approval
- Proceed to next feature without approval
- Proceed to Stage 3 without approval
- Assume approval if user is silent

**DO:**
- Wait for explicit "yes", "approved", "looks good", etc.
- Answer any questions about acceptance criteria
- Make modifications if user requests changes
- Re-present if spec is updated

**Update Agent Status:**
```markdown
**Progress:** Phase 6 - Waiting for user approval of acceptance criteria
**Next Action:** Wait for user to approve/request changes
**Blockers:** Waiting for user approval on acceptance criteria
```

---

### Step 6.4: Handle User Response

**If user APPROVES:**

Update spec.md:
```markdown
## User Approval

- [x] **I approve these acceptance criteria**

**Approval Timestamp:** {YYYY-MM-DD HH:MM}

**Approval Notes:**
User approved on {date} with no modifications requested.
```

Continue to Step 6.5 (Mark Feature Complete)

---

**If user REQUESTS CHANGES:**

1. **Document requested changes:**
   ```markdown
   **User Feedback ({Date}):**
   - {Change request 1}
   - {Change request 2}
   ```

2. **Update spec.md based on feedback:**
   - Modify requirements
   - Update acceptance criteria
   - Adjust file modifications if needed

3. **Update checklist.md if new questions arose:**
   - Add new questions to checklist
   - Return to Phase 3 if major changes
   - Stay in Phase 6 if minor tweaks

4. **Re-present updated acceptance criteria:**
   ```markdown
   I've updated the acceptance criteria based on your feedback:

   **Changes Made:**
   - {Change 1}
   - {Change 2}

   **Updated Acceptance Criteria:**
   {Summary of updated criteria}

   **Do you approve the updated acceptance criteria?**
   ```

5. **Wait for approval again (return to Step 6.3)**

---

**If user REJECTS (major changes needed):**

1. **Document rejection:**
   ```markdown
   **User Rejection ({Date}):**
   Reason: {Why rejected}
   Required changes: {What needs to change fundamentally}
   ```

2. **Determine what phase to return to:**
   - **Fundamental misunderstanding:** Return to Phase 0 (Epic Intent)
   - **Research gap:** Return to Phase 1 (Targeted Research)
   - **Wrong requirements:** Return to Phase 2 (Spec & Checklist)
   - **Wrong answers to questions:** Return to Phase 3 (Question Resolution)

3. **Update Agent Status:**
   ```markdown
   **Progress:** Returning to Phase {N} due to user feedback
   **Next Action:** {Specific action needed}
   **Blockers:** None
   ```

4. **Return to appropriate phase and restart from there**

---

### Step 6.5: Mark Feature Complete (After Approval)

**Update feature README.md:**

```markdown
## Feature Completion Checklist

### Stage 2: Feature Deep Dive
- [x] Phase 0: Epic Intent Extraction
- [x] Phase 1: Targeted Research
- [x] Phase 1.5: Research Completeness Audit
- [x] Phase 2: Spec & Checklist Creation
- [x] Phase 2.5: Spec-to-Epic Alignment Check
- [x] Phase 3: Interactive Question Resolution
- [x] Phase 4: Dynamic Scope Adjustment
- [x] Phase 5: Cross-Feature Alignment
- [x] Phase 6: Acceptance Criteria & User Approval
- **Stage 2 Status:** ✅ COMPLETE
- **Completion Date:** {YYYY-MM-DD}

---

## Agent Status

**Last Updated:** {YYYY-MM-DD HH:MM}
**Current Phase:** DEEP_DIVE_COMPLETE
**Current Step:** Stage 2 complete, ready for Stage 3
**Current Guide:** N/A (between stages)
**Critical Rules:** Stage 2 complete, await next feature or Stage 3

**Progress:** Stage 2 COMPLETE
**Next Action:** {Proceed to next feature / Proceed to Stage 3}
**Blockers:** None
```

---

**Update epic EPIC_README.md:**

Find Feature Tracking table and mark Stage 2 complete:

```markdown
## Feature Tracking

| Feature | Name | Stage 2 Complete | Stage 5 Complete | Status |
|---------|------|------------------|------------------|--------|
| 01      | {Name} | [x] {Date} | [ ] | Stage 2 Done |
```

---

**Update Epic Completion Checklist:**

```markdown
## Epic Completion Checklist

### Stage 2: Feature Deep Dives (Loop for each feature)
- [x] Feature 01: Spec complete, user approved ({Date})
- [ ] Feature 02: Spec complete, user approved
```

---

**Announce completion to user:**

```markdown
✅ **Feature {N} ({Name}) - Stage 2 Complete**

**Summary:**
- Epic intent extracted and documented
- {N} questions resolved
- {M} requirements documented with traceability
- Cross-feature alignment complete ({K} features compared, {L} conflicts resolved)
- Acceptance criteria approved by user

**Files Updated:**
- spec.md: Complete with user approval
- checklist.md: All questions resolved
- README.md: Stage 2 marked complete
- epic/research/{FEATURE_NAME}_DISCOVERY.md: Research findings
- {epic}/EPIC_README.md: Feature tracking updated

**Next Steps:**

{IF more features remain:}
- Begin Stage 2 for next feature: Feature {N+1} ({Name})
- Repeat deep dive process

{IF all features complete Stage 2:}
- Transition to Stage 3 (Cross-Feature Sanity Check)
- Systematic comparison of all feature specs
- Get user sign-off on complete plan

**Ready to proceed?**
```

---

## Stage 2 Complete Checklist (Per Feature)

**Refinement Phase (STAGE_2c) is COMPLETE when ALL of these are true:**

### Phase Completion
- [ ] Phase 3: Interactive Question Resolution complete
  - All checklist questions resolved (zero open items)
  - Spec/checklist updated after each answer
  - No batched questions

- [ ] Phase 4: Dynamic Scope Adjustment complete
  - Checklist item count documented
  - If >35 items: Split proposed and user decided
  - New work evaluated (new feature vs expanded scope)

- [ ] Phase 5: Cross-Feature Alignment complete
  - Compared to all features with "Stage 2 Complete"
  - Conflicts identified and resolved
  - Alignment documented in spec.md

- [ ] Phase 6: Acceptance Criteria & User Approval complete
  - Acceptance Criteria section created in spec.md
  - Presented to user
  - User APPROVED (checkbox marked [x])
  - Approval timestamp documented

### File Outputs
- [ ] spec.md updated with:
  - All user answers incorporated as requirements
  - Cross-feature alignment notes
  - Acceptance Criteria section (user approved)
  - User approval checkbox marked [x]
  - Approval timestamp

- [ ] checklist.md shows:
  - ALL questions marked [x] (resolved)
  - User answers documented
  - No open [ ] questions

- [ ] README.md updated:
  - Feature Completion Checklist: Stage 2 marked complete
  - Agent Status: Phase = DEEP_DIVE_COMPLETE

### Epic-Level Updates
- [ ] Epic EPIC_README.md updated:
  - Feature Tracking table: "[x]" for this feature's Stage 2
  - Completion date documented

### Mandatory Gate
- [ ] ✅ Phase 6: User APPROVED acceptance criteria

**If ANY item unchecked → Refinement Phase NOT complete**

**When ALL items checked:**
✅ Refinement Phase COMPLETE
✅ Stage 2 COMPLETE for this feature
→ Proceed to next feature's Stage 2 OR Stage 3 (if all features done)

---

## Completion Criteria

**STAGE_2c (Refinement Phase) is complete when:**

1. **All phases complete:**
   - Phase 3: All questions resolved
   - Phase 4: Scope validated
   - Phase 5: Cross-feature alignment done
   - Phase 6: Acceptance criteria user-approved

2. **Files current:**
   - spec.md has acceptance criteria + user approval
   - checklist.md has zero open questions
   - README.md shows Stage 2 complete

3. **Epic updated:**
   - EPIC_README.md Feature Tracking shows "[x]" for Stage 2
   - No blockers or waiting states

4. **User approval obtained:**
   - Acceptance criteria approved
   - Approval checkbox marked [x]
   - Approval timestamp documented

**Next Stage:** Either next feature's STAGE_2a OR STAGE_3 (if all features complete)

---

## Next Steps

**After Refinement Phase completes:**

**If more features remain:**
- Begin Stage 2 for next feature
- Start with STAGE_2a (Research Phase)
- Repeat all phases (0 through 6)

**If ALL features complete Stage 2:**
- Transition to Stage 3 (Cross-Feature Sanity Check)

📖 **READ:** `STAGE_3_cross_feature_sanity_check_guide.md`
🎯 **GOAL:** Systematic comparison of all feature specs, final epic-level validation
⏱️ **ESTIMATE:** 30-60 minutes (for entire epic)

**Stage 3 will:**
- Verify acceptance criteria approved for ALL features (mandatory pre-check)
- Compare all feature specs side-by-side
- Identify remaining conflicts (missed in per-feature alignment)
- Ensure requirements are aligned across all features
- Get user sign-off on complete plan before Stage 4

**Remember:** Use the phase transition prompt from `prompts_reference_v2.md` when starting next feature or Stage 3.

---

*End of STAGE_2c_refinement_phase_guide.md*
