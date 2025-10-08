# DRAFT_ORDER System Design

**Purpose:** Implement round-based bonus system using DRAFT_ORDER configuration with static point values

**Date:** 2025-09-29
**Status:** DESIGN PHASE

---

## Overview

The DRAFT_ORDER system provides round-specific bonuses to players whose positions match the draft strategy for that round. This replaces the current positional need calculation (which is being completely removed).

**Key Concepts:**
1. **Round-based bonuses** - Different bonus values per round
2. **Static point values** - No multipliers, direct point additions
3. **Position prioritization** - Primary and secondary positions per round
4. **Roster tracking** - Assign existing roster players to rounds
5. **Current round detection** - First unfilled round determines bonuses

---

## Updated DRAFT_ORDER Configuration

### New Structure (Static Point Values)

```python
DRAFT_ORDER = [
    {FLEX: 50, QB: 25},    # Round 1: FLEX priority (50 pts), QB secondary (25 pts)
    {FLEX: 50, QB: 25},    # Round 2: Same priorities
    {FLEX: 50, QB: 30},    # Round 3: QB priority increasing
    {FLEX: 50, QB: 30},    # Round 4: QB priority increasing
    {QB: 50, FLEX: 25},    # Round 5: QB now primary, FLEX secondary
    {TE: 50, FLEX: 25},    # Round 6: TE primary, FLEX secondary
    {FLEX: 50},            # Round 7: FLEX only
    {QB: 50, FLEX: 25},    # Round 8: QB primary again
    {TE: 50, FLEX: 25},    # Round 9: TE primary
    {FLEX: 50},            # Round 10: FLEX only
    {FLEX: 50},            # Round 11: FLEX only
    {K: 50},               # Round 12: Kicker
    {DST: 50},             # Round 13: Defense
    {FLEX: 50},            # Round 14: FLEX
    {FLEX: 50}             # Round 15: FLEX
]
```

### Position Priority Values

**Primary Position:** 50 points (configurable via simulation)
**Secondary Position:** 25 points (configurable via simulation)
**Tertiary Position (if needed):** 15 points (future expansion)

### Configuration Constants

```python
# draft_helper/draft_helper_config.py
DRAFT_ORDER_PRIMARY_BONUS = 50    # Points for #1 priority position
DRAFT_ORDER_SECONDARY_BONUS = 25  # Points for #2 priority position

# draft_helper/simulation/config.py
PARAMETER_RANGES = {
    'DRAFT_ORDER_PRIMARY_BONUS': [40, 50, 60],      # Test primary bonus range
    'DRAFT_ORDER_SECONDARY_BONUS': [20, 25, 30],    # Test secondary bonus range
}
```

---

## Bonus Calculation Algorithm

### Step 1: Determine Current Round

```python
def get_current_draft_round(roster: List[FantasyPlayer]) -> int:
    """
    Determine the current draft round based on roster size.

    Args:
        roster: List of current roster players

    Returns:
        int: Current round number (0-indexed for DRAFT_ORDER access)
    """
    roster_size = len(roster)

    # Current round is the next slot to fill
    # Example: 4 players drafted = round 5 (index 4)
    current_round_index = roster_size

    if current_round_index >= len(DRAFT_ORDER):
        return None  # Draft complete

    return current_round_index
```

### Step 2: Get Round Priorities

```python
def get_round_priorities(round_index: int) -> Dict[str, int]:
    """
    Get position priorities for a specific round.

    Args:
        round_index: Zero-indexed round number

    Returns:
        dict: Position -> bonus points mapping
    """
    if round_index is None or round_index >= len(DRAFT_ORDER):
        return {}  # No priorities (draft complete)

    return DRAFT_ORDER[round_index]
```

### Step 3: Calculate Player Bonus

