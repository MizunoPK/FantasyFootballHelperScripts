# Integrate New Player Data Into League Helper - Lessons Learned

> **PURPOSE**: This file captures issues encountered during development and QA that could have been prevented by better planning or development processes. After the feature is complete, these lessons will be used to update both guides in the `feature-updates/guides/` folder.

---

## How to Use This File

**When to add entries:**
1. During development: When you discover an edge case the planning phase should have identified
2. During development: When you find an issue that better verification would have caught
3. During QA: When testing reveals a problem the development process should have prevented
4. After user feedback: When the user reports something that wasn't working as expected

**What to capture:**
- What went wrong or was missed
- Why it happened (root cause)
- How the guides could be updated to prevent this in the future
- Specific additions or changes to recommend

---

## Lessons Learned

### Lesson 1: Interactive Question Resolution Process

**Date:** 2025-12-26

**What Happened (Symptom):**
During Phase 3 (Report and Pause), the agent presented all questions at once in a summary format. The user requested to "walk through the questions one by one and zoom in on each" for better decision-making.

**Immediate Cause:**
The planning guide does not explicitly instruct agents to resolve questions interactively with the user. The guide says to "present findings" but doesn't specify the format or interaction pattern.

**Root Cause Analysis:**

1. Why did the agent present all questions at once? → The planning guide says "present findings to user" without specifying interaction pattern
2. Why doesn't the guide specify interaction pattern? → Guide was written assuming batch presentation would be sufficient
3. Why was batch presentation assumed sufficient? → Guide didn't account for complex decisions requiring deep exploration
4. Why weren't complex decisions anticipated? → Guide is generic and doesn't model decision complexity
5. Why doesn't the guide model decision complexity? → **ROOT CAUSE: The planning guide lacks a structured protocol for iterative question resolution with user**

**Impact:**
- User had to explicitly request the one-by-one approach
- Could lead to rushed decisions if all questions dumped at once
- Misses opportunity to discover follow-up questions from each decision
- Less effective planning conversation

**Recommended Guide Update:**

**Which Guide:** `feature_planning_guide.md`

**Section to Update:** Phase 3: Report and Pause

**Recommended Change:**

Add explicit protocol for interactive question resolution:

```markdown
### Phase 3: Interactive Question Resolution

**CRITICAL: Do NOT present all questions at once. Follow this protocol:**

1. **Identify Priority Order:**
   - Critical architecture decisions first
   - Data mapping questions second
   - Implementation details last

2. **Present ONE Question at a Time:**
   - Provide full context for the question
   - Explain why it matters
   - Present options with pros/cons
   - Give your recommendation
   - Wait for user answer

3. **After EACH Answer:**
   - Update checklist with resolution
   - Update specs with decision details
   - **EVALUATE:** Does this decision create new questions?
   - If yes, add new questions to checklist
   - Document reasoning in specs

4. **Move to Next Question:**
   - Only after current question is fully resolved
   - Only after checklist/specs are updated
   - Only after new questions are identified

5. **Repeat Until All Resolved:**
   - Continue until checklist shows all items [x]
   - Confirm with user before moving to implementation

**Example Flow:**
```
Agent: "Question 1: Field mapping strategy - let me explain the options..."
[User provides answer]
Agent: "Updating checklist and specs... This decision creates 3 new questions about synchronization. Adding to checklist."
Agent: "Question 1a: Synchronization strategy - here's what we need to decide..."
[Continue until all questions resolved]
```

**Why this matters:**
- Allows user to make informed decisions with full context
- Discovers follow-up questions immediately
- Prevents decision regret from hasty choices
- Creates better documentation as decisions are made
```

**Systemic Fix:**
Add a mandatory step in Phase 3 workflow: "Interactive Question Resolution Protocol" that requires one-by-one discussion with checklist/specs updates after each answer and evaluation for new questions. This prevents the anti-pattern of "question dump" and ensures thorough exploration of each decision point.

---

### Lesson 2: Sub-Feature Breakdown Should Happen MUCH Earlier

**Date:** 2025-12-27

**What Happened (Symptom):**
After completing 47 planning decisions and creating 132 implementation items, the feature became unwieldy with 6 separate analysis documents, a 95KB monolithic spec file, and unclear dependencies. User requested breaking into sub-features at the END of planning, requiring significant reorganization work.

**Immediate Cause:**
The planning guide treats features as monolithic units throughout the entire planning phase. Only after all planning is complete does the agent create TODO files, at which point the complexity is already locked in.

**Root Cause Analysis:**

1. Why was the feature treated as monolithic until the end? → Planning guide doesn't have a sub-feature breakdown step
2. Why doesn't the guide have sub-feature breakdown? → Guide was designed for single-scope features
3. Why was it designed for single-scope features? → Didn't anticipate features growing to 132 items during research
4. Why didn't we anticipate large features? → No mechanism to detect and react to growing complexity during planning
5. Why no complexity detection mechanism? → **ROOT CAUSE: Planning guide lacks early assessment of feature scope and structured breakdown protocol**

**Impact:**
- Wasted effort: Created monolithic spec, then had to reorganize into 8 sub-features
- Confusing documentation: 6 analysis docs scattered at root level instead of organized
- Delayed recognition: Complexity issues not visible until planning complete
- Risk increase: 132 items in one feature = higher chance of cascading failures
- Harder resumption: Agents resuming work face overwhelming context

**Recommended Guide Update:**

**Which Guides:** Split `feature_planning_guide.md` into TWO separate guides

---

### NEW GUIDE STRUCTURE:

**Guide 1: `feature_creation_guide.md` (Initial Planning & Breakdown)**

**Purpose:** Initial feature setup, research, and sub-feature breakdown

**Phases:**
1. **Phase 1: Initial Setup**
   - Create feature folder
   - Move notes file
   - Create README.md

2. **Phase 2: Initial Research**
   - Read notes thoroughly
   - Do codebase reconnaissance (broad search, not deep dive)
   - Identify major components affected
   - Estimate rough scope (small/medium/large)

3. **Phase 3: Sub-Feature Breakdown Decision**
   - **CRITICAL CHECKPOINT:** Evaluate if feature should be broken down
   - **Triggers for breakdown:**
     - Affects 3+ major components
     - Estimated 30+ implementation items
     - Multiple independent subsystems
     - Different risk levels for different parts
   - **If breakdown needed:**
     - Propose logical sub-feature divisions
     - Explain dependencies between sub-features
     - Get user approval on breakdown strategy
   - **If NO breakdown needed:**
     - Continue with single feature approach
     - Create single spec and checklist

4. **Phase 4: Create Sub-Feature Structure** (if applicable)
   - Create `SUB_FEATURES_README.md` (master overview with implementation tracking)
   - Create `{feature_name}_sub_feature_{N}_{name}_spec.md` for EACH sub-feature
   - Create `{feature_name}_sub_feature_{N}_{name}_checklist.md` for EACH sub-feature
   - Create `research/` subfolder (for any research documents)
   - Document dependencies between sub-features
   - **IMPORTANT:** No global checklist or spec file - only sub-feature specific files

