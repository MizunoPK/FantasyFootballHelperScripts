# Audit System Update Implementation Plan

**Created:** 2026-02-06
**Purpose:** Implementation plan for audit system enhancements to catch semantic contradictions and workflow flow inconsistencies
**Context:** Gaps identified during KAI-8 epic planning (see AUDIT_FAILURE_ANALYSIS.md, AUDIT_SYSTEM_GAP_ANALYSIS.md)

---

## Executive Summary

**Problem:** The audit system catches structural issues (broken references, stale dates, wrong counts) but misses semantic contradictions (guides making incompatible claims about the same workflow).

**Solution:**
1. Enhance 4 existing dimensions with new pattern types
2. Add new D17: Stage Flow Consistency dimension
3. Update pattern library with semantic validation patterns
4. Add scenario coverage checklists

**Estimated Total Effort:** 12-16 hours

**Priority:** HIGH - These gaps caused 3+ hours of confusion during KAI-8 and will recur

---

## Implementation Overview

| Component | Type | Effort | Priority |
|-----------|------|--------|----------|
| D3: Workflow Description Patterns | Enhancement | 2-3 hours | HIGH |
| D9: Prerequisite-Content Consistency | Enhancement | 1-2 hours | HIGH |
| D14: Cross-Guide Claim Validation | Enhancement | 1-2 hours | MEDIUM |
| D15: Contradiction Detection | Enhancement | 1-2 hours | MEDIUM |
| D17: Stage Flow Consistency | New Dimension | 4-6 hours | HIGH |
| Pattern Library Updates | Enhancement | 1-2 hours | HIGH |
| Pre-Audit Script Updates | Enhancement | 1-2 hours | MEDIUM |

---

## Phase 1: Enhance Existing Dimensions (5-8 hours)

### 1.1 D3: Workflow Integration - Add Workflow Description Patterns

**File:** `feature-updates/guides_v2/audit/dimensions/d3_workflow_integration.md`

**Current State:** D3 validates structural workflow (prerequisites exist, stage transitions valid, file paths correct)

**Gap:** D3 doesn't validate semantic workflow descriptions (text claims about how workflow operates)

**Changes Required:**

#### 1.1.1 Add New Pattern Type (Insert after Type 5: Gate Placement Validation)

```markdown
---

### Type 6: Workflow Description Cross-Validation

**What to Check:**
Text descriptions of workflow behavior must be consistent across all guides.

**Why This Matters:**
Different guides may describe the same workflow differently, creating confusion:
- S1 says "groups complete S2->S3->S4 cycle"
- S2 says "groups complete S2 only, then S3"
- **CONTRADICTION** - agents receive conflicting instructions

**Common Patterns to Search:**

**Pattern 6.1: Stage Sequence Descriptions**
```bash
# Find text that describes stage sequences
grep -rn "S[0-9].*->.*S[0-9]\|S[0-9].*then.*S[0-9]\|S[0-9].*before.*S[0-9]" stages/

# Examples found:
# "groups complete S2->S3->S4 cycle"
# "S2 then S3 then S4"
# "complete S2 before S3"
```

**Pattern 6.2: Group/Parallel Workflow Descriptions**
```bash
# Find text describing when groups matter
grep -rn "group.*complete\|complete.*cycle\|group.*S[0-9]\|parallel.*S[0-9]" stages/

# Cross-validate: Do all findings agree on when groups matter?
```

**Pattern 6.3: Scope Transition Descriptions**
```bash
# Find text describing scope changes (epic/feature/group level)
grep -rn "epic.level\|feature.level\|group.level\|all features\|per feature" stages/
```

**Validation Process:**

1. **Extract all workflow descriptions:**
   ```bash
   # Collect all workflow claims
   grep -rn "S[0-9].*->.*S[0-9]\|complete.*S[0-9].*cycle\|group.*complete" stages/ > /tmp/workflow_claims.txt
   ```

2. **Group by topic:**
   - Stage sequence claims
   - Group handling claims
   - Scope transition claims

3. **Compare for consistency:**
   - All claims about same topic must agree
   - Flag contradictions for manual review

4. **Create contradiction matrix:**
   | Topic | S1 Says | S2 Says | S3 Says | Consistent? |
   |-------|---------|---------|---------|-------------|
   | When groups matter | S2->S3->S4 | S2 only | Unclear | NO |

**Red Flags:**
- S1 says "groups do X" but S2 describes different behavior
- Multiple stages describe same workflow differently
- Scope descriptions contradict each other

**Example Issue (KAI-8):**
```text
S1 Line 600: "Each group completes full S2->S3->S4 cycle"
S2.P2: "After all groups complete S2 -> Proceed to S3"

CONTRADICTION: S1 says groups matter for S3/S4, S2 says groups only matter for S2
```

**Automated:** Partial - Can find workflow descriptions, requires manual consistency check
```

#### 1.1.2 Update Validation Checklist (Add to existing checklist)

Add to "Validation Checklist" section:

```markdown
**Workflow Description Consistency:**
- [ ] All guides agree on stage sequence (S1->S2->...->S10)
- [ ] All guides agree on when groups/parallelization matters
- [ ] All guides agree on scope transitions (epic->feature->epic)
- [ ] No contradictory workflow descriptions across files
```

#### 1.1.3 Update Integration Section

Add to "Integration with Other Dimensions":

```markdown
### D17: Stage Flow Consistency

**Overlap:**
- D3 validates workflow descriptions are internally consistent
- D17 validates workflow behavior is consistent across stage transitions
- **Division:** D3 = within-stage, D17 = across-stage boundaries

**Example:**
- D3 checks: S2 workflow descriptions don't contradict each other
- D17 checks: S2's exit behavior matches S3's entry expectations
```

**Effort:** 2-3 hours

---

### 1.2 D9: Intra-File Consistency - Add Prerequisite-Content Validation

**File:** `feature-updates/guides_v2/audit/dimensions/d9_intra_file_consistency.md`

**Current State:** D9 validates notation, terminology, and contradictory instructions within files

**Gap:** D9 doesn't specifically check if prerequisites contradict file's own content

**Changes Required:**

#### 1.2.1 Add New Pattern Type (Insert after Type 7: Example-to-Principle Consistency)

```markdown
---

### Type 8: Prerequisite-Content Consistency

**What to Check:**
A file's prerequisites section must not contradict its own body content.

**Why This Matters:**
Prerequisites set expectations for what must be true before the stage runs. If content describes behavior that contradicts prerequisites, agents receive conflicting guidance.

**Common Contradiction Pattern:**

**Prerequisites say:**
```markdown
## Prerequisites

