"""The draft must score on PRE-SEASON ratings, never full-season hindsight.

json_exporter._calculate_player_ratings ranks players on cumulative ACTUAL points
through week N-1, so the week_18 construction snapshot carries a ranking spanning
the entire season. set_player_data refreshes only projected_points/actual_points,
so that value would stay frozen on every FantasyPlayer and the draft scorer reads
it. Measured before the fix: week_18 rating vs season production ranked within
position scored Spearman 0.92-0.95, against 0.69-0.75 for the honest week_01 value.
"""

import json
from pathlib import Path
from unittest.mock import patch

import pytest

from simulation.win_rate.SimulatedLeague import SimulatedLeague


CONFIG = {"config_name": "test", "description": "test", "parameters": {}}
POSITION_FILES = ["qb_data.json", "rb_data.json", "wr_data.json",
                  "te_data.json", "k_data.json", "dst_data.json"]


def _write_week(folder: Path, ratings: dict):
    """Write a 6-file week folder where every player carries `ratings[id]`."""
    folder.mkdir(parents=True, exist_ok=True)
    for name in POSITION_FILES:
        stem = name[:-5]
        folder / name
        records = [
            {
                "id": pid,
                "name": f"Player {pid}",
                "team": "SEA",
                "position": stem.split("_")[0].upper(),
                "bye_week": 5,
                "injury_status": "ACTIVE",
                "drafted_by": "",
                "locked": False,
                "average_draft_position": 10.0,
                "player_rating": rating,
                "projected_points": [1.0] * 17,
                "actual_points": [1.0] * 17,
            }
            for pid, rating in ratings.items()
        ]
        (folder / name).write_text(json.dumps({stem: records}, indent=2))


@pytest.fixture
def season(tmp_path):
    """A season whose week_01 and week_18 ratings are deliberately inverted."""
    root = tmp_path / "2099"
    weeks = root / "weeks"
    draft_time = {"1": 99.0, "2": 10.0, "3": 50.0}
    hindsight = {"1": 3.0, "2": 95.0, "3": 50.0}
    for w in range(1, 19):
        _write_week(weeks / f"week_{w:02d}", hindsight)
    _write_week(weeks / "week_01", draft_time)
    (root / "season_schedule.csv").write_text("week,team,opponent\n")
    return root, draft_time, hindsight


def _shared(season_root):
    with patch.object(SimulatedLeague, "_initialize_teams"), \
         patch.object(SimulatedLeague, "_generate_schedule"):
        league = SimulatedLeague(CONFIG, season_root)
    return league, league._create_shared_data_dir("probe", season_root / "weeks" / "week_18")


def _ratings(player_data_dir: Path):
    out = {}
    for f in sorted(player_data_dir.glob("*_data.json")):
        data = json.loads(f.read_text())
        for rec in data[next(iter(data))]:
            out[rec["id"]] = rec["player_rating"]
    return out


class TestDraftTimeRatingSubstitution:
    def test_shared_snapshot_carries_week_one_ratings(self, season):
        root, draft_time, hindsight = season
        _, shared = _shared(root)
        assert _ratings(shared / "player_data") == draft_time

    def test_hindsight_ratings_do_not_survive(self, season):
        """The specific failure: a player who busted must NOT be marked down."""
        root, draft_time, hindsight = season
        _, shared = _shared(root)
        got = _ratings(shared / "player_data")
        assert got["1"] == pytest.approx(99.0), "busted player still carries its week-18 markdown"
        assert got["1"] != pytest.approx(hindsight["1"])
        assert got["2"] == pytest.approx(10.0), "breakout player still carries its week-18 markup"
        assert got["2"] != pytest.approx(hindsight["2"])

    def test_a_rating_equal_in_both_snapshots_is_unchanged(self, season):
        root, draft_time, _ = season
        _, shared = _shared(root)
        assert _ratings(shared / "player_data")["3"] == pytest.approx(draft_time["3"])

    def test_every_other_field_still_comes_from_the_construction_snapshot(self, season):
        """Only player_rating is substituted; week_18 remains the source for the rest."""
        root, _, _ = season
        _, shared = _shared(root)
        data = json.loads((shared / "player_data" / "qb_data.json").read_text())
        rec = data["qb_data"][0]
        assert rec["actual_points"] == [1.0] * 17
        assert rec["average_draft_position"] == 10.0
        assert rec["bye_week"] == 5


class TestMissingWeekOneFailsLoudly:
    def test_absent_week_01_raises_rather_than_falling_back(self, season):
        """A silent fallback would reinstate the lookahead this guard removes."""
        root, _, _ = season
        import shutil
        shutil.rmtree(root / "weeks" / "week_01")
        with patch.object(SimulatedLeague, "_initialize_teams"), \
             patch.object(SimulatedLeague, "_generate_schedule"):
            league = SimulatedLeague(CONFIG, root)
        with pytest.raises(FileNotFoundError, match="week_01"):
            league._create_shared_data_dir("probe", root / "weeks" / "week_18")
