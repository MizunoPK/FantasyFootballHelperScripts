"""
Run Draft Order Loop Simulation Script

Loops through all draft order strategy files in simulation/sim_data/draft_order_possibilities/,
running full iterative optimization for each one. Each strategy gets its own dedicated config
folder in simulation/simulation_configs/strategies/{N}_{description}/.

Features:
- Per-strategy optimization with dedicated output folders
- Auto-resume from crashes via loop_progress.json and intermediate_* folder detection
- Endless loop cycling through all strategies continuously
- Uses same optimizations as run_simulation.py (--use-processes, workers, etc.)

Usage (from project root):
    python run_draft_order_loop.py                       # defaults
    python run_draft_order_loop.py --sims 100            # more simulations
    python run_draft_order_loop.py --use-processes       # use ProcessPoolExecutor

Author: Kai Mizuno
"""

import argparse
import sys
import json
import re
import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Tuple, Optional

from utils.LoggingManager import setup_logger, get_logger

# Add simulation directory to path for imports
sys.path.append(str(Path(__file__).parent / "simulation"))
from SimulationManager import SimulationManager


# Logging configuration - adjust these settings to control verbosity
LOGGING_LEVEL = 'INFO'
LOGGING_TO_FILE = False
LOG_NAME = "draft_order_loop"
LOGGING_FILE = './simulation/draft_order_loop_log.txt'
LOGGING_FORMAT = 'standard'

# Default values (matching run_simulation.py)
DEFAULT_SIMS = 3
DEFAULT_WORKERS = 8
DEFAULT_DATA = 'simulation/sim_data'
DEFAULT_TEST_VALUES = 24
NUM_PARAMETERS_TO_TEST = 1


