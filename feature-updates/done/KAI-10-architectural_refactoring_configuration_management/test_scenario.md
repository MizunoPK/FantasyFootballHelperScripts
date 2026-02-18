# F01: test_scenario.md — refactor_player_data_fetcher

## Test Scenario: Player Data Fetcher E2E (E2E mode)

**Feature:** F01 — refactor_player_data_fetcher
**Entry Point:** `python run_player_fetcher.py --e2e-test`

---

## Input Data Sources

- **ESPN API** (live, real data) — capped at 100 players via `--espn-player-limit 100` in E2E mode
- **NFL Schedule API** (via game_data_fetcher) — real game schedule data
- **No local input files required** — fetcher pulls directly from ESPN

---

## Expected Behavior

1. Fetch up to 100 players from ESPN projections API
2. Group players into 6 position buckets (QB, RB, WR, TE, K, DST)
3. Write 6 position JSON files to temp output dir (not `data/`)
4. Write per-team CSV files to temp `team_data/` folder
5. Write `game_data.csv` with schedule data to temp dir
6. Exit cleanly (code 0)

---

## Validation Criteria

- Script exits with code 0
- Output written to temp dir (NOT `data/player_data` or `data/team_data`)
- At least 4 of 6 position JSON files exist with player data
- Player records have non-placeholder projected_points values
- Team CSVs contain real weekly performance data
- Execution completes in under 120 seconds
