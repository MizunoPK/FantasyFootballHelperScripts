# Potential Scoring Metrics - Research Documentation

**Purpose:** Comprehensive research of 58 potential metrics for the fantasy football scoring algorithm

**Source:** Based on `docs/research/scoring_gap_analysis.md` (Version 3.0, Last Updated: December 17, 2025)

**Research Period:** December 2025

**Status:** Research in progress - see `RESEARCH_PROGRESS.md` for current status

---

## Overview

This directory contains individual research documents for 58 potential metrics identified in the scoring gap analysis. Each metric has been systematically researched to determine:

1. **Data Availability** - Can we get this data from existing sources, ESPN API, or free alternatives?
2. **Historical Data Availability** - Can we obtain weekly snapshots for simulation validation? (CRITICAL)
3. **Implementation Complexity** - How difficult is it to implement?
4. **Recommendation** - Should we pursue, defer, or skip this metric?

The research follows a standardized template (`TEMPLATE.md`) to ensure consistency across all 58 metrics.

---

## How to Use These Documents

### For Decision Making

1. **Start with HIGH priority metrics** (14 metrics) - These provide the most value
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

## Metrics Summary

### By Priority

| Priority | Count | Purpose |
|----------|-------|---------|
| **HIGH** | 14 | Critical for accuracy, implement first |
| **MEDIUM** | 15 | High value, implement after HIGH |
| **LOW** | 29 | Nice-to-have, implement as needed |

### By Category

| Category | Metrics | Examples |
|----------|---------|----------|
| **Original Gap Metrics** | 1-11 | Target Volume, QB Context, Vegas Lines |
| **Additional Review Metrics** | 12-19 | Implied Team Total, Air Yards, Snap Share |
| **Projection Calculation Metrics** | 20-38 | WOPR, xFP, EPA, Success Rate |
| **Position-Specific Metrics** | 39-58 | Kicker (39-41), TE (42-45), RB (46-51), QB (52-53), WR (54-58) |

### By Position Applicability

| Position | Applicable Metrics | Key Examples |
|----------|-------------------|--------------|
| **ALL** | ~30 metrics | Vegas Lines, Team Stats, Game Environment |
| **QB** | 10 metrics | Pressure Rate, Pass Block Rate, Scramble Tendency |
| **RB** | 12 metrics | Goal-Line Role, TD Equity, Yards Before Contact |
| **WR** | 15 metrics | Target Volume, Air Yards, Deep Ball Accuracy |
| **TE** | 10 metrics | Route Participation, RZ Target Efficiency, EPA/Target |
| **K** | 3 metrics | Team RZ TD%, Accuracy by Distance, Dome vs Outdoor |

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

## Quick Reference Tables

### HIGH Priority Metrics (Pursue First)

| # | Metric | Position | Why HIGH Priority |
|---|--------|----------|-------------------|
| 1 | Target Volume/Share | WR, TE, RB | Critical for weekly decisions |
| 2 | QB Context | WR, TE | Affects all pass-catchers |
| 4 | Vegas Lines | ALL | Game environment predictor |
| 12 | Implied Team Total | ALL | More precise than O/U |
| 21 | WOPR | WR, TE | Weighted opportunity metric |
| 22 | xFP | ALL | Expected fantasy points baseline |
| 39 | Team RZ TD% | K | K scoring differential |
| 40 | Kicker Accuracy | K | 2025 record accuracy |
| 42 | Route Participation | TE | TE usage indicator |
| 46 | Goal-Line Role | RB | TD equity determinant |
| 49 | Role Designation | RB | Workload security |
| 50 | Receiving Share | RB | Pass-catching RB value |
| 52 | Pass Block Rate | QB | QB protection quality |
| 53 | Pressure Rate | QB | QB performance under pressure |

### Position-Specific Metrics

**Kicker (3 metrics):**
- 39: Team Red Zone TD%
- 40: Kicker Accuracy by Distance
- 41: Dome vs Outdoor

**Tight End (4 metrics):**
- 42: Route Participation Rate
- 43: Red Zone Target Efficiency
- 44: EPA Per Target
- 45: Role Security

**Running Back (6 metrics):**
- 46: Goal-Line Role
- 47: TD Equity
- 48: Yards Before Contact
- 49: Role Designation
- 50: Receiving Share
- 51: Carries Inside 20-Yard Line

**Quarterback (4 metrics):**
- 52: Pass Block Rate (protection)
- 53: Pressure Rate
- 3: Weather Sensitivity
- Various passing metrics (24-26, 32)

**Wide Receiver (3 metrics):**
- 54: Deep Ball Accuracy
- 55: Target Depth Distribution
- 56: Red Zone Involvement
- 57: 3rd Down Conversion Rate
- 58: Total Opportunity Share

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

These 58 metrics address gaps including:
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

## Tracking Progress

**Primary Tracker:** `RESEARCH_PROGRESS.md`

- Real-time status of all 58 metrics
- Links to completed research documents
- Progress by priority tier (HIGH/MEDIUM/LOW)

**Update After Each Metric:**
1. Mark status (⏳ → 🔍 → ✅)
2. Add data source
3. Note historical availability
4. Link to research doc

---

## Related Documentation

| Document | Purpose |
|----------|---------|
| `TEMPLATE.md` | Template for creating new metric research docs |
| `RESEARCH_PROGRESS.md` | Real-time tracking of all 58 metrics |
| `../scoring_gap_analysis.md` | Source document identifying all 58 metrics |
| `../ESPN_NFL_Game_Data_Research_Report.md` | ESPN API research reference |
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

✅ **Standardized Research** - All 58 metrics use same template for consistency

✅ **Historical Data Focus** - Simulation validation is a critical requirement

✅ **Priority-Driven** - HIGH priority metrics researched first

✅ **Implementation-Ready** - Research docs provide schema, dependencies, effort estimates

✅ **Comprehensive** - Covers 6 categories: gaps, reviews, projections, position-specific

---

*This documentation is maintained as part of the fantasy football helper scripts project. For questions or updates, see `feature-updates/espn-api-metric-research/` for planning details.*

**Last Updated:** 2025-12-20
