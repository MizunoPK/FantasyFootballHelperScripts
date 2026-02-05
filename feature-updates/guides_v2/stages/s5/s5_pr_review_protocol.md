# PR Review Protocol (Hybrid Multi-Round Approach)

**Purpose:** Systematic PR review using fresh agent context to catch issues before committing.

**Applies to:**
- Feature-level PRs (S7 Phase 3)
- Epic-level PRs (S9 Phase 3)

**Key Principle:** Spawn fresh agents for each review round to avoid context bias and ensure "fresh eyes" on the code.

---

## Prerequisites

**Before starting Iteration Review:**

- [ ] Previous iterations complete
- [ ] implementation_plan.md exists
- [ ] Working directory: Feature folder

**If any prerequisite fails:** Complete missing iterations first

---

## Overview

**What is this iteration?**
Iteration Review: PR Review

---

## Overview: Hybrid Approach

**Round 1: Specialized Reviews** (4 different fresh agents)
- Code Quality Review
- Test Coverage Review
- Security Review
- Documentation Review

**Rounds 2-5: Repeated Comprehensive Reviews** (1 fresh agent per round)
- Full systematic review using complete checklist
- Continue until 2 consecutive rounds with ZERO issues
- Maximum 5 rounds total

---

## File Structure

Create `pr_review_issues.md` in the appropriate location:
- **Feature-level:** `feature_XX_{name}/pr_review_issues.md`
- **Epic-level:** `KAI-{N}-{epic_name}/pr_review_issues.md`

**Template:** See `templates/pr_review_issues_template.md`

---

## Round 1: Specialized Reviews

**Goal:** Systematic review from 4 different expert perspectives.

### Round 1a: Code Quality Review

**🚨 SPAWN FRESH AGENT** with this task:

```markdown
Review the following code changes for code quality issues:

**Review Focus:**
- [ ] Naming: Variables, functions, classes follow project conventions
- [ ] Structure: Logical organization, appropriate abstraction
- [ ] Duplication: No copy-paste code, DRY principle followed
- [ ] Complexity: Functions are single-purpose, not overly complex
- [ ] Style: Follows project coding standards (see CLAUDE.md)
- [ ] Type hints: All functions have proper type annotations
- [ ] Imports: Properly organized (standard, third-party, local)

**Code to review:**
{Provide git diff or file paths}

**Report ALL issues found** in this format:
- File: {path}:{line}
- Issue: {description}
- Severity: High/Medium/Low
- Fix: {suggested fix}
```

**Agent deliverable:** List of code quality issues (or "No issues found")

### Round 1b: Test Coverage Review

**🚨 SPAWN FRESH AGENT** with this task:

```markdown
Review the following code changes for test coverage issues:

**Review Focus:**
- [ ] Coverage: >90% line coverage for new/modified code
- [ ] Edge cases: All edge cases have dedicated tests
- [ ] Error paths: All error handling code is tested
- [ ] Mocking: External dependencies properly mocked
- [ ] Test quality: Tests are independent, use AAA pattern
- [ ] Assertions: Tests have meaningful assertions
- [ ] Test data: Fixtures used appropriately

**Code to review:**
{Provide git diff or file paths}
{Provide test file paths}

**Report ALL issues found** in the same format as Round 1a.
```

**Agent deliverable:** List of test coverage issues (or "No issues found")

### Round 1c: Security Review

**🚨 SPAWN FRESH AGENT** with this task:

```markdown
Review the following code changes for security issues:

**Review Focus:**
- [ ] Input validation: All user input validated
- [ ] SQL injection: No string concatenation in queries
- [ ] Path traversal: File paths properly validated
- [ ] Command injection: No shell commands with user input
- [ ] XSS: Output properly escaped (if applicable)
- [ ] Authentication: Proper auth checks (if applicable)
- [ ] Authorization: Proper permission checks (if applicable)
- [ ] Secrets: No hardcoded credentials or API keys
- [ ] Dependencies: No known vulnerable dependencies

**Code to review:**
{Provide git diff or file paths}

**Report ALL issues found** in the same format as Round 1a.

**IMPORTANT:** If ANY security issues found, mark as severity: High
```

