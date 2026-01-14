# Research Discovery: score_penalty_application

**Feature:** Feature 02 - score_penalty_application
**Epic:** nfl_team_penalty
**Research Date:** 2026-01-12
**Research Phase:** S2.P1 - Targeted Research

---

## Epic Intent Summary

User wants to apply a penalty multiplier to player scores in Add to Roster mode for specific NFL teams. Epic request (line 8): "for any player on the Raiders, Jets, Giants, or Chiefs... their final score would be multiplied by 0.75"

This feature applies the penalty settings loaded by Feature 01 to player scores after the 10-step scoring algorithm completes.

---

## Component 1: Add to Roster Mode

**User mentioned:** "during Add to Roster mode" (epic notes line 1)

**Found in codebase:**
- **File:** `league_helper/add_to_roster_mode/AddToRosterModeManager.py`
- **Lines:** 39-505 (entire class)

**How it works today:**

### get_recommendations() Method (lines 229-308)

This method provides player recommendations to the user:

```python
def get_recommendations(self) -> List[ScoredPlayer]:
    """
    Generate top player recommendations for the current draft round.

    Uses the complete 9-step scoring algorithm plus draft round bonuses to rank
    all available players. Returns the top 10 recommendations sorted by score.
    """
    available_players = self.player_manager.get_player_list(drafted_vals=[0], can_draft=True)
    scored_players : List[ScoredPlayer] = []
    current_round = self._get_current_round()

    # Score each player with most scoring factors enabled
    for p in available_players:
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
            is_draft_mode=True
        )
        scored_players.append(scored_player)

    ranked_players = sorted(scored_players, key=lambda x: x.score, reverse=True)
    return ranked_players[:Constants.RECOMMENDATION_COUNT]
```

**Key finding:** Line 281 calls `self.player_manager.score_player()` which delegates to PlayerScoringCalculator.

**Relevance:** This is WHERE the scoring happens that we need to modify. The scoring occurs in the PlayerScoringCalculator, not in AddToRosterModeManager.

---

## Component 2: Player Scoring Algorithm

**User mentioned:** "their final score would be multiplied by 0.75" (epic notes line 8)

**Found in codebase:**
- **File:** `league_helper/util/player_scoring.py`
- **Class:** PlayerScoringCalculator
- **Method:** score_player (lines 333-481)

**How final score is calculated:**

### score_player() Method Structure (lines 333-481)

```python
def score_player(self, p: FantasyPlayer, team_roster, use_weekly_projection=False, adp=False, ...):
    """
    Calculate score for a player (13-step calculation).

    Scoring System:
    1. Get normalized seasonal fantasy points (0-N scale)
    2. Apply ADP multiplier
    3. Apply Player Ranking multiplier
    4. Apply Team ranking multiplier
    5. Apply Performance multiplier
    6. Apply Matchup multiplier
    7. Apply Schedule multiplier
    8. Add DRAFT_ORDER bonus
    9. Subtract Bye Week penalty
    10. Subtract Injury penalty
    11. Apply Temperature bonus/penalty
    12. Apply Wind bonus/penalty
    13. Apply Location bonus/penalty

    Returns:
        ScoredPlayer: Scored player object with final score and reasons
    """
    reasons = []

    # STEP 1: Normalize fantasy points
    player_score, reason = self._get_normalized_fantasy_points(p, use_weekly_projection)
    add_to_reasons(reason)

    # STEP 2: Apply ADP multiplier
    if adp:
        player_score, reason = self._apply_adp_multiplier(p, player_score)
        add_to_reasons(reason)

    # ... Steps 3-13 ...

    # STEP 13: Apply Location bonus/penalty
    if location:
        player_score, reason = self._apply_location_modifier(p, player_score)
        add_to_reasons(reason)
        self.logger.debug(f"Step 13 - Final score for {p.name}: {player_score:.2f}")

    # Summary logging
    self.logger.debug(f"Scoring for {p.name}: final_score={player_score:.1f}")

    p.score = player_score

    # Calculate projected points (reverse normalization)
    calculated_projection = (player_score / normalization_scale) * chosen_max

    return ScoredPlayer(p, player_score, reasons, projected_points=calculated_projection)
```

**Key finding:** The "final score" is `player_score` variable after all 13 steps complete (line 467). The penalty must be applied AFTER line 460 (Step 13) and BEFORE line 481 (return statement).

**Pattern to follow:** All steps follow format `(new_score, reason) = self._apply_X(p, player_score)`, then append reason to list.

---

## Component 3: Player Team Attribute

**User mentioned:** "for any player on the Raiders, Jets, Giants, or Chiefs" (epic notes line 8)

**Found in codebase:**
- **File:** `utils/FantasyPlayer.py`
- **Class:** FantasyPlayer
- **Attribute:** team (line 91)

