# Validation Loop Pattern (Reference)

**Purpose:** Generic validation loop workflow applicable to both feature-level (S7.P2) and epic-level (S9.P2) quality control.

**This is a REFERENCE PATTERN.** Actual guides:
- **Feature-level:** `stages/s7/s7_p2_qc_rounds.md`
- **Epic-level:** `stages/s9/s9_p2_epic_qc_rounds.md`

---

## Table of Contents

1. [What is the Validation Loop?](#what-is-the-validation-loop)
2. [Validation Loop Structure](#validation-loop-structure)
3. [Universal Critical Rules](#universal-critical-rules)
4. [Round 1](#round-1-scope-specific---see-implementation-guides)
5. [Round 2](#round-2-scope-specific---see-implementation-guides)
6. [Round 3](#round-3-scope-specific---see-implementation-guides)
7. [Common Validation Patterns](#common-validation-patterns)
8. [Common Mistakes to Avoid](#common-mistakes-to-avoid)
9. [Issue Handling Decision Tree](#issue-handling-decision-tree)
10. [Scope-Specific Differences](#scope-specific-differences)
11. [Summary](#summary)

---

## What is the Validation Loop?

**Definition:** The Validation Loop is an iterative quality control process that checks ALL dimensions every round until 3 consecutive clean rounds are achieved.

**Purpose:**
- Comprehensive validation beyond smoke testing
- Zero tech debt tolerance
- Fix-and-continue approach (no restart needed)
- All dimensions checked every round (not different focuses per round)

**Scope-Specific Implementation:**
- **Feature-level (S7.P2):** 16 dimensions validated (7 master + 9 S7 QC-specific)
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

### 2. Fix-and-Continue Protocol (v2.0)

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
## ❌ NOT SUFFICIENT:
assert 'player_name' in df.columns  # Just checks column exists

## ✅ REQUIRED:
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
## Spec says: "Sort items by projected_value DESC"
## Implementation must use: df.sort_values('projected_value', ascending=False)
## NOT acceptable: Sorting by rank ASC (even if equivalent)
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
- **If issues found:** Fix immediately, reset clean counter to 0, continue to next round

**Scope-Specific Focus:**
- **Feature-level:** Unit tests, code structure, output files, interfaces, documentation
- **Epic-level:** Cross-feature integration, data flow, interface compatibility

---

## Round 2: [Scope-Specific - See Implementation Guides]

**Universal Pattern:**
- **Objective:** Deep verification
- **Time Estimate:** 10-20 minutes
- **Pass Criteria:**
  - ZERO issues found this round
  - All dimensions checked
- **If issues found:** Fix immediately, reset clean counter to 0, continue to next round

**Scope-Specific Focus:**
- **Feature-level:** Baseline comparison, data validation, regression testing, semantic diff, edge cases
- **Epic-level:** Epic cohesion & consistency, code style, naming conventions, error handling patterns

---

## Round 3: [Scope-Specific - See Implementation Guides]

**Universal Pattern:**
- **Objective:** Skeptical fresh-eyes review
- **Time Estimate:** 10-20 minutes
- **Pass Criteria:**
  - **ZERO issues found** (critical, medium, OR minor)
  - Spec re-read confirms 100% implementation
  - Fresh-eyes review finds no gaps
  - If clean: increment clean counter (need 3 consecutive clean rounds to exit)
- **If issues found:** Fix immediately, reset clean counter to 0, continue

**Scope-Specific Focus:**
- **Feature-level:** Fresh-eyes spec review, algorithm traceability re-check, integration gap re-check
- **Epic-level:** End-to-end success criteria, original epic request validation, user experience flows

**Exit Criteria:** 3 consecutive rounds with ZERO issues (not necessarily rounds 1-3; may require rounds 4, 5, 6+)

---

## Common Validation Patterns

### Pattern 1: Data Quality Checks

**Check data VALUES, not just structure:**

```python
## For ALL data files/outputs:
1. File exists? [x]
2. File has correct structure (columns/fields)? [x]
3. File has data (not empty)? [x]
4. Data values are correct type? [x]
5. Data values in expected range? [x]
6. Data values not placeholder/zero/null? [x]
7. Data values match spec requirements? [x]
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
## For each algorithm/method:
- Empty input ([], {}, "", None)
- Single item input
- Maximum expected input
- Invalid input (if applicable)
- Boundary values (0, 1, MAX, MIN)
```

### Pattern 4: Integration Point Validation

**Verify interfaces between components:**

```python
## For each integration point:
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
## WRONG - "Round 1 looks good, I'll skip to Round 3"
## Each round has unique focus - cannot skip

## CORRECT - Complete ALL 3 rounds in order
Round 1 → Round 2 → Round 3
```

### ❌ Mistake 2: Skipping Remaining Dimensions After Finding Issue

```markdown
## WRONG - Find issue in Dimension 3, stop checking other dimensions
## "I found a bug, I'll fix it and move on"

## CORRECT - Fix issue immediately, then complete ALL remaining dimensions
Fix D3 issue → reset clean counter → check D4...D12 → continue next round
```

### ❌ Mistake 3: Accepting "90% Done"

```markdown
## WRONG - "Feature is 90% complete, we can finish the last 10% later"
## Zero tech debt tolerance - either DONE or NOT DONE

## CORRECT - Complete 100% or mark INCOMPLETE and restart
100% complete = PASS
< 100% complete = INCOMPLETE = RESTART
```

### ❌ Mistake 4: Confirming Spec Without Re-Reading

```markdown
## WRONG - "I remember the spec, no need to re-read"
## Confirmation bias leads to missed requirements

## CORRECT - Close spec, re-read with fresh eyes in Round 3
Close spec → Wait 1 minute → Re-read independently
```

### ❌ Mistake 5: Structure-Only Validation

```python
## WRONG - Only checking structure
assert 'projected_value' in df.columns  # Just checks column exists

## CORRECT - Checking structure AND values
assert 'projected_value' in df.columns  # Structure
assert df['projected_value'].notna().all()  # Values not null
assert df['projected_value'].sum() > 0  # Values not zero
assert df['projected_value'].between(0, 500).all()  # Values in range
```

---

## Issue Handling Decision Tree

```bash
Did QC round find issues?
├─ NO ISSUES
│  └─ If clean count < 3: Proceed to next round
│  └─ If 3 consecutive clean rounds: QC complete, proceed to next stage
│
└─ ISSUES FOUND
   ├─ Fix ALL issues immediately (zero deferral tolerance)
   ├─ Reset consecutive clean counter to 0
   └─ Continue to next round (no restart needed)
      → Exit only after 3 consecutive clean rounds
      → Max 10 rounds (escalate to user if exceeded)
```

**Note:** S7.P2 uses fix-and-continue (not restart). Both critical and minor issues
are fixed immediately and validation continues. See `stages/s7/s7_p2_qc_rounds.md`
for the authoritative protocol.

---

## Scope-Specific Differences

### Feature-Level Validation Loop (S7.P2)

**16 Dimensions Checked EVERY Round (7 master + 9 S7 QC-specific):**

**See `reference/validation_loop_s7_feature_qc.md` for the authoritative dimension checklists.**

Master Dimensions (1-7):
1. Empirical Verification - All interfaces verified from source code
2. Completeness - All spec requirements implemented (100%)
3. Internal Consistency - No contradictions between implementation and spec
4. Traceability - Every function traces to spec requirement
5. Clarity & Specificity - No vague error messages or logging
6. Upstream Alignment - Implementation matches spec.md exactly
7. Standards Compliance - Follows project coding standards

S7 QC-Specific Dimensions (8-16):
8. Cross-Feature Integration - Integrates correctly with existing features
9. Error Handling Completeness - All error scenarios handled gracefully
10. End-to-End Functionality - E2E execution produces correct data values
11. Test Coverage Quality - Adequate test coverage with meaningful tests
12. Requirements Completion - 100% spec requirements verifiably implemented
13. Import & Dependency Hygiene - No circular imports, missing deps, or version conflicts
14. Cross-Layer & Type Consistency - Types match across all interface boundaries
15. Input Validation & Path Safety - All external inputs validated, no path traversal
16. Test Stub Consistency - Stubs match real interfaces, no silent mismatches

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
