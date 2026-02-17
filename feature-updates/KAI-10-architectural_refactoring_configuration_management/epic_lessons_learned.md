## Epic Lessons Learned: KAI-10 - Architectural Refactoring of Configuration Management

**Created:** 2026-02-13
**Purpose:** Document lessons learned during epic implementation to improve future epics and workflow guides

---

## Planning Phase Lessons (S1-S4)

### S1 - Epic Planning

#### Lesson 1: Integration/Test Features Have Hidden Spec Dependencies

**Date:** 2026-02-14
**Stage:** S1 Step 5.7.5 (Feature Dependency Analysis)

**What Happened:**
- Agent incorrectly classified Feature 09 (integration_test_framework) as having no spec-level dependencies
- Placed all 9 features in a single group for full parallelization
- Generated handoff packages for all 8 secondary agents (Features 02-09)

**The Mistake:**
Agent thought: "Integration framework needs other features' CODE (implementation dependency), but not their SPECS"

**Reality:**
Integration test framework DOES need other features' specs because:
- Must know what CLI arguments each script has (from Features 02-08 specs)
- Must know what E2E test modes exist (from Features 02-08 specs)
- Must define test scenarios based on CLI behaviors (from Features 02-08 specs)

**How It Was Caught:**
- User questioned: "Does the integration test framework not require all the other script's configs planned out?"
- Agent re-assessed and realized the spec-level dependency was missed

**Root Cause:**
1. Agent conflated "implementation dependency" (needs CODE) with "spec dependency" (needs SPEC information)
2. Didn't rigorously ask: "To write MY spec.md, what information do I need from THEIR spec.md?"
3. Missed the obvious: Integration/test features BY DEFINITION need to know what they're integrating/testing

**Correct Grouping:**
- Group 1: Features 01-08 (all can spec independently using Discovery + current code)
- Group 2: Feature 09 (needs Group 1's specs to write its own spec)

**Prevention:**
For each feature during dependency analysis, explicitly ask:
- "To write this feature's spec.md, what specific information from other features' specs do I need?"
- Pay special attention to integration/test/framework features - they almost always have spec dependencies
- Don't assume "needs code = implementation only" - specs contain critical information too

**Impact:**
- Required switching from Mode B (full parallelization) to Mode A (group-based waves)
- Feature 09 handoff package should be generated in Wave 2, not Wave 1
- Time estimate still valid (just different wave structure)

### S2 - Feature Deep Dives

#### Lesson 2: Downstream Features That Wire Into Upstream Outputs Have Spec Dependencies

**Date:** 2026-02-14
**Stage:** S1 Step 5.7.5 (re-discovered during S2.P1 execution)

**What Happened:**
- Features 01-08 were placed in a single S2 group (all considered independent)
- 7 secondary agents launched for Features 02-08 in parallel with Feature 01
- During Feature 01's S2.P1.I2 (checklist resolution), user noticed that Features 02-08 all depend on Feature 01's spec
- All 7 secondary agents had to be paused mid-S2

**The Mistake:**
For Feature 02, agent asked: *"Can I write the spec using Discovery + current code?"* → answered YES.
This was the wrong question.

**The Right Question:**
*"Can I write a COMPLETE spec without Feature 01's spec?"* → NO

Feature 02 specs how CLI args get wired into Settings/internal modules. Feature 01 is actively determining what those Settings/internal module signatures look like. Knowing the arg names from Discovery ≠ knowing the complete integration contract.

**Why This Applies to ALL of Features 02-08:**
All 7 runner features add CLI args and wire them into refactored constructors that Feature 01 defines. Same spec-level dependency pattern for all of them.

**Correct Grouping:**
- Group 1: Feature 01 only (establishes pattern + internal module signatures)
- Group 2: Features 02-08 (need Feature 01's spec to know wiring)
- Group 3: Feature 09 (needs Features 02-08's specs to know what to test)

**Root Cause (same underlying cause as Lesson 1, but more general):**
- Shallow check used: *"Can I identify WHAT to build?"*
- Should use deep check: *"Do I need another feature's spec to describe HOW it integrates?"*

**Key Pattern:**
Any feature that sits downstream in a data/dependency flow AND must interface with an upstream feature's output structure (not just its existence) has a spec-level dependency — especially when the upstream feature is actively defining that output structure in S2.

**Prevention:**
For each feature, explicitly ask:
- "What is the output/interface of the upstream feature?"
- "Does my spec need to describe how I use that interface?"
- "Is that interface fully defined in Discovery, or will it be defined in upstream's S2?"
- If the interface will be defined in upstream's S2 → spec-level dependency exists

**Impact:**
- 7 secondary agents had to be paused mid-S2
- Required restructuring to 3-wave group-based parallelization
- Features 02-08 must wait for Feature 01 S2 complete before starting their own S2

### S3 - Cross-Feature Sanity Check

*To be filled during S3*

### S4 - Epic Testing Strategy

*To be filled during S4*

---

## Implementation Phase Lessons (S5-S8)

*To be filled as features complete*

---

## QC Phase Lessons (S9)

*To be filled during S9*

---

## Epic Cleanup Lessons (S10)

*To be filled during S10*

---

## Guide Improvements Identified

*Document any guide gaps, unclear instructions, or workflow improvements needed*

---

*This file will be continuously updated throughout the epic lifecycle*
