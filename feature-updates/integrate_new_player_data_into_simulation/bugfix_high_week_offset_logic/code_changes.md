# Bug Fix: Week Offset Logic - Code Changes

**Purpose:** Document all code changes made during implementation (updated INCREMENTALLY)

**Last Updated:** 2026-01-02

---

## Change 1: Updated _load_season_data() in AccuracySimulationManager

**Date:** 2026-01-02
**File:** simulation/accuracy/AccuracySimulationManager.py
**Lines:** 293-337 (MODIFIED - previously 293-313)

**What Changed:**
- Changed from returning (week_folder, week_folder) to (projected_folder, actual_folder)
- Added projected_folder variable: week_N folder
- Added actual_folder variable: week_N+1 folder  - Added existence checks for BOTH folders (not just one)
- Added warning logs for missing folders
- Updated docstring to explain WHY two folders needed (point-in-time data model)

**Why:**
- Implements REQ-1 from spec.md (Solution Design - Change 1)
- Fixes bug where all actual_points were 0.0 (loading from wrong week folder)
- week_N folder has actual_points for weeks 1 to N-1 only
- week_N folder has actual_points[N-1] = 0.0 (week N not complete yet)
- week_N+1 folder has actual_points[N-1] = real value (week N now complete)

**Impact:**
- **Breaking change** for method semantics (returns different data)
- Callers must now handle TWO folder paths instead of one
- get_accuracy_for_week() must be updated to create TWO PlayerManagers (Change 2)
- No backward compatibility needed (this is a bug fix, not a feature)

**Testing:**
- Unit test: test_load_season_data_returns_two_folders() - Created in Task 6
- Unit test: test_load_season_data_handles_missing_actual_folder() - Created in Task 7

**Before:**
```python
def _load_season_data(
    self,
    season_path: Path,
    week_num: int
) -> Tuple[Optional[Path], Optional[Path]]:
    """
    Load data paths for a specific week in a season.

    Returns:
        Tuple of (week_folder, week_folder) or (None, None) if week folder not found
    """
    week_folder = season_path / "weeks" / f"week_{week_num:02d}"

    if not week_folder.exists():
        return None, None

    return week_folder, week_folder  # ❌ BUG
```

**After:**
```python
def _load_season_data(
    self,
    season_path: Path,
    week_num: int
) -> Tuple[Optional[Path], Optional[Path]]:
    """
    Load data paths for a specific week in a season.

    For accuracy calculations, we need TWO week folders:
    - week_N folder: Contains projected_points for week N
    - week_N+1 folder: Contains actual_points for week N

    This is because week_N folder represents data "as of" week N's start,
    so week N's actual results aren't known until week N+1.

    Returns:
        Tuple of (projected_folder, actual_folder) or (None, None) if folders not found
    """
    # Week N folder for projections
    projected_folder = season_path / "weeks" / f"week_{week_num:02d}"

    # Week N+1 folder for actuals
    actual_week_num = week_num + 1
    actual_folder = season_path / "weeks" / f"week_{actual_week_num:02d}"

    # Both folders must exist
    if not projected_folder.exists():
        self.logger.warning(f"Projected folder not found: {projected_folder}")
        return None, None

    if not actual_folder.exists():
        self.logger.warning(
            f"Actual folder not found: {actual_folder} "
            f"(needed for week {week_num} actuals)"
        )
        return None, None

    return projected_folder, actual_folder  # ✓ FIXED
```

**Verified:** 2026-01-02 - Code matches spec.md Solution Design - Change 1 exactly

---

## Change 2: Created Unit Tests for _load_season_data()

**Date:** 2026-01-02
**File:** tests/simulation/test_AccuracySimulationManager.py
**Lines:** 351-496 (ADDED - 3 new test methods)

**What Changed:**
- Added test_load_season_data_returns_two_folders() method (lines 351-399)
- Added test_load_season_data_handles_missing_actual_folder() method (lines 401-449)
- Added test_load_season_data_handles_missing_projected_folder() method (lines 451-496)

**Why:**
- Implements REQ-4a from spec.md (Task 6: Verify method returns two different folders)
- Implements REQ-4b from spec.md (Task 7: Verify graceful handling of missing folders)
- Verifies bug fix works correctly (week_N != week_N+1)
- Verifies error handling (missing folders return (None, None) with warning)

**Impact:**
- Tests verify Change 1 implementation works correctly
- Tests will PASS with fixed code (week_N + week_N+1)
- Tests provide regression protection

**Testing:**
- Unit test: test_load_season_data_returns_two_folders() - Verifies Task 1 implementation
- Unit test: test_load_season_data_handles_missing_actual_folder() - Verifies Task 1 error handling
- Unit test: test_load_season_data_handles_missing_projected_folder() - Verifies Task 1 error handling (bonus)

**Tests Created:**

