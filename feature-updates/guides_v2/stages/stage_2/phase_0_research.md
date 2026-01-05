# STAGE 2a: Research Phase Guide

**Guide Version:** 1.0
**Created:** 2026-01-02
**Prerequisites:** Stage 1 complete, feature folder exists
**Next Stage:** stages/stage_2/phase_1_specification.md

---

## 🚨 MANDATORY READING PROTOCOL

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

**What is this stage?**
Research Phase is the first part of Feature Deep Dive where you extract epic intent, conduct targeted research grounded in user requests, and verify research completeness through a mandatory audit before creating specifications.

**When do you use this guide?**
- Stage 1 complete (epic folder structure created)
- Feature folder exists with initial spec.md
- Ready to begin deep dive for this specific feature
- Starting from scratch on feature research

**Key Outputs:**
- ✅ Epic Intent section added to spec.md (user's original request with quotes)
- ✅ Targeted research complete (components user mentioned, not generic research)
- ✅ Research findings documented in epic/research/{FEATURE_NAME}_DISCOVERY.md
- ✅ Phase 1.5 Research Completeness Audit PASSED (MANDATORY GATE)
- ✅ Evidence collected (file paths, line numbers, code snippets)
- ✅ Ready for STAGE_2b (Specification Phase)

**Time Estimate:**
45-60 minutes (3 phases)

**Exit Condition:**
Research Phase is complete when Phase 1.5 audit passes (all 4 categories with evidence), Epic Intent section is documented in spec.md, and research findings are ready for spec creation.

---

## Critical Rules

```
┌─────────────────────────────────────────────────────────────┐
│ CRITICAL RULES - These MUST be copied to README Agent Status │
└─────────────────────────────────────────────────────────────┘

1. ⚠️ ALWAYS start with Phase 0 (Epic Intent Extraction)
   - Re-read epic notes file EVERY time (no exceptions)
   - Extract EXACT QUOTES from epic (not paraphrases)
   - Ground feature in user's original request BEFORE technical work

2. ⚠️ Research MUST be grounded in epic intent (not generic)
   - ONLY research components user explicitly mentioned
   - Do NOT research "how the codebase works generally"
   - Use Epic Intent section to guide what to research

3. ⚠️ READ source code - do NOT guess
   - Use Read tool to view actual code
   - Copy actual method signatures
   - Note actual line numbers
   - View actual data file contents

4. ⚠️ Phase 1.5 audit is MANDATORY GATE
   - Cannot proceed to STAGE_2b without PASSING audit
   - All 4 categories must pass (Component, Pattern, Data, Epic)
   - Evidence required: cite file paths, line numbers, code snippets

5. ⚠️ All research documents go in epic's research/ folder
   - NOT in feature folder
   - Shared across all features
   - Named: {FEATURE_NAME}_DISCOVERY.md

6. ⚠️ Update feature README.md Agent Status after EACH phase
```

---

## Critical Decisions Summary

**Research Phase has 1 major decision point:**

### Decision Point 1: Phase 1.5 - Research Completeness Audit (GO/NO-GO)
**Question:** Is research thorough enough to proceed to spec creation?
- **Evidence required:** Can cite exact files, line numbers, method signatures, data structures
- **If NO (cannot cite specifics):**
  - ❌ STOP at Phase 1.5
  - Continue research (re-read code, search for missing components)
  - Do NOT proceed to STAGE_2b until can cite specific evidence
- **If YES (can cite everything with specifics):**
  - ✅ Proceed to STAGE_2b (Specification Phase)
- **Impact:** Guessing instead of knowing causes wrong specs, which leads to complete rework

---

## Prerequisites Checklist

**Verify BEFORE starting Research Phase:**

□ Stage 1 (Epic Planning) complete - verified in epic EPIC_README.md
□ This feature folder exists: `feature_{N}_{name}/`
□ Feature folder contains:
  - README.md (with Agent Status)
  - spec.md (initial scope from Stage 1)
  - checklist.md (empty or with preliminary items)
  - lessons_learned.md (template)
□ Epic EPIC_README.md Feature Tracking table lists this feature
□ No other feature currently in deep dive phase (work on ONE feature at a time)
□ Epic notes file exists: `feature-updates/KAI-{N}-{epic_name}/{epic_name}_notes.txt`
□ Epic research folder exists: `feature-updates/KAI-{N}-{epic_name}/research/`

**If any prerequisite fails:**
- ❌ STOP - Do NOT proceed with research
- Complete missing prerequisites first
- Document blocker in feature README.md Agent Status

---

## Phase 0: Epic Intent Extraction (MANDATORY FIRST STEP)

**Goal:** Ground this feature in the epic's original request BEFORE any technical work

**⚠️ CRITICAL:** Do NOT skip this phase. Re-reading epic notes prevents misunderstanding user intent.

---

### Step 0.1: Re-Read Epic Request

**Read:** `feature-updates/KAI-{N}-{epic_name}/{epic_name}_notes.txt`

**Why this matters:**
- Even if you "remember" the epic from Stage 1, read it AGAIN
- Context window limits may have caused you to forget details
- User's exact words matter (not your interpretation)

**Do NOT skip this step.**

---

### Step 0.2: Extract User Intent for THIS Feature

**Answer these questions using EXACT QUOTES from epic notes:**

```markdown
## Epic Intent Analysis (Internal - for agent)

**1. What problem is THIS feature solving?**

Quote from epic notes: "{paste exact text from epic, cite line number}"

My interpretation: "{paraphrase in your own words}"

---

**2. What did the user EXPLICITLY request for this feature?**

Explicit request 1: "{quote from epic, cite line}"
Explicit request 2: "{quote from epic, cite line}"
Explicit request 3: "{quote from epic, cite line}"

(List ALL explicit requests related to this feature)

---

**3. What constraints did the user mention?**

Constraint 1: "{quote from epic, cite line}"
Constraint 2: "{quote from epic, cite line}"

(Examples: "must use existing CSV format", "don't change PlayerManager interface", "keep it simple")

---

**4. What is OUT of scope? (user said "not now" or "future")**

Out of scope 1: "{quote from epic, cite line}"
Out of scope 2: "{quote from epic, cite line}"

(Examples: "not including historical data", "automatic updates can come later")

---

**5. What is the user trying to ACCOMPLISH? (end goal)**

User's goal: "{quote from epic describing what user wants to achieve}"

(Example: "make better draft decisions", "reduce manual data entry", "improve recommendation accuracy")

---

**6. What technical components did the user mention?**

Component 1: "{term from epic}" - Line {N}
Component 2: "{term from epic}" - Line {N}
Data source: "{term from epic}" - Line {N}

(Examples: "PlayerManager", "CSV file", "scoring algorithm", "ADP data")
```

**CRITICAL RULE:**

- Use EXACT QUOTES (copy-paste from epic notes)
- Cite line numbers for every quote
- If user didn't mention something → it's an ASSUMPTION (add to checklist later)

---

### Step 0.3: Create "Epic Intent" Section in spec.md

**Update `feature_{N}_{name}/spec.md`:**

Add this as the **FIRST section** (before any technical details):

```markdown
# Feature {N}: {Descriptive Name}

---

## Epic Intent (User's Original Request)

**⚠️ CRITICAL:** All requirements below MUST trace back to this section.

**Problem This Feature Solves:**

"{Quote from epic notes describing the problem}"
(Source: Epic notes line {N})

---

**User's Explicit Requests:**

1. "{Quote 1 from epic notes}"
   (Source: Epic notes line {N})

2. "{Quote 2 from epic notes}"
   (Source: Epic notes line {N})

3. "{Quote 3 from epic notes}"
   (Source: Epic notes line {N})

---

**User's Constraints:**

- "{Quote from epic notes}"
  (Source: Epic notes line {N})

- "{Quote from epic notes}"
  (Source: Epic notes line {N})

---

**Out of Scope (User Explicitly Excluded):**

- "{What user said is NOT included}"
  (Source: Epic notes line {N})

---

**User's End Goal:**

"{Quote from epic notes describing what user wants to achieve}"
(Source: Epic notes line {N})

---

**Technical Components Mentioned by User:**

- **{Component 1}** (Epic notes line {N})
- **{Component 2}** (Epic notes line {N})
- **{Data source}** (Epic notes line {N})

---

**Agent Verification:**

□ Re-read epic notes file: {date/time}
□ Extracted exact quotes (not paraphrases)
□ Cited line numbers for all quotes
□ Identified out-of-scope items
□ Understand user's goal (not just technical implementation)

---

{Rest of spec.md sections will be added in STAGE_2b}
```

---

### Step 0.4: Verify Epic Alignment

**BEFORE proceeding to Phase 1, verify:**

```markdown
## Phase 0 Verification Checklist

□ I have re-read the epic notes file (`{epic_name}_notes.txt`)
□ I have extracted EXACT QUOTES (not paraphrased or interpreted)
□ I have cited line numbers for every quote
□ I understand what the USER wants (not what I think is technically best)
□ I have documented out-of-scope items (what user explicitly excluded)
□ I have added "Epic Intent" section to spec.md as FIRST section
□ I can list what user EXPLICITLY requested (vs what I'm assuming)
```

**If any item unchecked:**
- ❌ Do NOT proceed to Phase 1
- ❌ Complete this phase first
- ❌ Update Agent Status with blocker

**Why this matters:**
- Prevents misunderstanding user intent
- Prevents implementing features user didn't ask for
- Provides traceability (every requirement traces to epic intent)
- Allows early detection of scope mismatch (in STAGE_2b Phase 2.5 alignment check)

---

### Step 0.5: Update Agent Status

```markdown
## Agent Status

**Last Updated:** {YYYY-MM-DD HH:MM}
**Current Phase:** RESEARCH_PHASE
**Current Step:** Phase 0 - Epic Intent Extraction Complete
**Current Guide:** stages/stage_2/phase_0_research.md
**Guide Last Read:** {YYYY-MM-DD HH:MM}
**Critical Rules from Guide:**
- Always start with Phase 0 (Epic Intent Extraction)
- Re-read epic notes EVERY time
- Extract EXACT QUOTES, not paraphrases
- All requirements must trace to epic intent

**Progress:** 1/3 phases complete (Epic Intent Extraction)
**Next Action:** Phase 1 - Targeted Research (using epic intent to guide)
**Blockers:** None

**Epic Notes Re-Read:** {YYYY-MM-DD HH:MM}
**User Explicit Requests Identified:** {N}
```

---

## Phase 1: Targeted Research

**Goal:** Understand THIS feature's technical requirements (NOT the entire epic)

**⚠️ NEW: Use Phase 0 Epic Intent to GUIDE research (not generic research)**

---

### Step 1.1: Read Initial Spec from Stage 1

Read `feature_{N}_{name}/spec.md` created in Stage 1.

**Also re-read "Epic Intent" section** (just added in Phase 0).

**Extract:**
- Feature purpose (what it does)
- Initial scope (what's included)
- Dependencies (what it needs)
- User's explicit requests (from Epic Intent section)
- Technical components mentioned by user (from Epic Intent section)

---

### Step 1.2: Extract Research Questions FROM Epic Request (NOT Generic)

**CRITICAL CHANGE:** Do NOT use generic research questions. Only research what epic/feature explicitly mentions.

**FIRST: Review "Technical Components Mentioned by User" from Epic Intent section**

**For EACH component/term mentioned in epic, create targeted research:**

```markdown
## Research Checklist for Feature {N}

Based on Epic Intent section, I must research:

□ **{Component 1 from epic}** (e.g., "PlayerManager")
  - Action: Find class definition
  - Action: Read relevant methods mentioned in epic
  - Action: Document actual signatures (not assumed)
  - Evidence required: File path, line numbers, code snippets

□ **{Component 2 from epic}** (e.g., "scoring algorithm")
  - Action: Find implementation
  - Action: Understand current algorithm
  - Action: Document how it works today
  - Evidence required: Pseudocode or actual code

□ **{Data source from epic}** (e.g., "ADP data")
  - Action: Search for existing ADP references in codebase
  - Action: Check if ADP already used anywhere
  - Action: Verify what ADP means in this codebase
  - Evidence required: Grep results, file examples

□ **{Similar feature from epic}** (e.g., "injury penalty system")
  - Action: Find existing implementation
  - Action: READ the actual code (not guess at pattern)
  - Action: Document pattern used
  - Evidence required: File path, code structure

□ **{Data format from epic}** (e.g., "CSV format")
  - Action: Find example CSV files
  - Action: READ actual file contents
  - Action: Document exact format (columns, types, examples)
  - Evidence required: File path, first 5 lines of actual file
```

**Anti-Pattern Detection:**

❌ "Let me research how scoring works generally"
   ✅ STOP - Epic mentions "PlayerManager scoring" specifically, research THAT

❌ "Let me search for all data sources"
   ✅ STOP - Epic mentions "ADP data" specifically, research THAT

❌ "Let me understand the entire codebase architecture"
   ✅ STOP - Only research components mentioned in epic intent

**Key Principle:** If epic/feature doesn't mention it, DON'T research it yet. You'll discover additional needs later, but start grounded in user's words.

---

### Step 1.3: Conduct Targeted Searches

**For EACH item in research checklist, execute searches:**

**Example: Component mentioned is "PlayerManager"**

```bash
# Find class definition
grep -r "class PlayerManager" --include="*.py"

# Find it, now READ the file
# Use Read tool to read league_helper/util/PlayerManager.py

# Find method mentioned in epic (e.g., "scoring")
grep -r "def.*score" league_helper/util/PlayerManager.py

# READ that method
# Use Read tool to read specific line range
```

**Example: Data source mentioned is "ADP data"**

```bash
# Search for existing ADP references
grep -r "adp" --include="*.py" -i

# Search for ADP in data files
find data/ -name "*adp*" -o -name "*draft*"

# If found, READ actual file
# Use Read tool to see actual format
```

**Example: User mentioned "similar to injury penalty system"**

```bash
# Find injury-related code
grep -r "injury" --include="*.py" -i

# READ the implementation
# Use Read tool to understand the pattern
```

**CRITICAL RULE: READ, don't guess**

- Use Read tool to view actual code
- Copy actual method signatures
- Note actual line numbers
- View actual data file contents

---

### Step 1.4: Document Findings in Research Folder

Create `epic/research/{FEATURE_NAME}_DISCOVERY.md`:

```markdown
# Feature {N}: {Name} - Discovery Findings

**Research Date:** {YYYY-MM-DD}
**Researcher:** Agent
**Grounded In:** Epic Intent (user's explicit requests)

---

## Epic Intent Summary

**User requested:** "{brief summary from Epic Intent section}"

**Components user mentioned:**
- {Component 1}
- {Component 2}
- {Data source}

**This research focused on user-mentioned components ONLY.**

---

## Components Identified

### Component 1: {Name from Epic}

**User mentioned:** "{quote from epic}"

**Found in codebase:**
- File: `league_helper/util/PlayerManager.py`
- Class definition: Line 45
- Relevant method: `calculate_total_score()` at line 125

**Method signature (actual from source):**
```python
def calculate_total_score(self, player: FantasyPlayer, config: ConfigManager) -> float:
    """Calculate total score including all multipliers."""
    # ... (copied from actual source)
```

**How it works today:**
- Loads base score from player.projected_points
- Applies multipliers: injury, matchup, team_quality
- Returns final score

**Relevance to this feature:**
- User wants to add new data source to this scoring
- Will need to add new multiplier to this method

---

### Data Source: {Name from Epic}

**User mentioned:** "{quote from epic}"

**Found in codebase:**
- Searched for: `grep -r "adp" --include="*.py" -i`
- Result: NO existing ADP references found
- This is NEW data source (not currently in codebase)

**Data format research:**
- User mentioned: "CSV file"
- Need to determine exact format (add to checklist as question)

---

### Similar Feature: {Name from Epic}

**User mentioned:** "{quote from epic - e.g., 'similar to injury penalty'}"

**Found implementation:**
- File: `league_helper/util/PlayerManager.py`
- Lines: 450-480
- Pattern used: Multiplier-based penalty

**Code structure (actual):**
```python
def _calculate_injury_multiplier(self, player: FantasyPlayer) -> float:
    if player.injury_status == "Healthy":
        return 1.0
    elif player.injury_status == "Questionable":
        return 0.95
    elif player.injury_status == "Doubtful":
        return 0.85
    # ...
```

**Pattern to reuse:**
- Method returns float multiplier
- Range: 0.0-1.0 (penalty) or 1.0+ (bonus)
- Applied in calculate_total_score()

**Can follow this pattern for new feature.**

---

## Existing Test Patterns

**Found test pattern in:** `tests/league_helper/util/test_PlayerManager_scoring.py`

**Pattern observed:**
- Uses pytest fixtures for sample players
- Mocks ConfigManager
- Tests each multiplier in isolation
- Integration test with all multipliers

**Can follow this pattern for feature tests.**

---

## Interface Dependencies

**Classes This Feature Will Call:**

1. **ConfigManager.get_multiplier()** (example - actual dependency TBD)
   - Source: `league_helper/util/ConfigManager.py:234`
   - Signature (actual): `def get_adp_multiplier(self, adp: int) -> Tuple[float, int]`
   - Verified: Method exists (checked source code)

**Data Files This Feature Will Read:**

- TBD - Need to ask user about data format (add to checklist)

---

## Edge Cases Identified

**From reading existing code:**

1. Player not in data source → How to handle? (add to checklist)
2. Invalid values in data → Validation needed? (add to checklist)
3. Data file missing → Graceful degradation? (add to checklist)

---

## Research Completeness

**Components researched:**
- ✅ PlayerManager class (READ source code)
- ✅ Existing multiplier pattern (READ injury penalty code)
- ✅ Test patterns (READ existing tests)
- ✅ Data source search (grep for existing references)

**Evidence collected:**
- File paths: {list}
- Line numbers: {list}
- Actual code snippets: {copied above}

**Ready for Phase 1.5 audit.**

---

**Next Steps:**
- Phase 1.5: Verify research completeness
- STAGE_2b Phase 2: Update spec.md with findings
```

---

### Step 1.5: Update Agent Status

```markdown
## Agent Status

**Last Updated:** {YYYY-MM-DD HH:MM}
**Current Phase:** RESEARCH_PHASE
**Current Step:** Phase 1 - Targeted Research Complete
**Current Guide:** stages/stage_2/phase_0_research.md
**Guide Last Read:** {YYYY-MM-DD HH:MM}
**Critical Rules from Guide:**
- Research grounded in epic intent
- READ source code (not guess)
- Evidence required (file paths, line numbers)

**Progress:** 2/3 phases complete (Targeted Research)
**Next Action:** Phase 1.5 - Research Completeness Audit (MANDATORY GATE)
**Blockers:** None

**Components Researched:** {N}
**Research Document:** epic/research/{FEATURE_NAME}_DISCOVERY.md
```

---

## Phase 1.5: Research Completeness Audit (MANDATORY GATE)

**Goal:** Verify research was thorough enough to avoid "should have known" checklist questions

**⚠️ CRITICAL:** This is a MANDATORY GATE. Cannot proceed to STAGE_2b without passing this audit.

**Why this phase exists:**
- Prevents creating checklist questions about things you could have learned from codebase
- Ensures spec is based on actual code (not assumptions)
- Reduces back-and-forth with user about basic technical details

---

### Step 1.5.1: Component Knowledge Verification

**BEFORE creating spec/checklist, answer these verification questions:**

```markdown
## Research Completeness Audit

### Category 1: Component Knowledge

**Question 1.1:** Can I list the EXACT classes/files that will be modified?

❌ BAD: "Probably PlayerManager and maybe ConfigManager"
✅ GOOD: "PlayerManager (league_helper/util/PlayerManager.py:125-180) and ConfigManager (league_helper/util/ConfigManager.py:234)"

**My answer:** {be specific}

**Evidence:** {cite file paths and line numbers}

---

**Question 1.2:** Have I READ the source code for each component?

❌ BAD: "I searched for it but didn't read the actual code"
✅ GOOD: "Yes, used Read tool to view PlayerManager.py lines 1-300, focused on calculate_total_score() method"

**My answer:** {yes/no}

**Evidence:** {cite Read tool calls made, line ranges viewed}

---

**Question 1.3:** Can I cite actual method signatures from source?

❌ BAD: "The method probably takes a player and returns a score"
✅ GOOD: "def calculate_total_score(self, player: FantasyPlayer, config: ConfigManager) -> float (PlayerManager.py:125)"

**My answer:** {list actual signatures}

**Evidence:** {copied from source code}

---

**Verification Result for Category 1:**

□ All questions answered with ✅ GOOD level of detail
□ Evidence provided for each answer

**If any answer is ❌ BAD:**
- STOP - Go back to Phase 1 and research that component
- READ the actual source code
- Collect evidence (file paths, line numbers, code snippets)
```

---

### Step 1.5.2: Pattern Knowledge Verification

```markdown
### Category 2: Pattern Knowledge

**Question 2.1:** Have I searched for similar existing features?

❌ BAD: "I assume there are similar features but didn't search"
✅ GOOD: "Searched for 'injury penalty', found implementation in PlayerManager.py:450-480"

**My answer:** {what did you search for? what did you find?}

**Evidence:** {grep commands used, files found}

---

**Question 2.2:** Have I READ at least one similar feature's implementation?

❌ BAD: "Found it but didn't read the code"
✅ GOOD: "Read PlayerManager.py lines 450-480, documented pattern in research file"

**My answer:** {yes/no}

**Evidence:** {cite Read tool calls, summarize pattern found}

---

**Question 2.3:** Can I describe the existing pattern in detail?

❌ BAD: "It probably uses some kind of multiplier"
✅ GOOD: "Returns float multiplier (0.0-1.0 range), applied in calculate_total_score(), follows method naming pattern _calculate_{type}_multiplier()"

**My answer:** {describe pattern}

**Evidence:** {code snippets showing pattern}

---

**Verification Result for Category 2:**

□ All questions answered with ✅ GOOD level of detail
□ Evidence provided for each answer

**If any answer is ❌ BAD:**
- STOP - Go back to Phase 1 and research similar features
- READ actual implementations
- Document patterns found
```

---

### Step 1.5.3: Data Structure Knowledge Verification

```markdown
### Category 3: Data Structure Knowledge

**Question 3.1:** Have I READ the actual data files (CSV/JSON examples)?

❌ BAD: "I assume CSV has Name, Position columns"
✅ GOOD: "Read data/players.csv, actual columns: Name,Position,Team,Points,ADP (line 1)"

**My answer:** {yes/no - which files did you read?}

**Evidence:** {file paths, actual content from first 5 lines}

---

**Question 3.2:** Can I describe the current format from actual examples?

❌ BAD: "CSV format with player data"
✅ GOOD: "CSV with header row, 5 columns (Name,Position,Team,Points,ADP), example: 'Patrick Mahomes,QB,KC,450.5,5'"

**My answer:** {describe actual format}

**Evidence:** {paste actual file header and sample row}

---

**Question 3.3:** Have I verified field names from source code?

❌ BAD: "I assume player has 'name' field"
✅ GOOD: "FantasyPlayer class (league_helper/util/FantasyPlayer.py:15) has fields: name: str, position: str, team: str, projected_points: float"

**My answer:** {list actual fields from source}

**Evidence:** {cite file and line numbers}

---

**Verification Result for Category 3:**

□ All questions answered with ✅ GOOD level of detail
□ Evidence provided for each answer

**If any answer is ❌ BAD:**
- STOP - Go back to Phase 1 and research data structures
- READ actual files and class definitions
- Document exact formats and field names
```

---

### Step 1.5.4: Epic Request Knowledge Verification

```markdown
### Category 4: Epic Request Knowledge

**Question 4.1:** Have I re-read the epic notes file in THIS phase?

❌ BAD: "I read it in Phase 0, don't need to read again"
✅ GOOD: "Re-read in Phase 0 at {timestamp}, extracted user requests"

**My answer:** {yes/no - when did you read it?}

**Evidence:** {cite Phase 0 completion timestamp}

---

**Question 4.2:** Can I list what the user EXPLICITLY requested?

❌ BAD: "User wants better draft recommendations"
✅ GOOD: "User requested: 1) 'integrate ADP data' (line 15), 2) 'factor ADP into scoring' (line 18), 3) 'use FantasyPros CSV' (line 22)"

**My answer:** {list explicit requests with line citations}

**Evidence:** {quotes from epic notes}

---

**Question 4.3:** Can I identify what's NOT mentioned (assumptions)?

❌ BAD: "Everything seems covered"
✅ GOOD: "User did NOT mention: fuzzy matching, automatic CSV updates, caching. These are agent assumptions (need to add to checklist as questions)"

**My answer:** {list things you're tempted to add but user didn't mention}

**Evidence:** {review epic notes - if not mentioned, it's an assumption}

---

**Verification Result for Category 4:**

□ All questions answered with ✅ GOOD level of detail
□ Evidence provided for each answer

**If any answer is ❌ BAD:**
- STOP - Go back to Phase 0 and re-read epic notes
- Extract explicit requests
- Identify assumptions (things not mentioned)
```

---

### Step 1.5.5: Overall Audit Result

```markdown
## Phase 1.5 Audit Summary

**Category 1 (Component Knowledge):**
□ PASSED - All questions answered with evidence

**Category 2 (Pattern Knowledge):**
□ PASSED - All questions answered with evidence

**Category 3 (Data Structure Knowledge):**
□ PASSED - All questions answered with evidence

**Category 4 (Epic Request Knowledge):**
□ PASSED - All questions answered with evidence

---

**OVERALL RESULT:**

□ ✅ PASSED - All 4 categories passed, ready for STAGE_2b
□ ❌ FAILED - At least one category failed, must return to Phase 1

---

**If PASSED:**
- Proceed to STAGE_2b (Specification Phase)
- Document audit completion in Agent Status

**If FAILED:**
- Return to Phase 1
- Research the specific areas that failed
- Re-run this audit
- Do NOT proceed to STAGE_2b until PASSED

---

**Evidence Summary:**

**Files Read:** {count}
- {list file paths}

**Code Snippets Collected:** {count}
- {list purposes: method signatures, data examples, pattern examples}

**Epic Notes Citations:** {count}
- {list line numbers cited}

**Ready for STAGE_2b:** {YES/NO}
```

---

### Step 1.5.6: Update Agent Status

```markdown
## Agent Status

**Last Updated:** {YYYY-MM-DD HH:MM}
**Current Phase:** RESEARCH_PHASE
**Current Step:** Phase 1.5 - Research Completeness Audit PASSED
**Current Guide:** stages/stage_2/phase_0_research.md
**Guide Last Read:** {YYYY-MM-DD HH:MM}
**Critical Rules from Guide:**
- Phase 1.5 audit is MANDATORY GATE
- Cannot proceed without passing all 4 categories
- Evidence required for all answers

**Progress:** 3/3 phases complete (Research Phase COMPLETE)
**Next Action:** Specification Phase (Update Spec & Checklist with traceability)
**Next Guide:** stages/stage_2/phase_1_specification.md
**Blockers:** None

**Audit Result:** ✅ PASSED (all 4 categories)
**Files Read:** {N}
**Code Snippets Collected:** {N}
```

---

## Completion Criteria

**Research Phase (STAGE_2a) is COMPLETE when ALL of these are true:**

□ **Phase 0 Complete:**
  - Epic notes file re-read
  - "Epic Intent" section created in spec.md (FIRST section)
  - User explicit requests extracted with line citations
  - Out-of-scope items documented

□ **Phase 1 Complete:**
  - Targeted research conducted (grounded in epic intent)
  - Research focused on components mentioned in epic
  - Findings documented in epic/research/{FEATURE_NAME}_DISCOVERY.md
  - Evidence collected (file paths, line numbers, code snippets)

□ **Phase 1.5 Complete:**
  - Research completeness audit PASSED
  - All 4 categories verified (Component, Pattern, Data, Epic)
  - Evidence provided for all audit questions
  - Overall audit result: ✅ PASSED

□ **Documentation Complete:**
  - spec.md has Epic Intent section at top
  - research/{FEATURE_NAME}_DISCOVERY.md created with findings
  - Agent Status updated with STAGE_2a completion

□ **Ready for Next Stage:**
  - All research evidence collected and documented
  - Clear understanding of components, patterns, and data structures
  - Epic intent fully extracted and understood
  - Ready to create detailed specification in STAGE_2b

**Exit Condition:** Research Phase is complete when Phase 1.5 audit passes (all 4 categories with evidence), Epic Intent section is in spec.md, research findings are documented, and you're ready to proceed to STAGE_2b for specification creation.

---

## Next Stage

**After completing Research Phase:**

→ **Proceed to:** stages/stage_2/phase_1_specification.md

**What happens in STAGE_2b:**
- Phase 2: Update Spec & Checklist (with requirement traceability)
- Phase 2.5: Spec-to-Epic Alignment Check (MANDATORY GATE)

**Prerequisites for STAGE_2b:**
- Phase 1.5 audit PASSED (from this guide)
- Epic Intent section in spec.md
- Research findings documented

**Time Estimate for STAGE_2b:** 30-45 minutes

---

**END OF STAGE_2a - RESEARCH PHASE GUIDE**
