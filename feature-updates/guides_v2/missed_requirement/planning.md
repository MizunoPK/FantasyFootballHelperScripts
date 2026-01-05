# PHASE 2: Planning (Stage 2 Deep Dive)

**Purpose:** Create/update feature spec through Stage 2 deep dive

**When to Use:** After PHASE 1 complete, user decided on approach

**Previous Phase:** PHASE 1 (Discovery) - See `missed_requirement/discovery.md`

**Next Phase:** PHASE 3 (Realignment) - See `missed_requirement/realignment.md`

---

## Overview

**PHASE 2 returns to Stage 2 (Feature Deep Dive) to properly plan the new/updated feature:**

- Create/update feature folder structure
- Run full Stage 2 deep dive process
- Create/update spec.md and checklist.md
- Same rigor as all features (no shortcuts)
- User approval required before proceeding to Stage 3

---

## If Creating NEW Feature

### Step 1: Create Feature Folder

**Create standard feature folder structure:**

```bash
# Navigate to epic folder
cd feature-updates/{epic_name}/

# Create new feature folder
mkdir -p feature_{XX}_{name}

# Create standard files
touch feature_{XX}_{name}/README.md
touch feature_{XX}_{name}/spec.md
touch feature_{XX}_{name}/checklist.md
touch feature_{XX}_{name}/lessons_learned.md
```

**Folder structure:**
```
feature-updates/{epic_name}/feature_{XX}_{name}/
├── README.md            (create with Agent Status)
├── spec.md              (create in this phase)
├── checklist.md         (create in this phase)
├── lessons_learned.md   (empty for now)
└── research/            (create if needed)
```

### Step 2: Create README.md

**Template:**

```markdown
# Feature {XX}: {Name}

**Epic:** {epic_name}
**Status:** Stage 2 (Feature Deep Dive - Planning)
**Created:** {YYYY-MM-DD}
**Origin:** Missed requirement discovered during {stage/feature}

---

## Agent Status

**Last Updated:** {YYYY-MM-DD HH:MM}

**Current Phase:** MISSED_REQUIREMENT_PLANNING
**Current Guide:** missed_requirement/planning.md
**Guide Last Read:** {YYYY-MM-DD HH:MM}

**Current Stage:** Stage 2 (Feature Deep Dive)
**Current Guide:** stages/stage_2/feature_deep_dive.md

**Next Action:** Follow Stage 2 process (Phases 0-6)

**Critical Rules from Guide:**
- Full Stage 2 deep dive required (no shortcuts)
- Create complete spec.md with all requirements
- Create checklist.md with all decisions
- User approval before Stage 3

---

## Missed Requirement Context

**Discovered during:** {stage and feature}
**What's missing:** {brief description}
**Priority:** {high/medium/low}
**Sequence position:** {where in epic sequence}

---

## Feature Overview

{Will be filled during Stage 2 deep dive}
```

---

### Step 3: Run Full Stage 2 Deep Dive

**🚨 FIRST ACTION:** Use "Starting Stage 2" prompt from `prompts/stage_2_prompts.md`

**READ:** `stages/stage_2/feature_deep_dive.md`

**Follow complete Stage 2 process:**

**Phase 0-1.5: Research & Epic Intent**
- Review epic intent for this missed requirement
- Research technical approaches if needed
- Audit similar features (in this epic or other projects)

**Phase 2-2.5: Specification with Traceability**
- Create spec.md with:
  - Feature overview
  - Requirements (functional and non-functional)
  - Data flow and integration points
  - Algorithms and business logic
  - Success criteria
  - Traceability matrix (epic intent → requirements)

**Phase 3-6: Questions, Scope, Alignment, Approval**
- Ask clarifying questions (one at a time)
- Validate scope completeness
- Check alignment with other features
- Get user approval on spec

**No shortcuts:**
- Full rigor required
- Same quality as all features
- Complete spec.md documentation
- All questions resolved

---

## If Updating UNSTARTED Feature

### Step 1: Read Existing Feature Files

**Read current feature state:**

