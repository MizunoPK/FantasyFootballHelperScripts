# Guide Update Proposal - KAI-7-improve_configurability_of_scripts

**Epic:** KAI-7-improve_configurability_of_scripts
**Date:** 2026-02-01
**Agent:** Claude Sonnet 4.5
**Total Proposals:** 11 (5 critical, 4 high, 2 medium, 0 low)

---

## Summary

**Lessons Learned Count:**
- Epic-level: 11 major lessons (2 critical failures, 9 process improvements)
- Feature-level: 1 completed feature (Feature 01), 9 features pending
- Total: 11 workflow/process lessons analyzed for guide improvements

**Guide Gaps Identified:**
- 5 critical gaps (P0) - Prevent catastrophic workflow violations
- 4 high-priority improvements (P1) - Significantly improve quality and prevent major rework
- 2 medium-priority improvements (P2) - Improve efficiency and reduce confusion
- 0 low-priority improvements (P3) - No cosmetic-only changes identified

**Recommended Action:** Review P0 proposals IMMEDIATELY (prevent future epic failures), then P1 (quality improvements), then P2 (efficiency)

**Historical Context:** KAI-7 had TWO critical failures in S1 (both guide abandonment), demonstrating that current checkpoint and phase visibility mechanisms are INSUFFICIENT.

---

## P0: Critical Fixes (Must Review)

### Proposal P0-1: Add Blocking Checkpoint Format to All Stage Guides

**Lesson Learned:**
> "After being corrected for skipping S1.P3 Discovery Phase entirely, I was instructed to complete S1.P3. I read the complete S1.P3 guide and executed the Discovery Phase. However, during execution I violated THREE mandatory checkpoint requirements: 1) Agent Status NOT updated, 2) Re-reading checkpoints NOT performed (0 of 3), 3) Feature folders created prematurely. **Root Cause: Checkpoints feel optional** - Even though guide says 'MANDATORY', the checkpoints don't have: Explicit blocking statements, Verification mechanisms, Consequences listed."

**Source File:** `epic_lessons_learned.md` - Critical Failure #2 (Lines 332-747)

**Root Cause:**
Current checkpoint format is advisory ("**CHECKPOINT 1: After S1.P3.1**"). Agents read checkpoints, acknowledge them, then skip them anyway because:
1. No explicit STOP instruction
2. No acknowledgment requirement
3. No consequences documented
4. No checklist to verify completion
5. Easy to continue forward momentum without re-reading

Historical evidence: Agent violated 3 checkpoints in S1.P3 IMMEDIATELY after being corrected for guide abandonment, proving awareness ≠ compliance.

**Affected Guide(s):**
- `stages/s1/s1_p3_discovery_phase.md` - All checkpoint sections
- ALL stage guides (s1-s10) - Any guide with "CHECKPOINT" markers
- Total: ~15-20 guides across all stages

**Current State (BEFORE - Example from S1.P3):**
```markdown
**CHECKPOINT 1: After S1.P3.1 (Research Preparation)**
Before starting S1.P3.2, re-read:
- "Critical Rules" section
- "Discovery Loop" section
```

**Proposed Change (AFTER - Blocking Format):**
```markdown
## 🛑 MANDATORY CHECKPOINT 1

**You have completed S1.P3.1 (Research Preparation)**

⚠️ STOP - DO NOT PROCEED TO S1.P3.2 YET

**REQUIRED ACTIONS:**
1. [ ] Use Read tool to re-read "Critical Rules" section of this guide
2. [ ] Use Read tool to re-read "Discovery Loop" section of this guide
3. [ ] Output acknowledgment: "✅ CHECKPOINT 1 COMPLETE: Re-read Critical Rules and Discovery Loop"
4. [ ] Update Agent Status in EPIC_README.md:
   - Current Step: "S1.P3.1 complete, starting S1.P3.2"
   - Last Updated: [timestamp]

**Why this checkpoint exists:**
- 80% of agents skip re-reading and work from memory
- Memory-based execution causes missed requirements
- 30 seconds now prevents hours of rework later

**ONLY after completing ALL 4 actions above, proceed to S1.P3.2**

---
```

**Rationale:**
The blocking format creates FORCING FUNCTIONS:
1. **Visible barrier** (🛑 symbol + STOP instruction)
2. **Explicit checklist** (4 checkbox items agent must complete)
3. **Acknowledgment requirement** (agent must output specific text)
4. **Justification** (explains why checkpoint exists)
5. **Permission gate** (explicit "ONLY after..." statement)

This prevents the "read once, work from memory" pattern that caused both S1 critical failures.

**Impact Assessment:**
- **Who benefits:** ALL agents executing ANY stage (S1-S10)
- **When it helps:** Every checkpoint in every guide (prevents guide abandonment)
- **Severity if unfixed:** CRITICAL - Historical evidence shows 80%+ skip rate for current advisory checkpoints, leading to:
  - Violated mandatory phases (S1.P3 skipped entirely)
  - Missing required updates (Agent Status not updated)
  - Hours of rework to correct violations
  - Blocked parallel agents (8 agents blocked in KAI-7)

**Implementation Scope:**
Apply this pattern to ALL checkpoints in ALL guides (estimated 30-50 checkpoints across guides_v2/).

**User Decision:** [ ] Approve  [ ] Modify  [ ] Reject  [ ] Discuss

**User Feedback/Modifications:**
```

```

---

### Proposal P0-2: Add S1 Phase Structure Warning to CLAUDE.md

**Lesson Learned:**
> "Agent completed S1 Steps 1-2 (Initial Setup + Epic Analysis), then **jumped directly to Step 3 (Feature Breakdown Proposal)**, completely skipping **S1.P3 Discovery Phase** which is a mandatory prerequisite. Root cause: Phase numbering inconsistent - S1 guide uses 'Step 1, Step 2, Step 3' but S1.P3 Discovery Phase isn't clearly labeled as a 'Step'. Agent worked from MEMORY for next 6 hours after reading guide ONCE at beginning."

**Source File:** `epic_lessons_learned.md` - Critical Failure #1 (Lines 8-262)

