# Bug Fix: Wrong Data Folder - Verified Interface Contracts

**Purpose:** Document ALL external interfaces verified from source code before implementation

**Verification Date:** 2026-01-01

---

## Interface 1: pandas.DataFrame (Input Parameter)

**Source:** Standard pandas library (external)

**Usage:** Input parameter to update_player_adp_values()

**Expected Interface:**
```python
adp_dataframe: pd.DataFrame
```

**Required Columns:**
- `player_name` (str): Player name from CSV
- `adp` (float): ADP value from CSV
- `position` (str): Clean position code (QB, RB, WR, TE, K, DST)

**Methods Used:**
- `df.empty` → bool (check if DataFrame is empty)
- `df.columns` → Index (get column names)
- `df[df['position'] == position]` → DataFrame (filtering)
- `df.iterrows()` → Iterator[Tuple[int, Series]]

**Verified:** ✅ Interface matches TODO assumptions (checked pandas docs)

**Notes:**
- DataFrame comes from Feature 1 (load_adp_from_csv)
- Already validated in Feature 1, but we re-validate required columns
- No changes to pandas interface needed

---

## Interface 2: pathlib.Path (File Operations)

**Source:** Python stdlib pathlib

**Usage:** File and directory operations for week folders and JSON files

**Methods Used:**
```python
Path(data_folder)  # Constructor
path.glob('week_*')  # Discover week folders
path / 'folder' / 'file.json'  # Path composition
path.exists()  # Check existence
path.with_suffix('.tmp')  # Create temp file path
tmp_path.replace(original_path)  # Atomic rename
```

**Verified:** ✅ All methods exist in Path class (Python 3.8+)

**Example Usage in Bug Fix:**
```python
sim_data_folder = Path(sim_data_folder)
weeks_folder = sim_data_folder
week_folders = sorted(weeks_folder.glob('week_*'))
json_path = week_folder / filename
tmp_path = json_path.with_suffix('.tmp')
tmp_path.replace(json_path)  # Atomic write
```

**Notes:**
- Using Path instead of string concatenation (project standard)
- Atomic write pattern already used in current implementation (lines 282-287)
- No changes to Path interface needed

---

## Interface 3: json.load() / json.dump()

**Source:** Python stdlib json

**Current Usage (WRONG):**
```python
# Load
json_data = json.load(f)  # Returns Dict
players = json_data.get(position_key, [])  # Extract array from dict

# Save
json.dump(json_data, f, indent=2)  # Write dict with wrapper
```

**New Usage (CORRECT - Direct Arrays):**
```python
# Load
players = json.load(f)  # Returns List directly (no wrapper)

# Save
json.dump(players, f, indent=2)  # Write list directly
```

**Verified:** ✅ json.load() returns whatever structure is in JSON file
- If JSON file contains `[...]`, returns list
- If JSON file contains `{...}`, returns dict
- Simulation files contain direct arrays, so json.load() returns list

**Methods Used:**
- `json.load(file_object)` → Any (load JSON from file)
- `json.dump(obj, file_object, indent=int)` → None (write JSON to file)

**Critical Change:**
- ❌ OLD: Expects wrapped dict structure `{"qb_data": [...]}`
- ✅ NEW: Expects direct array structure `[...]`
- Must update lines 228-232 and 284

**Notes:**
- No change to json interface itself
- Change is in how we interpret the returned data
- Must handle ValueError if unexpected structure found

---

## Interface 4: LoggingManager.get_logger()

**Source:** utils/LoggingManager.py

**Verified from source:** ✅ Read utils/LoggingManager.py

**Function Signature:**
```python
def get_logger(name: str = None) -> logging.Logger:
    """
    Get configured logger instance.

    Args:
        name (str, optional): Logger name. Defaults to None (root logger).

    Returns:
        logging.Logger: Configured logger instance
    """
```

**Methods Used:**
```python
logger.info(message)    # Info level logging
logger.warning(message) # Warning level logging
logger.error(message, exc_info=True)  # Error with traceback
```

**Verified:** ✅ Returns standard Python logging.Logger

**Current Usage in adp_updater.py:**
```python
# Line 23
from utils.LoggingManager import get_logger
logger = get_logger()

# Lines 216, 223, 279, 289, 302-307
logger.info("...")
logger.warning("...")
```

**New Usage in Bug Fix:**
- Add per-week logging (Task 9)
- Example: `logger.info(f"Processing week {week_num}: {week_folder.name}")`

**Notes:**
- Already imported and used correctly
- No interface changes needed
- Just add more logging calls for per-week progress

---

## Interface 5: Helper Methods (Internal - Already in adp_updater.py)

**Source:** utils/adp_updater.py (same file)

**Method 1: normalize_name()**
```python
# Lines 37-66
def normalize_name(name: str) -> str:
    """Normalize player name for fuzzy matching."""
    # Returns lowercase, no punctuation/suffixes
```

**Verified:** ✅ Already implemented and tested

---

**Method 2: calculate_similarity()**
```python
# Lines 69-87
def calculate_similarity(name1: str, name2: str) -> float:
    """Calculate similarity score between two names."""
    # Returns 0.0-1.0 using SequenceMatcher
```

**Verified:** ✅ Already implemented and tested

---

**Method 3: find_best_match()**
```python
# Lines 90-143
def find_best_match(
    json_player_name: str,
    csv_df: pd.DataFrame,
    position: str
) -> Optional[Tuple[str, float, float]]:
    """Find best matching CSV player using fuzzy matching."""
    # Returns (csv_name, adp_value, confidence) or None
```

**Verified:** ✅ Already implemented and tested

**Usage:** Called in player matching loop (line 241)

**Notes:**
- No changes needed to these helper methods
- They work with both old and new data structures
- Confidence threshold CONFIDENCE_THRESHOLD = 0.75 (line 26)

---

## Interface Summary

**Total External Dependencies:** 5

| Interface | Source | Status | Changes Needed |
|-----------|--------|--------|----------------|
| pandas.DataFrame | External lib | ✅ Verified | None (already correct) |
| pathlib.Path | Python stdlib | ✅ Verified | None (same operations) |
| json.load/dump | Python stdlib | ✅ Verified | Usage change (not interface) |
| LoggingManager.get_logger() | utils/ | ✅ Verified | None (add more calls) |
| Helper methods | Same file | ✅ Verified | None (reuse as-is) |

**Interface Verification:** ✅ COMPLETE

**Confidence:** HIGH - All interfaces verified from actual source code or documentation

**Critical Finding:**
- json.load() returns whatever structure is in the file
- Simulation files have direct arrays `[...]` not wrapped dicts `{"key": [...]}`
- This is the KEY difference that requires code changes

**No interface mismatches found** - All TODO assumptions match reality

---

**Last Updated:** 2026-01-01 00:40
