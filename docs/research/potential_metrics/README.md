# Potential Scoring Metrics - Research Documentation

**Purpose:** Comprehensive research of potential metrics for the fantasy football scoring algorithm

**Source:** Based on `docs/research/scoring_gap_analysis.md` (Version 3.0, Last Updated: December 17, 2025)

**Research Period:** December 2025

**Status:** Not started

---

## Overview

This directory contains individual research documents for potential metrics identified in the scoring gap analysis. Each metric has been systematically researched to determine:

1. **Data Availability** - Can we get this data from existing sources, ESPN API, or free alternatives?
2. **Historical Data Availability** - Can we obtain weekly snapshots for simulation validation? (CRITICAL)
3. **Implementation Complexity** - How difficult is it to implement?
4. **Recommendation** - Should we pursue, defer, or skip this metric?

The research follows a standardized template (`TEMPLATE.md`) to ensure consistency across all 58 metrics.

---

## How to Use These Documents

### For Decision Making

1. **Start with HIGH priority metrics** - These provide the most value
2. **Review the Recommendation section** - Clear pursue/defer/skip guidance
3. **Check Historical Data Availability** - Critical for simulation validation
4. **Assess Implementation Complexity** - Balance value vs. effort

### For Implementation

1. **Read the complete research document** for chosen metrics
2. **Note the Preferred Data Source** - Use the recommended source
3. **Review Dependencies** - Implement dependent metrics first
4. **Follow Schema Definition** - Use documented column names and types
5. **Reference Implementation Complexity** - Follow suggested patterns

### File Naming Convention

Research documents follow the pattern: `{metric_number}_{metric_name}.md`

Examples:
- `01_target_volume.md` - Target Volume/Share (Metric 1)
- `39_team_rz_td_percentage.md` - Team Red Zone TD% (Metric 39)
- `52_pass_block_rate.md` - Pass Block Rate (Metric 52)

---

## Research Methodology

Each metric research document answers 7 key questions:

### 1. Existing Data Analysis
Can we calculate this from data already in the `data/` folder?

### 2. ESPN API Availability
Is this available via ESPN Fantasy Football API endpoints?

### 3. Free Alternative Sources
What free data sources provide this metric? (Minimum 2-3 researched)

### 4. Data Quality Assessment
How reliable, accurate, and frequently updated is the data?

### 5. Historical Data Availability ⚠️ CRITICAL
Can we obtain weekly snapshots for simulation validation?

**Historical Data Requirements:**
- Minimum: 1 complete season (17 weeks)
- Ideal: 3 seasons (2021, 2022, 2024)
- Structure: Must fit `simulation/sim_data/{YEAR}/weeks/week_{NN}/` format
- Timing: Data must represent "what we knew going INTO that week" (predictive, not retrospective)

### 6. Implementation Complexity
Effort required, dependencies, schema integration

### 7. Recommendation
Should we pursue, defer, or skip? What's the preferred data source?

---
## Integration with Existing System

### Current 13-Step Scoring Algorithm

The existing algorithm covers:
1. Normalization (fantasy points)
2. ADP Multiplier
3. Player Rating
4. Team Quality
5. Performance Multiplier
6. Matchup (opponent defense)
7. Schedule (future opponents)
8. Draft Order Bonus
9. Bye Week Penalty
10. Injury Penalty
11. Wind Factor
12. Temperature Factor
13. Location Bonus

### Gaps Addressed by This Research

These metrics should address gaps including:
- Target/opportunity volume (not in current system)
- QB context for pass-catchers (partially covered by team quality)
- Vegas lines/game environment (not in current system)
- Position-specific metrics (partially covered)
- Advanced efficiency metrics (EPA, xFP, WOPR)

---

## Data Source Priority

Research follows this source priority order:

1. **EXISTING DATA** - Calculate from `data/` folder (quickest wins)
2. **ESPN API** - Available but not yet integrated (medium effort)
3. **FREE ALTERNATIVES** - External free sources (higher effort, ongoing maintenance)
4. **HISTORICAL ACCESS** - Can we get past seasons for validation? (CRITICAL filter)

---

## Implementation Roadmap

### Phase 1: Quick Wins
Metrics calculable from existing data (no new data fetching required)

### Phase 2: ESPN API Integration
Metrics available via ESPN but not currently pulled

### Phase 3: Free Alternative Sources
High-value metrics requiring external data sources

### Phase 4: Advanced Metrics
Lower priority or complex metrics

**Note:** All phases require historical data availability for simulation validation

---

## Related Documentation

| Document | Purpose |
|----------|---------|
| `TEMPLATE.md` | Template for creating new metric research docs |
| `../scoring_gap_analysis.md` | Source document identifying all 58 metrics |
| `../../espn/` | ESPN API documentation |

---

## Contributing to This Research

### When Adding a New Metric (59+)

1. Add metric to `scoring_gap_analysis.md` first
2. Create research doc using `TEMPLATE.md`
3. Update `RESEARCH_PROGRESS.md` with new row
4. Follow file naming convention: `{number}_{name}.md`
5. Complete all 7 mandatory sections

### When Updating Existing Research

1. Add update date to research doc
2. Note what changed (data source discontinued, new alternative found, etc.)
3. Update `RESEARCH_PROGRESS.md` if status changes
4. Consider annual re-validation for all metrics

---

## Key Takeaways

✅ **Standardized Research** - All metrics use same template for consistency

✅ **Historical Data Focus** - Simulation validation is a critical requirement

✅ **Priority-Driven** - HIGH priority metrics researched first

✅ **Implementation-Ready** - Research docs provide schema, dependencies, effort estimates

✅ **Comprehensive** - Covers 6 categories: gaps, reviews, projections, position-specific

---

*This documentation is maintained as part of the fantasy football helper scripts project. For questions or updates, see `feature-updates/espn-api-metric-research/` for planning details.*

**Last Updated:** 2025-12-20
