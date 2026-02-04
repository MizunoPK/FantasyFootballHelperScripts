# Feature 10 Checklist: Refactor Player Fetcher

**Feature:** feature_10_refactor_player_fetcher
**Created:** 2026-01-31
**Status:** NOT STARTED (S2.P1 research not yet complete)

---

## Open Questions

### Functional Questions

(None)

---

### Technical Questions

#### Question 1: What to do with config.py file after refactoring?

**Context:**
After refactoring, run_player_fetcher.py will no longer import or override constants from config.py. The 23 CLI-exposed constants will be passed as constructor parameters instead. However, config.py also contains constants NOT exposed to CLI (LOG_NAME, LOGGING_FORMAT, DEFAULT_FILE_CAPS, EXPORT_COLUMNS, etc.).

**Options:**

**Option A: Keep config.py as fallback defaults**
- **Pros:** Tests or other code can still import from config.py, backward compatible
- **Cons:** Two sources of truth (argparse defaults + config.py defaults), can be confusing

**Option B: Remove config.py entirely**
- **Pros:** Single source of truth (all defaults in argparse or Settings class), cleaner
- **Cons:** Need to move non-CLI constants elsewhere, may break other code importing config.py

**Option C: Keep config.py for non-CLI constants only**
- **Pros:** Clear separation (CLI-configurable in argparse, internal-only in config.py)
- **Cons:** Need to remove/document which constants are CLI-configurable

**Recommendation:** Option C (keep for non-CLI constants, document CLI constants elsewhere)

**Reasoning:** Cleanest separation. CLI-configurable constants have defaults in argparse. Internal constants (LOG_NAME, LOGGING_FORMAT) stay in config.py.

**Impact on spec.md:**
- If Option A: config.py stays as-is, may import for fallback defaults
- If Option B: Move non-CLI constants to player_data_fetcher_main.py, remove config.py
- If Option C: Update config.py comments to mark internal-only constants

**User Answer:** Option C

**Answered:** 2026-01-31

**Resolution:**
- Keep config.py for non-CLI constants (LOG_NAME, LOGGING_FORMAT, DEFAULT_FILE_CAPS, EXPORT_COLUMNS, etc.)
- Remove or document CLI-configurable constants (can be deleted since argparse has defaults)
- Add clear comments in config.py to mark internal-only constants
- player_data_fetcher_main.py can continue importing non-CLI constants from config.py

---

#### Question 2: How should Settings class accept constructor parameters?

**Context:**
Settings class currently reads defaults from config.py module constants. After refactoring, it needs to accept values from settings dictionary created by run_player_fetcher.py.

**Options:**

**Option A: Modify Settings.__init__ to accept kwargs**
```python
class Settings(BaseSettings):
    def __init__(self, **overrides):
        defaults = {'season': 2025, 'current_nfl_week': 17, ...}
        merged = {**defaults, **overrides}
        super().__init__(**merged)

# Usage: settings = Settings(**settings_dict)
```
- **Pros:** Standard Python pattern, explicit control
- **Cons:** Need to list all defaults explicitly, can't use pydantic's field defaults

**Option B: Factory function create_settings_from_dict()**
```python
def create_settings_from_dict(settings_dict: dict | None) -> Settings:
    if settings_dict is None:
        return Settings()  # Use field defaults
    return Settings.model_validate(settings_dict)

# Usage: settings = create_settings_from_dict(settings_dict)
```
- **Pros:** Clean separation, leverages pydantic's model_validate(), Settings class unchanged
- **Cons:** Extra function, Settings defaults still need to be hardcoded (not from config.py)

**Option C: Use pydantic's model_validate() directly in main()**
```python
# In main()
if settings_dict is not None:
    settings = Settings.model_validate(settings_dict)
else:
    settings = Settings()  # Use defaults

# No factory function needed
```
- **Pros:** Simplest, uses pydantic as intended, no extra abstraction
- **Cons:** Settings defaults still need to be hardcoded in class definition

**Recommendation:** Option B (factory function)

