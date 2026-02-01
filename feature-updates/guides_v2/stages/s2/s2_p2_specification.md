# S2: Feature Deep Dives
## S2.P2: Specification Phase

**Guide Version:** 1.0
**Created:** 2026-01-02
**Prerequisites:** S2.P1 complete (Research Phase PASSED)
**Next Phase:** `stages/s_2/s2_p3_refinement.md`
**File:** `s2_p2_specification.md`

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
Specification Phase is where you create detailed technical specifications with requirement traceability (every requirement must have a source), identify open questions for the user, and verify spec alignment with epic intent through a mandatory gate.

**When do you use this guide?**
- S2.P1 complete (Phase 1.5 Research Audit PASSED)
- Discovery Context section exists in spec.md
- Research findings documented
- Ready to create detailed specifications

**Key Outputs:**
- ✅ Complete spec.md with detailed requirements (all with sources: Epic/Derived)
- ✅ Requirement traceability documented (every requirement traces to source)
- ✅ checklist.md created with valid open questions (user preferences, edge cases)
- ✅ Phase 2.5 Spec-to-Epic Alignment Check PASSED (MANDATORY GATE)
- ✅ Zero scope creep, zero missing requirements
- ✅ Ready for S2.P3 (Refinement Phase)

**Time Estimate:**
30-45 minutes (2 phases)

**Exit Condition:**
Specification Phase is complete when spec.md has complete requirements with traceability, checklist.md has valid questions, and Phase 2.5 alignment check passes (no scope creep, no missing requirements).

---

## Critical Rules

```
┌─────────────────────────────────────────────────────────────┐
│ CRITICAL RULES - These MUST be copied to README Agent Status │
└─────────────────────────────────────────────────────────────┘

1. ⚠️ Every requirement MUST have traceability
   - Source: Epic Request (cite line from epic notes)
   - Source: User Answer (cite question number)
   - Source: Derived Requirement (explain derivation)
   - If source is "assumption" → STOP, add to checklist as question

2. ⚠️ NEVER MAKE ASSUMPTIONS - CONFIRM WITH USER FIRST
   - Do NOT assume requirements, methodologies, or behavior
   - Do NOT write specs based on "what makes sense" or "best practices"
   - ASK USER via checklist.md questions BEFORE asserting in spec.md
   - Only document requirements after explicit user confirmation
   - If uncertain about ANY detail → create question in checklist.md

3. ⚠️ Phase 2.5 alignment check is MANDATORY GATE
   - Verify no scope creep (adding things user didn't ask for)
   - Verify no missing requirements (user requested but not in spec)
   - Cannot proceed to STAGE_2c without passing alignment check

4. ⚠️ Only create questions for GENUINE unknowns
   - Good questions: User preferences, business logic, edge cases
   - Bad questions: Things you should have researched in STAGE_2a
   - If you should have known it from code → NOT a checklist question

5. ⚠️ Update feature README.md Agent Status after EACH phase
```

---

## Critical Decisions Summary

**Specification Phase has 1 major decision point:**

### Decision Point 1: Phase 2.5 - Spec-to-Epic Alignment Check (GO/NO-GO)
**Question:** Does spec match user's original request (no scope creep, no missing requirements)?
- **Check for:**
  - Scope creep: Adding things user didn't ask for
  - Missing requirements: User asked but not in spec
  - Invalid sources: Requirements with "assumption" as source
- **If NO (scope creep OR missing requirements found):**
  - ❌ STOP at Phase 2.5
  - Remove scope creep items (move to questions.md)
  - Add missing requirements from epic intent
  - Fix invalid source traceability
  - Re-run Phase 2.5 alignment check
- **If YES (perfect alignment, all requirements traced):**
  - ✅ Proceed to STAGE_2c (Refinement Phase)
- **Impact:** Prevents implementing features user didn't ask for or missing what they did ask for

---

## Prerequisites Checklist

**Verify BEFORE starting Specification Phase:**

