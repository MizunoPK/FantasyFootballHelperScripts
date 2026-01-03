# STAGE 2b: Specification Phase Guide

**Guide Version:** 1.0
**Created:** 2026-01-02
**Prerequisites:** STAGE_2a complete (Research Phase PASSED)
**Next Stage:** STAGE_2c_refinement_phase_guide.md

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
Specification Phase is where you create detailed technical specifications with requirement traceability (every requirement must have a source), identify open questions for the user, and verify spec alignment with epic intent through a mandatory gate.

**When do you use this guide?**
- STAGE_2a complete (Phase 1.5 Research Audit PASSED)
- Epic Intent section exists in spec.md
- Research findings documented
- Ready to create detailed specifications

**Key Outputs:**
- ✅ Complete spec.md with detailed requirements (all with sources: Epic/Derived)
- ✅ Requirement traceability documented (every requirement traces to source)
- ✅ checklist.md created with valid open questions (user preferences, edge cases)
- ✅ Phase 2.5 Spec-to-Epic Alignment Check PASSED (MANDATORY GATE)
- ✅ Zero scope creep, zero missing requirements
- ✅ Ready for STAGE_2c (Refinement Phase)

**Time Estimate:**
30-45 minutes (2 phases)

**Exit Condition:**
Specification Phase is complete when spec.md has complete requirements with traceability, checklist.md has valid questions, and Phase 2.5 alignment check passes (no scope creep, no missing requirements).

---

## Critical Rules

```
┌─────────────────────────────────────────────────────────────┐
│ CRITICAL RULES - These MUST be copied to README Agent Status │
└─────────────────────────────────────────────────────────────┘

1. ⚠️ Every requirement MUST have traceability
   - Source: Epic Request (cite line from epic notes)
   - Source: User Answer (cite question number)
   - Source: Derived Requirement (explain derivation)
   - If source is "assumption" → STOP, add to checklist as question

2. ⚠️ NEVER MAKE ASSUMPTIONS - CONFIRM WITH USER FIRST
   - Do NOT assume requirements, methodologies, or behavior
   - Do NOT write specs based on "what makes sense" or "best practices"
   - ASK USER via checklist.md questions BEFORE asserting in spec.md
   - Only document requirements after explicit user confirmation
   - If uncertain about ANY detail → create question in checklist.md

3. ⚠️ Phase 2.5 alignment check is MANDATORY GATE
   - Verify no scope creep (adding things user didn't ask for)
   - Verify no missing requirements (user requested but not in spec)
   - Cannot proceed to STAGE_2c without passing alignment check

4. ⚠️ Only create questions for GENUINE unknowns
   - Good questions: User preferences, business logic, edge cases
   - Bad questions: Things you should have researched in STAGE_2a
   - If you should have known it from code → NOT a checklist question

5. ⚠️ Update feature README.md Agent Status after EACH phase
```

---

## Critical Decisions Summary

**Specification Phase has 1 major decision point:**

### Decision Point 1: Phase 2.5 - Spec-to-Epic Alignment Check (GO/NO-GO)
**Question:** Does spec match user's original request (no scope creep, no missing requirements)?
- **Check for:**
  - Scope creep: Adding things user didn't ask for
  - Missing requirements: User asked but not in spec
  - Invalid sources: Requirements with "assumption" as source
- **If NO (scope creep OR missing requirements found):**
  - ❌ STOP at Phase 2.5
  - Remove scope creep items (move to questions.md)
  - Add missing requirements from epic intent
  - Fix invalid source traceability
  - Re-run Phase 2.5 alignment check
- **If YES (perfect alignment, all requirements traced):**
  - ✅ Proceed to STAGE_2c (Refinement Phase)
- **Impact:** Prevents implementing features user didn't ask for or missing what they did ask for

---

## Prerequisites Checklist

**Verify BEFORE starting Specification Phase:**

□ STAGE_2a complete (Research Phase)
□ Phase 1.5 Research Audit PASSED (all 4 categories)
□ Epic Intent section exists in spec.md (created in Phase 0)
□ Research findings documented in epic/research/{FEATURE_NAME}_DISCOVERY.md
□ Evidence collected (file paths, line numbers, code snippets)
□ Feature README.md Agent Status shows STAGE_2a complete

**If any prerequisite fails:**
- ❌ STOP - Do NOT proceed with specification
- Complete missing prerequisites first
- Document blocker in feature README.md Agent Status

