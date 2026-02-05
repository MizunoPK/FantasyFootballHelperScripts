# STAGE 2c: Refinement Phase - Detailed Examples

**Guide Version:** 1.0
**Created:** 2026-01-10
**Purpose:** Detailed examples and templates for Refinement Phase execution
**Prerequisites:** Read stages/s2/s2_p3_refinement.md first
**Main Guide:** stages/s2/s2_p3_refinement.md

---

## Purpose

This reference provides detailed examples for executing Refinement Phase (S2.P3). Use this alongside the main guide for:
- Example interactive question resolution
- Sample feature scope adjustments
- Cross-feature alignment comparisons
- Acceptance criteria templates

**Always read the main guide first.** This is a reference supplement, not a standalone guide.

---

## Phase 3 Examples: Interactive Question Resolution

### Example 1: Complete Question-Answer Cycle

**Agent asks Question 1:**

```markdown
I have a question about Feature 01 (ADP Integration):

## Question 1: ADP CSV Column Names

**Context:** I need to know the exact column names in the FantasyPros ADP CSV to parse it correctly. You mentioned "use FantasyPros CSV format" but didn't specify the structure.

**Options:**

A. **Assume standard format: Name, Position, ADP**
   - Pros: Common format, likely correct
   - Cons: Might be wrong, would require rework

B. **Ask you to provide sample CSV or column names**
   - Pros: Guaranteed correct, no guesswork
   - Cons: Requires you to provide file or info

C. **Support multiple formats with auto-detection**
   - Pros: Flexible, works with various sources
   - Cons: Complex, overkill for single data source

**My recommendation:** Option B - Can you provide the exact column names from the FantasyPros CSV, or share a sample file?

**What do you prefer?**
```

**User answers:**

```bash
The columns are: Name, Position, OverallRank

(Note: FantasyPros calls it "OverallRank" not "ADP")
```

**Agent updates IMMEDIATELY:**

**Update checklist.md:**

```markdown
### Question 1: ADP CSV Column Names
- [x] **RESOLVED:** Name, Position, OverallRank

**User's Answer:**
"The columns are: Name, Position, OverallRank (FantasyPros calls it 'OverallRank' not 'ADP')"

**Implementation Impact:**
- CSV parsing will use columns: ['Name', 'Position', 'OverallRank']
- Internal field name remains adp_value for clarity
- Update spec.md data structures section
- Update adp_loader implementation
```

**Update spec.md:**

```markdown
### Data Structure: ADP CSV Format

**Source:** User Answer to Checklist Question 1
**Traceability:** User confirmed on 2026-01-10

**CSV Format:**
```
Name,Position,OverallRank
Patrick Mahomes,QB,5
Christian McCaffrey,RB,1
Tyreek Hill,WR,8
```markdown

**Column Definitions:**
- **Name** (string): Player full name (e.g., "Patrick Mahomes")
- **Position** (string): Position abbreviation (QB, RB, WR, TE, K, DST)
- **OverallRank** (integer): ADP ranking from FantasyPros (1-300)
  - Note: FantasyPros uses "OverallRank" terminology, but we'll refer to it as ADP internally

**Implementation:**
```
# adp_loader.py
def load_adp_data(filepath: Path) -> Dict[str, int]:
    """Load ADP data from FantasyPros CSV.

    Args:
        filepath: Path to CSV file

    Returns:
        Dictionary mapping "name_position" to ADP value
    """
    df = read_csv_with_validation(
        filepath,
        required_columns=['Name', 'Position', 'OverallRank']
    )

    adp_dict = {}
    for _, row in df.iterrows():
        key = f"{row['Name']}_{row['Position']}"
        adp_dict[key] = int(row['OverallRank'])

    return adp_dict
```text
```

**Agent evaluates for new questions:**

```markdown
**New questions from this answer:**
- NONE - Answer was complete and clear

**Other questions resolved:**
- Question 4 (Player Key Format) - Implicitly answered
  - User provided Name and Position columns
  - Can use "name_position" as key
  - Mark Q4 as resolved with note
```

**Update checklist.md Question 4:**