```bash
# Read existing spec
cat feature_{XX}_{name}/spec.md

# Read existing checklist
cat feature_{XX}_{name}/checklist.md

# Read existing README
cat feature_{XX}_{name}/README.md
```

**Understand:**
- Current feature scope
- Existing requirements
- Integration points
- Decisions made in checklist

---

### Step 2: Update README.md

**Add missed requirement section:**

```markdown
## Missed Requirement Update

**Last Updated:** {YYYY-MM-DD HH:MM}

**Added Scope:** {brief description of what's being added}
**Discovered during:** {stage and feature}
**Impact:** Scope increases, implementation time may increase

**Currently:** Updating spec.md and checklist.md to include new scope

**Critical Rules:**
- Full Stage 2 deep dive for additions
- Update spec.md with new requirements
- Update checklist.md with new decisions
- Maintain alignment with existing scope
```

---

### Step 3: Update spec.md

**🚨 FIRST ACTION:** Use "Starting Stage 2" prompt from `prompts/stage_2_prompts.md`

**READ:** `stages/stage_2/feature_deep_dive.md`

**Update approach:**

**1. Add new sections for missed requirement:**
```markdown
## New Requirement: {Name}

**Origin:** Missed requirement discovered during {stage/feature}

### Requirements
{New requirements for this missed functionality}

### Data Flow
{How new functionality integrates with existing feature}

### Algorithms
{Any new algorithms or business logic}
```

**2. Update existing sections affected:**
```markdown
## Integration Points (UPDATED)

**Original integration points:**
- {existing integrations}

**New integration points:**
- {integrations added by missed requirement}
```

**3. Update traceability matrix:**
```markdown
## Traceability Matrix (UPDATED)

| Epic Intent | Requirement | Implementation |
|-------------|-------------|----------------|
| {existing} | {existing} | {existing} |
| {new from missed req} | {new requirement} | {planned implementation} |
```

**4. Document scope increase:**
```markdown
## Scope Changes

**Original Scope:** {summary of original feature}

**Added Scope (Missed Requirement):** {what was added}

**Impact:**
- Implementation complexity: {increased/same}
- Estimated time: {may increase}
- Dependencies: {any new dependencies}
```

---

### Step 4: Update checklist.md

**Add new decisions:**

```markdown
## Planning Decisions (UPDATED - Missed Requirement)

**Last Updated:** {YYYY-MM-DD HH:MM}

### New Decisions (from missed requirement)

**Q: {Question about new scope}**
- A: {Decision made}
- Reasoning: {Why this decision}

**Q: {Integration approach for new functionality}**
- A: {Decision made}
- Reasoning: {Why this approach}

### Original Decisions
{Keep all existing decisions}
```

---

### Step 5: Follow Stage 2 Process for Additions

**Run Stage 2 Phases 0-6 focused on the additions:**

- Research new functionality if needed
- Specify new requirements clearly
- Ask clarifying questions about new scope
- Validate completeness
- Check alignment with existing feature scope
- Get user approval

**Critical:**
- Same rigor as original feature planning
- Don't skip steps
- Ensure new scope aligns with existing scope
- Update all affected sections

---

## Completion Criteria

**PHASE 2 complete when:**

### For NEW feature:
- [x] Feature folder created (feature_{XX}_{name}/)
- [x] README.md created with Agent Status
- [x] spec.md created following Stage 2 process
- [x] checklist.md created with all decisions
- [x] All Stage 2 phases completed (0-6)
- [x] User approved spec

### For UPDATED feature:
- [x] Existing spec.md and checklist.md read
- [x] README.md updated with missed requirement context
- [x] spec.md updated with new requirements
- [x] checklist.md updated with new decisions
- [x] All affected sections updated
- [x] Scope increase documented
- [x] All Stage 2 phases completed for additions
- [x] User approved updated spec

### For BOTH:
- [x] Full Stage 2 rigor applied (no shortcuts)
- [x] Complete documentation
- [x] All questions resolved
- [x] User approval obtained

---

