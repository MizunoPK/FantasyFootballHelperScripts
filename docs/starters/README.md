# Starter Helper Documentation

This folder contains guides and assessments for weekly fantasy football start/sit decisions.

## Contents

```
docs/starters/
├── README.md                    # This file
├── starter_research_guide.md    # How-to guide for agents conducting research
└── assessments/                 # Weekly analysis reports
    ├── week15_wr_analysis_report.md
    ├── week15_rb_analysis_report.md
    └── ...
```

## Quick Reference

### For Agents

When a user asks for start/sit advice:

1. **Read** `starter_research_guide.md` for the methodology
2. **Follow** the 10-Factor Analysis Model
3. **Execute** the search strategy (parallel searches)
4. **Save** the completed report to `assessments/week{N}_{position}_analysis_report.md`

### Key Files

| File | Purpose |
|------|---------|
| `starter_research_guide.md` | Comprehensive methodology for start/sit research |
| `assessments/` | Completed weekly analysis reports |

## The 10-Factor Analysis Model

Every start/sit decision evaluates:

1. **Projections** - Consensus weekly fantasy point projections
2. **Matchup Quality** - Opponent defensive ranking vs. position
3. **Recent Performance** - Last 3-5 game trends
4. **Target/Touch Volume** - Opportunity share
5. **Game Environment** - Vegas O/U, spread, implied total
6. **Weather Conditions** - Temperature, wind (outdoor games)
7. **Team Context** - O-line, QB performance, scheme
8. **Opponent Context** - Secondary injuries, coverage
9. **Injury Status** - Player's own health
10. **Floor/Ceiling** - Range of outcomes

## Report Naming Convention

```
week{N}_{position}_analysis_report.md

Examples:
- week15_wr_analysis_report.md
- week15_rb_analysis_report.md
- week16_qb_analysis_report.md
```

## Integration with Scoring System

The research methodology in this folder is complementary to the automated scoring system in `league_helper/`. Key gaps identified in manual research that aren't covered by the scoring algorithm:

| Manual Research Metric | Scoring System Coverage |
|-----------------------|------------------------|
| Target Volume/Share | Not covered |
| QB Context | Not covered |
| Vegas O/U Lines | Not covered |
| Teammate Injuries | Not covered |
| Weather (basic) | Steps 11-12 |
| Matchup | Step 6 |
| Recent Performance | Step 5 |

See `feature-updates/scoring_gap_analysis.md` for details on potential scoring system enhancements.
