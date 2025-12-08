"""
Run Draft Order Simulation Script

Tests all draft order strategy files in simulation/sim_data/draft_order_possibilities/
and produces a JSON file mapping each strategy to its win percentage.

This script runs simulations for all 75 draft order strategies to determine which
strategies perform best in league simulations.

Usage (from project root):
    python run_draft_order_simulation.py                    # defaults to 15 sims per file
    python run_draft_order_simulation.py --sims 50          # more accurate
    python run_draft_order_simulation.py --sims 5           # faster testing

Author: Kai Mizuno
"""

import argparse
import sys
import json
import time
import copy
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional

from utils.LoggingManager import setup_logger, get_logger

# Add simulation directory to path
sys.path.append(str(Path(__file__).parent / "simulation"))
from ParallelLeagueRunner import ParallelLeagueRunner
from ConfigGenerator import ConfigGenerator


# Logging configuration
LOGGING_LEVEL = 'INFO'
LOGGING_TO_FILE = False
LOG_NAME = "draft_order_simulation"
LOGGING_FILE = './simulation/draft_order_log.txt'
LOGGING_FORMAT = 'standard'

# Default values
DEFAULT_SIMS = 5
DEFAULT_OUTPUT = 'simulation/draft_order_results'
DEFAULT_WORKERS = 7
DEFAULT_DATA = 'simulation/sim_data'
DEFAULT_BASELINE = ''
PROGRESS_LOG_INTERVAL = 5  # Log progress every 5 files


def discover_draft_order_files(draft_order_dir: Path) -> List[int]:
    """
    Discover all draft order JSON files and extract their numbers.

    Args:
        draft_order_dir (Path): Directory containing draft order files

    Returns:
        List[int]: Sorted list of file numbers (e.g., [1, 2, 3, ..., 75])

    Raises:
        FileNotFoundError: If draft order directory doesn't exist

    Example:
        >>> files = discover_draft_order_files(Path("simulation/sim_data/draft_order_possibilities"))
        >>> print(files)
        [1, 2, 3, ..., 75]
    """
    logger = get_logger()

    if not draft_order_dir.exists():
        raise FileNotFoundError(f"Draft order directory not found: {draft_order_dir}")

    json_files = list(draft_order_dir.glob("*.json"))
    file_numbers = []

    for json_file in json_files:
        # Extract leading digits from filename (e.g., "1.json" -> 1, "2_zero_rb.json" -> 2)
        match = re.match(r"^(\d+)", json_file.stem)
        if match:
            file_numbers.append(int(match.group(1)))
        else:
            logger.warning(f"Skipping file with no leading number: {json_file.name}")

    file_numbers.sort()
    logger.info(f"Discovered {len(file_numbers)} draft order files")

    return file_numbers


def load_draft_order_from_file(file_num: int, data_folder: Path) -> list:
    """
    Load DRAFT_ORDER array from numbered file.

    Args:
        file_num (int): File number (e.g., 1 for "1.json" or "1_strategy.json")
        data_folder (Path): Base data folder (contains draft_order_possibilities/)

    Returns:
        list: DRAFT_ORDER array from the file

    Raises:
        FileNotFoundError: If no matching file found

    Example:
        >>> draft_order = load_draft_order_from_file(2, Path("simulation/sim_data"))
        >>> print(len(draft_order))
        15
    """
    logger = get_logger()
    draft_order_dir = data_folder / "draft_order_possibilities"

    # Try pattern with suffix first (e.g., 2_zero_rb.json)
    matches = list(draft_order_dir.glob(f"{file_num}_*.json"))
    if not matches:
        # Try exact match (e.g., 1.json)
        matches = list(draft_order_dir.glob(f"{file_num}.json"))

    if not matches:
        raise FileNotFoundError(f"No draft order file found for number {file_num} in {draft_order_dir}")

    with open(matches[0], 'r') as f:
        data = json.load(f)

    logger.debug(f"Loaded DRAFT_ORDER from {matches[0].name}")
    return data['DRAFT_ORDER']


