# Simulation Implementation TODO

## 📋 Project Overview
Implement a comprehensive fantasy football draft and season simulation system to optimize configuration parameters through automated testing. The system will run 46,656 different parameter combinations (6^6), with 100 league simulations per configuration, to find the optimal settings that maximize DraftHelper win rate.

## 🎯 Implementation Phases

### Phase 1: Core Data Structures & Models (Manual Testing Foundation)
Build the fundamental classes and data structures needed for a single manual simulation.

#### 1.1 Enhanced Team Classes
- [ ] **DraftHelperTeam class** (simulation/DraftHelperTeam.py)
  - [ ] Store roster (list of drafted players)
  - [ ] Store 2 PlayerManager instances (projected + actual)
  - [ ] Store ConfigManager instance
  - [ ] Initialize AddToRosterModeManager for draft decisions
  - [ ] Initialize StarterHelperModeManager for weekly lineups
  - [ ] Method: `draft_player(player)` - adds player to roster, marks as drafted
  - [ ] Method: `get_draft_recommendation()` - uses AddToRosterModeManager
  - [ ] Method: `set_weekly_lineup(week)` - uses StarterHelperModeManager
  - [ ] Method: `get_weekly_score(week)` - calculates actual points from lineup

- [ ] **SimulatedOpponent class** (simulation/SimulatedOpponent.py)
  - [ ] Store roster (list of drafted players)
  - [ ] Store 2 PlayerManager instances (projected + actual)
  - [ ] Store strategy string ('adp_aggressive', 'projected_points_aggressive', etc.)
  - [ ] Method: `draft_player(player)` - adds player to roster, marks as drafted
  - [ ] Method: `get_draft_recommendation()` - implements strategy-based drafting
    - [ ] 'adp_aggressive': Pick lowest ADP available
    - [ ] 'projected_points_aggressive': Pick highest projected points
    - [ ] 'adp_with_draft_order': Use ADP with position priorities from config
    - [ ] 'projected_points_with_draft_order': Use points with position priorities
  - [ ] Method: `apply_human_error(recommendations)` - 20% chance to pick from top 5 instead of #1
  - [ ] Method: `set_weekly_lineup(week)` - picks highest projected points per position
  - [ ] Method: `get_weekly_score(week)` - calculates actual points from lineup

#### 1.2 League Simulation Classes
- [ ] **Week class** (simulation/Week.py)
  - [ ] Store week number (1-17)
  - [ ] Store matchups (list of tuples: [(team1, team2), ...])
  - [ ] Method: `generate_matchups(teams)` - creates round-robin pairings
  - [ ] Method: `simulate_week()` - runs all matchups, determines winners
  - [ ] Method: `get_results()` - returns dict of {team: (opponent, points_scored, points_against, won)}

- [ ] **SimulatedLeague class** (simulation/SimulatedLeague.py)
  - [ ] Store 10 teams (1 DraftHelperTeam + 9 SimulatedOpponent)
  - [ ] Store 17 Week instances
  - [ ] Store ConfigManager instance
  - [ ] Store draft order (randomized snake order)
  - [ ] Method: `initialize_teams()` - creates all team instances with fresh PlayerManagers
  - [ ] Method: `load_player_data()` - loads CSV data into PlayerManagers
  - [ ] Method: `run_draft()` - executes full snake draft (15 rounds)
  - [ ] Method: `run_season()` - simulates all 17 weeks
  - [ ] Method: `get_draft_helper_results()` - returns (wins, losses, total_points)

#### 1.3 Round-Robin Scheduling
- [ ] **RoundRobinScheduler utility** (simulation/utils/scheduler.py)
  - [ ] Method: `generate_double_round_robin(teams)` - creates 17-week schedule
    - [ ] Each team plays every other team twice (9 opponents × 2 = 18 games)
    - [ ] Fit into 17 weeks (one team gets 16 games instead of 18)
  - [ ] Return list of 17 week matchup lists

#### 1.4 Unit Tests for Core Components
- [ ] **test_DraftHelperTeam.py**
  - [ ] Test initialization with PlayerManagers
  - [ ] Test draft_player() updates roster and marks as drafted
  - [ ] Test get_draft_recommendation() calls AddToRosterModeManager
  - [ ] Test set_weekly_lineup() uses StarterHelperModeManager
  - [ ] Test get_weekly_score() calculates actual points correctly

