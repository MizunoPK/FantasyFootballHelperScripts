"""
Accuracy Simulation Manager

Orchestrates accuracy simulation to find optimal scoring algorithm configurations.
Selection optimizes pairwise ranking accuracy (how often the config orders any two
players the same way their actual fantasy points do); MAE (Mean Absolute Error)
between calculated projected points and actual player performance is also computed,
but only as a reported diagnostic.

Mode:
- Weekly: Evaluates per-week projection accuracy
  - Optimizes week1-5.json, week6-9.json, week10-13.json, week14-17.json
  - Used for Starter Helper and Trade Simulator modes

Unlike win-rate simulation:
- No randomness (deterministic ranking-metric / MAE calculation, no random draws)
- Selection optimizes pairwise ranking accuracy (higher is better); MAE is a reported diagnostic
- Tests prediction parameters (PARAMETER_ORDER in run_accuracy_simulation.py) not strategy parameters

Selection optimizes pairwise ranking accuracy, NOT MAE — do not revert `is_better_than` to an
MAE comparison; the League Helper's decisions are ordinal. MAE is a reported diagnostic only.

Author: Kai Mizuno
"""

import re
import shutil
import signal
import tempfile
import time
import json
from pathlib import Path
from typing import Dict, FrozenSet, List, Optional, Tuple

from FantasyFootballHelperScriptsWorkspace.FantasyFootballHelperScripts.utils.LoggingManager import get_logger
from FantasyFootballHelperScriptsWorkspace.FantasyFootballHelperScripts.simulation.shared.ConfigGenerator import ConfigGenerator, DEFAULT_ACCURACY_SEED
from FantasyFootballHelperScriptsWorkspace.FantasyFootballHelperScripts.simulation.shared.ProgressTracker import ProgressTracker
from FantasyFootballHelperScriptsWorkspace.FantasyFootballHelperScripts.simulation.shared.config_cleanup import cleanup_accuracy_intermediate_folders
from FantasyFootballHelperScriptsWorkspace.FantasyFootballHelperScripts.simulation.shared.sim_data_coverage import excluded_weeks_by_season
from FantasyFootballHelperScriptsWorkspace.FantasyFootballHelperScripts.simulation.accuracy.AccuracyCalculator import AccuracyCalculator
from FantasyFootballHelperScriptsWorkspace.FantasyFootballHelperScripts.simulation.accuracy.AccuracyResultsManager import (
    AccuracyResultsManager,
    WEEK_RANGES,
    format_metric_pct,
    format_metric_corr,
)
from FantasyFootballHelperScriptsWorkspace.FantasyFootballHelperScripts.simulation.accuracy.horizon_labels import (
    HORIZON_COUNT,
    candidate_values_label,
    configs_per_param_label,
)

# T69/D1: safety bound on the ascent loop. This is a DELIBERATE DIVERGENCE from the port
# source: SweepTournament has no cap ("convergence is the sole stopping rule -- no
# wall-time, no pass cap"). T69 adds one because this story exists to replace a runner that
# never exited, and an uncapped loop would reproduce that defect under a new name.
#
# It is a safety net, NOT the stopping rule. Hitting it is reported distinctly and is never
# described as convergence -- a run that stopped because it ran out of passes has not
# settled, and conflating the two would hide the non-convergence the bound exists to
# surface. Coordinate ascent over a finite candidate grid normally settles in a few passes.
MAX_ASCENT_PASSES = 10

PAIRWISE_ACCURACY_WARN_THRESHOLD = 0.65
TOP_10_ACCURACY_WARN_THRESHOLD = 0.70


