# D21: Agent Comprehension Risk

**Dimension Number:** 21
**Category:** Advanced Dimensions
**Automation Level:** 15% automated
**Priority:** HIGH
**Last Updated:** 2026-03-08

**Focus:** Verify that individual guides are unambiguously comprehensible to an arriving agent — correct scope, no authoring noise in the instruction path, no confusion from structural similarity to sibling guides
**Typical Issues Found:** 0-8 per restructuring event; 0-2 in steady state

---

## Table of Contents

1. [What This Checks](#what-this-checks)
2. [Why This Matters](#why-this-matters)
3. [How This Differs From D18](#how-this-differs-from-d18)
4. [Pattern Types](#pattern-types)
5. [Scope Clarity Checklist](#scope-clarity-checklist)
6. [How Errors Happen](#how-errors-happen)
7. [Automated Validation](#automated-validation)
8. [Manual Validation](#manual-validation)
9. [Real Examples](#real-examples)
10. [Integration with Other Dimensions](#integration-with-other-dimensions)

---

## What This Checks

**D21: Agent Comprehension Risk** validates that each guide can be correctly understood by an agent arriving at it fresh — without relying on memory of the previous stage or careful inference from prerequisites.

Three risk types:

1. **Scope Clarity** - Does the guide prominently state its operational scope (once-per-epic, once-per-feature, conditional)? Or is scope only inferable from prerequisites that the agent may skim?
2. **Migration Notes in Instruction Path** - Does the Overview or first-contact section contain authoring/historical notes that are not agent instructions and could introduce prior stage structures the agent has never seen?
3. **Structural Similarity Confusion** - Does this guide share a template structure with a sibling guide serving a different scope, without adequate differentiation callouts to prevent the agent from treating them as interchangeable?

**Coverage:**
- All stage primary guides (s1–s10)
- All stage sub-guides that agents read directly
- Highest risk: any guide that follows a scope transition (e.g., S3 following a per-feature S2 loop; S9 following a per-feature S5-S8 loop)

---

## Why This Matters

**Agent comprehension failures cause workflow scope errors that are hard to detect and expensive to recover from.**

An agent that misidentifies a guide's scope will:
- Apply per-feature work patterns to an epic-level stage (or vice versa)
- Repeat an epic-level stage once per feature instead of once total
- Produce output for the wrong scope without flagging an error

Unlike broken links (D1) or missing sections (D6), scope misidentification produces no immediate error — the agent works normally but in the wrong context.

### Why Scope Must Be Stated Prominently

Agents often skim prerequisites. A scope statement buried in a checklist item ("ALL features must have completed S2") is less reliable than a blockquote immediately after the H1 that says "This stage runs once per epic."

An agent finishing a long per-feature loop (S2, or S5–S8) has built strong feature-scope momentum. A new guide with even a small scope ambiguity risks being interpreted through that lens.

### Why Migration Notes Are Hazardous

After a workflow restructuring, Overview sections sometimes contain notes like:
- "Key Changes from Old S3"
- "Moved from old S4, expanded"
- "Note: This content was previously part of S6"

These notes were useful to the guide author. They are not useful to an executing agent. Worse, they actively introduce stage structures the agent has never encountered. An agent reading "Moved from old S4" while working in S3 may attempt to apply S4-pattern thinking to S3's workflow.

### Why Structural Similarity Is Dangerous

When two guides share a template structure (same section headers, same output file names, similar workflow steps) but serve different scopes, agents risk treating them as functionally equivalent. Without explicit "this is NOT X" callouts, the agent may not notice the distinction.

The S3.P1 / S4 case is the canonical example: both produce test plans using similar templates, but S3.P1 produces epic-level smoke tests while S4 produces per-feature tests.

---

## How This Differs From D18

| Aspect | D18: Stage Flow Consistency | D21: Agent Comprehension Risk |
|--------|----------------------------|-------------------------------|
| **Unit of analysis** | Stage boundary (N -> N+1) | Individual guide (arriving agent) |
| **Question** | Do S2's exit promises match S3's entry expectations? | Would an agent arriving at S3 understand what it is? |
| **Catches** | Contradictions between adjacent stages | Ambiguity within a single stage guide |
| **Trigger** | Workflow behavior mismatches | Scope absence, authoring noise, structural confusion |
| **When D18 passes but D21 fails** | S2 exit and S3 entry agree on "epic-level" | S3 itself doesn't state "epic-level" prominently enough for an arriving agent to know |

**Complementary relationship:**
- D18 validates that the handoff between stages is consistent
- D21 validates that the receiving guide is clear enough for any arriving agent

Both must pass. A consistent handoff (D18 clean) does not guarantee agent comprehension (D21 clean).

---

## Pattern Types

### Type 1: Scope Clarity

**What to Check:**
Each stage guide must state its operational scope explicitly near the H1 — not just in prerequisites or deep in the body.

**High-risk scope transitions (check these first):**
- S3: Runs once per epic, after ALL features complete S2 — risk because agents arrive from a per-feature S2 loop
- S9: Runs once per epic, after ALL features complete S5-S8 — risk because agents arrive from a long per-feature implementation loop
- Any stage that is conditionally epic-level vs feature-level depending on parallelization mode

**Validation Process:**

1. **Check for scope callout near H1:**
   ```bash
   # Read the first 30 lines of each stage primary guide
   head -30 stages/sN/sN_*.md
   ```
   A passing guide has either:
   - A blockquote or bold statement before the first H2 that explicitly names the scope ("This stage runs once per epic", "This stage runs once per feature for each feature in the epic")
   - An explicit scope statement in the first section body (immediately after H1 or Overview H2)

2. **Check that scope is NOT only in prerequisites:**
   ```bash
   grep -n "once per epic\|once per feature\|runs once\|ALL features" stages/sN/*.md
   ```
   If the only matches are in Prerequisites sections — insufficient. Scope must also appear before the first H2.

**Red Flags:**
- Scope is only determinable by reading the Prerequisites checklist
- No explicit "this runs N times" statement anywhere in the guide
- Guide body uses "the feature" when it should say "the epic" (or vice versa)
- H1 title does not differentiate scope (e.g., titled generically when sibling guides could cause confusion)

**Checklist:**
- [ ] Scope stated explicitly before or in the first section (not just in Prerequisites)
- [ ] Scope statement uses unambiguous language ("once per epic", "once per feature")
- [ ] An agent finishing a per-feature loop would encounter the scope statement before reaching any workflow steps

---

### Type 2: Migration Notes in Agent Instruction Path

**What to Check:**
The Overview, Purpose, or any first-contact section must contain only agent-facing instructions. Authoring history — how the guide changed — must not appear in the primary instruction path.

**Search:**
```bash
grep -rn "Key Changes from Old\|Moved from old\|Previously called\|Renamed from\|This content was.*moved\|Note:.*was.*part of\|Note:.*was.*in" stages/ --include="*.md"
```

**Also check for:**
- Section headers like "What Changed in This Restructuring"
- Bullet points referencing old stage numbers (e.g., "old S4", "prior S3") in Overview or Purpose sections
- "Note:" callouts in Overviews that explain how the guide was assembled rather than how to use it

**Severity:**
- **HIGH** if the note references a stage by name/number that the agent has never executed (e.g., mentioning "old S4" while the agent is in S3)
- **MEDIUM** if the note is about the current stage's own history but creates no stage-structure confusion
- **LOW** if the note is in an appendix or clearly labeled as a changelog entry

**Fix:**
Move restructuring history to an appendix section (e.g., "## Change History") or remove it. The Overview must contain only what an executing agent needs.

**Red Flags:**
- "Key Changes from Old X" as a bullet list in Overview
- "Moved from old Y, expanded" as a sub-item in a structure description
- Any mention of stage names/numbers the executing agent has not visited yet

---

### Type 3: Structural Similarity Confusion

**What to Check:**
When two guides serve different scopes but share similar templates (same section headers, same output file formats, similar workflow steps), each guide must have explicit scope differentiation callouts that prevent an agent from treating them as interchangeable.

**Identify structurally similar guide pairs:**

Structurally similar guides are those that:
- Produce the same type of artifact (e.g., both produce test plan markdown files)
- Use the same section headers (e.g., both have "Validation Loop", "Gate", "Output Files")
- Appear in adjacent or near-adjacent stages

**Known pairs (validate these specifically):**
- **S3.P1 and S4** — both produce test planning documents; S3.P1 is epic-level, S4 is per-feature
- Any future stage pairs sharing output templates

**Validation:**
For each identified pair (Guide A at scope X, Guide B at scope Y):

1. **Guide A must explicitly state it is NOT Guide B's scope:**
   ```bash
   grep -n "NOT per-feature\|NOT epic\|NOT a.*test\|not.*the same as\|distinct from" stages/sA/*.md
   ```

2. **Guide B must explicitly state its scope relative to Guide A:**
   ```bash
   grep -n "per-feature\|NOT epic-level\|individual feature\|unlike.*S[0-9]" stages/sB/*.md
   ```

3. **Manual read:** Open both guides and ask: "If an agent read only Guide A, would it realize it should NOT apply Guide A's patterns when it later reaches Guide B?" If not — both guides need stronger differentiation callouts.

**Red Flags:**
- Both guides have identical H2 section names with no scope qualifier
- Guide A's output file names are identical to Guide B's output file names
- No "This is NOT X" callout in either guide
- An agent who read Guide A first could plausibly apply it wholesale to Guide B's context

**Checklist for each similar-scope pair:**
- [ ] Guide A has explicit "this is NOT [Guide B's scope]" callout
- [ ] Guide B has explicit "this is NOT [Guide A's scope]" callout
- [ ] Output file names are distinct (or clearly scoped by their path)
- [ ] Scope difference is stated in the first section of each guide, not only in a late section

---

## Scope Clarity Checklist

Run this checklist for every stage primary guide after a restructuring:

```markdown
## D21 Scope Clarity Checklist — Stage SN

### Type 1: Scope Clarity
- [ ] Scope stated explicitly before first H2 (blockquote or bold statement near H1)
- [ ] Scope statement uses unambiguous language ("once per epic" / "once per feature" / specific condition)
- [ ] An agent arriving from a per-feature loop would see the scope callout before reading any workflow steps
- [ ] If epic-level: "ALL features must have completed [previous stage]" type signal present
- [ ] If feature-level: clear indication of which feature this iteration covers

### Type 2: Migration Notes
- [ ] Overview contains no "Key Changes from Old X" blocks
- [ ] Overview contains no "Moved from old Y" annotations
- [ ] No Notes in the first-contact section that reference stages the agent has not visited
- [ ] Restructuring history (if needed for maintainers) is in an appendix, not the Overview

### Type 3: Structural Similarity
- [ ] If this guide shares a template with a sibling guide: does this guide have an explicit "NOT sibling scope" callout?
- [ ] If structurally similar pair identified: sibling guide reviewed (D21 both directions)
- [ ] Output file names cannot be confused with sibling guide's output files
```

---

## How Errors Happen

### Root Cause 1: Scope Was Always Implicit

**Scenario:**
- Guide was authored when the workflow had fewer stages
- Scope was "obvious" from context at the time
- After restructuring added similar-scope guides nearby, the implicit scope became ambiguous
- No one added an explicit callout because the guide "hadn't changed"

**Prevention:** D21 audit after any restructuring that adds stages or changes scope at adjacent stages

---

### Root Cause 2: Overview Written for the Author, Not the Agent

**Scenario:**
- Guide author knows the restructuring history
- Overview written as "here's what changed" rather than "here's what to do"
- Author notes ("Moved from old S4") remain in the merged guide
- Next reader (agent) has no prior context for "old S4"

**Prevention:** D21 Type 2 check after every guide merge or major restructuring

---

### Root Cause 3: Template Reuse Without Differentiation

**Scenario:**
- New guide created by copying a similar existing guide
- Template structure preserved (same section headers, same output file pattern)
- Copy-paste author adds new content but leaves structural similarity
- No "this is NOT the same as the original" callout added

**Prevention:** D21 Type 3 check whenever a new guide is created from an existing guide's template

---

## Automated Validation

### Automation Coverage: ~15%

**What can be partially automated:**

```bash
#!/bin/bash
# CHECK: Agent Comprehension Risk (D21)
# ============================================================================

echo "=== D21: Agent Comprehension Risk Checks ==="

# Check 1: Scope statements near H1 (first 30 lines of stage primary guides)
echo ""
echo "--- Scope Statements in First 30 Lines ---"
echo "(Manual verification needed: confirm these are prominent scope callouts)"
for file in stages/s{1..10}/*.md; do
  scope=$(head -30 "$file" 2>/dev/null | grep -i "once per\|runs once\|per epic\|per feature\|ALL features")
  if [ -n "$scope" ]; then
    echo "FOUND in $file:"
    echo "  $scope"
  else
    echo "ABSENT in $file — check for scope clarity"
  fi
done

# Check 2: Migration notes in instruction path
echo ""
echo "--- Migration Notes in Stage Guides ---"
grep -rn "Key Changes from Old\|Moved from old\|Previously called\|Renamed from\|Note:.*was.*part of\|Note:.*was.*in old" \
  stages/ --include="*.md"
echo "(Any matches above are potential Type 2 issues — review context)"

# Check 3: Structural similarity — S3.P1 / S4 pair
echo ""
echo "--- S3.P1 / S4 Differentiation Callouts ---"
echo "S3 has 'NOT per-feature' callout:"
grep -rn "NOT per-feature\|not per-feature\|not.*feature.*test" stages/s3/ --include="*.md" | head -3
echo ""
echo "S4 has 'NOT epic' or scope distinction callout:"
grep -rn "epic.*must.*complete\|S3.*complete\|NOT.*epic\|per-feature.*only" stages/s4/ --include="*.md" | head -3

echo ""
echo "=== D21 Pre-Check Complete ==="
echo "Manual review required for semantic validation of all findings"
```

**Automated catches (~15%):**
- Presence/absence of scope keywords in first 30 lines
- Known migration note patterns in stage guides
- Known structurally similar pair (S3.P1 / S4) differentiation keyword presence

**Manual required (~85%):**
- Whether a scope statement is actually prominent (vs. buried in a list item)
- Whether a note is genuinely migration noise vs. a valid agent instruction
- Whether structural similarity creates actual confusion risk for this guide pair
- Identifying NEW structurally similar pairs not covered by automated checks

---

## Manual Validation

### Full D21 Process

**Duration:** 30-60 minutes
**Frequency:** After any stage restructuring; after adding new stage guides; after guide merges

**Step 1: Identify high-risk guides (5 min)**

High-risk guides are those that:
- Follow a scope transition (agent arriving from a different scope loop)
- Were recently restructured or merged from prior stages
- Were created by copying another guide's template

Focus here first, but all stage primary guides must eventually be checked.

**Step 2: Check Type 1 (Scope Clarity) for each guide (3-5 min each)**

1. Open the guide
2. Read only the first 30 lines (H1 + first section)
3. Ask: "Would an agent arriving from a per-feature loop know this is epic-level? Would an agent arriving from an epic-level stage know this is per-feature?"
4. If the answer requires reading the Prerequisites section — flag as insufficient

**Step 3: Check Type 2 (Migration Notes) for each guide (2 min each)**

1. Search with the automated commands above
2. For each match: read 5-10 lines of context
3. Assess: Is this agent-facing instruction or authoring history?
4. If authoring history: flag as a finding

**Step 4: Check Type 3 (Structural Similarity) for all known similar pairs (10 min)**

1. For each known similar pair (S3.P1/S4 and any others):
2. Open both guides side by side
3. Verify each has an explicit scope differentiation callout
4. Verify the callouts are in the first-contact section, not buried in an appendix
5. Verify output file names are distinct

**Step 5: Document findings**

```markdown
## D21 Agent Comprehension Risk Findings

### Guides Checked
- [ ] S1 primary: [PASS/FAIL]
- [ ] S2 primary: [PASS/FAIL]
- [ ] S3 primary (HIGH RISK): [PASS/FAIL]
- [ ] S4 primary: [PASS/FAIL]
- [ ] S5-S8 primaries: [PASS/FAIL]
- [ ] S9 primary (HIGH RISK): [PASS/FAIL]
- [ ] S10 primary: [PASS/FAIL]

### Issues Found (by type)
#### Type 1: Scope Clarity
1. [Guide]: [Issue description]

#### Type 2: Migration Notes
1. [Guide]: [Note content found, location, severity]

#### Type 3: Structural Similarity
1. [Guide pair]: [Issue description]
```

---

## Real Examples

### Example 1: S3 Scope Ambiguity (SHAMT-6)

**Issue Found:**
`s3_epic_planning_approval.md` had no prominent scope statement near the H1. The only indication that S3 runs once per epic was in the prerequisites checklist ("ALL features have completed S2").

**Impact:**
Child project agents finishing the per-feature S2 loop proceeded to S3 and treated it as a per-feature stage — running S3 once per feature instead of once for the epic.

**Fix Applied:**
Added blockquote immediately after H1:
```markdown
> **SCOPE:** This stage runs **once per epic**, after S2 is complete for ALL features. It is not
> repeated per feature. Working directory is the **epic folder root**, not a feature folder.
```

**D21 Detection:**
- Type 1: Scope Clarity check — first 30 lines contained no scope statement before the fix
- Would have been caught by the automated check showing "ABSENT" in s3_epic_planning_approval.md

---

### Example 2: Migration Notes in S3 Overview (SHAMT-6)

**Issue Found:**
`s3_epic_planning_approval.md` Overview contained:
```markdown
**Key Changes from Old S3:**
- **Pairwise comparison removed** (moved to S2.P2)
- **Epic testing strategy from old S4 moved here** (S3.P1)
- **Two Validation Loops** (testing strategy + documentation)
- **Gate 4.5 explicit with 3-tier rejection handling**
```

**Impact:**
An agent reading the Overview encountered references to "old S3", "old S4", and prior features like "pairwise comparison" — none of which are part of the current workflow. This introduced conceptual noise and risk of the agent attempting to locate or execute the "pairwise comparison" step.

Additionally, the S3.P1 structure bullet listed "- Moved from old S4, expanded" — causing an agent to mentally associate S3.P1 with S4 before ever reaching S4.

**Fix Applied:**
Removed the "Key Changes from Old S3" block and the "Moved from old S4, expanded" annotation from the structure list.

**D21 Detection:**
- Type 2: Migration Notes check — grep for "Moved from old\|Key Changes from Old" would have surfaced both instances

---

### Example 3: S3.P1 / S4 Structural Similarity (SHAMT-6)

**Issue Found:**
S3.P1 (epic smoke test plan) and S4 (per-feature test strategy) used nearly identical template structures — same section headers, same output formats, same validation loop format. No guide had an explicit "this is NOT the other guide" callout.

**Impact:**
Agents who completed S3.P1 and then reached S4 treated them as the same workflow, reusing S3.P1-level thinking (cross-feature scenarios) for per-feature test planning, or skipping S4 on the assumption that "test planning was already done in S3."

**Fix Applied:**
- Added to S3.P1: `> **This is NOT per-feature test planning.** Tests defined here span multiple features and verify end-to-end workflows across the whole epic.`
- S4 already had a prerequisite "S3 complete" — no additional callout was added to S4, but one should be added per Type 3 checklist

**D21 Detection:**
- Type 3: Structural Similarity check — manual read of both guides side by side reveals identical template without scope differentiation

---

## Integration with Other Dimensions

| Dimension | Relationship to D21 |
|-----------|---------------------|
| **D1: Cross-Reference Accuracy** | D1 catches broken links; D21 catches misleading prose references that are technically valid but belong to a different context |
| **D2: Terminology Consistency** | D2 catches inconsistent stage naming; D21 catches structurally consistent guides that serve different scopes without differentiation |
| **D3: Workflow Integration** | D3 validates that stage numbers in prerequisites are correct; D21 validates that stage *names* and scope descriptions are correct in those same prerequisites |
| **D15: Context-Sensitive Validation** | D15 protects historical content from being incorrectly flagged; D21 specifically identifies where that protection creates agent comprehension risk (migration notes in the instruction path) |
| **D18: Stage Flow Consistency** | D18 validates cross-stage handoff consistency; D21 validates within-guide clarity for the arriving agent — complementary, both required |

**Recommended Audit Order:**
1. D18 (cross-stage behavioral validation)
2. D21 (within-guide agent comprehension validation)

D18 should run first because fixing cross-stage inconsistencies may change what scope statements D21 needs to verify. D21 then checks each guide independently for arriving-agent clarity.

---

**Last Updated:** 2026-03-08
**Version:** 1.0
**Status:** New (SHAMT-6)
