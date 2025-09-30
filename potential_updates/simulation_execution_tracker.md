# Simulation Execution Tracker

**Purpose**: Working document to track simulation runs, results, and next steps
**Created**: 2025-09-30
**Last Updated**: 2025-09-30
**Status**: Ready for Phase 1

---

## Quick Reference

**Current Phase**: Phase 0 (Baseline & Setup)
**Next Phase**: Phase 1 (Core Scoring Foundation)
**Completion**: 0% (0 of 6 phases complete)

**Reference Documentation**:
- Full optimization strategy: `simulation_optimization_strategy.md`
- Current simulation config: `draft_helper/simulation/config.py`

---

## Phase Status Overview

| Phase | Parameters | Configs | Status | Start Date | Complete Date | Winner Config |
|-------|-----------|---------|--------|------------|---------------|---------------|
| **Phase 1** | Normalization + Draft Order | 27 | ⏳ Pending | - | - | - |
| **Phase 2a** | ADP Adjustments | 27 | ⏳ Pending | - | - | - |
| **Phase 2b** | Player Rating | 27 | ⏳ Pending | - | - | - |
| **Phase 2c** | Team Quality | 27 | ⏳ Pending | - | - | - |
| **Phase 3** | Matchup Multipliers | 243 | ⏳ Pending | - | - | - |
| **Phase 4** | Injury & Bye | 27 | ⏳ Pending | - | - | - |
| **Phase 5** | Validation | 10-15 | ⏳ Pending | - | - | - |
| **Phase 6** | Final Verification | 1 | ⏳ Pending | - | - | - |

**Legend**: ⏳ Pending | 🔄 In Progress | ✅ Complete | ❌ Failed | ⏭️ Skipped

---

## Current Phase: Phase 1 - Core Scoring Foundation

### Objectives
1. Test 27 combinations of normalization scale and draft order bonuses
2. Establish optimal balance between scale and position bonuses
3. Establish foundation for remaining phases
4. Verify simulation infrastructure is working with 3-value testing

### Configuration

**Run ID**: `phase1_core_scoring`
**Date Started**: [NOT STARTED]
**Simulations**: 20 per configuration (using `SIMULATIONS_PER_CONFIG`)
**Total Configurations**: 27 (3^3 combinations)

**Parameters Under Test** (3 parameters with 3 values each):
```python
{
    # UNDER TEST (3 values each = 27 combinations)
    'NORMALIZATION_MAX_SCALE': [100, 110, 120],
    'DRAFT_ORDER_PRIMARY_BONUS': [50, 55, 60],
    'DRAFT_ORDER_SECONDARY_BONUS': [25, 27, 30],

    # FIXED AT BASELINE (middle value)
    'MATCHUP_EXCELLENT_MULTIPLIER': 1.20,
    'MATCHUP_GOOD_MULTIPLIER': 1.10,
    'MATCHUP_NEUTRAL_MULTIPLIER': 1.00,
    'MATCHUP_POOR_MULTIPLIER': 0.90,
    'MATCHUP_VERY_POOR_MULTIPLIER': 0.80,
    'INJURY_PENALTIES_MEDIUM': 15.0,
    'INJURY_PENALTIES_HIGH': 30.0,
    'BASE_BYE_PENALTY': 10.0,
    'ADP_EXCELLENT_MULTIPLIER': 1.15,
    'ADP_GOOD_MULTIPLIER': 1.08,
    'ADP_POOR_MULTIPLIER': 0.90,
    'PLAYER_RATING_EXCELLENT_MULTIPLIER': 1.20,
    'PLAYER_RATING_GOOD_MULTIPLIER': 1.10,
    'PLAYER_RATING_POOR_MULTIPLIER': 0.90,
    'TEAM_EXCELLENT_MULTIPLIER': 1.12,
    'TEAM_GOOD_MULTIPLIER': 1.06,
    'TEAM_POOR_MULTIPLIER': 0.94,
}
```