- [ ] ALL features must complete S2 before starting S3
```

**Content says:**
```markdown
## Dependency Groups Section

S3 runs ONCE PER ROUND (not just once at end):
- **Round 1 S3:** Validate Group 1 features only
- **Round 2 S3:** Validate Group 2 features + Group 1
```

**CONTRADICTION:**
- Prerequisites: "ALL features complete S2 first" (epic-level)
- Content: "Round 1: Group 1 features only" (implies group-level, not all features)

**Search Commands:**

```bash
# Step 1: Find files with "ALL" in prerequisites
grep -l "^## Prerequisites" stages/**/*.md | while read file; do
  has_all=$(grep -A 15 "^## Prerequisites" "$file" | grep -i "ALL\|all features\|every feature")
  if [ -n "$has_all" ]; then
    echo "=== $file ==="
    echo "Prerequisites: $has_all"

    # Step 2: Check for group/round-based content
    has_groups=$(grep -i "Round [0-9]:.*Group\|Group [0-9].*only\|per group" "$file")
    if [ -n "$has_groups" ]; then
      echo "Content: $has_groups"
      echo "POTENTIAL CONTRADICTION"
    fi
  fi
done
```

**Validation Checklist:**

For each stage guide:
- [ ] If prerequisites say "ALL features/stages complete" → content doesn't describe per-group execution
- [ ] If prerequisites say "per feature" → content doesn't assume epic-level context
- [ ] Scope in prerequisites matches scope in content
- [ ] Timing in prerequisites matches timing described in content

**Example Issue (KAI-8):**

**File:** `stages/s3/s3_epic_planning_approval.md`

**Prerequisites (Line 46):**
```markdown
- ALL features have completed S2 (Feature Deep Dives)
```

**Content (Lines 67-71):**
```markdown
S3 runs ONCE PER ROUND (not just once at end):
- **Round 1 S3:** Validate Group 1 features against each other
- **Round 2 S3:** Validate Group 2 features against ALL Group 1 features
```

**Analysis:**
- Prerequisites say "ALL features complete S2 first"
- Content says "Round 1 S3: Group 1 features" (implies S3 starts before all features complete S2)
- **CONTRADICTION** within same file

**Red Flags:**
- "ALL" in prerequisites + "Round/Group X only" in content
- "Per feature" in prerequisites + "epic-level" in content
- Different timing assumptions between sections

**Automated:** Partial - Can find keyword patterns, requires semantic validation
```

#### 1.2.2 Update Summary Section

Add to Key Validations list:

```markdown
8. ⚠️ Prerequisite-content consistency (prerequisites don't contradict body)
```

**Effort:** 1-2 hours

---

### 1.3 D14: Content Accuracy - Add Cross-Guide Claim Validation

**File:** `feature-updates/guides_v2/audit/dimensions/d14_content_accuracy.md`

**Current State:** D14 validates claims against implementation (file counts, script existence, stale dates)

**Gap:** D14 doesn't validate claims in Guide A against claims in Guide B

**Changes Required:**

#### 1.3.1 Add New Pattern Type (Insert after Type 4: Feature/Capability Claims)

```markdown
---

### Type 5: Cross-Guide Claim Consistency

**What to Check:**
Claims about the same topic made in different guides must agree with each other.

**Why This Matters:**
Different guides may make incompatible claims about the same workflow:
- Guide A claims X works one way
- Guide B claims X works differently
- Both can't be correct

**This differs from D14's other checks:**
- Types 1-4: Claims vs implementation (do claims match reality?)
- Type 5: Claims vs claims (do guides agree with each other?)

**Common Topics to Cross-Validate:**

| Topic | Guides to Compare | What Must Agree |
|-------|-------------------|-----------------|
| Group workflow | S1, S2, S3, S4 | When do groups matter? |
| Parallel work | S1, S2, parallel_work/ | How does parallelization work? |
| Stage sequence | All stage guides | S1->S2->...->S10 |
| Gate requirements | Stage guides, mandatory_gates.md | Gate numbers and locations |

**Search Commands:**

```bash
# Find all claims about group workflow
grep -rn "group.*S[0-9]\|S[0-9].*group\|group.*complete\|complete.*cycle" stages/ > /tmp/group_claims.txt

# Review for consistency
cat /tmp/group_claims.txt | sort

# Expected: All claims describe same workflow
# Error: Different claims describe different workflows
```

**Validation Process:**

1. **Identify high-value topics:**
   - Group-based parallelization
   - Stage sequence
   - Gate placement
   - Scope transitions

2. **For each topic, extract all claims:**
   ```bash
   grep -rn "[topic pattern]" stages/ reference/
   ```

3. **Compare claims:**
   - Do all claims agree?
   - If not, which is correct?
   - Flag contradictions

4. **Document in validation matrix:**
   | Topic | File | Claim | Consistent? |
   |-------|------|-------|-------------|
   | Group workflow | s1_epic_planning.md:600 | "groups do S2->S3->S4" | |
   | Group workflow | s2_feature_deep_dive.md:157 | "groups do S2 only" | NO |

**Example Issue (KAI-8):**

**Topic:** When do groups matter?

**S1 Claim (Line 600):**
```markdown
Each group completes full S2->S3->S4 cycle before next group starts
```

**S2 Claim (Lines 150-157):**
```markdown
After S2.P2:
- If all groups done → Proceed to S3
```

**Analysis:**
- S1 says groups matter for S2, S3, AND S4
- S2 says groups only matter for S2, then S3 is epic-level
- **CONTRADICTION**

**Red Flags:**
- Different guides describe same workflow differently
- Claims use different scope (epic vs feature vs group)
- Timing claims conflict

**Automated:** Partial - Can extract claims, requires manual consistency check
```

**Effort:** 1-2 hours

---

### 1.4 D15: Duplication Detection - Add Contradiction Detection

**File:** `feature-updates/guides_v2/audit/dimensions/d15_duplication_detection.md`

**Current State:** D15 finds duplicate content for DRY principle enforcement

**Gap:** D15 doesn't find contradictory content (same topic, different claims)

**Changes Required:**

#### 1.4.1 Add New Pattern Type (Insert after Type 7: Template Content Propagation)

