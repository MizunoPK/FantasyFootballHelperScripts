# Old Epic Compatibility Guide

This guide explains how to work with epics that were started **before 2026-01-10** when the file structure changed from `todo.md` (3,896 lines) to the new `implementation_plan.md` (~400 lines) approach.

---

## 🚨 Critical File Changes (2026-01-10)

On 2026-01-10, the epic workflow file structure was significantly updated to improve efficiency and reduce file sizes.

### Quick Identification

**How to quickly identify epic age:**

```bash
ls feature-updates/{epic_name}/feature_01_*/

# If you see: todo.md → Old epic (before 2026-01-10)
# If you see: implementation_plan.md → New epic (after 2026-01-10)
```

---

## Old Epic File Structure (Before 2026-01-10)

```
┌─────────────────────────────────────────────────────────────────┐
│ 🚨 CRITICAL: RESUMING OLD EPICS (Before 2026-01-10)            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ If you see `todo.md` in a feature folder:                       │
│                                                                  │
│ 1. Epic was started BEFORE file structure change               │
│ 2. Use todo.md as reference (don't update it)                  │
│ 3. Don't expect new files (implementation_plan.md, etc.)       │
│ 4. Follow old workflow patterns from README.md Agent Status    │
│                                                                  │
│ If you see `implementation_plan.md`:                            │
│                                                                  │
│ 1. Epic uses NEW workflow (after 2026-01-10)                   │
│ 2. Use implementation_plan.md as PRIMARY reference             │
│ 3. Follow new workflow as documented in current guides         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Old File Structure

**Old epics had:**

```
feature_XX_{name}/
├── README.md                      (Agent Status - current phase, next action)
├── spec.md                        (Requirements specification)
├── checklist.md                   (Questions and decisions)
├── todo.md                        (3,896 lines - comprehensive TODO list)
├── code_changes.md                (Actual changes)
├── lessons_learned.md             (Retrospective)
└── debugging/                     (If issues found)
    └── ...
```

**Key differences:**
- ❌ `todo.md` - Massive file (3,896 lines) with ALL implementation details
- ❌ `checklist.md` - Agents could mark items `[x]` autonomously (old behavior)
- ❌ No `implementation_plan.md`
- ❌ No `implementation_checklist.md`
- ❌ No `questions.md`

---

## New File Structure (After 2026-01-10)

**New epics have:**

```
feature_XX_{name}/
├── README.md                      (Agent Status - current phase, guide, next action)
├── spec.md                        (Requirements specification - user-approved Stage 2)
├── checklist.md                   (QUESTIONS ONLY - user answers ALL before Stage 5a)
├── implementation_plan.md         (Implementation build guide ~400 lines - user-approved Stage 5a)
├── implementation_checklist.md    (Progress tracker ~50 lines - created Stage 5b)
├── code_changes.md                (Actual changes - updated Stage 5b)
├── lessons_learned.md             (Retrospective - created Stage 5c)
└── debugging/                     (Created if issues found during testing)
    ├── ISSUES_CHECKLIST.md
    ├── issue_XX_{name}.md
    └── ...
```

**Key differences:**
- ✅ `implementation_plan.md` - Focused guide (~400 lines) - PRIMARY reference
- ✅ `implementation_checklist.md` - Progress tracker (~50 lines)
- ✅ `questions.md` - Only if NEW questions arise during Stage 5a
- ✅ `checklist.md` - NOW QUESTION-ONLY (agents CANNOT mark `[x]` autonomously)
- ❌ `todo.md` - DELETED, replaced by implementation_plan.md

---

## How to Work with Old Epics

### Step 1: Identify the Epic Age

```bash
# Check for todo.md
ls feature-updates/{epic_name}/feature_01_*/todo.md

# If file exists → Old epic
# If file doesn't exist → New epic (check for implementation_plan.md)
```

---

### Step 2: Read Agent Status

**Location:** `feature_updates/{epic_name}/feature_XX_{name}/README.md`

**Check the "Agent Status" section:**
- Current stage and phase
- Current guide being followed
- Next action to take
- Critical rules

**Example (Old Epic):**
```markdown
## Agent Status

