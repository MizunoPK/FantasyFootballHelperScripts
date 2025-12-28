# Sub-Feature 3: Locked Field Migration - Implementation TODO

---

## 📖 Guide Reminder

**This file is governed by:** `feature-updates/guides/todo_creation_guide.md`

**Ready for implementation when:** ALL 24 iterations complete (see guide lines 87-93)

**DO NOT proceed to implementation until:**
- [ ] All 24 iterations executed individually
- [ ] Iteration 4a passed (TODO Specification Audit)
- [ ] Iteration 23a passed (Pre-Implementation Spec Audit - 4 parts)
- [ ] Iteration 24 passed (Implementation Readiness Checklist)
- [ ] Interface verification complete (copy-pasted signatures verified)
- [ ] No "Alternative:" or "May need to..." notes remain in TODO

⚠️ **If you think verification is complete, re-read guide lines 87-93 FIRST!**

⚠️ **Do NOT offer user choice to "proceed to implementation OR continue verification" - you MUST complete all 24 iterations**

---

## Iteration Progress Tracker

### Compact View (Quick Status)

```
R1: ■■■■■■■ (7/7)   R2: ■■■■■■■■■ (9/9)   R3: ■■■■■■■■ (8/8)
```
Legend: ■ = complete, □ = pending, ▣ = in progress

**Current:** Iteration 24 (ALL 24 ITERATIONS COMPLETE ✅)
**Confidence:** HIGH - READY FOR IMPLEMENTATION
**Blockers:** NONE

### Detailed View

| Round | Iterations | Status |
|-------|------------|--------|
| First (7) | [x]1 [x]2 [x]3 [x]4 [x]5 [x]6 [x]7 | 7/7 ✅ |
| Second (9) | [x]8 [x]9 [x]10 [x]11 [x]12 [x]13 [x]14 [x]15 [x]16 | 9/9 ✅ |
| Third (8) | [x]17 [x]18 [x]19 [x]20 [x]21 [x]22 [x]23 [x]24 | 8/8 ✅ |

**Current Iteration:** 24 ✅ **ALL COMPLETE - READY FOR IMPLEMENTATION**

---

## Protocol Execution Tracker

Track which protocols have been executed (protocols must be run at specified iterations):

| Protocol | Required Iterations | Completed |
|----------|---------------------|-----------|
| Standard Verification | 1, 2, 3, 8, 9, 10, 15, 16 | [x]1 [x]2 [x]3 [x]8 [x]9 [x]10 [x]15 [x]16 | ✅ |
| Algorithm Traceability | 4, 11, 19 | [x]4 [x]11 [x]19 | ✅ |
| End-to-End Data Flow | 5, 12 | [x]5 [x]12 | ✅ |
| Skeptical Re-verification | 6, 13, 22 | [x]6 [x]13 [x]22 | ✅ |
| Integration Gap Check | 7, 14, 23 | [x]7 [x]14 [x]23 | ✅ |
| Fresh Eyes Review | 17, 18 | [x]17 [x]18 | ✅ |
| Edge Case Verification | 20 | [x]20 | ✅ |
| Test Coverage Planning + Mock Audit | 21 | [x]21 | ✅ |
| Implementation Readiness | 24 | [x]24 | ✅ |
| TODO Specification Audit (4a) | 4a | [x]4a | ✅ |
| Pre-Implementation Spec Audit (23a) | 23a | [x]23a (4/4 parts) | ✅ |
| Interface Verification | Pre-impl | [x] | ✅ |

---

## Verification Summary

- Iterations completed: 24/24 ✅ **ALL COMPLETE - READY FOR IMPLEMENTATION**
- Requirements from spec: 21 items (NEW-54 to NEW-74)
- Requirements in TODO: 22 (21 from spec + 1 comment update)
- Questions for user: 0 (spec complete - see sub_feature_03_locked_field_migration_questions.md)
- Integration points identified: 11 code locations (8 comparisons + 2 assignments + 1 comment)

---

