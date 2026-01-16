# Feature Checklist: score_penalty_application

**Feature:** Feature 02 - score_penalty_application
**Epic:** nfl_team_penalty
**Created:** 2026-01-12
**Last Updated:** 2026-01-12
**Status:** S2.P2 - Specification Phase

---

## Purpose

This checklist tracks decisions and questions that need user input. Agents create QUESTIONS in this file. Users provide ANSWERS. Agents CANNOT autonomously mark items as resolved.

---

## Questions Status Summary

**Total Questions:** 1
**Answered:** 1 (Simulation compatibility - approved 2026-01-13)
**Pending:** 0

---

## Open Questions

**No open questions** - Question 1 approved by user

---

## Resolved Questions

### Question 1: Simulation Code Compatibility ✅

**Status:** ✅ RESOLVED
**Asked:** 2026-01-13 (user request)
**Investigated:** 2026-01-13 (agent)
**Approved:** 2026-01-13 (user: "approve the simulation compatibility findings")

**Question:** Do simulations call PlayerScoringCalculator.score_player()? If so, do we need to update simulation code or JSON files to handle the new `nfl_team_penalty` parameter?

**Context:** We're adding a new `nfl_team_penalty=False` parameter to score_player(). While Feature 01 updates simulation config JSON files with default values ([], 1.0), we need to verify that simulation code still works after the parameter is introduced.

**User Requirement:** "While we don't need the simulation to simulate different versions of the new parameter, we DO need to ensure that the simulation works still after the parameter is introduced."

**Agent Investigation Results:**

Searched simulation codebase for `score_player()` usage:

1. **AccuracySimulationManager.py** (line 471):
   ```python
   scored = projected_mgr.score_player(
       player,
       use_weekly_projection=True,
       adp=False, player_rating=False, team_quality=True,
       performance=True, matchup=True, schedule=False,
       bye=False, injury=False,
   )
   ```
   - ✅ Calls PlayerManager.score_player()
   - ✅ Doesn't pass `nfl_team_penalty` → will use default (False)

2. **ParallelAccuracyRunner.py** (line 140):
   ```python
   scored = projected_mgr.score_player(
       player,
       use_weekly_projection=True,
       adp=False, player_rating=False, team_quality=True,
       performance=True, matchup=True, schedule=False,
       bye=False, injury=False,
   )
   ```
   - ✅ Calls PlayerManager.score_player()
   - ✅ Doesn't pass `nfl_team_penalty` → will use default (False)

3. **SimulatedOpponent.py** (lines 193, 211):
   - ❌ Defines LOCAL functions named `score_player()` (not related to PlayerManager)
   - ✅ Does NOT call PlayerManager.score_player()

**Agent's Recommendation:** **Option A - No changes needed**

**Rationale:**
- New parameter has default value (`nfl_team_penalty=False`)
- Python allows adding optional parameters with defaults (backward compatible)
- Existing simulation calls don't pass the parameter → automatically use default (False)
- Default value (False) is correct behavior (simulations should NOT apply team penalties)
- Feature 01 already updated simulation JSON configs with defaults ([], 1.0)
- Even if simulation loaded penalty settings, they wouldn't be used (flag=False)

**Files requiring changes (if user approves):** ZERO

**Verification needed during testing:**
- Run existing simulation tests after implementing Feature 02
- Verify simulations produce same results as before (no penalty applied)
- Confirm no errors from missing parameter

**Additional Investigation (ConfigManager instantiation):**

User asked: "What about when ConfigManagers are created? Investigate if there will be any issues when *reading* the config json files"

**Findings:**

Simulations create ConfigManager instances in 3 locations:
1. **SimulatedLeague.py** (line 175): `shared_config = ConfigManager(shared_dir)`
2. **AccuracySimulationManager.py** (line 405): `config_mgr = ConfigManager(temp_dir)`
3. **ParallelAccuracyRunner.py** (line 305): `config_mgr = ConfigManager(temp_dir)`

**ConfigManager initialization flow:**
1. `ConfigManager.__init__()` called
2. Calls `self._load_config()` (line 226)
3. Loads JSON file (line 875-876)
4. Calls `self._extract_parameters()` (line 917)
5. Extracts all parameters from JSON using `.get()` with defaults

