# Sub-Feature 7: DraftedRosterManager Consolidation

## Objective
Consolidate DraftedRosterManager functionality into PlayerManager (eliminates 680+ lines of fuzzy matching code).

## Dependencies
**Prerequisites:** Sub-feature 1 (Core Data Loading)
**Blocks:** None

## Scope (12 items)
- NEW-124 to NEW-135: DraftedRosterManager consolidation

**From checklist:**
- NEW-124: Add get_players_by_team() method to PlayerManager
- NEW-125: Add comprehensive docstrings
- NEW-126: Add error handling
- NEW-127: Remove DraftedRosterManager import from TradeSimulatorModeManager
- NEW-128: Simplify _initialize_team_data() method
- NEW-129: Update docstrings in TradeSimulatorModeManager
- NEW-130 to NEW-131: Add deprecation warnings to DraftedRosterManager
- NEW-132 to NEW-135: Testing

## Key Implementation

**90% of DraftedRosterManager becomes obsolete** - JSON drafted_by field eliminates need for fuzzy matching.

**Add to PlayerManager:**
```python
def get_players_by_team(self) -> Dict[str, List[FantasyPlayer]]:
    """Organize players by their fantasy team."""
    teams = {}
    for player in self.all_players:
        if player.drafted_by:  # Non-empty = drafted
            if player.drafted_by not in teams:
                teams[player.drafted_by] = []
            teams[player.drafted_by].append(player)
    return teams
```

**Update TradeSimulatorModeManager (lines 209-219):**
```python
# OLD:
drafted_data_csv = self.data_folder / 'drafted_data.csv'
roster_manager = DraftedRosterManager(str(drafted_data_csv), Constants.FANTASY_TEAM_NAME)
if roster_manager.load_drafted_data():
    self.team_rosters = roster_manager.get_players_by_team(all_players)

# NEW:
self.team_rosters = self.player_manager.get_players_by_team()
```

## Success Criteria
- [ ] 3 roster methods added to PlayerManager
- [ ] TradeSimulatorModeManager updated (2 files)
- [ ] DraftedRosterManager marked deprecated
- [ ] Trade analysis working with new approach

See `research/DRAFTED_ROSTER_MANAGER_ANALYSIS.md` for complete analysis.
