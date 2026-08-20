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
            position_key = filename.removesuffix(".json")
            (week_dir / filename).write_text(json.dumps({position_key: players}))

    def test_run_win_rate_simulation_e2e(self, tmp_path):
        data_folder = tmp_path / "sim_data"
        draft_dir = data_folder / "draft_order_possibilities"
        draft_dir.mkdir(parents=True)

        real_strategy = Path("simulation/sim_data/draft_order_possibilities/1_zero_rb.json")
        assert real_strategy.exists(), f"Real strategy file missing: {real_strategy}"
        (draft_dir / "1_zero_rb.json").write_text(real_strategy.read_text())

        week_counts = {"QB": 50, "RB": 50, "WR": 50, "TE": 50, "K": 20, "DST": 20}

        # T73/R12: the full week_01..week_18 tree. Weeks 1-17 are simulated and week_18
        # supplies week 17's actuals, so SimDataLoader._validate_season_data now refuses a
        # 17-folder season outright (season_count == 0 -> the sweep reports 0.0). Every week
        # folder carries identical actual_points, so T73/R12 itself left the pin below
        # unchanged (it was 8/17 then; T79 later moved it to 10/17 — see that comment).
        for week_num in range(1, 19):
            week_dir = data_folder / "2024" / "weeks" / f"week_{week_num:02d}"
            self._write_week(week_dir, week_counts)

        fixture_config = "tests/fixtures/win_rate_e2e/configs/league_config.json"
        argv = [
            sys.executable,
            "run_win_rate_simulation.py",
            "--sims", "1",
            "--strategy", "1_zero_rb.json",
            "--data", str(data_folder),
            "--config", fixture_config,
            "--seed", "42",
            "--log-level", "WARNING",
        ]

        # D4.3/du6 item 4: guard the isolation itself. The fixture tree is a byte-identical
        # snapshot of data/configs/ TODAY, so dropping the --config entry below would leave
        # this test green while silently restoring the live-config coupling D4.3 exists to
        # cut — the regression would only surface once the live store drifts, which is
        # exactly the moment the pin below is hardest to trust. This reads the argv list, not
        # source text, so it fails on precisely that deletion.
        assert "--config" in argv, "the --config redirect was removed from the e2e argv"
        assert argv[argv.index("--config") + 1] == fixture_config
        assert Path(fixture_config).is_file(), f"fixture config missing: {fixture_config}"

        result = subprocess.run(
            argv,
            capture_output=True,
            text=True,
            cwd=str(Path(__file__).parent.parent.parent),
            timeout=120,
        )

        assert result.returncode == 0, f"Non-zero exit code: {result.stderr}"

        meta_data_path = data_folder / "win_rate_meta_data.json"
        assert meta_data_path.exists(), "win_rate_meta_data.json was not created"

        meta_data = json.loads(meta_data_path.read_text())
        assert "1_zero_rb.json" in meta_data["strategies"]

        entry = meta_data["strategies"]["1_zero_rb.json"]
        assert 0.0 <= entry["best_win_rate"] <= 1.0
        # Deterministic with --seed 42 on this identical-week fixture: best_win_rate == 10/17.
        # The value is pinned, not ranged: the original *unseeded* 0.30..0.85 range was flaky
        # (natural unseeded draws span ~0.29..0.77 and dip below 0.30), so a low draw failed the
        # build. Seeding plus an exact pin removed that flakiness and must keep doing so — widen
        # this back to a range and the flakiness returns.
        # The pin was 8/17 through T42, which was behavior-neutral on this fixture. T79 is NOT:
        # it makes draft rounds that name RB/WR natively award their PRIMARY/SECONDARY bonus
        # (previously silently 0), and the real 1_zero_rb.json strategy this fixture loads names
        # RB/WR natively — so opponent drafting, and hence the simulated win rate, changed BY
        # DESIGN. 10/17 was the post-T79 deterministic value at --seed 42 (observed identical on
        # three consecutive runs, 2026-07-28). Re-pin, never re-range, if a future change moves
        # it again. (T79; see the story's simulation_impact.md for the measured strategy deltas.)
        # D4.2 moved it again, also BY DESIGN — it flipped ADP_SCORING.THRESHOLDS.DIRECTION
        # INCREASING -> DECREASING, making the ADP ladder five-tier, which re-ordered drafting on
        # this fixture and so moved the win rate. At that point this test still redirected only
        # --data, so the run read the LIVE data/configs/league_config.json through
        # DraftStrategyOrchestrator/CombinationEvaluator's default config_path: it was an INDIRECT
        # live-config consumer, and every config change reached it.
        #
        # D4.3 CUT that coupling. The run now passes --config at the committed, frozen fixture tree
        # tests/fixtures/win_rate_e2e/configs/ (provenance and closed consumer set: that tree's
        # README.md), so only a deliberate edit to THAT tree can move this number again.
        #
        # The pin below was RE-MEASURED against the fixture — it is not carried over from D4.2.
        # Population: this test's own 18-week synthetic tree scored against
        # tests/fixtures/win_rate_e2e/configs/ as the ConfigManager root. Convention: one pass,
        # --sims 1, --seed 42, one season, so best_win_rate = wins / (17 weeks x 1 sim x 1 season).
        # D4.2's 10/17-vs-8/17 arms were measured over a DIFFERENT population (the live
        # data/configs/ tree as the config root), so they are evidence that DIRECTION moves this
        # number, NOT this fixture's expected values.
        # Why the re-measurement nonetheless landed on exactly D4.2's 8/17: the fixture tree was
        # snapshotted BYTE-IDENTICAL from data/configs/ at pin time (see that tree's README.md
        # §Provenance), so the two populations had different ROOTS but identical CONTENT. The
        # coincidence is a consequence of the snapshot, not evidence the value was carried over —
        # and the two will diverge the moment the live store moves, which is the point of D4.3.
        # Re-pin, never re-range, if a future change moves it again.
        #
        # 2026-08-19 moved it again, BY DESIGN and via exactly the D4.3 channel above: raising the
        # ADP_SCORING_WEIGHT sweep floor to 4.00 put this tree's own 2.12 anchor out of bounds
        # (generate_candidate_values rejects an anchor outside [min, max]), so the fixture's ADP
        # weight was edited 2.12 -> 7.0. That is a deliberate edit to the frozen tree, which
        # re-ordered drafting and moved the rate 8/17 -> 7/17. Re-pinned, not re-ranged.
        assert abs(entry["best_win_rate"] - 7 / 17) < 1e-9
        assert "total_wins" in entry
        assert "total_games" in entry
        assert entry["total_games"] >= entry["total_wins"]
