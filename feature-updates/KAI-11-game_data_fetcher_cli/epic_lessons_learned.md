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

{To be populated throughout — improvements to epic workflow guides go through S10.P1}

---

## Key Patterns for Successor Epics

{To be populated after completion — notes for the other successor epics from KAI-10}