```python
def calculate_draft_order_bonus(
    player: FantasyPlayer,
    current_round_index: int
) -> float:
    """
    Calculate DRAFT_ORDER bonus for a player based on current round.

    Args:
        player: Player to calculate bonus for
        current_round_index: Current draft round (0-indexed)

    Returns:
        float: Bonus points to add to player's score
    """
    # Get priorities for current round
    round_priorities = get_round_priorities(current_round_index)

    if not round_priorities:
        return 0.0  # No bonus (draft complete)

    player_position = player.position

    # Check direct position match
    if player_position in round_priorities:
        bonus = round_priorities[player_position]
        logger.debug(f"DRAFT_ORDER bonus for {player.name} ({player_position}): +{bonus} pts (Round {current_round_index + 1})")
        return bonus

    # Check FLEX eligibility
    if player_position in FLEX_ELIGIBLE_POSITIONS and FLEX in round_priorities:
        bonus = round_priorities[FLEX]
        logger.debug(f"DRAFT_ORDER bonus for {player.name} ({player_position}→FLEX): +{bonus} pts (Round {current_round_index + 1})")
        return bonus

    # No match - no bonus
    logger.debug(f"No DRAFT_ORDER bonus for {player.name} ({player_position}) in Round {current_round_index + 1}")
    return 0.0
```

---

## Round Tracking System

### Purpose

When the system starts, it needs to:
1. Assign existing roster players to rounds
2. Determine which round is "current" for new picks

This is **display and tracking only** - doesn't affect scoring of available players.

### Assignment Algorithm

```python
def assign_players_to_rounds(roster: List[FantasyPlayer]) -> Dict[int, FantasyPlayer]:
    """
    Assign existing roster players to draft rounds based on position fit.

    Args:
        roster: List of current roster players

    Returns:
        dict: Mapping of round_number (1-15) -> FantasyPlayer
    """
    round_assignments = {}  # round_number -> player

    # Create list of unassigned players
    unassigned_players = roster.copy()

    # Loop through each round and find best fit
    for round_num in range(1, MAX_PLAYERS + 1):
        if not unassigned_players:
            break  # All players assigned

        round_index = round_num - 1
        round_priorities = DRAFT_ORDER[round_index]

        if not round_priorities:
            continue  # Skip empty rounds

        # Find highest priority position for this round
        highest_priority_position = max(round_priorities, key=round_priorities.get)

        # Find first player matching this position
        for player in unassigned_players:
            position_matches = (
                player.position == highest_priority_position or
                (player.position in FLEX_ELIGIBLE_POSITIONS and highest_priority_position == FLEX)
            )

            if position_matches:
                # Assign this player to this round
                round_assignments[round_num] = player
                unassigned_players.remove(player)
                break

    return round_assignments
```

### Important Note from User Clarifications

**User:** "It doesn't matter. It doesn't matter which player is slotted into Round 1 or 3 for example, all that matters is that there are enough positions already rostered to fill those slots."

**Implication:**
- Don't worry about which specific RB goes to which round
- Just ensure position counts match DRAFT_ORDER expectations
- The algorithm above is sufficient (first-fit strategy)

### Validation Check

```python
def validate_roster_matches_draft_order(roster: List[FantasyPlayer]) -> bool:
    """
    Verify that roster composition aligns with DRAFT_ORDER position expectations.

    This is a critical invariant - the system should NEVER allow a roster
    that violates DRAFT_ORDER position requirements.

    Args:
        roster: Current roster players

    Returns:
        bool: True if roster matches DRAFT_ORDER, False otherwise
    """
    # Count positions in roster
    position_counts = {}
    for player in roster:
        pos = player.position
        position_counts[pos] = position_counts.get(pos, 0) + 1

    # Count expected positions from DRAFT_ORDER (up to roster size)
    expected_counts = {}
    for round_index in range(len(roster)):
        round_priorities = DRAFT_ORDER[round_index]
        if not round_priorities:
            continue

        highest_priority = max(round_priorities, key=round_priorities.get)

        if highest_priority == FLEX:
            # FLEX can be RB or WR - don't count specifically
            pass
        else:
            expected_counts[highest_priority] = expected_counts.get(highest_priority, 0) + 1

    # Verify counts match (accounting for FLEX flexibility)
    # This is complex - may need refinement based on actual roster rules
    return True  # TODO: Implement proper validation
```

