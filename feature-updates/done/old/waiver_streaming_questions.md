# Waiver Streaming Mode - Questions for User

**Objective**: Clarify implementation details for waiver streaming mode selection

**Source**: `updates/waiver_streaming.txt`

---

## Mode Selection UI

### Q1: Should mode selection allow cancellation?

**Context**: When user enters Waiver Optimizer, they're presented with mode selection.

**Options**:
- **Option A**: Include "Cancel" option that returns to Trade Simulator menu
- **Option B**: Require mode selection (no cancel option)

**Recommendation**: Option A (include cancel) - gives user flexibility to back out

Answer: Option A

---

## Scoring Parameters

### Q2: Should we use team_quality in Current Week mode?

**Context**: The spec says "using the same scoring calculation that the Starter Helper uses". Starter Helper includes `team_quality=True` (StarterHelperModeManager.py line 370).

**Current Understanding**: team_quality should be included (matches Starter Helper exactly)

**Confirmation Needed**: Is this correct, or should team_quality be excluded for weekly streaming?

**Recommendation**: Include team_quality=True (matches spec "same scoring calculation")

Answer: Yes include team_quality

---

## Display and User Experience

### Q3: Should we show scoring parameters in the output?

**Context**: Users might not understand why recommendations differ between modes.

**Options**:
- **Option A**: Show brief explanation ("Weekly projections with matchup multipliers")
- **Option B**: Show detailed scoring parameters (matchup=True, player_rating=False, etc.)
- **Option C**: Minimal display (just show mode name)

**Recommendation**: Option A (brief explanation) - balances clarity with simplicity

Answer: Option C

---

## File Output

### Q4: Should mode be included in filename?

**Context**: Waiver recommendations are saved to files in trade_outputs/

**Current Filename**: `waiver_optimizer_YYYYMMDD_HHMMSS.txt`

**Options**:
- **Option A**: `waiver_ros_YYYYMMDD_HHMMSS.txt` and `waiver_weekly_YYYYMMDD_HHMMSS.txt`
- **Option B**: `waiver_optimizer_YYYYMMDD_HHMMSS.txt` (include mode in file header only)

**Recommendation**: Option A (include in filename) - easier to distinguish files

Answer: Option A

---

## Trade Threshold

### Q5: Should MIN_WAIVER_IMPROVEMENT differ between modes?

**Context**: Current MIN_WAIVER_IMPROVEMENT = 0 (in Constants, used line 249, 851)

**Question**: Should Current Week mode use a different threshold than Rest of Season mode?

**Reasoning**:
- Weekly streaming often targets smaller, short-term advantages
- Rest of Season targets longer-term value

**Options**:
- **Option A**: Same threshold for both modes (simpler)
- **Option B**: Different thresholds (e.g., 0 for Current Week, 5 for Rest of Season)

**Recommendation**: Option A (same threshold) - can adjust later if needed

Answer: Option A

---

## Trade Suggestor and Manual Trade Modes

### Q6: Should Trade Suggestor also have mode selection?

**Context**: The spec ONLY mentions Waiver Optimizer. Trade Suggestor finds trades with opponents.

**Question**: Should Trade Suggestor also offer weekly vs seasonal scoring?

**Use Case**: Weekly scoring might help find "win this week" trades vs long-term value trades

**Options**:
- **Option A**: Only Waiver Optimizer has mode selection (per spec)
- **Option B**: Extend mode selection to Trade Suggestor as well

**Recommendation**: Option A (only Waiver Optimizer) - follows spec, can extend later if desired

Answer: Option A

### Q7: Should Manual Trade Visualizer have mode selection?

**Same Context/Options as Q6**

**Recommendation**: Option A (only Waiver Optimizer) - follows spec

Answer: Option A

---

## Documentation

### Q8: Should we add detailed scoring documentation?

**Context**: New mode introduces different scoring calculations

**Options**:
- **Option A**: Add `docs/scoring/waiver_streaming.md` with detailed explanation
- **Option B**: Document in README only
- **Option C**: Minimal documentation

**Recommendation**: Option B (README only for now) - can add detailed docs later if needed

Answer: Option B

---

## Backward Compatibility

### Q9: Should we maintain exact backward compatibility?

**Context**: Adding use_weekly_scoring parameter to TradeSimTeam

**Current Approach**: Default value False preserves all existing behavior

**Question**: Is this the right approach, or should we consider any migration?

**Recommendation**: Default False is correct - maintains backward compatibility

Answer: Yes correct

---

## Testing

### Q10: What level of test coverage is expected?

**Options**:
- **Option A**: Standard coverage (unit tests + integration tests)
- **Option B**: Comprehensive coverage (add performance tests, edge cases)
- **Option C**: Minimal coverage (basic functionality only)

**Recommendation**: Option A (standard coverage) - balances thoroughness with effort

Answer: Option A

---

## Future Enhancements

### Q11: Should we plan for additional modes in the future?

**Context**: Currently planning for 2 modes (Rest of Season, Current Week)

**Potential Future Modes**:
- "Next 3 Weeks" (short-term streaming)
- "Playoff Focus" (weeks 15-17 only)
- "Custom Window" (user specifies week range)

**Question**: Should architecture support easy addition of future modes?

**Recommendation**: Yes - use flexible parameter structure, but don't over-engineer

Answer: Yes

---

## README Correction

### Q12: Confirm README correction?

**Issue Found**: README.md lines 133-135 list incorrect sub-mode names

**Current (INCORRECT)**:
- Manual Trade Visualizer
- Search Trade Opportunities
- Full Trade Simulation

**Actual (from code)**:
- Waiver Optimizer
- Trade Suggestor
- Manual Trade Visualizer

**Question**: Should we correct README as part of this update?

**Recommendation**: Yes - correct it now to prevent confusion

Answer: Yes

---

## Summary of Recommendations

| Question | Recommendation |
|----------|---------------|
| Q1: Cancellation | Include cancel option |
| Q2: team_quality | Include (matches Starter Helper) |
| Q3: Display params | Show brief explanation |
| Q4: Filename mode | Include mode in filename |
| Q5: Threshold | Same threshold for both modes |
| Q6: Trade Suggestor mode | Only Waiver Optimizer (per spec) |
| Q7: Manual Trade mode | Only Waiver Optimizer (per spec) |
| Q8: Documentation | README only for now |
| Q9: Backward compat | Default False (maintains compatibility) |
| Q10: Test coverage | Standard coverage |
| Q11: Future modes | Support flexible structure |
| Q12: README correction | Yes, correct now |

**High Priority Clarifications**:
- Q2: Confirm team_quality inclusion
- Q4: Confirm filename format preference
- Q6/Q7: Confirm scope (Waiver Optimizer only)
- Q12: Confirm README correction

**Low Priority** (can use recommendations):
- Q1, Q3, Q5, Q8, Q9, Q10, Q11
