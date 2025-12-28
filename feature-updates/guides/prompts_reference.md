# Prompts Reference

This file contains ready-to-use conversation prompts for guiding planning and development conversations with users.

---

## Quick Prompt Index

| Situation | Section |
|-----------|---------|
| User has vague ideas | [Suggesting Options](#when-user-has-vague-ideas) |
| Details are missing | [Surfacing Questions](#when-details-are-missing) |
| Scope is growing | [Scope Management](#when-scope-is-creeping) |
| Technical decision needed | [Technical Decisions](#when-technical-decisions-are-needed) |
| Edge cases to discuss | [Edge Cases](#when-edge-cases-need-discussion) |
| Ready to move forward | [Progress Updates](#when-ready-to-move-forward) |
| Presenting investigation results | [Investigation Results](#presenting-investigation-results) |
| Asking for direction | [Direction Requests](#asking-for-direction) |
| After verification round | [Presenting Round Summary](#presenting-round-summary) |
| Before implementation | [Presenting Interface Contracts](#presenting-interface-contracts) |
| Starting new phase | [Phase Transitions](#phase-transition-prompts) |

---

## Phase Transition Prompts

**CRITICAL:** These prompts MUST be used when transitioning between phases. Agents must READ the guide FIRST, acknowledge key requirements, THEN proceed.

### Starting Feature Creation

Use when user says "Help me develop {feature-name}" or "Let's plan {feature-name}":

> "I'm reading `feature_creation_guide.md` to ensure I follow the initial planning workflow...
>
> **The guide requires:**
> - Phase 1: Create feature folder and move notes
> - Phase 2: Broad reconnaissance (identify major components, estimate scope)
> - **Phase 3: CRITICAL CHECKPOINT - Sub-feature breakdown decision**
>   - Evaluate if feature should be broken into sub-features
>   - Triggers: 3+ components, 30+ items, multiple subsystems, mixed risk levels
> - Phase 4: Create file structure (single OR sub-features)
>   - If single: Create spec + checklist
>   - If sub-features: Create SUB_FEATURES_README.md + per-sub-feature files
>   - ALWAYS: Create research/ subfolder
> - Phase 5: Transition to deep dive planning
>
> **NO global checklist/spec if using sub-features** - only sub-feature specific files
>
> I'll now proceed with Phase 1: Initial Setup..."

---

### Starting Deep Dive (Per Sub-Feature)

Use when starting detailed planning for a sub-feature (or single feature):

> "I'm reading `feature_deep_dive_guide.md` to ensure I follow the complete deep dive workflow...
>
> **The guide requires:**
> - Phase 1: Targeted research (ONLY for this sub-feature's scope)
> - Phase 2: Update spec and checklist with findings
> - **Phase 3: Interactive question resolution**
>   - **ONE question at a time** (Lesson 1)
>   - Update spec/checklist after EACH answer
>   - Evaluate for new questions after each resolution
> - Phase 4: Sub-feature complete + **dynamic scope adjustment check**
>   - If scope grew significantly (>35 items), propose split into additional sub-features
> - Phase 5: Next sub-feature or alignment review
> - **Phase 6: Cross-sub-feature alignment review** (MANDATORY for multi-sub-feature)
>   - Review all specs together for conflicts
>   - Verify interface contracts align
>   - Fix conflicting assumptions
> - Phase 7: Ready for sequential implementation
>
> **All research documents go in research/ folder**
>
> I'll now proceed with Phase 1: Targeted Research for {sub-feature name}..."

---

### Starting TODO Creation (Phase 2a)

Use when user says "Prepare for updates based on {feature-name}" or "Create the TODO file":

> "I'm reading `todo_creation_guide.md` to ensure I follow all 24 verification iterations...
>
> **The guide requires:**
> - **24 mandatory iterations** across 3 rounds (Rounds 1-3: iterations 1-7, 8-16, 17-24)
> - Algorithm Traceability Matrix (iterations 4, 11, 19)
> - TODO Specification Audit (iteration 4a) - acceptance criteria for every task
> - Pre-Implementation Spec Audit (iteration 23a) - 4-part fresh-eyes audit
> - Integration Gap Check (iterations 7, 14, 23) - verify all callers
> - Implementation Readiness Protocol (iteration 24) - final go/no-go
> - **NO SKIPPING ITERATIONS** - complexity hides, shortcuts cause 40% QC failure
>
> I'll now proceed with Round 1 (iterations 1-7). I'll create the questions file after iteration 7 if needed."

---

### Starting Implementation (Phase 2b)

Use when user says "Start implementation" or "Begin coding":

> "I'm reading `implementation_execution_guide.md` to ensure I follow the complete implementation workflow...
>
> **The guide requires:**
> - Interface Verification Protocol FIRST (verify all method signatures from source)
> - Create implementation checklist from specs.md
> - Implement phase-by-phase with continuous validation
> - Run unit tests after EVERY phase (100% pass required)
> - Mini-QC checkpoints after each major component
> - Keep specs.md VISIBLE during implementation
> - Document all changes in code_changes.md incrementally
>
> I'll now execute Interface Verification Protocol before writing any code..."

---

### Starting Post-Implementation QC (Phase 2c)

Use when user says "Run QC" or "Validate the implementation":

> "I'm reading `post_implementation_guide.md` to ensure I follow all validation protocols...
>
> **The guide requires:**
> - **Smoke Testing Protocol** (3 parts: import, entry point, E2E execution) - MANDATORY
> - **3 QC Rounds** (no exceptions):
>   - Round 1: Script execution test + document review
>   - Round 2: Deep verification + semantic diff check
>   - Round 3: Final skeptical review
> - **Requirement Verification Protocol** - 100% completion required
> - **Algorithm Verification** - implementation must match spec exactly
> - Lessons learned capture for guide improvements
>
> I'll now begin with the Smoke Testing Protocol (Part 1: Import Test)..."

---

### Resuming In-Progress Feature

Use when resuming work on an existing feature folder:

> "I found an in-progress feature: `{feature-name}/`
>
> Reading `{feature-name}/README.md` to understand current status...
>
> **Agent Status from README:**
> - Current Phase: {phase}
> - Current Step: {step}
> - Next Action: {action}
> - Completion Status: {X/Y items complete}
>
> I'll continue from where the previous agent left off: {next action description}"

---

## Planning Phase Prompts

### When User Has Vague Ideas

Use when the user knows what they want but hasn't defined specifics:

> "I notice we haven't defined {X}. Let me suggest a few approaches:
> 1. **Option A** - {description} (Pros: ... Cons: ...)
> 2. **Option B** - {description} (Pros: ... Cons: ...)
>
> Based on {context from codebase}, I'd recommend **Option A** because..."

---

### When Details Are Missing

Use when you need specific information to proceed:

> "For {component}, we need to decide:
> - Where does the data come from?
> - What format will it be in?
> - How will errors be handled?
>
> Looking at the existing codebase, I see {similar code} handles this by..."

---

### When Scope Is Creeping

Use when requirements keep expanding:

> "This is getting larger in scope. Let me clarify what's in vs out:
> - **In scope:** {core requirements}
> - **Potentially out of scope:** {extras}
>
> Would you like to include {extra item} in this feature, or save it for later?"

---

### When Technical Decisions Are Needed

Use when there are multiple valid implementation approaches:

> "I've found a few ways to implement {feature}:
> 1. **{Approach A}** - {brief description}
>    - Similar to how `{existing_file.py}` does it
>    - Pros: ...
>    - Cons: ...
> 2. **{Approach B}** - {brief description}
>    - Pros: ...
>    - Cons: ...
>
> My recommendation is **{Approach X}** because it aligns with the existing patterns in the codebase."

---

### When Edge Cases Need Discussion

Use when you've identified scenarios that need explicit handling:

> "I've identified some edge cases we should decide on:
> - **{Edge case 1}:** What happens when {scenario}?
> - **{Edge case 2}:** How should we handle {scenario}?
>
> For {edge case 1}, similar code in `{file}` handles this by {approach}. Should we follow the same pattern?"

---

### When Ready to Move Forward

Use when transitioning between checklist items:

> "We've resolved {N} items. The remaining questions are:
> - {Question 1}
> - {Question 2}
>
> Which would you like to address next? Or if you'd like, I can investigate {item} and propose an answer."

---

### Presenting Investigation Results

Use after researching a specific question:

> "I investigated {topic}. Here's what I found:
>
> **Current Codebase Pattern:**
> {description of existing approach}
> - File: `{path/to/file.py}:{line_numbers}`
> - Pattern: {description}
>
> **Recommendation for this feature:**
> {recommended approach based on findings}
>
> Does this approach work for you?"

---

### Asking for Direction

Use at Phase 3 pause point:

> "Would you like to:
> 1. **Add more items** to the checklist before we start?
> 2. **Start addressing** specific checklist items?
>
> If starting, which item would you like to address first? You can either:
> - **Direct me to investigate** (I'll research and propose an answer)
> - **Provide the answer directly** (if you already know what you want)"

---

## Development Phase Prompts

### Starting a Verification Round

Use when beginning a new verification round:

> "Starting verification round {N} (iterations {X}-{Y}).
>
> This round focuses on:
> - {focus area 1}
> - {focus area 2}
>
> I'll update you when I complete the round or have questions."

---

### Presenting Questions File

Use when you've completed the questions file:

> "I've completed the first verification round (7 iterations) and have {N} questions that need your input before I can proceed.
>
> I've documented these in `{feature_name}_questions.md`. For each question, I've provided:
> - Context explaining why the question arose
> - 2-3 options with pros/cons
> - My recommendation
>
> Please review and provide your answers. I'll wait for your input before continuing."

---

### Reporting Verification Progress

Use to update user on verification status:

> "Completed iteration {N}/{24}.
>
> **Key findings this iteration:**
> - {finding 1}
> - {finding 2}
>
> **TODO updates:**
> - Added: {new tasks}
> - Modified: {changed tasks}
>
> Continuing to iteration {N+1}..."

---

### Implementation Phase Start

Use when beginning implementation:

> "All 24 verification iterations complete. TODO is ready for implementation.
>
> **Summary:**
> - Total tasks: {N}
> - Files to modify: {list}
> - New files to create: {list}
> - Tests to write: {N}
>
> I'll implement phase by phase, running tests after each phase. I'll update you on progress and flag any issues."

---

### Reporting Implementation Progress

Use to update on implementation:

> "Completed implementation phase {N}/{total}.
>
> **Changes made:**
> - {file 1}: {description}
> - {file 2}: {description}
>
> **Test status:** {X}/{Y} tests passing
>
> Proceeding to phase {N+1}..."

---

### QC Round Completion

Use after completing a QC round:

> "Completed Quality Control Round {N}/3.
>
> **Issues found:** {list or "None"}
> **Issues fixed:** {list or "N/A"}
> **Status:** {PASSED / ISSUES FOUND (fixed)}
>
> {Next action: proceeding to round N+1 / feature complete}"

---

### Presenting Interface Contracts

Use when documenting verified interfaces before implementation:

> "I've completed interface verification for all dependencies. Here are the verified contracts:
>
> **Dependencies Verified:**
> | Class | Method | Signature | Source |
> |-------|--------|-----------|--------|
> | {ClassName} | {method_name} | `{params} -> {return}` | {file.py}:{line} |
>
> **Data Model Attributes Verified:**
> | Model | Attribute | Type | Semantics |
> |-------|-----------|------|-----------|
> | {ModelName} | {attr} | {type} | {what it means} |
>
> **Key Findings:**
> - {any surprises or important notes about interfaces}
>
> Ready to proceed with implementation."

---

### Presenting Round Summary

Use after completing a verification round (7, 16, or 24):

> "Completed verification round {N} ({X} iterations).
>
> **Round Summary:**
> - Key findings: {what was learned}
> - Gaps identified: {what's still missing or unclear}
> - Scope changes: {any additions/removals from original scope}
> - Confidence level: {High/Medium/Low} - {brief justification}
>
> **Ready for:** {next phase: questions file / second round / implementation}"

---

## Problem Situation Prompts

### When Stuck on Investigation

Use when you can't find information:

> "I've searched for {topic} but couldn't find a clear pattern in the codebase.
>
> **What I searched:**
> - {search 1}: {result}
> - {search 2}: {result}
>
> **Options:**
> 1. I can search with different terms: {suggestions}
> 2. You might know where this is defined
> 3. We may need to establish a new pattern
>
> What would you like me to try?"

---

### When Requirements Conflict

Use when you find conflicting requirements:

> "I found a potential conflict in the requirements:
>
> **Requirement A:** {description}
> **Requirement B:** {description}
>
> **The conflict:** {explanation of why they can't both be true}
>
> Which should take priority? Or is there a way to satisfy both that I'm missing?"

---

### When Tests Are Failing

Use when encountering test failures:

> "Tests are failing after implementing {component}:
>
> **Failing test:** `{test_name}`
> **Error:** {error message}
> **Likely cause:** {your analysis}
>
> **Options:**
> 1. Fix the code: {approach}
> 2. Update the test: {if test expectation is wrong}
>
> I'll proceed with option {N} unless you prefer otherwise."

---

### When Requesting Clarification

Use when user's answer is ambiguous:

> "Thanks for the answer on {topic}. I want to confirm I understood correctly:
>
> **My understanding:** {your interpretation}
>
> **This means I'll:**
> - {action 1}
> - {action 2}
>
> Is this correct, or did you mean something different?"

---

## Related Files

| File | Purpose |
|------|---------|
| `feature_planning_guide.md` | Planning phase workflow |
| `feature_development_guide.md` | Development phase workflow |
| `protocols/README.md` | Detailed protocol definitions |
| `templates.md` | File templates |
