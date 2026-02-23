# Shamt — Initiative Planning Document

**Project Name:** Shamt the AI Dev
**Status:** Planning complete — ready to build
**Origin:** Fantasy Football Helper Scripts project (`FantasyFootballHelperScriptsRefactored`)
**Purpose:** Extract the epic-driven workflow guide system into a standalone, distributable framework that can be initialized in any project. The agent persona using the guides is called "Shamt." Importing the guides into a new project creates a new "version of Shamt."

---

## What We Know

### Concept

"Shamt" is both the name of the framework and the AI agent persona that uses it. When the guides are imported into a new project and initialized, that project gets its own version of Shamt (customized to that codebase). The name "Shamt" is user-customizable per project. The default epic tag is `SHAMT` (customizable at init time).

**Versioning:** A Shamt repo's version is recorded in its `CHANGELOG_INDEX.md`. For the master, this is in `outbound_changelogs/CHANGELOG_INDEX.md` (latest published entry = current version). For a child, it's in `applied_external_changes/CHANGELOG_INDEX.md` (latest applied master changelog = current version). Both master and FF start at version 0.

Shamt is AI-service-agnostic. It maintains a built-in registry (`ai_services.md`) of known AI services and their rules file conventions. When an unrecognized service is encountered during init, the agent works with the user to determine the correct setup, adds it to the registry, then prompts the user: "Should I write a changelog for this so it can be contributed back to master?"

The master Shamt repo has its own `CLAUDE.md` covering: applying child changelogs (audit, versioning), the master dev workflow, and how to update the AI service registry.

There are two separate changelog application guides (not one combined):
- **Master receiving guide:** How the master agent applies an incoming child changelog (evaluate relevance, incorporate improvements, run audit, assign version number, update index)
- **Child applying guide:** How a child agent applies an incoming master changelog (evaluate applicability against local customizations, apply changes; if conflict is found → always escalate to user, never resolve autonomously)

Both `CHANGELOG_INDEX.md` files are updated by the agent as part of the publishing/applying protocols — not a user responsibility.

The master dev workflow guide lives inside `.shamt/guides/` and is distributed to children — because children also reference it when applying incoming master changelogs to their own guides.

The Fantasy Football project will eventually become a child of the Shamt master — adopting the `.shamt/` folder structure going forward with no retroactive changelog required.

---

### Master Repo Structure

```
shamt/                              (repo root — the master Shamt repo)
├── README.md                       (what Shamt is, how to initialize a child)
├── CLAUDE.md                       (active rules file for developing the master Shamt repo)
└── .shamt/
    ├── guides/
    │   ├── stages/                 # Core workflow (s1-s10) — S10 includes changelog writing protocol
    │   ├── reference/              # Gates, common mistakes, glossary, protocols
    │   ├── templates/              # File templates
    │   ├── debugging/              # Debugging protocol
    │   ├── missed_requirement/
    │   ├── prompts/                # Phase transition prompts
    │   ├── parallel_work/          # Parallel work coordination
    │   ├── audit/                  # Modular audit system — includes changelog writing protocol
    │   ├── changelog_application/
    │   │   ├── master_receiving_child_changelog.md   (master applies incoming child changelog)
    │   │   └── child_applying_master_changelog.md    (child applies incoming master changelog)
    │   └── master_dev_workflow/    # Standardized process for updating guides; used by master + children
    ├── initialization/
    │   ├── RULES_FILE.template.md  (AI rules file — renamed/placed during init per AI service)
    │   ├── ARCHITECTURE.template.md
    │   ├── CODING_STANDARDS.template.md
    │   ├── EPIC_TRACKER.template.md
    │   ├── ai_services.md          (registry: known AI services + their rules file conventions)
    │   ├── init.sh                 (Bash — Linux/Mac)
    │   └── init.ps1                (PowerShell — Windows)
    ├── epics/                      (master's own epic work — guide improvement epics)
    │   ├── EPIC_TRACKER.md         (tracks all epics + next available number)
    │   ├── requests/               (incoming improvement requests)
    │   ├── done/                   (archived completed epics)
    │   └── SHAMT-[N]-[name]/       (active epic folders)
    ├── changelogs/
    │   ├── unapplied_external_changes/   (received from children, not yet applied)
    │   └── applied_external_changes/     (received from children, already applied)
    └── outbound_changelogs/
        ├── CHANGELOG_INDEX.md      (master version record + index of all published changelogs)
        └── v0001_[description].md
```

### Child Project Structure (After Initialization)

