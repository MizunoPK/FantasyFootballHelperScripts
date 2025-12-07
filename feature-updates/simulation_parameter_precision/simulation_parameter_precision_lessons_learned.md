# Simulation Parameter Precision - Lessons Learned

> **PURPOSE**: This file captures issues encountered during development and QA that could have been prevented by better planning or development processes. After the feature is complete, these lessons will be used to update both guides in the `feature-updates/guides/` folder.

---

## How to Use This File

**When to add entries:**
1. During development: When you discover an edge case the planning phase should have identified
2. During development: When you find an issue that better verification would have caught
3. During QA: When testing reveals a problem the development process should have prevented
4. After user feedback: When the user reports something that wasn't working as expected

**What to capture:**
- What went wrong or was missed
- Why it happened (root cause)
- How the guides could be updated to prevent this in the future
- Specific additions or changes to recommend

---

## Lessons Learned

### Lesson 1: Agent Resolved Questions Without User Input

**What went wrong:** After the user answered Q1 (precision detection algorithm), the agent immediately resolved Q2-Q10 without asking the user for each decision. The agent assumed answers based on "logical consequences" of Q1.

**Why it happened:**
- Session compaction lost context about being in an iterative resolution phase
- Agent prioritized "efficiency" over following the one-at-a-time pattern
- Some questions seemed like obvious follow-ons (e.g., "implementation location" was partially answered by Q1)

**Root cause:** The planning guide emphasizes "one question at a time" but doesn't explicitly warn against resolving multiple items after receiving one answer.

**Recommended guide update:**
Add to `feature_planning_guide.md` in the "Common Mistakes to Avoid" table:
```
| Resolving multiple items from one answer | User loses control of decisions; may disagree with "obvious" conclusions | Only mark ONE item [x] per user response; even if items seem related, confirm each separately |
```

Also add a warning box in Phase 4:
```
⚠️ ONE RESOLUTION PER USER RESPONSE
Even if a user's answer seems to resolve multiple items, only mark ONE item as resolved.
Present the "obviously related" items as follow-up questions - the user may have different opinions.
```

---

### Lesson 2: Agent Didn't Follow Question Format

**What went wrong:** Agent presented questions with options but without the structured format specified in the guide (Context, Question, Options with pros/cons, Recommendation).

**Why it happened:**
- Session compaction lost awareness of the specific format requirements
- Agent knew to ask questions but didn't re-read the guide to verify format
- The format is documented in a "Best Practices" section that's easy to overlook

**Root cause:** The question format is in section "3. Questions File Format" under "Best Practices" - not prominently placed in the Phase 4 workflow.

**Recommended guide update:**
Add to `feature_planning_guide.md` Phase 4 section, directly after "One Question at a Time Pattern":
```markdown
### Question Presentation Format

**REQUIRED FORMAT** for each question:

## Q{N}: {Short Title}

**Context:** {Why this decision matters - 1-2 sentences}

**Question:** {The specific question}

**Options:**
1. **Option A** - {description}
   - Pros: {benefits}
   - Cons: {drawbacks}
2. **Option B** - {description}
   - Pros: {benefits}
   - Cons: {drawbacks}

**Recommendation:** Option {X} because {reasoning}

**Your Answer:** _{to be filled by user}_
```

Also add to "Common Mistakes to Avoid" table:
```
| Presenting options without recommendations | User has to do more work; agent isn't being helpful | Always include a recommendation with reasoning - the user can disagree |
```

---

## Summary of Recommended Updates

After development and QA are complete, use this summary to update the guides:

| Guide | Section | Change Type | Description |
|-------|---------|-------------|-------------|
| feature_planning_guide.md | Common Mistakes to Avoid | Add row | "Resolving multiple items from one answer" |
| feature_planning_guide.md | Phase 4: Iterative Resolution | Add warning box | "ONE RESOLUTION PER USER RESPONSE" |
| feature_planning_guide.md | Phase 4: Iterative Resolution | Add section | "Question Presentation Format" with required template |
| feature_planning_guide.md | Common Mistakes to Avoid | Add row | "Presenting options without recommendations" |

---

## Guide Update Status

- [ ] All lessons documented
- [ ] Recommendations reviewed with user
- [ ] feature_planning_guide.md updated
- [ ] feature_development_guide.md updated
- [ ] Updates verified by user