```markdown
---

### Type 8: Contradictory Content Detection

**What to Check:**
Multiple files describing the same concept must not contradict each other.

**Key Distinction from Duplication:**
- **Duplication (Types 1-7):** Same content copied → maintenance burden
- **Contradiction (Type 8):** Different claims about same topic → confusion

**Why This Belongs in D15:**
Both duplication and contradiction involve multiple files describing the same thing:
- Duplication: Same thing, same words (redundant)
- Contradiction: Same thing, incompatible words (incorrect)

**Common Contradiction Patterns:**

**Pattern 8.1: Workflow Sequence Contradictions**
```text
File A: "Groups complete S2->S3->S4 cycle before next group starts"
File B: "After all groups complete S2, proceed to S3 (epic-level)"

Same topic (group workflow), incompatible claims
```

**Pattern 8.2: Scope Contradictions**
```text
File A: "S3 runs at epic-level (all features together)"
File B: "Round 1 S3: Group 1 features only"

Same topic (S3 scope), incompatible claims
```

**Pattern 8.3: Timing Contradictions**
```text
File A: "ALL features must complete S2 before S3 starts"
File B: "S3 Round 1 runs after Group 1 completes S2"

Same topic (S3 timing), incompatible claims
```

**Search Strategy:**

```bash
# Step 1: Identify topic clusters
topics=(
  "group.*workflow\|workflow.*group"
  "S3.*scope\|scope.*S3"
  "parallel.*S2\|S2.*parallel"
)

# Step 2: For each topic, extract all claims
for topic in "${topics[@]}"; do
  echo "=== Topic: $topic ==="
  grep -rn "$topic" stages/ | head -20
done

# Step 3: Manual review for contradictions
```

**Validation Process:**

1. **Identify topic to validate** (e.g., "group workflow")

2. **Extract all claims about topic:**
   ```bash
   grep -rn "group.*complete\|complete.*group\|group.*S[0-9]" stages/
   ```

3. **Categorize claims:**
   - Claim A: Groups do X
   - Claim B: Groups do Y
   - Are X and Y compatible?

4. **Determine correct claim:**
   - Which matches intended workflow?
   - Which should be updated?

5. **Flag contradictions:**
   ```markdown
   CONTRADICTION FOUND:
   - File: s1_epic_planning.md:600
   - Claim: "groups complete S2->S3->S4 cycle"
   - Contradicts: s2_feature_deep_dive.md:157 ("groups complete S2 only")
   - Resolution: [Determine correct behavior]
   ```

**Example Issue (KAI-8):**

**Topic:** Group workflow

**Claims Found:**

| File | Line | Claim |
|------|------|-------|
| s1_epic_planning.md | 600 | "Each group completes full S2->S3->S4 cycle" |
| s2_feature_deep_dive.md | 157 | "After all groups done → Proceed to S3" |
| s3_epic_planning_approval.md | 46 | "ALL features complete S2" (prerequisite) |
| s3_epic_planning_approval.md | 67 | "Round 1 S3: Group 1 features" (content) |

**Contradiction Matrix:**

| Claim | S2->S3->S4 per group | S2 only, then S3 epic |
|-------|---------------------|----------------------|
| S1:600 | YES | |
| S2:157 | | YES |
| S3:46 | | YES |
| S3:67 | Partial (implies per-group S3) | |

**Resolution:** S2:157 and S3:46 are correct (groups matter for S2 only). S1:600 and S3:67 need updating.

**Red Flags:**
- Multiple claims about same workflow feature
- Claims describe incompatible behaviors
- One "ALL" claim contradicted by "per group" claim

**Automated:** Partial - Can cluster claims by topic, requires manual contradiction detection
```

#### 1.4.2 Update Summary Section

Add to Key Validations:

```markdown
8. ⚠️ Contradiction detection (same topic, incompatible claims)
```

**Effort:** 1-2 hours

---

## Phase 2: Create New D17 Dimension (4-6 hours)

### 2.1 Create D17: Stage Flow Consistency

**File:** `feature-updates/guides_v2/audit/dimensions/d17_stage_flow_consistency.md`

**Purpose:** Validate behavioral continuity and semantic consistency between adjacent stages

**Full Dimension Content:**

