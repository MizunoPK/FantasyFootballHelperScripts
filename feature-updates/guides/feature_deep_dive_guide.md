# Feature Deep Dive Guide

**Purpose:** Detailed research, specification development, and question resolution for ONE sub-feature (or entire feature if not broken down).

**Use this guide when:** After completing `feature_creation_guide.md`

**Execute:** ONCE per sub-feature. ALL sub-features must complete deep dive before proceeding to implementation.

---

## Quick Overview

This guide helps you:
1. Conduct targeted research for THIS sub-feature's scope
2. Populate spec and checklist with detailed findings
3. Resolve questions interactively with user (one at a time)
4. Detect and adjust scope if needed (dynamic sub-feature creation)
5. Ensure alignment across all sub-features before implementation

**Key Principle:** Focus ONLY on the current sub-feature. Don't get distracted by other components.

---

## Workflow Overview

```
Phase 1: Targeted Research
  Deep dive into THIS sub-feature's scope only
                ↓
Phase 2: Update Spec and Checklist
  Document findings, create comprehensive checklist
                ↓
Phase 3: Interactive Question Resolution
  ONE question at a time, update after each answer
                ↓
Phase 4: Sub-Feature Complete + Scope Check
  Mark complete, check if scope adjustment needed
                ↓
Phase 5: Next Sub-Feature or Alignment Review
  If more sub-features: Repeat for next
  If all complete: Proceed to Phase 6
                ↓
Phase 6: Cross-Sub-Feature Alignment Review (MANDATORY for multi-sub-feature)
  Review all specs together, resolve conflicts
                ↓
Phase 7: Ready for Implementation
  All sub-features aligned, ready for TODO creation
```

---

## Before You Start

### For Single Feature

If feature was NOT broken into sub-features:
- Work with `{feature_name}_specs.md` and `{feature_name}_checklist.md`
- Skip Phase 6 (alignment review)
- After Phase 4, proceed directly to Phase 7

### For Sub-Features

If feature WAS broken into sub-features:
- Work with `sub_feature_{N}_{name}_spec.md` and matching checklist
- Execute this guide ONCE per sub-feature
- After completing ALL sub-features, MANDATORY Phase 6 alignment review
- Track progress in `SUB_FEATURES_README.md`

---

## Phase 1: Targeted Research

**Goal:** Deep understanding of THIS sub-feature's implementation requirements

**Scope:** ONLY research relevant to this sub-feature. Ignore other sub-features for now.

### Step 1.1: Identify files and components

**Search for:**
- Classes/methods that will change
- Existing patterns to follow
- Similar implementations to reference
- Integration points with other code

**Document in spec:**
```markdown
## Files Affected

**Primary changes:**
- `path/to/file.py` (lines X-Y) - Description of changes

**Secondary changes:**
- `path/to/other.py` - Minor updates needed

**Integration points:**
- `calling_code.py` calls method_name() - verify interface
```

### Step 1.2: THREE-ITERATION Question Generation (MANDATORY)

Generate questions in three passes to ensure completeness:

**Iteration 1: Core Functionality**
- Edge cases and error conditions
- Configuration options
- Data validation requirements
- Field mappings and transformations

**Iteration 2: Quality & Operations**
- Logging strategies
- Performance considerations
- Testing approaches
- Integration workflows

**Iteration 3: Cross-Cutting Concerns**
- Relationships to other sub-features
- Backward compatibility
- Migration strategies
- Documentation needs

Add ALL questions to checklist.

### Step 1.3: CODEBASE VERIFICATION Rounds (MANDATORY)

**Goal:** Transform checklist from "list of questions" to "researched options with recommendations"

**CRITICAL:** This is NOT "read some files to understand the area" - this is SYSTEMATIC VERIFICATION of EVERY unchecked checklist item.

---

#### Pre-Verification: Count and Categorize Items

**BEFORE starting verification, count checklist items by type:**

```markdown
## Verification Progress Tracking

**Total Items:** {X}
**Item Breakdown:**
- Policy decisions: {N} items (already [x] from planning - SKIP)
- Implementation tasks: {N} items (NEED VERIFICATION)
- Testing items: {N} items (defer to implementation - mark with note)

**Verification Target:** {N} implementation items need patterns/recommendations
**Current Progress:** {X} / {N} verified
```

**Item Type Distinction:**

1. **Policy Decisions** (already `[x]` from initial planning):
   - Example: "NEW-41: Confirm simulation module is OUT OF SCOPE ✅ RESOLVED"
   - **Action:** SKIP - already resolved, no verification needed