```markdown
### Question 4: Player Matching Key Format
- [x] **RESOLVED:** Use "name_position" key (derived from Q1 answer)

**Context:** User's answer to Q1 confirmed CSV has Name and Position columns, which are sufficient for unique matching.

**Implementation:**
- Key format: "{name}_{position}" (e.g., "Patrick Mahomes_QB")
- Normalize both sources before matching (remove extra spaces, consistent casing)
```

**Agent moves to next question:**

```markdown
I have a question about Feature 01 (ADP Integration):

## Question 2: Valid ADP Value Range

**Context:** I need to know the min/max ADP values for validation and error handling. Your CSV might have different ranges depending on league depth.

**Options:**

A. **1-300 (standard 12-team league)**
   - Most common format
   - Assumes roster depth of ~25 players

B. **1-500 (deeper league)**
   - Supports 14-16 team leagues
   - More comprehensive rankings

C. **No upper limit validation**
   - Accept any positive integer
   - More flexible but less validation

**My recommendation:** Option A (1-300) since FantasyPros standard format is 12-team leagues, but confirm if you have deeper league.

**What ADP range does your league use?**
```

{Cycle continues for all questions...}

---

### Example 2: User Requests Clarification

**Agent asks Question 3:**

```markdown
## Question 3: ADP Multiplier Calculation Formula

**Context:** You said "factor ADP into draft recommendations" but didn't specify how much impact it should have. I need to know whether high-ADP players get a small boost or large boost.

**Options:**

A. **Config-based ranges**
   - Define in league_config.json: ADP 1-50 = 1.2x, 51-100 = 1.1x, etc.
   - Pros: Flexible, tune without code changes
   - Cons: Requires config updates

B. **Linear formula**
   - Formula: multiplier = 1.0 + ((300 - adp) / 300) * 0.2
   - Pros: Simple, continuous
   - Cons: Less control

C. **Exponential formula**
   - Higher impact for top picks
   - Pros: Reflects real draft value
   - Cons: Complex

**My recommendation:** Option A (config-based)

**What do you prefer?**
```

**User requests clarification:**

```text
Can you explain the difference in impact? Like, if Patrick Mahomes has ADP 5 vs a waiver wire player with no ADP, what's the scoring difference for each option?
```

**Agent provides clarification:**

```markdown
Good question! Let me illustrate with concrete examples:

**Scenario:** Patrick Mahomes (ADP 5) vs Backup QB (no ADP data)
- Base projected points: Mahomes 450, Backup 200

**Option A (Config-based):**
- Mahomes: ADP 5 → in range 1-50 → multiplier 1.2x → final score: 450 * 1.2 = 540
- Backup: No ADP → default 1.0x → final score: 200 * 1.0 = 200
- **Difference:** 60 point boost (13% increase)

**Option B (Linear):**
- Mahomes: multiplier = 1.0 + ((300-5)/300)*0.2 = 1.197x → 450 * 1.197 = 539
- Backup: No ADP → 1.0x → 200
- **Difference:** ~60 point boost (similar to config)

**Option C (Exponential):**
- Mahomes: multiplier = 1.0 + (300/5)*0.05 = 4.0x → 450 * 4.0 = 1800 (!)
- Backup: 200
- **Difference:** 1350 point boost (300% increase!) - probably too extreme

**Key differences:**
- **Config:** You can tune ranges exactly how you want
- **Linear:** Automatic calculation, but fixed impact
- **Exponential:** Very high impact for top picks (might be too much)

**My recommendation:** Start with config-based Option A with conservative multipliers:
- ADP 1-50: 1.15x (15% boost)
- ADP 51-100: 1.08x (8% boost)
- ADP 101-200: 1.03x (3% boost)
- ADP 201+: 1.0x (neutral)

This gives top picks a noticeable boost without dominating the scoring.

**Does that help clarify? Which option do you prefer?**
```

**User decides:**

```bash
Okay, config-based with your recommended ranges sounds good. Let's go with Option A.
```

**Agent updates IMMEDIATELY:**

{Same update process as Example 1...}

---

### Example 3: User Suggests Alternative

**Agent asks Question 5:**

