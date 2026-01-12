# S2: Feature Deep Dive Guide (ROUTER)

🚨 **IMPORTANT: This guide has been split into focused sub-stages**

**This is a routing guide.** The complete S2 workflow is now split across three focused guides:

- **S2.P1 (Research):** Epic intent extraction, targeted research, research audit
- **S2.P2 (Specification):** Spec with traceability, alignment check
- **S2.P3 (Refinement):** Questions, scope, cross-feature alignment, user approval

**📖 Read the appropriate sub-stage guide based on your current phase.**

---

## 📖 Terminology Note

**S2 is split into phases:**
- **S2.P1:** Research (guide: `s2_p1_research.md`)
- **S2.P2:** Specification (guide: `s2_p2_specification.md`)
- **S2.P3:** Refinement (guide: `s2_p3_refinement.md`)

**Naming:** Uses hierarchical notation (S2.P1, 2.2, 2.3)

---

## Quick Navigation

**Use this table to find the right guide:**

| Current Phase | Guide to Read | Time Estimate |
|---------------|---------------|---------------|
| Starting S2 | `stages/s2/s2_p1_research.md` | 45-60 min |
| Phase 0: Epic Intent Extraction | `stages/s2/s2_p1_research.md` | 15 min |
| Phase 1: Targeted Research | `stages/s2/s2_p1_research.md` | 30-45 min |
| Phase 1.5: Research Completeness Audit | `stages/s2/s2_p1_research.md` | 15 min |
| Phase 2: Update Spec & Checklist | `stages/s2/s2_p2_specification.md` | 30-45 min |
| Phase 2.5: Spec-to-Epic Alignment Check | `stages/s2/s2_p2_specification.md` | 15 min |
| Phase 3: Interactive Question Resolution | `stages/s2/s2_p3_refinement.md` | 30-90 min |
| Phase 4: Dynamic Scope Adjustment | `stages/s2/s2_p3_refinement.md` | 15 min |
| Phase 5: Cross-Feature Alignment | `stages/s2/s2_p3_refinement.md` | 15-30 min |
| Phase 6: Acceptance Criteria & User Approval | `stages/s2/s2_p3_refinement.md` | 15-30 min |

---

## S2 Overview

**What is S2?**
Feature Deep Dive is where you thoroughly analyze each feature by extracting epic intent, researching the codebase, creating detailed specifications with requirement traceability, and getting user approval on acceptance criteria.

**Total Time Estimate:** 2-3 hours per feature (9 phases across 3 guides, 2 mandatory gates)

**Exit Condition:** S2 is complete for a feature when the spec has user-approved acceptance criteria, passes both mandatory gates (Research Completeness Audit + Spec-to-Epic Alignment Check), and has zero unresolved checklist items

---

## Sub-Stage Breakdown

### S2.P1: Research Phase (Phases 0, 1, 1.5)

**Read:** `stages/s2/s2_p1_research.md`

