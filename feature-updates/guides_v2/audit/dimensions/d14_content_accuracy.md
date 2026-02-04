# Dimension 14: Content Accuracy

**Focus:** Ensure guide content matches reality (file counts, iteration counts, freshness, claims validation)
**Automation Level:** 70% automated
**Typical Issues Found:** 10-20 per audit
**Reading Time:** 15 minutes

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

---

## What This Checks

**Content Accuracy** validates that documented claims match reality:

✅ **File Counts:**
- "19 templates" matches actual template count
- "10 stages" matches actual number of stages
- "22 iterations" matches actual S5 iteration count

✅ **Iteration/Phase Counts:**
- "S2.P1 has 3 iterations" matches actual file structure
- "S5 has 3 rounds" matches actual phase count
- "S7 has 3 phases" matches actual implementation

✅ **Freshness Indicators:**
- "Last Updated" dates are recent (within 1-2 months)
- Stale dates indicate content not reviewed during recent changes
- Root-level files (README.md, EPIC_WORKFLOW_USAGE.md) especially critical

✅ **Claims vs Reality:**
- "Run pre_audit_checks.sh" → script actually exists
- "Checks 6 of 16 dimensions" → actually checks 6 (not 5 or 7)
- "Minimum 3 rounds" → workflow enforces minimum 3

✅ **Version Numbers:**
- "Version 2.0" matches actual workflow version
- Deprecated content marked as such
- Historical references clearly labeled

---

## Why This Matters

### Impact of Inaccurate Content

**Critical Impact:**
- **User Confusion:** "Says 19 templates but I see 23" → trust eroded
- **Agent Errors:** "Run script X" but script doesn't exist → workflow blocked
- **Stale Information:** Last Updated: 2025-12-30 but major changes in Jan 2026 → outdated
- **Template Propagation:** Wrong counts in templates = all new epics have wrong info

**Example Failure (Real):**
```
Guide said: "Audit system has 16 dimensions"
Reality: Only 2 dimensions fully implemented (D1, D2)
         6 dimensions partially implemented (automation only, no guides)
         8 dimensions not implemented at all
Result: User confused about audit completeness, agent claimed "full audit" prematurely
```

### Common Trigger Events

**After Major Refactoring:**
- S5 split into S5-S8 → iteration counts change
- File reorganization → file counts change
- Template additions → template count increases

**After Time Passes:**
- "Last Updated" dates become stale (>1 month old)
- Content describes old workflow but hasn't been updated
- Root files especially prone to staleness

**After Feature Additions:**
- New templates added but README claims old count
- New dimensions added but overview shows old count
- New stages added but workflow diagrams show old count

---

## Pattern Types

### Type 0: Root-Level File Freshness (CRITICAL - Often Missed)

**Files to Always Check:**
```
feature-updates/guides_v2/README.md
feature-updates/guides_v2/EPIC_WORKFLOW_USAGE.md
feature-updates/guides_v2/prompts_reference_v2.md
feature-updates/guides_v2/audit/README.md
feature-updates/guides_v2/audit/audit_overview.md
```

**Why These Matter:**
- **High visibility** - Entry point files referenced in CLAUDE.md
- **High change frequency** - Summarize entire workflow, need frequent updates
- **High impact if stale** - Users see outdated info first

**Search Commands:**
```bash
# Find "Last Updated" dates in root files
cd feature-updates/guides_v2
for file in README.md EPIC_WORKFLOW_USAGE.md prompts_reference_v2.md audit/README.md audit/audit_overview.md; do
  echo "=== $file ==="
  grep -n "Last Updated" "$file" | head -1
done

# Manual check: Are dates within last 1-2 months?
# If NO → File likely stale, needs content review
```

**Red Flags:**
- Last Updated > 2 months old = HIGH RISK of stale content
- Last Updated > 1 month old = WARNING, review recommended
- Root file without "Last Updated" field = CRITICAL GAP

**Validation:**
```bash
# Check if major changes happened since Last Updated date
git log --since="2025-12-30" --oneline stages/ reference/ | wc -l
# If >50 commits → Content likely outdated
```

### Type 1: File Count Claims

**Common Claims:**
```
"19 templates"
"10 stages"
"16 dimensions"
"22 iterations in S5"
```

