"""
Unit tests for espn_league_snapshot_models module

Tests Pydantic models, strict field typing, and model-level semantic validation for the ESPN
league draft-snapshot payload.

Author: Kai Mizuno
"""

import pytest
from pydantic import ValidationError

from player_data_fetcher.espn_league_snapshot_models import (
    DraftPick,
    LeagueTeam,
    DraftSettings,
    LeagueSnapshot,
    DEFAULT_POSITION_ID_TO_POSITION,
    LINEUP_SLOT_ID_TO_POSITION,
)


VALID_DRAFT_PICK_KWARGS = dict(overallPickNumber=1, playerId=5, teamId=1, roundId=1, lineupSlotId=2)


class TestDraftPickInitialization:
    """Test DraftPick model initialization"""

    def test_init_with_required_fields(self):
        pick = DraftPick(overallPickNumber=1, playerId=-1, teamId=1, roundId=1, lineupSlotId=2)

        assert pick.overallPickNumber == 1
        assert pick.playerId == -1
        assert pick.teamId == 1
        assert pick.roundId == 1
        assert pick.lineupSlotId == 2

    def test_init_with_all_fields(self):
        pick = DraftPick(
            overallPickNumber=1,
            playerId=100,
            teamId=1,
            roundId=1,
            lineupSlotId=2,
            roundPickNumber=1,
            keeper=False,
            reservedForKeeper=False,
            autoDraftTypeId=0,
            bidAmount=None,
            nominatingTeamId=None,
            tradeLocked=False,
            id=101,
        )

        assert pick.roundPickNumber == 1
        assert pick.keeper is False
        assert pick.reservedForKeeper is False
        assert pick.autoDraftTypeId == 0
        assert pick.bidAmount is None
        assert pick.nominatingTeamId is None
        assert pick.tradeLocked is False
        assert pick.id == 101


@pytest.mark.parametrize("field", ["overallPickNumber", "playerId", "teamId", "roundId", "lineupSlotId"])
@pytest.mark.parametrize("bad_value", ["1", 1.0, True, None])
def test_draft_pick_strict_int_field_rejects_non_int(field, bad_value):
    kwargs = dict(VALID_DRAFT_PICK_KWARGS)
    kwargs[field] = bad_value
    with pytest.raises(ValidationError):
        DraftPick(**kwargs)


@pytest.mark.parametrize("field", ["overallPickNumber", "playerId", "teamId", "roundId", "lineupSlotId"])
def test_draft_pick_missing_required_field_rejected(field):
    kwargs = dict(VALID_DRAFT_PICK_KWARGS)
    del kwargs[field]
    with pytest.raises(ValidationError):
        DraftPick(**kwargs)


class TestLeagueTeamInitialization:
    """Test LeagueTeam model initialization"""

    def test_init_with_required_fields(self):
        team = LeagueTeam(id=1)

        assert team.id == 1

    def test_init_with_all_fields(self):
        team = LeagueTeam(id=1, name="Team One", abbrev="T1")

        assert team.name == "Team One"
        assert team.abbrev == "T1"


@pytest.mark.parametrize("bad_value", ["1", 1.0, True, None])
def test_league_team_strict_int_id_rejects_non_int(bad_value):
    with pytest.raises(ValidationError):
        LeagueTeam(id=bad_value)


def test_league_team_missing_required_id_rejected():
    with pytest.raises(ValidationError):
        LeagueTeam()


class TestDraftSettingsInitialization:
    """Test DraftSettings model initialization"""

    def test_init_with_pick_order(self):
        settings = DraftSettings(pickOrder=[1, 2, 3])

        assert settings.pickOrder == [1, 2, 3]

    def test_init_with_all_fields(self):
        settings = DraftSettings(pickOrder=[1, 2], type="SNAKE", timePerSelection=90)

        assert settings.type == "SNAKE"
        assert settings.timePerSelection == 90


class TestDraftSettingsStrictTyping:
    def test_pick_order_rejects_non_int_entry(self):
        with pytest.raises(ValidationError):
            DraftSettings(pickOrder=["1", 2])


# FIXTURES

@pytest.fixture
def two_team_settings():
    return DraftSettings(pickOrder=[1, 2], type="SNAKE", timePerSelection=90)


