"""
Tests for simulation.win_rate.config_promoter.

Covers the live-config promotion writer: promoting the top-ranked combination's
DRAFT_ORDER + 6 params, preserving all other keys, cumulative-win-rate ranking
(not best_single_run_win_rate), the four error paths that converge to ConfigurationError with
no write (empty store, strategy absent, strategy files missing, config missing/
corrupt), the git dirty-state warn-and-proceed behavior, the graceful git probe,
and write-failure safety (FileOperationError + no orphaned .tmp). Exercised against
a real SweepResultsManager on tmp_path and a tmp_path copy of the real
league_config.json; load_valid_strategies and the git probe are patched.

Author: Kai Mizuno
"""

# Standard library
import json
import shutil
import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

# Third-party
import pytest

# Local
from simulation.win_rate import config_promoter
from simulation.win_rate.config_promoter import (
    compute_promotion,
    promote_best_combination,
    CLUSTER_SE_INFLATION,
    DEFAULT_CONFIDENCE,
    DEFAULT_MIN_SHORTLIST_GAMES,
)
from simulation.win_rate.config_overrides import extract_draft_param_values
from simulation.win_rate.paired_comparison import PairedComparisonResult
from simulation.win_rate.SweepResultsManager import SweepResultsManager
from simulation.win_rate.sweep_summary import wilson_interval
from utils.error_handler import ConfigurationError, FileOperationError

MODULE = "simulation.win_rate.config_promoter"

# T62: the promote path is now seeded (the CLI resolves the seed and passes it down), so every
# call site here supplies one explicit fixed value — the tests must stay deterministic.
_SEED = 20260720

# A stubbed re-measurement that CLEARS the promote gate: delta > 0 and the clustering-adjusted
# z (5.0 / 1.28 = 3.906) is above the one-sided 0.95 critical value 1.645, with margin.
_SIGNIFICANT_RESULT = PairedComparisonResult(
    current_rate=0.50,
    recommended_rate=0.55,
    delta=0.05,
    z=5.0,
    games=1700,
    seed=_SEED,
)

# The live config's current values for the 6 draft-side params.
_LIVE_PARAMS = {
    "SAME_POS_BYE_WEIGHT": 0.07,
    "DIFF_POS_BYE_WEIGHT": 0.01,
    "PRIMARY_BONUS": 67,
    "SECONDARY_BONUS": 69,
    "ADP_SCORING_WEIGHT": 4.76,
    "PLAYER_RATING_SCORING_WEIGHT": 3.52,
}

# Winner values — all in-bounds (per ConfigGenerator.PARAM_DEFINITIONS) and
# deliberately DISTINCT from _LIVE_PARAMS so a successful promote is observable.
_WINNER_PARAMS = {
    "SAME_POS_BYE_WEIGHT": 0.20,
    "DIFF_POS_BYE_WEIGHT": 0.05,
    "PRIMARY_BONUS": 90,
    "SECONDARY_BONUS": 100,
    "ADP_SCORING_WEIGHT": 3.00,
    "PLAYER_RATING_SCORING_WEIGHT": 2.00,
}

_WINNER_ORDER = [{"round": 1, "position": "RB"}, {"round": 2, "position": "WR"}]
_WINNER_ID = "2_winner.json"


_REAL_CONFIGS = Path("data/configs")


def _make_config_root(tmp_path, root_name):
    """Build a real <root>/configs/ tree so ConfigManager can merge the week files (T62).

    compute_promotion resolves its data root as config_path.parent.parent and hands it to
    ConfigManager, which requires <root>/configs/league_config.json plus the week*.json siblings.
    A bare league_config.json dropped in tmp_path does NOT satisfy that, so every fixture here
    reproduces the real data/ layout. All four week files are copied so the merge works whatever
    CURRENT_NFL_WEEK the committed config carries.
    """
    configs = tmp_path / root_name / "configs"
    configs.mkdir(parents=True)
    for src in [_REAL_CONFIGS / "league_config.json", *sorted(_REAL_CONFIGS.glob("week*.json"))]:
        shutil.copyfile(src, configs / src.name)
    return configs / "league_config.json"


@pytest.fixture
def config_path(tmp_path):
    """The real league_config.json inside a real tmp configs/ root (source never mutated)."""
    return _make_config_root(tmp_path, "live")


@pytest.fixture
def store(tmp_path):
    """A real SweepResultsManager holding the winning combination as the sole entry."""
    mgr = SweepResultsManager(tmp_path / "sweep.json")
    mgr.update(_WINNER_ID, _WINNER_PARAMS, 0.75, 75, 100)
    mgr.set_discriminating(True)
    return mgr


