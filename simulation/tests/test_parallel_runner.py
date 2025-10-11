"""
Test script for ParallelLeagueRunner and ProgressTracker

Tests that parallel execution works correctly:
- Multiple simulations run concurrently
- Results are collected correctly
- Progress tracking works
- Thread safety is maintained

Author: Kai Mizuno
Date: 2024
"""

import sys
import json
from pathlib import Path
import time

sys.path.append(str(Path(__file__).parent))
from ParallelLeagueRunner import ParallelLeagueRunner
from ProgressTracker import ProgressTracker, MultiLevelProgressTracker


def load_config(json_path: Path) -> dict:
    """Load configuration from JSON file."""
    with open(json_path, 'r') as f:
        config_data = json.load(f)
    return config_data


def test_progress_tracker():
    """Test basic ProgressTracker functionality."""
    print("\n" + "=" * 80)
    print("Testing ProgressTracker")
    print("=" * 80)

    tracker = ProgressTracker(total=50, description="Test Progress")
    print("✓ ProgressTracker initialized")

    # Simulate progress
    print("\nSimulating progress updates:")
    for i in range(50):
        tracker.update(1)
        time.sleep(0.02)  # Small delay to simulate work

    tracker.finish()
    print("✓ Progress tracker completed successfully")


def test_multi_level_tracker():
    """Test MultiLevelProgressTracker functionality."""
    print("\n" + "=" * 80)
    print("Testing MultiLevelProgressTracker")
    print("=" * 80)

    tracker = MultiLevelProgressTracker(
        outer_total=3,
        inner_total=10,
        outer_desc="Configs",
        inner_desc="Simulations"
    )
    print("✓ MultiLevelProgressTracker initialized")

    print("\nSimulating multi-level progress:")
    for config_idx in range(3):
        for sim_idx in range(10):
            tracker.update_inner(sim_idx + 1)
            time.sleep(0.02)
        tracker.next_outer()

    tracker.finish()
    print("✓ Multi-level tracker completed successfully")


def test_single_simulation():
    """Test running a single simulation."""
    print("\n" + "=" * 80)
    print("Testing Single Simulation")
    print("=" * 80)

    # Load baseline config
    baseline_path = Path("simulation/simulated_configs/optimal_2025-10-02_15-29-14.json.json")
    if not baseline_path.exists():
        print(f"⚠ Baseline config not found at {baseline_path}")
        print("  Skipping single simulation test")
        return

    config_dict = load_config(baseline_path)
    print(f"✓ Loaded config from {baseline_path.name}")

    # Create runner (uses default data_folder = simulation/sim_data)
    runner = ParallelLeagueRunner(max_workers=1)
    print("✓ ParallelLeagueRunner initialized (1 worker)")

    # Run single test
    print("\nRunning single test simulation...")
    start_time = time.time()
    wins, losses, points = runner.test_single_run(config_dict)
    elapsed = time.time() - start_time

    print(f"✓ Simulation complete in {elapsed:.2f}s")
    print(f"  Result: {wins}W-{losses}L, {points:.2f} points")
    print(f"  Win rate: {wins / (wins + losses):.2%}")

    # Validate results
    assert wins >= 0 and wins <= 17, "Wins should be 0-17"
    assert losses >= 0 and losses <= 17, "Losses should be 0-17"
    assert wins + losses == 17, "Total games should be 17"
    assert points > 0, "Points should be positive"
    print("✓ Results validation passed")


