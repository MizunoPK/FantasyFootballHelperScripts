"""
Config Promoter

Lands a re-measured winning combination from a multi-parameter sweep into the live
league_config.json. Reads the accumulated sweep results, shortlists the top candidates by a
Wilson lower confidence bound over their pooled totals, RE-MEASURES each shortlisted
candidate head-to-head against the current live config on fresh CRN-paired season replays
(paired_comparison.run_paired_ab_comparison), and writes the significant winner's DRAFT_ORDER
plus the six draft-side parameters onto league_config.json via the shared
apply_draft_overrides helper — preserving every other key.

This module therefore RUNS SIMULATIONS (T62): --promote is no longer a read-then-write. The
store's ranking selects only which candidates are worth paying to re-measure; it is never the
promoted or reported number, because taking the maximum over ~10^3 noisy store estimates is
upward-biased by roughly the size of the entire signal being ranked on. Two consequences the
operator is told about rather than shielded from: the promoted headline is still the argmax
over K fresh measurements (a residual max-over-K bias), and the K significance tests are
uncorrected for multiplicity. A promote can now REFUSE — when no candidate beats the live
config significantly on fresh evidence, nothing is written.

Because it now simulates, this module carries TWO config representations that must never be
collapsed: the RAW league_config.json (read by _read_config) is what the diff and the atomic write
operate on, and a ConfigManager-MERGED config (built by _build_simulation_base_config) is what the
re-measurement arms are built from. The raw file alone lacks four parameters SimulatedLeague
requires, and the merged config carries week-file-derived parameters league_config.json must never
be given — so each representation is wrong for the other's job.

This is the one component that mutates the operator's live config. The write is
atomic (tmp -> rename) so a crash mid-write cannot corrupt the file, and a
read-only git dirty-state check warns before overwriting uncommitted edits (the
only state git cannot recover). Recovery otherwise relies on git: league_config.json
is tracked, so a promote is reviewable / revertable via git diff / git checkout.

Author: Kai Mizuno
"""

# Standard library
import json
import subprocess
from pathlib import Path
from statistics import NormalDist
from typing import Any, Dict

# Local
from league_helper.util.ConfigManager import ConfigManager
from simulation.win_rate.config_overrides import (
    apply_draft_overrides,
    extract_draft_param_values,
)
from simulation.win_rate.paired_comparison import run_paired_ab_comparison
from simulation.win_rate.strategy_loader import load_valid_strategies
from simulation.win_rate.SweepTournament import DEFAULT_CONFIDENCE
from simulation.win_rate.sweep_summary import rank_combinations, wilson_interval
from utils.error_handler import ConfigurationError, FileOperationError
from utils.LoggingManager import get_logger

logger = get_logger()

# Promote-path re-measurement parameters (T62/D3/D5). Module-scope, mirroring
# SweepTournament's DEFAULT_* block, so the CLI flags' defaults and the computation share one
# source of truth (no drift between what --promote-shortlist advertises and what runs).
# DEFAULT_CONFIDENCE is IMPORTED from SweepTournament above, deliberately never re-declared —
# the same one-source-of-truth reason its own module comment gives.
DEFAULT_PROMOTE_SHORTLIST = 3
DEFAULT_PROMOTE_SIMS = 20
# Mirrors SweepTournament.DEFAULT_MIN_GAMES rather than inventing a second floor value: the
# established house degenerate-input floor, cleared trivially at production settings (one
# default --sims 10 single-season evaluation is 170 games) and firing only on pathological
# stores.
DEFAULT_MIN_SHORTLIST_GAMES = 30
# sqrt(VIF) with the VIF ~= 1.64 measured in ARCHITECTURE.md Decision 6 (latent per-league
# quality, rho ~= 0.04; false-adoption 4.8% -> 9.1% against a 5% nominal level). Applied to the
# operator-facing re-measured interval AND to the promote/refuse decision z — both drive the
# live-config write — but NEVER to the shortlist LCB, which is an internal heuristic filter
# over incommensurable pooled totals and can support no precision claim (T62/D5).
CLUSTER_SE_INFLATION = 1.28


