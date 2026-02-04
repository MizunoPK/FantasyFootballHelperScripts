# D4: Count Accuracy

**Dimension Number:** 4
**Category:** Content Quality Dimensions
**Automation Level:** 90% automated
**Priority:** MEDIUM
**Last Updated:** 2026-02-04

**Focus:** Ensure numeric claims in documentation match reality (stage counts, iteration counts, file counts)
**Typical Issues Found:** 5-15 per audit

---

## Table of Contents

1. [What This Checks](#what-this-checks)
2. [Why This Matters](#why-this-matters)
3. [Pattern Types](#pattern-types)
4. [How Errors Happen](#how-errors-happen)
5. [Automated Validation](#automated-validation)
6. [Manual Validation](#manual-validation)
7. [Context-Sensitive Rules](#context-sensitive-rules)
8. [Real Examples](#real-examples)
9. [Integration with Other Dimensions](#integration-with-other-dimensions)

---

## What This Checks

**D4: Count Accuracy** validates that numeric claims in documentation match reality:

1. **Stage Counts** - "10 stages" actually shows S1-S10
2. **Phase Counts** - "S5 has 3 phases" matches S5.P1, S5.P2, S5.P3
3. **Iteration Counts** - "22 iterations in S5" matches actual iteration count
4. **Gate Counts** - "8 mandatory gates" matches reference/mandatory_gates.md
5. **File Counts** - "16 dimensions" matches actual dimension count
6. **List Item Counts** - Numbered lists match their claimed count
7. **Duration Claims** - "3-5 rounds typical" matches historical evidence

**Coverage:**
- All workflow documentation (CLAUDE.md, README.md, EPIC_WORKFLOW_USAGE.md)
- Stage guides (iteration counts, phase counts)
- Reference materials (gate lists, dimension lists)
- Templates (step counts, checklist counts)

**Key Distinction from D14 (Content Accuracy):**
- **D14:** Validates semantic correctness (claims match reality broadly)
- **D4:** Validates numeric correctness (specific counts are accurate)

---

## Why This Matters

**Incorrect counts = User and agent confusion about workflow completeness**

### Impact of Count Errors:

**Stage Count Mismatch:**
- Documentation says "9 stages"
- Actual workflow has 10 stages (S1-S10)
- User thinks workflow incomplete or documentation wrong
- Example: After S4 added, several places still said "9 stages"

**Iteration Count Errors:**
- Guide says "S5 has 20 iterations"
- Actual S5 has 22 iterations
- Agent completes I20, thinks done, skips I21-I22
- Critical gates (Gate 23a, Gate 24, Gate 25) in I21-I22 missed

**Gate Count Mismatches:**
- CLAUDE.md says "5 gates"
- reference/mandatory_gates.md lists 10 gates
- Agent doesn't know which is correct
- May skip important gates

**File Count Claims:**
- README says "8 dimensions implemented"
- Only 6 dimension files exist in dimensions/
- User questions documentation accuracy
- Creates doubt about entire system

**List Item Count Errors:**
- Section header: "## 5 Critical Rules"
- List has 7 items
- User confused about which 5 are "critical"
- May skip important rules thinking they're extra

### Historical Evidence:

**KAI-7 Issues:**
- Multiple places said "9 stages" after S4 was added (actual: 10)
- S5 guide header said "20 iterations" but had 22
- CLAUDE.md Stage Workflows section listed inconsistent gate counts
- README.md dimension table showed wrong totals after Phase 1

**Why 90% Automation:**
- Automated: Counting files, list items, stages, phases, iterations
- Manual Required: Validating semantic meaning of counts (e.g., "typical" vs "maximum")

---

## Pattern Types

### Type 0: Root-Level Workflow Count Claims (CRITICAL - Often Missed)

**Files to Always Check:**
```
C:\Users\kmgam\code\FantasyFootballHelperScripts\CLAUDE.md
feature-updates/guides_v2/README.md
feature-updates/guides_v2/EPIC_WORKFLOW_USAGE.md
feature-updates/guides_v2/prompts_reference_v2.md
```

**What to Validate:**

**CLAUDE.md - Stage Count:**
```markdown
## Stage Workflows Quick Reference

**S1: Epic Planning**
**S2: Feature Planning**
...
**S10: Epic Cleanup**
```

**Search Commands:**
```bash
# Count stage sections in CLAUDE.md
grep -c "^\*\*S[0-9]" CLAUDE.md
# Expected: 10 (S1-S10)

# Verify no missing stages
for i in {1..10}; do
  if ! grep -q "^\*\*S$i:" CLAUDE.md; then
    echo "MISSING: S$i not found in CLAUDE.md"
  fi
done
```

**README.md - Dimension Count:**
```markdown
The audit evaluates guides across **16 critical dimensions**:
```

**Validation:**
```bash
# Count dimension entries in README.md dimension table
grep -c "^\| \*\*D[0-9]" feature-updates/guides_v2/audit/README.md
# Expected: 16

# Count actual dimension files
ls -1 feature-updates/guides_v2/audit/dimensions/d*.md | wc -l
# Should match README claim
```

**EPIC_WORKFLOW_USAGE.md - Stage/Phase/Iteration Claims:**
```markdown
S5: Implementation Planning (22 iterations, 3 rounds)
```

**Validation:**
```bash
# Extract iteration count claim
claimed=$(grep "S5.*iterations" feature-updates/guides_v2/EPIC_WORKFLOW_USAGE.md | grep -oE "[0-9]+ iterations")

# Count actual iterations in S5 guides
actual=$(grep -rh "^### S5\\.P[0-9]\\." feature-updates/guides_v2/stages/s5/ | wc -l)

# Compare
if [ "$claimed" != "$actual" ]; then
  echo "MISMATCH: S5 iteration count claim doesn't match reality"
fi
```

**Red Flags:**
- CLAUDE.md lists 9 stages but workflow has 10
- README.md says "8 dimensions" but table lists 16
- EPIC_WORKFLOW_USAGE.md says "S5 has 20 iterations" but S5 guides show 22
- prompts_reference_v2.md says "45 prompts" but only 38 exist

**Automated:** ✅ Yes (can count stages, files, list items automatically)

---

### Type 1: Stage Count Validation

**What to Check:**
All references to total stage count should say "10 stages" (S1-S10).

**Common Locations:**
```markdown
## Workflow Overview

The epic workflow consists of **10 stages** from planning to cleanup.

**Stages:**
S1 → S2 → S3 → S4 → S5 → S6 → S7 → S8 → S9 → S10
```

**Search Commands:**
```bash
# Find all numeric stage claims
grep -rn "[0-9]+ stages\|[0-9]+-stage" feature-updates/guides_v2/

# Extract just the numbers
grep -roh "[0-9]+ stages" feature-updates/guides_v2/ | sort | uniq -c

# Should show: "10 stages" (not 9, not 11)
```

**Validation Checklist:**
- [ ] CLAUDE.md mentions correct total (10 stages)
- [ ] README.md workflow section shows 10 stages
- [ ] EPIC_WORKFLOW_USAGE.md stage list has 10 entries
- [ ] No files claim "9 stages" (outdated after S4 added)
- [ ] Stage progression diagrams show all 10 stages

**Common Errors:**
- "9 stages" (before S4 was added between old S3 and S4)
- "7 stages" (very old workflow before S8, S9, S10 added)
- Diagram shows S1 → S2 → ... → S9 (missing S10)

**Automated:** ✅ Yes (grep for stage count claims, verify against actual count)

---

### Type 2: Phase Count Validation

**What to Check:**
Each stage's phase count claims match actual phase structure.

**Phase Count by Stage:**

| Stage | Phases | Notation |
|-------|--------|----------|
| S1 | 6 | P1-P6 |
| S2 | 2 | P1-P2 |
| S3 | 3 | P1-P3 |
| S4 | 4 iterations (no phases) | I1-I4 |
| S5 | 3 | P1-P3 |
| S6 | No phases (single-phase) | - |
| S7 | 3 | P1-P3 |
| S8 | 2 | P1-P2 |
| S9 | 4 | P1-P4 |
| S10 | No phases (with S10.P1 sub-section) | - |

**Search Commands:**
```bash
# For each stage, extract phase count claim
for stage in s{1..10}; do
  echo "=== $stage ==="
  # Find claims like "S1 has 6 phases" or "(6 phases)"
  grep -rn "$stage.*[0-9]+ phase\|[0-9]+ phases.*$stage" \
    feature-updates/guides_v2/ | head -3

  # Count actual phase directories/files
  phase_count=$(find feature-updates/guides_v2/stages/$stage/ -name "*_p[0-9]*" | wc -l)
  echo "Actual phase files: $phase_count"
done
```

**Validation Process:**

**Example: S1 Phase Count**
```bash
# Claim in documentation
grep "S1.*phases" feature-updates/guides_v2/EPIC_WORKFLOW_USAGE.md
# Should say: "S1 has 6 phases (P1-P6)"

# Actual phases in S1 guide
grep "^## S1\.P[0-9]" feature-updates/guides_v2/stages/s1/*.md | wc -l
# Should return: 6

# Verify P1-P6 all exist
for p in {1..6}; do
  if ! grep -q "S1\.P$p" feature-updates/guides_v2/stages/s1/*.md; then
    echo "MISSING: S1.P$p"
  fi
done
```

**Red Flags:**
- Documentation says "S1 has 5 phases" but guide shows P1-P6
- Missing phase in sequence (P1, P2, P4, P5 - P3 missing)
- Phase count includes iterations incorrectly (counting I1-I4 as phases)

**Automated:** ✅ Yes (can count phase sections and compare to claims)

---

### Type 3: Iteration Count Validation

**What to Check:**
Iteration counts in documentation match actual iteration sections in guides.

**Critical: S5 Iteration Count (Most Complex)**

**Documentation Claim:**
```markdown
S5: Implementation Planning (22 iterations across 3 rounds)
- Round 1 (P1): I1-I7 (7 iterations)
- Round 2 (P2): I8-I13 (6 iterations)
- Round 3 (P3): I14-I22 (9 iterations)
```

**Validation Commands:**
```bash
# Count S5 iteration sections
grep -rh "^### S5\.P[0-9]\.I[0-9]\|^## I[0-9]" \
  feature-updates/guides_v2/stages/s5/ | wc -l
# Expected: 22

# Verify Round 1 (I1-I7)
grep -c "^### I[1-7]\b\|S5\.P1\.I[1-7]" \
  feature-updates/guides_v2/stages/s5/s5_p1*.md
# Expected: 7

# Verify Round 2 (I8-I13)
grep -c "^### I[89]\b\|^### I1[0-3]\b\|S5\.P2\.I" \
  feature-updates/guides_v2/stages/s5/s5_p2*.md
# Expected: 6

# Verify Round 3 (I14-I22)
grep -c "^### I1[4-9]\b\|^### I2[0-2]\b\|S5\.P3\.I" \
  feature-updates/guides_v2/stages/s5/s5_p3*.md
# Expected: 9
```

**Other Stages with Iterations:**

**S2.P1 (3 iterations):**
```bash
grep -c "S2\.P1\.I[1-3]" feature-updates/guides_v2/stages/s2/*.md
# Expected: 3 (I1, I2, I3)
```

**S4 (4 iterations):**
```bash
grep -c "S4\.I[1-4]" feature-updates/guides_v2/stages/s4/*.md
# Expected: 4 (I1, I2, I3, I4)
```

**Red Flags:**
- Documentation says "S5 has 20 iterations" (old count before I21-I22 added)
- Missing iteration in sequence (I1, I2, I4 - I3 missing)
- Iteration numbers don't match round boundaries (Round 2 starts at I9 instead of I8)

**Automated:** ✅ Yes (can count iteration sections and validate sequence)

---

### Type 4: Gate Count Validation

**What to Check:**
Gate count claims match reference/mandatory_gates.md official count.

**Source of Truth:**
```
feature-updates/guides_v2/reference/mandatory_gates.md
```

**Official Gate Count: 10 gates**
- Gate 1, Gate 2, Gate 3 (stage-level)
- Gate 4.5, Gate 5 (stage-level)
- Gate 4a, Gate 7a, Gate 23a, Gate 24, Gate 25 (iteration-level)

**Search Commands:**
```bash
# Count gates in mandatory_gates.md
grep -c "^| Gate [0-9]" \
  feature-updates/guides_v2/reference/mandatory_gates.md
# Expected: 10

# Find all gate count claims in documentation
grep -rn "[0-9]+ gates\|[0-9]+ mandatory gates" \
  feature-updates/guides_v2/ CLAUDE.md

# Verify each claim matches 10
```

**Common Count Claims to Validate:**

**CLAUDE.md:**
```markdown
## Gate Numbering System

The workflow uses **10 quality gates** (both stage-level and iteration-level):
```

**README.md:**
```markdown
## Quality Gates

The workflow includes **10 mandatory gates** to ensure quality.
```

**Validation:**
```bash
# Extract claimed count
claimed=$(grep -oh "[0-9]+ gates" CLAUDE.md | head -1 | grep -o "[0-9]+")

# Count actual gates in reference
actual=$(grep -c "^| Gate" feature-updates/guides_v2/reference/mandatory_gates.md)

if [ "$claimed" -ne "$actual" ]; then
  echo "MISMATCH: Gate count claim ($claimed) != actual ($actual)"
fi
```

**Red Flags:**
- Documentation says "8 gates" (outdated after Gates 24, 25 added)
- Documentation says "5 user gates" but only 3 exist (Gates 3, 4.5, 5)
- Inconsistent counts between CLAUDE.md and README.md

**Automated:** ✅ Yes (can count gates in reference file and compare to claims)

---

### Type 5: File Count Validation

**What to Check:**
Claims about file counts match actual file system.

**Common File Count Claims:**

**Dimension Count:**
```markdown
The audit system has **16 dimensions** covering all quality aspects.
```

**Validation:**
```bash
# Count dimension files
ls -1 feature-updates/guides_v2/audit/dimensions/d*.md | wc -l
# Expected: 16 (d1.md through d16.md, may have gaps)

# Count dimension entries in README
grep -c "^\| \*\*D[0-9]" feature-updates/guides_v2/audit/README.md
# Expected: 16
```

**Stage Count:**
```markdown
The workflow consists of **10 stages** with guides in stages/ directory.
```

**Validation:**
```bash
# Count stage directories
ls -d feature-updates/guides_v2/stages/s*/ | wc -l
# Expected: 10 (s1/ through s10/)
```

**Template Count:**
```markdown
We provide **8 templates** for common workflows.
```

**Validation:**
```bash
# Count templates
ls -1 feature-updates/guides_v2/templates/*.md | wc -l
# Compare to claim in README
```

**Prompt Count:**
```markdown
prompts_reference_v2.md consolidates **45+ prompts** from all stages.
```

**Validation:**
```bash
# Count prompt sections
grep -c "^###[^#]" feature-updates/guides_v2/prompts_reference_v2.md
# Should be ≥45 if claim is "45+"
```

**Red Flags:**
- Claim says "8 dimensions" but 16 files exist
- Claim says "12 templates" but only 8 files in templates/
- Vague claims like "dozens of prompts" without specific count

**Automated:** ✅ Yes (can count files and compare to documentation claims)

---

### Type 6: List Item Count Validation

**What to Check:**
Section headers claiming "N items" actually have N items in list.

**Common Pattern:**
```markdown
## 5 Critical Rules

1. Rule one
2. Rule two
3. Rule three
4. Rule four
5. Rule five
6. Rule six  ← ERROR: Claimed 5, have 6
```

**Search Commands:**
```bash
# Find headers with numeric claims
grep -rn "^## [0-9]+ \|^### [0-9]+ " feature-updates/guides_v2/

# For each match, count items in following list
# (Manual validation required - need to parse list structure)
```

**Validation Process:**

1. **Find numeric header:**
   ```bash
   grep -n "^## 8 Exit Criteria" stages/s5/s5_p3_i2_gates_part1.md
   # Line 245: ## 8 Exit Criteria
   ```

2. **Extract list following header:**
   ```bash
   sed -n '245,/^##/p' stages/s5/s5_p3_i2_gates_part1.md | grep "^- \|^[0-9]\."
   ```

3. **Count items:**
   ```bash
   sed -n '245,/^##/p' stages/s5/s5_p3_i2_gates_part1.md | grep -c "^- \|^[0-9]\."
   # Should be 8
   ```

**Common Patterns to Validate:**

- "## 3 Phases" → 3 phase subsections
- "### 5 Validation Steps" → 5 numbered steps
- "## 10 Mandatory Gates" → 10 gate entries
- "### 4 Common Mistakes" → 4 mistake descriptions

**Red Flags:**
- "## 5 Rules" but 7 rules listed
- "### 3 Examples" but only 2 examples provided
- "## 10 Steps" but steps go 1-9 (missing step 10)

**Automated:** ⚠️ Partial (can find headers, requires parsing to count items reliably)

---

### Type 7: Duration Estimate Consistency

**What to Check:**
Duration claims are consistent across documentation and match historical evidence.

**Common Duration Claims:**

**Stage Duration:**
```markdown
S5: Implementation Planning (3-5 hours)
```

**Validation:**
- Check CLAUDE.md for same stage
- Check EPIC_WORKFLOW_USAGE.md for same stage
- Verify durations are consistent
- Compare to phase/iteration durations (should sum to total)

**Example: S5 Duration Breakdown**
```markdown
CLAUDE.md: S5 (3-5 hours total)

EPIC_WORKFLOW_USAGE.md:
- S5.P1: 60-90 min
- S5.P2: 45-60 min
- S5.P3: 90-120 min
TOTAL: 195-270 min = 3.25-4.5 hours ✓ (within 3-5 hour range)
```

**Search Commands:**
```bash
# Find all duration mentions for a stage
grep -rn "S5.*hour\|S5.*min" feature-updates/guides_v2/ CLAUDE.md

# Check for inconsistencies
# - CLAUDE.md says "2-3 hours"
# - README.md says "3-5 hours"
# → MISMATCH
```

**Audit Round Duration:**
```markdown
audit/README.md: Typical audit requires 3-5 rounds
```

**Validation:**
- Check historical evidence section in audit guides
- Verify claim matches reality
- Look for "typically" vs "minimum" vs "maximum" distinctions

**Red Flags:**
- CLAUDE.md says "2-3 hours", guide says "4-6 hours"
- Phase durations sum to 6 hours, but stage claims "3-4 hours"
- Historical evidence shows 5 rounds typical, but docs say 3

**Automated:** ⚠️ Partial (can find duration mentions, requires semantic comparison)

---

## How Errors Happen

### Root Cause 1: Workflow Evolution Without Count Updates

**Scenario:**
- Original workflow: 9 stages (S1-S9)
- S4 added between old S3 and S4
- All stages renumbered
- **FORGOT** to update count claims in documentation

**Result:**
- CLAUDE.md still says "9 stages"
- README.md workflow section shows 10 stages
- Inconsistent counts across documentation

**Example from History:**
After S4 (Feature Testing Strategy) added, several files still said "9 stages" for weeks until audit caught it.

---

### Root Cause 2: Iterations Added Without Header Updates

**Scenario:**
- S5 originally had 20 iterations (I1-I20)
- Gates 23a, 24, 25 required more setup
- Added I21, I22 for gate implementation
- Updated iteration content
- **FORGOT** to update section headers saying "20 iterations"

**Result:**
- Guide headers say "S5 (20 iterations)"
- Actual guide has I1-I22 (22 iterations)
- Agent completes I20, thinks done, skips critical gates

---

### Root Cause 3: List Expansion Without Count Update

**Scenario:**
- Section: "## 5 Critical Rules"
- User feedback: "Add rule about X"
- Added 6th rule to list
- **FORGOT** to update header to "## 6 Critical Rules"

**Result:**
- Header says 5, list has 6
- User confused about which 5 are "critical"
- May skip rule 6 thinking it's optional

---

### Root Cause 4: Copy-Paste Count Propagation

**Scenario:**
- Create new dimension guide by copying D1
- D1 has "Type 1-5 patterns (5 types total)"
- New dimension has 6 types
- **FORGOT** to update count in overview

**Result:**
- Overview says "5 pattern types"
- Guide defines 6 pattern types (Type 0-5)
- Documentation-to-content mismatch

---

### Root Cause 5: Aggregate Counts Not Updated After Changes

**Scenario:**
- Phase 1 complete: 8 dimensions implemented
- Implementation tracker updated
- README.md says "Current: 8 dimensions"
- **LATER** Phase 2 complete: 12 dimensions total
- Implementation tracker updated
- **FORGOT** to update README.md

**Result:**
- README.md says "8 dimensions" (outdated)
- Tracker says "12 dimensions" (current)
- Users see conflicting information

---

## Automated Validation

### Pre-Audit Script Coverage

**From `scripts/pre_audit_checks.sh`:**

**CHECK 12: Stage Count Validation** *(planned, not yet implemented)*
```bash
#!/bin/bash
echo "Validating stage counts..."

# Count actual stages
actual_stages=$(ls -d feature-updates/guides_v2/stages/s*/ | wc -l)

# Find stage count claims
claims=$(grep -roh "[0-9]+ stages" feature-updates/guides_v2/ CLAUDE.md | \
         grep -o "[0-9]+" | sort -u)

# Verify all claims match actual
for claim in $claims; do
  if [ "$claim" -ne "$actual_stages" ]; then
    echo "ERROR: Found claim of '$claim stages' but actual is $actual_stages"
  fi
done

echo "Expected: $actual_stages stages"
```

**CHECK 13: Iteration Count Validation** *(planned, not yet implemented)*
```bash
#!/bin/bash
echo "Validating S5 iteration count..."

# Count S5 iterations
actual=$(grep -rh "^### S5\.P[0-9]\.I[0-9]" feature-updates/guides_v2/stages/s5/ | wc -l)

# Find iteration count claims for S5
claims=$(grep -roh "S5.*[0-9]+ iterations" feature-updates/guides_v2/ | \
         grep -o "[0-9]+" | head -1)

if [ "$claims" -ne "$actual" ]; then
  echo "ERROR: S5 iteration count claim ($claims) doesn't match actual ($actual)"
fi

echo "S5 iterations: $actual (claimed: $claims)"
```

**CHECK 14: Gate Count Validation** *(planned, not yet implemented)*
```bash
#!/bin/bash
echo "Validating gate counts..."

# Count gates in reference
actual=$(grep -c "^| Gate" feature-updates/guides_v2/reference/mandatory_gates.md)

# Find gate count claims
claims=$(grep -roh "[0-9]+ gates\|[0-9]+ mandatory gates" \
         feature-updates/guides_v2/ CLAUDE.md | grep -o "[0-9]+" | sort -u)

for claim in $claims; do
  if [ "$claim" -ne "$actual" ]; then
    echo "ERROR: Found claim of '$claim gates' but reference shows $actual"
  fi
done

echo "Expected: $actual gates"
```

**CHECK 15: Dimension Count Validation** *(planned, not yet implemented)*
```bash
#!/bin/bash
echo "Validating dimension counts..."

# Count dimension files
actual_files=$(ls -1 feature-updates/guides_v2/audit/dimensions/d*.md | wc -l)

# Count dimension entries in README
readme_count=$(grep -c "^\| \*\*D[0-9]" feature-updates/guides_v2/audit/README.md)

# Find dimension count claims
claims=$(grep -oh "[0-9]+ dimensions" feature-updates/guides_v2/audit/README.md | \
         grep -o "[0-9]+" | head -1)

if [ "$readme_count" -ne "$actual_files" ]; then
  echo "ERROR: README lists $readme_count dimensions but $actual_files files exist"
fi

if [ "$claims" -ne "$readme_count" ]; then
  echo "ERROR: README claims $claims dimensions but table shows $readme_count"
fi

echo "Dimensions: $actual_files files, $readme_count in table, $claims claimed"
```

**Automation Coverage: ~90%**
- ✅ Stage counts
- ✅ Phase counts
- ✅ Iteration counts
- ✅ Gate counts
- ✅ File counts
- ⚠️ List item counts (requires parsing)
- ⚠️ Duration consistency (requires semantic comparison)

---

## Manual Validation

### Manual Process (Count Audit)

**Duration:** 30-45 minutes
**Frequency:** After workflow changes, after dimension/stage additions

**Step 1: Validate Root-Level Count Claims (10 min)**

```bash
# Extract all numeric claims from root files
echo "=== CLAUDE.md Count Claims ==="
grep -n "[0-9]+ stages\|[0-9]+ gates\|[0-9]+ phases" CLAUDE.md

echo "=== README.md Count Claims ==="
grep -n "[0-9]+ dimensions\|[0-9]+ stages" \
  feature-updates/guides_v2/README.md

echo "=== EPIC_WORKFLOW_USAGE.md Count Claims ==="
grep -n "[0-9]+ iterations\|[0-9]+ phases" \
  feature-updates/guides_v2/EPIC_WORKFLOW_USAGE.md
```

**For each claim:**
1. Note the claimed number
2. Verify against actual count (stages, gates, dimensions, etc.)
3. Flag mismatches for fixing

**Step 2: Validate S5 Iteration Count (Special Case) (5 min)**

```bash
# S5 is most complex - validate thoroughly
echo "=== S5 Iteration Count Validation ==="

# Count Round 1 iterations (I1-I7)
r1=$(grep -c "### I[1-7]\b" feature-updates/guides_v2/stages/s5/s5_p1*.md)
echo "Round 1: $r1 iterations (expected 7)"

# Count Round 2 iterations (I8-I13)
r2=$(grep -c "### I[89]\b\|### I1[0-3]\b" \
     feature-updates/guides_v2/stages/s5/s5_p2*.md)
echo "Round 2: $r2 iterations (expected 6)"

# Count Round 3 iterations (I14-I22)
r3=$(grep -c "### I1[4-9]\b\|### I2[0-2]\b" \
     feature-updates/guides_v2/stages/s5/s5_p3*.md)
echo "Round 3: $r3 iterations (expected 9)"

total=$((r1 + r2 + r3))
echo "TOTAL: $total iterations (expected 22)"
```

**Step 3: Validate Phase Counts Per Stage (10 min)**

```bash
# For each stage, verify phase count
for stage in s{1..10}; do
  echo "=== $stage ==="

  # Find phase count claim in documentation
  claim=$(grep "$stage.*[0-9]+ phase" \
    feature-updates/guides_v2/EPIC_WORKFLOW_USAGE.md | \
    grep -o "[0-9]+" | head -1)

  # Count actual phases
  actual=$(grep -c "^## ${stage^^}\.P[0-9]" \
    feature-updates/guides_v2/stages/$stage/*.md)

  if [ "$claim" != "$actual" ]; then
    echo "MISMATCH: Claimed $claim phases, found $actual"
  else
    echo "OK: $actual phases"
  fi
done
```

**Step 4: Validate List Item Counts (10 min)**

```bash
# Find headers with numeric claims
grep -rn "^## [0-9]+ \|^### [0-9]+ " \
  feature-updates/guides_v2/ > /tmp/numeric_headers.txt

# For each header (manual inspection required)
cat /tmp/numeric_headers.txt

# For each entry:
# 1. Open file at line number
# 2. Count items in list following header
# 3. Verify count matches header claim
# 4. Flag mismatches
```

**Manual Process:**
1. Open file at line number
2. Find end of list (next header or blank section)
3. Count list items (lines starting with "- " or "1. ", etc.)
4. Compare to header claim
5. Record mismatch if found

**Step 5: Validate Gate Count Consistency (5 min)**

```bash
# Get official count from reference
official=$(grep -c "^| Gate" \
  feature-updates/guides_v2/reference/mandatory_gates.md)
echo "Official gate count: $official"

# Find all gate count mentions
echo "=== Gate Count Claims ==="
grep -rn "[0-9]+ gates" feature-updates/guides_v2/ CLAUDE.md

# Manually verify each claim matches official count
```

---

## Context-Sensitive Rules

### Rule 1: "Typical" vs "Maximum" vs "Minimum" Counts

**Context:** Some counts describe ranges or typical cases, not absolutes.

**Valid Variations:**

**Audit Rounds:**
```markdown
audit/README.md: Typical audit requires 3-5 rounds (minimum 3)
```

This is VALID even if some audits take 6-7 rounds:
- "Typical" = most common, not absolute maximum
- "Minimum 3" is the hard requirement
- Outliers beyond typical range are acceptable

**Stage Durations:**
```markdown
S5: 3-5 hours (can extend to 6+ for complex features)
```

This is VALID - duration is estimate, not guarantee.

**Detection:**
```bash
# Look for qualifying language
grep -rn "typical\|usual\|minimum\|maximum\|approximately\|about" \
  feature-updates/guides_v2/
```

**Validation:** If claim uses "typical," "usually," "minimum," "maximum" → VALID (not exact count requirement)

---

### Rule 2: Historical Counts Are Intentionally Different

**Context:** Historical evidence sections may reference old counts.

**Example:**
```markdown
## Historical Evidence

The old workflow had 9 stages (before S4 was added in 2025).
Current workflow: 10 stages.
```

**This is VALID:**
- Historical section intentionally references old structure
- Current section shows updated count
- Not a mismatch error

**Detection:**
```bash
# Check if count appears in "Historical Evidence" section
grep -B 5 -A 5 "9 stages" feature-updates/guides_v2/ | \
  grep -q "Historical Evidence\|History\|Old workflow"
```

**Validation:** Old counts in historical context sections → VALID (not errors)

---

### Rule 3: Approximate Counts With "+" Suffix

**Context:** Some counts intentionally vague with approximations.

**Valid Approximations:**
```markdown
prompts_reference_v2.md: 45+ prompts across all stages
```

**Validation:**
- Count actual prompts: 47
- Claim says "45+"
- 47 ≥ 45, so claim is ACCURATE

**Invalid Example:**
```markdown
Claim: "50+ dimensions"
Actual: 16 dimensions
16 < 50 → INVALID
```

**Detection:**
```bash
# Find approximate counts
grep -rn "[0-9]++" feature-updates/guides_v2/
```

**Validation:** If claim uses "+", verify actual ≥ claimed → VALID if true

---

### Rule 4: Dimension Implementation Status Intentionally Shows Progress

**Context:** Implementation tracker shows current vs total counts.

**Valid Format:**
```markdown
Current Progress: 12/16 dimensions (75%) fully implemented
```

**This shows:**
- 12 currently done
- 16 total planned
- 75% complete

**Not a mismatch** - intentionally showing partial completion.

**Validation:** "X/Y" format indicates progress tracking → VALID (not count error)

---

## Real Examples

### Example 1: Stage Count Outdated After S4 Addition

**Issue Found During KAI-7 Audit Round 2:**

**CLAUDE.md (Root File):**
```markdown
## Epic-Driven Development Workflow (v2)

The v2 workflow is a **9-stage epic-driven development process**...
```

**Problem:**
- Claimed 9 stages
- Actual workflow: S1-S10 (10 stages)
- S4 added between old S3 and S4, all subsequent stages renumbered

**Fix:**
```diff
## Epic-Driven Development Workflow (v2)

-The v2 workflow is a **9-stage epic-driven development process**...
+The v2 workflow is a **10-stage epic-driven development process**...
```

**Root Cause:** S4 added, stage count updated in guides but not in CLAUDE.md root file

**How D4 Detects:**
- Type 0: Root-Level Workflow Count Claims
- Type 1: Stage Count Validation
- Automated: CHECK 12 in pre_audit_checks.sh

---

### Example 2: S5 Iteration Count Mismatch

**Issue Found During S5.P3 Implementation:**

**S5 Router Guide Header:**
```markdown
# S5: Implementation Planning

**Duration:** 3-5 hours
**Iterations:** 20 (across 3 rounds)
```

**Actual S5 Structure:**
- Round 1: I1-I7 (7 iterations)
- Round 2: I8-I13 (6 iterations)
- Round 3: I14-I22 (9 iterations)
- **Total: 22 iterations**

**Problem:**
- Header claimed 20 iterations
- Actual guide has 22 iterations (I21-I22 added for Gates 24, 25)

**Fix:**
```diff
# S5: Implementation Planning

**Duration:** 3-5 hours
-**Iterations:** 20 (across 3 rounds)
+**Iterations:** 22 (across 3 rounds)
```

**Root Cause:** Iterations added for gate implementation, header not updated

**How D4 Detects:**
- Type 3: Iteration Count Validation
- Automated: CHECK 13 validates S5 iteration count specifically

---

### Example 3: Gate Count Inconsistency Between Files

**Issue Found During Gate Reference Creation:**

**CLAUDE.md:**
```markdown
## Gate Numbering System

The workflow uses two types of gates:

**Stage-Level Gates:** 5 gates (Gates 1, 2, 3, 4.5, 5)
**Iteration-Level Gates:** 3 gates (Gates 4a, 7a, 23a)
**TOTAL: 8 gates**
```

**reference/mandatory_gates.md:**
```markdown
| Gate | Type | Location |
|------|------|----------|
| Gate 1 | Stage | S2.P1.I1 |
| Gate 2 | Stage | S2.P1.I3 |
| Gate 3 | Stage | S2.P1.I3 |
| Gate 4.5 | Stage | S3.P3 |
| Gate 5 | Stage | S5.P3 |
| Gate 4a | Iteration | S5.P1.I2 |
| Gate 7a | Iteration | S5.P1.I3 |
| Gate 23a | Iteration | S5.P3.I2 |
| Gate 24 | Iteration | S5.P3.I3 |
| Gate 25 | Iteration | S5.P3.I3 |

TOTAL: 10 gates
```

**Problem:**
- CLAUDE.md said "8 gates total"
- Reference showed 10 gates (Gates 24, 25 not mentioned in CLAUDE.md)

**Fix:**
```diff
## Gate Numbering System

The workflow uses two types of gates:

-**Stage-Level Gates:** 5 gates (Gates 1, 2, 3, 4.5, 5)
+**Stage-Level Gates:** 5 gates (Gate 1, Gate 2, Gate 3, Gate 4.5, Gate 5)
-**Iteration-Level Gates:** 3 gates (Gates 4a, 7a, 23a)
+**Iteration-Level Gates:** 5 gates (Gate 4a, Gate 7a, Gate 23a, Gate 24, Gate 25)
-**TOTAL: 8 gates**
+**TOTAL: 10 gates**
```

**Root Cause:** New gates added to reference, CLAUDE.md not updated

**How D4 Detects:**
- Type 4: Gate Count Validation
- Automated: CHECK 14 compares all gate count claims to reference

---

### Example 4: List Item Count Doesn't Match Header

**Issue Found During S5.P3 Guide Review:**

**Guide Content:**
```markdown
## 8 Exit Criteria for Audit Completion

1. Minimum 3 rounds complete
2. Zero new discoveries in current round
3. Zero verification findings
4. All documented
5. User approved
6. Confidence ≥80%
7. Pattern diversity
8. Spot-checks clean
9. No user challenges
10. File size reductions complete
```

**Problem:**
- Header says "8 Exit Criteria"
- List has 10 items
- Criteria 9-10 added later, header not updated

**Fix Option 1 (Update Header):**
```diff
-## 8 Exit Criteria for Audit Completion
+## 10 Exit Criteria for Audit Completion
```

**Fix Option 2 (Remove Extra Criteria):**
If 9-10 are actually sub-criteria, move them as sub-bullets under criteria 8.

**Root Cause:** List expanded without updating header count

**How D4 Detects:**
- Type 6: List Item Count Validation
- Manual validation: Count list items following numeric headers

---

### Example 5: Dimension Count Outdated After Phase 1

**Issue Found After Phase 1 Completion:**

**README.md:**
```markdown
## Audit System Status

**Current Progress:** 2/16 dimensions (12.5%) fully implemented
```

**Implementation Tracker (Updated):**
```markdown
**Current Progress:** 8/16 dimensions (50%) fully implemented
```

**Problem:**
- README.md showed old progress (2 dimensions)
- Tracker showed current progress (8 dimensions)
- README not updated after Phase 1 completion

**Fix:**
```diff
## Audit System Status

-**Current Progress:** 2/16 dimensions (12.5%) fully implemented
+**Current Progress:** 8/16 dimensions (50%) fully implemented
```

**Root Cause:** Tracker updated, but README overview section forgotten

**How D4 Detects:**
- Type 5: File Count Validation
- Compare claims across files (README vs Tracker)
- Flag inconsistencies

---

## Integration with Other Dimensions

### D14: Content Accuracy

**Overlap:**
- D14 validates semantic correctness broadly
- D4 validates numeric correctness specifically
- **Division:** D14 = "is claim true?", D4 = "is number correct?"

**Example:**
- D14 checks: "S5 is most complex stage" (semantic claim)
- D4 checks: "S5 has 22 iterations" (numeric claim)

**Recommendation:** Run D4 BEFORE D14 (numbers are easier to verify than semantics)

---

### D5: Content Completeness

**Overlap:**
- D5 validates required content exists
- D4 validates counts of that content are correct
- **Division:** D5 = presence, D4 = quantity

**Example:**
- D5 checks: Guide has "Prerequisites" section ✅
- D4 checks: If header says "5 Prerequisites," list has 5 items ✅

---

### D13: Documentation Quality

**Overlap:**
- D13 validates structure and formatting
- D4 validates numeric claims within that structure
- **Division:** D13 = format, D4 = numbers

**Example:**
- D13 checks: Section headers follow consistent format ✅
- D4 checks: "## 8 Steps" actually has 8 steps ✅

---

### D3: Workflow Integration

**Overlap:**
- D3 validates workflow sequence is correct
- D4 validates numeric descriptions of that sequence
- **Division:** D3 = logic, D4 = counts

**Example:**
- D3 checks: S1 → S2 → S3 sequence correct ✅
- D4 checks: Documentation says "10 stages" ✅

---

## Summary

**D4: Count Accuracy validates that numeric claims match reality.**

**Key Validations:**
1. ✅ Stage counts (10 stages S1-S10)
2. ✅ Phase counts (per-stage verification)
3. ✅ Iteration counts (especially S5's 22 iterations)
4. ✅ Gate counts (10 mandatory gates)
5. ✅ File counts (dimensions, templates, etc.)
6. ✅ List item counts (headers match list lengths)
7. ⚠️ Duration consistency (requires semantic validation)

**Automation: ~90%**
- Highly automated (counting is mechanical)
- Manual needed for: semantic contexts, approximate counts, qualifying language

**Critical for:**
- Preventing user/agent confusion about workflow completeness
- Ensuring documentation stays updated after workflow evolution
- Maintaining accuracy in high-visibility root files

**Next Dimension:** D9: Intra-File Consistency (validate consistency within single files)

---

**Last Updated:** 2026-02-04
**Version:** 1.0
**Status:** ✅ Fully Implemented
