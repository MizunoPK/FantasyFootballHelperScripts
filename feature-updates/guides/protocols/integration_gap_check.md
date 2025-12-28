# Integration Gap Check Protocol

**Purpose:** Ensure all new code will actually be called from entry points (no orphan code).

**Related:** [README.md](README.md) - Protocol index

---


> *Rationale: The #1 cause of "feature complete but doesn't work" is orphan code - methods that exist, have tests, but are never called from the actual entry point. This protocol catches that pattern.*

**Execute during:** Iterations 7, 14, and 23

**Steps:**

1. **Create Integration Matrix:**
   ```
   | New Component | File | Called By | Caller File:Line | Caller Modification Task |
   |---------------|------|-----------|------------------|--------------------------|
   | save_configs_folder() | ResultsManager.py | run_iterative() | SimulationManager.py:261 | Task 4.2 |
   ```

2. **Verify Caller Modifications in TODO:**
   - For each row in the matrix, confirm a TODO task exists to modify the caller
   - If missing → add the task immediately
   - Flag with warning if integration was previously overlooked

3. **Check for Orphan Code:**
   - Any new component without a caller = orphan code
   - Either add caller modification task OR remove the orphan component

4. **Verify Entry Point Coverage:**
   - For each entry point affected by requirements
   - Trace through to output
   - Confirm all new code is in the execution path

5. **Check Entry Script File Discovery** (if output format changes):
   - List all `run_*.py` scripts that auto-detect files
   - Verify glob patterns match new output format
   - Add TODO tasks for any entry script updates needed

6. **Cross-Feature Impact Check:**
   Before marking integration complete, verify no unintended impacts on existing features:

   a. **List all files modified** (from TODO's "Files to Modify" section)

   b. **For each modified file, identify:**
      - What OTHER features use this file?
      - What callers besides your new code use modified methods?
      - Use: `grep -r "modified_method\(" .` to find all callers

   c. **For each affected feature:**
      - Do existing tests still pass? (They should if run after each phase)
      - Does behavior change for existing use cases?
      - If behavior changes intentionally, document it
      - If behavior changes unintentionally, fix it

   d. **Create impact matrix if multiple features affected:**
      ```
      | Modified File | Other Features Using It | Impact | Mitigation |
      |---------------|------------------------|--------|------------|
      | PlayerManager.py | Trade Mode, Starter Mode | None - added new method | N/A |
      | ConfigManager.py | All modes | Changed return type | Updated all callers |
      ```

   **Why this matters:** Features don't exist in isolation. Changes can have ripple effects that aren't caught by the feature's own tests.

7. **Check for Unresolved Alternatives (CRITICAL):**
   - Search TODO for "Alternative:" notes - these indicate unresolved decisions
   - Search TODO for "May need to..." phrases - these indicate uncertainty
   - For each unresolved item:
     - Document the options with pros/cons
     - Create a question in the questions file
     - DO NOT proceed past verification until user decides

   **Valid deferral reasons:**
   - "Will be created when X runs" (file generation)
   - "Low priority, not blocking" (documentation)

   **Invalid deferral reasons (must resolve NOW):**
   - "Requires user decision" → Should have been asked during planning
   - "Multiple approaches possible" → Should have been decided during planning

---

