# Epic Request: Target Share Trend Scoring Integration (M17)

**File Location:** `.shamt/epics/requests/metrics/metric-17-target-share-trend-v2.md`

---

## Epic Overview

**Epic Name:** Target Share Trend Scoring Integration (M17)

**Date:** 2026-03-09

**Requested By:** User

**Epic Type:** Feature Implementation

**Estimated Complexity:** Small

---

## Problem Statement

**What problem does this epic solve?**

The player scoring algorithm evaluates season-long target share averages but does not detect whether a player's target share is trending up or down in recent weeks. A WR whose target share jumped from 14% to 22% over the last 3 weeks is trending up and deserves a boost, while one whose share fell from 20% to 11% deserves a penalty.

**Why is this important?**

Recent target share trends are highly predictive of near-term fantasy production. They capture role changes (new starter, injury to teammate, scheme changes) that season-long averages miss. Expected improvement: 5-8% in WR/TE accuracy, particularly for Starter Helper mode.

**Who is affected?**

Fantasy managers making weekly lineup decisions for WR, TE, and RB players.

---

## Goals & Success Metrics

**Primary Goals:**
1. Implement a Target Share Trend calculator comparing last 3 weeks vs. prior 3 weeks
2. Classify the change into trending tiers (EXCELLENT through POOR)
3. Integrate into the player scoring pipeline as a conditional modifier

**Success Metrics:**
- Rising target share players boosted; declining ones penalized
- Only applies at week 7+ (requires 6 games of data for comparison)
- Expected 5-8% improvement in weekly decision accuracy
- All unit tests passing

**Out of Scope (Explicitly Not Included):**
- Season-long target share (M01 covers this)
- Target consistency/variance (M51)

---

## Requirements

### Functional Requirements

1. **Target Share Trend Calculation**
   - Compare recent 3-week target share to prior 3-week target share
   - Require at least week 7 of the season (needs 6+ active games)
   - Classify change into tiers: EXCELLENT (≥+15% change), GOOD, AVERAGE, POOR (≥-15% decline)
   - Requires team-level target totals for share calculation

2. **Scoring Integration**
   - Apply trend-based multiplier to WR/TE/RB score
   - Return neutral when insufficient data

### Technical Requirements

- **Dependencies:** `FantasyPlayer` (weekly targets), `ConfigManager`, team lookup for share calculation
- **Integrations:** `player_scoring.py`; depends on M01 Target Volume data availability

---

## Research & Background

**Current State:** No target share trend scoring step exists.

**Research Findings:**
- `receiving.targets` available in `wr_data.json`, `te_data.json`, `rb_data.json` as weekly arrays
- Trend window: last 3 active games vs. prior 3 active games
- Minimum season week 7 required for meaningful trend data

**Alternative Approaches Considered:**
1. **2-week vs. 4-week window:** Less stable than 3 vs. 3
2. **3-week vs. 3-week (Recommended):** Balance between recency and stability

### Technical Constraints

**Known Limitations:**
- Target share requires team-level context (same as M01)
- Cannot detect trends accurately before week 7

---

## Initial Feature Breakdown (Preliminary)

**Proposed Features:**

1. **Feature 1:** Target Share Trend Calculator Module
   - **Purpose:** Compare recent vs. prior target share; return (multiplier, tier)
   - **Key Components:** Window extraction, share calculation, trend comparison

2. **Feature 2:** Scoring Pipeline Integration
   - **Purpose:** Apply trend modifier to WR/TE/RB score
   - **Key Components:** `_apply_target_share_trend_scoring()` method, week check

3. **Feature 3:** Configuration (`TARGET_SHARE_TREND_SCORING` block)

4. **Feature 4:** Unit Tests (trending up, trending down, insufficient data)

---

## Dependencies & Risks

### External Dependencies

- **M01 (Target Volume):** Requires same team target aggregation infrastructure

### Risks & Mitigation

| Risk | Impact | Probability | Mitigation Strategy |
|------|--------|-------------|---------------------|
| Injury games inflate "trend down" signal | Low | Low | Track window using active games only |
| Early season insufficient data | Low | Low | Week 7+ check |

---

## Timeline & Resources

**Estimated Timeline:** 2-3 days

---

## Implementation Considerations

### Existing Codebase Integration

**Areas of the Codebase That May Require Changes:**
- `league_helper/util/player_scoring.py`: Add target share trend scoring step
- `data/league_config.json`: Add `TARGET_SHARE_TREND_SCORING` config block

**New Areas That May Need Creation:**
- `league_helper/util/TargetShareTrendCalculator.py`

**Coding Practices to Follow:**
- Position guard: WR, TE, RB
- Depends on team target aggregation; consider sharing with M01 calculator
- Type hints, docstrings, LoggingManager, error_context()

### Testing Strategy (High-Level)

- **Unit Tests:** Trending-up WR gets boost; trending-down WR gets penalty; pre-week-7 returns neutral; bye weeks excluded from windows

---

## Open Questions

1. **Window size:** Is 3 weeks vs. 3 weeks the right comparison, or should it be configurable?
   - **Status:** Unanswered

---

## References

- **Related Docs:** `player_scoring.py`, `data/player_data/wr_data.json`
- **Related Epics:** M01 (Target Volume), M51 (Target Consistency), M34 (Recent Form)

---

## Next Steps

**To proceed with this epic:**
1. User reviews this request
2. User says "Start S1 for Target Share Trend Scoring Integration"
3. Agent reads `.shamt/guides/stages/s1/s1_epic_planning.md`
4. Agent creates git branch and FF-{N} folder during S1
5. Agent runs S1 Discovery Phase to refine this request

**This request file remains in `.shamt/epics/requests/` until S1 creates the epic folder.**
