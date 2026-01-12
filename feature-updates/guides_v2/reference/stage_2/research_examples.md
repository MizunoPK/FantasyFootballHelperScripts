# STAGE 2a: Research Phase - Detailed Examples

**Guide Version:** 1.0
**Created:** 2026-01-10
**Purpose:** Detailed examples and templates for Research Phase execution
**Prerequisites:** Read stages/s2/s2_p1_research.md first
**Main Guide:** stages/s2/s2_p1_research.md

---

## Purpose

This reference provides detailed examples for executing Research Phase (Phase 2.1). Use this alongside the main guide for:
- Example epic intent extraction
- Sample research findings documents
- Detailed audit verification examples
- Real-world research patterns

**Always read the main guide first.** This is a reference supplement, not a standalone guide.

---

## Phase 0 Examples: Epic Intent Extraction

### Example 1: Complete Epic Intent Analysis

```markdown
## Epic Intent Analysis (Internal - for agent)

**1. What problem is THIS feature solving?**

Quote from epic notes: "Draft helper doesn't account for ADP (Average Draft Position) when ranking players. This means we might recommend players who get drafted way earlier than projected, making recommendations useless in real drafts."
(Source: Epic notes line 12-14)

My interpretation: Users want draft recommendations that reflect real-world draft patterns, not just our scoring projections in isolation.

---

**2. What did the user EXPLICITLY request for this feature?**

Explicit request 1: "integrate ADP data from FantasyPros"
(Source: Epic notes line 15)

Explicit request 2: "factor ADP into draft recommendations so high-ADP players rank higher"
(Source: Epic notes line 18-19)

Explicit request 3: "use FantasyPros CSV format"
(Source: Epic notes line 22)

---

**3. What constraints did the user mention?**

Constraint 1: "Don't change PlayerManager interface too much - other code depends on it"
(Source: Epic notes line 35)

Constraint 2: "Keep it simple - just add ADP as another multiplier like injury penalty"
(Source: Epic notes line 37-38)

---

**4. What is OUT of scope? (user said "not now" or "future")**

Out of scope 1: "Don't worry about historical ADP trends, just use current season ADP"
(Source: Epic notes line 42)

Out of scope 2: "Automatic ADP updates can come later, manual CSV for now"
(Source: Epic notes line 45)

---

**5. What is the user trying to ACCOMPLISH? (end goal)**

User's goal: "Make better draft decisions by incorporating real-world draft patterns into our recommendations"
(Source: Epic notes line 8-10)

---

**6. What technical components did the user mention?**

Component 1: "PlayerManager" - Line 35
Component 2: "injury penalty system" (as a pattern to follow) - Line 37
Data source: "FantasyPros CSV" - Line 22
```

### Example 2: Epic Intent Section in spec.md

```markdown
# Feature 01: ADP Integration

---

## Epic Intent (User's Original Request)

**⚠️ CRITICAL:** All requirements below MUST trace back to this section.

**Problem This Feature Solves:**

"Draft helper doesn't account for ADP (Average Draft Position) when ranking players. This means we might recommend players who get drafted way earlier than projected, making recommendations useless in real drafts."
(Source: Epic notes line 12-14)

---

**User's Explicit Requests:**

1. "integrate ADP data from FantasyPros"
   (Source: Epic notes line 15)

2. "factor ADP into draft recommendations so high-ADP players rank higher"
   (Source: Epic notes line 18-19)

3. "use FantasyPros CSV format"
   (Source: Epic notes line 22)

---

**User's Constraints:**

- "Don't change PlayerManager interface too much - other code depends on it"
  (Source: Epic notes line 35)

- "Keep it simple - just add ADP as another multiplier like injury penalty"
  (Source: Epic notes line 37-38)

---

**Out of Scope (User Explicitly Excluded):**

- "Don't worry about historical ADP trends, just use current season ADP"
  (Source: Epic notes line 42)

- "Automatic ADP updates can come later, manual CSV for now"
  (Source: Epic notes line 45)

---

**User's End Goal:**

"Make better draft decisions by incorporating real-world draft patterns into our recommendations"
(Source: Epic notes line 8-10)

---

**Technical Components Mentioned by User:**

- **PlayerManager** (Epic notes line 35)
- **injury penalty system** (as pattern to follow) (Epic notes line 37)
- **FantasyPros CSV** (Epic notes line 22)

---

**Agent Verification:**

□ Re-read epic notes file: 2026-01-02 10:15
□ Extracted exact quotes (not paraphrases)
□ Cited line numbers for all quotes
□ Identified out-of-scope items
□ Understand user's goal (not just technical implementation)

---

{Rest of spec.md sections will be added in Phase 2.2}
```

