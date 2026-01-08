# STAGE 2b.5: Specification Validation Phase Guide

**Guide Version:** 1.0
**Created:** 2026-01-06
**Prerequisites:** STAGE_2b complete (Specification Phase PASSED)
**Next Stage:** stages/stage_2/phase_2_refinement.md

---

## 🚨 MANDATORY READING PROTOCOL

**Before starting this stage:**
1. Use Read tool to load THIS ENTIRE GUIDE
2. Acknowledge critical requirements (see "Critical Rules" section below)
3. Verify prerequisites (see "Prerequisites Checklist" section below)
4. Update feature README.md Agent Status with guide name + timestamp

**DO NOT proceed without reading this guide.**

**After session compaction:**
- Check feature README.md Agent Status for current phase
- READ THIS GUIDE again (full guide, not summary)
- Continue from "Next Action" in Agent Status

---

## Quick Start

**What is this stage?**
Specification Validation Phase is a critical quality gate where you assume everything in the spec and checklist is wrong, inaccurate, or incomplete, then conduct deep research to validate every claim and self-resolve as many checklist questions as possible before user interaction.

**When do you use this guide?**
- STAGE_2b complete (Phase 2.5 Spec-to-Epic Alignment Check PASSED)
- spec.md has requirements with traceability
- checklist.md has open questions
- Ready to validate and improve specification quality

**Key Outputs:**
- ✅ All spec claims validated with additional evidence
- ✅ Checklist questions self-resolved where possible (research-based answers)
- ✅ New checklist questions identified through deeper investigation
- ✅ Multi-approach questions flagged for user decision
- ✅ Specification quality significantly improved before user interaction

**Time Estimate:**
30-45 minutes (1 phase with 4 steps)

**Exit Condition:**
Validation Phase is complete when all spec claims are validated, maximum checklist questions are self-resolved through research, and only genuine unknowns or multi-approach decisions remain for user input.

---

## Critical Rules

```
┌─────────────────────────────────────────────────────────────┐
│ CRITICAL RULES - These MUST be copied to README Agent Status │
└─────────────────────────────────────────────────────────────┘

1. ⚠️ ASSUME EVERYTHING IS WRONG (validation mindset)
   - Treat spec.md as hypotheses to validate (not facts)
   - Treat checklist.md as assumptions to research (not final questions)
   - Question every claim, requirement, and implementation detail
   - Validate with additional evidence from codebase

2. ⚠️ DEEP RESEARCH VALIDATION (beyond Phase 1 research)
   - Go deeper than initial research (read more files, check patterns)
   - Look for counter-evidence that contradicts spec claims
   - Find actual examples of similar implementations
   - Verify field mappings, data types, naming conventions

3. ⚠️ SELF-RESOLVE CHECKLIST QUESTIONS (reduce user burden)
   - Research answers to checklist questions where possible
   - Only leave questions that require user preference/decision
   - Convert research findings into spec requirements with sources
   - Mark resolved questions [x] with research evidence

4. ⚠️ IDENTIFY NEW QUESTIONS (comprehensive discovery)
   - Look for missing edge cases through deeper investigation
   - Find additional implementation decisions not yet considered
   - Discover integration points or dependencies missed in initial research
   - Add new questions to checklist based on validation findings

5. ⚠️ FLAG MULTI-APPROACH QUESTIONS (user decision required)
   - If multiple valid approaches exist, leave as user question
   - Document all viable options with pros/cons
   - Don't make arbitrary choices between valid alternatives
   - Let user decide on architectural/design preferences

6. ⚠️ UPDATE SPEC IMMEDIATELY (real-time validation)
   - Add new requirements based on validation findings
   - Update existing requirements with additional evidence
   - Remove or modify incorrect claims discovered during validation
   - Maintain requirement traceability (Source: Validation Research)
```

---

## Critical Decisions Summary

**Validation Phase has 1 major decision point per checklist question:**

### Decision Point: Can This Question Be Self-Resolved?
**Question:** Can this checklist question be answered through additional research?
- **Single clear answer found:** Self-resolve, add to spec as requirement, mark [x] in checklist
- **Multiple valid approaches found:** Flag for user decision, document all options
- **No research-based answer possible:** Leave as user question (preference/business decision)
- **Impact:** Reduces user burden by answering researchable questions, improves spec quality

---

## Prerequisites Checklist

**Verify BEFORE starting Validation Phase:**

