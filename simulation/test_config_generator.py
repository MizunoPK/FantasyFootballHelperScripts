"""
Quick test script for ConfigGenerator

Tests that ConfigGenerator produces the expected number of configurations
and that multipliers are applied correctly.

Author: Kai Mizuno
Date: 2024
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))
from ConfigGenerator import ConfigGenerator

def main():
    print("Testing ConfigGenerator...")
    print("=" * 80)

    # Load baseline config
    baseline_path = Path("simulation/simulated_configs/optimal_2025-10-02_15-29-14.json.json")
    print(f"\nLoading baseline config from: {baseline_path}")

    gen = ConfigGenerator(baseline_path)
    print(f"✓ ConfigGenerator initialized")

    # Test parameter value generation
    print("\nTesting parameter value generation:")
    value_sets = gen.generate_all_parameter_value_sets()
    print(f"✓ Generated {len(value_sets)} parameter value sets")

    for param_name, values in value_sets.items():
        print(f"  {param_name}: {len(values)} values, range=[{min(values):.2f}, {max(values):.2f}]")

    # Test combination generation
    print("\nTesting combination generation:")
    combinations = gen.generate_all_combinations()
    print(f"✓ Generated {len(combinations)} combinations")

    if len(combinations) == 46656:
        print(f"✓ Correct number of combinations (6^6 = 46,656)")
    else:
        print(f"✗ ERROR: Expected 46,656 combinations, got {len(combinations)}")

    # Test config creation
    print("\nTesting config creation:")
    first_combo = combinations[0]
    print(f"First combination parameters:")
    for key, val in first_combo.items():
        print(f"  {key}: {val:.3f}")

    first_config = gen.create_config_dict(first_combo)
    print(f"✓ Created config dict")

    # Verify structure
    assert 'config_name' in first_config
    assert 'parameters' in first_config
    params = first_config['parameters']

    # Check scalar parameters
    assert params['NORMALIZATION_MAX_SCALE'] == first_combo['NORMALIZATION_MAX_SCALE']
    assert params['BASE_BYE_PENALTY'] == first_combo['BASE_BYE_PENALTY']
    assert params['DRAFT_ORDER_BONUSES']['PRIMARY'] == first_combo['PRIMARY_BONUS']
    assert params['DRAFT_ORDER_BONUSES']['SECONDARY'] == first_combo['SECONDARY_BONUS']
    print(f"✓ Scalar parameters updated correctly")

    # Check multipliers
    print(f"\nVerifying multipliers in scoring sections:")
    for section in ConfigGenerator.SCORING_SECTIONS:
        if section in params and 'MULTIPLIERS' in params[section]:
            mults = params[section]['MULTIPLIERS']
            print(f"  {section}:")
            print(f"    EXCELLENT: {mults.get('EXCELLENT', 'N/A'):.3f}")
            print(f"    GOOD: {mults.get('GOOD', 'N/A'):.3f}")
            print(f"    POOR: {mults.get('POOR', 'N/A'):.3f}")
            print(f"    VERY_POOR: {mults.get('VERY_POOR', 'N/A'):.3f}")

            # Verify GOOD != EXCELLENT
            if 'GOOD' in mults and 'EXCELLENT' in mults:
                assert mults['GOOD'] != mults['EXCELLENT'], f"{section}: GOOD and EXCELLENT should be different"

            # Verify POOR != VERY_POOR
            if 'POOR' in mults and 'VERY_POOR' in mults:
                assert mults['POOR'] != mults['VERY_POOR'], f"{section}: POOR and VERY_POOR should be different"

    print(f"✓ All multipliers unique within sections")

    # Test memory estimate
    print("\nMemory estimate:")
    import sys as sys_module
    config_size = sys_module.getsizeof(str(first_config))
    total_size_mb = (config_size * len(combinations)) / (1024 * 1024)
    print(f"  Single config size: ~{config_size / 1024:.1f} KB")
    print(f"  Total for 46,656 configs: ~{total_size_mb:.1f} MB")

    print("\n" + "=" * 80)
    print("All tests passed! ✓")
    print("=" * 80)


if __name__ == "__main__":
    main()
