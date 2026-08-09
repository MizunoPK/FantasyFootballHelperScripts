---
Last Updated: 2026-08-05
Update History:
  - 2026-07-15: Initial creation — established from master template after framework import; solo / trunk-based, github-automated merge, no deploy environments (slug: project-doc-master-alignment)
  - 2026-07-18: Post-`#187` import refresh — corrected the Phase-6 gating bullet to the `user_test_plan_mode: agent-run` config vocabulary (was the stale "`optional` mode"), and the Review run-log name to `review_{datetime}.md` (was `review_vN.md`)
  - 2026-07-27: Mode C refresh after framework import — added the template's now-**consumed** `Merge strategy` field (`squash`; `/e9` reads it to pick the `gh pr merge` flag under `pr_provider: github`) and corrected the Purpose's stale "reference-only / does not change merge automation" claim; retired the dangling `testing_plan.md` reference and aligned the Phase-6 gating bullet to the `agent-run` required-on-every-story rule (was "optional per story", contradicting TESTING_STANDARDS); `/e9` finalize described as the local `**Status: Done**` marker (tracker status is user-managed); added the missing falsified-clause Update Trigger; corrected "the optional Shamt Phase 7 (Review)" — every phase in the nine-phase Engineer sequence is mandatory, and what this solo project lacks is a *human* approval gate, not the phase (adversarial-validation finding)
  - 2026-08-04: Mode C refresh after framework import — added the template's new `## Rollout safety` section (the delivery track's provision → cutover → contract declarations), filled minimally per the template's own instruction for a project that has never run a staged rollout: merge-implies-deploy **Yes**, no flag mechanism, in-flight observation **n/a** (nothing runs as a service), no drain window, teardown self-authorized. Nothing consumes these fields while this project stays on the default `standard` flow track (`flow_track` is absent from `shamt-config.json`, which resolves to `standard`)
  - 2026-08-05: Rewrote `## Rollout safety` after the user rejected its founding premise. The 2026-08-04 revision read the service-shaped template fields (in-flight observation, drain window) as evidence that staged rollouts do not apply to a project with no service, and declared `Flag mechanism: none`. That is backwards: **a deployment here is a merge to `main`**, which is exactly why the contract stage's irreversibility boundary is real. The section now defines deployment that way up front, declares a REAL flag mechanism grounded in an existing precedent (`--naive-opponents`, `CombinationEvaluator.py:64` / `SweepResultsManager.py:252`, with `SimDataLoader.py:156-161`'s legacy-structure fallback as a second), replaces "in-flight observation" with a three-item **drain-evidence** contract (no caller remains / suite green with the legacy path unreachable / measured-equivalence run at a fixed seed), and adds the worked provision -> cutover -> contract shape for a win-rate-simulator replacement. Also corrected the Purpose, which still described `/e9-finalize-story` and the nine-phase Engineer flow -- both gone since this project moved to `flow_track: delivery`; the consumers are now `/du7-finalize` and `/dt3-design`. The framework-side gate that made the original misreading easy is filed upstream as `proposals/deployment-risk-triggers-assume-a-service-deploy.md`
  - 2026-08-05: Mode C refresh after framework import — the upstream proposal the 2026-08-05 entry above filed has **landed** (shamt-core `#367`, commit `d3536a5`; the local copy moved to `proposals/already-merged/` by this import), so `## Rollout safety`'s "until it lands, evaluate the triggers against the definition above rather than against their infrastructure wording" workaround is discharged and its `proposals/` pointer no longer dangled anywhere active. Replaced with the landed state: the Step-6 trigger set is now anchored on **this project's own `Merge implies deploy:` declaration** rather than on a hosted-service deploy, and carries a seventh disjunctive trigger for the **behavior-preserving replacement of a live path** — so the reading this section argued for is now the framework's own rule. No declaration changed; the template's `in-flight observation method` field independently grew the callsite-census / test-suite-assertion wording this doc's three-item drain-evidence contract already used, so the section needed no realignment
