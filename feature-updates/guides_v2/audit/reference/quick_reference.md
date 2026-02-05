# Audit Quick Reference

**Purpose:** One-page cheat sheet for common audit tasks and quick lookups
**Best For:** When you know what you need, just need the command or checklist
**Reading Time:** 2-3 minutes

---

## "I Need To..." Decision Tree

**I need to START a new audit →** `README.md` → Run `bash scripts/pre_audit_checks.sh` → `stage_1_discovery.md`

**I need to RESUME an audit →** `README.md` → "Resuming Audit?" section → Jump to current stage

**I need to find BROKEN LINKS →** `dimensions/d1_cross_reference_accuracy.md` → Pattern Type 1

**I need to find NOTATION INCONSISTENCIES →** `dimensions/d2_terminology_consistency.md` → Pattern Types 1-4

**I need to FIX issues I found →** `stage_2_fix_planning.md` → Group issues → `stage_3_apply_fixes.md`

**I need to VERIFY fixes worked →** `stage_4_verification.md` → Three-tier verification

**I need to DECIDE if audit is complete →** `stage_5_loop_decision.md` → Check all 9 exit criteria

**I need to understand FRESH EYES →** `audit_overview.md` → "How to Achieve Fresh Eyes" → TL;DR box

**I need to know WHEN to audit →** `audit_overview.md` → "When to Run Audits" section

**I need to check ROOT FILE sync →** `dimensions/d8_claude_md_sync.md` → Automated + manual checks

**I need PRE-BUILT PATTERNS →** See "Common Search Patterns" below (or `reference/pattern_library.md` ⏳ when created)

**I need to report RESULTS →** Use templates:
- Stage 1 output: `templates/discovery_report_template.md`
- Stage 2 output: `templates/fix_plan_template.md`
- Stage 4 output: `templates/verification_report_template.md`
- Stage 5 output: `templates/round_summary_template.md`

---

## Common Search Patterns

### Cross-Reference Patterns (D1)

```bash
# Find all file path references
grep -rn "stages/s[0-9].*\.md" --include="*.md"
grep -rn "templates/.*\.md" --include="*.md"
grep -rn "reference/.*\.md" --include="*.md"

# Find broken markdown links
grep -rn "\[.*\](.*\.md)" --include="*.md" | grep -o "(.*\.md)" | \
  sed 's/[()]//g' | while read path; do [ ! -f "$path" ] && echo "BROKEN: $path"; done

# Find stage references (S1-S10)
grep -rn "\bS[0-9][0-9]*\b" --include="*.md"
```

---

### Notation Patterns (D2)

```bash
# Old notation patterns (pre-standardization)
grep -rn "\bS[0-9][a-z]\b" --include="*.md"        # S5a, S6b
grep -rn "Stage [0-9][a-z]" --include="*.md"       # Stage 5a
grep -rn "Phase [0-9]" --include="*.md"            # Phase 1 (should be P1)

# Formatting issues
grep -rn "S[0-9][A-Z][0-9]" --include="*.md"       # S5P1 (missing dot)
grep -rn "S[0-9]-[A-Z]" --include="*.md"           # S5-P1 (wrong separator)
grep -rn "s[0-9]\.p[0-9]" --include="*.md"         # s5.p1 (lowercase, should be uppercase)

# Current notation validation
grep -rn "S[0-9]\.P[0-9]\.I[0-9]" --include="*.md" # S5.P1.I2 (correct format)
```

---

### Count Patterns (D4)

```bash
# Find explicit counts that may be outdated
grep -rn "[0-9]+ files\|[0-9]+ stages\|[0-9]+ rounds" --include="*.md"
grep -rn "[0-9]+ iterations\|[0-9]+ phases" --include="*.md"

# Find list items for manual count verification
grep -rn "^[0-9]\. " --include="*.md"              # Numbered lists
grep -rn "^- " --include="*.md"                    # Bullet lists
```

---

### File Size Check (D10)

```bash
# Find files over 1000 lines (potential readability issues)
for file in $(find stages -name "*.md"); do
  lines=$(wc -l < "$file")
  [ "$lines" -gt 1000 ] && echo "$file: $lines lines"
done

# Estimate tokens (rough: lines * 13)
for file in $(find . -name "*.md"); do
  lines=$(wc -l < "$file")
  tokens=$((lines * 13))
  [ "$tokens" -gt 10000 ] && echo "$file: ~$tokens tokens (exceeds 10K limit)"
done
```

---

