# D1 Round 1: Fix Plan
# Cross-Reference Accuracy

**Date:** 2026-02-05
**Dimension:** D1 (Cross-Reference Accuracy)
**Round:** 1 (Fix Planning)
**Issues Found:** 50+ broken references across 5 categories

---

## Executive Summary

**Total Broken References:** 50+
**Fix Categories:** 5 distinct categories
**Total Estimated Time:** 3.5-4.5 hours
**Recommended Approach:** Sequential by priority (root files first)

**Fix Strategy:**
1. Priority 1: Root-level files (30 min) - CRITICAL impact
2. Priority 2: Old S5 structure (1 hour) - HIGH priority
3. Priority 3: Missing templates (1-2 hours) - MEDIUM priority
4. Priority 4: Missing reference files (30 min) - MEDIUM priority
5. Priority 5: Low-impact issues (30 min) - LOW priority

---

## Priority 1: Root-Level Files (CRITICAL)

**Time Estimate:** 30 minutes
**Impact:** CRITICAL (main entry points for guides)

### Files to Fix

#### 1.1: README.md
**Broken References:**
- `debugging/ISSUES_CHECKLIST.md`

**Fix Strategy:**
- Update phrasing from "See: debugging/ISSUES_CHECKLIST.md" to "Creates: debugging/ISSUES_CHECKLIST.md"
- Context: This file is created during debugging protocol, not a pre-existing template

**Specific Changes:**
```markdown
OLD: See: debugging/ISSUES_CHECKLIST.md for issue tracking
NEW: Creates: debugging/ISSUES_CHECKLIST.md during debugging (central issue tracker)
```

---

#### 1.2: EPIC_WORKFLOW_USAGE.md
**Broken References:**
- `stages/s5/round3_todo_creation.md` (multiple occurrences)
- `stages/s5/5.1.3.2_round3_part2a.md`
- `stages/s5/5.1.3.3_round3_part2b.md`
- `stages/s5/round1/planning.md`
- `stages/s5/s5_implementation_planning.md`
- `stages/s5/round1/file.md`

**Fix Strategy:**
- Map old S5 paths to new S5 structure (see Priority 2 for mappings)
- Use global find-replace for each old → new mapping

**Path Mappings:**
```
stages/s5/round3_todo_creation.md → stages/s5/s5_p3_planning_round3.md
stages/s5/5.1.3.2_round3_part2a.md → stages/s5/s5_p3_i2_gates_part1.md
stages/s5/5.1.3.3_round3_part2b.md → stages/s5/s5_p3_i3_gates_part2.md
stages/s5/round1/planning.md → stages/s5/s5_p1_planning_round1.md
stages/s5/s5_implementation_planning.md → stages/s5/s5_p1_planning_round1.md
stages/s5/round1/file.md → stages/s5/s5_p1_planning_round1.md
```

---

#### 1.3: audit/README.md
**Broken References:**
- `templates/discovery_report_template.md` (4 occurrences)
- `templates/fix_plan_template.md` (4 occurrences)
- `templates/verification_report_template.md` (5 occurrences)
- `templates/round_summary_template.md` (5 occurrences)
- `reference/pattern_library.md`
- `reference/verification_commands.md`
- Other reference files

**Fix Strategy:**
- Create placeholder template files in `audit/templates/` (see Priority 3)
- Mark reference files as "⏳ Coming Soon" inline (see Priority 4)

---

## Priority 2: Old S5 File Structure (HIGH)

**Time Estimate:** 1 hour
**Impact:** HIGH (breaks workflow navigation)
**Total Occurrences:** 10+ references across multiple files

### Complete Path Mapping

| Old Path | New Path | Occurrences |
|----------|----------|-------------|
| `stages/s5/round3_todo_creation.md` | `stages/s5/s5_p3_planning_round3.md` | 2 |
| `stages/s5/5.1.3.2_round3_part2a.md` | `stages/s5/s5_p3_i2_gates_part1.md` | 3 |
| `stages/s5/5.1.3.3_round3_part2b.md` | `stages/s5/s5_p3_i3_gates_part2.md` | 4 |
| `stages/s5/round1/planning.md` | `stages/s5/s5_p1_planning_round1.md` | 3 |
| `stages/s5/s5_implementation_planning.md` | `stages/s5/s5_p1_planning_round1.md` | 6 |
| `stages/s5/round1/file.md` | `stages/s5/s5_p1_planning_round1.md` | 2 |

