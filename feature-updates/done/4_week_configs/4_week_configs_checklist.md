# 4 Week Configs - Requirements Checklist

> **IMPORTANT**: When marking items as resolved, also update `4_week_configs_specs.md`
> with full implementation details. The checklist tracks status; the specs file is
> the implementation specification.

---

## General Decisions

- [x] **Week ranges:** 1-5, 6-9, 10-13, 14-17 (confirmed in user notes)
- [x] **Config file names:** week1-5.json, week6-9.json, week10-13.json, week14-17.json
- [x] **Naming convention:** No zero-padding (`week6-9.json`, not `week06-09.json`)

---

## Data Questions

- [x] **New config file content source:** Copy from existing files
  - `week6-11.json` → `week6-9.json` and `week10-13.json`
  - `week12-17.json` → `week14-17.json`

---

## Architecture Questions

- [x] **Existing simulation strategy folders:** Manual update by user as needed
  - Old folders in `simulation/simulation_configs/strategies/` will be updated manually

- [x] **Backward compatibility for ResultsManager.load_configs_from_folder():** No backward compatibility
  - Only support new 4-file structure
  - Old 3-file folders will fail until manually updated

---

## Files to Modify

### Source Files

| File | Status | Notes |
|------|--------|-------|
| `league_helper/util/ConfigManager.py` | [ ] | `_get_week_config_filename()` |
| `simulation/ConfigGenerator.py` | [ ] | `required_files`, loop references |
| `simulation/SimulationManager.py` | [ ] | `required_files`, `week_file_mapping` |
| `simulation/ResultsManager.py` | [ ] | Multiple week mappings |

### Data Files

| File | Status | Action |
|------|--------|--------|
| `data/configs/week6-11.json` | [ ] | DELETE or backup |
| `data/configs/week12-17.json` | [ ] | DELETE or backup |
| `data/configs/week6-9.json` | [ ] | CREATE |
| `data/configs/week10-13.json` | [ ] | CREATE |
| `data/configs/week14-17.json` | [ ] | CREATE |

### Test Files

| File | Status | Notes |
|------|--------|-------|
| `tests/league_helper/util/test_ConfigManager_week_config.py` | [ ] | Primary test file - extensive updates |
| Other 14 test files | [ ] | Review for week config references |

---

## Edge Cases

- [x] **Week boundary: 5→6:** Already exists, no change
- [ ] **Week boundary: 9→10:** New boundary - need tests
- [ ] **Week boundary: 13→14:** New boundary - need tests
- [x] **Week 1 (minimum):** Uses week1-5.json, no change
- [x] **Week 17 (maximum):** Uses week14-17.json

---

## Testing & Validation

- [ ] **Unit tests pass:** All tests in `test_ConfigManager_week_config.py`
- [ ] **New boundary tests added:** Tests for weeks 9, 10, 13, 14
- [ ] **Simulation integration:** Verify simulation system works with 4 configs
- [ ] **Full test suite:** `python tests/run_all_tests.py` passes

---

## Data Source Summary

| Data | Source | Status |
|------|--------|--------|
| week1-5.json | Existing file | No change |
| week6-9.json | TBD (pending user decision) | Pending |
| week10-13.json | TBD (pending user decision) | Pending |
| week14-17.json | TBD (pending user decision) | Pending |

---

## Resolution Log

| Item | Resolution | Date |
|------|------------|------|
| Week ranges | 1-5, 6-9, 10-13, 14-17 per user spec | 2025-12-13 |
| Config file names | week{N}-{M}.json format | 2025-12-13 |
| Naming convention | No zero-padding (e.g., `week6-9.json`) | 2025-12-13 |
| New config content | Copy from existing week6-11.json and week12-17.json | 2025-12-13 |
| Strategy folders | Manual update by user as needed | 2025-12-13 |
| Backward compatibility | No - 4-file structure only | 2025-12-13 |