class AccuracySimulationManager:
    """
    Manages accuracy simulation for scoring algorithm optimization.

    Coordinates ConfigGenerator, AccuracyCalculator, and AccuracyResultsManager
    to test parameter combinations and identify optimal settings.

    Attributes:
        baseline_config_path (Path): Path to baseline configuration
        output_dir (Path): Directory to save results
        data_folder (Path): Path to sim_data folder
        config_generator (ConfigGenerator): Generates parameter combinations
        accuracy_calculator (AccuracyCalculator): Calculates MAE
        results_manager (AccuracyResultsManager): Tracks results
        logger: Logger instance
    """

    ORPHANED_DIR_MAX_AGE_HOURS = 24

    def __init__(
        self,
        baseline_config_path: Path,
        output_dir: Path,
        data_folder: Path,
        parameter_order: List[str],
        num_test_values: int = 5,
        num_parameters_to_test: int = 1,
        max_workers: int = 8,
        use_processes: bool = True,
        seed: int = DEFAULT_ACCURACY_SEED,
        exclude_low_coverage_weeks: bool = False
    ) -> None:
        """
        Initialize AccuracySimulationManager.

        Args:
            baseline_config_path (Path): Path to baseline configuration JSON
            output_dir (Path): Directory to save results
            data_folder (Path): Path to sim_data folder
            parameter_order (List[str]): List of parameter names defining optimization order
            num_test_values (int): Number of test values per parameter
            num_parameters_to_test (int): Number of parameters to test at once
            max_workers (int): Number of parallel workers for config evaluation
            use_processes (bool): Use ProcessPoolExecutor (True) or ThreadPoolExecutor (False)
            seed (int): Seed threaded into ConfigGenerator's private candidate-value RNG
                (default: DEFAULT_ACCURACY_SEED) so config selection is reproducible run-to-run.
            exclude_low_coverage_weeks (bool): When True, drop from the evaluation
                corpus every season-week the shared coverage owner reports below the
                per-week floor (D8.4). Default False — nothing is computed, nothing is
                logged, and the evaluation corpus is exactly today's.
        """
        self.logger = get_logger()
        self.logger.info("Initializing AccuracySimulationManager")

        self.baseline_config_path = baseline_config_path
        self.output_dir = output_dir
        self.data_folder = data_folder
        self.parameter_order = parameter_order
        self.num_test_values = num_test_values
        self.num_parameters_to_test = num_parameters_to_test

        self.max_workers = max_workers
        self.use_processes = use_processes
        self.parallel_runner = None
        self.progress_tracker = None

        self._current_optimal_config_path: Optional[Path] = None
        self._original_sigint_handler = None
        self._original_sigterm_handler = None

        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.config_generator = ConfigGenerator(
            baseline_config_path,
            num_test_values=num_test_values,
            seed=seed
        )
        self.accuracy_calculator = AccuracyCalculator()
        self.results_manager = AccuracyResultsManager(output_dir, baseline_config_path)

        self.available_seasons = self._discover_seasons()
        self.logger.info(
            f"Discovered {len(self.available_seasons)} historical seasons: "
            f"{[s.name for s in self.available_seasons]}"
        )

        # D8.4: the exclusion DECISION is a parent-side pre-pass, computed once
        # per run before any worker starts (HD1). With the flag off nothing is
        # computed and nothing is logged, so a default run is byte-identical.
        self.excluded_season_weeks: Dict[str, FrozenSet[int]] = (
            excluded_weeks_by_season(self.available_seasons)
            if exclude_low_coverage_weeks else {}
        )

        candidate_values = num_test_values + 1
        configs_per_param = candidate_values * HORIZON_COUNT
        self.logger.info(
            f"AccuracySimulationManager initialized: "
            f"{candidate_values_label(candidate_values)}; "
            f"{configs_per_param_label(candidate_values, configs_per_param)}"
        )

    def _sweep_orphaned_temp_dirs(self) -> None:
        """
        Delete stale accuracy_sim_* temp dirs from the system temp folder.

        Scans tempfile.gettempdir() for directories matching accuracy_sim_*
        that are older than ORPHANED_DIR_MAX_AGE_HOURS hours. Each stale
        directory is deleted with a warning log. Deletion failures are logged
        and skipped without aborting the sweep.
        """
        temp_root = Path(tempfile.gettempdir())
        current_time = time.time()
        threshold_seconds = self.ORPHANED_DIR_MAX_AGE_HOURS * 3600
        deleted_count = 0

        for candidate in temp_root.glob("accuracy_sim_*"):
            if not candidate.is_dir():
                continue
            try:
                mtime = candidate.stat().st_mtime
            except OSError as e:
                self.logger.warning(f"Could not stat orphaned temp dir candidate {candidate}: {e}")
                continue
            age_seconds = current_time - mtime
            if age_seconds > threshold_seconds:
                age_hours = age_seconds / 3600
                try:
                    shutil.rmtree(candidate)
                    self.logger.warning(
                        f"Deleted orphaned temp dir {candidate} (age: {age_hours:.1f}h)"
                    )
                    deleted_count += 1
                except OSError as e:
                    self.logger.warning(f"Failed to delete orphaned temp dir {candidate}: {e}")

        if deleted_count > 0:
            self.logger.info(
                f"Orphan sweep: deleted {deleted_count} stale accuracy_sim_* "
                f"temp dir(s) older than {self.ORPHANED_DIR_MAX_AGE_HOURS}h"
            )

    def _discover_seasons(self) -> List[Path]:
        """
        Find all valid historical season folders (20XX/) in data_folder.

        Returns:
            List[Path]: Sorted list of valid season folder paths
        """
        seasons = []
        for folder in self.data_folder.iterdir():
            if folder.is_dir() and folder.name.isdigit() and len(folder.name) == 4:
                weeks_folder = folder / "weeks"
                if weeks_folder.exists():
                    seasons.append(folder)

        if not seasons:
            raise ValueError(
                f"No valid season folders found in {self.data_folder}. "
                "Expected folders like '2024/' with 'weeks/' subfolder."
            )

        return sorted(seasons)

    def _setup_signal_handlers(self) -> None:
        """Set up signal handlers for graceful shutdown."""
        self._original_sigint_handler = signal.getsignal(signal.SIGINT)
        self._original_sigterm_handler = signal.getsignal(signal.SIGTERM)

        def graceful_shutdown(signum, frame):
            """Handle SIGINT/SIGTERM signals for graceful shutdown with current best config save."""
            self.logger.warning(f"Received signal {signum}, initiating graceful shutdown...")
            if self._current_optimal_config_path:
                self.logger.info(f"Current best config saved at: {self._current_optimal_config_path}")
            raise KeyboardInterrupt("Graceful shutdown requested")

        signal.signal(signal.SIGINT, graceful_shutdown)
        signal.signal(signal.SIGTERM, graceful_shutdown)

    def _restore_signal_handlers(self) -> None:
        """Restore original signal handlers."""
        if self._original_sigint_handler:
            signal.signal(signal.SIGINT, self._original_sigint_handler)
        if self._original_sigterm_handler:
            signal.signal(signal.SIGTERM, self._original_sigterm_handler)


    def _read_ascent_state(self, folder: Path) -> Tuple[int, set]:
        """Read T69/D5 ascent state from an intermediate folder.

        Args:
            folder (Path): The intermediate folder selected for resume.

        Returns:
            Tuple[int, set]: (pass_idx, frozen_horizons). Returns (0, set()) when the file
                is absent or unreadable -- a folder written before T69 has no ascent state,
                and losing the pass/frozen detail is far better than discarding the run's
                completed work or raising on it.
        """
        state_file = folder / '_ascent_state.json'
        if not state_file.exists():
            self.logger.debug(f"No ascent state in {folder.name}; resuming as pass 0, nothing frozen")
            return (0, set())
        try:
            with open(state_file, 'r') as f:
                data = json.load(f)
            return (int(data.get('pass_idx', 0)), set(data.get('frozen_horizons', [])))
        except (json.JSONDecodeError, OSError, TypeError, ValueError) as e:
            self.logger.warning(
                f"Could not read ascent state from {state_file.name} ({e}); "
                f"resuming as pass 0 with nothing frozen"
            )
            return (0, set())

    def _detect_resume_state(self, mode: str = 'weekly') -> Tuple[bool, int, Optional[Path], int, set]:
        """
        Detect if optimization should resume from a previous run.

        Scans the output directory for accuracy_intermediate_*/ folders and determines
        whether to resume optimization from where it left off or start fresh.

        Args:
            mode: 'weekly' or 'ros' - affects folder name pattern matching

        Returns:
            Tuple[bool, int, Optional[Path], int, set]: A tuple containing:
                - should_resume (bool): True if resuming, False if starting fresh
                - start_idx (int): Parameter index to start from (0 if starting fresh)
                - last_config_path (Optional[Path]): Path to last intermediate folder if resuming
                - pass_idx (int): T69/D5 -- ascent pass to resume at (0 if fresh or legacy)
                - frozen_horizons (set): T69/D5 -- horizons already converged (empty if fresh
                  or legacy). A pre-T69 intermediate folder carries no ascent state; that is
                  treated as "pass 0, nothing frozen" rather than raising, so an interrupted
                  run from before this story still resumes instead of being discarded.

        Logic:
            - No intermediate folders → (False, 0, None) - start from beginning
            - Folders for all parameters → (False, 0, None) - completed, cleanup and restart
            - Folders for some parameters → (True, highest_idx + 1, path) - resume from next (first not-yet-optimized) parameter
            - Parameter order mismatch → (False, 0, None) - validation failed, start fresh
        """
        self.logger.debug(f"_detect_resume_state: mode={mode}, output_dir={self.output_dir}")

        intermediate_folders = [
            p for p in self.output_dir.glob("accuracy_intermediate_*")
            if p.is_dir()
        ]

        if not intermediate_folders:
            self.logger.debug("No intermediate folders found")
            self.logger.debug("_detect_resume_state exit: should_resume=False, start_idx=0, last_config=None")
            return (False, 0, None, 0, set())

        valid_folders = []
        param_order = self.parameter_order

        pattern = r'accuracy_intermediate_(\d+)_(.+)'

        for folder_path in intermediate_folders:
            folder_name = folder_path.name
            match = re.match(pattern, folder_name)

            if not match:
                self.logger.warning(f"Skipping folder with invalid name format: {folder_name}")
                continue

            try:
                param_idx = int(match.group(1))
                param_suffix = match.group(2)

                if mode == 'weekly':
                    for week_key in ['week1-5', 'week6-9', 'week10-13', 'week14-17']:
                        if param_suffix.startswith(f"{week_key}_"):
                            param_name = param_suffix[len(week_key) + 1:]
                            break
                    else:
                        param_name = param_suffix
                else:
                    param_name = param_suffix

                if param_name not in param_order:
                    self.logger.debug(f"Folder {folder_name}: param '{param_name}' not in parameter order")
                    continue

                config_files = ['week1-5.json', 'week6-9.json',
                               'week10-13.json', 'week14-17.json']
                has_config = any((folder_path / f).exists() for f in config_files)
                if not has_config:
                    self.logger.warning(f"Skipping incomplete folder {folder_name}: no config files")
                    continue

                valid_folders.append((param_idx, param_name, folder_path))

            except Exception as e:
                self.logger.warning(f"Error processing {folder_name}: {e}")
                continue

        if not valid_folders:
            self.logger.debug("No valid intermediate folders found after validation")
            self.logger.debug("_detect_resume_state exit: should_resume=False, start_idx=0, last_config=None")
            return (False, 0, None, 0, set())

        valid_folders.sort(key=lambda x: x[0])
        highest_idx, highest_param, highest_path = valid_folders[-1]

        if highest_idx >= len(param_order) - 1:
            # T69/D5: completing every parameter finishes a PASS, not necessarily the RUN.
            # Pre-T69 there was only ever one pass, so this correctly meant "done". Now, if
            # the recorded ascent state still has unfrozen horizons, the next thing to do is
            # start the NEXT pass at parameter 0 -- refusing to resume here would discard a
            # completed pass and restart the whole ascent.
            pass_idx, frozen_horizons = self._read_ascent_state(highest_path)
            all_horizons = set(WEEK_RANGES.keys())
            if frozen_horizons >= all_horizons:
                self.logger.debug("All parameters complete and all horizons frozen -- run is done")
                return (False, 0, None, 0, set())
            self.logger.info(
                f"Pass {pass_idx + 1} completed all {len(param_order)} parameters; "
                f"resuming at pass {pass_idx + 2} from parameter 1 "
                f"(frozen: {sorted(frozen_horizons) or 'none'})"
            )
            return (True, 0, highest_path, pass_idx + 1, frozen_horizons)

        self.logger.debug(
            f"Found {len(valid_folders)} valid intermediate folders, "
            f"highest: {highest_param} (idx {highest_idx})"
        )
        self.logger.debug(f"_detect_resume_state exit: should_resume=True, start_idx={highest_idx + 1}, last_config={highest_path}")
        pass_idx, frozen_horizons = self._read_ascent_state(highest_path)
        return (True, highest_idx + 1, highest_path, pass_idx, frozen_horizons)

    def run_both(self) -> Path:
        """
        Run tournament optimization: each parameter optimizes across ALL 4 weekly horizons.

        For each parameter:
        - Generate test configs from 4 baseline configs (one per horizon)
        - Evaluate each config across all 4 horizons
        - Track best config for each horizon independently
        - Save intermediate results (all 4 best configs)
        - Update baselines for next parameter

        Returns:
            Path: Path to optimal configuration folder
        """
        self._sweep_orphaned_temp_dirs()
        total_params = len(self.parameter_order)
        self.logger.info(
            f"Starting tournament optimization: {total_params} parameters × "
            f"{self.config_generator.num_test_values} test values × 4 horizons "
            f"(each config evaluated across all 4 week ranges)"
        )

        self._setup_signal_handlers()

        try:
            (should_resume, resume_param_idx, last_config_path,
             resume_pass_idx, resume_frozen) = self._detect_resume_state()

            if not should_resume:
                # D2.2 Polish finding 1: _detect_resume_state has three should_resume=False
                # branches that can fire with a scratch candidate-dump file still on disk (no
                # intermediate folders found; a parameter-order mismatch; all parameters complete
                # and all horizons frozen). None of them reset the scratch, so a fresh ascent
                # would otherwise silently merge an abandoned run's records into its own promoted
                # candidate_results.json. Reset before evaluating the first candidate.
                self.results_manager.reset_candidate_dump()

            baseline_to_use = None
            if should_resume and last_config_path:
                baseline_to_use = last_config_path
                all_intermediate = sorted(
                    p.name for p in self.output_dir.glob("accuracy_intermediate_*")
                    if p.is_dir()
                )
                self.logger.info(
                    f"Intermediate folders found ({len(all_intermediate)}): {all_intermediate}"
                )
                self.logger.info(
                    f"Resuming from parameter {resume_param_idx + 1}. "
                    f"Selected: {last_config_path.name}"
                )
                self.results_manager.load_intermediate_results(last_config_path)
            else:
                required_files = ['league_config.json', 'week1-5.json', 'week6-9.json', 'week10-13.json', 'week14-17.json']
                optimal_folders = sorted(
                    (p for p in self.output_dir.glob("accuracy_optimal_*")
                     if p.is_dir() and all((p / f).exists() for f in required_files)),
                    key=lambda p: p.stat().st_mtime
                )
                if optimal_folders:
                    baseline_to_use = optimal_folders[-1]
                    self.logger.info(f"Using latest optimal config as baseline: {baseline_to_use.name}")

            if baseline_to_use:
                self.logger.info(f"Reloading baseline configs from {baseline_to_use}")
                self.config_generator.baseline_configs = ConfigGenerator.load_baseline_from_folder(baseline_to_use)
                self.logger.info(f"Loaded {len(self.config_generator.baseline_configs)} horizon configs from {baseline_to_use.name}")

            # T69/D1: the CONVERGENCE LOOP. Repeat full ascent passes until every horizon
            # has frozen (a pass in which it adopted nothing) or the bound is hit. Each of
            # the 4 horizons is an INDEPENDENT tournament -- one freezing does not stop the
            # others -- mirroring SweepTournament's per-config independence.
            # T69/D5: resume mid-ascent. A pre-T69 folder yields (0, set()), i.e. today's
            # behaviour, so an interrupted run from before this story still resumes.
            all_horizons = set(WEEK_RANGES.keys())
            frozen_horizons = set(resume_frozen) & all_horizons
            pass_idx = resume_pass_idx if should_resume else 0
            bound_hit = False

            if should_resume and (pass_idx or frozen_horizons):
                self.logger.info(
                    f"Resuming mid-ascent at pass {pass_idx + 1} "
                    f"with frozen horizons: {sorted(frozen_horizons) or 'none'}"
                )

            while True:
                if frozen_horizons >= all_horizons:
                    # T69/D5: a resume can arrive already fully frozen. Running a pass here
                    # would do no work yet still write intermediate folders, so check BEFORE
                    # dispatching rather than only after.
                    self.logger.info("All horizons already converged on entry; nothing to run")
                    break

                self.logger.info(
                    f"--- Ascent pass {pass_idx + 1} | "
                    f"active horizons: {sorted(all_horizons - frozen_horizons)} ---"
                )
                adopted = self._run_ascent_pass(
                    pass_idx, frozen_horizons, should_resume, resume_param_idx,
                    resume_pass_idx
                )

                newly_frozen = (all_horizons - frozen_horizons) - adopted
                for horizon in sorted(newly_frozen):
                    self.logger.info(
                        f"Horizon {horizon} CONVERGED after pass {pass_idx + 1} "
                        f"(a full pass adopted no parameter)"
                    )
                frozen_horizons |= newly_frozen
                pass_idx += 1

                if frozen_horizons == all_horizons:
                    self.logger.info(
                        f"All {len(all_horizons)} horizons converged after {pass_idx} pass(es)"
                    )
                    break

                if pass_idx >= MAX_ASCENT_PASSES:
                    bound_hit = True
                    # T69/AC3: a BOUND HIT is not convergence. Say so distinctly -- a run
                    # that stopped because it ran out of passes has NOT settled, and calling
                    # it converged would hide exactly the non-convergence the bound exists
                    # to surface.
                    self.logger.warning(
                        f"MAX PASS BOUND REACHED ({MAX_ASCENT_PASSES} passes) with "
                        f"{sorted(all_horizons - frozen_horizons)} still adopting. These "
                        f"horizons did NOT converge; results are the best found so far."
                    )
                    break

            optimal_path = self.results_manager.save_optimal_configs()

            self._warn_low_accuracy_promoted()

            deleted_count = cleanup_accuracy_intermediate_folders(self.output_dir)
            if deleted_count > 0:
                self.logger.info(f"Cleaned up {deleted_count} intermediate folders")

            outcome = (
                f"BOUND-HIT after {pass_idx} passes (not converged)" if bound_hit
                else f"CONVERGED after {pass_idx} pass(es)"
            )
            self.logger.info(
                f"Tournament optimization complete: {outcome}. Optimized {total_params} "
                f"parameters across 4 week ranges. Results saved to: {optimal_path}"
            )

            return optimal_path

        finally:
            self._restore_signal_handlers()


    def _run_ascent_pass(self, pass_idx: int, frozen_horizons: set,
                         should_resume: bool, resume_param_idx: int,
                         resume_pass_idx: int = 0) -> set:
        """Run ONE full coordinate-ascent pass over parameter_order.

        T69/D1: ported from SweepTournament's `while moved:` shape. A pass walks every
        parameter, evaluates its candidates, and records adoptions. The caller freezes any
        horizon that adopted nothing in the pass.

        Args:
            pass_idx (int): 0-based pass number. The resume skip applies only to pass 0.
            frozen_horizons (set): Horizons already converged; skipped for both config
                generation and result recording so a frozen horizon's best cannot move.
            should_resume (bool): From _detect_resume_state.
            resume_param_idx (int): Parameter index to resume at, pass 0 only.

        Returns:
            set: Horizons that adopted at least one candidate during this pass.
        """
        adopted_this_pass = set()

        for param_idx, param_name in enumerate(self.parameter_order):
            # T69/D5: the resume skip applies to the pass being RESUMED INTO -- not
            # unconditionally to pass 0. A run interrupted mid-pass-2 resumes at pass 2 and
            # must skip the parameters that pass already completed; every LATER pass walks
            # every parameter from the top.
            if should_resume and pass_idx == resume_pass_idx and param_idx < resume_param_idx:
                continue

            test_values_dict = self.config_generator.generate_horizon_test_values(param_name)

            for horizon, test_values in test_values_dict.items():
                if len(test_values) == 0:
                    raise ValueError(f"No test values generated for parameter {param_name}, horizon {horizon}")

            # T69/D1: count only the horizons this pass will actually evaluate. Counting all
            # of them would inflate the ProgressTracker total and the log line, so a
            # partially-frozen pass could never reach 100% -- reporting a bar that cannot
            # complete as if work were missing.
            active_horizons = [h for h in test_values_dict if h not in frozen_horizons]
            total_configs = sum(len(test_values_dict[h]) for h in active_horizons)
            total_evaluations = total_configs * len(WEEK_RANGES)

            if total_configs == 0:
                # Every horizon frozen: nothing to evaluate for this parameter.
                continue

            self.logger.info(f"Optimizing parameter {param_idx + 1}/{len(self.parameter_order)}: {param_name}")
            self.logger.info(f"  Evaluating {total_configs} configs × 4 horizons = {total_evaluations} total evaluations")

            self.progress_tracker = ProgressTracker(
                total=total_configs,
                description="Configs (each tests 4 horizons)"
            )

            configs_to_evaluate = []
            config_metadata = []

            for horizon, test_values in test_values_dict.items():
                if horizon in frozen_horizons:
                    continue   # T69/D1: converged -- generate no further candidates
                for test_idx, test_value in enumerate(test_values):
                    config_dict = self.config_generator.get_config_for_horizon(horizon, param_name, test_idx)

                    config_dict['_eval_metadata'] = {
                        'param_name': param_name,
                        'param_value': test_value,
                        'horizon': horizon,
                        'test_idx': test_idx
                    }

                    configs_to_evaluate.append(config_dict)
                    config_metadata.append((horizon, test_idx))

            if self.parallel_runner is None:
                from FantasyFootballHelperScriptsWorkspace.FantasyFootballHelperScripts.simulation.accuracy.ParallelAccuracyRunner import ParallelAccuracyRunner
                self.parallel_runner = ParallelAccuracyRunner(
                    self.data_folder,
                    self.available_seasons,
                    max_workers=self.max_workers,
                    use_processes=self.use_processes,
                    excluded_season_weeks=self.excluded_season_weeks
                )

            def progress_update(completed):
                self.progress_tracker.update()

            evaluation_results = self.parallel_runner.evaluate_configs_parallel(
                configs_to_evaluate,
                progress_callback=progress_update
            )

            self.progress_tracker.finish()

            for (config_dict, results_dict), (horizon, test_idx) in zip(evaluation_results, config_metadata):
                for result_horizon, result in results_dict.items():
                    if result_horizon in frozen_horizons:
                        continue   # T69/D1: frozen -- its best is final for this run
                    is_new_best = self.results_manager.add_result(
                        result_horizon,
                        config_dict,
                        result,
                        param_name=param_name,
                        test_idx=test_idx,
                        base_horizon=horizon,
                        pass_idx=pass_idx
                    )

                    if is_new_best:
                        adopted_this_pass.add(result_horizon)
                        self.logger.info(f"    New best for {result_horizon}: MAE={result.mae:.4f} (test_{test_idx})")

            self.results_manager.save_intermediate_results(
                param_idx,
                param_name,
                pass_idx=pass_idx,
                frozen_horizons=frozen_horizons
            )

            horizon_map = {
                'week_1_5': '1-5',
                'week_6_9': '6-9',
                'week_10_13': '10-13',
                'week_14_17': '14-17'
            }
            for week_key, horizon_key in horizon_map.items():
                if week_key in frozen_horizons:
                    continue   # T69/D1: frozen -- baseline is final
                best_perf = self.results_manager.best_configs.get(week_key)
                if best_perf is not None:
                    self.config_generator.update_baseline_for_horizon(horizon_key, best_perf.config_dict)
                else:
                    self.logger.warning(f"No best config found for {week_key} after parameter {param_name}")

            self._log_parameter_summary(param_name)

        return adopted_this_pass

    def _warn_low_accuracy_promoted(self) -> None:
        """Warn once per horizon when the promoted config scores below the accuracy bar.

        Reads the winning AccuracyConfigPerformance for each horizon straight from
        results_manager.best_configs at the moment save_optimal_configs() has written
        them, so each warning names the config the run is actually shipping. Emits at
        most one line per threshold per horizon (<= 8 lines per run, 0 when healthy).
        """
        for week_key in WEEK_RANGES.keys():
            best_perf = self.results_manager.best_configs.get(week_key)
            if not best_perf or not best_perf.overall_metrics:
                continue

            metrics = best_perf.overall_metrics

            if (metrics.pairwise_accuracy is not None
                    and metrics.pairwise_accuracy < PAIRWISE_ACCURACY_WARN_THRESHOLD):
                self.logger.warning(
                    f"[{week_key}] Low pairwise accuracy: "
                    f"{metrics.pairwise_accuracy:.1%} (threshold: {PAIRWISE_ACCURACY_WARN_THRESHOLD:.0%})"
                )

            if (metrics.top_10_accuracy is not None
                    and metrics.top_10_accuracy < TOP_10_ACCURACY_WARN_THRESHOLD):
                self.logger.warning(
                    f"[{week_key}] Low top-10 accuracy: "
                    f"{metrics.top_10_accuracy:.1%} (threshold: {TOP_10_ACCURACY_WARN_THRESHOLD:.0%})"
                )

    def _log_parameter_summary(self, param_name: str) -> None:
        """Log summary of best results for all horizons after parameter completes."""
        self.logger.info(f"Parameter {param_name} complete:")

        for week_key in ['week_1_5', 'week_6_9', 'week_10_13', 'week_14_17']:
            best_perf = self.results_manager.best_configs.get(week_key)
            if best_perf:
                test_idx = best_perf.test_idx if best_perf.test_idx is not None else '?'

                if best_perf.overall_metrics:
                    self.logger.info(
                        f"  {week_key}: "
                        f"Pairwise={format_metric_pct(best_perf.overall_metrics.pairwise_accuracy)} | "
                        f"Top-10={format_metric_pct(best_perf.overall_metrics.top_10_accuracy)} | "
                        f"Spearman={format_metric_corr(best_perf.overall_metrics.spearman_correlation)} | "
                        f"MAE={best_perf.mae:.4f} (diag) "
                        f"(test_{test_idx})"
                    )
                else:
                    self.logger.info(f"  {week_key}: MAE={best_perf.mae:.4f} (test_{test_idx})")
            else:
                self.logger.info(f"  {week_key}: No results yet")


