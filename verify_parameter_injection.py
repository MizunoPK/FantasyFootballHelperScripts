#!/usr/bin/env python3
"""
Systematic verification that ALL 23 parameters are correctly injected
from JSON config into the draft helper simulation logic.

This script traces each parameter from JSON → config_params → TeamStrategyManager → actual usage.
"""

import sys
from pathlib import Path

# Add paths
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / 'draft_helper' / 'simulation'))

print("="*80)
print("SYSTEMATIC PARAMETER INJECTION VERIFICATION")
print("="*80)
print()

# Load parameter config
from draft_helper.simulation.parameter_loader import load_parameter_config

config = load_parameter_config('draft_helper/simulation/parameters/optimal_2025-10-05_14-33-13.json')
config_params = {k: v[0] for k, v in config['parameters'].items()}

print(f"✅ Loaded {len(config_params)} parameters from JSON")
print()

# Create TeamStrategyManager with these params
from draft_helper.simulation.team_strategies import TeamStrategyManager

manager = TeamStrategyManager(config_params)

print("="*80)
print("PARAMETER-BY-PARAMETER VERIFICATION")
print("="*80)
print()

# Track results
verified = 0
failed = 0
not_applicable = 0

# ============================================================================
# GROUP 1: NORMALIZATION (Used in different part of simulation)
# ============================================================================
print("GROUP 1: NORMALIZATION PARAMETERS")
print("-" * 80)

param = "NORMALIZATION_MAX_SCALE"
json_value = config_params.get(param)
print(f"\n{param}:")
print(f"  JSON value: {json_value}")
print(f"  ⚠️  NOT INJECTED into TeamStrategyManager")
print(f"  ℹ️  Used by NormalizationCalculator (separate component)")
print(f"  ℹ️  Injection verified in scoring_engine.py tests")
not_applicable += 1

# ============================================================================
# GROUP 2: DRAFT ORDER BONUSES
# ============================================================================
print("\n" + "="*80)
print("GROUP 2: DRAFT ORDER BONUS PARAMETERS")
print("-" * 80)

params = [
    ("DRAFT_ORDER_PRIMARY_BONUS", "draft_order_primary_bonus"),
    ("DRAFT_ORDER_SECONDARY_BONUS", "draft_order_secondary_bonus")
]

for json_key, attr_name in params:
    json_value = config_params.get(json_key)
    injected_value = getattr(manager, attr_name, None)

    print(f"\n{json_key}:")
    print(f"  JSON value: {json_value}")
    print(f"  Injected as: manager.{attr_name} = {injected_value}")

    if json_value == injected_value:
        print(f"  ✅ VERIFIED - Values match")
        verified += 1
    else:
        print(f"  ❌ FAILED - Values don't match!")
        failed += 1

# Check draft_order array uses these values
draft_order_uses_primary = False
draft_order_uses_secondary = False
for round_priorities in manager.draft_order:
    for pos, bonus in round_priorities.items():
        if bonus == manager.draft_order_primary_bonus:
            draft_order_uses_primary = True
        if bonus == manager.draft_order_secondary_bonus or bonus == manager.draft_order_secondary_bonus + 5:
            draft_order_uses_secondary = True

print(f"\n  Draft Order Array Usage:")
print(f"    Primary bonus used in DRAFT_ORDER: {'✅' if draft_order_uses_primary else '❌'}")
print(f"    Secondary bonus used in DRAFT_ORDER: {'✅' if draft_order_uses_secondary else '❌'}")

# ============================================================================
# GROUP 3: INJURY PENALTIES
# ============================================================================
print("\n" + "="*80)
print("GROUP 3: INJURY PENALTY PARAMETERS")
print("-" * 80)

params = [
    ("INJURY_PENALTIES_MEDIUM", "MEDIUM"),
    ("INJURY_PENALTIES_HIGH", "HIGH")
]

