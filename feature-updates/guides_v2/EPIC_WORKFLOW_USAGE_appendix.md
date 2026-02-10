# Epic-Driven Development Workflow - Usage Guide Appendix

**Version:** 2.0
**Last Updated:** 2025-12-31
**Purpose:** Detailed examples, FAQs, and stage-by-stage workflows extracted from main usage guide

**Main Guide:** `EPIC_WORKFLOW_USAGE.md`

---

## Table of Contents

1. [Common Patterns](#common-patterns)
2. [Frequently Asked Questions](#frequently-asked-questions)
3. [Stage-by-Stage Detailed Workflows](#stage-by-stage-detailed-workflows)

---

## Common Patterns

### Pattern 1: Starting from User Request

**User says:** "Help me develop {feature_name}"

**Your response:**
```text
I'll help you develop {feature_name} using the Epic-Driven Development Workflow.

First, I need to check if there are any in-progress epics...
[Check feature-updates/ folder]

No in-progress epics found. Let me verify you have a request file...

I see you have feature-updates/{epic_name}.txt. Let me start S1.

[Use "Starting S1" prompt from prompts_reference_v2.md]
[Read stages/s1/s1_epic_planning.md]

I'm reading stages/s1/s1_epic_planning.md to ensure I follow the complete epic planning process...

The guide requires:
- Analyze epic request and perform codebase reconnaissance
- Propose feature breakdown (get user approval)
- Create epic folder structure with all required files
- Create feature folders with initial documentation
- Generate initial epic_smoke_test_plan.md

Prerequisites I'm verifying:
✅ User created feature-updates/{epic_name}.txt with initial notes
✅ feature-updates/guides_v2/ folder exists
✅ No conflicting in-progress epics

I'll now proceed with S1...

[Begin S1 workflow]
```

### Pattern 2: Resuming In-Progress Epic

**You notice epic folder exists in feature-updates/**

**Your response:**
```text
I notice there's an in-progress epic: {epic_name}

Let me check its current status...

[Read feature-updates/KAI-{N}-{epic_name}/EPIC_README.md Agent Status section]

I see the epic is currently at:
- Current Stage: S6 - Implementation Execution
- Current Step: Implementing Feature 2, component 3 of 5
- Next Action: Complete PlayerManager.calculate_score() method

[Use "Resuming In-Progress Epic" prompt from prompts_reference_v2.md]

I'm resuming the in-progress epic {epic_name}. Let me read the current guide to restore context...

[Read stages/s6/s6_execution.md]

The guide requires:
- Keep spec.md VISIBLE at all times
- Run unit tests after EVERY component (100% pass required)
- Continuous spec verification via implementation_checklist.md

Current status:
- Feature: feature_02_{name}
- Component: 3 of 5 complete
- Next: Complete PlayerManager.calculate_score() method

I'll now continue with the implementation...

[Continue from next action listed in Agent Status]
```

### Pattern 3: Transitioning Between Stages

**Completing S2, moving to S3**

**Your response:**
```text
I've completed S2 (Feature Deep Dives) for all features.

Let me verify completion criteria before moving to S3...

S2 Completion Criteria:
✅ All features have complete spec.md files
✅ All checklist.md items resolved
✅ Feature README.md files updated
✅ User questions answered

All criteria met. Ready to proceed to S3.

[Update EPIC_README.md Agent Status to show S2 complete]

[Use "Starting S3" prompt from prompts_reference_v2.md]

I'm reading stages/s3/s3_cross_feature_sanity_check.md to ensure I perform thorough cross-feature validation...

The guide requires:
- Systematic pairwise comparison of all feature specs
- Identify conflicts, overlaps, and gaps
- Resolve all inconsistencies
- Get explicit user sign-off on complete plan

Prerequisites I'm verifying:
✅ ALL features have complete specs (S2 done)
✅ All checklist.md items resolved
✅ Feature dependencies identified

I'll now proceed with S3...

[Begin S3 workflow]
```

### Pattern 4: Handling QC Validation Loop Issues

**Validation loop finds issues**

**Your response:**
```text
Validation Loop Round 3 found the following issues:

CRITICAL:
1. PlayerManager.calculate_score() returns incorrect value for edge case (injured player with bye week)

MINOR:
2. Missing type hint on helper function _normalize_score()

These issues require fixes before proceeding.

Following Validation Loop Protocol from stages/s7/s7_p2_qc_rounds.md:
- Fix ALL issues immediately (no deferrals)
- Reset clean counter to 0
- Continue validation (no restart needed)

Fixing issues now...

[Fix issue 1 - calculate_score() edge case]
[Fix issue 2 - add type hint]
[Run unit tests - verify 100% pass]

All issues fixed. Clean counter reset to 0. Continuing validation...

[Execute Validation Round 4 - check all 11 dimensions]
[Execute Validation Round 5 - check all 11 dimensions]
[Execute Validation Round 6 - check all 11 dimensions]

3 consecutive clean rounds achieved. Proceeding to Final Review...
```

### Pattern 5: User Testing Finds Bugs (S10)

**User reports bugs during mandatory testing**

**Your response:**
```text
You reported the following bugs during testing:

1. Draft recommendations show incorrect player rankings
2. Export file has wrong column headers

Following S10 bug fix protocol from stages/s10/s10_epic_cleanup.md:

Step 1: Document Bugs

Creating bug fix folders:
- bugfix_high_incorrect_rankings/
- bugfix_low_wrong_headers/

[Create notes.txt for each bug]

Please verify these notes.txt files accurately describe the bugs...

[Wait for user verification]

Step 2: Fix ALL Bugs

[For each bug fix, follow stages/s5/s5_bugfix_workflow.md]
[S2: Create spec.md]
[S5: Create implementation_plan.md, get user approval]
[S6: Implement fix]
[S7: Smoke testing + QC rounds]

Both bug fixes complete.

Step 3: RESTART S9 (Epic Final QC)

Following guide requirement: After bug fixes, must restart ENTIRE S9.

[Read stages/s9/s9_p1_epic_smoke_testing.md]
[Execute epic smoke testing - 4 parts]
[Read stages/s9/s9_p2_epic_qc_rounds.md]
[Execute epic QC rounds - 3 rounds]
[Read stages/s9/s9_p4_epic_final_review.md]
[Execute epic PR review and final verification]

S9 complete with zero issues.

Step 4: Return to User Testing

I've fixed both bugs and re-validated the epic (S9 passed).

Bugs fixed:
- Bug 1: Draft recommendations now show correct rankings (sorted by score DESC)
- Bug 2: Export headers now match expected format (Name, Position, Team, Score)

Please test the system again to verify the bugs are fixed and no new issues introduced.

[Wait for user testing results]
```

### Pattern 6: Session Compaction Mid-Epic

**You start conversation and notice in-progress epic but no context**

**Your response:**
```text
I notice there's an in-progress epic but I don't have the conversation history.

Let me check the epic status to understand where we are...

[Read feature-updates/KAI-{N}-{epic_name}/EPIC_README.md Agent Status]

The epic is currently at:
- Stage: S5 - Implementation Planning
- Round: Round 2
- Iteration: 11 of 16
- Guide: stages/s5/s5_p2_planning_round2.md
- Next Action: Complete Algorithm Traceability Matrix (iteration 11)

Session compaction occurred. Following resumption protocol...

[Use "Resuming After Session Compaction" prompt from prompts_reference_v2.md]

I'm resuming work on {epic_name} after session compaction. Let me restore context...

[Read stages/s5/s5_p2_planning_round2.md]
[Read feature spec.md]
[Read current implementation_plan.md]

Context restored. Current task: Iteration 11 (Algorithm Traceability Matrix)

The guide requires:
- Re-verify algorithm traceability from iteration 4
- Check for any new algorithms discovered during iterations 8-10
- Update traceability matrix if needed

I'll now continue with iteration 11...

[Resume work from iteration 11]
```


### Pattern 7: S2 Parallel Work (3+ Features)

**Scenario:** Epic has 3+ features, Primary offers parallel work to user

**Overview:**
When an epic has 3 or more features, S2 (Feature Deep Dives) can be parallelized with multiple agents working simultaneously. This reduces S2 time by 40-60% (e.g., 3-feature epic saves ~4 hours).

**Key Roles:**
- **Primary Agent**: Coordinator + Feature 01 owner (85% feature work, 15% coordination)
- **Secondary Agents**: Feature owners (90% feature work, 10% coordination)

---

#### Phase 1: Offering Parallel Work (Primary, during S1)

**At S1 Step 5.8 (Analyze Features for Parallelization):**

```text
I've created {N} features for this epic.

Let me analyze if parallel work would be beneficial...

Feature count: {N} features
Expected S2 time (sequential): {N × 2.5} hours = {total} hours
Expected S2 time (parallel): ~3 hours with {N} agents
Time savings: ~{savings} hours (40-60% reduction)

Decision: {N} >= 3, parallel work recommended.

[Continue to S1 Step 5.9]
```

**At S1 Step 5.9 (Offer Parallel Work to User):**

```markdown
I can offer parallel work for S2 (Feature Deep Dives):

**Parallel Mode:**
- Multiple agents work on S2 simultaneously
- Each agent owns one feature completely
- I coordinate and own Feature 01
- Time: ~3 hours total (vs {sequential_time} hours sequential)
- Complexity: Requires spawning additional agents

**Sequential Mode:**
- I complete all features one by one
- Simpler coordination (just me)
- Time: ~{sequential_time} hours
- Standard workflow

**Recommendation:** Parallel mode saves ~{savings} hours for {N} features.

Would you like to:
1. ✅ Enable parallel work for S2 (I'll provide setup instructions)
2. ❌ Continue sequential (I'll do all features one by one)
3. ❓ Discuss parallelization approach
```

**If user chooses Option 1 (Enable parallel):**

```text
Great! I'll coordinate parallel S2 work.

After completing S1, I'll:
1. Generate handoff packages for secondary agents
2. Provide spawn commands for you to create secondary agents
3. Begin S2.P1 for Feature 01 while secondaries work on their features
4. Coordinate via checkpoints and message files

You'll need to spawn {N-1} secondary agents (I'll provide exact commands).

Continuing with S1...

[Complete S1 as normal]
```

---

#### Phase 2: Generating Handoff Packages (Primary, after S1)

**After S1 completes, Primary generates handoff packages and awaits secondary agent spawn.**

This reduced section focuses on the workflow without showing all the detailed coordination mechanics (those are in the dedicated guides).

---

#### Phase 3: Coordination During S2 (Primary)

**Primary performs coordination heartbeat every 15 minutes:**
- Update own checkpoint
- Check secondary inboxes for messages/escalations
- Process any escalations (answer questions, clarify specs)
- Verify no stale agents (checkpoint age < 30 min warning, < 60 min failure)
- Update EPIC_README.md with progress
- Continue Feature 01 work

**Coordination overhead:** <10% of time (15 min coordination per hour)

---

#### Phase 4: Secondary Agent Workflow

**Secondary receives handoff from user, executes startup:**
1. Parse handoff configuration
2. Create communication and coordination files
3. Send startup confirmation to Primary
4. Begin S2.P1 for assigned feature

**During S2 work:**
- Execute S2.P1, S2.P2, S2.P3 for assigned feature
- Coordinate every 15 minutes (update checkpoint, check inbox, update STATUS)
- Escalate blockers to Primary within 15 minutes
- Focus 90% on feature work, 10% on coordination

**After completing S2.P3:**
- Send completion message to Primary
- Update STATUS: READY_FOR_SYNC
- Update checkpoint: WAITING_FOR_SYNC
- WAIT for Primary to run S3

---

#### Phase 5: Sync Point - Transition to S3

**Primary verifies all agents completed S2:**
1. Check all completion messages received
2. Verify all STATUS files: READY_FOR_SYNC = true
3. Verify all checkpoints fresh and WAITING_FOR_SYNC
4. Create sync verification document
5. Notify secondaries that S3 is starting
6. Run S3 solo (secondaries wait)
7. After S3+S4 complete, notify secondaries to proceed

**S3 and S4 run sequentially by Primary only** (requires epic-level view)

---

#### Phase 6: Common Issues

**Stale Agent (checkpoint > 60 minutes old):**
- Primary detects during coordination heartbeat
- Sends status check message (wait 15 min)
- If no response, escalates to user
- Recovery: Same agent resumes, new agent takes over, or Primary absorbs feature
- See: `parallel_work/stale_agent_protocol.md`

**Sync Timeout (S2 not all complete within expected time):**
- Soft timeout: 4 hours (send reminder, request ETA)
- Hard timeout: 6 hours (escalate to user)
- Recovery: Wait with ETA, investigate blocker, abort parallel for late feature
- See: `parallel_work/sync_timeout_protocol.md`

**Escalation Handling:**
- Secondary escalates blocker to Primary
- Primary attempts to resolve (answer question, clarify spec)
- If requires user input, Primary escalates to user
- SLA: 15-minute response time
- See: `parallel_work/communication_protocol.md`

---

#### Summary: Benefits and Requirements

**Benefits:**
- 40-60% time reduction for S2 phase
- Scales with feature count (3 features = 4 hours vs 7.5 hours)
- Each agent focuses deeply on one feature
- Maintains quality through individual feature ownership

**Requirements:**
- User must spawn secondary agents (Primary provides commands)
- All agents coordinate via files (checkpoints, messages, STATUS)
- Primary dedicates 15% time to coordination
- Checkpoint updates every 15 minutes (enables recovery)

**When to Use:**
- 3+ features: Recommended (good time savings)
- 2 features: Optional (modest savings, user decides)
- 1 feature: Not applicable (no parallelization possible)

**See Complete Guides:**
- `parallel_work/s2_parallel_protocol.md` - Master protocol overview
- `parallel_work/s2_primary_agent_guide.md` - Primary agent complete workflow
- `parallel_work/s2_secondary_agent_guide.md` - Secondary agent complete workflow
- `parallel_work/stale_agent_protocol.md` - Stale agent detection and recovery
- `parallel_work/sync_timeout_protocol.md` - Sync point timeout handling
- `parallel_work/communication_protocol.md` - Message formats and channels
- `parallel_work/checkpoint_protocol.md` - Checkpoint structure and updates
- `parallel_work/lock_file_protocol.md` - File locking for shared resources

---

---

## Frequently Asked Questions

### Q: Can I skip stages for small changes?

**A:** No. The workflow is designed for consistency and quality. However:
- Very small bug fixes can use the Bug Fix Workflow (skips some stages)
- Each stage has clear purpose - skipping leads to issues
- Historical data: 80% of "small changes" that skip stages require rework

### Q: What if spec.md is wrong after implementation?

**A:** Update it. Document why.
- S8.P1 specifically addresses this (Cross-Feature Spec Alignment)
- Implementation reveals reality that planning couldn't predict
- Update spec.md to reflect actual implementation
- Document reason for change in spec.md

### Q: How long does a typical epic take?

**A:** Depends on complexity:
- Small epic (2 features): 1-2 days
- Medium epic (3-5 features): 3-5 days
- Large epic (6+ features): 1-2 weeks

**Time breakdown:**
- Stages 1-4 (Planning): 20% of time
- S5 (Implementation): 60% of time
- Stages 6-7 (Validation/Cleanup): 20% of time

### Q: What if user wants changes during implementation?

**A:** Update the spec, restart affected stages:
1. Pause current work
2. Update spec.md with new requirements
3. Determine impact (which stages affected)
4. Restart from earliest affected stage
5. Example: New requirement in S6 → Return to S5

### Q: Can multiple agents work on one epic?

**A:** Yes, but coordinate carefully:
- Each agent should work on different feature (S5)
- Stages 1-4 and 6-7 should be single agent
- Use Agent Status to avoid conflicts
- Epic README tracks all feature progress

### Q: What if tests are failing from unrelated changes?

**A:** Fix them.
- S10 requires 100% test pass rate
- It's acceptable to fix pre-existing failures
- Document in epic_lessons_learned.md
- Goal: Clean test suite for everyone

### Q: How do I handle dependencies between features?

**A:** Plan them in S1, implement in order:
- S1: Identify dependencies
- S4: Plan integration testing
- S5: Implement features sequentially (dependency first)
- S9: Validate integration

### Q: What if S9 finds major architectural issues?

**A:** Create bug fixes, potentially refactor:
1. Document issues as high-priority bug fixes
2. Determine if architectural change needed
3. If major refactor: May need new epic
4. If fixable: Create bug fixes, restart S9
5. No shortcuts - quality is non-negotiable

### Q: How does the guide improvement workflow work?

**A:** Every epic includes mandatory guide updates (S10.P1):

**When:** After S10 user testing passes, before final commit

**What gets updated:**
- All files in `feature-updates/guides_v2/` (16 guides + supporting files)
- `CLAUDE.md` (root project instructions)
- Any files that support future agents

**Process:**
1. **Analyze lessons learned:** Agent reads ALL `lessons_learned.md` files (epic + features)
2. **Identify guide gaps:** For each lesson, determine which guide(s) could have prevented the issue
3. **Create proposals:** Agent creates `GUIDE_UPDATE_PROPOSAL.md` with prioritized improvements:
   - **P0 (Critical):** Prevents catastrophic bugs, mandatory gate gaps
   - **P1 (High):** Significantly improves quality, reduces major rework
   - **P2 (Medium):** Moderate improvements, clarifies ambiguity
   - **P3 (Low):** Minor improvements, cosmetic fixes
4. **User approval:** Agent presents EACH proposal individually with before/after comparison
5. **User decides:** For each proposal: Approve / Modify / Reject / Discuss
6. **Apply changes:** Agent applies ONLY approved changes (or user modifications)
7. **Separate commit:** Guide updates committed separately from epic code

**Why mandatory:**
- Continuous guide improvement based on real implementation experience
- Future agents benefit from lessons learned in this epic
- Systematic feedback loop: implementation → lessons → guide updates
- User has full control over guide evolution

**Time estimate:** 20-45 minutes per epic (depending on lessons count)

**See:** `stages/s10/s10_p1_guide_update_workflow.md` for complete workflow

---

## Stage-by-Stage Detailed Workflows

**Purpose:** Complete workflow details for all 10 stages (extracted from CLAUDE.md for reference)

**When to use:** When you need detailed phase/iteration structure for a specific stage beyond the quick reference in CLAUDE.md

---

### S1: Epic Planning (Detailed)

**Trigger:** "Help me develop {epic-name}"
**First Action:** Use "Starting S1" prompt from `prompts_reference_v2.md`
**Guide:** `stages/s1/s1_epic_planning.md`

⚠️ **CRITICAL: S1 HAS 6 PHASES (NOT 5 STEPS)**

**S1 Phase Structure:**
- **S1.P1:** Initial Setup (Steps 1.0-1.4)
  - Assign KAI number
  - Create git branch
  - Create epic folder structure

- **S1.P2:** Epic Analysis (Step 2)
  - Analyze epic request
  - Identify scope and constraints

- **S1.P3: DISCOVERY PHASE (Step 3)** ← MANDATORY, CANNOT SKIP
  - Guide: `stages/s1/s1_p3_discovery_phase.md`
  - Output: DISCOVERY.md (epic-level source of truth)
  - Time-Box: SMALL 1-2hrs, MEDIUM 2-3hrs, LARGE 3-4hrs
  - Feature folders NOT created until Discovery approved
  - Iterative research and Q&A loop until 3 consecutive iterations with no new questions
  - Re-read code/requirements with fresh perspective each iteration
  - **Historical failure:** KAI-7 agent skipped S1.P3 entirely, blocked 8 secondary agents for 4 hours

- **S1.P4:** Feature Breakdown Proposal (Step 4)
  - Propose feature breakdown
  - Get user approval

- **S1.P5:** Epic Structure Creation (Step 5)
  - Create feature folders
  - Create initial documentation

- **S1.P6:** Transition to S2 (Step 6)
  - Verify structure complete
  - Prepare for S2

**You CANNOT skip S1.P3 Discovery Phase:**
- Must create DISCOVERY.md before feature breakdown
- Must get user approval before creating feature folders
- Feature specs will reference DISCOVERY.md findings
- S2.P1 Phase 0 requires DISCOVERY.md to exist

**Next:** S2

---

### S2: Feature Planning (Detailed)

**First Action:** Use "Starting S2" prompt from `prompts_reference_v2.md`
**Guide:** `stages/s2/s2_feature_deep_dive.md` (router to phases)
**Duration:** 2.25-4 hours per feature (3 iterations)

**Phases:**

**S2.P1: Spec Creation and Refinement** (3 iterations)
- **S2.P1.I1: Feature-Level Discovery** (60-90 min)
  - Embeds Gate 1 (Research Completeness Audit)
  - Research and document feature requirements
  - Create initial spec.md

- **S2.P1.I2: Checklist Resolution** (45-90 min)
  - 9-step protocol for resolving questions
  - User answers questions (agents CANNOT mark [x] autonomously)
  - Update spec.md with answers

- **S2.P1.I3: Refinement & Alignment** (30-60 min)
  - Embeds Gate 2 (Spec-to-Epic Alignment)
  - Includes Gate 3 (User Checklist Approval)
  - Refine spec based on alignment check
  - Get user approval on checklist

**S2.P2: Cross-Feature Alignment** (20-60 min)
- Primary agent only
- Pairwise comparison of feature specs
- Alignment validation

**Key Outputs:**
- spec.md (requirements specification - user-approved)
- checklist.md (QUESTIONS ONLY - user answers ALL before S5.P1)
- RESEARCH_NOTES.md (REQUIRED)

**Validation Loops:**
- S2.P1.I1 (embeds Gate 1)
- S2.P1.I3 (embeds Gate 2)
- S2.P2 (alignment validation)

**Gates:**
- Gate 1: Research Completeness Audit (S2.P1.I1)
- Gate 2: Spec-to-Epic Alignment (S2.P1.I3)
- Gate 3: User Checklist Approval (S2.P1.I3 - explicit user approval)

**Next:** S3 (after ALL features in all groups complete S2)

---

### S3: Epic-Level Documentation, Testing Plans, and Approval (Detailed)

**First Action:** Use "Starting S3" prompt from `prompts_reference_v2.md`
**Guide:** `stages/s3/s3_epic_planning_approval.md`
**Duration:** 75-105 minutes total

**Phases:**

**S3.P1: Epic Testing Strategy Development** (45-60 min)
- Epic-level integration tests
- Cross-feature test scenarios
- Define epic success criteria

**S3.P2: Epic Documentation Refinement** (20-30 min)
- Review epic-level documentation
- Ensure consistency across features
- Update EPIC_README.md

**S3.P3: Epic Plan Approval** (10-15 min)
- Gate 4.5 with 3-tier rejection handling
- User reviews complete epic plan
- User approves or requests changes

**Key Changes from Old Workflow:**
- Pairwise comparison moved to S2.P2
- Old S4 content moved here

**Validation Loops:**
- S3.P1 (testing strategy validation)
- S3.P2 (documentation validation)

**Gates:**
- Gate 4.5: User approves epic plan (MANDATORY, 3-tier rejection handling)

**Next:** S4 (first feature testing strategy)

---

### S4: Feature Testing Strategy (Detailed)

**First Action:** Use "Starting S4" prompt from `prompts_reference_v2.md`
**Guide:** `stages/s4/s4_feature_testing_strategy.md` (router to 4 iterations)
**Purpose:** Test-driven development - plan tests BEFORE implementation
**Duration:** 45-60 minutes per feature

**Iterations:**

**S4.I1: Test Strategy Development** (15-20 min)
- Unit tests planning
- Integration tests planning
- Edge tests planning
- Goal: >90% coverage

**S4.I2: Edge Case Enumeration** (10-15 min)
- Boundary conditions
- Error paths
- Invalid inputs
- State transitions

**S4.I3: Configuration Change Impact** (10-15 min)
- Config test matrix
- Environment variations
- Parameter combinations

**S4.I4: Validation Loop** (15-20 min)
- Validate test strategy completeness
- 3 consecutive clean rounds required
- Zero deferred issues

**Key Output:**
- test_strategy.md (>90% coverage goal)
- Merged into implementation_plan.md in S5.P1.I1

**Next:** S5 (Implementation Planning)

---

### S5: Implementation Planning (Detailed)

**First Action:** Use "Starting S5 Round 1/2/3" prompt from `prompts_reference_v2.md`
**🚨 CRITICAL:** Execute iterations ONE at a time, IN ORDER (no batching, no skipping)
**Duration:** 22 iterations across 3 rounds
**Key Change:** Testing iterations (old I8-I10) moved to S4, remaining iterations renumbered sequentially

**Round 1: Planning Foundation** (7 iterations)
- **Guide:** `stages/s5/s5_p1_planning_round1.md` (router to I1-I3)

**S5.P1.I1: Requirements Analysis** (I1-I3)
- Guide: `stages/s5/s5_p1_i1_requirements.md`
- Merges test_strategy.md from S4
- I1: Requirements review
- I2: Dependencies analysis
- I3: Interface contracts

**S5.P1.I2: Algorithm Planning** (I4-I6 + Gate 4a)
- Guide: `stages/s5/s5_p1_i2_algorithms.md`
- I4: Algorithm design
- I5: Data structures
- I6: Performance considerations
- Gate 4a: TODO Specification Audit

**S5.P1.I3: Integration Planning** (I7 + Gate 7a)
- Guide: `stages/s5/s5_p1_i3_integration.md`
- I7: Integration points
- Gate 7a: Backward Compatibility Check

**Validation Loop:** Added at end of Round 1 (validates Gates 4a, 7a)

**Round 2: Verification** (6 iterations)
- **Guide:** `stages/s5/s5_p2_planning_round2.md` (router, I8-I13)

**S5.P2.I1: First Verification** (I8-I9, formerly I11-I12)
- I8: Requirements verification
- I9: Design verification

**S5.P2.I2: Reverification** (I10-I13, formerly I13-I16)
- I10: Cross-reference check
- I11: Dependency validation
- I12: Risk assessment
- I13: Resource estimation

**Round 3: Final Preparation** (9 iterations)
- **Guide:** `stages/s5/s5_p3_planning_round3.md` (router, I14-I22)

**S5.P3.I1: Implementation Preparation** (I14-I19, formerly I17-I22)
- Guide: `stages/s5/s5_p3_i1_preparation.md`
- I14: Implementation order
- I15: Error handling strategy
- I16: Logging strategy
- I17: Documentation plan
- I18: Code review checklist
- I19: Rollback plan

**Validation Loop:** Added before Gate 23a (validates complete plan)

**S5.P3.I2: Pre-Implementation Audit** (I20)
- Guide: `stages/s5/s5_p3_i2_gates_part1.md`
- Gate 23a: Pre-Implementation Spec Audit (5 parts)
  - Part 1: Completeness check
  - Part 2: Consistency check
  - Part 3: Feasibility check
  - Part 4: Testability check
  - Part 5: Maintainability check

**S5.P3.I3: Final Gates** (I21-I22)
- Guide: `stages/s5/s5_p3_i3_gates_part2.md`
- I21: Gate 25 (Spec Validation Check)
- I22: Gate 24 (GO/NO-GO Decision based on confidence)

**Key Output:**
- implementation_plan.md (~400 lines) - PRIMARY reference for S6
- Includes merged test strategy from S4
- User-approved via Gate 5

**Gates:**
- Gate 4a: TODO Specification Audit (S5.P1.I2)
- Gate 7a: Backward Compatibility Check (S5.P1.I3)
- Gate 23a: Pre-Implementation Spec Audit (S5.P3.I2)
- Gate 25: Spec Validation Check (S5.P3.I3)
- Gate 24: GO/NO-GO Decision (S5.P3.I3)
- Gate 5: User approves implementation plan (MANDATORY, 3-tier rejection handling)

**Next:** S6 (Implementation Execution)

---

### S6: Implementation Execution (Detailed)

**First Action:** Use "Starting S6" prompt from `prompts_reference_v2.md`
**Guide:** `stages/s6/s6_execution.md`
**Duration:** Varies by feature complexity

**Key Actions:**
- Create implementation_checklist.md from implementation_plan.md
- Implement code following implementation_plan.md (PRIMARY reference)
- Use spec.md to verify WHAT to build (verification only)
- Update implementation_checklist.md as work progresses

**Key Principle:**
- implementation_plan.md = HOW to build (primary guide)
- spec.md = WHAT to build (verification)

**Next:** S7 (Testing & Review)

---

### S7: Implementation Testing & Review (Detailed)

**First Action:** Use "Starting S7.P1 Smoke Testing" prompt from `prompts_reference_v2.md`
**🚨 RESTART PROTOCOL:** If ANY issues found → Restart from S7.P1 (NOT mid-QC)
**Duration:** 3 phases + commit

**Phases:**

**S7.P1: Smoke Testing** (MANDATORY GATE)
- Guide: `stages/s7/s7_p1_smoke_testing.md`
- Run basic functionality tests
- If issues found → Enter debugging protocol → Fix all issues → Restart from S7.P1
- MUST pass before proceeding to QC rounds

**S7.P2: QC Rounds** (3 rounds)
- Guide: `stages/s7/s7_p2_qc_rounds.md`
- Round 1: Functional QC
- Round 2: Integration QC
- Round 3: Edge case QC
- If issues found → Enter debugging protocol → Fix all issues → Restart from S7.P1 (NOT mid-QC)

**S7.P3: Final Review**
- Guide: `stages/s7/s7_p3_final_review.md`
- PR-style review of code
- Create lessons_learned.md
- Document what worked, what didn't

**After S7.P3:**
- COMMIT FEATURE (feature-level commit)
- Use git commit protocol from CLAUDE.md

**Next:** S8 (Post-Feature Alignment)

---

### S8: Post-Feature Alignment (Detailed)

**First Action:** Use "Starting S8.P1" prompt from `prompts_reference_v2.md`
**Duration:** 2 phases

**Phases:**

**S8.P1: Cross-Feature Alignment**
- Guide: `stages/s8/s8_p1_cross_feature_alignment.md`
- Update remaining feature specs based on completed feature
- Identify conflicts or dependencies
- Adjust upcoming features as needed

**S8.P2: Epic Testing Update**
- Guide: `stages/s8/s8_p2_epic_testing_update.md`
- Reassess epic_smoke_test_plan.md
- Update based on completed feature
- Adjust integration test scenarios

**Key Actions:**
- Update remaining feature specs
- Update epic testing plan
- Ensure alignment across all features

**Next:**
- Repeat S5 for next feature
- OR S9 (if all features done)

---

### S9: Epic-Level Final QC (Detailed)

**First Action:** Use "Starting S9" prompt from `prompts_reference_v2.md`
**🚨 RESTART PROTOCOL:** If ANY issues found → Restart from S9.P1 (NOT mid-QC)
**Guide:** `stages/s9/s9_epic_final_qc.md` (router to phases)

**Phases:**

**S9.P1: Epic Smoke Testing**
- Guide: `stages/s9/s9_p1_epic_smoke_testing.md`
- Run epic-level smoke tests
- Test feature integration
- If issues found → Enter debugging protocol → Fix all issues → Restart from S9.P1

**S9.P2: Epic QC Rounds** (3 rounds)
- Guide: `stages/s9/s9_p2_epic_qc_rounds.md`
- Round 1: Epic functionality QC
- Round 2: Epic integration QC
- Round 3: Epic edge case QC
- If issues found → Enter debugging protocol → Fix all issues → Restart from S9.P1

**S9.P3: User Testing**
- Guide: `stages/s9/s9_p3_user_testing.md`
- User runs tests
- User reports bugs OR "no bugs found"
- ZERO bugs required to proceed to S10

**S9.P4: Epic Final Review**
- Guide: `stages/s9/s9_p4_epic_final_review.md`
- Review epic as a whole
- Document epic-level lessons learned
- Prepare for S10

**If Issues Found:**
- Enter debugging protocol
- Fix ALL issues
- Restart from S9.P1 (complete restart, not mid-QC)

**Next:** S10 (only when user reports ZERO bugs in S9.P3)

---

### S10: Epic Cleanup (Detailed)

**First Action:** Use "Starting S10" prompt from `prompts_reference_v2.md`
**Prerequisites:** S9 complete (user testing PASSED with ZERO bugs)
**Guide:** `stages/s10/s10_epic_cleanup.md`

**Key Actions:**

1. **Run Unit Tests** (100% pass required)
   - All tests must pass
   - No test failures allowed
   - Fix any failures before proceeding

2. **S10.P1: Guide Updates** (MANDATORY)
   - Guide: `stages/s10/s10_p1_guide_update_workflow.md`
   - Analyze lessons learned from epic
   - Create GUIDE_UPDATE_PROPOSAL.md
   - User approval required
   - Apply approved guide updates

3. **Commit Epic**
   - Create epic-level commit
   - Follow git commit protocol

4. **Create Pull Request**
   - Create PR for user review
   - User merges when ready

5. **After PR Merged:**
   - Update EPIC_TRACKER.md
   - Move epic to done/
   - Archive working files

**S10.P1 (MANDATORY):**
- Cannot skip guide update workflow
- Must analyze lessons learned
- Must propose guide improvements
- Must get user approval
- Must apply approved updates

**Next:** Epic complete!

---

**For more information:**
- Complete guide index: `README.md`
- Phase transition prompts: `prompts_reference_v2.md`
- File templates: `templates/`
- Detailed workflow spec: `PLAN.md`

**Questions or feedback?** Update `epic_lessons_learned.md` with guide improvement suggestions.

---

**END OF EPIC WORKFLOW USAGE GUIDE APPENDIX**
