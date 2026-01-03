# Feature Todo Template

**Filename:** `todo.md`
**Location:** `feature-updates/{epic_name}/feature_XX_{name}/todo.md`
**Created:** {YYYY-MM-DD} (Stage 5a)

**Purpose:** Implementation task list with complete traceability, created during Stage 5a (TODO Creation).

---

## Template

```markdown
# Feature TODO: {feature_name}

**Part of Epic:** {epic_name}
**Created:** {YYYY-MM-DD} (Stage 5a)
**Status:** {IN PROGRESS / COMPLETE}

---

## Verification Summary

**24 Verification Iterations:** {PASSED / IN PROGRESS}
**Iteration 4a (TODO Specification Audit):** {PASSED / PENDING}
**Iteration 23a (Pre-Implementation Spec Audit):** {PASSED / PENDING}
**Iteration 24 (Implementation Readiness):** {PASSED / PENDING}

**Ready to Implement?** {YES / NO}

---

## Implementation Tasks

### Phase 1: Core Algorithm Implementation

**Task 1: Implement {AlgorithmName}**
**File:** `{path/to/file.py}`
**Function/Class:** `{function_or_class_name}`
**Spec Reference:** spec.md - Section "Algorithms" → Algorithm 1
**Description:** {Brief description of what this task does}

**Subtasks:**
- [ ] Create function signature
- [ ] Implement step 1: {description}
- [ ] Implement step 2: {description}
- [ ] Handle edge case: {case 1}
- [ ] Handle edge case: {case 2}
- [ ] Add docstring
- [ ] Add type hints

**Acceptance:**
- Returns correct output for normal inputs
- Handles all edge cases as specified
- Follows project coding standards

**Status:** {NOT STARTED / IN PROGRESS / COMPLETE}

---

**Task 2: Implement {DataStructure}**
**File:** `{path/to/file.py}`
**Class:** `{class_name}`
**Spec Reference:** spec.md - Section "Data Structures" → Data Structure 1
**Description:** {Brief description}

**Subtasks:**
- [ ] {Subtask 1}
- [ ] {Subtask 2}

**Status:** {NOT STARTED / IN PROGRESS / COMPLETE}

{Continue for all Phase 1 tasks...}

---

### Phase 2: Integration Implementation

**Task 5: Implement Interface to {OtherFeature}**
**File:** `{path/to/file.py}`
**Method:** `{method_name}`
**Spec Reference:** spec.md - Section "Interfaces" → Interface 1
**Description:** {Description}

**Subtasks:**
- [ ] {Subtask 1}
- [ ] {Subtask 2}

**Status:** {NOT STARTED / IN PROGRESS / COMPLETE}

{Continue for all Phase 2 tasks...}

---

### Phase 3: Error Handling Implementation

**Task 8: Implement Error Handling for {Scenario}**
**File:** `{path/to/file.py}`
**Spec Reference:** spec.md - Section "Error Handling" → Error Scenario 1
**Description:** {Description}

**Subtasks:**
- [ ] {Subtask 1}
- [ ] {Subtask 2}

**Status:** {NOT STARTED / IN PROGRESS / COMPLETE}

{Continue for all Phase 3 tasks...}

---

### Phase 4: Testing Implementation

**Task 10: Write Unit Tests for {Algorithm}**
**File:** `tests/feature_XX_{name}/test_{module}.py`
**Spec Reference:** spec.md - Section "Testing Strategy"
**Description:** {Description}

**Subtasks:**
- [ ] Test normal inputs
- [ ] Test edge cases
- [ ] Test error conditions
- [ ] Verify 100% code coverage for algorithm

**Status:** {NOT STARTED / IN PROGRESS / COMPLETE}

{Continue for all Phase 4 tasks...}

---

## Algorithm Traceability Matrix

**Purpose:** Map every algorithm in spec.md to exact code location

| Algorithm (from spec.md) | File | Function/Method | Line Numbers | Status |
|---------------------------|------|-----------------|--------------|--------|
| Algorithm 1: {name} | {file.py} | {function_name()} | Lines {N}-{M} | {IMPLEMENTED / TODO} |
| Algorithm 2: {name} | {file.py} | {function_name()} | Lines {N}-{M} | {IMPLEMENTED / TODO} |

{All algorithms from spec.md MUST be listed here}

---

## Interface Verification Matrix

**Purpose:** Verify all interfaces match actual implementations

| Interface (from spec.md) | Provider File | Provider Method | Consumer File | Consumer Method | Verified |
|---------------------------|---------------|-----------------|---------------|-----------------|----------|
| Interface 1: {name} | {provider.py} | {method()} | {consumer.py} | {method()} | {YES / NO} |
| Interface 2: {name} | {provider.py} | {method()} | {consumer.py} | {method()} | {YES / NO} |

{All interfaces from spec.md MUST be listed here}

---

## Integration Points Checklist

**Purpose:** Track all integration points

| Integration Point | This Feature | Other Feature | Data Passed | Interface | Status |
|-------------------|--------------|---------------|-------------|-----------|--------|
| To Feature 02 | Provides | Consumes | {data description} | {interface name} | {IMPLEMENTED / TODO} |
| From Feature 01 | Consumes | Provides | {data description} | {interface name} | {IMPLEMENTED / TODO} |

{All integration points from spec.md MUST be listed here}

---

## Progress Tracking

**Total Tasks:** {N}
**Completed:** {X}
**In Progress:** {Y}
**Not Started:** {Z}

**Overall Progress:** {X/N} ({percentage}%)

**Current Phase:** Phase {N} - {phase name}
**Next Task:** Task {N} - {task name}

---

## Blockers

{List any blockers preventing task completion}

**Blocker 1:**
- **Task Affected:** Task {N}
- **Issue:** {Description of blocker}
- **Resolution:** {How to resolve or "TBD"}
- **Status:** {BLOCKED / RESOLVED}

{If no blockers: "No blockers"}

---

## Completion Checklist

**Before marking TODO complete:**
- [ ] ALL tasks marked COMPLETE
- [ ] Algorithm Traceability Matrix: All algorithms implemented
- [ ] Interface Verification Matrix: All interfaces verified
- [ ] Integration Points: All integration points implemented
- [ ] All unit tests written and passing (100%)
- [ ] No blockers remain

**TODO Complete?** {YES / NO}
```