# Proposal Consistency Loop - Round 5

**Date:** 2026-02-03
**Reviewing:** PROPOSAL_FIXES_V3.md (Round 4 fix applied)
**Method:** Workflow simulation, dependency validation, integration testing
**Goal:** Verify proposals work together in practice

---

## Round 5 Approach - Different Validation Patterns

**What I've checked in previous rounds:**
- Round 3: Random spot-checks, thematic clustering, quality preservation
- Round 4: Fix verification, cross-fix validation

**What I'm checking in Round 5:**
1. **Workflow Simulation:** Trace through complete workflow (S1 → S10)
2. **Dependency Chain:** Verify proposal dependencies are correct
3. **User Implementability:** Can user actually implement these?
4. **Integration Testing:** Do proposals work together?
5. **Stress Testing:** What breaks under edge cases?

**Assumption:** Proposals might work individually but fail when combined

---

## Test 1: Workflow Simulation (Happy Path)

**Scenario:** Agent starts new epic "Add Player Projections" with 3 features

### S1: Epic Planning

**Proposal 3 (S1.P3 Discovery Phase):**
- Create DISCOVERY.md draft ✅
- Run Consistency Loop until 3 consecutive clean ✅
- References `consistency_loop_discovery.md` from Proposal 2 ✅

**Dependency check:**
- Proposal 3 depends on Proposal 1 (master protocol) ✅
- Proposal 3 depends on Proposal 2 (discovery variant) ✅
- **Status:** Dependencies satisfied ✅

**Integration check:**
- Does S1.P3 output feed into S2.P1.I1? YES - DISCOVERY.md is read in S2.P1.I1 Step 1 ✅

---

### S2: Feature Planning (Feature 01)

**Proposal 4 (S2.P1.I1 - Feature Discovery):**
- Step 1: Read DISCOVERY.md ✅ (from S1.P3)
- Step 2: Reference previous features (none for Feature 01) ✅
- Step 3: Targeted research + library compatibility ✅
- Step 4: Draft spec & checklist ✅
- Step 5: Document research findings → RESEARCH_NOTES.md (REQUIRED) ✅
- Step 6: Consistency Loop (embeds Gate 1) ✅

**Dependency check:**
- Needs `consistency_loop_discovery.md` from Proposal 2 ✅
- Needs DISCOVERY.md from S1.P3 ✅
- **Status:** Dependencies satisfied ✅

**Output check:**
- Creates: spec.md, checklist.md, RESEARCH_NOTES.md ✅
- All 3 files used later?
  - spec.md → used in I2, I3, S4, S5 ✅
  - checklist.md → used in I2, I3 ✅
  - RESEARCH_NOTES.md → audit trail (not directly used but valuable) ✅

---

**Proposal 4 (S2.P1.I2 - Checklist Resolution):**
- Step 1: Present checklist ✅
- Step 2: One-at-a-time resolution with "Correct Status Progression" protocol ✅
- Step 3: Update spec with answers ✅

**Protocol check:**
- 9-step "Correct Status Progression" prevents autonomous resolution ✅
- Example shows WRONG vs CORRECT behavior ✅

**Output check:**
- Updates: spec.md (with answers), checklist.md (all ANSWERED) ✅

---

**Proposal 4 (S2.P1.I3 - Refinement & Alignment):**
- Step 1: Per-feature alignment check ✅
  - For Feature 01: No previous features to align with ✅
- Step 1.5: Agent-to-agent communication (if parallel) ✅
  - For Feature 01: Not applicable (first feature) ✅
- Step 2: Consistency Loop (embeds Gate 2) ✅
- Step 3: If gaps → loop back to I2 ✅
- Step 4: Dynamic scope adjustment (if >35 items) ✅
- Step 4.5: Create Acceptance Criteria (MANDATORY) ✅
- Step 5: Gate 3 user approval ✅

**Edge case check - "Total Spec Rejection":**
- If user says "start over" → Ask user: I1 or S1? ✅
- Doesn't assume where to go ✅

**Output check:**
- Final: spec.md (approved, with acceptance criteria), checklist.md (all [x]) ✅

---

