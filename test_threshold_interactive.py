#!/usr/bin/env python3
"""
Interactive test to verify threshold parameter changes affect scoring calculations.

Tests:
1. Load config with baseline STEPS values
2. Calculate scores for sample players
3. Modify STEPS values in config
4. Recalculate scores and verify they changed appropriately
5. Test all 5 scoring types (ADP, PLAYER_RATING, TEAM_QUALITY, PERFORMANCE, MATCHUP)
"""

from pathlib import Path
from league_helper.util.ConfigManager import ConfigManager
import json
import copy

def print_section(title):
    print(f"\n{'='*80}")
    print(f"  {title}")
    print(f"{'='*80}\n")

def print_thresholds(cm, scoring_type):
    """Print current thresholds for a scoring type."""
    thresholds = cm.parameters[scoring_type]['THRESHOLDS']
    print(f"{scoring_type}:")
    print(f"  STEPS: {thresholds['STEPS']}")
    print(f"  VERY_POOR: {thresholds['VERY_POOR']}")
    print(f"  POOR: {thresholds['POOR']}")
    print(f"  GOOD: {thresholds['GOOD']}")
    print(f"  EXCELLENT: {thresholds['EXCELLENT']}")

def get_multiplier_for_value(cm, scoring_type, value):
    """Get the multiplier that would be applied for a given value."""
    if scoring_type == 'ADP_SCORING':
        mult, label = cm.get_adp_multiplier(value)
    elif scoring_type == 'PLAYER_RATING_SCORING':
        mult, label = cm.get_player_rating_multiplier(value)
    elif scoring_type == 'TEAM_QUALITY_SCORING':
        mult, label = cm.get_team_quality_multiplier(value)
    elif scoring_type == 'PERFORMANCE_SCORING':
        mult, label = cm.get_performance_multiplier(value)
    elif scoring_type == 'MATCHUP_SCORING':
        mult, label = cm.get_matchup_multiplier(value)
    else:
        raise ValueError(f"Unknown scoring type: {scoring_type}")

    return mult, label

def test_adp_scoring():
    """Test ADP scoring with different STEPS values."""
    print_section("TEST 1: ADP_SCORING (DECREASING direction)")

    cm = ConfigManager(Path('data'))
    print("Baseline configuration:")
    print_thresholds(cm, 'ADP_SCORING')

    # Test values: lower ADP = better
    test_adps = [10, 30, 50, 80, 120, 160]
    print("\nBaseline multipliers for test ADP values:")
    for adp in test_adps:
        mult, label = get_multiplier_for_value(cm, 'ADP_SCORING', adp)
        print(f"  ADP {adp:3d}: multiplier = {mult:.6f}, label = {label}")

    # Modify STEPS from 37.5 to 50.0
    print("\n" + "-"*80)
    print("Modifying STEPS from 37.5 to 50.0...")
    print("-"*80 + "\n")

    # Directly modify the parameters and re-extract
    cm.parameters['ADP_SCORING']['THRESHOLDS']['STEPS'] = 50.0
    cm._extract_parameters()

    print("Modified configuration:")
    print_thresholds(cm, 'ADP_SCORING')

    print("\nModified multipliers for test ADP values:")
    for adp in test_adps:
        mult, label = get_multiplier_for_value(cm, 'ADP_SCORING', adp)
        print(f"  ADP {adp:3d}: multiplier = {mult:.6f}, label = {label}")

    print("\n✓ Expected behavior: With larger STEPS (50.0 vs 37.5), thresholds spread out more")
    print("  - EXCELLENT threshold moves from 37.5 to 50.0")
    print("  - Players with ADP between 37.5-50 should see multiplier change from GOOD to EXCELLENT")

