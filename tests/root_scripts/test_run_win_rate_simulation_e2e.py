import json
import sys
from pathlib import Path
import subprocess


class TestWinRateSimulationE2E:
    """E2E test for run_win_rate_simulation.py CLI using mock sim data."""

    def _make_players(self, position: str, count: int, base_score: float = 12.0) -> list:
        players = []
        for i in range(count):
            score_multiplier = max(0.3, 1.0 - (i / count) * 0.8)
            score = round(base_score * score_multiplier, 1)
            players.append({
                "id": i,
                "name": f"{position} Player {i}",
                "position": position,
                "team": "KC",
                "drafted_by": "",
                "locked": False,
                "projected_points": [score] * 17,
                "actual_points": [score] * 17,
            })
        return players

    def _write_week(self, week_dir: Path, position_counts: dict) -> None:
        week_dir.mkdir(parents=True, exist_ok=True)
        pos_to_file = {
            "QB": "qb_data.json",
            "RB": "rb_data.json",
            "WR": "wr_data.json",
            "TE": "te_data.json",
            "K": "k_data.json",
            "DST": "dst_data.json",
        }
        for pos, filename in pos_to_file.items():
            count = position_counts.get(pos, 1)
            base_score = 2.0 if pos == "RB" else 12.0
            players = self._make_players(pos, count, base_score)
            (week_dir / filename).write_text(json.dumps(players))

    def test_run_win_rate_simulation_e2e(self, tmp_path):
        data_folder = tmp_path / "sim_data"
        draft_dir = data_folder / "draft_order_possibilities"
        draft_dir.mkdir(parents=True)

        real_strategy = Path("simulation/sim_data/draft_order_possibilities/1_zero_rb.json")
        (draft_dir / "1_zero_rb.json").write_text(real_strategy.read_text())

        week_01_counts = {"QB": 25, "RB": 50, "WR": 50, "TE": 25, "K": 10, "DST": 10}
        minimal_counts = {"QB": 1, "RB": 1, "WR": 1, "TE": 1, "K": 1, "DST": 1}

        week_01_dir = data_folder / "2024" / "weeks" / "week_01"
        self._write_week(week_01_dir, week_01_counts)

        for week_num in range(2, 18):
            week_dir = data_folder / "2024" / "weeks" / f"week_{week_num:02d}"
            self._write_week(week_dir, minimal_counts)

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
        assert 0.0 <= entry["best_win_rate"] <= 1.0
        assert "total_wins" in entry
        assert "total_games" in entry
        assert entry["total_games"] >= entry["total_wins"]
