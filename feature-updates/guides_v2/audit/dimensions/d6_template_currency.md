# Dimension 6: Template Currency

**Focus:** Ensure templates reflect current workflow structure, notation, and stage numbering
**Automation Level:** 70% automated (notation, stage numbers), manual (content accuracy)
**Typical Issues Found:** 5-10 per major workflow change
**Reading Time:** 12 minutes

---

## Table of Contents

1. [What This Checks](#what-this-checks)
2. [Why This Matters](#why-this-matters)
3. [Pattern Types](#pattern-types)
4. [How Templates Become Outdated](#how-templates-become-outdated)
5. [Automated Validation](#automated-validation)
6. [Manual Validation](#manual-validation)
7. [Context-Sensitive Rules](#context-sensitive-rules)
8. [Real Examples](#real-examples)

---

## What This Checks

**Template Currency** validates that templates stay synchronized with current workflow:

✅ **Notation Up-to-Date:**
- Templates use S#.P#.I# notation (not old "S5a", "Stage 5a")
- No old stage references in template text
- Consistent with current naming conventions

✅ **Stage Numbers Correct:**
- Templates reference correct current stage numbers (S1-S10)
- No references to old stage numbers (pre-renumbering)
- Workflow diagrams show current structure

✅ **Section Structure Current:**
- Template sections match current guide structure
- Required sections align with D11 (Structural Patterns)
- No obsolete sections from old workflow

✅ **Example Content Accurate:**
- Example workflows in templates use current stages
- Sample file paths use current structure
- Example commands use current notation

✅ **Agent Status Fields Current:**
- README templates have current guide field names
- Status tracking fields match current workflow
- No obsolete tracking fields

---

## Why This Matters

### Impact of Outdated Templates

**Critical Impact:**
- **Error Propagation:** Every new epic copies outdated template → all new epics have errors
- **Workflow Confusion:** Template shows old workflow → agents follow wrong path
- **Broken References:** Template references old files → new epics have broken links
- **Notation Inconsistency:** Template uses old notation → new epics mix old/new notation

**Example Failure (Hypothetical):**
```
Template: templates/epic_readme_template.md

**Current Stage:** [S6a - Implementation]  ← Old notation

User creates epic → Copies template → New epic has "S6a" notation
Result: New epic mixes old notation "S6a" with new guides using "S6.P1"
Confusion: Is S6a the same as S6? S6.P1? S7?
```

**Multiplication Effect:**
- 1 error in template
- 10 epics created from template
- = 10 epics with same error
- **Fix cost:** 10x if not caught in template

---

## Pattern Types

### Type 1: Old Notation in Templates

**Common Old Notations:**
```
"Stage 5a" → Should be "S5.P1"
"S6a" → Should be "S6.P1" or current stage number
"Round 1" → Should be "S5.P1" (if referring to planning phases)
"5a, 5b, 5c" → Should be "S5.P1, S5.P2, S5.P3" or current structure
```

**Search Commands:**
```bash
# Find old notation in templates
grep -rn "\bS[0-9][a-z]\b\|Stage [0-9][a-z]\|Round [0-9]" templates/

# Find all caps variants
grep -rn "STAGE_[0-9][a-z]" templates/

# Find lowercase variants
grep -rn "s[0-9][a-z]:" templates/
```

**Automated:** ✅ Yes (pattern matching)

### Type 2: Incorrect Stage Numbers

**Pattern:**
```
Templates reference stages that were renumbered

Old workflow: S1 → S2 → S3 → S4 → S5 → S6 → S7
Renumbering: S6 → S9, S7 → S10
Current: S1 → S2 → S3 → S4 → S5 → S6 → S7 → S8 → S9 → S10

Template still says:
"After S5, proceed to S6 for testing" ← Wrong if S6 changed purpose
"S7: Epic Cleanup" ← Wrong, S7 is now different, S10 is Epic Cleanup
```

**Search Commands:**
```bash
# Extract all stage references from templates
grep -rn "S[0-9]\+:" templates/ | grep -o "S[0-9]\+:"

# Check if stage names match current stage names
# (Requires manual verification against actual guides)
```

**Automated:** ⚠️ Partial (can find stage numbers, manual to verify correctness)

### Type 3: Outdated Workflow Diagrams

**Pattern:**
```markdown
File: templates/epic_readme_template.md

## Workflow Overview

```
S1 → S2 → S3 → S4 → S5 → S6 → S7
```

[Workflow actually has S1-S10]
```

**Why This is Wrong:**
- Workflow expanded from 7 to 10 stages
- Template shows old 7-stage workflow
- New epics show incomplete workflow diagram

**Search Commands:**
```bash
# Find workflow diagrams in templates
grep -A 5 -B 5 "S1.*→.*S2" templates/

# Manually verify diagram shows all current stages
```

**Automated:** ⚠️ Partial (can find diagrams, manual to verify completeness)

### Type 4: Obsolete Section Headers

**Pattern:**
```markdown
File: templates/feature_readme_template.md

## Current Stage

**Status:** [S5a - Planning]

[Old format - current format is "S5.P1 - Planning Round 1"]
```

**Common Obsolete Sections:**
- "Current Stage: S#a" (old notation)
- "Round:" (now "Phase:")
- Old section names that changed

**Search Commands:**
```bash
# Find old section headers
grep -rn "## Current Stage" templates/ | grep -A 2 "S[0-9][a-z]"
grep -rn "## Round:" templates/

# Find sections using old terminology
grep -rn "Implementation.*Round\|Planning.*Round" templates/
```

**Automated:** ✅ Yes (pattern matching for known obsolete formats)

### Type 5: Example Content Using Old Structure

**Pattern:**
```markdown
File: templates/epic_ticket_template.md

## Example Epic Ticket

**Features:**
1. Feature 01: Player Fetcher
   - spec.md, implementation.md, tests.md

[Old structure - current structure uses implementation_plan.md and implementation_checklist.md]
```

**Why This is Wrong:**
- Example shows old file names
- Agents copy example → create wrong files
- Actual workflow uses different file names

**Search Commands:**
```bash
# Find example file references in templates
grep -rn "implementation\.md\|spec_v1\.md" templates/

# Check if example paths match current file structure
```

**Automated:** ⚠️ Partial (can find file references, manual to verify currency)

---

## How Templates Become Outdated

### Root Cause 1: Workflow Evolution Without Template Update

**Scenario:** Workflow changes during epic, templates not updated

**Timeline:**
```
2025-10: Templates created for original 7-stage workflow
2025-12: Workflow expanded to 10 stages
2026-01: S5 split into more iterations
2026-02: Templates still show 2025-10 structure
```

**Why It Happens:**
- Focus on updating guides, templates forgotten
- Templates not part of regular review
- No systematic template validation after changes

**Prevention:**
- S10.P1 includes template review
- Audit D6 validates template currency
- Templates listed in "affected files" for workflow changes

### Root Cause 2: Stage Renumbering Incomplete

**Scenario:** Stages renumbered, templates partially updated

**Renumbering Event:**
```
S6 → S9 (Epic Smoke Testing)
S7 → S10 (Epic Cleanup)
```

**Template Updates:**
```
epic_readme_template.md: Updated ✅
feature_spec_template.md: Updated ✅
epic_ticket_template.md: Not updated ❌
feature_readme_template.md: Partially updated ❌
```

**Result:** Mix of old and new stage numbers in templates

### Root Cause 3: New Fields Added, Templates Not Backfilled

**Scenario:** Workflow adds new status fields, old templates lack them

**New Requirement (2026-01):**
```
EPIC_README.md must have:
- Current Guide: [guide path]
- Guide Last Read: [timestamp]
```

**Templates:**
```
epic_readme_template.md (created 2025-10):
- Current Stage: [S#.P#]
- Last Updated: [date]

[Missing: Current Guide, Guide Last Read]
```

**Result:** New epics lack required fields

### Root Cause 4: Example Workflows Copy-Pasted From Old Epics

**Scenario:** Templates updated by copying from old epic

**What Happens:**
```bash
# Agent updates template by copying from KAI-5 (old epic)
cp KAI-5-old_epic/EPIC_README.md templates/epic_readme_template.md

# KAI-5 used old notation and old structure
# Template now has old notation
```

**Why It Happens:**
- "Use working example" approach
- Don't verify example is current
- Copy without adapting to current structure

---

## Automated Validation

### Script 1: Notation Validation in Templates (SHOULD ADD)

```bash
# CHECK: Template Currency - Notation Validation (D6)
# ============================================================================

echo "=== Template Currency - Notation Validation (D6) ==="

# Find old notation in templates
OLD_NOTATION=$(grep -rn "\bS[0-9][a-z]\b\|Stage [0-9][a-z]" templates/ | \
  grep -v "historical\|example of wrong\|Before:" | \
  wc -l)

if [ "$OLD_NOTATION" -gt 0 ]; then
  echo "⚠️  Old notation found in templates: $OLD_NOTATION instances"
  grep -rn "\bS[0-9][a-z]\b\|Stage [0-9][a-z]" templates/ | \
    grep -v "historical" | head -10
else
  echo "✅ All templates use current notation"
fi

# Find "Round" references (may be outdated)
ROUND_REFS=$(grep -rn "\bRound [0-9]\b" templates/ | \
  grep -v "QC round\|round robin\|historical" | \
  wc -l)

if [ "$ROUND_REFS" -gt 0 ]; then
  echo "⚠️  'Round N' references in templates: $ROUND_REFS"
  echo "   (Verify these should be Phase notation: S#.P#)"
fi
```

### Script 2: Stage Number Validation (SHOULD ADD)

```bash
# CHECK: Template Currency - Stage Numbers (D6)
# ============================================================================

echo "=== Template Stage Number Validation ==="

# Extract stage references from templates
TEMPLATE_STAGES=$(grep -roh "S[0-9]\+:" templates/ | sort -u)

echo "Stage references found in templates:"
echo "$TEMPLATE_STAGES"

# Check if referenced stages exist in stages/ directory
for stage_ref in $TEMPLATE_STAGES; do
  stage_num=$(echo "$stage_ref" | grep -o "[0-9]\+")
  stage_dir="stages/s$stage_num"

  if [ ! -d "$stage_dir" ]; then
    echo "⚠️  Template references $stage_ref but $stage_dir doesn't exist"
  fi
done

# Find workflow diagrams showing old structure
DIAGRAMS_WITH_S7=$(grep -l "S1.*S7" templates/)
ACTUAL_MAX_STAGE=$(ls -d stages/s* | sed 's/.*s//' | sort -n | tail -1)

if [ "$ACTUAL_MAX_STAGE" -gt 7 ] && [ -n "$DIAGRAMS_WITH_S7" ]; then
  echo "⚠️  Templates show workflow ending at S7, but stages go to S$ACTUAL_MAX_STAGE"
  echo "   Files: $DIAGRAMS_WITH_S7"
fi
```

### Script 3: Required Field Validation (SHOULD ADD)

```bash
# CHECK: Template Currency - Required Fields (D6)
# ============================================================================

echo "=== Template Required Field Validation ==="

# Check epic_readme_template has current required fields
if [ -f "templates/epic_readme_template.md" ]; then
  echo "Checking epic_readme_template.md..."

  required_fields=("Current Guide" "Guide Last Read" "Current Stage" "Next Action")

  for field in "${required_fields[@]}"; do
    if ! grep -q "$field:" templates/epic_readme_template.md; then
      echo "⚠️  Missing required field: $field"
    fi
  done
fi

# Check feature_readme_template has current fields
if [ -f "templates/feature_readme_template.md" ]; then
  echo "Checking feature_readme_template.md..."

  required_fields=("Current Guide" "Current Step" "Next Action")

  for field in "${required_fields[@]}"; do
    if ! grep -q "$field:" templates/feature_readme_template.md; then
      echo "⚠️  Missing required field: $field"
    fi
  done
fi
```

---

## Manual Validation

### Manual Currency Review Process

**For each template:**

```markdown
STEP 1: Check notation consistency
- [ ] All stage references use S#.P#.I# notation (not S5a, Stage 5a)
- [ ] No "Round N" where should be "Phase N" or "S#.P#"
- [ ] Consistent with current naming conventions

STEP 2: Verify stage numbers
- [ ] Stage numbers match current workflow (S1-S10)
- [ ] Stage names match current guide titles
- [ ] No references to old renumbered stages

STEP 3: Review workflow diagrams
- [ ] Diagrams show complete current workflow (S1-S10)
- [ ] Stage flow matches current workflow
- [ ] No outdated workflow structures

STEP 4: Check section structure
- [ ] Sections match current guide structure
- [ ] Required fields match current requirements (Agent Status, etc.)
- [ ] No obsolete sections from old workflow

STEP 5: Validate examples
- [ ] Example file paths match current structure
- [ ] Example commands use current notation
- [ ] Sample content reflects current workflow

STEP 6: Compare to actual guides
- [ ] Template structure matches actual guide structure
- [ ] Template required sections align with D11
- [ ] Template doesn't have extra obsolete sections

STEP 7: Document currency issues
- Old notation instances
- Incorrect stage numbers
- Outdated workflow diagrams
- Obsolete sections
- Example content inaccuracies
```

---

## Context-Sensitive Rules

### When Old Content in Templates is Acceptable

**1. Historical Examples (Clearly Labeled):**
```markdown
**Before v2.0 notation:**
- Stage 5a → Implementation Planning

**Current v2.0 notation:**
- S5.P1 → Implementation Planning Round 1
```
**Verdict:** ✅ ACCEPTABLE (teaching migration, clearly labeled)

**2. Comments for Template Authors:**
```markdown
<!-- Template Note: This section replaced old "Round:" notation in v2.0 -->

## Phase
```
**Verdict:** ✅ ACCEPTABLE (comment, not actual content)

### When Old Content is Error

**1. Current Workflow Instructions:**
```markdown
File: templates/epic_readme_template.md

**Current Stage:** [S6a - Testing]
```
**Verdict:** ❌ ERROR (should be S#.P# notation, not S6a)

**2. Workflow Diagrams:**
```markdown
**Workflow:**
S1 → S2 → S3 → S4 → S5 → S6 → S7
```
**Verdict:** ❌ ERROR (workflow has S1-S10, shows only S1-S7)

**3. Example File Paths:**
```markdown
**Create files:**
- feature_01/spec.md
- feature_01/implementation.md

[Current structure uses implementation_plan.md and implementation_checklist.md]
```
**Verdict:** ❌ ERROR (example file names don't match current structure)

**4. Required Fields Missing:**
```markdown
## Agent Status

**Current Stage:** [S#.P#]
**Last Updated:** [date]

[Missing: Current Guide, Guide Last Read - required fields in current workflow]
```
**Verdict:** ❌ ERROR (template missing required fields)

---

## Real Examples

### Example 1: Template Using Old Notation

**Issue Found:**
```bash
$ grep -n "S[0-9][a-z]" templates/epic_readme_template.md
234:**Current Stage:** [S5a - Planning]
456:Next: Proceed to S6a for testing
```

**Analysis:**
- Template uses old notation "S5a", "S6a"
- Current notation is "S5.P1", "S6.P1" or actual current stage names
- Every epic created from template will have old notation

**Impact:** ❌ HIGH - Error propagates to all new epics

**Fix:**
```markdown
# Before
**Current Stage:** [S5a - Planning]
Next: Proceed to S6a for testing

# After
**Current Stage:** [S5.P1 - Planning Round 1]
Next: Proceed to S6 - Execution
```

### Example 2: Workflow Diagram Outdated

**Issue Found:**
```markdown
File: templates/epic_readme_template.md

## Workflow Overview

```
S1 (Epic Planning) → S2 (Feature Planning) → S3 (Cross-Feature Check) →
S4 (Testing Strategy) → S5 (Implementation Planning) → S6 (Execution) →
S7 (Testing & Review)
```

[Actual workflow has S1-S10]
```

**Analysis:**
- Template shows 7-stage workflow
- Current workflow has 10 stages (S5-S8 is feature loop, S9-S10 added)
- Diagram incomplete

**Impact:** ⚠️ MEDIUM - Confusing, but not blocking

**Fix:**
```markdown
## Workflow Overview

```
S1 (Epic Planning) → S2 (Feature Planning) → S3 (Epic Planning Approval) →
S4 (Feature Testing Strategy) → S5-S8 (Feature Loop: Planning, Execution, Testing, Alignment) →
S9 (Epic Final QC) → S10 (Epic Cleanup)
```
```

### Example 3: Missing Required Fields

**Issue Found:**
```bash
$ grep "Current Guide:" templates/epic_readme_template.md
[No results]

$ grep "Guide Last Read:" templates/epic_readme_template.md
[No results]
```

**Analysis:**
- Current workflow requires "Current Guide" and "Guide Last Read" in Agent Status
- Template created before these fields were added
- New epics created from template will lack required fields

**Impact:** ⚠️ MEDIUM - New epics incomplete

**Fix:**
```markdown
## Agent Status

**Last Updated:** [YYYY-MM-DD HH:MM]
**Current Stage:** [S#.P#.I# notation]
**Current Step:** [What you just completed]
**Next Action:** [What you're about to do]
**Current Guide:** [feature-updates/guides_v2/path/to/guide.md]  ← ADD
**Guide Last Read:** [YYYY-MM-DD HH:MM]  ← ADD
```

### Example 4: Example File Names Outdated

**Issue Found:**
```markdown
File: templates/feature_spec_template.md

## Related Files

When creating this feature, you'll also create:
- implementation.md (detailed implementation steps)
- test_plan.md (testing approach)
- progress.md (tracking)
```

**Analysis:**
- Current workflow uses different file names:
  - implementation_plan.md (not implementation.md)
  - test_strategy.md (not test_plan.md)
  - implementation_checklist.md (not progress.md)
- Template examples don't match current structure

**Impact:** ⚠️ MEDIUM - Confusing naming

**Fix:**
```markdown
## Related Files

When creating this feature, you'll also create:
- implementation_plan.md (detailed implementation steps, ~400 lines)
- implementation_checklist.md (progress tracking)
- test_strategy.md (created in S4, referenced in S5)
- lessons_learned.md (created in S7.P3)
```

### Example 5: Stage Number References Incorrect

**Issue Found:**
```markdown
File: templates/feature_readme_template.md

## Workflow Position

**Before this feature:** S1, S2, S3 complete
**Current:** S4 (Implementation Planning)
**After this feature:** S5 (Testing), S6 (Epic QC), S7 (Cleanup)
```

**Analysis:**
- Says "S4 (Implementation Planning)" but S4 is Testing Strategy, S5 is Planning
- Says "S5 (Testing)" but S7 is Testing
- Stage numbers don't match current workflow

**Impact:** ❌ HIGH - Completely incorrect stage mapping

**Fix:**
```markdown
## Workflow Position

**Before this feature:** S1-S4 complete (Epic planning, Feature planning, Epic approval, Testing strategy)
**Current:** S5 (Implementation Planning) → S6 (Execution) → S7 (Testing) → S8 (Alignment)
**After this feature:** Repeat S5-S8 for next feature OR S9 (Epic QC) → S10 (Cleanup)
```

---

## Integration with Other Dimensions

**Works With:**
- **D1: Cross-Reference Accuracy** - Template file references must be valid
- **D2: Terminology Consistency** - Templates must use current notation

**Complementary:**
- **D11: Structural Patterns** - Template structure should match current patterns
- **D14: Content Accuracy** - Template stage numbers and counts must be accurate

**Difference from Other Dimensions:**
- **D6:** Template-specific currency issues
- **D1/D2:** Apply to all files (including templates)
- **D6 Focus:** Template as source of propagated errors

---

## See Also

**Related Dimensions:**
- `d1_cross_reference_accuracy.md` - Validate template file paths
- `d2_terminology_consistency.md` - Validate template notation
- `d11_structural_patterns.md` - Template structure patterns
- `d14_content_accuracy.md` - Template content accuracy

**Audit Stages:**
- `../stages/stage_1_discovery.md` - How to discover template currency issues
- `../stages/stage_4_verification.md` - Verify templates after fixes

**Workflow Integration:**
- `../stages/s10/s10_p1_guide_update_workflow.md` - Template review in S10.P1

---

**When to Use:** Run D6 validation after any workflow changes (stage renumbering, new stages added, notation changes) and during regular audits. Template errors multiply across all new epics - fix templates to prevent error propagation.