@pytest.fixture(autouse=True)
def stub_comparator():
    """Stub the promote path's fresh re-measurement for every test in this module (T62/D2).

    compute_promotion now calls run_paired_ab_comparison, which globs 20*/ season folders
    under the passed data_folder and raises FileNotFoundError when none exist — and every
    test here passes Path("unused"). Patching once, autouse, at the config_promoter import
    site (this file's established MODULE idiom) keeps all of these cases exercising SELECTION
    and WRITE behavior rather than season I/O, without repeating the same patch clause in
    every `with` block. A test that needs different re-measurement behavior nests its own
    patch(f"{MODULE}.run_paired_ab_comparison", ...), which takes precedence.

    The stub returns the SAME result for every candidate, so an exact delta tie falls through
    to compute_promotion's strict `>` comparison and the FIRST (highest-LCB) shortlisted
    candidate wins — which is exactly what the ranking and tie-break tests below assert.

    It is NOT a bare return_value: it first ASSERTS that both arms it receives are the
    ConfigManager-merged configs and not the raw league_config.json (T62 amendment). Stubbing the
    comparator is what let the original raw-config defect ship green; guarding the stub is what
    makes that impossible to repeat here.
    """
    def _stub(current_config, recommended_config, *args, **kwargs):
        _assert_simulator_ready(current_config, "current")
        _assert_simulator_ready(recommended_config, "recommended")
        return _SIGNIFICANT_RESULT

    with patch(f"{MODULE}.run_paired_ab_comparison", side_effect=_stub):
        yield


# T62: the four parameters the RAW data/configs/league_config.json does NOT carry — they exist
# only after ConfigManager merges the sibling week*.json files. Any config reaching the simulator
# must have all four, or SimulatedLeague raises "Config missing required parameters: ...".
_SIMULATOR_REQUIRED_PARAMS = (
    "NORMALIZATION_MAX_SCALE",
    "TEAM_QUALITY_SCORING",
    "PERFORMANCE_SCORING",
    "MATCHUP_SCORING",
)


def _assert_simulator_ready(config, arm):
    """Fail loudly if an arm handed to the comparator is the RAW config, not the merged one."""
    missing = [p for p in _SIMULATOR_REQUIRED_PARAMS if p not in config.get("parameters", {})]
    assert not missing, (
        f"T62 regression: the {arm} arm passed to run_paired_ab_comparison is missing "
        f"{missing}. compute_promotion must pass the ConfigManager-MERGED config "
        f"(_build_simulation_base_config), never the raw _read_config dict — a real --promote "
        f"would refuse every time with a misleading data-folder message."
    )


def _patch_strategies(*triples):
    """Patch load_valid_strategies on the module to return the given (filename, order, name) triples."""
    return patch(f"{MODULE}.load_valid_strategies", return_value=(list(triples), 0))


def _fresh_config(tmp_path, name):
    """An independent tmp configs/ root per `name`, for tests promoting into separate configs.

    `name` names the ROOT directory, not the file: the returned path always ends in
    league_config.json, because that is the filename ConfigManager looks for. Callers only compare
    promotion results, never the basename, so keeping the parameter shape unchanged keeps every
    existing call site byte-identical.
    """
    return _make_config_root(tmp_path, Path(name).stem)