### CLAUDE.md Sync Check (D8)

```bash
# Extract paths from CLAUDE.md
grep -oh "feature-updates/guides_v2/[^)\"' ]*\.md" CLAUDE.md | sort -u

# Verify each path exists
grep -oh "feature-updates/guides_v2/[^)\"' ]*\.md" CLAUDE.md | \
  while read path; do [ ! -f "$path" ] && echo "BROKEN: $path"; done

# Find stage references in CLAUDE.md
grep -n "S[0-9]" CLAUDE.md | grep -o "S[0-9][0-9]*\(\.P[0-9][0-9]*\)\?\(\.I[0-9][0-9]*\)\?"
```

---

## Exit Criteria Quick Checklist

**ALL 9 must pass to exit audit:**

- [ ] **Criterion 1:** Minimum 3 rounds completed with fresh eyes
- [ ] **Criterion 2:** Stage 1 found ZERO new issues this round
- [ ] **Criterion 3:** Stage 4 verification N_new = 0
- [ ] **Criterion 4:** All N_remaining documented as intentional
- [ ] **Criterion 5:** User has NOT challenged results
- [ ] **Criterion 6:** Confidence ≥ 80%
- [ ] **Criterion 7:** Pattern diversity ≥ 5 types used
- [ ] **Criterion 8:** Spot-checks (10+ files) found 0 issues

**If ANY checkbox is unchecked → LOOP to Round N+1**

**See:** `stages/stage_5_loop_decision.md` for detailed sub-requirements

---

## Fresh Eyes Quick Checklist

**5-Step Fresh Eyes Protocol:**

- [ ] **Clear context:** Close all Round N-1 files, take 5-10 min break
- [ ] **Different patterns:** Use NEW search patterns (not same grep from Round N-1)
- [ ] **Different order:** Search folders in DIFFERENT order than Round N-1
- [ ] **Don't peek:** Don't look at Round N-1 discoveries until AFTER Round N discovery
- [ ] **Self-check:** Am I skipping folders? → ❌ NOT fresh, check anyway

**Common Failure:** Re-running same patterns from Round N-1 → Finds nothing new

**See:** `audit_overview.md` → "How to Achieve Fresh Eyes" for detailed operational guide

---

## Stage Selection Guide

**Quick lookup: Which stage do I need?**

| Stage | When to Use | Duration |
|-------|-------------|----------|
| **Stage 1: Discovery** | Find issues using search patterns | 30-60 min |
| **Stage 2: Fix Planning** | Organize discovered issues into groups | 15-30 min |
| **Stage 3: Apply Fixes** | Execute fix plan incrementally | 30-90 min |
| **Stage 4: Verification** | Verify all fixes + find missed variations | 30-45 min |
| **Stage 5: Loop Decision** | Decide EXIT or LOOP based on 9 criteria | 15-30 min |

**Flow:** Always complete stages sequentially (1 → 2 → 3 → 4 → 5)

**After Stage 5:**
- All criteria pass → EXIT audit
- Any criteria fail → LOOP back to Stage 1 (Round N+1)

---

## Dimension Selection Guide

**Quick lookup: Which dimension applies to my issue?**

| Dimension | Focus | Automation | Use When |
|-----------|-------|------------|----------|
| **D1: Cross-Reference** | File paths, links, stage refs | 90% | After renumbering, restructuring |
| **D2: Terminology** | Notation, naming conventions | 80% | After notation changes |
| **D3: Workflow** ⏳ | Prerequisites, transitions | 40% | After workflow changes |
| **D4: Count Accuracy** ⏳ | File counts, list counts | 90% | After adding/removing files |
| **D5: Completeness** ⏳ | Missing sections, TODOs | 85% | After major updates |
| **D6: Template Currency** ⏳ | Template synchronization | 70% | After template changes |
| **D7: Context-Sensitive** ⏳ | Intentional exceptions | 20% | Advanced: distinguishing errors |
| **D8: CLAUDE.md Sync** | Root file synchronization | 60% | After S10.P1 guide updates |
| **D9: Intra-File** ⏳ | Within-file consistency | 80% | File seems internally inconsistent |
| **D10: File Size** ⏳ | Readability limits | 100% | Files seem too large |
| **D11: Structural** ⏳ | Template compliance | 60% | After structural changes |
| **D12: Dependencies** ⏳ | Cross-file dependencies | 30% | After major refactors |
| **D13: Quality** ⏳ | Required sections, examples | 90% | General quality check |
| **D14: Accuracy** ⏳ | Claims vs reality | 70% | Content seems wrong |
| **D15: Duplication** ⏳ | DRY principle | 50% | Suspected duplicate content |
| **D16: Accessibility** ⏳ | Navigation, UX | 80% | Usability concerns |