5. **Phase 5: Transition to Deep Dive**
   - Confirm all sub-feature files created
   - Identify which sub-feature to start with
   - Transition to Feature Deep Dive Guide

---

**Guide 2: `feature_deep_dive_guide.md` (Per-Subfeature Planning)**

**Purpose:** Detailed research and question resolution for ONE sub-feature at a time

**Scope:** Execute this guide ONCE per sub-feature. ALL sub-features must complete deep dive before proceeding to TODO creation.

**Phases:**

1. **Phase 1: Targeted Research**
   - Deep dive into THIS sub-feature's scope only
   - Codebase analysis specific to this component
   - Identify all files/methods/classes affected
   - Create research documents if needed (save to `research/` folder)
   - THREE-ITERATION question generation (MANDATORY)
   - CODEBASE VERIFICATION rounds (MANDATORY)

2. **Phase 2: Update Spec and Checklist**
   - Update THIS sub-feature's spec file with context
   - Update THIS sub-feature's checklist with questions
   - Create dependency map for this sub-feature
   - ASSUMPTIONS AUDIT (list all assumptions)

3. **Phase 3: Interactive Question Resolution**
   - Present questions ONE AT A TIME (per Lesson 1)
   - Update spec and checklist after each answer
   - Identify new questions arising from answers
   - Continue until ALL checklist items resolved

4. **Phase 4: Sub-Feature Complete**
   - Mark sub-feature as "Deep Dive Complete" in SUB_FEATURES_README.md
   - Verify all checklist items resolved
   - Confirm spec is comprehensive
   - **DYNAMIC SCOPE ADJUSTMENT:** If discoveries during deep dive significantly increase scope:
     - Propose creating additional sub-features to manage complexity
     - Get user approval for new breakdown
     - Create new sub-feature files if approved
     - Update SUB_FEATURES_README.md with new sub-features
   - **DO NOT** proceed to TODO creation yet

5. **Phase 5: Next Sub-Feature or Final Review**
   - If more sub-features remain: Repeat this guide for next sub-feature
   - If all sub-features complete: Proceed to Final Review

**Final Review (After ALL Sub-Features Complete Deep Dive):**

6. **Phase 6: Cross-Sub-Feature Alignment Review** (MANDATORY)
   - Review all sub-feature specs together
   - Check for conflicting changes or assumptions
   - Verify dependency order is correct
   - Ensure interface contracts align
   - Update any conflicting specs
   - Get user confirmation on alignment

7. **Phase 7: Ready for Sequential Implementation**
   - All sub-features have complete specs and checklists
   - All cross-sub-feature conflicts resolved
   - Dependencies documented and verified
   - Ready to begin sequential sub-feature implementation
   - **NEXT:** Execute full implementation cycle for FIRST sub-feature

---

### KEY WORKFLOW CHANGES:

**OLD Workflow (Current):**
```
feature_planning_guide.md (monolithic)
  → Phase 1: Setup
  → Phase 2: Research (ENTIRE feature)
  → Phase 3: Report & Pause
  → Phase 4: Resolve Questions (ENTIRE feature)
  → Planning Complete
  → todo_creation_guide.md (monolithic)
  → implementation_execution_guide.md
```

**NEW Workflow (Recommended):**
```
feature_creation_guide.md
  → Phase 1: Initial Setup
  → Phase 2: Initial Research (broad scan)
  → Phase 3: Sub-Feature Breakdown Decision
  → Phase 4: Create Sub-Feature Structure
  → Phase 5: Transition

FOR EACH SUB-FEATURE:
  feature_deep_dive_guide.md (per sub-feature)
    → Phase 1: Targeted Research
    → Phase 2: Update Spec/Checklist
    → Phase 3: Interactive Question Resolution
    → Phase 4: Mark Complete
    → Phase 5: Next Sub-Feature

  (repeat until all sub-features complete)

Cross-Sub-Feature Alignment Review (MANDATORY)
  → Phase 6: Review all specs together
  → Phase 7: Resolve conflicts

FOR EACH SUB-FEATURE (Sequential, One at a Time):
  todo_creation_guide.md (FULL 24 iterations - NO SKIPPING)
    → Create {subfeature}_todo.md
    → Interface verification
    → Algorithm traceability

  implementation_execution_guide.md (FULL process - NO SKIPPING)
    → Code implementation
    → Unit tests (100% pass required)
    → Integration tests with other completed sub-features

  post_implementation_guide.md (FULL QC - NO SKIPPING)
    → QC Round 1: Requirement verification
    → QC Round 2: Code quality
    → QC Round 3: Integration verification
    → SMOKE TESTING PROTOCOL (all 3 parts - MANDATORY)

  Commit Changes (one commit per sub-feature)
    → Git commit with sub-feature completion message
    → Mark sub-feature complete in SUB_FEATURES_README.md

  (Repeat for next sub-feature until all complete)

Final Feature Completion:
  → All sub-features implemented and tested
  → Full integration test across all sub-features
  → Final smoke testing protocol
  → Move entire feature folder to done/
```

---

### RULES FOR SUB-FEATURE BREAKDOWN:

**When to Break Down:**
- Feature affects 3+ major components (different managers, modes, subsystems)
- Estimated scope > 30 implementation items
- Mix of different risk levels (some high-risk, some low-risk changes)
- Independent subsystems that can be developed in parallel
- User explicitly requests breakdown

