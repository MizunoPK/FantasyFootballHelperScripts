# S2 Refinement Phase - Phase 6 Examples: Acceptance Criteria & User Approval

**Guide Version:** 1.0
**Created:** 2026-02-05 (Split from refinement_examples.md)
**Purpose:** Detailed examples for Phase 6 (Acceptance Criteria & User Approval)
**Prerequisites:** Read stages/s2/s2_p3_refinement.md Phase 6 first
**Main Guide:** stages/s2/s2_p3_refinement.md
**Parent Reference:** reference/stage_2/refinement_examples.md

---

## Purpose

This reference provides detailed examples specifically for **Phase 6: Acceptance Criteria & User Approval** of the Refinement Phase (S2.P3).

**What's Covered:**
- Acceptance criteria templates for different feature types
- User approval workflows (clean approval, approval with modifications)
- Handling approval feedback and iterations
- Final spec validation before S3

**When to Use:** During S2.P3 Phase 6 when creating acceptance criteria or preparing for Gate 3 (User Checklist Approval)

**Always read the main guide first.** This is a reference supplement, not a standalone guide.

---

## Phase 6 Examples: Acceptance Criteria & User Approval

### Example 1: Complete Acceptance Criteria

```markdown
---

## Acceptance Criteria (USER MUST APPROVE)

**Feature 01: ADP Integration**

When this feature is complete, the following will be true:

### Behavior Changes

**New Functionality:**
1. ADP data can be loaded from CSV file at `data/adp_rankings.csv`
   - File format: Name, Position, OverallRank columns
   - Loaded automatically during PlayerManager initialization
   - Players matched using name+position normalization (via Feature 05 utility)

2. Draft recommendations incorporate ADP multipliers
   - High ADP players (1-50) get 15% scoring boost
   - Mid ADP players (51-100) get 8% scoring boost
   - Lower ADP players get smaller or no boost
   - Players without ADP data use neutral 1.0x multiplier

3. Command-line flag `--use-adp` available
   - When enabled: Requires ADP CSV (fails if missing)
   - When disabled (default): Graceful degradation if CSV missing

**Modified Functionality:**
1. PlayerManager.calculate_total_score() includes ADP multiplier
   - Before: `total_score = base * injury * matchup * team`
   - After: `total_score = base * injury * matchup * team * adp`
   - Order of multiplication doesn't affect result (commutative)

2. FantasyPlayer class has new fields
   - Before: name, position, team, projected_points, injury_status
   - After: (all above) + adp_value, adp_multiplier
   - adp_value: Optional[int] (None if not in CSV)
   - adp_multiplier: float (default 1.0)

**No Changes:**
- Draft mode UI will not change (no visual indication of ADP)
- Trade analyzer will not use ADP (only draft recommendations)
- Other scoring multipliers (injury, matchup, team) unchanged
- PlayerManager public interface unchanged (no new parameters)

---

### Files Modified

**New Files Created:**
1. `league_helper/loaders/adp_loader.py`
   - Purpose: Load and parse ADP data from CSV
   - Exports:
     - `load_adp_data(filepath: Path) -> Dict[str, int]`
     - `load_adp_data_with_fallback(filepath: Path, require: bool) -> Dict[str, int]`
   - Lines: ~80 lines (loader + error handling)

2. `data/adp_rankings.csv` (template file)
   - Purpose: Example ADP data structure for users
   - Format: Name,Position,OverallRank header + sample rows
   - Note: Users must replace with actual FantasyPros data

3. `tests/league_helper/loaders/test_adp_loader.py`
   - Purpose: Test CSV loading, parsing, error handling
   - Tests: 12 unit tests
     - Valid CSV loading
     - Missing file handling
     - Invalid format handling
     - Player matching
     - Fallback behavior (require flag)

4. `tests/league_helper/util/test_PlayerManager_adp.py`
   - Purpose: Test ADP multiplier calculation and integration
   - Tests: 15 unit tests
     - ADP multiplier calculation (various ranges)
     - Missing ADP handling (default 1.0)
     - Integration with calculate_total_score
     - Config-based multiplier ranges

**Existing Files Modified:**
1. `league_helper/util/PlayerManager.py`
   - Lines modified: Approximately 125-180 (calculate_total_score region)
   - Changes:
     - `load_players()` method: Add call to load ADP data
     - `calculate_total_score()` method: Add ADP multiplier to calculation
   - Methods added:
     - `_calculate_adp_multiplier(player: FantasyPlayer) -> float` (new, ~25 lines)
   - Methods modified:
     - `calculate_total_score()`: Add 1 line for ADP multiplication
     - `load_players()`: Add 3 lines for ADP data loading

2. `league_helper/util/FantasyPlayer.py`
   - Lines modified: 15-25 (dataclass definition)
   - Changes:
     - Add field: `adp_value: Optional[int] = None`
     - Add field: `adp_multiplier: float = 1.0`

3. `league_helper/util/ConfigManager.py`
   - Lines modified: Approximately 180-220 (multiplier methods)
   - Methods added:
     - `get_adp_multiplier(adp: int) -> float` (new, ~20 lines)
   - Pattern: Follow existing get_injury_multiplier() structure

4. `data/league_config.json`
   - Section added: `adp_multipliers` with range configuration
   - Format:
     ```
     "adp_multipliers": {
       "ranges": [
         {"min": 1, "max": 50, "multiplier": 1.15},
         {"min": 51, "max": 100, "multiplier": 1.08},
         {"min": 101, "max": 200, "multiplier": 1.03},
         {"min": 201, "max": 500, "multiplier": 1.0}
       ]
     }
     ```text

5. `run_league_helper.py`
   - Lines modified: Argument parser section (~line 25)
   - Changes: Add `--use-adp` command-line flag
   - Usage: `python run_league_helper.py --use-adp`

---

### Data Structures

**New Data Structures:**
1. ADP Dictionary (internal)
   - Type: `Dict[str, int]`
   - Key format: "name_position" (e.g., "Patrick Mahomes_QB")
   - Value: ADP ranking (1-300)
   - Example: {"Patrick Mahomes_QB": 5, "Christian McCaffrey_RB": 1}

**Modified Data Structures:**
1. `FantasyPlayer` class
   - New fields:
     - `adp_value: Optional[int]` - ADP ranking from CSV (1-300), None if not found
     - `adp_multiplier: float` - Calculated multiplier (0.8-1.2 range), default 1.0
   - Location: league_helper/util/FantasyPlayer.py

2. Config JSON structure
   - New section: `adp_multipliers` with range-based multipliers
   - Format: List of range objects (min, max, multiplier)

---

### API/Interface Changes

**New Public Methods:**
1. `ADPDataLoader.load_adp_data(filepath: Path) -> Dict[str, int]`
   - Purpose: Load ADP data from CSV file
   - Parameters:
     - filepath: Path to ADP CSV (required columns: Name, Position, OverallRank)
   - Returns: Dictionary mapping player key to ADP value
   - Raises: FileNotFoundError if file missing, ValueError if invalid format

2. `ADPDataLoader.load_adp_data_with_fallback(filepath: Path, require: bool = False) -> Dict[str, int]`
   - Purpose: Load ADP data with optional graceful degradation
   - Parameters:
     - filepath: Path to ADP CSV
     - require: If True, raise exception on missing file (for --use-adp flag)
   - Returns: Dictionary of ADP data, or empty dict if file missing and require=False

3. `ConfigManager.get_adp_multiplier(adp: int) -> float`
   - Purpose: Get ADP multiplier from config based on ADP value
   - Parameters:
     - adp: ADP ranking (1-500)
   - Returns: Multiplier float (typically 0.8-1.2 range)

**Modified Public Methods:**
- NONE (PlayerManager.calculate_total_score signature unchanged)

**No API Changes:**
- PlayerManager public interface maintained (user constraint honored)
- Existing multiplier methods unchanged

---

### Testing

**New Tests:**
- Unit tests: 27 tests total
  - adp_loader tests: 12 tests
  - PlayerManager ADP tests: 15 tests
- Integration tests: 3 tests
  - Full scoring with all multipliers (including ADP)
  - CSV loading → player matching → multiplier calculation → scoring
- Test files: 2 new test files
  - `tests/league_helper/loaders/test_adp_loader.py`
  - `tests/league_helper/util/test_PlayerManager_adp.py`

**Test Coverage:**
- Target: 100% coverage for new code
- Edge cases covered:
  - Missing ADP CSV file (with and without --use-adp flag)
  - Player not in ADP data (defaults to 1.0 multiplier)
  - Invalid ADP values (<1 or >300)
  - Corrupt CSV format
  - Multiple players with similar names (matching logic)
  - Empty CSV file
  - Config file missing adp_multipliers section

---

### Dependencies

**This Feature Depends On:**
- Feature 05: Player Name Matching Utility (must be implemented first)
  - Uses normalize_player_name() function for CSV matching
  - Blocks: Cannot start Feature 01 implementation until Feature 05 complete

**Features That Depend On This:**
- NONE (Feature 01 is independent, doesn't block other features)

**External Dependencies:**
- FantasyPros ADP CSV data (user must provide)
- csv_utils.read_csv_with_validation() (already exists in codebase)
- No new Python package dependencies

---

### Edge Cases & Error Handling

**Edge Cases Handled:**
1. Player not in ADP CSV
   - Behavior: Set adp_value = None, adp_multiplier = 1.0 (neutral)
   - No error raised, graceful default

2. ADP CSV file missing
   - Default mode: Log WARNING, continue with all multipliers = 1.0
   - --use-adp mode: Raise FileNotFoundError with clear message

3. Invalid ADP value (< 1 or > 300)
   - Behavior: Log warning, use neutral multiplier 1.0
   - Validation in get_adp_multiplier()

4. Corrupt CSV format (missing columns, wrong types)
   - Behavior: Raise ValueError with specific error message
   - Caught by read_csv_with_validation()

5. Multiple players with same name
   - Behavior: Match using name+position key (normalization from Feature 05)
   - Example: "Mike Williams_WR" (LAC) vs "Mike Williams_WR" (was on NYJ)
   - Note: Normalization handles this, but still potential ambiguity (user data quality)

**Error Conditions:**
1. ADP CSV not found (--use-adp mode)
   - User sees: "ADP CSV not found at data/adp_rankings.csv. Provide file or remove --use-adp flag."
   - System does: Raises FileNotFoundError, stops execution

2. ADP CSV invalid format
   - User sees: "Invalid ADP CSV format: missing required columns [OverallRank]"
   - System does: Raises ValueError, stops execution

3. Config missing adp_multipliers section
   - User sees: "Config missing adp_multipliers section, using default ranges"
   - System does: Log warning, use hardcoded default ranges

---

### Documentation

**User-Facing Documentation:**
- README.md updated with:
  - "ADP Integration" section under Features
  - How to provide ADP CSV data
  - --use-adp flag usage
  - Example ADP CSV format
- Examples added:
  - Sample data/adp_rankings.csv with 10 example players
  - Command-line usage: `python run_league_helper.py --use-adp`

**Developer Documentation:**
- Docstrings added to:
  - adp_loader.py: All public functions
  - PlayerManager._calculate_adp_multiplier(): Implementation details
  - ConfigManager.get_adp_multiplier(): Config format and range logic
- Architecture docs: No updates needed (follows existing multiplier pattern)

---

## User Approval

- [ ] **I approve these acceptance criteria**

**Approval Timestamp:** {To be filled after user approval}

**Approval Notes:**
{Any clarifications or modifications requested by user}

---

**Next Steps After Approval:**
1. Agent marks approval checkbox [x]
2. Agent documents approval timestamp
3. Agent updates Feature Tracking in EPIC_README.md
4. Agent proceeds to next feature OR S3 (if all features complete)
```

