# 2025 season corpus — provenance and handling

**Status: RESTORED and VALIDATED, 2026-08-18.**

> **DO NOT RECOMPILE THIS SEASON FROM ESPN.** Doing so would destroy its ADP. See §Do not
> regenerate below — this is not a style preference, it is a measured data-loss hazard.

This corpus is treated as an **irreplaceable archive**, not a regenerable artifact. ESPN's
fantasy archive has decayed for prior seasons, so several fields here can no longer be re-fetched
from the source that originally produced them.

---

## Field provenance

| field | source | state |
|---|---|---|
| `average_draft_position` | FantasyPros (via the now-retired CSV path, `D17.6`) | **healthy — 598 distinct, 3 nulls** |
| `player_rating` | ESPN positional rank (wk 1), cumulative actuals (wk 2+) | **healthy — 403 distinct wk1, 579 wk2+** |
| `projected_points` | ESPN `statSourceId=1`, `seasonId`-filtered | **healthy — 91.0% coverage** |
| `actual_points` | ESPN `statSourceId=0` | healthy |
| `extra_points` / `field_goals` | ESPN, **unwrapped 2026-08-18** (see below) | **restored** |
| `season_schedule.csv`, `game_data.csv`, `team_data/` | ESPN Scoreboard + Open-Meteo | **healthy — score values verified** |

## What was changed on 2026-08-18

**The kicker stat block was unwrapped from `kicking` to the flat shape the parser reads.**
`historical_data_compiler/json_exporter.py` nested kicker statistics under a `kicking` key, but
`utils/FantasyPlayer.from_json` reads top-level `extra_points` / `field_goals` and has **no
`kicking` field at all**. Every kicker in this season therefore parsed to
`field_goals=None, extra_points=None` — the statistics were present on disk and unreadable by
every consumer.

- **684 records** unwrapped (38 kickers x 18 weeks).
- **Lossless and invertible**: the wrapper contained exactly those two blocks with the identical
  inner structure the live producer emits at top level.
- **Verified**: 684 records compared field-by-field against a pre-change copy — **0
  discrepancies**; every non-kicker file byte-identical; the CSV layer untouched.
- **Confirmed readable**: `Jason Myers` wk18 now parses to 39 field goals and 47 extra points made.

The code-side fix so both producers emit one shape is ticket
`D30-producer-player-record-schema-parity-kicker-block`.

## Validation performed

- **ADP cross-validated against an independent source.** Matched against Fantasy Football
  Calculator's 2025 draft-sampled ADP (245 pairs): **Pearson r = 0.922, Spearman r = 0.942.**
  The disagreements are entirely deep-tail scale (FFC's pool ends near 177 while this corpus
  spreads to 880), not ordering. **This season's ADP is real, independently corroborated data.**
- **Projection coverage**: 91.0% season-wide, no week below the per-week floor
  (`simulation/shared/sim_data_coverage.py`).
- **`game_data.csv` scores** spot-checked against ESPN's Scoreboard API for week 12: 14/14 exact.
- **Bye weeks** agree three ways — `season_schedule.csv`, the `team_data` all-zero row, and the
  player JSON `bye_week` — for all 32 teams.
- `validate_sim_data.py --year 2025`: **all checks passed.**
- `SimDataLoader` loads the season: `is_valid=True`, 17 weeks, 773 players per week.

## Do not regenerate

**ESPN now serves a flat `170.0` ADP sentinel for every 2025 player** (measured 2026-08-18:
1,087 of 1,090 players, `distinct = 1`). Recompiling this season would replace the validated,
598-value, granular ADP recorded above with **a single repeated number** — the same pathology
`D9.1` inflicted on the live corpus and `D29` exists to track.

**This season's ADP is deeper and more granular than its 2021-2024 siblings**, which carry ESPN's
undrafted pile at 169.8-170.0. When making the five seasons commensurable, the correct direction is
to raise the others, **never to lower 2025 toward them.**

## Known remaining gap

`average_draft_position` uses a deeper scale than 2021-2024, so cross-season comparisons that treat
ADP as a common measurement are not yet valid. Tracked in the spike
`.shamt-core/spikes/historical-corpus-restoration.md`.
