# S8.P2: Epic Testing Update - Real-World Examples

**Reference File:** Detailed examples of how to update epic_smoke_test_plan.md after feature completion

**Main Guide:** stages/s8/s8_p2_epic_testing_update.md

**When to use:** Reference these examples when updating testing plan in S8.P2

---


### Example 1: Adding Integration Point Test

**Just completed:** feature_01_adp_integration

**Implementation review reveals:**
```python
# File: league_helper/util/PlayerManager.py

def calculate_total_score(self, player: FantasyPlayer) -> float:
    """Calculate final player score with all multipliers."""

    # Start with projected points
    score = player.projected_points

    # Apply ADP multiplier (NEW in feature_01)
    adp_multiplier, adp_score = self.config.get_adp_multiplier(player.adp)
    player.adp_multiplier = adp_multiplier  # Store for display
    player.adp_score = adp_score  # Store for debugging
    score *= adp_multiplier  # Apply to final score

    return score
```

**Current test plan (from S4):**
```markdown
### Scenario 3: Scoring Calculation

**What to test:** Verify player scores calculated correctly

**How to test:**
- Load players
- Calculate scores
- Check scores are reasonable

**Expected result:** Players have scores
```

**S8.P2 (Epic Testing Update) updates:**

**Update existing scenario:**
```markdown
### Scenario 3: Scoring Calculation

**What to test:** Verify player scores calculated correctly

**How to test:**
1. Load players:
   ```
   python run_league_helper.py --mode draft
   ```markdown

2. Review recommendations output:
   - Open data/recommendations.csv
   - **[UPDATED S8.P2 (Epic Testing Update) - feature_01]:** Verify all players have adp_multiplier column
   - **[UPDATED S8.P2 (Epic Testing Update) - feature_01]:** Verify all players have adp_score column
   - **[UPDATED S8.P2 (Epic Testing Update) - feature_01]:** Verify final_score = projected_points * adp_multiplier

**Expected result:**
- Players have scores
- **[UPDATED S8.P2 (Epic Testing Update) - feature_01]:** All adp_multiplier values between 0.85-1.50
- **[UPDATED S8.P2 (Epic Testing Update) - feature_01]:** All adp_score values between 0-100
- **[UPDATED S8.P2 (Epic Testing Update) - feature_01]:** Math verifies: final_score = projected * multiplier
```

**Add new integration scenario:**
```markdown
### Scenario 9: PlayerManager → ConfigManager Integration

**Added:** S8.P2 (Epic Testing Update) (feature_01_adp_integration)

**What to test:** Verify PlayerManager correctly integrates with ConfigManager for ADP multipliers

**How to test:**
1. Create test player with known ADP:
   - Player: "Test Player"
   - Position: QB
   - Projected Points: 300.0
   - ADP: 10 (elite pick)

2. Run scoring calculation:
   ```
   python -c "
   from league_helper.util.PlayerManager import PlayerManager
   from league_helper.util.ConfigManager import ConfigManager
   from league_helper.util.FantasyPlayer import FantasyPlayer

   config = ConfigManager('data/')
   manager = PlayerManager(config)

   player = FantasyPlayer('Test Player', 'QB', projected_points=300.0, adp=10)
   score = manager.calculate_total_score(player)

   print(f'Final score: {score}')
   print(f'ADP multiplier: {player.adp_multiplier}')
   print(f'ADP score: {player.adp_score}')
   print(f'Math check: {300.0 * player.adp_multiplier}')
   "
   ```text

3. Verify integration:
   - ConfigManager.get_adp_multiplier() was called
   - Returned tuple was unpacked correctly
   - Multiplier was stored in player.adp_multiplier
   - Score was stored in player.adp_score
   - Final score = 300.0 * multiplier

**Expected result:**
- ADP multiplier ≈ 1.45 (elite pick gets high multiplier)
- ADP score ≈ 95 (elite rating)
- Final score ≈ 435.0 (300 * 1.45)
- Math check matches final score

**Why added:** Implementation revealed specific integration pattern (ConfigManager → tuple return → PlayerManager unpacks and stores). S4 plan didn't specify this interaction. Need explicit test to ensure it works correctly.
```