**Reasoning:** Cleanest separation of concerns. Factory function handles None case gracefully. Settings class can keep simple field definitions. Easy to test.

**Impact on spec.md:**
- Algorithm 2 implementation depends on this choice
- Settings class definition may change (Option A) or stay mostly same (Options B/C)

**User Answer:** Option B

**Answered:** 2026-01-31

**Resolution:**
- Create factory function `create_settings_from_dict(settings_dict: dict | None) -> Settings`
- Function handles None case (returns Settings() with defaults)
- Function uses `Settings.model_validate(settings_dict)` for parameter case
- Settings class field definitions stay simple (hardcoded defaults, not from config.py)
- Easy to test and maintain

---

#### Question 3: Where should non-CLI constants live?

**Context:**
Constants like LOG_NAME, LOGGING_FORMAT, DEFAULT_FILE_CAPS, EXPORT_COLUMNS, COORDINATES_JSON, ESPN_USER_AGENT are NOT exposed to CLI. After refactoring, where should they be defined?

**Constants Affected:**
- LOG_NAME = "player_data_fetcher"
- LOGGING_FORMAT = 'standard'
- DEFAULT_FILE_CAPS = {'csv': 5, 'json': 18, ...}
- EXCEL_POSITION_SHEETS = ['QB', 'RB', 'WR', 'TE', 'K', 'DST']
- EXPORT_COLUMNS = ['id', 'name', 'team', ...]
- COORDINATES_JSON = 'coordinates.json'
- ESPN_USER_AGENT = "Mozilla/5.0..."
- REQUEST_TIMEOUT = 30
- RATE_LIMIT_DELAY = 0.2

**Options:**

**Option A: Keep in config.py, import in player_data_fetcher_main.py**
```python
# player_data_fetcher_main.py
from config import LOG_NAME, LOGGING_FORMAT, EXPORT_COLUMNS, ...
```
- **Pros:** No code changes needed, constants stay in one place
- **Cons:** Still importing from config.py (less clean separation)

**Option B: Move to player_data_fetcher_main.py as module-level constants**
```python
# player_data_fetcher_main.py (at top of file)
LOG_NAME = "player_data_fetcher"
LOGGING_FORMAT = 'standard'
# ... all non-CLI constants
```
- **Pros:** Self-contained, no config.py dependency
- **Cons:** Constants scattered across files, may complicate testing

**Option C: Make them class-level constants in appropriate classes**
```python
class NFLProjectionsCollector:
    EXPORT_COLUMNS = ['id', 'name', 'team', ...]
    EXCEL_POSITION_SHEETS = ['QB', 'RB', ...]

class ESPNClient:
    USER_AGENT = "Mozilla/5.0..."
    REQUEST_TIMEOUT = 30
```
- **Pros:** Best encapsulation, clear ownership
- **Cons:** More refactoring required, constants split across classes

**Recommendation:** Option A (keep in config.py for now)

**Reasoning:** Minimal refactoring impact. Can always move to class-level constants later as separate refactoring.

**Impact on spec.md:**
- Algorithm 3 (extract_logging_config) may need to import LOG_NAME, LOGGING_FORMAT
- R8 implementation depends on this choice

**User Answer:** Option A

**Answered:** 2026-02-01

**Resolution:**
- Keep non-CLI constants in config.py (LOG_NAME, LOGGING_FORMAT, DEFAULT_FILE_CAPS, etc.)
- player_data_fetcher_main.py continues importing these constants from config.py
- Minimal refactoring impact - no need to move constants
- Consistent with Question 1 answer (config.py for non-CLI constants only)
- Can refactor to class-level constants later if needed (separate improvement)

---

### Integration Questions

#### Question 4: Backward compatibility - does other code import from config.py?

**Context:**
Before removing or heavily modifying config.py, need to verify if any other scripts, tests, or modules import from player-data-fetcher/config.py.

**Need to Check:**
- Other runner scripts (run_schedule_fetcher.py, run_game_data_fetcher.py, etc.)
- Test files (tests/**/*.py)
- Any other modules that might import player-data-fetcher/config.py

**Options:**

