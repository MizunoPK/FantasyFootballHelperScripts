from pathlib import Path
import json
import pandas as pd

FIXTURES_ROOT = Path(__file__).parent


def get_fixture_path(fixture_type: str, filename: str) -> Path:
    """Return the absolute path to a fixture file.

    Args:
        fixture_type: Subdirectory name ('espn_api', 'historical', 'player_data', 'league')
        filename: Fixture filename (e.g., 'schedule_2024.json')

    Returns:
        Absolute Path to the fixture file
    """
    return FIXTURES_ROOT / fixture_type / filename


def load_json_fixture(fixture_type: str, filename: str) -> dict:
    """Load and parse a JSON fixture file.

    Args:
        fixture_type: Subdirectory name
        filename: Fixture filename

    Returns:
        Parsed JSON as dict

    Raises:
        FileNotFoundError: If fixture file does not exist, with descriptive message
    """
    path = get_fixture_path(fixture_type, filename)
    if not path.exists():
        raise FileNotFoundError(
            f"Fixture file not found: {path}. Run the fixture recording mechanism (F3) to populate it."
        )
    with open(path) as f:
        return json.load(f)


def assert_dataframe_output(
    df: "pd.DataFrame",
    min_rows: int,
    required_columns: list[str],
    non_null_columns: list[str],
) -> None:
    """Assert that a DataFrame output meets minimum validity criteria.

    Args:
        df: DataFrame to validate
        min_rows: Minimum expected row count
        required_columns: Columns that must be present
        non_null_columns: Columns that must have no NaN values

    Raises:
        AssertionError: With descriptive message if any check fails
    """
    if len(df) < min_rows:
        raise AssertionError(
            f"DataFrame has {len(df)} rows, expected at least {min_rows}"
        )
    for col in required_columns:
        if col not in df.columns:
            raise AssertionError(
                f"Required column '{col}' not found in DataFrame. "
                f"Columns present: {list(df.columns)}"
            )
    for col in non_null_columns:
        nan_count = df[col].isna().sum()
        if nan_count > 0:
            raise AssertionError(
                f"Column '{col}' contains {nan_count} NaN values (expected none)"
            )
