# Pre-Commit Validation Checklist

**Usage**: Execute this checklist when instructed to "validate and commit" changes
**Purpose**: Ensure code quality, test coverage, and system stability before committing
**Duration**: 10-15 minutes depending on scope of changes

---

## 📊 **Step 1: Analyze All Changes**

### **Change Analysis**
- [ ] Run `git status` to identify all modified files
- [ ] Run `git diff` to review all code changes
- [ ] Run `git diff --cached` to review staged changes
- [ ] List new files created since last commit
- [ ] List deleted files since last commit

### **Change Context Documentation**
- [ ] **Modified Files**: Document what was changed and why
- [ ] **New Features**: List new functionality added
- [ ] **Bug Fixes**: Document issues resolved
- [ ] **Breaking Changes**: Note any API or interface changes
- [ ] **Dependencies**: Check if new dependencies were added

**Change Summary**:
```
Modified Files:
- [File 1]: [Description of changes]
- [File 2]: [Description of changes]

New Files:
- [File 1]: [Purpose]
- [File 2]: [Purpose]

Deleted Files:
- [File 1]: [Reason for deletion]

Key Changes:
- [Feature/Fix 1]: [Description]
- [Feature/Fix 2]: [Description]
```

---

## 🧪 **Step 2: Unit Test Assessment**

### **Test Coverage Analysis**
- [ ] Identify new functions/methods that need unit tests
- [ ] Identify edge cases not covered by existing tests
- [ ] Check for dependencies on config files or static files
- [ ] Ensure tests use mocks for external dependencies

### **Required New Tests**
- [ ] **New Functions**: Create tests for all new functions/methods
- [ ] **Edge Cases**: Test boundary conditions and error scenarios
- [ ] **Mock Dependencies**: Replace config/file dependencies with mocks
- [ ] **Integration Points**: Test interactions between modified components

### **Test Implementation**
- [ ] Write new unit tests for uncovered code
- [ ] Ensure tests are deterministic (no random behavior)
- [ ] Verify tests don't require external files or network access
- [ ] Add parametrized tests for multiple input scenarios

**New Tests Added**:
```
Test File: [test_file.py]
- test_[function_name]_[scenario]: [Description]
- test_[function_name]_edge_case: [Description]

Mock Usage:
- @mock.patch('[dependency]'): [Reason]
- Mock data files: [copied into test]
```

---

## ✅ **Step 3: Full Repository Test Suite**

### **MANDATORY: Execute Complete Test Suite**

**CRITICAL**: You MUST run the complete test suite across ALL modules. Do not skip this step.

### **Required Test Commands**
Execute ALL of the following test suites in order:

```bash
# 1. Core runner scripts (REQUIRED)
python -m pytest tests/test_runner_scripts.py -v

# 2. Draft helper tests (REQUIRED)
python -m pytest draft_helper/tests/test_draft_helper.py -v

# 3. Shared files tests (REQUIRED)
python -m pytest shared_files/tests/ -v

# 4. Player data fetcher tests (REQUIRED)
python -m pytest player-data-fetcher/tests/ -v

# 5. NFL scores fetcher tests (REQUIRED)
python -m pytest nfl-scores-fetcher/tests/ -v

# 6. Starter helper tests (REQUIRED)
python -m pytest starter_helper/tests/ -v

# 7. Full suite summary (REQUIRED - run this last for final verification)
python -m pytest tests/ draft_helper/tests/test_draft_helper.py shared_files/tests/ --tb=short
```

**IMPORTANT**: If ANY test suite times out or fails, you MUST investigate and fix before proceeding.

### **Test Results Validation**
- [ ] **Core Tests**: 21/21 runner script tests pass
- [ ] **Draft Helper Tests**: 34/34 tests pass
- [ ] **Shared Files Tests**: All tests pass
- [ ] **Player Data Fetcher Tests**: All tests pass
- [ ] **NFL Scores Fetcher Tests**: All tests pass
- [ ] **Starter Helper Tests**: All tests pass
- [ ] **Pass Rate**: 100% of tests must pass (no exceptions)
- [ ] **New Test Validation**: All newly added tests pass
- [ ] **Regression Check**: No previously passing tests now fail
- [ ] **Performance Check**: No significant test slowdown

**Test Execution Results**:
```
Module: tests/test_runner_scripts.py
  Tests: [X]/21 passed ✅/❌

Module: draft_helper/tests/test_draft_helper.py
  Tests: [X]/34 passed ✅/❌

Module: shared_files/tests/
  Tests: [X]/[X] passed ✅/❌

Module: player-data-fetcher/tests/
  Tests: [X]/[X] passed ✅/❌

Module: nfl-scores-fetcher/tests/
  Tests: [X]/[X] passed ✅/❌

Module: starter_helper/tests/
  Tests: [X]/[X] passed ✅/❌

TOTAL TESTS: [X]
PASSED: [X]
FAILED: [0] ← MUST BE ZERO
SKIPPED: [X]
Duration: [X seconds]

New Tests Added: [X]
All New Tests Pass: ✅/❌
```

---

## 🔧 **Step 4: Integration Testing**

### **Core Application Startup Validation**
- [ ] **Player Data Fetcher Startup Test**: Verify application starts without errors
- [ ] **NFL Scores Fetcher Startup Test**: Verify application starts without errors

### **Startup Test Execution**
```bash
# Test player data fetcher startup (should load config and show progress)
timeout 10 python run_player_data_fetcher.py
# Expected: Shows "Starting player data fetcher..." or similar, no import/config errors
# Press Ctrl+C after startup confirmation

# Test NFL scores fetcher startup (should load config and show progress)
timeout 10 python run_nfl_scores_fetcher.py
# Expected: Shows startup message or begins fetching, no import/config errors
# Press Ctrl+C after startup confirmation
```

