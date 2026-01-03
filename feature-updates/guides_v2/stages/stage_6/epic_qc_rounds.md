# STAGE 6b: Epic QC Rounds Guide

🚨 **MANDATORY READING PROTOCOL**

**Before starting this stage:**
1. Use Read tool to load THIS ENTIRE GUIDE
2. Acknowledge critical requirements (see "Critical Rules" section below)
3. Verify prerequisites (see "Prerequisites Checklist" section below)
4. Update epic EPIC_README.md Agent Status with guide name + timestamp

**DO NOT proceed without reading this guide.**

**After session compaction:**
- Check EPIC_README.md Agent Status for current step
- READ THIS GUIDE again (full guide, not summary)
- Continue from "Next Action" in Agent Status

---

## Quick Start

**What is this stage?**
Epic QC Rounds validate the epic as a cohesive whole through 3 systematic quality checks: Cross-Feature Integration (Round 1), Epic Cohesion & Consistency (Round 2), and End-to-End Success Criteria (Round 3). Unlike feature-level QC (Stage 5c), these rounds focus on epic-wide patterns, architectural consistency, and validation against the original epic request.

**When do you use this guide?**
- After STAGE_6a complete (Epic Smoke Testing passed)
- Ready to perform deep QC validation on epic
- All cross-feature integration verified at basic level

**Key Outputs:**
- ✅ QC Round 1 complete (cross-feature integration validated)
- ✅ QC Round 2 complete (epic cohesion and consistency verified)
- ✅ QC Round 3 complete (success criteria met, original goals achieved)
- ✅ All findings documented in epic_lessons_learned.md
- ✅ Any issues fixed or bug fixes created

**Time Estimate:**
30-60 minutes (10-20 minutes per round)

**Exit Condition:**
Epic QC Rounds are complete when all 3 rounds pass with zero critical issues, all findings documented, and epic validated against original request

---

## Critical Rules

```
┌─────────────────────────────────────────────────────────────┐
│ CRITICAL RULES - These MUST be copied to README Agent Status │
└─────────────────────────────────────────────────────────────┘

1. ⚠️ ALL 3 QC rounds are MANDATORY (cannot skip any)
   - Round 1: Cross-Feature Integration
   - Round 2: Epic Cohesion & Consistency
   - Round 3: End-to-End Success Criteria
   - Must complete rounds in order (1 → 2 → 3)

2. ⚠️ If ANY round finds critical issues → Create bug fixes, RESTART Stage 6
   - Critical issue: Integration point fails, success criterion not met
   - After bug fix → RESTART from STAGE_6a (smoke testing)
   - Re-run: Smoke testing → QC 1 → QC 2 → QC 3

3. ⚠️ Minor issues can be fixed immediately without restart
   - Minor issue: Naming inconsistency, comment improvement
   - Fix immediately, re-run affected tests
   - Document fix in epic_lessons_learned.md
   - Continue to next round (no full restart)

4. ⚠️ ALL success criteria must be met 100%
   - If criterion was in original epic request or spec → REQUIRED
   - No "nice to have" or "optional" requirements
   - If cannot meet → Get user approval to remove from scope
   - Do NOT leave requirements unimplemented

5. ⚠️ Document findings for EACH round
   - Update epic_lessons_learned.md after each round
   - Include: Issues found, fixes applied, status
   - Serves as evidence of thorough QC

6. ⚠️ Focus on EPIC-LEVEL validation (not feature-level)
   - Feature-level QC done in Stage 5c
   - Epic-level focuses on: Integration, consistency, cohesion
   - Compare across ALL features (not individual features)
```

---

## Critical Decisions Summary

**This stage has ONE critical decision point per round:**

### Decision Point 1: QC Round 1 Result (PASS/FAIL)

**Question:** Did QC Round 1 find critical issues?
- **If ZERO critical issues:** Continue to Round 2
- **If critical issues found:** Create bug fixes, RESTART Stage 6 from 6a
- **Impact:** Critical integration issues require full restart

### Decision Point 2: QC Round 2 Result (PASS/MINOR/FAIL)

**Question:** Did QC Round 2 find issues?
- **If ZERO issues:** Continue to Round 3
- **If MINOR issues:** Fix immediately, continue to Round 3 (no restart)
- **If CRITICAL issues:** Create bug fixes, RESTART Stage 6 from 6a
- **Impact:** Minor consistency issues can be fixed inline, critical require restart

### Decision Point 3: QC Round 3 Result (PASS/FAIL)

**Question:** Did ALL success criteria pass?
- **If ALL criteria met:** Proceed to STAGE_6c
- **If ANY criteria not met:** Determine acceptability, fix or get user approval
- **If critical failures:** Create bug fixes, RESTART Stage 6 from 6a
- **Impact:** Unmet success criteria may invalidate epic implementation

---

## Prerequisites Checklist

**Before starting Epic QC Rounds (STAGE_6b), verify:**

□ **STAGE_6a complete:**
  - Epic smoke testing PASSED (all 4 parts)
  - Epic smoke test results documented
  - No smoke testing failures

□ **Epic smoke test plan executed:**
  - All import tests passed
  - All entry point tests passed
  - All E2E execution tests passed with DATA VALUES verified
  - All cross-feature integration tests passed

□ **Agent Status updated:**
  - EPIC_README.md shows STAGE_6a complete
  - Current guide: STAGE_6b_epic_qc_rounds_guide.md

□ **Original epic request available:**
  - Have access to {epic_name}.txt
  - Can reference original goals for Round 3

**If any prerequisite fails:**
- ❌ Do NOT start Epic QC Rounds
- Return to STAGE_6a to complete smoke testing
- Verify all prerequisites met before proceeding

---

## Workflow Overview

