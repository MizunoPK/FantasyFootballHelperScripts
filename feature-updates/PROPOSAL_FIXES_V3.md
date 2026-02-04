# Guide Update Proposals (V3 - ALL ROUNDS 3-11 ISSUES FIXED)

**Date:** 2026-02-03
**Source:** my_memory.md (authoritative), with user clarifications from Rounds 1-11
**Status:** Ready for user approval and implementation
**Changes from V2:** Fixed all issues from Rounds 3-11 Consistency Loop (23 issues total + 1 design decision documented)

---

## Summary of All Corrections

### Round 1 Fixes (20 issues):
1-20. ✅ All issues from initial consistency review incorporated

### Round 2 Fixes (10 issues):
21-31. ✅ All issues from Round 2 incorporated

### Round 3 Fixes (13 issues):
32. ✅ Added fix-introduces-issue example (Proposal 1)
33. ✅ Made acceptance criteria approval explicit (Proposal 4, S2.P1.I3)
34. ✅ Specified pairwise comparison matrix file location (Proposal 4, S2.P2)
35. ✅ Fixed S5 renumbering math (Proposal 7)
36. ✅ Clarified Gates 4a/7a fate (Proposal 7)
37. ✅ Added maximum round limit for stuck loops (Proposal 1)
38. ✅ Added total spec rejection handling (Proposal 4, Gate 3)
39. ✅ Added missing test_strategy.md error handling (Proposal 7, S5.P1.I1)
40. ✅ Clarified research notes requirement (Proposal 4, S2.P1.I1)
41. ✅ Added "Correct Status Progression" protocol (Proposal 4, S2.P1.I2)
42. ✅ Added agent-to-agent communication protocol (Proposal 4, S2.P1.I3)
43. ✅ Expanded S3.P1 with detail from current S4 (Proposal 5)
44. ✅ Specified test_strategy_template.md content requirements (Proposal 10)