---

## Phase 1 Examples: Targeted Research

### Example 1: Research Checklist (Grounded in Epic)

```markdown
## Research Checklist for Feature 01 (ADP Integration)

Based on Epic Intent section, I must research:

□ **PlayerManager** (mentioned epic line 35)
  - Action: Find class definition
  - Action: Read calculate_total_score() method (user mentioned scoring)
  - Action: Document actual signatures (not assumed)
  - Evidence required: File path, line numbers, code snippets

□ **injury penalty system** (mentioned epic line 37 as pattern)
  - Action: Find implementation
  - Action: READ the actual code (not guess at pattern)
  - Action: Document pattern used (method structure, multiplier approach)
  - Evidence required: File path, code structure, actual code snippets

□ **FantasyPros CSV format** (mentioned epic line 22)
  - Action: Search for existing CSV files in data/
  - Action: Check if ADP already used anywhere in codebase
  - Action: Document expected CSV structure (if examples exist)
  - Evidence required: File paths, column names, sample data

□ **Multiplier pattern in scoring** (user said "like injury penalty")
  - Action: Find how multipliers are applied in calculate_total_score()
  - Action: Document the pattern (how to add new multiplier)
  - Action: Check if ConfigManager involved
  - Evidence required: Code showing multiplier application
```

### Example 2: Complete Research Findings Document

```markdown
# Feature 01: ADP Integration - Discovery Findings

**Research Date:** 2026-01-02
**Researcher:** Agent
**Grounded In:** Epic Intent (user's explicit requests)

---

## Epic Intent Summary

**User requested:** "integrate ADP data from FantasyPros and factor it into draft recommendations using a multiplier pattern similar to injury penalty"

**Components user mentioned:**
- PlayerManager (scoring integration)
- injury penalty system (pattern to follow)
- FantasyPros CSV (data source)

**This research focused on user-mentioned components ONLY.**

---

## Components Identified

### Component 1: PlayerManager (from Epic line 35)

**User mentioned:** "Don't change PlayerManager interface too much"

**Found in codebase:**
- File: `league_helper/util/PlayerManager.py`
- Class definition: Line 45
- Relevant method: `calculate_total_score()` at line 125

**Method signature (actual from source):**
```python
def calculate_total_score(self, player: FantasyPlayer, config: ConfigManager) -> float:
    """Calculate total score including all multipliers.

    Args:
        player (FantasyPlayer): Player to score
        config (ConfigManager): Configuration for multiplier ranges

    Returns:
        float: Final score with all multipliers applied
    """
    base_score = player.projected_points

    # Apply multipliers
    injury_mult = self._calculate_injury_multiplier(player)
    matchup_mult = self._calculate_matchup_multiplier(player)
    team_mult = self._calculate_team_quality_multiplier(player)

    total_score = base_score * injury_mult * matchup_mult * team_mult
    return total_score
