# Fix Plan - Round 3

**Date:** 2026-02-04
**Round:** 3
**Total Issues:** 8
**Fix Groups:** 2 groups (both manual)
**Estimated Duration:** 20-30 minutes

---

## Execution Order Summary

| Priority | Group | Type | Count | Duration |
|----------|-------|------|-------|----------|
| P1 | Group 1: Glossary format fixes | Manual | 5 | 15-20 min |
| P1 | Group 2: Round 3 table fixes | Manual | 3 | 5-10 min |

**Total:** 20-30 minutes (all manual edits)

**Why All Manual:**
- Format changes need context preservation (can't use sed for "+ Gate" → "includes" rewrites)
- Table edits require maintaining markdown alignment
- Multi-line context-sensitive changes

---

## Group 1: Glossary Format Fixes (P1, Manual)

**Pattern:** Inconsistent format for describing round structure, wrong counts

**All issues in:** `reference/glossary.md`

### Issue R3-1: glossary.md:683 - Round 1 count and format

**File:** `reference/glossary.md`
**Line:** 683

**Current:**
```markdown
- **Round 1:** Iterations 1-7 + Gate 4a + Gate 7a (9 iterations)
```

**Target:**
```markdown
- **Round 1:** Iterations 1-7 (7 iterations, includes Gates 4a, 7a)
```

**Changes:**
- Remove "+ Gate 4a + Gate 7a" format
- Change "(9 iterations)" → "(7 iterations, includes Gates 4a, 7a)"

---

### Issue R3-2: glossary.md:684 - Round 2 count

**File:** `reference/glossary.md`
**Line:** 684

**Current:**
```markdown
- **Round 2:** Iterations 8-13 (9 iterations)
```

**Target:**
```markdown
- **Round 2:** Iterations 8-13 (6 iterations)
```

**Changes:**
- Change "(9 iterations)" → "(6 iterations)"

---

### Issue R3-3: glossary.md:1075 - Round 1 format

**File:** `reference/glossary.md`
**Line:** 1075

**Current:**
```markdown
- Round 1: Iterations 1-7 + Gate 4a (Initial TODO)
```

**Target:**
```markdown
- Round 1: Iterations 1-7 (7 iterations, includes Gate 4a) - Initial TODO
```

**Changes:**
- Remove "+ Gate 4a" format
- Add "(7 iterations, includes Gate 4a)" after range
- Keep "(Initial TODO)" descriptor

---

### Issue R3-4: glossary.md:1077 - Round 3 range

**File:** `reference/glossary.md`
**Line:** 1077

**Current:**
```markdown
- Round 3: Iterations 17-24 (Preparation + Gates)
```

**Target:**
```markdown
- Round 3: Iterations 14-22 (9 iterations, includes Gates 23a=I20, 25=I21, 24=I22) - Preparation + Gates
```

**Changes:**
- Change range "17-24" → "14-22"
- Add "(9 iterations, includes Gates 23a=I20, 25=I21, 24=I22)"
- Keep "(Preparation + Gates)" descriptor

---

### Issue R3-5: faq_troubleshooting.md:42 - Round 1 format

**File:** `reference/faq_troubleshooting.md`
**Line:** 42

**Current:**
```markdown
- **Iteration:** Single verification step (Round 1 has Iterations 1-7 + Gate 4a)
```

**Target:**
```markdown
- **Iteration:** Single verification step (Round 1 has 7 iterations: I1-I7, includes Gates 4a, 7a)
```

**Changes:**
- Remove "+ Gate 4a" format
- Add "7 iterations: I1-I7, includes Gates 4a, 7a"
- Add missing Gate 7a reference

---

## Group 2: Round 3 Table Fixes (P1, Manual)

**Pattern:** Table in s5_p3_planning_round3.md has old iteration numbers (pre-renumbering)

**File:** `stages/s5/s5_p3_planning_round3.md`

**Context:** Table shows Round 3 parts with iteration ranges

### Issue R3-6: s5_p3_planning_round3.md:58 - Preparation range

**File:** `stages/s5/s5_p3_planning_round3.md`
**Line:** 58

**Current:**
```markdown
| S5.P3.1: Preparation | `stages/s5/s5_p3_i1_preparation.md` | 14-19 | 45-60 min |
```

**Target:**
```markdown
| S5.P3.1: Preparation | `stages/s5/s5_p3_i1_preparation.md` | 14-19 | 45-60 min |
```

**Changes:**
- Change iterations "14-19" → "14-19"
- Maintain table alignment

---

### Issue R3-7: s5_p3_planning_round3.md:59 - Gate 23a iteration

**File:** `stages/s5/s5_p3_planning_round3.md`
**Line:** 59

**Current:**
```markdown
| S5.P3.2: Gates 1-2 | `stages/s5/s5_p3_i2_gates_part1.md` | 23, 23a + Gate 23a | 30-45 min |
```

**Target:**
```markdown
| S5.P3.2: Gate 23a | `stages/s5/s5_p3_i2_gates_part1.md` | 20 (Gate 23a) | 30-45 min |
```

**Changes:**
- Change part name "Gates 1-2" → "Gate 23a"
- Change iterations "23, 23a + Gate 23a" → "20 (Gate 23a)"
- Maintain table alignment

---

### Issue R3-8: s5_p3_planning_round3.md:60 - Gates 24, 25 iterations

**File:** `stages/s5/s5_p3_planning_round3.md`
**Line:** 60

**Current:**
```markdown
| S5.P3.3: Gate 3 | `stages/s5/s5_p3_i3_gates_part2.md` | 24, 25 + Gates 24, 25 | 15-30 min |
```

**Target:**
```markdown
| S5.P3.3: Gates 24, 25 | `stages/s5/s5_p3_i3_gates_part2.md` | 21, 22 (Gates 25, 24) | 15-30 min |
```

**Changes:**
- Change part name "Gate 3" → "Gates 24, 25"
- Change iterations "24, 25 + Gates 24, 25" → "21, 22 (Gates 25, 24)"
- Note: Gate 25 = I21, Gate 24 = I22 (order matters)
- Maintain table alignment

---

### Related Issue: s5_p3_i3_gates_part2.md:4 - Header iteration numbers

**File:** `stages/s5/s5_p3_i3_gates_part2.md`
**Line:** 4

**Current:**
```markdown
#### Step 5.1.3.3: Part 2b (Iterations 24, 25 + Gates 24, 25)
```

**Target:**
```markdown
#### Step 5.1.3.3: Part 2b (Iterations 21, 22: Gates 25, 24)
```

**Changes:**
- Change "Iterations 24, 25" → "Iterations 21, 22"
- Change format "+ Gates 24, 25" → ": Gates 25, 24"
- Clarify that I21 = Gate 25, I22 = Gate 24

---

## Execution Steps

### Step 1: Group 1 - Glossary Fixes

**File:** `reference/glossary.md`

Use Edit tool for each line:

```markdown
# Issue R3-1 (Line 683):
OLD: - **Round 1:** Iterations 1-7 + Gate 4a + Gate 7a (9 iterations)
NEW: - **Round 1:** Iterations 1-7 (7 iterations, includes Gates 4a, 7a)

# Issue R3-2 (Line 684):
OLD: - **Round 2:** Iterations 8-13 (9 iterations)
NEW: - **Round 2:** Iterations 8-13 (6 iterations)

# Issue R3-3 (Line 1075):
OLD: - Round 1: Iterations 1-7 + Gate 4a (Initial TODO)
NEW: - Round 1: Iterations 1-7 (7 iterations, includes Gate 4a) - Initial TODO

# Issue R3-4 (Line 1077):
OLD: - Round 3: Iterations 17-24 (Preparation + Gates)
NEW: - Round 3: Iterations 14-22 (9 iterations, includes Gates 23a=I20, 25=I21, 24=I22) - Preparation + Gates
```

---

### Step 2: FAQ Troubleshooting Fix

**File:** `reference/faq_troubleshooting.md`

Use Edit tool:

```markdown
# Issue R3-5 (Line 42):
OLD: - **Iteration:** Single verification step (Round 1 has Iterations 1-7 + Gate 4a)
NEW: - **Iteration:** Single verification step (Round 1 has 7 iterations: I1-I7, includes Gates 4a, 7a)
```

---

### Step 3: Group 2 - Round 3 Planning Table

**File:** `stages/s5/s5_p3_planning_round3.md`

**Strategy:** Read lines 56-62 (full table), then use Edit tool to replace entire table section

**Current Table (Lines 56-60):**
```markdown
| Part | Guide to Read | Iterations | Time Estimate |
|------|---------------|------------|---------------|
| S5.P3.1: Preparation | `stages/s5/s5_p3_i1_preparation.md` | 14-19 | 45-60 min |
| S5.P3.2: Gates 1-2 | `stages/s5/s5_p3_i2_gates_part1.md` | 23, 23a + Gate 23a | 30-45 min |
| S5.P3.3: Gate 3 | `stages/s5/s5_p3_i3_gates_part2.md` | 24, 25 + Gates 24, 25 | 15-30 min |
```

**Target Table:**
```markdown
| Part | Guide to Read | Iterations | Time Estimate |
|------|---------------|------------|---------------|
| S5.P3.1: Preparation | `stages/s5/s5_p3_i1_preparation.md` | 14-19 | 45-60 min |
| S5.P3.2: Gate 23a | `stages/s5/s5_p3_i2_gates_part1.md` | 20 (Gate 23a) | 30-45 min |
| S5.P3.3: Gates 24, 25 | `stages/s5/s5_p3_i3_gates_part2.md` | 21, 22 (Gates 25, 24) | 15-30 min |
```

---

### Step 4: Gate Header Fix

**File:** `stages/s5/s5_p3_i3_gates_part2.md`

Use Edit tool:

```markdown
# Line 4:
OLD: #### Step 5.1.3.3: Part 2b (Iterations 24, 25 + Gates 24, 25)
NEW: #### Step 5.1.3.3: Part 2b (Iterations 21, 22: Gates 25, 24)
```

---

## Verification Commands

After all fixes applied:

```bash
# Verify glossary lines fixed
grep -n "Round 1:.*Iterations 1-7\|Round 2:.*Iterations 8-13\|Round 3:.*Iterations" reference/glossary.md

# Expected output (should show corrected format):
# 683:- **Round 1:** Iterations 1-7 (7 iterations, includes Gates 4a, 7a)
# 684:- **Round 2:** Iterations 8-13 (6 iterations)
# 685:- **Round 3:** Iterations 14-22 (9 iterations, includes Gates 23a=I20, 25=I21, 24=I22)
# 1075:- Round 1: Iterations 1-7 (7 iterations, includes Gate 4a) - Initial TODO
# 1077:- Round 3: Iterations 14-22 (9 iterations, includes Gates 23a=I20, 25=I21, 24=I22) - Preparation + Gates

# Verify no "+ Gate" format remains in problematic contexts
grep -n "+ Gate" reference/glossary.md reference/faq_troubleshooting.md | grep "Round 1\|Round 3"
# Expected: 0 results

# Verify table updated
grep -A 3 "S5.P3.1: Preparation" stages/s5/s5_p3_planning_round3.md
# Expected: Shows "14-19" not "14-19"

# Verify old iteration numbers gone from table
grep -n "23, 23a\|24, 25" stages/s5/s5_p3_planning_round3.md
# Expected: 0 results

# Verify gate header fixed
grep -n "Iterations 24, 25\|Iterations 21, 22" stages/s5/s5_p3_i3_gates_part2.md
# Expected: Should show "21, 22" not "24, 25"
```

---

## Files Modified Summary

| File | Issues | Type |
|------|--------|------|
| `reference/glossary.md` | 4 | Format + count + range |
| `reference/faq_troubleshooting.md` | 1 | Format |
| `stages/s5/s5_p3_planning_round3.md` | 3 | Table entries |
| `stages/s5/s5_p3_i3_gates_part2.md` | 1 (related) | Header |

**Total Files:** 4
**Total Issues:** 8 (+ 1 related)

---

## Exit Criteria

- [x] All issues grouped by pattern
- [x] Groups prioritized by severity
- [x] Manual edit locations identified with exact line numbers
- [x] Target format specified for each issue
- [x] Fix order documented
- [x] Verification commands provided
- [x] Ready for Stage 3 (Apply Fixes)

---

**Next Stage:** `stages/stage_3_apply_fixes.md` (Round 3)
