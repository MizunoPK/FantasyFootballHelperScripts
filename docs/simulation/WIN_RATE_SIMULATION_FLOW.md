# Win Rate Simulation - Functional Flow Documentation (CORRECTED)

> **IMPORTANT**: This document describes the **Win Rate Simulation ONLY**.
> For Accuracy Simulation (prediction optimization), see ACCURACY_SIMULATION_FLOW_VERIFIED.md
> These are **separate simulation systems** with different purposes and parameters.

---

## ⚠️ DOCUMENT SCOPE

**This Document Covers:**
- Win Rate Simulation (`run_win_rate_simulation.py`)
- Draft strategy parameter optimization (the six `DRAFT_SWEEP_PARAMS`)
- Maximizing league win percentage

**This Document Does NOT Cover:**
- Accuracy Simulation (`run_accuracy_simulation.py`) - separate system for prediction optimization

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Entry Point and Flag Surface](#entry-point-and-flag-surface)
4. [Core Components](#core-components)
5. [Data Flow](#data-flow)
6. [Configuration System](#configuration-system)
7. [Performance Characteristics](#performance-characteristics)

---

## Overview

The Win Rate Simulation optimizes **draft strategy parameters** by simulating complete fantasy football leagues across multiple historical seasons.

### Purpose

- **Optimize the six swept draft strategy parameters** (`DRAFT_SWEEP_PARAMS`) to maximize league win rate
- **Test DraftHelper recommendations** against realistic AI opponents
- **Validate parameter changes** before applying to production configs
- **Discover optimal settings** that work across different seasons

### Key Metrics

- **Win Rate**: Percentage of head-to-head matchups won
- **Total Points**: Fantasy points scored across all weeks
- **Multi-Season Validation**: Performance across 2021, 2022, 2024+ seasons

### Parameters Swept

**The win-rate sweep tunes DRAFT STRATEGY parameters only** — the members of
`simulation.win_rate.param_value_generation.DRAFT_SWEEP_PARAMS`, in declaration order:

1. **SAME_POS_BYE_WEIGHT** - Penalty for drafting same-position players with same bye
2. **DIFF_POS_BYE_WEIGHT** - Penalty for drafting different-position players with same bye
3. **PRIMARY_BONUS** - Bonus points for drafting primary positions at optimal time
4. **SECONDARY_BONUS** - Bonus points for drafting secondary positions
5. **ADP_SCORING_WEIGHT** - Weight given to Average Draft Position
6. **PLAYER_RATING_SCORING_WEIGHT** - Weight given to expert rankings

Each parameter's range and precision come from `simulation.shared.ConfigGenerator.PARAM_DEFINITIONS`.

**Note**: `DRAFT_NORMALIZATION_MAX_SCALE` is still a live base-config parameter
(`simulation.shared.config_constants.BASE_CONFIG_PARAMS`) but is **no longer swept** — it was dropped from
`DRAFT_SWEEP_PARAMS` by T33.

**Note**: Prediction accuracy parameters (TEAM_QUALITY, MATCHUP, WEATHER, etc.) are optimized separately by `run_accuracy_simulation.py`.

---

## Architecture

### High-Level Components

```
run_win_rate_simulation.py (Entry Point — flags only, no positional mode)
    ↓
    ├─ (no workflow flag) → DraftStrategyOrchestrator   rank every draft strategy
    ├─ --sweep            → SweepTournament             coordinate ascent over DRAFT_SWEEP_PARAMS
    └─ --promote          → config_promoter → paired_comparison
        ↓
    For each configuration evaluated:
        ↓
    ParallelLeagueRunner (Thread Pool, sized by --workers)
        ↓
    Multiple SimulatedLeague instances (parallel)
        ├─ DraftHelperTeam (system under test)
        └─ SimulatedOpponent (AI competitors, --naive-opponents field)
            ↓
        Snake Draft (15 rounds, 150 picks)
            ↓
        17-Week Season Simulation
            ├─ Week 1 through Week 17
            └─ Each week: Lineup optimization + scoring + matchup resolution
                ↓
        Return: wins, losses, points_scored, points_against
            ↓
    Results persist to win_rate_meta_data.json / win_rate_sweep_results.json
        ↓
    --promote --confirm writes data/configs/league_config.json
```

### Module Organization

```
simulation/
├─ win_rate/                          # Win rate optimization
│   ├─ DraftStrategyOrchestrator.py   # Enumerates draft strategies, runs the ranking pass
│   ├─ WinRateMetaDataManager.py      # Best-win-rate-per-strategy persistence
│   ├─ strategy_loader.py             # Loads draft_order_possibilities/*.json
│   ├─ SweepTournament.py             # Coordinate-ascent parameter sweep
│   ├─ CombinationEvaluator.py        # Evaluates one parameter combination
│   ├─ SweepResultsManager.py         # win_rate_sweep_results.json persistence
│   ├─ sweep_summary.py               # Sweep reporting
│   ├─ param_value_generation.py      # DRAFT_SWEEP_PARAMS + candidate value generation
│   ├─ config_promoter.py             # Promotion decision (LCB shortlist + re-measure)
│   ├─ paired_comparison.py           # Head-to-head A/B comparison
│   ├─ config_overrides.py            # Applies a trial config over the base config
│   ├─ SimDataLoader.py               # Historical season data loading and validation
│   ├─ SimulatedLeague.py             # League simulation logic
│   ├─ DraftHelperTeam.py             # Draft Helper system team
│   ├─ SimulatedOpponent.py           # AI opponent teams
│   ├─ Week.py                        # Weekly matchup simulation
│   └─ ParallelLeagueRunner.py        # Parallel execution engine
├─ shared/                            # Shared utilities
│   ├─ ConfigGenerator.py             # Parameter combination generator (accuracy simulation)
│   ├─ ResultsManager.py              # Result tracking and ranking
│   ├─ ConfigPerformance.py           # Per-config performance record
│   └─ config_constants.py            # BASE_CONFIG_PARAMS / WEEK_SPECIFIC_PARAMS
└─ sim_data/                          # Historical season data + draft_order_possibilities/
```

---

## Entry Point and Flag Surface

`run_win_rate_simulation.py` takes **no positional argument**. Every workflow is selected by flags on the
one entry point. (It once carried `single` / `full` / `iterative` subcommands; those were removed when the
CLI was rewritten.)

**Authoritative description:** `.shamt-core/project-specific-files/ARCHITECTURE.md` §"Component 2:
Win-Rate Simulation Engine" is the maintained description of this CLI — its flags, defaults, and
semantics. This section is a **pointer**, deliberately not a second copy: two descriptions of one CLI is
the condition that produced the drift this section replaces. Run `python run_win_rate_simulation.py --help`
for the authoritative flag list.

**Real modules behind the flags** (all under `simulation/win_rate/`): `DraftStrategyOrchestrator`,
`SweepTournament`, `config_promoter`, `paired_comparison`, `WinRateMetaDataManager`.

### The three workflows

**1. Strategy ranking — the default (no workflow flag).**

```bash
python run_win_rate_simulation.py --sims 10 --workers 8
```

Enumerates the draft strategies that `simulation.win_rate.strategy_loader` globs from
`simulation/sim_data/draft_order_possibilities/*.json`, runs each through `DraftStrategyOrchestrator`, and
prints the ranked strategy/win-rate table via `run_win_rate_simulation._print_summary`. Best-per-strategy
results persist through `WinRateMetaDataManager`. Optional: `--strategy`, `--endless`, `--seed`,
`--naive-opponents`.

**2. Parameter sweep (`--sweep`).**

```bash
python run_win_rate_simulation.py --sweep --num-values 5
```

`run_win_rate_simulation._run_sweep_mode` drives `SweepTournament`: **coordinate ascent** over the six
parameters in `simulation.win_rate.param_value_generation.DRAFT_SWEEP_PARAMS`. Each trial config is
evaluated **measured-vs-incumbent** — the measured team drafts the trial config while the rest of the
field drafts the running best — so a win rate is a marginal "does this beat the best so far?" signal, not
an absolute. Results persist through `SweepResultsManager`. Optional: `--fresh`, `--seed`, `--data`.

**3. Paired comparison / promote (`--promote`).**

```bash
python run_win_rate_simulation.py --promote
python run_win_rate_simulation.py --promote --confirm
python run_win_rate_simulation.py --promote --promote-shortlist 3 --promote-sims 20
python run_win_rate_simulation.py --sweep --promote
```

Bare `--promote` previews and writes nothing; adding `--confirm` writes `data/configs/league_config.json`.
`simulation.win_rate.config_promoter.compute_promotion` LCB-shortlists candidates and re-measures them
head-to-head against the live config via
`simulation.win_rate.paired_comparison.run_paired_ab_comparison`, and **may refuse to write**.

**Guard:** `--promote` cannot be combined with `--endless`. `run_win_rate_simulation.main` checks this
explicitly, logs "`--promote` cannot be combined with `--endless`: an endless sweep never terminates to
promote", and exits with status **`2`**.

### There is no "single mode"

The removed `single` mode has no flag analog — nothing on this CLI evaluates one named configuration and
reports its statistics. The nearest runnable equivalent is a bounded default run:

```bash
python run_win_rate_simulation.py --sims 1 --workers 1 --data simulation/sim_data
```

That ranks every strategy at one simulation each rather than evaluating a single named config; treat it as
a smoke test, not as a measurement.

### Why there is no grid-search mode

An exhaustive cartesian grid search was **abandoned** in favour of coordinate ascent — it is a removed
feature, not a missing one. The arithmetic it implied is why it was impractical:

- The configuration count is the product of every varied parameter's candidate-value count, so it grows multiplicatively with the number of parameters varied

**Formula**: the product of each varied parameter's `test_values + 1` candidate values — a full cartesian product over the parameters varied simultaneously

---

## Core Components

### 3. ParallelLeagueRunner

**File**: `simulation/win_rate/ParallelLeagueRunner.py`

**Responsibilities**:
- Execute multiple league simulations in parallel
- Manage thread/process pools
- Handle exceptions and timeouts
- Track progress and collect results
- Memory management and cleanup

**Execution Strategies**:

#### ThreadPoolExecutor (Default)
```python
with ThreadPoolExecutor(max_workers=8) as executor:
    futures = []
    for sim_num in range(num_sims):
        future = executor.submit(run_single_simulation, config, sim_num)
        futures.append(future)

    for future in as_completed(futures):
        result = future.result()
        results.append(result)
```

**Advantages**:
- Lower memory overhead
- Shared memory space
- Faster startup

**Disadvantages**:
- Python GIL limits true parallelism
- CPU-bound bottleneck

#### ProcessPoolExecutor (Optional)
```python
with ProcessPoolExecutor(max_workers=8) as executor:
    # Same structure as ThreadPoolExecutor
```

**Advantages**:
- True parallelism (no GIL)
- Better CPU utilization

**Disadvantages**:
- Higher memory overhead (separate processes)
- Slower startup
- Data serialization overhead

---

### 4. SimulatedLeague

**File**: `simulation/win_rate/SimulatedLeague.py`

**Responsibilities**:
- Create and manage 10 fantasy football teams
- Orchestrate snake draft (15 rounds, 150 picks)
- Simulate 17-week season with matchups
- Track wins, losses, and points
- Manage team-specific PlayerManager instances

**League Structure**:

```python
class SimulatedLeague:
    # Team strategy distribution (from lines 77-83)
    TEAM_STRATEGIES = {
        'draft_helper': 1,                            # 1 DraftHelper team
        'adp_aggressive': 2,                          # 2 ADP-focused teams
        'projected_points_aggressive': 2,             # 2 projection-focused teams
        'adp_with_draft_order': 2,                    # 2 ADP + draft order teams
        'projected_points_with_draft_order': 3        # 3 projection + draft order teams
    }
```

**Total**: 10 teams (1 DraftHelper + 9 AI opponents)

**Snake Draft Implementation**:

```python
def run_draft(self):
    """Execute 15-round snake draft"""
    num_rounds = 15
    num_teams = 10

    for round_num in range(1, num_rounds + 1):
        if round_num % 2 == 1:  # Odd rounds: 1→10
            draft_order = list(range(10))
        else:  # Even rounds: 10→1 (snake)
            draft_order = list(range(9, -1, -1))

        for team_idx in draft_order:
            team = self.teams[team_idx]
            player = team.select_draft_pick()
            team.draft_player(player)

            # Mark player as drafted for all teams
            for t in self.teams:
                t.mark_player_drafted(player.id)
```

**Data Optimization**:
- **Shared read-only directories**: All teams reference same season data folder
- **In-memory PlayerManager instances**: Each team has independent instance (no disk copies)
- **Pre-loaded week data**: All 17 weeks loaded at initialization to avoid repeated I/O

---

### 5. SimulatedOpponent

**File**: `simulation/win_rate/SimulatedOpponent.py`

**Responsibilities**:
- Represent AI opponent teams with different strategies
- Make draft decisions based on strategy type
- Optimize weekly lineups
- Provide realistic competition for DraftHelper team

**Strategy Types**:

| Strategy | Draft Logic | Weighting |
|----------|------------|-----------|
| `adp_aggressive` | Prioritize ADP (Best Player Available) | 80% ADP, 20% Projected Points |
| `projected_points_aggressive` | Prioritize projected points | 20% ADP, 80% Projected Points |
| `adp_with_draft_order` | ADP + draft order bonuses | 60% ADP, 20% PP, 20% Draft Order |
| `projected_points_with_draft_order` | Projected points + draft order | 30% ADP, 50% PP, 20% Draft Order |

---

## Data Flow

### Historical Season Data Structure

```
simulation/sim_data/
├─ 2021/
│   ├─ season_schedule.csv           # Bye weeks, game matchups
│   ├─ game_data.csv                 # Weather, location data
│   ├─ team_data/                    # Per-NFL-team rankings
│   │   ├─ ARI.csv
│   │   ├─ ATL.csv
│   │   └─ ... (32 teams)
│   └─ weeks/
│       ├─ week_01/
│       │   ├─ qb_data.json          # QB projected + actual points
│       │   ├─ rb_data.json          # RB projected + actual points
│       │   ├─ wr_data.json          # WR projected + actual points
│       │   ├─ te_data.json          # TE projected + actual points
│       │   ├─ k_data.json           # K projected + actual points
│       │   └─ dst_data.json         # DST projected + actual points
│       ├─ week_02/
│       └─ ... week_17/
├─ 2022/
└─ 2024/
```

**Note**: Each position JSON file contains arrays for:
- `projected_points[0..16]` - Projected points for weeks 1-17
- `actual_points[0..16]` - Actual points for weeks 1-17

---

## Configuration System

### Three-Level Hierarchy

#### Level 1: Base Configuration (`league_config.json`)

**Parameters that apply league-wide** (optimized by win rate simulation):

```json
{
  "DRAFT_NORMALIZATION_MAX_SCALE": 150,
  "SAME_POS_BYE_WEIGHT": 0.25,
  "DIFF_POS_BYE_WEIGHT": 0.15,
  "DRAFT_ORDER_BONUSES": {
    "PRIMARY": 87,
    "SECONDARY": 78
  },
  "ADP_SCORING": {
    "WEIGHT": 3.0,
    "THRESHOLDS": { "STEPS": 25 }
  },
  "PLAYER_RATING_SCORING": {
    "WEIGHT": 2.0
  }
}
```

#### Level 2: Week-Range Configurations (`week*.json`)

**Parameters optimized separately for different season phases** (by accuracy simulation):

- `week1-5.json` - Early season
- `week6-9.json` - Mid-early season
- `week10-13.json` - Mid-late season
- `week14-17.json` - Playoffs

**These are NOT optimized by win rate simulation** - they're optimized by `run_accuracy_simulation.py`

---

## Performance Characteristics

### Scalability

**Simulation Count Scaling** (single config, single season):
- 10 sims: ~0.4s
- 50 sims: ~2s
- 100 sims: ~4s
- 500 sims: ~18s

**Worker Count Scaling** (100 sims, single season):
- 1 worker: 15s
- 2 workers: 8s
- 4 workers: 5s
- 8 workers: 4s
- 16 workers: 3.5s (diminishing returns)

**Optimal**: 8 workers for most systems.

### Configuration Counts

Coordinate ascent (`simulation/win_rate/SweepTournament.py`) is **not** a fixed-configuration-count
algorithm. It visits one parameter at a time from
`simulation.win_rate.param_value_generation.DRAFT_SWEEP_PARAMS`, and the number of configurations it
evaluates depends on `--num-values`, on how many passes converge, and on which trials the
measured-vs-incumbent comparison rejects. Any fixed "N configs" figure for this engine is wrong by
construction.

**Historical note** — the count formula for the exhaustive grid-search mode that was removed when the CLI
was rewritten (wording retained verbatim from T65's correction):

| Mode (removed) | Formula | Default Count | Notes |
|------|---------|---------------|-------|
| Full | product of each varied parameter's (test_values + 1) values | grows multiplicatively | Impractical |

---

## Summary

### Key Takeaways

1. **Win Rate Simulation optimizes DRAFT STRATEGY parameters** (not prediction parameters) — the sweep tunes the six members of `simulation.win_rate.param_value_generation.DRAFT_SWEEP_PARAMS`

2. **One entry point, no positional modes**: workflows are selected by flags — no flag (strategy ranking), `--sweep` (parameter sweep), `--promote` (paired comparison)

3. **The sweep is coordinate ascent**, so it has no fixed configuration count; the number of configurations evaluated depends on `--num-values`, on how many passes converge, and on which trials the incumbent comparison rejects

4. **Multi-season validation**: Tests across all available historical seasons (2021, 2022, 2024+)

5. **10-team league simulation**: 1 DraftHelper + 9 AI opponents with diverse strategies

6. **High-performance parallel execution**: ThreadPoolExecutor default, ProcessPoolExecutor optional

7. **5-file config structure**: league_config.json + 4 week-range files

### Typical Use Cases

**Development Workflow**:

1. Modify draft strategy parameters in `data/configs/league_config.json`
2. Run a bounded smoke test:

```bash
python run_win_rate_simulation.py --sims 1 --workers 1 --data simulation/sim_data
```

3. If promising, run the sweep:

```bash
python run_win_rate_simulation.py --sweep --num-values 5
```

4. Review the sweep store `win_rate_sweep_results.json` under the `--data` folder (written by `SweepResultsManager`)
5. Promote the winner:

```bash
python run_win_rate_simulation.py --promote --confirm
```

**Continuous Improvement**:

1. Re-run the sweep periodically; each pass measures trial configs against the current incumbent
2. Track win rate trends over time via `win_rate_meta_data.json` (`WinRateMetaDataManager`)
3. Adjust candidate ranges in `simulation.win_rate.param_value_generation` based on findings
4. Archive results for historical comparison

---

## Conclusion

The Win Rate Simulation is a sophisticated system for optimizing fantasy football draft strategies through multi-season league simulations. By testing configurations against realistic AI opponents across historical data, it provides data-driven insights into optimal parameter settings.

**Key Distinction**: This system optimizes **DRAFT STRATEGY** (how to pick players). Separate `run_accuracy_simulation.py` optimizes **PREDICTION ACCURACY** (how to score players).

**For more information**:
- See `.shamt-core/project-specific-files/ARCHITECTURE.md` for complete system architecture (§"Component 2: Win-Rate Simulation Engine" is the authoritative win-rate CLI description)
- See `README.md` for usage instructions
- See `simulation/README.md` for simulation-specific details
- See `run_accuracy_simulation.py` for prediction optimization

---

**Document Version**: 2.0 (Corrected)
**Last Updated**: 2026-01-05
**Verified Against**: Latest main branch source code