**Unit Test Required:**
```python
def test_roster_composition_matches_draft_order():
    """
    Verify roster composition always aligns with DRAFT_ORDER expectations.

    This test ensures the system can't create invalid rosters.
    """
    # Test various roster combinations
    # Ensure MAX_POSITIONS limits align with DRAFT_ORDER
    pass  # Detailed implementation in testing phase
```

---

## Integration with Scoring Engine

### Current Scoring (To Be Removed)

```python
# OLD - compute_positional_need_score() - DELETE THIS
pos_score = self.compute_positional_need_score(player)
```

### New Scoring (Add to Roster Mode Only)

```python
# Step 5 of 7: Add DRAFT_ORDER bonus
current_round = get_current_draft_round(self.team.roster)
draft_bonus = calculate_draft_order_bonus(player, current_round)
draft_bonus_score = team_rank_multiplied_score + draft_bonus
```

### Waiver Optimizer and Trade Simulator

**NO DRAFT_ORDER bonus** - these modes skip this step entirely.

---

## Class Structure

```python
class DraftOrderCalculator:
    """
    Calculates DRAFT_ORDER round-based bonuses for draft recommendations.

    This calculator determines the current draft round and applies position-specific
    bonuses based on the configured draft strategy.
    """

    def __init__(
        self,
        team,
        primary_bonus: float = 50.0,
        secondary_bonus: float = 25.0,
        logger=None
    ):
        """
        Initialize the DRAFT_ORDER calculator.

        Args:
            team: FantasyTeam instance
            primary_bonus: Bonus points for primary position (default: 50.0)
            secondary_bonus: Bonus points for secondary position (default: 25.0)
            logger: Logger instance for debugging
        """
        self.team = team
        self.primary_bonus = primary_bonus
        self.secondary_bonus = secondary_bonus
        self.logger = logger or logging.getLogger(__name__)
        self._current_round_cache = None

    def get_current_draft_round(self) -> Optional[int]:
        """
        Determine the current draft round based on roster size.

        Returns:
            int: Current round index (0-indexed), or None if draft complete
        """
        roster_size = len(self.team.roster)

        if roster_size >= Constants.MAX_PLAYERS:
            self.logger.debug("Draft complete, no current round")
            return None

        self.logger.debug(f"Current draft round: {roster_size + 1} (index {roster_size})")
        return roster_size

    def get_round_priorities(self, round_index: int) -> Dict[str, float]:
        """
        Get position priorities for a specific round.

        Args:
            round_index: Zero-indexed round number

        Returns:
            dict: Position -> bonus points mapping
        """
        if round_index is None or round_index >= len(Constants.DRAFT_ORDER):
            return {}

        return Constants.DRAFT_ORDER[round_index]

    def calculate_bonus(self, player: FantasyPlayer) -> float:
        """
        Calculate DRAFT_ORDER bonus for a player based on current round.

        Args:
            player: Player to calculate bonus for

        Returns:
            float: Bonus points to add to player's score
        """
        # Get current round
        current_round = self.get_current_draft_round()

        if current_round is None:
            return 0.0  # Draft complete

        # Get priorities for this round
        round_priorities = self.get_round_priorities(current_round)

        if not round_priorities:
            return 0.0  # No priorities defined

        player_position = player.position

        # Check direct position match
        if player_position in round_priorities:
            bonus = round_priorities[player_position]
            self.logger.info(
                f"DRAFT_ORDER bonus for {player.name} ({player_position}): "
                f"+{bonus} pts (Round {current_round + 1})"
            )
            return bonus

        # Check FLEX eligibility
        if player_position in Constants.FLEX_ELIGIBLE_POSITIONS and Constants.FLEX in round_priorities:
            bonus = round_priorities[Constants.FLEX]
            self.logger.info(
                f"DRAFT_ORDER bonus for {player.name} ({player_position}→FLEX): "
                f"+{bonus} pts (Round {current_round + 1})"
            )
            return bonus

        # No match
        self.logger.debug(
            f"No DRAFT_ORDER bonus for {player.name} ({player_position}) "
            f"in Round {current_round + 1}"
        )
        return 0.0

    def assign_players_to_rounds(self) -> Dict[int, FantasyPlayer]:
        """
        Assign existing roster players to draft rounds for display purposes.

        Returns:
            dict: Mapping of round_number (1-15) -> FantasyPlayer
        """
        round_assignments = {}
        unassigned_players = self.team.roster.copy()

        for round_num in range(1, Constants.MAX_PLAYERS + 1):
            if not unassigned_players:
                break

            round_index = round_num - 1
            round_priorities = Constants.DRAFT_ORDER[round_index]

            if not round_priorities:
                continue

            highest_priority = max(round_priorities, key=round_priorities.get)

            for player in unassigned_players:
                position_matches = (
                    player.position == highest_priority or
                    (player.position in Constants.FLEX_ELIGIBLE_POSITIONS and
                     highest_priority == Constants.FLEX)
                )

                if position_matches:
                    round_assignments[round_num] = player
                    unassigned_players.remove(player)
                    self.logger.debug(
                        f"Assigned {player.name} ({player.position}) to Round {round_num}"
                    )
                    break

        return round_assignments
```

