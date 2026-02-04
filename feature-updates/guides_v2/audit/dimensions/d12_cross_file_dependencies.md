# D12: Cross-File Dependencies

**Dimension Number:** 12
**Category:** Structural Dimensions
**Automation Level:** 30% automated
**Priority:** HIGH
**Last Updated:** 2026-02-04

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

**D12: Cross-File Dependencies** validates that files correctly reference and depend on each other at RUNTIME (not just documentation):

1. **Stage Handoff Files** - Outputs from Stage A actually exist and match Stage B input expectations
2. **Cross-Stage References** - spec.md references DISCOVERY.md findings, implementation_plan.md references spec.md requirements
3. **Template Dependencies** - Templates reference files that exist in real workflow
4. **Import/Include Validation** - Guides that say "see file X" actually have file X available
5. **Prerequisite File Existence** - Files listed in Prerequisites sections actually get created by previous stages
6. **Dependency Graph Completeness** - No circular dependencies, no missing links in chain

**Coverage:**
- Stage-to-stage handoff files (DISCOVERY.md, spec.md, test_strategy.md, implementation_plan.md, etc.)
- Template references to workflow files
- Cross-references between guides
- Root-level files referencing sub-guides

**Key Distinction from D3:**
- **D3 (Workflow Integration):** Validates DOCUMENTATION says correct prerequisites and transitions
- **D12 (Cross-File Dependencies):** Validates files ACTUALLY EXIST at runtime matching documentation

---

## Why This Matters

**Missing dependencies = Workflow breaks at runtime**

### Impact of Dependency Errors:

**Missing Handoff Files:**
- Stage B expects file from Stage A, file doesn't exist
- Agent blocked, cannot proceed
- Manual intervention required
- Example: S5 expects test_strategy.md from S4, but S4 was skipped → S5 cannot start

**Incorrect File References:**
- spec.md says "see DISCOVERY.md Section 3.2"
- DISCOVERY.md has no Section 3.2
- Agent confused about where to find information
- Example: spec.md references DISCOVERY findings that don't exist

**Circular Dependencies:**
- File A requires File B complete first
- File B requires File A complete first
- Deadlock situation
- Example: S2 checklist says "see spec.md", spec.md says "see checklist.md first"

**Orphaned Files:**
- File created but no stage uses it
- Wasted effort creating unused files
- Confusion about file purpose
- Example: S4 creates feature_requirements.md, but no stage reads it

**Template Propagation Errors:**
- Template references "see implementation_checklist.md"
- But implementation_checklist.md not created until S6
- Every new epic hits this error
- Example: spec.md template says "refer to test_plan.md" but workflow creates test_strategy.md

### Historical Evidence:

**KAI-7 Issues:**
- S5 guide said "merge test_strategy.md" but file sometimes missing (S4 skipped)
- spec.md template referenced DISCOVERY.md sections that didn't exist in actual DISCOVERY.md structure
- Templates had "see X.md" references where X.md was never created in workflow

**Why 30% Automation:**
- Automated: File existence checks, basic reference validation
- Manual Required: Semantic matching (does content of output actually satisfy input needs?), dependency graph analysis

---

## Pattern Types

### Type 0: Root-Level File Cross-References (CRITICAL - Often Missed)

**Files to Always Check:**
```
feature-updates/guides_v2/README.md
feature-updates/guides_v2/EPIC_WORKFLOW_USAGE.md
feature-updates/guides_v2/prompts_reference_v2.md
C:\Users\kmgam\code\FantasyFootballHelperScripts\CLAUDE.md
```

**What to Validate:**

**README.md:**
- [ ] References to stage guides point to files that exist
- [ ] "See also" references point to existing files
- [ ] Template links point to existing templates
- [ ] Reference links point to existing reference files

**EPIC_WORKFLOW_USAGE.md:**
- [ ] Stage guide paths are correct and files exist
- [ ] Template examples reference existing templates
- [ ] Cross-references to other guides exist

**CLAUDE.md:**
- [ ] Stage Workflows section references existing stage guides
- [ ] Reference links point to existing files in guides_v2/
- [ ] No broken links to moved/renamed files

**Search Commands:**
```bash
# Extract all file references from root files
cd feature-updates/guides_v2
grep -oE '\`[^`]+\.md\`' README.md EPIC_WORKFLOW_USAGE.md prompts_reference_v2.md

# Check each reference exists
for ref in $(grep -oE '\`[^`]+\.md\`' README.md | tr -d '`'); do
  if [ ! -f "$ref" ]; then
    echo "BROKEN REFERENCE in README.md: $ref"
  fi
