# STAGE 2b: Specification Phase - Detailed Examples

**Guide Version:** 1.0
**Created:** 2026-01-10
**Purpose:** Detailed examples and templates for Specification Phase execution
**Prerequisites:** Read stages/stage_2/phase_1_specification.md first
**Main Guide:** stages/stage_2/phase_1_specification.md

---

## Purpose

This reference provides detailed examples for executing Specification Phase (STAGE_2b). Use this alongside the main guide for:
- Example spec.md sections with requirement traceability
- Sample checklist.md with valid questions
- Alignment check examples
- Real-world specification patterns

**Always read the main guide first.** This is a reference supplement, not a standalone guide.

---

## Phase 2 Examples: Spec & Checklist with Traceability

### Example 1: Components Affected Section (with sources)

```markdown
## Components Affected

**Classes to Modify:**

1. **PlayerManager** (`league_helper/util/PlayerManager.py`)
   - **Source:** Epic notes line 35: "integrate into PlayerManager scoring"
   - **Traceability:** Direct user request
   - **Changes:**
     - `calculate_total_score()` method (line 125) - Add ADP multiplier to calculation
       - Current: `total_score = base * injury * matchup * team`
       - New: `total_score = base * injury * matchup * team * adp`
     - `load_players()` method (line 89) - Call new ADP loader
     - New method: `_calculate_adp_multiplier(player: FantasyPlayer) -> float`
       - Pattern: Follow existing multiplier methods (line 450-550)
       - Returns: Float multiplier based on player.adp_value

2. **ConfigManager** (`league_helper/util/ConfigManager.py`)
   - **Source:** Derived from user request (need configuration for ADP multiplier ranges)
   - **Traceability:** User requested ADP integration (epic line 15), configuration is necessary to define multiplier ranges (similar to existing injury/matchup config)
   - **Changes:**
     - New method: `get_adp_multiplier(adp: int) -> float`
       - Pattern: Similar to get_injury_multiplier() at line 180
       - Input: ADP value (1-500 range, TBD - add to checklist Q2)
       - Output: Float multiplier
     - New config keys in league_config.json:
       - `adp_ranges`: Define ADP value ranges (TBD format - add to checklist Q3)
       - `adp_multipliers`: Define multiplier for each range

3. **FantasyPlayer** (`league_helper/util/FantasyPlayer.py`)
   - **Source:** Derived from user request (need to store ADP data per player)
   - **Traceability:** User requested "integrate ADP data" (epic line 15), storing ADP value on player object is logically required
   - **Changes:**
     - Add field: `adp_value: Optional[int] = None`
       - Type: Optional int (None if player not in ADP data)
       - Range: 1-500 (TBD - verify with user in checklist Q2)
     - Add field: `adp_multiplier: float = 1.0`
       - Type: Float
       - Default: 1.0 (neutral, no bonus/penalty)
       - Calculated: Set by _calculate_adp_multiplier()

**New Files to Create:**

1. `league_helper/loaders/adp_loader.py` (NEW)
   - **Source:** Derived requirement (need dedicated loader for ADP data)
   - **Traceability:** User specified "use FantasyPros CSV" (epic line 22), loading CSV requires dedicated loader module
   - **Purpose:** Load and parse ADP data from CSV
   - **Exports:**
     - `load_adp_data(filepath: Path) -> Dict[str, int]`
       - Returns: Dictionary mapping player key to ADP value
       - Player key format: TBD (add to checklist Q4 - "name" or "name_position"?)

2. `data/adp_rankings.csv` (NEW)
   - **Source:** Epic notes line 22: "use FantasyPros CSV format"
   - **Traceability:** Direct user request for data source
   - **Format:** TBD (add to checklist Q1 - ask user for exact format)
   - **Expected columns:** Name, Position, ADP (TBD - verify with user)

3. `tests/league_helper/util/test_PlayerManager_adp.py` (NEW)
   - **Source:** Derived requirement (all new features require tests)
   - **Traceability:** Standard practice (100% test coverage required per project standards)
   - **Purpose:** Test ADP multiplier calculation and integration
   - **Pattern:** Follow test_PlayerManager_scoring.py structure (verified in Phase 1)

4. `tests/league_helper/loaders/test_adp_loader.py` (NEW)
   - **Source:** Derived requirement (new loader requires tests)
   - **Traceability:** Standard practice
   - **Purpose:** Test CSV loading, parsing, error handling
```