---

## Testing Strategy

### Unit Test 1: Current Round Detection

```python
def test_current_round_empty_roster():
    """Test round detection with empty roster"""
    team = FantasyTeam()
    calc = DraftOrderCalculator(team)

    current_round = calc.get_current_draft_round()
    assert current_round == 0  # Round 1 (index 0)


def test_current_round_partial_roster():
    """Test round detection with partial roster"""
    team = FantasyTeam()
    # Add 4 players
    for i in range(4):
        team.draft_player(FantasyPlayer(id=i, drafted=2))

    calc = DraftOrderCalculator(team)
    current_round = calc.get_current_draft_round()
    assert current_round == 4  # Round 5 (index 4)


def test_current_round_full_roster():
    """Test round detection with full roster"""
    team = FantasyTeam()
    # Add 15 players (MAX_PLAYERS)
    for i in range(15):
        team.draft_player(FantasyPlayer(id=i, drafted=2))

    calc = DraftOrderCalculator(team)
    current_round = calc.get_current_draft_round()
    assert current_round is None  # Draft complete
```

### Unit Test 2: Bonus Calculation

```python
def test_bonus_round_1_flex_priority():
    """Test DRAFT_ORDER bonus in Round 1 (FLEX priority)"""
    team = FantasyTeam()  # Empty roster = Round 1
    calc = DraftOrderCalculator(team, primary_bonus=50, secondary_bonus=25)

    # DRAFT_ORDER[0] = {FLEX: 50, QB: 25}
    rb = FantasyPlayer(position='RB')  # FLEX-eligible
    qb = FantasyPlayer(position='QB')
    te = FantasyPlayer(position='TE')

    assert calc.calculate_bonus(rb) == 50.0  # FLEX priority
    assert calc.calculate_bonus(qb) == 25.0  # QB secondary
    assert calc.calculate_bonus(te) == 0.0   # Not in priorities


def test_bonus_round_5_qb_priority():
    """Test DRAFT_ORDER bonus in Round 5 (QB priority)"""
    team = FantasyTeam()
    # Draft 4 players to reach Round 5
    for i in range(4):
        team.draft_player(FantasyPlayer(id=i, drafted=2))

    calc = DraftOrderCalculator(team, primary_bonus=50, secondary_bonus=25)

    # DRAFT_ORDER[4] = {QB: 50, FLEX: 25}
    qb = FantasyPlayer(position='QB')
    rb = FantasyPlayer(position='RB')  # FLEX-eligible
    te = FantasyPlayer(position='TE')

    assert calc.calculate_bonus(qb) == 50.0  # QB primary
    assert calc.calculate_bonus(rb) == 25.0  # FLEX secondary
    assert calc.calculate_bonus(te) == 0.0   # Not in priorities
```

### Unit Test 3: Round Assignment

