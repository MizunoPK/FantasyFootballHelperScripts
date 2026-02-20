"""
Tests for run_game_data_fetcher.py (KAI-11: CLI refactoring pattern)
"""


class TestRunGameDataFetcher:
    """Test run_game_data_fetcher.py (KAI-11: parse_args extraction, no subprocess)"""

    def test_has_parse_args(self):
        """Test run_game_data_fetcher has parse_args function (KAI-11 refactoring)"""
        import run_game_data_fetcher
        assert hasattr(run_game_data_fetcher, 'parse_args')
        assert callable(run_game_data_fetcher.parse_args)

    def test_parse_args_defaults(self):
        """Test parse_args([]) returns correct defaults (argparse as single source of truth)"""
        import run_game_data_fetcher
        args = run_game_data_fetcher.parse_args([])
        assert args.season == 2025
        assert args.current_week == 17
        assert args.log_level == 'INFO'
        assert args.e2e_test is False
        assert args.request_timeout == 30
        assert args.historical_season is False

    def test_no_subprocess(self):
        """Test run_game_data_fetcher does not use subprocess (KAI-11 direct import)"""
        import run_game_data_fetcher
        assert not hasattr(run_game_data_fetcher, 'subprocess')
