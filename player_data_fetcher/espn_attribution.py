#!/usr/bin/env python3
"""
ESPN Attribution Reconciliation

Pure function joining a validated ESPN league-draft snapshot (D17.2's
LeagueSnapshot) against the complete local player pool on exact integer
playerId, producing a complete `local playerId (str) -> team name` map or
no attribution at all.

Spec: D17.4 spec.md Proposed Architecture; ticket TD2/TD3.

Author: Kai Mizuno
"""

from typing import Dict, List, Optional, Union

from league_helper.constants import FANTASY_TEAM_NAME
from player_data_fetcher.espn_league_snapshot_models import LeagueSnapshot
from player_data_fetcher.player_data_models import ESPNPlayerData, PlayerDataValidationError
from utils.FantasyPlayer import FantasyPlayer


def reconcile_espn_attribution(
    snapshot: LeagueSnapshot,
    players: List[Union[ESPNPlayerData, FantasyPlayer]],
) -> Optional[Dict[str, str]]:
    """Reconcile a validated ESPN league snapshot against the local player pool.

    Pure function: no I/O, no mutation of `snapshot` or `players`, deterministic
    given the same inputs (spec.md Requirements).

    Completeness predicate is exclusively `playerId != -1` (ticket TD2 / spec.md
    AC5) -- draft-level `drafted`/`inProgress` flags and `len(picks)` are never
    consulted here. The single explicit int(ESPN)->str(local) playerId
    normalization boundary is the `str(pick.playerId)` call below (ticket TD3);
    no other normalization (name/team/fuzzy) exists on this path.

    Args:
        snapshot: D17.2-validated league snapshot (picks + teams).
        players: The complete local player pool for this run. Two concrete types reach
            this parameter and their `id` fields are DIFFERENT Python types:
            `ESPNPlayerData.id` is `str` (the fetch path) and `FantasyPlayer.id` is
            `int` (D18.5's live draft cockpit). Both are matched by normalizing the
            local side with `str()` below, which is a no-op for the former. Only `.id`
            is read; nothing else about the objects is assumed.

    Returns:
        A complete `{local playerId: team name}` map covering every completed
        pick (including our own team's picks, per spec.md AC3), or `None` if
        any completed pick's playerId has no local match -- never a partial
        dict. Callers turn a `None` return into a loud raised failure; this
        function itself never raises.
    """
    team_names_by_id = {team.id: team.name for team in snapshot.teams}
    # str()-normalized because the two caller-side player types disagree on the id's
    # Python type (see Args). The ESPN side is already normalized to str a few lines
    # below, at the single int->str boundary ticket D17's TD3 sanctions; matching that
    # here keeps the boundary single rather than adding a second, opposite coercion.
    local_ids = {str(player.id) for player in players}

    attribution: Dict[str, str] = {}
    missing_ids = []
    unresolved_team_ids = []

    for pick in snapshot.draftDetail.picks:
        if pick.playerId == -1:
            continue

        local_id = str(pick.playerId)

        if local_id not in local_ids:
            missing_ids.append(pick.playerId)
            continue

        team_name = team_names_by_id.get(pick.teamId)
        if team_name is None:
            unresolved_team_ids.append(pick.teamId)
            continue

        attribution[local_id] = team_name

    if missing_ids or unresolved_team_ids:
        return None

    return attribution


