"""
Tests for simulation.win_rate.config_promoter.

Covers the live-config promotion writer: promoting the top-ranked combination's
DRAFT_ORDER + 7 params, preserving all other keys, cumulative-win-rate ranking
(not best_win_rate), the four error paths that converge to ConfigurationError with
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
from simulation.win_rate.config_promoter import promote_best_combination
from simulation.win_rate.config_overrides import extract_draft_param_values
from simulation.win_rate.SweepResultsManager import SweepResultsManager
from utils.error_handler import ConfigurationError, FileOperationError

MODULE = "simulation.win_rate.config_promoter"

# The live config's current values for the 7 draft-side params.
_LIVE_PARAMS = {
    "DRAFT_NORMALIZATION_MAX_SCALE": 150,
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
    "DRAFT_NORMALIZATION_MAX_SCALE": 130,
    "SAME_POS_BYE_WEIGHT": 0.20,
    "DIFF_POS_BYE_WEIGHT": 0.05,
    "PRIMARY_BONUS": 90,
    "SECONDARY_BONUS": 100,
    "ADP_SCORING_WEIGHT": 3.00,
    "PLAYER_RATING_SCORING_WEIGHT": 2.00,
}

_WINNER_ORDER = [{"round": 1, "position": "RB"}, {"round": 2, "position": "WR"}]
_WINNER_ID = "2_winner.json"


@pytest.fixture
def config_path(tmp_path):
    """A tmp_path copy of the real league_config.json (real structure, never mutated source)."""
    dest = tmp_path / "league_config.json"
    shutil.copyfile(Path("data/configs/league_config.json"), dest)
    return dest


@pytest.fixture
def store(tmp_path):
    """A real SweepResultsManager holding the winning combination as the sole entry."""
    mgr = SweepResultsManager(tmp_path / "sweep.json")
    mgr.update(_WINNER_ID, _WINNER_PARAMS, 0.75, 75, 100)
    return mgr


def _patch_strategies(*triples):
    """Patch load_valid_strategies on the module to return the given (filename, order, name) triples."""
    return patch(f"{MODULE}.load_valid_strategies", return_value=(list(triples), 0))


def _fresh_config(tmp_path, name):
    """A fresh tmp copy of the real league_config.json under `name` (never the source)."""
    dest = tmp_path / name
    shutil.copyfile(Path("data/configs/league_config.json"), dest)
    return dest


class TestConfigPromoter:
    # --- Step 1: happy path -------------------------------------------------

    def test_promotes_winner_draft_order_and_params(self, store, config_path):
        with _patch_strategies((_WINNER_ID, _WINNER_ORDER, "Winner")), \
                patch(f"{MODULE}._has_uncommitted_changes", return_value=False):
            promote_best_combination(store, Path("unused"), config_path)

        written = json.loads(config_path.read_text())
        assert written["parameters"]["DRAFT_ORDER"] == _WINNER_ORDER
        assert extract_draft_param_values(written) == _WINNER_PARAMS

    def test_returns_exactly_four_keys(self, store, config_path):
        with _patch_strategies((_WINNER_ID, _WINNER_ORDER, "Winner")), \
                patch(f"{MODULE}._has_uncommitted_changes", return_value=False):
            result = promote_best_combination(store, Path("unused"), config_path)

        assert set(result) == {"strategy_id", "param_values", "win_rate", "games"}
        assert result["strategy_id"] == _WINNER_ID
        assert result["param_values"] == _WINNER_PARAMS
        assert result["games"] == 100

    # --- Step 2: preservation + cumulative ranking --------------------------

    def test_other_keys_preserved(self, store, config_path):
        original = json.loads(config_path.read_text())
        with _patch_strategies((_WINNER_ID, _WINNER_ORDER, "Winner")), \
                patch(f"{MODULE}._has_uncommitted_changes", return_value=False):
            promote_best_combination(store, Path("unused"), config_path)

        written = json.loads(config_path.read_text())
        # Top-level keys other than parameters are untouched.
        assert written["config_name"] == original["config_name"]
        assert written["description"] == original["description"]
        # Every parameters key except DRAFT_ORDER and the 7 promoted params is unchanged.
        promoted_sections = {
            "DRAFT_ORDER", "DRAFT_NORMALIZATION_MAX_SCALE", "SAME_POS_BYE_WEIGHT",
            "DIFF_POS_BYE_WEIGHT", "DRAFT_ORDER_BONUSES", "ADP_SCORING",
            "PLAYER_RATING_SCORING",
        }
        for key, value in original["parameters"].items():
            if key not in promoted_sections:
                assert written["parameters"][key] == value, f"{key} was mutated"

    def test_ranks_by_cumulative_not_best(self, tmp_path, config_path):
        # A: high single-run best (0.9) but low cumulative (9/20 = 0.45).
        # B: lower best (0.6) but higher cumulative (6/10 = 0.6) -> B must win.
        alpha_order = [{"round": 1, "position": "QB"}]
        mgr = SweepResultsManager(tmp_path / "sweep.json")
        mgr.update("1_alpha.json", _LIVE_PARAMS, 0.9, 9, 10)
        mgr.update("1_alpha.json", _LIVE_PARAMS, 0.0, 0, 10)
        mgr.update(_WINNER_ID, _WINNER_PARAMS, 0.6, 6, 10)

        with _patch_strategies(
            ("1_alpha.json", alpha_order, "Alpha"),
            (_WINNER_ID, _WINNER_ORDER, "Winner"),
        ), patch(f"{MODULE}._has_uncommitted_changes", return_value=False):
            result = promote_best_combination(mgr, Path("unused"), config_path)

        # B (the higher-cumulative combo) is promoted, not A (higher best_win_rate).
        assert result["strategy_id"] == _WINNER_ID
        written = json.loads(config_path.read_text())
        assert written["parameters"]["DRAFT_ORDER"] == _WINNER_ORDER
        assert extract_draft_param_values(written) == _WINNER_PARAMS

    # --- Step 3: error paths converge to ConfigurationError, no write -------

    def test_empty_store_raises_no_write(self, tmp_path, config_path):
        mgr = SweepResultsManager(tmp_path / "empty.json")
        before = config_path.read_bytes()
        with pytest.raises(ConfigurationError):
            promote_best_combination(mgr, Path("unused"), config_path)
        assert config_path.read_bytes() == before

    def test_strategy_absent_raises_no_write(self, store, config_path):
        before = config_path.read_bytes()
        with _patch_strategies(("9_other.json", [{"round": 1}], "Other")), \
                pytest.raises(ConfigurationError):
            promote_best_combination(store, Path("unused"), config_path)
        assert config_path.read_bytes() == before

    def test_load_strategies_filenotfound_raises_no_write(self, store, config_path):
        before = config_path.read_bytes()
        with patch(f"{MODULE}.load_valid_strategies",
                   side_effect=FileNotFoundError("no strategy files")), \
                pytest.raises(ConfigurationError):
            promote_best_combination(store, Path("unused"), config_path)
        assert config_path.read_bytes() == before

    def test_config_missing_raises_no_write(self, store, tmp_path):
        missing = tmp_path / "does_not_exist.json"
        with _patch_strategies((_WINNER_ID, _WINNER_ORDER, "Winner")), \
                pytest.raises(ConfigurationError):
            promote_best_combination(store, Path("unused"), missing)
        assert not missing.exists()

    # --- Step 4: git warning, graceful probe, write-failure safety ----------

    def test_dirty_state_warns_and_writes(self, store, config_path):
        with _patch_strategies((_WINNER_ID, _WINNER_ORDER, "Winner")), \
                patch(f"{MODULE}._has_uncommitted_changes", return_value=True), \
                patch(f"{MODULE}.logger", MagicMock()) as mock_logger:
            promote_best_combination(store, Path("unused"), config_path)

        assert mock_logger.warning.called
        written = json.loads(config_path.read_text())
        assert extract_draft_param_values(written) == _WINNER_PARAMS

    def test_clean_state_no_warning(self, store, config_path):
        with _patch_strategies((_WINNER_ID, _WINNER_ORDER, "Winner")), \
                patch(f"{MODULE}._has_uncommitted_changes", return_value=False), \
                patch(f"{MODULE}.logger", MagicMock()) as mock_logger:
            promote_best_combination(store, Path("unused"), config_path)

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
            promote_best_combination(store, Path("unused"), config_path)

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
        # 7 params (so make_combo_key's param suffix is identical) and differ only
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

        store_b = SweepResultsManager(tmp_path / "store_b.json")
        store_b.update(larger_id, shared_params, 0.5, 50, 100)   # Y first
        store_b.update(smaller_id, shared_params, 0.5, 50, 100)  # then X

        strategies = (
            (smaller_id, smaller_order, "Smaller"),
            (larger_id, larger_order, "Larger"),
        )

        # Act — promote from each independent store to its own throwaway config.
        with _patch_strategies(*strategies), \
                patch(f"{MODULE}._has_uncommitted_changes", return_value=False):
            result_a = promote_best_combination(
                store_a, Path("unused"), _fresh_config(tmp_path, "config_a.json"))
            result_b = promote_best_combination(
                store_b, Path("unused"), _fresh_config(tmp_path, "config_b.json"))

        # Assert — both promote the smallest strategy_id, regardless of order.
        assert result_a["strategy_id"] == smaller_id
        assert result_b["strategy_id"] == smaller_id
        assert result_a["strategy_id"] == result_b["strategy_id"]