class TestConfigPromoter:
    # --- Step 1: happy path -------------------------------------------------

    def test_promotes_winner_draft_order_and_params(self, store, config_path):
        with _patch_strategies((_WINNER_ID, _WINNER_ORDER, "Winner")), \
                patch(f"{MODULE}._has_uncommitted_changes", return_value=False):
            promote_best_combination(store, Path("unused"), config_path, seed=_SEED)

        written = json.loads(config_path.read_text())
        assert written["parameters"]["DRAFT_ORDER"] == _WINNER_ORDER
        assert extract_draft_param_values(written) == _WINNER_PARAMS

    def test_returns_exactly_the_promotion_keys(self, store, config_path):
        # T62: the return shape changed BY DESIGN. The store-derived rate/games are retained
        # but renamed max_selected_* (they are an in-sample maximum, not an estimate), and the
        # fresh re-measurement fields are the new headline.
        with _patch_strategies((_WINNER_ID, _WINNER_ORDER, "Winner")), \
                patch(f"{MODULE}._has_uncommitted_changes", return_value=False):
            result = promote_best_combination(store, Path("unused"), config_path, seed=_SEED)

        assert set(result) == {
            "strategy_id", "param_values",
            "remeasured_rate", "remeasured_ci", "remeasured_games",
            "delta", "z", "z_adjusted", "shortlist_size", "seed",
            "max_selected_win_rate", "max_selected_games", "lcb",
        }
        assert result["strategy_id"] == _WINNER_ID
        assert result["param_values"] == _WINNER_PARAMS
        assert result["max_selected_games"] == 100
        assert result["remeasured_rate"] == _SIGNIFICANT_RESULT.recommended_rate
        assert result["delta"] == _SIGNIFICANT_RESULT.delta
        assert result["seed"] == _SEED
        assert result["shortlist_size"] == 1

    # --- Step 2: preservation + cumulative ranking --------------------------

    def test_other_keys_preserved(self, store, config_path):
        original = json.loads(config_path.read_text())
        with _patch_strategies((_WINNER_ID, _WINNER_ORDER, "Winner")), \
                patch(f"{MODULE}._has_uncommitted_changes", return_value=False):
            promote_best_combination(store, Path("unused"), config_path, seed=_SEED)

        written = json.loads(config_path.read_text())
        # Top-level keys other than parameters are untouched.
        assert written["config_name"] == original["config_name"]
        assert written["description"] == original["description"]
        # Every parameters key except DRAFT_ORDER and the 6 promoted params is unchanged.
        promoted_sections = {
            "DRAFT_ORDER", "SAME_POS_BYE_WEIGHT",
            "DIFF_POS_BYE_WEIGHT", "DRAFT_ORDER_BONUSES", "ADP_SCORING",
            "PLAYER_RATING_SCORING",
        }
        for key, value in original["parameters"].items():
            if key not in promoted_sections:
                assert written["parameters"][key] == value, f"{key} was mutated"

    def test_ranks_by_cumulative_not_best(self, tmp_path, config_path):
        # A: high single-run best (0.9) but low cumulative (90/200 = 0.45).
        # B: lower best (0.6) but higher cumulative (60/100 = 0.6) -> B must win.
        #
        # T62: the counts are 10x the original 9/20 vs 6/10 so BOTH clear
        # DEFAULT_MIN_SHORTLIST_GAMES = 30 and the shortlist is non-empty. The rates — and
        # therefore the test's intent — are unchanged, and the Wilson lower bounds preserve
        # the ordering: LCB_A = 0.393 < LCB_B = 0.518 (both computed at the one-sided 0.95
        # level). Because the module's autouse stub returns the same re-measurement for every
        # candidate, the delta tie falls through to compute_promotion's strict `>` and the
        # first-by-LCB candidate (B) is promoted — so this still asserts the RANKING.
        alpha_order = [{"round": 1, "position": "QB"}]
        mgr = SweepResultsManager(tmp_path / "sweep.json")
        mgr.update("1_alpha.json", _LIVE_PARAMS, 0.9, 90, 100)
        mgr.update("1_alpha.json", _LIVE_PARAMS, 0.0, 0, 100)
        mgr.update(_WINNER_ID, _WINNER_PARAMS, 0.6, 60, 100)
        mgr.set_discriminating(True)

        with _patch_strategies(
            ("1_alpha.json", alpha_order, "Alpha"),
            (_WINNER_ID, _WINNER_ORDER, "Winner"),
        ), patch(f"{MODULE}._has_uncommitted_changes", return_value=False):
            result = promote_best_combination(mgr, Path("unused"), config_path, seed=_SEED)

        # B (the higher-cumulative, higher-LCB combo) is promoted, not A.
        assert result["strategy_id"] == _WINNER_ID
        written = json.loads(config_path.read_text())
        assert written["parameters"]["DRAFT_ORDER"] == _WINNER_ORDER
        assert extract_draft_param_values(written) == _WINNER_PARAMS

    # --- Step 3: error paths converge to ConfigurationError, no write -------

    def test_empty_store_raises_no_write(self, tmp_path, config_path):
        mgr = SweepResultsManager(tmp_path / "empty.json")
        mgr.set_discriminating(True)
        before = config_path.read_bytes()
        with pytest.raises(ConfigurationError):
            promote_best_combination(mgr, Path("unused"), config_path, seed=_SEED)
        assert config_path.read_bytes() == before

    def test_strategy_absent_raises_no_write(self, store, config_path):
        before = config_path.read_bytes()
        with _patch_strategies(("9_other.json", [{"round": 1}], "Other")), \
                pytest.raises(ConfigurationError):
            promote_best_combination(store, Path("unused"), config_path, seed=_SEED)
        assert config_path.read_bytes() == before

    def test_load_strategies_filenotfound_raises_no_write(self, store, config_path):
        before = config_path.read_bytes()
        with patch(f"{MODULE}.load_valid_strategies",
                   side_effect=FileNotFoundError("no strategy files")), \
                pytest.raises(ConfigurationError):
            promote_best_combination(store, Path("unused"), config_path, seed=_SEED)
        assert config_path.read_bytes() == before

    def test_config_missing_raises_no_write(self, store, tmp_path):
        missing = tmp_path / "does_not_exist.json"
        with _patch_strategies((_WINNER_ID, _WINNER_ORDER, "Winner")), \
                pytest.raises(ConfigurationError):
            promote_best_combination(store, Path("unused"), missing, seed=_SEED)
        assert not missing.exists()

    # --- Step 4: git warning, graceful probe, write-failure safety ----------

    def test_dirty_state_warns_and_writes(self, store, config_path):
        with _patch_strategies((_WINNER_ID, _WINNER_ORDER, "Winner")), \
                patch(f"{MODULE}._has_uncommitted_changes", return_value=True), \
                patch(f"{MODULE}.logger", MagicMock()) as mock_logger:
            promote_best_combination(store, Path("unused"), config_path, seed=_SEED)

        assert mock_logger.warning.called
        written = json.loads(config_path.read_text())
        assert extract_draft_param_values(written) == _WINNER_PARAMS

    def test_clean_state_no_warning(self, store, config_path):
        with _patch_strategies((_WINNER_ID, _WINNER_ORDER, "Winner")), \
                patch(f"{MODULE}._has_uncommitted_changes", return_value=False), \
                patch(f"{MODULE}.logger", MagicMock()) as mock_logger:
            promote_best_combination(store, Path("unused"), config_path, seed=_SEED)

        assert not mock_logger.warning.called
        written = json.loads(config_path.read_text())
        assert extract_draft_param_values(written) == _WINNER_PARAMS

    def test_git_swallows_subprocess_failure(self, tmp_path):
        target = tmp_path / "league_config.json"
        # git missing / OS error
        with patch(f"{MODULE}.subprocess.run", side_effect=OSError("git not found")):
            assert config_promoter._has_uncommitted_changes(target) is False
        # non-zero exit (check=True -> CalledProcessError, a SubprocessError)
        with patch(f"{MODULE}.subprocess.run",
                   side_effect=subprocess.CalledProcessError(128, "git")):
            assert config_promoter._has_uncommitted_changes(target) is False

    def test_write_failure_wraps_and_cleans_tmp(self, store, config_path):
        before = config_path.read_bytes()
        tmp_sibling = config_path.with_suffix(".tmp")
        with _patch_strategies((_WINNER_ID, _WINNER_ORDER, "Winner")), \
                patch(f"{MODULE}._has_uncommitted_changes", return_value=False), \
                patch.object(Path, "replace", side_effect=OSError("disk full")), \
                pytest.raises(FileOperationError):
            promote_best_combination(store, Path("unused"), config_path, seed=_SEED)

        # Original config untouched and no orphaned .tmp left behind.
        assert config_path.read_bytes() == before
        assert not tmp_sibling.exists()

    # --- Step 5: deterministic tie-break, order-independent (T12) -----------

    def test_tie_break_is_order_independent(self, tmp_path):
        """
        On an exact win_rate AND games tie, the promoted winner is the
        lexicographically-smallest strategy_id, independent of insertion order.

        Proved with TWO independent stores: the two tied configs are inserted in
        opposite orders ([X, Y] vs [Y, X]); both stores must promote the same
        smallest-strategy_id winner. A single shared store could not prove
        order-independence — both records would coexist in one resulting order.
        """
        # Arrange — two configs tied on BOTH win_rate AND games. They share the
        # 6 params (so make_combo_key's param suffix is identical) and differ only
        # by strategy_id, forcing the (-win_rate, -games, combo_key) sort to fall
        # through to combo_key, i.e. the strategy_id prefix. "1_aaa" < "2_bbb".
        smaller_id = "1_aaa.json"
        larger_id = "2_bbb.json"
        shared_params = _WINNER_PARAMS
        smaller_order = [{"round": 1, "position": "RB"}]
        larger_order = [{"round": 1, "position": "WR"}]

        store_a = SweepResultsManager(tmp_path / "store_a.json")
        store_a.update(smaller_id, shared_params, 0.5, 50, 100)  # X first
        store_a.update(larger_id, shared_params, 0.5, 50, 100)   # then Y
        store_a.set_discriminating(True)

        store_b = SweepResultsManager(tmp_path / "store_b.json")
        store_b.update(larger_id, shared_params, 0.5, 50, 100)   # Y first
        store_b.update(smaller_id, shared_params, 0.5, 50, 100)  # then X
        store_b.set_discriminating(True)

        strategies = (
            (smaller_id, smaller_order, "Smaller"),
            (larger_id, larger_order, "Larger"),
        )

        # Act — promote from each independent store to its own throwaway config.
        with _patch_strategies(*strategies), \
                patch(f"{MODULE}._has_uncommitted_changes", return_value=False):
            result_a = promote_best_combination(
                store_a, Path("unused"), _fresh_config(tmp_path, "config_a.json"),
                seed=_SEED)
            result_b = promote_best_combination(
                store_b, Path("unused"), _fresh_config(tmp_path, "config_b.json"),
                seed=_SEED)

        # Assert — both promote the smallest strategy_id, regardless of order.
        assert result_a["strategy_id"] == smaller_id
        assert result_b["strategy_id"] == smaller_id
        assert result_a["strategy_id"] == result_b["strategy_id"]


