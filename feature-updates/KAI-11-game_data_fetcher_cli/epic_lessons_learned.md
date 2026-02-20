## Epic Lessons Learned: game_data_fetcher_cli

**Epic:** KAI-11-game_data_fetcher_cli
**Created:** 2026-02-19 (S1)
**Last Updated:** 2026-02-19

---

## Planning Phase Lessons (S1-S4)

### E2E Output: Always Use Fixed Paths

**Established:** 2026-02-19 (S2 checklist resolution)

User preference: **all runner scripts must use fixed /tmp paths for E2E output**, never
`tempfile.mkdtemp()` or other random paths.

- ✅ `run_game_data_fetcher.py`: `/tmp/game_data_e2e_test.csv`
- ❌ `run_player_fetcher.py`: currently uses `tempfile.mkdtemp()` — tracked for fix in
  `feature-updates/requests/cli-enhancements/player_fetcher_e2e_path_fix_notes.txt`

**Why:** Fixed paths make smoke tests predictable (can verify output without parsing stdout).
Apply this pattern to all future runner scripts with `--e2e-test` mode.

---

## Implementation Phase Lessons (S5-S8)

{To be populated during S5-S8}

---

## QC Phase Lessons (S9-S10)

{To be populated during S9-S10}

---

## Guide Improvements Identified

### S9 Shortcut: Skip S9.P1 and S9.P2 for Single-Feature Epics

**Identified:** 2026-02-19 (S7.P3)

For single-feature epics, S9.P1 (epic smoke testing) and S9.P2 (epic validation loop) are
largely redundant with S7.P1 and S7.P2:
- The code hasn't changed between S7 and S9
- There are no other features to integrate (Part 4 cross-feature is N/A)
- S9.P1 would re-run the same 3-part smoke test as S7.P1

**Proposed guide change:** Add a single-feature shortcut to `stages/s9/s9_epic_final_qc.md`:
> "If this epic has exactly 1 feature and no cross-feature integration exists, skip S9.P1 and
> S9.P2. Proceed directly to S9.P3 (User Testing). The S7 quality gates are sufficient."

**S9.P3 remains mandatory** — user testing is the genuine value-add of S9 and cannot be
replicated by the agent regardless of feature count.

**Applies when:** Exactly 1 feature in the epic AND no cross-feature workflows to verify.
**Do NOT skip when:** 2+ features, or integration between features exists.

*Guide update to be applied in S10.P1 (Guide Updates).*

---

## Key Patterns for Successor Epics

{To be populated after completion — notes for the other successor epics from KAI-10}
