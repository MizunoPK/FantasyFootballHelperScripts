# Sub-Feature 7: DraftedRosterManager Consolidation - Implementation Checklist

**Instructions**: Check off EACH requirement as you implement it. Do NOT batch-check.

## From Spec & Traceability Matrix:

### Phase 1: PlayerManager Methods

- [x] NEW-124: Add get_players_by_team() method to PlayerManager
      Spec: lines 29-38
      Implementation: PlayerManager.py lines 1024-1065 (42 lines)
      Verified: [x] Matches spec exactly (with critical fix: self.players)

- [x] NEW-125: Add comprehensive docstrings
      Spec: lines 29-38
      Implementation: Part of get_players_by_team() method
      Verified: [x] Google Style, includes examples

- [x] NEW-126: Add error handling
      Spec: Defensive programming
      Implementation: if not self.players check
      Verified: [x] Returns {}, logs warning

### Phase 2: TradeSimulator Updates

- [x] NEW-127: Remove DraftedRosterManager import
      Spec: lines 40-50
      Implementation: TradeSimulatorModeManager.py line 45 (removed)
      Verified: [x] Line deleted, no other imports

- [x] NEW-128: Simplify _initialize_team_data() method
      Spec: lines 40-50
      Implementation: TradeSimulatorModeManager.py lines 202-210
      Verified: [x] 11 lines → 1 line

- [x] NEW-129: Update docstrings
      Spec: lines 40-50
      Implementation: Class and method docstrings (3 locations)
      Verified: [x] No CSV references remain

### Phase 3: Deprecation

- [x] NEW-130: Add module deprecation notice
      Spec: lines 52-60
      Implementation: DraftedRosterManager.py lines 1-38
      Verified: [x] Migration path clear

- [x] NEW-131: Add method deprecation warnings
      Spec: lines 52-60
      Implementation: __init__, load_drafted_data, get_players_by_team, apply_drafted_state_to_players
      Verified: [x] warnings.warn() with stacklevel=2

### Phase 4: Testing

- [x] NEW-132: Unit tests for get_players_by_team()
      Spec: Testing strategy
      Implementation: test_PlayerManager_scoring.py (9 new tests)
      Verified: [x] All edge cases covered (92/92 passing)

- [x] NEW-133: Integration tests (TradeSimulator)
      Spec: Testing strategy
      Implementation: test_trade_simulator.py (54 tests)
      Verified: [x] Mocks + real objects (54/54 passing)

- [x] NEW-134: End-to-end integration test
      Spec: Testing strategy
      Implementation: test_league_helper_integration.py (2 E2E tests)
      Verified: [x] Real objects, tmp_path, JSON (25/25 passing)

- [x] NEW-135: Test file deprecation notice
      Spec: Testing strategy
      Implementation: test_DraftedRosterManager.py
      Verified: [x] Notice added, tests pass (58/58 passing)

## Verification Log:

| Requirement | Spec Location | Implementation | Verified? | Matches Spec? | Notes |
|-------------|---------------|----------------|-----------|---------------|-------|
| NEW-124 | spec:29-38 | PlayerManager.py:1024-1065 | [x] | [x] | Critical fix: self.players |
| NEW-125 | spec:29-38 | PlayerManager.py:1024-1065 | [x] | [x] | Google Style docstrings |
| NEW-126 | spec:defensive | PlayerManager.py:1030-1032 | [x] | [x] | Graceful degradation |
| NEW-127 | spec:40-50 | TradeSimulator.py:45 (removed) | [x] | [x] | Import deleted |
| NEW-128 | spec:40-50 | TradeSimulator.py:202-210 | [x] | [x] | 11 lines → 1 line |
| NEW-129 | spec:40-50 | TradeSimulator.py (3 locations) | [x] | [x] | No CSV references |
| NEW-130 | spec:52-60 | DraftedRosterManager.py:1-38 | [x] | [x] | Migration guide clear |
| NEW-131 | spec:52-60 | DraftedRosterManager.py (4 methods) | [x] | [x] | DeprecationWarning added |
| NEW-132 | spec:testing | test_PlayerManager.py | [x] | [x] | 9 tests, all edge cases |
| NEW-133 | spec:testing | test_trade_simulator.py | [x] | [x] | 54 tests passing |
| NEW-134 | spec:testing | test_integration.py | [x] | [x] | 2 E2E tests passing |
| NEW-135 | spec:testing | test_DraftedRoster.py | [x] | [x] | Deprecation notice added |

## Continuous Verification (Check every 5-10 minutes):

- [x] "Did I consult specs.md in last 5 minutes?"
- [x] "Can I point to exact spec line this code satisfies?"
- [x] "Working from documentation, not memory?"
- [x] "Checked off requirement in implementation checklist?"

**Last Updated:** 2025-12-29 (Implementation complete - QC Rounds 1-3 PASSED)
