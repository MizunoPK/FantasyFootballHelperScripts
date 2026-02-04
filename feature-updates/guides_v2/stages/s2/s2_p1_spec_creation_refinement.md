# S2.P1: Spec Creation and Refinement (3 Iterations)

🚨 **MANDATORY READING PROTOCOL**

**Before starting this phase:**
1. Use Read tool to load THIS ENTIRE GUIDE
2. Verify prerequisites (S1 complete, feature folder exists)
3. Update feature README.md Agent Status with guide name + timestamp

---

## Quick Start

**Purpose:** Research feature, create spec.md and checklist.md, get user approval (Gate 3)

**Structure:** 3 iterations
- S2.P1.I1: Feature-Level Discovery (60-90 min) - Embeds Gate 1
- S2.P1.I2: Checklist Resolution (45-90 min)
- S2.P1.I3: Refinement & Alignment (30-60 min) - Embeds Gate 2, includes Gate 3

**Time:** 2.25-4 hours per feature
**Prerequisites:** S1 complete, DISCOVERY.md exists, feature folder created

---

## S2.P1.I1: Feature-Level Discovery (60-90 min)

### Purpose
Research feature, draft spec.md and checklist.md, validate with Validation Loop (embeds Gate 1)

### Steps

**1. Read Discovery Context (5-10 min)**
- Read `DISCOVERY.md` from S1.P3
- Identify feature-specific sections
- Note integration points

**2. Reference Previously Completed Features (5-10 min)**
- Read spec.md files from ALL previously completed features
- Check alignment opportunities (naming, patterns, approaches)
- Identify potential conflicts early
- Document alignment decisions

**3. Targeted Research (20-30 min)**
- Search for related code (Glob, Grep)
- **USE READ TOOL** to read existing implementations
- **Verify External Library Compatibility** (if feature uses external APIs/libraries):
  - Test libraries with mock data BEFORE writing spec
  - Check: endpoint override support, mock compatibility, test environment compatibility
  - Document compatibility or workarounds needed
  - Time investment: 15-20 min per library (saves 2+ hours debugging later)
- Document findings in research notes

**4. Draft Spec & Checklist (20-30 min)**
- Create `feature_XX_name/spec.md` (initial draft with Discovery Context)
- Create `feature_XX_name/checklist.md` (QUESTIONS ONLY - agents NEVER mark [x])
- Include requirement traceability (link to epic requirements)

**5. Document Research Findings (5-10 min)** - **MANDATORY**
- Create `feature_XX_name/RESEARCH_NOTES.md` (REQUIRED for all features)
- Include: code locations found, integration points, compatibility findings, open questions
- **Optional exception:** Features with <3 requirements AND no external dependencies may skip
- When in doubt, create research notes (better to have than not)

**6. Validation Loop Validation (15-30 min)** - **EMBEDS GATE 1**

**Reference:** `reference/validation_loop_discovery.md`

- **Round 1:** Check spec completeness, checklist coverage
  - **Gate 1 Check (Research Completeness Audit):**
    - Category 1: Can cite EXACT files/classes to modify (with line numbers)?
    - Category 2: Have READ source code (actual method signatures)?
    - Category 3: Have verified data structures from source?
    - Category 4: Have reviewed DISCOVERY.md for context?
  - All 4 categories must pass with evidence
- **Round 2:** Fresh review with different patterns, find new issues
- **Round 3:** Final validation
- **Exit:** 3 consecutive clean rounds (Gate 1 passed as part of validation)

**Outputs:**
- spec.md (draft, validated, Discovery Context included)
- checklist.md (QUESTIONS ONLY)
- RESEARCH_NOTES.md (REQUIRED, with rare exceptions documented above)

**Gates Embedded:**
- Gate 1: Research Completeness Audit (embedded in Validation Loop Round 1)

---

## S2.P1.I2: Checklist Resolution (45-90 min)

### Purpose
Present checklist to user, resolve questions one-at-a-time, update spec

### Steps

