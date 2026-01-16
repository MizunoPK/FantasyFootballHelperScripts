# Implementation Checklist Template

**Instructions for Agents:**
This template is used during S6 (Implementation Execution) to track progress through implementation tasks. Create this file at the START of S6 from the implementation_plan.md task list.

**Key Principles:**
- Simple checkboxes for tracking completion
- Update in real-time as tasks complete
- No detailed documentation (reference implementation_plan.md for details)
- Shows user current progress at a glance

---

## Template

```markdown
# Implementation Progress Checklist

**Feature:** {feature_name}
**Started:** {YYYY-MM-DD HH:MM}
**Status:** {In Progress / Complete}
**Reference:** implementation_plan.md v3.0

---

## Phase 1: {Phase Name} (Tasks {X-Y})

- [ ] Task {N}: {task_name_brief}
- [ ] Task {N}: {task_name_brief}
- [ ] Task {N}: {task_name_brief}

**Phase 1 Status:** {◻️ Not Started / 🔄 In Progress ({m}/{n}) / ✅ Complete}

---

## Phase 2: {Phase Name} (Tasks {X-Y})

- [ ] Task {N}: {task_name_brief}
- [ ] Task {N}: {task_name_brief}
- [ ] Task {N}: {task_name_brief}

**Phase 2 Status:** {◻️ Not Started / 🔄 In Progress ({m}/{n}) / ✅ Complete}

---

## Phase 3: {Phase Name} (Tasks {X-Y})

- [ ] Task {N}: {task_name_brief}

**Phase 3 Status:** {◻️ Not Started / 🔄 In Progress ({m}/{n}) / ✅ Complete}

---

## Mini-QC Checkpoints

- [ ] Checkpoint 1: After Phase {N} ({description})
  - Date: {YYYY-MM-DD HH:MM if complete}
  - Result: {PASSED / FAILED with issues}

- [ ] Checkpoint 2: After Phase {N} ({description})
  - Date: {YYYY-MM-DD HH:MM if complete}
  - Result: {PASSED / FAILED with issues}

- [ ] Checkpoint 3: After Phase {N} ({description})
  - Date: {YYYY-MM-DD HH:MM if complete}
  - Result: {PASSED / FAILED with issues}

---

**Overall Progress:** {m}/{n} tasks complete ({percentage}%)
**Current Phase:** Phase {N} ({Phase Name})
**Current Task:** Task {N} ({task_name_brief})
**Blockers:** {List blockers or "None"}

---

**Last Updated:** {YYYY-MM-DD HH:MM}
```

---

## Usage Notes

**When to create:** Start of S6 (after user approves implementation_plan.md)

**How to populate:**
1. Copy task list from implementation_plan.md
2. Organize by phases (from implementation_plan.md "Implementation Phasing" section)
3. Simplify task descriptions (brief summary only)
4. Add mini-QC checkpoint entries (every 5-7 tasks)

**Update frequency:** After each task completes, mark checkbox and update progress metrics

**File location:** `feature_XX_{name}/implementation_checklist.md`

**Purpose:**
- Agent tracking: Know what's done vs pending
- User visibility: User can see real-time progress
- NOT for details: Reference implementation_plan.md for acceptance criteria, code locations, etc.

---

## Example (Simple Feature)

```markdown
# Implementation Progress Checklist

**Feature:** Add K and DST Support to Ranking Metrics
**Started:** 2026-01-08 20:00
**Status:** In Progress
**Reference:** implementation_plan.md v3.0

---

## Phase 1: Code Changes (Tasks 1-3)

- [x] Task 1: Add K/DST to position_data dict (line 258)
- [x] Task 2: Add K/DST to positions list (line 544)
- [ ] Task 3: Update docstrings (lines 351, 535)

**Phase 1 Status:** 🔄 In Progress (2/3)

---

## Phase 2: Unit Tests (Tasks 4-7)

- [ ] Task 4: test_k_pairwise_accuracy
- [ ] Task 5: test_dst_pairwise_accuracy
- [ ] Task 6: test_top_n_small_sample
- [ ] Task 7: test_spearman_k_dst

**Phase 2 Status:** ◻️ Not Started

---

## Phase 3: Integration Test (Task 8)

- [ ] Task 8: test_end_to_end_with_k_dst

**Phase 3 Status:** ◻️ Not Started

---

## Mini-QC Checkpoints

- [ ] Checkpoint 1: After Phase 1 (code changes)
- [ ] Checkpoint 2: After Phase 2 (unit tests)
- [ ] Checkpoint 3: After Phase 3 (integration)

---

**Overall Progress:** 2/8 tasks complete (25%)
**Current Phase:** Phase 1 (Code Changes)
**Current Task:** Task 3 (Update docstrings)
**Blockers:** None

---

**Last Updated:** 2026-01-08 20:30
```
