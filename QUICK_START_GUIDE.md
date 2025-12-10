# Quick Start Guide

A practical guide to using Fantasy Football Helper Scripts throughout your fantasy football season.

## Overview

This project provides tools to help you make data-driven decisions at every stage of your fantasy football season:
- **Pre-season**: Fetch player data and optimize your draft strategy
- **Draft day**: Get real-time player recommendations during your draft
- **In-season**: Optimize weekly lineups and evaluate trade opportunities

---

## Pre-Season Setup

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd FantasyFootballHelperScriptsRefactored

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

This creates `data/players.csv` with current season projections.

### 3. Fetch Schedule and Game Data

```bash
# Fetch NFL season schedule
python run_schedule_fetcher.py

# Fetch game data (venue, weather)
python run_game_data_fetcher.py
```

### 4. (Optional) Run Simulations

If you want to optimize scoring parameters:

```bash
# Quick test (5 simulations)
python run_simulation.py single --sims 5

# Full optimization (~2-3 hours)
python run_simulation.py iterative --sims 100 --workers 8
```

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
- Consider the "why" behind each recommendation (shown in scoring breakdown)

---

## Weekly In-Season

### 1. Update Player Data

Before each week, refresh your data:

```bash
# Update player projections
python run_player_fetcher.py

# Update scores and team rankings
python run_scores_fetcher.py
```

### 2. Update Ownership Data

Use the Chrome extension to import current league rosters:

1. Install extension from `nfl-fantasy-exporter-extension/`
2. Go to NFL Fantasy → Players → All Taken Players
3. Click extension → "Extract All Pages" → Download CSV
4. Move file to `data/drafted_data.csv`

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

- **Waiver Optimizer**: Find best waiver wire pickups
- **Trade Suggestor**: Discover mutually beneficial trades
- **Manual Trade Visualizer**: Analyze specific trade proposals

---

## Quick Reference

### All Scripts

| Script | Purpose | When to Use |
|--------|---------|-------------|
| `run_league_helper.py` | Interactive draft/lineup/trade tool | Draft day, weekly |
| `run_player_fetcher.py` | Download player projections | Pre-season, weekly |
| `run_scores_fetcher.py` | Update NFL scores and rankings | Weekly |
| `run_schedule_fetcher.py` | Fetch NFL schedule | Pre-season |
| `run_game_data_fetcher.py` | Fetch game/weather data | Pre-season, weekly |
| `run_simulation.py` | Optimize scoring parameters | Pre-season |
| `run_draft_order_simulation.py` | Test draft strategies | Pre-season |

### Common Commands

```bash
# Start league helper (most common)
python run_league_helper.py

# Update all data before weekly decisions
python run_player_fetcher.py && python run_scores_fetcher.py

# Run quick simulation test
python run_simulation.py single --sims 5

# Run all tests
python tests/run_all_tests.py
```

---

## Need More Help?

- **Detailed documentation**: See `README.md`
- **System architecture**: See `ARCHITECTURE.md`
- **Scoring algorithms**: See `docs/scoring_v2/`
- **Development guidelines**: See `CLAUDE.md`