**1. Present Checklist to User (5 min)**
- Show checklist.md
- Explain: "These are questions I need answered to finalize the spec"
- Ask: "Ready to resolve these?"

**2. One-at-a-Time Resolution (30-60 min)**
- For each question in checklist:
  - Present question + context
  - Wait for user answer
  - **Use "Correct Status Progression" protocol** (see below)
  - Update spec.md immediately with answer
- **CRITICAL:** Do NOT batch questions
- **CRITICAL:** Do NOT mark [x] autonomously

**3. Update Spec with Answers (10-20 min)**
- Incorporate all user answers into spec.md
- Maintain traceability (link questions to requirements)
- Update checklist.md status (ANSWERED, not [x] yet)

### "Correct Status Progression" Protocol (9 steps)

**This protocol prevents autonomous question resolution:**

1. User asks question (e.g., "check simulation compatibility")
2. Agent adds question to checklist → Status: OPEN
3. Agent investigates comprehensively (use 5-category checklist: method calls, config loading, integration points, timing/dependencies, edge cases)
4. Agent presents findings → Status: PENDING USER APPROVAL
5. User reviews findings, may ask follow-ups
6. Agent investigates follow-ups (if any)
7. User says "approved" or "looks good" (explicit approval required)
8. **ONLY THEN** agent marks → Status: RESOLVED
9. Agent adds requirement to spec with source: "User Answer to Question N"

**Key Principle:** Investigation complete ≠ Question resolved. Always wait for explicit user approval before marking RESOLVED.

**Example:**
```
❌ WRONG:
- Agent: "I checked simulations. Question 1 RESOLVED. Added Requirement 9."

✅ CORRECT:
- Agent: "I checked simulations. My findings: [details]. Status: PENDING. Do you approve?"
- User: "Yes, approved"
- Agent: "Question 1 marked RESOLVED. Adding Requirement 9 to spec."
```

**Outputs:**
- spec.md (updated with user answers)
- checklist.md (all questions marked ANSWERED)

---

## S2.P1.I3: Refinement & Alignment (30-60 min)

### Purpose
Validate spec completeness, check per-feature alignment, get Gate 3 user approval

### Steps

**1. Per-Feature Alignment Check (10-15 min)**
- Read spec.md files from ALL previously completed features
- Compare against current feature's spec.md
- **Cross-Reference Checklist Questions** (for Group 2+ features):
  - If prior features answer question consistently → DELETE from checklist, document as "Aligned with Features X-Y"
  - If prior features answer inconsistently → Escalate to Primary (if parallel mode)
  - If prior features don't answer → KEEP question
- Check for: naming conflicts, approach conflicts, data structure conflicts
- Document any conflicts found
- Update current spec if needed

**1.5. Agent-to-Agent Issue Reporting (parallel mode only)**

**If working in parallel mode and issues found in OTHER features:**

Create message: `agent_comms/{YOUR_ID}_to_{PRIMARY_ID}.md`

Format:
```markdown
⏳ UNREAD

**From:** Secondary Agent {YOUR_ID}
**To:** Primary Agent {PRIMARY_ID}
**Date:** {timestamp}
**Type:** Cross-Feature Issue

## Issue Found

**Feature:** Feature {N} {name}
**Issue Type:** [Naming Conflict | Approach Conflict | Data Structure Conflict]
**Description:** [Detailed description]

**Affected Files:**
- feature_{M}_{your_feature}/spec.md (your feature)
- feature_{N}_{other_feature}/spec.md (other feature with issue)

**Recommended Resolution:** [Your suggestion]

**Priority:** [HIGH | MEDIUM | LOW]
```

Primary agent reviews during coordination heartbeat (every 15 minutes).

**If NOT in parallel mode:** Document issues in notes, fix in S2.P2

**2. Validation Loop Validation (15-30 min)** - **EMBEDS GATE 2**

**Reference:** `reference/validation_loop_spec_refinement.md`

