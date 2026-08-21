"""Season-scoped week-stat selection in DataExporter.

Covers the defect measured live on 2026-08-18: ESPN returns entries for
MULTIPLE seasons under the same scoringPeriodId, and the exporter matched on
(scoringPeriodId, statSourceId) alone, taking whichever sorted first. Because a
team's PRIOR-season bye week carries appliedTotal 0.0, that read blanked the
entire roster for one non-bye week -- 24 of 32 teams in the 2026 corpus.
"""

from types import SimpleNamespace

import pytest

from player_data_fetcher.player_data_exporter import DataExporter
from player_data_fetcher.player_data_models import ESPNPlayerData


CURRENT_SEASON = 2026
PRIOR_SEASON = 2025


def _exporter(tmp_path, season=CURRENT_SEASON, current_nfl_week=1):
    """Build a DataExporter scoped to `season`, or to no season when None."""
    return DataExporter(
        output_dir=str(tmp_path),
        current_nfl_week=current_nfl_week,
        position_json_output=str(tmp_path / "player_data"),
        team_data_folder=str(tmp_path / "team_data"),
        espn_settings=None if season is None else SimpleNamespace(season=season),
    )


def _player(raw_stats):
    return ESPNPlayerData(
        id="1", name="Test Player", team="DET", position="RB", raw_stats=raw_stats
    )


def _stat(season, week, source, total):
    return {
        "seasonId": season,
        "scoringPeriodId": week,
        "statSourceId": source,
        "appliedTotal": total,
    }


class TestProjectedPointsSeasonScoping:
    def test_prior_season_bye_zero_does_not_mask_current_season_projection(self, tmp_path):
        """The exact live failure: prior-season 0.0 sorts FIRST for week 8.

        Pre-fix this stored 0.0 (Jahmyr Gibbs week 8 against a true 21.53).
        """
        player = _player([
            _stat(PRIOR_SEASON, 8, 1, 0.0),       # prior-season bye, sorts first
            _stat(CURRENT_SEASON, 8, 1, 21.53),   # the real projection
        ])
        points = _exporter(tmp_path)._get_projected_points_array(player)
        assert points[7] == pytest.approx(21.53)

    def test_order_independence(self, tmp_path):
        """Selection must not depend on raw_stats ordering.

        30 teams had differing byes across the two seasons but only 24 showed the
        defect, which is what ordering-dependent selection looks like.
        """
        forward = _player([_stat(PRIOR_SEASON, 3, 1, 0.0), _stat(CURRENT_SEASON, 3, 1, 12.5)])
        reverse = _player([_stat(CURRENT_SEASON, 3, 1, 12.5), _stat(PRIOR_SEASON, 3, 1, 0.0)])
        exporter = _exporter(tmp_path)
        assert exporter._get_projected_points_array(forward)[2] == pytest.approx(12.5)
        assert exporter._get_projected_points_array(reverse)[2] == pytest.approx(12.5)

    def test_prior_season_value_is_never_substituted(self, tmp_path):
        """A prior-season entry must not be used when the current season is absent.

        Reading 18.0 here would be a plausible-looking WRONG number, which is
        worse than the 0.0 the array already means "no projection" with.
        """
        player = _player([_stat(PRIOR_SEASON, 5, 1, 18.0)])
        assert _exporter(tmp_path)._get_projected_points_array(player)[4] == 0.0

    def test_genuine_current_season_bye_stays_zero(self, tmp_path):
        player = _player([_stat(CURRENT_SEASON, 9, 1, 0.0)])
        assert _exporter(tmp_path)._get_projected_points_array(player)[8] == 0.0

    def test_actuals_are_season_scoped_too(self, tmp_path):
        """Same defect on the actuals path; latent preseason, live once week > 1."""
        player = _player([
            _stat(PRIOR_SEASON, 2, 0, 0.0),
            _stat(CURRENT_SEASON, 2, 0, 14.2),
        ])
        exporter = _exporter(tmp_path, current_nfl_week=5)
        assert exporter._get_actual_points_array(player)[1] == pytest.approx(14.2)

    def test_projection_and_actual_sources_stay_separate(self, tmp_path):
        player = _player([
            _stat(CURRENT_SEASON, 4, 0, 9.9),    # actual
            _stat(CURRENT_SEASON, 4, 1, 15.1),   # projection
        ])
        exporter = _exporter(tmp_path, current_nfl_week=10)
        assert exporter._get_projected_points_array(player)[3] == pytest.approx(15.1)
        assert exporter._get_actual_points_array(player)[3] == pytest.approx(9.9)