**Result:** Test plan now has specific, executable test for integration point discovered during implementation.

---

### Example 2: Adding Edge Case Test

**Just completed:** feature_01_adp_integration

**Implementation review reveals:**
```python
# File: league_helper/util/ConfigManager.py

def get_adp_multiplier(self, adp_value: float) -> Tuple[float, int]:
    """Calculate ADP multiplier."""

    # Handle missing ADP data
    if adp_value is None or adp_value == 0:
        self.logger.info(f"ADP value missing or zero, using neutral multiplier")
        return (1.0, 50)  # Neutral multiplier, mid-range score

    # Handle undrafted players (rank > 250)
    if adp_value > 250:
        adp_value = 250  # Cap at 250

    # Calculate multiplier...
```

**Current test plan (from S4):**
- No edge case scenarios for missing data or boundary conditions

**S8.P2 (Epic Testing Update) update - Add new scenario:**
```markdown
### Scenario 10: Edge Case - Missing ADP Data

**Added:** S8.P2 (Epic Testing Update) (feature_01_adp_integration)

**What to test:** Verify system handles players with missing ADP data gracefully

**How to test:**
1. Create test scenario:
   - Edit data/player_data/adp_data.csv
   - Remove entry for "P.Mahomes"
   - Ensure "P.Mahomes" exists in data/players.csv

2. Run draft mode:
   ```
   python run_league_helper.py --mode draft
   ```bash

3. Check output:
   - Open data/recommendations.csv
   - Find "P.Mahomes" row
   - Verify adp_multiplier = 1.0 (neutral)
   - Verify adp_score = 50 (mid-range)
   - Verify final_score = projected_points * 1.0 (no advantage/penalty)

4. Check logs:
   - Should have INFO log: "ADP value missing or zero, using neutral multiplier"
   - Should NOT have ERROR or WARNING

**Expected result:**
- "P.Mahomes" appears in recommendations (not excluded)
- adp_multiplier = 1.0 exactly
- adp_score = 50 exactly
- No crashes, exceptions, or errors
- Missing ADP doesn't advantage or penalize player

**Why added:** Implementation discovered fallback behavior for missing ADP data (returns neutral multiplier 1.0). This wasn't specified in original spec and needs explicit testing to ensure it works correctly. Important for data quality scenarios where ADP data is incomplete.
```

**Add another edge case scenario:**
```markdown
### Scenario 11: Edge Case - ADP Rank > 250

**Added:** S8.P2 (Epic Testing Update) (feature_01_adp_integration)

**What to test:** Verify system caps ADP ranks above 250 to prevent extreme penalties

**How to test:**
1. Create test scenario:
   - Edit data/player_data/adp_data.csv
   - Add test player: "Test Player,QB,TEST,500,500.0"
   - ADP rank 500 (very late pick)

2. Run draft mode:
   ```
   python run_league_helper.py --mode draft
   ```bash

3. Check output:
   - Open data/recommendations.csv
   - Find "Test Player" row
   - Verify adp_multiplier ≈ 0.85 (minimum, capped)
   - Verify adp_score ≈ 0 (lowest rating)
   - Compare to player with ADP rank 250 (should have same multiplier)

**Expected result:**
- ADP rank 500 gets same multiplier as rank 250 (both capped at 0.85)
- No extreme penalties for very late picks
- Multiplier doesn't go below 0.85

**Why added:** Implementation discovered capping behavior for ADP > 250. Prevents extreme penalties for late-round picks. Need test to verify cap is applied correctly and consistently.
```

**Result:** Test plan now covers edge cases discovered during implementation that weren't anticipated in S4.

---

### Example 3: Updating Success Criteria

**Just completed:** feature_01_adp_integration

**Implementation reveals:** System must handle missing data gracefully (wasn't in original epic success criteria)

**Original Epic Success Criteria (from S1):**
```markdown
## Epic Success Criteria