def discover_draft_order_files(draft_order_dir: Path) -> List[int]:
    """
    Discover all draft order JSON files and extract their numbers.

    Args:
        draft_order_dir (Path): Directory containing draft order files

    Returns:
        List[int]: Sorted list of file numbers (e.g., [0, 1, 2, ..., N])

    Raises:
        FileNotFoundError: If draft order directory doesn't exist
    """
    logger = get_logger()

    if not draft_order_dir.exists():
        raise FileNotFoundError(f"Draft order directory not found: {draft_order_dir}")

    json_files = list(draft_order_dir.glob("*.json"))
    file_numbers = []

    for json_file in json_files:
        # Extract leading digits from filename (e.g., "0_MINE.json" -> 0, "1_zero_rb.json" -> 1)
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
        file_num (int): File number (e.g., 0 for "0_MINE.json")
        data_folder (Path): Base data folder (contains draft_order_possibilities/)

    Returns:
        list: DRAFT_ORDER array from the file

    Raises:
        FileNotFoundError: If no matching file found
    """
    logger = get_logger()
    draft_order_dir = data_folder / "draft_order_possibilities"

    # Try pattern with suffix first (e.g., 0_MINE.json)
    matches = list(draft_order_dir.glob(f"{file_num}_*.json"))
    if not matches:
        # Try exact match (e.g., 0.json)
        matches = list(draft_order_dir.glob(f"{file_num}.json"))

    if not matches:
        raise FileNotFoundError(f"No draft order file found for number {file_num} in {draft_order_dir}")

    with open(matches[0], 'r') as f:
        data = json.load(f)

    logger.debug(f"Loaded DRAFT_ORDER from {matches[0].name}")
    return data['DRAFT_ORDER']


def get_strategy_name(file_num: int, data_folder: Path) -> str:
    """
    Get strategy folder name from file number.

    Args:
        file_num (int): File number (e.g., 0, 1, 2)
        data_folder (Path): Base data folder

    Returns:
        str: Strategy name (e.g., "0_MINE", "1_zero_rb")

    Raises:
        FileNotFoundError: If no matching file found
    """
    draft_order_dir = data_folder / "draft_order_possibilities"

    # Try pattern with suffix first (e.g., 0_MINE.json)
    matches = list(draft_order_dir.glob(f"{file_num}_*.json"))
    if matches:
        return matches[0].stem  # "0_MINE"

    # Try exact match (e.g., 0.json)
    matches = list(draft_order_dir.glob(f"{file_num}.json"))
    if matches:
        return matches[0].stem  # "0"

    raise FileNotFoundError(f"No draft order file found for number {file_num}")


def find_latest_optimal_folder(config_dir: Path) -> Optional[Path]:
    """
    Find the most recent optimal_* folder in the config directory.

    Args:
        config_dir (Path): Directory to search (e.g., simulation/simulation_configs)

    Returns:
        Optional[Path]: Path to most recent optimal folder, or None if none found
    """
    required_files = ['league_config.json', 'week1-5.json', 'week6-9.json', 'week10-13.json', 'week14-17.json']

    optimal_folders = []
    for folder in config_dir.glob("optimal_*"):
        if folder.is_dir() and all((folder / f).exists() for f in required_files):
            optimal_folders.append(folder)

    if not optimal_folders:
        return None

    # Sort by modification time (most recent first)
    optimal_folders.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return optimal_folders[0]


def find_resume_point(draft_files: List[int], strategies_dir: Path, data_folder: Path) -> Tuple[int, str, int]:
    """
    Find where to resume the loop from.

    Args:
        draft_files (List[int]): List of draft order file numbers
        strategies_dir (Path): Path to strategies directory
        data_folder (Path): Path to simulation data folder

    Returns:
        Tuple[int, str, int]: (start_idx, action, current_cycle)
            - start_idx: Index into draft_files to start from
            - action: "start" or "resume" (has intermediate_*)
            - current_cycle: Which optimization cycle
    """
    logger = get_logger()
    progress_file = strategies_dir / "loop_progress.json"

    # Load progress (or initialize if first run)
    if progress_file.exists():
        with open(progress_file, 'r') as f:
            progress = json.load(f)
        last_completed = progress.get("last_completed_strategy", -1)
        current_cycle = progress.get("current_cycle", 1)

        # Bounds check: if files were removed, reset
        if last_completed >= len(draft_files):
            logger.warning(
                f"Progress index {last_completed} exceeds file count {len(draft_files)}. "
                f"Resetting to start of new cycle."
            )
            last_completed = -1
            current_cycle += 1
    else:
        last_completed = -1  # None completed yet
        current_cycle = 1

    # Next strategy to process
    next_strategy_idx = last_completed + 1

    # Check if we've completed all strategies in this cycle
    if next_strategy_idx >= len(draft_files):
        # Start new cycle
        current_cycle += 1
        next_strategy_idx = 0

    # Check if the next strategy has an intermediate_* folder (mid-optimization resume)
    if next_strategy_idx < len(draft_files):
        file_num = draft_files[next_strategy_idx]
        try:
            strategy_name = get_strategy_name(file_num, data_folder)
        except FileNotFoundError:
            # Use file number as name if file not found
            strategy_name = str(file_num)

        strategy_folder = strategies_dir / strategy_name
        if strategy_folder.exists():
            intermediate_folders = list(strategy_folder.glob("intermediate_*"))
            if intermediate_folders:
                return next_strategy_idx, "resume", current_cycle

    return next_strategy_idx, "start", current_cycle


def update_progress(progress_file: Path, last_completed: int, cycle: int) -> None:
    """
    Update progress tracker file after strategy completion.

    Args:
        progress_file (Path): Path to loop_progress.json
        last_completed (int): Index of last completed strategy
        cycle (int): Current optimization cycle
    """
    progress = {
        "current_cycle": cycle,
        "last_completed_strategy": last_completed,
        "last_updated": datetime.now().isoformat()
    }
    with open(progress_file, 'w') as f:
        json.dump(progress, f, indent=2)


def seed_strategy_folder(strategy_folder: Path, root_baseline: Path, file_num: int, data_folder: Path) -> None:
    """
    Seed a new strategy folder from root baseline with DRAFT_ORDER injected.

    Args:
        strategy_folder (Path): Path to strategy folder to create
        root_baseline (Path): Path to root optimal_* folder to copy from
        file_num (int): Draft order file number
        data_folder (Path): Base data folder for loading draft order
    """
    logger = get_logger()

    seed_folder = strategy_folder / "optimal_seed"
    seed_folder.mkdir(parents=True, exist_ok=True)

    # Copy 4 config files from root baseline
    for filename in ['league_config.json', 'week1-5.json', 'week6-9.json', 'week10-13.json', 'week14-17.json']:
        shutil.copy(root_baseline / filename, seed_folder / filename)

    # Inject DRAFT_ORDER into league_config.json
    draft_order = load_draft_order_from_file(file_num, data_folder)
    league_config_path = seed_folder / 'league_config.json'

    with open(league_config_path, 'r') as f:
        config = json.load(f)

    config['parameters']['DRAFT_ORDER_FILE'] = file_num
    config['parameters']['DRAFT_ORDER'] = draft_order

    with open(league_config_path, 'w') as f:
        json.dump(config, f, indent=2)

    logger.info(f"Seeded strategy folder: {strategy_folder.name}")


def ensure_strategy_folder(strategy_folder: Path, root_baseline: Path, file_num: int, data_folder: Path) -> None:
    """
    Ensure strategy folder exists with valid configs. Seed if needed.

    Args:
        strategy_folder (Path): Path to strategy folder
        root_baseline (Path): Path to root optimal_* folder
        file_num (int): Draft order file number
        data_folder (Path): Base data folder
    """
    logger = get_logger()
    required_files = ['league_config.json', 'week1-5.json', 'week6-9.json', 'week10-13.json', 'week14-17.json']

    # Check if we need to seed
    needs_seed = False
    if not strategy_folder.exists():
        needs_seed = True
    else:
        # Check for any optimal_* folder with required files
        has_valid_baseline = False
        for opt_folder in strategy_folder.glob("optimal_*"):
            if all((opt_folder / f).exists() for f in required_files):
                has_valid_baseline = True
                break

        if not has_valid_baseline:
            logger.warning(f"Corrupt strategy folder {strategy_folder.name}, re-seeding")
            shutil.rmtree(strategy_folder)
            needs_seed = True

    if needs_seed:
        seed_strategy_folder(strategy_folder, root_baseline, file_num, data_folder)


def get_strategy_baseline(strategy_folder: Path) -> Path:
    """
    Get the best baseline to use for this strategy's optimization.

    Args:
        strategy_folder (Path): Path to strategy folder

    Returns:
        Path: Path to baseline folder (optimal_iterative_* or optimal_seed)

    Raises:
        ValueError: If no valid baseline found
    """
    required_files = ['league_config.json', 'week1-5.json', 'week6-9.json', 'week10-13.json', 'week14-17.json']

    # Prefer most recent optimal_iterative_* if exists (from previous optimization)
    optimal_folders = sorted(
        [f for f in strategy_folder.glob("optimal_*") if f.name != "optimal_seed" and f.is_dir()],
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )

    for folder in optimal_folders:
        if all((folder / f).exists() for f in required_files):
            return folder

    # Fall back to optimal_seed
    seed_folder = strategy_folder / "optimal_seed"
    if seed_folder.exists() and all((seed_folder / f).exists() for f in required_files):
        return seed_folder

    raise ValueError(f"No valid baseline found in {strategy_folder}")


def cleanup_intermediate_folders(strategy_folder: Path) -> None:
    """
    Remove intermediate_* folders after successful optimization.

    Args:
        strategy_folder (Path): Path to strategy folder
    """
    logger = get_logger()
    for folder in strategy_folder.glob("intermediate_*"):
        if folder.is_dir():
            shutil.rmtree(folder)
            logger.debug(f"Cleaned up: {folder.name}")


def main():
    """
    Main entry point for draft order loop simulation CLI.

    Loops through all draft order strategy files, running iterative optimization
    for each one with dedicated per-strategy config folders.
    """
    # Initialize logging
    setup_logger(LOG_NAME, LOGGING_LEVEL, LOGGING_TO_FILE, LOGGING_FILE, LOGGING_FORMAT)
    logger = get_logger()

    # Create argument parser
    parser = argparse.ArgumentParser(
        description="Loop through draft order strategies, running iterative optimization for each",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run with default settings
  python run_draft_order_loop.py

  # Run with more simulations per config
  python run_draft_order_loop.py --sims 100

  # Use ProcessPoolExecutor for true parallelism
  python run_draft_order_loop.py --use-processes

  # Custom workers and test values
  python run_draft_order_loop.py --workers 16 --test-values 50
        """
    )

    parser.add_argument('--sims', type=int, default=DEFAULT_SIMS,
                        help=f'Number of simulations per config (default: {DEFAULT_SIMS})')
    parser.add_argument('--workers', type=int, default=DEFAULT_WORKERS,
                        help=f'Number of parallel workers (default: {DEFAULT_WORKERS})')
    parser.add_argument('--data', type=str, default=DEFAULT_DATA,
                        help=f'Path to simulation data folder (default: {DEFAULT_DATA})')
    parser.add_argument('--test-values', type=int, default=DEFAULT_TEST_VALUES,
                        help=f'Number of test values per parameter (default: {DEFAULT_TEST_VALUES})')
    parser.add_argument('--use-processes', action='store_true', default=False,
                        help='Use ProcessPoolExecutor for true parallelism (bypasses GIL)')

    args = parser.parse_args()

    # Set up paths
    data_folder = Path(args.data)
    config_dir = Path("simulation/simulation_configs")
    strategies_dir = config_dir / "strategies"
    strategies_dir.mkdir(parents=True, exist_ok=True)
    progress_file = strategies_dir / "loop_progress.json"

    # Find root baseline (error if none)
    root_baseline = find_latest_optimal_folder(config_dir)
    if not root_baseline:
        logger.error("No optimal_* folders found in simulation/simulation_configs/")
        logger.error("Please run 'python run_simulation.py iterative' first to create a baseline.")
        sys.exit(1)

    logger.info(f"Using root baseline: {root_baseline.name}")

    # Validate data folder
    draft_order_dir = data_folder / "draft_order_possibilities"
    if not draft_order_dir.exists():
        logger.error(f"Draft order directory not found: {draft_order_dir}")
        sys.exit(1)

    # Discover draft order files
    draft_files = discover_draft_order_files(draft_order_dir)
    if not draft_files:
        logger.error("No draft order files found")
        sys.exit(1)

    logger.info(f"Found {len(draft_files)} draft order strategies")

    # Find resume point
    start_idx, action, current_cycle = find_resume_point(draft_files, strategies_dir, data_folder)
    logger.info(f"Resuming at cycle {current_cycle}, strategy index {start_idx} ({action})")

    # Display configuration
    executor_type = "ProcessPoolExecutor" if args.use_processes else "ThreadPoolExecutor"
    logger.info("=" * 80)
    logger.info("DRAFT ORDER LOOP SIMULATION")
    logger.info("=" * 80)
    logger.info(f"Simulations per config: {args.sims}")
    logger.info(f"Workers: {args.workers} ({executor_type})")
    logger.info(f"Test values per parameter: {args.test_values}")
    logger.info(f"Strategies directory: {strategies_dir}")
    logger.info("=" * 80)

    # Endless loop
    while True:
        # Process strategies from resume point to end
        for idx in range(start_idx, len(draft_files)):
            file_num = draft_files[idx]
            strategy_name = get_strategy_name(file_num, data_folder)
            strategy_folder = strategies_dir / strategy_name

            logger.info("=" * 80)
            logger.info(f"OPTIMIZING STRATEGY: {strategy_name} (cycle {current_cycle}, {idx + 1}/{len(draft_files)})")
            logger.info("=" * 80)

            # Ensure strategy folder exists and is valid (seed if needed)
            ensure_strategy_folder(strategy_folder, root_baseline, file_num, data_folder)

            # Determine baseline for this run (most recent optimal_* in strategy folder)
            baseline = get_strategy_baseline(strategy_folder)
            logger.info(f"Using baseline: {baseline.name}")

            # Run iterative optimization for this strategy
            # (DRAFT_ORDER already in config files from seeding)
            manager = SimulationManager(
                baseline_config_path=baseline,
                output_dir=strategy_folder,
                num_simulations_per_config=args.sims,
                num_test_values=args.test_values,
                max_workers=args.workers,
                data_folder=data_folder,
                num_parameters_to_test=NUM_PARAMETERS_TO_TEST,
                use_processes=args.use_processes,
                auto_update_league_config=False  # Don't update root data/configs
            )
            manager.run_iterative_optimization()

            # Clean up intermediate folders after successful completion
            cleanup_intermediate_folders(strategy_folder)

            # Update progress tracker
            update_progress(progress_file, last_completed=idx, cycle=current_cycle)
            logger.info(f"Completed optimization for {strategy_name}")

        # All strategies complete for this cycle
        logger.info("=" * 80)
        logger.info(f"Cycle {current_cycle} complete. Starting cycle {current_cycle + 1}...")
        logger.info("=" * 80)
        current_cycle += 1
        start_idx = 0  # Reset to first strategy for new cycle


if __name__ == "__main__":
    main()
