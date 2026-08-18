#!/usr/bin/env python3
"""
Tests for Player Data Exporter Module

Basic smoke tests for data export functionality.

Author: Kai Mizuno
"""

import pytest
import asyncio
import json
from unittest.mock import Mock, patch, AsyncMock
from pathlib import Path

from player_data_fetcher.player_data_exporter import DataExporter, zero_bye_week_points
from player_data_fetcher.player_data_models import (
    ProjectionData, PlayerProjection, ESPNPlayerData, PlayerDataValidationError,
)


# FIXTURES

@pytest.fixture(autouse=True)
def sandbox_fetcher_data_root(tmp_path, monkeypatch):
    """T91: redirect the fetcher's data ROOT into a per-test sandbox.

    Defence in depth beneath each test's own explicit injection. Every
    DataExporter constructed in this file without explicit path parameters
    resolves its defaults under this sandbox rather than the tracked repo
    data/ tree, so a future test that adds an `await exporter.export_*()` call
    cannot silently acquire T91's defect.

    The sandbox subdirectory is deliberately NOT named 'data': a root named
    'data' would make T41's `endswith('data/player_data')` assertions pass
    vacuously against the sandbox instead of the repo (spec.md:87).

    A test that must observe the UNREDIRECTED production defaults opts out with
    `monkeypatch.delenv('PLAYER_DATA_DIR', raising=False)` -- see
    test_exporter_defaults_anchored_to_repo_data_root.
    """
    monkeypatch.setenv('PLAYER_DATA_DIR', str(tmp_path / 'fetcher_root'))


@pytest.fixture
def espn_data_with_weekly_stats():
    """A 17-week ESPN stat stub with distinct projected and actual weekly totals.

    Projected (statSourceId=1) is 10.0 + week; actual (statSourceId=0) is
    20.0 + week. Distinct per-week values make a bye-slot zeroing observable
    at exactly one index instead of hiding inside a uniform array.
    """
    raw_stats = []
    for week in range(1, 18):
        raw_stats.append({'scoringPeriodId': week, 'statSourceId': 1, 'appliedTotal': 10.0 + week})
        raw_stats.append({'scoringPeriodId': week, 'statSourceId': 0, 'appliedTotal': 20.0 + week})

    espn_data = Mock()
    espn_data.configure_mock(raw_stats=raw_stats)
    return espn_data


@pytest.fixture
def bye_week_player():
    """Factory for the minimal FantasyPlayer stand-in _prepare_position_json_data reads."""
    def _make(bye_week):
        player = Mock()
        player.configure_mock(
            id=1,
            name="Test Player",
            team="KC",
            position="UNKNOWN",
            bye_week=bye_week,
            injury_status="ACTIVE",
            drafted_by="",
            locked=False,
            average_draft_position=None,
            player_rating=None,
        )
        return player

    return _make


class TestDataExporterInit:
    """Test DataExporter initialization"""

    def test_exporter_initialization(self, tmp_path):
        """Test DataExporter can be initialized"""
        output_dir = str(tmp_path / "output")
        exporter = DataExporter(output_dir=output_dir)

        assert exporter.output_dir == Path(output_dir)

    def test_exporter_creates_output_directory(self, tmp_path):
        """Test DataExporter creates output directory if it doesn't exist"""
        output_dir = str(tmp_path / "nonexistent" / "output")
        exporter = DataExporter(output_dir=output_dir)

        assert exporter.output_dir.exists()

class TestSetTeamData:
    """Test setting team rankings and schedules"""

    def test_set_team_rankings(self, tmp_path):
        """Test set_team_rankings stores data correctly"""
        exporter = DataExporter(output_dir=str(tmp_path))

        team_rankings = {'KC': {'offense': 1, 'defense': 5}}
        exporter.set_team_rankings(team_rankings)

        assert exporter.team_rankings == team_rankings

    def test_set_current_week_schedule(self, tmp_path):
        """Test set_current_week_schedule stores data correctly"""
        exporter = DataExporter(output_dir=str(tmp_path))

        schedule = {'KC': 'vs SF'}
        exporter.set_current_week_schedule(schedule)

        assert exporter.current_week_schedule == schedule


class TestGetFantasyPlayers:
    """Test converting to FantasyPlayer objects"""

    def test_get_fantasy_players_returns_list(self, tmp_path):
        """Test get_fantasy_players returns list of FantasyPlayer objects"""
        exporter = DataExporter(output_dir=str(tmp_path), use_csv_ownership=True)

        projection_data = ProjectionData(
            season=2024,
            scoring_format='PPR',
            total_players=1,
            players=[
                PlayerProjection(id="1", name="Test", position="QB", team="KC", fantasy_points=300.0)
            ]
        )

        result = exporter.get_fantasy_players(projection_data)

        assert isinstance(result, list)
        assert len(result) == 1

    def test_get_fantasy_players_with_empty_data(self, tmp_path):
        """Test get_fantasy_players handles empty data"""
        exporter = DataExporter(output_dir=str(tmp_path), use_csv_ownership=True)

        projection_data = ProjectionData(
            season=2024,
            scoring_format='PPR',
            total_players=0,
            players=[]
        )

        result = exporter.get_fantasy_players(projection_data)

        assert isinstance(result, list)
        assert len(result) == 0


