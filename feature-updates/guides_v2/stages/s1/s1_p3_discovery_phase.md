# S1.P3: Discovery Phase Guide

**Guide Version:** 1.0
**Created:** 2025-01-20
**Prerequisites:** S1 Steps 1-2 complete (Initial Setup + Epic Analysis)
**Next Step:** S1 Step 4 (Feature Breakdown Proposal)
**Template:** `templates/discovery_template.md`

---

## Quick Start

**What is this guide?**
The Discovery Phase is a mandatory iterative research loop where the agent explores the problem space, asks clarifying questions, and refines understanding before proposing feature breakdown.

**When do you use this guide?**
- After completing S1 Step 2 (Epic Analysis)
- Before proposing feature breakdown (S1 Step 4)
- For EVERY epic (mandatory, not optional)

**Key Outputs:**
- DISCOVERY.md created and user-approved
- Problem space thoroughly explored
- Solution approach determined
- Scope clearly defined (in/out/deferred)
- Feature breakdown ready to propose

**Time-Box by Epic Size:**
| Epic Size | Discovery Time-Box | Typical Iterations |
|-----------|-------------------|-------------------|
| SMALL (1-2 features) | 1-2 hours | 2-3 iterations |
| MEDIUM (3-5 features) | 2-3 hours | 3-5 iterations |
| LARGE (6+ features) | 3-4 hours | 5-7 iterations |

**Exit Condition:**
Discovery Phase is complete when a research iteration produces no new questions, DISCOVERY.md is complete, and user has approved the recommended approach and feature breakdown.

---

## Critical Rules

```
+-------------------------------------------------------------+
| CRITICAL RULES - Copy to EPIC_README.md Agent Status        |
+-------------------------------------------------------------+

1. Discovery Phase is MANDATORY for every epic
   - No exceptions, even for "clear" epics
   - Cannot create feature folders until Discovery completes

2. Discovery Loop continues until NO NEW QUESTIONS emerge
   - Not a fixed number of iterations
   - Exit when research round produces zero questions

3. All findings and answers go in DISCOVERY.md
   - Single source of truth for epic-level decisions
   - Feature specs will reference this document

4. User answers questions throughout (not just at end)
   - Present questions after each research iteration
   - Update DISCOVERY.md with answers before next iteration

5. DISCOVERY.md becomes reference after approval
   - Only update if something found incorrect/outdated
   - Feature specs reference Discovery for shared context

6. Feature folders NOT created until Discovery approved
   - Discovery informs feature breakdown
   - Cannot know features until Discovery complete
```

---

## Workflow Overview

```
+-------------------------------------------------------------+
|                 DISCOVERY PHASE WORKFLOW                     |
+-------------------------------------------------------------+

S1.P3.1: Initialize Discovery Document (10-15 min)
    |
    +-- Create DISCOVERY.md from template
    +-- Extract initial questions from epic request
    +-- Set time-box based on epic size
    |
    v
S1.P3.2: Discovery Loop (iterative)
    |
    +------------------------------------------+
    |                                          |
    |   +-------------+                        |
    |   |  Research   | Read code, docs        |
    |   +------+------+                        |
    |          |                               |
    |          v                               |
    |   +-------------+                        |
    |   |  Document   | Update DISCOVERY.md    |
    |   +------+------+                        |
    |          |                               |
    |          v                               |
    |   +-------------+     No questions       |
    |   | Questions?  |--------+               |
    |   +------+------+        |               |
    |          | Has questions |               |
    |          v               |               |
    |   +-------------+        |               |
    |   |  Ask User   |        |               |
    |   +------+------+        |               |
    |          |               |               |
    |          v               |               |
    |   +-------------+        |               |
    |   |   Record    |        |               |
    |   +------+------+        |               |
    |          |               |               |
    |          +---------------+               |
    |          Loop back       |               |
    |                          v               |
    +--------------------------+ Exit Loop     |
    |
    v
S1.P3.3: Synthesize Findings (20-30 min)
    |
    +-- Compare solution options
    +-- Document recommended approach
    +-- Define scope (in/out/deferred)
    +-- Draft feature breakdown
    |
    v
S1.P3.4: User Approval
    |
    +-- Present Discovery summary
    +-- User approves approach and breakdown
    +-- DISCOVERY.md marked complete
    |
    v
Proceed to S1 Step 4 (Feature Breakdown Proposal)
```