### Round 4 Fix (1 minor gap):
45. ✅ Added test_strategy.md content validation (Proposal 7, S5.P1.I1 - enhances Issue #39)

### Round 5 Fix (1 issue):
46. ✅ Added Gate 4.5 rejection handling (Proposal 5, S3.P3 - consistency with Gate 3)

### Round 5 Deferred (1 design decision):
47. 📋 Post-approval spec changes - DOCUMENTED AS DESIGN DECISION (user reviews at Gate 4.5)

### Round 6 Fixes (3 issues):
48. ✅ Added Gate 5 definition with rejection handling (Proposal 7, after Round 3 Consistency Loop - consistency with Gates 3 & 4.5)
49. ✅ Clarified Round 3 final iteration sequence (Proposal 7, Round 3 exit - now lists I23, I25, I24, Gate 5)
50. ✅ Added Proposal 9 complete section (CLAUDE.md updates with all stage redesign changes)

### Round 7 Fixes (3 issues):
51. ✅ Removed duplicate Proposal 9 section (old incomplete version at lines 1754-1829 - kept new comprehensive version)
52. ✅ Fixed Phase 1 time estimate (was 3-4h, corrected to 5-8h to match Proposals 1+2)
53. ✅ Fixed Phase 4 time estimate (was 2-4h, corrected to 3-5h to match Proposals 3+8+10)

### Round 8 Fix (1 issue):
54. ✅ Added "Why" section to Proposal 10 (structural consistency - all proposals now have explicit rationale)

### Rounds 9-10:
- Round 9: CLEAN (0 issues found) ✅
- Round 10: CLEAN (0 issues found) ✅

### Round 11 Fix (1 issue):
55. ✅ Updated "Next Steps" section to reference ALL Rounds 3-8 fixes (was outdated, only mentioned Round 3)

---

## PROPOSAL 1: Create Consistency Loop Master Protocol

### What
Create a master Consistency Loop protocol file that defines the core protocol, which other guides will reference and adapt to their specific contexts.

### Why (From User Memory)
"We want a Consistency Loop protocol that is referenced and treated as the master version, then any places that use the protocol should define *how* they use the protocol."

**Core Protocol Requirements:**
- Assume everything created/updated is completely wrong, inconsistent, full of gaps
- Re-read document/code with fresh eyes each loop (no previous biases)
- Research to ensure nothing left out
- Continue until **3 consecutive loops with NO issues/gaps**
- **Accept NO deferred issues** - ALL identified issues must be addressed
- Each context defines HOW they apply the protocol optimally

### Audit Evidence
✅ **100% CONFIRMED** - consistency_loop_qc_pr.md found with 12 references (Round 13:102-110)

### Files Affected
**CREATE:**
1. `consistency_loop_protocol.md` - Master protocol
   - Location: `feature-updates/guides_v2/reference/`

### File Content Outline

```markdown
# Consistency Loop Protocol (Master)

## Purpose
Systematic validation requiring 3 consecutive clean rounds with zero deferred issues.

## Core Principles

1. **Assume Everything is Wrong**
   - Start each round assuming document/code is completely wrong
   - Look for: inconsistencies, gaps, missing information, errors

2. **Fresh Eyes Each Round**
   - Take 2-5 minute break between rounds (clear mental model)
   - Do NOT rely on memory from previous round
   - Approach each round as if reading for first time

3. **Explicit Re-Reading Required**
   - Must physically re-read the document/code (not work from memory)
   - Use Read tool for each round
   - Cannot skip re-reading

4. **Research to Fill Gaps**
   - If gaps found, research to fill them
   - Verify against source materials (DISCOVERY.md, epic notes, code)
   - Don't guess - look it up

5. **Exit: 3 Consecutive Clean Loops**
   - Must have 3 consecutive rounds with ZERO issues/gaps
   - NOT cumulative, CONSECUTIVE
   - If Round 5 finds issues, need Rounds 6, 7, 8 all clean

6. **No Deferred Issues**
   - ALL identified issues must be addressed immediately
   - Cannot defer issues for "later" or "future iteration"
   - Cannot mark issues as "low priority" to skip fixing
   - If issue found in Round N, fix it before Round N+1
   - Only exit when ZERO issues remain (not "acceptable number")
   - "Good enough" is never good enough - aim for zero defects

**Why This Principle:**
- Deferred issues accumulate into technical debt
- "Later" never comes - issues compound
- Small issues become big bugs
- Quality cannot be retrofitted
- User requested: "Accept no deferred issues"

**What "No Deferred" Means:**
- Round 1 finds 5 issues → Fix ALL 5 before Round 2
- Round 2 finds 2 issues → Fix ALL 2 before Round 3
- Round 3 finds 1 issue → Loop back, fix it, restart count
- Cannot proceed with known issues (no matter how minor)

**Important Note About Fixes:** - **FIX FOR ISSUE #32**
Fixing an issue can introduce new issues. This is expected and handled by the protocol:

**Example:**
```
Round 1: Find typo in spec.md requirement R1 → Fix typo
Round 2: Re-read spec → Notice R1 fix made it contradict R2 → This is a NEW issue
Round 2 outcome: 1 issue found (R1/R2 contradiction)
Action: Fix contradiction before Round 3, reset counter to 0
Round 3: Re-read spec → Check if fix introduced other issues
```

**Key Insight:** The "restart counter" behavior handles fix-induced issues naturally. Don't be discouraged if fixes introduce new issues - that's why we have multiple rounds with fresh eyes.

7. **Maximum Round Limit (Safety Mechanism)** - **FIX FOR ISSUE #37**

**Escalation Protocol for Stuck Loops:**
If Consistency Loop exceeds 10 rounds without achieving 3 consecutive clean loops:
1. STOP the loop
2. Document all issues found in last 3 rounds
3. Escalate to user with summary:
   - "I've completed 10+ rounds of validation"
   - "Issues continue to be found: [list recurring pattern]"
   - "I need help deciding how to proceed"
4. Await user guidance

**Rationale:**
- 10 rounds = ~2-3 hours of validation work
- If issues persist after 10 rounds, there's likely a fundamental problem
- Human judgment needed to assess: architecture issue? scope issue? misunderstanding?
- Prevents infinite loops and wasted agent time

**User Options After Escalation:**
- Adjust scope/approach
- Accept current state (override "no deferred" for specific issues)
- Return to earlier stage (S1 Discovery, S2 Research, etc.)
- Provide additional context/clarification

## Embedded Gates Explanation

**What "Embedded" Means Operationally:**

When a gate is "embedded" in a Consistency Loop, the gate criteria become issue types that the loop checks for:

- **Gate criteria failures = Issues found**
- **If gate check fails in Round 1 → Fix → Continue loop**
- **Exit requires gate criteria passing (not separate checkpoint)**

**Example - Gate 1 Embedded in S2.P1.I1:**
- Round 1 checks: Gate 1 criteria (can cite files? read code? verified structures?)
- If any Gate 1 criterion fails → Issue found → Fix it
- Round 2 checks Gate 1 again (along with other issues)
- Exit requires: Gate 1 passes + no other issues + 3 consecutive clean

**Contrast with Separate Gate:**
- **Embedded gate:** Validation dimension within loop
- **Separate gate:** Explicit STOP point requiring user approval
- Gate 3 (User Approval) stays separate (requires user decision)
- Gates 1 & 2 become embedded (agent validates during loop)

## The 3-Round Loop

### Round 1: Initial Validation
**Goal:** Find obvious issues

**Process:**
1. Re-read document/code completely
2. Check for completeness, consistency, gaps
3. Document ALL issues found
4. Report: "Round 1: N issues found"

**If N > 0:** Fix ALL issues (no deferring), proceed to Round 2
**If N = 0:** Proceed to Round 2 anyway (need 3 consecutive clean)

### Round 2: Different Perspective
**Goal:** Find issues missed in Round 1

**Process:**
1. Take 2-5 minute break (clear mental model)
2. Re-read ENTIRE document/code (not just fixed sections)
3. Use DIFFERENT search/reading patterns than Round 1
4. Look for NEW issues (not just verify fixes)
5. Document ALL issues found
6. Report: "Round 2: N issues found"

**If N > 0:** Fix ALL issues (no deferring), proceed to Round 3
**If N = 0:** Proceed to Round 3 anyway (need 3 consecutive clean)

### Round 3: Final Sweep
**Goal:** Confirm zero issues remain

**Process:**
1. Take 2-5 minute break (fresh perspective)
2. Re-read ENTIRE document/code again
3. Use DIFFERENT search/reading patterns than Rounds 1 & 2
4. Random spot-checks
5. Document ALL issues found
6. Report: "Round 3: N issues found"

**If N > 0:** Fix ALL issues, continue to Round 4, RESET counter to 0
**If N = 0:** Check consecutive clean count (increment by 1)

**Exit Criteria:**
- 3 consecutive rounds with ZERO new issues each
- Rounds N-2, N-1, N all found zero issues
- Only then: Mark as PASSED

### Example: Round 5 Finds Issues
```
Round 1: 5 issues → fix ALL → Round 2
Round 2: 2 issues → fix ALL → Round 3
Round 3: 0 issues → Round 4 (count = 1 clean)
Round 4: 0 issues → Round 5 (count = 2 clean)
Round 5: 1 issue → fix it → Round 6, RESET count to 0
Round 6: 0 issues → Round 7 (count = 1 clean)
Round 7: 0 issues → Round 8 (count = 2 clean)
Round 8: 0 issues → PASSED (count = 3 consecutive clean)
```

**Key:** Counter resets when ANY issues found (no matter how minor)

## Context-Specific Adaptations

Different contexts will adapt this protocol by defining:
1. **WHAT is being validated** (document, code, test plan, spec)
2. **WHAT counts as "issue"** (gaps, inconsistencies, missing requirements, etc.)
3. **WHAT patterns differ per round** (sequential read vs reverse vs spot-check)
4. **WHAT specific criteria** (Gate checklists, coverage thresholds, alignment checks)

**See context-specific guides:**
- `consistency_loop_discovery.md` - Research and discovery context
- `consistency_loop_spec_refinement.md` - Spec/document refinement context
- `consistency_loop_alignment.md` - Cross-feature/cross-doc alignment context
- `consistency_loop_test_strategy.md` - Test plan validation context
- `consistency_loop_qc_pr.md` - QC and PR validation context
```

### Estimated Time
1-2 hours

### Priority
**CRITICAL** - Foundation for all other Consistency Loop changes

---

## PROPOSAL 2: Create Consistency Loop Context-Specific Variants

### What
Create context-specific Consistency Loop guides that reference the master protocol and define HOW to apply it in different contexts.

### Why (From User Memory)
"The way that they most optimally use the fresh eyes perspectives and what they are looking for and validating may change depending on the context of the Consistency Loop."

### Audit Evidence
✅ **100% CONFIRMED** - consistency_loop_qc_pr.md exists (for QC/PR context)

### Files Affected
**CREATE:**

#### 1. consistency_loop_discovery.md
**Location:** `feature-updates/guides_v2/reference/`
**Context:** S1.P3 Discovery Phase, S2.P1.I1 Feature Discovery
**What's validated:** Discovery documents, research findings
**Fresh Eyes per round:**
- Round 1: Sequential read, completeness check
- Round 2: Different folder/file order, integration point verification
- Round 3: Random spot-checks, alignment with epic intent
**Specific criteria:**
- All components mentioned in epic are researched
- All integration points identified
- All user questions answered
- Zero assumptions remain
**What counts as "issue":**
- Missing research areas
- Unanswered questions
- Assumptions instead of verified facts
- Gaps in integration understanding

#### 2. consistency_loop_spec_refinement.md
**Location:** `feature-updates/guides_v2/reference/`
**Context:** S2.P1.I3 Spec Refinement, S3.P2 Epic Refinement
**What's validated:** Spec.md, checklist.md completeness and consistency
**Fresh Eyes per round:**
- Round 1: Sequential read, requirement traceability check
- Round 2: Read in reverse order, gap detection
- Round 3: Random requirement spot-checks, alignment with DISCOVERY.md
**Specific criteria (EMBEDS Gate 2):**
- Every requirement has source (Epic/User Answer/Derived)
- No scope creep (nothing user didn't ask for)
- No missing requirements (everything user asked for is included)
- All requirements trace to validated sources
- Zero assumptions in spec
**What counts as "issue":**
- Requirements without sources
- Scope creep items
- Missing requirements from epic
- Gaps in spec coverage
- Inconsistencies between sections
- Assumptions instead of confirmed facts

#### 3. consistency_loop_alignment.md
**Location:** `feature-updates/guides_v2/reference/`
**Context:** S2.P1.I1 per-feature alignment, S2.P1.I3 per-feature alignment, S2.P2 group alignment
**What's validated:** Cross-feature consistency, no conflicts
**Fresh Eyes per round:**
- Round 1: Pairwise comparison in feature order (F1 vs F2, F2 vs F3, etc.)
- Round 2: Pairwise comparison in reverse order (FN vs F1, F3 vs F2, etc.)
- Round 3: Random pair spot-checks, thematic clustering (all data structures, all error handling, etc.)
**Specific criteria:**
- No naming conflicts (same name, different meaning)
- No approach conflicts (contradictory implementations)
- No data structure conflicts (incompatible formats)
- Consistent patterns across features
- Integration points identified and consistent
**What counts as "issue":**
- Naming conflicts
- Contradictory approaches
- Incompatible data structures
- Pattern inconsistencies
- Integration mismatches

#### 4. consistency_loop_test_strategy.md
**Location:** `feature-updates/guides_v2/reference/`
**Context:** S3.P1 Epic Testing Strategy, S4 Feature Testing Strategy
**What's validated:** Test plans, coverage completeness
**Fresh Eyes per round:**
- Round 1: Sequential read, requirement coverage check
- Round 2: Edge case enumeration, gap identification
- Round 3: Random requirement spot-checks, integration test verification
**Specific criteria:**
- Every requirement has test coverage
- Edge cases identified and tested
- Integration points have tests
- >90% coverage planned (for feature-level)
- End-to-end scenarios complete (for epic-level)
**What counts as "issue":**
- Requirements without tests
- Missing edge cases
- Integration gaps
- Coverage below threshold
- Vague test descriptions

#### 5. consistency_loop_qc_pr.md (AUDIT CONFIRMED)
**Location:** `feature-updates/guides_v2/reference/`
**Context:** S7.P2 QC Rounds, S7.P3 PR Review, S9.P2 Epic QC Rounds
**What's validated:** Code, tests, implementation correctness
**Fresh Eyes per round:**
- Round 1: Automated tests + sequential code review
- Round 2: Different file order + manual verification patterns
- Round 3: Random file spot-checks + integration verification
**Specific criteria:**
- All tests pass (100% pass rate)
- Code matches implementation plan
- No issues found (critical, major, or minor)
- All requirements implemented
- Integration points work
**What counts as "issue":**
- Test failures
- Code not matching plan
- Bugs found during review
- Missing requirements
- Integration problems

### Estimated Time
4-6 hours (5 variants × 1 hour each, plus cross-linking)

### Priority
**HIGH** - Needed for all stage redesigns

---

## PROPOSAL 3: Update S1 Discovery Phase (S1.P3) to Use Consistency Loop

### What
Refactor S1.P3 Discovery Phase to use Consistency Loop protocol instead of the current "3 consecutive iterations with no new questions" approach.

### Why (From User Memory)
"The Discovery Phase of the initial epic planning should be turned into a Consistency Loop, where the discovery document is created then put through the consistency loop to see if any corrections or updates are needed"

### Current vs New Approach

**Current:** Iterative Q&A loop until 3 consecutive iterations with no new questions
**New:** Create DISCOVERY.md → Apply Consistency Loop → Exit when 3 consecutive loops find no issues/gaps

**Key Difference:**
- **Old exit criteria:** No new QUESTIONS (focuses on user Q&A)
- **New exit criteria:** No ISSUES/GAPS (focuses on document completeness and quality)
- **"Issues/gaps" include:** Missing research, incomplete sections, unanswered questions, assumptions, integration gaps, unclear scope

### Files Affected
**MODIFY:**
1. `stages/s1/s1_p3_discovery_phase.md`
   - Update workflow to use Consistency Loop
   - Reference `consistency_loop_discovery.md`
   - Change exit criteria from "no new questions" to "3 consecutive clean loops"
   - Keep Q&A with user during loop (when questions arise)

### Updated Workflow
```
Create DISCOVERY.md draft
  ↓
Consistency Loop Round 1:
  - Read DISCOVERY.md completely
  - Check for completeness, gaps, assumptions
  - Research any gaps found
  - Ask user questions as needed
  - Document issues found
  ↓
Fix ALL issues (no deferred) → Round 2
  ↓
Consistency Loop Round 2:
  - Re-read DISCOVERY.md with fresh eyes
  - Use different patterns (reverse order, different focus)
  - Check for NEW issues/gaps
  - Research, ask user as needed
  ↓
Fix ALL issues OR Round 3 (if zero issues)
  ↓
Consistency Loop Round 3:
  - Re-read again
  - Random spot-checks
  - Final validation
  ↓
If issues: Fix ALL, continue to Round 4, reset count
If zero issues: Check consecutive count
  ↓
Exit when 3 consecutive rounds with zero issues/gaps
```

### Estimated Time
1 hour

### Priority
**MEDIUM** - Improves S1 quality, not blocking for S2-S5 redesigns

---

## PROPOSAL 4: Redesign Stage 2 → "Feature Planning" (Two Phases, Three Iterations)

### What
Refactor S2 from 9-phase structure to **S2.P1 (3 iterations: Discovery, Checklist Resolution, Refinement)** and **S2.P2 (Cross-Feature Alignment with pairwise comparison)**.

### Why (From User Memory)
"We identified the existing S2, S3, and S4 as being large, unwieldy, and confusing. We refactored the three stages..."

**Time Tradeoff:** New S2 takes 2.25-4 hours (vs current 2-3 hours), but improves quality and clarity. User confirmed acceptable.

### Audit Evidence
✅ Gate 3 = User Checklist Approval confirmed (Audit Round 11:119-132)

### User Clarifications from Review
1. **Pairwise comparison moves to S2.P2** (not S3)
2. **Per-feature alignment stays** in S2.P1.I1 and S2.P1.I3
3. **Consistency Loops EMBED Gates 1 & 2**, Gate 3 stays separate
4. **Time increase acceptable** (quality over speed)

### Files Affected

**CREATE:**
1. **`s2_feature_planning.md`** - Main S2 guide (router)
2. **`s2_p1_spec_creation_refinement.md`** - S2.P1 complete guide
3. **`s2_p2_cross_feature_alignment.md`** - S2.P2 complete guide

**MODIFY:**
4. `s2_feature_deep_dive.md` - Update router to point to new files

### Structure Details

#### S2.P1 - Spec Creation and Refinement (Parallelizable)

##### S2.P1.I1 - Feature-Level Discovery (60-90 min)

**Purpose:** Research feature, draft spec.md and checklist.md, validate with Consistency Loop

**Steps:**

1. **Read Discovery Context** (5-10 min)
   - Read `DISCOVERY.md` from S1.P3
   - Identify feature-specific sections
   - Note integration points

2. **Reference Previously Completed Features** (5-10 min)
   - Read spec.md files from ALL previously completed features
   - Check for alignment opportunities (naming, patterns, approaches)
   - Identify potential conflicts early
   - Document alignment decisions

3. **Targeted Research** (20-30 min)
   - Search for related code (Glob, Grep)
   - Read existing implementations (USE READ TOOL)
   - **Verify External Library Compatibility** (if feature uses external APIs/libraries)
     - Test libraries with mock data or test environment BEFORE writing spec
     - Check: endpoint override support, mock response compatibility, test environment compatibility
     - Document compatibility or workarounds needed
     - Historical lesson: KAI-1 Feature 02 skipped this, cost 2 hours in S7
     - Time investment: 15-20 min per library
     - Time saved: 2+ hours debugging per incompatible library
   - Document findings in research notes

4. **Draft Spec & Checklist** (20-30 min)
   - Create `feature_XX_name/spec.md` (initial draft with Discovery Context)
   - Create `feature_XX_name/checklist.md` (QUESTIONS ONLY)
   - Include requirement traceability (link to epic requirements)

5. **Document Research Findings** (5-10 min) - **FIX FOR ISSUE #1 (CLARIFICATION)**
   - Create `feature_XX_name/RESEARCH_NOTES.md` (REQUIRED for all features)
   - Include: code locations found, integration points, compatibility findings, open questions
   - **Rationale:** Research notes provide audit trail and context for future maintenance
   - **Optional exception:** Features with <3 requirements AND no external dependencies may skip
   - When in doubt, create research notes (better to have than not)

6. **Consistency Loop Validation** (15-30 min) - **EMBEDS GATE 1**
   - Reference: `consistency_loop_discovery.md`
   - **Round 1:**
     - Check spec completeness, checklist coverage
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
- `spec.md` (draft, validated, Discovery Context included)
- `checklist.md` (QUESTIONS ONLY)
- `RESEARCH_NOTES.md` (REQUIRED, with rare exceptions documented above)

**Gates Embedded:**
- Gate 1: Research Completeness Audit (embedded in Consistency Loop Round 1)

---

##### S2.P1.I2 - Checklist Resolution (45-90 min)

**Purpose:** Present checklist to user, resolve questions one-at-a-time, update spec

**Steps:**

1. **Present Checklist to User** (5 min)
   - Show checklist.md
   - Explain: "These are questions I need answered to finalize the spec"
   - Ask: "Ready to resolve these?"

2. **One-at-a-Time Resolution** (30-60 min)
   - For each question in checklist:
     - Present question + context
     - Wait for user answer
     - **Use "Correct Status Progression" protocol** (see below)
     - Update spec.md immediately with answer
   - **CRITICAL:** Do NOT batch questions
   - **CRITICAL:** Do NOT mark [x] autonomously

3. **Update Spec with Answers** (10-20 min)
   - Incorporate all user answers into spec.md
   - Maintain traceability (link questions to requirements)
   - Update checklist.md status (ANSWERED, not [x] yet)

**"Correct Status Progression" Protocol** (9 steps) - **FIX FOR ISSUE #2**

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
- `spec.md` (updated with user answers)
- `checklist.md` (all questions marked ANSWERED)

**Anti-Patterns to Avoid:**
- ❌ Marking [x] before user confirms
- ❌ Batching multiple questions in one message
- ❌ Autonomous resolution ("I checked the code, answer is X")

---

##### S2.P1.I3 - Refinement & Alignment (30-60 min)

**Purpose:** Validate spec completeness, check per-feature alignment, get Gate 3 user approval

**Steps:**

1. **Per-Feature Alignment Check** (10-15 min)
   - Read spec.md files from ALL previously completed features
   - Compare against current feature's spec.md
   - **Cross-Reference Checklist Questions** (for Group 2+ features):
     - If prior features answer question consistently → DELETE from checklist, document as "Aligned with Features X-Y"
     - If prior features answer inconsistently → Escalate to Primary
     - If prior features don't answer → KEEP question
     - Example: KAI-7 Feature 08 deleted Q3 (precedence rule) because Features 01-07 all defined it consistently
   - Check for: naming conflicts, approach conflicts, data structure conflicts
   - Document any conflicts found
   - Update current spec if needed

1.5. **Agent-to-Agent Issue Reporting** (for parallel mode) - **FIX FOR ISSUE #3**

**If working in parallel mode and issues found in OTHER features:**

**Protocol:**
1. Create message file: `agent_comms/{YOUR_ID}_to_{PRIMARY_ID}.md`
2. Format:
```markdown
⏳ UNREAD

**From:** Secondary Agent {YOUR_ID}
**To:** Primary Agent {PRIMARY_ID}
**Date:** {timestamp}
**Type:** Cross-Feature Issue

## Issue Found

**Feature:** Feature {N} {name}
**Issue Type:** [Naming Conflict | Approach Conflict | Data Structure Conflict]
**Description:** [Detailed description of issue]

**Affected Files:**
- feature_{M}_{your_feature}/spec.md (your feature)
- feature_{N}_{other_feature}/spec.md (other feature with issue)

**Recommended Resolution:** [Your suggestion]

**Priority:** [HIGH | MEDIUM | LOW]
```

3. Primary agent reviews during next coordination heartbeat (every 15 minutes)
4. Primary agent responds via agent_comms or fixes directly
5. **Do NOT defer to S2.P2** - Fix immediately (distributed validation principle)

**Rationale:**
- Issues found early = cheaper to fix
- Distributed validation catches more issues than centralized
- Immediate fixes prevent cascading problems
- Parallel work maintains quality without sacrificing speed

**If NOT in parallel mode:** Document issues in notes, fix in S2.P2

2. **Consistency Loop Validation** (15-30 min) - **EMBEDS GATE 2**
   - Reference: `consistency_loop_spec_refinement.md`
   - **Round 1:**
     - Check spec completeness and consistency
     - **Gate 2 Check (Spec-to-Epic Alignment):**
       - Every requirement has source (Epic/User Answer/Derived)?
       - No scope creep (nothing user didn't ask for)?
       - No missing requirements (everything user asked for is included)?
       - All requirements trace to validated sources?
     - Zero scope creep, zero missing requirements required
   - **Round 2:** Fresh review, different patterns, find gaps
   - **Round 3:** Final validation
   - **Exit:** 3 consecutive clean rounds (Gate 2 passed as part of validation)

3. **If Gaps Found During Consistency Loop** - **LOOP-BACK MECHANISM**
   - Add new questions to checklist.md
   - **LOOP BACK to S2.P1.I2** (Checklist Resolution)
   - Resolve new questions with user
   - **RESTART S2.P1.I3 from beginning** (fresh Consistency Loop)
   - Continue until Consistency Loop passes with NO gaps

4. **Dynamic Scope Adjustment** (5-10 min if needed)
   - Count checklist.md items
   - If >35 items: Propose feature split to user
   - Get user approval before proceeding
   - If approved: Create new feature folders, split requirements
   - If rejected: Continue with large feature

4.5. **Create Acceptance Criteria Section** (5-10 min) - **MANDATORY BEFORE GATE 3**
   - Add "Acceptance Criteria" section to spec.md
   - For each requirement, define measurable success criteria
   - Define "Done" for each requirement
   - Clear pass/fail conditions
   - Reference: Current guides require acceptance criteria before user approval

5. **Gate 3: User Checklist Approval** (5-10 min) - **SEPARATE FROM CONSISTENCY LOOP**
   - Present final spec.md to user (including Acceptance Criteria)
   - Present final checklist.md (all ANSWERED)
   - **Explicitly state:** "Please approve this spec.md (including the Acceptance Criteria section) and checklist.md" - **FIX FOR ISSUE #33**
   - Ask: "Approve this feature specification?"
   - **MANDATORY GATE:** Cannot proceed without approval
   - Mark checklist items [x] ONLY AFTER user approves

   **If User Requests Changes:**
   - Update spec.md based on user feedback
   - **LOOP BACK to S2.P1.I3 Step 2** (Consistency Loop)
   - Re-validate spec with fresh Consistency Loop
   - Re-present to user for approval
   - Continue until user explicitly approves (no changes requested)

   **If User Rejects Entire Approach:** - **FIX FOR ISSUE #38 (EDGE CASE)**
   - User says: "This entire approach is wrong, start over"
   - **STOP - Do not loop back to I3**
   - Options:
     - (A) **Loop back to S2.P1.I1** (re-do research with different approach)
     - (B) **Escalate to S1** (re-do Discovery Phase if fundamental misunderstanding)
   - Ask user: "Should I re-do research (S2.P1.I1) or return to Discovery Phase (S1.P3)?"
   - Await user decision
   - **Rationale:** Total rejection indicates fundamental issue, not refinement issue

**Outputs:**
- `spec.md` (final, user-approved, aligned with previous features, with acceptance criteria)
- `checklist.md` (final, user-approved, all marked [x])

**Exit Condition:**
- User explicitly approves spec (including acceptance criteria)
- Gate 3 passed

**Secondary Agent Behavior:**
```
**If Secondary Agent:**
- Stop after S2.P1.I3 completes (Consistency Loop passes + Gate 3 approved)
- Do NOT proceed to S2.P2 (only Primary runs S2.P2)
- Report to Primary: "S2.P1 complete for Feature XX"
- Update STATUS file: READY_FOR_SYNC = true
- Wait for Primary to run S2.P2 and S3
```

---

#### S2.P2 - Cross-Feature Alignment Check (Primary Agent Only)

**When:** After entire group completes S2.P1

**Purpose:** Pairwise comparison of all features in group (and previous groups) with Consistency Loop validation

**Steps:**

0. **Sync Verification (If Parallel Mode)** (5-10 min)
   - **Only if parallel work mode enabled**
   - Verify all features in group completed S2.P1:
     - Check completion messages from secondary agents
     - Verify STATUS files show READY_FOR_SYNC = true
     - Verify checkpoints show WAITING_FOR_SYNC (not stale)
     - Check for stale agents (checkpoint >60 min old → escalate)
   - See: `parallel_work/s2_parallel_protocol.md` → Sync Point 1
   - **If any agent missing/stale:** STOP, send status check, wait for response
   - **Cannot proceed without all agents synced**

1. **Verify Group Completion** (5 min)
   - Check all features in current group completed S2.P1
   - Verify all STATUS files show READY_FOR_SYNC = true
   - If parallel mode: Verify all secondary agents reported completion

2. **Pairwise Comparison** (20-40 min)
   - For each pair of features in scope:
     - Current group features vs each other
     - Current group features vs ALL previous group features
   - Check for:
     - Naming conflicts (same name, different meaning)
     - Approach conflicts (contradictory implementations)
     - Data structure conflicts (incompatible formats)
     - Integration dependencies
     - Pattern inconsistencies
   - Document conflicts in comparison matrix

2.5. **Save Comparison Results** (5 min) - **FIX FOR ISSUE #34**
   - Create `epic/research/S2_P2_COMPARISON_MATRIX_GROUP_{N}.md`
   - Include:
     - Pairwise comparison matrix (all pairs checked)
     - Conflicts found (with severity: HIGH/MEDIUM/LOW)
     - Resolutions applied (or N/A if no conflicts)
     - Date and group number
   - **Rationale:** Audit trail for cross-feature decisions, helps with future debugging

3. **Conflict Resolution** (10-20 min)
   - For each conflict found:
     - Update affected feature spec.md files
     - Document resolution approach
     - Note dependencies in EPIC_README.md

4. **Consistency Loop Validation** (15-30 min)
   - Reference: `consistency_loop_alignment.md`
   - **Round 1:** Pairwise comparison in feature order
   - **Round 2:** Pairwise comparison in reverse order (different patterns)
   - **Round 3:** Random pair spot-checks, thematic clustering
   - **Exit:** 3 consecutive clean rounds (no conflicts)
   - **Zero Tolerance:** ALL issues (HIGH/MEDIUM/LOW) must be resolved (reference Proposal 1 "No Deferred Issues")

**Outputs:**
- Updated spec.md files (if conflicts resolved)
- `epic/research/S2_P2_COMPARISON_MATRIX_GROUP_{N}.md` (NEW FILE)
- Conflict resolution notes (in comparison matrix file)

**Group-Based Looping:**
```
S2.P2 runs MULTIPLE TIMES in parallel mode:
- After Group 1 completes S2.P1 → Run S2.P2 on Group 1 features only
- After Group 2 completes S2.P1 → Run S2.P2 on Group 2 + ALL Group 1 features
- After Group 3 completes S2.P1 → Run S2.P2 on Group 3 + ALL Groups 1-2 features
- Scope expands each iteration (cumulative alignment check)
```

**After S2.P2:**
- If more groups remain → Loop back to S2.P1 with next group
- If all groups done → Proceed to S3

---

### Parallel Work Compatibility

**S2.P1 (all 3 iterations) can be parallelized:**
- Multiple agents work on different features simultaneously
- Each agent executes S2.P1.I1, I2, I3 for their feature(s)
- Existing parallel work protocols apply (checkpoints, comms, locks, STATUS files)

**S2.P2 is PRIMARY AGENT ONLY:**
- Only Primary runs S2.P2 after each group completes S2.P1
- Secondary agents wait at end of S2.P1.I3

**No changes to parallel infrastructure needed** - existing protocols work with new structure.

---

### Estimated Time
**Per feature:**
- S2.P1.I1: 60-90 min
- S2.P1.I2: 45-90 min
- S2.P1.I3: 30-60 min
- **Total S2.P1: 135-240 min (2.25-4 hours)**

**Per group (Primary only):**
- S2.P2: 20-40 min (scales with feature count)

**Total S2: 2.5-4.5 hours per feature** (vs current 2-3 hours)
- User confirmed acceptable (quality and clarity over speed)

### Priority
**CRITICAL** - Core workflow redesign

---

## PROPOSAL 5: Redesign Stage 3 → "Epic Level Documentation, Testing Plans, and Approval"

### What
Refactor S3 to focus on epic-level artifacts with two Consistency Loops: (1) Epic-level testing strategy, (2) Epic documentation refinement. **Pairwise comparison moved to S2.P2.**

### Why (From User Memory)
"Once all the groups have finished their S2 work, then the primary agent will move here to S3. During this stage, the agent should perform 2 consistency loops. First, they should develop an Epic-level testing strategy for when all feature work is completed... After the test plan is created, then the agent should do another consistency loop to refine the epic ticket."

### Audit Evidence
✅ stage_3_reference_card.md was deleted (Audit Round 12) - Old card claimed "S3 and S4 merged" (FALSE)

### User Clarifications from Review
1. **S3 creates epic-level test plan** (for when all features complete)
2. **S4 creates feature-level test plans** (per feature, different from S3)
3. **Two separate test plans** (not merged)
4. **Pairwise comparison moved to S2.P2** (removed from S3)

### Files Affected

**CREATE:**
1. **`s3_epic_planning_approval.md`** - Complete S3 guide

**MODIFY/DELETE:**
2. `s3_cross_feature_sanity_check.md` - Update router or deprecate

### Structure Details

**Phase 1: Epic Testing Strategy Development (45-60 min)** - **EXPANDED WITH DETAIL (FIX FOR ISSUE #4)**

**Purpose:** Create epic_smoke_test_plan.md for end-to-end integration testing when all features complete

**What This Tests:**

**Epic-Level Tests (S3):**
- End-to-end workflows across ALL features
- Integration points between features
- Epic-level success criteria
- Data flow through complete system

**Example (Epic Level):**
```markdown
**Epic:** Fantasy Football Draft Helper with 3 features

**S3 Epic-Level Test:**
- Scenario 1: Feature 01 creates player rankings CSV → Feature 02 reads CSV and generates draft recommendations → Feature 03 exports recommendations to league format
- Scenario 2: All 3 features work together in single draft session (integration test)
- Scenario 3: Edge case spans features: Missing player in rankings affects recommendations and export (cross-feature error handling)
```

**Feature-Level Tests (S4) - For Contrast:**
```markdown
**S4 Feature-Level Test (Feature 02 only):**
- Unit Test: Recommendation algorithm calculates correct scores (function-level)
- Integration Test: Feature 02 reads various CSV formats (component-level)
- Edge Case: Feature 02 handles missing players gracefully (within feature boundary)
```

**Key Distinction:** S3 tests ACROSS features, S4 tests WITHIN features

**Steps:**

1. **Review All Feature Test Requirements** (10-15 min)
   - Read each feature's spec.md test section
   - Identify epic-level integration scenarios
   - Note dependencies between features
   - Identify end-to-end workflows

2. **Identify Integration Points** (15-20 min) - **EXPANDED FROM CURRENT S4 STEP 2**

**Create integration point map with details:**

```markdown
## Integration Points Identified

### Integration Point 1: FantasyPlayer Data Model
**Features Involved:** All features (1, 2, 3, 4)
**Type:** Shared data structure
**Flow:**
- Feature 1 adds: adp_value, adp_multiplier fields
- Feature 2 adds: injury_status, injury_multiplier fields
- Feature 3 adds: schedule_strength field
- Feature 4 reads: ALL above fields

**Test Need:** Verify all fields present after all features run

---

### Integration Point 2: Scoring Algorithm
**Features Involved:** Features 1, 2, 3, 4
**Type:** Computational dependency
**Flow:**
- Feature 1: score *= adp_multiplier
- Feature 2: score *= injury_multiplier
- Feature 3: score *= schedule_strength
- Feature 4: Combines all multipliers

**Test Need:** Verify final score includes all multipliers

---

### Integration Point 3: Data File Locations
**Features Involved:** Features 1, 2, 3
**Type:** File system interaction
**Flow:**
- Feature 1 creates: data/rankings/adp.csv
- Feature 2 creates: data/player_info/injury_reports.csv
- Feature 3 creates: data/rankings/schedule_strength.csv
- All files must exist for Feature 4 to work

**Test Need:** Verify all data files created in correct locations
```

3. **Define Epic Success Criteria** (15-20 min) - **EXPANDED FROM CURRENT S4 STEP 3**

**Convert vague goals to MEASURABLE criteria:**

```markdown
## Epic Success Criteria

**The epic is successful if ALL of these criteria are met:**

### Criterion 1: All Data Files Created
✅ **MEASURABLE:** Verify these files exist:
- `data/rankings/adp.csv` (from Feature 1)
- `data/player_info/injury_reports.csv` (from Feature 2)
- `data/rankings/schedule_strength.csv` (from Feature 3)

**Verification:** `ls data/rankings/ data/player_info/` shows all 3 files

---

### Criterion 2: All Multipliers Applied
✅ **MEASURABLE:** Run draft helper and verify player scores include:
- ADP multiplier contribution (Feature 1)
- Injury multiplier contribution (Feature 2)
- Schedule strength contribution (Feature 3)

**Verification:**
1. Load player data
2. Check FantasyPlayer object has all fields
3. Verify total_score calculation includes all three

---

### Criterion 3: Recommendations Updated
✅ **MEASURABLE:** Draft recommendations list shows:
- At least 10 players ranked
- Each player has total_score > 0
- Scores reflect new data sources

**Verification:** Run draft helper, verify recommendation output
```

4. **Create Specific Test Scenarios** (15-25 min) - **EXPANDED FROM CURRENT S4 STEP 4**

**Convert high-level categories to concrete tests with commands:**

```markdown
## Specific Test Scenarios

### Test Scenario 1: Data File Creation (Features 1, 2, 3)

**Purpose:** Verify all features create their data files

**Steps:**
1. Clear data directories: `rm -rf data/rankings/* data/player_info/*`
2. Run Feature 1: Load ADP data
3. Run Feature 2: Load injury data
4. Run Feature 3: Load schedule data

**Expected Results:**
✅ `data/rankings/adp.csv` exists and contains >100 rows
✅ `data/player_info/injury_reports.csv` exists and contains >50 rows
✅ `data/rankings/schedule_strength.csv` exists and contains >30 rows

**Failure Indicators:**
❌ Any file missing → Feature failed to create output
❌ File exists but empty → Feature ran but no data loaded

**Command to verify:**
```bash
test -f data/rankings/adp.csv && echo "Feature 1 OK" || echo "Feature 1 FAILED"
test -f data/player_info/injury_reports.csv && echo "Feature 2 OK" || echo "Feature 2 FAILED"
test -f data/rankings/schedule_strength.csv && echo "Feature 3 OK" || echo "Feature 3 FAILED"
```

---

### Test Scenario 2: FantasyPlayer Field Integration (All Features)

**Purpose:** Verify all features add their fields to FantasyPlayer model

**Steps:**
1. Run league helper with all features enabled
2. Load player data
3. Inspect first player object

**Expected Results:**
✅ Player object has field: `adp_value` (Feature 1)
✅ Player object has field: `adp_multiplier` (Feature 1)
✅ Player object has field: `injury_status` (Feature 2)
✅ Player object has field: `injury_multiplier` (Feature 2)
✅ Player object has field: `schedule_strength` (Feature 3)

**Command to verify:**
```python
from league_helper.util.PlayerManager import PlayerManager
pm = PlayerManager(data_folder="data/")
players = pm.load_players()
p = players[0]
print(f"ADP: {p.adp_value}, {p.adp_multiplier}")
print(f"Injury: {p.injury_status}, {p.injury_multiplier}")
print(f"Schedule: {p.schedule_strength}")
```

---

[Continue with 3-4 more test scenarios following same detailed format]
```

5. **Update epic_smoke_test_plan.md** (10-15 min)
   - Replace S1 placeholder content with concrete scenarios
   - Add all integration points
   - Add all success criteria
   - Add all test scenarios
   - Mark as "S3 version - will update in S8.P2 (Epic Testing Update)"

6. **Consistency Loop Validation** (15-20 min)
   - Reference: `consistency_loop_test_strategy.md`
   - **Round 1:** Check test plan completeness
     - All features integrated in tests?
     - All integration points tested?
     - End-to-end scenarios complete?
     - Edge cases across features included?
     - Exit criteria clear?
   - **Round 2:** Fresh review, find gaps in coverage
   - **Round 3:** Final validation, spot-check scenarios
   - **Exit:** 3 consecutive clean rounds

**Outputs:**
- `epic_smoke_test_plan.md` (validated, epic-level integration tests with detailed scenarios)

---

**Phase 2: Epic Documentation Refinement (20-30 min)**

**Purpose:** Refine epic ticket with details from all developed feature specs

**Steps:**

1. **Consolidate Feature Details** (10-15 min)
   - Read all feature spec.md files
   - Extract key approaches, data structures, integration points
   - Identify epic-level patterns

2. **Update Epic Ticket** (10-15 min)
   - Enhance `EPIC_README.md` or epic ticket
   - Add feature summary section (1-2 sentences per feature)
   - Document epic-level architecture decisions
   - Clarify scope boundaries

3. **Consistency Loop Validation** (15-20 min)
   - Reference: `consistency_loop_spec_refinement.md`
   - **Round 1:** Check epic documentation completeness
     - All features described?
     - Architecture decisions documented?
     - Scope boundaries clear?
     - Integration approach explained?
   - **Round 2:** Fresh review, different reading patterns
   - **Round 3:** Final validation
   - **Exit:** 3 consecutive clean rounds

**Outputs:**
- `EPIC_README.md` (updated with feature details)

---

**Phase 3: Epic Plan Approval (10-15 min)**

**Purpose:** Get user approval for complete epic plan before proceeding to S4

**Steps:**

1. **Create Epic Summary** (5-10 min)
   - Consolidate all feature specs
   - List all features with 1-sentence descriptions
   - Summarize epic test plan approach
   - Estimate total timeline (feature count × ~6-8 hours)

2. **Gate 4.5: User Approval of Epic Plan** (5 min)
   - Present epic summary to user
   - Present epic_smoke_test_plan.md
   - Ask: "Approve this epic plan and testing strategy?"
   - **MANDATORY GATE:** Cannot proceed to S4 without approval
   - **Note:** Single Gate 4.5 (not split into 4.5a/4.5b per user direction)

**If User Requests Changes:**
- Update epic_smoke_test_plan.md or EPIC_README.md based on feedback
- LOOP BACK to appropriate phase:
  - If testing strategy issues → S3.P1
  - If documentation issues → S3.P2
  - If fundamental approach wrong → S2 (cross-feature conflicts need re-resolution)
- Re-run updated phase with Consistency Loop
- Re-present to user for approval (Gate 4.5 again)

**If User Rejects Entire Epic Approach:**
- User says: "This epic scope/approach is fundamentally wrong"
- STOP - Do not loop back to S3
- Ask user for guidance:
  - (A) Re-do Discovery Phase (S1.P3) - research was incomplete
  - (B) Revise feature breakdown (S1.P4) - features defined incorrectly
  - (C) Exit epic planning - epic should not proceed
- Await user decision before proceeding
- **Rationale:** Total rejection indicates problem earlier than S3, not refinement issue

**Outputs:**
- `EPIC_SUMMARY.md` (optional, for user reference)
- User approval obtained

**Exit Condition:**
- User explicitly approves epic plan
- Gate 4.5 passed
- Ready to proceed to S4 (first feature)

---

### Why This Works

**Advantages:**
1. **Epic-Level Focus:** S3 only handles epic-level artifacts
2. **Feature Conflicts Already Resolved:** Pairwise comparison done in S2.P2
3. **Clear Separation:** S3 = epic-level, S4 = feature-level
4. **Earlier Validation:** Testing strategy approved before feature work starts
5. **Consistency Loop Quality:** Two independent validations
6. **Detailed Guidance:** Expanded S3.P1 preserves current S4 quality

### Estimated Time
60-90 minutes per epic

### Priority
**CRITICAL** - Core workflow redesign

---

## PROPOSAL 6: Create New Stage 4 → "Feature Level Testing Plan Development"

### What
Create new S4 stage for feature-level test planning (test-driven development), pulled out from old S5 iterations.

### Why (From User Memory)
"This stage takes the iterations of test plan development out of Stage 5 and gives them a dedicated stage. The agent will focus on the ways they expect to test the changes in the feature. Consider this test-driven development. This will involve a consistency loop to verify the test plan."

### Audit Evidence
✅ **100% CONFIRMED** - All 4 files explicitly listed (Audit Round 11:235-241)

### User Clarifications from Review
1. **Two separate test plans:** S3 = epic-level, S4 = feature-level
2. **Follow naming conventions** from guides_v2

### Clarification
**Current S4 vs New S4:**
- **Current s4_epic_testing_strategy.md:** Epic-level testing (updates epic_smoke_test_plan.md)
- **New S4 (this proposal):** Feature-level testing (creates feature test strategy)
- **What happens to current S4 content:** Moves to S3.P1 (Epic Testing Strategy Development)
- **This proposal REPLACES current S4**

### Files Affected

**CREATE (All 4 files AUDIT CONFIRMED):**
1. **`s4_feature_testing_strategy.md`** - Main S4 guide (router)
2. **`s4_test_strategy_development.md`** - Iterations 1-3 detailed guide
3. **`s4_consistency_loop.md`** - Iteration 4 specialized guide
4. **`s4_feature_testing_card.md`** - Quick reference card

**REPLACE:**
5. `stages/s4/s4_epic_testing_strategy.md` - Content moves to S3.P1, file deprecated

### Structure Details

**Purpose:** Test-driven development - plan tests BEFORE implementation

**Naming Convention:** S4.I1, S4.I2, S4.I3, S4.I4 (no phases, 4 iterations)

**Examples:**

**Feature-Level Tests (S4):**
```markdown
**Feature 02: Draft Recommendations**

**S4 Feature-Level Tests:**
- Unit Test: `test_calculate_player_score()` - Verify scoring algorithm
- Unit Test: `test_handle_missing_stats()` - Verify graceful error handling
- Integration Test: `test_read_rankings_csv()` - Verify CSV parsing
- Integration Test: `test_recommendation_workflow()` - Verify end-to-end
- Edge Case: Empty CSV file → raises clear error
- Edge Case: Player with zero games → excluded from recommendations
- Config Test: Custom scoring weights → recommendations adjust
```

**Iteration 1: Test Strategy Development (15-20 min)**

**Purpose:** Plan unit tests, integration tests, edge cases

**Steps:**

1. **Requirement Coverage Analysis** (5-10 min)
   - For each requirement in spec.md: identify testable behaviors, edge cases, error conditions
   - Create test coverage matrix

2. **Test Case Enumeration** (10-15 min)
   - Draft test cases:
     - Unit tests (function-level, >80% coverage goal)
     - Integration tests (component-level, key workflows)
     - Edge case tests (boundary conditions, error paths)
   - Link each test to requirement (traceability)

**Output:** Test coverage matrix (draft), test case list (draft)

---

**Iteration 2: Edge Case Enumeration (10-15 min)**

**Purpose:** Systematically identify ALL edge cases

**Steps:**

1. **Boundary Conditions** (5-10 min)
   - For each input: min/max values, null/empty/zero, invalid types
   - Document expected behavior

2. **Error Path Enumeration** (5-10 min)
   - For each error condition: invalid input, dependency failure, race conditions, state conflicts
   - Document error handling approach

**Output:** Edge case catalog, updated test coverage matrix

---

**Iteration 3: Configuration Change Impact (10-15 min)**

**Purpose:** Identify config changes, plan tests

**Steps:**

1. **Configuration Dependency Analysis** (5-10 min)
   - Which config files? Which values affect behavior? What if invalid/missing?

2. **Configuration Test Cases** (5-10 min)
   - Test: Default, custom, invalid, missing configurations

**Output:** Configuration test matrix, updated test coverage matrix

---

**Iteration 4: Consistency Loop (Test Strategy Validation) (15-20 min)**

**Purpose:** Validate test strategy completeness

**Reference:** `consistency_loop_test_strategy.md`

**Round 1 Checklist:**
- All requirements have test coverage
- >90% code coverage planned
- All edge cases have tests
- All config scenarios have tests
- Error paths have tests
- Integration points have tests
- Traceability: Each test links to requirement

**Round 2 Checklist:**
- Re-read spec.md with fresh eyes
- Any new edge cases?
- Any new integration points?
- Any assumptions needing validation?
- Coverage gaps?

**Round 3 Checklist:**
- Random spot-check 5 requirements
- Integration tests cover all interactions?
- Error handling tests comprehensive?
- Final coverage estimate >90%?

**Exit Criteria:**
- 3 consecutive rounds with zero new issues
- All checklists pass

---

**After S4 Completes:**

**Output to separate file:**
- Create `feature_{N}_{name}/test_strategy.md` with:
  - All test categories (unit, integration, edge, config)
  - Representative test cases
  - Coverage goal (>90%)
  - Traceability matrix
  - Edge case catalog
  - Configuration test matrix
- This file will be merged into implementation_plan.md during S5.P1 Iteration 1

**Why separate file:** S5 creates implementation_plan.md, so S4 cannot write to it yet.

**No separate Gate 4.5b:** Single Gate 4.5 at end of S3, feature test strategy approved as part of Gate 5 (after S5)

### Estimated Time
45-60 minutes per feature

### Priority
**CRITICAL** - 100% confirmed

---

## PROPOSAL 7: Update Stage 5 → "Implementation Plan Creation" (Remove Testing Iterations, Add Consistency Loops)

### What
Update S5 to remove testing iterations (moved to S4) and add Consistency Loops at key validation points. Renumber remaining iterations sequentially.

### Why (From User Memory)
"This is a version of the existing stage 5, where we are creating an implementation plan, except it will omit the testing iterations that are moved to stage 4, and there will be several places where we place consistency loops."

### User Clarifications from Review
1. **Renumber iterations sequentially** (no gaps)
2. **Add Consistency Loops** at Round 1 end and Round 3 pre-Gate 23a

### Files Affected

**MODIFY:**
1. S5 router files
2. S5 iteration files (renumber after removing I8-I10)
3. **S5.P1 Iteration 1:** Add step to merge test_strategy.md from S4

**CREATE:**
4. Consistency Loop integration guides (if needed)

### Structure Changes

**Remove from S5:** (Moved to S4)
- Old Iteration 8: Test Strategy Development → **MOVED TO S4.I1**
- Old Iteration 9: Edge Cases → **MOVED TO S4.I2**
- Old Iteration 10: Config Impact → **MOVED TO S4.I3**

**Add to S5:**

**NEW: S5.P1 Iteration 1 Enhancement:**
```markdown
**Iteration 1: Requirements Coverage Check + Test Strategy Integration**

**NEW STEP 0: Merge Test Strategy from S4** (5-10 min) - **FIX FOR ISSUE #39**

**Prerequisites Check:**
1. Verify `feature_{N}_{name}/test_strategy.md` exists
2. **If file missing:**
   - STOP immediately
   - Output error: "test_strategy.md not found - S4 may not have completed"
   - Escalate to user: "S4 test strategy file is missing. Should I:"
     - (A) Go back to S4 to create test strategy
     - (B) Create placeholder test strategy now (not recommended)
     - (C) Investigate why S4 didn't create file
   - **Do NOT proceed without test strategy**
   - **Rationale:** test_strategy.md is foundation for implementation planning

3. **If file exists, validate content:** - **FIX FOR ROUND 4 MINOR GAP**
   - Read file to verify it's not empty
   - Check file contains required sections:
     - "Unit Tests" or "Test Strategy" section header
     - At least 50 bytes of content (not just whitespace)
   - **If file exists but empty/invalid:**
     - STOP immediately
     - Output error: "test_strategy.md exists but appears empty or invalid"
     - Escalate to user: "S4 test strategy file has no content. Should I:"
       - (A) Go back to S4 to recreate test strategy
       - (B) Proceed anyway (not recommended - will create incomplete plan)
       - (C) Investigate why S4 created empty file
     - **Do NOT proceed with empty/invalid file**
     - **Rationale:** Empty test strategy provides no planning value, leads to incomplete implementation plan

4. **If file exists and valid:**
- Read `feature_{N}_{name}/test_strategy.md` (created in S4)
- Incorporate test strategy into implementation_plan.md "Test Strategy" section
- Include: All test categories, representative cases, coverage goal, traceability matrix
- Reference S4 test strategy throughout implementation tasks
```

**Renumbering:** - **FIX FOR ISSUE #35**

**Old numbering (with gaps):**
- Round 1: I1-I7 (7 iterations), skip 8-10, I11-I12 (2 iterations) = 9 total
- Round 2: I13-I16 (4 iterations)
- Round 3: I17-I25 (9 iterations)
- **Total: 22 iterations** (excluding removed 8-10)

**New numbering (sequential, CORRECTED):**
- **Round 1:** I1-I7 (7 iterations) + Consistency Loop
- **Round 2:** I8-I13 (6 iterations: old I11-I12 become I8-I9, old I13-I16 become I10-I13)
- **Round 3:** I14-I22 (9 iterations: old I17-I25 renumbered)
- **Total: 22 iterations** (same count, sequential numbering)

**Detailed Mapping:**
- Old I1-I7 → New I1-I7 (unchanged)
- Old I11 → New I8
- Old I12 → New I9
- Old I13 → New I10
- Old I14 → New I11
- Old I15 → New I12
- Old I16 → New I13
- Old I17 → New I14
- Old I18 → New I15
- Old I19 → New I16
- Old I20 → New I17
- Old I21 → New I18
- Old I22 → New I19
- Old I23 → New I20
- Old I24 → New I21
- Old I25 → New I22

**Gates:** - **FIX FOR ISSUE #36 (CLARIFICATION)**

**Gates 4a and 7a are EMBEDDED in Round 1 Consistency Loop:**
- **Old Gate 4a** (TODO Specification Audit) → Now checked in Round 1 Consistency Loop Round 1 (see checklist below)
- **Old Gate 7a** (Backward Compatibility) → Now checked in Round 1 Consistency Loop Round 1 (see checklist below)

**Keep (existing gates):**
- Gate 5: Implementation Plan Approval (after S5 complete, before S6)
- Gate 23a: Pre-Implementation Spec Audit (embedded in Round 3 Consistency Loop)
- Gate 24: GO/NO-GO Decision (after Gate 23a)
- Gate 25: Spec Validation Check (with Gate 24)

### Consistency Loop Details

**Round 1 Consistency Loop (After Iteration 7):**

**Purpose:** Validate implementation plan completeness after Round 1 drafting

**Timing:** After Iteration 7 (Integration Points), before Round 2

**Checklist (Each Round):**

**Round 1 Checks (EMBEDS Gates 4a and 7a):**
- [ ] All requirements from spec.md in implementation plan?
- [ ] All TODO items from Iterations 1-7 addressed? **(Gate 4a criterion)**
- [ ] **Every implementation task has acceptance criteria?** **(Gate 4a criterion)**
- [ ] Test strategy from S4 fully integrated?
- [ ] Algorithm pseudocode complete?
- [ ] Data structures defined?
- [ ] File structure planned?
- [ ] Integration points documented?
- [ ] **Backward compatibility addressed? Old data formats handled?** **(Gate 7a criterion)**

**Round 2 Checks:**
- [ ] Re-read spec.md: Any missed requirements?
- [ ] Re-read implementation plan: Any vague sections?
- [ ] Any assumptions needing clarification?
- [ ] Any integration points missed?
- [ ] Traceability: Each requirement maps to implementation section?

**Round 3 Checks:**
- [ ] Spot-check 5 random requirements
- [ ] Check TODO list: All resolved or carried forward?
- [ ] Cross-reference spec.md acceptance criteria with plan
- [ ] Final completeness check

**Exit:** 3 consecutive rounds with zero new issues

---

**Round 3 Consistency Loop (Before Gate 23a):**

**Purpose:** Final pre-implementation validation

**Timing:** After Iteration 22 (Pre-Implementation Readiness), before Gate 23a

**Gate 23a is EMBEDDED in this Consistency Loop:**

**Round 1 Checks (Gate 23a Parts 1-5):**
- **Part 1: Requirement Traceability**
  - [ ] Every spec.md requirement has implementation plan section
  - [ ] Every plan section links to spec.md requirement
  - [ ] No orphaned requirements, no orphaned sections

- **Part 2: Test Coverage Alignment**
  - [ ] Test strategy section complete (from S4)
  - [ ] >90% coverage planned
  - [ ] All edge cases have tests

- **Part 3: Acceptance Criteria Verification**
  - [ ] Each acceptance criterion has implementation approach
  - [ ] "Done" definition clear for each requirement

- **Part 4: Dependency Completeness**
  - [ ] All external/internal/config dependencies documented

- **Part 5: Implementation Readiness**
  - [ ] File structure planned, algorithms designed, data structures defined
  - [ ] Error handling documented, no unresolved TODOs

**Round 2 Checks:**
- [ ] Re-read spec.md with fresh eyes
- [ ] Any requirements interpretation changed?
- [ ] Any new edge cases?
- [ ] Check test strategy: Any gaps?
- [ ] Check algorithms: Any concerns?

**Round 3 Checks:**
- [ ] Random spot-check 5 requirements
- [ ] Verify traceability both directions
- [ ] Check for vague language
- [ ] Final readiness check

**Exit:** 3 consecutive rounds with zero new issues
- Gate 23a effectively passed through Consistency Loop
- Proceed to final gate sequence:
  - Iteration 23: Integration Gap Check (verify all implementation tasks have callers)
  - Iteration 25: Spec Validation (verify spec against all validated sources)
  - Iteration 24: GO/NO-GO Decision (implementation readiness)
  - Gate 5: User Approval of implementation_plan.md (see Gate 5 section below)

---

### Gate 5: User Approval of Implementation Plan (After S5, Before S6)

**Purpose:** Get user approval for implementation_plan.md before starting implementation

**Timing:** After all 22 iterations complete + all Consistency Loops pass + all embedded gates pass (Gates 4a, 7a, 23a) + Iterations 23-25 complete + Iteration 24 returns GO decision

**Process:**

1. **Check questions.md status:**
   - If open questions exist → Present to user first → Update plan → Ask restart confirmation
   - If no questions (or after user answers) → Proceed to step 2

2. **Present implementation_plan.md to user for approval:**
   - Highlight key sections (tasks, dependencies, test strategy, phasing)
   - Request explicit approval
   - Use prompt from `prompts_reference_v2.md`

3. **Wait for user response:**
   - If approved → Document approval, proceed to S6
   - If changes requested → See "If User Requests Changes" below
   - If rejected entirely → See "If User Rejects Entire Plan" below

**If User Requests Changes:**
- Update implementation_plan.md based on feedback
- LOOP BACK to appropriate round:
  - If requirements misunderstood → Round 1 (Iterations 1-7)
  - If test strategy issues → Round 2 (Iterations 8-13)
  - If implementation approach wrong → Round 3 (Iterations 14-22)
- Re-run updated round with Consistency Loop
- Re-run all subsequent rounds
- Re-run Iterations 23-25 and Iteration 24 GO/NO-GO
- Re-present to user for approval (Gate 5 again)

**If User Rejects Entire Implementation Plan:**
- User says: "This implementation approach is fundamentally wrong"
- STOP - Do not loop back to S5
- Ask user for guidance:
  - (A) Re-do S4 (test strategy may be inadequate)
  - (B) Re-do S2 (spec may need revision - requirements misunderstood)
  - (C) Bring in senior developer (technical complexity too high for current approach)
- Await user decision before proceeding
- **Rationale:** Total rejection indicates problem earlier than S5, not iteration-level issue

**Documentation:**
- Document Gate 5 approval in implementation_plan.md header:
  ```markdown
  **Gate 5 Status:** APPROVED by [user name] on [timestamp]
  ```
- Update feature README.md Agent Status:
  - Current Stage: S5 COMPLETE
  - Gate 5: PASSED [timestamp]
  - Next Action: Read S6 guide

**MANDATORY GATE:** Cannot proceed to S6 without Gate 5 approval

**Consistency with Other Gates:**
- Same 3-tier pattern as Gates 3 and 4.5 (approval → minor changes → major rejection)
- User always gets explicit escalation options for fundamental issues
- Loop-back mechanism preserves Consistency Loop quality

---

### Estimated Time
Similar to current S5 (testing iterations moved to S4, Consistency Loops added ≈ net neutral)

### Priority
**HIGH** - Depends on S4 being created first

---

## PROPOSAL 8: Update Stages 7 & 9 QC/Final Review with Consistency Loops

### What
Add Consistency Loops to QC rounds and Final Review in both S7 (feature-level) and S9 (epic-level) stages.

### Why (From User Memory)
"The QC rounds and Final Review from both the feature level and epic level QA phases should be updated to include consistency loops where they are analyzing all the files involved and skeptically verifying their changes."

### Audit Evidence
✅ **100% CONFIRMED** - consistency_loop_qc_pr.md has 12 references

### Files Affected

**MODIFY:**
1. `stages/s7/s7_p2_qc_rounds.md` - Add Consistency Loop references (3 locations)
2. `stages/s7/s7_p3_final_review.md` - Add Consistency Loop references (2 locations)
3. `stages/s9/s9_p2_epic_qc_rounds.md` - Add Consistency Loop references (3 references)

### Changes Details

**S7.P2 (QC Rounds) - 3 references:**

**QC Round 1:**
- Add: Reference to `consistency_loop_qc_pr.md`
- Apply: Consistency Loop approach (assume everything is wrong)
- Fresh eyes: Skeptically analyze all changed files
- Automated: Run all tests + linters
- Manual: Code review with different patterns each round
- **No deferred issues:** ALL issues (critical, major, minor) must be fixed before Round 2

**QC Round 2:**
- Add: Reference to `consistency_loop_qc_pr.md`
- Apply: Different review patterns than Round 1
- Focus: Verify Round 1 fixes, find NEW issues
- **No deferred issues:** ALL new issues must be fixed before Round 3

**QC Round 3:**
- Add: Reference to `consistency_loop_qc_pr.md`
- Apply: Final validation with spot-checks
- Requirement: ZERO issues (critical, major, or minor)
- **Exit criteria:** 3 consecutive clean rounds (no known issues remain)

---

**S7.P3 (Final Review) - 2 references:**

**PR Review:**
- Add: Reference to `consistency_loop_qc_pr.md`
- Apply: Consistency Loop for PR review
- Verify: All changes before commit
- Fresh eyes: Different review patterns
- **No deferred issues:** Cannot commit with known issues

**Lessons Learned:**
- Add: Reference to `consistency_loop_qc_pr.md` (optional)
- Apply: Review lessons with fresh perspective

---

**S9.P2 (Epic QC Rounds) - 3 references:**

**Epic QC Round 1:**
- Add: Reference to `consistency_loop_qc_pr.md`
- Apply: Consistency Loop at epic level
- Analyze: All features together
- Integration: Test feature interactions
- **No deferred issues:** ALL issues across ALL features must be fixed

**Epic QC Round 2:**
- Add: Reference to `consistency_loop_qc_pr.md`
- Apply: Different patterns than Round 1
- Cross-feature: Verify integration points
- **No deferred issues:** ALL new issues must be fixed

**Epic QC Round 3:**
- Add: Reference to `consistency_loop_qc_pr.md`
- Apply: Final validation
- Requirement: ZERO issues across entire epic
- **Exit criteria:** 3 consecutive clean rounds (epic is defect-free)

### Estimated Time
1-2 hours

### Priority
**MEDIUM** - Depends on consistency_loop_qc_pr.md being created first

---

## PROPOSAL 9: Update CLAUDE.md with New Workflow

### What
Update CLAUDE.md to reflect all stage redesigns, Consistency Loop protocol, and new workflow structure.

### Why
CLAUDE.md is the primary reference file that agents read when starting work on this codebase. It must accurately reflect the new v2 workflow with Consistency Loops, redesigned stages, and updated gate locations. Without these updates, agents will follow outdated workflow patterns.

### Changes Required

#### Section: Stage Workflows Quick Reference

**Update S2 (Feature Deep Dives):**
```markdown
**S2: Feature Deep Dives** (Loop through ALL features)
- **First Action:** Use "Starting S2" prompt
- **Guide:** `stages/s2/s2_feature_deep_dive.md` (router to phases)
- **Phases:**
  - S2.P1: Research and Specification (3 iterations)
    - S2.P1.I1: Feature-Level Discovery (Consistency Loop embeds Gate 1)
    - S2.P1.I2: Checklist Resolution (one question at a time, "Correct Status Progression" protocol)
    - S2.P1.I3: Refinement & Alignment (Consistency Loop embeds Gate 2, Gate 3 user approval)
  - S2.P2: Cross-Feature Alignment Check (Primary agent only, includes pairwise comparison)
- **Key Outputs:** spec.md, checklist.md (QUESTIONS ONLY), RESEARCH_NOTES.md (REQUIRED)
- **Gates:** Gate 1 (embedded in I1), Gate 2 (embedded in I3), Gate 3 (user approval at I3 end)
- **Next:** S3 (after ALL features)
```

**Update S3 (Cross-Feature Sanity Check → Epic Planning):**
```markdown
**S3: Epic Planning** (After all features complete S2)
- **First Action:** Use "Starting S3" prompt
- **Guide:** `stages/s3/s3_epic_planning.md`
- **Phases:**
  - S3.P1: Epic Testing Strategy (Consistency Loop - moved from old S4)
  - S3.P2: Epic Documentation Refinement (Consistency Loop)
  - S3.P3: Epic Plan Approval (Gate 4.5 - user approval)
- **Key Outputs:** epic_smoke_test_plan.md, EPIC_README.md (updated), epic summary
- **Gate 4.5:** User approves epic plan and testing strategy (MANDATORY)
- **Next:** S4 (first feature)
```

**Add S4 (New Stage):**
```markdown
**S4: Feature Testing Strategy** (Per feature, before implementation)
- **First Action:** Use "Starting S4" prompt
- **Guide:** `stages/s4/s4_feature_testing_strategy.md`
- **Purpose:** Test-driven development - define testing approach before implementation
- **Phases:**
  - S4.P1: Test Strategy Development (Consistency Loop)
  - S4.P2: Test Coverage Planning (>90% coverage goal)
  - S4.P3: Edge Case Identification
- **Key Outputs:** test_strategy.md (~80-100 lines)
- **Next:** S5 (implementation planning for same feature)
```

**Update S5 (Implementation Planning):**
```markdown
**S5: Implementation Planning** (22 iterations, 3 rounds)
- **First Action:** Use "Starting S5 Round 1/2/3" prompt
- **Guide:** `stages/s5/s5_p1_planning_round1.md` (router)
- **Rounds:**
  - Round 1: I1-I7 (Requirements, Algorithms, Integration) + Consistency Loop (embeds Gates 4a, 7a)
  - Round 2: I8-I13 (incorporates test_strategy.md from S4) + Consistency Loop
  - Round 3: I14-I22 (Preparation) + Consistency Loop (embeds Gate 23a) + Iterations 23-25 + Gate 5
- **Output:** implementation_plan.md (~400 lines)
- **Gate 5:** User approves implementation plan (MANDATORY)
- **Next:** S6
```

#### Section: Key Principles

**Add after "Epic-first thinking":**
```markdown
- **Consistency Loop quality**: Assume everything is wrong, 3 consecutive clean rounds required, no deferred issues
- **No deferred issues principle**: ALL identified issues must be fixed immediately (cannot defer for "later")
- **Maximum round limit**: 10 rounds before escalation (safety mechanism for stuck loops)
```

#### Section: Gate Numbering System

**Update Complete Gate List table:**

| Gate | Type | Location | Purpose | Approver |
|------|------|----------|---------|----------|
| Gate 1 | Iteration | S2.P1.I1 (embedded) | Research Completeness Audit | Agent (checklist) |
| Gate 2 | Iteration | S2.P1.I3 (embedded) | Spec-to-Epic Alignment | Agent (checklist) |
| Gate 3 | Stage | S2.P1.I3 (end) | User Checklist Approval | User |
| Gate 4.5 | Stage | S3.P3 | Epic Plan Approval | User |
| Gate 5 | Stage | S5 (after I24) | Implementation Plan Approval | User |
| Gate 4a | Iteration | S5.P1 Round 1 (embedded) | TODO Specification Audit | Agent (checklist) |
| Gate 7a | Iteration | S5.P1 Round 1 (embedded) | Backward Compatibility Check | Agent (checklist) |
| Gate 23a | Iteration | S5.P3 Round 3 (embedded) | Pre-Implementation Spec Audit (5 parts) | Agent (checklist) |
| Gate 24 | Iteration | S5.P3 (after I25) | GO/NO-GO Decision | Agent (confidence) |
| Gate 25 | Iteration | S5.P3 (before I24) | Spec Validation Check | Agent (checklist) |

**Add note:**
```markdown
**Gate Patterns:**
- **Embedded gates:** Validation dimensions within Consistency Loops (Gates 1, 2, 4a, 7a, 23a)
- **User approval gates:** Explicit STOP points requiring user decision (Gates 3, 4.5, 5)
- **Agent decision gates:** Confidence-based progression (Gates 24, 25)
```

#### Section: Workflow Guides Location

**Add after "All guides location:":**
```markdown
**Core Protocol:**
- `reference/consistency_loop_protocol.md` - Master Consistency Loop protocol
- `reference/consistency_loop_*.md` - Context-specific variants (S2, S4, S5, S7, S9)
```

**Update guide references:**
```markdown
**Updated Stages:**
- `stages/s2/` - Feature Planning (redesigned with 3 iterations)
- `stages/s3/` - Epic Planning (redesigned with 3 phases)
- `stages/s4/` - Feature Testing Strategy (NEW)
- `stages/s5/` - Implementation Planning (22 iterations, testing moved to S4)
```

#### Section: Critical Rules Summary

**Update "Always Required" section:**
```markdown
✅ **Consistency Loop completion** (3 consecutive clean rounds, no deferred issues)
✅ **All embedded gates pass** before proceeding (Gates 1, 2, 4a, 7a, 23a)
```

**Update "Never Allowed" section:**
```markdown
❌ **Skip Consistency Loops** (quality validation is mandatory)
❌ **Defer issues for "later"** (no deferred issues principle - fix ALL immediately)
❌ **Exceed 10 rounds without escalation** (maximum round limit safety mechanism)
```

#### Section: Common Anti-Patterns to Avoid

**Add new anti-pattern:**
```markdown
### Anti-Pattern 3: Deferring Issues in Consistency Loops

**WRONG APPROACH:**
1. Run Consistency Loop Round 1, find 5 issues
2. Mark 3 as "high priority", 2 as "low priority - defer for later"
3. Fix only the 3 high priority issues
4. Proceed to Round 2 with 2 known issues

**CORRECT APPROACH:**
1. Run Consistency Loop Round 1, find 5 issues
2. Fix ALL 5 issues (no priority classification)
3. Proceed to Round 2 only when ZERO issues remain
4. If Round 2 finds new issues, fix ALL before Round 3

**Key Distinction:** "No deferred issues" means exactly that - zero tolerance for known issues
```

### Files Affected
**UPDATE:**
1. `CLAUDE.md` - Complete workflow section updates

### Estimated Time
1-2 hours

### Priority
**HIGH** - Required for agents to follow new workflow correctly

### Dependencies
Must complete Proposals 1, 2, 4, 5, 6, 7 first (stage redesigns and Consistency Loop protocol)

---

## PROPOSAL 10: Create Supporting Templates and Reference Materials

### What
Create templates and reference materials to support the new workflow.

### Why
Templates accelerate feature development and ensure consistency across epics. Consistency Loop logging provides audit trail and demonstrates "no deferred issues" principle. Research notes template ensures all features document integration points and external dependencies. Test strategy template preserves proven quality level from current S5 Iteration 8 template (~80 lines). Without templates, agents must recreate structure each time, leading to inconsistent documentation and quality variation.

### Files to Create

1. **`CONSISTENCY_LOOP_LOG_template.md`**
   - Track Consistency Loop rounds per feature/epic
   - Document issues found per round
   - Show consecutive clean count
   - Demonstrate "no deferred issues" principle
   - Location: `feature-updates/guides_v2/templates/`

2. **`FEATURE_RESEARCH_NOTES_template.md`**
   - Research notes from S2.P1.I1
   - Findings, integration points, questions
   - External library compatibility section
   - Location: `feature-updates/guides_v2/templates/`

3. **`feature_test_strategy_template.md`** - **EXPANDED (FIX FOR ISSUE #5)**
   - Template for S4 test strategy output file
   - **MUST include all detail from current s5_p2_i1_test_strategy.md Iteration 8 template**
   - Coverage matrix, test categories, traceability
   - Will be merged into implementation_plan.md during S5
   - Location: `feature-updates/guides_v2/templates/`

**Content Requirements for test_strategy_template.md:**

The template MUST include:
- **Unit Tests section** with format for 5-7 example test cases (Given/When/Then format)
- **Integration Tests section** with format for 2-3 example test cases
- **Edge Case Tests section** with format for 4-5 example test cases
- **Regression Tests section** with format for 2 example test cases
- **Test task template** showing how to add tests to implementation tasks
- Total: ~80-100 lines (matching current S5 Iteration 8 template detail level)

**Reference current template:** `stages/s5/s5_p2_i1_test_strategy.md` lines 26-103 (78 lines)

**Why this matters:** Template quality directly affects test strategy quality. Current template has proven effective over multiple epics. New template must preserve this quality level.

### Estimated Time
1-2 hours

### Priority
**LOW** - Nice to have, not blocking (except test_strategy_template.md which is MEDIUM priority)

---

## Summary of Proposals

| # | Proposal | Priority | Time | Dependencies |
|---|----------|----------|------|--------------|
| 1 | Consistency Loop Master Protocol | CRITICAL | 1-2h | None |
| 2 | Consistency Loop Context Variants | HIGH | 4-6h | Proposal 1 |
| 3 | S1 Discovery Phase Update | MEDIUM | 1h | Proposal 1, 2 |
| 4 | S2 Redesign (Feature Planning) | CRITICAL | 4-6h | Proposal 1, 2 |
| 5 | S3 Redesign (Epic Planning) | CRITICAL | 2-3h | Proposal 1, 2 |
| 6 | S4 New Stage (Feature Testing) | CRITICAL | 2-3h | Proposal 1, 2 |
| 7 | S5 Update (Remove Testing) | HIGH | 2-3h | Proposal 6 |
| 8 | S7/S9 QC Updates | MEDIUM | 1-2h | Proposal 2 |
| 9 | CLAUDE.md Updates | HIGH | 1-2h | Proposals 4-7 |
| 10 | Templates & References | LOW-MEDIUM | 1-2h | None |

**Total Estimated Time:** 19-30 hours

---

## Recommended Execution Order

### Phase 1: Foundation (5-8 hours)
1. Proposal 1: Consistency Loop Master Protocol
2. Proposal 2: Consistency Loop Context Variants

**COMMIT AFTER PHASE 1**

### Phase 2: Critical Stage Redesigns (8-12 hours)
3. Proposal 6: S4 New Stage (100% audit-confirmed, start here!)
4. Proposal 4: S2 Redesign
5. Proposal 5: S3 Redesign

**COMMIT AFTER PHASE 2**

### Phase 3: Stage Updates (3-5 hours)
6. Proposal 7: S5 Update
7. Proposal 9: CLAUDE.md Updates

**COMMIT AFTER PHASE 3**

### Phase 4: Refinements (3-5 hours)
8. Proposal 3: S1 Discovery Update
9. Proposal 8: S7/S9 QC Updates
10. Proposal 10: Templates

**COMMIT AFTER PHASE 4**

---

## All Issues Fixed Summary

**Round 3 Critical Issues (3):**
- ✅ Issue #35: S5 renumbering math corrected (Round 2 = I8-I13, not I8-I11)
- ✅ Issue #2: "Correct Status Progression" 9-step protocol added to S2.P1.I2
- ✅ Issue #3: Agent-to-agent communication protocol added to S2.P1.I3

**Round 3 Important Issues (4):**
- ✅ Issue #36: Gates 4a/7a clarified (embedded in S5 Round 1 Consistency Loop)
- ✅ Issue #37: Maximum round limit (10) added with escalation protocol
- ✅ Issue #1: Research notes requirement clarified (REQUIRED with rare exceptions)
- ✅ Issue #4: S3.P1 expanded with detail from current S4

**Round 3 Minor Issues (6):**
- ✅ Issue #32: Fix-introduces-issue example added to Proposal 1
- ✅ Issue #33: Acceptance criteria approval made explicit at Gate 3
- ✅ Issue #34: Pairwise comparison matrix file location specified
- ✅ Issue #5: test_strategy_template.md content requirements specified
- ✅ Issue #38: Total spec rejection handling added to Gate 3
- ✅ Issue #39: Missing test_strategy.md error handling added to S5.P1.I1

---

## Next Steps

**For User:**
1. Review these V3 proposals with all Rounds 3-8 issues fixed (22 issues total + 1 design decision documented)
2. Approve/Reject/Modify individual proposals
3. Confirm execution order
4. Authorize starting Phase 1

**For Agent:**
1. Wait for user approval
2. Execute approved proposals in order
3. Commit after each phase
4. Validate against user memory throughout
5. Apply "no deferred issues" principle during execution

---

**Status:** FINAL V3 proposals with ALL Rounds 3-8 issues fixed (22 issues + 1 design decision), ready for user approval and implementation
**Source Authority:** my_memory.md + user clarifications from Rounds 1-8 + all consistency review findings + 11 Consistency Loop rounds (Rounds 9-10 clean, Round 11 found 1 minor legacy text issue)
**All 44 issues from three consistency review rounds have been addressed**
