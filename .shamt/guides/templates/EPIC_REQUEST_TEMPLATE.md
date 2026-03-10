# Epic Request Template

**File Location:** `.shamt/epics/requests/{epic-name}.md`

**Purpose:** This file captures the epic request BEFORE S1 starts. It should contain high-level requirements, goals, constraints, and initial research. Focus on WHAT needs to be done, not HOW to implement it.

**⚠️ IMPORTANT GUIDELINES:**
- This file stays in `.shamt/epics/requests/` until the user explicitly initiates S1
- **DO NOT** create a `FF-{N}/` folder when writing an epic request
- **DO NOT** include code snippets, detailed schemas, or implementation details
- **DO** mention files/modules that MAY need updating (not specific code changes)
- **DO** reference general practices to follow (e.g., "follow existing agent pattern")
- The S1-S10 epic flow will determine detailed design and implementation

---

## Epic Overview

**Epic Name:** [Short descriptive name]

**Date:** [YYYY-MM-DD]

**Requested By:** [User name or role]

**Epic Type:** [Feature Implementation / Enhancement / Infrastructure / Bug Fix / etc.]

**Estimated Complexity:** [Small / Medium / Large]

---

## Problem Statement

**What problem does this epic solve?**

[Describe the current problem, pain point, or opportunity]

**Why is this important?**

[Business value, user impact, strategic alignment]

**Who is affected?**

[Users, teams, systems impacted]

---

## Goals & Success Metrics

**Primary Goals:**
1. [Goal 1]
2. [Goal 2]
3. [Goal 3]

**Success Metrics:**
- [Metric 1: Target value]
- [Metric 2: Target value]
- [Metric 3: Target value]

**Out of Scope (Explicitly Not Included):**
- [Item 1]
- [Item 2]

---

## Requirements

### Functional Requirements

1. **[Requirement Category 1]**
   - [Specific requirement]
   - [Specific requirement]

2. **[Requirement Category 2]**
   - [Specific requirement]
   - [Specific requirement]

### Non-Functional Requirements

- **Performance:** [Requirements]
- **Security:** [Requirements]
- **Scalability:** [Requirements]
- **Maintainability:** [Requirements]

### Technical Requirements

- **Dependencies:** [List dependencies]
- **Integrations:** [List integrations]
- **Technology Stack:** [Stack requirements or constraints]

---

## Research & Background

### Existing Solutions Analysis

**Current State:**
[How things work now, if applicable]

**Research Findings:**
- [Finding 1: Source/evidence]
- [Finding 2: Source/evidence]

**Alternative Approaches Considered:**
1. **[Approach 1]:** [Pros/Cons]
2. **[Approach 2]:** [Pros/Cons]
3. **[Recommended Approach]:** [Why this is best]

### Technical Constraints

**Known Limitations:**
- [Constraint 1]
- [Constraint 2]

**Architectural Considerations:**
- [Consideration 1]
- [Consideration 2]

---

## Initial Feature Breakdown (Preliminary)

**Note:** This is a preliminary breakdown. S1 Discovery Phase will refine this.

**Proposed Features:**

1. **Feature 1:** [Name]
   - **Purpose:** [1-2 sentences]
   - **Key Components:** [List]

2. **Feature 2:** [Name]
   - **Purpose:** [1-2 sentences]
   - **Key Components:** [List]

3. **Feature 3:** [Name]
   - **Purpose:** [1-2 sentences]
   - **Key Components:** [List]

---

## Dependencies & Risks

### External Dependencies

- **[Dependency 1]:** [Description, owner, timeline]
- **[Dependency 2]:** [Description, owner, timeline]

### Risks & Mitigation

| Risk | Impact | Probability | Mitigation Strategy |
|------|--------|-------------|---------------------|
| [Risk 1] | [High/Med/Low] | [High/Med/Low] | [How to mitigate] |
| [Risk 2] | [High/Med/Low] | [High/Med/Low] | [How to mitigate] |

---

## Timeline & Resources

**Estimated Timeline:** [Weeks]

**Team Members Required:**
- [Role 1: Name or TBD]
- [Role 2: Name or TBD]

**Key Milestones:**
1. [Milestone 1]: [Date]
2. [Milestone 2]: [Date]
3. [Milestone 3]: [Date]

---

## Implementation Considerations

### Existing Codebase Integration

**Areas of the Codebase That May Require Changes:**
- [Area/Module 1]: [Why it may need changes]
- [Area/Module 2]: [Why it may need changes]

**New Areas That May Need Creation:**
- [Area/Module 1]: [General purpose]
- [Area/Module 2]: [General purpose]

**Coding Practices to Follow:**
- [Practice 1, e.g., "Follow existing agent pattern with async/await"]
- [Practice 2, e.g., "Use Pydantic models for validation"]
- [Practice 3, e.g., "Externalize prompts to .md files"]

### Testing Strategy (High-Level)

- **Unit Tests:** [What should be tested, not how]
- **Integration Tests:** [What should be tested, not how]
- **End-to-End Tests:** [What scenarios should be validated]
- **Performance Tests:** [What metrics matter, if applicable]

**Note:** Epic smoke test plan (end-to-end) is finalized in S3.P1. Per-feature test strategies (test_strategy.md) are created in S4.

---

## Open Questions

1. **[Question 1]:** [Context]
   - **Status:** [Unanswered / Answered / Deferred]
   - **Answer:** [If answered]

2. **[Question 2]:** [Context]
   - **Status:** [Unanswered / Answered / Deferred]
   - **Answer:** [If answered]

---

## References

- **Related Docs:** [Links to relevant documentation]
- **Related Epics:** [Links to related epic requests or completed epics]
- **External Resources:** [Research papers, blog posts, library docs, etc.]

---

## Next Steps

**To proceed with this epic:**
1. User reviews this request
2. User says "Start S1 for [epic name]"
3. Agent reads `.shamt/guides/stages/s1/s1_epic_planning.md`
4. Agent creates git branch and FF-{N} folder during S1
5. Agent runs S1 Discovery Phase to refine this request

**This request file remains in `.shamt/epics/requests/` until S1 creates the epic folder.**
