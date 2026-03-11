# Epic Request: TD:INT Ratio Scoring Integration (M07)

**File Location:** `.shamt/epics/requests/metrics/metric-07-td-int-ratio-v2.md`

---

## Epic Overview

**Epic Name:** TD:INT Ratio Scoring Integration (M07)

**Date:** 2026-03-09

**Requested By:** User

**Epic Type:** Feature Implementation

**Estimated Complexity:** Small

---

## Problem Statement

**What problem does this epic solve?**

The player scoring algorithm does not account for QB TD:INT ratio. A QB with a high TD:INT ratio consistently generates positive fantasy scoring events (TDs worth 4-6 pts) while minimizing negative ones (INTs worth -2 pts). Without this metric, turnover-prone QBs are not sufficiently penalized in rankings.

**Why is this important?**

TD:INT ratio captures QB decision-making quality and directly impacts fantasy point totals. Expected improvement: 6-10% in QB evaluation accuracy.

**Who is affected?**

Fantasy managers evaluating or comparing QB players.

---

## Goals & Success Metrics

**Primary Goals:**
1. Implement a TD:INT Ratio calculator that handles zero-interception edge cases
2. Integrate the calculator into the player scoring pipeline
3. Configure thresholds, multipliers, and minimum TD requirements

**Success Metrics:**
- High ratio QBs (4.0+) ranked above equivalent-volume lower-ratio QBs
- Zero-INT QBs handled correctly (ratio = total TDs, not division by zero)
- INSUFFICIENT_DATA when below minimum TDs
- All unit tests passing

**Out of Scope (Explicitly Not Included):**
- Completion percentage (M06)
- Fumble tracking

---

## Requirements

### Functional Requirements

1. **TD:INT Ratio Calculation**
   - Calculate total passing TDs / total INTs
   - Handle zero INTs: ratio = total TDs (capped at a reasonable max, or use total TDs as ratio)
   - Require minimum TDs (e.g., 10) for valid tier
   - Classify into EXCELLENT (≥4.0), GOOD, AVERAGE, POOR tiers

2. **Scoring Integration**
   - Apply tier-based multiplier to QB score
   - Return neutral for INSUFFICIENT_DATA

### Non-Functional Requirements

- **Correctness:** Zero-INT case must not cause division by zero; must be handled explicitly

### Technical Requirements

- **Dependencies:** `FantasyPlayer` (passing TDs and INTs), `ConfigManager`
- **Integrations:** `player_scoring.py`

---

## Research & Background

**Current State:** No TD:INT scoring step exists.

**Research Findings:**
- `passing.pass_tds` and `passing.interceptions` available in `qb_data.json`
- EXCELLENT: ≥4.0 ratio; zero INTs handled as ratio = total TDs (provides bonus)
- MIN_TDS = 10 for valid tier

---

## Initial Feature Breakdown (Preliminary)

**Proposed Features:**

1. **Feature 1:** TD:INT Ratio Calculator Module (with zero-INT handling)
2. **Feature 2:** Scoring Pipeline Integration
3. **Feature 3:** Configuration (`TD_INT_RATIO_SCORING` block)
4. **Feature 4:** Unit Tests (including zero-INT edge case)

---

## Dependencies & Risks

### Risks & Mitigation

| Risk | Impact | Probability | Mitigation Strategy |
|------|--------|-------------|---------------------|
| Division by zero (0 INTs) | High | Medium | Explicit zero-INT branch in calculation |
| Small TD count for backups | Medium | Medium | MIN_TDS threshold |

---

## Timeline & Resources

**Estimated Timeline:** 2 days

---

## Implementation Considerations

### Existing Codebase Integration

**Areas of the Codebase That May Require Changes:**
- `league_helper/util/player_scoring.py`: Add TD:INT scoring step
- `data/league_config.json`: Add `TD_INT_RATIO_SCORING` config block

**New Areas That May Need Creation:**
- `league_helper/util/TDINTRatioCalculator.py`

**Coding Practices to Follow:**
- Position guard: QB only
- Zero-INT edge case must be explicitly documented and tested
- Type hints, docstrings, LoggingManager, error_context()

### Testing Strategy (High-Level)

- **Unit Tests:** 4.0+ ratio → EXCELLENT; 0 INTs handled correctly; MIN_TDS guard; season totals calculated correctly

---

## Open Questions

1. **Zero-INT handling:** Should zero INTs result in ratio = total TDs, or a fixed maximum ratio value?
   - **Status:** Unanswered

---

## References

- **Related Docs:** `player_scoring.py`, `data/player_data/qb_data.json`
- **Related Epics:** M03 (Pass Attempts), M06 (Completion%), M12 (QB Quality)

---

## Next Steps

**To proceed with this epic:**
1. User reviews this request
2. User says "Start S1 for TD:INT Ratio Scoring Integration"
3. Agent reads `.shamt/guides/stages/s1/s1_epic_planning.md`
4. Agent creates git branch and FF-{N} folder during S1
5. Agent runs S1 Discovery Phase to refine this request

**This request file remains in `.shamt/epics/requests/` until S1 creates the epic folder.**
