# Feature Specification: score_penalty_application

**Created:** 2026-01-12
**Status:** S2 COMPLETE (Awaiting S5 - Feature 01 dependency now resolved)
**Last Updated:** 2026-01-14 (S8.P1 Cross-Feature Alignment review)

**S8.P1 Alignment Review (2026-01-14):**
- Reviewed against Feature 01 (config_infrastructure) ACTUAL implementation
- All spec assumptions validated against real code (ConfigManager.py)
- Dependency status updated: Feature 01 now S7 complete (production-ready)
- **Classification:** NO SIGNIFICANT REWORK NEEDED
- **Changes:** Minor updates only (dependency status, verification notes)
- **Ready for S5:** Blocking dependency resolved, can proceed to Implementation Planning

---

## Epic Intent

**Purpose:** Ground this feature in the epic's original request BEFORE technical work

**Epic Notes File:** `nfl_team_penalty_notes.txt`
**Epic Notes Re-Read:** 2026-01-12
**Feature Context:** This is Feature 02 of 2 in the nfl_team_penalty epic

---

### Problem This Feature Solves

**User's Request (lines 1, 8):**
> "Have a penalty during Add to Roster mode for specific NFL teams"
> "for any player on the Raiders, Jets, Giants, or Chiefs... their final score would be multiplied by 0.75"

**Problem:** Users currently cannot have player scores automatically penalized based on team affiliation. Feature 01 created the config infrastructure to load penalty settings. THIS feature applies those penalty settings to player scores in Add to Roster mode.

---

### User's Explicit Requests

1. **Apply penalty in Add to Roster mode** (line 1)
   > "Have a penalty during Add to Roster mode for specific NFL teams"
   - Penalty applies only in Add to Roster mode
   - Other modes (draft, optimizer, trade analyzer) not mentioned

2. **Multiply final score by penalty weight** (line 8)
   > "their final score would be multiplied by 0.75"
   - Apply multiplication to "final score"
   - Example: 0.75 multiplier (from Feature 01 config)
   - Affects "any player" on penalized teams

3. **Check player's team against penalty list** (line 8)
   > "for any player on the Raiders, Jets, Giants, or Chiefs"
   - Check if player's team is in NFL_TEAM_PENALTY list
   - Example teams: ["LV", "NYJ", "NYG", "KC"] (from Feature 01)

---

### User's Constraints

1. **Mode-Specific** (line 1)
   > "during Add to Roster mode"
   - Penalty ONLY applies in Add to Roster mode
   - Not mentioned: Other modes should NOT be affected
   - Assumption: Draft mode, optimizer, trade analyzer use original scores

2. **User-Specific Setting** (line 10)
   > "This is a user-specific setting that will not be simulated in the simulations."
   - Simulations use default values ([], 1.0) from Feature 01
   - User's league_config.json has actual penalties
   - Ensures simulations remain objective

---

### Out of Scope (What User Explicitly Excluded)

- **Config infrastructure** - Feature 01 handles loading/validation (completed)
- **Other modes** - User only mentioned "Add to Roster mode" (line 1)
- **Penalty calculation complexity** - User specified simple multiplication (line 8), not complex formula
- **Transparency details** - User didn't mention logging or scoring reasons (assumption: need to add)

---

### User's End Goal

**Quote (lines 1, 10):**
> "Have a penalty during Add to Roster mode for specific NFL teams"
> "to reflect the user's team preferences and perferred strategy"

**End Goal:** Allow users to automatically see reduced scores for players from teams they want to avoid drafting, making it easier to follow their preferred draft strategy without manually adjusting for team bias.

---

### Technical Components Mentioned by User

1. **Add to Roster mode** (line 1)
   - Context where penalty applies
   - Not mentioned: Specific file/class name (need to research)

2. **Player's team** (line 8)
   - "for any player on the Raiders, Jets, Giants, or Chiefs"
   - Players have team affiliation
   - Need to access player.team attribute

3. **Final score** (line 8)
   - "their final score would be multiplied"
   - Score exists after some calculation
   - Need to research where/when "final score" is calculated

4. **Penalty multiplier** (line 8)
   - Simple multiplication operation
   - Example: score * 0.75

---

### Agent Verification

- [x] Epic notes file re-read on 2026-01-12
- [x] All quotes verified with line citations
- [x] User explicit requests vs. agent assumptions identified
- [x] Out-of-scope items documented
- [x] Technical components mentioned by user extracted

**Assumptions Identified (not mentioned in epic):**
- Specific Add to Roster mode file/class location
- Where "final score" is calculated (before or after other adjustments)
- Whether to log penalty application
- Whether to update scoring reasons
- How to handle edge cases (empty penalty list, weight = 1.0)

---

## Original Purpose (from S1)

Apply NFL team penalty multiplier to player scores in Add to Roster mode after the 10-step scoring algorithm completes.

---

## Components Affected

### 1. PlayerScoringCalculator.score_player() Method Signature

**File:** `league_helper/util/player_scoring.py`
**Lines to modify:** 333 (method signature)

