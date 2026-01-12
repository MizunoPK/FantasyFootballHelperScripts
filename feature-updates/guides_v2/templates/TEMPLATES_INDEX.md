# Templates Index

**Last Updated:** 2026-01-02
**Location:** `feature-updates/guides_v2/templates/`

---

## Quick Reference

**When you need a template, find it here by stage or file type.**

---

## Templates by Stage

### Stage 1: Epic Planning

| Template | Filename | Use When |
|----------|----------|----------|
| [Epic README](#epic-readme) | `epic_readme_template.md` | Creating epic folder structure |
| [Epic Ticket](#epic-ticket) | `epic_ticket_template.md` | Validating epic-level understanding (Step 3.6) |
| [Epic Smoke Test Plan](#epic-smoke-test-plan) | `epic_smoke_test_plan_template.md` | Creating initial epic test plan |
| [Epic Lessons Learned](#epic-lessons-learned) | `epic_lessons_learned_template.md` | Creating epic-level lessons document |

### Stage 2: Feature Deep Dive

| Template | Filename | Use When |
|----------|----------|----------|
| [Feature README](#feature-readme) | `feature_readme_template.md` | Creating feature folder |
| [Spec Summary](#spec-summary) | `spec_summary_template.md` | Validating feature understanding (Phase 6) |
| [Feature Spec](#feature-spec) | `feature_spec_template.md` | Writing detailed feature specification |
| [Feature Checklist](#feature-checklist) | `feature_checklist_template.md` | Tracking feature decisions |
| [Feature Lessons Learned](#feature-lessons-learned) | `feature_lessons_learned_template.md` | Creating feature-level lessons document |

### Stage 5a: TODO Creation (Implementation Planning)

| Template | Filename | Use When |
|----------|----------|----------|
| [Implementation Plan](#implementation-plan) | `implementation_plan_template.md` | Creating user-approved build guide through 28 iterations |

### Stage 5b: Implementation Execution

| Template | Filename | Use When |
|----------|----------|----------|
| [Implementation Checklist](#implementation-checklist) | `implementation_checklist_template.md` | Tracking progress during implementation |

### Bug Fix Workflow

| Template | Filename | Use When |
|----------|----------|----------|
| [Bug Fix Notes](#bug-fix-notes) | `bugfix_notes_template.md` | Creating bug fix documentation |

---

## Templates by File Type

### Epic-Level Files

#### Epic README
- **File:** `epic_readme_template.md`
- **Created:** Stage 1
- **Purpose:** Central epic tracking (Agent Status, progress, checklists)
- **Size:** ~260 lines
- **When to use:** Creating epic folder in Stage 1

#### Epic Ticket
- **File:** `epic_ticket_template.md`
- **Created:** Stage 1 - Step 3.6
- **Purpose:** User-validated epic-level outcomes
- **Size:** ~120 lines
- **When to use:** After feature breakdown, before folder creation
- **Critical:** Immutable after user validation

#### Epic Smoke Test Plan
- **File:** `epic_smoke_test_plan_template.md`
- **Created:** Stage 1
- **Updated:** Stage 4, Stage 5e (after each feature)
- **Purpose:** Epic end-to-end testing scenarios
- **Size:** ~270 lines
- **When to use:** Stage 1 initial creation, Stage 4 refinement

#### Epic Lessons Learned
- **File:** `epic_lessons_learned_template.md`
- **Created:** Stage 1
- **Updated:** Throughout all stages
- **Purpose:** Cross-feature insights and guide improvements
- **Size:** ~310 lines
- **When to use:** Stage 1 creation, updated after each stage

---

### Feature-Level Files

#### Feature README
- **File:** `feature_readme_template.md`
- **Created:** Stage 1 or Stage 2
- **Updated:** Throughout Stages 2-5e
- **Purpose:** Central feature tracking (Agent Status, progress)
- **Size:** ~160 lines
- **When to use:** Creating feature folder

#### Spec Summary
- **File:** `spec_summary_template.md`
- **Created:** Stage 2 - Phase 6
- **Purpose:** User-validated feature-level outcomes
- **Size:** ~140 lines
- **When to use:** After multi-phase research, before implementation
- **Critical:** Immutable after user validation

#### Feature Spec
- **File:** `feature_spec_template.md`
- **Created:** Stage 2
- **Purpose:** PRIMARY specification for implementation
- **Size:** ~270 lines
- **When to use:** Writing detailed requirements in Stage 2

#### Feature Checklist
- **File:** `feature_checklist_template.md`
- **Created:** Stage 2
- **Purpose:** Track resolved vs pending decisions
- **Size:** ~95 lines
- **When to use:** Stage 2 deep dive decision tracking

#### Implementation Plan
- **File:** `implementation_plan_template.md`
- **Created:** Stage 5a (accumulated through 28 iterations)
- **Purpose:** User-approved build guide with tasks, tests, edge cases, matrices
- **Size:** ~400 lines (grows from 150→300→400)
- **When to use:** Throughout Stage 5a, user approves after iteration 24

#### Implementation Checklist
- **File:** `implementation_checklist_template.md`
- **Created:** Stage 5b (start of implementation)
- **Purpose:** Live progress tracking with simple checkboxes
- **Size:** ~50 lines
- **When to use:** Create at Stage 5b start, update as tasks complete

#### Feature Lessons Learned
- **File:** `feature_lessons_learned_template.md`
- **Created:** Stage 2
- **Updated:** After Stages 5a, 5b, 5c
- **Purpose:** Feature-specific development insights
- **Size:** ~180 lines
- **When to use:** Stage 2 creation, updated after each substage

---

### Bug Fix Files

#### Bug Fix Notes
- **File:** `bugfix_notes_template.md`
- **Created:** When bug discovered (any stage)
- **Purpose:** User-verified bug description and fix plan
- **Size:** ~85 lines
- **When to use:** Creating bug fix folder during any stage

---

## How to Use Templates

### Step 1: Find the Right Template

Use the tables above to find the template you need based on:
- **Stage:** What stage are you in?
- **File Type:** What type of document do you need to create?

### Step 2: Read the Template

```bash
Read feature-updates/guides_v2/templates/{template_name}.md
```

### Step 3: Copy and Fill In

1. Copy the markdown content from the `## Template` section
2. Replace all `{placeholders}` with actual values
3. Create the file in the correct location (see template header)

### Step 4: Verify Completeness

- Check that NO `{placeholders}` remain
- Verify all required sections are filled
- Update status fields appropriately

---

## Template Metadata Quick Reference

| Template | Lines | Immutable | User Validation Required |
|----------|-------|-----------|-------------------------|
| Epic README | ~260 | No | No |
| Epic Ticket | ~120 | Yes (after validation) | Yes (Stage 1) |
| Epic Smoke Test Plan | ~270 | No | No |
| Epic Lessons Learned | ~310 | No | No |
| Feature README | ~160 | No | No |
| Spec Summary | ~140 | Yes (after validation) | Yes (Stage 2) |
| Feature Spec | ~270 | No | No |
| Feature Checklist | ~95 | No | No |
| Implementation Plan | ~400 | Yes (after validation) | Yes (Stage 5a) |
| Implementation Checklist | ~50 | No | No |
| Feature Lessons Learned | ~180 | No | No |
| Bug Fix Notes | ~85 | Yes (after validation) | Yes |

**Immutable templates:** Epic Ticket, Spec Summary, Implementation Plan, Bug Fix Notes (after user validation)

---

## Common Template Workflows

### Starting a New Epic (Stage 1)

1. ✅ Create epic folder
2. ✅ Use **Epic README** template
3. ✅ Create feature breakdown
4. ✅ Use **Epic Ticket** template (get user validation)
5. ✅ Create feature folders
6. ✅ Use **Epic Smoke Test Plan** template
7. ✅ Use **Epic Lessons Learned** template

### Starting a New Feature (Stage 2)

1. ✅ Use **Feature README** template
2. ✅ Research codebase (multi-phase)
3. ✅ Use **Feature Spec** template
4. ✅ Use **Spec Summary** template (get user validation)
5. ✅ Use **Feature Checklist** template
6. ✅ Use **Feature Lessons Learned** template

### Implementing a Feature (Stage 5a-5b)

1. ✅ Create **Implementation Plan** (Stage 5a - grows through 28 iterations)
2. ✅ Show Implementation Plan to user for approval
3. ✅ Create **Implementation Checklist** from plan (Stage 5b start)
4. ✅ Update checklist as tasks complete

### Creating Bug Fix Documentation

1. ✅ Create `bugfix_{priority}_{name}/` folder
2. ✅ Use **Bug Fix Notes** template
3. ✅ Present to user for validation
4. ✅ Proceed with bug fix workflow (Stages 2 → 5a → 5b → 5c)

---

## Original Comprehensive Reference

The original comprehensive reference file (`templates_v2.md`) has been archived as `templates_v2_ARCHIVE.md` for historical reference. Individual template files are now preferred for:
- Faster access (read only what you need)
- Clearer organization
- Reduced context window usage

---

## Notes

- **Prefer individual templates** over reading the entire archive
- **All templates use markdown format** for consistency
- **Placeholders use `{curly_braces}`** - replace with actual values
- **Some templates are immutable** after user validation (see table above)
- **Templates evolve** based on lessons learned from epics

---

**For questions about templates:** See `EPIC_WORKFLOW_USAGE.md` or `prompts_reference_v2.md`
