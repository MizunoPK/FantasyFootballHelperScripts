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
from simulation.win_rate.SweepTournament import SweepTournament, DEFAULT_EPSILON
from simulation.win_rate.config_overrides import extract_draft_param_values
from simulation.win_rate.sweep_summary import rank_combinations, format_summary, write_sweep_report
from simulation.win_rate.config_promoter import promote_best_combination
from utils.error_handler import ConfigurationError, FileOperationError

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
        "--num-values", type=int, default=5, metavar="N",
        help="Candidate grid density per draft-side parameter for the sweep (default: 5). Sweep mode only."
    )
    parser.add_argument(
        "--promote", action="store_true",
        help="Promote the best-ranked sweep combination into data/configs/league_config.json. "
             "Alone: promote from the existing sweep results. With --sweep: run the sweep, then promote "
             "its winner. Incompatible with --endless."
    )
    parser.add_argument(
        "--fresh", action="store_true",
        help="Ignore any existing sweep checkpoint and run every config from baseline. Sweep mode only."
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

    if args.promote and args.endless:
        logger.error(
            "--promote cannot be combined with --endless: an endless sweep never "
            "terminates to promote. Run the sweep, then --promote separately."
        )
        sys.exit(2)

    if args.sweep:
        _run_sweep_mode(args, data_folder, logger)
        if args.promote:
            _run_promote_mode(data_folder, logger)
        return

    if args.promote:
        _run_promote_mode(data_folder, logger)
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
    """Run the multi-parameter sweep: tournament with per-config convergence as the stopping rule."""
    triples, _ = load_valid_strategies(data_folder)        # raises FileNotFoundError if none -> caught by main
    if not triples:
        logger.error("No valid strategies found for sweep")
        sys.exit(1)
    strategies = [(filename, draft_order) for filename, draft_order, _ in triples]

    evaluator = CombinationEvaluator(
        data_folder=data_folder, num_simulations=args.sims, max_workers=args.workers
    )
    baseline_params = extract_draft_param_values(evaluator.base_config)
    store = SweepResultsManager(data_folder / "win_rate_sweep_results.json")

    # Auto-resume decision (D1/D2/D4): recompute the input fingerprint with the shared
    # DEFAULT_EPSILON and string-compare it to the stored one. --fresh, an empty stored
    # digest, or a mismatch -> no resume (run every config from baseline).
    strategy_ids = [filename for filename, _ in strategies]
    fp_now = SweepResultsManager.compute_input_fingerprint(
        strategy_ids, baseline_params, args.num_values, DEFAULT_EPSILON
    )
    if args.fresh:
        resume = False
    else:
        stored = store.get_input_fingerprint()
        if stored == "":
            resume = False
        elif stored == fp_now:
            resume = True
        else:
            logger.warning(
                "Sweep inputs changed since last checkpoint (fingerprint mismatch) — "
                "discarding stale checkpoint and starting fresh."
            )
            resume = False
    if resume:
        if store.is_all_converged(strategy_ids):
            logger.info(
                f"Sweep already complete — all {len(strategy_ids)} configs converged; "
                "nothing to do."
            )
        else:
            converged = [
                sid for sid in strategy_ids
                if (store.get_config_convergence(sid) or {}).get("status") == "converged"
            ]
            in_progress = [
                sid for sid in strategy_ids
                if (store.get_config_convergence(sid) or {}).get("status") == "in_progress"
            ]
            not_started = [
                sid for sid in strategy_ids if store.get_config_convergence(sid) is None
            ]
            resuming_id = in_progress[0] if in_progress else "(none)"
            logger.info(
                f"Resuming sweep: {len(converged)} configs already converged (skipped), "
                f"resuming config {resuming_id} from checkpoint; {len(not_started)} not yet started."
            )
    # Refresh the stored fingerprint on every launch (D1) so a fresh / input-changed file
    # records the current inputs.
    store.set_input_fingerprint(fp_now)
    tournament = SweepTournament(evaluator, store, num_values=args.num_values)

    pass_num = 0
    try:
        while True:
            pass_num += 1
            if args.endless:
                logger.info(f"--- Endless sweep pass {pass_num} starting ---")
            tournament.run(strategies, baseline_params, resume=resume)
            resume = False  # endless passes 2+ are always full fresh passes
            ranked = rank_combinations(store.get_all_combinations())
            print(format_summary(ranked))
            write_sweep_report(ranked, data_folder)
            if not args.endless:
                break
    except KeyboardInterrupt:
        logger.info("Received interrupt — exiting after current pass")
        ranked = rank_combinations(store.get_all_combinations())
        print(format_summary(ranked))
        write_sweep_report(ranked, data_folder)
        sys.exit(0)


def _run_promote_mode(data_folder: Path, logger) -> None:
    """Promote the best sweep combination into league_config.json and report the result."""
    store = SweepResultsManager(data_folder / "win_rate_sweep_results.json")
    try:
        result = promote_best_combination(store, data_folder)
    except (ConfigurationError, FileOperationError) as e:
        logger.error(f"Promotion failed: {e}")
        sys.exit(1)
    _print_promotion(result)


def _print_promotion(result: dict) -> None:
    """Print a human-readable report of what was promoted to league_config.json."""
    print("\nPromoted best combination to data/configs/league_config.json")
    print("──────────────────────────────────────────────────────────────")
    print(f"  Strategy:  {result['strategy_id']}")
    print(f"  Win rate:  {result['win_rate']:.3f} over {result['games']} games")
    print("  Parameters:")
    for name, value in result["param_values"].items():
        print(f"    {name}: {value}")
    print("──────────────────────────────────────────────────────────────")


if __name__ == "__main__":
    main()

