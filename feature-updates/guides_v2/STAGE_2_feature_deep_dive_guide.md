# STAGE 2: Feature Deep Dive Guide

🚨 **MANDATORY READING PROTOCOL**

**Before starting this stage:**
1. Use Read tool to load THIS ENTIRE GUIDE
2. Acknowledge critical requirements (see "Critical Rules" section below)
3. Verify prerequisites (see "Prerequisites Checklist" section below)
4. Update feature README.md Agent Status with guide name + timestamp

**DO NOT proceed without reading this guide.**

**After session compaction:**
- Check feature README.md Agent Status for current phase
- READ THIS GUIDE again (full guide, not summary)
- Continue from "Next Action" in Agent Status

---

## Quick Start

**6-Phase Overview:**
1. **Targeted Research** - Investigate THIS feature's scope only
2. **Update Spec & Checklist** - Document findings and open questions
3. **Interactive Question Resolution** - ONE question at a time, update after each answer
4. **Dynamic Scope Adjustment** - Evaluate if feature grew too large (split?)
5. **Cross-Feature Alignment** - Compare to other feature specs, resolve conflicts
6. **Acceptance Criteria & User Approval** - Create explicit acceptance criteria, get user sign-off (MANDATORY)

**Estimated Time:** 1-2 hours per feature
**Prerequisites:** Stage 1 complete, feature folder exists with initial spec.md
**Outputs:** Complete spec.md, all checklist items resolved, cross-feature alignment verified, user-approved acceptance criteria

---

## Critical Rules

```
┌─────────────────────────────────────────────────────────────┐
│ CRITICAL RULES - These MUST be copied to README Agent Status │
└─────────────────────────────────────────────────────────────┘

1. ⚠️ Targeted research for THIS feature ONLY (not entire epic)
   - Do NOT deep dive into other features yet
   - Keep research focused on current feature's scope

2. ⚠️ NEVER MAKE ASSUMPTIONS - CONFIRM WITH USER FIRST
   - Do NOT assume requirements, methodologies, or behavior
   - Do NOT write specs based on "what makes sense" or "best practices"
   - ASK USER via checklist.md questions BEFORE asserting in spec.md
   - Only document requirements after explicit user confirmation
   - If uncertain about ANY detail → create question in checklist.md
   - Spec assertions MUST be traced to user answers, not agent assumptions

3. ⚠️ ONE question at a time (Lesson Learned: don't batch questions)
   - Ask question
   - Wait for user answer
   - Update spec/checklist immediately
   - Evaluate for new questions
   - Then ask next question (if any)

4. ⚠️ Update spec.md and checklist.md IMMEDIATELY after each answer
   - Do NOT batch updates
   - Keep files current in real-time

5. ⚠️ All research documents go in epic's research/ folder
   - NOT in feature folder
   - Shared across all features

6. ⚠️ If scope grows >35 checklist items, propose split into multiple features
   - Trigger: Checklist has >35 items
   - Action: Propose splitting feature, return to Stage 1
   - Get user approval before splitting

7. ⚠️ Cross-feature alignment is MANDATORY
   - Compare THIS feature's spec to ALL already-completed feature specs
   - Look for: Conflicts, duplicate logic, incompatible assumptions
   - Resolve conflicts BEFORE marking feature complete

8. ⚠️ "New Scope" discovery: Use decision criteria (see Phase 4)
   - Independent subsystem? → New feature (return to Stage 1)
   - Extension of current feature? → Expanded scope (update spec)

9. ⚠️ Mark feature complete in epic EPIC_README.md
   - Update Feature Tracking table
   - Check off "Stage 2 Complete" for this feature

10. ⚠️ Do NOT start Stage 5a (TODO creation) from Stage 2
    - Stage 2 completes ALL feature deep dives first
    - Stage 3 (sanity check) and Stage 4 (testing strategy) come next

11. ⚠️ Update feature README.md Agent Status after EACH phase

12. ⚠️ Phase 6 (Acceptance Criteria & User Approval) is MANDATORY
    - MUST create explicit acceptance criteria in spec.md
    - MUST get user approval before proceeding to Stage 3
    - Prevents implementing wrong scope (saves massive rework)
    - User confirms WHAT before agent builds HOW
```

---

## Prerequisites Checklist

**Verify BEFORE starting Stage 2 for this feature:**

□ Stage 1 (Epic Planning) complete - verified in epic EPIC_README.md
□ This feature folder exists: `feature_{N}_{name}/`
□ Feature folder contains:
  - README.md (with Agent Status)
  - spec.md (initial scope from Stage 1)
  - checklist.md (empty or with preliminary items)
  - lessons_learned.md (template)
□ Epic EPIC_README.md Feature Tracking table lists this feature
□ No other feature currently in deep dive phase (work on ONE feature at a time)

**If any prerequisite fails:**
- ❌ STOP - Do NOT proceed with deep dive
- Complete missing prerequisites first
- Document blocker in feature README.md Agent Status

---

## Workflow Overview

```
┌──────────────────────────────────────────────────────────────┐
│                  STAGE 2 WORKFLOW (Per Feature)              │
└──────────────────────────────────────────────────────────────┘

Phase 1: Targeted Research
   ├─ Read initial spec.md from Stage 1
   ├─ Identify components/files to investigate
   ├─ Search codebase for relevant patterns
   ├─ Document findings in research/ folder
   └─ Update spec.md with technical details

Phase 2: Update Spec & Checklist
   ├─ Add detailed requirements to spec.md
   ├─ Document algorithms, data structures, interfaces
   ├─ Create checklist.md with open questions
   └─ Identify dependencies on other features

Phase 3: Interactive Question Resolution
   ├─ Ask ONE question
   ├─ Wait for user answer
   ├─ Update spec.md/checklist.md immediately
   ├─ Mark question as resolved in checklist
   ├─ Evaluate if new questions arose
   └─ Repeat until ALL questions resolved

Phase 4: Dynamic Scope Adjustment
   ├─ Count checklist items
   ├─ If >35 items: Propose split into multiple features
   ├─ If new work discovered: Evaluate "new feature" vs "expanded scope"
   ├─ Get user approval for scope changes
   └─ Update epic structure if needed (return to Stage 1)

Phase 5: Cross-Feature Alignment
   ├─ Identify all features with completed specs
   ├─ Compare THIS feature's spec to each completed spec
   ├─ Look for: Conflicts, duplicates, incompatible assumptions
   ├─ Resolve conflicts (update THIS feature or other features)
   └─ Document alignment verification

Mark Feature Complete
   ├─ Update epic EPIC_README.md Feature Tracking table
   ├─ Update feature README.md Agent Status
   └─ Announce completion to user
```

