# Guide Update Proposal - KAI-10

**Epic:** KAI-10-architectural_refactoring_configuration_management
**Created:** 2026-02-17
**Phase:** S10.P1 (applied early - epic paused mid-S2 to capture lessons)

---

## Summary

**Lessons Analyzed:**
- Epic lessons: 2
- Feature lessons: 0 (features not yet implemented)
- Total: 2 lessons

**Proposals:**
- P0 (Critical): 1
- P1 (High): 1
- P2 (Medium): 0
- P3 (Low): 0
- Total: 2 proposals

**Both proposals affect:** `stages/s1/s1_epic_planning.md` - Step 5.7.5 (Feature Dependency Analysis)

---

## Proposal P0-1: Add Downstream Wiring Dependency Check to Step 5.7.5

**Lesson Learned:**
> "Features 01-08 were placed in a single S2 group. 7 secondary agents launched for Features 02-08 in parallel with Feature 01. During Feature 01's S2.P1.I2 (checklist resolution), user noticed that Features 02-08 all depend on Feature 01's spec. All 7 secondary agents had to be paused mid-S2. Agent used shallow check: 'Can I identify WHAT to build?' Should use deep check: 'Do I need another feature's spec to describe HOW it integrates?' Any feature that sits downstream in a data/dependency flow AND must interface with an upstream feature's output structure has a spec-level dependency — especially when the upstream feature is actively defining that output structure in S2."

**Source:** `epic_lessons_learned.md` - Lesson 2 (S2 - Feature Deep Dives)

**Root Cause:**
The Step 5.7.5 analysis questions only prompt the agent to ask "does this feature need other features' SPECS?" but don't give enough scaffolding to catch the subtle case where a feature can identify WHAT to build (from Discovery) but cannot describe HOW it integrates without knowing the upstream feature's output structure.

**Affected Guide:**
- `stages/s1/s1_epic_planning.md` - Step 5.7.5: Analyze Feature Dependencies

**Current State (BEFORE):**
```markdown
**For EACH feature:**

1. **Spec Dependencies (matters for S2 parallelization):**
   - Does this feature need other features' SPECS to write its own spec?
   - Example: Feature B needs to know Feature A's API to write integration spec
   - → Creates S2 dependency (Feature A must complete S2 before Feature B starts)

2. **Implementation Dependencies (matters for S5-S8, NOT S2):**
   - Does this feature need other features' CODE to build its implementation?
   - Example: Feature B calls Feature A's functions
   - → Creates S5 dependency (Feature A must complete S5-S8 before Feature B starts)
   - → Does NOT affect S2 parallelization (both can research/specify in parallel)

**Decision Criteria for Grouping:**
- **Spec-level dependency → Different group** (affects S2 parallelization)
- **Implementation dependency only → Same group** (doesn't affect S2)
- **No dependencies → Group 1** (can parallelize freely)
```

**Proposed Change (AFTER):**
```markdown
**For EACH feature:**

1. **Spec Dependencies (matters for S2 parallelization):**
   - Does this feature need other features' SPECS to write its own spec?
   - Example: Feature B needs to know Feature A's API to write integration spec
   - → Creates S2 dependency (Feature A must complete S2 before Feature B starts)

   **🚨 Use the DEEP CHECK, not the shallow check:**
   - ❌ Shallow check (WRONG): "Can I identify WHAT to build from Discovery?"
   - ✅ Deep check (CORRECT): "Can I write a COMPLETE spec without knowing upstream's output structure?"

   **Ask for EACH feature:**
   a. What is the output/interface that the upstream feature will define in S2?
   b. Does MY spec need to describe how I use that interface?
   c. Is that interface fully defined in Discovery, or will it be defined in upstream's S2?
   d. **If the interface will be defined in upstream's S2 → spec-level dependency exists**

   **Common patterns that indicate spec-level dependency:**
   - "My feature wires CLI args into [upstream's refactored constructors/APIs]" → SPEC DEP
   - "My feature calls [upstream's functions/endpoints] that don't exist yet" → SPEC DEP
   - "My feature's behavior depends on decisions upstream is making in S2" → SPEC DEP

2. **Implementation Dependencies (matters for S5-S8, NOT S2):**
   - Does this feature need other features' CODE to build its implementation?
   - Example: Feature B calls Feature A's functions
   - → Creates S5 dependency (Feature A must complete S5-S8 before Feature B starts)
   - → Does NOT affect S2 parallelization (both can research/specify in parallel)

**Decision Criteria for Grouping:**
- **Spec-level dependency → Different group** (affects S2 parallelization)
- **Implementation dependency only → Same group** (doesn't affect S2)
- **No dependencies → Group 1** (can parallelize freely)

**Historical Warning:**
KAI-10 placed Features 02-08 in the same group as Feature 01. Features 02-08 add CLI args that wire into Feature 01's refactored constructors. They could identify WHAT CLI args to add (from Discovery) but could NOT write a complete spec for HOW those args wire through without Feature 01's spec. All 7 secondary agents had to be paused mid-S2 to restructure.
```