### Files Affected

**Root-level files:**
- EPIC_WORKFLOW_USAGE.md (6 occurrences) - covered in Priority 1

**Audit files:**
- audit/dimensions/d10_file_size_assessment.md
- audit/dimensions/d12_cross_file_dependencies.md
- audit/outputs/d10_file_size/stage2_fix_plan.md
- audit/outputs/d10_file_size/stage3_session1_progress.md

### Fix Approach

1. **Create sed script for batch replacement:**
```bash
#!/bin/bash
# fix_s5_paths.sh

FILES=(
  "feature-updates/guides_v2/EPIC_WORKFLOW_USAGE.md"
  "feature-updates/guides_v2/audit/dimensions/d10_file_size_assessment.md"
  "feature-updates/guides_v2/audit/dimensions/d12_cross_file_dependencies.md"
  "feature-updates/guides_v2/audit/outputs/d10_file_size/stage2_fix_plan.md"
  "feature-updates/guides_v2/audit/outputs/d10_file_size/stage3_session1_progress.md"
)

for file in "${FILES[@]}"; do
  sed -i 's|stages/s5/round3_todo_creation\.md|stages/s5/s5_p3_planning_round3.md|g' "$file"
  sed -i 's|stages/s5/5\.1\.3\.2_round3_part2a\.md|stages/s5/s5_p3_i2_gates_part1.md|g' "$file"
  sed -i 's|stages/s5/5\.1\.3\.3_round3_part2b\.md|stages/s5/s5_p3_i3_gates_part2.md|g' "$file"
  sed -i 's|stages/s5/round1/planning\.md|stages/s5/s5_p1_planning_round1.md|g' "$file"
  sed -i 's|stages/s5/s5_implementation_planning\.md|stages/s5/s5_p1_planning_round1.md|g' "$file"
  sed -i 's|stages/s5/round1/file\.md|stages/s5/s5_p1_planning_round1.md|g' "$file"
done
```

2. **Manual verification:**
   - Spot-check each file after replacement
   - Verify context makes sense with new paths
   - Check for any residual broken references

---

## Priority 3: Missing Audit Templates (MEDIUM)

**Time Estimate:** 1-2 hours
**Impact:** MEDIUM (prevents audit completion)
**Total Occurrences:** 18 references

### Templates to Create

#### 3.1: discovery_report_template.md
**References:** 4 occurrences in audit/README.md
**Purpose:** Template for Stage 1 (Discovery) output

**Content Strategy:**
```markdown
# D{N} Round {R}: Discovery Report
# {Dimension Name}

**Date:** YYYY-MM-DD
**Dimension:** D{N} ({Dimension Name})
**Automation Level:** {percentage}% automated
**Round:** {R} (Initial Discovery / Follow-up)

---

## Executive Summary

**Issues Found:** {count} issues across {categories} categories
**Categories:** [list categories]
**Priority:** {HIGH/MEDIUM/LOW}
**Estimated Fix Time:** {estimate}

**Impact:**
- [Impact point 1]
- [Impact point 2]

---

## Issues by Category

### Category 1: {NAME} (PRIORITY)

**Total Occurrences:** {count}
**Priority:** {HIGH/MEDIUM/LOW}

**Pattern:** [Description of pattern]

**Broken References/Issues:**
1. [Issue 1]
2. [Issue 2]

**Files Affected:**
- [File 1]
- [File 2]

**Root Cause:** [Analysis]

**Fix Strategy:** [Proposed fix]

---

[Repeat for each category]

---

## Validation Statistics

**Files Scanned:** {count}
**Total Issues Found:** {count}
**False Positives:** {count}
**True Issues:** {count}

---

## Recommended Fix Priority

**Priority 1:** {description} ({time estimate})
**Priority 2:** {description} ({time estimate})

---

## Next Steps

**Stage 2: Fix Planning**
- [Planning task 1]
- [Planning task 2]

---

**D{N} Round {R} Discovery: COMPLETE**
**Ready for:** Stage 2 (Fix Planning)
```

**File Location:** `feature-updates/guides_v2/audit/templates/discovery_report_template.md`