**Search Commands:**
```bash
# Find all count claims
grep -rn "[0-9]\+ template\|[0-9]\+ stage\|[0-9]\+ dimension\|[0-9]\+ iteration" \
  --include="*.md" guides_v2/

# Extract specific claims
grep -rn "19 template" guides_v2/
grep -rn "10 stage" guides_v2/
grep -rn "16 dimension" guides_v2/
```

**Validation:**
```bash
# Count actual files
find templates -name "*.md" -o -name "*.txt" | wc -l  # Should match claimed template count
ls -d stages/s* | wc -l  # Should match claimed stage count
ls audit/dimensions/d*.md | wc -l  # Should match claimed dimension count (if "fully implemented")
```

### Type 2: Iteration/Phase Count Claims

**Common Claims:**
```
"S2.P1 has 3 iterations"
"S5 has 3 rounds"
"S7 has 3 phases"
"S5 Planning has 22 iterations total"
```

**Search Commands:**
```bash
# Find iteration count claims
grep -rn "S[0-9]\.P[0-9] has [0-9]\+ iteration" guides_v2/
grep -rn "S[0-9] has [0-9]\+ round\|phase" guides_v2/
grep -rn "[0-9]\+ iterations total" guides_v2/
```

**Validation:**
```bash
# Count actual iterations for S5
ls stages/s5/s5_p*_i*.md | wc -l  # Should match claimed iteration count

# Count actual phases for S7
ls stages/s7/s7_p*.md | wc -l  # Should match claimed phase count

# Count rounds for S5
ls stages/s5/s5_p*.md | grep -o "s5_p[0-9]" | sort -u | wc -l  # Should match round count
```

### Type 3: Script/File Existence Claims

**Common Claims:**
```
"Run pre_audit_checks.sh"
"Read ARCHITECTURE.md"
"Use templates/feature_spec_template.md"
```

**Search Commands:**
```bash
# Find all script/file references
grep -rn "Run [a-z_]*\.sh\|Read [A-Z_]*\.md\|Use templates/" \
  --include="*.md" guides_v2/
```

**Validation:**
```bash
# Check each referenced file exists
while read file; do
  [ ! -f "$file" ] && echo "CLAIM BROKEN: $file (referenced but doesn't exist)"
done < referenced_files.txt
```

### Type 4: Feature/Capability Claims

**Common Claims:**
```
"Automated validation catches 90%"
"Checks 6 of 16 dimensions"
"Minimum 3 rounds required"
"100% test pass rate enforced"
```

**Search Commands:**
```bash
# Find capability claims
grep -rn "automated.*[0-9]\+%\|catch.*[0-9]\+%\|Checks [0-9] of [0-9]" \
  --include="*.md" guides_v2/ -i

# Find requirement claims
grep -rn "minimum [0-9]\+\|required.*[0-9]\+\|enforced" \
  --include="*.md" guides_v2/ -i
```

**Validation:**
- **Manual review** - Check if code actually enforces claim
- **Example:** "100% test pass rate enforced" → Verify S7, S9, S10 actually check exit codes
- **Example:** "Minimum 3 rounds" → Verify S5 guides don't allow early exit

---

## How Errors Happen

### Root Cause 1: Content Updated, Metadata Not

**Scenario:** Major refactoring completed, but "Last Updated" not changed

**What Happens:**
```
2025-12-30: Major S5 restructuring (split into 3 rounds)
README.md still shows: "Last Updated: 2025-11-15"
Result: Stale date signals content may be outdated
```

**Why It Happens:**
- Agents focus on content changes, forget metadata
- No automated check for stale "Last Updated" dates
- Root files especially prone (updated less frequently)

### Root Cause 2: Count Claims Hardcoded

**Scenario:** Template added, but hardcoded count not updated

**Before:**
```markdown
The workflow provides 19 templates for epic development.
```

**Change:** Added 4 new templates

**After (WRONG):**
```markdown
The workflow provides 19 templates for epic development.
# Actually 23 templates now
```

**Fix:**
```markdown
The workflow provides 23 templates for epic development.
# OR use dynamic reference:
See `templates/` folder for complete template list.
```

### Root Cause 3: Feature Removed, Claims Remain

**Scenario:** Refactoring removes feature, but documentation still claims it exists

**Example:**
```markdown
Guide: "S5.I10 validates test coverage"
Reality: S5 only has iterations I1-I7 now (I8-I10 merged into S4)
Result: Agent looks for non-existent iteration
```

### Root Cause 4: Optimistic Capability Claims

**Scenario:** Documentation claims feature works, but implementation incomplete