```

**How it works today:**
- Loads base score from player.projected_points
- Applies multipliers: injury, matchup, team_quality
- Each multiplier is a separate method (pattern: `_calculate_{type}_multiplier()`)
- Returns final score as product of base * all multipliers

**Relevance to this feature:**
- User wants to add ADP as another multiplier
- Should follow existing pattern: create `_calculate_adp_multiplier()` method
- Multiply into total_score alongside existing multipliers

---

### Component 2: injury penalty system (from Epic line 37 - pattern to follow)

**User mentioned:** "Keep it simple - just add ADP as another multiplier like injury penalty"

**Found implementation:**
- File: `league_helper/util/PlayerManager.py`
- Lines: 450-480
- Pattern used: Multiplier-based penalty

**Code structure (actual):**
```python
def _calculate_injury_multiplier(self, player: FantasyPlayer) -> float:
    """Calculate injury status multiplier.

    Args:
        player (FantasyPlayer): Player to evaluate

    Returns:
        float: Multiplier between 0.0-1.0 (penalty for injury)
    """
    if player.injury_status == "Healthy":
        return 1.0
    elif player.injury_status == "Questionable":
        return 0.95
    elif player.injury_status == "Doubtful":
        return 0.85
    elif player.injury_status == "Out":
        return 0.0
    else:
        # Unknown status - neutral
        return 1.0
```

**Pattern to reuse:**
- Method returns float multiplier
- Range: 0.0-1.0 (penalty) or 1.0+ (bonus)
- Applied in calculate_total_score() by multiplication
- Uses player fields to determine multiplier value
- Defaults to 1.0 (neutral) for unknown/missing data

**For ADP feature:**
- Create `_calculate_adp_multiplier(player: FantasyPlayer) -> float`
- High ADP (1-50) → multiplier > 1.0 (bonus)
- Low ADP (200+) → multiplier = 1.0 (neutral)
- Missing ADP → multiplier = 1.0 (neutral, like injury unknown status)
- Add to total_score calculation: `total_score = base * injury * matchup * team * adp`

---

### Data Source: FantasyPros CSV (from Epic line 22)

**User mentioned:** "use FantasyPros CSV format"

**Found in codebase:**
- Searched for: `grep -r "adp" --include="*.py" -i`
- Result: NO existing ADP references found
- This is NEW data source (not currently in codebase)

**Searched for example CSV files:**
- `find data/ -name "*.csv"`
- Found: `data/players.csv`, `data/injury_report.csv`

**Example CSV structure (from players.csv):**
```csv
Name,Position,Team,ProjectedPoints
Patrick Mahomes,QB,KC,450.5
Christian McCaffrey,RB,CAR,380.2
```

**For ADP feature:**
- Need to determine exact FantasyPros CSV format (add to checklist as question)
- Likely columns: Name, Position, ADP (TBD - ask user)
- Will need to match players by Name+Position (matching logic TBD - add to checklist)

---

## Existing Test Patterns

**Found test pattern in:** `tests/league_helper/util/test_PlayerManager_scoring.py`

**Pattern observed:**
- Uses pytest fixtures for sample players
- Mocks ConfigManager
- Tests each multiplier in isolation:
  ```python
  def test_injury_multiplier_healthy():
      player = FantasyPlayer(name="Test", injury_status="Healthy")
      manager = PlayerManager()
      mult = manager._calculate_injury_multiplier(player)
      assert mult == 1.0

  def test_injury_multiplier_questionable():
      player = FantasyPlayer(name="Test", injury_status="Questionable")
      manager = PlayerManager()
      mult = manager._calculate_injury_multiplier(player)
      assert mult == 0.95
  ```
- Integration test with all multipliers combined
- Edge case tests (missing data, invalid values)

**Can follow this pattern for ADP feature tests:**
- `test_adp_multiplier_high()` - ADP 1-50 returns bonus
- `test_adp_multiplier_low()` - ADP 200+ returns neutral
- `test_adp_multiplier_missing()` - No ADP data returns 1.0
- Integration test with all multipliers including ADP

---

## Interface Dependencies

**Classes This Feature Will Call:**

1. **ConfigManager.get_adp_multiplier()** (may need to create)
   - Searched: `grep -r "get_.*_multiplier" league_helper/util/ConfigManager.py`
   - Found similar method: `get_injury_multiplier(status: str) -> float` at line 180
   - Pattern: Takes input value, returns multiplier
   - For ADP: Will need `get_adp_multiplier(adp: int) -> float`
   - May need to add this method (not currently exists)

2. **CSV utilities** (for reading FantasyPros CSV)
   - Source: `utils/csv_utils.py`
   - Method: `read_csv_with_validation(filepath, required_columns)`
   - Verified: Method exists (checked source code line 45)
   - Can use for loading ADP data

3. **FantasyPlayer class** (need to add ADP field)
   - Source: `league_helper/util/FantasyPlayer.py`
   - Current fields (line 15): name, position, team, projected_points, injury_status
   - Will add: `adp_value: Optional[int]` (new field)

---

## Edge Cases Identified

**From reading existing code:**

1. Player not in ADP data → How to handle?
   - Pattern from injury: Return neutral multiplier (1.0)
   - Add to checklist: "Should players without ADP get neutral 1.0 or penalty?"

2. Invalid ADP values (< 1 or > 500) → Validation needed?
   - Add to checklist: "What's valid ADP range? How to handle invalid values?"

3. ADP data file missing → Graceful degradation?
   - Pattern from injury: If injury_report.csv missing, all players get 1.0
   - Add to checklist: "If ADP CSV missing, should we fail or default to neutral?"

4. Multiple players with same name → Matching logic?
   - Add to checklist: "How to match players? Exact name+position? Fuzzy matching?"

---

## Research Completeness

**Components researched:**
- ✅ PlayerManager class (READ source code lines 45-500)
- ✅ Existing multiplier pattern (READ injury penalty code lines 450-480)
- ✅ Test patterns (READ existing tests in test_PlayerManager_scoring.py)
- ✅ Data source search (grep for existing ADP references - none found)
- ✅ CSV utilities (verified read_csv_with_validation exists)
- ✅ FantasyPlayer class structure (READ source code lines 1-100)

**Evidence collected:**
- File paths: 5 files (PlayerManager.py, FantasyPlayer.py, ConfigManager.py, csv_utils.py, test_PlayerManager_scoring.py)
- Line numbers: Cited for all code references
- Actual code snippets: Copied method signatures, example implementations

**Ready for Phase 1.5 audit.**

---

**Next Steps:**
- Phase 1.5: Verify research completeness
- Phase 2.2 Phase 2: Update spec.md with findings
```