Update Triggers: |
  Update this document when:
  - The merge/approval process changes (who may approve, who may merge, required reviewers)
  - An environment is added, removed, or re-sequenced in the promotion path (e.g. dev/QA → staging → prod)
  - The promotion trigger between environments changes (manual gate, scheduled, automated on green)
  - A gating check is added or removed (required status checks, approvals, sign-offs)
  - Branch or base conventions change (integration branch, release branch, protected branches)
  - When adding an entry, re-read this document's own overview/status/summary prose and flag any clause the new entry falsifies; re-run until a clean pass.
How to Update: |
  Open a delivery ticket (or a framework-update proposal if this is a shamt-core change), follow the
  delivery track, and amend the relevant sections of this file. `/du5-review` (per unit) and
  `/dt7-review` (cross-unit) flag whether a change implies an update; `/du6-polish` / `/dt8-polish`
  applies it and re-validates. `/update-project-doc` is the direct route for a doc-only edit.
  Run `/validate-artifact .shamt-core/project-specific-files/DEPLOYMENT_STANDARDS.md` after
  substantive edits. Keep `Last Updated` current and add an `Update History` entry with the
  triggering ticket/unit or proposal slug.
---

# Project Deployment Standards

**Purpose:** Declare this project's merge and deployment process so the flow has a per-project home
for "how does a change actually ship?" This project runs the **delivery track**
(`flow_track: delivery`), so the consuming stages are `/du7-finalize` (the per-unit merge — one unit,
one PR, one merge) and `/dt3-design` (the per-trigger Deployment Risk evaluation). Two surfaces here
are **consumed, not informational**: the **`Merge strategy`** field drives the `gh pr merge` flag
`/du7` issues (`--squash` / `--merge` / `--rebase`; absent ⇒ `squash`, and this project sets
`pr_provider: github`), and the whole **`## Rollout safety`** section feeds `/dt3-design`'s trigger
evaluation and any `contract` unit's drain evidence.

**Project shape in one line:** this is a **local, single-user Python toolkit** run from a checkout
(see `ARCHITECTURE.md` → Overview). There is **no hosted service, build artifact, container, or
environment promotion path** — "deploy" means "merge to `main`, then pull and run the latest
checkout." The sections below reflect that minimal reality.

---

## Merge process

Who may approve and who may merge a change, and whether the merge is **framework-automated** or
owned by an **external process**.

- **Who approves:** The repository owner (Kai Mizuno) — this is a solo project, so approval is
  self-review. Two reviews run, and they are not redundant: **`/du5-review`** is the 16-category
  sweep over each unit's own diff and is the **gate on that unit's merge**, while **`/dt7-review`** is
  the cross-unit sweep over the assembled rollout *after* every unit has shipped. What is absent here
  is any *human* approval gate: there is **no required second reviewer** and no CODEOWNERS gate.
  (Reviews under the retired nested layout used `review_v1.md` / `review_{datetime}.md` under
  `epics/`; delivery-track reviews land in each unit's own `feedback/`.)
- **Who merges:** The author, via **`/du7-finalize`**, behind its freshness guard, mergeable guard
  and an explicit per-unit confirmation. **The merge is at the UNIT altitude** — one unit, one PR,
  one merge. `/dt9-finalize` is archive-only and merges nothing.
- **Merge automation:** **Framework-automated** (`pr_provider: github`). `/du7` runs
  `gh pr merge --squash --delete-branch` behind those guards. There is no external
  approval/deployment pipeline — the squash-merge into `main` is the terminal ship step, and is
  therefore the irreversibility boundary §Rollout safety is written against.
- **Merge strategy:** **squash** — consumed by `/du7-finalize` (this project is
  `pr_provider: github`) to select the `gh pr merge` flag, here `--squash`. Squash keeps `main` a
  linear one-commit-per-unit history, matching the trunk-based convention below.

---

## Environment sequence

The ordered path a merged change travels from integration to production, and what triggers each hop.

| # | Environment | Purpose | Promotion trigger into the next |
|---|-------------|---------|----------------------------------|
| 1 | Local checkout on `main` | Run in place from the repo root (`.venv/bin/python run_*.py`) by the single user | **terminal** — there is no deploy/promotion step; merging to `main` *is* shipping |

There is a single "environment": the user's local working copy. A merged change reaches "production"
the moment the user pulls `main` and runs the scripts — no build, no artifact publish, no
container/orchestrator, no staging→prod promotion.

---

## Gating checks

The approvals and checks that must pass before a merge is allowed.

- **Full offline test suite green** — `python tests/run_all_tests.py` (100% pass, runs `-m "not
  live_api"`), invoked via `run_pre_commit_validation.py` before committing/merging. This is the
  **single enforced quality gate** (see `CODING_STANDARDS.md` → Lint and Format; there is no
  linter/formatter and no line-coverage threshold).
- **Unit test stage green** — `/du4-test`, recorded in the unit's `testing_results.md`: the whole
  declared automated suite run from `TESTING_STANDARDS.md` §"Automated test infrastructure" (the
  run-source). This blocks the unit's own merge; a fabricated green is forbidden.
- **Ticket-scope test stage green** — `/dt6-execute-tests`, which runs the declared suite **and** the
  ticket-scope `user_test_plan.md` against the assembled change. Because this project sets
  `user_test_plan_mode: agent-run`, that plan is executed by the `user-simulator` and its recorded
  `Session PASS` is a hard green gate. Note this stage runs **after** every unit has merged, so it is
  a post-hoc sweep, not a gate on shipping — which is precisely why `/du5-review` and `/du4-test`
  carry the real gate.
- **No unresolved review threads** on the unit's PR before `/du7-finalize` merges (self-resolved
  during `/du6-polish`).
