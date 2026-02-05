# Discovery Document Template

**Filename:** `DISCOVERY.md`
**Location:** `feature-updates/KAI-{N}-{epic_name}/DISCOVERY.md`
**Created:** S1.P3 (Discovery Phase)

**Purpose:** Epic-level source of truth for problem understanding, solution approach, and feature breakdown rationale. Created through iterative research and user Q&A during the Discovery Phase.

---

## Template

```markdown
# Discovery Phase: {epic_name}

**Epic:** KAI-{N}-{epic_name}
**Created:** {YYYY-MM-DD}
**Last Updated:** {YYYY-MM-DD}
**Status:** {IN_PROGRESS | COMPLETE}

---

## Epic Request Summary

{2-4 sentence summary of what the user requested. Capture the essence without interpretation.}

**Original Request:** `{epic_name}_notes.txt`

---

## Discovery Questions

{Questions identified during research that need answers. Updated throughout Discovery Loop.}

### Resolved Questions

| # | Question | Answer | Impact | Resolved |
|---|----------|--------|--------|----------|
| 1 | {Question text} | {User's answer} | {How this affects approach} | {YYYY-MM-DD} |
| 2 | {Question text} | {User's answer} | {How this affects approach} | {YYYY-MM-DD} |

### Pending Questions

| # | Question | Context | Asked |
|---|----------|---------|-------|
| {N} | {Question text} | {Why this matters} | {YYYY-MM-DD} |

{When Discovery completes, Pending Questions section should be empty.}

---

## Research Findings

{Findings from each iteration of the Discovery Loop.}

### Iteration 1 ({YYYY-MM-DD HH:MM})

**Researched:** {What was investigated}

**Files Examined:**
- `{path/to/file.py}` (lines {X-Y}): {What was found}
- `{path/to/other.py}` (lines {A-B}): {What was found}

**Key Findings:**
- {Finding 1}
- {Finding 2}
- {Finding 3}

**Questions Identified:**
- {Question arising from research}
- {Question arising from research}

---

### Iteration 2 ({YYYY-MM-DD HH:MM})

**Researched:** {What was investigated based on Iteration 1 answers}

**Files Examined:**
- {File list with findings}

**Key Findings:**
- {Finding 1}
- {Finding 2}

**Questions Identified:**
- {Question arising from research}

---

{Continue for each iteration until no new questions emerge}

### Iteration {N} ({YYYY-MM-DD HH:MM}) - FINAL

**Researched:** {What was investigated}

**Files Examined:**
- {File list}

**Key Findings:**
- {Finding 1}
- {Finding 2}

**Questions Identified:**
- None (Discovery Loop complete)

---

## Solution Options

{Potential approaches identified during research. Compare trade-offs.}

### Option 1: {Option Name}

**Description:** {How this approach would work}

**Pros:**
- {Benefit 1}
- {Benefit 2}

**Cons:**
- {Drawback 1}
- {Drawback 2}

**Effort Estimate:** {LOW | MEDIUM | HIGH}

**Fit Assessment:** {How well this fits the user's needs}

---

### Option 2: {Option Name}

**Description:** {How this approach would work}

**Pros:**
- {Benefits}

**Cons:**
- {Drawbacks}

**Effort Estimate:** {LOW | MEDIUM | HIGH}

**Fit Assessment:** {How well this fits the user's needs}

---

{Add more options as identified}

### Option Comparison Summary

| Option | Effort | Fit | Recommended |
|--------|--------|-----|-------------|
| {Option 1} | {LOW/MED/HIGH} | {GOOD/MODERATE/POOR} | {YES/NO} |
| {Option 2} | {LOW/MED/HIGH} | {GOOD/MODERATE/POOR} | {YES/NO} |

---

## Recommended Approach

{Filled in during S1.P3.3 Synthesis}

**Recommendation:** {Option name or combination}

**Rationale:**
- {Reason 1 - tied to user answer or finding}
- {Reason 2 - tied to user answer or finding}
- {Reason 3 - tied to user answer or finding}

**Key Design Decisions:**
- {Decision 1}: {Rationale}
- {Decision 2}: {Rationale}

---

## Scope Definition

{Clear boundaries for the epic based on Discovery findings and user answers.}

### In Scope

- {Item 1}
- {Item 2}
- {Item 3}
- {Item 4}

### Out of Scope

- {Item 1} - {Brief reason}
- {Item 2} - {Brief reason}

### Deferred (Future Work)

- {Item 1} - {When/why to revisit}
- {Item 2} - {When/why to revisit}

---

## Proposed Feature Breakdown

{Feature breakdown informed by Discovery research and user answers.}

**Total Features:** {N}
**Implementation Order:** {Sequential | Parallel where noted}

### Feature 1: {feature_name}

**Purpose:** {1-2 sentence description}

**Scope:**
- {Key capability 1}
- {Key capability 2}
- {Key capability 3}

**Dependencies:** {None | Depends on Feature X}

**Discovery Basis:**
- Based on Finding: {Reference to research finding}
- Based on User Answer: {Reference to Q# answer}

**Estimated Size:** {SMALL | MEDIUM | LARGE}

---

### Feature 2: {feature_name}

**Purpose:** {1-2 sentence description}

**Scope:**
- {Key capabilities}

**Dependencies:** {Dependencies}

**Discovery Basis:**
- Based on Finding: {Reference}
- Based on User Answer: {Reference}

**Estimated Size:** {SMALL | MEDIUM | LARGE}

---

{Continue for all features}

### Feature Dependency Diagram

```text
Feature 1 ({name})
    |
    v
