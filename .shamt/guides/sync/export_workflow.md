# Shamt Export Workflow

Export is how improvements you've made to shared guides and scripts flow back to the master Shamt repo for distribution to other projects.

---

## When to Export

Export when you have made improvements to files in `.shamt/guides/` or `.shamt/scripts/` that are:

- **Generic** — applicable to any Shamt project, not just this one
- **Deliberate** — an intentional improvement, not an accidental modification
- **Recorded** — documented in `.shamt/CHANGES.md`

Export typically happens after S10.P1 guide updates or after an audit that improved shared guides.

Do not export if all your changes are in `.shamt/project-specific-configs/` — those are project-specific by definition and never exported.

---

## Step 1: Verify Your CHANGES.md Is Current

Before exporting, confirm that `.shamt/CHANGES.md` accurately documents what you changed and why. PR reviewers will use this as context.

If entries are missing, add them now:

```markdown
## YYYY-MM-DD — [brief description]
- Modified: `.shamt/guides/path/to/file.md`
- Reason: [one line]
```

---

## Step 1.2: Compare Your Rules File Against the Template

The rules file (e.g., `CLAUDE.md`, `.github/copilot-instructions.md`) lives outside `.shamt/` and is **not exported automatically** by the export script. Generic improvements you have added to it will not reach other Shamt projects unless you back-propagate them to `RULES_FILE.template.md` in the master repo.

Compare:
- Your rules file (wherever it lives for this AI service)
- `{master_repo}/scripts/initialization/RULES_FILE.template.md`

For each section in your rules file not present in the template, ask: *would this apply to any Shamt project regardless of tech stack?*

**Signs of generic content (back-propagate):**
- Rules about Shamt workflow behavior (validation loops, stage transitions, missed requirements)
- Rules about how agents interact with Shamt system files
- Conventions that apply regardless of language or domain

**Signs of project-specific content (leave in rules file only):**
- References to actual tech stack or test commands (`pytest`, `tsc --noEmit`, etc.)
- Historical context specific to this project
- Your project's epic tag as a literal value rather than `{{EPIC_TAG}}`

**If generic additions exist:**
1. Add the content to `RULES_FILE.template.md` in the master repo
2. Replace your epic tag with `{{EPIC_TAG}}` wherever it appears as a template variable
3. Add a `CHANGES.md` entry (see `sync/separation_rule.md` for format):

```markdown
## YYYY-MM-DD — Rules file template: [section name]
- Modified: `scripts/initialization/RULES_FILE.template.md`
- Rules file section: [section name or brief description]
- Reason: [why this is generic]
```

The template update will be included in the export alongside guide changes.

**If no generic additions:** note "Rules file compared — no template updates needed" and proceed.

---

## Step 1.5: Check for Epic Tag Contamination

Before running the audit, scan the shared guides for your project's epic tag. If it appears inside `.shamt/guides/` files, those are contaminated and must not be exported.

Run this from your project root (substituting your actual epic tag):

```bash
grep -r "YOUR_EPIC_TAG-{N}" .shamt/guides/
# Example: grep -r "KAI-{N}" .shamt/guides/
```

If any matches are found:

1. **Stop** — do not proceed to Step 2 (audit) until these are resolved
2. The matches are guide files where an agent incorrectly replaced the generic `SHAMT-{N}` placeholder with your project's epic tag
3. For each affected file: revert the epic tag substitution back to `SHAMT-{N}`, preserving any other legitimate changes you made to that file
4. Re-run the grep to confirm zero matches before continuing

**What counts as contamination vs. acceptable:**
- ❌ Workflow instruction text with your epic tag instead of `SHAMT-{N}` — revert
- ✅ Attribution comments in file metadata (e.g., "Added from KAI-1 lessons learned") — acceptable, do not revert

---

## Step 2: Run the Full Guide Audit

Before exporting, run the guide audit on the entire `.shamt/guides/` tree (starting from `guides/audit/README.md`). The audit must achieve 3 consecutive zero-issue rounds before you proceed to Step 3.

This step is **mandatory**. Exporting without a full audit risks submitting changes that are internally inconsistent with other guides — cross-references, terminology, or workflow descriptions may need to be updated in files you didn't directly modify.

---

## Step 3: Run the Export Script

From the project root:

```bash
# Preview what would change without modifying master:
bash .shamt/scripts/export/export.sh --dry-run

# Apply the export:
bash .shamt/scripts/export/export.sh

# On Windows:
# & ".shamt\scripts\export\export.ps1" -DryRun   (preview)
# & ".shamt\scripts\export\export.ps1"            (apply)
```

The script:
1. Reads the master path from `.shamt/shamt_master_path.conf`
2. Warns if master's working tree has uncommitted changes (exported files would be mixed with them)
3. Compares your `guides/` and `scripts/` against master by content comparison
4. Copies all differing files to master, and deletes from master any files absent from your child
5. Excludes `guides/audit/outputs/` (your audit history stays local)
6. Prints a summary of what was copied and deleted

Review the output. If files were exported that you didn't intend to change, investigate before opening a PR.

---

## Step 4: Open a PR in shamt-ai-dev

```bash
cd /path/to/shamt-ai-dev

git checkout main
git checkout -b feat/child-sync-YYYY-MM-DD
git add -A .shamt/guides/ .shamt/scripts/
git commit -m "sync: [use the message printed by the export script]"
git push origin feat/child-sync-YYYY-MM-DD
```

The export script prints a ready-to-use commit message in its "Next steps" output — copy it exactly. If `gh` CLI is available, the script also prints a ready-to-run `gh pr create` command.

**PR description template:**

```markdown
## Summary
<!-- Brief description of what improved and why -->

## Changes
<!-- Paste relevant entries from .shamt/CHANGES.md -->

## Source project
<!-- Optional: which project contributed this improvement -->
```

---

## Step 5: PR Review

The master repo maintainer (or agent) reviews the PR diff:

- **Approves** if the changes are genuinely generic and improve the guide system
- **Requests changes** if project-specific content has leaked into shared files
- **Rejects** if the change is specific to your project or contradicts a Shamt design decision

After the PR is merged, the improvement is available to all Shamt projects on their next import.

---

## What Makes a Good Export

**Good to export:**
- A clarification that prevents a common agent mistake
- A new guide section that addresses a workflow gap
- A corrected procedure that was previously wrong or ambiguous
- A new template or reference file

**Do not export:**
- Examples using your project's actual code, filenames, or APIs
- Guide customizations that only make sense for your tech stack
- Test command overrides or language-specific instructions
- Content in `project-specific-configs/` (never exported by the script)

---

## Common Situations

**Export script fails with "Master directory not found":**
`.shamt/shamt_master_path.conf` is stale — the master repo has moved or you're on a different machine. Update the file with the current path to your local `shamt-ai-dev` clone:

```bash
echo "/path/to/shamt-ai-dev" > .shamt/shamt_master_path.conf
```

---

## Relationship to CHANGES.md

`CHANGES.md` is written during S10 and audit work, at the time you make the change. The export workflow uses it at export time. Think of it as the PR description written incrementally as you work.

If you export without a complete `CHANGES.md`, reviewers have no context for the diff. Keep it current.
