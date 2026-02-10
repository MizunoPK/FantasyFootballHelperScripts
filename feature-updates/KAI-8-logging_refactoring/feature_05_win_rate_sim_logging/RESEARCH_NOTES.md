# Research Notes: Feature 05 (win_rate_sim_logging)

**Feature:** win_rate_sim_logging
**Research Date:** 2026-02-06
**Agent:** Secondary-D

---

## Research Objective

Identify all files, logging calls, and integration points for adding --enable-log-file CLI flag to run_win_rate_simulation.py and improving log quality in simulation/win_rate/ modules.

---

## Code Locations Found

### Entry Script

**File:** `run_win_rate_simulation.py` (actually named `run_simulation.py`)
**Path:** `/home/kai/code/FantasyFootballHelperScriptsRefactored/run_simulation.py`

**Key Findings:**
- **Line 34:** `LOGGING_TO_FILE = False` - Hardcoded constant (NEEDS REPLACEMENT)
- **Line 33-37:** Logging configuration section with hardcoded values
- **Line 117:** `setup_logger(LOG_NAME, LOGGING_LEVEL, LOGGING_TO_FILE, LOGGING_FILE, LOGGING_FORMAT)`
- **Uses argparse** (lines 94-214) for CLI argument parsing
- **No --enable-log-file flag** currently exists

**Required Changes:**
1. Remove LOGGING_TO_FILE constant (line 34)
2. Add --enable-log-file argument to argparser
3. Update setup_logger() call to use args.enable_log_file

---

### Win Rate Simulation Modules

**Directory:** `simulation/win_rate/`

**Module Inventory:**
1. `SimulationManager.py` - 111 logging calls
2. `ParallelLeagueRunner.py` - 26 logging calls
3. `SimulatedLeague.py` - 35 logging calls
4. `DraftHelperTeam.py` - 8 logging calls
5. `SimulatedOpponent.py` - 5 logging calls
6. `Week.py` - 6 logging calls
7. `manual_simulation.py` - 6 logging calls

**Total:** 197 logging calls across 7 files

**Logging Pattern:**
```python
# All modules use this pattern:
from utils.LoggingManager import get_logger

class SomeClass:
    def __init__(self):
        self.logger = get_logger()  # Gets CURRENT logger (configured by entry script)
```

**Key Insight:**
- Entry script calls `setup_logger()` to configure logging
- Internal modules call `get_logger()` to access that configured logger
- No changes needed to internal modules for CLI flag (only entry script)

---

### LoggingManager Integration

**File:** `utils/LoggingManager.py`

**Key Functions:**
- **Line 45:** `def setup_logger(...)` - Configures NEW logger (called by entry scripts)
- **Line 120:** `def get_logger()` - Returns CURRENT logger (called by internal modules)
- **Line 149:** `_logging_manager = LoggingManager()` - Singleton instance

**Integration with Feature 01:**
- Feature 01 modifies setup_logger() to use LineBasedRotatingHandler
- run_win_rate_simulation.py calls setup_logger() with log_to_file parameter
- log_to_file parameter will be driven by --enable-log-file CLI flag

---

## Log Quality Analysis

### Current Logging Examples

**From SimulationManager.py:**
```python
# INFO level examples:
self.logger.info("Initializing SimulationManager")  # ✅ Good - script start
self.logger.info(f"Generated {len(combinations)} parameter combinations")  # ✅ Good - major phase
self.logger.info(f"Registered {len(combinations)} configurations")  # ✅ Good - significant outcome

# DEBUG level examples:
self.logger.debug(f"Season {season_idx + 1}/{total_seasons}: {season_name}")  # ✅ Good - iteration details
self.logger.debug(f"Season {season_folder.name}: {valid_count} valid players - OK")  # ✅ Good - data validation
```

**Quality Assessment:**
- INFO logs appear appropriate (script start, major phases, significant outcomes)
- DEBUG logs provide useful detail without excessive noise
- Need full audit to verify all 197 calls meet criteria

---

## Discovery Context Integration

### Feature Scope (from DISCOVERY.md)

**Confirmed Scope:**
- ✅ Add --enable-log-file flag to run_win_rate_simulation.py (direct entry script)
- ✅ Replace hardcoded LOGGING_TO_FILE constant with CLI flag
- ✅ Apply DEBUG/INFO quality criteria to simulation/win_rate/ modules (7 files, 197 calls)
- ✅ Update affected test assertions (tests/root_scripts/test_root_scripts.py)