**Test 1: test_load_season_data_returns_two_folders()** (Task 6)
```python
def test_load_season_data_returns_two_folders(self, tmp_path):
    """Test that _load_season_data returns two different folders (week_N and week_N+1)."""
    # Creates: week_01, week_02, week_17, week_18 folders

    # Test week 1: should return (week_01, week_02)
    projected, actual = manager._load_season_data(season_path, 1)
    assert projected.name == "week_01"
    assert actual.name == "week_02"
    assert projected != actual  # ✓ Different folders

    # Test week 17: should return (week_17, week_18)
    projected, actual = manager._load_season_data(season_path, 17)
    assert projected.name == "week_17"
    assert actual.name == "week_18"
    assert projected != actual  # ✓ Different folders
```

**Test 2: test_load_season_data_handles_missing_actual_folder()** (Task 7 - part 1)
```python
def test_load_season_data_handles_missing_actual_folder(self, tmp_path, caplog):
    """Test that _load_season_data handles missing week_N+1 folder gracefully."""
    # Creates: week_18 folder but NO week_19

    projected, actual = manager._load_season_data(season_path, 18)

    # Should return (None, None)
    assert projected is None
    assert actual is None

    # Should log warning
    assert any("Actual folder not found" in record.message for record in caplog.records)
    assert any("week_19" in record.message for record in caplog.records)

    # No exception raised ✓
```

**Test 3: test_load_season_data_handles_missing_projected_folder()** (Task 7 - part 2, BONUS)
```python
def test_load_season_data_handles_missing_projected_folder(self, tmp_path, caplog):
    """Test that _load_season_data handles missing week_N folder gracefully."""
    # Creates: NO week_01 folder

    projected, actual = manager._load_season_data(season_path, 1)

    # Should return (None, None)
    assert projected is None
    assert actual is None

    # Should log warning
    assert any("Projected folder not found" in record.message for record in caplog.records)
    assert any("week_01" in record.message for record in caplog.records)

    # No exception raised ✓
```

**Verified:** 2026-01-02 - Tests match Task 6 and Task 7 requirements exactly

---

## Change 3: Updated _evaluate_config_weekly() to Use TWO PlayerManagers

**Date:** 2026-01-02
**File:** simulation/accuracy/AccuracySimulationManager.py
**Lines:** 435-505 (MODIFIED - previously 435-496)

**What Changed:**
- Changed from creating ONE player_mgr to creating TWO (projected_mgr, actual_mgr)
- projected_mgr loads from week_N folder (for projections)
- actual_mgr loads from week_N+1 folder (for actuals)
- Check both paths exist before proceeding: `if not projected_path or not actual_path: continue`
- Get projections from `projected_mgr.players` loop
- Get actuals from `actual_mgr.players` loop
- Match by player ID: `if player.id in projections`
- Cleanup BOTH managers in finally block

**Why:**
- Implements REQ-2 from spec.md (Solution Design - Change 2)
- Fixes bug where actuals loaded from wrong week folder (week_N instead of week_N+1)
- week_N folder has actual_points[N-1] = 0.0 (week N not complete yet)
- week_N+1 folder has actual_points[N-1] = real value (week N now complete)

**Impact:**
- **Critical fix** for accuracy simulation functionality
- Accuracy calculations will now use REAL actual points (not 0.0)
- MAE values will be realistic (3-8 range) instead of near-zero
- Changes loop structure (2x PlayerManager creation per week)

**Testing:**
- Unit test: test_get_accuracy_uses_correct_folders() - Will create in Task 8
- Integration test: test_week_1_accuracy_with_real_data() - Will create in Task 9
- Integration test: test_week_17_uses_week_18_folder() - Will create in Task 10
- Integration test: test_all_weeks_have_realistic_mae() - Will create in Task 11

**Before:**
```python
for week_num in range(start_week, end_week + 1):
    projected_path, actual_path = self._load_season_data(season_path, week_num)
    if not projected_path:
        continue

    # Create player manager with this config
    player_mgr = self._create_player_manager(config_dict, projected_path, season_path)  # ❌ Only week_N

    try:
        # ... get projections from player_mgr.players ...

        # Get actuals from SAME player_mgr (week_N folder)
        for player in player_mgr.players:  # ❌ Wrong folder
            actual = player.actual_points[week_num - 1]  # ❌ Gets 0.0

    finally:
        self._cleanup_player_manager(player_mgr)  # Only one cleanup
```

**After:**
```python
for week_num in range(start_week, end_week + 1):
    projected_path, actual_path = self._load_season_data(season_path, week_num)
    if not projected_path or not actual_path:  # ✓ Check BOTH
        # Skip if either folder missing
        continue

    # Create TWO player managers:
    # 1. projected_mgr (from week_N folder) for projections
    # 2. actual_mgr (from week_N+1 folder) for actuals
    projected_mgr = self._create_player_manager(config_dict, projected_path, season_path)  # ✓ week_N
    actual_mgr = self._create_player_manager(config_dict, actual_path, season_path)  # ✓ week_N+1

    try:
        # Get projections from week_N folder (projected_mgr)
        for player in projected_mgr.players:
            scored = projected_mgr.score_player(...)
            if scored:
                projections[player.id] = scored.projected_points

        # Get actuals from week_N+1 folder (actual_mgr)
        # week_N+1 has actual_points[N-1] populated (week N complete)
        for player in actual_mgr.players:  # ✓ Correct folder
            actual = player.actual_points[week_num - 1]  # ✓ Gets REAL value
            if actual is not None and actual > 0:
                actuals[player.id] = actual

                # Match with projection by player ID
                if player.id in projections:  # ✓ Match by ID
                    player_data.append({
                        'name': player.name,
                        'position': player.position,
                        'projected': projections[player.id],
                        'actual': actual
                    })

    finally:
        self._cleanup_player_manager(projected_mgr)  # ✓ Cleanup both
        self._cleanup_player_manager(actual_mgr)
```

