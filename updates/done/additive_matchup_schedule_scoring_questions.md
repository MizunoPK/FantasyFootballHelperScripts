# Questions: Additive Matchup and Schedule Scoring Implementation

**Status**: Awaiting User Answers

**Context**: After 3 iterations of codebase research, several implementation choices and preferences need clarification before proceeding.

---

## Q1: Initial IMPACT_SCALE Values

**Question**: What initial values should we use for IMPACT_SCALE parameters?

**Options**:
A. **Use proposed values from spec** (MATCHUP: 150.0, SCHEDULE: 80.0)
   - Start with spec values and optimize later via simulation
   - Rationale: These were calculated based on NORMALIZATION_MAX_SCALE and expected bonus ranges

B. **Start with conservative values** (MATCHUP: 100.0, SCHEDULE: 50.0)
   - Lower initial values to minimize risk of over-valuing waiver players
   - Optimize upward if simulation shows improvement

C. **Run optimization immediately** (no preset values)
   - Skip manual values entirely, let simulation find optimal IMPACT_SCALE
   - Requires more simulation time upfront

**Recommendation**: Option A - Use spec values (150.0, 80.0) as starting point, then optimize

**Your Answer**:
```
Option A
```

---

## Q2: Minimum Acceptable Win Rate

**Question**: What's the minimum win rate to consider the additive system successful?

**Context**: We'll implement additive scoring, run full re-optimization, and evaluate results. If performance is poor, we'll revert the commit.

**Options**:
A. **High bar** (≥73%)
   - Must match or exceed typical optimal performance
   - Strictest success criteria

B. **Reasonable bar** (≥70%)
   - Allows 3% degradation for conceptually better system
   - Balance performance with logic

C. **Any improvement** (>50%)
   - As long as it's better than random
   - Focus on philosophy over performance

**Recommendation**: Option B - ≥70% win rate

**Your Answer**:
```
Option B
```

---

## Q3: Documentation Timing

**Question**: When should we update documentation (README, ARCHITECTURE)?

**Options**:
A. **Before implementation**
   - Update docs to reflect planned changes
   - Ensures docs stay in sync
   - Risk: May need revision if implementation differs

B. **After implementation, before simulation**
   - Document what was actually implemented
   - More accurate documentation
   - Can test docs with real code

C. **After simulation validation**
   - Only document changes that proved successful
   - Risk: If simulation fails, docs already outdated
   - Most conservative approach

**Recommendation**: Option B - After implementation, before simulation

**Your Answer**:
```
Option B
```

---

## Q4: Handling Existing Tests

**Question**: How should we handle test_PlayerManager_scoring.py tests that expect multiplicative scoring?

**Context**: This file likely has assertions checking for multiplier values (e.g., `* 1.05`)

**Options**:
A. **Update all tests immediately**
   - Change assertions to expect additive bonuses
   - Ensures test suite stays green
   - Most work upfront

B. **Mark tests as expected to change**
   - Add `@pytest.mark.skip(reason="Pending additive scoring update")`
   - Update after implementation complete
   - Allows incremental progress

C. **Create new test file for additive**
   - Keep old tests as-is
   - Add new test_PlayerManager_scoring_additive.py
   - Eventually remove old tests

**Recommendation**: Option A - Update all tests immediately for clean test suite

**Your Answer**:
```
Option A
```

---

## Q5: Parameter Optimization Priority

**Question**: Which parameters should be optimized first after implementing additive scoring?

**Options**:
A. **IMPACT_SCALE only** (focused)
   - Optimize MATCHUP_IMPACT_SCALE and SCHEDULE_IMPACT_SCALE first
   - Keep other parameters at current optimal values
   - Fastest to isolate additive system performance

B. **IMPACT_SCALE + WEIGHT** (moderate)
   - Optimize IMPACT_SCALE and WEIGHT parameters together
   - Better optimization but more combinations

C. **Full re-optimization** (comprehensive)
   - Re-optimize all 16+ parameters with new additive system
   - Most thorough but slowest (days of simulation)

**Recommendation**: Option A - IMPACT_SCALE only, then Option C if results are promising

**Your Answer**:
```
Option C
```

---

## Q6: Backward Compatibility Strategy

**Question**: How should we handle configs without IMPACT_SCALE?

**Context**: ConfigManager will default to 150.0/80.0 if IMPACT_SCALE missing

**Options**:
A. **Silent defaults** (current plan)
   - Use default values without warning
   - Seamless backward compatibility
   - Risk: Users don't know defaults are being used

B. **Warning logged** (current plan)
   - Log warning when IMPACT_SCALE missing
   - Users aware defaults are active
   - Encourages config updates

C. **Error and require explicit value**
   - Fail if IMPACT_SCALE not in config
   - Forces users to make conscious choice
   - Breaking change

**Recommendation**: Option B - Warning logged (already in TODO)

**Your Answer**:
```
Option C
```

---

## Summary

**Answers Provided**: 6/6 ✅

**Implementation Approach**:
- Implement additive scoring system directly (no feature flags or A/B testing)
- Use initial IMPACT_SCALE values: MATCHUP=150.0, SCHEDULE=80.0
- Run full re-optimization of all parameters after implementation
- Accept results if win rate ≥70%
- If results are poor (<70%), revert the commit and keep current system

Once TODO is updated with these answers, we'll proceed with the second verification round (3 more iterations) before implementation begins.