class TestPromoteGuard:
    """T54/D3: promote guard blocks non-discriminating stores, passes discriminating ones."""

    def test_compute_promotion_blocks_when_flag_absent(self, tmp_path, config_path):
        """Guard blocks when discriminating flag absent (pre-fix store)."""
        mgr = SweepResultsManager(tmp_path / "sweep.json")
        mgr.update(_WINNER_ID, _WINNER_PARAMS, 0.75, 75, 100)
        # Do NOT call set_discriminating — pre-fix store
        before = config_path.read_bytes()

        with pytest.raises(ConfigurationError, match="Refusing to promote"):
            compute_promotion(mgr, Path("unused"), config_path, seed=_SEED)

        assert config_path.read_bytes() == before

    def test_compute_promotion_blocks_when_flag_false(self, tmp_path, config_path):
        """Guard blocks when discriminating flag explicitly False."""
        mgr = SweepResultsManager(tmp_path / "sweep.json")
        mgr.update(_WINNER_ID, _WINNER_PARAMS, 0.75, 75, 100)
        mgr.set_discriminating(False)
        before = config_path.read_bytes()

        with pytest.raises(ConfigurationError, match="Refusing to promote"):
            compute_promotion(mgr, Path("unused"), config_path, seed=_SEED)

        assert config_path.read_bytes() == before

    def test_promote_best_combination_blocks_when_flag_absent(self, tmp_path, config_path):
        """Guard blocks write entry point when flag absent."""
        mgr = SweepResultsManager(tmp_path / "sweep.json")
        mgr.update(_WINNER_ID, _WINNER_PARAMS, 0.75, 75, 100)
        # Do NOT call set_discriminating
        before = config_path.read_bytes()

        with pytest.raises(ConfigurationError, match="Refusing to promote"):
            promote_best_combination(mgr, Path("unused"), config_path, seed=_SEED)

        assert config_path.read_bytes() == before

    def test_promote_succeeds_when_flag_true(self, store, config_path):
        """Promote succeeds when store is discriminating."""
        with _patch_strategies((_WINNER_ID, _WINNER_ORDER, "Winner")), \
                patch(f"{MODULE}._has_uncommitted_changes", return_value=False):
            result = promote_best_combination(store, Path("unused"), config_path, seed=_SEED)

        # Promote succeeds -> result contains the promoted combination.
        assert result["strategy_id"] == _WINNER_ID
        assert result["param_values"] == _WINNER_PARAMS