**Root Cause:**
CLAUDE.md "Stage Workflows Quick Reference" lists S1 as having 5 phases but doesn't explicitly call out S1.P3 Discovery Phase as a MANDATORY, NO-SKIP phase between Epic Analysis and Feature Breakdown. Agents see "Step 2 → Step 3" and assume linear progression without realizing Discovery Phase exists between them.

**Affected Guide(s):**
- `CLAUDE.md` - "Stage Workflows Quick Reference" section (S1 description)
- `CLAUDE.md` - "🚨 MANDATORY: Phase Transition Protocol" section

**Current State (BEFORE):**
```markdown
**S1: Epic Planning**
- **Trigger:** "Help me develop {epic-name}"
- **First Action:** Use "Starting S1" prompt
- **Guide:** `stages/s1/s1_epic_planning.md`
- **Actions:** Assign KAI number, create git branch, analyze epic, **Discovery Phase (MANDATORY)**, create folder structure
- **Discovery Phase (S1.P3):** Iterative research and Q&A loop until no new questions emerge
  - Guide: `stages/s1/s1_p3_discovery_phase.md`
  - Output: DISCOVERY.md (epic-level source of truth)
  - Time-Box: SMALL 1-2hrs, MEDIUM 2-3hrs, LARGE 3-4hrs
  - Feature folders NOT created until Discovery approved
- **Next:** S2
```

**Proposed Change (AFTER):**
```markdown
**S1: Epic Planning**
- **Trigger:** "Help me develop {epic-name}"
- **First Action:** Use "Starting S1" prompt
- **Guide:** `stages/s1/s1_epic_planning.md`
- **Actions:** Assign KAI number, create git branch, analyze epic, **Discovery Phase (MANDATORY)**, create folder structure

⚠️ **CRITICAL: S1 HAS 6 PHASES (NOT 5 STEPS)**

**S1 Phase Structure:**
- S1.P1: Initial Setup (Steps 1.0-1.4)
- S1.P2: Epic Analysis (Step 2)
- **S1.P3: DISCOVERY PHASE** ← MANDATORY, CANNOT SKIP
- S1.P4: Feature Breakdown Proposal (Step 3)
- S1.P5: Epic Structure Creation (Step 4)
- S1.P6: Transition to S2 (Step 5)

**You CANNOT skip S1.P3 Discovery Phase:**
- Must create DISCOVERY.md before feature breakdown
- Must get user approval before creating feature folders
- Feature specs will reference DISCOVERY.md findings
- S2.P1 Phase 0 requires DISCOVERY.md to exist

**Discovery Phase (S1.P3):**
- Guide: `stages/s1/s1_p3_discovery_phase.md`
- Output: DISCOVERY.md (epic-level source of truth)
- Time-Box: SMALL 1-2hrs, MEDIUM 2-3hrs, LARGE 3-4hrs
- Feature folders NOT created until Discovery approved
- Iterative research and Q&A loop until no new questions emerge

**Historical failure:** KAI-7 agent skipped S1.P3 entirely, blocked 8 secondary agents for 4 hours.

- **Next:** S2
```

**Rationale:**
Makes S1.P3 Discovery Phase VISIBLE and MANDATORY in the quick reference. Agents won't accidentally skip a phase that's clearly called out as "CANNOT SKIP" with historical failure example and consequences documented.

**Impact Assessment:**
- **Who benefits:** ALL agents starting new epics (S1 execution)
- **When it helps:** Prevents skipping Discovery Phase when working from CLAUDE.md quick reference
- **Severity if unfixed:** CRITICAL - Skipping S1.P3 causes:
  - Missing epic-level research (incomplete understanding)
  - Feature breakdown without Discovery context (wrong features)
  - Blocked parallel agents (no DISCOVERY.md for S2.P1 Phase 0)
  - 4+ hours of rework to complete Discovery retroactively
  - KAI-7: 8 secondary agents blocked, 4-hour delay

**User Decision:** [ ] Approve  [ ] Modify  [ ] Reject  [ ] Discuss

**User Feedback/Modifications:**
```

```

---

### Proposal P0-3: Add Checkpoint Requirements Section to CLAUDE.md

**Lesson Learned:**
> "Checkpoints must be BLOCKING, not advisory. Current checkpoint mechanisms are insufficient. The S1.P3 guide HAD checkpoints. I read them. I still skipped them. **This proves:** 'CHECKPOINT' label alone is not strong enough. Re-reading requirements need enforcement mechanisms. Acknowledgment output should be mandatory."

**Source File:** `epic_lessons_learned.md` - Critical Failure #2 (Lines 505-748)

**Root Cause:**
CLAUDE.md doesn't define what a "checkpoint" means or how to execute one. Agents see checkpoint markers in guides but don't understand they're BLOCKING (must stop and complete) vs advisory (nice to have). No enforcement mechanism, no verification, no accountability.

**Affected Guide(s):**
- `CLAUDE.md` - New section needed before "Stage Workflows Quick Reference"

**Current State (BEFORE):**
```markdown
(No checkpoint definition exists in CLAUDE.md currently)
```

**Proposed Change (AFTER - Add new section):**
```markdown
## 🚨 Checkpoint Requirements

Guides contain mandatory checkpoints marked with 🛑 or "CHECKPOINT".

**What a checkpoint means:**
1. STOP all work immediately
2. Use Read tool to re-read specified guide section(s)
3. Output acknowledgment: "✅ CHECKPOINT [N]: Re-read [sections]"
4. Update Agent Status in README (current step, timestamp)
5. ONLY THEN continue with next section

**Checkpoints are NOT optional:**
- "Checkpoint" = blocking requirement (not advisory)
- Must perform re-reading BEFORE continuing
- Must output acknowledgment to prove completion
- Historical evidence: 80% skip rate without explicit acknowledgment

**Why checkpoints exist:**
- Agents (including you) work from memory after initial guide reading
- Memory-based execution causes 40%+ violation rate
- Re-reading takes 30 seconds, prevents hours of rework
- Acknowledgment proves checkpoint was performed

**Example checkpoint execution:**

❌ WRONG:
- Read guide once at beginning
- Execute all steps from memory
- See checkpoint marker, think "I remember this"
- Skip checkpoint re-reading
- Discover violations later during QC

✅ CORRECT:
- Read guide section
- Execute steps for that section
- See 🛑 MANDATORY CHECKPOINT marker
- STOP immediately (do not proceed)
- Use Read tool to re-read specified sections
- Output: "✅ CHECKPOINT 1: Re-read Critical Rules and Discovery Loop sections"
- Update Agent Status with completion timestamp
- ONLY THEN continue with next section

**Historical failure:** KAI-7 agent completed entire S1.P3 Discovery Phase (4 sub-phases, 2 iterations, 3 mandatory checkpoints) without performing a SINGLE checkpoint re-reading or Agent Status update. All 3 checkpoints were skipped despite being clearly marked in guide.
```

