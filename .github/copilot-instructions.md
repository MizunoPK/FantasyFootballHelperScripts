# Shamt Rules

**Version:** v2 (template)
**Purpose:** Canonical agent rules — story workflow, the five core patterns, and the three cross-cutting design principles.

> A **template** rendered into a child project's `CLAUDE.md` at install or regen time; generated copies are overwritten. Edit only here, in `shamt-core/templates/`.

---

## What is Shamt?

Shamt is a quality framework for AI-assisted development under Claude Code. It defines **5 core patterns** (validation loops, severity classification, spec protocol, code review, implementation planning) and **two role flows** — an **Engineer flow** (a linear, mandatory-phase story-execution sequence) and a **Product Owner flow** (Epic → Feature → Story decomposition) — with **the story** as the handoff artifact between the two roles. The Engineer flow is load-bearing; the PO flow serves initiatives large enough to warrant top-down decomposition. An opt-in **delivery track** (`flow_track: delivery`) replaces both in a project that selects it, with a single ticket → unit command set (`/dt*`, `/du*`) — a third command **track**, not a third role flow.

Core files:

- `SHAMT_RULES.template.md` — these rules (this file).
- `.shamt-core/README.md` — host-wiring quick reference (commands, skills, personas).
- `reference/` — expanded examples, standards, recipes; `templates/` — artifact skeletons.
- `stories/`, `epics/` — per-story and PO-flow artifacts (folder shape + nesting per **# Ticket IDs** and **§PO-tree resolution**).
- `.shamt-core/proposals/` — framework-update proposals.
- `shamt-config.json` — per-project config (tracker, etc.); work-root-relative (see §PO-tree resolution).

---

# Cross-Cutting Design Principles

These three principles apply to **every** multi-phase flow and every artifact-generation flow Shamt defines.

## Principle 1: Phase-per-command + slug resumability

Every multi-phase flow follows this pattern:

1. **One slash command per phase.** No single mega-orchestrator: a flow's intake, spec and planning phases are separate commands, not steps inside one `/run-story`.
2. **Every command takes a ticket ID or slug.** `/command {id-or-slug}` resolves to exactly one folder via the §PO-tree resolution globs (ID or slug form, work-root-relative); halt if ambiguous (>1) or none. ID/slug forms per **# Ticket IDs**.
3. **Fresh-agent runnable.** A new agent with no conversation history reads the on-disk artifacts under the resolved folder, determines current state from artifact presence (from the re-baseline record in `context.md`, or `active_artifacts.md` for grandfathered stories), and executes the requested phase.
4. **No state file, no orchestrator memory.** State lives in the filesystem. If the prior phase's artifact exists and passes its exit gate, the next phase can run.
5. **Each command is a single skill.** A skill *is* the slash command — invoking a phase command invokes its skill directly, and the same skill also fires on natural-language trigger phrases (e.g. "spec this ticket"). One canonical body, one host wiring; there is no separate `.claude/commands/` mirror.
6. **Context-clear breakpoints between phases.** Encouraged but not enforced. `/clear` between phases keeps context fresh and proves resumability.
7. **Single-session sizing constraint.** Every slug-started command should produce work that fits one session without compaction. If a phase would compact, split further (architect/builder sub-agent, sub-phase decomposition) rather than span compacted sessions; between-session resume uses the slug + on-disk artifacts (per point 3).

## Principle 2: Open-questions iterative dialog

When an agent drafts a new artifact (spec, plan, proposal, epic, feature, story ticket, etc.), open questions are surfaced **one at a time** and answered before the artifact is considered drafted.

1. **Maintain an "Open Questions" section** in the artifact while drafting. Add new questions as they arise.
2. **Present each question to the user via `AskUserQuestion`** (or equivalent). One at a time. Never bulk-bomb.
3. **Update the artifact with the answer before moving to the next question.** The "Open Questions" section shrinks as the artifact firms up.
4. **An artifact is not "drafted" while open questions remain.** Validation cannot start; user approval cannot be requested; the next phase cannot run.
5. **Never proceed on an assumption when a question exists.** If the answer changes the artifact, write it down. If the answer doesn't, record the resolution inline so future agents understand why the question was closable.
6. **A question surfaced to the user is user-owned.** Point 5's self-close applies only to one the agent resolves from code/evidence; a later pass may attach evidence + a *proposed* resolution but may **not** self-close it. The item stays visible marked **`Pending user confirmation`**, blocking validation **exit** (footer) + the spec's **Gate 2b**, not the validation run — so it is **exempt from point 4**. Mechanics in [`reference/validation_exit_criteria.md`](reference/validation_exit_criteria.md) §"User-owned open questions".

Applies to every artifact-generation flow: Engineer-flow Spec / Plan / Review / Polish; PO-flow Epic / Feature / Story definition; framework-update proposals; any v2-original artifact.

## Principle 3: Disk-authoritative cross-session work

Shamt is multi-session and parallel by design: multiple agents author artifacts, run personas, and advance work concurrently. The on-disk artifacts — not any one agent's conversation history — are the authoritative record of work performed.

1. **Disk is the record; the session is not.** An agent reasons about work from on-disk artifacts (proposals/footers/banners, story folders, `feedback/`, the re-baseline record in `context.md` — `active_artifacts.md` for grandfathered stories — the archive/deferred/rejected folders) and git history, never from the assumption that its own session observed everything.
2. **Absence-from-session is not evidence of fabrication.** "I did not perform or observe X this session" does not mean "X never happened." A provenance claim recorded in an artifact (a validation footer, an f0 capture banner, a confirmed-root-cause line, a tracker attribution) is **presumed genuine** — a parallel session did real work this session cannot see.
3. **Verify by reading, never by destroying.** If a cross-session claim genuinely needs verification, the evidence is git history across branches, the cited artifact/folder, or the user — never silent deletion, revert, or rename-back. (The "never halt or revert on unrelated tree state" rules in the framework-update flow's implement and archive phases depend on this.) **This governs the working tree itself, not only artifacts:** a phase owns the files its own work item touches, never the tree; unattributable tree state is halt-and-ask, never repair, and no tree-discarding git command may run against it — [`reference/working_tree_safety.md`](reference/working_tree_safety.md).
4. **This does not relax Pattern 1.** Its adversarial validation still distrusts unsupported *claims about reality* (code, governing docs) and verifies them from evidence, and agents still never fabricate work they did not do. Distrusting a claim about the codebase is in scope; distrusting an artifact's cross-session **provenance** merely because this session didn't author it is not.

---

# Engineer Flow — Phase Map


### §PO-tree resolution

The PO hierarchy nests — features under their epic, stories under their feature. **The layout is one of three, selected by the derived `layout_kind`** (`scripts/layout-kind.sh`, resolved in this order): **`delivery`** when `flow_track == delivery` — a `tickets/{ticketID}-*/units/{ticketID}.{N}-*/` tree, walkthrough in [`reference/delivery_track.md`](reference/delivery_track.md); else **`nested`** when `work_item_tracker == local` — this `epics/` PO tree; else **`flat`** — `features/` is the sole top-level work folder, every story nesting inside a feature record at `features/{featureID}-{slug}-{brief}/stories/{featureID}.{N}-{slug}-{brief}/` (`features/archive/` excluded). The PO flow (`/pe*`/`/pf*`/`/ps*`) is **nested-only**. Nested + flat walkthrough in [`reference/po_tree_resolution.md`](reference/po_tree_resolution.md).

**Resolution contract — all three layouts.** Slug-first commands resolve a folder by a **tree-wide glob** (slugs are globally unique, so the `{slug}-*` tail is unambiguous), **anchored on the altitude's marker file** (`epic.md` / `feature.md` / `ticket.md` / `unit.md`, which is also what disambiguates altitude alongside depth) with `archive/` **excluded**: exactly one match — **halt on zero or multiple**. No legacy fallback. **`{ID}`'s form depends on the layout and the item's origin** (local-only or tracker-backed) — see **# Ticket IDs**.

Throughout command / skill / template / reference bodies, `epics/{slug}/`, `features/{slug}/`, `stories/{slug}/` denote **the resolved folder** (leaf still `…-{brief}/`). All bare `epics/`/`features/`/`stories/`/`code_reviews/`/`shamt-state/`/`shamt-config.json` paths are **work-root-relative** — repo root on self-host, `.shamt-core/` in a child; resolve the work root once via `.shamt-core/`-presence before globbing/writing, and a child writes work-tree artifacts only under `.shamt-core/`.


**Delivery layout — `tickets/` is the sole top-level work folder.** The durable tree is **two levels**, ticket → unit: `tickets/{ticketID}-{slug}-{brief}/{ticket.md,context.md,STATUS.md}` plus `units/{ticketID}.{N}-{slug}-{brief}/unit.md` — the typed **unit replaces the story record**; there is no story or feature altitude. Resolution: `resolve-item.sh ticket` at depth 1 under `tickets/` anchored on `ticket.md`, `resolve-item.sh unit` at depth 3 (`tickets/*/units/*`) anchored on `unit.md`, with `tickets/archive/` + `tickets/*/units/archive/` excluded; `epic` / `feature` / `story` are **n/a**. IDs: a locally-authored ticket = `D{N}` (`next-id.sh dticket`), a pulled ticket = its bare tracker ID (no allocation), every unit = `{ticketID}.{N}` (`next-id.sh unit {ticketID}`). A unit finalizes `**Status: Done**` **in place**; the whole ticket subtree archives to `tickets/archive/` at ticket finalize. Full walkthrough in [`reference/delivery_track.md`](reference/delivery_track.md).

---

# Global Story Invariants

Apply across Spec, Plan, Build, Test, Review, and Polish:

- **Story folder resolution.** Resolve the story folder per §PO-tree resolution (the resolution contract — globs are **work-root-relative**), anchored on `ticket.md`: multiple → halt and ask; none → halt and report.
- **On-disk artifact search discipline.** To locate a work-tree story/epic/feature artifact, resolve the owning folder first (`scripts/resolve-item.sh {altitude} {slug}`, per §PO-tree resolution) and read by that path; never bare-`Glob`/`Grep` an artifact filename (`**/user_test_plan.md`, `**/spec.md`, `**/ticket.md`) — that bypasses the halt-on-ambiguity + `archive/`-exclusion contract and silently matches the archived sibling. When the owning slug is not yet known, the same contract still applies: exclude the `**/archive/**` sibling and halt on zero-or-multiple rather than silently picking one.
- **Baseline resolution.** If `active_artifacts.md` is present, honor its pointer (legacy grandfathered story); otherwise the unsuffixed `{name}.md` is the current baseline.
- **TODO gate.** TODO comments are allowed only for team-discussion placeholders or temporary debug logging that must be removed before merge. Polish cannot complete while any TODO remains in the implementation plan or code. If `.shamt-core/project-specific-files/CODING_STANDARDS.md` is stricter, follow it.
- **Re-baseline rule.** When a post-approval requirement change makes the active spec or plan misleading, stop and create a new baseline instead of patching the old one in place. See the Re-baseline Protocol below.
- **Story branch baseline rule.** Before creating a story branch in any affected repo, fetch the story's **base branch** (the captured `**Base Branch:**` value; default = the configured remote development branch) and create the story branch (name = the captured `**Story Branch:**` value; default = `feature/{slug}/<owner-or-team>`) **from the fetched remote base branch**, never from current local HEAD. Absent/blank markers ⇒ today's exact behavior (base = the configured remote development branch; name = `feature/{slug}/<owner-or-team>`). If the story branch already exists, halt and report. (Exact commands: [`reference/implementation_plan_reference.md`](reference/implementation_plan_reference.md).)
- **Repo layout (`repo_layout`).** When `repo_layout: multi-repo-workspace` (config; default `single-repo`, absent ⇒ `single-repo`) the work root is **not** itself a git repo — never run `git` at the work root. Git/commit/PR ops target the sub-repo(s) named in `ticket.md`'s `**Affected repos:**` field. See [`reference/repo_layout.md`](reference/repo_layout.md).
- **Standards check.** The `.shamt-core/project-specific-files/` docs are governing references for artifacts and reviews. Note absence only if a file does not exist. Doc-silence bounds contested rules only, never "no standard exists."
- **Codebase pattern discovery.** Before surfacing a Gate 2a option recommendation, Plan, Build, Review, or Polish, search for the comparable existing shape, emulate the nearest established one when behaviour is comparable, and document an approved divergence rather than silently inventing a new shape. When that shape is a shared helper, **reuse** it rather than fork or duplicate, and share extractable peer logic rather than copy it; a divergence from the dominant house convention needs an approved reason. A new affordance/entry point for an existing action must **share that action's single owner** — carrying its whole gating contract (visibility, enablement, authorization, ordering) — not fork a partial peer copy implementing only some gating dimensions; a recorded deviation reason permits a genuine divergence. An emulated shape also carries **prose assertions whose truth is not shape-preserved**: re-derive every inherited log / warning / error / comment claim against the new path's actual reachability rather than copying it. This affirmative discover-and-conform duty grounds the convention-evidence and behavioral-contract-mirroring rules — elaborated in [`reference/spec_protocol_reference.md`](reference/spec_protocol_reference.md).

---

# Part 1: Core Patterns

## Pattern 1: Validation Loops

**Purpose:** Iterative self-review until the artifact meets the quality threshold.

**Exit criteria:** every validation is uniform — a **primary clean round + 1 independent adversarial sub-agent confirmation, clean on both its claim-verify and gap-hunt phases** (one sub-agent, two phases: *is what this says true?* and *what does it fail to ask?*; a clean claim pass over an unrun or non-empty gap hunt is not a confirmation). No lower-rigor single-pass tier; the sub-agent always runs (no one-LOW allowance, either phase). The former Quick/Standard rigor selector is retired framework-wide.

### The 8-Step Validation Process

The eight steps — read/investigate, identify issues across dimensions, classify severity, fix immediately, update `consecutive_clean` (clean = zero issues or one LOW fixed), check exit, adversarial sub-agent review (**no one-LOW allowance**; the sub-agent applies the evidentiary bar — verify from *authoritative* tool evidence, not from memory or a tool inauthoritative for the claim class — to the reality-claims *its own* findings rest on, not only the artifact's, per `reference/validation_exit_criteria.md` §Adversarial Review Posture), add footer — have their full per-step mechanics + worked counter examples in [`reference/validation_exit_criteria.md`](reference/validation_exit_criteria.md). The normative dimension lists and footer format stay here:

**Step 2 — dimensions per artifact type** (first check alignment with `.shamt-core/project-specific-files/ARCHITECTURE.md` + `CODING_STANDARDS.md`):

**Specs (8 dimensions):** Completeness; Correctness; Consistency; Helpfulness; Improvements; Missing proposals; Open questions; Standards/architecture alignment. Hard checks per Pattern 3 (the spec-phase command body where that command is generated + [`reference/spec_protocol_reference.md`](reference/spec_protocol_reference.md)).

**Implementation Plans (8 dimensions):** Step clarity; Mechanical executability; File coverage; Operation specificity; Verification completeness; Dependency ordering; Requirements alignment; Naming clarity. Hard checks per the Twenty hard planning checks in [`reference/implementation_plan_reference.md`](reference/implementation_plan_reference.md) (named inline in the plan-phase command body where that command is generated); plus imports listed for a file must be used there.

**Code Reviews (6 dimensions):** Correctness; Completeness; Helpfulness; Severity accuracy; Evidence; Standards/architecture alignment. Hard checks per [`reference/review_categories.md`](reference/review_categories.md): review every changed file/function/branch independently (do not assume parallel files are identical).

**General Artifacts (5 dimensions):** Completeness; Clarity; Accuracy; Actionability; Standards/architecture alignment.

**Step 8 — footer format.** When complete, append the single footer line below; on re-validation **replace** the prior line rather than stacking a fresh one or adding a `Touched` line (history lives in git):

```text
---
Validated {date} — N rounds, 1 adversarial sub-agent confirmed
```

## Pattern 2: Severity Classification

Use the four levels consistently. Quick questions:

1. If not fixed, can the workflow complete? **No** → CRITICAL.
2. Will it cause confusion or wrong decisions? **Yes** → HIGH.
3. Does it noticeably reduce quality / usability? **Yes** → MEDIUM.
4. Otherwise → LOW.

Exactly one LOW issue fixed still counts as a clean primary round. Any sub-agent issue resets validation.

## Pattern 3: Spec Protocol

**Purpose:** Targeted research + design dialog + validated user-facing spec and supporting context. (Exact spec-template section placement lives in the spec-phase command body where that command is generated + `templates/spec.template.md`.)

**Normative contract:** the spec-phase command body where that command is generated (Steps 1–8, Gates 2a/2b, spec-side hard checks); walkthrough + the five validation pair-checks verbatim in [`reference/spec_protocol_reference.md`](reference/spec_protocol_reference.md).

## Pattern 4: Code Review Process

**Purpose:** Structured review with validated, copy-paste-ready feedback.

**Normative contract:** the 16 categories + finding format in [`reference/review_categories.md`](reference/review_categories.md), applied via `agents/review-executor.md`.


## Pattern 5: Implementation Planning

**Purpose:** Create mechanical plans that separate planning from execution.

Every story requires a validated `implementation_plan.md` (Phase 3) after spec approval and before Build — planning is mandatory; no inline-build shortcut.

**Normative contract:** [`reference/implementation_plan_reference.md`](reference/implementation_plan_reference.md) — plan contract, operation contracts, the Twenty hard planning checks — named inline in the plan-phase command body where that command is generated; builder contract in the build-phase command body where that command is generated + `agents/plan-executor.md`; the post-build standards self-audit gate in the test-phase command body where that command is generated, §Step 4c; expanded detail in [`reference/implementation_plan_reference.md`](reference/implementation_plan_reference.md).

---

# Part 2: Token Discipline & Model Selection

Shamt treats token cost as a design constraint. Every flow / persona / phase has a recommended model tier; cheap-tier is used wherever the task is mechanical or zero-bias.

## Operational rules

- Cross-cutting always-on rules (principles, severity, global invariants) live in the rules file; a **phase-specific normative contract lives in that phase's skill body**, which the rules file points to.
- Read the `.shamt-core/project-specific-files/` standards docs once during research and reuse a recorded inline digest.

## Default tier mapping

| Tier | Model | When to use |
|------|-------|-------------|
| **Cheap** | Haiku | File ops, git ops, mechanical execution, sub-agent confirmations, status rollups, intake / freeform ticket capture, test execution |
| **Balanced** | Sonnet | Code reading, structural analysis, spec research, plan creation, medium-complexity validation, formal-mode code-review metadata, user-test-plan authoring |
| **Reasoning** | Opus | Primary validation loops (artifact validation), root-cause analysis, design decisions, multi-dimensional checks, formal-mode review issue-finding, design dialog (Gate 2a), epic/feature decomposition |

Sub-agent confirmations **always** use Cheap tier — these are zero-bias re-reads, not deep reasoning.

## Recommended models per phase (Engineer flow)

The per-phase model tiers for the Engineer flow live in `reference/model_selection.md` (the authoritative table). Personas can override per their definition (see `host/templates/claude/`).


---

# Requirement Re-baseline Protocol

Use a re-baseline when a large requirement change arrives after Gate 2b, Gate 3, or Build execution and the active spec or plan would become misleading: the new baseline is the unsuffixed `{name}.md` and the superseded copy moves to `archive/{name}_{datetime}.md`. When a requirement instead surfaces *after* execution and is genuinely additive, use the **Supplement Protocol** — a scoped `{name}_addendum{N}-{slug}.md` spec + plan beside the baseline — instead. Full trigger lists + both contracts live in [`reference/rebaseline_protocol.md`](reference/rebaseline_protocol.md).

---

# Ticket IDs

Every work item — an epic, feature or story in the nested layout, a feature or sub-story in the flat one, a ticket or unit in the delivery one — is a **ticket** with a short, globally-unique ticket ID, used alongside its slug, in one of **four forms** (the last two layout-scoped). The form is selected by **intake mode** (locally authored vs pulled); *which* local form follows from `layout_kind`:

- **Local-only** — `T{N}` (`T1`, `T2`, …), **nested layout only**. Used with no tracker (`local`/`none`), when the profile's freeform-fallback fires (the slug does not parse to a tracker work-item ID, or the profile lacks the work-item type), or for a decomposition stub written by a decompose or stage-0 draft command.
- **Tracker-backed** — the tracker's own work-item ID (e.g. `3760`), used when the slug parses to one via the profile's `## Slug resolution` and freeform-fallback did not fire. Used **as-is** — no allocation, no max-scan; the tracker owns uniqueness. Applies in **every** layout.
- **Local delivery ticket** — `D{N}` (`D1`, `D2`, …), **delivery layout only**: a locally-authored ticket at `tickets/{ticketID}-*/`. Allocated by `scripts/next-id.sh dticket`; `^D`-anchored, so it is disjoint from `T{N}`, `F{N}` and tracker IDs. Deliberately not `F{N}` — the delivery track has no features. Full detail in [`reference/ticket_ids.md`](reference/ticket_ids.md) §"Fourth ID form".
- **Parent-scoped composite** — `{parentID}.{N}`: the parent ID joined to a per-parent counter by a **`.`**, so the ID carries **no internal `-`**. In this layout the instance is a **delivery unit** `{ticketID}.{N}` (`D7.1`, `4821.2`; `scripts/next-id.sh unit {ticketID}`, §"Fourth ID form").

The forms occupy **disjoint prefix namespaces** — `^T[0-9]+-` (nested local),
`^D[0-9]+-` (delivery local ticket), the `.`-joined composite `{ticketID}.{N}`,
and `^[0-9]+-` (tracker-backed) — so a mixed tree is legal and each max-scan is unaffected by the other prefixes. Because every composite join is a **`.`** (never `-`), **no** ID form contains an internal `-`, so the universal parse **"everything before the first `-`"** is correct for **all** of them — no per-consumer ordering rule; `scripts/resolve-item.sh id-extract` is that parse's canonical helper.

The ID prefixes the folder:

- **Local-prefixed (`T{N}` / `F{N}` / `D{N}`):** `{ID}-{slug}-{brief}/` — a 3-segment shape, mirroring `proposals/{NN}-{slug}.md`.
Delivery: a locally-authored ticket at `tickets/D{N}-{slug}-{brief}/`, its units at `units/{ticketID}.{N}-{slug}-{brief}/`.
All per §PO-tree resolution.
- **Tracker-backed:** `{tracker-id}-{brief}/` — a **2-segment** shape (tracker ID + brief, no separate slug segment), e.g. `3760-efax-parity-option/`.

- **Addressing.** Commands accept the ID (`T{N}` or bare tracker ID), the slug, **or** the paired form (`T{N}-{slug}` or `{tracker-id}-{brief}`), resolved per §PO-tree resolution.
- **Display convention.** Every display that *names* a ticket uses the paired-ID form — `T{N}-{slug}` or `{tracker-id}-{brief}`; never slug-alone, number-alone, or the full folder form. Output only.

The **allocation rule** — a locally-authored ID is a disk **max-scan** (that prefix's existing max across its owning tree, +1; **no counter file**, never reused; layout-scoped allocators, and tracker-backed IDs are never allocated) — plus its traversal mechanics (`epics/archive/` traversal so archived numbers are never reused, Tech-Stories reserved-slug max-scan participation, the post-allocation uniqueness halt-check), the tracker-vs-local decision branch, **new-tickets-only / retroactive-rename posture**, **stub-ID preservation**, and the exhaustive display-convention detail (surface list, slug-alone degradation, ambient-statusline `basename` exemption) all live in [`reference/ticket_ids.md`](reference/ticket_ids.md).

---

# Story Artifact Naming

Core naming rules — three families (full detail in [`reference/rebaseline_protocol.md`](reference/rebaseline_protocol.md)):

- **Baseline** (`spec`, `context`, `implementation_plan`, `user_test_plan`, `test_build_plan`) — the current baseline is the unsuffixed `{name}.md`; the superseded copy moves to `archive/{name}_{datetime}.md` on re-baseline (`datetime` = `YYYY-MM-DDTHHMM`).
- **Supplement** — a scoped post-execution follow-up adds `spec_addendum{N}-{slug}.md` + `implementation_plan_addendum{N}-{slug}.md` beside the live baseline (adds, never replaces).
- **Run-log** — timestamped runs `review_{datetime}.md`, `diagram_{datetime}.html` (plus `agent_test_session_{datetime}.md` under `user_test_plan_mode: agent-run`); resolve the latest by max timestamp. **Append-only after emission**: annotating beneath an existing entry is legal; rewriting, removing or renumbering emitted content is not — a run needing different content emits a new run-log.
- **Grandfather** — existing `_vN` / `active_artifacts.md` stories keep resolving unchanged.
- `test_data/` is an **optional** story-folder artifact — a durable prerequisite-fixture set (seed + provenance/mapping README + the captured batch or a pinned regeneration command) Phase 4 creates when a plan's Setup needs generated/ephemeral fixtures; see `reference/testing.md` §"Setup discipline".

---

# Framework Maintenance

Use the per-phase framework-update commands for changes to canonical framework files; never edit live generated files (`CLAUDE.md`, `.claude/`) directly. Edit canonical sources in `shamt-core/`, run regen, run `-Check` against a known-clean child project, verify semantic consistency and generated sizes, then archive the proposal.

---

*Shamt v2 — two roles, one framework, slug-resumable phases.*

---
Validated 2026-05-26 — 5 rounds, 1 adversarial sub-agent confirmed
