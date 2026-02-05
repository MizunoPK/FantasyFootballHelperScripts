# Fix Plan - Round 5 (Final Round)

**Date:** 2026-02-04
**Round:** 5
**Total Issues:** 3 (2 content + 1 file size policy)
**Fix Groups:** 2 groups
**Estimated Duration:** 5-10 minutes (content fixes), CLAUDE.md reduction deferred

---

## Execution Order Summary

| Priority | Group | Type | Count | Duration |
|----------|-------|------|-------|----------|
| P1 | Group 1: Progress fractions | Manual | 2 | 5 min |
| P2 | Group 2: CLAUDE.md file size | Deferred | 1 | (separate task) |

**Total Immediate:** 5 minutes (content fixes only)
**Deferred:** CLAUDE.md reduction (30-45 min, separate from iteration count audit)

---

## Group 1: Progress Fraction Corrections (P1, Manual)

**Pattern:** Wrong progress fractions for Round 1 (8/8 → 7/7)

**All issues in:** `prompts/s5_s8_prompts.md`

### Issue R5-1: s5_s8_prompts.md:81 - Progress fraction

**File:** `prompts/s5_s8_prompts.md`
**Line:** 81

**Current:**
```markdown
**User says:** Agent detects Round 1 complete (8/8 iterations done, confidence >= MEDIUM)
```text

**Target:**
```markdown
**User says:** Agent detects Round 1 complete (7/7 iterations done, confidence >= MEDIUM)
```markdown

**Change:**
- "8/8 iterations done" → "7/7 iterations done"

---

### Issue R5-2: s5_s8_prompts.md:111 - Progress fraction

**File:** `prompts/s5_s8_prompts.md`
**Line:** 111

**Current:**
```markdown
✅ Round 1 complete (8/8 iterations)
```text

**Target:**
```markdown
✅ Round 1 complete (7/7 iterations)
```markdown

**Change:**
- "8/8 iterations" → "7/7 iterations"

---

## Group 2: CLAUDE.md File Size Reduction (P2, Deferred)

**Issue:** CLAUDE.md exceeds 40,000 character policy limit

**Current State:**
- Size: 45,786 characters (1,011 lines)
- Limit: 40,000 characters
- Overage: 5,786 characters (14.5% over)

**Why Deferring:**
1. **Different scope:** File size reduction is architectural/organizational, not iteration count correction
2. **Strategic decision needed:** Requires analysis of what content to extract and where
3. **Audit focus:** Current audit focused on iteration count accuracy (28 → 22 renumbering)
4. **Separate tracking:** Should be tracked as standalone improvement task

**Recommended Approach (for separate task):**
1. **Analyze CLAUDE.md sections** by size and necessity
2. **Extract candidates** (~6,000 characters needed):
   - Stage Workflows Quick Reference (~2,000) → reference EPIC_WORKFLOW_USAGE.md
   - S2 Parallel Work details (~1,500) → reference parallel_work/README.md
   - Common Anti-Patterns examples (~1,000) → reference common_mistakes.md
   - Protocol details (~2,000) → reference respective protocol files
3. **Maintain critical content** in CLAUDE.md:
   - Quick Start section
   - Phase Transition Protocol (essential)
   - Critical Rules Summary
   - Git Safety Rules
   - Tool usage policy
4. **Replace extracted sections** with short references pointing to detailed guides
5. **Verify** CLAUDE.md ≤ 40,000 characters
6. **Test** that agents can still effectively use streamlined CLAUDE.md

**Status:** Documented in Round 5 discovery, recommend creating separate issue

---

## Execution Steps

### Step 1: Fix Progress Fractions

**File:** `prompts/s5_s8_prompts.md`

**Use Edit tool (Issue R5-1):**
```markdown
OLD: **User says:** Agent detects Round 1 complete (8/8 iterations done, confidence >= MEDIUM)
NEW: **User says:** Agent detects Round 1 complete (7/7 iterations done, confidence >= MEDIUM)
```text

**Use Edit tool (Issue R5-2):**
```markdown
OLD: ✅ Round 1 complete (8/8 iterations)
NEW: ✅ Round 1 complete (7/7 iterations)
```markdown

