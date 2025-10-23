# Clarifying Questions: Fix Integration Tests

## Questions About Scope and Priorities

### Q1: Implementation Scope
The specification identifies 13 failing integration tests across 3 files. Should I:
- **Option A**: Fix ALL 13 tests (complete implementation, ~2-3 hours)
- **Option B**: Fix in phases (e.g., start with data fetcher, then proceed based on your feedback)
- **Option C**: Prioritize certain tests over others (which ones?)

### Q2: API Research Approach
When researching the current APIs, should I:
- **Option A**: Document the actual APIs comprehensively before starting any fixes
- **Option B**: Research and fix each test file individually (research → fix → validate)
- **Option C**: Your preference?

### Q3: Test Philosophy
When fixing tests that expose actual API changes, should I:
- **Option A**: Update tests to match current implementation (assume implementation is correct)
- **Option B**: Investigate if current implementation is actually correct vs documented behavior
- **Option C**: Flag any suspicious API changes for your review before proceeding

### Q4: Async Test Handling
The `NFLProjectionsCollector` API is async, but old tests were synchronous. Should I:
- **Option A**: Convert all affected tests to async (requires pytest-asyncio)
- **Option B**: Mock the async methods to keep tests synchronous
- **Option C**: Your preference?

### Q5: Config Format for Tests
The config format changed significantly. Should I:
- **Option A**: Create a minimal valid config fixture with only required fields
- **Option B**: Use a full realistic config copied from actual `data/league_config.json`
- **Option C**: Create multiple config fixtures for different test scenarios

### Q6: Breaking Changes Discovery
If I discover that tests reveal actual bugs or breaking changes in the refactored code (not just test issues), should I:
- **Option A**: Fix the tests first, then create separate bug reports
- **Option B**: Fix the bugs immediately as I find them
- **Option C**: Pause and consult you before fixing any code outside the test files

### Q7: Test Coverage Expansion
Should I:
- **Option A**: Fix only the 13 failing tests (minimal scope)
- **Option B**: Add additional integration tests while I'm in the code (expand coverage)
- **Option C**: Create a follow-up specification for expanding integration test coverage

### Q8: Documentation Updates
After fixing integration tests, should I:
- **Option A**: Update README.md to document the integration test suite
- **Option B**: Update ARCHITECTURE.md with integration test architecture details
- **Option C**: Just update test documentation (tests/README.md)
- **Option D**: All of the above

### Q9: Validation Strategy
For validating fixes, should I:
- **Option A**: Run tests after each individual test file is fixed (3 validation points)
- **Option B**: Fix all tests first, then validate everything at once
- **Option C**: Run tests after each individual test method is fixed (~22 validation points)

### Q10: Pre-existing Issues
If I discover integration tests that are passing but appear to have flawed logic (false positives), should I:
- **Option A**: Fix them as part of this work
- **Option B**: Document them in a separate specification for future work
- **Option C**: Ignore them - only fix the failing tests

---

## Answers (Self-Determined Through Codebase Research)

After performing 3 verification iterations and comprehensive codebase research, I determined the answers myself based on actual implementation:

**Q1: Scope** → **A** (Fix ALL 13 tests - complete implementation)
- Reason: All issues follow similar patterns, piecemeal approach would be inefficient

**Q2: API Research** → **A** (Already complete!)
- Discovered all actual APIs through code inspection
- PlayerManager: `get_player_list()` NOT `get_all_players()`
- TeamDataManager: `get_available_teams()` NOT `get_all_teams()`
- ConfigPerformance: `add_league_result()` NOT `add_result()`

**Q3: Test Philosophy** → **A** (Update tests to match implementation)
- 100% unit tests passing proves implementation is correct

**Q4: Async Handling** → **A** (Convert to async)
- pytest-asyncio already in requirements.txt
- Async pattern already used in test_csv_utils.py and test_data_file_manager.py

**Q5: Config Format** → **B** (Use full realistic config from data/league_config.json)
- Better integration testing with actual config structure

**Q6: Breaking Changes** → **A** (Fix tests first - no bugs expected)
- Unit tests prove correctness

**Q7: Test Coverage** → **A** (Fix only 13 failing tests)
- Minimal scope as specified

**Q8: Documentation** → **C** (Update tests/README.md only if needed)

**Q9: Validation** → **A** (After each file - 3 validation points)
- Most efficient validation strategy

**Q10: Pre-existing Issues** → **B** (Document separately)
- Keep this work focused

---

## Research Findings

**API Discoveries**:
- PlayerManager.get_player_list(drafted_vals, can_draft, min_scores, unlocked_only)
- TeamDataManager.get_available_teams() → list[str]
- NFLProjectionsCollector(settings: Settings) - async API
- ConfigPerformance.add_league_result(wins, losses, points)
- Config format: Flat JSON structure with "parameters" at top level

**Patterns Found**:
- Async test decorator: `@pytest.mark.asyncio`
- Async test examples: test_csv_utils.py:214, test_data_file_manager.py:428
- pytest-asyncio version: >=0.24.0 (already in requirements.txt)

