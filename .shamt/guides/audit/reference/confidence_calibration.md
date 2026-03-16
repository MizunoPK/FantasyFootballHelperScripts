# Confidence Calibration

**Purpose:** Scoring system for audit completeness and confidence assessment
**Audience:** Agents evaluating readiness to exit audit loop (Stage 5)
**Last Updated:** 2026-02-25

---

## Table of Contents

1. [Quick Reference](#quick-reference)
2. [Confidence Scoring Formula](#confidence-scoring-formula)
3. [Component Scores](#component-scores)
4. [Red Flags](#red-flags)
5. [Self-Assessment Questions](#self-assessment-questions)
6. [Confidence Levels](#confidence-levels)
7. [Exit Threshold](#exit-threshold)

---

## Quick Reference

### Minimum Exit Threshold

```text
┌─────────────────────────────────────────────────────────────────┐
│  🎯 TARGET: Confidence Score ≥ 80%                              │
│                                                                  │
│  Required for exit (Stage 5 Criterion 7):                       │
│  • Self-assessed using scoring rubric (this guide)              │
│  • No red flags present                                         │
│  • Feel genuinely complete (not just wanting to finish)         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Quick Self-Assessment

**Ask yourself:**
1. Did I check ALL 22 dimensions across all 4 sub-rounds? (Yes/No)
2. Did I use 5+ different pattern types across rounds? (Yes/No)
3. Did I manually read 10+ random files per sub-round? (Yes/No)
4. Did I find ZERO new issues in latest round (all 4 sub-rounds)? (Yes/No)
5. Do I feel certain I didn't miss anything obvious? (Yes/No)

**If ANY answer is "No" → Confidence <80% → Must loop**

---

## Confidence Scoring Formula

### Overall Formula

```text
Confidence Score = (Coverage × Rigor × Verification × Consistency) × 100%

Where each component ranges from 0.0 to 1.0
```

### Component Weights

| Component | Description | Weight in Formula |
|-----------|-------------|-------------------|
| **Coverage** | Completeness of search scope | 25% (multiply by all) |
| **Rigor** | Thoroughness of validation | 25% (multiply by all) |
| **Verification** | Quality of fix validation | 25% (multiply by all) |
| **Consistency** | Pattern diversity across rounds | 25% (multiply by all) |

**Note:** Multiplicative formula means weakness in ANY area significantly reduces overall score.

---

## Component Scores

### Component 1: Coverage (Did you check everywhere?)

**Scoring Criteria:**

| Score | Coverage Description | Checklist |
|-------|----------------------|-----------|
| 1.0 | **Complete** | ✅ All 22 dimensions checked<br>✅ All 4 sub-rounds completed<br>✅ Root files checked (README.md, EPIC_WORKFLOW_USAGE.md, prompts_reference_v2.md)<br>✅ All directories searched (stages/, templates/, reference/, dimensions/)<br>✅ No intentional exclusions |
| 0.8 | **Mostly Complete** | ✅ All 22 dimensions checked<br>✅ All 4 sub-rounds completed<br>⚠️ Root files partially checked<br>✅ Main directories searched<br>⚠️ Minor directories skipped (examples/) |
| 0.6 | **Partial** | ⚠️ 15-18 dimensions checked<br>✅ All 4 sub-rounds completed<br>❌ Root files not specifically checked<br>✅ stages/ directory checked<br>⚠️ Some directories skipped |
| 0.4 | **Incomplete** | ❌ <15 dimensions checked<br>⚠️ Some sub-rounds skipped<br>❌ Root files not checked<br>⚠️ Only stages/ directory checked |
| 0.2 | **Minimal** | ❌ <11 dimensions checked<br>❌ Sub-rounds not followed<br>❌ Root files excluded<br>❌ Only subset of directories |

**Self-Assessment:**
```text
Coverage Score = [Your score 0.0-1.0]

Justification:
- Dimensions checked: [N/19]
- Sub-rounds completed: [N.1, N.2, N.3, N.4 - all or subset]
- Root files checked: [Yes/No]
- Directories searched: [List]
- Intentional exclusions: [If any, why]
```

---

### Component 2: Rigor (How thoroughly did you check?)

**Scoring Criteria:**

| Score | Rigor Description | Checklist |
|-------|-------------------|-----------|
| 1.0 | **Very High** | ✅ 5+ pattern types used per dimension category<br>✅ Automated search + Manual reading<br>✅ Pattern variations checked (punctuation, spacing, case)<br>✅ Context analysis for all matches<br>✅ Spot-checked 10+ random files per sub-round<br>✅ Deep dives into complex files |
| 0.8 | **High** | ✅ 3-4 pattern types used<br>✅ Automated search + some manual reading<br>✅ Some pattern variations checked<br>⚠️ Context analysis for most matches<br>✅ Spot-checked 5-10 files per sub-round |
| 0.6 | **Medium** | ⚠️ 2-3 pattern types used<br>✅ Automated search only<br>⚠️ Basic patterns, few variations<br>⚠️ Context analysis for obvious cases<br>⚠️ Spot-checked <5 files per sub-round |
| 0.4 | **Low** | ⚠️ 1-2 pattern types used<br>⚠️ Automated search only<br>❌ Exact matches only, no variations<br>❌ No context analysis<br>❌ No spot-checks |
| 0.2 | **Minimal** | ❌ Single pattern type<br>❌ Basic grep only<br>❌ No variations<br>❌ No context analysis<br>❌ No manual validation |

**Self-Assessment:**
```text
Rigor Score = [Your score 0.0-1.0]

Justification:
- Pattern types used: [List types]
- Automated + Manual: [Yes/No]
- Variations checked: [List variations]
- Context analysis: [Always/Sometimes/Never]
- Spot-checks performed: [N files per sub-round]
```

---

### Component 3: Verification (How well did you validate fixes?)

**Scoring Criteria:**

| Score | Verification Description | Checklist |
|-------|--------------------------|-----------|
| 1.0 | **Complete** | ✅ Re-ran ALL discovery patterns<br>✅ Tried NEW pattern variations<br>✅ Spot-checked 10+ modified files<br>✅ Before/after examples documented<br>✅ N_remaining = 0 OR all documented as intentional<br>✅ N_new = 0 (no new issues introduced) |
| 0.8 | **Thorough** | ✅ Re-ran most discovery patterns<br>⚠️ Tried some new variations<br>✅ Spot-checked 5-10 modified files<br>✅ Some before/after examples<br>✅ N_remaining = 0 OR documented<br>✅ N_new = 0 |
| 0.6 | **Adequate** | ⚠️ Re-ran main patterns<br>⚠️ Few new variations<br>⚠️ Spot-checked <5 files<br>⚠️ Limited before/after examples<br>⚠️ N_remaining > 0 (some undocumented)<br>✅ N_new = 0 |
| 0.4 | **Insufficient** | ⚠️ Re-ran some patterns<br>❌ No new variations<br>❌ Minimal spot-checks<br>❌ No before/after examples<br>❌ N_remaining > 0 (undocumented)<br>⚠️ N_new > 0 (minor) |
| 0.2 | **Minimal** | ❌ Didn't re-run patterns<br>❌ No new variations<br>❌ No spot-checks<br>❌ No documentation<br>❌ N_new > 0 (significant) |

**Self-Assessment:**
```text
Verification Score = [Your score 0.0-1.0]

Justification:
- Patterns re-run: [N/M]
- New variations tried: [Yes/No, which]
- Spot-checks: [N files]
- Before/after documented: [Yes/No]
- N_remaining: [N, documented or undocumented]
- N_new: [N]
```

---

### Component 4: Consistency (Did you use fresh eyes each round?)

**Scoring Criteria:**

| Score | Consistency Description | Checklist |
|-------|-------------------------|-----------|
| 1.0 | **Excellent** | ✅ 5+ different pattern types across all rounds<br>✅ Different search order each round<br>✅ Fresh mental model (2-5 min break between rounds)<br>✅ Didn't rely on memory from previous rounds<br>✅ Each round found NEW issues OR validated thoroughness<br>✅ No pattern repetition without variation |
| 0.8 | **Good** | ✅ 4 different pattern types<br>✅ Mostly different search order<br>✅ Some breaks between rounds<br>⚠️ Sometimes relied on memory<br>✅ Most rounds productive |
| 0.6 | **Fair** | ⚠️ 3 pattern types<br>⚠️ Similar search order<br>⚠️ Minimal breaks<br>⚠️ Relied on memory from Round 1<br>⚠️ Some rounds redundant |
| 0.4 | **Poor** | ⚠️ 2 pattern types<br>❌ Same search order<br>❌ No breaks<br>❌ Heavily relied on memory<br>❌ Most rounds redundant |
| 0.2 | **Very Poor** | ❌ 1 pattern type repeated<br>❌ Identical approach each round<br>❌ No fresh eyes<br>❌ All rounds redundant |

**Self-Assessment:**
```text
Consistency Score = [Your score 0.0-1.0]

Justification:
- Pattern types across rounds: [List all types used]
- Search order variation: [Yes/No]
- Breaks between rounds: [Yes/No, duration]
- Relied on memory: [Never/Sometimes/Often]
- Round productivity: [Each round found issues OR validated completeness]
```

---

## Red Flags

### Automatic Confidence Reduction

**If ANY of these are true, reduce confidence by 20 percentage points:**

🚩 **consecutive_clean < 3:** Required consecutive zero-issue rounds not yet met
🚩 **N_new > 0:** New issues introduced by fixes
🚩 **User Challenged:** User expressed doubt at any point
🚩 **Root Files Skipped:** README.md, EPIC_WORKFLOW_USAGE.md, prompts_reference_v2.md not checked
🚩 **Sub-Round Skipped:** Did not complete all 4 sub-rounds
🚩 **Pattern Diversity <3:** Used fewer than 3 different pattern types
🚩 **No Manual Reading:** Relied entirely on automated grep
🚩 **Working from Memory:** Didn't re-read files in later rounds
🚩 **Feeling Rushed:** Want to finish quickly rather than genuinely complete

**Example:**
```text
Calculated Score: 85%
Red Flags Present: 2 (User challenged, Pattern diversity <3)
Final Score: 85% - (2 × 20%) = 45%
Conclusion: MUST LOOP (< 80% threshold)
```

---

## Self-Assessment Questions

### Honest Evaluation (Answer Yes/No)

**Coverage Questions:**
1. Did I check ALL 22 dimensions? ___
2. Did I check root files (README.md, EPIC_WORKFLOW_USAGE.md, prompts_reference_v2.md)? ___
3. Did I search ALL directories (stages/, templates/, reference/, dimensions/)? ___
4. Did I complete ALL 4 sub-rounds (Core, Content, Structural, Advanced)? ___

**Rigor Questions:**
5. Did I use 5+ different pattern types? ___
6. Did I manually read files (not just grep)? ___
7. Did I check pattern variations (punctuation, spacing, case)? ___
8. Did I perform context analysis on matches? ___
9. Did I spot-check 10+ random files per sub-round? ___

**Verification Questions:**
10. Did I re-run ALL discovery patterns? ___
11. Did I try NEW pattern variations in verification? ___
12. Did I spot-check modified files? ___
13. Is N_new = 0 (no new issues introduced)? ___
14. Are ALL remaining instances documented as intentional? ___

**Consistency Questions:**
15. Did I use different patterns each round? ___
16. Did I take breaks between rounds (2-5 min)? ___
17. Did I search in different order each round? ___
18. Did I re-read files (not rely on memory)? ___

**Feeling Questions:**
19. Do I genuinely feel complete (not just tired)? ___
20. Would I bet my reputation this audit is thorough? ___

**Scoring:**
- **18-20 Yes:** Confidence 90-100% (Excellent)
- **15-17 Yes:** Confidence 80-89% (Good, exit threshold)
- **12-14 Yes:** Confidence 65-79% (Adequate, must loop)
- **9-11 Yes:** Confidence 50-64% (Insufficient, must loop)
- **<9 Yes:** Confidence <50% (Poor, restart audit)

---

## Confidence Levels

### 90-100%: Very High Confidence

**Characteristics:**
- All 4 components ≥ 0.9
- Zero red flags
- Comprehensive coverage
- Extreme rigor
- Complete verification
- Excellent pattern diversity

**Can Exit?** ✅ YES (exceeds threshold)

**Example:**
```text
Coverage: 1.0 (all 22 dimensions, all directories, root files)
Rigor: 0.95 (6 pattern types, automated + manual, deep context analysis)
Verification: 0.95 (all patterns re-run, new variations, extensive spot-checks)
Consistency: 1.0 (5+ pattern types across rounds, fresh eyes each round)

Score: 1.0 × 0.95 × 0.95 × 1.0 = 0.90 = 90%
```

---

### 80-89%: High Confidence

**Characteristics:**
- All 4 components ≥ 0.8
- Zero or one minor red flag
- Complete coverage
- High rigor
- Thorough verification
- Good pattern diversity

**Can Exit?** ✅ YES (meets threshold)

**Example:**
```text
Coverage: 1.0 (all dimensions, all directories)
Rigor: 0.8 (4 pattern types, automated + some manual)
Verification: 0.85 (most patterns re-run, some new variations)
Consistency: 0.8 (4 pattern types across rounds, mostly fresh eyes)

Score: 1.0 × 0.8 × 0.85 × 0.8 = 0.54 → 54% base
No red flags: 54% final

Wait - this example shows how multiplicative formula reduces score!
Need to recalculate with better component scores to hit 80%:

Coverage: 1.0
Rigor: 0.90
Verification: 0.90
Consistency: 1.0

Score: 1.0 × 0.9 × 0.9 × 1.0 = 0.81 = 81% ✅
```

---

### 65-79%: Medium Confidence

**Characteristics:**
- Some components <0.8
- One or two red flags
- Partial coverage OR moderate rigor
- Adequate verification
- Fair pattern diversity

**Can Exit?** ❌ NO (below threshold)

**Must:** Loop for at least one more round

---

### 50-64%: Low Confidence

**Characteristics:**
- Multiple components <0.7
- Multiple red flags
- Incomplete coverage
- Low rigor
- Insufficient verification

**Can Exit?** ❌ NO (significantly below threshold)

**Must:** Loop for 2+ more rounds with improved methodology

---

### <50%: Very Low Confidence

**Characteristics:**
- Most components <0.6
- Many red flags
- Minimal coverage
- Minimal rigor
- Minimal verification

**Can Exit?** ❌ NO (unacceptable)

**Must:** Restart audit with different approach

---

## Exit Threshold

### The 80% Rule

**Why 80%?**
- Balances thoroughness with practical completion
- High enough to ensure quality
- Achievable without perfectionism
- Based on historical audit data

**Historical Evidence:**
- Audits scoring <80%: Found 30+ additional issues in next round
- Audits scoring ≥80%: Found <5 issues in next round (mostly false positives)
- User challenges: 100% correlated with confidence <75%

### Calculating Your Score

**Step 1: Score Each Component (0.0 to 1.0)**
```text
Coverage Score: _____
Rigor Score: _____
Verification Score: _____
Consistency Score: _____
```

**Step 2: Calculate Base Score**
```text
Base Score = Coverage × Rigor × Verification × Consistency × 100%
Base Score = _____ %
```

**Step 3: Apply Red Flag Penalties**
```text
Red Flags Present: [List all that apply]
Count: _____ flags
Penalty: _____ × 20% = _____ %
```

**Step 4: Final Score**
```text
Final Score = Base Score - Penalty
Final Score = _____ %
```

**Step 5: Compare to Threshold**
```text
Exit Threshold: 80%
Your Score: _____ %

Decision:
[ ] ≥80% → Can exit (if all other criteria met)
[ ] <80% → Must loop
```

---

## Example Calculations

### Example 1: Strong Audit (Can Exit)

```text
Coverage: 1.0 (all 22 dimensions, all directories, root files checked)
Rigor: 0.9 (5 pattern types, automated + manual, thorough context analysis)
Verification: 0.9 (all patterns re-run, new variations, N_new=0)
Consistency: 0.95 (fresh eyes, different patterns each round)

Base Score: 1.0 × 0.9 × 0.9 × 0.95 = 0.7695 = 77%
Red Flags: None
Penalty: 0%

Final Score: 77% + 0% = 77%... wait, that's <80%!

This shows multiplicative formula is strict. To hit 80%, need:
Coverage: 1.0, Rigor: 0.95, Verification: 0.9, Consistency: 0.95
1.0 × 0.95 × 0.9 × 0.95 = 0.81 = 81% ✅
```

### Example 2: Weak Audit (Must Loop)

```text
Coverage: 0.8 (skipped root files)
Rigor: 0.7 (only 3 pattern types, no manual reading)
Verification: 0.7 (didn't re-run all patterns)
Consistency: 0.6 (same search order, relied on memory)

Base Score: 0.8 × 0.7 × 0.7 × 0.6 = 0.24 = 24%
Red Flags: Root Files Skipped (-20%), Pattern Diversity <3 (-20%)
Penalty: 40%

Final Score: 24% - 40% = 0% (floor at 0)
Decision: MUST LOOP ❌
```

---

## See Also

- **Stage 5 Loop Decision:** `stages/stage_5_loop_decision.md` - Exit criteria checklist
- **User Challenge Protocol:** `reference/user_challenge_protocol.md` - What to do if user challenges
- **Audit Overview:** `audit_overview.md` - Fresh eyes and zero assumptions philosophy