- [ ] **test_SimulatedOpponent.py**
  - [ ] Test each strategy type (adp_aggressive, projected_points_aggressive, etc.)
  - [ ] Test human error rate (mock random to verify 20% error triggering)
  - [ ] Test draft_player() marks player as drafted across all teams
  - [ ] Test set_weekly_lineup() picks highest projected points
  - [ ] Test get_weekly_score() uses actual points data

- [ ] **test_Week.py**
  - [ ] Test matchup generation (5 pairings for 10 teams)
  - [ ] Test simulate_week() determines correct winners
  - [ ] Test tie handling (ties count as losses)

- [ ] **test_SimulatedLeague.py**
  - [ ] Test team initialization (1 DraftHelper + 9 opponents)
  - [ ] Test draft flow (snake order, 15 rounds, all players marked drafted)
  - [ ] Test season flow (17 weeks, all matchups played)
  - [ ] Test results aggregation (wins/losses/points)

- [ ] **test_RoundRobinScheduler.py**
  - [ ] Test double round-robin generates correct schedule
  - [ ] Test each team plays correct number of games (~17-18)
  - [ ] Test no team plays itself

### Phase 2: Configuration Management & Parameter Generation
Build the system to generate and manage different configuration combinations.

#### 2.1 Parameter Generation System
- [ ] **ConfigGenerator class** (simulation/ConfigGenerator.py)
  - [ ] Method: `load_baseline_config(json_path)` - loads starting config
  - [ ] Method: `generate_parameter_values()` - creates 6 values per parameter
    - [ ] NORMALIZATION_MAX_SCALE: optimal ± 20, bounded [60, 140]
    - [ ] BASE_BYE_PENALTY: optimal ± 10, bounded [0, 40]
    - [ ] DRAFT_ORDER_BONUSES.PRIMARY: optimal ± 20, bounded [25, 100]
    - [ ] DRAFT_ORDER_BONUSES.SECONDARY: optimal ± 20, bounded [25, 75]
    - [ ] POSITIVE_MULTIPLIER: optimal ± 0.1, bounded [1.0, 1.3]
    - [ ] NEGATIVE_MULTIPLIER: optimal ± 0.1, bounded [0.7, 1.0]
  - [ ] Method: `generate_all_combinations()` - creates 6^6 = 46,656 configs
  - [ ] Method: `create_config_dict(combination)` - builds config JSON from parameter values
  - [ ] Method: `apply_multipliers(config, positive_mult, negative_mult)` - applies to all scoring sections
    - [ ] For each section (ADP, Player Rating, Team Quality, Consistency, Matchup):
      - [ ] Generate GOOD multiplier from POSITIVE_MULTIPLIER range
      - [ ] Generate EXCELLENT multiplier from POSITIVE_MULTIPLIER range (different value)
      - [ ] Generate POOR multiplier from NEGATIVE_MULTIPLIER range
      - [ ] Generate VERY_POOR multiplier from NEGATIVE_MULTIPLIER range (different value)

#### 2.2 Configuration Testing
- [ ] **test_ConfigGenerator.py**
  - [ ] Test baseline config loading
  - [ ] Test parameter value generation (6 values per parameter, within bounds)
  - [ ] Test combination generation (exactly 46,656 configs)
  - [ ] Test config dict creation (valid JSON structure)
  - [ ] Test multiplier application (all sections updated correctly)
  - [ ] Test multiplier differentiation (GOOD ≠ EXCELLENT, POOR ≠ VERY_POOR)

### Phase 3: Single Manual Simulation (Testing & Validation)
Run and validate a complete single league simulation before automation.

#### 3.1 Manual Simulation Script
- [ ] **manual_simulation.py** (simulation/manual_simulation.py)
  - [ ] Load baseline config from optimal_2025-10-02 JSON
  - [ ] Create ConfigManager with baseline config
  - [ ] Initialize SimulatedLeague with config
  - [ ] Run draft and print results (which team got which players)
  - [ ] Run season and print weekly results
  - [ ] Print final standings (wins/losses/points for each team)
  - [ ] Validate DraftHelper team uses AddToRosterMode and StarterHelper correctly

#### 3.2 Manual Simulation Validation
- [ ] Run manual_simulation.py and verify:
  - [ ] Draft completes successfully (150 total picks, 15 per team)
  - [ ] Top ADP players go early (validate draft logic)
  - [ ] DraftHelper team gets reasonable players
  - [ ] All 17 weeks simulate correctly
  - [ ] Weekly lineups make sense (starters vs bench)
  - [ ] Final results are realistic (win rates, point totals)

