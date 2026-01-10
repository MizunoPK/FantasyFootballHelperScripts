# Process Failure Analysis - KAI-5 Add K/DST Ranking Metrics Support

**Purpose:** Systematic analysis of why bugs got through our process and how to prevent them

**Date:** 2026-01-09

---

## Issue #1: Incomplete Simulation Results - Missing Ranking Metrics and Metadata

### Bug Summary
- **What was the bug:** Resume logic loaded old intermediate files (created before epic) without ranking_metrics, polluting best_configs with invalid data. Comparison logic fell back to MAE when one config had metrics and another didn't, causing new configs with ranking_metrics to be rejected in favor of old configs without metrics.
- **Root Cause:**
  1. load_intermediate_results() populated best_configs with old metrics from files created before ranking_metrics were implemented
  2. is_better_than() had MAE fallback that allowed mixed comparisons (configs with metrics vs without metrics)
  3. Invalid 'ros' key in horizon_map caused spurious warning
- **Severity:** HIGH (Breaks core epic functionality - K/DST metrics not saved to output)
- **Discovery Stage:** Stage 6c - User Testing

### Why Did This Bug Get Through?

**Research Phase Analysis (Stage 5a - TODO Creation):**
- ✅ Was this scenario considered during Iterations 1-7 (Round 1)?
  - **NO** - Resume behavior with old files was NOT considered
  - **Why not:** The research focused on adding K/DST support to NEW calculations, not how the system would interact with EXISTING intermediate files from before the epic
  - **Gap:** Backward compatibility with old intermediate files was not part of the research scope

**Implementation Phase Analysis (Stage 5b):**
- ✅ Did implementation match spec?
  - **YES** - Implementation correctly added ranking_metrics to NEW calculations
  - **Problem:** Spec didn't address resume behavior with old files

- ✅ Were edge cases tested during implementation?
  - **NO** - Resume scenario with old files was not tested
  - **Why not:** Test focused on new functionality (ranking metrics calculation), not backward compatibility

**Smoke Testing Phase Analysis (Stage 5ca):**
- ✅ Did smoke tests cover this scenario?
  - **NO** - Smoke tests used fresh runs without intermediate files
  - **Why missed:** Smoke tests didn't simulate resuming from old intermediate folders

**QC Rounds Phase Analysis (Stage 5cb):**
- ✅ Did QC rounds catch this?
  - **NO** - QC rounds focused on code inspection, not resume scenarios
  - **Why missed:** QC checklists don't explicitly require testing resume behavior

**Epic Testing Phase Analysis (Stage 6):**
- ✅ Did epic smoke test catch this?
  - **NO** - Epic smoke tests ran fresh simulations
  - **Why missed:** Epic smoke test plan didn't include resume scenario testing

**User Testing Phase Analysis (Stage 7):**
- ✅ How was it discovered?
  - **User ran simulation** that found old intermediate folders and tried to resume
  - **Symptom:** Output files missing ranking_metrics despite epic implementation
  - **This is CORRECT discovery point** - User testing is designed to catch real-world usage scenarios

### Process Gaps Identified

**Gap 1: Backward Compatibility Not Part of Research**
- **Stage:** Stage 5a (TODO Creation)
- **Issue:** Research didn't consider how new code interacts with data created by old code
- **Impact:** Resume behavior with old files completely missed

**Gap 2: Test Scenarios Don't Cover Resume Behavior**
- **Stage:** Stage 5ca (Smoke Testing), Stage 6 (Epic Testing)
- **Issue:** Tests always start fresh, never test resume scenarios
- **Impact:** Resume bugs not discovered until user testing

**Gap 3: MAE Fallback Allowed Invalid Comparisons**
- **Stage:** Stage 5a (Spec Design)
- **Issue:** Spec allowed MAE fallback "for backward compatibility" without considering implications
- **Impact:** New configs with metrics could be rejected in favor of old configs without metrics

### Root Cause Category

**Category:** Backward Compatibility Oversight
- This bug occurred at the intersection of new functionality and old data
- Resume behavior was not explicitly considered during research
- Test scenarios didn't cover this real-world usage pattern

### Could This Bug Have Been Prevented?

**YES - Multiple prevention points:**

1. **During Stage 5a Round 1 (Codebase Research):**
   - Add explicit iteration: "How does this interact with existing data?"
   - Research question: "What happens if simulation resumes from old intermediate folders?"

2. **During Stage 5a Round 2 (Test Coverage Analysis):**
   - Add test scenario: "Resume from intermediate folder created before this epic"
   - Require backward compatibility tests when touching data persistence

3. **During Stage 5ca (Smoke Testing):**
   - Add smoke test scenario: "Resume from old intermediate folder"
   - Explicitly test backward compatibility

4. **During Spec Review (Iteration 23a):**
   - Question "backward compatibility" design decisions
   - Challenge: "If we have MAE fallback, what happens when old and new configs are compared?"

### Specific Process Improvements Needed

**See guide_update_recommendations.md for concrete guide updates**

---

## Cross-Bug Pattern Analysis

**Total Bugs:** 1
**Pattern Identified:** Backward compatibility gaps

**Common Theme:**
- New features don't always consider interaction with old data
- Resume/persistence scenarios undertested
- "Backward compatibility" design decisions need more scrutiny

**Process Strength:**
- User testing caught the issue before epic completion
- Investigation protocol worked well (1 round to root cause)
- Fix was straightforward once root cause identified

**Process Weakness:**
- Research phase doesn't explicitly prompt for backward compatibility analysis
- Test scenarios focused on "happy path" with fresh data
- Spec review didn't catch problematic design decision (MAE fallback)

---

## Summary

**Why This Bug Got Through:**
1. Backward compatibility with old files not part of research scope
2. Test scenarios didn't cover resume behavior
3. MAE fallback design decision not questioned during spec review

**How to Prevent:**
1. Add backward compatibility research iteration to Stage 5a Round 1
2. Add resume scenario testing to smoke test requirements
3. Add "challenge design decisions" checkpoint to spec review

**Effort to Fix:** 30 minutes investigation + 1 hour implementation + tests
**Effort to Prevent:** Would have added ~15 minutes to research, ~10 minutes to smoke testing

**Recommendation:** Prevention is more efficient than debugging. Update guides to include backward compatibility checkpoints.