class TestComputePromotion:
    """compute_promotion: the no-write preview computation behind a bare --promote."""

    def test_compute_promotion_no_write(self, store, config_path):
        before = config_path.read_bytes()
        with _patch_strategies((_WINNER_ID, _WINNER_ORDER, "Winner")):
            plan = compute_promotion(store, Path("unused"), config_path, seed=_SEED)

        # No write occurred.
        assert config_path.read_bytes() == before
        # Plan carries the winner + the proposed config (not yet on disk).
        assert plan["strategy_id"] == _WINNER_ID
        assert plan["param_values"] == _WINNER_PARAMS
        assert extract_draft_param_values(plan["new_config"]) == _WINNER_PARAMS
        assert plan["new_config"]["parameters"]["DRAFT_ORDER"] == _WINNER_ORDER

    def test_compute_promotion_diff_current_to_proposed(self, store, config_path):
        current = extract_draft_param_values(json.loads(config_path.read_text()))
        with _patch_strategies((_WINNER_ID, _WINNER_ORDER, "Winner")):
            plan = compute_promotion(store, Path("unused"), config_path, seed=_SEED)

        diff = plan["diff"]
        # Every changed draft-side param shows the live current -> the winner's value.
        for name, winner_value in _WINNER_PARAMS.items():
            if current[name] != winner_value:
                assert diff[name] == {"current": current[name], "proposed": winner_value}
        # The winner's DRAFT_ORDER differs from the live order, so it is in the diff.
        assert "DRAFT_ORDER" in diff
        assert diff["DRAFT_ORDER"]["proposed"] == _WINNER_ORDER

    def test_compute_promotion_empty_store_raises_no_write(self, tmp_path, config_path):
        mgr = SweepResultsManager(tmp_path / "empty.json")
        before = config_path.read_bytes()
        with pytest.raises(ConfigurationError):
            compute_promotion(mgr, Path("unused"), config_path, seed=_SEED)
        assert config_path.read_bytes() == before

    def test_compute_promotion_non_tty_no_write(self, store, config_path):
        # The flag, not the TTY, is the gate: even simulating a non-TTY stdout, the
        # preview computation writes nothing (no isatty/EOF dependency on this path).
        before = config_path.read_bytes()
        with _patch_strategies((_WINNER_ID, _WINNER_ORDER, "Winner")), \
                patch("sys.stdout.isatty", return_value=False):
            compute_promotion(store, Path("unused"), config_path, seed=_SEED)
        assert config_path.read_bytes() == before

    def test_compute_promotion_structurally_incomplete_config_raises(self, store, tmp_path):
        # A valid-JSON config that is structurally incomplete (missing "parameters")
        # must raise ConfigurationError, NOT a bare KeyError/TypeError.
        # The incomplete file sits INSIDE a valid configs/ root (T62): ConfigManager merges the
        # sibling league_config.json fine, so compute_promotion gets past the merge and the
        # structurally-incomplete RAW dict reaches apply_draft_overrides — which is the code path
        # this test exists to pin. Without the valid root the merge would raise first and the
        # assertion would pass for the wrong reason.
        incomplete = _make_config_root(tmp_path, "incomplete").parent / "incomplete_config.json"
        incomplete.write_text(json.dumps({"config_name": "stub", "description": "no parameters"}))
        with _patch_strategies((_WINNER_ID, _WINNER_ORDER, "Winner")), \
                pytest.raises(ConfigurationError):
            compute_promotion(store, Path("unused"), incomplete, seed=_SEED)