**Not in Scope:**
- ❌ Changes to accuracy_sim (Feature 04's responsibility)
- ❌ Changes to LoggingManager.py (Feature 01's responsibility)
- ❌ New logging infrastructure (Feature 01's responsibility)

---

## Feature 01 Dependency

### What Feature 01 Provides

**From feature_01_core_logging_infrastructure/spec.md:**

1. **LineBasedRotatingHandler class** - Custom handler with 500-line rotation
2. **Modified setup_logger() API** - Integrates new handler
3. **Centralized logs/{script_name}/ folder structure**
4. **Timestamped filenames:** {script_name}-{YYYYMMDD_HHMMSS}.log
5. **Max 50 files cleanup** per subfolder

**Integration Contracts (MUST follow):**
1. **Logger name = folder name:** Use consistent name (e.g., "win_rate_simulation" not variations)
2. **log_file_path=None:** Don't specify custom paths (let LoggingManager generate)
3. **log_to_file from CLI:** Wire --enable-log-file flag to log_to_file parameter

**Example from Feature 01 spec:**
```python
from utils.LoggingManager import setup_logger

logger = setup_logger(
    name="win_rate_simulation",     # Script name (becomes folder name)
    level="INFO",                    # Log level
    log_to_file=True,               # Enable file logging (CLI-driven)
    log_file_path=None,             # Let LoggingManager auto-generate path
    log_format="standard"           # Format style
)
# Result: logs/win_rate_simulation/win_rate_simulation-{timestamp}.log with 500-line rotation
```

---

## Test Impact Analysis

### Tests Requiring Updates

**File:** `tests/root_scripts/test_root_scripts.py`

**Current Assertion:**
```python
assert hasattr(run_win_rate_simulation, 'LOGGING_TO_FILE')
```

**Impact:** This assertion will FAIL after removing LOGGING_TO_FILE constant

**Required Fix:**
- Option A: Remove this assertion entirely
- Option B: Update to check for argparser with --enable-log-file flag
- **Recommendation:** Remove (checking for module constant is not valuable test)

---

## Open Questions

### For User (tracked in checklist.md)

1. **Q1: Logger Name** - Should logger name be "win_rate_simulation" or "simulation"?
   - Current code uses "simulation" (LOG_NAME constant line 35)
   - Feature 01 contract: logger name becomes folder name
   - Options:
     - A) Keep "simulation" → logs/simulation/ folder (may conflict with other simulation types)
     - B) Change to "win_rate_simulation" → logs/win_rate_simulation/ folder (more specific)

2. **Q2: Test Assertion** - How to handle failing test assertion?
   - tests/root_scripts/test_root_scripts.py checks for LOGGING_TO_FILE constant
   - Options:
     - A) Remove assertion entirely
     - B) Update to check for CLI flag in argparser
     - C) Keep constant as deprecated (for backward compatibility)

3. **Q3: Log Quality Audit Scope** - How thorough should log quality review be?
   - 197 logging calls across 7 files
   - Options:
     - A) Audit all 197 calls manually (2-3 hours)
     - B) Spot-check ~20% (30-40 calls) and document patterns (30-45 min)
     - C) Fix only obvious violations found during implementation

---

## Implementation Complexity

**Estimated Size:** SMALL-MEDIUM

**Breakdown:**
- CLI integration: SMALL (10-15 lines in run_win_rate_simulation.py)
- Test updates: TRIVIAL (1-2 lines removed)
- Log quality audit: MEDIUM (197 calls across 7 files, need systematic review)
- Log quality improvements: UNKNOWN (depends on audit findings)

**Risk Assessment:** LOW
- Entry script changes are straightforward (argparse patterns established)
- Log quality improvements are subjective but have clear criteria
- No architectural changes needed

---

## Notes

- Win rate simulation uses same LoggingManager pattern as other scripts
- Feature 01 spec provides clear integration contracts to follow
- Logger name decision affects folder structure (needs user input)
- Log quality criteria from Discovery Phase provide clear audit framework

---

**Research Complete:** 2026-02-06
**Next Step:** Draft spec.md based on these findings
