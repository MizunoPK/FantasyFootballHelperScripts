# Feature Templates

This file contains all file templates used during feature planning and development. Reference these when creating new feature files.

---

## Quick Template Index

| Template | When to Use | Section |
|----------|-------------|---------|
| README.md | Phase 1: Create structure | [Link](#feature-readme-template) |
| {feature_name}_specs.md | Phase 1: Create structure | [Link](#specification-template) |
| Dependency Map | Phase 2.6: Add to specs | [Link](#dependency-map-template) |
| {feature_name}_checklist.md | Phase 1: Create structure | [Link](#checklist-template) |
| {feature_name}_lessons_learned.md | Phase 1: Create structure | [Link](#lessons-learned-template) |
| {feature_name}_questions.md | Step 3: Create questions | [Link](#questions-file-template) |
| {feature_name}_todo.md | Step 1: Create TODO | [Link](#todo-file-template) |
| {feature_name}_code_changes.md | After TODO creation | [Link](#code-changes-template) |

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
- [ ] QC Round 1
- [ ] QC Round 2
- [ ] QC Round 3
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

## Related Files

| File | Purpose |
|------|---------|
| `feature_planning_guide.md` | Planning phase workflow |
| `feature_development_guide.md` | Development phase workflow |
| `protocols_reference.md` | Detailed protocol definitions |
| `README.md` | Guide overview |
