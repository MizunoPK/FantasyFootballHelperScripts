# Feature Planning Guide

This guide helps agents assist users in developing thorough, well-structured feature specifications. A well-planned feature enables future agents to implement it efficiently without re-researching decisions.

**Related Files:**
- `templates.md` - File templates (README, specs, checklist, lessons learned)
- `feature_development_guide.md` - Implementation workflow (use after planning)

---

## Quick Start (5 Steps)

1. **Create folder** - `feature-updates/{feature_name}/`, move `.txt` notes into it
2. **Create planning files** - README, specs, checklist, lessons_learned (use templates)
3. **Investigate codebase** - Research patterns, files to modify, populate checklist with questions
4. **Report & STOP** - Present findings to user, wait for direction (Phase 3 is mandatory pause)
5. **Resolve iteratively** - Address checklist items until all are `[x]`, then user says "Prepare for updates"

**CRITICAL:** Update the README.md "Agent Status" section after completing each step. This ensures continuity if the session is interrupted.

**Need to resume?** → See "Resuming Work Mid-Planning" section below.

---

## Common Mistakes to Avoid

| Mistake | Why It's Bad | Prevention |
|---------|--------------|------------|
| Skipping Phase 3 STOP | User doesn't approve direction; wasted work | **Always wait for explicit user approval** before Phase 4 |
| Vague checklist items | "Figure out data" doesn't help implementation | Break down to field-level: "Where does `player_rating` come from?" |
| Not linking to existing code | Future agents re-research the same patterns | Include file paths and line numbers: `PlayerManager.py:150-200` |
| Assuming answers | Guessing requirements leads to rework | Always confirm with user; document source of each decision |
| Incomplete investigation | Missing edge cases discovered during implementation | Use ALL checklist categories: API, Algorithm, Architecture, Edge Cases |
| Accepting vague specs | "Resume capability" without defining mechanism | **Vagueness Audit** - flag phrases like "similar to X", "handle appropriately" |
| Missing feature pairs | "Save X" implemented but "Load X" forgotten | **Feature Pair Check** - if save exists, load must too (and be called!) |

---

## When to Use This Guide

Use this guide when a user says something like:
- "Help me develop the {feature_name} feature"
- "I want to plan {feature_name}"
- "Let's work on the {feature_name} specification"

The user will have already created a `.txt` file in the `feature-updates/` folder with their initial high-level requirements. This file contains their scratchwork notes and initial ideas.

**Do NOT use this guide for:**
- Bug fixes (use standard workflow)
- Simple changes that don't require planning
- Questions about existing functionality
- Implementation work (use `feature_development_guide.md` instead)

---

## When You Get Stuck

| Situation | Action |
|-----------|--------|
| Can't find relevant code | Search with different terms; check imports; ask user for hints |
| User's notes are unclear | Ask clarifying questions in Phase 3; don't guess |
| Too many open questions | Group by category; prioritize most impactful first |
| User not responding | Document current state in README; pause at Phase 3 |
| Scope keeps growing | Document "out of scope" items; ask user to confirm boundaries |
| Conflicting requirements | Document conflict in checklist; ask user to resolve |

---

## Resuming Work Mid-Planning

If you're picking up planning work started by a previous agent:

1. **Read the feature folder README first**: `feature-updates/{feature_name}/README.md`
   - Check "Current Status" to see which phase you're in
   - Review "What's Resolved" vs "What's Still Pending"

2. **Determine current phase:**
   | README Status | Current Phase | Next Action |
   |---------------|---------------|-------------|
   | "Phase 1: Creating Structure" | Phase 1 incomplete | Finish creating files |
   | "Phase 2: Investigation" | Phase 2 in progress | Continue codebase research |
   | "Phase 3: Awaiting User Input" | Phase 3 STOP | Present findings to user, wait for direction |
   | "Phase 4: Resolving Items" | Phase 4 in progress | Check checklist for next unresolved item |
   | "Ready for Implementation" | Planning complete | Switch to `feature_development_guide.md` |

3. **Read supporting files in order:**
   - `{feature_name}_specs.md` - Current specification state
   - `{feature_name}_checklist.md` - What's resolved `[x]` vs pending `[ ]`
   - `{feature_name}_notes.txt` - Original requirements (reference only)

4. **Continue from where previous agent stopped** - Don't restart from Phase 1

---

## Pre-Phase: Investigation Spike (Optional)

**When to use:** When initial notes are too vague to begin structured planning. Signs you need a spike:
- "I want something like X but I'm not sure how"
- "Can we even do Y with the current codebase?"
- Multiple fundamental unknowns that block even basic planning
- User is unsure what they want and needs exploration to clarify

**Spike Process:**

1. **Time-box:** Maximum 2-4 hours of investigation
2. **Goal:** Answer ONE question: "Is this feasible and what's the general approach?"
3. **Activities:**
   - Explore the codebase for relevant patterns
   - Research external APIs or data sources
   - Prototype a minimal proof-of-concept (NO production code)
   - Identify key unknowns that need resolution

4. **Output:** Updated notes file with:
   ```markdown
   ## Spike Results

   **Feasibility:** [Yes / No / Maybe with caveats]

   **Rough Approach:**
   - [High-level approach if feasible]

   **Key Unknowns to Resolve During Planning:**
   - [Unknown 1]
   - [Unknown 2]

   **Risks Identified:**
   - [Risk 1]
   ```

**After spike:** Return to Phase 1 with a better foundation for structured planning.

**Do NOT use spikes to:**
- Delay planning indefinitely ("we need more spikes")
- Write prototype code that becomes production code
- Skip planning ("we already did a spike, let's just implement")
- Avoid making decisions ("let's spike it first" as procrastination)

**Spike vs Planning:**
| Spike | Planning |
|-------|----------|
| Answers "can we?" | Answers "how will we?" |
| Time-boxed (2-4 hours) | Takes as long as needed |
| Output: feasibility + rough approach | Output: detailed specs |
| Optional | Mandatory |

---

## Workflow Overview