□ STAGE_2a complete (Research Phase)
□ Phase 1.5 Research Audit PASSED (all 4 categories)
□ Discovery Context section exists in spec.md (created in Phase 0)
□ Research findings documented in epic/research/{FEATURE_NAME}_DISCOVERY.md
□ Evidence collected (file paths, line numbers, code snippets)
□ Feature README.md Agent Status shows STAGE_2a complete

**If any prerequisite fails:**
- ❌ STOP - Do NOT proceed with specification
- Complete missing prerequisites first
- Document blocker in feature README.md Agent Status

---
## 🔄 Parallel Work Coordination (If Applicable)

**Skip this section if you're in sequential mode**

**If you're in parallel S2 work mode:**

### Coordination Heartbeat (Every 15 Minutes)

**IMPORTANT:** Coordinate regularly to ensure alignment and handle escalations.

1. **Update Checkpoint:**
   - File: `agent_checkpoints/{your_agent_id}.json`
   - Update: `last_checkpoint`, `stage`, `current_step`, `files_modified`
   - Purpose: Enable crash recovery and stale detection

2. **Check Inbox:**
   - File: `agent_comms/primary_to_{your_id}.md` (if Secondary)
   - File: `agent_comms/secondary_{x}_to_primary.md` (if Primary - check ALL secondaries)
   - Look for: ⏳ UNREAD messages
   - Process: Read, mark as ✅ READ, take action, reply if needed

3. **Update STATUS:**
   - File: `feature_{N}_{name}/STATUS`
   - Update: `STAGE`, `PHASE`, `UPDATED`, `BLOCKERS`, `NEXT_ACTION`
   - Format: Plain text key-value pairs

4. **Update EPIC_README.md (when progress changes):**
   - Acquire lock: `.epic_locks/epic_readme.lock` (5-minute timeout)
   - Update only your section (between BEGIN/END markers for your feature)
   - Release lock immediately after update
   - See: `parallel_work/lock_file_protocol.md` for locking details

5. **Set 15-minute timer** for next heartbeat

### Escalation Protocol

**If you're blocked for >30 minutes:**
- Send escalation message to Primary (use template in `parallel_work/communication_protocol.md`)
- Update STATUS: `BLOCKERS: <description>`
- Update checkpoint: `"blockers": ["description"]`
- Wait for Primary response (SLA: 15 minutes)

**Primary-Specific Coordination:**
- Check ALL secondary inboxes every 15 minutes
- Respond to escalations within 15 minutes (mandatory SLA)
- Monitor STATUS files and checkpoints for staleness (30 min warning, 60 min failure)
- Time blocking: 45 min feature work, 15 min coordination

**Coordination overhead target:** <10% of parallel time

**See:** `parallel_work/s2_parallel_protocol.md` for complete coordination workflow

---


## Phase 2: Update Spec & Checklist

**Goal:** Document findings in spec.md and create checklist.md with open questions

**⚠️ NEW: Every requirement must have traceability (source)**

---

### Step 2a: Review Prior Dependency Group Features (NEW - For Group 2+ features only)

**IF your feature is in Group 2 or later (depends on prior group specs):**

1. Identify all completed features from previous dependency groups
   - Check EPIC_README.md Feature Dependency Groups section
   - For Feature 08 (Group 2): Features 01-07 (Group 1) should be complete

2. Read their spec.md files focusing on areas relevant to current feature
   - Focus on: Arguments, configuration, patterns your feature will test/document/integrate with
   - Example: Integration test feature reads argument definitions from all prior features

3. Cross-reference EACH draft checklist question:
   - **If prior features answer it consistently:** DELETE question, document answer as "Aligned with Features X-Y"
   - **If prior features answer it inconsistently:** Escalate as alignment issue to Primary
   - **If prior features don't answer it:** KEEP question (genuinely open)

4. Document which questions were answered by prior features:
   - In spec.md: "Requirements derived from prior group alignment: R1 (from F01-07), R2 (from F03), etc."

**Example from KAI-7 Feature 08:**
- **Draft Q3:** "--debug vs --log-level precedence?"
- **Check Features 01-07:** All 7 specify --debug forces DEBUG level (Option A)
- **Action:** DELETE Q3, ADD to spec.md R1: "Precedence rule: --debug forces DEBUG (aligned with Features 01-07)"
- **Result:** No user question needed, no alignment conflict later

