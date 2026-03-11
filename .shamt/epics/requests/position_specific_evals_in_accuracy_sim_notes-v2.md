# Epic Request: Position-Specific Accuracy Sim Evaluations

**File Location:** `.shamt/epics/requests/position_specific_evals_in_accuracy_sim_notes-v2.md`

---

## Epic Overview

**Epic Name:** Position-Specific Accuracy Sim Evaluations

**Date:** 2026-03-09

**Requested By:** User

**Epic Type:** Enhancement

**Estimated Complexity:** Small

---

## Problem Statement

**What problem does this epic solve?**

The Accuracy Simulation currently evaluates all positions together for every parameter variation. When testing a parameter like `WIND`, the simulation ranks and compares players across all positions (QB, RB, WR, TE, K, DST) — even though wind primarily affects only a subset of positions (e.g., QB, WR, K). This dilutes the accuracy signal and makes it harder to assess how well each parameter is tuned for the positions it actually influences.

**Why is this important?**

Including irrelevant positions in a parameter's accuracy evaluation introduces noise. A parameter like `WIND` that is tuned specifically for passers and kickers should only be evaluated against those positions. Filtering by relevant positions produces cleaner accuracy signals and enables more meaningful comparison across parameter configurations.

**Who is affected?**

Users analyzing and tuning Accuracy Simulation results to improve the scoring algorithm's parameter settings.

---

## Goals & Success Metrics

**Primary Goals:**
1. Allow each Accuracy Sim parameter to specify which positions are included in its pairwise accuracy evaluations
2. Ensure players from excluded positions are not pulled in for ranking or comparison under a given parameter
3. Keep the configuration flexible and easy to extend as new parameters or positions are added

**Success Metrics:**
- Each parameter in the Accuracy Sim can independently specify its relevant positions
- Pairwise evaluations for a given parameter only include players from the configured positions
- Existing behavior is preserved for parameters that include all positions
- No regressions in Accuracy Sim functionality

**Out of Scope (Explicitly Not Included):**
- Changes to the scoring algorithm itself
- Changes to how parameters are varied or ranked
- Multi-season or cross-week evaluation changes

---

## Requirements

### Functional Requirements

1. **Position Mapping Configuration**
   - Add a `PARAMETER_POSITION_MAPPING` config structure to the Accuracy Sim
   - Each parameter key maps to a list of positions whose players are included in evaluations
   - Parameters not present in the mapping default to all positions

2. **Player Filtering in Evaluation Loop**
   - When evaluating a given parameter, only load/rank players belonging to the configured positions
   - Apply filtering before pairwise accuracy computation

### Non-Functional Requirements

- **Maintainability:** The position mapping should live in configuration, not hardcoded in evaluation logic
- **Backwards Compatibility:** Parameters not specified in the mapping continue to evaluate all positions

### Technical Requirements

- **Dependencies:** Accuracy Simulation config system
- **Integrations:** Existing pairwise accuracy evaluation loop
- **Technology Stack:** Python, existing config loading pattern

---

## Research & Background

### Existing Solutions Analysis

**Current State:**
The Accuracy Simulation evaluates all positions together for each parameter variation. There is no per-parameter position filtering.

**Research Findings:**
- Parameters like `WIND` and `TEMPERATURE` primarily affect passing/kicking positions (QB, WR, K)
- Parameters like `TEAM_QUALITY` and `PERFORMANCE` are relevant to most or all positions
- Mixing all positions for a position-specific parameter dilutes accuracy metrics

**Alternative Approaches Considered:**
1. **Global position filter:** Single config for all parameters — does not allow per-parameter control
2. **Per-parameter position mapping (Recommended):** Flexible, explicit, and easy to extend

### Technical Constraints

**Known Limitations:**
- The mapping must handle the case where a parameter is not listed (default to all positions)
- Position lists must match the position codes used in player data

**Architectural Considerations:**
- Config should follow the existing pattern in `run_simulation.py` / Accuracy Sim config files
- Filtering should occur early in the evaluation loop to avoid unnecessary data loading

---

## Initial Feature Breakdown (Preliminary)

**Note:** This is a preliminary breakdown. S1 Discovery Phase will refine this.

**Proposed Features:**

1. **Feature 1:** Position Mapping Configuration
   - **Purpose:** Add `PARAMETER_POSITION_MAPPING` to the Accuracy Sim configuration
   - **Key Components:** Config schema update, default-all-positions fallback

2. **Feature 2:** Evaluation Loop Filtering
   - **Purpose:** Filter players by configured positions before pairwise accuracy evaluation
   - **Key Components:** Player list filtering logic in the accuracy evaluation loop

---

## Dependencies & Risks

### External Dependencies

- **Accuracy Simulation codebase:** Changes needed in `run_simulation.py` and/or related accuracy sim modules

### Risks & Mitigation

| Risk | Impact | Probability | Mitigation Strategy |
|------|--------|-------------|---------------------|
| Position codes mismatch between config and player data | Medium | Low | Validate position codes against known values at config load time |
| Missing parameter in mapping breaks evaluation | Medium | Low | Default to all positions if parameter not in mapping |

---

## Timeline & Resources

**Estimated Timeline:** 1-2 days

**Team Members Required:**
- Developer: TBD

**Key Milestones:**
1. Config structure designed and reviewed: Day 1
2. Filtering logic implemented and tested: Day 2

---

## Implementation Considerations

### Existing Codebase Integration

**Areas of the Codebase That May Require Changes:**
- `run_simulation.py` or the Accuracy Sim config loader: Add `PARAMETER_POSITION_MAPPING` support
- Accuracy evaluation loop module: Apply per-parameter position filtering

**New Areas That May Need Creation:**
- No new modules expected; changes are contained to existing accuracy sim files

**Coding Practices to Follow:**
- Follow existing config loading patterns in the simulation codebase
- Use LoggingManager for any diagnostic output
- Follow type hint and docstring standards from CODING_STANDARDS.md

### Testing Strategy (High-Level)

- **Unit Tests:** Verify that player lists are correctly filtered per position mapping; verify all-positions default behavior
- **Integration Tests:** Run Accuracy Sim with a position-mapped config and verify correct players appear in evaluations
- **End-to-End Tests:** Full accuracy sim run with position mapping enabled produces valid results

---

## Open Questions

1. **Default behavior for unmapped parameters:** Should unmapped parameters evaluate all positions, or raise a warning?
   - **Status:** Unanswered

2. **Config location:** Should `PARAMETER_POSITION_MAPPING` live in the main accuracy sim config file or a separate positions config?
   - **Status:** Unanswered

---

## References

- **Related Docs:** Accuracy Simulation documentation; `run_simulation.py`
- **Related Epics:** None
- **External Resources:** N/A

---

## Next Steps

**To proceed with this epic:**
1. User reviews this request
2. User says "Start S1 for Position-Specific Accuracy Sim Evaluations"
3. Agent reads `.shamt/guides/stages/s1/s1_epic_planning.md`
4. Agent creates git branch and FF-{N} folder during S1
5. Agent runs S1 Discovery Phase to refine this request

**This request file remains in `.shamt/epics/requests/` until S1 creates the epic folder.**