done

# Check CLAUDE.md references
cd ../..
grep -oE 'feature-updates/guides_v2/[^)]+\.md' CLAUDE.md | while read ref; do
  if [ ! -f "$ref" ]; then
    echo "BROKEN REFERENCE in CLAUDE.md: $ref"
  fi
done
```

**Red Flags:**
- README.md references "stages/s4/s4_testing.md" but file is "s4_feature_testing_strategy.md"
- CLAUDE.md references "guides_v2/old_guide.md" that was deleted
- prompts_reference_v2.md references prompt files that don't exist

**Automated:** ⚠️ Partial (can check file existence, cannot validate semantic match)

---

### Type 1: Stage Handoff File Dependencies

**What to Check:**
Critical files passed from one stage to the next must exist at the right time.

**Dependency Chain (S1 → S10):**

```
S1 → DISCOVERY.md
     ↓
S2 → spec.md, checklist.md, RESEARCH_NOTES.md (per feature)
     ↓
S3 → epic_smoke_test_plan.md, refined EPIC_README.md
     ↓
S4 → test_strategy.md (per feature)
     ↓
S5 → implementation_plan.md (per feature, merges test_strategy.md)
     ↓
S6 → implementation_checklist.md (per feature), implemented code
     ↓
S7 → lessons_learned.md (per feature), committed feature
     ↓
S8 → Updated specs (remaining features)
     ↓
S9 → Epic testing report
     ↓
S10 → PR, updated EPIC_TRACKER.md
```

**Validation Commands:**

```bash
# Check S1 → S2 handoff
epic_dir="feature-updates/KAI-N-name"
if [ ! -f "$epic_dir/DISCOVERY.md" ]; then
  echo "ERROR: S1 did not create DISCOVERY.md"
fi

# Check S2 → S3 handoff (all features must have spec.md)
for feature_dir in $epic_dir/feature_*; do
  if [ ! -f "$feature_dir/spec.md" ]; then
    echo "ERROR: S2 did not create spec.md for $(basename $feature_dir)"
  fi
  if [ ! -f "$feature_dir/checklist.md" ]; then
    echo "ERROR: S2 did not create checklist.md for $(basename $feature_dir)"
  fi
done

# Check S3 → S4 handoff
if [ ! -f "$epic_dir/epic_smoke_test_plan.md" ]; then
  echo "ERROR: S3 did not create epic_smoke_test_plan.md"
fi

# Check S4 → S5 handoff
if [ ! -f "$feature_dir/test_strategy.md" ]; then
  echo "ERROR: S4 did not create test_strategy.md"
fi

# Check S5 → S6 handoff
if [ ! -f "$feature_dir/implementation_plan.md" ]; then
  echo "ERROR: S5 did not create implementation_plan.md"
fi

# Check S6 → S7 handoff
if [ ! -f "$feature_dir/implementation_checklist.md" ]; then
  echo "ERROR: S6 did not create implementation_checklist.md"
fi

# Check S7 → S8 handoff
if [ ! -f "$feature_dir/lessons_learned.md" ]; then
  echo "ERROR: S7 did not create lessons_learned.md"
fi
```

**Red Flags:**
- File expected but not created by previous stage
- File created but never used by subsequent stage (orphaned)
- File created with different name than expected
- File created in wrong location (epic root vs feature folder)

**Automated:** ✅ Yes (can validate file existence in expected locations)

---

### Type 2: Intra-Document Cross-References

**What to Check:**
When one document references another document's sections, those sections must exist.

**Common Patterns:**

**spec.md references DISCOVERY.md:**
```markdown
## Background

From epic discovery (see DISCOVERY.md Section 3: Technical Constraints),
we identified that...
```

**Validation:**
- [ ] DISCOVERY.md has "Section 3: Technical Constraints"
- [ ] Section contains content referenced in spec.md

**implementation_plan.md references spec.md:**
```markdown
## Implementation Approach

Per spec.md Section 5: Acceptance Criteria, we must implement...
```

**Validation:**
- [ ] spec.md has "Section 5: Acceptance Criteria"
- [ ] Criteria listed in spec.md match what implementation_plan.md describes

**Search Commands:**

```bash
# Find all cross-document references in spec.md
grep -n "see [A-Z_]*\.md\|refer to [A-Z_]*\.md\|per [A-Z_]*\.md" feature_*/spec.md