---

## Phase 1.5 Examples: Research Completeness Audit

### Example 1: Complete Audit with PASSING Results

```markdown
## Research Completeness Audit

### Category 1: Component Knowledge

**Question 1.1:** Can I list the EXACT classes/files that will be modified?

❌ BAD: "Probably PlayerManager and maybe ConfigManager"
✅ GOOD: "PlayerManager (league_helper/util/PlayerManager.py:125-180) and ConfigManager (league_helper/util/ConfigManager.py:234)"

**My answer:**
- PlayerManager (league_helper/util/PlayerManager.py)
  - calculate_total_score() method at line 125
  - Will add _calculate_adp_multiplier() method around line 485
- FantasyPlayer (league_helper/util/FantasyPlayer.py)
  - Class definition at line 15
  - Will add adp_value field
- ConfigManager (league_helper/util/ConfigManager.py)
  - May need to add get_adp_multiplier() method (similar to get_injury_multiplier at line 180)

**Evidence:**
- Read PlayerManager.py lines 1-500 (Read tool call at 10:25)
- Read FantasyPlayer.py lines 1-100 (Read tool call at 10:27)
- Read ConfigManager.py lines 1-300 (Read tool call at 10:30)

---

**Question 1.2:** Have I READ the source code for each component?

❌ BAD: "I searched for it but didn't read the actual code"
✅ GOOD: "Yes, used Read tool to view PlayerManager.py lines 1-300, focused on calculate_total_score() method"

**My answer:** Yes, read source code for all components:
- PlayerManager.py: Read lines 1-500, focused on calculate_total_score() (125-150) and injury multiplier pattern (450-480)
- FantasyPlayer.py: Read lines 1-100, documented current field structure
- ConfigManager.py: Read lines 1-300, found get_injury_multiplier() pattern
- csv_utils.py: Read lines 1-100, verified read_csv_with_validation() exists
- test_PlayerManager_scoring.py: Read entire file, documented test patterns

**Evidence:** Read tool calls made at 10:25, 10:27, 10:30, 10:32, 10:35

---

**Question 1.3:** Can I cite actual method signatures from source?

❌ BAD: "The method probably takes a player and returns a score"
✅ GOOD: "def calculate_total_score(self, player: FantasyPlayer, config: ConfigManager) -> float (PlayerManager.py:125)"

**My answer:** Yes, documented actual signatures:

```python
# PlayerManager.calculate_total_score
def calculate_total_score(self, player: FantasyPlayer, config: ConfigManager) -> float:
    # Source: PlayerManager.py:125