---

#### 3.2: fix_plan_template.md
**References:** 4 occurrences in audit/README.md
**Purpose:** Template for Stage 2 (Fix Planning) output

**Content Strategy:**
```markdown
# D{N} Round {R}: Fix Plan
# {Dimension Name}

**Date:** YYYY-MM-DD
**Dimension:** D{N} ({Dimension Name})
**Round:** {R} (Fix Planning)
**Issues Found:** {count} issues across {categories} categories

---

## Executive Summary

**Total Issues:** {count}
**Fix Categories:** {count} distinct categories
**Total Estimated Time:** {estimate}
**Recommended Approach:** {Sequential/Parallel}

**Fix Strategy:**
1. Priority 1: {description} ({time})
2. Priority 2: {description} ({time})
[...]

---

## Priority 1: {NAME} (CRITICAL/HIGH/MEDIUM/LOW)

**Time Estimate:** {estimate}
**Impact:** {CRITICAL/HIGH/MEDIUM/LOW}

### Specific Fixes

#### 1.1: {Fix Name}
**Broken References:**
- [Reference 1]
- [Reference 2]

**Fix Strategy:**
- [Strategy point 1]
- [Strategy point 2]

**Specific Changes:**
```
OLD: [old content]
NEW: [new content]
```

---

[Repeat for each priority]

---

## Fix Validation Checklist

After applying all fixes, verify:
- [ ] All broken references resolved
- [ ] No new broken references introduced
- [ ] Cross-references consistent
- [ ] Navigation paths functional
- [ ] Context preserved

---

## Next Steps

**Stage 3: Apply Fixes**
- Apply fixes in priority order
- Commit changes incrementally
- Test navigation paths

---

**D{N} Round {R} Fix Planning: COMPLETE**
**Ready for:** Stage 3 (Apply Fixes)
```

**File Location:** `feature-updates/guides_v2/audit/templates/fix_plan_template.md`

---

#### 3.3: verification_report_template.md
**References:** 5 occurrences in audit/README.md, AUDIT_CREATION_STATUS.md
**Purpose:** Template for Stage 4 (Verification) output

**Content Strategy:**
```markdown
# D{N} Round {R}: Verification Report
# {Dimension Name}

**Date:** YYYY-MM-DD
**Dimension:** D{N} ({Dimension Name})
**Round:** {R} (Verification)
**Fixes Applied:** {count} fixes

---

## Executive Summary

**Verification Status:** {PASS/FAIL}
**Issues Remaining:** {count}
**New Issues Found:** {count}
**Ready for Loop Decision:** {YES/NO}

---

## Verification Results

### Original Issues

| Issue ID | Category | Status | Notes |
|----------|----------|--------|-------|
| 1 | {category} | ✅ FIXED / ❌ REMAINS | {notes} |
| 2 | {category} | ✅ FIXED / ❌ REMAINS | {notes} |

**Summary:**
- Fixed: {count} issues
- Remaining: {count} issues
- Success Rate: {percentage}%

---

### New Issues Discovered

**New Issues Found:** {count}

| Issue ID | Category | Priority | Description |
|----------|----------|----------|-------------|
| N1 | {category} | {priority} | {description} |

---

## Validation Method

**Automated Checks:**
- [Check 1]: {PASS/FAIL}
- [Check 2]: {PASS/FAIL}

**Manual Spot Checks:**
- [File 1]: {PASS/FAIL}
- [File 2]: {PASS/FAIL}

---

## Recommendations

**If PASS (zero issues):**
- Proceed to Stage 5 (Loop Decision)
- Consider exit if all criteria met

**If FAIL (issues remain):**
- Return to Stage 2 (Fix Planning) for remaining issues
- OR proceed to Round 2 if significant progress made

---

## Next Steps

**Stage 5: Loop Decision**
- Evaluate exit criteria (8 criteria)
- Decide: Exit audit OR Round 2

---

**D{N} Round {R} Verification: COMPLETE**
**Status:** {PASS/FAIL}
```

**File Location:** `feature-updates/guides_v2/audit/templates/verification_report_template.md`

---

#### 3.4: round_summary_template.md
**References:** 5 occurrences in audit/README.md, PERFECTION_VERIFICATION.md
**Purpose:** Template for round completion summary

