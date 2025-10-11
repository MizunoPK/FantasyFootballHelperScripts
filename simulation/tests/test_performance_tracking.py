"""
Test script for ConfigPerformance and ResultsManager

Tests that performance tracking correctly:
- Tracks individual config results across multiple simulations
- Calculates win rates and average points correctly
- Compares configs properly (win rate primary, points tiebreaker)
- Identifies best configuration
- Saves results with proper metadata

Author: Kai Mizuno
Date: 2024
"""

import sys
from pathlib import Path
import tempfile
import shutil

sys.path.append(str(Path(__file__).parent))
from ConfigPerformance import ConfigPerformance
from ResultsManager import ResultsManager


def test_config_performance():
    """Test ConfigPerformance individual tracking."""
    print("\n" + "=" * 80)
    print("Testing ConfigPerformance")
    print("=" * 80)

    # Create a test config
    config_dict = {
        'config_name': 'test_config',
        'parameters': {
            'NORMALIZATION_MAX_SCALE': 100.0,
            'BASE_BYE_PENALTY': 25.0
        }
    }

    perf = ConfigPerformance("config_0001", config_dict)
    print(f"✓ Created ConfigPerformance: {perf.config_id}")

    # Test initial state
    assert perf.total_wins == 0
    assert perf.total_losses == 0
    assert perf.total_points == 0.0
    assert perf.num_simulations == 0
    assert perf.get_win_rate() == 0.0
    assert perf.get_avg_points_per_league() == 0.0
    print("✓ Initial state correct (all zeros)")

    # Add first simulation result
    perf.add_league_result(10, 7, 1404.62)
    assert perf.total_wins == 10
    assert perf.total_losses == 7
    assert perf.total_games == 17
    assert perf.total_points == 1404.62
    assert perf.num_simulations == 1
    print(f"✓ First simulation added: {perf.total_wins}W-{perf.total_losses}L, {perf.total_points:.2f} pts")

    # Verify win rate calculation
    expected_win_rate = 10 / 17
    actual_win_rate = perf.get_win_rate()
    assert abs(actual_win_rate - expected_win_rate) < 0.0001
    print(f"✓ Win rate correct: {actual_win_rate:.4f} (expected {expected_win_rate:.4f})")

    # Verify average points calculation
    expected_avg = 1404.62
    actual_avg = perf.get_avg_points_per_league()
    assert abs(actual_avg - expected_avg) < 0.01
    print(f"✓ Avg points correct: {actual_avg:.2f} (expected {expected_avg:.2f})")

    # Add more simulation results
    perf.add_league_result(12, 5, 1523.45)
    perf.add_league_result(8, 9, 1320.88)
    assert perf.num_simulations == 3
    assert perf.total_wins == 30
    assert perf.total_losses == 21
    assert perf.total_games == 51
    print(f"✓ Multiple simulations: {perf.num_simulations} sims, {perf.total_wins}W-{perf.total_losses}L")

    # Verify aggregated calculations
    expected_win_rate = 30 / 51
    actual_win_rate = perf.get_win_rate()
    assert abs(actual_win_rate - expected_win_rate) < 0.0001
    print(f"✓ Aggregated win rate: {actual_win_rate:.4f}")

    expected_avg = (1404.62 + 1523.45 + 1320.88) / 3
    actual_avg = perf.get_avg_points_per_league()
    assert abs(actual_avg - expected_avg) < 0.01
    print(f"✓ Aggregated avg points: {actual_avg:.2f}")

    # Test to_dict() serialization
    perf_dict = perf.to_dict()
    assert perf_dict['config_id'] == 'config_0001'
    assert perf_dict['total_wins'] == 30
    assert perf_dict['total_losses'] == 21
    assert perf_dict['num_simulations'] == 3
    assert 'win_rate' in perf_dict
    assert 'avg_points_per_league' in perf_dict
    print("✓ Serialization to dict works correctly")

    print("\n✅ ConfigPerformance tests passed!\n")
    return perf