# ---------------------------------------------------------------------------
# T62 NEW COVERAGE (test_build_plan.md). Everything below tests behaviour that
# did not exist before the Wilson shortlist + fresh re-measurement landed.
# ---------------------------------------------------------------------------

def _result(delta=0.05, z=5.0, recommended_rate=0.55, games=1700):
    """Build a PairedComparisonResult with the fields the promote gate and CI reader use.

    Defaults CLEAR the gate: delta > 0 and z / CLUSTER_SE_INFLATION = 5.0 / 1.28 = 3.906,
    comfortably above the one-sided 0.95 critical value 1.645.
    """
    return PairedComparisonResult(
        current_rate=recommended_rate - delta,
        recommended_rate=recommended_rate,
        delta=delta,
        z=z,
        games=games,
        seed=_SEED,
    )


def _stub_comparator(result):
    """Patch the comparator with a fixed result, KEEPING the merged-arm guard in force.

    Nests inside (and takes precedence over) the module's autouse stub_comparator fixture, per
    that fixture's documented contract. It re-applies _assert_simulator_ready deliberately: a
    bare return_value here would create a hole in exactly the guard the T62 amendment added.
    """
    def _side_effect(current_config, recommended_config, *args, **kwargs):
        _assert_simulator_ready(current_config, "current")
        _assert_simulator_ready(recommended_config, "recommended")
        return result

    return patch(f"{MODULE}.run_paired_ab_comparison", side_effect=_side_effect)


# 31 configs sharing ONE true rate of exactly 0.500, differing only by per-combo noise:
# wins 70..100 over 170 games. mean(70..100) = 85 = 0.500 * 170, so the true rate is 0.500 by
# construction, while the in-sample MAXIMUM is 100/170 = 0.5882 — 0.088 above the truth purely
# by selection. That gap IS the bug this story fixes. The noise is written out explicitly
# rather than sampled, so the fixture is deterministic with no RNG dependency.
_EQUAL_RATE_GAMES = 170
_EQUAL_RATE_WINS = list(range(70, 101))


def _equal_true_rate_store(tmp_path):
    """A synthetic store of equal-true-rate combos with per-combo noise (T62 regression)."""
    mgr = SweepResultsManager(tmp_path / "equal_rate_sweep.json")
    for index, wins in enumerate(_EQUAL_RATE_WINS):
        mgr.update(
            f"{index}_noise.json", _WINNER_PARAMS,
            wins / _EQUAL_RATE_GAMES, wins, _EQUAL_RATE_GAMES,
        )
    mgr.set_discriminating(True)
    return mgr


def _patch_equal_rate_strategies():
    """Resolve a DRAFT_ORDER for every synthetic equal-true-rate config."""
    return _patch_strategies(*[
        (f"{index}_noise.json", _WINNER_ORDER, f"Noise {index}")
        for index in range(len(_EQUAL_RATE_WINS))
    ])


class TestMaxSelectionBiasRegression:
    """T62: the promoted headline is the FRESH re-measurement, never the store's maximum."""

    def test_equal_true_rate_store_does_not_promote_an_inflated_rate(self, tmp_path, config_path):
        # THE regression test (spec.md "New coverage required", bullet 1). 31 configs share one
        # true rate (0.500) and differ only by noise, so the store's maximum (100/170 = 0.5882)
        # overstates the truth by ~0.088 by selection alone. The comparator is stubbed to
        # return the TRUE rate 0.500, standing in for honest fresh evidence.
        #
        # THIS FAILS TODAY: compute_promotion returns rank_combinations(...)[0] and reports its
        # 0.5882 store maximum as "win_rate" — there is no separate re-measured headline at all,
        # so neither of the first two assertions can even be expressed against today's code.
        mgr = _equal_true_rate_store(tmp_path)
        with _patch_equal_rate_strategies(), \
                _stub_comparator(_result(delta=0.02, z=5.0, recommended_rate=0.50)), \
                patch(f"{MODULE}._has_uncommitted_changes", return_value=False):
            result = promote_best_combination(
                mgr, Path("unused"), config_path, seed=_SEED, shortlist=3
            )

        # The reported headline is the fresh measurement, at the TRUE rate.
        assert result["remeasured_rate"] == 0.50
        # The store's in-sample maximum is retained, but only as a separately labelled field.
        assert result["max_selected_win_rate"] == pytest.approx(100 / _EQUAL_RATE_GAMES)
        # The headline is BELOW the store maximum: the selection inflation is not promoted.
        assert result["remeasured_rate"] < result["max_selected_win_rate"]
        # The two are distinct labelled fields, never one conflated number.
        assert "win_rate" not in result
        assert "games" not in result

    def test_shortlist_winner_is_reported_with_its_k(self, tmp_path, config_path):
        # The residual max-over-K bias is disclosed, not hidden: K is carried in the result so
        # both printers can label the headline "winner of a K-way re-measurement".
        mgr = _equal_true_rate_store(tmp_path)
        with _patch_equal_rate_strategies(), \
                _stub_comparator(_result()), \
                patch(f"{MODULE}._has_uncommitted_changes", return_value=False):
            result = promote_best_combination(
                mgr, Path("unused"), config_path, seed=_SEED, shortlist=3
            )
        assert result["shortlist_size"] == 3
        assert result["seed"] == _SEED