class TestPositionJSONExport:
    """Test that position JSON export still works after legacy format removal"""

    @pytest.mark.asyncio
    async def test_position_json_files_created(self, tmp_path):
        """Test that position JSON files are created (regression test)"""
        output_dir = tmp_path / "player_data_fetcher" / "data"
        # T91: export_position_json_files() writes through position_json_output,
        # NOT output_dir. Sandboxing output_dir alone sent every write straight
        # into the tracked repo data/player_data/ tree.
        position_json_output = tmp_path / "player_data_fetcher" / "position_json"

        exporter = DataExporter(
            output_dir=str(output_dir),
            position_json_output=str(position_json_output),
            use_csv_ownership=True,
        )

        projection_data = ProjectionData(
            season=2024,
            scoring_format='PPR',
            total_players=2,
            players=[
                PlayerProjection(id="1", name="QB Player", position="QB", team="KC", fantasy_points=300.0),
                PlayerProjection(id="2", name="RB Player", position="RB", team="SF", fantasy_points=250.0)
            ]
        )

        exporter.set_team_rankings({'KC': {'offense': 1, 'defense': 5}, 'SF': {'offense': 2, 'defense': 3}})

        files = await exporter.export_position_json_files(projection_data)

        assert len(files) > 0, "Position JSON files should be created"
        assert all(f.endswith('.json') for f in files), "All files should be JSON"
        assert all(f.startswith(str(position_json_output)) for f in files), \
            "T91: every exported file must land inside the tmp_path sandbox, " \
            "never the tracked repo data/player_data/ tree"

    def test_zero_bye_week_points_in_range(self, tmp_path):
        """A valid bye zeroes the matching slot in both arrays only."""
        exporter = DataExporter(output_dir=str(tmp_path))
        projected_points = [float(week) for week in range(1, 18)]
        actual_points = [float(week + 20) for week in range(1, 18)]

        exporter._zero_bye_week_points(projected_points, actual_points, 6)

        assert projected_points == [1.0, 2.0, 3.0, 4.0, 5.0, 0.0] + [float(week) for week in range(7, 18)]
        assert actual_points == [21.0, 22.0, 23.0, 24.0, 25.0, 0.0] + [float(week) for week in range(27, 38)]

    @pytest.mark.parametrize("bye_week", [None, 0, -1, 18])
    def test_zero_bye_week_points_skips_invalid_byes(self, tmp_path, bye_week):
        """Falsey and out-of-range byes neither mutate nor index either array."""
        exporter = DataExporter(output_dir=str(tmp_path))
        projected_points = [1.0] * 17
        actual_points = [2.0] * 17

        exporter._zero_bye_week_points(projected_points, actual_points, bye_week)

        assert projected_points == [1.0] * 17
        assert actual_points == [2.0] * 17

    def test_zero_bye_week_points_method_delegates_to_module_owner(self, tmp_path):
        """D3.2 UD6: the retained method is a real pass-through to the single owner.

        Spied with wraps=, not stubbed, so the module-level function still runs:
        the call assertion proves the delegation edge exists and the array
        assertions prove the two forms agree rather than both merely existing.
        """
        exporter = DataExporter(output_dir=str(tmp_path))
        projected_points = [float(week) for week in range(1, 18)]
        actual_points = [float(week + 20) for week in range(1, 18)]

        with patch(
            "player_data_fetcher.player_data_exporter.zero_bye_week_points",
            wraps=zero_bye_week_points,
        ) as owner_spy:
            exporter._zero_bye_week_points(projected_points, actual_points, 6)

        owner_spy.assert_called_once_with(projected_points, actual_points, 6)
        assert projected_points == [1.0, 2.0, 3.0, 4.0, 5.0, 0.0] + [float(week) for week in range(7, 18)]
        assert actual_points == [21.0, 22.0, 23.0, 24.0, 25.0, 0.0] + [float(week) for week in range(27, 38)]

    def test_prepare_position_json_data_applies_bye_helper(
        self, tmp_path, bye_week_player, espn_data_with_weekly_stats
    ):
        """D3.4 cutover: the record builder invokes the bye helper once, before serializing.

        Inverts D3.1's provision-era idleness guard. The helper is spied with
        wraps=, not stubbed, so the real predicate still runs on this edge.
        """
        exporter = DataExporter(output_dir=str(tmp_path))

        with patch.object(
            exporter, "_zero_bye_week_points", wraps=exporter._zero_bye_week_points
        ) as zero_spy:
            result = exporter._prepare_position_json_data(
                bye_week_player(6), espn_data_with_weekly_stats, "UNKNOWN"
            )

        zero_spy.assert_called_once_with(
            result["projected_points"], result["actual_points"], 6
        )
        assert result["projected_points"][5] == 0.0
        assert result["actual_points"][5] == 0.0

    @pytest.mark.parametrize("bye_week", [1, 6, 17])
    def test_prepare_position_json_data_zeroes_in_range_bye(
        self, tmp_path, bye_week_player, espn_data_with_weekly_stats, bye_week
    ):
        """An in-range bye zeroes both emitted arrays at bye-1 and no other slot.

        Covers both inside boundaries (1 and 17) as well as an interior value, so
        an off-by-one in the helper's sole numeric bound (0 <= bye_idx < 17) fails
        here. current_nfl_week is passed explicitly so every actual-points slot is
        populated and the only zero in either array is the bye slot itself.
        """
        exporter = DataExporter(output_dir=str(tmp_path), current_nfl_week=18)

        result = exporter._prepare_position_json_data(
            bye_week_player(bye_week), espn_data_with_weekly_stats, "UNKNOWN"
        )

        assert result["projected_points"] == [
            0.0 if week == bye_week else float(10 + week) for week in range(1, 18)
        ]
        assert result["actual_points"] == [
            0.0 if week == bye_week else float(20 + week) for week in range(1, 18)
        ]

    @pytest.mark.parametrize("bye_week", [None, 0, -1, 18])
    def test_prepare_position_json_data_leaves_invalid_byes_untouched(
        self, tmp_path, bye_week_player, espn_data_with_weekly_stats, bye_week
    ):
        """Falsey and out-of-range byes emit the pre-cutover arrays without raising.

        current_nfl_week is passed explicitly so no slot is zeroed by the
        actual-points recency gate, leaving the bye predicate the only thing
        under test.
        """
        exporter = DataExporter(output_dir=str(tmp_path), current_nfl_week=18)

        result = exporter._prepare_position_json_data(
            bye_week_player(bye_week), espn_data_with_weekly_stats, "UNKNOWN"
        )

        assert result["projected_points"] == [float(10 + week) for week in range(1, 18)]
        assert result["actual_points"] == [float(20 + week) for week in range(1, 18)]

    def test_prepare_position_json_data_handles_missing_espn_data(
        self, tmp_path, bye_week_player
    ):
        """A player absent from the ESPN stat map still emits the zero-filled arrays.

        _export_single_position_json resolves espn_data by dict .get(), which
        yields None on a miss, so the cutover runs the helper over both fallback
        arrays on a live branch.
        """
        exporter = DataExporter(output_dir=str(tmp_path))

        result = exporter._prepare_position_json_data(
            bye_week_player(6), None, "UNKNOWN"
        )

        assert result["projected_points"] == [0.0] * 17
        assert result["actual_points"] == [0.0] * 17

    def test_prepare_position_json_data_preserves_key_order(
        self, tmp_path, bye_week_player, espn_data_with_weekly_stats
    ):
        """The cutover changes two values, never the record's key set or order."""
        exporter = DataExporter(output_dir=str(tmp_path))

        result = exporter._prepare_position_json_data(
            bye_week_player(6), espn_data_with_weekly_stats, "UNKNOWN"
        )

        assert list(result.keys()) == [
            "id",
            "name",
            "team",
            "position",
            "bye_week",
            "injury_status",
            "drafted_by",
            "locked",
            "average_draft_position",
            "player_rating",
            "projected_points",
            "actual_points",
        ]


