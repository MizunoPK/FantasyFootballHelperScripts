# Epic Request: QB Quality Scoring Integration (M12)

**File Location:** `.shamt/epics/requests/metrics/metric-12-qb-quality-v2.md`

---

## Epic Overview

**Epic Name:** QB Quality Scoring Integration (M12)

**Date:** 2026-03-09

**Requested By:** User

**Epic Type:** Feature Implementation

**Estimated Complexity:** Medium

---

## Problem Statement

**What problem does this epic solve?**

The player scoring algorithm does not account for the quality of a WR, TE, or RB's QB when evaluating them. A WR catching passes from an elite QB has significantly more fantasy upside than the same WR on a team with a poor QB. Without this metric, players on bad QB teams are overrated and players on great QB teams are underrated.

**Why is this important?**

QB quality is a major context factor for all pass catchers. Expected improvement: 8-12% in WR/TE recommendation accuracy and 4-6% for RBs. This metric affects all three modes.

**Who is affected?**

Fantasy managers evaluating or comparing WR, TE, and RB players.

---

## Goals & Success Metrics

**Primary Goals:**
1. Implement a QB Quality calculator that produces a composite QB score from multiple performance dimensions
2. Apply the QB score as a position-weighted modifier for pass catchers on that team
3. Configure composite weights, tier thresholds, and position-specific weights

**Success Metrics:**
- WR/TE on elite QB teams score higher than equivalent players on poor QB teams
- 8-12% improvement in WR/TE accuracy evaluations
- Composite QB score uses weighted combination of fantasy PPG, completion%, TD:INT, and YPA
- All unit tests passing

**Out of Scope (Explicitly Not Included):**
- Direct evaluation of the QB themselves (covered by M02, M03, M06, M07)
- DST evaluation

---

## Requirements

### Functional Requirements

1. **Composite QB Score**
   - Calculate QB score as weighted combination of: fantasy PPG (40%), completion% (20%), TD:INT ratio (25%), yards per attempt (15%)
   - Normalize to a 0-100 scale
   - Classify into ELITE (≥80), GOOD (65-79), AVERAGE (45-64), POOR (25-44), VERY_POOR (<25)

2. **Position-Specific Application**
   - WR: QB quality has high weight (2.5) — most dependent on QB
   - TE: Moderate weight (2.0)
   - RB: Lower weight (1.0) — least dependent on QB passing

3. **Team Lookup**
   - Must look up the player's QB by team to apply the modifier

4. **Scoring Integration**
   - Apply QB quality multiplier to WR/TE/RB score
   - Require minimum QB games played for valid tier

### Non-Functional Requirements

- **Performance:** QB composite scores should be cached per scoring run (same QB evaluated for all teammates)

### Technical Requirements

- **Dependencies:** `FantasyPlayer` (all QB metrics), `ConfigManager`, `PlayerManager` (QB lookup by team)
- **Integrations:** `player_scoring.py`

---

## Research & Background

**Current State:** No QB quality scoring step exists for pass catchers.

**Research Findings:**
- QB data available in `qb_data.json` with `actual_points`, `passing.completions`, `passing.pass_attempts`, `passing.pass_tds`, `passing.interceptions`, `passing.pass_yds`
- Position-specific weights appropriate: WR most impacted, RB least impacted
- `PlayerManager.get_players_by_team()` required to look up the team's QB

**Alternative Approaches Considered:**
1. **Fantasy PPG only:** Simpler but misses efficiency dimensions
2. **Composite score (Recommended):** More robust, handles different QB archetypes (efficient vs. volume)

### Technical Constraints

**Known Limitations:**
- Teams with multiple QBs (injury replacement) need careful handling
- QB must have minimum games to produce valid composite score

---

## Initial Feature Breakdown (Preliminary)

**Proposed Features:**

1. **Feature 1:** QB Quality Calculator Module
   - **Purpose:** Compute composite QB score from multiple metrics; return (multiplier, tier)
   - **Key Components:** Weighted composite calculation, normalization, tier classification, caching

2. **Feature 2:** Scoring Pipeline Integration
   - **Purpose:** Apply QB quality modifier to WR/TE/RB scores based on team QB
   - **Key Components:** `_apply_qb_quality_scoring()` method, QB lookup by team, position-specific weights

3. **Feature 3:** Configuration
   - **Purpose:** Externalize composite weights, tier thresholds, position weights
   - **Key Components:** `QB_QUALITY_SCORING` config block with position sub-configs

4. **Feature 4:** Unit Tests
   - **Purpose:** Verify composite score calculation, position-specific weights, team QB lookup
   - **Key Components:** Elite QB scenario, poor QB scenario, all three positions

---

## Dependencies & Risks

### External Dependencies

- **PlayerManager.get_players_by_team():** Required to look up QB by team

### Risks & Mitigation

| Risk | Impact | Probability | Mitigation Strategy |
|------|--------|-------------|---------------------|
| Multi-QB teams (injury replacement) | Medium | Medium | Use highest-game-count QB or most recent starter |
| QB cache invalidation | Low | Low | Cache is per-run, not persisted |
| QB with insufficient data | Low | Low | Return neutral multiplier for INSUFFICIENT_DATA |

---

## Timeline & Resources

**Estimated Timeline:** 3-4 days

**Team Members Required:**
- Developer: TBD

---

## Implementation Considerations

### Existing Codebase Integration

**Areas of the Codebase That May Require Changes:**
- `league_helper/util/player_scoring.py`: Add QB quality scoring step for WR/TE/RB
- `league_helper/util/PlayerManager.py`: Verify QB lookup by team is available
- `data/league_config.json`: Add `QB_QUALITY_SCORING` config block

**New Areas That May Need Creation:**
- `league_helper/util/QBQualityCalculator.py`

**Coding Practices to Follow:**
- Cache QB composite scores per run to avoid recalculation for every teammate
- Position guard: WR, TE, RB only (not for QB themselves)
- Follow existing Calculator class pattern
- Type hints, Google docstrings, error_context(), LoggingManager

### Testing Strategy (High-Level)

- **Unit Tests:** Composite score calculation verified against known inputs; ELITE QB boosts WR/TE/TE; VERY_POOR QB penalizes; position weights applied correctly; WR affected more than RB
- **Integration Tests:** QB lookup by team works correctly in full scoring run

---

## Open Questions

1. **Multi-QB teams:** If a team used 2+ QBs this season, which QB score is used for teammate evaluation?
   - **Status:** Unanswered

2. **Composite weights:** Are the proposed weights (40% PPG, 25% TD:INT, 20% comp%, 15% YPA) correct, or should they be adjusted?
   - **Status:** Unanswered

---

## References

- **Related Docs:** `player_scoring.py`, `data/player_data/qb_data.json`, `PlayerManager.py`
- **Related Epics:** M02 (QB Rushing Upside), M03 (Pass Attempts), M06 (Completion%), M07 (TD:INT Ratio), M01 (Target Volume)
- **External Resources:** N/A

---

## Next Steps

**To proceed with this epic:**
1. User reviews this request
2. User says "Start S1 for QB Quality Scoring Integration"
3. Agent reads `.shamt/guides/stages/s1/s1_epic_planning.md`
4. Agent creates git branch and FF-{N} folder during S1
5. Agent runs S1 Discovery Phase to refine this request

**This request file remains in `.shamt/epics/requests/` until S1 creates the epic folder.**
