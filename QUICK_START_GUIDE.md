# Quick Start Guide

A practical guide to using Fantasy Football Helper Scripts throughout your fantasy football season.

## Overview

This project provides tools to help you make data-driven decisions at every stage of your fantasy football season:
- **Pre-season**: Fetch player data and tune your scoring parameters
- **Draft day**: Get real-time player recommendations during your draft
- **In-season**: Optimize weekly lineups and evaluate trade opportunities

---

## Pre-Season Setup

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd FantasyFootballHelperScripts

# Install dependencies
pip install -r requirements.txt

# Verify installation
python tests/run_all_tests.py
```

### 2. Fetch Player Data

```bash
# Download latest player projections
python run_player_fetcher.py
```

This writes the per-position player pool under `data/player_data/` (`qb_data.json`, `rb_data.json`, `wr_data.json`, `te_data.json`, `k_data.json`, `dst_data.json`).

### 3. Fetch Schedule and Historical Data

```bash
# Fetch the NFL season schedule (including bye weeks)
python run_schedule_fetcher.py

# Compile a historical season (games, weather, per-team stats) for the simulation engines
python compile_historical_data.py --year 2024
```

### 4. (Optional) Tune Scoring Parameters

If you want to optimize scoring parameters, run one of the two simulation engines:

```bash
# Win-rate optimization (ranks strategies / parameter combinations by simulated win rate)
python run_win_rate_simulation.py --sweep

# Pairwise-ranking-accuracy optimization
python run_accuracy_simulation.py
```

Both engines replay the committed historical seasons under `simulation/sim_data/`. Use `--promote` (win-rate: add `--confirm` to write) to promote the winning config into `data/configs/`.

---

## Draft Day

### Using the Draft Helper

```bash
python run_league_helper.py
```

1. Select **"Add to Roster"** mode
2. The system shows top player recommendations based on:
   - Projected points and ADP
   - Your current roster needs
   - Bye week conflicts
   - Player injury status
3. After each pick, enter the drafted player
4. Recommendations update automatically

**Tips:**
- Keep the helper running throughout your draft
- Pay attention to bye week warnings
- Consider the "why" behind each recommendation (shown in the scoring breakdown)

---

## Weekly In-Season

### 1. Update Player Data

Before each week, refresh your data:

```bash
# Update player projections
python run_player_fetcher.py

# Refresh the schedule if needed
python run_schedule_fetcher.py
```

### 2. Update Ownership Data

Use the Chrome extension to import current league rosters:

1. Install the extension from `nfl-fantasy-exporter-extension/`
2. Go to NFL Fantasy → Players → All Taken Players
3. Click the extension → "Extract All Pages" → Download CSV
4. Move the file to `data/drafted_data.csv`

### 3. Optimize Your Lineup

```bash
python run_league_helper.py
```

Select **"Starter Helper"** mode to see:
- Recommended starters for each position
- Matchup advantages/disadvantages
- Bye week alerts
- Expected points per player

### 4. Evaluate Trades

In the League Helper, select **"Trade Simulator"** mode:

- **Waiver Optimizer**: Find the best waiver-wire pickups
- **Trade Suggestor**: Discover mutually beneficial trades
- **Manual Trade Visualizer**: Analyze specific trade proposals

---

## Quick Reference

### All Scripts

| Script | Purpose | When to Use |
|--------|---------|-------------|
| `run_league_helper.py` | Interactive draft/lineup/trade tool | Draft day, weekly |
| `run_player_fetcher.py` | Download player projections | Pre-season, weekly |
| `run_schedule_fetcher.py` | Fetch the NFL schedule | Pre-season |
| `compile_historical_data.py` | Compile a historical season for simulation | Pre-season |
| `validate_sim_data.py` | Sanity-check a compiled sim_data season | Pre-season |
| `run_win_rate_simulation.py` | Tune scoring params by win rate | Pre-season |
| `run_accuracy_simulation.py` | Tune scoring params by ranking accuracy | Pre-season |
| `run_pre_commit_validation.py` | Run the full test suite (pre-commit gate) | Before commits |

### Common Commands

```bash
# Start the league helper (most common)
python run_league_helper.py

# Update player data before weekly decisions
python run_player_fetcher.py

# Run a win-rate parameter sweep
python run_win_rate_simulation.py --sweep

# Run all tests
python tests/run_all_tests.py
```

---

## Need More Help?

- **Detailed documentation**: See `README.md`
- **System architecture**: See `.shamt-core/project-specific-files/ARCHITECTURE.md`
- **Scoring algorithms**: See `docs/scoring/`
- **Development guidelines**: See `CLAUDE.md`
