import pytest
import json
from pathlib import Path

import pandas as pd

project_root = Path(__file__).parent.parent.parent


class TestDirectoryStructure:

    def test_fixture_subdirectories_exist(self):
        fixtures_dir = project_root / "tests" / "fixtures"
        assert (fixtures_dir / "espn_api").is_dir()
        assert (fixtures_dir / "historical").is_dir()
        assert (fixtures_dir / "player_data").is_dir()
        assert (fixtures_dir / "league").is_dir()

    def test_init_files_exist(self):
        fixtures_dir = project_root / "tests" / "fixtures"
        assert (fixtures_dir / "__init__.py").exists()
        assert (fixtures_dir / "espn_api" / "__init__.py").exists()
        assert (fixtures_dir / "historical" / "__init__.py").exists()
        assert (fixtures_dir / "player_data" / "__init__.py").exists()
        assert (fixtures_dir / "league" / "__init__.py").exists()


class TestHelpersFunctions:

    def test_get_fixture_path_returns_correct_path(self):
        from tests.fixtures.helpers import get_fixture_path, FIXTURES_ROOT
        result = get_fixture_path("espn_api", "test.json")
        assert result == FIXTURES_ROOT / "espn_api" / "test.json"

    def test_load_json_fixture_raises_on_missing_file(self):
        from tests.fixtures.helpers import load_json_fixture
        with pytest.raises(FileNotFoundError) as exc_info:
            load_json_fixture("espn_api", "nonexistent_fixture_xyz.json")
        assert "Fixture file not found" in str(exc_info.value)
        assert "F3" in str(exc_info.value)

    def test_load_json_fixture_returns_dict_for_valid_file(self):
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
        from tests.fixtures.helpers import assert_dataframe_output
        df = pd.DataFrame({"col": [1, 2, 3]})
        with pytest.raises(AssertionError) as exc_info:
            assert_dataframe_output(df, min_rows=10, required_columns=[], non_null_columns=[])
        assert "3 rows" in str(exc_info.value)
        assert "10" in str(exc_info.value)

    def test_assert_dataframe_output_raises_on_missing_column(self):
        from tests.fixtures.helpers import assert_dataframe_output
        df = pd.DataFrame({"col_a": [1, 2, 3]})
        with pytest.raises(AssertionError) as exc_info:
            assert_dataframe_output(df, min_rows=1, required_columns=["missing_col"], non_null_columns=[])
        assert "missing_col" in str(exc_info.value)
        assert "col_a" in str(exc_info.value)

    def test_assert_dataframe_output_raises_on_nan_in_non_null_column(self):
        from tests.fixtures.helpers import assert_dataframe_output
        df = pd.DataFrame({"name": ["Alice", None, "Bob"]})
        with pytest.raises(AssertionError) as exc_info:
            assert_dataframe_output(df, min_rows=1, required_columns=[], non_null_columns=["name"])
        assert "name" in str(exc_info.value)
        assert "NaN" in str(exc_info.value)

    def test_assert_dataframe_output_passes_for_valid_dataframe(self):
        from tests.fixtures.helpers import assert_dataframe_output
        df = pd.DataFrame({"name": ["Alice", "Bob"], "score": [10, 20]})
        assert_dataframe_output(df, min_rows=1, required_columns=["name", "score"], non_null_columns=["name"])


class TestPytestMarkerInfrastructure:

    def test_pytest_ini_exists_with_live_api_marker(self):
        pytest_ini = project_root / "pytest.ini"
        assert pytest_ini.exists()
        content = pytest_ini.read_text()
        assert "live_api" in content

    def test_schedule_fetcher_integration_has_pytestmark(self):
        test_file = project_root / "tests" / "integration" / "test_schedule_fetcher_integration.py"
        content = test_file.read_text()
        assert "pytestmark = pytest.mark.live_api" in content


class TestRunAllTestsChanges:

    def test_run_all_tests_has_marker_exclusion(self):
        run_all_tests = project_root / "tests" / "run_all_tests.py"
        content = run_all_tests.read_text()
        assert "-m" in content
        assert "not live_api" in content

    def test_run_all_tests_has_exit_code_5_handling(self):
        run_all_tests = project_root / "tests" / "run_all_tests.py"
        content = run_all_tests.read_text()
        assert "returncode in [0, 5]" in content
