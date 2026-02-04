# Stage 5: Loop Decision

**Purpose:** Decide whether audit is complete or another round is needed
**Duration:** 15-30 minutes
**Input:** Verification report from Stage 4
**Output:** Round summary + decision to EXIT or LOOP
**Reading Time:** 10-15 minutes

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Exit Criteria Checklist](#exit-criteria-checklist)
4. [Decision Logic](#decision-logic)
5. [If Continuing to Next Round](#if-continuing-to-next-round)
6. [If Exiting Audit](#if-exiting-audit)
7. [User Presentation](#user-presentation)
8. [Commit Strategy](#commit-strategy)

---

## Overview

### Purpose

**Stage 5: Loop Decision** is where you determine if the audit is complete or if another round is needed.

**Two outcomes possible:**
1. **EXIT** - Audit complete, all criteria met
2. **LOOP** - Continue to Round N+1 with fresh patterns

**Critical Principle:** Better to do one more round than exit prematurely.

### Why This Stage Matters

**Historical Evidence (KAI-7 Audit):**
- Agents naturally want to finish quickly
- Premature exit = missed issues
- "Are you sure?" from user = red flag
- Minimum 3 rounds is NOT arbitrary - it's evidence-based

**From monolithic guide:**
> "Premature completion claims: 3 times (each time, 50+ more issues found)"

---

## Prerequisites

### Before Making Loop Decision

**Verify you have:**

- [ ] Completed Stage 4 (Verification)
- [ ] Verification report with all counts
- [ ] N_new = 0 (no new issues in verification)
- [ ] N_remaining documented (intentional cases explained)
- [ ] Spot-check results (10+ files)
- [ ] Pattern variation results (5+ patterns)
- [ ] Round summary prepared

**If missing any:** Return to Stage 4 and complete verification fully.

---

## Exit Criteria Checklist

### ALL Must Be True to Exit

**Check each criterion - failing ANY means LOOP:**

#### Criterion 1: Minimum Rounds
- [ ] Completed at least 3 rounds with fresh eyes
- [ ] Each round used different patterns than previous
- [ ] Each round explored different file orders
- [ ] Clear mental break between rounds (fresh perspective)

**If Round < 3:** MUST loop (not optional)

#### Criterion 2: Zero New Discoveries
- [ ] Round N Discovery (Stage 1) found ZERO new issues
- [ ] Tried at least 5 different pattern types in discovery
- [ ] Searched all folders systematically
- [ ] Used automated scripts + manual search

**If found new issues in Stage 1:** MUST loop

#### Criterion 3: Zero Verification Findings
- [ ] Round N Verification (Stage 4) found ZERO new issues
- [ ] Re-ran all patterns from Discovery
- [ ] Tried pattern variations not used in Discovery
- [ ] Spot-checked 10+ random files

**If N_new > 0:** MUST loop

#### Criterion 4: All Remaining Documented
- [ ] All remaining pattern matches are documented
- [ ] Each has: File path + line number
- [ ] Each has: Why it's intentional
- [ ] Each has: Why it's acceptable
- [ ] Context analysis performed for each

**If undocumented matches remain:** MUST loop

#### Criterion 5: User Verification Passed
- [ ] User has NOT challenged findings
- [ ] No "are you sure?" questions from user
- [ ] No "did you actually make fixes?" questions
- [ ] No "assume everything is wrong" requests

**If user challenged:** IMMEDIATELY loop back to Round 1

#### Criterion 6: Confidence Calibrated
- [ ] Confidence score ≥ 80% (see `../reference/confidence_calibration.md` ⏳ - use self-assessment)
- [ ] Self-assessed using scoring rubric
- [ ] No red flags present
- [ ] Feel genuinely complete, not just wanting to finish

**If confidence < 80%:** MUST loop

#### Criterion 7: Pattern Diversity
- [ ] Used at least 5 different pattern types across ALL rounds
- [ ] Basic exact matches ✓
- [ ] Pattern variations ✓
- [ ] Contextual patterns ✓
- [ ] Manual reading ✓
- [ ] Spot-checks ✓

**If pattern diversity < 5 types:** MUST loop

#### Criterion 8: Spot-Check Clean
- [ ] Random sample of 10+ files shows zero issues
- [ ] Files selected randomly (not cherry-picked)
- [ ] Manually read sections (not just grep)
- [ ] No issues found in visual inspection

**If spot-checks found issues:** MUST loop

---

## Decision Logic

### The Decision Tree

```
┌─────────────────────────────────────────────┐
│  Check ALL 8 Exit Criteria                  │
└─────────────────────────────────────────────┘
                    ↓
          ┌─────────┴─────────┐
          │                   │
    ALL criteria met?    ANY criterion failed?
          │                   │
          ↓                   ↓
    ┌─────────┐         ┌─────────┐
    │ Maybe   │         │  LOOP   │
    │ Exit    │         │ BACK    │
    └─────────┘         └─────────┘
          │                   │
          ↓                   ↓
    Present to user    Round N+1 Stage 1
          │            (fresh patterns)
          ↓
    User approves?
          │
    ┌─────┴─────┐
    │           │
   YES         NO
    │           │
    ↓           ↓
   EXIT       LOOP
(commit)    (user knows best)
```

### Automated Decision

```bash
# Count criteria met
criteria_met=0

# Criterion 1: Minimum 3 rounds
[ $round_number -ge 3 ] && ((criteria_met++))

# Criterion 2: Zero new discoveries in Stage 1
[ $stage1_new_issues -eq 0 ] && ((criteria_met++))

# Criterion 3: Zero new findings in Stage 4
[ $N_new -eq 0 ] && ((criteria_met++))

# Criterion 4: All remaining documented
[ $undocumented_matches -eq 0 ] && ((criteria_met++))

# Criterion 5: User not challenged
[ "$user_challenged" == "false" ] && ((criteria_met++))

# Criterion 6: Confidence ≥ 80%
[ $confidence_score -ge 80 ] && ((criteria_met++))

# Criterion 7: Pattern diversity ≥ 5
[ $pattern_types_used -ge 5 ] && ((criteria_met++))

# Criterion 8: Spot-checks clean
[ $spot_check_issues -eq 0 ] && ((criteria_met++))

# Decision
if [ $criteria_met -eq 8 ]; then
  echo "✅ ALL criteria met - Present to user for final approval"
else
  echo "❌ $((8-criteria_met)) criteria failed - LOOP to Round $((round_number+1))"
fi
```

---

## If Continuing to Next Round

### When to Loop

**MUST loop if:**
- ANY of the 8 criteria failed
- User challenged findings
- You feel uncertain about completeness
- Spot-checks revealed issues

### Preparing for Next Round

**Before starting Round N+1:**

```markdown
## Round N+1 Preparation

### Why Looping
[List which criteria failed]

### Lessons from Round N
[What was missed, why it was missed]

### Changes for Round N+1
**Different Patterns:**
- [List new patterns to try]

**Different Approach:**
- [Different folder order, different search strategy]

**Fresh Eyes:**
- [Take 5-10 minute break]
- [Clear assumptions from Round N]
- [Approach as if first time]

### Specific Focus
[What to pay extra attention to]
```

### Starting Round N+1

```
1. Take 5-10 minute break (clear mental model)
   ↓
2. Do NOT look at Round N notes until after discovery
   ↓
3. Return to Stage 1: Discovery
   ↓
4. Use completely different patterns than Round N
   ↓
5. Search folders in different order
   ↓
6. Complete all 5 stages again
   ↓
7. Return to Stage 5 decision
```

---

## If Exiting Audit

### When Exit is Appropriate

**Only exit if:**
- ALL 8 criteria met
- User approves exit
- Feel genuinely complete (not just tired)
- No lingering doubts

### Final Actions Before Exit

```markdown
## Pre-Exit Checklist

- [ ] All 8 criteria verified one more time
- [ ] Round summary created
- [ ] Evidence compiled for user
- [ ] Intentional cases documented
- [ ] Commit message drafted
- [ ] User presentation prepared
```

### Creating Final Summary

```markdown
# Audit Complete Summary

**Date:** YYYY-MM-DD
**Total Rounds:** N
**Total Duration:** X hours
**Total Issues Found:** N
**Total Issues Fixed:** N

## By Round

### Round 1
- Focus: [Initial discovery]
- Issues: N found, N fixed
- Duration: XX min

### Round 2
- Focus: [Pattern variations]
- Issues: N found, N fixed
- Duration: XX min

### Round 3
- Focus: [Deep validation]
- Issues: N found, N fixed
- Duration: XX min

[Continue for all rounds]

## By Dimension

| Dimension | Issues Found | Issues Fixed |
|-----------|--------------|--------------|
| D1: Cross-Reference | 20 | 20 |
| D2: Terminology | 70 | 70 |
| D10: File Size | 2 | 2 |
[Continue for all dimensions with issues]

## Final Verification

- N_remaining: 0 (or N intentional cases documented)
- N_new: 0 (no new issues in final verification)
- Spot-checks: 12 files, zero issues
- Confidence: 95%

## Intentional Cases (if any)

[Document any remaining pattern matches that are intentional]

## Recommendations

[Any suggestions for preventing these issues in future]
```

---

## User Presentation

### What to Present to User

**Required information:**

```markdown
# Audit Results - Round N Complete

## Executive Summary

**Status:** Ready to exit OR Need another round
**Total Issues:** [N found, N fixed, N remaining]
**Confidence:** [XX%]
**Recommendation:** [EXIT or LOOP]

## Evidence

### Verification Passed
- N_new = 0
- N_remaining = 0 (or only intentional)
- Spot-checks clean (10+ files)
- 5+ pattern types used

### All Criteria Met
- [x] Criterion 1: Minimum 3 rounds completed
- [x] Criterion 2: Zero new discoveries
- [x] Criterion 3: Zero verification findings
- [x] Criterion 4: All remaining documented
- [x] Criterion 5: User verification passed
- [x] Criterion 6: Confidence ≥ 80%
- [x] Criterion 7: Pattern diversity ≥ 5
- [x] Criterion 8: Spot-checks clean

### Files Modified
[List of files changed with brief description]

### Before/After Examples
[Show 2-3 examples of fixes with context]

## Invite Challenge

Please review findings and challenge if:
- You see incomplete verification
- You notice patterns we missed
- You have doubts about completeness
- You see issues we didn't catch

**If you say "are you sure?", I will immediately loop back to Round 1**
```

### Responding to User

**If user approves:**
```
✅ Proceed to commit
```

**If user challenges:**
```
🚨 IMMEDIATELY loop back to Round 1
- User challenge = evidence of missed issues
- Do NOT defend findings
- Assume user is correct
- Start fresh with new patterns
```

**If user asks clarifying questions:**
```
Answer thoroughly, then:
- If still satisfied → commit
- If user expresses doubt → loop back
```

---

## Commit Strategy

### When to Commit

**Only commit if:**
- All 8 exit criteria met
- User approved exit
- Round summary created
- No outstanding issues

### Commit Organization

**Strategy:** One commit per round

```bash
# For each round, create separate commit
git add -A
git commit -m "feat/KAI-7: Apply Round N audit fixes - [focus]"

# Example for Round 3:
git commit -m "feat/KAI-7: Apply Round 3 audit fixes - notation standardization

Fixed 70+ instances of old notation across 30+ files:

Group 1: Old Stage Notation (60+ instances)
- S5a → S5, S6a → S6, S7a → S7, S8a → S8, S9a → S9

Group 2: STAGE_Xx Format (1 instance)
- s8_p2_epic_testing_update.md: STAGE_5a → S5

Group 3: Wrong Stage Header (1 instance)
- s10_epic_cleanup.md: CRITICAL RULES FOR STAGE 7 → STAGE 10

Verification: Zero remaining issues

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
"
```

### Final Commit

**After all rounds complete:**

```bash
# All round commits done individually
# Update any tracking files if needed

git log --oneline | head -10
# Shows all round commits
```

---

## Exit Criteria Decision Matrix

### Quick Reference

| Criterion | How to Check | Pass Threshold | If Failed |
|-----------|--------------|----------------|-----------|
| 1. Min Rounds | Count rounds | ≥ 3 | LOOP (not optional) |
| 2. Zero New in Stage 1 | Stage 1 report | 0 issues | LOOP |
| 3. Zero New in Stage 4 | N_new count | 0 | LOOP |
| 4. All Documented | Undocumented count | 0 | LOOP |
| 5. User Approved | User response | No challenge | LOOP if challenged |
| 6. Confidence | Self-assessment | ≥ 80% | LOOP |
| 7. Pattern Diversity | Count pattern types | ≥ 5 types | LOOP |
| 8. Spot-Check Clean | Issues in spot-check | 0 | LOOP |

**EXIT RULE:** ALL 8 must pass + user approval

---

## See Also

**Previous Stage:**
- `stage_4_verification.md` - Verification that informs this decision

**If Looping:**
- `stage_1_discovery.md` - Start Round N+1 with fresh patterns

**Templates:**
- `../templates/round_summary_template.md` - Use for final summary

**Reference:**
- `../reference/confidence_calibration.md` ⏳ - How to score confidence (use self-assessment for now)
- `../reference/user_challenge_protocol.md` ⏳ - How to respond to challenges (see audit_overview.md)

---

**After completing Stage 5:**
- If EXIT → Commit and complete audit
- If LOOP → Return to Stage 1 for Round N+1
