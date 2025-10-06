#!/usr/bin/env python3
"""
Test the new position-scaled bye week penalty formula across different scenarios
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from draft_helper.draft_helper import DraftHelper
from shared_files.FantasyPlayer import FantasyPlayer

def create_test_player(name, position, bye_week, drafted=0):
    """Create a test player"""
    return FantasyPlayer(
        id=name,
        name=name,
        team="TEST",
        position=position,
        bye_week=bye_week,
        fantasy_points=100.0,
        injury_status="ACTIVE",
        drafted=drafted
    )

def test_scenario(draft_helper, scenario_name, test_player, expected_conflicts, expected_penalty):
    """Test a specific scenario"""
    penalty = draft_helper.compute_bye_penalty_for_player(test_player)

    max_slots = draft_helper.scoring_engine.config.MAX_POSITIONS.get(test_player.position, 1)
    expected_calc = (expected_conflicts / max_slots) * 18.85

    print(f"\n{scenario_name}")
    print(f"  Position: {test_player.position} (max slots: {max_slots})")
    print(f"  Bye Week: {test_player.bye_week}")
    print(f"  Conflicts: {expected_conflicts}")
    print(f"  Expected: ({expected_conflicts}/{max_slots}) × 18.85 = {expected_calc:.2f}")
    print(f"  Actual: {penalty:.2f}")
    print(f"  ✓ PASS" if abs(penalty - expected_calc) < 0.01 else f"  ✗ FAIL")

    return abs(penalty - expected_calc) < 0.01

def main():
    print("="*80)
    print("BYE WEEK PENALTY FORMULA TEST - Position-Scaled Calculation")
    print("="*80)
    print("\nFormula: (Same-Position Conflicts / Max Position Slots) × BASE_BYE_PENALTY")
    print("BASE_BYE_PENALTY = 18.85")
    print("\nRoster Limits: QB=2, RB=4, WR=4, TE=2, K=1, DST=1")

    # Initialize draft helper
    draft_helper = DraftHelper("shared_files/players.csv")

    # Clear the roster
    draft_helper.team.roster = []

    all_passed = True

    # SCENARIO 1: No conflicts (baseline)
    print("\n" + "="*80)
    print("SCENARIO 1: No Conflicts (Empty Roster)")
    print("="*80)

    test_player = create_test_player("Test_RB1", "RB", 7)
    all_passed &= test_scenario(
        draft_helper,
        "RB with bye week 7 (no roster conflicts)",
        test_player,
        expected_conflicts=0,
        expected_penalty=0.0
    )

    # SCENARIO 2: Single position - Kicker (max 1)
    print("\n" + "="*80)
    print("SCENARIO 2: Kicker Position (Max Slots = 1)")
    print("="*80)

    draft_helper.team.roster = []
    kicker1 = create_test_player("K1", "K", 7, drafted=2)
    draft_helper.team.roster.append(kicker1)

    test_player = create_test_player("Test_K2", "K", 7)
    all_passed &= test_scenario(
        draft_helper,
        "2nd Kicker with same bye week 7",
        test_player,
        expected_conflicts=1,
        expected_penalty=18.85  # (1/1) × 18.85 = full penalty
    )

    # SCENARIO 3: QB position (max 2)
    print("\n" + "="*80)
    print("SCENARIO 3: QB Position (Max Slots = 2)")
    print("="*80)

    draft_helper.team.roster = []
    qb1 = create_test_player("QB1", "QB", 7, drafted=2)
    draft_helper.team.roster.append(qb1)

    test_player = create_test_player("Test_QB2", "QB", 7)
    all_passed &= test_scenario(
        draft_helper,
        "2nd QB with same bye week 7",
        test_player,
        expected_conflicts=1,
        expected_penalty=9.425  # (1/2) × 18.85
    )

    # SCENARIO 4: RB position (max 4) - 1 conflict
    print("\n" + "="*80)
    print("SCENARIO 4: RB Position - 1 Conflict (Max Slots = 4)")
    print("="*80)

    draft_helper.team.roster = []
    rb1 = create_test_player("RB1", "RB", 9, drafted=2)
    draft_helper.team.roster.append(rb1)

    test_player = create_test_player("Test_RB2", "RB", 9)
    all_passed &= test_scenario(
        draft_helper,
        "2nd RB with same bye week 9",
        test_player,
        expected_conflicts=1,
        expected_penalty=4.7125  # (1/4) × 18.85
    )

    # SCENARIO 5: RB position (max 4) - 2 conflicts
    print("\n" + "="*80)
    print("SCENARIO 5: RB Position - 2 Conflicts (Max Slots = 4)")
    print("="*80)

    rb2 = create_test_player("RB2", "RB", 9, drafted=2)
    draft_helper.team.roster.append(rb2)

    test_player = create_test_player("Test_RB3", "RB", 9)
    all_passed &= test_scenario(
        draft_helper,
        "3rd RB with same bye week 9",
        test_player,
        expected_conflicts=2,
        expected_penalty=9.425  # (2/4) × 18.85
    )

    # SCENARIO 6: RB position (max 4) - 3 conflicts
    print("\n" + "="*80)
    print("SCENARIO 6: RB Position - 3 Conflicts (Max Slots = 4)")
    print("="*80)

    rb3 = create_test_player("RB3", "RB", 9, drafted=2)
    draft_helper.team.roster.append(rb3)

    test_player = create_test_player("Test_RB4", "RB", 9)
    all_passed &= test_scenario(
        draft_helper,
        "4th RB with same bye week 9",
        test_player,
        expected_conflicts=3,
        expected_penalty=14.1375  # (3/4) × 18.85
    )

    # SCENARIO 7: Different bye weeks don't conflict
    print("\n" + "="*80)
    print("SCENARIO 7: Different Bye Weeks (No Conflict)")
    print("="*80)

    draft_helper.team.roster = []
    wr1 = create_test_player("WR1", "WR", 7, drafted=2)
    wr2 = create_test_player("WR2", "WR", 9, drafted=2)
    draft_helper.team.roster.extend([wr1, wr2])

    test_player = create_test_player("Test_WR3", "WR", 11)
    all_passed &= test_scenario(
        draft_helper,
        "WR with different bye week (7, 9 on roster, testing 11)",
        test_player,
        expected_conflicts=0,
        expected_penalty=0.0
    )

    # SCENARIO 8: Different positions don't conflict
    print("\n" + "="*80)
    print("SCENARIO 8: Different Positions (No Conflict)")
    print("="*80)

    draft_helper.team.roster = []
    qb = create_test_player("QB", "QB", 7, drafted=2)
    rb = create_test_player("RB", "RB", 7, drafted=2)
    wr = create_test_player("WR", "WR", 7, drafted=2)
    draft_helper.team.roster.extend([qb, rb, wr])

    test_player = create_test_player("Test_TE", "TE", 7)
    all_passed &= test_scenario(
        draft_helper,
        "TE with bye week 7 (QB, RB, WR all have week 7 too)",
        test_player,
        expected_conflicts=0,
        expected_penalty=0.0
    )

    # SCENARIO 9: Exclude self in trade mode
    print("\n" + "="*80)
    print("SCENARIO 9: Exclude Self (Trade Mode)")
    print("="*80)

    draft_helper.team.roster = []
    existing_wr = create_test_player("Existing_WR", "WR", 10, drafted=2)
    draft_helper.team.roster.append(existing_wr)

    # When evaluating a roster player, exclude self from conflict count
    penalty_without_exclude = draft_helper.scoring_engine.compute_bye_penalty_for_player(
        existing_wr, exclude_self=False
    )
    penalty_with_exclude = draft_helper.scoring_engine.compute_bye_penalty_for_player(
        existing_wr, exclude_self=True
    )

    print(f"\nExisting roster WR with bye week 10")
    print(f"  Without exclude_self: {penalty_without_exclude:.2f} (counts self as conflict)")
    print(f"  With exclude_self: {penalty_with_exclude:.2f} (doesn't count self)")
    print(f"  ✓ PASS" if penalty_with_exclude == 0.0 else f"  ✗ FAIL")

    all_passed &= (penalty_with_exclude == 0.0)

    # Final summary
    print("\n" + "="*80)
    print("FINAL SUMMARY")
    print("="*80)
    if all_passed:
        print("✓ ALL TESTS PASSED - Bye week penalty formula is working correctly!")
    else:
        print("✗ SOME TESTS FAILED - Check the output above")

    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
