# Team Ranking Research - Questions for Clarification

**Date**: 2025-11-01
**Objective**: Team ranking accuracy research and report

---

## Context

Based on initial codebase research, the current team ranking system uses:
- **Offensive Rank**: `totalPointsPerGame` from ESPN team stats
- **Defensive Rank**: `totalTakeaways` from ESPN team stats
- **Position-Specific Defense**: Calculated internally from fantasy points allowed per position

Your concern is that these rankings may not properly represent actual team strength. I've identified several potential areas for improvement.

---

## Questions

### Q1: Scope of Analysis - Which Rankings Need Review?

Which team ranking values should the report focus on analyzing and potentially improving?

**Options:**
1. **Offensive rankings only** - Focus on improving offensive_rank calculation
2. **Defensive rankings only** - Focus on improving defensive_rank calculation
3. **Position-specific defense only** - Focus on def_vs_qb_rank, def_vs_rb_rank, etc.
4. **All rankings** - Comprehensive review of all three ranking types

**Recommendation**: All rankings (Option 4) - Since you expressed concern about both offensive and positional defense rankings, a comprehensive analysis would be most valuable.

**Your Answer**: All rankings

---

### Q2: Defensive Ranking Metric - Takeaways vs Points Allowed?

The current defensive ranking uses `totalTakeaways` (interceptions + fumbles recovered). However, takeaways are:
- **Volatile**: Can vary wildly week-to-week
- **Unpredictable**: Hard to forecast or rely on
- **Not directly correlated**: Doesn't always reflect overall defensive quality

ESPN also provides `pointsPerGameAllowed` which is:
- **Stable**: More consistent week-to-week
- **Predictable**: Better reflects sustained defensive performance
- **Direct measure**: Points allowed directly impacts fantasy outcomes

Should the report recommend switching from `totalTakeaways` to `pointsPerGameAllowed` for defensive rankings?

**Options:**
1. **Keep totalTakeaways** - Maintain current approach
2. **Switch to pointsPerGameAllowed** - Use more stable metric
3. **Combine both metrics** - Create composite score using both
4. **Research and recommend** - Analyze correlation with fantasy outcomes and recommend best approach

**Recommendation**: Research and recommend (Option 4) - The report should analyze which metric (or combination) best predicts fantasy player performance.

**Your Answer**: Option 4

---

### Q3: Offensive Ranking Metric - Single vs Multiple Metrics?

Current offensive ranking uses only `totalPointsPerGame`. ESPN provides many other offensive metrics:
- `totalYards` - Total offensive yardage
- Passing yards, rushing yards
- Red zone efficiency
- 3rd down conversion rate
- Yards per play

Should offensive rankings consider multiple metrics for a more comprehensive assessment?

**Options:**
1. **Keep totalPointsPerGame only** - Simplest, most direct measure
2. **Add totalYards as secondary factor** - Consider both scoring and yardage
3. **Create composite offensive score** - Weighted combination of multiple metrics
4. **Research and recommend** - Analyze which approach best predicts fantasy outcomes

**Recommendation**: Research and recommend (Option 4) - The report should evaluate whether additional metrics improve ranking accuracy.

**Your Answer**: Option 4

---

### Q4: Position-Specific Defense Calculation - Current Method OK?

The position-specific defense rankings (def_vs_qb_rank, etc.) are calculated by:
1. Summing fantasy points allowed by each defense to each position
2. Only using actual game data (weeks 1 to current week)
3. Ranking 1-32 where lower points allowed = better rank

This method was implemented in the "strength_of_schedule" update and follows industry standard practices.

Do you have concerns about this calculation method, or is it working well?

**Options:**
1. **Current method is good** - No changes needed, focus report on offensive/defensive ranks only
2. **Needs improvement** - Report should analyze and propose better calculation methods
3. **Unsure** - Report should evaluate current method and recommend if changes are needed

**Recommendation**: Current method is good (Option 1) - This calculation follows industry best practices and directly measures what matters (fantasy points allowed).

**Your Answer**: Option 3

---

### Q5: Report Detail Level - Technical vs Summary?

How detailed should the analysis report be?

**Options:**
1. **Executive summary** - High-level findings and recommendations only (2-3 pages)
2. **Moderate detail** - Findings, analysis, examples, and recommendations (5-10 pages)
3. **Comprehensive technical** - Deep analysis with data examples, correlation studies, code snippets, API responses (15+ pages)

**Recommendation**: Moderate detail (Option 2) - Provides thorough analysis without overwhelming detail.

**Your Answer**: Option 2

---

### Q6: Implementation Recommendations - Include in Report?

Should the report include specific implementation recommendations (which code to change, exact formulas to use, etc.)?

**Options:**
1. **Analysis only** - Just evaluate current approach and identify issues
2. **Recommendations included** - Suggest specific improvements with formulas/approaches
3. **Full implementation plan** - Include exact code changes, API endpoints, calculation formulas

**Recommendation**: Recommendations included (Option 2) - Provide actionable suggestions without writing actual code.

**Your Answer**: Option 2

---

## Summary

Please answer each question above so I can tailor the research report to your specific needs. If you're unsure about any question, the recommendations provided are based on best practices for this type of analysis.

Once I have your answers, I'll proceed with creating the comprehensive team ranking research report in `docs/team_rankings/`.
