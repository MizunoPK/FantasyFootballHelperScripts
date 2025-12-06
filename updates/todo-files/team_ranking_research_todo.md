# Team Ranking Research - TODO

**Objective**: Research and analyze ESPN API data to improve team ranking accuracy

**Status**: ✅ COMPLETE
**Created**: 2025-11-01
**Last Updated**: 2025-11-01

---

## Overview

Create a comprehensive analysis report on ESPN API data available for calculating team rankings. The report should evaluate current ranking methodology and propose improvements for more accurate team rankings in `teams.csv`.

**Current Issue**: Team ranking values (offensive_rank, defensive_rank, def_vs_*_rank) may not properly represent actual team rankings.

**Deliverable**: Research report in `docs/team_rankings/` folder analyzing ESPN API data and ranking calculation methods.

---

## DRAFT TODO - Before Verification

### Phase 1: Understand Current Implementation
- [x] **Task 1.1**: Read ESPN documentation in `docs/espn/`
- [x] **Task 1.2**: Analyze current team ranking generation in `player-data-fetcher/espn_client.py`
- [x] **Task 1.3**: Review current teams.csv structure and columns
- [x] **Task 1.4**: Document current ranking calculation methodology
  - **Offensive Rank**: Based on `totalPointsPerGame` (ESPN team stats API)
    - Endpoint: `https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{team_id}/statistics`
    - Method: `_calculate_team_rankings_for_season()` at lines 785-854
    - Ranks teams 1-32 by PPG (higher PPG = better rank)
  - **Defensive Rank**: Based on `totalTakeaways` (ESPN team stats API)
    - Same endpoint as offensive rank
    - Ranks teams 1-32 by takeaways (more takeaways = better rank)
  - **Position-Specific Defense Rankings**: Calculated internally from player performance
    - Method: `_calculate_position_defense_rankings()` at lines 1017-1097
    - Sums fantasy points allowed by each defense to each position (QB/RB/WR/TE/K)
    - Only uses actual game data (weeks 1 to current_week-1)
    - Ranks 1-32 where lower points allowed = better rank
    - **NOT** from ESPN API - calculated from player game stats

### Phase 2: Analyze ESPN API Data Sources ✅ COMPLETE
- [x] **Task 2.1**: Identify all available team statistics from ESPN API
  - ✅ Documented in report Section 3: "ESPN API Available Data"
  - ✅ Offensive metrics table: totalPointsPerGame, totalYards, passingYards, rushingYards
  - ✅ Defensive metrics table: pointsPerGameAllowed, totalYardsAllowed, totalTakeaways
- [x] **Task 2.2**: Research position-specific defensive statistics
  - ✅ **FOUND**: Position-specific rankings calculated internally (not from ESPN)
  - ✅ Evaluated in report Section 5.3: "Position-Specific Defense Evaluation"
  - ✅ Method documented at espn_client.py:1017-1097
  - ✅ **CONCLUSION**: Current method is industry standard - no changes needed
- [x] **Task 2.3**: Evaluate offensive ranking metrics
  - ✅ Analysis in report Section 5.1: "Offensive Ranking Evaluation"
  - ✅ **Current**: `totalPointsPerGame` - CORRECT, aligned with industry
  - ✅ Evaluated alternatives: totalYards, recent performance weighting
  - ✅ **CONCLUSION**: Current metric is optimal, optional enhancements available
- [x] **Task 2.4**: Evaluate defensive ranking metrics
  - ✅ Analysis in report Section 5.2: "Defensive Ranking Evaluation"
  - ✅ **Current**: `totalTakeaways` - PROBLEMATIC, volatile and unpredictive
  - ✅ Research shows pointsPerGameAllowed is more stable and predictive
  - ✅ **CONCLUSION**: Recommend switching to pointsPerGameAllowed

### Phase 3: Research Best Practices ✅ COMPLETE
- [x] **Task 3.1**: Research fantasy football industry standard team rankings
  - ✅ Researched 10+ major platforms (FantasyPros, ESPN, NFL.com, CBS, Yahoo, NBC, PFF, etc.)
  - ✅ Documented in report Section 4: "Industry Best Practices"
  - ✅ Offensive: Industry uses PPG as primary metric (validates current approach)
  - ✅ Defensive: Industry uses points allowed (NOT takeaways)
  - ✅ Position-specific: Industry uses fantasy points allowed per position (validates current approach)