```markdown
# D17: Stage Flow Consistency

**Dimension Number:** 17
**Category:** Advanced Dimensions
**Automation Level:** 30% automated
**Priority:** HIGH
**Last Updated:** 2026-02-06

**Focus:** Ensure behavioral continuity and semantic consistency between adjacent workflow stages
**Typical Issues Found:** 5-15 per major workflow change

---

## Table of Contents

1. [What This Checks](#what-this-checks)
2. [Why This Matters](#why-this-matters)
3. [How This Differs From D3](#how-this-differs-from-d3)
4. [Pattern Types](#pattern-types)
5. [Stage Transition Checklists](#stage-transition-checklists)
6. [How Errors Happen](#how-errors-happen)
7. [Automated Validation](#automated-validation)
8. [Manual Validation](#manual-validation)
9. [Context-Sensitive Rules](#context-sensitive-rules)
10. [Real Examples](#real-examples)
11. [Integration with Other Dimensions](#integration-with-other-dimensions)

---

## What This Checks

**D17: Stage Flow Consistency** validates that adjacent stages agree on workflow behavior:

1. **Handoff Promises** - What Stage N promises to deliver matches what Stage N+1 expects
2. **Workflow Behavior** - How Stage N describes workflow matches how Stage N+1 operates
3. **Conditional Logic** - Branching in Stage N matches entry conditions in Stage N+1
4. **Terminology Alignment** - Terms introduced in Stage N used consistently in Stage N+1
5. **Scope Alignment** - Epic/feature/group scope is consistent across transitions

**Coverage:**
- All 9 stage transitions (S1→S2, S2→S3, ..., S9→S10)
- Branching transitions (S8→S5 loop, S8→S9 exit)
- Parallel work transitions (Primary→Secondary handoffs)

---

## Why This Matters

**Flow inconsistencies = Agents receive conflicting instructions at stage boundaries**

### Impact of Flow Inconsistencies:

**Handoff Mismatches:**
- Stage N promises to produce X
- Stage N+1 expects Y
- Agent confused about what inputs to use
- Example: S1 says "groups cycle through S2-S4", S2 only handles groups for S2

**Scope Confusion:**
- Stage N operates at group level
- Stage N+1 assumes epic level
- Agent unsure which scope applies
- Example: S2 says "proceed to S3 (epic-level)", S3 content says "Round 1: Group 1"

**Conditional Logic Gaps:**
- Stage N produces multiple modes (sequential, parallel, group-based)
- Stage N+1 only handles some modes
- Agent enters unhandled state
- Example: S1 produces "group-based parallel", S2 router doesn't route it

### Historical Evidence (KAI-8):

The group-based parallelization issue was a flow consistency problem:
- S1 promised groups would cycle through S2→S3→S4
- S2 only implemented groups for S2
- S3 had internal confusion about group vs epic scope
- **Result:** 3+ hours of confusion, 8 guide gaps identified

---

## How This Differs From D3

| Aspect | D3: Workflow Integration | D17: Stage Flow Consistency |
|--------|-------------------------|----------------------------|
| **Focus** | Structural references | Behavioral continuity |
| **Checks** | File paths valid, prerequisites exist | Workflow descriptions align |
| **Scope** | Within-stage validation | Cross-stage boundary validation |
| **Example Pass** | "S2 → S3 file path valid" | |
| **Example Fail** | | "S2 says epic-level S3, S3 says group-level" |

**D3 catches:** "S2 says Next: S4" (wrong stage number - structural)
**D17 catches:** "S2 says groups end at S2, S1 says groups continue to S4" (contradictory behavior - semantic)

**Complementary relationship:**
- Run D3 first (ensure structure is valid)
- Run D17 second (ensure behavior is consistent)

---

## Pattern Types

### Type 1: Handoff Promise Validation

**What to Check:**
What Stage N promises to deliver must match what Stage N+1 expects to receive.

**Validation Process:**

1. **Extract Stage N exit promises:**
   ```bash
   # Find what Stage N says it produces/hands off
   grep -A 15 "^## Next Stage\|^## Outputs\|^## Exit Criteria\|^## Transition" stages/sN/*.md
   ```

2. **Extract Stage N+1 entry expectations:**
   ```bash
   # Find what Stage N+1 expects to receive
   grep -A 15 "^## Prerequisites\|^## Inputs\|^## Entry\|^## Assumes" stages/s(N+1)/*.md
   ```

3. **Compare:**
   - File outputs match file inputs?
   - Workflow state descriptions match?
   - Scope/level descriptions match?

**Checklist:**
- [ ] Stage N output files listed in Stage N+1 prerequisites
- [ ] Stage N workflow exit description matches Stage N+1 workflow entry
- [ ] Stage N scope (epic/feature/group) matches Stage N+1 scope assumption
- [ ] Stage N conditional branches all handled by Stage N+1

**Red Flags:**
- Stage N produces file X, Stage N+1 expects file Y
- Stage N says "workflow continues with X", Stage N+1 doesn't mention X
- Stage N operates at group scope, Stage N+1 assumes epic scope

---

### Type 2: Workflow Behavior Alignment

**What to Check:**
How Stage N describes workflow mechanics must match how Stage N+1 operates.

**Key Questions Per Transition:**

| Transition | Key Alignment Question |
|------------|------------------------|
| S1→S2 | Does S1's parallelization description match S2's handling? |
| S2→S3 | Does S2's "proceed to S3" condition match S3's prerequisites? |
| S3→S4 | Does S3's scope (epic/group) match S4's scope? |
| S4→S5 | Does S4's test strategy integrate into S5's planning? |
| S5→S6 | Does S5's plan format match S6's execution expectations? |
| S6→S7 | Does S6's completion state match S7's entry assumptions? |
| S7→S8 | Does S7's commit status match S8's alignment assumptions? |
| S8→S5 | Does S8's loop-back condition match S5's re-entry handling? |
| S8→S9 | Does S8's exit condition match S9's prerequisites? |
| S9→S10 | Does S9's QC completion match S10's entry requirements? |

**Search Commands:**
```bash
# Extract workflow descriptions from Stage N
grep -n "proceed\|after.*complete\|when.*done\|workflow" stages/sN/*.md

# Extract workflow assumptions from Stage N+1
grep -n "prerequisite\|assumes\|expect\|after" stages/s(N+1)/*.md

# Compare for consistency
```

---

### Type 3: Conditional Logic Consistency

**What to Check:**
All branching paths from Stage N must be handled by target stages.

**Critical Branching Points:**

**S1 → S2 Branch:**
```text
S1 can produce:
- Sequential mode (user declined parallel)
- Full parallel mode (all features independent)
- Group-based parallel mode (features have dependencies)

S2 must handle:
- [ ] Sequential mode routing
- [ ] Full parallel mode routing
- [ ] Group-based parallel mode routing ← Often missed
```

**S8 → S5 or S9 Branch:**
```text
S8 can produce:
- More features remain (loop to S5)
- All features complete (proceed to S9)

S5 must handle:
- [ ] Re-entry for next feature
- [ ] Context from previous feature

S9 must handle:
- [ ] All features committed
- [ ] Ready for epic-level QC
```

**Validation:**
```bash
# Find all conditional logic in Stage N
grep -n "if\|when\|scenario\|mode\|option" stages/sN/*.md

# For each condition, verify target stage handles it
```

**Red Flags:**
- Stage N has 3 modes, Stage N+1 router only handles 2
- Stage N branching logic doesn't clearly map to Stage N+1 entries
- Conditional text in Stage N doesn't appear in Stage N+1

---

### Type 4: Terminology Alignment

**What to Check:**
Terms introduced or defined in Stage N must be used consistently in Stage N+1.

**Common Terms to Track:**

| Term | Defined In | Must Be Consistent In |
|------|-----------|----------------------|
| "Dependency Group" | S1 | S2, S3 |
| "Spec-level dependency" | S1 | S2 |
| "Implementation dependency" | S1 | S5, S6 |
| "Epic-level" | S1 | All stages |
| "Feature-level" | S1 | S2, S4, S5-S8 |
| "Consistency Loop" | S2 | S4, S5, S7, S9 |

**Search Commands:**
```bash
# Find term definition
grep -n "dependency group" stages/s1/*.md

# Find term usage in subsequent stages
grep -rn "dependency group" stages/s{2,3,4}/*.md

# Compare: Is meaning preserved?
```

**Red Flags:**
- Term defined one way in Stage N, used differently in Stage N+1
- Term introduced without definition, meaning unclear
- Stage N+1 redefines term with different meaning

---

### Type 5: Scope Alignment

**What to Check:**
Scope transitions (epic→feature→group→epic) must be explicit and consistent.

**Standard Scope Progression:**

| Stage | Typical Scope | Transition |
|-------|--------------|------------|
| S1 | Epic (planning whole epic) | → S2 (feature-level) |
| S2 | Feature (within groups?) | → S3 (epic-level) |
| S3 | Epic (cross-feature sanity) | → S4 (feature-level) |
| S4 | Feature (test strategy) | → S5 (feature-level) |
| S5-S8 | Feature (implementation loop) | → S5 or S9 |
| S9 | Epic (final QC) | → S10 (epic-level) |
| S10 | Epic (cleanup, PR) | → Done |

**Validation:**

For each transition:
- [ ] Stage N explicitly states its scope
- [ ] Stage N+1 explicitly states its scope
- [ ] Scope transition is clear (if changing)
- [ ] No ambiguity about current scope

**Example Issue (KAI-8):**

**S2 Exit Scope:** "Proceed to S3 (epic-level)"
**S3 Entry Scope:** Prerequisites say "ALL features" (epic)
**S3 Content Scope:** "Round 1 S3: Group 1 features" (group)

**INCONSISTENCY:** S3 has mixed scope signals

---

## Stage Transition Checklists

### S1 → S2 Transition Checklist

```markdown
## S1 → S2 Flow Validation

### Handoff Promises
- [ ] S1 outputs (epic folder, feature folders, DISCOVERY.md) listed in S2 prerequisites
- [ ] S1 parallelization mode decision documented for S2 routing
- [ ] S1 dependency groups (if any) documented for S2 handling

### Workflow Behavior
- [ ] S1's parallelization description matches S2's parallel work handling
- [ ] S1's sequential description matches S2's sequential handling
- [ ] S1's group-based description matches S2's group-based handling

### Conditional Logic
- [ ] All S1 parallelization modes (sequential, full-parallel, group-based) routed in S2
- [ ] S2 router explicitly handles each mode S1 can produce

### Terminology
- [ ] "Dependency group" defined in S1, used consistently in S2
- [ ] "Spec-level dependency" defined in S1, applied correctly in S2

### Scope
- [ ] S1 operates at epic scope (clear)
- [ ] S2 operates at feature scope (clear)
- [ ] Transition from epic to feature is explicit
```

### S2 → S3 Transition Checklist

```markdown
## S2 → S3 Flow Validation

### Handoff Promises
- [ ] S2 outputs (spec.md, checklist.md for all features) match S3 prerequisites
- [ ] S2's "when to proceed to S3" matches S3's prerequisites

### Workflow Behavior
- [ ] S2 says "after all features complete S2" matches S3 prerequisite "all features complete S2"
- [ ] S2's scope at exit (epic-level) matches S3's scope at entry

### Scope
- [ ] S2 exits with all features having completed S2 (epic-level aggregation)
- [ ] S3 enters at epic level (cross-feature sanity check)
- [ ] No group-level language in S3 that contradicts epic-level entry
```

### S8 → S5/S9 Transition Checklist

```markdown
## S8 → S5 (Loop) or S9 (Exit) Flow Validation

### Branching Logic
- [ ] S8 clearly defines "more features remain" vs "all features complete"
- [ ] S8 → S5 transition documented (which feature next, context preserved)
- [ ] S8 → S9 transition documented (prerequisites for S9)

### S5 Re-Entry Handling
- [ ] S5 handles re-entry (not just first entry)
- [ ] Context from previous features preserved
- [ ] S8 alignment updates reflected in S5 planning

### S9 Entry Requirements
- [ ] S9 prerequisites match what S8 produces when "all features complete"
- [ ] All features committed (S8 exit state)
- [ ] Ready for epic-level QC (scope transition)
```

*[Include checklists for all 9 transitions]*

---

## How Errors Happen

### Root Cause 1: Stages Authored Independently

**Scenario:**
- S1 author describes group workflow one way
- S2 author, unaware of S1's description, describes it differently
- S3 author adds group-based content without checking S1/S2

**Result:** Three stages have incompatible descriptions of same workflow

**Prevention:** D17 validation after any stage guide changes

---

### Root Cause 2: Workflow Evolution Without Cascade Updates

**Scenario:**
- Original design: Groups matter for S2, S3, S4
- Decision made: Groups only matter for S2
- S2 updated with new behavior
- S1 and S3 not updated

**Result:** S1 still describes old behavior, S3 has remnant group-based content

**Prevention:** D17 validation after workflow design changes

---

### Root Cause 3: Copy-Paste from Wrong Stage

**Scenario:**
- Creating S3 guide
- Copy-paste workflow description from S2
- S2's description doesn't apply to S3 (different scope)
- Don't notice the mismatch

**Result:** S3 content doesn't match S3's actual workflow

**Prevention:** D17 Type 2 (Workflow Behavior Alignment) validation

---

## Automated Validation

### Script: Stage Flow Consistency Pre-Check

```bash
#!/bin/bash
# CHECK: Stage Flow Consistency (D17)
# ============================================================================

echo "=== D17: Stage Flow Consistency Checks ==="

# Check 1: Workflow description consistency
echo ""
echo "--- Workflow Description Claims ---"
echo "Claims about group workflow:"
grep -rn "group.*S[0-9].*->.*S[0-9]\|group.*complete.*S[0-9]\|S[0-9].*cycle" stages/
echo ""
echo "Review above for contradictions (different stages saying different things)"

# Check 2: Scope language at transitions
echo ""
echo "--- Scope Language at Stage Exits ---"
for stage in {1..9}; do
  echo "S$stage exit scope:"
  grep -n "proceed.*S$((stage+1))\|epic.level\|feature.level\|all features" stages/s$stage/*.md 2>/dev/null | head -3
done

# Check 3: Parallelization mode coverage
echo ""
echo "--- S2 Router Mode Coverage ---"
echo "S1 can produce these modes:"
grep -n "sequential\|parallel\|group" stages/s1/*.md | grep -i "mode\|option\|scenario" | head -5
echo ""
echo "S2 router handles:"
grep -n "sequential\|parallel\|group" stages/s2/s2_feature_deep_dive.md | head -5
echo ""
echo "Verify all S1 modes are handled in S2 router"

# Check 4: Prerequisites vs content scope
echo ""
echo "--- Prerequisite-Content Scope Alignment ---"
for file in stages/**/*.md; do
  prereq_all=$(grep -A 10 "^## Prerequisites" "$file" 2>/dev/null | grep -i "ALL features\|all.*complete")
  content_group=$(grep -i "Round [0-9]:.*Group\|Group [0-9].*only" "$file" 2>/dev/null)

  if [ -n "$prereq_all" ] && [ -n "$content_group" ]; then
    echo "POTENTIAL CONFLICT in $file:"
    echo "  Prerequisites: $prereq_all"
    echo "  Content: $content_group"
  fi
