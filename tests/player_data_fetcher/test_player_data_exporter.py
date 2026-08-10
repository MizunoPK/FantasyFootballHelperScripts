#!/usr/bin/env python3
"""
Tests for Player Data Exporter Module

Basic smoke tests for data export functionality.

Author: Kai Mizuno
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from pathlib import Path

from player_data_fetcher.player_data_exporter import DataExporter
from player_data_fetcher.player_data_models import ProjectionData, PlayerProjection


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
        exporter = DataExporter(output_dir=str(tmp_path))

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
        exporter = DataExporter(output_dir=str(tmp_path))

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
        exporter = DataExporter(output_dir=str(tmp_path / 'out'))
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

