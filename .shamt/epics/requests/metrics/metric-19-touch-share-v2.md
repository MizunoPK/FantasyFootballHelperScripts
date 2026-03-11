# Epic Request: Touch Share Scoring Integration (M19)

**File Location:** `.shamt/epics/requests/metrics/metric-19-touch-share-v2.md`

---

## Epic Overview

**Epic Name:** Touch Share Scoring Integration (M19)

**Date:** 2026-03-09

**Requested By:** User

**Epic Type:** Feature Implementation

**Estimated Complexity:** Small

---

## Problem Statement

**What problem does this epic solve?**

The player scoring algorithm does not account for a player's total offensive involvement relative to their team. An RB or WR with a high share of the team's total touches (carries + targets) has a guaranteed volume floor that players with low touch share lack. Without this metric, high-touch-share players are not appropriately valued for their opportunity dominance.

**Why is this important?**

Touch share captures the complete opportunity picture for RBs and WRs by combining rushing and receiving volume. Expected improvement: 10-14% in RB/WR opportunity assessment accuracy.

**Who is affected?**

Fantasy managers evaluating or comparing RB and WR players, especially in PPR formats where both carry and target volume matter.

---

## Goals & Success Metrics

**Primary Goals:**
1. Implement a Touch Share calculator that expresses a player's combined carries + targets as a percentage of total team touches
2. Apply position-specific tier thresholds (RB and WR differ)
3. Integrate into the player scoring pipeline

**Success Metrics:**
- Bell cow RBs (30%+ touch share) ranked significantly higher than committee backs
- WRs with rushing work (Deebo Samuel type) appropriately valued
- 10-14% improvement in RB/WR evaluation accuracy
- All unit tests passing

**Out of Scope (Explicitly Not Included):**
- Touch share for QB, TE, K, DST

---

## Requirements

### Functional Requirements

1. **Touch Share Calculation**
   - Player touches = season rushing attempts + season receiving targets
   - Team total touches = all players' rushing attempts + all players' receiving targets
   - Touch share = player touches / team total touches
   - Position-specific tiers: RB EXCELLENT ≥30%, WR EXCELLENT ≥18%

2. **Scoring Integration**
   - Apply position-and-tier-based multiplier
   - Requires team player aggregation

3. **Touches Per Game**
   - Also calculate average touches per game for the reason string

### Non-Functional Requirements

- **Performance:** Team touch totals should be cached per run

### Technical Requirements

- **Dependencies:** `FantasyPlayer` (rushing attempts + receiving targets), `ConfigManager`, `PlayerManager.get_players_by_team()`
- **Integrations:** `player_scoring.py`

---

## Research & Background

**Current State:** No touch share scoring step exists.

**Research Findings:**
- `rushing.attempts` available in RB/WR/QB data; `receiving.targets` available in RB/WR/TE data
- RB EXCELLENT: ≥30% touch share; WR EXCELLENT: ≥18%
- Team total includes all positions' carrying and receiving touches

**Alternative Approaches Considered:**
1. **Carry share only (for RBs):** Misses PPR value from targets
2. **Target share only (for WRs):** Misses rushing upside (Deebo Samuel type)
3. **Combined touch share (Recommended):** Captures complete opportunity profile

### Technical Constraints

**Known Limitations:**
- Team aggregation covers all positions; QB rushing included in team total
- Need to decide whether to include QB rushing attempts in team total

---

## Initial Feature Breakdown (Preliminary)

**Proposed Features:**

1. **Feature 1:** Touch Share Calculator Module
   - **Purpose:** Calculate touch share percentage; return (multiplier, tier) with position-specific thresholds
   - **Key Components:** Touches calculation, team aggregation, position-specific tiers

2. **Feature 2:** Scoring Pipeline Integration
   - **Purpose:** Add touch share as a scoring step for RB and WR
   - **Key Components:** `_apply_touch_share_scoring()`, team player lookup

3. **Feature 3:** Configuration (`TOUCH_SHARE_SCORING` with WR and RB sub-configs)

4. **Feature 4:** Unit Tests (bell cow, WR with rush work, committee back, bye weeks)

---

## Dependencies & Risks

### External Dependencies

- **PlayerManager.get_players_by_team():** Required for team touch aggregation

### Risks & Mitigation

| Risk | Impact | Probability | Mitigation Strategy |
|------|--------|-------------|---------------------|
| Team aggregation performance | Medium | Medium | Cache team totals per scoring run |
| QB rushing in team total | Low | Low | Configurable option to include/exclude QB rushing |

---

## Timeline & Resources

**Estimated Timeline:** 3-4 days

---

## Implementation Considerations

### Existing Codebase Integration

**Areas of the Codebase That May Require Changes:**
- `league_helper/util/player_scoring.py`: Add touch share scoring step for RB/WR
- `league_helper/util/PlayerManager.py`: Verify `get_players_by_team()` available
- `data/league_config.json`: Add `TOUCH_SHARE_SCORING` with RB and WR sub-configs

**New Areas That May Need Creation:**
- `league_helper/util/TouchShareCalculator.py`

**Coding Practices to Follow:**
- Position guard: RB and WR only
- Cache team touch totals per scoring run
- Type hints, Google docstrings, error_context(), LoggingManager

### Testing Strategy (High-Level)

- **Unit Tests:** Bell cow RB EXCELLENT; WR with rush work valued correctly; committee back POOR; bye weeks excluded from touches; position-specific thresholds verified

---

## Open Questions

1. **QB rushing in team total:** Should QB rushing attempts be included in the team total touches denominator?
   - **Status:** Unanswered

2. **PPR weighting:** Should targets be weighted more heavily than carries (e.g., 1.5x) for PPR formats?
   - **Status:** Unanswered

---

## References

- **Related Docs:** `player_scoring.py`, `data/player_data/rb_data.json`, `data/player_data/wr_data.json`
- **Related Epics:** M01 (Target Volume), M04 (Carries Per Game), M11 (RB Receiving Workload), M50 (Touch Consistency)

---

## Next Steps

**To proceed with this epic:**
1. User reviews this request
2. User says "Start S1 for Touch Share Scoring Integration"
3. Agent reads `.shamt/guides/stages/s1/s1_epic_planning.md`
4. Agent creates git branch and FF-{N} folder during S1
5. Agent runs S1 Discovery Phase to refine this request

**This request file remains in `.shamt/epics/requests/` until S1 creates the epic folder.**
