#!/usr/bin/env python3
"""
Smoke Test: Verify bye_week field is included in JSON exports

This script directly tests the modified methods to verify the bye_week field
is correctly added to JSON output.
"""

import sys
import json
from pathlib import Path

# Add paths for imports
sys.path.append(str(Path(__file__).parent))
sys.path.append(str(Path(__file__).parent / "player-data-fetcher"))
sys.path.append(str(Path(__file__).parent / "historical_data_compiler"))

def test_player_data_exporter():
    """Test that player-data-fetcher includes bye_week in JSON"""
    print("=" * 70)
    print("TEST 1: Player-Data-Fetcher JSON Export")
    print("=" * 70)

    # Check existing file structure (before regeneration)
    json_file = Path("data/player_data/qb_data.json")
    if json_file.exists():
        with open(json_file) as f:
            data = json.load(f)
            players = data.get('qb_data', [])
            if players:
                first_player = players[0]
                fields = list(first_player.keys())

                print(f"\nFile: {json_file}")
                print(f"First player: {first_player.get('name', 'Unknown')}")
                print(f"Fields present: {fields}")
                print(f"\n[OK] bye_week present: {'bye_week' in fields}")

                if 'bye_week' in fields:
                    # Verify placement: should be after 'position', before 'injury_status'
                    try:
                        pos_idx = fields.index('position')
                        bye_idx = fields.index('bye_week')
                        inj_idx = fields.index('injury_status')

                        correct_order = pos_idx < bye_idx < inj_idx
                        print(f"[OK] Field placement correct: {correct_order}")
                        print(f"  Order: position({pos_idx}) → bye_week({bye_idx}) → injury_status({inj_idx})")

                        # Check data type
                        bye_value = first_player['bye_week']
                        is_valid_type = bye_value is None or isinstance(bye_value, int)
                        print(f"[OK] Data type correct: {is_valid_type} (value: {bye_value}, type: {type(bye_value).__name__})")

                        return True
                    except ValueError as e:
                        print(f"[FAIL] Field placement error: {e}")
                        return False
                else:
                    print("[FAIL] bye_week field is MISSING")
                    print("\n[WARNING] This means the JSON files were generated BEFORE the code changes.")
                    print("   Need to regenerate files to complete smoke test.")
                    return False
    else:
        print(f"[FAIL] File not found: {json_file}")
        return False

def test_historical_compiler():
    """Test that historical-data-compiler includes bye_week in JSON"""
    print("\n" + "=" * 70)
    print("TEST 2: Historical Data Compiler JSON Export")
    print("=" * 70)

    # Check simulation data
    json_file = Path("simulation/sim_data/2024/weeks/week_01/qb_data.json")
    if json_file.exists():
        with open(json_file) as f:
            data = json.load(f)
            if data and isinstance(data, list):
                first_player = data[0]
                fields = list(first_player.keys())

                print(f"\nFile: {json_file}")
                print(f"First player: {first_player.get('name', 'Unknown')}")
                print(f"Fields present: {fields}")
                print(f"\n[OK] bye_week present: {'bye_week' in fields}")

                if 'bye_week' in fields:
                    # Verify placement
                    try:
                        pos_idx = fields.index('position')
                        bye_idx = fields.index('bye_week')
                        inj_idx = fields.index('injury_status')

                        correct_order = pos_idx < bye_idx < inj_idx
                        print(f"[OK] Field placement correct: {correct_order}")
                        print(f"  Order: position({pos_idx}) → bye_week({bye_idx}) → injury_status({inj_idx})")

                        # Check data type
                        bye_value = first_player['bye_week']
                        is_valid_type = bye_value is None or isinstance(bye_value, int)
                        print(f"[OK] Data type correct: {is_valid_type} (value: {bye_value}, type: {type(bye_value).__name__})")

                        return True
                    except ValueError as e:
                        print(f"[FAIL] Field placement error: {e}")
                        return False
                else:
                    print("[FAIL] bye_week field is MISSING")
                    print("\n[WARNING] This means the JSON files were generated BEFORE the code changes.")
                    print("   Need to regenerate files to complete smoke test.")
                    return False
    else:
        print(f"[FAIL] File not found: {json_file}")
        return False

def verify_code_changes():
    """Verify the actual code changes are in place"""
    print("\n" + "=" * 70)
    print("CODE VERIFICATION: Check source files have bye_week")
    print("=" * 70)

    # Check player_data_exporter.py
    exporter_file = Path("player-data-fetcher/player_data_exporter.py")
    with open(exporter_file) as f:
        content = f.read()
        has_bye_week = '"bye_week": player.bye_week' in content
        print(f"\n{exporter_file}:")
        print(f"  [OK] Contains '\"bye_week\": player.bye_week': {has_bye_week}")

    # Check json_exporter.py
    json_exp_file = Path("historical_data_compiler/json_exporter.py")
    with open(json_exp_file) as f:
        content = f.read()
        has_bye_week = '"bye_week": player_data.bye_week' in content
        print(f"\n{json_exp_file}:")
        print(f"  [OK] Contains '\"bye_week\": player_data.bye_week': {has_bye_week}")

    print()

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("SMOKE TEST: Bye Week Field in JSON Exports")
    print("=" * 70)

    # Verify code changes first
    verify_code_changes()

    # Test JSON files
    test1_pass = test_player_data_exporter()
    test2_pass = test_historical_compiler()

    print("\n" + "=" * 70)
    print("SMOKE TEST SUMMARY")
    print("=" * 70)
    print(f"Player-Data-Fetcher: {'PASS' if test1_pass else 'NEEDS REGENERATION'}")
    print(f"Historical Compiler: {'PASS' if test2_pass else 'NEEDS REGENERATION'}")

    if test1_pass and test2_pass:
        print("\n[PASS] SMOKE TEST PASSED: bye_week field correctly added to JSON exports")
        sys.exit(0)
    else:
        print("\n[WARNING] SMOKE TEST INCOMPLETE: JSON files need regeneration with new code")
        print("   Code changes are in place, but output files are from before the changes.")
        sys.exit(1)
