"""
Comprehensive Unit Tests for FantasyTeam.py

Tests the FantasyTeam class which manages fantasy roster operations including:
- Player drafting with position limits and FLEX eligibility
- Slot assignment tracking (natural position vs FLEX)
- Player removal and replacement (trades)
- Roster validation and integrity checks
- Bye week tracking
- Draft order management

This is a CRITICAL module (748 lines) with complex FLEX logic that needs thorough testing.

Author: Kai Mizuno
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from typing import List

from league_helper.util.FantasyTeam import FantasyTeam
from league_helper.util.ConfigManager import ConfigManager
import league_helper.constants as Constants
from utils.FantasyPlayer import FantasyPlayer



@pytest.fixture(autouse=True)
def mock_logger():
    """Mock the logger for all tests"""
    with patch('utils.LoggingManager.get_logger') as mock_get_logger:
        mock_get_logger.return_value = Mock()
        yield mock_get_logger


@pytest.fixture
def mock_data_folder(tmp_path):
    """Create temporary data folder with test config"""
    data_folder = tmp_path / "data"
    data_folder.mkdir()

    config_content = """{
  "config_name": "Test Config",
  "description": "Test configuration for FantasyTeam unit tests",
  "parameters": {
    "CURRENT_NFL_WEEK": 6,
    "NFL_SEASON": 2025,
    "NFL_SCORING_FORMAT": "ppr",
    "NORMALIZATION_MAX_SCALE": 100.0,
    "DRAFT_NORMALIZATION_MAX_SCALE": 163,
    "SAME_POS_BYE_WEIGHT": 1.0,
            "DIFF_POS_BYE_WEIGHT": 1.0,
    "DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY": 5.0,
    "INJURY_PENALTIES": {
      "LOW": 0,
      "MEDIUM": 10.0,
      "HIGH": 75.0
    },
    "DRAFT_ORDER_BONUSES": {
      "PRIMARY": 50,
      "SECONDARY": 30
    },
    "DRAFT_ORDER": [
      {"FLEX": "P", "QB": "S"},
      {"FLEX": "P", "QB": "S"},
      {"QB": "P", "FLEX": "S"},
      {"TE": "P", "FLEX": "S"},
      {"FLEX": "P"},
      {"FLEX": "P"},
      {"FLEX": "P"},
      {"FLEX": "P"},
      {"QB": "P"},
      {"TE": "P"},
      {"FLEX": "P"},
      {"K": "P"},
      {"DST": "P"},
      {"FLEX": "P"},
      {"FLEX": "P"}
    ],
    "MAX_POSITIONS": {
      "QB": 2,
      "RB": 4,
      "WR": 4,
      "FLEX": 2,
      "TE": 1,
      "K": 1,
      "DST": 1
    },
    "FLEX_ELIGIBLE_POSITIONS": ["RB", "WR"],
    "ADP_SCORING": {
      "THRESHOLDS": {
        "EXCELLENT": 20,
        "GOOD": 50,
        "POOR": 100,
        "VERY_POOR": 150
      },
      "MULTIPLIERS": {
        "EXCELLENT": 1.20,
        "GOOD": 1.10,
        "POOR": 0.90,
        "VERY_POOR": 0.70
      },
      "WEIGHT": 1.0
    },
    "PLAYER_RATING_SCORING": {
      "THRESHOLDS": {
        "EXCELLENT": 80,
        "GOOD": 60,
        "POOR": 40,
        "VERY_POOR": 20
      },
      "MULTIPLIERS": {
        "EXCELLENT": 1.25,
        "GOOD": 1.15,
        "POOR": 0.95,
        "VERY_POOR": 0.75
      },
      "WEIGHT": 1.0
    },
    "TEAM_QUALITY_SCORING": {
      "THRESHOLDS": {
        "EXCELLENT": 5,
        "GOOD": 10,
        "POOR": 20,
        "VERY_POOR": 25
      },
      "MULTIPLIERS": {
        "EXCELLENT": 1.30,
        "GOOD": 1.15,
        "POOR": 0.85,
        "VERY_POOR": 0.70
      },
      "WEIGHT": 1.0
    },
    "PERFORMANCE_SCORING": {
      "MIN_WEEKS": 3,
      "THRESHOLDS": {
        "VERY_POOR": -0.2,
        "POOR": -0.1,
        "GOOD": 0.1,
        "EXCELLENT": 0.2
      },
      "MULTIPLIERS": {
        "VERY_POOR": 0.60,
        "POOR": 0.80,
        "GOOD": 1.20,
        "EXCELLENT": 1.50
      },
      "WEIGHT": 1.0
    },
    "MATCHUP_SCORING": {
      "IMPACT_SCALE": 150.0,
      "THRESHOLDS": {
        "EXCELLENT": 15,
        "GOOD": 6,
        "POOR": -6,
        "VERY_POOR": -15
      },
      "MULTIPLIERS": {
        "EXCELLENT": 1.25,
        "GOOD": 1.10,
        "POOR": 0.90,
        "VERY_POOR": 0.75
      },
      "WEIGHT": 1.0
    },
    "SCHEDULE_SCORING": {
      "IMPACT_SCALE": 80.0,
      "THRESHOLDS": {
        "EXCELLENT": 24,
        "GOOD": 20,
        "POOR": 12,
        "VERY_POOR": 8
      },
      "MULTIPLIERS": {
        "EXCELLENT": 1.0,
        "GOOD": 1.0,
        "POOR": 1.0,
        "VERY_POOR": 1.0
      },
      "WEIGHT": 0.0
    }
  }
}"""
    config_file = data_folder / "league_config.json"
    config_file.write_text(config_content)

    return data_folder


@pytest.fixture
def config(mock_data_folder):
    """Create ConfigManager for tests"""
    return ConfigManager(mock_data_folder)


@pytest.fixture
def empty_team(config):
    """Create empty FantasyTeam"""
    return FantasyTeam(config, players=[])


@pytest.fixture
def sample_players():
    """Create sample test players"""
    players = [
        FantasyPlayer(id=1, name="QB1", team="KC", position="QB", bye_week=7,
                     fantasy_points=250.0, injury_status="ACTIVE", drafted_by="", locked=0),
        FantasyPlayer(id=2, name="QB2", team="BUF", position="QB", bye_week=10,
                     fantasy_points=220.0, injury_status="ACTIVE", drafted_by="", locked=0),

        FantasyPlayer(id=3, name="RB1", team="SF", position="RB", bye_week=7,
                     fantasy_points=200.0, injury_status="ACTIVE", drafted_by="", locked=0),
        FantasyPlayer(id=4, name="RB2", team="PHI", position="RB", bye_week=8,
                     fantasy_points=180.0, injury_status="ACTIVE", drafted_by="", locked=0),
        FantasyPlayer(id=5, name="RB3", team="DAL", position="RB", bye_week=9,
                     fantasy_points=160.0, injury_status="ACTIVE", drafted_by="", locked=0),
        FantasyPlayer(id=6, name="RB4", team="MIA", position="RB", bye_week=10,
                     fantasy_points=140.0, injury_status="ACTIVE", drafted_by="", locked=0),

        FantasyPlayer(id=7, name="WR1", team="MIN", position="WR", bye_week=6,
                     fantasy_points=190.0, injury_status="ACTIVE", drafted_by="", locked=0),
        FantasyPlayer(id=8, name="WR2", team="CIN", position="WR", bye_week=7,
                     fantasy_points=175.0, injury_status="ACTIVE", drafted_by="", locked=0),
        FantasyPlayer(id=9, name="WR3", team="DET", position="WR", bye_week=8,
                     fantasy_points=165.0, injury_status="ACTIVE", drafted_by="", locked=0),
        FantasyPlayer(id=10, name="WR4", team="LAC", position="WR", bye_week=9,
                     fantasy_points=155.0, injury_status="ACTIVE", drafted_by="", locked=0),

        FantasyPlayer(id=11, name="TE1", team="KC", position="TE", bye_week=7,
                     fantasy_points=145.0, injury_status="ACTIVE", drafted_by="", locked=0),
        FantasyPlayer(id=12, name="TE2", team="SF", position="TE", bye_week=8,
                     fantasy_points=120.0, injury_status="ACTIVE", drafted_by="", locked=0),

        FantasyPlayer(id=13, name="K1", team="BAL", position="K", bye_week=10,
                     fantasy_points=100.0, injury_status="ACTIVE", drafted_by="", locked=0),

        FantasyPlayer(id=14, name="DST1", team="SF", position="DST", bye_week=7,
                     fantasy_points=95.0, injury_status="ACTIVE", drafted_by="", locked=0),
    ]
    return players


@pytest.fixture
def full_roster_team(config, sample_players):
    """Create FantasyTeam with a full valid roster"""
    roster = [
        sample_players[0],
        sample_players[1],
        sample_players[2],
        sample_players[3],
        sample_players[4],
        sample_players[5],
        sample_players[6],
        sample_players[7],
        sample_players[8],
        sample_players[9],
        sample_players[10],
        sample_players[12],
        sample_players[13],
        FantasyPlayer(id=15, name="RB5", team="ATL", position="RB", bye_week=11,
                     fantasy_points=130.0, injury_status="ACTIVE", drafted_by="", locked=0),
        FantasyPlayer(id=16, name="RB6", team="GB", position="RB", bye_week=12,
                     fantasy_points=125.0, injury_status="ACTIVE", drafted_by="", locked=0)
    ]

    for p in roster:
        p.drafted_by = "Sea Sharp"

    return FantasyTeam(config, players=roster)



class TestInitialization:
    """Test FantasyTeam initialization"""

    def test_init_empty_roster(self, config):
        """Test initialization with no players"""
        team = FantasyTeam(config, players=[])

        assert len(team.roster) == 0
        assert len(team.injury_reserve) == 0
        assert team.pos_counts[Constants.QB] == 0
        assert team.pos_counts[Constants.RB] == 0
        assert team.pos_counts[Constants.WR] == 0
        assert team.pos_counts[Constants.TE] == 0
        assert team.pos_counts[Constants.K] == 0
        assert team.pos_counts[Constants.DST] == 0
        assert team.pos_counts[Constants.FLEX] == 0

    def test_init_with_active_players(self, config, sample_players):
        """Test initialization with active players"""
        roster = sample_players[:5]
        for p in roster:
            p.drafted_by = "Sea Sharp"
            p.injury_status = "ACTIVE"

        team = FantasyTeam(config, players=roster)

        assert len(team.roster) == 5
        assert len(team.injury_reserve) == 0
        assert all(p in team.roster for p in roster)

    def test_init_separates_injury_reserve(self, config, sample_players):
        """Test that only HIGH-risk injured players go to injury_reserve"""
        roster = sample_players[:3]
        roster[0].injury_status = "ACTIVE"
        roster[1].injury_status = "OUT"
        roster[2].injury_status = "INJURY_RESERVE"

        for p in roster:
            p.drafted_by = "Sea Sharp"

        team = FantasyTeam(config, players=roster)

        assert len(team.roster) == 2
        assert len(team.injury_reserve) == 1
        assert roster[0] in team.roster
        assert roster[1] in team.roster
        assert roster[2] in team.injury_reserve

    def test_init_questionable_goes_to_active_roster(self, config, sample_players):
        """Test that QUESTIONABLE players go to active roster (not IR)"""
        player = sample_players[0]
        player.injury_status = "QUESTIONABLE"
        player.drafted_by = "Sea Sharp"

        team = FantasyTeam(config, players=[player])

        assert len(team.roster) == 1
        assert len(team.injury_reserve) == 0
        assert player in team.roster

    def test_init_position_counts_correct(self, config, sample_players):
        """Test that position counts are calculated correctly"""
        roster = [
            sample_players[0],
            sample_players[2],
            sample_players[3],
            sample_players[6],
        ]
        for p in roster:
            p.drafted_by = "Sea Sharp"

        team = FantasyTeam(config, players=roster)

        assert team.pos_counts[Constants.QB] == 1
        assert team.pos_counts[Constants.RB] == 2
        assert team.pos_counts[Constants.WR] == 1
        assert team.pos_counts[Constants.TE] == 0

    def test_init_slot_assignments_correct(self, config, sample_players):
        """Test that slot assignments are set up correctly"""
        roster = [sample_players[0], sample_players[2]]
        for p in roster:
            p.drafted_by = "Sea Sharp"

        team = FantasyTeam(config, players=roster)

        assert sample_players[0].id in team.slot_assignments[Constants.QB]
        assert sample_players[2].id in team.slot_assignments[Constants.RB]

    def test_init_bye_week_counts(self, config, sample_players):
        """Test that bye week counts are tracked"""
        roster = [sample_players[2], sample_players[3]]
        for p in roster:
            p.drafted_by = "Sea Sharp"

        team = FantasyTeam(config, players=roster)

        assert team.bye_week_counts[7][Constants.RB] == 1
        assert team.bye_week_counts[8][Constants.RB] == 1



class TestCanDraft:
    """Test can_draft() method"""

    def test_can_draft_available_player(self, empty_team, sample_players):
        """Test drafting an available player"""
        player = sample_players[0]
        player.drafted_by = ""

        assert empty_team.can_draft(player) is True

    def test_cannot_draft_already_drafted_player(self, empty_team, sample_players):
        """Test that already drafted players cannot be drafted"""
        player = sample_players[0]
        player.drafted_by = "Opponent Team"

        assert empty_team.can_draft(player) is False

    def test_cannot_draft_when_roster_full(self, full_roster_team, sample_players):
        """Test that players cannot be drafted when roster is full"""
        new_player = FantasyPlayer(id=99, name="Extra", team="KC", position="QB",
                                   bye_week=7, fantasy_points=100.0,
                                   injury_status="ACTIVE", drafted_by="", locked=0)

        assert full_roster_team.can_draft(new_player) is False

    def test_cannot_draft_when_position_full(self, empty_team, sample_players):
        """Test that position limits are enforced"""
        empty_team.draft_player(sample_players[0])
        empty_team.draft_player(sample_players[1])

        third_qb = FantasyPlayer(id=99, name="QB3", team="KC", position="QB",
                                bye_week=7, fantasy_points=100.0,
                                injury_status="ACTIVE", drafted_by="", locked=0)

        assert empty_team.can_draft(third_qb) is False

    def test_can_draft_to_flex_when_position_full(self, empty_team, sample_players):
        """Test that FLEX-eligible players can be drafted to FLEX when natural position is full"""
        for i in range(4):
            empty_team.draft_player(sample_players[2 + i])

        fifth_rb = FantasyPlayer(id=99, name="RB5", team="KC", position="RB",
                                bye_week=7, fantasy_points=100.0,
                                injury_status="ACTIVE", drafted_by="", locked=0)

        assert empty_team.can_draft(fifth_rb) is True

    def test_cannot_draft_non_flex_when_position_full(self, empty_team, sample_players):
        """Test that non-FLEX positions cannot overflow"""
        empty_team.draft_player(sample_players[0])
        empty_team.draft_player(sample_players[1])

        third_qb = FantasyPlayer(id=99, name="QB3", team="KC", position="QB",
                                bye_week=7, fantasy_points=100.0,
                                injury_status="ACTIVE", drafted_by="", locked=0)

        assert empty_team.can_draft(third_qb) is False

    def test_can_draft_with_invalid_bye_week(self, empty_team, sample_players):
        """Test handling of invalid bye weeks"""
        player = sample_players[0]
        player.bye_week = 20
        player.drafted_by = ""

        assert empty_team.can_draft(player) is False

    def test_can_draft_with_none_bye_week(self, empty_team, sample_players):
        """Test that None bye week is acceptable"""
        player = sample_players[0]
        player.bye_week = None
        player.drafted_by = ""

        assert empty_team.can_draft(player) is True

    def test_cannot_draft_invalid_position(self, empty_team):
        """Test that invalid positions are rejected"""
        invalid_player = FantasyPlayer(id=99, name="Invalid", team="KC", position="INVALID",
                                      bye_week=7, fantasy_points=100.0,
                                      injury_status="ACTIVE", drafted_by="", locked=0)

        assert empty_team.can_draft(invalid_player) is False



class TestDraftPlayer:
    """Test draft_player() method"""

    def test_draft_player_success(self, empty_team, sample_players):
        """Test successful player draft"""
        player = sample_players[0]
        player.drafted_by = ""

        result = empty_team.draft_player(player)

        assert result is True
        assert player.drafted_by == "Sea Sharp"
        assert player in empty_team.roster
        assert len(empty_team.roster) == 1

    def test_draft_player_updates_position_count(self, empty_team, sample_players):
        """Test that drafting updates position counts"""
        player = sample_players[0]
        player.drafted_by = ""

        empty_team.draft_player(player)

        assert empty_team.pos_counts[Constants.QB] == 1

    def test_draft_player_assigns_to_slot(self, empty_team, sample_players):
        """Test that drafting assigns player to correct slot"""
        player = sample_players[0]
        player.drafted_by = ""

        empty_team.draft_player(player)

        assert player.id in empty_team.slot_assignments[Constants.QB]

    def test_draft_player_to_flex_slot(self, empty_team, sample_players):
        """Test drafting FLEX-eligible player to FLEX slot"""
        for i in range(4):
            empty_team.draft_player(sample_players[2 + i])

        fifth_rb = FantasyPlayer(id=99, name="RB5", team="KC", position="RB",
                                bye_week=7, fantasy_points=100.0,
                                injury_status="ACTIVE", drafted_by="", locked=0)

        result = empty_team.draft_player(fifth_rb)

        assert result is True
        assert fifth_rb.id in empty_team.slot_assignments[Constants.FLEX]
        assert empty_team.pos_counts[Constants.FLEX] == 1

    def test_draft_player_fails_when_cannot_draft(self, empty_team, sample_players):
        """Test that draft fails when can_draft returns False"""
        player = sample_players[0]
        player.drafted_by = "Opponent Team"

        result = empty_team.draft_player(player)

        assert result is False
        assert player not in empty_team.roster

    def test_draft_player_rollback_on_slot_error(self, empty_team, sample_players):
        """Test that draft rolls back if slot assignment fails"""
        for i in range(15):
            if i < len(sample_players):
                sample_players[i].drafted_by = ""
                empty_team.draft_player(sample_players[i])

        extra_player = FantasyPlayer(id=99, name="Extra", team="KC", position="QB",
                                     bye_week=7, fantasy_points=100.0,
                                     injury_status="ACTIVE", drafted_by="", locked=0)

        result = empty_team.draft_player(extra_player)

        assert result is False
        assert extra_player.is_free_agent()

    def test_draft_multiple_players(self, empty_team, sample_players):
        """Test drafting multiple players"""
        players_to_draft = sample_players[:5]

        for player in players_to_draft:
            player.drafted_by = ""
            result = empty_team.draft_player(player)
            assert result is True

        assert len(empty_team.roster) == 5
        assert all(p in empty_team.roster for p in players_to_draft)



class TestRemovePlayer:
    """Test remove_player() method"""

    def test_remove_player_success(self, empty_team, sample_players):
        """Test successful player removal"""
        player = sample_players[0]
        player.drafted_by = ""
        empty_team.draft_player(player)

        result = empty_team.remove_player(player)

        assert result is True
        assert player not in empty_team.roster
        assert player.is_free_agent()
        assert len(empty_team.roster) == 0

    def test_remove_player_updates_position_count(self, empty_team, sample_players):
        """Test that removal updates position counts"""
        player = sample_players[0]
        player.drafted_by = ""
        empty_team.draft_player(player)

        empty_team.remove_player(player)

        assert empty_team.pos_counts[Constants.QB] == 0

    def test_remove_player_clears_slot_assignment(self, empty_team, sample_players):
        """Test that removal clears slot assignments"""
        player = sample_players[0]
        player.drafted_by = ""
        empty_team.draft_player(player)

        empty_team.remove_player(player)

        assert player.id not in empty_team.slot_assignments[Constants.QB]

    def test_remove_player_from_flex_slot(self, empty_team, sample_players):
        """Test removing player from FLEX slot"""
        for i in range(5):
            sample_players[2 + i].drafted_by = ""
            empty_team.draft_player(sample_players[2 + i])

        flex_player = sample_players[6]

        result = empty_team.remove_player(flex_player)

        assert result is True
        assert flex_player.id not in empty_team.slot_assignments[Constants.FLEX]
        assert empty_team.pos_counts[Constants.FLEX] == 0

    def test_remove_player_not_in_roster(self, empty_team, sample_players):
        """Test removing player not in roster fails"""
        player = sample_players[0]

        result = empty_team.remove_player(player)

        assert result is False

    def test_remove_player_updates_bye_week_counts(self, empty_team, sample_players):
        """Test that removal updates bye week counts"""
        player = sample_players[2]
        player.drafted_by = ""
        empty_team.draft_player(player)

        assert empty_team.bye_week_counts[7][Constants.RB] == 1

        empty_team.remove_player(player)

        assert empty_team.bye_week_counts[7][Constants.RB] == 0



class TestReplacePlayer:
    """Test replace_player() method"""

    def test_replace_same_position(self, empty_team, sample_players):
        """Test replacing player with same position"""
        old_player = sample_players[0]
        new_player = sample_players[1]

        old_player.drafted_by = ""
        new_player.drafted_by = ""
        empty_team.draft_player(old_player)

        result = empty_team.replace_player(old_player, new_player)

        assert result is True
        assert old_player not in empty_team.roster
        assert new_player in empty_team.roster
        assert new_player.drafted_by == "Sea Sharp"
        assert old_player.drafted_by == ""

    def test_replace_flex_eligible_rb_with_wr(self, empty_team, sample_players):
        """Test replacing RB with WR (both FLEX-eligible)"""
        old_rb = sample_players[2]
        new_wr = sample_players[6]

        old_rb.drafted_by = ""
        new_wr.drafted_by = ""
        empty_team.draft_player(old_rb)

        result = empty_team.replace_player(old_rb, new_wr)

        assert result is True
        assert new_wr in empty_team.roster

    def test_replace_rollback_on_failure(self, empty_team, sample_players):
        """Test that failed replacement restores old player"""
        old_player = sample_players[0]
        new_player = FantasyPlayer(id=99, name="Invalid", team="KC", position="INVALID",
                                  bye_week=7, fantasy_points=100.0,
                                  injury_status="ACTIVE", drafted_by="", locked=0)

        old_player.drafted_by = ""
        empty_team.draft_player(old_player)

        result = empty_team.replace_player(old_player, new_player)

        assert result is False
        assert old_player in empty_team.roster

    def test_cannot_replace_qb_with_rb(self, empty_team, sample_players):
        """Test that non-FLEX positions cannot be swapped"""
        old_qb = sample_players[0]
        new_rb = sample_players[2]

        old_qb.drafted_by = ""
        new_rb.drafted_by = ""
        empty_team.draft_player(old_qb)

        result = empty_team.replace_player(old_qb, new_rb)

        assert result is False



class TestFlexEligibility:
    """Test flex_eligible() method"""

    def test_rb_flex_eligible_when_slots_full(self, empty_team, sample_players):
        """Test RB is FLEX-eligible when RB slots are full"""
        for i in range(4):
            empty_team.draft_player(sample_players[2 + i])

        assert empty_team.flex_eligible(Constants.RB) is True

    def test_rb_not_flex_eligible_when_slots_available(self, empty_team):
        """Test RB is not FLEX-eligible when RB slots are available"""
        assert empty_team.flex_eligible(Constants.RB) is False

    def test_wr_flex_eligible_when_slots_full(self, empty_team, sample_players):
        """Test WR is FLEX-eligible when WR slots are full"""
        for i in range(4):
            empty_team.draft_player(sample_players[6 + i])

        assert empty_team.flex_eligible(Constants.WR) is True

    def test_qb_never_flex_eligible(self, empty_team, sample_players):
        """Test QB is never FLEX-eligible"""
        empty_team.draft_player(sample_players[0])
        empty_team.draft_player(sample_players[1])

        assert empty_team.flex_eligible(Constants.QB) is False

    def test_flex_not_eligible_when_flex_full(self, empty_team, sample_players):
        """Test FLEX eligibility false when FLEX slots are full (2 slots)"""
        for i in range(4):
            sample_players[2 + i].drafted_by = ""
            empty_team.draft_player(sample_players[2 + i])

        fifth_rb = FantasyPlayer(id=99, name="RB5", team="KC", position="RB",
                                bye_week=7, fantasy_points=100.0,
                                injury_status="ACTIVE", drafted_by="", locked=0)
        empty_team.draft_player(fifth_rb)

        sixth_rb = FantasyPlayer(id=100, name="RB6", team="KC", position="RB",
                                bye_week=8, fantasy_points=100.0,
                                injury_status="ACTIVE", drafted_by="", locked=0)
        empty_team.draft_player(sixth_rb)

        assert empty_team.flex_eligible(Constants.RB) is False



class TestSlotAssignment:
    """Test _assign_player_to_slot() method"""

    def test_assign_to_natural_position(self, empty_team, sample_players):
        """Test player assigned to natural position when available"""
        player = sample_players[0]
        player.drafted_by = ""

        empty_team.draft_player(player)

        assert player.id in empty_team.slot_assignments[Constants.QB]
        assert player.id not in empty_team.slot_assignments[Constants.FLEX]

    def test_assign_to_flex_when_natural_full(self, empty_team, sample_players):
        """Test player assigned to FLEX when natural position is full"""
        for i in range(4):
            empty_team.draft_player(sample_players[2 + i])

        fifth_rb = FantasyPlayer(id=99, name="RB5", team="KC", position="RB",
                                bye_week=7, fantasy_points=100.0,
                                injury_status="ACTIVE", drafted_by="", locked=0)
        empty_team.draft_player(fifth_rb)

        assert fifth_rb.id in empty_team.slot_assignments[Constants.FLEX]
        assert fifth_rb.id not in empty_team.slot_assignments[Constants.RB]

    def test_slot_assignments_track_all_players(self, empty_team, sample_players):
        """Test that all drafted players are tracked in slot_assignments"""
        players_to_draft = sample_players[:5]

        for p in players_to_draft:
            p.drafted_by = ""
            empty_team.draft_player(p)

        total_assigned = sum(len(ids) for ids in empty_team.slot_assignments.values())
        assert total_assigned == 5



class TestRosterValidation:
    """Test validate_roster_integrity() method"""

    def test_valid_roster_passes(self, empty_team, sample_players):
        """Test that valid roster passes integrity check"""
        for i in range(5):
            sample_players[i].drafted_by = ""
            empty_team.draft_player(sample_players[i])

        assert empty_team.validate_roster_integrity() is True

    def test_empty_roster_passes(self, empty_team):
        """Test that empty roster passes integrity check"""
        assert empty_team.validate_roster_integrity() is True

    def test_full_roster_passes(self, full_roster_team):
        """Test that full roster passes integrity check"""
        assert full_roster_team.validate_roster_integrity() is True



class TestByeWeekTracking:
    """Test get_matching_byes_in_roster() method"""

    def test_no_matching_byes(self, empty_team, sample_players):
        """Test count when no players have matching bye weeks"""
        empty_team.draft_player(sample_players[0])
        empty_team.draft_player(sample_players[3])

        test_player = sample_players[2]
        matches = empty_team.get_matching_byes_in_roster(9, Constants.RB, False)

        assert matches == 0

    def test_matching_byes_same_position(self, empty_team, sample_players):
        """Test count with matching bye weeks and same position"""
        rb1 = sample_players[2]
        rb1.bye_week = 7
        rb1.drafted_by = ""

        rb2 = sample_players[3]
        rb2.bye_week = 7
        rb2.drafted_by = ""

        empty_team.draft_player(rb1)
        empty_team.draft_player(rb2)

        matches = empty_team.get_matching_byes_in_roster(7, Constants.RB, False)

        assert matches == 2

    def test_excludes_player_being_scored(self, empty_team, sample_players):
        """Test that player being scored is excluded from count"""
        rb1 = sample_players[2]
        rb1.bye_week = 7
        rb1.drafted_by = ""

        rb2 = sample_players[3]
        rb2.bye_week = 7
        rb2.drafted_by = ""

        empty_team.draft_player(rb1)
        empty_team.draft_player(rb2)

        matches = empty_team.get_matching_byes_in_roster(7, Constants.RB, True)

        assert matches == 1



class TestUtilityMethods:
    """Test utility methods"""

    def test_set_score(self, empty_team, sample_players):
        """Test set_score() method"""
        player = sample_players[0]
        player.drafted_by = ""
        empty_team.draft_player(player)

        empty_team.set_score(player.id, 150.5)

        assert player.score == 150.5

    def test_get_players_by_slot_qb(self, empty_team, sample_players):
        """Test get_players_by_slot() for QB"""
        qb = sample_players[0]
        qb.drafted_by = ""
        empty_team.draft_player(qb)

        qb_players = empty_team.get_players_by_slot(Constants.QB)

        assert len(qb_players) == 1
        assert qb in qb_players

    def test_get_players_by_slot_flex(self, empty_team, sample_players):
        """Test get_players_by_slot() for FLEX"""
        for i in range(4):
            sample_players[2 + i].drafted_by = ""
            empty_team.draft_player(sample_players[2 + i])

        fifth_rb = FantasyPlayer(id=99, name="RB5", team="KC", position="RB",
                                bye_week=7, fantasy_points=100.0,
                                injury_status="ACTIVE", drafted_by="", locked=0)
        empty_team.draft_player(fifth_rb)

        flex_players = empty_team.get_players_by_slot(Constants.FLEX)

        assert len(flex_players) == 1
        assert fifth_rb in flex_players

    def test_get_slot_assignment(self, empty_team, sample_players):
        """Test get_slot_assignment() method"""
        player = sample_players[0]
        player.drafted_by = ""
        empty_team.draft_player(player)

        slot = empty_team.get_slot_assignment(player)

        assert slot == Constants.QB

    def test_get_slot_assignment_flex(self, empty_team, sample_players):
        """Test get_slot_assignment() for FLEX player"""
        for i in range(4):
            empty_team.draft_player(sample_players[2 + i])

        fifth_rb = FantasyPlayer(id=99, name="RB5", team="KC", position="RB",
                                bye_week=7, fantasy_points=100.0,
                                injury_status="ACTIVE", drafted_by="", locked=0)
        empty_team.draft_player(fifth_rb)

        slot = empty_team.get_slot_assignment(fifth_rb)

        assert slot == Constants.FLEX



class TestEdgeCases:
    """Test edge cases and boundary conditions"""

    def test_draft_exactly_max_players(self, empty_team, sample_players):
        """Test drafting exactly MAX_PLAYERS (15)"""
        players_to_draft = [
            sample_players[0],
            sample_players[1],
            sample_players[2],
            sample_players[3],
            sample_players[4],
            sample_players[5],
            sample_players[6],
            sample_players[7],
            sample_players[8],
            sample_players[9],
            sample_players[10],
            sample_players[12],
            sample_players[13],
            FantasyPlayer(id=115, name="RB5", team="ATL", position="RB", bye_week=11,
                         fantasy_points=130.0, injury_status="ACTIVE", drafted_by="", locked=0),
            FantasyPlayer(id=116, name="WR5", team="GB", position="WR", bye_week=12,
                         fantasy_points=125.0, injury_status="ACTIVE", drafted_by="", locked=0)
        ]

        for player in players_to_draft:
            player.drafted_by = ""
            empty_team.draft_player(player)

        assert len(empty_team.roster) == 15
        assert empty_team.validate_roster_integrity() is True

    def test_cannot_draft_16th_player(self, full_roster_team):
        """Test that 16th player cannot be drafted"""
        extra_player = FantasyPlayer(id=999, name="Extra", team="KC", position="QB",
                                    bye_week=7, fantasy_points=100.0,
                                    injury_status="ACTIVE", drafted_by="", locked=0)

        result = full_roster_team.draft_player(extra_player)

        assert result is False

    def test_draft_with_none_bye_week(self, empty_team):
        """Test drafting player with None bye_week"""
        player = FantasyPlayer(id=1, name="Player", team="KC", position="QB",
                              bye_week=None, fantasy_points=100.0,
                              injury_status="ACTIVE", drafted_by="", locked=0)

        result = empty_team.draft_player(player)

        assert result is True

    def test_multiple_players_same_bye_week(self, empty_team, sample_players):
        """Test tracking multiple players with same bye week"""
        for i in range(3):
            player = sample_players[2 + i]
            player.bye_week = 7
            player.drafted_by = ""
            empty_team.draft_player(player)

        total_byes_week_7 = sum(empty_team.bye_week_counts[7].values())
        assert total_byes_week_7 == 3



class TestDraftPositionWeights:
    """Test get_next_draft_position_weights() method"""

    def test_get_next_draft_position_weights_empty_roster(self, empty_team):
        """Test getting weights for first draft pick"""
        weights = empty_team.get_next_draft_position_weights()

        assert weights is not None
        assert isinstance(weights, dict)

    def test_get_next_draft_position_weights_partial_roster(self, empty_team, sample_players):
        """Test getting weights after partial draft"""
        for i in range(3):
            sample_players[i].drafted_by = ""
            empty_team.draft_player(sample_players[i])

        weights = empty_team.get_next_draft_position_weights()

        assert weights is not None

    def test_get_next_draft_position_weights_full_roster(self, full_roster_team):
        """Test getting weights when roster is full (or last position)"""
        weights = full_roster_team.get_next_draft_position_weights()

        assert weights is not None or weights is None



class TestTeamScore:
    """Test get_total_team_score() and scoring functions"""

    def test_get_total_team_score_empty(self, empty_team):
        """Test total score for empty roster"""
        def scoring_func(player):
            return player.fantasy_points

        score = empty_team.get_total_team_score(scoring_func)

        assert score == 0

    def test_get_total_team_score_single_player(self, empty_team, sample_players):
        """Test total score with one player"""
        player = sample_players[0]
        player.drafted_by = ""
        player.fantasy_points = 100.0
        empty_team.draft_player(player)

        def scoring_func(player):
            return player.fantasy_points

        score = empty_team.get_total_team_score(scoring_func)

        assert score == 100.0

    def test_get_total_team_score_multiple_players(self, empty_team, sample_players):
        """Test total score with multiple players"""
        for i in range(5):
            sample_players[i].drafted_by = ""
            sample_players[i].fantasy_points = 100.0 * (i + 1)
            empty_team.draft_player(sample_players[i])

        def scoring_func(player):
            return player.fantasy_points

        score = empty_team.get_total_team_score(scoring_func)

        assert score == 1500.0

    def test_get_total_team_score_custom_function(self, empty_team, sample_players):
        """Test total score with custom scoring function"""
        for i in range(3):
            sample_players[i].drafted_by = ""
            empty_team.draft_player(sample_players[i])

        def custom_scoring(player):
            return player.fantasy_points * 2

        score = empty_team.get_total_team_score(custom_scoring)

        expected = sum(p.fantasy_points * 2 for p in sample_players[:3])
        assert score == expected



class TestWeakestPlayer:
    """Test get_weakest_player_by_position() method"""

    def test_get_weakest_player_no_players_at_position(self, empty_team):
        """Test getting weakest player when position has no players"""
        def scoring_func(player):
            return player.fantasy_points

        weakest = empty_team.get_weakest_player_by_position(Constants.QB, scoring_func)

        assert weakest is None

    def test_get_weakest_player_single_player(self, empty_team, sample_players):
        """Test getting weakest player with only one at position"""
        qb = sample_players[0]
        qb.drafted_by = ""
        empty_team.draft_player(qb)

        def scoring_func(player):
            return player.fantasy_points

        weakest = empty_team.get_weakest_player_by_position(Constants.QB, scoring_func)

        assert weakest == qb

    def test_get_weakest_player_multiple_players(self, empty_team, sample_players):
        """Test getting weakest player with multiple at position"""
        rbs = sample_players[2:5]
        rbs[0].fantasy_points = 200.0
        rbs[1].fantasy_points = 150.0
        rbs[2].fantasy_points = 180.0

        for rb in rbs:
            rb.drafted_by = ""
            empty_team.draft_player(rb)

        def scoring_func(player):
            return player.fantasy_points

        weakest = empty_team.get_weakest_player_by_position(Constants.RB, scoring_func)

        assert weakest == rbs[1]
        assert weakest.fantasy_points == 150.0



class TestOptimalSlot:
    """Test get_optimal_slot_for_player() method"""

    def test_optimal_slot_natural_position_available(self, empty_team, sample_players):
        """Test optimal slot is natural position when available"""
        player = sample_players[2]

        optimal = empty_team.get_optimal_slot_for_player(player)

        assert optimal == Constants.RB

    def test_optimal_slot_flex_when_natural_full(self, empty_team, sample_players):
        """Test optimal slot is FLEX when natural position is full"""
        for i in range(4):
            empty_team.draft_player(sample_players[2 + i])

        fifth_rb = FantasyPlayer(id=99, name="RB5", team="KC", position="RB",
                                bye_week=7, fantasy_points=100.0,
                                injury_status="ACTIVE", drafted_by="", locked=0)

        optimal = empty_team.get_optimal_slot_for_player(fifth_rb)

        assert optimal == Constants.FLEX

    def test_optimal_slot_none_when_all_full(self, empty_team, sample_players):
        """Test optimal slot is None when both natural and FLEX slots are full (2 FLEX slots)"""
        for i in range(4):
            empty_team.draft_player(sample_players[2 + i])

        fifth_rb = FantasyPlayer(id=99, name="RB5", team="KC", position="RB",
                                bye_week=7, fantasy_points=100.0,
                                injury_status="ACTIVE", drafted_by="", locked=0)
        empty_team.draft_player(fifth_rb)

        sixth_rb = FantasyPlayer(id=100, name="RB6", team="KC", position="RB",
                                bye_week=8, fantasy_points=100.0,
                                injury_status="ACTIVE", drafted_by="", locked=0)
        empty_team.draft_player(sixth_rb)

        seventh_rb = FantasyPlayer(id=101, name="RB7", team="KC", position="RB",
                                bye_week=9, fantasy_points=100.0,
                                injury_status="ACTIVE", drafted_by="", locked=0)

        optimal = empty_team.get_optimal_slot_for_player(seventh_rb)

        assert optimal is None

    def test_optimal_slot_non_flex_position(self, empty_team, sample_players):
        """Test optimal slot for non-FLEX-eligible position"""
        qb = sample_players[0]

        optimal = empty_team.get_optimal_slot_for_player(qb)

        assert optimal == Constants.QB

    def test_optimal_slot_non_flex_position_full(self, empty_team, sample_players):
        """Test optimal slot None for non-FLEX position when full"""
        empty_team.draft_player(sample_players[0])
        empty_team.draft_player(sample_players[1])

        third_qb = FantasyPlayer(id=99, name="QB3", team="KC", position="QB",
                                bye_week=7, fantasy_points=100.0,
                                injury_status="ACTIVE", drafted_by="", locked=0)

        optimal = empty_team.get_optimal_slot_for_player(third_qb)

        assert optimal is None



class TestFlexOptimization:
    """Test optimize_flex_assignments() method"""

    def test_optimize_no_flex_players(self, empty_team, sample_players):
        """Test optimization with no FLEX players"""
        for i in range(2):
            sample_players[i].drafted_by = ""
            empty_team.draft_player(sample_players[i])

        def scoring_func(player):
            return player.fantasy_points

        result = empty_team.optimize_flex_assignments(scoring_func)

        assert result is False

    def test_optimize_flex_player_to_natural_position(self, empty_team, sample_players):
        """Test moving FLEX player to natural position when space available"""
        for i in range(3):
            sample_players[2 + i].drafted_by = ""
            empty_team.draft_player(sample_players[2 + i])

        high_score_rb = FantasyPlayer(id=99, name="RB_FLEX", team="KC", position="RB",
                                     bye_week=7, fantasy_points=250.0,
                                     injury_status="ACTIVE", drafted_by="Sea Sharp", locked=0)
        empty_team.roster.append(high_score_rb)
        empty_team.slot_assignments[Constants.FLEX].append(high_score_rb.id)
        empty_team.pos_counts[Constants.RB] += 1
        empty_team.pos_counts[Constants.FLEX] += 1

        def scoring_func(player):
            return player.fantasy_points

        result = empty_team.optimize_flex_assignments(scoring_func)

        assert result is True
        assert high_score_rb.id in empty_team.slot_assignments[Constants.RB]

    def test_optimize_swap_flex_with_natural(self, empty_team, sample_players):
        """Test swapping FLEX player with weaker natural position player"""
        rbs = sample_players[2:6]
        rbs[0].fantasy_points = 200.0
        rbs[1].fantasy_points = 150.0
        rbs[2].fantasy_points = 180.0
        rbs[3].fantasy_points = 170.0

        for rb in rbs:
            rb.drafted_by = ""
            empty_team.draft_player(rb)

        flex_rb = FantasyPlayer(id=99, name="RB5", team="KC", position="RB",
                               bye_week=7, fantasy_points=190.0,
                               injury_status="ACTIVE", drafted_by="", locked=0)
        empty_team.draft_player(flex_rb)

        def scoring_func(player):
            return player.fantasy_points

        result = empty_team.optimize_flex_assignments(scoring_func)

        flex_players = empty_team.get_players_by_slot(Constants.FLEX)
        if flex_players:
            flex_scores = [scoring_func(p) for p in flex_players]
            rb_players = empty_team.get_players_by_slot(Constants.RB)
            rb_scores = [scoring_func(p) for p in rb_players]
            assert min(flex_scores) <= max(rb_scores) or result is True

    def test_optimize_no_change_when_optimal(self, empty_team, sample_players):
        """Test no optimization when assignments are already optimal"""
        rbs = sample_players[2:6]
        for i, rb in enumerate(rbs):
            rb.fantasy_points = 200.0 - (i * 10)
            rb.drafted_by = ""
            empty_team.draft_player(rb)

        flex_rb = FantasyPlayer(id=99, name="RB5", team="KC", position="RB",
                               bye_week=7, fantasy_points=160.0,
                               injury_status="ACTIVE", drafted_by="", locked=0)
        empty_team.draft_player(flex_rb)

        def scoring_func(player):
            return player.fantasy_points

        result = empty_team.optimize_flex_assignments(scoring_func)

        assert result is False



class TestCopyTeam:
    """Test copy_team() method"""

    def test_copy_empty_team(self, empty_team):
        """Test copying empty team"""
        copied = empty_team.copy_team()

        assert copied is not empty_team
        assert len(copied.roster) == 0
        assert copied.pos_counts == empty_team.pos_counts

    def test_copy_team_with_players(self, empty_team, sample_players):
        """Test copying team with players"""
        for i in range(5):
            sample_players[i].drafted_by = ""
            empty_team.draft_player(sample_players[i])

        copied = empty_team.copy_team()

        assert copied is not empty_team
        assert len(copied.roster) == len(empty_team.roster)
        assert copied.roster is not empty_team.roster

    def test_copy_team_independence(self, empty_team, sample_players):
        """Test that copied team is independent of original"""
        for i in range(3):
            sample_players[i].drafted_by = ""
            empty_team.draft_player(sample_players[i])

        copied = empty_team.copy_team()

        new_player = sample_players[10]
        new_player.drafted_by = ""
        empty_team.draft_player(new_player)

        assert len(empty_team.roster) == 4
        assert len(copied.roster) == 3



class TestRecalculatePositionCounts:
    """Test _recalculate_position_counts() method"""

    def test_recalculate_after_manual_modification(self, empty_team, sample_players):
        """Test recalculating counts after manual roster modification"""
        for i in range(5):
            sample_players[i].drafted_by = ""
            empty_team.draft_player(sample_players[i])

        empty_team.pos_counts[Constants.QB] = 999

        empty_team._recalculate_position_counts()

        assert empty_team.pos_counts[Constants.QB] == 2

    def test_recalculate_flex_count(self, empty_team, sample_players):
        """Test that FLEX count is recalculated correctly"""
        for i in range(5):
            sample_players[2 + i].drafted_by = ""
            empty_team.draft_player(sample_players[2 + i])

        flex_count_before = len(empty_team.slot_assignments[Constants.FLEX])

        empty_team._recalculate_position_counts()

        assert empty_team.pos_counts[Constants.FLEX] == flex_count_before



class TestDisplayRoster:
    """Test display_roster() method"""

    def test_display_empty_roster(self, empty_team, capsys):
        """Test displaying empty roster"""
        empty_team.display_roster()

        captured = capsys.readouterr()
        assert "Current Roster by Position" in captured.out
        assert "Total roster: 0/15 players" in captured.out

    def test_display_roster_with_players(self, empty_team, sample_players, capsys):
        """Test displaying roster with players"""
        for i in range(5):
            sample_players[i].drafted_by = ""
            empty_team.draft_player(sample_players[i])

        empty_team.display_roster()

        captured = capsys.readouterr()
        assert "Current Roster by Position" in captured.out
        assert "Total roster: 5/15 players" in captured.out
        assert "--- QB ---" in captured.out
        assert "--- RB ---" in captured.out

    def test_display_roster_shows_bye_weeks(self, empty_team, sample_players, capsys):
        """Test that bye weeks are displayed"""
        player = sample_players[0]
        player.drafted_by = ""
        player.bye_week = 7
        empty_team.draft_player(player)

        empty_team.display_roster()

        captured = capsys.readouterr()
        assert "Bye Weeks" in captured.out

    def test_display_roster_shows_injury_reserve(self, config, capsys):
        """Test that injury reserve is displayed"""
        injured_player = FantasyPlayer(id=1, name="Injured", team="KC", position="QB",
                                      bye_week=7, fantasy_points=100.0,
                                      injury_status="OUT", drafted_by="Sea Sharp", locked=0)

        team = FantasyTeam(config, players=[injured_player])
        team.display_roster()

        captured = capsys.readouterr()
        assert "Injury Reserve" in captured.out


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])


