# S1.P3: Discovery Phase Guide

**Guide Version:** 1.0
**Created:** 2025-01-20
**Prerequisites:** S1 Steps 1-2 complete (Initial Setup + Epic Analysis)
**Next Step:** S1 Step 4 (Feature Breakdown Proposal)
**Template:** `templates/discovery_template.md`

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Overview](#overview)
3. [Critical Rules](#critical-rules)
4. [Workflow Overview](#workflow-overview)
5. [S1.P3.1: Initialize Discovery Document](#s1p31-initialize-discovery-document)
6. [S1.P3.2: Validation Loop Validation](#s1p32-validation-loop-validation)
7. [S1.P3.3: Synthesize Findings](#s1p33-synthesize-findings)
8. [S1.P3.4: User Approval](#s1p34-user-approval)
9. [Completion Criteria](#completion-criteria)
10. [Common Mistakes to Avoid](#common-mistakes-to-avoid)
11. [Re-Reading Checkpoints](#re-reading-checkpoints)
12. [Exit Criteria](#exit-criteria)
13. [Next Step](#next-step)

---

## Prerequisites

**Before starting S1.P3 (Discovery Phase):**

- [ ] S1 Steps 1-2 complete (Initial Setup + Epic Analysis)
- [ ] Epic folder created with EPIC_README.md
- [ ] Epic request file ({epic_name}_notes.txt) exists and reviewed
- [ ] Initial scope assessment complete (SMALL/MEDIUM/LARGE)
- [ ] Working directory: Epic folder root
- [ ] Read validation_loop_discovery.md to understand validation requirements

**If any prerequisite fails:**
- Return to S1 to complete missing steps
- Do NOT start Discovery until Steps 1-2 complete

---

## Overview

**What is this guide?**
The Discovery Phase is a mandatory research and validation process where the agent explores the problem space, creates a comprehensive DISCOVERY.md document, then validates it through Validation Loop protocol until 3 consecutive clean rounds confirm completeness.

**When do you use this guide?**
- After completing S1 Step 2 (Epic Analysis)
- Before proposing feature breakdown (S1 Step 4)
- For EVERY epic (mandatory, not optional)

**Key Outputs:**
- DISCOVERY.md created and user-approved
- Problem space thoroughly explored (validated through Validation Loop)
- Solution approach determined
- Scope clearly defined (in/out/deferred)
- Feature breakdown ready to propose

**Time-Box by Epic Size:**
| Epic Size | Discovery Time-Box | Typical Rounds |
|-----------|-------------------|----------------|
| SMALL (1-2 features) | 1-2 hours | 4-6 rounds (incl. 3 clean) |
| MEDIUM (3-5 features) | 2-3 hours | 5-8 rounds (incl. 3 clean) |
| LARGE (6+ features) | 3-4 hours | 7-10 rounds (incl. 3 clean) |

**Exit Condition:**
Discovery Phase is complete when Validation Loop validation produces THREE CONSECUTIVE clean rounds (zero issues/gaps), DISCOVERY.md is complete, and user has approved the recommended approach and feature breakdown.

**Validation Loop Reference:** `reference/validation_loop_discovery.md`

---

## Critical Rules

```text
+-------------------------------------------------------------+
| CRITICAL RULES - Copy to EPIC_README.md Agent Status        |
+-------------------------------------------------------------+

1. Discovery Phase is MANDATORY for every epic
   - No exceptions, even for "clear" epics
   - Cannot create feature folders until Discovery completes

2. Discovery uses Validation Loop validation (see validation_loop_discovery.md)
   - Exit criteria: 3 consecutive clean rounds with ZERO issues/gaps
   - Issues/gaps include: Missing research, incomplete sections, unanswered questions,
     assumptions not verified, integration gaps, unclear scope
   - Re-read DISCOVERY.md with fresh perspective each round
   - Fix ALL issues immediately (zero tolerance for deferred issues)

3. All findings and answers go in DISCOVERY.md
   - Single source of truth for epic-level decisions
   - Feature specs will reference this document

4. User answers questions throughout (not just at end)
   - Present questions when they arise during validation rounds
   - Update DISCOVERY.md with answers before continuing

5. DISCOVERY.md becomes reference after approval
   - Only update if something found incorrect/outdated
   - Feature specs reference Discovery for shared context

6. Feature folders NOT created until Discovery approved
   - Discovery informs feature breakdown
   - Cannot know features until Discovery complete
```

---

## Workflow Overview

```text
+-------------------------------------------------------------+
|                 DISCOVERY PHASE WORKFLOW                     |
+-------------------------------------------------------------+

S1.P3.1: Initialize Discovery Document (10-15 min)
    |
    +-- Create DISCOVERY.md from template
    +-- Conduct initial research
    +-- Document findings, questions, approach
    +-- Set time-box based on epic size
    |
    v
S1.P3.2: Validation Loop Validation (iterative)
    |
    +--------------------------------------------------+
    |  Reference: validation_loop_discovery.md        |
    |                                                  |
    |   +-------------+                                |
    |   | Round N     | Re-read DISCOVERY.md          |
    |   | Validation  | (fresh perspective!)          |
    |   +------+------+                                |
    |          |                                       |
    |          v                                       |
    |   +----------------+                             |
    |   | Identify       | Check for issues/gaps:     |
    |   | Issues/Gaps    | - Missing research         |
    |   |                | - Incomplete sections      |
    |   |                | - Unanswered questions     |
    |   |                | - Unverified assumptions   |
    |   |                | - Integration gaps         |
    |   |                | - Unclear scope            |
    |   +------+---------+                             |
    |          |                                       |
    |          v                                       |
    |   +-------------+      No issues                |
    |   |  Issues?    |--------+                      |
    |   +------+------+        |                      |
    |          | Has issues    | Counter++            |
    |          v               |                      |
    |   +-------------+        | Counter>=3?          |
    |   |  Fix ALL    |        +----No-----+          |
    |   |  Issues     |              |     |          |
    |   +------+------+        Reset |  Yes|          |
    |          |               Counter     |          |
    |          v                     |     |          |
    |   +-------------+              |     |          |
    |   |  Ask User   | (if needed)  |     |          |
    |   |  Questions  |              |     |          |
    |   +------+------+              |     |          |
    |          |                     |     |          |
    |          +---------------------+     |          |
    |          Loop back                   v          |
    +----------------------------------Exit Loop      |
    |                                                  |
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

**Time:** 30-45 minutes (includes initial research)

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

### Step 3: Conduct Initial Research

Research the problem space and document findings in DISCOVERY.md:

**Research activities:**
- Read code/files mentioned in epic request
- Examine existing patterns that could be leveraged
- Identify components affected by the epic
- Note what exists vs what's missing
- Identify solution approaches

**Document findings in DISCOVERY.md sections:**
- Technical Analysis
- Key Findings
- Solution Options (if multiple approaches exist)

### Step 4: Extract Initial Questions

Based on initial research, identify questions that need user input:

**Question sources:**
- Ambiguous language ("easier", "better", "improved")
- Undefined terms ("debugging version run")
- Implicit assumptions that need verification
- Scope boundaries that are unclear
- Multiple valid approaches (need user preference)

**Document in DISCOVERY.md:**
```markdown
### Pending Questions

| # | Question | Context | Asked |
|---|----------|---------|-------|
| 1 | What does "debugging version run" mean? | Term undefined in request | 2025-01-20 |
| 2 | Should all scripts share the same debug approach? | 6 different scripts mentioned | 2025-01-20 |
```

**Ask user questions before proceeding to Validation Loop**

### Step 5: Set Time-Box

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
| 2025-01-20 10:30 | Initial research complete | Documented findings, identified 3 questions |
| 2025-01-20 10:45 | User answered questions | Clarified approach, ready for validation |
```

### Step 6: Update Agent Status

```markdown
## Agent Status

**Current Phase:** DISCOVERY_PHASE
**Current Step:** S1.P3.1 Complete - Initial Research and DISCOVERY.md Draft
**Current Guide:** stages/s1/s1_p3_discovery_phase.md
**Progress:** DISCOVERY.md drafted, entering Validation Loop validation
**Next Action:** S1.P3.2 - Validation Loop Round 1
```

---

## S1.P3.2: Validation Loop Validation

**Time:** Varies by epic size (bulk of Discovery time)

**Reference:** `reference/validation_loop_discovery.md`

The Validation Loop repeats until THREE CONSECUTIVE validation rounds find ZERO issues or gaps in DISCOVERY.md.

**Clean Round Counter:** Track consecutive rounds with zero issues/gaps
- Counter starts at 0
- Increments when round finds NO issues/gaps
- Resets to 0 when round finds ANY issues/gaps
- Loop exits when counter reaches 3

**Issues/Gaps Include:**
- Missing research or incomplete analysis
- Incomplete sections in DISCOVERY.md
- Unanswered questions or unresolved unknowns
- Unverified assumptions
- Integration gaps or unclear dependencies
- Unclear scope (in/out/deferred not defined)

### Round Structure

Each validation round follows this pattern:

```text
A. Re-read DISCOVERY.md (FRESH PERSPECTIVE each round)
       |
       v
B. Identify Issues/Gaps (check completeness, consistency, clarity)
       |
       v
C. Fix ALL Issues Immediately (zero tolerance for deferred issues)
   - Research missing information
   - Ask user questions if needed
   - Update DISCOVERY.md sections
   - Verify assumptions
   - Clarify scope
       |
       v
D. Check Exit (update clean round counter, check if counter >= 3)
```

---

### Step A: Re-read DISCOVERY.md with Fresh Perspective

**CRITICAL: Re-read DISCOVERY.md Completely Each Round**

Each round, you MUST re-read the ENTIRE DISCOVERY.md document. Use different reading patterns:

**Round-Specific Reading Patterns (from validation_loop_discovery.md):**
- **Round 1:** Sequential read (top to bottom), completeness check
- **Round 2:** Reverse order read (bottom to top), consistency check
- **Round 3:** Random section spot-checks, final validation
- **Round 4+:** Thematic clustering (group related sections), cross-reference validation

**Why this matters:** First-pass reading misses 40%+ of important details. Fresh perspective catches what memory-based work misses.

---

### Step B: Identify Issues/Gaps

**Check DISCOVERY.md for these issue categories:**

1. **Missing Research**
   - Incomplete code examination
   - External dependencies not researched
   - Existing patterns not identified
   - Solution approaches not explored

2. **Incomplete Sections**
   - Empty or stub sections in DISCOVERY.md
   - Vague descriptions ("TBD", "will add later")
   - Missing required sections from template

3. **Unanswered Questions**
   - Pending questions not resolved
   - Ambiguous language not clarified
   - Scope boundaries unclear

4. **Unverified Assumptions**
   - Assumptions not checked with user
   - "Probably" or "likely" statements
   - Guesses without verification

5. **Integration Gaps**
   - Unclear how features interact
   - Missing dependency analysis
   - Unclear integration points

6. **Unclear Scope**
   - In/out/deferred not defined
   - Boundaries not documented
   - Feature breakdown rationale missing

**Document all issues found:**
```markdown
## Round {N} Issues Found ({YYYY-MM-DD HH:MM})

### Issue 1: Missing External Dependencies Research
**Category:** Missing Research
**Description:** Section 3 mentions "API integration" but doesn't specify which API or research alternatives
**Action Required:** Research ESPN API, Sleeper API, compare options, ask user preference

### Issue 2: Unverified Assumption
**Category:** Unverified Assumption
**Description:** States "users probably want offline mode" without verification
**Action Required:** Ask user if offline mode is required

[Continue for all issues...]
```

---

### Step C: Fix ALL Issues Immediately

**CRITICAL: Zero Tolerance for Deferred Issues**

For EACH issue identified in Step B, you MUST fix it BEFORE continuing to Step D.

**Fixing strategies by issue type:**

1. **Missing Research** → Research now, document findings
   - Use Grep/Glob to find files
   - Use Read to examine code
   - Document in DISCOVERY.md Technical Analysis

2. **Incomplete Sections** → Complete sections now
   - Fill in TBD markers
   - Add specific details
   - Remove vague placeholders

3. **Unanswered Questions** → Ask user now, record answers
   - Present questions to user
   - Wait for answers
   - Update DISCOVERY.md with answers

4. **Unverified Assumptions** → Verify now
   - Ask user to confirm/reject assumption
   - Replace "probably" with confirmed answer
   - Document verification in Resolved Questions

5. **Integration Gaps** → Analyze now
   - Identify integration points
   - Document dependencies
   - Clarify data flow

6. **Unclear Scope** → Define now
   - Explicitly list in/out/deferred
   - Document rationale for boundaries
   - Get user confirmation if needed

**Update DISCOVERY.md with fixes:**
```markdown
## Round {N} Fixes Applied

### Fix 1: External Dependencies Researched
**Issue:** Missing API research
**Resolution:** Researched ESPN API (free, reliable) and Sleeper API (better data). Asked user, user prefers ESPN API.
**Updated Section:** Technical Analysis - External Dependencies

### Fix 2: Verified Offline Requirement
**Issue:** Unverified offline assumption
**Resolution:** Asked user, confirmed offline mode NOT required (API calls acceptable)
**Updated Section:** Resolved Questions #5

[Continue for all fixes...]
```

---

### Step D: Check Exit Condition

**Update Clean Round Counter:**

1. **Check this round:** Were ANY issues/gaps found in Step B?
   - **YES (issues found):** Counter = 0 (reset after fixing all), continue loop
   - **NO (zero issues):** Counter++ (increment), check counter value

2. **Check counter value:**
   - **Counter = 1:** First clean round, continue loop with fresh perspective
   - **Counter = 2:** Second clean round, continue loop with fresh perspective
   - **Counter = 3:** Third clean round, proceed to exit verification

3. **If counter = 3, verify exit readiness:**
   ```markdown
   ## Validation Loop Exit Verification (After 3 Clean Rounds)

   [ ] 3 consecutive rounds found zero issues/gaps
   [ ] All sections of DISCOVERY.md complete
   [ ] All pending questions resolved
   [ ] All assumptions verified
   [ ] Scope clearly defined (in/out/deferred documented)
   [ ] Solution approach identified with rationale
   [ ] Feature breakdown ready with Discovery basis

   If any unchecked --> Reset counter to 0, continue loop
   If all checked --> Proceed to S1.P3.3 Synthesis
   ```

**Document round in DISCOVERY.md:**
```markdown
## Validation Loop Round {N} ({YYYY-MM-DD HH:MM})

**Reading Pattern:** {Sequential | Reverse | Random spot-check | Thematic clustering}
**Issues Found:** {Number}
**Clean Round Counter:** {0, 1, 2, or 3}

[Issues and fixes documented above...]
```

**Why 3 consecutive clean rounds:**
- Round 1 (clean): Might have missed subtle gaps
- Round 2 (clean): Might have missed consistency issues
- Round 3 (clean): High confidence - document is complete

**Continue loop (counter < 3) if:**
- ANY issues/gaps found (reset counter after fixing)
- Counter = 1 or 2 (need more clean rounds)
- Exit verification checklist has unchecked items

**Exit loop (counter = 3) when:**
- 3 consecutive rounds found ZERO issues/gaps
- Exit verification checklist all checked
- DISCOVERY.md is complete and validated

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

```json
[ ] DISCOVERY.md created with all sections populated
[ ] Validation Loop exited (3 consecutive rounds found zero issues/gaps)
[ ] Clean round counter reached 3
[ ] All pending questions resolved
[ ] All assumptions verified
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

```text
+------------------------------------------------------------+
| "If You're Thinking This, STOP" - Anti-Pattern Detection   |
+------------------------------------------------------------+

X "This epic seems clear, I'll skip Discovery"
  --> STOP - Discovery is MANDATORY for every epic

X "I'll defer these issues and fix them later"
  --> STOP - Validation Loop has ZERO TOLERANCE for deferred issues

X "I know the answer, don't need to ask user"
  --> STOP - User answers all scope/preference/assumption questions

X "I'll create feature folders now and update Discovery later"
  --> STOP - Feature folders created AFTER Discovery approval

X "No issues found, but I haven't checked assumptions"
  --> STOP - Assumptions count as issues until verified

X "User approved, but I want to add one more feature"
  --> STOP - Feature breakdown is what user approved

X "I'll update DISCOVERY.md later with fixes"
  --> STOP - Fix ALL issues immediately in current round

X "One clean round with no issues, I'm done with Discovery"
  --> STOP - Need 3 CONSECUTIVE clean rounds, not just one

X "I've re-read DISCOVERY.md before, I'll skip re-reading"
  --> STOP - MUST re-read completely with fresh perspective each round

X "Counter is at 2, close enough to 3"
  --> STOP - Must reach exactly 3, no rounding

X "This section is 'good enough', I'll mark it complete"
  --> STOP - Good enough = incomplete = issue found = counter reset

X "I found 5 issues, I'll fix 3 now and 2 later"
  --> STOP - Fix ALL issues before proceeding (zero deferred issues)
```

---

## Re-Reading Checkpoints

## 🛑 MANDATORY CHECKPOINT 1

**You have completed S1.P3.1 (Initialize)**

⚠️ STOP - DO NOT PROCEED TO S1.P3.2 YET

**REQUIRED ACTIONS:**
1. [ ] Use Read tool to re-read "Critical Rules" section of this guide
2. [ ] Use Read tool to re-read `reference/validation_loop_discovery.md` (context variant)
3. [ ] Verify DISCOVERY.md created with initial research documented
4. [ ] Verify initial questions asked and answered by user
5. [ ] Verify time-box set based on epic size (SMALL: 1-2hrs, MEDIUM: 2-3hrs, LARGE: 3-4hrs)
6. [ ] Update EPIC_README.md Agent Status:
   - Current Step: "S1.P3.1 complete, starting S1.P3.2 Validation Loop Round 1"
   - Last Updated: [timestamp]
7. [ ] Output acknowledgment: "✅ CHECKPOINT 1 COMPLETE: Re-read Critical Rules and validation_loop_discovery.md, verified DISCOVERY.md drafted"

**Why this checkpoint exists:**
- Critical Rules define Validation Loop exit condition (3 consecutive clean rounds)
- validation_loop_discovery.md defines reading patterns and issue categories
- 80% of agents forget to re-read with fresh perspective each round
- 30 seconds now prevents hours of wasted validation rounds

**ONLY after completing ALL 7 actions above, proceed to S1.P3.2 (Validation Loop)**

---

## 🛑 MANDATORY CHECKPOINT 2

**You have completed one Validation Loop round**

⚠️ STOP - DO NOT PROCEED TO NEXT ROUND YET

**REQUIRED ACTIONS:**
1. [ ] Use Read tool to re-read "Validation Loop Validation" section of this guide
2. [ ] Verify all issues/gaps documented in DISCOVERY.md
3. [ ] Verify ALL issues/gaps fixed (not deferred) - zero tolerance policy
4. [ ] Update clean round counter:
   - Issues/gaps found? → Counter = 0 (reset after fixing all)
   - Zero issues/gaps? → Counter++
5. [ ] Check counter value: Counter < 3 = continue loop, Counter = 3 = verify exit readiness
6. [ ] Update EPIC_README.md Agent Status:
   - Current Step: "S1.P3.2 Round N complete, clean counter = {X}, [continuing loop OR proceeding to S1.P3.3]"
   - Last Updated: [timestamp]
7. [ ] Output acknowledgment: "✅ CHECKPOINT 2 COMPLETE: Re-read Validation Loop section, verified all issues fixed, counter = {X}"

**Why this checkpoint exists:**
- Validation Loop requires 3 CONSECUTIVE clean rounds
- 75% of agents exit after first clean round (premature)
- 60% of agents defer issues instead of fixing immediately
- Premature exit or deferred issues cause incomplete discovery and rework in S2

**ONLY after completing ALL 7 actions above, proceed to next round OR S1.P3.3**

---

## 🛑 MANDATORY CHECKPOINT 3

**You are about to request User Approval (S1.P3.4)**

⚠️ STOP - DO NOT PROCEED TO S1.P3.4 YET

**REQUIRED ACTIONS:**
1. [ ] Use Read tool to re-read "Synthesize Findings" section of this guide
2. [ ] Verify Validation Loop exited cleanly (counter = 3, zero issues in last 3 rounds)
3. [ ] Verify all sections of DISCOVERY.md complete:
   - [ ] Executive Summary
   - [ ] Key Findings
   - [ ] Technical Analysis
   - [ ] Solution Options with comparison
   - [ ] Recommended Approach with rationale
   - [ ] Scope Definition (in/out/deferred)
   - [ ] Recommended Feature Breakdown
   - [ ] All Open Questions resolved
4. [ ] Verify feature breakdown has Discovery basis for each feature
5. [ ] Update EPIC_README.md Agent Status:
   - Current Step: "S1.P3.3 complete, requesting user approval in S1.P3.4"
   - Last Updated: [timestamp]
6. [ ] Output acknowledgment: "✅ CHECKPOINT 3 COMPLETE: Re-read Synthesize section, verified Validation Loop exited cleanly, DISCOVERY.md complete"

**Why this checkpoint exists:**
- DISCOVERY.md must be complete before user approval
- Validation Loop must exit cleanly (not prematurely)
- 90% of agents miss at least one required section
- Incomplete DISCOVERY causes user confusion and delays approval

**ONLY after completing ALL 6 actions above, proceed to S1.P3.4 (User Approval)**

---

---

## Exit Criteria

**S1.P3 (Discovery Phase) is complete when ALL of these are true:**

- [ ] Validation Loop validation complete (3 consecutive clean rounds with zero issues/gaps)
- [ ] DISCOVERY.md created and complete with all required sections:
  - [ ] Executive Summary
  - [ ] Key Findings
  - [ ] Technical Analysis
  - [ ] Solution Options with comparison
  - [ ] Recommended Approach with rationale
  - [ ] Scope Definition (in/out/deferred)
  - [ ] Recommended Feature Breakdown (with Discovery basis for each feature)
  - [ ] All Open Questions resolved
- [ ] User has approved DISCOVERY.md (S1.P3.4)
- [ ] User has approved recommended approach
- [ ] Feature breakdown drafted and ready to present
- [ ] EPIC_README.md updated with Discovery completion
- [ ] Ready to proceed to S1 Step 4 (Feature Breakdown Proposal)

**If any criterion unchecked:** Do NOT proceed to S1 Step 4

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