**Source:** Derived Requirement
**Derivation:** Research discovered all modes (draft, optimizer, trade, add to roster) call the same score_player() method (research/SCORE_PENALTY_APPLICATION_DISCOVERY.md, Component 7). User specified penalty only for "Add to Roster mode" (epic notes line 1). Therefore, need parameter flag to enable/disable penalty per-mode. Established pattern uses boolean flags (adp=False, player_rating=True, etc. at line 333).

**Changes needed:**
```python
def score_player(self, p: FantasyPlayer, team_roster: List[FantasyPlayer],
                 use_weekly_projection=False, adp=False, player_rating=True,
                 team_quality=True, performance=True, matchup=False, schedule=True,
                 draft_round=-1, bye=True, injury=True,
                 roster: Optional[List[FantasyPlayer]] = None,
                 temperature=False, wind=False, location=False,
                 is_draft_mode: bool = False,
                 nfl_team_penalty=False) -> ScoredPlayer:  # <-- ADD THIS PARAMETER
```

**Default value:** False (opt-in, only Add to Roster mode enables)
**Rationale:** Safe default - other modes unaffected unless explicitly enabled

---

### 2. PlayerScoringCalculator Step 14 - Apply NFL Team Penalty

**File:** `league_helper/util/player_scoring.py`
**Lines to add:** After line 460 (after Step 13), before line 481 (return statement)

**Source:** Epic Request (epic notes line 8)
> "their final score would be multiplied by 0.75"

**Traceability:** User explicitly requested multiplication of "final score", meaning after all existing scoring steps complete.

**Changes needed:**
```python
# STEP 13: Apply Location bonus/penalty
if location:
    player_score, reason = self._apply_location_modifier(p, player_score)
    add_to_reasons(reason)
    self.logger.debug(f"Step 13 - After location scoring for {p.name}: {player_score:.2f}")

# STEP 14: Apply NFL Team Penalty (NEW)
if nfl_team_penalty:
    player_score, reason = self._apply_nfl_team_penalty(p, player_score)
    add_to_reasons(reason)
    self.logger.debug(f"Step 14 - After NFL team penalty for {p.name}: {player_score:.2f}")

# Summary logging
self.logger.debug(f"Scoring for {p.name}: final_score={player_score:.1f}")
```

**Pattern followed:** Matches existing steps (if flag: apply, add reason, log)

---

### 3. PlayerScoringCalculator._apply_nfl_team_penalty() Helper Method

**File:** `league_helper/util/player_scoring.py`
**Lines to add:** After line 716 (_apply_injury_penalty method)

**Source:** Derived Requirement
**Derivation:** Established pattern in player_scoring.py - all scoring steps have private helper methods (e.g., _apply_injury_penalty at lines 704-716, _apply_adp_multiplier at lines 504-512). Necessary to follow consistent code organization.

**Method to add:**
```python
def _apply_nfl_team_penalty(self, p: FantasyPlayer, player_score: float) -> Tuple[float, str]:
    """Apply NFL team penalty multiplier (Step 14)."""
    # Check if player's team is in penalty list
    if p.team in self.config.nfl_team_penalty:
        # Apply penalty weight (multiply final score)
        weight = self.config.nfl_team_penalty_weight
        reason = f"NFL Team Penalty: {p.team} ({weight:.2f}x)"
        return player_score * weight, reason

    # No penalty - return unchanged score and empty reason
    return player_score, ""
```

**Pattern followed:** Returns `(modified_score, reason_string)` or `(unchanged_score, "")` if no change

---

### 4. AddToRosterModeManager.get_recommendations() Method

**File:** `league_helper/add_to_roster_mode/AddToRosterModeManager.py`
**Lines to modify:** 281 (score_player call)

**Source:** Epic Request (epic notes line 1)
> "Have a penalty during Add to Roster mode for specific NFL teams"

**Traceability:** User explicitly specified "Add to Roster mode", so this is the ONLY mode that should enable the penalty.

**Changes needed:**
```python
scored_player = self.player_manager.score_player(
    p,
    draft_round=current_round,
    adp=True,
    player_rating=True,
    team_quality=True,
    performance=False,
    matchup=False,
    schedule=False,
    bye=True,
    injury=True,
    is_draft_mode=True,
    nfl_team_penalty=True  # <-- ADD THIS LINE (Add to Roster mode only)
)
```

---

### 5. PlayerManager.score_player() Method Signature

**File:** `league_helper/util/PlayerManager.py`
**Lines to modify:** 925 (method signature)

**Source:** Derived Requirement
**Derivation:** PlayerManager.score_player() delegates to PlayerScoringCalculator.score_player() (research line 925). To pass new parameter through, must add to PlayerManager's signature as well. Standard pattern for all scoring flags.