Feature 2 ({name}) <-- depends on Feature 1
    |
    v
Feature 3 ({name}) <-- depends on Features 1, 2
```json

{Or if parallel:}

```text
Feature 1 ({name})     Feature 2 ({name})
         \                   /
          \                 /
           v               v
         Feature 3 ({name})
```markdown

---

## Discovery Log

{Chronological record of Discovery Phase progress.}

| Timestamp | Activity | Outcome |
|-----------|----------|---------|
| {YYYY-MM-DD HH:MM} | Initialized Discovery | Created initial questions |
| {YYYY-MM-DD HH:MM} | Iteration 1 Research | Found {N} components, {M} questions |
| {YYYY-MM-DD HH:MM} | User answered Q1-Q{N} | Clarified {topic} |
| {YYYY-MM-DD HH:MM} | Iteration 2 Research | Found {N} patterns, {M} questions |
| {YYYY-MM-DD HH:MM} | User answered Q{N}-Q{M} | Decided {approach} |
| {YYYY-MM-DD HH:MM} | Final Iteration | No new questions |
| {YYYY-MM-DD HH:MM} | Synthesis complete | Recommended {approach} |
| {YYYY-MM-DD HH:MM} | User approved | Proceed to feature breakdown |

---

## User Approval

**Discovery Approved:** {YES | NO}
**Approved Date:** {YYYY-MM-DD}
**Approved By:** User

**Approval Notes:**
{Any notes from user approval, modifications requested, etc.}

---

## Post-Discovery Updates

{This section tracks any updates made to DISCOVERY.md after the Discovery Phase completes. Updates should only occur if something is found to be incorrect or outdated.}

| Date | What Changed | Why | Impact on Features |
|------|--------------|-----|-------------------|
| {YYYY-MM-DD} | {Change description} | {Reason for update} | {Which features affected} |

{If no updates: "No post-Discovery updates."}
```

---

## Usage Notes

### When to Create

- **Stage:** S1.P3.1 (Initialize Discovery Document)
- **Trigger:** After S1 Step 2 (Epic Analysis) completes

### How to Update

- **During Discovery Loop:** Update after each iteration
- **After Discovery:** Only update if something is found incorrect or outdated
- **Post-Discovery updates:** Document in "Post-Discovery Updates" section

### Key Principles

1. **Source of Truth:** DISCOVERY.md is the epic-level source of truth for decisions
2. **Traceability:** Every recommendation ties to research findings or user answers
3. **Immutable (mostly):** After approval, only update to correct errors
4. **Referenced by Features:** Feature specs reference this document for shared context

### What Stays Here vs Feature Specs

| Content | Location | Why |
|---------|----------|-----|
| Epic problem statement | DISCOVERY.md | Shared across features |
| Solution approach | DISCOVERY.md | Affects all features |
| User answers (scope/priorities) | DISCOVERY.md | Epic-level decisions |
| Scope boundaries | DISCOVERY.md | Epic-level |
| Feature breakdown rationale | DISCOVERY.md | Why these features |
| Feature-specific requirements | spec.md | Feature-specific |
| Feature implementation details | spec.md | Feature-specific |
| Feature acceptance criteria | spec.md | Feature-specific |

---

## Related Templates

- **Feature Spec Template:** `feature_spec_template.md` - References Discovery Context
- **Epic README Template:** `epic_readme_template.md` - Tracks Discovery status
- **Epic Ticket Template:** `epic_ticket_template.md` - Created after Discovery

---

*End of Discovery Template*