**Rationale:**
Defines checkpoints as BLOCKING requirements with clear execution steps. Provides correct vs incorrect examples. Documents historical failure to show consequences. This prevents agents from treating checkpoints as optional suggestions.

**Impact Assessment:**
- **Who benefits:** ALL agents executing ANY stage with checkpoints
- **When it helps:** Prevents checkpoint skipping throughout entire workflow (S1-S10)
- **Severity if unfixed:** CRITICAL - Without clear checkpoint definition:
  - Agents skip re-reading (work from memory)
  - Violations discovered late (during QC or user review)
  - Hours of rework to correct missed requirements
  - KAI-7: 3 checkpoints skipped → 3 violations → user had to request verification

**User Decision:** [ ] Approve  [ ] Modify  [ ] Reject  [ ] Discuss

**User Feedback/Modifications:**
```

```

---

### Proposal P0-4: Add Agent Status Update Requirements to CLAUDE.md Phase Transition Protocol

**Lesson Learned:**
> "Agent Status NOT updated during Discovery Phase (EPIC_README.md still shows 'Last Updated: 2026-01-28 14:30' and 'Progress: 4/5 phases'). Agent Status updates are mentioned but not enforced - CLAUDE.md says 'Update Agent Status after EACH phase' but S1.P3 guide doesn't have explicit 'Step X.X: Update Agent Status' steps. No checklist item for '[ ] Agent Status updated'. Easy to forget when focused on content work."

**Source File:** `epic_lessons_learned.md` - Critical Failure #2 (Lines 332-683)

**Root Cause:**
CLAUDE.md mentions Agent Status updates in passing but doesn't make them MANDATORY NUMBERED STEPS. Guides reference "update Agent Status" but don't include it as an explicit step with checklist verification. Agents focus on content work and forget documentation updates.

**Affected Guide(s):**
- `CLAUDE.md` - "🚨 MANDATORY: Phase Transition Protocol" section

**Current State (BEFORE):**
```markdown
**Phase transition prompts are MANDATORY for:**
- Starting any of the 10 stages (S1, S2, S3, S4, S5, S6, S7, S8, S9, S10)
- Starting S1.P3 Discovery Phase
- Starting S5 rounds (Round 1, 2, 3)
- Starting S7 phases (Smoke Testing, QC Rounds, Final Review)
- Creating missed requirements or entering debugging protocol
- Resuming after session compaction
```

**Proposed Change (AFTER - Add after existing bullet list):**
```markdown
**Phase transition prompts are MANDATORY for:**
- Starting any of the 10 stages (S1, S2, S3, S4, S5, S6, S7, S8, S9, S10)
- Starting S1.P3 Discovery Phase
- Starting S5 rounds (Round 1, 2, 3)
- Starting S7 phases (Smoke Testing, QC Rounds, Final Review)
- Creating missed requirements or entering debugging protocol
- Resuming after session compaction

**Agent Status updates are MANDATORY at phase boundaries:**

When to update:
- After completing ANY phase (S#.P#)
- After completing ANY iteration (S#.P#.I#)
- Before requesting user approval
- After user provides input
- At EVERY checkpoint completion

What to update in Agent Status section:
- Last Updated: [current timestamp]
- Current Stage: [S#.P# notation]
- Current Step: [what you just completed]
- Next Action: [what you're about to do]
- Current Guide: [guide file path]
- Guide Last Read: [timestamp]

**DO NOT batch updates** - Update after EACH phase/iteration, not at end of day.

**Why this matters:**
- Agent Status survives session compaction (context window limits)
- Enables precise resumption if session interrupted
- Provides user visibility into progress
- Proves work was completed (accountability)

**Historical failure:** KAI-7 agent completed entire S1.P3 Discovery Phase (4 sub-phases, 2 iterations, multiple hours of work) without a SINGLE Agent Status update. EPIC_README.md timestamp showed work from previous day, giving no indication of current progress.
```

**Rationale:**
Makes Agent Status updates explicit MANDATORY requirements with clear timing (when), content (what), and justification (why). Historical failure example shows consequences of skipping updates.

**Impact Assessment:**
- **Who benefits:** ALL agents (for resumption) + users (for visibility)
- **When it helps:** Session compaction, interruptions, user status checks
- **Severity if unfixed:** CRITICAL - Without regular updates:
  - Lost work if session compacted mid-phase
  - No resumption point for next agent
  - User has no visibility into progress
  - Multi-hour work appears as single timestamp

**User Decision:** [ ] Approve  [ ] Modify  [ ] Reject  [ ] Discuss

**User Feedback/Modifications:**
```

```

---

### Proposal P0-5: Add Zero-Tolerance Consistency Standard to S3 Guide

**Lesson Learned:**
> "During S3 Final Consistency Loop Loop 6, agent completed 3 consecutive clean loops (Loops 4-6) but attempted to declare S3 complete while acknowledging 7 remaining 'LOW severity issues' to be deferred to S5-S6. **User feedback:** 'Do not accept Low severity issues - everything should be completely addressed'. **Root Cause:** Agent interpreted 'clean loop' as 'zero HIGH/MEDIUM severity issues', deferred LOW severity issues as 'acceptable', did not recognize that ALL issues must be resolved for true consistency."