□ **STAGE_2b complete:**
  - Phase 2 complete: spec.md has requirements with traceability
  - Phase 2 complete: checklist.md has open questions
  - Phase 2.5 complete: Spec-to-Epic Alignment Check PASSED

□ **Files exist and are current:**
  - feature_{N}_{name}/spec.md exists with Epic Intent and requirements
  - feature_{N}_{name}/checklist.md exists with open questions
  - epic/research/{FEATURE_NAME}_DISCOVERY.md exists from Phase 1

□ **Research foundation exists:**
  - Phase 1.5 Research Completeness Audit PASSED
  - Evidence collected from initial research phase

□ **Agent Status updated:**
  - Last guide: stages/stage_2/phase_1_specification.md
  - Current phase: Ready to start Validation Phase

**If any prerequisite fails:**
- ❌ Do NOT start Validation Phase
- Complete missing prerequisites first
- Return to STAGE_2b if Phase 2.5 not passed

---

## Phase 2.75: Specification Validation

**Goal:** Validate all spec claims and self-resolve maximum checklist questions through deep research

**⚠️ CRITICAL:** Assume everything in spec and checklist is wrong until proven right with evidence.

---

### Step 2.75.1: Validate All Spec Claims

**Validation mindset:** Every requirement in spec.md is a hypothesis to validate.

**For EACH requirement in spec.md:**

```markdown
## Spec Validation Audit

### Requirement 1: {Name}

**Original Claim:** {What spec currently says}

**Validation Research:**
- Additional files checked: {List files read for validation}
- Evidence found: {Specific evidence supporting or contradicting claim}
- Counter-evidence: {Any evidence that contradicts the claim}

**Validation Result:**
- ✅ CONFIRMED: Claim is accurate (evidence: {cite specific evidence})
- ⚠️ MODIFIED: Claim needs adjustment (change: {what to modify})
- ❌ INCORRECT: Claim is wrong (correction: {what's actually true})

**Action Taken:**
- {No change needed / Updated spec.md / Added new requirement}
```

**Example validation research:**

```markdown
### Requirement 2: Create CrewMemberS3VO with Essential Fields

**Original Claim:** "Include nested objects: crewMemberSchedulePeriod, qualifications, historicalAssignments"

**Validation Research:**
- Additional files checked: 
  - CrewMemberSchedulePeriodBatchResponseVO.java (read full structure)
  - CrewQualificationBatchResponseVO.java (read field definitions)
  - Searched for "historicalAssignments" usage patterns
- Evidence found: 
  - CrewMemberSchedulePeriodBatchResponseVO has 29 fields (not just basic fields)
  - QualificationBatchResponseVO has aircraftType, qualified, expirationDate fields
  - historicalAssignments is List<Long> in current code, but S3 schema shows full objects
- Counter-evidence: 
  - S3 schema shows historicalAssignments as full assignment objects, not just IDs

**Validation Result:**
- ⚠️ MODIFIED: Need to clarify historicalAssignments structure (full objects vs IDs)

**Action Taken:**
- Added Question 5 to checklist about historicalAssignments structure
- Updated requirement to note discrepancy between current code and S3 schema
```

**Research deeper than Phase 1:**
- Read complete file contents (not just searched patterns)
- Check multiple similar classes for consistency
- Look for existing conversion examples
- Verify data type mappings
- Check naming convention patterns

---

### Step 2.75.2: Self-Resolve Checklist Questions

**For EACH question in checklist.md:**

**Research approach:**
1. **Can this be answered by reading more code?** → Research and resolve
2. **Are there existing patterns to follow?** → Research and resolve
3. **Is this a user preference/business decision?** → Leave for user
4. **Are there multiple valid approaches?** → Document options, leave for user

**Self-resolution process:**

```markdown
## Checklist Question Research

### Question 1: {Title}

**Research Conducted:**
- Files examined: {List additional files read}
- Patterns found: {Existing patterns in codebase}
- Similar implementations: {Examples of similar code}

**Research Findings:**
- {Finding 1 with evidence}
- {Finding 2 with evidence}
- {Finding 3 with evidence}

**Resolution Decision:**
- ✅ SELF-RESOLVED: Clear answer found through research
- ⚠️ MULTI-APPROACH: Multiple valid options found (user decision needed)
- ❓ USER-PREFERENCE: Business/design decision (user input required)

**If SELF-RESOLVED:**
- Answer: {Research-based answer}
- Evidence: {Cite specific code/patterns found}
- Action: Mark [x] in checklist, add requirement to spec

**If MULTI-APPROACH or USER-PREFERENCE:**
- Options documented: {List all viable approaches}
- Recommendation updated: {Best option based on research}
- Leave for user decision in STAGE_2c
```

