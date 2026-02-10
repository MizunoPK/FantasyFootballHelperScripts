# Validation Loop Pattern (Reference)

**Purpose:** Generic validation loop workflow applicable to both feature-level (S7.P2) and epic-level (S9.P2) quality control.

**This is a REFERENCE PATTERN.** Actual guides:
- **Feature-level:** `stages/s7/s7_p2_qc_rounds.md`
- **Epic-level:** `stages/s9/s9_p2_epic_qc_rounds.md`

---

## What is the Validation Loop?

**Definition:** The Validation Loop is an iterative quality control process that checks ALL dimensions every round until 3 consecutive clean rounds are achieved.

**Purpose:**
- Comprehensive validation beyond smoke testing
- Zero tech debt tolerance
- Fix-and-continue approach (no restart needed)
- All dimensions checked every round (not different focuses per round)

**Scope-Specific Implementation:**
- **Feature-level (S7.P2):** 11 dimensions validated
- **Epic-level (S9.P2):** 12 dimensions validated (7 master + 5 epic-specific)

---

## Validation Loop Structure

**The validation loop follows this pattern:**

```text
Each Round: Check ALL dimensions
   ↓ All dimensions checked every round
   ↓ Pass criteria: ZERO issues found
   ↓
   If CLEAN (0 issues) → Increment clean counter
      → If 3 consecutive clean rounds → EXIT (proceed to next stage)
      → Otherwise → Next round

   If ISSUES FOUND → Fix immediately
      → Reset clean counter to 0
      → Continue validation (next round)
      → No restart needed - fix-and-continue approach
```

---

## Universal Critical Rules

**These rules apply to ALL QC rounds (feature or epic):**

### 1. ALL 3 Rounds Are MANDATORY
- Cannot skip any round
- Must complete in order (Round 1 → 2 → 3)
- Each round has DIFFERENT focus
- Each round catches different issues

### 2. QC Restart Protocol
**If ANY round fails, RESTART from smoke testing:**

```text
VALIDATION LOOP PROTOCOL (v2.0):
1. Fix ALL issues found immediately
2. Reset clean counter to 0
3. Continue validation (no restart needed)
4. Exit after 3 consecutive clean rounds

WHY fix-and-continue?
- Saves 60-180 minutes per issue vs restart
- Maintains validation context
- Still achieves same quality (3 consecutive clean rounds)
```

**Issue Handling:**
- **Any Round:** Fix issues immediately, reset clean counter, continue
- **Exit Criteria:** 3 consecutive rounds with ZERO issues
- **Max Rounds:** 10 (escalate to user if exceeded)

### 3. NO Partial Work Accepted - ZERO TECH DEBT TOLERANCE

**These are INCOMPLETE (NOT acceptable):**
- "File structure correct but data pending"
- "Method exists but returns placeholder values"
- "Stat arrays created but filled with zeros"
- "90% complete, will finish later"
- "Working on my machine but not tested with real data"

**Rule:** If implementation cannot achieve 100% of spec requirements, it's INCOMPLETE

**NO shortcuts, NO "temporary" solutions, NO deferred work**

**Must be production-ready with ZERO tech debt**

### 4. Each Round Has Unique Focus

**Cannot skip rounds - each catches different issues:**
- **Round 1:** Basic validation (does it work at basic level?)
- **Round 2:** Deep verification (does it work correctly with all scenarios?)
- **Round 3:** Skeptical review (is it ACTUALLY complete and ready?)

**Progressive validation approach:**
- Round 1 catches obvious issues
- Round 2 catches subtle correctness issues
- Round 3 catches completeness gaps

### 5. Verify DATA VALUES (Not Just Structure)

**Every round must verify data VALUES are correct:**

```python
# ❌ NOT SUFFICIENT:
assert 'player_name' in df.columns  # Just checks column exists

# ✅ REQUIRED:
assert df['player_name'].notna().all()  # Verify values not null
assert (df['player_name'] != "").all()  # Verify values not empty
assert df['player_name'].str.len().min() > 2  # Verify reasonable values
```

**Examples:**
- Don't just check "column exists", verify values make sense
- Don't just check "logs exist", verify no unexpected WARNINGs
- Don't just check "file created", verify file contains correct data

### 6. Re-Reading Checkpoints

**Mandatory re-reading at specific points:**
- **After Round 1:** Re-read "Common Mistakes" section
- **After Round 2:** Re-read "Critical Rules" section
- **Before Round 3:** Re-read spec with fresh eyes (close it first to avoid confirmation bias)