---

### Example 2: User Approval Process

**Agent presents acceptance criteria:**

```markdown
## Feature 01 (ADP Integration) - Ready for Approval

I've completed the deep dive for Feature 01. Here's a summary:

**Spec Status:**
- All 6 checklist questions resolved (user answers incorporated)
- Cross-feature alignment complete (compared to Feature 00, zero conflicts)
- Scope validated (13 checklist items, within limits)

**What This Feature Will Do:**
Load ADP data from FantasyPros CSV and factor it into draft recommendations as a scoring multiplier, following the same pattern as existing injury/matchup multipliers.

**Impact:**
- Files modified: 2 new files (adp_loader.py, template CSV), 5 existing files modified
- New fields on FantasyPlayer: adp_value, adp_multiplier
- Command-line flag: --use-adp (optional strict mode)
- Test coverage: 27 new unit tests, 3 integration tests

**Full Details:**

Please review the "Acceptance Criteria" section in spec.md:
`feature-updates/KAI-1-improve_draft_helper/feature_01_adp_integration/spec.md`

**Acceptance Criteria Section includes:**
- Exact behavior changes (what's new, what's modified, what's unchanged)
- All files that will be modified (new: 4 files, modified: 5 files)
- Data structure changes (new fields on FantasyPlayer, new config section)
- API/interface changes (3 new methods, zero breaking changes)
- Testing approach (27 unit tests, 100% coverage)
- Edge cases and error handling (5 edge cases documented)
- Documentation updates (README + docstrings)

**Next Steps:**

If you approve these acceptance criteria:
- I'll mark the approval checkbox and timestamp
- I'll mark Feature 01 as "S2 Complete" in epic tracking
- I'll proceed to next feature (Feature 02) or S3 if all features done

If you want changes:
- Let me know what to modify
- I'll update the spec and re-present for approval

**Do you approve these acceptance criteria?**
```