---

## Phase 2: Update Spec & Checklist

**Goal:** Document findings in spec.md and create checklist.md with open questions

**⚠️ NEW: Every requirement must have traceability (source)**

---

### Step 2.1: Update spec.md with Technical Details (WITH TRACEABILITY)

**CRITICAL CHANGE:** Every requirement must cite its source.

**Valid sources:**
1. **Epic Request** - User explicitly asked for this (cite line from epic notes)
2. **User Answer** - User answered checklist question (cite question number)
3. **Derived Requirement** - Logically required to fulfill user request (explain derivation)

**If source is "assumption":**
- ❌ Remove from spec.md immediately
- ❌ Add to checklist.md as a QUESTION
- ❌ Get user answer first, THEN add to spec with "Source: User Answer to Q{N}"

---

**Add/expand these sections in `spec.md`:**

#### Components Affected

```markdown
## Components Affected

**Classes to Modify:**

1. **PlayerManager** (`league_helper/util/PlayerManager.py`)
   - **Source:** Epic notes line 15: "integrate into PlayerManager scoring"
   - **Traceability:** Direct user request
   - **Changes:**
     - `calculate_total_score()` method (line 125) - Add new multiplier calculation
     - `load_players()` method (line 89) - Load new data source
     - New method: `_calculate_adp_multiplier()` - Encapsulate logic

2. **ConfigManager** (`league_helper/util/ConfigManager.py`)
   - **Source:** Derived from user request (need configuration for multiplier ranges)
   - **Traceability:** User requested ADP integration (epic line 15), config is necessary implementation detail
   - **Changes:**
     - Use existing `get_multiplier()` pattern (line 234)
     - May need new config keys (add to checklist as question)

3. **FantasyPlayer** (`league_helper/util/FantasyPlayer.py`)
   - **Source:** Derived from user request (need to store ADP data per player)
   - **Traceability:** User requested ADP integration, storing ADP value is logically required
   - **Changes:**
     - Add field: `adp_value: Optional[int]` - Store ranking
     - Add field: `adp_multiplier: float` - Store calculated multiplier

**New Files to Create:**

- `data/adp_rankings.csv`
  - **Source:** ⚠️ ASSUMPTION - User mentioned "ADP data" but not format
  - **Traceability:** Need to ask user (add to checklist as Question)
  - **Action:** Move to checklist.md, ask user about data format

- `tests/league_helper/util/test_PlayerManager_adp.py`
  - **Source:** Derived requirement (tests are required for all new features)
  - **Traceability:** Standard practice, not user-requested but necessary
```

#### Requirements (WITH SOURCES)

```markdown
## Requirements

### Requirement 1: Load ADP data

**Description:** Load ADP (Average Draft Position) data from external source

**Source:** Epic notes line 15: "integrate ADP data from FantasyPros"
**Traceability:** Direct user request

**Implementation:**
- Load data during player initialization
- Match players by name+position (TBD - add to checklist)

---

### Requirement 2: Calculate ADP multiplier

**Description:** Convert ADP value to multiplier for scoring

**Source:** Epic notes line 18: "factor ADP into draft recommendations"
**Traceability:** Direct user request

**Implementation:**
- Use ConfigManager for multiplier ranges
- Apply multiplier in calculate_total_score()

---

### Requirement 3: Handle missing player data

**Description:** Handle case where player not in ADP data

**Source:** Derived requirement
**Traceability:** Not all players may have ADP data (edge case), need to handle gracefully

**Implementation:**
- Use neutral multiplier (1.0) if player not found (TBD - add to checklist as question)
- Log warning for missing players

---

**Requirements Summary:**

- ✅ Requirement 1: Direct user request (epic line 15)
- ✅ Requirement 2: Direct user request (epic line 18)
- ✅ Requirement 3: Derived (logically necessary for edge cases)

**Total Requirements:** 3 (all traced to sources)
```

#### Data Structures

