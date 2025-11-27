# New Scoring Parameters - Implementation Questions

These questions arose during the first verification round (iterations 1-5) of codebase research.

---

## Q1: GameDataManager Injection Pattern

**Context**: The PlayerScoringCalculator is currently created in PlayerManager.__init__ with these parameters:
```python
self.scoring_calculator = PlayerScoringCalculator(
    config,
    self.projected_points_manager,
    0.0,
    team_data_manager,
    season_schedule_manager,
    config.current_nfl_week
)
```

**Question**: How should GameDataManager be integrated?

**Options**:
1. **Add to PlayerScoringCalculator constructor** - Pass as new parameter, similar to team_data_manager
2. **Add setter method** - Add `set_game_data_manager()` to PlayerScoringCalculator
3. **Create in PlayerManager** - PlayerManager creates GameDataManager and passes to scorer

**Recommendation**: Option 1 (constructor parameter) is cleanest and matches existing patterns. GameDataManager would be created in LeagueHelperManager and passed through PlayerManager.


Answer: Option 1

---

## Q2: Simulation Game Data Handling

**Context**:
- `simulation/sim_data/game_data.csv` contains 2024 historical data
- `data/game_data.csv` contains 2025 current season data
- Simulation runs through weeks 1-17, changing `config.current_nfl_week` each iteration

**Question**: Should simulation use game conditions for weekly scoring?

**Options**:
1. **Yes - Full integration** - Simulation uses historical game data for weekly lineup optimization
2. **Yes - Optional** - Add flag to enable/disable game conditions in simulation
3. **No - Skip for now** - Game conditions only apply to League Helper, not simulation

**Recommendation**: Option 2 (optional). This allows simulation to test parameters but can be disabled if it complicates things. The spec says "Update the simulation to allow for testing of different parameters for the new scoring."

Answer: Option 1

---

## Q3: Default Values for New Parameters

**Context**: The spec recommends starting values:
- TEMPERATURE_SCORING: IMPACT_SCALE=50.0, WEIGHT=1.0
- WIND_SCORING: IMPACT_SCALE=60.0, WEIGHT=1.0
- LOCATION_MODIFIERS: HOME=2, AWAY=-2, INTERNATIONAL=-5

**Question**: Should new scoring steps be enabled or disabled by default in score_player()?

**Options**:
1. **All disabled by default** (temperature=False, wind=False, location=False) - Conservative, explicit enablement
2. **All enabled by default** - Aggressive, users get new features immediately
3. **Some enabled** - E.g., location=True (simpler), weather=False (complex)

**Recommendation**: Option 1 (all disabled by default). This follows the existing pattern where `matchup=False`, `schedule=False` by default. Starter Helper mode explicitly enables them.

Answer: Option 1

---

## Q4: Position-Specific Weather Effects

**Context**: The spec mentions potential position-specific effects:
> "Wind: Most affects QB, WR, K; may benefit RB, DST"
> "Cold: Most affects K (kick distance), QB (ball grip)"

**Question**: Should weather effects be position-specific?

**Options**:
1. **No - Uniform effect** - All players get same temperature/wind bonus/penalty
2. **Yes - Position-specific multipliers** - Different effect magnitudes by position
3. **Later enhancement** - Implement uniform first, position-specific later

**Recommendation**: Option 1 (uniform effect) for initial implementation. The spec documents this as "future consideration." We can add position-specific effects in a later iteration if desired.

Answer: Have the Wind penalty only apply to QB, WR, and K. Other positions will just not have that scoring method considered for them. Have Temperature effect ALL positions

---

## Q5: ConfigManager get_location_modifier() Signature

**Context**: The spec shows:
```python
def get_location_modifier(self, game: UpcomingGame, team: str) -> float
```

**Question**: Should get_location_modifier be in ConfigManager or as a method on UpcomingGame?

**Options**:
1. **ConfigManager method** - Keeps all scoring logic in ConfigManager, consistent with other getters
2. **UpcomingGame method** - `game.get_location_modifier(team, config)` - keeps data + logic together
3. **PlayerScoringCalculator helper** - Calculate directly in _apply_location_modifier

**Recommendation**: Option 1 (ConfigManager). This is consistent with other `get_*_multiplier()` methods and keeps configuration values in ConfigManager.

Answer: Option 1

---

## Q6: Test File Location for New Classes

**Context**: We're creating two new modules:
- `league_helper/util/game_data_models.py` (UpcomingGame dataclass)
- `league_helper/util/GameDataManager.py` (GameDataManager class)

**Question**: Should tests be in one file or two?

**Options**:
1. **Two separate files** - `test_game_data_models.py` and `test_GameDataManager.py`
2. **One combined file** - `test_game_data.py` covering both
3. **Existing file** - Add to `test_player_scoring.py` since closely related

**Recommendation**: Option 1 (two separate files). This follows the existing pattern where each source module has its own test file.

Answer: Option 1

---

## Q7: Backward Compatibility Error Handling

**Context**: Old config files won't have TEMPERATURE_SCORING, WIND_SCORING, or LOCATION_MODIFIERS.

**Question**: How should missing config sections be handled?

**Options**:
1. **Silent defaults** - Return neutral values (0 bonus) if config missing
2. **Log warning** - Log that weather/location scoring disabled due to missing config
3. **Require config** - Raise error if trying to use weather scoring without config

**Recommendation**: Option 1 (silent defaults) for scoring methods, but Option 2 (log warning) for _extract_parameters. This ensures existing configs work but makes it clear when features are disabled.

Answer: Option 1

---

## Answers Section

*Please provide answers to the questions above. The TODO file will be updated based on your responses.*

### A1: GameDataManager Injection Pattern
Answer:

### A2: Simulation Game Data Handling
Answer:

### A3: Default Values for New Parameters
Answer:

### A4: Position-Specific Weather Effects
Answer:

### A5: ConfigManager get_location_modifier() Signature
Answer:

### A6: Test File Location for New Classes
Answer:

### A7: Backward Compatibility Error Handling
Answer:
