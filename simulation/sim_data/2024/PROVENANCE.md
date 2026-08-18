# 2024 season corpus — provenance and handling

**Status: RESTORED, 2026-08-18.**

> **DO NOT RECOMPILE THIS SEASON FROM ESPN.** Its ADP would be re-contaminated and its week-1
> rating would revert. See §Do not regenerate.

This corpus is an **irreplaceable archive**, not a regenerable artifact.

---

## `average_draft_position` — REPLACED with draft-time values

ESPN's `ownership.averageDraftPosition` is a **single live field with no time dimension**. It keeps
updating after a season is played, so a stored historical value reflects **end-of-season consensus,
not draft time**. Measured for this season before restoration: agreement with independent
draft-time ADP was only Pearson **0.796**, and **6** of FFC's top-50
players were buried below ADP 100 — systematically the ones whose seasons went badly.

The control that proved this is ESPN's own 2026 data, where **no season has been played**: there it
agrees with FFC at Pearson **0.945** and buries **nobody**. The drift appears only after a season
is played.

Replaced with **Fantasy Football Calculator** ADP, sampled from real drafts in the days before that
season's week 1 — point-in-time by construction, so it cannot encode an outcome.

- **200 players** carry FFC draft-time ADP.
- **574 players** carry the undrafted sentinel `200.0`. FFC's sampled drafts never took
  them, and every ADP at or above 100 maps to the same `VERY_POOR` multiplier — so the stored value
  conveyed nothing, and a uniform honest sentinel replaces a drifted number with fake precision.
- **Dropped: `Broncos D/ST`, `Vikings D/ST`.** ESPN priced each as a real pick (ADP below 100) while FFC's thousands of sampled drafts never took them — an unresolvable contradiction, and precisely where the drift lives. A kicker priced at ADP 67 or a defense at 88 is not a draft position, it is a season result.

### `player_rating` — KEPT, verified honest

Unlike its ADP, ESPN's rank data for this season is **not** outcome-drifted. Week-1 rating agrees
with FFC's independent draft-time ADP at **Spearman 0.79** (ranked within position, 200 pairs),
which is what an honest pre-season ranking looks like. Left exactly as compiled.

Weeks 2-18 are computed from cumulative actuals through the prior week — legitimate point-in-time
information for that week's snapshot.

## Kicker statistics — UNWRAPPED

**738 records** (41 kickers x 18 weeks) moved from the compiler's `kicking`
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

A recompile would restore ESPN's drifted ADP for this season.
Of the seasons in this corpus only **2024** re-fetches cleanly from ESPN at all, and even there the
ADP would come back contaminated.

## Related

Draft-time lookahead in `player_rating` consumption was fixed separately in `bd8bdab9` — the draft
read week_18's full-season ranking. Investigation record:
`.shamt-core/spikes/historical-corpus-restoration.md`.