**Why re-reading matters:**
- Prevents autopilot validation
- Ensures fresh perspective
- Catches issues missed in earlier rounds

### 7. Algorithm Verification

**Implementation must match spec EXACTLY:**
- Re-check Algorithm Traceability Matrix from S5
- Every algorithm in spec must map to exact code location
- Code behavior must match spec behavior (not interpretation)
- No "close enough" implementations

**Example:**
```markdown
# Spec says: "Sort players by projected_points DESC"
# Implementation must use: df.sort_values('projected_points', ascending=False)
# NOT acceptable: Sorting by rank ASC (even if equivalent)
```

### 8. 100% Requirement Completion

**ALL spec requirements must be implemented:**
- ALL spec requirements → implemented
- ALL checklist items → verified
- NO "we'll add that later" items
- Implementation is DONE or NOT DONE (no partial credit)

**If requirement cannot be met:**
- Get user approval to remove from scope
- Update spec to reflect removal
- Document why in lessons learned
- Do NOT leave requirements silently unimplemented

---

## Round 1: [Scope-Specific - See Implementation Guides]

**Universal Pattern:**
- **Objective:** Basic validation
- **Time Estimate:** 10-20 minutes
- **Pass Criteria:** Scope-specific (see implementation guides)
- **If FAIL:** Fix issues, RESTART from smoke testing

**Scope-Specific Focus:**
- **Feature-level:** Unit tests, code structure, output files, interfaces, documentation
- **Epic-level:** Cross-feature integration, data flow, interface compatibility

---

## Round 2: [Scope-Specific - See Implementation Guides]

**Universal Pattern:**
- **Objective:** Deep verification
- **Time Estimate:** 10-20 minutes
- **Pass Criteria:**
  - ALL Round 1 issues resolved (none remaining)
  - ZERO new critical issues found
- **If FAIL:** Fix issues, RESTART from smoke testing

**Scope-Specific Focus:**
- **Feature-level:** Baseline comparison, data validation, regression testing, semantic diff, edge cases
- **Epic-level:** Epic cohesion & consistency, code style, naming conventions, error handling patterns

**Critical:** Round 2 builds on Round 1. If Round 1 issues unresolved OR new critical issues appear, implementation is unstable → RESTART

---

## Round 3: [Scope-Specific - See Implementation Guides]

**Universal Pattern:**
- **Objective:** Final skeptical review with ZERO tolerance
- **Time Estimate:** 10-20 minutes
- **Pass Criteria:**
  - **ZERO issues found** (critical, medium, OR minor)
  - Spec re-read confirms 100% implementation
  - Fresh-eyes review finds no gaps
- **If FAIL:** Fix issues, RESTART from smoke testing

**Scope-Specific Focus:**
- **Feature-level:** Fresh-eyes spec review, algorithm traceability re-check, integration gap re-check
- **Epic-level:** End-to-end success criteria, original epic request validation, user experience flows

**Critical:** Round 3 is ZERO TOLERANCE checkpoint
- ANY issue found → RESTART
- "Minor" issues are still issues → RESTART
- This is final chance to catch problems
- Production readiness gate

---

## Common Validation Patterns

### Pattern 1: Data Quality Checks

**Check data VALUES, not just structure:**

```python
# For ALL data files/outputs:
1. File exists? ✓
2. File has correct structure (columns/fields)? ✓
3. File has data (not empty)? ✓
4. Data values are correct type? ✓
5. Data values in expected range? ✓
6. Data values not placeholder/zero/null? ✓
7. Data values match spec requirements? ✓
```

### Pattern 2: Algorithm Verification

**Verify implementation matches spec:**

```markdown
1. Read algorithm description in spec
2. Find implementation in code (use Algorithm Traceability Matrix)
3. Trace through implementation step-by-step
4. Verify each step matches spec
5. Test with sample data
6. Verify output matches expected result from spec
```

### Pattern 3: Edge Case Validation

**Test boundary conditions:**

```python
# For each algorithm/method:
- Empty input ([], {}, "", None)
- Single item input
- Maximum expected input
- Invalid input (if applicable)
- Boundary values (0, 1, MAX, MIN)
```

### Pattern 4: Integration Point Validation

**Verify interfaces between components:**

```python
# For each integration point:
1. Verify caller sends correct data format
2. Verify callee receives data correctly
3. Verify processing is correct
4. Verify return value format is correct
5. Verify caller handles return value correctly
6. Verify error handling at boundary
```

---

## Common Mistakes to Avoid

### ❌ Mistake 1: Skipping Rounds