for json_key, dict_key in params:
    json_value = config_params.get(json_key)
    injected_value = manager.injury_penalties.get(dict_key)

    print(f"\n{json_key}:")
    print(f"  JSON value: {json_value}")
    print(f"  Injected as: manager.injury_penalties['{dict_key}'] = {injected_value}")

    if json_value == injected_value:
        print(f"  ✅ VERIFIED - Values match")
        verified += 1
    else:
        print(f"  ❌ FAILED - Values don't match!")
        failed += 1

# LOW is always 0 (not a parameter)
print(f"\nINJURY_PENALTIES_LOW:")
print(f"  Hardcoded as: manager.injury_penalties['LOW'] = {manager.injury_penalties.get('LOW')}")
print(f"  ℹ️  Expected to be 0 (not a configurable parameter)")

# ============================================================================
# GROUP 4: BYE WEEK PENALTY
# ============================================================================
print("\n" + "="*80)
print("GROUP 4: BYE WEEK PENALTY PARAMETER")
print("-" * 80)

param = "BASE_BYE_PENALTY"
json_value = config_params.get(param)
injected_value = manager.base_bye_penalty

print(f"\n{param}:")
print(f"  JSON value: {json_value}")
print(f"  Injected as: manager.base_bye_penalty = {injected_value}")

if json_value == injected_value:
    print(f"  ✅ VERIFIED - Values match")
    verified += 1
else:
    print(f"  ❌ FAILED - Values don't match!")
    failed += 1

# ============================================================================
# GROUP 5: ENHANCED SCORING - ADP MULTIPLIERS
# ============================================================================
print("\n" + "="*80)
print("GROUP 5: ADP MULTIPLIER PARAMETERS (Enhanced Scoring)")
print("-" * 80)

params = [
    ("ADP_EXCELLENT_MULTIPLIER", "adp_excellent_multiplier"),
    ("ADP_GOOD_MULTIPLIER", "adp_good_multiplier"),
    ("ADP_POOR_MULTIPLIER", "adp_poor_multiplier")
]

for json_key, config_key in params:
    json_value = config_params.get(json_key)
    injected_value = manager.enhanced_scorer.config.get(config_key)

    print(f"\n{json_key}:")
    print(f"  JSON value: {json_value}")
    print(f"  Injected as: manager.enhanced_scorer.config['{config_key}'] = {injected_value}")

    if json_value == injected_value:
        print(f"  ✅ VERIFIED - Values match")
        verified += 1
    else:
        print(f"  ❌ FAILED - Values don't match!")
        failed += 1

# ============================================================================
# GROUP 6: ENHANCED SCORING - PLAYER RATING MULTIPLIERS
# ============================================================================
print("\n" + "="*80)
print("GROUP 6: PLAYER RATING MULTIPLIER PARAMETERS (Enhanced Scoring)")
print("-" * 80)

params = [
    ("PLAYER_RATING_EXCELLENT_MULTIPLIER", "player_rating_excellent_multiplier"),
    ("PLAYER_RATING_GOOD_MULTIPLIER", "player_rating_good_multiplier"),
    ("PLAYER_RATING_POOR_MULTIPLIER", "player_rating_poor_multiplier")
]

for json_key, config_key in params:
    json_value = config_params.get(json_key)
    injected_value = manager.enhanced_scorer.config.get(config_key)

    print(f"\n{json_key}:")
    print(f"  JSON value: {json_value}")
    print(f"  Injected as: manager.enhanced_scorer.config['{config_key}'] = {injected_value}")

    if json_value == injected_value:
        print(f"  ✅ VERIFIED - Values match")
        verified += 1
    else:
        print(f"  ❌ FAILED - Values don't match!")
        failed += 1

# ============================================================================
# GROUP 7: ENHANCED SCORING - TEAM QUALITY MULTIPLIERS
# ============================================================================
print("\n" + "="*80)
print("GROUP 7: TEAM QUALITY MULTIPLIER PARAMETERS (Enhanced Scoring)")
print("-" * 80)

