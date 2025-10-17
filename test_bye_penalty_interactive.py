#!/usr/bin/env python3
"""
Interactive Bye Penalty Testing

Tests the bye week penalty system including both:
1. BASE_BYE_PENALTY (applied per same-position bye week overlap)
2. DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY (applied per different-position overlap)

Requirements from updates/done/different_player_bye_penalty.txt:
- BASE_BYE_PENALTY applies based on same-position bye week overlaps
- DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY applies based on different-position overlaps
- Both penalties should affect player scoring calculations
- Config changes should modify scoring results appropriately
"""

from pathlib import Path
from league_helper.util.ConfigManager import ConfigManager
from league_helper.util.PlayerManager import PlayerManager
from league_helper.util.TeamDataManager import TeamDataManager
from utils.FantasyPlayer import FantasyPlayer
import json
import tempfile
import shutil

def print_section(title):
    print(f"\n{'='*80}")
    print(f"  {title}")
    print(f"{'='*80}\n")

def create_test_player(player_id, name, position, bye_week, drafted=0):
    """Create a test player with minimal required fields."""
    return FantasyPlayer(
        player_id=player_id,
        name=name,
        team="TEST",
        position=position,
        bye_week=bye_week,
        fantasy_points=100.0,
        injury_status="ACTIVE",
        drafted=drafted,
        locked=0,
        adp=50,
        player_rating=50,
        # Weekly points (all zeros for testing)
        **{f'week_{i}_points': 0.0 for i in range(1, 18)}
    )

def test_bye_penalty_calculation():
    """Test that bye penalties are calculated correctly."""
    print_section("TEST 1: Bye Penalty Calculation Logic")

    cm = ConfigManager(Path('data'))

    print("Current config values:")
    print(f"  BASE_BYE_PENALTY: {cm.base_bye_penalty}")
    print(f"  DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY: {cm.parameters.get('DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY', 'NOT SET')}")

    print("\nTest Case 1: No overlaps")
    penalty = cm.get_bye_week_penalty(num_same_position=0, num_different_position=0)
    print(f"  get_bye_week_penalty(0, 0) = {penalty}")
    if penalty == 0:
        print("  ✓ No overlaps = no penalty")
    else:
        print(f"  ✗ Expected 0, got {penalty}")
        return False

    print("\nTest Case 2: One same-position overlap")
    penalty = cm.get_bye_week_penalty(num_same_position=1, num_different_position=0)
    expected = cm.base_bye_penalty * 1
    print(f"  get_bye_week_penalty(1, 0) = {penalty}")
    print(f"  Expected: {expected} (BASE_BYE_PENALTY × 1)")
    if penalty == expected:
        print("  ✓ Correct same-position penalty")
    else:
        print(f"  ✗ Expected {expected}, got {penalty}")
        return False

    print("\nTest Case 3: Multiple same-position overlaps")
    penalty = cm.get_bye_week_penalty(num_same_position=3, num_different_position=0)
    expected = cm.base_bye_penalty * 3
    print(f"  get_bye_week_penalty(3, 0) = {penalty}")
    print(f"  Expected: {expected} (BASE_BYE_PENALTY × 3)")
    if penalty == expected:
        print("  ✓ Correct multiple same-position penalty")
    else:
        print(f"  ✗ Expected {expected}, got {penalty}")
        return False

    print("\nTest Case 4: One different-position overlap")
    penalty = cm.get_bye_week_penalty(num_same_position=0, num_different_position=1)
    different_penalty_param = cm.parameters.get('DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY', 0)
    expected = different_penalty_param * 1
    print(f"  get_bye_week_penalty(0, 1) = {penalty}")
    print(f"  Expected: {expected} (DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY × 1)")
    if penalty == expected:
        print("  ✓ Correct different-position penalty")
    else:
        print(f"  ✗ Expected {expected}, got {penalty}")
        return False

    print("\nTest Case 5: Multiple different-position overlaps")
    penalty = cm.get_bye_week_penalty(num_same_position=0, num_different_position=4)
    expected = different_penalty_param * 4
    print(f"  get_bye_week_penalty(0, 4) = {penalty}")
    print(f"  Expected: {expected} (DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY × 4)")
    if penalty == expected:
        print("  ✓ Correct multiple different-position penalty")
    else:
        print(f"  ✗ Expected {expected}, got {penalty}")
        return False

    print("\nTest Case 6: Mixed overlaps (2 same + 3 different)")
    penalty = cm.get_bye_week_penalty(num_same_position=2, num_different_position=3)
    expected = (cm.base_bye_penalty * 2) + (different_penalty_param * 3)
    print(f"  get_bye_week_penalty(2, 3) = {penalty}")
    print(f"  Expected: {expected} (BASE × 2 + DIFFERENT × 3)")
    if penalty == expected:
        print("  ✓ Correct mixed penalty calculation")
    else:
        print(f"  ✗ Expected {expected}, got {penalty}")
        return False

    print("\n✓ All bye penalty calculation tests passed")
    return True