2. **Implementation Tasks** (need verification):
   - Example: "NEW-14: Validate arrays have exactly 17 elements (pad if needed)"
   - **Action:** VERIFY - search codebase for patterns, document recommendations

3. **Testing Items** (defer):
   - Example: "TEST-1: Test FantasyPlayer.from_json() with complete QB data"
   - **Action:** Mark with "(Testing - defer to implementation)" and leave `[ ]`

---

#### Verification Process

**For EACH implementation task item:**

**Straightforward verification items:**
- Search codebase to verify yes/no answers
- Mark as `[x]` resolved with verification notes
- **DO NOT ask user** - answer from code
- Include file:line references

**Decision/ambiguous items:**
- Research relevant source code and patterns
- List viable options with pros/cons
- **Add YOUR recommendation** based on research
- Keep as `[ ]` for user decision, but WITH full context
- Include pattern examples from codebase

**Consumer identification:**
- Grep for where outputs are used
- Identify ALL consumers
- Verify expected format/structure
- Document in checklist

---

#### Verification Format Examples

**BEFORE verification (unchecked, no details):**
```markdown
- [ ] **NEW-14:** Validate arrays have exactly 17 elements (pad if needed)
```

**AFTER verification (checked, with pattern and recommendation):**
```markdown
- [x] **NEW-14:** Validate arrays have exactly 17 elements (pad if needed) ✅ VERIFIED
  - **Pattern from codebase:** Lenient approach - no strict validation found in existing code
  - **Recommendation:** Pad if too short, truncate if too long, log warning for mismatches
  - **Rationale:** Matches existing lenient pattern (skip bad data with warnings, don't fail)
  - **Implementation:** `(array + [0.0] * 17)[:17]` - simple one-liner
  - **Reference:** FantasyPlayer.from_dict() uses safe_*_conversion helpers (lines 159-194)
```

**BEFORE verification (decision item):**
```markdown
- [ ] **NEW-78:** Handle position file missing
```

**AFTER verification (with researched options):**
```markdown
- [ ] **NEW-78:** Handle position file missing **(USER DECISION REQUIRED - Phase 3)**
  - What if qb_data.json doesn't exist?
  - **Option A:** Create new file with players from self.players for that position
  - **Option B:** Raise FileNotFoundError (consistent with loading policy in Sub-feature 1)
  - **Recommendation:** Option B (fail fast - missing file is structural issue)
  - **Pattern:** PlayerManager.py:236-250 shows fail-fast for structural issues
  - **STATUS:** Awaiting user decision in Phase 3 (Interactive Question Resolution)
```

---

#### Verification Rounds

**Round 1: Initial Verification**
- Search codebase for answers to each item
- Document patterns found
- Mark items `[x]` with verification notes
- Update progress count after each item

**Round 2: Skeptical Re-verification**
- Re-verify findings from Round 1 (verify your verification)
- Ensure file:line references are correct
- Verify patterns actually exist in codebase
- Check for missed consumers

---

#### MANDATORY Checkpoint Before Phase 2

**After completing Round 2, verify:**

```markdown
## Verification Checkpoint (MANDATORY)

- [ ] **Item count verified:**
  - Total items: {X}
  - Policy decisions (skipped): {N}
  - Implementation tasks (verified): {N}
  - Testing items (deferred): {N}
  - VERIFIED: {N} implementation + {N} testing = {X} total ✓

- [ ] **ALL implementation items have:**
  - [x] Pattern from actual codebase identified (with file:line reference)
  - [x] Specific recommendation given (not vague)
  - [x] Rationale explaining why
  - [x] Implementation approach suggested (code snippet if applicable)

- [ ] **ALL decision items have:**
  - [x] Multiple options documented (with pros/cons)
  - [x] Recommendation based on research (not gut feeling)
  - [x] Pattern references from codebase supporting recommendation
  - [x] Marked for Phase 3 user decision

- [ ] **No items left unchecked** (except testing deferred and user decisions)

**IF ANY CHECKBOX ABOVE IS UNCHECKED:** Return to verification rounds and complete missing work.

**ONLY proceed to Phase 2 when ALL checkboxes are `[x]`**
```

---

**Result:** Checklist has:
- Many `[x]` items with patterns and recommendations documented
- `[ ]` decision items with researched options (awaiting Phase 3)
- `[ ]` testing items with "(Testing - defer to implementation)" note

### Step 1.4: Create research documents (if needed)

**When to create research doc:**
- Complex analysis (>200 lines of findings)
- Verification reports (breaking changes, migration strategies)
- Algorithm analysis (method-by-method walkthroughs)