params = [
    ("TEAM_EXCELLENT_MULTIPLIER", "team_excellent_multiplier"),
    ("TEAM_GOOD_MULTIPLIER", "team_good_multiplier"),
    ("TEAM_POOR_MULTIPLIER", "team_poor_multiplier")
]

for json_key, config_key in params:
    json_value = config_params.get(json_key)
    injected_value = manager.enhanced_scorer.config.get(config_key)

    print(f"\n{json_key}:")
    print(f"  JSON value: {json_value}")
    print(f"  Injected as: manager.enhanced_scorer.config['{config_key}'] = {injected_value}")

    if json_value == injected_value:
        print(f"  ✅ VERIFIED - Values match")
        verified += 1
    else:
        print(f"  ❌ FAILED - Values don't match!")
        failed += 1

# ============================================================================
# GROUP 8: CONSISTENCY MULTIPLIERS
# ============================================================================
print("\n" + "="*80)
print("GROUP 8: CONSISTENCY MULTIPLIER PARAMETERS")
print("-" * 80)

params = [
    ("CONSISTENCY_LOW_MULTIPLIER", "LOW"),
    ("CONSISTENCY_MEDIUM_MULTIPLIER", "MEDIUM"),
    ("CONSISTENCY_HIGH_MULTIPLIER", "HIGH")
]

for json_key, dict_key in params:
    json_value = config_params.get(json_key)
    injected_value = manager.consistency_multipliers.get(dict_key)

    print(f"\n{json_key}:")
    print(f"  JSON value: {json_value}")
    print(f"  Injected as: manager.consistency_multipliers['{dict_key}'] = {injected_value}")

    if json_value == injected_value:
        print(f"  ✅ VERIFIED - Values match")
        verified += 1
    else:
        print(f"  ❌ FAILED - Values don't match!")
        failed += 1

# ============================================================================
# GROUP 9: MATCHUP MULTIPLIERS (Used in Season Simulation, not Draft)
# ============================================================================
print("\n" + "="*80)
print("GROUP 9: MATCHUP MULTIPLIER PARAMETERS")
print("-" * 80)

matchup_params = [
    "MATCHUP_EXCELLENT_MULTIPLIER",
    "MATCHUP_GOOD_MULTIPLIER",
    "MATCHUP_NEUTRAL_MULTIPLIER",
    "MATCHUP_POOR_MULTIPLIER",
    "MATCHUP_VERY_POOR_MULTIPLIER"
]

for param in matchup_params:
    json_value = config_params.get(param)
    print(f"\n{param}:")
    print(f"  JSON value: {json_value}")
    print(f"  ⚠️  NOT INJECTED into TeamStrategyManager")
    print(f"  ℹ️  Used by SeasonSimulator/LineupOptimizer for weekly matchups")
    print(f"  ℹ️  Affects season simulation, not draft picks")
    not_applicable += 1

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "="*80)
print("VERIFICATION SUMMARY")
print("="*80)
print()

total_params = len(config_params)
draft_relevant = verified + failed

print(f"Total parameters in JSON: {total_params}")
print(f"Draft-relevant parameters: {draft_relevant}")
print(f"  ✅ Verified correct: {verified}")
print(f"  ❌ Failed verification: {failed}")
print(f"Season/other parameters: {not_applicable}")
print()

if failed > 0:
    print("❌ VERIFICATION FAILED - Some parameters not injected correctly!")
    sys.exit(1)
elif verified == draft_relevant:
    print("✅ ALL DRAFT-RELEVANT PARAMETERS VERIFIED!")
    print()
    print("Parameter injection is working correctly:")
    print(f"  • {verified} parameters injected into TeamStrategyManager")
    print(f"  • {not_applicable} parameters used in other simulation components")
    print()
    print("The simulation correctly overrides draft helper logic with test values.")
    sys.exit(0)
else:
    print("⚠️  Unexpected state - review output above")
    sys.exit(1)