**Rationale:**
The "deep vs shallow check" distinction directly prevents the failure mode. The concrete questions (a-d) give agents a systematic check rather than relying on intuition. The "wiring" pattern example directly mirrors the KAI-10 failure case.

**Impact Assessment:**
- **Who benefits:** All agents performing Step 5.7.5 dependency analysis for any epic with a "foundation" feature whose outputs are used by downstream features
- **When it helps:** During S1 Step 5.7.5, when grouping features for S2 parallelization
- **Severity if unfixed:** Critical — causes secondary agents to do wasted work and requires restructuring mid-S2, adding hours of overhead

**User Decision:** [x] Approve  [ ] Modify  [ ] Reject  [ ] Discuss

---

## Proposal P1-1: Add Integration/Test/Framework Feature Warning to Step 5.7.5

**Lesson Learned:**
> "Agent incorrectly classified Feature 09 (integration_test_framework) as having no spec-level dependencies. Agent thought: 'Integration framework needs other features' CODE (implementation dependency), but not their SPECS.' Reality: Integration test framework DOES need other features' specs because it must know what CLI arguments each script has, what E2E test modes exist, and must define test scenarios based on CLI behaviors."

**Source:** `epic_lessons_learned.md` - Lesson 1 (S1 - Epic Planning)

**Root Cause:**
Step 5.7.5 doesn't call out the well-known pattern that integration/test/framework features almost always have spec-level dependencies on the features they integrate/test.

**Affected Guide:**
- `stages/s1/s1_epic_planning.md` - Step 5.7.5: Analyze Feature Dependencies

**Current State (BEFORE):**
No special callout for integration/test/framework features.

**Proposed Change (AFTER):**
Add the following note under the Decision Criteria section in Step 5.7.5:

```markdown
**⚠️ Special Cases — Almost Always Have Spec Dependencies:**
- **Integration features** (e.g., "integrate X with Y") — need both X and Y specs
- **Test/framework features** (e.g., "integration test framework", "test runner") — need specs of what they test
- **Orchestration features** (e.g., "master runner", "pipeline coordinator") — need specs of what they orchestrate
- **Wrapper/adapter features** (e.g., "CLI wrapper for existing API") — need the API spec

For these feature types, default assumption is SPEC DEPENDENCY EXISTS unless you can prove otherwise.
```

**Rationale:**
These feature types share a structural property: they describe HOW to interact with other features, which requires knowing those features' specifications. Making this explicit as a "special case" shortcut prevents agents from having to reason through the deep check for obvious cases.

**Impact Assessment:**
- **Who benefits:** All agents doing Step 5.7.5 when epic includes test/integration/framework features
- **When it helps:** During S1 Step 5.7.5 grouping
- **Severity if unfixed:** High — integration/test features are common in epics, and misclassifying them causes wasted parallel work

**User Decision:** [x] Approve  [ ] Modify  [ ] Reject  [ ] Discuss

---

## Also Affects: common_mistakes.md

Both lessons suggest adding entries to `reference/common_mistakes.md` under the S1 section. This would be a sub-part of each proposal — if either proposal above is approved, common_mistakes.md should also be updated with the corresponding anti-pattern.

Current common_mistakes.md S1 section:
```
### S1: Epic Planning
- ❌ Creating a documentation feature (handled in S7.P3 + S10, unless user explicitly requests it)
```

Proposed addition (if P0-1 approved):
```
- ❌ Using shallow check for spec dependencies ("Can I identify WHAT to build?") instead of deep check ("Can I write a COMPLETE spec without upstream's output structure?")
```

Proposed addition (if P1-1 approved):
```
- ❌ Assuming integration/test/framework features have no spec dependencies — they almost always do
```
