# Fix Plan - Round 1

**Date:** 2026-02-04
**Round:** 1
**Total Issues:** 40+
**Fix Groups:** 4 groups
**Estimated Duration:** 30-45 minutes

---

## Execution Order Summary

| Priority | Group | Type | Count | Duration |
|----------|-------|------|-------|----------|
| P1 | Group 1: 28 → 22 iterations | Automated | 35+ | 10 min |
| P1 | Group 2: 24 iterations conflict | Manual | 4 | 5 min |
| P1 | Group 3: S2 9-phase → 2-phase | Manual | 3+ | 10 min |
| P2 | Group 4: Audit examples (15/28) | Manual | 6 | 10 min |

**Total:** 35-45 minutes

---

## Group 1: 22 iterations → 22 iterations (P1, Automated)

**Pattern:** `22 iteration` → `22 iteration` (with word boundaries)
**Count:** 35+ instances across 15+ files
**Severity:** High (affects user understanding and agent execution)
**Automated:** Yes

### Affected Files

- `README.md` (8+ instances)
- `EPIC_WORKFLOW_USAGE.md` (3 instances)
- `prompts/s5_s8_prompts.md` (7 instances)
- `prompts/special_workflows_prompts.md` (1 instance)
- `prompts_reference_v2.md` (1 instance)
- `reference/common_mistakes.md` (1 instance)
- `reference/faq_troubleshooting.md` (1 instance)
- `reference/glossary.md` (4 instances)
- `reference/stage_5/stage_5_reference_card.md` (3 instances)
- `reference/stage_10/lessons_learned_examples.md` (1 instance)
- `stages/s5/s5_bugfix_workflow.md` (4 instances)
- `stages/s5/s5_p2_planning_round2.md` (1+ instances)
- `templates/epic_lessons_learned_template.md` (1 instance)
- `templates/epic_readme_template.md` (1 instance)
- `templates/TEMPLATES_INDEX.md` (3 instances)
- `missed_requirement/s9_s10_special.md` (1 instance)

### Fix Command

```bash
# Execute from feature-updates/guides_v2/
cd feature-updates/guides_v2

# Global replacement across all markdown files (excluding S5_UPDATE_NOTES.md which is intentional)
find . -name "*.md" -type f ! -name "S5_UPDATE_NOTES.md" \
  -exec sed -i 's/22 iteration/22 iteration/g' {} +
```

### Verification Command

```bash
# Should return 0 (excluding S5_UPDATE_NOTES.md)
grep -rn "22 iteration" --include="*.md" . | grep -v "S5_UPDATE_NOTES.md" | wc -l

# Spot-check key files
grep "iteration" README.md | grep -E "(22|24|28)"
grep "iteration" EPIC_WORKFLOW_USAGE.md | grep -E "(22|24|28)"
grep "iteration" prompts/s5_s8_prompts.md | head -10
```

### Expected Changes

- README.md: 8 replacements (lines 112, 171, 224, 334, 496, 499, 774, 776)
- All other files: "22 iteration" → "22 iteration"

---

## Group 2: Iteration progress fractions (P1, Manual)

**Pattern:** Progress notation like "16/28", "22/28", "12/28" needs recalculation
**Count:** 7+ instances in prompts/s5_s8_prompts.md
**Severity:** High (incorrect progress tracking)
**Automated:** No (requires round boundary recalculation)

### Context

S5 now has 22 iterations across 3 rounds:
- **Round 1:** I1-I7 = 7 iterations (progress after: 7/22)
- **Round 2:** I8-I13 = 6 iterations (progress after: 13/22)
- **Round 3:** I14-I22 = 9 iterations (progress after: 22/22)

### Affected File

`prompts/s5_s8_prompts.md`

### Manual Edits Required

**Line 133:**
```diff
- Round 2 complete (16/22 iterations done, confidence >= MEDIUM, test coverage >90%)
+ Round 2 complete (13/22 iterations done, confidence >= MEDIUM, test coverage >90%)
```

**Line 172:**
```diff
- ✅ Round 2 complete (16/22 iterations)
+ ✅ Round 2 complete (13/22 iterations)
```

**Line 195:**
```diff
- Round 3 Part 1 complete (22/22 iterations done)
+ Round 3 Part 1 complete (22/22 iterations done)
```

