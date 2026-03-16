# Common Mistakes Across All Stages

**Purpose:** Quick reference for anti-patterns and mistakes to avoid

**Note:** This is a summary. See individual stage guides for detailed "Common Mistakes" sections with full context.

---

## 🚨 Critical Mistakes (Can Block Progress)

### Skipping Mandatory Reading
- ❌ "I'm familiar with the process, I'll skip the guide"
- ✅ ALWAYS read the ENTIRE guide before starting stage
- **Why:** 40% guide abandonment rate without reading

### Skipping Phase Transition Prompts
- ❌ Starting work without using phase transition prompt
- ✅ ALWAYS use prompt from prompts_reference_v2.md
- **Why:** Proves guide was read, prevents missed requirements

### Proceeding Without User Approval
- ❌ "User will probably approve, I'll just proceed"
- ✅ WAIT for explicit user approval at gates
- **Why:** Wastes hours of work if user wants changes

### Skipping Validation Dimensions
- ❌ "Dimension 7 seems obvious, I'll skip it in this round"
- ✅ ALL 11 dimensions in S5 v2 are MANDATORY every validation round, and the Validation Loop must be completed (3 consecutive clean rounds)
- **Why:** Each dimension catches specific bug categories

### Committing Without Tests
- ❌ Committing code without running full test suite
- ✅ Run tests, verify 100% pass, THEN commit
- **Why:** Breaking tests blocks other developers

---

## ⚠️ High-Impact Mistakes (Cause Rework)

### Assuming Interfaces
- ❌ "ConfigManager probably has get_config() method"
- ✅ READ actual source code, verify exact method signature
- **Why:** Wrong assumptions cause implementation failures

### Batching Root Cause Analysis
- ❌ "I'll analyze all bugs together after fixing"
- ✅ Phase 4b IMMEDIATELY after each bug (per-issue)
- **Why:** Context loss reduces analysis quality by 3x

### Deferring Issues
- ❌ "I'll fix this TODO comment later"
- ✅ Fix ALL issues immediately (zero tech debt)
- **Why:** "Later" often never comes

### Not Updating Agent Status
- ❌ Forgetting to update README Agent Status
- ✅ Update after EACH major checkpoint
- **Why:** Breaks resumability after session compaction

### Not Following Validation Loop Protocol
- ❌ "I fixed the bug, I'll just continue from where I left off"
- ✅ Fix issue immediately, reset clean counter to 0, continue validation
- **Why:** Validation Loop uses fix-and-continue approach (3 consecutive clean rounds required)

---

## 📋 Stage-Specific Mistakes

### S1: Epic Planning
- ❌ Creating folders before user approves feature breakdown
- ❌ Skipping SHAMT number assignment
- ❌ Making epic_smoke_test_plan.md too detailed (should be placeholder)
- ❌ Creating a documentation feature (handled in S7.P3 + S10, unless user explicitly requests it)
- ❌ Using shallow check for spec dependencies in Step 5.7.5: "Can I identify WHAT to build from Discovery?" → Use deep check: "Can I write a COMPLETE spec without knowing upstream's output structure?" (SHAMT-10: 7 agents paused mid-S2 from this mistake)
- ❌ Assuming integration/test/framework/orchestration/wrapper features have no spec dependencies — they almost always do (they describe HOW to interact with other features, which requires knowing those features' specs)

### S2: Feature Deep Dives
- ❌ Marking checklist.md items resolved autonomously (agents create QUESTIONS, users provide ANSWERS)
- ❌ Skipping S2.P1 Validation Loop (spec validation is embedded in S2.P1.I3)
- ❌ Not getting user approval for checklist (Gate 3)

### S3: Epic-Level Docs, Tests, and Approval
- ❌ Only checking new features (must check ALL pairwise)
- ❌ Resolving conflicts without user input
- ❌ Not getting user approval (Gate 4.5 — epic plan + test strategy approval occurs in S3.P3)

### S4: (Deprecated — redirects to S5)
- ❌ Trying to follow S4 as an active stage — S4 is deprecated; test scope decision is now S5 Step 0
- ❌ Creating a separate test_strategy.md file — this file is no longer required (Options A/B only); use S5 Step 0 instead

### S5: Implementation Planning
- ❌ Skipping dimensions or gates in the Validation Loop
- ❌ Exiting the Validation Loop before achieving 3 consecutive clean rounds (confidence must be MEDIUM or HIGH)
- ❌ Proceeding without user approval of implementation_plan.md (Gate 5)

### S6: Implementation
- ❌ Not keeping spec.md visible at all times
- ❌ Not running tests after each component
- ❌ Not updating implementation_checklist.md continuously

### S7: Post-Implementation
- ❌ Skipping smoke testing Part 3 (E2E with data verification)
- ❌ Not restarting from beginning after finding issues
- ❌ Leaving tech debt "to fix later"

### S8.P1: Cross-Feature Alignment
- ❌ Only updating next feature (must update ALL remaining)
- ❌ Not updating based on ACTUAL implementation

### S8.P2: Epic Testing Plan Update
- ❌ Not adding newly discovered integration points
- ❌ Keeping outdated test scenarios

### S9: Epic Final QC
- ❌ Skipping user testing (MANDATORY in Step 6)
- ❌ Not looping back to S9.P1 after bug fixes

### S10: Epic Cleanup
- ❌ Not running tests before committing
- ❌ Only checking epic lessons_learned.md (must check ALL sources)
- ❌ Moving features individually (move ENTIRE epic folder)
- ❌ Merging PR without user review

---

## 🔍 Debugging Protocol Mistakes

### Step 1: Discovery
- ❌ Not creating ISSUES_CHECKLIST.md
- ❌ Working on issues not in checklist

### Step 2: Investigation
- ❌ Exceeding 5 rounds without user escalation
- ❌ Not documenting failed hypotheses

### Step 3: Resolution
- ❌ Not adding tests for the fix

### Step 4: User Verification
- ❌ Self-declaring victory (user MUST confirm)
- ❌ Not presenting before/after state clearly

### Step 4b: Root Cause Analysis
- ❌ Batching Phase 4b until all bugs fixed
- ❌ Writing generic lessons ("be more careful")
- ❌ Not getting user confirmation of root cause

### Step 5: Loop Back
- ❌ Not doing cross-bug pattern analysis
- ❌ Not looping back to START of testing

---

## 💡 Protocol Selection Mistakes

### Missed Requirement vs Debugging
- ❌ Using debugging protocol when solution is KNOWN
- ❌ Using missed requirement when root cause is UNKNOWN
- ✅ Solution known? → Missed Requirement Protocol
- ✅ Requires investigation? → Debugging Protocol

---

## 📊 Documentation Mistakes

### Agent Status
- ❌ Not updating after major checkpoints
- ❌ Generic next actions ("continue working")
- ✅ Specific next actions ("Begin Validation Round 4 - Dimension 6")

### Commit Messages
- ❌ Vague messages ("fixed stuff", "updates")
- ❌ Including emojis or subjective prefixes
- ✅ Clear, descriptive, 100 chars or less

---

## 🎯 Quick Reference: Top 10 Mistakes

1. Skipping mandatory reading protocol
2. Not using phase transition prompts
3. Proceeding without user approval (gates)
4. Skipping iterations in S5
5. Assuming interfaces instead of verifying
6. Batching Phase 4b root cause analysis
7. Not updating Agent Status regularly
8. Committing without running tests
9. Not looping back to start after fixes
10. Only checking epic lessons (not all sources)

---

**See individual stage guides for detailed "Common Mistakes" sections with full context and examples.**

---

**END OF COMMON MISTAKES REFERENCE**
