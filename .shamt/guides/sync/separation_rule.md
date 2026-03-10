# Shamt Separation Rule

## The Rule

All content in `.shamt/guides/` and `.shamt/scripts/` must be **generic** — applicable to any Shamt project, regardless of tech stack, domain, or conventions. Never write project-specific information into these files.

Project-specific content belongs **exclusively** in `.shamt/project-specific-configs/`. This includes:
- Architecture and coding standards for this project
- Project-specific rules or rule supplements
- Project-specific overrides or extensions to any guide's default behavior
- Lessons learned or audit notes that apply only to this project

**The only exception:** when a shared guide file has been supplemented, that file must contain a pointer note directing the agent to check for the supplement. The pointer is the only project-specific content permitted in a shared guide file. There is no equivalent pointer mechanism for scripts — scripts must be universally applicable as written.

**When in doubt:** if the content would need to change when used in a different project, it is project-specific.

---

## What Goes Where

### Shared (`guides/` and `scripts/`)

- Workflow stages and protocols (S1–S10)
- Reference materials, gates, decision trees
- Templates (generic, with placeholders)
- Debugging, missed requirement, parallel work protocols
- Export, import, and initialization scripts
- The separation rule itself (this file)

### Project-specific (`project-specific-configs/`)

- `ARCHITECTURE.md` — this project's stack, services, data models
- `CODING_STANDARDS.md` — this project's conventions, test commands, formatting rules
- Supplements to guide sections (e.g. project-specific test strategy notes, stage-specific overrides)
- Rules file content that is project-specific
- `init_config.md` — generated at initialization
- Audit notes, exceptions, or findings that apply only to this project

### Never in shared files

- Tech stack specifics ("this project uses Next.js")
- Test commands for this project
- API keys, environment variable names specific to this project
- Language/framework conventions that are project-specific
- Examples drawn from this project's actual codebase

---

## `project-specific-configs/` Folder Structure

`project-specific-configs/` mirrors the guide folder structure. Supplements for a given guide go in the corresponding mirrored directory:

```text
.shamt/project-specific-configs/
  init_config.md                          ← init handoff
  ARCHITECTURE.md                         ← this project's architecture
  CODING_STANDARDS.md                     ← this project's standards
  guides/
    stages/
      s5/                                 ← supplements for s5 guides
      s10/                                ← supplements for s10 guides
    reference/                            ← supplements for reference guides
    ...
```

This means pointer notes reference a predictable directory path, not a specific filename. Any number of supplement files can exist in that directory.

---

## Pointer Convention

Pointers are added to shared guide files **only when a supplement is actually created** — never preemptively.

Once a pointer is added by any child project and exported to master via PR, it flows to all future child projects permanently. This marks the section as a known extension point for all future users.

**Pointer format:**
```markdown
> **Project-specific supplement:** Check `.shamt/project-specific-configs/guides/[mirrored-path]/`
> for any extensions to this section. If none exist for your project, consider whether
> a supplement is appropriate during initialization, S10, or audit.
```

**Placement:** Immediately after the relevant section heading, or at the top of the file if the supplement covers the whole file.

---

## `CHANGES.md` — Tracking Shared File Modifications

When you modify any file in `.shamt/guides/` or `.shamt/scripts/`, record it in `.shamt/CHANGES.md`. This file is used as context for PR reviewers when you export improvements to master.

> **Note:** This applies to child projects only. In master context (no `shamt_master_path.conf` present), the PR description serves this purpose — do not create `CHANGES.md` in the master repo.

**Location:** `.shamt/CHANGES.md`

**Format** (newest entries at top):

```markdown
## YYYY-MM-DD — [brief description]
- Modified: `.shamt/guides/path/to/file.md`
- Reason: [one line]

## YYYY-MM-DD — [brief description]
- Modified: `.shamt/scripts/export/export.sh`
- Reason: [one line]
```

**For rules file template updates** (when back-propagating generic content from your project's rules file to the master template):

```markdown
## YYYY-MM-DD — Rules file template: [section name]
- Modified: `scripts/initialization/RULES_FILE.template.md`
- Rules file section: [section name or brief description]
- Reason: [why this is generic]
```

**When to write CHANGES.md entries:**
- During S10.P1 when applying approved guide improvements
- During audit when fixing guide issues
- Any time you deliberately improve a shared guide or script

**What NOT to record:**
- Modifications to `project-specific-configs/` (those are never exported)
- Automatic substitutions applied by the init script
- Routine work that doesn't change guide content

---

## Enforcement During S10.P1

When applying guide improvements from lessons learned, before writing to any file in `.shamt/guides/`:

1. Confirm the change is generic — would it apply to any Shamt project?
2. If yes → write it to the shared guide file, record in `CHANGES.md`
3. If no → write it to `.shamt/project-specific-configs/guides/[mirrored-path]/`, add a pointer to the shared guide if not already present

---

## Enforcement During Audit

When the audit discovers that a guide file contains project-specific content:

1. Extract the project-specific content
2. Move it to the appropriate `project-specific-configs/guides/[mirrored-path]/` location
3. Add a pointer to the shared guide if not already present
4. Record the change in `CHANGES.md`

---

## Enforcement on Import

After running `import.sh`, during the agent validation loop:

1. For each changed shared guide, check whether your `project-specific-configs/` supplements are still accurate
2. Check whether any pointers in the changed files are still correctly placed
3. Check whether any new extension points in the changed guides warrant new supplements

See `sync/import_workflow.md` for the full post-import validation loop.
