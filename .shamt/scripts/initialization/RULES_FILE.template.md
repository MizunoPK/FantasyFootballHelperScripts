# {{PROJECT_NAME}} — Agent Rules

> **This file:** `RULES_FILE.template.md` is renamed and placed during initialization per the AI service being used (e.g., `CLAUDE.md` for Claude Code, `.github/copilot-instructions.md` for GitHub Copilot).

---

## Quick Start for New Agents

**FIRST:** Read `.shamt/project-specific-configs/ARCHITECTURE.md` for complete architectural overview and implementation details.

**SECOND:** Read this file for workflow rules, coding standards references, and commit protocols.

**THIRD:** Check `.shamt/epics/` for any in-progress epic work to resume.

---

## Project Overview

**Project:** {{PROJECT_NAME}}
**Epic Tag:** {{EPIC_TAG}}
**Agent Name:** {{SHAMT_NAME}}
**Git Platform:** {{GIT_PLATFORM}}
**Default Branch:** {{DEFAULT_BRANCH}}

---

## Project Context

**Tech Stack:** [Agent: fill in — language(s), framework(s), key libraries]
**Runtime / Version:** [Agent: fill in — e.g. Node 20, Python 3.12, Go 1.22]
**Package Manager / Build Tool:** [Agent: fill in — e.g. npm, poetry, gradle]
**Test Runner:** [Agent: fill in — e.g. pytest, jest, go test]
**Deployment Target:** [Agent: fill in — e.g. Vercel, AWS Lambda, local only, Docker]

**Critical Gotchas:**
- [Agent: fill in — project-specific things that affect every feature and are easy to get wrong]

---

## Workflow System

This project uses the **Shamt epic-driven development workflow** (S1–S10).

**All guides live at:** `.shamt/guides/`

**Stage overview:**
```
S1: Epic Planning → S2: Feature Deep Dives → S3: Epic-Level Docs, Tests, and Approval →
S4: Feature Testing Strategy → S5-S8: Feature Loop → S9: Epic Final QC → S10: Cleanup

Per-feature: S5 (Plan) → S6 (Execute) → S7 (Test) → S8 (Align) → repeat or S9
```

**Resuming in-progress work:** Check `.shamt/epics/` for active epic folders. Read `EPIC_README.md` → Agent Status section for exact resumption point.

---

## Critical Rules

✅ **Always required:**
- Read guide before starting each stage
- Use phase transition prompts from `.shamt/guides/prompts/`
- Update Agent Status in README files at every checkpoint
- Fix ALL issues immediately (zero tech debt tolerance)
- 100% test pass rate before commits

❌ **Never allowed:**
- Skip any required phase or step within a guide — guides must be executed completely, not selectively
- Defer issues for later
- Commit without running tests
- Autonomous conflict resolution (always escalate to user)
- Replace `SHAMT-{N}` with `{{EPIC_TAG}}-{N}` inside `.shamt/guides/` files — see "Shared Guide Rules" below
- Add code comments, docstrings, or inline explanations to implemented code — see `.shamt/project-specific-configs/CODING_STANDARDS.md` for the no-comment policy and any project-specific exceptions

---

## Parallel Epic Play

When multiple epics are active simultaneously in separate agent windows:

- **S1–S5 (planning):** Multiple agents may proceed independently and in parallel. Each agent operates in its own epic's subdirectory under `.shamt/epics/`. No coordination required.
- **S6–S9 (execution, smoke testing, QC):** Only ONE agent may be in execution at a time. Before starting S6, confirm with the user that no other agent is currently in S6–S9.
- **S10 (completion):** S10 also writes to `EPIC_TRACKER.md`. Two agents completing S10 simultaneously risk a file-level conflict. Treat S10 like S6–S9: only one at a time. Confirm with the user before starting S10 if another agent may also be finishing.

If you are ready to begin S6 or S10 and are unsure whether another agent is at those stages: **STOP and ask the user to confirm it is safe to proceed.**

---

## Guide Execution Protocol

When a guide is referenced for a stage or phase, the following rules apply regardless
of how familiar the task seems:

- **Read the entire guide before starting any work** — the overview does not substitute
  for the full guide including all steps
- **Before executing each step, re-read that step's instructions from the guide** — do
  not execute from memory after an initial read
- **Guide instructions override your training knowledge** — if the guide specifies how to
  perform a step, follow the guide's method even if you know a different approach
- **All phases in a guide are mandatory** — do not stop after the phase that produces the
  primary artifact and skip remaining phases (e.g., completing a draft but skipping the
  validation loop)
