# Feature Research Notes - {Feature Name}

**Feature ID:** feature_{NN}_{name}
**Date Created:** {YYYY-MM-DD}
**Stage:** S2.P1.I1 (Feature-Level Discovery)
**Researcher:** {Agent ID or session}

---

## Quick Reference

**Purpose:** Document research findings from S2.P1.I1 feature-level discovery

**Key Outputs:**
- Technical findings
- Integration points identified
- External dependencies researched
- Questions and answers
- Recommended approach

**Next Steps:** Use findings to create spec.md and checklist.md in S2.P1.I2

---

## 1. Epic Context

**Epic Name:** {KAI-N - Epic Name}
**Epic Location:** `feature-updates/KAI-{N}-{epic_name}/`
**DISCOVERY.md Reference:** `KAI-{N}-{epic_name}/DISCOVERY.md`

**Relevant Epic Findings:**
- {Key finding 1 from DISCOVERY.md relevant to this feature}
- {Key finding 2 from DISCOVERY.md relevant to this feature}
- {Key finding 3 from DISCOVERY.md relevant to this feature}

**Epic-Level Decisions Affecting This Feature:**
- {Decision 1}
- {Decision 2}

---

## 2. Feature Scope Summary

**What this feature does:**
{2-3 sentence description of feature purpose and scope}

**In Scope:**
- {Item 1}
- {Item 2}
- {Item 3}

**Out of Scope:**
- {Item 1}
- {Item 2}

**Dependencies:**
- **Prerequisite Features:** {List features that must be complete first}
- **Dependent Features:** {List features that depend on this one}

---

## 3. Code Research Findings

### 3.1 Existing Code Examined

**Files Read:**
- `path/to/file1.py` (lines {X}-{Y}): {What was learned}
- `path/to/file2.py` (lines {X}-{Y}): {What was learned}
- `path/to/file3.py` (lines {X}-{Y}): {What was learned}

**Key Findings:**
1. **{Finding Category 1}:**
   - {Detailed finding}
   - **Impact on Feature:** {How this affects implementation}
   - **Files to Modify:** {List specific files}

2. **{Finding Category 2}:**
   - {Detailed finding}
   - **Impact on Feature:** {impact}
   - **Files to Modify:** {files}

3. **{Finding Category 3}:**
   - {Detailed finding}
   - **Impact on Feature:** {impact}
   - **Files to Modify:** {files}

### 3.2 Existing Patterns to Leverage

**Pattern 1: {Pattern Name}**
- **Location:** `path/to/example.py` (lines {X}-{Y})
- **Description:** {What the pattern does}
- **Application:** {How to apply to this feature}
- **Adaptation Needed:** {Any changes required}

**Pattern 2: {Pattern Name}**
- **Location:** {location}
- **Description:** {description}
- **Application:** {application}
- **Adaptation Needed:** {adaptation}

### 3.3 Code Gaps Identified

