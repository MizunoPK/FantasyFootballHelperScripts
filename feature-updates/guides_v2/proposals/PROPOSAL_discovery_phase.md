# Proposal: Mandatory Discovery Phase for S1 Epic Planning

**Proposal ID:** PROP-001
**Status:** DRAFT
**Created:** 2025-01-20
**Author:** Agent (with user input)

---

## Executive Summary

This proposal introduces a mandatory **Discovery Phase** to S1 Epic Planning. The Discovery Phase is an iterative research loop where the agent explores the problem space, asks clarifying questions, and refines understanding before proposing feature breakdown.

**Key Changes:**
- Add mandatory Discovery Phase (S1.P3) between Epic Analysis and Feature Breakdown
- Create DISCOVERY.md as epic-level source of truth for decisions
- Modify S2.P1 to reference Discovery instead of re-interpreting epic notes
- Feature specs reference Discovery for shared context

---

## Problem Statement

### Current Workflow Gap

The current S1 Epic Planning assumes:
1. Epic requests are clear enough to break into features immediately
2. The agent can correctly interpret user intent from raw notes
3. Solution approach is obvious or can be quickly determined

**This fails for vague epics like:**
```
I want to make it easier to do test runs of each script
There should be a way to automate a test that for example runs a single simulation and creates log files
Make it easier to quickly smoke test and allow an agent to test by themselves
I want to be able to have a debugging version run of:
- Every mode in the League helper
- Player data fetcher
- Win Rate Sim
- Accuracy Sim
- Historical Data fetcher
- Schedule Data Fetcher
```

**Problems with current approach:**
- "Make it easier" is vague - no clear solution approach
- "Debugging version run" is undefined
- Multiple possible solutions exist (CLI flags, config files, test harness)
- Agent may misinterpret intent without clarification
- Feature breakdown may be wrong if solution approach is unclear

### Why Agent Assessment Doesn't Work

Initially considered: Agent assesses epic clarity and triggers Discovery only when needed.

**Rejected because:**
- Agent judgment about "vague vs clear" is unreliable
- Even seemingly clear epics benefit from exploration
- Inconsistent process across epics
- User doesn't trust agent to make this call correctly

---

## Proposed Solution: Mandatory Discovery Phase

### Overview

The Discovery Phase is an **iterative research loop** that occurs for **every epic**, where the agent:

1. Reads code and documentation
2. Documents findings in a working document (DISCOVERY.md)
3. Identifies questions and unknowns
4. Asks user questions
5. Updates document with answers
6. Continues research based on new understanding
7. Repeats until no questions remain
8. Synthesizes findings into feature breakdown recommendation

### Key Principles

1. **Mandatory** - Every epic goes through Discovery, no exceptions
2. **Iterative** - Research → Questions → Answers → Update → Repeat
3. **Time-boxed** - Limited by epic size (1-4 hours)
4. **User-collaborative** - User answers questions throughout
5. **Document-driven** - DISCOVERY.md captures all findings and decisions
6. **Foundation for features** - Discovery informs feature breakdown

---

## Detailed Design

### S1 Workflow with Discovery Phase

```
S1 Epic Planning (Revised):

  Step 1: Initial Setup
    - Create git branch
    - Create epic folder
    - Move epic request file
    - Create EPIC_README.md

  Step 2: Epic Analysis
    - Read epic request thoroughly
    - Identify goals, constraints, requirements
    - Estimate rough scope (SMALL/MEDIUM/LARGE)

  Step 3: Discovery Phase (NEW - MANDATORY)
    - S1.P3.1: Initialize discovery document
    - S1.P3.2: Discovery Loop (iterative)
        Research → Questions → User Answers → Update → Repeat
    - S1.P3.3: Synthesize findings
    - S1.P3.4: User approval of recommended approach

  Step 4: Feature Breakdown Proposal
    - Propose features based on Discovery findings
    - User approves breakdown
    - Create epic ticket

  Step 5: Epic Structure Creation
    - Create feature folders
    - Seed spec.md with Discovery Context
    - Create epic-level files

  Step 6: Transition to S2
```