- [x] **Task 3.2**: Identify most predictive statistics for fantasy impact
  - ✅ Research findings documented in report Section 4.2
  - ✅ Defensive: "Fantasy Points Per Game is the strongest predictor"
  - ✅ Defensive: Points allowed more stable than takeaways
  - ✅ Position-specific: Fantasy points allowed is direct measurement

### Phase 4: Create Comprehensive Report ✅ COMPLETE
- [x] **Task 4.1**: Create `docs/team_rankings/` folder
  - ✅ Created: `/docs/team_rankings/`
- [x] **Task 4.2**: Write report analyzing current methodology
  - ✅ Report Section 2: "Current Implementation Analysis"
  - ✅ Documented all three ranking methods with code references
  - ✅ Strengths and weaknesses identified for each method
- [x] **Task 4.3**: Document available ESPN API data
  - ✅ Report Section 3: "ESPN API Available Data"
  - ✅ Tables of offensive and defensive metrics with use cases
  - ✅ API endpoint and response structure documented
- [x] **Task 4.4**: Propose improved ranking calculations
  - ✅ Report Section 6: "Recommendations"
  - ✅ Offensive: Keep totalPointsPerGame (already optimal)
  - ✅ Defensive: Switch to pointsPerGameAllowed
  - ✅ Position-specific: No changes (already optimal)
- [x] **Task 4.5**: Include implementation recommendations
  - ✅ Report Section 7: "Implementation Guidance"
  - ✅ Step-by-step code changes with line numbers
  - ✅ Before/after code examples
  - ✅ Testing and validation guidance

### Phase 5: Validation and Documentation ✅ COMPLETE
- [x] **Task 5.1**: Review report for completeness
  - ✅ Report is 8 sections, moderate detail (5-10 page equivalent)
  - ✅ All user questions answered (comprehensive analysis, research-based recommendations)
  - ✅ Includes formulas/approaches without full implementation
- [x] **Task 5.2**: Ensure all questions from team_ranking_research.txt are answered
  - ✅ Original concern: "ranking scores may not properly represent real team rankings"
  - ✅ Report confirms: Defensive rank is suboptimal, offensive/position-specific are correct
  - ✅ Specific recommendations provided for improvement
- [x] **Task 5.3**: Update CLAUDE.md or README.md if needed
  - ℹ️ No updates needed - this is a research report, not a feature implementation
- [x] **Task 5.4**: Move team_ranking_research.txt to updates/done/
  - ✅ Moved to `updates/done/team_ranking_research.txt`

---

## Verification Summary

**Iterations Completed**: 6/6 (ALL VERIFICATION COMPLETE - Ready for execution)

### First Verification Round (Before Questions File)
- **Iteration 1**: ✅ COMPLETE
  - Re-read all source documents (team_ranking_research.txt, rules.md, ESPN docs)
  - Researched current implementation in espn_client.py
  - Found position-specific defense ranking implementation (lines 1017-1097)
  - Discovered previous investigation: `updates/done/espn_api_investigation_results.md`
  - Key findings:
    - Offensive rank: Based on totalPointsPerGame (may be too simple)
    - Defensive rank: Based on totalTakeaways (volatile metric)
    - Position defense: Calculated internally from player stats (good approach)
  - Updated Phase 1 and Phase 2 tasks with detailed findings

- **Iteration 2**: ✅ COMPLETE
  - Deep dive into ESPN API available statistics
  - Researched docs/espn/espn_team_data.md for all available metrics
  - Identified alternative metrics:
    - For defense: pointsPerGameAllowed (more stable than takeaways)
    - For offense: totalYards, yards per play, red zone stats
  - Analyzed position-specific defense calculation (appears sound, follows industry standards)
  - Updated Phase 2 tasks with specific ESPN stat names and concerns

- **Iteration 3**: ✅ COMPLETE
  - Reviewed all requirements from team_ranking_research.txt
  - Cross-referenced with current implementation
  - Identified key questions needing user clarification
  - Questions created covering:
    - Scope (which rankings to focus on)
    - Defensive metric choice (takeaways vs points allowed)
    - Offensive metric choice (single vs composite)
    - Position defense method validation
    - Report detail level
    - Implementation recommendations inclusion

### Questions File Created: ✅ COMPLETE
- Created: `updates/team_ranking_research_questions.md`
- Contains 6 questions with recommendations
- Awaiting user answers before proceeding to Phase 2 verification

