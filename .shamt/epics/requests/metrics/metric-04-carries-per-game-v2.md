# Epic Request: Carries Per Game Scoring Integration (M04)

**File Location:** `.shamt/epics/requests/metrics/metric-04-carries-per-game-v2.md`

---

## Epic Overview

**Epic Name:** Carries Per Game Scoring Integration (M04)

**Date:** 2026-03-09

**Requested By:** User

**Epic Type:** Feature Implementation

**Estimated Complexity:** Small

---

## Problem Statement

**What problem does this epic solve?**

The player scoring algorithm does not account for RB carry volume. An RB who receives 20+ carries per game is a bell cow with a guaranteed scoring floor, while one averaging 5-8 carries is a committee back with much lower ceiling and floor. Without this metric, the scoring pipeline cannot distinguish these meaningfully different workload profiles.

**Why is this important?**

Carries per game is the most direct measure of RB opportunity. Expected improvement: 10-14% in RB evaluation accuracy, with the largest impact in Add To Roster and Trade Simulator modes.

**Who is affected?**

Fantasy managers evaluating or comparing RB players.

---

## Goals & Success Metrics

**Primary Goals:**
1. Implement a Carries Per Game calculator with 5-tier classification (EXCELLENT through VERY_POOR)
2. Integrate the calculator into the player scoring pipeline
3. Configure thresholds and multipliers in the league config

**Success Metrics:**
- Bell cow RBs (20+ carries/game) ranked significantly above committee backs
- 10-14% improvement in RB evaluation accuracy
- All unit tests passing

**Out of Scope (Explicitly Not Included):**
- Receiving volume for RBs (covered by M11 RB Receiving Workload)
- Yards per carry efficiency (covered by M08)

---

## Requirements

### Functional Requirements

1. **Carries Per Game Calculation**
   - Calculate average carries per game from weekly data
   - Exclude bye weeks (0 carries with no game activity)
   - Classify into 5 tiers: EXCELLENT (≥20), GOOD (15-19), AVERAGE (10-14), POOR (5-9), VERY_POOR (<5)

2. **Scoring Integration**
   - Apply tier-based multiplier to RB score
   - Require minimum games played

### Non-Functional Requirements

- **Maintainability:** 5-tier thresholds configurable in config

### Technical Requirements

- **Dependencies:** `FantasyPlayer` (rushing attempts data), `ConfigManager`
- **Integrations:** `player_scoring.py` scoring pipeline

---

## Research & Background

### Existing Solutions Analysis

**Current State:**
No carries per game scoring step in `player_scoring.py`.

**Research Findings:**
- `rushing.attempts` available in `rb_data.json` as weekly array
- 5 tiers appropriate: bell cow (20+), workhorse (15-19), committee lead (10-14), limited (5-9), backup (<5)

**Alternative Approaches Considered:**
1. **3 tiers:** Less granular, less useful for distinguishing workload profiles
2. **5 tiers (Recommended):** Better granularity for the full range of RB workload profiles

### Technical Constraints

**Known Limitations:**
- Committee RBs may have variable carries week-to-week; season average is used

---

## Initial Feature Breakdown (Preliminary)

**Proposed Features:**

1. **Feature 1:** Carries Per Game Calculator Module
   - **Purpose:** Calculate carries/game and return (multiplier, tier) with 5-tier classification
   - **Key Components:** Calculation logic, bye week exclusion, 5-tier system

2. **Feature 2:** Scoring Pipeline Integration
   - **Purpose:** Add as RB-specific scoring step
   - **Key Components:** `_apply_carries_per_game_scoring()` method

3. **Feature 3:** Configuration
   - **Purpose:** Externalize 5-tier thresholds and multipliers
   - **Key Components:** `CARRIES_PER_GAME_SCORING` config block

4. **Feature 4:** Unit Tests
   - **Purpose:** Verify all 5 tier boundaries and edge cases
   - **Key Components:** Bell cow, committee back, backup, bye week handling

---

## Dependencies & Risks

### External Dependencies

None beyond existing codebase.

### Risks & Mitigation

| Risk | Impact | Probability | Mitigation Strategy |
|------|--------|-------------|---------------------|
| Bye week detection via 0 carries | Low | Low | Check for any game activity to distinguish bye from 0-carry game |

---

## Timeline & Resources

**Estimated Timeline:** 2 days

**Team Members Required:**
- Developer: TBD

---

## Implementation Considerations

### Existing Codebase Integration

**Areas of the Codebase That May Require Changes:**
- `league_helper/util/player_scoring.py`: Add carries per game scoring step
- `data/league_config.json`: Add `CARRIES_PER_GAME_SCORING` config block

**New Areas That May Need Creation:**
- `league_helper/util/CarriesPerGameCalculator.py`

**Coding Practices to Follow:**
- Follow existing Calculator class pattern
- Position guard: RB only
- Type hints, docstrings, LoggingManager, error_context()

### Testing Strategy (High-Level)

- **Unit Tests:** All 5 tiers tested; bye week exclusion; minimum games guard
- **Integration Tests:** Carries scoring step fires only for RBs

---

## Open Questions

1. **Bye week detection:** Should 0-carry games be excluded only when all rushing/receiving stats are 0, or based on a game activity flag?
   - **Status:** Unanswered

---

## References

- **Related Docs:** `player_scoring.py`, `data/player_data/rb_data.json`
- **Related Epics:** M08 (Yards Per Carry), M11 (RB Receiving Workload), M19 (Touch Share), M50 (Touch Consistency)
- **External Resources:** N/A

---

## Next Steps

**To proceed with this epic:**
1. User reviews this request
2. User says "Start S1 for Carries Per Game Scoring Integration"
3. Agent reads `.shamt/guides/stages/s1/s1_epic_planning.md`
4. Agent creates git branch and FF-{N} folder during S1
5. Agent runs S1 Discovery Phase to refine this request

**This request file remains in `.shamt/epics/requests/` until S1 creates the epic folder.**