### How to Execute

```bash
# Run Phase 1 simulation with JSON configuration
python run_simulation.py draft_helper/simulation/parameters/phase1_core_scoring.json

# This will test all 27 combinations (3^3) automatically
# Results will be saved to: draft_helper/simulation/results/result_YYYY-MM-DD_HH-MM-SS.md
```

### Expected Runtime
- **Per configuration**: 20 simulations × 10-15 min = 3.3-5 hours
- **Total for 27 configs**: 27 × 3.5 hours = ~95 hours (~4 days)
- **With parallel execution (4-way)**: ~24 hours (~1 day)
- **Recommended**: Use parallel execution or run over weekend

### Results to Capture

**Primary Metrics** (from results CSV):
- Mean win rate (target baseline: ~50%)
- Mean championship rate (target: ~10%)
- Mean playoff rate (target: ~60%)
- Standard deviation of win rate

**Success Criteria**:
- ✅ All 20 simulations complete without errors
- ✅ Results logged to CSV and JSON
- ✅ Mean win rate between 45-55% (reasonable baseline)
- ✅ No crashes or data corruption

### Results

**Status**: ⏳ NOT STARTED

**Execution Log**:
```
[Log entries will be added here as simulation runs]
```

**Performance Summary**:
```
[Summary statistics will be added here after completion]

Example format:
Win Rate: 0.5123 ± 0.0234 (mean ± std)
Championship Rate: 0.0950 ± 0.0156
Playoff Rate: 0.6050 ± 0.0312
Points For: 1523.4 ± 45.6
```

**Files Generated**:
- [ ] `baseline_001_results.csv`
- [ ] `baseline_001_summary.json`
- [ ] `baseline_001_logs.txt`

### Notes & Observations

```
[Add any observations, issues, or insights here]

Example:
- Simulation took longer than expected (7 hours vs 5 hours)
- Week 12 matchups showed unusual variance
- Team strategy #3 (positional) performed best in baseline
```

### Blockers & Issues

```
[Track any problems encountered]

Example:
- Issue: Simulation crashed at week 15 on sim #8
  Status: RESOLVED
  Solution: Fixed null pointer in matchup calculator
  Date: 2025-09-30
```

---

## Next Phase: Phase 2a - ADP Adjustments

### Objectives
1. Test 27 combinations of ADP multipliers
2. Find optimal ADP impact level
3. Determine if following market consensus improves results

### Configuration Matrix

**Parameters Under Test** (3 parameters with 3 values each = 27 combinations):
- `ADP_EXCELLENT_MULTIPLIER`: [1.15, 1.175, 1.20]
- `ADP_GOOD_MULTIPLIER`: [1.08, 1.09, 1.10]
- `ADP_POOR_MULTIPLIER`: [0.85, 0.90, 0.95]

**All Other Parameters**: Fixed at Phase 1 winners + baseline values

### Execution Plan

**Recommended Order**: Run configurations sequentially or in parallel if resources allow

**Option 1: Sequential** (safer, easier to monitor)
```bash
# Run each config one at a time
for config_id in p1_001 p1_002 p1_003 p1_004 p1_005 p1_006 p1_007 p1_008; do
    echo "Running $config_id..."
    python run_simulation.py --config $config_id --sims 20
    echo "$config_id complete"
done
```

**Option 2: Parallel** (faster, requires more resources)
```bash
# Run 4 configs in parallel (adjust based on CPU cores)
parallel -j 4 python run_simulation.py --config {} --sims 20 ::: \
    p1_001 p1_002 p1_003 p1_004 p1_005 p1_006 p1_007 p1_008
```

### Expected Runtime
- **Per config**: 3.3-5 hours (20 sims × 10-15 min)
- **Total sequential**: 26-40 hours
- **Total parallel (4-way)**: 6.5-10 hours

### Analysis Plan

