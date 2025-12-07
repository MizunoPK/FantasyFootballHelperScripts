# Team Data Architecture Refactor - Code Changes Documentation

## Overview
This document tracks all code changes made during the team data architecture refactor. It will be updated incrementally as each task is completed.

**Objective**: Replace centralized teams.csv with per-team historical data files and on-the-fly ranking calculations.

---

## Change Log

*To be updated as implementation progresses*

---

## Phase 1: Create New Data Structure

### 1.1 - Define new team CSV format
**Status**: Pending

### 1.2 - Update player-data-fetcher/config.py
**Status**: Pending

Files to modify:
- player-data-fetcher/config.py

Changes planned:
- Remove TEAMS_CSV constant (line 40)
- Remove MIN_WEEKS_FOR_CURRENT_SEASON_RANKINGS constant (line 43)
- Add TEAM_DATA_FOLDER constant

---

## Phase 2: Update League Helper

### 2.1 - Update league_config.json
**Status**: Pending

### 2.2 - Update ConfigManager.py
**Status**: Pending

### 2.3 - Refactor TeamDataManager.py
**Status**: Pending

### 2.4 - Update PlayerManager.py
**Status**: Pending

### 2.5 - Update LeagueHelperManager.py
**Status**: Pending

---

## Phase 3: Update Simulation

### 3.1 - Create generate_team_data.py
**Status**: Pending

### 3.2 - Update ConfigGenerator.py
**Status**: Pending

### 3.3 - Update SimulatedLeague.py
**Status**: Pending

### 3.4 - Remove old simulation team data
**Status**: Pending

---

## Phase 4: Cleanup and Testing

### 4.1 - Remove teams.csv references
**Status**: Pending

### 4.2 - Update unit tests
**Status**: Pending

### 4.3 - Update integration tests
**Status**: Pending

### 4.4 - Update documentation
**Status**: Pending

### 4.5 - Final validation
**Status**: Pending

---

## Files Modified Summary

*To be updated as changes are made*

### Production Code
- [ ] player-data-fetcher/config.py
- [ ] player-data-fetcher/espn_client.py
- [ ] player-data-fetcher/player_data_exporter.py
- [ ] player-data-fetcher/player_data_fetcher_main.py
- [ ] data/league_config.json
- [ ] league_helper/util/TeamDataManager.py
- [ ] league_helper/util/PlayerManager.py
- [ ] league_helper/util/ConfigManager.py
- [ ] league_helper/LeagueHelperManager.py
- [ ] simulation/generate_team_data.py (new)
- [ ] simulation/ConfigGenerator.py
- [ ] simulation/SimulatedLeague.py
- [ ] utils/TeamData.py

### Test Code
- [ ] tests/utils/test_TeamData.py
- [ ] tests/league_helper/util/test_TeamDataManager.py (18+ changes)
- [ ] tests/league_helper/trade_simulator_mode/test_manual_trade_visualizer.py (5 changes)
- [ ] tests/league_helper/util/test_PlayerManager_scoring.py (1 change)
- [ ] tests/player-data-fetcher/test_config.py
- [ ] tests/integration/*.py

### Documentation
- [ ] docs/scoring/04_team_quality_multiplier.md
- [ ] docs/scoring/06_matchup_multiplier.md
- [ ] docs/scoring/07_schedule_multiplier.md
- [ ] README.md
- [ ] ARCHITECTURE.md
- [ ] CLAUDE.md

### Data Files
- [ ] Create: data/team_data/*.csv (32 files)
- [ ] Create: simulation/sim_data/team_data/*.csv (32 files)
- [ ] Remove: data/teams.csv
- [ ] Remove: player-data-fetcher/data/teams_*.csv
- [ ] Remove: simulation/sim_data/teams_week_*.csv (18 files)

---

## Verification Checklist

- [ ] All unit tests pass (100%)
- [ ] All integration tests pass
- [ ] Manual testing of league_helper modes
- [ ] Manual testing of simulation system
- [ ] Documentation updated
- [ ] No teams.csv references remaining

---

## Notes

- TeamDataManager signature changed from 3 params to 4 params (breaking change)
- 24+ call sites need updating for TeamDataManager
- 47 files reference teams.csv (need cleanup)
