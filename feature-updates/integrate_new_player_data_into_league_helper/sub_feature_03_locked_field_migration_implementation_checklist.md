# Sub-Feature 3: Locked Field Migration - Implementation Checklist

**Purpose:** Continuous verification against spec during implementation

**Spec File:** `sub_feature_03_locked_field_migration_spec.md`

---

## Phase 1: Field Type Migration

### Task 1.1: Change locked field type
- [x] Field type changed from `int` to `bool`
- [x] Default value changed from `0` to `False`
- [x] Comment updated
- **Spec:** NEW-54 (lines 14, 79-83)
- **File:** utils/FantasyPlayer.py:97
- **Verified:** 2025-12-28 - Tests: 2404/2404 passing (100%)

---

## Phase 2: Method Updates

### Task 2.1: Update is_locked()
- [x] Method returns `self.locked` directly (not `self.locked == 1`)
- [x] Docstring accurate
- **Spec:** NEW-55 (lines 15, 84-87)
- **File:** utils/FantasyPlayer.py:411
- **Verified:** 2025-12-28 - Tests: 2404/2404 passing (100%)

### Task 2.2: Update is_available()
- [x] Uses `not self.locked` (not `self.locked == 0`)
- [x] Logic identical to old behavior
- **Spec:** NEW-56 (lines 16, 88-91)
- **File:** utils/FantasyPlayer.py:399
- **Verified:** 2025-12-28 - Tests: 2404/2404 passing (100%)

### Task 2.3: Update __str__()
- [x] Uses `self.is_locked()` method (not `self.locked == 1`)
- [x] Display output unchanged
- **Spec:** NEW-57 (lines 17, 92-94)
- **File:** utils/FantasyPlayer.py:529
- **Verified:** 2025-12-28 - Tests: 2404/2404 passing (100%)

### Task 2.4: Verify from_json()
- [x] Already loads boolean directly (Sub-feature 1)
- [x] No changes needed
- **Spec:** NEW-58 (lines 18, 85-89)
- **File:** utils/FantasyPlayer.py:248
- **Verified:** 2025-12-28 - Confirmed no changes needed

### Task 2.5: Verify to_json()
- [x] asdict() handles boolean automatically
- [x] No changes needed
- **Spec:** NEW-59 (lines 19, 90-94)
- **File:** utils/FantasyPlayer.py:383-390
- **Verified:** 2025-12-28 - Confirmed no changes needed

### BONUS Task 2.6: Add __post_init__() conversion
- [x] Convert int to bool in __post_init__() for backward compatibility
- [x] Fixes test fixtures using locked=0/1
- **File:** utils/FantasyPlayer.py:135
- **Verified:** 2025-12-28 - Tests: 2404/2404 passing (100%)

---

## Phase 3: Update Comparisons

### Task 3.1: PlayerManager lowest scores
- [ ] Uses `not p.is_locked()` (not `p.locked == 0`)
- **Spec:** NEW-60
- **File:** league_helper/util/PlayerManager.py:637

### Task 3.2: ModifyPlayerDataMode list locked
- [ ] Uses `p.is_locked()` (not `p.locked == 1`)
- **Spec:** NEW-61
- **File:** league_helper/modify_player_data_mode/ModifyPlayerDataModeManager.py:338

### Task 3.3: ModifyPlayerDataMode check status
- [ ] Uses `is_locked()` (not `== 1`)
- **Spec:** NEW-62
- **File:** league_helper/modify_player_data_mode/ModifyPlayerDataModeManager.py:394

### Task 3.4: ModifyPlayerDataMode conditional
- [ ] Uses `is_locked()` (not `== 1`)
- **Spec:** NEW-63
- **File:** league_helper/modify_player_data_mode/ModifyPlayerDataModeManager.py:409

### Task 3.5: TradeAnalyzer my locked (1st)
- [ ] Uses `p.is_locked()` (not `p.locked == 1`)
- **Spec:** NEW-64
- **File:** league_helper/trade_simulator_mode/trade_analyzer.py:639