### **Startup Validation Results**
- [ ] **Player Data Fetcher**: ✅ Starts successfully / ❌ Import/config errors
- [ ] **NFL Scores Fetcher**: ✅ Starts successfully / ❌ Import/config errors
- [ ] **No Import Errors**: All required modules load properly
- [ ] **Configuration Loading**: All config files parse without errors

### **Draft Helper Validation**
- [ ] Copy `draft_helper_validation_checklist.md` to `tests/temp_integration_checklist.md`
- [ ] Execute all 23 integration test steps
- [ ] Update checklist with pass/fail status for each test
- [ ] Validate FLEX system functionality
- [ ] Verify CSV data persistence
- [ ] Confirm point calculations accuracy

### **Integration Test Execution**
```bash
# Copy checklist for working reference
cp tests/draft_helper_validation_checklist.md tests/temp_integration_checklist.md

# Execute integration test sequence
echo -e "2\nHunt\n6\nexit\n3\n\n4\nHunt\n1\ny\nHampton\n1\ny\nexit\n1\n1\n5\n15\ny\n16\n3\n\n5\n15\ny\n16\n6\n\n7\n" | python run_draft_helper.py
```

- [ ] **Test 1-4**: Mark Drafted Player ✅/❌
- [ ] **Test 5-7**: Trade Analysis ✅/❌
- [ ] **Test 8-11**: Drop Player ✅/❌
- [ ] **Test 12-13**: Add to Roster ✅/❌
- [ ] **Test 14-19**: Lock/Unlock ✅/❌
- [ ] **Test 20-22**: Starter Helper ✅/❌
- [ ] **Test 23**: Clean Exit ✅/❌

### **Critical Validations**
- [ ] **FLEX System**: WR (4/4) and FLEX (1/1) display correctly
- [ ] **CSV Updates**: All changes reflected in `shared_files/players.csv`
- [ ] **Point Consistency**: Fantasy points consistent across all modes

### **Cleanup**
- [ ] Delete `tests/temp_integration_checklist.md` after completion

---

## 📚 **Step 5: Documentation Updates**

### **Rules Files Assessment**
- [ ] Check if `potential_updates/rules.txt` needs updates
- [ ] Review project-specific rules for changes
- [ ] Update development protocols if workflows changed
- [ ] Document new testing procedures if added

### **README Updates**
- [ ] Update main `README.md` if functionality changed
- [ ] Update module-specific README files
- [ ] Document new features or significant changes
- [ ] Update installation/setup instructions if needed
- [ ] Refresh usage examples if interfaces changed

### **CLAUDE.md Updates**
- [ ] Update configuration documentation for new settings
- [ ] Document new development patterns or standards
- [ ] Update tool usage instructions if changed
- [ ] Refresh testing procedures and validation steps

**Documentation Changes Made**:
```
Files Updated:
- README.md: [Changes]
- CLAUDE.md: [Changes]
- potential_updates/rules.txt: [Changes]

New Documentation:
- [File]: [Purpose]
```

---

## 💾 **Step 6: Commit Changes**

### **Pre-Commit Verification**
- [ ] All tests passing (100% pass rate)
- [ ] Integration tests completed successfully
- [ ] Documentation updated appropriately
- [ ] No temporary or debug files staged
- [ ] No sensitive data in commit

### **Commit Execution**
- [ ] Stage all relevant changes: `git add .`
- [ ] Verify staged files: `git status`
- [ ] Create commit with clear, concise message
- [ ] **EXCLUDE**: Do not commit this checklist file
- [ ] **EXCLUDE**: Do not include icons or Claude references
- [ ] **EXCLUDE**: Do not commit temporary test files

### **Commit Message Format**
```bash
git commit -m "Brief description of changes

- Key change 1
- Key change 2
- Key change 3

[Type]: [Component] - [Brief description]
Examples:
- Fix: FLEX assignment in roster display
- Add: Unit tests for parameter validation
- Update: Documentation for new features
"
```

**Commit Command**:
```bash
git add .
git status  # Verify correct files staged
git commit -m "[COMMIT MESSAGE]"
```

---

## 🧹 **Step 7: Cleanup**

### **File Cleanup**
- [ ] Delete this checklist file: `rm tests/pre_commit_validation_checklist.md`
- [ ] Remove any temporary test files created
- [ ] Clean up debug output files
- [ ] Verify no leftover development artifacts

### **Final Verification**
- [ ] `git status` shows clean working directory
- [ ] No uncommitted changes remain
- [ ] Repository is in clean state for next development cycle

---

## ❌ **Failure Protocols**

### **If Tests Fail**
1. **STOP** - Do not proceed with commit
2. Fix failing tests or code issues
3. Re-run full validation checklist
4. Only commit when all tests pass

### **If Integration Tests Fail**
1. **STOP** - Critical functionality is broken
2. Debug and fix integration issues
3. Re-run integration test suite
4. Verify FLEX system and CSV persistence

### **If Documentation is Outdated**
1. Update all relevant documentation
2. Ensure accuracy of setup/usage instructions
3. Re-verify documentation changes

---

## ✅ **Success Criteria**

**Ready to Commit When**:
- [ ] All unit tests pass (100% pass rate)
- [ ] All integration tests pass (23/23 steps)
- [ ] New tests added for new functionality
- [ ] Documentation updated appropriately
- [ ] No temporary files in staging area
- [ ] Commit message is clear and concise

**Final Checklist Complete**: ✅ Ready to commit and cleanup

---

*This checklist ensures code quality, test coverage, and system stability before any commit.*