**Content Strategy:**
```markdown
# D{N} Round {R}: Summary
# {Dimension Name}

**Date:** YYYY-MM-DD
**Dimension:** D{N} ({Dimension Name})
**Round:** {R}
**Status:** {COMPLETE/IN-PROGRESS}

---

## Round Overview

**Duration:** {estimate}
**Stages Completed:** 5/5
**Issues Found:** {count}
**Issues Fixed:** {count}
**Issues Remaining:** {count}

---

## Stage Summaries

### Stage 1: Discovery
**Status:** ✅ COMPLETE
**Output:** discovery_report.md
**Issues Found:** {count}

### Stage 2: Fix Planning
**Status:** ✅ COMPLETE
**Output:** fix_plan.md
**Fixes Planned:** {count}

### Stage 3: Apply Fixes
**Status:** ✅ COMPLETE
**Commits:** {count}
**Files Modified:** {count}

### Stage 4: Verification
**Status:** ✅ COMPLETE
**Output:** verification_report.md
**Verification Result:** {PASS/FAIL}

### Stage 5: Loop Decision
**Status:** ✅ COMPLETE
**Decision:** {EXIT/ROUND_2}
**Reason:** {explanation}

---

## Key Achievements

1. {Achievement 1}
2. {Achievement 2}
3. {Achievement 3}

---

## Lessons Learned

**What worked well:**
- {Lesson 1}
- {Lesson 2}

**What could be improved:**
- {Improvement 1}
- {Improvement 2}

---

## Final Status

**If Exiting:**
- ✅ All issues resolved
- ✅ Exit criteria met
- ✅ D{N} audit COMPLETE

**If Continuing:**
- ⏳ Round 2 required
- New patterns to investigate: [list]
- Estimated time for Round 2: {estimate}

---

**D{N} Round {R}: COMPLETE**
```

**File Location:** `feature-updates/guides_v2/audit/templates/round_summary_template.md`

---

### Template Creation Checklist

After creating all 4 templates:
- [ ] All templates created in `audit/templates/` directory
- [ ] Templates follow consistent markdown structure
- [ ] Placeholders clearly marked with {curly braces}
- [ ] Each template has complete sections for its stage
- [ ] All references in audit/README.md now point to existing files
- [ ] Templates are ready for copy-paste use in future audits

---

## Priority 4: Missing Reference Files (MEDIUM)

**Time Estimate:** 30 minutes
**Impact:** MEDIUM (marked as "coming soon")
**Total Occurrences:** 30+ references

### Reference Files Referenced

1. `reference/pattern_library.md` (7 occurrences)
2. `reference/verification_commands.md` (7 occurrences)
3. `reference/file_size_reduction_guide.md` (6 occurrences)
4. `reference/user_challenge_protocol.md` (4 occurrences)
5. `reference/confidence_calibration.md` (4 occurrences)
6. `reference/context_analysis_guide.md` (3 occurrences)
7. `reference/quick_reference.md` (2 occurrences)
8. `reference/fresh_eyes_guide.md` (1 occurrence)
9. `reference/issue_classification.md` (1 occurrence)

### Fix Strategy: Mark as Future Work

**Approach:** Remove broken file path links, mark inline as future work

**Pattern for replacement:**
```markdown
OLD: See: reference/pattern_library.md (Coming Soon)
NEW: ⏳ Pattern library reference (planned for future audit work)

OLD: **See:** reference/verification_commands.md (Coming Soon)
NEW: **Future Reference:** ⏳ Verification commands guide (planned)
```

**Files Affected:**
- audit/README.md (main references)
- audit/AUDIT_SYSTEM_REVIEW.md
- audit/audit_overview.md
- audit/dimensions/d10_file_size_assessment.md

**Specific Changes by File:**

#### audit/README.md
Replace all "Coming Soon" references with ⏳ symbol and "planned" notation:
- Pattern library → "⏳ Pattern library (planned)"
- Verification commands → "⏳ Verification commands (planned)"
- File size reduction → "⏳ File size reduction guide (planned)"
- (etc. for all 9 references)

Remove markdown link syntax `[text](path)` and replace with plain text with emoji.

---

## Priority 5: Low-Impact Issues (LOW)

**Time Estimate:** 30 minutes
**Impact:** LOW (informational references, missing entry point)