class TestDataExporterKAI10:
    """
    Tests verifying KAI-10 refactoring: DataExporter constructor accepts
    new parameters and defaults match old config.py values.
    (REQ-07 — 6 tests)
    """

    def test_exporter_accepts_my_team_name_parameter(self, tmp_path):
        """7.1: DataExporter accepts my_team_name constructor parameter"""
        exporter = DataExporter(
            output_dir=str(tmp_path),
            my_team_name='Test Team',
        )
        assert exporter.my_team_name == 'Test Team'

    def test_exporter_accepts_current_nfl_week_parameter(self, tmp_path):
        """7.2: DataExporter accepts current_nfl_week constructor parameter"""
        exporter = DataExporter(
            output_dir=str(tmp_path),
            current_nfl_week=10,
        )
        assert exporter.current_nfl_week == 10

    def test_exporter_backward_compat_no_new_params(self, tmp_path):
        """7.3: DataExporter(output_dir=...) still works without new params (backward compat)"""
        exporter = DataExporter(output_dir=str(tmp_path))
        assert exporter.current_nfl_week == 17
        assert exporter.my_team_name == 'Sea Sharp'
        assert exporter.load_drafted_data is True

    def test_exporter_defaults_anchored_to_repo_data_root(self, tmp_path, monkeypatch):
        """I-8 (T41): DataExporter path defaults are repo-anchored absolute paths, no longer cwd-relative '../data/...'

        T91: explicitly opts OUT of this file's autouse PLAYER_DATA_DIR redirect so
        the six assertions below keep their original T41 subject -- the UNREDIRECTED
        production defaults. Opting out is safe here: this test only reads
        constructor attributes and writes nothing. Do not remove the delenv, and do
        not weaken any of the six assertions.
        """
        monkeypatch.delenv('PLAYER_DATA_DIR', raising=False)
        exporter = DataExporter(output_dir=str(tmp_path))
        assert Path(exporter.position_json_output).is_absolute()
        assert exporter.position_json_output.endswith('data/player_data')
        assert Path(exporter.team_data_folder).is_absolute()
        assert exporter.team_data_folder.endswith('data/team_data')
        assert Path(exporter.drafted_data_path).is_absolute()
        assert exporter.drafted_data_path.endswith('data/drafted_data.csv')

    def test_exporter_custom_team_name_used(self, tmp_path):
        """E-14: DataExporter with custom my_team_name stores it correctly"""
        exporter = DataExporter(
            output_dir=str(tmp_path),
            my_team_name='My Custom Team',
        )
        assert exporter.my_team_name == 'My Custom Team'

    def test_exporter_custom_drafted_data_path(self, tmp_path):
        """E-18: DataExporter with custom drafted_data_path stores it correctly"""
        custom_path = str(tmp_path / 'custom_drafted.csv')
        exporter = DataExporter(
            output_dir=str(tmp_path),
            drafted_data_path=custom_path,
        )
        assert exporter.drafted_data_path == custom_path


class TestDataExporterDataRootSeam:
    """T91: DataExporter resolves its path defaults at CONSTRUCTION time (spec D2, AC2/AC3/AC4)"""

    def test_defaults_redirect_under_player_data_dir(self, monkeypatch, tmp_path):
        """T91-5 (AC2): with PLAYER_DATA_DIR set, a no-path-param DataExporter lands under it"""
        root = tmp_path / 'fetcher_root'
        monkeypatch.setenv('PLAYER_DATA_DIR', str(root))

        exporter = DataExporter(output_dir=str(tmp_path / 'out'))

        assert exporter.position_json_output == str(root / 'player_data')
        assert exporter.team_data_folder == str(root / 'team_data')
        assert exporter.drafted_data_path == str(root / 'drafted_data.csv')

    def test_defaults_are_repo_anchored_when_unset(self, monkeypatch, tmp_path):
        """T91-6 (AC3): with PLAYER_DATA_DIR unset, the defaults are byte-identical to today's"""
        monkeypatch.delenv('PLAYER_DATA_DIR', raising=False)
        repo_data = Path(__file__).parent.parent.parent / 'data'

        exporter = DataExporter(output_dir=str(tmp_path / 'out'))

        assert exporter.position_json_output == str(repo_data / 'player_data')
        assert exporter.team_data_folder == str(repo_data / 'team_data')
        assert exporter.drafted_data_path == str(repo_data / 'drafted_data.csv')

    def test_env_set_after_import_still_redirects(self, monkeypatch, tmp_path):
        """T91-7 (AC4): the module is ALREADY imported when the variable is set.

        This is the regression guard for the naive form the spec forbids. A
        def-time-baked default (or a _DATA_ROOT monkeypatch) is captured once at
        import and would ignore this setenv entirely -- passing silently while
        protecting nothing. Setting the variable here, after import, makes that
        regression FAIL instead.
        """
        import player_data_fetcher.player_data_exporter as exporter_module

        assert exporter_module is not None, "module already imported at collection time"
        late_root = tmp_path / 'set_after_import'
        monkeypatch.setenv('PLAYER_DATA_DIR', str(late_root))

        exporter = DataExporter(output_dir=str(tmp_path / 'out'))

        assert exporter.position_json_output == str(late_root / 'player_data')

    def test_explicit_injection_wins_over_the_env_seam(self, monkeypatch, tmp_path):
        """T91-8: an explicitly passed path beats PLAYER_DATA_DIR (D1 above D2)"""
        monkeypatch.setenv('PLAYER_DATA_DIR', str(tmp_path / 'fetcher_root'))
        explicit = str(tmp_path / 'explicit_json')

        exporter = DataExporter(
            output_dir=str(tmp_path / 'out'),
            position_json_output=explicit,
        )

        assert exporter.position_json_output == explicit
        assert exporter.team_data_folder == str(tmp_path / 'fetcher_root' / 'team_data')

    def test_position_json_export_writes_only_under_the_redirected_root(self, monkeypatch, tmp_path):
        """T91-9: the ACTUAL WRITE follows the seam, with no explicit injection.

        This is the twelve-latent-constructions case made live: a construction
        that passes no path parameter, then exports. Without the seam this write
        lands in the tracked repo data/player_data/ tree -- exactly T91.
        """
        root = tmp_path / 'fetcher_root'
        monkeypatch.setenv('PLAYER_DATA_DIR', str(root))
        exporter = DataExporter(output_dir=str(tmp_path / 'out'), use_csv_ownership=True)
        exporter.set_team_rankings({'KC': {'offense': 1, 'defense': 5}})
        projection_data = ProjectionData(
            season=2024,
            scoring_format='PPR',
            total_players=1,
            players=[
                PlayerProjection(id="1", name="QB Player", position="QB", team="KC", fantasy_points=300.0)
            ]
        )

        files = asyncio.run(exporter.export_position_json_files(projection_data))

        assert len(files) > 0
        assert all(f.startswith(str(root)) for f in files), \
            "every exported file must land under the PLAYER_DATA_DIR root"
        assert all(str(tmp_path) in f for f in files), \
            "no exported file may escape tmp_path into the tracked repo tree"



