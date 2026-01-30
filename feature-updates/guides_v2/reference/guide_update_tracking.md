# Guide Update Tracking - Lessons Applied to Guides

**Purpose:** Track which lessons learned from epics have been applied to guides, enabling pattern analysis and continuous improvement

**Use Case:** After each epic's S10.P1, document approved guide updates to maintain history and identify patterns

---

## Overview

This document tracks the feedback loop from implementation → lessons learned → guide updates:

1. **Epic completes** → Generates lessons_learned.md files
2. **Agent analyzes lessons** → Creates GUIDE_UPDATE_PROPOSAL.md
3. **User approves changes** → Agent applies to guides
4. **Agent logs here** → Creates traceable history

**Benefits:**
- Visibility into guide evolution over time
- Pattern detection across multiple epics
- Accountability for applied vs rejected changes
- Evidence of continuous improvement

---

## Applied Lessons Log

**Format:** Epic | Priority | Lesson Summary | Guide(s) Updated | Date | Commit Hash

| Epic | Priority | Lesson Summary | Guide(s) Updated | Date Applied | Commit |
|------|----------|----------------|------------------|--------------|--------|
| KAI-1 (external) | P0 | Code Inspection Protocol - agents rushed through QC without reading actual code | s7_p2_qc_rounds.md | 2026-01-30 | dd10778 |
| KAI-1 (external) | P1 | External Dependency Verification - assumed libraries work without testing | s1_p3_discovery_phase.md, s2_p1_research.md, s5_p1_i3_integration.md | 2026-01-30 | dd10778 |
| KAI-1 (external) | P3 | Shell Script Best Practices - missing set -e caused silent failures | reference/shell_script_best_practices.md (NEW) | 2026-01-30 | dd10778 |
| KAI-7-improve_debugging_runs | P0 | Debugging Active Detection - new agents missed active debugging | CLAUDE.md, debugging_protocol.md, epic_readme_template.md | 2026-01-23 | pending |
| KAI-7-improve_debugging_runs | P0 | Zero Tolerance for Errors - agent marked errors as "environment issue" | smoke_testing_pattern.md | 2026-01-23 | pending |
| KAI-7-improve_debugging_runs | P1 | Make implementation_checklist.md creation first step in S6 | s6_execution.md | 2026-01-23 | pending |
| KAI-7-improve_debugging_runs | P2 | Windows File Locking in logging tests | s7_p1_smoke_testing.md | 2026-01-23 | pending |

**Instructions:**
- Add one row per lesson applied (even if multiple guides updated)
- If one lesson updates multiple guides, list all guides in "Guide(s) Updated" column
- Include commit hash for traceability
- Keep sorted by date (newest first)

---

## Pending Lessons

**Format:** Lessons identified but not yet applied (awaiting user approval or deferred)

| Epic | Priority | Lesson Summary | Proposed Guide(s) | Status | Reason Pending |
|------|----------|----------------|-------------------|--------|----------------|
| {Example - delete after use} |
| KAI-2-example | P2 | Add example of integration gap | s5_p1_planning_round1.md | User Discuss | Needs clarification on example format |

**Instructions:**
- Add lessons where user marked "Discuss" and hasn't yet approved
- Remove from this section once approved and moved to "Applied Lessons Log"
- If lesson is rejected, move to "Rejected Lessons" section

---

## Rejected Lessons

**Format:** Lessons user rejected with rationale (helps avoid re-proposing same changes)

| Epic | Priority | Lesson Summary | Proposed Guide(s) | Date Rejected | User Rationale |
|------|----------|----------------|-------------------|---------------|----------------|
| {Example - delete after use} |
| KAI-3-example | P3 | Add typo fix | workflow_diagrams.md | 2026-01-10 | Too minor, not worth guide churn |

**Instructions:**
- Document all rejected proposals to avoid re-proposing
- Include user's rationale to understand why rejected
- Helps identify proposals that consistently get rejected

---

## Pattern Analysis

**Purpose:** Identify common lesson patterns across epics to drive systematic guide improvements

### Pattern 1: {Pattern Name}

**Observed In:**
- KAI-{N}-{epic_name} - {brief description}
- KAI-{N}-{epic_name} - {brief description}
- KAI-{N}-{epic_name} - {brief description}

**Root Cause:**
{Why this pattern keeps appearing}

**Guide Impact:**
- {Guide 1} - {How updated to address pattern}
- {Guide 2} - {How updated to address pattern}

**Status:** {Fully Addressed / Partially Addressed / Monitoring}

**Next Steps:**
{What additional changes might be needed}

---

### Pattern 2: {Pattern Name}

{Same structure...}

---

## Metrics

**Epic Guide Update Statistics:**