# PlayerManager._calculate_injury_multiplier
def _calculate_injury_multiplier(self, player: FantasyPlayer) -> float:
    # Source: PlayerManager.py:450

# ConfigManager.get_injury_multiplier
def get_injury_multiplier(self, status: str) -> float:
    # Source: ConfigManager.py:180

# csv_utils.read_csv_with_validation
def read_csv_with_validation(filepath: Union[str, Path], required_columns: List[str]) -> pd.DataFrame:
    # Source: csv_utils.py:45
```

**Evidence:** Copied from actual source files, cited line numbers

---

**Verification Result for Category 1:**

☑ All questions answered with ✅ GOOD level of detail
☑ Evidence provided for each answer

**Category 1: PASSED**

---

### Category 2: Pattern Knowledge

**Question 2.1:** Have I searched for similar existing features?

❌ BAD: "I assume there are similar features but didn't search"
✅ GOOD: "Searched for 'injury penalty', found implementation in PlayerManager.py:450-480"

**My answer:** Yes, searched for multiplier pattern:
- grep -r "multiplier" --include="*.py" league_helper/
- Found: injury_multiplier, matchup_multiplier, team_quality_multiplier
- All follow same pattern in PlayerManager
- Read injury_multiplier as example (most similar to ADP use case)

**Evidence:**
- grep results showed 3 existing multipliers
- Read PlayerManager.py lines 450-550 to see all multiplier implementations

---

**Question 2.2:** Have I READ at least one similar feature's implementation?

❌ BAD: "Found it but didn't read the code"
✅ GOOD: "Read PlayerManager.py lines 450-480, documented pattern in research file"

**My answer:** Yes, read injury penalty implementation in detail:
- Method structure: `_calculate_{type}_multiplier(player: FantasyPlayer) -> float`
- Return value: Float between 0.0-1.0 for penalties, 1.0+ for bonuses
- Default: Returns 1.0 for unknown/missing data
- Integration: Multiplied into total_score in calculate_total_score()

**Evidence:** Documented full code in research file with line citations

---

**Question 2.3:** Can I describe the existing pattern in detail?

❌ BAD: "It probably uses some kind of multiplier"
✅ GOOD: "Returns float multiplier (0.0-1.0 range), applied in calculate_total_score(), follows method naming pattern _calculate_{type}_multiplier()"

**My answer:** Pattern details:
- **Naming:** `_calculate_{type}_multiplier(self, player: FantasyPlayer) -> float`
- **Range:** 0.0-1.0 for penalties (injury, bad matchup), 1.0+ for bonuses (good matchup)
- **Default:** Returns 1.0 for neutral/missing data
- **Integration:** All multipliers multiplied together in calculate_total_score():
  ```python
  total_score = base_score * mult1 * mult2 * mult3 * ... * multN
  ```
- **Config:** Some multipliers use ConfigManager for ranges (matchup uses config.get_matchup_multiplier())

**Evidence:**
- injury_multiplier code (lines 450-480)
- matchup_multiplier code (lines 490-520)
- calculate_total_score integration (lines 125-150)

---

**Verification Result for Category 2:**

☑ All questions answered with ✅ GOOD level of detail
☑ Evidence provided for each answer

**Category 2: PASSED**

---

### Category 3: Data Structure Knowledge

**Question 3.1:** Have I READ the actual data files (CSV/JSON examples)?

❌ BAD: "I assume CSV has Name, Position columns"
✅ GOOD: "Read data/players.csv, actual columns: Name,Position,Team,Points,ADP (line 1)"

**My answer:** Yes, read existing CSV files to understand format:
- Read data/players.csv (example player data)
- Read data/injury_report.csv (example status data)
- No existing ADP CSV found (this is new data source)
- Documented format patterns from existing files

**Evidence:**
- data/players.csv header: `Name,Position,Team,ProjectedPoints`
- data/injury_report.csv header: `Name,Position,Status,Updated`
- Sample row from players.csv: `Patrick Mahomes,QB,KC,450.5`

---

**Question 3.2:** Can I describe the current format from actual examples?

❌ BAD: "CSV format with player data"
✅ GOOD: "CSV with header row, 5 columns (Name,Position,Team,Points,ADP), example: 'Patrick Mahomes,QB,KC,450.5,5'"

**My answer:**
Existing CSV pattern (from players.csv):
- Format: CSV with header row
- Columns: Name,Position,Team,ProjectedPoints
- Name: Full player name (e.g., "Patrick Mahomes")
- Position: Standard position abbreviation (QB, RB, WR, TE, K, DST)
- Team: Team abbreviation (e.g., "KC")
- ProjectedPoints: Float value

For ADP CSV (need to confirm with user):
- Will likely follow same pattern
- Expected columns: Name, Position, ADP (TBD - add to checklist)
- ADP: Integer ranking 1-500 (TBD - ask user for range)

**Evidence:**
- Actual header from data/players.csv: `Name,Position,Team,ProjectedPoints`
- Sample rows documented in research file

---

**Question 3.3:** Have I verified field names from source code?

❌ BAD: "I assume player has 'name' field"
✅ GOOD: "FantasyPlayer class (league_helper/util/FantasyPlayer.py:15) has fields: name: str, position: str, team: str, projected_points: float"

**My answer:** Yes, verified FantasyPlayer class fields:

```python
@dataclass
class FantasyPlayer:
    name: str
    position: str
    team: str
    projected_points: float
    injury_status: Optional[str] = None
    matchup_rating: Optional[float] = None
    team_quality: Optional[float] = None
    # Will add: adp_value: Optional[int] = None
