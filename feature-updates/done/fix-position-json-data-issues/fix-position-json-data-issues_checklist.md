# Fix Position JSON Data Issues - Planning Checklist

This file tracks all open questions and decisions that need to be resolved before implementation.

---

## Checklist Status

**Total Items:** 28
**Resolved:** 28 (23 via codebase verification + 5 via user decision)
**Pending:** 0 - ✅ ALL QUESTIONS RESOLVED

---

## Categories

### Issue #1: File Naming Questions

#### Q1.1: File Saving Approach
- [x] **How should files be written without timestamps?**
  - **Resolution:** Write files directly using Python's `open()` with fixed filenames
  - **Source:** Codebase verification - DataFileManager always adds timestamps
  - **Code:** utils/data_file_manager.py:237-258 (generate_timestamped_filename always adds timestamp)
  - **Rationale:** Simpler than modifying DataFileManager; matches pattern of other output files

#### Q1.2: File Caps Configuration
- [x] **Should file caps for position JSON be disabled?**
  - **Resolution:** No caps needed - reuse players.csv write pattern
  - **Source:** User decision + codebase verification
  - **Code:** Follow same pattern as players.csv export (player_data_exporter.py:678-708)
  - **Rationale:** Direct file write like players.csv - no timestamps, no accumulation, no caps needed

