import asyncio
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

from compile_historical_data import compile_season_data


def test_compile_season_data_uses_asyncio_gather(tmp_path: Path) -> None:
    schedule_result = {1: {}}
    bye_weeks_result = {}
    game_data_result = []

    with (
        patch(
            "compile_historical_data.asyncio.gather",
            new_callable=AsyncMock,
        ) as mock_gather,
        patch(
            "compile_historical_data.fetch_and_write_schedule",
            new_callable=AsyncMock,
        ),
        patch(
            "compile_historical_data.fetch_and_write_game_data",
            new_callable=AsyncMock,
        ),
        patch(
            "compile_historical_data.fetch_player_data",
            new_callable=AsyncMock,
            return_value=[],
        ),
        patch(
            "compile_historical_data.calculate_and_write_team_data",
            return_value=MagicMock(),
        ),
        patch("compile_historical_data.generate_weekly_snapshots"),
    ):
        mock_gather.return_value = ((schedule_result, bye_weeks_result), game_data_result)

        asyncio.run(compile_season_data(2025, tmp_path, True, True))

        assert mock_gather.call_count == 1
        assert len(mock_gather.call_args[0]) == 2