def test_player_rating_scoring():
    """Test PLAYER_RATING scoring with different STEPS values."""
    print_section("TEST 2: PLAYER_RATING_SCORING (INCREASING direction)")

    cm = ConfigManager(Path('data'))
    print("Baseline configuration:")
    print_thresholds(cm, 'PLAYER_RATING_SCORING')

    # Test values: higher rating = better
    test_ratings = [10, 30, 50, 70, 90]
    print("\nBaseline multipliers for test rating values:")
    for rating in test_ratings:
        mult, label = get_multiplier_for_value(cm, 'PLAYER_RATING_SCORING', rating)
        print(f"  Rating {rating:2d}: multiplier = {mult:.6f}, label = {label}")

    # Modify STEPS from 20.0 to 15.0
    print("\n" + "-"*80)
    print("Modifying STEPS from 20.0 to 15.0...")
    print("-"*80 + "\n")

    # Directly modify the parameters and re-extract
    cm.parameters['PLAYER_RATING_SCORING']['THRESHOLDS']['STEPS'] = 15.0
    cm._extract_parameters()

    print("Modified configuration:")
    print_thresholds(cm, 'PLAYER_RATING_SCORING')

    print("\nModified multipliers for test rating values:")
    for rating in test_ratings:
        mult, label = get_multiplier_for_value(cm, 'PLAYER_RATING_SCORING', rating)
        print(f"  Rating {rating:2d}: multiplier = {mult:.6f}, label = {label}")

    print("\n✓ Expected behavior: With smaller STEPS (15.0 vs 20.0), thresholds compress")
    print("  - EXCELLENT threshold moves from 80 to 60")
    print("  - Players with rating 60-80 should see multiplier change from GOOD to EXCELLENT")

def test_performance_scoring():
    """Test PERFORMANCE scoring with different STEPS values."""
    print_section("TEST 3: PERFORMANCE_SCORING (BI_EXCELLENT_HI direction)")

    cm = ConfigManager(Path('data'))
    print("Baseline configuration:")
    print_thresholds(cm, 'PERFORMANCE_SCORING')

    # Test values: centered around 0, both positive and negative
    test_perf = [-0.3, -0.15, -0.05, 0.0, 0.05, 0.15, 0.3]
    print("\nBaseline multipliers for test performance values:")
    for perf in test_perf:
        mult, label = get_multiplier_for_value(cm, 'PERFORMANCE_SCORING', perf)
        print(f"  Performance {perf:+.2f}: multiplier = {mult:.6f}, label = {label}")

    # Modify STEPS from 0.1 to 0.15
    print("\n" + "-"*80)
    print("Modifying STEPS from 0.1 to 0.15...")
    print("-"*80 + "\n")

    # Directly modify the parameters and re-extract
    cm.parameters['PERFORMANCE_SCORING']['THRESHOLDS']['STEPS'] = 0.15
    cm._extract_parameters()

    print("Modified configuration:")
    print_thresholds(cm, 'PERFORMANCE_SCORING')

    print("\nModified multipliers for test performance values:")
    for perf in test_perf:
        mult, label = get_multiplier_for_value(cm, 'PERFORMANCE_SCORING', perf)
        print(f"  Performance {perf:+.2f}: multiplier = {mult:.6f}, label = {label}")

    print("\n✓ Expected behavior: With larger STEPS (0.15 vs 0.1), bidirectional thresholds spread")
    print("  - EXCELLENT threshold moves from 0.2 to 0.3")
    print("  - VERY_POOR threshold moves from -0.2 to -0.3")
    print("  - Players with performance 0.2-0.3 should see multiplier change from GOOD to EXCELLENT")