**Agent deliverable:** List of security issues (or "No issues found")

### Round 1d: Documentation Review

**🚨 SPAWN FRESH AGENT** with this task:

```markdown
Review the following code changes for documentation issues:

**Review Focus:**
- [ ] Docstrings: All public functions/classes have docstrings
- [ ] Docstring accuracy: Docstrings match actual implementation
- [ ] Type hints: Match docstring descriptions
- [ ] Comments: Complex logic has explanatory comments
- [ ] No stale comments: No outdated or misleading comments
- [ ] README updates: User-facing changes documented (if applicable)
- [ ] ARCHITECTURE updates: Architectural changes documented (if applicable)

**Code to review:**
{Provide git diff or file paths}

**Report ALL issues found** in the same format as Round 1a.
```

**Agent deliverable:** List of documentation issues (or "No issues found")

---

## Consolidate Round 1 Results

**After all 4 specialized reviews complete:**

1. **Consolidate issues** into `pr_review_issues.md` (use template)
2. **Categorize by severity:** High, Medium, Low
3. **Check for multi-approach issues:**
   - If ANY issue has multiple valid solutions → **ESCALATE TO USER**
   - Use AskUserQuestion to present options and get decision
   - Update pr_review_issues.md with user decision

4. **If issues found:**
   - Fix ALL issues (following user decisions if escalated)
   - **RESTART PR review from Round 1a** (spawn fresh agents again)
   - Update pr_review_issues.md with "Fixed" status

5. **If NO issues found:**
   - Mark Round 1 as PASSED in pr_review_issues.md
   - Proceed to Round 2

---

## Rounds 2-5: Repeated Comprehensive Reviews

**Goal:** Continue reviewing with fresh eyes until 2 consecutive rounds find ZERO issues.

### Round N Process (N = 2, 3, 4, 5)

**🚨 SPAWN FRESH AGENT** with this task:

```bash
Perform a comprehensive PR review of the following code changes:

**Context:** This is Round {N} of PR review. Previous rounds found issues that were fixed. Your job is to find ANY remaining issues with fresh eyes.

**Complete Review Checklist:**

**Code Quality:**
- [ ] Naming: Variables, functions, classes follow conventions
- [ ] Structure: Logical organization, appropriate abstraction
- [ ] Duplication: No copy-paste code, DRY principle
- [ ] Complexity: Single-purpose functions, not overly complex

**Testing:**
- [ ] Coverage: >90% line coverage
- [ ] Edge cases: All edge cases tested
- [ ] Error paths: All error handling tested
- [ ] Test quality: Independent tests, AAA pattern

**Security:**
- [ ] Input validation: All user input validated
- [ ] No injection vulnerabilities (SQL, command, XSS)
- [ ] No hardcoded secrets
- [ ] Dependencies: No known vulnerabilities

**Documentation:**
- [ ] Docstrings: All public functions documented
- [ ] Accuracy: Docstrings match implementation
- [ ] Comments: Complex logic explained

**Spec Alignment:**
- [ ] All requirements in spec.md implemented
- [ ] No extra functionality not in spec
- [ ] Acceptance criteria met

**Implementation Plan Alignment:**
- [ ] All tasks in implementation_plan.md completed
- [ ] Implementation matches planned approach
- [ ] No deviations without good reason

**Tech Debt:**
- [ ] No TODO, FIXME, or XXX comments
- [ ] No commented-out code
- [ ] No temporary/debug code
- [ ] No print statements (unless intentional)

**Performance:**
- [ ] No obvious inefficiencies (N+1 queries, etc.)
- [ ] Appropriate data structures used
- [ ] No unnecessary loops or computations

**Code to review:**
{Provide git diff or file paths}
{Provide spec.md path}
{Provide implementation_plan.md path}

**Report ALL issues found** in the standard format:
- File: {path}:{line}
- Issue: {description}
- Severity: High/Medium/Low
- Fix: {suggested fix}

**CRITICAL:** Be thorough. If you find ANYTHING that could be improved, report it.
```

