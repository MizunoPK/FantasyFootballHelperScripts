# Epic Completion Summary Template - S10

**Purpose:** Template for completing EPIC_README.md Epic Completion Summary section
**When to use:** Step 8d of S10 (Final Verification & Completion)
**Main Guide:** `stages/s10/s10_epic_cleanup.md`

---

## Template: EPIC_README.md Agent Status (Final Update)

After epic is complete and moved to done/, update the EPIC_README.md file in its new location.

**Location:** `.shamt/epics/done/{epic_name}/EPIC_README.md`

**Section to update:** "Agent Status" section at the top

```markdown
## Agent Status

**Last Updated:** {YYYY-MM-DD HH:MM}
**Current Stage:** S10 - Epic Cleanup
**Status:** ✅ COMPLETE

**Epic Completion Summary:**
- Start Date: {YYYY-MM-DD}
- End Date: {YYYY-MM-DD}
- Duration: {N} days
- Total Features: {N}
- Bug Fixes Created: {N} (or 0 if none)
- Final Test Pass Rate: 100% ({total_tests}/{total_tests} tests)

**Epic Moved To:** .shamt/epics/done/SHAMT-{N}-{epic_name}/
**Original Request:** .shamt/epics/requests/{epic_name}.txt

**Next Steps:** None - epic complete! 🎉
```

---

## Template with Example Values

**Example: "SHAMT-1-improve_recommendation_engine" epic**

```markdown
## Agent Status

**Last Updated:** 2025-12-30 16:00
**Current Stage:** S10 - Epic Cleanup
**Status:** ✅ COMPLETE

**Epic Completion Summary:**
- Start Date: 2025-12-15
- End Date: 2025-12-30
- Duration: 15 days
- Total Features: 3
- Bug Fixes Created: 1
- Final Test Pass Rate: 100% ({N}/{N} tests)

**Epic Moved To:** .shamt/epics/done/SHAMT-1-improve_recommendation_engine/
**Original Request:** .shamt/epics/requests/improve_recommendation_engine.txt

**Next Steps:** None - epic complete! 🎉
```

---

## Usage Instructions

### When to Update

Update EPIC_README.md **after** the epic folder is moved to done/ (Step 7 of S10).

### Steps

1. **Navigate to epic's new location:**
   ```bash
   cd .shamt/epics/done/{epic_name}/
   ```

2. **Open EPIC_README.md** using Read tool

3. **Locate "Agent Status" section** (should be near the top)

4. **Replace Agent Status content** with the template above

5. **Fill in all placeholders:**
   - `{YYYY-MM-DD HH:MM}`: Current timestamp
   - `{YYYY-MM-DD}`: Start and end dates
   - `{N}`: Actual numbers (duration, features, bug fixes)
   - `{total_tests}`: Actual test count from test suite
   - `{epic_name}`: Your epic's folder name

6. **Save updated EPIC_README.md** using Edit tool

---

## What Each Field Means

### Start Date
The date when S1 (Epic Planning) began. Check git history or EPIC_README.md early Agent Status entries.

### End Date
The date when S10 (Epic Cleanup) was completed. Use today's date if completing now.

### Duration
Calculate: End Date - Start Date in calendar days. Shows how long epic took.

### Total Features
Count of feature folders in epic (e.g., feature_01, feature_02, feature_03 = 3 features).

### Bug Fixes Created
Count of bugfix folders in epic (e.g., bugfix_high_interface_mismatch = 1 bug fix). Use 0 if no bug fixes.

### Final Test Pass Rate
Result of `{TEST_COMMAND}` showing passed/total. Should always be 100%.

### Epic Moved To
The new location in done/ folder. Always: `.shamt/epics/done/SHAMT-{N}-{epic_name}/`

### Original Request
Location of the original .txt file with user's request. Always: `.shamt/epics/requests/{epic_name}.txt`

---

## Additional Section: S10 - User Testing Results (Optional)

If bugs were found and fixed during user testing, add this section to EPIC_README.md:

```markdown
## S10 - User Testing Results

**User Testing Conducted:** {YYYY-MM-DD}
**Bugs Found:** {N}
**Bugs Fixed:** {N}
**Final User Testing Result:** ✅ NO BUGS - Approved for commit

**Bug Fixes Created During User Testing:**
- bugfix_{priority}_{name}/: {Brief description}
- bugfix_{priority}_{name}/: {Brief description}

**S9 Re-Validation:** ✅ PASSED (after bug fixes)
```

