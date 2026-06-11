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
from simulation.win_rate.strategy_loader import load_valid_strategies
from simulation.win_rate.CombinationEvaluator import CombinationEvaluator
from simulation.win_rate.SweepResultsManager import SweepResultsManager
from simulation.win_rate.SweepTournament import SweepTournament
from simulation.win_rate.config_overrides import extract_draft_param_values
from simulation.win_rate.budget_sizing import measure_unit_cost, compute_sizing
from simulation.win_rate.sweep_summary import rank_combinations, format_summary

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
    """Win rate sim uses ThreadPoolExecutor (I/O-bound — disk reads dominate); accuracy sim uses ProcessPoolExecutor (CPU-bound — score computation dominates). Use --workers to tune thread parallelism. ProcessPoolExecutor (use_processes=True on ParallelLeagueRunner) is available but adds process-creation overhead."""
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
    parser.add_argument(
        "--sweep", action="store_true",
        help="Run the multi-parameter sweep (strategy + 7 draft-side params) instead of strategy-only mode."
    )
    parser.add_argument(
        "--budget-hours", type=float, default=8.0, metavar="H",
        help="Overnight wall-time budget for a sweep pass in hours (default: 8.0). Sweep mode only."
    )
    parser.add_argument(
        "--top-n", type=int, default=20, metavar="N",
        help="Number of top combinations to show in the sweep summary (default: 20). Sweep mode only."
    )
    parser.add_argument(
        "--calib-sims", type=int, default=2, metavar="N",
        help="Simulations used for the per-sim cost calibration before a sweep (default: 2). Sweep mode only."
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

    if args.sweep:
        _run_sweep_mode(args, data_folder, logger)
        return

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


def _run_sweep_mode(args: argparse.Namespace, data_folder: Path, logger) -> None:
    """Run the multi-parameter sweep: calibrate -> size -> tournament -> ranked summary."""
    triples, _ = load_valid_strategies(data_folder)        # raises FileNotFoundError if none -> caught by main
    if not triples:
        logger.error("No valid strategies found for sweep")
        sys.exit(1)
    strategies = [(filename, draft_order) for filename, draft_order, _ in triples]

    calib = CombinationEvaluator(
        data_folder=data_folder, num_simulations=args.calib_sims, max_workers=args.workers
    )
    baseline_params = extract_draft_param_values(calib.base_config)
    unit_cost = measure_unit_cost(calib, strategies[0][1], baseline_params, args.calib_sims)

    sizing = compute_sizing(unit_cost, num_strategies=len(strategies),
                            budget_seconds=args.budget_hours * 3600)
    logger.info(
        f"Sweep sizing: num_simulations={sizing['num_simulations']}, "
        f"num_values={sizing['num_values']}, estimated={sizing['estimated_seconds'] / 3600:.2f}h"
    )
    if not sizing["feasible"]:
        logger.warning(
            f"Sweep estimate ({sizing['estimated_seconds'] / 3600:.2f}h) exceeds the "
            f"{args.budget_hours:.1f}h budget even at the minimum sims — running at the floor; "
            "interrupt with Ctrl+C to stop."
        )

    evaluator = CombinationEvaluator(
        data_folder=data_folder, num_simulations=sizing["num_simulations"], max_workers=args.workers
    )
    store = SweepResultsManager(data_folder / "win_rate_sweep_results.json")
    tournament = SweepTournament(evaluator, store, num_values=sizing["num_values"])

    pass_num = 0
    try:
        while True:
            pass_num += 1
            if args.endless:
                logger.info(f"--- Endless sweep pass {pass_num} starting ---")
            tournament.run(strategies, baseline_params)
            print(format_summary(rank_combinations(store.get_all_combinations(), args.top_n)))
            if not args.endless:
                break
    except KeyboardInterrupt:
        logger.info("Received interrupt — exiting after current pass")
        print(format_summary(rank_combinations(store.get_all_combinations(), args.top_n)))
        sys.exit(0)


if __name__ == "__main__":
    main()

