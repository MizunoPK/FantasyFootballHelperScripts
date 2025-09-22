#!/usr/bin/env python3
"""
Unit Tests for Matchup Analyzer

Tests the core matchup analysis functionality including rating calculations,
ESPN API integration, and weekly analysis workflows.

Author: Generated for Fantasy Football Helper Scripts
Last Updated: September 2025
"""

import unittest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Add path for imports
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent.parent))

from matchup_analyzer import MatchupAnalyzer
from matchup_models import (
    TeamDefenseStats, WeeklyMatchup, PlayerMatchupContext, MatchupRating,
    FantasyPosition, HomeAwayStatus, GameStatus, InjuryStatus
)
from espn_matchup_client import ESPNMatchupClient


class TestMatchupAnalyzer(unittest.TestCase):
    """Test suite for MatchupAnalyzer functionality"""

    def setUp(self):
        """Set up test environment"""
        # Create mock ESPN client
        self.mock_espn_client = AsyncMock(spec=ESPNMatchupClient)
        self.mock_espn_client.NFL_SEASON = 2025
        self.mock_espn_client.CURRENT_NFL_WEEK = 5

        # Create analyzer with mock client
        self.analyzer = MatchupAnalyzer(espn_client=self.mock_espn_client)

        # Sample test data
        self.sample_defense_stats = self._create_sample_defense_stats()
        self.sample_player_context = self._create_sample_player_context()
        self.sample_league_averages = self._create_sample_league_averages()

    def _create_sample_defense_stats(self) -> TeamDefenseStats:
        """Create sample team defense statistics"""
        return TeamDefenseStats(
            team_id=4,  # CIN
            team_name="Bengals",
            team_abbreviation="CIN",
            qb_points_allowed=22.0,
            rb_points_allowed=18.0,
            wr_points_allowed=16.0,
            te_points_allowed=8.0,
            k_points_allowed=7.0,
            dst_points_allowed=10.0,
            recent_qb_trend=24.0,
            recent_rb_trend=20.0,
            recent_wr_trend=18.0,
            recent_te_trend=9.0,
            recent_k_trend=8.0,
            recent_dst_trend=11.0,
            games_played=4,
            recent_games_analyzed=3
        )

    def _create_sample_player_context(self) -> PlayerMatchupContext:
        """Create sample player matchup context"""
        return PlayerMatchupContext(
            player_id="4431569",
            player_name="Lamar Jackson",
            player_position=FantasyPosition.QB,
            player_team_id=33,  # BAL
            player_team_abbreviation="BAL",
            opponent_team_id=4,  # CIN
            opponent_team_name="Bengals",
            opponent_team_abbreviation="CIN",
            is_home_game=False,
            week=5,
            game_date=datetime.now() + timedelta(days=3),
            injury_status=InjuryStatus.ACTIVE,
            is_available=True
        )

    def _create_sample_league_averages(self) -> dict:
        """Create sample league averages"""
        return {
            FantasyPosition.QB: 20.0,
            FantasyPosition.RB: 15.0,
            FantasyPosition.WR: 14.0,
            FantasyPosition.TE: 8.5,
            FantasyPosition.K: 7.0,
            FantasyPosition.DST: 9.0,
            FantasyPosition.FLEX: 14.5
        }

    def test_analyzer_initialization(self):
        """Test MatchupAnalyzer initialization"""
        # Test with default ESPN client
        analyzer = MatchupAnalyzer()
        self.assertIsNotNone(analyzer.espn_client)
        self.assertIsNotNone(analyzer.config)

        # Test with provided ESPN client
        analyzer_with_client = MatchupAnalyzer(espn_client=self.mock_espn_client)
        self.assertEqual(analyzer_with_client.espn_client, self.mock_espn_client)

    def test_calculate_defense_strength_rating(self):
        """Test defense strength rating calculation"""
        # Test better than average defense (allows fewer points)
        rating = self.analyzer._calculate_defense_strength_rating(
            self.sample_player_context,
            self.sample_defense_stats,
            self.sample_league_averages
        )

        # CIN allows 22.0 QB points vs league average 20.0 = +2.0 difference
        # Should result in rating > 50 (better matchup)
        self.assertGreater(rating, 50.0)
        self.assertLessEqual(rating, 100.0)
        self.assertGreaterEqual(rating, 1.0)

        # Test worse than average defense
        bad_defense = TeamDefenseStats(
            team_id=1, team_name="Test", team_abbreviation="TST",
            qb_points_allowed=15.0,  # Below league average = worse matchup
            rb_points_allowed=12.0, wr_points_allowed=11.0,
            te_points_allowed=6.0, k_points_allowed=5.0, dst_points_allowed=7.0,
            recent_qb_trend=15.0, recent_rb_trend=12.0, recent_wr_trend=11.0,
            recent_te_trend=6.0, recent_k_trend=5.0, recent_dst_trend=7.0,
            games_played=4, recent_games_analyzed=3
        )

        bad_rating = self.analyzer._calculate_defense_strength_rating(
            self.sample_player_context, bad_defense, self.sample_league_averages
        )
        self.assertLess(bad_rating, 50.0)  # Worse matchup

    def test_calculate_recent_trend_rating(self):
        """Test recent trend rating calculation"""
        # Test declining defense (allowing more points recently)
        rating = self.analyzer._calculate_recent_trend_rating(
            self.sample_player_context,
            self.sample_defense_stats,
            self.sample_league_averages
        )

        # Recent trend (24.0) > season average (22.0) = declining defense = better matchup
        self.assertGreater(rating, 50.0)
        self.assertLessEqual(rating, 100.0)
        self.assertGreaterEqual(rating, 1.0)

        # Test improving defense
        improving_defense = TeamDefenseStats(
            team_id=1, team_name="Test", team_abbreviation="TST",
            qb_points_allowed=22.0, rb_points_allowed=18.0, wr_points_allowed=16.0,
            te_points_allowed=8.0, k_points_allowed=7.0, dst_points_allowed=10.0,
            recent_qb_trend=18.0,  # Less than season average = improving defense
            recent_rb_trend=15.0, recent_wr_trend=14.0,
            recent_te_trend=7.0, recent_k_trend=6.0, recent_dst_trend=8.0,
            games_played=4, recent_games_analyzed=3
        )

        improving_rating = self.analyzer._calculate_recent_trend_rating(
            self.sample_player_context, improving_defense, self.sample_league_averages
        )
        self.assertLess(improving_rating, 50.0)  # Worse matchup

    def test_calculate_home_field_rating(self):
        """Test home field advantage rating calculation"""
        # Test away game
        away_rating = self.analyzer._calculate_home_field_rating(self.sample_player_context)
        self.assertLess(away_rating, 50.0)

        # Test home game
        home_context = PlayerMatchupContext(
            player_id="test", player_name="Test Player", player_position=FantasyPosition.QB,
            player_team_id=1, player_team_abbreviation="TST",
            opponent_team_id=2, opponent_team_name="Opponent", opponent_team_abbreviation="OPP",
            is_home_game=True, week=5, game_date=datetime.now(),
            injury_status=InjuryStatus.ACTIVE, is_available=True
        )

        home_rating = self.analyzer._calculate_home_field_rating(home_context)
        self.assertGreater(home_rating, 50.0)

        # Both should be within reasonable bounds
        self.assertGreaterEqual(away_rating, 40.0)
        self.assertLessEqual(away_rating, 60.0)
        self.assertGreaterEqual(home_rating, 40.0)
        self.assertLessEqual(home_rating, 60.0)

    def test_calculate_schedule_strength_rating(self):
        """Test schedule strength rating calculation"""
        # Create multiple defense stats for comparison
        all_defenses = {
            1: TeamDefenseStats(team_id=1, team_name="Best", team_abbreviation="BST",
                               qb_points_allowed=15.0, rb_points_allowed=12.0, wr_points_allowed=11.0,
                               te_points_allowed=6.0, k_points_allowed=5.0, dst_points_allowed=7.0,
                               recent_qb_trend=15.0, recent_rb_trend=12.0, recent_wr_trend=11.0,
                               recent_te_trend=6.0, recent_k_trend=5.0, recent_dst_trend=7.0,
                               games_played=4, recent_games_analyzed=3),
            4: self.sample_defense_stats,  # CIN - middle defense
            30: TeamDefenseStats(team_id=30, team_name="Worst", team_abbreviation="WST",
                                qb_points_allowed=30.0, rb_points_allowed=25.0, wr_points_allowed=24.0,
                                te_points_allowed=15.0, k_points_allowed=12.0, dst_points_allowed=18.0,
                                recent_qb_trend=30.0, recent_rb_trend=25.0, recent_wr_trend=24.0,
                                recent_te_trend=15.0, recent_k_trend=12.0, recent_dst_trend=18.0,
                                games_played=4, recent_games_analyzed=3)
        }

        rating = self.analyzer._calculate_schedule_strength_rating(
            self.sample_player_context, self.sample_defense_stats, all_defenses
        )

        # CIN should be middle-ranked, so rating should be around 50
        self.assertGreater(rating, 30.0)
        self.assertLess(rating, 70.0)
        self.assertGreaterEqual(rating, 20.0)
        self.assertLessEqual(rating, 80.0)

    @patch('starter_helper_config.DEFENSE_STRENGTH_WEIGHT', 0.4)
    @patch('starter_helper_config.RECENT_TREND_WEIGHT', 0.3)
    @patch('starter_helper_config.HOME_FIELD_WEIGHT', 0.15)
    @patch('starter_helper_config.SCHEDULE_STRENGTH_WEIGHT', 0.15)
    async def test_analyze_player_matchup(self):
        """Test complete player matchup analysis"""
        # Setup team defenses dict
        team_defenses = {4: self.sample_defense_stats}

        # Analyze matchup
        rating = await self.analyzer.analyze_player_matchup(
            self.sample_player_context, team_defenses, self.sample_league_averages
        )

        # Verify rating structure
        self.assertIsInstance(rating, MatchupRating)
        self.assertEqual(rating.player_context, self.sample_player_context)

        # Verify rating bounds
        self.assertGreaterEqual(rating.overall_rating, 1.0)
        self.assertLessEqual(rating.overall_rating, 100.0)

        # Verify component ratings
        self.assertGreaterEqual(rating.defense_strength_rating, 1.0)
        self.assertLessEqual(rating.defense_strength_rating, 100.0)
        self.assertGreaterEqual(rating.recent_trend_rating, 1.0)
        self.assertLessEqual(rating.recent_trend_rating, 100.0)
        self.assertGreaterEqual(rating.home_field_rating, 1.0)
        self.assertLessEqual(rating.home_field_rating, 100.0)
        self.assertGreaterEqual(rating.schedule_strength_rating, 1.0)
        self.assertLessEqual(rating.schedule_strength_rating, 100.0)

        # Verify detailed metrics
        self.assertEqual(rating.opponent_points_allowed, 22.0)  # QB points allowed
        self.assertEqual(rating.league_average_allowed, 20.0)   # League average
        self.assertEqual(rating.points_above_average, 2.0)      # Difference

        # Verify confidence and sample size
        self.assertGreater(rating.confidence_score, 0.0)
        self.assertLessEqual(rating.confidence_score, 100.0)
        self.assertEqual(rating.sample_size, 4)

    async def test_analyze_player_matchup_missing_defense(self):
        """Test matchup analysis when opponent defense data is missing"""
        # Empty team defenses
        team_defenses = {}

        rating = await self.analyzer.analyze_player_matchup(
            self.sample_player_context, team_defenses, self.sample_league_averages
        )

        # Should return default neutral rating
        self.assertEqual(rating.overall_rating, 50.0)
        self.assertEqual(rating.confidence_score, 30.0)
        self.assertEqual(rating.sample_size, 0)

    async def test_analyze_weekly_matchups(self):
        """Test weekly matchup analysis for multiple players"""
        # Setup mock ESPN client responses
        self.mock_espn_client.fetch_team_defense_stats.return_value = {
            4: self.sample_defense_stats
        }

        self.mock_espn_client.fetch_current_week_schedule.return_value = [
            WeeklyMatchup(
                week=5, season=2025,
                home_team_id=4, home_team_name="Bengals", home_team_abbreviation="CIN",
                away_team_id=33, away_team_name="Ravens", away_team_abbreviation="BAL",
                game_date=datetime.now() + timedelta(days=3),
                game_status=GameStatus.SCHEDULED
            )
        ]

        # Sample roster players
        roster_players = [
            {
                'id': '4431569',
                'name': 'Lamar Jackson',
                'position': 'QB',
                'team_id': 33,
                'injury_status': 'ACTIVE'
            }
        ]

        # Mock the create_player_matchup_context method
        self.mock_espn_client.create_player_matchup_context.return_value = self.sample_player_context

        # Perform analysis
        analysis = await self.analyzer.analyze_weekly_matchups(roster_players, week=5)

        # Verify analysis structure
        self.assertIsNotNone(analysis)
        self.assertEqual(analysis.week, 5)
        self.assertEqual(analysis.season, 2025)
        self.assertEqual(analysis.total_players_analyzed, 1)
        self.assertGreater(analysis.analysis_runtime_seconds, 0.0)

        # Verify player ratings
        self.assertEqual(len(analysis.player_ratings), 1)
        player_rating = analysis.player_ratings[0]
        self.assertEqual(player_rating.player_context.player_name, "Lamar Jackson")

    def test_get_matchup_display_indicator(self):
        """Test matchup display indicator generation"""
        # Test excellent matchup
        self.assertEqual(self.analyzer.get_matchup_display_indicator(85.0), "**")

        # Test good matchup
        self.assertEqual(self.analyzer.get_matchup_display_indicator(70.0), "*")

        # Test average matchup
        self.assertEqual(self.analyzer.get_matchup_display_indicator(55.0), "o")

        # Test below average matchup
        self.assertEqual(self.analyzer.get_matchup_display_indicator(40.0), "-")

        # Test poor matchup
        self.assertEqual(self.analyzer.get_matchup_display_indicator(25.0), "x")

        # Test boundary conditions
        self.assertEqual(self.analyzer.get_matchup_display_indicator(75.0), "**")
        self.assertEqual(self.analyzer.get_matchup_display_indicator(65.0), "*")
        self.assertEqual(self.analyzer.get_matchup_display_indicator(50.0), "o")
        self.assertEqual(self.analyzer.get_matchup_display_indicator(35.0), "-")

    def test_format_matchup_summary(self):
        """Test matchup summary formatting"""
        # Create a sample rating
        rating = MatchupRating(
            player_context=self.sample_player_context,
            overall_rating=75.0,
            defense_strength_rating=70.0,
            recent_trend_rating=80.0,
            home_field_rating=45.0,
            schedule_strength_rating=75.0,
            opponent_points_allowed=22.0,
            league_average_allowed=20.0,
            points_above_average=2.0,
            recent_opponent_average=24.0,
            trend_direction="declining",
            trend_magnitude=2.0,
            home_field_advantage=0.0,
            weather_impact=0.0,
            venue_impact=0.0,
            confidence_score=85.0,
            sample_size=4
        )

        # Test simple format
        simple_summary = self.analyzer.format_matchup_summary(rating, show_detailed=False)
        self.assertIn("**", simple_summary)
        self.assertIn("75", simple_summary)

        # Test detailed format
        detailed_summary = self.analyzer.format_matchup_summary(rating, show_detailed=True)
        self.assertIn("**", detailed_summary)
        self.assertIn("75", detailed_summary)
        self.assertIn("CIN", detailed_summary)
        self.assertIn("A", detailed_summary)  # Away game
        self.assertIn("declining", detailed_summary)

    def test_calculate_confidence_score(self):
        """Test confidence score calculation"""
        # Test high confidence (many games)
        high_confidence_defense = TeamDefenseStats(
            team_id=1, team_name="Test", team_abbreviation="TST",
            qb_points_allowed=20.0, rb_points_allowed=15.0, wr_points_allowed=14.0,
            te_points_allowed=8.0, k_points_allowed=7.0, dst_points_allowed=9.0,
            recent_qb_trend=20.0, recent_rb_trend=15.0, recent_wr_trend=14.0,
            recent_te_trend=8.0, recent_k_trend=7.0, recent_dst_trend=9.0,
            games_played=10, recent_games_analyzed=4
        )

        high_confidence = self.analyzer._calculate_confidence_score(high_confidence_defense)
        self.assertGreater(high_confidence, 80.0)

        # Test low confidence (few games)
        low_confidence_defense = TeamDefenseStats(
            team_id=1, team_name="Test", team_abbreviation="TST",
            qb_points_allowed=20.0, rb_points_allowed=15.0, wr_points_allowed=14.0,
            te_points_allowed=8.0, k_points_allowed=7.0, dst_points_allowed=9.0,
            recent_qb_trend=20.0, recent_rb_trend=15.0, recent_wr_trend=14.0,
            recent_te_trend=8.0, recent_k_trend=7.0, recent_dst_trend=9.0,
            games_played=1, recent_games_analyzed=0
        )

        low_confidence = self.analyzer._calculate_confidence_score(low_confidence_defense)
        self.assertLess(low_confidence, 60.0)

    def test_analyze_trend_direction(self):
        """Test trend direction analysis"""
        # Test declining trend (defense getting worse)
        direction, magnitude = self.analyzer._analyze_trend_direction(20.0, 23.0)
        self.assertEqual(direction, "declining")
        self.assertEqual(magnitude, 3.0)

        # Test improving trend (defense getting better)
        direction, magnitude = self.analyzer._analyze_trend_direction(20.0, 17.0)
        self.assertEqual(direction, "improving")
        self.assertEqual(magnitude, 3.0)

        # Test stable trend
        direction, magnitude = self.analyzer._analyze_trend_direction(20.0, 20.5)
        self.assertEqual(direction, "stable")
        self.assertEqual(magnitude, 0.5)

        # Test zero values
        direction, magnitude = self.analyzer._analyze_trend_direction(0.0, 0.0)
        self.assertEqual(direction, "stable")
        self.assertEqual(magnitude, 0.0)

    async def test_close_resources(self):
        """Test proper resource cleanup"""
        # Test close method exists and can be called
        await self.analyzer.close()
        self.mock_espn_client.close.assert_called_once()