```
STAGE 6b: Epic QC Rounds
│
├─> QC ROUND 1: Cross-Feature Integration
│   ├─ Integration point validation
│   ├─ Data flow across features
│   ├─ Interface compatibility
│   ├─ Error propagation handling
│   └─ Document findings
│
├─> QC ROUND 2: Epic Cohesion & Consistency
│   ├─ Code style consistency
│   ├─ Naming convention consistency
│   ├─ Error handling consistency
│   ├─ Architectural pattern consistency
│   └─ Document findings
│
├─> QC ROUND 3: End-to-End Success Criteria
│   ├─ Validate against original epic request
│   ├─ Verify epic success criteria (from Stage 4)
│   ├─ User experience flow validation
│   ├─ Performance characteristics
│   └─ Document findings
│
└─> Decision: QC Rounds Result
    ├─ ALL PASSED → Proceed to STAGE_6c
    ├─ MINOR ISSUES → Fix, document, proceed to 6c
    └─ CRITICAL ISSUES → Create bug fixes, RESTART Stage 6
```

---

## QC Round 1: Cross-Feature Integration

**Objective:** Validate integration points between features work correctly.

**Time Estimate:** 10-20 minutes

---

### Step 1.1: Integration Point Validation

**Review integration points identified in Stage 4 epic_smoke_test_plan.md:**

**Find integration points section:**
```markdown
## Cross-Feature Integration Points

1. **Feature 01 → Feature 02:**
   - Feature 01 provides: `adp_multiplier` (float)
   - Feature 02 consumes: Used in matchup score calculation
   - Interface: `get_adp_multiplier(player_name: str) -> float`

2. **Feature 02 → Feature 03:**
   - Feature 02 provides: `matchup_difficulty` (str: 'easy'/'medium'/'hard')
   - Feature 03 consumes: Logged in performance tracking
   - Interface: `get_matchup_difficulty(player_name: str, week: int) -> str`

3. **Feature 03 → Feature 01:**
   - Feature 03 provides: `accuracy_score` (float 0-100)
   - Feature 01 consumes: Adjusts ADP confidence
   - Interface: `get_accuracy_score(player_name: str) -> float`
```

**Validation Questions for EACH integration point:**

1. **Do integration points use correct interfaces?**
   - ✅ Verify method signatures match between provider and consumer
   - ✅ Check parameter types are compatible
   - ✅ Verify return types match expectations

2. **Is data passed in expected format?**
   - ✅ Test with real data (not just types)
   - ✅ Verify data ranges are acceptable
   - ✅ Check for data corruption or transformation errors

3. **Are edge cases handled?**
   - ✅ What if provider returns None?
   - ✅ What if provider raises exception?
   - ✅ What if data is missing or invalid?

4. **Do features gracefully degrade if dependency unavailable?**
   - ✅ Test with Feature 01 disabled → Does Feature 02 crash or degrade?
   - ✅ Verify error messages are helpful
   - ✅ Check that epic continues with reduced functionality

**Document validation:**
```markdown
### Integration Point 1: Feature 01 → Feature 02

**Interface:** `get_adp_multiplier(player_name: str) -> float`

**Validation Results:**
- Interface match: ✅ PASS (signatures compatible)
- Data format: ✅ PASS (float in expected range 0.5-1.5)
- Edge case (None): ✅ PASS (returns 1.0 as default)
- Edge case (exception): ✅ PASS (logs error, returns default)
- Graceful degradation: ✅ PASS (Feature 02 works without ADP data)

**Status:** ✅ VALIDATED
```

---

### Step 1.2: Data Flow Across Features

**Trace data flow through a complete epic workflow:**

**Example Trace (Draft Workflow):**
```
User Input: python run_league_helper.py --mode draft --week 5
  ↓
Feature 01 (ADP Integration):
  - Fetch ADP data from CSV
  - Calculate adp_multiplier for each player
  - Output: player_data['adp_multiplier'] = 1.15
  ↓
Feature 02 (Matchup System):
  - Fetch matchup data from API
  - Calculate matchup_difficulty
  - Consume ADP multiplier from Feature 01
  - Combine: final_score = base * adp_mult * matchup_mult
  - Output: player_data['final_score'] = base * 1.15 * 0.85
  ↓
Feature 03 (Performance Tracker):
  - Log player selection with all data
  - Record: ADP rank, matchup difficulty, final score
  - Update historical accuracy
  - Output: performance_log.csv updated
  ↓
Final Output: Ranked draft recommendations with all features integrated
```

**Validation Steps:**

1. **Execute complete workflow with real data:**
   ```bash
   python run_league_helper.py --mode draft --week 5 --debug
   ```

2. **Verify data at each step:**
   ```python
   # After Feature 01
   assert 'adp_multiplier' in player_data
   assert 0.5 <= player_data['adp_multiplier'] <= 1.5

   # After Feature 02
   assert 'matchup_multiplier' in player_data
   assert player_data['final_score'] == (
       player_data['base_score'] *
       player_data['adp_multiplier'] *
       player_data['matchup_multiplier']
   )

   # After Feature 03
   assert performance_log_updated()
   assert 'adp_rank' in log_entry
   assert 'matchup_difficulty' in log_entry
   ```

3. **Check for data loss or corruption:**
   - ✅ No data dropped between features
   - ✅ No precision loss in calculations
   - ✅ All required fields present in final output

**Document findings:**
```markdown
### Data Flow Validation

**Workflow Tested:** Draft mode, Week 5

**Data Flow Trace:**
- User Input → Feature 01: ✅ Data received correctly
- Feature 01 → Feature 02: ✅ ADP multiplier passed correctly
- Feature 02 → Feature 03: ✅ Matchup data passed correctly
- Feature 03 → Output: ✅ All data present in final output

**Data Integrity:**
- No data loss: ✅ VERIFIED
- No corruption: ✅ VERIFIED
- Precision maintained: ✅ VERIFIED

**Status:** ✅ PASSED
```

---

