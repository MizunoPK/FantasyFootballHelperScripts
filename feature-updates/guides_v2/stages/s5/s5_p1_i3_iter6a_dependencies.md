# S5: Feature Implementation
## S5.P1: Planning Round 1
### S5.P1.I3: External Dependency Verification

**Purpose:** External Dependency Verification
**Prerequisites:** Previous iterations complete
**Main Guide:** `stages/s5/s5_p1_planning_round1.md`
**Router:** `stages/s5/s5_p1_i3_integration.md`

---

## Iteration 6a: External Dependency Final Verification (NEW - from KAI-1 lessons)

**Purpose:** Re-verify external library assumptions before implementation

**Prerequisites:**
- Iteration 6 complete (Error handling scenarios documented)
- S1 Discovery identified potential external dependencies
- S2 Research tested library compatibility

**Historical Context (KAI-1 Feature 02):**
- Feature assumed library would work without final verification
- Result: 6/16 tests failed during S7
- Time cost: 2 hours debugging + workaround
- **This final checkpoint catches missed assumptions**

---

### Quick Re-Verification Checklist

**If S1 and S2 verified external dependencies:**

This is a quick checkpoint (5-10 minutes) to ensure nothing was missed:

- [ ] Review S1 Discovery: Were external dependencies identified?
- [ ] Review S2 Research: Were libraries tested with test environment?
- [ ] Check implementation_plan.md: Are workarounds documented?
- [ ] Verify: No NEW external dependencies added since S2

**If verification PASSED in S1/S2:**
- ✅ Proceed to Checkpoint (no additional work needed)

**If verification was SKIPPED or INCOMPLETE in S1/S2:**
- ⚠️ **STOP** - Perform full verification NOW (see below)

---

### Full Verification (If Skipped in S1/S2)

**Only perform if external dependencies were NOT verified in S1/S2:**

**1. List ALL External Libraries:**
```markdown
External libraries this feature uses:
- ESPN API (espn_api package) - fetch player data
- pandas - CSV manipulation
- requests - HTTP calls
```

**2. For EACH Library, Quick Test:**
```python
# Test library with test environment
# 10 minutes per library
```

**3. Document Findings:**
```markdown
Library: ESPN API
Compatibility: ✅ Works with mocks
Workaround: None needed
```

**4. Add Workaround Tasks (if needed):**
- Update implementation_plan.md with test client tasks
- Add time estimates

---

### Decision Point

**All libraries verified compatible?**
- ✅ Proceed to Checkpoint

**Library incompatible, no workaround planned?**
- ❌ **STOP** - Add workaround tasks to implementation_plan.md
- Document approach, add tasks, update time estimates
- Then proceed to Checkpoint

**NEW external dependency discovered?**
- ❌ **STOP** - Verify compatibility NOW (can't wait until S7)
- Test with test environment
- Document findings
- Add tasks if needed
- Then proceed to Checkpoint

---

**Time Investment:**
- If S1/S2 verification done: 5 minutes (quick checklist)
- If S1/S2 verification skipped: 15-30 minutes per library (full verification)

**Why This Final Checkpoint?**
- Catches dependencies added during planning (not in S1/S2)
- Ensures workarounds are actually in implementation_plan.md
- Last chance before implementation to avoid S7 debugging

**Update Agent Status:**
```bash
Progress: Iteration 6a/9 (Planning Round 1) complete - External dependencies verified
Next Action: Checkpoint - After Iterations 5-6a
Critical Finding: [X libraries verified, Y workarounds in plan]
```

---

## Checkpoint: After Iterations 5-6a (UPDATED)

**Before proceeding to Iteration 7:**

**Verify:**
- [ ] End-to-end data flow documented
- [ ] Data flow tests added to implementation_plan.md
- [ ] ALL downstream consumption locations identified (grepped comprehensively)
- [ ] OLD vs NEW API comparison completed
- [ ] ALL breaking changes documented
- [ ] Consumption update tasks added (if needed)
- [ ] ALL error scenarios from spec.md documented
- [ ] Error handling logic defined for each scenario
- [ ] Error handling tasks added to implementation_plan.md
- [ ] External dependencies verified compatible (or workarounds planned) - NEW

**Files Updated:**
- ✅ implementation_plan.md - Data flow diagram added
- ✅ implementation_plan.md - E2E test task added
- ✅ implementation_plan.md - Consumption update tasks added (if breaking changes)
- ✅ implementation_plan.md - Error handling tasks added
- ✅ questions.md - Updated with new questions/answers (if any)
- ✅ feature README.md Agent Status - Progress: Iteration 6/9 complete

**Critical Verification:**
- ✅ **Iteration 5a prevents catastrophic bugs** - Consumption code verified

**Next:** Read `stages/s5/s5_p1_i3_integration.md` for Integration Gap Check

---

**END OF ITERATIONS 5-6**
# Planning Round 1: Iteration 7 - Integration & Compatibility

**Purpose:** Verify all new code is integrated (no orphans) and handles backward compatibility
**Prerequisites:** Iteration 6 complete (s5_p1_i2_algorithms.md)
**Next:** Planning Round 1 Checkpoint, then Planning Round 2 (s5_p2_planning_round2.md)
**Main Guide:** `stages/s5/s5_p1_planning_round1.md`

---

## Overview

Iteration 7 has two parts:
- **Iteration 7:** Integration Gap Check - Verify EVERY new method has a caller
- **Iteration 7a:** Backward Compatibility Analysis - Handle old data formats gracefully

**Why These Matter:**
- Iteration 7: Prevents orphan code that never gets called ("If nothing calls it, it's not integrated")
- Iteration 7a: Prevents bugs from loading old files created before this epic

---