def compute_promotion(
    store,
    data_folder: Path,
    config_path: Path = Path("data/configs/league_config.json"),
    *,
    seed: int,
    shortlist: int = DEFAULT_PROMOTE_SHORTLIST,
    sims: int = DEFAULT_PROMOTE_SIMS,
) -> Dict[str, Any]:
    """
    Re-measure the shortlisted sweep candidates and compute the promotion WITHOUT writing.

    Performs every step of a promotion except the disk write (T62/D2). The store's ranking is
    no longer the promotion: taking element [0] of a rate-ordered store was a double maximum
    (max over combos within a config, then max over configs) with no fresh evidence anywhere
    between it and the live-config write. Instead this:

      1. shortlists the top ``shortlist`` candidates by Wilson lower confidence bound, over
         combinations with at least DEFAULT_MIN_SHORTLIST_GAMES recorded games;
      2. builds each candidate in TWO representations via apply_draft_overrides — a RAW-derived
         one (the write/diff arm) and a ConfigManager-MERGED one (the simulate arm). See
         _build_simulation_base_config for why the two must never be collapsed;
      3. re-measures each MERGED candidate head-to-head against the MERGED live config on fresh,
         CRN-paired runs over the committed season data (run_paired_ab_comparison);
      4. promotes the candidate with the largest fresh delta among those clearing the
         clustering-adjusted one-sided significance threshold with delta > 0 — and REFUSES,
         writing nothing, when none clears.

    This SHRINKS rather than eliminates the selection bias: the promoted headline is the
    argmax of delta over ``shortlist`` fresh measurements, so a max-over-K bias of order
    0.85 sigma survives (against the ~3 sigma max-over-10^3 store bias it replaces), and the
    ``shortlist`` significance tests are an UNCORRECTED multiplicity (up to ~3x the nominal
    one-sided level at shortlist=3). Both are reported to the operator, not implied away.

    No file is written and config_path is left untouched. This is the no-write path behind the
    bare ``--promote`` preview; the write path (promote_best_combination) delegates here.

    Args:
        store: A SweepResultsManager exposing get_all_combinations() and get_discriminating().
        data_folder (Path): Simulation data root. Used both to resolve each candidate
            strategy's DRAFT_ORDER via load_valid_strategies AND as the season-data root the
            re-measurement replays (it must contain 20XX/ season folders).
        config_path (Path): The live league_config.json. Read RAW for the current values and the
            diff, and separately merged via ConfigManager (_build_simulation_base_config) to form
            the "before" arm of every re-measurement. Never written here. Its parent.parent must
            be the data root whose configs/ folder holds league_config.json plus the week*.json
            files ConfigManager merges.
        seed (int): Base seed for the re-measurement, making the paired comparison
            reproducible and CRN-paired across arms. Required — the caller resolves it.
        shortlist (int): How many top-LCB candidates to re-measure (K).
        sims (int): Simulations per season per arm for each re-measurement (B).

    Returns:
        Dict[str, Any]: {"strategy_id", "param_values", "remeasured_rate", "remeasured_ci",
            "remeasured_games", "delta", "z", "z_adjusted", "shortlist_size", "seed",
            "max_selected_win_rate", "max_selected_games", "lcb", "new_config", "diff"}.
            "remeasured_rate" is the recommended arm's FRESH win rate and is the only value
            here offered as an estimate; "remeasured_ci" is its clustering-widened Wilson
            interval. "max_selected_win_rate" is the store-derived in-sample maximum, retained
            for display and explicitly NOT an estimate. "new_config" is the proposed config
            dict and "diff" maps each changed key to {"current", "proposed"}.

    Raises:
        ConfigurationError: If the store is non-discriminating or empty, no combination clears
            the minimum-games floor, the winning strategy cannot be resolved, config_path is
            missing/corrupt or structurally incomplete, the MERGED simulation config cannot be
            built from config_path (see _build_simulation_base_config — a distinct, separately
            worded failure, never conflated with the data-folder one below), the re-measurement
            finds no season data (comparator FileNotFoundError) or no valid games (comparator
            ValueError), or no re-measured candidate clears significance with delta > 0. No
            write occurs in any case.
    """
    if not store.get_discriminating():
        raise ConfigurationError(
            "Refusing to promote: the sweep store was not produced under the discriminating "
            "(measured-vs-incumbent) regime — re-run the sweep. A noise-driven winner from a "
            "non-discriminating sweep must not be written."
        )

    combinations = store.get_all_combinations()
    if not combinations:
        raise ConfigurationError(
            "No sweep combinations to promote — run the sweep first."
        )

    candidates = rank_combinations(
        combinations, min_games=DEFAULT_MIN_SHORTLIST_GAMES
    )[:shortlist]
    if not candidates:
        raise ConfigurationError(
            f"Refusing to promote: no sweep combination has at least "
            f"{DEFAULT_MIN_SHORTLIST_GAMES} recorded games, so the re-measurement shortlist "
            f"is empty. Accumulate more sweep evidence before promoting."
        )

    # TWO config representations, deliberately (T62). Do NOT collapse these into one variable.
    #   base_config — the RAW file. The ONLY dict the write path and the diff may touch, because
    #     _atomic_write_json must reproduce league_config.json's exact structure.
    #   sim_base    — the ConfigManager-MERGED config. The ONLY dict the comparator may be handed,
    #     because SimulatedLeague validates against ConfigManager's required-parameter list, which
    #     the raw file (14 params) does not satisfy and the merged config (22 params) does.
    # _read_config runs FIRST and this ordering is load-bearing: a missing or corrupt config must
    # still surface as _read_config's existing "Cannot read config {path}" error, not as a
    # merge error.
    base_config = _read_config(config_path)
    sim_base = _build_simulation_base_config(config_path)
    critical_z = NormalDist().inv_cdf(DEFAULT_CONFIDENCE)

    best_row = None
    best_measured = None
    best_config = None
    for row in candidates:
        draft_order = _resolve_draft_order(row["strategy_id"], data_folder)
        try:
            # The WRITE arm: raw-derived, carried out of this function as "new_config".
            candidate_config = apply_draft_overrides(
                base_config, draft_order, row["param_values"]
            )
            # The SIMULATE arm: merged-derived, never written and never diffed. Both are built
            # from the same draft_order + param_values, so the two arms describe the same
            # candidate; only their parameter completeness differs.
            sim_candidate = apply_draft_overrides(
                sim_base, draft_order, row["param_values"]
            )
        except (KeyError, TypeError) as e:
            raise ConfigurationError(
                f"Config at {config_path} is structurally incomplete — missing key or section: {e}"
            ) from e

        try:
            measured = run_paired_ab_comparison(
                sim_base, sim_candidate, data_folder, seed, num_simulations=sims
            )
        except (FileNotFoundError, ValueError) as e:
            # The comparator's two new failure modes reach the promote path for the first
            # time here. _run_promote_mode catches only (ConfigurationError,
            # FileOperationError), so an unwrapped raise would surface as a bare traceback.
            raise ConfigurationError(
                f"Cannot re-measure promotion candidates from {data_folder}: {e}"
            ) from e

        adjusted_z = measured.z / CLUSTER_SE_INFLATION
        logger.info(
            f"compute_promotion re-measured {row['strategy_id']} | "
            f"delta={measured.delta:+.4f} z={measured.z:.2f} z_adjusted={adjusted_z:.2f} "
            f"over {measured.games} games/arm (seed={seed})"
        )
        # Strictly greater, so an exact delta tie keeps the earlier (higher-LCB) candidate.
        if measured.delta > 0 and adjusted_z >= critical_z:
            if best_measured is None or measured.delta > best_measured.delta:
                best_row = row
                best_measured = measured
                best_config = candidate_config

    if best_measured is None:
        raise ConfigurationError(
            f"Refusing to promote: none of the {len(candidates)} re-measured candidate(s) "
            f"beat the live config on fresh data by a clustering-adjusted significant margin "
            f"(one-sided z / {CLUSTER_SE_INFLATION} >= {critical_z:.3f}, with delta > 0). "
            f"Nothing was written."
        )

    diff = _build_promotion_diff(base_config, best_config)
    # PairedComparisonResult carries the recommended arm's RATE, not its win count; under CRN
    # both arms evaluate the same number of games, so the count is exactly rate * games.
    recommended_wins = round(best_measured.recommended_rate * best_measured.games)
    ci_low, ci_high = wilson_interval(
        recommended_wins,
        best_measured.games,
        DEFAULT_CONFIDENCE,
        se_inflation=CLUSTER_SE_INFLATION,
    )

    return {
        "strategy_id": best_row["strategy_id"],
        "param_values": best_row["param_values"],
        "remeasured_rate": best_measured.recommended_rate,
        "remeasured_ci": (ci_low, ci_high),
        "remeasured_games": best_measured.games,
        "delta": best_measured.delta,
        "z": best_measured.z,
        "z_adjusted": best_measured.z / CLUSTER_SE_INFLATION,
        "shortlist_size": len(candidates),
        "seed": seed,
        "max_selected_win_rate": best_row["win_rate"],
        "max_selected_games": best_row["games"],
        "lcb": best_row["lcb"],
        "new_config": best_config,
        "diff": diff,
    }


