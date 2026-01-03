# Cross-Feature Sanity Check

**Date:** 2026-01-01
**Epic:** integrate_new_player_data_into_simulation
**Features Compared:** 2 features

---

## Comparison Matrix

### Category 1: Data Structures

| Feature | Data Read | File Format | Data Types | Array Structures | Conflicts? |
|---------|-----------|-------------|------------|------------------|------------|
| Feature 1 (Win Rate Sim) | 6 JSON files per week | qb/rb/wr/te/k/dst_data.json | string, boolean, float arrays | projected_points[17], actual_points[17] | ❌ None |
| Feature 2 (Accuracy Sim) | 6 JSON files per week | qb/rb/wr/te/k/dst_data.json | string, boolean, float arrays | projected_points[17], actual_points[17] | ❌ None |

**Analysis:**
- ✅ Both features read SAME 6 JSON files (qb_data.json, rb_data.json, wr_data.json, te_data.json, k_data.json, dst_data.json)
- ✅ Both expect SAME data types (drafted_by: string, locked: boolean, projected_points/actual_points: float arrays)
- ✅ Both expect SAME array structure (17 elements, index 0 = Week 1)
- ✅ Both rely on FantasyPlayer.from_json() for type handling
- **NO CONFLICTS** - Data structure expectations are identical

### Category 2: Interfaces & Dependencies

| Feature | Depends On | Creates Directories | PlayerManager Usage | Return Types Expected | Conflicts? |
|---------|-----------|---------------------|---------------------|----------------------|------------|
| Feature 1 | PlayerManager, ConfigManager, SeasonScheduleManager, TeamDataManager | shared_dir/player_data/ | Load all players at simulation start | List[FantasyPlayer] | ❌ None |
| Feature 2 | PlayerManager, ConfigManager, SeasonScheduleManager, TeamDataManager | temp_dir/player_data/ | Load per config evaluation | List[FantasyPlayer] | ❌ None |

**Analysis:**
- ✅ Both features use SAME dependencies (PlayerManager, ConfigManager, SeasonScheduleManager, TeamDataManager)
- ✅ Both features call PlayerManager with SAME directory structure requirement (player_data/ subfolder)
- ✅ Both features expect PlayerManager to return List[FantasyPlayer]
- ✅ Directory naming differs intentionally (shared_dir vs temp_dir) - this is by design, not a conflict
  - Feature 1: Shared directory reused across iterations (performance)
  - Feature 2: Temp directory created per evaluation (isolation)
- ✅ Both features call PlayerManager() instantiation the SAME way
- **NO CONFLICTS** - Interface and dependency usage is consistent

### Category 3: File Locations & Naming

| Feature | Reads From | Creates Temp Dirs | Folder Structure | Naming Conventions | Conflicts? |
|---------|-----------|-------------------|------------------|-------------------|------------|
| Feature 1 | simulation/sim_data/{year}/weeks/week_{N:02d}/ | shared_dir/player_data/ | Shared across simulation | 6 position files | ❌ None |
| Feature 2 | simulation/sim_data/{year}/weeks/week_{N:02d}/ | temp_dir/player_data/ | New temp per config | 6 position files | ❌ None |

**Analysis:**
- ✅ Both features read from SAME source location (simulation/sim_data/{year}/weeks/week_{N:02d}/)
- ✅ Both features use SAME file naming (qb_data.json, rb_data.json, wr_data.json, te_data.json, k_data.json, dst_data.json)
- ✅ Both features create player_data/ subdirectory (REQUIRED by PlayerManager)
- ✅ Temp directory lifetimes differ (intentional by design):
  - Feature 1: Shared directory lives for entire simulation (many iterations)
  - Feature 2: Temp directory lives for single config evaluation
- ✅ Both features copy season-level files (season_schedule.csv, game_data.csv, team_data/)
- **NO CONFLICTS** - File locations and naming are consistent

### Category 4: Configuration Keys

| Feature | Config Keys Used | Config File | Key Conflicts? | Conflicts? |
|---------|------------------|-------------|----------------|------------|
| Feature 1 | league_config.json keys | Reads existing config | No new keys added | ❌ None |
| Feature 2 | league_config.json keys | Reads existing config | No new keys added | ❌ None |

**Analysis:**
- ✅ Both features use SAME config file (league_config.json)
- ✅ NEITHER feature adds NEW config keys (pure data format migration)
- ✅ Both features read existing league configuration
- ✅ Both features create temp config files with same structure
- **NO CONFLICTS** - No configuration key additions or changes