done

echo ""
echo "=== D17 Pre-Check Complete ==="
echo "Manual review required for semantic validation"
```

### Automation Coverage: ~30%

**Automated:**
- Finding workflow description claims
- Extracting scope language
- Detecting keyword patterns (group, parallel, sequential)
- Finding potential prerequisite-content conflicts

**Manual Required:**
- Determining if claims actually contradict
- Understanding semantic meaning of workflow descriptions
- Validating behavioral consistency
- Deciding which claim is correct

---

## Manual Validation

### Manual Process (Stage Flow Audit)

**Duration:** 60-90 minutes
**Frequency:** After stage guide changes, workflow updates, major restructuring

**Step 1: Prepare Transition Inventory (10 min)**

```bash
# List all stage transitions to validate
transitions=(
  "S1→S2" "S2→S3" "S3→S4" "S4→S5"
  "S5→S6" "S6→S7" "S7→S8"
  "S8→S5" "S8→S9" "S9→S10"
)

# For each, extract exit and entry content
for trans in "${transitions[@]}"; do
  src="${trans%→*}"  # e.g., S1
  dst="${trans#*→}"  # e.g., S2
  echo "=== $trans ===" > /tmp/transition_$trans.txt
  echo "--- $src Exit ---" >> /tmp/transition_$trans.txt
  grep -A 10 "^## Next Stage\|^## Exit\|^## Transition" stages/$src/*.md >> /tmp/transition_$trans.txt
  echo "--- $dst Entry ---" >> /tmp/transition_$trans.txt
  grep -A 10 "^## Prerequisites\|^## Entry" stages/$dst/*.md >> /tmp/transition_$trans.txt
done
```

**Step 2: Validate Each Transition (5-10 min each)**

For each transition file:
1. Read Stage N exit description
2. Read Stage N+1 entry description
3. Check: Do they describe same workflow state?
4. Check: Is scope consistent?
5. Check: Are all conditional branches covered?
6. Document findings

**Step 3: Validate Workflow Description Consistency (15 min)**

```bash
# Extract all workflow descriptions
grep -rn "S[0-9].*->.*S[0-9]\|complete.*cycle\|group.*complete" stages/ > /tmp/workflow_claims.txt

# Group by topic
# Compare: Do all claims agree?
# Flag contradictions
```

**Step 4: Validate Scope Transitions (10 min)**

For each stage boundary:
- What scope is Stage N operating at?
- What scope does Stage N+1 expect?
- Is transition explicit or implicit?
- Any conflicting scope signals?

**Step 5: Document Findings (10 min)**

```markdown
## D17 Flow Consistency Findings

### Transitions Validated
- [ ] S1→S2: [PASS/FAIL]
- [ ] S2→S3: [PASS/FAIL]
- ...

### Issues Found
1. [Transition]: [Issue description]
2. ...

### Contradictions Detected
| File A | File B | Topic | Contradiction |
|--------|--------|-------|---------------|
| ... | ... | ... | ... |
```

---

## Context-Sensitive Rules

### Rule 1: Intentional Scope Transitions

**Context:** Some scope transitions are intentional and documented.

**Example:**
```markdown
S2 → S3:
S2 operates at feature level
S3 operates at epic level
Transition is intentional: aggregate all feature specs for cross-feature sanity check
```

**Validation:** If scope change is documented and intentional → VALID

---

### Rule 2: Parallel Work Creates Non-Linear Flow

**Context:** Parallel work coordination breaks linear S1→S2→S3 flow.

**Example:**
```markdown
Primary agent: S1 → S2 (Feature 1) → coordinate
Secondary agents: S2 (Features 2-N) simultaneously
All agents: → S3 (after all complete)
```

**Validation:** Non-linear flow in parallel work is expected → VALID

---

### Rule 3: S8 Loop Creates Multiple Entry Points

**Context:** S5 can be entered from S4 (first time) or S8 (loop).

**Example:**
```markdown
First feature: S4 → S5
Subsequent features: S8 → S5 (loop back)
```

**Validation:** S5 must handle both entry points → Check both are documented

---

## Real Examples

### Example 1: Group Workflow Contradiction (KAI-8)

**Issue Found:**

**S1 Exit (Line 600):**
```markdown
Workflow: Each group completes full S2->S3->S4 cycle before next group starts
```

**S2 Operation (Lines 150-157):**
```markdown
After S2.P2:
- If all groups done → Proceed to S3
```

**Analysis:**
- S1 promises: Groups cycle through S2, S3, AND S4
- S2 implements: Groups only matter for S2, then S3 is epic-level
- **FLOW INCONSISTENCY**

**Impact:**
- Agent following S1 expects group-based S3
- Agent reaching S2 finds epic-level S3
- Confusion about workflow

**Fix:**
- Update S1 to say "Groups complete S2 only, then proceed to S3 (epic-level)"
- Ensure S2 and S1 describe same workflow

**How D17 Detects:**
- Type 1: Handoff Promises (S1 promises differ from S2 behavior)
- Type 2: Workflow Behavior Alignment (descriptions don't match)

---

### Example 2: S3 Internal Scope Conflict

**Issue Found:**

**S3 Prerequisites (Line 46):**
```markdown
- ALL features have completed S2 (Feature Deep Dives)
```

**S3 Content (Lines 67-71):**
```markdown
S3 runs ONCE PER ROUND (not just once at end):
- Round 1 S3: Validate Group 1 features against each other
```

**Analysis:**
- Prerequisites say "ALL features" (epic-level)
- Content says "Round 1: Group 1" (group-level)
- **INTERNAL SCOPE CONFLICT**

**Note:** This is also caught by D9 (intra-file consistency), but D17 would flag it when validating S2→S3 transition (S2 says epic-level S3, S3 content says group-level).

**How D17 Detects:**
- Type 5: Scope Alignment (S2 exit scope doesn't match S3 content scope)

---

### Example 3: Missing S2 Router Mode

**Issue Found:**

**S1 Produces (Step 5.9):**
```markdown
Parallelization modes:
1. Sequential (user declined)
2. Full parallel (all features independent)
3. Group-based parallel (features have dependencies)
```

**S2 Router Handles:**
```markdown
### Are You a Secondary Agent? [handles #2]
### Are You Primary Agent in Parallel Mode? [handles #2]
### Are You in Sequential Mode? [handles #1]
[Missing: Group-based parallel mode]
```

**Analysis:**
- S1 can produce 3 modes
- S2 router only handles 2 modes
- Group-based parallel mode falls through

**Impact:**
- Agent with group-based epic reaches S2
- No routing guidance
- Agent confused about which guide to follow

**Fix:**
- Add "Are You Primary Agent in Group-Based Parallel Mode?" to S2 router
- Create s2_primary_agent_group_wave_guide.md

**How D17 Detects:**
- Type 3: Conditional Logic Consistency (S1 branches not all handled in S2)

---

## Integration with Other Dimensions

| Dimension | Relationship to D17 |
|-----------|---------------------|
| **D3: Workflow Integration** | D3 = structural (links valid), D17 = behavioral (content matches) |
| **D9: Intra-File Consistency** | D9 = within file, D17 = across stage boundary |
| **D14: Content Accuracy** | D14 = claims vs reality, D17 = claims vs claims across stages |
| **D15: Duplication Detection** | D15 = same content copied, D17 = contradictory content |

**Recommended Audit Order:**
1. D3 (structural validation)
2. D17 (behavioral validation)
3. D9 (within-file validation)
4. D15 (duplication/contradiction)

---

## Summary

**D17: Stage Flow Consistency validates behavioral continuity across stage transitions.**

**Key Validations:**
1. ⚠️ Handoff promises match expectations
2. ⚠️ Workflow behavior aligned across stages
3. ⚠️ Conditional logic fully covered
4. ⚠️ Terminology used consistently
5. ⚠️ Scope transitions explicit and consistent

**Automation: ~30%**
- Automated for finding claims and patterns
- Manual for semantic validation and contradiction detection

**Critical for:**
- Ensuring agents receive consistent instructions across stage boundaries
- Preventing workflow gaps when stages authored independently
- Catching contradictions before they cause confusion

---

**Last Updated:** 2026-02-06
**Version:** 1.0
**Status:** NEW DIMENSION
```

**Effort:** 4-6 hours

---

## Phase 3: Update Supporting Files (2-4 hours)

### 3.1 Update Pattern Library

**File:** `feature-updates/guides_v2/audit/reference/pattern_library.md`

**Add new section:**

```markdown
---

## Workflow Description Patterns (D3, D17)

### Pattern W1: Stage Sequence Descriptions

```bash
# Find text describing stage sequences
grep -rn "S[0-9].*->.*S[0-9]\|S[0-9].*then.*S[0-9]" stages/

# Find cycle/loop descriptions
grep -rn "complete.*cycle\|cycle.*complete" stages/
```

### Pattern W2: Group Workflow Descriptions

```bash
# Find text about when groups matter
grep -rn "group.*complete\|group.*S[0-9]\|S[0-9].*group" stages/

# Find parallel work descriptions
grep -rn "parallel.*S[0-9]\|S[0-9].*parallel\|wave" stages/
```

### Pattern W3: Scope Descriptions

```bash
# Find scope language
grep -rn "epic.level\|feature.level\|group.level\|all features\|per feature" stages/

# Find scope transitions
grep -rn "proceed to.*level\|transition to.*level" stages/
```

### Pattern W4: Cross-Stage Comparison

```bash
# Extract workflow claims for comparison
for stage in {1..10}; do
  echo "=== S$stage workflow claims ==="
  grep -n "group\|parallel\|scope\|level" stages/s$stage/*.md | head -10
done
```

---

## Contradiction Detection Patterns (D15, D17)

### Pattern C1: Find Contradictory Keywords

```bash
# Find "ALL" claims
grep -rn "ALL features\|all.*complete\|every feature" stages/

# Find "per group" claims
grep -rn "Group [0-9]\|per group\|Round [0-9]:.*Group" stages/

# If both exist for same topic → potential contradiction
```

### Pattern C2: Prerequisite-Content Conflicts

```bash
# For each file, check prerequisite scope vs content scope
for file in stages/**/*.md; do
  prereq=$(grep -A 10 "^## Prerequisites" "$file" | grep -i "ALL\|every\|all features")
  content=$(grep -i "Round [0-9]:.*Group\|Group [0-9].*only\|per group" "$file")

  if [ -n "$prereq" ] && [ -n "$content" ]; then
    echo "POTENTIAL CONFLICT: $file"
  fi
