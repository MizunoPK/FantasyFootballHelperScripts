# Feature Creation Guide

**Purpose:** Initial feature setup, broad reconnaissance, and sub-feature breakdown decision.

**Use this guide when:** User says "Help me develop the {feature_name} feature"

**Next guide:** After completing this guide, transition to `feature_deep_dive_guide.md` for detailed planning of each sub-feature.

---

## Quick Overview

This guide helps you:
1. Set up the feature folder structure
2. Conduct broad codebase reconnaissance
3. **Decide if the feature should be broken into sub-features**
4. Create appropriate file structure (single feature OR sub-features)
5. Transition to deep dive planning

**Key Decision Point:** Phase 3 determines if this is a single feature or needs breakdown into multiple sub-features.

---

## When to Use This Guide

**Use when user says:**
- "Help me develop the {feature_name} feature"
- "I want to plan {feature_name}"
- "Let's work on the {feature_name} specification"

**Do NOT use for:**
- Bug fixes (use standard workflow)
- Simple changes that don't require planning
- Resuming existing feature work (read that feature's README.md first)

---

## Workflow Overview

```
Phase 1: Initial Setup
  Create folder, move notes, create README.md
                ↓
Phase 2: Broad Reconnaissance
  Read notes, identify major components, estimate scope
                ↓
Phase 3: Sub-Feature Breakdown Decision ⚠️ CRITICAL CHECKPOINT
  Evaluate complexity → Single feature OR multiple sub-features?
                ↓
Phase 4: Create File Structure
  Single: Create spec + checklist
  OR
  Multi: Create SUB_FEATURES_README.md + per-sub-feature spec/checklist
  ALWAYS: Create research/ subfolder
                ↓
Phase 5: Transition to Deep Dive
  Move to feature_deep_dive_guide.md
```

---

## Phase 1: Initial Setup

**Goal:** Create feature folder and basic README

### Step 1.1: Create folder and move notes

```bash
mkdir -p feature-updates/{feature_name}/
mv feature-updates/{feature_name}.txt feature-updates/{feature_name}/{feature_name}_notes.txt
```

### Step 1.2: Create README.md

Use the template from `templates.md` but with this Agent Status section:

```markdown
## AGENT STATUS (Read This First)

**Current Phase:** CREATION
**Current Step:** Phase 1 - Initial Setup
**Next Action:** Broad reconnaissance to determine scope

### WHERE AM I RIGHT NOW?

Current Phase:  [x] CREATION  [ ] DEEP_DIVE  [ ] IMPLEMENTATION  [ ] COMPLETE
Current Step:   Phase 1 - Initial setup complete
Next Action:    Phase 2 - Broad reconnaissance
Last Activity:  [Date] - Created feature folder and README
```

### Step 1.3: Update README status

Mark Phase 1 complete in the README:
```markdown
**Current Step:** Phase 1 complete - ready for reconnaissance
```

---

## Phase 2: Broad Reconnaissance

**Goal:** Understand the feature at a high level and estimate complexity

**IMPORTANT:** This is NOT deep research. You're doing a quick scan to understand scope, not solving all problems.

### Step 2.1: Read notes thoroughly

- Understand user's intent
- Identify key requirements
- Note any explicit constraints or preferences

### Step 2.2: Identify major components affected

**Quick searches to find:**
- Which managers/classes will change?
- Which modules/subsystems are involved?
- Are there similar existing features to reference?

**Example findings:**
- "Affects PlayerManager, FantasyTeam, and 3 mode managers"
- "Similar to existing CSV loading but for JSON"
- "Touches data layer, business logic, and UI display"

### Step 2.3: Estimate rough scope

**Ask yourself:**
- How many major components affected? (1-2 / 3-5 / 6+)
- Rough implementation items? (<20 / 20-50 / 50+)
- Single subsystem or multiple independent parts?
- Different risk levels for different parts?

**Tag the feature:**
- **SMALL:** 1-2 components, <20 items, straightforward
- **MEDIUM:** 3-5 components, 20-50 items, some complexity
- **LARGE:** 6+ components, 50+ items, high complexity

### Step 2.4: Update README

Add findings to README:

```markdown
## Broad Reconnaissance Findings

**Components Affected:**
- [Component 1]
- [Component 2]
- ...

**Rough Scope Estimate:** SMALL / MEDIUM / LARGE

**Similar Features:** [Existing features that do similar things]

**Initial Complexity Assessment:**
- Estimated items: ~X
- Major subsystems: Y
- Risk level: LOW / MEDIUM / HIGH
```

---

## Phase 3: Sub-Feature Breakdown Decision

**⚠️ CRITICAL CHECKPOINT - This decision affects the entire workflow**

### Evaluation Criteria

**Break into sub-features if ANY of these apply:**

1. **Multiple major components:** Affects 3+ managers, modes, or subsystems
2. **Large scope:** Estimated 30+ implementation items
3. **Independent subsystems:** Parts can be developed/tested separately
4. **Mixed risk levels:** Some parts high-risk, others low-risk
5. **Different skill areas:** Database + UI + API in one feature
6. **User explicitly requests:** "Can we break this into smaller pieces?"

**Keep as single feature if ALL of these apply:**

1. **Single component:** Affects 1-2 related classes
2. **Small scope:** <20 implementation items
3. **Tightly coupled:** Changes can't be separated
4. **Low complexity:** Straightforward implementation

### Step 3.1: Make recommendation

**If recommending breakdown:**

```markdown
## Sub-Feature Breakdown Recommendation

**Reasoning:**
- Affects 5+ major components
- Estimated 60+ implementation items
- Contains independent subsystems (data loading, UI updates, validation)

**Proposed Sub-Features:**

1. **Core Data Loading** (estimated 20 items)
   - Scope: JSON loading, field mapping
   - Dependencies: None (foundation)
   - Risk: MEDIUM

2. **UI Integration** (estimated 15 items)
   - Scope: Display updates, user interaction
   - Dependencies: Sub-feature 1
   - Risk: LOW

3. **Validation & Error Handling** (estimated 10 items)
   - Scope: Data validation, error messages
   - Dependencies: Sub-feature 1
   - Risk: LOW

**Benefits:**
- Each sub-feature tested independently
- Parallel development possible
- Clear progress tracking
- Reduced risk through smaller units
```

Present to user and **WAIT for approval**.

**If keeping single feature:**

```markdown
## Single Feature Approach

**Reasoning:**
- Affects 2 components
- Estimated 15 items
- Tightly coupled changes
- Straightforward implementation

Proceeding with single spec and checklist.
```

---

## Phase 4: Create File Structure

### Option A: Single Feature Structure

If keeping as single feature:

```bash
feature-updates/{feature_name}/
├── README.md (already created)
├── {feature_name}_notes.txt (already exists)
├── {feature_name}_specs.md (CREATE NOW)
├── {feature_name}_checklist.md (CREATE NOW)
├── {feature_name}_lessons_learned.md (CREATE NOW)
└── research/ (CREATE NOW - for any research documents)
```

**Create files:**
- `{feature_name}_specs.md` - Use template from templates.md
- `{feature_name}_checklist.md` - Empty, will populate during deep dive
- `{feature_name}_lessons_learned.md` - Use template from templates.md
- `research/` folder - For any analysis documents created during deep dive

### Option B: Sub-Feature Structure

If breaking into sub-features:

```bash
feature-updates/{feature_name}/
├── README.md (already created)
├── {feature_name}_notes.txt (already exists)
├── SUB_FEATURES_README.md (CREATE NOW - master overview)
├── {feature_name}_lessons_learned.md (CREATE NOW)
├── sub_feature_01_{descriptive_name}_spec.md (CREATE for EACH)
├── sub_feature_01_{descriptive_name}_checklist.md (CREATE for EACH)
├── sub_feature_02_{descriptive_name}_spec.md
├── sub_feature_02_{descriptive_name}_checklist.md
├── ...
└── research/ (CREATE NOW - shared research folder)
```

**IMPORTANT:** No global spec or checklist file - only sub-feature specific files.

**Create SUB_FEATURES_README.md:**

```markdown
# Sub-Feature Breakdown: {Feature Name}

## Overview
[Brief description of overall feature]

## Sub-Features

| Sub-Feature | Items | Dependencies | Risk | Priority |
|-------------|-------|--------------|------|----------|
| 1. [Name] | ~X | None | [RISK] | [PRIORITY] |
| 2. [Name] | ~Y | Sub-feature 1 | [RISK] | [PRIORITY] |
| ... | | | | |

## Implementation Order

**Recommended sequence:**
1. Sub-feature 1 (foundation)
2. Sub-feature 2 (depends on 1)
3. ...

## Progress Tracking

- [ ] Sub-feature 1: [Name] - Deep Dive
- [ ] Sub-feature 1: [Name] - Implementation
- [ ] Sub-feature 2: [Name] - Deep Dive
- [ ] Sub-feature 2: [Name] - Implementation
- ...

## Dependencies

[Explain dependency relationships between sub-features]
```

**Create per-sub-feature files:**

For each sub-feature, create:
- `sub_feature_{N}_{name}_spec.md` with initial scope
- `sub_feature_{N}_{name}_checklist.md` (empty, populate during deep dive)

**Example initial spec:**

```markdown
# Sub-Feature {N}: {Descriptive Name}

## Objective
[What this sub-feature accomplishes]

## Scope
[What's included in THIS sub-feature]

## Dependencies
**Prerequisites:** [Which sub-features must complete first]
**Blocks:** [Which sub-features depend on this one]

## Initial Estimates
- Implementation items: ~X
- Risk level: LOW/MEDIUM/HIGH
- Priority: LOW/MEDIUM/HIGH

## Files Likely Affected
- [File 1]
- [File 2]
- ...

[Rest will be filled during deep dive]
```

### Create research/ folder (BOTH options)

```bash
mkdir research/
```

Create `research/README.md`:

```markdown
# Research and Analysis Documents

This folder contains all research, analysis, and verification reports.

**Purpose:**
- Keeps root folder clean (only specs, checklists, README)
- Centralizes reference material
- Clear separation: specs = implementation guidance, research = context

**File Naming:**
- `{TOPIC}_ANALYSIS.md` - Detailed analysis of specific topic
- `VERIFICATION_REPORT_{DATE}.md` - Verification findings
- `RESEARCH_FINDINGS_{DATE}.md` - General research results

**All research documents go here from the start.**
```

---

## Phase 5: Transition to Deep Dive

### Step 5.1: Update README status

**For single feature:**
```markdown
**Current Phase:** DEEP_DIVE
**Current Step:** Ready to begin detailed planning
**Next Action:** Follow feature_deep_dive_guide.md
**Structure:** Single feature approach
```

**For sub-features:**
```markdown
**Current Phase:** DEEP_DIVE
**Current Step:** Ready to begin sub-feature 1 deep dive
**Next Action:** Follow feature_deep_dive_guide.md for sub-feature 1
**Structure:** {N} sub-features (see SUB_FEATURES_README.md)
```

### Step 5.2: Confirm files created

**Single feature checklist:**
- [x] README.md with Agent Status
- [x] {feature_name}_specs.md (initial)
- [x] {feature_name}_checklist.md (empty)
- [x] {feature_name}_lessons_learned.md
- [x] research/ folder
- [x] research/README.md

**Sub-feature checklist:**
- [x] README.md with Agent Status
- [x] SUB_FEATURES_README.md (overview)
- [x] sub_feature_{N}_{name}_spec.md for EACH sub-feature
- [x] sub_feature_{N}_{name}_checklist.md for EACH sub-feature
- [x] {feature_name}_lessons_learned.md (shared)
- [x] research/ folder
- [x] research/README.md

### Step 5.3: Announce transition

**For single feature:**
```
Feature structure created. Starting detailed planning.

Following feature_deep_dive_guide.md for complete specification development.
```

**For sub-features:**
```
Sub-feature structure created with {N} sub-features.

Starting deep dive for Sub-feature 1: {Name}

Following feature_deep_dive_guide.md. Will complete deep dive for ALL sub-features
before proceeding to implementation.
```

---

## Common Mistakes to Avoid

| Mistake | Why It's Bad | Prevention |
|---------|--------------|------------|
| Skipping breakdown decision | Large features become unmanageable | Always evaluate at Phase 3 |
| Breaking down too early | Adds complexity for simple features | Use triggers: 3+ components, 30+ items |
| Creating global spec with sub-features | Confusion about what to follow | Only sub-feature files when using breakdown |
| Not creating research/ folder | Documents scattered at root | Create research/ in Phase 4 |
| Deep diving during reconnaissance | Wastes time before breakdown decision | Keep Phase 2 broad and quick |
| Guessing at sub-feature divisions | Poor boundaries cause conflicts | Base on actual component boundaries |

---

## Next Steps

After completing this guide, you will have:
- [x] Feature folder created
- [x] Appropriate file structure (single OR sub-features)
- [x] research/ folder ready for analysis documents
- [x] README with current status

**NEXT:** Transition to `feature_deep_dive_guide.md`

**For single feature:** Execute deep dive guide once

**For sub-features:** Execute deep dive guide once per sub-feature, then do cross-sub-feature alignment review before implementation