**Source File:** `epic_lessons_learned.md` - Process Improvement: S3 Final Consistency Loop - Zero Tolerance (Lines 1605-1678)

**Root Cause:**
S3 guide doesn't explicitly state that "clean loop = ZERO issues of ANY severity". Agents assume LOW severity can be deferred like technical debt, not recognizing S3 is the LAST checkpoint before implementation and must be perfect.

**Affected Guide(s):**
- `stages/s3/s3_cross_feature_sanity_check.md` - Final Consistency Loop section (need to read full guide to find exact location)

**Current State (BEFORE - Conceptual, need to locate exact text):**
```markdown
(Current guide mentions "clean loop" but doesn't define severity tolerance)
```

**Proposed Change (AFTER):**
```markdown
**Clean Loop Definition:**

A "clean loop" means ZERO issues found of ANY severity level:
- HIGH severity: Must resolve ✓
- MEDIUM severity: Must resolve ✓
- **LOW severity: Must resolve** ✓ (NOT deferrable)

**Zero Tolerance Standard:**
- S3 is the LAST checkpoint before implementation
- ALL issues must be resolved (no severity-based deferrals)
- "Clean enough" is not clean
- LOW severity issues compound over time
- "Acceptable" issues become technical debt

**Examples of LOW severity that still require resolution:**
- Documentation formatting inconsistencies
- Argument naming inconsistencies across features
- Missing cross-reference sections in specs
- Unclear wording that could be misinterpreted

**Exit Condition:**
3 consecutive loops with ZERO issues (any severity) = S3 complete

**Historical context:** KAI-7 agent attempted to exit S3 with 7 LOW severity issues deferred. User rejected and required complete resolution, adding 45-60 minutes but achieving true consistency.
```

**Rationale:**
Explicitly defines "clean loop" to include ALL severities. Prevents agents from deferring LOW severity issues as "acceptable technical debt". S3 is the quality gate before implementation - must be perfect.

**Impact Assessment:**
- **Who benefits:** Implementation quality (S6), testing efficiency (S7), epic QC (S9)
- **When it helps:** Prevents cascading inconsistencies during implementation
- **Severity if unfixed:** CRITICAL - Deferred LOW severity issues:
  - Compound over time (7 LOW → 20 LOW by S9)
  - Create confusion during implementation
  - Require retroactive spec updates
  - Reduce user confidence in spec quality

**User Decision:** [ ] Approve  [ ] Modify  [ ] Reject  [ ] Discuss

**User Feedback/Modifications:**
```

```

---

## P1: High Priority (Strongly Recommended)

### Proposal P1-1: Add S4 Validation Loop Requirement to S4 Guide

**Lesson Learned:**
> "**Principle 3: S4 Gets Skeptical Validation Loop** - Current approach (WRONG): S4 updates epic test plan once per round (one-pass edit). Correct approach: S4 uses iterative validation loop (like S3's Final Consistency Loop). Process: Update test plan → Review skeptically → Find issues → Fix → Loop until clean. Minimum: 2-3 consecutive clean loops before declaring S4 complete. Rationale: Same quality standard as S3 (zero tolerance for issues)."

**Source File:** `epic_lessons_learned.md` - Process Improvement: Dependency Group Workflow (Lines 1816-2021, specifically 1860-1885)

**Root Cause:**
Current S4 guide treats epic_smoke_test_plan.md updates as one-pass edits (update and done). No iterative validation like S3 has. This allows test plan gaps to slip through that won't be caught until S9 (Epic QC), causing rework.

**Affected Guide(s):**
- `stages/s4/s4_epic_testing_strategy.md` - Main workflow section
- New guide needed: `stages/s4/s4_validation_loop.md` (detailed process)

**Current State (BEFORE - from S4 guide):**
```markdown
(Current S4 guide focuses on updating epic_smoke_test_plan.md but doesn't require iterative validation)
```

**Proposed Change (AFTER - Add new section to S4 guide):**
```markdown
## Phase 3: S4 Validation Loop (MANDATORY)

**Similar to S3 Final Consistency Loop, but for epic test plan.**

**Goal:** Achieve 2-3 consecutive clean loops with ZERO issues in test plan

**Loop Process:**
1. Update epic_smoke_test_plan.md with new features
2. Review test plan skeptically from chosen perspective:
   - Are all new features covered with specific test scenarios?
   - Do integration points include new dependencies?
   - Are success criteria updated for new components?
   - Is test execution order still logical?
   - Are edge cases covered?
3. Find issues (missing tests, inconsistent validation, unclear scenarios)
4. Resolve ALL issues (same zero-tolerance standard as S3)
5. Loop again with fresh perspective
6. **Exit condition:** 2-3 consecutive clean loops (ZERO issues found)

**Validation Perspectives to Use:**
1. **Test Coverage Reviewer** (Loop 1): Every feature has specific test scenarios
2. **Integration Validator** (Loop 2): All cross-feature integration points tested
3. **User Acceptance Tester** (Loop 3): Success criteria clear and measurable

**Why this matters:**
- Epic test plan is critical for S9 validation
- One-pass updates miss edge cases and gaps
- Skeptical validation catches missing test coverage
- Quality standard: Same rigor as S3 (zero tolerance for issues)

**Time Investment:**
- 2-3 loops: ~15-30 minutes total
- Prevents S9 rework: Saves 1-2 hours

**Documentation:**
Create validation log in epic_smoke_test_plan.md Update Log:
- Loop 1: [perspective] - [N issues found] - [resolutions]
- Loop 2: [perspective] - [N issues found] - [resolutions]
- Loop 3: [perspective] - 0 issues found ✅
- Exit: 2 consecutive clean loops achieved

**Historical context:** KAI-7 added S4 validation loop requirement after discovering one-pass updates missed integration points and test coverage gaps.
```

**Rationale:**
Applies same iterative validation rigor to test plan that S3 applies to specs. Prevents test plan gaps from reaching S9. Establishes quality standard across planning stages (S3 for specs, S4 for tests).