class TestUnknownSeasonPreservesPriorBehaviour:
    def test_no_season_skips_filtering(self, tmp_path):
        """historical_data_compiler constructs without espn_settings.

        Its raw_stats come from a single-season fetch, so it has no collision to
        guard against and must keep matching on (period, source) alone.
        """
        player = _player([_stat(PRIOR_SEASON, 6, 1, 11.0)])
        assert _exporter(tmp_path, season=None)._get_projected_points_array(player)[5] == pytest.approx(11.0)


class TestMalformedEntriesAreSkipped:
    @pytest.mark.parametrize("bad", [None, "not-a-number", float("nan")])
    def test_bad_applied_total_does_not_raise_and_yields_zero(self, tmp_path, bad):
        player = _player([_stat(CURRENT_SEASON, 7, 1, bad)])
        assert _exporter(tmp_path)._get_projected_points_array(player)[6] == 0.0

    def test_bad_entry_does_not_hide_a_good_sibling(self, tmp_path):
        player = _player([
            _stat(CURRENT_SEASON, 7, 1, float("nan")),
            _stat(CURRENT_SEASON, 7, 1, 8.4),
        ])
        assert _exporter(tmp_path)._get_projected_points_array(player)[6] == pytest.approx(8.4)

    def test_non_dict_entry_is_skipped(self, tmp_path):
        """Exercised on the helper, not through ESPNPlayerData.

        The model validates raw_stats as List[Dict], so a non-dict cannot reach
        the array builders at all -- the guard is only reachable for a caller
        passing raw ESPN data straight to the helper, which is how the sibling
        ESPNClient._extract_raw_espn_week_points is invoked.
        """
        selected = _exporter(tmp_path)._select_week_stat(
            ["garbage", _stat(CURRENT_SEASON, 7, 1, 8.4)],
            week=7,
            stat_source_id=1,
            season=CURRENT_SEASON,
        )
        assert selected == pytest.approx(8.4)


