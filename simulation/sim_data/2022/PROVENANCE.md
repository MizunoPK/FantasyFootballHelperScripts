# 2022 season corpus — provenance and handling

**Status: RESTORED, 2026-08-18.**

> **DO NOT RECOMPILE THIS SEASON FROM ESPN.** Its ADP would be re-contaminated and its week-1
> rating would revert. See §Do not regenerate.

This corpus is an **irreplaceable archive**, not a regenerable artifact.

---

## `average_draft_position` — REPLACED with draft-time values

ESPN's `ownership.averageDraftPosition` is a **single live field with no time dimension**. It keeps
updating after a season is played, so a stored historical value reflects **end-of-season consensus,
not draft time**. Measured for this season before restoration: agreement with independent
draft-time ADP was only Pearson **0.816**, and **5** of FFC's top-50
players were buried below ADP 100 — systematically the ones whose seasons went badly.

The control that proved this is ESPN's own 2026 data, where **no season has been played**: there it
agrees with FFC at Pearson **0.945** and buries **nobody**. The drift appears only after a season
is played.

Replaced with **Fantasy Football Calculator** ADP, sampled from real drafts in the days before that
season's week 1 — point-in-time by construction, so it cannot encode an outcome.

- **147 players** carry FFC draft-time ADP.
- **642 players** carry the undrafted sentinel `200.0`. FFC's sampled drafts never took
  them, and every ADP at or above 100 maps to the same `VERY_POOR` multiplier — so the stored value
  conveyed nothing, and a uniform honest sentinel replaces a drifted number with fake precision.
- **Dropped: `Evan McPherson`, `Packers D/ST`.** ESPN priced each as a real pick (ADP below 100) while FFC's thousands of sampled drafts never took them — an unresolvable contradiction, and precisely where the drift lives. A kicker priced at ADP 67 or a defense at 88 is not a draft position, it is a season result.

### `player_rating` (week 1) — REBUILT from FFC

ESPN serves **no positional rank data at all** for this season (measured 2026-08-18: 0 of the
players returned carry either `rankings[].averageRank` or `draftRanksByRankType`). Every player
therefore fell to `json_exporter.py`'s `50.0` fallback, giving a **flat week-1 rating** — one
distinct value across the whole corpus. A recompile reproduces it exactly; the source is gone.

Rebuilt from **FFC ADP ranked within position**, normalised the way the compiler normalises
`averageRank` (best in position → 100, worst → 1). This is the same CLASS of draft-time consensus
the compiler originally used, and it is pre-season by construction, so it cannot leak outcome.

Players FFC's drafts never took carry **`None`**, not a fabricated midpoint.
`PLAYER_RATING_SCORING.MISSING_VALUE_TIER` scores an absent rating as `VERY_POOR`, so the data is
self-documenting: it says "unknown", and the scorer treats unknown as undrafted rather than average.

Weeks 2-18 are untouched — those are computed from cumulative actuals through the prior week, which
is legitimate point-in-time information for that week's snapshot.

## Kicker statistics — UNWRAPPED

**666 records** (37 kickers x 18 weeks) moved from the compiler's `kicking`
wrapper to the flat `extra_points` / `field_goals` shape `utils/FantasyPlayer.from_json` actually
reads. They were present on disk and unreadable by every consumer. Lossless and invertible; verified
record-by-record against a pre-change copy with zero discrepancies.

## Unchanged and verified healthy

`projected_points` — ESPN, `seasonId`-filtered, and confirmed NOT outcome-drifted: it tracks actuals
no more closely than an independent contemporaneous forecast does (deltas within noise against
Sleeper/RotoWire on sampled weeks). `actual_points`, `season_schedule.csv`, `game_data.csv`,
`team_data/` — all unchanged; the bye layer agrees three ways and scores were spot-checked against
ESPN's Scoreboard API.

## Do not regenerate

A recompile would restore ESPN's drifted ADP for this season and reinstate the flat 50.0 week-1 rating.
Of the seasons in this corpus only **2024** re-fetches cleanly from ESPN at all, and even there the
ADP would come back contaminated.

## Related

Draft-time lookahead in `player_rating` consumption was fixed separately in `bd8bdab9` — the draft
read week_18's full-season ranking. Investigation record:
`.shamt-core/spikes/historical-corpus-restoration.md`.