**Example (Real):**
```markdown
Guide: "Audit system validates 16 dimensions comprehensively"
Reality: Only D1, D2 fully implemented (guides + automation)
         D8, D10, D11, D13, D14, D16 partially implemented (automation only)
         D3, D4, D5, D6, D7, D9, D12, D15 not implemented
Result: Users expect comprehensive audit, get partial validation
```

---

## Automated Validation

### Script 1: Validate File Counts (IN pre_audit_checks.sh)

```bash
# CHECK 4: Content Accuracy - File Counts (D14)
# ============================================================================

echo "=== Content Accuracy - File Counts (D14) ==="

# Count actual templates
ACTUAL_TEMPLATES=$(find templates -name "*.md" -o -name "*.txt" | wc -l)

# Check if any files claim different count
CLAIMED_COUNT=$(grep -rn "19 template" stages templates 2>/dev/null | wc -l)

if [ "$CLAIMED_COUNT" -gt 0 ]; then
  echo "Checking template count claims..."
  if [ "$ACTUAL_TEMPLATES" -ne 19 ]; then
    echo "⚠️  Template count mismatch:"
    echo "   Actual: $ACTUAL_TEMPLATES"
    echo "   Claimed: 19 (in $CLAIMED_COUNT locations)"
    # Issue flagged
  else
    echo "✅ Template count accurate: $ACTUAL_TEMPLATES"
  fi
fi
```

### Script 2: Validate Iteration Counts (SHOULD ADD to pre_audit_checks.sh)

```bash
# CHECK 4b: Iteration Count Validation (D14)
# ============================================================================

echo "=== Iteration Count Validation ==="

# S5 should have 22 iterations total
ACTUAL_S5_ITERATIONS=$(grep -rn "I[0-9]\{1,2\}:" stages/s5/ | grep -o "I[0-9]\{1,2\}" | sort -u | wc -l)
CLAIMED_S5_ITERATIONS=$(grep -rn "22 iteration" guides_v2/ | wc -l)

if [ "$ACTUAL_S5_ITERATIONS" -ne 22 ] && [ "$CLAIMED_S5_ITERATIONS" -gt 0 ]; then
  echo "⚠️  S5 iteration count mismatch:"
  echo "   Actual: $ACTUAL_S5_ITERATIONS"
  echo "   Claimed: 22"
fi

# S2.P1 should have 3 iterations
ACTUAL_S2P1_ITERATIONS=$(ls stages/s2/s2_p1_i*.md 2>/dev/null | wc -l)
CLAIMED_S2P1_ITERATIONS=$(grep -rn "S2\.P1.*3 iteration" guides_v2/ | wc -l)

if [ "$ACTUAL_S2P1_ITERATIONS" -ne 3 ] && [ "$CLAIMED_S2P1_ITERATIONS" -gt 0 ]; then
  echo "⚠️  S2.P1 iteration count mismatch:"
  echo "   Actual: $ACTUAL_S2P1_ITERATIONS"
  echo "   Claimed: 3"
fi
```

### Script 3: Check Last Updated Freshness (SHOULD ADD to pre_audit_checks.sh)

```bash
# CHECK 4c: Last Updated Freshness (D14)
# ============================================================================

echo "=== Last Updated Freshness Check ==="

# Get current date (YYYY-MM-DD)
CURRENT_DATE=$(date +%Y-%m-%d)
CURRENT_EPOCH=$(date +%s)

# Check root-level files
for file in README.md EPIC_WORKFLOW_USAGE.md prompts_reference_v2.md audit/README.md; do
  if [ -f "$file" ]; then
    LAST_UPDATED=$(grep "Last Updated" "$file" | head -1 | grep -o "[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}")

    if [ -n "$LAST_UPDATED" ]; then
      # Convert to epoch for comparison
      UPDATED_EPOCH=$(date -d "$LAST_UPDATED" +%s 2>/dev/null || echo "0")
      DAYS_OLD=$(( ($CURRENT_EPOCH - $UPDATED_EPOCH) / 86400 ))

      if [ "$DAYS_OLD" -gt 60 ]; then
        echo "⚠️  STALE: $file (Last Updated: $LAST_UPDATED, $DAYS_OLD days ago)"
      elif [ "$DAYS_OLD" -gt 30 ]; then
        echo "⚠️  WARNING: $file (Last Updated: $LAST_UPDATED, $DAYS_OLD days old)"
      else
        echo "✅ FRESH: $file (Last Updated: $LAST_UPDATED)"
      fi
    else
      echo "❌ MISSING: $file has no 'Last Updated' field"
    fi
  fi
done
```