```markdown
## Question 5: Behavior When ADP CSV Missing

**Context:** Need to handle case where ADP CSV file is missing or can't be read.

**Options:**

A. **Fail with error**
   - Stop execution, force user to provide file
   - Pros: Ensures data is loaded
   - Cons: Breaks draft helper if file missing

B. **Default all players to neutral (1.0)**
   - Log warning, continue without ADP
   - Pros: Graceful degradation
   - Cons: Silent failure

C. **Prompt for file location**
   - Interactive recovery
   - Pros: User-friendly
   - Cons: Requires interaction

**My recommendation:** Option B (graceful degradation)

**What do you prefer?**
```

**User suggests alternative:**

```text
How about a hybrid approach? Try to load the file, and if it fails, show a prominent warning but continue. However, if the user explicitly enabled --use-adp flag, then fail with error since they clearly wanted ADP data.

That way:
- Default behavior: graceful degradation
- Explicit ADP flag: fail if missing (user expects it)
```

**Agent incorporates alternative:**

```markdown
Excellent idea! That's better than my options. Let me update the spec with your hybrid approach:

**Updated Approach (User-Suggested):**

1. **Check if --use-adp flag provided (command-line argument)**

2. **If --use-adp flag:**
   - Try to load ADP CSV
   - If missing/unreadable: FAIL with clear error message
     - Error: "ADP CSV not found at {path}. Provide file or remove --use-adp flag."
   - Rationale: User explicitly requested ADP data, should fail if unavailable

3. **If NO --use-adp flag (default):**
   - Try to load ADP CSV
   - If missing/unreadable: Log WARNING, continue with all multipliers = 1.0
     - Warning: "ADP CSV not found, using neutral multipliers. Use --use-adp to require ADP data."
   - Rationale: Graceful degradation, doesn't break existing functionality

**Benefits of this approach:**
- ✅ Default behavior: robust, doesn't break
- ✅ Explicit mode: fail-fast, ensures data quality
- ✅ Clear messaging: user knows what happened

**I'll update the spec with this logic. Does that match your intent?**
```

**User confirms:**

```text
Perfect, that's exactly what I meant.
```

**Agent updates spec.md with alternative:**

```markdown
### Requirement 6: Handle Missing ADP CSV

**Description:** Gracefully handle missing or unreadable ADP CSV file, with behavior dependent on user intent

**Source:** User Answer to Checklist Question 5 (user-suggested hybrid approach)
**Traceability:** User confirmed on 2026-01-10

**Implementation:**

**1. Add command-line flag:**
```
# run_league_helper.py
parser.add_argument('--use-adp', action='store_true',
                   help='Require ADP data (fail if CSV missing)')
```markdown

**2. ADP loading logic:**
```
def load_adp_data_with_fallback(filepath: Path, require: bool = False) -> Dict[str, int]:
    """Load ADP data with graceful degradation or strict mode.

    Args:
        filepath: Path to ADP CSV
        require: If True, raise exception if file missing (--use-adp flag)

    Returns:
        Dictionary of ADP data, or empty dict if file missing (when require=False)

    Raises:
        FileNotFoundError: If require=True and file missing
    """
    try:
        return load_adp_data(filepath)
    except FileNotFoundError:
        if require:
            # User explicitly wanted ADP data, fail with clear error
            raise FileNotFoundError(
                f"ADP CSV not found at {filepath}. "
                f"Provide file or remove --use-adp flag."
            )
        else:
            # Default mode: graceful degradation
            logger.warning(
                f"ADP CSV not found at {filepath}. "
                f"Using neutral multipliers (1.0). "
                f"Use --use-adp to require ADP data."
            )
            return {}  # Empty dict, all players default to 1.0
```bash

**Edge Cases:**
- User runs `python run_league_helper.py` (no flag)
  - Missing CSV: WARNING logged, continues with multipliers = 1.0
- User runs `python run_league_helper.py --use-adp`
  - Missing CSV: ERROR raised, execution stops
- CSV exists but corrupt:
  - Same behavior as missing (handled by try/except)
```

---

## Phase 4 Examples: Dynamic Scope Adjustment

### Example 1: Feature Too Large (>35 Items) - Propose Split