**When NOT to Break Down:**
- Single component affected (e.g., one class, one file)
- Estimated scope < 20 items
- All changes tightly coupled (can't be separated)
- Simple, straightforward feature

**Sub-Feature Characteristics:**
- Each sub-feature has clear scope (15-30 items ideal)
- Dependencies between sub-features are explicit
- Each can be tested independently
- Each has its own spec and checklist files
- Research documents shared in `research/` folder

**File Naming Convention:**
- `{feature_name}_sub_feature_01_{descriptive_name}_spec.md`
- `{feature_name}_sub_feature_01_{descriptive_name}_checklist.md`
- Master overview: `SUB_FEATURES_README.md`
- Shared research: `research/{research_document}.md`

---

### CRITICAL: Research Document Organization

**ALL research documents must go in `research/` subfolder from the start:**
- `research/README.md` - Overview of research findings
- `research/{TOPIC_NAME}_ANALYSIS.md` - Individual analysis documents
- `research/VERIFICATION_REPORT_{DATE}.md` - Verification findings
- `research/RESEARCH_FINDINGS_{DATE}.md` - General research

**Benefits:**
- Cleaner root folder (only specs, checklists, and README)
- Easier to find reference material
- Clear separation: specs = implementation guidance, research = context/decisions
- Can be moved to done/ folder intact

---

**Why This Matters:**

**Early Breakdown:**
- Prevents overwhelming complexity from accumulating
- Identifies parallelization opportunities early
- Reduces risk through smaller, testable units
- Easier for agents to resume work (smaller context)
- Better error isolation during implementation

**Two-Guide Structure:**
- Clear separation: broad vs deep planning
- Systematic approach to sub-features
- Prevents monolithic specs
- Ensures alignment through mandatory review
- Scalable to any feature size

**Per-Sub-Feature Deep Dive:**
- Focused research (not distracted by other components)
- Better question resolution (smaller scope)
- Independent testing possible
- Parallel development enabled
- Clearer dependencies

**Sequential Implementation:**
- Complete TODO → Implementation → Post-Implementation for ONE sub-feature at a time
- Full quality gates (no skipping: smoke testing, integration testing, QC rounds)
- One commit per sub-feature (clear progress tracking)
- Each sub-feature fully validated before starting next
- Integration testing includes previously completed sub-features
- Reduces risk: if sub-feature fails, others not affected

**Dynamic Scope Management:**
- Agent monitors scope during deep dive
- Proposes new sub-features if scope grows significantly
- Prevents sub-features from becoming too large
- Maintains manageable complexity throughout

**File Structure:**
- No global checklist or spec file
- Only sub-feature-specific files
- SUB_FEATURES_README.md tracks overall progress
- Cleaner organization, focused documentation

**This lesson is HIGH PRIORITY** - impacts fundamental workflow structure

---

### Lesson 3: Skipping Codebase Verification Rounds During Deep Dive

**Date:** 2025-12-27

**What Happened (Symptom):**
During Phase 1 of the deep dive guide for Sub-feature 1 (Core Data Loading), the agent completed "targeted research" but then immediately jumped to Phase 6 (Cross-Sub-Feature Alignment Review) WITHOUT performing the mandatory CODEBASE VERIFICATION ROUNDS specified in the guide (Step 1.3). This resulted in all 29 checklist items remaining unchecked `[ ]` with no pattern verification, no recommendations documented, and no decisions resolved. The user had to explicitly ask "are there no new checklist items to go through?" to catch this error.

**Immediate Cause:**
The agent misunderstood "targeted research" as "read some files to understand the area" rather than "systematically verify every checklist item against the codebase and document findings."

**Root Cause Analysis:**

1. Why did the agent skip verification rounds? → Agent didn't recognize Step 1.3 as mandatory for EVERY checklist item
2. Why wasn't Step 1.3 recognized as mandatory? → Guide says "MANDATORY" but agent treated research as complete after reading a few files
3. Why did agent treat research as complete early? → Agent saw that "policy decisions were already resolved" and assumed no work needed
4. Why assume no work needed? → Agent didn't understand the DIFFERENCE between:
   - **Policy decisions** (already resolved during initial planning - marked `[x]`)
   - **Implementation items** (need pattern verification from codebase - NOT automatically `[x]`)
5. Why confusion between policy and implementation items? → **ROOT CAUSE: Deep dive guide doesn't explicitly state that EVERY `[ ]` item needs verification, and doesn't distinguish between different types of checklist items clearly enough**

**Impact:**
- **29 items left unverified** - no pattern identification from codebase
- **No recommendations documented** - implementation would proceed without guidance
- **Wasted implementation time** - developer would have to discover patterns themselves during coding
- **Risk of inconsistency** - without pattern verification, new code might not match existing code style
- **User intervention required** - user had to notice the gap and ask about it
- **False confidence** - agent reported "deep dive complete" when critical work was skipped

**What SHOULD Have Happened:**

According to `feature_deep_dive_guide.md` Step 1.3, the agent should have:

**Round 1: Codebase Verification**
- For EACH `[ ]` checklist item (all 29 items):
  - **Straightforward verification items:** Search codebase to verify yes/no → Mark `[x]` with findings
  - **Decision/ambiguous items:** Research patterns, list options with pros/cons, ADD RECOMMENDATION → Keep `[ ]` for user but WITH full context
  - **Consumer identification:** Grep for where outputs are used, identify ALL consumers, verify format

**Round 2: Skeptical Re-verification**
- Re-verify findings from Round 1 to catch mistakes

**Result Expected:**
- Many items marked `[x]` with verification notes
- Decision items remain `[ ]` but have researched options + recommendations
- Clear implementation patterns documented

**What ACTUALLY Happened:**
- Read 3-4 files for general understanding
- Declared "research complete"
- Moved to alignment review with 29 unchecked items

**Recommended Guide Updates:**

**Which Guide:** `feature_deep_dive_guide.md`

**Section to Update:** Step 1.3: CODEBASE VERIFICATION Rounds (MANDATORY)

**Recommended Changes:**

1. **Add explicit item count requirement:**
```markdown
### Step 1.3: CODEBASE VERIFICATION Rounds (MANDATORY)

**CRITICAL: This step is MANDATORY for EVERY unchecked `[ ]` item in the checklist.**

**Before starting:**
- Count total `[ ]` items in checklist (exclude `[x]` items already resolved)
- Document: "Starting verification for {N} items"

**After Round 1:**
- Count items marked `[x]` after verification
- Count items remaining `[ ]` with research documented
- Verify: Total items = Marked + Remaining
- **STOP if numbers don't match** - you missed items

**Completion criteria:**
- ALL items have EITHER:
  - `[x]` with verification findings documented, OR
  - `[ ]` with researched options + recommendation documented
- NO items should remain `[ ]` without research
```

2. **Add explicit distinction between item types:**
```markdown
### Understanding Checklist Item Types

**Policy Decisions (Already `[x]` from initial planning):**
- Example: "NEW-44: Position-specific field policy ✅ RESOLVED"
- **Action:** None needed - already complete
- **Skip these** - focus on `[ ]` items

**Implementation Tasks (Currently `[ ]`):**
- Example: "NEW-14: Validate arrays have exactly 17 elements (pad if needed)"
- **Action Required:** Research existing code patterns, document recommendation
- **Mark as:** `[x]` with pattern verification notes

**Testing Tasks (Currently `[ ]`):**
- Example: "TEST-1: Test FantasyPlayer.from_json() with complete QB data"
- **Action Required:** None during deep dive (testing comes later)
- **Mark as:** Leave as `[ ]` - no verification needed
- **Note:** Add comment "(Testing - no verification needed during deep dive)"
```

3. **Add progress tracking template:**
```markdown
### Verification Progress Template

**Start of Step 1.3:**
```
Total checklist items: {X}
Already resolved (policy decisions): {Y} items marked `[x]`
Need verification (implementation): {Z} items currently `[ ]`
Testing items (defer): {T} items (no verification needed)

Target: Verify {Z} items, leave {T} as `[ ]` with note
```

**After Round 1:**
```
Verified and marked `[x]`: {A} items
Researched with recommendation (still `[ ]`): {B} items
Testing (deferred): {T} items
Total: {A + B + T} should equal {Z + T}

✅ All items processed
[ ] Missing items - RECOUNT
```

4. **Add examples of what verification looks like:**
```markdown
### Verification Example

**BEFORE (incomplete):**
```markdown
- [ ] **NEW-14:** Validate arrays have exactly 17 elements (pad if needed)
```

**AFTER (verification complete):**
```markdown
- [x] **NEW-14:** Validate arrays have exactly 17 elements (pad if needed) ✅ VERIFIED
  - **Pattern from codebase:** Lenient approach - no strict validation found in existing code
  - **Recommendation:** Pad if too short, truncate if too long, log warning for mismatches
  - **Rationale:** Matches existing lenient pattern (skip bad data with warnings, don't fail)
  - **Implementation:** `(array + [0.0] * 17)[:17]` - simple one-liner
  - **Reference:** FantasyPlayer.from_dict() uses safe_*_conversion helpers (lines 159-194)
```

**Key differences:**
- Marked `[x]` (resolved)
- Pattern from actual codebase identified
- Specific recommendation given
- Rationale explains why
- Implementation approach suggested
- Line numbers referenced
```

**Systemic Fix:**

Add MANDATORY verification checkpoint in feature_deep_dive_guide.md Phase 1:
- **Before Phase 2:** Count checklist items (total, resolved, needing verification, testing)
- **During Step 1.3:** Systematically verify EACH item, document findings
- **After Step 1.3:** Recount to verify ALL items processed
- **Error if mismatch:** "Found {X} unprocessed items - returning to verification"

This prevents the anti-pattern of "I read some code and understand the area" being confused with "I verified every checklist item against the codebase."

**Why This Matters:**

**Pattern Verification:**
- Ensures new code matches existing code style
- Identifies safe conversion helpers, error handling patterns, logging conventions
- Documents "how we do things here" for implementation

**Recommendation Documentation:**
- Gives implementer clear guidance on approach
- Reduces decision-making during coding (decisions made during planning)
- Creates reviewable specification (user can see and approve patterns)

**Quality Assurance:**
- Catches mismatches between spec assumptions and actual code
- Identifies missing consumers that need updating
- Verifies interfaces match reality

**Implementation Efficiency:**
- Developer doesn't have to discover patterns during coding
- Clear examples from existing code to follow
- Reduces "figure it out as I go" time

**This lesson is CRITICAL PRIORITY** - skipping verification undermines the entire deep dive phase purpose

---

### Lesson 4: Sub-Feature Phase Completion Tracking

**Date:** 2025-12-28

**What Happened (Symptom):**
During deep dive work, the agent completed Phases 1-2 (Research and Spec Updates) for Sub-features 1-6, but did not proceed to Phase 3 (Interactive Question Resolution) or complete Phases 1-2 for Sub-features 7-8. There was no systematic tracking to ensure all 8 sub-features went through all required phases before proceeding to Phase 6 (Alignment Review) and Phase 7 (Ready for Implementation).

**Immediate Cause:**
No dedicated tracking mechanism exists to monitor which phases each sub-feature has completed. Progress was tracked informally in conversation and the DEEP_DIVE_SUMMARY.md, but there was no structured checklist ensuring all sub-features completed all phases systematically. More critically, there was no tracking of the 24 TODO creation iterations, implementation sub-phases, or 3 QC rounds - meaning agents could skip critical verification steps without detection.

**Root Cause Analysis:**

1. Why didn't the agent complete all phases for all sub-features? → No systematic tracker showing which phases were complete vs incomplete
2. Why was there no systematic tracker? → Feature creation guide doesn't require creating a phase completion tracking file
3. Why doesn't the guide require a tracker? → Guide assumes agents will naturally track progress through all phases
4. Why is this assumption wrong? → Multi-sub-feature projects have complex phase × sub-feature matrix (8 sub-features × 7 phases = 56 checkpoints)
5. **ROOT CAUSE:** No dedicated tracking file created during feature creation to ensure systematic completion of all phases across all sub-features

**Impact:**
- **Planning phase:** Easy to lose track which sub-features completed which phases (6/8 done Phase 2 vs 8/8)
- **Critical skipping risk:** Phase 3 (User Questions) can be completely forgotten without tracking
- **TODO creation:** No visibility into which of 24 iterations are complete (could skip Round 2 entirely)
- **Implementation:** No tracking of which TODO groups complete, mini-QC checkpoints, or continuous testing
- **QC phase:** Could skip QC Round 2 or smoke testing entirely - no way to verify completion
- **Agent resumption:** Agents resuming after context limits don't know where to continue (reconstruct from conversation)
- **Quality gates:** Phase 6 requires ALL sub-features complete Phase 4 - no systematic verification possible
- **Guide compliance:** No enforcement of re-reading guides before marking phases complete (agents rely on memory)
- **Audit trail:** No record of when phases completed or by which agent session

**Recommended Guide Update:**

**Add to feature_creation_guide.md (when creating sub-features):**

Create mandatory `SUB_FEATURES_PHASE_TRACKER.md` file with this template:

```markdown
# Sub-Feature Phase Completion Tracker

**Purpose:** Complete source of truth tracking each sub-feature's progress through ALL phases (planning, TODO creation, implementation, QC) to ensure systematic completion.

**Instructions:**
- Mark `[x]` when phase/sub-phase is 100% complete for that sub-feature
- DO NOT skip phases or sub-phases
- **MANDATORY: Re-read the corresponding guide BEFORE marking any phase complete** to verify all steps were followed
- Update "Current Status" section after each phase completion

---

## Phase Completion Matrix

### Sub-feature 1: {Name}

**Planning Phases (feature_deep_dive_guide.md):**
- [ ] Phase 1: Targeted Research
  - [ ] Step 1.1: Identify files and components
  - [ ] Step 1.2: THREE-ITERATION question generation (core, quality, cross-cutting)
  - [ ] Step 1.3: CODEBASE VERIFICATION rounds (2 rounds minimum)
  - [ ] Step 1.4: Create research documents (if needed)
  - [ ] **Re-read guide before marking complete**
- [ ] Phase 2: Update Spec and Checklist
  - [ ] Step 2.1: Update spec with findings
  - [ ] Step 2.2: Create dependency map
  - [ ] Step 2.3: ASSUMPTIONS AUDIT
  - [ ] Step 2.4: Populate checklist
  - [ ] **Re-read guide before marking complete**
- [ ] Phase 3: Interactive Question Resolution
  - [ ] Step 3.1: Prioritize questions
  - [ ] Step 3.2-3.5: ONE question at a time (all user decisions resolved)
  - [ ] **Re-read guide before marking complete**
- [ ] Phase 4: Sub-Feature Complete + Scope Check
  - [ ] Step 4.1: Verify completion (all checklist items `[x]`)
  - [ ] Step 4.2: Dynamic scope adjustment check
  - [ ] Step 4.3: Mark sub-feature complete in SUB_FEATURES_README.md
  - [ ] **Re-read guide before marking complete**

**TODO Creation Phase (todo_creation_guide.md):**
- [ ] Round 1: Iterations 1-7
  - [ ] Iteration 1: Initial TODO list creation from spec
  - [ ] Iteration 2: Dependency analysis
  - [ ] Iteration 3: Interface verification
  - [ ] Iteration 4: Algorithm traceability matrix
  - [ ] Iteration 4a: TODO specification audit
  - [ ] Iteration 5: Error path coverage
  - [ ] Iteration 6: Test coverage planning
  - [ ] Iteration 7: Round 1 completion checkpoint
- [ ] Round 2: Iterations 8-16
  - [ ] Iteration 8: Consumer identification
  - [ ] Iteration 9: Data flow validation
  - [ ] Iteration 10: Edge case enumeration
  - [ ] Iteration 11: Algorithm traceability matrix (update)
  - [ ] Iteration 12: Logging strategy
  - [ ] Iteration 13: Performance considerations
  - [ ] Iteration 14: Security review
  - [ ] Iteration 15: Backwards compatibility check
  - [ ] Iteration 16: Round 2 completion checkpoint
- [ ] Round 3: Iterations 17-24
  - [ ] Iteration 17: Integration points verification
  - [ ] Iteration 18: Documentation requirements
  - [ ] Iteration 19: Algorithm traceability matrix (final)
  - [ ] Iteration 20: Success criteria validation
  - [ ] Iteration 21: Rollback strategy
  - [ ] Iteration 22: Migration path verification
  - [ ] Iteration 23: Final TODO review
  - [ ] Iteration 23a: Questions file creation (if needed)
  - [ ] Iteration 24: FINAL CHECKPOINT - Ready for implementation
  - [ ] **Re-read guide before marking complete**

**Implementation Phase (implementation_execution_guide.md):**
- [ ] Setup and Preparation
  - [ ] Create implementation checklist
  - [ ] Interface verification (actual source code)
  - [ ] Environment setup
  - [ ] **Re-read guide sections before starting**
- [ ] Execution (by TODO group)
  - [ ] Group 1: {Description} - All TODOs complete
  - [ ] Group 2: {Description} - All TODOs complete
  - [ ] Group 3: {Description} - All TODOs complete
  - [ ] [Add groups as needed based on TODO file]
- [ ] Continuous Verification
  - [ ] Mini-QC checkpoint after each group
  - [ ] Unit tests 100% pass after each major component
  - [ ] Spec verification (implementation matches spec)
- [ ] Documentation
  - [ ] Code changes documented in {name}_code_changes.md
  - [ ] All modifications tracked incrementally
  - [ ] **Re-read guide before marking complete**

**Post-Implementation QC (post_implementation_guide.md):**
- [ ] Smoke Testing (MANDATORY - 3 parts)
  - [ ] Part 1: Core functionality smoke test
  - [ ] Part 2: Integration smoke test
  - [ ] Part 3: Edge case smoke test
- [ ] QC Round 1: Code Quality
  - [ ] Code review checklist
  - [ ] Style consistency
  - [ ] Documentation completeness
  - [ ] Round 1 issues resolved
- [ ] QC Round 2: Functional Correctness
  - [ ] Spec alignment verification
  - [ ] All success criteria met
  - [ ] Integration tests passing
  - [ ] Round 2 issues resolved
- [ ] QC Round 3: Production Readiness
  - [ ] Error handling verified
  - [ ] Performance acceptable
  - [ ] Security reviewed
  - [ ] Round 3 issues resolved
- [ ] Final Steps
  - [ ] ALL unit tests passing (100%)
  - [ ] Lessons learned documented
  - [ ] **Re-read guide before marking complete**

**Completion:**
- [ ] Changes committed (with descriptive message)
- [ ] Feature folder moved to done/

---

### Sub-feature 2: {Name}

**Planning Phases (feature_deep_dive_guide.md):**
- [ ] Phase 1: Targeted Research (4 steps + re-read guide)
- [ ] Phase 2: Update Spec and Checklist (4 steps + re-read guide)
- [ ] Phase 3: Interactive Question Resolution (all user decisions + re-read guide)
- [ ] Phase 4: Sub-Feature Complete + Scope Check (3 steps + re-read guide)

**TODO Creation Phase (todo_creation_guide.md):**
- [ ] Round 1: Iterations 1-7 (including 4a)
- [ ] Round 2: Iterations 8-16
- [ ] Round 3: Iterations 17-24 (including 23a + re-read guide)

**Implementation Phase (implementation_execution_guide.md):**
- [ ] Setup and Preparation (interface verification + re-read guide)
- [ ] Execution (all TODO groups complete)
- [ ] Continuous Verification (mini-QC + tests)
- [ ] Documentation (code_changes.md + re-read guide)

**Post-Implementation QC (post_implementation_guide.md):**
- [ ] Smoke Testing (3 parts)
- [ ] QC Round 1: Code Quality
- [ ] QC Round 2: Functional Correctness
- [ ] QC Round 3: Production Readiness
- [ ] Final Steps (tests + lessons + re-read guide)

**Completion:**
- [ ] Committed and moved to done/

---

[Repeat for ALL sub-features with same detailed breakdown]

---

## Cross-Sub-Feature Phases

**Execute ONLY after ALL sub-features complete their Phase 4:**

- [ ] Phase 6: Cross-Sub-Feature Alignment Review (feature_deep_dive_guide.md Phase 6)
  - [ ] Step 6.1: Review all specs together
  - [ ] Step 6.2: Check for conflicts (interface, naming, duplication, dependencies)
  - [ ] Step 6.3: Update conflicting specs
  - [ ] Step 6.4: Verify dependency chain (no circular dependencies)
  - [ ] Step 6.5: Get user confirmation
  - [ ] **Re-read guide before marking complete**
- [ ] Phase 7: Ready for Implementation (feature_deep_dive_guide.md Phase 7)
  - [ ] Step 7.1: Final verification (all specs complete, conflicts resolved)
  - [ ] Step 7.2: Update README status to "IMPLEMENTATION - Ready for TODO creation"
  - [ ] Step 7.3: Document implementation order
  - [ ] Step 7.4: Announce readiness
  - [ ] **Re-read guide before marking complete**

---

## Quality Gates

**Before Phase 6 Alignment Review:**
- [ ] ALL sub-features marked complete in Phase 4 above (all checklist items `[x]`)
- [ ] ALL user decisions from Phase 3 documented in specs
- [ ] ALL verification findings from Phase 1-2 documented in specs
- [ ] ALL research documents in research/ folder

**Before Phase 7 Ready for Implementation:**
- [ ] Phase 6 alignment review complete
- [ ] All conflicts resolved and documented
- [ ] Dependency order verified (no circular dependencies)
- [ ] Implementation order documented in SUB_FEATURES_README.md

**Before Starting TODO Creation for ANY Sub-Feature:**
- [ ] Phase 7 complete (all sub-features aligned)
- [ ] Sub-feature specs final and locked
- [ ] All prerequisites for that sub-feature complete

---

## Current Status

**Last updated:** {Date/Time}
**Sub-features complete (Phase 4):** {X} / {N}
**Current phase:** {Description}
**Current sub-feature:** {Name or "N/A"}
**Next action:** {What to do next}
**Blockers:** {Any blockers preventing progress}

---

## Agent Instructions

**At START of every session:**
1. Read this tracker file FIRST (before doing any other work)
2. Check "Current Status" to understand where previous agent left off
3. Identify next unchecked item in the matrix
4. Re-read corresponding guide section before starting work

**Before marking ANY phase complete:**
1. Re-read the ENTIRE corresponding guide (not just skimming)
2. Verify ALL steps in that phase were completed
3. Verify ALL sub-steps if phase has breakdown
4. Update "Current Status" section with new status
5. Mark `[x]` only if 100% confident phase is complete

**After completing each phase:**
1. Update "Current Status" immediately
2. Identify next phase to work on
3. Check quality gates if approaching Phase 6 or 7
```

**When to use:**
- **START OF EVERY SESSION:** Agent checks this file BEFORE any other work
- **BEFORE marking phase complete:** Agent re-reads corresponding guide to verify all steps followed
- **AFTER completing phase:** Agent updates `[x]` and "Current Status" immediately
- **BEFORE Phase 6/7:** Agent verifies quality gates are met
- **AGENT RESUMPTION:** Next agent reads "Current Status" to know where to continue
- **THROUGHOUT IMPLEMENTATION:** Track TODO creation, implementation, and QC progress

**Benefits:**
- **Complete lifecycle tracking:** Planning, TODO creation (24 iterations), implementation, QC (3 rounds) - all tracked
- **Single source of truth:** No ambiguity about what's complete vs incomplete
- **Prevents phase skipping:** Can't skip Phase 3 questions or Round 2 of TODO creation
- **Guide compliance:** Mandatory re-reading ensures all steps actually followed
- **Agent resumption:** Next agent knows exactly where to continue (no progress reconstruction)
- **Quality gates:** Enforces systematic completion before proceeding
- **Detailed progress visibility:** Can see exactly which iteration of TODO creation is complete
- **Audit trail:** Shows what was completed when throughout entire lifecycle

**Location:** Create in feature folder root: `feature-updates/{feature-name}/SUB_FEATURES_PHASE_TRACKER.md`

**Systemic Fix:**

Add to feature_creation_guide.md when creating sub-feature structure:

**After creating SUB_FEATURES_README.md, MANDATORY: Create SUB_FEATURES_PHASE_TRACKER.md**
- One section per sub-feature with DETAILED breakdown:
  - 4 planning phases (with all sub-steps)
  - 24 TODO creation iterations (grouped in 3 rounds)
  - Implementation phase (setup, execution groups, verification, documentation)
  - Post-implementation QC (smoke testing + 3 QC rounds)
  - Completion checkpoint (commit + move to done/)
- Cross-sub-feature phases (6-7) with sub-steps
- Quality gates at critical transition points
- Current status section with timestamp and next action
- Agent instructions for using the tracker
- **MANDATORY re-read requirement** before marking any phase complete

This ensures:
- No sub-feature gets "lost" in the complexity
- All phases completed systematically with guide compliance
- Complete audit trail from planning through QC
- Agents can resume at any point with full context

**Why This Matters:**

**Comprehensive Progress Tracking:**
- Tracks 100+ checkpoints per sub-feature across entire lifecycle
- Visual progress: See "Round 2, Iteration 12 of TODO creation" vs vague "TODO creation in progress"
- Eliminates "we did some work but I'm not sure what's left" confusion
- Shows exactly where agent is in 24-iteration TODO creation process

**Guide Compliance Enforcement:**
- **MANDATORY re-read before marking complete** prevents "I think I did it right" mistakes
- Forces verification against actual guide steps
- Catches missed sub-steps (e.g., Algorithm Traceability Matrix updates)
- Ensures quality (can't skip Round 2 of TODO creation verification)

**Phase Skipping Prevention:**
- Can't mark Iteration 11 complete without Iterations 1-10 being `[x]`
- Can't start Implementation without all 24 TODO iterations complete
- Can't skip QC Round 2 and jump to Round 3
- Quality gates enforce prerequisites (Phase 7 requires Phase 6 complete for ALL sub-features)

**Agent Resumption Support:**
- Next agent reads tracker file at START of session
- "Current Status" section shows: "Sub-feature 3, TODO Creation, Round 2, Iteration 14"
- No reconstruction needed - exact checkpoint preserved
- Agent knows to re-read todo_creation_guide.md before continuing

**Quality Assurance:**
- Enforces systematic completion (no shortcuts)
- Quality gates at major transitions (planning→TODO, TODO→implementation, implementation→QC)
- Audit trail: Shows when each phase completed
- Tracks QC rounds separately (prevents "one QC pass and done" shortcuts)
- Smoke testing explicitly tracked (prevents skipping)

**Complete Source of Truth:**
- Replaces scattered progress notes across multiple files
- One place to check overall feature status
- Tracks both "what's done" AND "what's next"
- Shows blockers preventing progress
- Timestamp shows when last updated (detects stale status)

**This lesson is CRITICAL PRIORITY** - complex multi-sub-feature projects require comprehensive tracking of 800+ total checkpoints (8 sub-features × 100+ checkpoints each). Without structured tracking, phase skipping and incomplete work is inevitable.

---

### Lesson 5: Nearly Skipped Post-Implementation QC for Sub-Feature 1

**Date:** 2025-12-28

**What Happened (Symptom):**
After completing implementation and all tests passing (2,394/2,394 - 100%) for Sub-feature 1 (Core Data Loading), the agent declared the sub-feature "COMPLETE" and created `sub_feature_01_IMPLEMENTATION_COMPLETE.md` without executing the mandatory Post-Implementation QC protocol. The agent immediately moved to start TODO creation for Sub-feature 2. User caught this error by asking: "wait - did the post-implementation steps get run for sub-1?"

**Immediate Cause:**
The agent assumed that passing tests = feature complete, without recognizing that Phase 2c (Post-Implementation QC) is a separate mandatory phase that must be executed after Phase 2b (Implementation).

**Root Cause Analysis:**

1. Why did agent skip post-implementation QC? → Agent assumed "all tests passing" means work is complete
2. Why was tests passing assumed to mean complete? → Agent didn't recognize post-implementation QC as mandatory separate phase
3. Why wasn't post-implementation recognized as mandatory? → Agent didn't consult SUB_FEATURES_PHASE_TRACKER.md or phase transition protocol
4. Why wasn't tracker consulted? → Agent focused on implementation completion without checking full workflow
5. **ROOT CAUSE:** No automatic trigger or reminder to execute post-implementation QC after implementation phase completes. Agent must remember to transition phases manually, creating skipping risk.

**Impact:**
- **Quality risk:** Could have proceeded to Sub-feature 2 with unverified Sub-feature 1 code
- **Missing verification:** Would have skipped:
  - Requirement verification (29 requirements unverified against implementation)
  - Smoke Testing Protocol (3 parts - MANDATORY per guide)
  - QC Round 1 (code conventions, docstrings, structural alignment)
  - QC Round 2 (deep verification, regressions, semantic correctness)
  - QC Round 3 (final skeptical review, completeness verification)
  - Lessons learned documentation
- **User intervention required:** User had to catch the skip and explicitly request QC execution
- **Wasted time:** Retroactive QC execution after declaring complete (had to retract completion claim)
- **False confidence:** Declared "IMPLEMENTATION COMPLETE" prematurely without full quality validation
- **Documentation gap:** Created completion file before actually being complete

**What SHOULD Have Happened:**

According to the workflow guides and phase transition protocol:

**After Implementation Phase 2b Complete:**
1. **DO NOT** declare sub-feature complete
2. **DO NOT** create "IMPLEMENTATION_COMPLETE.md" file
3. **MANDATORY:** Use "Starting Post-Implementation QC" prompt from `prompts_reference.md`
4. **READ:** `post_implementation_guide.md` in full
5. **EXECUTE:** All 8 steps of post-implementation protocol:
   - Step 1: Run full test suite (verify 100% pass)
   - Step 2: Requirement verification (create verification matrix)
   - Step 3: Smoke Testing Protocol (3 parts - MANDATORY)
   - Step 4: QC Round 1 (code quality)
   - Step 5: QC Round 2 (functional correctness)
   - Step 6: QC Round 3 (production readiness)
   - Step 7: Lessons learned documentation
   - Step 8: Completion checklist (verify all success criteria)
6. **ONLY THEN:** Mark sub-feature complete and proceed to next sub-feature

**What ACTUALLY Happened:**
- Tests passed → immediately declared "IMPLEMENTATION COMPLETE"
- Created completion file without QC
- Moved to Sub-feature 2 TODO creation
- User caught the skip: "wait - did the post-implementation steps get run for sub-1?"
- Had to retroactively execute full 8-step protocol

**Recommended Guide Updates:**

**Which Guide:** `implementation_execution_guide.md` AND `SUB_FEATURES_PHASE_TRACKER.md` template

**Section to Update:** Final step of implementation_execution_guide.md

**Recommended Changes:**

1. **Add explicit warning at end of implementation_execution_guide.md:**

```markdown
## CRITICAL: After Implementation Complete

**🚨 DO NOT DECLARE SUB-FEATURE COMPLETE YET 🚨**

You have completed Phase 2b (Implementation), but the sub-feature is NOT complete until Phase 2c (Post-Implementation QC) is finished.

**Before proceeding to next sub-feature or creating any "COMPLETE" files:**

1. **STOP:** Do not declare feature complete
2. **READ:** `post_implementation_guide.md` in full
3. **USE:** "Starting Post-Implementation QC" prompt from `prompts_reference.md`
4. **EXECUTE:** All 8 steps of post-implementation protocol:
   - Smoke Testing (3 parts - MANDATORY)
   - QC Round 1: Code Quality
   - QC Round 2: Functional Correctness
   - QC Round 3: Production Readiness
   - Lessons learned
   - Completion checklist
5. **ONLY THEN:** Mark sub-feature complete in SUB_FEATURES_PHASE_TRACKER.md

**Common mistake:** Assuming "all tests passing" = complete
**Reality:** Tests passing = implementation phase complete, QC phase still required
**Consequence of skipping:** Unverified code, missed issues, incomplete quality validation

**Next step:** Execute post_implementation_guide.md (do NOT skip to next sub-feature)
```

2. **Add QC reminder in SUB_FEATURES_PHASE_TRACKER.md template:**

```markdown
**Post-Implementation QC (post_implementation_guide.md):**
🚨 MANDATORY - DO NOT SKIP - Tests passing ≠ sub-feature complete
- [ ] Smoke Testing (MANDATORY - 3 parts)
  - [ ] Part 1: Core functionality smoke test
  - [ ] Part 2: Integration smoke test
  - [ ] Part 3: Edge case smoke test
- [ ] QC Round 1: Code Quality
  - [ ] Code review checklist
  - [ ] Style consistency
  - [ ] Documentation completeness
  - [ ] Round 1 issues resolved
- [ ] QC Round 2: Functional Correctness
  - [ ] Spec alignment verification
  - [ ] All success criteria met
  - [ ] Integration tests passing
  - [ ] Round 2 issues resolved
- [ ] QC Round 3: Production Readiness
  - [ ] Error handling verified
  - [ ] Performance acceptable
  - [ ] Security reviewed
  - [ ] Round 3 issues resolved
- [ ] Final Steps
  - [ ] ALL unit tests passing (100%)
  - [ ] Lessons learned documented
  - [ ] **Re-read guide before marking complete**

**WARNING:** Do NOT skip post-implementation QC. Tests passing only means implementation phase complete, NOT sub-feature complete.
```

3. **Add to TODO creation guide (before starting Sub-feature 2):**

```markdown
## Step 0: Verify Previous Sub-Feature QC Complete

**BEFORE starting TODO creation for Sub-feature N:**

1. **Check:** Has Sub-feature N-1 completed ALL post-implementation QC steps?
2. **Verify in SUB_FEATURES_PHASE_TRACKER.md:**
   - [ ] Post-Implementation QC section ALL marked `[x]`
   - [ ] Smoke Testing complete (3 parts)
   - [ ] QC Rounds 1-3 complete
   - [ ] Lessons learned documented
   - [ ] Completion checklist verified
3. **If NOT all complete:**
   - STOP - do not proceed to Sub-feature N
   - Return to Sub-feature N-1 post-implementation QC
   - Complete ALL remaining QC steps
4. **ONLY if all QC complete:**
   - Proceed to Sub-feature N TODO creation

**Why this matters:** Sub-feature dependencies mean unverified code in Sub-feature N-1 can cause cascading failures in Sub-feature N.
```

**Systemic Fix:**

**Primary Fix:** Add explicit QC reminder at END of implementation_execution_guide.md that prevents declaring complete without QC

**Secondary Fix:** Add Step 0 to todo_creation_guide.md that verifies previous sub-feature QC complete before starting new TODO

**Tertiary Fix:** Update SUB_FEATURES_PHASE_TRACKER.md template with QC warning

**Enforcement:** Phase transition protocol in prompts_reference.md already requires this, but agents must remember to use it

**Why This Matters:**

**Quality Assurance:**
- Post-implementation QC catches issues tests can't detect (code conventions, semantic correctness, spec alignment)
- Smoke testing validates real-world usage (not just unit test scenarios)
- 3 QC rounds provide systematic review (quick surface check → deep verification → final skeptical review)
- Requirement verification ensures all 29 spec requirements actually implemented
- Prevents "it works on my machine" syndrome

**Risk Prevention:**
- Unverified code can have hidden bugs (edge cases, error paths, integration issues)
- Missing QC means no baseline comparison (could introduce regressions unknowingly)
- Skipping smoke tests misses entry point failures (code works in tests but fails in real usage)
- No lessons learned documentation means mistakes repeat in future sub-features

**Workflow Integrity:**
- Implementation phase ≠ sub-feature complete
- Full cycle is: Planning → TODO → Implementation → **QC** → Complete
- Skipping QC breaks the cycle and undermines quality gates
- Each sub-feature must be fully validated before starting next (dependencies!)

**User Trust:**
- User expects QC to be automatic/mandatory (shouldn't have to ask "did you do QC?")
- Declaring complete without QC erodes confidence
- Retroactive QC creates rework (declaring complete, then retracting)

**Integration Safety:**
- Sub-feature 2 depends on Sub-feature 1 data structures
- If Sub-feature 1 has unverified bugs, Sub-feature 2 inherits them
- QC validates integration contracts match spec (from_json output → load_players_from_json input)
- Cross-sub-feature integration testing requires previous sub-features to be verified

**This lesson is CRITICAL PRIORITY** - Post-implementation QC is NOT optional. Tests passing = implementation phase complete, but QC phase is separate and mandatory. Agent must transition to Phase 2c immediately after Phase 2b, not skip to next sub-feature.

---

## Summary of Recommended Updates

After development and QA are complete, use this summary to update the guides:

| Guide | Section | Change Type | Description |
|-------|---------|-------------|-------------|
| feature_planning_guide.md | Phase 3: Report and Pause | Add | Add "Interactive Question Resolution Protocol" - require one-by-one question discussion with checklist/specs updates and new question evaluation after each answer |
| **MAJOR RESTRUCTURE** | **Split into TWO guides** | **Create New** | **Split feature_planning_guide.md into feature_creation_guide.md (initial + breakdown) and feature_deep_dive_guide.md (per sub-feature deep planning)** |
| feature_creation_guide.md | NEW GUIDE | Create | Initial setup, broad research, sub-feature breakdown decision (Phase 3 checkpoint), structure creation, transition to deep dive |
| feature_deep_dive_guide.md | NEW GUIDE | Create | Per-sub-feature targeted research, spec/checklist updates, interactive question resolution, completion tracking, cross-sub-feature alignment review (Phase 6 MANDATORY) |
| ALL guides | Research documents | Add | ALL research documents must go in research/ subfolder from the start |
| feature_creation_guide.md | Phase 3: Sub-Feature Breakdown | Add | CRITICAL CHECKPOINT - Triggers: 3+ components, 30+ items, multiple subsystems, different risk levels. Create SUB_FEATURES_README.md + individual specs/checklists per sub-feature |
| feature_deep_dive_guide.md | Phase 6: Cross-Sub-Feature Review | Add | MANDATORY before TODO creation - review all sub-feature specs together, check for conflicts, verify dependencies, ensure interface alignment |
| feature_deep_dive_guide.md | Step 1.3: CODEBASE VERIFICATION Rounds | **CRITICAL UPDATE** | **Add explicit item counting, type distinction (policy/implementation/testing), progress tracking template, verification examples. MANDATORY verification checkpoint before Phase 2. Prevents skipping verification rounds.** |
| feature_creation_guide.md | Sub-Feature Structure Creation | **CRITICAL - Add** | **Create SUB_FEATURES_PHASE_TRACKER.md when creating sub-features - COMPLETE source of truth tracking 100+ checkpoints per sub-feature: 4 planning phases (with sub-steps), 24 TODO iterations (3 rounds), implementation phase (4 sections), post-implementation QC (smoke testing + 3 rounds), completion. Includes quality gates, agent instructions, and MANDATORY re-read guide requirement before marking any phase complete. Tracks entire lifecycle from planning through commit.** |
| implementation_execution_guide.md | Final Step - After Implementation Complete | **CRITICAL - Add** | **Add explicit warning: DO NOT DECLARE COMPLETE - Phase 2c (Post-Implementation QC) is mandatory separate phase. Must execute all 8 steps before proceeding to next sub-feature. Common mistake: assuming tests passing = complete. Reality: tests = implementation phase done, QC phase still required.** |
| SUB_FEATURES_PHASE_TRACKER.md template | Post-Implementation QC Section | Add | Add warning emoji and reminder: "🚨 MANDATORY - DO NOT SKIP - Tests passing ≠ sub-feature complete" to QC section |
| todo_creation_guide.md | Beginning - Before TODO Creation | Add | Add Step 0: Verify Previous Sub-Feature QC Complete - must verify in PHASE_TRACKER that all QC steps complete before starting TODO for next sub-feature |

---

## Guide Update Status

- [x] All lessons documented (5 lessons total)
- [x] Recommendations reviewed with user
- [x] **Lesson 1:** Already implemented in feature_deep_dive_guide.md Phase 3
- [x] **Lesson 2:** Already implemented (guides split into feature_creation_guide.md and feature_deep_dive_guide.md)
- [x] **Lesson 3:** Applied to feature_deep_dive_guide.md Step 1.3 (2025-12-28)
  - Added explicit item counting and type distinction
  - Added progress tracking template
  - Added verification format examples
  - Added MANDATORY checkpoint before Phase 2
- [x] **Lesson 4:** Applied to feature_creation_guide.md and templates.md (2025-12-28)
  - Added SUB_FEATURES_PHASE_TRACKER.md requirement in feature_creation_guide.md
  - Added complete template in templates.md
  - Tracks 800+ checkpoints across planning, TODO creation, implementation, and QC
  - Includes mandatory re-read guide requirement and agent instructions
- [x] **Lesson 5:** Nearly Skipped Post-Implementation QC for Sub-Feature 1 (2025-12-28)
  - **What happened:** Declared sub-feature 1 "COMPLETE" without running post-implementation QC
  - **User caught it:** Asked "wait - did the post-implementation steps get run for sub-1?"
  - **Impact:** Had to retroactively execute all 8 QC steps (requirement verification, smoke testing, 3 QC rounds)
  - **Root cause:** No automatic trigger to execute Phase 2c after Phase 2b completes
  - **Recommended updates:**
    - Add warning at end of implementation_execution_guide.md: "DO NOT DECLARE COMPLETE"
    - Add QC reminder in SUB_FEATURES_PHASE_TRACKER.md template
    - Add Step 0 to todo_creation_guide.md: verify previous sub-feature QC complete
  - **Critical lesson:** Tests passing = implementation phase complete, QC phase still required
- [ ] Updates verified by user (awaiting user review)

---

### Sub-Feature 4: Lessons from Implementation

**Date:** 2025-12-28
**Sub-Feature:** File Update Strategy

**Process Successes (not lessons learned, but validation of correct process):**

1. **Interface Verification Protocol Worked as Designed**
   - **What happened:** During Interface Verification Protocol, discovered that FantasyPlayer has NO `drafted_by` attribute (only `drafted: int`)
   - **Why this is success:** Protocol caught interface mismatch BEFORE coding began
   - **Impact:** Prevented runtime AttributeError, corrected approach to use conditional logic
   - **Validation:** Interface Verification Protocol is working correctly - continue using it

2. **Testing Caught Implementation Bugs**
   - **Bug 1:** JSON structure wrapper mismatch (read/write format inconsistency)
     - Tests revealed: Implementation assumed bare array `[...]` but files use `{"qb_data": [...]}`
     - Fixed immediately: Unwrap when reading, wrap when writing
   - **Bug 2:** Windows atomic replace failure
     - Tests revealed: `Path.rename()` fails on Windows when target file exists (FileExistsError)
     - Fixed immediately: Changed to `Path.replace()` for cross-platform atomicity
   - **Why this is success:** Comprehensive tests caught bugs before user discovered them
   - **Validation:** Test-driven approach working correctly - 2/2 bugs caught and fixed in test phase

3. **Minimal QC Issues**
   - QC Round 1: 0 critical issues
   - QC Round 2: 0 issues
   - QC Round 3: 0 issues
   - **Why this is success:** Continuous spec verification during implementation prevented issues
   - **Validation:** Continuous verification process working - implementation matched spec exactly

**No New Lessons Learned:**
- All issues encountered were caught by existing processes (Interface Verification, Testing, QC)
- No process failures identified
- Workflow guides followed correctly
- Quality gates effective

**Recommended Action:** No guide updates needed from Sub-Feature 4 implementation
