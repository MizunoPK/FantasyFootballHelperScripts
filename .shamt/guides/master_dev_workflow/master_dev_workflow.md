# Master Dev Workflow — Guide Improvement Process

This guide defines the standardized process for improving the master Shamt guides directly (as opposed to receiving improvements via a child project PR).

Use this when:
- You've identified a gap, error, or improvement opportunity in the master guides
- You're making structural changes to the guide system
- You're adding new guides or sections

This process is intentionally lighter than the full S1-S10 epic workflow. It's aligned with S10's lessons-learned update approach.

---

## When to Use This vs. the Full Epic Workflow

| Scope | Use |
|-------|-----|
| Single guide fix, clarification, or small addition | This workflow |
| New guide section (< 1 guide file) | This workflow |
| New guide files or significant restructuring | Full epic workflow (S1-S10) with SHAMT epic tracking |
| Multi-guide cross-cutting changes | Full epic workflow |

---

## Step 1: Define the Change

Before touching any files, write a one-paragraph description of:
- What the current guide says (or doesn't say)
- What the problem or gap is
- What the improvement should be

This becomes the basis for your commit message or PR description.

---

## Step 2: Read the Affected Guides

Use the Read tool to load the full content of every guide you plan to modify.

Do not work from memory. Even if you just read the guide, re-read it now.

---

## Step 3: Make the Changes

Apply your improvements to the guide files.

Rules:
- Fix ALL issues in one pass — do not leave partial fixes
- If you discover scope is larger than expected → stop and switch to full epic workflow
- No deferred issues — fix everything or don't change anything

**If your changes affect system behavior** (new sync scripts, new guides, new audit scope, new workflow steps, changed commands or file locations): also review and update the three master-only files that are not propagated to child projects via import:
- [ ] `CLAUDE.md` (root) — does the PR review checklist, Critical Rules, or workflow description need updating?
- [ ] Root `README.md` — does the sync or initialization description need updating?
- [ ] `scripts/initialization/RULES_FILE.template.md` — does the Shamt Sync section or any other section need updating?

These files are the agent's first point of reference and are not kept current by the import mechanism — they require deliberate manual updates when behavior changes.

---

## Step 4: Run the Guide Audit

After making changes:

1. Open `.shamt/guides/audit/README.md`
2. Run the pre-audit checks: `bash .shamt/guides/audit/scripts/pre_audit_checks.sh` (if applicable)
3. Work through the audit stages
4. Fix any issues found before proceeding
5. The audit must pass cleanly

---

## Step 5: Commit

```bash
git add .shamt/guides/ .shamt/scripts/
git commit -m "feat/SHAMT-[N]: [brief description of guide improvement]"
```

For master-internal improvements, commit directly to a branch and open a PR against `main`. Child projects will receive the improvement on their next import.

---

## Larger Changes: Branch + Design Doc

For multi-guide or cross-cutting changes, use a branch with an optional design doc:

1. Create branch: `feat/SHAMT-[N]`
2. For planning: create `SHAMT[N]_DESIGN.md` at the repo root (not in `.shamt/`) to capture scope, decisions, and open questions
3. Make changes across the affected guides and scripts
4. Run the full guide audit before merging (3 consecutive zero-issue rounds required)
5. Open a PR against `main` — child projects receive the changes on their next import run

**What NOT to do for master work:**
- Do not maintain `.shamt/epics/EPIC_TRACKER.md` — SHAMT-N numbers are sequence markers, not epic IDs
- Do not follow S1-S10 stage gates or phase transitions
- Do not create epic folders in `.shamt/epics/`

**Scope threshold:** Judgment call. Single-guide fix → lightweight workflow (Steps 1-5 above). Multi-guide or requires planning → branch + design doc. There is no formal gate between the two.
