#!/usr/bin/env python3
"""
Tests for historical_data_compiler/player_data_fetcher.py

Tests PlayerData model and raw_stats field functionality.
"""

import pytest
import sys
from pathlib import Path
from dataclasses import field

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from unittest.mock import AsyncMock, MagicMock, patch
from historical_data_compiler.player_data_fetcher import PlayerData, PlayerDataFetcher


class TestPlayerDataModel:
    """Tests for PlayerData dataclass"""

    def test_player_data_has_raw_stats_field(self):
        """PlayerData should have raw_stats field"""
        player = PlayerData(
            id="12345",
            name="Test Player",
            team="KC",
            position="QB"
        )
        assert hasattr(player, 'raw_stats')

    def test_raw_stats_defaults_to_empty_list(self):
        """raw_stats should default to empty list"""
        player = PlayerData(
            id="12345",
            name="Test Player",
            team="KC",
            position="QB"
        )
        assert player.raw_stats == []
        assert isinstance(player.raw_stats, list)

    def test_raw_stats_can_be_populated(self):
        """raw_stats should accept list of dicts"""
        test_stats = [
            {'id': '002024', 'stats': [10.0, 20.0, 30.0]},
            {'id': '102024', 'stats': [15.0, 25.0, 35.0]}
        ]
        player = PlayerData(
            id="12345",
            name="Test Player",
            team="KC",
            position="QB",
            raw_stats=test_stats
        )
        assert player.raw_stats == test_stats
        assert len(player.raw_stats) == 2

    def test_raw_stats_preserves_structure(self):
        """raw_stats should preserve ESPN API structure"""
        espn_stats = [
            {
                'id': '002024',
                'seasonId': 2024,
                'statSourceId': 0,
                'statSplitTypeId': 1,
                'stats': {
                    '0': 25.5,
                    '3': 350.2
                }
            }
        ]
        player = PlayerData(
            id="12345",
            name="Test Player",
            team="KC",
            position="QB",
            raw_stats=espn_stats
        )
        assert player.raw_stats[0]['statSourceId'] == 0
        assert player.raw_stats[0]['stats']['0'] == 25.5

    def test_player_data_all_fields(self):
        """PlayerData should support all fields including raw_stats"""
        player = PlayerData(
            id="12345",
            name="Patrick Mahomes",
            team="KC",
            position="QB",
            bye_week=10,
            fantasy_points=325.5,
            average_draft_position=8.5,
            player_rating=98.5,
            injury_status="ACTIVE",
            week_points={1: 25.5, 2: 30.2},
            projected_weeks={1: 24.0, 2: 28.0},
            raw_stats=[{'id': '002024', 'stats': []}]
        )
        assert player.id == "12345"
        assert player.name == "Patrick Mahomes"
        assert player.position == "QB"
        assert player.raw_stats == [{'id': '002024', 'stats': []}]

    def test_raw_stats_independent_instances(self):
        """Each PlayerData instance should have independent raw_stats"""
        player1 = PlayerData(id="1", name="Player1", team="KC", position="QB")
        player2 = PlayerData(id="2", name="Player2", team="SF", position="RB")

        player1.raw_stats.append({'test': 'data1'})

        assert len(player1.raw_stats) == 1
        assert len(player2.raw_stats) == 0
        assert player1.raw_stats != player2.raw_stats


class TestPlayerDataCSVConversion:
    """Tests for PlayerData to_csv_row method"""

    def test_to_csv_row_does_not_include_raw_stats(self):
        """CSV export should not include raw_stats field"""
        player = PlayerData(
            id="12345",
            name="Test Player",
            team="KC",
            position="QB",
            raw_stats=[{'test': 'data'}]
        )
        csv_row = player.to_csv_row()

        assert 'raw_stats' not in csv_row

        assert 'id' in csv_row
        assert 'name' in csv_row
        assert 'position' in csv_row


class TestParsePlayersMilestoneLogging:
    """R3: Tests for milestone-based INFO logging in _parse_players()"""

    @pytest.fixture
    def fetcher(self):
        return PlayerDataFetcher(MagicMock())

    def _make_4_players(self):
        return [{"player": {"id": str(i), "defaultPositionId": 1}} for i in range(1, 5)]

    async def _run_parse_4_players(self, fetcher):
        mock_logger = MagicMock()
        fetcher.logger = mock_logger
        with patch.object(fetcher, '_parse_single_player', new_callable=AsyncMock) as mock_parse:
            mock_parse.side_effect = [
                PlayerData(id="1", name="P1", team="KC", position="QB"),
                PlayerData(id="2", name="P2", team="SF", position="RB"),
                PlayerData(id="3", name="P3", team="DAL", position="WR"),
                PlayerData(id="4", name="P4", team="BUF", position="TE"),
            ]
            await fetcher._parse_players({"players": self._make_4_players()}, 2025, {})
        return [c.args[0] for c in mock_logger.info.call_args_list]

    @pytest.mark.parametrize("milestone_str", ["25%", "50%", "75%", "100%"])
    @pytest.mark.asyncio
    async def test_logs_milestone(self, fetcher, milestone_str):
        info_calls = await self._run_parse_4_players(fetcher)
        assert any(milestone_str in msg for msg in info_calls)

    @pytest.mark.asyncio
    async def test_milestone_message_format(self, fetcher):
        info_calls = await self._run_parse_4_players(fetcher)
        assert any(
            msg.startswith("Parsed 25% of players (") and msg.endswith("/4)")
            for msg in info_calls
        )

    @pytest.mark.asyncio
    async def test_each_milestone_logged_at_most_once(self, fetcher):
        mock_logger = MagicMock()
        fetcher.logger = mock_logger
        with patch.object(fetcher, '_parse_single_player', new_callable=AsyncMock) as mock_parse:
            mock_parse.return_value = PlayerData(id="1", name="P", team="KC", position="QB")
            await fetcher._parse_players({"players": self._make_4_players()}, 2025, {})
        info_calls = [c.args[0] for c in mock_logger.info.call_args_list]
        for pct_str in ["25%", "50%", "75%", "100%"]:
            count = sum(1 for msg in info_calls if pct_str in msg)
            assert count <= 1, f"Milestone {pct_str} logged {count} times (expected at most 1)"

    @pytest.mark.asyncio
    async def test_empty_players_no_milestone_logs(self, fetcher):
        mock_logger = MagicMock()
        fetcher.logger = mock_logger
        await fetcher._parse_players({"players": []}, 2025, {})
        info_calls = [c.args[0] for c in mock_logger.info.call_args_list]
        assert not any(
            pct_str in msg
            for pct_str in ["25%", "50%", "75%", "100%"]
            for msg in info_calls
        )

    @pytest.mark.asyncio
    async def test_100_percent_milestone_fires_when_some_players_return_none(self, fetcher):
        mock_logger = MagicMock()
        fetcher.logger = mock_logger
        with patch.object(fetcher, '_parse_single_player', new_callable=AsyncMock) as mock_parse:
            mock_parse.side_effect = [
                PlayerData(id="1", name="P", team="KC", position="QB"),
                None,
                PlayerData(id="3", name="P", team="KC", position="QB"),
                None,
            ]
            await fetcher._parse_players({"players": self._make_4_players()}, 2025, {})
        info_calls = [c.args[0] for c in mock_logger.info.call_args_list]
        assert any("100%" in msg for msg in info_calls)