```markdown
## Feature Scope Analysis: Feature 02 (Trade Analyzer)

**Current Status:**
- Checklist items: 42 items
- Threshold: 35 items (maximum for maintainability)
- **Assessment:** ⚠️ Feature is too large

**Why This Matters:**
- Features with >35 items are difficult to implement systematically
- Testing becomes complex (too many edge cases)
- Higher risk of bugs and missed requirements
- S5 implementation planning becomes unwieldy

**Checklist Breakdown:**
- Data loading: 8 items
- Trade evaluation logic: 12 items
- Multi-player trade handling: 15 items
- UI integration: 7 items

**Proposed Split:**

I recommend splitting this into 2 separate features:

**Feature 02a: Basic Trade Evaluator**
- Scope: 1-for-1 and 2-for-2 trades (simpler cases)
- Checklist items: ~20 items
- Includes:
  - Data loading (8 items)
  - Basic trade evaluation logic (7 items)
  - UI integration for simple trades (5 items)
- Rationale: Foundational functionality, most common use case

**Feature 02b: Multi-Player Trade Support**
- Scope: Complex trades (3+ players per side)
- Checklist items: ~15 items
- Includes:
  - Multi-player evaluation logic (10 items)
  - Advanced UI for complex trades (5 items)
- Rationale: Advanced functionality, builds on 02a
- Dependency: Must implement 02a first

**Benefits of Split:**
- ✅ Each feature <35 items (manageable scope)
- ✅ Clear dependency (02a → 02b)
- ✅ Can deliver basic functionality sooner
- ✅ Easier to test and validate each piece

**Dependencies:**
- Feature 02a: Independent (can start now)
- Feature 02b: Depends on 02a (implement after 02a complete)
- No circular dependencies

**Next Steps If Approved:**
1. Return to S1 to create new feature folders
   - `feature_02a_basic_trade_evaluator/`
   - `feature_02b_multi_player_trades/`
2. Split current spec.md and checklist.md
   - Move items 1-20 to 02a
   - Move items 21-35 to 02b
3. Update epic EPIC_README.md Feature Tracking table
4. Continue S2 for Feature 02a (implement first)
5. Then S2 for Feature 02b (implement second)

**Do you approve this split?** (or suggest alternative grouping)
```

**If user approves:**

```markdown
✅ User approved split on 2026-01-10

**Actions Taken:**
1. Created new feature folders:
   - feature_02a_basic_trade_evaluator/
   - feature_02b_multi_player_trades/
2. Split spec.md content:
   - 02a: Basic evaluation logic (20 items)
   - 02b: Multi-player support (15 items)
3. Updated EPIC_README.md Feature Tracking:
   | Feature | Name | S2 Complete |
   |---------|------|------------------|
   | 02a | Basic Trade Evaluator | [ ] |
   | 02b | Multi-Player Trades | [ ] |
4. Updated feature dependencies in specs

**Next Steps:**
- Resume S2 for Feature 02a (Research Phase)
- Complete 02a through S5
- Then begin S2 for Feature 02b
```

---

### Example 2: New Work Discovered - Create Separate Feature

```markdown
## New Work Discovered: Player Name Matching Utility

**What We Found:**

During question resolution for Feature 01 (ADP Integration), we discovered a need for player name matching logic. User confirmed need to:
- Normalize player names (remove periods, extra spaces)
- Handle common variations ("A.J. Brown" vs "AJ Brown")
- Match across multiple data sources (ADP CSV, injury reports, etc.)

**Current Feature:**
Feature 01: ADP Integration
- Original scope: Load ADP data, integrate into scoring
- Current checklist: 18 items

**New Work:**
Player Name Matching Utility
- Normalize names for consistent matching
- Handle initials, spacing variations, suffixes (Jr., Sr.)
- Provide utility function used by multiple features
- Estimated: 10-15 checklist items

**Assessment:**

This new work should be its own feature because:
1. **Independent subsystem:** Can be developed and tested independently
2. **Reusable:** Will be used by multiple features:
   - Feature 01: ADP Integration (match ADP CSV to players)
   - Feature 02: Injury Risk (match injury reports to players)
   - Feature 03: Schedule Strength (match team schedules to players)
3. **Clear interface:** Single utility function with well-defined inputs/outputs
4. **Testing isolation:** Can thoroughly test matching logic separately

**Recommendation:**

Create new Feature 05: Player Name Matching Utility

**Scope:**
- Name normalization function
- Matching algorithm (exact after normalization)
- Unit tests for various name formats
- Documentation of supported variations

**Dependencies:**
- Feature 01 will DEPEND on Feature 05
- Feature 02 will DEPEND on Feature 05
- Feature 03 will DEPEND on Feature 05
- Should implement Feature 05 FIRST (before 01, 02, 03)

**Impact on Current Feature (01):**
- Reduces Feature 01 scope by ~5 items (matching logic moved to 05)
- Feature 01 checklist goes from 18 → 13 items
- Feature 01 will call utility from Feature 05

**Alternative:**

Keep matching logic in Feature 01:
- Pros: Keeps all ADP logic together
- Cons: Duplicated code when Features 02 and 03 need same logic
- Cons: Harder to maintain (changes in 3 places)

**Do you want to create this as a separate feature?** (or keep in Feature 01)
```

