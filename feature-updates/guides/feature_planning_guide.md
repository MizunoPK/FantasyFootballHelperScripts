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

## Workflow Overview

```
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
  □ Read and analyze _notes.txt thoroughly
  □ Research codebase (patterns, files to modify, similar features)
  □ Populate checklist with ALL open questions by category
  □ Update _specs.md with discovered context
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

### Step 2.3.1: Include Performance Analysis

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

### Step 2.4: Update specs and readme

- Add discovered context to `_specs.md` (what you learned about the codebase)
- Update `README.md` with key findings and current status
- Ensure checklist has ALL open items before proceeding

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
2. **Update `_specs.md`** with the resolved detail
3. **Mark checklist item `[x]`** as done
4. **Update `README.md`** if the answer affects scope or key context

### After each resolution

Report current status:
> "Resolved: {item description}
>
> Remaining open items: {count}
> - {next item 1}
> - {next item 2}
>
> Which item would you like to address next?"

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