#### Q1.3: File Location
- [x] **Where should position JSON files be written?**
  - **Resolution:** `data/` folder (root data folder, same as players.csv)
  - **Source:** User decision - corrected from initial incorrect assumption
  - **Code:** Path pattern: `Path(__file__).parent / '../data/{position}_data.json'`
  - **Files:** `data/qb_data.json`, `data/rb_data.json`, `data/wr_data.json`, `data/te_data.json`, `data/k_data.json`, `data/dst_data.json`
  - **Rationale:** Consistent with other output files (players.csv, team_data/*.csv)

---

### Issue #2: Projected Points Questions

#### Q2.1: Data Source Access Method
- [x] **How to access statSourceId=1 (projected) vs statSourceId=0 (actual)?**
  - **Resolution:** Use existing `_extract_raw_espn_week_points()` method with `source_type` parameter
  - **Source:** Codebase verification - espn_client.py:429-555
  - **Code:** `_extract_raw_espn_week_points(player_data, week, position, 'projection')` for statSourceId=1
  - **Code:** `_extract_raw_espn_week_points(player_data, week, position, 'actual')` for statSourceId=0
  - **Rationale:** Method already exists and handles both data sources correctly

#### Q2.2: ESPN Data Object Availability
- [x] **Is raw ESPN player_info dict available in player_data_exporter.py?**
  - **Resolution:** No, only ESPNPlayerData object is available
  - **Source:** Codebase verification - player_data_exporter.py:525-578
  - **Code:** Methods receive `ESPNPlayerData` object, not raw ESPN dict
  - **Problem:** Need access to raw `player_info` dict with `stats` array
  - **Solution Required:** Pass raw player_info dict to export methods OR store it in ESPNPlayerData

#### Q2.3: Player Info Dict Storage
- [x] **Should raw player_info dict be stored in ESPNPlayerData model?**
  - **Resolution:** Store only stats array in ESPNPlayerData (Option C)
  - **Source:** User decision (2024-12-24)
  - **Implementation:** Add `raw_stats: Optional[List[Dict[str, Any]]] = None` field to ESPNPlayerData
  - **Code Change:** In `espn_client.py` parsing, populate: `raw_stats=player_info.get('stats', [])`
  - **Rationale:** Minimal memory overhead, no signature changes, stores only what's needed

#### Q2.4: Projected Weeks Usage
- [x] **Can projected_weeks dict be used for projected_points array?**
  - **Resolution:** Yes, but only for statSourceId=1 data
  - **Source:** Codebase verification - player_data_models.py:114-124
  - **Code:** `projected_weeks: Dict[int, float]` stores statSourceId=1 projections
  - **Code:** `get_week_projected(week)` method already exists
  - **Rationale:** This dict already contains pre-game projections we need

#### Q2.5: Fantasy Points Extraction Method
- [x] **How to extract projected vs actual fantasy points from ESPN API?**
  - **Resolution:** Extract from BOTH statSourceId entries, both use `appliedTotal`
  - **Source:** Codebase verification - compile_historical_data pattern (player_data_fetcher.py:424-463)
  - **Pattern:**
    ```python
    for stat in stats:
        if stat.get('scoringPeriodId') == week:
            if stat.get('statSourceId') == 0:  # Actual
                actual_points = stat.get('appliedTotal')
            elif stat.get('statSourceId') == 1:  # Projected
                projected_points = stat.get('appliedTotal')
    ```
  - **Key Insight:** TWO stat entries per week (statSourceId=0 and statSourceId=1), BOTH use `appliedTotal`
  - **Rationale:** This is the correct ESPN API pattern, not a choice between calculation methods

---

### Issue #3: Stat Arrays Questions

#### Q3.1: Stats Array Access
- [x] **Where are individual stat values stored in ESPN API response?**
  - **Resolution:** `stats[week].appliedStats` dictionary with string keys
  - **Source:** Codebase verification - espn_client.py:473-517
  - **Code:** `stat.get('appliedStats')` dict contains stat_0, stat_1, etc. as string keys
  - **Example:** `appliedStats['3']` = passing yards value
  - **Rationale:** ESPN API structure confirmed in working code

#### Q3.2: Stat Extraction Helper Method
- [x] **Does a helper method exist for extracting stat values from appliedStats?**
  - **Resolution:** No dedicated helper, but pattern exists in espn_client.py and compile_historical_data
  - **Source:** Codebase verification - espn_client.py:473-517, player_data_fetcher.py:424-463
  - **Code:** Direct dict access: `stat.get('appliedStats', {}).get('3', 0.0)`
  - **Need:** Create helper method to extract stat values for all 17 weeks
  - **Pattern:** Extract from statSourceId=0 entry for actual stats
  - **Rationale:** Will need to build stat extraction utility following compile_historical_data pattern

#### Q3.3: Stat ID Data Type
- [x] **Are stat IDs stored as integers or strings in appliedStats dict?**
  - **Resolution:** Strings (e.g., '0', '1', '3', not 0, 1, 3)
  - **Source:** Codebase verification - espn_client.py:500-517
  - **Code:** `appliedStats` uses string keys based on API structure
  - **Rationale:** Must use string keys when accessing stat values

#### Q3.4: Missing Stat Handling
- [x] **How should missing stats be handled (bye weeks, future weeks, no data)?**
  - **Resolution:** Return 0.0 for missing stats
  - **Source:** Codebase verification - Current implementation pattern
  - **Code:** player_data_exporter.py:585-669 (all TODOs return [0.0] * 17)
  - **Rationale:** Consistent with existing approach

#### Q3.5: Stat Value Data Type
- [x] **What data type are stat values (int vs float)?**
  - **Resolution:** Float (ESPN API returns floats)
  - **Source:** Codebase verification - espn_client.py:502
  - **Code:** `points = float(stat['appliedTotal'])` - explicit float conversion
  - **Rationale:** All ESPN stat values should be treated as floats

#### Q3.6: Two-Point Conversion Calculation
- [x] **How to combine multiple 2PT stat IDs (19, 26, 44, 62)?**
  - **Resolution:** Remove two_pt field entirely from JSON output
  - **Source:** User decision (2024-12-24)
  - **Rationale:** Not important enough to justify the complexity of aggregating 4 different stat IDs
  - **Implementation:** Remove "two_pt" field from misc stats dict in all positions

#### Q3.7: Return Stats Calculation
- [x] **How to combine kickoff (114) and punt (115) return yards?**
  - **Resolution:** Simple addition: stat_114 + stat_115
  - **Source:** Research document - FINAL_STAT_RESEARCH_COMPLETE.md:286-296
  - **Code Example:** `kr_yds + pr_yds`
  - **Rationale:** Documented algorithm from original research

#### Q3.9: Individual Stat Extraction Source (NEW)
- [x] **Which statSourceId should be used for individual stat arrays (passing_yds, rushing_tds, etc.)?**
  - **Resolution:** Use statSourceId=0 (actual stats only)
  - **Source:** Codebase verification + logic analysis
  - **Code Pattern:**
    ```python
    # Find stat entry with statSourceId=0 for this week
    for stat in raw_stats:
        if stat.get('scoringPeriodId') == week and stat.get('statSourceId') == 0:
            applied_stats = stat.get('appliedStats', {})
            passing_yards = float(applied_stats.get('3', 0.0))  # stat_3
    ```
  - **Rationale:** Individual stats are actual game stats (what happened), not projections
  - **Note:** Projected points use statSourceId=1, but stat detail arrays use statSourceId=0 only

#### Q3.8: Defense TD Calculation
- [x] **Use stat_94 directly OR calculate from stat_103 + stat_104?**
  - **Resolution:** Use stat_94 (defensiveTouchdowns) directly (Option A)
  - **Source:** User decision (2024-12-24)
  - **Implementation:** `def_td = self._extract_stat_value(raw_stats, week, '94')`
  - **Rationale:** Simpler, single stat lookup, ESPN's official total value

---

### Issue #4: Implementation Architecture Questions

#### Q4.1: ESPN Player Info Access
- [x] **How to pass player_info dict to position JSON export?**
  - **Resolution:** Same as Q2.3 - Store stats array in ESPNPlayerData.raw_stats
  - **Source:** User decision (2024-12-24)
  - **Implementation:** Add `raw_stats` field to model, populate during parsing
  - **Rationale:** Resolves both Q2.3 and Q4.1 with single architectural decision

#### Q4.2: Stat Extraction Utility Location
- [x] **Where should stat extraction helper methods be located?**
  - **Resolution:** In player_data_exporter.py as private methods
  - **Source:** Architecture analysis
  - **Rationale:** Only used by position JSON export, keep methods private to class
  - **Methods Needed:**
    - `_extract_stat_value(stats_array, week, stat_id) -> float`
    - `_extract_combined_stat(stats_array, week, stat_ids) -> float`

#### Q4.3: Error Handling Strategy
- [x] **How should errors in stat extraction be handled?**
  - **Resolution:** Log warning and return 0.0 for that stat/week
  - **Source:** Codebase pattern verification
  - **Code:** Similar pattern in fantasy_points_calculator.py:196-198
  - **Rationale:** Don't fail entire export if one stat is missing

#### Q4.4: Performance Considerations
- [x] **Is there a performance concern with iterating all stats for all weeks?**
  - **Resolution:** No, reasonable performance expected
  - **Source:** Architecture analysis
  - **Calculation:** ~500 players × 6 positions × 17 weeks × 30 stats = manageable
  - **Rationale:** Current implementation already iterates similarly

---

### Edge Case Questions

#### Q5.1: Bye Week Handling
- [x] **Should bye weeks show 0 in all stat arrays?**
  - **Resolution:** Yes, 0 for all stats during bye week
  - **Source:** Specs verification - specs.md:94-96
  - **Code Example:** "Week 7 (index 6) = 0 (bye week)"
  - **Rationale:** Explicitly stated in requirements

#### Q5.2: Future Week Handling
- [x] **Should future weeks (Week 17 onwards) show 0 in actual arrays?**
  - **Resolution:** Yes, 0 for actual stats, but may have projected values
  - **Source:** Specs verification - specs.md:96
  - **Code Example:** "Week 17 (index 16) = 0 (not yet played)"
  - **Rationale:** Explicitly stated in requirements

#### Q5.3: Negative DST Points
- [x] **Should negative fantasy points be allowed for DST?**
  - **Resolution:** Yes, DST can have negative points
  - **Source:** Codebase verification - fantasy_points_calculator.py:35
  - **Code:** `include_negative_dst_points: bool = True`
  - **Rationale:** DST scoring allows negative values

#### Q5.4: Incomplete Weeks
- [x] **How to handle weeks in progress (current week)?**
  - **Resolution:** Use actual stats if available, 0 if game not played
  - **Source:** Logic analysis
  - **Rationale:** Current week may have partial data as games complete

---

### Testing & Validation Questions

#### Q6.1: Spot-Check Player Selection
- [x] **Which player should be used for external validation?**
  - **Resolution:** Josh Allen (QB) Week 1
  - **Source:** Specs verification - specs.md:196-203
  - **Rationale:** Explicitly stated in testing requirements

#### Q6.2: Validation Data Source
- [x] **Where to get ground truth data for spot-check validation?**
  - **Resolution:** ESPN.com manually
  - **Source:** Specs verification - specs.md:205-208
  - **URL:** ESPN player game log page
  - **Rationale:** Explicitly stated in testing requirements

#### Q6.3: Test Coverage
- [x] **Which positions must be tested?**
  - **Resolution:** All 6 (QB, RB, WR, TE, K, DST)
  - **Source:** Specs verification - specs.md:210-213
  - **Rationale:** Explicitly stated in success criteria

---

## Resolution Log

### Resolved via Codebase Verification + User Decisions (22 items)

1. **Q1.1: File Saving Approach**
   - **Resolved:** Write files directly with fixed filenames
   - **Evidence:** utils/data_file_manager.py always adds timestamps, simpler to bypass
   - **File:** utils/data_file_manager.py:237-258

2. **Q1.3: File Location**
   - **Resolved:** `data/` folder (corrected from initial assumption)
   - **Evidence:** Reuse players.csv pattern (player_data_exporter.py:678)
   - **File:** player-data-fetcher/player_data_exporter.py:678-708

3. **Q2.1: Data Source Access Method**
   - **Resolved:** Use `_extract_raw_espn_week_points()` with source_type='projection' or 'actual'
   - **Evidence:** Method already exists and handles both statSourceId values
   - **File:** player-data-fetcher/espn_client.py:429-555

4. **Q2.2: ESPN Data Object Availability**
   - **Resolved:** Not available, need to pass it
   - **Evidence:** Export methods only receive ESPNPlayerData object
   - **File:** player-data-fetcher/player_data_exporter.py:525-578

5. **Q2.4: Projected Weeks Usage**
   - **Resolved:** Yes, use projected_weeks dict
   - **Evidence:** Dict already populated with statSourceId=1 data
   - **File:** player-data-fetcher/player_data_models.py:114-124

6. **Q3.1: Stats Array Access**
   - **Resolved:** Via stats[week].appliedStats dict
   - **Evidence:** ESPN client already accesses this structure
   - **File:** player-data-fetcher/espn_client.py:473-517

7. **Q3.2: Stat Extraction Helper Method**
   - **Resolved:** Need to create helper methods
   - **Evidence:** No existing helper, but pattern is clear
   - **File:** player-data-fetcher/espn_client.py:473-517

8. **Q3.3: Stat ID Data Type**
   - **Resolved:** Strings (e.g., '0', '1', '3')
   - **Evidence:** appliedStats uses string keys
   - **File:** player-data-fetcher/espn_client.py:500-517

9. **Q3.4: Missing Stat Handling**
   - **Resolved:** Return 0.0
   - **Evidence:** Current TODO implementation pattern
   - **File:** player-data-fetcher/player_data_exporter.py:585-669

10. **Q3.5: Stat Value Data Type**
    - **Resolved:** Float
    - **Evidence:** ESPN API returns floats
    - **File:** player-data-fetcher/espn_client.py:502

11. **Q3.7: Return Stats Calculation**
    - **Resolved:** Sum stat_114 + stat_115
    - **Evidence:** Documented algorithm
    - **File:** FINAL_STAT_RESEARCH_COMPLETE.md:286-296

12. **Q4.2: Stat Extraction Utility Location**
    - **Resolved:** Private methods in player_data_exporter.py
    - **Evidence:** Architecture best practices
    - **Rationale:** Single-use methods, keep private to class

13. **Q4.3: Error Handling Strategy**
    - **Resolved:** Log warning, return 0.0
    - **Evidence:** Pattern in fantasy_points_calculator.py
    - **File:** player-data-fetcher/fantasy_points_calculator.py:196-198

14. **Q4.4: Performance Considerations**
    - **Resolved:** No concerns
    - **Evidence:** Similar patterns already exist
    - **Rationale:** Reasonable data volume

15. **Q5.1: Bye Week Handling**
    - **Resolved:** 0 for all stats
    - **Evidence:** Specs explicitly state this
    - **File:** specs.md:94-96

16. **Q5.2: Future Week Handling**
    - **Resolved:** 0 for actual, may have projected
    - **Evidence:** Specs explicitly state this
    - **File:** specs.md:96

17. **Q5.3: Negative DST Points**
    - **Resolved:** Yes, allow negative
    - **Evidence:** Config flag set to true
    - **File:** player-data-fetcher/fantasy_points_calculator.py:35

18. **Q5.4: Incomplete Weeks**
    - **Resolved:** Use actual if available, else 0
    - **Evidence:** Logic analysis
    - **Rationale:** Handles partial week data correctly

19. **Q6.1: Spot-Check Player Selection**
    - **Resolved:** Josh Allen Week 1
    - **Evidence:** Specs requirement
    - **File:** specs.md:196-203

20. **Q6.2: Validation Data Source**
    - **Resolved:** ESPN.com manual check
    - **Evidence:** Specs requirement
    - **File:** specs.md:205-208

21. **Q6.3: Test Coverage**
    - **Resolved:** All 6 positions
    - **Evidence:** Specs success criteria
    - **File:** specs.md:210-213

22. **Q1.2: File Caps Configuration**
    - **Resolved:** No caps needed - reuse players.csv pattern
    - **Evidence:** User decision (2024-12-24)
    - **File:** player-data-fetcher/player_data_exporter.py:678-708
    - **Rationale:** Direct file write to data/ folder, files overwrite like players.csv

23. **Q2.3: Player Info Dict Storage**
    - **Resolved:** Store only stats array in ESPNPlayerData (Option C)
    - **Evidence:** User decision (2024-12-24)
    - **Implementation:** Add `raw_stats: Optional[List[Dict[str, Any]]]` field to ESPNPlayerData model
    - **Rationale:** Minimal memory overhead, no method signature changes, stores only what's needed

24. **Q4.1: ESPN Player Info Access**
    - **Resolved:** Same as Q2.3 - use raw_stats field
    - **Evidence:** User decision (2024-12-24)
    - **Rationale:** Single architectural decision resolves both data access questions

25. **Q2.5: Fantasy Points Extraction Method**
    - **Resolved:** Extract from both statSourceId entries, both use appliedTotal
    - **Evidence:** Codebase verification - compile_historical_data pattern
    - **File:** historical_data_compiler/player_data_fetcher.py:424-463
    - **Pattern:** Two stat entries per week (statSourceId=0 for actual, statSourceId=1 for projected)

26. **Q3.9: Individual Stat Extraction Source**
    - **Resolved:** Use statSourceId=0 only for actual stats
    - **Evidence:** Logic analysis + compile_historical_data pattern
    - **Rationale:** Stat detail arrays show what actually happened (actual stats only)

27. **Q3.6: Two-Point Conversion Calculation**
    - **Resolved:** Remove two_pt field entirely
    - **Evidence:** User decision (2024-12-24)
    - **Rationale:** Not worth the complexity of aggregating 4 stat IDs

28. **Q3.8: Defense TD Calculation**
    - **Resolved:** Use stat_94 directly
    - **Evidence:** User decision (2024-12-24)
    - **Rationale:** Simpler than calculating from components, ESPN's official total

---

### Pending User Decisions (0 items)

✅ **ALL QUESTIONS RESOLVED!** Ready to proceed to implementation.

---

## Instructions for Future Agents

1. **During Phase 2 Investigation:** ✅ COMPLETE
2. **During Phase 3:** ✅ COMPLETE - All questions presented and answered
3. **During Phase 4:** ✅ COMPLETE - All resolutions documented
4. **Ready for Implementation:** ✅ ALL 28 items resolved and marked [x]

**Next Step:** Proceed to implementation phase (follow `todo_creation_guide.md`)
