"""
Win Rate Simulation Runner

Entry point for running win rate simulations across all draft strategies.

Author: Kai Mizuno
"""

import argparse
import random
import sys
from pathlib import Path

from utils.LoggingManager import setup_logger, get_logger
from simulation.win_rate.WinRateMetaDataManager import WinRateMetaDataManager
from simulation.win_rate.DraftStrategyOrchestrator import DraftStrategyOrchestrator
from simulation.win_rate.strategy_loader import load_valid_strategies
from simulation.win_rate.CombinationEvaluator import CombinationEvaluator
from simulation.win_rate.SimulatedLeague import WEEKS_PER_SEASON
from simulation.win_rate.SweepResultsManager import SweepResultsManager
from simulation.win_rate.SweepTournament import (
    SweepTournament,
    DEFAULT_CONFIDENCE,
    DEFAULT_MIN_EFFECT_SIZE,
    DEFAULT_MIN_GAMES,
)
from simulation.shared.ProgressTracker import ProgressTracker
from simulation.win_rate.config_overrides import extract_draft_param_values
from simulation.win_rate.sweep_summary import rank_combinations, format_summary, write_sweep_report
from simulation.win_rate.config_promoter import (
    compute_promotion,
    promote_best_combination,
    DEFAULT_PROMOTE_SHORTLIST,
    DEFAULT_PROMOTE_SIMS,
)
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
        help="Run the multi-parameter sweep (strategy + 6 draft-side params) instead of strategy-only mode."
    )
    parser.add_argument(
        "--num-values", type=int, default=5, metavar="N",
        help="Candidate grid density per draft-side parameter for the sweep (default: 5). Sweep mode only."
    )
    parser.add_argument(
        "--promote", action="store_true",
        help="Preview promoting the best-ranked sweep combination into data/configs/league_config.json "
             "(DRY RUN by default — prints the current -> proposed diff and writes nothing). "
             "Alone: preview from the existing sweep results. With --sweep: run the sweep, then preview "
             "its winner. Add --confirm to actually write. Incompatible with --endless."
    )
    parser.add_argument(
        "--confirm", action="store_true",
        help="Required alongside --promote to actually WRITE data/configs/league_config.json. "
             "Without --confirm, --promote only previews the change (behavior change: a bare --promote "
             "no longer writes). Safe in non-TTY/scripted runs — the flag, not a prompt, is the write gate."
    )
    parser.add_argument(
        "--promote-shortlist", type=int, default=DEFAULT_PROMOTE_SHORTLIST, metavar="N",
        help=f"How many top-ranked sweep candidates --promote re-measures head-to-head on "
             f"fresh data before promoting one (default: {DEFAULT_PROMOTE_SHORTLIST}). Cost "
             f"scales linearly: each candidate replays 2 arms x every season x --promote-sims. "
             f"Use 1 for a fast bounded run."
    )
    parser.add_argument(
        "--promote-sims", type=int, default=DEFAULT_PROMOTE_SIMS, metavar="N",
        help=f"Simulations per season per arm for each --promote re-measurement "
             f"(default: {DEFAULT_PROMOTE_SIMS}). At the defaults a promote is a deliberate "
             f"long-running operator action (tens of minutes); use 1 for a fast bounded run."
    )
    parser.add_argument(
        "--fresh", action="store_true",
        help="Ignore any existing sweep checkpoint and run every config from baseline. Sweep mode only."
    )
    parser.add_argument(
        "--naive-opponents", action="store_true",
        help="Use the legacy naive-opponent composition (1 DraftHelperTeam + 9 SimulatedOpponents) "
             "instead of the default self-play field (10 DraftHelperTeams). Reproduces the prior ~0.84 baseline."
    )
    parser.add_argument(
        "--seed", type=int, default=None, metavar="N",
        help="Base seed for deterministic evaluation (T29). With --seed N, repeated runs with "
             "identical inputs produce identical win-rate aggregates. Omit to use OS entropy "
             "(default stochastic behavior, unchanged from prior runs)."
    )
    return parser


def _cumulative_rate(entry: dict) -> float:
    """Cumulative win rate (total_wins / total_games) of one strategy entry; 0.0 at zero games.

    Args:
        entry (dict): A WinRateMetaDataManager per-strategy entry.

    Returns:
        float: The cumulative rate, or 0.0 when no games are recorded.
    """
    total_games = entry.get("total_games", 0)
    if total_games <= 0:
        return 0.0
    return entry.get("total_wins", 0) / total_games