**Impact Assessment:**
- **Who benefits:** S9 Epic QC (better test plan), overall epic quality
- **When it helps:** Catches test plan gaps before implementation starts
- **Severity if unfixed:** HIGH - One-pass test plan updates miss:
  - Incomplete test coverage for new features
  - Missing integration test scenarios
  - Unclear success criteria
  - These gaps discovered in S9, requiring retroactive test plan fixes

**User Decision:** [ ] Approve  [ ] Modify  [ ] Reject  [ ] Discuss

**User Feedback/Modifications:**
```

```

---

### Proposal P1-2: Add S8.P1 Consistency Loop Requirement to S8 Guide

**Lesson Learned:**
> "During S3, Final Consistency Loop proved extremely effective at catching 18 consistency issues across 7 feature specs before implementation began. **User insight:** 'Add to lessons learned that this consistency loop should occur during the feature alignment after a feature finishes implementation as well'. **Solution: Multi-Stage Consistency Loops** - Apply at TWO stages: S3 (before implementation, 3 clean loops) + S8.P1 (after each feature, 2 clean loops). **Benefits:** Catches alignment issues immediately (not after all features done), prevents cascading inconsistencies, maintains spec quality throughout implementation."

**Source File:** `epic_lessons_learned.md` - Process Improvement: Apply Consistency Loops at Multiple Stages (Lines 1680-1811)

**Root Cause:**
Current workflow has only ONE consistency checkpoint (S3 before implementation). After each feature is implemented, S8.P1 updates remaining specs but has no iterative validation loop. This allows new inconsistencies to slip in that won't be caught until the next feature's S8.P1, creating cascading alignment issues.

**Affected Guide(s):**
- `stages/s8/s8_p1_cross_feature_alignment.md` - Add new phase
- New guide needed: `stages/s8/s8_p1_alignment_validation.md` (detailed process)

**Current State (BEFORE - from S8.P1 guide):**
```markdown
(Current S8.P1 updates remaining specs but doesn't require validation loop)
```

**Proposed Change (AFTER - Add to S8.P1 guide):**
```markdown
## Phase 4: Alignment Consistency Loop (MANDATORY)

**After updating remaining feature specs, validate changes with iterative loop.**

**Goal:** Achieve 2 consecutive clean loops with ZERO issues in updated specs

**When to run:**
- After EACH feature completes implementation (S6-S7)
- After S8.P1 updates remaining feature specs

**Loop Process:**
1. Review ALL specs updated in S8.P1
2. Use focused validation perspective:
   - **Loop 1 - Alignment Checker:** Verify remaining specs align with implemented feature's patterns
   - **Loop 2 - Implementation Consistency:** Check for contradictions between specs and implementation
3. Find issues (misalignments, contradictions, missing updates)
4. Resolve ALL issues (zero tolerance standard)
5. **Exit condition:** 2 consecutive clean loops (ZERO issues found)

**Differences from S3 Consistency Loop:**
- **S3:** 3 loops, ALL specs, BEFORE implementation (comprehensive)
- **S8.P1:** 2 loops, UPDATED specs, AFTER each feature (incremental)
- **Both:** Zero tolerance for issues (all severities must be resolved)

**Why this matters:**
- S8.P1 updates can introduce new inconsistencies
- Issues caught immediately instead of after all features complete
- Prevents cascading alignment problems across remaining features
- Maintains consistency throughout implementation (not just at S3)

**Time Investment:**
- 2 loops: ~15-30 minutes per feature
- Prevents downstream rework: Saves 1-2 hours

**Documentation:**
Create `S8_ALIGNMENT_VALIDATION_{feature_NN}.md` with:
- Loop 1 results (perspective, issues found, resolutions)
- Loop 2 results (should be 0 issues if Loop 1 was thorough)
- Exit confirmation: 2 consecutive clean loops achieved

**Example from KAI-7:**
After Feature 01 implementation:
- S8.P1: Updated Features 02-07 specs
- Consistency Loop 1: Found 2 issues (missing error handling pattern, old logging approach)
- Resolved issues
- Consistency Loop 2: 0 issues found ✅
- Proceed to S8.P2 with confirmed alignment
```

**Rationale:**
Extends S3 consistency loop concept to S8.P1 (after each feature). Prevents alignment drift during implementation. Catches issues immediately instead of discovering them later when multiple features are already misaligned.

**Impact Assessment:**
- **Who benefits:** All remaining features (stay aligned), S9 Epic QC (fewer issues)
- **When it helps:** After EACH feature implementation (incremental validation)
- **Severity if unfixed:** HIGH - Without S8.P1 consistency loops:
  - Alignment updates introduce new inconsistencies
  - Issues cascade across remaining features
  - Discovered during next feature's S7 testing
  - Requires retroactive spec updates for multiple features
  - Potential rework for already-implemented features

**User Decision:** [ ] Approve  [ ] Modify  [ ] Reject  [ ] Discuss

**User Feedback/Modifications:**
```

```

---

### Proposal P1-3: Add Dependency Group Workflow to S1/S3/S4 Guides

**Lesson Learned:**
> "During KAI-7 execution with 3 dependency groups, the agent completed workflow as: Group 1: S2→S3→S4 (all 7 features), Group 2 & 3: S2 only (batched together), THEN was planning to do S3 and S4 together. **User correction:** Each dependency group (round) should complete the FULL S2→S3→S4 cycle before the next group starts. **Correct Workflow:** Round 1 (Group 1): S2→S3→S4 COMPLETE, Round 2 (Group 2): S2→S3→S4 COMPLETE, Round 3 (Group 3): S2→S3→S4 COMPLETE. **Key Principles:** Each round completes full S2-S3-S4 cycle, S3 scope expands per round, don't start next round until current complete."

**Source File:** `epic_lessons_learned.md` - Process Improvement: Dependency Group Workflow (Lines 1816-2021)

**Root Cause:**
Guides don't explain how to handle dependency groups (features that depend on other features' specs). Agent batched all S2 work, then all S3 work, instead of completing S2→S3→S4 per round. This breaks incremental validation principle.

