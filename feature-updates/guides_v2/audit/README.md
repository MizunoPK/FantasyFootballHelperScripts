# Audit Guide Router

**Version:** 3.0 (Modular)
**Purpose:** Navigate the audit process for ensuring guides_v2 consistency and accuracy
**Last Updated:** 2026-02-06

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Audit Process Overview](#audit-process-overview-sub-round-system)
3. [Audit Files Structure](#audit-files-structure)
4. [Dimension Categories](#dimension-categories)
5. [Stage Workflow Guides](#stage-workflow-guides)
6. [Dimension Guides](#dimension-guides)
7. [Reference Materials](#reference-materials)
8. [Templates](#templates)
9. [Scripts](#scripts)
10. [Outputs](#outputs)

---

## Quick Start

### New Audit?

**STEP 1:** Read `audit_overview.md` (10-15 minutes)
- Understand when to run audits
- Learn the audit philosophy
- Review exit criteria

**STEP 2:** Run automated pre-checks (5 minutes)
```bash
cd feature-updates/guides_v2/audit
bash scripts/pre_audit_checks.sh
```diff

**STEP 3:** Start Round 1 Discovery
- Read `stages/stage_1_discovery.md`
- Use `dimensions/` guides as needed
- Create discovery report using `templates/discovery_report_template.md`

### Resuming Audit?

**Check your current stage:**
- Stage 1: Discovery → Read `stages/stage_1_discovery.md`
- Stage 2: Fix Planning → Read `stages/stage_2_fix_planning.md`
- Stage 3: Apply Fixes → Read `stages/stage_3_apply_fixes.md`
- Stage 4: Verification → Read `stages/stage_4_verification.md`
- Stage 5: Loop Decision → Read `stages/stage_5_loop_decision.md`

**Continue from where you left off.**

---

## Audit Process Overview (Sub-Round System)

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
  │   S1: Discovery → S2: Planning → S3: Apply → S4: Verify → S5: Loop Decision
  │   If 0 issues → Sub-Round N.2 | If issues → Fix & Re-run N.1
  │
  ├─> Sub-Round N.2: Content Quality (D4, D5, D6, D13, D14)
  │   S1: Discovery → S2: Planning → S3: Apply → S4: Verify → S5: Loop Decision
  │   If 0 issues → Sub-Round N.3 | If issues → Fix & Re-run N.2
  │
  ├─> Sub-Round N.3: Structural (D9, D10, D11, D12)
  │   S1: Discovery → S2: Planning → S3: Apply → S4: Verify → S5: Loop Decision
  │   If 0 issues → Sub-Round N.4 | If issues → Fix & Re-run N.3
  │
  └─> Sub-Round N.4: Advanced (D7, D15, D16, D17)
      S1: Discovery → S2: Planning → S3: Apply → S4: Verify → S5: Loop Decision
      If 0 issues → Round N complete | If issues → Fix & Re-run N.4

Round N complete → Round N+1 (fresh eyes) → EXIT when all criteria met
```

### Sub-Round Benefits

1. **Dependency Management:** Core fixes (broken references) applied before Structural checks
2. **Focused Discovery:** Check 4-5 related dimensions per sub-round, not all 17 at once
3. **Incremental Verification:** Verify fixes before moving to next category
4. **Mental Clarity:** Fresh mental model between dimension categories
5. **Complete Coverage:** ALL 17 dimensions checked systematically every round
6. **No Blind Spots:** Can't skip dimensions accidentally

---

## Navigation by Stage

| Stage | Guide | Duration | Primary Activities | Output |
|-------|-------|----------|-------------------|--------|
| **1. Discovery** | `stages/stage_1_discovery.md` | 30-60 min | Find issues using search patterns | Discovery report |
| **2. Fix Planning** | `stages/stage_2_fix_planning.md` | 30-90 min | Group issues, **investigate complex issues**, ask user if uncertain | Fix plan + user questions |
| **3. Apply Fixes** | `stages/stage_3_apply_fixes.md` | 60-180 min | Apply ALL fixes (content + file size), **no deferrals** | Fixed files |
| **4. Verification** | `stages/stage_4_verification.md` | 30-45 min | Re-run patterns, spot-check, verify ALL fixes | Verification report |
| **5. Loop Decision** | `stages/stage_5_loop_decision.md` | 15-30 min | Report results, decide continue/exit | Round summary |

**Critical Rules:**
- Complete stages sequentially. Never skip stages.
- **NO DEFERRALS ALLOWED** - Investigate or ask user, never defer to later rounds
- File size reduction is first-class work (not deferred). See `reference/file_size_reduction_guide.md`
- Duration estimates include investigation time - deep dives are EXPECTED

---

## Sub-Round Structure

**Each round consists of 4 sub-rounds organized by dimension category:**

| Sub-Round | Dimensions | Count | Focus | Duration |
|-----------|------------|-------|-------|----------|
| **N.1: Core** | D1, D2, D3, D8 | 4 | File paths, terminology, workflow, CLAUDE.md | 60-90 min |
| **N.2: Content** | D4, D5, D6, D13, D14 | 5 | Counts, completeness, templates, documentation | 75-120 min |
| **N.3: Structural** | D9, D10, D11, D12 | 4 | File consistency, size, patterns, dependencies | 60-90 min |
| **N.4: Advanced** | D7, D15, D16, D17 | 4 | Context-sensitive, duplication, accessibility, flow | 60-90 min |
| **TOTAL** | All 17 dimensions | 17 | Complete coverage | 4.5-6.5 hours |

**Execution Order:**
1. **Core first** - Fixes broken references and inconsistent notation that affect all other checks
2. **Content second** - Content fixes may reveal structural issues
3. **Structural third** - Structure depends on correct content and references
4. **Advanced last** - Advanced checks require all other dimensions to be clean

**Loop Logic:**
- Sub-round finds issues → Fix ALL → Re-run SAME sub-round → Repeat until 0 issues
- Sub-round clean → Proceed to next sub-round
- All 4 sub-rounds clean → Round complete → Next round (fresh eyes)
- Minimum 3 rounds (12 sub-rounds) + all clean → Consider exit

---

## Navigation by Audit Dimension

The audit evaluates guides across **17 critical dimensions**:

### Core Dimensions (Always Check)

| Dimension | Guide | Focus | Automation |
|-----------|-------|-------|------------|
| **D1: Cross-Reference Accuracy** | `dimensions/d1_cross_reference_accuracy.md` | File paths, links | 90% automated |
| **D2: Terminology Consistency** | `dimensions/d2_terminology_consistency.md` | Notation, naming | 80% automated |
| **D3: Workflow Integration** | `dimensions/d3_workflow_integration.md` | Prerequisites, transitions | 40% automated |
| **D8: CLAUDE.md Sync** | `dimensions/d8_claude_md_sync.md` | Root file synchronization | 60% automated |

### Content Quality Dimensions

| Dimension | Guide | Focus | Automation |
|-----------|-------|-------|------------|
| **D4: Count Accuracy** | `dimensions/d4_count_accuracy.md` | File counts, iteration counts | 90% automated |
| **D5: Content Completeness** | `dimensions/d5_content_completeness.md` | Missing sections, TODOs | 85% automated |
| **D6: Template Currency** | `dimensions/d6_template_currency.md` | Template synchronization | 70% automated |
| **D13: Documentation Quality** | `dimensions/d13_documentation_quality.md` | Required sections, examples | 90% automated |
| **D14: Content Accuracy** | `dimensions/d14_content_accuracy.md` | Claims vs reality | 70% automated |

### Structural Dimensions

| Dimension | Guide | Focus | Automation |
|-----------|-------|-------|------------|
| **D9: Intra-File Consistency** | `dimensions/d9_intra_file_consistency.md` | Within-file quality | 80% automated |
| **D10: File Size Assessment** | `dimensions/d10_file_size_assessment.md` | Readability limits | 100% automated |
| **D11: Structural Patterns** | `dimensions/d11_structural_patterns.md` | Template compliance | 60% automated |
| **D12: Cross-File Dependencies** | `dimensions/d12_cross_file_dependencies.md` | Stage transitions | 30% automated |

### Advanced Dimensions

| Dimension | Guide | Focus | Automation |
|-----------|-------|-------|------------|
| **D7: Context-Sensitive Validation** | `dimensions/d7_context_sensitive_validation.md` | Intentional exceptions | 20% automated |
| **D15: Duplication Detection** | `dimensions/d15_duplication_detection.md` | DRY principle | 50% automated |
| **D16: Accessibility** | `dimensions/d16_accessibility_usability.md` | Navigation, UX | 80% automated |
| **D17: Stage Flow Consistency** | `dimensions/d17_stage_flow_consistency.md` | Cross-stage behavior | 30% automated |

**Usage:** Read dimension guides as needed during discovery. Not all dimensions apply to every audit.

---

## Recommended Dimension Reading Order

**Avoid circular dependencies - start with foundational dimensions, then build up.**

### Level 1: Foundational (Start Here)
Read these first - they're most common and easiest to validate:
- **D1: Cross-Reference Accuracy** - File paths, links (90% automated)
- **D2: Terminology Consistency** - Notation, naming (80% automated)

**Why start here:** Most audit issues fall into D1-D2. High automation = quick wins.

### Level 2: Content Quality (After Level 1)
Build on D1-D2 findings:
- **D5: Content Completeness** - Finds missing sections that D1 cross-references pointed to
- **D13: Documentation Quality** - Expands D5 with structure requirements

### Level 3: Structural (Optional, As Needed)
Deep-dive validations for specific issues:
- **D9: Intra-File Consistency** - Within-file quality (use if files seem inconsistent)
- **D10: File Size Assessment** - Readability limits (use if files seem too large)
- **D11: Structural Patterns** - Template compliance (use after template changes)

### Level 4: Advanced (Rare, Specialized)
Only needed for specific scenarios:
- **D7: Context-Sensitive Validation** - Distinguishing errors from intentional cases
- **D15: Duplication Detection** - Finding duplicate content across guides

**Note:** You don't need to read ALL dimension guides for every audit. Read what's relevant to your trigger event (see Common Scenarios below).

---

## Common Scenarios

### Scenario 1: After S10.P1 Guide Updates

**Trigger:** Just completed lessons learned integration (S10.P1)

**High-Risk Dimensions:**
1. D1: Cross-Reference Accuracy (guide changes may break links)
2. D2: Terminology Consistency (new terminology may be inconsistent)
3. D6: Template Currency (templates may not reflect guide changes)
4. D8: CLAUDE.md Sync (quick reference may be outdated)

**Recommended Approach:**
```bash
# Run pre-checks
bash scripts/pre_audit_checks.sh

# Start Round 1 focusing on high-risk dimensions
# Read stages/stage_1_discovery.md
# Then read d1, d2, d6, d8 dimension guides
```markdown

**Estimated Duration:** 3-4 hours (3-4 rounds)

---

### Scenario 2: After Stage Renumbering

**Trigger:** Major restructuring (e.g., S5 split into S5-S8, S6→S9, S7→S10)

**High-Risk Dimensions:**
1. D1: Cross-Reference Accuracy (old stage numbers in references)
2. D3: Workflow Integration (prerequisite chains broken)
3. D6: Template Currency (templates have old stage numbers)
4. D8: CLAUDE.md Sync (quick reference outdated)
5. D12: Cross-File Dependencies (stage transitions broken)

**Recommended Approach:**
```bash
# Run pre-checks
bash scripts/pre_audit_checks.sh

# Start Round 1 with comprehensive search
# Focus on old stage number patterns
# Read all 5 high-risk dimension guides
```

**Estimated Duration:** 4-6 hours (3-4 rounds minimum)

---

### Scenario 3: After Terminology Changes

**Trigger:** Notation updates (e.g., "Stage 5a" → "S5.P1")

**High-Risk Dimensions:**
1. D2: Terminology Consistency (old notation stragglers)
2. D6: Template Currency (templates use old notation)
3. D7: Context-Sensitive Validation (intentional old notation in examples)
4. D9: Intra-File Consistency (mixed notation within files)

**Recommended Approach:**
```bash
# Run pre-checks
bash scripts/pre_audit_checks.sh

# Generate pattern variations of old notation
# Read dimensions/d2_terminology_consistency.md for pattern strategies
# Manual review for context-sensitive cases
```markdown

**Estimated Duration:** 3-5 hours (3-4 rounds)

---

### Scenario 4: User Reports Inconsistency

**Trigger:** User found error or reports confusion

**Recommended Approach:**
1. **Spot-Audit:** Check the specific file and related files
2. **Assess Scope:** Is this isolated or widespread?
3. **If Isolated:** Fix and verify immediately
4. **If Widespread:** Run full audit focusing on related dimension

```bash
# Example: User reports broken link in S5 guide
# Step 1: Fix the specific issue
# Step 2: Run cross-reference validation on all S5 files
grep -rn "stages/s5" stages/s5/*.md | grep "\.md"

# Step 3: If many broken links, run full D1 audit
# Read dimensions/d1_cross_reference_accuracy.md
```

---

### Scenario 5: Quarterly Maintenance

**Trigger:** Routine quality check (no specific changes)

**Recommended Approach:**
```bash
# Run automated checks
bash scripts/pre_audit_checks.sh

# If clean: No manual audit needed
# If issues found: Run focused audit on failing dimensions
```diff

**Estimated Duration:** 1-2 hours (mostly automated)

---

## Reference Materials

### File Size Reduction Guide ✅ COMPLETE
`reference/file_size_reduction_guide.md` - Systematic approach to reducing large files
- File size thresholds (CLAUDE.md: 40,000 chars, guides: 1250 lines)
- Evaluation framework (when to split vs keep)
- Reduction strategies (extract sub-guides, reference files, consolidate, examples)
- CLAUDE.md reduction protocol
- Workflow guide reduction protocol
- Validation checklist
- **Used in Stage 2 (planning), Stage 3 (execution), Stage 4 (verification)**

### Pattern Library ✅ COMPLETE
`reference/pattern_library.md` - Pre-built search patterns organized by category
- File path patterns
- Notation patterns
- Stage reference patterns
- Count verification patterns
- Template patterns

### Verification Commands ✅ COMPLETE
`reference/verification_commands.md` - Command library with examples
- grep patterns
- sed commands
- Validation scripts
- Spot-check commands

### Context Analysis Guide ✅ COMPLETE
`reference/context_analysis_guide.md` - How to determine if pattern match is error or intentional
- Decision trees
- Example analyses
- File-specific exception rules

### User Challenge Protocol ✅ COMPLETE
`reference/user_challenge_protocol.md` - How to respond when user challenges findings
- "Are you sure?" response
- "Did you actually make fixes?" response
- "Assume everything is wrong" response

### Confidence Calibration ✅ COMPLETE
`reference/confidence_calibration.md` - Scoring system for audit completeness
- Confidence score calculation
- Exit criteria thresholds
- Red flags indicating more work needed

### Issue Classification ✅ COMPLETE
`reference/issue_classification.md` - Severity levels and prioritization
- Critical: Breaks workflow
- High: Causes confusion
- Medium: Cosmetic but important
- Low: Nice-to-have

---

## Templates

### Discovery Report
`templates/discovery_report_template.md` - Stage 1 output format
- Issue documentation structure
- Categorization by dimension
- Severity assignment

### Fix Plan
`templates/fix_plan_template.md` - Stage 2 output format
- Grouping strategy
- Priority order
- Sed commands

### Verification Report
`templates/verification_report_template.md` - Stage 4 output format
- Before/after evidence
- Count tracking (N_found, N_fixed, N_remaining, N_new)
- Spot-check results

### Round Summary
`templates/round_summary_template.md` - Stage 5 output format
- Round results summary
- Loop decision documentation
- Evidence for user review

---

## Real Examples ✅ COMPLETE

Learn from actual audit rounds:

### KAI-7 Audit Examples
- `examples/audit_round_example_1.md` ✅ - Round 1: Step number mapping issues (4 fixes)
- `examples/audit_round_example_2.md` ✅ - Round 2: Router links and path formats (10 fixes)
- `examples/audit_round_example_3.md` ✅ - Round 3: Notation standardization (70+ fixes)
- `examples/audit_round_example_4.md` ✅ - Round 4: Cross-reference validation (20+ fixes)

**Total Issues Fixed:** 104+ instances across 4 rounds, 50+ files modified

---

## Automated Scripts

### Pre-Audit Checks
`scripts/pre_audit_checks.sh` - Run before manual audit begins
- Checks 10 of 17 dimensions (D1, D3, D8, D9, D10, D11, D13, D14, D16, D17)
- Catches common structural issues (estimated 45-55% of typical issues)
- Fast execution (5 minutes)
- Generates initial report
- **NOT checked:** D2 Terminology (most common - requires manual pattern search)

### Individual Check Scripts
**Design Decision:** Checks are intentionally **consolidated** into `pre_audit_checks.sh` rather than separate scripts.

**Rationale:**
- Single command runs all automated checks
- Unified output format and error handling
- Easier maintenance (one file vs 7)
- Better performance (~5 minutes total)
- Most audits run all checks anyway (not selective)

**What would have been separate scripts:**
- `check_file_sizes.sh` - D10: File size and complexity assessment
- `validate_structure.sh` - D11: Structural pattern validation
- `check_completeness.sh` - D13: Documentation quality checks
- `verify_counts.sh` - D14: Content accuracy validation
- `check_navigation.sh` - D16: Accessibility checks
- `find_duplicates.sh` - D15: Duplication detection
- `validate_dependencies.sh` - D12: Cross-file dependency checks

**All functionality available in:** `scripts/pre_audit_checks.sh` (12KB, 7 dimensions)

---

## Critical Success Factors

### Minimum Requirements for Audit Completion

**ALL 9 exit criteria must be met:**
1. ✅ All issues resolved | 2. ✅ Zero new discoveries | 3. ✅ Zero verification findings
4. ✅ Minimum 3 rounds | 5. ✅ All documented | 6. ✅ User approved
7. ✅ Confidence ≥80% | 8. ✅ Pattern diversity | 9. ✅ Spot-checks clean

**See `stages/stage_5_loop_decision.md` for detailed criteria with sub-requirements.**

**IF USER CHALLENGES YOU:**
- Immediately loop back to Round 1
- User challenge = evidence you missed something
- Do NOT defend - user is usually right
- Re-verify EVERYTHING with fresh patterns

---

## Philosophy

**🚨 ZERO TOLERANCE FOR DEFERRALS - CRITICAL POLICY**

**ALL identified issues MUST be investigated and addressed immediately.**

- **NO deferring to "later rounds" or "post-audit"**
- **Deep dives into files are ENCOURAGED** - Read files, analyze context, determine fixes
- **If uncertain after investigation, ASK THE USER** - Don't defer, get clarity
- **Audit purpose:** Achieve OPTIMAL state, not just quick wins

**Decision Framework:**
```text
Issue discovered → Can I fix with confidence?
  ├─ YES → Fix immediately
  └─ NO  → Read files, investigate (15-30 min)
            ├─ NOW confident? → Fix immediately
            └─ Still uncertain? → ASK USER (provide analysis + options)
```

**Fresh Eyes, Zero Assumptions, User Skepticism is Healthy**

- Approach each round as if you've never seen the codebase
- Question everything, verify everything, assume you missed something
- Use iterative loops until zero new issues found (minimum 3 rounds as baseline, typically 3-5)
- Provide evidence, not just claims
- When user challenges you, THEY ARE USUALLY RIGHT - re-verify immediately

**Historical Evidence:**
- Session 2-3 audits: 221+ fixes across 110 files
- Premature completion claims: 3 times (each time, 50+ more issues found)
- User challenges: 3 ("are you sure?", "did you actually make fixes?", "assume everything is wrong")
- Rounds required: 3+ to reach zero new issues
- **Historical deferral failure:** Round 1-2 deferred 137 issues (67% deferral rate) - ALL should have been investigated and addressed

---

## Getting Help

**If stuck or uncertain:**
1. Read `audit_overview.md` for philosophy and principles
2. Check relevant dimension guide for specific checks
3. Review `examples/` for similar situations
4. Use `reference/user_challenge_protocol.md` if user challenges findings
5. Remember: Better to over-audit than under-audit

**Key Principle:** If you're unsure whether to continue auditing, continue auditing.

---

**Next Step:** Read `audit_overview.md` to understand audit philosophy and triggers.
