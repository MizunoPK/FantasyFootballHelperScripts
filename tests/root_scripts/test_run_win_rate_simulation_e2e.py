import json
import sys
from pathlib import Path
import subprocess


class TestWinRateSimulationE2E:
    """E2E test for run_win_rate_simulation.py CLI using mock sim data."""

    def _make_players(
        self, position: str, count: int, id_offset: int,
        base_score: float, adp_start: float, adp_step: float
    ) -> list:
        players = []
        for i in range(count):
            proj_multiplier = max(0.3, 1.0 - (i / count) * 0.8)
            proj_score = round(base_score * proj_multiplier, 1)
            adp = round(adp_start + i * adp_step, 1)
            player_id = id_offset + i
            actual = []
            for week_idx in range(17):
                period = (player_id + week_idx) % 3
                multiplier = [0.0, 1.0, 2.0][period]
                actual.append(round(base_score * multiplier, 1))
            players.append({
                "id": player_id,
                "name": f"{position} Player {i}",
                "position": position,
                "team": "KC",
                "drafted_by": "",
                "locked": False,
                "projected_points": [proj_score] * 17,
                "actual_points": actual,
                "average_draft_position": adp,
                "player_rating": 5.0,
                "bye_week": 7,
                "injury_status": "ACTIVE",
            })
        return players

    def _write_week(self, week_dir: Path, position_counts: dict) -> None:
        week_dir.mkdir(parents=True, exist_ok=True)
        pos_config = {
            "QB":  ("qb_data.json",  0,    12.0, 1.0, 0.5),
            "RB":  ("rb_data.json",  1000, 12.0, 1.1, 0.5),
            "WR":  ("wr_data.json",  2000, 12.0, 1.2, 0.5),
            "TE":  ("te_data.json",  3000, 12.0, 1.3, 0.5),
            "K":   ("k_data.json",   4000,  6.0, 50.0, 3.0),
            "DST": ("dst_data.json", 5000,  6.0, 51.0, 2.5),
        }
        for pos, (filename, id_offset, base_score, adp_start, adp_step) in pos_config.items():
            count = position_counts.get(pos, 1)
            players = self._make_players(pos, count, id_offset, base_score, adp_start, adp_step)
            (week_dir / filename).write_text(json.dumps(players))

    def test_run_win_rate_simulation_e2e(self, tmp_path):
        data_folder = tmp_path / "sim_data"
        draft_dir = data_folder / "draft_order_possibilities"
        draft_dir.mkdir(parents=True)

        real_strategy = Path("simulation/sim_data/draft_order_possibilities/1_zero_rb.json")
        (draft_dir / "1_zero_rb.json").write_text(real_strategy.read_text())

        week_counts = {"QB": 50, "RB": 50, "WR": 50, "TE": 50, "K": 20, "DST": 20}

        for week_num in range(1, 18):
            week_dir = data_folder / "2024" / "weeks" / f"week_{week_num:02d}"
            self._write_week(week_dir, week_counts)

        result = subprocess.run(
            [
                sys.executable,
                "run_win_rate_simulation.py",
                "--sims", "1",
                "--strategy", "1_zero_rb.json",
                "--data", str(data_folder),
                "--log-level", "WARNING",
            ],
            capture_output=True,
            text=True,
            cwd=str(Path(__file__).parent.parent.parent),
        )

        assert result.returncode == 0, f"Non-zero exit code: {result.stderr}"

        meta_data_path = data_folder / "win_rate_meta_data.json"
        assert meta_data_path.exists(), "win_rate_meta_data.json was not created"

        meta_data = json.loads(meta_data_path.read_text())
        assert "1_zero_rb.json" in meta_data["strategies"]

        entry = meta_data["strategies"]["1_zero_rb.json"]
        assert 0.30 <= entry["best_win_rate"] <= 0.85
        assert "total_wins" in entry
        assert "total_games" in entry
        assert entry["total_games"] >= entry["total_wins"]
