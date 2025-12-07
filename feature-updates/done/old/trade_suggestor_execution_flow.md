# Trade Suggestor - Complete Execution Flow

This document walks through the complete execution flow of the Trade Suggestor, including waiver recommendations and drop system logic.

---

## Phase 1: Initialization & Setup

### Entry Point: `start_trade_suggestor()` (Line 225)

**Called by**: User selecting Trade Suggestor from menu in `run_league_helper.py`

**Initial Checks** (Lines 234-268):
1. **Verify opponent teams exist** (Line 234-236)
   - If no opponents: Return early

2. **Check roster size violations** (Lines 238-261)
   - Check if any team (user or opponents) exceeds `MAX_PLAYERS` (15)
   - Log warnings for teams over limit
   - **Important**: Trades will still be generated, but drop system will handle violations

3. **Log analysis start** (Lines 263-268)
   ```python
   self.logger.info("BEGINNING TRADE ANALYSIS")
   self.logger.info(f"My Team: {self.my_team.name} (Score: {self.my_team.team_score:.2f})")
   self.logger.info(f"Opponent Teams: {len(self.opponent_simulated_teams)}")
   ```

---

## Phase 2: Trade Generation Loop

### For Each Opponent Team (Lines 275-327)

**Step 1: Calculate Expected Combinations** (Lines 279-304)
```python
my_unlocked = len([p for p in self.my_team.team if p.locked != 1])
their_unlocked = len([p for p in opponent_team.team if p.locked != 1])

# Calculate combinations for each enabled trade type
one_for_one_combos = my_unlocked * their_unlocked if ENABLE_ONE_FOR_ONE else 0
two_for_two_combos = (my_unlocked * (my_unlocked - 1) // 2) * (their_unlocked * (their_unlocked - 1) // 2) if ENABLE_TWO_FOR_TWO else 0
two_for_one_combos = (my_unlocked * (my_unlocked - 1) // 2) * their_unlocked if ENABLE_TWO_FOR_ONE else 0
one_for_two_combos = my_unlocked * (their_unlocked * (their_unlocked - 1) // 2) if ENABLE_ONE_FOR_TWO else 0
# ... etc for 3:1, 1:3, 3:2, 2:3
```

**Why**: Shows user how many combinations will be evaluated. Formula is combinatorics: C(n, k) = n! / (k! * (n-k)!)

**Step 2: Call `get_trade_combinations()`** (Lines 309-323)
```python
trade_combos = self.get_trade_combinations(
    my_team=self.my_team,
    their_team=opponent_team,
    is_waivers=False,
    one_for_one=ENABLE_ONE_FOR_ONE,
    two_for_two=ENABLE_TWO_FOR_TWO,
    three_for_three=ENABLE_THREE_FOR_THREE,
    two_for_one=ENABLE_TWO_FOR_ONE,
    one_for_two=ENABLE_ONE_FOR_TWO,
    three_for_one=ENABLE_THREE_FOR_ONE,
    one_for_three=ENABLE_ONE_FOR_THREE,
    three_for_two=ENABLE_THREE_FOR_TWO,
    two_for_three=ENABLE_TWO_FOR_THREE,
    ignore_max_positions=True
)
```

