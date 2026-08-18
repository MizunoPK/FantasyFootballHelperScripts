#!/usr/bin/env python3
"""
Tests for ESPN Attribution Reconciliation

Pure-function tests for reconcile_espn_attribution: complete map, missing-player
rejection, own-team inclusion, playerId != -1 predicate, pick-order-change
re-read behavior.

Spec: D17.4 spec.md Requirements; ticket TD2/TD3, spike F13b.

Author: Kai Mizuno
"""

from unittest.mock import Mock

from player_data_fetcher.espn_attribution import reconcile_espn_attribution
from player_data_fetcher.player_data_models import ESPNPlayerData


# FIXTURES

def make_pick(player_id, team_id):
    pick = Mock()
    pick.playerId = player_id
    pick.teamId = team_id
    return pick


def make_team(team_id, name):
    team = Mock()
    team.id = team_id
    team.name = name
    return team


def make_snapshot(picks, teams):
    snapshot = Mock()
    snapshot.draftDetail = Mock()
    snapshot.draftDetail.picks = picks
    snapshot.teams = teams
    return snapshot


def make_local_player(player_id):
    return ESPNPlayerData(id=player_id, name=f"Player {player_id}", team="KC", position="WR")


class TestReconcileEspnAttribution:
    """Complete-or-nothing exact-playerId reconciliation."""

    def test_complete_map_when_every_completed_pick_resolves(self):
        """AC1: validated snapshot + complete local pool -> complete map."""
        picks = [make_pick(101, 1), make_pick(102, 2)]
        teams = [make_team(1, "Team A"), make_team(2, "Team B")]
        snapshot = make_snapshot(picks, teams)
        players = [make_local_player("101"), make_local_player("102")]

        result = reconcile_espn_attribution(snapshot, players)

        assert result == {"101": "Team A", "102": "Team B"}

    def test_returns_none_when_completed_playerid_missing_locally(self):
        """AC4: any completed playerId absent from the local pool rejects the
        whole snapshot -- None, never a partial dict."""
        picks = [make_pick(101, 1), make_pick(999, 2)]
        teams = [make_team(1, "Team A"), make_team(2, "Team B")]
        snapshot = make_snapshot(picks, teams)
        players = [make_local_player("101")]

        result = reconcile_espn_attribution(snapshot, players)

        assert result is None

    def test_own_team_picks_included_no_separate_path(self):
        """AC3: our own configured teamId's completed picks flow through the
        same reconciliation as every other team."""
        picks = [make_pick(101, 1), make_pick(102, 7)]
        teams = [make_team(1, "Opponent"), make_team(7, "Sea Sharp")]
        snapshot = make_snapshot(picks, teams)
        players = [make_local_player("101"), make_local_player("102")]

        result = reconcile_espn_attribution(snapshot, players)

        assert result["102"] == "Sea Sharp"

    def test_placeholder_picks_playerid_negative_one_excluded(self):
        """AC5: playerId != -1 is the sole completeness predicate; a
        placeholder row (playerId == -1) is never treated as completed and
        never causes a missing-local-match rejection."""
        picks = [make_pick(101, 1), make_pick(-1, 2)]
        teams = [make_team(1, "Team A"), make_team(2, "Team B")]
        snapshot = make_snapshot(picks, teams)
        players = [make_local_player("101")]

        result = reconcile_espn_attribution(snapshot, players)

        assert result == {"101": "Team A"}

    def test_pick_order_change_produces_different_result_no_caching(self):
        """AC6: the pick grid backing a call is whatever that call's snapshot
        carries -- calling twice with different snapshots yields independently
        correct results (no internal memoization across calls)."""
        players = [make_local_player("101"), make_local_player("102")]

        snapshot_a = make_snapshot(
            [make_pick(101, 1)], [make_team(1, "Team A"), make_team(2, "Team B")]
        )
        result_a = reconcile_espn_attribution(snapshot_a, players)
        assert result_a == {"101": "Team A"}

        snapshot_b = make_snapshot(
            [make_pick(101, 1), make_pick(102, 2)],
            [make_team(1, "Team A"), make_team(2, "Team B")],
        )
        result_b = reconcile_espn_attribution(snapshot_b, players)
        assert result_b == {"101": "Team A", "102": "Team B"}

    def test_int_to_str_normalization_is_the_sole_join_boundary(self):
        """TD3: exact playerId join via one explicit int(ESPN)->str(local)
        normalization; a local id stored as a non-matching string never joins
        (guards against an accidental fuzzy/loose comparison creeping in)."""
        picks = [make_pick(101, 1)]
        teams = [make_team(1, "Team A")]
        snapshot = make_snapshot(picks, teams)
        players = [make_local_player("0101")]

        result = reconcile_espn_attribution(snapshot, players)

        assert result is None
