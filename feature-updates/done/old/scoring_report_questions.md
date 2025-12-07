# Scoring Algorithm Documentation - Questions for Clarification

## Overview

This questions file addresses ambiguities and implementation choices discovered during codebase research for the scoring documentation project.

---

## Format and Style Questions

### Q1: Documentation Format
**Question**: What format would you prefer for the metric reports?

**Options**:
1. **Markdown only** - Pure markdown with code blocks
2. **Markdown with embedded diagrams** - Include flowcharts/diagrams (requires mermaid or similar)
3. **Markdown with example outputs** - Include actual calculated examples in tables

**Recommendation**: Option 3 (Markdown with example outputs) - Provides the most practical value with concrete examples users can reference.

### Q2: ESPN API JSON Depth
**Question**: How detailed should the ESPN API JSON object analysis be?

**Options**:
1. **Full object dumps** - Show complete JSON structures (can be very long)
2. **Relevant excerpts** - Show only the specific fields used (more focused)
3. **Field path notation** - Document paths like `player.rankings['10'][*].averageRank` (most concise)

**Recommendation**: Option 2 with Option 3 - Show relevant excerpts with clear field paths for easy reference.

---

## Scope and Priority Questions

### Q3: Priority Order
**Question**: If time is limited, which metrics are highest priority to document first?

**Context**: 10 metrics × 8 requirements each = significant documentation effort

**Options**:
1. **Document in scoring order** (Normalization → ADP → Player Rating → ... → Injury)
2. **Document most complex first** (Performance, Bye Week, Schedule, then simpler ones)
3. **Document data-dependent first** (metrics requiring ESPN API analysis)

**Recommendation**: Option 2 - Tackle complex metrics first while context is fresh, simpler ones can be done quickly later.

**User Input Requested**: Would you like to prioritize specific metrics over others?

### Q4: Example Player Count
**Question**: You mentioned "top 20 players in each position" - should this be:

**Options**:
1. **Top 20 by fantasy points** (highest projected)
2. **Top 20 by final score** (after all metrics applied)
3. **Representative sample** (mix of high/mid/low tier players)

**Recommendation**: Option 3 - Show top 5, mid 5, and bottom 5 for each position to demonstrate metric effects across value tiers.

---

## Technical Details Questions

### Q5: Code Snippets
**Question**: Should the documentation include actual code snippets from the implementation?

**Options**:
1. **No code** - Prose descriptions only
2. **Simplified pseudocode** - Conceptual algorithms
3. **Actual Python code** - Real implementation snippets with line references

**Recommendation**: Option 3 - Include actual code snippets with file:line references for traceability.

### Q6: Configuration Values
**Question**: How should configuration values (thresholds, multipliers) be documented?

**Options**:
1. **Current values only** - Document what's currently in league_config.json
2. **Historical context** - Show if values changed over time
3. **Rationale included** - Explain why specific thresholds were chosen (if known)

**Recommendation**: Option 1 - Current values with notes if any have been recently updated (like player_rating fix).

---

## Mode-Specific Questions

### Q7: Mode Usage Detail
**Question**: For "which modes use this metric" - how detailed should this be?

**Modes identified that use scoring**:
- Add To Roster Mode (draft helper)
- Starter Helper Mode (roster optimizer)
- Trade Simulator Mode (trade analysis)

**Options**:
1. **List modes only** - Just name the modes
2. **Usage context** - Explain HOW each mode uses the metric
3. **Parameter differences** - Document if modes use different parameter settings

**Recommendation**: Option 2 - Provide context for HOW metrics are used in each mode (e.g., "Draft mode uses schedule=True for long-term value").

---

## Special Cases Questions

### Q8: Recent Changes
**Question**: How should recently changed systems (like player_rating) be documented?

**Context**: Player rating system was just updated (Nov 5, 2025) to use current week ROS rankings instead of stale pre-season data.

**Options**:
1. **Current state only** - Document only the new system
2. **Before/After** - Show old vs new approach with rationale
3. **Migration guide** - Include transition notes

**Recommendation**: Option 2 - Document current system with clear "Recent Update" section explaining the fix and why it matters.

---

## Data Source Questions

### Q9: players.csv Field Documentation
**Question**: Should field documentation include data types and valid ranges?

**Options**:
1. **Field name only** - Just identify which fields are used
2. **Field with type** - Include data type (float, int, string, etc.)
3. **Full specification** - Type, valid ranges, example values

**Recommendation**: Option 3 - Full specification helps understand data constraints and validation.

### Q10: Cross-References
**Question**: Should reports cross-reference each other when metrics interact?

**Example**: Performance metric uses ProjectedPointsManager which is also used in Normalization.

**Options**:
1. **No cross-references** - Each report standalone
2. **See also links** - Light references to related metrics
3. **Dependency diagrams** - Visual showing metric relationships

**Recommendation**: Option 2 with Option 3 - Include "See Also" sections and one overall dependency diagram in README.md.

---

## Summary of Recommendations

Based on codebase research, I recommend:

1. **Format**: Markdown with example outputs in tables
2. **API JSON**: Relevant excerpts + field path notation
3. **Priority**: Complex metrics first (Performance, Bye Week, Schedule)
4. **Examples**: Representative samples (top/mid/bottom tier players)
5. **Code**: Include actual Python snippets with line references
6. **Config**: Current values with recent update notes
7. **Modes**: Usage context explaining HOW metrics are used
8. **Changes**: Before/After for recently updated systems
9. **Fields**: Full specification (type, range, examples)
10. **Cross-refs**: "See Also" sections + dependency diagram

**Please provide your preferences for any questions where you'd like something different from the recommendation.**

---

## Additional Questions

**Q11**: Are there any specific metrics you're particularly interested in understanding in depth?

**Q12**: Should the documentation include troubleshooting sections (e.g., "Why is my player's score lower than expected?")?

**Q13**: Target audience - is this for developers modifying the code, or users trying to understand scoring decisions?
