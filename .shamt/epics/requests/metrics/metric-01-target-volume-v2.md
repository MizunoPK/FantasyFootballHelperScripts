# Epic Request: Target Volume Scoring Integration (M01)

**File Location:** `.shamt/epics/requests/metrics/metric-01-target-volume-v2.md`

---

## Epic Overview

**Epic Name:** Target Volume Scoring Integration (M01)

**Date:** 2026-03-09

**Requested By:** User

**Epic Type:** Feature Implementation

**Estimated Complexity:** Small

---

## Problem Statement

**What problem does this epic solve?**

The player scoring algorithm does not account for target volume, meaning WR, TE, and RB players are evaluated without considering how many receiving opportunities they get. A WR who sees 12 targets per game is fundamentally more valuable than one who sees 4, even if their per-target efficiency is similar. Without this metric, the scoring pipeline undervalues high-volume receivers and overvalues low-volume ones.

**Why is this important?**

Target volume is one of the most predictive metrics for fantasy football receiver production. Incorporating it is expected to improve WR/TE/RB recommendation accuracy by 8-10%. It directly affects Add To Roster, Starter Helper, and Trade Simulator modes.

**Who is affected?**

Fantasy managers using the tool to evaluate or compare WR, TE, and RB players.

---

## Goals & Success Metrics

**Primary Goals:**
1. Implement a Target Volume calculator that determines a tier (EXCELLENT, GOOD, AVERAGE, POOR) based on target share percentage (WR/TE) or targets per game (RB)
2. Integrate the calculator as a scoring step in the player scoring pipeline
3. Configure thresholds and multipliers in the league config

**Success Metrics:**
- 8-10% improvement in WR/TE/RB accuracy evaluations
- High-volume receivers ranked higher than equal-efficiency low-volume receivers
- All unit tests passing

**Out of Scope (Explicitly Not Included):**
- Changes to how target data is fetched
- Historical multi-season data analysis

---

## Requirements

### Functional Requirements

1. **Target Volume Calculation**
   - For WR/TE: calculate target share as a percentage of team targets
   - For RB: calculate targets per game
   - Classify into EXCELLENT, GOOD, AVERAGE, POOR tiers with position-specific thresholds

2. **Scoring Integration**
   - Apply a tier-based multiplier to the player's score
   - Require minimum targets/games played to produce a valid tier (insufficient data returns neutral)

3. **Team Context (WR/TE)**
   - Requires aggregating team-level target totals; needs access to all players on the same team

### Non-Functional Requirements

- **Performance:** Team target aggregation should be cached within a scoring run
- **Maintainability:** Thresholds and multipliers externalized to config

### Technical Requirements

- **Dependencies:** `FantasyPlayer`, `ConfigManager`, `PlayerManager.get_players_by_team()`
- **Integrations:** `player_scoring.py` scoring pipeline
- **Technology Stack:** Python 3, existing project structure

---

## Research & Background

### Existing Solutions Analysis

**Current State:**
`player_scoring.py` does not have a target volume scoring step. WR/TE/RB evaluations rely on other metrics.

**Research Findings:**
- Target share is available from `receiving.targets` in player data JSON files for WR, TE, RB
- Team-level target totals must be aggregated from all players on the team
- Position-specific thresholds are appropriate (WR EXCELLENT ≥25% share; RB uses targets/game)

**Alternative Approaches Considered:**
1. **Raw targets per game only:** Simpler but doesn't normalize for team volume differences
2. **Target share % for WR/TE, targets/game for RB (Recommended):** Position-appropriate normalization

### Technical Constraints

**Known Limitations:**
- Team target aggregation requires iterating all teammates; should be cached per run
- Minimum targets threshold needed to prevent noisy results for players with few games

**Architectural Considerations:**
- Follow the existing Calculator class pattern (e.g., as implemented by other scoring metrics)
- `get_players_by_team()` may need to be implemented or verified in `PlayerManager`

---