- **Do not present outputs to the user until all guide phases are complete**
- **When resuming a prior session:** re-read the current guide before continuing — Agent
  Status indicates where you are, not what the guide requires next

**Bypass pattern to watch for:** "I know how to write an implementation plan / spec /
test strategy, so I'll do it my way." Your knowledge of how to perform the task does not
reduce the requirement to follow the guide's specific steps.

---

## Missed Requirement Protocol (Post-S5)

🚨 **If a new requirement is discovered AFTER S5 has started for any feature:**

- **DO NOT** implement it directly — this is a protocol violation
- **DO** read `.shamt/guides/missed_requirement/missed_requirement_protocol.md` FIRST
- **DO** present options to user (new feature vs update unstarted feature)
- **DO** follow the full protocol: Discovery → Planning → Realignment → S2/S3/S4 → S5-S8

**Trigger keywords:** "missed", "forgot", "should have", "discovered", "gap", "create another feature", "add a feature for", "we also need"

**Decision tree — "NEW, CURRENT, or MISSED?"**
- **NEW** requirement (no epic exists) → S1 epic planning
- **CURRENT** requirement (during S2/S3/S4, before S5) → Update specs in current stage
- **MISSED** requirement (after S5 started) → Missed requirement protocol (`.shamt/guides/missed_requirement/`)

---

## Validation Loop Enforcement (ALL stages)

🚨 **MANDATORY — applies every time a Validation Loop runs (S2, S3, S4, S5, S7, S8, S9)**

**The Validation Loop is the most commonly shortcut protocol. These rules exist because agents consistently:**
- Declare validation "complete" after finding and fixing issues (without achieving 3 CLEAN rounds)
- Skip full artifact re-reads (reading partial sections instead of the entire artifact)
- Skip dimension checklists (finding issues "organically" instead of walking all dimensions)
- Never create the required VALIDATION_LOG.md file
- Treat "issues found and fixed" rounds as clean rounds (they are NOT clean — counter resets to 0)

**Non-negotiable requirements:**

1. **Create VALIDATION_LOG.md BEFORE Round 1.** File: `{feature_folder}/VALIDATION_LOG.md`. Every round must be documented with: timestamp, reading pattern, artifacts re-read (list read_file calls), technical claims verified (list grep/search calls), findings per dimension, round summary with clean counter. If this file does not exist, the validation loop has not started.

2. **Full artifact re-read every round.** Use `read_file` to read the ENTIRE artifact from line 1 to end. Partial reads (e.g., "lines 200-400") do NOT count. If the artifact is >200 lines, read it in 2-3 chunks covering ALL lines. Document the read_file calls in the log.

3. **All dimensions checked every round.** Walk through every dimension checklist (7 master + scenario-specific) and document PASS or ISSUE for each. "I found issues organically" is not sufficient — you must check dimensions you did NOT find issues in too.

4. **Clean counter resets to 0 when ANY issue is found.** A round where you found issues and fixed them is NOT a clean round. The counter only increments on rounds where ZERO issues are found across ALL dimensions.

5. **3 consecutive clean rounds required to exit.** You need counter = 3 (three rounds in a row with zero issues). Typical validation takes 4-7 total rounds. If you're finishing in ≤3 rounds, you are almost certainly doing mechanical validation.

6. **Spot-check technical claims against source code.** Each round must include ≥3 verified technical claims using `read_file`, `grep_search`, or `file_search` against actual source files. Document what you verified and the result.

7. **Never delegate validation rounds to subagents.** The agent running the validation loop must do the reads and checks itself — subagents cannot provide "fresh eyes."

**Self-check before declaring validation complete:**
- [ ] VALIDATION_LOG.md exists with documented rounds
- [ ] Clean counter = 3 (three consecutive zero-issue rounds)
- [ ] Every round has full artifact re-read evidence (read_file calls covering all lines)
- [ ] Every round has all dimensions documented (PASS or ISSUE for each)
- [ ] Every round has ≥3 spot-checked technical claims with tool evidence
- [ ] No round that found issues was counted toward the clean counter

🚨 **TOOL USAGE EVIDENCE — MANDATORY PER ROUND**

Each round in VALIDATION_LOG.md MUST include a "Tool Usage" section listing:
- Every `read_file` call made (file path + line range)
- Every `grep_search` call made (query + result summary)
- Specific findings tied to tool output (not memory)

