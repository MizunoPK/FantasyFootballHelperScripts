# D22: Guide Bypass Risk

**Dimension Number:** 22
**Category:** Advanced Dimensions
**Automation Level:** 30% automated
**Priority:** HIGH
**Last Updated:** 2026-03-15

**Focus:** Verify that each guide is structurally resistant to agent bypass — that agents cannot skip phases, omit the reading protocol, or proceed without completing mandatory quality gates
**Typical Issues Found:** 0-4 per new guide set; 0-1 in steady state

---

## Table of Contents

1. [What This Checks](#what-this-checks)
2. [Why This Matters](#why-this-matters)
3. [How This Differs From D21](#how-this-differs-from-d21)
4. [Structural Checks](#structural-checks)
5. [Content Quality Checks](#content-quality-checks)
6. [How Errors Happen](#how-errors-happen)
7. [Automated Validation](#automated-validation)
8. [Manual Validation](#manual-validation)
9. [Integration with Other Dimensions](#integration-with-other-dimensions)

---

## What This Checks

**D22: Guide Bypass Risk** validates that each guide has the structural enforcement mechanisms that prevent agents from skipping required phases, omitting the reading protocol, or completing a guide only partially.

Four bypass failure modes this dimension targets:

1. **Purpose-inference bypass** — Agent reads the title or overview, grasps the purpose, then executes from training knowledge without following the guide's specific steps
2. **Mid-guide mode-switch** — Agent reads the guide once at the start, then reverts to "general knowledge mode" during execution
3. **Phase completion blindness** — Agent finishes the phase that produces the primary artifact (the draft, the plan, the test strategy) and treats the work as done, skipping the quality-gate phase
4. **Resume-without-reread** — Agent returns mid-guide using Agent Status alone, without re-reading the guide's instructions for the current phase

**Coverage:**
- All stage primary guides (s1–s10 directories)
- All stage sub-guides that agents read directly (s7_p2, s9_p2, etc.)
- Highest risk: guides with a mandatory quality-gate phase following the primary artifact phase (S5, S7.P2, S9.P2, S3)

---

## Why This Matters

**Bypass failures produce apparently complete output that is actually incomplete.** An agent that skips Phase 2 of S5 still produces an implementation_plan.md — it just hasn't been validated. An agent that skips S7.P2 QC rounds still reports "QC done" after a single pass. The failure is invisible until downstream stages reveal the missing quality.

Unlike a broken reference (D1) or a missing section (D6), a bypass failure produces no immediate error signal. The agent works normally but produces a lower-quality artifact without flagging the shortcut.

### Why Structure Prevents Bypass

The MANDATORY READING PROTOCOL places a concrete, checkable action before any work can begin: use the Read tool to load the entire guide. The FORBIDDEN SHORTCUTS block names the specific bypass the agent is about to make — before the agent makes it. The phase commitment gate requires explicit acknowledgment of mandatory subsequent phases before the first phase builds momentum.

These mechanisms work because they front-load the commitment. An agent that acknowledges "Phase 2 is mandatory — I will not skip it" before Phase 1 begins is less likely to treat Phase 1 completion as the finish line than an agent that encounters Phase 2 only after Phase 1 feels done.

---

## How This Differs From D21

| Aspect | D21: Agent Comprehension Risk | D22: Guide Bypass Risk |
|--------|-------------------------------|------------------------|
| **Question** | Can an agent correctly understand what this guide is for? | Can an agent successfully skip steps in this guide? |
| **Failure mode** | Agent misidentifies scope, applies wrong workflow | Agent correctly identifies scope, then skips phases |
| **Catches** | Scope ambiguity, migration notes, structural confusion | Missing MRP, missing FORBIDDEN SHORTCUTS, absent commitment gates |
| **When D21 passes but D22 fails** | Agent knows this is S5 Implementation Planning | Agent knows this is S5, then drafts the plan from training knowledge |

**Complementary relationship:**
- D21 validates that the arriving agent understands the guide's scope
- D22 validates that the guide enforces its own execution against bypass

Both must pass. A clearly scoped guide (D21 clean) can still lack bypass resistance (D22 fail) if it has no MRP, no FORBIDDEN SHORTCUTS, and no commitment gate.

---

## Structural Checks

These checks verify that the bypass-resistance mechanisms exist. Check every stage primary guide and sub-guide.

### Check 1: MANDATORY READING PROTOCOL Present

**Pass:** Guide has a `🚨 **MANDATORY READING PROTOCOL**` or `## 🚨 MANDATORY READING PROTOCOL` block at or near the top (before the first substantive section), explicitly covering both fresh starts and resumption.

**Fail signals:**
- No reading protocol block anywhere
- Reading protocol exists but is not near the top (buried after Prerequisites or Overview)
- Reading protocol does not mention resumption ("including when resuming a prior session")
- Protocol is too lightweight (e.g., just "read the guide before starting" without requiring use of Read tool)

**Check:**
```bash
grep -l "MANDATORY READING PROTOCOL" .shamt/guides/stages/s*/*.md
```
Files not in this list are missing the MRP.

---

### Check 2: FORBIDDEN SHORTCUTS Block Present

**Pass:** Guide has a `🚫 **FORBIDDEN SHORTCUTS**` block immediately after the MRP (or near the top, before Prerequisites), naming at least 2 guide-specific bypass patterns.

**Fail signals:**
- No FORBIDDEN SHORTCUTS block anywhere in the guide
- Block exists but is positioned late in the guide (after Prerequisites, after Overview)
- Block contains only generic items not tied to this guide's steps/phases

**Check:**
```bash
grep -l "FORBIDDEN SHORTCUTS" .shamt/guides/stages/s*/*.md
```
Files not in this list are missing FORBIDDEN SHORTCUTS.

---

### Check 3: Phase Commitment Gate Present (Multi-Phase Guides Only)

**Applies to:** Guides where the primary artifact is produced in Phase 1 (or an early phase) and a mandatory quality-gate phase follows.

**Confirmed scope:** S5 (Phase 2 = Validation Loop), S3 (P2+P3 follow P1), S7.P2 (validation loop rounds), S9.P2 (validation loop rounds)

**Pass:** The first substantive phase includes a commitment checkpoint (checklist format, ≤4 items) that names the mandatory subsequent phase(s) explicitly and states the agent will not skip them.

**Fail signals:**
- Multi-phase guide has no commitment checkpoint at the start of Phase 1
- Commitment checkpoint uses generic language ("complete all phases") instead of naming the specific subsequent phase
- Commitment checkpoint is placed AFTER Phase 1 content instead of BEFORE it

---

### Check 4: Validation Loop Cross-Referenced Before Its Section (Multi-Phase Guides Only)

**Applies to:** Guides with a mandatory validation loop phase.

**Pass:** The validation loop is mentioned in the guide overview AND at the start of the phase that precedes it, not only in the validation loop section itself.

**Fail signals:**
- The validation loop section exists but is only referenced in its own section header
- The overview describes "Phase 1" without mentioning Phase 2 exists
- The commitment gate (Check 3) refers to the loop but the overview does not

---

### Check 5: RULES_FILE Contains Guide Execution Protocol

**Pass:** The child project's rules file (CLAUDE.md, copilot-instructions.md, etc.) contains a `## Guide Execution Protocol` section.

**Check (in child project context):**
```bash
grep -l "Guide Execution Protocol" CLAUDE.md .github/copilot-instructions.md 2>/dev/null
```

**Note:** In master context, check `RULES_FILE.template.md`. In child project audits, check the deployed rules file.

---

## Content Quality Checks

These checks verify that the bypass-resistance mechanisms contain genuinely effective content, not just structurally present boilerplate.

### Check 6: FORBIDDEN SHORTCUTS Items Are Guide-Specific

**Pass:** Each item in FORBIDDEN SHORTCUTS references specific steps, phases, or output names from THIS guide.

Examples of guide-specific items:
- "Draft an implementation plan based on general knowledge — follow Steps 0–7 in Phase 1" (references S5 Steps 0–7)
- "Skip Phase 2 (Validation Loop) because Phase 1 is 'done enough'" (references S5 Phase 2)
- "Skip the Code Inspection Protocol (MANDATORY) by reviewing code from memory" (references S7.P2's specific named protocol)

Examples of non-specific items that fail this check:
- "Skip required steps" (generic — doesn't name what steps)
- "Follow the guide" (circular — restates the requirement, doesn't name the bypass)
- "Do not rush" (behavioral guidance, not a specific shortcut pattern)

---

### Check 7: Phase Commitment Gate Names the Specific Phase

**Pass:** The commitment gate names the exact mandatory subsequent phase (e.g., "Phase 2 (Validation Loop)") rather than generic language.

**Fail:** "I will complete all subsequent phases" — doesn't name which phase.

**Pass:** "Phase 2 (Validation Loop) is mandatory after Phase 1 — I will not skip it" — names the specific phase.

---

## How Errors Happen

### Root Cause 1: Guide Written for Content, Not Execution Enforcement

**Scenario:**
- Guide author focuses on the what (what steps to execute) not the how-to-enforce (how to prevent the agent from skipping steps)
- The guide has excellent step-by-step content but no MRP, no FORBIDDEN SHORTCUTS, no commitment gate
- An agent who reads the guide will follow it; an agent who skips to the relevant section will not

**Prevention:** D22 check after every new guide is written

---

### Root Cause 2: MRP Copied Without Resumption Clause

**Scenario:**
- Guide author copies the MRP from another guide
- The copy omits "including when resuming a prior session"
- Agent resuming mid-guide uses Agent Status alone and doesn't re-read

**Prevention:** D22 Check 1 verifies resumption coverage explicitly

---

### Root Cause 3: Phase Commitment Gate Added Late

**Scenario:**
- Phase commitment gate is added after the PHASE 1 header but after some Phase 1 content — it appears mid-phase
- An agent scanning the guide may reach Phase 1 content before reaching the commitment checkpoint
- The checkpoint's effect depends on position: it must appear BEFORE Phase 1 content, not within it

**Prevention:** D22 Check 3 verifies positioning — the gate must precede the first Phase 1 content block

---

## Automated Validation

### Automation Coverage: ~30%

**What can be partially automated:**

```bash
#!/bin/bash
# CHECK: Guide Bypass Risk (D22)
# ============================================================================

echo "=== D22: Guide Bypass Risk Checks ==="
STAGES_DIR=".shamt/guides/stages"
PROMPTS_DIR=".shamt/guides/prompts"

# Check 1: MANDATORY READING PROTOCOL presence
echo ""
echo "--- Check 1: MANDATORY READING PROTOCOL in stage guides ---"
for file in "$STAGES_DIR"/s*/*.md; do
  if grep -q "MANDATORY READING PROTOCOL" "$file"; then
    echo "FOUND: $file"
  else
    echo "ABSENT: $file — add MANDATORY READING PROTOCOL"
  fi
done

# Check 2: FORBIDDEN SHORTCUTS presence
echo ""
echo "--- Check 2: FORBIDDEN SHORTCUTS in stage guides ---"
for file in "$STAGES_DIR"/s*/*.md; do
  if grep -q "FORBIDDEN SHORTCUTS" "$file"; then
    echo "FOUND: $file"
  else
    echo "ABSENT: $file — add FORBIDDEN SHORTCUTS block"
  fi
done

# Check 5 (RULES_FILE): Guide Execution Protocol presence
echo ""
echo "--- Check 5: Guide Execution Protocol in rules file ---"
if grep -q "Guide Execution Protocol" CLAUDE.md 2>/dev/null; then
  echo "FOUND in CLAUDE.md"
elif grep -q "Guide Execution Protocol" .shamt/scripts/initialization/RULES_FILE.template.md 2>/dev/null; then
  echo "FOUND in RULES_FILE.template.md"
else
  echo "ABSENT — add Guide Execution Protocol section to rules file"
fi

# P5 prompts: NEXT MANDATORY STEP presence for multi-phase transitions
echo ""
echo "--- P5: NEXT MANDATORY STEP in prompts ---"
for file in "$PROMPTS_DIR"/*.md; do
  count=$(grep -c "NEXT MANDATORY STEP" "$file" 2>/dev/null || echo 0)
  if [ "$count" -gt 0 ]; then
    echo "FOUND ($count occurrences): $file"
  fi
done
echo "(Manual review: verify the transitions that NEED NEXT MANDATORY STEP have it)"

echo ""
echo "=== D22 Pre-Check Complete ==="
echo "Manual review required for: MRP resumption coverage, FORBIDDEN SHORTCUTS specificity, commitment gate positioning"
```

**Automated catches (~30%):**
- Presence/absence of MRP heading in stage guides
- Presence/absence of FORBIDDEN SHORTCUTS heading in stage guides
- Presence/absence of Guide Execution Protocol in rules file
- NEXT MANDATORY STEP occurrence count in prompts files

**Manual required (~70%):**
- Whether MRP covers resumption scenarios (not just fresh starts)
- Whether FORBIDDEN SHORTCUTS items are guide-specific (not generic)
- Whether phase commitment gate appears BEFORE Phase 1 content (not within it)
- Whether commitment gate names the specific subsequent phase
- Identifying multi-phase guides that need but are missing commitment gates

---

## Manual Validation

### Full D22 Process

**Duration:** 20-40 minutes
**Frequency:** After any new guide is written; after any guide restructuring that adds or removes phases; after SHAMT-N changes that affect guide structure

**Step 1: Identify multi-phase guides (5 min)**

Multi-phase guides requiring commitment gates:
- Guides where Phase 1 produces the primary artifact AND Phase 2+ contains the quality gate
- Currently confirmed: S5, S3, S7.P2, S9.P2
- New guides: check if a similar structure exists

**Step 2: Run automated checks (5 min)**

Run the bash snippet above. Note all ABSENT results.

**Step 3: For each stage guide — MRP quality check (2 min each)**

1. Open the guide
2. Find the MRP block
3. Verify: does it explicitly say "including when resuming a prior session" or equivalent?
4. Verify: is it positioned before Prerequisites? (It must precede substantive content)

**Step 4: For each stage guide — FORBIDDEN SHORTCUTS quality check (2 min each)**

1. Find the FORBIDDEN SHORTCUTS block
2. Read each item
3. Ask: "Does this item name a specific step, phase, or named protocol from THIS guide?"
4. If any item is generic (could apply to any guide without modification) — flag as insufficient

**Step 5: For multi-phase guides — commitment gate check (3 min each)**

1. Navigate to the start of Phase 1 (or the first substantive phase)
2. Verify: commitment gate appears before any Phase 1 content (goal, steps, time estimates)
3. Verify: commitment gate names the specific subsequent mandatory phase by name

**Step 6: Document findings**

```markdown
## D22 Guide Bypass Risk Findings

### Stage Guides Checked
- [ ] S1 primary: [PASS/FAIL] — MRP: Y/N | FS: Y/N
- [ ] S2 primary: [PASS/FAIL] — MRP: Y/N | FS: Y/N
- [ ] S3 primary: [PASS/FAIL] — MRP: Y/N | FS: Y/N | Gate: Y/N
- [ ] S5 primary: [PASS/FAIL] — MRP: Y/N | FS: Y/N | Gate: Y/N
- [ ] S6 primary: [PASS/FAIL] — MRP: Y/N | FS: Y/N
- [ ] S7.P2: [PASS/FAIL] — MRP: Y/N | FS: Y/N | Gate: Y/N
- [ ] S9.P2: [PASS/FAIL] — MRP: Y/N | FS: Y/N | Gate: Y/N
- [ ] Other sub-guides: [list]

### Issues Found
#### Check 1: Missing or insufficient MRP
1. [Guide]: [Issue]

#### Check 2: Missing or non-specific FORBIDDEN SHORTCUTS
1. [Guide]: [Issue]

#### Check 3: Missing or mispositioned commitment gate
1. [Guide]: [Issue]

#### Check 5: Rules file missing Guide Execution Protocol
- [PASS/FAIL]
```

---

## Integration with Other Dimensions

| Dimension | Relationship to D22 |
|-----------|---------------------|
| **D6: Content Completeness** | D6 catches missing sections; D22 catches missing bypass-resistance mechanisms (MRP, FORBIDDEN SHORTCUTS) that are not "content sections" but structural enforcement |
| **D12: Structural Patterns** | D12 verifies that guides follow the standard structure template; D22 verifies that guides have the specific enforcement blocks required for bypass resistance — complementary, different focus |
| **D18: Stage Flow Consistency** | D18 validates that stage handoffs are consistent; D22 validates that NEXT MANDATORY STEP footers in phase transition prompts name the correct next prompt |
| **D19: Rules File Template Alignment** | D19 checks that child rules files match the master template; D22 checks that the master template itself contains the Guide Execution Protocol |
| **D21: Agent Comprehension Risk** | D21 asks "can an agent understand this guide?"; D22 asks "can an agent skip steps in this guide?" — a guide can pass D21 and fail D22 |

**Recommended Audit Order:**
1. D21 (within-guide comprehension validation)
2. D22 (within-guide bypass resistance validation)

D21 should run first: if a guide has scope clarity issues, those may need to be resolved before D22's structural bypass checks make sense.

---

**Last Updated:** 2026-03-15
**Version:** 1.0
**Status:** New (SHAMT-8)