---

## Phase 1: Targeted Research

**Goal:** Understand THIS feature's technical requirements (NOT the entire epic)

### Step 1.1: Read Initial Spec from Stage 1

Read `feature_{N}_{name}/spec.md` created in Stage 1.

**Extract:**
- Feature purpose (what it does)
- Initial scope (what's included)
- Dependencies (what it needs)
- Files likely affected (rough list)

### Step 1.2: Identify Research Questions

Based on initial spec, list:

1. **What components will this feature modify?**
   - Classes, modules, managers
   - Which methods need changes?

2. **What existing patterns can we leverage?**
   - Similar features in codebase
   - Established architectural patterns

3. **What data structures are involved?**
   - Input/output formats
   - Internal data representations

4. **What interfaces do we depend on?**
   - External classes/methods we'll call
   - Need to verify exact signatures

5. **What edge cases exist?**
   - Error scenarios
   - Boundary conditions

### Step 1.3: Conduct Targeted Searches

**Use Glob and Grep to find relevant code:**

```bash
# Example searches (adjust based on feature)

# Find relevant classes
grep -r "class PlayerManager" --include="*.py"

# Find similar functionality
grep -r "calculate.*score" --include="*.py"

# Find data file patterns
find data/ -name "*.csv" -o -name "*.json"

# Find existing tests (patterns to follow)
grep -r "test.*player.*score" tests/ --include="*.py"
```

**Document findings:**

Create `epic/research/{FEATURE_NAME}_DISCOVERY.md`:

```markdown
# Feature {N}: {Name} - Discovery Findings

**Research Date:** {YYYY-MM-DD}
**Researcher:** Agent

---

## Components Identified

**Classes to Modify:**
- `PlayerManager` (league_helper/util/PlayerManager.py:125)
  - Method: `calculate_total_score()` - Will add new multiplier here
  - Method: `load_players()` - May need to load additional data

**Similar Existing Features:**
- Injury penalty system (league_helper/util/PlayerManager.py:450-480)
  - Uses similar multiplier pattern
  - Can reuse structure

**Data Structures:**
- Input: Player CSV with columns [Name, Position, Team, Points]
- Output: Updated PlayerManager with new score component
- Internal: Need to add `adp_multiplier` field to FantasyPlayer

## Interface Dependencies

**External Classes We'll Call:**
- `ConfigManager.get_adp_multiplier(adp_value)` → returns (multiplier, rating)
  - Source: league_helper/util/ConfigManager.py:234
  - Signature verified: def get_adp_multiplier(self, adp: int) -> Tuple[float, int]

**Data Files We'll Read:**
- `data/adp_rankings.csv` (NEW - need to create)
  - Format: Name,Position,ADP

## Edge Cases Identified

1. Player not in ADP data (how to handle?)
2. Invalid ADP value (negative, zero, >500)
3. Multiple players with same name (disambiguation)
4. ADP data file missing or corrupt

## Existing Test Patterns

Found test pattern in `tests/league_helper/util/test_PlayerManager_scoring.py`:
- Uses pytest fixtures for sample players
- Mocks ConfigManager
- Tests each multiplier in isolation

Can follow this pattern for ADP tests.

---

**Next Steps:**
- Update spec.md with these findings
- Create checklist.md with open questions
```

### Step 1.4: Update Agent Status

```markdown
## Agent Status

**Last Updated:** {YYYY-MM-DD HH:MM}
**Current Phase:** DEEP_DIVE
**Current Step:** Phase 1 - Targeted Research Complete
**Current Guide:** STAGE_2_feature_deep_dive_guide.md
**Guide Last Read:** {YYYY-MM-DD HH:MM}
**Critical Rules from Guide:**
- Targeted research for THIS feature only
- ONE question at a time (don't batch)
- All research in epic's research/ folder

**Progress:** 1/5 phases complete (Targeted Research)
**Next Action:** Phase 2 - Update spec.md and checklist.md
**Blockers:** None
```

---

## Phase 2: Update Spec & Checklist

**Goal:** Document findings in spec.md and create checklist.md with open questions

**🚨 CRITICAL: NO ASSUMPTIONS ALLOWED**

Before writing ANYTHING in spec.md, ask yourself:
- ❌ "Am I assuming this is the right approach?" → ASK USER via checklist.md
- ❌ "This seems like the obvious methodology" → ASK USER via checklist.md
- ❌ "Best practices say to do X" → ASK USER if they want X
- ✅ "User explicitly told me to do Y" → Document Y in spec.md

**Rule:** If you haven't asked the user and received explicit confirmation, it goes in checklist.md as a QUESTION, NOT in spec.md as a requirement.

### Step 2.1: Update spec.md with Technical Details

Add/expand these sections in `spec.md` - BUT ONLY with information you've CONFIRMED with the user or discovered through research (not assumptions):

**Components Affected:**
```markdown
## Components Affected

**Classes to Modify:**
1. **PlayerManager** (`league_helper/util/PlayerManager.py`)
   - `calculate_total_score()` method - Add ADP multiplier calculation
   - `load_players()` method - Load ADP data
   - New method: `_calculate_adp_multiplier()` - Encapsulate ADP logic

2. **ConfigManager** (`league_helper/util/ConfigManager.py`)
   - `get_adp_multiplier()` method - Already exists, will use

3. **FantasyPlayer** (`league_helper/util/FantasyPlayer.py`)
   - Add field: `adp_value: Optional[int]` - Store ADP ranking
   - Add field: `adp_multiplier: float` - Store calculated multiplier

**New Files to Create:**
- `data/adp_rankings.csv` - ADP data source
- `tests/league_helper/util/test_PlayerManager_adp.py` - ADP-specific tests
```

**Data Structures:**
```markdown
## Data Structures

**Input Data:**
```csv
Name,Position,ADP
Patrick Mahomes,QB,5
Christian McCaffrey,RB,1
...
```

**Internal Representation:**
```python
class FantasyPlayer:
    adp_value: Optional[int]  # 1-500, None if not in ADP data
    adp_multiplier: float     # 0.8-1.2 based on ADP
```

**Output:**
Updated `total_score` in PlayerManager with ADP multiplier applied
```

**Algorithms:**
```markdown
## Algorithms

### ADP Multiplier Calculation

**Pseudocode:**
```
1. Load ADP data from data/adp_rankings.csv
2. For each player:
   a. Match player name+position to ADP data
   b. If match found:
      - Get ADP value (1-500)
      - Call ConfigManager.get_adp_multiplier(adp_value)
      - Store multiplier in player.adp_multiplier
   c. If NO match found:
      - Use default multiplier (1.0 = neutral)
3. In calculate_total_score():
   total_score = base_score * adp_multiplier * [other multipliers...]
```

**Edge Case Handling:**
- Player not in ADP data → multiplier = 1.0 (neutral, no penalty/bonus)
- Invalid ADP (<1 or >500) → log warning, use 1.0
- Multiple players with same name → match on Name+Position
- ADP file missing → log error, all multipliers = 1.0 (graceful degradation)
```

**Dependencies:**
```markdown
## Dependencies

**This feature depends on:**
- ConfigManager.get_adp_multiplier() method (already exists)
- CSV utilities (utils/csv_utils.py) for reading ADP data
- FantasyPlayer class structure (can add fields)

**This feature blocks:**
- Feature 4: Recommendation Engine Updates (will use ADP multipliers)

**This feature is independent of:**
- Feature 2: Injury Risk Assessment (parallel, no interaction)
- Feature 3: Schedule Strength Analysis (parallel, no interaction)
```

### Step 2.2: Create checklist.md with Open Questions

Populate `checklist.md`:

```markdown
# Feature 1: ADP Integration - Planning Checklist

**Purpose:** Track open questions and decisions for this feature

**Instructions:**
- [ ] = Open question (needs user answer)
- [x] = Resolved (answer documented below)

---

## Open Questions

### Question 1: ADP Data Source
- [ ] Where should we get ADP data from?
  - Option A: External API (ESPN, Yahoo, etc.)
  - Option B: Manual CSV file (user provides)
  - Option C: Web scraping (FantasyPros, etc.)

**Context:** Need to decide data source to know how to implement loading logic.

**Recommendation:** Option B (manual CSV) - Simplest, no API dependencies, user controls data.

---

### Question 2: Player Name Matching
- [ ] How should we handle players with similar names?
  - Option A: Match on Name+Position (strict)
  - Option B: Fuzzy matching (handle typos)
  - Option C: Match on unique ID (requires ID in ADP data)

**Context:** CSV might have "Patrick Mahomes" while ADP has "P. Mahomes"

**Recommendation:** Option A (strict matching). If fuzzy matching is required, add it to the spec NOW - do not defer features "for later". Every requirement in the spec MUST be implemented 100%.

---

### Question 3: ADP Value Ranges
- [ ] What ADP range is valid?
  - Option A: 1-300 (typical league size)
  - Option B: 1-500 (larger leagues)
  - Option C: Configurable in league_config.json

**Context:** Need to validate ADP values and define multiplier ranges.

**Recommendation:** Option B (1-500) - Covers all league sizes.

---

### Question 4: Missing Player Behavior
- [ ] What happens if player NOT in ADP data?
  - Option A: Use multiplier = 1.0 (neutral, no bonus/penalty)
  - Option B: Use multiplier = 0.9 (slight penalty for unknown)
  - Option C: Log warning and exclude from draft recommendations

**Context:** Rookies or obscure players might not have ADP data.

**Recommendation:** Option A (neutral 1.0) - Don't penalize players for missing data.

---

### Question 5: ADP Update Frequency
- [ ] How often should ADP data be updated?
  - Option A: Manual (user downloads new CSV)
  - Option B: Automatic (fetch weekly)
  - Option C: On-demand (fetch when user requests)

**Context:** ADP values change during draft season.

**Recommendation:** Option A (manual updates). If automatic updates are required, add them to the spec NOW. Do not leave features as "for later" - implement 100% of requirements specified in the spec.

---

## Resolved Questions

{Will populate as questions are answered}

---

## Additional Scope Discovered

{Will document if deep dive reveals new work not in original scope}
```

### Step 2.3: Update Agent Status

```markdown
## Agent Status

**Last Updated:** {YYYY-MM-DD HH:MM}
**Current Phase:** DEEP_DIVE
**Current Step:** Phase 2 - Spec & Checklist Updated
**Current Guide:** STAGE_2_feature_deep_dive_guide.md
**Guide Last Read:** {YYYY-MM-DD HH:MM}
**Critical Rules from Guide:**
- ONE question at a time (don't batch)
- Update spec/checklist immediately after each answer
- Research documents in epic's research/ folder

**Progress:** 2/5 phases complete (Spec & Checklist)
**Next Action:** Phase 3 - Ask first question from checklist
**Blockers:** None

**Checklist Status:** 5 open questions, 0 resolved
```

---

## Phase 3: Interactive Question Resolution

**Goal:** Resolve ALL checklist questions ONE AT A TIME

### Step 3.1: Select Next Question

**Priority order:**
1. **Blocking questions** - Must be answered before other questions make sense
2. **High-impact questions** - Affect algorithm or data structure design
3. **Low-impact questions** - Implementation details

**Example blocking question:** "Where should we get ADP data from?" (affects all other decisions)

### Step 3.2: Ask ONE Question

**Format:**

```markdown
I have a question about Feature 1 (ADP Integration):

## Question 1: ADP Data Source

**Context:** We need to decide where to get ADP data from to implement the loading logic.

**Options:**

A. **External API** (ESPN, Yahoo, etc.)
   - Pros: Always up-to-date, automatic
   - Cons: API dependencies, rate limits, complexity

B. **Manual CSV file** (user provides)
   - Pros: Simple, user controls data, no dependencies
   - Cons: Manual updates, user must find data source

C. **Web scraping** (FantasyPros, etc.)
   - Pros: Automatic, no API key needed
   - Cons: Fragile (site changes break it), legal concerns

**My recommendation:** Option B (Manual CSV) because it's simplest and gives user control.

**What do you prefer?** (or suggest a different approach)
```

### Step 3.3: WAIT for User Answer

⚠️ **STOP HERE - Do NOT proceed without user answer**

**Update Agent Status:**
```markdown
**Progress:** 2/5 phases complete (Phase 3 - Waiting for answer to Question 1)
**Next Action:** Wait for user answer to Question 1
**Blockers:** Waiting for user input on ADP data source
```

### Step 3.4: Update Spec & Checklist Immediately

**After user answers**, update files IMMEDIATELY:

**Update checklist.md:**
```markdown
### Question 1: ADP Data Source
- [x] **RESOLVED:** Manual CSV file (user provides)

**User's Answer:**
{Paste user's exact answer or paraphrase}

**Implementation Impact:**
- Create CSV reader in PlayerManager
- Document CSV format in README
- No API client needed
```

**Update spec.md:**
```markdown
## Data Sources

**ADP Data:**
- Source: Manual CSV file (`data/adp_rankings.csv`)
- User provides file (download from FantasyPros, ESPN, etc.)
- Format: Name,Position,ADP
- Updated: User responsible for updating file
```

### Step 3.5: Evaluate for New Questions

**After updating files, ask:**
- Did this answer create NEW questions?
- Did this answer resolve OTHER questions?

**Example:**
- Answered "Manual CSV" → Resolves Question 5 (update frequency = manual)
- Created new question: "What CSV format documentation should we provide?"

**Update checklist.md:**
```markdown
### Question 5: ADP Update Frequency
- [x] **RESOLVED:** Manual (follows from Question 1 answer)

**Rationale:** Since we're using manual CSV (Question 1), updates are manual.

---

### NEW Question 6: CSV Format Documentation
- [ ] What level of documentation should we provide for CSV format?
  - Option A: Comment in code
  - Option B: README section
  - Option C: Dedicated CSV_FORMAT.md file

**Context:** User needs to know how to format CSV file.
```

### Step 3.6: Repeat Until ALL Questions Resolved

Continue asking questions ONE AT A TIME until checklist shows:

```markdown
**Checklist Status:** 0 open questions, 8 resolved
```

**Update Agent Status after each question:**
```markdown
**Progress:** Phase 3 - Question 3/8 answered
**Next Action:** Ask Question 4
**Blockers:** None
```

---

## Phase 4: Dynamic Scope Adjustment

**Goal:** Evaluate if feature scope grew too large (requires split)

### Step 4.1: Count Checklist Items

Count total items in spec.md:
- Requirements
- Algorithms
- Edge cases to handle
- Tests to write
- Files to create/modify

**Example count:**
- 3 classes to modify
- 2 new files to create
- 5 algorithms to implement
- 8 edge cases to handle
- 12 tests to write
- Total: ~30 items

### Step 4.2: Evaluate "New Scope" vs "Expanded Scope"

**If deep dive revealed ADDITIONAL WORK, use decision criteria:**

**RETURN TO STAGE 1 (Add New Feature) if:**
- ✅ Work is independent subsystem (can develop/test separately)
- ✅ Work requires 3+ major components NOT in current feature's scope
- ✅ Work has different dependencies than current feature
- ✅ Work addresses different aspect of epic request
- ✅ Work could fail independently without affecting current feature
- ✅ Work represents 20+ new checklist items

**Example:** While planning "Player Data Loading", discovered need for "Data Validation Service" (separate API validation layer, different components, independent failure modes) → ADD NEW FEATURE

**HANDLE WITHIN STAGE 2 (Expanded Scope) if:**
- ✅ Work is extension of current feature's functionality
- ✅ Work uses same components already identified
- ✅ Work has same dependencies as current feature
- ✅ Work is directly related to current feature's core purpose
- ✅ Work cannot function independently (tightly coupled)
- ✅ Work represents <20 new checklist items

**Example:** While planning "Player Data Loading", discovered need for error handling, retry logic, progress logging → UPDATE CURRENT FEATURE SPEC

### Step 4.3: If Scope >35 Items, Propose Split

**If checklist has >35 items:**

```markdown
## Scope Assessment

**Feature 1 (ADP Integration) has grown to 47 items.**

**Current scope includes:**
- Load ADP data (15 items)
- Parse and validate data (12 items)
- Integrate into scoring system (10 items)
- Build recommendation engine (10 items)

**Proposed split:**

**Feature 1a: ADP Data Integration** (~25 items)
- Load ADP data
- Parse and validate
- Integrate into scoring

**Feature 1b: ADP-Based Recommendations** (~22 items)
- Build recommendation engine using ADP scores
- UI display updates
- User interaction

**Rationale:**
- Data integration can be tested independently
- Recommendation engine depends on integration
- Clear boundary: Data layer vs UI layer
- Each feature is manageable size

**Recommend:**
- Split Feature 1 into Features 1a and 1b
- Return to Stage 1 to create new feature folder
- Continue Stage 2 for both features

**Do you approve this split?**
```

### Step 4.4: Get User Approval for Scope Changes

⚠️ **WAIT for user approval before modifying epic structure**

**If approved:**
1. Document decision in current feature's README.md
2. Return to Stage 1 guide
3. Create new feature folder(s)
4. Update epic EPIC_README.md Feature Tracking table
5. Continue Stage 2 for updated features

**If rejected:**
1. Document decision in current feature's README.md
2. Continue with current scope (but may be risky if too large)

---

## Phase 5: Cross-Feature Alignment

**Goal:** Compare THIS feature's spec to OTHER completed features, resolve conflicts

### Step 5.1: Identify Completed Features

Check epic EPIC_README.md Feature Tracking table:

```markdown
| # | Feature Name | Stage 2 Complete | Notes |
|---|--------------|------------------|-------|
| 1 | feature_01_adp_integration | [x] | ← Currently completing |
| 2 | feature_02_injury_assessment | [ ] | Not started |
| 3 | feature_03_schedule_analysis | [ ] | Not started |
| 4 | feature_04_recommendation_updates | [ ] | Not started |
```

**In this example:** No other features completed yet (Feature 1 is first).

**If this is NOT the first feature:**
- List all features with `[x]` in "Stage 2 Complete" column
- Will compare THIS feature to those features

### Step 5.2: Compare Specs (If Not First Feature)

**For EACH completed feature, compare:**

1. **Data Structures:**
   - Do we define same data in different ways?
   - Do we use different field names for same concept?
   - **Example conflict:** Feature 1 uses `adp_value: int`, Feature 2 uses `adp_rank: str`

2. **Interfaces:**
   - Do we call same methods with different assumptions?
   - Do we expect different return types?
   - **Example conflict:** Feature 1 expects `get_player()` returns `Optional[Player]`, Feature 2 assumes it always returns `Player`

3. **File Locations:**
   - Do we create files in different locations?
   - **Example conflict:** Feature 1 puts data in `data/adp/`, Feature 2 puts data in `data/rankings/`

4. **Configuration:**
   - Do we add config with conflicting keys?
   - **Example conflict:** Both add `"multiplier_threshold"` but mean different things

5. **Dependencies:**
   - Do we depend on same component but assume different behavior?
   - **Example conflict:** Feature 1 assumes PlayerManager loads CSV, Feature 2 assumes it loads JSON

### Step 5.3: Document Conflicts Found

Create `epic/research/ALIGNMENT_CHECK_{DATE}.md`:

```markdown
# Cross-Feature Alignment Check

**Date:** {YYYY-MM-DD}
**Feature Being Aligned:** Feature 1 (ADP Integration)
**Compared Against:** N/A (first feature in epic)

---

## Comparison Results

**No conflicts found** - This is the first feature in the epic.

**For future features:** Compare against THIS feature's spec to ensure alignment.

---

**Next Steps:**
- Mark Feature 1 as "Stage 2 Complete" in epic EPIC_README.md
- When Feature 2 begins Stage 2, compare against Feature 1
```

**If conflicts ARE found:**

```markdown
## Conflicts Identified

### Conflict 1: Data File Location
**Feature 1 spec:** Creates `data/adp_rankings.csv`
**Feature 3 spec:** Creates `data/schedule_strength.csv`
**Conflict:** Both in root data/ folder (could use subdirectories)

**Resolution:**
- Update Feature 1: `data/rankings/adp.csv`
- Update Feature 3: `data/rankings/schedule_strength.csv`
- Reasoning: Group all ranking data together

**Files to update:**
- [ ] Feature 1 spec.md
- [ ] Feature 3 spec.md

---

### Conflict 2: PlayerManager Method Signature
**Feature 1 assumes:** `get_player(name: str) -> Optional[Player]`
**Feature 2 assumes:** `get_player(name: str) -> Player` (no Optional)

**Conflict:** Feature 2 will crash if player not found

**Resolution:**
- Update Feature 2 spec: Handle Optional return type
- Add null check in Feature 2 algorithm
- Reasoning: Feature 1 is correct (player might not exist)

**Files to update:**
- [ ] Feature 2 spec.md (add null handling)
```

### Step 5.4: Resolve Conflicts

**For EACH conflict:**

1. **Determine correct approach** (which feature's assumption is right?)
2. **Update affected specs** (may be THIS feature or OTHERS)
3. **Document resolution** in alignment check file
4. **Notify user** if significant changes needed

**After resolving all conflicts:**
```markdown
## Conflicts Resolved

- [x] Conflict 1: Data file location - Both specs updated
- [x] Conflict 2: Method signature - Feature 2 spec updated

**All features now aligned.**
```

### Step 5.5: Update Agent Status

```markdown
## Agent Status

**Last Updated:** {YYYY-MM-DD HH:MM}
**Current Phase:** DEEP_DIVE
**Current Step:** Phase 5 - Cross-Feature Alignment Complete
**Current Guide:** STAGE_2_feature_deep_dive_guide.md
**Guide Last Read:** {YYYY-MM-DD HH:MM}
**Critical Rules from Guide:**
- Mark feature complete in epic EPIC_README.md
- Update Feature Tracking table

**Progress:** 5/6 phases complete (Ready for acceptance criteria approval)
**Next Action:** Phase 6 - Create Acceptance Criteria & Get User Approval
**Blockers:** None
```

---

## Phase 6: Acceptance Criteria & Deliverables Approval (MANDATORY)

**Goal:** Create explicit acceptance criteria and get user approval BEFORE implementation

**⚠️ CRITICAL:** This phase prevents entire epics from being implemented incorrectly. User must approve WHAT will be built before you build it.

---

### Why This Phase Exists

**Real-World Example (Epic: fix_2025_adp):**
- Epic implemented 102+ hours of work
- All unit tests passed (2,463/2,463)
- Stage 6 Epic QC passed
- **Stage 7 user testing revealed:** ENTIRE EPIC TARGETED WRONG FOLDER
- Root cause: No explicit acceptance criteria approved by user
- Result: Massive rework required (wrong 6 files instead of correct 108 files)

**Lesson:** Explicit acceptance criteria with user approval prevents wrong implementations.

---

### Step 6.1: Create Acceptance Criteria Section in spec.md

Add this MANDATORY section to spec.md:

```markdown
---

## Acceptance Criteria (⚠️ USER MUST APPROVE)

**Files Modified:**
- [ ] {List EXACT file paths that will be modified}
- [ ] {Include counts: e.g., "108 files total: 18 weeks × 6 positions"}
- [ ] {Be specific: "simulation/sim_data/2025/weeks/week_01/qb_data.json" not "some JSON files"}

**Example:**
- [ ] simulation/sim_data/2025/weeks/week_01/qb_data.json
- [ ] simulation/sim_data/2025/weeks/week_01/rb_data.json
- [ ] simulation/sim_data/2025/weeks/week_01/wr_data.json
- [ ] ... (105 more files across weeks 01-18)
- [ ] Total: 108 files (18 weeks × 6 positions)

**Data Structures:**
- [ ] {Expected format: direct arrays, wrapped dicts, CSV columns, etc.}
- [ ] {Include examples of BEFORE and AFTER states}

**Example:**
- [ ] Files use direct JSON arrays: `[{player1}, {player2}, ...]`
- [ ] NOT wrapped dicts: `{"qb_data": [...]}`
- [ ] Each player object has: name, id, average_draft_position

**Behavior Changes:**
- [ ] {EXACTLY what will change and how}
- [ ] {Include expected values/ranges}
- [ ] {What stays the same}

**Example:**
- [ ] Players with ADP 170.0 (placeholder) → actual FantasyPros ADP values (range: 1.0-500.0)
- [ ] Unmatched players keep 170.0 default
- [ ] Match rate expected: >85% (650+ out of 739 players)
- [ ] All other player fields remain unchanged

**Deliverables:**
- [ ] {List what will be created: files, modules, tests}
- [ ] {Include line counts or complexity estimates}

**Example:**
- [ ] utils/adp_csv_loader.py (new module, ~100 lines)
- [ ] utils/adp_updater.py (new module, ~300 lines)
- [ ] tests/utils/test_adp_csv_loader.py (~15 tests)
- [ ] tests/utils/test_adp_updater.py (~25 tests)
- [ ] Match report (JSON file with matched/unmatched players)

**Success Criteria:**
- [ ] {How to verify feature works}
- [ ] {Measurable outcomes}

**Example:**
- [ ] All 108 files updated (verified by file modification timestamps)
- [ ] ADP values changed from 170.0 to actual values (verified by spot-checking 10 random players)
- [ ] Match rate >85% (verified in match report)
- [ ] All unit tests pass (100% pass rate)

---

⚠️ **USER APPROVAL REQUIRED:**

**User, please review the above acceptance criteria and confirm:**

[ ] YES - These acceptance criteria are correct, proceed with implementation
[ ] NO - Acceptance criteria need changes (specify what's wrong)

**Agent: DO NOT proceed to Stage 3 without explicit user approval above.**
```

---

### Step 6.2: Present Acceptance Criteria to User

**Use AskUserQuestion tool with this format:**

```markdown
I've created detailed acceptance criteria for this feature in spec.md.

Please review the "Acceptance Criteria (USER MUST APPROVE)" section and confirm:

**Files Modified:** {brief summary - e.g., "108 simulation files across 18 weeks"}
**Data Structures:** {brief summary - e.g., "Direct JSON arrays, not wrapped dicts"}
**Behavior Changes:** {brief summary - e.g., "ADP values: 170.0 → actual FantasyPros values"}
**Deliverables:** {brief summary - e.g., "2 new modules, 40 tests, match report"}

Are these acceptance criteria correct?
```

**Options:**
1. "Yes, proceed with implementation" (Recommended if criteria match user's intent)
2. "No, needs changes" (Select if criteria don't match what you want)

---

### Step 6.3: Handle User Response

**If user approves ("Yes"):**
1. Update spec.md: Change `[ ]` to `[x]` for "USER APPROVAL REQUIRED"
2. Document approval timestamp in spec.md
3. Proceed to "Mark Feature Complete" section below

**If user rejects ("No") or requests changes:**
1. Ask user: "What specifically needs to change in the acceptance criteria?"
2. Update spec.md based on user feedback
3. Return to Step 6.2 (re-present for approval)
4. Repeat until user approves

**Example user feedback:**
```
User: "No, you're targeting the wrong folder. Should be simulation/sim_data/2025/weeks/, not data/player_data/"

Agent response:
1. Update spec.md acceptance criteria with correct folder paths
2. Update file counts (108 files instead of 6)
3. Re-present acceptance criteria for approval
```

---

### Step 6.4: Document Approval in spec.md

Once approved, update spec.md:

```markdown
⚠️ **USER APPROVAL REQUIRED:**

[x] YES - These acceptance criteria are correct, proceed with implementation

**Approved by:** User
**Approved on:** {YYYY-MM-DD HH:MM}
**Agent:** Confirmed acceptance criteria reviewed and approved before Stage 3
```

---

### Step 6.5: Update Agent Status

```markdown
## Agent Status

**Last Updated:** {YYYY-MM-DD HH:MM}
**Current Phase:** DEEP_DIVE
**Current Step:** Phase 6 - Acceptance Criteria Approved
**Current Guide:** STAGE_2_feature_deep_dive_guide.md
**Guide Last Read:** {YYYY-MM-DD HH:MM}
**Critical Rules from Guide:**
- Acceptance criteria approved by user
- Mark feature complete in epic EPIC_README.md

**Progress:** 6/6 phases complete (Ready to mark feature complete)
**Next Action:** Mark feature as "Stage 2 Complete" in epic EPIC_README.md
**Blockers:** None
```

---

**Why This Matters:**

1. **Prevents wrong implementations** - User confirms WHAT before agent builds HOW
2. **Explicit, not assumed** - Agent can't assume user intent, must get approval
3. **Concrete, not vague** - Exact file paths, counts, structures (not "some files")
4. **Early detection** - Wrong scope caught in Stage 2, not Stage 7
5. **Documentation** - Approval recorded for future reference

---

## Mark Feature Complete

### Step 1: Update Epic EPIC_README.md

Update Feature Tracking table:

```markdown
| # | Feature Name | Stage 2 Complete | Stage 5e Complete | Notes |
|---|--------------|------------------|-------------------|-------|
| 1 | feature_01_adp_integration | [x] | [ ] | Spec complete {date} |
| 2 | feature_02_injury_assessment | [ ] | [ ] | Not started |
```

### Step 2: Update Feature README.md

Update Feature Completion Checklist:

```markdown
**Stage 2 (Deep Dive):**
- [x] spec.md created and complete
- [x] checklist.md all items resolved
- [x] Compared to other feature specs (N/A - first feature)
- [x] Updated epic EPIC_README.md
```

Update Agent Status:

```markdown
## Agent Status

**Last Updated:** {YYYY-MM-DD HH:MM}
**Current Phase:** DEEP_DIVE_COMPLETE
**Current Step:** Feature 1 deep dive complete, ready for next feature
**Current Guide:** STAGE_2_feature_deep_dive_guide.md
**Guide Last Read:** {YYYY-MM-DD HH:MM}

**Progress:** Stage 2 complete for Feature 1
**Next Action:** Begin Stage 2 for Feature 2 (or proceed to Stage 3 if all features complete)
**Blockers:** None
```

### Step 3: Announce Completion

```markdown
✅ **Feature 1 (ADP Integration) - Stage 2 Deep Dive Complete**

**Spec.md status:** Complete
- 3 components identified
- 5 algorithms documented
- 8 edge cases defined
- ~30 implementation items estimated

**Checklist status:** 8 questions asked and resolved

**Cross-feature alignment:** Verified (first feature, no conflicts)

**Next:** Begin Stage 2 for Feature 2 (Injury Risk Assessment)
```

---

## When ALL Features Complete Stage 2

**After the LAST feature completes Phase 5:**

```markdown
✅ **ALL Features Complete Stage 2 (Deep Dive)**

**Features with complete specs:**
- Feature 1: ADP Integration
- Feature 2: Injury Risk Assessment
- Feature 3: Schedule Strength Analysis
- Feature 4: Recommendation Engine Updates

**Next: Stage 3 (Cross-Feature Sanity Check)**

I'll now transition to `STAGE_3_cross_feature_sanity_check_guide.md` to systematically compare all feature specs and resolve any final conflicts before implementation.
```

**Update epic EPIC_README.md Agent Status:**

```markdown
## Agent Status

**Last Updated:** {YYYY-MM-DD HH:MM}
**Current Phase:** SANITY_CHECK
**Current Step:** Ready to begin Stage 3
**Current Guide:** STAGE_3_cross_feature_sanity_check_guide.md
**Guide Last Read:** NOT YET (will read when starting Stage 3)

**Progress:** Stage 2 complete for all {N} features
**Next Action:** Read STAGE_3_cross_feature_sanity_check_guide.md and begin sanity check
**Blockers:** None

**Features Ready for Stage 3:**
- All {N} features have complete specs
- All checklists resolved
- Per-feature alignment checks complete
```

---

## 🔄 Mandatory Re-Reading Checkpoints

**CHECKPOINT 1:** After completing Phase 2 (Spec & Checklist)
- Re-read "Critical Rules" section
- Verify checklist has open questions (not all resolved yet)
- Verify you're asking ONE question at a time (not batching)
- Update feature README.md Agent Status

**CHECKPOINT 2:** After resolving 50% of questions (Phase 3)
- Re-read "Interactive Question Resolution" section
- Verify you're updating spec/checklist after EACH answer (not batching)
- Verify new questions are being added to checklist as discovered
- Check for scope creep (growing item count)

**CHECKPOINT 3:** Before marking feature complete (Phase 5)
- Re-read "Completion Criteria" section below
- Verify ALL checklist items resolved
- Verify cross-feature alignment performed (if not first feature)
- Verify epic EPIC_README.md updated

**Why this matters:** Deep dives are detailed work. Re-reading prevents shortcuts.

---

## Completion Criteria

**Stage 2 is complete for THIS feature when ALL of these are true:**

□ spec.md is complete with:
  - Components Affected section (detailed)
  - Data Structures section (with examples)
  - Algorithms section (pseudocode or description)
  - Dependencies section (what this feature needs/blocks)
  - Edge Cases section (how to handle errors)
  - Files Likely Affected (specific paths and line numbers)
□ checklist.md shows:
  - ALL questions marked [x] (resolved)
  - User answers documented for each question
  - No open [ ] questions remaining
□ Research findings documented in epic/research/ folder
□ Cross-feature alignment performed (Phase 5):
  - Compared to all features with "Stage 2 Complete"
  - Conflicts identified and resolved
  - Alignment report in epic/research/
□ Feature README.md updated:
  - Feature Completion Checklist: Stage 2 items checked
  - Agent Status: Phase = DEEP_DIVE_COMPLETE
□ Epic EPIC_README.md updated:
  - Feature Tracking table: Stage 2 Complete = [x] for this feature
  - Epic Completion Checklist: "Feature {N} spec complete" noted

**If any item unchecked:**
- ❌ Stage 2 is NOT complete for this feature
- ❌ Do NOT proceed to next feature or Stage 3
- Complete missing items first

---

## Common Mistakes to Avoid

```
┌────────────────────────────────────────────────────────────┐
│ "If You're Thinking This, STOP" - Anti-Pattern Detection  │
└────────────────────────────────────────────────────────────┘

❌ "I'll research the entire epic now"
   ✅ STOP - Research THIS feature only (targeted, not comprehensive)

❌ "Let me ask all 8 questions at once"
   ✅ STOP - ONE question at a time, update after each

❌ "I'll update the specs after all questions are answered"
   ✅ STOP - Update IMMEDIATELY after each answer (real-time)

❌ "This checklist has 50 items, but it's fine"
   ✅ STOP - Propose split if >35 items (too large)

❌ "I'll skip cross-feature alignment, looks similar enough"
   ✅ STOP - MUST compare specs to find conflicts

❌ "Let me start TODO creation for this feature"
   ✅ STOP - Stage 2 completes ALL features first, then Stage 3, then Stage 4, THEN Stage 5a

❌ "New work discovered, I'll just add it to this feature"
   ✅ STOP - Use decision criteria (new feature vs expanded scope)

❌ "Feature 1 is done, I'll mark the epic complete"
   ✅ STOP - Epic needs ALL features complete, not just one

❌ "Research document goes in feature folder"
   ✅ STOP - Research goes in epic/research/ (shared)

❌ "I'll remember to mark the feature complete later"
   ✅ STOP - Update epic EPIC_README.md NOW (before moving to next feature)
```

---

## Real-World Examples

### Example 1: Good Deep Dive Process

**Feature:** ADP Integration

**Phase 1:** Targeted research
- Searched for "calculate_score" in PlayerManager
- Found existing multiplier pattern
- Documented in research/ADP_DISCOVERY.md

**Phase 2:** Updated spec
- Added Components: PlayerManager, ConfigManager, FantasyPlayer
- Added Algorithm: Pseudocode for ADP loading and calculation
- Created checklist with 5 questions

**Phase 3:** Interactive questions (ONE AT A TIME)
- Asked Question 1: "Where should ADP data come from?"
- User answered: "Manual CSV"
- IMMEDIATELY updated spec.md and checklist.md
- Asked Question 2: "How to handle missing players?"
- User answered: "Use neutral multiplier 1.0"
- IMMEDIATELY updated files again
- (Continued for all 5 questions)

**Phase 4:** Scope check
- Counted: 28 items (<35 threshold)
- No split needed
- No new scope discovered

**Phase 5:** Alignment
- First feature in epic (no conflicts possible)
- Documented in research/ALIGNMENT_CHECK.md

**Result:** Complete spec, all questions resolved, ready for Stage 3

---

### Example 2: Scope Grew Too Large

**Feature:** Recommendation Engine Updates

**During deep dive:**
- Initial estimate: 20 items
- After research: 52 items discovered

**Checklist had:**
- 15 integration points
- 12 UI updates
- 10 algorithm changes
- 8 data transformations
- 7 test scenarios

**Agent proposed split:**
```
Feature 4a: Recommendation Algorithm Updates (25 items)
- Core algorithm changes
- Data transformations
- Unit tests

Feature 4b: Recommendation UI Updates (27 items)
- UI display updates
- User interaction
- Integration tests
```

**User approved split.**

**Actions taken:**
1. Documented split decision in feature_04/README.md
2. Returned to Stage 1 guide
3. Created feature_04a and feature_04b folders
4. Updated epic EPIC_README.md Feature Tracking (now 5 features)
5. Continued Stage 2 for both new features

---

### Example 3: Cross-Feature Conflict

**Feature 2** (Injury Assessment) completing Phase 5.

**Compared to Feature 1** (ADP Integration - already complete).

**Conflict found:**

**Feature 1 spec:** Adds `adp_multiplier` field to FantasyPlayer
```python
class FantasyPlayer:
    adp_multiplier: float
```

**Feature 2 spec:** Also adds `injury_multiplier` field
```python
class FantasyPlayer:
    injury_multiplier: float
```

**No conflict yet, but...**

**Feature 1 algorithm:**
```
total_score = base_score * adp_multiplier * [other multipliers]
```

**Feature 2 algorithm:**
```
total_score = base_score * injury_multiplier
```

**Conflict identified:** Both features multiply base_score by ONE multiplier. But when BOTH features are implemented, need to multiply by BOTH.

**Resolution:**
```
total_score = base_score * adp_multiplier * injury_multiplier * [other multipliers]
```

**Actions:**
1. Update Feature 2 spec: Algorithm shows ALL multipliers
2. Update Feature 1 spec: Note that other features will add multipliers
3. Document resolution in research/ALIGNMENT_CHECK.md
4. Create integration test plan: Test scoring with BOTH features active

---

### Example 4: "New Scope" Decision

**Feature:** Player Data Loading

**During deep dive, discovered:** Need for data validation service (validate player stats are reasonable).

**Evaluation using decision criteria:**

**Is it independent subsystem?** YES - Validation logic separate from loading
**Does it require 3+ new components?** YES - Validator class, validation rules config, error reporter
**Different dependencies?** YES - Validation depends on loaded data (not parallel)
**Different aspect of epic?** YES - Data quality vs data loading
**Could fail independently?** YES - Loading could work but validation could fail
**20+ new items?** YES - 25 items estimated

**Decision:** NEW FEATURE - Return to Stage 1

**Actions:**
1. Documented discovery in feature_01/README.md
2. Updated epic EPIC_README.md: "Feature 5: Data Validation Service discovered during Feature 1 deep dive"
3. Returned to Stage 1 guide
4. Created feature_05_data_validation/ folder
5. Updated Feature Tracking table (now 5 features)
6. Continued Stage 2 for Features 1-5

---

## README Agent Status Update Requirements

**Update feature README.md Agent Status at these points:**

1. ⚡ After Phase 1 complete (Targeted Research)
2. ⚡ After Phase 2 complete (Spec & Checklist)
3. ⚡ After EACH question answered in Phase 3 (increment question count)
4. ⚡ After Phase 4 complete (Scope Adjustment)
5. ⚡ After Phase 5 complete (Cross-Feature Alignment)
6. ⚡ When marking feature complete (update both feature and epic READMEs)
7. ⚡ After session compaction (update "Guide Last Read" with re-read timestamp)
8. ⚡ When blocked waiting for user answer (mark blocker)

---

## Guide Comprehension Verification

**Before starting Stage 2, answer these questions:**

1. Should you research the ENTIRE epic or just THIS feature?
   {Answer: Just THIS feature - targeted research}

2. How many questions should you ask at once?
   {Answer: ONE question at a time}

3. When should you update spec.md after getting an answer?
   {Answer: IMMEDIATELY after each answer (not batched)}

4. What's the trigger for proposing a feature split?
   {Answer: Checklist grows >35 items}

5. Where do research documents go?
   {Answer: epic/research/ folder (shared across features)}

6. Can you start Stage 5a (TODO creation) after Feature 1 completes Stage 2?
   {Answer: NO - Must complete Stage 2 for ALL features, then Stage 3, then Stage 4, THEN Stage 5a}

**Document your answers in feature README.md notes** to prove guide comprehension.

---

## Prerequisites for Stage 3

**Before transitioning to Stage 3, verify:**

□ ALL features have completed Stage 2 (check epic EPIC_README.md Feature Tracking)
□ Every feature has:
  - Complete spec.md
  - All checklist items resolved
  - Cross-feature alignment performed
  - **Acceptance criteria created and USER-APPROVED**
□ Every feature spec.md contains:
  - "Acceptance Criteria (USER MUST APPROVE)" section
  - User approval checkbox marked [x]
  - Approval timestamp documented
□ Epic EPIC_README.md shows all features with "[x]" in "Stage 2 Complete" column
□ No features have open questions or blockers

**If any prerequisite fails:**
- ❌ Do NOT transition to Stage 3
- Complete remaining Stage 2 work for incomplete features

---

## Next Stage

**After ALL features complete Stage 2:**

📖 **READ:** `STAGE_3_cross_feature_sanity_check_guide.md`
🎯 **GOAL:** Systematically compare all feature specs, resolve conflicts
⏱️ **ESTIMATE:** 30-60 minutes (for entire epic)

**Stage 3 will:**
- Compare all feature specs side-by-side
- Identify remaining conflicts (missed in per-feature alignment)
- Ensure requirements are aligned across all features
- Get user sign-off on complete plan before Stage 4

**Remember:** Use the phase transition prompt from `prompts_reference_v2.md` when starting Stage 3.

---

*End of STAGE_2_feature_deep_dive_guide.md*