def test_config_comparison():
    """Test ConfigPerformance comparison logic."""
    print("=" * 80)
    print("Testing ConfigPerformance Comparison")
    print("=" * 80)

    # Create two configs with different win rates
    config1 = ConfigPerformance("config_001", {})
    config1.add_league_result(12, 5, 1500.0)  # 12/17 = 70.6% win rate

    config2 = ConfigPerformance("config_002", {})
    config2.add_league_result(10, 7, 1600.0)  # 10/17 = 58.8% win rate

    # config1 should win (higher win rate)
    result = config1.compare_to(config2)
    assert result == 1, f"Expected 1, got {result}"
    print(f"✓ config1 (win_rate={config1.get_win_rate():.2%}) beats config2 (win_rate={config2.get_win_rate():.2%})")

    # Test reverse comparison
    result = config2.compare_to(config1)
    assert result == -1
    print(f"✓ Reverse comparison works correctly")

    # Test equal win rates with different points (tiebreaker)
    config3 = ConfigPerformance("config_003", {})
    config3.add_league_result(10, 7, 1450.0)  # Same 58.8% win rate, fewer points

    result = config2.compare_to(config3)
    assert result == 1, "Higher points should win when win rates equal"
    print(f"✓ Points tiebreaker works (1600 pts > 1450 pts)")

    # Test essentially equal configs (within 0.01 points threshold)
    config4 = ConfigPerformance("config_004", {})
    config4.add_league_result(10, 7, 1600.005)  # Within 0.01 of config2's 1600.0

    result = config2.compare_to(config4)
    assert result == 0, "Essentially equal configs should tie"
    print(f"✓ Essentially equal configs tie correctly")

    print("\n✅ Comparison tests passed!\n")


def test_results_manager():
    """Test ResultsManager aggregation and best config selection."""
    print("=" * 80)
    print("Testing ResultsManager")
    print("=" * 80)

    mgr = ResultsManager()
    print("✓ ResultsManager initialized")

    # Test empty state
    assert len(mgr.results) == 0
    assert mgr.get_best_config() is None
    print("✓ Empty state handled correctly")

    # Register and test multiple configs
    configs = [
        ("config_001", {'name': 'config_001'}, [(10, 7, 1404.62), (12, 5, 1523.45)]),
        ("config_002", {'name': 'config_002'}, [(11, 6, 1450.30), (9, 8, 1380.75)]),
        ("config_003", {'name': 'config_003'}, [(13, 4, 1600.20), (14, 3, 1650.88)]),  # Best config
        ("config_004", {'name': 'config_004'}, [(8, 9, 1320.50), (7, 10, 1290.33)]),
        ("config_005", {'name': 'config_005'}, [(12, 5, 1500.00), (11, 6, 1475.25)]),
    ]

    print(f"\nRegistering and simulating {len(configs)} configs...")
    for config_id, config_dict, results in configs:
        mgr.register_config(config_id, config_dict)
        for wins, losses, points in results:
            mgr.record_result(config_id, wins, losses, points)

    print(f"✓ Registered {len(mgr.results)} configs with multiple simulations each")

    # Verify best config selection
    best = mgr.get_best_config()
    assert best is not None
    assert best.config_id == "config_003", f"Expected config_003, got {best.config_id}"
    print(f"✓ Best config identified: {best.config_id}")
    print(f"  Win rate: {best.get_win_rate():.2%}")
    print(f"  Record: {best.total_wins}W-{best.total_losses}L")
    print(f"  Avg points: {best.get_avg_points_per_league():.2f}")
    print(f"  Simulations: {best.num_simulations}")

    # Test top N configs
    top_3 = mgr.get_top_n_configs(3)
    assert len(top_3) == 3
    assert top_3[0].config_id == "config_003"
    print(f"\n✓ Top 3 configs retrieved:")
    for i, config in enumerate(top_3, 1):
        print(f"  {i}. {config.config_id}: {config.get_win_rate():.2%} win rate, {config.get_avg_points_per_league():.2f} avg pts")

    # Verify sorting is correct
    for i in range(len(top_3) - 1):
        curr = top_3[i]
        next_config = top_3[i + 1]
        assert curr.compare_to(next_config) >= 0, "Top N should be sorted best to worst"
    print("✓ Top N configs correctly sorted")

    # Test statistics
    stats = mgr.get_stats()
    assert stats['total_configs'] == 5
    assert 'min_win_rate' in stats
    assert 'max_win_rate' in stats
    assert 'avg_win_rate' in stats
    assert 'min_avg_points' in stats
    assert 'max_avg_points' in stats
    print(f"\n✓ Statistics calculated:")
    print(f"  Total configs: {stats['total_configs']}")
    print(f"  Win rate range: {stats['min_win_rate']:.2%} - {stats['max_win_rate']:.2%}")
    print(f"  Avg win rate: {stats['avg_win_rate']:.2%}")
    print(f"  Points range: {stats['min_avg_points']:.2f} - {stats['max_avg_points']:.2f}")

    print("\n✅ ResultsManager tests passed!\n")
    return mgr