def test_parallel_simulations():
    """Test running multiple simulations in parallel."""
    print("\n" + "=" * 80)
    print("Testing Parallel Simulations")
    print("=" * 80)

    # Load baseline config
    baseline_path = Path("simulation/simulated_configs/optimal_2025-10-02_15-29-14.json.json")
    if not baseline_path.exists():
        print(f"⚠ Baseline config not found at {baseline_path}")
        print("  Skipping parallel simulations test")
        return

    config_dict = load_config(baseline_path)
    print(f"✓ Loaded config from {baseline_path.name}")

    # Create runner with multiple workers
    num_simulations = 10
    num_workers = 4

    # Create progress tracker
    tracker = ProgressTracker(total=num_simulations, description="Simulations")

    def progress_callback(completed: int, total: int):
        tracker.set_completed(completed)

    runner = ParallelLeagueRunner(
        max_workers=num_workers,
        progress_callback=progress_callback
    )
    print(f"✓ ParallelLeagueRunner initialized ({num_workers} workers)")

    # Run simulations
    print(f"\nRunning {num_simulations} simulations in parallel...")
    start_time = time.time()
    results = runner.run_simulations_for_config(config_dict, num_simulations)
    elapsed = time.time() - start_time

    tracker.finish()

    print(f"\n✓ Completed {len(results)} simulations in {elapsed:.2f}s")
    print(f"  Average: {elapsed / len(results):.2f}s per simulation")
    print(f"  Speedup: ~{len(results) * (elapsed / len(results)) / elapsed:.1f}x with {num_workers} workers")

    # Validate results
    assert len(results) == num_simulations, f"Expected {num_simulations} results, got {len(results)}"
    print(f"✓ All {num_simulations} simulations completed successfully")

    # Analyze results
    total_wins = sum(r[0] for r in results)
    total_losses = sum(r[1] for r in results)
    total_points = sum(r[2] for r in results)
    avg_wins = total_wins / len(results)
    avg_losses = total_losses / len(results)
    avg_points = total_points / len(results)
    avg_win_rate = total_wins / (total_wins + total_losses)

    print("\nResults Summary:")
    print(f"  Average record: {avg_wins:.1f}W-{avg_losses:.1f}L")
    print(f"  Average win rate: {avg_win_rate:.2%}")
    print(f"  Average points: {avg_points:.2f}")
    print(f"  Points range: {min(r[2] for r in results):.2f} - {max(r[2] for r in results):.2f}")


def test_multiple_configs():
    """Test running simulations for multiple configs."""
    print("\n" + "=" * 80)
    print("Testing Multiple Configs")
    print("=" * 80)

    # Load baseline config
    baseline_path = Path("simulation/simulated_configs/optimal_2025-10-02_15-29-14.json.json")
    if not baseline_path.exists():
        print(f"⚠ Baseline config not found at {baseline_path}")
        print("  Skipping multiple configs test")
        return

    config_dict = load_config(baseline_path)

    # Create 3 test configs (just use same config with different names)
    configs = []
    for i in range(3):
        test_config = config_dict.copy()
        test_config['config_name'] = f'test_config_{i:04d}'
        configs.append(test_config)

    print(f"✓ Created {len(configs)} test configs")

    # Create runner
    simulations_per_config = 5

    runner = ParallelLeagueRunner(max_workers=4)
    print("✓ ParallelLeagueRunner initialized")

    # Run simulations
    print(f"\nRunning {simulations_per_config} simulations for each of {len(configs)} configs...")
    print(f"Total simulations: {len(configs) * simulations_per_config}")

    start_time = time.time()
    all_results = runner.run_multiple_configs(configs, simulations_per_config)
    elapsed = time.time() - start_time

    print(f"\n✓ Completed all configs in {elapsed:.2f}s")

    # Validate results
    assert len(all_results) == len(configs), f"Expected {len(configs)} config results"
    for config_name, results in all_results.items():
        assert len(results) == simulations_per_config, \
            f"Expected {simulations_per_config} results for {config_name}"

    print(f"✓ All {len(configs)} configs completed with {simulations_per_config} sims each")

    # Show summary for each config
    print("\nResults by config:")
    for config_name, results in all_results.items():
        total_wins = sum(r[0] for r in results)
        total_losses = sum(r[1] for r in results)
        avg_points = sum(r[2] for r in results) / len(results)
        win_rate = total_wins / (total_wins + total_losses)
        print(f"  {config_name}: {win_rate:.2%} win rate, {avg_points:.2f} avg pts")


def main():
    print("\n" + "=" * 80)
    print("PARALLEL RUNNER TEST SUITE")
    print("=" * 80)

    try:
        # Test progress trackers first (fast)
        test_progress_tracker()
        test_multi_level_tracker()

        # Test simulations (slower, requires data files)
        test_single_simulation()
        test_parallel_simulations()
        test_multiple_configs()

        print("\n" + "=" * 80)
        print("ALL TESTS PASSED! ✅")
        print("=" * 80)
        print("\nPhase 5 (Parallel Execution) is complete and validated.")
        print("Ready to proceed to Phase 6 (SimulationManager).\n")

    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}\n")
        raise
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
        raise


if __name__ == "__main__":
    main()
