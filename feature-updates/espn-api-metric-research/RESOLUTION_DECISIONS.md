# ESPN API Metric Research - All Decisions Resolved

**Date:** 2025-12-20
**Status:** All 47 checklist items systematically resolved using recommended approaches

---

## Category 1: Research Document Template & Structure

### Q1.1: Template Selection ✅
**Decision:** Create new standardized template (Option C)
**Rationale:** Ensures consistency across all 58 metrics

### Q1.2: Mandatory vs Optional Sections ✅
**Decision:** 8 mandatory sections (7 questions + Position Applicability header)
**Rationale:** Comprehensive yet efficient structure

### Q1.3: "Data Not Available" Documentation
**Decision:** Moderate documentation (Option B)
**Details:**
- Document sources checked with specific endpoints/fields
- Include reference to documentation reviewed
- Note what was searched and not found
- Balance thoroughness with efficiency for 58 metrics

### Q1.4: Code Examples in Research Docs
**Decision:** No code examples in research phase
**Rationale:**
- Research phase is for data availability, not implementation
- Code examples belong in implementation documentation
- Keeps research docs focused and consistent
- Can add pseudocode formulas in "Implementation Complexity" section if helpful

---

## Category 2: Data Source Verification Strategy

### Q2.1: ESPN API Endpoint Verification
**Decision:** Rely on existing ESPN API documentation in `docs/espn/` with spot checks
**Details:**
- Primary: Review existing ESPN API docs
- Secondary: Spot check 2-3 endpoints for HIGH priority metrics
- Document authentication limitations if encountered
- No need to test all endpoints for all 58 metrics

### Q2.2: Free Alternatives Verification
**Decision:** Documentation review sufficient, with testing for HIGH priority metrics
**Details:**
- Minimum 2-3 alternatives researched per metric (per notes requirement)
- Documentation review acceptable for most metrics
- Spot test APIs for HIGH priority metrics (14 metrics)
- Document rate limits and free tier constraints

### Q2.3: Data Quality Validation
**Decision:** Documentation review for SLAs, no live testing required
**Details:**
- Review API documentation for update frequency
- Check community forums for reliability reports
- Note any known issues or limitations
- Live testing only if documentation is unclear

### Q2.4: Test Scripts for API Verification
**Decision:** No test scripts during research phase
**Rationale:**
- Research phase is about availability, not implementation
- Test scripts belong in implementation phase
- Manual testing with documentation sufficient
- Can reference `player-data-fetcher/` patterns in "Implementation Complexity"

---

## Category 3: Historical Data Availability Assessment

### Q3.1: Historical Data Definition
**Decision:** 1 season sufficient for validation, prefer multiple seasons when available
**Details:**
- Minimum: 1 complete season (17 weeks) for simulation validation
- Ideal: 2-3 seasons (2021, 2022, 2024)
- Document which seasons are available
- Note if only 2023 data exists (would need to add to sim_data)

### Q3.2: Weekly Snapshot Verification
**Decision:** Sample verification (weeks 1, 5, 10, 15) sufficient
**Details:**
- Verify 4 sample weeks across the season
- Document if only certain weeks have data
- Note gaps in availability
- Full 17-week verification only for HIGH priority metrics with confirmed availability

### Q3.3: Metric Data Fit in sim_data Structure
**Decision:** Document fit based on metric type
**Details:**
- **Player-level metrics:** Add columns to `players.csv` (for actuals) and `players_projected.csv` (for projections)
- **Team-level metrics:** Add columns to `team_data/{TEAM}.csv`
- **Game-level metrics:** Add columns to `game_data.csv`
- **Complex metrics:** Create new weekly snapshot file only if doesn't fit above
- Document exact column names and types in research doc

### Q3.4: Predictive vs Retrospective Data Timing
**Decision:** Document timing requirements, test with 1 sample metric per data source
**Details:**
- Clearly state: "Data must represent what we knew going INTO that week"
- Example format: week_05/ has weeks 1-4 actuals + weeks 5-17 projections
- Test with one sample metric from each data source to verify timing
- Document collection timing requirements in "Historical Data" section

