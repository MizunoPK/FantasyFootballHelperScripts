# Bug Fix: Week Offset Logic - Verified Interface Contracts

**Purpose:** Document ALL interfaces verified from source code BEFORE implementation

**Verification Date:** 2026-01-02

**⚠️ CRITICAL:** All interfaces verified by reading actual source files (not from memory or assumptions)

---

## Interface 1: AccuracySimulationManager._load_season_data()

**Source:** simulation/accuracy/AccuracySimulationManager.py:293-313

**Current Signature (BROKEN - will be modified):**
```python
def _load_season_data(
    self,
    season_path: Path,
    week_num: int
) -> Tuple[Optional[Path], Optional[Path]]
```

**Parameters:**
- `season_path` (Path): Path to season folder (e.g., sim_data/2024/)
- `week_num` (int): Week number (1-17)

**Current Returns:**
- `Tuple[Optional[Path], Optional[Path]]`
- Currently returns `(week_folder, week_folder)` ← **BUG** (line 313)
- Should return `(projected_folder, actual_folder)` where actual_folder = week_N+1

**Exceptions:**
- None (returns (None, None) if folder doesn't exist)

**Verified:** ✅ Signature matches TODO assumptions
**Bug Confirmed:** ✅ Line 313 returns same folder twice (this is what we're fixing)

---

## Interface 2: AccuracySimulationManager._create_player_manager()

**Source:** simulation/accuracy/AccuracySimulationManager.py:315-380

**Signature:**
```python
def _create_player_manager(
    self,
    config_dict: dict,
    week_data_path: Path,
    season_path: Path
) -> PlayerManager
```

**Parameters:**
- `config_dict` (dict): Configuration dictionary
- `week_data_path` (Path): Path to week folder containing position JSON files
- `season_path` (Path): Path to season folder containing season_schedule.csv, team_data/

**Returns:**
- `PlayerManager`: Configured player manager with temp_dir for cleanup

**Side Effects:**
- Creates temp directory (stored in player_mgr._temp_dir)
- Copies JSON files, season data to temp directory

**Usage Pattern (from source line 417):**
```python
player_mgr = self._create_player_manager(config_dict, projected_path, season_path)
```

**Verified:** ✅ Interface matches TODO assumptions
**Note:** Will be called TWICE in fixed code (once for projected_path, once for actual_path)

---

## Interface 3: AccuracySimulationManager._cleanup_player_manager()

**Source:** simulation/accuracy/AccuracySimulationManager.py:382-386

**Signature:**
```python
def _cleanup_player_manager(self, player_mgr: PlayerManager) -> None
```

**Parameters:**
- `player_mgr` (PlayerManager): PlayerManager instance to cleanup

**Returns:**
- `None`

**Side Effects:**
- Removes temp directory (player_mgr._temp_dir)

**Usage Pattern (from source line 472):**
```python
finally:
    self._cleanup_player_manager(player_mgr)
```

**Verified:** ✅ Interface matches TODO assumptions
**Note:** Will be called TWICE in fixed code (cleanup both projected_mgr and actual_mgr)

---

## Interface 4: ParallelAccuracyRunner._load_season_data()

**Source:** simulation/accuracy/ParallelAccuracyRunner.py:195-206

**⚠️ IMPORTANT:** This is a **STANDALONE FUNCTION** (no `self` parameter)

**Current Signature (BROKEN - will be modified):**
```python
def _load_season_data(season_path: Path, week_num: int) -> Tuple[Path, Path]
```

**Parameters:**
- `season_path` (Path): Path to season folder
- `week_num` (int): Week number (1-17)

**Current Returns:**
- `Tuple[Path, Path]`
- Currently returns `(week_folder, week_folder)` ← **BUG** (line 206)
- Should return `(projected_folder, actual_folder)`

**Exceptions:**
- None (returns (None, None) if folder doesn't exist)

**Verified:** ✅ Signature matches TODO assumptions
**Note:** STANDALONE FUNCTION (not instance method) - no `self` parameter
**Bug Confirmed:** ✅ Line 206 returns same folder twice (this is what we're fixing)

---

## Interface 5: ParallelAccuracyRunner._create_player_manager()

**Source:** simulation/accuracy/ParallelAccuracyRunner.py:209-266

**⚠️ IMPORTANT:** This is a **STANDALONE FUNCTION** (no `self` parameter)

**Signature:**
```python
def _create_player_manager(config_dict: dict, week_data_path: Path, season_path: Path) -> PlayerManager
```

**Parameters:**
- `config_dict` (dict): Configuration dictionary
- `week_data_path` (Path): Path to week folder containing position JSON files
- `season_path` (Path): Path to season folder

**Returns:**
- `PlayerManager`: Configured player manager with temp_dir for cleanup

**Side Effects:**
- Same as AccuracySimulationManager version (creates temp dir, copies files)

**Verified:** ✅ Interface matches TODO assumptions
**Note:** STANDALONE FUNCTION - same logic as AccuracySimulationManager version, just not a method

---

## Interface 6: ParallelAccuracyRunner._cleanup_player_manager()

**Source:** simulation/accuracy/ParallelAccuracyRunner.py:269-272

**⚠️ IMPORTANT:** This is a **STANDALONE FUNCTION** (no `self` parameter)

**Signature:**
```python
def _cleanup_player_manager(player_mgr: PlayerManager) -> None
```

**Parameters:**
- `player_mgr` (PlayerManager): PlayerManager instance to cleanup

**Returns:**
- `None`

**Side Effects:**
- Removes temp directory

**Verified:** ✅ Interface matches TODO assumptions
**Note:** STANDALONE FUNCTION

---

## Interface 7: FantasyPlayer.actual_points field

**Source:** utils/FantasyPlayer.py (verified from Feature 01/02)

**Field:**
```python
actual_points: List[float]  # 17-element list
```

**Type:** `List[float]` with 17 elements

**Data Model (CRITICAL):**
- week_N folder: actual_points[0 to N-1] have values, actual_points[N to 16] = 0.0
- week_N folder: actual_points[N-1] = 0.0 (week N not complete yet)
- week_N+1 folder: actual_points[N-1] = real value (week N now complete)

**Usage Pattern (from source line 454):**
```python
actual = player.actual_points[week_num - 1]  # Gets value from current PlayerManager's data
```

**Verified:** ✅ Field exists (from Feature 01/02)
**Critical:** We need to get actual_points from week_N+1 PlayerManager, not week_N PlayerManager

---

## Interface 8: Path.exists()

**Source:** Python stdlib pathlib.Path

**Signature:**
```python
def exists(self) -> bool
```

**Returns:**
- `bool`: True if path exists, False otherwise

**Usage Pattern (from source line 310):**
```python
if not week_folder.exists():
    return None, None
```

**Verified:** ✅ Standard library interface

---

## Interface Verification Summary

**Total Interfaces Verified:** 8

**From AccuracySimulationManager.py:**
1. ✅ _load_season_data() - Instance method, returns tuple
2. ✅ _create_player_manager() - Instance method, creates temp PlayerManager
3. ✅ _cleanup_player_manager() - Instance method, cleans up temp dir

**From ParallelAccuracyRunner.py:**
4. ✅ _load_season_data() - **STANDALONE FUNCTION** (no self)
5. ✅ _create_player_manager() - **STANDALONE FUNCTION** (no self)
6. ✅ _cleanup_player_manager() - **STANDALONE FUNCTION** (no self)

**From utils/FantasyPlayer.py:**
7. ✅ actual_points field - List[float] with 17 elements

**From Python stdlib:**
8. ✅ Path.exists() - Returns bool

**Interface Mismatches Found:** 0 (all TODO assumptions match reality)

**Critical Notes:**
- ParallelAccuracyRunner uses STANDALONE FUNCTIONS (not instance methods)
- AccuracySimulationManager uses instance methods (has `self` parameter)
- Both have identical logic, just different function types
- actual_points array requires week_N+1 folder to get week N actuals

**Verification Complete:** ✅ All interfaces verified from source code, ready to implement

---

*Created during Stage 5b Step 1 - Interface Verification Protocol*
*All interfaces verified by reading actual source files (not assumptions)*
