# Lessons Learned Protocol

**Purpose:** Capture issues that could have been prevented by better planning or development processes.

**Related:** [README.md](README.md) - Protocol index

---


**Execute:** Throughout development and QA, continuously.

**When to Update the Lessons Learned File:**

Update `{feature_name}_lessons_learned.md` whenever:

1. **During Verification Iterations**: You discover an edge case that should have been identified during planning
2. **During Implementation**: You find an issue that better verification would have caught
3. **During QA/Testing**: Tests reveal a problem the development process should have prevented
4. **After User Feedback**: The user reports something that wasn't working as expected
5. **During Quality Control Rounds**: You find issues that slipped through previous verification

**What to Capture:**

For each lesson, document:
- **What Happened**: The specific issue or problem discovered
- **Root Cause**: Why this was missed during planning or development
- **Impact**: How this affected the feature or required rework
- **Recommended Guide Update**: Specific changes to make to the planning or development guides

**Example Entry:**

```markdown
### Lesson 1: Missing Edge Case for Bye Week Handling

**Date:** 2024-12-06

**What Happened:**
During QA testing, discovered that the player data was returning 0 points for bye weeks, but the downstream calculation was treating 0 as "no data" instead of "bye week".

**Root Cause:**
The planning phase checklist didn't include a specific question about how bye weeks should be distinguished from missing data.

**Impact:**
Required rework of the data structure to add a `bye_week` flag, and modification of 3 downstream functions.

**Recommended Guide Update:**

**Which Guide:** feature_planning_guide.md

**Section to Update:** Checklist Template - Edge Cases

**Recommended Change:**
Add to the Edge Cases section:
- [ ] **Bye week handling:** How to distinguish bye weeks from missing/zero data?
```

**Mandatory Lessons Learned Triggers:**

You MUST add an entry when:
- A bug is found during QA that wasn't caught by the verification iterations
- The user reports the feature isn't working as expected
- An algorithm implementation doesn't match the spec (caught during review)
- An integration point was missed (orphan code created)
- Tests pass but actual behavior is wrong

---