## Common Patterns

### Pattern 1: New Feature - Simple Addition

**Scenario:** Missed requirement is self-contained, minimal integration

**Approach:**
- Create feature folder
- Run Stage 2 with focus on standalone functionality
- Keep integration points simple
- Document clear boundaries

---

### Pattern 2: New Feature - Complex Integration

**Scenario:** Missed requirement requires significant integration with other features

**Approach:**
- Create feature folder
- Run Stage 2 with heavy focus on integration points
- Document data flows clearly
- Identify dependencies early
- May discover need for changes to other features (handle in Stage 3)

---

### Pattern 3: Update Unstarted - Logical Grouping

**Scenario:** Missed requirement naturally fits within existing feature scope

**Approach:**
- Update spec.md with new section
- Integrate seamlessly with existing requirements
- Minimal disruption to original scope
- Document as logical extension

---

### Pattern 4: Update Unstarted - Significant Scope Increase

**Scenario:** Missed requirement significantly expands feature scope

**Approach:**
- Update spec.md with major new sections
- Clearly mark scope increase
- May need to restructure spec for clarity
- Document implementation time impact
- Consider if feature should be renamed

---

## Anti-Patterns to Avoid

### ❌ Anti-Pattern 1: Rushed Spec

**Mistake:** "Just add a quick note to spec, we know what to build"

**Why wrong:** Incomplete spec leads to implementation issues, missed edge cases

**Correct:** Full Stage 2 rigor - complete spec with all details

---

### ❌ Anti-Pattern 2: Skipping User Approval

**Mistake:** "I'll just add this to the spec, user already approved the concept"

**Why wrong:** User needs to see complete spec, may have feedback

**Correct:** Follow Stage 2 through user approval phase

---

### ❌ Anti-Pattern 3: Not Updating Traceability

**Mistake:** Add requirements but don't update traceability matrix

**Why wrong:** Lost connection between epic intent and requirements

**Correct:** Update traceability matrix with new requirements

---

### ❌ Anti-Pattern 4: Minimal Documentation

**Mistake:** "This is a small addition, doesn't need full documentation"

**Why wrong:** Even small features need complete documentation for future agents

**Correct:** Full documentation regardless of size

---

## Examples

### Example 1: New Feature - Player Injury Tracking

**Context:** Missed requirement discovered during feature_02 implementation

**Actions:**
1. Create `feature_05_injury_tracking/` folder
2. Create README.md with missed requirement context
3. Run Stage 2 deep dive:
   - Phase 0-1.5: Research injury data sources, audit similar tracking features
   - Phase 2-2.5: Create spec.md with:
     - Data model for injury status
     - API integration requirements
     - Update frequency
     - Impact on projections
     - Traceability to epic intent
   - Phase 3-6: Ask questions, validate scope, get approval
4. Create checklist.md with decisions (data source, update frequency, etc.)
5. User approves spec

**Output:** Complete feature_05 spec ready for Stage 3 alignment

---

### Example 2: Update Feature - Add CSV Export

**Context:** Missed CSV export functionality, should be part of feature_03_performance_tracker

**Actions:**
1. Read existing feature_03 spec.md and checklist.md
2. Update README.md with missed requirement context
3. Run Stage 2 focused on additions:
   - Research CSV export libraries
   - Add "CSV Export" section to spec.md
   - Update integration points (new export API)
   - Update data flow (export pipeline)
   - Document scope increase
4. Update checklist.md with export decisions (format, columns, frequency)
5. User approves updated spec

**Output:** Updated feature_03 spec with CSV export included

---

## Next Steps

**After completing PHASE 2 (Planning - Stage 2 Deep Dive):**

✅ Feature folder created OR existing feature updated
✅ spec.md created/updated with complete requirements
✅ checklist.md created/updated with all decisions
✅ Full Stage 2 rigor applied
✅ User approved spec

**Next:** Read `missed_requirement/realignment.md` for PHASE 3 & 4 (Stage 3 & 4 Alignment)

---

**END OF PHASE 2 GUIDE**