def _build_promotion_diff(base_config: dict, new_config: dict) -> Dict[str, Dict[str, Any]]:
    """
    Build the current -> proposed diff of the keys a promotion changes.

    Compares the six draft-side params (via extract_draft_param_values) and
    DRAFT_ORDER between the current (base) and proposed (new) configs, returning
    only the keys whose value changes. Insertion order is the six params (in
    DRAFT_PARAM_LOCATIONS order) followed by DRAFT_ORDER.

    Args:
        base_config (dict): The current live config.
        new_config (dict): The proposed config from apply_draft_overrides.

    Returns:
        Dict[str, Dict[str, Any]]: {changed_key: {"current": ..., "proposed": ...}}.
    """
    diff: Dict[str, Dict[str, Any]] = {}

    current_params = extract_draft_param_values(base_config)
    proposed_params = extract_draft_param_values(new_config)
    for name, current_value in current_params.items():
        proposed_value = proposed_params[name]
        if current_value != proposed_value:
            diff[name] = {"current": current_value, "proposed": proposed_value}

    current_order = base_config["parameters"].get("DRAFT_ORDER")
    proposed_order = new_config["parameters"].get("DRAFT_ORDER")
    if current_order != proposed_order:
        diff["DRAFT_ORDER"] = {"current": current_order, "proposed": proposed_order}

    return diff