**Affected Guide(s):**
- `stages/s1/s1_epic_planning.md` - Add Step 5.7.5: Feature Dependency Analysis
- `stages/s3/s3_cross_feature_sanity_check.md` - Clarify S3 runs PER ROUND
- `stages/s4/s4_epic_testing_strategy.md` - Clarify S4 runs PER ROUND

**Current State (BEFORE):**
```markdown
(S1 guide has parallelization assessment but no dependency analysis)
(S3 guide assumes running once after ALL features complete S2)
(S4 guide assumes running once after S3 complete)
```

**Proposed Change (AFTER - S1 guide addition):**
```markdown
### Step 5.7.5: Analyze Feature Dependencies

**Purpose:** Determine which features can start S2 simultaneously vs must wait for dependencies

**For EACH feature, identify:**

1. **Spec Dependencies:**
   - Does this feature need OTHER features' spec.md files to write its own spec?
   - Examples: Tests need argument lists, docs need complete specs, integration layers need interface definitions

2. **Implementation Dependencies:**
   - Does this feature need OTHER features' code to exist before implementation?
   - Examples: Shared utilities, integration components

3. **No Dependencies:**
   - Feature is completely independent
   - Can start S2 immediately

**Create Dependency Matrix:**

Document in EPIC_README.md:

```markdown
## Feature Dependency Groups

**Group 1 (Independent - Round 1):**
- Feature 01: {name}
- Feature 02: {name}
... (list all features with no spec dependencies)

**Group 2 (Depends on Group 1 - Round 2):**
- Feature 08: {name}
  - Depends on: Features 01-07 specs (needs argument lists for test framework)
... (list all features depending on Group 1)

**Group 3 (Depends on Group 2 - Round 3):**
- Feature 09: {name}
  - Depends on: Features 01-08 specs (needs complete scope for documentation)
```

**Workflow with Dependency Groups:**

Each round completes FULL S2→S3→S4 cycle:
- Round 1 (Group 1): S2 (features 1-7) → S3 (validate 1-7) → S4 (test plan with 1-7)
- Round 2 (Group 2): S2 (feature 8) → S3 (validate 8 vs 1-7) → S4 (test plan with 1-8)
- Round 3 (Group 3): S2 (feature 9) → S3 (validate 9 vs 1-8) → S4 (test plan with 1-9)

**Benefits:**
- Dependent features get specs they need before starting S2
- Incremental validation at each round
- Test plan evolves with each round
- No wasted effort on paused/blocked features

**If ALL features are independent:**
```markdown
## Feature Dependency Groups

**All features are independent - Single group (parallel execution)**
```
```

**Proposed Change (AFTER - S3 guide clarification):**
```markdown
**FOR DEPENDENCY GROUP EPICS:**

S3 runs ONCE PER ROUND (not just once at end):

- **Round 1 S3:** Validate Group 1 features against each other
- **Round 2 S3:** Validate Group 2 features against ALL Group 1 features
- **Round 3 S3:** Validate Group 3 features against ALL Groups 1-2 features

**Scope expands per round** - Each round validates new features against ALL prior features.
```

**Proposed Change (AFTER - S4 guide clarification):**
```markdown
**FOR DEPENDENCY GROUP EPICS:**

S4 runs ONCE PER ROUND (not just once at end):

- **Round 1 S4:** Update test plan with Group 1 features (+ validation loop)
- **Round 2 S4:** Update test plan with Group 2 features (+ validation loop)
- **Round 3 S4:** Update test plan with Group 3 features (+ validation loop)

**Test plan evolves incrementally** - Each round adds new features and validates complete plan.
```

**Rationale:**
Provides explicit workflow for dependency groups. Prevents batching all S2 then all S3 then all S4. Establishes per-round validation principle (incremental quality gates).

**Impact Assessment:**
- **Who benefits:** Epics with feature dependencies (common pattern)
- **When it helps:** Planning phase (S1-S4) for multi-group epics
- **Severity if unfixed:** HIGH - Without dependency group workflow:
  - Dependent features start S2 prematurely (missing dependencies)
  - Agents waste time then get paused
  - Batched S3/S4 misses incremental validation opportunities
  - Test plan updated once instead of evolving incrementally

**User Decision:** [ ] Approve  [ ] Modify  [ ] Reject  [ ] Discuss

**User Feedback/Modifications:**
```

```

---

### Proposal P1-4: Add Cross-Feature Alignment with Agent Messaging to S2.P3 Guide

**Lesson Learned:**
> "**Mechanism 1: Agent Messaging During S2.P3 Phase 5** - When Agent B finds issue in Feature A during cross-feature alignment: Agent B documents issue, sends message to Agent A via agent_comms, Agent A reviews during coordination heartbeat, evaluates suggestion, updates spec if agreed. **Benefits:** Issues fixed immediately instead of deferred to S3, distributed validation (multiple agents reviewing each feature), agents maintain ownership, reduces Primary's S3 workload."

**Source File:** `epic_lessons_learned.md` - Process Improvement: Enhanced Cross-Feature Alignment (Lines 864-1135)

**Root Cause:**
Current S2.P3 Phase 5 (cross-feature alignment) is one-directional: agents can only update their own feature's spec. If Agent B finds issue in Feature A's spec, no mechanism to notify Agent A. Issues deferred to S3 instead of being fixed immediately.

**Affected Guide(s):**
- `stages/s2/s2_p3_refinement.md` - Phase 5: Cross-Feature Alignment
- `parallel_work/communication_protocol.md` - Add message type

**Current State (BEFORE - from S2.P3 guide):**
```markdown
(Current Phase 5 has agents compare to other features but only update their own spec)
```

**Proposed Change (AFTER - Add to S2.P3 Phase 5):**
```markdown
### Step 5.2.5: Send Messages for Issues in Other Features (NEW)

If you find issues in another feature's spec during comparison:

**DO NOT update other feature's files directly**

Instead, send message via agent_comms:

**File:** `agent_comms/{your_id}_to_{owner_id}.md`

**Template:**
```markdown
## Message: Cross-Feature Alignment Issue
**From:** {your_id} (Feature {N})
**To:** {owner_id} (Feature {M})
**Subject:** {Brief description}
**Status:** ⏳ UNREAD