---

### Example 2: Requirements Section (with full traceability)

```markdown
## Requirements

### Requirement 1: Load ADP Data from CSV

**Description:** Load Average Draft Position (ADP) data from FantasyPros CSV file and match to existing players

**Source:** Epic notes line 15: "integrate ADP data from FantasyPros"
**Traceability:** Direct user request

**Implementation:**
- Load CSV during PlayerManager initialization (in load_players() method)
- Use csv_utils.read_csv_with_validation() for robust loading
- Match players to ADP data using player key (TBD format - checklist Q4)
- Store ADP value in player.adp_value field

**Edge Cases:**
- CSV file missing: TBD behavior (checklist Q5 - fail or default to neutral?)
- Player not in CSV: Set adp_value = None, adp_multiplier = 1.0
- Invalid ADP value: TBD validation (checklist Q2 - valid range?)

**Dependencies:**
- csv_utils.read_csv_with_validation() (exists, verified in Phase 1)
- adp_loader.load_adp_data() (new, to be created)

---

### Requirement 2: Calculate ADP Multiplier

**Description:** Convert ADP value (1-500 range) to multiplier for scoring calculation

**Source:** Epic notes line 18-19: "factor ADP into draft recommendations so high-ADP players rank higher"
**Traceability:** Direct user request

**Implementation:**
- New method: PlayerManager._calculate_adp_multiplier(player: FantasyPlayer) -> float
- Pattern: Follow existing multiplier methods (injury, matchup, team)
- Input: player.adp_value (Optional[int])
- Output: Float multiplier
  - High ADP (1-50): Multiplier > 1.0 (bonus) - TBD exact values (checklist Q3)
  - Mid ADP (51-200): Multiplier ~1.0 (neutral) - TBD
  - Low ADP (201+): Multiplier = 1.0 (neutral) - TBD
  - Missing ADP (None): Multiplier = 1.0 (neutral)

**Algorithm:** TBD (checklist Q3 - linear, exponential, or config-based?)

**Dependencies:**
- ConfigManager.get_adp_multiplier() (new, to be created)
- Player must have adp_value populated (Requirement 1)

---

### Requirement 3: Integrate ADP Multiplier into Scoring

**Description:** Apply ADP multiplier in calculate_total_score() alongside existing multipliers

**Source:** Epic notes line 37-38: "Keep it simple - just add ADP as another multiplier like injury penalty"
**Traceability:** Direct user request (user specified implementation pattern)

**Implementation:**
- Modify PlayerManager.calculate_total_score() method
- Current calculation:
  ```python
  total_score = base_score * injury_mult * matchup_mult * team_mult
  ```
- New calculation:
  ```python
  adp_mult = self._calculate_adp_multiplier(player)
  total_score = base_score * injury_mult * matchup_mult * team_mult * adp_mult
  ```
- Maintain interface: No parameter changes (user constraint epic line 35)

**Dependencies:**
- Requirement 2 complete (_calculate_adp_multiplier method exists)
- Player must have adp_multiplier calculated

---

### Requirement 4: Handle Missing Player Data

**Description:** Gracefully handle players not in ADP data

**Source:** Derived requirement
**Traceability:** Not all players may have ADP data (rookies, obscure players), system must handle gracefully to avoid crashes

**Implementation:**
- If player not in ADP CSV: Set adp_value = None
- _calculate_adp_multiplier() behavior when adp_value is None:
  - Return 1.0 (neutral multiplier, no bonus/penalty)
  - Pattern: Same as injury multiplier when status unknown
- Optional: Log warning for missing players (TBD - checklist Q6)

**Edge Cases:**
- Entire ADP CSV missing: TBD (checklist Q5 - fail or all players neutral?)
- Player name mismatch: Won't find in CSV, treated as missing (neutral 1.0)

---

### Requirement 5: Configuration for ADP Multiplier Ranges

**Description:** Define ADP value ranges and corresponding multipliers in configuration file

**Source:** Derived requirement
**Traceability:** User requested "factor ADP into scoring" but didn't specify formula. Config-based approach allows flexibility without code changes.

**Implementation:**
- Add to data/league_config.json:
  ```json
  "adp_multipliers": {
    "ranges": [
      {"min": 1, "max": 50, "multiplier": 1.2},
      {"min": 51, "max": 100, "multiplier": 1.1},
      {"min": 101, "max": 200, "multiplier": 1.0},
      {"min": 201, "max": 500, "multiplier": 1.0}
    ]
  }
  ```
  (Note: Exact ranges/values TBD - checklist Q3)

- ConfigManager.get_adp_multiplier(adp: int) implementation:
  - Find range containing ADP value
  - Return corresponding multiplier
  - Default to 1.0 if ADP out of range

**Alternative:** Linear or exponential formula (checklist Q3 - ask user preference)

---

**Requirements Summary:**

- ✅ Requirement 1: Direct user request (epic line 15)
- ✅ Requirement 2: Direct user request (epic line 18-19)
- ✅ Requirement 3: Direct user request (epic line 37-38)
- ✅ Requirement 4: Derived (logically necessary for robustness)
- ✅ Requirement 5: Derived (implementation detail for Requirement 2)

**Total Requirements:** 5 (all traced to sources)
**User Requests:** 3 direct, 2 derived
**Assumptions:** 0 (all TBD items moved to checklist as questions)
```