**User reviews and approves:**

```text
Yes, this looks good. I approve.

One minor note: For the --use-adp flag documentation, can you emphasize that it's optional? I don't want users to think they HAVE to use it.
```

**Agent updates with approval:**

```markdown
✅ Approved! Thank you.

I'll update the documentation to emphasize the flag is optional.

**Updated Documentation Section:**

**User-Facing Documentation:**
- README.md updated with:
  - "ADP Integration (Optional)" section under Features
  - **Emphasis: --use-adp flag is OPTIONAL**
    - Default behavior: Works with or without ADP data (graceful)
    - Optional strict mode: Use --use-adp to require ADP data
  - How to provide ADP CSV data (if desired)
  - Example ADP CSV format

**Marking approval in spec.md:**

```
## User Approval

- [x] **I approve these acceptance criteria**

**Approval Timestamp:** 2026-01-10 16:20

**Approval Notes:**
User approved on 2026-01-10 with request to emphasize --use-adp flag is optional (not required). Updated documentation section to clarify default behavior works with or without ADP data.
```markdown

**Updating Feature Tracking:**

```
## Feature Tracking (in EPIC_README.md)

| Feature | Name | S2 Complete | S5 Complete | Status |
|---------|------|------------------|------------------|--------|
| 01 | ADP Integration | [x] 2026-01-10 | [ ] | S2 Done |
| 02 | Injury Risk | [ ] | [ ] | In Progress |
```markdown

**Next: Begin S2 for Feature 02 (Injury Risk Assessment)**

Would you like me to start Feature 02, or do you want to review anything else about Feature 01?
```

---

## Success Criteria Summary

**Refinement Phase (S2.P3) passes when:**

✅ **Phase 3 (Interactive Question Resolution):**
- All checklist questions resolved (zero open items)
- Each question asked ONE AT A TIME
- Spec and checklist updated IMMEDIATELY after each answer
- New questions evaluated after each answer
- User answers documented verbatim or paraphrased

✅ **Phase 4 (Dynamic Scope Adjustment):**
- Checklist item count documented
- If >35 items: Split proposed to user, user decided
- If new work discovered: Evaluated (new feature vs expanded scope)
- Scope adjustments documented

✅ **Phase 5 (Cross-Feature Alignment):**
- Compared to ALL features with "S2 Complete"
- Systematic pairwise comparison performed
- Conflicts identified (if any)
- Conflicts resolved or user consulted
- Alignment verification documented in spec.md

✅ **Phase 6 (Acceptance Criteria & User Approval):**
- Acceptance Criteria section created in spec.md
- Complete coverage: behavior, files, structures, API, tests, edge cases, docs
- Presented to user for approval
- User APPROVED (explicit confirmation)
- Approval checkbox marked [x]
- Approval timestamp documented

**Ready for next feature or S3 when all phases complete with user approval.**

---

*End of refinement_examples.md*