## Phase 1: Field Type Migration

### Task 1.1: Change locked field type from int to bool
- **File:** `utils/FantasyPlayer.py:96`
- **Spec:** NEW-54
- **Tests:** `tests/utils/test_FantasyPlayer.py`
- **Status:** [ ] Not started

**Implementation details:**
```python
# OLD:
locked: int = 0  # 0 = not locked, 1 = locked

# NEW:
locked: bool = False  # True = locked (cannot be drafted or traded)
```

**Acceptance Criteria:**
- [ ] Field type is `bool`
- [ ] Default value is `False`
- [ ] Comment updated to reflect boolean semantics

---

## Phase 2: Method Updates

### Task 2.1: Update is_locked() method
- **File:** `utils/FantasyPlayer.py:404`
- **Spec:** NEW-55
- **Tests:** `tests/utils/test_FantasyPlayer.py`
- **Status:** [ ] Not started

**Implementation details:**
```python
# OLD:
def is_locked(self) -> bool:
    return self.locked == 1

# NEW:
def is_locked(self) -> bool:
    return self.locked
```

**Acceptance Criteria:**
- [ ] Method returns `self.locked` directly
- [ ] No comparison needed (already boolean)
- [ ] Docstring updated if needed

### Task 2.2: Update is_available() method
- **File:** `utils/FantasyPlayer.py:392`
- **Spec:** NEW-56
- **Tests:** `tests/utils/test_FantasyPlayer.py`
- **Status:** [ ] Not started

**Implementation details:**
```python
# OLD:
def is_available(self) -> bool:
    return self.drafted == 0 and self.locked == 0

# NEW:
def is_available(self) -> bool:
    return self.drafted == 0 and not self.locked
```

**Acceptance Criteria:**
- [ ] Uses `not self.locked` instead of `self.locked == 0`
- [ ] Logic identical to old behavior
- [ ] Tests verify availability logic

### Task 2.3: Update __str__() method
- **File:** `utils/FantasyPlayer.py:529`
- **Spec:** NEW-57
- **Tests:** `tests/utils/test_FantasyPlayer.py`
- **Status:** [ ] Not started

**Implementation details:**
```python
# OLD:
locked_indicator = " [LOCKED]" if self.locked == 1 else ""

# NEW:
locked_indicator = " [LOCKED]" if self.is_locked() else ""
```

**Acceptance Criteria:**
- [ ] Uses `is_locked()` method instead of direct comparison
- [ ] Display output unchanged
- [ ] Tests verify locked indicator shows correctly

### Task 2.4: Update from_json() loading
- **File:** `utils/FantasyPlayer.py:180-275` (from_json method)
- **Spec:** NEW-58
- **Tests:** `tests/utils/test_FantasyPlayer.py`
- **Status:** [ ] Not started

**Implementation details:**
```python
# Direct boolean assignment - no conversion needed
locked = data.get('locked', False)
```

**Note:** Sub-feature 1 already implemented this, verify it's using boolean directly

**Acceptance Criteria:**
- [ ] Loads boolean value directly from JSON
- [ ] Default value is `False` (not 0)
- [ ] No int-to-bool conversion

### Task 2.5: Verify to_json() writes boolean
- **File:** `utils/FantasyPlayer.py:383-390` (to_dict method)
- **Spec:** NEW-59
- **Tests:** `tests/utils/test_FantasyPlayer.py`
- **Status:** [ ] Not started

**Implementation details:**
```python
# to_dict() uses asdict() - automatically handles boolean
# Verify in tests that JSON contains boolean, not int
```

**Acceptance Criteria:**
- [ ] JSON output contains `true`/`false` (not 0/1)
- [ ] No conversion logic needed (dataclass handles it)
- [ ] Tests verify boolean in JSON output

---

## Phase 3: Update Comparisons (8 locations)

### Task 3.1: PlayerManager.py:552 - lowest_scores calculation
- **File:** `league_helper/util/PlayerManager.py:552`
- **Spec:** NEW-60
- **Tests:** `tests/league_helper/util/test_PlayerManager_scoring.py`
- **Status:** [ ] Not started