**If user approves new feature:**

```markdown
✅ User approved separate feature on 2026-01-10

**Actions Taken:**
1. Created new feature folder:
   - feature_05_player_name_matching/
2. Updated EPIC_README.md Feature Tracking:
   | Feature | Name | S2 Complete | Priority |
   |---------|------|------------------|----------|
   | 05 | Player Name Matching | [ ] | HIGH (blocks 01,02,03) |
   | 01 | ADP Integration | [ ] | MEDIUM (after 05) |
   | 02 | Injury Risk | [ ] | MEDIUM (after 05) |
3. Updated feature dependencies:
   - Feature 01 spec.md: Added "Depends on: Feature 05"
   - Feature 02 spec.md: Added "Depends on: Feature 05"
   - Feature 05 spec.md: Added "Blocks: Features 01, 02, 03"
4. Reduced Feature 01 scope:
   - Removed 5 matching-related checklist items
   - Updated requirement to use utility from Feature 05
   - New checklist count: 13 items

**Next Steps:**
- Begin S2 for Feature 05 (high priority, blocks others)
- Complete Feature 05 through S5
- Then resume Feature 01 (can now use matching utility)
```

---

## Phase 5 Examples: Cross-Feature Alignment

### Example 1: Complete Feature Comparison

```markdown
# Alignment Check: Feature 02 vs Feature 01

**Date:** 2026-01-10
**Current Feature:** Feature 02: Injury Risk Assessment
**Comparison Target:** Feature 01: ADP Integration (S2 Complete)

---

## Comparison Categories

### 1. Components Affected

**Feature 02 modifies:**
- PlayerManager (calculate_total_score method)
- FantasyPlayer (add injury_risk field)
- InjuryDataLoader (new file)

**Feature 01 modifies:**
- PlayerManager (calculate_total_score method)
- FantasyPlayer (add adp_value field)
- ADPDataLoader (new file)

**Overlap Analysis:**
- ⚠️ Both modify PlayerManager.calculate_total_score()
  - Feature 01 adds: `total_score *= adp_multiplier`
  - Feature 02 adds: `total_score *= injury_multiplier`
  - **Conflict?** ❌ NO - Different multipliers, can coexist
  - **Resolution:** Both multiply into same total_score, order doesn't matter (multiplication is commutative)

- ⚠️ Both modify FantasyPlayer class
  - Feature 01 adds: adp_value, adp_multiplier fields
  - Feature 02 adds: injury_risk, injury_multiplier fields
  - **Conflict?** ❌ NO - Different fields, no overlap
  - **Resolution:** Both can add fields independently

**Verification:**
```
# After both features, FantasyPlayer will have:
@dataclass
class FantasyPlayer:
    # Existing fields
    name: str
    position: str
    # Feature 01 additions
    adp_value: Optional[int] = None
    adp_multiplier: float = 1.0
    # Feature 02 additions
    injury_risk: Optional[float] = None
    injury_multiplier: float = 1.0