---

## S1.P3.1: Initialize Discovery Document

**Time:** 10-15 minutes

### Step 1: Create DISCOVERY.md

Create `DISCOVERY.md` in the epic folder using the template.

**Location:** `feature-updates/KAI-{N}-{epic_name}/DISCOVERY.md`

**Template:** `templates/discovery_template.md`

### Step 2: Write Epic Request Summary

Summarize what the user requested in 2-4 sentences. Capture the essence without interpretation.

**Example:**
```markdown
## Epic Request Summary

User wants easier test runs for scripts, automated smoke testing,
and "debugging version runs" for league helper modes (4 modes),
simulations (win rate, accuracy), and data fetchers (player, scores,
historical, schedule).

**Original Request:** `improve_debugging_runs_notes.txt`
```

### Step 3: Extract Initial Questions

Read the epic request and identify initial questions.

**Question sources:**
- Ambiguous language ("easier", "better", "improved")
- Undefined terms ("debugging version run")
- Implicit assumptions that need verification
- Scope boundaries that are unclear

**Example initial questions:**
```markdown
### Pending Questions

| # | Question | Context | Asked |
|---|----------|---------|-------|
| 1 | What does "debugging version run" mean? | Term undefined in request | 2025-01-20 |
| 2 | Should all scripts share the same debug approach? | 6 different scripts mentioned | 2025-01-20 |
| 3 | What makes current testing "not easy"? | Need to understand pain points | 2025-01-20 |
```

### Step 4: Set Time-Box

Based on epic size (from S1 Step 2.3), set Discovery time-box:

| Epic Size | Time-Box |
|-----------|----------|
| SMALL (1-2 features) | 1-2 hours |
| MEDIUM (3-5 features) | 2-3 hours |
| LARGE (6+ features) | 3-4 hours |

Document in Discovery Log:
```markdown
## Discovery Log

| Timestamp | Activity | Outcome |
|-----------|----------|---------|
| 2025-01-20 10:00 | Initialized Discovery | Epic size MEDIUM, time-box 2-3 hours |
```

### Step 5: Update Agent Status

```markdown
## Agent Status

**Current Phase:** DISCOVERY_PHASE
**Current Step:** S1.P3.1 Complete - Initialize Discovery
**Current Guide:** stages/s1/s1_p3_discovery_phase.md
**Progress:** Discovery initialized, entering loop
**Next Action:** S1.P3.2 - Discovery Loop Iteration 1
```

---

## S1.P3.2: Discovery Loop

**Time:** Varies by epic size (bulk of Discovery time)

The Discovery Loop repeats until a research iteration produces no new questions.

### Iteration Structure

Each iteration follows this pattern:

```
A. Research (read code, examine patterns)
       |
       v
B. Document (update DISCOVERY.md with findings)
       |
       v
C. Identify Questions (what unknowns emerged?)
       |
       v
D. Ask User (present questions, await answers)
       |
       v
E. Record Answers (update DISCOVERY.md)
       |
       v
F. Check Exit (any new questions? if no, exit loop)
```

---

### Step A: Research

**What to research:**

1. **Components mentioned in epic**
   - Scripts, modules, classes referenced
   - Entry points and argument handling
   - Current behavior and interfaces

2. **Existing patterns**
   - Similar functionality that exists
   - Patterns that could be leveraged
   - Conventions used in codebase

3. **Pain points**
   - Why current approach is problematic
   - What's missing vs what exists
   - Friction points user might experience

4. **Solution space**
   - Possible approaches
   - Trade-offs between options
   - Constraints that limit choices

5. **External dependencies** (NEW - from KAI-1 lessons)
   - Libraries or APIs the epic might require
   - Known compatibility issues with test environments
   - Experience with these libraries in previous features
   - Alternative libraries if primary choice has issues

**Research activities:**
- Use Grep/Glob to find relevant files
- Use Read to examine actual code
- Document file paths, line numbers, key findings
- Note what exists vs what's missing

**DO:**
- Read actual source code
- Note specific file paths and line numbers
- Look for existing patterns to leverage
- Consider multiple solution approaches

**DO NOT:**
- Write any code (research only)
- Make assumptions without verification
- Skip reading code you reference
- Guess at implementation details

