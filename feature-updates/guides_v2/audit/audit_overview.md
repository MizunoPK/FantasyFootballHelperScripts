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

### The 16 Audit Dimensions

**Core Accuracy (D1-D4):**
- ✅ **D1: Cross-Reference Accuracy** - All file paths, stage references, and cross-links are valid
- ✅ **D2: Terminology Consistency** - Notation, naming conventions, and terminology are uniform
- ✅ **D3: Workflow Integration** - Guides correctly reference each other and form cohesive workflows
- ✅ **D4: Count Accuracy** - File counts, stage counts, iteration counts match reality

**Content Quality (D5-D6, D13-D14):**
- ✅ **D5: Content Completeness** - No missing sections, gaps in coverage, or orphaned references
- ✅ **D6: Template Currency** - Templates reflect current workflow structure and terminology
- ✅ **D13: Documentation Quality** - All required sections present, no TODOs or placeholders
- ✅ **D14: Content Accuracy** - Claims in guides match reality (step counts, durations, etc.)

**Structural Quality (D9-D12):**
- ✅ **D9: Intra-File Consistency** - Within-file quality (headers, checklists, formatting)
- ✅ **D10: File Size Assessment** - Files within readable limits, complex files split appropriately
- ✅ **D11: Structural Patterns** - Guides follow expected template structures
- ✅ **D12: Cross-File Dependencies** - Stage prerequisites match outputs, workflow continuity

**Advanced Quality (D7-D8, D15-D16):**
- ✅ **D7: Context-Sensitive Validation** - Same pattern validated differently based on context
- ✅ **D8: CLAUDE.md Synchronization** - Root file quick references match actual guide content
- ✅ **D15: Duplication Detection** - No duplicate content or contradictory instructions
- ✅ **D16: Accessibility** - Navigation aids, TOCs, scannable structure

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

**1. Fresh Eyes, Zero Assumptions**
- Approach each round as if you've never seen the codebase
- Don't trust previous rounds - verify everything again
- Clear mental model between rounds (take 5-min break)

**2. User Skepticism is Healthy**
- When user challenges you, THEY ARE USUALLY RIGHT
- "Are you sure?" = red flag you missed something
- Do NOT defend findings - re-verify immediately

**3. Evidence Over Claims**
- Show actual file contents, not just grep output
- Before/after comparisons for every fix
- Spot-check random files to verify grep accuracy

**4. Iterative Until Zero**
- Minimum 3 rounds required
- Continue until round finds ZERO new issues
- Each round uses completely different patterns

**5. Better to Over-Audit Than Under-Audit**
- False positives can be resolved
- False negatives cause user confusion
- When uncertain, flag for review

### Critical Mindset Shifts

**From "Probably Fine" to "Prove It's Fine":**
```
❌ WRONG: "I checked the main files, probably caught everything"
✅ CORRECT: "Verified all 50+ files, spot-checked 10 random files, tried 5 pattern variations"
```

**From "Grep Says Zero" to "Actually Zero":**
```
❌ WRONG: grep returns nothing, must be fixed
✅ CORRECT: grep returns nothing AND spot-read 5 files to confirm AND tried pattern variations
```

**From "I Remember Checking" to "Documented Evidence":**
```
❌ WRONG: "I think I checked that folder"
✅ CORRECT: "Checked stages/s5/ - see discovery_report.md line 45"
```

---

## The Iterative Loop

### Loop Structure

```
┌─────────────────────────────────────────────────────────────────┐
│         AUDIT LOOP (Repeat until ZERO new issues found)         │
│                    MINIMUM 3 ROUNDS REQUIRED                     │
└─────────────────────────────────────────────────────────────────┘

Round 1: Initial Discovery (new audit, broad patterns)
  ↓
Stage 1: Discovery → Stage 2: Planning → Stage 3: Fixes → Stage 4: Verify → Stage 5: Decision
  ↓                                                                                    ↓
  ├────────────────────────────────────────────────────────────────────────────────────┤
  │                                                                                    │
  └─> Round 2: Fresh Eyes (different patterns, different order) ←──────────────────┘
       ↓
       Stage 1-5 (new patterns, new approach)
       ↓
       Round 3: Deep Validation (context-sensitive, spot-checks)
       ↓
       Stage 1-5 (manual review, edge cases)
       ↓
       EXIT (only if ALL exit criteria met + user approves)
```