**Save ALL research docs to `research/` folder:**

```bash
# Example
research/ALGORITHM_ANALYSIS.md
research/VERIFICATION_REPORT_2025-12-27.md
research/MIGRATION_STRATEGY.md
```

Add entry to `research/README.md`:

```markdown
| File | Purpose | Key Findings |
|------|---------|-------------|
| ALGORITHM_ANALYSIS.md | Analysis of sorting algorithm options | Recommends quicksort for performance |
```

---

## Phase 2: Update Spec and Checklist

### Step 2.1: Update spec with findings

Add to spec file:

```markdown
## Implementation Details

### Data Flow
[Diagram or description of how data moves through this sub-feature]

### Key Algorithms
[Pseudocode or description of core algorithms]

### Integration Points
[How this sub-feature connects to other code]

### Dependencies
[External libraries, other sub-features, existing code]
```

### Step 2.2: Create dependency map

Add to spec:

```markdown
## Dependency Map

**Module Dependencies:**
```
Module A
  ├─► Module B (uses method_x)
  └─► Module C (reads data_y)
```

**Data Flow:**
```
Input: data/file.json
  ↓
Load & Parse (this sub-feature)
  ↓
Transform & Validate
  ↓
Output: FantasyPlayer objects → Used by Module Z
```
```

### Step 2.3: ASSUMPTIONS AUDIT

Document ALL assumptions:

```markdown
## Assumptions

| Assumption | Basis | Risk if Wrong | Mitigation |
|------------|-------|---------------|------------|
| File always exists | Current code doesn't create it | HIGH - crashes | Add existence check + clear error |
| Values are valid floats | Upstream validation | MEDIUM - bad data | Add try/except with logging |
```

### Step 2.4: Populate checklist

Organize questions by category:

```markdown
# {Sub-Feature Name} Checklist

## Core Functionality (X items)
- [ ] **API-1:** What endpoint format? Options: A, B, C. Recommend: B because...
- [x] **API-2:** Does endpoint support pagination? ✅ Yes, verified in docs.py:45
- [ ] **DATA-1:** How to handle missing fields? Options: default, skip, error. Recommend...

## Error Handling (Y items)
- [ ] **ERR-1:** Missing file behavior? Options: A, B, C. Recommend...
- [x] **ERR-2:** Does current code log errors? ✅ Yes, uses logger.error() pattern

## Testing (Z items)
- [ ] **TEST-1:** Integration test approach?
- [ ] **TEST-2:** Expected vs actual comparisons needed?
```

---

## Phase 3: Interactive Question Resolution

**CRITICAL: Implement Lesson 1 - ONE question at a time**

### Step 3.1: Prioritize questions

**Order:**
1. Critical architecture decisions
2. Data mapping questions
3. Implementation details
4. Testing approaches

### Step 3.2: Present ONE question at a time

**Template:**

```markdown
## Question {N}: {Brief Description}

**Context:**
[Why this matters, what code is affected]

**Current State:**
[What the code does now, if applicable]

**Options:**

**Option A:** [Description]
- Pros: ...
- Cons: ...

**Option B:** [Description]
- Pros: ...
- Cons: ...

**My Recommendation:** Option [X] because [reasoning based on research]

**Your decision?**
```

**WAIT for user answer. DO NOT present multiple questions at once.**

### Step 3.3: After EACH answer

**IMMEDIATELY after user responds:**

1. **Update spec** with decision details:
   ```markdown
   ## {Decision Area}
   **Decision:** [User's choice]
   **Rationale:** [Why they chose this]
   **Implementation:** [How we'll do it]
   ```

2. **Mark checklist item** `[x]` with resolution:
   ```markdown
   - [x] **Q-5:** Error handling strategy ✅ RESOLVED - Use Option A (fail fast)
   ```

3. **EVALUATE:** Does this answer create new questions?
   - If YES: Add new questions to checklist immediately
   - Document why new questions arose

4. **Update README** if scope affected

**Example:**
```
User chose Option A (fail fast on errors)

This creates 3 new questions:
- What error message format?
- Where to log errors?
- Should we create custom exception class?

Adding these to checklist as Q-12, Q-13, Q-14.
```

### Step 3.4: Move to next question

**After updates complete:**

```markdown
Question {N} resolved. Updated spec and checklist.

{X} questions remaining.

Next question: {Brief description}

[Present next question using same template]
```

### Step 3.5: Repeat until all resolved

Continue until checklist shows ALL items `[x]`.

**Progress tracking:**
```
✅ Resolved: 25 items
⏳ Remaining: 3 items

Remaining questions:
- Q-23: Integration test approach
- Q-24: Logging format
- Q-25: Error message wording
```