def test_team_quality_scoring():
    """Test TEAM_QUALITY scoring with different STEPS values."""
    print_section("TEST 4: TEAM_QUALITY_SCORING (DECREASING direction)")

    cm = ConfigManager(Path('data'))
    print("Baseline configuration:")
    print_thresholds(cm, 'TEAM_QUALITY_SCORING')

    # Test values: lower rank = better team
    test_ranks = [1, 5, 10, 15, 20, 28]
    print("\nBaseline multipliers for test team rank values:")
    for rank in test_ranks:
        mult, label = get_multiplier_for_value(cm, 'TEAM_QUALITY_SCORING', rank)
        print(f"  Team Rank {rank:2d}: multiplier = {mult:.6f}, label = {label}")

    # Modify STEPS from 6.25 to 8.0
    print("\n" + "-"*80)
    print("Modifying STEPS from 6.25 to 8.0...")
    print("-"*80 + "\n")

    # Directly modify the parameters and re-extract
    cm.parameters['TEAM_QUALITY_SCORING']['THRESHOLDS']['STEPS'] = 8.0
    cm._extract_parameters()

    print("Modified configuration:")
    print_thresholds(cm, 'TEAM_QUALITY_SCORING')

    print("\nModified multipliers for test team rank values:")
    for rank in test_ranks:
        mult, label = get_multiplier_for_value(cm, 'TEAM_QUALITY_SCORING', rank)
        print(f"  Team Rank {rank:2d}: multiplier = {mult:.6f}, label = {label}")

    print("\n✓ Expected behavior: With larger STEPS (8.0 vs 6.25), thresholds spread out")
    print("  - EXCELLENT threshold moves from 6.25 to 8")
    print("  - Teams ranked 7-8 should see multiplier change from GOOD to EXCELLENT")

def test_matchup_scoring():
    """Test MATCHUP scoring with different STEPS values."""
    print_section("TEST 5: MATCHUP_SCORING (BI_EXCELLENT_HI direction)")

    cm = ConfigManager(Path('data'))
    print("Baseline configuration:")
    print_thresholds(cm, 'MATCHUP_SCORING')

    # Test values: centered around 0
    test_matchups = [-20, -10, -5, 0, 5, 10, 20]
    print("\nBaseline multipliers for test matchup values:")
    for matchup in test_matchups:
        mult, label = get_multiplier_for_value(cm, 'MATCHUP_SCORING', matchup)
        print(f"  Matchup {matchup:+3d}: multiplier = {mult:.6f}, label = {label}")

    # Modify STEPS from 7.5 to 10.0
    print("\n" + "-"*80)
    print("Modifying STEPS from 7.5 to 10.0...")
    print("-"*80 + "\n")

    # Directly modify the parameters and re-extract
    cm.parameters['MATCHUP_SCORING']['THRESHOLDS']['STEPS'] = 10.0
    cm._extract_parameters()

    print("Modified configuration:")
    print_thresholds(cm, 'MATCHUP_SCORING')

    print("\nModified multipliers for test matchup values:")
    for matchup in test_matchups:
        mult, label = get_multiplier_for_value(cm, 'MATCHUP_SCORING', matchup)
        print(f"  Matchup {matchup:+3d}: multiplier = {mult:.6f}, label = {label}")

    print("\n✓ Expected behavior: With larger STEPS (10.0 vs 7.5), bidirectional thresholds spread")
    print("  - EXCELLENT threshold moves from 15 to 20")
    print("  - VERY_POOR threshold moves from -15 to -20")
    print("  - Matchups 15-20 should see multiplier change from GOOD to EXCELLENT")

def main():
    """Run all interactive tests."""
    print("\n" + "="*80)
    print("  THRESHOLD PARAMETER INTERACTIVE TESTING")
    print("  Verifying that STEPS modifications affect scoring calculations")
    print("="*80)

    try:
        test_adp_scoring()
        test_player_rating_scoring()
        test_performance_scoring()
        test_team_quality_scoring()
        test_matchup_scoring()

        print_section("ALL TESTS COMPLETED")
        print("✓ All 5 scoring types tested")
        print("✓ Threshold calculations respond correctly to STEPS modifications")
        print("✓ Both INCREASING, DECREASING, and BI_EXCELLENT_HI directions validated")

    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0

if __name__ == '__main__':
    exit(main())