**Example self-resolution:**

```markdown
### Question 1: Date Field Format in S3 Schema

**Research Conducted:**
- Files examined: 
  - AssignmentBatchResponseVO.java (current date field types)
  - Jackson configuration in application.yml
  - Existing JSON serialization examples
- Patterns found: 
  - Current VOs use String for dateTime fields (beginDateTime, endDateTime)
  - Jackson auto-converts Calendar to ISO 8601 strings
  - No custom date serializers configured

**Research Findings:**
- AssignmentBatchResponseVO already uses String for beginDateTime/endDateTime
- S3 schema matches existing pattern (ISO 8601 strings)
- No conversion needed - direct field mapping

**Resolution Decision:**
- ✅ SELF-RESOLVED: Use String fields (matches existing pattern)

**Answer:** Use String fields for all date/time values (ISO 8601 format)
**Evidence:** AssignmentBatchResponseVO.java lines 15-16 show String beginDateTime/endDateTime
**Action:** Mark [x] in checklist, add requirement to spec
```

---

### Step 2.75.3: Identify New Questions Through Deep Investigation

**Deep investigation areas:**

**1. Integration Points:**
- How does this feature integrate with existing systems?
- Are there dependency injection requirements?
- What about transaction boundaries?

**2. Error Handling:**
- What happens when conversion fails?
- How are null/missing values handled?
- Are there validation requirements?

**3. Performance Considerations:**
- Are there memory implications for large datasets?
- Should conversion be streamed or batched?
- Are there caching considerations?

**4. Testing Requirements:**
- What test data is needed?
- Are there existing test utilities to leverage?
- What edge cases need coverage?

**5. Configuration:**
- Are there configurable parameters?
- Environment-specific behavior?
- Feature flags or toggles?

**Research process:**
```bash
# Look for similar conversion methods
grep -r "convertTo.*Response" --include="*.java"

# Check error handling patterns
grep -r "try.*catch" service/ota-info-service-application/src/main/java/com/swacorp/crew/sched/ota/info/application/service/

# Look for validation patterns
grep -r "@Valid\|@NotNull\|@NotEmpty" --include="*.java"

# Check configuration patterns
find . -name "application*.yml" -o -name "*.properties"
```

**Add new questions to checklist:**
```markdown
### Question 5: {New Question} (NEW - from validation research)
- [ ] **OPEN**

**Context:** During validation, discovered {what was found}

**Research Evidence:** {What research revealed this question}

**Options:**
A. {Option based on research}
B. {Alternative option}
C. {Third option if applicable}

**Recommendation:** {Best option based on research findings}

**Why this is a question:** {Why user input is needed despite research}
```

---

### Step 2.75.4: Update Spec with Validation Findings

**Add new requirements based on validation:**

```markdown
### Requirement 8: {New Requirement from Validation}

**Description:** {What this requirement specifies}

**Source:** Validation Research (Phase 2.75)
**Traceability:** Discovered during spec validation through {research method}

**Implementation:**
- {Implementation details based on research}
- {Evidence from codebase}

**Technical Details:**
- {Specific technical requirements}
- {Integration points discovered}
- {Error handling requirements}

**Evidence:**
- File: {specific file and line numbers}
- Pattern: {existing pattern found}
- Similar implementation: {reference to similar code}
```

**Update existing requirements with additional evidence:**

```markdown
### Requirement 2: Create CrewMemberS3VO with Essential Fields (UPDATED)

**Description:** {Original description}

**Source:** Epic notes Step 2, Task 2 + Validation Research
**Traceability:** Direct user request + additional validation evidence

**Implementation:**
- {Original implementation}
- **Validation Update:** {Additional details from validation research}

**Additional Evidence (from validation):**
- CrewMemberSchedulePeriodBatchResponseVO has 29 fields (full structure documented)
- QualificationBatchResponseVO structure verified (aircraftType, qualified, expirationDate)
- Historical assignments mapping clarified through S3 schema comparison
```

**Mark resolved checklist questions:**