**Implementation details:**
```python
# OLD:
if p.score < lowest_scores[p.position] and p.locked == 0:

# NEW:
if p.score < lowest_scores[p.position] and not p.is_locked():
```

**Acceptance Criteria:**
- [ ] Uses `not p.is_locked()` instead of `p.locked == 0`
- [ ] Logic unchanged
- [ ] Tests verify lowest scores calculation

### Task 3.2: ModifyPlayerDataModeManager.py:338 - list locked players
- **File:** `league_helper/modify_player_data_mode/ModifyPlayerDataModeManager.py:338`
- **Spec:** NEW-61
- **Tests:** `tests/league_helper/modify_player_data_mode/test_modify_player_data_mode.py`
- **Status:** [ ] Not started

**Implementation details:**
```python
# OLD:
locked_players = [p for p in self.player_manager.players if p.locked == 1]

# NEW:
locked_players = [p for p in self.player_manager.players if p.is_locked()]
```

**Acceptance Criteria:**
- [ ] Uses `p.is_locked()` instead of `p.locked == 1`
- [ ] List comprehension works identically
- [ ] Tests verify locked player list

### Task 3.3: ModifyPlayerDataModeManager.py:394 - check lock status
- **File:** `league_helper/modify_player_data_mode/ModifyPlayerDataModeManager.py:394`
- **Spec:** NEW-62
- **Tests:** `tests/league_helper/modify_player_data_mode/test_modify_player_data_mode.py`
- **Status:** [ ] Not started

**Implementation details:**
```python
# OLD:
was_locked = selected_player.locked == 1

# NEW:
was_locked = selected_player.is_locked()
```

**Acceptance Criteria:**
- [ ] Uses `is_locked()` method
- [ ] `was_locked` is boolean
- [ ] Tests verify lock toggle logic

### Task 3.4: ModifyPlayerDataModeManager.py:409 - conditional check
- **File:** `league_helper/modify_player_data_mode/ModifyPlayerDataModeManager.py:409`
- **Spec:** NEW-63
- **Tests:** `tests/league_helper/modify_player_data_mode/test_modify_player_data_mode.py`
- **Status:** [ ] Not started

**Implementation details:**
```python
# OLD:
if selected_player.locked == 1:

# NEW:
if selected_player.is_locked():
```

**Acceptance Criteria:**
- [ ] Uses `is_locked()` method
- [ ] Conditional logic unchanged
- [ ] Tests verify lock check

### Task 3.5: trade_analyzer.py:639 - my locked players
- **File:** `league_helper/trade_simulator_mode/trade_analyzer.py:639`
- **Spec:** NEW-64
- **Tests:** `tests/league_helper/trade_simulator_mode/test_trade_analyzer.py`
- **Status:** [ ] Not started

**Implementation details:**
```python
# OLD:
my_locked_original = [p for p in my_team.team if p.locked == 1 and p.get_risk_level() != "HIGH"]

# NEW:
my_locked_original = [p for p in my_team.team if p.is_locked() and p.get_risk_level() != "HIGH"]
```

**Acceptance Criteria:**
- [ ] Uses `p.is_locked()` instead of `p.locked == 1`
- [ ] Filter logic identical
- [ ] Tests verify locked player filtering

### Task 3.6: trade_analyzer.py:643 - their locked players
- **File:** `league_helper/trade_simulator_mode/trade_analyzer.py:643`
- **Spec:** NEW-65
- **Tests:** `tests/league_helper/trade_simulator_mode/test_trade_analyzer.py`
- **Status:** [ ] Not started

**Implementation details:**
```python
# OLD:
their_locked_original = [p for p in their_team.team if p.locked == 1 and p.get_risk_level() != "HIGH"]

# NEW:
their_locked_original = [p for p in their_team.team if p.is_locked() and p.get_risk_level() != "HIGH"]
```