---

### Step B: Document Findings

Update DISCOVERY.md with iteration findings:

```markdown
### Iteration {N} ({YYYY-MM-DD HH:MM})

**Researched:** {What was investigated}

**Files Examined:**
- `run_league_helper.py` (lines 45-78): Uses argparse, has 4 mode choices
- `run_simulation.py` (lines 12-34): Has --iterations flag, default 1000
- `utils/logging_config.py` (lines 1-50): Existing verbose logging setup

**Key Findings:**
- League helper uses argparse with mode selection
- Simulation already has iteration count parameter
- Verbose logging infrastructure exists in utils/
- No consistent debug flag pattern across scripts

**Questions Identified:**
- Should debug mode use existing verbose logging?
- What iteration count is appropriate for debug runs?
```

---

### Step C: Identify Questions

**Question types to look for:**

| Type | Description | Example |
|------|-------------|---------|
| **Clarification** | Epic language is ambiguous | "What does 'easier' mean specifically?" |
| **Scope** | Boundaries unclear | "All 4 modes or just specific ones?" |
| **Preference** | Multiple valid approaches | "CLI flags or config file?" |
| **Priority** | Trade-offs need input | "Speed or thoroughness for debug?" |
| **Constraint** | Limits need verification | "Must work offline?" |
| **External Dependencies** | Libraries/APIs needed | "Will we use ESPN API or another source?" "Are there known compatibility issues?" |

**For each question, document:**
- The question itself
- Why it matters (context)
- What research triggered it

---

### Step D: Ask User

Present questions to user after each research iteration.

**Format:**
```markdown
## Discovery Iteration {N} - Questions

Based on my research, I have the following questions:

### Question 1: {Category}
{Question text}

**Context:** {Why this matters / what research raised this}

**Options (if applicable):**
- Option A: {description}
- Option B: {description}

### Question 2: {Category}
{Question text}

**Context:** {Why this matters}

---

Please answer these questions so I can continue research.
```

**Guidelines:**
- Batch related questions together
- Provide context for why each question matters
- Offer options when clear choices exist
- Keep questions specific and actionable

---

### Step E: Record Answers

Update DISCOVERY.md with user answers:

```markdown
### Resolved Questions

| # | Question | Answer | Impact | Resolved |
|---|----------|--------|--------|----------|
| 1 | What does "debugging version run" mean? | Fewer iterations + verbose output | Defines debug behavior | 2025-01-20 |
| 2 | CLI flags or config file? | CLI flag preferred, config override nice | Design both mechanisms | 2025-01-20 |
```

Also update Discovery Log:
```markdown
| 2025-01-20 10:45 | User answered Q1-Q3 | Clarified debug behavior, preferred CLI approach |
```

---

### Step F: Check Exit Condition

**Continue loop if:**
- New questions emerged from research
- Research revealed new unknowns
- Scope still unclear
- Solution approach not determined

**Exit loop when:**
- Research iteration produced NO new questions
- Scope is well-defined
- Solution approach is clear
- Ready to propose feature breakdown

**Exit checkpoint:**
```markdown
## Discovery Loop Exit Check

[ ] Research iteration produced no new questions
[ ] All pending questions resolved
[ ] Scope clearly defined (in/out/deferred documented)
[ ] Solution approach identified
[ ] Can articulate feature breakdown rationale

If any unchecked --> Continue loop
If all checked --> Proceed to S1.P3.3 Synthesis
```

---

## S1.P3.3: Synthesize Findings

**Time:** 20-30 minutes

After the Discovery Loop exits, compile findings into actionable recommendations.

### Step 1: Document Solution Options

For each approach identified during research:

```markdown
## Solution Options

### Option 1: CLI Flags Per Script

**Description:** Add --debug flag to each script that enables reduced iterations and verbose logging.

**Pros:**
- Simple, familiar pattern
- Per-script control
- No new dependencies

**Cons:**
- Must update each script individually
- No centralized configuration

**Effort Estimate:** MEDIUM

**Fit Assessment:** Good - matches user's CLI preference

### Option 2: Shared Debug Configuration

**Description:** Central debug config in shared_config.py, read by all scripts.

**Pros:**
- Single place to configure
- Consistent behavior

**Cons:**
- Less per-script flexibility
- Must modify config loading

**Effort Estimate:** MEDIUM

**Fit Assessment:** Good - supports override requirement
```