class TestUseCsvOwnershipFlag:
    """D17.5 D1/D2: the flag now defaults False (ESPN is the default supplier),
    DraftedRosterManager construction is gated on it, and get_fantasy_players
    branches on it."""

    def test_default_use_csv_ownership_is_false(self, tmp_path):
        """D17.5 D1: use_csv_ownership defaults False -- the ESPN snapshot is
        the default ownership supplier after the cutover."""
        exporter = DataExporter(
            output_dir=str(tmp_path / 'out'),
            load_drafted_data=False,
        )
        assert exporter.use_csv_ownership is False

    def test_drafted_roster_manager_not_constructed_on_the_default_path(self, tmp_path):
        """D17.5 D2: on the default (ESPN) path the legacy CSV owner is absent
        from the object graph -- not merely unused."""
        exporter = DataExporter(
            output_dir=str(tmp_path / 'out'),
            load_drafted_data=False,
        )
        assert exporter.drafted_roster_manager is None

    def test_drafted_roster_manager_constructed_on_the_rollback_path(self, tmp_path):
        """D17.5 D2: --use-csv-ownership still builds the legacy owner, so the
        rollback path is intact."""
        exporter = DataExporter(
            output_dir=str(tmp_path / 'out'),
            load_drafted_data=False,
            use_csv_ownership=True,
        )
        assert exporter.drafted_roster_manager is not None


class TestLoadEspnAttribution:
    """D17.4 CONCERN-1 (polish): coverage for the exporter's only new async
    method -- the session-wrapped live fetch, the fail-fast on missing
    espn_settings, and the fail-closed PlayerDataValidationError raise that
    AC4 requires but the pre-polish diff never exercised."""

    def test_no_op_when_use_csv_ownership_true(self, tmp_path):
        """No-op path: neither ConfigManager nor ESPNClient is touched."""
        exporter = DataExporter(
            output_dir=str(tmp_path / 'out'),
            load_drafted_data=False,
            use_csv_ownership=True,
        )

        with patch('player_data_fetcher.espn_client.ESPNClient') as mock_client_cls:
            asyncio.run(exporter.load_espn_attribution(players=[]))

        mock_client_cls.assert_not_called()
        assert exporter._espn_attribution is None

    def test_raises_fast_when_espn_settings_missing(self, tmp_path):
        """New Copilot PR comment (player_data_exporter.py:142): espn_settings
        is an optional ctor arg; use_csv_ownership=False with no espn_settings
        must fail fast with a clear error, not AttributeError or
        ESPNClient(None)."""
        exporter = DataExporter(
            output_dir=str(tmp_path / 'out'),
            load_drafted_data=False,
            use_csv_ownership=False,
            espn_settings=None,
        )

        with patch('player_data_fetcher.espn_client.ESPNClient') as mock_client_cls:
            with pytest.raises(PlayerDataValidationError):
                asyncio.run(exporter.load_espn_attribution(players=[]))

        mock_client_cls.assert_not_called()

    def test_live_fetch_enters_session_and_closes_client(self, tmp_path):
        """BLOCKING-1 (D17.4 polish): the live fetch must be wrapped in
        `async with espn_client.session():` -- proven here by asserting the
        mock client's session() context manager is entered before
        get_league_snapshot is awaited -- and close() must be called
        afterwards (SUGGESTION-2) so the wrapper does not leak a connection."""
        exporter = DataExporter(
            output_dir=str(tmp_path / 'out'),
            load_drafted_data=False,
            use_csv_ownership=False,
            espn_settings=Mock(season=2025),
        )

        # D17.5 D6: the configured ESPN_TEAM_ID (12345 here, from the patched
        # ConfigManager below) must resolve in teams[] or normalization fails
        # closed -- so this fixture now carries our own team row.
        our_team = Mock()
        our_team.id = 12345
        our_team.name = "Kai's Krew"
        snapshot = Mock()
        snapshot.draftDetail = Mock()
        snapshot.draftDetail.picks = []
        snapshot.teams = [our_team]

        mock_client = Mock()
        session_cm = AsyncMock()
        mock_client.session = Mock(return_value=session_cm)
        mock_client.get_league_snapshot = AsyncMock(return_value=snapshot)
        mock_client.close = AsyncMock()

        with patch('player_data_fetcher.espn_client.ESPNClient', return_value=mock_client), \
             patch('league_helper.util.ConfigManager.ConfigManager') as mock_cm_cls:
            mock_cm_cls.return_value.get_parameter.return_value = 12345
            asyncio.run(exporter.load_espn_attribution(players=[]))

        # session() entered (async context manager protocol) before the fetch,
        # and close() called exactly once afterwards -- the copy-pasteable
        # try/async-with/finally shape the review requires, not the wrapper
        # alone.
        session_cm.__aenter__.assert_awaited_once()
        session_cm.__aexit__.assert_awaited_once()
        mock_client.get_league_snapshot.assert_awaited_once()
        mock_client.close.assert_awaited_once()
        assert exporter._espn_attribution == {}

    def test_raises_and_closes_client_on_fail_closed_missing_playerid(self, tmp_path):
        """AC4's fail-closed half: a completed pick with no local match
        raises PlayerDataValidationError naming the offending playerId, and
        the client is still closed (finally-scoped close, not
        with-scoped)."""
        exporter = DataExporter(
            output_dir=str(tmp_path / 'out'),
            load_drafted_data=False,
            use_csv_ownership=False,
            espn_settings=Mock(season=2025),
        )

        pick = Mock(playerId=999, teamId=1)
        team = Mock(id=1, name="Team A")
        snapshot = Mock()
        snapshot.draftDetail = Mock()
        snapshot.draftDetail.picks = [pick]
        snapshot.teams = [team]

        session_cm = AsyncMock()
        mock_client = Mock()
        mock_client.session = Mock(return_value=session_cm)
        mock_client.get_league_snapshot = AsyncMock(return_value=snapshot)
        mock_client.close = AsyncMock()

        with patch('player_data_fetcher.espn_client.ESPNClient', return_value=mock_client), \
             patch('league_helper.util.ConfigManager.ConfigManager') as mock_cm_cls:
            mock_cm_cls.return_value.get_parameter.return_value = 12345
            with pytest.raises(PlayerDataValidationError, match="999"):
                asyncio.run(exporter.load_espn_attribution(players=[]))

        mock_client.close.assert_awaited_once()
        assert exporter._espn_attribution is None