### Step 1.3: Interface Compatibility

**Review interfaces between features in detail:**

**For EACH interface, verify:**

**Example Interface Review:**
```python
# Feature 01 provides:
def get_adp_multiplier(player_name: str, position: str) -> Tuple[float, int]:
    """
    Get ADP-based multiplier for a player.

    Args:
        player_name: Full player name (e.g., "Patrick Mahomes")
        position: Player position (QB, RB, WR, TE, K)

    Returns:
        Tuple[float, int]: (multiplier, adp_rank)
        - multiplier: 0.5-1.5 range, 1.0 = average
        - adp_rank: 1-500, lower is better

    Raises:
        DataProcessingError: If player not found in ADP data
    """
    pass

# Feature 02 consumes:
def calculate_matchup_score(
    player: FantasyPlayer,
    adp_data: Tuple[float, int]
) -> float:
    """
    Calculate matchup score with ADP adjustment.

    Args:
        player: FantasyPlayer object
        adp_data: Tuple from get_adp_multiplier (multiplier, rank)

    Returns:
        float: Matchup-adjusted score
    """
    multiplier, rank = adp_data  # Expects tuple
    pass
```

**Validation Checklist:**
- [ ] Type signatures match between provider and consumer
- [ ] Parameter names are clear and consistent
- [ ] Return values documented and understood by consumers
- [ ] Error handling for invalid inputs
- [ ] Docstrings explain interface contract
- [ ] Examples provided for complex interfaces

**Common Interface Issues to Check:**

1. **Type Mismatch:**
   ```python
   # Feature 01 returns:
   return 1.15  # float

   # Feature 02 expects:
   multiplier, rank = adp_data  # Expects tuple - MISMATCH!
   ```

2. **Parameter Order:**
   ```python
   # Feature 01 signature:
   get_data(player_name, position)

   # Feature 02 calls:
   get_data(position, player_name)  # WRONG ORDER!
   ```

3. **Missing Error Handling:**
   ```python
   # Feature 01 may raise DataProcessingError
   # Feature 02 doesn't catch it - ERROR PROPAGATES!
   ```

**Document findings:**
```markdown
### Interface Compatibility Review

**Interfaces Reviewed:** 5

**Compatibility Issues Found:** 0

**Interface Status:**
- Feature 01 → Feature 02: ✅ COMPATIBLE
- Feature 02 → Feature 03: ✅ COMPATIBLE
- Feature 03 → Feature 01: ✅ COMPATIBLE
- Shared utilities: ✅ COMPATIBLE
- Error interfaces: ✅ COMPATIBLE

**Status:** ✅ PASSED
```

---

### Step 1.4: Error Propagation Handling

**Test error propagation across features:**

**Error Scenarios to Test:**

**Scenario 1: Feature 01 Fails to Fetch ADP Data**
```python
# Simulate ADP data unavailable
# What happens?
# Expected: Feature 02 should NOT crash, should use default multiplier

# Test:
python run_league_helper.py --mode draft --week 5 --simulate-adp-failure

# Verify:
# - Feature 02 continues execution
# - Default multiplier (1.0) used
# - Error logged (not silent failure)
# - User sees warning: "ADP data unavailable, using default values"
```

**Scenario 2: Feature 02 Raises Invalid Matchup Data Exception**
```python
# Simulate invalid matchup data
# What happens?
# Expected: Epic should log error, continue with degraded functionality

# Test:
python run_league_helper.py --mode draft --week 5 --simulate-matchup-error

# Verify:
# - Epic doesn't crash
# - Feature 03 still records data (even without matchup info)
# - Error message identifies which feature failed
# - Epic output includes note about degraded data
```

**Scenario 3: Feature 03 Cannot Write to Performance Log**
```python
# Simulate permission error on log file
# What happens?
# Expected: Draft recommendations still generated, error logged

# Test:
python run_league_helper.py --mode draft --week 5 --readonly-log

# Verify:
# - Draft recommendations complete
# - Error logged: "Performance tracking failed: Permission denied"
# - Epic continues with reduced functionality
```

**Validation Checklist:**
- [ ] Errors don't cascade (one feature failure ≠ epic failure)
- [ ] Error messages identify which feature failed
- [ ] Epic continues with degraded functionality (if possible)
- [ ] User-facing errors are helpful (not technical stack traces)
- [ ] Errors logged for debugging
- [ ] Retry logic appropriate (for transient failures)

**Document findings:**
```markdown
### Error Propagation Testing

**Scenarios Tested:** 3

**Results:**
- ADP data failure: ✅ HANDLED GRACEFULLY (default values used)
- Matchup error: ✅ HANDLED GRACEFULLY (epic continues with warning)
- Performance log failure: ✅ HANDLED GRACEFULLY (draft still works)

**Error Handling Quality:**
- No cascade failures: ✅ VERIFIED
- Clear error messages: ✅ VERIFIED
- Graceful degradation: ✅ VERIFIED
- User-friendly errors: ✅ VERIFIED

**Status:** ✅ PASSED
```

---

### Step 1.5: Document QC Round 1 Findings

**Update epic_lessons_learned.md:**

