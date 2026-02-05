# Fix Plan - Round 4

**Date:** 2026-02-04
**Round:** 4
**Total Issues:** 2
**Fix Groups:** 1 group (manual)
**Estimated Duration:** 5-10 minutes

---

## Execution Order Summary

| Priority | Group | Type | Count | Duration |
|----------|-------|------|-------|----------|
| P1 | Group 1: Count corrections | Manual | 2 | 5-10 min |

**Total:** 5-10 minutes (all manual edits)

**Why All Manual:**
- Issue R4-1: Inside markdown code block in example section
- Issue R4-2: Checklist item requiring context preservation
- Both need careful editing to preserve surrounding content

---

## Group 1: Count Corrections (P1, Manual)

**Pattern:** Wrong iteration counts in examples and checklists

### Issue R4-1: d8_claude_md_sync.md:571 - Example counts

**File:** `audit/dimensions/d8_claude_md_sync.md`
**Lines:** 569-572

**Current:**
```markdown
```markdown
CLAUDE.md: "S5: Implementation Planning (22 iterations)"
Guide: "S5: Implementation Planning (22 iterations across 3 rounds:
        Round 1 (7 iterations), Round 2 (9 iterations), Round 3 (12 iterations))"
```text
CLAUDE.md simplified but accurate ✅
```

**Target:**
```markdown
```markdown
CLAUDE.md: "S5: Implementation Planning (22 iterations)"
Guide: "S5: Implementation Planning (22 iterations across 3 rounds:
        Round 1 (7 iterations), Round 2 (6 iterations), Round 3 (9 iterations))"
```text
CLAUDE.md simplified but accurate ✅
```

**Changes:**
- Line 571: "Round 2 (9 iterations)" → "Round 2 (6 iterations)"
- Line 571: "Round 3 (12 iterations))" → "Round 3 (9 iterations))"

**Note:** This is inside a triple-backtick code block, need to preserve the nested markdown structure.

---

### Issue R4-2: mandatory_gates.md:435 - Total iteration count

**File:** `reference/mandatory_gates.md`
**Line:** 435

**Current:**
```markdown
- Iteration Completion: All 25 iterations complete
```text

**Target:**
```markdown
- Iteration Completion: All 22 iterations complete
```markdown

**Change:**
- "All 25 iterations complete" → "All 22 iterations complete"

---

## Execution Steps

### Step 1: Fix d8 Example

**File:** `audit/dimensions/d8_claude_md_sync.md`

**Read context first:**
```bash
# Read lines 567-574 to see full context
```text

**Use Edit tool:**
```markdown
OLD:
CLAUDE.md: "S5: Implementation Planning (22 iterations)"
Guide: "S5: Implementation Planning (22 iterations across 3 rounds:
        Round 1 (7 iterations), Round 2 (9 iterations), Round 3 (12 iterations))"

NEW:
CLAUDE.md: "S5: Implementation Planning (22 iterations)"
Guide: "S5: Implementation Planning (22 iterations across 3 rounds:
        Round 1 (7 iterations), Round 2 (6 iterations), Round 3 (9 iterations))"
```markdown

---

### Step 2: Fix Mandatory Gates Checklist

**File:** `reference/mandatory_gates.md`

**Use Edit tool:**
```markdown
OLD:
- Iteration Completion: All 25 iterations complete

NEW:
- Iteration Completion: All 22 iterations complete
```markdown

---

## Verification Commands

After all fixes applied:

```bash
# Verify d8 example fixed
grep -A 3 "Round 1 (7 iterations)" audit/dimensions/d8_claude_md_sync.md | grep "Round 2"
# Expected: Should show "Round 2 (6 iterations)"

# Verify mandatory gates fixed
grep -n "All.*iterations complete" reference/mandatory_gates.md
# Expected: Should show "All 22 iterations complete" (not 25)

# Comprehensive check for any remaining wrong counts
grep -rn "\b9 iterations.*Round 2\|\b12 iterations.*Round 3\|\b25 iterations" --include="*.md" . | grep -v "_audit_output" | grep -v "S5_UPDATE_NOTES"
# Expected: 0 results
```

---

## Files Modified Summary

| File | Issues | Type |
|------|--------|------|
| `audit/dimensions/d8_claude_md_sync.md` | 1 | Example counts (2 numbers changed) |
| `reference/mandatory_gates.md` | 1 | Checklist item |

**Total Files:** 2
**Total Issues:** 2

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

**Next Stage:** `stages/stage_3_apply_fixes.md` (Round 4)