def test_player_scoring_with_bye_penalties():
    """Test that bye penalties correctly affect player scoring."""
    print_section("TEST 2: Bye Penalties in Player Scoring")

    # Setup test environment
    cm = ConfigManager(Path('data'))
    team_mgr = TeamDataManager(Path('data'))

    # Create temporary data directory with test players
    temp_dir = Path(tempfile.mkdtemp())
    temp_players_csv = temp_dir / 'players.csv'

    # Create test roster with various bye weeks
    # Player being scored: QB, bye week 7
    # Roster: 2 same-position (QB, bye 7), 3 different-position (RB/WR/TE, bye 7)
    test_roster_data = [
        # Player being scored
        ('1', 'Test QB1', 'QB', 7, 0),  # Available, being evaluated
        # Same-position overlaps (2 QBs with bye 7 on roster)
        ('2', 'Roster QB2', 'QB', 7, 2),  # On roster, bye 7
        ('3', 'Roster QB3', 'QB', 7, 2),  # On roster, bye 7
        # Different-position overlaps (3 non-QBs with bye 7 on roster)
        ('4', 'Roster RB1', 'RB', 7, 2),  # On roster, bye 7
        ('5', 'Roster WR1', 'WR', 7, 2),  # On roster, bye 7
        ('6', 'Roster TE1', 'TE', 7, 2),  # On roster, bye 7
        # Non-overlapping roster players
        ('7', 'Roster RB2', 'RB', 9, 2),  # On roster, bye 9 (no conflict)
        ('8', 'Roster WR2', 'WR', 10, 2), # On roster, bye 10 (no conflict)
    ]

    # Write test CSV - give different players different projections to establish max_projection
    with open(temp_players_csv, 'w') as f:
        f.write('id,name,team,position,bye_week,fantasy_points,injury_status,drafted,locked,average_draft_position,player_rating,')
        f.write(','.join([f'week_{i}_points' for i in range(1, 18)]))
        f.write('\n')

        for i, (pid, name, pos, bye, drafted) in enumerate(test_roster_data):
            # Vary fantasy points to establish max_projection, highest for first player
            fantasy_points = 200.0 if i == 0 else 150.0 - (i * 5)
            f.write(f'{pid},{name},TEST,{pos},{bye},{fantasy_points},ACTIVE,{drafted},0,50,50,')
            f.write(','.join(['5.0'] * 17))  # Non-zero weekly points for consistency calc
            f.write('\n')

    # Create PlayerManager with test data
    player_mgr = PlayerManager(temp_dir, cm, team_mgr)

    # Get the player being scored (QB1, bye 7, available)
    # Note: FantasyPlayer.from_dict converts id to int
    test_player = next(p for p in player_mgr.players if str(p.id) == '1')

    print(f"Scoring player: {test_player.name} ({test_player.position}, Bye Week {test_player.bye_week})")
    print(f"\nRoster composition (bye week 7 overlaps):")
    print(f"  Same-position (QB, bye 7): 2 players")
    print(f"  Different-position (RB/WR/TE, bye 7): 3 players")
    print(f"  No overlap: 2 players")

    print(f"\nConfig penalties:")
    print(f"  BASE_BYE_PENALTY: {cm.base_bye_penalty}")
    different_penalty = cm.parameters.get('DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY', 0)
    print(f"  DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY: {different_penalty}")

    # Score without bye penalty
    print("\n--- Scoring WITHOUT bye penalty ---")
    result_no_bye = player_mgr.score_player(test_player, bye=False)
    print(f"Score: {result_no_bye.score:.2f}")

    # Score with bye penalty
    print("\n--- Scoring WITH bye penalty ---")
    result_with_bye = player_mgr.score_player(test_player, bye=True)
    print(f"Score: {result_with_bye.score:.2f}")

    # Find bye penalty reason in results (note: ScoredPlayer uses 'reason' not 'reasons')
    bye_reason = next((r for r in result_with_bye.reason if 'Bye' in r), None)
    if bye_reason:
        print(f"Reason: {bye_reason}")

    # Calculate expected penalty
    expected_penalty = (cm.base_bye_penalty * 2) + (different_penalty * 3)
    actual_penalty = result_no_bye.score - result_with_bye.score

    print(f"\nPenalty Analysis:")
    print(f"  Expected penalty: {expected_penalty:.2f} (BASE×2 + DIFFERENT×3)")
    print(f"  Actual penalty: {actual_penalty:.2f}")
    print(f"  Difference: {abs(expected_penalty - actual_penalty):.2f}")

    # Clean up
    temp_players_csv.unlink()
    temp_dir.rmdir()

    if abs(expected_penalty - actual_penalty) < 0.01:  # Allow small floating point error
        print("\n✓ Bye penalty correctly applied to player scoring")
        return True
    else:
        print(f"\n✗ Penalty mismatch: expected {expected_penalty:.2f}, got {actual_penalty:.2f}")
        return False

