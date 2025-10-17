#!/usr/bin/env python3
"""
Test ConfigGenerator's ability to generate varied STEPS values for threshold parameters.

Validates:
1. generate_all_parameter_value_sets() creates STEPS value sets
2. Each STEPS parameter gets N+1 values (baseline + N variations)
3. Values respect min/max constraints from PARAM_DEFINITIONS
4. create_config_dict() correctly applies STEPS to generated configs
5. Generated configs have properly formatted threshold sections
"""

from pathlib import Path
from simulation.ConfigGenerator import ConfigGenerator
from league_helper.util.ConfigManager import ConfigManager
import json

def print_section(title):
    print(f"\n{'='*80}")
    print(f"  {title}")
    print(f"{'='*80}\n")

def test_parameter_definitions():
    """Test that STEPS parameters are defined in ConfigGenerator."""
    print_section("TEST 1: STEPS Parameter Definitions")

    gen = ConfigGenerator(Path('data/league_config.json'), num_test_values=3)

    steps_params = [
        'ADP_SCORING_STEPS',
        'PLAYER_RATING_SCORING_STEPS',
        'TEAM_QUALITY_SCORING_STEPS',
        'PERFORMANCE_SCORING_STEPS',
        'MATCHUP_SCORING_STEPS'
    ]

    print("Checking PARAM_DEFINITIONS for STEPS parameters:")
    for param in steps_params:
        if param in gen.param_definitions:
            range_val, min_val, max_val = gen.param_definitions[param]
            print(f"  ✓ {param}:")
            print(f"      range={range_val}, min={min_val}, max={max_val}")
        else:
            print(f"  ✗ {param}: NOT FOUND")
            return False

    print("\n✓ All 5 STEPS parameters are defined in PARAM_DEFINITIONS")
    return True

def test_parameter_order():
    """Test that STEPS parameters are in PARAMETER_ORDER."""
    print_section("TEST 2: STEPS in Parameter Order")

    gen = ConfigGenerator(Path('data/league_config.json'), num_test_values=3)

    steps_params = [
        'ADP_SCORING_STEPS',
        'PLAYER_RATING_SCORING_STEPS',
        'TEAM_QUALITY_SCORING_STEPS',
        'PERFORMANCE_SCORING_STEPS',
        'MATCHUP_SCORING_STEPS'
    ]

    print("Checking PARAMETER_ORDER for STEPS parameters:")
    for param in steps_params:
        if param in gen.PARAMETER_ORDER:
            idx = gen.PARAMETER_ORDER.index(param)
            print(f"  ✓ {param}: position {idx}")
        else:
            print(f"  ✗ {param}: NOT FOUND")
            return False

    print(f"\n✓ All 5 STEPS parameters are in PARAMETER_ORDER")
    print(f"✓ Total parameters: {len(gen.PARAMETER_ORDER)}")
    return True

def test_value_set_generation():
    """Test generate_all_parameter_value_sets creates STEPS value sets."""
    print_section("TEST 3: STEPS Value Set Generation")

    gen = ConfigGenerator(Path('data/league_config.json'), num_test_values=5)

    print("Generating parameter value sets with num_test_values=5...")
    value_sets = gen.generate_all_parameter_value_sets()

    steps_params = [
        'ADP_SCORING_STEPS',
        'PLAYER_RATING_SCORING_STEPS',
        'TEAM_QUALITY_SCORING_STEPS',
        'PERFORMANCE_SCORING_STEPS',
        'MATCHUP_SCORING_STEPS'
    ]

    print("\nGenerated STEPS value sets:")
    all_valid = True
    for param in steps_params:
        if param in value_sets:
            values = value_sets[param]
            print(f"\n  {param}:")
            print(f"    Values: {values}")
            print(f"    Count: {len(values)} (expected 6 = 1 baseline + 5 variations)")

            if len(values) != 6:
                print(f"    ✗ INCORRECT COUNT")
                all_valid = False
            else:
                # Check min/max constraints
                range_val, min_val, max_val = gen.param_definitions[param]
                if any(v < min_val or v > max_val for v in values):
                    print(f"    ✗ VALUES OUT OF RANGE [{min_val}, {max_val}]")
                    all_valid = False
                else:
                    print(f"    ✓ All values within range [{min_val}, {max_val}]")
        else:
            print(f"\n  {param}: ✗ NOT FOUND")
            all_valid = False

    if all_valid:
        print("\n✓ All STEPS value sets generated correctly")
    return all_valid