done
```
```

**Effort:** 1-2 hours

---

### 3.2 Update Pre-Audit Script

**File:** `feature-updates/guides_v2/audit/scripts/pre_audit_checks.sh`

**Add new checks:**

```bash
# ============================================================================
# CHECK: Workflow Description Consistency (D3, D17)
# ============================================================================

echo ""
echo "=== Workflow Description Consistency (D3, D17) ==="

# Find all workflow sequence claims
echo "Workflow sequence claims:"
grep -rn "S[0-9].*->.*S[0-9]" stages/ 2>/dev/null | head -10
echo ""
echo "Review above: Do all claims describe same workflow sequence?"

# Find group workflow claims
echo ""
echo "Group workflow claims:"
grep -rn "group.*complete\|complete.*group\|group.*S[0-9]" stages/ 2>/dev/null | head -10
echo ""
echo "Review above: Do all claims agree on when groups matter?"

# ============================================================================
# CHECK: Prerequisite-Content Consistency (D9)
# ============================================================================

echo ""
echo "=== Prerequisite-Content Consistency (D9) ==="

conflict_count=0
for file in stages/**/*.md; do
  prereq_all=$(grep -A 10 "^## Prerequisites" "$file" 2>/dev/null | grep -i "ALL features\|all.*complete")
  content_group=$(grep -i "Round [0-9]:.*Group\|Group [0-9].*only" "$file" 2>/dev/null)

  if [ -n "$prereq_all" ] && [ -n "$content_group" ]; then
    echo "POTENTIAL CONFLICT: $file"
    echo "  Prerequisites: $prereq_all"
    echo "  Content: $content_group"
    ((conflict_count++))
  fi
done

if [ $conflict_count -eq 0 ]; then
  echo "No prerequisite-content conflicts detected"
else
  echo ""
  echo "Found $conflict_count potential conflicts - manual review required"
fi

# ============================================================================
# CHECK: Stage Flow Consistency (D17)
# ============================================================================

echo ""
echo "=== Stage Flow Consistency (D17) ==="

echo "S1 parallelization modes produced:"
grep -n "sequential\|parallel\|group" stages/s1/*.md 2>/dev/null | grep -i "mode\|option\|scenario" | head -5

echo ""
echo "S2 router modes handled:"
grep -n "Sequential\|Parallel\|Group" stages/s2/s2_feature_deep_dive.md 2>/dev/null | head -5

echo ""
echo "Verify: All S1 modes have corresponding S2 router entries"
```

