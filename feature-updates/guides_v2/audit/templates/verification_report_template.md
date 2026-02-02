# Verification Report - Round [N]

**Date:** YYYY-MM-DD
**Round:** [Number]
**Duration:** [XX] minutes
**Verified By:** [Agent/Person]

---

## Executive Summary

**Verification Status:** ✅ PASSED / ❌ FAILED / ⚠️ PARTIAL

**Critical Counts:**
- **N_found:** [Number of issues from Stage 1 Discovery]
- **N_fixed:** [Number of issues fixed in Stage 3]
- **N_remaining:** [Number of instances still found - should be 0 or intentional]
- **N_new:** [Number of NEW issues found during verification - MUST be 0]

**Decision:**
- ✅ Ready for Stage 5 (Loop Decision)
- ❌ Loop back to Stage 3 (fixes incomplete)
- ❌ Loop back to Round N+1 Stage 1 (new issues found)

**Confidence Level:** [Low / Medium / High / Very High] ([XX]%)

---

## Tier 1: Re-Run Original Patterns

**Purpose:** Verify all issues from Stage 1 Discovery are resolved

### Pattern 1: [Description]

**Original Discovery Command:**
```bash
grep -rn "PATTERN" --include="*.md" path/
```

**Original Count:** [N] instances found in Stage 1

**Verification Results:**
```bash
$ grep -rn "PATTERN" --include="*.md" path/
# Results:
[Show matches OR "0 matches - ✅ Clean"]
```

**Status:** ✅ Clean / ⚠️ Remaining / ❌ Issues

**If Remaining:**
```
File: path/to/file.md
Line: 123
Match: [content]
Reason: [Intentional - historical example / Error - missed in Stage 3]
Action: [Document as acceptable / Fix and re-verify]
```

---

### Pattern 2: [Description]

[Repeat template for each pattern from Stage 1]

**Original Discovery Command:**
```bash
[Command]
```

**Original Count:** [N]

**Verification Results:**
```bash
[Results]
```

**Status:** ✅ Clean / ⚠️ Remaining / ❌ Issues

---

### Tier 1 Summary

**Total Patterns Re-Run:** [N]
**Patterns Clean:** [N] ✅
**Patterns with Remaining:** [N] ⚠️
**Patterns with Errors:** [N] ❌

**Tier 1 Status:** ✅ PASSED / ❌ FAILED

---

## Tier 2: New Pattern Variations

**Purpose:** Try variations of original patterns not used in Stage 1 to catch missed instances

### Why New Patterns Matter

**Original patterns might miss:**
- Punctuation variations (`:`, `-`, `.`, `,`)
- Parentheses/brackets (`(5a)`, `[5a]`)
- Context phrases ("back to 5a", "proceed to 5a")
- Case variations (lowercase, UPPERCASE)

### New Pattern 1: [Description]

**Pattern Not Tried in Stage 1:**
```bash
grep -rn "NEW_VARIATION" --include="*.md" path/
```

**Rationale:** [Why this variation might exist]

**Results:**
```bash
$ grep -rn "NEW_VARIATION" --include="*.md" path/
# Results:
[Show matches OR "0 matches - ✅ Clean"]
```

**Status:** ✅ Clean (0 matches) / ❌ Found issues (N matches)

**If Issues Found:**
```
N_new = N_new + [count]

Examples:
- file.md:45: [content]
- file.md:67: [content]

Analysis: [Why these were missed in Stage 1]
```

---

### New Pattern 2: [Description]

[Repeat for each new pattern variation tried]

**Pattern:**
```bash
[Command]
```

**Results:**
```bash
[Results]
```

**Status:** ✅ Clean / ❌ Found issues

---

### Tier 2 Summary

**New Pattern Variations Tried:** [N] (minimum 5 required)

**Results by Pattern:**
| Pattern | Description | Matches Found | N_new Contribution |
|---------|-------------|---------------|-------------------|
| 1 | [Description] | 0 | 0 ✅ |
| 2 | [Description] | 3 | +3 ❌ |
| 3 | [Description] | 0 | 0 ✅ |
| ... | ... | ... | ... |

**Total N_new from Tier 2:** [N]

**Tier 2 Status:** ✅ PASSED (N_new = 0) / ❌ FAILED (N_new > 0)

---

## Tier 3: Spot-Check Random Files

**Purpose:** Manual visual inspection to catch issues grep can't find

### Random File Selection

```bash
# Command used to select random files
find stages templates reference -name "*.md" -type f | shuf -n [N]
```

**Files Selected:** [N] files (minimum 10 required)