### 5.1: Debugging File Phrasing

**Occurrences:** 15+ references
**Pattern:** References to output files created during debugging

**Broken References:**
- `debugging/ISSUES_CHECKLIST.md` (10 occurrences)
- `debugging/guide_update_recommendations.md` (6 occurrences)
- `debugging/investigation_rounds.md` (3 occurrences)
- `debugging/lessons_learned.md` (3 occurrences)
- `debugging/process_failure_analysis.md` (3 occurrences)

**Fix Strategy:**
Update phrasing from "See:" to "Creates:"

**Pattern:**
```markdown
OLD: See: debugging/ISSUES_CHECKLIST.md
NEW: Creates: debugging/ISSUES_CHECKLIST.md (central issue tracker during debugging)

OLD: **See:** debugging/guide_update_recommendations.md
NEW: **Creates:** debugging/guide_update_recommendations.md (output file from debugging)
```

**Files Affected:**
- README.md (covered in Priority 1)
- debugging/debugging_protocol.md
- debugging/investigation_protocol.md
- debugging/issue_tracking.md

---

### 5.2: Missing parallel_work README

**Occurrences:** 6 references
**Files Affected:**
- audit output files
- audit/dimensions/d10_file_size_assessment.md

**Fix Strategy:**
Create basic `parallel_work/README.md` as router to protocol files

**Content:**
```markdown
# Parallel Work System - S2 Feature Planning

**Purpose:** Coordinate multiple agents working on S2 feature planning in parallel

**When to use:** Epics with 3+ features (40-60% time reduction for S2 phase)

---

## Quick Navigation

### Master Protocol
- **[s2_parallel_protocol.md](s2_parallel_protocol.md)** - Complete overview with 9-phase workflow

### Agent Guides
- **[s2_primary_agent_guide.md](s2_primary_agent_guide.md)** - Primary agent workflow (coordinator + Feature 01)
- **[s2_secondary_agent_guide.md](s2_secondary_agent_guide.md)** - Secondary agent workflow (feature owner)

### Infrastructure Protocols
- **[lock_file_protocol.md](lock_file_protocol.md)** - File locking for shared resources
- **[communication_protocol.md](communication_protocol.md)** - Agent-to-agent messaging
- **[checkpoint_protocol.md](checkpoint_protocol.md)** - Crash recovery and staleness detection

### Recovery Protocols
- **[stale_agent_protocol.md](stale_agent_protocol.md)** - Handling crashed/hung agents
- **[sync_timeout_protocol.md](sync_timeout_protocol.md)** - Sync point timeout handling

### Templates
- **[templates/handoff_package_s2_template.md](templates/handoff_package_s2_template.md)** - Secondary agent handoff
- **[templates/feature_status_template.txt](templates/feature_status_template.txt)** - STATUS file format
- **[templates/epic_readme_template.md](templates/epic_readme_template.md)** - EPIC_README with parallel sections

---

## System Overview

**Agent Roles:**
- **Primary Agent:** Coordinator + Feature 01 owner (85% feature work, 15% coordination)
- **Secondary Agent:** Feature owner only (90% feature work, 10% coordination)

**Coordination Mechanisms:**
- Checkpoints (every 15 minutes) - Crash recovery + staleness detection
- Communication (file-based messaging) - Async agent-to-agent messaging
- STATUS Files (per feature) - Quick status check
- Locks (shared files) - Prevent race conditions

**Sync Points:**
- Sync Point 1 (S2 → S3): All agents complete S2, Primary runs S3 solo
- Sync Point 2 (S4 → S5): Primary completes S4, all agents continue to S5

---

## Quick Start

**For Primary Agent:**
1. Read [s2_primary_agent_guide.md](s2_primary_agent_guide.md)
2. Generate handoff packages for secondaries
3. Execute S2 for Feature 01 while coordinating

**For Secondary Agent:**
1. Read [s2_secondary_agent_guide.md](s2_secondary_agent_guide.md)
2. Receive handoff package from Primary
3. Execute S2 for assigned feature

---

## Integration with Workflow

**S1 Step 5.8-5.9:** Offer parallel work (if 3+ features)
**S1 Final Step:** Generate handoffs (if parallel enabled)
**S2 Router:** Detects Primary vs Secondary role
**S3 Start:** Sync verification
**S4 End:** Notify secondaries to proceed

**Note:** Parallel work is OPTIONAL - workflow works identically in sequential mode.

---

**See:** Master protocol for complete details and decision guides.
```