# D17.5 FIXTURE HELPERS -- ESPN ownership cutover

def _cutover_pick(player_id, team_id):
    """One draftDetail.picks[] row (playerId == -1 marks a placeholder)."""
    pick = Mock()
    pick.playerId = player_id
    pick.teamId = team_id
    return pick


def _cutover_team(team_id, name):
    """One teams[] row. `name` is assigned AFTER construction -- Mock(name=...)
    sets the mock's own repr name instead of a `.name` attribute."""
    team = Mock()
    team.id = team_id
    team.name = name
    return team


def _cutover_snapshot(picks, teams):
    snapshot = Mock()
    snapshot.draftDetail = Mock()
    snapshot.draftDetail.picks = picks
    snapshot.teams = teams
    return snapshot


def _cutover_exporter(tmp_path, **kwargs):
    """A DataExporter on the default (ESPN) supplier path."""
    params = dict(output_dir=str(tmp_path / 'out'), load_drafted_data=False)
    params.update(kwargs)
    return DataExporter(**params)


class TestOurTeamNormalization:
    """D17.5 D3/D6: our configured teamId's picks are rewritten to
    Constants.FANTASY_TEAM_NAME at the DataExporter seam, keyed on teamId."""

    def test_our_picks_are_rewritten_to_the_in_app_token(self, tmp_path):
        """D3: the fixture's own ESPN team name is deliberately NOT "Sea Sharp",
        so removing the normalization makes this test fail."""
        exporter = _cutover_exporter(tmp_path)
        snapshot = _cutover_snapshot(
            [_cutover_pick(101, 7), _cutover_pick(102, 3), _cutover_pick(-1, 3)],
            [_cutover_team(7, "Kai's Krew"), _cutover_team(3, "Synthetic Team 3")],
        )

        normalized = exporter._normalize_our_team_attribution(
            snapshot, {"101": "Kai's Krew", "102": "Synthetic Team 3"}, 7
        )

        assert normalized["101"] == "Sea Sharp"

    def test_normalized_pick_satisfies_is_rostered(self, tmp_path):
        """D3: the whole point of the normalization -- the downstream
        string-equality readers must classify our picks as ours."""
        exporter = _cutover_exporter(tmp_path)
        snapshot = _cutover_snapshot(
            [_cutover_pick(101, 7), _cutover_pick(102, 3)],
            [_cutover_team(7, "Kai's Krew"), _cutover_team(3, "Synthetic Team 3")],
        )
        exporter._espn_attribution = exporter._normalize_our_team_attribution(
            snapshot, {"101": "Kai's Krew", "102": "Synthetic Team 3"}, 7
        )
        data = ProjectionData(season=2025, scoring_format="ppr", total_players=2, players=[
            ESPNPlayerData(id="101", name="Ours", team="KC", position="WR"),
            ESPNPlayerData(id="102", name="Theirs", team="SF", position="RB"),
        ])

        ours, theirs = exporter.get_fantasy_players(data)

        assert ours.is_rostered() is True
        assert ours.is_drafted_by_opponent() is False
        assert theirs.is_rostered() is False
        assert theirs.is_drafted_by_opponent() is True

    def test_other_teams_keep_their_raw_espn_names(self, tmp_path):
        """Normalization applies solely to the configured teamId."""
        exporter = _cutover_exporter(tmp_path)
        snapshot = _cutover_snapshot(
            [_cutover_pick(101, 7), _cutover_pick(102, 3)],
            [_cutover_team(7, "Kai's Krew"), _cutover_team(3, "Synthetic Team 3")],
        )

        normalized = exporter._normalize_our_team_attribution(
            snapshot, {"101": "Kai's Krew", "102": "Synthetic Team 3"}, 7
        )

        assert normalized["102"] == "Synthetic Team 3"

    def test_absent_configured_team_id_fails_closed(self, tmp_path):
        """A configured teamId with no teams[] row halts instead of leaving
        every pick opponent-attributed."""
        exporter = _cutover_exporter(tmp_path)
        snapshot = _cutover_snapshot(
            [_cutover_pick(101, 3)], [_cutover_team(3, "Synthetic Team 3")]
        )

        with pytest.raises(PlayerDataValidationError, match="ESPN_TEAM_ID 7"):
            exporter._normalize_our_team_attribution(snapshot, {"101": "Synthetic Team 3"}, 7)

    @pytest.mark.parametrize("colliding_name", ["Sea Sharp", "sea sharp", "  Sea Sharp  "])
    def test_same_name_collision_fails_closed(self, tmp_path, colliding_name):
        """D6: another team named like FANTASY_TEAM_NAME -- exactly, in a
        different case, or with surrounding whitespace -- halts rather than
        normalizing an opponent's players into our roster."""
        exporter = _cutover_exporter(tmp_path)
        snapshot = _cutover_snapshot(
            [_cutover_pick(101, 7), _cutover_pick(102, 3)],
            [_cutover_team(7, "Kai's Krew"), _cutover_team(3, colliding_name)],
        )

        with pytest.raises(PlayerDataValidationError, match=r"\[3\]"):
            exporter._normalize_our_team_attribution(
                snapshot, {"101": "Kai's Krew", "102": colliding_name}, 7
            )

    def test_collision_error_carries_no_credential_value(self, tmp_path, monkeypatch):
        """TD4: the guard's message names team ids only."""
        monkeypatch.setenv('espn_s2', 'SENTINEL_S2_VALUE')
        monkeypatch.setenv('SWID', 'SENTINEL_SWID_VALUE')
        exporter = _cutover_exporter(tmp_path)
        snapshot = _cutover_snapshot(
            [_cutover_pick(101, 7)],
            [_cutover_team(7, "Kai's Krew"), _cutover_team(3, "Sea Sharp")],
        )

        with pytest.raises(PlayerDataValidationError) as excinfo:
            exporter._normalize_our_team_attribution(snapshot, {"101": "Kai's Krew"}, 7)

        assert 'SENTINEL_S2_VALUE' not in str(excinfo.value)
        assert 'SENTINEL_SWID_VALUE' not in str(excinfo.value)