@pytest.fixture
def two_teams():
    return [LeagueTeam(id=1, name="Team One"), LeagueTeam(id=2, name="Team Two")]


def _placeholder_pick(overall_pick_number, round_id, team_id):
    return DraftPick(
        overallPickNumber=overall_pick_number,
        playerId=-1,
        teamId=team_id,
        roundId=round_id,
        lineupSlotId=0,
    )


def _completed_pick(overall_pick_number, round_id, team_id, player_id):
    return DraftPick(
        overallPickNumber=overall_pick_number,
        playerId=player_id,
        teamId=team_id,
        roundId=round_id,
        lineupSlotId=2,
    )


class TestLeagueSnapshotValidPayload:
    """Test LeagueSnapshot accepts a valid representative payload (unit.md AC8)."""

    def test_valid_mixed_completed_and_placeholder_payload(self, two_team_settings, two_teams):
        snapshot = LeagueSnapshot(
            picks=[
                _completed_pick(1, 1, 1, 100),
                _placeholder_pick(2, 1, 2),
            ],
            drafted=False,
            inProgress=True,
            teams=two_teams,
            draftSettings=two_team_settings,
        )
        assert len(snapshot.picks) == 2
        assert snapshot.picks[0].playerId == 100
        assert snapshot.picks[1].playerId == -1


class TestLeagueSnapshotDraftLevelFlagsStrict:
    def test_drafted_rejects_non_bool(self, two_team_settings, two_teams):
        with pytest.raises(ValidationError):
            LeagueSnapshot(
                picks=[_placeholder_pick(1, 1, 1)],
                drafted="false",
                inProgress=False,
                teams=two_teams,
                draftSettings=two_team_settings,
            )

    def test_in_progress_rejects_non_bool(self, two_team_settings, two_teams):
        with pytest.raises(ValidationError):
            LeagueSnapshot(
                picks=[_placeholder_pick(1, 1, 1)],
                drafted=False,
                inProgress=0,
                teams=two_teams,
                draftSettings=two_team_settings,
            )


class TestLeagueSnapshotSemanticValidation:
    """Model-level validators (unit.md AC5)."""

    def test_rejects_duplicate_completed_player_id(self, two_team_settings, two_teams):
        with pytest.raises(ValidationError):
            LeagueSnapshot(
                picks=[
                    _completed_pick(1, 1, 1, 100),
                    _completed_pick(2, 1, 2, 100),
                ],
                drafted=True,
                inProgress=False,
                teams=two_teams,
                draftSettings=two_team_settings,
            )

    def test_allows_duplicate_placeholder_player_id(self, two_team_settings, two_teams):
        # playerId == -1 rows are pre-allocated placeholders (spike F11a); duplicates among
        # them are the expected pre-draft shape, never rejected.
        snapshot = LeagueSnapshot(
            picks=[
                _placeholder_pick(1, 1, 1),
                _placeholder_pick(2, 1, 2),
            ],
            drafted=False,
            inProgress=False,
            teams=two_teams,
            draftSettings=two_team_settings,
        )
        assert len(snapshot.picks) == 2

    def test_rejects_duplicate_overall_pick_number(self, two_team_settings, two_teams):
        with pytest.raises(ValidationError):
            LeagueSnapshot(
                picks=[
                    _completed_pick(1, 1, 1, 100),
                    _placeholder_pick(1, 1, 2),
                ],
                drafted=True,
                inProgress=False,
                teams=two_teams,
                draftSettings=two_team_settings,
            )

    def test_rejects_completed_pick_team_id_absent_from_teams(self, two_team_settings, two_teams):
        with pytest.raises(ValidationError):
            LeagueSnapshot(
                picks=[_completed_pick(1, 1, 99, 100)],
                drafted=True,
                inProgress=False,
                teams=two_teams,
                draftSettings=two_team_settings,
            )

    def test_allows_placeholder_pick_team_id_absent_from_teams(self, two_team_settings, two_teams):
        # An unfilled placeholder row's teamId is pre-allocated slot ownership, not a
        # completed-pick relationship — only a completed pick's teamId is checked against
        # teams[] (unit.md AC5's "any COMPLETED pick whose teamId is absent").
        snapshot = LeagueSnapshot(
            picks=[_placeholder_pick(1, 1, 99)],
            drafted=False,
            inProgress=False,
            teams=two_teams,
            draftSettings=two_team_settings,
        )
        assert snapshot.picks[0].teamId == 99