def validate_season_data(season_folder: Path) -> bool:
    """
    Validate season has sufficient valid player data for simulation.

    A season needs at least 150 valid players (drafted=0 AND fantasy_points>0)
    to support a 10-team draft with 15 picks each.

    Args:
        season_folder (Path): Path to season folder

    Returns:
        bool: True if season has sufficient data, False otherwise
    """
    import csv
    logger = get_logger()
    MIN_VALID_PLAYERS = 150  # 10 teams × 15 picks

    # Check week 1 players_projected.csv for valid player count
    players_file = season_folder / "weeks" / "week_01" / "players_projected.csv"
    if not players_file.exists():
        players_file = season_folder / "weeks" / "week_01" / "players.csv"

    if not players_file.exists():
        logger.warning(f"Season {season_folder.name}: No player CSV found")
        return False

    try:
        with open(players_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            valid_count = 0
            for row in reader:
                drafted = row.get('drafted', '0')
                fp = row.get('fantasy_points', '')
                try:
                    fp_val = float(fp) if fp else 0
                except (ValueError, TypeError):
                    fp_val = 0
                if drafted == '0' and fp_val > 0:
                    valid_count += 1

            if valid_count < MIN_VALID_PLAYERS:
                logger.warning(
                    f"Season {season_folder.name}: Only {valid_count} valid players "
                    f"(need {MIN_VALID_PLAYERS}+ for draft)"
                )
                return False

            logger.debug(f"Season {season_folder.name}: {valid_count} valid players - OK")
            return True

    except Exception as e:
        logger.warning(f"Season {season_folder.name}: Error reading player data: {e}")
        return False


def discover_season_folders(data_folder: Path) -> List[Path]:
    """
    Discover available historical season folders (2021, 2022, 2024, etc.).

    Validates each season has both:
    1. Required folder structure (weeks/week_XX/)
    2. Sufficient valid player data (150+ draftable players)

    Args:
        data_folder (Path): Base simulation data folder

    Returns:
        List[Path]: List of valid season folder paths, sorted

    Raises:
        FileNotFoundError: If no season folders found
    """
    logger = get_logger()

    season_folders = sorted(data_folder.glob("20*/"))

    if not season_folders:
        raise FileNotFoundError(
            f"No historical season folders (20XX/) found in {data_folder}. "
            "Run compile_historical_data.py first."
        )

    # Validate each season has required structure AND sufficient player data
    valid_seasons = []
    for folder in season_folders:
        # Check for week data structure
        weeks_dir = folder / "weeks"
        if not weeks_dir.exists() or not any(weeks_dir.glob("week_*")):
            logger.warning(f"Skipping {folder.name} - missing weeks/ structure")
            continue

        # Validate sufficient player data
        if not validate_season_data(folder):
            logger.warning(f"Skipping {folder.name} - insufficient player data")
            continue

        valid_seasons.append(folder)
        logger.debug(f"Found valid season: {folder.name}")

    if not valid_seasons:
        raise FileNotFoundError(
            f"No valid season folders with sufficient data found in {data_folder}"
        )

    logger.info(f"Discovered {len(valid_seasons)} valid seasons: {[f.name for f in valid_seasons]}")
    return valid_seasons


def run_simulation_for_draft_order(
    file_num: int,
    baseline_config: dict,
    num_sims_per_season: int,
    runner: ParallelLeagueRunner,
    data_folder: Path,
    season_folders: List[Path]
) -> Tuple[int, float, bool]:
    """
    Run multi-season simulations for a single draft order file.

    Iterates through all available season folders (2021, 2022, 2024, etc.)
    and aggregates results across seasons for robust validation.

    Args:
        file_num (int): Draft order file number
        baseline_config (dict): Baseline configuration to use
        num_sims_per_season (int): Number of simulations per season
        runner (ParallelLeagueRunner): Initialized runner instance
        data_folder (Path): Base data folder (for loading draft order files)
        season_folders (List[Path]): List of season folders to simulate

    Returns:
        Tuple[int, float, bool]: (file_num, win_percentage, success)
            - file_num: The draft order file number
            - win_percentage: Win percentage (0.0-100.0) across all seasons
            - success: True if simulation succeeded, False if failed

    Example:
        >>> file_num, win_pct, success = run_simulation_for_draft_order(
        ...     1, config, 5, runner, data_folder, season_folders)
        >>> print(f"File {file_num}: {win_pct}% win rate")
        File 1: 72.5% win rate
    """
    logger = get_logger()

    try:
        # Deep copy baseline config to avoid mutations
        config = copy.deepcopy(baseline_config)

        # Load DRAFT_ORDER from file
        draft_order = load_draft_order_from_file(file_num, data_folder)

        # Update config with this draft order
        config['parameters']['DRAFT_ORDER_FILE'] = file_num
        config['parameters']['DRAFT_ORDER'] = draft_order

        # Run simulations across all seasons
        logger.info(f"Testing draft order file {file_num} across {len(season_folders)} seasons...")

        total_wins = 0
        total_losses = 0

        for season_folder in season_folders:
            # Update runner to use this season's data
            runner.set_data_folder(season_folder)

            # Run simulations for this season using week-by-week method
            season_results = runner.run_simulations_for_config_with_weeks(
                config, num_sims_per_season
            )

            # Aggregate season results
            # run_simulations_for_config_with_weeks returns List[List[Tuple[week, won, points]]]
            for sim_result in season_results:
                for _week_num, won, _points in sim_result:
                    if won:
                        total_wins += 1
                    else:
                        total_losses += 1

        total_games = total_wins + total_losses

        # Calculate win percentage
        if total_games > 0:
            win_pct = round((total_wins / total_games) * 100, 1)
        else:
            win_pct = 0.0

        logger.debug(f"File {file_num}: {total_wins}W-{total_losses}L = {win_pct}%")
        return (file_num, win_pct, True)

    except Exception as e:
        logger.error(f"Failed to simulate draft order {file_num}: {e}")
        return (file_num, 0.0, False)


def save_results_json(
    results: Dict[str, float],
    metadata: dict,
    output_dir: Path
) -> Path:
    """
    Save results to JSON file with metadata.

    Args:
        results (Dict[str, float]): Mapping of file numbers to win percentages
        metadata (dict): Metadata about the simulation run
        output_dir (Path): Output directory path

    Returns:
        Path: Path to saved JSON file

    Example:
        >>> results = {"1": 70.2, "2": 80.1}
        >>> metadata = {"timestamp": "2025-11-24 12:34:56", ...}
        >>> path = save_results_json(results, metadata, Path("simulation/draft_order_results"))
        >>> print(f"Results saved to {path}")
    """
    logger = get_logger()

    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    # Create filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"draft_order_win_rates_{timestamp}.json"

    # Combine metadata and results
    output_data = {
        "metadata": metadata,
        "results": results
    }

    # Save to file
    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2)

    logger.info(f"Results saved to: {output_file}")
    return output_file


