# 4 Week Configs

## Objective

Update the week-specific config system from 3 config files to 4 config files, changing the week ranges from (1-5, 6-11, 12-17) to (1-5, 6-9, 10-13, 14-17) for more granular seasonal scoring parameter optimization.

---

## High-Level Requirements

### 1. Config File Structure

**Current Structure:**
```
data/configs/
├── league_config.json      # Base config with NFL settings
├── week1-5.json            # Early season
├── week6-11.json           # Mid season (6 weeks)
└── week12-17.json          # Late season (6 weeks)
```

**New Structure:**
```
data/configs/
├── league_config.json      # Base config (unchanged)
├── week1-5.json            # Early season (unchanged)
├── week6-9.json            # Mid-early season (4 weeks)
├── week10-13.json          # Mid-late season (4 weeks)
└── week14-17.json          # Late season/playoffs (4 weeks)
```

### 2. Week Range Mapping

| Week | Current Config | New Config |
|------|---------------|------------|
| 1-5  | week1-5.json  | week1-5.json |
| 6-9  | week6-11.json | week6-9.json |
| 10-11| week6-11.json | week10-13.json |
| 12-13| week12-17.json| week10-13.json |
| 14-17| week12-17.json| week14-17.json |

### 3. Files to Modify

**Core Source Files:**

| File | Line(s) | Change Description |
|------|---------|-------------------|
| `league_helper/util/ConfigManager.py` | 231-256 | Update `_get_week_config_filename()` |
| `simulation/ConfigGenerator.py` | 343, 364 | Update `required_files` list |
| `simulation/SimulationManager.py` | 578, 878 | Update file lists and mappings |
| `simulation/ResultsManager.py` | 425-427, 524-526, 589, 609-611, 775 | Update all week file mappings |

**Data Files:**
- DELETE or backup: `data/configs/week6-11.json`, `data/configs/week12-17.json`
- CREATE: `data/configs/week6-9.json`, `data/configs/week10-13.json`, `data/configs/week14-17.json`

**Test Files:**
- `tests/league_helper/util/test_ConfigManager_week_config.py` - Primary test updates
- 14 other test files with week config references (may need updates)

---

## Resolved Questions

### Data Source

1. **New config file content:** RESOLVED - Copy from existing
   - `week6-11.json` → `week6-9.json` and `week10-13.json`
   - `week12-17.json` → `week14-17.json`

### Architecture

2. **Existing simulation_configs strategy folders:** RESOLVED - Manual update
   - User will update old 3-file folders manually as needed
   - No migration script required

3. **Config file naming convention:** RESOLVED - No zero-padding
   - Files: `week6-9.json`, `week10-13.json`, `week14-17.json`

4. **Backward compatibility:** RESOLVED - No backward compatibility
   - Only support new 4-file structure
   - Old folders will fail until manually updated

---

## Resolved Implementation Details

### ConfigManager._get_week_config_filename()

**File:** `league_helper/util/ConfigManager.py`
**Lines:** 231-256

**Current Implementation:**
```python
def _get_week_config_filename(self, week: int) -> str:
    if 1 <= week <= 5:
        return "week1-5.json"
    elif 6 <= week <= 11:
        return "week6-11.json"
    elif 12 <= week <= 17:
        return "week12-17.json"
    else:
        raise ValueError(f"Invalid week number: {week}. Must be between 1 and 17.")
```

**New Implementation:**
```python
def _get_week_config_filename(self, week: int) -> str:
    if 1 <= week <= 5:
        return "week1-5.json"
    elif 6 <= week <= 9:
        return "week6-9.json"
    elif 10 <= week <= 13:
        return "week10-13.json"
    elif 14 <= week <= 17:
        return "week14-17.json"
    else:
        raise ValueError(f"Invalid week number: {week}. Must be between 1 and 17.")
```

---

## Implementation Notes

### Files to Modify (Detailed)

#### 1. ConfigManager.py
- Update `_get_week_config_filename()` method
- Update docstring to reflect new ranges

#### 2. ConfigGenerator.py
- Line 343: `required_files = ['league_config.json', 'week1-5.json', 'week6-9.json', 'week10-13.json', 'week14-17.json']`
- Line 364: Update loop to use new filenames

#### 3. SimulationManager.py
- Line 578: Update `required_files` list
- Line 878: Update `week_file_mapping` dict to:
  ```python
  week_file_mapping = {
      '1-5': 'week1-5.json',
      '6-9': 'week6-9.json',
      '10-13': 'week10-13.json',
      '14-17': 'week14-17.json'
  }
  ```
- All other references to week ranges ('6-11', '12-17') need updates

#### 4. ResultsManager.py
- Lines 425-427: Update week-to-filename mapping
- Lines 524-526: Update week-to-filename mapping
- Line 589: Update required_files list
- Lines 609-611: Update filename-to-range mapping
- Line 775: Update CONFIG_FILES constant

### Dependencies
- No external dependencies
- Only internal code changes required

### Testing Strategy
- Update `test_ConfigManager_week_config.py` boundary tests
- Add tests for new week boundaries (9→10, 13→14)
- Verify all 15 test files with week references

---

## Status: READY FOR IMPLEMENTATION