---

### Example 3: Valid Checklist Questions

```markdown
# Feature 01: ADP Integration - Planning Checklist

**Purpose:** Track open questions and decisions for this feature

**Instructions:**
- [ ] = Open question (needs user answer)
- [x] = Resolved (answer documented below)

---

## Open Questions

### Question 1: ADP CSV Format and Columns

- [ ] What are the exact column names in the FantasyPros ADP CSV?

**Context:** Need to know exact column names to parse CSV correctly. User mentioned "FantasyPros CSV" but didn't specify structure.

**Epic reference:** Line 22: "use FantasyPros CSV format" (format not detailed)

**Options:**
A. Ask user to provide sample CSV or column names
B. Assume standard format: Name, Position, ADP
C. Support multiple formats with auto-detection

**Recommendation:** Option A - Ask user for actual file or column names to ensure correct parsing

**Why this is a question:** Cannot assume CSV structure without seeing actual file or user confirmation

**Impact on spec.md:** Will update data structures section with exact column names and parsing logic

---

### Question 2: Valid ADP Value Range

- [ ] What is the valid range for ADP values?

**Context:** Need to know min/max ADP values for validation and multiplier calculation.

**Epic reference:** Not mentioned in epic

**Options:**
A. 1-300 (typical for standard leagues)
B. 1-500 (deeper leagues)
C. No upper limit (any positive integer)

**Recommendation:** Option A (1-300) unless user has deeper league

**Why this is a question:** User didn't specify league depth or ADP range

**Impact on spec.md:** Will update validation logic and ConfigManager ranges

---

### Question 3: ADP Multiplier Calculation Formula

- [ ] How should ADP value translate to scoring multiplier?

**Context:** User said "factor ADP into scoring" but didn't specify how much impact it should have.

**Epic reference:** Line 18-19: "factor ADP into draft recommendations so high-ADP players rank higher" (no formula specified)

**Options:**
A. **Config-based ranges** (recommended)
   - Define ranges in league_config.json
   - Example: ADP 1-50 = 1.2x, 51-100 = 1.1x, 101+ = 1.0x
   - Pros: Flexible, easy to tune without code changes
   - Cons: Requires config file updates

B. **Linear formula**
   - Formula: multiplier = 1.0 + ((300 - adp) / 300) * 0.2
   - Example: ADP 1 = 1.2x, ADP 150 = 1.1x, ADP 300 = 1.0x
   - Pros: Simple, continuous
   - Cons: Less control over ranges

C. **Exponential formula**
   - Formula: multiplier = 1.0 + (300 / adp) * 0.05
   - Example: ADP 1 = 1.15x, ADP 50 = 1.03x, ADP 300 = 1.0x
   - Pros: Higher impact for top picks
   - Cons: Complex, harder to tune

**Recommendation:** Option A (config-based) - Most flexible, follows existing pattern (injury/matchup use config)

**Why this is a question:** User specified integration but not formula or impact level

**Impact on spec.md:** Will update algorithm section and ConfigManager implementation details

---

### Question 4: Player Matching Strategy

- [ ] How should we match players between ADP CSV and player list?

**Context:** Player names might vary between data sources (e.g., "A.J. Brown" vs "AJ Brown").

**Epic reference:** Not mentioned in epic

**Options:**
A. **Exact match on Name+Position**
   - Match: name == name AND position == position
   - Pros: Simple, no false positives
   - Cons: Misses players with name variations

B. **Name normalization then exact match**
   - Normalize: Remove periods, extra spaces, convert to lowercase
   - Then match: normalized_name == normalized_name AND position == position
   - Pros: Handles common variations (initials, spacing)
   - Cons: Still misses some cases (nicknames)

C. **Fuzzy matching (Levenshtein distance)**
   - Match if name similarity > threshold AND position matches
   - Pros: Handles more variations
   - Cons: Potential false positives, slower

**Recommendation:** Option B (normalization) - Balanced approach, handles 90% of cases without false positives

**Why this is a question:** User didn't specify matching logic, data source variations are common

**Impact on spec.md:** Will add player matching utility and update load_adp_data implementation

---

### Question 5: Behavior When ADP CSV Missing

- [ ] What should happen if the ADP CSV file is missing or unreadable?

**Context:** Need to handle case where user hasn't provided ADP data yet or file path is wrong.

**Epic reference:** Not mentioned in epic

**Options:**
A. **Fail with clear error message**
   - Raise exception, stop execution
   - Pros: Forces user to provide data
   - Cons: Breaks draft helper if file missing

B. **Default all players to neutral (1.0 multiplier)**
   - Log warning, continue with all adp_multiplier = 1.0
   - Pros: Graceful degradation, doesn't break functionality
   - Cons: Silent failure (user might not notice)

C. **Prompt user for file location**
   - Interactive: Ask user to provide file path
   - Pros: Recoverable, user-friendly
   - Cons: Requires interactive input

**Recommendation:** Option B (graceful degradation) with prominent warning log

**Why this is a question:** Error handling strategy not specified by user

**Impact on spec.md:** Will update edge case handling and error strategy sections

---

### Question 6: Logging for Missing Player Matches

- [ ] Should we log warnings when players aren't found in ADP data?

**Context:** Some players (rookies, obscure) might not have ADP data. Decide on logging verbosity.

**Epic reference:** Not mentioned in epic

**Options:**
A. **Log warning for each missing player**
   - Pros: User aware of missing data
   - Cons: Verbose output if many missing

B. **Log summary only** (e.g., "15 players not in ADP data")
   - Pros: Cleaner output
   - Cons: User doesn't know which players

C. **No logging** (silent default to 1.0 multiplier)
   - Pros: Clean output
   - Cons: User unaware of missing data

**Recommendation:** Option B (summary only) - Balance between awareness and verbosity

**Why this is a question:** Logging preference not specified by user

**Impact on spec.md:** Will update logging section and implementation details

---

## Resolved Questions

{Will populate as questions are answered}

---

## Questions NOT to Ask (Should Have Researched)

**❌ BAD QUESTION: "Which file contains PlayerManager?"**
→ This should have been found in Phase 1 research

**❌ BAD QUESTION: "Does PlayerManager have a scoring method?"**
→ This should have been verified in Phase 1.5 audit

**❌ BAD QUESTION: "What's the pattern for adding new multipliers?"**
→ This should have been documented by reading injury penalty code

**❌ BAD QUESTION: "How do we load CSV files?"**
→ This should have been researched (csv_utils exists, verified in Phase 1)

**Good questions ask about:**
✅ User preferences (Option A vs B vs C)
✅ Business logic not in epic (multiplier formula)
✅ Edge case handling (missing data behavior)
✅ External data formats (CSV column names from FantasyPros)
```