**Issue:** {Detailed description with line numbers from Feature M spec}

**Suggested Action:** {What owner should do to resolve}

**Urgency:** {LOW/MEDIUM/HIGH}

**Context:** Found during S2.P3 Phase 5 (Cross-Feature Alignment) for Feature {N}
```

**The other agent will:**
- Review during next coordination heartbeat (15 min)
- Evaluate suggestion
- Update their spec if agreed OR send counter-proposal
- Send acknowledgment message
- Mark your message as ✅ READ

**Primary agent monitors:**
- All agent-to-agent messages during coordination
- Resolves disputes if agents can't align
- Escalates to user if necessary

**Benefits:**
- Issues fixed immediately (not deferred to S3)
- Distributed validation (multiple agents review each feature)
- Agents maintain ownership of their features
- Reduces Primary's S3 workload
```

**Proposed Change (AFTER - Add to communication_protocol.md):**
```markdown
### Message Type 4: Cross-Feature Alignment Issue

**When to use:** During S2.P3 Phase 5, when you find issue in another feature

**Template:** (same as above)

**Response SLA:**
- LOW urgency: 1 hour
- MEDIUM urgency: 30 minutes
- HIGH urgency: 15 minutes (coordination heartbeat)

**Escalation:**
- If no response within SLA: Send reminder
- If disagreement: Escalate to Primary agent
- If blocking: Escalate to Primary immediately
```

**Rationale:**
Enables distributed validation during S2.P3. Issues fixed by feature owners immediately instead of Primary fixing everything in S3. Scales better for large epics.

**Impact Assessment:**
- **Who benefits:** Parallel work epics (multiple agents), Primary agent workload reduction
- **When it helps:** S2.P3 Phase 5 cross-feature alignment, reduces S3 issues
- **Severity if unfixed:** HIGH - Without agent messaging:
  - Issues deferred to S3 (delayed resolution)
  - Primary agent must find and fix all cross-feature issues alone
  - Doesn't scale to large epics (Primary becomes bottleneck)
  - Lost opportunity for distributed validation

**User Decision:** [ ] Approve  [ ] Modify  [ ] Reject  [ ] Discuss

**User Feedback/Modifications:**
```

```

---

## P2: Medium Priority (Consider)

### Proposal P2-1: Add Pre-Made Handoff Packages to S1 Guide (Feature Folders)

**Lesson Learned:**
> "**New Handoff Process:** Primary agent generates handoff packages DIRECTLY to feature folders: feature_02_{name}/HANDOFF_PACKAGE.md, feature_03_{name}/HANDOFF_PACKAGE.md. User spawns new agent with simple command: 'You are a secondary agent for Feature 02'. Secondary agent detects instruction, reads feature_02_{name}/HANDOFF_PACKAGE.md, extracts assignment and begins work. **Benefits:** Simpler user experience (one-line instruction), no copy/paste errors, scalable (2 or 20 features), consistent startup pattern."

**Source File:** `epic_lessons_learned.md` - Process Improvement: Pre-Made Handoff Packages (Lines 750-863)

**Root Cause:**
Current approach has Primary generate handoffs to `handoffs/secondary_{id}_handoff.md`, requiring user to copy/paste 500-800 lines of text per agent. Clunky for user, error-prone, doesn't scale to large epics.

**Affected Guide(s):**
- `stages/s1/s1_epic_planning.md` - Step 5.8-5.9 (handoff generation)
- `parallel_work/s2_secondary_agent_guide.md` - Startup protocol
- `templates/handoff_package_template.md` - File location

**Current State (BEFORE):**
```markdown
Generate handoff packages in handoffs/ folder:
- handoffs/secondary_a_handoff.md
- handoffs/secondary_b_handoff.md
```

**Proposed Change (AFTER):**
```markdown
Generate handoff packages DIRECTLY in feature folders:
- feature_02_{name}/HANDOFF_PACKAGE.md
- feature_03_{name}/HANDOFF_PACKAGE.md
- (one per secondary agent feature)

**User startup command:**
"You are a secondary agent for Feature 02 (schedule_fetcher)"

**Secondary agent will:**
- Detect "secondary agent for Feature 02" instruction
- Read feature_02_{name}/HANDOFF_PACKAGE.md automatically
- Extract assignment and begin S2.P1

**Benefits:**
- No copy/paste needed (one-line instruction per agent)
- No copy/paste errors (agent reads file directly)
- Scalable (works identically for 2 or 20 features)
- Consistent startup pattern for all secondary agents
```

**Rationale:**
Simplifies user experience significantly. User spawns 8 agents with 8 one-line commands instead of copy/pasting 8 large text blocks. Reduces friction for parallel work.

**Impact Assessment:**
- **Who benefits:** Users spawning parallel agents, secondary agents (simpler startup)
- **When it helps:** S1 handoff generation, secondary agent startup
- **Severity if unfixed:** MEDIUM - Current approach works but is clunky:
  - User must copy/paste 500-800 lines per agent
  - Error-prone (easy to miss content during copy)
  - Not scalable (8 agents = 8 copy/paste operations)
  - Manual overhead instead of simple commands

**User Decision:** [ ] Approve  [ ] Modify  [ ] Reject  [ ] Discuss

**User Feedback/Modifications:**
```

```

---

### Proposal P2-2: Add S2.P2 Prior Group Review to Checklist Creation

**Lesson Learned:**
> "During Feature 08 S2.P2 checklist creation, agent created Q3: 'Should --debug or --log-level take precedence?' User selected Option B. During S2.P3 Phase 5 alignment, discovered Features 01-07 ALL specify Option A. **Resolution:** Override User Answer Q3 to align with Features 01-07. **Root Cause:** Checklist created WITHOUT prior group review. Q3 was ALREADY answered in Features 01-07 specs (implicitly through argparse). Question should have been confirmation, not open question. **What SHOULD have happened:** Review Features 01-07 specs before creating checklist, cross-reference each question, delete Q3 and document 'Precedence: --debug forces DEBUG (aligned with Features 01-07)'."

