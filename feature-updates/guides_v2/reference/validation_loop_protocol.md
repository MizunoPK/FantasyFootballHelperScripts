# Validation Loop Protocol (Master)

## Purpose
Systematic validation requiring 3 consecutive clean rounds with zero deferred issues.

## Core Principles

### 1. Assume Everything is Wrong
- Start each round assuming document/code is completely wrong
- Look for: inconsistencies, gaps, missing information, errors
- No complacency - treat each validation with skepticism

### 2. Fresh Eyes Each Round
- Take 2-5 minute break between rounds (clear mental model)
- Do NOT rely on memory from previous round
- Approach each round as if reading for first time
- Use different reading patterns/perspectives each round

### 3. Explicit Re-Reading Required
- Must physically re-read the document/code (not work from memory)
- Use Read tool for each round
- Cannot skip re-reading
- Read ENTIRE document/code, not just changed sections

### 4. Research to Fill Gaps
- If gaps found, research to fill them
- Verify against source materials (DISCOVERY.md, epic notes, code)
- Don't guess - look it up
- Cross-reference with related documents

### 5. Exit: 3 Consecutive Clean Loops
- Must have 3 consecutive rounds with ZERO issues/gaps
- NOT cumulative, CONSECUTIVE
- If Round 5 finds issues, need Rounds 6, 7, 8 all clean
- Counter resets when ANY issues found (no matter how minor)

### 6. No Deferred Issues
ALL identified issues must be addressed immediately.

**What "No Deferred" Means:**
- Cannot defer issues for "later" or "future iteration"
- Cannot mark issues as "low priority" to skip fixing
- If issue found in Round N, fix it before Round N+1
- Only exit when ZERO issues remain (not "acceptable number")
- "Good enough" is never good enough - aim for zero defects

**Why This Principle:**
- Deferred issues accumulate into technical debt
- "Later" never comes - issues compound
- Small issues become big bugs
- Quality cannot be retrofitted
- User requested: "Accept no deferred issues"

**Example:**
```bash
Round 1: Find 5 issues → Fix ALL 5 before Round 2
Round 2: Find 2 issues → Fix ALL 2 before Round 3
Round 3: Find 1 issue → Loop back, fix it, restart count to 0
Round 4: Find 0 issues → Continue (count = 1 clean)
```markdown

Cannot proceed with known issues, no matter how minor.

**Important Note About Fixes:**
Fixing an issue can introduce new issues. This is expected and handled by the protocol:

**Example:**
```bash
Round 1: Find typo in spec.md requirement R1 → Fix typo
Round 2: Re-read spec → Notice R1 fix made it contradict R2 → This is a NEW issue
Round 2 outcome: 1 issue found (R1/R2 contradiction)
Action: Fix contradiction before Round 3, reset counter to 0
Round 3: Re-read spec → Check if fix introduced other issues
```markdown

**Key Insight:** The "restart counter" behavior handles fix-induced issues naturally. Don't be discouraged if fixes introduce new issues - that's why we have multiple rounds with fresh eyes.

### 7. Maximum Round Limit (Safety Mechanism)

**Escalation Protocol for Stuck Loops:**

If Validation Loop exceeds 10 rounds without achieving 3 consecutive clean loops:

1. STOP the loop
2. Document all issues found in last 3 rounds
3. Escalate to user with summary:
   - "I've completed 10+ rounds of validation"
   - "Issues continue to be found: [list recurring pattern]"
   - "I need help deciding how to proceed"
4. Await user guidance

**Rationale:**
- 10 rounds = ~2-3 hours of validation work
- If issues persist after 10 rounds, there's likely a fundamental problem
- Human judgment needed to assess: architecture issue? scope issue? misunderstanding?
- Prevents infinite loops and wasted agent time

**User Options After Escalation:**
- Adjust scope/approach
- Accept current state (override "no deferred" for specific issues)
- Return to earlier stage (S1 Discovery, S2 Research, etc.)
- Provide additional context/clarification

---

## Embedded Gates Explanation

**What "Embedded" Means Operationally:**

When a gate is "embedded" in a Validation Loop, the gate criteria become issue types that the loop checks for:

- **Gate criteria failures = Issues found**
- **If gate check fails in Round 1 → Fix → Continue loop**
- **Exit requires gate criteria passing (not separate checkpoint)**

**Example - Gate 1 Embedded in S2.P1.I1:**
- Round 1 checks: Gate 1 criteria (can cite files? read code? verified structures?)
- If any Gate 1 criterion fails → Issue found → Fix it
- Round 2 checks Gate 1 again (along with other issues)
- Exit requires: Gate 1 passes + no other issues + 3 consecutive clean

**Contrast with Separate Gate:**
- **Embedded gate:** Validation dimension within loop (agent self-validates)
- **Separate gate:** Explicit STOP point requiring user approval (user decides)
- Gate 3 (User Approval) stays separate (requires user decision)
- Gates 1 & 2 become embedded (agent validates during loop)

---

## The 3-Round Loop

### Round 1: Initial Validation
**Goal:** Find obvious issues