def test_config_changes_affect_penalties():
    """Test that changing config values changes penalty calculations."""
    print_section("TEST 3: Config Changes Affect Penalties")

    # Create temporary config with modified values
    temp_dir = Path(tempfile.mkdtemp())

    # Test with baseline config
    print("Loading baseline config...")
    cm_baseline = ConfigManager(Path('data'))
    baseline_base = cm_baseline.base_bye_penalty
    baseline_different = cm_baseline.parameters.get('DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY', 0)

    print(f"  BASE_BYE_PENALTY: {baseline_base}")
    print(f"  DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY: {baseline_different}")

    penalty_baseline = cm_baseline.get_bye_week_penalty(2, 3)
    print(f"  Penalty for (2 same, 3 different): {penalty_baseline:.2f}")

    # Create modified config
    print("\nCreating modified config...")
    with open('data/league_config.json', 'r') as f:
        config_dict = json.load(f)

    # Modify both penalties
    config_dict['parameters']['BASE_BYE_PENALTY'] = baseline_base * 2
    config_dict['parameters']['DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY'] = baseline_different * 3

    temp_config = temp_dir / 'league_config.json'
    with open(temp_config, 'w') as f:
        json.dump(config_dict, f)

    print(f"  BASE_BYE_PENALTY: {baseline_base} → {baseline_base * 2}")
    print(f"  DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY: {baseline_different} → {baseline_different * 3}")

    # Load modified config
    cm_modified = ConfigManager(temp_dir)
    modified_base = cm_modified.base_bye_penalty
    modified_different = cm_modified.parameters.get('DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY', 0)

    print(f"\nVerifying modified config loaded:")
    print(f"  BASE_BYE_PENALTY: {modified_base}")
    print(f"  DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY: {modified_different}")

    penalty_modified = cm_modified.get_bye_week_penalty(2, 3)
    print(f"  Penalty for (2 same, 3 different): {penalty_modified:.2f}")

    # Verify changes
    print("\nAnalyzing changes:")

    base_changed = abs(modified_base - baseline_base * 2) < 0.01
    different_changed = abs(modified_different - baseline_different * 3) < 0.01
    penalty_changed = penalty_modified > penalty_baseline

    expected_modified_penalty = (modified_base * 2) + (modified_different * 3)
    penalty_correct = abs(penalty_modified - expected_modified_penalty) < 0.01

    print(f"  BASE_BYE_PENALTY doubled: {'✓' if base_changed else '✗'}")
    print(f"  DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY tripled: {'✓' if different_changed else '✗'}")
    print(f"  Total penalty increased: {'✓' if penalty_changed else '✗'}")
    print(f"  Penalty calculation correct: {'✓' if penalty_correct else '✗'}")

    # Clean up
    temp_config.unlink()
    temp_dir.rmdir()

    if all([base_changed, different_changed, penalty_changed, penalty_correct]):
        print("\n✓ Config changes correctly affect penalty calculations")
        return True
    else:
        print("\n✗ Config changes did not affect penalties as expected")
        return False