**Changes needed:**
```python
def score_player(self, p: FantasyPlayer, use_weekly_projection=False, adp=False,
                 player_rating=True, team_quality=True, performance=False, matchup=False,
                 schedule=False, draft_round=-1, bye=True, injury=True,
                 roster: Optional[List[FantasyPlayer]] = None, temperature=False, wind=False,
                 location=False, *, is_draft_mode: bool = False,
                 nfl_team_penalty=False) -> ScoredPlayer:  # <-- ADD THIS PARAMETER
```

---

### 6. Test File (new file to create)

**File:** `tests/league_helper/util/test_player_scoring_nfl_team_penalty.py`

**Source:** Derived Requirement
**Derivation:** All scoring features have dedicated test files (observed pattern: test_ConfigManager_max_positions.py, test_player_scoring.py). New scoring step requires test coverage for robustness.

**Test scenarios needed:**
1. Apply penalty when player team in penalty list
2. No penalty when player team not in penalty list
3. No penalty when penalty list is empty
4. No penalty when nfl_team_penalty flag is False (default)
5. Verify penalty weight = 0.75 produces correct score
6. Verify penalty weight = 1.0 produces unchanged score
7. Verify penalty weight = 0.0 produces score of 0.0
8. Verify reason string format when penalty applied
9. Verify empty reason string when no penalty
10. Verify other modes (draft, optimizer, trade) don't apply penalty

---

## Requirements

### Requirement 1: Add nfl_team_penalty Parameter to score_player()

**Description:** Add `nfl_team_penalty=False` parameter to PlayerScoringCalculator.score_player() and PlayerManager.score_player() method signatures

**Source:** Derived Requirement
**Derivation:** Research discovered all modes use same score_player() method (research Component 7). User constraint "during Add to Roster mode" (epic notes line 1) requires mode-specific behavior. Established pattern uses boolean parameters (adp, player_rating, etc.). Necessary to isolate penalty to Add to Roster mode only.

**Implementation:**
- Add parameter to PlayerScoringCalculator.score_player() signature (line 333)
- Add parameter to PlayerManager.score_player() signature (line 925)
- Default value: False (safe default, opt-in)

**Edge cases:**
- If forgotten, defaults to False (no penalty - safe)
- If other modes accidentally set True, penalty would apply (test coverage needed)

---

### Requirement 2: Check Player Team Against Penalty List

**Description:** In Step 14, check if `player.team` is in `config.nfl_team_penalty` list

**Source:** Epic Request (epic notes line 8)
> "for any player on the Raiders, Jets, Giants, or Chiefs"

**Traceability:** User explicitly requested checking player's team affiliation

**Implementation:**
```python
if p.team in self.config.nfl_team_penalty:
    # Apply penalty
```

**Technical details:**
- Player team: FantasyPlayer.team attribute (string, e.g., "LV")
- Penalty list: config.nfl_team_penalty (List[str] from Feature 01)
- Check uses Python `in` operator (efficient list membership test)

**Edge cases:**
- Empty penalty list ([]) → no matches, no penalties applied
- Player team not in list → check fails, no penalty applied
- Player team in list → check succeeds, penalty applied

---

### Requirement 3: Multiply Final Score by Penalty Weight

**Description:** When player team is in penalty list, multiply `player_score` by `config.nfl_team_penalty_weight`

**Source:** Epic Request (epic notes line 8)
> "their final score would be multiplied by 0.75"

**Traceability:** User explicitly requested multiplication operation on "final score"

**Implementation:**
```python
weight = self.config.nfl_team_penalty_weight
return player_score * weight, reason
```

**Technical details:**
- Weight value: config.nfl_team_penalty_weight (float from Feature 01, range 0.0-1.0)
- Operation: Simple multiplication (score * weight)
- "Final score" timing: After all 13 existing steps complete (after line 460)

**Edge cases:**
- Weight = 1.0 → score * 1.0 = unchanged (no penalty effect)
- Weight = 0.75 → score * 0.75 = 75% of original (example from epic)
- Weight = 0.0 → score * 0.0 = 0.0 (complete penalty)

---

### Requirement 4: Add Reason String for Transparency

**Description:** When penalty applied, add reason string to scoring reasons list

**Source:** Derived Requirement
**Derivation:** All scoring steps add reason strings for transparency (observed pattern at lines 386, 392, 398, etc.). User sees scoring breakdown in recommendations (AddToRosterModeManager lines 154-155 prints ScoredPlayer). Necessary for user understanding of why scores changed.

**Implementation:**
```python
reason = f"NFL Team Penalty: {p.team} ({weight:.2f}x)"
add_to_reasons(reason)
```

**Reason format:**
- When penalty applies: `"NFL Team Penalty: LV (0.75x)"`
- When no penalty: `""` (empty string, not added to list)

**Rationale:** Matches existing format pattern (shows what happened + value)

**Edge cases:**
- If penalty list empty → no reason added (empty string)
- If player team not in list → no reason added (empty string)
- If weight = 1.0 → reason still shown (user should know penalty was checked but had no effect)

---

### Requirement 5: Enable Penalty Only in Add to Roster Mode

**Description:** AddToRosterModeManager.get_recommendations() must pass `nfl_team_penalty=True` when calling score_player()

