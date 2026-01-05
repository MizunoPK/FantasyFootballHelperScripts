# Epic Readme Template

**Filename:** `EPIC_README.md`
**Location:** `feature-updates/KAI-{N}-{epic_name}/EPIC_README.md`
**Created:** {YYYY-MM-DD}
**Updated:** Throughout all stages

**Purpose:** Central tracking document for the entire epic, containing Agent Status, progress tracker, and workflow checklists.

---

## Template

```markdown
# Epic: {epic_name}

**Created:** {YYYY-MM-DD}
**Status:** {IN PROGRESS / COMPLETE}
**Total Features:** {N}

---

## 🎯 Quick Reference Card (Always Visible)

**Current Stage:** Stage X - {stage name}
**Active Guide:** `guides_v2/{guide_name}.md`
**Last Guide Read:** {YYYY-MM-DD HH:MM}

**Stage Workflow:**
```
Stage 1 → Stage 2 → Stage 3 → Stage 4 → Stage 5 → Stage 6 → Stage 7
  ↓         ↓         ↓         ↓         ↓         ↓         ↓
Epic    Features  Sanity   Testing   Impl     Epic      Done
Plan    Deep Dive  Check   Strategy  (5a-5e)  QC
```

**You are here:** ➜ Stage {X}

**Critical Rules for Current Stage:**
1. {Rule 1 from current guide}
2. {Rule 2 from current guide}
3. {Rule 3 from current guide}
4. {Rule 4 from current guide}
5. {Rule 5 from current guide}

**Before Proceeding to Next Step:**
- [ ] Read guide: `guides_v2/{current_guide}.md`
- [ ] Acknowledge critical requirements
- [ ] Verify prerequisites from guide
- [ ] Update this Quick Reference Card

---

## Agent Status

**Last Updated:** {YYYY-MM-DD HH:MM}
**Current Stage:** Stage {X} - {stage name}
**Current Phase:** {PLANNING / IMPLEMENTATION / QC}
**Current Step:** {Specific step name - e.g., "QC Round 2 (Consistency)"}
**Current Guide:** `{guide_file_name}.md`
**Guide Last Read:** {YYYY-MM-DD HH:MM}

**Critical Rules from Guide:**
- {Rule 1 - e.g., "24 iterations mandatory, no skipping"}
- {Rule 2 - e.g., "Update Agent Status after each round"}
- {Rule 3 - e.g., "STOP if confidence < Medium"}
- {Rule 4 - e.g., "RESTART Post-Implementation if ANY issues found"}
- {Rule 5 - e.g., "Verify against ACTUAL implementation"}

**Progress:** {X/Y items complete}
**Next Action:** {Exact next task with guide step reference}
**Blockers:** {List any issues or "None"}

---

## Epic Overview

**Epic Goal:**
{Concise description of what this epic achieves - pulled from original {epic_name}.txt request}

**Epic Scope:**
{High-level scope - what's included and what's excluded}

**Key Outcomes:**
1. {Outcome 1}
2. {Outcome 2}
3. {Outcome 3}

**Original Request:** `feature-updates/{epic_name}.txt`

---

## Epic Progress Tracker

**Overall Status:** {X/Y features complete}

| Feature | Stage 1 | Stage 2 | Stage 3 | Stage 4 | Stage 5a | Stage 5b | Stage 5c | Stage 5d | Stage 5e |
|---------|---------|---------|---------|---------|----------|----------|----------|----------|----------|
| feature_01_{name} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} |
| feature_02_{name} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} |
| feature_03_{name} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} |

**Legend:**
- ✅ = Complete
- ◻️ = Not started or in progress

**Stage 6 - Epic Final QC:** {✅ COMPLETE / ◻️ NOT STARTED / 🔄 IN PROGRESS}
- Epic smoke testing passed: {✅/◻️}
- Epic QC rounds passed: {✅/◻️}
- Epic PR review passed: {✅/◻️}
- End-to-end validation passed: {✅/◻️}
- Date completed: {YYYY-MM-DD or "Not complete"}

**Stage 7 - Epic Cleanup:** {✅ COMPLETE / ◻️ NOT STARTED / 🔄 IN PROGRESS}
- Final commits made: {✅/◻️}
- Epic moved to done/ folder: {✅/◻️}
- Date completed: {YYYY-MM-DD or "Not complete"}

---

## Feature Summary

### Feature 01: {feature_name}
**Folder:** `feature_01_{name}/`
**Purpose:** {Brief description}
**Status:** {Stage X complete}
**Dependencies:** {List other features or "None"}

### Feature 02: {feature_name}
**Folder:** `feature_02_{name}/`
**Purpose:** {Brief description}
**Status:** {Stage X complete}
**Dependencies:** {List other features or "None"}

### Feature 03: {feature_name}
**Folder:** `feature_03_{name}/`
**Purpose:** {Brief description}
**Status:** {Stage X complete}
**Dependencies:** {List other features or "None"}

{Continue for all features...}

---

## Bug Fix Summary

**Bug Fixes Created:** {N}

{If no bug fixes: "No bug fixes created yet"}

{If bug fixes exist:}

### Bug Fix 1: {name}
**Folder:** `bugfix_{priority}_{name}/`
**Priority:** {high/medium/low}
**Discovered:** {Stage X - {feature or epic level}}
**Status:** {Stage 5c complete / In progress}
**Impact:** {Brief description of what bug affected}

{Repeat for all bug fixes...}

---

## Epic-Level Files

**Created in Stage 1:**
- `EPIC_README.md` (this file)
- `epic_smoke_test_plan.md` - How to test the complete epic
- `epic_lessons_learned.md` - Cross-feature insights

**Feature Folders:**
- `feature_01_{name}/` - {Brief purpose}
- `feature_02_{name}/` - {Brief purpose}
- `feature_03_{name}/` - {Brief purpose}

**Bug Fix Folders (if any):**
- `bugfix_{priority}_{name}/` - {Brief description}

---

## Workflow Checklist

**Stage 1 - Epic Planning:**
- [ ] Epic folder created
- [ ] All feature folders created
- [ ] Initial `epic_smoke_test_plan.md` created
- [ ] `EPIC_README.md` created (this file)
- [ ] `epic_lessons_learned.md` created

**Stage 2 - Feature Deep Dives:**
- [ ] ALL features have `spec.md` complete
- [ ] ALL features have `checklist.md` resolved
- [ ] ALL feature `README.md` files created

**Stage 3 - Cross-Feature Sanity Check:**
- [ ] All specs compared systematically
- [ ] Conflicts resolved
- [ ] User sign-off obtained

**Stage 4 - Epic Testing Strategy:**
- [ ] `epic_smoke_test_plan.md` updated based on deep dives
- [ ] Integration points identified
- [ ] Epic success criteria defined

**Stage 5 - Feature Implementation:**
- [ ] Feature 1: 5a→5b→5c→5d→5e complete
- [ ] Feature 2: 5a→5b→5c→5d→5e complete
- [ ] Feature 3: 5a→5b→5c→5d→5e complete
- [ ] {List all features}

**Stage 6 - Epic Final QC:**
- [ ] Epic smoke testing passed (all 4 parts)
- [ ] Epic QC rounds passed (all 3 rounds)
- [ ] Epic PR review passed (all 11 categories)
- [ ] End-to-end validation vs original request passed

**Stage 7 - Epic Cleanup:**
- [ ] All unit tests passing (100%)
- [ ] Documentation verified complete
- [ ] Guides updated based on lessons learned (if needed)
- [ ] Final commits made
- [ ] Epic moved to `feature-updates/done/{epic_name}/`

---

## Guide Deviation Log

**Purpose:** Track when agent deviates from guide (helps identify guide gaps)

| Timestamp | Stage | Deviation | Reason | Impact |
|-----------|-------|-----------|--------|--------|
| {YYYY-MM-DD HH:MM} | {Stage X} | {What was skipped/changed} | {Why agent deviated} | {Consequence - e.g., "QC failed, rework required"} |

**Rule:** If you deviate from guide, DOCUMENT IT HERE immediately.

{If no deviations: "No deviations from guides"}

---

## Epic Completion Summary

{This section filled out in Stage 7}

**Completion Date:** {YYYY-MM-DD}
**Start Date:** {YYYY-MM-DD}
**Duration:** {N days}

**Features Implemented:** {N}
**Bug Fixes Created:** {N}

**Final Test Pass Rate:** {X/Y tests passing} ({percentage}%)

**Epic Location:** `feature-updates/done/{epic_name}/`
**Original Request:** `feature-updates/{epic_name}.txt`

**Key Achievements:**
- {Achievement 1}
- {Achievement 2}
- {Achievement 3}

**Lessons Applied to Guides:**
- {Guide update 1 or "None"}
- {Guide update 2 or "None"}
```