---

## Manual Validation

### ⚠️ CRITICAL: Always Check Root-Level Files First

**Mandatory root file freshness validation:**

```bash
# Step 0: Check root files for stale Last Updated dates (high-priority)
cd feature-updates/guides_v2

echo "=== Root File Freshness Check ==="
for file in README.md EPIC_WORKFLOW_USAGE.md prompts_reference_v2.md audit/README.md audit/audit_overview.md; do
  if [ -f "$file" ]; then
    echo "File: $file"
    grep -n "Last Updated" "$file" | head -1

    # Check for major changes since that date
    LAST_DATE=$(grep "Last Updated" "$file" | grep -o "[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}" | head -1)
    if [ -n "$LAST_DATE" ]; then
      CHANGES=$(git log --since="$LAST_DATE" --oneline . | wc -l)
      echo "  Commits since Last Updated: $CHANGES"
      if [ "$CHANGES" -gt 50 ]; then
        echo "  ⚠️  HIGH RISK: Many changes since last update - content likely stale"
      fi
    fi
    echo ""
  fi
done
```

**Red Flags:**
- Last Updated > 60 days old = CRITICAL, immediate review needed
- Last Updated > 30 days old = WARNING, content may be stale
- >50 commits since Last Updated = Content likely outdated

### Manual Validation Process

**For count claims:**

```markdown
STEP 1: Extract all count claims from guides
$ grep -rn "[0-9]\+ template\|[0-9]\+ iteration\|[0-9]\+ dimension" guides_v2/

STEP 2: Count actual files for each claim
$ find templates -name "*.md" | wc -l  # Verify template count
$ ls stages/s5/s5_p*_i*.md | wc -l    # Verify S5 iteration count

STEP 3: Compare claimed vs actual
- Match? → ✅ PASS
- Mismatch? → ❌ Add to fix list

STEP 4: For mismatches, update all locations
$ grep -rl "19 template" guides_v2/ | xargs sed -i 's/19 template/23 template/g'
```

**For capability claims:**

```markdown
STEP 1: Extract capability claims
$ grep -rn "automated.*[0-9]\+%\|Checks [0-9] of [0-9]" guides_v2/

STEP 2: Verify each claim manually
- "Checks 6 of 16 dimensions" → Check pre_audit_checks.sh has 6 CHECK blocks
- "90% automated" → Estimate automation coverage

STEP 3: Update or add disclaimers
- If claim accurate → ✅ PASS
- If claim overstates → ❌ Add disclaimer or update claim
```

---

## Context-Sensitive Rules

### Acceptable Variances

**1. Approximate Percentages:**
```markdown
"~90% automated" or "approximately 90%"
```
**Verdict:** ✅ ACCEPTABLE (approximate, not exact)

**2. Historical Counts:**
```markdown
**Before refactoring:** 19 templates
**After refactoring:** 23 templates
```
**Verdict:** ✅ ACCEPTABLE (clearly labeled as historical)

**3. Range Claims:**
```markdown
"Typically finds 10-20 issues per audit"
```
**Verdict:** ✅ ACCEPTABLE (range, not exact)

### Always Errors

**1. Exact Count Wrong:**
```markdown
"The workflow has 19 templates" (but actually has 23)
```
**Verdict:** ❌ ERROR (exact claim, must be accurate)

**2. Stale Last Updated:**
```markdown
Last Updated: 2025-11-15 (but major changes in Jan 2026)
```
**Verdict:** ❌ ERROR (should update metadata)

**3. Feature Claim for Unimplemented Feature:**
```markdown
"Audit validates 16 dimensions" (but only 2 fully implemented)
```
**Verdict:** ❌ ERROR (overstates capability)

---

## Real Examples

### Example 1: Stale Root File (High Priority)

**Issue Found:**
```markdown
File: feature-updates/guides_v2/README.md
Last Updated: 2025-12-30
Current Date: 2026-02-04
Days Stale: 36 days
```

**Analysis:**
- README.md is main entry point (referenced in CLAUDE.md)
- Over 1 month old, likely missed recent changes
- Check git log for changes since 2025-12-30:
  ```bash
  git log --since="2025-12-30" --oneline feature-updates/guides_v2/ | wc -l
  # Result: 127 commits
  ```
- **CRITICAL** - Many changes since last update

