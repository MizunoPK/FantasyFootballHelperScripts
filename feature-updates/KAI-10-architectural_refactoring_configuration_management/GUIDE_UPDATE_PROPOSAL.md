# Guide Update Proposal: KAI-10 — architectural_refactoring_configuration_management

**Created:** 2026-02-18
**Epic:** KAI-10 (architectural_refactoring_configuration_management)
**Lessons Analyzed:**
- epic_lessons_learned.md — 5 lessons with guide improvement recommendations (S2 section)
- feature_01_refactor_player_data_fetcher/lessons_learned.md — 1 guide improvement identified
- feature_02 through feature_08/lessons_learned.md — all empty templates (features never implemented)

**Total Lessons Analyzed:** 6 lessons with guide impact
**Total Proposals:** 6

| Priority | Count | Proposals |
|----------|-------|-----------|
| P0 (Critical) | 0 | — |
| P1 (High) | 4 | P1-1, P1-2, P1-3, P1-4 |
| P2 (Medium) | 2 | P2-1, P2-2 |
| P3 (Low) | 0 | — |

**Recommendation:** All 4 P1 proposals address concrete workflow problems observed during KAI-10.
The 2 P2 proposals are meaningful improvements to parallel work UX.

---

## P1 Proposals (High Priority)

---

### Proposal P1-1: Add Epic Size Limit Recommendation to S1 Epic Planning

**Lesson Learned:**
> "I have found that this epic is too large and unwieldy. Add to lessons learned that if an epic
> is looking at having more than 5 features, then the agent should suggest breaking the epic up
> into smaller epics."

