# Discovery Phase Examples

**Purpose:** Detailed real-world examples of Discovery Phase iterations, questions, and outcomes
**Prerequisites:** S1.P3 guide read from `stages/s1/s1_p3_discovery_phase.md`
**Main Guide:** `stages/s1/s1_p3_discovery_phase.md`

---

## Table of Contents

1. [Example 1: Well-Executed Discovery Phase (MEDIUM Epic)](#example-1-well-executed-discovery-phase-medium-epic)
2. [Example 2: Discovery Loop Exit (3 Consecutive Clean Rounds)](#example-2-discovery-loop-exit-3-consecutive-clean-rounds)
3. [Example 3: Discovery Revealing Larger Scope](#example-3-discovery-revealing-larger-scope)
4. [Example 4: Anti-Pattern - Skipping Discovery](#example-4-anti-pattern---skipping-discovery)
5. [Example 5: Discovery Time-Boxing by Size](#example-5-discovery-time-boxing-by-size)
6. [Key Takeaways](#key-takeaways)

---

## Example 1: Well-Executed Discovery Phase (MEDIUM Epic)

**Epic Request:** "Make debugging runs easier"

### S1.P3.1: Initialize DISCOVERY.md

**Initial Epic Request Summary:**
```markdown
## Epic Request Summary

**Original Request:** "Make debugging runs easier"

**Initial Understanding:**
- User finds current debugging workflow frustrating
- "Easier" is not defined - need to clarify

**Initial Questions:**
1. What makes debugging hard currently?
2. What would "easier" look like?
3. Which parts of the workflow are most painful?
```

### S1.P3.2: Discovery Loop - Iteration 1

**Research Focus:** Understand current debugging workflow

**Files Examined:**
- `[run_script].py:45-120` - Main entry point, no debug flags found
- `[module]/core.py:200-350` - Calculation core, minimal logging
- `[module]/runner.py:180-290` - Similar pattern, no debug output

**Findings:**
- No debug logging in critical calculation paths
- Errors fail silently (caught exceptions with no output)
- No way to run simulation on subset of data
- No intermediate output to inspect calculation steps

**Questions for User:**

**Question 1: Pain Points**
What specifically is frustrating about debugging?

**Context:** I found no debug logging and silent error handling.

**Options:**
- Option A: Can't see intermediate values during calculations
- Option B: Errors don't show useful information
- Option C: Can't run on small datasets for testing
- Option D: All of the above
- Option E: Something else entirely

---

**User Answer:** "Option D - all of the above, plus it takes forever to run and I can't tell if it's stuck or making progress"

---

### S1.P3.2: Discovery Loop - Iteration 2

**Research Focus:** Progress visibility and performance

**Files Examined:**
- `[module]/core.py:1-50` - No progress callbacks
- `[module]/runner.py:1-50` - Same pattern
- `[module]/executor.py:100-200` - Main loop, no progress reporting

**Findings:**
- Processing runs {N} iterations with no progress output
- No way to know if simulation is stuck vs working
- No partial results saved (all-or-nothing)
- Average run time: 15-20 minutes with no feedback

**Questions for User:**

**Question 2: Progress Visibility**
Would progress bars/percentage complete solve the "can't tell if stuck" problem?

**Context:** Currently runs {N} iterations with zero output until completion.

**Options:**
- Option A: Yes, progress bar would help a lot
- Option B: I also want to see partial results as it runs
- Option C: I need to be able to cancel and resume later

---

**User Answer:** "Option A is fine - I don't need partial results, just want to know it's working"

---

**Question 3: Debug Mode Scope**
Should debug mode affect all simulations, or just specific types?

**Context:** There are two simulation types (accuracy and win rate).

**Options:**
- Option A: Same debug mode for both
- Option B: Separate debug options for each type

---

**User Answer:** "Option A - keep it simple, same debug mode for both"

---

### S1.P3.2: Discovery Loop - Iteration 3

**Research Focus:** Logging infrastructure and data subsetting

**Files Examined:**
- `utils/logger.py:1-100` - Existing logger, not used in processing modules
- `data/records.json:1-50` - {N}+ records in file
- `[module]/config.py:20-80` - No subset options

**Findings:**
- Logger exists but not used in processing modules
- Running on full {N}-record dataset even for debugging
- No config option to limit record count
- Config already has verbose flag (unused)

**Questions for User:**

**Question 4: Subset Size**
For debugging, how many records should the "small subset" include?

**Context:** Full dataset is {N}+ records.

**Options:**
- Option A: 10 records (very fast, but might miss edge cases)
- Option B: 50 records (reasonable coverage, quick)
- Option C: 100 records (better coverage, ~30 seconds)
- Option D: Let me specify the number

---

**User Answer:** "Option D - I want to specify it, but default to 50"

---

**Question 5: Error Visibility**
When errors occur, what information do you need?

**Context:** Currently errors are caught silently.

**Options:**
- Option A: Stack trace + item that caused error
- Option B: Full context dump (all variables)
- Option C: Just the error message is fine

---

**User Answer:** "Option A - stack trace and which item caused it"

---

### S1.P3.2: Discovery Loop - Iteration 4 (Clean Round 1 of 3)

**Research Focus:** Validate DISCOVERY.md for completeness — check for gaps, inconsistencies, missing scope

**Files Examined:**
- Re-reviewed all simulation modules
- Checked config patterns
- Looked at existing verbose flag usage

**Findings:**
- Existing verbose flag could be repurposed for debug mode
- All questions answered — zero issues/gaps found this round
- Clear picture of what needs to be built

**Questions for User:** None

**Clean Round Counter:** 1 of 3 — two more clean rounds needed before exit.

*(Note: Example 1 abbreviates iterations 5 and 6 for brevity — both produced zero issues/gaps, reaching counter = 3 and triggering Discovery Loop exit.)*

---

### S1.P3.3: Synthesize Findings

**Discovery Summary:**
```markdown
## Summary of Findings

**Core Problems Identified:**
1. No visibility into simulation progress
2. Silent error handling hides problems
3. Full dataset runs are slow for debugging
4. No intermediate calculation visibility

**User Preferences Confirmed:**
- Progress bar (not partial results)
- Same debug mode for both simulation types
- Configurable subset size (default 50)
- Stack trace + item context for errors

## Recommended Approach

Add a debug mode to simulations with:
1. Progress bar showing iteration count
2. Configurable item subset for fast runs
3. Verbose error output with stack traces
4. Debug logging in calculation paths
```

### S1.P3.4: Proposed Feature Breakdown

**Proposed Scope:**

**In Scope:**
- Progress bar for simulation iterations
- Item subset configuration
- Debug logging in calculations
- Enhanced error messages with context

**Out of Scope:**
- Partial result saving (user said not needed)
- Separate debug modes per simulation type (user wants unified)
- Resume capability (not requested)

**Proposed Features:**

1. **Feature 01: Debug Mode Infrastructure**
   - Purpose: Add debug flag and progress tracking
   - Scope: Config options, progress bar, logging setup
   - Dependencies: None (foundation)

2. **Feature 02: Subset Simulation Support**
   - Purpose: Run on configurable item subsets
   - Scope: Item filtering, count parameter
   - Dependencies: Feature 01

3. **Feature 03: Enhanced Error Reporting**
   - Purpose: Improve error visibility with context
   - Scope: Stack traces, item context, error logging
   - Dependencies: Feature 01

---

**User Approval:** "Approved - this captures what I need"

---

## Example 2: Discovery Loop Exit (3 Consecutive Clean Rounds)

**Epic Request:** "Add JSON export for item rankings"

### Iteration 1 - Research

**Files Examined:**
- `[module]/export.py` - Existing CSV export found
- `[module]/classes/PlayerRanking.py` - Data structure examined

**Findings:**
- CSV export already exists, can use similar pattern
- PlayerRanking has `to_dict()` method
- JSON library already imported in project

**Questions for User:**

**Question 1:** What format should the JSON file have?
- Option A: Array of item objects
- Option B: Object with item names as keys
- Option C: Nested by position, then items

**User Answer:** "Option A - simple array"

---

### Iteration 2 - Research (Clean Round 1 of 3)

**Files Examined:**
- Re-reviewed export.py patterns
- Checked other JSON files in project for consistency

**Findings:**
- Pattern is clear: copy CSV export, change serialization
- Simple scope, zero issues/gaps found this round

**Questions for User:** None

**Clean Round Counter:** 1 of 3 — continuing loop.

---

### Iteration 3 - Research (Clean Round 2 of 3)

**Files Examined:**
- Checked integration points (data pipeline, file I/O layer)
- Verified no naming conflicts with existing exports

**Findings:**
- Integration points confirmed — no changes required
- Zero issues/gaps found this round

**Questions for User:** None

**Clean Round Counter:** 2 of 3 — continuing loop.

---

### Iteration 4 - Research (Clean Round 3 of 3)

**Files Examined:**
- Final review: error handling patterns, test coverage expectations
- Confirmed scope boundary (export only, no UI changes)

**Findings:**
- No new integration concerns
- Zero issues/gaps found this round

**Questions for User:** None

**Clean Round Counter:** 3 of 3 — exit criterion met.

**Discovery Loop Exit:** 3 consecutive clean rounds with zero issues/gaps completed.

---

### Synthesis

**Assessment:** This is a SMALL epic (possibly single feature).
- Clear pattern to follow
- No ambiguity in requirements
- Straightforward implementation

**Recommendation:** Proceed with single feature epic or consider as non-epic task.

---

## Example 3: Discovery Revealing Larger Scope

**Epic Request:** "Fix the broken trend projections"

### Iteration 1 - Initial Research

**Files Examined:**
- `[module]/trends.py` - File not found!
- `[module]/modes/` - No trend projection mode exists

**Findings:**
- There IS no trend projection feature
- User thinks it exists but it doesn't
- This is a NEW FEATURE, not a fix

**Questions for User:**

**Question 1:** I can't find existing trend projections. Were you expecting this to already exist?

**User Answer:** "Oh, I thought it was there. I guess we need to build it from scratch."

---

### Iteration 2 - Scope Clarification

**Questions for User:**

**Question 2:** What should trend projections show?
- Option A: Just probability of exceeding threshold
- Option B: Full trend lines with breakdowns by period
- Option C: Both probability and trend lines

**User Answer:** "Option A for now - just probability"

**Question 3:** Which periods count as the projection window?
- Option A: Last N periods (configurable)
- Option B: Fixed rolling window
- Option C: Let me configure it

**User Answer:** "Option C - let me configure it"

---

### Iteration 3 - Technical Research

**Files Examined:**
- `[module]/classes/[EntityClass].py` - Has record tracking
- `[module]/projections/` - Has projection capabilities

**Findings:**
- Entity records are tracked
- Projection logic exists in projections module
- Need to combine historical records + projections

**Questions for User:** None - scope is now clear.

---

### Synthesis

**Scope Changed:** This is a NEW FEATURE epic, not a bug fix.
- Estimated 3-4 features
- MEDIUM complexity
- Discovery prevented building the wrong thing

---

## Example 4: Anti-Pattern - Skipping Discovery

**What happens when Discovery is skipped:**

**Epic Request:** "Improve data loading performance"

**Without Discovery:**
```text
Agent creates features immediately:
- Feature 01: Add caching
- Feature 02: Parallelize loading
- Feature 03: Optimize queries

Problems discovered DURING implementation:
- Bottleneck was actually network latency, not code
- User wanted faster startup time, not faster data load
- Caching strategy conflicted with existing cache
- All 3 features were wrong approach
```

**With Discovery:**
```bash
Iteration 1: "What is slow?"
User: "Startup takes 30 seconds"

Iteration 2: Research reveals startup loads config twice
User: "Didn't know that, can we fix it?"

Iteration 3: Find unnecessary API call during startup
User: "Yes, remove that"

Actual fix: 2 small changes, no new features needed
Time saved: 2 weeks of wrong work
```

---

## Example 5: Discovery Time-Boxing by Size

### SMALL Epic (1-2 hours time-box)

**Request:** "Add dark mode to CLI output"

**Discovery completes in 3 iterations:**
1. Check current color handling (colorama library found)
2. Ask about color preferences (user wants invert, not custom)
3. Verify no other requirements (none - single feature)

**Total time:** 45 minutes
**Features:** 1

---

### MEDIUM Epic (2-3 hours time-box)

**Request:** "Improve search recommendations"

**Discovery completes in 5-6 iterations:**
1. Understand current algorithm
2. Identify what's "wrong" with recommendations
3. Research data sources
4. Clarify weighting preferences
5. Verify integration points
6. Confirm scope boundaries

**Total time:** 2.5 hours
**Features:** 3-4

---

### LARGE Epic (3-4 hours time-box)

**Request:** "Add multi-tenant account support"

**Discovery completes in 8-9 iterations:**
1. Understand isolation requirements
2. Research subscription/tier concepts
3. Identify affected modules
4. Clarify cross-account data handling
5. Discuss new user onboarding
6. Review budget limit requirements
7. Check database schema needs
8. Verify migration requirements
9. Confirm integration strategy
10. Validate scope boundaries

**Total time:** 3.5 hours
**Features:** 6-7

---

## Key Takeaways

### Good Discovery Patterns

1. **Start broad, then narrow**
   - First iteration: "What's the problem?"
   - Later iterations: "Which specific option?"

2. **Research before asking**
   - Check code first
   - Form hypotheses
   - Ask informed questions

3. **Exit when no questions emerge**
   - Don't force more iterations
   - If research produces no questions, you're done

4. **Document everything**
   - Every finding
   - Every question
   - Every answer
   - Enables future reference

### Bad Discovery Patterns

1. **Asking without research**
   - "What do you want?" (too vague)
   - Should be: "I found X, should we do A or B?"

2. **Too many iterations**
   - 10+ iterations for SMALL epic = overthinking
   - Respect time-box

3. **Not exiting when done**
   - Research produces no questions = exit
   - Don't invent questions to fill time

4. **Skipping entirely**
   - "I know what to do" = dangerous assumption
   - Always do at least 1-2 iterations

---

*End of reference/stage_1/discovery_examples.md*
