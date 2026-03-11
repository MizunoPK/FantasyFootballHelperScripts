# Epic Request: Yards Per Reception Scoring Integration (M09)

**File Location:** `.shamt/epics/requests/metrics/metric-09-yards-per-reception-v2.md`

---

## Epic Overview

**Epic Name:** Yards Per Reception Scoring Integration (M09)

**Date:** 2026-03-09

**Requested By:** User

**Epic Type:** Feature Implementation

**Estimated Complexity:** Small

---

## Problem Statement

**What problem does this epic solve?**

The player scoring algorithm does not account for receiving efficiency (yards per reception). A WR averaging 16 yards per reception generates more value per catch than one averaging 9 YPR, particularly in non-PPR formats where yards matter more than catch counts. Without position-specific thresholds, WRs and TEs are evaluated on the same scale despite having different typical ranges.

**Why is this important?**

YPR is a key receiving efficiency metric. Position-specific thresholds (WR vs. TE) appropriately account for the different roles each position plays. Expected improvement: 5-8% in WR/TE evaluation accuracy.

**Who is affected?**

Fantasy managers evaluating or comparing WR and TE players.

---

## Goals & Success Metrics

**Primary Goals:**
1. Implement a Yards Per Reception calculator with position-specific thresholds (WR and TE)
2. Integrate the calculator into the player scoring pipeline
3. Configure thresholds, multipliers, and minimum reception requirements

**Success Metrics:**
- Deep-threat WRs with high YPR ranked appropriately vs. short-route specialists
- Position-specific thresholds: WR EXCELLENT ≥15.0, TE EXCELLENT ≥12.0
- INSUFFICIENT_DATA when below minimum receptions
- All unit tests passing

**Out of Scope (Explicitly Not Included):**
- Catch rate efficiency (covered by M10)
- Target volume (covered by M01)

---

## Requirements

### Functional Requirements

1. **YPR Calculation**
   - Calculate total receiving yards / total receptions
   - Require minimum receptions (e.g., 30) for valid tier
   - Position-specific tier thresholds: different EXCELLENT/GOOD/AVERAGE/POOR values for WR vs. TE

2. **Scoring Integration**
   - Apply tier-based multiplier
   - Return neutral for INSUFFICIENT_DATA

### Technical Requirements

- **Dependencies:** `FantasyPlayer` (receiving yards + receptions), `ConfigManager`
- **Integrations:** `player_scoring.py`

---

## Research & Background

**Current State:** No YPR scoring step exists.

**Research Findings:**
- `receiving.rec_yds` and `receiving.receptions` available in `wr_data.json` and `te_data.json`
- WR EXCELLENT: ≥15.0 YPR; TE EXCELLENT: ≥12.0 YPR
- MIN_RECEPTIONS = 30 for valid tier

---

## Initial Feature Breakdown (Preliminary)

**Proposed Features:**

1. **Feature 1:** YPR Calculator Module (with position-specific thresholds)
2. **Feature 2:** Scoring Pipeline Integration
3. **Feature 3:** Configuration (`YARDS_PER_RECEPTION_SCORING` with WR and TE blocks)
4. **Feature 4:** Unit Tests (WR and TE paths separately)

---

## Dependencies & Risks

### Risks & Mitigation

| Risk | Impact | Probability | Mitigation Strategy |
|------|--------|-------------|---------------------|
| Position-specific threshold logic | Low | Low | Position-keyed threshold lookup |
| Small sample noise | Medium | Medium | MIN_RECEPTIONS = 30 |

---

## Timeline & Resources

**Estimated Timeline:** 2 days

---

## Implementation Considerations

### Existing Codebase Integration

**Areas of the Codebase That May Require Changes:**
- `league_helper/util/player_scoring.py`: Add YPR scoring step
- `data/league_config.json`: Add `YARDS_PER_RECEPTION_SCORING` with position-specific sub-config

**New Areas That May Need Creation:**
- `league_helper/util/YardsPerReceptionCalculator.py`

**Coding Practices to Follow:**
- Position guard: WR and TE only
- Position-specific threshold lookup (not hardcoded per-branch)
- Type hints, docstrings, LoggingManager, error_context()

### Testing Strategy (High-Level)

- **Unit Tests:** WR and TE EXCELLENT tiers tested separately; INSUFFICIENT_DATA guard; season totals used

---

## Open Questions

1. **Minimum receptions:** Is 30 the right minimum, or should it scale with games played?
   - **Status:** Unanswered

---

## References

- **Related Docs:** `player_scoring.py`, `data/player_data/wr_data.json`, `data/player_data/te_data.json`
- **Related Epics:** M01 (Target Volume), M10 (Catch Rate), M51 (Target Consistency)

---

## Next Steps

**To proceed with this epic:**
1. User reviews this request
2. User says "Start S1 for Yards Per Reception Scoring Integration"
3. Agent reads `.shamt/guides/stages/s1/s1_epic_planning.md`
4. Agent creates git branch and FF-{N} folder during S1
5. Agent runs S1 Discovery Phase to refine this request

**This request file remains in `.shamt/epics/requests/` until S1 creates the epic folder.**