**Process:**
1. Re-read document/code completely
2. Check for completeness, consistency, gaps
3. Document ALL issues found
4. Report: "Round 1: N issues found"

**If N > 0:** Fix ALL issues (no deferring), proceed to Round 2
**If N = 0:** Proceed to Round 2 anyway (need 3 consecutive clean)

### Round 2: Different Perspective
**Goal:** Find issues missed in Round 1

**Process:**
1. Take 2-5 minute break (clear mental model)
2. Re-read ENTIRE document/code (not just fixed sections)
3. Use DIFFERENT search/reading patterns than Round 1
4. Look for NEW issues (not just verify fixes)
5. Document ALL issues found
6. Report: "Round 2: N issues found"

**If N > 0:** Fix ALL issues (no deferring), proceed to Round 3
**If N = 0:** Proceed to Round 3 anyway (need 3 consecutive clean)

### Round 3: Final Sweep
**Goal:** Confirm zero issues remain

**Process:**
1. Take 2-5 minute break (fresh perspective)
2. Re-read ENTIRE document/code again
3. Use DIFFERENT search/reading patterns than Rounds 1 & 2
4. Random spot-checks
5. Document ALL issues found
6. Report: "Round 3: N issues found"

**If N > 0:** Fix ALL issues, continue to Round 4, RESET counter to 0
**If N = 0:** Check consecutive clean count (increment by 1)

**Exit Criteria:**
- 3 consecutive rounds with ZERO new issues each
- Rounds N-2, N-1, N all found zero issues
- Only then: Mark as PASSED

### Example: Round 5 Finds Issues

```text
Round 1: 5 issues → fix ALL → Round 2
Round 2: 2 issues → fix ALL → Round 3
Round 3: 0 issues → Round 4 (count = 1 clean)
Round 4: 0 issues → Round 5 (count = 2 clean)
Round 5: 1 issue → fix it → Round 6, RESET count to 0
Round 6: 0 issues → Round 7 (count = 1 clean)
Round 7: 0 issues → Round 8 (count = 2 clean)
Round 8: 0 issues → PASSED (count = 3 consecutive clean)
```

**Key:** Counter resets when ANY issues found (no matter how minor)

---

## Context-Specific Adaptations

Different contexts will adapt this protocol by defining:

1. **WHAT is being validated** (document, code, test plan, spec)
2. **WHAT counts as "issue"** (gaps, inconsistencies, missing requirements, etc.)
3. **WHAT patterns differ per round** (sequential read vs reverse vs spot-check)
4. **WHAT specific criteria** (Gate checklists, coverage thresholds, alignment checks)

**See context-specific guides:**
- `validation_loop_discovery.md` - Research and discovery context
- `validation_loop_spec_refinement.md` - Spec/document refinement context
- `validation_loop_alignment.md` - Cross-feature/cross-doc alignment context
- `validation_loop_test_strategy.md` - Test plan validation context
- `validation_loop_qc_pr.md` - QC and PR validation context

Each context guide will:
- Reference this master protocol
- Define context-specific validation criteria
- Provide examples for that context
- Specify round-to-round pattern variations

---

## Common Patterns Across Contexts

### Round 1 Patterns (Common)
- Sequential reading (top to bottom)
- Completeness checks (all sections present?)
- Obvious gap identification

### Round 2 Patterns (Common)
- Reverse reading (bottom to top)
- Cross-reference validation
- Consistency checks (contradictions?)

### Round 3 Patterns (Common)
- Random spot-checks
- Edge case identification
- Final sweep with fresh perspective

---

## Anti-Patterns to Avoid

### ❌ Working from Memory
**Wrong:** "I remember I checked this in Round 1, so I'll skip it in Round 2"
**Right:** Re-read ENTIRE document each round

### ❌ Deferring Minor Issues
**Wrong:** "This is a minor typo, I'll fix it later"
**Right:** Fix ALL issues immediately, no matter how minor

### ❌ Stopping at 3 Rounds
**Wrong:** "I've done 3 rounds, I'm done"
**Right:** Need 3 CONSECUTIVE CLEAN rounds (may require 5, 10, or more total rounds)

### ❌ Batching Fixes
**Wrong:** "I'll fix all issues from Rounds 1-3 at once"
**Right:** Fix all issues from Round N before starting Round N+1

### ❌ Skipping Re-Reading
**Wrong:** "I only changed one line, I don't need to re-read everything"
**Right:** Re-read ENTIRE document every round (fixes can introduce new issues)

---

## Success Metrics

**A Validation Loop is successful when:**
- ✅ 3 consecutive rounds found zero issues each
- ✅ All identified issues fixed (zero deferred)
- ✅ All embedded gate criteria passed
- ✅ Document/code meets quality standards
- ✅ Agent has high confidence in completeness

**A Validation Loop has failed when:**
- ❌ 10 rounds completed without 3 consecutive clean
- ❌ Recurring issues indicate fundamental problem
- ❌ Agent stuck in fix-introduces-issue cycle
- ❌ Escalation to user required

---

**This is the master protocol. All Validation Loop implementations must follow these 7 principles.**

**Context-specific guides adapt HOW these principles are applied, not WHETHER they are applied.**