- **No GitHub CI status checks** — `.github/workflows/` is empty; there is **no** remote CI. The gate
  is entirely the local pre-commit suite above. (If CI is added later, list its required checks here
  and update `Update Triggers`.)

---

## Branch & base conventions

The integration base and any release/protected branches the process depends on.

- **Integration base:** `main`.
- **Release branch(es):** none — **trunk-based**; changes ship straight to `main` (there is no
  `release/*` line and no version tagging process).
- **Protected branches:** `main` — protected **by convention and the Shamt unit-branch flow**
  (all work goes through a unit branch + PR), not by enforced GitHub branch-protection rules on
  this solo repo.
- **Unit branch base:** `main`. Each delivery unit branches **directly off the project default** at
  `/du3-build` (per `unit_branch_pattern`; absent ⇒ the framework default), adapts to base drift
  before building, and targets `main`. There is no shared feature branch and no staging branch — that
  is the remote `/ef*` track's topology, not this one. A delivery **ticket** has no branch at all.

---

## Rollout safety

The per-project declarations a **staged rollout** depends on (`reference/rollout_staging.md` —
provision → cutover → contract). **These fields are live.** This project sets `flow_track: delivery`
(`.shamt-core/shamt-config.json`), so `layout_kind` resolves to `delivery` and the `/dt*` / `/du*`
stages consume them — `/dt3-design`'s per-trigger Deployment Risk evaluation reads them, and a
`contract` unit's spec must cite the drain evidence declared below.

### What "deployment" means here — read this before filling anything in

**A deployment is a merge to `main`.** That is the whole definition, and it is deliberately *not*
narrowed to "a hosted service released to an environment". This project has no service, no
environment promotion, and no in-flight traffic — and staged rollouts still apply to it in full,
because the risk staging manages is **not** "traffic hits a half-deployed service". It is:

> a working path was replaced, and there was a window in which the replacement was live and the
> original was already gone.

That window is reachable in a local toolkit exactly as it is in a distributed system. A merge to
`main` is the point past which the change is what the user runs, so a merge is where
irreversibility lands and where the contract stage's boundary sits.