```python
def test_assign_players_to_rounds():
    """Test roster player assignment to rounds"""
    team = FantasyTeam()

    # Create roster matching DRAFT_ORDER expectations
    players = [
        FantasyPlayer(id=1, position='RB', drafted=2),   # Round 1: FLEX
        FantasyPlayer(id=2, position='WR', drafted=2),   # Round 2: FLEX
        FantasyPlayer(id=3, position='WR', drafted=2),   # Round 3: FLEX
        FantasyPlayer(id=4, position='RB', drafted=2),   # Round 4: FLEX
        FantasyPlayer(id=5, position='QB', drafted=2),   # Round 5: QB
    ]

    for player in players:
        team.draft_player(player)

    calc = DraftOrderCalculator(team)
    assignments = calc.assign_players_to_rounds()

    assert len(assignments) == 5
    assert assignments[1].position in ['RB', 'WR']  # FLEX
    assert assignments[5].position == 'QB'          # QB round
```

### Unit Test 4: Roster Validation

```python
def test_roster_composition_matches_draft_order():
    """Verify roster composition aligns with DRAFT_ORDER"""
    # This test ensures MAX_POSITIONS and DRAFT_ORDER are consistent
    # Count expected positions from DRAFT_ORDER
    expected_counts = {}
    for round_dict in DRAFT_ORDER:
        highest_priority = max(round_dict, key=round_dict.get)
        if highest_priority != FLEX:
            expected_counts[highest_priority] = expected_counts.get(highest_priority, 0) + 1

    # Verify against MAX_POSITIONS
    for position, expected_count in expected_counts.items():
        assert MAX_POSITIONS[position] >= expected_count, \
            f"MAX_POSITIONS[{position}] ({MAX_POSITIONS[position]}) < expected from DRAFT_ORDER ({expected_count})"
```

---

## Configuration Syntax Fix

### Current Issue (Line 49)

```python
DRAFT_ORDER = [
    {FLEX: 1.0 QB: 0.7},    # ❌ SYNTAX ERROR - Missing comma
```

### Fixed Syntax

```python
DRAFT_ORDER = [
    {FLEX: 50, QB: 25},     # ✅ FIXED - Comma added, static values
```

---

## Migration Notes

### Before (Positional Need)

```python
# OLD scoring calculation:
pos_score = compute_positional_need_score(player)  # 0-300+ range
# Formula: (max_limit - current_count) * POS_NEEDED_SCORE
```

### After (DRAFT_ORDER Bonus)

```python
# NEW scoring calculation:
draft_bonus = calculate_draft_order_bonus(player, current_round)  # 0-50 range
# Formula: direct lookup from DRAFT_ORDER dictionary
```

### Impact Comparison

| Scenario | Old Positional Need | New DRAFT_ORDER Bonus |
|----------|--------------------|-----------------------|
| Round 1, need RB | ~195 points | 50 points |
| Round 5, QB priority | ~130 points | 50 points |
| Round 1, TE (not priority) | ~130 points | 0 points |

**Note:** Scores will be lower with new system, but this is intentional. The normalized base scores (0-100 range) combined with bonuses (0-50 range) create a more balanced scoring system.

---

## File Structure

**Location:** `draft_helper/core/draft_order_calculator.py`

**Dependencies:**
- `draft_helper/draft_helper_constants.py` - DRAFT_ORDER, MAX_POSITIONS
- `shared_files/FantasyPlayer.py` - Player data model
- `draft_helper/FantasyTeam.py` - Team roster
- `logging` - Standard library

**Imported By:**
- `draft_helper/core/scoring_engine.py` - Main scoring calculations
- Test files

---

## Design Complete

**Next Steps:**
1. Fix DRAFT_ORDER syntax error in config
2. Update DRAFT_ORDER values to static points
3. Implement `DraftOrderCalculator` class
4. Write comprehensive unit tests
5. Integrate into `ScoringEngine` (Add to Roster mode only)
6. Validate roster composition alignment

**Design Approved:** Ready for implementation in Phase 2-3