class TestLeagueSnapshotCompletedPickPredicate:
    """playerId != -1 is the sole completed-pick predicate (unit.md AC4)."""

    def test_all_placeholder_payload_has_zero_completed_picks(self, two_team_settings, two_teams):
        snapshot = LeagueSnapshot(
            picks=[_placeholder_pick(1, 1, 1), _placeholder_pick(2, 1, 2)],
            drafted=False,
            inProgress=False,
            teams=two_teams,
            draftSettings=two_team_settings,
        )
        completed = [p for p in snapshot.picks if p.playerId != -1]
        assert len(completed) == 0
        # len(picks) alone would wrongly report 2 "completed" picks (spike F11a) — assert the
        # naive signal and the correct signal disagree on this fixture.
        assert len(snapshot.picks) != len(completed)


class TestPositionEnumLookupTables:
    """Separate lookup tables for defaultPositionId vs lineupSlotId (unit.md AC6)."""

    def test_rb_coincides_across_both_tables(self):
        assert DEFAULT_POSITION_ID_TO_POSITION[2] == "RB"
        assert LINEUP_SLOT_ID_TO_POSITION[2] == "RB"

    def test_wr_diverges_across_both_tables(self):
        # Spike F14a: WR is 3 in defaultPositionId but 4 in lineupSlotId — collapsing them
        # into one table silently mis-positions every WR.
        assert DEFAULT_POSITION_ID_TO_POSITION[3] == "WR"
        assert LINEUP_SLOT_ID_TO_POSITION[4] == "WR"
        assert DEFAULT_POSITION_ID_TO_POSITION.get(4) != "WR"
        assert LINEUP_SLOT_ID_TO_POSITION.get(3) != "WR"

    def test_tables_are_distinct_objects(self):
        assert DEFAULT_POSITION_ID_TO_POSITION is not LINEUP_SLOT_ID_TO_POSITION

    def test_unmapped_lineup_slot_id_raises_key_error_on_direct_indexing(self):
        # 20 is not in the evidenced six-value LINEUP_SLOT_ID_TO_POSITION set (a plausible
        # bench/IR/flex slot per the module docstring's miss contract, not itself evidenced by
        # this unit) — direct [] indexing on a genuine miss must raise KeyError, not return None.
        assert 20 not in LINEUP_SLOT_ID_TO_POSITION
        with pytest.raises(KeyError):
            LINEUP_SLOT_ID_TO_POSITION[20]

    def test_unmapped_lineup_slot_id_get_returns_unknown_sentinel(self):
        # The documented lookup contract is .get(value, 'UNKNOWN'), mirroring the established
        # ESPN_POSITION_MAPPINGS.get(position_id, 'UNKNOWN') idiom (espn_client.py:1478).
        assert LINEUP_SLOT_ID_TO_POSITION.get(20, 'UNKNOWN') == 'UNKNOWN'

    def test_unmapped_default_position_id_get_returns_unknown_sentinel(self):
        assert 20 not in DEFAULT_POSITION_ID_TO_POSITION
        assert DEFAULT_POSITION_ID_TO_POSITION.get(20, 'UNKNOWN') == 'UNKNOWN'


class TestLeagueSnapshotSchemaDrift:
    """A schema-drifting payload fails loudly (unit.md AC8)."""

    def test_missing_required_top_level_key_rejected(self, two_team_settings, two_teams):
        with pytest.raises(ValidationError):
            LeagueSnapshot(
                picks=[_placeholder_pick(1, 1, 1)],
                # drafted omitted entirely
                inProgress=False,
                teams=two_teams,
                draftSettings=two_team_settings,
            )

    def test_wrong_type_for_picks_rejected(self, two_team_settings, two_teams):
        with pytest.raises(ValidationError):
            LeagueSnapshot(
                picks="not-a-list",
                drafted=False,
                inProgress=False,
                teams=two_teams,
                draftSettings=two_team_settings,
            )
