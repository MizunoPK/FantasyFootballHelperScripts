# Epic Request Template

**File Location:** `.shamt/epics/requests/{epic-name}.md`

**Purpose:** This file captures the epic request BEFORE S1 starts. It gives the agent enough context to scope Discovery effectively. Focus on WHAT needs to be done and what's UNKNOWN — not HOW to implement it.

**Guidelines:**
- This file stays in `.shamt/epics/requests/` until the user explicitly initiates S1
- **DO NOT** create a `SHAMT-{N}/` folder when writing an epic request
- **DO NOT** include code snippets, detailed schemas, or implementation details
- **DO** mention files/modules that may be relevant (not specific code changes)
- **DO** capture your preferred direction if you have one — don't leave it for Discovery to guess
- The S1-S10 epic flow determines detailed design and implementation

---

## Epic Overview

**Epic Name:** [Short descriptive name]

**Date:** [YYYY-MM-DD]

**Epic Type:** [Feature / Enhancement / Infrastructure / Bug Fix]

**Rough Size:** [Small (1-2 features) / Medium (3-5 features) / Large (6+ features — may need splitting before S1)]

---

## Goal

[One paragraph: what should be true when this epic is complete that isn't true now? Be concrete about the outcome, not the implementation.]

**Expected interaction (concrete example):**
[Write at least one specific I/O example: "I run X with args Y, I see output Z" or "I open page X, I click Y, I see Z." Even rough. This example will be used in Discovery approval to confirm the agent is solving the right thing.]

**Invisible changes (if applicable):**
[If no user-visible output — e.g., pure refactor, background job — describe what a developer would observe to verify it worked. Leave blank if the change is user-visible.]

**Known edge cases or failure behavior:**
[What should happen when things go wrong? If you have specific expectations about error handling, graceful degradation, or boundary cases — e.g., "if the API is unavailable, fall back to cached data" or "empty input should return an empty list, not an error" — note them here. Leave blank if you have no strong preferences.]

---

## Background & Current State

[How does this area of the system work today? What's the gap or pain point? Why is this coming up now?]

**Prior attempts or related work:**
[Has this been tried before? Is there existing code in this space that's being replaced, extended, or used as a reference? If none, say so.]

---

## Current Workflow

[Walk through how you or your users currently do the thing this epic is replacing or improving. Aim for a step-by-step sequence — even 3-4 rough steps is more useful than a narrative paragraph. This is one of the most time-consuming things for the agent to reconstruct through research alone, and a concrete sequence anchors Discovery immediately.]

**Current workaround (if any):**
[If you're working around the gap today — manually, with a script, by avoiding something — describe it. This establishes the minimum bar the solution needs to clear and signals how much the gap actually costs.]

---

## Unknowns

*Note: These sections cover functional and requirement unknowns. For technical approach unknowns — which library, which pattern, which architecture — see Technical Direction > Genuinely open below.*

**Blockers** — things that must be resolved before any implementation decision is valid:

1. [Question or unknown]
2. [Question or unknown]

**Open questions** — things worth exploring in Discovery but not necessarily blockers:

- [e.g., "not sure whether to extend the existing X or build a separate Y"]

---

## Discovery Targets

[What do you most want Discovery to investigate and decide? List 1-3 specific questions or areas you want the agent to research and bring back a recommendation on. This gives Discovery a clear mandate when there are competing priorities.]

- [e.g., "Is the existing X module extensible enough, or does it need to be rewritten?"]
- [e.g., "What's the right granularity for feature breakdown — one feature or three?"]

*Leave blank if the Unknowns and Technical Direction sections already capture everything clearly.*

---

## Constraints

**Must have:**
- [Non-negotiable requirement]

**Must not:**
- [Hard constraint / anti-requirement — what would make an approach unacceptable?]

---

## Technical Direction

[What technical decisions are already made? What should the agent anchor on — or avoid — when evaluating approaches during Discovery?]

**Pre-decided choices:**
[Things already locked in — specific libraries, patterns, or architectural decisions not up for debate. If none, say so.]

**Patterns to follow:**
[If this should work like an existing part of the codebase, name specific files or modules. The agent will read these early in Discovery to anchor on the right paradigm.]

**Approaches to avoid:**
[Directions that have been tried and rejected, or are known to be incompatible with the system. For each entry, include a brief reason — "tried X, failed because Y" or "incompatible with Z because of W". This lets Discovery distinguish a hard constraint from a preference, and evaluate whether novel approaches repeat the same mistake. Include any code-level failure modes in this area — silent failures, off-by-one offsets, caching bugs — that have burned you before. If none, say so.]

**Genuinely open (Discovery decides):**
[Major technical decisions you're neutral on. For each, note what makes it open — competing options you're indifferent between, or areas where you're missing context to decide. This tells the agent whether to generate options and present trade-offs, or just pick a reasonable approach. For functional unknowns (what the feature should do, not how), use the Unknowns section above.]

---

## Non-functional Requirements

[Constraints on how the system behaves, not just what it does. Write N/A for items that don't apply.]

**Performance:** [Latency targets, throughput expectations, or acceptable slowdowns — or N/A]

**Scale:** [Data volume, user count, or frequency assumptions — or N/A]

**Compatibility:** [Platform, runtime version, or integration constraints — or N/A]

**Security:** [Auth, data handling, or access control requirements — or N/A]

---

## Scope

**In scope:**
- [Item]

**Out of scope (explicitly):**
- [Item — things that might seem related but are intentionally excluded]

---

## Preliminary Feature Sketch

**Note:** This is a hypothesis for Discovery to validate — not a constraint. If Discovery reveals a different breakdown is better, that supersedes this sketch. Even three rough feature names is more useful than leaving this blank.

1. **[Feature name]:** [One sentence on what it does]
2. **[Feature name]:** [One sentence on what it does]

---

## Relevant Codebase Areas

[Files, modules, or systems you already know are involved. Don't try to be exhaustive — just what you already know matters.]

**Coding practices to observe:**
- [e.g., "follow the existing agent pattern with async/await"]
- [e.g., "use Pydantic models for all data structures"]

---

## Definition of Done

[How will you know this epic is complete and working correctly? Be as concrete as you can — this directly seeds the epic ticket's acceptance criteria and failure patterns.]

**Success looks like:**
- [Measurable outcome — e.g., "all N records load without zero-value data", "command completes in under 2 seconds"]

**Failure looks like:**
- [Specific symptom that would indicate something is broken — e.g., ">90% of values are 0.0", "only the last 2 periods have data"]

---

## Known Risks or Blockers

- [Anything that could derail or complicate this epic]
- [Active dependencies on other work, external systems, or team decisions]

---

## Anything Else

[Anything that doesn't fit the sections above — context, intuitions, things that feel relevant but you're not sure where they belong. Leave blank if nothing.]

---

## References

- **Related epics:** [Links to related requests or completed epics in `.shamt/epics/`]
- **External resources:** [Docs, blog posts, library pages, etc.]