**When to include this:**
- Only if user found bugs during S10 Step 5 (User Testing)
- Documents the bug fix cycle during final testing
- Shows transparency of quality process

**Example:**

```markdown
## S10 - User Testing Results

**User Testing Conducted:** 2025-12-30
**Bugs Found:** 2
**Bugs Fixed:** 2
**Final User Testing Result:** ✅ NO BUGS - Approved for commit

**Bug Fixes Created During User Testing:**
- bugfix_high_point_calculation/: Fixed incorrect trade value calculation
- bugfix_medium_display_format/: Corrected multi-item trade display

**S9 Re-Validation:** ✅ PASSED (after bug fixes)
```

---

## Verification Checklist

Before considering epic completion summary complete:

- [ ] Agent Status section updated in EPIC_README.md
- [ ] All placeholders replaced with actual values
- [ ] Dates are accurate (check git history if unsure)
- [ ] Feature count matches actual feature folders
- [ ] Bug fix count matches actual bugfix folders
- [ ] Test pass rate is 100% (verified with recent test run)
- [ ] Epic location shows done/ folder path
- [ ] Original request location is correct (still in root)
- [ ] User testing completed in S9 (Step 6) — ZERO bugs reported (prerequisite for S10)
- [ ] EPIC_README.md saved in done/ folder (not root)

---

## Common Mistakes

### ❌ Mistake 1: Updating EPIC_README.md before moving epic

**Wrong:**
```bash
## Edit .shamt/epics/improve_recommendation_engine/EPIC_README.md
## Then move epic to done/
## Result: Edit is lost because file moved before saving
```

**Right:**
```bash
## Move epic to done/
## Then edit .shamt/epics/done/improve_recommendation_engine/EPIC_README.md
## Result: Edit persists in correct location
```

### ❌ Mistake 2: Wrong epic location in completion summary

**Wrong:**
```markdown
**Epic Moved To:** .shamt/epics/improve_recommendation_engine/  ← Still in root!
```

**Right:**
```markdown
**Epic Moved To:** .shamt/epics/done/improve_recommendation_engine/  ← In done/
```

### ❌ Mistake 3: Forgetting to count bug fixes

**Wrong:**
```markdown
**Total Features:** 3
**Bug Fixes Created:** 0  ← Actually had 1 bug fix!
```

**Right:**
```markdown
**Total Features:** 3
**Bug Fixes Created:** 1
```

**How to verify:** Use `ls .shamt/epics/done/{epic_name}/` and count bugfix_* folders.

### ❌ Mistake 4: Including failed tests in pass rate

**Wrong:**
```markdown
**Final Test Pass Rate:** 95% (N-fail/N tests)  ← Should be 100%!
```

**Right:**
```markdown
**Final Test Pass Rate:** 100% ({N}/{N} tests)  ← All tests passing
```

**Note:** If tests aren't 100%, don't commit. Fix tests first, then complete S10.

---

## Epic Progress Tracker (Also Update This)

In addition to Agent Status, update the "Epic Progress Tracker" section:

```markdown
## Epic Progress Tracker

**Last Updated:** {YYYY-MM-DD}

**Overall Epic Status:** ✅ COMPLETE

| Stage | Status | Date Completed |
|-------|--------|----------------|
| S1: Epic Planning | ✅ COMPLETE | {YYYY-MM-DD} |
| S2: Feature Deep Dives (All Features) | ✅ COMPLETE | {YYYY-MM-DD} |
| S3: Epic-Level Docs, Tests, and Approval | ✅ COMPLETE | {YYYY-MM-DD} |
| S4: (Deprecated — Test Scope Decision in S5 Step 0) | N/A | N/A |
| S5: Feature Implementation (All Features) | ✅ COMPLETE | {YYYY-MM-DD} |
| S9: Epic Final QC | ✅ COMPLETE | {YYYY-MM-DD} |
| S10: Epic Cleanup | ✅ COMPLETE | {YYYY-MM-DD} |

**Epic Completion Date:** {YYYY-MM-DD}
```

---

**END OF EPIC COMPLETION TEMPLATE**