---

## Phase 2.5 Examples: Spec-to-Epic Alignment Check

### Example 1: Alignment Check - PASSING

```markdown
## Phase 2.5 Alignment Summary

### Requirement Source Verification

**Requirement 1: Load ADP Data**
- Source: Epic Request (line 15)
- Citation: ✅ "integrate ADP data from FantasyPros"
- Valid: ✅ YES

**Requirement 2: Calculate ADP Multiplier**
- Source: Epic Request (line 18-19)
- Citation: ✅ "factor ADP into draft recommendations"
- Valid: ✅ YES

**Requirement 3: Integrate into Scoring**
- Source: Epic Request (line 37-38)
- Citation: ✅ "add ADP as another multiplier like injury penalty"
- Valid: ✅ YES

**Requirement 4: Handle Missing Data**
- Source: Derived
- Derivation: ✅ "Not all players may have ADP data, must handle gracefully"
- Valid: ✅ YES

**Requirement 5: Configuration**
- Source: Derived
- Derivation: ✅ "User requested integration but not formula, config allows flexibility"
- Valid: ✅ YES

**All requirements have valid sources:** ✅ YES

---

### Scope Creep Check

**Reviewed each requirement against Epic Intent:**

**Requirement 1 (Load ADP Data):**
- User asked for this: ✅ YES (epic line 15: "integrate ADP data")
- Match: ✅ PERFECT

**Requirement 2 (Calculate Multiplier):**
- User asked for this: ✅ YES (epic line 18-19: "factor ADP into scoring")
- Match: ✅ PERFECT

**Requirement 3 (Integrate Scoring):**
- User asked for this: ✅ YES (epic line 37-38: "add as multiplier")
- Match: ✅ PERFECT

**Requirement 4 (Handle Missing):**
- User asked for this: ⚠️ NOT EXPLICITLY
- Necessary: ✅ YES (logically required to avoid crashes)
- Scope creep: ❌ NO (derived requirement, necessary for robustness)

**Requirement 5 (Configuration):**
- User asked for this: ⚠️ NOT EXPLICITLY
- Necessary: ✅ YES (implementation detail for Req 2)
- Scope creep: ❌ NO (derived requirement, follows existing pattern)

**Scope Creep Found:** ❌ NONE

**All requirements either:**
- ✅ Directly requested by user, OR
- ✅ Logically necessary to fulfill user request

---

### Missing Requirements Check

**Re-read Epic Intent section - User's explicit requests:**

1. "integrate ADP data from FantasyPros" (line 15)
   → Found in spec: ✅ Requirement 1

2. "factor ADP into draft recommendations so high-ADP players rank higher" (line 18-19)
   → Found in spec: ✅ Requirement 2 + 3

3. "use FantasyPros CSV format" (line 22)
   → Found in spec: ✅ Requirement 1 (data structures section)

4. "Don't change PlayerManager interface too much" (line 35 - constraint)
   → Found in spec: ✅ Requirement 3 (maintains interface, no parameter changes)

5. "Keep it simple - add ADP as multiplier like injury penalty" (line 37-38)
   → Found in spec: ✅ Requirement 3 (follows multiplier pattern)

**Missing Requirements Found:** ❌ NONE

**All user requests are in spec.**

---

### OVERALL RESULT: ✅ PASSED

**Summary:**
- ✅ All requirements have valid sources (3 Epic Request, 2 Derived)
- ✅ No scope creep detected
- ✅ No missing requirements
- ✅ All user constraints honored

**Alignment Evidence:**
- Requirements aligned with epic: 5/5 (100%)
- Scope creep removed: 0 requirements
- Missing requirements added: 0 requirements
- Final requirement count: 5 (all traced to sources)

**Ready for STAGE_2c:** ✅ YES

**Next Action:** Present checklist to user (Gate 2) or proceed to STAGE_2c Phase 3
```

