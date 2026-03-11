# Epic Request: Yards Per Carry Scoring Integration (M08)

**File Location:** `.shamt/epics/requests/metrics/metric-08-yards-per-carry-v2.md`

---

## Epic Overview

**Epic Name:** Yards Per Carry Scoring Integration (M08)

**Date:** 2026-03-09

**Requested By:** User

**Epic Type:** Feature Implementation

**Estimated Complexity:** Small

---

## Problem Statement

**What problem does this epic solve?**

The player scoring algorithm does not account for RB rushing efficiency. An RB averaging 5.5 yards per carry consistently produces more value than one averaging 3.5 YPC, even with the same carry volume, because big plays and longer runs generate more fantasy points per opportunity.

**Why is this important?**

YPC is a key RB efficiency metric. Expected improvement: 5-8% in RB evaluation accuracy, particularly for distinguishing elite runners from below-average ones at similar volume.

**Who is affected?**

Fantasy managers evaluating or comparing RB players.

---

## Goals & Success Metrics

**Primary Goals:**
1. Implement a Yards Per Carry calculator that tiers RBs by rushing efficiency
2. Integrate the calculator into the player scoring pipeline
3. Configure thresholds, multipliers, and minimum attempts requirements

**Success Metrics:**
- Elite rushers (5.0+ YPC) ranked higher than same-volume less efficient RBs
- INSUFFICIENT_DATA when below minimum attempts
- 5-8% improvement in RB evaluation accuracy
- All unit tests passing

**Out of Scope (Explicitly Not Included):**
- Carry volume (covered by M04)
- Receiving efficiency (covered by M09)

---

## Requirements

### Functional Requirements

1. **YPC Calculation**
   - Calculate total rushing yards / total rushing attempts
   - Require minimum attempts (e.g., 50) for valid tier
   - Classify into EXCELLENT (≥5.0), GOOD, AVERAGE, POOR tiers

2. **Scoring Integration**
   - Apply tier-based multiplier
   - Return neutral for INSUFFICIENT_DATA

### Technical Requirements

- **Dependencies:** `FantasyPlayer` (rushing yards + attempts), `ConfigManager`
- **Integrations:** `player_scoring.py`

---

## Research & Background

**Current State:** No YPC scoring step exists.

**Research Findings:**
- `rushing.rush_yds` and `rushing.attempts` available in `rb_data.json`
- EXCELLENT: ≥5.0 YPC; MIN_ATTEMPTS = 50

---

## Initial Feature Breakdown (Preliminary)

**Proposed Features:**

1. **Feature 1:** YPC Calculator Module
2. **Feature 2:** Scoring Pipeline Integration
3. **Feature 3:** Configuration (`YARDS_PER_CARRY_SCORING` block)
4. **Feature 4:** Unit Tests

---

## Dependencies & Risks

### Risks & Mitigation

| Risk | Impact | Probability | Mitigation Strategy |
|------|--------|-------------|---------------------|
| Small sample noise | Medium | Medium | MIN_ATTEMPTS = 50 |

---

## Timeline & Resources

**Estimated Timeline:** 2 days

---

## Implementation Considerations

### Existing Codebase Integration

**Areas of the Codebase That May Require Changes:**
- `league_helper/util/player_scoring.py`: Add YPC scoring step
- `data/league_config.json`: Add `YARDS_PER_CARRY_SCORING` config block

**New Areas That May Need Creation:**
- `league_helper/util/YardsPerCarryCalculator.py`

**Coding Practices to Follow:**
- Position guard: RB only
- Follow existing Calculator class pattern
- Type hints, docstrings, LoggingManager, error_context()

### Testing Strategy (High-Level)

- **Unit Tests:** EXCELLENT for 5.0+; INSUFFICIENT_DATA below minimum; uses season totals not weekly averages

---

## Open Questions

1. **Minimum attempts:** Is 50 the right threshold, or should it be game-based?
   - **Status:** Unanswered

---

## References

- **Related Docs:** `player_scoring.py`, `data/player_data/rb_data.json`
- **Related Epics:** M04 (Carries Per Game), M11 (RB Receiving Workload), M19 (Touch Share)

---

## Next Steps

**To proceed with this epic:**
1. User reviews this request
2. User says "Start S1 for Yards Per Carry Scoring Integration"
3. Agent reads `.shamt/guides/stages/s1/s1_epic_planning.md`
4. Agent creates git branch and FF-{N} folder during S1
5. Agent runs S1 Discovery Phase to refine this request

**This request file remains in `.shamt/epics/requests/` until S1 creates the epic folder.**