---

### File 1: [path/to/file.md]

**Sections Checked:**
- Lines 1-50 (beginning)
- Lines [mid]-[mid+50] (middle)
- Last 50 lines (end)

**What Looked For:**
- [ ] Patterns correct in context
- [ ] No broken markdown formatting
- [ ] Headers properly leveled
- [ ] Cross-references make sense
- [ ] No obvious typos
- [ ] Terminology consistent within file
- [ ] Code blocks properly formatted
- [ ] Lists/checklists consistent

**Issues Found:** [N]

**Details:**
```markdown
[If issues found, document each:
- Line: [N]
- Issue: [Description]
- Severity: Critical/High/Medium/Low
- N_new contribution: +1 if not caught in Stage 1
]

OR

No issues found - ✅ Clean
```

---

### File 2: [path/to/file.md]

[Repeat template for each spot-checked file]

**Sections Checked:** [Lines]

**Issues Found:** [N]

**Details:** [Details OR "No issues - ✅"]

---

### Tier 3 Summary

**Total Files Spot-Checked:** [N]
**Files Clean:** [N] ✅
**Files with Issues:** [N] ❌

**Total N_new from Tier 3:** [N]

**Tier 3 Status:** ✅ PASSED (0 issues) / ❌ FAILED (issues found)

---

## Final Counts

### The Four Critical Numbers

```markdown
┌─────────────────────────────────────────────┐
│ N_found:     [XX]  (from Stage 1)           │
│ N_fixed:     [XX]  (in Stage 3)             │
│ N_remaining: [XX]  (should be 0)            │
│ N_new:       [XX]  (MUST be 0)              │
└─────────────────────────────────────────────┘
```

**Verification Math:**
```
N_found = N_fixed + N_remaining
[XX] = [XX] + [XX]
✅ Math checks out / ❌ Math doesn't match
```

### N_remaining Breakdown (If > 0)

**All N_remaining instances must be documented:**

#### Remaining Instance #1
**File:** path/to/file.md
**Line:** 123
**Content:** `[old pattern still present]`
**Reason:** [Intentional - historical example / Intentional - quote / ERROR - missed fix]
**Status:** ✅ Acceptable (documented) / ❌ Must fix

[Repeat for each remaining instance]

**Summary:**
- Intentional cases: [N] (all documented and acceptable) ✅
- Errors (missed in Stage 3): [N] ❌

**If errors found:** Loop back to Stage 3, fix, re-run Stage 4

---

### N_new Breakdown (If > 0)

**⚠️ CRITICAL: N_new MUST be 0 to proceed to Stage 5**

**N_new Sources:**
- From Tier 2 (new pattern variations): [N]
- From Tier 3 (spot-checks): [N]
- **Total N_new:** [N]

**If N_new > 0:**
```markdown
❌ VERIFICATION FAILED - New issues discovered

Required Action:
1. STOP - Do not proceed to Stage 5
2. Document why these were missed in Stage 1
3. LOOP BACK to Round N+1 Stage 1
4. Use enhanced patterns in next round
5. Complete full audit loop again

Analysis of Why Missed:
[Explain what patterns/approach was insufficient in Stage 1]

Enhanced Patterns for Round N+1:
[List new patterns to use in next round's discovery]
```

---

## Pattern Diversity Assessment

**Purpose:** Ensure sufficient search coverage (minimum 5 pattern types required)

**Pattern Types Used Across All Rounds:**

- [ ] Basic exact matches (e.g., `grep -rn "exact string"`)
- [ ] Pattern variations (punctuation, case, etc.)
- [ ] Contextual patterns (phrases, sentences)
- [ ] Manual reading (spot-checks)
- [ ] Automated scripts (pre-audit checks)
- [ ] Cross-reference validation (link checking)
- [ ] File structure validation (find commands)
- [ ] Other: [Describe]

**Total Pattern Types Used:** [N]

**Status:** ✅ Sufficient diversity (≥ 5 types) / ⚠️ Limited diversity (< 5 types)

---

## Confidence Assessment

**Self-Assessment Scoring:**

### Completeness (25 points)
- [ ] All Stage 1 patterns re-run (10 pts)
- [ ] 5+ new pattern variations tried (10 pts)
- [ ] 10+ files spot-checked (5 pts)

**Score:** [XX]/25

### Accuracy (25 points)
- [ ] N_remaining = 0 OR all documented (10 pts)
- [ ] N_new = 0 (10 pts)
- [ ] All intentional cases verified (5 pts)

**Score:** [XX]/25