def find_config_folders(search_dir: Path, pattern: str) -> list:
    """
    Find config folders matching pattern, sorted by modification time (newest first).

    Args:
        search_dir (Path): Directory to search in
        pattern (str): Glob pattern for folder names (e.g., "optimal_*")

    Returns:
        list: List of valid config folder paths, sorted newest first
    """
    folders = [p for p in search_dir.glob(pattern) if p.is_dir()]
    # Validate folders have required files
    required_files = ['league_config.json', 'week1-5.json', 'week6-11.json', 'week12-17.json']
    valid_folders = []
    for folder in folders:
        if all((folder / f).exists() for f in required_files):
            valid_folders.append(folder)
    # Sort by modification time (most recent first)
    valid_folders.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return valid_folders


def load_baseline_config(baseline_path: Optional[Path]) -> Tuple[dict, Path]:
    """
    Load baseline configuration from folder.

    The system now uses folder-based configs with multiple files:
    - league_config.json (base parameters)
    - week1-5.json, week6-11.json, week12-17.json (week-specific params)

    Args:
        baseline_path (Optional[Path]): Path to baseline config folder, or None to auto-detect

    Returns:
        Tuple[dict, Path]: (Loaded configuration dictionary, path to config folder)

    Raises:
        SystemExit: If no baseline config found
    """
    logger = get_logger()

    # If baseline specified, try to load it
    if baseline_path:
        if not baseline_path.exists():
            logger.error(f"Specified baseline config not found: {baseline_path}")
            sys.exit(1)
        if not baseline_path.is_dir():
            logger.error(f"Baseline must be a folder, not a file: {baseline_path}")
            logger.error("Expected folder with: league_config.json, week1-5.json, week6-11.json, week12-17.json")
            sys.exit(1)
    else:
        # Auto-detect: look for most recent optimal_*/ folder
        config_dir = Path("simulation/simulation_configs")

        if not config_dir.exists():
            logger.error(f"Config directory not found: {config_dir}")
            logger.error("Please provide a baseline config folder using --baseline argument")
            sys.exit(1)

        optimal_folders = find_config_folders(config_dir, "optimal_*")

        if not optimal_folders:
            logger.error(f"No optimal config folders found in {config_dir}")
            logger.error("Expected folders with: league_config.json, week1-5.json, week6-11.json, week12-17.json")
            logger.error("Please provide a baseline config folder using --baseline argument")
            sys.exit(1)

        baseline_path = optimal_folders[0]
        logger.info(f"Using baseline config folder: {baseline_path.name}")

    # Load config using ConfigGenerator's folder loader
    config = ConfigGenerator.load_baseline_from_folder(baseline_path)

    return config, baseline_path


