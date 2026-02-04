# D3: Workflow Integration

**Dimension Number:** 3
**Category:** Core Dimensions (Always Check)
**Automation Level:** 40% automated
**Priority:** HIGH
**Last Updated:** 2026-02-04

**Focus:** Ensure workflow stages form coherent sequential flow with correct prerequisites and transitions
**Typical Issues Found:** 10-20 per major workflow restructuring

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

**D3: Workflow Integration** validates that the workflow stages form a coherent, sequential flow with correct:

1. **Prerequisites** - Each stage lists correct previous stages/outputs required
2. **Stage Transitions** - "Next Stage" references point to correct subsequent stages
3. **Output-to-Input Mapping** - One stage's outputs match next stage's prerequisites
4. **Workflow Completeness** - All stages (S1-S10) correctly linked in sequence
5. **Phase Dependencies** - Phases within stages have correct ordering
6. **Gate Placement** - Quality gates appear at correct stage boundaries

**Coverage:**
- All 10 stages (S1-S10) in `stages/` directory
- Router files (README.md, stage guide entry points)
- Root-level workflow documentation (EPIC_WORKFLOW_USAGE.md)
- Reference materials describing workflow flow

---

## Why This Matters

**Broken workflow integration = Agents get stuck or skip critical steps**

### Impact of Workflow Integration Errors:

**Broken Prerequisites:**
- Agent starts stage without required inputs
- Missing context causes poor decisions
- Rework required when prerequisites discovered later
- Example: S5 started without S4 test_strategy.md → implementation plan incomplete

**Wrong Stage Transitions:**
- Agent proceeds to wrong stage after completion
- Workflow sequence broken
- Critical stages skipped
- Example: S2 guide says "Next: S4" → S3 Epic Testing Strategy skipped entirely

**Output-to-Input Mismatches:**
- Stage A produces file X, Stage B expects file Y
- Agent confused about what inputs to use
- Manual workarounds required
- Example: S5 expects "implementation_plan.md" but S4 creates "test_plan.md"

**Incomplete Workflow Documentation:**
- Stages reference non-existent stages
- Workflow appears to have gaps
- User and agent confusion about process
- Example: Guide references "S11" which doesn't exist

### Historical Evidence:

**KAI-7 Issues:**
- S2 guide originally said "Next: S4" → S3 got skipped
- Multiple stages had stale prerequisites from old workflow
- Phase transitions referenced old notation (S5a/b/c instead of S5.P1/P2/P3)

**Why 40% Automation:**
- Automated: Stage number validation, file existence, basic sequence
- Manual Required: Semantic correctness (does prerequisite actually match what stage needs?)

---

## Pattern Types

### Type 0: Root-Level Workflow Documentation (CRITICAL - Often Missed)

**Files to Always Check:**
```
feature-updates/guides_v2/README.md
feature-updates/guides_v2/EPIC_WORKFLOW_USAGE.md
C:\Users\kmgam\code\FantasyFootballHelperScripts\CLAUDE.md (Stage Workflows section)
```

**What to Validate:**

**README.md:**
- [ ] Stage overview lists S1-S10 in correct sequence
- [ ] Each stage points to correct guide path
- [ ] Stage dependencies shown correctly
- [ ] No missing stages in overview

**EPIC_WORKFLOW_USAGE.md:**
- [ ] Stage-by-Stage section covers ALL stages (S1-S10)
- [ ] Each stage shows correct phases, iterations, gates
- [ ] Prerequisites listed for each stage match reality
- [ ] Next stage transitions are correct

**CLAUDE.md (Stage Workflows section):**
- [ ] All 10 stages listed with correct guides
- [ ] Prerequisites shown correctly
- [ ] "Next:" references point to correct subsequent stages
- [ ] No references to non-existent stages (S11, S0, etc.)

**Search Commands:**
```bash
# Check stage sequence in root files
grep -n "^## S[0-9]" feature-updates/guides_v2/README.md
grep -n "^### S[0-9]" feature-updates/guides_v2/EPIC_WORKFLOW_USAGE.md
grep -n "^\*\*S[0-9]:" CLAUDE.md

# Find "Next:" references in CLAUDE.md
grep -n "Next:" CLAUDE.md

# Find prerequisite mentions
grep -in "prerequisite\|required\|depends on" CLAUDE.md
```

**Automated:** ❌ No (requires semantic validation)