def test_save_functionality():
    """Test saving optimal config and all results."""
    print("=" * 80)
    print("Testing Save Functionality")
    print("=" * 80)

    # Create temp directory for testing
    temp_dir = Path(tempfile.mkdtemp())
    print(f"✓ Created temp directory: {temp_dir}")

    try:
        # Create ResultsManager with test data
        mgr = ResultsManager()

        configs = [
            ("config_001", {'param1': 100.0}, [(10, 7, 1404.62)]),
            ("config_002", {'param1': 110.0}, [(12, 5, 1523.45)]),  # Best
            ("config_003", {'param1': 90.0}, [(8, 9, 1320.88)]),
        ]

        for config_id, config_dict, results in configs:
            mgr.register_config(config_id, config_dict)
            for wins, losses, points in results:
                mgr.record_result(config_id, wins, losses, points)

        # Test save_optimal_config
        output_path = mgr.save_optimal_config(temp_dir)
        assert output_path.exists(), "Optimal config file should exist"
        assert output_path.parent == temp_dir
        assert output_path.name.startswith("optimal_")
        assert output_path.name.endswith(".json")
        print(f"✓ Saved optimal config to: {output_path.name}")

        # Verify optimal config contents
        import json
        with open(output_path, 'r') as f:
            saved_config = json.load(f)

        assert 'param1' in saved_config
        assert 'performance_metrics' in saved_config
        metrics = saved_config['performance_metrics']
        assert metrics['config_id'] == 'config_002'
        assert 'win_rate' in metrics
        assert 'total_wins' in metrics
        assert 'total_losses' in metrics
        assert 'avg_points_per_league' in metrics
        assert 'timestamp' in metrics
        print("✓ Optimal config contains correct data and metadata")

        # Test save_all_results
        all_results_path = temp_dir / "all_results.json"
        mgr.save_all_results(all_results_path)
        assert all_results_path.exists()
        print(f"✓ Saved all results to: {all_results_path.name}")

        # Verify all results contents
        with open(all_results_path, 'r') as f:
            all_results = json.load(f)

        assert 'total_configs' in all_results
        assert all_results['total_configs'] == 3
        assert 'configs' in all_results
        assert len(all_results['configs']) == 3
        assert 'config_001' in all_results['configs']
        assert 'config_002' in all_results['configs']
        assert 'config_003' in all_results['configs']
        print("✓ All results file contains complete data")

        print("\n✅ Save functionality tests passed!\n")

    finally:
        # Cleanup temp directory
        shutil.rmtree(temp_dir)
        print(f"✓ Cleaned up temp directory")


def test_print_summary():
    """Test print_summary output."""
    print("=" * 80)
    print("Testing Print Summary")
    print("=" * 80)

    mgr = ResultsManager()

    # Add test data
    for i in range(15):
        config_id = f"config_{i:04d}"
        config_dict = {'test_param': float(i)}
        mgr.register_config(config_id, config_dict)

        # Vary performance to test ranking
        wins = 10 + (i % 5)
        losses = 17 - wins
        points = 1400.0 + (i * 10)

        mgr.record_result(config_id, wins, losses, points)

    print(f"\n✓ Created {len(mgr.results)} test configs")

    # Test print_summary (visual inspection)
    print("\nTesting print_summary output (top 5):")
    mgr.print_summary(top_n=5)

    print("✅ Print summary test complete!\n")


def main():
    print("\n" + "=" * 80)
    print("PERFORMANCE TRACKING TEST SUITE")
    print("=" * 80)

    try:
        # Run all tests
        test_config_performance()
        test_config_comparison()
        test_results_manager()
        test_save_functionality()
        test_print_summary()

        print("=" * 80)
        print("ALL TESTS PASSED! ✅")
        print("=" * 80)
        print("\nPhase 4 (Performance Tracking) is complete and validated.")
        print("Ready to proceed to Phase 5 (Parallel Execution).\n")

    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}\n")
        raise
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
        raise


if __name__ == "__main__":
    main()
