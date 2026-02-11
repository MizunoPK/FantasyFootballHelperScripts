# Master Validation Loop Protocol

**Version:** 2.0
**Last Updated:** 2026-02-10
**Purpose:** Universal validation loop protocol with master dimensions that apply to ALL validation contexts
**Extends:** This master protocol is extended by scenario-specific validation loop guides

---

## Table of Contents

1. [Overview](#overview)
2. [When to Use This Protocol](#when-to-use-this-protocol)
3. [Core Validation Process](#core-validation-process)
4. [Universal Dimensions (Master - Always Checked)](#universal-dimensions-master---always-checked)
5. [Round-by-Round Execution](#round-by-round-execution)
6. [Documentation Requirements](#documentation-requirements)
7. [Quality Standards](#quality-standards)
8. [Exit Criteria](#exit-criteria)
9. [Common Mistakes](#common-mistakes)
10. [How Scenario-Specific Loops Extend This Master](#how-scenario-specific-loops-extend-this-master)
11. [Templates](#templates)

---

## Overview

**What is the Validation Loop?**
The Validation Loop is a systematic quality assurance process that validates artifacts (specs, plans, code, documentation) through iterative rounds until achieving 3 consecutive clean rounds with zero issues.

**Why use Validation Loops?**
- **Prevents cascading failures**: Catch issues early before propagating downstream
- **Eliminates redundant re-verification**: Check all concerns every round (no need to restart)
- **Guarantees quality**: 3 consecutive clean rounds ensures thorough validation
- **Consistent approach**: Same process across all stages and artifacts

**Key Innovation (from S5 v2):**
- Instead of sequential iterations checking different concerns (S5 v1 had 22 iterations)
- Use validation dimensions checked EVERY round (S5 v2 has 11 dimensions)
- Fix issues immediately, continue validation (no restart from beginning)
- Exit when 3 consecutive rounds have ZERO issues

---

## When to Use This Protocol

**Use Validation Loops for:**
- ✅ Specifications (S2: Feature specs)
- ✅ Plans (S5: Implementation plans)
- ✅ Test strategies (S4: Test plans)
- ✅ Documentation (S3: Epic documentation)
- ✅ Code quality (S7: QC rounds)
- ✅ Cross-artifact alignment (S8: Spec alignment)
- ✅ Epic-level validation (S9: Epic QC)

**Do NOT use for:**
- ❌ Simple checklists (use regular checklist)
- ❌ One-time verification (use standard review)
- ❌ User approval gates (use approval protocol)

**Typical Timing:**
- After creating draft artifact
- Before user approval gates
- After fixing issues (continue validation)

---

## Core Validation Process

### Fundamental Principles

**1. Zero Deferred Issues**
- ALL issues must be fixed immediately (not "later")
- No severity threshold (ALL levels matter: LOW, MEDIUM, HIGH)
- Cannot proceed to next round with open issues
- Fix → Re-validate → Repeat

**2. Three Consecutive Clean Rounds Required**
- Round N: 0 issues found ✅
- Round N+1: 0 issues found ✅
- Round N+2: 0 issues found ✅
- **THEN and ONLY THEN**: Exit validation loop

**3. Fresh Eyes Every Round**
- Re-read ENTIRE artifact each round (not from memory)
- Use different reading patterns/perspectives
- Approach as if seeing for first time
- Don't assume previous rounds were thorough

**4. All Dimensions Every Round**
- Check EVERY dimension EVERY round (master + scenario-specific)
- Cannot skip dimensions
- Cannot batch dimensions
- Systematic top-to-bottom review

### Process Flow

```text
┌─────────────────────────────────────────────────────────────┐
│              VALIDATION LOOP PROCESS FLOW                    │
└─────────────────────────────────────────────────────────────┘

Draft Artifact Created
         │
         ▼
    ┌─────────────────┐
    │   ROUND 1       │
    │                 │
    │ Check ALL       │
    │ Dimensions      │
    │ (Master +       │
    │  Specific)      │
    └─────────────────┘
         │
         ├─→ Issues Found? → FIX ALL IMMEDIATELY → Round 2
         │
         └─→ 0 Issues? → Continue to Round 2
                │
                ▼
           ┌─────────────────┐
           │   ROUND 2       │
           │                 │
           │ Re-read ENTIRE  │
           │ artifact with   │
           │ fresh eyes      │
           │                 │
           │ Check ALL       │
           │ Dimensions      │
           └─────────────────┘
                │
                ├─→ Issues Found? → FIX ALL → RESTART from Round 1
                │                   (Counter resets to 0)
                │
                └─→ 0 Issues? → Counter = 1 → Continue to Round 3
                       │
                       ▼
                  ┌─────────────────┐
                  │   ROUND 3       │
                  │                 │
                  │ Re-read ENTIRE  │
                  │ artifact        │
                  │                 │
                  │ Check ALL       │
                  │ Dimensions      │
                  └─────────────────┘
                       │
                       ├─→ Issues Found? → FIX ALL → RESTART from Round 1
                       │
                       └─→ 0 Issues? → Counter = 2 → Continue to Round 4
                              │
                              ▼
                         ┌─────────────────┐
                         │   ROUND 4       │
                         │                 │
                         │ Re-read ENTIRE  │
                         │ artifact        │
                         │                 │
                         │ Check ALL       │
                         │ Dimensions      │
                         └─────────────────┘
                              │
                              ├─→ Issues Found? → FIX → RESTART Round 1
                              │
                              └─→ 0 Issues? → Counter = 3 ✅
                                     │
                                     ▼
                              ┌──────────────┐
                              │   SUCCESS    │
                              │              │
                              │ 3 consecutive│
                              │ clean rounds │
                              │              │
                              │ EXIT LOOP    │
                              └──────────────┘
```

**Counter Reset Rule:**
- Clean round counter starts at 0
- Each clean round increments counter
- ANY issue found → Counter resets to 0
- Need counter = 3 to exit

**Example:**
- Round 1: 5 issues → Fix all → Counter = 0
- Round 2: 0 issues → Counter = 1
- Round 3: 0 issues → Counter = 2
- Round 4: 1 issue → Fix → **Counter resets to 0**
- Round 5: 0 issues → Counter = 1
- Round 6: 0 issues → Counter = 2
- Round 7: 0 issues → Counter = 3 ✅ **EXIT**

---

## Universal Dimensions (Master - Always Checked)

These 7 dimensions apply to **ALL** validation loops, regardless of context.

### Dimension 1: Empirical Verification ⚡ CRITICAL

**Question:** Is everything claimed/referenced verified against actual reality (not assumptions)?

**Core Principle:** "Never assume - always verify from source of truth"

**Why This is Dimension 1:**
- If working with made-up facts, nothing else matters
- Must establish reality BEFORE checking completeness/consistency
- Catches issues earlier (before propagating downstream)
- Prevents cascading failures from wrong assumptions

**Checklist:**

**Code References:**
- [ ] All class names verified from source code (use grep/Read, not memory)
- [ ] All method/function names verified from source code
- [ ] All function signatures copy-pasted from actual code (not paraphrased)
- [ ] All return types verified from source code
- [ ] All parameter types verified from source code (including optional/default values)
- [ ] All exception types verified from source code

**File System:**
- [ ] All file paths verified to exist (use ls/Read, not assumption)
- [ ] All directory paths verified to exist
- [ ] All referenced data files verified to exist (actual ls output)
- [ ] All import paths verified to work (test imports)

**Configuration:**
- [ ] All config keys verified from actual config files (exact key names)
- [ ] All config value types verified (string vs int vs bool)
- [ ] All environment variables verified from actual environment

**External Dependencies:**
- [ ] All library imports verified from requirements.txt or actual imports
- [ ] All version numbers verified from actual installed versions
- [ ] All API endpoints verified from actual API (if applicable)

**Data Structures:**
- [ ] All CSV column names verified from actual files (read header row)
- [ ] All JSON keys verified from actual files (read actual JSON)
- [ ] All database table names verified from schema (if applicable)
- [ ] All field names verified from source of truth

**Evidence Documentation:**
- [ ] Every verified item has source location (file:line)
- [ ] Copy-paste of actual code provided (not summary or paraphrase)
- [ ] Verification method documented (Read tool / grep / ls command)
- [ ] Verification timestamp included
- [ ] No "assumption" or "probably" as verification method

**Common Violations:**

❌ **WRONG - Made-up function signature:**
```markdown
Task 3: Call ConfigManager.get_adp_multiplier(adp: int) -> float
Source: Assumption based on spec description
```

✅ **CORRECT - Verified from source:**
```markdown
Task 3: Call ConfigManager.get_adp_multiplier(adp: int) -> Tuple[float, int]
Source: Verified from league_helper/util/ConfigManager.py:234
Verification method: Read tool
Verification timestamp: 2026-02-10 14:30

Actual signature:
    def get_adp_multiplier(self, adp: int) -> Tuple[float, int]:
        """
        Calculate ADP multiplier based on ADP ranking.

        Args:
            adp (int): ADP ranking (1-500)

        Returns:
            Tuple[float, int]: (multiplier, rating)
        """
```

❌ **WRONG - Made-up file path:**
```markdown
Load data from: data/adp_rankings.csv
Verification: Not checked (assumed from spec)
```

✅ **CORRECT - Verified path:**
```markdown
Load data from: data/rankings/adp.csv
Verification method: ls command
Verification timestamp: 2026-02-10 14:32

Command: ls -la data/rankings/adp.csv
Output: -rw-r--r-- 1 user user 45832 Feb 10 10:15 data/rankings/adp.csv

Note: Spec mentioned "adp_rankings.csv" but actual file is in rankings/ subdirectory
```

❌ **WRONG - Assumed class name:**
```markdown
Integration: PlayerDataManager.load_players()
Source: Mentioned in epic request as "player data manager"
```

✅ **CORRECT - Verified class name:**
```markdown
Integration: PlayerManager.load_players()
Source: Verified from league_helper/util/PlayerManager.py:23
Verification method: grep command

Command: grep -r "class Player.*Manager" --include="*.py"
Output: league_helper/util/PlayerManager.py:23:class PlayerManager:

Note: Epic request used phrase "player data manager" but actual class is PlayerManager (no "Data")
```

**Verification Evidence Template:**
```markdown
## Dimension 1: Empirical Verification

**Item:** [Function/Class/File/Config being verified]
**Claimed in artifact:** [What the spec/plan/doc says]
**Verification method:** [Read tool / grep / ls / import test]
**Verification timestamp:** [YYYY-MM-DD HH:MM]
**Source location:** [file:line]
**Actual reality:** [Copy-paste from actual source]
**Match status:** ✅ MATCH / ❌ MISMATCH (updated artifact)
```

---

### Dimension 2: Completeness

**Question:** Are all required sections/elements present per template/checklist?

**Checklist:**

**Structural Completeness:**
- [ ] All mandatory sections present (per template)
- [ ] No "TBD" or "TODO" placeholders remaining
- [ ] No "..." or "etc." without specifics
- [ ] All cross-references point to existing content

**Content Completeness:**
- [ ] All requirements/tasks enumerated (not "and others")
- [ ] All edge cases identified (not "handle errors")
- [ ] All dependencies listed (not "various dependencies")
- [ ] All acceptance criteria defined (not "works correctly")

**Example Completeness:**
- [ ] All examples include expected input AND output
- [ ] All code examples are syntactically complete
- [ ] All examples reference real code/data (verified in Dimension 1)

**Cross-Reference Completeness:**
- [ ] All references to other documents include section/line numbers
- [ ] All "see X" references exist and are correct
- [ ] All links/paths are valid (verified in Dimension 1)

**Common Violations:**

❌ **WRONG - Incomplete requirements:**
```markdown
## Requirements
1. Load player data
2. Calculate scores
3. Handle errors
... (additional requirements TBD)
```

✅ **CORRECT - Complete enumeration:**
```markdown
## Requirements
1. Load player data from CSV
2. Validate player data structure
3. Calculate ADP-based scores
4. Apply position-specific adjustments
5. Handle missing data gracefully
6. Handle invalid ADP values (< 1 or > 500)
7. Handle file not found errors
8. Log all operations

(8 total requirements - all enumerated)
```

---

### Dimension 3: Internal Consistency

**Question:** Are there any contradictions or conflicts within this artifact?

**Checklist:**

**Statement Consistency:**
- [ ] No contradictory requirements ("must use X" vs "must use Y")
- [ ] No contradictory approaches (sync in one place, async in another)
- [ ] No contradictory data types (string vs int for same field)

**Terminology Consistency:**
- [ ] Same concept uses same term throughout (not "player_count" then "num_players")
- [ ] Abbreviations defined and used consistently
- [ ] Field/variable names consistent throughout

**Example Consistency:**
- [ ] Examples match specifications
- [ ] Code examples use same variable names as spec
- [ ] Sample data matches described structure

**Dependency Consistency:**
- [ ] No circular dependencies (A depends on B, B depends on A)
- [ ] Execution order is possible (no impossible orderings)
- [ ] Prerequisites are consistent with workflow

**Common Violations:**

❌ **WRONG - Contradictory approach:**
```markdown
## Section 1: Data Loading
Use synchronous file reading for predictable timing.

## Section 4: Performance
Use async file reading for better performance.
```

✅ **CORRECT - Consistent approach:**
```markdown
## Section 1: Data Loading
Use synchronous file reading for predictable timing and simpler error handling.

## Section 4: Performance
Optimize synchronous reading with buffering and batch processing.
```

❌ **WRONG - Inconsistent terminology:**
```markdown
## Section 2
Load player_count from config.

## Section 5
Validate that num_players is positive.
```

✅ **CORRECT - Consistent terminology:**
```markdown
## Section 2
Load player_count from config.

## Section 5
Validate that player_count is positive.
```

---

### Dimension 4: Traceability

**Question:** Can every decision/requirement be traced to an authoritative source?

**Checklist:**

**Requirement Traceability:**
- [ ] All requirements cite source (Epic Request / User Answer / Derived)
- [ ] No requirements with "assumption" as source
- [ ] Derived requirements explain derivation logic clearly
- [ ] User answers include question context and date

**Decision Traceability:**
- [ ] All design decisions cite rationale
- [ ] All "why" questions answered with source
- [ ] All trade-offs documented with reasoning
- [ ] All deviations from normal patterns explained

**Source Citation Format:**
- [ ] Epic references include line numbers (e.g., "Epic request line 45")
- [ ] User answer references include question number and date
- [ ] Derived requirements show derivation chain
- [ ] Code references include file:line

**Common Violations:**

❌ **WRONG - No source cited:**
```markdown
## Requirement 5
System must handle timeout after 30 seconds.
```

✅ **CORRECT - Source traced:**
```markdown
## Requirement 5
System must handle timeout after 30 seconds.

**Source:** User Answer to Question 12 (2026-02-08)
**Question:** "What timeout should we use for API calls?"
**Answer:** "30 seconds is standard for our APIs"
```

❌ **WRONG - Assumption as source:**
```markdown
## Requirement 8
Use JSON format for output files.

**Source:** Assumption (most Python projects use JSON)
```

✅ **CORRECT - Proper source or question:**
```markdown
## Requirement 8
Use JSON format for output files.

**Source:** Epic request line 67: "...output should be in JSON format for easy parsing..."
```

**Derived Requirement Example:**
```markdown
## Requirement 12 (Derived)
Log all API calls with timestamps.

**Source:** Derived from Requirements 5 and 9
**Derivation Logic:**
- Requirement 5: Must handle API timeouts
- Requirement 9: Must debug production issues
- Derivation: To debug timeouts in production, we need timestamps of API calls
- Therefore: Log all API calls with timestamps
```

---

### Dimension 5: Clarity & Specificity

**Question:** Is language specific, concrete, and unambiguous (no vague terms)?

**Checklist:**

**Banned Vague Terms:**
- [ ] No "should" (use "must" or "will")
- [ ] No "might" or "may" (specify conditions)
- [ ] No "probably" or "likely" (verify or make definite)
- [ ] No "usually" or "typically" (specify exact behavior)
- [ ] No "appropriate" or "reasonable" (specify criteria)
- [ ] No "etc." or "and so on" (enumerate completely)

**Specific Values Required:**
- [ ] Timeouts specified in seconds (not "reasonable timeout")
- [ ] Counts specified as numbers (not "several" or "many")
- [ ] Ranges specified with min/max (not "between 1 and 10-ish")
- [ ] Percentages exact (not "most" or "almost all")

**Concrete Actions:**
- [ ] Verbs are action-oriented (not "deal with errors")
- [ ] Steps are implementable (not "handle appropriately")
- [ ] Conditions are measurable (not "when ready")

**Unambiguous Language:**
- [ ] "Or" clarified (inclusive or exclusive?)
- [ ] "All" vs "some" explicit
- [ ] Order specified when matters (not "do A and B")

**Common Violations:**

❌ **WRONG - Vague language:**
```markdown
## Task 3
Handle errors appropriately.
Timeout should be reasonable.
Validate input as needed.
```

✅ **CORRECT - Specific language:**
```markdown
## Task 3
Handle errors with try/except blocks:
- FileNotFoundError: Log error, return empty list
- ValueError: Log error, raise with context
- ConnectionError: Retry 3 times with 5-second delays, then raise

Timeout: 30 seconds (per Requirement 5)

Validate input:
- Check adp value is integer between 1 and 500
- Raise ValueError if out of range
```

❌ **WRONG - "Should" instead of "must":**
```markdown
The system should validate player data.
```

✅ **CORRECT - Definitive language:**
```markdown
The system must validate player data before processing.
```

---

### Dimension 6: Upstream Alignment

**Question:** Does this artifact align with its parent/upstream artifacts?

**Checklist:**

**No Scope Creep:**
- [ ] All requirements trace to upstream (no additions)
- [ ] No features/tasks added that weren't requested
- [ ] No "improvements" beyond stated scope
- [ ] Enhancements flagged as optional/future (not required)

**No Missing Scope:**
- [ ] All upstream requirements reflected downstream
- [ ] No upstream items omitted without justification
- [ ] All explicit user requests included
- [ ] All epic goals addressed

**Change Propagation:**
- [ ] Upstream changes reflected in this artifact
- [ ] Version alignment (if upstream updated, this updated)
- [ ] References to upstream are current (not stale)

**Interpretation Accuracy:**
- [ ] Understands upstream intent correctly
- [ ] No misinterpretation of requirements
- [ ] Clarifications from user incorporated

**Common Violations:**

❌ **WRONG - Scope creep:**
```markdown
Epic Request: "Load ADP data and calculate multipliers"

Spec Requirements:
1. Load ADP data from CSV
2. Calculate multipliers based on ADP
3. Generate visualization dashboard ← NOT REQUESTED
4. Export to multiple formats ← NOT REQUESTED
```

✅ **CORRECT - Scope match:**
```markdown
Epic Request: "Load ADP data and calculate multipliers"

Spec Requirements:
1. Load ADP data from CSV (Epic request line 12)
2. Validate ADP values (Derived from requirement 1)
3. Calculate multipliers based on ADP (Epic request line 13)
4. Return multiplier values (Derived from requirement 3)

Future Enhancements (out of scope for this feature):
- Visualization dashboard
- Export to multiple formats
```

❌ **WRONG - Missing scope:**
```markdown
Epic Request: "Handle errors gracefully and log all operations"

Plan Tasks:
1. Implement data loading
2. Implement calculation
← Missing: Error handling (epic requirement)
← Missing: Logging (epic requirement)
```

✅ **CORRECT - Complete scope:**
```markdown
Epic Request: "Handle errors gracefully and log all operations"

Plan Tasks:
1. Implement data loading
2. Implement calculation
3. Implement error handling (Epic requirement line 45)
4. Implement operation logging (Epic requirement line 46)
```

---

### Dimension 7: Standards Compliance

**Question:** Does this follow project conventions, templates, and established patterns?

**Checklist:**

**Template Compliance:**
- [ ] Uses official template structure (not custom format)
- [ ] All template sections present
- [ ] Section ordering matches template
- [ ] Required metadata included (dates, versions, etc.)

**Naming Conventions:**
- [ ] File names follow project pattern (snake_case for Python)
- [ ] Variable names follow codebase style
- [ ] Class names follow conventions (PascalCase for Python)
- [ ] Function names follow conventions (snake_case for Python)

**Code Style Compliance:**
- [ ] Import organization follows project standard (see CODING_STANDARDS.md)
- [ ] Docstring format matches project (Google style)
- [ ] Type hints used where required
- [ ] Error handling follows project patterns

**Documentation Standards:**
- [ ] Headers follow markdown standards
- [ ] Code blocks have language specifiers
- [ ] Lists are consistently formatted
- [ ] Links use proper markdown syntax

**Common Violations:**

❌ **WRONG - Custom format instead of template:**
```markdown
## My Feature Spec

## What it does
...

## How it works
...
```

✅ **CORRECT - Using official template:**
```markdown
## Feature Spec: ADP Integration

## Discovery Context
...

## Feature Requirements
### Objective
...

### Scope
...

### Components Affected
...
```

❌ **WRONG - Inconsistent naming:**
```markdown
def LoadPlayerData():  # PascalCase (wrong for Python)
    player_count = ...
    numPlayers = ...  # camelCase (inconsistent)
```

✅ **CORRECT - Consistent naming:**
```markdown
def load_player_data():  # snake_case (Python convention)
    """Load player data from CSV file."""
    player_count = ...
    total_players = ...  # snake_case (consistent)
```

---

## Round-by-Round Execution

### Round 1: Initial Validation

**Purpose:** First systematic check of all dimensions

**Process:**
1. **Re-read entire artifact** (use Read tool, don't work from memory)
2. **Check each dimension sequentially** (1→2→3→4→5→6→7)
3. **Document findings** in validation log
4. **Categorize issues** by dimension and severity

**Documentation:**
```markdown
## Round 1 Results

**Timestamp:** 2026-02-10 15:00
**Artifact:** feature_02_spec.md (v1.0)

### Dimension 1: Empirical Verification
- ❌ ISSUE 1 (HIGH): Function signature assumed, not verified
  - Location: Section 3.2, line 45
  - Problem: Claims ConfigManager.get_adp() returns float
  - Reality: Returns Tuple[float, int] per ConfigManager.py:234
  - Fix: Update section 3.2 with correct signature

- ❌ ISSUE 2 (MEDIUM): File path not verified
  - Location: Section 2.1, line 12
  - Problem: References data/adp.csv
  - Reality: Actual path is data/rankings/adp.csv (verified with ls)
  - Fix: Update file path

### Dimension 2: Completeness
- ✅ PASS: All sections present

### Dimension 3: Internal Consistency
- ❌ ISSUE 3 (LOW): Inconsistent terminology
  - Location: Sections 2.1 and 4.3
  - Problem: Uses both "player_count" and "num_players"
  - Fix: Standardize on "player_count"

... (continue for all 7 dimensions)

**Round 1 Summary:**
- Total issues found: 8
- HIGH: 2, MEDIUM: 3, LOW: 3
- Issues must be fixed before Round 2
- Clean round counter: 0
```

**After Round 1:**
- Fix ALL issues immediately (no deferring)
- Update artifact
- Prepare for Round 2

---

### Round 2: Fresh Eyes Validation

**Purpose:** Re-validate with fresh perspective after fixes

**Process:**
1. **CRITICAL: Re-read ENTIRE artifact** (don't skip to changed sections)
2. **Use different reading pattern** (bottom-up, random spot-checks, etc.)
3. **Check ALL dimensions** (not just ones with issues in Round 1)
4. **Look for cross-cutting impacts** (did fix in Section 2 affect Section 5?)

**Fresh Eyes Techniques:**
- Read in reverse order (last section to first)
- Read out of sequence (random sections)
- Focus on different aspects (data flow vs error handling)
- Pretend you've never seen this before

**Documentation:**
```markdown
## Round 2 Results

**Timestamp:** 2026-02-10 15:45
**Artifact:** feature_02_spec.md (v1.1 - after Round 1 fixes)
**Reading pattern:** Bottom-up (Section 5→4→3→2→1)

### Dimension 1: Empirical Verification
- ✅ PASS: All issues from Round 1 fixed and verified
- ❌ ISSUE 9 (MEDIUM): New discovery - missed in Round 1
  - Location: Section 4.5, line 89
  - Problem: References PlayerDataManager class
  - Reality: Actual class is PlayerManager (verified grep)
  - Fix: Update class name

### Dimension 2: Completeness
- ✅ PASS: Complete

... (continue for all 7 dimensions)

**Round 2 Summary:**
- Total issues found: 2 (new issues, not from Round 1)
- HIGH: 0, MEDIUM: 2, LOW: 0
- Issues must be fixed
- Clean round counter: RESETS to 0 (issues found)
```

**If issues found:**
- Fix ALL issues
- **Counter resets to 0**
- Continue to Round 3

**If 0 issues:**
- Counter = 1
- Continue to Round 3

---

### Round 3+: Achieving Clean Rounds

**Purpose:** Continue validation until 3 consecutive clean rounds

**Process (same as Round 2):**
1. Re-read entire artifact with fresh eyes
2. Use different reading pattern
3. Check ALL dimensions
4. Document findings

**Counter Logic:**

**Scenario A: Issue found in Round 3**
```markdown
Round 1: 8 issues → Fix → Counter = 0
Round 2: 2 issues → Fix → Counter = 0
Round 3: 1 issue → Fix → Counter = 0  ← RESET
Round 4: 0 issues → Counter = 1
Round 5: 0 issues → Counter = 2
Round 6: 0 issues → Counter = 3 ✅ EXIT
```

**Scenario B: Clean from Round 3 onward**
```markdown
Round 1: 5 issues → Fix → Counter = 0
Round 2: 0 issues → Counter = 1
Round 3: 0 issues → Counter = 2
Round 4: 0 issues → Counter = 3 ✅ EXIT
```

**Maximum Rounds:**
- No hard maximum (continue until 3 consecutive clean)
- Typical: 4-7 rounds total
- If exceeding 10 rounds: Re-evaluate approach (may need to redesign artifact)

---

## Documentation Requirements

### Validation Log Template

**File:** `{artifact_name}_VALIDATION_LOG.md`

**Structure:**
```markdown
## Validation Loop Log: {Artifact Name}

**Artifact:** {file name and version}
**Validation Start:** {YYYY-MM-DD HH:MM}
**Validation End:** {YYYY-MM-DD HH:MM}
**Total Rounds:** {N}
**Final Status:** ✅ PASSED (3 consecutive clean rounds)

---

## Round 1

**Timestamp:** {YYYY-MM-DD HH:MM}
**Reading Pattern:** Sequential (top to bottom)
**Artifact Version:** v1.0

### Dimension 1: Empirical Verification
[Checklist items with ✅ PASS or ❌ ISSUE]

### Dimension 2: Completeness
[Checklist items]

... (all 7 master dimensions)

### Scenario-Specific Dimensions
[If applicable - e.g., S5 has 5 additional dimensions]

**Round 1 Summary:**
- Total Issues: {N}
- Severity Breakdown: HIGH: {N}, MEDIUM: {N}, LOW: {N}
- Clean Round Counter: {0-3}
- Next Action: Fix {N} issues, proceed to Round 2

---

## Round 2

**Timestamp:** {YYYY-MM-DD HH:MM}
**Reading Pattern:** Bottom-up
**Artifact Version:** v1.1 (after Round 1 fixes)

[Same structure as Round 1]

---

## Round N (Final Clean Round)

**Timestamp:** {YYYY-MM-DD HH:MM}
**Reading Pattern:** Random spot-checks
**Artifact Version:** v1.X

### All Dimensions: ✅ PASS

**Round N Summary:**
- Total Issues: 0 ✅
- Clean Round Counter: 3 ✅
- Status: VALIDATION COMPLETE

---

## Validation Summary

**Total Rounds:** {N}
**Total Issues Found:** {N}
**Total Issues Fixed:** {N}
**Final Clean Rounds:** 3 consecutive ✅

**Issue Breakdown by Dimension:**
- Dimension 1 (Empirical Verification): {N} issues
- Dimension 2 (Completeness): {N} issues
- Dimension 3 (Internal Consistency): {N} issues
- Dimension 4 (Traceability): {N} issues
- Dimension 5 (Clarity): {N} issues
- Dimension 6 (Upstream Alignment): {N} issues
- Dimension 7 (Standards): {N} issues

**Time Spent:**
- Round 1: {X} minutes
- Round 2: {X} minutes
- ...
- Total: {X} hours

**Lessons Learned:**
- [Most common issue type]
- [Patterns noticed]
- [Process improvements for next validation]
```

---

## Quality Standards

### Issue Severity Classification

**HIGH Severity:**
- Made-up facts (Dimension 1 violations)
- Missing critical requirements (Dimension 2)
- Logic contradictions (Dimension 3)
- No source for requirements (Dimension 4)
- Unusable/unimplementable (Dimension 5)
- Scope creep or missing scope (Dimension 6)

**MEDIUM Severity:**
- Minor verification gaps (class name wrong but similar)
- Missing optional sections
- Terminology inconsistencies
- Vague language that could be interpreted
- Minor deviations from templates

**LOW Severity:**
- Formatting inconsistencies
- Typos that don't affect meaning
- Style guideline deviations
- Documentation formatting

**CRITICAL:** ALL severity levels must be fixed (no "we'll fix LOW later")

### Reading Patterns for Fresh Eyes

**Round 1:** Sequential (top to bottom)
**Round 2:** Reverse (bottom to top)
**Round 3:** Random spot-checks (different sections)
**Round 4:** Perspective shift (from user POV, from implementer POV)
**Round 5+:** Combination approaches

### Time Expectations

**Per Round:**
- Short artifacts (specs): 15-20 minutes
- Medium artifacts (plans): 30-40 minutes
- Long artifacts (epic docs): 45-60 minutes

**Total Validation:**
- Typical: 4-7 rounds × per-round time
- Example (medium artifact): 5 rounds × 35 min = ~3 hours
- Includes fix time between rounds

---

## Exit Criteria

**Validation Loop is COMPLETE when ALL of the following are true:**

- [ ] At least 3 rounds completed
- [ ] 3 consecutive rounds with ZERO issues found
- [ ] All 7 master dimensions checked every round
- [ ] All scenario-specific dimensions checked every round
- [ ] Clean round counter = 3
- [ ] Validation log complete with all rounds documented
- [ ] Final artifact version tagged/noted
- [ ] Summary section completed in validation log

**Cannot exit if:**
- ❌ Only 2 consecutive clean rounds
- ❌ Skipped any dimensions in any round
- ❌ Deferred any issues (even LOW severity)
- ❌ Worked from memory (didn't re-read)
- ❌ Last round found issues

---

## Common Mistakes

### Mistake 1: Skipping Dimension 1 (Empirical Verification)

❌ **WRONG:**
```markdown
Round 1 Check:
- Dimension 2 (Completeness): ✅ PASS
- Dimension 3 (Consistency): ✅ PASS
[Skipped Dimension 1 - "looks fine"]
```

✅ **CORRECT:**
```markdown
Round 1 Check:
- Dimension 1 (Empirical Verification):
  - [ ] Verified ConfigManager.get_adp() signature from source
  - [ ] Verified file path data/rankings/adp.csv exists
  - [ ] Verified PlayerManager class name from grep
  - Result: ❌ 2 issues found (wrong signature, wrong path)
```

**Why this matters:** Dimension 1 violations cascade (if function signature is wrong, everything depending on it is wrong)

---

### Mistake 2: Working from Memory Instead of Re-Reading

❌ **WRONG:**
```markdown
Round 3:
"I remember fixing Section 3.2 in Round 1, so I'll skip reading it again.
Just checking new sections..."
```

✅ **CORRECT:**
```markdown
Round 3:
"Re-reading ENTIRE artifact from beginning, even sections I know I fixed.
Using bottom-up reading pattern for fresh perspective..."
```

**Why this matters:** Fresh eyes catch issues missed when working from memory

---

### Mistake 3: Deferring LOW Severity Issues

❌ **WRONG:**
```markdown
Round 2 Summary:
- HIGH issues: 0
- MEDIUM issues: 0
- LOW issues: 3 (formatting, will fix later)
- Counter: 1 ✅ [WRONG - issues still exist]
```

✅ **CORRECT:**
```markdown
Round 2 Summary:
- HIGH issues: 0
- MEDIUM issues: 0
- LOW issues: 3 (formatting - MUST FIX NOW)
- Fix all 3 LOW issues
- Counter: RESETS to 0 (issues found)
```

**Why this matters:** Zero deferred issues principle - ALL issues matter

---

### Mistake 4: Not Resetting Counter When Issues Found

❌ **WRONG:**
```markdown
Round 3: 1 issue found → Fixed
Round 4: 0 issues
Counter: 2 [WRONG - should reset]
Round 5: 0 issues
Counter: 3 → EXIT [WRONG - didn't get 3 consecutive]
```

✅ **CORRECT:**
```markdown
Round 3: 1 issue found → Fixed
Counter: RESETS to 0
Round 4: 0 issues → Counter = 1
Round 5: 0 issues → Counter = 2
Round 6: 0 issues → Counter = 3 → EXIT ✅
```

---

### Mistake 5: Batching Dimensions Instead of Checking All

❌ **WRONG:**
```markdown
Round 1: Check Dimensions 1-3
Round 2: Check Dimensions 4-7
[Never check all dimensions in single round]
```

✅ **CORRECT:**
```markdown
Round 1: Check ALL 7 dimensions + scenario-specific
Round 2: Check ALL 7 dimensions + scenario-specific
Round 3: Check ALL 7 dimensions + scenario-specific
```

**Why this matters:** Issues can span dimensions (fixing D1 might affect D6)

---

## How Scenario-Specific Loops Extend This Master

### Extension Pattern

**All scenario-specific validation loops:**
1. **Reference this master protocol** ("See validation_loop_master_protocol.md")
2. **Inherit all 7 master dimensions** (always checked)
3. **Add 2-8 scenario-specific dimensions** (context-dependent)
4. **Total dimensions: 9-15** per scenario

### Example: S5 Implementation Planning Loop

**File:** `reference/validation_loop_implementation_planning.md`

**Structure:**
```markdown
## Validation Loop: Implementation Planning (S5)

**Extends:** Master Validation Loop Protocol
**See:** reference/validation_loop_master_protocol.md

## Master Dimensions (7) - Always Checked

1. ✅ Empirical Verification
2. ✅ Completeness
3. ✅ Internal Consistency
4. ✅ Traceability
5. ✅ Clarity & Specificity
6. ✅ Upstream Alignment
7. ✅ Standards Compliance

**See master protocol for checklists**

---

## S5-Specific Dimensions (5) - Implementation Context

### Dimension 8: Algorithm Traceability
[Specific to implementation plans]
[Checklist for tracing algorithm steps to spec]

### Dimension 9: Integration Gap Check
[Specific to implementation plans]
[Checklist for external dependencies]

### Dimension 10: E2E Data Flow
[Specific to implementation plans]
[Checklist for data flow completeness]

### Dimension 11: TODO Specificity
[Specific to implementation plans]
[Checklist for actionable TODOs]

### Dimension 12: Error Handling Coverage
[Specific to implementation plans]
[Checklist for error scenarios]

---

## Total Dimensions: 12 (7 master + 5 S5-specific)

## Validation Process
[Same as master: 3 consecutive clean rounds, zero deferred issues]
```

### Scenario-Specific Dimension Examples

**S2 Spec Validation:**
- Dimension 8: Research Completeness (all unknowns researched)
- Dimension 9: Question Quality (checklist has valid questions)

**S4 Test Strategy:**
- Dimension 8: Test Coverage (>90% requirement coverage)
- Dimension 9: Edge Case Enumeration (all edge cases identified)
- Dimension 10: Test Specificity (tests are concrete, not vague)

**S7 Validation Loop:**
- Dimension 8: Cross-Feature Integration (integration points work)
- Dimension 9: Data Flow Validation (data flows correctly)
- Dimension 10: Error Propagation (errors propagate correctly)

**S9 Epic QC:**
- Dimension 8: Epic-Level Integration (all features work together)
- Dimension 9: Epic Cohesion (architectural consistency)
- Dimension 10: Epic Success Criteria (original goals met)
- Dimension 11: Performance Validation (meets performance targets)

---

## Templates

### Quick Checklist Template (Per Round)

```markdown
## Round {N} Checklist

**Master Dimensions:**
- [ ] D1: Empirical Verification (everything verified from source)
- [ ] D2: Completeness (all sections present)
- [ ] D3: Internal Consistency (no contradictions)
- [ ] D4: Traceability (all decisions sourced)
- [ ] D5: Clarity & Specificity (no vague language)
- [ ] D6: Upstream Alignment (matches parent artifacts)
- [ ] D7: Standards Compliance (follows templates)

**Scenario-Specific Dimensions:**
- [ ] D8: [Scenario dimension 1]
- [ ] D9: [Scenario dimension 2]
... (as applicable)

**Round Result:**
- Issues Found: {N}
- Clean Round Counter: {0-3}
- Next Action: [Fix issues / Continue to next round / EXIT]
```

### Issue Tracking Template

```markdown
## Issue {N}

**Dimension:** [1-7 or scenario-specific]
**Severity:** [HIGH / MEDIUM / LOW]
**Location:** [Section, line number]
**Found in Round:** {N}

**Problem:**
[What is wrong]

**Expected:**
[What should it be]

**Fix:**
[How to fix it]

**Verification:**
[How to verify fix]

**Fixed:** [ ] Yes [Timestamp]
**Verified in Round:** {N}
```

---

## Summary

**Master Validation Loop Protocol provides:**
- ✅ 7 universal dimensions (apply to ALL validation contexts)
- ✅ Core process (3 consecutive clean rounds, zero deferred issues)
- ✅ Systematic approach (all dimensions every round)
- ✅ Quality guarantee (fresh eyes, complete re-reading)
- ✅ Extensibility (scenario-specific loops add dimensions)

**Next Steps:**
1. Apply this master protocol to your validation scenario
2. Add scenario-specific dimensions (2-8 typical)
3. Follow round-by-round execution
4. Document in validation log
5. Exit when 3 consecutive clean rounds achieved

**Key Principle:**
> "Never assume - always verify. Check everything, every round, until 3 consecutive rounds are clean."

---

*End of Master Validation Loop Protocol v2.0*
