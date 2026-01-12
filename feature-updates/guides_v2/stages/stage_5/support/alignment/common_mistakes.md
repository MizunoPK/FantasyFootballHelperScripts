# Stage 5d: Common Mistakes to Avoid

**Purpose:** Anti-patterns and pitfalls during cross-feature alignment review
**Prerequisites:** Understanding of Stage 5d workflow from post_feature_alignment.md
**Main Guide:** `stages/stage_5/post_feature_alignment.md`

---

## Overview

This reference documents the most common mistakes agents make during Stage 5d (Cross-Feature Alignment). Each anti-pattern includes:
- The mistake (what agents say/do wrong)
- Why it's wrong (the impact)
- Correct approach (what to do instead)

---

## Common Mistakes to Avoid

### Anti-Pattern 1: Reviewing Only "Related" Features

**Mistake:**
"Feature_01 was ADP integration, so I'll only review feature_02 (player ratings) since they're both scoring multipliers. Feature_03 (schedule strength) is unrelated, I'll skip it."

**Why it's wrong:** Implementation insights can affect unexpected features. Maybe ADP integration revealed ConfigManager patterns that ALL features should follow.

**Correct approach:** Review ALL remaining features, no exceptions. Takes 10 minutes per feature, prevents hours of rework.

---

### Anti-Pattern 2: Comparing to Plan Instead of Code

**Mistake:**
"According to the TODO list, feature_01 was supposed to use ConfigManager.get_adp(), so feature_02 should use ConfigManager.get_rating(). No update needed."

**Why it's wrong:** Plans change during implementation. Actual code might be different.

**Correct approach:** READ THE ACTUAL CODE. Don't assume implementation matches plan.

**Example:**
```python
# Plan said:
ConfigManager.get_adp(player_id) -> float

# Actual code:
ConfigManager.get_adp_multiplier(player_id) -> Tuple[float, int]

# If you compared to plan, you'd miss the signature difference
```

---

### Anti-Pattern 3: Noting Issues But Not Updating Specs

**Mistake:**
"I found that feature_02 spec assumes wrong interface. I'll just make a note in my head and fix it during implementation."

**Why it's wrong:** You'll forget, or next agent won't know. Spec becomes outdated.

**Correct approach:** UPDATE SPEC NOW. Add clear notes about what changed and why.

---

### Anti-Pattern 4: "Probably Fine" Assumptions

**Mistake:**
"Feature_02 spec mentions ConfigManager.get_rating(), feature_01 created get_adp_multiplier(). Probably similar pattern, probably fine."

**Why it's wrong:** "Probably" is not verification. Takes 30 seconds to check actual code.

**Correct approach:** Open the actual source file. Read the actual method signature. Verify, don't assume.

---

### Anti-Pattern 5: Not Getting User Approval for Major Rework

**Mistake:**
"Feature_02 needs to return to Stage 2 because API is deprecated. I'll just go back to Stage 2 and start researching alternatives."

**Why it's wrong:** Major rework decisions should involve user. Maybe they want to remove the feature entirely, or defer it, or have a preferred alternative.

**Correct approach:** Present finding to user, get approval for approach before proceeding.

---

### Anti-Pattern 6: Batch Updates Without Review

**Mistake:**
"I'll update all 4 feature specs at once, then commit everything together."

**Why it's wrong:** Easy to miss nuances when batch processing. Each feature deserves focused attention.

**Correct approach:** Review and update ONE feature at a time. Commit after each. Sequential, focused work.

---

### Anti-Pattern 7: Ignoring checklist.md

**Mistake:**
"I updated spec.md with new interface. Checklist.md doesn't matter, I'll skip it."

**Why it's wrong:** Checklist.md tracks decisions and questions. If you update spec, you should mark corresponding checklist items.

**Correct approach:** Update BOTH spec.md AND checklist.md for each feature.

---

### Anti-Pattern 8: Vague Update Notes

**Mistake:**
```markdown
## Configuration Integration

[Updated]

Use ConfigManager for ratings.
```

**Why it's wrong:** Doesn't say WHAT changed or WHY. Future agent won't understand.

**Correct approach:** Specific update notes:
```markdown
## Configuration Integration

**[UPDATED based on feature_01_adp_integration implementation - 2025-12-30]**

Changed interface from `get_rating() -> float` to `get_rating_multiplier() -> Tuple[float, int]`
to match pattern established by ADP integration. Second value is rating_score for debugging.

See ConfigManager.get_adp_multiplier() at league_helper/util/ConfigManager.py:234 for reference.
```

---

### Anti-Pattern 9: Skipping Git Commits

**Mistake:**
"I'll update all feature specs and commit once at the end of Stage 5d."

**Why it's wrong:** If something goes wrong, you lose all work. Can't track which feature caused issues.