class TestPromoteRefusals:
    """T62/D2: every NEW no-write refusal path, each asserted byte-unchanged on disk."""

    def test_refuses_when_no_candidate_clears_significance(self, store, config_path):
        # spec.md "New coverage required", bullet 4 — the headline refusal, with the file-level
        # no-write assertions mirroring the existing test_write_failure_wraps_and_cleans_tmp
        # idiom (config_path.read_bytes() == before, no orphaned .tmp).
        before = config_path.read_bytes()
        tmp_sibling = config_path.with_suffix(".tmp")
        with _patch_strategies((_WINNER_ID, _WINNER_ORDER, "Winner")), \
                _stub_comparator(_result(delta=0.001, z=0.4)), \
                pytest.raises(ConfigurationError, match="Refusing to promote"):
            promote_best_combination(store, Path("unused"), config_path, seed=_SEED)

        assert config_path.read_bytes() == before
        assert not tmp_sibling.exists()

    def test_refuses_when_delta_is_negative_even_at_high_z(self, store, config_path):
        # delta > 0 is required IN ADDITION to significance: a significantly WORSE candidate is
        # exactly the case a z-only gate would happily write.
        before = config_path.read_bytes()
        with _patch_strategies((_WINNER_ID, _WINNER_ORDER, "Winner")), \
                _stub_comparator(_result(delta=-0.05, z=5.0)), \
                pytest.raises(ConfigurationError, match="Refusing to promote"):
            promote_best_combination(store, Path("unused"), config_path, seed=_SEED)

        assert config_path.read_bytes() == before

    def test_refuses_when_every_combination_is_below_the_games_floor(self, tmp_path, config_path):
        # spec.md "New coverage required", bullet 3 (the empty-shortlist half).
        mgr = SweepResultsManager(tmp_path / "tiny.json")
        mgr.update(_WINNER_ID, _WINNER_PARAMS, 0.75, 15, 20)  # 20 games < the 30-game floor
        mgr.set_discriminating(True)
        before = config_path.read_bytes()

        with _patch_strategies((_WINNER_ID, _WINNER_ORDER, "Winner")), \
                pytest.raises(
                    ConfigurationError,
                    match=f"at least {DEFAULT_MIN_SHORTLIST_GAMES} recorded games"):
            promote_best_combination(mgr, Path("unused"), config_path, seed=_SEED)

        assert config_path.read_bytes() == before

    def test_comparator_missing_seasons_becomes_configuration_error_no_write(self, store, config_path):
        # spec.md "New coverage required", bullet 6 (FileNotFoundError half). Unwrapped, this
        # would escape _run_promote_mode's (ConfigurationError, FileOperationError) catch as a
        # bare traceback (run_win_rate_simulation.py:386).
        before = config_path.read_bytes()
        with _patch_strategies((_WINNER_ID, _WINNER_ORDER, "Winner")), \
                patch(f"{MODULE}.run_paired_ab_comparison",
                      side_effect=FileNotFoundError(
                          "no historical season folders (20XX/) found")), \
                pytest.raises(ConfigurationError,
                              match="Cannot re-measure promotion candidates"):
            promote_best_combination(store, Path("unused"), config_path, seed=_SEED)

        assert config_path.read_bytes() == before

    def test_comparator_all_seasons_invalid_becomes_configuration_error_no_write(self, store, config_path):
        # spec.md "New coverage required", bullet 6 (ValueError half).
        before = config_path.read_bytes()
        with _patch_strategies((_WINNER_ID, _WINNER_ORDER, "Winner")), \
                patch(f"{MODULE}.run_paired_ab_comparison",
                      side_effect=ValueError("no valid games evaluated")), \
                pytest.raises(ConfigurationError,
                              match="Cannot re-measure promotion candidates"):
            promote_best_combination(store, Path("unused"), config_path, seed=_SEED)

        assert config_path.read_bytes() == before

    def test_config_merge_failure_is_worded_distinctly_from_the_data_folder_failure(self, store, tmp_path):
        # Both failure modes raise ConfigurationError, so only the WORDING keeps them apart —
        # which is Step 8-A's entire reason for being a named helper. A configs/ root holding
        # league_config.json but NO week*.json siblings makes ConfigManager raise
        # "Config missing required parameters: NORMALIZATION_MAX_SCALE, ..." (verified against
        # the current tree), which _build_simulation_base_config wraps.
        root = tmp_path / "no_week_files" / "configs"
        root.mkdir(parents=True)
        shutil.copyfile(Path("data/configs/league_config.json"), root / "league_config.json")

        with _patch_strategies((_WINNER_ID, _WINNER_ORDER, "Winner")), \
                pytest.raises(ConfigurationError, match="CONFIG problem") as exc:
            compute_promotion(
                store, Path("unused"), root / "league_config.json", seed=_SEED
            )

        assert "Cannot re-measure promotion candidates" not in str(exc.value)
        assert "merged simulation config" in str(exc.value)


