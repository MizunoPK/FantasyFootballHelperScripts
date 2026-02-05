# S2: Feature Deep Dives
## S2.P1: Research Phase

**Guide Version:** 1.0
**Created:** 2026-01-02
**Prerequisites:** S1 complete, feature folder exists
**Next Phase:** `stages/s2/s2_p2_specification.md`
**Detailed Examples:** `reference/stage_2/research_examples.md`
**File:** `s2_p1_research.md`

---

**📚 Companion Reference:** This guide focuses on workflow steps. For detailed examples, templates, and anti-patterns, see `reference/stage_2/research_examples.md`

---

## Table of Contents

1. [🚨 MANDATORY READING PROTOCOL](#-mandatory-reading-protocol)
2. [Overview](#overview)
3. [Critical Rules](#critical-rules)
4. [Critical Decisions Summary](#critical-decisions-summary)
5. [Prerequisites Checklist](#prerequisites-checklist)
6. [🔄 Parallel Work Coordination (If Applicable)](#-parallel-work-coordination-if-applicable)
7. [Step 0: Discovery Context Review (MANDATORY FIRST STEP)](#step-0-discovery-context-review-mandatory-first-step)
8. [Discovery Context](#discovery-context)
9. [Phase 0 Verification Checklist](#phase-0-verification-checklist)
10. [Agent Status](#agent-status)
11. [Phase 1: Feature-Specific Research](#phase-1-feature-specific-research)
12. [External Library Verification](#external-library-verification)
13. [Agent Status](#agent-status-1)
14. [Phase 1.5: Research Completeness Audit (MANDATORY GATE)](#phase-15-research-completeness-audit-mandatory-gate)
15. [Agent Status](#agent-status-2)
16. [Exit Criteria](#exit-criteria)
17. [Next Stage](#next-stage)

---


## 🚨 MANDATORY READING PROTOCOL

**Before starting this guide:**
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

## Overview

**What is this guide?**
Research Phase is the first part of Feature Deep Dive where you review Discovery Context, conduct feature-specific research, and verify research completeness through a mandatory audit before creating specifications.

**When do you use this guide?**
- S1 complete (epic folder structure created, Discovery approved)
- Feature folder exists with spec.md seeded with Discovery Context
- Ready to begin deep dive for this specific feature
- Starting feature-specific research (epic-level research done in Discovery)

**Key Outputs:**
- Discovery Context verified in spec.md (from DISCOVERY.md)
- Feature-specific research complete (deeper dive on this feature's implementation)
- Research findings documented in epic/research/{FEATURE_NAME}_RESEARCH.md
- Phase 1.5 Research Completeness Audit PASSED (MANDATORY GATE)
- Evidence collected (file paths, line numbers, code snippets)
- Ready for S2.P2 (Specification Phase)

**Time Estimate:**
30-45 minutes (2 phases - Phase 0 is now quick review)

**Exit Condition:**
Research Phase is complete when Phase 1.5 audit passes (all 4 categories with evidence), Discovery Context is verified in spec.md, and feature-specific research findings are ready for spec creation.

---

## Critical Rules

```text
+-------------------------------------------------------------+
| CRITICAL RULES - These MUST be copied to README Agent Status |
+-------------------------------------------------------------+

1. ALWAYS start with Phase 0 (Discovery Context Review)
   - Read DISCOVERY.md to understand epic-level context
   - Verify spec.md has Discovery Context section populated
   - Epic-level understanding comes from Discovery (NOT raw epic notes)

2. Research is FEATURE-SPECIFIC (epic-level done in Discovery)
   - Discovery handled epic-level research and questions
   - S2 research focuses on implementation details for THIS feature
   - Go deeper on components relevant to this specific feature

3. READ source code - do NOT guess
   - Use Read tool to view actual code
   - Copy actual method signatures
   - Note actual line numbers
   - View actual data file contents

4. Phase 1.5 audit is MANDATORY GATE
   - Cannot proceed to S2.P2 without PASSING audit
   - All 4 categories must pass (Component, Pattern, Data, Discovery)
   - Evidence required: cite file paths, line numbers, code snippets

5. All research documents go in epic's research/ folder
   - NOT in feature folder
   - Shared across all features
   - Named: {FEATURE_NAME}_RESEARCH.md

6. Update feature README.md Agent Status after EACH phase
```

---

## Critical Decisions Summary

**Research Phase has 1 major decision point:**

### Decision Point 1: Phase 1.5 - Research Completeness Audit (GO/NO-GO)
**Question:** Is research thorough enough to proceed to spec creation?
- **Evidence required:** Can cite exact files, line numbers, method signatures, data structures
- **If NO (cannot cite specifics):**
  - ❌ STOP at Phase 1.5
  - Continue research (re-read code, search for missing components)
  - Do NOT proceed to STAGE_2b until can cite specific evidence
- **If YES (can cite everything with specifics):**
  - ✅ Proceed to STAGE_2b (Specification Phase)
- **Impact:** Guessing instead of knowing causes wrong specs, which leads to complete rework

---

## Prerequisites Checklist

**Verify BEFORE starting Research Phase:**

□ S1 (Epic Planning) complete - verified in epic EPIC_README.md
□ This feature folder exists: `feature_{N}_{name}/`
□ Feature folder contains:
  - README.md (with Agent Status)
  - spec.md (initial scope from S1)
  - checklist.md (empty or with preliminary items)
  - lessons_learned.md (template)
□ Epic EPIC_README.md Feature Tracking table lists this feature
□ No other feature currently in deep dive phase (work on ONE feature at a time)
□ Epic notes file exists: `feature-updates/KAI-{N}-{epic_name}/{epic_name}_notes.txt`
□ Epic research folder exists: `feature-updates/KAI-{N}-{epic_name}/research/`

**If any prerequisite fails:**
- ❌ STOP - Do NOT proceed with research
- Complete missing prerequisites first
- Document blocker in feature README.md Agent Status

---

## 🔄 Parallel Work Coordination (If Applicable)

**Skip this section if you're in sequential mode (only you working on epic)**

**If you're in parallel S2 work mode** (multiple agents, coordination files exist):

### Coordination Heartbeat (Every 15 Minutes)

**Throughout S2.P1, every 15 minutes:**

1. **Update Checkpoint:**
   - File: `agent_checkpoints/{your_agent_id}.json`
   - Update: `last_checkpoint`, `stage`, `current_step`, `files_modified`
   - See: `parallel_work/checkpoint_protocol.md`

2. **Check Inbox:**
   - File: `agent_comms/primary_to_{your_id}.md` (if Secondary)
   - File: `agent_comms/secondary_{x}_to_primary.md` (if Primary, check all)
   - Look for: ⏳ UNREAD messages
   - Process: Read, mark as ✅ READ, take action, reply if needed
   - See: `parallel_work/communication_protocol.md`

3. **Update STATUS:**
   - File: `feature_{N}_{name}/STATUS`
   - Update: `STAGE`, `PHASE`, `UPDATED`, `BLOCKERS`, `NEXT_ACTION`
   - Format: Plain text key-value pairs

4. **Update EPIC_README.md (when progress changes):**
   - Acquire lock: `.epic_locks/epic_readme.lock`
   - Update only your section (between BEGIN/END markers)
   - Release lock
   - See: `parallel_work/lock_file_protocol.md`

5. **Set 15-minute timer** for next heartbeat

### Escalation Protocol

**If blocked >30 minutes:**
- Send escalation message to Primary
- Update STATUS: `BLOCKERS: <description>`
- Update checkpoint: `"blockers": ["description"]`
- See: `parallel_work/s2_parallel_protocol.md` → Escalation Protocol

### Primary-Specific Coordination

**If you're Primary:**
- Check secondary agent inboxes every 15 min
- Respond to escalations within 15 min
- Monitor STATUS files and checkpoints for staleness
- See: `parallel_work/s2_primary_agent_guide.md`

**Coordination overhead target:** <10% of work time
- Heartbeat: ~5 minutes per hour
- Escalations: As needed (respond fast)
- Don't let coordination interrupt deep work flow

**For full parallel work details:** See `parallel_work/s2_parallel_protocol.md`

---

## Step 0: Discovery Context Review (MANDATORY FIRST STEP)

**Goal:** Verify this feature's Discovery Context and understand epic-level decisions before feature-specific research.

**Key Change:** Epic-level understanding now comes from DISCOVERY.md (created and approved in S1.P3), not from re-interpreting raw epic notes. This ensures consistency across all features.

---

### Step 0.1: Read DISCOVERY.md

**Read:** `feature-updates/KAI-{N}-{epic_name}/DISCOVERY.md`

**Focus on:**
- Recommended Approach section
- Scope Definition (in/out/deferred)
- This feature's entry in Proposed Feature Breakdown
- Relevant User Answers that affect this feature

**Why this matters:**
- Discovery captured epic-level understanding with user approval
- All features reference the same source of truth
- Prevents re-interpreting epic differently per feature

---

### Step 0.2: Verify Discovery Context in spec.md

**Check `feature_{N}_{name}/spec.md`:**

Verify the Discovery Context section (created in S1 Step 5) is populated:

```markdown
## Discovery Context

**Discovery Document:** `../DISCOVERY.md`

### This Feature's Scope (from Discovery)
{Should be populated from S1}

### Relevant Discovery Decisions
{Should be populated from S1}

### Relevant User Answers (from Discovery)
{Should be populated from S1}
```

**If Discovery Context is missing or incomplete:**
- Copy relevant sections from DISCOVERY.md
- Ensure scope matches what Discovery defined
- Link user answers that affect this feature

---

### Step 0.3: Extract Feature-Specific Focus

Based on Discovery Context, identify what THIS feature needs to accomplish:

1. What is this feature's specific purpose? (from Discovery)
2. What components does this feature touch? (from Discovery scope)
3. What constraints apply to this feature? (from Discovery decisions)
4. What dependencies does this feature have? (from Discovery)
5. What implementation approach was decided? (from Discovery)

**Note:** These answers come from DISCOVERY.md, not raw epic notes. Discovery already refined the epic understanding.

---

### Step 0.4: Verify Discovery Alignment

**BEFORE proceeding to Phase 1, verify:**

```markdown
## Phase 0 Verification Checklist

[ ] I have read DISCOVERY.md
[ ] I understand the recommended approach from Discovery
[ ] I know this feature's scope from Discovery
[ ] spec.md has Discovery Context section populated
[ ] I can list relevant user answers from Discovery
[ ] I understand how this feature fits in the overall solution
[ ] I know this feature's dependencies from Discovery
```

**If any item unchecked:**
- Do NOT proceed to Phase 1
- Complete this phase first
- Update Agent Status with blocker

**Why this matters:**
- Ensures consistency with epic-level decisions
- Prevents scope creep beyond what Discovery defined
- Provides traceability (requirements trace to Discovery)
- All features work from same understanding

---

### Step 0.5: Update Agent Status

```markdown
## Agent Status

**Last Updated:** {YYYY-MM-DD HH:MM}
**Current Phase:** RESEARCH_PHASE
**Current Step:** Phase 0 - Discovery Context Review Complete
**Current Guide:** stages/s2/s2_p1_research.md
**Guide Last Read:** {YYYY-MM-DD HH:MM}
**Critical Rules from Guide:**
- Start with Discovery Context review (not raw epic notes)
- Epic-level understanding comes from DISCOVERY.md
- Feature research is implementation-focused
- All requirements trace to Discovery

**Progress:** 1/2 phases complete (Discovery Context Review)
**Next Action:** Phase 1 - Feature-Specific Research
**Blockers:** None

**Discovery Reviewed:** {YYYY-MM-DD HH:MM}
**Feature Scope Verified:** Yes
```

---

## Phase 1: Feature-Specific Research

**Goal:** Understand THIS feature's implementation requirements (epic-level understanding from Discovery)

**Key Difference from Discovery:** Discovery explored the problem space. Phase 1 goes deeper on implementation details for this specific feature.

---

### Step 1.1: Review Discovery Context from spec.md

Read `feature_{N}_{name}/spec.md` Discovery Context section.

**Extract:**
- Feature purpose and scope (from Discovery)
- Dependencies (from Discovery)
- Relevant user answers (from Discovery)
- Solution approach (from Discovery)

**Use Discovery Context to guide research:**
- What components does this feature need to modify?
- What interfaces does this feature need to implement?
- What patterns should this feature follow?

---

### Step 1.2: Identify Feature-Specific Research Questions

**Based on Discovery Context, identify what you need to learn for implementation:**

Research questions should be implementation-focused:
- How exactly does component X work? (mentioned in Discovery scope)
- What is the interface for Y? (needed for this feature)
- What patterns does similar feature Z follow? (for consistency)
- What data structures are involved? (for this feature's scope)

**Anti-Pattern Detection:**

X "Let me research the overall epic scope"
  --> STOP - Epic scope is in Discovery, research THIS feature's implementation

X "Let me ask user about priorities"
  --> STOP - Priorities were resolved in Discovery, research implementation details

X "Let me understand the entire codebase architecture"
  --> STOP - Only research components this feature touches

**Key Principle:** Discovery answered "what to build." Phase 1 answers "how to build this specific feature."

---

### Step 1.3: Conduct Targeted Searches

**For EACH item in research checklist, execute searches:**

**Basic search pattern:**
1. Use Grep/Glob to find components
2. Use Read tool to view actual code (NOT just search)
3. Document file paths, line numbers, actual signatures
4. Collect evidence for Phase 1.5 audit

**Detailed search command examples:** See `reference/stage_2/research_examples.md` → Phase 1 Examples (shows grep, find, Read tool sequences)

**CRITICAL RULE: READ, don't guess**

- Use Read tool to view actual code
- Copy actual method signatures
- Note actual line numbers
- View actual data file contents

---

### Step 1.3a: Verify External Library Compatibility (NEW - from KAI-1 lessons)

**Purpose:** Test external libraries with test environment/mock data BEFORE writing spec

**Historical Context (KAI-1 Feature 02):**
- Feature assumed S3Util library would work with LocalStack test environment
- Didn't test during research
- Result: 6/16 tests failed during S7
- Time cost: 2 hours debugging + workaround implementation
- **This step prevents that scenario**

---

**Process:**

**1. Identify External Libraries This Feature Needs:**

Review Discovery Context and research findings:
- What libraries or APIs will this feature use?
- ESPN API, pandas, requests, third-party packages?
- New libraries not currently used?

**Examples:**
- ESPN API (espn_api package) - for player projections
- pandas - for CSV manipulation
- requests - for HTTP calls
- BeautifulSoup - for web scraping

---

**2. For Each External Library, Test Compatibility:**

**Quick compatibility test (15-20 minutes per library):**

```python
# Example: Test ESPN API with mock responses
import espn_api
from unittest.mock import Mock, patch

# Can we mock this library's responses?
with patch('espn_api.League') as mock_league:
    mock_league.return_value = Mock(players=[...])
    # Does library work with mocks?
    # Can we configure endpoints?
```

**Check:**
- [ ] Does library accept endpoint override (for test APIs)?
- [ ] Does library support mock responses?
- [ ] Can library work with test data files?
- [ ] Are there known compatibility issues?

---

**3. Document Findings:**

Add to research notes:

```markdown
## External Library Verification

### Library: ESPN API (espn_api package)
- **Purpose:** Fetch player projections
- **Test Environment:** Mock API responses
- **Compatibility:** ✅ COMPATIBLE
  - Library accepts mocked responses
  - No endpoint override needed (uses League ID)
  - Tested with unittest.mock - works correctly
- **Workaround:** None needed

### Library: custom-java-lib (hypothetical)
- **Purpose:** S3 file uploads
- **Test Environment:** LocalStack
- **Compatibility:** ❌ INCOMPATIBLE
  - Library doesn't support endpoint override
  - Hardcoded to AWS production endpoints
  - Cannot configure for LocalStack
- **Workaround:** Create custom test client using boto3 directly
- **Impact:** Add 2 tasks to spec for test client wrapper
```

---

**4. Update Spec Scope if Workarounds Needed:**

If library incompatible:
- Document workaround approach
- Note additional tasks needed
- Estimate additional time
- May need to ask user if significant scope increase

---

**When to Skip This Step:**

- Feature uses NO external libraries (only internal code)
- Feature uses ONLY well-tested libraries (pandas, requests) with no test environment concerns
- Discovery already identified and resolved external dependency issues

**When This Step is CRITICAL:**

- Feature uses new external API (ESPN, third-party services)
- Feature uses library with endpoint configuration (AWS, cloud services)
- Feature uses library requiring authentication (OAuth, API keys)
- Feature uses library with strict validation (XML parsers, formatters)

**Time Investment:** 15-20 minutes per library
**Time Saved:** 2+ hours of S7 debugging per incompatible library

---

### Step 1.4: Document Findings in Research Folder

Create `epic/research/{FEATURE_NAME}_RESEARCH.md`:

**Required sections:**
- Discovery Context Summary (brief summary from DISCOVERY.md for this feature)
- Components Researched (for each component in feature scope)
  - Discovery scope reference
  - Found in codebase (file paths, line numbers)
  - Actual code signatures and snippets
  - How it works today
  - Implementation approach for this feature
- Existing Test Patterns (test structure to follow)
- Interface Dependencies (classes/methods this feature will call)
- Edge Cases Identified (from reading existing code)
- Research Completeness (checklist of what was researched)

**Complete template with detailed examples:** See `reference/stage_2/research_examples.md` → Phase 1 Examples → Example 2

---

### Step 1.5: Update Agent Status

```markdown
## Agent Status

**Last Updated:** {YYYY-MM-DD HH:MM}
**Current Phase:** RESEARCH_PHASE
**Current Step:** Phase 1 - Targeted Research Complete
**Current Guide:** stages/s2/s2_p1_research.md
**Guide Last Read:** {YYYY-MM-DD HH:MM}
**Critical Rules from Guide:**
- Research grounded in epic intent
- READ source code (not guess)
- Evidence required (file paths, line numbers)

**Progress:** 2/3 phases complete (Targeted Research)
**Next Action:** Phase 1.5 - Research Completeness Audit (MANDATORY GATE)
**Blockers:** None

**Components Researched:** {N}
**Research Document:** epic/research/{FEATURE_NAME}_DISCOVERY.md
```

---

## Phase 1.5: Research Completeness Audit (MANDATORY GATE)

**Goal:** Verify research was thorough enough to avoid "should have known" checklist questions

**⚠️ CRITICAL:** This is a MANDATORY GATE. Cannot proceed to STAGE_2b without passing this audit.

**Why this phase exists:**
- Prevents creating checklist questions about things you could have learned from codebase
- Ensures spec is based on actual code (not assumptions)
- Reduces back-and-forth with user about basic technical details

---

### Step 1.5.1-4: Answer Audit Questions for 4 Categories

**Category 1: Component Knowledge**
- Question 1.1: Can I list EXACT classes/files to modify?
- Question 1.2: Have I READ source code for each component?
- Question 1.3: Can I cite actual method signatures?

**Category 2: Pattern Knowledge**
- Question 2.1: Have I searched for similar existing features?
- Question 2.2: Have I READ at least one similar feature's implementation?
- Question 2.3: Can I describe the existing pattern in detail?

**Category 3: Data Structure Knowledge**
- Question 3.1: Have I READ actual data files (CSV/JSON examples)?
- Question 3.2: Can I describe current format from actual examples?
- Question 3.3: Have I verified field names from source code?

**Category 4: Discovery Context Knowledge**
- Question 4.1: Have I reviewed DISCOVERY.md for this feature?
- Question 4.2: Can I list this feature's scope from Discovery?
- Question 4.3: Do I understand relevant user answers from Discovery?

**For EACH question, provide:**
- Your answer (be specific, cite evidence)
- Evidence (file paths, line numbers, code snippets, timestamps)

**Complete audit template with examples:** See `reference/stage_2/research_examples.md` → Phase 1.5 Examples → Example 1 (PASSING) and Example 2 (FAILED)

---

### Step 1.5.5: Overall Audit Result

**Summarize audit results for all 4 categories:**

[ ] Category 1 (Component Knowledge): PASSED / FAILED
[ ] Category 2 (Pattern Knowledge): PASSED / FAILED
[ ] Category 3 (Data Structure Knowledge): PASSED / FAILED
[ ] Category 4 (Discovery Context Knowledge): PASSED / FAILED

**OVERALL RESULT:**
- PASSED - All 4 categories passed --> Proceed to S2.P2
- FAILED - At least one category failed --> Return to Phase 1

**Evidence Summary:**
- Files Read: {count and list}
- Code Snippets Collected: {count and purposes}
- Epic Notes Citations: {count and line numbers}

**Complete audit summary template:** See `reference/stage_2/research_examples.md` → Phase 1.5 Examples → Example 1

---

### Step 1.5.6: Update Agent Status

```markdown
## Agent Status

**Last Updated:** {YYYY-MM-DD HH:MM}
**Current Phase:** RESEARCH_PHASE
**Current Step:** Phase 1.5 - Research Completeness Audit PASSED
**Current Guide:** stages/s2/s2_p1_research.md
**Guide Last Read:** {YYYY-MM-DD HH:MM}
**Critical Rules from Guide:**
- Phase 1.5 audit is MANDATORY GATE
- Cannot proceed without passing all 4 categories
- Evidence required for all answers

**Progress:** 3/3 phases complete (Research Phase COMPLETE)
**Next Action:** Specification Phase (Update Spec & Checklist with traceability)
**Next Guide:** stages/s2/s2_p2_specification.md
**Blockers:** None

**Audit Result:** ✅ PASSED (all 4 categories)
**Files Read:** {N}
**Code Snippets Collected:** {N}
```

---

## Exit Criteria

**Research Phase (S2.P1) is COMPLETE when ALL of these are true:**

[ ] **Phase 0 Complete:**
  - DISCOVERY.md reviewed
  - Discovery Context section verified in spec.md
  - Feature scope understood from Discovery
  - Relevant user answers identified

[ ] **Phase 1 Complete:**
  - Feature-specific research conducted
  - Research focused on implementation details for this feature
  - Findings documented in epic/research/{FEATURE_NAME}_RESEARCH.md
  - Evidence collected (file paths, line numbers, code snippets)

[ ] **Phase 1.5 Complete:**
  - Research completeness audit PASSED
  - All 4 categories verified (Component, Pattern, Data, Discovery Context)
  - Evidence provided for all audit questions
  - Overall audit result: PASSED

[ ] **Documentation Complete:**
  - spec.md has Discovery Context section populated
  - research/{FEATURE_NAME}_RESEARCH.md created with findings
  - Agent Status updated with S2.P1 completion

[ ] **Ready for Next Stage:**
  - All research evidence collected and documented
  - Clear understanding of components, patterns, and data structures
  - Feature scope aligned with Discovery
  - Ready to create detailed specification in S2.P2

**Exit Condition:** Research Phase is complete when Phase 1.5 audit passes (all 4 categories with evidence), Discovery Context is verified in spec.md, research findings are documented, and you're ready to proceed to S2.P2 for specification creation.

---

## Next Stage

**After completing Research Phase:**

--> **Proceed to:** stages/s2/s2_p2_specification.md

**What happens in S2.P2:**
- Step 2: Update Spec & Checklist (with requirement traceability)
- Phase 2.5: Spec-to-Discovery Alignment Check (MANDATORY GATE)

**Prerequisites for S2.P2:**
- Phase 1.5 audit PASSED (from this guide)
- Discovery Context section verified in spec.md
- Research findings documented

**Time Estimate for S2.P2:** 30-45 minutes

---

**END OF S2.P1 - RESEARCH PHASE GUIDE**