```markdown
### Question 1: Date Field Format in S3 Schema
- [x] **RESOLVED:** Use String fields (matches existing pattern)

**Research Answer:**
AssignmentBatchResponseVO already uses String for beginDateTime/endDateTime fields. S3 schema matches this existing pattern. No conversion needed - direct field mapping.

**Evidence:**
- File: AssignmentBatchResponseVO.java lines 15-16
- Pattern: String beginDateTime, String endDateTime
- Consistency: S3 schema uses same format

**Implementation Impact:**
- Use String fields for all date/time values in S3 VOs
- Direct field mapping from existing VOs (no conversion logic needed)
- Follow ISO 8601 format as shown in S3 schema examples
```

---

### Step 2.75.5: Update Agent Status

```markdown
## Agent Status

**Last Updated:** {YYYY-MM-DD HH:MM}
**Current Phase:** VALIDATION_PHASE
**Current Step:** Phase 2.75 - Specification Validation Complete
**Current Guide:** stages/stage_2/phase_2b5_specification_validation.md
**Guide Last Read:** {YYYY-MM-DD HH:MM}
**Critical Rules from Guide:**
- Assume everything is wrong until validated
- Self-resolve checklist questions through research
- Identify new questions through deep investigation
- Flag multi-approach questions for user decision

**Progress:** Validation Phase COMPLETE
**Next Action:** Refinement Phase (Interactive Question Resolution)
**Next Guide:** stages/stage_2/phase_2_refinement.md
**Blockers:** None

**Validation Results:**
- Spec claims validated: {N} confirmed, {M} modified, {K} corrected
- Checklist questions self-resolved: {X} resolved, {Y} remaining
- New questions identified: {Z} added to checklist
- Multi-approach questions: {A} flagged for user decision
```

---

## Completion Criteria

**Validation Phase (STAGE_2b.5) is COMPLETE when ALL of these are true:**

□ **All spec claims validated:**
  - Every requirement researched with additional evidence
  - Incorrect claims corrected or removed
  - New requirements added based on validation findings
  - All claims have supporting evidence from codebase

□ **Maximum checklist questions self-resolved:**
  - Research conducted for every checklist question
  - Questions with clear research-based answers marked [x] resolved
  - Resolved questions converted to spec requirements
  - Only genuine unknowns or multi-approach decisions remain open

□ **Deep investigation completed:**
  - Integration points researched and documented
  - Error handling patterns investigated
  - Performance considerations identified
  - Testing requirements discovered
  - Configuration needs assessed

□ **New questions identified:**
  - Additional unknowns discovered through deep research
  - Edge cases identified that weren't in original checklist
  - Multi-approach decisions flagged for user input
  - All new questions added to checklist with research context

□ **Documentation updated:**
  - spec.md updated with validation findings
  - checklist.md updated with resolved questions and new questions
  - Agent Status updated with validation results
  - Evidence documented for all changes

**Exit Condition:** Validation Phase is complete when spec quality is significantly improved through validation research, maximum questions are self-resolved, and only genuine user decisions remain for STAGE_2c.

---

## Next Stage

**After completing Validation Phase:**

→ **Proceed to:** stages/stage_2/phase_2_refinement.md

**What happens in STAGE_2c:**
- Phase 3: Interactive Question Resolution (remaining questions only)
- Phase 4: Dynamic Scope Adjustment
- Phase 5: Cross-Feature Alignment
- Phase 6: Acceptance Criteria & User Approval

**Prerequisites for STAGE_2c:**
- Validation Phase complete (from this guide)
- spec.md has validated requirements
- checklist.md has minimal remaining questions (only user decisions)

**Expected improvement:** 50-70% reduction in user questions due to self-resolution through research

---

## Benefits of Validation Phase

**Quality Improvements:**
- Spec accuracy increased through validation research
- Implementation details verified against actual codebase
- Edge cases discovered before user interaction
- Technical decisions made based on existing patterns

**User Experience Improvements:**
- Fewer questions for user (only genuine decisions needed)
- Better quality questions (well-researched options)
- Faster user interaction (less back-and-forth)
- More confident recommendations (evidence-based)

**Development Efficiency:**
- Reduced rework due to better specifications
- Fewer implementation surprises (validated against codebase)
- Better alignment with existing patterns
- More complete requirements before implementation

---

**END OF STAGE_2b.5 - SPECIFICATION VALIDATION PHASE GUIDE**