# Extract referenced sections
grep -oE "Section [0-9]+:?[^,)]*" feature_*/spec.md

# For each reference, validate section exists in target document
# (Manual validation required)
```

**Red Flags:**
- spec.md says "see DISCOVERY.md Section 4" but DISCOVERY.md only has 3 sections
- implementation_plan.md says "per spec.md Section 8" but spec.md Section 8 is about something different
- Cross-reference uses old section number (DISCOVERY.md was reorganized)

**Automated:** ❌ No (requires semantic validation of section content)

---

### Type 3: Template File References

**What to Check:**
Templates used to create new epics/features must reference files that exist in real workflow.

**Templates to Validate:**
```
templates/epic_readme_template.md
templates/feature_spec_template.md
templates/checklist_template.md
templates/implementation_plan_template.md
templates/discovery_template.md
```

**Validation Process:**

```bash
# Find all file references in templates
grep -rn "see.*\.md\|refer to.*\.md\|\`.*\.md\`" templates/

# For each reference, check if file exists in guides_v2
for ref in $(grep -oE '\`[^`]+\.md\`' templates/*.md | tr -d '`'); do
  if [ ! -f "feature-updates/guides_v2/$ref" ] && [ ! -f "$ref" ]; then
    echo "BROKEN REFERENCE in template: $ref"
  fi
done
```

**Common Template Errors:**

**spec.md template:**
```markdown
## Background

See DISCOVERY.md for full context.

## Technical Approach

Refer to implementation_checklist.md for build steps.
```

**Problems:**
- ✅ DISCOVERY.md reference is VALID (exists when spec.md created)
- ❌ implementation_checklist.md reference is INVALID (doesn't exist until S6, spec.md created in S2)

**Fix:**
```diff
## Technical Approach

-Refer to implementation_checklist.md for build steps.
+Refer to implementation_plan.md (created in S5) for build steps.
```

**Red Flags:**
- Template references file created AFTER template is instantiated
- Template references old filename (test_plan.md instead of test_strategy.md)
- Template references file that never gets created in workflow
- Template says "see X.md Section 4" but X.md structure doesn't have numbered sections

**Automated:** ⚠️ Partial (can check file existence, cannot validate timing/semantic correctness)

---

### Type 4: Guide Import/Include References

**What to Check:**
Guides that say "for details, see X.md" must have X.md available and accessible.

**Common Pattern:**

**Stage router file:**
```markdown
# S5: Implementation Planning

For detailed iteration guides, see:
- Round 1: `stages/s5/s5_p1_planning_round1.md`
- Round 2: `stages/s5/s5_p2_planning_round2.md`
- Round 3: `stages/s5/s5_p3_planning_round3.md`
```

**Validation:**
- [ ] All 3 files exist at specified paths
- [ ] Files are not empty/stub
- [ ] Files contain expected content (not placeholder)

**Search Commands:**

```bash
# Find all "see X.md" references in guides
grep -rn "see \`.*\.md\`\|See \`.*\.md\`" stages/ reference/

# Extract file paths and validate existence
for file in $(grep -oE '\`stages/[^`]+\.md\`' stages/**/*.md | tr -d '`'); do
  if [ ! -f "feature-updates/guides_v2/$file" ]; then
    echo "BROKEN INCLUDE: $file"
  fi
done
```

**Red Flags:**
- Guide says "see detailed_guide.md" but file doesn't exist
- Guide references "stages/s5/s5_phase1.md" but actual file is "s5_p1_planning_round1.md"
- Guide says "for examples, see examples.md" but examples.md is empty/stub
- Router references phase guide that was deleted

**Automated:** ✅ Yes (can validate file existence and basic content presence)

---

### Type 5: Circular Dependency Detection

**What to Check:**
No two files should require each other to be completed first.

**Common Circular Patterns:**

**Pattern 1: Checklist ↔ Spec**
```markdown
# checklist.md
Q1: What framework should we use?
→ See spec.md Section 4 for framework decision

# spec.md
## Section 4: Framework
See checklist.md Q1 for framework requirements
```

**Problem:** Each file says "see the other file first" → deadlock

**Pattern 2: Stage Prerequisites**
```markdown
# S5 guide
Prerequisites:
- [ ] Completed S6