**Source:** Epic Request (epic notes line 1)
> "during Add to Roster mode"

**Traceability:** User explicitly specified mode-specific behavior

**Implementation:**
AddToRosterModeManager line 281:
```python
scored_player = self.player_manager.score_player(
    p,
    ...existing parameters...,
    nfl_team_penalty=True  # Add to Roster mode only
)
```

**Verification:** Other modes (draft, optimizer, trade) do NOT set this flag, so penalty doesn't apply

---

### Requirement 6: Log Penalty Application at Debug Level

**Description:** Log when penalty is applied using self.logger.debug()

**Source:** Derived Requirement
**Derivation:** All scoring steps log at debug level (lines 386, 392, 398, 410, 416, 422, 430, 436, 442, 448, 454, 460). Consistent logging essential for debugging and troubleshooting. Necessary to follow established pattern.

**Implementation:**
```python
self.logger.debug(f"Step 14 - After NFL team penalty for {p.name}: {player_score:.2f}")
```

**Log format:** Matches existing pattern (step number, action, player name, score)

---

### Requirement 7: Follow Existing Penalty Pattern

**Description:** _apply_nfl_team_penalty() method must follow established penalty method pattern

**Source:** Derived Requirement
**Derivation:** Existing penalty methods (_apply_injury_penalty at lines 704-716, _apply_bye_week_penalty) establish consistent pattern. Code organization and maintainability require following same pattern.

**Pattern requirements:**
1. Method signature: `def _apply_X(self, p: FantasyPlayer, player_score: float) -> Tuple[float, str]:`
2. Return tuple: `(modified_score, reason_string)`
3. Empty reason if no change: `return player_score, ""`
4. Descriptive reason if changed: `return new_score, "Penalty: details"`

**Implementation matches _apply_injury_penalty pattern exactly**

---

### Requirement 8: Create Comprehensive Unit Tests

**Description:** Create test file `test_player_scoring_nfl_team_penalty.py` with 10+ test scenarios

**Source:** Derived Requirement
**Derivation:** All scoring features have dedicated test files (observed pattern). New scoring step requires test coverage to prevent regressions and verify edge cases. Standard practice for all new features.

**Test scenarios (10 minimum):**
1. Penalty applied when team in list (score * weight)
2. No penalty when team not in list (score unchanged)
3. No penalty when penalty list empty (score unchanged)
4. No penalty when flag False (score unchanged)
5. Weight 0.75 produces correct score
6. Weight 1.0 produces unchanged score
7. Weight 0.0 produces score of 0.0
8. Reason string correct format when applied
9. Reason string empty when not applied
10. Mode isolation: other modes don't apply penalty

**Coverage target:** 100% of new code (_apply_nfl_team_penalty method, Step 14 logic)

---

### Requirement 9: Verify Simulation Compatibility (Backward Compatibility)

**Description:** Ensure simulations continue to work after adding `nfl_team_penalty` parameter (no code changes needed, verification only)

**Source:** User Answer to Question 1 (checklist.md)
**Traceability:** User requested verification: "ensure that the simulation works still after the parameter is introduced" → Agent investigated → User approved findings on 2026-01-13

**Investigation Results:**

**Category 1: score_player() Calls**
- AccuracySimulationManager.py (line 471) calls PlayerManager.score_player() without passing `nfl_team_penalty`
- ParallelAccuracyRunner.py (line 140) calls PlayerManager.score_player() without passing `nfl_team_penalty`
- Both will use default value (False) → correct behavior (no penalty in simulations)

**Category 2: ConfigManager Instantiation**
- Simulations create ConfigManager in 3 locations (SimulatedLeague.py, AccuracySimulationManager.py, ParallelAccuracyRunner.py)
- ConfigManager initialization: `__init__()` → `_load_config()` → `_extract_parameters()`
- Feature 01 extraction uses `.get()` with defaults: `self.parameters.get(NFL_TEAM_PENALTY, [])`
- If JSON has keys ([], 1.0): ConfigManager reads them, validation passes
- If JSON missing keys: `.get()` returns defaults ([], 1.0) - no error
- Backward compatible: Works with or without keys in JSON

**Implementation:**
- **No code changes needed** - Parameter defaults to False
- **No simulation JSON changes needed** - Feature 01 already updated them with defaults ([], 1.0)
- Simulations automatically use default (backward compatible)

**Verification during S6 (Testing):**
1. Run existing simulation tests after implementing Feature 02
2. Verify simulations produce same results as before (no penalty applied)
3. Confirm no errors from missing parameter
4. Verify AccuracySimulationManager and ParallelAccuracyRunner still function correctly
5. Confirm ConfigManager instantiation succeeds with or without JSON keys

**Files requiring changes:** ZERO

**Edge cases:**
- Simulation loads penalty config ([], 1.0) → No effect because flag=False
- Simulation doesn't load penalty config → Uses defaults ([], 1.0), flag=False
- Old simulation JSON (missing keys) with new code → Uses defaults, no error
- New simulation JSON (has keys) with new code → Reads values, no penalty applied (flag=False)
- All scenarios result in no penalty applied (correct behavior)