class TestParsePlayersPositionRankRanges:
    """D9.2: Regression that the rating population is exactly the exported population."""

    @pytest.fixture
    def fetcher(self):
        return PlayerDataFetcher(MagicMock())

    @pytest.mark.asyncio
    async def test_range_population_is_the_exported_population(self, fetcher):
        rows = [
            {"player": {"id": "rb-best", "firstName": "Best", "lastName": "Back", "proTeamId": 1, "defaultPositionId": 2, "rankings": {"0": [{"rankType": "PPR", "slotId": 2, "averageRank": 10.0}]}, "ownership": {}, "stats": []}},
            {"player": {"id": "rb-export-floor", "firstName": "Floor", "lastName": "Back", "proTeamId": 2, "defaultPositionId": 2, "rankings": {"0": [{"rankType": "PPR", "slotId": 2, "averageRank": 20.0}]}, "ownership": {}, "stats": []}},
            {"player": {"id": "rb-unknown-team", "firstName": "Dropped", "lastName": "Back", "proTeamId": 0, "defaultPositionId": 2, "rankings": {"0": [{"rankType": "PPR", "slotId": 2, "averageRank": 30.0}]}, "ownership": {}, "stats": []}},
        ]
        with patch.object(fetcher, '_extract_weekly_points', new_callable=AsyncMock) as mock_weekly:
            mock_weekly.return_value = ({}, {})
            result = await fetcher._parse_players({"players": rows}, 2025, {"ATL": 5, "BUF": 6})
        assert [player.id for player in result] == ["rb-best", "rb-export-floor"]
        assert [player.player_rating for player in result] == [100.0, 1.0]

    @pytest.mark.asyncio
    async def test_player_without_extractable_rank_keeps_no_rating(self, fetcher):
        """A parsed player carrying no rankings leaves player_rating None.

        Covers the `positional_rank is None` continue branch in both new loops.
        """
        rows = [
            {"player": {"id": "rb-ranked-a", "firstName": "Ranked", "lastName": "Back", "proTeamId": 1, "defaultPositionId": 2, "rankings": {"0": [{"rankType": "PPR", "slotId": 2, "averageRank": 10.0}]}, "ownership": {}, "stats": []}},
            {"player": {"id": "rb-ranked-b", "firstName": "Other", "lastName": "Back", "proTeamId": 2, "defaultPositionId": 2, "rankings": {"0": [{"rankType": "PPR", "slotId": 2, "averageRank": 20.0}]}, "ownership": {}, "stats": []}},
            {"player": {"id": "rb-unranked", "firstName": "Unranked", "lastName": "Back", "proTeamId": 3, "defaultPositionId": 2, "ownership": {}, "stats": []}},
        ]
        with patch.object(fetcher, '_extract_weekly_points', new_callable=AsyncMock) as mock_weekly:
            mock_weekly.return_value = ({}, {})
            result = await fetcher._parse_players({"players": rows}, 2025, {})
        by_id = {player.id: player for player in result}
        assert by_id["rb-unranked"].player_rating is None
        assert by_id["rb-ranked-a"].player_rating == 100.0

    @pytest.mark.asyncio
    async def test_single_ranked_player_in_position_keeps_no_rating(self, fetcher):
        """A position with one ranked exported player leaves player_rating None.

        Covers the degenerate `ranges['max'] <= ranges['min']` continue branch,
        whose None is converted to 50.0 downstream by json_exporter.
        """
        rows = [
            {"player": {"id": "qb-only", "firstName": "Only", "lastName": "Passer", "proTeamId": 1, "defaultPositionId": 1, "rankings": {"0": [{"rankType": "PPR", "slotId": 0, "averageRank": 12.0}]}, "ownership": {}, "stats": []}},
        ]
        with patch.object(fetcher, '_extract_weekly_points', new_callable=AsyncMock) as mock_weekly:
            mock_weekly.return_value = ({}, {})
            result = await fetcher._parse_players({"players": rows}, 2025, {})
        assert [player.id for player in result] == ["qb-only"]
        assert result[0].player_rating is None