### Time-Box by Epic Size

| Epic Size | Discovery Time-Box | Typical Iterations |
|-----------|-------------------|-------------------|
| SMALL (1-2 features) | 1-2 hours | 2-3 iterations |
| MEDIUM (3-5 features) | 2-3 hours | 3-5 iterations |
| LARGE (6+ features) | 3-4 hours | 5-7 iterations |

---

### Discovery Phase Steps

#### S1.P3.1: Initialize Discovery Document (10-15 min)

Create `DISCOVERY.md` in epic folder with initial structure:

```markdown
# Discovery Phase: {Epic Name}

## Epic Request Summary
{Brief summary of what user requested}

## Discovery Questions
{Questions to investigate - populated during research}

## Research Findings
{Findings documented during research iterations}

## User Answers
{Answers from user, with timestamps}

## Solution Options
{Potential approaches identified during research}

## Recommended Approach
{Filled in during synthesis}

## Proposed Feature Breakdown
{Filled in during synthesis}

---

## Discovery Log
{Chronological log of iterations}
```

#### S1.P3.2: Discovery Loop (Iterative)

```
┌─────────────────────────────────────────┐
│           DISCOVERY LOOP                │
│                                         │
│  ┌─────────────┐                        │
│  │  Research   │ Read code, docs        │
│  └──────┬──────┘                        │
│         │                               │
│         ▼                               │
│  ┌─────────────┐                        │
│  │  Document   │ Update DISCOVERY.md    │
│  └──────┬──────┘                        │
│         │                               │
│         ▼                               │
│  ┌─────────────┐     No questions       │
│  │  Questions? │────────────────────────┼──► Exit Loop
│  └──────┬──────┘                        │
│         │ Has questions                 │
│         ▼                               │
│  ┌─────────────┐                        │
│  │  Ask User   │ Present questions      │
│  └──────┬──────┘                        │
│         │                               │
│         ▼                               │
│  ┌─────────────┐                        │
│  │  Record     │ Update with answers    │
│  └──────┬──────┘                        │
│         │                               │
│         └───────────────────────────────┘
│                    Loop back
└─────────────────────────────────────────┘
```

**Research Activities:**
- Read components/scripts/modules mentioned in epic
- Examine existing patterns that could be leveraged
- Document current behavior and interfaces
- Identify what exists vs what's missing

**Question Types:**
1. **Clarification** - Epic language is ambiguous
2. **Scope** - Boundaries unclear
3. **Preference** - Multiple valid approaches exist
4. **Priority** - Trade-offs need user input
5. **Constraint** - Technical/practical limits

**Exit Conditions:**
- No new questions identified
- Scope is well-defined
- Solution approach is clear
- Ready to propose feature breakdown

#### S1.P3.3: Synthesize Findings (20-30 min)

Compile research into actionable recommendations:

- Solution options comparison
- Recommended approach with rationale
- Scope definition (in/out/deferred)
- Proposed feature breakdown

#### S1.P3.4: User Approval

Present Discovery summary to user:
- Key findings
- Recommended approach
- Proposed scope
- Proposed feature breakdown

**User must approve before proceeding to Step 4.**

---

### DISCOVERY.md as Epic-Level Source of Truth

#### Content Ownership

| Content Type | Location | Rationale |
|-------------|----------|-----------|
| Epic problem statement | DISCOVERY.md | Shared understanding |
| Solution approach decision | DISCOVERY.md | Affects all features |
| User answers (scope, priorities) | DISCOVERY.md | Epic-level decisions |
| Scope boundaries (in/out/deferred) | DISCOVERY.md | Epic-level |
| Feature breakdown rationale | DISCOVERY.md | Why these features |
| Feature-specific requirements | spec.md | Feature-specific |
| Feature implementation details | spec.md | Feature-specific |
| Feature acceptance criteria | spec.md | Feature-specific |