**Line 234:**
```diff
- ✅ Round 3 Part 1 complete (22/22 iterations)
+ ✅ Round 3 Part 1 complete (22/22 iterations)
```

**Line 258:**
```diff
- Agent detects S5 complete (22 iterations done)
+ Agent detects S5 complete (22 iterations done)
```

**Line 260:**
```diff
- Prerequisite: S5 complete (22 iterations passed, implementation_plan.md v3.0 created)
+ Prerequisite: S5 complete (22 iterations passed, implementation_plan.md v3.0 created)
```

**Line 322:**
```diff
- ✅ S5 complete (EPIC_README.md shows 22 iterations done)
+ ✅ S5 complete (EPIC_README.md shows 22 iterations done)
```

### Also Check: README.md "24 iterations" conflict

**Lines 532, 536, 632, 721** mention "24 verification iterations":

**Analysis:** These likely meant "22 iterations" originally and got confused during an earlier update. Should all be "22 iterations" now.

**Manual Edits:**

`README.md`:
```diff
- Line 532: 1. 24 verification iterations mandatory (NO SKIPPING)
+ Line 532: 1. 22 verification iterations mandatory (NO SKIPPING)

- Line 632: 4. Agent executes 24 verification iterations across 3 rounds
+ Line 632: 4. Agent executes 22 verification iterations across 3 rounds

- Line 721: 1. Session compacts during S5 (iteration 12/24)
+ Line 721: 1. Session compacts during S5 (iteration 12/22)
```

**Line 536:** "Algorithm Traceability Matrix required (iterations 4, 11, 19)" - Keep as-is (specific iteration numbers, not a count)

### Verification

```bash
# Should return 0
grep -rn "/28\|28/" prompts/s5_s8_prompts.md | wc -l
grep -rn "24 iteration\|/24" README.md | wc -l
```

---

## Group 3: S2 9-phase → 2-phase structure (P1, Manual)

**Pattern:** References to "9 phases across 3 sub-stages" → "2 phases: S2.P1 (3 iterations), S2.P2 (pairwise)"
**Count:** 3+ instances
**Severity:** High (workflow structure changed)
**Automated:** No (requires rewrite)

### Affected File

`reference/stage_2/stage_2_reference_card.md`

### Manual Edits Required

**Line 5:**
```diff
- **Total Time:** 2-3 hours per feature (9 phases across 3 sub-stages)
+ **Total Time:** 2.25-4 hours per feature (2 phases: S2.P1 with 3 iterations, S2.P2 pairwise comparison)
```

**Line 12-21 (Current structure):**
```text
S2.P1: Research Phase (45-60 min)
...
S2.P2: Specification Phase (30-45 min)
...
S2.P3: Refinement Phase (45-60 min)
```

**Should Be:**
```text
S2.P1: Spec Creation and Refinement (2.25-3.5 hours)
  - S2.P1.I1: Feature-Level Discovery (60-90 min)
  - S2.P1.I2: Checklist Resolution (45-90 min)
  - S2.P1.I3: Refinement & Alignment (30-60 min)

S2.P2: Cross-Feature Alignment (20-60 min)
  - Primary agent only
  - Pairwise comparison of all features in group
```

**Line 231:**
```diff
- - [ ] All 9 phases executed (0 through 6)
+ - [ ] All phases executed (S2.P1 iterations 1-3, S2.P2 alignment)
```

### Also Check: stages/s2/s2_feature_deep_dive.md

**Lines 418, 498, 532** have old checklist content:

**Line 99:** "S2.P1 now has 3 iterations (was 9 phases across 3 files)" - **Keep as-is** (intentional historical reference)

**Line 418:** "□ All 9 phases complete:" - **Needs update** to new structure

**Line 498:** "A: No. All 9 phases are mandatory." - **Needs update** to clarify new structure

**Line 532:** "Workflow remains the same: 9 phases, 3 mandatory gates..." - **Needs update**

### Verification

```bash
# Should return 0-1 (only line 99 with historical reference should remain)
grep -rn "9 phase" reference/stage_2/ stages/s2/ --include="*.md" -i | wc -l
```

---

## Group 4: Audit examples with outdated iteration counts (P2, Manual)

