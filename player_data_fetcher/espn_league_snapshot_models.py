"""
Data Models for ESPN League Draft Snapshot

This module contains Pydantic v2 data models for the ESPN authenticated league-draft-snapshot
payload (`draftDetail.picks[]`, `teams[]`, `settings.draftSettings`) from the `mDraftDetail` +
`mTeam` view pair, plus model-level semantic validation of that payload's cross-row invariants.

Author: Kai Mizuno
"""

from typing import Dict, List, Optional

from pydantic import BaseModel, Field, StrictBool, StrictInt, model_validator


DEFAULT_POSITION_ID_TO_POSITION: Dict[int, str] = {
    1: 'QB',
    2: 'RB',
    3: 'WR',
    4: 'TE',
    5: 'K',
    16: 'DST',
}
"""Maps the projections-view (`kona_player_info`) `defaultPositionId` enum to a position name.
Not used by this module's own models (`DraftPick` carries no `defaultPositionId` field — that
field belongs to a different ESPN view outside this unit's `mDraftDetail` + `mTeam` scope) —
provided so a caller resolving `defaultPositionId` elsewhere has a table symmetric with
LINEUP_SLOT_ID_TO_POSITION below, per unit.md AC6.

Coverage / miss contract: these six starting-position values are the complete set this unit's
evidence base confirms (`player_data_fetcher/espn_client.py`'s existing `ESPN_POSITION_MAPPINGS`
site, `player_data_fetcher/player_data_constants.py`). ESPN's `defaultPositionId` enum is not
otherwise evidenced by the spike (`.shamt-core/spikes/archive/espn-draft-night-integration.md`
never lists a `defaultPositionId` value outside this set), so a value outside this table is
either genuinely unassigned or simply unobserved by this unit's evidence base — exhaustiveness is
NOT claimed. A caller doing lookup MUST use `.get(value, 'UNKNOWN')`, mirroring the established
`ESPN_POSITION_MAPPINGS.get(position_id, 'UNKNOWN')` idiom at `espn_client.py:1478` — direct `[]`
indexing on a miss raises `KeyError` rather than returning `None`, which is why the `.get(...,
'UNKNOWN')` form is the documented contract rather than an incidental usage note."""

LINEUP_SLOT_ID_TO_POSITION: Dict[int, str] = {
    0: 'QB',
    2: 'RB',
    4: 'WR',
    6: 'TE',
    16: 'DST',
    17: 'K',
}
"""Maps the draft-pick-row `lineupSlotId` enum to a position name. RB (2) coincides with
DEFAULT_POSITION_ID_TO_POSITION; WR (4 here vs 3 there) and K/DST positions diverge — the two
tables are never merged (spike F14a).

Coverage / miss contract: these six starting-position-slot values are the complete set this
unit's evidence base confirms — spike F11's live-probe field list for `picks[]` names
`lineupSlotId` as a real field but does not enumerate its full value range, and this repo's
pre-existing `_position_to_slot_id` docstring (`espn_client.py:1337`) independently documents the
identical six-value set (`QB=0, RB=2, WR=4, TE=6, K=17, DST=16`) under a different name (ranking
`slotId`). ESPN's public `lineupSlotId` enum is known to include non-starting values this unit's
evidence does NOT confirm or deny — bench, IR, and multi-position flex slots among them — so this
table's exhaustiveness over the FULL enum is explicitly NOT claimed; only the six evidenced
starting-position values are asserted correct. A caller doing lookup MUST use `.get(value,
'UNKNOWN')`, the same fail-loud-via-sentinel idiom `DEFAULT_POSITION_ID_TO_POSITION` documents
above — direct `[]` indexing on an unmapped `lineupSlotId` (e.g. a bench/IR/flex slot) raises
`KeyError` rather than silently returning `None`; a caller that must distinguish "no position"
from "table incomplete" should catch `KeyError` explicitly rather than relying on `.get()`'s
sentinel alone. D17.4 (reconciliation, out of this unit's scope) is the consumer responsible for
deciding what a genuinely-unmapped completed pick's `lineupSlotId` means for ownership purposes;
this unit's job stops at making the miss loud rather than silent."""


class DraftPick(BaseModel):
    """
    One row of `draftDetail.picks[]` from the ESPN `mDraftDetail` view.

    `picks[]` is pre-allocated for the whole draft before any selection is made, with every
    unfilled row carrying `playerId == -1` (spike F11a) — never infer completion from array
    length or truthiness; use `playerId != -1` (see `LeagueSnapshot`'s semantic validators).

    Attributes:
        overallPickNumber: 1-based overall pick order across the whole draft. Strict int — no coercion.
        playerId: ESPN's integer player ID, or -1 for an unfilled placeholder row. Strict int — no coercion.
        teamId: The fantasy team ID this pick slot belongs to. Strict int — no coercion.
        roundId: 1-based draft round number. Strict int — no coercion.
        lineupSlotId: ESPN's roster-slot enum for this pick — a DIFFERENT enum from
            `defaultPositionId` (see `LINEUP_SLOT_ID_TO_POSITION`). Strict int — no coercion.
        roundPickNumber: 1-based pick number within the round. Ordinary coercion.
        keeper: Whether this pick is a designated keeper slot. Ordinary coercion.
        reservedForKeeper: Whether this slot is reserved for a keeper. Ordinary coercion.
        autoDraftTypeId: ESPN's auto-draft classification for this pick. Ordinary coercion.
        bidAmount: Auction bid amount, when applicable. Ordinary coercion.
        nominatingTeamId: Team ID that nominated this pick, when applicable. Ordinary coercion.
        tradeLocked: Whether this pick is trade-locked. Ordinary coercion.
        id: ESPN's own row identifier for this pick. Ordinary coercion.
    """

    overallPickNumber: StrictInt
    playerId: StrictInt
    teamId: StrictInt
    roundId: StrictInt
    lineupSlotId: StrictInt

    roundPickNumber: Optional[int] = None
    keeper: Optional[bool] = None
    reservedForKeeper: Optional[bool] = None
    autoDraftTypeId: Optional[int] = None
    bidAmount: Optional[int] = None
    nominatingTeamId: Optional[int] = None
    tradeLocked: Optional[bool] = None
    id: Optional[int] = None