```

Source: league_helper/util/FantasyPlayer.py lines 15-25

**Evidence:**
- Read FantasyPlayer.py lines 1-100
- Copied actual field definitions with type hints

---

**Verification Result for Category 3:**

☑ All questions answered with ✅ GOOD level of detail
☑ Evidence provided for each answer

**Category 3: PASSED**

---

### Category 4: Epic Request Knowledge

**Question 4.1:** Have I re-read the epic notes file in THIS phase?

❌ BAD: "I read it in Phase 0, don't need to read again"
✅ GOOD: "Re-read in Phase 0 at 2026-01-02 10:15, extracted user requests"

**My answer:** Yes, re-read epic notes in Phase 0:
- File: feature-updates/KAI-1-improve_draft_helper/improve_draft_helper_notes.txt
- Read timestamp: 2026-01-02 10:15
- Extracted user quotes with line numbers
- Created Epic Intent section in spec.md

**Evidence:** Phase 0 completion timestamp in Agent Status: 2026-01-02 10:20

---

**Question 4.2:** Can I list what the user EXPLICITLY requested?

❌ BAD: "User wants better draft recommendations"
✅ GOOD: "User requested: 1) 'integrate ADP data' (line 15), 2) 'factor ADP into scoring' (line 18), 3) 'use FantasyPros CSV' (line 22)"

**My answer:** User explicit requests:
1. "integrate ADP data from FantasyPros" (epic line 15)
2. "factor ADP into draft recommendations so high-ADP players rank higher" (epic line 18-19)
3. "use FantasyPros CSV format" (epic line 22)
4. "Keep it simple - just add ADP as another multiplier like injury penalty" (epic line 37-38)

**Evidence:** Exact quotes with line citations in Epic Intent section of spec.md

---

**Question 4.3:** Can I identify what's NOT mentioned (assumptions)?

❌ BAD: "Everything seems covered"
✅ GOOD: "User did NOT mention: fuzzy matching, automatic CSV updates, caching. These are agent assumptions (need to add to checklist as questions)"

**My answer:** User did NOT mention:
- ADP multiplier formula (how to convert ADP 1-500 to multiplier)
- Player matching strategy (exact vs fuzzy)
- Default behavior when player not in ADP data
- ADP value ranges (min/max valid ADP)
- CSV location/filename
- Handling multiple players with same name

All of these are agent assumptions → Added to checklist as questions

**Evidence:** Reviewed epic notes, none of these topics mentioned

---

**Verification Result for Category 4:**

☑ All questions answered with ✅ GOOD level of detail
☑ Evidence provided for each answer

**Category 4: PASSED**

---

## Phase 1.5 Audit Summary

**Category 1 (Component Knowledge):** ✅ PASSED
**Category 2 (Pattern Knowledge):** ✅ PASSED
**Category 3 (Data Structure Knowledge):** ✅ PASSED
**Category 4 (Epic Request Knowledge):** ✅ PASSED

---

**OVERALL RESULT:** ✅ PASSED - All 4 categories passed, ready for Phase 2.2

---

**Evidence Summary:**

**Files Read:** 6
- league_helper/util/PlayerManager.py (lines 1-500)
- league_helper/util/FantasyPlayer.py (lines 1-100)
- league_helper/util/ConfigManager.py (lines 1-300)
- utils/csv_utils.py (lines 1-100)
- tests/league_helper/util/test_PlayerManager_scoring.py (entire file)
- data/players.csv (header + sample rows)

**Code Snippets Collected:** 8
- calculate_total_score() signature and implementation
- _calculate_injury_multiplier() full implementation
- _calculate_matchup_multiplier() signature
- get_injury_multiplier() signature
- read_csv_with_validation() signature
- FantasyPlayer class definition with fields
- Test pattern examples (3 test methods)

**Epic Notes Citations:** 8 line numbers
- Lines 8-10, 12-14, 15, 18-19, 22, 35, 37-38, 42, 45

**Ready for Phase 2.2:** YES

---

### Example 2: Audit with FAILURES (What NOT to do)

```markdown
## Research Completeness Audit (FAILED EXAMPLE)