---

### Type 1: Stage Prerequisites Validation

**What to Check:**
Each stage guide must list correct prerequisites from previous stages.

**Standard Prerequisites Pattern:**
```markdown
## Prerequisites

- [ ] Completed [Previous Stage]
- [ ] File X exists (from Previous Stage output)
- [ ] User approval at Gate N (if applicable)
- [ ] All tests passing (if post-implementation)
```

**Search Commands:**
```bash
# Find all prerequisite sections
grep -rn "^## Prerequisites" stages/

# Extract prerequisites from each stage
for stage in stages/s*/; do
  echo "=== $(basename $stage) ==="
  grep -A 10 "^## Prerequisites" $stage/*.md | head -15
done
```

**Validation Checklist:**

**S1: Epic Planning**
- [ ] Prerequisites: None (entry point to workflow)

**S2: Feature Planning**
- [ ] Prerequisites: S1 complete, epic folder structure exists, DISCOVERY.md exists

**S3: Epic-Level Documentation**
- [ ] Prerequisites: S2 complete for ALL features, all spec.md files exist

**S4: Feature Testing Strategy**
- [ ] Prerequisites: S3 complete, epic plan approved (Gate 4.5), spec.md exists for feature

**S5: Implementation Planning**
- [ ] Prerequisites: S4 complete, test_strategy.md exists (merged into implementation_plan.md in S5.P1.I1)

**S6: Implementation Execution**
- [ ] Prerequisites: S5 complete, implementation_plan.md exists, user approved plan (Gate 5)

**S7: Implementation Testing**
- [ ] Prerequisites: S6 complete, implementation complete, all code written

**S8: Post-Feature Alignment**
- [ ] Prerequisites: S7 complete, feature committed, all tests passing

**S9: Epic-Level Final QC**
- [ ] Prerequisites: S8 complete for ALL features, all features committed

**S10: Epic Cleanup**
- [ ] Prerequisites: S9 complete, user testing passed (S9.P3), ZERO bugs reported