```
(Optional) Pre-Phase: Investigation Spike
    For high-uncertainty features only
                            ↓
Phase 1: Create Structure
    Agent creates folder, moves notes, creates initial specs/checklist/readme
                            ↓
Phase 2: Investigation
    Agent researches codebase, identifies open questions,
    populates checklist with all unknowns
                            ↓
Phase 3: Report & Pause
    Agent reports understanding + open questions to user
    Asks: "Add items? Or start addressing checklist?"
                            ↓
Phase 4: Iterative Resolution (loop)
    User directs agent to investigate item OR provides answer
    Agent updates specs, marks checklist done, updates readme
    Repeat until all items resolved
                            ↓
Ready for Implementation
    User says "Prepare for updates based on {feature_name}"
```

---

## Agent Quick Reference Checklist

Use this checklist to track progress through planning phases:

```
□ PHASE 1: Create Structure
  □ Create folder: feature-updates/{feature_name}/
  □ Move notes: {feature_name}.txt → {feature_name}_notes.txt
  □ Create: README.md (use template with Agent Status section)
  □ Create: {feature_name}_specs.md (objective + requirements from notes)
  □ Create: {feature_name}_checklist.md (empty, to be populated)
  □ Create: {feature_name}_lessons_learned.md (empty template)
  □ ⚡ UPDATE README Agent Status: Phase=PLANNING, Step=Phase 1 complete

□ PHASE 2: Investigation
  □ 2.1: Read and analyze _notes.txt thoroughly
  □ 2.2: Research codebase (patterns, files to modify, similar features)
  □ 2.3: Populate checklist with ALL open questions by category
  □ 2.3.1: THREE-ITERATION question generation (MANDATORY)
    □ Iteration 1: Edge cases, error conditions, configuration options
    □ Iteration 2: Logging, performance, testing, integration workflows
    □ Iteration 3: Relationships to similar features, cross-cutting concerns
  □ 2.4: CODEBASE VERIFICATION rounds (MANDATORY)
    □ Round 1: Search codebase for answers to each question
    □ Round 2: Skeptically re-verify findings from Round 1
    □ Categorize: [x] Resolved from code | [ ] Needs user decision | [ ] Unknown
  □ 2.5: Performance analysis for implementation options
  □ 2.6: Create DEPENDENCY MAP showing module + data flow
  □ 2.7: Update _specs.md with discovered context + dependency map
  □ 2.8: VAGUENESS AUDIT - flag ambiguous phrases, add checklist items for each
    □ Flag phrases like "similar to X", "resume capability", "handle appropriately"
    □ Check feature pairs: if "save X" exists, verify "load X" is also specified
    □ Add checklist items for each vague phrase requiring clarification
  □ 2.9: ASSUMPTIONS AUDIT - list all assumptions with basis/risk/mitigation
  □ 2.10: TESTING REQUIREMENTS ANALYSIS (MANDATORY)
    □ Identify integration points (what modules/systems interact)
    □ Define smoke test success criteria (output validation, not just "runs")
    □ List expected vs actual comparisons (baseline values, log patterns)
    □ Identify user-facing outputs (logs, files, progress displays)
    □ Plan acceptance testing (how will user confirm it works correctly)
    □ Add testing checklist items for user to review/confirm
  □ Update README.md with key findings
  □ ⚡ UPDATE README Agent Status: Step=Phase 2 complete

⛔ PHASE 3: Report & Pause ════════════════════════════════════════
  ║ MANDATORY FULL STOP - DO NOT PROCEED WITHOUT USER APPROVAL ║
  □ Present: Feature summary (1 paragraph)
  □ Present: Key findings from codebase research
  □ Present: Files likely to be affected
  □ Present: Scope (in vs out)
  □ Present: All open questions grouped by category
  □ Ask user: "Add items? Or start addressing checklist?"
  □ ⚡ UPDATE README Agent Status: Step=Phase 3 - Awaiting user direction
  □ 🛑 WAIT for user response before proceeding
  ════════════════════════════════════════════════════════════════

□ PHASE 4: Iterative Resolution
  □ For each item user directs:
    □ If "investigate": Research → Propose → Wait for confirmation
    □ If user provides answer: Document immediately
    □ Update _specs.md with resolved details
    □ Mark checklist item [x]
    □ Update README.md if scope affected
    □ Report remaining items, ask "which next?"
  □ Repeat until ALL checklist items are [x]
  □ ⚡ UPDATE README Agent Status after each resolution

□ READY FOR IMPLEMENTATION
  □ All checklist items marked [x]
  □ _specs.md has complete implementation details
  □ ⚡ UPDATE README Agent Status: Phase=PLANNING, Step=Complete
  □ Mark README checklist: Planning Complete - Ready for Implementation
  □ User confirms planning is complete
  □ Wait for: "Prepare for updates based on {feature_name}"
```

**⚡ = Status Update Required**: These steps update the README "Agent Status" section to ensure session continuity.

### Files to Update Per Phase

| Phase | Files Created/Updated |
|-------|----------------------|
| 1 | Create all 5 files (README, specs, checklist, lessons_learned, notes) |
| 2 | Update: checklist.md (add questions), specs.md (add context), README.md (findings) |
| 3 | No file changes (reporting to user only) |
| 4 | Update: checklist.md (mark [x]), specs.md (add details), README.md (if scope changes) |
| Done | Update: README.md (status → "Ready for Implementation") |

---

## Phase 1: Create Folder Structure

**Trigger:** User says "Help me develop the {feature_name} feature"

### Step 1.1: Create the folder and move notes

```bash
mkdir -p feature-updates/{feature_name}/
mv feature-updates/{feature_name}.txt feature-updates/{feature_name}/{feature_name}_notes.txt
```

### Step 1.2: Create initial planning files

```
feature-updates/{feature_name}/
├── README.md                        # Context for future agents
├── {feature_name}_notes.txt         # Original scratchwork (moved from root)
├── {feature_name}_specs.md          # Detailed specification
├── {feature_name}_checklist.md      # Tracks decisions and open questions
└── {feature_name}_lessons_learned.md # Captures issues to improve the guides
```

### Step 1.3: Populate initial files based on notes

Read the `_notes.txt` file and create initial versions of:

**README.md** - Basic context:
- What the feature is (from notes)
- Why it's needed (from notes)
- Current status: "Phase 2: Investigation"