---

### Example 2: Alignment Check - FAILED (Scope Creep Detected)

```markdown
## Phase 2.5 Alignment Summary - FAILED EXAMPLE

### Requirement Source Verification

{Requirements 1-5 same as passing example...}

**Requirement 6: Historical ADP Tracking** ❌
- Source: ⚠️ "Best practice for trend analysis"
- Citation: ❌ NOT in epic notes
- Valid: ❌ NO - This is scope creep

**Requirement 7: Automatic ADP Updates** ❌
- Source: ⚠️ "Nice to have for automation"
- Citation: ❌ NOT in epic notes
- Valid: ❌ NO - User explicitly excluded (epic line 45: "manual CSV for now")

**Issues found:** ❌ 2 requirements have invalid sources

---

### Scope Creep Check

**Requirement 6 (Historical ADP Tracking):**
- User asked for this: ❌ NO
- User explicitly excluded: ✅ YES (epic line 42: "Don't worry about historical ADP trends")
- **Assessment:** 🚨 SCOPE CREEP - User said NOT to include this
- **Action:** REMOVE from spec, this is out of scope

**Requirement 7 (Automatic Updates):**
- User asked for this: ❌ NO
- User explicitly excluded: ✅ YES (epic line 45: "Automatic updates can come later, manual CSV for now")
- **Assessment:** 🚨 SCOPE CREEP - User said "later", not now
- **Action:** REMOVE from spec, add to questions.md as "Future Enhancement?"

**Scope Creep Found:** ✅ YES - 2 requirements

---

### OVERALL RESULT: ❌ FAILED

**Failures:**
- ❌ 2 requirements are scope creep (Req 6, 7)
- ❌ User explicitly excluded these features
- ❌ Cannot proceed with these in spec

**Required Actions:**
1. REMOVE Requirement 6 from spec.md
2. REMOVE Requirement 7 from spec.md
3. Add note to questions.md: "User deferred historical tracking and auto-updates to future"
4. Re-run Phase 2.5 alignment check
5. Do NOT proceed to STAGE_2c until PASSED

**Lesson:** Read "Out of Scope" section in Epic Intent. User explicitly said what NOT to include.
```