#### Traceability Chain

```
epic_notes.txt (raw user request)
       │
       ▼ Interpreted through Discovery Loop
DISCOVERY.md (refined understanding, user-approved)
       │
       ▼ Relevant sections copied to each feature
spec.md (feature-specific, references Discovery)
       │
       ▼ Implementation details added in S5
implementation_plan.md (how to build)
```

---

### Feature Spec Interaction with Discovery

#### Spec.md Structure (Revised)

```markdown
# Feature Spec: {feature_name}

## Discovery Context

**Discovery Document:** `../DISCOVERY.md`

### This Feature's Scope (from Discovery)
{Copy of this feature's scope from DISCOVERY.md Proposed Feature Breakdown}

### Relevant Discovery Decisions
- **Solution Approach:** {Brief summary of approach from Discovery}
- **Key Constraints:** {Constraints that affect this feature}
- **Dependencies:** {What this feature depends on / what depends on it}

### Relevant User Answers (from Discovery)
| Question | Answer | Impact on This Feature |
|----------|--------|----------------------|
| {Q from Discovery} | {A} | {How it affects this feature} |

---

## Feature Requirements

### Requirement 1: {Name}
**Source:** Discovery Decision / User Answer / Feature-Specific
{Requirement details}

...

## Acceptance Criteria
...

## Edge Cases
...
```

#### S1 Step 5: Seed Specs with Discovery Context

When creating feature folders, each spec.md starts with Discovery Context already populated:

```markdown
# Feature Spec: {feature_name}

## Discovery Context

**Discovery Document:** `../DISCOVERY.md`

### This Feature's Scope (from Discovery)
{Copied from DISCOVERY.md Feature Breakdown section}

### Relevant Discovery Decisions
{Copied from DISCOVERY.md - decisions affecting this feature}

### Relevant User Answers
{Copied from DISCOVERY.md - answers affecting this feature}

---

## Feature Requirements
{To be completed in S2}

## Acceptance Criteria
{To be completed in S2}
```

---

### S2.P1 Changes

#### Current S2.P1 (without Discovery)

- Phase 0: Epic Intent Extraction (re-read epic notes, extract quotes)
- Phase 1: Targeted Research (investigate codebase)
- Phase 1.5: Research Completeness Audit

#### Revised S2.P1 (with Discovery)