def test_backward_compatibility():
    """Test that the method works with single argument (backward compatibility)."""
    print_section("TEST 4: Backward Compatibility")

    cm = ConfigManager(Path('data'))

    print("Testing backward compatibility with single argument...")
    print(f"  BASE_BYE_PENALTY: {cm.base_bye_penalty}")

    try:
        # Call with only num_same_position (old signature)
        penalty_old = cm.get_bye_week_penalty(3)
        expected_old = cm.base_bye_penalty * 3

        print(f"\nOld signature: get_bye_week_penalty(3)")
        print(f"  Result: {penalty_old}")
        print(f"  Expected: {expected_old}")

        if abs(penalty_old - expected_old) < 0.01:
            print("  ✓ Old signature still works (backward compatible)")
        else:
            print(f"  ✗ Expected {expected_old}, got {penalty_old}")
            return False

        # Call with both arguments (new signature)
        penalty_new = cm.get_bye_week_penalty(3, 2)
        different_penalty = cm.parameters.get('DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY', 0)
        expected_new = (cm.base_bye_penalty * 3) + (different_penalty * 2)

        print(f"\nNew signature: get_bye_week_penalty(3, 2)")
        print(f"  Result: {penalty_new}")
        print(f"  Expected: {expected_new}")

        if abs(penalty_new - expected_new) < 0.01:
            print("  ✓ New signature works correctly")
        else:
            print(f"  ✗ Expected {expected_new}, got {penalty_new}")
            return False

        print("\n✓ Backward compatibility maintained")
        return True

    except Exception as e:
        print(f"\n✗ Backward compatibility test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_edge_cases():
    """Test edge cases and boundary conditions."""
    print_section("TEST 5: Edge Cases")

    cm = ConfigManager(Path('data'))

    test_cases = [
        (0, 0, "No overlaps"),
        (10, 0, "Many same-position, no different"),
        (0, 10, "No same-position, many different"),
        (5, 5, "Equal same and different"),
        (1, 10, "Few same, many different"),
        (10, 1, "Many same, few different"),
    ]

    print("Testing edge cases:")
    all_passed = True

    for same, different, desc in test_cases:
        penalty = cm.get_bye_week_penalty(same, different)
        expected = (cm.base_bye_penalty * same) + (cm.parameters.get('DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY', 0) * different)

        passed = abs(penalty - expected) < 0.01
        status = "✓" if passed else "✗"

        print(f"  {status} {desc}: ({same}, {different}) → penalty={penalty:.2f}")

        if not passed:
            print(f"      Expected: {expected:.2f}")
            all_passed = False

    if all_passed:
        print("\n✓ All edge cases passed")
    else:
        print("\n✗ Some edge cases failed")

    return all_passed

def test_simulation_parameter_optimization():
    """Test that simulation system can optimize both bye penalty parameters."""
    print_section("TEST 6: Simulation Parameter Optimization Support")

    from simulation.ConfigGenerator import ConfigGenerator

    print("Checking ConfigGenerator parameter definitions...")
    gen = ConfigGenerator(Path('data/league_config.json'), num_test_values=2)

    # Check BASE_BYE_PENALTY
    if 'BASE_BYE_PENALTY' in gen.PARAMETER_ORDER:
        print("  ✓ BASE_BYE_PENALTY in PARAMETER_ORDER")
        idx = gen.PARAMETER_ORDER.index('BASE_BYE_PENALTY')
        print(f"    Position: {idx + 1}/{len(gen.PARAMETER_ORDER)}")
    else:
        print("  ✗ BASE_BYE_PENALTY not in PARAMETER_ORDER")
        return False

    # Check DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY
    if 'DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY' in gen.PARAMETER_ORDER:
        print("  ✓ DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY in PARAMETER_ORDER")
        idx = gen.PARAMETER_ORDER.index('DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY')
        print(f"    Position: {idx + 1}/{len(gen.PARAMETER_ORDER)}")
    else:
        print("  ✗ DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY not in PARAMETER_ORDER")
        return False

    # Test parameter value generation
    print("\nGenerating parameter value sets...")
    try:
        value_sets = gen.generate_all_parameter_value_sets()

        if 'BASE_BYE_PENALTY' in value_sets:
            base_values = value_sets['BASE_BYE_PENALTY']
            print(f"  ✓ BASE_BYE_PENALTY: {len(base_values)} values generated")
            print(f"    Range: {min(base_values):.2f} - {max(base_values):.2f}")
        else:
            print("  ✗ BASE_BYE_PENALTY not in value sets")
            return False

        if 'DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY' in value_sets:
            diff_values = value_sets['DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY']
            print(f"  ✓ DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY: {len(diff_values)} values generated")
            print(f"    Range: {min(diff_values):.2f} - {max(diff_values):.2f}")
        else:
            print("  ✗ DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY not in value sets")
            return False

        print("\n✓ Both bye penalty parameters available for simulation optimization")
        return True

    except Exception as e:
        print(f"\n✗ Parameter generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all bye penalty interactive tests."""
    print("\n" + "="*80)
    print("  BYE PENALTY INTERACTIVE TESTING")
    print("  Verifying BASE_BYE_PENALTY and DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY")
    print("="*80)

    tests = [
        ("Bye Penalty Calculation Logic", test_bye_penalty_calculation),
        ("Bye Penalties in Player Scoring", test_player_scoring_with_bye_penalties),
        ("Config Changes Affect Penalties", test_config_changes_affect_penalties),
        ("Backward Compatibility", test_backward_compatibility),
        ("Edge Cases", test_edge_cases),
        ("Simulation Parameter Optimization", test_simulation_parameter_optimization),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Error in {name}: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))

    # Summary
    print_section("TEST SUMMARY")
    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")

    print(f"\n{passed}/{total} tests passed")

    if passed == total:
        print("\n✓ Bye penalty system fully functional")
        print("✓ Both BASE_BYE_PENALTY and DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY working")
        print("✓ Config changes correctly modify scoring results")
        print("✓ Ready for simulation-based parameter optimization")
        return 0
    else:
        print("\n✗ Some tests failed - review output above")
        return 1

if __name__ == '__main__':
    exit(main())
