# Simulation Optimal Config Caps - Checklist

## Open Questions

### Architecture Questions

- [x] **Q1: Where should the cleanup logic live?**
  - ~~Option A: Add method to SimulationManager~~
  - ~~Option B: Add method to ResultsManager~~
  - **Option C: Create shared utility function (called by both classes)** ✓

- [x] **Q2: How to determine "oldest" folder?**
  - **Option A: Parse timestamp from folder name (reliable, sortable)** ✓
  - ~~Option B: Use filesystem mtime~~

### Configuration Questions

- [x] **Q3: Where should the limit be configured?**
  - **Option A: Hardcoded constant in utility file** ✓
  - ~~Option B: Constructor parameter with default~~
  - ~~Option C: In league_config.json~~
  - ~~Option D: Command-line argument~~

- [x] **Q4: What should the default limit be?**
  - **5 folders** ✓

### Edge Case Questions

- [x] **Q5: What if deletion fails (permissions, folder in use)?**
  - **Option A: Log warning and continue (don't block new folder creation)** ✓
  - ~~Option B: Raise error and abort~~

- [x] **Q6: Should intermediate folders also have a cap?**
  - **Option A: Out of scope** ✓ (intermediate folders already have automatic cleanup)

---

## Resolution Log

| Question | Resolution | Date | Notes |
|----------|------------|------|-------|
| Q1 | Shared utility function | 2025-12-06 | Both SimulationManager and ResultsManager will call it |
| Q2 | Folder name timestamp | 2025-12-06 | Folders sort alphabetically, `sorted(folders)[0]` = oldest |
| Q3 | Hardcoded constant | 2025-12-06 | `MAX_OPTIMAL_FOLDERS = 5` in utility file |
| Q4 | 5 folders | 2025-12-06 | Confirmed by user |
| Q5 | Log warning, continue | 2025-12-06 | Don't block simulation for housekeeping failures |
| Q6 | Out of scope | 2025-12-06 | Intermediate folders already have automatic cleanup |