| Metric | Count | Notes |
|--------|-------|-------|
| Total epics completed | 2 | Since guide update workflow started (1 internal + 1 external) |
| Epics with guide updates | 2 | 100% of total |
| Total proposals created | 7 | Across all epics |
| Total proposals approved | 6 | 85.7% approval rate (1 was modified) |
| Total proposals rejected | 0 | 0% rejection rate |
| Total proposals modified | 1 | 14.3% modification rate (P1-1 expanded to multi-stage) |

**Approval Rate by Priority:**

| Priority | Proposed | Approved | Approval Rate | Notes |
|----------|----------|----------|---------------|-------|
| P0 (Critical) | 3 | 3 | 100% | Target: >80% |
| P1 (High) | 2 | 2 | 100% (1 modified) | Target: >60% |
| P2 (Medium) | 1 | 1 | 100% | Target: >40% |
| P3 (Low) | 1 | 1 | 100% | Target: >20% |

**Most Frequently Updated Guides:**

| Guide | Updates | Last Updated | Notes |
|-------|---------|--------------|-------|
| {guide_name.md} | {N} | {YYYY-MM-DD} | {Why frequently updated} |
| {guide_name.md} | {N} | {YYYY-MM-DD} | {Why frequently updated} |
| {guide_name.md} | {N} | {YYYY-MM-DD} | {Why frequently updated} |

**Common Lesson → Guide Mappings:**

| Lesson Type | Typical Guide(s) Updated | Count |
|-------------|--------------------------|-------|
| Spec misinterpretation | 5.1.3.3_round3_part2b.md (Iteration 25) | {N} |
| Interface verification missed | s5_p1_planning_round1.md (Iteration 2) | {N} |
| Algorithm traceability incomplete | s5_p1_planning_round1.md (Iteration 4) | {N} |
| Integration gap not identified | s5_p1_planning_round1.md (Iteration 7) | {N} |
| Test coverage insufficient | s5_p2_planning_round2.md (Iterations 8-10) | {N} |
| Gate not enforced | mandatory_gates.md | {N} |
| QC round missed issue | qc_rounds.md | {N} |

---

## Usage Notes

### For Agents

**After S10.P1 (Guide Update Workflow):**
1. For each approved proposal, add entry to "Applied Lessons Log"
2. For each modified proposal, add entry with user's modification
3. For each rejected proposal, add entry to "Rejected Lessons" with rationale
4. Update metrics section (counts, approval rates)
5. Look for patterns: if same lesson appears 2+ times, create Pattern Analysis entry

### For Users

**Reviewing this document:**
- Check "Applied Lessons Log" to see what improvements have been made
- Review "Pattern Analysis" to understand systemic improvements
- Check metrics to see if approval rates match expectations
- Use "Rejected Lessons" to understand why certain proposals were declined

**Quarterly review:**
- Every 10-20 epics, review Pattern Analysis
- Identify if certain guides need major restructuring vs incremental updates
- Determine if workflow is generating valuable proposals

---

## Maintenance

**Update frequency:**
- After every epic's S10.P1 (Applied Lessons Log, Pending, Rejected)
- Monthly: Update metrics section
- Quarterly: Update pattern analysis, identify systemic improvements

**Quality checks:**
- Ensure commit hashes are accurate and traceable
- Verify all approved lessons are logged (none missing)
- Check that patterns are actionable (not just observations)
- Confirm metrics calculations are correct

---

## History

**Document Created:** 2026-01-11
**Last Major Update:** 2026-01-30
**Total Lessons Tracked:** 7 (4 from KAI-7, 3 from KAI-1 external)

---

## Examples (DELETE AFTER FIRST REAL USE)

### Example: Applied Lesson Entry

**Epic:** KAI-1-improve_draft_helper
**Priority:** P0
**Lesson:** "Iteration 25 (Spec Validation Against Validated Documents) caught that spec.md misinterpreted epic notes about week_N+1 folder logic. Epic said 'create week folders' but spec said 'no code changes needed for folders.' Gate prevented week+ of rework."
**Guide Updated:** `reference/mandatory_gates.md`
**Changes Made:**
- Added historical context to Gate 3 (Iteration 25)
- Emphasized importance of three-way comparison (epic notes, epic ticket, spec summary)
- Added example of spec misinterpretation caught by this gate
**Date Applied:** 2026-01-10
**Commit Hash:** abc1234

**Guide Updated:** `stages/s5/5.1.3.3_round3_part2b.md`
**Changes Made:**
- Added emphasis to "close spec.md and implementation_plan.md" step
- Added "ask critical questions" examples specific to folder/file operations
- Added success story showing gate catching misinterpretation
**Date Applied:** 2026-01-10
**Commit Hash:** abc1234

---

**End of Examples**