class LeagueTeam(BaseModel):
    """
    One row of `teams[]` from the ESPN `mTeam` view — the id-to-name mapping `drafted_by`
    resolution depends on.

    Attributes:
        id: The fantasy team's ESPN integer ID. Strict int — no coercion; `DraftPick.teamId`
            joins against this field.
        name: The team's display name. Ordinary coercion.
        abbrev: The team's short abbreviation. Ordinary coercion.
    """

    id: StrictInt

    name: Optional[str] = None
    abbrev: Optional[str] = None


class DraftSettings(BaseModel):
    """
    The `settings.draftSettings` sub-object from the ESPN `mTeam` view.

    Attributes:
        pickOrder: The team-ID draft order for round 1 (length == team count; spike F11). Every
            entry is strict int — no coercion — since this list is the payload's only
            directly-stated team-count-bearing field (context.md: round/team counts are derived
            from the payload, never hardcoded).
        type: The draft type (e.g. "SNAKE", "OFFLINE"). Ordinary coercion.
        timePerSelection: Per-pick time limit in seconds. Ordinary coercion.
    """

    pickOrder: List[StrictInt]

    type: Optional[str] = None
    timePerSelection: Optional[int] = None


class LeagueSnapshot(BaseModel):
    """
    The top-level ESPN league-draft-snapshot envelope combining `draftDetail`, `teams[]`, and
    `settings.draftSettings` from the `mDraftDetail` + `mTeam` view pair.

    Model-level (`@model_validator`) semantic checks enforce invariants that span multiple rows
    or sub-objects and cannot be expressed as per-field constraints: no duplicate completed
    `playerId`, no duplicate `overallPickNumber`, and every completed pick's `teamId` present in
    `teams[]`. `playerId != -1` is the sole completed-pick predicate everywhere below — never
    `len(picks)`, array truthiness, or `drafted`/`inProgress` (spike F11a).

    Attributes:
        picks: `draftDetail.picks[]` — one row per pre-allocated draft slot.
        drafted: Draft-level "has drafting started" flag. Strict bool — no coercion. Never used
            as a completed-pick predicate; see `playerId != -1` above.
        inProgress: Draft-level "is drafting currently active" flag. Strict bool — no coercion.
            Never used as a completed-pick predicate; see `playerId != -1` above.
        teams: `teams[]` — the id-to-name mapping pick `teamId` values join against.
        draftSettings: `settings.draftSettings`.
    """

    picks: List[DraftPick]
    drafted: StrictBool
    inProgress: StrictBool
    teams: List[LeagueTeam]
    draftSettings: DraftSettings

    @model_validator(mode="after")
    def _no_duplicate_completed_player_ids(self) -> "LeagueSnapshot":
        """Reject a snapshot with more than one completed pick sharing the same `playerId`."""
        seen: Dict[int, int] = {}
        for pick in self.picks:
            if pick.playerId == -1:
                continue
            seen[pick.playerId] = seen.get(pick.playerId, 0) + 1
        duplicates = [player_id for player_id, count in seen.items() if count > 1]
        if duplicates:
            raise ValueError(
                f"Duplicate completed playerId(s) in draftDetail.picks[]: {sorted(duplicates)}"
            )
        return self

    @model_validator(mode="after")
    def _no_duplicate_overall_pick_number(self) -> "LeagueSnapshot":
        """Reject a snapshot with more than one pick row sharing the same `overallPickNumber`."""
        seen: Dict[int, int] = {}
        for pick in self.picks:
            seen[pick.overallPickNumber] = seen.get(pick.overallPickNumber, 0) + 1
        duplicates = [number for number, count in seen.items() if count > 1]
        if duplicates:
            raise ValueError(
                f"Duplicate overallPickNumber(s) in draftDetail.picks[]: {sorted(duplicates)}"
            )
        return self

    @model_validator(mode="after")
    def _completed_pick_team_id_present(self) -> "LeagueSnapshot":
        """Reject a completed pick whose `teamId` is absent from `teams[]`."""
        team_ids = {team.id for team in self.teams}
        missing = sorted(
            {pick.teamId for pick in self.picks if pick.playerId != -1 and pick.teamId not in team_ids}
        )
        if missing:
            raise ValueError(
                f"Completed pick teamId(s) not present in teams[]: {missing}"
            )
        return self