class TestZeroMatchOwnershipWarning:
    """D17.5 D4: the ESPN supplier's mirror of DraftedRosterManager's
    zero-match guard (utils/DraftedRosterManager.py:247-250)."""

    def test_warns_when_our_team_owns_none_of_the_completed_picks(self, tmp_path):
        exporter = _cutover_exporter(tmp_path)
        exporter.logger = Mock()
        snapshot = _cutover_snapshot(
            [_cutover_pick(101, 3), _cutover_pick(-1, 7)],
            [_cutover_team(7, "Kai's Krew"), _cutover_team(3, "Synthetic Team 3")],
        )

        exporter._normalize_our_team_attribution(snapshot, {"101": "Synthetic Team 3"}, 7)

        exporter.logger.warning.assert_called_once()
        assert "ESPN_TEAM_ID 7 matched zero of 1 completed picks" in \
            exporter.logger.warning.call_args[0][0]

    def test_no_warning_when_our_team_owns_a_completed_pick(self, tmp_path):
        exporter = _cutover_exporter(tmp_path)
        exporter.logger = Mock()
        snapshot = _cutover_snapshot(
            [_cutover_pick(101, 7)], [_cutover_team(7, "Kai's Krew")]
        )

        exporter._normalize_our_team_attribution(snapshot, {"101": "Kai's Krew"}, 7)

        exporter.logger.warning.assert_not_called()

    def test_warning_carries_no_credential_value(self, tmp_path, monkeypatch):
        monkeypatch.setenv('espn_s2', 'SENTINEL_S2_VALUE')
        monkeypatch.setenv('SWID', 'SENTINEL_SWID_VALUE')
        exporter = _cutover_exporter(tmp_path)
        exporter.logger = Mock()
        snapshot = _cutover_snapshot(
            [_cutover_pick(101, 3)],
            [_cutover_team(7, "Kai's Krew"), _cutover_team(3, "Synthetic Team 3")],
        )

        exporter._normalize_our_team_attribution(snapshot, {"101": "Synthetic Team 3"}, 7)

        message = exporter.logger.warning.call_args[0][0]
        assert 'SENTINEL_S2_VALUE' not in message
        assert 'SENTINEL_SWID_VALUE' not in message


def _cutover_client(snapshot):
    """A mocked D17.3 ESPNClient returning `snapshot` from the session-wrapped
    authenticated read."""
    session_cm = AsyncMock()
    client = Mock()
    client.session = Mock(return_value=session_cm)
    client.get_league_snapshot = AsyncMock(return_value=snapshot)
    client.close = AsyncMock()
    return client


def _cutover_config(league_id=12345, team_id=7):
    """A ConfigManager patch whose get_parameter answers per key."""
    def _get_parameter(key, default=None):
        return {'ESPN_LEAGUE_ID': str(league_id), 'ESPN_TEAM_ID': team_id}.get(key, default)
    config_manager = Mock()
    config_manager.get_parameter = Mock(side_effect=_get_parameter)
    return config_manager


class TestLoadEspnAttributionAppliesNormalization:
    """D17.5 D6: the normalization runs INSIDE load_espn_attribution, on
    reconcile_espn_attribution's output, before anything is stored."""

    def test_stored_map_is_normalized(self, tmp_path):
        exporter = _cutover_exporter(tmp_path, espn_settings=Mock(season=2025))
        snapshot = _cutover_snapshot(
            [_cutover_pick(101, 7), _cutover_pick(102, 3)],
            [_cutover_team(7, "Kai's Krew"), _cutover_team(3, "Synthetic Team 3")],
        )
        players = [
            ESPNPlayerData(id="101", name="Ours", team="KC", position="WR"),
            ESPNPlayerData(id="102", name="Theirs", team="SF", position="RB"),
        ]

        with patch('player_data_fetcher.espn_client.ESPNClient', return_value=_cutover_client(snapshot)), \
             patch('league_helper.util.ConfigManager.ConfigManager', return_value=_cutover_config()):
            asyncio.run(exporter.load_espn_attribution(players=players))

        assert exporter._espn_attribution == {"101": "Sea Sharp", "102": "Synthetic Team 3"}

    def test_guard_failure_stores_nothing_and_mutates_no_player(self, tmp_path):
        """TD2 atomicity: a failure raised AFTER a fully successful
        reconciliation still leaves ownership state entirely untouched."""
        exporter = _cutover_exporter(tmp_path, espn_settings=Mock(season=2025))
        snapshot = _cutover_snapshot(
            [_cutover_pick(101, 7), _cutover_pick(102, 3)],
            [_cutover_team(7, "Kai's Krew"), _cutover_team(3, "Sea Sharp")],
        )
        players = [
            ESPNPlayerData(id="101", name="Ours", team="KC", position="WR"),
            ESPNPlayerData(id="102", name="Theirs", team="SF", position="RB"),
        ]
        before = [player.drafted_by for player in players]

        with patch('player_data_fetcher.espn_client.ESPNClient', return_value=_cutover_client(snapshot)), \
             patch('league_helper.util.ConfigManager.ConfigManager', return_value=_cutover_config()):
            with pytest.raises(PlayerDataValidationError):
                asyncio.run(exporter.load_espn_attribution(players=players))

        assert [player.drafted_by for player in players] == before
        assert exporter._espn_attribution is None

        data = ProjectionData(season=2025, scoring_format="ppr", total_players=2, players=players)
        with pytest.raises(PlayerDataValidationError):
            exporter.get_fantasy_players(data)

    def test_auth_failure_propagates_loudly_and_redacted(self, tmp_path, monkeypatch):
        """An ESPNAPIError from the authenticated read is neither swallowed nor
        downgraded to a silent unowned board, and nothing on this path adds a
        credential value to it."""
        from player_data_fetcher.espn_client import ESPNAPIError

        monkeypatch.setenv('espn_s2', 'SENTINEL_S2_VALUE')
        monkeypatch.setenv('SWID', 'SENTINEL_SWID_VALUE')
        exporter = _cutover_exporter(tmp_path, espn_settings=Mock(season=2025))
        players = [ESPNPlayerData(id="101", name="Ours", team="KC", position="WR")]
        client = _cutover_client(Mock())
        client.get_league_snapshot = AsyncMock(
            side_effect=ESPNAPIError("ESPN league read failed: HTTP 401 (credentials redacted)")
        )

        with patch('player_data_fetcher.espn_client.ESPNClient', return_value=client), \
             patch('league_helper.util.ConfigManager.ConfigManager', return_value=_cutover_config()):
            with pytest.raises(ESPNAPIError) as excinfo:
                asyncio.run(exporter.load_espn_attribution(players=players))

        assert 'SENTINEL_S2_VALUE' not in str(excinfo.value)
        assert 'SENTINEL_SWID_VALUE' not in str(excinfo.value)
        assert exporter._espn_attribution is None
        assert players[0].drafted_by == ""
        client.close.assert_awaited_once()