# S6 guide
Prerequisites:
- [ ] Completed S5
```

**Problem:** Impossible to complete either stage

**Detection Commands:**

```bash
# Build dependency graph (manual process)
# For each file, extract what it REQUIRES and what it PROVIDES

echo "Building dependency graph..."
for file in feature-updates/guides_v2/stages/**/*.md; do
  echo "=== $file ==="
  echo "REQUIRES:"
  grep -A 5 "^## Prerequisites" "$file"
  echo "PROVIDES:"
  grep -A 5 "^## Outputs" "$file"
done > /tmp/dependency_graph.txt

# Manually review for circular references
# Look for: File A requires File B, File B requires File A
```

**Validation Process:**

1. Create list of all files and their dependencies
2. For each file, trace backwards to see what it needs
3. If tracing backwards leads back to original file → CIRCULAR
4. Flag for manual review

**Red Flags:**
- File A prerequisites mention File B
- File B prerequisites mention File A
- Stage N says "Completed Stage N+1" required
- Template includes itself

**Automated:** ⚠️ Partial (can detect simple cycles, complex cycles require graph analysis)

---

### Type 6: Orphaned File Detection

**What to Check:**
Files created in workflow should be used by at least one subsequent stage.

**Validation Process:**

```bash
# Step 1: List all files CREATED by stages
grep -rh "^## Outputs" stages/ | grep -oE "[a-z_]+\.md" | sort -u > /tmp/created_files.txt

# Step 2: List all files USED by stages
grep -rh "^## Prerequisites" stages/ | grep -oE "[a-z_]+\.md" | sort -u > /tmp/used_files.txt

# Step 3: Find files created but never used
comm -23 /tmp/created_files.txt /tmp/used_files.txt > /tmp/orphaned_files.txt

echo "Orphaned files (created but never used):"
cat /tmp/orphaned_files.txt
```

**Common Orphaned Files:**

**lessons_learned.md:**
- Created in S7.P3
- Intended for S10.P1 guide updates
- Often not explicitly listed in S10 prerequisites
- **Status:** NOT orphaned (used in S10.P1)

**RESEARCH_NOTES.md:**
- Created in S2.P1.I1
- Used by agent during S2 for reference
- Not explicitly required by S3
- **Status:** Borderline orphaned (agent reference file, not stage handoff file)

**feature_requirements.md:**
- If a stage created this but workflow uses "spec.md" instead
- Never referenced in any subsequent stage
- **Status:** ORPHANED (should be removed or renamed to spec.md)

**Red Flags:**
- File created in Outputs section but never appears in any Prerequisites
- File mentioned in guide but no stage actually creates it
- File name mismatch (stage creates X.md, next stage expects Y.md)

**Automated:** ✅ Yes (can detect files created vs files used)

---

## How Errors Happen

### Root Cause 1: File Renamed Without Reference Updates

**Scenario:**
- S4 output file renamed from "test_plan.md" to "test_strategy.md" for clarity
- S4 guide updated
- S5 prerequisites updated
- **FORGOT** to update templates, CLAUDE.md, other cross-references

**Result:**
- Templates still say "see test_plan.md"
- New epics created from template have broken references
- Error propagates to all new work

---

### Root Cause 2: Stage Skipped Without Dependency Adjustment

**Scenario:**
- User decides to skip S4 for simple feature
- Agent proceeds directly S3 → S5
- S5 expects test_strategy.md from S4
- **File doesn't exist** because S4 was skipped

**Result:**
- S5 blocks on missing file
- Agent asks user for clarification
- Manual workaround created
- Workflow documentation doesn't reflect actual practice

---

### Root Cause 3: Template Created Before Workflow Finalized

**Scenario:**
- Workflow designed: S1 → S2 → S3 → S4 → S5
- Templates created referencing this workflow
- **LATER** S4 added between S3 and original S4
- Templates never updated to reflect new numbering

**Result:**
- Template says "After S3, see S4_implementation.md"
- But S4 is now testing strategy, S5 is implementation
- Wrong file referenced in every new epic

---

### Root Cause 4: Section Reorganization Without Cross-Reference Updates

**Scenario:**
- DISCOVERY.md originally had:
  - Section 1: Background
  - Section 2: Technical Analysis
  - Section 3: Constraints
- Reorganized to:
  - Section 1: Background
  - Section 2: Constraints
  - Section 3: Technical Analysis
- spec.md template says "see DISCOVERY.md Section 3 for technical analysis"
- **After reorganization:** Section 3 is now technical analysis (was constraints)

**Result:**
- Reference still works but confusing
- If template not updated, references become stale over time

---

### Root Cause 5: Parallel File Creation Without Coordination

**Scenario:**
- Agent A creates spec.md
- Agent B simultaneously creates checklist.md
- spec.md says "see checklist.md Q5"
- checklist.md only has Q1-Q4 (Q5 doesn't exist yet)

**Result:**
- Broken reference at creation time
- Requires coordination between agents
- Historical issue in KAI-6 parallel work

---

## Automated Validation

### Pre-Audit Script Coverage

**From `scripts/pre_audit_checks.sh`:**

**CHECK 9: Stage Handoff File Validation** *(planned, not yet implemented)*
```bash
#!/bin/bash
# Validate stage handoff files exist in expected locations