def promote_best_combination(
    store,
    data_folder: Path,
    config_path: Path = Path("data/configs/league_config.json"),
    *,
    seed: int,
    shortlist: int = DEFAULT_PROMOTE_SHORTLIST,
    sims: int = DEFAULT_PROMOTE_SIMS,
) -> Dict[str, Any]:
    """
    Write the re-measurement-winning sweep combination into league_config.json.

    Delegates the whole selection to compute_promotion — shortlist by Wilson lower confidence
    bound, re-measure each candidate head-to-head against the live config on fresh data, and
    take the significant winner (or refuse) — then applies that candidate's DRAFT_ORDER plus
    the six draft-side params onto config_path via apply_draft_overrides (all other keys
    preserved). The write mechanics are unchanged (T62 does not touch them): the write is
    atomic, and a git dirty-state warning is logged (but does not block) when config_path has
    uncommitted changes. The new refuse-to-promote gate sits inside compute_promotion, i.e.
    strictly IN FRONT of this write.

    What is written is always the RAW-derived config (compute_promotion's "new_config"), never the
    ConfigManager-merged dict the re-measurement ran on — merging is a read-side concern only, and
    writing a merged config back would inject week-file-derived parameters league_config.json does
    not own. See _build_simulation_base_config.

    Args:
        store: A SweepResultsManager exposing get_all_combinations() and get_discriminating().
        data_folder (Path): Simulation data root — resolves each candidate strategy's
            DRAFT_ORDER and supplies the 20XX/ season data the re-measurement replays.
        config_path (Path): The live league_config.json to overwrite.
        seed (int): Base seed for the re-measurement (required; the caller resolves it).
        shortlist (int): How many top-LCB candidates to re-measure (K).
        sims (int): Simulations per season per arm for each re-measurement (B).

    Returns:
        Dict[str, Any]: Exactly {"strategy_id", "param_values", "remeasured_rate",
            "remeasured_ci", "remeasured_games", "delta", "z", "z_adjusted",
            "shortlist_size", "seed", "max_selected_win_rate", "max_selected_games", "lcb"}
            describing the promoted combination. The headline is "remeasured_rate" with
            "remeasured_ci"; "max_selected_win_rate" is the store-derived in-sample maximum
            and is NOT an estimate.

    Raises:
        ConfigurationError: For every compute_promotion failure — non-discriminating or empty
            store, empty shortlist, unresolvable strategy, missing/corrupt/incomplete config,
            an unbuildable merged simulation config, re-measurement finding no season data or no
            valid games, or no candidate clearing significance. No write occurs in any of these
            cases.
        FileOperationError: If the atomic write itself fails (config_path is left
            untouched and no orphaned .tmp remains).
    """
    plan = compute_promotion(
        store, data_folder, config_path, seed=seed, shortlist=shortlist, sims=sims
    )
    new_config = plan["new_config"]

    if _has_uncommitted_changes(config_path):
        logger.warning(
            f"{config_path} has uncommitted changes — promotion will overwrite "
            f"them (git cannot recover uncommitted edits)."
        )

    _atomic_write_json(new_config, config_path)

    logger.info(
        f"Promoted {plan['strategy_id']} to {config_path} "
        f"(re-measured win_rate={plan['remeasured_rate']:.3f} "
        f"[{plan['remeasured_ci'][0]:.3f}, {plan['remeasured_ci'][1]:.3f}] over "
        f"{plan['remeasured_games']} games/arm — winner of a {plan['shortlist_size']}-way "
        f"re-measurement at seed {plan['seed']}; delta={plan['delta']:+.4f}, "
        f"z={plan['z']:.2f}, z_adjusted={plan['z_adjusted']:.2f}; "
        f"max_selected={plan['max_selected_win_rate']:.3f} over "
        f"{plan['max_selected_games']} store games)."
    )
    return {
        "strategy_id": plan["strategy_id"],
        "param_values": plan["param_values"],
        "remeasured_rate": plan["remeasured_rate"],
        "remeasured_ci": plan["remeasured_ci"],
        "remeasured_games": plan["remeasured_games"],
        "delta": plan["delta"],
        "z": plan["z"],
        "z_adjusted": plan["z_adjusted"],
        "shortlist_size": plan["shortlist_size"],
        "seed": plan["seed"],
        "max_selected_win_rate": plan["max_selected_win_rate"],
        "max_selected_games": plan["max_selected_games"],
        "lcb": plan["lcb"],
    }