class TestSupplierSelection:
    """D17.5 D1/D2 composition: the flag selects WHICH SUPPLIER RUNS -- it does
    not merely decide which of two equal outputs is returned.

    Every test here wires BOTH suppliers with DELIBERATELY DIFFERENT values for
    the same player, so the resulting `drafted_by` names the branch that
    produced it. TestSupplierParity below asserts the two agree when both are
    correctly wired, which is exactly why parity alone cannot catch a default
    pointing at the wrong branch -- these tests can.
    """

    def _projection_data(self):
        return ProjectionData(season=2025, scoring_format="ppr", total_players=1, players=[
            ESPNPlayerData(id="101", name="Alpha Runner", team="KC", position="RB"),
        ])

    def _csv_naming_a_different_owner(self, tmp_path):
        csv_path = tmp_path / 'drafted_data.csv'
        csv_path.write_text("Alpha Runner RB - KC,CSV Owner\n", encoding='utf-8')
        return csv_path

    def test_default_path_applies_espn_and_never_invokes_the_csv_applier(self, tmp_path):
        """D17.5 D1/D2: with no flag supplied, the ESPN attribution is what
        lands -- proven on the MECHANISM (the CSV applier is never called) as
        well as on the value, because a value-only assertion cannot distinguish
        the two suppliers once both are wired."""
        exporter = DataExporter(
            output_dir=str(tmp_path / 'out'),
            drafted_data_path=str(self._csv_naming_a_different_owner(tmp_path)),
        )

        # D2 first: on the default path the legacy owner is not constructed.
        assert exporter.drafted_roster_manager is None

        # Now simulate the regression D2 exists to prevent -- a CSV owner back
        # in the object graph -- and prove get_fantasy_players still does not
        # route through it.
        intruder = Mock()
        exporter.drafted_roster_manager = intruder
        exporter._espn_attribution = {"101": "ESPN Owner"}

        players = exporter.get_fantasy_players(self._projection_data())

        assert players[0].drafted_by == "ESPN Owner"
        intruder.apply_drafted_state_to_players.assert_not_called()

    def test_rollback_path_applies_csv_even_when_espn_attribution_is_present(self, tmp_path):
        """D17.5 D1: with --use-csv-ownership the CSV supplier wins even though
        a fully-populated ESPN map is sitting on the exporter -- so the test
        cannot pass by reading the wrong source and getting a lucky match."""
        exporter = DataExporter(
            output_dir=str(tmp_path / 'out'),
            drafted_data_path=str(self._csv_naming_a_different_owner(tmp_path)),
            use_csv_ownership=True,
        )
        assert exporter.drafted_roster_manager is not None
        apply_spy = Mock(wraps=exporter.drafted_roster_manager.apply_drafted_state_to_players)
        exporter.drafted_roster_manager.apply_drafted_state_to_players = apply_spy
        exporter._espn_attribution = {"101": "ESPN Owner"}

        players = exporter.get_fantasy_players(self._projection_data())

        assert players[0].drafted_by == "CSV Owner"
        apply_spy.assert_called_once()

    def test_exported_json_carries_the_default_supplier_ownership(self, tmp_path):
        """The branch selection survives all the way into the written file, not
        just the in-memory list: the exported JSON carries the ESPN owner while
        a CSV naming a different owner sits on disk beside it."""
        exporter = DataExporter(
            output_dir=str(tmp_path / 'out'),
            position_json_output=str(tmp_path / 'json'),
            team_data_folder=str(tmp_path / 'team'),
            drafted_data_path=str(self._csv_naming_a_different_owner(tmp_path)),
        )
        exporter._espn_attribution = {"101": "ESPN Owner"}

        asyncio.run(exporter.export_position_json_files(self._projection_data()))

        rb_json = json.loads((tmp_path / 'json' / 'rb_data.json').read_text())
        assert [player['drafted_by'] for player in rb_json['rb_data']] == ["ESPN Owner"]