```markdown
## Data Structures

### Input Data Format

**Format:** CSV file with ADP rankings

**Source:** ⚠️ ASSUMPTION - User mentioned "ADP data" but not specific format
**Action:** Add to checklist as Question 1: "What format is the ADP data in? CSV, JSON, or API?"

**Assumed structure (pending user confirmation):**
```csv
Name,Position,ADP
Patrick Mahomes,QB,5
Christian McCaffrey,RB,1
```

**Field definitions:**
- Name: Player full name (str)
- Position: Player position (str)
- ADP: Average Draft Position ranking (int, 1-500)

---

### Internal Representation

**FantasyPlayer class additions:**

```python
class FantasyPlayer:
    # Existing fields...

    # New fields for this feature:
    adp_value: Optional[int]  # 1-500, None if not in ADP data
    adp_multiplier: float     # 0.8-1.2 based on ADP (range TBD - add to checklist)
```

**Source:** Derived requirement (need to store ADP data per player)
**Traceability:** User requested ADP integration, storing values is implementation detail

---

### Output

**Updated scoring in PlayerManager:**

```python
total_score = base_score * adp_multiplier * [other existing multipliers...]
```

**Source:** Epic notes line 18: "factor ADP into draft recommendations"
**Traceability:** Direct user request
```

#### Algorithms

```markdown
## Algorithms

### ADP Multiplier Calculation

**Source:** Epic notes line 18: "factor ADP into draft recommendations"
**Traceability:** Direct user request (algorithm is implementation detail)

**Pseudocode:**
```
1. Load ADP data from source (format TBD - checklist Q1)
2. For each player:
   a. Match player name+position to ADP data (matching method TBD - checklist Q2)
   b. If match found:
      - Get ADP value (1-500)
      - Calculate multiplier (formula TBD - checklist Q3)
      - Store multiplier in player.adp_multiplier
   c. If NO match found:
      - Use default multiplier (value TBD - checklist Q4)
3. In calculate_total_score():
   total_score = base_score * adp_multiplier * [other multipliers...]
```

**TBD items (need user answers):**
- Data source format (Question 1)
- Player matching method (Question 2)
- Multiplier calculation formula (Question 3)
- Default multiplier for missing players (Question 4)

---

### Edge Case Handling

**Source:** Derived requirements (edge cases not mentioned in epic, but necessary)

1. **Player not in ADP data**
   - Action: Use default multiplier (value TBD - add to checklist)
   - Source: Derived (edge case handling)

2. **Invalid ADP value (<1 or >500)**
   - Action: Log warning, use default multiplier
   - Source: Derived (data validation)

3. **Multiple players with same name**
   - Action: Match on Name+Position (method TBD - add to checklist)
   - Source: Derived (disambiguation logic)

4. **ADP data file missing or corrupt**
   - Action: Graceful degradation - all multipliers = 1.0 (TBD - add to checklist)
   - Source: Derived (error handling)
```

#### Dependencies

```markdown
## Dependencies

**This feature depends on:**

- **ConfigManager.get_adp_multiplier() method**
  - Source: Derived (need config for multiplier ranges)
  - Status: Need to verify if method exists (Phase 1 research found similar get_multiplier())
  - May need to create new method (add to implementation items)

- **CSV utilities (utils/csv_utils.py)**
  - Source: Derived (need to read CSV data)
  - Status: Exists in codebase (verified in Phase 1)

- **FantasyPlayer class structure**
  - Source: Derived (need to add new fields)
  - Status: Can add fields (verified in Phase 1, class is extensible)

**This feature blocks:**

- Feature 4: Recommendation Engine Updates
  - Source: Epic structure (Feature 4 depends on Features 1-3)
  - Will use ADP multipliers from this feature

**This feature is independent of:**

- Feature 2: Injury Risk Assessment (parallel)
- Feature 3: Schedule Strength Analysis (parallel)
```

---

### Step 2.2: Create checklist.md with Open Questions

**Populate `checklist.md` with questions identified during spec creation:**

**CRITICAL:** Only add questions for actual unknowns (not things you should have researched).

