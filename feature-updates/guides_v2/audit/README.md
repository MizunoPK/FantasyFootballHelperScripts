# Audit Guide Router

**Version:** 3.0 (Modular)
**Purpose:** Navigate the audit process for ensuring guides_v2 consistency and accuracy
**Last Updated:** 2026-02-01

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
```

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

## Audit Process Overview

```
┌─────────────────────────────────────────────────────────────────┐
│         AUDIT LOOP (Repeat until ZERO new issues found)         │
│          MINIMUM 3 ROUNDS BASELINE (typically 3-5 rounds)        │
│        EXIT TRIGGER: Round N finds ZERO issues + 8 criteria      │
└─────────────────────────────────────────────────────────────────┘

Round 1: Initial Discovery
  ↓
Stage 1: Discovery (30-60 min)
  ↓
Stage 2: Fix Planning (15-30 min)
  ↓
Stage 3: Apply Fixes (30-90 min)
  ↓
Stage 4: Verification (30-45 min)
  ↓
Stage 5: Loop Decision (15-30 min)
  ↓
├─> EXIT (if all criteria met + user approves)
└─> LOOP BACK to Round 2 Discovery (with fresh eyes, new patterns)
```

---

## Navigation by Stage

| Stage | Guide | Duration | Primary Activities | Output |
|-------|-------|----------|-------------------|--------|
| **1. Discovery** | `stages/stage_1_discovery.md` | 30-60 min | Find issues using search patterns | Discovery report |
| **2. Fix Planning** | `stages/stage_2_fix_planning.md` | 15-30 min | Group issues, prioritize, **plan file size reductions** | Fix plan |
| **3. Apply Fixes** | `stages/stage_3_apply_fixes.md` | 30-90 min | Apply fixes incrementally, **reduce large files** | Fixed files |
| **4. Verification** | `stages/stage_4_verification.md` | 30-45 min | Re-run patterns, spot-check, **verify file sizes** | Verification report |
| **5. Loop Decision** | `stages/stage_5_loop_decision.md` | 15-30 min | Report results, decide continue/exit | Round summary |

**Critical Rule:** Complete stages sequentially. Never skip stages.

**File Size Integration:** File size reduction is integrated into Stages 2-4 as first-class fixes (not deferred). See `reference/file_size_reduction_guide.md` for methodology.

---

## Navigation by Audit Dimension

The audit evaluates guides across **16 critical dimensions**:

### Core Dimensions (Always Check)

| Dimension | Guide | Focus | Automation |
|-----------|-------|-------|------------|
| **D1: Cross-Reference Accuracy** | `dimensions/d1_cross_reference_accuracy.md` | File paths, links | 90% automated |
| **D2: Terminology Consistency** | `dimensions/d2_terminology_consistency.md` | Notation, naming | 80% automated |
| **D3: Workflow Integration** | `dimensions/d3_workflow_integration.md` ⏳ | Prerequisites, transitions | 40% automated |
| **D8: CLAUDE.md Sync** | `dimensions/d8_claude_md_sync.md` ⏳ | Root file synchronization | 60% automated |

### Content Quality Dimensions

| Dimension | Guide | Focus | Automation |
|-----------|-------|-------|------------|
| **D4: Count Accuracy** | `dimensions/d4_count_accuracy.md` ⏳ | File counts, iteration counts | 90% automated |
| **D5: Content Completeness** | `dimensions/d5_content_completeness.md` ⏳ | Missing sections, TODOs | 85% automated |
| **D6: Template Currency** | `dimensions/d6_template_currency.md` ⏳ | Template synchronization | 70% automated |
| **D13: Documentation Quality** | `dimensions/d13_documentation_quality.md` ⏳ | Required sections, examples | 90% automated |
| **D14: Content Accuracy** | `dimensions/d14_content_accuracy.md` ⏳ | Claims vs reality | 70% automated |

### Structural Dimensions

| Dimension | Guide | Focus | Automation |
|-----------|-------|-------|------------|
| **D9: Intra-File Consistency** | `dimensions/d9_intra_file_consistency.md` ⏳ | Within-file quality | 80% automated |
| **D10: File Size Assessment** | `dimensions/d10_file_size_assessment.md` ⏳ | Readability limits | 100% automated |
| **D11: Structural Patterns** | `dimensions/d11_structural_patterns.md` ⏳ | Template compliance | 60% automated |
| **D12: Cross-File Dependencies** | `dimensions/d12_cross_file_dependencies.md` ⏳ | Stage transitions | 30% automated |

### Advanced Dimensions

| Dimension | Guide | Focus | Automation |
|-----------|-------|-------|------------|
| **D7: Context-Sensitive Validation** | `dimensions/d7_context_sensitive_validation.md` ⏳ | Intentional exceptions | 20% automated |
| **D15: Duplication Detection** | `dimensions/d15_duplication_detection.md` ⏳ | DRY principle | 50% automated |
| **D16: Accessibility** | `dimensions/d16_accessibility_usability.md` ⏳ | Navigation, UX | 80% automated |

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
- **D5: Content Completeness** ⏳ - Finds missing sections that D1 cross-references pointed to
- **D13: Documentation Quality** ⏳ - Expands D5 with structure requirements

### Level 3: Structural (Optional, As Needed)
Deep-dive validations for specific issues:
- **D9: Intra-File Consistency** ⏳ - Within-file quality (use if files seem inconsistent)
- **D10: File Size Assessment** ⏳ - Readability limits (use if files seem too large)
- **D11: Structural Patterns** ⏳ - Template compliance (use after template changes)

### Level 4: Advanced (Rare, Specialized)
Only needed for specific scenarios:
- **D7: Context-Sensitive Validation** ⏳ - Distinguishing errors from intentional cases
- **D15: Duplication Detection** ⏳ - Finding duplicate content across guides

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
```

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
```

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
```

