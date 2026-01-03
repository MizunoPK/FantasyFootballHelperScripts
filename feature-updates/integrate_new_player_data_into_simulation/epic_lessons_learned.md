# Epic: integrate_new_player_data_into_simulation - Lessons Learned

**Purpose:** Document cross-feature patterns and systemic insights from this epic

---

## Planning Phase Lessons (Stages 1-4)

### Stage 1: Epic Planning

**Lessons from Phase 2 Analysis:**
- JSON migration happened very recently (2025-12-30), only 3 days old at epic start
- Partial implementation already exists but user flagged as "buggy and incomplete"
- Need to verify all existing work rather than assume it's correct
- SimulatedLeague already has _parse_players_json(), AccuracySimulationManager already copies JSON files
- Week 17 fix already implemented in code (week_num_for_actual parameter)

**Key Decision:** Framed as verification/cleanup epic rather than greenfield implementation

{More lessons will be added as Stages 2-4 progress}

---

## Implementation Phase Lessons (Stage 5)

{Will be populated during Stage 5 as features are implemented}

---

## QC Phase Lessons (Stage 6)

{Will be populated during Stage 6 epic final QC}

---

## Guide Improvements Identified

{Track guide gaps/improvements discovered during this epic}

| Guide File | Issue | Proposed Fix | Status |
|------------|-------|--------------|--------|
| (none yet) | (will track as issues discovered) | (proposed solutions) | Pending/Done |

---

## Cross-Feature Patterns

{Will be populated as patterns emerge across features}

**Common patterns identified:**
- TBD

**Anti-patterns to avoid:**
- TBD

---

## Epic-Specific Insights

**What made this epic unique:**
- Verification/cleanup of partial work instead of new implementation
- Two different simulation architectures (Win Rate: direct parsing, Accuracy: via PlayerManager)
- Recent transition period (CSV just deprecated 3 days before epic start)

**What we'd do differently:**
- TBD (will populate during/after epic)
