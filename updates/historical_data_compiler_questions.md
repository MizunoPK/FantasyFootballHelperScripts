# Historical Data Compiler - Questions for User

> These questions arose during the first verification round (7 iterations). Please answer each question to help refine the implementation plan.

---

## Q1: Module Structure

**Context**: The TODO proposes creating a `historical_data_compiler/` module folder with 5+ submodules.

**Question**: How should we structure the code?

**Options**:
1. **Multi-module structure** - Create `historical_data_compiler/` with separate files for each component (schedule_fetcher.py, game_data_fetcher.py, etc.)
   - Pros: Clean separation, easy to test, follows existing `player-data-fetcher/` pattern
   - Cons: More files to manage, more import complexity

2. **Single-file script** - Put everything in `compile_historical_data.py` at root level
   - Pros: Simple, easy to understand, no import issues
   - Cons: Potentially large file (1000+ lines), harder to test individual components

3. **Minimal modules** - Root script with just 1-2 helper modules for complex logic
   - Pros: Balance of simplicity and organization
   - Cons: May need refactoring later if code grows

**Recommendation**: Option 1 (Multi-module structure) - matches existing project patterns

**Your Answer**: Option 1

---

## Q2: Code Reuse Strategy

**Context**: The `player-data-fetcher/` module has working code for ESPN API calls, weather fetching, and team data calculation.

**Question**: How should we handle code that overlaps with existing functionality?

**Options**:
1. **Import from existing modules** - Use imports from `player-data-fetcher/` directly
   - Pros: DRY, consistent behavior, no duplication
   - Cons: Creates dependencies, existing code optimized for current season not historical

2. **Copy and adapt** - Copy relevant code to new module, modify for historical data needs
   - Pros: Full control, can optimize for historical use case
   - Cons: Code duplication, two places to maintain

3. **Extract shared utilities** - Create new `utils/espn_api.py` with common functions used by both
   - Pros: Proper abstraction, both modules can benefit
   - Cons: Requires refactoring existing code, higher risk

**Recommendation**: Option 2 (Copy and adapt) - historical data compiler is standalone, different requirements than live fetcher

**Your Answer**: Option 2

---

## Q3: API Rate Limiting

**Context**: Historical data compilation requires many API calls (17 weeks × multiple requests per week). ESPN may rate limit.

**Question**: How should we handle API rate limiting?

**Options**:
1. **Aggressive throttling** - Add 1-2 second delays between all requests
   - Pros: Very safe, unlikely to hit rate limits
   - Cons: Slow (could take 30+ minutes per season)

2. **Minimal throttling** - Small delays (0.5s) only between batches
   - Pros: Faster execution (~10 minutes)
   - Cons: May hit rate limits occasionally

3. **Adaptive throttling** - Start fast, slow down if we get 429 errors
   - Pros: Optimal speed when possible, handles rate limits gracefully
   - Cons: More complex to implement

**Recommendation**: Option 3 (Adaptive throttling) - matches existing `espn_client.py` pattern with tenacity retry

**Your Answer**: Option 3

---

## Q4: Error Handling for Partial Data

**Context**: The spec says "fail loudly" for errors. But what if one week's data is missing while 16 weeks succeed?

**Question**: How should we handle partial failures?

**Options**:
1. **Fail completely** - Any error stops entire compilation, no output
   - Pros: Guarantees complete data or nothing
   - Cons: One bad week means no data at all

2. **Continue with warnings** - Log errors but continue, output incomplete data with clear markers
   - Pros: Get most data even if some fails
   - Cons: Risk of using incomplete data unknowingly

3. **Checkpoint and resume** - Save progress, allow re-running to fill gaps
   - Pros: Robust for large jobs, can recover from failures
   - Cons: More complex, need state management

**Recommendation**: Option 1 (Fail completely) - per original spec "fail loudly", simulation needs complete data

**Your Answer**: Option 1

---

## Q5: Multi-Year Support

**Context**: The script supports `--year` parameter. Should it support compiling multiple years at once?

**Question**: Should we add batch processing for multiple years?

**Options**:
1. **Single year only** - `--year 2024` runs one year at a time
   - Pros: Simple, predictable, easy to debug
   - Cons: User must run multiple times for historical analysis

2. **Year range support** - Add `--start-year 2021 --end-year 2024`
   - Pros: Convenient for initial population
   - Cons: More complex argument handling

3. **All available years** - Add `--all-years` flag to compile 2021-present
   - Pros: Easiest for full historical setup
   - Cons: Could be slow/risky if API issues mid-run

**Recommendation**: Option 1 (Single year only) for initial implementation - can add batch later

**Your Answer**: Option 1

---

## Q6: Output Location

**Context**: The spec says output goes to `simulation/sim_data/{YEAR}/`.

**Question**: Is this the correct location, or should we use a different folder?

**Options**:
1. **simulation/sim_data/{YEAR}/** - As specified in requirements
   - Pros: Matches spec, future simulation integration
   - Cons: Mixes with current season data

2. **simulation/historical_data/{YEAR}/** - Separate folder for historical
   - Pros: Clear separation, no confusion with current data
   - Cons: Different from spec, needs simulation update

3. **Configurable via --output-dir** - Let user specify
   - Pros: Flexible
   - Cons: More complexity, inconsistent outputs

**Recommendation**: Option 1 (simulation/sim_data/{YEAR}/) - matches spec exactly

**Your Answer**: Option 1

---

## Q7: Testing Strategy

**Context**: New code needs tests. Should we prioritize unit tests, integration tests, or both?

**Question**: What testing approach should we use?

**Options**:
1. **Unit tests only** - Mock all API calls, test logic in isolation
   - Pros: Fast, reliable, no network dependency
   - Cons: May miss integration issues

2. **Unit + live API tests** - Unit tests plus optional live API integration tests
   - Pros: Thorough coverage, catches real API changes
   - Cons: Integration tests may fail in CI, need network

3. **Unit + fixture tests** - Unit tests plus tests with saved API response fixtures
   - Pros: Good coverage without network, reproducible
   - Cons: Fixtures can become stale, need maintenance

**Recommendation**: Option 3 (Unit + fixture tests) - reliable tests with real data patterns

**Your Answer**: Option 3

---

## Summary

Please review each question and provide your answers. After receiving answers, I'll update the TODO file and proceed with the second verification round (9 more iterations).
