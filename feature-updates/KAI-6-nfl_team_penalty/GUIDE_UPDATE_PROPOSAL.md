# Guide Update Proposal: KAI-6-nfl_team_penalty

**Epic:** nfl_team_penalty (KAI-6)
**Created:** 2026-01-15
**Total Lessons Analyzed:** 3 (0 epic-level + 3 feature-level)
**Total Proposals:** 5 (P1: 5, P2: 0, P3: 0)

---

## Executive Summary

This epic identified **5 actionable guide improvements** primarily focused on preventing autonomous resolution of checklist items and improving investigation systematicity.

**Breakdown by Priority:**
- **P0 (Critical):** 0 proposals
- **P1 (High):** 5 proposals (prevent autonomous resolution, improve investigation frameworks)
- **P2 (Medium):** 0 proposals
- **P3 (Low):** 0 proposals

**Recommended Action:** Approve all P1 proposals to prevent future autonomous resolution violations and improve investigation quality.

---

## Analysis Summary

**Source Files:**
1. `feature_01_config_infrastructure/lessons_learned.md` - 1 lesson (pre-existing test failures)
2. `feature_02_score_penalty_application/lessons_learned.md` - 2 critical lessons (autonomous resolution + incomplete investigation)
3. `epic_lessons_learned.md` - 0 lessons (not yet populated)

**Key Patterns:**
- Feature 02 had critical S2 violations (autonomous resolution)
- Investigation scope was too narrow (missed config loading)
- Both issues caught by user before causing downstream problems
- Feature 01 had no guide gaps (config-only features work well)

---

## P1 (High Priority) Proposals

### Proposal P1-1: Add Autonomous Resolution Warning to S2.P3 Guide

**Lesson Learned:**
> "User requested: 'Add a checklist item - ensure that the simulation works still after the parameter is introduced'
>
> My actions:
> 1. ✅ Added Question 1 to checklist (CORRECT)
> 2. ✅ Investigated simulation code (CORRECT)
> 3. ❌ Marked Question 1 as 'RESOLVED' (WRONG - only users can resolve)
> 4. ❌ Added Requirement 9 to spec.md based on unapproved answer (WRONG)
> 5. ❌ Updated acceptance criteria prematurely (WRONG)
>
> User correction: 'The guides should require my express sign off on ALL checklist items'"

**Source File:** `feature_02_score_penalty_application/lessons_learned.md` - Critical Mistake 1

**Root Cause:**
Agent conflated "investigation complete" with "question resolved" and marked checklist items as RESOLVED without explicit user approval. Missing the key distinction that research findings ≠ user approval.

**Affected Guide(s):**
- `stages/s2/s2_p3_refinement.md` - Critical Rules section

**Current State (BEFORE):**
```markdown
## 🛑 Critical Rules

```
┌─────────────────────────────────────────────────────────────────┐
│ CRITICAL RULES FOR S2.P3                                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ 1. ⚠️ ZERO AUTONOMOUS RESOLUTION                                │
│    - Ask user for ALL decisions                                  │
│    - No assumptions or inferences                                │
│    - When in doubt, create a checklist question                  │
│                                                                  │
```
```

**Proposed Change (AFTER):**
```markdown
## 🛑 Critical Rules

```
┌─────────────────────────────────────────────────────────────────┐
│ CRITICAL RULES FOR S2.P3                                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ 1. ⚠️ ZERO AUTONOMOUS RESOLUTION                                │
│    - Ask user for ALL decisions                                  │
│    - No assumptions or inferences                                │
│    - When in doubt, create a checklist question                  │
│                                                                  │
│ 1.5. ⚠️ INVESTIGATION COMPLETE ≠ QUESTION RESOLVED              │
│    - Agent investigates → Status: PENDING USER APPROVAL          │
│    - User explicitly approves → Status: RESOLVED                 │
│    - NEVER mark questions as resolved without explicit approval  │
│    - Research findings ≠ User approval                           │
│                                                                  │
│    WRONG: Investigate → Mark RESOLVED → Add requirement          │
│    CORRECT: Investigate → Mark PENDING → User approves →         │
│              Mark RESOLVED → Add requirement                     │
│                                                                  │
```
```