def _resolve_draft_order(strategy_id: str, data_folder: Path) -> list:
    """
    Resolve the winning strategy's DRAFT_ORDER by matching its filename.

    Linear-searches the (filename, DRAFT_ORDER, name) triples from
    load_valid_strategies for filename == strategy_id.

    Raises:
        ConfigurationError: If no strategy matches, or no valid strategy files
            exist (load_valid_strategies raises FileNotFoundError).
    """
    try:
        strategies, _ = load_valid_strategies(data_folder)
    except FileNotFoundError as e:
        raise ConfigurationError(
            f"Cannot resolve winning strategy {strategy_id}: {e}"
        ) from e

    for filename, draft_order, _name in strategies:
        if filename == strategy_id:
            return draft_order

    raise ConfigurationError(
        f"Winning strategy {strategy_id} not found among valid strategies"
    )


def _build_simulation_base_config(config_path: Path) -> dict:
    """
    Build the MERGED config the simulator requires — deliberately NOT the raw file contents.

    The promote path carries TWO distinct config representations (T62) and a future reader must
    not collapse them into one:

      * the RAW representation (_read_config) is what apply_draft_overrides + _build_promotion_diff
        + _atomic_write_json operate on. The atomic write must reproduce the live file's exact
        structure, so writing a merged config back would silently inflate league_config.json with
        the week-file-derived prediction parameters it does not own.
      * the MERGED representation (this function) is what run_paired_ab_comparison needs, because
        it constructs a SimulatedLeague, which validates against ConfigManager's full
        required-parameter list. The raw data/configs/league_config.json carries 14 parameters and
        is missing NORMALIZATION_MAX_SCALE, TEAM_QUALITY_SCORING, PERFORMANCE_SCORING, and
        MATCHUP_SCORING; those exist only after ConfigManager merges the sibling
        data/configs/week*.json files (22 merged parameters). Handing the raw dict to the
        comparator raises "Config missing required parameters: ..." on EVERY promote.

    Mirrors CombinationEvaluator.__init__ (CombinationEvaluator.py:78-85) — the established in-repo
    shape for turning a config path into a simulator-ready dict — including its
    (FileNotFoundError, ValueError) catch. It diverges from that peer in the raised type only:
    CombinationEvaluator raises FileOperationError, while this module's own _read_config raises
    ConfigurationError for a config-load failure, and the in-module peer governs here. Both types
    are caught by _run_promote_mode (run_win_rate_simulation.py:386), so neither escapes as a bare
    traceback.

    Args:
        config_path (Path): The live league_config.json. Its parent.parent is the data root
            ConfigManager loads (data/configs/league_config.json -> data/).

    Returns:
        dict: {"config_name", "description", "parameters"} carrying the FULL merged parameter set.

    Raises:
        ConfigurationError: If the merged config cannot be built — a missing league_config.json,
            missing/invalid week*.json siblings, or a structurally incomplete config. The message
            names the CONFIG PATH and says so explicitly, so a config-merge failure can never be
            mistaken for the comparator's "no season data in {data_folder}" failure. Distinguishing
            these two is the whole point of routing the merge through its own named helper.
    """
    try:
        cm = ConfigManager(config_path.parent.parent)
    except (FileNotFoundError, ValueError) as e:
        raise ConfigurationError(
            f"Cannot build the merged simulation config from {config_path} "
            f"(data root {config_path.parent.parent}): {e}. This is a CONFIG problem, not a "
            f"season-data problem — the re-measurement was never reached and nothing was written."
        ) from e

    return {
        "config_name": cm.config_name,
        "description": cm.description,
        "parameters": dict(cm.parameters),
    }


