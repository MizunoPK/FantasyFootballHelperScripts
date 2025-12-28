# End-to-End Data Flow Protocol

**Purpose:** Trace complete path from user action to system output; identify integration points.

**Related:** [README.md](README.md) - Protocol index

---


**Execute during:** Iterations 5 and 12

**Steps:**

1. **Identify Entry Points:**
   - List ALL user-facing scripts (run_*.py files)
   - List ALL manager classes that orchestrate operations
   - For EACH requirement, identify which entry point triggers it

2. **Trace Data Flow:**
   - For EACH requirement, document the complete path:
     ```
     Entry: run_simulation.py
       → SimulationManager.run_iterative_optimization()
       → ResultsManager.save_optimal_config()  ← CURRENT
       → ResultsManager.save_optimal_configs_folder()  ← REQUIRED
     ```
   - Identify WHERE in the flow the new code fits
   - Identify WHAT existing code needs to change

3. **Document Integration Points:**
   - For EACH new method/class, document:
     - What file it will be in
     - What existing method will CALL it
     - What line in the caller needs to change
   - Add these as explicit TODO tasks

4. **Verify No Orphan Code:**
   - Review each new component planned
   - Confirm each has a caller identified
   - If any new code has no caller → add integration task

5. **Weekly Mode Integration Check (for features with weekly projections):**
   - If feature uses `use_weekly_projection=True`, verify:
     - [ ] `calculate_max_weekly_projection(week_num)` is called BEFORE scoring
     - [ ] Result is assigned to `scoring_calculator.max_weekly_projection`
     - [ ] This initialization happens for EVERY week evaluated (not just once)
   - Compare to working reference: `StarterHelperModeManager` lines 452-453
   - Add TODO task: "Verify weekly projection initialization matches StarterHelperMode pattern"

---

