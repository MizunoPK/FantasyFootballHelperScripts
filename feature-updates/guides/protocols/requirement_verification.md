# Requirement Verification Protocol

**Purpose:** Final verification before marking objective complete.

**Related:** [README.md](README.md) - Protocol index

---


**Execute:** After all implementation work appears complete, before moving to done/.

**Steps:**

**Step 1: Re-read Original Requirements File**
- Open and read EVERY LINE of the specification file: `feature-updates/{feature_name}/{feature_name}_specs.md`
- Create a checklist of EVERY requirement mentioned (numbered or implied)
- For each requirement, verify it has been implemented
- Mark each requirement as DONE or MISSING

**Step 2: Re-read Question Answers File**
- Open and read EVERY ANSWER in `feature-updates/{feature_name}/{feature_name}_questions.md`
- Create a checklist of EVERY answer that implies implementation work
- For each answer, verify the implementation matches what was answered
- Mark each answer as IMPLEMENTED or NOT IMPLEMENTED

**Step 3: Search Codebase for Implementation**
- Use Grep/Glob tools to search for evidence of each requirement
- Verify files were actually modified as required
- Check that new files were created if specified
- Confirm no placeholder code or TODOs remain

**Step 3.5: Algorithm Verification (CRITICAL)**

For each algorithm/calculation in the spec, verify the implementation matches **exactly**:

1. **Extract Algorithm from Spec**:
   - Quote the exact algorithm description from the original spec file
   - Note any conditional logic (if/else, week-specific, position-specific)
   - Identify edge cases mentioned in the spec

2. **Read Implementation Code**:
   - Open the file that implements this algorithm
   - Read the actual code line-by-line
   - Compare each condition and calculation to the spec

3. **Verify Logic Matches**:
   - For each conditional in the spec, find the corresponding code condition
   - For each calculation formula, verify the code implements it correctly
   - Check that edge cases are handled as specified

4. **Create Algorithm Verification Matrix**:
   ```
   | Spec Line | Algorithm | Code File:Line | Spec Says | Code Does | Match? |
   |-----------|-----------|----------------|-----------|-----------|--------|
   | 158-186 | projected weeks | generator.py:195 | week >= X: use projection | uses projection | YES |
   | 241-276 | player_rating | generator.py:147 | week 2+: cumulative | copies same rating | NO - MISMATCH |
   ```

5. **Fix Mismatches Immediately**:
   - Any MISMATCH requires immediate correction
   - Re-verify after fixing
   - Update tests to cover the algorithm behavior

**Common Algorithm Verification Failures**:
- Spec says "recalculate per iteration" but code calculates once
- Spec says "use value A for condition X, value B for condition Y" but code uses same value
- Spec describes conditional logic but code uses simplified unconditional logic
- Spec mentions edge cases but code doesn't handle them

**Step 4: Verify End-to-End Integration**
- For each NEW method/function created:
  - Search codebase to find what CALLS this method
  - If nothing calls it → INTEGRATION MISSING
  - Verify the caller is in the execution path from entry point
- For each requirement:
  - Trace from entry point (run_*.py) to output
  - Verify the new code is in the execution path
  - Run the actual script to confirm behavior (not just unit tests)
- Create integration evidence:
  ```
  Requirement: "Simulation outputs folders"
  New Method: save_optimal_configs_folder()
  Called By: SimulationManager.run_iterative_optimization() line 261
  Entry Point: run_simulation.py --mode iterative
  Verified: Running script produces folder output
  ```

**Step 5: Identify Missing Requirements**
- If ANY requirement is MISSING or NOT IMPLEMENTED or INTEGRATION MISSING:
  - STOP immediately
  - Update the TODO file
  - Document ALL missing requirements and integration gaps
  - Implement missing requirements before proceeding
  - Re-run this verification protocol

**Step 6: Document Verification**
- Add a "Requirements Verification" section to the code changes file
- List each requirement and its implementation status
- Include file paths and line numbers as evidence
- Confirm 100% requirement coverage

### Acceptance Criteria

```
╔═════════════════════════════════════════════════════════════════╗
║  🛑 CRITICAL: 100% COMPLETION REQUIRED - NO EXCEPTIONS         ║
╠═════════════════════════════════════════════════════════════════╣
║                                                                 ║
║  There is NO "acceptable partial" category.                    ║
║  There is NO "we'll finish it later" exception.                ║
║  There is NO "structure is done, data is pending" loophole.    ║
║                                                                 ║
║  EVERY requirement MUST be FULLY implemented.                  ║
║  EVERY data field MUST contain REAL data (not zeros/nulls).   ║
║  EVERY feature MUST achieve its PRIMARY USE CASE.              ║
║                                                                 ║
║  IF ANY REQUIREMENT IS INCOMPLETE:                             ║
║  → Requirement Verification FAILS                              ║
║  → Return to implementation immediately                        ║
║  → Complete ALL missing requirements                           ║
║  → Re-run verification from Step 1                             ║
║                                                                 ║
╚═════════════════════════════════════════════════════════════════╝
```

**Required for PASS:**

- ✅ ALL requirements from original file implemented (100% coverage)
- ✅ ALL question answers reflected in implementation
- ✅ NO missing functionality or partial implementations
- ✅ NO placeholder data (zeros, nulls, empty arrays where real data required)
- ✅ NO "TODO: implement later" comments in production code
- ✅ Evidence of implementation exists in codebase
- ✅ All unit tests pass (100%)
- ✅ Manual testing confirms functionality works
- ✅ Feature achieves its PRIMARY USE CASE completely
- ✅ ALL new methods have identified callers (no orphan code)
- ✅ Integration verified from entry point to output
- ✅ Actual scripts run and produce expected behavior
- ✅ Minimum 3 quality control review rounds completed
- ✅ Lessons learned reviewed and guide updates applied

**Automatic FAIL conditions:**

- ❌ Any requirement marked "partial" or "incomplete"
- ❌ Any data field with placeholder values (zeros, nulls) where real data expected
- ❌ Feature cannot achieve primary use case with current implementation
- ❌ Any "future work" or "pending" items that block core functionality

---