---

## Category 4: Existing Data Leverage

### Q4.1: Metrics Calculable from Existing Data - Detail Level
**Decision:** Document formula + reference existing columns
**Details:**
- Exact calculation formula in "Existing Data Analysis" section
- Reference specific column names from current files
- Example: "Can calculate from `week_N_points` columns in players.csv"
- No need for sample calculations with real data (research phase)

### Q4.2: Identify Partially Available Metrics
**Decision:** Yes, mark these as "quick wins"
**Details:**
- Review current columns: ADP, player_rating, weekly_points, team rankings
- Identify which of 58 metrics are "data exists, just need logic"
- Mark in research doc: "Quick Win - Data Already Available"
- Prioritize these in implementation recommendations

### Q4.3: Metrics Requiring Multiple Data Sources
**Decision:** Document each source separately with integration notes
**Details:**
- List each data source in its own subsection
- Add "Data Integration" note in "Implementation Complexity" section
- Estimate combined complexity (sum of individual + integration overhead)
- Identify dependencies between sources

---

## Category 5: Priority Sequencing & Workflow

### Q5.1: Research Priority Order
**Decision:** Follow priority order (Phase 1 HIGH → Phase 2 MEDIUM → Phase 3 LOW)
**Rationale:**
- Start with 14 HIGH priority metrics
- Ensures most valuable metrics researched first
- Aligns with notes' priority structure
- Can adjust if patterns emerge (e.g., all ESPN metrics together if efficient)

### Q5.2: Track Research Progress
**Decision:** Create summary document showing status
**Details:**
- Create `docs/research/potential_metrics/RESEARCH_PROGRESS.md`
- Table with: Metric #, Name, Priority, Status, Data Source, Historical Available
- Update after each metric researched
- Provides at-a-glance view of all 58 metrics

### Q5.3: Group Related Metrics
**Decision:** Research by priority order, but note relationships
**Details:**
- Primary: Priority order (HIGH → MEDIUM → LOW)
- Secondary: Note related metrics in each research doc
- Example: "See also Metric 13 (Air Yards) - dependency for this metric"
- Can research related metrics consecutively within same priority tier

### Q5.4: Timeline/Pace for Research
**Decision:** No fixed timeline, research by priority
**Details:**
- HIGH priority (14 metrics): Research first, thorough
- MEDIUM priority (15 metrics): Research second
- LOW priority (29 metrics): Research based on findings from HIGH/MEDIUM
- Pace: Flexible, quality over speed
- Parallel research: Not recommended (ensure consistency)

---

## Category 6: Research Quality & Validation

### Q6.1: Ensure Research Completeness
**Decision:** Checklist within each metric document
**Details:**
- Add "Research Checklist" section at end of each metric doc
- Verify all 8 mandatory sections completed
- Check that recommendation is clear and actionable
- No peer review process needed (single researcher for consistency)

### Q6.2: Evidence for "Not Available" Conclusions
**Decision:** Document endpoints/APIs checked (aligns with Q1.3 decision)
**Details:**
- List specific endpoints/fields checked
- Note documentation reviewed
- Minimum 2-3 sources checked before concluding unavailable
- No screenshots needed (documentation of search sufficient)

### Q6.3: Handle Conflicting Information
**Decision:** Document conflicts and recommend best source
**Details:**
- Note the conflict in research doc
- Test if possible to resolve
- Recommend most reliable source with rationale
- Flag for user decision if can't resolve

### Q6.4: Verify "Free" Sources
**Decision:** Yes, verify free tier limitations
**Details:**
- Check for API rate limits
- Verify no credit card required for free tier
- Test free tier limitations where documented
- Document any costs if free tier insufficient

---

## Category 7: Documentation Output & Organization

### Q7.1: File Naming Convention
**Decision:** Use underscores, format: `{metric_number}_{metric_name}.md`
**Details:**
- Example: `01_target_volume.md`, `39_team_rz_td_percentage.md`
- Long names: Use full name (no truncation for clarity)
- Metric number: Zero-padded (01-58)
- Lowercase with underscores

