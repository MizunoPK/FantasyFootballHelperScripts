# Epic Request: Completion Percentage Scoring Integration (M06)

**File Location:** `.shamt/epics/requests/metrics/metric-06-completion-percentage-v2.md`

---

## Epic Overview

**Epic Name:** Completion Percentage Scoring Integration (M06)

**Date:** 2026-03-09

**Requested By:** User

**Epic Type:** Feature Implementation

**Estimated Complexity:** Small

---

## Problem Statement

**What problem does this epic solve?**

The player scoring algorithm does not account for QB completion percentage. A QB who completes 70%+ of passes consistently produces more fantasy points from the same number of attempts than a 58% completion QB, because more completions mean more completion bonuses, yards, and downstream TD opportunities.

**Why is this important?**

Completion percentage is a core QB efficiency metric that predicts consistent production. Expected improvement: 5-8% in QB evaluation accuracy.

**Who is affected?**

Fantasy managers evaluating or comparing QB players.

---

## Goals & Success Metrics

**Primary Goals:**
1. Implement a Completion Percentage calculator that tiers QBs by efficiency
2. Integrate the calculator into the player scoring pipeline
3. Configure thresholds, multipliers, and minimum attempt requirements

**Success Metrics:**
- Elite completion% QBs (70%+) ranked higher than equivalent-volume lower-accuracy QBs
- 5-8% improvement in QB evaluation accuracy
- INSUFFICIENT_DATA when below minimum attempts threshold
- All unit tests passing

**Out of Scope (Explicitly Not Included):**
- Passing volume (covered by M03)
- TD:INT ratio (covered by M07)

---

## Requirements

### Functional Requirements

1. **Completion% Calculation**
   - Calculate completions / attempts across season
   - Require minimum attempts (e.g., 100) for valid tier
   - Classify into EXCELLENT (≥70%), GOOD, AVERAGE, POOR tiers

2. **Scoring Integration**
   - Apply tier-based multiplier to QB score
   - Return neutral (1.0) for INSUFFICIENT_DATA

### Non-Functional Requirements

- **Reliability:** Minimum attempts guard prevents noise from backup QBs

### Technical Requirements

- **Dependencies:** `FantasyPlayer` (passing completions/attempts), `ConfigManager`
- **Integrations:** `player_scoring.py` scoring pipeline

---

## Research & Background

**Current State:** No completion% scoring step exists.

**Research Findings:**
- `passing.completions` and `passing.pass_attempts` available in `qb_data.json`
- EXCELLENT: ≥70%; MIN_ATTEMPTS: 100 season attempts

---

## Initial Feature Breakdown (Preliminary)

**Proposed Features:**

1. **Feature 1:** Completion% Calculator Module
2. **Feature 2:** Scoring Pipeline Integration
3. **Feature 3:** Configuration (`COMPLETION_PERCENTAGE_SCORING` block)
4. **Feature 4:** Unit Tests

---

## Dependencies & Risks

### Risks & Mitigation

| Risk | Impact | Probability | Mitigation Strategy |
|------|--------|-------------|---------------------|
| Backup QB noise | Medium | Medium | MIN_ATTEMPTS = 100 threshold |

---

## Timeline & Resources

**Estimated Timeline:** 2 days

---

## Implementation Considerations

### Existing Codebase Integration

**Areas of the Codebase That May Require Changes:**
- `league_helper/util/player_scoring.py`: Add completion% scoring step
- `data/league_config.json`: Add `COMPLETION_PERCENTAGE_SCORING` config block

**New Areas That May Need Creation:**
- `league_helper/util/CompletionPercentageCalculator.py`

**Coding Practices to Follow:**
- Position guard: QB only
- Follow existing Calculator class pattern
- Type hints, docstrings, LoggingManager, error_context()

### Testing Strategy (High-Level)

- **Unit Tests:** EXCELLENT for ≥70%; INSUFFICIENT_DATA below minimum; bye week handling
- **Integration Tests:** Fires only for QBs

---

## Open Questions

1. **Minimum attempts:** Is 100 the right minimum, or should it be game-based (e.g., 8+ games)?
   - **Status:** Unanswered

---

## References

- **Related Docs:** `player_scoring.py`, `data/player_data/qb_data.json`
- **Related Epics:** M03 (Pass Attempts), M07 (TD:INT Ratio), M12 (QB Quality)

---

## Next Steps

**To proceed with this epic:**
1. User reviews this request
2. User says "Start S1 for Completion Percentage Scoring Integration"
3. Agent reads `.shamt/guides/stages/s1/s1_epic_planning.md`
4. Agent creates git branch and FF-{N} folder during S1
5. Agent runs S1 Discovery Phase to refine this request

**This request file remains in `.shamt/epics/requests/` until S1 creates the epic folder.**
