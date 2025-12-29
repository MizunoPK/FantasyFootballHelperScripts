# Feature Templates

This file contains all file templates used during feature planning and development. Reference these when creating new feature files.

---

## Quick Template Index

| Template | When to Use | Section |
|----------|-------------|---------|
| README.md | Phase 1: Create structure | [Link](#feature-readme-template) |
| {feature_name}_specs.md | Phase 1: Create structure (single feature) | [Link](#specification-template) |
| Dependency Map | Phase 2.6: Add to specs | [Link](#dependency-map-template) |
| {feature_name}_checklist.md | Phase 1: Create structure (single feature) | [Link](#checklist-template) |
| {feature_name}_lessons_learned.md | Phase 1: Create structure | [Link](#lessons-learned-template) |
| {feature_name}_questions.md | Step 3: Create questions | [Link](#questions-file-template) |
| {feature_name}_todo.md | Step 1: Create TODO | [Link](#todo-file-template) |
| {feature_name}_implementation_checklist.md | Step 6a: Before implementation | [Link](#implementation-checklist-template) |
| {feature_name}_code_changes.md | After TODO creation | [Link](#code-changes-template) |
| **SUB-FEATURE TEMPLATES** | | |
| SUB_FEATURES_README.md | Phase 4: Create sub-feature structure | [Link](#sub-features-readme-template) |
| **SUB_FEATURES_PHASE_TRACKER.md** | **Phase 4: MANDATORY for sub-features** | **[Link](#sub-features-phase-tracker-template)** |
| sub_feature_{N}_{name}_spec.md | Phase 4: Per sub-feature | [Link](#sub-feature-spec-template) |
| sub_feature_{N}_{name}_checklist.md | Phase 4: Per sub-feature | [Link](#sub-feature-checklist-template) |
| research/README.md | Phase 4: Create research folder | [Link](#research-folder-readme-template) |

---

## Planning Phase Templates

### Feature README Template

Create in: `feature-updates/{feature_name}/README.md`

```markdown
# {Feature Name} - Work in Progress

---

## AGENT STATUS (Read This First)

**Current Phase:** [PLANNING | DEVELOPMENT | POST-IMPLEMENTATION | COMPLETE]
**Current Step:** [specific step name from checklist below]
**Next Action:** [what to do next]

### WHERE AM I RIGHT NOW? (Quick State Check)

Update this section after EVERY step to ensure session continuity:

```
Current Phase:  [ ] PLANNING  [ ] DEVELOPMENT  [ ] POST-IMPL  [ ] COMPLETE
Current Step:   _____________________________________________
Blocked:        [ ] NO  [ ] YES → Reason: ___________________
Next Action:    _____________________________________________
Last Activity:  {YYYY-MM-DD HH:MM} - {what was done}
```

**Session Resume Instructions:**
1. Read this section first
2. Check the workflow checklist below for detailed progress
3. Continue from "Next Action" - do NOT restart the workflow

---

## 📖 Active Development Guide

**Current Phase:** [PLANNING | TODO_CREATION | IMPLEMENTATION | POST_IMPLEMENTATION]
**Active Guide:** `feature-updates/guides/[guide_file].md`
**Critical Section:** [specific section agent should reference]

⚠️ **AGENTS: Re-read the active guide section before major decisions!**

**Guide by Phase:**
- **PLANNING:** `feature_planning_guide.md`
- **TODO_CREATION:** `todo_creation_guide.md`
- **IMPLEMENTATION:** `implementation_execution_guide.md`
- **POST_IMPLEMENTATION:** `post_implementation_guide.md`

**Update this section when transitioning between phases.**

---

### Full Workflow Checklist

> **Instructions:** Update this checklist as you complete each step. This is your persistent state across sessions.

**PLANNING PHASE** (feature_planning_guide.md)
- [ ] Phase 1: Initial Setup
  - [ ] Create folder structure
  - [ ] Move notes file
  - [ ] Create README.md (this file)
  - [ ] Create {feature_name}_specs.md
  - [ ] Create {feature_name}_checklist.md
  - [ ] Create {feature_name}_lessons_learned.md
- [ ] Phase 2: Deep Investigation
  - [ ] 2.1: Analyze notes thoroughly
  - [ ] 2.2: Research codebase patterns
  - [ ] 2.3: Populate checklist with questions
  - [ ] 2.3.1: THREE-ITERATION question generation (MANDATORY)
  - [ ] 2.4: CODEBASE VERIFICATION rounds (MANDATORY)
  - [ ] 2.5: Performance analysis for options
  - [ ] 2.6: Create DEPENDENCY MAP
  - [ ] 2.7: Update specs with context + dependency map
  - [ ] 2.8: ASSUMPTIONS AUDIT (list all assumptions)
- [ ] Phase 3: Report and Pause
  - [ ] Present findings to user
  - [ ] Wait for user direction
- [ ] Phase 4: Resolve Questions
  - [ ] All checklist items resolved [x]
  - [ ] Specs updated with all decisions
- [ ] Planning Complete - Ready for Implementation

**DEVELOPMENT PHASE** (feature_development_guide.md)
- [ ] Step 1: Create TODO file
- [ ] Step 2: First Verification Round (7 iterations)
  - [ ] Iterations 1-3: Standard verification
  - [ ] Iteration 4: Algorithm Traceability
  - [ ] Iteration 5: End-to-End Data Flow
  - [ ] Iteration 6: Skeptical Re-verification
  - [ ] Iteration 7: Integration Gap Check
- [ ] Step 3: Create questions file (if needed)
  - [ ] Present questions to user
  - [ ] Wait for user answers
- [ ] Step 4: Update TODO with answers
- [ ] Step 5: Second Verification Round (9 iterations)
  - [ ] Iterations 8-10: Verification with answers
  - [ ] Iteration 11: Algorithm Traceability
  - [ ] Iteration 12: End-to-End Data Flow
  - [ ] Iteration 13: Skeptical Re-verification
  - [ ] Iteration 14: Integration Gap Check
  - [ ] Iterations 15-16: Final preparation
- [ ] Step 6: Third Verification Round (8 iterations)
  - [ ] Iterations 17-18: Fresh Eyes Review
  - [ ] Iteration 19: Algorithm Deep Dive
  - [ ] Iteration 20: Edge Case Verification
  - [ ] Iteration 21: Test Coverage Planning + Mock Audit
  - [ ] Iteration 22: Skeptical Re-verification #3
  - [ ] Iteration 23: Integration Gap Check #3
  - [ ] Iteration 24: Implementation Readiness
- [ ] Interface Verification (pre-implementation)
- [ ] Implementation
  - [ ] Create code_changes.md
  - [ ] Execute TODO tasks
  - [ ] Tests passing (100%)

**POST-IMPLEMENTATION PHASE**
- [ ] Requirement Verification Protocol
- [ ] QC Round 1 (initial review)
- [ ] QC Round 2 (semantic diff + deep verification)
- [ ] QC Round 3 (final skeptical review)
- [ ] **SMOKE TESTING PROTOCOL** ← MANDATORY - DO NOT SKIP
  - [ ] Import Test (all modules import successfully)
  - [ ] Entry Point Test (scripts start without errors)
  - [ ] Execution Test (feature works end-to-end with real data)
- [ ] Lessons Learned Review
- [ ] Apply guide updates (if any)
- [ ] Move folder to done/

---

## What This Is

{One paragraph explaining what is being built}

## Why We Need This

1. {Reason 1}
2. {Reason 2}
3. {Reason 3}

## Scope

**IN SCOPE:**
- {What IS included in this work}

**OUT OF SCOPE:**
- {What is NOT included}

### Files in This Folder

| File | Purpose |
|------|---------|
| `README.md` | This file - context and status for agents |
| `{feature_name}_notes.txt` | Original scratchwork notes from user |
| `{feature_name}_specs.md` | Main specification with detailed requirements |
| `{feature_name}_checklist.md` | Tracks open questions and decisions |
| `{feature_name}_lessons_learned.md` | Captures issues to improve the guides |

## Key Context for Future Agents

### {Key Topic 1}
{Important context discovered during investigation}

### {Key Topic 2}
{More context as needed}

## What's Resolved
- {Decision 1}
- {Decision 2}

## What's Still Pending
- {Open question 1}
- {Open question 2}

## How to Continue This Work

1. **Check the AGENT STATUS section above** for current phase and step
2. Read `{feature_name}_specs.md` for complete specifications
3. Read `{feature_name}_checklist.md` to see what's resolved vs pending
4. Continue from the current step in the workflow checklist
5. **Update the AGENT STATUS section** as you complete steps
```

---

### Specification Template

Create in: `feature-updates/{feature_name}/{feature_name}_specs.md`

```markdown
# {Feature Name}

## Objective

{Clear, concise statement of what this feature accomplishes}

---

## High-Level Requirements

### 1. {Requirement Category 1}
- **{Aspect}:** {Detail}
- **{Aspect}:** {Detail}

### 2. {Requirement Category 2}
{Structure depends on the feature}

### 3. Output/Deliverables
```
{folder/file structure or expected outputs}
```

---

## Open Questions (To Be Resolved)

### API/Data Source Questions

1. **{Question}:** PENDING
   - {Context or options being considered}

### Algorithm/Logic Questions

2. **{Question}:** PENDING
   - {Context}

### Architecture Questions

3. **{Question}:** PENDING
   - {Context}

---

## Resolved Implementation Details

### {Component 1}

**Decision:** {What was decided}
**Reasoning:** {Why this approach}
**Source:** {Where data/logic comes from}

**Implementation:**
```
{Pseudocode or algorithm description}
```

### {Component 2}

{Continue for each resolved component}

---

## Implementation Notes

### Files to Modify
- `{path/to/file.py}` - {what changes needed}

### Dependencies
- {Dependency 1}

### Reusable Code
- `{path/to/file.py}` - {what can be reused}

### Testing Strategy
- {How this will be tested}

---

## Status: {PLANNING / READY FOR IMPLEMENTATION}
```

---

### Dependency Map Template

Include in `_specs.md` during Phase 2.6 of planning:

```markdown
## Dependency Map

### Module Dependencies

```
┌─────────────────────────────────────────────────────────────┐
│ {entry_point_script.py} (entry point)                       │
│     │                                                       │
│     ▼                                                       │
│ {MainManager}                                               │
│     │                                                       │
│     ├──► {DependencyClass1} ({location})                    │
│     │         └──► {data_source_1}                          │
│     │                                                       │
│     ├──► {DependencyClass2} (NEW)                           │
│     │         └──► {DependencyClass3}                       │
│     │                   └──► {data_source_2}                │
│     │                                                       │
│     └──► {OutputManager}                                    │
│               └──► {output_file} (output)                   │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

```
Input: {input_source}
   ▼
{Step1Class}.{method}()
   ▼
{Step2Class}.{method}()
   ▼
{Step3Class}.{method}()  ← NEW (if applicable)
   ▼
Output: {output_destination}
```

### Key Integration Points

| Component | Depends On | Used By | Notes |
|-----------|------------|---------|-------|
| {NewClass} | {DependencyClass} | {CallerClass} | {important notes} |
```

**Why this matters:** The dependency map helps identify:
- Which interfaces need to be verified before implementation
- Where integration points exist
- Which existing code might be affected
- Data flow from entry to output

---

### Checklist Template

Create in: `feature-updates/{feature_name}/{feature_name}_checklist.md`

```markdown
# {Feature Name} - Requirements Checklist

> **IMPORTANT**: When marking items as resolved, also update `{feature_name}_specs.md`
> with full implementation details. The checklist tracks status; the specs file is
> the implementation specification.

---

## General Decisions

- [ ] **{Decision 1}:** {Options or context}
- [ ] **{Decision 2}:** {Options or context}

---

## API/Data Source Questions

- [ ] **{Question about data source}:** {Context}
- [ ] **{Question about API}:** {Context}

---

## Output Files / Data Structures

For each output file or major data structure, create a detailed section:

### {Output File or Component Name}

**File-level decisions:**
- [ ] Data source: {Pending or resolved source}
- [ ] Format: {Pending or resolved format}

**Fields:**

| Field | Source Known? | Notes |
|-------|---------------|-------|
| `field_name` | [ ] | {Source or pending question} |
| `another_field` | [x] | {Resolved: from API X.Y.Z} |

**Questions:**
- [ ] {Specific question about this component}

**Implementation Note:** {Reference to similar code or algorithm if known}

---

## Output Consumer Validation (MANDATORY)

**CRITICAL:** Every output file/folder must be validated against its consumers. If output cannot be loaded as input by consumers, it is broken.

### Consumer Identification

| Output | Consumer(s) | Consumer Location | What Consumer Expects |
|--------|-------------|-------------------|----------------------|
| {output_folder/file} | {What loads/uses this} | {file:function} | {Required structure} |

### Roundtrip Test Requirements

For each output that can be used as input elsewhere:

```
□ Output: {describe output}
  □ Consumer 1: {name} ({location})
    □ Required files: {list}
    □ Required structure within files: {describe}
    □ Roundtrip test planned: {describe test}
  □ Consumer 2: ...
```

**If output has no consumers:** Document why and confirm with user that output is meant to be standalone.

**Example (from accuracy simulation):**
```
□ Output: accuracy_optimal_TIMESTAMP/
  □ Consumer 1: find_baseline_config() (run_accuracy_simulation.py)
    □ Required files: league_config.json, draft_config.json, week1-5.json, week6-9.json, week10-13.json, week14-17.json
    □ Required structure: Each file must have {config_name, description, parameters} nested structure
    □ Roundtrip test: test_optimal_folder_usable_as_baseline()
  □ Consumer 2: ConfigGenerator.__init__() (shared/ConfigGenerator.py)
    □ Required files: Same as above
    □ Required structure: parameters dict must be loadable as baseline_config
    □ Roundtrip test: Same test - creates new ConfigGenerator with output folder
```

---

## Algorithm/Logic Questions

- [ ] **{Question about calculation}:** {Context}
- [ ] **{Question about logic}:** {Context}

---

## Architecture Questions

- [ ] **{Question about code structure}:** {Context}
- [ ] **{Question about patterns}:** {Context}

---

## Error Handling Questions

- [ ] **{What happens when X fails}:** {Context}

---

## Edge Cases

- [ ] **{Edge case 1}:** {Context}
- [ ] **{Edge case 2}:** {Context}

---

## Testing & Validation

- [ ] **{Test approach}:** {Context}
- [ ] **{Validation method}:** {Context}

---

## Data Source Summary

| Data | Source | Status |
|------|--------|--------|
| {Data type 1} | {API or calculation} | Pending |
| {Data type 2} | {API or calculation} | Verified |

---

## Resolution Log

| Item | Resolution | Date |
|------|------------|------|
| {Item 1} | {Brief answer} | {Date} |
| {Item 2} | {Brief answer} | {Date} |
```

---

### Lessons Learned Template

Create in: `feature-updates/{feature_name}/{feature_name}_lessons_learned.md`

```markdown
# {Feature Name} - Lessons Learned

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

### Lesson 1: {Brief Title}

**Date:** {Date}

**What Happened (Symptom):**
{Describe the observable issue or problem that was discovered}

**Immediate Cause:**
{Why did this specific issue occur?}

**Root Cause Analysis:**
{Use the "5 Whys" technique to find the systemic issue}

1. Why did [symptom] happen? → {immediate cause}
2. Why did [immediate cause] happen? → {deeper cause}
3. Why did [deeper cause] happen? → {even deeper}
4. Why did [even deeper] happen? → {approaching root}
5. Why did [approaching root] happen? → **ROOT CAUSE: {systemic issue}**

**Impact:**
{How did this affect the feature or require rework?}

**Recommended Guide Update:**

**Which Guide:** {feature_planning_guide.md / feature_development_guide.md / both}

**Section to Update:** {Specific section name}

**Recommended Change:**
{Specific text or checklist item to add, or process change to make}

**Systemic Fix:**
{What process change prevents this CATEGORY of error, not just this specific instance?}

---

### Lesson 2: {Brief Title}

{Repeat structure for each lesson}

---

## Summary of Recommended Updates

After development and QA are complete, use this summary to update the guides:

| Guide | Section | Change Type | Description |
|-------|---------|-------------|-------------|
| {guide name} | {section} | {Add/Modify/Emphasize} | {Brief description} |

---

## Guide Update Status

- [ ] All lessons documented
- [ ] Recommendations reviewed with user
- [ ] feature_planning_guide.md updated
- [ ] feature_development_guide.md updated
- [ ] Updates verified by user
```

---

## Development Phase Templates

### Questions File Template

Create in: `feature-updates/{feature_name}/{feature_name}_questions.md`

```markdown
# {Feature Name} - Questions

## Question 1: {Brief Title}

### Context
{Explain the background and why this question is being asked. Include relevant findings from codebase research, constraints discovered, or ambiguities in the original specification that necessitate clarification.}

### Question
{State the specific question or problem that needs to be resolved. Be clear and direct about what decision needs to be made.}

### Options

**Option A: {Option Title}**
- Description: {What this option entails}
- Pros: {Benefits of this approach}
- Cons: {Drawbacks or risks}

**Option B: {Option Title}**
- Description: {What this option entails}
- Pros: {Benefits of this approach}
- Cons: {Drawbacks or risks}

**Option C: {Option Title}** (if applicable)
- Description: {What this option entails}
- Pros: {Benefits of this approach}
- Cons: {Drawbacks or risks}

### Agent Recommendation
{State the agent's recommended option and provide clear reasoning for why this option is preferred based on codebase research, existing patterns, and technical considerations.}

### User Answer
> **Selected Option:**
>
> **Additional Notes/Elaboration:**
>
>

---

## Question 2: {Brief Title}

{Repeat the same structure for each additional question}
```

### Questions Template Requirements

1. **Context Section**: Must explain WHY this question arose - reference specific findings from codebase research, conflicts in requirements, or gaps in the specification
2. **Question Section**: Must be a clear, answerable question - not vague or open-ended
3. **Options Section**: Must provide at least 2 concrete options with pros/cons for each
4. **Agent Recommendation**: Must state a clear preference with technical justification
5. **User Answer Section**: Must include dedicated, clearly marked space for the selected option and elaboration

---

### TODO File Template

Create in: `feature-updates/{feature_name}/{feature_name}_todo.md`

```markdown
# {Feature Name} - Implementation TODO

---

## 📖 Guide Reminder

**This file is governed by:** `feature-updates/guides/todo_creation_guide.md`

**Ready for implementation when:** ALL 24 iterations complete (see guide lines 87-93)

**DO NOT proceed to implementation until:**
- [ ] All 24 iterations executed individually
- [ ] Iteration 4a passed (TODO Specification Audit)
- [ ] Iteration 23a passed (Pre-Implementation Spec Audit - 4 parts)
- [ ] Iteration 24 passed (Implementation Readiness Checklist)
- [ ] Interface verification complete (copy-pasted signatures verified)
- [ ] No "Alternative:" or "May need to..." notes remain in TODO

⚠️ **If you think verification is complete, re-read guide lines 87-93 FIRST!**

⚠️ **Do NOT offer user choice to "proceed to implementation OR continue verification" - you MUST complete all 24 iterations**

---

## Iteration Progress Tracker

### Compact View (Quick Status)

```
R1: □□□□□□□ (0/7)   R2: □□□□□□□□□ (0/9)   R3: □□□□□□□□ (0/8)
```
Legend: ■ = complete, □ = pending, ▣ = in progress

**Current:** Iteration ___ ({type} - Round {N})
**Confidence:** HIGH / MEDIUM / LOW
**Blockers:** None / {description}

### Detailed View

| Round | Iterations | Status |
|-------|------------|--------|
| First (7) | [ ]1 [ ]2 [ ]3 [ ]4 [ ]5 [ ]6 [ ]7 | 0/7 |
| Second (9) | [ ]8 [ ]9 [ ]10 [ ]11 [ ]12 [ ]13 [ ]14 [ ]15 [ ]16 | 0/9 |
| Third (8) | [ ]17 [ ]18 [ ]19 [ ]20 [ ]21 [ ]22 [ ]23 [ ]24 | 0/8 |

**Current Iteration:** ___

---

## Protocol Execution Tracker

Track which protocols have been executed (protocols must be run at specified iterations):

| Protocol | Required Iterations | Completed |
|----------|---------------------|-----------|
| Standard Verification | 1, 2, 3, 8, 9, 10, 15, 16 | [ ]1 [ ]2 [ ]3 [ ]8 [ ]9 [ ]10 [ ]15 [ ]16 |
| Algorithm Traceability | 4, 11, 19 | [ ]4 [ ]11 [ ]19 |
| End-to-End Data Flow | 5, 12 | [ ]5 [ ]12 |
| Skeptical Re-verification | 6, 13, 22 | [ ]6 [ ]13 [ ]22 |
| Integration Gap Check | 7, 14, 23 | [ ]7 [ ]14 [ ]23 |
| Fresh Eyes Review | 17, 18 | [ ]17 [ ]18 |
| Edge Case Verification | 20 | [ ]20 |
| Test Coverage Planning + Mock Audit | 21 | [ ]21 |
| Implementation Readiness | 24 | [ ]24 |
| Interface Verification | Pre-impl | [ ] |

---

## Verification Summary

- Iterations completed: 0/24
- Requirements from spec: {count}
- Requirements in TODO: {count}
- Questions for user: {count}
- Integration points identified: {count}

---

## Phase 1: {Phase Name}

### Task 1.1: {Task Description}
- **File:** `{path/to/file.py}`
- **Similar to:** `{reference_file.py}:{line_numbers}` (if applicable)
- **Tests:** `tests/{path}/test_{file}.py`
- **Status:** [ ] Not started

**Implementation details:**
{Specific implementation notes}

### Task 1.2: {Task Description}
{Continue for each task}

### QA CHECKPOINT 1: {Brief Description}
- **Status:** [ ] Not started
- **Expected outcome:** {What should happen}
- **Test command:** `{python command to run}`
- **Verify:**
  - [ ] Unit tests pass
  - [ ] E2E test produces meaningful output (non-zero values)
  - [ ] No errors in output
- **If checkpoint fails:** STOP, fix issue, document in lessons learned, then re-run

---

## Phase 2: {Phase Name}

{Continue for each phase}

### QA CHECKPOINT 2: {Brief Description}
- **Status:** [ ] Not started
- **Expected outcome:** {What should happen}
- **Test command:** `{python command to run}`
- **Verify:**
  - [ ] Unit tests pass
  - [ ] E2E test completes
  - [ ] Output files written correctly
- **If checkpoint fails:** STOP, fix issue, document in lessons learned, then re-run

---

## Interface Contracts (Verified Pre-Implementation)

### {DependencyClass}
- **Method:** `{method_name}(param1: Type, param2: Type) -> ReturnType`
- **Source:** `{path/to/file.py}:{line}`
- **Existing usage:** `{where_its_used.py}:{line}`
- **Verified:** [ ]

### {DataModel}
- **Attribute:** `{attribute_name}` - {description}
- **Type:** {type}
- **Source:** `{path/to/model.py}:{line}`
- **Note:** {any important semantics, e.g., "projected, not actual"}
- **Verified:** [ ]

### Quick E2E Validation Plan
- **Minimal test command:** `{python command to validate interfaces}`
- **Expected result:** {what should happen}
- **Run before:** Full implementation begins
- **Status:** [ ] Not run | [ ] Passed | [ ] Failed (fix before proceeding)

---

## Integration Matrix

| New Component | File | Called By | Caller File:Line | Caller Modification Task |
|---------------|------|-----------|------------------|--------------------------|
| {method_name}() | {file.py} | {caller_method}() | {caller_file.py}:{line} | Task {X.Y} |

---

## Algorithm Traceability Matrix

| Spec Section | Algorithm Description | Code Location | Conditional Logic |
|--------------|----------------------|---------------|-------------------|
| Lines {X-Y} | {description} | {file.py}:{method} | {if/else logic} |

---

## Data Flow Traces

### Requirement: {Requirement Name}
```
Entry: {run_script.py}
  → {ManagerClass.method()}
  → {HelperClass.method()}  ← NEW
  → Output: {expected output}
```

---

## Verification Gaps

Document any gaps found during iterations here:

### Iteration {X} Gaps
- [GAP-1] {Description} - Severity: {Critical/Non-critical} - Status: {Fixed/Pending}

---

## Skeptical Re-verification Results

### Round 1 (Iteration 6)
- **Verified correct:** {list}
- **Corrections made:** {list}
- **Confidence level:** {High/Medium/Low}
  - High = All paths verified, no assumptions
  - Medium = Most verified, minor assumptions
  - Low = Multiple unverified items (DO NOT proceed)

### Round 2 (Iteration 13)
{Repeat structure}

### Round 3 (Iteration 22)
{Repeat structure}

---

## Progress Notes

Keep this section updated for session continuity:

**Last Updated:** {date/time}
**Current Status:** {description}
**Next Steps:** {what to do next}
**Blockers:** {any blockers or issues}
```

---

### Implementation Checklist Template

Create in: `feature-updates/{feature_name}/{feature_name}_implementation_checklist.md`

**Purpose:** Track continuous verification of each requirement against specs during implementation (Step 6a).

**When to create:** Before beginning implementation (after Iteration 24 passes).

**How to use:** Check off EACH requirement as you implement it. Do NOT batch-check. Keep this file open alongside specs.md during implementation.

```markdown
# {Feature Name} - Implementation Checklist

**Instructions**: Check off EACH requirement as you implement it. Do NOT batch-check.

**Created:** {date}
**Last Updated:** {date/time}

---

## From Traceability Matrix:

### Phase 1: {Phase Name}

- [ ] REQ-001: {Description from specs.md lines X-Y}
      **Implementation details:**
      - {Specific requirement details from specs}
      - Expected output: {example from specs}
      - NOT: {common mistake to avoid}

      **Implemented in:** {file:line} (fill in after implementing)
      **Verified against specs:** [ ] YES
      **Verified date/time:** {date/time}
      **Notes:** {any deviations or issues}

- [ ] REQ-002: {Description from specs.md lines X-Y}
      **Implementation details:**
      - {Specific requirement details from specs}
      - Expected output: {example from specs}
      - NOT: {common mistake to avoid}

      **Implemented in:** {file:line}
      **Verified against specs:** [ ] YES
      **Verified date/time:** {date/time}
      **Notes:** {any deviations or issues}

{Continue for all requirements in Phase 1}

### Phase 2: {Phase Name}

- [ ] REQ-003: {Description}
      {Continue same structure}

{Continue for all phases}

---

## Verification Log:

This table provides at-a-glance verification status:

| Requirement | Spec Location | Implementation | Verified? | Matches Spec? | Notes |
|-------------|---------------|----------------|-----------|---------------|-------|
| REQ-001 | specs.md:45-50 | file.py:120-135 | ✅ | ✅ | Exact match |
| REQ-002 | specs.md:52-58 | file.py:140-160 | ✅ | ✅ | Exact match |
| REQ-003 | specs.md:60-65 | file.py:165-180 | ✅ | ⚠️ | Minor deviation: {explain} |
| REQ-004 | specs.md:70-75 | {pending} | ⏳ | ⏳ | In progress |
| REQ-005 | specs.md:80-85 | {not started} | ❌ | ❌ | Not started |

---

## Mini-QC Checkpoints:

### After Phase 1 Complete

**Date/Time:** {when completed}

- [ ] Read specs.md section for Phase 1
- [ ] All Phase 1 requirements implemented?
- [ ] All Phase 1 TODO acceptance criteria satisfied?
- [ ] Any deviations documented and justified?
- [ ] Tests passing for Phase 1?
- [ ] Output matches spec examples?

**Status:** ✅ PASS / ❌ FAIL (if fail, fix before continuing)
**Issues Found:** {list or "None"}
**Deviations:** {list or "None"}

### After Phase 2 Complete

{Repeat structure for each phase}

---

## Self-Audit Checkpoints:

Track when you last consulted specs during implementation:

| Time | Last Spec Consultation | Implementing | Notes |
|------|----------------------|--------------|-------|
| {time} | specs.md lines X-Y | REQ-001 | Starting implementation |
| {time} | specs.md lines X-Y | REQ-001 | Verifying output structure |
| {time} | specs.md lines A-B | REQ-002 | Checking field types |

**Purpose:** Ensure you're consulting specs every 5-10 minutes during implementation.

**Red flag:** If gaps between consultations >15 minutes, you may be working from memory.

---

## Deviation Log:

Document ANY deviations from specs:

| Requirement | Spec Says | Implementation Does | Reason | User Approved? |
|-------------|-----------|---------------------|--------|----------------|
| {REQ-ID} | {what spec requires} | {what was implemented instead} | {justification} | YES/NO/PENDING |

**Rule:** If deviation is significant, get user approval before proceeding.

---

## Progress Summary:

- **Total Requirements:** {count}
- **Implemented:** {count}
- **Verified:** {count}
- **Deviations:** {count}
- **Completion:** {percentage}%

**Last Updated:** {date/time}
**Ready for QC Round 1:** YES / NO
```

**Template Notes:**

1. **Create this file BEFORE starting implementation** (Step 6a requirement)
2. **Keep it open** alongside specs.md during implementation
3. **Update in real-time** - check off requirements as you complete them
4. **Self-audit frequently** - use the Self-Audit Checkpoints section to track spec consultations
5. **Document deviations immediately** - don't wait until QC to discover mismatches
6. **Mini-QC after each phase** - ensures continuous alignment with specs

**Historical Context:** This template was added after a feature implementation passed all 24 verification iterations but failed QC Round 1 with 40% failure rate due to not consulting specs during implementation. Using this checklist enforces continuous verification.

---

### Code Changes Template

Create in: `feature-updates/{feature_name}/{feature_name}_code_changes.md`

```markdown
# {Feature Name} - Code Changes Documentation

## Overview

{Brief summary of what was implemented}

---

## Files Modified

### {file_path_1.py}

**Lines Changed:** {start}-{end}

**Before:**
```python
{original code}
```

**After:**
```python
{new code}
```

**Rationale:** {Why this change was made}

**Impact:** {What this change affects}

---

### {file_path_2.py}

{Repeat structure for each file}

---

## New Files Created

### {new_file_path.py}

**Purpose:** {What this file does}

**Key Components:**
- `{ClassName}` - {description}
- `{function_name}()` - {description}

---

## Configuration Changes

{Any changes to config files, constants, etc.}

---

## Test Modifications

### New Tests
- `tests/{path}/test_{file}.py` - {description}

### Modified Tests
- `tests/{path}/test_{file}.py` - {what changed and why}

---

## Requirements Verification

| Requirement | Implementation | File:Line | Status |
|-------------|---------------|-----------|--------|
| {req 1} | {how implemented} | {location} | DONE |
| {req 2} | {how implemented} | {location} | DONE |

---

## Quality Control Rounds

### Round 1
- **Reviewed:** {date/time}
- **Issues Found:** {list or "None"}
- **Issues Fixed:** {list or "N/A"}
- **Status:** PASSED / ISSUES FOUND (fixed)

### Round 2
{Repeat structure}

### Round 3
{Repeat structure}

---

## Integration Evidence

| Requirement | New Method | Called By | Entry Point | Verified |
|-------------|------------|-----------|-------------|----------|
| {req} | {method}() | {caller}() | {script.py} | YES/NO |
```

---

## Round Checkpoint Summary Template

Use this template when completing a verification round (after iterations 7, 16, or 24) to summarize findings for the user:

```markdown
## Round {N} Checkpoint Summary

**Iterations Completed:** {X-Y} ({count} iterations)
**Date:** {YYYY-MM-DD}

### Key Findings
- {Finding 1: what was discovered or verified}
- {Finding 2: any surprises or issues found}
- {Finding 3: important decisions made}

### Gaps Identified
| Gap | Severity | Resolution |
|-----|----------|------------|
| {missing info} | High/Medium/Low | {how it was resolved OR "Needs user input"} |

### TODO Updates This Round
- **Added:** {N} new tasks
- **Modified:** {N} tasks updated with details
- **Removed:** {N} tasks found unnecessary

### Scope Changes
- **In scope (confirmed):** {list}
- **Added to scope:** {list or "None"}
- **Removed from scope:** {list or "None"}

### Confidence Assessment
**Confidence Level:** {High/Medium/Low}

| Area | Confidence | Notes |
|------|------------|-------|
| Requirements understood | H/M/L | {brief note} |
| Interfaces verified | H/M/L | {brief note} |
| Integration path clear | H/M/L | {brief note} |
| Edge cases identified | H/M/L | {brief note} |

### Next Steps
- {What happens next: Round 2 / Questions file / Implementation}
- {Any blockers or dependencies}
```

**When to use:** Present this summary to the user at each round checkpoint to keep them informed and get approval before proceeding.

---

## Folder Structure Reference

### During Planning
```
feature-updates/{feature_name}/
├── README.md                           # Context for future agents
├── {feature_name}_notes.txt            # Original scratchwork (moved)
├── {feature_name}_specs.md             # Main specification
├── {feature_name}_checklist.md         # Requirements checklist
└── {feature_name}_lessons_learned.md   # Issues to improve guides
```

### During Development
```
feature-updates/{feature_name}/
├── README.md
├── {feature_name}_notes.txt
├── {feature_name}_specs.md
├── {feature_name}_checklist.md
├── {feature_name}_lessons_learned.md
├── {feature_name}_questions.md         # Questions and answers
├── {feature_name}_todo.md              # Implementation tracking
└── {feature_name}_code_changes.md      # Documentation of changes
```

### After Completion
```
feature-updates/done/{feature_name}/
├── (all files preserved for reference)
```

---

## Sub-Feature Templates

### SUB_FEATURES_README Template

Create in: `feature-updates/{feature_name}/SUB_FEATURES_README.md`

```markdown
# Sub-Feature Breakdown: {Feature Name}

## Overview

{Brief description of overall feature and why it was broken into sub-features}

## Sub-Features

| Sub-Feature | Items | Dependencies | Risk | Priority |
|-------------|-------|--------------|------|----------|
| 1. {Name} | ~X | None | LOW/MED/HIGH | LOW/MED/HIGH |
| 2. {Name} | ~Y | Sub-feature 1 | LOW/MED/HIGH | LOW/MED/HIGH |
| 3. {Name} | ~Z | Sub-feature 1, 2 | LOW/MED/HIGH | LOW/MED/HIGH |

## Implementation Order

**Recommended sequence based on dependencies:**
1. Sub-feature 1: {Name} (foundation - no dependencies)
2. Sub-feature 2: {Name} (depends on 1)
3. Sub-feature 3: {Name} (depends on 1, 2)
...

**Rationale for order:**
- {Explain why this sequence makes sense}

## Progress Tracking

**Planning (Deep Dive):**
- [ ] Sub-feature 1: {Name} - Deep Dive Complete
- [ ] Sub-feature 2: {Name} - Deep Dive Complete
- [ ] Sub-feature 3: {Name} - Deep Dive Complete
- [ ] **Cross-Sub-Feature Alignment Review** (MANDATORY before implementation)

**Implementation (Sequential - One at a Time):**
- [ ] Sub-feature 1: {Name} - TODO Creation (24 iterations)
- [ ] Sub-feature 1: {Name} - Implementation Complete
- [ ] Sub-feature 1: {Name} - QC Rounds Complete (1-3)
- [ ] Sub-feature 1: {Name} - Committed ✅
- [ ] Sub-feature 2: {Name} - TODO Creation (24 iterations)
- [ ] Sub-feature 2: {Name} - Implementation Complete
- [ ] Sub-feature 2: {Name} - QC Rounds Complete (1-3)
- [ ] Sub-feature 2: {Name} - Committed ✅
...

**Final Integration:**
- [ ] All sub-features implemented
- [ ] Final integration test across all sub-features
- [ ] Final smoke testing protocol
- [ ] Move to done/ folder

## Dependencies

### Dependency Graph

```
Sub-feature 1
  ├─► Sub-feature 2 (depends on 1)
  └─► Sub-feature 3 (depends on 1)

Sub-feature 2
  └─► Sub-feature 4 (depends on 2)

Sub-feature 3 + Sub-feature 4
  └─► Sub-feature 5 (depends on 3, 4)
```

### Detailed Dependencies

**Sub-feature 1: {Name}**
- Prerequisites: None
- Provides: {What it provides to other sub-features}
- Blocks: {Which sub-features depend on this}

**Sub-feature 2: {Name}**
- Prerequisites: Sub-feature 1 ({what it needs from sub-feature 1})
- Provides: {What it provides}
- Blocks: {Which sub-features depend on this}

...

## Cross-Sub-Feature Integration Points

**Critical interfaces between sub-features:**

| Interface | Provider | Consumer | Contract |
|-----------|----------|----------|----------|
| {Interface name} | Sub-feature 1 | Sub-feature 2 | {Description of contract} |
| {Interface name} | Sub-feature 2 | Sub-feature 3 | {Description of contract} |

## Notes

**Why sub-features:**
- {Reason for breakdown}

**Key decisions:**
- {Important decisions about structure}

**Lessons learned during planning:**
- {Anything discovered during planning that's important}
```

---

### SUB_FEATURES_PHASE_TRACKER Template

**🚨 MANDATORY for all multi-sub-feature projects**

Create in: `feature-updates/{feature_name}/SUB_FEATURES_PHASE_TRACKER.md`

**Purpose:** Complete source of truth tracking each sub-feature through ALL phases from planning through commit.

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

**When to use this tracker:**
- **START OF EVERY SESSION:** Agent checks this file BEFORE any other work
- **BEFORE marking phase complete:** Agent re-reads corresponding guide to verify all steps followed
- **AFTER completing phase:** Agent updates `[x]` and "Current Status" immediately
- **BEFORE Phase 6/7:** Agent verifies quality gates are met
- **AGENT RESUMPTION:** Next agent reads "Current Status" to know where to continue
- **THROUGHOUT IMPLEMENTATION:** Track TODO creation, implementation, and QC progress

**Why this is critical:**
- Tracks 800+ checkpoints (8 sub-features × 100+ checkpoints each)
- Prevents phase skipping (can't skip Phase 3 questions or TODO Round 2)
- Enforces guide compliance (mandatory re-read requirement)
- Supports agent resumption (exact checkpoint preserved)
- Provides complete audit trail from planning through commit

---

### Sub-Feature Spec Template

Create in: `feature-updates/{feature_name}/sub_feature_{N}_{descriptive_name}_spec.md`

```markdown
# Sub-Feature {N}: {Descriptive Name}

## Objective

{What this sub-feature accomplishes - 1-2 sentences}

## Dependencies

**Prerequisites:** {Which sub-features must complete first, or "None" if foundation}

**Blocks:** {Which sub-features depend on this one completing}

## Scope

### Checklist Items ({X} total)

**From {Category} ({Item Range}):**
- {ITEM-ID}: {Description}
- {ITEM-ID}: {Description}
...

**From {Category} ({Item Range}):**
- {ITEM-ID}: {Description}
...

## Implementation Details

### {Component 1}

{Detailed description of what needs to be implemented}

**Approach:**
{How it will be implemented}

**Files Affected:**
- `path/to/file.py` (lines X-Y) - {Description of changes}

### {Component 2}

{Details...}

## Data Flow

{Diagram or description of how data moves through this sub-feature}

```
Input: {source}
  ↓
{Processing step 1}
  ↓
{Processing step 2}
  ↓
Output: {destination} → Used by {consumer}
```

## Key Algorithms

{Pseudocode or description of core algorithms}

## Integration Points

### With Other Sub-Features

**Depends on Sub-feature {N}:**
- Uses: {interface/method/data}
- Contract: {what we expect}

**Provides to Sub-feature {N}:**
- Exposes: {interface/method/data}
- Contract: {what we guarantee}

### With Existing Code

**Calls:**
- `ClassName.method_name()` - {purpose}

**Called by:**
- `OtherClass.method()` - {purpose}

## Assumptions

| Assumption | Basis | Risk if Wrong | Mitigation |
|------------|-------|---------------|------------|
| {Assumption} | {Why we believe this} | {Impact} | {How to handle if wrong} |

## Testing Requirements

### Unit Tests

- Test {scenario 1}
- Test {scenario 2}
...

### Integration Tests

- Test integration with Sub-feature {N}
- Test with existing code at {integration point}

## Success Criteria

✅ **Core Functionality:**
- [ ] {Criterion 1}
- [ ] {Criterion 2}

✅ **Error Handling:**
- [ ] {Criterion 1}

✅ **Testing:**
- [ ] All unit tests passing (100%)
- [ ] Integration tests with completed sub-features passing

✅ **Code Quality:**
- [ ] {Quality criterion}

## Notes

**Temporary Conversions:**
- {Any temporary workarounds}

**Out of Scope:**
- {What's explicitly not in this sub-feature}

**Dependencies for Next Sub-Features:**
- Sub-feature {N} depends on {what from this sub-feature}
```

---

### Sub-Feature Checklist Template

Create in: `feature-updates/{feature_name}/sub_feature_{N}_{descriptive_name}_checklist.md`

```markdown
# Sub-Feature {N}: {Descriptive Name} - Checklist

## Purpose

Track open questions and decisions for THIS sub-feature only.

**Deep Dive Status:** {Phase X of feature_deep_dive_guide.md}

---

## Core Functionality ({X} items)

- [ ] **{ID}:** {Question or decision needed}
  - Context: {Why this matters}
  - Options: {If multiple approaches}
  - Recommendation: {If researched}

- [x] **{ID}:** {Resolved decision} ✅ RESOLVED
  - Decision: {What was chosen}
  - Rationale: {Why}

---

## Error Handling ({Y} items)

- [ ] **{ID}:** {Question}
...

---

## Testing ({Z} items)

- [ ] **{ID}:** {Question}
...

---

## Integration ({W} items)

- [ ] **{ID}:** Integration with Sub-feature {N}
  - Question: {What needs clarification}
...

---

## Status Summary

**Total Items:** {X}
**Resolved:** {Y} [x]
**Pending:** {Z} [ ]

**Ready for Implementation:** {YES / NO}
```

---

### Research Folder README Template

Create in: `feature-updates/{feature_name}/research/README.md`

```markdown
# Research and Analysis Documents

This folder contains all research, analysis, and verification reports generated during planning.

**Purpose:**
- Keeps root folder clean (only specs, checklists, README)
- Centralizes reference material
- Clear separation: specs = implementation guidance, research = context

**File Naming:**
- `{TOPIC}_ANALYSIS.md` - Detailed analysis of specific topic
- `VERIFICATION_REPORT_{DATE}.md` - Verification findings
- `RESEARCH_FINDINGS_{DATE}.md` - General research results
- `{ALGORITHM}_ALGORITHM_ANALYSIS.md` - Algorithm deep dives

**All research documents go here from the start.**

## Files in this folder

| File | Purpose | Key Findings |
|------|---------|-------------|
| `{filename}.md` | {Purpose} | {Summary of findings} |
| ... | ... | ... |

## How to Use These Documents

**During Deep Dive:**
- Research documents support decision-making
- Reference when answering checklist questions

**During Implementation:**
- Verify implementation matches research findings
- Use as reference for complex algorithms

**After Completion:**
- Preserved in done/ folder for future reference
- Helpful for similar features
```

---

## Related Files

| File | Purpose |
|------|---------|
| `feature_creation_guide.md` | Initial planning & sub-feature breakdown |
| `feature_deep_dive_guide.md` | Per-sub-feature detailed planning |
| `feature_planning_guide.md` | Legacy monolithic planning (DEPRECATED) |
| `todo_creation_guide.md` | TODO creation (execute per sub-feature) |
| `implementation_execution_guide.md` | Implementation (execute per sub-feature) |
| `post_implementation_guide.md` | QC & validation (execute per sub-feature) |
| `protocols/README.md` | Detailed protocol definitions |
| `README.md` | Guide overview |