**{feature_name}_specs.md** - Initial specification:
- Objective (extracted from notes)
- High-level requirements (extracted from notes)
- Empty "Open Questions" section (to be populated in Phase 2)
- Empty "Resolved Implementation Details" section

**{feature_name}_checklist.md** - Initial checklist:
- General decisions section (empty, to be populated in Phase 2)
- Note at top: "Checklist items will be added during investigation phase"

**{feature_name}_lessons_learned.md** - Lessons learned file:
- Empty initially with header explaining purpose
- Will be populated during development and QA phases
- Used to improve the planning and development guides

---

## Phase 2: Investigation

**Goal:** Research the codebase and notes to identify ALL open questions about code structure and algorithm implementation.

### Step 2.1: Analyze the notes thoroughly

Read the `_notes.txt` file and identify:
- What is clearly specified vs what is ambiguous
- What technical decisions need to be made
- What data sources or APIs are involved
- What existing code might be affected or reused

### Step 2.2: Research the codebase

Use exploration tools to understand:
- Existing patterns that should be followed
- Files that will need modification
- Dependencies and integration points
- Similar features that can serve as reference

### Step 2.3: Populate the checklist with open questions

Add ALL identified open questions to the checklist, organized by category:

**Categories to consider:**
- **API/Data Source Questions:** Where does data come from? What format?
- **Algorithm Questions:** How should X be calculated? What logic?
- **Architecture Questions:** Where should code live? What patterns?
- **Error Handling Questions:** What happens when X fails?
- **Edge Case Questions:** What about bye weeks, injuries, missing data?
- **Integration Questions:** How does this interact with existing code?
- **Testing Questions:** How will this be validated?

**For API-dependent features:** Consider running test scripts against the actual API during planning to verify assumptions about edge cases and data formats. This prevents surprises during implementation (e.g., verifying DST negative scores, bye week handling, missing data responses).

### Step 2.3.1: Three-Iteration Question Generation (MANDATORY)

After initial checklist population, complete THREE separate iterations of question generation:

**Iteration 1:** Review initial questions and categories. For each category, ask:
- "What edge cases might apply here?"
- "What error conditions could occur?"
- "What configuration options might be needed?"

**Iteration 2:** Consider operational aspects:
- Logging and debugging needs
- Performance and parallelization
- Testing and validation approaches
- Integration with existing workflows

**Iteration 3:** Consider relationships and comparisons:
- How does this feature relate to similar existing features?
- What cross-cutting concerns exist (multi-season, multi-mode)?
- What user workflow questions remain?

Document new questions discovered in each iteration before proceeding.

**Why this matters:** A single pass of question generation typically misses 20+ questions across 8+ categories. Multiple iterations surface:
- Scoring mode configuration questions
- Multi-season handling questions
- Parallelization & performance questions
- Logging & debugging questions
- Relationship between feature modes
- Additional edge cases (minimum thresholds)
- Integration workflow questions

### Step 2.4: Codebase Verification Rounds (MANDATORY)

After populating the checklist with questions, perform TWO verification rounds to determine which questions can be answered from existing code:

**CRITICAL: DO NOT mark any checklist items as [x] during codebase verification.**

Your role is to:
- Research the codebase
- Document findings in the checklist's Resolution Log
- Provide recommendations
- Leave ALL items as [ ] for user review

Only the USER can mark items as [x] after reviewing your findings during Phase 4.

**Round 1: Initial Codebase Research**
For each open checklist item:
1. Search the codebase for relevant code, patterns, or existing implementations
2. If a straightforward answer exists in the code → document it in Resolution Log (leave as [ ])
3. If multiple valid approaches exist → document options with code references for user decision (leave as [ ])
4. If no answer found in codebase → leave as open question for user (leave as [ ])

**Round 2: Skeptical Re-verification**
Assume all findings from Round 1 are potentially incorrect:
1. Re-search with different terms and approaches
2. Verify claims made in Round 1 are accurate
3. Check for edge cases or exceptions missed in Round 1
4. Look for contradictions between code and documentation

**Output:** Checklist Resolution Log should categorize each item:
- "RESOLVED from codebase" - straightforward answer found (code references provided)
- "NEEDS USER DECISION" - multiple valid approaches documented
- "UNKNOWN" - no answer in codebase, requires user input

All items remain `[ ]` until Phase 4 when user reviews and approves.

**Why this matters:** This prevents:
- Asking the user questions that have obvious answers in the code
- Planning phase taking longer than necessary
- Wasting user's time on questions the agent could answer itself

### Step 2.5: Include Performance Analysis

When proposing implementation options, ALWAYS analyze efficiency implications:

**Performance Checklist:**
- [ ] **Time complexity**: Big-O or estimated operation counts for each option
- [ ] **Space complexity**: Memory usage, object creation overhead
- [ ] **I/O analysis**: Disk reads, network calls, file operations
- [ ] **Comparison table**: Side-by-side performance comparison of options

**Example:**
```markdown
| Option | Disk I/O | Memory | Time Complexity |
|--------|----------|--------|-----------------|
| A: Copy files per-week | 340 copies/sim | Low | O(weeks × files) |
| B: Direct folder refs | 0 copies | Low | O(1) |
| C: Pre-load all data | 17 reads/init | High | O(weeks) at init |

**Recommendation:** Option C - Higher complexity but 20× fewer disk reads per simulation.
```

**User preference principle:** Increased complexity is acceptable if it improves efficiency. Prioritize:
1. Runtime performance (time efficiency)
2. Memory efficiency (space efficiency)
3. Code simplicity (acceptable to sacrifice for performance)

### Step 2.6: Create Dependency Map

Create a visual dependency map showing how the feature connects to existing code:

```
## Dependency Map

### Module Dependencies
```
┌─────────────────────────────────────────────────────────────┐
│ run_accuracy_simulation.py (entry point)                    │
│     │                                                       │
│     ▼                                                       │
│ AccuracySimulationManager                                   │
│     │                                                       │
│     ├──► ConfigGenerator (shared/)                          │
│     │         └──► league_config.json                       │
│     │                                                       │
│     ├──► AccuracyCalculator (NEW)                           │
│     │         └──► PlayerManager                            │
│     │                   └──► players.csv                    │
│     │                                                       │
│     └──► AccuracyResultsManager (NEW)                       │
│               └──► performance_metrics.json (output)        │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow
```
Input: sim_data/YEAR/weeks/week_NN/players.csv
   ▼
PlayerManager.load_players()
   ▼
AccuracyCalculator.calculate_mae()
   ▼
AccuracyResultsManager.save_results()
   ▼
Output: simulation_configs/accuracy_optimal_*/performance_metrics.json
```
```

**Why this matters:** The dependency map helps identify:
- Which interfaces need to be verified before implementation
- Where integration points exist
- Which existing code might be affected
- Data flow from entry to output

### Step 2.6.1: Compare to Working Reference (CRITICAL)

**When implementing something similar to existing functionality**, explicitly compare your approach to the working reference implementation.

**The `max_weekly_projection` Bug Prevention Example:**

The accuracy simulation needed to score players with weekly projections. A working reference already existed: `StarterHelperModeManager`.

**What should have happened during planning:**
1. Question: "How do we score players with weekly projections?"
2. Search: Find `StarterHelperModeManager` uses `score_player(use_weekly_projection=True)`
3. **Examine initialization**: Read lines 452-453:
   ```python
   max_weekly = self.player_manager.calculate_max_weekly_projection(self.config.current_nfl_week)
   self.player_manager.scoring_calculator.max_weekly_projection = max_weekly
   ```
4. Document: "Must call `calculate_max_weekly_projection()` and set `scoring_calculator.max_weekly_projection` before calling `score_player(use_weekly_projection=True)`"
5. Add checklist item: "Verify weekly scoring initialization matches StarterHelperMode pattern"

**What actually happened:**
- Called `score_player(use_weekly_projection=True)` without setting `max_weekly_projection`
- Result: Always 0, causing warnings and incorrect normalization
- Bug slipped through because **we didn't check how the working reference does it**

**Checklist Template:**

For any feature similar to existing functionality, add these verification questions:

```markdown
## Working Reference Comparison

- [ ] Identify working reference feature: `{feature_name}`
- [ ] Read how reference initializes: `{file_path}:{line_range}`
- [ ] Document initialization steps:
  1. {step 1}
  2. {step 2}
  3. {step 3}
- [ ] Verify our approach matches these steps
- [ ] Check for any setup code that runs before main logic
- [ ] Compare our parameters/flags to reference parameters/flags
```

**When to use this:**
- "Similar to X" appears in requirements
- Reusing existing classes/methods in new contexts
- Implementing parallel version of sequential code
- Any time there's a working example to learn from

**Why this matters:** Working code is the best specification. If something already works correctly, understanding **how** it works prevents reimplementing it incorrectly.

### Step 2.7: Update specs and readme

- Add discovered context to `_specs.md` (what you learned about the codebase)
- Add dependency map to `_specs.md`
- Update `README.md` with key findings and current status
- Ensure checklist has ALL open items before proceeding

### Step 2.8: Vagueness Audit (MANDATORY)

Before Phase 3, review the specs for vague language that could be interpreted multiple ways. Vague specifications cause incomplete implementations.

**Vague Phrases to Flag:**

| Vague Phrase | Problem | Action |
|--------------|---------|--------|
| "Similar to X" / "Mirror X" | Which aspects? Structure? Methods? Constants? | Add checklist: "Document ALL patterns from X to mirror" |
| "Resume capability" / "Support resuming" | What mechanism? Detect state? Load from where? | Add checklist: "Define resume mechanism: detection + loading" |
| "Handle errors appropriately" | What errors? What handling? Log? Retry? Fail? | Add checklist: "List specific errors and their handling" |
| "Save intermediate results" | Save only, or also load on restart? | Add checklist: "Verify save AND load/resume are both implemented" |
| "Same pattern as Y" | Pattern could mean many things | Add checklist: "List specific elements of pattern Y to replicate" |
| "Support multiple X" | How many? What variations? | Add checklist: "Define exact variations of X to support" |
| "Configurable" / "Flexible" | What's configurable? Defaults? | Add checklist: "List specific configuration options" |

**Feature Pair Completeness Check:**

Many features come in pairs - if one exists, the other must too:

| If Spec Says... | Must Also Have... | Example |
|-----------------|-------------------|---------|
| "Save X" | "Load X" (and use it!) | save_intermediate → load_intermediate + call it |
| "Resume capability" | Detection + Loading + Restart logic | _detect_resume_state() + load config |
| "Mirror X" | Full pattern audit of X | Constants, structure, method locations |
| "Create config" | Load config + use it | draft_config.json → ConfigManager support |
| "Track progress" | Display progress + resume from it | ProgressTracker + resume state |
| "Optimize parameters" | Enable flags for those parameters | TEMPERATURE_WEIGHT → temperature=True |
| "Output usable as baseline/input" | Consumer validation + roundtrip test | Output folder loadable by find_baseline_config() |
| "Same format as X" | Read X's actual structure NOW | Read real file X, list all contents, document in specs |

**"Same As X" Verification (CRITICAL - Do During Planning):**

When a spec says "same as X", "same format as X", "same structure as X", or similar:

```
┌─────────────────────────────────────────────────────────────────┐
│  DO NOT WAIT FOR DEVELOPMENT TO READ X!                         │
│                                                                 │
│  During PLANNING:                                               │
│  1. READ the actual file/folder X right now                     │
│  2. LIST every file it contains                                 │
│  3. DOCUMENT the internal structure of each file                │
│  4. ADD explicit entries to the specs for EACH file             │
│  5. IDENTIFY consumers of X and their requirements              │
│                                                                 │
│  This prevents: "Same 5-JSON structure" being misinterpreted    │
│  as "5 files with data" when it actually means "6 files         │
│  (including league_config.json) with nested structure"          │
└─────────────────────────────────────────────────────────────────┘
```

**Example (from accuracy simulation failure):**
- Spec said: "Same 5-JSON structure (draft_config.json + 4 week-range files)"
- What should have happened during planning:
  1. Read an actual win-rate optimal folder
  2. Found: league_config.json, week1-5.json, week6-9.json, week10-13.json, week14-17.json
  3. Read week1-5.json structure: `{config_name, description, parameters}`
  4. Updated specs to explicitly list all 6 files and their structure
- What actually happened: Assumed "5 files" meant the spec was complete, never read actual reference

**Add Checklist Item:**
```markdown
- [ ] "Same as X" VERIFICATION: For phrase "{spec phrase}", I have:
  - [ ] Read actual file/folder X: {path}
  - [ ] Listed all files found: {list}
  - [ ] Documented internal structure of each file
  - [ ] Added explicit spec entries for EACH file
  - [ ] Identified consumers and their requirements