**Timing/Dependencies:**
- Feature 01 completes S5-S7 BEFORE Feature 02 begins S5
- By implementation time: ConfigManager has extraction code + simulation JSONs have defaults
- No transition period issues

---

## Data Structures

### Input: ConfigManager Attributes (from Feature 01)

**Structure:**
```python
self.config.nfl_team_penalty: List[str]       # ["LV", "NYJ", "NYG", "KC"]
self.config.nfl_team_penalty_weight: float    # 0.75
```

**Source:** Feature 01 (config_infrastructure)
**Validation:** Feature 01 validates team abbreviations and weight range

---

### Input: Player Team Attribute

**Structure:**
```python
player.team: str  # "LV", "NYJ", "NYG", "KC", etc.
```

**Source:** FantasyPlayer.py line 91
**Format:** Uppercase 2-3 letter abbreviation (matches ALL_NFL_TEAMS list)

---

### Internal: Scoring Flow

**Before Step 14:**
```python
player_score: float  # Score after Steps 1-13 (e.g., 120.5)
```

**After Step 14 (penalty applied):**
```python
player_score: float  # Score * weight (e.g., 120.5 * 0.75 = 90.375)
reason: str          # "NFL Team Penalty: LV (0.75x)"
```

**After Step 14 (no penalty):**
```python
player_score: float  # Score unchanged (e.g., 120.5)
reason: str          # "" (empty)
```

---

### Output: ScoredPlayer Object

**Structure:**
```python
ScoredPlayer(
    player=p,                          # Original FantasyPlayer
    score=player_score,                # Final score (after penalty if applied)
    reasons=[...list of reason strings...],  # Includes penalty reason if applied
    projected_points=calculated_projection
)
```

**User sees:** Recommendations list in Add to Roster mode shows ScoredPlayer.__str__() which includes score and reasons

---

## Algorithms

### Algorithm 1: NFL Team Penalty Check and Application

**Pseudocode:**
```python
def _apply_nfl_team_penalty(player, current_score):
    # Step 1: Check if player's team is in penalty list
    if player.team not in config.nfl_team_penalty:
        # No penalty - return unchanged
        return current_score, ""

    # Step 2: Get penalty weight from config
    weight = config.nfl_team_penalty_weight

    # Step 3: Apply multiplication
    new_score = current_score * weight

    # Step 4: Format reason string
    reason = f"NFL Team Penalty: {player.team} ({weight:.2f}x)"

    # Step 5: Return modified score and reason
    return new_score, reason
```

**Edge case handling:**
- Empty penalty list → check fails at Step 1, returns unchanged
- Weight = 1.0 → multiplication at Step 3 produces same score (no effect)
- Weight = 0.0 → multiplication produces 0.0 (complete penalty)
- Player team not in list → check fails at Step 1, returns unchanged

---

### Algorithm 2: Mode Isolation via Parameter Flag

**Pseudocode:**
```python
# Add to Roster Mode (line 281)
score_player(p, ..., nfl_team_penalty=True)   # Penalty enabled

# Draft Mode (other file)
score_player(p, ..., nfl_team_penalty=False)  # Penalty disabled (default)

# Inside score_player():
if nfl_team_penalty:  # Only True for Add to Roster
    player_score, reason = _apply_nfl_team_penalty(p, player_score)
    add_to_reasons(reason)
else:
    # Skip Step 14, no penalty applied
    pass
```

**Ensures:** Penalty only applies when explicitly enabled (Add to Roster mode only)

---

## Dependencies

### This Feature Depends On:

1. **Feature 01: config_infrastructure**
   - **Status:** ✅ S7 COMPLETE (2026-01-14) - Production-ready
   - **Purpose:** Provides config.nfl_team_penalty and config.nfl_team_penalty_weight
   - **Usage:** Read-only access in _apply_nfl_team_penalty() method
   - **Blocking:** Cannot implement Feature 02 until Feature 01 is complete
   - **[UPDATED based on feature_01_config_infrastructure S8.P1 alignment review 2026-01-14]**
   - **Verified Implementation:**
     - Instance variables: `self.nfl_team_penalty: List[str]`, `self.nfl_team_penalty_weight: float`
     - Extraction: Uses `.get()` with defaults ([], 1.0) for backward compatibility
     - Validation: Team abbreviations validated against ALL_NFL_TEAMS, weight range 0.0-1.0
     - All spec assumptions match actual implementation

2. **FantasyPlayer.team attribute**
   - **Status:** Exists (utils/FantasyPlayer.py line 91)
   - **Purpose:** Player team abbreviation (e.g., "LV")
   - **Usage:** Read-only access in penalty check

3. **PlayerScoringCalculator**
   - **Status:** Exists (league_helper/util/player_scoring.py lines 48-716)
   - **Purpose:** Scoring algorithm implementation
   - **Usage:** Add Step 14 to existing algorithm

