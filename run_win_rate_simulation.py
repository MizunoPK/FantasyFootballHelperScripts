"""
Win Rate Simulation Runner

Entry point for running win rate simulations across all draft strategies.

Author: Kai Mizuno
"""

import argparse
import sys
from pathlib import Path

from utils.LoggingManager import setup_logger, get_logger
from simulation.win_rate.WinRateMetaDataManager import WinRateMetaDataManager
from simulation.win_rate.DraftStrategyOrchestrator import DraftStrategyOrchestrator

LOG_NAME = "win_rate_simulation"


def _build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser for the win-rate simulation runner."""
    parser = argparse.ArgumentParser(
        description="Win rate simulation runner — iterates all draft strategies and tracks best win rates. "
                    "Must be run from the project root directory."
    )
    parser.add_argument(
        "--sims", type=int, default=10, metavar="N",
        help="Number of simulations per season per strategy (default: 10)"
    )
    parser.add_argument(
        "--workers", type=int, default=8, metavar="N",
        help="Max parallel worker threads for ParallelLeagueRunner (default: 8)"
    )
    parser.add_argument(
        "--endless", action="store_true",
        help="Run continuously until KeyboardInterrupt"
    )
    parser.add_argument(
        "--data", type=str, default="simulation/sim_data", metavar="PATH",
        help="Path to simulation data root folder (default: simulation/sim_data)"
    )
    parser.add_argument(
        "--log-level", type=str, default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging verbosity (default: INFO)"
    )
    parser.add_argument(
        "--enable-log-file", action="store_true",
        help="Enable logging to file (default: console only)"
    )
    parser.add_argument(
        "--strategy", type=str, default=None, metavar="FILENAME",
        help="Run only the named strategy file (exact basename match, e.g., '1_zero_rb.json'). Default: run all strategies."
    )
    return parser


def _print_summary(meta_data_manager: WinRateMetaDataManager) -> None:
    """Print a ranked, table-formatted summary of strategy win rates to stdout."""
    strategies = meta_data_manager.get_all_strategies()
    if not strategies:
        print("No strategies evaluated yet.")
        return
    sorted_entries = sorted(
        strategies.items(),
        key=lambda kv: kv[1].get("best_win_rate", 0.0),
        reverse=True,
    )
    print("\nStrategy Win Rate Summary")
    print("──────────────────────────────────────────────────────────────")
    print("Rank  Strategy Name              Win Rate  Cumul.  Runs  Last Run")
    print("────  ─────────────────────────  ────────  ──────  ────  ──────────")
    for rank, (_, entry) in enumerate(sorted_entries, 1):
        total_games = entry.get("total_games", 0)
        total_wins = entry.get("total_wins", 0)
        cumulative = total_wins / total_games if total_games > 0 else 0.0
        print(
            f"{rank:>4}  {entry['name']:<25}  "
            f"{entry.get('best_win_rate', 0.0):>8.3f}  "
            f"{cumulative:>6.3f}  "
            f"{entry['total_runs']:>4}  "
            f"{entry.get('last_run', 'N/A')}"
        )
    print("──────────────────────────────────────────────────────────────")


def main() -> None:
    """
    Entry point for win rate simulation runner.

    Parses CLI arguments, initializes WinRateMetaDataManager and
    DraftStrategyOrchestrator once, then runs one or more passes
    through all 51 strategy files.
    """
    args = _build_parser().parse_args()

    setup_logger(LOG_NAME, args.log_level, args.enable_log_file, None, "standard")
    logger = get_logger()

    data_folder = Path(args.data)
    meta_data_manager = WinRateMetaDataManager(data_folder / "win_rate_meta_data.json")
    orchestrator = DraftStrategyOrchestrator(
        data_folder=data_folder,
        num_simulations=args.sims,
        max_workers=args.workers,
        meta_data_manager=meta_data_manager,
        strategy_filter=args.strategy,
    )

    pass_num = 0
    try:
        if args.endless:
            while True:
                pass_num += 1
                logger.info(f"--- Endless pass {pass_num} starting ---")
                orchestrator.run()
                _print_summary(meta_data_manager)
        else:
            orchestrator.run()
    except KeyboardInterrupt:
        logger.info("Received interrupt — exiting after current strategy")
        _print_summary(meta_data_manager)
        sys.exit(0)
    except FileNotFoundError as e:
        logger.error(str(e))
        sys.exit(1)

    _print_summary(meta_data_manager)


if __name__ == "__main__":
    main()

