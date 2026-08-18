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

from typing import Dict, List, Optional

from player_data_fetcher.espn_league_snapshot_models import LeagueSnapshot
from player_data_fetcher.player_data_models import ESPNPlayerData


def reconcile_espn_attribution(
    snapshot: LeagueSnapshot,
    players: List[ESPNPlayerData],
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
        players: The complete local ProjectionData player pool for this run.

    Returns:
        A complete `{local playerId: team name}` map covering every completed
        pick (including our own team's picks, per spec.md AC3), or `None` if
        any completed pick's playerId has no local match -- never a partial
        dict. Callers turn a `None` return into a loud raised failure; this
        function itself never raises.
    """
    team_names_by_id = {team.id: team.name for team in snapshot.teams}
    local_ids = {player.id for player in players}

    attribution: Dict[str, str] = {}
    missing_ids = []

    for pick in snapshot.draftDetail.picks:
        if pick.playerId == -1:
            continue

        local_id = str(pick.playerId)

        if local_id not in local_ids:
            missing_ids.append(pick.playerId)
            continue

        attribution[local_id] = team_names_by_id.get(pick.teamId, "")

    if missing_ids:
        return None

    return attribution