---

## Phase 4: Sub-Feature Complete + Scope Check

### Step 4.1: Verify completion

**Checklist:**
- [ ] All checklist items marked `[x]`
- [ ] Spec has comprehensive implementation details
- [ ] Dependency map created
- [ ] Assumptions documented
- [ ] Research documents (if any) in `research/` folder

### Step 4.2: DYNAMIC SCOPE ADJUSTMENT

**CRITICAL: Check if scope grew significantly during deep dive**

**Triggers for scope adjustment:**
- Sub-feature grew from 15 → 40+ items
- Discovered entirely new component that needs updating
- Found hidden complexity not visible during initial breakdown
- Risk level changed dramatically (LOW → HIGH)

**If scope grew significantly:**

1. **Stop and assess:** Don't just keep going
2. **Propose adjustment:** "This sub-feature has grown to 45 items. Should we split into two sub-features?"
3. **Wait for user approval**
4. **If approved:**
   - Create new sub-feature spec and checklist files
   - Update `SUB_FEATURES_README.md` with new sub-features
   - Redistribute checklist items across sub-features
   - Update dependencies
5. **If not approved:**
   - Document reason in README
   - Continue with larger sub-feature

**Example:**
```markdown
## Scope Adjustment Proposal

**Sub-feature 2** has grown from estimated 20 items → 45 items during deep dive.

**Discovery:** Found that data validation is much more complex than anticipated,
with 3 separate validation layers needed.

**Proposal:** Split into:
- Sub-feature 2a: Core data loading (15 items)
- Sub-feature 2b: Validation layer (30 items)

This allows us to:
- Test data loading independently
- Add validation incrementally
- Reduce risk per sub-feature

**Approve split?**
```

### Step 4.3: Mark sub-feature complete

**Update `SUB_FEATURES_README.md`** (if using sub-features):

```markdown
## Progress Tracking

- [x] Sub-feature 1: Core Data Loading - Deep Dive ✅
- [ ] Sub-feature 1: Core Data Loading - Implementation
- [ ] Sub-feature 2: UI Integration - Deep Dive
- [ ] Sub-feature 2: UI Integration - Implementation
```

**Update feature `README.md`:**

```markdown
**Current Step:** Sub-feature 1 deep dive complete, starting sub-feature 2
```

---

## Phase 5: Next Sub-Feature or Final Review

### If more sub-features remain

```markdown
Sub-feature {N} deep dive complete.

Starting deep dive for Sub-feature {N+1}: {Name}

Repeating feature_deep_dive_guide.md for this sub-feature.
```

**Return to Phase 1 for next sub-feature.**

### If all sub-features complete

```markdown
All {N} sub-features have completed deep dive.

Moving to Phase 6: Cross-Sub-Feature Alignment Review (MANDATORY)
```

**Proceed to Phase 6.**

### If single feature (no sub-features)

```markdown
Feature deep dive complete. All questions resolved.

Proceeding to Phase 7: Ready for Implementation
```

**Skip Phase 6, go directly to Phase 7.**

---

## Phase 6: Cross-Sub-Feature Alignment Review

**MANDATORY for multi-sub-feature setups. SKIP for single features.**

**Goal:** Ensure all sub-feature specs align and don't conflict.

### Step 6.1: Review all specs together

**Read ALL sub-feature specs in sequence:**
- Note interfaces between sub-features
- Check for conflicting assumptions
- Verify dependency order is correct
- Look for duplicated work

### Step 6.2: Check for conflicts

**Common conflicts:**

| Conflict Type | Example | Resolution |
|--------------|---------|------------|
| Interface mismatch | Sub-1 outputs dict, Sub-2 expects list | Align on single format |
| Naming inconsistency | Sub-1 uses "player_id", Sub-2 uses "id" | Standardize across all |
| Duplicate work | Both validate same field | Move to one sub-feature |
| Wrong dependencies | Sub-2 needs Sub-3's output but deps say Sub-2 first | Reorder dependencies |
| Conflicting decisions | Sub-1 uses JSON, Sub-2 uses CSV for storage | Choose one approach |

### Step 6.3: Update conflicting specs

**For each conflict found:**

1. Determine correct approach
2. Update affected sub-feature specs
3. Document the alignment decision
4. Update dependencies if needed

**Example update:**

```markdown
## Alignment Decision: Field Naming

**Conflict:** Sub-feature 1 used "player_id", Sub-feature 2 used "id"

**Resolution:** Standardized on "player_id" across all sub-features

**Updated:** Sub-feature 2 spec (Section 3.2) to use "player_id"
```

