#!/usr/bin/env python3
"""
E2E Smoke Test for Feature 01: File Persistence Issues

Tests the complete workflow:
1. Mark a player as drafted
2. Verify JSON file updated with correct drafted_by value
3. Verify NO .bak files created
4. Verify data persists across restarts

This test uses REAL data (not test fixtures) as required by smoke testing guide.
"""

import sys
import json
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from league_helper.util.PlayerManager import PlayerManager
from league_helper.util.ConfigManager import ConfigManager
from league_helper.util.TeamDataManager import TeamDataManager
from league_helper.util.SeasonScheduleManager import SeasonScheduleManager


def main():
    """Run E2E smoke test."""

    print("=" * 80)
    print("FEATURE 01: File Persistence E2E Smoke Test")
    print("=" * 80)
    print()

    data_folder = project_root / "data"

    # STEP 1: Create PlayerManager instance
    print("[Step 1] Creating PlayerManager instance...")
    config_manager = ConfigManager(data_folder)
    team_data_manager = TeamDataManager(data_folder)
    schedule_manager = SeasonScheduleManager(data_folder)
    player_manager = PlayerManager(data_folder, config_manager, team_data_manager, schedule_manager)
    print("✅ PlayerManager created successfully")
    print(f"   Loaded {len(player_manager.all_players)} total players")
    print()

    # STEP 2: Select a test player (first QB)
    print("[Step 2] Selecting test player...")
    qb_players = player_manager.players_by_position.get('QB', [])
    if not qb_players:
        print("❌ FAIL: No QB players found")
        return False

    test_player = qb_players[0]
    original_drafted_by = test_player.drafted_by
    print(f"✅ Selected player: {test_player.name} ({test_player.position}, {test_player.team})")
    print(f"   Current drafted_by: '{original_drafted_by}'")
    print(f"   Player ID: {test_player.id}")
    print()

    # STEP 3: Modify player (mark as drafted)
    print("[Step 3] Marking player as drafted...")
    test_owner = "SMOKE_TEST_OWNER"
    test_player.drafted_by = test_owner
    print(f"✅ Set drafted_by to: '{test_owner}'")
    print()

    # STEP 4: Call update_players_file() to persist changes
    print("[Step 4] Persisting changes to JSON files...")
    player_manager.update_players_file()
    print("✅ update_players_file() completed")
    print()

    # STEP 5: Verify NO .bak files created
    print("[Step 5] Verifying NO .bak files created...")
    player_data_folder = data_folder / "player_data"
    bak_files = list(player_data_folder.glob("*.bak"))

    if bak_files:
        print(f"❌ FAIL: Found {len(bak_files)} .bak files:")
        for bak_file in bak_files:
            print(f"   - {bak_file.name}")
        return False

    print("✅ No .bak files found (PRIMARY BUG FIX VERIFIED)")
    print()

    # STEP 6: Verify JSON file contains correct drafted_by value
    print("[Step 6] Verifying JSON file contains correct DATA VALUES...")
    json_file = player_data_folder / f"{test_player.position.lower()}_data.json"

    if not json_file.exists():
        print(f"❌ FAIL: JSON file not found: {json_file}")
        return False

    with open(json_file, 'r') as f:
        json_data = json.load(f)

    # Find our player in the JSON data
    position_key = f"{test_player.position.upper()}s"
    players_array = json_data.get(position_key, [])

    player_found = False
    player_data = None

    for player_dict in players_array:
        # Convert ID to int for comparison (JSON stores as string)
        player_id = int(player_dict.get('id')) if isinstance(player_dict.get('id'), str) else player_dict.get('id')
        if player_id == test_player.id:
            player_found = True
            player_data = player_dict
            break

    if not player_found:
        print(f"❌ FAIL: Player ID {test_player.id} not found in JSON file")
        return False

    actual_drafted_by = player_data.get('drafted_by', '')

    if actual_drafted_by != test_owner:
        print(f"❌ FAIL: JSON drafted_by value incorrect")
        print(f"   Expected: '{test_owner}'")
        print(f"   Actual: '{actual_drafted_by}'")
        return False

    print(f"✅ JSON file contains correct drafted_by value: '{actual_drafted_by}'")
    print(f"   File: {json_file.name}")
    print(f"   Player ID: {test_player.id}")
    print()

    # STEP 7: Verify data persists across restarts (simulate restart)
    print("[Step 7] Verifying data persists across restarts...")

    # Delete current instance (simulate app shutdown)
    del player_manager
    del config_manager
    del team_data_manager
    del schedule_manager

    # Create new instance (simulate app restart)
    config_manager_2 = ConfigManager(data_folder)
    team_data_manager_2 = TeamDataManager(data_folder)
    schedule_manager_2 = SeasonScheduleManager(data_folder)
    player_manager_2 = PlayerManager(data_folder, config_manager_2, team_data_manager_2, schedule_manager_2)

    # Find the same player in the reloaded data
    reloaded_player = None
    for player in player_manager_2.all_players:
        if player.id == test_player.id:
            reloaded_player = player
            break

    if not reloaded_player:
        print(f"❌ FAIL: Player ID {test_player.id} not found after reload")
        return False

    if reloaded_player.drafted_by != test_owner:
        print(f"❌ FAIL: Data did not persist across restart")
        print(f"   Expected: '{test_owner}'")
        print(f"   Actual: '{reloaded_player.drafted_by}'")
        return False

    print(f"✅ Data persisted across restart")
    print(f"   Reloaded player: {reloaded_player.name}")
    print(f"   drafted_by value: '{reloaded_player.drafted_by}'")
    print()

    # STEP 8: Cleanup - Restore original state
    print("[Step 8] Cleanup - Restoring original state...")
    reloaded_player.drafted_by = original_drafted_by
    player_manager_2.update_players_file()
    print(f"✅ Restored drafted_by to original value: '{original_drafted_by}'")
    print()

    # Final verification
    print("=" * 80)
    print("SMOKE TEST RESULT: ✅ ALL CHECKS PASSED")
    print("=" * 80)
    print()
    print("Summary:")
    print("  ✅ Part 1: Import Test - PlayerManager imports successfully")
    print("  ✅ Part 2: Entry Point Test - Script starts correctly")
    print("  ✅ Part 3: E2E Execution Test - Feature works end-to-end")
    print()
    print("Verified:")
    print("  ✅ NO .bak files created (PRIMARY BUG FIX)")
    print("  ✅ JSON file updated with correct drafted_by value (DATA VALUES verified)")
    print("  ✅ Changes persist immediately")
    print("  ✅ Changes persist across app restarts")
    print()

    return True


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ SMOKE TEST FAILED WITH EXCEPTION: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
