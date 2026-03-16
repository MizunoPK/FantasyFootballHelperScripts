# S4 Prompts: Feature Testing Strategy

> **⚠️ DEPRECATED (SHAMT-6):** S4 has been deprecated. Test Scope Decision is now Step 0 of S5.
> Do NOT follow these prompts for new epics. See `stages/s4/archive/s4_feature_testing_strategy.md` for the redirect stub (archived).

**Stage:** 4 (DEPRECATED)
**Purpose:** (Deprecated) Feature-level test strategy creation based on feature specs

---

## Starting S4: Feature Testing Strategy

**User says:** "Plan tests for {feature_name}" or "Start feature testing strategy" or Agent detects S3 complete

**Prerequisite:** S3 complete (Gate 4.5 passed — user approved epic plan in S3.P3)

**Agent MUST respond:**

```markdown
I'm reading `stages/s4/s4_feature_testing_strategy.md` to ensure I create a comprehensive feature testing strategy...

**The guide requires:**
- Create feature-level test_strategy.md (NOT updating epic_smoke_test_plan.md — that was done in S3.P1)
- 4 iterations:
  - I1: Test Strategy Development — test coverage matrix (unit, integration, edge)
  - I2: Edge Case Enumeration — boundary conditions, error paths
  - I3: Configuration Change Impact — config test matrix
  - I4: Validation Loop — 3 consecutive clean rounds required
- >90% coverage goal (feature-level, not epic-level)
- Traceability required: each test links to a spec.md requirement
- Output: test_strategy.md (agent-validated only, NO user approval gate)

**Note:** S4 has ZERO formal gates. Gate 4.5 was passed in S3.P3. test_strategy.md is
validated by Validation Loop (I4), not by user approval.

**Prerequisites I'm verifying:**
✅ S3 complete (Gate 4.5 passed — user approved epic plan in S3.P3)
✅ Feature spec.md finalized and user-approved (Gate 3 passed from S2)
✅ Feature README.md has Agent Status section

**Updating feature README.md Agent Status:**
- Current Stage: S4 - Feature Testing Strategy
- Current Guide: stages/s4/s4_feature_testing_strategy.md
- Guide Last Read: {YYYY-MM-DD HH:MM}
- Critical Rules: "plan tests BEFORE implementation", ">90% coverage goal", "4 iterations mandatory", "Validation Loop (I4) = 3 consecutive clean rounds", "NO user approval gate in S4"
- Next Action: Begin I1 (Test Strategy Development) for {feature_name}

Starting feature test strategy...
```

---

## S4 Complete: Transition to S5

**Trigger:** Agent completes S4.I4 Validation Loop (3 consecutive clean rounds), creates test_strategy.md

**Agent MUST confirm:**

```markdown
✅ **S4 Complete — Feature Testing Strategy Done**

**test_strategy.md created for {feature_name}:**
- **Unit tests:** {N} test cases defined
- **Integration tests:** {N} test cases defined
- **Edge cases:** {N} edge cases catalogued
- **Config tests:** {N} configuration scenarios defined
- **Coverage:** {N}% (goal: >90%)
- **Traceability:** All {N} requirements have test coverage

**Validation Loop (I4) passed:** 3 consecutive clean rounds confirmed
**No user approval needed:** S4 is agent-validated only (Gate 4.5 was in S3.P3)

**Updating feature README.md Agent Status:**
- Agent Status: S4_COMPLETE
- S4 completion: {YYYY-MM-DD HH:MM}

**Next: S5 (Implementation Planning)**

Reading `stages/s5/s5_v2_validation_loop.md` to create comprehensive implementation plan.
S5.P1.I1 will verify test_strategy.md exists and merge it into implementation_plan.md.
```

---

*For prompts for other stages, see the [prompts index](../prompts_reference_v2.md)*