### Q7.2: Create Index/Summary Document
**Decision:** Yes, create `docs/research/potential_metrics/README.md`
**Details:**
- Table with all 58 metrics
- Columns: #, Name, Priority, Status, Data Available, Historical Available, Recommendation
- Links to each metric document
- Summary stats (X available, Y not available, Z pending)

### Q7.3: Link to scoring_gap_analysis.md
**Decision:** Cross-reference metric numbers, copy key details
**Details:**
- Reference scoring_gap_analysis.md metric number
- Copy position applicability and thresholds into research doc
- Note if gap analysis updates (date-based versioning)
- Keep research docs independent (snapshot of gap analysis at research time)

### Q7.4: Include Implementation Estimates
**Decision:** Yes, include difficulty rating and dependencies
**Details:**
- Difficulty: Easy/Medium/Hard in "Implementation Complexity" section
- Rough effort estimate: Hours/days (not precise, directional)
- List dependencies on other metrics
- Note required external packages/APIs

---

## Category 8: Integration with Existing Workflows

### Q8.1: Research Feeds Into Implementation Planning
**Decision:** Research informs separate implementation feature
**Details:**
- Research output: Prioritized list of metrics to implement
- Create separate feature: "implement-metrics-batch-1" (based on research findings)
- Group metrics by data source for implementation efficiency
- Use research docs as specification for implementation

### Q8.2: Include Fetcher Design Patterns
**Decision:** Reference patterns, don't design in detail
**Details:**
- Note in "Implementation Complexity": "Follow player-data-fetcher/ async pattern"
- Reference existing patterns, don't create new designs
- Design belongs in implementation phase, not research
- Document which pattern applies (ESPN API vs external API)

### Q8.3: Handle External Dependencies
**Decision:** Document packages, auth, and costs
**Details:**
- List required packages (e.g., `requests`, `odds-api-client`)
- Note authentication requirements (API keys, OAuth)
- Estimate costs if free tier insufficient
- Flag metrics requiring paid data as higher complexity

### Q8.4: Update Existing ESPN API Docs
**Decision:** Keep research docs separate, optionally update ESPN docs later
**Details:**
- Research docs are standalone in `docs/research/potential_metrics/`
- ESPN API docs (`docs/espn/`) remain as reference
- Optional: Update ESPN docs with new discoveries after research complete
- No updates during research phase (keep workflows separate)

---

## Category 9: Multi-Season & Multi-Mode Considerations

### Q9.1: Year-Specific Metrics
**Decision:** Document metric availability per season
**Details:**
- Note if metric definition changed over time
- Document rule changes affecting metric (e.g., 2025 kicker accuracy changes)
- Verify historical data uses same definition
- Flag inconsistencies for user decision

### Q9.2: Metrics Across Scoring Modes
**Decision:** Document mode applicability
**Details:**
- Position-specific metrics: Note applicable positions
- Universal metrics: Note "All positions"
- Mode-specific behavior: Document in "Implementation Complexity"
- Reference league_config.json for mode definitions

### Q9.3: Playoff-Specific Metrics
**Decision:** Document if metric behavior changes in playoffs
**Details:**
- Note in research doc if metric more/less important weeks 15-17
- Document playoff game environment differences
- Example: Weather metrics more important in playoffs (outdoor games)
- No separate playoff metric research needed

---

## Category 10: Data Format & Schema Compatibility

### Q10.1: New Metric Column Compatibility
**Decision:** Document naming convention and data types
**Details:**
- Column naming: snake_case (matches existing files)
- Data types: int, float, string, boolean (document in research doc)
- Null handling: Document expected behavior for missing data
- Validate against existing schema in "Implementation Complexity"