4. **AddToRosterModeManager**
   - **Status:** Exists (league_helper/add_to_roster_mode/AddToRosterModeManager.py lines 39-505)
   - **Purpose:** Add to Roster mode implementation
   - **Usage:** Modify get_recommendations() to enable penalty flag

---

### This Feature Blocks:

**None** - This is the final feature in the epic

---

### This Feature is Independent Of:

**All other epic features** - This is the only remaining feature in epic (Feature 01 complete)

---

## Phase 2.5: Spec-to-Epic Alignment Check (MANDATORY GATE)

**Date:** 2026-01-12
**Result:** ✅ PASSED

### Step 2.5.1: Epic Intent Re-Read ✓

Epic Intent section reviewed. User's explicit requests identified:
1. Line 1: "Have a penalty during Add to Roster mode"
2. Line 8: "their final score would be multiplied by 0.75"
3. Line 8: "for any player on the Raiders, Jets, Giants, or Chiefs"
4. Line 10: "This is a user-specific setting that will not be simulated"

### Step 2.5.2: Requirement Source Verification ✓

All 8 requirements verified:
- **3 Epic Request sources:** Requirements 2, 3, 5 (direct user quotes)
- **5 Derived Requirement sources:** Requirements 1, 4, 6, 7, 8 (clear rationale)
- **All derivations justified:** Mode isolation, transparency, consistency, code organization, quality

### Step 2.5.3: Scope Creep Check ✓

**Result:** Zero scope creep detected
- Requirements 2, 3, 5: Direct user requests
- Requirements 1, 4, 6, 7, 8: Necessary for correct implementation (mode isolation, transparency, patterns, tests)
- No features added beyond user's request

### Step 2.5.4: Missing Requirements Check ✓

**Result:** Zero missing requirements
- "penalty during Add to Roster mode" (line 1) → Requirement 5 ✓
- "multiply by 0.75" (line 8) → Requirement 3 ✓
- "check player team" (line 8) → Requirement 2 ✓
- "not simulated" (line 10) → Addressed in spec (lines 57-62) ✓

### Step 2.5.5: Overall Alignment Result

**PASSED** - Spec fully aligned with epic request:
- ✅ All requirements have valid sources
- ✅ Zero scope creep
- ✅ Zero missing requirements
- ✅ Complete traceability

**Ready for Phase 2.6 (Gate 2: Present Checklist to User)**

---

## Gate 2: User Checklist Approval

**Date:** 2026-01-13
**Result:** ✅ PASSED

**Checklist presented:** feature_02_score_penalty_application/checklist.md
- Total questions: 0
- User approved: "approved"
- Zero questions rationale accepted: User was explicit, patterns established, no genuine unknowns

**Next Steps:**
- Skip Phase 3 (Interactive Question Resolution) - zero questions
- Proceed to Phase 4 (Dynamic Scope Adjustment)
- Phase 5 (Cross-Feature Alignment)
- Phase 6 (Acceptance Criteria & User Approval)

---

## S2.P3: Refinement Phase

### Phase 3: Interactive Question Resolution

**Status:** ✅ SKIPPED (zero questions to resolve)

**Checklist Status:** 0 open questions, 0 resolved

**Rationale:** Checklist has zero questions because user was explicit about requirements and implementation patterns are well-established.

---

### Phase 4: Dynamic Scope Adjustment

**Date:** 2026-01-13
**Result:** ✅ PASSED

**Step 4.1: Checklist Item Count**
- Total items: 0 (0 resolved, 0 open)

**Step 4.2: Feature Size Evaluation**
- **Size Category:** Straightforward (<20 items)
- **Action:** No split needed
- **Complexity:** Low (straightforward scoring feature)

**Step 4.4: New Work Discovered**
- **Result:** None
- **Scope Creep:** Zero
- **Rationale:** All requirements derived from user's explicit request or established patterns

**Next:** Phase 5 (Cross-Feature Alignment)

---

### Phase 5: Cross-Feature Alignment

**Date:** 2026-01-13
**Result:** ✅ PASSED (zero conflicts)

**Compared To:**
- Feature 01: config_infrastructure (S2 Complete 2026-01-12)

**Alignment Status:** ✅ No conflicts found

**Comparison Categories:**
1. Components Affected: Zero overlapping files (clean separation) ✓
2. Data Structures: Perfectly aligned (Feature 01 provides, Feature 02 consumes) ✓
3. Requirements: No duplicates (distinct responsibilities) ✓
4. Assumptions: Compatible (weight range 0.0-1.0, team format uppercase) ✓
5. Integration Points: Dependencies correctly documented in both specs ✓

**Details:**
- Feature 01 provides: `config.nfl_team_penalty` (List[str]), `config.nfl_team_penalty_weight` (float)
- Feature 02 consumes: Same structures via read-only access in `_apply_nfl_team_penalty()`
- Data structure match: Perfect alignment (validated types, value ranges compatible)
- Implementation sequencing: Feature 01 must complete S5-S7 before Feature 02 begins S5

**Changes Made:** None required (zero conflicts)