- Phase 0: Review Discovery Context (read DISCOVERY.md, verify spec has context)
- Phase 1: Feature-Specific Research (deeper dive on this feature's implementation)
- Phase 1.5: Research Completeness Audit (verify feature-level understanding)

**Key Change:** Epic-level understanding comes from DISCOVERY.md (already user-approved). S2 research focuses on feature implementation details, not re-interpreting the overall problem.

#### Phase 0 Comparison

| Aspect | Current Phase 0 | Revised Phase 0 |
|--------|-----------------|-----------------|
| **Input** | Raw epic notes | DISCOVERY.md |
| **Action** | Extract quotes, interpret intent | Review existing context |
| **Output** | Epic Intent section | Verified Discovery Context |
| **Risk** | Different interpretation | Consistent with Discovery |
| **Time** | 15-20 min | 5-10 min |

---

### File Structure

```
feature-updates/KAI-{N}-{epic_name}/
├── {epic_name}_notes.txt           # Original user request (immutable)
├── DISCOVERY.md                     # Refined understanding (epic-level)
├── EPIC_README.md
├── EPIC_TICKET.md
├── epic_smoke_test_plan.md
├── research/                        # Research files from Discovery
│   └── {topic}_findings.md
├── feature_01_{name}/
│   ├── README.md
│   ├── spec.md                      # References DISCOVERY.md
│   ├── checklist.md
│   └── ...
├── feature_02_{name}/
│   ├── spec.md                      # References DISCOVERY.md
│   └── ...
└── ...
```

### DISCOVERY.md Lifecycle

| Stage | DISCOVERY.md Status |
|-------|-------------------|
| S1.P3 | Created and iterated through Discovery Loop |
| S1.P3.4 | User-approved, becomes epic-level reference |
| S2-S4 | Referenced by all feature specs |
| S5-S8 | Referenced during implementation |
| S8.P1 | May be updated if epic understanding changes (rare, needs user approval) |
| S9-S10 | Final reference for epic review |
| After S10 | Archived with epic in done/ |

---

## Example: improve_debugging_runs Epic

### S1.P3.1: Initialize

```markdown
# Discovery Phase: improve_debugging_runs

## Epic Request Summary
User wants easier test runs for scripts, automated smoke testing,
and "debugging version runs" for league helper modes, simulations,
and data fetchers.

## Discovery Questions
- What does "easier" mean?
- What is a "debugging version run"?
- What are current pain points?
```

### S1.P3.2: Discovery Loop

**Iteration 1:**

*Research:*
- Read `run_league_helper.py` - uses argparse, 4 modes
- Read `run_simulation.py` - has iteration count parameter
- Found existing `--verbose` flag in some scripts

*Questions to User:*
```
Q1: What does "debugging version run" mean to you?
- Fewer iterations?
- Mock/sample data?
- More verbose output?
- All of the above?

Q2: For league helper's 4 modes, do all need debug support
or just specific ones?
```

*User Answers:*
```
A1: Fewer iterations and more verbose output. Mock data would
    be nice but not required for first version.
A2: All 4 modes should have it.
```

**Iteration 2:**

*Research:*
- Examined iteration parameters in simulation scripts
- Found logging configuration in utils/
- Checked data loading patterns

*Questions to User:*
```
Q3: Should debug mode be activated via:
- CLI flag (--debug)
- Environment variable (DEBUG=1)
- Config file setting

Q4: For "fewer iterations" - what's a good debug number?
- 1 iteration (fastest)
- 9 iterations (some statistical validity)
- User-configurable
```

*User Answers:*
```
A3: CLI flag preferred, but config file override would be nice too
A4: 1 iteration for speed, but configurable would be ideal
```

**Iteration 3:**

*Research:*
- Examined config loading patterns
- Found shared_config.py exists
- Verified all scripts can access shared config

*Questions to User:*
```
Q5: Should all scripts share the same debug config, or each
    have independent settings?
```

*User Answer:*
```
A5: Shared config with ability to override per-script if needed
```

**Exit Check:** No more questions - scope clear, approach determined.

### S1.P3.3: Synthesis

```markdown
## Recommended Approach

Add `--debug` CLI flag to each script that:
- Reduces iterations to 1 (configurable via shared config)
- Enables verbose logging
- Reads from shared debug configuration

Shared debug configuration in `shared_config.py` with per-script
override capability.

## Scope Definition

**In Scope:**
- --debug flag for all 6 script types
- Shared debug config
- Reduced iterations
- Verbose logging

**Out of Scope:**
- Mock data (deferred to future)
- GUI/interactive debug mode
- Automated test framework

**Deferred:**
- Mock data support (nice-to-have, future epic)

## Proposed Feature Breakdown

### Feature 1: debug_infrastructure
Shared debug config, verbose logging setup, base debug utilities

### Feature 2: league_helper_debug
Debug mode for all 4 league helper modes

### Feature 3: simulation_debug
Debug mode for win rate and accuracy simulations

### Feature 4: fetcher_debug
Debug mode for player, scores, historical, and schedule fetchers
```

### S1.P3.4: User Approval

User approves Discovery findings and feature breakdown.

### Resulting Feature Specs

Each feature's spec.md starts with:

```markdown
# Feature Spec: debug_infrastructure

## Discovery Context

**Discovery Document:** `../DISCOVERY.md`

### This Feature's Scope (from Discovery)
Shared debug config, verbose logging setup, base debug utilities

### Relevant Discovery Decisions
- **Solution Approach:** CLI --debug flag + shared config
- **Key Constraints:** Must work with existing argparse patterns
- **Dependencies:** None (foundation feature)

### Relevant User Answers (from Discovery)
| Question | Answer | Impact |
|----------|--------|--------|
| Debug activation method | CLI flag + config override | Need both mechanisms |
| Iteration count | 1 default, configurable | Config must support this |
| Shared vs independent | Shared with per-script override | Design config hierarchy |

---

## Feature Requirements
{To be completed in S2}
```

---

## Impact Assessment

### Benefits

1. **Consistent Process** - Every epic gets thorough exploration
2. **User Collaboration** - Questions answered before feature breakdown
3. **Better Feature Breakdown** - Informed by research, not guessed
4. **Reduced Rework** - Misunderstandings caught early
5. **Clear Traceability** - Decisions documented with rationale
6. **Single Source of Truth** - DISCOVERY.md for epic-level decisions

### Costs

1. **Added Time** - 1-4 hours per epic for Discovery Phase
2. **More Files** - DISCOVERY.md added to epic structure
3. **Guide Updates** - Multiple guides need modification
4. **Learning Curve** - Agents need to learn new phase

### Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Discovery takes too long | Time-box by epic size |
| Too many questions overwhelm user | Batch related questions, limit per iteration |
| Discovery findings change during S2 | Update DISCOVERY.md with user approval |
| Agent skips Discovery | Mandatory phase, cannot proceed without |

---

## Implementation Plan

### New Files to Create

| File | Purpose |
|------|---------|
| `stages/s1/s1_p3_discovery_phase.md` | Main Discovery Phase guide |
| `reference/stage_1/discovery_examples.md` | Example Discovery sessions |
| `templates/discovery_template.md` | DISCOVERY.md template |

### Files to Modify

| File | Changes |
|------|---------|
| `stages/s1/s1_epic_planning.md` | Add Step 3 Discovery Phase, update Steps 4-6 numbering |
| `stages/s2/s2_p1_research.md` | Change Phase 0 from Epic Intent to Discovery Context Review |
| `prompts_reference_v2.md` | Add Discovery Phase prompts |
| `reference/glossary.md` | Add Discovery terminology |
| `templates/feature_spec_template.md` | Add Discovery Context section |
| `templates/epic_readme_template.md` | Add Discovery status tracking |
| `CLAUDE.md` (project root) | Update S1 workflow overview |

### Implementation Order

1. Create DISCOVERY.md template
2. Create Discovery Phase guide (s1_p3_discovery_phase.md)
3. Update S1 Epic Planning guide
4. Update feature spec template
5. Update S2.P1 Research guide
6. Add prompts to prompts_reference_v2.md
7. Update glossary
8. Update CLAUDE.md overview
9. Create example Discovery sessions

---

## Open Questions (RESOLVED)

1. **Parallel Discovery:** If parallel S2 work is enabled, should Discovery always complete before parallelization begins?
   - **Answer:** Yes - Discovery must always complete before creation of any features. Feature folders are not created until Discovery is complete and approved.

2. **Discovery Updates:** How formal should the process be for updating DISCOVERY.md after S1?
   - **Answer:** DISCOVERY.md stays unchanged after Discovery phase ends, UNLESS something is found to be incorrect or outdated during later stages. In that case, update the doc to reflect the change in requirements or understanding. No formal approval process required for corrections.

3. **Minimum Iterations:** Should there be a minimum number of Discovery iterations?
   - **Answer:** No minimum required. Keep looping until a research round brings up no new questions. Exit condition is purely based on whether new questions emerge.

---

## Approval

**APPROVED** - 2025-01-20

- [x] User approves overall approach
- [x] User approves S1 workflow changes
- [x] User approves DISCOVERY.md as source of truth
- [x] User approves S2.P1 changes
- [x] User approves implementation plan
- [x] Open questions resolved

---

## Revision History

| Date | Version | Changes |
|------|---------|---------|
| 2025-01-20 | 0.1 | Initial draft |

---

*End of Proposal*