echo "Checking stage handoff file dependencies..."

# Define expected handoff files per stage
declare -A stage_outputs=(
  ["S1"]="DISCOVERY.md"
  ["S2"]="spec.md checklist.md RESEARCH_NOTES.md"
  ["S3"]="epic_smoke_test_plan.md"
  ["S4"]="test_strategy.md"
  ["S5"]="implementation_plan.md"
  ["S6"]="implementation_checklist.md"
  ["S7"]="lessons_learned.md"
)

# Check if guides document these outputs
for stage in "${!stage_outputs[@]}"; do
  stage_dir="stages/$(echo $stage | tr '[:upper:]' '[:lower:]')"
  for output_file in ${stage_outputs[$stage]}; do
    if ! grep -rq "$output_file" "$stage_dir/"; then
      echo "ERROR: $stage should output $output_file but guide doesn't mention it"
    fi
  done
done
```

**CHECK 10: Cross-Reference Validation** *(planned, not yet implemented)*
```bash
#!/bin/bash
# Validate file references in guides point to existing files

echo "Checking cross-references in guides..."

# Find all markdown file references
refs=$(grep -roh '\`[^`]*\.md\`' stages/ reference/ templates/ | tr -d '`' | sort -u)

for ref in $refs; do
  # Try relative to guides_v2
  if [ ! -f "feature-updates/guides_v2/$ref" ] && \
     [ ! -f "$ref" ] && \
     [ ! -f "feature-updates/guides_v2/stages/$ref" ]; then
    echo "WARNING: Reference to $ref found but file doesn't exist"
  fi
done
```

**CHECK 11: Circular Dependency Detection** *(planned, not yet implemented)*
```bash
#!/bin/bash
# Detect simple circular dependencies

echo "Checking for circular dependencies..."

# Build prerequisite graph
for file in stages/**/*.md; do
  prereqs=$(grep -A 10 "^## Prerequisites" "$file" | grep -oE "stages/[^)]+\.md")
  for prereq in $prereqs; do
    # Check if prereq also requires this file
    if grep -q "$(basename $file)" "$prereq" 2>/dev/null; then
      echo "ERROR: Circular dependency detected: $file ↔ $prereq"
    fi
  done
