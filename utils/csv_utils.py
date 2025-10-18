#!/usr/bin/env python3
"""
CSV Utilities Module

Provides common CSV operations used across multiple modules in the fantasy football system.
Consolidates repetitive CSV reading/writing patterns and standardizes error handling.

Author: Kai Mizuno
"""

import csv
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any, Optional, Union
import logging
import asyncio

from utils.error_handler import (
    create_component_error_handler, FileOperationError, DataProcessingError,
    handle_errors, error_context
)

logger = logging.getLogger(__name__)

# Create error handler for this module
error_handler = create_component_error_handler("csv_utils")


def validate_csv_columns(filepath: Union[str, Path], required_columns: List[str]) -> bool:
    """
    Validate that a CSV file contains all required columns.

    Args:
        filepath: Path to the CSV file
        required_columns: List of column names that must be present

    Returns:
        bool: True if all required columns are present, False otherwise

    Raises:
        FileOperationError: If the CSV file doesn't exist
        DataProcessingError: If required columns are missing
    """
    filepath = Path(filepath)

    # error_context provides structured error logging with file path tracking
    with error_context("validate_csv_columns", component="csv_utils",
                      file_path=str(filepath)) as context:

        # Early exit if file doesn't exist (fail fast pattern)
        if not filepath.exists():
            raise FileOperationError(
                f"CSV file not found: {filepath}",
                context=context
            )

        try:
            with open(filepath, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                # Use set for O(1) lookup when checking required columns
                existing_columns = set(reader.fieldnames or [])
                # Build list of missing columns for error reporting
                missing_columns = [col for col in required_columns if col not in existing_columns]

                if missing_columns:
                    raise DataProcessingError(
                        f"Missing required columns: {missing_columns}",
                        context=context
                    )

                return True

        except (OSError, UnicodeDecodeError) as e:
            raise FileOperationError(
                f"Error reading CSV file {filepath}: {e}",
                context=context,
                original_exception=e
            )


def read_csv_with_validation(filepath: Union[str, Path],
                           required_columns: Optional[List[str]] = None,
                           encoding: str = 'utf-8') -> pd.DataFrame:
    """
    Read CSV file with optional column validation and standardized error handling.

    Args:
        filepath: Path to the CSV file
        required_columns: Optional list of required column names
        encoding: File encoding (default: utf-8)

    Returns:
        pd.DataFrame: Loaded DataFrame

    Raises:
        FileNotFoundError: If the CSV file doesn't exist
        ValueError: If required columns are missing
    """
    filepath = Path(filepath)

    if not filepath.exists():
        raise FileNotFoundError(f"CSV file not found: {filepath}")

    try:
        # Validate columns if required
        if required_columns:
            validate_csv_columns(filepath, required_columns)

        # Read CSV with pandas
        df = pd.read_csv(filepath, encoding=encoding)
        logger.info(f"Successfully loaded {len(df)} rows from {filepath}")

        return df

    except Exception as e:
        logger.error(f"Error reading CSV file {filepath}: {e}")
        raise


def write_csv_with_backup(df: pd.DataFrame,
                         filepath: Union[str, Path],
                         create_backup: bool = True,
                         encoding: str = 'utf-8') -> None:
    """
    Write DataFrame to CSV with optional backup of existing file.

    Args:
        df: DataFrame to write
        filepath: Destination file path
        create_backup: Whether to create backup of existing file
        encoding: File encoding (default: utf-8)
    """
    filepath = Path(filepath)

    try:
        # Skip backup for temporary files (common in tests)
        # This prevents pytest tmp_path from accumulating backups during test runs
        is_temp_file = 'tmp' in str(filepath) or 'temp' in str(filepath).lower()

        # Create backup if file exists and backup is requested and not a temp file
        # Backup strategy: rename original to .backup extension, then write new file
        if create_backup and filepath.exists() and not is_temp_file:
            backup_path = filepath.with_suffix(f'.backup{filepath.suffix}')
            # Remove existing backup if it exists (keep only one backup level)
            # This prevents unlimited backup accumulation
            if backup_path.exists():
                backup_path.unlink()
            # Use rename instead of copy for atomic operation
            filepath.rename(backup_path)
            logger.info(f"Created backup: {backup_path}")

        # Ensure directory exists
        filepath.parent.mkdir(parents=True, exist_ok=True)

        # Write CSV
        df.to_csv(filepath, index=False, encoding=encoding)
        logger.info(f"Successfully wrote {len(df)} rows to {filepath}")

    except Exception as e:
        logger.error(f"Error writing CSV file {filepath}: {e}")
        raise


async def write_csv_async(df: pd.DataFrame,
                         filepath: Union[str, Path],
                         encoding: str = 'utf-8') -> None:
    """
    Write DataFrame to CSV asynchronously using thread pool.

    Args:
        df: DataFrame to write
        filepath: Destination file path
        encoding: File encoding (default: utf-8)
    """
    filepath = Path(filepath)

    try:
        # Ensure directory exists
        filepath.parent.mkdir(parents=True, exist_ok=True)

        # Write CSV asynchronously using thread pool
        # run_in_executor with None uses default ThreadPoolExecutor
        # This prevents blocking the event loop during I/O operations
        await asyncio.get_event_loop().run_in_executor(
            None, lambda: df.to_csv(str(filepath), index=False, encoding=encoding)
        )

        logger.info(f"Successfully wrote {len(df)} rows to {filepath} (async)")

    except Exception as e:
        logger.error(f"Error writing CSV file {filepath} (async): {e}")
        raise


def read_dict_csv(filepath: Union[str, Path],
                 required_columns: Optional[List[str]] = None,
                 encoding: str = 'utf-8') -> List[Dict[str, Any]]:
    """
    Read CSV file and return as list of dictionaries.

    Args:
        filepath: Path to the CSV file
        required_columns: Optional list of required column names
        encoding: File encoding (default: utf-8)

    Returns:
        List[Dict[str, Any]]: List of row dictionaries
    """
    filepath = Path(filepath)

    if not filepath.exists():
        raise FileNotFoundError(f"CSV file not found: {filepath}")

    try:
        # Validate columns if required
        # This happens before reading to fail fast on schema issues
        if required_columns:
            validate_csv_columns(filepath, required_columns)

        rows = []
        # newline='' is required by csv module to handle line endings correctly
        # See: https://docs.python.org/3/library/csv.html#csv.reader
        with open(filepath, 'r', encoding=encoding, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)

        logger.info(f"Successfully loaded {len(rows)} rows from {filepath}")
        return rows

    except Exception as e:
        logger.error(f"Error reading CSV file {filepath}: {e}")
        raise


def write_dict_csv(data: List[Dict[str, Any]],
                  filepath: Union[str, Path],
                  fieldnames: Optional[List[str]] = None,
                  encoding: str = 'utf-8') -> None:
    """
    Write list of dictionaries to CSV file.

    Args:
        data: List of dictionaries to write
        filepath: Destination file path
        fieldnames: Optional list of field names (defaults to keys from first row)
        encoding: File encoding (default: utf-8)
    """
    filepath = Path(filepath)

    if not data:
        logger.warning(f"No data to write to {filepath}")
        return

    try:
        # Ensure directory exists
        filepath.parent.mkdir(parents=True, exist_ok=True)

        # Use provided fieldnames or extract from first row
        if fieldnames is None:
            fieldnames = list(data[0].keys())

        with open(filepath, 'w', encoding=encoding, newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

        logger.info(f"Successfully wrote {len(data)} rows to {filepath}")

    except Exception as e:
        logger.error(f"Error writing CSV file {filepath}: {e}")
        raise


def merge_csv_files(input_files: List[Union[str, Path]],
                   output_file: Union[str, Path],
                   how: str = 'concat') -> pd.DataFrame:
    """
    Merge multiple CSV files into a single DataFrame and optionally save.

    Args:
        input_files: List of CSV file paths to merge
        output_file: Output file path
        how: Method for merging ('concat' for concatenation)

    Returns:
        pd.DataFrame: Merged DataFrame
    """
    try:
        dataframes = []

        for file_path in input_files:
            if Path(file_path).exists():
                df = pd.read_csv(file_path)
                dataframes.append(df)
                logger.info(f"Loaded {len(df)} rows from {file_path}")
            else:
                logger.warning(f"File not found, skipping: {file_path}")

        if not dataframes:
            raise ValueError("No valid CSV files found to merge")

        # Merge dataframes
        # concat: Stack dataframes vertically (union all rows)
        if how == 'concat':
            # ignore_index=True creates new sequential index (0, 1, 2...)
            # This prevents duplicate index values from different files
            merged_df = pd.concat(dataframes, ignore_index=True)
        else:
            # Currently only concat is supported; could add 'merge' for joins later
            raise ValueError(f"Unsupported merge method: {how}")

        # Write merged data
        write_csv_with_backup(merged_df, output_file, create_backup=False)

        logger.info(f"Successfully merged {len(dataframes)} files into {output_file}")
        return merged_df

    except Exception as e:
        logger.error(f"Error merging CSV files: {e}")
        raise


# Decorator provides automatic error handling with logging
# Returns empty DataFrame on any exception (graceful degradation)
@handle_errors(default_return=pd.DataFrame(), component="csv_utils", operation="safe_csv_read")
def safe_csv_read(filepath: Union[str, Path],
                 default_value: Optional[pd.DataFrame] = None) -> pd.DataFrame:
    """
    Safely read CSV file with fallback to default value if file doesn't exist.
    Enhanced with standardized error handling.

    Args:
        filepath: Path to the CSV file
        default_value: Default DataFrame to return if file doesn't exist

    Returns:
        pd.DataFrame: Loaded DataFrame or default value
    """
    filepath = Path(filepath)

    try:
        if filepath.exists():
            return pd.read_csv(filepath)
        else:
            logger.warning(f"CSV file not found: {filepath}, using default value")
            return default_value if default_value is not None else pd.DataFrame()

    except Exception as e:
        logger.warning(f"Error reading CSV file {filepath}: {e}, using default value")
        return default_value if default_value is not None else pd.DataFrame()


def csv_column_exists(filepath: Union[str, Path], column_name: str) -> bool:
    """
    Check if a specific column exists in a CSV file.

    Args:
        filepath: Path to the CSV file
        column_name: Name of the column to check

    Returns:
        bool: True if column exists, False otherwise
    """
    filepath = Path(filepath)

    try:
        if not filepath.exists():
            return False

        with open(filepath, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            return column_name in (reader.fieldnames or [])

    except Exception as e:
        logger.error(f"Error checking column in {filepath}: {e}")
        return False