```

**Method Call Parameter Verification:**

When a feature involves calling existing methods with configurable parameters, verify the call signature matches the feature's intent:

| If Spec Says... | Must Verify... | Example |
|-----------------|----------------|---------|
| "Optimize parameter X" | The flag/enable for X is set to True | Optimizing MATCHUP_WEIGHT requires matchup=True |
| "Use same scoring as Mode Y" | Call uses identical flags as Mode Y | Accuracy sim should match StarterHelper flags |
| "Calculate X for players" | Method call enables all X-related options | score_player() with all relevant flags enabled |

**Example of Parameter/Flag Mismatch (from accuracy simulation):**

The spec said "Optimize these 17 parameters" including TEMPERATURE_WEIGHT, WIND_WEIGHT, MATCHUP_WEIGHT, etc. But the implementation called:
```python
scored = player_mgr.score_player(player)  # All defaults!
```

The defaults had `temperature=False`, `wind=False`, `matchup=False`, so optimizing these parameters had **no effect** - they were never used in the calculation!

**Prevention:** When a spec says "optimize parameter X", add a checklist item:
```markdown
- [ ] PARAMETER ACTIVATION: For each parameter being optimized, verify:
  - [ ] What flag/enable controls this parameter?
  - [ ] Is that flag set to True in the method call?
  - [ ] Does the call match the consuming mode's call signature?
```

**Create Vagueness Checklist Items:**

For each vague phrase found, add a checklist item:
```markdown
## Vagueness Resolution

- [ ] "Similar to SimulationManager.py" - Document specific patterns to mirror:
  - [ ] What constants defined at top of file?
  - [ ] What methods correspond to which?
  - [ ] What is the resume mechanism?
- [ ] "Resume capability via intermediate folders" - Define complete mechanism:
  - [ ] How is resume state detected on startup?
  - [ ] Where is state loaded from?
  - [ ] What triggers resume vs fresh start?
```

**Why this matters:** The accuracy simulation spec said "Resume capability via intermediate folders" which was interpreted as:
- ✅ Save intermediate folders (implemented)
- ❌ Detect resume state on startup (NOT implemented)
- ❌ Load from intermediate folders (method exists but never called)

A Vagueness Audit would have caught this by asking: "What's the complete mechanism for resume capability?"

---

### Step 2.10: Testing Requirements Analysis (MANDATORY)

**Purpose:** Define how the feature will be validated during smoke testing and QA to catch integration bugs and UX issues.

Unit tests validate individual functions, but **integration bugs** (components not connecting properly) and **UX bugs** (confusing output, poor error messages) need explicit testing requirements.

**Real-world example:** The accuracy simulation had:
- ✅ 2296 unit tests passing (100%)
- ❌ `max_weekly_projection` never set (integration bug)
- ❌ Confusing log output (UX bug)
- ❌ Misleading progress display (UX bug)

These weren't caught because we didn't define **what good output looks like** or **how to validate integration**.

#### 2.10.1: Identify Integration Points

List all modules/systems that must interact correctly:

```markdown
## Integration Points

| Component A | Component B | Integration Mechanism | How to Verify |
|-------------|-------------|----------------------|---------------|
| AccuracyCalculator | PlayerManager | Calls score_player() with use_weekly_projection=True | Check max_weekly_projection is set before call |
| ParallelRunner | AccuracyCalculator | Passes configs to worker processes | Verify config has all required fields |
| Main script | Signal handler | Ctrl+C should exit cleanly | Test Ctrl+C during execution |
```

**For each integration point, add checklist item:**
- [ ] How does Component A call Component B? (method signature, parameters)
- [ ] What data flows between them? (structure, validation)
- [ ] What happens if integration fails? (error handling, recovery)
- [ ] How will we verify it works? (test with real data, check logs)

#### 2.10.2: Define Smoke Test Success Criteria

**Don't just check "it runs"** - define what correct output looks like:

```markdown
## Smoke Test Success Criteria

### 1. Output Validation
- [ ] MAE values in expected range (e.g., 3-10 for weekly, 50-70 for ROS)
- [ ] Compare to baseline config (variance < 10%)
- [ ] All 5 horizons produce results (not just some)
- [ ] Player counts match expected (ROS=~1800, weekly=4000-6000)

### 2. Log Quality
- [ ] No WARNING or ERROR messages in output (grep for them)
- [ ] Config identification is clear (can tell which param value being tested)
- [ ] Progress updates are meaningful (not "0/5 horizons")
- [ ] Summary shows all 5 horizon results for each config

### 3. User Experience
- [ ] Ctrl+C exits cleanly (no hanging processes)
- [ ] ETA estimates are reasonable (not wildly off)
- [ ] Progress bar updates smoothly (not stuck at 0%)
- [ ] Intermediate files are created (check folder structure)

### 4. Reference Comparison
- [ ] Run existing working feature (e.g., StarterHelperMode) to compare behavior
- [ ] Check that new feature follows same patterns (logging, initialization)
- [ ] Verify any shared code is called correctly (e.g., calculate_max_weekly_projection)
```

**Add these as checklist items for user confirmation:**
- [ ] User: What MAE values indicate success? (provide baseline for comparison)
- [ ] User: How should progress display look? (show example output)
- [ ] User: What log messages are most important? (highlight key information)

#### 2.10.3: Expected vs Actual Comparisons

Define specific values/patterns to check:

```markdown
## Expected vs Actual Validation

