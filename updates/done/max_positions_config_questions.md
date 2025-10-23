# MAX_POSITIONS Config Migration - Questions

These questions arose during codebase research and planning. Your answers will help finalize the implementation approach.

---

## Question 1: MAX_PLAYERS Handling Strategy

**Context**:
- `MAX_PLAYERS` constant (currently 15) is tightly coupled to `MAX_POSITIONS`
- Current code has a test that validates: `sum(MAX_POSITIONS.values()) == MAX_PLAYERS`
- MAX_PLAYERS is referenced in 14 places across PlayerManager, FantasyTeam, and AddToRosterModeManager
- The two values must stay synchronized

**Question**: How should we handle MAX_PLAYERS when moving MAX_POSITIONS to config?

**Options**:

**A) Add MAX_PLAYERS to config as explicit value (with validation)**
- Pros: Explicit, easy to understand, matches current structure
- Cons: Redundant (can be calculated from MAX_POSITIONS), risk of desynchronization
- Implementation: Add to config.json, validate `max_players == sum(max_positions.values())`

**B) Calculate MAX_PLAYERS dynamically as a property (RECOMMENDED)**
- Pros: Single source of truth, impossible to desynchronize, cleaner
- Cons: Slightly less explicit in config file
- Implementation: Add `@property` to ConfigManager that returns `sum(self.max_positions.values())`

**Recommendation**: **Option B** - Calculate dynamically to avoid duplication and ensure consistency

**Your Answer**:
<!-- Please choose A or B, or suggest alternative approach -->
Option B

---

## Question 2: Deprecation Strategy for Constants

**Context**:
- After migration, `Constants.MAX_POSITIONS` will be redundant
- May want transition period for backward compatibility
- Could keep with deprecation warning or remove immediately

**Question**: Should we deprecate Constants.MAX_POSITIONS or remove it immediately?

**Options**:

**A) Keep with deprecation comment (transition period)**
- Keep constant in constants.py
- Add comment: `# Deprecated: Use ConfigManager.max_positions instead`
- Update all internal code to use config version
- External code (if any) can still import constant

**B) Remove immediately and update all references**
- Delete MAX_POSITIONS from constants.py
- Update ALL references at once in single change
- Cleaner but breaks any external dependencies

**Recommendation**: **Option A** - Keep with deprecation for safety, can remove in future cleanup

**Your Answer**:
<!-- Please choose A or B -->
Option B

---

## Question 3: Default Values Confirmation

**Context**:
- Current MAX_POSITIONS values in constants.py (line 60-68):
  ```python
  MAX_POSITIONS = {
      QB: 2,      # 2 Quarterbacks
      RB: 4,      # 4 Running Backs
      WR: 4,      # 4 Wide Receivers
      FLEX: 2,    # 2 FLEX (RB/WR/TE/DST eligible)
      TE: 1,      # 1 Tight End
      K: 1,       # 1 Kicker
      DST: 1,     # 1 Defense/Special Teams
  }
  # Sum = 15 players
  ```

**Question**: Should these values be used as the defaults in league_config.json?

**Your Answer**:
<!-- Please confirm "Yes" or provide different values -->
Yes

---

## Question 4: Config Structure Format

**Context**:
- Need to decide how to represent position limits in JSON
- Two possible formats:

**Format A: String keys (matches current constant structure)**
```json
"MAX_POSITIONS": {
  "QB": 2,
  "RB": 4,
  "WR": 4,
  "FLEX": 2,
  "TE": 1,
  "K": 1,
  "DST": 1
}
```

**Format B: Full names for clarity**
```json
"MAX_POSITIONS": {
  "QUARTERBACK": 2,
  "RUNNING_BACK": 4,
  "WIDE_RECEIVER": 4,
  "FLEX": 2,
  "TIGHT_END": 1,
  "KICKER": 1,
  "DEFENSE": 1
}
```

**Recommendation**: **Format A** - Use position abbreviations (QB, RB, WR, etc.) to match existing constant structure and code expectations

**Your Answer**:
<!-- Please choose A or B -->
A

---

## Question 5: Validation Strictness

**Context**:
- Need to validate MAX_POSITIONS config structure
- Can be strict (fail on any issue) or lenient (use defaults)

**Question**: How strict should validation be?

**Options**:

**A) Strict validation (RECOMMENDED)**
- Require all positions present (QB, RB, WR, TE, K, DST, FLEX)
- Require all values be positive integers
- Raise ValueError if anything missing or invalid
- Ensures config is always valid

**B) Lenient validation with defaults**
- Use default values if position missing
- Coerce to int if possible
- Only fail on critical errors
- More forgiving but riskier

**Recommendation**: **Option A** - Strict validation to catch configuration errors early

**Your Answer**:
<!-- Please choose A or B -->
A

---

## Question 6: Testing Strategy

**Context**:
- 13 test files mock ConfigManager
- Tests will need max_positions attribute on mocks
- Can update tests incrementally or all at once

**Question**: Should test updates be done:

**A) Incrementally (as tests fail)**
- Run tests after implementation
- Fix mocks as tests fail
- Iterative approach

**B) Proactively (update all mocks upfront)**
- Search for all config mocks before implementation
- Add max_positions to all mocks preemptively
- Prevents test failures

**Recommendation**: **Option B** - Update mocks proactively as part of Phase 3 to ensure clean test run

**Your Answer**:
<!-- Please choose A or B -->
B

---

## Summary

Please answer each question above. Once I receive your answers, I will:
1. Update the TODO file with your decisions (STEP 4)
2. Perform second verification round with 3 more iterations (STEP 5)
3. Begin implementation with a comprehensive, verified plan

**Current Progress**: First verification round complete (3/6 iterations), awaiting answers to proceed