**Recommended:** Start with D1-D2 (most common issues, highest automation)

---

## Verification Commands Quick Reference

### Re-Run Pattern (Tier 1)

```bash
# After fixing issue, re-run original pattern
grep -rn "OLD_PATTERN" --include="*.md"
# Expected: 0 matches (or only intentional cases)

grep -rn "NEW_PATTERN" --include="*.md"
# Expected: N matches (same as N_fixed)
```

---

### Try Variations (Tier 2)

```bash
# If fixed "S5a" → "S5.P1", try variations
grep -rn "S5 a\|S5-a\|S5_a" --include="*.md"  # Space, dash, underscore variations
grep -rn "stage 5a\|Stage 5a" --include="*.md" # Lowercase variations
```

---

### Spot-Check Files (Tier 3)

```bash
# Random file selection
ls stages/**/*.md | shuf -n 10  # 10 random files

# Visual inspection
sed -n '100,150p' path/to/file.md  # Read lines 100-150
```

---

## Critical Counts Tracker

**Track these 4 numbers through verification:**

| Count | Meaning | Target |
|-------|---------|--------|
| **N_found** | Issues from Stage 1 Discovery | Any |
| **N_fixed** | Issues fixed in Stage 3 | = N_found |
| **N_remaining** | Still found after fixes | 0 or intentional |
| **N_new** | NEW issues in Stage 4 verification | **0** (MUST) |

**Decision Logic:**
- N_new > 0 → LOOP to Round N+1 (missed something)
- N_remaining > 0 AND not intentional → Loop to Stage 3 (incomplete fixes)
- N_new = 0 AND N_remaining acceptable → Continue to Stage 5

---

## Common Sed Commands

### Replace Pattern

```bash
# Basic replacement
sed -i 's|OLD|NEW|g' file1.md file2.md

# With regex
sed -i 's|S[0-9]a|S5.P1|g' *.md

# Case-insensitive
sed -i 's|pattern|replacement|gi' file.md
```

---

### Verify Before Applying

```bash
# Preview changes (without -i)
sed 's|OLD|NEW|g' file.md | grep "NEW"

# Count replacements
sed -n 's|OLD|NEW|gp' file.md | wc -l
```

---

### Multi-File Safety Pattern

```bash
# 1. Test on one file first
sed -i 's|OLD|NEW|g' test_file.md
grep -n "NEW" test_file.md  # Verify correct
grep -n "OLD" test_file.md  # Should be empty

# 2. Apply to all if test passed
sed -i 's|OLD|NEW|g' file1.md file2.md file3.md

# 3. Verify each file
for file in file1.md file2.md file3.md; do
  echo "=== $file ==="
  grep -n "NEW" "$file"
done
```

---

## Confidence Calibration Quick Guide

**Self-assess confidence using this scale:**

### 90-100%: Very High Confidence
- ✅ 5+ rounds completed
- ✅ 0 new issues in last 2 rounds
- ✅ 10+ pattern types used
- ✅ All folders checked systematically
- ✅ 20+ files spot-checked
- ✅ Zero nagging doubts

### 80-89%: High Confidence (Exit Threshold)
- ✅ 3-4 rounds completed
- ✅ 0 new issues this round
- ✅ 5+ pattern types used
- ✅ All folders checked
- ✅ 10+ files spot-checked
- ⚠️ Minor doubts but investigated

### 60-79%: Medium Confidence
- ⚠️ 2-3 rounds completed
- ⚠️ Found issues this round but N_new = 0
- ⚠️ 3-4 pattern types used
- ⚠️ Most folders checked
- ⚠️ Some areas skipped

**→ Continue to Round N+1**

### < 60%: Low Confidence
- ❌ < 2 rounds completed
- ❌ Significant areas not checked
- ❌ Limited pattern diversity
- ❌ Nagging doubts

**→ Continue to Round N+1, expand search**

---

## File Size Limits

**Target:** All files < 10,000 tokens for tool readability

**Rough Conversion:**
- 1 line ≈ 13 tokens
- 770 lines ≈ 10,000 tokens
- 1,000 lines ≈ 13,000 tokens (too large)

**Check:**
```bash
wc -l file.md  # Count lines
# If > 770 lines, consider splitting
```