**Pattern:** Examples showing "15 iterations" and "22 iterations" in d8_claude_md_sync.md
**Count:** 6 instances
**Severity:** Medium (audit dimension examples)
**Automated:** No (requires example rewrite with context)

### Affected File

`audit/dimensions/d8_claude_md_sync.md`

### Context

File uses "15 iterations" and "22 iterations" as historical examples of CLAUDE.md being out of sync. Need to update examples to reflect current reality (22 iterations) while preserving educational value.

### Manual Edits Required

**Lines 69-72:**
```diff
- CLAUDE.md: "S5: Implementation Planning (15 iterations, 3 phases)"
- Reality: S5 has 22 iterations across 3 rounds
- Result: Agent thinks they're done after 15 iterations, skips critical checks
+ CLAUDE.md: "S5: Implementation Planning (22 iterations, 3 rounds)" (outdated as of 2026-02-04)
+ Reality: S5 has 22 iterations across 3 rounds (as of 2026-02-04)
+ Result: Agent thinks they need to do 22 iterations, expects iterations that don't exist
```

**Lines 269-272:**
```diff
- 2. Update S5 guides: 15 iterations → 22 iterations
- 3. Current epic uses updated 28-iteration process
- 4. Forget to update CLAUDE.md (still says 15 iterations)
- 5. Next epic starts, reads CLAUDE.md, thinks 15 iterations
+ 2. Update S5 guides: 22 iterations → 22 iterations (testing moved to S4)
+ 3. Current epic uses updated 22-iteration process
+ 4. Forget to update CLAUDE.md (still says 22 iterations)
+ 5. Next epic starts, reads CLAUDE.md, thinks 22 iterations exist
```

**Lines 577-578:**
```diff
- CLAUDE.md: "S5: Implementation Planning (15 iterations)"
- Guide: "S5: Implementation Planning (22 iterations across 3 rounds:
+ CLAUDE.md: "S5: Implementation Planning (22 iterations)" (outdated)
+ Guide: "S5: Implementation Planning (22 iterations across 3 rounds)"
```

**Lines 631-632:**
```diff
- **Problem:** S5 expanded from 15 to 22 iterations
- **Actual:** S5 has 22 iterations across 3 rounds
+ **Problem:** S5 changed from 28 to 22 iterations (testing moved to S4)
+ **Actual:** S5 has 22 iterations across 3 rounds
```

**Lines 186-188, 569-570:** Similar updates needed

### Verification

```bash
# Check that examples now reference 22 iterations as current reality
grep -rn "22 iteration" audit/dimensions/d8_claude_md_sync.md | wc -l  # Should be >0

# Check that historical context is preserved
grep -rn "22 iteration.*outdated\|22 iteration.*(as of" audit/dimensions/d8_claude_md_sync.md | wc -l  # Should be >0
```

---

## Execution Steps

### Step 1: Run Automated Fix (Group 1)

```bash
cd feature-updates/guides_v2

# Backup (optional but recommended)
git status  # Ensure clean state
git diff    # No uncommitted changes

# Execute replacement
find . -name "*.md" -type f ! -name "S5_UPDATE_NOTES.md" \
  -exec sed -i 's/22 iteration/22 iteration/g' {} +

# Verify
grep -rn "22 iteration" --include="*.md" . | grep -v "S5_UPDATE_NOTES.md"
# Expected: 0 results (or only intentional contexts)
```

### Step 2: Manual Fixes - Group 2 (Iteration progress)

Use Edit tool to update `prompts/s5_s8_prompts.md` and `README.md` as documented above.

### Step 3: Manual Fixes - Group 3 (S2 structure)

Use Edit tool to update `reference/stage_2/stage_2_reference_card.md` and `stages/s2/s2_feature_deep_dive.md` as documented above.

### Step 4: Manual Fixes - Group 4 (Audit examples)

Use Edit tool to update `audit/dimensions/d8_claude_md_sync.md` as documented above.

### Step 5: Verification Round

Run all verification commands from each group to ensure completeness.

---

## Exit Criteria

- [x] All issues grouped by pattern
- [x] Groups prioritized by severity
- [x] Sed commands created for automated groups
- [x] Manual edit locations identified
- [x] Fix order documented
- [x] Verification commands provided
- [x] Ready to proceed to Stage 3 (Apply Fixes)

---

**Next Stage:** `stages/stage_3_apply_fixes.md`