```markdown
---

## Stage 6b - QC Round 1 Findings (Cross-Feature Integration)

**Date:** {YYYY-MM-DD}
**Round:** 1 of 3
**Focus:** Cross-feature integration validation

**Integration Points Reviewed:** 5
**Issues Found:** {0 or list}
**Status:** {✅ PASSED / ⚠️ MINOR ISSUES / ❌ CRITICAL ISSUES}

### Integration Point Summary

**Feature 01 → Feature 02 (ADP to Matchup):**
- Interface: ✅ Compatible
- Data flow: ✅ Correct
- Error handling: ✅ Graceful degradation

**Feature 02 → Feature 03 (Matchup to Performance):**
- Interface: ✅ Compatible
- Data flow: ✅ Correct
- Error handling: ✅ Graceful degradation

**Feature 03 → Feature 01 (Performance to ADP):**
- Interface: ✅ Compatible
- Data flow: ✅ Correct
- Error handling: ✅ Graceful degradation

### Data Flow Validation

**Workflow:** Draft mode, Week 5
- User Input → Features: ✅ Data received correctly
- Feature chaining: ✅ All data passed correctly
- Final output: ✅ All features integrated

### Error Propagation Testing

**Scenarios Tested:** 3
- ADP failure: ✅ Handled gracefully
- Matchup error: ✅ Handled gracefully
- Log failure: ✅ Handled gracefully

### Issues Found

{If ZERO issues:}
**No issues found.** All integration points validated successfully.

{If issues found:}
**Issue 1:** {Description}
- Severity: {CRITICAL / MINOR}
- Fix: {What was done OR bug fix created}

### Next Steps

{If PASSED:}
**Action:** Proceed to QC Round 2 (Epic Cohesion & Consistency)

{If CRITICAL ISSUES:}
**Action:** Create bug fixes, RESTART Stage 6 from STAGE_6a
**Bug Fixes:** {list}
```

**If CRITICAL issues found:**
- STOP - Do not proceed to Round 2
- Create bug fixes for integration issues
- After bug fixes complete → RESTART Stage 6 from STAGE_6a
- Re-run: Smoke testing → QC 1 → QC 2 → QC 3

**If MINOR issues found:**
- Fix immediately (if simple, like comment update)
- Document fix in findings
- Continue to Round 2

**If NO issues found:**
- Document "No issues found"
- Proceed to Round 2

---

## QC Round 2: Epic Cohesion & Consistency

**Objective:** Validate epic maintains consistency across all features.

**Time Estimate:** 10-20 minutes

---

### Step 2.1: Code Style Consistency

**Review code style across ALL feature implementations:**

**Consistency Checks:**

1. **Naming Conventions:**
   ```python
   # Check: Do all features use same naming pattern?

   # Feature 01:
   def get_adp_multiplier(...)  # Uses "get_" prefix

   # Feature 02:
   def get_matchup_difficulty(...)  # ✅ Also uses "get_" prefix

   # Feature 03:
   def fetch_performance_data(...)  # ❌ Uses "fetch_" prefix - INCONSISTENT!
   ```

2. **File Organization:**
   ```
   # Check: Do all features follow same structure?

   feature_01_adp_integration/
     ├── adp_manager.py           # Manager pattern
     ├── adp_data_loader.py       # Data loader
     └── tests/test_adp_manager.py

   feature_02_matchup_system/
     ├── matchup_manager.py       # ✅ Manager pattern
     ├── matchup_data_loader.py   # ✅ Data loader
     └── tests/test_matchup_manager.py

   feature_03_performance_tracker/
     ├── tracker.py               # ❌ NOT using Manager pattern - INCONSISTENT!
     ├── data_loader.py
     └── tests/test_tracker.py
   ```

3. **Import Style:**
   ```python
   # Check: Do all features use same import format?

   # Feature 01:
   from typing import Dict, List, Tuple
   from pathlib import Path

   # Feature 02:
   from typing import Dict, List, Tuple
   from pathlib import Path
   # ✅ Same style

   # Feature 03:
   import typing
   import os  # ❌ Uses os instead of Path - INCONSISTENT!
   ```

4. **Docstring Style:**
   ```python
   # Check: Do all features use same docstring format?

   # Feature 01:
   def get_data(player_name: str) -> float:
       """
       Get data for player.

       Args:
           player_name: Player name

       Returns:
           float: Data value
       """
   # Uses Google-style docstrings

   # Feature 02:
   def get_matchup(player: str) -> str:
       """Get matchup difficulty for player"""
   # ❌ One-line docstring, no Args/Returns - INCONSISTENT!
   ```

**Document findings:**
```markdown
### Code Style Consistency

**Areas Reviewed:** 4

**Findings:**
- Naming conventions: ⚠️ INCONSISTENT ("get_" vs "fetch_" prefix)
  - Fix: Renamed fetch_performance_data → get_performance_data
- File organization: ⚠️ INCONSISTENT (tracker.py vs manager pattern)
  - Fix: Renamed tracker.py → performance_manager.py
- Import style: ⚠️ INCONSISTENT (os vs Path)
  - Fix: Updated to use Path consistently
- Docstring style: ⚠️ INCONSISTENT (Google-style vs one-line)
  - Fix: Updated all docstrings to Google-style

**Status:** ⚠️ MINOR ISSUES (fixed inline)
```

---

### Step 2.2: Naming Convention Consistency

**Review naming across features:**

**Consistency Checks:**

1. **Variable Names:**
   ```python
   # Check: Similar concepts use similar names

   # Feature 01:
   player_name = "Patrick Mahomes"

   # Feature 02:
   player_name = "Patrick Mahomes"  # ✅ Consistent

   # Feature 03:
   player_id = "Patrick Mahomes"  # ❌ INCONSISTENT (id vs name)
   ```

2. **Abbreviations:**
   ```python
   # Check: Abbreviations are consistent

   # Feature 01:
   adp_rank = 5  # Uses lowercase "adp"

   # Feature 02:
   ADP_MULTIPLIER = 1.15  # ❌ Uses uppercase "ADP" - INCONSISTENT!

   # Should be: adp_multiplier = 1.15
   ```

3. **File Naming:**
   ```
   # Check: File naming follows same pattern

   feature_01_adp_integration/
     ├── adp_manager.py           # Uses underscore, lowercase

   feature_02_matchup_system/
     ├── matchup_manager.py       # ✅ Consistent

   feature_03_performance_tracker/
     ├── PerformanceManager.py    # ❌ PascalCase - INCONSISTENT!
   ```