**Rationale:**
Adds explicit rule preventing agents from marking checklist items as RESOLVED after investigation. The before/after comparison makes it clear that "investigation complete" and "question resolved" are two different states requiring different status markers.

**Impact Assessment:**
- **Who benefits:** All agents in S2.P3 (Refinement phase) handling checklist questions
- **When it helps:** When agents complete investigations and need to present findings to user
- **Severity if unfixed:** High - agents may autonomously resolve questions and add unapproved requirements to specs, violating zero autonomous resolution principle and potentially implementing wrong solutions

**User Decision:** [x] Approve  [ ] Modify  [ ] Reject  [ ] Discuss

**User Feedback/Modifications:**
```
(User response here)
```

---

### Proposal P1-2: Update Checklist Template with Role Definitions

**Lesson Learned:**
> "User correction: 'The guides should require my express sign off on ALL checklist items'
>
> Root Cause Analysis:
> 1. Overconfidence after research - Finding an answer made me feel the question was 'done'
> 2. Conflated 'investigation complete' with 'question resolved'
> 3. Misunderstanding of agent vs user roles"

**Source File:** `feature_02_score_penalty_application/lessons_learned.md` - Critical Mistake 1

**Root Cause:**
Agent misunderstood the boundary between agent role (investigate, present findings) and user role (review findings, make decisions, approve). Checklist template doesn't clearly define these roles at the top of the file.

**Affected Guide(s):**
- `templates/feature_checklist_template.md` - Top of file (before questions section)

**Current State (BEFORE):**
```markdown
# Feature Checklist: {feature_name}

**Part of Epic:** {epic_name}
**Feature Number:** {N}
**Created:** {YYYY-MM-DD}

---

## Purpose

This checklist tracks open questions and decisions needed from the user during feature specification (S2) and implementation planning (S5).

**Status Definitions:**
- **OPEN** - Question not yet investigated
- **PENDING USER APPROVAL** - Agent investigated, awaiting user decision
- **RESOLVED** - User approved, answer incorporated into spec/plan
```

**Proposed Change (AFTER):**
```markdown
# Feature Checklist: {feature_name}

**Part of Epic:** {epic_name}
**Feature Number:** {N}
**Created:** {YYYY-MM-DD}

---

## 🚨 CRITICAL: Agent vs User Roles

**Agent Role:**
- Create questions based on spec gaps
- Investigate comprehensively
- Present findings clearly
- Mark status as PENDING USER APPROVAL

**User Role:**
- Review agent findings
- Make decisions
- Ask follow-up questions
- Approve resolutions (explicit "approved" required)

**AGENTS CANNOT:**
- ❌ Mark questions as RESOLVED (only users can)
- ❌ Assume approval (even if answer seems obvious)
- ❌ Add requirements based on unapproved answers
- ❌ Skip waiting for user sign-off

**Status Progression:**
1. Question added → OPEN
2. Agent investigates → PENDING USER APPROVAL
3. User approves → RESOLVED (agent marks after explicit approval)

---

## Purpose

This checklist tracks open questions and decisions needed from the user during feature specification (S2) and implementation planning (S5).

**Status Definitions:**
- **OPEN** - Question not yet investigated
- **PENDING USER APPROVAL** - Agent investigated, awaiting user decision
- **RESOLVED** - User approved, answer incorporated into spec/plan
```

**Rationale:**
Adding role definitions at the top of checklist template makes it impossible for agents to miss the boundary between investigation (agent's job) and approval (user's job). The "AGENTS CANNOT" section uses direct anti-patterns from this epic's experience.

