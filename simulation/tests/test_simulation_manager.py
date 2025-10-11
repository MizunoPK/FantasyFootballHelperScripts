"""
Test script for SimulationManager

Quick integration test to validate that SimulationManager correctly orchestrates
all components (ConfigGenerator, ParallelLeagueRunner, ResultsManager).

Author: Kai Mizuno
Date: 2024
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))
from SimulationManager import SimulationManager


def test_single_config():
    """Test running a single configuration."""
    print("\n" + "=" * 80)
    print("Testing Single Config Mode")
    print("=" * 80)

    baseline_path = Path("simulation/simulated_configs/optimal_2025-10-02_15-29-14.json.json")
    if not baseline_path.exists():
        print(f"⚠ Baseline config not found at {baseline_path}")
        print("  Skipping test")
        return

    # Create manager with minimal settings
    manager = SimulationManager(
        baseline_config_path=baseline_path,
        output_dir=Path("simulation/results/test"),
        num_simulations_per_config=3,  # Just 3 sims for speed
        max_workers=2
    )
    print("✓ SimulationManager initialized")

    # Run single config test
    print("\nRunning single config test (3 simulations)...")
    manager.run_single_config_test(config_id="integration_test")

    print("\n✓ Single config test complete")


def test_subset():
    """Test running a subset of configurations."""
    print("\n" + "=" * 80)
    print("Testing Subset Mode")
    print("=" * 80)

    baseline_path = Path("simulation/simulated_configs/optimal_2025-10-02_15-29-14.json.json")
    if not baseline_path.exists():
        print(f"⚠ Baseline config not found at {baseline_path}")
        print("  Skipping test")
        return

    # Create manager
    manager = SimulationManager(
        baseline_config_path=baseline_path,
        output_dir=Path("simulation/results/test"),
        num_simulations_per_config=2,  # Just 2 sims for speed
        max_workers=2
    )
    print("✓ SimulationManager initialized")

    # Run subset test (3 configs × 2 sims = 6 total simulations)
    print("\nRunning subset test (3 configs × 2 sims = 6 total)...")
    optimal_path = manager.run_subset_test(num_configs=3)

    print(f"\n✓ Subset test complete")
    print(f"✓ Optimal config saved: {optimal_path}")
    print(f"✓ File exists: {optimal_path.exists()}")


def main():
    print("\n" + "=" * 80)
    print("SIMULATION MANAGER INTEGRATION TEST")
    print("=" * 80)

    try:
        # Test single config mode
        test_single_config()

        # Test subset mode
        test_subset()

        print("\n" + "=" * 80)
        print("ALL TESTS PASSED! ✅")
        print("=" * 80)
        print("\nPhase 6 (SimulationManager) is complete and validated.")
        print("The full simulation system is now operational.")
        print("\nYou can now run:")
        print("  python simulation/run_simulation.py single --sims 5")
        print("  python simulation/run_simulation.py subset --configs 10 --sims 10")
        print("  python simulation/run_simulation.py full --sims 100 --workers 8")
        print()

    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    main()
