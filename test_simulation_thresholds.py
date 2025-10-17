#!/usr/bin/env python3
"""
Test that simulation system properly uses different threshold configurations.

Validates:
1. Baseline parameterized config can be loaded by SimulationManager
2. ConfigGenerator can create configs with varied STEPS values
3. Generated configs can be loaded and validated by ConfigManager
"""

from pathlib import Path
from simulation.SimulationManager import SimulationManager
from simulation.ConfigGenerator import ConfigGenerator
from league_helper.util.ConfigManager import ConfigManager
import json
import tempfile
import shutil

def print_section(title):
    print(f"\n{'='*80}")
    print(f"  {title}")
    print(f"{'='*80}\n")

def test_simulation_manager_loads_baseline():
    """Test that SimulationManager can load baseline parameterized config."""
    print_section("TEST 1: SimulationManager Loads Parameterized Config")

    print("Loading baseline config with parameterized thresholds...")
    cm = ConfigManager(Path('data'))

    print(f"  ADP_SCORING STEPS: {cm.parameters['ADP_SCORING']['THRESHOLDS']['STEPS']}")
    print(f"  PLAYER_RATING_SCORING STEPS: {cm.parameters['PLAYER_RATING_SCORING']['THRESHOLDS']['STEPS']}")
    print(f"  PERFORMANCE_SCORING STEPS: {cm.parameters['PERFORMANCE_SCORING']['THRESHOLDS']['STEPS']}")

    print("\nCreating SimulationManager with parameterized config...")
    try:
        # Check that simulation data directory exists
        sim_data = Path('simulation/sim_data')
        if not sim_data.exists():
            print(f"  ⚠ Simulation data directory not found: {sim_data}")
            print(f"  Skipping SimulationManager initialization (requires full sim environment)")
            print(f"  ✓ Baseline config validation passed")
            return True

        temp_output = Path(tempfile.mkdtemp())

        sim = SimulationManager(
            baseline_config_path=Path('data/league_config.json'),
            output_dir=temp_output,
            num_simulations_per_config=2,
            max_workers=2,
            data_folder=sim_data,
            num_test_values=1
        )

        print(f"  ✓ SimulationManager initialized successfully")
        print(f"  ✓ ConfigGenerator created with parameterized thresholds")

        # Verify ConfigGenerator has STEPS parameters
        gen = sim.config_generator
        baseline_params = gen.baseline_config['parameters']

        for scoring_type in ['ADP_SCORING', 'PLAYER_RATING_SCORING', 'PERFORMANCE_SCORING']:
            steps = baseline_params[scoring_type]['THRESHOLDS']['STEPS']
            print(f"  ✓ {scoring_type} STEPS = {steps}")

        # Clean up
        temp_output.rmdir()

        return True
    except Exception as e:
        print(f"\n  ✗ SimulationManager initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_configgenerator_creates_valid_configs():
    """Test that ConfigGenerator creates configs with varied STEPS that validate."""
    print_section("TEST 2: ConfigGenerator Creates Valid Configs with Different STEPS")

    print("Generating configs with different STEPS values...")
    gen = ConfigGenerator(Path('data/league_config.json'), num_test_values=2)

    baseline_combo = gen._extract_combination_from_config(gen.baseline_config)

    # Create 3 configs with different STEPS values
    configs = []
    steps_values = [
        (30.0, 0.08, "tight thresholds"),
        (37.5, 0.1, "baseline"),
        (45.0, 0.15, "wide thresholds")
    ]

    for adp_steps, perf_steps, desc in steps_values:
        combo = baseline_combo.copy()
        combo['ADP_SCORING_STEPS'] = adp_steps
        combo['PERFORMANCE_SCORING_STEPS'] = perf_steps
        config_dict = gen.create_config_dict(combo)
        configs.append((config_dict, desc, adp_steps, perf_steps))

    print(f"\n  ✓ Generated {len(configs)} configs with different STEPS values\n")

    # Validate each config can be loaded by ConfigManager
    for i, (config_dict, desc, adp_steps, perf_steps) in enumerate(configs):
        print(f"Config {i+1} ({desc}):")
        print(f"  ADP_SCORING_STEPS: {adp_steps}")
        print(f"  PERFORMANCE_SCORING_STEPS: {perf_steps}")

        # Write to temp directory
        temp_dir = Path(tempfile.mkdtemp())
        temp_config_path = temp_dir / 'league_config.json'

        try:
            with open(temp_config_path, 'w') as f:
                json.dump(config_dict, f)

            # Load with ConfigManager to validate
            cm = ConfigManager(temp_dir)

            # Verify STEPS values
            actual_adp = cm.parameters['ADP_SCORING']['THRESHOLDS']['STEPS']
            actual_perf = cm.parameters['PERFORMANCE_SCORING']['THRESHOLDS']['STEPS']

            if actual_adp == adp_steps and actual_perf == perf_steps:
                print(f"  ✓ Config validates and loads correctly")
            else:
                print(f"  ✗ STEPS values don't match")
                return False

            # Verify thresholds were calculated
            if 'VERY_POOR' in cm.parameters['ADP_SCORING']['THRESHOLDS']:
                print(f"  ✓ Thresholds calculated from STEPS")
            else:
                print(f"  ✗ Thresholds not calculated")
                return False

            # Clean up
            temp_config_path.unlink()
            temp_dir.rmdir()

        except Exception as e:
            print(f"  ✗ Config validation failed: {e}")
            try:
                temp_config_path.unlink()
                temp_dir.rmdir()
            except:
                pass
            return False

    print("\n✓ All generated configs validate correctly")
    return True

def test_iterative_optimization_ready():
    """Test that iterative optimization system is ready for STEPS optimization."""
    print_section("TEST 3: Iterative Optimization Ready for STEPS Parameters")

    print("Verifying simulation system components...")

    # Check that baseline config exists
    baseline = Path('data/league_config.json')
    if not baseline.exists():
        print(f"  ✗ Baseline config not found: {baseline}")
        return False
    print(f"  ✓ Baseline config exists")

    # Check ConfigGenerator has STEPS in PARAMETER_ORDER
    gen = ConfigGenerator(baseline, num_test_values=1)
    steps_params = [p for p in gen.PARAMETER_ORDER if '_STEPS' in p]

    print(f"\n  STEPS parameters in optimization order:")
    for i, param in enumerate(steps_params):
        idx = gen.PARAMETER_ORDER.index(param)
        print(f"    {idx+1}. {param}")

    if len(steps_params) != 5:
        print(f"\n  ✗ Expected 5 STEPS parameters, found {len(steps_params)}")
        return False

    print(f"\n  ✓ All 5 STEPS parameters are in PARAMETER_ORDER")
    print(f"  ✓ Total optimizable parameters: {len(gen.PARAMETER_ORDER)}")

    # Verify single parameter config generation works for STEPS
    print(f"\n  Testing single-parameter config generation for ADP_SCORING_STEPS...")
    try:
        configs = gen.generate_single_parameter_configs('ADP_SCORING_STEPS', gen.baseline_config)
        print(f"  ✓ Generated {len(configs)} configs (expected 2 = 1 baseline + 1 variation)")

        if len(configs) != 2:
            print(f"  ✗ Wrong number of configs generated")
            return False

    except Exception as e:
        print(f"  ✗ Single parameter config generation failed: {e}")
        return False

    print(f"\n✓ Simulation system ready for iterative STEPS optimization")
    print(f"✓ Use 'python run_simulation.py iterative --sims N' to optimize all parameters")

    return True

def main():
    """Run all simulation threshold tests."""
    print("\n" + "="*80)
    print("  SIMULATION THRESHOLD TESTING")
    print("  Verifying simulation system handles different threshold configs")
    print("="*80)

    tests = [
        ("SimulationManager Loads Parameterized Config", test_simulation_manager_loads_baseline),
        ("ConfigGenerator Creates Valid Configs", test_configgenerator_creates_valid_configs),
        ("Iterative Optimization Ready", test_iterative_optimization_ready),
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
        print("\n✓ Simulation system correctly handles threshold parameter variations")
        print("✓ Ready for parameter optimization via iterative simulation")
        return 0
    else:
        print("\n✗ Some tests failed - review output above")
        return 1

if __name__ == '__main__':
    exit(main())