## Initial Feature Breakdown (Preliminary)

**Proposed Features:**

1. **Feature 1:** Target Volume Calculator Module
   - **Purpose:** Calculate target share (WR/TE) or targets per game (RB) and return a (multiplier, tier) tuple
   - **Key Components:** Calculation logic, tier classification, min-games guard

2. **Feature 2:** Scoring Pipeline Integration
   - **Purpose:** Add target volume as a scoring step in `player_scoring.py`
   - **Key Components:** `_apply_target_volume_scoring()` method, team player lookup

3. **Feature 3:** Configuration
   - **Purpose:** Externalize thresholds, multipliers, and weights to `league_config.json`
   - **Key Components:** `TARGET_VOLUME_SCORING` config block

4. **Feature 4:** Unit Tests
   - **Purpose:** Verify calculation correctness across positions and edge cases
   - **Key Components:** High-share WR, low-share WR, RB volume tiers, insufficient data

---

## Dependencies & Risks

### External Dependencies

- **PlayerManager.get_players_by_team():** Required for team target aggregation; may need to be added

### Risks & Mitigation

| Risk | Impact | Probability | Mitigation Strategy |
|------|--------|-------------|---------------------|
| Team target aggregation performance | Medium | Medium | Cache team totals per scoring run |
| PlayerManager missing get_players_by_team | Medium | Low | Check and add if missing |
| Noisy results from small sample sizes | Low | Low | Require minimum targets threshold |

---

## Timeline & Resources

**Estimated Timeline:** 2-3 days

**Team Members Required:**
- Developer: TBD

**Key Milestones:**
1. Calculator module + config: Day 1
2. Scoring integration: Day 2
3. Unit tests passing: Day 3

---

## Implementation Considerations

### Existing Codebase Integration

**Areas of the Codebase That May Require Changes:**
- `league_helper/util/player_scoring.py`: Add `_apply_target_volume_scoring()` step
- `league_helper/util/PlayerManager.py`: Add or verify `get_players_by_team()` method
- `data/league_config.json`: Add `TARGET_VOLUME_SCORING` configuration block

**New Areas That May Need Creation:**
- `league_helper/util/TargetVolumeCalculator.py`: New calculator class

**Coding Practices to Follow:**
- Follow the existing Calculator class pattern (constructor receives config_manager, `calculate()` returns `Tuple[float, str]`)
- Use LoggingManager, not print()
- Google-style docstrings and type hints on all public methods
- Use `error_context()` from `utils/error_handler.py`
- Follow CODING_STANDARDS.md

### Testing Strategy (High-Level)

- **Unit Tests:** High-volume WR gets EXCELLENT tier; low-volume WR gets POOR tier; RB targets/game tiers work correctly; insufficient data returns neutral; bye weeks excluded
- **Integration Tests:** Target volume step fires correctly in full scoring run
- **End-to-End Tests:** Players with high target share rank above equivalent low-share players

---

## Open Questions

1. **Rolling vs. season-long:** Should target share use a season-long average or a rolling window?
   - **Status:** Unanswered

2. **PPR weighting:** Should targets be weighted differently in PPR leagues vs. standard scoring?
   - **Status:** Unanswered

---

## References

- **Related Docs:** `league_helper/util/player_scoring.py`, `data/player_data/wr_data.json`, `data/player_data/te_data.json`, `data/player_data/rb_data.json`
- **Related Epics:** M11 (RB Receiving Workload), M17 (Target Share Trend), M51 (Target Consistency)
- **External Resources:** N/A

---

## Next Steps

**To proceed with this epic:**
1. User reviews this request
2. User says "Start S1 for Target Volume Scoring Integration"
3. Agent reads `.shamt/guides/stages/s1/s1_epic_planning.md`
4. Agent creates git branch and FF-{N} folder during S1
5. Agent runs S1 Discovery Phase to refine this request

**This request file remains in `.shamt/epics/requests/` until S1 creates the epic folder.**