### Category 1: Component Knowledge

**Question 1.1:** Can I list the EXACT classes/files that will be modified?

**My answer:** ❌ "Probably PlayerManager and maybe ConfigManager, not sure what else"

**Evidence:** ❌ None - didn't check file paths or line numbers

**FAILURE:** Vague answer, no evidence
**Action Required:** Use Glob to find files, Read to verify components, cite exact paths

---

**Question 1.2:** Have I READ the source code for each component?

**My answer:** ❌ "I used grep to search for PlayerManager but didn't actually read the file"

**Evidence:** ❌ grep results only, no Read tool calls

**FAILURE:** Searched but didn't READ
**Action Required:** Use Read tool to view actual source code, document what you found

---

**Question 1.3:** Can I cite actual method signatures from source?

**My answer:** ❌ "The scoring method probably takes a player and returns a number"

**Evidence:** ❌ None - guessing based on assumptions

**FAILURE:** Assumption, not actual code
**Action Required:** Read source file, copy exact signature with types and line number

---

**Verification Result for Category 1:** ❌ FAILED

**Must return to Phase 1 and:**
1. Find exact file paths for all components
2. READ source code (not just search)
3. Document actual signatures with evidence
4. Re-run audit after research complete

**DO NOT PROCEED TO Phase 2.2**
```

---

## Anti-Patterns to Avoid

### Anti-Pattern 1: Generic Research

❌ **WRONG:**
```markdown
## Research Questions