| Metric | Expected Value/Pattern | How to Check |
|--------|------------------------|--------------|
| ROS MAE | 50-70 range | Compare to baseline config MAE |
| Weekly MAE | 3-10 range | Compare to baseline config MAE |
| Log format | "Config: X=Y [horizon] \| Eval: Z \| MAE=..." | Grep for pattern, verify readable |
| Progress | Configs count up 1,2,3... | Watch output, verify increments |
| Warnings | 0 warnings | `grep -i warning output.log` should be empty |
```

**For each metric, ask:**
- What's the expected value/range?
- How will we measure it during smoke test?
- What's the tolerance for variance?

#### 2.10.4: Identify User-Facing Outputs

List everything the user will see/interact with:

```markdown
## User-Facing Outputs

### Console Output
- [ ] Progress display format: `Configs (each tests 5 horizons): [=>  ] 6.7% (1/15)`
- [ ] Config completion summary: Shows all 5 horizon MAE values
- [ ] Final output: Path to optimal config folder

### Files Created
- [ ] `simulation/simulation_configs/accuracy_optimal_TIMESTAMP/`
  - [ ] `draft_config.json` (ROS horizon)
  - [ ] `week1-5.json` (early season)
  - [ ] `week6-9.json` (mid season)
  - [ ] `week10-13.json` (late season)
  - [ ] `week14-17.json` (playoffs)
- [ ] `simulation/simulation_configs/accuracy_intermediate_XX_PARAM/` (per parameter)

### Error Messages
- [ ] Clear error when baseline config not found
- [ ] Clear error when data files missing
- [ ] Clear error when config invalid
```

**Add checklist items:**
- [ ] User: Review proposed log format - is this helpful?
- [ ] User: Review proposed file structure - is this what you expect?
- [ ] User: Review error messages - are they actionable?

#### 2.10.5: Plan Acceptance Testing

Define how the user will confirm it works:

```markdown
## Acceptance Testing Plan

### Manual Verification Steps
1. User runs: `python run_accuracy_simulation.py --test-values 2 --num-params 1`
2. User observes:
   - [ ] Progress updates regularly (every 20-30 seconds)
   - [ ] Config completion summaries show all 5 horizons
   - [ ] No warnings/errors in output
3. User tests Ctrl+C:
   - [ ] Press Ctrl+C during execution
   - [ ] Verify exits immediately (< 2 seconds)
   - [ ] Check no zombie processes (`ps aux | grep python`)
4. User checks output:
   - [ ] Optimal config folder created
   - [ ] All 5 horizon files present
   - [ ] MAE values are reasonable

### Comparison to Existing Feature
Run existing feature that works correctly (e.g., `run_win_rate_simulation.py`) and compare:
- [ ] Logging style similar?
- [ ] Progress display similar?
- [ ] File structure similar?
- [ ] Error handling similar?
```

**Add these to checklist:**
- [ ] User: What's your acceptance criteria? (how will you know it works?)
- [ ] User: Should we run comparison against similar feature? (which one?)
- [ ] User: How long should smoke test run? (30 seconds? 5 minutes? Full run?)

#### 2.10.6: Add Testing Checklist Items

Based on the above analysis, add specific items to `_checklist.md`:

```markdown
## Testing & Validation

- [ ] Define baseline MAE values for comparison (ROS and weekly)
- [ ] Confirm log format is readable and informative
- [ ] Verify progress display updates correctly
- [ ] Test Ctrl+C exits cleanly
- [ ] Compare behavior to StarterHelperMode (uses weekly projections correctly)
- [ ] Verify max_weekly_projection is set before scoring (check against working reference)
- [ ] Test with small dataset first (--test-values 2 --num-params 1)
- [ ] Run full smoke test and compare output to expected patterns
```

**Why this matters:** These bugs were caught **after** implementation:
- `max_weekly_projection = 0` - Would have been caught by "Compare to StarterHelperMode" check
- Confusing logs - Would have been caught by "Confirm log format is readable" review
- Misleading progress - Would have been caught by "Verify progress display updates" test

Defining testing requirements during planning ensures they're built correctly from the start.

---

### Step 2.9: Assumptions Audit (MANDATORY)

Before Phase 3, explicitly list ALL assumptions being made. Many bugs come from unstated assumptions that seem "obvious" but turn out to be wrong.

**Assumption Categories to Check:**

| Category | Questions to Ask |
|----------|------------------|
| **Data assumptions** | "The API always returns X" - have you tested edge cases? |
| **Timing assumptions** | "This will run after X" - what if order changes? |
| **Environment assumptions** | "The file will exist" - what if it doesn't? |
| **Scale assumptions** | "There won't be more than N items" - what if there are? |
| **Format assumptions** | "The data will be in format X" - what if it varies? |
| **State assumptions** | "The system will be in state X" - what if it's not? |

**Create an Assumptions Table in `_specs.md`:**

```markdown
## Assumptions

| Assumption | Basis | Risk if Wrong | Mitigation |
|------------|-------|---------------|------------|
| Players.csv has all columns | Tested locally | Script crashes | Add column validation |
| API returns data within 5s | Documentation says so | Timeout errors | Add configurable timeout |
| Week numbers are 1-17 | Current season structure | Off-by-one errors | Validate week range |
```

**For each assumption:**
1. **Basis:** Why do you believe this? (Code evidence, documentation, testing)
2. **Risk if Wrong:** What breaks if this assumption is false?
3. **Mitigation:** How will the code handle the assumption being wrong?

**Assumptions that need user confirmation:**
- Move to checklist as questions if basis is weak
- Don't assume - verify or ask

**Why this matters:** Unstated assumptions become bugs. Making them explicit allows:
- Challenging them during planning
- Adding defensive code during implementation
- Documenting limitations for future maintainers

---

## Phase 3: Report and Pause

```
╔═══════════════════════════════════════════════════════════════════╗
║  ⛔ MANDATORY FULL STOP - DO NOT PROCEED WITHOUT USER APPROVAL ⛔  ║
╚═══════════════════════════════════════════════════════════════════╝
```

**This is a checkpoint.** You MUST:
1. Present your findings to the user
2. Wait for explicit user direction
3. **DO NOT** start Phase 4 automatically

### Step 3.1: Summarize understanding

Present to the user:
1. **Feature Summary:** One paragraph explaining what will be built
2. **Key Findings:** What you learned from investigating the codebase
3. **Files Affected:** List of files that will likely need changes
4. **Scope:** What's in scope vs out of scope

### Step 3.2: Present open questions

List all checklist items that need resolution:
```
## Open Questions ({count} items)