**Example of compliant round documentation:**
```
Round 3 Tool Usage:
- read_file(implementation_plan.md:1-200) ✓
- read_file(implementation_plan.md:200-400) ✓
- grep_search("{ClassName}") → found at line {N} ✓
- grep_search("{fieldName}") → found at line {N} ✓
Finding: Line {N} uses `{fieldName}` (verified via grep), matches spec requirement R3.
```

**Red flags that indicate fake validation (user will reject and restart from Round 1):**
- Listing dimensions as "✅ PASS" without citing any tool calls
- Using phrases like "I remember..." or "This looks correct from earlier..."
- Finding exactly 1 token issue per round, then declaring clean
- Completing a round in <2 minutes (insufficient time for full re-read)
- No `read_file` or `grep_search` calls visible in the round log

---

## Git Conventions

- **Branch format:** `{work_type}/{{EPIC_TAG}}-{N}` (epic/feat/fix)
- **Commit format:** `{commit_type}/{{EPIC_TAG}}-{N}: {message}`
- **Commit title max:** 100 characters
- **No AI attribution** in commit messages (no Co-Authored-By, no "Generated with")
- **Never force-add gitignored files** — if `git check-ignore` reports a file as ignored, do NOT use `git add -f`. Apply changes locally but skip the commit step.

### Guide File Commit Rule

🚨 **Before committing guide updates (`.shamt/guides/` or the rules file):**

1. Run `git check-ignore .shamt/guides/` to verify guides are NOT ignored
2. If guides ARE gitignored → apply changes locally, skip commit, inform user
3. If guides are NOT gitignored → proceed with `git add` and `git commit`
4. **NEVER use `git add -f` to force-commit gitignored guide files**

---

## PR Review Comment Workflow

**When user provides PR review comments** (copy/pasted or via a file), follow this protocol:

### Input

The user will provide comments in one of two ways:
- **Copy/paste** directly into the chat
- **File** (e.g., a `.txt` export of the review email) — read it with `read_file`

### Processing — One Comment at a Time

Walk through each comment **sequentially** with the user. For each comment:

1. **Present the comment.** Quote the reviewer's concern so both parties are aligned on what's being addressed.

2. **Propose a solution.** Read the relevant source code, analyze the issue, and propose a concrete fix. Explain _what_ you'll change and _why_.

3. **Wait for user confirmation.** Do NOT proceed with implementation until the user confirms the approach. The user may:
   - Approve as-is → proceed
   - Suggest a different approach → adapt and re-propose
   - Decline the fix → skip and move to next comment

4. **Implement the fix.** Apply the code change.

5. **Root-cause analysis.** Reflect on _why_ this issue made it into the PR in the first place. Consider:
   - Was it a gap in coding standards?
   - Was it a missing validation step in the S5–S8 development loop?
   - Was it a pattern the agent should have caught during S9 Final QC?
   - Would a guide update prevent this class of issue in future epics?

6. **Update lessons learned.** Append the issue and root-cause analysis to the epic's lessons learned document at `.shamt/epics/{{EPIC_TAG}}-{N}-{epic_name}/epic_lessons_learned.md`. Each entry should include:
   - Issue number (sequential across all PR review rounds)
   - File and location
   - What the reviewer flagged
   - What was fixed
   - Root cause category (e.g., "unused import", "hardcoded value", "missing validation")
   - Recommended guide update (if applicable)

7. **Repeat** for the next comment.

### After All Comments Are Addressed

1. **Run tests.** Run your project's tests per `CODING_STANDARDS.md` — all must pass before committing.
2. **Commit.** Single commit for the entire round of fixes. Format: `fix/{{EPIC_TAG}}-{N}: address PR review round {R} — {brief summary}`. Do NOT include the review input file in the commit (unstage it if present).
3. **Provide copy/pastable replies.** For each comment, generate a reply the user can paste directly into the PR. Each reply must:
   - Start with "Fixed in {commit_hash}."
   - Briefly describe what was changed and why
   - Be self-contained (one reply per comment, independently copy/pastable)

**Example reply format:**
```
Fixed in {commit_hash}. {Brief description of what was changed and why.}
```

### Reply Format for Non-Review Fixes

When the user addresses feedback that isn't from the automated PR reviewer (e.g., tech lead comments, user-reported bugs), still provide a copy/pastable reply in the same format after committing the fix.

---

## Epic Request Workflow

**CRITICAL:** Understand the distinction between creating an epic request vs starting S1.

### Creating an Epic Request (Before S1)

**When user says:** "Create an epic request for [feature]"

