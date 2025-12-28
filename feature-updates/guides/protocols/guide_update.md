# Guide Update Protocol

**Purpose:** Update planning and development guides based on lessons learned.

**Related:** [README.md](README.md) - Protocol index

---


**Execute:** After all QA is complete, before moving folder to done/.

**Steps:**

**Step 1: Review Lessons Learned File**
1. Read through all entries in `{feature_name}_lessons_learned.md`
2. Identify which entries have actionable guide updates
3. Group updates by target guide (planning vs development)

**Step 2: Discuss Updates with User**
Present a summary to the user:
> "Based on lessons learned during this feature's development, I recommend the following updates to the guides:
>
> **Planning Guide Updates:**
> - {summary of changes}
>
> **Development Guide Updates:**
> - {summary of changes}
>
> Would you like me to apply these updates?"

**Step 3: Apply Updates**
After user approval:
1. Update `feature-updates/guides/feature_planning_guide.md` with approved changes
2. Update `feature-updates/guides/feature_development_guide.md` with approved changes
3. Mark the "Guide Update Status" section in lessons learned as complete

**Step 4: Document in Lessons Learned**
Update the "Guide Update Status" checklist:
```markdown
## Guide Update Status

- [x] All lessons documented
- [x] Recommendations reviewed with user
- [x] feature_planning_guide.md updated
- [x] feature_development_guide.md updated
- [x] Updates verified by user
```

---

