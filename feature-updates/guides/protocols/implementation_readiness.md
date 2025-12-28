# Implementation Readiness Protocol

**Purpose:** Final checklist before starting to write code.

**Related:** [README.md](README.md) - Protocol index

---


**Execute during:** Iteration 24

**Steps:**

1. **Verify all iterations complete:**
   - [ ] Iterations 1-23 marked complete in tracker
   - [ ] All protocol results documented
   - [ ] No pending items in any round

2. **Verify TODO completeness:**
   - [ ] Every spec requirement has a task
   - [ ] Every task has file path and line numbers
   - [ ] Every new method has caller modification task
   - [ ] Integration matrix is complete

3. **Verify test readiness:**
   - [ ] Test file locations identified
   - [ ] Test patterns from codebase documented
   - [ ] Behavior tests planned (not just structure tests)

4. **Final confidence check:**
   - [ ] No "TBD" or "TODO" placeholders in plan
   - [ ] No questions waiting for answers
   - [ ] No ambiguous requirements remaining

5. **Create implementation order:**
   - List tasks in dependency order
   - Mark which tests to write first
   - Identify rollback points

**Output:** "READY TO IMPLEMENT" or list of blockers.

---

### The Infrastructure Trap

A common failure pattern:
1. Create new methods/classes with tests
2. Tests pass
3. **BUT**: Methods never called from entry points
4. **RESULT**: Feature appears complete but doesn't work for users

**Example**: Created `save_optimal_configs_folder()` but `SimulationManager` still calls `save_optimal_config()`.

### Red Flags to Watch For

- "I created a new method but didn't modify any existing code to call it"
- "The tests pass but I haven't run the actual script"
- "I built the infrastructure but the manager still uses the old approach"
- "I changed the output format but entry scripts still look for the old format"

---

## Pre-Implementation Protocols