✅ **DO:** Create file in `.shamt/epics/requests/{name}.md` or `.txt`
✅ **DO:** Write comprehensive request document (requirements, goals, constraints, research)
✅ **DO:** Focus on WHAT needs to be done (requirements, not implementation)
✅ **DO:** Mention files/areas that MAY need changes (not specific code)
✅ **DO:** Reference coding practices to follow
✅ **DO:** Leave file in `requests/` folder

❌ **DO NOT:** Include code snippets, detailed schemas, or implementation details
❌ **DO NOT:** Design the exact implementation (that happens during S1-S10)
❌ **DO NOT:** Create `{{EPIC_TAG}}-{N}/` folder yet
❌ **DO NOT:** Create EPIC_README.md yet
❌ **DO NOT:** Create git branch yet

**The request file waits in `requests/` until user initiates S1. The S1-S10 flow will determine detailed design and implementation.**

### Starting S1 Epic Planning (After Request Exists)

**When user says:** "Start S1 for [epic request]"

✅ **DO:** Read `.shamt/guides/stages/s1/s1_epic_planning.md` first
✅ **DO:** Verify request file exists in `.shamt/epics/requests/`
✅ **DO:** Create git branch
✅ **DO:** Assign `{{EPIC_TAG}}-{N}` number
✅ **DO:** Create `{{EPIC_TAG}}-{N}/` folder structure during S1 Step 5

**`{{EPIC_TAG}}-{N}` folders are ONLY created during S1, never before.**

---

## Key File Locations

| File | Location | Purpose |
|------|----------|---------|
| Epic requests | `.shamt/epics/requests/` | Epic request files (BEFORE S1 starts) |
| Epic tracker | `.shamt/epics/EPIC_TRACKER.md` | All epics + next available number |
| Active epics | `.shamt/epics/{{EPIC_TAG}}-{N}/` | Epic folders (CREATED DURING S1) |
| Architecture | `.shamt/project-specific-configs/ARCHITECTURE.md` | Project structure and design |
| Coding standards | `.shamt/project-specific-configs/CODING_STANDARDS.md` | Style, naming, testing rules |
| Project-specific configs | `.shamt/project-specific-configs/` | All project-specific supplements and overrides |
| Guides | `.shamt/guides/` | Full S1–S10 workflow |
| Completed epics | `.shamt/epics/done/` | Archived epics |

---

## Coding Standards

See `.shamt/project-specific-configs/CODING_STANDARDS.md` for complete standards. Key points:
- [Agent: fill in 3–5 key coding rules after analyzing the codebase]

---

## Shared Guide Rules

The files in `.shamt/guides/` are **shared with all Shamt projects** via the export/import sync system. They must stay generic.

**`SHAMT-{N}` is a universal placeholder** — it means "epic number N" in any child project. It does NOT refer to the master Shamt project specifically. When you see `SHAMT-{N}` in a guide, leave it as `SHAMT-{N}`.

❌ **Never do this** in `.shamt/guides/` files:
```text
# Wrong — replaces the generic placeholder with a project-specific tag
git checkout -b feat/{{EPIC_TAG}}-{N}
```

✅ **Leave it as-is:**
```text
# Correct — generic placeholder stays generic
git checkout -b feat/SHAMT-{N}
```

Your project's epic tag (`{{EPIC_TAG}}`) belongs in:
- `.shamt/project-specific-configs/` — project-specific supplements and overrides
- `.shamt/epics/` — your actual epic folders and work products
- Commit messages and branch names for real commits

If you modify a shared guide file for a legitimate reason (adding a clarification, fixing a procedure), keep all `SHAMT-{N}` references intact. Only the content changes — never the placeholder.

---

## Shamt Sync

This project syncs improvements with the master Shamt repo via scripts:
- **Import updates from master:** `bash .shamt/scripts/import/import.sh`
- **Export improvements to master:** `bash .shamt/scripts/export/export.sh` (then open a PR)
- **Log shared file changes:** `.shamt/CHANGES.md` (written by agent during S10/audit work)
- **Sync guide system overview:** `.shamt/guides/sync/README.md`

**When to consider importing:** At the start of a new epic, or if the guides feel stale — check `.shamt/last_sync.conf` for the date of the last import, then run the import script if an update seems warranted.

**If import or export scripts fail with "Master directory not found":** `.shamt/shamt_master_path.conf` is stale (the master repo has moved or you're on a different machine). Update it with the current path to your local `shamt-ai-dev` clone.