### Q10.2: Define Schema for Each Metric
**Decision:** Yes, include schema in research doc
**Details:**
- Document in "Implementation Complexity" section
- Include: column name, data type, range, example values
- Reference existing structure (players.csv, team_data/*.csv)
- Validate compatibility with existing schema

### Q10.3: Complex Data Structures
**Decision:** Recommend simplest structure that fits
**Details:**
- Prefer: Multiple related columns over JSON
- Array/list: Use separate columns (week_1_targets, week_2_targets)
- Nested data: Flatten if possible, otherwise document JSON structure
- Document trade-offs in "Implementation Complexity"

---

## Category 11: Metric Relationships & Dependencies

### Q11.1: Identify Metric Dependencies
**Decision:** Yes, document dependencies in each metric doc
**Details:**
- Note in "Implementation Complexity" if metric requires another metric
- Example: WOPR requires target share (Metric 1) + air yards share (Metric 13)
- Document calculation order
- Cross-reference dependent metrics

### Q11.2: Composite Metrics
**Decision:** Research components separately, document formula
**Details:**
- Research each component as separate metric
- Document composite formula in main metric doc
- Recommend implementing components first
- Note dependencies in "Implementation Complexity"

### Q11.3: Overlapping/Redundant Metrics
**Decision:** Document overlaps and recommend priority
**Details:**
- Identify similar metrics in research doc
- Compare pros/cons of each approach
- Recommend which to prioritize (easier data, better quality)
- Note in recommendation section

---

## Category 12: Testing & Validation Strategy

### Q12.1: Include Sample Data
**Decision:** No sample data in research phase
**Rationale:**
- Research is about availability, not implementation
- Sample data belongs in implementation/testing phase
- Keeps research docs focused
- Can note example API responses if helpful for understanding

### Q12.2: Validate Metric Improves Accuracy
**Decision:** Not during research phase
**Details:**
- Research documents availability only
- Accuracy validation happens during implementation
- Note expected impact in "Recommendation" section (directional)
- Actual validation via accuracy simulations post-implementation

### Q12.3: Pilot Test High-Priority Metrics
**Decision:** No pilot implementation during research
**Rationale:**
- Research phase separate from implementation
- Pilot tests belong in implementation phase
- Research should be thorough but not include coding
- Findings may inform decision to pilot test during implementation

---

## Category 13: Long-Term Maintenance

### Q13.1: Keep Research Current
**Decision:** Version research documents with date
**Details:**
- Add "Research Date: YYYY-MM-DD" to each metric doc
- Note API version if applicable
- Plan periodic re-validation (annual basis)
- Note API stability/change history if known

### Q13.2: Document Metric Lifecycle
**Decision:** Include deprecation notes in research template
**Details:**
- Add "Lifecycle Notes" subsection in template
- Document when data source might be discontinued
- Note replacement strategy if deprecated
- Version tracking via research date

### Q13.3: Handle New Metrics (59+)
**Decision:** Append new metrics, update numbering
**Details:**
- New metrics: Continue numbering (59, 60, 61, ...)
- Update README index with new metrics
- Keep research docs in sync with scoring_gap_analysis.md
- Process: Same research workflow for new metrics

---

## Summary of Key Decisions

### Research Approach
- Standardized template with 8 mandatory sections
- Moderate documentation level (thorough but efficient)
- Priority order: HIGH → MEDIUM → LOW
- No implementation during research phase

### Data Verification
- ESPN API: Documentation review + spot checks for HIGH priority
- Free alternatives: Minimum 2-3 researched per metric
- Historical data: 1 season minimum, sample verification (4 weeks)
- Data quality: Documentation review sufficient

### Documentation Standards
- File naming: `{number}_{name}.md` with underscores
- Create README index with summary table
- Include schema definition in each doc
- Version with research date

### Integration
- Research informs separate implementation feature
- Document dependencies and relationships
- Reference existing patterns, don't design new ones
- Keep research docs separate from implementation docs

---

## Next Steps

1. Create template at `docs/research/potential_metrics/TEMPLATE.md`
2. Create progress tracker at `docs/research/potential_metrics/RESEARCH_PROGRESS.md`
3. Start researching HIGH priority metrics (14 metrics)
4. Update progress tracker after each metric
5. Create README index after research complete
