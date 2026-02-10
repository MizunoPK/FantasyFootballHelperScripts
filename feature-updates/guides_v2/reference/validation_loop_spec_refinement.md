# Validation Loop: Spec Refinement

**Extends:** Master Validation Loop Protocol
**See:** `reference/validation_loop_master_protocol.md`

**Applicable Stages:**
- S2.P1.I3: Feature Spec Refinement (embeds Gates 1, 2)
- S3.P2: Epic Documentation Refinement

**Version:** 2.0 (Updated to extend master protocol)
**Last Updated:** 2026-02-10

---

## Table of Contents

1. [Overview](#overview)
2. [Master Dimensions (7) - Always Checked](#master-dimensions-7---always-checked)
3. [Spec Refinement Dimensions (2) - Context-Specific](#spec-refinement-dimensions-2---context-specific)
4. [Total Dimensions: 9](#total-dimensions-9)
5. [What's Being Validated](#whats-being-validated)
6. [Embedded Gates](#embedded-gates)
7. [Fresh Eyes Patterns Per Round](#fresh-eyes-patterns-per-round)
8. [Common Issues in Spec Refinement Context](#common-issues-in-spec-refinement-context)
9. [Exit Criteria](#exit-criteria)
10. [Integration with Stages](#integration-with-stages)

---

## Overview

**Purpose:** Validate specification documents for completeness, accuracy, and alignment before user approval

**What this validates:**
- spec.md (feature-level in S2.P1.I3)
- EPIC_README.md and documentation (epic-level in S3.P2)
- checklist.md quality (questions vs research gaps)

**Quality Standard:**
- All requirements traced to sources
- Zero scope creep
- Zero assumptions (all uncertainties → checklist questions)
- Ready for user approval (Gate 3 or Gate 4.5)

**Uses:** All 7 master dimensions + 2 spec refinement-specific dimensions = 9 total

---

## Master Dimensions (7) - Always Checked

**See `reference/validation_loop_master_protocol.md` for complete checklists.**

These universal dimensions apply to spec refinement validation:

### Dimension 1: Empirical Verification
- [ ] All referenced file paths verified to exist
- [ ] All referenced class/function names verified from source code
- [ ] All existing interfaces verified (not assumed)
- [ ] All config keys verified from actual config files
- [ ] All data file structures verified (CSV columns, JSON keys)

### Dimension 2: Completeness
- [ ] All spec sections present (Objective, Scope, Components, Algorithms, Edge Cases, Acceptance Criteria)
- [ ] All requirements enumerated (not "...and others")
- [ ] All edge cases identified
- [ ] All integration points documented
- [ ] Acceptance criteria present for all requirements

### Dimension 3: Internal Consistency
- [ ] No contradictory requirements within spec
- [ ] Terminology used consistently throughout
- [ ] Examples match specifications
- [ ] Dependencies are acyclic

### Dimension 4: Traceability
- [ ] Every requirement has source (Epic Request / User Answer / Derived)
- [ ] No "assumption" as source
- [ ] Derived requirements explain derivation logic
- [ ] User answer references include question context and date

### Dimension 5: Clarity & Specificity
- [ ] No vague language ("should", "might", "probably")
- [ ] Specific values/ranges (not "reasonable")
- [ ] Concrete actions (not "handle appropriately")
- [ ] Measurable acceptance criteria

### Dimension 6: Upstream Alignment
- [ ] Spec aligns with DISCOVERY.md findings (feature-level)
- [ ] Spec aligns with epic request (no scope creep)
- [ ] All epic requirements reflected in spec
- [ ] Epic intent preserved

### Dimension 7: Standards Compliance
- [ ] Follows spec template structure
- [ ] Naming conventions consistent with codebase
- [ ] Documentation format matches project standards
- [ ] Cross-references use proper format

---

## Spec Refinement Dimensions (2) - Context-Specific

These 2 dimensions are specific to spec refinement validation:

### Dimension 8: Research Completeness (Gate 1)

**Question:** Is ALL implementation research complete (no research gaps in checklist)?

**Purpose:** Embeds Gate 1 (Research Completeness Audit) from S2.P1.I1

**Checklist:**

**Code Evidence Collected:**
- [ ] All components to be modified identified (specific files:line numbers)
- [ ] All external dependencies verified from source code (not assumed)
- [ ] All existing patterns examined (similar features read, not guessed)
- [ ] All data file formats verified (actual CSV/JSON read, not assumed)
- [ ] All configuration dependencies verified from config files

**Research Documentation:**
- [ ] RESEARCH_NOTES.md or equivalent exists
- [ ] Research notes include file paths, line numbers, code snippets
- [ ] Similar features identified and studied
- [ ] Integration points researched (not assumed)

**No Research Gaps in Checklist:**
- [ ] All checklist questions are valid uncertainties (not research gaps)
- [ ] No questions like "What file is this in?" (should have researched)
- [ ] No questions like "What's the function signature?" (should have verified)
- [ ] All "how does X work?" questions answered via research

**Common Violations:**

❌ **WRONG - Research gap in checklist:**
```markdown
checklist.md:
- [ ] Q1: What file is ConfigManager in?
- [ ] Q2: What parameters does get_adp_multiplier take?
- [ ] Q3: Where is the player data stored?
← These should have been RESEARCHED, not asked
```

✅ **CORRECT - Valid checklist questions (uncertainties):**
```markdown
checklist.md (after research complete):
- [ ] Q1: Should we cache ADP data, or reload every time?
- [ ] Q2: What timeout should we use for file operations?
- [ ] Q3: Should multipliers be configurable or hardcoded?

RESEARCH_NOTES.md shows:
- ConfigManager located: league_helper/util/ConfigManager.py:234
- get_adp_multiplier signature: (self, adp: int) -> Tuple[float, int]
- Player data stored: data/players_2024.csv (verified with ls)
```

❌ **WRONG - Assumption instead of research:**
```markdown
spec.md:
## Components Affected
- ConfigManager (probably in league_helper/util/)
- Uses get_adp_multiplier (probably returns float)

Source: Assumption
```

✅ **CORRECT - Research verified:**
```markdown
spec.md:
## Components Affected
- ConfigManager (league_helper/util/ConfigManager.py:23)
  - Method: get_adp_multiplier(self, adp: int) -> Tuple[float, int]
  - Verified: Read tool, lines 234-256

Source: Verified from source code (2026-02-10)
Evidence: ConfigManager.py:234
```

---

### Dimension 9: Scope Boundary Validation (Gate 2)

**Question:** Does spec match epic scope exactly (no creep, no missing requirements)?

**Purpose:** Embeds Gate 2 (Spec-to-Epic Alignment) from S2.P1.I3

**Checklist:**

**No Scope Creep:**
- [ ] Every requirement traces to epic request OR user answer OR derived
- [ ] No features added that user didn't request
- [ ] No "improvements" beyond stated scope
- [ ] Enhancements flagged as optional/future (not required)

**No Missing Scope:**
- [ ] All epic requirements present in spec
- [ ] All explicit user requests included
- [ ] All Discovery findings reflected
- [ ] No epic goals omitted

**Alignment Verification:**
- [ ] Spec aligns with DISCOVERY.md findings (feature-level)
- [ ] Spec aligns with epic request (no misinterpretation)
- [ ] User intent preserved
- [ ] Scope boundaries clear (in vs out vs deferred)

**Common Violations:**

❌ **WRONG - Scope creep:**
```markdown
Epic Request: "Load ADP data and calculate multipliers"

spec.md Requirements:
1. Load ADP data from CSV (Epic request line 12) ✓
2. Calculate multipliers based on ADP (Epic request line 13) ✓
3. Generate visualization dashboard ← NOT REQUESTED (scope creep)
4. Export to multiple formats ← NOT REQUESTED (scope creep)
```

✅ **CORRECT - Scope match:**
```markdown
Epic Request: "Load ADP data and calculate multipliers"

spec.md Requirements:
1. Load ADP data from CSV
   Source: Epic request line 12
2. Validate ADP values
   Source: Derived from requirement 1 (must validate before use)
3. Calculate multipliers based on ADP
   Source: Epic request line 13
4. Return multiplier values
   Source: Derived from requirement 3 (output requirement)

Out of Scope (future enhancements):
- Visualization dashboard (not requested)
- Export to multiple formats (not requested)
```

❌ **WRONG - Missing scope:**
```markdown
Epic Request: "Handle errors gracefully and log all operations"

spec.md Requirements:
1. Load data
2. Calculate scores
← Missing: Error handling (epic requirement)
← Missing: Logging (epic requirement)
```

✅ **CORRECT - Complete scope:**
```markdown
Epic Request: "Handle errors gracefully and log all operations"

spec.md Requirements:
1. Load data
   Source: Epic request line 10
2. Calculate scores
   Source: Epic request line 12
3. Handle errors gracefully
   Source: Epic request line 15
   - FileNotFoundError: Log and return empty list
   - ValueError: Log and raise with context
4. Log all operations
   Source: Epic request line 16
   - Log data load events
   - Log calculation events
   - Log error events
```

---

## Total Dimensions: 9

**Every validation round checks ALL 9 dimensions:**
- 7 Master dimensions (universal)
- 2 Spec Refinement dimensions (context-specific, embed Gates 1 & 2)

**Process:** See master protocol for 3 consecutive clean rounds requirement

---

## What's Being Validated

### S2.P1.I3: Feature Spec Refinement

**Artifact:** spec.md (feature-level)

**Validates:**
- Feature requirements complete and traceable
- All research complete (no gaps in checklist)
- Scope matches epic (no creep, no missing)
- Acceptance criteria measurable
- Ready for user approval (Gate 3)

**Embeds:**
- Gate 1 (Research Completeness Audit) - Dimension 8
- Gate 2 (Spec-to-Epic Alignment) - Dimension 9

**Success Criteria:**
- Zero research gaps
- Zero scope creep
- Zero missing requirements
- Ready for Gate 3 (User Checklist Approval)

---

### S3.P2: Epic Documentation Refinement

**Artifact:** EPIC_README.md, epic_smoke_test_plan.md

**Validates:**
- Epic documentation complete
- Feature summaries accurate
- Architecture decisions documented
- Scope boundaries clear
- Ready for user approval (Gate 4.5)

**Success Criteria:**
- All features described
- Epic-level architecture documented
- Integration approach clear
- Ready for Gate 4.5 (Epic Plan Approval)

---

## Embedded Gates

### Gate 1: Research Completeness Audit (Dimension 8)

**Embedded in:** Dimension 8 (Research Completeness)

**Pass Criteria:**
- All components researched (specific files:line numbers)
- All external dependencies verified from source code
- All similar features examined
- All data formats verified
- No research gaps in checklist

**When checked:** Every validation round (part of 9 dimensions)

**Cannot exit validation loop if:** Any research gaps remain

---

### Gate 2: Spec-to-Epic Alignment (Dimension 9)

**Embedded in:** Dimension 9 (Scope Boundary Validation)

**Pass Criteria:**
- Zero scope creep (nothing user didn't ask for)
- Zero missing requirements (everything user asked for)
- All requirements trace to epic/user answer/derived
- Epic intent preserved

**When checked:** Every validation round (part of 9 dimensions)

**Cannot exit validation loop if:** Any scope misalignment exists

---

## Fresh Eyes Patterns Per Round

**See master protocol for general fresh eyes principles.**

Spec refinement-specific reading patterns:

### Round 1: Sequential Read + Traceability Check

**Pattern:**
1. Read spec.md sequentially (top to bottom)
2. Check every requirement has source
3. Verify no scope creep
4. Check acceptance criteria measurable

**Checklist:**
- [ ] All 9 dimensions checked (7 master + 2 spec refinement)
- [ ] Gate 1 passed (Dimension 8): Research complete, no gaps in checklist
- [ ] Gate 2 passed (Dimension 9): Scope matches epic exactly
- [ ] Every requirement has source (Epic/User Answer/Derived)
- [ ] Acceptance criteria measurable

**Document findings in validation log**

---

### Round 2: Reverse Read + Gap Detection

**Pattern:**
1. Read spec.md in reverse (bottom to top)
2. Look for gaps between requirements
3. Check implicit vs explicit requirements
4. Verify acceptance criteria completeness

**Focus Areas:**
- Dimension 2 (Completeness) - primary focus
- Dimension 6 (Upstream Alignment) - no missing epic requirements
- Dimension 9 (Scope Boundary) - verify complete coverage

**Checklist:**
- [ ] All 9 dimensions checked
- [ ] No gaps between requirements
- [ ] All implicit requirements made explicit
- [ ] Acceptance criteria for each requirement
- [ ] No vague language

---

### Round 3: Random Spot-Checks + Alignment

**Pattern:**
1. Random spot-check 5 requirements
2. Verify each aligns with DISCOVERY.md
3. Check consistency with epic intent
4. Verify no contradictions

**Focus Areas:**
- Dimension 1 (Empirical Verification) - verify claims are real
- Dimension 4 (Traceability) - sources valid
- Dimension 6 (Upstream Alignment) - matches DISCOVERY.md

**Checklist:**
- [ ] All 9 dimensions checked
- [ ] Spot-checked requirements align with DISCOVERY.md
- [ ] Epic intent preserved
- [ ] No contradictions
- [ ] Ready for user approval

---

## Common Issues in Spec Refinement Context

### Issue 1: Missing Sources

**Problem:** Requirement exists but no source cited

❌ **WRONG:**
```markdown
## Requirement 5
System must handle timeout after 30 seconds.
```

✅ **CORRECT:**
```markdown
## Requirement 5
System must handle timeout after 30 seconds.

**Source:** User Answer to Question 12 (2026-02-08)
**Question:** "What timeout should we use for API calls?"
**Answer:** "30 seconds is standard for our APIs"
```

---

### Issue 2: Scope Creep

**Problem:** Added feature user didn't request

❌ **WRONG:**
```markdown
Epic Request: "Load player data and calculate scores"

spec.md:
1. Load player data ✓
2. Calculate scores ✓
3. Generate PDF reports ← NOT REQUESTED
4. Send email notifications ← NOT REQUESTED
```

✅ **CORRECT:**
```markdown
Epic Request: "Load player data and calculate scores"

spec.md In-Scope:
1. Load player data
   Source: Epic request line 10
2. Calculate scores
   Source: Epic request line 12

Out of Scope (future):
- PDF reports (not requested)
- Email notifications (not requested)
```

---

### Issue 3: Research Gap in Checklist

**Problem:** Checklist has questions that should have been researched

❌ **WRONG:**
```markdown
checklist.md:
- [ ] What file is PlayerManager in?
- [ ] What are the parameters for load_players()?
- [ ] Where is the config file located?
← Should have researched these, not asked user
```

✅ **CORRECT:**
```markdown
After research (RESEARCH_NOTES.md):
- PlayerManager: league_helper/util/PlayerManager.py:23
- load_players(): No parameters, returns List[FantasyPlayer]
- Config file: data/league_config.json

checklist.md (valid uncertainties only):
- [ ] Should we cache player data?
- [ ] What timeout for file operations?
- [ ] Should config be validated on load?
```

---

### Issue 4: Vague Requirements

**Problem:** Requirements not specific enough to implement

❌ **WRONG:**
```markdown
Requirement 3: System should handle errors appropriately
Requirement 5: Performance should be good
```

✅ **CORRECT:**
```markdown
Requirement 3: System must handle errors
- FileNotFoundError: Return empty list, log error at ERROR level
- ValueError: Raise with context, log at ERROR level
- KeyError: Raise with missing key name, log at ERROR level

Requirement 5: Performance targets
- Data load: < 2 seconds for 1000 players
- Calculation: < 100ms for single player
- Memory: < 50MB for typical dataset
```

---

### Issue 5: Missing Acceptance Criteria

**Problem:** Requirement has no "done" definition

❌ **WRONG:**
```markdown
Requirement 7: Implement logging for all operations
```

✅ **CORRECT:**
```markdown
Requirement 7: Implement logging for all operations

**Acceptance Criteria:**
- [ ] All data load operations logged at INFO level
- [ ] All calculation operations logged at DEBUG level
- [ ] All errors logged at ERROR level with stack trace
- [ ] Log output includes timestamp and operation context
- [ ] Log format follows project standard (see CODING_STANDARDS.md)
```

---

### Issue 6: Contradictory Requirements

**Problem:** Requirements conflict with each other

❌ **WRONG:**
```markdown
Requirement 1: Use synchronous file I/O for predictable timing
...
Requirement 8: Use async file I/O for better performance
```

✅ **CORRECT:**
```markdown
Requirement 1: Use synchronous file I/O

**Rationale:** Prioritize predictable timing over performance per user guidance
**Trade-off:** Performance optimization via buffering instead of async
```

---

## Exit Criteria

**Spec refinement validation is COMPLETE when ALL of the following are true:**

**From Master Protocol:**
- [ ] 3 consecutive rounds with ZERO issues found
- [ ] All 7 master dimensions checked every round
- [ ] All 2 spec refinement dimensions checked every round
- [ ] Validation log complete with all rounds documented

**Spec Refinement Specific:**
- [ ] Gate 1 passed (Dimension 8): Research complete, zero research gaps
- [ ] Gate 2 passed (Dimension 9): Scope matches epic exactly
- [ ] All requirements have sources (Epic/User Answer/Derived)
- [ ] Zero scope creep
- [ ] Zero missing requirements
- [ ] All acceptance criteria measurable
- [ ] Ready for user approval (Gate 3 or Gate 4.5)

**Cannot exit if:**
- ❌ Any research gaps in checklist
- ❌ Any scope creep (unrequested features)
- ❌ Any missing epic requirements
- ❌ Any requirements without sources
- ❌ Any vague acceptance criteria

---

## Integration with Stages

### S2.P1.I3: Feature Spec Refinement

**When:** After S2.P1.I1 (Research) and S2.P1.I2 (Checklist Resolution)

**Validates:** spec.md (feature-level)

**Embeds:**
- Gate 1 (Research Completeness) in Dimension 8
- Gate 2 (Spec-to-Epic Alignment) in Dimension 9

**Process:**
1. Use this validation loop protocol
2. Check all 9 dimensions (7 master + 2 spec refinement)
3. Verify Gates 1 & 2 pass (embedded in dimensions)
4. Exit when 3 consecutive clean rounds
5. Proceed to Gate 3 (User Checklist Approval)

**User Approval:** Gate 3 (separate from validation loop)

---

### S3.P2: Epic Documentation Refinement

**When:** After S3.P1 (Epic Testing Strategy Development)

**Validates:** EPIC_README.md, epic_smoke_test_plan.md

**Process:**
1. Use this validation loop protocol
2. Check all 9 dimensions (7 master + 2 spec refinement)
3. Exit when 3 consecutive clean rounds
4. Proceed to S3.P3 (Gate 4.5 - Epic Plan Approval)

**User Approval:** Gate 4.5 (separate from validation loop)

---

## Example Validation Round Sequence

```text
Round 1: Sequential Read + Traceability
- Read spec.md top to bottom
- Check all 9 dimensions
- Issues found: 7
  - D1 (Empirical Verification): ConfigManager signature assumed, not verified
  - D4 (Traceability): Requirements R5, R7 have no source
  - D5 (Clarity): "Handle errors appropriately" is vague
  - D8 (Research Completeness): Checklist Q3 is research gap ("What file?")
  - D9 (Scope Boundary): Requirement R12 is scope creep (not requested)
- Fix all 7 issues
- Clean counter: 0

Round 2: Reverse Read + Gap Detection
- Read spec.md bottom to top
- Check all 9 dimensions
- Issues found: 3
  - D2 (Completeness): Missing edge case for null input
  - D6 (Upstream Alignment): Epic requirement E3 not in spec
  - D9 (Scope Boundary): Missing epic requirement (missing scope)
- Fix all 3 issues
- Clean counter: 0

Round 3: Random Spot-Checks + Alignment
- Spot-check 5 requirements
- Check all 9 dimensions
- Issues found: 0 ✅
- Gates 1 & 2 passed (embedded in D8, D9)
- Clean counter: 1

Round 4: Repeat Validation
- Fresh eyes, different pattern
- Check all 9 dimensions
- Issues found: 0 ✅
- Clean counter: 2

Round 5: Final Sweep
- Complete re-read
- Check all 9 dimensions
- Issues found: 0 ✅
- Clean counter: 3 → VALIDATION COMPLETE ✅

Next: Proceed to Gate 3 (User Checklist Approval)
```

---

## Summary

**Spec Refinement Validation Loop:**
- **Extends:** Master Validation Loop Protocol (7 universal dimensions)
- **Adds:** 2 spec refinement-specific dimensions
- **Total:** 9 dimensions checked every round
- **Embeds:** Gates 1 (Research) & 2 (Alignment) in validation loop
- **Process:** 3 consecutive clean rounds required
- **Quality:** Zero research gaps, zero scope creep, all requirements sourced

**Key Principle:**
> "Every requirement must be traceable to an authoritative source (Epic/User Answer/Derived), with zero assumptions and zero scope creep."

---

*End of Spec Refinement Validation Loop v2.0*
