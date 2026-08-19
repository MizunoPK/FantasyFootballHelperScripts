"""
Draft Geometry Reader

A pure function that reads the draft geometry — our slot, overall pick number, current
round, snake direction, and picks-until-our-next-turn — from an already-validated
`LeagueSnapshot` (`player_data_fetcher/espn_league_snapshot_models.py`). No network
access, no parsing, and no snake reconstruction: ESPN pre-computes the snake reversal and
pre-allocates every `draftDetail.picks[]` row with its owning team, round and overall
number, so this module *reads* the geometry rather than deriving it (`TD3`).

`playerId != -1` is the sole completed-pick predicate throughout, inherited verbatim from
`LeagueSnapshot`'s own model contract — never `len(picks)`, array truthiness, or
`drafted`/`inProgress`.

This is a `provision`-stage unit: additive and callerless. Nothing in `league_helper/`
imports this module yet — wiring it into `AddToRosterModeManager` is `D18.5`'s job.

Author: Kai Mizuno
"""

from dataclasses import dataclass
from typing import Optional

from player_data_fetcher.espn_league_snapshot_models import LeagueSnapshot


@dataclass
class DraftGeometry:
    """
    The draft geometry read from a single `LeagueSnapshot` evaluation.

    `our_slot` is always populated — it is resolved independently of the rest of the
    geometry (`pickOrder.index(our_team_id)`), so it survives both sentinel states below.

    Two distinct sentinel states exist, and they are NOT the same shape:

    - **ALL-SENTINEL** (no row anywhere in `picks[]` has `playerId == -1` — the
      draft-complete/placeholder-lag boundary): every field below `our_slot` is `None`.
    - **Field-level sentinel** (our team has no remaining incomplete pick, but some other
      team's current pick still exists): only `picks_until_our_next_turn` is `None`;
      `current_round`, `overall_pick_number`, and `snake_direction` stay populated.

    Attributes:
        our_slot: Our 0-based position in `settings.draftSettings.pickOrder`, re-resolved
            from the live payload every call. Always populated.
        current_round: The `roundId` of the current (lowest-`overallPickNumber` incomplete)
            pick, or `None` at the ALL-SENTINEL boundary.
        overall_pick_number: The `overallPickNumber` of the current pick, or `None` at the
            ALL-SENTINEL boundary.
        snake_direction: `"forward"` if the current round's served pick order matches
            `pickOrder`, `"reverse"` if it matches `reversed(pickOrder)`, or `None` at the
            ALL-SENTINEL boundary. Never derived from `roundId % 2` parity.
        picks_until_our_next_turn: The overall-pick-number gap between the current pick and
            our next incomplete pick, or `None` when our team has no remaining incomplete
            pick (field-level sentinel) or at the ALL-SENTINEL boundary.
    """

    our_slot: int
    current_round: Optional[int]
    overall_pick_number: Optional[int]
    snake_direction: Optional[str]
    picks_until_our_next_turn: Optional[int]


def read_geometry(snapshot: LeagueSnapshot, our_team_id: int) -> DraftGeometry:
    """Read the draft geometry from an already-validated `LeagueSnapshot`.

    Performs no network access, no parsing, and no snake reconstruction — every value is
    read directly off the already-validated payload (`TD3`).

    Args:
        snapshot: An already-validated `LeagueSnapshot`. This function does not construct,
            fetch, or revalidate it.
        our_team_id: Our fantasy team's ESPN id (`ConfigManager.espn_team_id`). Used only to
            resolve our slot and our next pick — never cached, re-read every call.

    Returns:
        The `DraftGeometry` for this snapshot. See `DraftGeometry`'s docstring for its two
        distinct sentinel states.

    Raises:
        ValueError: `our_team_id` is absent from `settings.draftSettings.pickOrder` — a real
            misconfiguration (wrong `ESPN_TEAM_ID` or wrong-league payload), never a valid
            mid-draft state.
        ValueError: `settings.draftSettings.pickOrder` contains a duplicate team id — this
            function's own corruption guard. `LeagueSnapshot`'s models enforce no
            distinctness constraint on `pickOrder`, so this reader enforces it itself,
            before anything derived from `pickOrder`'s per-position distinctness (our slot's
            index resolution, the snake-direction prefix comparison below) is computed.
        ValueError: The current round's served team-id order matches neither `pickOrder`'s
            prefix nor its reversed prefix — a corruption guard, not a freshness check (a
            stale-but-internally-consistent grid still passes it).
        ValueError: `snapshot.round_count` raises on an entirely empty `picks[]` — inherited
            from `LeagueSnapshot.round_count`'s own contract, not re-derived here.
    """
    pick_order = snapshot.settings.draftSettings.pickOrder

    if our_team_id not in pick_order:
        raise ValueError(
            f"our_team_id {our_team_id} not found in pickOrder {pick_order}"
        )

    if len(set(pick_order)) != len(pick_order):
        raise ValueError(
            f"pickOrder contains duplicate team ids: {pick_order}"
        )

    our_slot = pick_order.index(our_team_id)

    # Triggers LeagueSnapshot.round_count's own ValueError on an entirely empty picks[] —
    # an inherited guard, never re-derived. The returned value is not otherwise used here:
    # current_round is read from the served pick rows themselves, below.
    _ = snapshot.round_count

    picks = snapshot.draftDetail.picks
    incomplete_picks = [pick for pick in picks if pick.playerId == -1]

    if not incomplete_picks:
        return DraftGeometry(
            our_slot=our_slot,
            current_round=None,
            overall_pick_number=None,
            snake_direction=None,
            picks_until_our_next_turn=None,
        )

    current_pick = min(incomplete_picks, key=lambda pick: pick.overallPickNumber)
    current_round = current_pick.roundId
    overall_pick_number = current_pick.overallPickNumber

    served_this_round = sorted(
        (pick for pick in picks if pick.roundId == current_round),
        key=lambda pick: pick.overallPickNumber,
    )
    served_team_ids = [pick.teamId for pick in served_this_round]
    served_count = len(served_team_ids)
    forward_prefix = pick_order[:served_count]
    reverse_prefix = list(reversed(pick_order))[:served_count]

    if served_team_ids == forward_prefix:
        snake_direction = "forward"
    elif served_team_ids == reverse_prefix:
        snake_direction = "reverse"
    else:
        raise ValueError(
            f"Round {current_round} served team order {served_team_ids} matches neither "
            f"pickOrder prefix {forward_prefix} nor reversed prefix {reverse_prefix}"
        )

    our_incomplete_picks = [
        pick for pick in incomplete_picks if pick.teamId == our_team_id
    ]
    if not our_incomplete_picks:
        picks_until_our_next_turn = None
    else:
        our_next_pick = min(
            our_incomplete_picks, key=lambda pick: pick.overallPickNumber
        )
        picks_until_our_next_turn = (
            our_next_pick.overallPickNumber - current_pick.overallPickNumber
        )

    return DraftGeometry(
        our_slot=our_slot,
        current_round=current_round,
        overall_pick_number=overall_pick_number,
        snake_direction=snake_direction,
        picks_until_our_next_turn=picks_until_our_next_turn,
    )