```markdown

**Status:** ✅ No conflicts

---

### 2. Data Structures

**Feature 02 introduces:**
- Injury CSV format: Name, Position, InjuryStatus, RiskScore
- injury_risk field on FantasyPlayer (float, 0.0-1.0 range)

**Feature 01 introduces:**
- ADP CSV format: Name, Position, OverallRank
- adp_value field on FantasyPlayer (int, 1-300 range)

**Overlap Analysis:**
- ⚠️ Both use CSV files from data/ directory
  - Feature 01: data/adp_rankings.csv
  - Feature 02: data/injury_report.csv
  - **Conflict?** ❌ NO - Different files, different formats
  - **Resolution:** No overlap

- ⚠️ Both need to match players from CSV to player list
  - Feature 01: Uses player name matching (depends on Feature 05)
  - Feature 02: Uses player name matching (depends on Feature 05)
  - **Conflict?** ❌ NO - Both use same utility
  - **Resolution:** Both depend on Feature 05, consistent matching

**Status:** ✅ No conflicts

---

### 3. Requirements

**Feature 02 requirements:**
- Load injury data from CSV
- Calculate injury risk multiplier
- Apply multiplier in scoring

**Feature 01 requirements:**
- Load ADP data from CSV
- Calculate ADP multiplier
- Apply multiplier in scoring

**Overlap Analysis:**
- ✅ No duplicate requirements
- ✅ Similar patterns (both add multipliers) - this is intentional consistency
- ⚠️ Both depend on Feature 05 (player matching)
  - **Conflict?** ❌ NO - Both correctly specify dependency
  - **Resolution:** Feature 05 must be implemented first

**Status:** ✅ No conflicts, good consistency

---

### 4. Assumptions

**Feature 02 assumptions:**
- Injury CSV will be updated weekly (user responsibility)
- Missing injury data defaults to "healthy" (risk = 0.0, multiplier = 1.0)
- Injury risk calculated as: multiplier = 1.0 - (risk * 0.3)

**Feature 01 assumptions:**
- ADP CSV provided manually by user (no auto-updates)
- Missing ADP data defaults to neutral (multiplier = 1.0)
- ADP impact defined in config file

**Compatibility Check:**
- ✅ Compatible assumptions
- ⚠️ Both assume CSV files updated by user
  - This is consistent across features
  - Could suggest unified data update process (future enhancement)

**Status:** ✅ Compatible, no conflicts

---

### 5. Integration Points

**Does Feature 02 depend on Feature 01?**
- ❌ NO - Independent data sources, independent multipliers

**Does Feature 01 depend on Feature 02?**
- ❌ NO - Independent

**Do both depend on Feature 05?**
- ✅ YES - Both use player name matching utility

**Circular dependency?**
- ❌ NO

**Implementation order:**
1. Feature 05 (Player Matching) - FIRST (blocks both)
2. Features 01 and 02 can be parallel (after Feature 05)
3. No required sequence between 01 and 02

**Status:** ✅ No circular dependencies, clear order

---

## Summary

**Total Conflicts Found:** 0

**Critical Conflicts (must resolve):** NONE

**Minor Conflicts (nice to resolve):** NONE

**No Conflicts:**
- ✅ Components - Both modify PlayerManager but different logic
- ✅ Data Structures - Different CSV files, different fields
- ✅ Requirements - No duplicates, intentional consistency
- ✅ Assumptions - Compatible approaches
- ✅ Integration - Clear dependencies, no circular

**Action Items:**
- [ ] ✅ No changes needed to Feature 02 spec.md
- [ ] ✅ No changes needed to Feature 01 spec.md
- [ ] ✅ Document alignment verification in Feature 02 spec

**Alignment Status:** ✅ PASS - Zero conflicts, features are fully compatible
```

---

### Example 2: Alignment with Conflicts Found