---

### Example 3: Alignment Check - FAILED (Missing Requirement)

```markdown
## Phase 2.5 Alignment Summary - FAILED EXAMPLE

### Missing Requirements Check

**Re-read Epic Intent section - User's explicit requests:**

1. "integrate ADP data from FantasyPros" (line 15)
   → Found in spec: ✅ Requirement 1

2. "factor ADP into draft recommendations so high-ADP players rank higher" (line 18-19)
   → Found in spec: ✅ Requirement 2 + 3

3. "use FantasyPros CSV format" (line 22)
   → Found in spec: ✅ Requirement 1

4. "show ADP value in draft recommendations UI" (line 28)
   → Found in spec: ❌ MISSING - Not in any requirement!

5. "Don't change PlayerManager interface too much" (line 35)
   → Found in spec: ✅ Requirement 3

**Missing Requirements Found:** ✅ YES - 1 requirement

**User requested UI change but it's not in spec!**

---

### OVERALL RESULT: ❌ FAILED

**Failures:**
- ❌ User requested "show ADP value in draft recommendations UI" (epic line 28)
- ❌ This requirement is MISSING from spec
- ❌ Cannot proceed without addressing user's explicit request

**Required Actions:**
1. ADD new Requirement 6: Display ADP in UI
   - Source: Epic Request (line 28)
   - Describe what UI changes are needed
   - Components affected: Draft mode UI classes
2. Research draft UI code (might need mini Phase 1)
3. Update checklist with UI-related questions
4. Re-run Phase 2.5 alignment check
5. Do NOT proceed to STAGE_2c until PASSED

**Lesson:** Read ALL explicit requests in Epic Intent. Missing even one means spec is incomplete.
```

---

## Gate 2 Examples: User Checklist Approval

### Example: Presenting Checklist for Approval

