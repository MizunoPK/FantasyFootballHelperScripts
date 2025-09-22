#!/usr/bin/env python3
"""
Unit tests for Starter Helper main module.

Tests the main starter helper functionality including:
- CSV-based weekly projection loading
- Roster player filtering (drafted=2)
- Optimal lineup display and formatting
- File output and logging
- Integration with LineupOptimizer
"""

import asyncio
import pytest
import sys
import tempfile
import shutil
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch
import pandas as pd
from io import StringIO

# Add the parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from starter_helper import StarterHelper, main
from lineup_optimizer import OptimalLineup, StartingRecommendation
from starter_helper_config import CURRENT_NFL_WEEK, PLAYERS_CSV


class TestStarterHelper:
    """Test suite for StarterHelper main class"""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for test files"""
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        shutil.rmtree(temp_dir, ignore_errors=True)

    @pytest.fixture
    def sample_csv_data(self):
        """Create sample CSV data with weekly projections"""
        return f"""id,name,team,position,bye_week,drafted,locked,fantasy_points,injury_status,week_{CURRENT_NFL_WEEK}_points
1,Josh Allen,BUF,QB,12,2,0,387.9,ACTIVE,28.5
2,Christian McCaffrey,SF,RB,9,2,0,285.3,ACTIVE,22.3
3,Breece Hall,NYJ,RB,11,2,0,234.7,QUESTIONABLE,18.7
4,Tyreek Hill,MIA,WR,6,2,0,267.4,ACTIVE,19.2
5,Davante Adams,LV,WR,13,2,0,198.5,ACTIVE,16.8
6,Travis Kelce,KC,TE,10,2,0,178.4,ACTIVE,14.1
7,Jaylen Waddle,MIA,WR,6,2,0,165.3,OUT,15.4
8,Justin Tucker,BAL,K,14,2,0,142.7,ACTIVE,9.2
9,Buffalo Bills,BUF,DST,12,2,0,98.6,ACTIVE,11.5
10,Backup RB,BENCH,RB,5,2,0,67.3,ACTIVE,8.3
11,Not Drafted,FREE,QB,7,0,0,200.0,ACTIVE,20.0
12,Bench Player,BENCH,WR,8,1,0,150.0,ACTIVE,12.0"""

    @pytest.fixture
    def helper(self):
        """Create StarterHelper instance"""
        return StarterHelper()

    @pytest.mark.asyncio
    async def test_load_roster_players_success(self, helper, temp_dir, sample_csv_data):
        """Test successful loading of roster players"""
        csv_file = temp_dir / "test_players.csv"
        csv_file.write_text(sample_csv_data, encoding='utf-8')

        with patch('starter_helper.PLAYERS_CSV', str(csv_file)):
            roster_players = helper.load_roster_players()

            # Should only load players with drafted=2
            assert len(roster_players) == 10  # Excluding players with drafted=0 or drafted=1
            assert all(roster_players['drafted'] == 2)

            # Verify we have expected positions
            positions = roster_players['position'].value_counts()
            assert 'QB' in positions
            assert 'RB' in positions
            assert 'WR' in positions

    def test_load_roster_players_missing_file(self, helper):
        """Test loading roster players when file doesn't exist"""
        with patch('starter_helper.PLAYERS_CSV', 'nonexistent_file.csv'):
            with pytest.raises(FileNotFoundError):
                helper.load_roster_players()

    @pytest.mark.asyncio
    async def test_get_current_week_projections_success(self, helper, temp_dir, sample_csv_data):
        """Test successful extraction of current week projections"""
        csv_file = temp_dir / "test_players.csv"
        csv_file.write_text(sample_csv_data, encoding='utf-8')

        with patch('starter_helper.PLAYERS_CSV', str(csv_file)):
            roster_players = helper.load_roster_players()
            projections = helper.get_current_week_projections(roster_players)

            # Should extract projections for all roster players
            assert len(projections) == len(roster_players)

            # Check specific projections
            assert projections['1'] == 28.5  # Josh Allen
            assert projections['2'] == 22.3  # CMC
            assert projections['3'] == 18.7  # Breece Hall

            # All projections should be floats
            for player_id, points in projections.items():
                assert isinstance(points, float)
                assert points >= 0.0

    def test_get_current_week_projections_missing_column(self, helper):
        """Test projections when weekly column is missing"""
        # Create DataFrame without weekly column
        roster_data = {
            'id': [1, 2],
            'name': ['Player 1', 'Player 2'],
            'position': ['QB', 'RB']
        }
        roster_players = pd.DataFrame(roster_data)

        projections = helper.get_current_week_projections(roster_players)

        # Should return 0.0 for all players when column missing
        assert len(projections) == 2
        assert all(points == 0.0 for points in projections.values())

    def test_get_current_week_projections_invalid_data(self, helper):
        """Test projections with invalid weekly data"""
        # Create DataFrame with invalid weekly data
        week_col = f"week_{CURRENT_NFL_WEEK}_points"
        roster_data = {
            'id': [1, 2, 3, 4],
            'name': ['Valid', 'NaN', 'None', 'Invalid'],
            'position': ['QB', 'RB', 'WR', 'TE'],
            week_col: [20.5, float('nan'), None, 'invalid']
        }
        roster_players = pd.DataFrame(roster_data)

        projections = helper.get_current_week_projections(roster_players)

        # Should handle invalid data gracefully
        assert projections['1'] == 20.5  # Valid data
        assert projections['2'] == 0.0   # NaN converted
        assert projections['3'] == 0.0   # None converted
        assert projections['4'] == 0.0   # Invalid string converted

    def test_display_optimal_lineup(self, helper):
        """Test optimal lineup display formatting"""
        # Create sample optimal lineup
        lineup = OptimalLineup()
        lineup.qb = StartingRecommendation("1", "Josh Allen", "QB", "BUF", 28.5, "ACTIVE", 12, 28.5, "No penalties")
        lineup.rb1 = StartingRecommendation("2", "CMC", "RB", "SF", 22.3, "ACTIVE", 9, 22.3, "No penalties")
        lineup.rb2 = StartingRecommendation("3", "Breece Hall", "RB", "NYJ", 18.7, "QUESTIONABLE", 11, 13.7, "-5 injury penalty")
        lineup.wr1 = StartingRecommendation("4", "Tyreek Hill", "WR", "MIA", 19.2, "ACTIVE", 6, 19.2, "No penalties")
        lineup.wr2 = StartingRecommendation("5", "Davante Adams", "WR", "LV", 16.8, "ACTIVE", 13, 16.8, "No penalties")
        lineup.te = StartingRecommendation("6", "Travis Kelce", "TE", "KC", 14.1, "ACTIVE", 10, 14.1, "No penalties")
        lineup.flex = StartingRecommendation("7", "Waddle", "WR", "MIA", 15.4, "OUT", 6, 5.4, "-10 injury penalty")
        lineup.k = StartingRecommendation("8", "Tucker", "K", "BAL", 9.2, "ACTIVE", 14, 9.2, "No penalties")
        lineup.dst = StartingRecommendation("9", "Bills DST", "DST", "BUF", 11.5, "ACTIVE", 12, 11.5, "No penalties")

        # Capture output
        helper.output_buffer = StringIO()

        helper.display_optimal_lineup(lineup)
        output = helper.output_buffer.getvalue()

        # Verify output contains expected elements
        assert "OPTIMAL STARTING LINEUP" in output
        assert f"WEEK {CURRENT_NFL_WEEK}" in output
        assert "Josh Allen" in output
        assert "CMC" in output
        assert "TOTAL PROJECTED POINTS" in output

        # Verify lineup positions are displayed in correct order
        lines = output.split('\n')
        lineup_lines = [line for line in lines if any(pos in line for pos in ['QB  :', 'RB  :', 'WR  :', 'TE  :', 'FLEX:', 'K   :', 'DEF :'])]

        # Should have 9 lineup positions
        assert len(lineup_lines) >= 9

    def test_display_bench_recommendations(self, helper):
        """Test bench recommendations display"""
        bench_recs = [
            StartingRecommendation("10", "Bench Player 1", "RB", "TEST", 12.0, "ACTIVE", 5, 12.0, "No penalties"),
            StartingRecommendation("11", "Bench Player 2", "WR", "TEST", 10.5, "QUESTIONABLE", 7, 7.5, "-3 injury penalty")
        ]

        helper.output_buffer = StringIO()
        helper.display_bench_recommendations(bench_recs, set())

        output = helper.output_buffer.getvalue()

        assert "TOP BENCH ALTERNATIVES" in output
        assert "Bench Player 1" in output
        assert "Bench Player 2" in output
        assert "12.0 pts" in output

    def test_display_roster_summary(self, helper, temp_dir, sample_csv_data):
        """Test full roster summary display"""
        csv_file = temp_dir / "test_players.csv"
        csv_file.write_text(sample_csv_data, encoding='utf-8')

        with patch('starter_helper.PLAYERS_CSV', str(csv_file)), \
             patch('starter_helper.SHOW_PROJECTION_DETAILS', True):

            roster_players = helper.load_roster_players()
            projections = helper.get_current_week_projections(roster_players)

            helper.output_buffer = StringIO()
            helper.display_roster_summary(roster_players, projections)

            output = helper.output_buffer.getvalue()

            if output:  # Only check if SHOW_PROJECTION_DETAILS is True
                assert "FULL ROSTER" in output
                assert f"WEEK {CURRENT_NFL_WEEK} PROJECTIONS" in output

    @pytest.mark.asyncio
    async def test_save_output_to_files(self, helper, temp_dir):
        """Test saving output to files"""
        with patch('starter_helper.SAVE_OUTPUT_TO_FILE', True), \
             patch('starter_helper_config.DATA_DIR', str(temp_dir)):

            test_content = "Test output content\nLine 2\nLine 3"
            helper.save_output_to_files(test_content)

            # Check that files were created (timestamped and latest)
            files = list(temp_dir.glob("*.txt"))
            assert len(files) >= 1  # At least latest file should be created

            # Verify content
            for file in files:
                content = file.read_text(encoding='utf-8')
                assert test_content in content

    @pytest.mark.asyncio
    async def test_save_output_disabled(self, helper):
        """Test that output saving is skipped when disabled"""
        with patch('starter_helper.SAVE_OUTPUT_TO_FILE', False):
            # Should not raise any errors or create files
            helper.save_output_to_files("test content")

    @pytest.mark.asyncio
    async def test_run_complete_workflow(self, helper, temp_dir, sample_csv_data):
        """Test complete starter helper workflow"""
        csv_file = temp_dir / "test_players.csv"
        csv_file.write_text(sample_csv_data, encoding='utf-8')

        with patch('starter_helper.PLAYERS_CSV', str(csv_file)), \
             patch('starter_helper.SAVE_OUTPUT_TO_FILE', False):

            # Should complete without errors
            await helper.run()

            output = helper.output_buffer.getvalue()

            # Verify output contains expected sections
            assert "Fantasy Football Starter Helper" in output
            assert f"Week {CURRENT_NFL_WEEK}" in output
            assert "OPTIMAL STARTING LINEUP" in output
            assert "TOTAL PROJECTED POINTS" in output

    @pytest.mark.asyncio
    async def test_run_no_roster_players(self, helper, temp_dir):
        """Test run with no roster players (drafted=2)"""
        # Create CSV with no drafted=2 players
        csv_data = """id,name,team,position,drafted,week_{}_points
1,Free Agent,FA,QB,0,20.0
2,Drafted by Other,OTHER,RB,1,15.0""".format(CURRENT_NFL_WEEK)

        csv_file = temp_dir / "empty_roster.csv"
        csv_file.write_text(csv_data, encoding='utf-8')

        with patch('starter_helper.PLAYERS_CSV', str(csv_file)), \
             patch('starter_helper.SAVE_OUTPUT_TO_FILE', False):

            await helper.run()

            output = helper.output_buffer.getvalue()
            assert "No roster players found" in output

    @pytest.mark.asyncio
    async def test_run_error_handling(self, helper):
        """Test error handling in run method"""
        with patch('starter_helper.PLAYERS_CSV', 'nonexistent_file.csv'), \
             patch('starter_helper.SAVE_OUTPUT_TO_FILE', False):

            # Should handle FileNotFoundError gracefully
            with pytest.raises(FileNotFoundError):
                await helper.run()

    def test_print_and_capture(self, helper):
        """Test print and capture functionality"""
        helper.output_buffer = StringIO()

        test_message = "Test message for capture"

        # Capture print output
        with patch('builtins.print') as mock_print:
            helper.print_and_capture(test_message)
            mock_print.assert_called_once_with(test_message)

        # Verify message was captured
        captured = helper.output_buffer.getvalue()
        assert test_message in captured

    def test_setup_logging_enabled(self, helper):
        """Test logging setup when enabled"""
        with patch('starter_helper.LOGGING_ENABLED', True), \
             patch('starter_helper.LOGGING_LEVEL', 'INFO'), \
             patch('logging.basicConfig') as mock_config:

            helper.setup_logging()
            mock_config.assert_called_once()

    def test_setup_logging_disabled(self, helper):
        """Test logging setup when disabled"""
        with patch('starter_helper.LOGGING_ENABLED', False), \
             patch('logging.disable') as mock_disable:

            helper.setup_logging()
            mock_disable.assert_called_once()

    @pytest.mark.asyncio
    async def test_integration_with_lineup_optimizer(self, helper, temp_dir, sample_csv_data):
        """Test integration with LineupOptimizer"""
        csv_file = temp_dir / "test_players.csv"
        csv_file.write_text(sample_csv_data, encoding='utf-8')

        with patch('starter_helper.PLAYERS_CSV', str(csv_file)):
            roster_players = helper.load_roster_players()
            projections = helper.get_current_week_projections(roster_players)

            # Test that optimizer produces valid lineup
            optimal_lineup = helper.optimizer.optimize_lineup(roster_players, projections)

            assert isinstance(optimal_lineup, OptimalLineup)
            assert optimal_lineup.qb is not None  # Should have QB
            assert optimal_lineup.total_projected_points > 0

    @pytest.mark.asyncio
    async def test_main_function_integration(self):
        """Test main function integration"""
        with patch('starter_helper.StarterHelper') as mock_helper_class:
            mock_helper = AsyncMock()
            mock_helper_class.return_value = mock_helper

            await main()

            mock_helper_class.assert_called_once()
            mock_helper.run.assert_called_once()

    @pytest.mark.asyncio
    async def test_large_roster_performance(self, helper, temp_dir):
        """Test performance with large roster"""
        # Create large roster CSV
        csv_lines = [f"id,name,team,position,bye_week,drafted,week_{CURRENT_NFL_WEEK}_points"]

        for i in range(100):  # Large roster
            position = ['QB', 'RB', 'WR', 'TE', 'K', 'DST'][i % 6]
            csv_lines.append(f"{i+1},Player {i+1},TEAM{i%8},{position},{(i%17)+1},2,{10.0 + (i*0.1)}")

        csv_data = '\n'.join(csv_lines)
        csv_file = temp_dir / "large_roster.csv"
        csv_file.write_text(csv_data, encoding='utf-8')

        import time
        start_time = time.time()

        with patch('starter_helper.PLAYERS_CSV', str(csv_file)), \
             patch('starter_helper.SAVE_OUTPUT_TO_FILE', False):

            await helper.run()

        end_time = time.time()

        # Should complete large roster in reasonable time (increased for matchup analysis)
        assert end_time - start_time < 60.0

        output = helper.output_buffer.getvalue()
        assert "OPTIMAL STARTING LINEUP" in output

    def test_edge_case_empty_projections(self, helper):
        """Test handling of empty projections"""
        roster_data = {
            'id': [1, 2],
            'name': ['Player 1', 'Player 2'],
            'position': ['QB', 'RB']
        }
        roster_players = pd.DataFrame(roster_data)

        # No weekly column - should return all zeros
        projections = helper.get_current_week_projections(roster_players)

        assert len(projections) == 2
        assert all(points == 0.0 for points in projections.values())

    def test_unicode_player_names(self, helper, temp_dir):
        """Test handling of unicode player names"""
        csv_data = f"""id,name,team,position,drafted,week_{CURRENT_NFL_WEEK}_points
1,José Rodríguez,MIA,QB,2,25.0
2,François Müller,GB,RB,2,20.0"""

        csv_file = temp_dir / "unicode_players.csv"
        csv_file.write_text(csv_data, encoding='utf-8')

        with patch('starter_helper.PLAYERS_CSV', str(csv_file)):
            roster_players = helper.load_roster_players()
            projections = helper.get_current_week_projections(roster_players)

            assert len(roster_players) == 2
            assert 'José Rodríguez' in roster_players['name'].values
            assert 'François Müller' in roster_players['name'].values
            assert projections['1'] == 25.0
            assert projections['2'] == 20.0


if __name__ == "__main__":
    # Run tests with pytest if available, otherwise basic test
    try:
        import pytest
        pytest.main([__file__, "-v"])
    except ImportError:
        print("pytest not available, running basic tests...")

        async def run_basic_tests():
            helper = StarterHelper()

            # Test basic initialization
            assert helper.optimizer is not None
            assert helper.output_buffer is not None
            print("✅ Initialization test passed")

            # Test print and capture
            helper.output_buffer = StringIO()
            helper.print_and_capture("Test message")
            assert "Test message" in helper.output_buffer.getvalue()
            print("✅ Print and capture test passed")

            # Test projections with empty data
            roster_data = pd.DataFrame({
                'id': [1, 2],
                'name': ['Player 1', 'Player 2'],
                'position': ['QB', 'RB']
            })
            projections = helper.get_current_week_projections(roster_data)
            assert len(projections) == 2
            print("✅ Empty projections handling test passed")

            # Test main function
            with patch('starter_helper.StarterHelper') as mock_helper_class:
                mock_helper = AsyncMock()
                mock_helper_class.return_value = mock_helper

                await main()
                mock_helper.run.assert_called_once()
            print("✅ Main function test passed")

            print("Basic tests completed successfully!")

        asyncio.run(run_basic_tests())