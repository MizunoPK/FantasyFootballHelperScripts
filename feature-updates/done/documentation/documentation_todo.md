# Documentation Feature - Implementation TODO

## Progress Tracker

| Phase | Status |
|-------|--------|
| TODO Creation | In Progress |
| Verification | Pending |
| README.md Updates | Pending |
| ARCHITECTURE.md Updates | Pending |
| QUICK_START_GUIDE.md Creation | Pending |
| QC Review | Pending |

**Current Step:** Creating TODO from specs

---

## Verification Summary

- **Source:** `documentation_specs.md` (approved)
- **Requirements identified:** 3 documents to update/create
- **Specific changes mapped:** See phases below

---

## Phase 1: README.md Updates

### Task 1.1: Fix Test Count
- **File:** `README.md`
- **Change:** Update "1,811 tests" → "2,255 tests (70 test files)"
- **Locations:** Search for "1,811" or "1811"
- **Status:** [ ] Not started

### Task 1.2: Add Missing Scripts
- **File:** `README.md`
- **Scripts to add:**
  - `run_schedule_fetcher.py` - Fetches NFL schedule → `data/season_schedule.csv`
  - `run_game_data_fetcher.py` - Fetches game/weather data → `data/game_data.csv`
  - `run_draft_order_loop.py` - Loops through draft order strategies for optimization
- **Section:** Data Fetchers / Simulation sections
- **Status:** [ ] Not started

### Task 1.3: Add Chrome Extension Documentation
- **File:** `README.md`
- **Component:** `nfl-fantasy-exporter-extension/`
- **Description:** Chrome extension to extract player ownership from NFL Fantasy
- **Section:** New section or under "Data Collection"
- **Status:** [ ] Not started

### Task 1.4: Fix Incorrect Paths
- **File:** `README.md`
- **Changes:**
  - `docs/scoring/` → `docs/scoring_v2/`
  - `drafted_players.csv` → `drafted_data.csv`
  - `teams_week_N.csv` → `team_data/*.csv` (per-team files in folder)
- **Status:** [ ] Not started

### Task 1.5: Update Data Files Section
- **File:** `README.md`
- **Add missing files:**
  - `data/configs/` - Configuration folder
  - `data/game_data.csv` - Game data with weather
  - `data/players_projected.csv` - Projected player data
  - `data/historical_data/` - Historical data archive
- **Status:** [ ] Not started

### Task 1.6: Update Project Structure Tree
- **File:** `README.md`
- **Update:** Tree diagram to reflect current state
- **Status:** [ ] Not started

---

## Phase 2: ARCHITECTURE.md Updates

### Task 2.1: Add Missing Managers
- **File:** `ARCHITECTURE.md`
- **Managers to add:**
  - `GameDataManager` - Manages game data including weather
  - `SeasonScheduleManager` - Manages NFL season schedule
  - `ProjectedPointsManager` - Manages projected points data
- **Section:** Component Architecture / Manager Hierarchy
- **Status:** [ ] Not started

### Task 2.2: Update Test Count
- **File:** `ARCHITECTURE.md`
- **Change:** Update test count references to 2,255
- **Status:** [ ] Not started

### Task 2.3: Verify Data Flow Diagrams (Quick Check)
- **File:** `ARCHITECTURE.md`
- **Action:** Spot-check core diagrams are still accurate
- **Status:** [ ] Not started

---

## Phase 3: Create QUICK_START_GUIDE.md

### Task 3.1: Create File with Structure
- **File:** `QUICK_START_GUIDE.md` (new file in root)
- **Sections:**
  1. Overview (1 paragraph)
  2. Pre-Season Setup
  3. Draft Day
  4. Weekly In-Season
  5. Reference (script quick reference)
- **Status:** [ ] Not started

### Task 3.2: Write Pre-Season Section
- **Content:**
  - Installation (pip install)
  - Fetch player data (`run_player_fetcher.py`)
  - Fetch schedule/game data
  - Optional: Run simulations
- **Status:** [ ] Not started

### Task 3.3: Write Draft Day Section
- **Content:**
  - Run league helper (`run_league_helper.py`)
  - Use "Add to Roster" mode
  - Follow recommendations
- **Status:** [ ] Not started

### Task 3.4: Write Weekly In-Season Section
- **Content:**
  - Update player/scores data
  - Use "Starter Helper" mode
  - Use "Trade Simulator" mode
- **Status:** [ ] Not started

### Task 3.5: Write Reference Section
- **Content:**
  - All scripts quick reference table
  - Common commands
- **Status:** [ ] Not started

---

## Phase 4: QC Review

### Task 4.1: Run Tests
- **Command:** `python tests/run_all_tests.py`
- **Expected:** 100% pass (documentation changes shouldn't break tests)
- **Status:** [ ] Not started

### Task 4.2: QC Round 1 - Path Verification
- **Check:** All file paths mentioned in docs exist
- **Status:** [ ] Not started

### Task 4.3: QC Round 2 - Completeness Check
- **Check:** All items from specs implemented
- **Status:** [ ] Not started

### Task 4.4: QC Round 3 - Consistency Check
- **Check:** Test counts, script names consistent across docs
- **Status:** [ ] Not started

---

## File Checklist

| File | Action | Status |
|------|--------|--------|
| `README.md` | Update | [ ] |
| `ARCHITECTURE.md` | Update | [ ] |
| `QUICK_START_GUIDE.md` | Create | [ ] |
| `CLAUDE.md` | Check if updates needed | [ ] |

---

## Progress Notes

**Last Updated:** Starting TODO creation
**Current Status:** Step 1 - Creating TODO
**Next Steps:** Verify tasks against specs, then begin implementation
**Blockers:** None