def normalize_our_team_attribution(
    snapshot: LeagueSnapshot,
    attribution: Dict[str, str],
    our_team_id: int,
    logger,
) -> Dict[str, str]:
    """Rewrite our configured team's picks to the in-app ownership token.

    D17.5 D3/D6. `reconcile_espn_attribution` returns raw ESPN league names
    and stays pure/unchanged, but every downstream ownership reader compares
    `drafted_by` against `league_helper.constants.FANTASY_TEAM_NAME` by string
    equality (`FantasyPlayer.is_rostered`, utils/FantasyPlayer.py:367).
    Normalizing here -- at the seam, keyed on the stable `teamId` rather than
    on a name -- makes `drafted_by` carry the exact token those readers
    compare against, so an ESPN-side team rename cannot break our own identity.

    Hoisted from `DataExporter._normalize_our_team_attribution` to module scope by
    D18.5 so the live draft cockpit and the fetch path share ONE owner of this
    action's whole gating contract instead of the cockpit forking a partial copy.
    `DataExporter._normalize_our_team_attribution` now delegates here; `logger` is a
    parameter because the two callers own different loggers.

    Args:
        snapshot: The validated ESPN league snapshot `attribution` came from.
        attribution: `reconcile_espn_attribution`'s complete
            `local playerId -> raw ESPN team name` map.
        our_team_id: The configured `ESPN_TEAM_ID`.
        logger: The caller's logger, used only for the zero-match warning below.

    Returns:
        A new map identical to `attribution` except that every pick belonging
        to `our_team_id` carries `FANTASY_TEAM_NAME`.

    Raises:
        PlayerDataValidationError: when `our_team_id` is absent from
            `snapshot.teams[]`, or when any OTHER team carries a name equal to
            `FANTASY_TEAM_NAME` (compared case-insensitively and
            whitespace-stripped). Both are fail-closed halts raised BEFORE the
            caller stores anything, so no `drafted_by` is ever mutated.
            Messages name team ids only -- never a credential value.
    """
    team_ids = {team.id for team in snapshot.teams}
    if our_team_id not in team_ids:
        raise PlayerDataValidationError(
            f"ESPN attribution normalization failed: configured ESPN_TEAM_ID "
            f"{our_team_id} is absent from the snapshot's teams[] "
            f"(team ids present: {sorted(team_ids)}); "
            f"ownership state unchanged."
        )

    our_token = FANTASY_TEAM_NAME.strip().casefold()
    colliding_team_ids = sorted(
        team.id
        for team in snapshot.teams
        if team.id != our_team_id
        and team.name is not None
        and team.name.strip().casefold() == our_token
    )
    if colliding_team_ids:
        raise PlayerDataValidationError(
            f"ESPN attribution normalization failed: team id(s) "
            f"{colliding_team_ids} carry a name equal to FANTASY_TEAM_NAME "
            f"while the configured team is id {our_team_id}; normalizing "
            f"would make an opponent's players indistinguishable from ours. "
            f"Rename the colliding ESPN team; ownership state unchanged."
        )

    our_local_ids = {
        str(pick.playerId)
        for pick in snapshot.draftDetail.picks
        if pick.playerId != -1 and pick.teamId == our_team_id
    }
    normalized = {
        local_id: (FANTASY_TEAM_NAME if local_id in our_local_ids else team_name)
        for local_id, team_name in attribution.items()
    }

    completed_picks = sum(
        1 for pick in snapshot.draftDetail.picks if pick.playerId != -1
    )
    our_matches = sum(1 for name in normalized.values() if name == FANTASY_TEAM_NAME)
    if completed_picks and our_matches == 0:
        logger.warning(
            f"ESPN_TEAM_ID {our_team_id} matched zero of {completed_picks} "
            f"completed picks in the ESPN draft snapshot. Check that "
            f"ESPN_TEAM_ID in data/configs/league_config.json is your own "
            f"team's id."
        )

    return normalized


def reconcile_espn_attribution_or_raise(
    snapshot: LeagueSnapshot,
    players: List[Union[ESPNPlayerData, FantasyPlayer]],
    our_team_id: int,
    logger,
) -> Dict[str, str]:
    """Reconcile + normalize, raising a named failure instead of returning None.

    THE single owner of "turn a validated ESPN snapshot into a complete,
    our-team-normalized `local playerId -> owning team name` map". Both entry points
    call it: `DataExporter.load_espn_attribution` (the fetch path, D17.5) and
    `DraftModeManager._reconcile_ownership_from_snapshot` (the live draft cockpit,
    D18.5). Hoisted by D18.5 rather than copied, so the cockpit cannot inherit some of
    this action's gating dimensions and strand the rest.

    Fail-closed and atomic (ticket D17 TD2): nothing is returned, and no caller-side
    ownership is mutated, unless BOTH the reconcile and the normalization succeed.

    Args:
        snapshot: D17.2-validated league snapshot.
        players: The complete local player pool (see `reconcile_espn_attribution`).
        our_team_id: The configured `ESPN_TEAM_ID`.
        logger: The caller's logger, forwarded to `normalize_our_team_attribution`.

    Returns:
        The complete, our-team-normalized attribution map.

    Raises:
        PlayerDataValidationError: when a completed pick's playerId has no local match
            or its teamId has no resolvable name (the `None` return of
            `reconcile_espn_attribution`, turned into a named failure listing every
            offending id), or from `normalize_our_team_attribution`'s own two
            fail-closed guards.
    """
    attribution = reconcile_espn_attribution(snapshot, players)

    if attribution is None:
        local_ids = {str(player.id) for player in players}
        team_ids = {team.id for team in snapshot.teams if team.name is not None}
        missing_ids = sorted(
            pick.playerId
            for pick in snapshot.draftDetail.picks
            if pick.playerId != -1 and str(pick.playerId) not in local_ids
        )
        unresolved_team_ids = sorted(set(
            pick.teamId
            for pick in snapshot.draftDetail.picks
            if pick.playerId != -1
            and str(pick.playerId) in local_ids
            and pick.teamId not in team_ids
        ))
        raise PlayerDataValidationError(
            f"ESPN attribution reconciliation failed: completed playerId(s) "
            f"{missing_ids} have no local player match, and teamId(s) "
            f"{unresolved_team_ids} have no resolvable team name; "
            f"ownership state unchanged."
        )

    return normalize_our_team_attribution(snapshot, attribution, our_team_id, logger)