def test_config_creation():
    """Test that create_config_dict correctly applies STEPS values."""
    print_section("TEST 4: Config Creation with STEPS")

    gen = ConfigGenerator(Path('data/league_config.json'), num_test_values=3)

    # Create a test combination with modified STEPS values
    baseline_combination = gen._extract_combination_from_config(gen.baseline_config)

    # Modify STEPS values
    test_combination = baseline_combination.copy()
    test_combination['ADP_SCORING_STEPS'] = 50.0  # Changed from 37.5
    test_combination['PLAYER_RATING_SCORING_STEPS'] = 25.0  # Changed from 20
    test_combination['TEAM_QUALITY_SCORING_STEPS'] = 8.0  # Changed from 6.25
    test_combination['PERFORMANCE_SCORING_STEPS'] = 0.15  # Changed from 0.1
    test_combination['MATCHUP_SCORING_STEPS'] = 10.0  # Changed from 7.5

    print("Creating config with modified STEPS values:")
    print(f"  ADP_SCORING_STEPS: 37.5 → 50.0")
    print(f"  PLAYER_RATING_SCORING_STEPS: 20 → 25.0")
    print(f"  TEAM_QUALITY_SCORING_STEPS: 6.25 → 8.0")
    print(f"  PERFORMANCE_SCORING_STEPS: 0.1 → 0.15")
    print(f"  MATCHUP_SCORING_STEPS: 7.5 → 10.0")

    config_dict = gen.create_config_dict(test_combination)

    print("\nVerifying generated config structure:")
    scoring_types = [
        ('ADP_SCORING', 50.0),
        ('PLAYER_RATING_SCORING', 25.0),
        ('TEAM_QUALITY_SCORING', 8.0),
        ('PERFORMANCE_SCORING', 0.15),
        ('MATCHUP_SCORING', 10.0)
    ]

    all_valid = True
    for scoring_type, expected_steps in scoring_types:
        thresholds = config_dict['parameters'][scoring_type]['THRESHOLDS']

        # Check parameterized format
        has_params = all(k in thresholds for k in ['BASE_POSITION', 'DIRECTION', 'STEPS'])
        if not has_params:
            print(f"  ✗ {scoring_type}: Missing parameterized threshold keys")
            all_valid = False
            continue

        actual_steps = thresholds['STEPS']
        if actual_steps == expected_steps:
            print(f"  ✓ {scoring_type}: STEPS = {actual_steps}")
        else:
            print(f"  ✗ {scoring_type}: STEPS = {actual_steps} (expected {expected_steps})")
            all_valid = False

    if all_valid:
        print("\n✓ All STEPS values correctly applied to config")
    return all_valid

def test_single_parameter_configs():
    """Test generate_single_parameter_configs for STEPS parameters."""
    print_section("TEST 5: Single Parameter Config Generation for STEPS")

    gen = ConfigGenerator(Path('data/league_config.json'), num_test_values=4)

    print("Generating single-parameter configs for ADP_SCORING_STEPS...")
    configs = gen.generate_single_parameter_configs('ADP_SCORING_STEPS', gen.baseline_config)

    print(f"\nGenerated {len(configs)} configs (expected 5 = 1 baseline + 4 variations)")

    if len(configs) != 5:
        print("✗ INCORRECT NUMBER OF CONFIGS")
        return False

    print("\nSTEPS values in generated configs:")
    for i, cfg in enumerate(configs):
        steps = cfg['parameters']['ADP_SCORING']['THRESHOLDS']['STEPS']
        print(f"  Config {i+1}: STEPS = {steps}")

    # Verify configs are valid and loadable
    print("\nVerifying configs can be loaded by ConfigManager:")
    for i, cfg in enumerate(configs):
        try:
            # Write to temp directory with correct filename
            import tempfile
            temp_dir = Path(tempfile.mkdtemp())
            temp_config_path = temp_dir / 'league_config.json'

            with open(temp_config_path, 'w') as f:
                json.dump(cfg, f)

            cm = ConfigManager(temp_dir)
            # If we get here, config loaded successfully
            print(f"  ✓ Config {i+1}: Loaded successfully (STEPS = {cm.parameters['ADP_SCORING']['THRESHOLDS']['STEPS']})")

            # Clean up
            temp_config_path.unlink()
            temp_dir.rmdir()
        except Exception as e:
            print(f"  ✗ Config {i+1}: Failed to load - {e}")
            return False

    print("\n✓ Single parameter configs generated correctly")
    return True