**Feature 01's extraction approach (backward compatible):**
```python
self.nfl_team_penalty = self.parameters.get(self.keys.NFL_TEAM_PENALTY, [])
self.nfl_team_penalty_weight = self.parameters.get(self.keys.NFL_TEAM_PENALTY_WEIGHT, 1.0)
```

**Analysis:**
- ✅ **If JSON has keys** ([], 1.0): ConfigManager reads them, validation passes (empty list valid, 1.0 valid)
- ✅ **If JSON missing keys**: `.get()` returns defaults ([], 1.0) - no error
- ✅ **Backward compatible**: Works with or without keys in JSON

**Timing/Dependency protection:**
- Feature 02 spec (line 899): "Feature 01 MUST complete S5-S7 before Feature 02 begins S5"
- By the time Feature 02 is implemented:
  - ConfigManager ALREADY has extraction code (Feature 01 done)
  - Simulation JSONs ALREADY have keys with defaults ([], 1.0)
  - No transition issues (both code and data updated together in Feature 01)

**Conclusion:** **No issues when ConfigManager reads simulation JSON files**
- Feature 01 uses `.get()` with safe defaults (backward compatible)
- Validation allows empty list and weight=1.0
- Dependency structure prevents timing mismatches

**User's Answer:** "approve the simulation compatibility findings"

**User Decision:** No code changes needed. Simulations are backward compatible.

**Implementation Impact:**
- Files requiring code changes: ZERO
- Verification needed: Run existing simulation tests during S6 to confirm no regressions
- New requirement added: Requirement 9 (simulation compatibility verification)

**Source for new requirement:** User Answer to Question 1 (checklist.md)

---

## Analysis

**Why are there zero questions?**

This feature has zero open questions because:

1. **User was very explicit:**
   - Provided exact operation: "final score would be multiplied by 0.75" (line 8)
   - Specified mode: "during Add to Roster mode" (line 1)
   - Provided example: "any player on the Raiders, Jets, Giants, or Chiefs" (line 8)

2. **Implementation patterns are well-established:**
   - Scoring steps have consistent structure (13 existing steps to follow)
   - Penalty methods have consistent pattern (_apply_injury_penalty, _apply_bye_week_penalty)
   - Mode isolation uses parameter flags (adp, player_rating, etc.)
   - Test patterns are consistent (dedicated test file per feature)

3. **No genuine unknowns:**
   - No user preferences to choose between (operation is defined: multiplication)
   - No business logic ambiguity (straightforward penalty application)
   - No edge case ambiguity (all edge cases have precedents: weight=1.0, empty list)

4. **All requirements have sources:**
   - Epic Request: User explicitly stated (3 requirements: multiplication, mode, team check)
   - Derived Requirement: Logically necessary based on observed patterns (5 requirements: parameter, logging, reason string, pattern following, tests)
   - Zero assumptions (all were researched or explicitly stated)

**This is unusual but valid** - Most features have 3-5 open questions, but straightforward scoring features like this sometimes have zero unknowns when:
- User is explicit about requirements (what to do, where to do it)
- Existing patterns are clear and consistent (how to implement it)
- No new business logic is introduced (just applying existing pattern)

---

## Next Steps

1. **Phase 2.5:** Run Spec-to-Epic Alignment Check (verify no scope creep, no missing requirements)
2. **Gate 2:** Present checklist to user (explain zero questions, confirm understanding is correct)
3. **If user approves:** Skip S2.P3 (Refinement), proceed to acceptance criteria and S5 (Implementation Planning)

---

## User Approval

**Status:** ✅ APPROVED (Gate 2)
**Presented to user:** 2026-01-13
**User response:** "approved"
**Gate 2:** PASSED

**Question 1 Approval:**
**Status:** ✅ APPROVED
**Presented to user:** 2026-01-13
**User response:** "approve the simulation compatibility findings"
**Result:** Requirement 9 added to spec.md

---

**Notes:** This checklist has zero questions because all requirements were either explicitly stated by the user or derived from well-established PlayerScoringCalculator patterns. If user identifies missing questions or concerns during Gate 2 review, they will be added here.
