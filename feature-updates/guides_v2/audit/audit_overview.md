# Audit Overview

**Purpose:** Understand when to run audits, audit philosophy, and completion criteria
**Audience:** Agents conducting quality audits after guide updates
**Reading Time:** 10-15 minutes

---

## Table of Contents

1. [What This Audit Covers](#what-this-audit-covers)
2. [What This Audit Does NOT Cover](#what-this-audit-does-not-cover)
3. [When to Run This Audit](#when-to-run-this-audit)
4. [Audit Philosophy](#audit-philosophy)
5. [The Iterative Loop](#the-iterative-loop)
6. [Exit Criteria](#exit-criteria)
7. [Historical Evidence](#historical-evidence)
8. [Critical External Files](#critical-external-files)

---

## What This Audit Covers

This audit ensures **consistency, accuracy, and completeness** across all guides_v2 files AND related external files.

### The 17 Audit Dimensions

**Core Dimensions (Always Check) - D1, D2, D3, D8:**
- ✅ **D1: Cross-Reference Accuracy** - All file paths, stage references, and cross-links are valid
- ✅ **D2: Terminology Consistency** - Notation, naming conventions, and terminology are uniform
- ✅ **D3: Workflow Integration** - Guides correctly reference each other and form cohesive workflows
- ✅ **D8: CLAUDE.md Synchronization** - Root file quick references match actual guide content

**Content Quality Dimensions - D4, D5, D6, D13, D14:**
- ✅ **D4: Count Accuracy** - File counts, stage counts, iteration counts match reality
- ✅ **D5: Content Completeness** - No missing sections, gaps in coverage, or orphaned references
- ✅ **D6: Template Currency** - Templates reflect current workflow structure and terminology
- ✅ **D13: Documentation Quality** - All required sections present, no TODOs or placeholders
- ✅ **D14: Content Accuracy** - Claims in guides match reality (step counts, durations, etc.)

**Structural Dimensions - D9, D10, D11, D12:**
- ✅ **D9: Intra-File Consistency** - Within-file quality (headers, checklists, formatting)
- ✅ **D10: File Size Assessment** - Files within readable limits, complex files split appropriately
- ✅ **D11: Structural Patterns** - Guides follow expected template structures
- ✅ **D12: Cross-File Dependencies** - Stage prerequisites match outputs, workflow continuity

**Advanced Dimensions - D7, D15, D16, D17:**
- ✅ **D7: Context-Sensitive Validation** - Same pattern validated differently based on context
- ✅ **D15: Duplication Detection** - No duplicate content or contradictory instructions
- ✅ **D16: Accessibility** - Navigation aids, TOCs, scannable structure
- ✅ **D17: Stage Flow Consistency** - Behavioral continuity and semantic consistency across stage transitions

---

## What This Audit Does NOT Cover

**Out of Scope:**
- ❌ Content quality evaluation (writing style, clarity, tone)
- ❌ Workflow design decisions (whether stages are correct)
- ❌ Code implementation (actual Python scripts)
- ❌ Pedagogical effectiveness (whether guides teach well)

**Rationale:** This audit focuses on **technical consistency and accuracy**, not subjective quality or design choices.

---

## When to Run This Audit

### MANDATORY Triggers

**1. After Major Restructuring**
- Stage renumbering (e.g., S6→S9, S7→S10)
- Folder reorganization
- File splits/merges (e.g., splitting S5 into S5-S8)

**Why:** Restructuring creates cascading reference updates. Missed updates = broken workflow.

**2. After Terminology Changes**
- Notation updates (e.g., "Stage 5a" → "S5.P1")
- Naming convention changes
- Reserved term redefinitions

**Why:** Old notation can persist in unexpected places. Inconsistent terminology = user confusion.

**3. After Workflow Updates**
- Adding/removing stages, phases, or iterations
- Changing gate requirements or checkpoints
- Modifying file structures

**Why:** Workflow changes affect prerequisites, exit criteria, and cross-references throughout guides.

**4. After S10.P1 Guide Updates**
- After completing lessons learned integration
- When guide changes were made based on epic retrospectives

**Why:** Guide changes can introduce inconsistencies. Validate all cross-references still accurate.

**5. User Reports Inconsistency**
- User finds error or reports confusion
- Immediate spot-audit of related files
- Full audit if issue appears widespread

**Why:** User-reported issues indicate blind spots. One error often signals more nearby.

### OPTIONAL Triggers

**Quarterly Maintenance:**
- Even without changes, run audit every 3 months
- Catches drift and accumulation of small issues

**Before Major Release:**
- Before releasing epic to production
- Ensures documentation quality for users

**After Significant Content Updates:**
- After adding multiple new guides
- After updating core guides with new sections

**After Adding New Templates:**
- Templates propagate to new epics
- Errors in templates multiply rapidly

---

## Audit Philosophy

### Core Principles

**1. ZERO TOLERANCE FOR DEFERRALS** 🚨 CRITICAL
- **ALL identified issues MUST be investigated and addressed immediately**
- **NO deferring issues to "later rounds" or "post-audit"**
- **If you cannot determine the correct fix with confidence, ASK THE USER**
- The audit's purpose is to achieve OPTIMAL state, not just quick wins

**Rationale:**
- Deep dives into files are ENCOURAGED, not discouraged
- Time spent investigating = correct fixes vs superficial patches
- Deferred issues become technical debt that compounds
- User questions get immediate clarity vs accumulating uncertainty

**Decision Framework:**
```text
Issue discovered → Can I fix with confidence?
  ├─ YES → Fix immediately, verify, document
  └─ NO  → Read affected files, analyze context
            ├─ NOW confident? → Fix immediately
            └─ Still uncertain? → ASK USER (provide options, analysis, recommendation)
```markdown

**Examples of CORRECT behavior:**
- ✅ 34 files missing Prerequisites/Exit Criteria → Read each file → Determine if sections needed → Add or document as intentional
- ✅ 32 files >1250 lines → Read each file → Split using reduction guide → Verify file sizes reduced
- ✅ Broken file reference → Cannot determine correct path → ASK USER for intended reference

**Examples of WRONG behavior:**
- ❌ 34 files missing Prerequisites/Exit Criteria → "Requires file reading" → Defer to Round 3
- ❌ 32 files >1250 lines → "Requires 12-16 hours" → Defer to post-audit
- ❌ Uncertain about fix → "Seems complex" → Defer for later

**2. Fresh Eyes, Zero Assumptions**
- Approach each round as if you've never seen the codebase
- Don't trust previous rounds - verify everything again
- Clear mental model between rounds (take 5-min break)

**3. User Skepticism is Healthy**
- When user challenges you, THEY ARE USUALLY RIGHT
- "Are you sure?" = red flag you missed something
- Do NOT defend findings - re-verify immediately

**4. Evidence Over Claims**
- Show actual file contents, not just grep output
- Before/after comparisons for every fix
- Spot-check random files to verify grep accuracy

**5. Iterative Until Zero**
- Minimum 3 rounds as baseline (NOT a target - KAI-7 needed 4 rounds)
- TRUE exit trigger: Round N finds ZERO new issues + ALL 9 criteria met
- Continue auditing regardless of round count until criteria satisfied
- Each round uses completely different patterns

**6. Better to Over-Audit Than Under-Audit**
- False positives can be resolved
- False negatives cause user confusion
- When uncertain, ASK USER (don't defer)

---

## How to Achieve Fresh Eyes (Operational Guide)

**What "Fresh Eyes" Means:**
Approaching the audit as if you've never seen these files before, with zero assumptions about what's correct or what you've already checked.

---

### 📋 TL;DR (Quick Reference)

**5-Step Fresh Eyes Checklist:**

1. **Clear context:** Close all Round N-1 files, take 5-10 min break
2. **Different patterns:** Use NEW search patterns (not same grep commands from Round N-1)
3. **Different order:** Search folders in DIFFERENT order than Round N-1
4. **Don't peek:** Don't look at Round N-1 discoveries until AFTER Round N discovery complete
5. **Self-check:** Am I skipping folders "because I know they're clean"? → ❌ NOT fresh, check anyway

**Common Failure:** Re-running same patterns from Round N-1 to "verify" → Finds nothing new (false confidence)

**Full guide below provides detailed anti-patterns, examples, verification checklist, and recovery steps.**

---

### STEP 1: Clear Context (5-10 minutes)

**Before starting Round N, clear your working memory:**

- [ ] Close all files from Round N-1
- [ ] Don't look at Round N-1 discovery report until AFTER Round N discovery complete
- [ ] Take a 5-10 minute break (work on different task, clear mental model)
- [ ] Start Round N without reviewing what Round N-1 found

**Why This Matters:** Looking at Round N-1 discoveries primes you to search for those same patterns and miss different ones.

### STEP 2: Change Perspective (Required)

**Use DIFFERENT approach than Round N-1:**

**Pattern Diversity:**
- [ ] Use DIFFERENT search patterns than Round N-1 (not same grep commands)
- [ ] Search folders in DIFFERENT order than Round N-1
- [ ] Start from DIFFERENT dimension than Round N-1
- [ ] Ask "what would I search for if I just learned about this issue type?"

**Examples:**
```markdown
Round 1: Started with D1 (cross-references), searched stages/ first
Round 2: Start with D2 (terminology), search templates/ first
Round 3: Start with D10 (file sizes), search reference/ first
```markdown

**Pattern Type Rotation:**
```markdown
Round 1: Exact string matches ("S5a", "Stage 6")
Round 2: Pattern variations ("S5a:", "S5a-", "(S5a)")
Round 3: Context-based ("back to S5a", "restart at S5.P1")
Round 4: Manual reading (spot-check random files)
```markdown

### STEP 3: Verify Fresh Approach (Self-Check)

**Before proceeding with Round N, verify ALL true:**

- [ ] Am I using DIFFERENT patterns than last round? (not just re-running same greps)
- [ ] Am I searching folders in DIFFERENT order? (not stages → templates → reference again)
- [ ] Am I questioning Round N-1's findings? (not assuming they were complete)
- [ ] Do I feel like "this is redundant, I already checked"? → ❌ NOT FRESH (continue anyway!)
- [ ] Am I skipping folders "because I know they're clean"? → ❌ NOT FRESH (check anyway!)

**If ANY checkbox unchecked:** Adjust approach before starting discovery.

### Anti-Patterns (What NOT Fresh Eyes Looks Like)

**❌ WRONG Approaches:**
```markdown
❌ "I already checked stages/ in Round 1, I'll skip it in Round 2"
   → Round 2 patterns might find issues Round 1 missed

❌ "I'll just re-run the same grep commands to verify they're still zero"
   → Re-running same patterns finds same things (or nothing)

❌ "I remember seeing this pattern everywhere, no need to check again"
   → Memory is unreliable, patterns change, files get edited

❌ "Round 1 was thorough, Round 2 is just a formality"
   → KAI-7 evidence: Round 3 found 70+ issues after Round 1-2 "thorough" checks

❌ "I'll read Round 1 report first to see what to look for"
   → Primes you to find Round 1 patterns, miss Round 2 patterns
```markdown

**✅ CORRECT Approaches:**
```markdown
✅ "Round 2: I'll search templates/ first (Round 1 started with stages/)"
   → Different folder order reveals different pattern distributions

✅ "Round 2: I'll use pattern variations (':' '-' '.') not tried in Round 1"
   → New patterns catch stragglers from Round 1 fixes

✅ "Round 2: I'll spot-read 10 random files manually (Round 1 was grep-only)"
   → Manual reading catches context issues grep misses

✅ "Round 3: I'll assume Round 1-2 missed something and search differently"
   → Adversarial mindset finds issues defensive mindset misses
```markdown

### Fresh Eyes Verification Checklist

**Before claiming "fresh eyes" for Round N, verify:**

**Pattern Diversity:**
- [ ] Used at least 1 pattern type NOT used in Round N-1
- [ ] Tried at least 3 variations of main pattern (punctuation, context, etc.)
- [ ] Searched with both automated (grep) AND manual (reading) methods

**Folder Coverage:**
- [ ] Searched folders in different order than Round N-1
- [ ] Didn't skip ANY folders (even if "known clean" from Round N-1)
- [ ] Gave equal attention to all folders (not just "problem areas")

**Mental Model:**
- [ ] Took 5-10 min break before starting Round N
- [ ] Did NOT review Round N-1 discoveries before Round N discovery
- [ ] Questioned Round N-1 completeness (didn't assume it was thorough)
- [ ] Felt like "this seems redundant" but continued anyway

**If ALL checked:** You have genuinely fresh eyes for Round N

**If ANY unchecked:** Pause, reset approach, try again

### Common Fresh Eyes Failures

**Failure Mode 1: "I'll just verify Round 1 findings"**
```bash
Round 1: grep -rn "S5a" → 60 matches, fixed all
Round 2: grep -rn "S5a" → 0 matches (verify)
Conclusion: ✅ Done!

Problem: Used SAME pattern. Missed "S5a:" "S5a-" "(S5a)"
Result: 20+ issues remain (found in Round 3 with variations)
```yaml

**Failure Mode 2: "I remember which folders have issues"**
```text
Round 1: stages/ had most issues, templates/ had few
Round 2: Focus on stages/, quick check templates/
Conclusion: ✅ Most thorough where it matters!

Problem: Memory bias, confirmation bias
Result: Missed template drift (templates not updated after stage changes)
```yaml

**Failure Mode 3: "Round 1 was comprehensive, Round 2 is validation"**
```text
Round 1: 4 hours, very thorough, found 60 issues
Round 2: 1 hour, just verify Round 1 fixes
Conclusion: ✅ Efficient validation!

Problem: Assumed Round 1 completeness, didn't search for new patterns
Result: Round 3 found 70+ different issues Round 1 never looked for
```

### How to Recover From Lost Fresh Eyes

**If you realize mid-round that you don't have fresh eyes:**

**STOP Immediately:**
1. Acknowledge: "I'm re-tracing Round N-1 steps"
2. Don't continue current discovery
3. Don't try to salvage current round

**Reset:**
1. Take 10-15 minute break (longer than 5 min)
2. Close all files, clear context
3. List what patterns Round N-1 used
4. List what patterns Round N SHOULD use (completely different)

**Restart:**
1. Start Round N discovery from scratch
2. Use patterns from "SHOULD use" list
3. Don't look at current round's partial findings
4. Document this reset in discovery report

---

### Critical Mindset Shifts

**From "Probably Fine" to "Prove It's Fine":**
```text
❌ WRONG: "I checked the main files, probably caught everything"
✅ CORRECT: "Verified all 50+ files, spot-checked 10 random files, tried 5 pattern variations"
```bash

**From "Grep Says Zero" to "Actually Zero":**
```bash
❌ WRONG: grep returns nothing, must be fixed
✅ CORRECT: grep returns nothing AND spot-read 5 files to confirm AND tried pattern variations
```markdown

**From "I Remember Checking" to "Documented Evidence":**
```text
❌ WRONG: "I think I checked that folder"
✅ CORRECT: "Checked stages/s5/ - see discovery_report.md line 45"
```markdown

---

## The Iterative Loop

### Loop Structure (Sub-Round System)

**The audit uses a 4 sub-round structure per round, organized by dimension category:**

```text
┌─────────────────────────────────────────────────────────────────┐
│         AUDIT LOOP (Repeat until ZERO new issues found)         │
│     MINIMUM 3 ROUNDS (each with 4 sub-rounds: 12 cycles min)    │
│  EXIT TRIGGER: Round N all 4 sub-rounds ZERO issues + 9 criteria│
└─────────────────────────────────────────────────────────────────┘

Round N:
  │
  ├─> Sub-Round N.1: Core Dimensions (D1, D2, D3, D8)
  │   ├─ S1: Discovery → S2: Planning → S3: Apply → S4: Verify → S5: Loop Decision
  │   └─ If 0 issues found → Sub-Round N.2
  │       If issues found → Fix all → Re-run Sub-Round N.1
  │
  ├─> Sub-Round N.2: Content Quality (D4, D5, D6, D13, D14)
  │   ├─ S1: Discovery → S2: Planning → S3: Apply → S4: Verify → S5: Loop Decision
  │   └─ If 0 issues found → Sub-Round N.3
  │       If issues found → Fix all → Re-run Sub-Round N.2
  │
  ├─> Sub-Round N.3: Structural (D9, D10, D11, D12)
  │   ├─ S1: Discovery → S2: Planning → S3: Apply → S4: Verify → S5: Loop Decision
  │   └─ If 0 issues found → Sub-Round N.4
  │       If issues found → Fix all → Re-run Sub-Round N.3
  │
  └─> Sub-Round N.4: Advanced (D7, D15, D16)
      ├─ S1: Discovery → S2: Planning → S3: Apply → S4: Verify → S5: Loop Decision
      └─ If 0 issues found → Round N complete
          If issues found → Fix all → Re-run Sub-Round N.4

Round N complete when: ALL 4 sub-rounds find 0 new issues
  ↓
Round N+1 (with fresh eyes, new patterns, different approach)
  ↓
EXIT (only if Round N had 0 issues in all 4 sub-rounds + 9 criteria met)
```markdown

### Why Sub-Rounds?

**Benefits of the 4 sub-round structure:**

1. **Dependency Management:** Core dimension fixes (broken references) applied before Structural checks (cross-file dependencies)
2. **Focused Discovery:** Check 4-5 related dimensions per sub-round, not all 17 at once
3. **Incremental Verification:** Verify fixes before moving to next category
4. **Mental Clarity:** Fresh mental model between dimension categories
5. **Better Tracking:** Know exactly which category and dimensions you're auditing
6. **Prevents Blind Spots:** ALL 17 dimensions checked systematically every round

### Dimension Organization by Sub-Round

**Sub-Round N.1: Core Dimensions (Always Check First)**
- D1: Cross-Reference Accuracy - File paths, links (90% automated)
- D2: Terminology Consistency - Notation, naming (80% automated)
- D3: Workflow Integration - Prerequisites, transitions (40% automated)
- D8: CLAUDE.md Sync - Root file alignment (60% automated)

**Why First:** Broken references and inconsistent notation affect all other checks

**Sub-Round N.2: Content Quality Dimensions**
- D4: Count Accuracy - File counts, iteration counts (90% automated)
- D5: Content Completeness - Missing sections, gaps (85% automated)
- D6: Template Currency - Template synchronization (70% automated)
- D13: Documentation Quality - Required sections (90% automated)
- D14: Content Accuracy - Claims vs reality (70% automated)

**Why Second:** Content fixes may reveal structural issues

**Sub-Round N.3: Structural Dimensions**
- D9: Intra-File Consistency - Within-file quality (80% automated)
- D10: File Size Assessment - Readability limits (100% automated)
- D11: Structural Patterns - Template compliance (60% automated)
- D12: Cross-File Dependencies - Stage transitions (30% automated)

**Why Third:** Structure depends on correct content and references

**Sub-Round N.4: Advanced Dimensions**
- D7: Context-Sensitive Validation - Intentional exceptions (20% automated)
- D15: Duplication Detection - DRY principle (50% automated)
- D16: Accessibility - Navigation, UX (80% automated)

**Why Last:** Advanced checks require all other dimensions to be clean

### Why Minimum 3 Rounds (12 Sub-Rounds Total)?

**3 rounds × 4 sub-rounds = 12 minimum cycles**

**Rationale:**
- Each round uses different patterns and approaches
- Sub-rounds within Round 1 catch different issue types
- Round 2 finds patterns Round 1 missed (fresh eyes)
- Round 3 validates Round 1-2 were thorough

**Historical Evidence from KAI-7 Audit (Pre-Sub-Round System):**
- **Round 1:** Found 4 issues (step number mapping)
- **Round 2:** Found 10 issues (router links, path formats)
- **Round 3:** Found 70+ issues (notation standardization)
- **Round 4:** Found 20+ issues (cross-references)
- **Total:** 104+ issues across 4 rounds

**With sub-rounds:** Would have caught all 104 issues across fewer rounds due to systematic dimension coverage

### Sub-Round Progression Pattern

**Round 1: Initial Discovery**
- Sub-Round 1.1 (Core): Basic patterns, exact string matches, obvious errors
- Sub-Round 1.2 (Content): File counts, missing sections, placeholder text
- Sub-Round 1.3 (Structural): File sizes, basic structure compliance
- Sub-Round 1.4 (Advanced): Obvious duplicates, missing TOCs

**Round 2: Pattern Variations (Fresh Eyes)**
- Sub-Round 2.1 (Core): Punctuation variations, contextual patterns
- Sub-Round 2.2 (Content): Content accuracy claims, template drift
- Sub-Round 2.3 (Structural): Cross-file dependency validation, intra-file consistency
- Sub-Round 2.4 (Advanced): Context-sensitive analysis, subtle duplications

**Round 3+: Deep Validation**
- Sub-Round 3.1 (Core): Manual reading, edge cases, exception validation
- Sub-Round 3.2 (Content): Spot-checks, random sampling
- Sub-Round 3.3 (Structural): Complete dependency chain validation
- Sub-Round 3.4 (Advanced): Final confidence calibration

---

## Exit Criteria

### MANDATORY Loop Conditions (Sub-Round System)

```text
┌─────────────────────────────────────────────────────────────────┐
│  🚨 CRITICAL: You MUST continue looping until:                  │
│                                                                  │
│  SUB-ROUND LEVEL:                                               │
│  - Current sub-round finds ZERO new issues                      │
│  - All issues from current sub-round RESOLVED                   │
│  - If issues found → Fix ALL → Re-run same sub-round            │
│                                                                  │
│  ROUND LEVEL:                                                   │
│  - ALL 4 sub-rounds complete with ZERO issues each              │
│  - Sub-Rounds 1, 2, 3, 4 all found 0 new issues                 │
│                                                                  │
│  AUDIT LEVEL:                                                   │
│  - Minimum 3 complete rounds (12 sub-rounds)                    │
│  - Latest round had 0 issues in all 4 sub-rounds                │
│  - ALL 9 exit criteria met (see below)                          │
└─────────────────────────────────────────────────────────────────┘
```markdown

**Loop Logic:**
```text
Sub-Round N.X found issues → Fix ALL → Re-run Sub-Round N.X → Repeat until 0 issues
Sub-Round N.X found ZERO issues → Proceed to Sub-Round N.(X+1)
Sub-Round N.4 found ZERO issues + Sub-Rounds N.1-N.3 were clean → Round N complete
Round N complete (all 4 sub-rounds clean) → Round N+1 (fresh patterns)
Round N complete + Minimum 3 rounds + ALL 9 criteria met → Consider exit
```markdown

### ALL 9 Criteria Must Be Met (Audit Level)

**Cannot exit audit loop until ALL of these are satisfied:**

1. ✅ **All issues resolved:** Every issue from ALL rounds AND sub-rounds fixed and verified
2. ✅ **Zero new issues:** Latest round found ZERO issues in ALL 4 sub-rounds
3. ✅ **Zero verification findings:** Latest round verifications (S4) found ZERO new issues across all sub-rounds
4. ✅ **Minimum 3 rounds:** At least 3 complete rounds (12 sub-rounds total) completed
5. ✅ **All remaining documented:** All remaining instances documented as intentional
6. ✅ **User has NOT challenged:** User has not questioned findings
7. ✅ **Confidence score:** ≥ 80% confidence in completeness across all 17 dimensions
8. ✅ **Pattern diversity:** ≥ 5 pattern types used per dimension category across rounds
9. ✅ **Spot-check clean:** 10+ files manually checked per sub-round, zero issues

**For detailed criteria with sub-requirements, see `stages/stage_5_loop_decision.md` → "Exit Criteria Checklist"**

### Critical Rules

**If current sub-round found ANY issues:**
```text
└─> 🔄 MANDATORY RE-RUN of same sub-round
     - Fix ALL issues from current sub-round
     - Re-run SAME sub-round (e.g., if 2.3 found issues, re-run 2.3)
     - Continue until sub-round finds ZERO issues
     - THEN proceed to next sub-round
```markdown

**If sub-round clean but still in same round:**
```text
└─> ✅ PROCEED to next sub-round
     - Sub-Round N.1 clean → N.2
     - Sub-Round N.2 clean → N.3
     - Sub-Round N.3 clean → N.4
     - Sub-Round N.4 clean → Round N complete
```

**If round complete (all 4 sub-rounds clean):**
```text
└─> 🔄 PROCEED to Round N+1 (with fresh eyes)
     - Start at Sub-Round (N+1).1
     - Use fresh patterns, different approach
     - Continue until achieving clean round
```markdown

**If user challenges you in ANY way:**
```bash
└─> 🚨 IMMEDIATE LOOP BACK to Round 1, Sub-Round 1.1
     (User challenge = evidence you missed something)
```diff

**Exit conditions:**
- ✅ Round N complete (all 4 sub-rounds clean)
- ✅ Minimum 3 rounds complete (12 sub-rounds total)
- ✅ ALL 9 exit criteria met
- ✅ User approves exit

**See Stage 5 guide for complete decision logic, verification checklists, and loop preparation.**

---

## File Size Considerations

### Rationale

**Large files create barriers for agent comprehension and may cause agents to miss critical instructions.**

When agents read guides at task start, overwhelming file size impacts effectiveness. Large guides may be partially skipped, misunderstood, or cause agents to miss mandatory steps.

**User Directive:** "The point of it is to ensure that agents are able to effectively read and process the guides as they are executing them. I want to ensure that agents have no barriers in their way toward completing their task, or anything that would cause them to incorrectly complete their task."

### File Size Policy

**CLAUDE.md:**
- **MUST NOT exceed 40,000 characters**
- This is a hard policy limit, not a guideline
- Rationale: Agents read CLAUDE.md at start of EVERY task
- Overwhelming file size impacts agent effectiveness

**Workflow Guides:**
- **Large files (>600 lines)** should be evaluated for potential splitting
- Consider if file serves multiple distinct purposes
- Check if content has natural subdivisions
- Assess if agents report difficulty following guide

### When to Split Files

**Evaluate splitting if ANY true:**
- File exceeds readability threshold (varies by file type)
- Content has natural subdivisions (e.g., phases, iterations)
- Agents report difficulty following guide
- File serves multiple distinct purposes
- File is referenced in context where only portion is relevant

**Don't split if:**
- Content is cohesive single workflow
- Splitting would create excessive navigation overhead
- File is primarily reference material (intended to be comprehensive)

### How Pre-Audit Script Checks File Size

The automated pre-audit script (`scripts/pre_audit_checks.sh`) performs two file size checks:

**1. Workflow Guide Size Check (D10):**
- Checks all `stages/**/*.md` files
- Flags files >1250 lines as **TOO LARGE** (critical issue)
- Updated policy: Baseline increased from 1000 → 1250 lines during Meta-Audit (2026-02-05)

**2. CLAUDE.md Character Count (D10 Policy Compliance):**
- Checks `CLAUDE.md` character count
- Flags if exceeds 40,000 characters (critical policy violation)
- Reports overage amount
- Recommends extraction to separate files

### Example: CLAUDE.md Reduction Strategy

If CLAUDE.md exceeds 40,000 characters, extract detailed content to separate files:

**Extraction Candidates:**
- Detailed workflow descriptions → `EPIC_WORKFLOW_USAGE.md`
- Stage-specific workflows → individual stage guide references
- Protocol details → respective protocol files (debugging/, missed_requirement/)
- Anti-pattern examples → `common_mistakes.md`

**Keep in CLAUDE.md:**
- Quick Start section
- Phase Transition Protocol (essential)
- Critical Rules Summary
- Git Safety Rules
- Tool usage policy
- Stage Workflows Quick Reference (navigation only)

**Target:** Replace extracted sections with short references pointing to detailed guides.

**Validation:** After extraction, verify CLAUDE.md ≤40,000 characters AND agents can still effectively use streamlined CLAUDE.md.

---

## Historical Evidence

### Real Audit Data (KAI-7 S10.P1 Guide Updates)

**Context:** After completing S10.P1 guide update workflow, ran formal audit per protocol

**Session Duration:** 4+ hours
**Total Rounds:** 4 rounds before exit criteria met
**Total Issues Found:** 104+ instances across 50+ files
**Premature Completion Attempts:** 0 (protocol followed correctly)

**Round Breakdown:**

| Round | Focus | Patterns Used | Issues Found | Files Modified |
|-------|-------|---------------|--------------|----------------|
| 1 | Step number mapping | Exact numeric searches | 4 | 2 |
| 2 | Router links, paths | File path patterns | 10 | 12 |
| 3 | Notation standardization | Old notation variations | 70+ | 30+ |
| 4 | Cross-reference validation | Automated link checking | 20+ | 29 |

**Key Findings:**
- Each round found issues invisible to previous rounds
- Different pattern types revealed different error categories
- Manual context analysis prevented false positives
- Automated pre-checks would have caught ~60% of Round 1-2 issues

**Lessons Learned:**
- Minimum 3 rounds is NOT arbitrary - it's evidence-based
- Pattern diversity is critical (same patterns each round = same blind spots)
- Fresh eyes approach works (breaking between rounds found new issues)
- User skepticism is warranted (agents naturally want to finish quickly)

---

## Critical External Files

### CLAUDE.md (Project Root)

**Location:** `CLAUDE.md` (project root, 3 levels up from audit/)

**Why Critical:** Often the FIRST file agents read. If out of sync with guides, agents follow wrong instructions.

**What to Check:**
- Step numbers in quick reference match actual guide step numbers
- Stage descriptions match guide content
- Workflow diagrams match actual workflow structure
- Decision criteria match guide decision criteria
- Mandatory flags/checkpoints are reflected in quick reference

**Example Issue (from KAI-7):**
```text
CLAUDE.md said: "S1 Step 4.8-4.9" (parallel work offer)
Actual guide had: "Step 5.8-5.9"

Result: Agent followed CLAUDE.md, looked for non-existent steps,
        skipped parallelization offer entirely

Root cause: CLAUDE.md was NOT in audit scope
```

**Audit Dimension:** D8: CLAUDE.md Synchronization

**How to Check:**
1. Read CLAUDE.md Stage Workflows section
2. For each stage, verify step numbers match actual guide
3. For each decision point, verify criteria match guide
4. For each mandatory checkpoint, verify it's documented in both

---

## Next Steps

**After reading this overview:**

1. **If starting new audit:**
   - Run `scripts/pre_audit_checks.sh`
   - Read `stages/stage_1_discovery.md`
   - Begin Round 1 Discovery

2. **If resuming audit:**
   - Check which stage you're in
   - Read that stage's guide
   - Continue from where you left off

3. **If uncertain about dimension:**
   - Check `README.md` dimension table
   - Read relevant dimension guide
   - Apply to current round

4. **If user challenged findings:**
   - Read `reference/user_challenge_protocol.md`
   - Reset to Round 1
   - Use fresh patterns

---

**Remember:** Better to over-audit than under-audit. When uncertain, continue auditing.

**Next Guide:** `stages/stage_1_discovery.md` (when ready to start/resume Round 1)
