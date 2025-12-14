# Always Show Calculated Projection - Implementation TODO

## Iteration Progress Tracker

| Round | Iterations | Status |
|-------|------------|--------|
| First (7) | [ ]1 [ ]2 [ ]3 [ ]4 [ ]5 [ ]6 [ ]7 | 0/7 |
| Second (9) | [ ]8 [ ]9 [ ]10 [ ]11 [ ]12 [ ]13 [ ]14 [ ]15 [ ]16 | 0/9 |
| Third (8) | [ ]17 [ ]18 [ ]19 [ ]20 [ ]21 [ ]22 [ ]23 [ ]24 | 0/8 |

**Current Iteration:** 1

---

## Protocol Execution Tracker

| Protocol | Required Iterations | Completed |
|----------|---------------------|-----------|
| Standard Verification | 1, 2, 3, 8, 9, 10, 15, 16 | |
| Algorithm Traceability | 4, 11, 19 | |
| End-to-End Data Flow | 5, 12 | |
| Skeptical Re-verification | 6, 13, 22 | |
| Integration Gap Check | 7, 14, 23 | |
| Fresh Eyes Review | 17, 18 | |
| Edge Case Verification | 20 | |
| Test Coverage Planning | 21 | |
| Implementation Readiness | 24 | |

---

## Verification Summary

- Iterations completed: 0/24
- Requirements from spec: 3 main tasks
- Questions for user: 0 (all resolved in planning)
- Integration points identified: 2 (ScoredPlayer creation, __str__ display)
- Test files to update: ~1 test file (test_ScoredPlayer.py or similar)

---

## Phase 1: ScoredPlayer Changes

### Task 1.1: Add `projected_points` field to ScoredPlayer.__init__()
- **File:** `league_helper/util/ScoredPlayer.py`
- **Location:** Line 32 (`__init__` method)
- **Status:** [ ] Not started

**Current signature:**
```python
def __init__(self, player : FantasyPlayer, score : float, reasons : List[str] = []):
```

**New signature:**
```python
def __init__(self, player : FantasyPlayer, score : float, projected_points : float = 0.0, reasons : List[str] = []):
```

**Note:** Default value of 0.0 is REQUIRED for backward compatibility with:
- ReserveAssessmentModeManager.py:377 (creates ScoredPlayer without projection)
- 80+ test instantiations that don't provide projection

**Add storage:**
```python
self.projected_points = projected_points
```

### Task 1.2: Update ScoredPlayer.__str__() to show projection
- **File:** `league_helper/util/ScoredPlayer.py`
- **Location:** Lines 64-89 (`__str__` method)
- **Status:** [ ] Not started

**Current format:**
```python
header = f"[{self.player.position}] [{self.player.team}] {self.player.name} - {self.score:.2f} pts (Bye={self.player.bye_week})"
```

**New format (conditional - only when projection > 0):**
```python
if self.projected_points > 0:
    header = f"[{self.player.position}] [{self.player.team}] {self.player.name} - {self.projected_points:.2f} pts (Score: {self.score:.2f}) (Bye={self.player.bye_week})"
else:
    # Keep old format for backward compatibility
    header = f"[{self.player.position}] [{self.player.team}] {self.player.name} - {self.score:.2f} pts (Bye={self.player.bye_week})"
```

---

## Phase 2: PlayerScoringCalculator Changes

### Task 2.1: Capture orig_pts in score_player()
- **File:** `league_helper/util/player_scoring.py`
- **Location:** Lines 369-371 (Step 1 in score_player)
- **Status:** [ ] Not started

**Current:**
```python
player_score, reason = self._get_normalized_fantasy_points(p, use_weekly_projection)
```

**Change to:**
```python
player_score, reason, orig_pts = self._get_normalized_fantasy_points(p, use_weekly_projection)
```

### Task 2.2: Update _get_normalized_fantasy_points() to return orig_pts
- **File:** `league_helper/util/player_scoring.py`
- **Location:** Lines 456-475 (`_get_normalized_fantasy_points` method)
- **Status:** [ ] Not started

**Current return:**
```python
return weighted_pts, reason
```

**New return:**
```python
return weighted_pts, reason, orig_pts
```

### Task 2.3: Pass projected_points when creating ScoredPlayer
- **File:** `league_helper/util/player_scoring.py`
- **Location:** Line 454
- **Status:** [ ] Not started

**Current:**
```python
return ScoredPlayer(p, player_score, reasons)
```

**New:**
```python
return ScoredPlayer(p, player_score, orig_pts, reasons)
```

---

## Phase 3: Test Updates

### Task 3.1: Update ScoredPlayer tests
- **File:** `tests/league_helper/util/test_ScoredPlayer.py` (or similar)
- **Status:** [ ] Not started

**Changes needed:**
- Update test fixtures that create ScoredPlayer to include `projected_points`
- Add tests for new `__str__` format
- Verify projected_points field is stored correctly

### Task 3.2: Update player_scoring tests
- **File:** `tests/league_helper/util/test_player_scoring.py`
- **Status:** [ ] Not started

**Changes needed:**
- Update tests that check ScoredPlayer creation
- Verify orig_pts is passed correctly

---

## Integration Matrix

| New Component | File | Called By | Caller File:Line | Caller Modification Task |
|---------------|------|-----------|------------------|--------------------------|
| `projected_points` param in ScoredPlayer | ScoredPlayer.py | score_player() | player_scoring.py:454 | Task 2.3 |
| `orig_pts` return from _get_normalized_fantasy_points | player_scoring.py | score_player() | player_scoring.py:370 | Task 2.1 |

---

## Algorithm Traceability Matrix

| Spec Section | Algorithm Description | Code Location | Conditional Logic |
|--------------|----------------------|---------------|-------------------|
| Q1 Resolution | Use ROS or weekly projection (context-dependent) | player_scoring.py:459-469 | if use_weekly_projection: weekly else: ROS |
| Q2 Resolution | Format: projection pts (Score: X) | ScoredPlayer.py:79 | None (always show both) |

---

## Data Flow Traces

### Requirement: Projection value flows from scoring to display

```
Entry: AddToRosterModeManager.get_player_recommendations()
  → PlayerManager.score_player(p, ...)
  → PlayerScoringCalculator.score_player(p, ...)
  → _get_normalized_fantasy_points() returns (weighted, reason, orig_pts)
  → ScoredPlayer(p, player_score, orig_pts, reasons)
  → ScoredPlayer.__str__() displays projected_points
```

---

## Progress Notes

**Last Updated:** 2024-12-13
**Current Status:** TODO created - starting iterations
**Next Steps:** Execute iterations 1-7 (First Round)
**Blockers:** None
