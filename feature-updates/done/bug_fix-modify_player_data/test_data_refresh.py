#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to verify if data refresh bug exists after Feature 01 completion.

Tests:
1. Modify a player (mark as drafted)
2. Check if subsequent queries see the updated value (same session)
3. Simulate reload and verify changes persist

If bug exists: Feature 02 needed
If no bug: Feature 02 can be skipped
"""

import sys
import os
from pathlib import Path

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Add project root and league_helper directories to path (same as tests/conftest.py)
project_root = Path(__file__).parent.parent.parent
league_helper_dir = project_root / "league_helper"

sys.path.insert(0, str(project_root))
sys.path.insert(0, str(league_helper_dir / "util"))
sys.path.insert(0, str(league_helper_dir))

from util.PlayerManager import PlayerManager
from util.ConfigManager import ConfigManager
from util.TeamDataManager import TeamDataManager
from util.SeasonScheduleManager import SeasonScheduleManager


def main():
    """Run data refresh test."""

    print("=" * 80)
    print("DATA REFRESH BUG TEST")
    print("=" * 80)
    print()

    data_folder = project_root / "data"

    # PART 1: Initial load
    print("[Part 1] Loading player data...")
    config = ConfigManager(data_folder)
    team_data = TeamDataManager(data_folder, config)
    schedule = SeasonScheduleManager(data_folder)
    player_manager = PlayerManager(data_folder, config, team_data, schedule)

    total_players = len(player_manager.players)
    print(f"✅ Loaded {total_players} players")
    print()

    # PART 2: Find a test player (first undrafted QB)
    print("[Part 2] Finding test player...")
    test_player = None
    for player in player_manager.players:
        if player.position == "QB" and player.drafted_by == "":
            test_player = player
            break

    if not test_player:
        print("⚠️  All QBs are drafted, using first QB regardless")
        test_player = next((p for p in player_manager.players if p.position == "QB"), None)

    if not test_player:
        print("❌ No QB players found")
        return False

    print(f"✅ Test player: {test_player.name} (ID: {test_player.id})")
    print(f"   Current drafted_by: '{test_player.drafted_by}'")
    print(f"   Current locked: {test_player.locked}")
    original_drafted_by = test_player.drafted_by
    original_locked = test_player.locked
    print()

    # PART 3: Modify the player (simulate user action)
    print("[Part 3] Modifying player (mark as drafted)...")
    test_team = "DATA_REFRESH_TEST_TEAM"
    test_player.drafted_by = test_team
    test_player.locked = True
    print(f"✅ Modified in-memory object:")
    print(f"   drafted_by: '{original_drafted_by}' → '{test_player.drafted_by}'")
    print(f"   locked: {original_locked} → {test_player.locked}")
    print()

    # PART 4: Persist to JSON (simulate update_players_file call)
    print("[Part 4] Persisting to JSON files...")
    result = player_manager.update_players_file()
    print(f"✅ {result}")
    print()

    # PART 5: Query the same player WITHIN same session (no reload)
    print("[Part 5] Testing in-session data visibility...")
    print("   Searching for player in players list...")

    found_player = None
    for player in player_manager.players:
        if player.id == test_player.id:
            found_player = player
            break

    if not found_player:
        print("❌ FAIL: Player not found in players list!")
        return False

    # Check if it's the SAME object (same memory reference)
    if found_player is test_player:
        print("✅ Same object reference (expected - direct modification)")
    else:
        print("⚠️  Different object (unexpected)")

    # Verify values match what we set
    if found_player.drafted_by == test_team and found_player.locked:
        print(f"✅ In-session query sees updated values:")
        print(f"   drafted_by: '{found_player.drafted_by}' (correct)")
        print(f"   locked: {found_player.locked} (correct)")
        print("   ✅ NO BUG: In-session queries work correctly")
    else:
        print(f"❌ BUG FOUND: In-session query does NOT see updates!")
        print(f"   Expected drafted_by: '{test_team}'")
        print(f"   Actual drafted_by: '{found_player.drafted_by}'")
        print(f"   Expected locked: True")
        print(f"   Actual locked: {found_player.locked}")
        return False
    print()

    # PART 6: Simulate app restart (reload_player_data)
    print("[Part 6] Testing persistence across reload...")
    print("   Simulating reload_player_data() call...")

    # This is what LeagueHelperManager does before displaying menu
    player_manager.reload_player_data()

    print(f"✅ reload_player_data() completed")
    print(f"   Total players after reload: {len(player_manager.players)}")
    print()

    # PART 7: Query the player AFTER reload
    print("[Part 7] Verifying data after reload...")

    reloaded_player = None
    for player in player_manager.players:
        if player.id == test_player.id:
            reloaded_player = player
            break

    if not reloaded_player:
        print("❌ FAIL: Player not found after reload!")
        return False

    # Check if it's a DIFFERENT object (reload creates new objects)
    if reloaded_player is test_player:
        print("⚠️  Same object reference (reload didn't create new objects?)")
    else:
        print("✅ Different object (reload created new instances)")

    # Verify values persisted from JSON
    if reloaded_player.drafted_by == test_team and reloaded_player.locked:
        print(f"✅ Data persisted correctly after reload:")
        print(f"   drafted_by: '{reloaded_player.drafted_by}' (correct)")
        print(f"   locked: {reloaded_player.locked} (correct)")
        print("   ✅ NO BUG: Reload works correctly")
    else:
        print(f"❌ BUG FOUND: Data did NOT persist after reload!")
        print(f"   Expected drafted_by: '{test_team}'")
        print(f"   Actual drafted_by: '{reloaded_player.drafted_by}'")
        print(f"   Expected locked: True")
        print(f"   Actual locked: {reloaded_player.locked}'")
        return False
    print()

    # PART 8: Cleanup - restore original state
    print("[Part 8] Cleanup - Restoring original state...")
    reloaded_player.drafted_by = original_drafted_by
    reloaded_player.locked = original_locked
    player_manager.update_players_file()
    print(f"✅ Restored to original state")
    print(f"   drafted_by: '{original_drafted_by}'")
    print(f"   locked: {original_locked}")
    print()

    # FINAL RESULT
    print("=" * 80)
    print("TEST RESULT: ✅ NO DATA REFRESH BUG DETECTED")
    print("=" * 80)
    print()
    print("Summary:")
    print("  ✅ In-session queries see updated values immediately")
    print("  ✅ reload_player_data() correctly reloads from JSON")
    print("  ✅ Changes persist across reload")
    print("  ✅ Feature 01 (File Persistence) fixes the issue completely")
    print()
    print("Recommendation: Feature 02 NOT NEEDED - skip to Stage 6 (Epic QC)")
    print()

    return True


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ TEST FAILED WITH EXCEPTION: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