```
my-project/                         (child project root)
├── CLAUDE.md                       (or AI-service equivalent — placed where user specifies)
├── ARCHITECTURE.md                 (researched + written by agent during init)
├── CODING_STANDARDS.md             (researched + written by agent during init)
└── .shamt/
    ├── init_config.md              (written by script, read by agent, marked complete when done)
    ├── guides/                     (copied from master, customized during init + ongoing)
    ├── initialization/             (copy of init scripts + ai_services.md — kept for reference)
    ├── epics/                      (all epic work for this project)
    │   ├── EPIC_TRACKER.md         (tracks all epics + next available number)
    │   ├── requests/               (initial request files)
    │   ├── done/                   (archived completed epics — max 10)
    │   └── SHAMT-[N]-[name]/       (active epic folders)
    └── changelogs/
        ├── outbound/
        │   ├── CHANGELOG_INDEX.md  (index of child-authored entries + submission status)
        │   └── [entries].md
        ├── unapplied_external_changes/   (from master, downloaded but not yet applied)
        └── applied_external_changes/
            ├── CHANGELOG_INDEX.md  (child version record — latest applied entry = current version)
            └── [applied entries].md
```

**Note on file placement:** During init, the agent asks the user where they want the rules file and support files placed. They don't have to go at the project root.

---

### Core Components

**1. The Master Repo (Shamt)**
- Standalone git repository, public
- Cleaned-up, project-agnostic version of the guides (no FF-specific content)
- `CLAUDE.md` at root: covers applying child changelogs, master dev workflow, AI service registry updates
- Template files in `.shamt/initialization/` (separate from active root files)
- AI service registry (`ai_services.md`) lists known services + rules file conventions
- Receives changelogs from children → master agent applies using `master_receiving_child_changelog.md` guide + auto-runs audit + agent updates index
- Publishes sequentially versioned outbound changelogs; `CHANGELOG_INDEX.md` is the master version record

**2. Child Projects (versions of Shamt)**
- Clone master repo, copy `.shamt/` into project, run init
- Interactive prompts: AI service, epic tag, name override, file placement, git platform, etc.
- If AI service is unrecognized: agent discovers setup with user → adds to registry → prompts user about contributing a changelog back to master
- Agent analyzes codebase, writes support files from scratch (incorporating any existing partial files)
- Guides customized further over time
- Write changelog entries in `.shamt/changelogs/outbound/`; agent updates `outbound/CHANGELOG_INDEX.md`
- Child version tracked in `applied_external_changes/CHANGELOG_INDEX.md`

**3. Changelog / Sync System**

*Child → Master:*
- Child writes structured changelog in `.shamt/changelogs/outbound/`; agent updates `outbound/CHANGELOG_INDEX.md`
- Child maintainer manually provides file to master → placed in `.shamt/changelogs/unapplied_external_changes/`
- Master agent applies using `master_receiving_child_changelog.md` → auto-runs audit → assigns version → agent updates `outbound_changelogs/CHANGELOG_INDEX.md`

*Master → Child:*
- Master publishes to `.shamt/outbound_changelogs/`; agent updates `CHANGELOG_INDEX.md`
- Child maintainer downloads files not already in `applied_external_changes/` (deduplication by filename)
- Files go to `unapplied_external_changes/` → child agent applies using `child_applying_master_changelog.md`
- If conflict found → always escalate to user (never autonomous resolution)
- On completion → moved to `applied_external_changes/`; agent updates `applied_external_changes/CHANGELOG_INDEX.md`

*No automated merges:* Per-project customization makes this unviable.

**4. Initialization System**

The init scripts and agent have clearly separated responsibilities:

*Scripts (`init.sh` / `init.ps1`) prompt for and handle:*

| Prompt | Default | Notes |
|--------|---------|-------|
| AI service | Claude Code | Shows known services list; "Other" triggers agent discovery |
| Epic tag | `SHAMT` | Replaces all placeholder occurrences in templates |
| Shamt agent name | `Shamt` | User-customizable persona name |
| Git platform | GitHub | Determines CLI tool (gh vs glab etc.) and PR/MR terminology |
| Default/main branch | `main` | Used in git commands throughout guides |
| Project name | (required) | Used in EPIC_TRACKER, README header |
| Starting epic number | `1` | First SHAMT-N number; may be higher when onboarding existing project |
| Epic working directory | `.shamt/epics/` | Where epic folders + requests live; inside `.shamt/` |
| Rules file placement | project root | Where CLAUDE.md (or equivalent) goes |

