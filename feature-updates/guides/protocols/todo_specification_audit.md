# TODO Specification Audit Protocol

**Purpose:** Ensure every TODO item has enough detail to implement WITHOUT re-reading specs. This prevents implementation drift where code is written from memory instead of specifications.

**Related:** [README.md](README.md) - Protocol index

---


**Execute during:** Iteration 4a (immediately after Algorithm Traceability Matrix)

**Historical Context:** Added after feature implementation passed all 24 iterations but failed QC Round 1 with 40% failure rate. Root cause: TODO items were too vague, causing agent to implement from memory instead of specs.

**Steps:**

1. **For EACH TODO item in implementation phases:**
   - Read corresponding spec section(s) line-by-line
   - Extract EXACT requirements (data structures, field lists, constraints, examples)
   - Add "ACCEPTANCE CRITERIA" section to the TODO item with:
     - ✓ Each specific requirement as checkable item
     - Example of correct output from specs
     - Anti-example of common mistake
     - Spec line reference for verification

2. **Self-audit each TODO item:**
   - [ ] "Can I implement this without re-reading specs?" (YES required)
   - [ ] "Do I know what the output should look like?" (YES required)
   - [ ] "Do I know what NOT to do?" (YES required)
   - If answer is NO to any → add more detail from specs

3. **Red flags to watch for:**
   - ⛔ "Transform to [vague description]" without showing structure
   - ⛔ "Build [thing]" without listing required fields
   - ⛔ "Add [feature]" without expected output example
   - ⛔ "Handle [case]" without specifying correct behavior
   - ⛔ Missing spec references
   - ⛔ No examples of correct output

4. **Quality template for TODO items:**
   ```
   - [ ] X.X: [Task name]

     ACCEPTANCE CRITERIA (from specs.md):

     ✓ REQUIREMENT 1: [Exact specification]
       - Spec: specs.md lines X-Y
       - Example: [correct output]
       - NOT: [common mistake] ❌

     ✓ REQUIREMENT 2: [Exact specification]
       - Spec: specs.md lines A-B
       - Example: [correct output]
       - NOT: [common mistake] ❌

     VERIFICATION:
     - [ ] Passes check 1
     - [ ] Passes check 2
   ```

5. **Completion criteria:**
   - [ ] Every TODO item has Acceptance Criteria section
   - [ ] Every criteria has spec reference
   - [ ] Every criteria has example or anti-example
   - [ ] Self-audit passes for all items

**Example - GOOD TODO item:**
```
- [ ] Build JSON output

  ACCEPTANCE CRITERIA (from specs.md):

  ✓ Root structure must be {"qb_data": [...]} (spec line 24)
    Example: {"qb_data": [player1, player2]}
    NOT: {"position": "QB", "players": [...]} ❌

  ✓ Each player must have 11 fields (spec lines 44-56):
    id (number), name, team, position, injury_status,
    drafted_by, locked, average_draft_position,
    player_rating, projected_points, actual_points
    NOT: Missing any fields ❌

  ✓ Arrays must be 17 elements (spec line 58-65)
    Example: [null, null, 23.4, 18.7, ...]
    NOT: Variable length arrays ❌
```

**Example - BAD TODO item:**
```
- [ ] Build JSON output
  - Create JSON structure
  - Include all fields
  - Handle arrays correctly
```
(Too vague - will lead to implementation from memory)

**Key Insight:** The TODO must be SELF-CONTAINED with all details from specs embedded as acceptance criteria. If implementing requires re-reading specs to know what "correct" looks like, the TODO has failed its purpose.

**Output:** TODO file with all items having detailed acceptance criteria extracted from specs.

---