class TestDetailStatsAreSeasonScoped:
    """The detail-stat path (`_extract_stat_value`), missed by the original fix.

    Symptom: a 2026 preseason pull emitted populated receptions / rushing /
    kicking / defense arrays for games that had not been played, sitting beside
    an all-zero `actual_points` array that the season guard had already fixed.
    """

    def _boxscore(self, season, week, stats):
        entry = _stat(season, week, 0, 0.0)
        entry["stats"] = stats
        return entry

    def test_prior_season_boxscore_is_not_read_as_current_season(self, tmp_path):
        player = _player([self._boxscore(PRIOR_SEASON, 3, {"53": 7.0, "42": 96.0})])
        exporter = _exporter(tmp_path, current_nfl_week=17)
        receiving = exporter._extract_receiving_stats(player)
        assert receiving["receptions"][2] == 0.0
        assert receiving["receiving_yds"][2] == 0.0

    def test_current_season_boxscore_is_read(self, tmp_path):
        player = _player([self._boxscore(CURRENT_SEASON, 3, {"53": 7.0, "42": 96.0})])
        exporter = _exporter(tmp_path, current_nfl_week=17)
        receiving = exporter._extract_receiving_stats(player)
        assert receiving["receptions"][2] == pytest.approx(7.0)
        assert receiving["receiving_yds"][2] == pytest.approx(96.0)

    def test_prior_season_entry_does_not_shadow_current_season(self, tmp_path):
        """Prior-season entry sorts first; the current-season value must win."""
        player = _player([
            self._boxscore(PRIOR_SEASON, 4, {"53": 11.0}),
            self._boxscore(CURRENT_SEASON, 4, {"53": 3.0}),
        ])
        exporter = _exporter(tmp_path, current_nfl_week=17)
        assert exporter._extract_receiving_stats(player)["receptions"][3] == pytest.approx(3.0)

    def test_order_independence(self, tmp_path):
        forward = _player([
            self._boxscore(PRIOR_SEASON, 4, {"53": 11.0}),
            self._boxscore(CURRENT_SEASON, 4, {"53": 3.0}),
        ])
        reverse = _player([
            self._boxscore(CURRENT_SEASON, 4, {"53": 3.0}),
            self._boxscore(PRIOR_SEASON, 4, {"53": 11.0}),
        ])
        exporter = _exporter(tmp_path, current_nfl_week=17)
        assert exporter._extract_receiving_stats(forward)["receptions"][3] == pytest.approx(3.0)
        assert exporter._extract_receiving_stats(reverse)["receptions"][3] == pytest.approx(3.0)

    def test_projection_entries_are_never_read_as_actuals(self, tmp_path):
        """statSourceId=1 carries current-season projections; not a box score."""
        entry = _stat(CURRENT_SEASON, 5, 1, 14.0)
        entry["stats"] = {"53": 6.0}
        player = _player([entry])
        exporter = _exporter(tmp_path, current_nfl_week=17)
        assert exporter._extract_receiving_stats(player)["receptions"][4] == 0.0

    def test_every_stat_family_is_scoped(self, tmp_path):
        """Passing, rushing, receiving, misc, kicking and defense share the path."""
        prior = self._boxscore(PRIOR_SEASON, 2, {
            "3": 310.0, "24": 88.0, "53": 7.0, "68": 1.0, "83": 3.0, "99": 4.0,
        })
        player = _player([prior])
        exporter = _exporter(tmp_path, current_nfl_week=17)
        assert exporter._extract_passing_stats(player)["pass_yds"][1] == 0.0
        assert exporter._extract_rushing_stats(player)["rush_yds"][1] == 0.0
        assert exporter._extract_receiving_stats(player)["receptions"][1] == 0.0
        assert exporter._extract_misc_stats(player)["fumbles"][1] == 0.0

    def test_combined_stat_is_scoped_too(self, tmp_path):
        """`_extract_combined_stat` (DST return yards) delegates to the same helper."""
        player = _player([self._boxscore(PRIOR_SEASON, 6, {"114": 40.0, "115": 25.0})])
        exporter = _exporter(tmp_path, current_nfl_week=17)
        assert exporter._extract_combined_stat(player.raw_stats, 6, ["114", "115"]) == 0.0

    def test_unknown_season_preserves_prior_behaviour(self, tmp_path):
        """historical_data_compiler passes no espn_settings; keep it unfiltered."""
        player = _player([self._boxscore(PRIOR_SEASON, 3, {"53": 7.0})])
        exporter = _exporter(tmp_path, season=None, current_nfl_week=17)
        assert exporter._extract_receiving_stats(player)["receptions"][2] == pytest.approx(7.0)

    def test_future_week_gate_still_applies(self, tmp_path):
        """A current-season week at or beyond current_nfl_week stays zero."""
        player = _player([self._boxscore(CURRENT_SEASON, 9, {"53": 7.0})])
        exporter = _exporter(tmp_path, current_nfl_week=9)
        assert exporter._extract_receiving_stats(player)["receptions"][8] == 0.0

    @pytest.mark.parametrize("bad", [None, "not-a-number", float("nan")])
    def test_malformed_value_does_not_raise(self, tmp_path, bad):
        player = _player([self._boxscore(CURRENT_SEASON, 3, {"53": bad})])
        exporter = _exporter(tmp_path, current_nfl_week=17)
        assert exporter._extract_receiving_stats(player)["receptions"][2] == 0.0

    def test_malformed_entry_does_not_hide_a_good_sibling(self, tmp_path):
        player = _player([
            self._boxscore(CURRENT_SEASON, 3, {"53": float("nan")}),
            self._boxscore(CURRENT_SEASON, 3, {"53": 5.0}),
        ])
        exporter = _exporter(tmp_path, current_nfl_week=17)
        assert exporter._extract_receiving_stats(player)["receptions"][2] == pytest.approx(5.0)

    def test_missing_stats_dict_is_skipped(self, tmp_path):
        """An appliedTotal-only entry carries no `stats` dict at all."""
        player = _player([
            _stat(CURRENT_SEASON, 3, 0, 12.0),
            self._boxscore(CURRENT_SEASON, 3, {"53": 5.0}),
        ])
        exporter = _exporter(tmp_path, current_nfl_week=17)
        assert exporter._extract_receiving_stats(player)["receptions"][2] == pytest.approx(5.0)