**Benefits:**
- Fewer user questions (already-answered questions not re-asked)
- No alignment conflicts later (inconsistencies caught during checklist creation)
- Faster S2.P3 Phase 5 (fewer conflicts to resolve)
- Better user experience (don't answer same question twice)

---

### Step 2.1: Update spec.md with Technical Details (WITH TRACEABILITY)

**CRITICAL CHANGE:** Every requirement must cite its source.

**Valid sources:**
1. **Epic Request** - User explicitly asked for this (cite line from epic notes)
2. **User Answer** - User answered checklist question (cite question number)
3. **Derived Requirement** - Logically required to fulfill user request (explain derivation)

**If source is "assumption":**
- ❌ Remove from spec.md immediately
- ❌ Add to checklist.md as a QUESTION
- ❌ Get user answer first, THEN add to spec with "Source: User Answer to Q{N}"

---

**Add/expand these sections in `spec.md`:**

#### Components Affected

Document all classes/files to modify or create, with sources for each:
- List existing classes to modify (file path, line numbers, specific methods)
- List new files to create (purpose, exports, pattern to follow)
- Include traceability: Epic Request (cite line) or Derived (explain why necessary)
- Mark assumptions with ⚠️ and move to checklist

**See:** `reference/stage_2/specification_examples.md` → Example 1 for complete template

#### Requirements (WITH SOURCES)

Document each requirement with:
- Description (what this requirement does)
- Source (Epic Request line X / User Answer Q{N} / Derived)
- Traceability (why this requirement exists)
- Implementation details (how to fulfill requirement)
- Edge cases (TBD items → add to checklist)

**Key principle:** If you can't cite a source, it's an assumption → move to checklist

**See:** `reference/stage_2/specification_examples.md` → Example 2 for complete template

#### Data Structures

Document input/output/internal data formats with sources:
- Input data format (CSV/JSON/API structure - may be assumption, ask user)
- Internal representation (new fields on existing classes)
- Output format (how data flows through system)
- Mark TBD items and add to checklist

**See:** `reference/stage_2/specification_examples.md` → Example 3 for data structure patterns

#### Algorithms

Document implementation approach with TBD items:
- Pseudocode for main logic
- Edge case handling (what happens when X fails)
- TBD items that require user input → add to checklist
- Derived requirements (necessary for robustness)

**See:** `reference/stage_2/specification_examples.md` → Example 4 for algorithm patterns

#### Dependencies

Document feature dependencies and integration points:
- What this feature depends on (existing code, other features)
- What depends on this feature (what gets blocked)
- What's independent (parallel features)
- Include status (exists/need to create) and sources

**See:** `reference/stage_2/specification_examples.md` → Example 5 for dependency patterns

---

### Step 2.2: Create checklist.md with Open Questions

**Populate `checklist.md` with questions identified during spec creation:**

**CRITICAL:** Only add questions for actual unknowns (not things you should have researched).

**Good questions ask about:**
- ✅ User preferences (fuzzy vs strict matching, option A vs B)
- ✅ Business logic not specified in epic (multiplier formula, impact level)
- ✅ Edge case handling not mentioned (missing player behavior, error handling)
- ✅ External data formats (CSV column names, API structure)

**Bad questions (should have researched in STAGE_2a):**
- ❌ "Which class should we modify?" → Research in Phase 1
- ❌ "What's the current scoring algorithm?" → Read code in Phase 1
- ❌ "Does PlayerManager have method X?" → Verify in Phase 1.5 audit
- ❌ "How do we load CSV files?" → Research existing utilities

**Checklist Template:**

Each question should include:
- [ ] Checkbox (open question)
- Context (why this is uncertain)
- Options (2-3 approaches with pros/cons)
- Epic reference (what user said or didn't say)
- Recommendation (your suggested approach)
- Why this is a question (genuine unknown, not research gap)
- Impact on spec.md (what will change based on answer)

**See:** `reference/stage_2/specification_examples.md` → Example 3 for complete checklist template with valid/invalid question examples

---

### Step 2.3: Update Agent Status

```markdown
## Agent Status

**Last Updated:** {YYYY-MM-DD HH:MM}
**Current Phase:** SPECIFICATION_PHASE
**Current Step:** Phase 2 - Spec & Checklist Updated (with traceability)
**Current Guide:** stages/s_2/phase_1_specification.md
**Guide Last Read:** {YYYY-MM-DD HH:MM}
**Critical Rules from Guide:**
- Every requirement must have source (Epic/User Answer/Derived)
- If source is "assumption" → remove, add to checklist
- Phase 2.5 alignment check is next (MANDATORY GATE)

**Progress:** 1/2 phases complete (Spec & Checklist)
**Next Action:** Phase 2.5 - Spec-to-Epic Alignment Check (MANDATORY GATE)
**Blockers:** None

**Requirements Added:** {N} (all with sources)
**Checklist Questions:** {M} (all valid unknowns)
**Assumptions Moved to Checklist:** {K}
```

---

## Phase 2.5: Spec-to-Epic Alignment Check (MANDATORY GATE)

**Goal:** Verify spec matches user intent (no scope creep, no missing requirements)

**⚠️ CRITICAL:** This is a MANDATORY GATE. Cannot proceed to STAGE_2c without passing this check.

**Why this phase exists:**
- Prevents scope creep (adding features user didn't ask for)
- Prevents missing requirements (user asked but not in spec)
- Ensures spec traces back to epic intent
- Catches misalignment BEFORE asking user questions

---

### Step 2.5.1: Re-Read Discovery Context Section

**Read the "Discovery Context" section** at the top of spec.md (created in STAGE_2a Phase 0).

**Refresh your memory:**
- What did the user EXPLICITLY request?
- What constraints did user mention?
- What's out of scope?
- What's the user's end goal?

---

### Step 2.5.2: Verify Every Requirement Has Valid Source

**Review "Requirements" section of spec.md:**

For EACH requirement, verify:
- Source type (Epic Request / User Answer / Derived)
- Citation exists (epic line number if Epic Request)
- Derivation explanation (if Derived)
- No assumptions (if ⚠️ ASSUMPTION → remove and add to checklist)

**Valid source types:**
- **Epic Request:** Citation exists, quote accurate, matches user's words
- **User Answer:** N/A at this point (haven't asked questions yet)
- **Derived:** Explanation exists, logically necessary (not "nice to have")
- **⚠️ ASSUMPTION:** INVALID → remove from spec, add to checklist

**See:** `reference/stage_2/specification_examples.md` → Phase 2.5 Example 1 for complete verification template

---

### Step 2.5.3: Check for Scope Creep

**For EACH requirement, ask:**

1. **Did the user ask for this?** → Check Discovery Context section
2. **Is this necessary or "nice to have"?** → Necessary = logically required, Nice to have = best practice
3. **Am I solving the user's problem or a different one?** → Compare requirement to Discovery Context quotes

**If scope creep found:**
- ❌ Remove from spec.md immediately
- ❌ Add to checklist.md: "User requested X, should we also do Y?"
- ❌ Get user approval before adding back

**See:** `reference/stage_2/specification_examples.md` → Phase 2.5 Example 2 for scope creep detection template and example

---

### Step 2.5.4: Check for Missing Requirements

**Re-read Discovery Context section:**

List all explicit user requests, then verify EACH is in spec:

**If missing requirements found:**
- ❌ Add to spec.md immediately with source (epic notes line number)
- ❌ Verify no other user requests were missed
- ❌ Cannot proceed until all user requests are addressed

**See:** `reference/stage_2/specification_examples.md` → Phase 2.5 Example 3 for missing requirements detection template

---

### Step 2.5.5: Overall Alignment Result

**Document alignment check results:**

**Checklist:**
- [ ] All requirements have valid sources (Epic/Derived)
- [ ] No requirements with "User Answer" source (not asked yet)
- [ ] No requirements with "⚠️ ASSUMPTION" source
- [ ] No scope creep detected (or removed to checklist)
- [ ] No missing requirements (or added to spec)

**Result:**
- ✅ PASSED → Proceed to Phase 2.6 (Gate 2)
- ❌ FAILED → Resolve issues, re-run alignment check

**If FAILED:** Cannot proceed until PASSED (remove scope creep, add missing requirements, fix invalid sources)

**See:** `reference/stage_2/specification_examples.md` → Phase 2.5 Example 4 for complete alignment summary template

---

### Step 2.5.6: Update Agent Status

```markdown
## Agent Status

**Last Updated:** {YYYY-MM-DD HH:MM}
**Current Phase:** SPECIFICATION_PHASE
**Current Step:** Phase 2.5 - Spec-to-Epic Alignment Check PASSED
**Current Guide:** stages/s_2/phase_1_specification.md
**Guide Last Read:** {YYYY-MM-DD HH:MM}
**Critical Rules from Guide:**
- Phase 2.5 alignment check is MANDATORY GATE
- Cannot proceed without passing alignment check
- All requirements must trace to epic intent

**Progress:** 2/2 phases complete (Specification Phase COMPLETE)
**Next Action:** Refinement Phase (Interactive Question Resolution)
**Next Guide:** stages/s_2/phase_2_refinement.md
**Blockers:** None

**Alignment Result:** ✅ PASSED
**Scope Creep Removed:** {K} requirements
**Missing Requirements Added:** {L} requirements
**Final Requirements:** {N} (all aligned with epic)
```

---

## Completion Criteria

**Specification Phase (STAGE_2b) is COMPLETE when ALL of these are true:**

□ **Phase 2 Complete:**
  - spec.md updated with complete technical details
  - All requirements have traceability (Epic Request/Derived)
  - Components Affected section complete (with sources)
  - Data Structures section complete
  - Algorithms section complete (with TBD items noted)
  - Dependencies section complete
  - checklist.md created with valid open questions
  - Assumptions removed from spec and moved to checklist

□ **Phase 2.5 Complete:**
  - Spec-to-Epic alignment check PASSED
  - Every requirement has valid source verified
  - No scope creep detected (or removed)
  - No missing requirements (or added to spec)
  - Overall alignment result: ✅ PASSED

□ **Documentation Complete:**
  - spec.md has requirement traceability for ALL requirements
  - checklist.md has valid questions (user preferences, edge cases, unknowns)
  - Agent Status updated with STAGE_2b completion

□ **Ready for Next Stage:**
  - All requirements aligned with epic intent
  - Open questions identified (not assumptions)
  - Ready to ask user questions in STAGE_2c

**Exit Condition:** Specification Phase is complete when spec.md has complete requirements with traceability, Phase 2.5 alignment check passes, checklist.md has questions, and Gate 2 (User Checklist Approval) is obtained.

---

## Phase 2.6: Present Checklist to User for Approval (🚨 MANDATORY GATE 2)

**After Phase 2.5 passes, you MUST present checklist.md to user for approval before proceeding to STAGE_2c.**

**This is Gate 2 - User Checklist Approval (from mandatory_gates.md)**

### Why This Step Exists

**From guide-updates.txt #2:**
> "Require ALL checklist items to be confirmed by the user. Stop resolving anything on their own, including things the agent thinks is straightforward"

**Purpose:**
- User sees ALL questions/uncertainties before implementation planning
- User provides answers to ALL questions
- Zero autonomous agent resolution
- Prevents agents from making assumptions and "resolving" checklist items themselves

**This is NOT optional** - it's a MANDATORY checkpoint per mandatory_gates.md.

---

### Process

**1. Verify checklist.md is complete:**

Before presenting, verify:
- [ ] All sections populated (questions organized by category)
- [ ] Each question has: Context, Options, Recommendation, Impact
- [ ] NO items marked `[x]` (agents cannot self-resolve)
- [ ] Questions are valid (not things you should have researched)

**2. Present checklist to user:**

Use the "User Checklist Approval" prompt from `prompts_reference_v2.md`:
- List file location
- Summarize question count by category
- Explain user can answer all at once, one at a time, or request clarification

**See:** `reference/stage_2/specification_examples.md` → Gate 2 Example 1 for complete presentation template

**3. Wait for user response:**

- **If user provides answers:** Update spec.md + checklist.md, mark resolved
- **If user requests clarification:** Provide context, explain trade-offs, wait for decision
- **If user identifies invalid questions:** Remove, add to retrospective

**See:** `reference/stage_2/specification_examples.md` → Gate 2 Examples 2-4 for user response patterns

**4. Document approval:**

After ALL questions answered, add User Approval section to checklist.md with:
- Timestamp, approval status, question counts, user comments, Gate 2 status

**5. Update spec.md with all answers:**

For EACH question, update relevant spec.md section with:
- Source: User Answer to Checklist Q{N}
- User's answer (quote or paraphrase)
- Implementation impact

**6. Update Agent Status:**

Document Gate 2 completion with timestamp and PASSED status

---

### Final Checklist Approval

**After user answers ALL questions:**

Update Agent Status in feature README.md:
- Mark STAGE_2b COMPLETE + Gate 2 PASSED
- Document checklist status (all answered, pending 0)
- Note spec.md updated with user answers
- Identify next action (usually S5a if no NEW questions)

---

### Common Mistake to Avoid

**❌ MISTAKE: "I'll research this question and resolve it myself"**

**Why wrong:** Gate 2 prevents autonomous resolution. User MUST answer every question.

**Correct approach:**
- ✅ Present checklist to user
- ✅ WAIT for user answers
- ✅ Do NOT research and answer yourself
- ✅ Only update spec.md AFTER user provides answer

---

**After Gate 2 passes:**
- spec.md is complete and aligned with epic
- checklist.md has questions for user (if any)
- Ready to present to user for Gate 3 (User Checklist Approval)

**If user requests investigation during Gate 3 review:**

**Correct Status Progression (9 steps):**
1. User asks question (e.g., "check simulation compatibility")
2. Agent adds question to checklist → Status: OPEN
3. Agent investigates comprehensively (use 5-category checklist)
4. Agent presents findings → Status: PENDING USER APPROVAL
5. User reviews findings, may ask follow-ups
6. Agent investigates follow-ups (if any)
7. User says "approved" or "looks good" (explicit approval required)
8. **ONLY THEN** agent marks → Status: RESOLVED
9. Agent adds requirement to spec with source: "User Answer to Question N"

**Key Principle:** Investigation complete ≠ Question resolved. Always wait for explicit user approval before marking RESOLVED.

**WRONG:**


**CORRECT:**


---

**After Gate 2 passes (all questions answered and approved), you have two options:**

1. **If checklist complete with zero NEW questions:**
   - Skip STAGE_2c (Refinement Phase) entirely
   - Proceed directly to S5a (Implementation Planning)
   - Note: Phase 6 (Acceptance Criteria) still required before S5a

2. **If NEW questions arise:**
   - Proceed to STAGE_2c (Refinement Phase)
   - Handle any additional questions in Phase 3
   - Complete Phase 4-6 as normal

**Most common path:** Gate 2 completes checklist → Skip to S5a

---

## Next Stage

**After completing Specification Phase + Gate 2:**

**Option A: No new questions (most common):**
→ **Proceed to:** S5a (Implementation Planning)
→ **Skip:** STAGE_2c if checklist is complete

**Option B: New questions discovered:**
→ **Proceed to:** stages/s_2/phase_2_refinement.md (STAGE_2c)

**What happens in STAGE_2c (if needed):**
- Step 3: Handle any NEW questions (repeated)
- Step 4: Dynamic Scope Adjustment (split if >35 items)
- Step 5: Cross-Feature Alignment (compare to completed features)
- Step 6: Acceptance Criteria Creation (MANDATORY before S5a)

**Prerequisites for S5a:**
- ✅ Phase 2.5 alignment check PASSED
- ✅ Gate 2 (User Checklist Approval) PASSED
- ✅ spec.md has requirements with traceability
- ✅ spec.md updated with all user answers
- ✅ Acceptance criteria defined (Phase 6 or earlier)

**Time Estimate:**
- If skipping STAGE_2c: Proceed immediately to S5a
- If continuing to STAGE_2c: 45-60 minutes

---

**END OF STAGE_2b - SPECIFICATION PHASE GUIDE**