After all 8 configs complete:

**Step 1: Load and merge results**
```python
import pandas as pd
import glob

# Load all Phase 1 results
phase1_files = glob.glob('results/p1_*_results.csv')
df = pd.concat([pd.read_csv(f) for f in phase1_files])

# Group by configuration
summary = df.groupby('config_id').agg({
    'win_rate': ['mean', 'std'],
    'championship': 'mean',
    'playoff': 'mean',
    'points_for': 'mean'
})

print(summary.sort_values(('win_rate', 'mean'), ascending=False))
```

**Step 2: Statistical testing**
```python
from scipy import stats

# ANOVA: Are configs significantly different?
groups = [df[df['config_id'] == c]['win_rate'].values
          for c in df['config_id'].unique()]
f_stat, p_value = stats.f_oneway(*groups)
print(f"ANOVA: F={f_stat:.4f}, p={p_value:.4f}")

# If significant, find which configs differ
# (Use pairwise t-tests with Bonferroni correction)
```

**Step 3: Visualize results**
```python
import matplotlib.pyplot as plt

# Box plot of win rates
df.boxplot(column='win_rate', by='config_id', figsize=(12, 6))
plt.title('Phase 1: Win Rate by Configuration')
plt.savefig('results/phase1_boxplot.png')
```

**Step 4: Identify winner**
```python
# Winner = highest mean win rate with acceptable variance
winner = summary['win_rate']['mean'].idxmax()
print(f"Phase 1 Winner: {winner}")

# Extract winning parameter values
# Use these as baseline for Phase 2
```

### Success Criteria

- [ ] All 8 configurations complete successfully
- [ ] ANOVA shows significant difference (p < 0.05)
- [ ] Winner has effect size > 0.3 vs baseline
- [ ] Results documented and winner identified
- [ ] Winning config tested for reproducibility (optional: 5 extra sims)

### Results

**Status**: ⏳ NOT STARTED

**Execution Timeline**:
```
Start Date: [TO BE FILLED]
Config p1_001: [Status] - Started: [Date/Time] - Completed: [Date/Time]
Config p1_002: [Status] - Started: [Date/Time] - Completed: [Date/Time]
Config p1_003: [Status] - Started: [Date/Time] - Completed: [Date/Time]
Config p1_004: [Status] - Started: [Date/Time] - Completed: [Date/Time]
Config p1_005: [Status] - Started: [Date/Time] - Completed: [Date/Time]
Config p1_006: [Status] - Started: [Date/Time] - Completed: [Date/Time]
Config p1_007: [Status] - Started: [Date/Time] - Completed: [Date/Time]
Config p1_008: [Status] - Started: [Date/Time] - Completed: [Date/Time]
End Date: [TO BE FILLED]
```

**Performance Summary**:
```
[To be filled after analysis]

Example format:
Winner: p1_008 (NORM_SCALE=120, PRIMARY=60, SECONDARY=30)
Win Rate: 0.5345 ± 0.0198 (vs baseline: 0.5123)
Improvement: +4.3% (p=0.023, Cohen's d=0.42)
Championship Rate: 0.1050 ± 0.0145
Playoff Rate: 0.6450 ± 0.0289

Runner-up: p1_007 (NORM_SCALE=120, PRIMARY=60, SECONDARY=25)
Win Rate: 0.5312 ± 0.0203
Improvement: +3.7% (p=0.045, Cohen's d=0.38)
```

**Statistical Tests**:
```
[To be filled after analysis]

ANOVA Results:
  F-statistic: 3.456
  P-value: 0.012
  Conclusion: Configurations significantly different

Pairwise Comparisons (top 3 vs baseline):
  p1_008 vs baseline: t=2.34, p=0.023, d=0.42 ✅ Significant
  p1_007 vs baseline: t=2.01, p=0.045, d=0.38 ✅ Significant
  p1_004 vs baseline: t=1.67, p=0.098, d=0.31 ❌ Not significant
```