**Agent deliverable:** List of issues (or "No issues found")

### After Each Round

1. **Update pr_review_issues.md** with round results

2. **Check for multi-approach issues:**
   - If ANY issue has multiple valid solutions → **ESCALATE TO USER**
   - Get user decision
   - Update pr_review_issues.md with decision

3. **If issues found:**
   - Fix ALL issues
   - Increment round counter
   - **If round < 5:** RESTART from next round (spawn fresh agent)
   - **If round = 5:** ESCALATE TO USER (couldn't get clean after 5 rounds)

4. **If NO issues found:**
   - Check if previous round also had no issues
   - **If yes (2 consecutive clean rounds):** PR REVIEW PASSED ✅
   - **If no (first clean round):** Continue to next round

---

## Completion Criteria

**PASSED:** 2 consecutive rounds with ZERO issues (can happen as early as Rounds 1→2)

**ESCALATE TO USER:**
- Reached 5 rounds without 2 consecutive clean rounds
- Present pr_review_issues.md history to user
- Let user decide: continue reviews, manual fix, or approve as-is

---

## Integration with Workflow

### Feature-Level (S7 Phase 3)

**In final_review.md Step 1 "Create PR review checklist":**
- READ: `stages/s5/s5_pr_review_protocol.md`
- Follow protocol completely
- Create `pr_review_issues.md` in feature folder
- Cannot proceed to Step 2 until PR review PASSED

### Epic-Level (S9 Phase 3)

**In epic_final_qc.md Step 1 "Epic PR Review":**
- READ: `stages/s5/s5_pr_review_protocol.md`
- Follow protocol completely
- Create `pr_review_issues.md` in epic folder
- Review all changes across ALL features in epic
- Cannot proceed to Step 2 until PR review PASSED

---

## Key Principles

1. **Fresh Eyes:** Every review round uses a new agent (via Task tool)
2. **Systematic:** Use complete checklist every round
3. **Zero Tolerance:** Cannot proceed with known issues
4. **User Escalation:** Multi-approach issues go to user immediately
5. **Repeated:** Fix and restart until clean
6. **Documented:** All issues and fixes tracked in pr_review_issues.md

---

## Example pr_review_issues.md Structure

```markdown
# PR Review Issues Tracker

## Round 1a: Code Quality Review
**Status:** PASSED / FAILED
**Agent ID:** {task_id}
**Issues Found:** {count}

### Issue 1
- **File:** league_helper/PlayerManager.py:145
- **Issue:** Variable name `tmp` is not descriptive
- **Severity:** Low
- **Fix:** Rename to `filtered_players`
- **Status:** Fixed / Open / User Decision Pending

---

## Round 1b: Test Coverage Review
...

## Completion Summary
- **Total Rounds:** {N}
- **Total Issues Found:** {count}
- **All Issues Fixed:** Yes/No
- **Final Status:** PASSED / ESCALATED TO USER
```


## Exit Criteria

**Iteration Review complete when ALL of these are true:**

- [ ] All tasks in this iteration complete
- [ ] implementation_plan.md updated
- [ ] Agent Status updated
- [ ] Ready for next iteration

**If any criterion unchecked:** Complete missing items first

---
---

## Notes

- **Time estimate:** Round 1 (4 agents) ~15-20 minutes, each subsequent round ~5 minutes
- **Expected rounds:** Most PRs should pass in 2-3 rounds after Round 1
- **Cost:** Higher token usage due to fresh agents, but significantly improves quality
- **Historical evidence:** Similar approach (QC rounds) in S7 has high issue detection rate