class TestMatchupAnalyzerIntegration(unittest.IsolatedAsyncioTestCase):
    """Integration tests for MatchupAnalyzer with real-like data"""

    async def test_end_to_end_analysis_workflow(self):
        """Test complete end-to-end matchup analysis workflow"""
        # Create mock ESPN client with realistic responses
        mock_client = AsyncMock()

        # Mock defense stats response
        mock_defense_stats = {
            4: TeamDefenseStats(  # CIN
                team_id=4, team_name="Bengals", team_abbreviation="CIN",
                qb_points_allowed=22.5, rb_points_allowed=18.2, wr_points_allowed=16.8,
                te_points_allowed=8.9, k_points_allowed=7.3, dst_points_allowed=10.1,
                recent_qb_trend=24.1, recent_rb_trend=19.5, recent_wr_trend=18.0,
                recent_te_trend=9.2, recent_k_trend=7.8, recent_dst_trend=11.2,
                games_played=5, recent_games_analyzed=3
            ),
            33: TeamDefenseStats(  # BAL
                team_id=33, team_name="Ravens", team_abbreviation="BAL",
                qb_points_allowed=19.8, rb_points_allowed=14.5, wr_points_allowed=15.2,
                te_points_allowed=7.8, k_points_allowed=6.9, dst_points_allowed=9.3,
                recent_qb_trend=18.9, recent_rb_trend=13.8, recent_wr_trend=14.7,
                recent_te_trend=7.5, recent_k_trend=6.6, recent_dst_trend=8.9,
                games_played=5, recent_games_analyzed=3
            )
        }

        mock_client.fetch_team_defense_stats.return_value = mock_defense_stats

        # Mock schedule response
        mock_schedule = [
            WeeklyMatchup(
                week=5, season=2025,
                home_team_id=4, home_team_name="Bengals", home_team_abbreviation="CIN",
                away_team_id=33, away_team_name="Ravens", away_team_abbreviation="BAL",
                game_date=datetime.now() + timedelta(days=3),
                game_status=GameStatus.SCHEDULED,
                venue_name="Paycor Stadium",
                venue_city="Cincinnati",
                is_indoor=False,
                temperature=65,
                weather_condition="Clear"
            )
        ]

        mock_client.fetch_current_week_schedule.return_value = mock_schedule

        # Mock player context creation
        async def mock_create_context(player_id, player_name, player_position, player_team_id, week):
            return PlayerMatchupContext(
                player_id=player_id,
                player_name=player_name,
                player_position=player_position,
                player_team_id=player_team_id,
                player_team_abbreviation="BAL" if player_team_id == 33 else "CIN",
                opponent_team_id=4 if player_team_id == 33 else 33,
                opponent_team_name="Bengals" if player_team_id == 33 else "Ravens",
                opponent_team_abbreviation="CIN" if player_team_id == 33 else "BAL",
                is_home_game=(player_team_id == 4),
                week=week,
                game_date=datetime.now() + timedelta(days=3),
                injury_status=InjuryStatus.ACTIVE,
                is_available=True
            )

        mock_client.create_player_matchup_context.side_effect = mock_create_context

        # Create analyzer with mock client
        analyzer = MatchupAnalyzer(espn_client=mock_client)

        # Test roster players
        roster_players = [
            {'id': '4431569', 'name': 'Lamar Jackson', 'position': 'QB', 'team_id': 33, 'injury_status': 'ACTIVE'},
            {'id': '4362628', 'name': 'Mark Andrews', 'position': 'TE', 'team_id': 33, 'injury_status': 'ACTIVE'},
        ]

        # Perform analysis
        analysis = await analyzer.analyze_weekly_matchups(roster_players, week=5)

        # Verify analysis results
        self.assertIsNotNone(analysis)
        self.assertEqual(analysis.week, 5)
        self.assertEqual(analysis.total_players_analyzed, 2)
        self.assertGreater(analysis.average_confidence, 0.0)

        # Verify player ratings exist
        self.assertEqual(len(analysis.player_ratings), 2)

        # Find Lamar Jackson's rating
        lamar_rating = None
        for rating in analysis.player_ratings:
            if rating.player_context.player_name == "Lamar Jackson":
                lamar_rating = rating
                break

        self.assertIsNotNone(lamar_rating)
        self.assertEqual(lamar_rating.player_context.player_position, FantasyPosition.QB)
        self.assertEqual(lamar_rating.player_context.opponent_team_abbreviation, "CIN")
        self.assertFalse(lamar_rating.player_context.is_home_game)  # Away game

        # Verify rating is reasonable (CIN allows more QB points than league average)
        self.assertGreater(lamar_rating.overall_rating, 45.0)  # Should be decent matchup
        self.assertLess(lamar_rating.overall_rating, 100.0)

        # Test analysis helper methods
        top_matchups = analysis.get_top_matchups(limit=2)
        self.assertEqual(len(top_matchups), 2)

        worst_matchups = analysis.get_worst_matchups(limit=1)
        self.assertEqual(len(worst_matchups), 1)

        # Test position-specific rankings
        qb_rankings = analysis.get_team_defense_ranking(FantasyPosition.QB)
        self.assertGreater(len(qb_rankings), 0)

        # Cleanup
        await analyzer.close()


if __name__ == '__main__':
    # Run the tests
    unittest.main()