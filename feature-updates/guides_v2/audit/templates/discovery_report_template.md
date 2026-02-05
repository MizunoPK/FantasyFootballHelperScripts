# Discovery Report - Round [N]

**Date:** YYYY-MM-DD
**Round:** [Number]
**Duration:** [XX] minutes
**Patterns Used:** [Number] different pattern types
**Folders Checked:** [List folders]

---

## Summary

**Total Issues Found:** [N]

### By Dimension

| Dimension | Issues | Critical | High | Medium | Low |
|-----------|--------|----------|------|--------|-----|
| D1: Cross-Reference | 0 | 0 | 0 | 0 | 0 |
| D2: Terminology | 0 | 0 | 0 | 0 | 0 |
| D3: Workflow Integration | 0 | 0 | 0 | 0 | 0 |
| D4: Count Accuracy | 0 | 0 | 0 | 0 | 0 |
| D5: Content Completeness | 0 | 0 | 0 | 0 | 0 |
| D6: Template Currency | 0 | 0 | 0 | 0 | 0 |
| D7: Context-Sensitive | 0 | 0 | 0 | 0 | 0 |
| D8: CLAUDE.md Sync | 0 | 0 | 0 | 0 | 0 |
| D9: Intra-File Consistency | 0 | 0 | 0 | 0 | 0 |
| D10: File Size | 0 | 0 | 0 | 0 | 0 |
| D11: Structural Patterns | 0 | 0 | 0 | 0 | 0 |
| D12: Cross-File Dependencies | 0 | 0 | 0 | 0 | 0 |
| D13: Documentation Quality | 0 | 0 | 0 | 0 | 0 |
| D14: Content Accuracy | 0 | 0 | 0 | 0 | 0 |
| D15: Duplication | 0 | 0 | 0 | 0 | 0 |
| D16: Accessibility | 0 | 0 | 0 | 0 | 0 |
| **TOTAL** | **0** | **0** | **0** | **0** | **0** |

### By Severity

- **Critical:** [N] issues (blocks workflow)
- **High:** [N] issues (causes confusion)
- **Medium:** [N] issues (cosmetic but important)
- **Low:** [N] issues (nice-to-have)

---

## Patterns Used

Document all search patterns attempted this round:

### Pattern 1: [Description]
```bash
grep -rn "PATTERN" --include="*.md"
```
**Results:** [N] matches found
**Issues:** [N] are errors, [N] are intentional

### Pattern 2: [Description]
```bash
grep -rn "PATTERN" --include="*.md"
```
**Results:** [N] matches found
**Issues:** [N] are errors, [N] are intentional

[Continue for all patterns used]

---

## Issues by Dimension

### D1: Cross-Reference Accuracy ([N] issues)

#### Issue #1

**File:** path/to/file.md
**Line:** 123
**Severity:** Critical/High/Medium/Low

**Pattern That Found It:**
```bash
grep -rn "pattern" --include="*.md"
```

**Context (5 lines):**
```text
[Line 121]
[Line 122]
→ [Line 123 - ISSUE HERE]
[Line 124]
[Line 125]
```

**Current State:**
```text
old incorrect content here
```

**Should Be:**
```text
new correct content here
```

**Why This Is Wrong:**
File path points to non-existent file. After S6→S9 renumbering, this path was not updated.

**Fix Strategy:**
- [x] Automated sed replacement
- [ ] Manual edit required
- [ ] Requires user decision

**Sed Command:**
```bash
sed -i 's|old_path|new_path|g' path/to/file.md
```

---

#### Issue #2

[Repeat template for each issue]

---

### D2: Terminology Consistency ([N] issues)

[Repeat for each dimension with issues]

---

## Automated Pre-Check Results

```bash
$ bash scripts/pre_audit_checks.sh

=== File Size Assessment ===
Files >1000 lines: 2
Files 600-1000 lines: 5

=== Structure Validation ===
Missing Prerequisites: 3 files
Missing Exit Criteria: 2 files

=== Documentation Quality ===
TODOs remaining: 0
Placeholders found: 0

=== Content Accuracy ===
Count mismatches: 1

=== Accessibility ===
Large files missing TOC: 2
```

---

## Spot-Check Results

**Random files manually reviewed:** [N] files

### File 1: [path/to/file.md]
**Sections checked:** Lines 1-50, 100-150, 200-250
**Issues found:** [N]
- [Issue description]

### File 2: [path/to/file.md]
**Sections checked:** Lines 1-50, 100-150
**Issues found:** None

[Continue for all spot-checked files]

---

## Folders Checked

Document which folders were checked and in what order:

- [x] templates/
- [x] prompts/
- [x] reference/
- [x] stages/s1/
- [x] stages/s2/
- [x] stages/s3/
- [x] stages/s4/
- [x] stages/s5/
- [x] stages/s6/
- [x] stages/s7/
- [x] stages/s8/
- [x] stages/s9/
- [x] stages/s10/
- [x] debugging/
- [x] missed_requirement/
- [x] CLAUDE.md (root)
- [x] README.md
- [x] EPIC_WORKFLOW_USAGE.md

**Order:** [alphabetical / reverse / random / priority-based]

---

## New Discoveries This Round

**Issues found that previous rounds missed:**

### Discovery #1
**Pattern:** [What pattern finally found this]
**Why missed before:** [Reason - wrong pattern, wrong location, etc.]
**Issue:** [Description]

[Continue for all new discoveries]

---

## Intentional Cases Documented

**Pattern matches that are CORRECT (not errors):**

### Intentional #1
**File:** path/to/file.md
**Lines:** 45, 67, 89
**Pattern:** "old notation"
**Reason:** Historical example showing before/after comparison
**Acceptable:** Yes
**Verified by:** [Agent ID/name]

[Continue for all intentional cases]

---

## Confidence Assessment

### Self-Assessment Checklist

- [ ] Used at least 5 different pattern types
- [ ] Checked all critical files (templates, CLAUDE.md, prompts)
- [ ] Searched all folders systematically
- [ ] Performed spot-checks on 10+ random files
- [ ] Tried pattern variations (punctuation, context, case)
- [ ] Manually reviewed ambiguous matches
- [ ] Documented ALL findings (even if uncertain)
- [ ] No folders skipped due to assumptions

**Confidence Score:** [0-100]%

**Factors lowering confidence:**
- [List any concerns]

**Factors raising confidence:**
- [List supporting evidence]

---

## Next Steps

### If Zero Issues Found

**Proceed to Stage 5 (Loop Decision) IF:**
- [x] This is Round 3 or higher
- [x] Tried at least 5 different pattern types
- [x] Spot-checked 10+ files manually
- [x] No new discoveries compared to previous round
- [x] Confidence score ≥ 80%

**Otherwise:**
- Continue to Round [N+1] with fresh patterns

### If Issues Found

**Proceed to Stage 2 (Fix Planning):**
- Group issues by pattern
- Prioritize by severity
- Create fix plan
- Execute fixes
- Verify and loop back

---

## Time Breakdown

- Pattern generation: [XX] min
- Automated searches: [XX] min
- Manual spot-checks: [XX] min
- Documentation: [XX] min
- **Total:** [XX] min

---

**Status:** Discovery complete, ready for [Stage 2 Fix Planning / Stage 5 Loop Decision]

**Next Action:** [What to do next]