### Step 6.4: Verify dependency chain

**Check dependency order:**

```markdown
Sub-feature 1 (no dependencies) ✓
  ↓
Sub-feature 2 (depends on 1) ✓
  ↓
Sub-feature 3 (depends on 2) ✓
  ↓
Sub-feature 4 (depends on 1, 3) ✓
```

**Verify:** Can we implement in this order without circular dependencies?

### Step 6.5: Get user confirmation

**Present alignment summary:**

```markdown
## Cross-Sub-Feature Alignment Review Complete

**Conflicts Resolved:** {N}
- Standardized field naming across all sub-features
- Aligned interface contracts between Sub-2 and Sub-3
- Corrected dependency order (Sub-4 now after Sub-3)

**Dependency Chain Verified:**
[List final dependency order]

**All sub-features aligned and ready for implementation.**

Proceed to sequential implementation?
```

**WAIT for user approval.**

---

## Phase 7: Ready for Implementation

### Step 7.1: Final verification

**Checklist:**
- [ ] All sub-features have complete specs
- [ ] All checklists fully resolved `[x]`
- [ ] Cross-sub-feature conflicts resolved (if applicable)
- [ ] Dependencies documented and verified
- [ ] Research documents organized in `research/` folder

### Step 7.2: Update README status

```markdown
**Current Phase:** IMPLEMENTATION
**Current Step:** Ready for TODO creation
**Next Action:** Execute todo_creation_guide.md for first sub-feature
```

### Step 7.3: Document implementation order

**Update `SUB_FEATURES_README.md`** (if applicable):

```markdown
## Ready for Implementation

**Implementation Order:**
1. Sub-feature 1: {Name} (no dependencies)
2. Sub-feature 2: {Name} (depends on 1)
3. ...

**Process:** For EACH sub-feature sequentially:
- Execute todo_creation_guide.md (FULL 24 iterations)
- Execute implementation_execution_guide.md (FULL process)
- Execute post_implementation_guide.md (FULL QC + smoke testing)
- Commit changes (one commit per sub-feature)
- Mark complete in SUB_FEATURES_README.md
- Move to next sub-feature

**NO SKIPPING:** All quality gates apply to each sub-feature.
```

### Step 7.4: Announce readiness

**For single feature:**
```markdown
Feature specification complete. Ready for TODO creation.

Following todo_creation_guide.md next.
```

**For sub-features:**
```markdown
All {N} sub-features have complete specifications.

Cross-sub-feature alignment verified.

Ready for sequential implementation.

Starting with Sub-feature 1: {Name}

Following todo_creation_guide.md (FULL 24 iterations) for this sub-feature.
```

---

## Quality Gates

**Before proceeding to Phase 7:**

- [ ] **Completeness:** All questions answered, no `[ ]` items in checklists
- [ ] **Detail:** Specs have implementation-level detail, not just high-level descriptions
- [ ] **Verification:** Claims verified against actual code (not assumptions)
- [ ] **Alignment:** (If multi-sub-feature) All conflicts resolved
- [ ] **Dependencies:** Clear dependency chain with no circular dependencies
- [ ] **Documentation:** Research documents organized, assumptions documented

**If any gate fails:** Return to appropriate phase and address issue.

---

## Common Mistakes to Avoid

| Mistake | Why It's Bad | Prevention |
|---------|--------------|------------|
| Presenting all questions at once | User overwhelmed, rushed decisions | ONE question at a time (Lesson 1) |
| Not updating after each answer | Lose follow-up questions, forget decisions | Update spec/checklist immediately |
| Skipping alignment review | Conflicts discovered during implementation | Phase 6 MANDATORY for multi-sub-feature |
| Not checking scope during deep dive | Sub-features grow too large | Monitor item count, propose split if >35 items |
| Researching other sub-features | Distracted from current scope | Focus ONLY on current sub-feature |
| Skipping codebase verification | Many questions answerable from code | Verify before asking user |
| Vague spec entries | Future agents can't implement | Implementation-level detail required |
| Not creating research docs | Findings lost in conversation | Complex analysis → research/ folder |

---

## Next Steps

After completing this guide for ALL sub-features and alignment review:

**NEXT:** Execute `todo_creation_guide.md`

**For single feature:** Execute once

**For sub-features:** Execute once per sub-feature, sequentially:
1. TODO creation (24 iterations)
2. Implementation
3. Post-implementation QC
4. Commit
5. Move to next sub-feature

**NO PARALLEL IMPLEMENTATION:** Complete one sub-feature fully before starting next.
