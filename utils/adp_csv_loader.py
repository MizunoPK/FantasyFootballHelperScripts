"""
ADP CSV Loader Module

Purpose: Load and validate ADP (Average Draft Position) data from FantasyPros CSV file.
This module provides functionality to parse FantasyPros consensus ADP rankings and
prepare them for player matching and data updates.

Author: Claude Code (Epic: fix_2025_adp, Feature 1)
Created: 2025-12-31
"""

from pathlib import Path
from typing import Union
import pandas as pd

from utils.csv_utils import read_csv_with_validation
from utils.LoggingManager import get_logger
from utils.error_handler import DataProcessingError

logger = get_logger()


def load_adp_from_csv(csv_path: Union[str, Path]) -> pd.DataFrame:
    """
    Load ADP data from FantasyPros CSV file.

    Reads FantasyPros consensus ADP rankings CSV, validates data integrity,
    cleans position fields, and returns a structured DataFrame ready for
    player matching.

    Args:
        csv_path (Union[str, Path]): Path to FantasyPros CSV file

    Returns:
        pd.DataFrame: DataFrame with columns:
            - player_name (str): Player name from CSV
            - adp (float): Consensus ADP value (positive float)
            - position (str): Clean position (QB, RB, WR, TE, K, DST)

    Raises:
        FileNotFoundError: If CSV file doesn't exist at specified path
        DataProcessingError: If required columns missing or data validation fails

    Example:
        >>> from pathlib import Path
        >>> csv_path = Path('feature-updates/FantasyPros_2025_Overall_ADP_Rankings.csv')
        >>> adp_df = load_adp_from_csv(csv_path)
        >>> print(f"Loaded {len(adp_df)} players")
        Loaded 988 players
    """
    csv_path = Path(csv_path)

    if not csv_path.exists():
        logger.error(f"CSV file not found: {csv_path}")
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    required_columns = ['Player', 'POS', 'AVG']

    try:
        df = pd.read_csv(csv_path, encoding='utf-8', on_bad_lines='skip')
        logger.info(f"CSV loaded: {csv_path} ({len(df)} rows)")
    except Exception as e:
        logger.error(f"Error reading CSV: {e}")
        raise DataProcessingError(f"Error reading CSV: {e}")

    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        logger.error(f"Missing required columns: {missing_cols}")
        raise DataProcessingError(f"Missing required columns: {missing_cols}")
    logger.info(f"CSV validation passed: {csv_path}")

    df = df[['Player', 'POS', 'AVG']].copy()

    df['position'] = df['POS'].str.replace(r'\d+$', '', regex=True)

    df['adp'] = df['AVG'].astype(float)

    df = df.rename(columns={'Player': 'player_name'})

    df = df[['player_name', 'adp', 'position']]

    before_count = len(df)
    df = df[df['player_name'].notna() & (df['player_name'].str.len() > 0)]
    after_count = len(df)

    if before_count > after_count:
        logger.warning(f"Filtered out {before_count - after_count} rows with empty player names")
    logger.info(f"Validated {len(df)} player names")

    if not (df['adp'] > 0).all():
        invalid_adps = df[df['adp'] <= 0]
        logger.error(f"Invalid ADP values found: {invalid_adps['adp'].tolist()}")
        raise DataProcessingError(f"Invalid ADP values found: ADP must be > 0")
    logger.info(f"Validated {len(df)} ADP values (all > 0)")

    logger.info(f"Successfully loaded {len(df)} ADP rankings from CSV")
    return df