**Document findings:**
```markdown
### Naming Convention Consistency

**Areas Reviewed:** 3

**Findings:**
- Variable names: ⚠️ INCONSISTENT (player_name vs player_id)
  - Fix: Standardized on player_name across all features
- Abbreviations: ⚠️ INCONSISTENT (adp vs ADP)
  - Fix: Standardized on lowercase (adp, csv, api)
- File naming: ⚠️ INCONSISTENT (snake_case vs PascalCase)
  - Fix: Renamed PerformanceManager.py → performance_manager.py

**Status:** ⚠️ MINOR ISSUES (fixed inline)
```

---

### Step 2.3: Error Handling Consistency

**Review error handling patterns:**

**Consistency Checks:**

1. **Error Classes:**
   ```python
   # Check: All features use same error classes

   # Feature 01:
   raise DataProcessingError(f"ADP data not found for {player_name}")

   # Feature 02:
   raise DataProcessingError(f"Matchup data not found for {player_name}")
   # ✅ Same error class

   # Feature 03:
   raise ValueError(f"Performance data not found")
   # ❌ Uses ValueError instead of DataProcessingError - INCONSISTENT!
   ```

2. **Error Messages:**
   ```python
   # Check: Error messages follow same format

   # Feature 01:
   f"ADP data not found for {player_name}"  # Format: "{What} not found for {who}"

   # Feature 02:
   f"Matchup data not found for {player_name}"  # ✅ Same format

   # Feature 03:
   f"No performance data: {player_name}"  # ❌ Different format - INCONSISTENT!
   ```

3. **Logging Levels:**
   ```python
   # Check: Similar errors use same logging level

   # Feature 01:
   logger.error(f"Failed to fetch ADP data: {error}")

   # Feature 02:
   logger.warning(f"Failed to fetch matchup data: {error}")
   # ❌ Uses WARNING for same severity - INCONSISTENT!

   # Should use ERROR for data fetch failures consistently
   ```

**Document findings:**
```markdown
### Error Handling Consistency

**Areas Reviewed:** 3

**Findings:**
- Error classes: ⚠️ INCONSISTENT (DataProcessingError vs ValueError)
  - Fix: Updated Feature 03 to use DataProcessingError
- Error messages: ⚠️ INCONSISTENT (message format varies)
  - Fix: Standardized format: "{What} not found for {player_name}"
- Logging levels: ⚠️ INCONSISTENT (ERROR vs WARNING)
  - Fix: Standardized data fetch failures → ERROR level

**Status:** ⚠️ MINOR ISSUES (fixed inline)
```

---

### Step 2.4: Architectural Pattern Consistency

**Review architectural patterns:**

**Consistency Checks:**

1. **Design Patterns:**
   ```python
   # Check: All features use same patterns

   # Feature 01: Manager pattern
   class AdpManager:
       def __init__(self, config):
           self.config = config
       def get_data(self):
           pass

   # Feature 02: Manager pattern
   class MatchupManager:
       def __init__(self, config):
           self.config = config
       def get_data(self):
           pass
   # ✅ Same pattern

   # Feature 03: No manager pattern
   def get_performance_data(config):  # ❌ Functional, not OO - INCONSISTENT!
       pass
   ```

2. **Data Access:**
   ```python
   # Check: Data access patterns consistent

   # Feature 01: Uses csv_utils
   from utils.csv_utils import read_csv_with_validation
   df = read_csv_with_validation('data/adp.csv', required_columns=['name', 'rank'])

   # Feature 02: Uses csv_utils
   from utils.csv_utils import read_csv_with_validation
   df = read_csv_with_validation('data/matchup.csv', required_columns=['name', 'difficulty'])
   # ✅ Same pattern

   # Feature 03: Direct pandas
   df = pd.read_csv('data/performance.csv')  # ❌ Direct access - INCONSISTENT!
   ```

3. **Configuration Access:**
   ```python
   # Check: Configuration access consistent

   # Feature 01: Uses ConfigManager
   config = ConfigManager(data_folder)
   multiplier = config.get_adp_multiplier(adp)

   # Feature 02: Uses ConfigManager
   config = ConfigManager(data_folder)
   difficulty = config.get_matchup_difficulty(matchup)
   # ✅ Same pattern

   # Feature 03: Direct JSON read
   with open('config.json') as f:
       config = json.load(f)  # ❌ Direct access - INCONSISTENT!
   ```

**Document findings:**
```markdown
### Architectural Pattern Consistency

**Areas Reviewed:** 3

**Findings:**
- Design patterns: ⚠️ INCONSISTENT (Manager pattern vs functional)
  - Fix: Refactored Feature 03 to use PerformanceManager class
- Data access: ⚠️ INCONSISTENT (csv_utils vs direct pandas)
  - Fix: Updated Feature 03 to use csv_utils
- Configuration: ⚠️ INCONSISTENT (ConfigManager vs direct JSON)
  - Fix: Updated Feature 03 to use ConfigManager

**Status:** ⚠️ MINOR ISSUES (fixed inline)
```

---

### Step 2.5: Document QC Round 2 Findings

**Update epic_lessons_learned.md:**

