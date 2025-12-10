# Documentation Feature - Requirements Checklist

> **IMPORTANT**: When marking items as resolved, also update `documentation_specs.md`
> with full implementation details. The checklist tracks status; the specs file is
> the implementation specification.

---

## General Decisions

- [x] **Level of verification depth:** How thoroughly should we verify existing docs?
  - **RESOLVED:** Option B - Line-by-line verification with targeted updates
  - Focus on fixing known issues identified during investigation

- [x] **QUICK_START_GUIDE scope:** What level of detail?
  - **RESOLVED:** Option B - Moderate (3-5 pages)
  - Covers seasonal workflow with commands, references README for details

---

## README.md Questions

- [x] **Missing scripts:** Verify these scripts need to be added:
  - `run_schedule_fetcher.py` - **ADD** - Fetches NFL schedule → `data/season_schedule.csv`
  - `run_game_data_fetcher.py` - **ADD** - Fetches game/weather data → `data/game_data.csv`
  - `run_draft_order_loop.py` - **ADD** - Loops through draft order strategies

- [x] **Missing component:** Chrome extension
  - `nfl-fantasy-exporter-extension/` - **ADD** - Extracts player ownership from NFL Fantasy

- [x] **Project structure accuracy:** Does the tree diagram reflect current state?
  - **RESOLVED:** NO - needs updates for missing scripts, extension, data files

- [x] **Test count:** Is "1,811 tests" still accurate?
  - **RESOLVED:** NO - actual count is 2,255 tests across 70 test files

- [x] **Incorrect paths:** Fix these paths
  - `docs/scoring/` → `docs/scoring_v2/`
  - `drafted_players.csv` → `drafted_data.csv`
  - `teams_week_N.csv` → `team_data/*.csv` (folder structure)

- [x] **Feature descriptions:** Are all mode descriptions accurate?
  - **RESOLVED:** YES - 4 modes correctly documented

---

## ARCHITECTURE.md Questions

- [x] **Class diagrams accuracy:** Do ASCII diagrams match current code structure?
  - **RESOLVED:** Generally accurate, need to add 3 new managers

- [x] **Missing managers:** Add these to documentation
  - `GameDataManager`
  - `SeasonScheduleManager`
  - `ProjectedPointsManager`

- [x] **Data flow accuracy:** Are data flow descriptions current?
  - **RESOLVED:** Yes, core flows still accurate

- [x] **Extension points:** Are extension point examples still valid?
  - **RESOLVED:** Yes, still valid

- [x] **Configuration schema:** Does JSON schema example match actual config?
  - **RESOLVED:** Needs verification during implementation

---

## QUICK_START_GUIDE.md Questions

- [x] **Target audience:** Who is this guide for?
  - **RESOLVED:** Fantasy football users wanting to use the tools

- [x] **Seasonal phases:** What phases should be covered?
  - **RESOLVED:** All four phases:
    1. Pre-Season Setup
    2. Draft Day
    3. Weekly In-Season
    4. End of Season (brief)

- [x] **Command examples:** Should we include exact command examples?
  - **RESOLVED:** YES - include exact `python run_*.py` commands

- [x] **Screenshots/output examples:** Should we include sample outputs?
  - **RESOLVED:** NO - keep concise, users will see real output

---

## Edge Cases

- [x] **Deprecated features:** Are there any features documented that no longer exist?
  - **RESOLVED:** None found

- [x] **Undocumented features:** Are there features that exist but aren't documented?
  - **RESOLVED:** YES - Chrome extension, 3 scripts, 3 managers, data files

---

## Testing & Validation

- [x] **How to validate documentation accuracy?**
  - **RESOLVED:** Manual review during implementation, verify paths/counts match

---

## Data Source Summary

| Data | Source | Status |
|------|--------|--------|
| README content | `README.md` file | Audited |
| ARCHITECTURE content | `ARCHITECTURE.md` file | Audited |
| Script inventory | Glob for `run_*.py` + reading scripts | Complete |
| Test count | `find tests -name "test_*.py"` + grep | Complete (2,255) |
| Data files | `ls data/` | Complete |
| Chrome extension | `nfl-fantasy-exporter-extension/README.md` | Read |
| User requirements | `documentation_notes.txt` | Read |

---

## Resolution Log

| Item | Resolution | Date |
|------|------------|------|
| Folder structure | Created `feature-updates/documentation/` | Today |
| Notes moved | `documentation.txt` → `documentation_notes.txt` | Today |
| Initial investigation | README, ARCH, scripts analyzed | Today |
| Test count verified | 2,255 tests (not 1,811) | Today |
| Missing scripts identified | 3 scripts undocumented | Today |
| Chrome extension found | `nfl-fantasy-exporter-extension/` undocumented | Today |
| Path errors found | 3 incorrect paths in README | Today |
| All questions answered | See specs.md for proposed answers | Today |