```markdown
# Feature {N}: {Name} - Planning Checklist

**Purpose:** Track open questions and decisions for this feature

**Instructions:**
- [ ] = Open question (needs user answer)
- [x] = Resolved (answer documented below)

---

## Open Questions

### Question 1: ADP Data Source Format

- [ ] What format is the ADP data in?
  - Option A: CSV file (user provides manually)
  - Option B: JSON API (fetch automatically)
  - Option C: Web scraping (FantasyPros website)

**Context:** User mentioned "ADP data" but didn't specify format. Need to know format to implement loader.

**Epic reference:** Line 15: "integrate ADP data from FantasyPros" (no format specified)

**Recommendation:** Option A (CSV) - Simplest, user controls data, no API dependencies

**Why this is a question:** User didn't specify format in epic notes, this is a genuine unknown (not something we could have researched)

---

### Question 2: Player Name Matching Method

- [ ] How should we match players between CSV and existing data?
  - Option A: Exact match on Name+Position (strict)
  - Option B: Fuzzy matching (handle typos, "P. Mahomes" vs "Patrick Mahomes")
  - Option C: Match on unique ID (requires ID in both datasets)

**Context:** Player names may differ slightly between data sources.

**Epic reference:** Not mentioned in epic

**Recommendation:** Option A (strict matching) unless user needs fuzzy matching

**Why this is a question:** User didn't specify matching logic, could go either way

---

### Question 3: ADP Multiplier Calculation Formula

- [ ] How should ADP value translate to multiplier?
  - Option A: Linear (ADP 1-100 = 1.2x, 101-200 = 1.1x, 201+ = 1.0x)
  - Option B: Exponential (higher impact for top picks)
  - Option C: Config-based ranges (user defines in config file)

**Context:** Need to convert ADP ranking (1-500) to multiplier (0.8-1.2 range estimate).

**Epic reference:** Line 18: "factor ADP into draft recommendations" (no formula specified)

**Recommendation:** Option C (config-based) - Most flexible

**Why this is a question:** User said "factor ADP" but didn't specify how much impact

---

### Question 4: Default Multiplier for Missing Players

- [ ] What happens if player NOT in ADP data?
  - Option A: Use multiplier = 1.0 (neutral, no bonus/penalty)
  - Option B: Use multiplier = 0.9 (slight penalty for unknown)
  - Option C: Exclude from draft recommendations entirely

**Context:** Rookies or obscure players might not have ADP data.

**Epic reference:** Not mentioned in epic

**Recommendation:** Option A (neutral 1.0) - Don't penalize players for missing data

**Why this is a question:** Edge case not covered in epic, need user preference

---

### Question 5: CSV Column Names

- [ ] What are the exact column names in the FantasyPros CSV?
  - Need to know: Player name column, position column, ADP column
  - Ask user to provide column names or sample CSV

**Context:** Need exact column names to parse CSV correctly.

**Epic reference:** Line 15 mentions "FantasyPros" but not CSV structure

**Recommendation:** Ask user for sample CSV or column names

**Why this is a question:** Can't assume CSV structure without seeing actual file

---

## Resolved Questions

{Will populate as questions are answered}

---

## Additional Scope Discovered

{Will document if deep dive reveals new work not in original scope}
```

**Anti-Pattern Detection:**

❌ "Question: Which class should we modify?"
   ✅ STOP - You should have researched this in STAGE_2a (not a checklist question)

❌ "Question: What's the current scoring algorithm?"
   ✅ STOP - You should have READ the code in STAGE_2a (not a checklist question)

❌ "Question: Does PlayerManager have a calculate_score method?"
   ✅ STOP - You should have verified this in Phase 1.5 audit (not a checklist question)

**Good questions:**
- ✅ User preferences (fuzzy vs strict matching)
- ✅ Business logic not specified in epic (multiplier formula)
- ✅ Edge case handling not mentioned (missing player behavior)
- ✅ External data formats (CSV column names)

---

### Step 2.3: Update Agent Status

```markdown
## Agent Status

**Last Updated:** {YYYY-MM-DD HH:MM}
**Current Phase:** SPECIFICATION_PHASE
**Current Step:** Phase 2 - Spec & Checklist Updated (with traceability)
**Current Guide:** STAGE_2b_specification_phase_guide.md
**Guide Last Read:** {YYYY-MM-DD HH:MM}
**Critical Rules from Guide:**
- Every requirement must have source (Epic/User Answer/Derived)
- If source is "assumption" → remove, add to checklist
- Phase 2.5 alignment check is next (MANDATORY GATE)

**Progress:** 1/2 phases complete (Spec & Checklist)
**Next Action:** Phase 2.5 - Spec-to-Epic Alignment Check (MANDATORY GATE)
**Blockers:** None

**Requirements Added:** {N} (all with sources)
**Checklist Questions:** {M} (all valid unknowns)
**Assumptions Moved to Checklist:** {K}
```

---

## Phase 2.5: Spec-to-Epic Alignment Check (MANDATORY GATE)