done
```

**Automation Coverage: ~30%**
- ✅ File existence validation
- ✅ Basic reference checking
- ✅ Simple circular dependency detection
- ❌ Semantic correctness (does output actually satisfy input needs?)
- ❌ Complex dependency graph analysis
- ❌ Runtime validation (files exist at correct workflow points)

---

## Manual Validation

### Manual Process (Dependency Graph Audit)

**Duration:** 45-60 minutes
**Frequency:** After workflow changes, file renames, stage additions/removals

**Step 1: Build Dependency Matrix (15 min)**

Create spreadsheet or text file:

| Stage | Input Files Required | Output Files Created | References To | Referenced By |
|-------|---------------------|---------------------|---------------|---------------|
| S1 | None | DISCOVERY.md | - | S2 (spec.md) |
| S2 | DISCOVERY.md | spec.md, checklist.md | DISCOVERY.md | S3, S4, S5 |
| S3 | All spec.md files | epic_smoke_test_plan.md | spec.md files | S4, S9 |
| ... | ... | ... | ... | ... |

```bash
# Extract inputs and outputs for matrix
for stage_dir in stages/s{1..10}/; do
  echo "=== $(basename $stage_dir) ==="
  echo "INPUTS:"
  grep -A 5 "^## Prerequisites" $stage_dir/*.md | grep "\.md"
  echo "OUTPUTS:"
  grep -A 5 "^## Outputs" $stage_dir/*.md | grep "\.md"
  echo ""
done
```

**Step 2: Trace Critical File Paths (15 min)**

For each major handoff file, trace through workflow:

**DISCOVERY.md Path:**
1. Created: S1
2. Used by: S2 (spec.md creation)
3. Referenced in: spec.md, RESEARCH_NOTES.md
4. Lifetime: Epic duration (never deleted)

**spec.md Path:**
1. Created: S2
2. Used by: S3 (epic testing), S4 (feature testing), S5 (impl planning)
3. Updated by: S8 (alignment after each feature)
4. Lifetime: Epic duration

**test_strategy.md Path:**
1. Created: S4
2. Used by: S5.P1.I1 (merged into implementation_plan.md)
3. Lifetime: Until S5.P1.I1 merge (can be deleted after)

**implementation_plan.md Path:**
1. Created: S5 (includes merged test_strategy.md content)
2. Used by: S6 (implementation), S7 (testing reference)
3. Lifetime: Feature duration

**Validation Questions:**
- [ ] Does file exist when first used?
- [ ] Is file created before any references to it?
- [ ] If file updated, do all references reflect updates?
- [ ] If file deleted, are all references removed?

**Step 3: Validate Template References (10 min)**

```bash
# Check each template
for template in templates/*.md; do
  echo "=== $(basename $template) ==="

  # Find all file references
  refs=$(grep -oE '\`[^`]+\.md\`' "$template" | tr -d '`')

  for ref in $refs; do
    # Determine when this template is used
    template_name=$(basename "$template")

    # Check if referenced file exists at that point in workflow
    # (Manual analysis required)
    echo "Template $template_name references $ref"
    echo "   When is template used? Manual check needed."
    echo "   Does $ref exist at that point? Manual check needed."
  done
done
```

**Step 4: Check for Orphaned Files (5 min)**

```bash
# Find files created but never used
created=$(grep -rh "^## Outputs" stages/ | grep -oE "[a-z_]+\.md" | sort -u)
used=$(grep -rh "^## Prerequisites\|see.*\.md\|refer to.*\.md" stages/ reference/ | \
       grep -oE "[a-z_]+\.md" | sort -u)

echo "Files created in workflow:"
echo "$created"
echo ""
echo "Files used in workflow:"
echo "$used"
echo ""
echo "Potentially orphaned (created but not explicitly used):"
comm -23 <(echo "$created" | sort) <(echo "$used" | sort)
```

**Step 5: Validate Cross-Document Section References (10 min)**

```bash
# Find all section references
grep -rn "Section [0-9]\|see.*Section" feature-updates/guides_v2/templates/

# For each reference:
# 1. Identify source document
# 2. Identify target document and section
# 3. Open target document
# 4. Verify section exists
# 5. Verify section content matches what reference expects

# (Manual validation - requires reading both files)
```

---

## Context-Sensitive Rules

### Rule 1: RESEARCH_NOTES.md Is Agent-Only File

**Context:** Some files are created for agent reference, not stage handoffs.

**RESEARCH_NOTES.md:**
- Created in S2.P1.I1
- Used by agent during S2 research
- Not explicitly required by S3
- **Status:** NOT orphaned (valid agent-only file)

**Validation:** If file used by agent during single stage (not handed off) → VALID (not orphaned)

---

### Rule 2: Template References May Be Placeholders

**Context:** Templates may include placeholder sections for user to fill in.

**Example:**
```markdown
# spec.md template

## Background

[User: Provide background from DISCOVERY.md Section 2]
```

**This is NOT a broken reference:**
- [User: ...] indicates placeholder
- User expected to replace with actual content
- Not a broken cross-reference

**Detection:**
```bash
# Look for [User: ...] or [Agent: ...] markers
grep -rn "\[User:\|\[Agent:" templates/
```

**Validation:** Placeholder markers in templates → VALID (not broken reference)

---

### Rule 3: Optional Files May Not Exist

**Context:** Some stages have optional outputs depending on circumstances.

**debugging/ folder:**
- Created only if issues found during testing
- Not created for clean implementations
- **Status:** Optional dependency (not error if missing)

**lessons_learned.md:**
- Created in S7.P3
- May be empty for trivial features
- **Status:** Required file, optional content

**Validation:** If guide says "optional" or "if needed" → VALID (not error if missing)

---

### Rule 4: Parallel Work Has Different Dependency Patterns

**Context:** Parallel work involves simultaneous file creation with different dependency rules.

**Example:**
- Features 01-04 all create spec.md simultaneously
- No inter-feature dependencies (Feature 02 spec.md doesn't depend on Feature 01 spec.md)
- Dependencies are epic-level (all depend on DISCOVERY.md)

**Validation:** Parallel work files don't form linear chain → VALID

---

## Real Examples

### Example 1: Missing test_strategy.md After S4 Skip

**Issue Found During KAI-7 Testing:**

**Scenario:**
- User decided simple feature didn't need full S4 testing strategy
- Agent proceeded S3 → S5 directly
- S5.P1.I1 expects to merge test_strategy.md into implementation_plan.md
- **File doesn't exist**

**Error Message:**
```
Agent: "S5.P1.I1 requires test_strategy.md from S4. File not found.
Should I proceed without test strategy or create minimal test strategy now?"
```

**Problem:**
- Workflow dependency not flexible for simple features
- S4 skip breaks S5 assumptions

**Fix Options:**

**Option 1: Make test_strategy.md truly optional in S5**
```diff
S5.P1.I1 guide:

-Merge test_strategy.md into implementation_plan.md (mandatory)
+If test_strategy.md exists (from S4), merge into implementation_plan.md
+If test_strategy.md doesn't exist, create minimal testing section in implementation_plan.md
```

**Option 2: Always require S4 (no skipping)**
```markdown
S4 guide:

## Can S4 Be Skipped?

NO. Even simple features require testing strategy.
If feature is simple, S4.I1 will produce minimal test_strategy.md (5-10 min).
```

**Root Cause:** Optional stage created mandatory dependency

**How D12 Detects:**
- Type 1: Stage Handoff File Dependencies
- Manual validation: Check if "optional" stages produce "required" files

---

### Example 2: spec.md Template References Non-Existent Section

**Issue Found During KAI-6 Spec Creation:**

**Template Content:**
```markdown
# spec.md template

## Background

From epic discovery, see DISCOVERY.md Section 3: Technical Constraints.
```

**Actual DISCOVERY.md Structure:**
```markdown
# DISCOVERY.md

## 1. Epic Background
## 2. Existing Codebase Analysis
## 3. Feature Breakdown
## 4. Technical Considerations
```

**Problem:**
- Template references "Section 3: Technical Constraints"
- Actual DISCOVERY.md has "Section 4: Technical Considerations"
- Section names don't match

**Fix:**
```diff
# spec.md template

## Background

-From epic discovery, see DISCOVERY.md Section 3: Technical Constraints.
+From epic discovery, see DISCOVERY.md "Technical Considerations" section.
```

**Root Cause:** Template created before DISCOVERY.md structure finalized, not updated when structure changed

**How D12 Detects:**
- Type 2: Intra-Document Cross-References
- Type 3: Template File References
- Manual validation Step 5: Validate section references

---

### Example 3: Circular Reference Between checklist.md and spec.md

**Issue Found During KAI-5 S2 Review:**

**checklist.md:**
```markdown
## Questions

Q1: What authentication method should we use?
   → See spec.md Section 4: Authentication for decision rationale
```

**spec.md:**
```markdown
## Section 4: Authentication

Authentication method: [TBD - see checklist.md Q1 for requirements]
```

**Problem:**
- checklist.md says "see spec.md"
- spec.md says "see checklist.md"
- Circular dependency

**Fix:**
```diff
# spec.md

## Section 4: Authentication

-Authentication method: [TBD - see checklist.md Q1 for requirements]
+Authentication method: JWT tokens
+Rationale: Per checklist.md Q1 requirements (mobile app needs stateless auth)
```

**Workflow:**
1. checklist.md asks question
2. User answers question
3. spec.md documents decision + rationale
4. NO circular reference (spec can reference checklist for context, but doesn't depend on it being answered first)

**Root Cause:** Spec tried to defer decision back to checklist instead of documenting decision

**How D12 Detects:**
- Type 5: Circular Dependency Detection
- Manual validation: Build dependency graph, trace for cycles

---

### Example 4: Orphaned feature_requirements.md File

**Issue Found During KAI-4 Workflow Review:**

**What Happened:**
- Early workflow design had "feature_requirements.md" file
- Workflow evolved to use "spec.md" instead
- S2 guide updated to output spec.md
- Template still created feature_requirements.md
- **No stage used feature_requirements.md**

**Detection:**
```bash
# Created files
grep "^## Outputs" stages/s2/*.md
# Output: spec.md, checklist.md

# Used files
grep "feature_requirements.md" stages/**/*.md
# Output: (none)

