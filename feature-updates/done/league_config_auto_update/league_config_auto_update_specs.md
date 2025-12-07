# League Config Auto Update - Specification

## Objective

Fix the automatic update of `data/configs/` folder after iterative simulation to properly preserve user-maintained parameters and apply MATCHUP → SCHEDULE mapping.

---

## Requirements

### R1: Preserve Parameters in league_config.json

When updating `data/configs/league_config.json`, preserve these from the original:
- CURRENT_NFL_WEEK
- NFL_SEASON
- MAX_POSITIONS
- FLEX_ELIGIBLE_POSITIONS
- INJURY_PENALTIES (currently missing)

### R2: MATCHUP → SCHEDULE Mapping for Week Files

When updating week files (week1-5.json, week6-11.json, week12-17.json), copy these values:
- `SCHEDULE_SCORING.MIN_WEEKS` ← `MATCHUP_SCORING.MIN_WEEKS`
- `SCHEDULE_SCORING.IMPACT_SCALE` ← `MATCHUP_SCORING.IMPACT_SCALE`
- `SCHEDULE_SCORING.WEIGHT` ← `MATCHUP_SCORING.WEIGHT`

### R3: Replace shutil.copy2 with Smart Update

Replace the raw file copy in SimulationManager.py:841-845 with smart update logic that applies R1 and R2.

### R4: Update All Other Parameters

All parameters not in the preserve list should be updated from the optimal files.

---

## Implementation Context

### Current Problem Location

**SimulationManager.py:837-848:**
```python
if self.auto_update_league_config:
    data_configs_path = Path(__file__).parent.parent / "data" / "configs"
    if data_configs_path.exists():
        for config_file in ['league_config.json', 'week1-5.json', 'week6-11.json', 'week12-17.json']:
            src = final_folder / config_file
            dst = data_configs_path / config_file
            if src.exists():
                shutil.copy2(src, dst)  # <-- Raw copy, overwrites preserved params
```

### Existing Smart Update Method

**ResultsManager.py:647-733** has `update_league_config()`:
- Works for single JSON file updates
- Preserves: CURRENT_NFL_WEEK, NFL_SEASON, MAX_POSITIONS, FLEX_ELIGIBLE_POSITIONS
- **Missing:** INJURY_PENALTIES
- Has MATCHUP → SCHEDULE mapping logic

### Proposed Solution Options

**Option A: Extend update_league_config()**
- Add INJURY_PENALTIES to PRESERVE_KEYS
- Modify SimulationManager to call it for each file
- Works but method signature is for single file

**Option B: Create new update_configs_folder() method**
- New method in ResultsManager for folder-based updates
- Handles all files with appropriate logic per file type
- Cleaner separation of concerns

---

## Open Questions

See `league_config_auto_update_checklist.md` for all questions that need resolution.

---

## Resolved Implementation Details

### Q1: Architecture Approach

**Decision:** Create new `update_configs_folder()` method in ResultsManager.

**Implementation:**
- Keep existing `update_league_config()` for single file updates
- Add new `update_configs_folder(optimal_folder: Path, target_folder: Path)` method
- New method orchestrates:
  - Update league_config.json (preserving specified params)
  - Update week files (with MATCHUP → SCHEDULE mapping)
- SimulationManager will call `update_configs_folder()` instead of `shutil.copy2()`

### Q2: Week File Preservation

**Decision:** No preservation for week files - only MATCHUP→SCHEDULE mapping needed.

### Q3: Missing Sections Handling

**Decision:** Log warning and use existing values if MATCHUP_SCORING is missing.

### Q4: Performance Metrics

**Decision:** Keep performance_metrics in updated files (preserve for reference).

### Q5: Missing Target Files

**Decision:** If target files don't exist, create from optimal files directly (no preservation possible on first run).

### Q6: INJURY_PENALTIES

**Decision:** Add INJURY_PENALTIES to preserve list - it's a user-maintained setting.

**Final PRESERVE_KEYS list:**
```python
PRESERVE_KEYS = [
    'CURRENT_NFL_WEEK',
    'NFL_SEASON',
    'MAX_POSITIONS',
    'FLEX_ELIGIBLE_POSITIONS',
    'INJURY_PENALTIES'  # Added per user requirement
]
```