#### 3.3 Draft Synchronization Testing
- [ ] **test_draft_synchronization.py**
  - [ ] Test: When team A drafts player X, all other teams see X as drafted=1
  - [ ] Test: No team can draft the same player twice
  - [ ] Test: Player availability updates across projected AND actual managers
  - [ ] Test: Draft recommendations exclude already-drafted players

### Phase 4: Performance Metrics & Result Tracking
Build the system to track and compare configuration performance.

#### 4.1 Results Tracking Classes
- [ ] **ConfigPerformance class** (simulation/ConfigPerformance.py)
  - [ ] Store config parameters (dict)
  - [ ] Store total wins across all simulations
  - [ ] Store total games played
  - [ ] Store total points scored across all simulations
  - [ ] Method: `add_league_result(wins, losses, points)` - accumulates results
  - [ ] Method: `get_win_rate()` - returns wins / total_games
  - [ ] Method: `get_avg_points_per_league()` - returns total_points / num_leagues
  - [ ] Method: `compare_to(other)` - returns which config is better (win rate, then points)

- [ ] **ResultsManager class** (simulation/ResultsManager.py)
  - [ ] Store dict of {config_id: ConfigPerformance}
  - [ ] Method: `record_result(config_id, wins, losses, points)` - updates performance
  - [ ] Method: `get_best_config()` - returns ConfigPerformance with highest win rate
  - [ ] Method: `save_optimal_config(output_path)` - writes best config to JSON

#### 4.2 Results Testing
- [ ] **test_ConfigPerformance.py**
  - [ ] Test performance accumulation across multiple leagues
  - [ ] Test win rate calculation
  - [ ] Test avg points per league calculation
  - [ ] Test comparison logic (win rate primary, points tiebreaker)

- [ ] **test_ResultsManager.py**
  - [ ] Test result recording for multiple configs
  - [ ] Test best config selection (highest win rate)
  - [ ] Test tiebreaker (equal win rate, higher points wins)
  - [ ] Test JSON output format

### Phase 5: Parallel Execution & Progress Tracking
Implement parallelization and progress monitoring for large-scale simulations.

#### 5.1 Parallel League Runner
- [ ] **ParallelLeagueRunner class** (simulation/ParallelLeagueRunner.py)
  - [ ] Use ThreadPoolExecutor for parallel league simulations
  - [ ] Method: `run_config_batch(config, num_simulations)` - runs N leagues in parallel
  - [ ] Method: `simulate_single_league(config)` - thread-safe league simulation
    - [ ] Each thread loads fresh PlayerManager data from CSV files
    - [ ] No shared state between threads (each league fully isolated)
  - [ ] Return aggregated results (total wins, total points)

#### 5.2 Progress Tracking
- [ ] **ProgressTracker class** (simulation/ProgressTracker.py)
  - [ ] Track: current config number, total configs
  - [ ] Track: current league number, total leagues
  - [ ] Track: start time, elapsed time
  - [ ] Method: `update(leagues_completed)` - increments progress
  - [ ] Method: `estimate_time_remaining()` - calculates ETA based on current pace
  - [ ] Method: `print_progress()` - displays: "Leagues: 1234/4,665,600 | Elapsed: 2h 15m | ETA: 18h 30m"

#### 5.3 Parallelization Testing
- [ ] **test_ParallelLeagueRunner.py**
  - [ ] Test thread safety (no shared state corruption)
  - [ ] Test results aggregation from parallel runs
  - [ ] Test that parallel results match serial results (same seed)

- [ ] **test_ProgressTracker.py**
  - [ ] Test progress calculation
  - [ ] Test time estimation accuracy
  - [ ] Test progress display formatting

### Phase 6: Full Simulation Manager (Automation)
Tie everything together into the main simulation orchestration system.

#### 6.1 SimulationManager Implementation
- [ ] **SimulationManager class** (simulation/SimulationManager.py)
  - [ ] Method: `run_optimization_cycle()` - single end-to-end run
    - [ ] Load baseline config
    - [ ] Generate all parameter combinations (46,656 configs)
    - [ ] For each config:
      - [ ] Run 100 league simulations (parallelized)
      - [ ] Track results in ResultsManager
      - [ ] Update progress tracker
    - [ ] Get best config from ResultsManager
    - [ ] Save optimal config to JSON with timestamp
    - [ ] Return optimal config for next cycle
  - [ ] Method: `run_n_cycles(n)` - runs N optimization cycles (NUMBER_OF_RUNS)
    - [ ] Cycle 1: Start with baseline config
    - [ ] Cycle 2-N: Start with previous cycle's optimal config
  - [ ] Method: `initialize_logging()` - sets up simulation logging