```markdown
## User Checklist Approval - Gate 2

Stage 2b (Specification Phase) is complete. I've created checklist.md with 6 questions that need your input:

**Checklist Sections:**
- Functional Questions: 3 (CSV format, matching strategy, multiplier formula)
- Technical Questions: 1 (player key format)
- Error Handling Questions: 2 (missing CSV behavior, logging preferences)

**File Location:** `feature-updates/KAI-1-improve_draft_helper/feature_01_adp_integration/checklist.md`

**Question Summary:**
1. ADP CSV Format - What are the exact column names?
2. Valid ADP Range - What's the min/max ADP value?
3. Multiplier Formula - Config-based, linear, or exponential?
4. Player Matching - Exact, normalized, or fuzzy?
5. Missing CSV Behavior - Fail or default to neutral?
6. Logging Verbosity - Per-player warnings or summary?

**For each question I've provided:**
- Context (why this matters)
- 2-3 options with pros/cons
- My recommendation
- Impact on spec.md

**Please review checklist.md and answer each question. You can:**
- Answer all at once (provide answers for all 6 questions)
- Go one at a time (we'll go through interactively)
- Request clarification on any question

**What format works best for you?**
```

### Example: User Provides Answers

**User response:**
```
Let's go through them:

Q1: Column names are Name, Position, OverallRank (not ADP)
Q2: 1-300 range is fine
Q3: Config-based sounds good, let me tune it
Q4: Normalization approach works
Q5: Graceful degradation with warning
Q6: Summary logging is fine
```

**Agent updates spec.md and checklist.md:**

```markdown
## Checklist Updates

### Question 1: ADP CSV Format
- [x] **RESOLVED:** Columns are Name, Position, OverallRank

**User's Answer:**
"Column names are Name, Position, OverallRank (not ADP)"

**Implementation Impact:**
- CSV parsing will look for 'OverallRank' column (not 'ADP')
- Update adp_loader.py to use correct column name
- Update data structures section in spec.md

**spec.md update:**
```markdown
### Data Structure: ADP CSV Format

**Source:** User Answer to Checklist Q1

User confirmed FantasyPros CSV has columns:
- Name: Player full name (string)
- Position: Player position (string)
- OverallRank: ADP ranking (integer, 1-300 range)

**Implementation:**
```python
# adp_loader.py
def load_adp_data(filepath: Path) -> Dict[str, int]:
    df = read_csv_with_validation(
        filepath,
        required_columns=['Name', 'Position', 'OverallRank']
    )
    # Map OverallRank to adp_value
    # ...
```
```

{Continue for all 6 questions...}

---

**After all questions answered:**

```markdown
## User Approval Section

**User Reviewed:** 2026-01-10 14:30
**User Approval:** ✅ APPROVED
**Total Questions:** 6
**User Answered:** 6
**Pending:** 0

**User Comments:**
User provided answers for all 6 questions. Preferred config-based approach for multiplier calculation, which allows tuning without code changes.

**Gate 2 Status:** ✅ PASSED - All questions answered, spec.md updated accordingly

---

**STATUS:** ✅ APPROVED - Ready for Stage 5a (Implementation Planning)
```

---

## Success Criteria Summary

**Specification Phase (STAGE_2b) passes when:**

✅ **Phase 2 (Spec & Checklist):**
- spec.md has Epic Intent section (from STAGE_2a)
- All requirements have traceability (Epic Request/User Answer/Derived)
- Components Affected section lists exact files/lines
- Data Structures section describes formats
- Algorithms section has implementation details
- checklist.md has valid questions (user preferences, edge cases, unknowns)
- Zero assumptions in spec (all TBD items in checklist)

✅ **Phase 2.5 (Alignment Check):**
- All requirements verified against Epic Intent
- No scope creep (no features user didn't ask for)
- No missing requirements (all user requests in spec)
- All sources valid (Epic/Derived, not "assumptions")
- PASSED result documented

✅ **Phase 2.6 (Gate 2):**
- checklist.md presented to user
- User answered ALL questions
- spec.md updated with user answers
- Approval documented with timestamp
- Gate 2 PASSED

**Ready for STAGE_2c or Stage 5a when all phases complete.**

---

*End of specification_examples.md*