**Effort:** 1-2 hours

---

### 3.3 Update Audit README

**File:** `feature-updates/guides_v2/audit/README.md`

**Update dimension count and add D17:**

```markdown
## The 17 Audit Dimensions

[Update from 16 to 17]

**Advanced Dimensions - D7, D15, D16, D17:**
- D7: Context-Sensitive Validation - Distinguishing errors from intentional exceptions
- D15: Duplication Detection - No duplicate content or contradictory instructions
- D16: Accessibility - Navigation aids, TOCs, scannable structure
- D17: Stage Flow Consistency - Behavioral continuity across stage transitions **(NEW)**
```

**Effort:** 15 minutes

---

### 3.4 Update Audit Overview

**File:** `feature-updates/guides_v2/audit/audit_overview.md`

**Update dimension list and add D17 description:**

```markdown
**Advanced Dimensions - D7, D15, D16, D17:**
- ✅ **D7: Context-Sensitive Validation** - Same pattern validated differently based on context
- ✅ **D15: Duplication Detection** - No duplicate content or contradictory instructions
- ✅ **D16: Accessibility** - Navigation aids, TOCs, scannable structure
- ✅ **D17: Stage Flow Consistency** - Behavioral continuity and semantic consistency across stage transitions **(NEW)**
```

**Update Sub-Round structure:**

