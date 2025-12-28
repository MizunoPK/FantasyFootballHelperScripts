# Algorithm Traceability Matrix Protocol

**Purpose:** Ensure spec algorithms are implemented exactly, including all conditional logic.

**Related:** [README.md](README.md) - Protocol index

---


**Execute during:** Iterations 4, 11, and 19

**Steps:**

1. **For each calculation, formula, or algorithm in the spec:**
   - Extract the EXACT logic from the spec (quote it word-for-word)
   - Document which code file/method will implement it
   - Note any conditional logic (e.g., "if week < X then A, else B")

2. **Create matrix in TODO file:**
   ```
   | Spec Section | Algorithm Description | Code Location | Conditional Logic |
   |--------------|----------------------|---------------|-------------------|
   | Lines 158-186 | projected week columns | generator.py | week < X: historical, week >= X: current |
   | Lines 241-276 | player_rating calc | generator.py | week 1: draft rank, week 2+: cumulative |
   ```

3. **Verify during implementation:**
   - Each algorithm has a matching code location
   - Conditional branches match spec exactly
   - No "simplified" implementations that ignore spec conditions

---

