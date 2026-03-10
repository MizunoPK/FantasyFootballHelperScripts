# D16: Duplication Detection — Real Examples

Real examples of D16 violations and fixes, organized by pattern type.

**Referenced from:** `d16_duplication_detection.md` → "Real Examples" section

---

## Example 1: Critical Rules Duplicated Across 8 Guides

**Issue Found During SHAMT-7 Audit:**

**Duplication:**
```markdown
# S2, S3, S4, S5, S6, S7, S8, S9 all had identical section:

## Critical Rules

1. Always read guide before starting
2. Use mandatory phase transition prompts
3. Update Agent Status after each phase
4. Zero tech debt tolerance
5. Fix all issues immediately
```

**Problem:**
- 8 files with same content
- If rules change, must update 8 files
- High maintenance burden

**Solution:**

**Created:** `reference/critical_workflow_rules.md`

**All guides updated to:**
```markdown
## Critical Rules

See `reference/critical_workflow_rules.md` for universal workflow rules.

**Stage-Specific Rules:**
- [Stage-specific rules here]
```

**Result:**
- Single source of truth
- Updates in one place
- Guides focus on stage-specific rules

**Root Cause:** Copy-paste for consistency without consolidation

**How D16 Detects:**
- Type 1: Exact Duplicate Content
- Type 5: Entire Section Duplication
- Automated: CHECK 19 detects identical sections

---

## Example 2: Git Instructions Duplicated in S1 and S10

**Issue Found During Documentation Review:**

**S1 Guide:**
```markdown
## Step 1.1: Create Git Branch

Create branch using format: {work_type}/SHAMT-{number}

Where work_type is:
- epic: For epic-level work
- feat: For feature additions
- fix: For bug fixes

Command: `git checkout -b epic/SHAMT-{number}`
```

**S10 Guide:**
```markdown
## Create Pull Request

Ensure you're on correct branch format: {work_type}/SHAMT-{number}

Where work_type is:
- epic: For epic-level work
- feat: For feature additions
- fix: For bug fixes

Use: `git checkout -b epic/SHAMT-{number}` if needed
```

**Problem:**
- Branch naming rules duplicated
- Git commands duplicated
- Should reference GIT_WORKFLOW.md

**Solution:**

**Both guides updated to:**
```markdown
See `reference/GIT_WORKFLOW.md` for branch naming and git commands.
```

**Result:**
- Git workflow in one canonical location
- Guides reference, don't duplicate

**Root Cause:** Reference material embedded in guides instead of extracted

**How D16 Detects:**
- Type 3: Redundant Instructions Across Guides
- Automated: CHECK 20 counts instruction occurrences

---

## Example 3: Missing Import Example in 5 Guides

**Issue Found During Example Review:**

**S5, S6, S7, S9, Debugging Protocol all had:**
```markdown
### Example: Missing Import Error

**Problem:** Code fails with "ModuleNotFoundError: No module named 'pandas'"
**Cause:** Missing import statement
**Solution:** Add `import pandas as pd` at top of file
**Result:** Code executes successfully
```

**Problem:**
- Same example in 5 places
- If example needs updating (e.g., better debugging tip), must update 5 files

**Solution:**

**Created:** `reference/common_examples.md`

**Included:**
- Missing Import Error
- Logic Error Examples
- Configuration Error Examples
- Common Debugging Patterns

**Guides updated to:**
```markdown
### Example: Missing Import

See `reference/common_examples.md` → "Missing Import Error" for debugging approach.
```

**Result:**
- Examples in one location
- Guides reference by name
- Easy to maintain and expand

**Root Cause:** Examples not extracted to shared library

**How D16 Detects:**
- Type 4: Duplicate Examples Across Guides
- Manual validation: Compare example content

---

## Example 4: Template Boilerplate Never Customized

**Issue Found During Feature Spec Review:**

**Template:** `templates/feature_spec_template.md`
```markdown
## Common Pitfalls

1. Forgetting to run tests before committing
2. Skipping user approval gates
3. Not updating Agent Status regularly
4. Deferring issues for later
5. Skipping validation loops
```

**All 12 features in SHAMT-7 had identical "Common Pitfalls" section.**

**Problem:**
- Generic pitfalls, not feature-specific
- Template content never customized
- Should be reference material

**Solution:**

**Template updated to:**
```markdown
## Common Pitfalls

[List feature-specific pitfalls discovered during implementation]

**See:** `reference/common_pitfalls.md` for general workflow pitfalls
```

**Existing features:**
- Generic content removed
- Feature-specific pitfalls added

**Result:**
- Feature specs have feature-specific content
- Generic content in reference file

**Root Cause:** Template created generic content without customization prompt

**How D16 Detects:**
- Type 7: Template Content Propagation
- Manual validation: Check if template instances identical

---

## Example 5: Prerequisites Boilerplate in All Stage Guides

**Issue Found During Stage Guide Review:**

**All 10 stage guides started with:**
```markdown
## Prerequisites

Before starting this stage:

- [ ] Read the complete guide using Read tool
- [ ] Use mandatory phase transition prompt from prompts_reference_v2.md
- [ ] Verify prerequisites checklist
- [ ] Update Agent Status in README with current guide path
- [ ] THEN proceed with work
```

**Problem:**
- Same 5 items in all guides
- If standard prerequisite process changes, must update 10 files

**Solution:**

**Created:** `reference/standard_prerequisites.md`

**Stage guides updated to:**
```markdown
## Prerequisites

**Standard Prerequisites:**
See `reference/standard_prerequisites.md`

**Stage-Specific Prerequisites:**
- [ ] Completed [Previous Stage]
- [ ] [Stage-specific file] exists
- [ ] [Stage-specific approval] received
```

**Result:**
- Standard prerequisites in one place
- Guides focus on stage-specific prerequisites
- Clear separation

**Root Cause:** Standard boilerplate not extracted to shared reference

**How D16 Detects:**
- Type 5: Entire Section Duplication
- Automated: CHECK 19 detects identical Prerequisites sections

---

**Last Updated:** 2026-02-06
**Version:** 1.1
