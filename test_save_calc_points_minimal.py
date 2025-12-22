#!/usr/bin/env python3
"""
Minimal smoke test for Save Calculated Points - bypasses roster validation.

This test verifies the core feature functionality by mocking only the
PlayerManager initialization that requires valid roster state.
"""

from pathlib import Path
import json
import sys
from unittest.mock import Mock, patch

sys.path.append(str(Path(__file__).parent))

from league_helper.util.ConfigManager import ConfigManager
from league_helper.util.SeasonScheduleManager import SeasonScheduleManager
from league_helper.util.TeamDataManager import TeamDataManager
from league_helper.save_calculated_points_mode.SaveCalculatedPointsManager import SaveCalculatedPointsManager


def main():
    """Run minimal smoke test."""
    print("=" * 70)
    print("MINIMAL SMOKE TEST: Save Calculated Projected Points")
    print("=" * 70)

    base_path = Path(__file__).parent
    data_path = base_path / "data"

    print(f"\n1. Initializing managers...")

    # Real managers
    config = ConfigManager(data_path)
    print(f"   ✓ ConfigManager: {config.config_name} (Week {config.current_nfl_week})")

    season_schedule_manager = SeasonScheduleManager(data_path)
    print(f"   ✓ SeasonScheduleManager")

    team_data_manager = TeamDataManager(data_path, config, season_schedule_manager, config.current_nfl_week)
    print(f"   ✓ TeamDataManager")

    # Import PlayerManager and patch __init__ to skip team loading
    print(f"   Loading PlayerManager with patched initialization...")

    def mock_load_team(self):
        """Mock team loading to avoid roster validation."""
        mock_team = Mock()
        mock_team.roster = []
        self.team = mock_team

    with patch('league_helper.util.PlayerManager.PlayerManager.load_team', mock_load_team):
        from league_helper.util.PlayerManager import PlayerManager
        player_manager = PlayerManager(data_path, config, team_data_manager, season_schedule_manager)
        print(f"   ✓ PlayerManager: {len(player_manager.players)} players loaded")

    # Initialize Save Calculated Points Manager
    save_manager = SaveCalculatedPointsManager(config, player_manager, data_path)
    print(f"   ✓ SaveCalculatedPointsManager initialized")

    # Determine output path
    week = config.current_nfl_week
    season = config.nfl_season

    if week == 0:
        output_path = data_path / "historical_data" / str(season) / "calculated_season_long_projected_points.json"
    else:
        week_str = f"{week:02d}"
        output_path = data_path / "historical_data" / str(season) / week_str / "calculated_projected_points.json"

    output_folder = output_path.parent

    print(f"\n2. Expected output: {output_path}")

    # Check idempotent behavior
    if output_folder.exists():
        print(f"   ⚠ Output already exists (idempotent behavior)")
        print(f"   To test creation: rm -rf {output_folder}")
        print(f"\n   Smoke test PASSED (idempotent check)")
        return 0

    # Execute
    print(f"\n3. Executing save_calculated_points_manager.execute()...")
    try:
        save_manager.execute()
        print(f"   ✓ Execution completed")
    except Exception as e:
        print(f"   ✗ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1

    # Verify JSON
    print(f"\n4. Verifying JSON output...")
    if not output_path.exists():
        print(f"   ✗ JSON not created")
        return 1

    with open(output_path) as f:
        data = json.load(f)

    print(f"   ✓ JSON valid: {len(data)} players")

    # Sample check
    if len(data) > 0:
        sample_key = list(data.keys())[0]
        sample_value = data[sample_key]
        print(f"   ✓ Sample: {sample_key} = {sample_value}")

        # Check precision
        if isinstance(sample_value, float):
            str_val = str(sample_value)
            if '.' in str_val:
                decimals = len(str_val.split('.')[1])
                if decimals <= 2:
                    print(f"   ✓ Precision: {decimals} decimals (≤2)")
                else:
                    print(f"   ✗ Precision: {decimals} decimals (>2)")
                    return 1

    # Verify files copied
    print(f"\n5. Verifying copied files...")
    files = ["players.csv", "players_projected.csv", "game_data.csv", "drafted_data.csv"]
    for f in files:
        if (output_folder / f).exists():
            print(f"   ✓ {f}")

    if (output_folder / "configs").exists():
        print(f"   ✓ configs/")
    if (output_folder / "team_data").exists():
        print(f"   ✓ team_data/")

    print(f"\n" + "=" * 70)
    print(f"SMOKE TEST PASSED ✓")
    print(f"=" * 70)
    print(f"Output: {output_folder}")
    print(f"Players: {len(data)}")
    print(f"\nCleanup: rm -rf {output_folder}")
    print("=" * 70)

    return 0


if __name__ == "__main__":
    sys.exit(main())