**Alignment Report:** `research/ALIGNMENT_feature02_vs_feature01.md`

**Verified By:** Agent
**Date:** 2026-01-13

**Next:** Phase 6 (Acceptance Criteria & User Approval)

---

## Acceptance Criteria

**Feature:** Feature 02 - score_penalty_application
**Status:** Awaiting user approval
**Created:** 2026-01-13

---

### 1. Behavior Changes

**New Functionality:**
- PlayerScoringCalculator applies Step 14 (NFL team penalty) after all existing 13 steps complete
- When a player's team is in the penalty list AND nfl_team_penalty flag is True, multiply final score by penalty weight
- Penalty reason appears in scoring breakdown when applied (e.g., "NFL Team Penalty: LV (0.75x)")
- Add to Roster mode recommendations show reduced scores for penalized teams

**Modified Functionality:**
- PlayerScoringCalculator.score_player() accepts new `nfl_team_penalty=False` parameter
- PlayerManager.score_player() accepts new `nfl_team_penalty=False` parameter (pass-through)
- AddToRosterModeManager.get_recommendations() calls score_player() with `nfl_team_penalty=True`
- 13-step algorithm becomes 14-step algorithm (Step 14 added conditionally)

**No Changes:**
- Other modes (draft, optimizer, trade) continue using score_player() without penalty (flag defaults to False)
- Simulations unaffected (use default configs [], 1.0 from Feature 01)
- Player data, config loading, or file I/O unchanged

---

### 2. Files Modified

**New Files (1):**
- `tests/league_helper/util/test_player_scoring_nfl_team_penalty.py` - Unit tests for penalty logic

**Existing Files Modified (3):**
1. `league_helper/util/player_scoring.py`
   - Line 333: Add `nfl_team_penalty=False` parameter to score_player() signature
   - After line 460: Add Step 14 conditional logic (if nfl_team_penalty: apply penalty, add reason, log)
   - After line 716: Add `_apply_nfl_team_penalty()` helper method

2. `league_helper/add_to_roster_mode/AddToRosterModeManager.py`
   - Line 281: Add `nfl_team_penalty=True` argument to score_player() call

3. `league_helper/util/PlayerManager.py`
   - Line 925: Add `nfl_team_penalty=False` parameter to score_player() signature (pass through to PlayerScoringCalculator)

**Data Files:**
- None (config files modified by Feature 01)

---

### 3. Data Structures

**New Structures:**
- None (consumes existing structures from Feature 01)

**Modified Structures:**
- `PlayerScoringCalculator.score_player()` signature: Added `nfl_team_penalty: bool` parameter
- `PlayerManager.score_player()` signature: Added `nfl_team_penalty: bool` parameter
- `ScoredPlayer.reasons` list: May include "NFL Team Penalty: {team} ({weight}x)" when penalty applied

**Consumed Structures (from Feature 01):**
- `config.nfl_team_penalty: List[str]` - Read-only access in _apply_nfl_team_penalty()
- `config.nfl_team_penalty_weight: float` - Read-only access in _apply_nfl_team_penalty()

**Existing Structures Used:**
- `FantasyPlayer.team: str` - Read for team membership check

---

### 4. API/Interface Changes

**New Methods (1):**
```python
PlayerScoringCalculator._apply_nfl_team_penalty(p: FantasyPlayer, player_score: float) -> Tuple[float, str]
```
- Private helper method following existing penalty pattern
- Returns (modified_score, reason) or (unchanged_score, "")

**Modified Methods (3):**

1. `PlayerScoringCalculator.score_player()` - Signature change:
   ```python
   # Before: ...is_draft_mode: bool = False) -> ScoredPlayer:
   # After:  ...is_draft_mode: bool = False, nfl_team_penalty=False) -> ScoredPlayer:
   ```

2. `PlayerManager.score_player()` - Signature change:
   ```python
   # Before: ...is_draft_mode: bool = False) -> ScoredPlayer:
   # After:  ...is_draft_mode: bool = False, nfl_team_penalty=False) -> ScoredPlayer:
   ```

3. `AddToRosterModeManager.get_recommendations()` - Call site change:
   ```python
   # Before: ...is_draft_mode=True)
   # After:  ...is_draft_mode=True, nfl_team_penalty=True)
   ```

**No Changes:**
- ScoredPlayer dataclass (only adds reason strings to existing list)
- FantasyPlayer dataclass
- ConfigManager (reads only)

---

### 5. Testing

**Test File:** `tests/league_helper/util/test_player_scoring_nfl_team_penalty.py`

**Test Scenarios (11 total):**
1. Penalty applied when team in list AND flag True → score * weight
2. No penalty when team NOT in list (flag True) → score unchanged
3. No penalty when flag False (default) → score unchanged, even if team in list
4. No penalty when penalty list empty → score unchanged
5. Weight 0.75 produces correct score → verify exact calculation
6. Weight 1.0 produces unchanged score → verify edge case
7. Weight 0.0 produces score of 0.0 → verify edge case
8. Reason string correct format when applied → verify transparency
9. Reason string empty when not applied → verify clean output
10. Mode isolation: draft/optimizer/trade don't apply penalty → verify other modes
11. **Simulation compatibility: Run existing simulation tests → verify no regressions** (Requirement 9 - User approved 2026-01-13)