class TestSupplierParity:
    """D17.5: the rollback path still works, and both suppliers produce the same
    exported JSON for the same ownership facts."""

    POOL = [
        ("4429795", "Alpha Runner", "KC", "RB"),
        ("4430807", "Bravo Runner", "SF", "RB"),
        ("4426515", "Charlie Catcher", "MIN", "WR"),
        ("900001", "Delta Undrafted", "BUF", "WR"),
    ]

    def _projection_data(self):
        return ProjectionData(
            season=2025, scoring_format="ppr", total_players=len(self.POOL),
            players=[ESPNPlayerData(id=i, name=n, team=t, position=p) for i, n, t, p in self.POOL],
        )

    def _drafted_csv(self, tmp_path):
        csv_path = tmp_path / 'drafted_data.csv'
        csv_path.write_text(
            "Alpha Runner RB - KC,Sea Sharp\n"
            "Bravo Runner RB - SF,Synthetic Team 2\n"
            "Charlie Catcher WR - MIN,Synthetic Team 3\n",
            encoding='utf-8',
        )
        return csv_path

    def test_rollback_flag_reproduces_csv_ownership(self, tmp_path):
        """--use-csv-ownership still applies the legacy CSV/fuzzy path -- and
        does so BY INVOKING IT, not by coincidentally producing equal output."""
        exporter = DataExporter(
            output_dir=str(tmp_path / 'out'),
            drafted_data_path=str(self._drafted_csv(tmp_path)),
            use_csv_ownership=True,
        )

        # Invocation, not just output: the legacy owner must exist on this path
        # and must be the thing that ran.
        assert exporter.drafted_roster_manager is not None
        apply_spy = Mock(wraps=exporter.drafted_roster_manager.apply_drafted_state_to_players)
        exporter.drafted_roster_manager.apply_drafted_state_to_players = apply_spy

        players = exporter.get_fantasy_players(self._projection_data())

        assert [p.drafted_by for p in players] == [
            "Sea Sharp", "Synthetic Team 2", "Synthetic Team 3", ""
        ]
        apply_spy.assert_called_once()

    def test_exported_json_is_identical_under_both_suppliers(self, tmp_path):
        """Downstream output parity on a sanitized completed-pick snapshot: the
        ESPN default and the CSV rollback produce byte-equal position JSON."""
        data = self._projection_data()

        csv_exporter = DataExporter(
            output_dir=str(tmp_path / 'csv_out_dir'),
            position_json_output=str(tmp_path / 'csv_json'),
            team_data_folder=str(tmp_path / 'csv_team'),
            drafted_data_path=str(self._drafted_csv(tmp_path)),
            use_csv_ownership=True,
        )

        snapshot = _cutover_snapshot(
            [_cutover_pick(4429795, 7), _cutover_pick(4430807, 2), _cutover_pick(4426515, 3),
             _cutover_pick(-1, 3)],
            [_cutover_team(7, "Kai's Krew"), _cutover_team(2, "Synthetic Team 2"),
             _cutover_team(3, "Synthetic Team 3")],
        )
        espn_exporter = _cutover_exporter(
            tmp_path,
            output_dir=str(tmp_path / 'espn_out_dir'),
            position_json_output=str(tmp_path / 'espn_json'),
            team_data_folder=str(tmp_path / 'espn_team'),
        )
        espn_exporter._espn_attribution = espn_exporter._normalize_our_team_attribution(
            snapshot,
            {"4429795": "Kai's Krew", "4430807": "Synthetic Team 2", "4426515": "Synthetic Team 3"},
            7,
        )

        asyncio.run(csv_exporter.export_position_json_files(data))
        asyncio.run(espn_exporter.export_position_json_files(data))

        drafted_by_values = set()
        for position in ['qb', 'rb', 'wr', 'te', 'k', 'dst']:
            csv_json = json.loads((tmp_path / 'csv_json' / f'{position}_data.json').read_text())
            espn_json = json.loads((tmp_path / 'espn_json' / f'{position}_data.json').read_text())
            assert csv_json == espn_json
            drafted_by_values.update(
                player['drafted_by'] for player in csv_json[f'{position}_data']
            )

        # Non-vacuity: the two outputs agree on REAL ownership, not on an
        # entirely undrafted board.
        assert "Sea Sharp" in drafted_by_values
        assert "Synthetic Team 2" in drafted_by_values


class TestPreDraftZeroCompletedPicks:
    """D17.5 / ticket TD2: the PRE-DRAFT state -- `picks[]` fully pre-allocated
    with every row still `playerId == -1`.

    This is not an edge case for this ticket, it is the NORMAL state every time
    the fetcher runs before or at the start of draft night, so the cutover must
    be quiet and non-fatal here. Three distinct ways it could go wrong, one test
    each: raising, warning spuriously, or mistaking "the draft has not started"
    for "attribution was never loaded".
    """

    def _pre_draft_snapshot(self):
        """160 pre-allocated placeholder rows and a fully populated teams[] --
        the shape spike F11a records for a league whose draft has not begun."""
        picks = [_cutover_pick(-1, (i % 3) + 1) for i in range(160)]
        teams = [
            _cutover_team(7, "Kai's Krew"),
            _cutover_team(2, "Synthetic Team 2"),
            _cutover_team(3, "Synthetic Team 3"),
        ]
        return _cutover_snapshot(picks, teams)

    def _local_pool(self):
        return [
            ESPNPlayerData(id="101", name="Alpha Runner", team="KC", position="RB"),
            ESPNPlayerData(id="102", name="Charlie Catcher", team="MIN", position="WR"),
        ]

    def test_load_stores_an_empty_map_and_warns_nothing(self, tmp_path):
        """The full load path completes on a pre-draft snapshot: an EMPTY map is
        stored (not None, not a raise), and D4's zero-match warning stays silent
        because `completed_picks` is zero -- warning on a draft that has not
        started would cry wolf on every pre-draft run."""
        exporter = _cutover_exporter(tmp_path, espn_settings=Mock(season=2025))
        exporter.logger = Mock()
        players = self._local_pool()

        with patch('player_data_fetcher.espn_client.ESPNClient', return_value=_cutover_client(self._pre_draft_snapshot())), \
             patch('league_helper.util.ConfigManager.ConfigManager', return_value=_cutover_config()):
            asyncio.run(exporter.load_espn_attribution(players=players))

        assert exporter._espn_attribution == {}
        assert exporter._espn_attribution is not None
        exporter.logger.warning.assert_not_called()

    def test_pre_draft_state_leaves_every_player_a_free_agent(self, tmp_path):
        """get_fantasy_players over a loaded-but-empty attribution returns an
        entirely undrafted board rather than raising."""
        exporter = _cutover_exporter(tmp_path)
        exporter._espn_attribution = {}
        data = ProjectionData(
            season=2025, scoring_format="ppr", total_players=2, players=self._local_pool(),
        )

        fantasy_players = exporter.get_fantasy_players(data)

        assert [player.drafted_by for player in fantasy_players] == ["", ""]
        assert all(player.is_free_agent() for player in fantasy_players)
        assert not any(player.is_rostered() for player in fantasy_players)

    def test_loaded_but_empty_is_distinguished_from_never_loaded(self, tmp_path):
        """The fail-closed guard must test `is None`, NOT truthiness.

        An empty dict is falsy, so `if not self._espn_attribution:` would raise
        on every pre-draft run while passing every other test in this file --
        the tool would fail exactly when it is first used on draft night. This
        test pins both sides of that distinction.
        """
        exporter = _cutover_exporter(tmp_path)
        data = ProjectionData(
            season=2025, scoring_format="ppr", total_players=2, players=self._local_pool(),
        )

        # loaded-but-empty (pre-draft): must NOT raise
        exporter._espn_attribution = {}
        exporter.get_fantasy_players(data)

        # never loaded: must still raise
        exporter._espn_attribution = None
        with pytest.raises(PlayerDataValidationError):
            exporter.get_fantasy_players(data)