```markdown
---

## Stage 6b - QC Round 2 Findings (Epic Cohesion & Consistency)

**Date:** {YYYY-MM-DD}
**Round:** 2 of 3
**Focus:** Epic cohesion and consistency validation

**Consistency Areas Reviewed:** 4
**Issues Found:** {count}
**Status:** {✅ PASSED / ⚠️ MINOR ISSUES / ❌ CRITICAL ISSUES}

### Code Style Consistency

- Naming conventions: {✅ CONSISTENT / ⚠️ FIXED}
- File organization: {✅ CONSISTENT / ⚠️ FIXED}
- Import style: {✅ CONSISTENT / ⚠️ FIXED}
- Docstring style: {✅ CONSISTENT / ⚠️ FIXED}

### Naming Convention Consistency

- Variable names: {✅ CONSISTENT / ⚠️ FIXED}
- Abbreviations: {✅ CONSISTENT / ⚠️ FIXED}
- File naming: {✅ CONSISTENT / ⚠️ FIXED}

### Error Handling Consistency

- Error classes: {✅ CONSISTENT / ⚠️ FIXED}
- Error messages: {✅ CONSISTENT / ⚠️ FIXED}
- Logging levels: {✅ CONSISTENT / ⚠️ FIXED}

### Architectural Pattern Consistency

- Design patterns: {✅ CONSISTENT / ⚠️ FIXED}
- Data access: {✅ CONSISTENT / ⚠️ FIXED}
- Configuration: {✅ CONSISTENT / ⚠️ FIXED}

### Issues Found and Fixed

{List all issues with fixes applied}

**Issue 1:** Inconsistent function naming (get_ vs fetch_)
- Severity: MINOR
- Fix: Renamed all to use get_ prefix
- Tests re-run: ✅ 100% pass

**Issue 2:** Feature 03 not using Manager pattern
- Severity: MINOR
- Fix: Refactored to PerformanceManager class
- Tests re-run: ✅ 100% pass

[... more issues ...]

### Tests Re-Run After Fixes

**Command:** `python tests/run_all_tests.py`
**Result:** ✅ {N}/{N} tests passed (100%)

### Next Steps

{If all fixed:}
**Action:** Proceed to QC Round 3 (End-to-End Success Criteria)

{If critical issues:}
**Action:** Create bug fixes, RESTART Stage 6 from STAGE_6a
```

**If issues fixed inline:**
- Run unit tests to verify fixes: `python tests/run_all_tests.py`
- Verify 100% test pass rate
- Document fixes in findings
- Proceed to Round 3

**If critical issues found:**
- Create bug fixes for critical inconsistencies
- RESTART Stage 6 from STAGE_6a after fixes

---

## QC Round 3: End-to-End Success Criteria

**Objective:** Validate epic achieves original goals and meets all success criteria.

**Time Estimate:** 10-20 minutes

---

### Step 3.1: Validate Against Original Epic Request

**Re-read original {epic_name}.txt request:**

**Use Read tool to load the user's original epic request:**

**Example Request:**
```
Epic Request: Improve Draft Helper System

Goals:
1. Integrate ADP data for market wisdom
2. Add matchup-based projections
3. Track player performance vs projections

Expected Outcome:
User can make better draft decisions by seeing:
- Market consensus (ADP)
- Matchup difficulty
- Historical accuracy of projections

Success Criteria:
- ADP data visible in draft recommendations
- Matchup difficulty affects player scores
- Performance tracking persists across sessions
```

**Create validation table:**

| Original Goal | Achieved? | Evidence | Notes |
|---------------|-----------|----------|-------|
| Integrate ADP data | {✅ YES / ❌ NO} | Feature 01 implemented, ADP multipliers in output | {Any notes} |
| Add matchup projections | {✅ YES / ❌ NO} | Feature 02 implemented, difficulty shown in UI | {Any notes} |
| Track performance | {✅ YES / ❌ NO} | Feature 03 implemented, CSV persisted | {Any notes} |

**For EACH goal:**
1. **Read the goal from original request** (exact words)
2. **Verify implementation achieves goal** (test with real data)
3. **Check expected outcomes are delivered** (user can see results)
4. **Compare user's vision to actual implementation** (matches intent?)

**Document validation:**
```markdown
### Original Epic Request Validation

**Epic:** {epic_name}
**Original Request File:** {epic_name}.txt

**Goals Validation:**

**Goal 1: Integrate ADP data for market wisdom**
- Status: ✅ ACHIEVED
- Evidence:
  - Feature 01 (ADP Integration) fully implemented
  - ADP data loaded from FantasyPros CSV
  - Multipliers calculated and applied to player scores
  - ADP rank visible in draft recommendations UI
- User can see: Market consensus via ADP rank (1-500)

**Goal 2: Add matchup-based projections**
- Status: ✅ ACHIEVED
- Evidence:
  - Feature 02 (Matchup System) fully implemented
  - Matchup difficulty calculated for each player
  - Difficulty affects final scores (easy=1.1x, hard=0.8x)
  - Matchup info shown in recommendations
- User can see: Matchup difficulty (Easy/Medium/Hard)

**Goal 3: Track player performance vs projections**
- Status: ✅ ACHIEVED
- Evidence:
  - Feature 03 (Performance Tracker) fully implemented
  - Historical accuracy calculated and displayed
  - Performance data persisted to CSV
  - Accuracy trends visible in analysis mode
- User can see: Historical accuracy percentage

**Overall:** ✅ ALL GOALS ACHIEVED (3/3)
```

---

### Step 3.2: Verify Epic Success Criteria (from Stage 4)

**Re-read epic_smoke_test_plan.md "Epic Success Criteria" section:**

**Find success criteria:**
```markdown
## Epic Success Criteria

**Must Have (ALL REQUIRED):**
1. Draft recommendations include ADP multipliers
2. Matchup difficulty reflected in final scores
3. Performance tracking data persisted to CSV
4. Cross-feature integration: All 3 features work together
5. User can see all 3 data sources in output
6. Performance comparison shows accuracy trends
```

**⚠️ CRITICAL:** ALL success criteria are REQUIRED (100%). No "nice to have" or "optional" requirements.

**For EACH criterion:**

**Criterion 1: Draft recommendations include ADP multipliers**
- Test: Run draft mode, inspect output
- Expected: `adp_multiplier` field present with value 0.5-1.5
- Result: {✅ MET / ❌ NOT MET}
- Evidence: {Screenshot or data sample}