**Gap 1: {What's Missing}**
- **Description:** {Detailed description}
- **Impact:** {How this affects feature}
- **Solution Approach:** {How to address}

**Gap 2: {What's Missing}**
- **Description:** {description}
- **Impact:** {impact}
- **Solution Approach:** {solution}

---

## 4. Integration Points

### 4.1 Integration Point 1: {Name}

**Type:** {Shared data structure | Computational dependency | File system | API | Configuration}

**Interacting Components:**
- **This Feature:** {Component/module name}
- **Other Feature/Module:** {Name and location}

**Data Flow:**
```json
{Feature/Module A} --> {Data/Function} --> {Feature/Module B}
```

**Integration Requirements:**
- {Requirement 1}
- {Requirement 2}
- {Requirement 3}

**Risks:**
- {Risk 1 and mitigation}
- {Risk 2 and mitigation}

**Testing Approach:**
- {How to test this integration}

### 4.2 Integration Point 2: {Name}

[Same structure as Integration Point 1...]

---

## 5. External Dependencies

### 5.1 External Dependency 1: {Library/API Name}

**Purpose:** {Why this library/API is needed}

**Research Conducted:**
- **Documentation:** {URL to docs}
- **Version:** {Version researched}
- **License:** {License type}
- **Active Maintenance:** {Yes/No + evidence}

**Compatibility Analysis:**
- **Python Version:** {Compatible with project's Python version? Evidence?}
- **Test Environment:** {Works in test environment? Verified how?}
- **Known Issues:** {Any known compatibility issues? Links to issues?}

**Alternatives Considered:**
- **Alternative 1:** {Name} - {Why not chosen}
- **Alternative 2:** {Name} - {Why not chosen}

**Recommendation:** {Use this library | Use alternative | Build custom solution}

**Rationale:** {Why this recommendation}

**Experience/History:**
- {Any past experience with this library in this codebase}
- {Any lessons learned from similar features}

### 5.2 External Dependency 2: {Library/API Name}

[Same structure as Dependency 1...]

### 5.3 No External Dependencies

**If no external dependencies needed:**
- Feature can be implemented using only standard library and existing project code
- **Justification:** {Why no external dependencies needed}

---

## 6. Questions and Answers

### Pending Questions

| # | Question | Category | Asked | Priority |
|---|----------|----------|-------|----------|
| 1 | {Question text} | {Clarification \| Scope \| Preference \| Constraint} | {YYYY-MM-DD} | {High \| Medium \| Low} |
| 2 | {Question text} | {category} | {date} | {priority} |

### Resolved Questions

| # | Question | Answer | Impact | Resolved | Answered By |
|---|----------|--------|--------|----------|-------------|
| 1 | {Question text} | {Answer provided} | {How answer affects implementation} | {YYYY-MM-DD} | User |
| 2 | {Question text} | {Answer} | {Impact} | {date} | User |

---

## 7. Solution Approach

### 7.1 Recommended Implementation Approach

**Approach:** {High-level description of recommended solution}

**Rationale:**
- {Reason 1: Why this approach is best}
- {Reason 2: Alignment with codebase patterns}
- {Reason 3: User preference/requirements}

**Key Design Decisions:**
1. **{Decision 1}:** {Description and justification}
2. **{Decision 2}:** {Description and justification}
3. **{Decision 3}:** {Description and justification}

### 7.2 Alternative Approaches Considered

**Alternative 1: {Name}**
- **Description:** {How it would work}
- **Pros:** {Benefits}
- **Cons:** {Drawbacks}
- **Why Not Chosen:** {Reason}

**Alternative 2: {Name}**
- **Description:** {description}
- **Pros:** {pros}
- **Cons:** {cons}
- **Why Not Chosen:** {reason}

### 7.3 Implementation Complexity Assessment

**Complexity Level:** {Simple | Moderate | Complex}

**Factors:**
- **Code Volume:** {Small (<100 lines) | Medium (100-500 lines) | Large (>500 lines)}
- **Integration Complexity:** {Low | Medium | High}
- **Testing Complexity:** {Low | Medium | High}
- **Risk Level:** {Low | Medium | High}

**Estimated Effort:** {X hours implementation + Y hours testing}

---

## 8. Technical Specifications Preview

### 8.1 New Files to Create

| File Path | Purpose | Estimated Lines |
|-----------|---------|-----------------|
| `path/to/new_file1.py` | {Purpose} | ~{N} lines |
| `path/to/new_file2.py` | {Purpose} | ~{N} lines |

### 8.2 Existing Files to Modify

| File Path | Modification Type | Estimated Lines Changed |
|-----------|-------------------|-------------------------|
| `path/to/existing1.py` | {Add function \| Modify class \| Update logic} | ~{N} lines |
| `path/to/existing2.py` | {modification} | ~{N} lines |

### 8.3 Data Structures

**New Data Structures:**
```python
# Example data structure
class FeatureDataModel:
    def __init__(self, ...):
        self.field1 = ...
        self.field2 = ...
```

**Modified Data Structures:**
- **{Existing Class}:** Add fields `{field1}`, `{field2}`
- **{Existing Class}:** Modify method `{method_name}` to handle {new behavior}

### 8.4 Configuration Changes

**Config Files to Update:**
- `config/feature_config.json`: Add {section/key}
- `config/shared_config.py`: Add {constant/setting}

**New Config Requirements:**
- {Config item 1}: {Purpose and default value}
- {Config item 2}: {Purpose and default value}

---

## 9. Testing Considerations

### 9.1 Test Scope Preview

**Unit Tests Required:**
- {Component 1}: ~{N} test cases
- {Component 2}: ~{N} test cases
- Total Estimated: ~{N} unit tests

**Integration Tests Required:**
- {Integration point 1}: ~{N} test cases
- {Integration point 2}: ~{N} test cases
- Total Estimated: ~{N} integration tests

**Edge Cases to Test:**
- {Edge case 1}
- {Edge case 2}
- {Edge case 3}

### 9.2 Test Data Requirements

**Test Data Needed:**
- {Data type 1}: {Source or how to generate}
- {Data type 2}: {Source or how to generate}

**Existing Test Data:**
- {Can leverage existing test data? What exists?}

---

## 10. Risks and Mitigations

### Risk 1: {Risk Description}
- **Likelihood:** {Low | Medium | High}
- **Impact:** {Low | Medium | High}
- **Mitigation Strategy:** {How to prevent or handle}

### Risk 2: {Risk Description}
- **Likelihood:** {likelihood}
- **Impact:** {impact}
- **Mitigation Strategy:** {mitigation}

---

## 11. Next Steps

**Immediate Actions:**
1. ☐ Transfer findings to spec.md (S2.P1.I2)
2. ☐ Create checklist.md from pending questions (S2.P1.I2)
3. ☐ Resolve all pending questions before S2.P1.I3
4. ☐ Reference this document in spec.md "Research Notes" section

**Future References:**
- This document will be referenced during:
  - S4: Test strategy planning (integration points, edge cases)
  - S5: Implementation planning (code structure, external dependencies)
  - S6: Implementation execution (technical specifications)
  - S8: Post-feature alignment (integration points)

---

## 12. Research Log

| Timestamp | Activity | Duration | Outcome |
|-----------|----------|----------|---------|
| {YYYY-MM-DD HH:MM} | Read {files} | {X min} | {Key findings} |
| {YYYY-MM-DD HH:MM} | Research {library} | {X min} | {Decision made} |
| {YYYY-MM-DD HH:MM} | User Q&A | {X min} | {N questions resolved} |

**Total Research Time:** {X} hours

---

*This research document serves as the foundation for spec.md and will be referenced throughout the feature development lifecycle.*
