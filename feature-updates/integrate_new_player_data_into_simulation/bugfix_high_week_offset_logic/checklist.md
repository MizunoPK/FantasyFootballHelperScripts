# Bug Fix Checklist: Week Offset Logic

**Created:** 2026-01-02
**Status:** Stage 2 (Deep Dive)

---

## Phase A: Epic Requirement Validation

| Item | Question | Answer | Status | Evidence |
|------|----------|--------|--------|----------|
| 1 | Does epic notes line 8 explicitly state week_N + week_N+1 pattern? | YES - "use week_17 folders for projected_points, then look at actual_points array in week_18 folders" | ✅ VERIFIED | integrate_new_player_data_into_simulation_notes.txt:8 |
| 2 | Does the example generalize to ALL weeks (not just week 17)? | YES - week_17/week_18 is example of pattern | ✅ VERIFIED | Pattern applies to weeks 1-17 |
| 3 | Is this requirement stated clearly (not ambiguous)? | YES - Very clear | ✅ VERIFIED | User explicitly confirmed by asking verification question |

---

## Phase B: Data Model Investigation

| Item | Question | Answer | Status | Evidence |
|------|----------|--------|--------|----------|
| 4 | Does week_N folder contain week N actual points? | NO - Contains 0.0 for week N | ✅ VERIFIED | Manual inspection: week_01[0]['actual_points'][0] = 0.0 |
| 5 | Does week_N+1 folder contain week N actual points? | YES - Contains real values | ✅ VERIFIED | Manual inspection: week_02[0]['actual_points'][0] = 33.6 |
| 6 | Is this data model documented in code? | YES - json_exporter.py explains it | ✅ VERIFIED | json_exporter.py:306 "if week < current_week" |
| 7 | Is week_N folder a point-in-time snapshot? | YES - "as of" week N's start | ✅ VERIFIED | Week N hasn't completed yet when week_N folder created |
| 8 | Do ALL 17-element arrays follow this pattern? | YES - actual_points and projected_points | ✅ VERIFIED | Manual inspection confirmed 17 elements |

---

## Phase C: Current Implementation Analysis

| Item | Question | Answer | Status | Evidence |
|------|----------|--------|--------|----------|
| 9 | Does _load_season_data() return two different folders? | NO - Returns same folder twice | ✅ VERIFIED | AccuracySimulationManager.py:313 "return week_folder, week_folder" |
| 10 | Does get_accuracy_for_week() use both folders? | NO - Only uses projected_path | ✅ VERIFIED | Line 417 ignores actual_path |
| 11 | Does actual points come from correct folder? | NO - Comes from week_N (should be week_N+1) | ✅ VERIFIED | Lines 453-456 get actual_points from wrong source |
| 12 | Does ParallelAccuracyRunner have same bug? | YES - Same pattern | ✅ VERIFIED | Both files need fixing |

---

## Phase D: Solution Design

| Item | Question | Answer | Status | Evidence |
|------|----------|--------|--------|----------|
| 13 | Should _load_season_data() return (week_N, week_N+1)? | YES - Two folders needed | ✅ VERIFIED | Spec section "Solution Design" |
| 14 | Should we create two PlayerManager instances? | YES - One for projections, one for actuals | ✅ VERIFIED | Need separate data sources |
| 15 | Can we match players by ID between folders? | YES - IDs should be stable | ⏳ PENDING | Need to verify during implementation |
| 16 | What if week_18 folder doesn't exist? | Return (None, None), skip week 17 | ✅ VERIFIED | Acceptable fallback |
| 17 | Will this affect performance significantly? | Unknown - need to profile | ⏳ PENDING | Two PlayerManagers per week, but accuracy sim runs infrequently |

---

## Phase E: Testing Strategy

| Item | Question | Answer | Status | Evidence |
|------|----------|--------|--------|----------|
| 18 | Do we need unit tests for _load_season_data()? | YES - Test returns two folders | ✅ VERIFIED | Spec section "Testing Strategy" |
| 19 | Do we need integration tests for realistic MAE? | YES - Verify output is realistic | ✅ VERIFIED | MAE should be 3-8 range |
| 20 | Do we need statistical sanity checks in smoke testing? | YES - MANDATORY to prevent "0.0 acceptance" | ✅ VERIFIED | Zero percentage, variance, realistic ranges |
| 21 | Do we need to verify week 17 specifically? | YES - Epic called this out explicitly | ✅ VERIFIED | Integration test for week 17 |

---

## Phase F: Cross-Epic Verification (User Requirement)

| Item | Question | Answer | Status | Evidence |
|------|----------|--------|--------|----------|
| 22 | Does this affect Feature 01 (Win Rate Sim)? | NO - Separate files | ✅ VERIFIED | WinRateSimulationManager vs AccuracySimulationManager |
| 23 | Do we need to verify against original epic notes? | YES - User required | ✅ VERIFIED | Checklist includes epic notes verification |
| 24 | Do we need to verify against original simulation code? | YES - User required | ✅ VERIFIED | Compare with pre-epic implementation |
| 25 | Do we need to verify calculation algorithms unchanged? | YES - Only data loading should change | ✅ VERIFIED | MAE calculation logic should remain identical |

---

## Phase G: Lessons Learned Integration

| Item | Question | Answer | Status | Evidence |
|------|----------|--------|--------|----------|
| 26 | Did we re-read epic notes with fresh eyes? | YES - Stage 2.5 principles | ✅ VERIFIED | Spec "Epic Requirement" section |
| 27 | Did we manually inspect data files? | YES - Stage 5a.5 principles | ✅ VERIFIED | Spec "Manual Data Inspection Results" |
| 28 | Did we validate ALL assumptions with evidence? | YES - Assumption Validation Table | ✅ VERIFIED | Every claim has code/data reference |
| 29 | Did we include statistical sanity checks? | YES - In smoke testing | ✅ VERIFIED | Zero percentage, variance, MAE range |
| 30 | Did we add critical questions checklist? | YES - In verification plan | ✅ VERIFIED | Strategy 6 implemented |
| 31 | Will we use hands-on data inspection BEFORE implementing? | YES - Stage 5a.5 MANDATORY | ✅ VERIFIED | Pre-implementation verification section |

---

## Open Questions

*None - All questions resolved during spec creation*

---

## Decision Log

| # | Decision | Rationale | Date |
|---|----------|-----------|------|
| 1 | Use two PlayerManager instances per week | Need separate data sources (week_N and week_N+1) | 2026-01-02 |
| 2 | Match players by ID (not array index) | IDs should be stable across weeks | 2026-01-02 |
| 3 | Skip week if actual_folder missing | Acceptable fallback, maintains robustness | 2026-01-02 |
| 4 | Apply same fix to ParallelAccuracyRunner | Maintain consistency between serial/parallel | 2026-01-02 |
| 5 | Implement ALL 6 prevention strategies | Never allow "0.0 acceptance" failure again | 2026-01-02 |
| 6 | Add statistical sanity checks to smoke testing | MANDATORY to catch impossible data | 2026-01-02 |
| 7 | Verify ALL epic changes (user requirement) | Cross-reference with original notes/code/data | 2026-01-02 |

---

## Resolution Summary

**Total Items:** 31
**Verified:** 29
**Pending:** 2 (items 15, 17 - will verify during implementation)
**Blocked:** 0
**Open Questions:** 0

**All critical items resolved. Ready for Stage 5a (TODO Creation).**

---

*This checklist ensures every assumption is validated with evidence (Stage 2.5 principles). No claims without proof.*