□ Understand how PlayerManager works
□ Learn about the scoring system
□ Research data loading patterns
□ Study the codebase architecture
```

✅ **CORRECT:**
```markdown
## Research Questions (Grounded in Epic)

Based on user request to "integrate ADP data into PlayerManager scoring using injury penalty pattern":

□ PlayerManager.calculate_total_score() - How does it work? (user mentioned scoring)
□ injury penalty pattern - What's the implementation? (user said to follow this pattern)
□ FantasyPros CSV - Does similar data exist? (user specified this data source)
```

**Why:** Epic intent guides research. Only research what user explicitly mentioned.

---

### Anti-Pattern 2: Assuming Instead of Reading

❌ **WRONG:**
```markdown
**PlayerManager probably has a calculate_score method that takes a player.**

I'll assume it returns a float and we can add ADP as a parameter.
```

✅ **CORRECT:**
```markdown
**PlayerManager.calculate_total_score() actual signature:**

```python
def calculate_total_score(self, player: FantasyPlayer, config: ConfigManager) -> float:
```

Source: league_helper/util/PlayerManager.py:125
Read timestamp: 2026-01-02 10:30

**Cannot add ADP as parameter** - would break interface (user constraint: "don't change interface too much")
**Must follow multiplier pattern instead** - add as separate calculation, multiply into result
```

**Why:** READ the actual code. Don't guess at signatures or patterns.

---

### Anti-Pattern 3: Skipping Phase 0

❌ **WRONG:**
```markdown
I remember from Stage 1 that user wants ADP integration. I'll start researching PlayerManager now.

{Jumps straight to Phase 1 without re-reading epic}
```

✅ **CORRECT:**
```markdown
**Phase 0: Epic Intent Extraction**

Even though I worked on Stage 1, I'm re-reading epic notes now to ensure I understand user intent.

{Re-reads epic notes file}
{Extracts exact quotes with line numbers}
{Creates Epic Intent section in spec.md}
{THEN proceeds to Phase 1}
```

**Why:** Context windows have limits. Session compaction may have lost details. Always re-read epic in Phase 0.

---

## Success Criteria Summary

**Research Phase (Phase 2.1) passes when:**

✅ **Phase 0 (Epic Intent):**
- Epic notes file re-read (not relied on memory)
- Exact quotes extracted with line citations
- Epic Intent section created as FIRST section in spec.md
- User's explicit requests documented
- Out-of-scope items identified

✅ **Phase 1 (Targeted Research):**
- Research grounded in epic intent (not generic)
- Components mentioned by user researched FIRST
- Source code READ (not just searched)
- Evidence collected (file paths, line numbers, code snippets)
- Research findings documented in epic/research/{FEATURE_NAME}_DISCOVERY.md

✅ **Phase 1.5 (Audit):**
- All 4 categories answered with evidence
- Can cite exact files, lines, signatures
- Can describe patterns from actual code
- Can identify assumptions vs. user requests
- Overall result: PASSED

**Ready for Phase 2.2 when all 3 phases complete with evidence.**

---

*End of research_examples.md*