**Criterion 2: Matchup difficulty reflected in final scores**
- Test: Compare scores with/without matchup feature enabled
- Expected: Final score = base * adp_mult * matchup_mult
- Result: {✅ MET / ❌ NOT MET}
- Evidence: {Calculation verification}

**Criterion 3: Performance tracking data persisted to CSV**
- Test: Run draft, check for performance_log.csv
- Expected: CSV updated with latest selections
- Result: {✅ MET / ❌ NOT MET}
- Evidence: {CSV file exists and updated}

**Create validation table:**

| Criterion | Required? | Met? | Evidence |
|-----------|-----------|------|----------|
| 1. ADP in recommendations | ✅ YES | {✅/❌} | {Evidence} |
| 2. Matchup in scores | ✅ YES | {✅/❌} | {Evidence} |
| 3. Performance tracking CSV | ✅ YES | {✅/❌} | {Evidence} |
| 4. Cross-feature integration | ✅ YES | {✅/❌} | {Evidence} |
| 5. All data visible | ✅ YES | {✅/❌} | {Evidence} |
| 6. Accuracy trends | ✅ YES | {✅/❌} | {Evidence} |

**Document validation:**
```markdown
### Epic Success Criteria Validation

**Source:** epic_smoke_test_plan.md (Epic Success Criteria section)

**Criteria Met:** {M}/{N} ({percentage}%)

{For each criterion:}
**Criterion 1: Draft recommendations include ADP multipliers**
- Required: ✅ YES (from original epic request)
- Met: {✅ YES / ❌ NO}
- Evidence: Inspected output/draft_recommendations.csv, adp_multiplier field present
- Value range: 0.8-1.3 (expected: 0.5-1.5) ✅

**Overall:** {✅ ALL CRITERIA MET / ❌ FAILURES}

{If any criterion NOT met:}
**Unmet Criterion:** {Name}
- Why not met: {Explanation}
- Action: {Fix implementation / Get user approval to remove}
```

**If ANY criterion not met:**
- ❌ STOP - Success criteria are REQUIRED
- Determine if this can be fixed or if user approval needed to remove from scope
- If fixable → Create bug fix, RESTART Stage 6
- If user approval to remove → Document approval, update spec, continue

---

### Step 3.3: User Experience Flow Validation

**Execute COMPLETE user workflows:**

**Example User Workflow (Draft a QB for Week 5):**
```bash
# User Story: Draft a quarterback for Week 5

# Step 1: User runs command
python run_league_helper.py --mode draft --position QB --week 5

# Step 2: System displays rankings
# Expected output:
# Rank | Player          | ADP | Matchup  | Accuracy | Score
# 1    | Patrick Mahomes | 5   | Medium   | 85%      | 24.5
# 2    | Josh Allen      | 8   | Easy     | 82%      | 23.8
# 3    | Lamar Jackson   | 12  | Hard     | 80%      | 22.1

# Step 3: User selects player
# System provides recommendation with all data sources visible

# Step 4: Selection recorded in performance tracking
```

**Validation Questions:**

1. **Is workflow SMOOTH?**
   - ✅ No confusing steps
   - ✅ Clear instructions
   - ✅ Intuitive command structure

2. **Is output CLEAR?**
   - ✅ User understands all data
   - ✅ ADP rank clear ("5" means top 5)
   - ✅ Matchup difficulty clear (Easy/Medium/Hard)
   - ✅ Accuracy percentage clear (85% = reliable)

3. **Are errors HELPFUL?**
   - Test error scenario: Invalid week number
   - Expected: "Invalid week: 99. Please use 1-18."
   - ✅ Error explains what's wrong and how to fix

**Document validation:**
```markdown
### User Experience Flow Validation

**Workflow Tested:** Draft QB for Week 5

**User Steps:**
1. Run command: ✅ SMOOTH (clear syntax)
2. View rankings: ✅ CLEAR (all data visible and understandable)
3. Select player: ✅ INTUITIVE (numbered selection)
4. See results: ✅ COMPREHENSIVE (all features integrated)

**Output Clarity:**
- ADP data: ✅ CLEAR (rank + multiplier explained)
- Matchup data: ✅ CLEAR (difficulty + impact shown)
- Performance data: ✅ CLEAR (accuracy % + trend)

**Error Handling:**
- Invalid input: ✅ HELPFUL error messages
- Missing data: ✅ Clear degradation messages
- System errors: ✅ User-friendly (not stack traces)

**Overall UX:** ✅ SMOOTH AND CLEAR
```

---

### Step 3.4: Performance Characteristics

**Test performance with realistic data:**

**Performance Tests:**

**Test 1: Full Draft Recommendation (All Players, All Weeks)**
```bash
time python run_league_helper.py --mode draft --week 5

# Expected: < 5 seconds for full draft recommendation
# Actual: {time} seconds
# Status: {✅ ACCEPTABLE / ⚠️ SLOW / ❌ TOO SLOW}
```

**Test 2: Memory Usage**
```bash
# Monitor memory during full dataset processing
python -m memory_profiler run_league_helper.py --mode draft

# Expected: < 500MB for full dataset
# Actual: {memory} MB
# Status: {✅ ACCEPTABLE / ⚠️ HIGH / ❌ TOO HIGH}
```

**Test 3: Performance vs Baseline (Before Epic)**
```bash
# Compare performance before/after epic

# Before epic (baseline):
# Draft mode: 2.1 seconds
# Analysis mode: 1.5 seconds

# After epic:
# Draft mode: 3.2 seconds (1.1s slower) ← Acceptable? (52% increase)
# Analysis mode: 2.8 seconds (1.3s slower) ← Acceptable? (87% increase)

# Status: {✅ ACCEPTABLE / ⚠️ REGRESSION}
```