### Step 2: Create Comparison Summary

```markdown
### Option Comparison Summary

| Option | Effort | Fit | Recommended |
|--------|--------|-----|-------------|
| CLI Flags Per Script | MEDIUM | GOOD | YES (combined) |
| Shared Debug Config | MEDIUM | GOOD | YES (combined) |
| Separate Test Scripts | HIGH | POOR | NO |
```

### Step 3: Document Recommended Approach

```markdown
## Recommended Approach

**Recommendation:** Combined CLI flags + shared config

**Rationale:**
- User prefers CLI flags (Q2 answer)
- User wants config override capability (Q2 answer)
- Existing verbose logging can be leveraged (Iteration 1 finding)
- Pattern is consistent with codebase conventions (Iteration 2 finding)

**Key Design Decisions:**
- --debug flag on each script: Triggers debug mode
- Shared config for defaults: debug_iterations=1, debug_verbose=True
- Per-script override: Scripts can customize debug behavior
```

### Step 4: Define Scope

```markdown
## Scope Definition

### In Scope
- --debug CLI flag for all 6 script types
- Shared debug configuration
- Reduced iterations (default: 1)
- Verbose logging enabled

### Out of Scope
- Mock data support - deferred to future epic
- GUI/interactive debug mode - not requested
- Automated test framework - separate concern

### Deferred (Future Work)
- Mock data option - nice-to-have, revisit after core debug works
```

### Step 5: Draft Feature Breakdown

```markdown
## Proposed Feature Breakdown

**Total Features:** 4
**Implementation Order:** Sequential (Feature 1 first, then 2-4 can parallel)

### Feature 1: debug_infrastructure

**Purpose:** Shared debug configuration and utilities used by all scripts

**Scope:**
- Debug configuration in shared_config.py
- Verbose logging setup for debug mode
- Common debug utilities

**Dependencies:** None (foundation feature)

**Discovery Basis:**
- Based on Finding: Existing verbose logging in utils/ (Iteration 1)
- Based on User Answer: Shared config with per-script override (Q5)

**Estimated Size:** SMALL

### Feature 2: league_helper_debug

**Purpose:** Debug mode for all 4 league helper modes

**Scope:**
- --debug flag for run_league_helper.py
- Debug behavior for draft, optimizer, trade, data editor modes
- Integration with debug infrastructure

**Dependencies:** Feature 1 (debug_infrastructure)

**Discovery Basis:**
- Based on Finding: Uses argparse with mode selection (Iteration 1)
- Based on User Answer: All 4 modes need debug support (Q2)

**Estimated Size:** MEDIUM

### Feature 3: simulation_debug

**Purpose:** Debug mode for win rate and accuracy simulations

**Scope:**
- --debug flag for run_simulation.py
- Reduced iterations for both simulation types
- Verbose output during simulation

**Dependencies:** Feature 1 (debug_infrastructure)

**Discovery Basis:**
- Based on Finding: Has --iterations flag already (Iteration 1)
- Based on User Answer: 1 iteration default, configurable (Q4)

**Estimated Size:** SMALL

### Feature 4: fetcher_debug

**Purpose:** Debug mode for all data fetcher scripts

**Scope:**
- --debug flag for player, scores, historical, schedule fetchers
- Reduced data fetching in debug mode
- Verbose logging

**Dependencies:** Feature 1 (debug_infrastructure)

**Discovery Basis:**
- Based on Finding: Similar patterns across fetchers (Iteration 2)
- Based on User Answer: Same approach for all fetchers (Q5)

**Estimated Size:** MEDIUM
```

---

## S1.P3.4: User Approval

**Time:** 5-10 minutes

Present Discovery summary to user for approval.

### Approval Presentation