#### 6.2 Main Entry Point
- [ ] **run_simulation.py** (simulation/run_simulation.py)
  - [ ] Parse command line args (--runs, --threads, --simulations-per-config)
  - [ ] Initialize SimulationManager
  - [ ] Run optimization cycles
  - [ ] Print final results

#### 6.3 Integration Testing
- [ ] **test_SimulationManager.py**
  - [ ] Test single optimization cycle completes
  - [ ] Test config improvement across cycles (cycle 2 uses cycle 1 optimal)
  - [ ] Test JSON output format and file naming
  - [ ] Test logging output

- [ ] **End-to-End Integration Test**
  - [ ] Run small-scale test: 2 parameters, 3 values each = 9 configs, 5 sims per config
  - [ ] Verify: 45 total leagues simulated
  - [ ] Verify: Optimal config identified and saved
  - [ ] Verify: Progress tracking accurate
  - [ ] Verify: Results deterministic with same seed

### Phase 7: Optimization & Documentation
Final refinements, performance optimization, and documentation.

#### 7.1 Performance Optimization
- [ ] Profile simulation performance (identify bottlenecks)
- [ ] Optimize PlayerManager CSV loading (cache if safe)
- [ ] Optimize draft logic (reduce redundant calculations)
- [ ] Consider configuration reduction strategies for future (discussed with user)

#### 7.2 Documentation
- [ ] Update simulation/README.md with:
  - [ ] Architecture overview (classes and their roles)
  - [ ] How to run simulations (commands and parameters)
  - [ ] How to interpret results
  - [ ] Configuration parameter explanations
- [ ] Add docstrings to all classes and methods
- [ ] Create example simulation output files

#### 7.3 Error Handling & Robustness
- [ ] Add try-except blocks for file I/O operations
- [ ] Add validation for CSV data integrity
- [ ] Add validation for configuration parameters (bounds checking)
- [ ] Add resume capability (checkpoint progress to recover from crashes)

---

## 📊 Implementation Summary

### Key Numbers:
- **Parameters varied**: 6 (NORMALIZATION_MAX_SCALE, BASE_BYE_PENALTY, PRIMARY_BONUS, SECONDARY_BONUS, POSITIVE_MULT, NEGATIVE_MULT)
- **Values per parameter**: 6 (baseline + 5 random)
- **Total configurations**: 6^6 = 46,656
- **Simulations per config**: 100 leagues
- **Total leagues per run**: 4,665,600
- **Weeks per league**: 17
- **Games per league**: ~170 (10 teams × 17 weeks / 2)

### Architecture:
- **DraftHelperTeam**: Uses AddToRosterMode + StarterHelper (our system under test)
- **SimulatedOpponent**: Uses strategy-based drafting + simple projected-points lineup setting
- **SimulatedLeague**: Manages 10 teams through draft + 17-week season
- **ConfigGenerator**: Creates all parameter combinations
- **ResultsManager**: Tracks performance, identifies optimal config
- **ParallelLeagueRunner**: Parallelizes league simulations
- **SimulationManager**: Orchestrates full optimization cycles

### Testing Strategy:
1. Unit test each component individually
2. Manual single-league validation
3. Small-scale integration test (9 configs, 5 sims each)
4. Full-scale production run (46,656 configs, 100 sims each)

---

## 🚀 Getting Started

**Current Status**: Phase 1 - Core Data Structures (Not Started)

**Next Steps**:
1. Implement DraftHelperTeam class with draft and lineup logic
2. Implement SimulatedOpponent with strategy-based drafting
3. Create unit tests for both team classes
4. Implement Week class and round-robin scheduler
5. Implement SimulatedLeague to tie it all together

**Estimated Timeline** (with testing):
- Phase 1: 2-3 days (core classes + tests)
- Phase 2: 1 day (config generation)
- Phase 3: 1 day (manual simulation validation)
- Phase 4: 1 day (performance tracking)
- Phase 5: 1-2 days (parallelization)
- Phase 6: 1 day (full automation)
- Phase 7: 1 day (optimization + docs)

**Total**: ~8-10 days of development + testing