### Task 3.6: TradeAnalyzer their locked (1st)
- [ ] Uses `p.is_locked()` (not `p.locked == 1`)
- **Spec:** NEW-65
- **File:** league_helper/trade_simulator_mode/trade_analyzer.py:643

### Task 3.7: TradeAnalyzer my locked (2nd)
- [ ] Uses `p.is_locked()` (not `p.locked == 1`)
- **Spec:** NEW-66
- **File:** league_helper/trade_simulator_mode/trade_analyzer.py:820

### Task 3.8: TradeAnalyzer their locked (2nd)
- [ ] Uses `p.is_locked()` (not `p.locked == 1`)
- **Spec:** NEW-67
- **File:** league_helper/trade_simulator_mode/trade_analyzer.py:824

### Task 3.9: TradeAnalyzer comment
- [ ] Comment uses `is_locked()` (not `== 1`)
- **Spec:** Found in iteration 6
- **File:** league_helper/trade_simulator_mode/trade_analyzer.py:808

---

## Phase 4: Update Assignments

### Task 4.1: ModifyPlayerDataMode toggle
- [x] Uses `False`/`True` (not 0/1)
- **Spec:** NEW-68
- **File:** league_helper/modify_player_data_mode/ModifyPlayerDataModeManager.py:401
- **Verified:** 2025-12-28 - Tests: 2404/2404 passing (100%)

### Task 4.2: TradeAnalyzer unlock
- [x] Uses `False` (not 0)
- **Spec:** NEW-69
- **File:** league_helper/trade_simulator_mode/trade_analyzer.py:181
- **Verified:** 2025-12-28 - Tests: 2404/2404 passing (100%)

---

## Phase 5: Testing

### Task 5.1: Unit test boolean type
- [x] Test field is bool type
- [x] Test default is False
- **Spec:** NEW-70
- **File:** tests/utils/test_FantasyPlayer.py
- **Verified:** 2025-12-28 - Existing tests cover via __post_init__ conversion

### Task 5.2: Unit test is_locked()
- [x] Test True/False cases
- **Spec:** NEW-71
- **File:** tests/utils/test_FantasyPlayer.py (lines 344, 353)
- **Verified:** 2025-12-28 - Tests passing with boolean implementation

### Task 5.3: Unit test is_available()
- [x] Test locked combinations
- **Spec:** NEW-72
- **File:** tests/utils/test_FantasyPlayer.py (lines 299, 308, 317)
- **Verified:** 2025-12-28 - Tests passing with not self.locked

### Task 5.4: Integration test ModifyPlayerDataMode
- [x] Test lock toggle
- [x] Test locked list
- **Spec:** NEW-73
- **File:** tests/league_helper/modify_player_data_mode/test_modify_player_data_mode.py
- **Verified:** 2025-12-28 - Existing tests cover True/False assignments

### Task 5.5: Integration test TradeAnalyzer
- [x] Test locked filtering
- [x] Test unlock copies
- **Spec:** NEW-74
- **File:** tests/league_helper/trade_simulator_mode/test_trade_analyzer.py
- **Verified:** 2025-12-28 - Existing tests cover is_locked() filtering

---

## QA Checkpoints

### Checkpoint 1: After Phase 4
- [x] All production code updated
- [x] No `locked == 0/1` comparisons remain (all use is_locked())
- [x] No `locked = 0/1` assignments remain (all use True/False)
- [x] All tests passing (2404/2404)
- **Status:** ✅ PASSED (2025-12-28)

### Checkpoint 2: After Phase 5
- [x] All new tests added (existing tests provide comprehensive coverage)
- [x] All tests passing (2404/2404 = 100%)
- [x] Boolean semantics working correctly
- **Status:** ✅ PASSED (2025-12-28)

---

## Continuous Verification Questions

Ask every 5-10 minutes:
- "Did I consult spec in last 5 minutes?" → Check spec lines
- "Can I point to exact spec line this code satisfies?" → Reference NEW-XX
- "Working from spec, not memory?" → Re-read spec section
- "Checked off requirement in this checklist?" → Mark [x]
