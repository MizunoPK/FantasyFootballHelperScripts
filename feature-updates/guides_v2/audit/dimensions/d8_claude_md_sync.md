# D8: CLAUDE.md Synchronization

**Dimension Number:** 8
**Category:** Core Dimensions (Always Check)
**Automation Level:** 60% automated
**Priority:** HIGH
**Last Updated:** 2026-02-04

**Focus:** Ensure root CLAUDE.md file stays synchronized with guides_v2 folder content and structure
**Typical Issues Found:** 5-15 per major workflow change

---

## Table of Contents

1. [What This Checks](#what-this-checks)
2. [Why This Matters](#why-this-matters)
3. [Pattern Types](#pattern-types)
4. [How Desync Happens](#how-desync-happens)
5. [Automated Validation](#automated-validation)
6. [Manual Validation](#manual-validation)
7. [Context-Sensitive Rules](#context-sensitive-rules)
8. [Real Examples](#real-examples)

---

## What This Checks

**CLAUDE.md Synchronization** validates that the root project instructions file (`CLAUDE.md`) accurately reflects the guides_v2 system:

✅ **File Path References:**
- All paths mentioned in CLAUDE.md exist in guides_v2/
- Stage guide references point to correct files
- Template references are current
- Reference material paths are accurate

✅ **Workflow Descriptions:**
- Stage names match between CLAUDE.md and guide files
- Stage purposes align with actual guide content
- Prerequisites listed match guide prerequisites
- Output descriptions match template formats

✅ **Notation Consistency:**
- S#.P#.I# notation used consistently
- Stage numbering matches actual guide structure
- Phase and iteration numbers are correct

✅ **Key Concept Alignment:**
- Exit criteria in CLAUDE.md match stage_5
- Fresh Eyes concept matches audit_overview
- Gate descriptions match reference/mandatory_gates.md
- Terminology matches reference/glossary.md

✅ **Quick Reference Accuracy:**
- Stage workflow quick reference matches detailed guides
- Duration estimates align with guide estimates
- First action prompts match prompts_reference_v2.md

---

## Why This Matters

### Impact of Desynchronization

**Critical Impact:**
- **Agent Confusion:** CLAUDE.md says "Read X", but X doesn't exist or is wrong
- **Workflow Mismatch:** Quick reference doesn't match detailed guide (agent follows wrong path)
- **Outdated Instructions:** CLAUDE.md describes old workflow after guide updates
- **Trust Erosion:** Inconsistencies between "official" instructions and actual guides

**Example Failure (Hypothetical):**
```text
CLAUDE.md: "S5: Implementation Planning (28 iterations, 3 rounds)" (outdated as of 2026-02-04)
Reality: S5 has 22 iterations across 3 rounds (as of 2026-02-04, testing moved to S4)
Result: Agent expects 28 iterations, looks for I23-I28 which don't exist
```markdown

### Why CLAUDE.md Drifts

**Root Cause:** CLAUDE.md is read by agents on EVERY task, but only updated during S10.P1 (Epic Cleanup)

**Drift Pattern:**
1. Guide change happens mid-epic (e.g., S5 expanded from 15→22 iterations)
2. Current epic uses updated guides
3. CLAUDE.md not updated until S10.P1
4. Next epic starts, reads outdated CLAUDE.md
5. Confusion or incorrect workflow followed

**Solution:** D8 audits catch drift before it impacts new epics

---

## Pattern Types

### Type 1: File Path References

**What to Check:**
- All `feature-updates/guides_v2/` paths mentioned in CLAUDE.md
- Stage guide paths: `stages/sN/file.md`
- Template paths: `templates/file.md`
- Reference paths: `reference/file.md`

**Search Command:**
```bash
# Extract all guides_v2 file paths from CLAUDE.md
grep -n "feature-updates/guides_v2/" CLAUDE.md | \
  grep -o "feature-updates/guides_v2/[^)\"' ]*\.md" | \
  sort -u > /tmp/claude_paths.txt

# Verify each path exists
while read path; do
  full_path="${path#feature-updates/guides_v2/}"
  if [ ! -f "feature-updates/guides_v2/$full_path" ]; then
    echo "BROKEN: $path (referenced in CLAUDE.md)"
  fi
done < /tmp/claude_paths.txt
```

**Automated:** ✅ Yes (file existence check)

---

### Type 2: Stage Quick Reference Table

**What to Check:**
- Stage numbers (S1-S10)
- Stage names match guide titles
- Guide file paths are correct
- "Next" stage is correct
- Duration estimates align

**Location in CLAUDE.md:**
```markdown
## Stage Workflows Quick Reference

**S1: Epic Planning**
- **Guide:** `stages/s1/s1_epic_planning.md`
- **Next:** S2
```markdown

**Manual Check Required:**
1. Read CLAUDE.md Stage Workflows section
2. For each stage, verify:
   - Guide path exists
   - Guide title matches CLAUDE.md stage name
   - "Next" field points to correct successor
   - Duration estimate matches guide's estimated duration

**Automated:** ⚠️ Partial (path check automated, content match manual)

---

### Type 3: Gate Numbering

**What to Check:**
- Gate numbers in CLAUDE.md match reference/mandatory_gates.md
- Gate locations correct (which stage/phase)
- Gate types correct (user approval vs agent checklist)

**Search Command:**
```bash
# Extract gate numbers from CLAUDE.md
grep -n "Gate [0-9]" CLAUDE.md | grep -o "Gate [0-9a-z.]*"

# Compare with reference/mandatory_gates.md
grep -n "Gate [0-9]" feature-updates/guides_v2/reference/mandatory_gates.md | \
  grep -o "Gate [0-9a-z.]*"

# Look for discrepancies
```

**Manual Check:**
- Compare gate descriptions between CLAUDE.md and mandatory_gates.md
- Verify gate locations match (e.g., Gate 5 in S5, not S6)

**Automated:** ⚠️ Partial (number extraction, but descriptions manual)

---

### Type 4: Workflow Descriptions

**What to Check:**
- Stage purposes match guide purposes
- Key outputs match guide outputs
- Prerequisites match guide prerequisites
- Critical principles aligned

**Example Check:**
```markdown
CLAUDE.md: "S5: Implementation Planning (22 iterations, 3 rounds)"
          ↓ Should match ↓
stages/s5/s5_implementation_planning.md: "22 iterations across 3 rounds"
```markdown

**Manual Check Required:**
1. Read CLAUDE.md workflow description for each stage
2. Read corresponding stage guide's Overview/Purpose section
3. Verify alignment on:
   - Stage purpose
   - Duration
   - Input/Output
   - Key principles
   - Critical gates

**Automated:** ❌ No (semantic comparison required)

---

### Type 5: Notation Examples

**What to Check:**
- S#.P#.I# notation examples in CLAUDE.md
- Examples should reflect actual guide structure
- Notation system description matches glossary

**Search Command:**
```bash
# Find notation examples in CLAUDE.md
grep -n "S[0-9]\.P[0-9]" CLAUDE.md

# Find notation examples in glossary
grep -n "S[0-9]\.P[0-9]" feature-updates/guides_v2/reference/glossary.md

# Look for inconsistent usage
```

**Manual Check:**
- Verify notation examples are correct (e.g., S5.P1.I2 actually exists)
- Check notation system description matches glossary

**Automated:** ⚠️ Partial (pattern extraction, but correctness manual)

---

### Type 6: Template References

**What to Check:**
- Template file paths in CLAUDE.md exist
- Template purposes match CLAUDE.md descriptions
- Template output formats match stage guide expectations

**Search Command:**
```bash
# Extract template references from CLAUDE.md
grep -n "templates/" CLAUDE.md | \
  grep -o "templates/[^)\"' ]*\.md"

# Verify existence
for template in $(cat /tmp/template_refs.txt); do
  if [ ! -f "feature-updates/guides_v2/$template" ]; then
    echo "MISSING: $template"
  fi
done
```markdown

**Manual Check:**
- Read template descriptions in CLAUDE.md
- Open actual template files
- Verify descriptions match template content

**Automated:** ✅ Partial (existence automated, content manual)

---

## How Desync Happens

### Scenario 1: Guide Update Without CLAUDE.md Update

**Trigger:** Mid-epic guide improvement (e.g., adding new phase to S5)

**Timeline:**
1. Epic in progress, discover S5 needs more iterations
2. Update S5 guides: 15 iterations → 22 iterations
3. Current epic uses updated 28-iteration process
4. Forget to update CLAUDE.md (still says 15 iterations)
5. Next epic starts, reads CLAUDE.md, thinks 15 iterations

**Prevention:** D8 audit after any guide changes

---

### Scenario 2: Stage Renumbering

**Trigger:** Workflow evolution (e.g., S5 split into S5-S8, S6→S9)

**Timeline:**
1. Major workflow restructure decided
2. Create new stage guides (S5, S6, S7, S8 for feature loop)
3. Renumber old S6→S9, S7→S10
4. Update all guides with new stage numbers
5. Miss some references in CLAUDE.md quick reference
6. CLAUDE.md says "Next: S6" but should say "Next: S9"

**Prevention:** D1 (Cross-Reference) + D8 (CLAUDE.md Sync) audits

---

### Scenario 3: Template Addition/Removal

**Trigger:** New workflow requires new template

**Timeline:**
1. Add round_summary_template.md for Stage 5 output
2. Update stage_5 guide to reference new template
3. Update template/ README with new template
4. Forget to mention new template in CLAUDE.md
5. CLAUDE.md workflow description outdated (doesn't mention template)

**Prevention:** D8 audit catches missing template mention

---

### Scenario 4: Concept Evolution

**Trigger:** Clarification of key concept (e.g., "Fresh Eyes")

**Timeline:**
1. Discover "Fresh Eyes" concept needs operational definition
2. Add 150+ line guide to audit_overview.md
3. Update stage_5 exit criteria to reference Fresh Eyes guide
4. CLAUDE.md still has vague "Fresh Eyes" mention without details
5. Agents read CLAUDE.md, don't realize detailed guide exists

**Prevention:** D8 audit ensures CLAUDE.md points to new resources

---

## Automated Validation

### Script 1: File Path Validation

**Purpose:** Check all paths mentioned in CLAUDE.md exist

```bash
#!/bin/bash
# Check CLAUDE.md paths

echo "Extracting paths from CLAUDE.md..."
grep -oh "feature-updates/guides_v2/[^)\"' ]*\.md" CLAUDE.md | \
  sort -u > /tmp/claude_paths.txt

echo "Verifying paths exist..."
broken_count=0
while read path; do
  if [ ! -f "$path" ]; then
    echo "❌ BROKEN: $path"
    ((broken_count++))
  fi
done < /tmp/claude_paths.txt

if [ $broken_count -eq 0 ]; then
  echo "✅ All paths valid ($( wc -l < /tmp/claude_paths.txt ) paths checked)"
else
  echo "❌ Found $broken_count broken paths"
fi
```

**Coverage:** ~60% of D8 issues

---

### Script 2: Stage Number Consistency

**Purpose:** Check stage numbers referenced match actual structure

```bash
#!/bin/bash
# Check stage number consistency

echo "Checking stage references in CLAUDE.md..."

# Extract stage references (S1-S10, S#.P#, S#.P#.I#)
grep -oh "S[0-9][0-9]*\(\.P[0-9][0-9]*\)\?\(\.I[0-9][0-9]*\)\?" CLAUDE.md | \
  sort -u > /tmp/claude_stages.txt

# Check if stage folders exist
for stage_ref in $(cat /tmp/claude_stages.txt); do
  stage_num=$(echo $stage_ref | grep -o "^S[0-9]*" | sed 's/S//')
  stage_dir="feature-updates/guides_v2/stages/s$stage_num"

  if [ ! -d "$stage_dir" ]; then
    echo "❌ MISSING: Stage $stage_ref folder not found: $stage_dir"
  fi
done

echo "✅ Stage reference check complete"
```bash

**Coverage:** ~20% of D8 issues

---

### Integration with pre_audit_checks.sh

**Add to master script:**

```bash
echo ""
echo "=== D8: CLAUDE.md Synchronization ==="
echo ""

# Check file paths
bash scripts/check_claude_paths.sh

# Check stage consistency
bash scripts/check_claude_stages.sh

# Manual checks reminder
echo ""
echo "⚠️  MANUAL CHECKS REQUIRED:"
echo "  - Workflow descriptions match guide content"
echo "  - Gate numbering matches mandatory_gates.md"
echo "  - Duration estimates align with guides"
echo "  - Key concepts aligned (Fresh Eyes, exit criteria, etc.)"
```

---

## Manual Validation

### Checklist: CLAUDE.md Sync Validation

**Perform these checks manually (cannot be automated):**

#### Section 1: File Structure Reference

- [ ] Read CLAUDE.md section "Workflow Guides Location"
- [ ] Verify folder structure diagram matches actual structure
- [ ] Check all folder names correct (stages/, reference/, templates/, etc.)
- [ ] Verify "All guides location" path is correct

---

#### Section 2: Stage Workflows Quick Reference

**For EACH stage (S1-S10):**

- [ ] Stage name in CLAUDE.md matches guide file title
- [ ] Guide path exists and is correct
- [ ] "First Action" prompt matches prompts_reference_v2.md
- [ ] "Actions" list matches guide's Overview/Purpose
- [ ] "Next" stage is correct
- [ ] Duration estimate aligns with guide estimate

**How to Check:**
1. Open CLAUDE.md Stage Workflows section
2. Open corresponding stage guide
3. Compare side-by-side for alignment

---

#### Section 3: Gate Numbering

- [ ] Read CLAUDE.md "Gate Numbering System" section
- [ ] Read reference/mandatory_gates.md
- [ ] Verify gate list matches (Gate 1, 2, 3, 4.5, 5, 4a, 7a, 23a, 24, 25)
- [ ] Verify gate locations match (which stage each gate occurs in)
- [ ] Verify gate types match (user approval vs agent checklist)

---

#### Section 4: Key Concepts

**Fresh Eyes:**
- [ ] CLAUDE.md mentions Fresh Eyes
- [ ] References audit_overview.md for operational guide
- [ ] Aligns with audit philosophy

**Exit Criteria:**
- [ ] CLAUDE.md mentions exit criteria
- [ ] References stage_5_loop_decision.md as source
- [ ] Doesn't duplicate detailed criteria (single source of truth)

**Minimum 3 Rounds:**
- [ ] CLAUDE.md uses "minimum 3 rounds as baseline" phrasing
- [ ] Consistent with audit guides' messaging
- [ ] No contradictions (e.g., "exactly 3 rounds")

---

#### Section 5: Workflow Descriptions

**For Epic-Driven Workflow:**

- [ ] CLAUDE.md describes 10-stage workflow (S1-S10)
- [ ] Stage purposes match guide purposes
- [ ] Feature loop (S5-S8) described correctly
- [ ] Parallel work mention (if applicable) matches parallel_work/ guides

**For Special Workflows:**

- [ ] Missed Requirement Protocol matches missed_requirement/ guides
- [ ] Debugging Protocol matches debugging/ guides
- [ ] Protocol Decision Tree matches PROTOCOL_DECISION_TREE.md

---

#### Section 6: Template References

- [ ] CLAUDE.md mentions key templates
- [ ] Template paths are correct
- [ ] Template purposes match actual template content
- [ ] No references to deleted templates

---

#### Section 7: Notation System

- [ ] CLAUDE.md notation section matches reference/glossary.md
- [ ] S#.P#.I# examples are correct (reflect actual structure)
- [ ] Terminology definitions aligned with glossary

---

### Validation Process

**Step 1: Automated Checks (10 minutes)**
```bash
# Run automated scripts
bash feature-updates/guides_v2/audit/scripts/pre_audit_checks.sh | \
  grep -A 20 "D8: CLAUDE.md"
```markdown

**Step 2: Manual Checks (20-30 minutes)**
- Work through checklist above systematically
- Document any mismatches found
- Categorize by severity

**Step 3: Document Issues**
- Use discovery_report_template.md
- Tag with Dimension: D8
- Provide before/after for each issue

---

## Context-Sensitive Rules

### Rule 1: Historical Examples Are Intentional

**Pattern:** CLAUDE.md may reference old stage numbers in examples

**Context Check:**
```markdown
Example: "In KAI-6, we discovered S5 needed expansion..."
```

**This is OK if:**
- Clearly labeled as historical example
- Context makes it clear this is past state
- Used for lessons learned

**This is ERROR if:**
- Not labeled as example
- Presented as current instruction
- Could confuse agent about current structure

---

### Rule 2: Quick Reference vs Detailed

**CLAUDE.md Quick Reference is ALLOWED to be:**
- Shorter than detailed guide
- Higher-level overview
- Missing some details

**But MUST be:**
- Accurate (no contradictions with guides)
- Point to detailed guide for full info
- Consistent in key facts (stage count, gate count, etc.)

**Example - Acceptable:**
```markdown
CLAUDE.md: "S5: Implementation Planning (22 iterations)"
Guide: "S5: Implementation Planning (22 iterations across 3 rounds:
        Round 1 (7 iterations), Round 2 (6 iterations), Round 3 (9 iterations))"
```markdown
CLAUDE.md simplified but accurate ✅

**Example - Error:**
```markdown
CLAUDE.md: "S5: Implementation Planning (15 iterations)"
Guide: "S5: Implementation Planning (22 iterations)"
```
CLAUDE.md contradicts guide ❌

---

### Rule 3: Workflow Evolution Mentions

**CLAUDE.md may mention workflow history:**
```markdown
"The workflow evolved from 7 stages to 10 stages in version 2..."
```markdown

**This is OK** - provides context for users

**But check:**
- History is accurate
- Current workflow clearly distinguished from past
- No confusion about which workflow to follow NOW

---

## Real Examples

### Example 1: Broken Path Reference

**Issue:**
```markdown
# CLAUDE.md (line 123)
**S5 Guide:** `stages/s5/round1/s5_p1_round1.md`
```

**Problem:** File moved during restructure
**Actual location:** `stages/s5/s5_p1_planning_round1.md`

**Fix:**
```markdown
**S5 Guide:** `stages/s5/s5_p1_planning_round1.md`
```markdown

**How Found:** Automated path validation script

---

### Example 2: Outdated Iteration Count

**Issue:**
```markdown
# CLAUDE.md Stage Workflows
**S5: Implementation Planning**
- **Actions:** 15 verification iterations
```

**Problem:** S5 changed from 28 to 22 iterations (testing moved to S4)
**Actual:** S5 has 22 iterations across 3 rounds

**Fix:**
```markdown
**S5: Implementation Planning**
- **Actions:** 22 verification iterations across 3 rounds
```markdown

**How Found:** Manual comparison of CLAUDE.md vs s5_implementation_planning.md

---

### Example 3: Wrong "Next" Stage

**Issue:**
```markdown
# CLAUDE.md Stage Workflows
**S5: Implementation Planning**
- **Next:** S6
```

**Problem:** After workflow restructure, S5 loops to S6→S7→S8→(S5 or S9)
**Actual:** S5 next is S6 (correct for first feature), but should clarify loop

**Fix:**
```markdown
**S5: Implementation Planning**
- **Next:** S6 (then S7, S8, repeat S5-S8 for each feature, or S9 when all features done)
```diff

**How Found:** Manual workflow trace

---

### Example 4: Missing Template Mention

**Issue:**
```markdown
# CLAUDE.md Templates Section
- spec.md
- checklist.md
- implementation_plan.md
- implementation_checklist.md
```

**Problem:** Missing round_summary_template.md (added to Stage 5)
**Actual:** Stage 5 now outputs round summary using template

**Fix:**
```markdown
# CLAUDE.md Templates Section
- spec.md
- checklist.md
- implementation_plan.md
- implementation_checklist.md
- round_summary.md (Stage 5 output)
```

**How Found:** Cross-checking templates/ folder vs CLAUDE.md mentions

---

## Integration with Other Dimensions

### Works With D1 (Cross-Reference Accuracy)

**Overlap:** Both check file paths

**Difference:**
- D1: Checks paths WITHIN guides_v2 folder
- D8: Checks paths FROM CLAUDE.md TO guides_v2 folder

**Workflow:**
1. Run D1 first (validate guides_v2 internal consistency)
2. Run D8 second (validate CLAUDE.md points to correct guides_v2 files)

---

### Works With D2 (Terminology Consistency)

**Overlap:** Both check notation usage

**Difference:**
- D2: Checks S#.P#.I# notation within guides
- D8: Checks CLAUDE.md notation matches guides notation

**Workflow:**
1. Run D2 first (standardize notation in guides)
2. Run D8 second (ensure CLAUDE.md uses same notation)

---

### Works With D6 (Template Currency)

**Overlap:** Both check template references

**Difference:**
- D6: Checks templates match guide expectations
- D8: Checks CLAUDE.md describes templates correctly

**Workflow:**
1. Run D6 first (validate templates are current)
2. Run D8 second (ensure CLAUDE.md template descriptions match)

---

## When to Focus on D8

### High Priority Scenarios

**Trigger 1: After S10.P1 Guide Updates**
- S10.P1 is when guides are updated based on lessons learned
- CLAUDE.md should be updated in parallel
- D8 validates synchronization

**Trigger 2: After Workflow Evolution**
- Major workflow changes (e.g., 7→10 stages)
- Stage renumbering
- New stages added

**Trigger 3: Before New Epic Starts**
- Agents read CLAUDE.md first
- Outdated CLAUDE.md = wrong workflow followed
- Quick D8 check prevents misdirection

**Trigger 4: After Template Changes**
- New templates added
- Templates renamed or moved
- Template formats changed

---

### Low Priority Scenarios

**Skip D8 if:**
- No guide changes recently
- Mid-epic (CLAUDE.md won't be read until next epic)
- Only minor guide updates (typo fixes, clarifications)

---

## Severity Classification

### Critical: Broken Workflow

**Examples:**
- Wrong stage guide path (agent can't find file)
- Wrong "Next" stage (workflow broken)
- Missing gate (critical check skipped)

**Impact:** Blocks agent progress

**Fix Priority:** Immediate

---

### High: Misleading Description

**Examples:**
- Wrong iteration count (agent thinks they're done early)
- Wrong duration estimate (user expectations wrong)
- Outdated workflow description

**Impact:** Causes confusion, possible workflow errors

**Fix Priority:** Same round

---

### Medium: Incomplete Reference

**Examples:**
- Missing template mention
- Missing reference guide
- No pointer to new feature

**Impact:** Agent misses useful resource

**Fix Priority:** Same round

---

### Low: Cosmetic Inconsistency

**Examples:**
- Slightly different phrasing (but same meaning)
- Example uses old notation (but clearly labeled)
- Historical reference could be clearer

**Impact:** Minimal

**Fix Priority:** Next round or defer

---

## See Also

**Related Dimensions:**
- `d1_cross_reference_accuracy.md` - File path validation within guides
- `d2_terminology_consistency.md` - Notation standardization
- `d6_template_currency.md` - Template synchronization

**Stage Guides:**
- `../stages/s10/s10_p1_guide_update_workflow.md` - When CLAUDE.md should be updated

**Reference:**
- `../reference/glossary.md` - Terminology source of truth
- `../reference/mandatory_gates.md` - Gate numbering source of truth

---

**After reviewing D8:**
- Run automated scripts first (60% coverage)
- Complete manual checklist (remaining 40%)
- Document all mismatches found
- Prioritize fixes by severity
- Update CLAUDE.md to restore sync

**Remember:** CLAUDE.md is the entry point for all agents. Accuracy here prevents workflow confusion downstream.
