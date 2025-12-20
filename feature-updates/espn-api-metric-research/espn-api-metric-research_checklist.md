# ESPN API Metric Research - Checklist

**Last Updated:** 2025-12-19
**Status:** Phase 1 Complete - Awaiting Phase 2 Investigation

---

## Purpose

This checklist tracks all open questions and decisions that must be resolved before implementation. Items will be populated during Phase 2 (Investigation) and resolved during Phase 4 (Iterative Resolution).

---

## Checklist Items

**Total Items:** 47 (populated during Phase 2 - Investigation)
**Resolved:** 2 items marked [x]
**Pending:** 45 items marked [ ]

---

### ITERATION 1: Core Research Questions

#### Category 1: Research Document Template & Structure

- [x] **Q1.1:** What template should be used for metric research documents?
  - **RESOLVED:** Create new standardized template for consistency across all 58 metrics
  - Template based on 7 mandatory questions from notes
  - Ensures perfect consistency, tailored to exact research needs
  - Template will be created at `docs/research/potential_metrics/TEMPLATE.md`

- [x] **Q1.2:** What sections are mandatory vs optional in each metric document?
  - **RESOLVED:** 8 mandatory sections for every metric document
  - Mandatory: 7 questions + Position Applicability header
  - Optional sections skipped: Executive Summary (redundant), Implementation Examples (belongs in implementation phase)
  - Limitations included within Data Quality Assessment section (not separate)
  - Data Quality Assessment should cover: reliability, accuracy, update frequency, known limitations

- [ ] **Q1.3:** How should we document "data not available" findings?
  - What level of effort to prove something doesn't exist?
  - Document what we searched and didn't find?
  - Include alternative approaches if primary source unavailable?

- [ ] **Q1.4:** Should metric documents include code examples?
  - Python snippets showing data structure?
  - API request/response examples?
  - Calculation formulas in pseudocode?

#### Category 2: Data Source Verification Strategy

- [ ] **Q2.1:** How to verify ESPN API endpoint availability?
  - Test live against ESPN API for each metric?
  - Or rely on existing ESPN API documentation in `docs/espn/`?
  - What if endpoint exists but requires authentication we don't have?

- [ ] **Q2.2:** What constitutes sufficient verification of "free alternatives"?
  - Must we test API calls to each alternative source?
  - Or is documentation review sufficient?
  - How many alternatives to research per metric (minimum 2-3 per notes)?

- [ ] **Q2.3:** How to validate data quality and update frequency?
  - Test actual API responses and check timestamps?
  - Review API documentation for SLAs?
  - Compare multiple sources for accuracy?

- [ ] **Q2.4:** Should we create test scripts for API verification?
  - Follow pattern from `player-data-fetcher/` (async, retry logic)?
  - Or manual testing with documentation of findings?
  - Store test results as evidence in research docs?

#### Category 3: Historical Data Availability Assessment

- [ ] **Q3.1:** What defines "historical data available"?
  - Must data be available for all 3 seasons (2021, 2022, 2024)?
  - Or is 1 season sufficient for simulation validation?
  - What if only 2023 data exists (not currently in sim_data)?

- [ ] **Q3.2:** How to verify weekly snapshot availability?
  - Must we verify all 17 weeks are available?
  - Or sample verification (e.g., weeks 1, 5, 10, 15)?
  - What if only certain weeks have data?

- [ ] **Q3.3:** Where does metric data fit in sim_data structure?
  - Player-level metrics: Which file? (players.csv vs players_projected.csv)
  - Team-level metrics: New columns in team_data/{TEAM}.csv?
  - Game-level metrics: New columns in game_data.csv?
  - New file needed: When to create separate snapshot file?

- [ ] **Q3.4:** How to document "predictive vs retrospective" data timing?
  - What level of detail to verify data represents "what we knew then"?
  - Test with sample metric (e.g., target share through week 4 only)?
  - Document data collection timing requirements?

#### Category 4: Existing Data Leverage

- [ ] **Q4.1:** For metrics calculable from existing data, what level of detail?
  - Document exact calculation formula?
  - Provide example calculation with real player data?
  - Reference existing column names and structure?

- [ ] **Q4.2:** Should we identify metrics already partially available?
  - Review current columns (ADP, player_rating, weekly_points, team rankings)?
  - Mark which of 58 metrics are "already have data, just need logic"?
  - Prioritize these as "quick wins"?