---

## Template Quick Selection

| Stage | Template | Purpose |
|-------|----------|---------|
| **Stage 1** | `templates/discovery_report_template.md` | Document issues found |
| **Stage 2** | `templates/fix_plan_template.md` | Organize fixes by group |
| **Stage 4** | `templates/verification_report_template.md` | Document verification results |
| **Stage 5** | `templates/round_summary_template.md` | Summarize round + decision |

---

## Scenario Quick Lookup

**"I just completed S10.P1 guide updates"**
→ Run full audit focusing on D1, D2, D6, D8 (3-4 hours, 3-4 rounds)

**"I just did stage renumbering"**
→ Run full audit focusing on D1, D3, D6, D8, D12 (4-6 hours, 3-4 rounds min)

**"I just changed notation system"**
→ Run full audit focusing on D2, D6, D7, D9 (3-5 hours, 3-4 rounds)

**"User reported broken link"**
→ Spot-check (30 min), if widespread → Full D1 audit (2 hours)

**"Routine maintenance"**
→ Run `pre_audit_checks.sh` → If clean, done → If issues, focused audit (1-2 hours)

---

## Loop vs Exit Quick Decision

```text
┌─────────────────────────────────────┐
│  Are ALL 9 exit criteria TRUE?     │
│  (Minimum 3 rounds, N_new=0, etc.)  │
└─────────┬───────────────────────────┘
          │
    ┌─────┴─────┐
    │           │
   YES          NO
    │           │
    │           └──→ LOOP to Round N+1
    │                (Fix what failed)
    │
    ├──→ Has user challenged?
    │
    ├─ YES → LOOP immediately (user usually right)
    │
    └─ NO → Present results
           │
           └──→ User approves → EXIT audit ✅
                User challenges → LOOP to Round 1

```

---

## Troubleshooting Quick Guide

**"I keep finding issues every round"**
→ Good! This is normal. Keep looping until Round N finds ZERO new issues. KAI-7 needed 4 rounds.

**"Round 3 still found issues"**
→ Continue to Round 4. Minimum 3 rounds is BASELINE, not target. Exit trigger is ZERO issues, not round count.

**"User said 'are you sure?'"**
→ Immediately LOOP back to Round 1. User challenge = evidence you missed something. Do NOT defend previous work.

**"Confidence is 75%"**
→ Below 80% threshold. Continue to Round N+1 with expanded search. Target areas causing doubt.

**"Pre-audit script found 20 issues"**
→ Expected! Script catches 40-50% of issues. Fix these, then start Stage 1 discovery for remaining issues.

**"I fixed everything but verification found new issues"**
→ N_new > 0 means LOOP to Round N+1. Pattern variations exposed missed cases. This is the system working correctly.

**"Should I skip Stage 2?"**
→ No. All stages mandatory. Stage 2 groups issues for efficient fixes. Skipping stages = incomplete audit.

---

## Emergency Protocols

**User Lost Confidence in Audit:**
1. Acknowledge user is right to challenge
2. Return to Stage 1 with completely different patterns
3. Assume EVERYTHING is wrong until proven otherwise
4. Document evidence for every claim

**Audit Taking Too Long (> 8 hours):**
1. Check if using fresh eyes each round (most common issue)
2. Verify not re-running same patterns (wastes time finding nothing)
3. Check confidence - if < 80%, that's why still going
4. Remember: KAI-7 took 4 rounds, 221+ fixes. Long audits = thorough audits.

**Found Critical Workflow Break:**
1. Fix immediately (don't batch with cosmetic issues)
2. Test fix works (can agent follow workflow?)
3. Document in discovery report with HIGH severity
4. User should review critical fixes before continuing

---

## Further Reading

**For comprehensive understanding:**
- Start: `README.md` (navigation and scenarios)
- Philosophy: `audit_overview.md` (when to audit, fresh eyes, exit criteria)
- Execution: `stages/stage_N_*.md` (stage-by-stage guides)
- Deep-dives: `dimensions/dN_*.md` (dimension-specific patterns)

**For specific situations:**
- User challenges: `audit_overview.md` → "User Challenge Protocol"
- Low confidence: `audit_overview.md` → "Fresh Eyes" operational guide
- Deciding to exit: `stage_5_loop_decision.md` → All 9 exit criteria detailed

---

**This quick reference provides common commands and checklists. For complete methodology, read the full guides.**

**Last Updated:** 2026-02-02
**Version:** 1.0
