# Feature 1: Add K and DST Support to Ranking Metrics - Planning Checklist

**Status:** Stage 2 complete (specification with traceability)

**Purpose:** Track open questions and decisions for this feature

**Instructions:**
- [ ] = Open question (needs user answer)
- [x] = Resolved (answer documented below)

---

## Open Questions

**NO OPEN QUESTIONS**

**Why no questions:**
The user provided exceptionally thorough epic notes with:
- Exact line numbers to change (258, 544)
- Explicit constraints (filtering logic acceptable, defer adaptive top-N)
- Complete research tasks (all 7 systematically executed)
- Clear acceptance criteria (Must Have vs Nice to Have)
- Edge case analysis (small sample size, scoring patterns)

All technical details were either:
1. **Explicitly specified in epic notes** (what to change, where to change it)
2. **Verified through research** (no other changes needed, existing logic works)
3. **Derived requirements** (testing, documentation consistency)

---

## Resolved Questions

**All decisions resolved during epic creation and research phase:**

### Decision 1: Which lines to modify?
- [x] **Resolved:** Lines 258 and 544 specified in epic notes
- **Source:** Epic notes lines 78-84, 87-93
- **Answer:** Both lines required (line 544 calculates, line 258 aggregates)

### Decision 2: Should we change filtering logic?
- [x] **Resolved:** NO - keep existing threshold (actual >= 3.0)
- **Source:** Epic notes line 171: "Current filtering (actual >= 3.0) is acceptable for K/DST"
- **Answer:** No changes to lines 364, 430, 491

### Decision 3: Should we implement adaptive top-N?
- [x] **Resolved:** NO - defer as optional enhancement
- **Source:** Epic notes line 129: "Start with simple fix (just add K/DST to positions list)"
- **Answer:** Use existing top-5, top-10, top-20 for all positions

### Decision 4: What testing is required?
- [x] **Resolved:** Unit tests for K/DST metrics, integration test validation
- **Source:** Derived requirement (testing required for correctness)
- **Answer:** Add K/DST test cases, verify 100% pass rate

### Decision 5: What documentation needs updating?
- [x] **Resolved:** ACCURACY_SIMULATION_FLOW_VERIFIED.md
- **Source:** Epic notes line 355 (Must Have acceptance criterion)
- **Answer:** Update per-position metrics section, remove MAE-only caveat

### Decision 6: How to handle small sample size (N=32)?
- [x] **Resolved:** Accept existing behavior (debug logs for small pools)
- **Source:** Epic notes line 106-108 analysis, line 137 mitigation section
- **Answer:** Top-20 will trigger warnings (acceptable), no code changes needed

### Decision 7: Do other files need changes?
- [x] **Resolved:** NO - verified through Research Tasks 1-7
- **Source:** Research phase (Phase 1, all 7 tasks)
- **Answer:** AccuracyResultsManager, logging, metric methods already handle K/DST dynamically

---

## Additional Scope Discovered

**NO additional scope discovered**

**Research confirmed:**
- Minimum changes: Exactly 2 lines (258, 544) as user specified
- Documentation changes: 2 docstrings (351, 535) for consistency
- No unexpected complications
- All edge cases already handled in existing code

**Scope remains:** Simple fix (add K/DST to positions list) as user requested

---

## Notes

**Epic Quality:** Exceptionally well-specified
- User provided exact line numbers
- User completed initial technical analysis
- User identified minimum required changes
- User distinguished Must Have from Nice to Have
- User provided complete research task list

**Agent Verification:**
- Executed all 7 research tasks systematically
- Confirmed user's analysis was correct (lines 258, 544 are only code changes)
- Verified no other files require modifications
- Documented findings with evidence (file paths, line numbers, code snippets)

**Result:** Zero ambiguity, zero open questions, ready for implementation planning (Stage 5a)