**Correct approach:** Commit after EACH feature spec update. Atomic commits = better history.

---

### Anti-Pattern 10: Unclear Rework Marking

**Mistake:**
```markdown
# Feature 02: Player Rating Integration

Note: This might need updates.
```

**Why it's wrong:** "Might need updates" is vague. Does it need rework or not? Which stage?

**Correct approach:** Clear rework marking:
```markdown
# Feature 02: Player Rating Integration

**🚨 REQUIRES REWORK - Return to Stage 2 (Deep Dive)**

**Reason:** Player rating API deprecated in 2024, need alternative data source.

**Discovered during:** Stage 5d alignment review after feature_01 completion

**User approved:** 2025-12-30

**Next steps:** Research alternative sources, update spec, get user approval, then Stage 5a
```

---

## Anti-Pattern Summary

**Most Critical Mistakes (Fix These First):**
1. **Anti-Pattern 2** - Comparing to plan instead of actual code → Leads to wrong assumptions
2. **Anti-Pattern 3** - Not updating specs → Specs become outdated, rework required later
3. **Anti-Pattern 5** - Not getting user approval for major rework → Wasted effort on wrong approach

**Common Time-Wasters:**
1. **Anti-Pattern 1** - Skipping "unrelated" features → Miss unexpected impacts
2. **Anti-Pattern 4** - "Probably fine" assumptions → Small issues compound
3. **Anti-Pattern 6** - Batch processing → Miss nuances, lower quality

**Quality Issues:**
1. **Anti-Pattern 7** - Ignoring checklist.md → Incomplete updates
2. **Anti-Pattern 8** - Vague update notes → Future confusion
3. **Anti-Pattern 9** - Skipping commits → Lost work, poor history
4. **Anti-Pattern 10** - Unclear rework marking → Confusion about next steps

---

## How to Avoid These Mistakes

**Before Starting Stage 5d:**
- [ ] Read main guide completely (not just skim)
- [ ] Understand ALL 10 critical rules
- [ ] Acknowledge you will review ALL remaining features (not just "related" ones)

**During Each Feature Review:**
- [ ] Read ACTUAL code (not plan/TODO)
- [ ] Update specs immediately when issues found (don't defer)
- [ ] Update BOTH spec.md AND checklist.md
- [ ] Add specific update notes (WHAT changed, WHY, reference to code location)
- [ ] Commit after EACH feature (not batch at end)

**When Issues Found:**
- [ ] Use rework criteria to determine severity
- [ ] Get user approval for major rework (Stage 1 or 2 returns)
- [ ] Mark rework clearly (stage, reason, next steps)
- [ ] Don't assume "probably fine" - verify everything

**Final Check:**
- [ ] ALL remaining features reviewed (none skipped)
- [ ] ALL specs updated where needed
- [ ] ALL checklists updated where needed
- [ ] ALL updates committed individually
- [ ] ALL rework marked clearly
- [ ] User approval obtained for major rework

---

## Quick Self-Check Questions

**Before marking Stage 5d complete, ask yourself:**

1. **Did I review ALL remaining features?**
   - If you skipped any: ❌ Go back, review them
   - If you reviewed all: ✅ Continue

2. **Did I read ACTUAL code or just plans?**
   - If you compared to TODO/plan: ❌ Read actual implementation
   - If you read actual code: ✅ Continue

3. **Did I update specs immediately or just note issues?**
   - If you just noted issues: ❌ Update specs now
   - If you updated specs: ✅ Continue

4. **Did I update BOTH spec.md AND checklist.md?**
   - If only spec.md: ❌ Update checklist.md too
   - If updated both: ✅ Continue

5. **Did I get user approval for major rework?**
   - If you proceeded without approval: ❌ Ask user now
   - If you got approval: ✅ Continue

6. **Did I commit after each feature or batch at end?**
   - If batched: ❌ Git history unclear
   - If individual commits: ✅ Continue

7. **Are my update notes specific (WHAT, WHY, WHERE)?**
   - If vague notes: ❌ Add specifics
   - If detailed notes: ✅ Continue

8. **Are rework markers clear (stage, reason, steps)?**
   - If unclear: ❌ Clarify markers
   - If clear: ✅ Continue

---

## Remember

**Stage 5d Purpose:** Align remaining specs with ACTUAL implementation reality

**Key Principles:**
- Review ALL remaining features (not just "related")
- Compare to ACTUAL code (not plan)
- Update specs IMMEDIATELY (don't defer)
- Get user approval for MAJOR rework
- Sequential focused work (not batch processing)

**Time Investment:** 10-15 minutes per feature review
**Time Saved:** Hours of rework during implementation

**Better to spend 15 minutes updating spec NOW than 2 hours fixing bugs LATER.**

---

**END OF COMMON MISTAKES REFERENCE**