class TestClusteringInflationAndConfigSplit:
    """T62/D5 asymmetry + the 2026-07-20 raw-vs-merged amendment."""

    def test_decision_z_is_clustering_inflated(self, store, config_path):
        # spec.md "New coverage required", bullet 5 (the decision half). z = 2.00 clears the RAW
        # one-sided 0.95 critical value 1.6449 but NOT the clustering-adjusted gate:
        # 2.00 / 1.28 = 1.5625 < 1.6449. If the 1.28 were applied only to the DISPLAYED
        # interval and not to the decision, this candidate would be written.
        before = config_path.read_bytes()
        with _patch_strategies((_WINNER_ID, _WINNER_ORDER, "Winner")), \
                _stub_comparator(_result(delta=0.05, z=2.00)), \
                pytest.raises(ConfigurationError, match="Refusing to promote"):
            promote_best_combination(store, Path("unused"), config_path, seed=_SEED)

        assert config_path.read_bytes() == before

    def test_just_above_the_inflated_threshold_promotes(self, store, config_path):
        # The positive control for the test above — without it, a bug that refused EVERYTHING
        # would pass. z = 2.11 / 1.28 = 1.6484 >= 1.6449 (the threshold sits at z = 2.1054).
        with _patch_strategies((_WINNER_ID, _WINNER_ORDER, "Winner")), \
                _stub_comparator(_result(delta=0.05, z=2.11)), \
                patch(f"{MODULE}._has_uncommitted_changes", return_value=False):
            result = promote_best_combination(store, Path("unused"), config_path, seed=_SEED)

        assert result["strategy_id"] == _WINNER_ID
        assert result["z"] == 2.11
        assert result["z_adjusted"] == pytest.approx(2.11 / CLUSTER_SE_INFLATION)

    def test_reported_interval_is_the_inflated_wilson_interval(self, store, config_path):
        # spec.md "New coverage required", bullet 5 (the reported-interval half).
        # 935/1700 -> plain (0.526265, 0.573510); x1.28 -> (0.519600, 0.580031). Executed
        # before being written down. wins is reconstructed as round(0.55 * 1700) = 935.
        with _patch_strategies((_WINNER_ID, _WINNER_ORDER, "Winner")), \
                _stub_comparator(
                    _result(delta=0.05, z=5.0, recommended_rate=0.55, games=1700)), \
                patch(f"{MODULE}._has_uncommitted_changes", return_value=False):
            result = promote_best_combination(store, Path("unused"), config_path, seed=_SEED)

        low, high = result["remeasured_ci"]
        assert (round(low, 6), round(high, 6)) == (0.5196, 0.580031)
        # Identical to calling the helper with the inflation, and strictly wider without it.
        assert (low, high) == wilson_interval(
            935, 1700, DEFAULT_CONFIDENCE, se_inflation=CLUSTER_SE_INFLATION
        )
        plain_low, plain_high = wilson_interval(935, 1700, DEFAULT_CONFIDENCE)
        assert low < plain_low
        assert high > plain_high

    def test_comparator_receives_merged_arms_while_the_write_stays_raw(self, store, config_path):
        # The 2026-07-20 amendment's defect captured as one test (coverage bullet h). The
        # module's autouse guard already covers the first half for all 22 existing tests; the
        # SECOND half — that the WRITE arm is not contaminated with the four week-file-derived
        # parameters — is asserted only here. A "fix" that merged everything into one dict
        # would satisfy the autouse guard and silently inflate league_config.json.
        seen = {}

        def _capture(current_config, recommended_config, *args, **kwargs):
            seen["current"] = current_config
            seen["recommended"] = recommended_config
            return _result()

        with _patch_strategies((_WINNER_ID, _WINNER_ORDER, "Winner")), \
                patch(f"{MODULE}.run_paired_ab_comparison", side_effect=_capture):
            plan = compute_promotion(store, Path("unused"), config_path, seed=_SEED)

        # Direction 1 — both SIMULATE arms are the ConfigManager-merged config.
        for arm in ("current", "recommended"):
            for name in _SIMULATOR_REQUIRED_PARAMS:
                assert name in seen[arm]["parameters"], (
                    f"the {arm} arm is the RAW config — SimulatedLeague would raise "
                    f"'Config missing required parameters'"
                )
        # Direction 2 — the WRITE arm is raw-derived and carries none of them.
        for name in _SIMULATOR_REQUIRED_PARAMS:
            assert name not in plan["new_config"]["parameters"], (
                f"{name} leaked into the config that gets written to league_config.json — the "
                f"MERGED dict was used for the WRITE path"
            )
        # Both arms describe the same candidate; only parameter completeness differs.
        assert seen["recommended"]["parameters"]["DRAFT_ORDER"] == _WINNER_ORDER