- [ ] **Q4.3:** How to handle metrics requiring multiple data sources?
  - Document each source separately?
  - Provide integration guidance?
  - Estimate combined complexity?

#### Category 5: Priority Sequencing & Workflow

- [ ] **Q5.1:** Should research follow priority order (Phase 1 → 2 → 3)?
  - Start with 14 HIGH priority metrics first?
  - Or organize by data source (all ESPN metrics, then all free alternatives)?
  - Or by complexity (easy wins first)?

- [ ] **Q5.2:** How to track research progress?
  - Create tracking spreadsheet with 58 rows?
  - Update checklist in notes file as we go?
  - Create summary document showing status?

- [ ] **Q5.3:** Should related metrics be researched together?
  - Group position-specific metrics (all K metrics, all TE metrics)?
  - Group by data source (all ESPN API metrics)?
  - Research in numerical order (1-58)?

- [ ] **Q5.4:** What is the target timeline/pace for research?
  - How many metrics per session?
  - Aim for completion date?
  - Parallel research possible (multiple agents)?

---

### ITERATION 2: Operational & Quality Aspects

#### Category 6: Research Quality & Validation

- [ ] **Q6.1:** How to ensure research is complete before marking metric "done"?
  - Checklist within each metric document?
  - Peer review process?
  - User validation of findings?

- [ ] **Q6.2:** What evidence is required for "not available" conclusions?
  - Document which endpoints/APIs were checked?
  - Screenshot or log of failed attempts?
  - Minimum number of sources to check before concluding unavailable?

- [ ] **Q6.3:** How to handle conflicting information?
  - Documentation says available but API test fails?
  - Multiple sources give different data formats?
  - Document conflicts and recommend best source?

- [ ] **Q6.4:** Should we verify claimed "free" sources are actually free?
  - Check for API rate limits?
  - Verify no credit card required?
  - Test free tier limitations?

#### Category 7: Documentation Output & Organization

- [ ] **Q7.1:** File naming convention confirmation?
  - Notes suggest: `{metric_number}_{metric_name}.md`
  - Use underscores or hyphens? (e.g., `01_target_volume.md` vs `01-target-volume.md`)
  - How to handle long metric names (truncate? abbreviate?)?

- [ ] **Q7.2:** Should we create an index/summary document?
  - `docs/research/potential_metrics/README.md` with table of all metrics?
  - Link to each metric document?
  - Summary table showing: available/not available, priority, data source?

- [ ] **Q7.3:** How to link metrics to scoring_gap_analysis.md?
  - Cross-reference metric numbers?
  - Copy thresholds and position applicability from gap analysis?
  - Keep metrics synced if gap analysis updates?

- [ ] **Q7.4:** Should research docs include implementation estimates?
  - Hours/days to implement?
  - Difficulty rating (easy/medium/hard)?
  - Dependencies on other metrics?

#### Category 8: Integration with Existing Workflows

- [ ] **Q8.1:** How does this research feed into implementation planning?
  - Create separate feature for implementing metrics?
  - Prioritize implementation based on research findings?
  - Group metrics into implementation batches?

- [ ] **Q8.2:** Should research include fetcher design patterns?
  - Follow `player-data-fetcher/` async pattern?
  - Document required API clients/libraries?
  - Provide code structure recommendations?

- [ ] **Q8.3:** How to handle metrics requiring external dependencies?
  - Document required packages (e.g., odds-api-client)?
  - Note authentication/API key requirements?
  - Estimate cost if free tier insufficient?

- [ ] **Q8.4:** Should we update existing ESPN API docs?
  - Add findings to `docs/espn/espn_api_endpoints.md`?
  - Create new sections for newly discovered endpoints?
  - Keep research docs separate from API reference docs?

---

### ITERATION 3: Edge Cases, Relationships & Cross-Cutting Concerns

#### Category 9: Multi-Season & Multi-Mode Considerations

- [ ] **Q9.1:** How to handle year-specific metrics (e.g., 2025 rule changes)?
  - Document metric availability per season?
  - Note if metric definition changed over time?
  - Verify historical data uses same definition?

- [ ] **Q9.2:** How do metrics apply across different scoring modes?
  - Position-specific metrics only for that position?
  - Some metrics universal (weather) vs mode-specific?
  - Document mode applicability in each metric doc?

