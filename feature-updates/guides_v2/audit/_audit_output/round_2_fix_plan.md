# Fix Plan - Round 2

**Date:** 2026-02-04
**Round:** 2
**Total Issues:** 30+
**Fix Groups:** 6 groups
**Estimated Duration:** 45-60 minutes

---

## Execution Order Summary

| Priority | Group | Type | Count | Duration |
|----------|-------|------|-------|----------|
| P1 | Group 1: Iteration ranges | Automated | 10+ | 10 min |
| P1 | Group 2: Round counts | Automated | 8+ | 5 min |
| P1 | Group 3: Gate iterations (I23a→I20) | Automated | 10+ | 10 min |
| P1 | Group 4: Gate iterations (I24→I22) | Automated | 8+ | 5 min |
| P1 | Group 5: Gate iterations (I25→I21) | Automated | 3+ | 3 min |
| P2 | Group 6: Manual spot-fixes | Manual | 3 | 5 min |

**Total:** 40-50 minutes

---

## Group 1: Fix Iteration Ranges (P1, Automated)

**Pattern:** Iteration ranges that changed with renumbering

### Sub-group 1a: I8-I13 → I8-I13

**Count:** 5+ instances
**Files:**
- `prompts/s5_s8_prompts.md:16`
- `README.md:336`
- `reference/glossary.md:684, 1076`

**Fix Command:**
```bash
find . -name "*.md" -type f ! -path "./_audit_output/*" ! -name "S5_UPDATE_NOTES.md" \
  -exec sed -i 's/Iterations 8-13/Iterations 8-13/g; s/I8-I13/I8-I13/g' {} +
```markdown

### Sub-group 1b: I14-I22 → I14-I22

**Count:** 5+ instances
**Files:**
- `README.md:337`
- `reference/glossary.md:685, 1077`

**Fix Command:**
```bash
find . -name "*.md" -type f ! -path "./_audit_output/*" ! -name "S5_UPDATE_NOTES.md" \
  -exec sed -i 's/Iterations 14-22/Iterations 14-22/g; s/I14-I22/I14-I22/g' {} +
```markdown

### Sub-group 1c: "1-7 + Gate" → "1-7 (7 iterations, includes Gates"

**Count:** 2 instances (glossary.md)
**File:** `reference/glossary.md:683`

**Manual Fix (context-sensitive):**
```diff
- Round 1: Iterations 1-7 + Gate 4a + Gate 7a (9 iterations)
+ Round 1: Iterations 1-7 (7 iterations, includes Gates 4a, 7a)
```markdown

---

## Group 2: Fix Round Iteration Counts (P1, Automated)

**Pattern:** Round count descriptions

### Sub-group 2a: "9 iterations" for Round 2

**Count:** 5+ instances
**Files:**
- `EPIC_WORKFLOW_USAGE.md:383`
- `prompts/s5_s8_prompts.md:91`
- `reference/glossary.md:684`

**Fix Command:**
```bash
# Context-aware: Only Round 2 references
find . -name "*.md" -type f ! -path "./_audit_output/*" ! -name "S5_UPDATE_NOTES.md" \
  -exec sed -i 's/Round 2:.*9 iteration/Round 2: Deep verification (6 iterations/g' {} +

# Safer version (more specific):
find . -name "*.md" -type f ! -path "./_audit_output/*" ! -name "S5_UPDATE_NOTES.md" \
  -exec sed -i 's/Round 2: 6 MANDATORY iteration/Round 2: 6 MANDATORY iteration/g' {} +
```markdown

### Sub-group 2b: "9 iterations" for Round 3

**Count:** 3+ instances
**Files:**
- `EPIC_WORKFLOW_USAGE.md:387`
- `reference/glossary.md:685`
- `reference/stage_5/stage_5_reference_card.md:28`

**Fix Command:**
```bash
find . -name "*.md" -type f ! -path "./_audit_output/*" ! -name "S5_UPDATE_NOTES.md" \
  -exec sed -i 's/9 iterations/9 iterations/g' {} +
```markdown

### Sub-group 2c: "8 MANDATORY iterations" → "7 iterations"

**Count:** 3 instances

**Fix Command:**
```bash
find . -name "*.md" -type f ! -path "./_audit_output/*" ! -name "S5_UPDATE_NOTES.md" \
  -exec sed -i 's/Round 1: 7 MANDATORY iteration/Round 1: 7 MANDATORY iteration/g' {} +
```markdown

---

## Group 3: Fix Gate 23a = I20 (P1, Automated)

**Pattern:** "Iteration 20" → "Iteration 20"
**Pattern 2:** "Iteration 19:" → "Iteration 19:"

