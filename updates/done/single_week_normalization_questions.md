# Single Week Normalization - Implementation Questions

Based on codebase research during the first verification round (3 iterations), the following questions will help clarify implementation preferences and user expectations.

---

## Question 1: max_weekly_projection Caching Strategy

**Context**: The system needs to track the maximum weekly projection for normalization. There are two approaches:

**Option A: Recalculate on each mode invocation (Recommended)**
- Calculate max_weekly_projection when StarterHelperMode is entered
- Simple implementation: one field, recalculated as needed
- Low memory footprint
- Suitable since mode invocations are infrequent

**Option B: Cache per-week maximums**
- Store dictionary: `{week_num: max_projection}`
- Calculate once, reuse across mode invocations
- More complex but faster for repeated calls
- Requires cache invalidation if player data changes

**Research finding**: Starter Helper mode is typically called once per user session, making Option A sufficient.

**Question**: Which approach do you prefer?
- [ ] **Option A**: Recalculate each time (simpler, recommended)
- [X] **Option B**: Cache with dictionary (more complex, faster)
- [ ] **Other**: (specify)

**Recommendation**: Option A for simplicity and lower maintenance burden.

---

## Question 2: Zero max_weekly_projection Handling

**Context**: If no players have valid weekly projections (data quality issue), max_weekly_projection could be 0.

**Option A: Return 0.0 for all normalized scores (Fail-safe)**
- If max_weekly_projection == 0, weight_projection() returns 0.0
- Prevents division by zero
- Makes scoring issues obvious (all scores are 0)
- User can identify data problems

**Option B: Fall back to ROS normalization**
- If max_weekly_projection == 0, use max_projection instead
- Graceful degradation
- Scoring continues with slightly incorrect scale
- May mask data quality issues

**Question**: How should the system handle zero max_weekly_projection?
- [X] **Option A**: Return 0.0 (fail-safe, makes issues obvious)
- [ ] **Option B**: Fall back to ROS max (graceful degradation)
- [ ] **Other**: (specify)

**Recommendation**: Option A with WARNING log to alert user of data issue.

---

## Question 3: Logging Level for Normalization Details

**Context**: The implementation will add logging for normalization calculations to aid debugging.

**Option A: DEBUG level only**
- DEBUG: Log max_weekly_projection calculation
- DEBUG: Log which max is used (weekly vs ROS)
- DEBUG: Log normalization formula and result
- Keeps logs clean during normal operation

**Option B: INFO level for mode entry, DEBUG for calculations**
- INFO: Log "Using weekly normalization: max={value}" when entering Starter Helper
- DEBUG: Detailed calculation logs
- More visible to users, helps verify correct behavior

**Option C: Minimal logging (calculation details only)**
- Only log the final normalized value
- No mode-specific messages
- Quieter logs

**Question**: What logging level do you prefer?
- [X] **Option A**: DEBUG only (cleanest logs)
- [ ] **Option B**: INFO for mode entry + DEBUG for details (recommended)
- [ ] **Option C**: Minimal (quietest)
- [ ] **Other**: (specify)

**Recommendation**: Option B for better visibility during initial rollout.

---

## Question 4: Test Data Expectations

**Context**: After implementation, weekly normalized scores will be higher (using full 0-N scale). Existing tests may need updates.

**Option A: Update all existing test assertions**
- Modify test_normalization_with_weekly_projection_enabled (line 426)
- Update expected values to reflect new calculation
- More test churn but ensures correctness

**Option B: Add new tests, leave existing tests if they still pass**
- Add new tests specifically for weekly normalization behavior
- Only update existing tests if they fail
- Less test churn

**Question**: How should existing tests be handled?
- [X] **Option A**: Proactively update all affected tests (thorough)
- [ ] **Option B**: Only update tests that fail (minimal churn)
- [ ] **Other**: (specify)

**Recommendation**: Option A for thoroughness and clear test intent.

---

## Question 5: Documentation Detail Level

**Context**: The scoring documentation (docs/scoring/01_normalization.md) needs updates.

**Option A: Brief update (1-2 paragraphs)**
- Add section explaining single-week vs ROS difference
- Simple before/after example
- Quick reference

**Option B: Comprehensive update (Recommended)**
- Detailed explanation of max_weekly_projection tracking
- Multiple examples showing calculation differences
- Code references with line numbers
- Decision rationale (why separate normalization needed)

**Option C: Minimal update (code comments only)**
- Just add inline code comments
- No documentation file updates
- Fastest but least helpful for future reference

**Question**: What level of documentation detail do you prefer?
- [X] **Option A**: Brief (1-2 paragraphs)
- [ ] **Option B**: Comprehensive (recommended for maintainability)
- [ ] **Option C**: Minimal (code comments only)
- [ ] **Other**: (specify)

**Recommendation**: Option B to maintain high-quality documentation standards.

---

## Question 6: Backward Compatibility Verification

**Context**: Other modes (Draft Helper, Trade Simulator) must continue using ROS normalization unchanged.

**Option A: Add explicit verification tests**
- Create tests that explicitly check Draft Helper mode unchanged
- Create tests that explicitly check Trade Simulator mode unchanged
- Higher confidence, more thorough

**Option B: Rely on existing integration tests**
- Existing tests should catch any regressions
- Run full test suite to verify
- Less test code but still safe

**Question**: How thoroughly should backward compatibility be tested?
- [X] **Option A**: Add explicit new verification tests (thorough)
- [ ] **Option B**: Rely on existing integration tests (sufficient)
- [ ] **Other**: (specify)

**Recommendation**: Option B since comprehensive integration tests already exist.

---

## Summary

**Total Questions**: 6
**Questions requiring user input**: 6
**Questions with recommendations**: 6

Please answer each question by marking your chosen option with an [x]. You can also specify "Other" with custom requirements if the provided options don't match your needs.

After receiving your answers, I will:
1. Update the TODO file with your choices
2. Execute the second verification round (3 more iterations)
3. Finalize the implementation plan
4. Begin systematic implementation

---

## User Answers

*(Please fill in your answers below)*

### Question 1: max_weekly_projection Caching
- [ ] Option A (Recommended)
- [ ] Option B
- [ ] Other:

### Question 2: Zero max_weekly_projection Handling
- [ ] Option A (Recommended)
- [ ] Option B
- [ ] Other:

### Question 3: Logging Level
- [ ] Option A
- [ ] Option B (Recommended)
- [ ] Option C
- [ ] Other:

### Question 4: Test Data Expectations
- [ ] Option A (Recommended)
- [ ] Option B
- [ ] Other:

### Question 5: Documentation Detail
- [ ] Option A
- [ ] Option B (Recommended)
- [ ] Option C
- [ ] Other:

### Question 6: Backward Compatibility Testing
- [ ] Option A
- [ ] Option B (Recommended)
- [ ] Other:

**Additional Notes/Requirements**: *(Optional - add any additional context or requirements)*