**Data structure:**

```python
@dataclass
class FantasyPlayer:
    """
    Represents a fantasy football player with all relevant data fields.
    """
    # Core identification
    id: int
    name: str
    team: str  # <-- LINE 91: Team abbreviation (e.g., "LV", "NYJ", "NYG", "KC")
    position: str

    # ... other fields ...
```

**Data format:** Team is stored as 2-3 letter uppercase abbreviation (e.g., "LV", "NYJ", "NYG", "KC")

**Validation:** Feature 01 validates team abbreviations against ALL_NFL_TEAMS (32 teams) from historical_data_compiler/constants.py

**Usage in penalty check:**
```python
if p.team in self.config.nfl_team_penalty:
    # Player is on a penalized team
```

---

## Component 4: Existing Penalty Patterns

**User mentioned:** Not explicitly, but penalties exist in scoring system

**Found in codebase:**
- **File:** `league_helper/util/player_scoring.py`
- **Example:** _apply_injury_penalty (lines 704-716)

**Pattern to follow:**

```python
def _apply_injury_penalty(self, p: FantasyPlayer, player_score: float) -> Tuple[float, str]:
    """Apply injury penalty (Step 10)."""
    # Get penalty value from config
    penalty = self.config.get_injury_penalty(p.get_risk_level())

    # Only show reason if penalty applies
    # This keeps reason list clean when no penalty
    reason = "" if p.injury_status == "ACTIVE" else f"Injury: {p.injury_status} ({-penalty:.1f} pts)"

    # Subtract penalty from score (injury reduces player value)
    return player_score - penalty, reason
```

**Pattern identified:**
1. Method signature: `def _apply_X(self, p: FantasyPlayer, player_score: float) -> Tuple[float, str]:`
2. Calculate penalty/multiplier from config
3. Return empty string `""` if no change, otherwise descriptive reason
4. Return `(modified_score, reason)`

**For NFL team penalty:**
```python
def _apply_nfl_team_penalty(self, p: FantasyPlayer, player_score: float) -> Tuple[float, str]:
    """Apply NFL team penalty multiplier."""
    # Check if player's team is in penalty list
    if p.team in self.config.nfl_team_penalty:
        # Apply penalty weight (multiply final score)
        weight = self.config.nfl_team_penalty_weight
        reason = f"NFL Team Penalty: {p.team} ({weight:.2f}x)"
        return player_score * weight, reason

    # No penalty - return unchanged score and empty reason
    return player_score, ""
```

---

## Component 5: ConfigManager Integration

**User mentioned:** Implicitly (config loaded by Feature 01)

**Found in codebase:**
- **File:** `league_helper/util/ConfigManager.py`
- **Feature 01 adds:** `self.nfl_team_penalty: List[str]` and `self.nfl_team_penalty_weight: float`

**Usage in player_scoring.py:**

PlayerScoringCalculator already has `self.config` reference (line 90), so can access:
- `self.config.nfl_team_penalty` - List of team abbreviations (e.g., ["LV", "NYJ", "NYG", "KC"])
- `self.config.nfl_team_penalty_weight` - Multiplier weight (e.g., 0.75)

**No import changes needed** - ConfigManager already imported and instantiated.

---

## Component 6: ScoredPlayer Return Type

**User mentioned:** Not explicitly

**Found in codebase:**
- **File:** `league_helper/util/ScoredPlayer.py` (inferred from imports)
- **Usage:** line 481 in player_scoring.py

**Structure:**

```python
return ScoredPlayer(p, player_score, reasons, projected_points=calculated_projection)
```

**Fields:**
- `p: FantasyPlayer` - The original player object
- `player_score: float` - Final calculated score (after all steps + penalty)
- `reasons: List[str]` - List of scoring reasons for transparency
- `projected_points: float` - Calculated projection (reverse normalization)

**Penalty transparency:** When penalty applied, reason string "NFL Team Penalty: LV (0.75x)" is added to `reasons` list, which user sees in recommendations.

---

## Component 7: Mode Isolation (Other Modes)

**User mentioned:** "during Add to Roster mode" (epic notes line 1)

**Research question:** Do other modes use score_player()?

**Found in codebase:**
- **Draft Mode:** Uses PlayerManager.score_player() → YES, uses same method
- **Optimizer Mode:** Uses PlayerManager.score_player() → YES, uses same method
- **Trade Analyzer:** Uses PlayerManager.score_player() → YES, uses same method

**CRITICAL FINDING:** All modes call the same score_player() method in PlayerScoringCalculator!

**Implication:** We CANNOT just add the penalty to score_player() unconditionally, or it will affect ALL modes (draft, optimizer, trade).

