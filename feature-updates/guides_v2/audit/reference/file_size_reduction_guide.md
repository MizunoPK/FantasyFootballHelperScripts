# File Size Reduction Guide

**Purpose:** Systematic approach to evaluating and reducing large files for agent usability
**When Used:** Stage 3 (Apply Fixes) after content accuracy fixes, before verification
**Reading Time:** 15-20 minutes

---

## Table of Contents

1. [Why File Size Matters](#why-file-size-matters)
2. [File Size Thresholds](#file-size-thresholds)
3. [Evaluation Framework](#evaluation-framework)
4. [Reduction Strategies](#reduction-strategies)
5. [CLAUDE.md Reduction Protocol](#claudemd-reduction-protocol)
6. [Workflow Guide Reduction Protocol](#workflow-guide-reduction-protocol)
7. [Validation Checklist](#validation-checklist)

---

## Why File Size Matters

**User Directive:** "The point of it is to ensure that agents are able to effectively read and process the guides as they are executing them. I want to ensure that agents have no barriers in their way toward completing their task, or anything that would cause them to incorrectly complete their task."

### The Agent Workflow Philosophy

**Agents need three things to succeed:**
1. **Know exactly what to do next** - Linear, clear workflow
2. **Have exactly what they need to do work** - All required context accessible
3. **Not go off-script** - Read everything they should, follow instructions completely

### Impact on Agent Performance

**Large files create barriers:**
- **Comprehension barriers:** Overwhelming content volume → agents skim/skip sections
- **Navigation barriers:** Hard to find sections → agents work from memory instead of re-reading
- **Processing barriers:** Information overload → agents miss critical instructions
- **Execution barriers:** Incomplete reading → incorrect task completion

**BUT splitting files ALSO creates barriers:**
- **Navigation barriers:** Linked content → agents skip ("I'll check that later")
- **Context loss:** Jumping between files → agents lose big picture
- **Missing critical content:** Separate files for checkpoints → agents don't actually re-read them
- **Incomplete workflow:** Scattered instructions → agents miss required steps

### Critical Principle: Context Over Compression

**WRONG approach:** Split file to reduce size, regardless of impact
**RIGHT approach:** Reduce duplication and unnecessary detail while keeping workflow context intact

**Evidence:**
- Mandatory checkpoints MUST be inline with workflow (agents won't follow links to re-read)
- Exit criteria MUST be at end of workflow (agents need immediate context)
- Common mistakes SHOULD be visible during workflow (pattern recognition)
- Splitting workflow steps into separate files increases skip rate

---

## File Size Thresholds

### CLAUDE.md (Root File)

**HARD LIMIT:** 40,000 characters
- **Status:** POLICY VIOLATION if exceeded
- **Action:** MUST reduce before audit completion
- **Priority:** P1 (Critical)

### Workflow Guides (stages/, reference/, etc.)

**Line Count Thresholds:**

| Size | Threshold | Status | Action Required |
|------|-----------|--------|-----------------|
| Small | <600 lines | ✅ OK | None |
| Medium | 600-800 lines | ⚠️ WARNING | Evaluate for split |
| Large | 800-1000 lines | ⚠️ LARGE | Strongly consider split |
| Too Large | >1000 lines | ❌ CRITICAL | MUST reduce or justify |

**Character Count (for CLAUDE.md only):**
- ≤40,000 chars: ✅ OK
- 40,001-45,000 chars: ❌ VIOLATION (reduce by 10-15%)
- >45,000 chars: ❌ SEVERE (reduce by 20%+)

---

## Evaluation Framework

### Step 1: Identify Large Files

**From Pre-Audit Script Output:**
```bash
❌ TOO LARGE: stages/s5/s5_p1_planning_round1.md (1200 lines)
⚠️  LARGE: stages/s1/s1_epic_planning.md (650 lines)
❌ POLICY VIOLATION: CLAUDE.md (45786 chars) exceeds 40,000
```

**Priority Order:**
1. CLAUDE.md (if exceeds 40,000 chars) - P1
2. Files >1000 lines - P1
3. Files 800-1000 lines - P2
4. Files 600-800 lines - P3

### Step 2: Evaluate Each Large File

**For EACH large file, answer these questions:**

**1. Purpose Analysis:**
- [ ] What is the primary purpose of this file?
- [ ] Does it serve multiple distinct purposes?
- [ ] Is it a router, guide, reference, or template?

**2. Content Analysis:**
- [ ] Does content have natural subdivisions? (phases, iterations, categories)
- [ ] Is there duplicate content across sections?
- [ ] Are there detailed examples that could be extracted?
- [ ] Are there reference materials that could live elsewhere?

**3. Usage Analysis:**
- [ ] How do agents use this file? (read once, reference repeatedly, etc.)
- [ ] Do agents need ALL content at once, or only portions?
- [ ] Is file referenced in contexts where only portion is relevant?

**4. Reduction Potential:**
- [ ] Can content be extracted to separate files WITHOUT harming usability?
- [ ] Would splitting create excessive navigation overhead?
- [ ] Is there a clear extraction strategy with minimal disruption?

### Step 3: Make Split/Reduce Decision

**REDUCE if ANY true:**
- File exceeds hard limit (CLAUDE.md >40,000 chars, guides >1000 lines)
- Content has clear subdivisions (phases, iterations, categories)
- Agents report difficulty navigating file
- File serves multiple distinct purposes
- Extraction improves agent workflow (less searching, clearer structure)

**KEEP if ALL true:**
- File is cohesive single workflow
- Splitting would create excessive navigation overhead
- Content is interdependent (needs to be read together)
- File is primarily reference material (intended to be comprehensive)
- Size is justified by purpose (e.g., comprehensive dimension guide)

---

## What NEVER to Extract (Critical Content)

**🚨 THESE MUST REMAIN INLINE WITH WORKFLOW:**

### 1. Mandatory Checkpoints
**Why:** Checkpoints require agents to re-read specific sections. If checkpoints are in a separate file, agents won't actually re-read them.

**Examples:**
- `## 🛑 MANDATORY CHECKPOINT 1: Re-read Critical Rules`
- `## 🛑 CHECKPOINT: Verify Prerequisites Complete`

**Rule:** Keep ALL checkpoint sections inline in workflow guide. Never extract to separate file.

### 2. Exit Criteria
**Why:** Exit criteria must be at END of workflow to provide immediate context for completion verification.

**Examples:**
- `## Exit Criteria` section at end of guide
- Success checklists for current workflow

**Rule:** Keep exit criteria in same file as workflow. Agents need to check completion criteria immediately after finishing steps.

###3. Prerequisites
**Why:** Prerequisites must be at BEGINNING of workflow so agents verify before starting.

**Examples:**
- `## Prerequisites` section at start of guide
- Pre-flight checklists

**Rule:** Keep prerequisites in same file as workflow. Agents must verify requirements before proceeding.

### 4. Critical Rules / Constraints
**Why:** Agents need to see constraints DURING workflow execution, not in separate reference file.

**Examples:**
- `## Critical Rules` section
- `## Common Mistakes to Avoid`
- `## Anti-Patterns`

**Rule:** Keep critical rules visible in workflow guide. Agents need pattern recognition while working, not after navigation.

### 5. Linear Workflow Steps
**Why:** Breaking sequential steps across files destroys workflow continuity and increases skip rate.

**Examples:**
- Step 1 → Step 2 → Step 3 (must be in same file)
- Phase sub-steps (e.g., S1.P3.1 → S1.P3.2 → S1.P3.3)

**Rule:** Keep sequential steps together. Only extract if steps are INDEPENDENTLY executable (different phases/rounds).

### What CAN Be Extracted (Supplementary Content)

**✅ SAFE TO EXTRACT:**
- Detailed examples (keep 1-2 brief examples inline, extract rest)
- Historical context / backstory
- Extensive reference tables (keep summary inline, extract details)
- Duplicate content (consolidate to single reference file)
- Alternative approaches (keep recommended approach inline, extract alternatives)
- Appendices and deep dives

---

## Reduction Strategies

**Priority Order:** Always try strategies in this order:
1. **Reduce Duplication** (Strategy 0) - Try FIRST, least disruptive
2. **Consolidate Redundant Content** (Strategy 3) - Second choice
3. **Extract Supplementary Content** (Strategy 2, 4) - If still too large
4. **Extract to Sub-Guides** (Strategy 1) - Last resort, only for truly independent sections

### Strategy 0: Reduce Duplication (Try First - Least Disruptive)

**When:** File references detailed guide but also duplicates content from that guide

**Example Problem:**
```text
s1_epic_planning.md (1017 lines):
  - Step 3: Discovery Phase (MANDATORY)
    - Overview of Discovery workflow (69 lines)
    - Explanation of Discovery loop
    - Example Discovery outputs
    - "See full guide: stages/s1/s1_p3_discovery_phase.md"

s1_p3_discovery_phase.md (1006 lines):
  - Complete Discovery workflow (all details)
```

**Issue:** Step 3 section duplicates content that's already in the dedicated guide. Agents read overview in main file, then read full details in sub-guide → redundant.

**Solution: Minimal Reference Pattern**
```text
s1_epic_planning.md (reduces to ~960 lines):
  - Step 3: Discovery Phase (MANDATORY)
    - **Goal:** Explore problem space through iterative research and user Q&A
    - **Time-Box:** 1-4 hours depending on epic size
    - **Exit Condition:** 3 consecutive iterations with NO NEW QUESTIONS
    - **Detailed Guide:** stages/s1/s1_p3_discovery_phase.md (READ ENTIRE GUIDE)
    - **Key Outputs:** DISCOVERY.md, solution approach, scope definition, feature breakdown

s1_p3_discovery_phase.md (1006 lines):
  - Complete Discovery workflow (unchanged)
```

**Process:**
1. Identify sections that reference detailed guides
2. Check if section duplicates content from referenced guide
3. Reduce to: Goal + Exit Condition + Link to detailed guide + Key Outputs
4. Keep 4-8 line summary maximum
5. Ensure agents know to READ THE FULL GUIDE (explicit instruction)

**Validation:**
- [ ] Reduced by 40-70 lines per duplicated section
- [ ] Agents still understand what section does (goal + exit condition)
- [ ] Clear instruction to read detailed guide
- [ ] No information lost (it's in the detailed guide)

**When NOT to use:**
- Section doesn't have detailed guide elsewhere
- Section provides unique context not in detailed guide
- Removing detail would confuse workflow sequence

---

### Strategy 1: Break Into Sequential Phases (Preferred for Large Workflows)

**When:** File contains a multi-step workflow that can be broken into sequential phases that agents execute one at a time

**Key Principle:** Agents read ONE phase guide at a time → complete phase → read NEXT phase guide. This creates focus and reduces cognitive load.

**This is DIFFERENT from extracting supplementary content:**
- ❌ BAD: Extract checkpoints to separate file (agents skip links)
- ✅ GOOD: Break workflow into Phase 1 → Phase 2 → Phase 3, each with complete guide (agents read sequentially)

**Examples Already in System:**
- S5: Split into S5.P1 (Round 1), S5.P2 (Round 2), S5.P3 (Round 3)
- S7: Split into S7.P1 (Smoke), S7.P2 (QC Rounds), S7.P3 (Final Review)
- S1: Extracted S1.P3 (Discovery Phase) as separate guide

**When to Use This Strategy:**
- Workflow has clear sequential phases (Phase A completes before Phase B starts)
- Each phase is independently executable (Phase 1 has its own prerequisites/exit criteria)
- Breaking into phases improves focus (agent only needs Phase 1 context while in Phase 1)
- File >1000 lines with natural subdivisions

**Example: Breaking S1 Epic Planning (1017 lines)**

**Before:**
```text
s1_epic_planning.md (1017 lines)
  - Step 1: Initial Setup
  - Step 2: Epic Analysis
  - Step 3: Discovery Phase (references s1_p3_discovery_phase.md)
  - Step 4: Feature Breakdown Proposal
  - Step 5: Epic Structure Creation
  - Step 6: Transition to S2
  - 5 Mandatory Checkpoints
  - Exit Criteria
  - Common Mistakes
```

**After (Sequential Phase Breakdown):**
```text
s1_epic_planning.md (200 lines - Router)
  - Overview of S1 workflow
  - Phase structure (P1 → P2 → P3 → P4)
  - Navigation to phases
  - Overall exit criteria

s1_p1_preparation.md (~300 lines)
  - Prerequisites for S1
  - Step 1: Initial Setup (branch, folder, README)
  - Step 2: Epic Analysis (goals, constraints, scope)
  - Checkpoints 1-2 (inline)
  - Exit Criteria for P1
  - Next: Read s1_p2_discovery.md

s1_p2_discovery.md (rename existing s1_p3_discovery_phase.md)
  - Prerequisites for Discovery
  - Step 3: Discovery Phase (full workflow)
  - Discovery loop iterations
  - Checkpoints 3 (inline)
  - Exit Criteria for P2
  - Next: Read s1_p3_structure_creation.md

s1_p3_structure_creation.md (~400 lines)
  - Prerequisites (Discovery approved)
  - Step 4: Feature Breakdown Proposal
  - Step 5: Epic Structure Creation
  - Step 6: Transition to S2
  - Checkpoints 4-5 (inline)
  - Exit Criteria for P3
  - Next: S2
```

**Benefits:**
- Agent reads ~200-400 lines per phase (vs 1017 lines all at once)
- Each phase guide contains only what's needed for THAT phase
- Checkpoints remain inline with workflow (not skipped)
- Agent has complete context for current phase
- Exit criteria immediately after phase steps (clear completion signal)

**Process:**
1. Identify natural phase boundaries (where one logical chunk ends, next begins)
2. Create separate guide for each phase (s1_p1_*.md, s1_p2_*.md, etc.)
3. Each phase guide must include:
   - Prerequisites for THIS phase
   - Steps for THIS phase only
   - Checkpoints for THIS phase (inline)
   - Exit criteria for THIS phase
   - "Next: Read [next phase guide]" instruction
4. Convert main guide to router with:
   - Workflow overview
   - Phase structure diagram
   - Links to phase guides
   - Overall S1 exit criteria
5. Update CLAUDE.md Stage Workflows section to reference phase guides

**Validation:**
- [ ] Each phase guide is <600 lines (ideally 300-500)
- [ ] Phase boundaries make logical sense (clear stopping points)
- [ ] Each phase is independently executable (doesn't require reading other phases simultaneously)
- [ ] Agent knows exactly which guide to read next
- [ ] No information lost in restructuring
- [ ] All checkpoints remain inline with their respective phase steps

**When NOT to Use This Strategy:**
- Steps are tightly interdependent (need to see all steps together for context)
- File is already <600 lines (not worth navigation overhead)
- Splitting would create artificial boundaries (no natural phase transitions)
- Workflow is iterative/looping (not sequential)
- File is reference material (glossary, FAQ, etc.) - users dip in/out randomly

**Example:**
```text
Before:
stages/s5/s5_implementation_planning.md (1200 lines)
  - Round 1 (400 lines)
  - Round 2 (400 lines)
  - Round 3 (400 lines)

After:
stages/s5/s5_implementation_planning.md (200 lines - router)
stages/s5/s5_p1_planning_round1.md (400 lines)
stages/s5/s5_p2_planning_round2.md (400 lines)
stages/s5/s5_p3_planning_round3.md (400 lines)
```

**Process:**
1. Identify natural subdivision points (phases, iterations)
2. Create separate files for each subdivision
3. Convert original to router (table of contents + navigation)
4. Update all cross-references

**Validation:**
- [ ] Original file now <600 lines (ideally <300 for router)
- [ ] Sub-guides each <600 lines
- [ ] Router provides clear navigation
- [ ] All cross-references updated

### Strategy 2: Extract to Reference Files

**When:** File contains detailed reference material not needed during main workflow

**Example:**
```text
Before:
CLAUDE.md (45,786 chars)
  - Quick Start (2,000 chars)
  - Stage Workflows (12,000 chars)
  - Anti-Patterns (3,000 chars)
  - Detailed Examples (8,000 chars)
  - Reference Tables (5,000 chars)

After:
CLAUDE.md (38,000 chars)
  - Quick Start (2,000 chars)
  - Stage Workflows Quick Reference (4,000 chars) → Links to EPIC_WORKFLOW_USAGE.md
  - Critical Rules (3,000 chars)
  - Git Safety (2,000 chars)

Extracted:
reference/anti_patterns.md (3,000 chars) - detailed examples
reference/detailed_examples.md (8,000 chars)
reference/workflow_reference_tables.md (5,000 chars)
```

**Process:**
1. Identify sections with detailed content not critical for quick reference
2. Create dedicated reference files
3. Replace detailed sections with short summaries + links
4. Verify critical content remains in original

**Validation:**
- [ ] Original file ≤40,000 chars (CLAUDE.md) or <600 lines (guides)
- [ ] Critical content still in original (agents don't miss essentials)
- [ ] Links to extracted content clear and accessible
- [ ] Extracted files have clear purpose and structure

### Strategy 3: Consolidate Redundant Content

**When:** File has duplicate or near-duplicate content across sections

**Example:**
```text
Before:
- Section A explains Validation Loop (400 lines)
- Section B explains Validation Loop with slight variation (380 lines)
- Section C references Validation Loop (200 lines)

After:
- Create reference/validation_loop_protocol.md (500 lines - comprehensive)
- Section A: "See validation_loop_protocol.md" (10 lines)
- Section B: "See validation_loop_protocol.md" (10 lines)
- Section C: "See validation_loop_protocol.md" (10 lines)
```

**Process:**
1. Identify duplicate or near-duplicate content
2. Create single authoritative reference
3. Replace duplicates with links
4. Ensure no information loss

**Validation:**
- [ ] Single authoritative source created
- [ ] All duplicates replaced with references
- [ ] No information lost in consolidation
- [ ] Cross-references all valid

### Strategy 4: Move Detailed Examples to Appendices

**When:** File has extensive examples that could be separated

**Example:**
```text
Before:
guide.md (900 lines)
  - Concept explanation (200 lines)
  - Example 1 (100 lines)
  - Example 2 (100 lines)
  - Example 3 (100 lines)
  - Example 4 (100 lines)
  - Example 5 (100 lines)
  - Additional content (200 lines)

After:
guide.md (500 lines)
  - Concept explanation (200 lines)
  - Brief example (50 lines)
  - Link to examples/guide_examples.md
  - Additional content (200 lines)

examples/guide_examples.md (500 lines)
  - Example 1-5 (all detailed examples)
```

**Process:**
1. Identify extensive example sets
2. Keep 1-2 brief examples in main guide
3. Move detailed examples to separate file
4. Link from main guide

**Validation:**
- [ ] Main guide retains sufficient examples for understanding
- [ ] Detailed examples accessible via clear link
- [ ] Examples file well-organized
- [ ] No critical examples lost

---

## CLAUDE.md Reduction Protocol

### Step 1: Analyze Current Size

```bash
wc -c CLAUDE.md
# Example output: 45786
# Overage: 5786 chars (14.5% over limit)
```

### Step 2: Section-by-Section Analysis

**Create analysis table:**

| Section | Character Count | Category | Extraction Candidate? |
|---------|----------------|----------|----------------------|
| Quick Start | 2,000 | Critical | ❌ KEEP |
| Phase Transition Protocol | 1,500 | Critical | ❌ KEEP |
| Stage Workflows Quick Reference | 12,000 | Reference | ✅ EXTRACT (reduce to 4,000) |
| Git Safety Rules | 2,000 | Critical | ❌ KEEP |
| Common Anti-Patterns | 3,000 | Examples | ✅ EXTRACT |
| S2 Parallel Work Details | 2,500 | Detailed | ✅ EXTRACT |
| ... | ... | ... | ... |

**Categories:**
- **Critical:** Must remain in CLAUDE.md (agent needs at every task start)
- **Reference:** Detailed content that can be linked from CLAUDE.md
- **Examples:** Detailed examples that can live in separate files
- **Detailed:** In-depth content that can be summarized with links

### Step 3: Extract Content

**For EACH extraction candidate:**

1. **Create target file** (if doesn't exist)
2. **Copy content** to target file
3. **Replace in CLAUDE.md** with short summary + link
4. **Verify link** is clear and accessible

**Example Extraction:**

```markdown
# Before (CLAUDE.md):
## Common Anti-Patterns to Avoid

### Anti-Pattern 1: Autonomous Checklist Resolution
[300 lines of detailed explanation with examples]

### Anti-Pattern 2: Narrow Investigation Scope
[250 lines of detailed explanation with examples]

### Anti-Pattern 3: Deferring Issues
[200 lines of detailed explanation with examples]

# After (CLAUDE.md):
## Common Anti-Patterns to Avoid

**Agents MUST avoid these critical anti-patterns:**
- Autonomous checklist resolution (agent marks RESOLVED without user approval)
- Narrow investigation scope (checking only obvious aspects)
- Deferring issues during Validation Loop (zero tolerance for "fix later")

**See:** `feature-updates/guides_v2/reference/common_mistakes.md` for complete anti-pattern reference with detailed examples and recovery protocols.

# Extracted (reference/common_mistakes.md):
# Common Anti-Patterns Reference

[Full 750 lines of detailed anti-pattern documentation]
```

### Step 4: Validate Reduction

**After extraction, verify:**

- [ ] `wc -c CLAUDE.md` ≤ 40,000 characters
- [ ] All critical content remains in CLAUDE.md
- [ ] All links to extracted content are valid
- [ ] Extracted files have clear purpose and navigation
- [ ] No information lost in extraction
- [ ] CLAUDE.md still provides effective quick reference

### Step 5: Test Agent Usability

**Before finalizing, verify:**
- [ ] Can agent quickly find critical rules?
- [ ] Are phase transition requirements clear?
- [ ] Do extracted sections feel accessible (not buried)?
- [ ] Would agent know where to look for detailed content?

---

## Workflow Guide Reduction Protocol

### Step 1: Analyze File Purpose

**Answer these questions:**

- **Is this a router file?** (Table of contents linking to sub-guides)
  - Expected size: <300 lines
  - If >300: Review navigation structure

- **Is this a comprehensive guide?** (Complete workflow for phase/iteration)
  - Expected size: 300-600 lines
  - If >600: Consider phase/iteration subdivision

- **Is this a reference file?** (Comprehensive reference material)
  - Expected size: 400-800 lines (acceptable for reference)
  - If >1000: Consider category subdivision

### Step 2: Identify Subdivision Strategy

**For guides >600 lines:**

**Option A: Split by Phase/Iteration**
```text
Before: s5_implementation_planning.md (1200 lines)
After:
  - s5_implementation_planning.md (200 lines router)
  - s5_p1_planning_round1.md (400 lines)
  - s5_p2_planning_round2.md (400 lines)
  - s5_p3_planning_round3.md (400 lines)
```

**Option B: Split by Concept**
```text
Before: validation_loop_guide.md (900 lines)
After:
  - validation_loop_protocol.md (300 lines - foundation)
  - validation_loop_discovery.md (200 lines - context-specific)
  - validation_loop_spec_refinement.md (200 lines)
  - validation_loop_qc_pr.md (200 lines)
```

**Option C: Extract Examples/Reference**
```text
Before: s2_feature_deep_dive.md (800 lines)
After:
  - s2_feature_deep_dive.md (500 lines - main workflow)
  - s2_examples.md (300 lines - detailed examples)
```

### Step 3: Execute Split

**For each subdivision:**

1. **Create new file** with descriptive name
2. **Move content** to new file
3. **Update original** (router or shortened guide)
4. **Update cross-references** in ALL guides
5. **Update file path references** in CLAUDE.md, README.md, etc.

### Step 4: Validate Split

**After split, verify:**

- [ ] Original file <600 lines (ideally <400 for router)
- [ ] Sub-files each <600 lines
- [ ] Clear navigation between files
- [ ] All cross-references updated
- [ ] No broken links
- [ ] Workflow continuity maintained
- [ ] Agent can easily navigate split structure

---

## Validation Checklist

### After ALL File Size Reductions

**CRITICAL - Must verify ALL before proceeding:**

### File Size Compliance
- [ ] `wc -c CLAUDE.md` ≤ 40,000 characters
- [ ] All workflow guides ≤ 1000 lines
- [ ] Preferably all guides ≤ 600 lines
- [ ] No files flagged as TOO LARGE by pre-audit script

### Content Integrity
- [ ] No information lost during reduction
- [ ] All critical content still accessible
- [ ] Workflow continuity maintained
- [ ] Agent can complete tasks without missing steps

### Cross-Reference Accuracy
- [ ] All links to extracted content valid
- [ ] All file path references updated
- [ ] CLAUDE.md references correct
- [ ] README.md references correct
- [ ] Template references correct

### Navigation Quality
- [ ] Router files provide clear navigation
- [ ] Links are descriptive (not just "see here")
- [ ] Extracted content easy to find
- [ ] No excessive navigation overhead

### Agent Usability
- [ ] Can agent quickly find critical rules? (test with CLAUDE.md)
- [ ] Is workflow clear despite split? (test with workflow guides)
- [ ] Are detailed examples accessible when needed?
- [ ] Would split structure help or hinder agent?

### Re-run Pre-Audit Script
```bash
bash feature-updates/guides_v2/audit/scripts/pre_audit_checks.sh
```

**Expected output:**
```text
✅ PASS: CLAUDE.md (39,500 chars) within 40,000 character limit
✅ All files within size limits
```

**If ANY failures:**
- [ ] Address issues immediately
- [ ] Re-run validation checklist
- [ ] Do NOT proceed to verification until ALL pass

---

## Common Issues and Solutions

### Issue 1: Reduction Creates Excessive Navigation

**Problem:** Split file into too many pieces, agent spends too much time navigating

**Solution:**
- Consolidate related sub-guides
- Use fewer, larger sub-guides (400-600 lines each)
- Create router with clear section descriptions
- Add "Next Steps" links at end of each sub-guide

### Issue 2: Unclear Where Extracted Content Lives

**Problem:** Agent can't find extracted detailed content

**Solution:**
- Use descriptive link text ("See Anti-Patterns Guide" not "See here")
- Add file path in link (`reference/anti_patterns.md`)
- Include brief summary before link (so agent knows what they'll find)
- Ensure extracted file has clear title matching link

### Issue 3: Lost Information During Extraction

**Problem:** Critical detail removed during reduction, agent misses requirement

**Solution:**
- Re-read original file section-by-section
- Compare extracted content to original (diff check)
- Verify all requirements captured in extracted file
- Test agent workflow using reduced file

### Issue 4: CLAUDE.md Still Too Large After Extraction

**Problem:** Extracted content but still exceeds 40,000 chars

**Solution:**
- Analyze remaining sections (create new analysis table)
- Identify additional extraction candidates
- Shorten quick reference sections (more concise)
- Move detailed examples to reference files
- Consolidate redundant content

---

## Exit Criteria

**Before proceeding to Stage 4 Verification:**

- [ ] ALL file size issues addressed (not deferred)
- [ ] CLAUDE.md ≤ 40,000 characters (HARD REQUIREMENT)
- [ ] All workflow guides ≤ 1000 lines (preferably ≤ 600)
- [ ] Validation checklist 100% complete
- [ ] Pre-audit script passes file size checks
- [ ] Cross-references verified (no broken links)
- [ ] Agent usability tested (can navigate split files)

**If ANY unchecked:**
- DO NOT proceed to verification
- Address remaining issues
- Re-run validation
- ONLY proceed when 100% complete

---

## Next Steps

**After completing file size reduction:**

1. **Document Changes:**
   - List all files modified
   - Note extraction targets
   - Record character/line counts before/after

2. **Proceed to Stage 4:**
   - Read `stages/stage_4_verification.md`
   - Verify ALL fixes (content + file size)
   - Check for new issues introduced by reduction

3. **If Issues Found During Verification:**
   - Return to this guide
   - Refine reduction approach
   - Re-validate
   - Restart verification

---

**Remember:** File size reduction is NOT optional. Large files create barriers for agents. Reducing file size is as critical as fixing content accuracy.

**User Directive:** "I want to ensure that agents have no barriers in their way toward completing their task."