**Parameters**:
- `is_waivers=False`: This is a trade (not waiver optimization mode)
- `ignore_max_positions=True`: Allow opponent rosters to violate position limits (we'll handle with drop system)
- Boolean flags control which trade types to generate

---

## Phase 3: Trade Combination Generation

### Inside `get_trade_combinations()` (Line 1040)

**Step 1: Filter Unlocked Players** (Lines 1043-1049)
```python
my_unlocked_players = [p for p in my_team.team if p.locked != 1]
their_unlocked_players = [p for p in their_team.team if p.locked != 1]
my_locked = [p for p in my_team.team if p.locked == 1]
their_locked = [p for p in their_team.team if p.locked == 1]
```

**Why**: Only unlocked players can be traded. Locked players stay on roster for scoring.

**Step 2: Early Exit Checks** (Lines 1051-1073)
```python
if not my_unlocked_players or (not their_unlocked_players and not is_waivers):
    self.logger.warning("No unlocked players available for trades")
    return []
```

**Why**: Can't generate trades without tradeable players.

---

## Phase 4: Unequal Trade Type Processing (Example: 1:2 Trade)

Let's trace through a **1:2 trade** (User gives 1 player, gets 2 players) in detail.

### Entry Point: Line 1529 - "if one_for_two:"

**Step 1: Generate Player Combinations** (Lines 1531-1533)
```python
# Generate all 1-for-2 trades (I give 1, opponent gives 2)
for my_player in my_unlocked_players:
    for their_players in itertools.combinations(their_unlocked_players, 2):
```

**Math**: If I have 5 unlocked players and opponent has 5:
- My combinations: 5 choices
- Their combinations: C(5,2) = 10 choices
- Total: 5 × 10 = 50 trade combinations to evaluate

**Step 2: Calculate Roster Changes** (Lines 1534-1541)
```python
their_player1, their_player2 = their_players

# Calculate new rosters
my_new_roster = [p for p in my_unlocked_players if p != my_player]
my_new_roster.extend([their_player1, their_player2])

their_new_roster = [p for p in their_unlocked_players
                    if p != their_player1 and p != their_player2]
their_new_roster.append(my_player)
```

**What happens**:
- **My roster**: Remove 1 player, add 2 players → Net +1 player
- **Their roster**: Remove 2 players, add 1 player → Net -1 player

---

## Phase 5: Waiver Recommendation Calculation

### Determining Who Needs Waivers (Lines 1544-1547)

```python
# Calculate waiver recommendations for both teams BEFORE roster validation
# 1-for-2: I give 1, get 2 = net +1 (no waiver), they give 2, get 1 = net -1 (they need waiver)
my_waiver_recs = []  # I gain a roster spot, no waiver needed
their_waiver_recs = self._get_waiver_recommendations(num_spots=1) if not is_waivers else []
```

**Logic**:
- **User**: Net +1 player = roster GAINS a spot = NO waiver needed
- **Opponent**: Net -1 player = roster LOSES a spot = 1 waiver needed

**Why call `_get_waiver_recommendations()` now (before validation)**:
- Waivers need to be added to roster BEFORE creating TradeSimTeam
- TradeSimTeam calculates team_score including all players
- This ensures waiver players are factored into the trade assessment

---

## Phase 6: Inside `_get_waiver_recommendations()` (Line 905)

This method finds the best available waiver wire players.

### Step 1: Validate Input (Lines 924-926)
```python
if num_spots <= 0:
    self.logger.debug(f"No waiver recommendations needed (num_spots={num_spots})")
    return []
```

### Step 2: Get Available Players (Lines 928-934)
```python
# Get available players (drafted=0, unlocked)
# Note: Don't use can_draft=True filter here because it checks against current roster state,
# but we're generating recommendations for POST-TRADE roster with open spots
available_players = self.player_manager.get_player_list(
    drafted_vals=[0],
    unlocked_only=True
)
```

**CRITICAL FIX**:
- **OLD CODE**: Used `can_draft=True` which called `FantasyTeam.can_draft(player)`
- **PROBLEM**: `can_draft()` checks if player can be added to CURRENT roster (15/15 full)
- **RESULT**: Always returned empty list because roster was full
- **NEW CODE**: Removed `can_draft=True` filter
- **WHY**: We're recommending for POST-TRADE roster which will have open spots

### Step 3: Score Available Players (Lines 940-951)
```python
scored_players: List[ScoredPlayer] = []
for p in available_players:
    # Use current week for matchup scoring
    scored_player = self.player_manager.score_player(
        p,
        adp=False,
        player_rating=True,
        team_quality=True,
        performance=True,
        matchup=False
    )
    scored_players.append(scored_player)
```

**Scoring Weights Used**:
- `adp=False`: Don't use ADP (draft context, not relevant for waivers)
- `player_rating=True`: Use expert consensus ratings
- `team_quality=True`: Use offensive/defensive team strength
- `performance=True`: Use fantasy points projection
- `matchup=False`: Don't use opponent matchup (would need current week)

### Step 4: Rank and Return Top N (Lines 953-960)
```python
# Sort by score descending
ranked_players = sorted(scored_players, key=lambda x: x.score, reverse=True)

# Return top num_spots (or fewer if not enough available)
result_count = min(num_spots, len(ranked_players))
self.logger.info(f"Generated {result_count} waiver recommendations (requested: {num_spots})")

return ranked_players[:result_count]
```

**Result**: Returns list of top N ScoredPlayer objects, sorted by score

---

## Phase 7: Add Waivers to Rosters (Back in 1:2 Trade Logic)

### Lines 1549-1551
```python
# Add waiver players to rosters for scoring
my_new_roster_with_waivers = my_new_roster  # No waivers for me
their_new_roster_with_waivers = their_new_roster + [rec.player for rec in their_waiver_recs]
```

**Key Point**: Waivers added BEFORE validation and scoring

**Roster States Now**:
- **User**: (Original 15 players) - 1 traded + 2 received = 16 players (VIOLATION)
- **Opponent**: (Original 15 players) - 2 traded + 1 received + 1 waiver = 15 players (LEGAL)

---

## Phase 8: Roster Validation

### Lines 1553-1569
```python
# Validate rosters
my_roster_valid = self._validate_roster(
    my_new_roster_with_waivers + my_locked,
    ignore_max_positions=False
)

their_roster_valid = self._validate_roster(
    their_new_roster_with_waivers + their_locked,
    ignore_max_positions=ignore_max_positions
)
```

**Validation Rules** (from `_validate_roster()` method, line 1002):
1. **Total players**: Must be ≤ MAX_PLAYERS (15)
2. **Position limits**: Each position must be ≤ MAX_POSITIONS (QB:2, RB:4, WR:4, TE:2, K:1, DST:1)
3. **FLEX eligibility**: Excess RB/WR/DST can go to FLEX slot

**Expected Results for 1:2 Trade**:
- **User**: `my_roster_valid = False` (16 players > 15 limit)
- **Opponent**: `their_roster_valid = True` (15 players, legal)

---

## Phase 9: Drop System (When Validation Fails)

### Lines 1572-1661 - User Drop System for 1:2 Trades

Since `my_roster_valid = False`, we enter the drop system:

### Step 1: Get Drop Candidates (Lines 1574-1579)
```python
# 1:2 trade: User gets net +1, so need to drop 1 additional player
drop_candidates = self._get_lowest_scored_players_per_position(
    my_team,
    exclude_players=[my_player],
    num_per_position=2
)
```

**Inside `_get_lowest_scored_players_per_position()`** (Line 962):

```python
def _get_lowest_scored_players_per_position(self, team: TradeSimTeam,
                                            exclude_players: List[FantasyPlayer],
                                            num_per_position: int = 2) -> List[FantasyPlayer]:
    droppable_players = []

    # Group players by position, excluding locked and traded players
    position_groups: Dict[str, List[FantasyPlayer]] = {
        pos: [] for pos in Constants.MAX_POSITIONS.keys()
    }

    for player in team.team:
        if player in exclude_players or player.locked:
            continue
        if player.position in position_groups:
            position_groups[player.position].append(player)

    # For each position, get the lowest-scored players
    for players in position_groups.values():
        if not players:
            continue
        sorted_players = sorted(players, key=lambda p: p.score)
        droppable_players.extend(sorted_players[:num_per_position])

    return droppable_players
```

**What it does**:
1. Exclude players being traded away (`exclude_players=[my_player]`)
2. Exclude locked players
3. Group remaining players by position (QB, RB, WR, TE, K, DST)
4. For each position, sort by score ascending
5. Take lowest 2 scorers from each position
6. Return combined list of drop candidates

**Example Result**:
- Might return: [Lowest QB, 2nd Lowest QB, Lowest RB, 2nd Lowest RB, Lowest WR, 2nd Lowest WR, ...]
- Typically 10-12 drop candidates total (2 per position × 6 positions)

### Step 2: Try Each Drop Combination (Lines 1581-1661)

```python
# Try dropping each candidate
for drop_player in drop_candidates:
    # Create roster with drop
    my_roster_with_drop = [p for p in my_new_roster if p != drop_player]
    my_full_roster_with_drop = my_roster_with_drop + my_locked

    # Validate with drop
    if not self._validate_roster(my_full_roster_with_drop, ignore_max_positions=False):
        continue

    # ... validation and scoring ...
```

**For each drop candidate**:

#### 2a. Create Roster With Drop (Lines 1582-1584)
```python
my_roster_with_drop = [p for p in my_new_roster if p != drop_player]
my_full_roster_with_drop = my_roster_with_drop + my_locked
```

**Math**: (15 original) - 1 traded + 2 received - 1 dropped = 15 players

#### 2b. Validate New Roster (Lines 1586-1588)
```python
if not self._validate_roster(my_full_roster_with_drop, ignore_max_positions=False):
    continue
```

**Why might fail**:
- Dropping lowest-scoring QB might leave only 0 QBs (violates minimum)
- Skip this drop candidate if invalid

#### 2c. Validate Opponent Roster (Lines 1590-1604)
```python
# Also ensure opponent's roster is valid (with waivers)
if not their_roster_valid:
    # Their roster is ALSO invalid, skip this combination
    # (This shouldn't happen for 1:2 trades, but check anyway)
    continue
```

**For 1:2 trades**: Opponent roster should always be valid (they're net -1, filled with waiver)

#### 2d. Create TradeSimTeam Objects With Drops (Lines 1606-1617)
```python
# Create teams with drop included
my_new_team_with_drop = TradeSimTeam(
    my_team.name,
    my_roster_with_drop,
    self.player_manager,
    isOpponent=False
)

their_new_team = TradeSimTeam(
    their_team.name,
    their_new_roster_with_waivers,
    self.player_manager,
    isOpponent=True
)
```

**What TradeSimTeam does** (from TradeSimTeam.py):
1. Filters out OUT/IR injured players (keeps QUESTIONABLE/DOUBTFUL)
2. Calls `score_team()` method
3. Calculates `team_score` = sum of all player scores

**Important**:
- User team includes the DROP (not just trade)
- Opponent team includes their WAIVER pickup
- Both teams scored with their final rosters

#### 2e. Check Improvement Against ORIGINAL Score (Lines 1619-1621)
```python
# Check improvement against ORIGINAL team score
our_roster_improved = (my_new_team_with_drop.team_score - my_team.team_score) >= Constants.MIN_TRADE_IMPROVEMENT
their_roster_improved = (their_new_team.team_score - their_team.team_score) >= Constants.MIN_TRADE_IMPROVEMENT
```

**CRITICAL COMPARISON**:
- **User**: `(new_score_with_drop) - (original_score)` ≥ 30 points
- **Opponent**: `(new_score_with_waiver) - (original_score)` ≥ 30 points

**Why compare against ORIGINAL**:
- User's original score already includes the player being traded AND the player being dropped
- We're asking: "Is it worth trading Player A + dropping Player B to get Players X and Y?"
- Alternative would compare against hypothetical legal trade, but that's not the user's actual starting point

#### 2f. Create TradeSnapshot If Mutually Beneficial (Lines 1623-1661)
```python
if our_roster_improved and their_roster_improved:
    # Get ScoredPlayer objects for display
    my_new_scored = my_team.get_scored_players([their_player1, their_player2])
    my_original_scored = my_team.get_scored_players([my_player])

    their_new_scored = their_team.get_scored_players([my_player])
    their_original_scored = their_team.get_scored_players([their_player1, their_player2])

    my_dropped_scored = my_team.get_scored_players([drop_player])

    # Create TradeSnapshot with drop information
    snapshot = TradeSnapshot(
        my_new_team=my_new_team_with_drop,
        my_new_players=my_new_scored,
        their_new_team=their_new_team,
        their_new_players=their_new_scored,
        my_original_players=my_original_scored,
        waiver_recommendations=[],  # User doesn't need waivers
        their_waiver_recommendations=their_waiver_recs,
        my_dropped_players=my_dropped_scored,
        their_dropped_players=[]  # Opponent doesn't need drops
    )
    trade_combos.append(snapshot)
```

**TradeSnapshot stores**:
- Both teams' new rosters (with waivers/drops applied)
- Players involved in trade
- Waiver recommendations
- Dropped players
- Team scores (for sorting later)

---

## Phase 10: Handle Successful Validation (No Drops Needed)

### Lines 1484-1527 - Normal 1:2 Trade Path

If `my_roster_valid = True` (rare for 1:2, but possible if starting roster < 15):

```python
# Both rosters are valid, proceed with trade assessment
my_new_team = TradeSimTeam(my_team.name, my_new_roster_with_waivers, self.player_manager, isOpponent=False)
their_new_team = TradeSimTeam(their_team.name, their_new_roster_with_waivers, self.player_manager, isOpponent=True)

# Check improvements
our_roster_improved = (my_new_team.team_score - my_team.team_score) >= Constants.MIN_TRADE_IMPROVEMENT
their_roster_improved = (their_new_team.team_score - their_team.team_score) >= Constants.MIN_TRADE_IMPROVEMENT

if our_roster_improved and their_roster_improved:
    # Create TradeSnapshot without drops
    snapshot = TradeSnapshot(
        my_new_team=my_new_team,
        my_new_players=my_new_scored,
        their_new_team=their_new_team,
        their_new_players=their_new_scored,
        my_original_players=my_original_scored,
        waiver_recommendations=[],
        their_waiver_recommendations=their_waiver_recs,
        my_dropped_players=[],  # No drops needed
        their_dropped_players=[]
    )
    trade_combos.append(snapshot)
```

**Difference from drop path**:
- No `my_dropped_players`
- Roster valid without dropping anyone

---

## Phase 11: 2:1 Trade Logic (Opponent Drop System)

For completeness, let's also cover **2:1 trades** (User gives 2, gets 1) where OPPONENT needs drops.

### Entry Point: Line 1386 - "if two_for_one:"

### Waiver Calculation (Lines 1417-1419)
```python
# 2-for-1: I give 2, get 1 = net -1 (I need waiver), they get 2, give 1 = net +1 (no waiver)
my_waiver_recs = self._get_waiver_recommendations(num_spots=1)
their_waiver_recs = []  # They gain a roster spot, no waiver needed
```

**Logic**:
- **User**: Net -1 player = 1 waiver needed
- **Opponent**: Net +1 player = NO waiver needed

### Opponent Drop System (Lines 1427-1478)
```python
# If opponent validation fails, try drop variations
if not their_roster_valid:
    # 2:1 trade: Opponent gets net +1, so need to drop 1 additional player
    drop_candidates = self._get_lowest_scored_players_per_position(
        their_team,
        exclude_players=[their_player],
        num_per_position=2
    )

    for drop_player in drop_candidates:
        their_roster_with_drop = [p for p in their_new_roster_with_waivers if p != drop_player]
        their_full_roster_with_drop = their_roster_with_drop + their_locked

        # Validate
        if not self._validate_roster(their_full_roster_with_drop, ignore_max_positions=ignore_max_positions):
            continue

        # Create teams
        my_new_team = TradeSimTeam(my_team.name, my_new_roster_with_waivers, self.player_manager, isOpponent=False)
        their_new_team_with_drop = TradeSimTeam(their_team.name, their_roster_with_drop, self.player_manager, isOpponent=True)

        # Check improvement against ORIGINAL
        our_roster_improved = (my_new_team.team_score - my_team.team_score) >= Constants.MIN_TRADE_IMPROVEMENT
        their_roster_improved = (their_new_team_with_drop.team_score - their_team.team_score) >= Constants.MIN_TRADE_IMPROVEMENT

        if our_roster_improved and their_roster_improved:
            their_dropped_scored = their_team.get_scored_players([drop_player])

            snapshot = TradeSnapshot(
                my_new_team=my_new_team,
                my_new_players=my_new_scored,
                their_new_team=their_new_team_with_drop,
                their_new_players=their_new_scored,
                my_original_players=my_original_scored,
                waiver_recommendations=my_waiver_recs,
                their_waiver_recommendations=[],
                my_dropped_players=[],
                their_dropped_players=their_dropped_scored
            )
            trade_combos.append(snapshot)
```

**Key Difference**:
- Opponent's team gets scored with DROP
- User's team gets scored with WAIVER
- Both compared against ORIGINAL team scores

---

## Phase 12: Return to Trade Suggestor

### Back in `start_trade_suggestor()` - Line 326

After `get_trade_combinations()` returns:

```python
elapsed = time.time() - start_time
all_trades.extend(trade_combos)
self.logger.info(f"Found {len(trade_combos)} valid trades with {opponent_team.name} in {elapsed:.2f}s")
```

**Step 1: Collect All Trades** (Line 326)
- Aggregate trades from all opponents into `all_trades` list

### Check If Any Trades Found (Lines 331-333)
```python
if not all_trades:
    print("\nNo mutually beneficial trades found.")
    return (True, [])
```

### Sort Trades By User Improvement (Lines 336-340)
```python
sorted_trades = sorted(
    all_trades,
    key=lambda t: (t.my_new_team.team_score - self.my_team.team_score),
    reverse=True
)
```

**Why sort by user improvement**: User wants to see best trades for THEM first

---

## Phase 13: Display Trades

### Display Top Trades (Lines 342-398)

```python
print("\n" + "="*80)
print("TRADE SUGGESTOR - Top Trade Opportunities")
print("="*80)

max_display = Constants.MAX_TRADES_TO_DISPLAY
for idx, trade in enumerate(sorted_trades[:max_display], 1):
    print(f"\n#{idx} - Trade with {trade.their_new_team.name}")

    # Calculate improvements
    my_improvement = trade.my_new_team.team_score - self.my_team.team_score
    their_improvement = trade.their_new_team.team_score - trade.their_new_team.team_score

    print(f"  My improvement: +{my_improvement:.2f} pts")
    print(f"  Their improvement: +{their_improvement:.2f} pts")

    # Display players I give
    print(f"  I give:")
    for player in trade.my_original_players:
        print(f"    - {player}")

    # Display players I receive
    print(f"  I receive:")
    for player in trade.my_new_players:
        print(f"    - {player}")

    # Display waiver recommendations for user
    if trade.waiver_recommendations:
        print(f"  Recommended waiver wire adds to fill spots:")
        for player in trade.waiver_recommendations:
            print(f"    - {player}")

    # Display opponent waiver recommendations
    if trade.their_waiver_recommendations:
        print(f"  Opponent waiver wire adds to fill spots:")
        for player in trade.their_waiver_recommendations:
            print(f"    - {player}")

    # Display dropped players (beyond the trade itself)
    if trade.my_dropped_players:
        print(f"  Players I Must Drop (to make room):")
        for player in trade.my_dropped_players:
            print(f"    - {player}")

    # Display opponent dropped players
    if trade.their_dropped_players:
        print(f"  Players {trade.their_new_team.name} Must Drop (to make room):")
        for player in trade.their_dropped_players:
            print(f"    - {player}")
```

**Output Format Example**:
```
#1 - Trade with Team Opponent

  My improvement: +45.50 pts
  Their improvement: +32.75 pts

  I give:
    - [RB] [MIA] Player A - 85.50 pts

  I receive:
    - [WR] [BUF] Player X - 95.25 pts
    - [WR] [KC] Player Y - 88.75 pts

  Players I Must Drop (to make room):
    - [TE] [NYJ] Player B - 45.00 pts

  Opponent waiver wire adds to fill spots:
    - [RB] [DAL] Player Z - 72.00 pts
```

---

## Phase 14: Save Trades to File

### Lines 400-430 - User Prompt

```python
print(f"\nTotal trades found: {len(sorted_trades)}")
print(f"(Showing top {min(max_display, len(sorted_trades))})")

user_input = input("\nSave trades to file? (y/n): ").strip().lower()

if user_input == 'y':
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = self.output_folder / f"trade_info_{timestamp}.txt"
    self._write_trades_to_file(sorted_trades, filename)
```

### Inside `_write_trades_to_file()` (Line 2196)

**Same format as console output**, written to file:

```python
def _write_trades_to_file(self, trades: List[TradeSnapshot], filepath: Path):
    with open(str(filepath), 'w') as file:
        file.write("="*80 + "\n")
        file.write("TRADE SUGGESTOR - Trade Opportunities\n")
        file.write("="*80 + "\n\n")

        for idx, trade in enumerate(trades, 1):
            # ... same display logic as console ...
            file.write(f"\n#{idx} - Trade with {trade.their_new_team.name}\n")
            # ... write all trade details ...
```

**File saved to**: `league_helper/trade_simulator_mode/trade_outputs/trade_info_{timestamp}.txt`

---

## Summary: Complete Data Flow

### For 1:2 Trade (User gives 1, gets 2):

```
START: User roster = 15 players, Opponent roster = 15 players

1. Generate Combinations
   → 5 my players × C(5,2)=10 opponent pairs = 50 combinations

2. For Each Combination:
   a. Calculate Rosters:
      - My new: 15 - 1 + 2 = 16 players (INVALID)
      - Their new: 15 - 2 + 1 = 14 players (MISSING SPOT)

   b. Determine Waivers:
      - My waiver: 0 (gaining roster spot)
      - Their waiver: 1 (losing roster spot)

   c. Get Waiver Recommendations:
      → _get_waiver_recommendations(1)
      → Returns: [Top Waiver Player]

   d. Add Waivers to Rosters:
      - My roster: 16 players (INVALID)
      - Their roster: 14 + 1 waiver = 15 players (VALID)

   e. Validate Rosters:
      - My: INVALID (16 > 15)
      - Their: VALID (15 = 15)

   f. Enter Drop System:
      → Get lowest 2 scorers per position from my team
      → Try dropping each candidate

      For each drop candidate:
        - My roster: 16 - 1 drop = 15 players
        - Validate: VALID
        - Score both teams
        - Compare: my_new_score vs my_original_score
        - Compare: their_new_score vs their_original_score
        - If both ≥ +30 pts: Create TradeSnapshot

   g. Store TradeSnapshot:
      - my_new_team (with drop)
      - their_new_team (with waiver)
      - my_dropped_players = [dropped player]
      - their_waiver_recommendations = [waiver player]

3. Return all valid TradeSnapshots

4. Sort by user improvement

5. Display and save to file

END: User sees best trades with drops/waivers clearly labeled
```

---

## Key Design Decisions

### 1. **Why Add Waivers BEFORE Validation?**
- TradeSimTeam calculates team_score including all players
- Waivers must be in roster to be scored
- Alternative (score separately then add) would be more complex

### 2. **Why Compare Against ORIGINAL Score?**
- User's starting point is their current 15-player roster
- Trade asks: "Is it worth changing current roster to new configuration?"
- Comparing to hypothetical legal trade would be artificial baseline

### 3. **Why Only Top 2 Lowest Scorers Per Position?**
- Prevents combinatorial explosion (6 positions × 2 = 12 candidates)
- Dropping high-scoring players makes no sense for improving team
- 12 candidates is manageable to evaluate

### 4. **Why Separate User/Opponent Drop Systems?**
- Same logic, different teams
- User drop system: Lines 1572-1661
- Opponent drop system: Lines 1427-1478
- Could be refactored to shared method, but kept separate for clarity

### 5. **Why `ignore_max_positions=True` for Opponents?**
- Real-world: Opponent rosters may have imported incorrectly
- Don't want to skip valid trades due to opponent data issues
- Drop system will fix violations anyway

---

## Constants Reference

### Trade Type Flags (Lines 22-36)
```python
ENABLE_ONE_FOR_ONE = False      # 1:1 trades
ENABLE_TWO_FOR_TWO = False      # 2:2 trades
ENABLE_THREE_FOR_THREE = False  # 3:3 trades (waivers only)
ENABLE_TWO_FOR_ONE = True       # Give 2, get 1
ENABLE_ONE_FOR_TWO = True       # Give 1, get 2
ENABLE_THREE_FOR_ONE = False    # Give 3, get 1
ENABLE_ONE_FOR_THREE = False    # Give 1, get 3
ENABLE_THREE_FOR_TWO = False    # Give 3, get 2
ENABLE_TWO_FOR_THREE = False    # Give 2, get 3
```

### From constants.py
```python
MAX_PLAYERS = 15
MIN_TRADE_IMPROVEMENT = 30  # Minimum point improvement to suggest trade
MAX_TRADES_TO_DISPLAY = 10  # Show top 10 trades

MAX_POSITIONS = {
    'QB': 2,
    'RB': 4,
    'WR': 4,
    'TE': 2,
    'K': 1,
    'DST': 1,
    'FLEX': 1
}
```

---

## Edge Cases Handled

### 1. No Waiver Players Available
```python
if not available_players:
    self.logger.warning("No waiver wire players available for recommendations")
    return []
```
- Returns empty list
- Trade still evaluated without waivers
- Likely fails MIN_TRADE_IMPROVEMENT threshold

### 2. Insufficient Drop Candidates
- Drop system tries all candidates
- If none result in valid + improved roster: No TradeSnapshot created
- Trade combination is skipped

### 3. Both Teams Need Drops
- Currently: Each trade type handles one team at a time
- Future enhancement: Could try drop combinations for BOTH teams
- Current approach: Skip if other team also invalid

### 4. Locked Players
- Excluded from trade combinations
- Included in roster for validation and scoring
- Never appear in drop candidates

### 5. Injured Players (OUT/IR)
- Filtered out by TradeSimTeam during scoring
- Not included in team_score calculation
- Still count toward MAX_PLAYERS limit

---

## Conclusion

The Trade Suggestor implements a comprehensive system that:

1. ✅ Generates all possible trade combinations (based on enabled flags)
2. ✅ Calculates waiver recommendations for team losing roster spots
3. ✅ Validates rosters including waivers
4. ✅ Tries drop combinations when roster limits violated
5. ✅ Scores teams with waivers and drops included
6. ✅ Compares against original team scores
7. ✅ Only suggests mutually beneficial trades (both teams improve ≥30 pts)
8. ✅ Displays waivers and drops clearly in output
9. ✅ Saves results to timestamped file

The system ensures all trades are legal, beneficial, and actionable for the user.