```markdown
**Sub-Round N.4: Advanced (D7, D15, D16, D17)**
- D7: Context-Sensitive Validation (20% automated)
- D15: Duplication Detection (50% automated)
- D16: Accessibility (80% automated)
- D17: Stage Flow Consistency (30% automated) **(NEW)**
```

**Effort:** 30 minutes

---

## Phase 4: Validation and Testing (1-2 hours)

### 4.1 Validate Changes Against KAI-8 Issues

**Test:** Run new patterns against the known issues

```bash
# Test D3 workflow description patterns
grep -rn "S[0-9].*->.*S[0-9]" stages/
# Should find S1 Line 600: "S2->S3->S4 cycle"

# Test D9 prerequisite-content patterns
# Should flag S3's "ALL features" vs "Round 1: Group 1"

# Test D17 flow consistency
# Should flag S1→S2 handoff mismatch for group workflow
```

**Expected Results:**
- D3 Type 6 catches S1 vs S2 workflow description contradiction
- D9 Type 8 catches S3 internal prerequisite-content conflict
- D17 Type 1-3 catches S1→S2 flow inconsistency for group handling

### 4.2 Run Full Audit Round

**Test:** Execute a full audit round with new dimensions

1. Run pre_audit_checks.sh with new checks
2. Validate D3, D9, D14, D15 enhancements
3. Validate D17 stage flow checks
4. Document findings
5. Verify all KAI-8 issues would have been caught

---

## Implementation Schedule

### Recommended Order

| Phase | Task | Effort | Dependencies |
|-------|------|--------|--------------|
| 1.1 | D3 Workflow Description Patterns | 2-3h | None |
| 1.2 | D9 Prerequisite-Content Consistency | 1-2h | None |
| 1.3 | D14 Cross-Guide Claim Validation | 1-2h | None |
| 1.4 | D15 Contradiction Detection | 1-2h | None |
| 2.1 | D17 Stage Flow Consistency | 4-6h | 1.1-1.4 (builds on patterns) |
| 3.1 | Pattern Library Updates | 1-2h | 1.1-2.1 |
| 3.2 | Pre-Audit Script Updates | 1-2h | 1.1-2.1 |
| 3.3 | Audit README Update | 15m | 2.1 |
| 3.4 | Audit Overview Update | 30m | 2.1 |
| 4.1 | Validate Against KAI-8 | 1h | All |
| 4.2 | Full Audit Round Test | 1h | All |

### Parallel Execution Options

**Can run in parallel:**
- Phase 1.1 + 1.2 + 1.3 + 1.4 (independent dimension enhancements)

**Must run sequentially:**
- Phase 2 after Phase 1 (D17 builds on dimension patterns)
- Phase 3 after Phase 2 (supporting files reference D17)
- Phase 4 after Phase 3 (testing requires complete implementation)

---

## Success Criteria

### Functional Criteria

- [ ] D3 Type 6 patterns find workflow description contradictions
- [ ] D9 Type 8 patterns find prerequisite-content conflicts
- [ ] D14 Type 5 patterns find cross-guide claim inconsistencies
- [ ] D15 Type 8 patterns find contradictory content
- [ ] D17 validates all 9 stage transitions
- [ ] Pre-audit script includes new checks
- [ ] Pattern library includes new patterns

### Validation Criteria

- [ ] All KAI-8 issues would be caught by new patterns
- [ ] S1 Line 600 contradiction detected
- [ ] S3 internal conflict detected
- [ ] S2 router missing mode detected
- [ ] No false positives on valid content

### Documentation Criteria

- [ ] All dimension files updated with new pattern types
- [ ] D17 dimension file complete with all sections
- [ ] Pattern library includes semantic validation patterns
- [ ] Audit README and overview reflect 17 dimensions

---

## Risk Assessment

### Low Risk
- Dimension enhancements (additive, don't change existing behavior)
- Pattern library updates (additive)
- Documentation updates (additive)

### Medium Risk
- D17 complexity (new dimension, may need iteration)
- Pre-audit script changes (could affect existing checks)

### Mitigation
- Test all changes against known KAI-8 issues
- Run full audit round before considering complete
- Keep backup of original files during implementation

---

## Appendix: Files to Modify

### Existing Files

| File | Changes |
|------|---------|
| `audit/dimensions/d3_workflow_integration.md` | Add Type 6, update checklist, integration section |
| `audit/dimensions/d9_intra_file_consistency.md` | Add Type 8, update summary |
| `audit/dimensions/d14_content_accuracy.md` | Add Type 5 |
| `audit/dimensions/d15_duplication_detection.md` | Add Type 8, update summary |
| `audit/reference/pattern_library.md` | Add workflow and contradiction patterns |
| `audit/scripts/pre_audit_checks.sh` | Add new checks for D3, D9, D17 |
| `audit/README.md` | Update dimension count, add D17 |
| `audit/audit_overview.md` | Update dimension list, sub-round structure |

### New Files

| File | Purpose |
|------|---------|
| `audit/dimensions/d17_stage_flow_consistency.md` | New dimension |

---

## Conclusion

This implementation plan addresses the audit system gaps identified during KAI-8 by:

1. **Enhancing existing dimensions** with semantic validation patterns
2. **Adding D17** for cross-stage flow consistency validation
3. **Updating supporting infrastructure** (pattern library, pre-audit script)
4. **Validating against known issues** to ensure effectiveness

**Total Estimated Effort:** 12-16 hours

**Expected Outcome:** The audit system will catch semantic contradictions and workflow flow inconsistencies that previously went undetected, preventing future issues like the KAI-8 group-based parallelization confusion.