```markdown
## Discovery Phase Complete

I've completed the Discovery Phase for this epic.

**Time Spent:** {X} hours
**Iterations:** {N}
**Questions Resolved:** {M}
**Document:** `DISCOVERY.md`

### Summary of Findings

Through {N} research iterations and {M} questions, I've determined that
the best approach is {brief description}. Key findings include {finding 1},
{finding 2}, and {finding 3}.

### Recommended Approach

{2-3 sentence description of recommended solution}

### Proposed Scope

**In Scope:**
- {Item 1}
- {Item 2}
- {Item 3}

**Out of Scope:**
- {Item 1}

### Proposed Feature Breakdown

Based on Discovery research, I recommend {N} features:

1. **{Feature 1}:** {Brief description}
2. **{Feature 2}:** {Brief description}
3. **{Feature 3}:** {Brief description}
4. **{Feature 4}:** {Brief description}

### Questions for You

- Does this approach align with your expectations?
- Any scope adjustments needed?
- Does the feature breakdown make sense?

**Please approve to proceed to formal feature breakdown (S1 Step 4).**
```

### Handle User Response

**If user approves:**
1. Mark DISCOVERY.md status as COMPLETE
2. Update User Approval section with date
3. Proceed to S1 Step 4

**If user requests changes:**
1. Discuss concerns
2. Update DISCOVERY.md as needed
3. Re-present for approval

**If user has additional questions:**
1. Add to Discovery Questions
2. Research if needed
3. Update DISCOVERY.md
4. Re-present for approval

### Update DISCOVERY.md

```markdown
## User Approval

**Discovery Approved:** YES
**Approved Date:** 2025-01-20
**Approved By:** User

**Approval Notes:**
User approved recommended approach. Confirmed 4-feature breakdown is correct.
```

### Update Agent Status

```markdown
## Agent Status

**Current Phase:** EPIC_PLANNING
**Current Step:** S1.P3.4 Complete - Discovery Approved
**Current Guide:** stages/s1/s1_epic_planning.md
**Progress:** Discovery complete, proceeding to feature breakdown
**Next Action:** S1 Step 4 - Feature Breakdown Proposal
```

---

## Completion Criteria

**Discovery Phase is COMPLETE when ALL of these are true:**

```
[ ] DISCOVERY.md created with all sections populated
[ ] Discovery Loop exited (research produced no new questions)
[ ] All pending questions resolved
[ ] Solution options documented with comparison
[ ] Recommended approach documented with rationale
[ ] Scope defined (in/out/deferred)
[ ] Feature breakdown drafted with Discovery basis
[ ] User approved Discovery findings
[ ] DISCOVERY.md marked as COMPLETE
[ ] Agent Status updated for S1 Step 4
```

---

## Common Mistakes to Avoid

```
+------------------------------------------------------------+
| "If You're Thinking This, STOP" - Anti-Pattern Detection   |
+------------------------------------------------------------+

X "This epic seems clear, I'll skip Discovery"
  --> STOP - Discovery is MANDATORY for every epic

X "I'll just ask all questions at once to save time"
  --> STOP - Questions emerge from research; ask after each iteration

X "I know the answer, don't need to ask user"
  --> STOP - User answers all scope/preference questions

X "I'll create feature folders now and update Discovery later"
  --> STOP - Feature folders created AFTER Discovery approval

X "No more questions, but I haven't researched component X"
  --> STOP - Ensure thorough research before declaring no questions

X "User approved, but I want to add one more feature"
  --> STOP - Feature breakdown is what user approved

X "I'll update DISCOVERY.md later with answers"
  --> STOP - Update immediately after each Q&A round
```

---

## Re-Reading Checkpoints

**CHECKPOINT 1:** After S1.P3.1 (Initialize)
- Re-read "Critical Rules" section
- Verify DISCOVERY.md created with initial questions
- Verify time-box set based on epic size

**CHECKPOINT 2:** After each Discovery Loop iteration
- Re-read "Discovery Loop" section
- Verify findings documented
- Verify questions asked and answers recorded

**CHECKPOINT 3:** Before S1.P3.4 (User Approval)
- Re-read "Synthesize Findings" section
- Verify all sections of DISCOVERY.md complete
- Verify feature breakdown has Discovery basis for each feature

---

## Next Step

**After completing Discovery Phase:**

--> **Proceed to:** S1 Step 4 (Feature Breakdown Proposal)

**What happens in Step 4:**
- Present feature breakdown to user (already drafted in Discovery)
- User confirms/modifies breakdown
- Create epic ticket
- User validates epic ticket

**Prerequisites for Step 4:**
- DISCOVERY.md complete and user-approved
- Feature breakdown drafted with Discovery basis
- Recommended approach documented

---

*End of S1.P3 Discovery Phase Guide*