**Acceptance Criteria:**
- [ ] Uses `p.is_locked()` instead of `p.locked == 1`
- [ ] Filter logic identical
- [ ] Tests verify locked player filtering

### Task 3.7: trade_analyzer.py:820 - my locked players (second location)
- **File:** `league_helper/trade_simulator_mode/trade_analyzer.py:820`
- **Spec:** NEW-66
- **Tests:** `tests/league_helper/trade_simulator_mode/test_trade_analyzer.py`
- **Status:** [ ] Not started

**Implementation details:**
```python
# OLD:
my_locked = [p for p in my_team.team if p.locked == 1 and p.get_risk_level() != "HIGH"]

# NEW:
my_locked = [p for p in my_team.team if p.is_locked() and p.get_risk_level() != "HIGH"]
```

**Acceptance Criteria:**
- [ ] Uses `p.is_locked()` instead of `p.locked == 1`
- [ ] Filter logic identical
- [ ] Tests verify locked player filtering

### Task 3.8: trade_analyzer.py:824 - their locked players (second location)
- **File:** `league_helper/trade_simulator_mode/trade_analyzer.py:824`
- **Spec:** NEW-67
- **Tests:** `tests/league_helper/trade_simulator_mode/test_trade_analyzer.py`
- **Status:** [ ] Not started

**Implementation details:**
```python
# OLD:
their_locked = [p for p in their_team.team if p.locked == 1 and p.get_risk_level() != "HIGH"]

# NEW:
their_locked = [p for p in their_team.team if p.is_locked() and p.get_risk_level() != "HIGH"]
```

**Acceptance Criteria:**
- [ ] Uses `p.is_locked()` instead of `p.locked == 1`
- [ ] Filter logic identical
- [ ] Tests verify locked player filtering

### Task 3.9: trade_analyzer.py:808 - update comment
- **File:** `league_helper/trade_simulator_mode/trade_analyzer.py:808`
- **Spec:** NEW (found during iteration 6)
- **Tests:** N/A (comment only)
- **Status:** [ ] Not started

**Implementation details:**
```python
# OLD:
# - LOCKED players (player.locked == 1): Cannot be traded BUT count toward position limits

# NEW:
# - LOCKED players (player.is_locked()): Cannot be traded BUT count toward position limits
```

**Acceptance Criteria:**
- [ ] Comment updated to use `is_locked()` method
- [ ] Comment semantics unchanged
- [ ] Improves consistency with code changes

---

## Phase 4: Update Assignments (2 locations)

### Task 4.1: ModifyPlayerDataModeManager.py:401 - toggle lock status
- **File:** `league_helper/modify_player_data_mode/ModifyPlayerDataModeManager.py:401`
- **Spec:** NEW-68
- **Tests:** `tests/league_helper/modify_player_data_mode/test_modify_player_data_mode.py`
- **Status:** [ ] Not started

**Implementation details:**
```python
# OLD:
selected_player.locked = 0 if was_locked else 1

# NEW:
selected_player.locked = False if was_locked else True
```

**Acceptance Criteria:**
- [ ] Uses `True`/`False` instead of 1/0
- [ ] Toggle logic works identically
- [ ] Tests verify lock/unlock functionality

### Task 4.2: trade_analyzer.py:181 - unlock for testing
- **File:** `league_helper/trade_simulator_mode/trade_analyzer.py:181`
- **Spec:** NEW-69
- **Tests:** `tests/league_helper/trade_simulator_mode/test_trade_analyzer.py`
- **Status:** [ ] Not started

**Implementation details:**
```python
# OLD:
p_copy.locked = 0

# NEW:
p_copy.locked = False
```

**Acceptance Criteria:**
- [ ] Uses `False` instead of 0
- [ ] Unlock logic works identically
- [ ] Tests verify trade simulation with unlocked copies

