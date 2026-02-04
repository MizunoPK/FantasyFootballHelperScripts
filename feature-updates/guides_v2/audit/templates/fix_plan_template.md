# Fix Plan - Round [N]

**Date:** YYYY-MM-DD
**Round:** [Number]
**Total Issues:** [N] (from Discovery Report)
**Total Groups:** [N] groups

---

## Executive Summary

**Issues by Priority:**
- P0 (Critical): [N] issues in [N] groups
- P1 (High): [N] issues in [N] groups
- P2 (Medium): [N] issues in [N] groups
- P3 (Low): [N] issues in [N] groups

**Fix Strategy:**
- Automated: [N] groups ([N] issues)
- Manual: [N] groups ([N] issues)
- User Decision: [N] groups ([N] issues)

**Estimated Duration:** [XX] minutes

---

## Fix Groups

### Group 1: [Description] (P0 - Critical)

**Pattern:** `OLD_PATTERN` → `NEW_PATTERN`
**Dimension:** D# - [Dimension Name]
**Issue Count:** [N] instances
**Files Affected:** [N] files

**Files:**
- path/to/file1.md (lines: 45, 67, 89)
- path/to/file2.md (lines: 123, 156)
- path/to/file3.md (lines: 234)

**Fix Strategy:** Automated (sed)

**Sed Command:**
```bash
# Apply fix
sed -i 's|OLD_PATTERN|NEW_PATTERN|g' \
  path/to/file1.md \
  path/to/file2.md \
  path/to/file3.md
```

**Verification Command:**
```bash
# Verify new pattern exists
grep -n "NEW_PATTERN" path/to/file1.md path/to/file2.md path/to/file3.md

# Verify old pattern gone (should return 0)
grep -n "OLD_PATTERN" path/to/file1.md path/to/file2.md path/to/file3.md | wc -l
```

**Expected Before:**
```
file1.md:45:stages/s5/round1/planning.md
file1.md:67:stages/s5/round1/algorithms.md
```

**Expected After:**
```
file1.md:45:stages/s5/s5_p1_planning_round1.md
file1.md:67:stages/s5/s5_p1_i2_algorithms.md
```

---

### Group 2: [Description] (P0 - Critical)

[Repeat template for each group]

**Pattern:** `OLD` → `NEW`
**Dimension:** D#
**Issue Count:** [N]
**Files Affected:** [N]

[Continue with sed command, verification, etc.]

---

### Group 3: [Description] (P1 - High)

[Continue for all P1 groups]

---

### Group 4: [Description] (P2 - Medium)

[Continue for all P2 groups]

---

### Group 5: [Description] (P3 - Low)

[Continue for all P3 groups OR mark as deferred]

**Note:** P3 issues may be deferred if time-constrained. Document reason for deferral.

---

## Manual Fix Cases

### Manual Fix #1: [Description]

**File:** path/to/file.md
**Line:** [approximate]
**Issue:** [Description of what needs manual intervention]
**Reason for Manual:** [Context-sensitive / Adding content / Complex / User decision]

**Analysis:**
[What needs to be checked, what the context is]

**Options:**
1. **Option A:** [Description]
   - Pros: [Benefits]
   - Cons: [Drawbacks]

2. **Option B:** [Description]
   - Pros: [Benefits]
   - Cons: [Drawbacks]

**Recommendation:** [Chosen option with rationale]

**Action Plan:**
```markdown
1. Read file context (lines X-Y)
2. Determine correct fix based on [criteria]
3. Use Edit tool with:
   - old_string: [exact old content]
   - new_string: [exact new content]
4. Verify by reading changed section
5. Document before/after
```

---

### Manual Fix #2: [Description]

[Repeat for each manual fix]

---

## Execution Order

**Execute in this order (do NOT batch):**

```
PRIORITY 0 (Critical) - Fix Immediately
  ├─> Group 1: [Description] (Automated)
  ├─> Group 2: [Description] (Automated)
  └─> Group 3: [Description] (Manual)
      ↓
VERIFY P0 fixes before continuing
      ↓
PRIORITY 1 (High) - Fix in Same Session
  ├─> Group 4: [Description] (Automated)
  ├─> Group 5: [Description] (Automated)
  └─> Group 6: [Description] (Manual)
      ↓
VERIFY P1 fixes before continuing
      ↓
PRIORITY 2 (Medium) - Fix Soon
  ├─> Group 7: [Description] (Automated)
  └─> Group 8: [Description] (Manual)
      ↓
VERIFY P2 fixes before continuing
      ↓
PRIORITY 3 (Low) - Fix When Time Allows OR Defer
  ├─> Group 9: [Description] (Automated)
  └─> Group 10: [Description] (Manual OR Deferred)
      ↓
VERIFY P3 fixes OR document deferral
```