**Key Insights**:
```
[To be filled after analysis]

Example:
1. Higher NORMALIZATION_MAX_SCALE (120) consistently outperformed baseline (100)
2. Both bonus increases (60/30) showed benefit, with primary bonus having larger effect
3. All-aggressive config (p1_008) won, but p1_007 was close (lower secondary bonus)
4. Interaction effect: Scale increase amplifies bonus value
5. Variance was slightly higher with aggressive settings (0.020 vs 0.023)
```

**Winning Configuration**:
```python
# Phase 1 Winner: p1_008
PHASE1_WINNER = {
    'NORMALIZATION_MAX_SCALE': 120,
    'DRAFT_ORDER_PRIMARY_BONUS': 60,
    'DRAFT_ORDER_SECONDARY_BONUS': 30,
}

# Use this as baseline for Phase 2a
```

**Files Generated**:
- [ ] `p1_001_results.csv` through `p1_008_results.csv`
- [ ] `p1_*_summary.json` (8 files)
- [ ] `phase1_combined_results.csv`
- [ ] `phase1_analysis_report.md`
- [ ] `phase1_visualizations.png`

### Decisions & Next Steps

```
[To be filled after analysis]

Decisions Made:
- ✅ Selected p1_008 as winner (highest win rate, statistically significant)
- ✅ Will use NORM_SCALE=120, PRIMARY=60, SECONDARY=30 for all future phases
- ⏭️ Skipping boundary testing (120 is max in range, confident in choice)

Next Steps:
- [ ] Update Phase 2a configuration with Phase 1 winners
- [ ] Prepare 8 configs for Phase 2a (ADP adjustments)
- [ ] Schedule Phase 2a execution for [Date]

Open Questions:
- Should we test NORM_SCALE=130 or 140? (Outside current range)
- Is variance increase (0.023 vs 0.020) concerning? (Likely acceptable)
```

---

## Phase 2a: ADP Adjustments

### Status
**Current Status**: ⏳ BLOCKED - Waiting for Phase 1 completion
**Prerequisites**: Phase 1 winner identified

### Objectives
1. Test 8 combinations of ADP multipliers
2. Find optimal ADP impact level
3. Determine if following market consensus improves results

### Configuration Matrix

| Config | ADP_EXCELLENT | ADP_GOOD | ADP_POOR | Description |
|--------|---------------|----------|----------|-------------|
| **p2a_001** | 1.15 | 1.08 | 0.90 | All baseline |
| **p2a_002** | 1.15 | 1.08 | 0.95 | -Poor penalty |
| **p2a_003** | 1.15 | 1.10 | 0.90 | +Good boost |
| **p2a_004** | 1.15 | 1.10 | 0.95 | Good + poor |
| **p2a_005** | 1.20 | 1.08 | 0.90 | +Excellent boost |
| **p2a_006** | 1.20 | 1.08 | 0.95 | Excellent + poor |
| **p2a_007** | 1.20 | 1.10 | 0.90 | Excellent + good |
| **p2a_008** | 1.20 | 1.10 | 0.95 | All aggressive |

**Fixed Parameters**: Phase 1 winners + all other parameters at baseline

### Execution Plan

**Wait for**: Phase 1 completion and winner identification

**Preparation Steps**:
1. [ ] Extract Phase 1 winning configuration
2. [ ] Update simulation config template with Phase 1 winners
3. [ ] Generate 8 Phase 2a configuration files
4. [ ] Verify all configs use consistent baseline for non-tested parameters

**Execution**: Same as Phase 1 (sequential or parallel)

### Expected Runtime
Same as Phase 1: 26-40 hours sequential, 6.5-10 hours parallel (4-way)

### Results

**Status**: ⏳ NOT STARTED

[Results section to be filled during execution]

---

## Phase 2b: Player Rating Adjustments