### Why Minimum 3 Rounds?

**Historical Evidence from KAI-7 Audit:**
- **Round 1:** Found 4 issues (step number mapping)
- **Round 2:** Found 10 issues (router links, path formats) - WOULD HAVE MISSED if stopped after Round 1
- **Round 3:** Found 70+ issues (notation standardization) - WOULD HAVE MISSED if stopped after Round 2
- **Round 4:** Found 20+ issues (cross-references) - WOULD HAVE MISSED if stopped after Round 3

**Total:** 104+ issues found across 4 rounds. Each round used completely different discovery approach.

**Key Insight:** Each round's patterns were invisible to previous rounds. Multiple perspectives required.

### Round Progression Pattern

**Round 1: Broad Strokes**
- Basic patterns (exact string matches)
- Obvious errors (clearly wrong stage numbers)
- High-frequency issues
- Template files first (errors propagate)

**Round 2: Variations**
- Pattern variations (different punctuation, spacing)
- Contextual patterns ("back to 5a", "restart S5.P1")
- Systematic folder-by-folder search
- Different file order than Round 1

**Round 3: Deep Dive**
- Context-sensitive validation
- Manual reading of sections
- Spot-checks of random files
- Edge cases and exceptions

**Round 4+: Verification**
- Re-run all previous patterns
- Random sampling
- User challenge follow-up
- Final confidence calibration

---

## Exit Criteria

### Mandatory Requirements (ALL Must Be True)

**Cannot exit loop until ALL of these are satisfied:**

1. ✅ **Minimum Rounds:** Completed at least 3 rounds with fresh eyes
   - Each round used different patterns
   - Each round explored different file orders
   - Clear break between rounds (fresh perspective)

2. ✅ **Zero New Discoveries:** Round N Discovery finds ZERO new issues
   - Tried at least 5 different pattern types
   - Searched all folders systematically
   - Used automated scripts + manual search

3. ✅ **Zero Verification Findings:** Round N Verification finds ZERO new issues
   - Re-ran all patterns from Discovery
   - Tried pattern variations not used in Discovery
   - Spot-checked 10+ random files

4. ✅ **All Remaining Documented:** All remaining pattern matches documented as intentional
   - File path + line number
   - Why it's intentional
   - Why it's acceptable
   - Context analysis performed

5. ✅ **User Verification Passed:** User has NOT challenged findings
   - No "are you sure?" questions
   - No "did you actually make fixes?" questions
   - No "assume everything is wrong" requests

6. ✅ **Confidence Calibrated:** Confidence score ≥ 80%
   - See `reference/confidence_calibration.md`
   - Self-assessed using scoring rubric
   - No red flags present

7. ✅ **Pattern Diversity:** Used at least 5 different pattern types across all rounds
   - Basic exact matches
   - Pattern variations
   - Contextual patterns
   - Manual reading
   - Spot-checks

8. ✅ **Spot-Check Clean:** Random sample of 10+ files shows zero issues
   - Files selected randomly (not cherry-picked)
   - Manually read sections (not just grep)
   - No issues found

### Failing ANY Criterion = Continue Loop

**If ANY criterion fails:**
```
└─> 🔄 LOOP BACK to Stage 1 Round N+1
     Requirements for next round:
     - Clear all assumptions (fresh eyes)
     - Use DIFFERENT patterns than any previous round
     - Explore folders in DIFFERENT order
     - Question ALL previous findings
     - Incorporate lessons from this round
```

### Special Case: User Challenge

**If user challenges you in ANY way:**
```
└─> 🚨 IMMEDIATE LOOP BACK to Round 1
     - User challenge = evidence you missed something
     - Do NOT defend or justify - re-verify EVERYTHING
     - Assume you were wrong, prove yourself right
     - Use completely fresh patterns and approach
     - Reset round counter to 1
```

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

**Location:** `C:\Users\kmgam\code\FantasyFootballHelperScripts\CLAUDE.md`

**Why Critical:** Often the FIRST file agents read. If out of sync with guides, agents follow wrong instructions.

**What to Check:**
- Step numbers in quick reference match actual guide step numbers
- Stage descriptions match guide content
- Workflow diagrams match actual workflow structure
- Decision criteria match guide decision criteria
- Mandatory flags/checkpoints are reflected in quick reference

**Example Issue (from KAI-7):**
```
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