*Scripts also:*
- Create `.shamt/` folder structure and epic working directory
- Copy template files into place
- Perform substitutions throughout templates (epic tag, branch name, project name, etc.)
- Write `.shamt/init_config.md` — handoff file for the agent (see format below)
- Print instructions for the user to start an agent session

*Agent handles (after script completes):*
- Reads `.shamt/init_config.md` to understand what the script configured
- Handles "Other" AI service discovery with user, adds to registry, offers changelog
- Analyzes codebase deeply
- Writes `ARCHITECTURE.md`, `CODING_STANDARDS.md` from scratch (incorporating existing partial files)
- Customizes guides for the project
- Marks `init_config.md` complete when done

*Falls back to guided checklist* when scripts aren't sufficient or user has custom instructions.

**`init_config.md` format (handoff file):**
```markdown
# Shamt Initialization Config

**Generated:** YYYY-MM-DD
**Status:** PENDING_AGENT_COMPLETION

## Project Configuration
- **Project Name:** [name]
- **Epic Tag:** SHAMT
- **Shamt Agent Name:** Shamt
- **Starting Epic Number:** 1
- **Epic Working Directory:** .shamt/epics/

## AI Service
- **Service:** claude_code
- **Rules File Name:** CLAUDE.md
- **Rules File Placement:** project_root

## Git Configuration
- **Platform:** github
- **Default Branch:** main

## Agent Remaining Tasks
- [ ] Handle unknown AI service (if applicable)
- [ ] Analyze codebase
- [ ] Write ARCHITECTURE.md
- [ ] Write CODING_STANDARDS.md
- [ ] Customize guides
- [ ] Complete initialization
```

**5. New Guides to Build**
- **Changelog writing protocol:** Integrated into S10 and Audit guides — when to write, the template, how to assess universality; agent updates `CHANGELOG_INDEX.md` as part of protocol
- **`master_receiving_child_changelog.md`:** How master agent applies incoming child changelogs — evaluate relevance, incorporate, run audit, assign version, update index
- **`child_applying_master_changelog.md`:** How child agent applies incoming master changelogs — evaluate applicability, apply, escalate all conflicts to user, update applied index
- **Outbound changelog versioning protocol:** Agent-driven protocol for assigning sequential version numbers and updating `CHANGELOG_INDEX.md`
- **`master_dev_workflow/`:** Standardized process aligned with S10 lessons-learned approach; distributed to children who also reference it when applying changelogs

---

### Changelog Entry Format

One `.md` file per entry. Filename: `[PROJECT-TAG]-CHANGELOG-[NNN]_[brief-slug].md`

```markdown
# Shamt Changelog Entry

**Entry ID:** [PROJECT-TAG]-CHANGELOG-[NNN]
**Date:** YYYY-MM-DD
**Source Project:** [project name / "master"]
**Author:** [agent or user]

## Guide(s) Affected
- [.shamt/guides/path/to/guide.md] — [what section]

## Change Type
- [ ] Core functionality change (affects workflow steps, gates, or phases)
- [ ] New guide or section added
- [ ] Clarification / wording improvement
- [ ] Bug fix (guide was incorrect or contradictory)
- [ ] Structural/organizational change
- [ ] Other: ___

## Summary
[1-3 sentences: what changed]

## Rationale
[Why this change was made — what problem it solves]

## Universality Assessment
- [ ] Universal — likely beneficial to all Shamt versions
- [ ] Partially universal — see notes below
- [ ] Child-specific — included for awareness only, likely not applicable elsewhere

**Notes:** [context for the applying agent to assess fit for their version]

## How to Apply
[Optional: specific guidance for an agent applying this to a different version of the guides]
```

---

### CHANGELOG_INDEX.md Format

**Master's `outbound_changelogs/CHANGELOG_INDEX.md`:**
```markdown
# Shamt Outbound Changelog Index

**Current Master Version:** v0003

| Version | Date | Summary |
|---------|------|---------|
| v0003 | 2026-03-01 | Add Amazon Q to AI service registry |
| v0002 | 2026-02-25 | Improve S5 validation loop instructions |
| v0001 | 2026-02-20 | Initial release |
```

**Child's `applied_external_changes/CHANGELOG_INDEX.md`:**
```markdown
# Applied External Changes Index

**Current Version:** v0002

| Version | Date Applied | Summary |
|---------|-------------|---------|
| v0002 | 2026-02-28 | Improve S5 validation loop instructions |
| v0001 | 2026-02-22 | Initial release |
```

