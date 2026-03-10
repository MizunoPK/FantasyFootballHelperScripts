# S2.P1: Spec Creation - Detailed Examples

**Guide Version:** 1.0
**Created:** 2026-01-10
**Purpose:** Detailed examples and templates for S2.P1 spec creation and alignment execution
**Prerequisites:** Read stages/s2/s2_p1_spec_creation_refinement.md first
**Main Guide:** stages/s2/s2_p1_spec_creation_refinement.md

---

## Table of Contents

1. [Purpose](#purpose)
2. [S2.P1 Examples: Spec & Checklist with Traceability](#s2p1-examples-spec--checklist-with-traceability)
3. [S2.P1.I3 Examples: Spec-to-Epic Alignment Check (Gate 2)](#s2p1i3-examples-spec-to-epic-alignment-check-gate-2)
4. [Gate 3 Examples: User Checklist Approval](#gate-3-examples-user-checklist-approval)
5. [Success Criteria Summary](#success-criteria-summary)

---

## Purpose

This reference provides detailed examples for executing Spec Creation & Refinement (S2.P1). Use this alongside the main guide for:
- Example spec.md sections with requirement traceability
- Sample checklist.md with valid questions
- Alignment check examples
- Real-world specification patterns

**Always read the main guide first.** This is a reference supplement, not a standalone guide.

---

## S2.P1 Examples: Spec & Checklist with Traceability

### Example 1: Components Affected Section (with sources)

```markdown
## Components Affected

**Classes to Modify:**

1. **RecordManager** (`[module]/util/RecordManager.py`)
   - **Source:** Epic notes line 35: "integrate into RecordManager scoring"
   - **Traceability:** Direct user request
   - **Changes:**
     - `calculate_total_score()` method (line 125) - Add rank multiplier to calculation
       - Current: `total_score = base * injury * matchup * team`
       - New: `total_score = base * injury * matchup * team * rank`
     - `load_players()` method (line 89) - Call new rank priority loader
     - New method: `_calculate_rank_multiplier(item: DataRecord) -> float`
       - Pattern: Follow existing multiplier methods (line 450-550)
       - Returns: Float multiplier based on item.rank_value

2. **ConfigManager** (`[module]/util/ConfigManager.py`)
   - **Source:** Derived from user request (need configuration for rank multiplier ranges)
   - **Traceability:** User requested Rank integration (epic line 15), configuration is necessary to define multiplier ranges (similar to existing injury/matchup config)
   - **Changes:**
     - New method: `get_rank_multiplier(rank: int) -> float`
       - Pattern: Similar to get_attribute_multiplier() at line 180
       - Input: rank value (1-500 range, TBD - add to checklist Q2)
       - Output: Float multiplier
     - New config keys in league_config.json:
       - `rank_ranges`: Define rank value ranges (TBD format - add to checklist Q3)
       - `rank_multipliers`: Define multiplier for each range

3. **DataRecord** (`[module]/util/DataRecord.py`)
   - **Source:** Derived from user request (need to store rank data per item)
   - **Traceability:** User requested "integrate rank data" (epic line 15), storing rank value on item object is logically required
   - **Changes:**
     - Add field: `rank_value: Optional[int] = None`
       - Type: Optional int (None if item not in rank data)
       - Range: 1-500 (TBD - verify with user in checklist Q2)
     - Add field: `rank_multiplier: float = 1.0`
       - Type: Float
       - Default: 1.0 (neutral, no bonus/penalty)
       - Calculated: Set by _calculate_rank_multiplier()

**New Files to Create:**

1. `[module]/loaders/rank_loader.py` (NEW)
   - **Source:** Derived requirement (need dedicated loader for rank data)
   - **Traceability:** User specified "use [ranking source] CSV" (epic line 22), loading CSV requires dedicated loader module
   - **Purpose:** Load and parse rank data from CSV
   - **Exports:**
     - `load_rank_data(filepath: Path) -> Dict[str, int]`
       - Returns: Dictionary mapping item key to rank value
       - Item key format: TBD (add to checklist Q4 - "name" or "name_position"?)

2. `data/priority_rankings.csv` (NEW)
   - **Source:** Epic notes line 22: "use [ranking source] CSV format"
   - **Traceability:** Direct user request for data source
   - **Format:** TBD (add to checklist Q1 - ask user for exact format)
   - **Expected columns:** Name, Position, rank priority (TBD - verify with user)

3. `tests/[module]/util/test_RecordManager_rank.py` (NEW)
   - **Source:** Derived requirement (all new features require tests)
   - **Traceability:** Standard practice (100% test coverage required per project standards)
   - **Purpose:** Test rank multiplier calculation and integration
   - **Pattern:** Follow test_RecordManager_scoring.py structure (verified in S2.P1.I1)

4. `tests/[module]/loaders/test_rank_loader.py` (NEW)
   - **Source:** Derived requirement (new loader requires tests)
   - **Traceability:** Standard practice
   - **Purpose:** Test CSV loading, parsing, error handling
```

---

### Example 2: Requirements Section (with full traceability)

```markdown
## Requirements

### Requirement 1: Load Rank Data from CSV

**Description:** Load external rank priority (rank priority) data from [ranking source] CSV file and match to existing items

**Source:** Epic notes line 15: "integrate rank data from [ranking source]"
**Traceability:** Direct user request

**Implementation:**
- Load CSV during RecordManager initialization (in load_players() method)
- Use csv_utils.read_csv_with_validation() for robust loading
- Match items to rank data using item key (TBD format - checklist Q4)
- Store rank value in item.rank_value field

**Edge Cases:**
- CSV file missing: TBD behavior (checklist Q5 - fail or default to neutral?)
- Item not in CSV: Set rank_value = None, rank_multiplier = 1.0
- Invalid rank value: TBD validation (checklist Q2 - valid range?)

**Dependencies:**
- csv_utils.read_csv_with_validation() (exists, verified in S2.P1.I1)
- rank_loader.load_rank_data() (new, to be created)

---

### Requirement 2: Calculate rank priority Multiplier

**Description:** Convert rank value (1-500 range) to multiplier for scoring calculation

**Source:** Epic notes line 18-19: "factor rank priority into scoring recommendations so high-rank priority items rank higher"
**Traceability:** Direct user request

**Implementation:**
- New method: RecordManager._calculate_rank_multiplier(item: DataRecord) -> float
- Pattern: Follow existing multiplier methods (injury, matchup, team)
- Input: item.rank_value (Optional[int])
- Output: Float multiplier
  - High rank priority (1-50): Multiplier > 1.0 (bonus) - TBD exact values (checklist Q3)
  - Mid rank priority (51-200): Multiplier ~1.0 (neutral) - TBD
  - Low rank priority (201+): Multiplier = 1.0 (neutral) - TBD
  - Missing rank priority (None): Multiplier = 1.0 (neutral)

**Algorithm:** TBD (checklist Q3 - linear, exponential, or config-based?)

**Dependencies:**
- ConfigManager.get_rank_multiplier() (new, to be created)
- Item must have rank_value populated (Requirement 1)

---

### Requirement 3: Integrate rank priority Multiplier into Scoring

**Description:** Apply rank multiplier in calculate_total_score() alongside existing multipliers

**Source:** Epic notes line 37-38: "Keep it simple - just add rank priority as another multiplier like injury penalty"
**Traceability:** Direct user request (user specified implementation pattern)

**Implementation:**
- Modify RecordManager.calculate_total_score() method
- Current calculation:
  ```
  total_score = base_score * attribute_mult * context_mult * team_mult
  ```text
- New calculation:
  ```
  rank_mult = self._calculate_rank_multiplier(item)
  total_score = base_score * attribute_mult * context_mult * team_mult * rank_mult
  ```markdown
- Maintain interface: No parameter changes (user constraint epic line 35)

**Dependencies:**
- Requirement 2 complete (_calculate_rank_multiplier method exists)
- Item must have rank_multiplier calculated

---

### Requirement 4: Handle Missing Item Data

**Description:** Gracefully handle items not in rank data

**Source:** Derived requirement
**Traceability:** Not all items may have rank data (rookies, obscure items), system must handle gracefully to avoid crashes

**Implementation:**
- If item not in rank priority CSV: Set rank_value = None
- _calculate_rank_multiplier() behavior when rank_value is None:
  - Return 1.0 (neutral multiplier, no bonus/penalty)
  - Pattern: Same as injury multiplier when status unknown
- Optional: Log warning for missing items (TBD - checklist Q6)

**Edge Cases:**
- Entire rank priority CSV missing: TBD (checklist Q5 - fail or all items neutral?)
- Item name mismatch: Won't find in CSV, treated as missing (neutral 1.0)

---

### Requirement 5: Configuration for rank priority Multiplier Ranges

**Description:** Define rank value ranges and corresponding multipliers in configuration file

**Source:** Derived requirement
**Traceability:** User requested "factor rank priority into scoring" but didn't specify formula. Config-based approach allows flexibility without code changes.

**Implementation:**
- Add to data/league_config.json:
  ```
  "rank_multipliers": {
    "ranges": [
      {"min": 1, "max": 50, "multiplier": 1.2},
      {"min": 51, "max": 100, "multiplier": 1.1},
      {"min": 101, "max": 200, "multiplier": 1.0},
      {"min": 201, "max": 500, "multiplier": 1.0}
    ]
  }
  ```bash
  (Note: Exact ranges/values TBD - checklist Q3)

- ConfigManager.get_rank_multiplier(rank: int) implementation:
  - Find range containing rank value
  - Return corresponding multiplier
  - Default to 1.0 if rank priority out of range

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
## Feature 01: rank priority Integration - Planning Checklist

**Purpose:** Track open questions and decisions for this feature

**Instructions:**
- [ ] = Open question (needs user answer)
- [x] = Resolved (answer documented below)

---

## Open Questions

### Question 1: rank priority CSV Format and Columns

- [ ] What are the exact column names in the [ranking source] rank priority CSV?

**Context:** Need to know exact column names to parse CSV correctly. User mentioned "[ranking source] CSV" but didn't specify structure.

**Epic reference:** Line 22: "use [ranking source] CSV format" (format not detailed)

**Options:**
A. Ask user to provide sample CSV or column names
B. Assume standard format: Name, Position, rank priority
C. Support multiple formats with auto-detection

**Recommendation:** Option A - Ask user for actual file or column names to ensure correct parsing

**Why this is a question:** Cannot assume CSV structure without seeing actual file or user confirmation

**Impact on spec.md:** Will update data structures section with exact column names and parsing logic

---

### Question 2: Valid rank priority Value Range

- [ ] What is the valid range for rank values?

**Context:** Need to know min/max rank values for validation and multiplier calculation.

**Epic reference:** Not mentioned in epic

**Options:**
A. 1-300 (typical for standard leagues)
B. 1-500 (deeper leagues)
C. No upper limit (any positive integer)

**Recommendation:** Option A (1-300) unless user has deeper league

**Why this is a question:** User didn't specify league depth or rank priority range

**Impact on spec.md:** Will update validation logic and ConfigManager ranges

---

### Question 3: rank priority Multiplier Calculation Formula

- [ ] How should rank value translate to scoring multiplier?

**Context:** User said "factor rank priority into scoring" but didn't specify how much impact it should have.

**Epic reference:** Line 18-19: "factor rank priority into scoring recommendations so high-rank priority items rank higher" (no formula specified)

**Options:**
A. **Config-based ranges** (recommended)
   - Define ranges in league_config.json
   - Example: rank priority 1-50 = 1.2x, 51-100 = 1.1x, 101+ = 1.0x
   - Pros: Flexible, easy to tune without code changes
   - Cons: Requires config file updates

B. **Linear formula**
   - Formula: multiplier = 1.0 + ((300 - rank) / 300) * 0.2
   - Example: rank priority 1 = 1.2x, rank priority 150 = 1.1x, rank priority 300 = 1.0x
   - Pros: Simple, continuous
   - Cons: Less control over ranges

C. **Exponential formula**
   - Formula: multiplier = 1.0 + (300 / rank) * 0.05
   - Example: rank priority 1 = 1.15x, rank priority 50 = 1.03x, rank priority 300 = 1.0x
   - Pros: Higher impact for top picks
   - Cons: Complex, harder to tune

**Recommendation:** Option A (config-based) - Most flexible, follows existing pattern (injury/matchup use config)

**Why this is a question:** User specified integration but not formula or impact level

**Impact on spec.md:** Will update algorithm section and ConfigManager implementation details

---

### Question 4: Item Matching Strategy

- [ ] How should we match items between rank priority CSV and item list?

**Context:** Item names might vary between data sources (e.g., "A.J. Brown" vs "AJ Brown").

**Epic reference:** Not mentioned in epic

**Options:**
A. **Exact match on Name+Position**
   - Match: name == name AND position == position
   - Pros: Simple, no false positives
   - Cons: Misses items with name variations

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

**Impact on spec.md:** Will add item matching utility and update load_rank_data implementation

---

### Question 5: Behavior When rank priority CSV Missing

- [ ] What should happen if the rank priority CSV file is missing or unreadable?

**Context:** Need to handle case where user hasn't provided rank data yet or file path is wrong.

**Epic reference:** Not mentioned in epic

**Options:**
A. **Fail with clear error message**
   - Raise exception, stop execution
   - Pros: Forces user to provide data
   - Cons: Breaks recommendation engine if file missing

B. **Default all items to neutral (1.0 multiplier)**
   - Log warning, continue with all rank_multiplier = 1.0
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

### Question 6: Logging for Missing Item Matches

- [ ] Should we log warnings when items aren't found in rank data?

**Context:** Some items (rookies, obscure) might not have rank data. Decide on logging verbosity.

**Epic reference:** Not mentioned in epic

**Options:**
A. **Log warning for each missing item**
   - Pros: User aware of missing data
   - Cons: Verbose output if many missing

B. **Log summary only** (e.g., "15 items not in rank data")
   - Pros: Cleaner output
   - Cons: User doesn't know which items

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

**❌ BAD QUESTION: "Which file contains RecordManager?"**
→ This should have been found in S2.P1.I1 research

**❌ BAD QUESTION: "Does RecordManager have a scoring method?"**
→ This should have been verified in S2.P1.I1 Gate 1 audit

**❌ BAD QUESTION: "What's the pattern for adding new multipliers?"**
→ This should have been documented by reading injury penalty code

**❌ BAD QUESTION: "How do we load CSV files?"**
→ This should have been researched (csv_utils exists, verified in S2.P1.I1)

**Good questions ask about:**
✅ User preferences (Option A vs B vs C)
✅ Business logic not in epic (multiplier formula)
✅ Edge case handling (missing data behavior)
✅ External data formats (CSV column names from [ranking source])
```

---

## S2.P1.I3 Examples: Spec-to-Epic Alignment Check (Gate 2)

### Example 1: Alignment Check - PASSING

```markdown
## S2.P1.I3 Alignment Summary (Gate 2)

### Requirement Source Verification

**Requirement 1: Load Rank Data**
- Source: Epic Request (line 15)
- Citation: ✅ "integrate rank data from [ranking source]"
- Valid: ✅ YES

**Requirement 2: Calculate rank priority Multiplier**
- Source: Epic Request (line 18-19)
- Citation: ✅ "factor rank priority into scoring recommendations"
- Valid: ✅ YES

**Requirement 3: Integrate into Scoring**
- Source: Epic Request (line 37-38)
- Citation: ✅ "add rank priority as another multiplier like injury penalty"
- Valid: ✅ YES

**Requirement 4: Handle Missing Data**
- Source: Derived
- Derivation: ✅ "Not all items may have rank data, must handle gracefully"
- Valid: ✅ YES

**Requirement 5: Configuration**
- Source: Derived
- Derivation: ✅ "User requested integration but not formula, config allows flexibility"
- Valid: ✅ YES

**All requirements have valid sources:** ✅ YES

---

### Scope Creep Check

**Reviewed each requirement against Discovery Context:**

**Requirement 1 (Load Rank Data):**
- User asked for this: ✅ YES (epic line 15: "integrate rank data")
- Match: ✅ PERFECT

**Requirement 2 (Calculate Multiplier):**
- User asked for this: ✅ YES (epic line 18-19: "factor rank priority into scoring")
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

**Re-read Discovery Context section - User's explicit requests:**

1. "integrate rank data from [ranking source]" (line 15)
   → Found in spec: ✅ Requirement 1

2. "factor rank priority into scoring recommendations so high-rank priority items rank higher" (line 18-19)
   → Found in spec: ✅ Requirement 2 + 3

3. "use [ranking source] CSV format" (line 22)
   → Found in spec: ✅ Requirement 1 (data structures section)

4. "Don't change RecordManager interface too much" (line 35 - constraint)
   → Found in spec: ✅ Requirement 3 (maintains interface, no parameter changes)

5. "Keep it simple - add rank priority as multiplier like injury penalty" (line 37-38)
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

**Ready for Gate 3:** ✅ YES

**Next Action:** Present checklist to user (Gate 3 - User Checklist Approval)
```

---

### Example 2: Alignment Check - FAILED (Scope Creep Detected)

```markdown
## S2.P1.I3 Alignment Summary (Gate 2) - FAILED EXAMPLE

### Requirement Source Verification

{Requirements 1-5 same as passing example...}

**Requirement 6: Historical rank priority Tracking** ❌
- Source: ⚠️ "Best practice for trend analysis"
- Citation: ❌ NOT in epic notes
- Valid: ❌ NO - This is scope creep

**Requirement 7: Automatic rank priority Updates** ❌
- Source: ⚠️ "Nice to have for automation"
- Citation: ❌ NOT in epic notes
- Valid: ❌ NO - User explicitly excluded (epic line 45: "manual CSV for now")

**Issues found:** ❌ 2 requirements have invalid sources

---

### Scope Creep Check

**Requirement 6 (Historical rank priority Tracking):**
- User asked for this: ❌ NO
- User explicitly excluded: ✅ YES (epic line 42: "Don't worry about historical rank priority trends")
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
4. Re-run S2.P1.I3 alignment check (Gate 2)
5. Do NOT proceed to Gate 3 until PASSED

**Lesson:** Read "Out of Scope" section in Discovery Context. User explicitly said what NOT to include.
```

---

### Example 3: Alignment Check - FAILED (Missing Requirement)

```markdown
## S2.P1.I3 Alignment Summary (Gate 2) - FAILED EXAMPLE

### Missing Requirements Check

**Re-read Discovery Context section - User's explicit requests:**

1. "integrate rank data from [ranking source]" (line 15)
   → Found in spec: ✅ Requirement 1

2. "factor rank priority into scoring recommendations so high-rank priority items rank higher" (line 18-19)
   → Found in spec: ✅ Requirement 2 + 3

3. "use [ranking source] CSV format" (line 22)
   → Found in spec: ✅ Requirement 1

4. "show rank value in scoring recommendations UI" (line 28)
   → Found in spec: ❌ MISSING - Not in any requirement!

5. "Don't change RecordManager interface too much" (line 35)
   → Found in spec: ✅ Requirement 3

**Missing Requirements Found:** ✅ YES - 1 requirement

**User requested UI change but it's not in spec!**

---

### OVERALL RESULT: ❌ FAILED

**Failures:**
- ❌ User requested "show rank value in scoring recommendations UI" (epic line 28)
- ❌ This requirement is MISSING from spec
- ❌ Cannot proceed without addressing user's explicit request

**Required Actions:**
1. ADD new Requirement 6: Display rank priority in UI
   - Source: Epic Request (line 28)
   - Describe what UI changes are needed
   - Components affected: Draft mode UI classes
2. Research draft UI code (might need mini S2.P1.I1 research)
3. Update checklist with UI-related questions
4. Re-run S2.P1.I3 alignment check (Gate 2)
5. Do NOT proceed to Gate 3 until PASSED

**Lesson:** Read ALL explicit requests in Discovery Context. Missing even one means spec is incomplete.
```

---

## Gate 3 Examples: User Checklist Approval

### Example: Presenting Checklist for Approval

```markdown
## User Checklist Approval - Gate 3

S2.P1.I3 (Refinement & Alignment) is complete. I've created checklist.md with 6 questions that need your input:

**Checklist Sections:**
- Functional Questions: 3 (CSV format, matching strategy, multiplier formula)
- Technical Questions: 1 (item key format)
- Error Handling Questions: 2 (missing CSV behavior, logging preferences)

**File Location:** `.shamt/epics/SHAMT-1-improve_recommendation_engine/feature_01_rank_integration/checklist.md`

**Question Summary:**
1. rank priority CSV Format - What are the exact column names?
2. Valid rank priority Range - What's the min/max rank value?
3. Multiplier Formula - Config-based, linear, or exponential?
4. Item Matching - Exact, normalized, or fuzzy?
5. Missing CSV Behavior - Fail or default to neutral?
6. Logging Verbosity - Per-item warnings or summary?

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
```bash
Let's go through them:

Q1: Column names are Name, Position, OverallRank (not rank priority)
Q2: 1-300 range is fine
Q3: Config-based sounds good, let me tune it
Q4: Normalization approach works
Q5: Graceful degradation with warning
Q6: Summary logging is fine
```

**Agent updates spec.md and checklist.md:**

```markdown
## Checklist Updates

### Question 1: rank priority CSV Format
- [x] **RESOLVED:** Columns are Name, Position, OverallRank

**User's Answer:**
"Column names are Name, Position, OverallRank (not rank priority)"

**Implementation Impact:**
- CSV parsing will look for 'OverallRank' column (not 'rank priority')
- Update rank_loader.py to use correct column name
- Update data structures section in spec.md

**spec.md update:**
```
### Data Structure: rank priority CSV Format

**Source:** User Answer to Checklist Q1

User confirmed [ranking source] CSV has columns:
- Name: Item full name (string)
- Category: Item category (string)
- OverallRank: rank value (integer, 1-300 range)

**Implementation:**
```python
## rank_loader.py
def load_rank_data(filepath: Path) -> Dict[str, int]:
    df = read_csv_with_validation(
        filepath,
        required_columns=['Name', 'Position', 'OverallRank']
    )
    # Map OverallRank to rank_value
    # ...
```
```json

{Continue for all 6 questions...}

---

**After all questions answered:**

```
## User Approval Section

**User Reviewed:** 2026-01-10 14:30
**User Approval:** ✅ APPROVED
**Total Questions:** 6
**User Answered:** 6
**Pending:** 0

**User Comments:**
User provided answers for all 6 questions. Preferred config-based approach for multiplier calculation, which allows tuning without code changes.

**Gate 3 Status:** ✅ PASSED - All questions answered, spec.md updated accordingly

---

**STATUS:** ✅ APPROVED - Ready for S5 (Implementation Planning)

---

## Success Criteria Summary

**S2.P1 passes when:**

✅ **S2.P1.I1-I2 (Spec & Checklist):**
- spec.md has Discovery Context section (from S2.P1.I1)
- All requirements have traceability (Epic Request/User Answer/Derived)
- Components Affected section lists exact files/lines
- Data Structures section describes formats
- Algorithms section has implementation details
- checklist.md has valid questions (user preferences, edge cases, unknowns)
- Zero assumptions in spec (all TBD items in checklist)

✅ **S2.P1.I3 (Alignment Check — Gate 2):**
- All requirements verified against Discovery Context
- No scope creep (no features user didn't ask for)
- No missing requirements (all user requests in spec)
- All sources valid (Epic/Derived, not "assumptions")
- PASSED result documented

✅ **S2.P1.I3 (Gate 3):**
- checklist.md presented to user
- User answered ALL questions
- spec.md updated with user answers
- Approval documented with timestamp
- Gate 3 PASSED

**Ready for S2.P2 (Cross-Feature Alignment) or S5 when S2.P1 complete.**

---

*End of specification_examples.md*