def _read_config(config_path: Path) -> dict:
    """
    Read a config file as raw JSON, preserving its exact structure.

    Raises:
        ConfigurationError: If config_path is missing or not valid JSON.
    """
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise ConfigurationError(f"Cannot read config {config_path}: {e}") from e


def _has_uncommitted_changes(path: Path) -> bool:
    """
    Return True if `path` has uncommitted git changes, False otherwise.

    Runs `git status --porcelain <path>` read-only. Degrades gracefully: any
    failure (git missing, not a repo, non-zero exit, subprocess error) returns
    False so the promotion is never blocked or crashed by the git probe.
    """
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain", str(path)],
            capture_output=True,
            text=True,
            check=True,
        )
    except (OSError, subprocess.SubprocessError):
        return False
    return bool(result.stdout.strip())


def _atomic_write_json(data: dict, path: Path) -> None:
    """
    Write `data` as JSON to `path` atomically via tmp file -> rename.

    Mirrors SweepResultsManager._save: a mid-write failure leaves `path`
    untouched, and the orphaned .tmp is removed before re-raising.

    Raises:
        FileOperationError: On any OSError/PermissionError during the write.
    """
    tmp_path = path.with_suffix(".tmp")
    try:
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        tmp_path.replace(path)
    except (PermissionError, OSError) as e:
        tmp_path.unlink(missing_ok=True)
        raise FileOperationError(f"Failed to write config to {path}: {e}") from e