**Count:** 10+ instances
**Files:**
- `prompts/s5_s8_prompts.md` (3 instances)
- `EPIC_WORKFLOW_USAGE.md` (2 instances)
- `reference/faq_troubleshooting.md` (5+ instances)
- `debugging/root_cause_analysis.md`

**Fix Commands:**
```bash
# Fix "Iteration 20" → "Iteration 20"
find . -name "*.md" -type f ! -path "./_audit_output/*" ! -name "S5_UPDATE_NOTES.md" \
  -exec sed -i 's/Iteration 20/Iteration 20/g; s/iteration 20/iteration 20/g' {} +

# Fix "(Iteration 20)" → "(Iteration 20)"
find . -name "*.md" -type f ! -path "./_audit_output/*" ! -name "S5_UPDATE_NOTES.md" \
  -exec sed -i 's/(Iteration 20)/(Iteration 20)/g' {} +

# Fix "Iteration 19:" (Integration Gap Check)
find . -name "*.md" -type f ! -path "./_audit_output/*" ! -name "S5_UPDATE_NOTES.md" \
  -exec sed -i 's/Iteration 19:/Iteration 19:/g' {} +
```markdown

---

## Group 4: Fix Gate 24 = I22 (P1, Automated)

**Pattern:** "Iteration 22" → "Iteration 22"

**Count:** 15+ instances (most common)
**Files:**
- `prompts/s5_s8_prompts.md` (5+ instances)
- `prompts_reference_v2.md`
- `EPIC_WORKFLOW_USAGE.md`
- `reference/faq_troubleshooting.md` (8+ instances)
- `reference/glossary.md`
- `templates/implementation_plan_template.md` (2 instances)

**Fix Commands:**
```bash
# Fix "Iteration 22" → "Iteration 22"
find . -name "*.md" -type f ! -path "./_audit_output/*" ! -name "S5_UPDATE_NOTES.md" \
  -exec sed -i 's/Iteration 22/Iteration 22/g; s/iteration 22/iteration 22/g' {} +

# Fix "(Iteration 22)" → "(Iteration 22)"
find . -name "*.md" -type f ! -path "./_audit_output/*" ! -name "S5_UPDATE_NOTES.md" \
  -exec sed -i 's/(Iteration 22)/(Iteration 22)/g' {} +
```markdown

---

## Group 5: Fix Gate 25 = I21 (P1, Automated)

**Pattern:** "Iteration 21" → "Iteration 21"

**Count:** 5+ instances
**Files:**
- `prompts/s5_s8_prompts.md` (3 instances)
- `reference/faq_troubleshooting.md` (2 instances)

**Fix Commands:**
```bash
# Fix "Iteration 21" → "Iteration 21"
find . -name "*.md" -type f ! -path "./_audit_output/*" ! -name "S5_UPDATE_NOTES.md" \
  -exec sed -i 's/Iteration 21/Iteration 21/g; s/iteration 25/iteration 21/g' {} +

# Fix "(Iteration 21)" → "(Iteration 21)"
find . -name "*.md" -type f ! -path "./_audit_output/*" ! -name "S5_UPDATE_NOTES.md" \
  -exec sed -i 's/(Iteration 21)/(Iteration 21)/g' {} +
```markdown

---

## Group 6: Manual Spot-Fixes (P2, Manual)

### Issue M1: glossary.md complex rewrites

**Lines 683-685:** Need manual rewrite due to complex structure

**Current:**
```text
- Round 1: Iterations 1-7 + Gate 4a + Gate 7a (9 iterations)
- Round 2: Iterations 8-13 (9 iterations)
- Round 3: Iterations 14-22 (includes Gates 23a, 24, 25) (9 iterations)
```text

**After automated fixes:**
```text
- Round 1: Iterations 1-7 + Gate 4a + Gate 7a (7 iterations)  [STILL WRONG FORMAT]
- Round 2: Iterations 8-13 (6 iterations)  [FIXED BY AUTOMATION]
- Round 3: Iterations 14-22 (includes Gates 23a, 24, 25) (9 iterations)  [FIXED BY AUTOMATION]
```text

**Manual edit needed for Line 683:**
```diff
- Round 1: Iterations 1-7 + Gate 4a + Gate 7a (7 iterations)
+ Round 1: Iterations 1-7 (7 iterations, includes Gates 4a, 7a)
```markdown

### Issue M2: glossary.md Gate iteration mapping

**Line 503:** "Gate 24 = Iteration 22" → needs update

**Manual edit:**
```diff
- Gate 24 = Iteration 22
+ Gate 24 = Iteration 22
```markdown

### Issue M3: README.md gate descriptions

**Lines 115-117:** Add iteration numbers to gate descriptions

