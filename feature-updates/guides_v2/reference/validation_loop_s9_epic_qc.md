# Validation Loop: S9 Epic QC

**Extends:** Master Validation Loop Protocol
**See:** `reference/validation_loop_master_protocol.md`

**Applicable Stages:**
- S9.P2: Epic QC Validation Loop (post-feature epic validation)

**Version:** 2.0 (Created to extend master protocol)
**Last Updated:** 2026-02-10

---

## Table of Contents

1. [Overview](#overview)
2. [Master Dimensions (7) - Always Checked](#master-dimensions-7---always-checked)
3. [S9 Epic QC Dimensions (5) - Context-Specific](#s9-epic-qc-dimensions-5---context-specific)
4. [Total Dimensions: 12](#total-dimensions-12)
5. [What's Being Validated](#whats-being-validated)
6. [Fresh Eyes Patterns Per Round](#fresh-eyes-patterns-per-round)
7. [Common Issues in S9 QC Context](#common-issues-in-s9-qc-context)
8. [Exit Criteria](#exit-criteria)
9. [Integration with S9](#integration-with-s9)

---

## Overview

**Purpose:** Validate epic as a cohesive whole after all features complete

**What this validates:**
- All features working together as integrated system
- Cross-feature integration points
- Epic-wide architectural consistency
- Original epic goals achieved
- Ready for user testing

**Quality Standard:**
- All features integrated correctly
- Consistent patterns across features
- Original epic success criteria met
- Zero cross-feature issues
- Ready for S9.P3 (User Testing)

**Uses:** All 7 master dimensions + 5 S9 epic-specific dimensions = 12 total

---

## Master Dimensions (7) - Always Checked

**See `reference/validation_loop_master_protocol.md` for complete checklists.**

These universal dimensions apply to S9 Epic QC validation:

### Dimension 1: Empirical Verification
- [ ] All cross-feature interfaces verified from actual source code
- [ ] All integration points verified to exist (file:line references)
- [ ] All test commands verified to work (100% pass rate confirmed)
- [ ] All epic requirements traced to actual implementations

### Dimension 2: Completeness
- [ ] All features complete and integrated
- [ ] All cross-feature integration points implemented
- [ ] All epic success criteria implemented
- [ ] All error handling across features complete
- [ ] All edge cases across features handled

### Dimension 3: Internal Consistency
- [ ] No contradictions between features
- [ ] Naming conventions consistent across features
- [ ] Error handling approach consistent across features
- [ ] Coding patterns consistent across features
- [ ] Architectural patterns compatible

### Dimension 4: Traceability
- [ ] Every feature traces to epic requirement
- [ ] All integration points documented with source/destination
- [ ] All tests trace to requirements
- [ ] No orphan features (features without epic justification)

### Dimension 5: Clarity & Specificity
- [ ] No vague error messages across features
- [ ] Consistent logging format across features
- [ ] Clear naming conventions consistent across features
- [ ] Specific success criteria verification

### Dimension 6: Upstream Alignment
- [ ] Implementation matches original epic request ({epic_name}.txt)
- [ ] All original user goals achieved
- [ ] All acceptance criteria met
- [ ] No scope creep (no unrequested features)

### Dimension 7: Standards Compliance
- [ ] Follows project coding standards across all features
- [ ] Follows project structure/organization
- [ ] Uses project utilities consistently
- [ ] Import organization consistent across features
- [ ] Error handling follows project patterns

---

## S9 Epic QC Dimensions (5) - Context-Specific

These 5 dimensions are specific to S9.P2 Epic QC validation:

### Dimension 8: Cross-Feature Integration

**Question:** Do features integrate correctly with each other?

**Checklist:**

**Integration Point Verification:**
- [ ] All integration points between features identified
- [ ] All interface contracts verified (method signatures match)
- [ ] Data flow verified between all features
- [ ] Error propagation tested across feature boundaries

**Data Exchange:**
- [ ] Data structures compatible across features
- [ ] Data validation present at feature boundaries
- [ ] Data transformation correct between features
- [ ] Shared resources accessed correctly by all features

**Example Verification:**
```python
# Integration: Feature 01 -> Feature 02
from feature_01.PlayerDataManager import PlayerDataManager
from feature_02.RatingSystem import RatingSystem

# Verify data flows correctly
players = PlayerDataManager().get_all_players()
rated_players = RatingSystem().apply_ratings(players)

# Verify no data loss
assert len(rated_players) == len(players)
assert all(hasattr(p, 'rating') for p in rated_players)
```

---

### Dimension 9: Epic Cohesion

**Question:** Is the epic architecturally cohesive and consistent?

**Checklist:**

**Code Style Consistency:**
- [ ] Import style consistent across features
- [ ] Naming conventions consistent (snake_case, PascalCase)
- [ ] Docstring style consistent (Google style)
- [ ] Logging format consistent

**Pattern Consistency:**
- [ ] Design patterns compatible across features
- [ ] Similar operations use similar approaches
- [ ] Configuration access consistent
- [ ] Resource management consistent

**Common Violations:**

Wrong - Inconsistent patterns:
```python
# Feature 01: get_all_players()
# Feature 02: get_rated_players()  # Consistent
# Feature 03: fetch_recommendations()  # Different pattern
```

Correct - Consistent patterns:
```python
# Feature 01: get_all_players()
# Feature 02: get_rated_players()
# Feature 03: get_recommendations()  # Consistent
```

---

### Dimension 10: Error Handling Consistency

**Question:** Is error handling consistent across all features?

**Checklist:**

**Error Handling Approach:**
- [ ] Same exception hierarchy used across features
- [ ] Error messages follow same format
- [ ] Error logging consistent (level, context, format)
- [ ] Error recovery patterns consistent

**Boundary Error Handling:**
- [ ] Errors at feature boundaries handled consistently
- [ ] Upstream errors handled the same way
- [ ] Downstream errors propagated consistently
- [ ] Critical errors escalated the same way

**Common Violations:**

Wrong - Inconsistent error handling:
```python
# Feature 01: Raises DataProcessingError
except FileNotFoundError:
    raise DataProcessingError("Player data not found")

# Feature 03: Returns None
except FileNotFoundError:
    return None  # Inconsistent
```

Correct - Consistent error handling:
```python
# Feature 01: Raises DataProcessingError
except FileNotFoundError:
    raise DataProcessingError("Player data not found")

# Feature 03: Also raises DataProcessingError
except FileNotFoundError:
    raise DataProcessingError("Settings not found")
```

---

### Dimension 11: Architectural Alignment

**Question:** Are features architecturally aligned and compatible?

**Checklist:**

**Design Pattern Compatibility:**
- [ ] Patterns are compatible (Manager, System, Engine)
- [ ] No conflicting architectural approaches
- [ ] Feature boundaries clear and consistent
- [ ] Dependency directions correct (no circular)

**Layer Consistency:**
- [ ] All features follow same layering (if applicable)
- [ ] Data access patterns consistent
- [ ] Configuration patterns consistent
- [ ] API patterns consistent (if applicable)

---

### Dimension 12: Success Criteria Completion

**Question:** Does the epic meet all original success criteria?

**Checklist:**

**Original Epic Request:**
- [ ] Re-read original {epic_name}.txt
- [ ] All user goals achieved
- [ ] All stated requirements implemented
- [ ] No missing functionality

**Epic Success Criteria:**
- [ ] All S4 success criteria met (100%)
- [ ] Performance meets expectations
- [ ] User experience flow works correctly
- [ ] End-to-end scenarios all work

**Example Verification:**
```markdown
## Original Epic Goals (from {epic_name}.txt)

Goal 1: "Integrate ADP data into draft recommendations"
Verified: Feature 01 fetches ADP, Feature 02 applies ratings, Feature 03 uses in recommendations

Goal 2: "Allow users to adjust rating multipliers"
Verified: Feature 02 includes multiplier config, Feature 03 respects adjustments

Goal 3: "Generate top 200 ranked players"
Verified: Feature 03 outputs exactly 200 ranked players
```

---

## Total Dimensions: 12

**Every validation round checks ALL 12 dimensions:**
- 7 Master dimensions (universal)
- 5 Epic QC dimensions (context-specific)

**Process:** See master protocol for 3 consecutive clean rounds requirement

---

## What's Being Validated

### S9.P2: Epic QC Validation Loop

**Artifact:** Complete epic (all features together)

**Validates:**
- Cross-feature integration
- Epic-wide consistency
- Architectural alignment
- Original epic goals
- User experience flow

**Success Criteria:**
- All 12 dimensions checked every round
- 3 consecutive clean rounds achieved
- ZERO issues found
- Ready for user testing

---

## Fresh Eyes Patterns Per Round

**See master protocol for general fresh eyes principles.**

Epic-specific reading patterns:

### Round 1: Sequential Review + Integration Focus

**Pattern:**
1. Read features sequentially (Feature 01, 02, 03...)
2. Check integration points between features
3. Verify data flow across feature boundaries
4. Check all 12 dimensions

**Checklist:**
- [ ] All 12 dimensions checked (7 master + 5 epic)
- [ ] Integration points verified
- [ ] Data flow validated
- [ ] Tests passing (100%)

### Round 2: Reverse Order + Consistency Focus

**Pattern:**
1. Read features in reverse order (Feature 03, 02, 01...)
2. Focus on consistency across features
3. Compare patterns between features
4. Check all 12 dimensions

**Checklist:**
- [ ] All 12 dimensions checked
- [ ] Naming consistency verified
- [ ] Error handling consistency verified
- [ ] Architectural patterns compatible

### Round 3: Random Spot-Checks + Success Criteria

**Pattern:**
1. Random spot-check 3-5 integration points
2. Verify success criteria from original epic request
3. End-to-end scenario validation
4. Check all 12 dimensions

**Checklist:**
- [ ] All 12 dimensions checked
- [ ] Spot-checked integrations work correctly
- [ ] Success criteria met (100%)
- [ ] Ready for user testing

---

## Common Issues in S9 QC Context

### Issue 1: Integration Point Failures

**Symptom:** Features don't communicate correctly

**Example:**
```python
# Feature 01 returns List[Player]
# Feature 02 expects Dict[str, Player]
# Integration fails with TypeError
```

**Fix:** Verify interface contracts match, add data transformation if needed

---

### Issue 2: Inconsistent Error Handling

**Symptom:** Different features handle errors differently

**Example:**
```python
# Feature 01: raises exception on error
# Feature 02: returns None on error
# Integration breaks due to unexpected None
```

**Fix:** Standardize error handling approach across all features

---

### Issue 3: Missing Success Criteria

**Symptom:** Epic doesn't fully meet original request

**Example:**
```markdown
Original goal: "Generate top 200 players"
Implementation: Only generates top 100 players
```

**Fix:** Review original epic request and implement missing functionality

---

### Issue 4: Architectural Inconsistencies

**Symptom:** Features use incompatible patterns

**Example:**
```python
# Feature 01: Singleton pattern for config
# Feature 02: Instance-based config
# Conflict when accessing shared configuration
```

**Fix:** Standardize architectural patterns across features

---

## Exit Criteria

**Epic QC validation is COMPLETE when ALL of the following are true:**

**From Master Protocol:**
- [ ] 3 consecutive rounds with ZERO issues found
- [ ] All 7 master dimensions checked every round
- [ ] All 5 epic QC dimensions checked every round
- [ ] VALIDATION_LOOP_LOG.md complete with all rounds documented

**Epic QC Specific:**
- [ ] All cross-feature integration points work correctly
- [ ] Consistent patterns across all features
- [ ] Error handling consistent across features
- [ ] Architectural patterns compatible
- [ ] All success criteria met (100%)
- [ ] Original epic goals achieved
- [ ] Ready for user testing (S9.P3)

**Cannot exit if:**
- Any integration point fails
- Inconsistent patterns across features
- Missing success criteria
- Architectural conflicts
- Less than 3 consecutive clean rounds

---

## Integration with S9

### S9.P2: Epic QC Validation Loop

**When:** After S9.P1 (Epic Smoke Testing) passes

**Validates:** Complete epic (all features together)

**Process:**
1. Use this validation loop protocol
2. Check all 12 dimensions (7 master + 5 epic)
3. Exit when 3 consecutive clean rounds
4. Proceed to S9.P3 (User Testing)

**Threshold:** 3 consecutive clean rounds (ZERO issues)

---

## Example Validation Round Sequence

```text
Round 1: Sequential Review + Integration
- Read all features sequentially
- Check all 12 dimensions
- Issues found: 3
  - D8 (Integration): Feature 02 -> 03 data format mismatch
  - D9 (Cohesion): Inconsistent naming pattern in Feature 03
  - D12 (Success Criteria): Missing multiplier config validation
- Fix all 3 issues
- Clean counter: 0

Round 2: Reverse Order + Consistency
- Read features in reverse
- Check all 12 dimensions
- Issues found: 1
  - D10 (Error Handling): Feature 01 returns None, Feature 02 expects exception
- Fix issue
- Clean counter: 0

Round 3: Spot-Checks + Verification
- Random spot-check integration points
- Check all 12 dimensions
- Issues found: 0
- Clean counter: 1

Round 4: Repeat Validation
- Fresh eyes, different pattern
- Check all 12 dimensions
- Issues found: 0
- Clean counter: 2

Round 5: Final Sweep
- Complete re-read
- Check all 12 dimensions
- Issues found: 0
- Clean counter: 3 -> VALIDATION COMPLETE
```

---

## Summary

**S9 Epic QC Validation Loop:**
- **Extends:** Master Validation Loop Protocol (7 universal dimensions)
- **Adds:** 5 epic QC-specific dimensions
- **Total:** 12 dimensions checked every round
- **Process:** 3 consecutive clean rounds required
- **Focus:** Cross-feature integration, consistency, success criteria
- **Quality:** Epic works as cohesive whole, ready for user testing

**Key Principle:**
> "Every feature must work together seamlessly as a unified epic, with consistent patterns and complete success criteria achievement."

---

*End of S9 Epic QC Validation Loop v2.0*