### API/Data Source
- [ ] Question 1
- [ ] Question 2

### Algorithm/Logic
- [ ] Question 3

### Architecture
- [ ] Question 4
```

### Step 3.3: Ask user for direction

Present two options:
> "Would you like to:
> 1. **Add more items** to the checklist before we start?
> 2. **Start addressing** specific checklist items?
>
> If starting, which item would you like to address first? You can either:
> - **Direct me to investigate** (I'll research and propose an answer)
> - **Provide the answer directly** (if you already know what you want)"

```
┌─────────────────────────────────────────────────────────────────┐
│  🛑 STOP HERE - WAIT FOR USER RESPONSE                          │
│                                                                 │
│  Do NOT proceed to Phase 4 until user explicitly directs you.  │
│  The user must choose: add items OR start addressing items.    │
└─────────────────────────────────────────────────────────────────┘
```

---

## Phase 4: Iterative Resolution

**Goal:** Systematically resolve all checklist items with user guidance.

### One Question at a Time Pattern

**IMPORTANT:** Present and resolve questions ONE at a time, not in batches.

**Why this pattern works:**
- User can focus on one decision at a time
- Allows for follow-up questions and clarifications per item
- User can add requirements or constraints as they arise
- Creates natural checkpoints for progress tracking
- Easier to course-correct early if a decision is wrong

**Anti-pattern to avoid:** Presenting all questions at once and asking user to answer them all - this is overwhelming and doesn't allow for iterative refinement.

**Correct flow:**
```
1. Present question with options and analysis
2. Wait for user decision
3. Update checklist and specs with resolution
4. Move to next question
5. Repeat until all items resolved
```

### When user says "Investigate {item}"

1. **Research** the codebase for relevant information
2. **Analyze** options and trade-offs
3. **Propose** an answer with reasoning
4. **Wait** for user confirmation before marking resolved

### When user provides an answer

1. **Acknowledge** the answer
2. **IMMEDIATELY update both files:**
   - **Update `_specs.md`** with the resolved detail in the appropriate section
   - **Mark checklist item `[x]`** in `_checklist.md` with resolution summary
3. **Update `README.md`** if the answer affects scope or key context

**CRITICAL:** Update BOTH files after EACH answer, not at end of session.
- Specs should never contain "Open Questions" that have been resolved
- If a question in specs is answered, move it from "Open Questions" to "Resolved Implementation Decisions"
- This ensures continuity if session is interrupted

**Anti-pattern:** Updating only checklist during Phase 4, leaving specs outdated

### After each resolution

Report current status:
> "Resolved: {item description}
>
> Remaining open items: {count}
> - {next item 1}
> - {next item 2}
>
> Which item would you like to address next?"

### After Each Resolution (CRITICAL - Do Immediately)

**IMPORTANT:** Update the checklist file AFTER EACH ANSWER, not at end of session.

1. Mark item [x] in checklist with resolution details
2. Update "Progress: X/Y questions resolved" in Resolution Log
3. Write file to disk (changes persist)
4. Then move to next question

**Why this matters:** Session interruptions (compacting, terminal crash) will lose all progress if checklist isn't updated incrementally. User will have to repeat all decisions with next agent.

**Anti-pattern:** Waiting until end of session to batch-update checklist.

### Continue until all items resolved

Repeat the investigate/answer cycle until checklist is complete.

**Output:** All checklist items marked `[x]`, specs file complete, README shows "Ready for Implementation".

---

## File Templates

**All templates are in `templates.md`.** Reference that file when creating feature files.

| Template | When to Create | Purpose |
|----------|----------------|---------|
| `README.md` | Phase 1 | Context for future agents |
| `{feature_name}_specs.md` | Phase 1 | Detailed specification |
| `{feature_name}_checklist.md` | Phase 1 | Track open questions |
| `{feature_name}_lessons_learned.md` | Phase 1 | Capture process improvements |

### Folder Structure

```
feature-updates/{feature_name}/
├── README.md                           # Context for future agents
├── {feature_name}_notes.txt            # Original scratchwork (moved)
├── {feature_name}_specs.md             # Main specification
├── {feature_name}_checklist.md         # Requirements checklist
└── {feature_name}_lessons_learned.md   # Issues to improve guides
```

---

## Guiding Principles

### 1. Agent Investigates, User Decides

The agent's role is to:
- Research and surface questions
- Investigate when directed
- Propose answers with reasoning
- Document decisions made by user
- **Actively guide the conversation** with suggestions and ideas

The user's role is to:
- Direct which items to address
- Provide answers or approve agent proposals
- Decide when planning is complete

### 2. Be Proactive and Helpful

The agent should actively help guide the planning conversation:
- **Suggest options** when the user is unsure
- **Point out trade-offs** between approaches
- **Recommend** an approach when you have enough context
- **Surface related questions** the user may not have considered
- **Connect to existing patterns** in the codebase

### 3. Document Everything

When resolving a checklist item:
1. Mark it `[x]` in the checklist
2. Add full details to the `_specs.md` file
3. Update the README if it affects scope or key context
4. Add to Resolution Log in checklist

### 4. No Skipping Ahead

- Do NOT start implementation until all checklist items are resolved
- Do NOT assume answers - always confirm with user
- Do NOT proceed past Phase 3 without user direction

### 5. Be Thorough in Investigation

During Phase 2, ensure you identify:
- ALL data sources and their formats
- ALL algorithms that need definition
- ALL files that will be modified
- ALL edge cases and error conditions
- ALL integration points with existing code

---

## Conversation Prompts

**See `prompts_reference.md`** for ready-to-use conversation prompts including:
- Suggesting options when user has vague ideas
- Surfacing missing details
- Managing scope creep
- Presenting technical decisions
- Discussing edge cases
- Progress updates

---

## Best Practices (Learned from Historical Examples)

### 1. Field-Level Granularity in Checklists

Don't just ask "how do we get player data?" - break it down to individual fields:

**Good:**
```markdown
| Field | Source Known? | Notes |
|-------|---------------|-------|
| `id` | [x] | ESPN API `players[].player.id` |
| `name` | [x] | ESPN API `players[].player.fullName` |
| `bye_week` | [x] | Derived from schedule file |
| `player_rating` | [ ] | **PENDING**: How to calculate? |
```

**Bad:**
```markdown
- [ ] Figure out player data fields
```

### 2. Always Link to Existing Code

When describing implementation, reference specific files and line numbers:

**Good:**
> "Implementation Note: Reuse algorithm from `player-data-fetcher/espn_client.py:1150-1201` which already fetches schedule data."

**Bad:**
> "We'll need to fetch the schedule somehow."

### 3. Questions File Format

When asking the user questions, structure them with context, options, and recommendations:

```markdown
## Q1: {Short Title}