**The consequence, stated so no future author re-derives the wrong answer:** the fields below being
"n/a-shaped" in service vocabulary (no queues, no drain, no traffic) is **not** evidence that staging
does not apply here. Reading them that way is the error this section was rewritten to correct — the
prior revision declared `Flag mechanism: none` and treated "merging to `main` is shipping" as
grounds for skipping staging. It is grounds for *applying* it. Framework-side this is now settled:
the Step-6 trigger set is anchored on **the project's own declared release boundary** — the `Merge
implies deploy:` field below — rather than on a hosted-service deploy, and it carries a seventh,
disjunctive trigger for the **behavior-preserving replacement of a live path**. So the triggers are
read against the definition above **by the framework's own rule**, not by local workaround.

### The declarations

- **Merge implies deploy:** **Yes** — landing on `main` *is* the deploy. There is no promotion step
  and no separate deploy pipeline (see §Environment sequence). This is what makes a merge the
  irreversibility boundary rather than a later release event.
- **Flag mechanism:** an **opt-in `argparse` `store_true` flag on the affected runner**, defaulting
  to the new path once cutover lands, with the legacy path retained behind the flag until contract.
  This is an existing convention, not an aspiration — the precedent is **`--naive-opponents`** on
  `run_win_rate_simulation.py`, which retains the superseded self-play opponent field
  (`CombinationEvaluator.py:64` — *"False (default) = self-play composition; True = legacy naive"*;
  `SweepResultsManager.py:252`). A second, weaker precedent is a **graceful structural fallback**
  (`SimDataLoader.py:156-161`, which still reads the "legacy flat structure" when the `weeks/` folder
  is absent). Two further mechanisms are available where they fit better: a **config-driven default**
  through `ConfigManager` / `data/configs/` for scoring-parameter changes, and an **unwired entry
  point** — a new module with no caller — for the purely additive case where nothing needs a toggle.
- **Drain evidence — how the old path is shown to be unused** (this is the field the template calls
  *in-flight observation method*; nothing here runs as a service, so the question is not "what is
  still in flight?" but "what still reaches the old path?"). A `contract` unit records, per the
  drain-evidence idiom, **what was checked, when, and what it showed** — never that enough time
  passed. For this project that means all three of:
  1. **No caller remains** — a repo-wide search for the legacy entry point, flag, or symbol returns
     only its own definition and its tests, quoted in the unit's spec.
  2. **The declared suite is green with the legacy path already unreachable** —
     `python tests/run_all_tests.py` (see `TESTING_STANDARDS.md` for the current figure), run *after*
     the cutover and *before* the deletion.
  3. **For a simulation-engine change, a measured-equivalence run** — the same config at a fixed
     `--seed` on both paths, compared exactly. A behaviour-preserving replacement must show an
     identical result, not merely a completing run.
- **Minimum drain window:** **none — drain is observed, not timed.** There is no interval to wait
  out, because there is no traffic to bleed off. The contract stage is authorized by the evidence
  above, and a `contract` unit that cannot produce all three items does not proceed. Solo-project
  convenience is explicitly *not* a reason to skip them: the single user is also the only person who
  would notice a silent regression.
- **Teardown authorization:** the repository owner (Kai Mizuno) — solo project, so authorization is
  self-review, the same posture as §Merge process. Self-review is why the drain evidence is written
  down rather than judged in the moment.

### Worked shape — the case this section was written against

A major replacement of the win-rate simulator's internals, which is the motivating example and the
kind of change most likely to be mis-assessed as "single-PR, no deployment risk":

| Stage | Unit | Obligation |
|---|---|---|
| **provision** | New implementation lands behind the opt-in flag. Old path remains the default and serves every run. | Nothing consumes the new path; a run with no flag is byte-identical to today. |
| **cutover** | Flip the default to the new implementation; the legacy path stays reachable via the flag. | Reversible by flipping back. Observable **by construction** even if output is intended to be identical — the serving path changed. |
| **contract** | The final "rollover" PR deletes the legacy implementation and its flag. | Irreversible, and last. Gated on all three drain-evidence items above. |

Per `reference/rollout_staging.md`, this is a rollout, so it lives inside **one** delivery ticket as
three units — not three tickets.

---

*Template for project `.shamt-core/project-specific-files/DEPLOYMENT_STANDARDS.md` in Shamt. Header metadata block above is required — the framework-update audit reads it.*

---
Validated 2026-08-05 — 2 rounds, 1 adversarial sub-agent confirmed (Mode C refresh after framework import: the Rollout safety workaround for the service-deploy-shaped trigger set was discharged — shamt-core #367 landed it, so the paragraph now states the landed rule (Step-6 triggers anchored on this project's `Merge implies deploy:` declaration, plus the seventh disjunctive behavior-preserving-replacement trigger) instead of a local workaround; sub-agent independently counted the trigger set at seven and confirmed the retired `proposals/` pointer resolves nowhere active)
