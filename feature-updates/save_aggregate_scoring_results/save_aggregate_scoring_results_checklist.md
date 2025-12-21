# Save Aggregate Scoring Results - Requirements Checklist

> **IMPORTANT**: When marking items as resolved, also update `save_aggregate_scoring_results_specs.md`
> with full implementation details. The checklist tracks status; the specs file is
> the implementation specification.

---

## Progress Summary

**Total Items:** (To be counted after Phase 2 investigation)
**Resolved:** 0
**Pending:** (All items - to be populated in Phase 2)

---

## General Decisions

- [ ] **Architecture Approach:** Should this be a full mode manager (like AddToRosterMode) or simpler utility?
- [ ] **Menu Integration Pattern:** What's the exact pattern for adding top-level menu items?
- [ ] **Error Handling Strategy:** Fail fast vs. graceful degradation for missing files/folders?

---

## Menu System Integration

- [ ] **Menu Definition Location:** Where are top-level menu options defined in LeagueHelperManager?
- [ ] **Mode Dispatch Mechanism:** How does LeagueHelperManager route to mode managers?
- [ ] **Menu Option Label:** Confirm exact text "Save Calculated Projected Points" or adjust?
- [ ] **Return Behavior:** How do modes return control to main menu?
- [ ] **Menu Order:** Where should new option appear in the menu list?

---

## Scoring Logic

- [ ] **StarterHelper Scoring Method:** What exact method/class does StarterHelper use?
- [ ] **Scoring Parameters:** What parameters does StarterHelper pass to the scoring method?
- [ ] **Weekly vs Season-Long:** How does StarterHelper handle the weekly vs season-long distinction?
- [ ] **Scoring Initialization:** What setup is required before calling scoring (e.g., max_weekly_projection)?
- [ ] **Player Loading:** How to get all available players for scoring?
- [ ] **Player Filtering:** Should all players be scored, or only active/available players?

---

## Data Files & Historical Data

### Files to Copy

- [ ] **File List:** What files does player-data-fetcher currently copy to historical_data?
  - [ ] players.csv?
  - [ ] teams_week_N.csv?
  - [ ] league_config.json?
  - [ ] Other files?
- [ ] **Copy Method:** Use shutil.copy, or custom logic?
- [ ] **Overwrite Behavior:** What if files already exist in historical_data destination?

### Folder Structure

- [ ] **Season Determination:** How to get current SEASON value?
- [ ] **Week Determination:** How to get current WEEK value?
- [ ] **Folder Creation:** Should we create historical_data/{SEASON}/{WEEK} if it doesn't exist?
- [ ] **Week 0 Handling:** Confirm path for season-long is data/historical_data/{SEASON}/calculated_season_long_projected_points.json

### JSON Output

- [ ] **Player ID Format:** What format are player IDs (string, int)?
- [ ] **Score Precision:** How many decimal places for calculated scores?
- [ ] **JSON Structure:** Confirm simple flat dict {player_id: score} is sufficient
- [ ] **Empty Results:** What if no players are available to score?

---

## Error Handling & Edge Cases

- [ ] **Missing historical_data Folder:** Create automatically or error?
- [ ] **Missing Source Files:** Skip file copying or abort entirely?
- [ ] **Week > 17:** How to handle playoff weeks or off-season?
- [ ] **Empty players.csv:** Error and abort, or save empty JSON?
- [ ] **Malformed Data:** Validation strategy for input data?
- [ ] **File Write Failures:** How to handle permission errors or disk full?

---

## Architecture & Code Organization

- [ ] **New Mode Location:** Where should the new mode manager class be created?
  - Option A: `league_helper/save_scoring_mode/SaveScoringModeManager.py`
  - Option B: `league_helper/SaveScoringManager.py` (top level)
  - Option C: Add as method to LeagueHelperManager (no separate class)
- [ ] **Class Name:** SaveScoringModeManager? SaveCalculatedPointsManager? Other?
- [ ] **Inheritance:** Should it inherit from a base mode class?

---

## Testing & Validation

- [ ] **Unit Tests:** What aspects need unit test coverage?
- [ ] **Integration Tests:** How to test end-to-end (menu selection → file creation)?
- [ ] **Test Data:** Need fixture data for testing?
- [ ] **Verification:** How to verify JSON output is correct?

---

## Data Source Summary

| Data | Source | Status |
|------|--------|--------|
| Player data | players.csv via PlayerManager | Pending verification |
| Scoring method | StarterHelper scoring logic | Pending identification |
| Current week | ConfigManager | Pending verification |
| Current season | ConfigManager or elsewhere? | Pending |
| Files to copy | player-data-fetcher reference | Pending research |

---

## Resolution Log

| Item | Resolution | Date |
|------|------------|------|
| (To be populated as items are resolved) | | |

---

## Notes for Phase 2 Investigation

This checklist will be populated with detailed questions during Phase 2 investigation. The agent will:
1. Research the codebase to understand menu patterns
2. Identify StarterHelper scoring implementation details
3. Discover what player-data-fetcher copies to historical_data
4. Add specific questions about implementation approaches
5. Perform THREE-ITERATION question generation to ensure completeness
6. Run CODEBASE VERIFICATION rounds to answer questions from code where possible