**Coverage Target:**
- 100% coverage of new code (_apply_nfl_team_penalty method, Step 14 conditional logic)
- Integration test: Full scoring flow with penalty in Add to Roster mode
- **Regression test: Existing simulation tests pass without modification** (backward compatibility verification)

**Edge Cases Tested:**
- Empty penalty list ([])
- Weight at boundaries (0.0, 1.0)
- Player team not in list
- Flag False (default behavior)
- Multiple players, some penalized, some not

**Simulation Verification (Requirement 9):**
- AccuracySimulationManager tests pass (no parameter changes needed)
- ParallelAccuracyRunner tests pass (no parameter changes needed)
- Simulation results unchanged from baseline (no penalty applied)
- ConfigManager instantiation succeeds (with or without JSON keys)

---

### 6. Dependencies

**This Feature Depends On:**

1. **Feature 01: config_infrastructure** (BLOCKING DEPENDENCY - NOW RESOLVED)
   - **Status:** ✅ S7 COMPLETE (2026-01-14) - Production-ready, all tests passing (2496/2496)
   - **Provides:** config.nfl_team_penalty (List[str]), config.nfl_team_penalty_weight (float)
   - **Impact:** Feature 02 can NOW proceed to S5 (Implementation Planning) - blocking dependency resolved
   - **Sequencing:** Feature 01 S5-S7 ✅ COMPLETE → Feature 02 ready for S5
   - **[UPDATED based on feature_01_config_infrastructure S8.P1 alignment review 2026-01-14]**

2. **Existing Codebase:**
   - PlayerScoringCalculator (exists, will modify)
   - AddToRosterModeManager (exists, will modify)
   - PlayerManager (exists, will modify)
   - FantasyPlayer.team attribute (exists, read-only)

**This Feature Blocks:**
- None (final feature in epic)

**External Dependencies:**
- None (all dependencies internal to codebase)

---

### 7. Edge Cases & Error Handling

**Edge Cases Handled:**

1. **Empty penalty list ([]):**
   - Team check fails for all players
   - No penalty applied to anyone
   - Empty reason strings

2. **Penalty weight = 1.0:**
   - Multiplication has no effect (score * 1.0 = score)
   - Reason still shown (transparency: penalty was checked)

3. **Penalty weight = 0.0:**
   - Score becomes 0.0 (complete penalty)
   - Valid use case (user wants to completely avoid certain teams)

4. **Player team not in penalty list:**
   - Team check fails
   - No penalty applied
   - Empty reason string

5. **nfl_team_penalty flag False (default):**
   - Step 14 skipped entirely
   - Other modes (draft, optimizer, trade) unaffected
   - Safe default behavior

6. **Player team in list, flag True:**
   - Penalty applied correctly
   - Reason string added to transparency list
   - Debug logging shows penalty application

**Error Conditions:**
- **No errors expected** - Feature 01 validates all config values (team abbreviations, weight range 0.0-1.0)
- If config invalid, error occurs during config loading (Feature 01), NOT during scoring (Feature 02)
- Defensive programming: Empty list and weight boundaries handled gracefully

---

### 8. Documentation

**User-Facing Documentation:**
- None required (penalty appears automatically in Add to Roster mode scoring breakdowns)
- Scoring reason strings are self-explanatory: "NFL Team Penalty: LV (0.75x)"

**Developer Documentation:**
- Code comments in _apply_nfl_team_penalty() method (docstring)
- Inline comment at Step 14 explaining conditional application
- README.md updated with S2 completion status

**Existing Documentation Updates:**
- None required (scoring algorithm docs may optionally be updated, but not mandatory)

---

### 9. User Approval

- [x] **I approve these acceptance criteria**

**Approval Timestamp:** 2026-01-13

**Approval Notes:**
User approved acceptance criteria on 2026-01-13. No modifications requested. Feature 02 ready for S3 (Cross-Feature Sanity Check) or S5 (Implementation Planning).

---

## User Approval (Gate 4)

**Status:** ✅ APPROVED
**Presented to user:** 2026-01-13
**User response:** "approved"
**Gate 4:** PASSED

**Approval includes:**
- All 9 requirements (3 Epic Request, 5 Derived, 1 User Answer)
- All 6 components affected
- All acceptance criteria (behavior changes, files, data structures, API changes, testing, dependencies, edge cases, documentation)
- Requirement 9 (simulation compatibility) based on approved Question 1

---

## Notes

Specification completed in S2.P2 (Specification Phase). All requirements have traceability (Epic Request or Derived). Phase 2.5 alignment check PASSED. Gate 2 (User Checklist Approval) PASSED. S2.P3 Phases 3-5 complete. Ready for user approval of acceptance criteria (Gate 4).