**Context:** {Why this decision matters}

**Question:** {The specific question}

**Options:**
1. **Option A** - {description}
   - Pros: {benefits}
   - Cons: {drawbacks}
2. **Option B** - {description}
   - Pros: {benefits}
   - Cons: {drawbacks}

**Recommendation:** Option {X} because {reasoning}

**Your Answer:** {filled in by user}
```

### 4. Track Data Source Verification

Create a summary table showing what's verified vs pending:

```markdown
## Data Source Summary

| Data | Source | Status |
|------|--------|--------|
| Player weekly points | ESPN API `appliedTotal` | ✓ Verified |
| Schedule data | ESPN Scoreboard API | ✓ Verified |
| Weather data | Open-Meteo API | ⏳ Needs verification |
```

### 5. Document Resolution Logic

For complex decisions (like the "week column logic" example), document the full resolution:

```markdown
**Week Column Logic (RESOLVED):**
For `week_XX/players.csv` (file created at Week X):
- **Bye week:** Always `0`
- **Week < X:** Actual points from ESPN API (`statSourceId=0`)
- **Week >= X:** Projected points from ESPN API (`statSourceId=1`)
```

---

## Good vs Bad Planning Examples

### Good Planning: Thorough Investigation

```markdown
## Output: players.csv

**File-level decisions:**
- [x] Data source → ESPN Fantasy API (bulk request with `scoringPeriodId=0`)
- [x] Format → CSV with headers

**Fields:**

| Field | Source Known? | Notes |
|-------|---------------|-------|
| `id` | [x] | ESPN API `players[].player.id` |
| `name` | [x] | ESPN API `players[].player.fullName` |
| `fantasy_points` | [x] | Sum of `week_N_points` columns |
| `player_rating` | [x] | Week 1: draft rank; Week 2+: points ranking |

**Questions:**
- [x] How to handle players with no data? → Skip entirely
- [x] Include free agents? → Yes, if they have any points

**Implementation Note:** Reuse parsing logic from `historical_data_compiler/player_data_fetcher.py:190-261`
```

### Bad Planning: Vague and Incomplete

```markdown
## Players File

- Need to get player data from ESPN
- Should include all the fields
- Not sure about rankings
- Will figure out edge cases during implementation
```

---

## When Planning is Complete

A feature is ready for implementation when:

1. **All checklist items** are marked `[x]`
2. **Specs file** has complete implementation details for each item
3. **README** shows status "Ready for Implementation"
4. **Lessons learned file** is created (will be populated during development)
5. **User confirms** planning is complete

### Planning Completion Checklist

Before transitioning to development, verify ALL items in this checklist:

```
┌─────────────────────────────────────────────────────────────────┐
│  PLANNING COMPLETION CHECKLIST - VERIFY BEFORE HANDOFF          │
└─────────────────────────────────────────────────────────────────┘

SPECIFICATIONS
□ All checklist items are [x] (none pending)
□ _specs.md has implementation details for EVERY checklist item
□ No "Alternative:" or "OR" notes remain unresolved
□ No "TBD" or "TODO" placeholders in specs

DEPENDENCIES
□ All files to modify are listed in specs
□ All new files to create are listed in specs
□ Required external modules/imports identified
□ Data model dependencies documented

INTEGRATION
□ Entry point identified (which script/command triggers feature)
□ Exit point identified (what output/state change occurs)
□ Interaction with existing features documented

EDGE CASES
□ Error scenarios documented with expected behavior
□ Empty/null input handling specified
□ Boundary conditions identified

STATUS
□ README shows "Ready for Implementation"
□ User explicitly confirmed planning is complete
```

**If ANY item is unchecked:** Resolve it before proceeding to development. Each gap will surface during verification iterations, costing more time than resolving it now.

**Transition to Implementation:**

When the user says "Prepare for updates based on {feature_name}":
1. Follow `feature-updates/guides/feature_development_guide.md` workflow
2. Read `{feature_name}_specs.md` as the primary specification
3. Create TODO file in `feature-updates/{feature_name}/`
4. Begin verification iterations per `feature_development_guide.md`
5. Update `{feature_name}_lessons_learned.md` throughout development when issues are found

---

## Quick Reference

| Phase | Agent Action | User Action |
|-------|--------------|-------------|
| 1 | Create folder, move notes, create initial files (including lessons learned) | - |
| 2 | Research codebase, populate checklist with questions | - |
| 3 | Report findings, present questions, ask for direction | Choose: add items or start addressing |
| 4 | Investigate items OR document user answers | Direct investigation or provide answers |
| Done | - | Say "Prepare for updates based on {feature_name}" |
| Dev | Update lessons learned when issues found | - |
| Final | Apply lessons learned to update guides | Approve guide updates |

---

## Related Guides

| Guide | When to Use | Link |
|-------|-------------|------|
| **Development Guide** | After planning is complete, user says "Prepare for updates" | `feature_development_guide.md` |
| **Prompts Reference** | Ready-to-use conversation prompts for user discussions | `prompts_reference.md` |
| **Templates** | File templates for creating feature files | `templates.md` |
| **Guides README** | Overview of all guides and when to use each | `README.md` |

### Transition Points

**From this guide → Development Guide:**
- All checklist items are `[x]` (resolved)
- `_specs.md` has complete implementation details
- README shows "Ready for Implementation"
- User says "Prepare for updates based on {feature_name}"

**Back to this guide from Development Guide:**
- If major scope changes needed during implementation
- If new requirements discovered that need user planning decisions

---

*This guide complements `feature_development_guide.md`. Use this for planning phases, then transition to the development guide for implementation.*