### Second Verification Round (After User Answers)
- **Iteration 4**: ✅ COMPLETE
  - Re-read current implementation with user answers in mind
  - Confirmed all three ranking types need analysis:
    - Offensive: Uses only totalPointsPerGame (espn_client.py:828-835)
    - Defensive: Uses only totalTakeaways (espn_client.py:837-839)
    - Position-Specific: Calculated from fantasy points allowed (espn_client.py:1088-1108)
  - User wants RESEARCH-BASED recommendations (not just accept current metrics)
  - User is unsure about position-specific defense → needs full evaluation
  - Report: Moderate detail (5-10 pages) with recommendations and formulas

- **Iteration 5**: ✅ COMPLETE
  - Verified TODO tasks align with user preferences:
    - ✅ Q1 (All rankings): Phases 2-4 cover all three ranking types
    - ✅ Q2 (Research defensive metric): Task 2.4 evaluates alternatives
    - ✅ Q3 (Research offensive metric): Task 2.3 evaluates alternatives
    - ✅ Q4 (Evaluate position-specific): Task 2.2 includes full evaluation
    - ✅ Q5 (Moderate detail): Phase 4 tasks specify 5-10 page report
    - ✅ Q6 (Include recommendations): Tasks 4.4 and 4.5 include formulas/approaches
  - All phases properly structured for research-based analysis

- **Iteration 6**: ✅ COMPLETE
  - Final verification before execution
  - User preferences documented:
    - Scope: ALL rankings (offensive, defensive, position-specific)
    - Defensive: Research takeaways vs pointsPerGameAllowed vs combination
    - Offensive: Research single vs multiple metrics
    - Position-Specific: Evaluate current method (user unsure if it's optimal)
    - Detail: Moderate (5-10 pages)
    - Include: Recommendations with formulas/approaches (no full code)
  - Ready to proceed with Phase 2 (ESPN API research)

---

## Key Files and References

### Current Implementation
- `player-data-fetcher/espn_client.py:727-873` - Team ranking calculation methods
- `player-data-fetcher/espn_client.py:350-388` - `_fetch_team_rankings()` main entry
- `player-data-fetcher/espn_client.py:785-854` - `_calculate_team_rankings_for_season()`
- `utils/TeamData.py:200-246` - `extract_teams_from_rankings()`
- `data/teams.csv` - Current team rankings output

### ESPN Documentation
- `docs/espn/espn_team_data.md` - ESPN team data field reference
- `docs/espn/espn_api_endpoints.md` - ESPN API endpoint documentation

### Team Data Structure
- `offensive_rank`: Overall offensive quality (1-32)
- `defensive_rank`: Overall defensive quality (1-32)
- `def_vs_qb_rank`: Defense vs QB (1-32)
- `def_vs_rb_rank`: Defense vs RB (1-32)
- `def_vs_wr_rank`: Defense vs WR (1-32)
- `def_vs_te_rank`: Defense vs TE (1-32)
- `def_vs_k_rank`: Defense vs K (1-32)

---

## Completion Summary

**Date Completed**: 2025-11-01

**Deliverables**:
1. ✅ Comprehensive research report: `docs/team_rankings/team_ranking_analysis_report.md`
2. ✅ Questions file answered: `updates/team_ranking_research_questions.md`
3. ✅ TODO tracking file: `updates/todo-files/team_ranking_research_todo.md`
4. ✅ Original file moved: `updates/done/team_ranking_research.txt`

**Key Findings**:
- **Offensive Rankings**: ✅ Current method (totalPointsPerGame) is correct and aligned with industry
- **Defensive Rankings**: ❌ Current method (totalTakeaways) is suboptimal - recommend switching to pointsPerGameAllowed
- **Position-Specific Defense**: ✅ Current method (fantasy points allowed per position) is industry standard - no changes needed

**Report Location**: `/docs/team_rankings/team_ranking_analysis_report.md`

**Next Steps** (if implementing recommendations):
1. Review the report recommendations (Section 6)
2. Implement defensive ranking change from totalTakeaways to pointsPerGameAllowed
3. Follow implementation guidance in Section 7 of the report

---

## Notes

- This was a RESEARCH task, not an implementation task
- No code changes were made during this phase
- Report is comprehensive and data-driven with industry research
- Report includes specific API endpoints, stat names, and code references
- Report provides implementation recommendations with formulas/approaches