**Child's `outbound/CHANGELOG_INDEX.md`:**
```markdown
# Outbound Changelog Index

| Entry ID | Date | Summary | Submitted to Master |
|----------|------|---------|---------------------|
| FF-CHANGELOG-002 | 2026-02-25 | Improve S7 restart protocol | Yes |
| FF-CHANGELOG-001 | 2026-02-20 | Add pattern X to S7 | No |
```

---

### AI Service Registry Format (`ai_services.md`)

```markdown
## [Service Name]
- **Rules file name:** [filename]
- **Rules file location:** [path relative to project root]
- **Notes:** [anything special about how this service reads its rules file]
```

Known services to seed the registry with (to be verified during build):
- Claude Code → `CLAUDE.md` at project root
- GitHub Copilot → `.github/copilot-instructions.md`
- Cursor → `.cursorrules` at project root
- Windsurf → `.windsurfrules` at project root
- Amazon Q → TBD

---

## Open Questions

### AJ. Licensing
> *(Deferred)* Should the Shamt master repo be open source? If so, what license?

---

## Decisions Log

| # | Topic | Decision | Date |
|---|-------|----------|------|
| 1 | Repo format | Standalone git repository | 2026-02-20 |
| 2 | Content | Cleaned-up, project-agnostic (no FF-specific content) | 2026-02-20 |
| 3 | Changelog authoring | Manual — child writes entries; master has no git access to children | 2026-02-20 |
| 4 | Master consuming changelogs | Agent reads + applies + auto-audits; no automated merge | 2026-02-20 |
| 5 | Changelog → child distribution | Master publishes sequentially versioned files; child deduplicates by filename | 2026-02-20 |
| 6 | Init UX | Script/tool-first; fall back to guided checklist when needed | 2026-02-20 |
| 7 | Init input method | Interactive prompts | 2026-02-20 |
| 8 | Codebase analysis depth | Agent researches project, writes support files from scratch, incorporates existing partial files | 2026-02-20 |
| 9 | Project name | "Shamt the AI Dev"; agent = Shamt; name is user-customizable | 2026-02-20 |
| 10 | Top-level structure | `README.md` + `CLAUDE.md` + `.shamt/` at root | 2026-02-20 |
| 11 | Template files location | Inside `.shamt/initialization/`; placed during init per user's preferences | 2026-02-20 |
| 12 | Rules file template name | `RULES_FILE.template.md` — renamed during init per AI service convention | 2026-02-20 |
| 13 | AI service support | Built-in registry (`ai_services.md`) + discovery protocol for unknown services | 2026-02-20 |
| 14 | Unknown AI service handling | Agent discovers setup with user → adds to registry → prompts user about contributing changelog | 2026-02-20 |
| 15 | Changelog format | Structured template; one `.md` file per change | 2026-02-20 |
| 16 | Child changelog structure | `outbound/` + `unapplied_external_changes/` + `applied_external_changes/` | 2026-02-20 |
| 17 | Changelog trigger | Write when change affects core guide functionality or benefits other projects | 2026-02-20 |
| 18 | Audit trigger | Automatically runs after agent applies child changelog to master | 2026-02-20 |
| 19 | Outbound changelog versioning | Sequential version numbers (e.g., `v0001_description.md`); agent follows protocol guide | 2026-02-20 |
| 20 | Child deduplication of changelogs | Compare incoming filename against `applied_external_changes/` — skip if already present | 2026-02-20 |
| 21 | Changelog index — master | `outbound_changelogs/CHANGELOG_INDEX.md` is master version record + outbound index | 2026-02-20 |
| 22 | Changelog index — child | `applied_external_changes/CHANGELOG_INDEX.md` is child version record; `outbound/CHANGELOG_INDEX.md` tracks child-authored entries | 2026-02-20 |
| 23 | Shamt versioning model | Version = latest outbound changelog number applied; recorded in `CHANGELOG_INDEX.md` | 2026-02-20 |
| 24 | Init script languages | Bash (`init.sh`) + PowerShell (`init.ps1`) — same functionality in both | 2026-02-20 |
| 25 | Init scripts location | `.shamt/initialization/` | 2026-02-20 |
| 26 | Support file creation | Agent researches codebase, writes files; incorporates existing partial content | 2026-02-20 |
| 27 | "Shamt" in filenames | Yes — appears in folder/file names (e.g., `.shamt/`) | 2026-02-20 |
| 28 | Default epic tag | `SHAMT` (customizable during initialization) | 2026-02-20 |
| 29 | FF project relationship | Becomes a child; adopts `.shamt/` structure going forward; no retroactive changelog | 2026-02-20 |
| 30 | FF + master starting version | Both start at version 0 (no changelogs applied yet) | 2026-02-20 |
| 31 | Existing partial files during init | Agent incorporates them into the newly researched file | 2026-02-20 |
| 32 | Master CLAUDE.md | Covers: applying child changelogs, master dev workflow, AI service registry updates | 2026-02-20 |
| 33 | Changelog writing guide | New protocol integrated into S10 and Audit guides; agent updates index | 2026-02-20 |
| 34 | Changelog application guides | Two separate guides: `master_receiving_child_changelog.md` + `child_applying_master_changelog.md` | 2026-02-20 |
| 35 | Conflict handling (child applying) | Always escalate to user — no autonomous conflict resolution | 2026-02-20 |
| 36 | CHANGELOG_INDEX.md updates | Agent updates as part of publishing/applying protocols — not user responsibility | 2026-02-20 |
| 37 | Outbound versioning protocol | Dedicated protocol guide for assigning version numbers + agent updating index | 2026-02-20 |
| 38 | Master dev workflow guide location | Inside `.shamt/guides/master_dev_workflow/`; distributed to children | 2026-02-20 |
| 39 | Init script scope | Option B — scripts do interactive prompts + scaffolding + substitutions; agent handles codebase analysis, writing, edge cases | 2026-02-20 |
| 40 | Script → agent handoff | Script writes `.shamt/init_config.md`; agent reads it at session start and marks complete when done | 2026-02-20 |
| 41 | Script prompt list | AI service, epic tag, agent name, git platform, default branch, project name, starting epic number, epic working directory, rules file placement | 2026-02-20 |
| 42 | Epic working directory | `.shamt/epics/` — inside the hidden Shamt folder; contains requests/, done/, active epic folders | 2026-02-20 |
| 43 | EPIC_TRACKER.md location | `.shamt/epics/EPIC_TRACKER.md` — collocated with the epic work it tracks | 2026-02-20 |
| 44 | Licensing | Deferred | 2026-02-20 |