**Impact:**
- Users reading README get outdated information
- Content may reference old file structure, old notation
- Trust erosion if users discover inaccuracies

**Fix:**
```bash
# Manual review of README.md content
# Update outdated sections
# Update Last Updated field
sed -i 's/Last Updated:.*$/Last Updated: 2026-02-04/g' README.md
```

### Example 2: Template Count Mismatch

**Issue Found:**
```markdown
File: stages/s1/s1_epic_planning.md
Line: 234
Content: "The workflow provides 19 templates"
Actual Count: 23 templates
```

**Analysis:**
- Hardcoded count in documentation
- 4 new templates added since claim was written
- Claim appears in 3 different files

**Fix:**
```bash
# Find all locations with "19 templates"
grep -rl "19 template" guides_v2/

# Update to correct count
sed -i 's/19 template/23 template/g' stages/s1/s1_epic_planning.md
sed -i 's/19 template/23 template/g' README.md
sed -i 's/19 template/23 template/g' EPIC_WORKFLOW_USAGE.md
```

**Verification:**
```bash
# Verify updated count matches reality
find templates -name "*.md" -o -name "*.txt" | wc -l
# Should return: 23
```

### Example 3: Iteration Count Claim Outdated

**Issue Found:**
```markdown
File: stages/s5/s5_p1_planning_round1.md
Line: 12
Content: "Round 1 has 7 iterations (I1-I7)"
Actual: Round 1 has 7 iterations, but guide splits them across 3 sub-files
```

**Analysis:**
- Claim is technically correct (7 iterations)
- But structure changed: iterations now in s5_p1_i1_*.md, s5_p1_i2_*.md, s5_p1_i3_*.md
- Claim doesn't reflect new file organization

**Fix:**
```markdown
# Update claim to match new structure
"Round 1 has 7 iterations (I1-I7) organized across 3 iteration guides:
- s5_p1_i1_requirements.md (I1-I3)
- s5_p1_i2_algorithms.md (I4-I6 + Gate 4a)
- s5_p1_i3_integration.md (I7 + Gate 7a)"
```

### Example 4: Capability Claim Overstated

**Issue Found:**
```markdown
File: audit/README.md
Line: 87
Content: "The audit evaluates guides across **16 critical dimensions**"
Reality: Only 2 dimensions fully implemented (D1, D2)
         6 dimensions partially implemented (automation only)
         8 dimensions not implemented
```

**Analysis:**
- **CRITICAL** - Claim implies full 16-dimension coverage
- Reality is ~12.5% fully implemented
- Misleading to users expecting comprehensive audit

**Fix:**
```markdown
# Add disclaimer
"The audit evaluates guides across **16 critical dimensions** (2 fully implemented, 6 partially implemented, 8 planned)"

# OR update to reflect reality
"The audit currently implements **2 of 16 planned dimensions** (D1: Cross-Reference Accuracy, D2: Terminology Consistency)"
```

---

## Pattern Library

**Quick reference patterns for common validations:**

```bash
# Find all count claims
grep -rn "[0-9]\+ \(template\|iteration\|dimension\|stage\|phase\)" guides_v2/

# Check Last Updated dates in root files
grep -n "Last Updated" README.md EPIC_WORKFLOW_USAGE.md prompts_reference_v2.md

# Verify template count
find templates -name "*.md" -o -name "*.txt" | wc -l

# Verify stage count
ls -d stages/s* | wc -l

# Verify dimension count (fully implemented)
ls audit/dimensions/d*.md | wc -l

# Find capability claims
grep -rn "automat.*[0-9]\+%\|Checks [0-9] of [0-9]" guides_v2/ -i
```

---

## See Also

**Related Dimensions:**
- **D1: Cross-Reference Accuracy** - Validates file paths exist (complements count validation)
- **D2: Terminology Consistency** - Validates notation (complements claim validation)
- **D5: Content Completeness** ⏳ - Validates no missing sections (complements accuracy)

**Audit Stages:**
- `../stages/stage_1_discovery.md` - How to search for count mismatches
- `../stages/stage_4_verification.md` - Re-verify counts after fixes

**Reference:**
- `../reference/file_size_reduction_guide.md` - Why stale large files are problematic
- `../_internal/DIMENSION_IMPLEMENTATION_STATUS.md` - Current dimension implementation status

---

**When to Use:** Run D14 validation after any template additions, stage restructuring, or if root files haven't been updated in >1 month.