**Critical Rule:** Fix → Verify → Document before moving to next group

---

## Verification Checkpoints

### After P0 Groups

- [ ] All P0 groups applied
- [ ] All P0 verifications passed
- [ ] Before/after documented for each
- [ ] Git diff reviewed for sanity
- [ ] No critical issues remain
- [ ] Ready to proceed to P1

### After P1 Groups

- [ ] All P1 groups applied
- [ ] All P1 verifications passed
- [ ] Before/after documented for each
- [ ] Git diff reviewed
- [ ] No high-priority issues remain
- [ ] Ready to proceed to P2

### After P2 Groups

- [ ] All P2 groups applied
- [ ] All P2 verifications passed
- [ ] Before/after documented for each
- [ ] Git diff reviewed
- [ ] No medium-priority issues remain
- [ ] Ready to proceed to P3 OR Stage 4

### After P3 Groups (Optional)

- [ ] All P3 groups applied OR deferred (documented)
- [ ] Verifications passed if applied
- [ ] Deferral rationale documented if deferred
- [ ] Git diff reviewed
- [ ] Ready to proceed to Stage 4

---

## Deferred Issues (If Any)

**Only defer P3 (Low priority) issues if time-constrained.**

### Deferred Issue #1

**Group:** [Group number and description]
**Priority:** P3 (Low)
**Issue Count:** [N]
**Reason for Deferral:** [Time constraint / Low impact / User decision pending]
**Plan:** [When/how to address later]
**Tracked In:** [Issue tracker, TODO, etc.]

---

## Estimated Timeline

**Per-Group Estimates:**

| Group | Priority | Type | Estimated Time |
|-------|----------|------|----------------|
| 1 | P0 | Automated | 5 min |
| 2 | P0 | Automated | 5 min |
| 3 | P0 | Manual | 15 min |
| 4 | P1 | Automated | 5 min |
| 5 | P1 | Automated | 5 min |
| 6 | P1 | Manual | 10 min |
| 7 | P2 | Automated | 5 min |
| 8 | P2 | Manual | 10 min |
| 9 | P3 | Automated | 3 min |
| 10 | P3 | Deferred | 0 min |
| **TOTAL** | | | **63 min** |

**Add 20-30% buffer:** [75-80] minutes total

---

## Special Considerations

### Context-Sensitive Replacements

**Groups requiring context analysis before fixing:**
- Group [N]: [Description] - Some instances intentional (historical examples)

**Approach:**
1. Review each match individually
2. Read 5 lines of context
3. Determine: Error or intentional?
4. If error: Fix
5. If intentional: Document and skip

### Breaking Changes

**Groups that may have downstream effects:**
- Group [N]: [Description] - May require updating cross-references

**Mitigation:**
1. Fix primary issue first
2. Search for references to changed content
3. Update references in same commit
4. Verify no broken links remain

### Template Updates

**Groups affecting templates:**
- Group [N]: [Description] - Update [template_name.md]

**Extra Verification:**
1. Fix template
2. Check if any epics created from old template
3. Update those epics too (if applicable)
4. Document in commit message

---

## Rollback Plan

**If verification fails for any group:**

```bash
# Rollback the specific group
git restore file1.md file2.md file3.md

# Analyze why verification failed
# - Wrong pattern?
# - Missed edge case?
# - Context-sensitive issue?

# Refine pattern/approach
# Retry
```

**If multiple groups fail:**
```bash
# Rollback all changes to last clean state
git reset --hard HEAD

# Re-analyze fix plan
# Start over with refined approach
```

---

## Success Criteria

**Fix Plan execution is complete when:**

- [ ] All P0 groups fixed and verified
- [ ] All P1 groups fixed and verified
- [ ] All P2 groups fixed and verified
- [ ] All P3 groups fixed OR deferred (documented)
- [ ] Manual fixes completed
- [ ] All verifications passed
- [ ] Before/after documented for each group
- [ ] Git diff reviewed
- [ ] No verification failures
- [ ] Ready for Stage 4 (Comprehensive Verification)

---

## Notes

**Add any additional context, concerns, or observations here:**

- [Note 1]
- [Note 2]

---

**Status:** Ready to execute (Stage 3)
**Next Stage:** stages/stage_3_apply_fixes.md