- **Round 1:** Sequential read, requirement traceability check
  - **Gate 2 Check (Spec-to-Epic Alignment):**
    - Every requirement has source (Epic/User Answer/Derived)?
    - No scope creep (nothing user didn't ask for)?
    - No missing requirements (everything user asked for is included)?
    - All requirements trace to validated sources?
    - Zero assumptions in spec?
  - All criteria must pass
- **Round 2:** Read in reverse order, gap detection
- **Round 3:** Random requirement spot-checks, alignment with DISCOVERY.md
- **Exit:** 3 consecutive clean rounds (Gate 2 passed as part of validation)

**3. If Gaps Found During Validation Loop - LOOP-BACK MECHANISM**
- Add new questions to checklist.md
- **LOOP BACK to S2.P1.I2** (Checklist Resolution)
- Resolve new questions with user
- **RESTART S2.P1.I3 from beginning** (fresh Validation Loop)
- Continue until Validation Loop passes with NO gaps

**4. Dynamic Scope Adjustment (5-10 min if needed)**
- Count checklist.md items
- If >35 items: Propose feature split to user
- Get user approval before proceeding

**4.5. Create Acceptance Criteria Section (5-10 min)** - **MANDATORY BEFORE GATE 3**
- Add "Acceptance Criteria" section to spec.md
- For each requirement, define measurable success criteria
- Define "Done" for each requirement
- Clear pass/fail conditions

**5. Gate 3: User Checklist Approval (5-10 min)** - **SEPARATE FROM VALIDATION LOOP**
- Present final spec.md to user (including Acceptance Criteria)
- Present final checklist.md (all ANSWERED)
- **Explicitly state:** "Please approve this spec.md (including the Acceptance Criteria section) and checklist.md"
- Ask: "Approve this feature specification?"
- **MANDATORY GATE:** Cannot proceed without approval
- Mark checklist items [x] ONLY AFTER user approves

**If User Requests Changes:**
- Update spec.md based on user feedback
- **LOOP BACK to S2.P1.I3 Step 2** (Validation Loop)
- Re-validate spec with fresh Validation Loop
- Re-present to user for approval
- Continue until user explicitly approves (no changes requested)

**If User Rejects Entire Approach:**
- User says: "This entire approach is wrong, start over"
- **STOP - Do not loop back to I3**
- Options:
  - (A) **Loop back to S2.P1.I1** (re-do research with different approach)
  - (B) **Escalate to S1** (re-do Discovery Phase if fundamental misunderstanding)
- Ask user: "Should I re-do research (S2.P1.I1) or return to Discovery Phase (S1.P3)?"
- Await user decision

**Outputs:**
- spec.md (final, user-approved, aligned with previous features, with acceptance criteria)
- checklist.md (final, user-approved, all marked [x])

**Exit Condition:**
- User explicitly approves spec (including acceptance criteria)
- Gate 3 passed

**Secondary Agent Behavior:**
```
**If Secondary Agent:**
- Stop after S2.P1.I3 completes (Validation Loop passes + Gate 3 approved)
- Do NOT proceed to S2.P2 (only Primary runs S2.P2)
- Report to Primary: "S2.P1 complete for Feature XX"
- Update STATUS file: READY_FOR_SYNC = true
- Wait for Primary to run S2.P2 and S3
```

---

## Completion Criteria

**S2.P1 complete when ALL true:**

□ I1 complete (spec drafted, research notes created, Gate 1 passed)
□ I2 complete (all checklist questions resolved with user)
□ I3 complete (Gate 2 passed, Gate 3 passed)
□ spec.md finalized and user-approved
□ checklist.md all items marked [x] (after user approval)
□ RESEARCH_NOTES.md exists
□ Feature README.md updated with S2.P1_COMPLETE status

---

## Next: S2.P2 (Primary Agent Only)

**After S2.P1 complete:**

- **If Secondary Agent:** STOP, wait for Primary to run S2.P2
- **If Primary Agent:** Continue to S2.P2 after ALL features in group complete S2.P1

📖 **READ:** `stages/s2/s2_p2_cross_feature_alignment.md`

---

*End of s2_p1_spec_creation_refinement.md*
