"""
User Test Script: fix_2025_adp Epic (Full CSV - All Players)

Tests the complete epic end-to-end with the full FantasyPros CSV (988 players).
This is the MANDATORY user testing step from Stage 7.
"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

import json
from utils.adp_csv_loader import load_adp_from_csv
from utils.adp_updater import update_player_adp_values

print("=" * 80)
print("USER TEST: fix_2025_adp Epic (Full CSV - All Players)")
print("=" * 80)
print()

# =============================================================================
# STEP 1: Load Full FantasyPros CSV (Feature 1)
# =============================================================================
print("STEP 1: Loading FantasyPros CSV...")
print("-" * 80)

csv_path = Path('feature-updates/FantasyPros_2025_Overall_ADP_Rankings.csv')

try:
    adp_df = load_adp_from_csv(csv_path)
    print(f"✅ SUCCESS: Loaded {len(adp_df)} players from CSV")
    print(f"   Columns: {list(adp_df.columns)}")
    print(f"   Positions: {sorted(adp_df['position'].unique())}")
    print(f"   ADP range: {adp_df['adp'].min():.1f} - {adp_df['adp'].max():.1f}")
    print()
except Exception as e:
    print(f"❌ FAILED: Could not load CSV")
    print(f"   Error: {e}")
    sys.exit(1)

# =============================================================================
# STEP 2: Update Player Data (Feature 2)
# =============================================================================
print("STEP 2: Matching players and updating ADP values across all weeks...")
print("-" * 80)

sim_data_folder = Path('simulation/sim_data/2025/weeks')

try:
    report = update_player_adp_values(adp_df, sim_data_folder)
    print(f"✅ SUCCESS: Player matching complete (all 18 weeks processed)")
    print()
except Exception as e:
    print(f"❌ FAILED: Could not update player data")
    print(f"   Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# =============================================================================
# STEP 3: Display Match Report
# =============================================================================
print("STEP 3: Match Report")
print("-" * 80)

summary = report['summary']
print(f"Total JSON Players: {summary['total_json_players']}")
print(f"Matched:            {summary['matched']} ({summary['matched']/summary['total_json_players']*100:.1f}%)")
print(f"Unmatched JSON:     {summary['unmatched_json']}")
print(f"Unmatched CSV:      {summary['unmatched_csv']}")
print()

print("Confidence Distribution:")
for range_key, count in report['confidence_distribution'].items():
    print(f"  {range_key}: {count} players")
print()

# Show sample of high-confidence matches
if report['individual_matches']:
    print("Sample Matches (first 10):")
    for i, match in enumerate(report['individual_matches'][:10]):
        print(f"  {i+1}. {match['json_name']} -> {match['csv_name']} "
              f"(ADP: {match['adp']}, Confidence: {match['confidence']:.2f})")
    print()

# Show unmatched JSON players (if any)
if report['unmatched_json_players']:
    print(f"Unmatched JSON Players ({len(report['unmatched_json_players'])} total):")
    for i, player in enumerate(report['unmatched_json_players'][:10]):
        print(f"  {i+1}. {player['name']} ({player['position']}) - Kept default ADP 170.0")
    if len(report['unmatched_json_players']) > 10:
        print(f"  ... and {len(report['unmatched_json_players']) - 10} more")
    print()

# Show unmatched CSV players (if any)
if report['unmatched_csv_players']:
    print(f"Unmatched CSV Players ({len(report['unmatched_csv_players'])} total):")
    for i, player in enumerate(report['unmatched_csv_players'][:10]):
        print(f"  {i+1}. {player['player_name']} ({player['position']}, ADP: {player['adp']})")
    if len(report['unmatched_csv_players']) > 10:
        print(f"  ... and {len(report['unmatched_csv_players']) - 10} more")
    print()

# =============================================================================
# STEP 4: Verify JSON Files Updated (Sample from week_01)
# =============================================================================
print("STEP 4: Verifying JSON files updated correctly (sampling week_01)...")
print("-" * 80)

json_files = ['qb_data.json', 'rb_data.json', 'wr_data.json',
              'te_data.json', 'k_data.json', 'dst_data.json']

week_01_folder = Path('simulation/sim_data/2025/weeks/week_01')
total_updated = 0
for pos_file in json_files:
    json_path = week_01_folder / pos_file
    with open(json_path, 'r', encoding='utf-8') as f:
        players = json.load(f)  # Direct array, no wrapper dict

    # Count how many have non-default ADP
    updated = sum(1 for p in players if p.get('average_draft_position', 170.0) != 170.0)
    total = len(players)

    print(f"  {pos_file:20s}: {updated:3d}/{total:3d} players updated ({updated/total*100:5.1f}%)")
    total_updated += updated

print()
print(f"Total players with updated ADP (week_01): {total_updated}/{summary['total_json_players'] // 18}")
print(f"Note: Aggregated across all 18 weeks = {summary['matched']} matched players")
print()

# =============================================================================
# STEP 5: Sample Verification (Check Actual Values)
# =============================================================================
print("STEP 5: Sample Verification (Checking actual ADP values from week_01)...")
print("-" * 80)

# Load QB data from week_01 and check some well-known players
qb_path = Path('simulation/sim_data/2025/weeks/week_01/qb_data.json')
with open(qb_path, 'r', encoding='utf-8') as f:
    qb_data = json.load(f)  # Direct array, no wrapper dict

sample_players = ['Patrick Mahomes', 'Josh Allen', 'Jalen Hurts', 'Lamar Jackson', 'Joe Burrow']
print("Sample QB ADP values:")
for qb in qb_data:  # Direct array iteration
    if qb['name'] in sample_players:
        adp = qb.get('average_draft_position', 170.0)
        status = "✅ Updated" if adp != 170.0 else "⚠️ Default"
        print(f"  {qb['name']:20s}: ADP = {adp:6.1f}  {status}")

print()

# =============================================================================
# FINAL RESULT
# =============================================================================
print("=" * 80)
print("USER TEST COMPLETE")
print("=" * 80)
print()

# Calculate success metrics
match_rate = summary['matched'] / summary['total_json_players'] * 100
update_rate = total_updated / summary['total_json_players'] * 100

print("Summary:")
print(f"  ✅ CSV loaded successfully ({len(adp_df)} players)")
print(f"  ✅ Player matching complete ({match_rate:.1f}% match rate)")
print(f"  ✅ JSON files updated ({update_rate:.1f}% updated)")
print(f"  ✅ No errors or crashes")
print()

if match_rate >= 85.0:
    print("🎯 SUCCESS: Match rate >= 85% (epic success criterion met)")
else:
    print(f"⚠️ WARNING: Match rate {match_rate:.1f}% is below 85% target")

print()
print("Review the output above. If everything looks correct:")
print("  ✅ Report to Claude: 'Testing passed - proceed with commit'")
print()
print("If you found any bugs or unexpected behavior:")
print("  ❌ Report to Claude: 'Bug found: [description]'")
print()