### Coverage (25 points)
- [ ] All folders searched (10 pts)
- [ ] All file types included (5 pts)
- [ ] Pattern diversity ≥ 5 types (10 pts)

**Score:** [XX]/25

### Rigor (25 points)
- [ ] Manual reading performed (10 pts)
- [ ] Context analyzed for remaining (10 pts)
- [ ] No assumptions made (5 pts)

**Score:** [XX]/25

**Total Confidence Score:** [XX]/100 ([XX]%)

**Confidence Level:**
- 90-100%: Very High ✅
- 80-89%: High ✅
- 70-79%: Medium ⚠️
- < 70%: Low ❌

**Status:** ✅ Confidence ≥ 80% / ❌ Confidence < 80%

---

## Decision

### Exit Criteria Check (For Stage 5 Decision)

**Stage 4 Complete When ALL True:**

- [ ] All Stage 1 patterns re-run
- [ ] N_remaining = 0 OR only intentional (documented)
- [ ] Tried at least 5 new pattern variations
- [ ] N_new = 0 (no new issues discovered)
- [ ] Spot-checked 10+ random files
- [ ] Spot-checks found zero issues OR issues added to fix list
- [ ] All counts calculated (N_found, N_fixed, N_remaining, N_new)
- [ ] Verification report created
- [ ] Ready to proceed to Stage 5 (Loop Decision)

**Criteria Met:** [N]/9

### Decision Tree

```
IF N_new > 0:
  └─> ❌ LOOP BACK to Round N+1 Stage 1
      Reason: Discovery was incomplete
      Action: Start fresh round with enhanced patterns

IF N_remaining > 0 AND not all intentional:
  └─> ❌ LOOP BACK to Stage 3
      Reason: Fixes incomplete
      Action: Apply missing fixes, re-run Stage 4

IF N_new = 0 AND N_remaining acceptable:
  └─> ✅ PROCEED to Stage 5 (Loop Decision)
      Reason: Verification passed
      Action: Evaluate exit criteria
```

**Final Decision:**
- ✅ **PROCEED to Stage 5** - Verification passed, ready for loop decision
- ❌ **LOOP to Stage 3** - Fix incomplete issues, re-verify
- ❌ **LOOP to Round N+1** - New issues found, need fresh discovery

---

## Issues Requiring Action

### Critical Issues (Must Fix Before Proceeding)

**Issue #1:** [Description]
- **Type:** N_new (new discovery) / N_remaining (unfixed)
- **File:** path/to/file.md
- **Line:** 123
- **Action:** [Fix in Stage 3 / Re-run discovery in Round N+1]

[Repeat for each critical issue]

**Total Critical Issues:** [N]

### Non-Critical (Documented Intentional Cases)

**Intentional #1:** [Description]
- **File:** path/to/file.md
- **Line:** 123
- **Reason:** [Why this is intentional and acceptable]
- **Action:** None (documented and approved)

[Repeat for each intentional case]

**Total Intentional Cases:** [N]

---

## Lessons Learned

**What Worked Well:**
- [Pattern/approach that was effective]
- [Tool/command that found issues]
- [Strategy that saved time]

**What Could Improve:**
- [Pattern we should have tried sooner]
- [Folder we initially overlooked]
- [Variation we missed]

**For Next Round:**
- [Enhanced pattern to try]
- [Different search order]
- [Additional verification step]

---

## Appendix: Commands Reference

**All verification commands run in this stage:**

```bash
# Tier 1: Re-run original patterns
[Command 1]
[Command 2]
...

# Tier 2: New pattern variations
[Command 1]
[Command 2]
...

# Tier 3: Random file selection
find stages templates reference -name "*.md" -type f | shuf -n [N]
```

**Quick re-verification:**
```bash
# Re-run all Tier 1 patterns
[Provide script or command list for quick re-check]
```

---

## Next Steps

**If Proceeding to Stage 5:**
1. Read `stages/stage_5_loop_decision.md`
2. Evaluate all 8 exit criteria
3. Present findings to user
4. Decide: EXIT or LOOP to Round N+1

**If Looping to Stage 3:**
1. Fix all N_remaining errors
2. Apply fixes incrementally
3. Verify each fix
4. Return to Stage 4 and re-verify

**If Looping to Round N+1:**
1. Document why issues were missed
2. Prepare enhanced patterns
3. Take fresh approach
4. Start Round N+1 Stage 1 with better coverage

---

**Status:** [Draft / In Progress / Complete]
**Next Stage:** `stages/stage_5_loop_decision.md` (if passed) OR loop back (if failed)
