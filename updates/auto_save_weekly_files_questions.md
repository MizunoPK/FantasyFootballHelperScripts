# Auto-Save Weekly Files - Questions

## Overview
This document contains clarifying questions about the auto-save weekly files feature implementation. Each question includes researched options with recommendations based on codebase patterns.

---

## Question 1: Configuration Option for Auto-Save

**Question**: Should there be a configuration option to disable/enable the auto-save feature?

**Context**: The requirement doesn't specify whether this should always run or be configurable. Adding a config option provides flexibility for debugging or custom workflows but adds complexity.

**Options**:

### Option A: Always Enabled (No Config Option) ✅ **RECOMMENDED**
- Feature always runs after successful data export
- Simpler implementation, no configuration to maintain
- Consistent behavior across all runs
- Can be easily disabled later if needed by commenting out one line

**Reasoning**: The requirement states files should be saved automatically "as part of" the player data fetcher, implying it should always happen. The feature is non-intrusive (only creates folder once) and provides value every time.

### Option B: Add Config Option (ENABLE_HISTORICAL_DATA_SAVE)
- Add boolean flag to `player-data-fetcher/config.py`
- Check flag before saving
- Provides user control but adds configuration complexity

**Reasoning**: Useful if users want to disable for testing or have custom archival workflows.

Answer: Option B

---

## Question 2: User Notification Level

**Question**: How prominently should the auto-save operation be communicated to the user?

**Context**: The feature runs automatically after export. Users may want to know when files are saved vs. skipped.

**Options**:

### Option A: INFO Level Logging + Console Message ✅ **RECOMMENDED**
- Log with INFO level when folder created and files copied
- Log with INFO level when folder already exists (skip operation)
- Print console message: `[INFO] Saved weekly data to historical folder` or `[INFO] Weekly data already saved for Week N`

**Reasoning**: Consistent with existing patterns in player_data_fetcher_main.py lines 445-452 where important operations are logged and printed. Users should know the operation occurred.

### Option B: DEBUG Level Logging Only
- Log with DEBUG level (not visible by default)
- No console output
- Silent operation unless LOGGING_LEVEL set to DEBUG

**Reasoning**: Less user-facing, treats it as internal operation. May confuse users if they don't realize files are being saved.

### Option C: Prominent Console Banner
- Print bold/colored banner announcing save
- Example: `========== HISTORICAL DATA SAVED ==========`

**Reasoning**: Too prominent for a routine operation that happens every week.

Answer: Option A

---

## Question 3: Error Handling Behavior

**Question**: What should happen if folder creation or file copying fails?

**Context**: Possible failures include permission errors, disk space issues, or file locks.

**Options**:

### Option A: Log Warning, Continue Execution ✅ **RECOMMENDED**
- Catch exceptions, log with WARNING level
- Print warning message to console
- Allow main export workflow to complete successfully
- Historical save is supplementary - failure shouldn't break main workflow

**Reasoning**: Matches pattern from player_data_fetcher_main.py:348-356 where supplementary features (like players_projected.csv update) don't crash main workflow. Ensures data export always succeeds even if historical save fails.

### Option B: Log Error, Raise Exception
- Catch exceptions, log with ERROR level
- Re-raise exception to crash the program
- Forces user to fix issue before continuing

**Reasoning**: Ensures historical data is always saved correctly, but may be too strict for a supplementary feature.

### Option C: Silent Failure
- Catch exceptions, don't log or notify
- Continue as if nothing happened

**Reasoning**: Not recommended - users should know if automatic save failed.


Answer: Option A

---

## Question 4: Folder Naming Convention

**Question**: Should the folder name be `week{N}` or `Week{N}` (capitalization)?

**Context**: Existing historical data folders show mixed naming: `week10`, `week11`, `week9` (lowercase) but also `WEEK8` (uppercase).

**Options**:

### Option A: Lowercase `week{N}` ✅ **RECOMMENDED**
- Example: `week10`, `week11`, `week12`
- Matches majority of existing folders
- Standard Python/Unix convention (lowercase)

**Reasoning**: Most existing folders use lowercase. Only WEEK8 uses uppercase, likely a one-time naming inconsistency.

### Option B: Uppercase `Week{N}`
- Example: `Week10`, `Week11`, `Week12`
- Title case, more human-readable

**Reasoning**: Less common in Python projects, doesn't match existing pattern.

### Option C: All Uppercase `WEEK{N}`
- Example: `WEEK10`, `WEEK11`, `WEEK12`
- Matches one existing folder (WEEK8)

**Reasoning**: Only one folder uses this pattern, likely an anomaly.

