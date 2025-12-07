# Simulation Optimal Config Caps - Specification

## Objective

Add automatic cleanup of old optimal configuration folders when a new one is created. Limit the total number of `optimal_*` folders to a configurable maximum (default: 5).

---

## Requirements

### R1: Folder Limit Enforcement

When creating a new `optimal_*` folder, check if the limit would be exceeded:
- Count existing `optimal_*` folders in `simulation_configs/`
- If count >= limit, delete oldest folder(s) until count < limit
- Then create the new folder

### R2: Oldest Determination

Determine "oldest" folder by:
- **Option A**: Parse timestamp from folder name (sortable format)
- **Option B**: Use filesystem modification time

*(Decision pending - see checklist)*

### R3: Configurable Limit

The maximum number of optimal folders should be configurable:
- Default value: 5
- Where to configure: *(Decision pending - see checklist)*

### R4: Pattern Matching

Only count/delete folders matching `optimal_*` pattern:
- Include: `optimal_iterative_*`, `optimal_YYYY-*`
- Exclude: `intermediate_*`, other folders

---

## Implementation Context

### Code Locations

| Location | What Happens | Modification Needed |
|----------|--------------|---------------------|
| SimulationManager.py:772 | Creates `optimal_iterative_{timestamp}` | Add cleanup before creation |
| ResultsManager.py:400 | Creates `optimal_{timestamp}` | Add cleanup before creation |

### Current Creation Flow

**SimulationManager.py (iterative optimization):**
```python
# Line 772
final_folder = self.output_dir / f"optimal_iterative_{timestamp}"
final_folder.mkdir(parents=True, exist_ok=True)
```

**ResultsManager.py (save_optimal_configs_folder):**
```python
# Line 400
folder_name = f"optimal_{timestamp}"
folder_path = output_dir / folder_name
folder_path.mkdir(parents=True, exist_ok=True)
```

---

## Open Questions

See `simulation_optimal_config_caps_checklist.md` for all questions that need resolution.

---

## Resolved Implementation Details

### Q1: Cleanup Logic Location

**Decision:** Create a shared utility function that both callers can use.

**Implementation:**
- Create new function (location TBD, likely `simulation/` or `utils/`)
- Function signature: `cleanup_old_optimal_folders(config_dir: Path, max_folders: int = 5) -> int`
- Returns: Number of folders deleted
- Called by:
  - `SimulationManager.py:772` before creating `optimal_iterative_{timestamp}`
  - `ResultsManager.py:400` before creating `optimal_{timestamp}`

### Q2: Oldest Folder Determination

**Decision:** Use folder name timestamp (alphabetical sort).

**Implementation:**
- Folder names are already sortable: `optimal_iterative_20251130_*` < `optimal_iterative_20251205_*`
- Algorithm: `sorted(optimal_folders)[0]` returns oldest
- No timestamp parsing needed - string comparison works

### Q3: Configuration Location

**Decision:** Hardcoded constant in utility file.

**Implementation:**
```python
MAX_OPTIMAL_FOLDERS = 5  # Maximum number of optimal_* folders to keep
```
- Simple, rarely needs changing
- Can be promoted to config later if needed

### Q4: Default Limit

**Decision:** 5 folders (confirmed by user).

### Q5: Error Handling

**Decision:** Log warning and continue if deletion fails.

**Implementation:**
```python
try:
    shutil.rmtree(folder_path)
    logger.info(f"Deleted old optimal folder: {folder_path.name}")
except Exception as e:
    logger.warning(f"Failed to delete {folder_path.name}: {e}")
    # Continue anyway - don't block new folder creation
```

### Q6: Intermediate Folders

**Decision:** Out of scope - intermediate folders already have automatic cleanup implemented.
