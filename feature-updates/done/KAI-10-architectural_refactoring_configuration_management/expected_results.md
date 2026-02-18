# F01: expected_results.md — refactor_player_data_fetcher

## Expected Output Structure

**Output location:** System temp dir (e.g. `/tmp/player_fetcher_e2e_XXXXX/`)

```
/tmp/player_fetcher_e2e_XXXXX/
├── player_data/
│   ├── qb_data.json
│   ├── rb_data.json
│   ├── wr_data.json
│   ├── te_data.json
│   ├── k_data.json
│   └── dst_data.json
├── team_data/
│   └── {TEAM}.csv  (one per NFL team with data)
└── game_data.csv
```

---

## Expected Data Values

### Position JSON files (`player_data/*.json`)

Each file is a JSON array of player objects. Per spec:
- `id`: integer, > 0
- `name`: non-empty string
- `position`: one of QB/RB/WR/TE/K/DST
- `team`: 2-3 char NFL team abbreviation
- `projected_points`: list of 17 floats (weekly projections)
- `actual_points`: list of 17 floats (weekly actuals)

**Value ranges (from spec):**
- `projected_points` values: 0.0 – 60.0 per week (not all zeros for active players)
- `actual_points` values: 0.0 – 60.0 per week
- At least one player per position with projected_points sum > 0

### Team CSVs (`team_data/{TEAM}.csv`)

Columns: `week, QB, RB, WR, TE, K, points_scored, points_allowed`
- At least 1 row of data
- `week` values: 1–17
- `points_scored` / `points_allowed`: positive floats

### game_data.csv

Columns include home/away team, week, scores
- At least 1 game record

---

## Pass Criteria

| Check | Criterion |
|-------|-----------|
| Exit code | 0 |
| Output location | `/tmp/` prefix, NOT `data/` |
| Position files | At least 4 of 6 exist |
| Player count | At least 10 players total across all positions |
| Projected points | Not all zeros (at least 1 player with sum > 0) |
| Player names | Non-empty strings |
| Team CSVs | At least 1 file, at least 1 data row |
| Execution time | < 120 seconds |