```markdown
# Alignment Check: Feature 03 vs Feature 01 - CONFLICTS FOUND

**Date:** 2026-01-10
**Current Feature:** Feature 03: Schedule Strength Analysis
**Comparison Target:** Feature 01: ADP Integration (S2 Complete)

---

## Comparison Categories

### 1. Components Affected

**Feature 03 modifies:**
- PlayerManager (calculate_total_score method)
- FantasyPlayer (add schedule_strength field)
- ScheduleDataLoader (new file)
- **ConfigManager (add schedule multiplier config)**

**Feature 01 modifies:**
- PlayerManager (calculate_total_score method)
- FantasyPlayer (add adp_value field)
- ADPDataLoader (new file)
- **ConfigManager (add ADP multiplier config)**

**Overlap Analysis:**
- ⚠️ **CONFLICT: Both modify ConfigManager config structure**
  - Feature 01 spec: Add `adp_multipliers` section to league_config.json
  - Feature 03 spec: Add `schedule_multipliers` section to league_config.json
  - **Conflict?** ⚠️ POTENTIAL - Need to ensure compatible JSON structure
  - **Resolution:** Both features add separate sections, but need to coordinate format

**Feature 01 config format:**
```
{
  "adp_multipliers": {
    "ranges": [
      {"min": 1, "max": 50, "multiplier": 1.2}
    ]
  }
}
```markdown

**Feature 03 config format (from spec):**
```
{
  "schedule_strength": {
    "ranges": [
      {"min": 0.0, "max": 0.3, "bonus": 1.15}
    ]
  }
}
```markdown

**Issue:** Different field names for multiplier value:
- Feature 01 uses: `"multiplier": 1.2`
- Feature 03 uses: `"bonus": 1.15`

**Resolution:**
→ Standardize on `"multiplier"` field name for consistency
→ Update Feature 03 spec to use `"multiplier"` instead of `"bonus"`
→ This ensures consistent config pattern across all features

---

### 3. Requirements

**Feature 03 requirement:**
- Requirement 4: "Cache schedule data to avoid recalculating for each scoring call"

**Feature 01 requirement:**
- (No caching mentioned)

**Overlap Analysis:**
- ⚠️ **MINOR CONFLICT: Inconsistent caching strategy**
  - Feature 03 caches schedule data
  - Feature 01 doesn't mention caching for ADP data
  - **Impact:** Inconsistent performance characteristics

**Resolution Options:**

A. Add caching to Feature 01 (update spec)
   - Pros: Consistent performance across features
   - Cons: More complex implementation for Feature 01

B. Keep Feature 03 caching, Feature 01 without
   - Pros: Simpler for Feature 01
   - Cons: Inconsistent patterns
   - Justification: ADP data loaded once at startup, schedule data queried per player

**Recommendation:** Option B with justification:
- ADP data is static per session (loaded once)
- Schedule data may be dynamic (updated weekly)
- Caching makes sense for schedule, not necessary for ADP

**Action:** Add justification note to Feature 01 spec explaining why no caching

---

## Summary

**Total Conflicts Found:** 2

**Critical Conflicts (must resolve):**
1. **Config field name inconsistency**
   - Feature 01 uses "multiplier", Feature 03 uses "bonus"
   - Resolution: Update Feature 03 to use "multiplier" for consistency
   - Impact: Medium (affects implementation and config format)

**Minor Conflicts (nice to resolve):**
1. **Caching strategy inconsistency**
   - Feature 03 caches, Feature 01 doesn't
   - Resolution: Document justification (different use cases)
   - Impact: Low (explainable difference)

**Action Items:**
- [ ] Update Feature 03 spec.md: Change "bonus" field to "multiplier" in config format
- [ ] Update Feature 03 spec.md: Document why different from Feature 01 approach
- [ ] Update Feature 01 spec.md: Add note explaining no caching (static data)
- [ ] Verify both features after changes

**Alignment Status:** ⚠️ CONFLICTS FOUND - Must resolve before proceeding
```

**After resolving conflicts:**

```markdown
## Conflict Resolution - Feature 03 vs Feature 01

**Date:** 2026-01-10
**Status:** ✅ RESOLVED

**Conflict 1: Config field name - RESOLVED**
- Original conflict: Feature 01 used "multiplier", Feature 03 used "bonus"
- Resolution chosen: Standardize on "multiplier"
- Changes made:
  - Feature 03: Updated spec.md config format to use "multiplier" field
  - Updated ConfigManager section to match pattern
- Verified by: Agent
- Date: 2026-01-10 15:45

**Conflict 2: Caching strategy - RESOLVED**
- Original conflict: Feature 03 caches, Feature 01 doesn't
- Resolution chosen: Document justification (different use cases)
- Changes made:
  - Feature 01: Added note explaining no caching needed (static data loaded once)
  - Feature 03: Added note explaining caching needed (dynamic data queried frequently)
- Verified by: Agent
- Date: 2026-01-10 15:50

**Final Alignment Status:** ✅ PASS - All conflicts resolved, features now compatible
```

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