def _print_summary(meta_data_manager: WinRateMetaDataManager) -> None:
    """Print a ranked, table-formatted summary of strategy win rates to stdout."""
    strategies = meta_data_manager.get_all_strategies()
    if not strategies:
        print("No strategies evaluated yet.")
        return
    # T62: rank on the CUMULATIVE rate, not the best_win_rate running single-run MAXIMUM —
    # a maximum over noisy runs is upward-biased and orders strategies by luck. This store is
    # written only by strategy-only mode (no moving incumbent), so its cumulative totals are
    # homogeneous and this ordering is unambiguously correct here. Only the sort key changes;
    # the displayed WinRate column still renders the stored best_win_rate, whose RENAME is
    # T32-relabel-best-winrate-diagnostic-store-and-report's territory, not this story's.
    sorted_entries = sorted(
        strategies.items(),
        key=lambda kv: _cumulative_rate(kv[1]),
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
            # The sweep's own seed is not plumbed out of _run_sweep_mode, and re-using it
            # would couple two independently reproducible phases — so promote resolves its
            # own. mode_label keeps the two auto-assign hints distinguishable.
            _run_promote_mode(
                data_folder, logger, confirm=args.confirm,
                seed=_resolve_sweep_seed(args, logger, mode_label="promote"),
                shortlist=args.promote_shortlist, sims=args.promote_sims,
            )
        return

    if args.promote:
        _run_promote_mode(
            data_folder, logger, confirm=args.confirm,
            seed=_resolve_sweep_seed(args, logger, mode_label="promote"),
            shortlist=args.promote_shortlist, sims=args.promote_sims,
        )
        return

    meta_data_manager = WinRateMetaDataManager(data_folder / "win_rate_meta_data.json")
    orchestrator = DraftStrategyOrchestrator(
        data_folder=data_folder,
        num_simulations=args.sims,
        max_workers=args.workers,
        meta_data_manager=meta_data_manager,
        strategy_filter=args.strategy,
        naive_opponents=args.naive_opponents,
        seed=args.seed,
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


def _resolve_sweep_seed(args: argparse.Namespace, logger, mode_label: str = "sweep") -> int:
    """Resolve the base seed for a sweep run (D2/T30: paired-by-default + reproducible).

    With ``--seed N`` the value is returned verbatim. Without ``--seed`` a base seed is
    auto-assigned from OS entropy and logged with a reproduce hint. A fixed base seed makes
    the coordinate-ascent trial-vs-current comparison paired (common random numbers) via
    T29's config-independent per-task seeding, so the variance of their difference collapses
    while the run stays reproducible by re-supplying the logged value.

    Args:
        args (argparse.Namespace): Parsed CLI args; reads ``args.seed`` (Optional[int]).
        logger: Logger used to emit the auto-assign reproduce hint at INFO.
        mode_label (str): Names the phase in the auto-assign log line (default "sweep").
            Promote mode passes "promote" so that a combined ``--sweep --promote`` run, in
            which the sweep and the promote each resolve their OWN seed, emits two
            DISTINGUISHABLE reproduce hints rather than two lines that read as a
            contradiction. The default keeps every existing caller's message byte-identical.

    Returns:
        int: The base seed to use for the run.
    """
    if args.seed is not None:
        return args.seed
    base_seed = random.SystemRandom().randrange(2 ** 32)
    logger.info(
        f"Auto-assigned {mode_label} base seed: {base_seed} "
        f"(re-run with --seed {base_seed} to reproduce)"
    )
    return base_seed


def _run_sweep_mode(args: argparse.Namespace, data_folder: Path, logger) -> None:
    """Run the multi-parameter sweep: tournament with per-config convergence as the stopping rule."""
    triples, _ = load_valid_strategies(data_folder)        # raises FileNotFoundError if none -> caught by main
    if not triples:
        logger.error("No valid strategies found for sweep")
        sys.exit(1)
    strategies = [(filename, draft_order) for filename, draft_order, _ in triples]

    # D2/T30: resolve the run's base seed. A fixed base seed makes the coordinate-ascent
    # trial-vs-current comparison paired (common random numbers) via T29's config-independent
    # per-task seeding, so the variance of their difference collapses. Without --seed, a base
    # seed is auto-assigned and logged so the paired run stays reproducible by re-supplying it.
    base_seed = _resolve_sweep_seed(args, logger)
    evaluator = CombinationEvaluator(
        data_folder=data_folder, num_simulations=args.sims, max_workers=args.workers,
        naive_opponents=args.naive_opponents, seed=base_seed
    )

    # T61/D1: games-per-evaluation reachability pre-flight, run BEFORE any evaluation and at
    # zero simulation cost. Every simulated league plays a fixed WEEKS_PER_SEASON-week schedule
    # and each week result is counted as exactly one win or one loss, so a single evaluation
    # yields exactly WEEKS_PER_SEASON x --sims x valid-season-count games. Post-T58 that product
    # IS the adoption gate's operand, so when it is below the floor the gate can never fire for
    # any trial: no parameter can ever be adopted and (pre-T61) every config was recorded as
    # "converged" at its baseline, which then short-circuited every later resume.
    # T61/D2: log loudly at ERROR and CONTINUE — the codebase's convention for a
    # result-invalidating but non-fatal condition (CombinationEvaluator.evaluate's dropped-league
    # ERROR, ParallelLeagueRunner's drop ERROR); sys.exit here would refuse the documented
    # --sweep --sims 1 bounded-smoke practice. Correctness is restored by the "starved"
    # disposition below, not by refusing to run.
    season_count = evaluator.season_count
    games_per_evaluation = WEEKS_PER_SEASON * args.sims * season_count
    if games_per_evaluation < DEFAULT_MIN_GAMES:
        if season_count == 0:
            # T61: reachable (folders present but none pass SimDataLoader validation) and the
            # only divide-by-zero trap here — no --sims value can clear a zero product, so the
            # minimum-sims term is undefined and the season-folder lever is named alone.
            remedy = (
                f"no valid season data was loaded, so raising the simulation count cannot help — "
                f"add or repair season folders (20XX/) under --data {data_folder}"
            )
        else:
            # Ceiling division without importing math: -(-a // b).
            min_sims = -(-DEFAULT_MIN_GAMES // (WEEKS_PER_SEASON * season_count))
            remedy = (
                f"raise --sims to at least {min_sims}, or add season folders under "
                f"--data {data_folder}"
            )
        logger.error(
            f"Sweep starved: {games_per_evaluation} games per evaluation "
            f"({WEEKS_PER_SEASON} weeks x {args.sims} sims x {season_count} valid season(s)) "
            f"is below the adoption gate's minimum of {DEFAULT_MIN_GAMES}. No candidate can "
            f"clear the gate, so no parameter can be adopted and no config can be tuned; every "
            f"config will be recorded as 'starved', not 'converged'. Remedy: {remedy}."
        )

    baseline_params = extract_draft_param_values(evaluator.base_config)
    # T57/D3/D4: hand the store THIS run's opponent regime so _load can quarantine-and-restart
    # a store accumulated under the OTHER regime (a different estimand) BEFORE any reader can
    # observe it. args.naive_opponents is in scope from the top of this function, so no
    # statement reordering is required — fp_now stays exactly where it is. _run_promote_mode
    # passes nothing and keeps the default (None => the regime trigger is inert there).
    store = SweepResultsManager(
        data_folder / "win_rate_sweep_results.json",
        expected_naive_opponents=args.naive_opponents,
    )

    # Auto-resume decision (D1/D2/D4): recompute the input fingerprint with the shared
    # significance-gate constants and string-compare it to the stored one. --fresh, an empty
    # stored digest, or a mismatch -> no resume (run every config from baseline).
    strategy_ids = [filename for filename, _ in strategies]
    fp_now = SweepResultsManager.compute_input_fingerprint(
        strategy_ids, baseline_params, args.num_values,
        DEFAULT_CONFIDENCE, DEFAULT_MIN_EFFECT_SIZE, DEFAULT_MIN_GAMES, base_seed,
        args.naive_opponents
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
            # T57/D5: this branch does NOT archive anything — under T57/D4 only an
            # opponent-regime change quarantines, and that happens earlier at LOAD time with
            # its own WARNING. Under the unseeded default this branch is the COMMON case
            # (a fresh auto-seed every run), so say what is true: not resuming, re-tuning
            # every config from baseline, accumulated evidence RETAINED.
            logger.warning(
                "Sweep inputs changed since last checkpoint (fingerprint mismatch) — not "
                "resuming; every config will be re-tuned from baseline. The accumulated "
                "evidence in the store is retained (a store is archived only when the "
                "opponent regime changes)."
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
            # T61/D4: starved entries belong to none of the three buckets above, so without this
            # they would silently vanish from the breakdown and the counts would not add up.
            starved = [
                sid for sid in strategy_ids
                if (store.get_config_convergence(sid) or {}).get("status") == "starved"
            ]
            resuming_id = in_progress[0] if in_progress else "(none)"
            logger.info(
                f"Resuming sweep: {len(converged)} configs already converged (skipped), "
                f"resuming config {resuming_id} from checkpoint; {len(not_started)} not yet "
                f"started; {len(starved)} starved (re-tuned from baseline)."
            )
    # Refresh the stored fingerprint on every launch (D1) so a fresh / input-changed file
    # records the current inputs.
    store.set_input_fingerprint(fp_now)
    # T54/D3: certify this store as produced under the discriminating (measured-vs-incumbent)
    # regime so config_promoter allows a promote from it (a flagless store is fail-safe blocked).
    store.set_discriminating(True)
    # T57/D8: record the opponent regime this store accumulates its evidence under, so a later
    # launch under the OTHER regime quarantines instead of blending two estimands. Written on
    # EVERY launch (one more atomic save on a path that already performs two), so an unmarked
    # pre-T57 store self-heals after a single run.
    store.set_naive_opponents(args.naive_opponents)
    # T61/D3: hand the tournament the RAW pre-flight count (not a boolean), so it decides the
    # terminal disposition against its OWN min_games rather than trusting the driver's floor.
    tournament = SweepTournament(
        evaluator, store, num_values=args.num_values,
        games_per_evaluation=games_per_evaluation,
    )

    # T16/KDD-4: detect once whether stdout is a TTY. TTY -> a redrawing ProgressTracker bar;
    # non-TTY (piped / backgrounded / --enable-log-file) -> periodic full-line INFO log lines,
    # so a log file is not spammed with carriage-return partial rewrites.
    is_tty = sys.stdout.isatty()

    pass_num = 0
    carry_over = None  # T10/D3: None on pass 1 (resume governs); built from converged params for passes 2+
    try:
        while True:
            pass_num += 1
            if args.endless:
                logger.info(f"--- Endless sweep pass {pass_num} starting ---")
                print(f"=== Endless sweep pass {pass_num} ===")  # T10/D2: header before the per-pass table
            # T16/KDD-1+KDD-4: on a TTY, a FRESH per-pass ProgressTracker bar (so endless mode
            # resets cleanly each pass; total = configs in the pass). Off a TTY we build NO
            # tracker — progress is plain full-line INFO logs via a per-pass counter — so piped /
            # --enable-log-file output stays logger-lines-only with no ProgressTracker stdout banner.
            total = len(strategies)
            tracker = ProgressTracker(total=total, description="Configs") if is_tty else None
            logged = 0  # off-TTY per-config counter (the bar owns the count on a TTY)

            def progress_cb(strategy_id: str) -> None:
                """Per-config progress signal: advance the bar (TTY) or log a line (non-TTY)."""
                nonlocal logged
                if is_tty:
                    tracker.update()
                else:
                    logged += 1
                    logger.info(f"config {logged}/{total} ({strategy_id})")

            tournament.run(
                strategies, baseline_params, resume=resume, carry_over_seeds=carry_over,
                progress_callback=progress_cb,
            )
            if is_tty:
                tracker.finish()
            resume = False  # endless passes 2+ are always full fresh passes (carry-over governs them)
            if args.endless:
                # T10/D1: build the next pass's per-config seed map from the store's converged
                # params (continue-from-converged); configs without an entry fall back to baseline.
                # Single pass with a local `conv` so get_config_convergence is called once per id.
                carry_over = {}
                for sid in strategy_ids:
                    conv = store.get_config_convergence(sid)
                    if conv:
                        carry_over[sid] = dict(conv["best_param_values"])
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


def _run_promote_mode(data_folder: Path, logger, confirm: bool, seed: int,
                      shortlist: int, sims: int) -> None:
    """Preview or (with confirm=True) write the re-measured winning combination.

    The human-approval gate in front of the live-config write (T34). With confirm=False
    (a bare --promote) this computes and prints the current -> proposed preview and writes
    nothing; with confirm=True (--promote --confirm) it performs the atomic write via
    promote_best_combination and prints the promotion report. The gate is the --confirm
    flag, not a TTY prompt, so scripted / non-TTY runs are safe and no path writes without
    --confirm.

    Both paths now RE-MEASURE the shortlisted candidates on fresh season data (T62), so both
    run simulations and are correspondingly slow at the default shortlist/sims. Every failure
    mode — including the re-measurement's own missing-season-data and no-valid-games cases —
    is surfaced as ConfigurationError and handled here.

    Args:
        data_folder (Path): Simulation data root holding the sweep results AND the 20XX/
            season folders the re-measurement replays.
        logger: Logger used to report a promotion failure before exiting.
        confirm (bool): True to write (--confirm supplied); False to preview only.
        seed (int): Base seed for the re-measurement (resolved by the caller via
            _resolve_sweep_seed, so an unseeded run logs a reproduce hint).
        shortlist (int): How many top-ranked candidates to re-measure (--promote-shortlist).
        sims (int): Simulations per season per arm per candidate (--promote-sims).
    """
    store = SweepResultsManager(data_folder / "win_rate_sweep_results.json")
    try:
        if confirm:
            result = promote_best_combination(
                store, data_folder, seed=seed, shortlist=shortlist, sims=sims
            )
            _print_promotion(result)
        else:
            plan = compute_promotion(
                store, data_folder, seed=seed, shortlist=shortlist, sims=sims
            )
            _print_promotion_preview(plan)
    except (ConfigurationError, FileOperationError) as e:
        logger.error(f"Promotion failed: {e}")
        sys.exit(1)


def _print_promotion_evidence(plan: dict) -> None:
    """Print the shared re-measurement evidence block for both promotion printers (T62).

    Ordering is the requirement, not a preference: the FRESH re-measured rate and its
    clustering-widened Wilson interval lead, labelled as the winner of a K-way
    re-measurement (K printed) so the residual max-over-K bias and the uncorrected K-fold
    multiplicity are visible; the delta and z sit beneath as the decision evidence, labelled
    so the absolute rate is not misread as the improvement; the store-derived rate comes
    LAST, explicitly labelled max_selected and stated not to be an estimate.

    Args:
        plan (dict): A compute_promotion / promote_best_combination result.
    """
    ci_low, ci_high = plan["remeasured_ci"]
    k = plan["shortlist_size"]
    print(f"  Strategy:  {plan['strategy_id']}")
    print(f"  Re-measured win rate:  {plan['remeasured_rate']:.3f} "
          f"[{ci_low:.3f}, {ci_high:.3f}]  over {plan['remeasured_games']} games/arm")
    print(f"    winner of a {k}-way re-measurement on fresh data — NOT an unconditional "
          f"estimate of this config's rate")
    print(f"    interval widened for clustering; the {k} significance tests are uncorrected "
          f"for multiplicity")
    print(f"  Improvement vs live config:  delta={plan['delta']:+.4f}  "
          f"z={plan['z']:.2f}  z_adjusted={plan['z_adjusted']:.2f}")
    print(f"  Seed:  {plan['seed']}")
    print("  Parameters:")
    for name, value in plan["param_values"].items():
        print(f"    {name}: {value}")
    print(f"  max_selected (in-sample maximum — not an estimate):  "
          f"{plan['max_selected_win_rate']:.3f} over {plan['max_selected_games']} store "
          f"games, shortlist lcb={plan['lcb']:.3f}")


def _print_promotion(result: dict) -> None:
    """Print a human-readable report of what was promoted to league_config.json."""
    print("\nPromoted re-measured winner to data/configs/league_config.json")
    print("──────────────────────────────────────────────────────────────")
    _print_promotion_evidence(result)
    print("──────────────────────────────────────────────────────────────")


def _print_promotion_preview(plan: dict) -> None:
    """Print the current -> proposed promotion diff WITHOUT writing (bare --promote).

    The dry-run preview for the human-approval gate (T34): shows the re-measurement evidence
    for the winning candidate, then the current -> proposed diff of the changed draft-side
    keys (plus DRAFT_ORDER when it changes), then the apply hint. Nothing is written to
    data/configs/league_config.json.
    """
    print("\nPromotion preview (DRY RUN) — data/configs/league_config.json NOT modified")
    print("──────────────────────────────────────────────────────────────")
    _print_promotion_evidence(plan)
    diff = plan["diff"]
    if not diff:
        print("  No changes — the live config already matches the winning combination.")
    else:
        print("  Proposed changes (current -> proposed):")
        for key, change in diff.items():
            print(f"    {key}: {change['current']} -> {change['proposed']}")
    print("──────────────────────────────────────────────────────────────")
    print("  Re-run with --promote --confirm to apply.")


if __name__ == "__main__":
    main()

