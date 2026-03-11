# Epic Request: Kicker Accuracy Scoring Integration (M05)

**File Location:** `.shamt/epics/requests/metrics/metric-05-kicker-accuracy-v2.md`

---

## Epic Overview

**Epic Name:** Kicker Accuracy Scoring Integration (M05)

**Date:** 2026-03-09

**Requested By:** User

**Epic Type:** Feature Implementation

**Estimated Complexity:** Small

---

## Problem Statement

**What problem does this epic solve?**

The player scoring algorithm does not account for kicker accuracy (field goal percentage). A kicker who converts 95% of attempts is significantly more valuable than one who converts 75%, even if they have the same number of opportunities. Without this metric, kickers are not differentiated by a key performance dimension.

**Why is this important?**

FG% is the primary efficiency metric for kickers. Expected improvement: 8-12% in kicker evaluation accuracy, with the largest impact in streaming and Add To Roster modes.

**Who is affected?**

Fantasy managers evaluating or selecting kickers.

---

## Goals & Success Metrics

**Primary Goals:**
1. Implement a Kicker Accuracy calculator that computes FG% and classifies into tiers
2. Integrate the calculator into the player scoring pipeline
3. Configure thresholds, multipliers, and minimum attempt requirements in the league config

**Success Metrics:**
- Elite kickers (≥90% FG%) ranked higher than equivalent-volume but less accurate kickers
- 8-12% improvement in kicker evaluation accuracy
- INSUFFICIENT_DATA tier returned when attempts are below minimum threshold
- All unit tests passing

**Out of Scope (Explicitly Not Included):**
- Kicker volume (covered by M46 FG Attempts Per Game)
- Extra point accuracy as primary metric

---

## Requirements

### Functional Requirements

1. **FG% Calculation**
   - Calculate field goal percentage: FG made / FG attempted
   - Require a minimum number of attempts (e.g., 10) before producing a valid tier
   - Return INSUFFICIENT_DATA tier when below minimum

2. **Scoring Integration**
   - Apply tier-based multiplier to kicker score
   - INSUFFICIENT_DATA returns neutral multiplier (1.0)

### Non-Functional Requirements

- **Reliability:** Minimum attempts guard prevents misleading results from small samples

### Technical Requirements

- **Dependencies:** `FantasyPlayer` (field_goals data), `ConfigManager`
- **Integrations:** `player_scoring.py` scoring pipeline

---

## Research & Background

### Existing Solutions Analysis

**Current State:**
No kicker accuracy scoring step in `player_scoring.py`.

**Research Findings:**
- `field_goals.made` and `field_goals.missed` available in `k_data.json`
- EXCELLENT: ≥90% FG%; minimum MIN_ATTEMPTS = 10 for valid tier

**Alternative Approaches Considered:**
1. **No minimum threshold:** Kickers with 1/1 FG would get EXCELLENT tier unfairly
2. **MIN_ATTEMPTS guard (Recommended):** Prevents gaming and early-season noise

### Technical Constraints

**Known Limitations:**
- Distance-adjusted accuracy (long FGs harder) is more complex; season-level FG% is sufficient for this metric

---

## Initial Feature Breakdown (Preliminary)

**Proposed Features:**

1. **Feature 1:** Kicker Accuracy Calculator Module
   - **Purpose:** Calculate FG% and return (multiplier, tier) with INSUFFICIENT_DATA guard
   - **Key Components:** FG% calculation, MIN_ATTEMPTS check, tier classification

2. **Feature 2:** Scoring Pipeline Integration
   - **Purpose:** Add as K-specific scoring step
   - **Key Components:** `_apply_kicker_accuracy_scoring()` method

3. **Feature 3:** Configuration
   - **Purpose:** Externalize thresholds, multipliers, and MIN_ATTEMPTS
   - **Key Components:** `KICKER_ACCURACY_SCORING` config block

4. **Feature 4:** Unit Tests
   - **Purpose:** Verify accuracy tiers, INSUFFICIENT_DATA guard, bye week handling
   - **Key Components:** Elite kicker, poor accuracy, insufficient attempts

---

## Dependencies & Risks

### External Dependencies

None beyond existing codebase.

### Risks & Mitigation

| Risk | Impact | Probability | Mitigation Strategy |
|------|--------|-------------|---------------------|
| Small sample noise | Medium | Medium | MIN_ATTEMPTS threshold |
| Bye week detection | Low | Low | Check total FG + XP attempts for game activity |

---

## Timeline & Resources

**Estimated Timeline:** 2 days

**Team Members Required:**
- Developer: TBD

---

## Implementation Considerations

### Existing Codebase Integration

**Areas of the Codebase That May Require Changes:**
- `league_helper/util/player_scoring.py`: Add kicker accuracy scoring step
- `data/league_config.json`: Add `KICKER_ACCURACY_SCORING` config block

**New Areas That May Need Creation:**
- `league_helper/util/KickerAccuracyCalculator.py`

**Coding Practices to Follow:**
- Position guard: K only
- Follow existing Calculator class pattern
- Type hints, docstrings, LoggingManager, error_context()

### Testing Strategy (High-Level)

- **Unit Tests:** ≥90% FG% → EXCELLENT; <75% → POOR; <MIN_ATTEMPTS → INSUFFICIENT_DATA
- **Integration Tests:** Kicker accuracy step fires only for K

---

## Open Questions

1. **Minimum attempts:** What is the appropriate MIN_ATTEMPTS threshold — 10, 15, or more?
   - **Status:** Unanswered

---

## References

- **Related Docs:** `player_scoring.py`, `data/player_data/k_data.json`
- **Related Epics:** M46 (FG Attempts Per Game)
- **External Resources:** N/A

---

## Next Steps

**To proceed with this epic:**
1. User reviews this request
2. User says "Start S1 for Kicker Accuracy Scoring Integration"
3. Agent reads `.shamt/guides/stages/s1/s1_epic_planning.md`
4. Agent creates git branch and FF-{N} folder during S1
5. Agent runs S1 Discovery Phase to refine this request

**This request file remains in `.shamt/epics/requests/` until S1 creates the epic folder.**
