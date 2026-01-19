# S2: Feature Deep Dives
## S2.P1: Research Phase

**Guide Version:** 1.0
**Created:** 2026-01-02
**Prerequisites:** S1 complete, feature folder exists
**Next Phase:** `stages/s_2/s2_p2_specification.md`
**Detailed Examples:** `reference/stage_2/research_examples.md`
**File:** `s2_p1_research.md`

---

**📚 Companion Reference:** This guide focuses on workflow steps. For detailed examples, templates, and anti-patterns, see `reference/stage_2/research_examples.md`

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

## Quick Start

**What is this guide?**
Research Phase is the first part of Feature Deep Dive where you extract epic intent, conduct targeted research grounded in user requests, and verify research completeness through a mandatory audit before creating specifications.

**When do you use this guide?**
- S1 complete (epic folder structure created)
- Feature folder exists with initial spec.md
- Ready to begin deep dive for this specific feature
- Starting from scratch on feature research

**Key Outputs:**
- ✅ Epic Intent section added to spec.md (user's original request with quotes)
- ✅ Targeted research complete (components user mentioned, not generic research)
- ✅ Research findings documented in epic/research/{FEATURE_NAME}_DISCOVERY.md
- ✅ Phase 1.5 Research Completeness Audit PASSED (MANDATORY GATE)
- ✅ Evidence collected (file paths, line numbers, code snippets)
- ✅ Ready for S2.P2 (Specification Phase)

**Time Estimate:**
45-60 minutes (3 phases)

**Exit Condition:**
Research Phase is complete when Phase 1.5 audit passes (all 4 categories with evidence), Epic Intent section is documented in spec.md, and research findings are ready for spec creation.

---

## Critical Rules

```
┌─────────────────────────────────────────────────────────────┐
│ CRITICAL RULES - These MUST be copied to README Agent Status │
└─────────────────────────────────────────────────────────────┘

1. ⚠️ ALWAYS start with Phase 0 (Epic Intent Extraction)
   - Re-read epic notes file EVERY time (no exceptions)
   - Extract EXACT QUOTES from epic (not paraphrases)
   - Ground feature in user's original request BEFORE technical work

2. ⚠️ Research MUST be grounded in epic intent (not generic)
   - ONLY research components user explicitly mentioned
   - Do NOT research "how the codebase works generally"
   - Use Epic Intent section to guide what to research

3. ⚠️ READ source code - do NOT guess
   - Use Read tool to view actual code
   - Copy actual method signatures
   - Note actual line numbers
   - View actual data file contents

4. ⚠️ Phase 1.5 audit is MANDATORY GATE
   - Cannot proceed to STAGE_2b without PASSING audit
   - All 4 categories must pass (Component, Pattern, Data, Epic)
   - Evidence required: cite file paths, line numbers, code snippets

5. ⚠️ All research documents go in epic's research/ folder
   - NOT in feature folder
   - Shared across all features
   - Named: {FEATURE_NAME}_DISCOVERY.md

6. ⚠️ Update feature README.md Agent Status after EACH phase
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

## Step 0: Epic Intent Extraction (MANDATORY FIRST STEP)

**Goal:** Ground this feature in the epic's original request BEFORE any technical work

**⚠️ CRITICAL:** Do NOT skip this phase. Re-reading epic notes prevents misunderstanding user intent.

---

### Step 0.1: Re-Read Epic Request

**Read:** `feature-updates/KAI-{N}-{epic_name}/{epic_name}_notes.txt`

**Why this matters:**
- Even if you "remember" the epic from S1, read it AGAIN
- Context window limits may have caused you to forget details
- User's exact words matter (not your interpretation)

**Do NOT skip this step.**

---

### Step 0.2: Extract User Intent for THIS Feature

**Answer these 6 questions using EXACT QUOTES from epic notes:**

1. What problem is THIS feature solving?
2. What did the user EXPLICITLY request for this feature?
3. What constraints did the user mention?
4. What is OUT of scope? (user said "not now" or "future")
5. What is the user trying to ACCOMPLISH? (end goal)
6. What technical components did the user mention?

**Template and detailed examples:** See `reference/stage_2/research_examples.md` → Phase 0 Examples

**CRITICAL RULE:**
- Use EXACT QUOTES (copy-paste from epic notes)
- Cite line numbers for every quote
- If user didn't mention something → it's an ASSUMPTION (add to checklist later)

---

### Step 0.3: Create "Epic Intent" Section in spec.md

**Update `feature_{N}_{name}/spec.md`:**

Add Epic Intent section as the **FIRST section** (before any technical details).

**Required subsections:**
- Problem This Feature Solves (with quote and line citation)
- User's Explicit Requests (list with quotes and line citations)
- User's Constraints (list with quotes and line citations)
- Out of Scope (what user explicitly excluded)
- User's End Goal (quote and line citation)
- Technical Components Mentioned by User (list with line citations)
- Agent Verification checklist (re-read timestamp, extraction verification)

**Complete template with example:** See `reference/stage_2/research_examples.md` → Phase 0 Examples → Example 2

---

### Step 0.4: Verify Epic Alignment

**BEFORE proceeding to Phase 1, verify:**

```markdown
## Phase 0 Verification Checklist

□ I have re-read the epic notes file (`{epic_name}_notes.txt`)
□ I have extracted EXACT QUOTES (not paraphrased or interpreted)
□ I have cited line numbers for every quote
□ I understand what the USER wants (not what I think is technically best)
□ I have documented out-of-scope items (what user explicitly excluded)
□ I have added "Epic Intent" section to spec.md as FIRST section
□ I can list what user EXPLICITLY requested (vs what I'm assuming)
```

**If any item unchecked:**
- ❌ Do NOT proceed to Phase 1
- ❌ Complete this phase first
- ❌ Update Agent Status with blocker

**Why this matters:**
- Prevents misunderstanding user intent
- Prevents implementing features user didn't ask for
- Provides traceability (every requirement traces to epic intent)
- Allows early detection of scope mismatch (in STAGE_2b Phase 2.5 alignment check)

---

### Step 0.5: Update Agent Status

```markdown
## Agent Status

**Last Updated:** {YYYY-MM-DD HH:MM}
**Current Phase:** RESEARCH_PHASE
**Current Step:** Phase 0 - Epic Intent Extraction Complete
**Current Guide:** stages/s_2/phase_0_research.md
**Guide Last Read:** {YYYY-MM-DD HH:MM}
**Critical Rules from Guide:**
- Always start with Phase 0 (Epic Intent Extraction)
- Re-read epic notes EVERY time
- Extract EXACT QUOTES, not paraphrases
- All requirements must trace to epic intent

**Progress:** 1/3 phases complete (Epic Intent Extraction)
**Next Action:** Phase 1 - Targeted Research (using epic intent to guide)
**Blockers:** None

**Epic Notes Re-Read:** {YYYY-MM-DD HH:MM}
**User Explicit Requests Identified:** {N}
```

---

## Phase 1: Targeted Research

**Goal:** Understand THIS feature's technical requirements (NOT the entire epic)

**⚠️ NEW: Use Phase 0 Epic Intent to GUIDE research (not generic research)**

---

### Step 1.1: Read Initial Spec from S1

Read `feature_{N}_{name}/spec.md` created in S1.

**Also re-read "Epic Intent" section** (just added in Phase 0).

**Extract:**
- Feature purpose (what it does)
- Initial scope (what's included)
- Dependencies (what it needs)
- User's explicit requests (from Epic Intent section)
- Technical components mentioned by user (from Epic Intent section)

---

### Step 1.2: Extract Research Questions FROM Epic Request (NOT Generic)

**CRITICAL CHANGE:** Do NOT use generic research questions. Only research what epic/feature explicitly mentions.

**FIRST: Review "Technical Components Mentioned by User" from Epic Intent section**

**For EACH component/term mentioned in epic, create targeted research:**

Research only components user mentioned:
- Component classes (e.g., PlayerManager)
- Patterns to follow (e.g., injury penalty system)
- Data sources (e.g., CSV files)
- Related features (e.g., existing multipliers)

**Template with detailed checklist:** See `reference/stage_2/research_examples.md` → Phase 1 Examples → Example 1

**Anti-Pattern Detection:**

❌ "Let me research how scoring works generally"
   ✅ STOP - Epic mentions "PlayerManager scoring" specifically, research THAT

❌ "Let me search for all data sources"
   ✅ STOP - Epic mentions "ADP data" specifically, research THAT

❌ "Let me understand the entire codebase architecture"
   ✅ STOP - Only research components mentioned in epic intent

**Key Principle:** If epic/feature doesn't mention it, DON'T research it yet. You'll discover additional needs later, but start grounded in user's words.

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

### Step 1.4: Document Findings in Research Folder

Create `epic/research/{FEATURE_NAME}_DISCOVERY.md`:

**Required sections:**
- Epic Intent Summary (brief summary from Epic Intent section)
- Components Identified (for each component user mentioned)
  - User's quote mentioning component
  - Found in codebase (file paths, line numbers)
  - Actual code signatures and snippets
  - How it works today
  - Relevance to this feature
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
**Current Guide:** stages/s_2/phase_0_research.md
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

**Category 4: Epic Request Knowledge**
- Question 4.1: Have I re-read epic notes file in THIS phase?
- Question 4.2: Can I list what user EXPLICITLY requested?
- Question 4.3: Can I identify what's NOT mentioned (assumptions)?

**For EACH question, provide:**
- Your answer (be specific, cite evidence)
- Evidence (file paths, line numbers, code snippets, timestamps)

**Complete audit template with examples:** See `reference/stage_2/research_examples.md` → Phase 1.5 Examples → Example 1 (PASSING) and Example 2 (FAILED)

---

### Step 1.5.5: Overall Audit Result

**Summarize audit results for all 4 categories:**

□ Category 1 (Component Knowledge): PASSED / FAILED
□ Category 2 (Pattern Knowledge): PASSED / FAILED
□ Category 3 (Data Structure Knowledge): PASSED / FAILED
□ Category 4 (Epic Request Knowledge): PASSED / FAILED

**OVERALL RESULT:**
- ✅ PASSED - All 4 categories passed → Proceed to STAGE_2b
- ❌ FAILED - At least one category failed → Return to Phase 1

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
**Current Guide:** stages/s_2/phase_0_research.md
**Guide Last Read:** {YYYY-MM-DD HH:MM}
**Critical Rules from Guide:**
- Phase 1.5 audit is MANDATORY GATE
- Cannot proceed without passing all 4 categories
- Evidence required for all answers

**Progress:** 3/3 phases complete (Research Phase COMPLETE)
**Next Action:** Specification Phase (Update Spec & Checklist with traceability)
**Next Guide:** stages/s_2/phase_1_specification.md
**Blockers:** None

**Audit Result:** ✅ PASSED (all 4 categories)
**Files Read:** {N}
**Code Snippets Collected:** {N}
```

---

## Completion Criteria

**Research Phase (STAGE_2a) is COMPLETE when ALL of these are true:**

□ **Phase 0 Complete:**
  - Epic notes file re-read
  - "Epic Intent" section created in spec.md (FIRST section)
  - User explicit requests extracted with line citations
  - Out-of-scope items documented

□ **Phase 1 Complete:**
  - Targeted research conducted (grounded in epic intent)
  - Research focused on components mentioned in epic
  - Findings documented in epic/research/{FEATURE_NAME}_DISCOVERY.md
  - Evidence collected (file paths, line numbers, code snippets)

□ **Phase 1.5 Complete:**
  - Research completeness audit PASSED
  - All 4 categories verified (Component, Pattern, Data, Epic)
  - Evidence provided for all audit questions
  - Overall audit result: ✅ PASSED

□ **Documentation Complete:**
  - spec.md has Epic Intent section at top
  - research/{FEATURE_NAME}_DISCOVERY.md created with findings
  - Agent Status updated with STAGE_2a completion

□ **Ready for Next Stage:**
  - All research evidence collected and documented
  - Clear understanding of components, patterns, and data structures
  - Epic intent fully extracted and understood
  - Ready to create detailed specification in STAGE_2b

**Exit Condition:** Research Phase is complete when Phase 1.5 audit passes (all 4 categories with evidence), Epic Intent section is in spec.md, research findings are documented, and you're ready to proceed to STAGE_2b for specification creation.

---

## Next Stage

**After completing Research Phase:**

→ **Proceed to:** stages/s_2/phase_1_specification.md

**What happens in STAGE_2b:**
- Step 2: Update Spec & Checklist (with requirement traceability)
- Phase 2.5: Spec-to-Epic Alignment Check (MANDATORY GATE)

**Prerequisites for STAGE_2b:**
- Phase 1.5 audit PASSED (from this guide)
- Epic Intent section in spec.md
- Research findings documented

**Time Estimate for STAGE_2b:** 30-45 minutes

---

**END OF STAGE_2a - RESEARCH PHASE GUIDE**