### Category 5: Algorithms & Logic

| Feature | Data Loading Pattern | Caching Strategy | Week Extraction | Order Dependencies | Conflicts? |
|---------|---------------------|------------------|-----------------|-------------------|------------|
| Feature 1 | Pre-load all 17 weeks | Cache week data in dict | Extract week N from arrays[N-1] | Must parse JSON → extract week data | ❌ None |
| Feature 2 | Load 1 week on-demand | No caching | PlayerManager handles arrays | Just copy files, PlayerManager extracts | ❌ None |

**Analysis:**
- ✅ Different data loading patterns are INTENTIONAL (documented in both specs):
  - Feature 1: Pre-loads/caches all 17 weeks (Win Rate Sim runs thousands of iterations → performance critical)
  - Feature 2: Loads on-demand per config (Accuracy Sim runs once per config → caching adds overhead)
- ✅ Both use SAME array indexing (week_num - 1 to get index)
- ✅ Week extraction differs by design (both correct):
  - Feature 1: Needs _parse_players_json() to extract week-specific values (projected_points[week_num-1])
  - Feature 2: PlayerManager handles array extraction (no parsing method needed)
- ✅ Both features maintain SAME simulation functionality (just different data source)
- **NO CONFLICTS** - Algorithm differences are intentional and documented

### Category 6: Testing Assumptions

| Feature | Test Data Needs | Mock Dependencies | Integration Points | Testing Scope | Conflicts? |
|---------|----------------|-------------------|-------------------|---------------|------------|
| Feature 1 | JSON files with 17-element arrays | None (uses real data files) | SimulatedLeague integration | Full simulation runs | ❌ None |
| Feature 2 | JSON files with 17-element arrays | None (uses real data files) | AccuracyCalculator integration | Per-config accuracy evals | ❌ None |

**Analysis:**
- ✅ Both features use SAME test data (JSON files in simulation/sim_data/)
- ✅ Both features use real data files (no mocking needed for JSON structure)
- ✅ Integration points are DIFFERENT (as expected):
  - Feature 1: SimulatedLeague, DraftHelperTeam, SimulatedOpponent
  - Feature 2: AccuracyCalculator, AccuracyResultsManager
- ✅ NO SHARED integration points (features operate independently)
- ✅ Both features can be tested in parallel (no interdependencies)
- ✅ Epic smoke test will validate both simulations work with JSON
- **NO CONFLICTS** - Testing assumptions are clear and separate

---

## Conflicts Identified

**Total Conflicts Found:** 0

After systematic comparison across all 6 categories, NO conflicts were identified.

**Category Results:**
1. ✅ Data Structures - No conflicts (identical expectations)
2. ✅ Interfaces & Dependencies - No conflicts (consistent usage)
3. ✅ File Locations & Naming - No conflicts (same source locations)
4. ✅ Configuration Keys - No conflicts (no new keys added)
5. ✅ Algorithms & Logic - No conflicts (differences are intentional)
6. ✅ Testing Assumptions - No conflicts (separate integration points)

**Key Findings:**
- Both features read from SAME data source (simulation/sim_data/{year}/weeks/)
- Both features use SAME file format (6 JSON files per week)
- Both features have SAME data structure expectations (17-element arrays)
- Both features require SAME directory structure (player_data/ subfolder)
- Both features use SAME dependencies (PlayerManager, ConfigManager, etc.)

**Intentional Differences (by design, documented in specs):**
- Feature 1: Pre-loads/caches all weeks (performance for thousands of iterations)
- Feature 2: Loads on-demand per config (simplicity for single evaluations)
- Feature 1: Needs JSON parsing method (_parse_players_json)
- Feature 2: No parsing needed (PlayerManager handles it)
- Feature 1: Shared directory across simulation
- Feature 2: Temp directory per config evaluation

**Why differences are NOT conflicts:**
- Both specs explicitly document WHY approaches differ
- Different use cases justify different implementations
- No shared code between features (operate independently)
- Both maintain same simulation functionality (just different data source)

---

## Resolutions Applied

**No resolutions needed** - Zero conflicts identified.

All features are aligned and conflict-free.

---

## Final Status

**Conflicts Identified:** 0
**Conflicts Resolved:** 0 (none needed)
**Unresolved Conflicts:** 0

✅ **All features aligned and conflict-free**

**Ready for user sign-off**

**Status:** Step 2 complete (Systematic Comparison)
