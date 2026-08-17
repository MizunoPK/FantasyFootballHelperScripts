"""
Unit Tests for Feature 07: phase_parallelization

Tests verify that compile_season_data() dispatches asyncio.gather with the
Phase 1 (fetch_and_write_schedule) and Phase 2 (fetch_and_write_game_data)
coroutines, replacing the previous sequential awaits.

Test Category: R2 — asyncio.gather Dispatch (2 tests)
"""
import asyncio
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from compile_historical_data import compile_season_data


@pytest.mark.filterwarnings("ignore:coroutine.*was never awaited:RuntimeWarning")
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
            return_value=MagicMock(),
        ) as mock_schedule,
        patch(
            "compile_historical_data.fetch_and_write_game_data",
            return_value=MagicMock(),
        ) as mock_game_data,
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
        assert mock_schedule.call_count == 1
        assert mock_game_data.call_count == 1


@pytest.mark.filterwarnings("ignore:coroutine.*was never awaited:RuntimeWarning")
def test_compile_season_data_gather_propagates_max_weeks(tmp_path: Path) -> None:
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
            return_value=MagicMock(),
        ) as mock_schedule,
        patch(
            "compile_historical_data.fetch_and_write_game_data",
            return_value=MagicMock(),
        ) as mock_game_data,
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

        asyncio.run(compile_season_data(2025, tmp_path, True, True, max_weeks=3))

        assert mock_schedule.call_args.kwargs["max_weeks"] == 3
        assert mock_game_data.call_args.kwargs["max_weeks"] == 3