**Verified:** 2026-01-02 - Code matches spec.md Solution Design - Change 2 exactly

---

## Change 4: Updated _load_season_data() in ParallelAccuracyRunner

**Date:** 2026-01-02
**File:** simulation/accuracy/ParallelAccuracyRunner.py
**Lines:** 195-236 (MODIFIED - previously 195-206)

**What Changed:**
- IDENTICAL changes to AccuracySimulationManager._load_season_data()
- Created projected_folder variable: week_N folder
- Created actual_folder variable: week_N+1 folder
- Checks BOTH folders exist, logs warnings if not
- Returns (projected_folder, actual_folder) instead of (week_folder, week_folder)
- Updated docstring to explain point-in-time data model

**Why:**
- Implements REQ-1h from spec.md (parallel implementation consistency)
- Same bug fix as serial version (Task 1)
- STANDALONE FUNCTION (no self parameter) - different from AccuracySimulationManager

**Impact:**
- Parallel accuracy runner now loads correct folders
- Consistency between serial and parallel implementations
- Breaking change for function semantics (returns different data)

**Verified:** 2026-01-02 - Code matches spec.md Solution Design - Change 3 exactly

---

## Change 5: Updated Worker Function in ParallelAccuracyRunner

**Date:** 2026-01-02
**File:** simulation/accuracy/ParallelAccuracyRunner.py
**Lines:** 113-183 (MODIFIED - previously 113-174)

**What Changed:**
- IDENTICAL changes to AccuracySimulationManager._evaluate_config_weekly()
- Changed from creating ONE player_mgr to TWO (projected_mgr, actual_mgr)
- Check both paths exist: `if not projected_path or not actual_path: continue`
- projected_mgr loads from week_N folder (for projections)
- actual_mgr loads from week_N+1 folder (for actuals)
- Get projections from `projected_mgr.players` loop
- Get actuals from `actual_mgr.players` loop
- Match by player ID: `if player.id in projections`
- Cleanup BOTH managers in finally block

**Why:**
- Implements REQ-2k from spec.md (parallel implementation consistency)
- Same bug fix as serial version (Task 2)
- Parallel workers will now use REAL actual points (not 0.0)

**Impact:**
- Critical fix for parallel accuracy simulation functionality
- MAE calculations will be realistic in parallel mode
- Consistency between serial and parallel implementations
- Changes loop structure (2x PlayerManager creation per week)

**Before:**
```python
projected_path, actual_path = _load_season_data(season_path, week_num)
if not projected_path:
    continue

# Create player manager with this config
player_mgr = _create_player_manager(config_dict, projected_path, season_path)  # ❌ Only week_N

try:
    # ... get projections from player_mgr.players ...

    # Get actuals from SAME player_mgr (week_N folder)
    for player in player_mgr.players:  # ❌ Wrong folder
        actual = player.actual_points[week_num - 1]  # ❌ Gets 0.0

finally:
    _cleanup_player_manager(player_mgr)  # Only one cleanup
```

**After:**
```python
projected_path, actual_path = _load_season_data(season_path, week_num)
if not projected_path or not actual_path:  # ✓ Check BOTH
    continue

# Create TWO player managers:
projected_mgr = _create_player_manager(config_dict, projected_path, season_path)  # ✓ week_N
actual_mgr = _create_player_manager(config_dict, actual_path, season_path)  # ✓ week_N+1

try:
    # Get projections from week_N folder (projected_mgr)
    for player in projected_mgr.players:
        scored = projected_mgr.score_player(...)
        if scored:
            projections[player.id] = scored.projected_points

    # Get actuals from week_N+1 folder (actual_mgr)
    for player in actual_mgr.players:  # ✓ Correct folder
        actual = player.actual_points[week_num - 1]  # ✓ Gets REAL value
        if actual is not None and actual > 0:
            actuals[player.id] = actual

            # Match with projection by player ID
            if player.id in projections:  # ✓ Match by ID
                player_data.append(...)

finally:
    _cleanup_player_manager(projected_mgr)  # ✓ Cleanup both
    _cleanup_player_manager(actual_mgr)
```

**Verified:** 2026-01-02 - Code matches spec.md Solution Design - Change 3 exactly

---

*More changes will be added incrementally as implementation proceeds*
