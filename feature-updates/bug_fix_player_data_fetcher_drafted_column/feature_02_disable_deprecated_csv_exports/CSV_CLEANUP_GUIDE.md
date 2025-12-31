# CSV File Cleanup Guide

**Feature:** feature_02_disable_deprecated_csv_exports
**Created:** 2025-12-31
**Purpose:** Document cleanup of deprecated CSV files after implementation

---

## Overview

After implementing this feature, the player-data-fetcher no longer creates the following CSV files:
- `data/players.csv`
- `data/players_projected.csv`

These files have been replaced by position-specific JSON files in `data/player_data/`:
- `qb_data.json`
- `rb_data.json`
- `wr_data.json`
- `te_data.json`
- `k_data.json`
- `dst_data.json`

---

## Cleanup Instructions

### Option 1: Delete Old CSV Files (Recommended)

If you are confident that no external scripts depend on these CSV files, you can safely delete them:

```bash
# Navigate to project root
cd /path/to/FantasyFootballHelperScripts

# Delete deprecated CSV files
rm data/players.csv
rm data/players_projected.csv
```

**Note:** After deletion, these files will NOT be recreated by the player-data-fetcher.

### Option 2: Backup Before Deleting

If you want to be cautious, backup the files before deleting:

```bash
# Create backup folder
mkdir -p data/backup_deprecated_csv

# Move files to backup
mv data/players.csv data/backup_deprecated_csv/
mv data/players_projected.csv data/backup_deprecated_csv/
```

### Option 3: Keep Files (Not Recommended)

You can choose to keep the existing CSV files:
- They will NOT be updated by the player-data-fetcher
- They will become stale over time
- They may cause confusion about which data source is current

---

## Verification

After cleanup, verify that the system still works correctly:

1. **Run player-data-fetcher:**
   ```bash
   python run_player_fetcher.py
   ```
   - Check that position JSON files are created/updated
   - Verify NO new CSV files are created in data/

2. **Run league helper:**
   ```bash
   python run_league_helper.py
   ```
   - Test all modes (Draft, Optimize, Trade, Modify)
   - Verify all modes load data from JSON files successfully

3. **Run simulation:**
   ```bash
   python run_simulation.py
   ```
   - Verify simulation works without CSV files

---

## What If I Need the CSV Files?

If you discover that you need the CSV files for some external purpose:

1. The position JSON files contain ALL the same data as the deprecated CSVs
2. You can write a simple script to convert JSON → CSV if needed
3. Contact the maintainer if you need help with conversion

---

## Migration Impact Summary

**Files Deprecated:**
- `data/players.csv` (replaced by position JSON files)
- `data/players_projected.csv` (replaced by position JSON files)

**Files Still Created:**
- Position JSON files (qb_data.json, rb_data.json, etc.)
- Timestamped CSV exports in player-data-fetcher/data/ (for historical records)
- Timestamped JSON exports in player-data-fetcher/data/ (for historical records)
- Excel exports in player-data-fetcher/data/ (for human-readable reports)

**Systems Verified:**
- League Helper: Loads from JSON ✅
- Simulation: Uses historical sim_data/ ✅
- SaveCalculatedPointsManager: No longer copies deprecated CSVs ✅

---

## Questions?

If you encounter issues after cleanup, check:
1. Position JSON files exist in data/player_data/
2. League helper can load data successfully
3. Simulation can run successfully

For additional help, see the main project README.md or contact the maintainer.