---

### Step 2: Document CLAUDE.md Issue

**Action:** Create note for follow-up task (not fixed in this audit)

**Recommendation for audit guides:**
Add file size check to automated pre-audit script:

**File:** `audit/scripts/pre_audit_checks.sh`

**Add after line ~20 (file size assessment section):**
```bash
echo ""
echo "${BLUE}=== Policy Compliance Check ===${NC}"
echo ""

# Check CLAUDE.md size
claude_md="../../CLAUDE.md"
if [ -f "$claude_md" ]; then
    claude_size=$(wc -c < "$claude_md")
    if [ $claude_size -gt 40000 ]; then
        echo "${RED}❌ POLICY VIOLATION:${NC} CLAUDE.md ($claude_size chars) exceeds 40,000 character limit"
        echo "   Overage: $((claude_size - 40000)) characters"
        echo "   Reason: Large files create barriers for agent comprehension"
        echo "   Action: Extract ~$((claude_size - 40000)) characters to separate files"
    else
        echo "${GREEN}✅ PASS:${NC} CLAUDE.md ($claude_size chars) within 40,000 character limit"
    fi
else
    echo "${YELLOW}⚠️  WARNING:${NC} CLAUDE.md not found at expected location"
fi
```markdown

---

## Verification Commands

After immediate fixes applied:

```bash
# Verify progress fractions fixed
grep -n "8/8 iterations" prompts/s5_s8_prompts.md
# Expected: 0 results

grep -n "7/7 iterations" prompts/s5_s8_prompts.md
# Expected: 2 results (lines 81, 111)

# Comprehensive check for any remaining wrong fractions
grep -rn "[89]/[89] iterations" --include="*.md" . | grep -v "_audit_output" | grep "Round 1"
# Expected: 0 results

# CLAUDE.md size check (deferred, for tracking)
wc -c ../../CLAUDE.md
# Current: 45786 (EXCEEDS 40000 by 5786)
# Target: ≤40000 (separate task to address)
```markdown

---

## Files Modified Summary

**Immediate fixes:**
| File | Issues | Type |
|------|--------|------|
| `prompts/s5_s8_prompts.md` | 2 | Progress fractions |

**Total Files (immediate):** 1
**Total Issues (immediate):** 2

**Deferred:**
| File | Issue | Type |
|------|-------|------|
| `CLAUDE.md` | 1 | File size policy |

---

## Exit Criteria

- [x] All content issues grouped by pattern
- [x] Groups prioritized by severity
- [x] Manual edit locations identified with exact line numbers
- [x] Target format specified for each issue
- [x] Fix order documented
- [x] Verification commands provided
- [x] CLAUDE.md issue documented for follow-up
- [x] Audit guide improvement identified (pre-audit check enhancement)
- [x] Ready for Stage 3 (Apply Fixes)

---

## Audit Guide Improvements Identified

### Improvement 1: Add File Size Policy Check to Pre-Audit Script

**File:** `audit/scripts/pre_audit_checks.sh`
**Enhancement:** Add CLAUDE.md character count check against 40,000 limit
**Benefit:** Proactively catch file size policy violations
**Implementation:** See Step 2 above for exact code

### Improvement 2: Document File Size Policy in Audit Overview

**File:** `audit/audit_overview.md`
**Enhancement:** Add section on file size considerations
**Content:**
```markdown
## File Size Considerations

**Rationale:** Large files create barriers for agent comprehension and may cause agents to miss critical instructions.

**Policy:**
- **CLAUDE.md:** Must not exceed 40,000 characters
- **Workflow guides:** Large files (>600 lines) should be evaluated for potential splitting

**Why This Matters:**
- Agents read CLAUDE.md at start of every task
- Overwhelming file size impacts agent effectiveness
- Large guides may be partially skipped or misunderstood

**When to Split Files:**
- File exceeds readability threshold (varies by file type)
- Content has natural subdivisions
- Agents report difficulty following guide
- File serves multiple distinct purposes
```

---

**Next Stage:** `stages/stage_3_apply_fixes.md` (Round 5)
