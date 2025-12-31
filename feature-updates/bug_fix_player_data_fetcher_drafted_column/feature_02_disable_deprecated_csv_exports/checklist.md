# Feature 2: Disable Deprecated CSV File Exports - Planning Checklist

**Purpose:** Track open questions and decisions for this feature

**Instructions:**
- [ ] = Open question (needs user answer)
- [x] = Resolved (answer documented below)

**Status:** Phase 3 in progress - 2 questions resolved, 2 pending

---

## Open Questions

{All questions resolved!}

---

## Resolved Questions

### Question 1: Which Implementation Option? ✅ RESOLVED
- [x] **User's Answer:** Option C - Complete Removal

**User's Response:** "C"

**Implementation Impact:**
- DELETE lines 352-368 in player_data_fetcher_main.py (both export calls)
- DELETE export_to_data() method in player_data_exporter.py (**line 775** - updated from 808 after feature_01)
- DELETE export_projected_points_data() method in player_data_exporter.py (**line 877** - updated from 910 after feature_01)
- DELETE PLAYERS_CSV constant in config.py (**line 37** - updated from 38 after feature_01)
- UPDATE unit tests to verify CSVs NOT created
- Total: ~200 lines removed across 3 files

**[UPDATED based on feature_01 implementation - 2025-12-31]**
Line numbers shifted because feature_01 deleted ~23 lines from player_data_exporter.py (PRESERVE_DRAFTED_VALUES logic)

**Rationale:** Cleanest solution - removes all dead code, no confusion about what's deprecated

**Risk Mitigation:** Will thoroughly test all systems (league helper, simulation) before Stage 6 completion

---

### Question 2: Investigate File References Now or Later? ✅ RESOLVED
- [x] **User's Answer:** Investigate Now (Option A)

**User's Response:** "go ahead and investigate and update the checklist/spec accordingly"

**Investigation Results:**
- **14 files investigated** - See `research/FILE_REFERENCES_INVESTIGATION.md`
- **13 files:** Comments/docstrings/deprecated code only (NO changes needed)
- **1 file requires code change:** SaveCalculatedPointsManager.py

**Key Findings:**
1. **Simulation system NOT affected** - uses historical sim_data snapshots (NOT data/players.csv)
2. **PlayerManager already uses JSON** - deprecated load_players() not called by default
3. **ProjectedPointsManager already deprecated** - class consolidated
4. **SaveCalculatedPointsManager** - needs update to remove players.csv from files_to_copy list

**Implementation Impact:**
- ADD to spec: SaveCalculatedPointsManager.py Component 4
- UPDATE spec: Files Modified Summary (4 files instead of 3)
- UPDATE spec: Overall Risk LOW (down from MEDIUM - no hidden dependencies!)

---

### Question 3: Does Simulation System Depend on CSV Files? ✅ RESOLVED (via investigation)
- [x] **Answer:** NO - Simulation uses historical sim_data snapshots, NOT data/players.csv

**Investigation Finding:**
- Simulation system loads from `sim_data/{year}/weeks/week_NN/players.csv` (historical snapshots)
- These are SEPARATE files from `data/players.csv` (live current data)
- Deleting data/players.csv will NOT affect simulation system
- No code changes needed in simulation/

**Evidence:**
- SimulatedLeague.py line 164: `weeks_folder / "week_01" / "players.csv"` (within sim_data structure)
- SimulationManager.py validates sim_data folder structure with historical weekly snapshots
- All 7 simulation files reference sim_data historical files, NOT data/players.csv

---

### Question 4: Auto-Delete Old CSV Files? ✅ RESOLVED
- [x] **User's Answer:** Option C - Do Nothing

**User's Response:** "C"

**Implementation Impact:**
- No code changes needed for old file cleanup
- Old players.csv and players_projected.csv files will remain in data/ folder if they exist
- Files will become stale (not updated) after CSV exports are disabled
- User can manually delete if desired

**Rationale:** Simplest approach - no additional code, no risk of data loss

---

## Checklist Status

**Total Questions:** 4
**Open:** 0
**Resolved:** 4

**Phase 3 Complete:** All questions resolved

---

## Phase 4: Dynamic Scope Adjustment

**Scope Count (from spec.md Implementation Checklist):**
- High-level tasks: 10
- Estimated detailed items: ~12
- Threshold: 35 items

**Scope Assessment:** ✅ PASS - Well under 35 items, no split needed

**Complexity:** LOW
**Risk:** LOW

---

## Phase 5: Cross-Feature Alignment

**Features to Compare:** Feature 1 (Update Data Models and Field Migration) - Stage 5c complete ✅

**[UPDATED based on feature_01 ACTUAL implementation - 2025-12-31 (Stage 5d)]**

**Alignment Check:**
- Feature 1: Migrated ESPNPlayerData from `drafted: int` to `drafted_by: str` (COMPLETE)
- Feature 2: Disables CSV exports (players.csv, players_projected.csv)
- **Dependency:** ✅ Feature 2 depends on Feature 1 (confirmed and now COMPLETE)
- **Conflicts:** None - Feature 1 touched data models, Feature 2 touches export code
- **Integration:** Clean separation - minor line number shifts only

**Cross-Feature Integration Points:**
- Both touch player-data-fetcher module (different files)
- Both touch config.py (Feature 1 removed PRESERVE_DRAFTED_VALUES, Feature 2 will remove PLAYERS_CSV)
- Both touch player_data_exporter.py (Feature 1 modified conversion logic, Feature 2 will delete export methods)
- Sequential execution required (Feature 1 MUST complete before Feature 2) ✅ SATISFIED

**Line Number Updates from Feature_01:**
- export_to_data(): 808 → **775** (shifted up ~33 lines)
- export_projected_points_data(): 910 → **877** (shifted up ~33 lines)
- PLAYERS_CSV in config.py: 38 → **37** (shifted up 1 line)

**Alignment Status:** ✅ ALIGNED - Minor line number updates only, no algorithm changes, ready for Stage 5a

---

**Next:** Mark Stage 2 complete for Feature 2