**Source File:** `epic_lessons_learned.md` - Process Improvement: S2.P2 Checklist Validation (Lines 2023-2161)

**Root Cause:**
S2.P2 guide doesn't mention reviewing prior dependency group features before creating checklist. Agents create questions based solely on current feature scope, re-asking questions already answered by prior features.

**Affected Guide(s):**
- `stages/s2/s2_p2_specification.md` - Phase 2 (checklist creation)
- `stages/s2/s2_p2_5_spec_to_epic_alignment.md` - Add check

**Current State (BEFORE - from S2.P2 guide):**
```markdown
(Current Phase 2 creates checklist without prior group review step)
```

**Proposed Change (AFTER - Add to S2.P2 Phase 2):**
```markdown
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
```

**Rationale:**
Prevents redundant questions for dependency group features. Cross-references prior group decisions before asking user. Reduces user question count and prevents alignment conflicts.

**Impact Assessment:**
- **Who benefits:** Dependency group features (Group 2+), user (fewer questions)
- **When it helps:** S2.P2 checklist creation for dependent features
- **Severity if unfixed:** MEDIUM - Without prior group review:
  - Redundant questions (user answers same thing twice)
  - Alignment conflicts in S2.P3 Phase 5 (require overrides)
  - Wasted user time answering already-decided questions
  - Potential contradictions between user answers and prior features

**User Decision:** [ ] Approve  [ ] Modify  [ ] Reject  [ ] Discuss

**User Feedback/Modifications:**
```

```

---

## P3: Low Priority (Nice-to-Have)

*No P3 proposals - All lessons identified were significant enough to be P0-P2.*

---

## User Approval Summary

**Instructions:**
1. Review each proposal individually (start with P0, then P1, P2, P3)
2. Mark your decision in "User Decision" checkbox: Approve / Modify / Reject / Discuss
3. For "Modify", provide alternative text in "User Feedback/Modifications" section
4. For "Discuss", ask questions or request clarification in "User Feedback/Modifications" section
5. Agent will apply only approved changes (or your modifications)

**Guidelines:**
- **P0 (Critical):** Strongly recommended - prevents major bugs or workflow violations
- **P1 (High):** Recommended - significantly improves quality or reduces rework
- **P2 (Medium):** Consider - moderate improvements, clarifies ambiguity
- **P3 (Low):** Optional - minor improvements, cosmetic fixes

**Approval Statistics:**
- Total proposals: 11
- P0 proposals: 5 (critical - prevent workflow violations and catastrophic bugs)
- P1 proposals: 4 (high - significantly improve quality and process)
- P2 proposals: 2 (medium - improve efficiency and user experience)
- P3 proposals: 0 (low - no cosmetic-only changes)

**Priority Recommendations:**
1. **IMMEDIATE:** Review and approve P0-1 through P0-5 (blocking checkpoint format, S1.P3 visibility, checkpoint definition, Agent Status requirements, zero-tolerance standard)
2. **HIGH:** Review and approve P1-1 through P1-4 (S4/S8 validation loops, dependency groups, agent messaging)
3. **CONSIDER:** Review P2-1 and P2-2 (handoff packages, checklist validation)

**After User Review:**
- Approved: {User fills}
- Modified: {User fills}
- Rejected: {User fills}
- Pending discussion: {User fills}

**Next Steps:**
- [ ] Agent applies approved changes to guides
- [ ] Agent applies user modifications to guides
- [ ] Agent creates separate commit for guide updates
- [ ] Agent updates `reference/guide_update_tracking.md` with applied changes
- [ ] Agent proceeds with epic completion (S10)

---

## Analysis Summary

**Key Patterns Identified:**

1. **Guide Abandonment (Root Cause of Both Critical Failures):**
   - Agents read guides once, work from memory
   - Current checkpoints insufficient (advisory, not blocking)
   - Agent Status updates mentioned but not enforced
   - Solution: Blocking checkpoints (P0-1), checkpoint definition (P0-3), mandatory Agent Status steps (P0-4)

2. **Phase Visibility Issues:**
   - S1.P3 Discovery Phase not prominent enough
   - Agents skip between "Step 2 → Step 3" without realizing Discovery exists
   - Solution: S1 phase structure warning (P0-2)

3. **Consistency Standards:**
   - "Clean loop" definition ambiguous (allowed LOW severity deferrals)
   - Need explicit zero-tolerance standard
   - Solution: S3 zero-tolerance requirement (P0-5)

4. **Validation Gaps:**
   - S3 has consistency loop but S4/S8 don't
   - One-pass updates miss issues
   - Solution: S4 validation loop (P1-1), S8.P1 consistency loop (P1-2)

5. **Dependency Management:**
   - No workflow for feature dependency groups
   - Agents batch stages instead of completing per round
   - Solution: Dependency group workflow (P1-3)

6. **Parallel Work Improvements:**
   - Agent messaging would reduce S3 workload
   - Handoff packages could be simpler
   - Prior group review prevents redundant questions
   - Solution: Agent messaging (P1-4), handoff packages (P2-1), checklist validation (P2-2)

**Historical Context:**
- KAI-7 had TWO critical failures in S1 (both guide abandonment)
- 8 secondary agents blocked for 4 hours due to S1.P3 skip
- 3 mandatory checkpoints skipped in S1.P3 execution
- 7 LOW severity issues nearly deferred in S3 (user rejected)
- All issues traced to insufficient enforcement mechanisms

**Impact if Unfixed:**
- P0 proposals unfixed: CRITICAL - Future epics will have same S1 failures, checkpoint violations, consistency gaps
- P1 proposals unfixed: HIGH - Missed validation opportunities, test plan gaps, scaling issues
- P2 proposals unfixed: MEDIUM - User experience friction, redundant work

---

**Last Updated:** 2026-02-01 16:30