### Status
**Current Status**: ⏳ BLOCKED - Waiting for Phase 2a completion
**Prerequisites**: Phase 1 and 2a winners identified

[Details to be filled when Phase 2a completes]

---

## Phase 2c: Team Quality Adjustments

### Status
**Current Status**: ⏳ BLOCKED - Waiting for Phase 2b completion
**Prerequisites**: Phases 1, 2a, and 2b winners identified

[Details to be filled when Phase 2b completes]

---

## Phase 3: Matchup Multipliers

### Status
**Current Status**: ⏳ BLOCKED - Waiting for Phase 2 completion
**Prerequisites**: All Phase 2 winners identified

### Note
This is the largest phase with 32 configurations. Consider:
- Running in batches of 8 configs
- Using cloud computing for parallel execution
- Starting with reduced simulations (10 instead of 20) for preliminary screening

[Full details to be filled when Phase 2 completes]

---

## Phase 4: Injury & Bye Penalties

### Status
**Current Status**: ⏳ BLOCKED - Waiting for Phase 3 completion

[Details to be filled when Phase 3 completes]

---

## Phase 5: Validation & Refinement

### Status
**Current Status**: ⏳ BLOCKED - Waiting for Phase 4 completion

[Details to be filled when Phase 4 completes]

---

## Phase 6: Final Verification

### Status
**Current Status**: ⏳ BLOCKED - Waiting for Phase 5 completion

[Details to be filled when Phase 5 completes]

---

## Quick Start Guide

### Running Your First Simulation (Baseline)

**Step 1: Verify Environment**
```bash
cd C:\Users\kmgam\Code\FantasyFootballHelperScripts
.venv\Scripts\activate

# Check simulation config
python -c "from draft_helper.simulation.config import PARAMETER_RANGES; print('Config loaded successfully')"
```

**Step 2: Update Simulation Code**
The current simulation system uses 2-value ranges in `PARAMETER_RANGES`. For phased testing, we need to modify the simulation to accept a single configuration dict.

**Option A: Temporary modification** (Quick & dirty)
```python
# In draft_helper/simulation/config.py
# Comment out PARAMETER_RANGES and replace with single config

# PARAMETER_RANGES = {...}  # Comment out

# Baseline configuration for testing
SINGLE_CONFIG = {
    'NORMALIZATION_MAX_SCALE': 100,
    'DRAFT_ORDER_PRIMARY_BONUS': 50,
    # ... (all parameters at baseline)
}
```

**Option B: Add configuration override** (Better approach)
```python
# In draft_helper/simulation/simulation_engine.py
def run_simulation_with_config(config_dict: Dict[str, float], num_simulations: int = 20):
    """
    Run simulation with specific configuration values.

    Args:
        config_dict: Dictionary of parameter names to values
        num_simulations: Number of simulations to run
    """
    # Override PARAMETER_RANGES to use single values
    original_ranges = PARAMETER_RANGES.copy()

    # Convert each parameter to single-value "range"
    for param, value in config_dict.items():
        PARAMETER_RANGES[param] = [value]

    try:
        # Run simulation
        results = run_simulations(num_simulations)
        return results
    finally:
        # Restore original ranges
        PARAMETER_RANGES.update(original_ranges)
```

**Step 3: Run Baseline Simulation**
```bash
# Method 1: Via Python script
python -c "
from draft_helper.simulation.simulation_engine import run_simulation_with_config

baseline_config = {
    'NORMALIZATION_MAX_SCALE': 100,
    'DRAFT_ORDER_PRIMARY_BONUS': 50,
    'DRAFT_ORDER_SECONDARY_BONUS': 25,
    # Add all 20 parameters here...
}

print('Starting baseline simulation...')
results = run_simulation_with_config(baseline_config, num_simulations=20)
print('Baseline complete!')
"

# Method 2: Via modified simulation script
cd draft_helper/simulation
python simulation_engine.py  # If you modified config.py with SINGLE_CONFIG
```