**Current Stage:** Stage 5b (Implementation Execution)
**Current Guide:** `stages/stage_5/implementation_execution.md` (old path)
**Current Phase:** Implementing from todo.md
**Next Action:** Continue implementing tasks from todo.md Section 3.2
**Progress:** 45/120 tasks complete
```

---

### Step 3: Follow Old Workflow Patterns

**If resuming an old epic:**

1. **READ the old guide path** listed in Agent Status
   - Old guide paths may be different (e.g., `implementation_execution.md` instead of `phase_5.2_implementation_execution.md`)
   - Follow the guide referenced in Agent Status

2. **Use todo.md as reference** (PRIMARY reference for old epics)
   - todo.md contains all implementation details
   - Don't update todo.md (it's massive and hard to maintain)
   - Mark progress in README.md Agent Status instead

3. **Don't create new files**
   - Don't create `implementation_plan.md` (epic already uses todo.md)
   - Don't create `implementation_checklist.md`
   - Don't create `questions.md`

4. **Follow checklist.md old behavior**
   - In old epics, agents could mark checklist items `[x]`
   - Continue with this behavior for old epics (don't change mid-epic)

5. **Update Agent Status frequently**
   - Document progress in README.md
   - Track completed todo.md sections
   - Update "Next Action" after each checkpoint

---

### Step 4: Complete the Epic Using Old Workflow

**Continue with the old workflow** until the epic is complete. Don't try to migrate to the new workflow mid-epic.

**After epic completion:**
- Future epics will use the new workflow
- Old epics remain as-is (don't retroactively convert)

---

## When to Use New vs Old Workflow

### Use OLD Workflow (todo.md approach)

**When:**
- Epic was started BEFORE 2026-01-10
- `todo.md` exists in feature folder
- Agent Status references old guide paths

**How:**
- Use `todo.md` as PRIMARY reference
- Follow guide paths from Agent Status
- Don't create new files (implementation_plan.md, etc.)

---

### Use NEW Workflow (implementation_plan.md approach)

**When:**
- Epic started AFTER 2026-01-10
- No `todo.md` in feature folder
- Agent Status references new guide paths (e.g., `phase_5.2_implementation_execution.md`)

**How:**
- Use `implementation_plan.md` as PRIMARY reference during Stage 5b
- Create `implementation_checklist.md` in Stage 5b
- Follow new guide paths (`stages/stage_5/phase_5.2_implementation_execution.md`)

---

## File Roles Comparison

### Old Workflow (Before 2026-01-10)

| File | Role | User Approval | Created When |
|------|------|---------------|--------------|
| `spec.md` | Requirements specification | Stage 2 | Stage 1 |
| `checklist.md` | Questions AND agent decisions | Stage 2 | Stage 1 |
| `todo.md` | Comprehensive implementation guide (3,896 lines) | Stage 5a | Stage 5a |
| `code_changes.md` | Actual changes | No | Stage 5b |

**Key characteristics:**
- `todo.md` is massive (3,896 lines) and hard to navigate
- `checklist.md` allows agent autonomous marking
- No separation between planning and execution tracking

---

### New Workflow (After 2026-01-10)

| File | Role | User Approval | Created When |
|------|------|---------------|--------------|
| `spec.md` | Requirements specification | Stage 2 | Stage 1 |
| `checklist.md` | QUESTIONS ONLY (user answers) | **Gate 3 (Stage 2)** | Stage 1 |
| `implementation_plan.md` | HOW to build (~400 lines) | **Gate 5 (Stage 5a)** | Stage 5a |
| `implementation_checklist.md` | Progress tracker (~50 lines) | No | Stage 5b |
| `questions.md` | NEW questions from Stage 5a | No (optional) | Stage 5a (if needed) |
| `code_changes.md` | Actual changes | No | Stage 5b |

**Key characteristics:**
- `implementation_plan.md` is focused (~400 lines) and user-approved
- `checklist.md` is QUESTION-ONLY (agents CANNOT mark autonomously)
- Clear separation: planning (implementation_plan.md) vs tracking (implementation_checklist.md)
- Two new user approval gates (Gate 3, Gate 5)

---

## Migration Guidance

### ❌ DO NOT Migrate Mid-Epic

**Don't:**
- Convert `todo.md` to `implementation_plan.md` mid-epic
- Switch workflows during active development
- Create new files for old epics

**Why:**
- Risks breaking existing work
- Agents may get confused
- User has already approved old structure

---

### ✅ DO Use New Workflow for New Epics

**When starting a NEW epic after 2026-01-10:**
- Use new workflow from Stage 1
- Follow new guide paths
- Create `implementation_plan.md` in Stage 5a
- Use `checklist.md` QUESTION-ONLY format

---

## Troubleshooting

### Problem: Agent Status references old guide paths

**Symptoms:**
- Guide path: `stages/stage_5/implementation_execution.md`
- Instead of: `stages/stage_5/phase_5.2_implementation_execution.md`

**Solution:**
- This is an old epic
- Read the old guide path (it should still exist or have been renamed)
- Check git history: `git log --follow -- feature-updates/guides_v2/stages/stage_5/implementation_execution.md`
- Follow old workflow patterns

---

### Problem: Conflicting file structure (has both todo.md and implementation_plan.md)

**Symptoms:**
- Feature folder has both `todo.md` and `implementation_plan.md`

**Solution:**
- Check README.md Agent Status to see which file is active
- If Agent Status says "Implementing from todo.md" → Use todo.md
- If Agent Status says "Implementing from implementation_plan.md" → Use implementation_plan.md
- This shouldn't happen, but if it does, Agent Status is authoritative

---

### Problem: Not sure which workflow to use

**Solution:**
1. Check for `todo.md` existence → Old workflow
2. Check for `implementation_plan.md` existence → New workflow
3. Check README.md Agent Status → Authoritative source
4. When in doubt, ask user which workflow was used

---

## See Also

- `CLAUDE.md` - Complete epic development workflow (new version)
- `feature-updates/guides_v2/README.md` - Current guide index
- `feature-updates/guides_v2/reference/glossary.md` - Terminology reference
- `feature-updates/guides_v2/stages/stage_5/phase_5.2_implementation_execution.md` - Stage 5b guide (new version)