**Goal:** Verify spec matches user intent (no scope creep, no missing requirements)

**⚠️ CRITICAL:** This is a MANDATORY GATE. Cannot proceed to STAGE_2c without passing this check.

**Why this phase exists:**
- Prevents scope creep (adding features user didn't ask for)
- Prevents missing requirements (user asked but not in spec)
- Ensures spec traces back to epic intent
- Catches misalignment BEFORE asking user questions

---

### Step 2.5.1: Re-Read Epic Intent Section

**Read the "Epic Intent" section** at the top of spec.md (created in STAGE_2a Phase 0).

**Refresh your memory:**
- What did the user EXPLICITLY request?
- What constraints did user mention?
- What's out of scope?
- What's the user's end goal?

---

### Step 2.5.2: Verify Every Requirement Has Valid Source

**Review "Requirements" section of spec.md:**

```markdown
## Requirement Source Verification

For EACH requirement, verify source type:

**Requirement 1: {Name}**
- Source: {Epic Request / User Answer / Derived}
- Valid? ✅ / ❌

**Requirement 2: {Name}**
- Source: {Epic Request / User Answer / Derived}
- Valid? ✅ / ❌

...

**If source is "Epic Request":**
□ Citation exists (epic notes line number)
□ Quote is accurate
□ Requirement matches user's words

**If source is "User Answer":**
□ Wait - we haven't asked questions yet (STAGE_2c comes later)
□ Source cannot be "User Answer" at this stage
□ Change to "⚠️ ASSUMPTION - add to checklist"

**If source is "Derived":**
□ Derivation explanation exists
□ Logically necessary to fulfill user request
□ Not "nice to have" or "best practice"

**If source is "⚠️ ASSUMPTION":**
□ ❌ INVALID - Remove from spec
□ Add to checklist.md as question
□ Get user answer in STAGE_2c
```

---

### Step 2.5.3: Check for Scope Creep

**Scope creep detection:**

```markdown
## Scope Creep Check

**Review spec.md and ask for EACH requirement:**

1. **Did the user ask for this?**
   - Check Epic Intent section
   - If not mentioned → SCOPE CREEP candidate

2. **Is this "nice to have" or NECESSARY?**
   - Necessary: Logically required to fulfill user request
   - Nice to have: "Best practice" but user didn't ask for it

3. **Am I solving a different problem than user described?**
   - User's problem: "{quote from Epic Intent}"
   - This requirement solves: "{what problem?}"
   - Match? ✅ / ❌

**Scope Creep Candidates Found:**

□ Requirement {N}: {Name}
  - Why flagged: User didn't mention this
  - Action: Remove from spec, add to checklist as "Should we also...?"
  - User approval needed: YES

□ Requirement {N}: {Name}
  - Why flagged: "Best practice" but not user-requested
  - Action: Remove from spec or move to "nice to have" checklist section
  - User approval needed: YES

**If scope creep found:**
- ❌ Remove from spec.md immediately
- ❌ Add to checklist.md: "User requested X, should we also do Y?"
- ❌ Get user approval in STAGE_2c before adding back

**If no scope creep:**
- ✅ All requirements trace to user requests or logical derivations
```

---

### Step 2.5.4: Check for Missing Requirements

**Missing requirements detection:**

```markdown
## Missing Requirements Check

**Re-read Epic Intent section:**

User's explicit requests:
1. "{Quote 1 from epic}"
2. "{Quote 2 from epic}"
3. "{Quote 3 from epic}"

**For EACH explicit request, verify it's in spec:**

□ Request 1: "{quote}"
  - Found in spec? ✅ / ❌
  - If ❌: Add to spec as Requirement {N}

□ Request 2: "{quote}"
  - Found in spec? ✅ / ❌
  - If ❌: Add to spec as Requirement {N}

□ Request 3: "{quote}"
  - Found in spec? ✅ / ❌
  - If ❌: Add to spec as Requirement {N}

**Missing Requirements Found:**

□ Epic line {N}: "{quote}"
  - Why missed: {reason}
  - Action: Add to spec.md as Requirement {N}
  - Source: Epic notes line {N}

**If missing requirements found:**
- ❌ Add to spec.md immediately
- ❌ Document source (epic notes line number)
- ❌ Verify no other user requests were missed
```

---

### Step 2.5.5: Overall Alignment Result

```markdown
## Phase 2.5 Alignment Summary

**Requirement Source Verification:**
□ All requirements have valid sources (Epic/Derived)
□ No requirements with "User Answer" source (STAGE_2c not started yet)
□ No requirements with "⚠️ ASSUMPTION" source

**Scope Creep Check:**
□ No scope creep detected
□ OR: Scope creep found and removed (moved to checklist)

**Missing Requirements Check:**
□ No missing requirements detected
□ OR: Missing requirements found and added to spec

---

**OVERALL RESULT:**

□ ✅ PASSED - Spec aligns with epic intent, ready for STAGE_2c
□ ❌ FAILED - Issues found, must resolve before STAGE_2c

---

**If PASSED:**
- Proceed to STAGE_2c (Refinement Phase)
- Document alignment check completion in Agent Status

**If FAILED:**
- Resolve issues (remove scope creep, add missing requirements)
- Re-run this alignment check
- Do NOT proceed to STAGE_2c until PASSED

---

**Alignment Evidence:**

**Requirements aligned with epic:** {N / M} ({N} out of {M} total requirements)
**Scope creep removed:** {K} requirements
**Missing requirements added:** {L} requirements
**Final requirement count:** {N} (all traced to sources)

**Ready for STAGE_2c:** {YES/NO}
```

---

### Step 2.5.6: Update Agent Status

```markdown
## Agent Status

**Last Updated:** {YYYY-MM-DD HH:MM}
**Current Phase:** SPECIFICATION_PHASE
**Current Step:** Phase 2.5 - Spec-to-Epic Alignment Check PASSED
**Current Guide:** STAGE_2b_specification_phase_guide.md
**Guide Last Read:** {YYYY-MM-DD HH:MM}
**Critical Rules from Guide:**
- Phase 2.5 alignment check is MANDATORY GATE
- Cannot proceed without passing alignment check
- All requirements must trace to epic intent

**Progress:** 2/2 phases complete (Specification Phase COMPLETE)
**Next Action:** STAGE_2c - Refinement Phase (Interactive Question Resolution)
**Blockers:** None

**Alignment Result:** ✅ PASSED
**Scope Creep Removed:** {K} requirements
**Missing Requirements Added:** {L} requirements
**Final Requirements:** {N} (all aligned with epic)
```

---

## Completion Criteria

**Specification Phase (STAGE_2b) is COMPLETE when ALL of these are true:**

□ **Phase 2 Complete:**
  - spec.md updated with complete technical details
  - All requirements have traceability (Epic Request/Derived)
  - Components Affected section complete (with sources)
  - Data Structures section complete
  - Algorithms section complete (with TBD items noted)
  - Dependencies section complete
  - checklist.md created with valid open questions
  - Assumptions removed from spec and moved to checklist

□ **Phase 2.5 Complete:**
  - Spec-to-Epic alignment check PASSED
  - Every requirement has valid source verified
  - No scope creep detected (or removed)
  - No missing requirements (or added to spec)
  - Overall alignment result: ✅ PASSED

□ **Documentation Complete:**
  - spec.md has requirement traceability for ALL requirements
  - checklist.md has valid questions (user preferences, edge cases, unknowns)
  - Agent Status updated with STAGE_2b completion

□ **Ready for Next Stage:**
  - All requirements aligned with epic intent
  - Open questions identified (not assumptions)
  - Ready to ask user questions in STAGE_2c

**Exit Condition:** Specification Phase is complete when spec.md has complete requirements with traceability, Phase 2.5 alignment check passes (no scope creep, no missing requirements), and you're ready to proceed to STAGE_2c for question resolution and user approval.

---

## Next Stage

**After completing Specification Phase:**

→ **Proceed to:** STAGE_2c_refinement_phase_guide.md

**What happens in STAGE_2c:**
- Phase 3: Interactive Question Resolution (ONE question at a time)
- Phase 4: Dynamic Scope Adjustment (split if >35 items)
- Phase 5: Cross-Feature Alignment (compare to completed features)
- Phase 6: Acceptance Criteria & User Approval (MANDATORY)

**Prerequisites for STAGE_2c:**
- Phase 2.5 alignment check PASSED (from this guide)
- spec.md has requirements with traceability
- checklist.md has open questions

**Time Estimate for STAGE_2c:** 45-60 minutes

---

**END OF STAGE_2b - SPECIFICATION PHASE GUIDE**