def main():
    """
    Main entry point for draft order simulation script.

    Tests all 75 draft order strategies and produces a JSON file mapping
    file numbers to win percentages.
    """
    # Initialize logging
    setup_logger(LOG_NAME, LOGGING_LEVEL, LOGGING_TO_FILE, LOGGING_FILE, LOGGING_FORMAT)
    logger = get_logger()

    # Create argument parser
    parser = argparse.ArgumentParser(
        description="Test all draft order strategies and generate win percentage report",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run with default settings (15 sims per file, ~10-15 min)
  python run_draft_order_simulation.py

  # Run with more simulations for higher accuracy
  python run_draft_order_simulation.py --sims 50

  # Quick test with fewer simulations
  python run_draft_order_simulation.py --sims 5

  # Use custom baseline config
  python run_draft_order_simulation.py --baseline my_config.json
        """
    )

    parser.add_argument(
        '--sims',
        type=int,
        default=DEFAULT_SIMS,
        help=f'Number of simulations per draft order (default: {DEFAULT_SIMS}, ~10-15 min runtime)'
    )
    parser.add_argument(
        '--baseline',
        type=str,
        default=DEFAULT_BASELINE,
        help='Path to baseline configuration JSON (default: most recent optimal config)'
    )
    parser.add_argument(
        '--output',
        type=str,
        default=DEFAULT_OUTPUT,
        help=f'Output directory for results (default: {DEFAULT_OUTPUT})'
    )
    parser.add_argument(
        '--workers',
        type=int,
        default=DEFAULT_WORKERS,
        help=f'Number of parallel worker threads (default: {DEFAULT_WORKERS})'
    )
    parser.add_argument(
        '--data',
        type=str,
        default=DEFAULT_DATA,
        help=f'Path to simulation data folder (default: {DEFAULT_DATA})'
    )
    parser.add_argument(
        '--use-processes',
        action='store_true',
        default=False,
        help='Use ProcessPoolExecutor for true parallelism (bypasses GIL). '
             'Recommended for CPU-bound simulations on multi-core systems.'
    )

    args = parser.parse_args()

    # Convert paths
    output_dir = Path(args.output)
    data_folder = Path(args.data)
    baseline_path = Path(args.baseline) if args.baseline else None

    # Display configuration
    logger.info("=" * 80)
    logger.info("DRAFT ORDER STRATEGY SIMULATION")
    logger.info("=" * 80)
    logger.info(f"Simulations per draft order: {args.sims}")
    logger.info(f"Worker threads: {args.workers}")
    logger.info(f"Data folder: {data_folder}")
    logger.info(f"Output directory: {output_dir}")

    # Load baseline config
    baseline_config, actual_baseline_path = load_baseline_config(baseline_path)
    logger.info(f"Baseline config loaded: {baseline_config.get('config_name', 'unknown')}")
    logger.info(f"Baseline path: {actual_baseline_path}")

    # Validate data folder
    draft_order_dir = data_folder / "draft_order_possibilities"
    if not draft_order_dir.exists():
        logger.error(f"Draft order directory not found: {draft_order_dir}")
        sys.exit(1)

    # Discover available seasons for multi-season validation
    logger.info("=" * 80)
    logger.info("DISCOVERING HISTORICAL SEASONS")
    logger.info("=" * 80)
    try:
        season_folders = discover_season_folders(data_folder)
    except FileNotFoundError as e:
        logger.error(str(e))
        sys.exit(1)

    # Discover draft order files
    logger.info("=" * 80)
    logger.info("DISCOVERING DRAFT ORDER FILES")
    logger.info("=" * 80)
    draft_order_files = discover_draft_order_files(draft_order_dir)
    logger.info(f"Found {len(draft_order_files)} draft order files to test")

    # Estimate runtime (accounts for multi-season simulation)
    # Each draft order runs sims_per_season * num_seasons * 17_weeks simulations
    total_sims = len(draft_order_files) * args.sims * len(season_folders) * 17
    estimated_time_min = (total_sims * 0.1) / (args.workers * 60)  # ~0.1s per sim
    logger.info(f"Simulations per draft order: {args.sims} per season x {len(season_folders)} seasons")
    logger.info(f"Total simulations: {total_sims:,}")
    logger.info(f"Estimated runtime: {estimated_time_min:.1f} minutes")

    # Initialize parallel runner
    logger.info("=" * 80)
    logger.info("INITIALIZING SIMULATION RUNNER")
    logger.info("=" * 80)
    runner = ParallelLeagueRunner(
        max_workers=args.workers,
        data_folder=data_folder,
        use_processes=args.use_processes
    )
    executor_type = "ProcessPoolExecutor" if args.use_processes else "ThreadPoolExecutor"
    logger.info(f"Runner initialized with {args.workers} workers ({executor_type})")

    # Run simulations for all draft orders
    logger.info("=" * 80)
    logger.info("RUNNING MULTI-SEASON SIMULATIONS")
    logger.info("=" * 80)

    start_time = time.time()
    results = {}
    failed_files = []

    for idx, file_num in enumerate(draft_order_files, start=1):
        # Run multi-season simulation for this draft order
        file_num, win_pct, success = run_simulation_for_draft_order(
            file_num,
            baseline_config,
            args.sims,
            runner,
            data_folder,
            season_folders
        )

        if success:
            results[str(file_num)] = win_pct
        else:
            failed_files.append(file_num)

        # Log progress every N files
        if idx % PROGRESS_LOG_INTERVAL == 0:
            elapsed = time.time() - start_time
            files_per_sec = idx / elapsed
            remaining_files = len(draft_order_files) - idx
            eta_seconds = remaining_files / files_per_sec if files_per_sec > 0 else 0
            logger.info(
                f"Progress: {idx}/{len(draft_order_files)} files complete "
                f"({idx/len(draft_order_files)*100:.1f}%) - ETA: {eta_seconds/60:.1f} min"
            )

    # Calculate total runtime
    elapsed_time = time.time() - start_time

    # Display final summary
    logger.info("=" * 80)
    logger.info("SIMULATION COMPLETE")
    logger.info("=" * 80)
    logger.info(f"Total runtime: {elapsed_time/60:.1f} minutes")
    logger.info(f"Files tested successfully: {len(results)}/{len(draft_order_files)}")

    if failed_files:
        logger.warning(f"Failed files: {failed_files}")
    else:
        logger.info("All files tested successfully!")

    # Create metadata
    metadata = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "num_simulations_per_season": args.sims,
        "seasons_used": [f.name for f in season_folders],
        "num_seasons": len(season_folders),
        "total_files_tested": len(draft_order_files),
        "successful_files": len(results),
        "failed_files": failed_files,
        "baseline_config": str(actual_baseline_path),
        "runtime_minutes": round(elapsed_time / 60, 2)
    }

    # Save results
    logger.info("=" * 80)
    logger.info("SAVING RESULTS")
    logger.info("=" * 80)
    output_file = save_results_json(results, metadata, output_dir)

    logger.info("=" * 80)
    logger.info(f"✓ Results saved to: {output_file}")
    logger.info("=" * 80)

    # Display top 10 strategies
    logger.info("Top 10 Draft Order Strategies:")
    sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)
    for i, (file_num, win_pct) in enumerate(sorted_results[:10], start=1):
        logger.info(f"  {i}. File #{file_num}: {win_pct}% win rate")


if __name__ == "__main__":
    main()