**Step 4: Monitor Progress**
```bash
# In another terminal, watch the logs
tail -f draft_helper/simulation/logs/simulation_*.log

# Or check progress
ls -ltr draft_helper/simulation/results/
```

**Step 5: Analyze Results**
```bash
# After completion, analyze results
python -c "
import pandas as pd

# Load results
df = pd.read_csv('draft_helper/simulation/results/baseline_001_results.csv')

# Quick summary
summary = df.groupby('team_id').agg({
    'win_rate': 'mean',
    'championship': 'mean',
    'playoff': 'mean'
}).mean()

print('Baseline Performance:')
print(f'Win Rate: {summary.win_rate:.4f}')
print(f'Championship Rate: {summary.championship:.4f}')
print(f'Playoff Rate: {summary.playoff:.4f}')
"
```

**Step 6: Update This Document**
- Fill in the "Baseline Results" section above
- Update status to ✅ Complete
- Record any issues or observations
- Prepare for Phase 1

---

## Troubleshooting

### Common Issues

**Issue: Simulation hangs or takes too long**
- Check CPU usage - should be near 100% during simulation
- Verify no I/O bottlenecks (slow disk writes)
- Consider reducing `SIMULATIONS_PER_CONFIG` to 10 for testing
- Check for infinite loops in matchup resolution

**Issue: Results file not generated**
- Check simulation logs for errors
- Verify output directory exists and is writable
- Ensure simulation completed all 20 runs (check log count)

**Issue: Inconsistent results across runs**
- Check if random seed is set properly
- Verify player data hasn't changed between runs
- Confirm all parameters are being applied correctly

**Issue: Config not being applied**
- Print config values at simulation start to verify
- Check if PARAMETER_RANGES is being overridden correctly
- Ensure no caching of configuration values

### Getting Help

**Before asking for help, gather**:
1. Simulation logs (last 100 lines)
2. Configuration used
3. Error messages (full traceback)
4. System info (OS, Python version, memory available)

**Resources**:
- Full strategy document: `simulation_optimization_strategy.md`
- Simulation config: `draft_helper/simulation/config.py`
- CLAUDE.md simulation section

---

## Data Archive

### Result Files Location

**Primary Results**: `draft_helper/simulation/results/`
**Logs**: `draft_helper/simulation/logs/`
**Analysis**: `draft_helper/simulation/analysis/`
**Archive**: `draft_helper/simulation/archive/` (for completed phases)

### File Naming Convention

**Results CSV**: `{phase}_{config_id}_results.csv`
- Example: `baseline_001_results.csv`, `p1_003_results.csv`

**Summary JSON**: `{phase}_{config_id}_summary.json`
- Contains aggregated statistics

**Logs**: `{phase}_{config_id}_{timestamp}.log`
- Detailed execution logs

**Analysis**: `{phase}_analysis_report.md`
- Statistical analysis and findings

### Backup Strategy

After each phase completion:
1. [ ] Copy all result files to backup directory
2. [ ] Compress logs: `tar -czf phase{N}_logs.tar.gz logs/`
3. [ ] Upload to cloud storage (if available)
4. [ ] Verify backup integrity

---

## Change Log

### Version History

**v1.0.0** - 2025-09-30
- Initial document creation
- Set up baseline and Phase 1 tracking
- Defined configuration matrices for all phases
- Added quick start guide and troubleshooting

**Future Updates**:
- Add Phase 1 results when complete
- Update Phase 2a details after Phase 1
- Add visualizations and charts
- Document any methodology changes

---

## Notes & Learnings

### General Observations

```
[Add observations and lessons learned as you go]

Example entries:
- 2025-09-30: Baseline took 4.5 hours for 20 sims (avg 13.5 min per sim)
- 2025-10-02: Found that parallel execution reduces total time by 70%
- 2025-10-05: Phase 1 revealed NORM_SCALE has bigger impact than expected
```