**Impact Assessment:**
- **Who benefits:** All agents using checklist files (S2, S5)
- **When it helps:** Every time an agent needs to mark a checklist item status
- **Severity if unfixed:** High - agents will continue making autonomous resolution mistakes if role boundaries aren't crystal clear in the file they're actively editing

**User Decision:** [x] Approve  [ ] Modify  [ ] Reject  [ ] Discuss

**User Feedback/Modifications:**
```
(User response here)
```

---

### Proposal P1-3: Add Investigation Scope Checklist to S2 Guides

**Lesson Learned:**
> "User asked: 'ensure that the simulation works still after the parameter is introduced'
>
> My initial investigation:
> - ✅ Checked where simulations call score_player()
> - ❌ Didn't check ConfigManager instantiation
>
> User follow-up: 'What about when ConfigManagers are created? Investigate if there will be any issues when *reading* the config json files'
>
> Root Cause: Narrow interpretation - User said 'parameter' → I only checked parameter passing. Lack of systematic investigation framework - No mental checklist."

**Source File:** `feature_02_score_penalty_application/lessons_learned.md` - Critical Mistake 2

**Root Cause:**
Agent checked method calls but missed configuration loading. Investigation scope was too narrow because there was no systematic framework to ensure all categories were covered.

**Affected Guide(s):**
- `stages/s2/s2_p3_refinement.md` - Phase 6 (Acceptance Criteria) section

**Current State (BEFORE):**
```markdown
### Phase 6: Develop Acceptance Criteria

**Purpose:** Define measurable success criteria for feature completion

**Actions:**

6a. **Review requirements list** from spec.md

6b. **For each requirement, define acceptance criteria:**
```

**Proposed Change (AFTER):**
```markdown
### Phase 6: Develop Acceptance Criteria

**Purpose:** Define measurable success criteria for feature completion

**Actions:**

6a. **Review requirements list** from spec.md

6b. **When user requests investigation (e.g., "check compatibility"), use systematic framework:**

**Comprehensive Investigation Checklist:**

**Category 1: Method/Function Calls**
- Where does X call the new code?
- Do they pass new parameters?
- Are default values correct?

**Category 2: Configuration/Data Loading** ⚠️ (commonly missed)
- Where does X create ConfigManager/DataManager?
- How does it load new config keys?
- What if JSON missing keys?

**Category 3: Integration Points**
- Does new code affect X's flow?
- Other X files affected?

**Category 4: Timing/Dependencies**
- Transition period issues?
- Implementation sequencing?

**Category 5: Edge Cases**
- Old config with new code?
- New config with old code?

**After investigation:**
- Mark checklist status: PENDING USER APPROVAL
- Present findings covering ALL 5 categories
- Wait for explicit user approval
- ONLY THEN mark as RESOLVED

6c. **For each requirement, define acceptance criteria:**
```

**Rationale:**
Provides agents with a systematic 5-category checklist to prevent narrow investigation scope. The warning on Category 2 highlights the specific category that was missed in this epic (config/data loading).

**Impact Assessment:**
- **Who benefits:** All agents in S2.P3 investigating compatibility/integration questions
- **When it helps:** When user asks "check if this works with X" or "ensure compatibility with Y"
- **Severity if unfixed:** Medium-High - agents will continue doing narrow investigations and missing important categories, requiring user to ask follow-up questions

**User Decision:** [x] Approve  [ ] Modify  [ ] Reject  [ ] Discuss

**User Feedback/Modifications:**
```
(User response here)
```

---

### Proposal P1-4: Add Status Progression Examples to S2.P2 Guide

**Lesson Learned:**
> "What Should Have Happened:
>
> Correct workflow:
> 1. User asks for simulation compatibility check
> 2. Agent adds Question 1 to checklist (status: OPEN)
> 3. Agent investigates comprehensively
> 4. Agent presents findings (status: PENDING USER APPROVAL)
> 5. User reviews, asks follow-ups
> 6. Agent investigates follow-ups
> 7. User says 'approved'
> 8. ONLY THEN agent marks as RESOLVED
> 9. Agent adds requirement with source: 'User Answer to Question 1'"

