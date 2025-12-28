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

---

## Guide Update Status

- [ ] All lessons documented
- [ ] Recommendations reviewed with user
- [ ] feature_planning_guide.md updated
- [ ] feature_development_guide.md updated
- [ ] Updates verified by user