**Proposal 4 (S2.P2 - Cross-Feature Alignment):**
- For Feature 01 only: No other features to compare yet
- **Skip S2.P2 until more features complete S2.P1** ✅

---

### S2: Feature Planning (Feature 02)

**S2.P1.I1:**
- Step 2: Reference Feature 01 spec.md ✅
- Step 1.5: If finds issue in Feature 01 → agent-to-agent communication ✅

**Agent-to-agent check:**
- Creates message: `agent_comms/{SECONDARY_ID}_to_{PRIMARY_ID}.md` ✅
- Primary reviews during heartbeat (15 min) ✅
- Fix immediately (don't defer to S2.P2) ✅

**Integration question:** What if Feature 02 agent finds issue in Feature 01 AFTER Feature 01 completed S2.P1?
- Answer: Step 1.5 protocol says "fix immediately" ✅
- Primary agent can update Feature 01 spec.md ✅
- Feature 01 checklist already [x] by user - does it need re-approval? ⚠️ **POTENTIAL GAP**

Let me check if this is addressed...

**Checking Proposal 4 S2.P1.I3:**
- Gate 3: User approves spec + checklist
- After approval: checklist items marked [x]
- **What if spec changes after Gate 3?**
  - S2.P2 Step 3 says "Update affected feature spec.md files"
  - But doesn't mention re-approval requirement

**Is this a problem?**
- S2.P2 runs AFTER all features in group complete S2.P1
- If Feature 02 finds issue in Feature 01 during S2.P1.I1, it gets fixed immediately via agent-to-agent
- But this happens BEFORE S2.P2
- User has already approved Feature 01 at Gate 3
- Now Feature 01 spec is updated based on Feature 02's findings
- Should user re-approve? 🤔

**Checking current guides for precedent:**
Looking at agent-to-agent protocol (lines 630-670):
- Says "fix immediately"
- Says "Do NOT defer to S2.P2"
- Doesn't mention re-approval

**My assessment:** This is a MINOR GAP
- **Severity:** LOW-MEDIUM (user approved version A, gets version A')
- **Frequency:** UNCOMMON (requires parallel mode + issue found in completed feature)
- **Impact:** User might not know about changes made after approval
- **Mitigation:** Could add note to notify user of post-approval changes

**Decision:** Document as finding, assess if critical

---

### S2: Feature Planning (Feature 03)

Similar flow to Feature 02 ✅

---

### S2.P2: Cross-Feature Alignment (All 3 features done)

**Proposal 4 (S2.P2):**
- Step 0: Sync verification (if parallel) ✅
- Step 1: Verify group completion ✅
- Step 2: Pairwise comparison (3 features = 3 pairs: F1-F2, F1-F3, F2-F3) ✅
- Step 2.5: Save results to `S2_P2_COMPARISON_MATRIX_GROUP_1.md` ✅
- Step 3: Conflict resolution (update specs) ✅
- Step 4: Consistency Loop ✅

**Output check:**
- Creates: S2_P2_COMPARISON_MATRIX_GROUP_1.md ✅
- Updates: spec.md files if conflicts ✅

**Same re-approval question:** If specs updated in S2.P2, do they need re-approval?
- Specs were approved at Gate 3 (end of S2.P1.I3)
- Now they're updated in S2.P2
- User doesn't see updated version before S3
- ⚠️ Same GAP as above

---

### S3: Epic Planning & Approval

**Proposal 5 (S3.P1 - Epic Testing Strategy):**
- Steps 1-6 with expanded detail ✅
- Creates: epic_smoke_test_plan.md ✅

**Integration check:**
- Does epic_smoke_test_plan.md get used later? YES - S9.P1 (Epic Smoke Testing) ✅

**Proposal 5 (S3.P2 - Epic Documentation):**
- Updates: EPIC_README.md ✅

**Proposal 5 (S3.P3 - Epic Plan Approval):**
- Gate 4.5: User approves epic plan + testing strategy ✅

---

### S4: Feature Testing (Feature 01)

**Proposal 6 (S4 iterations 1-4):**
- I1: Test Strategy Development ✅
- I2: Edge Case Enumeration ✅
- I3: Configuration Change Impact ✅
- I4: Consistency Loop ✅
- **Output:** Creates `feature_01_name/test_strategy.md` ✅

**Integration check:**
- Does test_strategy.md get used in S5? YES - S5.P1.I1 Step 0 merges it ✅

---

### S5: Implementation Planning (Feature 01)

**Proposal 7 (S5.P1.I1 - enhanced):**
- **Step 0:** Merge test_strategy.md from S4 ✅
- **Prerequisites check (Issue #45 fix):**
  - Verify file exists ✅
  - Verify file has valid content (>50 bytes, has section headers) ✅
  - If invalid → escalate with 3 options ✅

**Integration check:**
- Prerequisite check protects against S4 failures ✅
- Content validation catches empty files ✅

**Proposal 7 (S5 renumbering - Issue #35 fix):**
- Round 1: I1-I7 ✅
- Round 2: I8-I13 ✅
- Round 3: I14-I22 ✅
- Total: 22 iterations ✅

**Proposal 7 (Gates 4a/7a - Issue #36 fix):**
- Gates 4a/7a embedded in Round 1 Consistency Loop ✅
- Checklist includes Gate 4a/7a criteria ✅

**Integration check:**
- Round 1 Consistency Loop runs after I7, before Round 2 (I8) ✅
- Timing makes sense ✅

---

### S6-S10: Later stages

Proposals 8, 9 don't change workflow structure, just add Consistency Loops to QC ✅

---

## Test 1 Result: Workflow Simulation

**Found:** 1 MINOR-MEDIUM GAP (spec changes after user approval)

---

## Test 2: Dependency Chain Validation

**Checking execution order from Proposal summary:**

### Phase 1: Foundation (Proposals 1-2)
1. Proposal 1: Master protocol ✅
2. Proposal 2: 5 context variants ✅
   - **Depends on:** Proposal 1 ✅

### Phase 2: Stage Redesigns (Proposals 6, 4, 5)
3. Proposal 6: S4 New Stage ✅
   - **Depends on:** Proposals 1, 2 ✅
4. Proposal 4: S2 Redesign ✅
   - **Depends on:** Proposals 1, 2 ✅
5. Proposal 5: S3 Redesign ✅
   - **Depends on:** Proposals 1, 2 ✅

### Phase 3: Stage Updates (Proposals 7, 9)
6. Proposal 7: S5 Update ✅
   - **Depends on:** Proposal 6 (S4 creates test_strategy.md) ✅
7. Proposal 9: CLAUDE.md Updates ✅
   - **Depends on:** Proposals 4-7 ✅

### Phase 4: Refinements (Proposals 3, 8, 10)
8. Proposal 3: S1 Discovery Update ✅
   - **Depends on:** Proposals 1, 2 ✅
9. Proposal 8: S7/S9 QC Updates ✅
   - **Depends on:** Proposal 2 (consistency_loop_qc_pr.md) ✅
10. Proposal 10: Templates ✅
    - **Depends on:** None ✅

**Dependency chain check:** All dependencies satisfied by execution order ✅

**Critical path check:**
- Proposal 1 must come first (master protocol) ✅
- Proposal 2 must come second (variants) ✅
- Proposal 6 must come before 7 (S4 before S5) ✅
- Proposals 4-7 must come before 9 (CLAUDE.md) ✅

**Status:** Dependency chain is CORRECT ✅

---

## Test 3: User Implementability

**Question:** Can user actually implement these proposals?

### Implementation Steps (from Proposal summary):

**Phase 1:** Create 1 master file + 5 variant files = 6 files
- Estimated: 3-4 hours
- **Feasible?** YES ✅

**Phase 2:** Create/modify 12 files for S2/S3/S4 redesigns
- Estimated: 8-12 hours
- **Feasible?** YES (spread over multiple sessions) ✅

**Phase 3:** Update S5 + CLAUDE.md
- Estimated: 3-5 hours
- **Feasible?** YES ✅

**Phase 4:** Update S1/S7/S9 + templates
- Estimated: 2-4 hours
- **Feasible?** YES ✅

**Total:** 19-30 hours
- **Feasible?** YES (1 week of full-time work, or 2-3 weeks part-time) ✅

**Commits planned:** 4 (one per phase) ✅

**Status:** User can implement ✅

---

## Test 4: Integration Testing (Cross-Proposal)

### Integration 1: Proposal 1 + Proposal 2
- Master protocol defines 7 principles ✅
- 5 variants reference master protocol ✅
- Each variant defines context-specific adaptations ✅
- **Integration:** WORKS ✅

### Integration 2: Proposal 2 + Proposals 4-7
- Proposals 4-7 reference specific variants ✅
- Example: S2.P1.I1 references `consistency_loop_discovery.md` ✅
- Example: S5 Round 1 references (implicitly) spec_refinement variant ✅
- **Integration:** WORKS ✅

### Integration 3: Proposal 4 + Proposal 6 + Proposal 7
- S2 creates spec.md ✅
- S4 uses spec.md to create test_strategy.md ✅
- S5 merges test_strategy.md into implementation_plan.md ✅
- **Chain:** S2 → S4 → S5 ✅
- **Integration:** WORKS ✅

### Integration 4: Proposal 5 + Proposal 8 + Proposal 9
- S3 creates epic_smoke_test_plan.md ✅
- S9 (from Proposal 8) uses epic_smoke_test_plan.md ✅
- CLAUDE.md (Proposal 9) documents both ✅
- **Integration:** WORKS ✅

### Integration 5: Proposal 4 (parallel) + Existing parallel infrastructure
- Agent-to-agent communication uses `agent_comms/` files ✅
- Matches existing parallel work file structure ✅
- References existing parallel work protocols ✅
- **Integration:** WORKS ✅

**Status:** All cross-proposal integrations WORK ✅

---

## Test 5: Stress Testing (Edge Cases)

### Stress Test 1: Consistency Loop Never Exits (Proposal 1, Issue #37)
**Scenario:** Agent loops 10 times, always finding new issues

**Protocol says:**
- If >10 rounds without 3 consecutive clean → STOP and escalate ✅
- Document issues from last 3 rounds ✅
- Give user 4 options ✅

**What if agent reaches Round 10 with 2 consecutive clean?**
- Protocol says "without achieving 3 consecutive clean loops"
- So Round 10 with 2 clean = hasn't achieved 3 consecutive yet
- Can continue to Round 11
- ✅ Wording allows this

**What if agent reaches Round 11 with 2 consecutive clean again?**
- Round 10: 0 issues (count = 1)
- Round 11: 0 issues (count = 2)
- Round 12: If 0 issues → count = 3, EXIT ✅
- Round 12: If issues found → count = 0, continue to Round 13
- **At Round 13:** >10 rounds, escalate ✅

**Status:** Stress test PASSES ✅

---

### Stress Test 2: User Rejects Everything at Every Gate
**Scenario:** User rejects at Gate 3, rejects at Gate 4.5, rejects at Gate 5

**Gate 3 (S2.P1.I3):**
- User rejects → Loop back to I3 Step 2 OR I1 OR S1 (user decides) ✅

**Gate 4.5 (S3.P3):**
- User rejects → What happens?
- **Checking Proposal 5 S3.P3...**
- Only shows "present and ask for approval"
- Doesn't show rejection handling ⚠️ **POTENTIAL GAP**

Let me verify if this is a gap or if it's implicit...

**Standard gate behavior:**
- Gates require user approval to proceed
- If user doesn't approve, agent doesn't proceed
- Agent would ask "what changes needed?" or "should I revise?"

**Is explicit rejection handling needed at Gate 4.5?**
- Gate 3 has explicit handling (Issue #38 fix) ✅
- Gate 5 (after S5) - not shown in proposals (existing behavior)
- Gate 4.5 (after S3) - not explicitly shown

**Is this a gap?**
- **Consistency issue:** Gate 3 has explicit rejection handling, Gate 4.5 doesn't
- **Impact:** MEDIUM (user might reject epic plan, agent unsure where to loop back)
- **Severity:** MEDIUM (inconsistency in gate handling)

**FINDING:** Gate 4.5 rejection handling not specified

---

### Stress Test 3: File System Failures
**Scenario:** Agent tries to create file, but file system is full / permission denied

**Proposal 4 S2.P1.I1:**
- Creates: spec.md, checklist.md, RESEARCH_NOTES.md
- **What if file creation fails?**
- Not addressed in proposals

**Proposal 6 S4:**
- Creates: test_strategy.md
- **What if file creation fails?**
- Proposal 7 S5 checks if file exists and has content
- But doesn't distinguish between "S4 failed to create" vs "S4 created but empty"

**Is this a gap?**
- **Scope question:** Should proposals handle file system errors?
- **My assessment:** NO - this is implementation-level error handling, not workflow design
- File system errors would cause immediate failure, agent would report error to user
- Not a workflow design issue

**Status:** Not a gap (out of scope) ✅

---

### Stress Test 4: Parallel Work - All Secondary Agents Stale
**Scenario:** Primary runs S2.P2, all 3 secondary agents are stale (>60 min)

**Proposal 4 S2.P2 Step 0:**
- Check for stale agents (>60 min) ✅
- If stale → escalate ✅
- **What if ALL agents stale?**
- Protocol says "send status check, wait for response"
- But if all 3 are stale, Primary is alone

**What should happen?**
- Existing parallel work protocols handle this (stale agent protocol)
- Primary would escalate to user
- User decides: wait, investigate, or abort parallel mode

**Is this a gap?**
- NO - existing parallel work protocols handle this ✅
- Proposal 4 correctly references existing protocols

**Status:** Not a gap ✅

---

### Stress Test 5: Circular Dependencies in Features
**Scenario:** Feature 01 depends on Feature 02, Feature 02 depends on Feature 01

**When detected?**
- S2.P2 pairwise comparison should detect this ✅
- "Integration dependencies" is one of the 6 check categories ✅

**What happens?**
- Conflict resolution (Step 3) updates specs ✅
- But doesn't specify HOW to resolve circular dependency

**Is this a gap?**
- **Scope question:** Should proposals prescribe HOW to resolve specific conflict types?
- **My assessment:** NO - conflict resolution requires human judgment
- S2.P2 detects issue, escalates to Primary agent
- Primary agent uses judgment or escalates to user
- Not a workflow gap

**Status:** Not a gap (requires human judgment) ✅

---

## Test 5 Result: Stress Testing

**Found:** 1 MEDIUM GAP (Gate 4.5 rejection handling not specified)

---

## Round 5 Findings

**Total issues found:** 2

### Issue #46: Post-Approval Spec Changes (MINOR-MEDIUM)
**Where:** Proposal 4, S2.P1.I3 + S2.P2
**Problem:** Specs can be updated after Gate 3 approval without re-approval
**Scenarios:**
1. Feature 02 finds issue in Feature 01 during S2.P1.I1 Step 1.5 (parallel mode)
2. S2.P2 finds conflicts and updates specs

**Current behavior:**
- User approves spec at Gate 3
- Spec gets updated afterward (by agent-to-agent comm or S2.P2 conflict resolution)
- User doesn't see updates before proceeding to S3

**Should user re-approve?**
- **Arguments FOR:** User approved version A, transparency requires showing version A'
- **Arguments AGAINST:** Changes are alignment/conflict fixes (not scope changes), would slow workflow

**Impact:** MEDIUM (transparency issue, but likely minor changes)
**Frequency:** UNCOMMON (requires finding issues in already-approved specs)
**Severity:** LOW-MEDIUM (user might not know about post-approval changes)

---

### Issue #47: Gate 4.5 Rejection Handling Not Specified (MEDIUM)
**Where:** Proposal 5, S3.P3 (Gate 4.5)
**Problem:** Gate 3 has explicit rejection handling (Issue #38 fix), Gate 4.5 doesn't
**Scenario:** User rejects epic plan at Gate 4.5

**Current behavior:**
- Proposal 5 shows: "Ask: 'Approve this epic plan and testing strategy?'"
- Proposal 5 shows: "Cannot proceed without approval"
- Proposal 5 does NOT show: What happens if user rejects?

**Missing:**
- Where to loop back? (S3.P1? S2? S1?)
- What options to give user?

**Impact:** MEDIUM (inconsistency with Gate 3 handling)
**Severity:** MEDIUM (agent unsure what to do if user rejects)

**Comparison with Gate 3:**
- Gate 3: Explicit "If User Requests Changes" + "If User Rejects Entire Approach" ✅
- Gate 4.5: No rejection handling specified ❌

---

## Round 5 Verdict

**New Issues Found:** 2 (1 minor-medium, 1 medium)

**Quality Assessment:**
- Round 4 fix (Issue #45) worked correctly ✅
- No new issues introduced by Round 4 fix ✅
- Workflow simulation revealed 2 new gaps ✅
- Dependency chain is correct ✅
- User can implement proposals ✅
- Cross-proposal integrations work ✅

**Issues:**
1. **Issue #46:** Post-approval spec changes (MINOR-MEDIUM)
2. **Issue #47:** Gate 4.5 rejection handling (MEDIUM)

**Consecutive Clean Count:**
- Round 1: 20 issues → fixed
- Round 2: 10 issues → fixed
- Round 3: 13 issues → fixed
- Round 4: 1 minor gap → fixed
- Round 5: 2 issues found
- **Count: 0** (not 3 consecutive clean rounds yet)

**Severity Assessment:**
- **Issue #46:** Could defer (document as "known limitation" - minor changes after approval)
- **Issue #47:** Should fix (consistency with other gates)

**Recommendation:**
- **Fix Issue #47** (Gate 4.5 rejection handling) - takes 5-10 minutes
- **Defer Issue #46** (post-approval changes) - document as "considered limitation"
  - Rationale: Changes are alignment/conflict fixes, not scope changes
  - User can review updated specs at Gate 4.5 (before S4 starts)
  - Adding re-approval would slow workflow significantly

**Alternative:** Fix both (takes 15-20 minutes total)

---

## Proposed Fixes

### Fix for Issue #47: Gate 4.5 Rejection Handling

**Add to Proposal 5, S3.P3, after Gate 4.5:**

```markdown
**If User Requests Changes:**
- Update epic_smoke_test_plan.md or EPIC_README.md based on feedback
- **LOOP BACK to appropriate phase:**
  - If testing strategy issues → S3.P1 (Epic Testing Strategy)
  - If documentation issues → S3.P2 (Epic Documentation)
  - If fundamental approach wrong → S2 (Feature Planning)
- Re-run updated phase with Consistency Loop
- Re-present to user for approval
- Continue until user explicitly approves

**If User Rejects Entire Epic Approach:**
- User says: "This epic scope/approach is fundamentally wrong"
- **STOP - Do not loop back to S3**
- Ask user: "Should I:"
  - (A) Re-do Discovery Phase (S1.P3) - rethink entire epic
  - (B) Revise feature breakdown (S1.P4) - keep epic, change features
  - (C) Exit epic planning - cancel epic
- Await user decision
- **Rationale:** Total rejection at epic level indicates fundamental misalignment
```

### Fix for Issue #46: Post-Approval Spec Changes (if user wants it)

**Add to Proposal 4, S2.P1.I3, after Step 1.5:**

```markdown
**Note on Post-Approval Changes:**
If specs are updated after Gate 3 approval (via agent-to-agent communication in Step 1.5 or conflict resolution in S2.P2), these changes will be alignment fixes (naming, data structures, integration points) rather than scope changes.

**User Visibility:**
- Updated specs will be reviewed by user at Gate 4.5 (S3.P3)
- User can verify alignment changes at that time
- If user objects to changes, can request revision back in S2

**Alternative (High Transparency):**
If strict approval tracking required, add notification step:
- After S2.P2 completes, list all features whose specs were updated
- Present summary of changes to user: "Feature 01 spec updated: aligned naming convention with Feature 02"
- Ask user: "Acknowledge these alignment changes before proceeding?"
```

---

**Status:** Round 5 complete - 2 issues found (1 should fix, 1 optional)
**Next Action:** User decides:
- (A) Fix Issue #47 only (recommended)
- (B) Fix both Issues #46 and #47
- (C) Defer both (document as considerations)