**Estimated Duration:** 1-2 hours (mostly automated)

---

## Reference Materials

### File Size Reduction Guide ✅ COMPLETE
`reference/file_size_reduction_guide.md` - Systematic approach to reducing large files
- File size thresholds (CLAUDE.md: 40,000 chars, guides: 1000 lines)
- Evaluation framework (when to split vs keep)
- Reduction strategies (extract sub-guides, reference files, consolidate, examples)
- CLAUDE.md reduction protocol
- Workflow guide reduction protocol
- Validation checklist
- **Used in Stage 2 (planning), Stage 3 (execution), Stage 4 (verification)**

### Pattern Library ⏳ COMING SOON
`reference/pattern_library.md` - Pre-built search patterns organized by category
- File path patterns
- Notation patterns
- Stage reference patterns
- Count verification patterns
- Template patterns

### Verification Commands ⏳ COMING SOON
`reference/verification_commands.md` - Command library with examples
- grep patterns
- sed commands
- Validation scripts
- Spot-check commands

### Context Analysis Guide ⏳ COMING SOON
`reference/context_analysis_guide.md` - How to determine if pattern match is error or intentional
- Decision trees
- Example analyses
- File-specific exception rules

### User Challenge Protocol ⏳ COMING SOON
`reference/user_challenge_protocol.md` - How to respond when user challenges findings
- "Are you sure?" response
- "Did you actually make fixes?" response
- "Assume everything is wrong" response

### Confidence Calibration ⏳ COMING SOON
`reference/confidence_calibration.md` - Scoring system for audit completeness
- Confidence score calculation
- Exit criteria thresholds
- Red flags indicating more work needed

### Issue Classification ⏳ COMING SOON
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

### Round Summary ⏳ COMING SOON
`templates/round_summary_template.md` - Stage 5 output format
- Round results summary
- Loop decision documentation
- Evidence for user review

---

## Real Examples ⏳ COMING SOON

Learn from actual audit rounds:

### KAI-7 Audit Examples
- `examples/audit_round_example_1.md` ⏳ - Round 1: Step number mapping issues (4 fixes)
- `examples/audit_round_example_2.md` ⏳ - Round 2: Router links and path formats (10 fixes)
- `examples/audit_round_example_3.md` ⏳ - Round 3: Notation standardization (70+ fixes)
- `examples/audit_round_example_4.md` ⏳ - Round 4: Cross-reference validation (20+ fixes)

**Total Issues Fixed:** 104+ instances across 4 rounds, 50+ files modified

---

## Automated Scripts

### Pre-Audit Checks
`scripts/pre_audit_checks.sh` - Run before manual audit begins
- Checks 6 of 16 dimensions (D1, D8, D10, D11, D13, D14, D16)
- Catches common structural issues (estimated 40-50% of typical issues)
- Fast execution (5 minutes)
- Generates initial report
- **NOT checked:** D2 Terminology (most common - requires manual pattern search)

### Individual Check Scripts ⏳ COMING SOON
**Note:** All checks currently integrated into `pre_audit_checks.sh`
- `scripts/check_file_sizes.sh` ⏳ - File size and complexity assessment (D10)
- `scripts/validate_structure.sh` ⏳ - Structural pattern validation (D11)
- `scripts/check_completeness.sh` ⏳ - Documentation quality checks (D13)
- `scripts/verify_counts.sh` ⏳ - Content accuracy validation (D14)
- `scripts/check_navigation.sh` ⏳ - Accessibility checks (D16)
- `scripts/find_duplicates.sh` ⏳ - Duplication detection (D15)
- `scripts/validate_dependencies.sh` ⏳ - Cross-file dependency checks (D12)

---

## Critical Success Factors

### Minimum Requirements for Audit Completion

**ALL 8 exit criteria must be met:**
1. ✅ Minimum 3 rounds | 2. ✅ Zero new discoveries | 3. ✅ Zero verification findings
4. ✅ All documented | 5. ✅ User approved | 6. ✅ Confidence ≥80%
7. ✅ Pattern diversity | 8. ✅ Spot-checks clean

**See `stages/stage_5_loop_decision.md` for detailed criteria with sub-requirements.**

**IF USER CHALLENGES YOU:**
- Immediately loop back to Round 1
- User challenge = evidence you missed something
- Do NOT defend - user is usually right
- Re-verify EVERYTHING with fresh patterns

---

## Philosophy

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