**Document validation:**
```markdown
### Performance Characteristics

**Tests Run:** 3

**Test 1: Full Draft Recommendation**
- Time: 3.2 seconds
- Expected: < 5 seconds
- Status: ✅ ACCEPTABLE

**Test 2: Memory Usage**
- Memory: 285 MB
- Expected: < 500 MB
- Status: ✅ ACCEPTABLE

**Test 3: Performance vs Baseline**
- Draft mode: 2.1s → 3.2s (+1.1s, +52%)
- Analysis mode: 1.5s → 2.8s (+1.3s, +87%)
- Status: ⚠️ REGRESSION (but still < 5s, acceptable)

**Overall Performance:** ✅ ACCEPTABLE
**Regressions:** ⚠️ NOTED (within acceptable limits)
```

---

### Step 3.5: Document QC Round 3 Findings

**Update epic_lessons_learned.md:**

```markdown
---

## Stage 6b - QC Round 3 Findings (End-to-End Success Criteria)

**Date:** {YYYY-MM-DD}
**Round:** 3 of 3
**Focus:** End-to-end success criteria validation

**Original Goals Validated:** {M}/{N}
**Success Criteria Met:** {K}/{L}
**Status:** {✅ PASSED / ❌ FAILURES}

### Original Epic Request Validation

**Epic:** {epic_name}

**Goals:**
- Goal 1 (Integrate ADP data): ✅ ACHIEVED
- Goal 2 (Add matchup projections): ✅ ACHIEVED
- Goal 3 (Track performance): ✅ ACHIEVED

**Overall:** ✅ ALL GOALS ACHIEVED ({N}/{N})

### Epic Success Criteria Validation

**Criteria:**
- Criterion 1 (ADP in recommendations): ✅ MET
- Criterion 2 (Matchup in scores): ✅ MET
- Criterion 3 (Performance tracking CSV): ✅ MET
- Criterion 4 (Cross-feature integration): ✅ MET
- Criterion 5 (All data visible): ✅ MET
- Criterion 6 (Accuracy trends): ✅ MET

**Overall:** ✅ ALL CRITERIA MET ({L}/{L})

**CRITICAL RULE VERIFIED:** All success criteria met 100% (no unimplemented requirements)

### User Experience Validation

- Workflow: ✅ SMOOTH
- Output: ✅ CLEAR
- Errors: ✅ HELPFUL

### Performance Validation

- Full draft: 3.2s (✅ < 5s target)
- Memory: 285 MB (✅ < 500 MB target)
- Regression: +52% slower (⚠️ noted, still acceptable)

### Next Steps

{If ALL PASSED:}
**Action:** Proceed to STAGE_6c (Epic Final Review)

{If ANY FAILURES:}
**Action:** {Fix issues / Get user approval / Create bug fixes}
```

---

## Completion Criteria

**STAGE_6b (Epic QC Rounds) is complete when ALL of these are true:**

### QC Round 1 Complete
- [ ] All integration points validated
- [ ] Data flow traced and verified
- [ ] Interface compatibility confirmed
- [ ] Error propagation tested
- [ ] Round 1 findings documented

### QC Round 2 Complete
- [ ] Code style consistency verified
- [ ] Naming conventions consistent
- [ ] Error handling consistent
- [ ] Architectural patterns consistent
- [ ] Round 2 findings documented
- [ ] Any minor issues fixed inline

### QC Round 3 Complete
- [ ] Original epic goals validated (ALL achieved)
- [ ] Success criteria validated (ALL met 100%)
- [ ] User experience flows validated
- [ ] Performance characteristics acceptable
- [ ] Round 3 findings documented

### All Findings Documented
- [ ] epic_lessons_learned.md updated with all 3 rounds
- [ ] Issues documented with severity and fixes
- [ ] Test results documented
- [ ] Next steps identified

### Agent Status Updated
- [ ] EPIC_README.md Agent Status shows STAGE_6b complete
- [ ] Next action: Transition to STAGE_6c
- [ ] No blockers

**If ANY item unchecked → STAGE_6b NOT complete**

**When ALL items checked:**
✅ STAGE_6b COMPLETE
→ Proceed to STAGE_6c (Epic Final Review)

---

## Common Mistakes to Avoid

```
┌─────────────────────────────────────────────────────────────┐
│ "If You're Thinking This, STOP" - Anti-Pattern Detection   │
└─────────────────────────────────────────────────────────────┘

❌ "Integration tests passed in smoke testing, I'll skip QC Round 1"
   ✅ STOP - QC Round 1 validates DEEPER than smoke tests

❌ "Code style is subjective, consistency doesn't matter"
   ✅ STOP - Consistency reduces cognitive load, REQUIRED

❌ "Minor naming inconsistency, I'll leave it"
   ✅ STOP - Fix ALL inconsistencies (minor issues don't require restart)

❌ "Success criterion is 95% met, close enough"
   ✅ STOP - ALL criteria must be 100% met (no partial credit)

❌ "Performance is 2x slower but still works, I'll proceed"
   ✅ STOP - Document regression, determine if acceptable

❌ "QC found issues but I'll proceed to Stage 6c anyway"
   ✅ STOP - Fix critical issues, RESTART Stage 6; fix minor issues inline

❌ "Original epic request is outdated, I'll skip that validation"
   ✅ STOP - MUST validate against original (proves epic delivers on promise)
```

---

## Next Stage

**After completing STAGE_6b:**

📖 **READ:** `STAGE_6c_epic_final_review_guide.md`
🎯 **GOAL:** Epic PR review, validation against original request, final verification
⏱️ **ESTIMATE:** 20-30 minutes

**Stage 6c will:**
- Epic PR review (11 categories applied to epic-wide changes)
- Final validation against original epic request
- Epic lessons learned capture
- Stage 6 completion verification
- Transition to Stage 7 (Epic Cleanup)

**Remember:** Use the phase transition prompt from `prompts_reference_v2.md` when starting STAGE_6c.

---

*End of STAGE_6b_epic_qc_rounds_guide.md*