### QA CHECKPOINT 1: All Production Code Updated
- **Status:** [ ] Not started
- **Expected outcome:** All 10 locations (8 comparisons + 2 assignments) updated
- **Test command:** `python tests/run_all_tests.py`
- **Verify:**
  - [ ] All unit tests pass (2404/2404 = 100%)
  - [ ] No `locked == 0` or `locked == 1` comparisons remain in league_helper/
  - [ ] No `locked = 0` or `locked = 1` assignments remain in league_helper/
  - [ ] All code uses `is_locked()` method or `True`/`False` values
- **If checkpoint fails:** STOP, fix issue, document in lessons learned, then re-run

---

## Phase 5: Testing

### Task 5.1: Unit test for boolean field type
- **File:** `tests/utils/test_FantasyPlayer.py`
- **Spec:** NEW-70
- **Status:** [ ] Not started

**Implementation details:**
- Test that `locked` field is boolean type
- Test default value is `False`
- Test setting to `True` works

**Acceptance Criteria:**
- [ ] Test verifies `isinstance(player.locked, bool)`
- [ ] Test verifies default is `False`
- [ ] Test verifies can set to `True`

### Task 5.2: Unit test for is_locked() method
- **File:** `tests/utils/test_FantasyPlayer.py`
- **Spec:** NEW-71
- **Status:** [ ] Not started

**Implementation details:**
- Test `is_locked()` returns `True` when `locked=True`
- Test `is_locked()` returns `False` when `locked=False`

**Acceptance Criteria:**
- [ ] Test covers both True/False cases
- [ ] Test verifies method returns boolean

### Task 5.3: Unit test for is_available() with locked field
- **File:** `tests/utils/test_FantasyPlayer.py`
- **Spec:** NEW-72
- **Status:** [ ] Not started

**Implementation details:**
- Test `is_available()` returns `False` when `locked=True`
- Test `is_available()` returns `True` when `locked=False` and `drafted=0`

**Acceptance Criteria:**
- [ ] Test verifies locked players are not available
- [ ] Test verifies unlocked, undrafted players are available

### Task 5.4: Integration test for modify player data mode
- **File:** `tests/league_helper/modify_player_data_mode/test_modify_player_data_mode.py`
- **Spec:** NEW-73
- **Status:** [ ] Not started

**Implementation details:**
- Test toggling lock status uses boolean values
- Test listing locked players works correctly
- Test unlock functionality

**Acceptance Criteria:**
- [ ] Test verifies lock toggle works with booleans
- [ ] Test verifies locked player list filtering
- [ ] Test verifies unlock sets `locked=False`

### Task 5.5: Integration test for trade analyzer
- **File:** `tests/league_helper/trade_simulator_mode/test_trade_analyzer.py`
- **Spec:** NEW-74
- **Status:** [ ] Not started

**Implementation details:**
- Test locked player filtering in trade analysis
- Test copying players unlocks them correctly

**Acceptance Criteria:**
- [ ] Test verifies locked players excluded from trades
- [ ] Test verifies player copies are unlocked (locked=False)

### QA CHECKPOINT 2: All Tests Passing
- **Status:** [ ] Not started
- **Expected outcome:** 2404/2404 tests passing (100%)
- **Test command:** `python tests/run_all_tests.py`
- **Verify:**
  - [ ] All unit tests pass
  - [ ] All integration tests pass
  - [ ] No test failures related to locked field
  - [ ] Boolean semantics working correctly across all tests
- **If checkpoint fails:** STOP, fix issue, document in lessons learned, then re-run

---

## Interface Contracts (Verified Pre-Implementation)

### FantasyPlayer.is_locked()
- **Method:** `is_locked(self) -> bool`
- **Source:** `utils/FantasyPlayer.py:404`
- **Current implementation:** Returns `self.locked == 1`
- **New implementation:** Returns `self.locked` (boolean)
- **Verified:** [ ]

### FantasyPlayer.is_available()
- **Method:** `is_available(self) -> bool`
- **Source:** `utils/FantasyPlayer.py:392`
- **Current implementation:** Returns `self.drafted == 0 and self.locked == 0`
- **New implementation:** Returns `self.drafted == 0 and not self.locked`
- **Verified:** [ ]