**Optional enhancement:**
```diff
- Gate 23a: Pre-Implementation Spec Audit (Round 3)
+ Gate 23a: Pre-Implementation Spec Audit (Round 3, Iteration 20)

- Gate 24: GO/NO-GO Decision (Round 3)
+ Gate 24: GO/NO-GO Decision (Round 3, Iteration 22)

- Gate 25: Spec Validation Check (Round 3)
+ Gate 25: Spec Validation Check (Round 3, Iteration 21)
```markdown

---

## Execution Steps

### Step 1: Run Automated Fixes (Groups 1-5)

Execute all sed commands in order:

```bash
cd feature-updates/guides_v2

# Group 1a: I8-I13 → I8-I13
find . -name "*.md" -type f ! -path "./_audit_output/*" ! -name "S5_UPDATE_NOTES.md" \
  -exec sed -i 's/Iterations 8-13/Iterations 8-13/g; s/I8-I13/I8-I13/g' {} +

# Group 1b: I14-I22 → I14-I22
find . -name "*.md" -type f ! -path "./_audit_output/*" ! -name "S5_UPDATE_NOTES.md" \
  -exec sed -i 's/Iterations 14-22/Iterations 14-22/g; s/I14-I22/I14-I22/g' {} +

# Group 2a: Round 2 counts
find . -name "*.md" -type f ! -path "./_audit_output/*" ! -name "S5_UPDATE_NOTES.md" \
  -exec sed -i 's/Round 2: 6 MANDATORY iteration/Round 2: 6 MANDATORY iteration/g' {} +

# Group 2b: 9 iterations → 9 iterations
find . -name "*.md" -type f ! -path "./_audit_output/*" ! -name "S5_UPDATE_NOTES.md" \
  -exec sed -i 's/9 iterations/9 iterations/g' {} +

# Group 2c: 8 MANDATORY → 7 MANDATORY
find . -name "*.md" -type f ! -path "./_audit_output/*" ! -name "S5_UPDATE_NOTES.md" \
  -exec sed -i 's/Round 1: 7 MANDATORY iteration/Round 1: 7 MANDATORY iteration/g' {} +

# Group 3: Iteration 20 → Iteration 20
find . -name "*.md" -type f ! -path "./_audit_output/*" ! -name "S5_UPDATE_NOTES.md" \
  -exec sed -i 's/Iteration 20/Iteration 20/g; s/iteration 20/iteration 20/g; s/(Iteration 20)/(Iteration 20)/g' {} +

# Group 3: Iteration 19: → Iteration 19:
find . -name "*.md" -type f ! -path "./_audit_output/*" ! -name "S5_UPDATE_NOTES.md" \
  -exec sed -i 's/Iteration 19:/Iteration 19:/g' {} +

# Group 4: Iteration 22 → Iteration 22
find . -name "*.md" -type f ! -path "./_audit_output/*" ! -name "S5_UPDATE_NOTES.md" \
  -exec sed -i 's/Iteration 22/Iteration 22/g; s/iteration 22/iteration 22/g; s/(Iteration 22)/(Iteration 22)/g' {} +

# Group 5: Iteration 21 → Iteration 21
find . -name "*.md" -type f ! -path "./_audit_output/*" ! -name "S5_UPDATE_NOTES.md" \
  -exec sed -i 's/Iteration 21/Iteration 21/g; s/iteration 25/iteration 21/g; s/(Iteration 21)/(Iteration 21)/g' {} +

echo "✓ Automated fixes complete"
```markdown

### Step 2: Manual Fixes (Group 6)

Use Edit tool for glossary.md and optional README.md enhancements.

### Step 3: Verification

```bash
# Verify iteration ranges
grep -rn "8-16\|17-25" --include="*.md" . | grep -v "_audit_output" | grep -v "S5_UPDATE_NOTES"
# Expected: 0 results

# Verify old gate iterations
grep -rn "Iteration 20\|Iteration 22\|Iteration 21" --include="*.md" . | grep -v "_audit_output" | grep -v "S5_UPDATE_NOTES"
# Expected: 0 results

# Verify round counts
grep -rn "9 iteration.*Round 2\|10 iteration.*Round 3\|8.*iteration.*Round 1" --include="*.md" -i . | grep -v "_audit_output"
# Expected: 0 results
```

---

## Exit Criteria

- [x] All issues grouped by pattern
- [x] Groups prioritized by severity
- [x] Sed commands created for automated groups
- [x] Manual edit locations identified
- [x] Fix order documented
- [x] Verification commands provided
- [x] Ready for Stage 3 (Apply Fixes)

---

**Next Stage:** `stages/stage_3_apply_fixes.md` (Round 2)