**What it covers:**
- **Phase 0:** Epic Intent Extraction (re-read epic, extract user's exact words)
- **Phase 1:** Targeted Research (research components mentioned in epic)
- **Phase 1.5:** Research Completeness Audit (MANDATORY GATE - verify research is thorough)

**Key Outputs:**
- "Epic Intent" section in spec.md (grounding in user's original request)
- Research findings documented in epic/research/{FEATURE_NAME}_DISCOVERY.md
- Evidence collected: file paths, line numbers, code snippets
- Research completeness audit passed

**Time Estimate:** 45-60 minutes

**When complete:** Transition to S2.P2

**Why this sub-stage exists:**
- Reduces token usage by 60% (1,037 lines vs 2,348 lines)
- Focuses agent on research phase only
- Clear mandatory gate (Phase 1.5) before specification work

---

### S2.P2: Specification Phase (Phases 2, 2.5)

**Read:** `stages/s2/s2_p2_specification.md`

**What it covers:**
- **Phase 2:** Update Spec & Checklist (document requirements with traceability)
- **Phase 2.5:** Spec-to-Epic Alignment Check (MANDATORY GATE - verify no scope creep)

**Key Outputs:**
- spec.md complete with requirement traceability (every requirement has source: Epic/User Answer/Derived)
- checklist.md with open questions (valid questions, not research gaps)
- Alignment check passed (no scope creep, no missing requirements)

**Time Estimate:** 30-45 minutes

**When complete:** Transition to S2.P3

**Why this sub-stage exists:**
- Focuses on specification quality and traceability
- Prevents scope creep through mandatory alignment check
- Ensures checklist questions are valid (not things that should have been researched)

---

### S2.P3: Refinement Phase (Phases 3, 4, 5, 6)

**Read:** `stages/s2/s2_p3_refinement.md`

**What it covers:**
- **Phase 3:** Interactive Question Resolution (ONE question at a time)
- **Phase 4:** Dynamic Scope Adjustment (split if >35 items)
- **Phase 5:** Cross-Feature Alignment (compare to completed features)
- **Phase 6:** Acceptance Criteria & User Approval (MANDATORY GATE)

**Key Outputs:**
- All checklist questions resolved (zero open items)
- Spec updated in real-time after each answer
- Feature scope validated (split if needed)
- Cross-feature conflicts resolved
- Acceptance criteria created and user-approved

**Time Estimate:** 1-2 hours (depends on number of questions)

**When complete:** Feature's S2 is COMPLETE

**Why this sub-stage exists:**
- Focuses on interactive refinement with user
- Clear one-question-at-a-time protocol
- Systematic cross-feature alignment process
- User approval as final gate

---

## Workflow Through Sub-Stages

```
┌──────────────────────────────────────────────────────────────┐
│                   S2 Workflow                           │
└──────────────────────────────────────────────────────────────┘

Start Feature Deep Dive
          │
          ▼
    ┌─────────────┐
    │  STAGE_2a   │  Research Phase
    │  (45-60min) │  • Phase 0: Epic Intent Extraction
    └─────────────┘  • Phase 1: Targeted Research
          │          • Phase 1.5: Research Audit (GATE)
          │
    [Research Audit Passed?]
          │
          ▼
    ┌─────────────┐
    │  STAGE_2b   │  Specification Phase
    │  (30-45min) │  • Phase 2: Spec & Checklist
    └─────────────┘  • Phase 2.5: Alignment Check (GATE)
          │
    [Alignment Check Passed?]
          │
          ▼
    ┌─────────────┐
    │  STAGE_2c   │  Refinement Phase
    │  (1-2 hours)│  • Phase 3: Question Resolution
    └─────────────┘  • Phase 4: Scope Adjustment
          │          • Phase 5: Cross-Feature Alignment
          │          • Phase 6: User Approval (GATE)
          │
    [User Approved?]
          │
          ▼
    S2 COMPLETE
          │
          ▼
    [More features?]
     │           │
    YES         NO
     │           │
     ▼           ▼
  Next        S3
 Feature
STAGE_2a
```

---

## Mandatory Gates

**S2 has THREE mandatory gates that cannot be skipped:**

### Gate 1: Phase 1.5 - Research Completeness Audit (STAGE_2a)

**Purpose:** Verify research was thorough enough to avoid "should have known" checklist questions

**Pass Criteria:**
- Can cite EXACT files/classes that will be modified (with line numbers)
- Have READ source code (not just searched)
- Can cite actual method signatures from source
- Have searched for similar features and READ their implementation
- Have READ actual data files (not just assumed format)
- Have re-read epic notes in this phase

**If fail:**
- Return to Phase 1 (Targeted Research)
- Conduct additional research
- Collect missing evidence
- Re-run audit

**Cannot proceed to Phase 2 without passing this gate.**

---

### Gate 2: Phase 2.5 - Spec-to-Epic Alignment Check (STAGE_2b)

**Purpose:** Verify spec accurately reflects epic intent (no scope creep, no missing requirements)

**Pass Criteria:**
- Every requirement traces back to epic request OR user answer OR logical derivation
- No requirements with "assumption" as source
- No scope creep (adding things user didn't ask for)
- No missing requirements (user asked but not in spec)
- All requirements have cited sources

**If fail:**
- Remove scope creep items (move to checklist as questions)
- Add missing requirements from epic
- Fix requirement sources (Epic/User Answer/Derived)
- Re-run alignment check

**Cannot proceed to Phase 3 without passing this gate.**

---

### Gate 3: Phase 6 - User Approval (STAGE_2c)

**Purpose:** Get explicit user sign-off on acceptance criteria before implementation planning

**Pass Criteria:**
- Acceptance Criteria section created in spec.md
- User has reviewed acceptance criteria
- User explicitly approved (said "yes", "approved", "looks good", etc.)
- Approval checkbox marked [x]
- Approval timestamp documented

**If fail:**
- Update spec based on user feedback
- Re-present acceptance criteria
- Wait for approval again

**Cannot proceed to S3 without user approval.**

---

## Critical Rules (Same Across All Sub-Stages)

```
┌─────────────────────────────────────────────────────────────┐
│ CRITICAL RULES - Apply to ALL sub-stages                    │
└─────────────────────────────────────────────────────────────┘

1. ⚠️ ALWAYS start with Phase 0 (Epic Intent Extraction)
   - Re-read epic notes file EVERY time (no exceptions)
   - Extract EXACT QUOTES from epic (not paraphrases)

2. ⚠️ Research MUST be thorough BEFORE creating checklist
   - Phase 1.5 audit is MANDATORY GATE
   - Evidence required: file paths, line numbers, code snippets

3. ⚠️ NEVER MAKE ASSUMPTIONS - CONFIRM WITH USER FIRST
   - Do NOT assume requirements or behavior
   - ASK USER via checklist.md questions
   - Spec assertions MUST be traced to sources

4. ⚠️ Every requirement MUST have traceability
   - Source: Epic Request (cite line)
   - Source: User Answer (cite question)
   - Source: Derived Requirement (explain derivation)
   - If source is "assumption" → add to checklist as question

5. ⚠️ ONE question at a time (don't batch questions)
   - Ask question
   - Wait for user answer
   - Update spec/checklist immediately
   - Then ask next question

6. ⚠️ Targeted research for THIS feature ONLY
   - Do NOT deep dive into other features yet
   - Keep research focused on current feature's scope

7. ⚠️ All research documents go in epic's research/ folder
   - NOT in feature folder
   - Shared across all features

8. ⚠️ If checklist grows >35 items, propose split
   - Too large to implement systematically
   - Get user approval before splitting
```

---

## How to Use This Router Guide

### If you're starting S2:

**READ:** `stages/s2/phase_0_research.md`

**Use the phase transition prompt** from `prompts_reference_v2.md`:
```markdown
I'm starting S2a (Research Phase) for Feature {N}: {Name}.

I acknowledge:
- This guide covers Phases 0, 1, and 1.5 (Epic Intent → Research → Audit)
- I must re-read epic notes (Phase 0) even if I "remember" it
- Phase 1.5 Research Audit is MANDATORY GATE (cannot proceed without passing)
- I must collect evidence: file paths, line numbers, code snippets
- Research must be targeted (THIS feature only, not entire epic)

Ready to begin Phase 0: Epic Intent Extraction.
```

---

### If you're resuming mid-S2:

**Check feature README.md Agent Status** to see current phase:

```markdown
**Current Phase:** DEEP_DIVE
**Current Step:** Phase {N} - {Description}
```

**Then read the appropriate guide:**
- **Phase 0, 1, or 1.5:** Read STAGE_2a
- **Phase 2 or 2.5:** Read STAGE_2b
- **Phase 3, 4, 5, or 6:** Read STAGE_2c

**Continue from "Next Action" in Agent Status.**

---

### If you're transitioning between sub-stages:

**After completing STAGE_2a:**
- Update feature README.md Agent Status: "Phase 1.5 complete, starting Phase 2"
- **READ:** `stages/s2/phase_1_specification.md` (full guide)
- Use phase transition prompt from `prompts_reference_v2.md`

**After completing STAGE_2b:**
- Update feature README.md Agent Status: "Phase 2.5 complete, starting Phase 3"
- **READ:** `stages/s2/s2_p3_refinement.md` (full guide)
- Use phase transition prompt from `prompts_reference_v2.md`

**After completing STAGE_2c:**
- Feature's S2 is COMPLETE
- Update epic EPIC_README.md Feature Tracking table
- Proceed to next feature or S3

---

## Completion Criteria (Same as Before Split)

**S2 is complete for THIS feature when ALL of these are true:**

□ **All 9 phases complete:**
  - Phase 0: Epic Intent extracted
  - Phase 1: Targeted Research complete
  - Phase 1.5: Research Audit PASSED (GATE)
  - Phase 2: Spec & Checklist created with traceability
  - Phase 2.5: Alignment Check PASSED (GATE)
  - Phase 3: All questions resolved (ONE at a time)
  - Phase 4: Scope validated (split if >35 items)
  - Phase 5: Cross-feature alignment complete
  - Phase 6: User APPROVED acceptance criteria (GATE)

□ **Files complete:**
  - spec.md: Epic Intent section, requirements with traceability, acceptance criteria (user approved)
  - checklist.md: All questions resolved
  - README.md: S2 marked complete
  - epic/research/{FEATURE_NAME}_DISCOVERY.md: Research findings

□ **Epic updated:**
  - EPIC_README.md Feature Tracking: "[x]" for this feature's S2

□ **All gates passed:**
  - ✅ Phase 1.5: Research Audit
  - ✅ Phase 2.5: Spec Alignment Check
  - ✅ Phase 6: User Approval

---

## Next Stage After S2

**If more features remain:**
- Begin S2 for next feature
- Start with STAGE_2a (Research Phase)
- Repeat all phases

**If ALL features complete S2:**
- Transition to S3 (Cross-Feature Sanity Check)

📖 **READ:** `stages/s_3/cross_feature_sanity_check.md`

---

## Why S2 Was Split

### Problems with Original Monolithic Guide (2,348 lines):

1. **Token inefficiency:** Agents loaded entire guide even when working on single phase
2. **Navigation difficulty:** Hard to find specific phase content in 2,348 line document
3. **Context dilution:** Important phase-specific rules buried in massive guide
4. **Checkpoint confusion:** Unclear when to re-read guide vs continue

### Benefits of Split Guides:

1. **60-70% token reduction per phase:**
   - STAGE_2a: 1,037 lines vs 2,348 lines (56% reduction)
   - STAGE_2b: ~700 lines vs 2,348 lines (70% reduction)
   - STAGE_2c: ~900 lines vs 2,348 lines (62% reduction)

2. **Clear phase boundaries:**
   - Natural breakpoints at mandatory gates
   - Each guide has focused critical rules
   - Obvious transition points

3. **Improved navigation:**
   - Agents read only relevant phase content
   - Faster guide comprehension
   - Easier to resume after session compaction

4. **Better mandatory reading protocol:**
   - Clear "read this guide" instruction per phase
   - Phase-specific acknowledgment prompts
   - Reduced guide abandonment

---

## Frequently Asked Questions

**Q: Do I need to read all three sub-stage guides?**
A: Yes, but sequentially. Read STAGE_2a first, complete it, then read STAGE_2b, complete it, then read STAGE_2c.

**Q: Can I skip a phase?**
A: No. All 9 phases are mandatory. The split doesn't change workflow, just organization.

**Q: What if I'm resuming mid-stage?**
A: Check feature README.md Agent Status for current phase, then read the guide for that phase.

**Q: Do the mandatory gates change?**
A: No. Still 3 gates: Phase 1.5 (Research Audit), Phase 2.5 (Alignment Check), Phase 6 (User Approval).

**Q: Why isn't Phase 2.5 (Spec Validation) in STAGE_2b?**
A: It is! Phase 2.5 is "Spec-to-Epic Alignment Check" covered in STAGE_2b.

**Q: Can I reference the original guide?**
A: Yes. The original guide is backed up as `STAGE_2_feature_deep_dive_guide_ORIGINAL_BACKUP.md` for reference, but use the new split guides for workflow.

---

## Original Guide Location

**Backup:** `STAGE_2_feature_deep_dive_guide_ORIGINAL_BACKUP.md`

**Purpose:** Historical reference only. Do NOT use for workflow.

The original guide has been preserved for reference but is deprecated. All S2 work should use the new split guides (2a, 2b, 2c).

---

## Summary

**S2 is now split into three focused guides:**

1. **stages/s2/phase_0_research.md** - Research & Audit (Phases 0, 1, 1.5)
2. **stages/s2/phase_1_specification.md** - Specification & Alignment (Phases 2, 2.5)
3. **stages/s2/s2_p3_refinement.md** - Refinement & Approval (Phases 3, 4, 5, 6)

**Workflow remains the same:** 9 phases, 3 mandatory gates, same completion criteria

**Improvement:** 60-70% reduction in guide size per phase, clearer navigation, better phase focus

**Start here:** `stages/s2/phase_0_research.md` (unless resuming mid-stage)

---

*End of stages/s2/feature_deep_dive.md (ROUTER)*