```markdown
# WRONG - "Round 1 looks good, I'll skip to Round 3"
# Each round has unique focus - cannot skip

# CORRECT - Complete ALL 3 rounds in order
Round 1 → Round 2 → Round 3
```

### ❌ Mistake 2: Partial Re-run After Failure

```markdown
# WRONG - Fix Round 2 issues, continue to Round 3
# (skipping smoke testing and Round 1)

# CORRECT - Fix issues, RESTART from smoke testing
Smoke Testing → Round 1 → Round 2 → Round 3
```

### ❌ Mistake 3: Accepting "90% Done"

```markdown
# WRONG - "Feature is 90% complete, we can finish the last 10% later"
# Zero tech debt tolerance - either DONE or NOT DONE

# CORRECT - Complete 100% or mark INCOMPLETE and restart
100% complete = PASS
< 100% complete = INCOMPLETE = RESTART
```

### ❌ Mistake 4: Confirming Spec Without Re-Reading

```markdown
# WRONG - "I remember the spec, no need to re-read"
# Confirmation bias leads to missed requirements

# CORRECT - Close spec, re-read with fresh eyes in Round 3
Close spec → Wait 1 minute → Re-read independently
```

### ❌ Mistake 5: Structure-Only Validation

```python
# WRONG - Only checking structure
assert 'projected_points' in df.columns  # Just checks column exists

# CORRECT - Checking structure AND values
assert 'projected_points' in df.columns  # Structure
assert df['projected_points'].notna().all()  # Values not null
assert df['projected_points'].sum() > 0  # Values not zero
assert df['projected_points'].between(0, 500).all()  # Values in range
```

---

## Restart Decision Tree

```bash
Did QC round find issues?
├─ NO ISSUES
│  └─ If Round 1 or 2: Proceed to next round
│  └─ If Round 3: QC complete, proceed to next stage
│
└─ ISSUES FOUND
   ├─ Are issues CRITICAL?
   │  ├─ YES (integration fails, requirements not met, data incorrect)
   │  │  └─ RESTART from smoke testing
   │  │
   │  └─ NO (minor cosmetic, naming inconsistency)
   │     ├─ Feature-level: Still RESTART (zero tolerance)
   │     └─ Epic-level: Fix immediately IF Round 1/2, RESTART IF Round 3
   │
   └─ Special case: Round 3
      └─ ANY issues (critical OR minor) → RESTART
```

---

## Scope-Specific Differences

### Feature-Level Validation Loop (S7.P2)

**11 Dimensions Checked EVERY Round:**
1. Content Accuracy - Requirements met
2. References - All links valid
3. Workflow Integration - Fits into overall workflow
4. Template Compliance - Follows templates
5. Cross-Feature Integration - Works with other features
6. Data Validation - Values correct (not just structure)
7. Error Handling - All errors caught and handled
8. Edge Cases - Boundary conditions handled
9. Algorithm Correctness - Logic matches spec
10. Regression Testing - Old functionality still works
11. Spec Alignment - Implementation matches spec

**If issues found:** Fix immediately, reset counter, continue

---

### Epic-Level Validation Loop (S9.P2)

**12 Dimensions Checked EVERY Round (7 master + 5 epic-specific):**

Master Dimensions (1-7):
1. Content Accuracy
2. References
3. Workflow Integration
4. Template Compliance
5. Cross-Feature Integration
6. Data Validation
7. Error Handling

Epic-Specific Dimensions (8-12):
8. Cross-Feature Integration Points
9. Data Flow Validation
10. Epic Cohesion & Consistency
11. Error Propagation
12. End-to-End Success Criteria

**If issues found:** Fix immediately, reset counter, continue

---

## Summary

**Key Principles:**
1. Check ALL dimensions every round (not different focuses)
2. Zero tech debt tolerance (fix issues immediately)
3. Fix-and-continue approach (no restart needed)
4. Verify DATA VALUES (not just structure)
5. Exit after 3 consecutive clean rounds
6. Re-reading checkpoints mandatory
7. Zero tolerance for deferred issues

**Purpose:**
- Comprehensive validation
- Catch issues smoke testing missed
- Ensure production readiness
- Zero tech debt deployment

**Remember:** Validation Loop ensures quality through systematic dimension checking. NEVER defer issues. NEVER skip dimensions. Fix immediately and continue.

---

*For actual implementation guides, see:*
- Feature-level: `stages/s7/s7_p2_qc_rounds.md`
- Epic-level: `stages/s9/s9_p2_epic_qc_rounds.md`