**Source:** User instruction + feature_01_refactor_player_data_fetcher/lessons_learned.md
(Guide Improvements Identified section + Recommendations #1)

**Root Cause:**
KAI-10 was scoped at 8 features. This made it too large to complete in a single epic lifecycle:
sessions ran out of context, the epic was abandoned mid-execution, and the remaining 7 features
had to be broken into new epic request files. No guide warned the agent at S1 planning time that
8 features was an unusually large scope that should prompt a split conversation with the user.

**Affected Guide:** `stages/s1/s1_epic_planning.md`

**Current State (BEFORE):**
The guide contains a scope assessment table (around line 348) that categorizes epics:
```
SMALL (1-2 features)
MEDIUM (3-5 features)
LARGE (6+ features)
```
There is no guidance to suggest splitting when the feature count is large.

**Proposed Change (AFTER):**
Add a scope limit check immediately after the Initial Scope Assessment section:

```markdown
### 🚨 Epic Size Check

**If the epic has more than 5 features, stop and discuss with the user before proceeding.**

An epic with 6+ features is likely too large to complete in a single epic lifecycle:
- Sessions run out of context mid-execution, causing continuity problems
- Multiple agents across many features accumulate coordination overhead
- The user often loses track of overall progress
- Later features frequently don't get implemented before the epic is abandoned

**Recommended conversation:**
> "This epic appears to have {N} features, which exceeds the recommended maximum of 5.
> I suggest splitting it into two epics:
> - Epic A: Features 1-{M} (Wave 1 — foundational work)
> - Epic B: Features {M+1}-{N} (Wave 2 — dependent/extended work)
>
> This keeps each epic manageable and improves completion likelihood.
> Would you like to split, or proceed with all {N} features in one epic?"

**If user chooses to proceed with 6+ features:** Document the decision in EPIC_README.md
and acknowledge the increased risk of context compaction during execution.
```

**Rationale:**
The check gives the agent a concrete trigger (>5 features) and a scripted conversation to have
with the user. It preserves user agency (they can still proceed) while surfacing the risk before
any work begins.

**Impact Assessment:**
- Who benefits: All agents starting epic planning for large feature sets
- When it helps: S1 Step 5 — before any specs are created
- Severity if unfixed: Agent and user invest many hours before discovering the epic is
  unmanageable; features get abandoned mid-epic; work must be restructured into new epics

**User Decision:** [ ] Approve  [ ] Modify  [ ] Reject  [ ] Discuss

**User Feedback/Modifications:**
```
{User writes response here}
```

---

### Proposal P1-2: Fix Outdated Parallel Work Coordination Paths

**Lesson Learned:**
> "The parallel work guides reference a coordination directory structure under
> `parallel_work/coordination/` with `agent_checkpoints/` using `.md` files and
> `inboxes/` with per-agent subdirectories. CLAUDE.md mandates a different structure
> (and overrides guide content): `.epic_locks/`, `agent_comms/` (flat .md files),
> `agent_checkpoints/` (.json files). Key conflicts: guide uses wrong base path,
> guide uses inbox subdirectories CLAUDE.md prohibits, guide checkpoint files use .md
> extension when CLAUDE.md mandates .json."

**Source:** epic_lessons_learned.md — S2 section, "Parallel work guide coordination paths are outdated"

**Root Cause:**
The parallel work guides were written before CLAUDE.md established the canonical structure.
CLAUDE.md acts as the override, but agents reading the guide first will try to follow guide paths
that conflict with CLAUDE.md validation requirements.

**Affected Guides:**
- `parallel_work/s2_primary_agent_group_wave_guide.md` — monitoring commands reference wrong paths
- `parallel_work/s2_primary_agent_guide.md` — same issue

**Current State (BEFORE) — from s2_primary_agent_group_wave_guide.md:**
```bash
# Monitor coordination infrastructure:
ls -lt parallel_work/coordination/agent_checkpoints/

# secondary_a_checkpoint.md (Feature 02)
# secondary_b_checkpoint.md (Feature 03)
```

Also: inbox references like `inboxes/from_secondary_a/` appear in agent communication examples.

**Proposed Change (AFTER):**
Replace all `parallel_work/coordination/` path references with paths matching CLAUDE.md:

```bash
# Monitor coordination infrastructure:
ls -lt agent_checkpoints/

# secondary_a.json (Feature 02)
# secondary_b.json (Feature 03)
```

Replace inbox subdirectory references with flat file references in `agent_comms/`:
```bash
# Messages are flat files in agent_comms/:
cat agent_comms/secondary_a_to_primary.md
cat agent_comms/primary_to_secondary_a.md
```

Add a note at the top of each affected guide:
```markdown
> **Path Reference:** All coordination paths below are relative to the epic folder.
> Checkpoint files use .json extension. Communication files are flat .md files in agent_comms/.
> See CLAUDE.md "S2 Parallel Work Structure Rules" for canonical structure.
```

**Rationale:**
Aligning guide examples with CLAUDE.md eliminates the conflict between what guides teach
and what CLAUDE.md enforces. Agents won't create wrong directory structures or wrong file
extensions that then fail validation.

**Impact Assessment:**
- Who benefits: All agents using group-based or full parallel S2 work
- When it helps: During coordination infrastructure setup and monitoring
- Severity if unfixed: Agents create wrong structure, validate_structure.sh fails, agents
  waste time debugging why their structure doesn't match requirements

**User Decision:** [ ] Approve  [ ] Modify  [ ] Reject  [ ] Discuss

**User Feedback/Modifications:**
```
{User writes response here}
```

---

### Proposal P1-3: Require Recommendation for Each Checklist Question

**Lesson Learned:**
> "When agents present checklist questions to the user during S2.P1.I2 (Checklist Resolution),
> they frequently omit a recommendation and instead present all options neutrally. The correct
> pattern: Agent researches options → evaluates tradeoffs → presents all options with pros/cons
> → explicitly states which option they recommend and why → asks user to make the final decision."

**Source:** epic_lessons_learned.md — S2 section, "Checklist question presentation — always
provide a recommended answer"

**Root Cause:**
The spec creation guide (S2.P1) tells agents to present questions but does not explicitly require
them to include a recommendation. Agents default to neutral option presentation, which pushes all
analytical work onto the user instead of doing the research and forming a recommendation first.

**Affected Guide:** `stages/s2/s2_feature_deep_dive.md` (or the spec creation phase guide)

**Current State (BEFORE):**
The checklist question presentation step instructs agents to present questions and options to the
user, but does not mandate a recommendation be included.

**Proposed Change (AFTER):**
Add an explicit requirement to the checklist question presentation step:

```markdown
**🚨 MANDATORY: Include a recommendation for EVERY checklist question**

For each question you present, you MUST:
1. Research the options (read relevant code, check existing patterns)
2. Evaluate tradeoffs for each option
3. State your recommendation explicitly: "I recommend Option A because..."
4. Explain your rationale (1-2 sentences)
5. Ask the user for their decision

**Why this is required:** The agent has already done the research. Presenting options without
a recommendation forces the user to repeat that analysis unnecessarily. A recommendation does
NOT remove user agency — the user still makes the final call.

**Anti-pattern (WRONG):**
> Q1: Should we use direct import or subprocess?
> - Option A: Direct import
> - Option B: Subprocess
> Which do you prefer?

**Correct pattern:**
> Q1: Should we use direct import or subprocess?
> - **Option A (Recommended):** Direct import — matches DISCOVERY.md pattern, simpler code,
>   no working directory issues, consistent with Feature 01 precedent
> - Option B: Subprocess — keeps runner isolated but adds complexity and subprocess overhead
> I recommend Option A. What is your decision?
```

Also update the `checklist.md` template to add a "Recommendation:" field:
```markdown
**Q1:** {question text}
- Option A: {description}
- Option B: {description}
**Recommendation:** {agent's recommended option and 1-2 sentence rationale}
**Status:** PENDING
**User Answer:** {to be filled}
```

**Rationale:**
Making the recommendation mandatory transforms checklist Q&A from a passive "here are options"
exchange into an active "here is my analysis + recommendation, please decide" exchange. This
is both more efficient (user makes faster decisions) and more thorough (ensures agent actually
did the tradeoff analysis).

**Impact Assessment:**
- Who benefits: All agents doing S2.P1.I2 (Checklist Resolution); all users reviewing questions
- When it helps: Every time a checklist question is presented to the user
- Severity if unfixed: Users must do their own tradeoff analysis for every question;
  agents appear unhelpful; decisions take longer

**User Decision:** [ ] Approve  [ ] Modify  [ ] Reject  [ ] Discuss

**User Feedback/Modifications:**
```
{User writes response here}
```

---

### Proposal P1-4: Clarify Primary Agent Must Not Relay Secondary Checklist Questions

**Lesson Learned:**
> "During Wave 2 monitoring, the Primary agent collected open questions from secondary agents'
> checklist.md files and began presenting them to the user. This is incorrect behavior.
> Secondary agents present their own checklist questions directly to the user during S2.P1.I2.
> Primary agent's job during Wave 2 is to monitor progress (checkpoint freshness), handle
> escalations, and wait."

**Source:** epic_lessons_learned.md — S2 section, "Primary agent should NOT relay secondary
checklist questions to the user"

**Root Cause:**
The group wave guide's Wave 2 monitoring section does not explicitly prohibit this behavior.
The Primary agent, seeing open checklist questions in secondary agents' files, tried to be
helpful by consolidating them. This bypasses the secondary's own workflow and creates confusion
about who is responsible for Q&A.

**Affected Guide:** `parallel_work/s2_primary_agent_group_wave_guide.md`

**Current State (BEFORE):**
The monitoring section describes checking checkpoint freshness but does not explicitly state
that the Primary must NOT read secondary checklist.md files to relay questions.

**Proposed Change (AFTER):**
Add an explicit prohibition to the Wave 2 monitoring section:

```markdown
**🚨 During Wave 2 monitoring, the Primary agent MUST NOT:**
- Read secondary agents' checklist.md files to gather their open questions
- Present secondary agents' checklist questions to the user on their behalf
- Intervene in a secondary's Q&A workflow unless the secondary explicitly escalates

**What to check during monitoring:**
- ✅ Checkpoint file timestamps (freshness — is agent active?)
- ✅ STATUS files (are agents making progress?)
- ✅ agent_comms/ for escalation messages TO Primary
- ❌ NOT checklist.md files (secondary handles their own Q&A)
- ❌ NOT spec.md drafts (secondary writes their own spec)

**If a secondary agent needs to ask the user a question:**
The secondary agent asks the user directly during their S2.P1.I2 step.
If the secondary is blocked and cannot ask directly, they send an escalation message
to agent_comms/ → Primary reads it → Primary presents the escalation to the user.
This is the ONLY case where Primary relays a secondary's question.
```

**Rationale:**
The explicit prohibition prevents the anti-pattern before it starts. The "what to check"
list gives Primary a clear scope for monitoring that excludes checklist files.

**Impact Assessment:**
- Who benefits: All Primary agents coordinating Wave 2 parallel work
- When it helps: During the Wave 2 monitoring phase
- Severity if unfixed: Primary agent disrupts secondary workflows, creates confused
  Q&A chains, and may present stale or out-of-context questions to the user

**User Decision:** [ ] Approve  [ ] Modify  [ ] Reject  [ ] Discuss

**User Feedback/Modifications:**
```
{User writes response here}
```

---

## P2 Proposals (Medium Priority)

---

### Proposal P2-1: Add Wave 1 Precedent Pattern to S1 Parallelization Assessment

**Lesson Learned:**
> "Wave splitting for design precedent — use a solo Wave 1 feature to establish patterns
> before parallel Wave 2. When an epic contains multiple similar features that share a common
> implementation pattern, group them so that ONE representative feature completes S2 (and
> ideally S5-S8) first as a solo wave, before the similar features begin their S2 in parallel.
> [Details: reduces cross-feature conflicts, resolved decisions propagate to Wave 2, etc.]
> Required guide update: Add this wave-splitting strategy to s1_epic_planning.md Step 5
> as a named option: 'Wave 1 Precedent Pattern'."

**Source:** epic_lessons_learned.md — S2 section, "Wave splitting for design precedent"

**Root Cause:**
The S1 parallelization section offers "group-based" and "full parallel" options but does not
describe the "Wave 1 Precedent" pattern — where one representative feature completes fully
(S5-S8) before similar features begin their S2. This pattern is especially valuable for
epics where all features implement the same architectural approach and concrete decisions
(dataclass structure, constructor signatures, arg naming) must be made once and inherited.

**Affected Guide:** `stages/s1/s1_epic_planning.md` — Step 5 parallelization assessment

**Current State (BEFORE):**
The parallelization options are:
- Group-based S2 (dependency-based wave groups)
- Full parallel S2 (all features independent)
- Sequential S2 (user declined parallel)

**Proposed Change (AFTER):**
Add a third option: "Wave 1 Precedent Pattern":

```markdown
### Option 3: Wave 1 Precedent Pattern (NEW)

**When to use:**
- Epic has 3+ features all implementing the SAME architectural pattern
- Pattern requires upfront decisions with multiple valid options (e.g., dataclass vs pydantic,
  subprocess vs direct import, arg naming conventions)
- Features are code-independent (no import/dependency chain between them)

**Pattern:**
- Wave 1: ONE representative feature completes S2 + S5 + S6 + S7 + S8 SOLO
  - Pick the most complex or most representative feature as Wave 1
  - Explicitly document all design decisions made (class structure, constructor signatures,
    arg naming) in Wave 1's HANDOFF_PACKAGE.md as "established precedents"
- Wave 2: Remaining similar features execute S2 in parallel, each referencing Wave 1's
  spec.md and established precedents as their starting point

**Benefits:**
- Wave 1 forces concrete decisions before 6+ parallel agents each make different choices
- Wave 2 handoffs say "use the same pattern as Feature 01" — simpler than re-speccing
- Checklist questions resolved in Wave 1 often don't need re-asking in Wave 2
- S3 cross-feature conflicts are greatly reduced (Wave 2 already aligned to Wave 1)

**Offer to user when:**
> "This epic has {N} similar features all implementing the same pattern.
> I suggest a 'Wave 1 Precedent' approach: Feature 01 executes fully first to establish
> design decisions, then Features 02-0N execute S2 in parallel using Feature 01 as a template.
> This reduces conflicts and gives each Wave 2 feature a concrete starting point.
> Would you like to use this approach?"
```

**Rationale:**
KAI-10 used this pattern by design — Feature 01 was the sole Wave 1 feature. Adding it as a
named option in the S1 guide means future agents will recognize and offer this pattern rather
than defaulting to full parallelization where design decisions collide.

**Impact Assessment:**
- Who benefits: Agents planning epics with 3+ features using the same architectural pattern
- When it helps: S1 Step 5 (parallelization assessment)
- Severity if unfixed: Agents default to full parallelization, multiple agents make
  inconsistent design decisions, S3 cross-feature conflicts require rework

**User Decision:** [ ] Approve  [ ] Modify  [ ] Reject  [ ] Discuss

**User Feedback/Modifications:**
```
{User writes response here}
```

---

### Proposal P2-2: Make Secondary Agents Self-Locating from Minimal Startup Instruction

**Lesson Learned:**
> "The current parallel work guides require the Primary to write a verbose one-liner startup
> instruction containing the full handoff package path. The user wants secondary agents to need
> only a minimal instruction like 'You are a secondary agent for epic KAI-10 for feature 02'.
> The secondary agent should be able to derive everything from that alone: look up KAI-10
> in feature-updates/, find feature_02_*/HANDOFF_PACKAGE.md by matching feature number,
> read the handoff package to get full context and instructions."

**Source:** epic_lessons_learned.md — S2 section, "Secondary agent startup UX — handoff
packages should be self-locating"

**Root Cause:**
The current guide requires Primary to construct a detailed startup instruction including the
full handoff package path. This is brittle (Primary can get the path wrong) and verbose.
The HANDOFF_PACKAGE.md files already live in each feature folder — a minimal instruction
containing epic + feature number is sufficient for a secondary to locate them.

**Affected Guides:**
- `parallel_work/s2_primary_agent_guide.md` — "Present Handoffs to User" step
- `parallel_work/s2_primary_agent_group_wave_guide.md` — same step
- `parallel_work/s2_secondary_agent_guide.md` — "Getting Started" step

**Current State (BEFORE):**
Primary generates verbose startup instruction that includes full handoff package path.
Secondary agent guide does not describe self-location behavior.

**Proposed Change (AFTER):**

In **s2_primary_agent_guide.md** and **s2_primary_agent_group_wave_guide.md**,
the "Present Handoffs to User" step changes:

```markdown
**Startup instructions for user to give to each secondary agent:**

For each secondary, give the user this short instruction (fill in N and feature number):
> "You are a secondary agent for KAI-{N} for feature {X}."

That is all the user needs to say. The secondary agent will locate the handoff package
automatically from the epic number and feature number.

(The full HANDOFF_PACKAGE.md is already saved to feature_{X}_{name}/HANDOFF_PACKAGE.md
and the secondary will find it on their own.)
```

In **s2_secondary_agent_guide.md**, add as Step 0 before any other steps:

```markdown
## Step 0: Self-Location (if given minimal startup instruction)

If your startup instruction is simply "You are a secondary agent for KAI-{N} for feature {X}":

1. Search for the epic folder: `Glob pattern="KAI-{N}-*" path="feature-updates/"`
2. Find your feature: `Glob pattern="feature_{X}_*/HANDOFF_PACKAGE.md" path="feature-updates/KAI-{N}-{epic_name}/"`
3. Read the HANDOFF_PACKAGE.md — it contains all context and instructions
4. Proceed with S2.P1 as directed in the handoff package

This self-location works because Primary saves HANDOFF_PACKAGE.md to each feature folder
before spawning secondary agents.
```

**Rationale:**
Minimal startup instructions are less error-prone and simpler for the user to provide.
The secondary agent's self-location step is deterministic — KAI number + feature number
uniquely identify the handoff package.

**Impact Assessment:**
- Who benefits: Users spawning secondary agents; Primary agents writing startup instructions
- When it helps: At the start of each secondary agent session
- Severity if unfixed: Primary agents write verbose paths that may be wrong; user experience
  is more complex than necessary

**User Decision:** [ ] Approve  [ ] Modify  [ ] Reject  [ ] Discuss

**User Feedback/Modifications:**
```
{User writes response here}
```

---

## Decision Summary

| ID | Title | Priority | Decision |
|----|-------|----------|---------|
| P1-1 | Epic size limit recommendation (>5 features → suggest split) | P1 | ✅ Approved — Applied |
| P1-2 | Fix outdated parallel work coordination paths | P1 | ✅ Approved — Applied |
| P1-3 | Require recommendation for each checklist question | P1 | ✅ Approved — Applied |
| P1-4 | Primary must not relay secondary checklist questions | P1 | ✅ Approved — Applied |
| P2-1 | Wave 1 Precedent Pattern in S1 parallelization | P2 | ✅ Approved — Applied |
| P2-2 | Secondary agents self-locate from minimal startup instruction | P2 | ✅ Approved — Applied |