---

## Next Steps

*All design decisions finalized. AJ (licensing) is deferred and non-blocking. Ready to build.*

1. **Create master Shamt git repository** — new standalone repo with `README.md`, `CLAUDE.md`, and `.shamt/` folder skeleton
2. **Clean up FF guides** → establish project-agnostic `.shamt/guides/` baseline (strip FF-specific content, replace KAI/ff references with SHAMT/project-generic equivalents)
3. **Write new guides:**
   - Changelog writing protocol (add to S10 + Audit guides)
   - `.shamt/guides/changelog_application/master_receiving_child_changelog.md`
   - `.shamt/guides/changelog_application/child_applying_master_changelog.md`
   - Outbound changelog versioning protocol (version number assignment + index update)
   - `.shamt/guides/master_dev_workflow/` (S10-aligned process for guide updates)
4. **Create template files** in `.shamt/initialization/`:
   - `RULES_FILE.template.md`
   - `ARCHITECTURE.template.md`
   - `CODING_STANDARDS.template.md`
   - `EPIC_TRACKER.template.md`
5. **Seed `ai_services.md`** registry — verify rules file conventions for Claude Code, Copilot, Cursor, Windsurf, Amazon Q
6. **Write `init.sh` and `init.ps1`** — interactive prompts, scaffolding, substitutions, `init_config.md` generation
7. **Write master `CLAUDE.md`** — covering changelog application workflow, master dev workflow, AI service registry updates
8. **Create `CHANGELOG_INDEX.md` templates** for master (`outbound_changelogs/`) and child (`applied_external_changes/`, `outbound/`)
9. **Write master `README.md`** — what Shamt is, how to initialize a child project, how the changelog system works
10. **Retroactively onboard FF project as a child** — adopt `.shamt/` folder structure, no retroactive changelog required
2. Create the master Shamt git repository
3. Clean up FF guides → establish project-agnostic `.shamt/guides/` baseline (remove FF-specific content)
4. Write all new guides:
   - Changelog writing protocol (into S10 + Audit guides)
   - `master_receiving_child_changelog.md`
   - `child_applying_master_changelog.md`
   - Outbound changelog versioning protocol
   - `master_dev_workflow/`
5. Create template files in `.shamt/initialization/`
6. Seed and verify `ai_services.md` registry (confirm known service conventions)
7. Write `init.sh` and `init.ps1`
8. Write master `CLAUDE.md`
9. Create `CHANGELOG_INDEX.md` template files for master and child
10. Write master `README.md`
11. Retroactively onboard FF project as a child (adopt `.shamt/` structure)
