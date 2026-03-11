# Epic Request: Recent Form Scoring Integration (M34)

**File Location:** `.shamt/epics/requests/metrics/metric-34-recent-form-v2.md`

---

## Epic Overview

**Epic Name:** Recent Form Scoring Integration (M34)

**Date:** 2026-03-09

**Requested By:** User

**Epic Type:** Feature Implementation

**Estimated Complexity:** Small

---

## Problem Statement

**What problem does this epic solve?**

The player scoring algorithm does not account for recent performance trends. A player who averaged 10 PPG on the season but has scored 20+ in each of the last 4 games is on a hot streak that season-long averages completely miss. Similarly, a star player in a 4-game slump is overvalued by their season average.

**Why is this important?**

Recent form (rolling 4-week average vs. season average) captures momentum, usage changes, and short-term trends that are highly predictive for weekly fantasy decisions. Expected improvement: 5-8% in all-position weekly decision accuracy.

**Who is affected?**

Fantasy managers making weekly lineup decisions for all positions (QB, RB, WR, TE, K, DST).

---

## Goals & Success Metrics

**Primary Goals:**
1. Implement a Recent Form calculator comparing the last 4 active games to season average
2. Classify form into 5 tiers: HOT, WARM, NEUTRAL, COLD, ICE_COLD
3. Apply across all positions
4. Exclude bye weeks from the rolling window

**Success Metrics:**
- Hot streak players boosted; cold streak players penalized
- 5-8% improvement in weekly decision accuracy
- HOT = recent avg ≥120% of season avg; ICE_COLD = <80%
- All unit tests passing

**Out of Scope (Explicitly Not Included):**
- Volume trends (covered by M17 Target Share Trend)
- Boom/bust patterns (covered by M37)

---

## Requirements

### Functional Requirements

1. **Recent Form Calculation**
   - Use `actual_points` weekly array
   - Filter out 0-point bye weeks
   - Get last N active games (default window = 4)
   - Calculate form ratio = recent average / season average
   - Classify: HOT (≥1.20), WARM (1.08-1.19), NEUTRAL (0.92-1.07), COLD (0.80-0.91), ICE_COLD (<0.80)

2. **Scoring Integration**
   - Apply tier-based multiplier to all positions
   - Return neutral when insufficient data (fewer than 2 active games)
   - Consider reduced weight for early season (fewer than 4 games)

### Non-Functional Requirements

- **Universality:** Applies to all positions equally (no position guard needed)

### Technical Requirements

- **Dependencies:** `FantasyPlayer` (actual_points), `ConfigManager`
- **Integrations:** `player_scoring.py`

---

## Research & Background

**Current State:** No recent form scoring step exists.

**Research Findings:**
- `actual_points` available in all position data JSON files as a weekly array
- 4-week rolling window provides a good balance between recency and noise reduction
- Bye weeks stored as 0.0 — must be excluded from the active game list

**Alternative Approaches Considered:**
1. **3-week window:** More recent but noisier
2. **6-week window:** Smoother but misses rapid changes
3. **4-week window (Recommended):** Standard in industry; good balance

### Technical Constraints

**Known Limitations:**
- Injury return cases: player misses 4 weeks, returns — recent form starts with return game
- Weeks 1-4: insufficient window, reduce weight or skip

---

## Initial Feature Breakdown (Preliminary)

**Proposed Features:**

1. **Feature 1:** Recent Form Calculator Module
   - **Purpose:** Compare last N active games to season average; return (multiplier, tier)
   - **Key Components:** Bye week filtering, window extraction, form ratio calculation, tier classification

2. **Feature 2:** Scoring Pipeline Integration
   - **Purpose:** Add recent form as a universal scoring step for all positions
   - **Key Components:** `_apply_recent_form_scoring()` method with current_week parameter

3. **Feature 3:** Configuration (`RECENT_FORM_SCORING` block with window size, thresholds, multipliers)

4. **Feature 4:** Unit Tests (hot streak, cold streak, bye week exclusion, early season handling)

---

## Dependencies & Risks

### Risks & Mitigation

| Risk | Impact | Probability | Mitigation Strategy |
|------|--------|-------------|---------------------|
| Bye week miscounted as poor performance | Medium | Medium | Filter out 0-point weeks before calculation |
| Early season noise | Low | Low | Reduce weight or skip when fewer than 4 active games |

---

## Timeline & Resources

**Estimated Timeline:** 2-3 days

---

## Implementation Considerations

### Existing Codebase Integration

**Areas of the Codebase That May Require Changes:**
- `league_helper/util/player_scoring.py`: Add recent form scoring step for all positions
- `data/league_config.json`: Add `RECENT_FORM_SCORING` config block

**New Areas That May Need Creation:**
- `league_helper/util/RecentFormCalculator.py`

**Coding Practices to Follow:**
- Applies to all positions (no position guard)
- Requires `current_week` parameter to determine which weeks are "played"
- Type hints, docstrings, LoggingManager, error_context()

### Testing Strategy (High-Level)

- **Unit Tests:** HOT streak → boost; ICE_COLD → penalty; bye week in window correctly excluded; early season returns neutral; works for all positions (at least QB and WR tested)

---

## Open Questions

1. **Early season weight:** Should the weight be halved for weeks 1-4, or should the metric simply be skipped?
   - **Status:** Unanswered

2. **Window size:** Is 4 games the right default, or should it be configurable?
   - **Status:** Unanswered

---

## References

- **Related Docs:** `player_scoring.py`, all `data/player_data/*_data.json` files
- **Related Epics:** M17 (Target Share Trend), M37 (Boom/Bust Frequency)

---

## Next Steps

**To proceed with this epic:**
1. User reviews this request
2. User says "Start S1 for Recent Form Scoring Integration"
3. Agent reads `.shamt/guides/stages/s1/s1_epic_planning.md`
4. Agent creates git branch and FF-{N} folder during S1
5. Agent runs S1 Discovery Phase to refine this request

**This request file remains in `.shamt/epics/requests/` until S1 creates the epic folder.**