Answer: Let's actually just have the folder named {N} like '11', '12, '13', etc. Update the existing folders to match this convention

---

## Question 5: File Copy Metadata Preservation

**Question**: Should file metadata (timestamps, permissions) be preserved when copying?

**Context**: `shutil.copy2()` preserves metadata vs `shutil.copy()` which doesn't.

**Options**:

### Option A: Preserve Metadata (use shutil.copy2) ✅ **RECOMMENDED**
- Preserves original modification time, permissions
- Historical snapshots maintain original file timestamps
- Useful for auditing when data was actually generated

**Reasoning**: More accurate historical record. No downside to preserving metadata.

### Option B: Don't Preserve Metadata (use shutil.copy)
- New files get current timestamp
- Simpler operation

**Reasoning**: Timestamp would reflect when historical copy was made, not when data was generated. Less accurate for historical purposes.

Answer: Option A 

---

## Question 6: Season Folder Creation

**Question**: Should the feature verify that the season folder exists, or assume it exists?

**Context**: Path structure is `data/historical_data/{Season}/week{Week}/`. Season folder might not exist for new seasons.

**Options**:

### Option A: Create Season Folder if Needed (parents=True) ✅ **RECOMMENDED**
- Use `mkdir(parents=True, exist_ok=True)`
- Automatically creates both season and week folders if missing
- More robust, handles first run of new season

**Reasoning**: Matches pattern from utils/data_file_manager.py:59 and player_data_exporter.py:43. Prevents errors when running for first time in new season.

### Option B: Assume Season Folder Exists
- Only create week folder
- Fail if season folder missing

**Reasoning**: Requires manual season folder setup, less user-friendly.


Answer: Option A

---

## Question 7: Week Number Padding

**Question**: Should week numbers be zero-padded (e.g., `week01`, `week10`) or not padded (`week1`, `week10`)?

**Context**: Existing folders show no padding: `week9`, `week10`, `week11`.

**Options**:

### Option A: No Padding ✅ **RECOMMENDED**
- Example: `week1`, `week2`, ..., `week10`, `week11`
- Matches all existing folders
- Simpler string formatting: `f"week{week_num}"`

**Reasoning**: Matches existing pattern. Sorting still works correctly since Python sorts strings with same prefix correctly (week10 comes after week9).

### Option B: Zero-Padded
- Example: `week01`, `week02`, ..., `week10`, `week11`
- Ensures alphabetical sorting matches numerical order

**Reasoning**: More consistent for sorting, but doesn't match existing pattern.

Answer: Yes make it zero-padded, so '01', '02', '11', '12', etc

---

## Question 8: Historical Data Cleanup

**Question**: Should the feature implement automatic cleanup of old historical data (e.g., delete data older than 2 seasons)?

**Context**: Historical data accumulates indefinitely. Each week = ~2.8MB, 17 weeks = ~48MB per season.

**Options**:

### Option A: No Automatic Cleanup ✅ **RECOMMENDED**
- Feature only creates folders, never deletes
- User manually manages old data if needed
- Append-only operation

**Reasoning**: The requirement only mentions creating/copying, not managing lifecycle. Deletion is risky - better to let users manage. Historical data is relatively small (48MB/season) and valuable for analysis.

### Option B: Automatic Cleanup After N Seasons
- Add config option: HISTORICAL_DATA_RETENTION_SEASONS = 2
- Delete folders older than N seasons
- Frees disk space automatically

**Reasoning**: Adds complexity and risk. Users may want to keep old data for analysis.

Answer: Option A

---

## User Answers

*To be filled in by user*

**Question 1 (Configuration)**: _______
**Question 2 (Notification Level)**: _______
**Question 3 (Error Handling)**: _______
**Question 4 (Folder Naming)**: _______
**Question 5 (Metadata Preservation)**: _______
**Question 6 (Season Folder Creation)**: _______
**Question 7 (Week Padding)**: _______
**Question 8 (Historical Cleanup)**: _______

---

## Summary of Recommendations

Based on codebase research and existing patterns:

1. **No config option** - always enabled (can add later if needed)
2. **INFO logging + console message** - consistent with existing important operations
3. **Log warning, continue execution** - supplementary feature shouldn't break main workflow
4. **Lowercase `week{N}`** - matches existing pattern
5. **Preserve metadata (copy2)** - more accurate historical record
6. **Create season folder if needed** - robust, handles new seasons automatically
7. **No zero-padding** - matches existing pattern
8. **No automatic cleanup** - append-only, user manages old data

These recommendations prioritize:
- Consistency with existing codebase patterns
- User-friendly behavior (robust error handling)
- Simplicity (minimal configuration)
- Safety (no automatic deletion)