**Source File:** `feature_02_score_penalty_application/lessons_learned.md` - Critical Mistake 1

**Root Cause:**
Agent didn't understand the correct multi-step workflow for checklist question resolution. The S2.P2 guide doesn't show this step-by-step progression clearly.

**Affected Guide(s):**
- `stages/s2/s2_p2_specification.md` - Section after Gate 2 (Spec-to-Epic Alignment)

**Current State (BEFORE):**
```markdown
**After Gate 2 passes:**
- spec.md is complete and aligned with epic
- checklist.md has questions for user (if any)
- Ready to present to user for Gate 3 (User Checklist Approval)
```

**Proposed Change (AFTER):**
```markdown
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
```
Agent: "I investigated. Question 1 is now RESOLVED. Added Requirement 9."
```

**CORRECT:**
```
Agent: "I investigated. My findings: [details]. Status: PENDING USER APPROVAL. What do you think?"
User: "Approved"
Agent: "Marking Question 1 as RESOLVED. Adding Requirement 9 with source 'User Answer to Question 1'."
```
```

**Rationale:**
Shows the exact 9-step workflow with before/after conversation examples. Makes it impossible to miss that step 7 (user says "approved") must happen before step 8 (mark RESOLVED).

**Impact Assessment:**
- **Who benefits:** All agents in S2.P2 (Specification) handling user questions
- **When it helps:** When user asks for investigations during spec review
- **Severity if unfixed:** High - without seeing the correct multi-step workflow, agents will continue jumping from "investigation complete" to "mark RESOLVED" without user approval

**User Decision:** [x] Approve  [ ] Modify  [ ] Reject  [ ] Discuss

**User Feedback/Modifications:**
```
(User response here)
```

---

### Proposal P1-5: Add Anti-Pattern Examples to CLAUDE.md

**Lesson Learned:**
> "Prevention Strategies:
>
> For agents:
> 1. ALWAYS use 'PENDING USER APPROVAL' status after investigation
> 2. Never mark questions resolved without explicit user approval
> 3. Two-step process:
>    - Step 1: Investigate → Present → Mark PENDING
>    - Step 2: User approves → Update spec → Mark RESOLVED"

**Source File:** `feature_02_score_penalty_application/lessons_learned.md` - Critical Mistake 1

**Root Cause:**
CLAUDE.md has general "zero autonomous resolution" rule but doesn't show concrete anti-pattern examples. Adding specific wrong/correct examples helps agents recognize the pattern in their own work.

**Affected Guide(s):**
- `CLAUDE.md` (root) - After "Key Principles" section

**Current State (BEFORE):**
```markdown
## Key Principles

- **Epic-first thinking**: Top-level work unit is an epic (collection of features)
- **Mandatory reading protocol**: ALWAYS read guide before starting each guide
- **Phase transition prompts**: MANDATORY acknowledgment (proves guide was read)
- **User approval gates**: Gates 3, 4.5, 5 (early approval prevents rework)
- **Zero autonomous resolution**: Agents create QUESTIONS, user provides ANSWERS
- **Continuous alignment**: S8.P1 updates specs after each feature
```

