# Simulation with Historical Data - Lessons Learned

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

### 1. Emphasize Space and Time Efficiency in Proposed Solutions

**What happened:** During Q2 (week-specific data loading), the initial proposal used `shutil.copy()` for file operations. When asked about runtime efficiency, analysis revealed this was wasteful - direct folder references eliminate 340 file copies per simulation.

**Root cause:** Initial proposals focused on correctness and simplicity without analyzing runtime performance implications.

**Recommendation for guides:** When presenting implementation options, ALWAYS include:
- Time complexity analysis (Big-O or estimated operations count)
- Space complexity analysis (memory usage, object creation)
- I/O analysis (disk reads, network calls)
- Performance comparison table between options

**User preference:** Increased complexity is acceptable if it improves efficiency. Prioritize:
1. Runtime performance (time efficiency)
2. Memory efficiency (space efficiency)
3. Code simplicity (acceptable to sacrifice for performance)

---

### 2. Walk Through Checklist Questions One-by-One

**What happened:** During Phase 4 (resolving checklist items), questions were presented and resolved iteratively - one at a time with user confirmation before moving to the next.

**Why this works well:**
- User can focus on one decision at a time
- Allows for follow-up questions and clarifications per item
- User can add requirements or constraints as they arise (e.g., "add week 17 back", "deprecate other modes")
- Creates natural checkpoints for progress tracking
- Easier to course-correct early if a decision is wrong

**Recommendation for guides:** During Phase 4, present questions ONE at a time:
1. Present the question with options and analysis
2. Wait for user decision
3. Update checklist and specs with resolution
4. Move to next question
5. Repeat until all items resolved

**Anti-pattern to avoid:** Presenting all questions at once and asking user to answer them all - this is overwhelming and doesn't allow for iterative refinement.

---

## Summary of Recommended Updates

After development and QA are complete, use this summary to update the guides:

| Guide | Section | Change Type | Description |
|-------|---------|-------------|-------------|
| feature_planning_guide.md | Phase 2 (Deep Investigation) | Add | Include performance analysis checklist for proposed solutions |
| feature_planning_guide.md | Phase 4 (Resolve Questions) | Clarify | Emphasize one-by-one question resolution pattern |

---

## Guide Update Status

- [x] All lessons documented (2 lessons captured)
- [x] Recommendations reviewed with user
- [x] feature_planning_guide.md updated
  - Added Step 2.3.1: Performance Analysis checklist
  - Added "One Question at a Time Pattern" to Phase 4
- [x] feature_development_guide.md updated (N/A - no changes needed)
- [x] Updates verified by user