# Template creates it
grep "feature_requirements.md" templates/feature_spec_template.md
# Output: Found (creates unused file)
```

**Problem:**
- Template created file that workflow never used
- Wasted effort for every feature
- Confusion about purpose of file

**Fix:**
```diff
# Remove from template
-Create feature_requirements.md with:
-[requirements content]

# Use spec.md instead (already in workflow)
```

**Root Cause:** Template not updated after workflow file naming change

**How D12 Detects:**
- Type 6: Orphaned File Detection
- Automated: Compare created files vs used files

---

### Example 5: implementation_checklist.md Referenced Too Early

**Issue Found During Template Review:**

**spec.md template:**
```markdown
## Implementation Notes

For build steps, refer to implementation_checklist.md.
```

**Problem:**
- spec.md created in S2
- implementation_checklist.md created in S6
- Reference broken for 4 stages

**Fix:**
```diff
## Implementation Notes

-For build steps, refer to implementation_checklist.md.
+For build steps, refer to implementation_plan.md (created in S5).
+During implementation (S6), refer to implementation_checklist.md for progress tracking.
```

**Root Cause:** Template referenced file created later in workflow

**How D12 Detects:**
- Type 3: Template File References
- Manual validation: Check when template used vs when referenced file created

---

## Integration with Other Dimensions

### D3: Workflow Integration

**Overlap:**
- D3 validates DOCUMENTATION says correct prerequisites
- D12 validates FILES EXIST matching those prerequisites
- **Division:** D3 = documentation, D12 = runtime reality

**Example:**
- D3 checks: S5 prerequisites say "test_strategy.md required" ✅
- D12 checks: test_strategy.md actually exists when S5 starts ✅

**Recommendation:** Run D3 BEFORE D12 (fix documentation first, then validate reality matches)

---

### D1: Cross-Reference Accuracy

**Overlap:**
- D1 validates file paths in references are technically correct
- D12 validates those files exist and have expected content
- **Division:** D1 = syntax, D12 = semantics

**Example:**
- D1 checks: Path `stages/s5/s5_implementation_planning.md` is correctly formatted ✅
- D12 checks: File exists and is not empty/stub ✅

---

### D5: Content Completeness

**Overlap:**
- D5 validates required sections exist in files
- D12 validates cross-references to those sections are correct
- **Division:** D5 = intra-file, D12 = inter-file

**Example:**
- D5 checks: DISCOVERY.md has "Technical Considerations" section ✅
- D12 checks: spec.md references to DISCOVERY.md "Technical Considerations" are valid ✅

---

### D10: File Size Assessment

**Overlap:**
- D10 validates files aren't too large
- D12 validates files exist and are usable
- **Division:** D10 = size, D12 = existence/dependencies

**Example:**
- D10 checks: implementation_plan.md is ~400 lines (not >1000) ✅
- D12 checks: implementation_plan.md exists when S6 needs it ✅

---

### D11: Structural Patterns

**Overlap:**
- D11 validates files follow template structure
- D12 validates files have content referenced by other files
- **Division:** D11 = structure, D12 = content dependencies

**Example:**
- D11 checks: spec.md has "## Prerequisites" section (structure) ✅
- D12 checks: Prerequisites section lists files that exist (dependencies) ✅

---

## Summary

**D12: Cross-File Dependencies validates that files correctly reference each other at RUNTIME.**

**Key Validations:**
1. ✅ Stage handoff files exist when needed
2. ✅ Cross-document section references are valid
3. ✅ Templates reference files that exist at template instantiation time
4. ✅ No circular dependencies between files
5. ✅ No orphaned files (created but never used)
6. ✅ Root-level files reference existing sub-guides

**Automation: ~30%**
- Automated: File existence, basic reference checking, simple circular dependencies
- Manual: Semantic correctness, complex dependency graphs, timing validation

**Critical for:**
- Preventing workflow blocks due to missing files
- Ensuring templates propagate correct references to all new epics
- Validating workflow remains coherent at runtime (not just documentation)

**Next Phase:** Phase 3 - Medium-priority dimensions (D4, D7, D9, D15)

---

**Last Updated:** 2026-02-04
**Version:** 1.0
**Status:** ✅ Fully Implemented
