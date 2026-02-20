## GUIDE ANCHOR: game_data_fetcher_cli (KAI-11)

**Purpose:** Resumption instructions for agents continuing after session compaction.

---

## If You Are Resuming This Epic

**Step 1:** Read `EPIC_README.md` in this folder — check Agent Status section for:
- Current Stage and Phase
- Current Guide (file path)
- Current Step
- Next Action
- Blockers

**Step 2:** Read the guide listed in Agent Status using the Read tool (FULL guide).

**Step 3:** Continue from the "Next Action" listed in Agent Status.

**DO NOT restart the workflow from S1 — continue from where the previous agent left off.**

---

## Epic Overview

**Epic:** KAI-11 — game_data_fetcher_cli
**Branch:** epic/KAI-11
**Request File:** `feature-updates/requests/cli-enhancements/game_data_fetcher_cli_notes.txt`

**Goal:** Refactor `run_game_data_fetcher.py` — add 4 CLI args, remove os.chdir + config imports,
wire log-level, implement E2E mode (Week 1, /tmp), add test file.

**Features:** 1 total
- `feature_01_game_data_fetcher_cli/` — Run game data fetcher runner refactor

---

## Workflow Reference

```
S1 → S2 → S3 → S4 → S5 → S6 → S7 → S8 → S9 → S10
 Done  ←current
```

**Stage Guides (CLAUDE.md is authoritative source):**
- S2: `stages/s2/s2_feature_deep_dive.md`
- S5: `stages/s5/s5_v2_validation_loop.md`
- S6: `stages/s6/s6_execution.md`
- S7: `stages/s7/s7_p1_smoke_testing.md`
- S9: `stages/s9/s9_epic_final_qc.md`
- S10: `stages/s10/s10_epic_cleanup.md`

**Phase transition prompts:** `guides_v2/prompts_reference_v2.md`

---

## Key Context

- KAI-10 Feature 03 spec fully approved — S2 will port it into `feature_01/spec.md`
- `game_data_fetcher.py` was already refactored by KAI-10 (constructor accepts `request_timeout`)
- No parallel work — 1 feature, sequential S2
- E2E output: `/tmp/game_data_e2e_test.csv`