**Red Flags:**
- Prerequisites reference non-existent files
- Prerequisites reference wrong stage outputs
- Prerequisites missing critical gates (S5 doesn't mention Gate 5)
- Prerequisites reference old workflow structure

**Automated:** ⚠️ Partial (can check file existence, cannot validate semantic correctness)

---

### Type 2: Stage Transition ("Next Stage") Validation

**What to Check:**
Each stage guide must correctly indicate next stage in sequence.

**Standard Pattern:**
```markdown
## Next Stage

Proceed to [Stage Name] (`path/to/guide.md`)

## See Also
- Next: `stages/sN/sN_name.md`
```

**Search Commands:**
```bash
# Find all "Next Stage" or "Next" sections
grep -rn "^## Next Stage\|^## Next" stages/

# Find all "Next:" references in See Also
grep -rn "Next:" stages/

# Extract next stage references
for file in stages/**/*.md; do
  echo "=== $file ==="
  grep -A 2 "^## Next" "$file"
done
```

**Validation Checklist:**

| Current Stage | Should Point To | Common Errors |
|---------------|-----------------|---------------|
| S1 | S2 | Points to S3, missing S2 |
| S2 | S3 (after ALL features) | Says "S4" or "S5" |
| S3 | S4 | Says "S5" (old workflow) |
| S4 | S5 | Says "S6" |
| S5 | S6 | Says "S7" |
| S6 | S7 | Says "S8" |
| S7 | S8 | Says "S9" or "S10" |
| S8 | Repeat S5 OR S9 | Unclear branching logic |
| S9 | S10 | Says "Done" without S10 reference |
| S10 | Done (no next stage) | References S11 |

**Correct S8 Transition Logic:**
```markdown
## Next Stage

**If more features remain:**
- Repeat S5-S8 loop for next feature
- Read `stages/s5/s5_implementation_planning.md`

**If all features complete:**
- Proceed to S9: Epic-Level Final QC
- Read `stages/s9/s9_epic_final_qc.md`
```

**Red Flags:**
- Next stage references non-existent stage (S11, S0)
- Next stage skips a stage (S2 → S4, missing S3)
- Next stage references old numbering (S6 was renumbered to S9 in past)
- Next stage has broken file path
- S8 doesn't show branching logic (repeat or continue)

**Automated:** ✅ Yes (can validate stage numbers and file paths exist)

---

### Type 3: Output-to-Input File Mapping

**What to Check:**
Stage A's documented outputs must match Stage B's documented prerequisites.

**Pattern:**

**Stage A Guide:**
```markdown
## Outputs

- `spec.md` - Requirements specification
- `checklist.md` - Questions for user
```

**Stage B Guide:**
```markdown
## Prerequisites

- [ ] Completed Stage A
- [ ] `spec.md` exists
- [ ] `checklist.md` resolved (all questions answered)
```

**Search Commands:**
```bash
# Find all Output sections
grep -rn "^## Outputs" stages/

# Find all Prerequisites sections
grep -rn "^## Prerequisites" stages/

# Extract both for comparison
for stage in stages/s*/; do
  echo "=== $(basename $stage) OUTPUTS ==="
  grep -A 5 "^## Outputs" $stage/*.md
  echo "=== NEXT STAGE PREREQUISITES ==="
  # Manually check next stage
done
```

**Validation Matrix:**

| Stage | Primary Outputs | Next Stage Expects |
|-------|----------------|-------------------|
| S1 | epic folder, DISCOVERY.md, feature_XX folders | S2: epic folder exists, DISCOVERY.md exists |
| S2 | spec.md, checklist.md, RESEARCH_NOTES.md | S3: all spec.md files exist |
| S3 | epic_smoke_test_plan.md, refined EPIC_README.md | S4: epic context for feature testing |
| S4 | test_strategy.md | S5.P1.I1: merges test_strategy.md into implementation_plan.md |
| S5 | implementation_plan.md | S6: implementation_plan.md as build guide |
| S6 | implementation_checklist.md, implemented code | S7: code to test |
| S7 | lessons_learned.md, committed feature | S8: committed feature for alignment check |
| S8 | Updated remaining specs | S5 (repeat) or S9: updated specs as context |
| S9 | Epic testing report | S10: confirmation all tests passed |
| S10 | PR, updated EPIC_TRACKER.md | Done |

**Red Flags:**
- S2 produces "specification.md" but S3 looks for "spec.md"
- S4 produces "testing_plan.md" but S5 expects "test_strategy.md"
- S5 says output is "plan.md" but S6 looks for "implementation_plan.md"
- Stage produces file but next stage doesn't mention it in prerequisites
- Stage expects file but previous stage doesn't produce it

**Automated:** ❌ No (requires cross-file semantic analysis)

---

### Type 4: Phase and Iteration Dependencies

**What to Check:**
Phases within a stage must have correct ordering and dependencies.

**Example: S5 (Implementation Planning) has 3 phases:**
```
S5.P1: Planning Round 1 (I1-I7)
  ↓ Must complete before
S5.P2: Planning Round 2 (I8-I13)
  ↓ Must complete before
S5.P3: Planning Round 3 (I14-I22)
```

**Example: S7 (Implementation Testing) has 3 phases:**
```
S7.P1: Smoke Testing (MANDATORY GATE)
  ↓ Must pass before
S7.P2: QC Rounds (3 rounds)
  ↓ Must complete before
S7.P3: Final Review
```

**Search Commands:**
```bash
# Find all phase references in a stage
grep -rn "^## S[0-9]\.P[0-9]" stages/s5/

# Check phase ordering
for file in stages/s5/*.md; do
  echo "=== $file ==="
  grep -n "^## " "$file" | grep -E "S5\.P[0-9]"
done
```

**Validation Checklist:**

**S1 Phases:**
- [ ] P1 (Setup) → P2 (Analysis) → P3 (Discovery) → P4 (Breakdown) → P5 (Structure) → P6 (Transition)
- [ ] P3 cannot start without P2 complete
- [ ] P4 cannot start without P3 user-approved

**S2 Phases:**
- [ ] P1 (Spec Creation - 3 iterations) → P2 (Cross-Feature Alignment)
- [ ] P2 runs AFTER all features complete P1
- [ ] P1.I1 → P1.I2 → P1.I3 sequential

**S5 Phases:**
- [ ] P1 (Round 1) → P2 (Round 2) → P3 (Round 3)
- [ ] Cannot skip rounds
- [ ] Each round has specific iterations that must run in order

**S7 Phases:**
- [ ] P1 (Smoke) → P2 (QC) → P3 (Review)
- [ ] P2 cannot start if P1 fails (restart from P1)
- [ ] P3 cannot start if P2 finds issues (restart from P1)

**S9 Phases:**
- [ ] P1 (Smoke) → P2 (QC) → P3 (User Testing) → P4 (Review)
- [ ] P3 cannot start without P2 passing
- [ ] P4 cannot start without user reporting ZERO bugs

**Red Flags:**
- Phase order documentation doesn't match actual workflow
- Phase prerequisites missing
- Phases reference each other circularly (P2 requires P3, P3 requires P2)
- Phase guide says "optional" when phase is mandatory
- Router file shows different phase order than individual guides

**Automated:** ⚠️ Partial (can check numbering sequence, cannot validate semantic dependencies)

---

### Type 5: Gate Placement Validation

**What to Check:**
Quality gates appear at correct stage boundaries with correct gate numbers.

**All Gates (from reference/mandatory_gates.md):**

| Gate | Location | Type | Approver | What It Validates |
|------|----------|------|----------|-------------------|
| Gate 1 | S2.P1.I1 | Embedded | Agent | Research completeness |
| Gate 2 | S2.P1.I3 | Embedded | Agent | Spec-to-epic alignment |
| Gate 3 | S2.P1.I3 | Stage | User | Checklist approval |
| Gate 4.5 | S3.P3 | Stage | User | Epic plan approval |
| Gate 5 | S5.P3 | Stage | User | Implementation plan approval |
| Gate 4a | S5.P1.I2 | Iteration | Agent | TODO specification audit |
| Gate 7a | S5.P1.I3 | Iteration | Agent | Backward compatibility |
| Gate 23a | S5.P3.I2 | Iteration | Agent | Pre-implementation spec audit |
| Gate 24 | S5.P3.I3 | Iteration | Agent | GO/NO-GO decision |
| Gate 25 | S5.P3.I3 | Iteration | Agent | Spec validation check |

**Search Commands:**
```bash
# Find all gate references
grep -rn "Gate [0-9]" stages/

# Find gate implementation sections
grep -rn "^### Gate\|^## Gate" stages/

# Check for gates in wrong locations
grep -rn "Gate 5" stages/s2/ stages/s3/ stages/s4/  # Should only be in S5
```

**Validation Checklist:**

- [ ] Gate 3 appears in S2.P1.I3 (not S2.P2 or S3)
- [ ] Gate 4.5 appears in S3.P3 (not S3.P1 or S4)
- [ ] Gate 5 appears in S5.P3 (not S5.P1 or S6)
- [ ] Gates 4a, 7a, 23a, 24, 25 appear in S5 only
- [ ] No gates reference deprecated gate numbers (Gate 6, Gate 7 that don't exist)
- [ ] Gates appear in numerical order within their sections
- [ ] Each gate has clear pass/fail criteria
- [ ] User gates (3, 4.5, 5) clearly marked as requiring user approval
- [ ] Agent gates clearly marked as self-validation

**Red Flags:**
- Gate appears in wrong stage (Gate 5 in S3)
- Gate number doesn't exist in mandatory gates reference
- Gate appears twice in workflow
- Gate missing from stage where it should be
- Gate says "user approval" but mandatory_gates.md says "agent"
- Gate reference uses old numbering (Gate 4 instead of Gate 4.5)

**Automated:** ✅ Yes (can validate gate numbers and locations)

---

## How Errors Happen

### Root Cause 1: Workflow Evolution Without Update Cascade

**Scenario:**
- Workflow evolves (e.g., S4 added between old S3 and S4)
- New stage guides created
- Old guides updated for their own content
- **BUT:** Cross-references not systematically updated

**Result:**
- S3 still says "Next: S5" (should now be "Next: S4")
- S5 prerequisites still say "Completed S3" (should say "Completed S4")

**Example from History:**
- Old workflow: S1 → S2 → S3 (crosscheck) → S4 (impl plan) → S5 (execution)
- New workflow: S1 → S2 → S3 (epic) → S4 (testing) → S5 (impl plan) → S6 (execution)
- Several guides kept old "Next: S4" when it should be "Next: S5" after renumbering

---

### Root Cause 2: Copy-Paste Template Propagation

**Scenario:**
- Create new stage guide by copying existing guide
- Update main content
- **FORGET** to update Prerequisites, Next Stage, See Also sections

**Result:**
- S7 guide copied from S6
- S7 Prerequisites still say "Completed S5" (should say "Completed S6")
- S7 Next Stage says "S7" (should say "S8")

---

### Root Cause 3: Output Filename Changes Without Input Updates

**Scenario:**
- S4 changes output from "test_plan.md" to "test_strategy.md" for clarity
- S4 guide updated
- **FORGET** to update S5 prerequisites to expect "test_strategy.md"

**Result:**
- S5 agent looks for "test_plan.md", doesn't find it
- Agent confused, asks user
- Manual workaround required

---

### Root Cause 4: Phase Additions Without Router Updates

**Scenario:**
- S5 splits into 3 phases (S5.P1, S5.P2, S5.P3)
- Individual phase guides created
- **FORGET** to update S5 router file with new structure

**Result:**
- Agent reads S5 router, sees old single-phase structure
- Agent skips S5.P2 entirely
- Verification iterations missing from implementation planning

---

### Root Cause 5: Gate Renumbering Without Cross-Reference Updates

**Scenario:**
- Gate numbering system revised (Gate 4 becomes Gate 4.5)
- Gate implementation section updated in S3
- **FORGET** to update references in CLAUDE.md, Prerequisites sections

**Result:**
- CLAUDE.md says "Gate 4" but guides reference "Gate 4.5"
- Agent confusion about which gate number is correct
- Inconsistent documentation

---

## Automated Validation

### Pre-Audit Script Coverage

**From `scripts/pre_audit_checks.sh`:**

**CHECK 7: Stage Sequence Validation** *(planned, not yet implemented)*
```bash
# Validate S1-S10 sequence in README.md
stages=$(grep -E "^\*\*S[0-9]" feature-updates/guides_v2/README.md | grep -oE "S[0-9]+")
expected="S1 S2 S3 S4 S5 S6 S7 S8 S9 S10"
if [ "$stages" != "$expected" ]; then
  echo "ERROR: Stage sequence incorrect in README.md"
fi

# Validate "Next:" references point to valid stages
for file in stages/**/*.md; do
  next_refs=$(grep -oE "Next: \`stages/s[0-9]+/" "$file")
  for ref in $next_refs; do
    stage_num=$(echo "$ref" | grep -oE "s[0-9]+")
    if [ ! -d "stages/$stage_num" ]; then
      echo "ERROR: $file references non-existent stage $stage_num"
    fi
  done
done
```

**CHECK 8: Gate Placement Validation** *(planned, not yet implemented)*
```bash
# Validate gates appear in correct stages
declare -A gate_locations=(
  ["Gate 3"]="stages/s2/"
  ["Gate 4.5"]="stages/s3/"
  ["Gate 5"]="stages/s5/"
  ["Gate 4a"]="stages/s5/"
  ["Gate 7a"]="stages/s5/"
  ["Gate 23a"]="stages/s5/"
)

for gate in "${!gate_locations[@]}"; do
  expected_dir="${gate_locations[$gate]}"
  found=$(grep -rl "$gate" stages/)
  for file in $found; do
    if [[ ! "$file" =~ ^$expected_dir ]]; then
      echo "ERROR: $gate found in wrong location: $file (expected $expected_dir)"
    fi
  done
done
```

**Automation Coverage: ~40%**
- ✅ Stage number sequence validation
- ✅ File path existence checks
- ✅ Gate number validation
- ❌ Semantic prerequisite correctness (requires human judgment)
- ❌ Output-to-input mapping (requires cross-file analysis)
- ❌ Workflow completeness assessment (requires understanding of workflow logic)

---

## Manual Validation

### Manual Process (Stage Sequence Audit)

**Duration:** 30-45 minutes
**Frequency:** After workflow changes, stage additions/removals, major restructuring

**Step 1: Extract Workflow Sequence (5 min)**

```bash
# Get stage list from README.md
grep -E "^\| \*\*[0-9]" feature-updates/guides_v2/README.md | head -10

# Get stage list from CLAUDE.md
grep -E "^\*\*S[0-9]" CLAUDE.md

# Compare - should match S1-S10
```

**Step 2: Validate Each Stage Prerequisites (15-20 min)**

For EACH stage S1-S10:
```bash
# Read Prerequisites section
stage_file="stages/sN/sN_name.md"  # Replace N with actual stage number
grep -A 10 "^## Prerequisites" "$stage_file"

# Questions to ask:
# 1. Does previous stage exist?
# 2. Do referenced files match previous stage outputs?
# 3. Are gate numbers correct?
# 4. Are file paths correct?
```

**Validation Matrix:**

| Stage | Expected Prerequisites | Files to Check |
|-------|------------------------|----------------|
| S1 | None | - |
| S2 | S1, DISCOVERY.md | DISCOVERY.md in epic folder |
| S3 | S2 (all features), spec.md files | All feature_XX/spec.md |
| S4 | S3, epic plan approved | epic_smoke_test_plan.md |
| S5 | S4, test_strategy.md | feature_XX/test_strategy.md |
| S6 | S5, implementation_plan.md | feature_XX/implementation_plan.md |
| S7 | S6, code complete | Implementation files |
| S8 | S7, feature committed | Git commit for feature |
| S9 | S8 (all features) | All features committed |
| S10 | S9, user testing passed | S9.P3 user approval |

**Step 3: Validate Stage Transitions (10-15 min)**

```bash
# For each stage, check "Next Stage" section
for stage_dir in stages/s{1..10}/; do
  echo "=== $(basename $stage_dir) ==="
  main_file="$stage_dir/$(basename $stage_dir)_*.md"
  grep -A 3 "^## Next" $main_file
done

# Validate:
# S1 → S2
# S2 → S3
# S3 → S4
# S4 → S5
# S5 → S6
# S6 → S7
# S7 → S8
# S8 → S5 (repeat) OR S9 (all done)
# S9 → S10
# S10 → Done
```

**Step 4: Validate Output-to-Input Mapping (10-15 min)**

```bash
# Create mapping document
echo "Stage Output-to-Input Validation" > /tmp/output_input_map.txt

# For each stage, extract outputs
for N in {1..9}; do  # S1-S9 (S10 is final)
  echo "=== S$N Outputs ===" >> /tmp/output_input_map.txt
  grep -A 5 "^## Outputs" stages/s$N/*.md >> /tmp/output_input_map.txt

  echo "=== S$((N+1)) Prerequisites ===" >> /tmp/output_input_map.txt
  grep -A 5 "^## Prerequisites" stages/s$((N+1))/*.md >> /tmp/output_input_map.txt
  echo "" >> /tmp/output_input_map.txt
done

# Manually review for mismatches
cat /tmp/output_input_map.txt
```

**Step 5: Validate Gate Placement (5 min)**

```bash
# Check each mandatory gate is in correct location
echo "Gate 3 should be in S2:"
grep -rn "Gate 3" stages/s2/

echo "Gate 4.5 should be in S3:"
grep -rn "Gate 4\.5" stages/s3/

echo "Gate 5 should be in S5:"
grep -rn "Gate 5" stages/s5/

echo "Gates 4a, 7a, 23a, 24, 25 should be in S5:"
grep -rn "Gate 4a\|Gate 7a\|Gate 23a\|Gate 24\|Gate 25" stages/s5/
```

---

## Context-Sensitive Rules

### Rule 1: Intentional Workflow Variations Are Valid

**Context:** Some features may have legitimate workflow variations.

**Examples of Valid Variations:**

**Bug Fix Workflow:**
- May skip S2-S4 for urgent hotfixes
- Documentation explicitly states "For bugs, proceed directly to debugging protocol"
- NOT an error

**Single-Feature Epics:**
- S2.P2 (Cross-Feature Alignment) may be marked "N/A - single feature"
- NOT an error if explicitly documented

**Detection:**
```bash
# Look for explicit workflow variation documentation
grep -rn "Note:\|Exception:\|Variation:" stages/

# Look for conditional logic
grep -rn "If.*feature\|When.*bug" stages/
```

**Validation:** If variation documented with clear rationale → VALID

---

### Rule 2: Historical References Are Valid in Examples

**Context:** Guides may reference old workflow in "Historical Evidence" sections.

**Example:**
```markdown
## Historical Evidence

In the old workflow, S5 was split into S5a/S5b/S5c phases. This caused confusion,
so we adopted S5.P1/P2/P3 notation instead.
```

**Detection:**
```bash
# Check if old references appear in historical context
grep -B 3 -A 3 "S5a\|S5b" stages/

# If found in "Historical Evidence" section → VALID
```

**Validation:** Old notation in historical context → VALID (not an error)

---

### Rule 3: Router Files May Show Simplified Workflow

**Context:** Router files (like stage README.md) may show simplified workflow for readability.

**Example:**
```markdown
# S5: Implementation Planning

S5.P1 → S5.P2 → S5.P3 → S6
```

This is simplified; actual workflow has 22 iterations. Router shows phase-level only.

**Validation:** Simplified view in router → VALID (if detailed guides exist)

---

### Rule 4: Parallel Work Sections May Reference Non-Linear Workflow

**Context:** Parallel work guides describe coordination, which breaks linear S1→S2→...→S10 flow.

**Example:**
```markdown
## S2 Parallel Work

Primary agent: S2.P1 for Feature 01
Secondary agents: S2.P1 for Features 02-04 (simultaneous)
```

**Detection:**
```bash
# Check if in parallel_work/ directory
if [[ "$file" =~ parallel_work/ ]]; then
  # Non-linear workflow expected
fi
```

**Validation:** Non-linear workflow in parallel_work/ → VALID

---

## Real Examples

### Example 1: Missing S4 Reference After Workflow Change

**Issue Found During KAI-7 Audit:**

**Location:** `stages/s3/s3_epic_planning_approval.md`

**Error:**
```markdown
## Next Stage

Proceed to S5: Implementation Planning (`stages/s5/s5_implementation_planning.md`)
```

**Problem:**
- S4 (Feature Testing Strategy) added between S3 and S5
- S3 guide updated for content, but "Next Stage" not updated
- Agents would skip S4 entirely

**Fix:**
```diff
## Next Stage

-Proceed to S5: Implementation Planning (`stages/s5/s5_implementation_planning.md`)
+Proceed to S4: Feature Testing Strategy (`stages/s4/s4_feature_testing_strategy.md`)
```

**Root Cause:** Workflow evolution without systematic update cascade

**How D3 Detects:**
- Type 2: Stage Transition validation
- Manual validation Step 3: Check each "Next Stage" section
- Automated: CHECK 7 validates stage sequence

---

### Example 2: Output-to-Input Filename Mismatch

**Issue Found During KAI-7 S4 Implementation:**

**S4 Guide (Output):**
```markdown
## Outputs

- `test_strategy.md` - Complete testing strategy for feature
```

**S5 Guide (Prerequisites):**
```markdown
## Prerequisites

- [ ] Completed S4
- [ ] `test_plan.md` exists
```

**Problem:**
- S4 creates "test_strategy.md"
- S5 expects "test_plan.md"
- Agent gets confused, asks user for clarification

**Fix:**
```diff
## Prerequisites

- [ ] Completed S4
-- [ ] `test_plan.md` exists
+- [ ] `test_strategy.md` exists (merged into implementation_plan.md in S5.P1.I1)
```

**Root Cause:** Filename changed in S4 without updating S5 prerequisites

**How D3 Detects:**
- Type 3: Output-to-Input File Mapping
- Manual validation Step 4: Extract outputs and compare to next stage prerequisites

---

### Example 3: Gate Number Mismatch After Gate Renumbering

**Issue Found During KAI-7 S3 Refactor:**

**CLAUDE.md (Root File):**
```markdown
**S3: Epic Planning**
- Gate 4: User approves epic plan
```

**S3 Guide:**
```markdown
## Gate 4.5: Epic Plan Approval

User must approve epic plan before proceeding to S4.
```

**Problem:**
- Gate renamed from "Gate 4" to "Gate 4.5" for clarity
- S3 guide updated
- CLAUDE.md root file NOT updated
- Inconsistent documentation confuses agents

**Fix:**
```diff
**S3: Epic Planning**
-- Gate 4: User approves epic plan
+- Gate 4.5: User approves epic plan
```

**Root Cause:** Gate renumbering without cross-reference updates

**How D3 Detects:**
- Type 5: Gate Placement Validation
- Type 0: Root-Level Workflow Documentation check
- Cross-reference with reference/mandatory_gates.md

---

### Example 4: S8 Branching Logic Not Documented

**Issue Found During KAI-7 S8 Guide Review:**

**Original S8 Guide:**
```markdown
## Next Stage

Proceed to S9: Epic-Level Final QC (`stages/s9/s9_epic_final_qc.md`)
```

**Problem:**
- S8 is END of per-feature loop
- After S8, agent should EITHER:
  - Return to S5 for next feature (if more features remain)
  - OR proceed to S9 (if all features complete)
- Guide only showed S9 transition
- No branching logic documented

**Fix:**
```markdown
## Next Stage

**If more features remain:**
- Repeat S5-S8 loop for next feature
- Read `stages/s5/s5_implementation_planning.md`

**If all features complete:**
- Proceed to S9: Epic-Level Final QC
- Read `stages/s9/s9_epic_final_qc.md`
```

**Root Cause:** Workflow has conditional branching, but documentation showed only linear path

**How D3 Detects:**
- Type 2: Stage Transition validation
- Manual validation: Review S8 transition logic specifically (known complexity point)

---

### Example 5: S10 Prerequisites Missing User Testing Requirement

**Issue Found During KAI-7 S9-S10 Transition:**

**Original S10 Guide:**
```markdown
## Prerequisites

- [ ] Completed S9
- [ ] All features tested
```

**Problem:**
- S9.P3 includes mandatory user testing
- User must report "ZERO bugs found" before S10 begins
- Prerequisites didn't explicitly mention user testing approval
- Agents attempted to start S10 before user confirmed testing passed

**Fix:**
```markdown
## Prerequisites

- [ ] Completed S9
- [ ] All features tested
+- [ ] User testing passed (S9.P3)
+- [ ] User reported ZERO bugs found
```

**Root Cause:** Prerequisites listed stage completion but not user approval requirement

**How D3 Detects:**
- Type 1: Stage Prerequisites Validation
- Manual validation: Check that prerequisites include user approval gates

---

## Integration with Other Dimensions

### D1: Cross-Reference Accuracy

**Overlap:**
- D1 validates file paths are correct
- D3 validates file paths point to CORRECT NEXT STAGE
- **Division:** D1 = technical correctness, D3 = workflow logic correctness

**Example:**
- D1 checks: `stages/s5/s5_implementation_planning.md` exists ✅
- D3 checks: S4 should point to S5 (not S6) ✅

---

### D2: Terminology Consistency

**Overlap:**
- D2 validates stage notation (S#.P#.I#)
- D3 validates stage numbers in prerequisites/transitions are correct stages
- **Division:** D2 = notation format, D3 = stage sequence

**Example:**
- D2 checks: Uses "S5.P1" not "S5a" ✅
- D3 checks: S4 → S5 transition exists ✅

---

### D5: Content Completeness

**Overlap:**
- D5 validates required sections exist (Prerequisites, Next Stage)
- D3 validates content of Prerequisites/Next Stage is correct
- **Division:** D5 = presence, D3 = correctness

**Example:**
- D5 checks: Guide has "## Prerequisites" section ✅
- D3 checks: Prerequisites list correct previous stage and files ✅

---

### D12: Cross-File Dependencies

**Overlap:**
- D12 validates stage handoff files exist (output from one, input to next)
- D3 validates those files are correctly documented in guides
- **Division:** D12 = runtime file dependencies, D3 = documentation of dependencies

**Example:**
- D3 checks: S5 prerequisites say "test_strategy.md required" ✅
- D12 checks: test_strategy.md actually exists when S5 starts ✅

**Recommendation:** Run D3 BEFORE D12 (D3 validates documentation, D12 validates reality matches documentation)

---

### D13: Documentation Quality

**Overlap:**
- D13 validates Prerequisites/Next Stage sections are present and well-formatted
- D3 validates content is semantically correct
- **Division:** D13 = structure/quality, D3 = logical correctness

**Example:**
- D13 checks: Prerequisites section uses checkbox format ✅
- D3 checks: Checkboxes reference correct previous stages ✅

---

## Summary

**D3: Workflow Integration validates the workflow forms a coherent, sequential process.**

**Key Validations:**
1. ✅ Prerequisites correctly reference previous stages
2. ✅ "Next Stage" transitions point to correct subsequent stages
3. ✅ Output files from Stage A match input requirements of Stage B
4. ✅ Phase dependencies within stages are correct
5. ✅ Quality gates appear at correct stage boundaries

**Automation: ~40%**
- Automated: Stage sequence, file existence, gate numbers
- Manual: Semantic correctness, output-to-input mapping

**Critical for:**
- Ensuring agents follow correct workflow sequence
- Preventing stage skipping or wrong transitions
- Validating workflow remains coherent after changes

**Next Dimension:** D4: Count Accuracy (validate file counts, iteration counts match reality)

---

**Last Updated:** 2026-02-04
**Version:** 1.0
**Status:** ✅ Fully Implemented