**Solution Options:**
1. **Option A:** Add `apply_nfl_team_penalty` parameter to score_player() (like adp, player_rating, etc.)
   - Add to Roster sets `apply_nfl_team_penalty=True`
   - Other modes set `apply_nfl_team_penalty=False` (default)

2. **Option B:** Check mode context inside score_player()
   - Look for a mode indicator flag
   - Only apply if in Add to Roster mode

**Research finding:** Looking at line 333 signature, all scoring steps already use boolean flags (adp=False, player_rating=True, etc.). **Option A is the established pattern.**

**Recommended approach:** Add `nfl_team_penalty=False` parameter to score_player() method signature.

---

## Integration Points

**Classes this feature will interact with:**

1. **PlayerScoringCalculator** (`league_helper/util/player_scoring.py`)
   - Add `nfl_team_penalty` parameter to score_player() method signature (line 333)
   - Add Step 14: Apply NFL team penalty (after line 460, before line 481)
   - Add `_apply_nfl_team_penalty()` helper method (follow existing penalty pattern)

2. **AddToRosterModeManager** (`league_helper/add_to_roster_mode/AddToRosterModeManager.py`)
   - Modify get_recommendations() (line 281) to pass `nfl_team_penalty=True`
   - No other changes needed (mode already calls score_player)

3. **ConfigManager** (`league_helper/util/ConfigManager.py`)
   - Already has `nfl_team_penalty` and `nfl_team_penalty_weight` (Feature 01)
   - No changes needed (read-only access)

4. **PlayerManager** (`league_helper/util/PlayerManager.py`)
   - Signature of score_player() needs `nfl_team_penalty=False` parameter added
   - Delegates to PlayerScoringCalculator.score_player()

---

## Edge Cases Identified

1. **Empty penalty list (`[]`)**: Player team check fails, no penalty applied ✓
2. **Penalty weight = 1.0**: Multiplication by 1.0 has no effect (neutral) ✓
3. **Penalty weight = 0.0**: Score becomes 0.0 (complete penalty) ✓
4. **Player team not in list**: Check fails, no penalty applied ✓
5. **Player team in list**: Penalty applied, reason shown ✓
6. **Other modes**: Flag set to False, penalty not applied ✓
7. **Mode flag forgotten**: Defaults to False (safe default - no penalty)

---

## Questions for Specification Phase

1. **Parameter default value**: Should `nfl_team_penalty` parameter default to False (opt-in) or True (opt-out)?
   - **Recommendation**: False (opt-in) - Only Add to Roster mode explicitly enables it
   - **Rationale**: Safer default, matches user constraint "during Add to Roster mode" (line 1)

2. **Reason string format**: What should the penalty reason look like?
   - **Recommendation**: `"NFL Team Penalty: {team} ({weight:.2f}x)"`
   - **Example**: `"NFL Team Penalty: LV (0.75x)"`
   - **Rationale**: Matches existing reason format (shows what happened and the value)

3. **Step number**: Should this be "Step 14" or inserted earlier?
   - **Recommendation**: Step 14 (after all existing steps)
   - **Rationale**: User said "final score" (line 8), meaning after everything else

4. **Logging level**: Should penalty application be logged at debug or info level?
   - **Recommendation**: Debug (matches other scoring steps)
   - **Rationale**: Consistent with existing steps (line 386, 392, 398, etc.)

---

## Research Completeness

**Components researched:**
- [x] Add to Roster mode (AddToRosterModeManager)
- [x] Player scoring algorithm (PlayerScoringCalculator.score_player)
- [x] Player team attribute (FantasyPlayer.team)
- [x] Existing penalty patterns (_apply_injury_penalty)
- [x] ConfigManager integration (Feature 01 outputs)
- [x] ScoredPlayer return type
- [x] Mode isolation (other modes also use score_player)

**Files read:**
- [x] `league_helper/add_to_roster_mode/AddToRosterModeManager.py` (lines 1-505)
- [x] `league_helper/util/player_scoring.py` (lines 1-532, 704-734)
- [x] `utils/FantasyPlayer.py` (lines 80-130)

**Evidence collected:**
- File paths cited: 5 key files
- Line numbers noted: 20+ specific locations
- Code snippets copied: 8 examples
- Method signatures documented: 5 methods

---

## Questions for Specification Phase

1. **Should we add unit tests for mode isolation?** Test that draft/optimizer/trade modes don't apply penalty?
   - Likely answer: Yes (prevents regression)

2. **Should we add integration tests?** Test full Add to Roster flow with penalty?
   - Likely answer: Yes (verify end-to-end behavior)

3. **Should we update scoring documentation?** docs/scoring/ folder has algorithm docs
   - Likely answer: Probably yes (keep docs in sync)

---

**Research Phase Complete - Ready for Specification Phase (S2.P2)**
