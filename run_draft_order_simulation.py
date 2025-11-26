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


# Logging configuration
LOGGING_LEVEL = 'INFO'
LOGGING_TO_FILE = False
LOG_NAME = "draft_order_simulation"
LOGGING_FILE = './simulation/draft_order_log.txt'
LOGGING_FORMAT = 'standard'

# Default values
DEFAULT_SIMS = 50
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


def run_simulation_for_draft_order(
    file_num: int,
    baseline_config: dict,
    num_sims: int,
    runner: ParallelLeagueRunner,
    data_folder: Path
) -> Tuple[int, float, bool]:
    """
    Run simulations for a single draft order file.

    Args:
        file_num (int): Draft order file number
        baseline_config (dict): Baseline configuration to use
        num_sims (int): Number of simulations to run
        runner (ParallelLeagueRunner): Initialized runner instance
        data_folder (Path): Base data folder

    Returns:
        Tuple[int, float, bool]: (file_num, win_percentage, success)
            - file_num: The draft order file number
            - win_percentage: Win percentage (0.0-100.0)
            - success: True if simulation succeeded, False if failed

    Example:
        >>> file_num, win_pct, success = run_simulation_for_draft_order(1, config, 15, runner, data_folder)
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

        # Run simulations
        logger.info(f"Testing draft order file {file_num}...")
        results = runner.run_simulations_for_config(config, num_sims)

        # Aggregate results
        total_wins = sum(wins for wins, losses, points in results)
        total_losses = sum(losses for wins, losses, points in results)
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


def load_baseline_config(baseline_path: Optional[Path], output_dir: Path) -> dict:
    """
    Load baseline configuration file.

    Args:
        baseline_path (Optional[Path]): Path to baseline config, or None to auto-detect
        output_dir (Path): Output directory to search for configs

    Returns:
        dict: Loaded configuration dictionary

    Raises:
        SystemExit: If no baseline config found
    """
    logger = get_logger()

    # If baseline specified, try to load it
    if baseline_path:
        if not baseline_path.exists():
            logger.error(f"Specified baseline config not found: {baseline_path}")
            sys.exit(1)
    else:
        # Auto-detect: look for most recent optimal_*.json
        config_dir = Path("simulation/simulation_configs")
        optimal_configs = list(config_dir.glob("optimal_*.json"))

        if not optimal_configs:
            logger.error(f"No optimal config files found in {config_dir}")
            logger.error("Please provide a baseline config using --baseline argument")
            sys.exit(1)

        # Sort by modification time (most recent first)
        optimal_configs.sort(key=lambda p: p.stat().st_mtime, reverse=True)
        baseline_path = optimal_configs[0]
        logger.info(f"Using baseline config: {baseline_path.name}")

    # Load config
    with open(baseline_path, 'r') as f:
        config = json.load(f)

    return config


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
    baseline_config = load_baseline_config(baseline_path, output_dir)
    logger.info(f"Baseline config loaded: {baseline_config.get('config_name', 'unknown')}")

    # Validate data folder
    draft_order_dir = data_folder / "draft_order_possibilities"
    if not draft_order_dir.exists():
        logger.error(f"Draft order directory not found: {draft_order_dir}")
        sys.exit(1)

    # Discover draft order files
    logger.info("=" * 80)
    logger.info("DISCOVERING DRAFT ORDER FILES")
    logger.info("=" * 80)
    draft_order_files = discover_draft_order_files(draft_order_dir)
    logger.info(f"Found {len(draft_order_files)} draft order files to test")

    # Estimate runtime
    estimated_time_min = (len(draft_order_files) * args.sims * 5) / (args.workers * 60)
    logger.info(f"Estimated runtime: {estimated_time_min:.1f} minutes")

    # Initialize parallel runner
    logger.info("=" * 80)
    logger.info("INITIALIZING SIMULATION RUNNER")
    logger.info("=" * 80)
    runner = ParallelLeagueRunner(max_workers=args.workers, data_folder=data_folder)
    logger.info(f"Runner initialized with {args.workers} workers")

    # Run simulations for all draft orders
    logger.info("=" * 80)
    logger.info("RUNNING SIMULATIONS")
    logger.info("=" * 80)

    start_time = time.time()
    results = {}
    failed_files = []

    for idx, file_num in enumerate(draft_order_files, start=1):
        # Run simulation for this draft order
        file_num, win_pct, success = run_simulation_for_draft_order(
            file_num,
            baseline_config,
            args.sims,
            runner,
            data_folder
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
        "num_simulations_per_file": args.sims,
        "total_files_tested": len(draft_order_files),
        "successful_files": len(results),
        "failed_files": failed_files,
        "baseline_config": str(baseline_path) if baseline_path else "auto-detected",
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