- [ ] **Q9.3:** Should we research playoff-specific metrics?
  - Weeks 15-17 (fantasy playoffs) different considerations?
  - Playoff game environment different from regular season?
  - Document if metric more/less important in playoffs?

#### Category 10: Data Format & Schema Compatibility

- [ ] **Q10.1:** How to ensure new metric columns are compatible with existing schema?
  - Column naming convention (snake_case, camelCase)?
  - Data types (int, float, string, boolean)?
  - Null/missing value handling?

- [ ] **Q10.2:** Should we define schema for each metric?
  - Include in research doc: column name, type, range, example values?
  - Create separate schema reference document?
  - Validate against existing players.csv/team_data structure?

- [ ] **Q10.3:** How to handle metrics with complex data structures?
  - Array/list columns (e.g., weekly target shares)?
  - Nested data (e.g., QB-WR connection matrix)?
  - Multiple related columns vs single JSON column?

#### Category 11: Metric Relationships & Dependencies

- [ ] **Q11.1:** Should we identify metric dependencies?
  - Metric A requires Metric B to be calculated first?
  - Document calculation order/dependencies?
  - Group dependent metrics together?

- [ ] **Q11.2:** How to handle composite metrics?
  - WOPR = f(target share, air yards share) - research both components?
  - Document calculation formula for composite metrics?
  - Recommend implementing components first?

- [ ] **Q11.3:** Should we identify overlapping/redundant metrics?
  - Multiple metrics measuring similar things (e.g., QB quality via different methods)?
  - Recommend which to prioritize?
  - Document trade-offs between similar metrics?

#### Category 12: Testing & Validation Strategy

- [ ] **Q12.1:** Should research include sample data for testing?
  - Provide example API responses?
  - Sample calculations with real player data?
  - Test cases for edge conditions?

- [ ] **Q12.2:** How to validate metric improves accuracy?
  - Require baseline comparison (simulation results)?
  - Document expected impact on accuracy?
  - Define success criteria before implementation?

- [ ] **Q12.3:** Should we pilot test high-priority metrics?
  - Implement 1-2 metrics as proof-of-concept during research?
  - Validate feasibility before researching all 58?
  - Use learnings to refine research approach?

#### Category 13: Long-Term Maintenance

- [ ] **Q13.1:** How to keep research current as APIs change?
  - Version research documents (date of research)?
  - Plan for periodic re-validation?
  - Note API stability/change history?

- [ ] **Q13.2:** Should we document metric lifecycle?
  - When to deprecate a metric (data source discontinued)?
  - How to replace deprecated metrics?
  - Version tracking for metric definitions?

- [ ] **Q13.3:** How to handle new metrics discovered later?
  - Process for adding metric 59+?
  - Update numbering or append?
  - Keep research docs in sync with scoring_gap_analysis.md?

---

## Resolution Log

**Progress:** 0/0 questions resolved (checklist to be populated in Phase 2)

### Resolved Items
*(Items marked [x] will appear here with resolution details)*

### Pending Items
*(Items marked [ ] will appear here until resolved)*

---

## Categories

Checklist items will be organized into these categories during Phase 2:

1. **Research Methodology**
   - How to structure research process?
   - What verification steps to include?
   - How to prioritize metrics?

2. **Data Source Verification**
   - How to verify ESPN API endpoints?
   - How to test free alternative APIs?
   - How to validate data quality?

3. **Historical Data Strategy**
   - How to identify historical data sources?
   - How to validate weekly snapshot availability?
   - How to structure historical data acquisition?

4. **Documentation Standards**
   - What template to use for metric documents?
   - How detailed should each section be?
   - How to document "not available" findings?

5. **Implementation Planning**
   - How to estimate implementation complexity?
   - How to categorize metrics (live-only vs simulation-validated)?
   - How to recommend data source preference?

6. **Quality & Validation**
   - How to ensure research completeness?
   - How to validate findings?
   - How to track research progress?

---

## Next Steps

1. **Phase 2:** Agent will investigate codebase and populate this checklist with ALL open questions
2. **Phase 3:** Agent will present findings and wait for user direction
3. **Phase 4:** User and agent will iteratively resolve each checklist item
4. **Completion:** All items marked [x], specs file updated, ready for implementation