def test_fixed_threshold_params():
    """Test that BASE_POSITION and DIRECTION are correctly preserved."""
    print_section("TEST 6: Fixed Threshold Parameters")

    gen = ConfigGenerator(Path('data/league_config.json'), num_test_values=3)

    print("Verifying THRESHOLD_FIXED_PARAMS constant:")
    expected_configs = {
        "ADP_SCORING": {"BASE_POSITION": 0, "DIRECTION": "DECREASING"},
        "PLAYER_RATING_SCORING": {"BASE_POSITION": 0, "DIRECTION": "INCREASING"},
        "TEAM_QUALITY_SCORING": {"BASE_POSITION": 0, "DIRECTION": "DECREASING"},
        "PERFORMANCE_SCORING": {"BASE_POSITION": 0.0, "DIRECTION": "BI_EXCELLENT_HI"},
        "MATCHUP_SCORING": {"BASE_POSITION": 0, "DIRECTION": "BI_EXCELLENT_HI"}
    }

    all_valid = True
    for scoring_type, expected in expected_configs.items():
        if scoring_type in gen.THRESHOLD_FIXED_PARAMS:
            actual = gen.THRESHOLD_FIXED_PARAMS[scoring_type]
            if actual == expected:
                print(f"  ✓ {scoring_type}: {actual}")
            else:
                print(f"  ✗ {scoring_type}: {actual} (expected {expected})")
                all_valid = False
        else:
            print(f"  ✗ {scoring_type}: NOT FOUND")
            all_valid = False

    if all_valid:
        print("\n✓ All fixed threshold parameters are correct")

    # Test that generated configs preserve these values
    print("\nVerifying generated configs preserve BASE_POSITION and DIRECTION:")

    test_combination = gen._extract_combination_from_config(gen.baseline_config)
    test_combination['ADP_SCORING_STEPS'] = 50.0

    config_dict = gen.create_config_dict(test_combination)

    for scoring_type, expected in expected_configs.items():
        thresholds = config_dict['parameters'][scoring_type]['THRESHOLDS']
        actual_base = thresholds['BASE_POSITION']
        actual_dir = thresholds['DIRECTION']
        expected_base = expected['BASE_POSITION']
        expected_dir = expected['DIRECTION']

        if actual_base == expected_base and actual_dir == expected_dir:
            print(f"  ✓ {scoring_type}: BASE={actual_base}, DIR={actual_dir}")
        else:
            print(f"  ✗ {scoring_type}: BASE={actual_base}, DIR={actual_dir} "
                  f"(expected BASE={expected_base}, DIR={expected_dir})")
            all_valid = False

    if all_valid:
        print("\n✓ Generated configs preserve fixed threshold parameters")
    return all_valid

def main():
    """Run all ConfigGenerator STEPS tests."""
    print("\n" + "="*80)
    print("  CONFIGGENERATOR STEPS PARAMETER TESTING")
    print("  Verifying ConfigGenerator correctly handles threshold STEPS parameters")
    print("="*80)

    tests = [
        ("Parameter Definitions", test_parameter_definitions),
        ("Parameter Order", test_parameter_order),
        ("Value Set Generation", test_value_set_generation),
        ("Config Creation", test_config_creation),
        ("Single Parameter Configs", test_single_parameter_configs),
        ("Fixed Threshold Parameters", test_fixed_threshold_params),
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
        print("\n✓ ConfigGenerator correctly handles STEPS parameters")
        print("✓ Ready for simulation parameter optimization")
        return 0
    else:
        print("\n✗ Some tests failed - review output above")
        return 1

if __name__ == '__main__':
    exit(main())