**Proposed Change (AFTER):**
```markdown
## Key Principles

- **Epic-first thinking**: Top-level work unit is an epic (collection of features)
- **Mandatory reading protocol**: ALWAYS read guide before starting each guide
- **Phase transition prompts**: MANDATORY acknowledgment (proves guide was read)
- **User approval gates**: Gates 3, 4.5, 5 (early approval prevents rework)
- **Zero autonomous resolution**: Agents create QUESTIONS, user provides ANSWERS
- **Continuous alignment**: S8.P1 updates specs after each feature

---

## Common Anti-Patterns to Avoid

### Anti-Pattern 1: Autonomous Checklist Resolution

**WRONG WORKFLOW:**
1. User asks question
2. Agent investigates
3. Agent marks question as RESOLVED
4. Agent adds requirement to spec
5. User sees requirement added without approval

**CORRECT WORKFLOW:**
1. User asks question
2. Agent investigates
3. Agent marks question as PENDING USER APPROVAL
4. Agent presents findings
5. User says "approved"
6. ONLY THEN agent marks RESOLVED and adds requirement

**Key Distinction:** Research findings ≠ User approval

**Example from KAI-6:**
- ❌ WRONG: "I checked simulations. Question 1 RESOLVED. Added Requirement 9."
- ✅ CORRECT: "I checked simulations. My findings: [details]. Status: PENDING. Approve?"

### Anti-Pattern 2: Narrow Investigation Scope

**WRONG APPROACH:**
1. User asks "check if this works with simulations"
2. Agent checks method calls only
3. Agent declares investigation complete
4. User asks "what about config loading?"
5. Agent realizes investigation was incomplete

**CORRECT APPROACH:**
1. User asks "check if this works with simulations"
2. Agent uses systematic 5-category checklist:
   - Category 1: Method/function calls ✓
   - Category 2: Configuration/data loading ✓
   - Category 3: Integration points ✓
   - Category 4: Timing/dependencies ✓
   - Category 5: Edge cases ✓
3. Agent presents comprehensive findings covering all categories
4. User approves once (not multiple follow-ups needed)

**Key Distinction:** Use systematic frameworks, don't rely on intuition

**When investigating compatibility/integration:**
- DON'T check just the most obvious aspect
- DO use 5-category investigation checklist (see S2.P3 guide)
- DON'T assume first answer is complete
- DO ask "what else?" at least 3 times

---
```

**Rationale:**
Adds concrete examples of the two anti-patterns discovered in this epic directly to CLAUDE.md where all agents read during onboarding. The side-by-side wrong/correct workflows make patterns immediately recognizable.

**Impact Assessment:**
- **Who benefits:** All agents across all stages (CLAUDE.md is foundational document)
- **When it helps:** During S2 (checklist questions) and any investigation task
- **Severity if unfixed:** High - without concrete anti-pattern examples in CLAUDE.md, agents may read "zero autonomous resolution" but not recognize they're violating it until user corrects them

**User Decision:** [x] Approve  [ ] Modify  [ ] Reject  [ ] Discuss

**User Feedback/Modifications:**
```
(User response here)
```

---

## Lessons Not Resulting in Proposals

### Feature 01: Pre-Existing Test Failures

**Lesson:**
> "Pre-existing test failures can block workflow stages that require 100% test pass rate"

**Why no proposal:**
- This is project-specific (test_root_scripts.py referenced non-existent file)
- Not a guide gap (S7.P1 correctly required 100% pass rate)
- Workflow functioned as designed (caught issue before proceeding)
- Solution is project maintenance, not guide change

---

## Decision Summary

**Total Proposals:** 5
- **P0 (Critical):** 0 proposals
- **P1 (High):** 5 proposals
- **P2 (Medium):** 0 proposals
- **P3 (Low):** 0 proposals

**Decisions Made:**
- Approved: 5 / 5
- Modified: 0 / 5
- Rejected: 0 / 5

**Status:** APPLIED (2026-01-15)

---

## Next Steps

After user reviews all proposals:
1. Apply approved changes to guides
2. Apply modified proposals with user's alternative text
3. Skip rejected proposals
4. Create separate commit for guide updates
5. Update reference/guide_update_tracking.md
6. Proceed to S10 STEP 5 (Final Commit & Pull Request)

---

**Proposal Created:** 2026-01-15
**Agent:** Claude Code (Sonnet 4.5)
