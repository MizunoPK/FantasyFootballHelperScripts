# QC Rounds Pattern (Reference)

**Purpose:** Generic QC rounds workflow applicable to both feature-level (S5.P6) and epic-level (S6.P2) quality control.

**This is a REFERENCE PATTERN.** Actual guides:
- **Feature-level:** `stages/s5/s5_p6_qc_rounds.md`
- **Epic-level:** `stages/s6/s6_p2_epic_qc_rounds.md`

---

## What are QC Rounds?

**Definition:** QC Rounds are systematic quality control checks performed through 3 progressively deeper validation rounds to ensure correctness, completeness, and production readiness.

**Purpose:**
- Comprehensive validation beyond smoke testing
- Zero tech debt tolerance
- Mandatory restart if critical issues found
- Progressive validation (each round catches different issues)

**Scope-Specific Implementation:**
- **Feature-level (S5.P6):** Validates individual feature correctness and completeness
- **Epic-level (S6.P2):** Validates cross-feature integration and epic cohesion

---

## Common QC Rounds Structure

**All QC rounds follow this 3-round pattern:**

```
Round 1: [Scope-Specific Focus]
   ↓ Basic validation level
   ↓ Pass criteria: Defined per scope
   ↓
   If PASS → Round 2
   If FAIL → Fix issues, RESTART from smoke testing

Round 2: [Scope-Specific Focus]
   ↓ Deep verification level
   ↓ Pass criteria: All Round 1 issues resolved + zero new critical issues
   ↓
   If PASS → Round 3
   If FAIL → Fix issues, RESTART from smoke testing

Round 3: [Scope-Specific Focus]
   ↓ Final skeptical review
   ↓ Pass criteria: ZERO issues (zero tolerance)
   ↓
   If PASS → Complete, proceed to next stage
   If FAIL → Fix issues, RESTART from smoke testing
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

```
RESTART PROTOCOL:
1. Fix ALL issues found in failed round
2. Return to smoke testing (S5.P5 OR S6.P1)
3. Re-run ALL smoke test parts
4. Re-run ALL 3 QC rounds from Round 1

WHY complete restart?
- Fixes can introduce new issues in earlier parts
- Clean validation state required
- Ensures ALL validation passes consistently
```

**Restart Triggers:**
- **Round 1:** Fails acceptance criteria (scope-specific)
- **Round 2:** Any Round 1 issues unresolved OR new critical issues found
- **Round 3:** ANY issues found (zero tolerance)

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
- Re-check Algorithm Traceability Matrix from Stage 5a
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

```
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

### Feature-Level QC Rounds (S5.P6)

**Round 1 Focus:** Basic Validation
- Unit tests passing
- Code structure correct
- Output files exist and correct
- Interfaces match dependencies
- Documentation complete

**Round 2 Focus:** Deep Verification
- Baseline comparison (if updating existing feature)
- Data validation (values correct)
- Regression testing (old functionality still works)
- Semantic diff (behavior matches spec)
- Edge cases handled

**Round 3 Focus:** Final Skeptical Review
- Re-read spec with fresh eyes
- Re-check Algorithm Traceability Matrix
- Re-check Integration Gap Check
- Zero issues tolerance

**Restart Destination:** S5.P5 (Feature Smoke Testing)

---

### Epic-Level QC Rounds (S6.P2)

**Round 1 Focus:** Cross-Feature Integration
- Integration points work correctly
- Data flows between features
- Interface compatibility
- Error propagation handling

**Round 2 Focus:** Epic Cohesion & Consistency
- Code style consistency across features
- Naming convention consistency
- Error handling consistency
- Architectural pattern consistency

**Round 3 Focus:** End-to-End Success Criteria
- Validation against original epic request
- Epic success criteria met (from Stage 4)
- User experience flows validated
- Performance characteristics acceptable

**Restart Destination:** S6.P1 (Epic Smoke Testing)

---

## Summary

**Key Principles:**
1. All 3 rounds mandatory (no skipping)
2. Zero tech debt tolerance (100% or INCOMPLETE)
3. Restart from smoke testing if ANY round fails
4. Verify DATA VALUES (not just structure)
5. Each round has unique focus (cannot skip)
6. Re-reading checkpoints mandatory
7. Round 3 is zero tolerance (ANY issue → RESTART)

**Purpose:**
- Comprehensive validation
- Catch issues smoke testing missed
- Ensure production readiness
- Zero tech debt deployment

**Remember:** QC Rounds take 30-60 minutes but ensure quality. NEVER accept partial implementations. NEVER skip rounds. NEVER skip restart protocol.

---

*For actual implementation guides, see:*
- Feature-level: `stages/s5/s5_p6_qc_rounds.md`
- Epic-level: `stages/s6/s6_p2_epic_qc_rounds.md`
