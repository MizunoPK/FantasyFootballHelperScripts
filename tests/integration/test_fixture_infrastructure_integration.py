"""
Integration Tests for F1: fixture_directory_and_helpers (KAI-15)

Tests verify the fixture directory structure, helpers.py utilities,
pytest live_api marker infrastructure, and run_all_tests.py changes.
"""
import pytest
import json
from pathlib import Path

import pandas as pd

project_root = Path(__file__).parent.parent.parent


class TestDirectoryStructure:
    """R1: Verify tests/fixtures/ subdirectory structure exists as specified."""

    def test_fixture_subdirectories_exist(self):
        """Verify all four required fixture subdirectories are present."""
        fixtures_dir = project_root / "tests" / "fixtures"
        assert (fixtures_dir / "espn_api").is_dir()
        assert (fixtures_dir / "historical").is_dir()
        assert (fixtures_dir / "player_data").is_dir()
        assert (fixtures_dir / "league").is_dir()

    def test_init_files_exist(self):
        """Verify __init__.py files exist in fixtures root and all subdirectories."""
        fixtures_dir = project_root / "tests" / "fixtures"
        assert (fixtures_dir / "__init__.py").exists()
        assert (fixtures_dir / "espn_api" / "__init__.py").exists()
        assert (fixtures_dir / "historical" / "__init__.py").exists()
        assert (fixtures_dir / "player_data" / "__init__.py").exists()
        assert (fixtures_dir / "league" / "__init__.py").exists()


class TestHelpersFunctions:
    """R5: Verify helpers.py path builders, fixture loaders, and assertion utilities."""

    def test_get_fixture_path_returns_correct_path(self):
        """Verify get_fixture_path returns FIXTURES_ROOT / fixture_type / filename."""
        from tests.fixtures.helpers import get_fixture_path, FIXTURES_ROOT
        result = get_fixture_path("espn_api", "test.json")
        assert result == FIXTURES_ROOT / "espn_api" / "test.json"

    def test_load_json_fixture_raises_on_missing_file(self):
        """Verify load_json_fixture raises FileNotFoundError with descriptive message."""
        from tests.fixtures.helpers import load_json_fixture
        with pytest.raises(FileNotFoundError) as exc_info:
            load_json_fixture("espn_api", "nonexistent_fixture_xyz.json")
        assert "Fixture file not found" in str(exc_info.value)
        assert "fixture directory" in str(exc_info.value)

    def test_load_json_fixture_returns_dict_for_valid_file(self):
        """Verify load_json_fixture returns parsed dict when fixture file exists."""
        from tests.fixtures.helpers import load_json_fixture, get_fixture_path
        fixture_path = get_fixture_path("espn_api", "_test_temp_fixture.json")
        try:
            fixture_path.write_text(json.dumps({"key": "value", "num": 42}))
            result = load_json_fixture("espn_api", "_test_temp_fixture.json")
            assert isinstance(result, dict)
            assert result["key"] == "value"
        finally:
            fixture_path.unlink(missing_ok=True)

    def test_assert_dataframe_output_raises_on_row_count_violation(self):
        """Verify assert_dataframe_output raises AssertionError when row count < min_rows."""
        from tests.fixtures.helpers import assert_dataframe_output
        df = pd.DataFrame({"col": [1, 2, 3]})
        with pytest.raises(AssertionError) as exc_info:
            assert_dataframe_output(df, min_rows=10, required_columns=[], non_null_columns=[])
        assert "3 rows" in str(exc_info.value)
        assert "10" in str(exc_info.value)

    def test_assert_dataframe_output_raises_on_missing_column(self):
        """Verify assert_dataframe_output raises AssertionError listing present columns."""
        from tests.fixtures.helpers import assert_dataframe_output
        df = pd.DataFrame({"col_a": [1, 2, 3]})
        with pytest.raises(AssertionError) as exc_info:
            assert_dataframe_output(df, min_rows=1, required_columns=["missing_col"], non_null_columns=[])
        assert "missing_col" in str(exc_info.value)
        assert "col_a" in str(exc_info.value)

    def test_assert_dataframe_output_raises_on_nan_in_non_null_column(self):
        """Verify assert_dataframe_output raises AssertionError reporting NaN count."""
        from tests.fixtures.helpers import assert_dataframe_output
        df = pd.DataFrame({"name": ["Alice", None, "Bob"]})
        with pytest.raises(AssertionError) as exc_info:
            assert_dataframe_output(df, min_rows=1, required_columns=[], non_null_columns=["name"])
        assert "name" in str(exc_info.value)
        assert "NaN" in str(exc_info.value)

    def test_assert_dataframe_output_passes_for_valid_dataframe(self):
        """Verify assert_dataframe_output does not raise for a fully valid DataFrame."""
        from tests.fixtures.helpers import assert_dataframe_output
        df = pd.DataFrame({"name": ["Alice", "Bob"], "score": [10, 20]})
        assert_dataframe_output(df, min_rows=1, required_columns=["name", "score"], non_null_columns=["name"])


class TestPytestMarkerInfrastructure:
    """R2 + R3: Verify live_api marker registration and test_schedule_fetcher_integration.py marking."""

    def test_pytest_ini_exists_with_live_api_marker(self):
        """Verify pytest.ini exists at project root and registers the live_api marker."""
        pytest_ini = project_root / "pytest.ini"
        assert pytest_ini.exists()
        content = pytest_ini.read_text()
        assert "live_api" in content

    def test_schedule_fetcher_integration_has_pytestmark(self):
        """Verify test_schedule_fetcher_integration.py has module-level pytestmark."""
        test_file = project_root / "tests" / "integration" / "test_schedule_fetcher_integration.py"
        content = test_file.read_text()
        assert "pytestmark = pytest.mark.live_api" in content


class TestRunAllTestsChanges:
    """R4: Verify run_all_tests.py excludes live_api tests and handles exit code 5."""

    def test_run_all_tests_has_marker_exclusion(self):
        """Verify run_all_tests.py passes -m not live_api to pytest commands."""
        run_all_tests = project_root / "tests" / "run_all_tests.py"
        content = run_all_tests.read_text()
        assert "-m" in content
        assert "not live_api" in content

    def test_run_all_tests_has_exit_code_5_handling(self):
        """Verify run_all_tests.py treats exit code 5 (no tests collected) as success."""
        run_all_tests = project_root / "tests" / "run_all_tests.py"
        content = run_all_tests.read_text()
        assert "returncode in [0, 5]" in content


