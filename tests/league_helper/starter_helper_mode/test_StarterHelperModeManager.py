"""
Unit Tests for StarterHelperModeManager

Tests the StarterHelperModeManager class and OptimalLineup class which handle
lineup optimization for weekly fantasy football starting decisions. Verifies
proper assignment of players to starting positions (QB, RB1, RB2, WR1, WR2, TE,
FLEX, K, DST) and bench overflow handling.

Author: Claude Code
Date: 2025-10-10
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch
from typing import List

# Add league_helper to path
sys.path.append(str(Path(__file__).parent.parent.parent.parent / "league_helper"))
from starter_helper_mode.StarterHelperModeManager import StarterHelperModeManager, OptimalLineup
from util.ScoredPlayer import ScoredPlayer
from util.ConfigManager import ConfigManager
from util.PlayerManager import PlayerManager
from util.TeamDataManager import TeamDataManager

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from utils.FantasyPlayer import FantasyPlayer


class TestOptimalLineupInitialization:
    """Test OptimalLineup class initialization and slot assignment"""

    def test_optimal_lineup_empty_roster(self):
        """Test OptimalLineup with empty roster"""
        lineup = OptimalLineup([])

        assert lineup.qb is None
        assert lineup.rb1 is None
        assert lineup.rb2 is None
        assert lineup.wr1 is None
        assert lineup.wr2 is None
        assert lineup.te is None
        assert lineup.flex is None
        assert lineup.k is None
        assert lineup.dst is None
        assert len(lineup.bench) == 0
        assert lineup.total_projected_points == 0.0

    def test_optimal_lineup_single_qb(self):
        """Test OptimalLineup with single QB"""
        player = FantasyPlayer(id=1, name="Patrick Mahomes", team="KC", position="QB")
        scored_player = ScoredPlayer(player, 25.5, ["Test reason"])

        lineup = OptimalLineup([scored_player])

        assert lineup.qb == scored_player
        assert lineup.qb.player.name == "Patrick Mahomes"
        assert lineup.total_projected_points == 25.5

    def test_optimal_lineup_two_qbs_bench_overflow(self):
        """Test OptimalLineup with two QBs - second goes to bench"""
        qb1 = ScoredPlayer(FantasyPlayer(id=1, name="QB1", team="KC", position="QB"), 30.0, [])
        qb2 = ScoredPlayer(FantasyPlayer(id=2, name="QB2", team="BUF", position="QB"), 25.0, [])

        lineup = OptimalLineup([qb1, qb2])

        # Higher scored QB1 should start
        assert lineup.qb == qb1
        assert lineup.qb.player.name == "QB1"
        # QB2 should be on bench
        assert len(lineup.bench) == 1
        assert lineup.bench[0] == qb2
        assert lineup.total_projected_points == 30.0

    def test_optimal_lineup_running_backs(self):
        """Test OptimalLineup with multiple RBs fills RB1, RB2, and FLEX"""
        rb1 = ScoredPlayer(FantasyPlayer(id=1, name="RB1", team="SF", position="RB"), 20.0, [])
        rb2 = ScoredPlayer(FantasyPlayer(id=2, name="RB2", team="DAL", position="RB"), 18.0, [])
        rb3 = ScoredPlayer(FantasyPlayer(id=3, name="RB3", team="PHI", position="RB"), 15.0, [])
        rb4 = ScoredPlayer(FantasyPlayer(id=4, name="RB4", team="MIA", position="RB"), 12.0, [])

        lineup = OptimalLineup([rb1, rb2, rb3, rb4])

        # Top 3 RBs should fill RB1, RB2, FLEX
        assert lineup.rb1 == rb1
        assert lineup.rb2 == rb2
        assert lineup.flex == rb3
        # 4th RB goes to bench
        assert len(lineup.bench) == 1
        assert lineup.bench[0] == rb4
        assert lineup.total_projected_points == 20.0 + 18.0 + 15.0

    def test_optimal_lineup_wide_receivers(self):
        """Test OptimalLineup with multiple WRs fills WR1, WR2, and FLEX"""
        wr1 = ScoredPlayer(FantasyPlayer(id=1, name="WR1", team="MIA", position="WR"), 22.0, [])
        wr2 = ScoredPlayer(FantasyPlayer(id=2, name="WR2", team="BUF", position="WR"), 19.0, [])
        wr3 = ScoredPlayer(FantasyPlayer(id=3, name="WR3", team="CIN", position="WR"), 16.0, [])
        wr4 = ScoredPlayer(FantasyPlayer(id=4, name="WR4", team="KC", position="WR"), 13.0, [])

        lineup = OptimalLineup([wr1, wr2, wr3, wr4])

        # Top 3 WRs should fill WR1, WR2, FLEX
        assert lineup.wr1 == wr1
        assert lineup.wr2 == wr2
        assert lineup.flex == wr3
        # 4th WR goes to bench
        assert len(lineup.bench) == 1
        assert lineup.bench[0] == wr4
        assert lineup.total_projected_points == 22.0 + 19.0 + 16.0

    def test_optimal_lineup_tight_ends(self):
        """Test OptimalLineup with multiple TEs - only one starts"""
        te1 = ScoredPlayer(FantasyPlayer(id=1, name="TE1", team="KC", position="TE"), 15.0, [])
        te2 = ScoredPlayer(FantasyPlayer(id=2, name="TE2", team="SF", position="TE"), 12.0, [])

        lineup = OptimalLineup([te1, te2])

        # Only top TE starts
        assert lineup.te == te1
        # Second TE goes to bench
        assert len(lineup.bench) == 1
        assert lineup.bench[0] == te2
        assert lineup.total_projected_points == 15.0

    def test_optimal_lineup_kickers(self):
        """Test OptimalLineup with multiple kickers"""
        k1 = ScoredPlayer(FantasyPlayer(id=1, name="K1", team="BAL", position="K"), 10.0, [])
        k2 = ScoredPlayer(FantasyPlayer(id=2, name="K2", team="SF", position="K"), 8.0, [])

        lineup = OptimalLineup([k1, k2])

        assert lineup.k == k1
        assert len(lineup.bench) == 1
        assert lineup.bench[0] == k2
        assert lineup.total_projected_points == 10.0

    def test_optimal_lineup_defenses(self):
        """Test OptimalLineup with multiple DSTs"""
        dst1 = ScoredPlayer(FantasyPlayer(id=1, name="DST1", team="SF", position="DST"), 12.0, [])
        dst2 = ScoredPlayer(FantasyPlayer(id=2, name="DST2", team="DAL", position="DST"), 9.0, [])

        lineup = OptimalLineup([dst1, dst2])

        assert lineup.dst == dst1
        assert len(lineup.bench) == 1
        assert lineup.bench[0] == dst2
        assert lineup.total_projected_points == 12.0

    def test_optimal_lineup_flex_priority_rb_over_wr(self):
        """Test FLEX slot filled by highest scoring flex-eligible player"""
        # Need at least 3 of one position to test FLEX behavior
        # Create 2 RBs and 3 WRs to test FLEX
        rb1 = ScoredPlayer(FantasyPlayer(id=1, name="RB1", team="SF", position="RB"), 25.0, [])
        rb2 = ScoredPlayer(FantasyPlayer(id=2, name="RB2", team="DAL", position="RB"), 20.0, [])
        wr1 = ScoredPlayer(FantasyPlayer(id=3, name="WR1", team="MIA", position="WR"), 24.0, [])
        wr2 = ScoredPlayer(FantasyPlayer(id=4, name="WR2", team="BUF", position="WR"), 22.0, [])
        wr_flex = ScoredPlayer(FantasyPlayer(id=5, name="WR_FLEX", team="CIN", position="WR"), 21.0, [])

        # After sorting: RB1(25), WR1(24), WR2(22), WR_FLEX(21), RB2(20)
        # RB1 → RB1, WR1 → WR1, WR2 → WR2, WR_FLEX → FLEX, RB2 → RB2
        lineup = OptimalLineup([rb1, rb2, wr1, wr2, wr_flex])

        # FLEX should be filled by WR_FLEX (3rd highest WR, but highest flex-eligible after RB/WR slots filled)
        assert lineup.flex == wr_flex
        assert lineup.flex.player.name == "WR_FLEX"
        assert lineup.flex.score == 21.0

    def test_optimal_lineup_complete_roster(self):
        """Test OptimalLineup with complete starting roster"""
        qb = ScoredPlayer(FantasyPlayer(id=1, name="QB", team="KC", position="QB"), 25.0, [])
        rb1 = ScoredPlayer(FantasyPlayer(id=2, name="RB1", team="SF", position="RB"), 20.0, [])
        rb2 = ScoredPlayer(FantasyPlayer(id=3, name="RB2", team="DAL", position="RB"), 18.0, [])
        wr1 = ScoredPlayer(FantasyPlayer(id=4, name="WR1", team="MIA", position="WR"), 22.0, [])
        wr2 = ScoredPlayer(FantasyPlayer(id=5, name="WR2", team="BUF", position="WR"), 19.0, [])
        te = ScoredPlayer(FantasyPlayer(id=6, name="TE", team="KC", position="TE"), 15.0, [])
        flex = ScoredPlayer(FantasyPlayer(id=7, name="FLEX_WR", team="CIN", position="WR"), 17.0, [])
        k = ScoredPlayer(FantasyPlayer(id=8, name="K", team="BAL", position="K"), 10.0, [])
        dst = ScoredPlayer(FantasyPlayer(id=9, name="DST", team="SF", position="DST"), 12.0, [])

        lineup = OptimalLineup([qb, rb1, rb2, wr1, wr2, te, flex, k, dst])

        assert lineup.qb == qb
        assert lineup.rb1 == rb1
        assert lineup.rb2 == rb2
        assert lineup.wr1 == wr1
        assert lineup.wr2 == wr2
        assert lineup.te == te
        assert lineup.flex == flex
        assert lineup.k == k
        assert lineup.dst == dst
        assert len(lineup.bench) == 0
        assert lineup.total_projected_points == 158.0

    def test_optimal_lineup_with_bench_players(self):
        """Test OptimalLineup with full roster plus bench"""
        starters = [
            ScoredPlayer(FantasyPlayer(id=1, name="QB", team="KC", position="QB"), 25.0, []),
            ScoredPlayer(FantasyPlayer(id=2, name="RB1", team="SF", position="RB"), 20.0, []),
            ScoredPlayer(FantasyPlayer(id=3, name="RB2", team="DAL", position="RB"), 18.0, []),
            ScoredPlayer(FantasyPlayer(id=4, name="WR1", team="MIA", position="WR"), 22.0, []),
            ScoredPlayer(FantasyPlayer(id=5, name="WR2", team="BUF", position="WR"), 19.0, []),
            ScoredPlayer(FantasyPlayer(id=6, name="TE", team="KC", position="TE"), 15.0, []),
            ScoredPlayer(FantasyPlayer(id=7, name="FLEX", team="CIN", position="WR"), 17.0, []),
            ScoredPlayer(FantasyPlayer(id=8, name="K", team="BAL", position="K"), 10.0, []),
            ScoredPlayer(FantasyPlayer(id=9, name="DST", team="SF", position="DST"), 12.0, []),
        ]
        bench = [
            ScoredPlayer(FantasyPlayer(id=10, name="Bench_QB", team="BUF", position="QB"), 20.0, []),
            ScoredPlayer(FantasyPlayer(id=11, name="Bench_RB", team="MIA", position="RB"), 14.0, []),
            ScoredPlayer(FantasyPlayer(id=12, name="Bench_WR", team="PHI", position="WR"), 13.0, []),
            ScoredPlayer(FantasyPlayer(id=13, name="Bench_TE", team="DAL", position="TE"), 11.0, []),
        ]

        all_players = starters + bench
        lineup = OptimalLineup(all_players)

        # Verify starters are correct (highest scoring)
        assert lineup.total_projected_points == 158.0
        assert len(lineup.bench) == 4
        # Verify bench players are sorted by score
        bench_names = [p.player.name for p in lineup.bench]
        assert "Bench_QB" in bench_names
        assert "Bench_RB" in bench_names
        assert "Bench_WR" in bench_names
        assert "Bench_TE" in bench_names


class TestOptimalLineupScoring:
    """Test OptimalLineup scoring and sorting logic"""

    def test_optimal_lineup_sorts_by_score(self):
        """Test that players are assigned by highest score"""
        # Create WRs with different scores
        wr_low = ScoredPlayer(FantasyPlayer(id=1, name="WR_LOW", team="JAX", position="WR"), 10.0, [])
        wr_high = ScoredPlayer(FantasyPlayer(id=2, name="WR_HIGH", team="MIA", position="WR"), 25.0, [])
        wr_mid = ScoredPlayer(FantasyPlayer(id=3, name="WR_MID", team="BUF", position="WR"), 18.0, [])

        lineup = OptimalLineup([wr_low, wr_high, wr_mid])

        # Highest score should be WR1
        assert lineup.wr1.player.name == "WR_HIGH"
        assert lineup.wr1.score == 25.0
        # Second highest WR2
        assert lineup.wr2.player.name == "WR_MID"
        assert lineup.wr2.score == 18.0
        # Lowest to FLEX (since no other flex-eligible)
        assert lineup.flex.player.name == "WR_LOW"
        assert lineup.flex.score == 10.0

    def test_total_projected_points_calculation(self):
        """Test total_projected_points property calculation"""
        players = [
            ScoredPlayer(FantasyPlayer(id=1, name="QB", team="KC", position="QB"), 24.5, []),
            ScoredPlayer(FantasyPlayer(id=2, name="RB1", team="SF", position="RB"), 19.3, []),
            ScoredPlayer(FantasyPlayer(id=3, name="RB2", team="DAL", position="RB"), 17.8, []),
            ScoredPlayer(FantasyPlayer(id=4, name="WR1", team="MIA", position="WR"), 21.2, []),
        ]

        lineup = OptimalLineup(players)

        expected_total = 24.5 + 19.3 + 17.8 + 21.2
        assert lineup.total_projected_points == expected_total

    def test_get_all_starters_order(self):
        """Test get_all_starters returns positions in correct order"""
        qb = ScoredPlayer(FantasyPlayer(id=1, name="QB", team="KC", position="QB"), 25.0, [])
        rb1 = ScoredPlayer(FantasyPlayer(id=2, name="RB1", team="SF", position="RB"), 20.0, [])
        rb2 = ScoredPlayer(FantasyPlayer(id=3, name="RB2", team="DAL", position="RB"), 18.0, [])
        wr1 = ScoredPlayer(FantasyPlayer(id=4, name="WR1", team="MIA", position="WR"), 22.0, [])
        wr2 = ScoredPlayer(FantasyPlayer(id=5, name="WR2", team="BUF", position="WR"), 19.0, [])
        te = ScoredPlayer(FantasyPlayer(id=6, name="TE", team="KC", position="TE"), 15.0, [])
        flex = ScoredPlayer(FantasyPlayer(id=7, name="FLEX", team="CIN", position="WR"), 17.0, [])
        k = ScoredPlayer(FantasyPlayer(id=8, name="K", team="BAL", position="K"), 10.0, [])
        dst = ScoredPlayer(FantasyPlayer(id=9, name="DST", team="SF", position="DST"), 12.0, [])

        lineup = OptimalLineup([qb, rb1, rb2, wr1, wr2, te, flex, k, dst])

        starters = lineup.get_all_starters()

        # Verify order: QB, RB1, RB2, WR1, WR2, TE, FLEX, K, DST
        assert starters[0] == qb
        assert starters[1] == rb1
        assert starters[2] == rb2
        assert starters[3] == wr1
        assert starters[4] == wr2
        assert starters[5] == te
        assert starters[6] == flex
        assert starters[7] == k
        assert starters[8] == dst


class TestOptimalLineupEdgeCases:
    """Test edge cases and boundary conditions"""

    def test_optimal_lineup_all_one_position(self):
        """Test lineup with only one position type"""
        qbs = [
            ScoredPlayer(FantasyPlayer(id=i, name=f"QB{i}", team="KC", position="QB"), 25.0 - i, [])
            for i in range(5)
        ]

        lineup = OptimalLineup(qbs)

        # Only one QB should start
        assert lineup.qb is not None
        assert lineup.qb == qbs[0]  # Highest score
        # All others on bench
        assert len(lineup.bench) == 4
        # All other positions empty
        assert lineup.rb1 is None
        assert lineup.wr1 is None

    def test_optimal_lineup_unknown_position(self):
        """Test player with unknown position goes to bench"""
        valid = ScoredPlayer(FantasyPlayer(id=1, name="QB", team="KC", position="QB"), 25.0, [])
        unknown = ScoredPlayer(FantasyPlayer(id=2, name="Unknown", team="???", position="UNKNOWN"), 30.0, [])

        lineup = OptimalLineup([valid, unknown])

        assert lineup.qb == valid
        assert len(lineup.bench) == 1
        assert lineup.bench[0] == unknown

    def test_optimal_lineup_zero_scores(self):
        """Test lineup with zero-scored players"""
        qb_zero = ScoredPlayer(FantasyPlayer(id=1, name="QB", team="KC", position="QB"), 0.0, [])
        rb_zero = ScoredPlayer(FantasyPlayer(id=2, name="RB", team="SF", position="RB"), 0.0, [])

        lineup = OptimalLineup([qb_zero, rb_zero])

        assert lineup.qb == qb_zero
        assert lineup.rb1 == rb_zero
        assert lineup.total_projected_points == 0.0

    def test_optimal_lineup_negative_scores(self):
        """Test lineup handles negative scores correctly"""
        dst_neg = ScoredPlayer(FantasyPlayer(id=1, name="DST", team="JAX", position="DST"), -5.0, [])
        dst_pos = ScoredPlayer(FantasyPlayer(id=2, name="DST2", team="SF", position="DST"), 10.0, [])

        lineup = OptimalLineup([dst_neg, dst_pos])

        # Positive score should start
        assert lineup.dst == dst_pos
        assert lineup.bench[0] == dst_neg
        assert lineup.total_projected_points == 10.0


class TestStarterHelperModeManager:
    """Test StarterHelperModeManager class"""

    @pytest.fixture
    def mock_config(self):
        """Create mock ConfigManager"""
        config = Mock(spec=ConfigManager)
        config.current_nfl_week = 5
        config.nfl_scoring_format = "ppr"
        config.normalization_max_scale = 100.0
        config.max_positions = {'QB': 2, 'RB': 4, 'WR': 4, 'FLEX': 2, 'TE': 1, 'K': 1, 'DST': 1}
        config.max_players = 15
        return config

    @pytest.fixture
    def mock_player_manager(self):
        """Create mock PlayerManager"""
        player_manager = Mock(spec=PlayerManager)
        player_manager.team = Mock()
        player_manager.team.roster = []
        # Mock scoring_calculator for weekly normalization
        player_manager.scoring_calculator = Mock()
        player_manager.scoring_calculator.max_weekly_projection = 0.0
        # Mock calculate_max_weekly_projection to return a reasonable value
        player_manager.calculate_max_weekly_projection = Mock(return_value=30.0)
        return player_manager

    @pytest.fixture
    def mock_team_data_manager(self):
        """Create mock TeamDataManager"""
        return Mock(spec=TeamDataManager)

    def test_manager_initialization(self, mock_config, mock_player_manager, mock_team_data_manager):
        """Test StarterHelperModeManager initialization"""
        manager = StarterHelperModeManager(mock_config, mock_player_manager, mock_team_data_manager)

        assert manager.config == mock_config
        assert manager.player_manager == mock_player_manager
        assert manager.team_data_manager == mock_team_data_manager
        assert manager.logger is not None

    def test_set_managers(self, mock_config, mock_player_manager, mock_team_data_manager):
        """Test set_managers updates manager references"""
        manager = StarterHelperModeManager(mock_config, mock_player_manager, mock_team_data_manager)

        new_player_manager = Mock(spec=PlayerManager)
        new_player_manager.team = Mock()
        new_player_manager.team.roster = []
        new_team_data_manager = Mock(spec=TeamDataManager)

        manager.set_managers(new_player_manager, new_team_data_manager)

        assert manager.player_manager == new_player_manager
        assert manager.team_data_manager == new_team_data_manager

    def test_create_starting_recommendation(self, mock_config, mock_player_manager, mock_team_data_manager):
        """Test create_starting_recommendation calls score_player correctly"""
        manager = StarterHelperModeManager(mock_config, mock_player_manager, mock_team_data_manager)

        test_player = FantasyPlayer(id=1, name="Test Player", team="KC", position="QB")
        expected_scored = ScoredPlayer(test_player, 100.0, ["Test reason"])

        # Mock score_player to return expected result
        mock_player_manager.score_player.return_value = expected_scored

        result = manager.create_starting_recommendation(test_player)

        # Verify score_player was called with correct parameters
        mock_player_manager.score_player.assert_called_once_with(
            test_player,
            use_weekly_projection=True,
            adp=False,
            player_rating=False,
            team_quality=True,
            performance=True,
            matchup=True,
            schedule=False,
            bye=False,
            injury=False,
            temperature=True,
            wind=True,
            location=True
        )
        assert result == expected_scored

    def test_optimize_lineup_empty_roster(self, mock_config, mock_player_manager, mock_team_data_manager):
        """Test optimize_lineup with empty roster"""
        mock_player_manager.team.roster = []
        manager = StarterHelperModeManager(mock_config, mock_player_manager, mock_team_data_manager)

        lineup = manager.optimize_lineup()

        assert lineup.qb is None
        assert lineup.rb1 is None
        assert lineup.total_projected_points == 0.0
        assert len(lineup.bench) == 0

    def test_optimize_lineup_full_roster(self, mock_config, mock_player_manager, mock_team_data_manager):
        """Test optimize_lineup with full roster"""
        # Create test roster
        roster_players = [
            FantasyPlayer(id=1, name="QB", team="KC", position="QB"),
            FantasyPlayer(id=2, name="RB1", team="SF", position="RB"),
            FantasyPlayer(id=3, name="RB2", team="DAL", position="RB"),
            FantasyPlayer(id=4, name="WR1", team="MIA", position="WR"),
            FantasyPlayer(id=5, name="WR2", team="BUF", position="WR"),
            FantasyPlayer(id=6, name="TE", team="KC", position="TE"),
            FantasyPlayer(id=7, name="K", team="BAL", position="K"),
            FantasyPlayer(id=8, name="DST", team="SF", position="DST"),
        ]
        mock_player_manager.team.roster = roster_players

        # Mock score_player to return consistent scores
        def mock_score_player(player, **kwargs):
            scores = {"QB": 25.0, "RB": 20.0, "WR": 22.0, "TE": 15.0, "K": 10.0, "DST": 12.0}
            score = scores.get(player.position, 15.0)
            return ScoredPlayer(player, score, [f"Score: {score}"])

        mock_player_manager.score_player.side_effect = mock_score_player

        manager = StarterHelperModeManager(mock_config, mock_player_manager, mock_team_data_manager)
        lineup = manager.optimize_lineup()

        # Verify all positions filled
        assert lineup.qb is not None
        assert lineup.rb1 is not None
        assert lineup.rb2 is not None
        assert lineup.wr1 is not None
        assert lineup.wr2 is not None
        assert lineup.te is not None
        assert lineup.k is not None
        assert lineup.dst is not None

        # score_player should be called for each roster player
        assert mock_player_manager.score_player.call_count == len(roster_players)

    def test_optimize_lineup_with_bench(self, mock_config, mock_player_manager, mock_team_data_manager):
        """Test optimize_lineup properly assigns overflow to bench"""
        # Create roster with extra RBs
        roster_players = [
            FantasyPlayer(id=1, name="RB1", team="SF", position="RB"),
            FantasyPlayer(id=2, name="RB2", team="DAL", position="RB"),
            FantasyPlayer(id=3, name="RB3", team="PHI", position="RB"),
            FantasyPlayer(id=4, name="RB4", team="MIA", position="RB"),
            FantasyPlayer(id=5, name="RB5", team="CLE", position="RB"),
        ]
        mock_player_manager.team.roster = roster_players

        # Mock scoring with descending values
        def mock_score_player(player, **kwargs):
            scores = {"RB1": 25.0, "RB2": 22.0, "RB3": 20.0, "RB4": 18.0, "RB5": 15.0}
            score = scores.get(player.name, 10.0)
            return ScoredPlayer(player, score, [])

        mock_player_manager.score_player.side_effect = mock_score_player

        manager = StarterHelperModeManager(mock_config, mock_player_manager, mock_team_data_manager)
        lineup = manager.optimize_lineup()

        # Top 3 should start (RB1, RB2, FLEX)
        assert lineup.rb1.player.name == "RB1"
        assert lineup.rb2.player.name == "RB2"
        assert lineup.flex.player.name == "RB3"

        # RB4 and RB5 should be on bench
        assert len(lineup.bench) == 2
        bench_names = [p.player.name for p in lineup.bench]
        assert "RB4" in bench_names
        assert "RB5" in bench_names


class TestOptimalLineupFLEXScenarios:
    """Test advanced FLEX optimization scenarios"""

    def test_optimal_lineup_dst_not_in_flex(self):
        """Test that DST cannot fill FLEX slot (only RB/WR allowed)"""
        # Create roster with only DST players
        dst1 = ScoredPlayer(FantasyPlayer(id=1, name="DST1", team="SF", position="DST"), 15.0, [])
        dst2 = ScoredPlayer(FantasyPlayer(id=2, name="DST2", team="DAL", position="DST"), 12.0, [])

        lineup = OptimalLineup([dst1, dst2])

        # Best DST should start in DST slot
        assert lineup.dst == dst1
        # Second DST should go to bench, NOT flex
        assert lineup.flex is None
        assert len(lineup.bench) == 1
        assert lineup.bench[0] == dst2

    def test_optimal_lineup_te_not_in_flex(self):
        """Test that TE cannot fill FLEX slot (only RB/WR allowed)"""
        # Create roster with only TE players
        te1 = ScoredPlayer(FantasyPlayer(id=1, name="TE1", team="KC", position="TE"), 18.0, [])
        te2 = ScoredPlayer(FantasyPlayer(id=2, name="TE2", team="SF", position="TE"), 15.0, [])

        lineup = OptimalLineup([te1, te2])

        # Best TE should start in TE slot
        assert lineup.te == te1
        # Second TE should go to bench, NOT flex
        assert lineup.flex is None
        assert len(lineup.bench) == 1
        assert lineup.bench[0] == te2

    def test_optimal_lineup_flex_wr_over_rb_by_score(self):
        """Test FLEX filled by highest scoring RB/WR regardless of position"""
        rb1 = ScoredPlayer(FantasyPlayer(id=1, name="RB1", team="SF", position="RB"), 22.0, [])
        rb2 = ScoredPlayer(FantasyPlayer(id=2, name="RB2", team="DAL", position="RB"), 20.0, [])
        rb3 = ScoredPlayer(FantasyPlayer(id=3, name="RB3", team="PHI", position="RB"), 18.0, [])
        wr1 = ScoredPlayer(FantasyPlayer(id=4, name="WR1", team="MIA", position="WR"), 21.0, [])
        wr2 = ScoredPlayer(FantasyPlayer(id=5, name="WR2", team="BUF", position="WR"), 19.0, [])
        wr3 = ScoredPlayer(FantasyPlayer(id=6, name="WR3_FLEX", team="CIN", position="WR"), 19.5, [])

        # After sorting by score: RB1(22), WR1(21), RB2(20), WR3(19.5), WR2(19), RB3(18)
        # RB1→RB1, WR1→WR1, RB2→RB2, WR3→WR2, WR2→FLEX (highest remaining flex-eligible)
        lineup = OptimalLineup([rb1, rb2, rb3, wr1, wr2, wr3])

        # FLEX should be filled by WR2 (19.0), which is higher than RB3 (18.0)
        assert lineup.flex.player.name == "WR2"
        assert lineup.flex.score == 19.0
        # RB3 should be on bench
        assert len(lineup.bench) == 1
        assert lineup.bench[0] == rb3

    def test_optimal_lineup_mixed_positions_partial_roster(self):
        """Test lineup with partial roster (missing some position types)"""
        qb = ScoredPlayer(FantasyPlayer(id=1, name="QB", team="KC", position="QB"), 25.0, [])
        rb = ScoredPlayer(FantasyPlayer(id=2, name="RB1", team="SF", position="RB"), 20.0, [])
        wr = ScoredPlayer(FantasyPlayer(id=3, name="WR1", team="MIA", position="WR"), 22.0, [])
        k = ScoredPlayer(FantasyPlayer(id=4, name="K", team="BAL", position="K"), 10.0, [])

        lineup = OptimalLineup([qb, rb, wr, k])

        # Filled positions
        assert lineup.qb == qb
        assert lineup.rb1 == rb
        assert lineup.wr1 == wr
        assert lineup.k == k

        # Empty positions
        assert lineup.rb2 is None
        assert lineup.wr2 is None
        assert lineup.te is None
        assert lineup.flex is None
        assert lineup.dst is None
        assert len(lineup.bench) == 0

        # Total should only include filled positions
        assert lineup.total_projected_points == 77.0


class TestStarterHelperInjuryHandling:
    """Test injury status handling in lineup optimization"""

    def test_optimize_lineup_includes_injured_players(self):
        """Test that injured players are still included in optimization"""
        # Create mock managers
        config = Mock(spec=ConfigManager)
        config.current_nfl_week = 5
        config.nfl_scoring_format = "ppr"
        player_manager = Mock(spec=PlayerManager)
        player_manager.team = Mock()
        player_manager.scoring_calculator = Mock()
        player_manager.scoring_calculator.max_weekly_projection = 0.0
        player_manager.calculate_max_weekly_projection = Mock(return_value=30.0)
        team_data_manager = Mock(spec=TeamDataManager)

        # Create roster with injured players
        healthy_qb = FantasyPlayer(id=1, name="Healthy QB", team="KC", position="QB", injury_status="ACTIVE")
        injured_qb = FantasyPlayer(id=2, name="Injured QB", team="BUF", position="QB", injury_status="QUESTIONABLE")

        player_manager.team.roster = [healthy_qb, injured_qb]

        # Mock scoring - injured player scores lower
        def mock_score_player(player, **kwargs):
            if player.name == "Healthy QB":
                return ScoredPlayer(player, 25.0, [])
            else:
                return ScoredPlayer(player, 20.0, [])

        player_manager.score_player.side_effect = mock_score_player

        manager = StarterHelperModeManager(config, player_manager, team_data_manager)
        lineup = manager.optimize_lineup()

        # Healthy QB should start (higher score)
        assert lineup.qb.player.name == "Healthy QB"
        # Injured QB should be on bench (not filtered out)
        assert len(lineup.bench) == 1
        assert lineup.bench[0].player.name == "Injured QB"

    def test_create_starting_recommendation_injury_parameter_false(self):
        """Test that injury penalty is disabled for weekly lineup decisions"""
        config = Mock(spec=ConfigManager)
        player_manager = Mock(spec=PlayerManager)
        player_manager.team = Mock()
        player_manager.team.roster = []
        team_data_manager = Mock(spec=TeamDataManager)

        test_player = FantasyPlayer(id=1, name="Player", team="KC", position="QB", injury_status="QUESTIONABLE")
        expected_scored = ScoredPlayer(test_player, 100.0, [])

        player_manager.score_player.return_value = expected_scored

        manager = StarterHelperModeManager(config, player_manager, team_data_manager)
        result = manager.create_starting_recommendation(test_player)

        # Verify injury=False and schedule=False were passed
        player_manager.score_player.assert_called_once_with(
            test_player,
            use_weekly_projection=True,
            adp=False,
            player_rating=False,
            team_quality=True,
            performance=True,
            matchup=True,
            schedule=False,
            bye=False,
            injury=False,
            temperature=True,
            wind=True,
            location=True
        )


class TestStarterHelperDisplayFunctionality:
    """Test display and user interaction functionality"""

    def test_show_recommended_starters_display(self, capsys):
        """Test show_recommended_starters displays formatted lineup"""
        config = Mock(spec=ConfigManager)
        config.current_nfl_week = 8
        config.nfl_scoring_format = "ppr"

        player_manager = Mock(spec=PlayerManager)
        player_manager.team = Mock()
        player_manager.scoring_calculator = Mock()
        player_manager.scoring_calculator.max_weekly_projection = 0.0
        player_manager.calculate_max_weekly_projection = Mock(return_value=30.0)
        team_data_manager = Mock(spec=TeamDataManager)

        # Create minimal roster
        qb = FantasyPlayer(id=1, name="Patrick Mahomes", team="KC", position="QB")
        player_manager.team.roster = [qb]

        # Mock scoring
        player_manager.score_player.return_value = ScoredPlayer(qb, 25.5, ["Weekly projection: 25.5"])

        manager = StarterHelperModeManager(config, player_manager, team_data_manager)

        # Mock input to avoid blocking
        with patch('builtins.input', return_value=''):
            manager.show_recommended_starters(player_manager, team_data_manager)

        # Check output
        captured = capsys.readouterr()
        assert "OPTIMAL STARTING LINEUP - WEEK 8" in captured.out
        assert "PPR SCORING" in captured.out
        assert "Patrick Mahomes" in captured.out
        assert "BENCH" in captured.out

    def test_print_player_list_with_players(self, capsys):
        """Test print_player_list displays formatted player information"""
        config = Mock(spec=ConfigManager)
        player_manager = Mock(spec=PlayerManager)
        player_manager.team = Mock()
        player_manager.team.roster = []
        team_data_manager = Mock(spec=TeamDataManager)

        manager = StarterHelperModeManager(config, player_manager, team_data_manager)

        qb = ScoredPlayer(FantasyPlayer(id=1, name="QB", team="KC", position="QB"), 25.0, [])
        rb = ScoredPlayer(FantasyPlayer(id=2, name="RB", team="SF", position="RB"), 20.0, [])

        player_list = [("QB", qb), ("RB", rb)]

        manager.print_player_list(player_list)

        captured = capsys.readouterr()
        assert "QB" in captured.out
        assert "RB" in captured.out
        assert "QB" in captured.out or "RB" in captured.out

    def test_print_player_list_with_empty_slots(self, capsys):
        """Test print_player_list handles empty slots gracefully"""
        config = Mock(spec=ConfigManager)
        player_manager = Mock(spec=PlayerManager)
        player_manager.team = Mock()
        player_manager.team.roster = []
        team_data_manager = Mock(spec=TeamDataManager)

        manager = StarterHelperModeManager(config, player_manager, team_data_manager)

        player_list = [("QB", None), ("RB", None)]

        manager.print_player_list(player_list)

        captured = capsys.readouterr()
        assert "No available player" in captured.out
        # Should appear twice (once for each empty slot)
        assert captured.out.count("No available player") == 2


class TestStarterHelperEdgeCases:
    """Test additional edge cases and boundary conditions"""

    def test_optimize_lineup_single_player_roster(self):
        """Test optimization with roster containing only one player"""
        config = Mock(spec=ConfigManager)
        config.current_nfl_week = 1
        config.nfl_scoring_format = "standard"

        player_manager = Mock(spec=PlayerManager)
        player_manager.team = Mock()
        player_manager.scoring_calculator = Mock()
        player_manager.scoring_calculator.max_weekly_projection = 0.0
        player_manager.calculate_max_weekly_projection = Mock(return_value=30.0)
        team_data_manager = Mock(spec=TeamDataManager)

        single_player = FantasyPlayer(id=1, name="Solo QB", team="KC", position="QB")
        player_manager.team.roster = [single_player]

        player_manager.score_player.return_value = ScoredPlayer(single_player, 30.0, [])

        manager = StarterHelperModeManager(config, player_manager, team_data_manager)
        lineup = manager.optimize_lineup()

        # Only QB should be filled
        assert lineup.qb.player.name == "Solo QB"
        # All other positions empty
        assert lineup.rb1 is None
        assert lineup.wr1 is None
        assert len(lineup.bench) == 0
        assert lineup.total_projected_points == 30.0

    def test_optimize_lineup_large_roster(self):
        """Test optimization with 15-player roster (all positions filled + extras)"""
        config = Mock(spec=ConfigManager)
        config.current_nfl_week = 10
        config.nfl_scoring_format = "half_ppr"

        player_manager = Mock(spec=PlayerManager)
        player_manager.team = Mock()
        player_manager.scoring_calculator = Mock()
        player_manager.scoring_calculator.max_weekly_projection = 0.0
        player_manager.calculate_max_weekly_projection = Mock(return_value=30.0)
        team_data_manager = Mock(spec=TeamDataManager)

        # Create 15-player roster
        roster = [
            FantasyPlayer(id=1, name="QB1", team="KC", position="QB"),
            FantasyPlayer(id=2, name="QB2", team="BUF", position="QB"),
            FantasyPlayer(id=3, name="RB1", team="SF", position="RB"),
            FantasyPlayer(id=4, name="RB2", team="DAL", position="RB"),
            FantasyPlayer(id=5, name="RB3", team="PHI", position="RB"),
            FantasyPlayer(id=6, name="RB4", team="MIA", position="RB"),
            FantasyPlayer(id=7, name="WR1", team="MIA", position="WR"),
            FantasyPlayer(id=8, name="WR2", team="BUF", position="WR"),
            FantasyPlayer(id=9, name="WR3", team="CIN", position="WR"),
            FantasyPlayer(id=10, name="WR4", team="DET", position="WR"),
            FantasyPlayer(id=11, name="TE1", team="KC", position="TE"),
            FantasyPlayer(id=12, name="TE2", team="SF", position="TE"),
            FantasyPlayer(id=13, name="K1", team="BAL", position="K"),
            FantasyPlayer(id=14, name="DST1", team="SF", position="DST"),
            FantasyPlayer(id=15, name="DST2", team="DAL", position="DST"),
        ]
        player_manager.team.roster = roster

        # Mock scoring with descending values
        def mock_score_player(player, **kwargs):
            base_scores = {"QB": 25, "RB": 20, "WR": 22, "TE": 15, "K": 10, "DST": 12}
            position = player.position
            # Add ID to create variety
            score = base_scores.get(position, 10) + (20 - player.id) * 0.5
            return ScoredPlayer(player, score, [])

        player_manager.score_player.side_effect = mock_score_player

        manager = StarterHelperModeManager(config, player_manager, team_data_manager)
        lineup = manager.optimize_lineup()

        # All starting positions should be filled
        assert lineup.qb is not None
        assert lineup.rb1 is not None
        assert lineup.rb2 is not None
        assert lineup.wr1 is not None
        assert lineup.wr2 is not None
        assert lineup.te is not None
        assert lineup.flex is not None  # Should be filled by 3rd best RB or WR
        assert lineup.k is not None
        assert lineup.dst is not None

        # Bench should have remaining 6 players
        assert len(lineup.bench) == 6


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