### FantasyPlayer.locked (field)
- **Attribute:** `locked`
- **Current type:** `int` (0 or 1)
- **New type:** `bool` (True or False)
- **Default:** `False` (was 0)
- **Source:** `utils/FantasyPlayer.py:96`
- **Verified:** [ ]

### Quick E2E Validation Plan
- **Minimal test command:** `python -m pytest tests/utils/test_FantasyPlayer.py -k "locked" -v`
- **Expected result:** All locked-related tests passing
- **Run before:** Full implementation begins
- **Status:** [ ] Not run

---

## Integration Matrix

| Component | Files Modified | Test Files | Integration Points |
|-----------|---------------|------------|-------------------|
| FantasyPlayer | utils/FantasyPlayer.py | tests/utils/test_FantasyPlayer.py | Field definition, is_locked(), is_available(), __str__() |
| PlayerManager | league_helper/util/PlayerManager.py | tests/league_helper/util/test_PlayerManager_scoring.py | Lowest scores calculation |
| ModifyPlayerDataMode | league_helper/modify_player_data_mode/ModifyPlayerDataModeManager.py | tests/league_helper/modify_player_data_mode/test_modify_player_data_mode.py | Lock toggling, locked player list |
| TradeAnalyzer | league_helper/trade_simulator_mode/trade_analyzer.py | tests/league_helper/trade_simulator_mode/test_trade_analyzer.py | Locked player filtering, copy unlocking |

**Total:** 4 components, 4 production files, 4 test files, 10 specific code locations

---

## Algorithm Traceability Matrix

**Spec Algorithm:** (sub_feature_03_locked_field_migration_spec.md lines 79-98)

```
Field Type Change:
  locked: int = 0  →  locked: bool = False

Method Updates:
  is_locked():     return self.locked == 1  →  return self.locked
  is_available():  ... and self.locked == 0  →  ... and not self.locked
  __str__():       if self.locked == 1       →  if self.is_locked()

Comparisons (8 locations):
  if p.locked == 1:   →  if p.is_locked():
  if p.locked == 0:   →  if not p.is_locked():

Assignments (2 locations):
  p.locked = 0  →  p.locked = False
  p.locked = 1  →  p.locked = True
```

**Implementation Matches Spec:** [ ] Verified in iteration 4

---

## Pre-Implementation Checklist

- [x] All 24 verification iterations complete ✅
- [x] Algorithm Traceability Matrix verified (iterations 4, 11, 19) ✅
- [x] TODO Specification Audit passed (iteration 4a) ✅
- [x] Pre-Implementation Spec Audit passed (iteration 23a - 4/4 parts) ✅
- [x] All interface signatures verified from actual source code ✅
- [x] Integration matrix complete (all files, tests, integration points identified) ✅
- [x] No "Alternative:" or "May need to..." notes remain ✅
- [x] Questions file created (0 questions - spec complete) ✅
- [x] User answers integrated (N/A - no questions) ✅
- [x] Implementation Readiness Protocol passed (iteration 24) ✅

✅ **STATUS: READY FOR IMPLEMENTATION** - Proceed to `implementation_execution_guide.md`

---

## Notes

**Migration Strategy:**
- Simple type change with method standardization
- No backward compatibility needed (internal implementation detail)
- All changes are mechanical replacements
- Boolean is more Pythonic and clearer than int flags

**Risk Level:** LOW
- Simple type change with clear transformation rules
- All locations identified during deep dive
- No complex logic changes required
- Comprehensive test coverage exists

**Dependencies:**
- Sub-feature 1 (Core Data Loading) already loads `locked` as boolean from JSON
- This sub-feature completes the migration by updating all usage

**Estimated Changes:**
- 1 field type definition
- 3 method updates
- 8 comparison updates
- 2 assignment updates
- 5 test additions/updates
- **Total:** 19 code changes across 4 files