**File Location:** `feature-updates/guides_v2/parallel_work/README.md`

---

## Fix Validation Checklist

After applying all fixes across all 5 priorities:

### Automated Validation
- [ ] Run validation scripts from Stage 1 (verify zero broken references)
- [ ] Check all root-level files (README.md, EPIC_WORKFLOW_USAGE.md, audit/README.md)
- [ ] Verify no new broken references introduced

### Manual Spot Checks
- [ ] README.md: Check debugging file phrasing updated
- [ ] EPIC_WORKFLOW_USAGE.md: Check all S5 paths updated
- [ ] audit/README.md: Check all template references valid
- [ ] audit/templates/: Check all 4 templates created
- [ ] parallel_work/README.md: Check router created

### Navigation Testing
- [ ] Click through S5 cross-references in EPIC_WORKFLOW_USAGE.md
- [ ] Click through template references in audit/README.md
- [ ] Verify parallel_work README navigates to protocols

### Context Verification
- [ ] Old S5 paths: Verify context makes sense with new paths
- [ ] Template references: Verify templates match their usage context
- [ ] Reference files: Verify "planned" notation is clear

---

## Commit Strategy

**Incremental commits recommended:**

1. **Commit 1: Root-level file fixes** (Priority 1)
   ```
   docs/d1: Fix broken references in root-level files

   - README.md: Update debugging file phrasing (See → Creates)
   - EPIC_WORKFLOW_USAGE.md: Update old S5 structure paths
   - audit/README.md: Update template references (to be created)
   ```

2. **Commit 2: Old S5 structure mapping** (Priority 2)
   ```
   docs/d1: Update all old S5 file structure references

   Mapped old S5 round structure to new phase/iteration structure:
   - round3_todo_creation.md → s5_p3_planning_round3.md
   - 5.1.3.2_round3_part2a.md → s5_p3_i2_gates_part1.md
   - 5.1.3.3_round3_part2b.md → s5_p3_i3_gates_part2.md
   - round1/planning.md → s5_p1_planning_round1.md
   - s5_implementation_planning.md → s5_p1_planning_round1.md

   Files updated: 5 files (audit dimension files, output files)
   ```

3. **Commit 3: Audit templates creation** (Priority 3)
   ```
   docs/d1: Create audit output templates

   Created 4 audit templates in audit/templates/:
   - discovery_report_template.md
   - fix_plan_template.md
   - verification_report_template.md
   - round_summary_template.md

   All templates follow consistent structure with {placeholder} syntax
   ```

4. **Commit 4: Reference file updates** (Priority 4)
   ```
   docs/d1: Mark planned reference files as future work

   Updated 9 "Coming Soon" references to ⏳ planned notation:
   - pattern_library.md
   - verification_commands.md
   - file_size_reduction_guide.md
   - (+ 6 others)

   Removed broken markdown links, clarified future work status
   ```

5. **Commit 5: Low-impact fixes** (Priority 5)
   ```
   docs/d1: Fix debugging phrasing and create parallel_work README

   - Updated debugging file references (See → Creates)
   - Created parallel_work/README.md as router to protocols

   All broken references now resolved
   ```

---

## Time Tracking

| Priority | Task | Estimated | Actual | Notes |
|----------|------|-----------|--------|-------|
| 1 | Root files | 30 min | | |
| 2 | Old S5 paths | 1 hour | | |
| 3 | Audit templates | 1-2 hours | | |
| 4 | Reference files | 30 min | | |
| 5 | Low-impact | 30 min | | |
| **Total** | | **3.5-4.5 hours** | | |

---

## Next Steps

**Stage 3: Apply Fixes**
- Execute fixes in priority order (1 → 5)
- Commit changes incrementally (5 commits recommended)
- Update time tracking as work progresses

**Stage 4: Verification**
- Re-run validation scripts
- Spot-check all modified files
- Verify zero broken references remain

---

**D1 Round 1 Fix Planning: COMPLETE**
**Ready for:** Stage 3 (Apply Fixes)