**If YES (other code imports config.py):**
- **Action:** Keep config.py for backward compatibility (Option A or C from Question 1)
- **Impact:** Cannot remove config.py entirely
- **Workaround:** Document which constants are CLI-overridable vs internal

**If NO (only Feature 01 uses config.py):**
- **Action:** Can remove config.py (Option B from Question 1) or modify freely
- **Impact:** More flexibility in refactoring approach

**How to Verify:**
```bash
# Search for imports from config.py
grep -r "from config import" --include="*.py" .
grep -r "import config" --include="*.py" .
```

**Recommendation:** Run search command during S2.P3, ask user to verify findings

**Impact on spec.md:**
- R8 implementation depends on backward compatibility requirements
- May affect Question 1 answer

**User Answer:** Hybrid approach (Option C)

**Answered:** 2026-02-01

**Research Findings:**
- **Files importing from config.py:** 5 internal modules + 1 external runner + 2 test files
- **Internal modules:** espn_client.py, player_data_exporter.py, game_data_fetcher.py, fantasy_points_calculator.py
- **External runner:** run_game_data_fetcher.py (uses NFL_SEASON, CURRENT_NFL_WEEK as fallback defaults)
- **CLI constants imported:** ESPN_PLAYER_LIMIT, CURRENT_NFL_WEEK, NFL_SEASON, CREATE_POSITION_JSON, POSITION_JSON_OUTPUT, PRESERVE_LOCKED_VALUES, TEAM_DATA_FOLDER, LOAD_DRAFTED_DATA_FROM_FILE, DRAFTED_DATA, MY_TEAM_NAME, GAME_DATA_CSV

**Resolution:**
- **Scope Expansion:** Feature 10 will refactor 4 internal modules (espn_client.py, player_data_exporter.py, game_data_fetcher.py, fantasy_points_calculator.py)
- **Approach:** Remove CLI-configurable constants from config.py
- **Settings Class:** Add all CLI-configurable constants as fields in Settings class
- **Constructor Changes:** Internal modules refactored to accept Settings object (not individual constants)
- **config.py:** Will only contain non-CLI constants (9 constants total)
- **Backward Compatibility:** run_game_data_fetcher.py may need refactoring (separate feature or include in Feature 10?)
- **Test Updates:** test_config.py and test_game_data_fetcher.py will need updates

**Impact on Scope:**
- **Components Affected:** Increases from 3 files to 7+ files (run_player_fetcher.py, player_data_fetcher_main.py, config.py, espn_client.py, player_data_exporter.py, game_data_fetcher.py, fantasy_points_calculator.py)
- **Estimated Size:** Increases from MEDIUM to LARGE
- **Risk:** Moderate to High (touching multiple core modules)
- **Benefits:** Clean architecture, single source of truth, consistent pattern across all modules

---

### Error Handling Questions

(None)

---

### Testing Questions

(None - all covered by R5: maintain 100% test pass rate)

---

### Dependencies & Blockers

(None - all dependencies verified in research)

---

## Question Summary

**Total Questions:** 4
- Functional: 0
- Technical: 3 (Questions 1, 2, 3)
- Integration: 1 (Question 4)
- Error Handling: 0
- Testing: 0
- Dependencies: 0

**Status:**
- Open: 0
- Answered: 4 (Questions 1, 2, 3, 4)
- Resolved: 4 (Questions 1, 2, 3, 4)

**Question Types:**
- ✅ All questions are GENUINE user preferences (implementation choices)
- ✅ No "should have researched" questions (research was thorough)
- ✅ All questions have clear options with pros/cons
- ✅ All questions have recommendations with reasoning

---

## User Approval

**Approval Status:** PENDING (waiting for S2.P3 Gate 3)
**Approved Date:** Not yet approved
**Approved By:** N/A

**Next Action:** Complete S2.P1 research, populate questions during S2.P2

---

## Notes

**Why This Feature Exists:**
Missed requirement discovered during S8.P1 alignment. Feature 01 uses config override pattern; constructor parameter pattern is better design. This feature refactors Feature 01 for consistency.