### Methodology Adjustments

```
[Track any changes to the optimization strategy]

Example:
- 2025-10-08: Reduced Phase 3 to 20 configs instead of 32 due to time constraints
  Reason: Initial results showed 3 of 5 matchup params had minimal impact
  Dropped: MATCHUP_NEUTRAL and MATCHUP_POOR from full testing
```

### Code Changes

```
[Track modifications to simulation code]

Example:
- 2025-09-30: Added run_simulation_with_config() to support single configs
- 2025-10-03: Fixed bug in week 15 matchup resolution
- 2025-10-10: Optimized draft logic, reduced sim time from 13.5 to 11.2 min
```

---

## Appendix: Configuration Templates

### Baseline Configuration (Template)

```python
# baseline_config.py
BASELINE_CONFIG = {
    # Core Scoring
    'NORMALIZATION_MAX_SCALE': 100,
    'DRAFT_ORDER_PRIMARY_BONUS': 50,
    'DRAFT_ORDER_SECONDARY_BONUS': 25,

    # Matchup Multipliers
    'MATCHUP_EXCELLENT_MULTIPLIER': 1.2,
    'MATCHUP_GOOD_MULTIPLIER': 1.1,
    'MATCHUP_NEUTRAL_MULTIPLIER': 1.0,
    'MATCHUP_POOR_MULTIPLIER': 0.9,
    'MATCHUP_VERY_POOR_MULTIPLIER': 0.8,

    # Injury & Bye Penalties
    'INJURY_PENALTIES_MEDIUM': 15,
    'INJURY_PENALTIES_HIGH': 30,
    'BASE_BYE_PENALTY': 10,

    # ADP Adjustments
    'ADP_EXCELLENT_MULTIPLIER': 1.15,
    'ADP_GOOD_MULTIPLIER': 1.08,
    'ADP_POOR_MULTIPLIER': 0.90,

    # Player Rating Adjustments
    'PLAYER_RATING_EXCELLENT_MULTIPLIER': 1.20,
    'PLAYER_RATING_GOOD_MULTIPLIER': 1.10,
    'PLAYER_RATING_POOR_MULTIPLIER': 0.90,

    # Team Quality Adjustments
    'TEAM_EXCELLENT_MULTIPLIER': 1.12,
    'TEAM_GOOD_MULTIPLIER': 1.06,
    'TEAM_POOR_MULTIPLIER': 0.94,
}
```

### Phase 1 Configuration Generator

```python
# generate_phase1_configs.py
def generate_phase1_configs():
    """Generate all 8 Phase 1 configurations."""
    configs = []

    # Parameter values to test
    norm_scales = [100, 120]
    primary_bonuses = [50, 60]
    secondary_bonuses = [25, 30]

    config_id = 1
    for norm in norm_scales:
        for primary in primary_bonuses:
            for secondary in secondary_bonuses:
                config = BASELINE_CONFIG.copy()
                config['NORMALIZATION_MAX_SCALE'] = norm
                config['DRAFT_ORDER_PRIMARY_BONUS'] = primary
                config['DRAFT_ORDER_SECONDARY_BONUS'] = secondary

                configs.append({
                    'id': f'p1_{config_id:03d}',
                    'config': config,
                    'description': f'Norm={norm}, Primary={primary}, Secondary={secondary}'
                })
                config_id += 1

    return configs

# Generate and save
if __name__ == '__main__':
    import json
    configs = generate_phase1_configs()

    for cfg in configs:
        filename = f"configs/{cfg['id']}_config.json"
        with open(filename, 'w') as f:
            json.dump(cfg, f, indent=2)

    print(f"Generated {len(configs)} Phase 1 configurations")
```

---

**END OF WORKING DOCUMENT**

**Remember**: Update this document as you execute each phase. It should always reflect current status and next steps.
