# Edge Case Verification Protocol

**Purpose:** Ensure every edge case has both a task and a test.

**Related:** [README.md](README.md) - Protocol index

---


**Execute during:** Iteration 20

**Steps:**

1. **List all edge cases from spec**
   - Search spec for words like: "if", "when", "unless", "except", "edge", "special"
   - List conditions: empty data, missing fields, zero values, max values
   - List states: bye weeks, injuries, trades, new players

2. **For each edge case, verify:**
   - [ ] Task exists in TODO to handle this case
   - [ ] Test planned that specifically tests this case
   - [ ] Expected behavior documented

3. **Create edge case matrix:**
   ```
   | Edge Case | TODO Task | Test Planned | Expected Behavior |
   |-----------|-----------|--------------|-------------------|
   | Empty roster | Task 3.2 | test_empty_roster | Return empty list |
   | Bye week | Task 4.1 | test_bye_week_handling | Score = 0, not null |
   ```

4. **Fill gaps**
   - Add tasks for unhandled edge cases
   - Add tests for untested edge cases

**Output:** Complete edge case matrix with no gaps.

---

