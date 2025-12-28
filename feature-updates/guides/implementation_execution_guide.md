# Implementation Execution Guide

This guide covers executing the TODO file and building the feature. Use this AFTER completing all 24 verification iterations.

**Related Files:**
- `todo_creation_guide.md` - Previous guide (create TODO with 24 iterations)
- `post_implementation_guide.md` - Next guide (QC and validation)
- `protocols/README.md` - Detailed protocol definitions
- `templates.md` - File templates

---

## ⚠️ IMPORTANT: Sub-Feature Workflow

**If your feature uses sub-features:**
- Execute this guide **ONCE PER SUB-FEATURE** (not once for entire feature)
- You should have completed `todo_creation_guide.md` for THIS sub-feature first
- Implement THIS sub-feature completely
- Run tests including integration with previously completed sub-features
- Proceed to `post_implementation_guide.md` for THIS sub-feature
- **Do NOT start next sub-feature** until current one passes all QC rounds

**Integration testing with sub-features:**
- Test THIS sub-feature's functionality
- Test integration with ALL previously completed sub-features
- Verify no regressions in earlier sub-features

**File naming for sub-features:**
- `{feature_name}_sub_feature_{N}_{name}_implementation_checklist.md`
- `{feature_name}_sub_feature_{N}_{name}_code_changes.md`

**If your feature is a single feature (no sub-features):**
- Execute this guide once
- File naming: `{feature_name}_implementation_checklist.md`, `{feature_name}_code_changes.md`

**How to tell which approach:**
- Check for `SUB_FEATURES_README.md` in feature folder
- If exists: Use sub-feature workflow
- If not exists: Use single feature workflow

---

## Quick Start (5 Steps)

1. **Verify prerequisites** - 24 iterations complete, interface verification done
2. **Create implementation checklist** - For continuous spec verification
3. **Execute TODO tasks phase by phase** - With continuous spec consultation
4. **Incremental QA checkpoints** - After each major phase
5. **Update documentation** - code_changes.md and lessons_learned.md throughout

**Result:** Feature implemented correctly, matching specs exactly

**Next Step:** → Proceed to `post_implementation_guide.md` for QC and validation

---

## Implementation Phase Quick Reference Checklist

```
┌─────────────────────────────────────────────────────────────────┐
│  IMPLEMENTATION PHASE CHECKLIST                                 │
│  Track progress through code implementation                     │
└─────────────────────────────────────────────────────────────────┘

□ SETUP
  □ Create implementation checklist from TODO requirements
  □ Open specs.md (keep VISIBLE throughout coding)
  □ Open TODO.md with acceptance criteria
  □ Verify all 24 iterations complete
  □ Verify interface verification complete

□ EXECUTE TODO TASKS PHASE BY PHASE
  □ Phase 1: [Core Implementation]
    □ For each task:
      □ READ requirement in specs.md
      □ VERIFY understanding before coding
      □ CODE implementation with spec references
      □ VERIFY against specs after coding
      □ CHECK OFF in implementation checklist
    □ Run unit tests (100% pass required)
    □ Mini-QC checkpoint passed
    □ Configuration Change Checkpoint (if config.py modified)

  □ Phase 2: [Integration/Next Phase]
    □ Repeat Implementation Loop for each task
    □ Run unit tests (100% pass required)
    □ Mini-QC checkpoint passed

  □ Phase 3+: [Continue for all phases]
    □ Execute all remaining TODO tasks
    □ Continuous spec verification
    □ Tests passing after each phase

□ CONTINUOUS VERIFICATION (Every 5-10 minutes)
  □ "Did I consult specs.md in last 5 minutes?"
  □ "Can I point to exact spec line this code satisfies?"
  □ "Working from documentation, not memory?"
  □ "Checked off requirement in implementation checklist?"

□ DOCUMENTATION (After each change - not batched)
  □ Update code_changes.md incrementally
  □ Update lessons_learned.md when issues found
  □ Commit after each major phase

□ COMPLETION CRITERIA
  □ All TODO tasks marked [x]
  □ All implementation checklist items verified
  □ All acceptance criteria satisfied
  □ All unit tests passing (100% pass rate)
  □ All mini-QC checkpoints passed
  □ code_changes.md complete
  □ lessons_learned.md updated
  □ No deviations from specs without documentation
  □ ⚡ UPDATE README Agent Status: Phase=POST-IMPLEMENTATION, Step=Implementation complete

□ READY FOR POST-IMPLEMENTATION
  □ Proceed to post_implementation_guide.md
```

**⚡ = Status Update Required**: Update README "Agent Status" section for session continuity.

---

## Verify TODO Creation Complete

```
┌─────────────────────────────────────────────────────────────────┐
│  ⚠️  MANDATORY: VERIFY TODO CREATION COMPLETE BEFORE CODING     │
└─────────────────────────────────────────────────────────────────┘
```

**BEFORE starting implementation**, verify TODO creation is 100% complete:

□ File exists: `{feature_name}_todo.md`
□ TODO file shows: "24/24 iterations complete"
□ TODO file shows: "READY TO IMPLEMENT" or similar confirmation
□ Iteration 4a (TODO Specification Audit) shows: "PASSED"
□ Iteration 23a (Pre-Implementation Spec Audit) shows: "ALL 4 PARTS PASSED"
□ Iteration 24 (Implementation Readiness) shows: "PASSED"
□ Interface Verification section shows: "COMPLETE"
□ Integration Matrix is complete (all new methods have callers identified)
□ Algorithm Traceability Matrix is complete
□ No "Alternative:" notes remain unresolved in TODO
□ No "May need to..." notes remain in TODO
□ README.md Agent Status shows: "Ready for Implementation"

**If ANY checkbox is unchecked:**
- ❌ DO NOT start coding
- Return to `todo_creation_guide.md` to complete verification
- Fix the incomplete items
- Re-verify this checklist

**If all checkboxes are checked:**
- ✅ TODO creation is complete
- ✅ Proceed with this guide (Implementation Execution)
- ✅ Start with "Implementation Phase Quick Reference Checklist" above

---

## Prerequisites Checklist

```
┌─────────────────────────────────────────────────────────────────┐
│  ✓ VERIFY BEFORE WRITING ANY CODE                               │
└─────────────────────────────────────────────────────────────────┘
```

Complete this checklist BEFORE starting implementation:

| Check | How to Verify | If Failed |
|-------|---------------|-----------|
| All 24 iterations complete | TODO shows "READY TO IMPLEMENT" | Complete remaining iterations |
| Iteration 23a passed | Pre-Implementation Audit shows all 4 parts passed | Fix audit failures first |
| Iteration 24 passed | Implementation Readiness checklist complete | Complete readiness checklist |
| Interface verification done | All external dependencies verified against source | Complete interface verification |
| No "Alternative:" notes | Search TODO for unresolved alternatives | Resolve alternatives with user |
| No "May need to..." notes | Search TODO for uncertainty markers | Resolve uncertainties |
| Unit tests pass | `python tests/run_all_tests.py` exits 0 | Fix failing tests |

**Why this matters:** Starting implementation without complete verification leads to rework.

---

## README Agent Status Requirements (Session Continuity)

```
┌─────────────────────────────────────────────────────────────────┐
│  CRITICAL: README.md Agent Status MUST be updated frequently    │
└─────────────────────────────────────────────────────────────────┘
```

**Why critical during implementation:** Implementation can span hours or days across multiple sessions. README Agent Status ensures any agent can pick up exactly where you left off.

### When to Update

**MANDATORY update points:**
- After completing each major phase (Phase 1, 2, 3, etc.)
- After each mini-QC checkpoint
- After committing code
- Before ending session (if work in progress)
- When blocked on an issue

### Template for Implementation Phase

```markdown
## Agent Status

**Last Updated:** {YYYY-MM-DD HH:MM}
**Current Phase:** DEVELOPMENT - Implementation
**Current Step:** Phase X - {Component name}
**Progress:** X/Y TODO tasks complete
**Next Action:** {Specific next task from TODO}
**Blockers:** {Issues or "None"}
**Notes:**
- Phase X: {Status}
- Mini-QC checkpoints: X/Y passed
- Tests: {pass/fail status}
- Last commit: {commit hash or "none yet"}
```

### Good Example

```markdown
## Agent Status

**Last Updated:** 2025-12-24 15:45
**Current Phase:** DEVELOPMENT - Implementation
**Current Step:** Phase 2 - Integration Layer
**Progress:** 12/35 TODO tasks complete
**Next Action:** Implement wire_manager_to_runner() method (Task 2.3 in TODO)
**Blockers:** None
**Notes:**
- Phase 1: Core classes complete, tests passing
- Phase 2: In progress (5/12 tasks done)
- Mini-QC checkpoints: 1/3 passed
- Tests: 100% pass rate (2,296/2,296)
- Last commit: abc123f "Phase 1 complete: core classes"
- Continuous spec verification: Active (last checked 15:40)
```

**Red Flags:** No specific task listed, no test status, no commit tracking

---

## CRITICAL RULES - READ BEFORE CODING

```
┌─────────────────────────────────────────────────────────────────┐
│  RULES FOR IMPLEMENTATION (Quick Reference)                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Keep specs.md VISIBLE at all times during coding            │
│  2. Verify EACH requirement BEFORE implementing                 │
│  3. Verify EACH requirement AFTER implementing                  │
│  4. Run tests after EVERY phase (100% pass required)            │
│  5. Update code_changes.md AFTER each change (not batched)      │
│  6. Mini-QC checkpoints after each major component              │
│  7. Never code from memory - always consult specs               │
│  8. Check off implementation checklist items as you go          │
│  9. Document deviations immediately in lessons_learned.md       │
│                                                                 │
│  COMMON MISTAKES TO AVOID:                                      │
│  ✗ "I remember what the spec said" → Consult specs now          │
│  ✗ "Tests pass so it's right" → Verify against specs            │
│  ✗ "I'll verify during QC" → Verify NOW during implementation   │
│  ✗ "Quick change, skip mini-QC" → Run mini-QC always            │
│  ✗ "Working from TODO alone" → TODO + specs.md together         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Critical Warning: Implementation Without Verification

```
┌─────────────────────────────────────────────────────────────────┐
│  ⚠️  CRITICAL: CONTINUOUS SPEC VERIFICATION IS MANDATORY        │
│                                                                 │
│  Historical Evidence: Feature implemented without continuous    │
│  verification resulted in:                                      │
│  - 40% QC failure rate (8 critical issues)                      │
│  - Wrong JSON structure (didn't match specs)                    │
│  - Missing 3 required fields                                    │
│  - Wrong stat mappings for all positions                        │
│  - 2+ hours of rework required                                  │
│                                                                 │
│  ALL issues were preventable by consulting specs during         │
│  implementation.                                                │
│                                                                 │
│  Implementation is NOT "just write code until it works"         │
│  Implementation IS "write code that matches specs exactly"      │
└─────────────────────────────────────────────────────────────────┘
```

---

## Common Shortcuts to Avoid (With Consequences)

```
┌─────────────────────────────────────────────────────────────────┐
│  ⚠️  SHORTCUT DETECTION - IF YOU'RE THINKING THIS, STOP        │
└─────────────────────────────────────────────────────────────────┘
```

These are real shortcuts agents have taken during implementation. Each leads to failures:

### Shortcut #1: "I Remember What the Spec Says"

❌ **Thought**: "I read the spec during verification, I remember it"

✅ **Reality**: Memory degrades within minutes. You'll implement based on wrong recall.

**Consequence**: Code doesn't match specs, QC Round 1 fails

**If you think this**: STOP. Open specs.md right now and keep it visible.

---

### Shortcut #2: "Tests Pass = Feature Works"

❌ **Thought**: "All tests pass, so my implementation is correct"

✅ **Reality**: Tests verify logic, not spec compliance. Can pass with wrong behavior.

**Consequence**: Feature works but does wrong thing, fails spec verification

**If you think this**: STOP. Verify against specs.md, not just test results.

---

### Shortcut #3: "I'll Verify During QC"

❌ **Thought**: "I'll check if this matches specs during post-implementation QC"

✅ **Reality**: QC is for minor issues, not fundamental spec compliance

**Consequence**: QC Round 1 fails catastrophically (≥3 critical issues)

**If you think this**: STOP. Verify NOW during implementation, not later.

---

### Shortcut #4: "This is a Quick Change - Skip Mini-QC"

❌ **Thought**: "This phase is small, I don't need mini-QC checkpoint"

✅ **Reality**: Small changes hide integration bugs. Skip = ship broken code.

**Consequence**: Integration failures discovered only during smoke testing

**If you think this**: STOP. Run mini-QC checkpoint for EVERY phase.

---

### Shortcut #5: "I Can Work from TODO Alone"

❌ **Thought**: "TODO has all the details, I don't need to consult specs"

✅ **Reality**: TODO is implementation plan, specs are requirements. Both needed.

**Consequence**: Implement plan correctly but miss spec nuances

**If you think this**: STOP. Use TODO + specs.md together always.

---

### Shortcut #6: "I'll Batch-Update Documentation Later"

❌ **Thought**: "I'll update code_changes.md after I finish all coding"

✅ **Reality**: Batch updates forget details, become inaccurate

**Consequence**: Cannot reconstruct what changed or why during QC

**If you think this**: STOP. Update code_changes.md AFTER EACH change.

---

### Shortcut #7: "I Know This Class Interface"

❌ **Thought**: "I've used this class before, I know its methods"

✅ **Reality**: Interfaces evolve. Your memory is outdated.

**Consequence**: Runtime errors from non-existent methods or wrong signatures

**If you think this**: STOP. Read the actual class definition right now.

---

### Shortcut #8: "This Deviation Doesn't Matter"

❌ **Thought**: "Specs say X, but Y is better. I'll just implement Y."

✅ **Reality**: Specs exist for a reason. Undocumented deviations = spec violations.

**Consequence**: QC rejects feature, must revert to spec

**If you think this**: STOP. Either follow specs OR document deviation + get approval.

---

### Shortcut #9: "I'll Skip Checking Off the Checklist"

❌ **Thought**: "I know I implemented everything, don't need checklist tracking"

✅ **Reality**: Memory is unreliable. Unchecked items = possibly not implemented.

**Consequence**: Miss requirements, incomplete implementation

**If you think this**: STOP. Check off implementation checklist as you code.

---

### Shortcut #10: "Specs Visible = Spec Consultation"

❌ **Thought**: "I have specs.md open, that's continuous verification"

✅ **Reality**: Open ≠ consulting. Must actively read before AND after each item.

**Consequence**: Specs are decorative wallpaper, not guidance

**If you think this**: STOP. Actively READ specs before implementing each requirement.

---

**REMEMBER**: Implementation shortcuts feel fast. They cost 2-10x time in rework.

---

## Before You Write ANY Code

### Setup Checklist

**Create your implementation environment:**

- [ ] Open specs.md in your editor (KEEP IT VISIBLE throughout implementation)
- [ ] Open TODO.md with traceability matrix (reference continuously)
- [ ] Create implementation checklist from TODO requirements
- [ ] Commit to checking off EACH requirement as implemented

**Implementation Environment:**
- Primary monitor: Code editor
- Secondary reference: specs.md (always visible)
- Third reference: TODO.md with acceptance criteria

---

### Create Implementation Checklist

Create this file: `{feature_name}_implementation_checklist.md`

```markdown
# Implementation Checklist

**Instructions**: Check off EACH requirement as you implement it. Do NOT batch-check.

## From Traceability Matrix:

- [ ] REQ-001: [Description from specs.md lines X-Y]
      Implemented in: [file:line]
      Verified: [date/time]

- [ ] REQ-002: [Description from specs.md lines X-Y]
      Implemented in: [file:line]
      Verified: [date/time]

...

## Verification Log:

| Requirement | Spec Location | Implementation | Verified? | Matches Spec? | Notes |
|-------------|---------------|----------------|-----------|---------------|-------|
| REQ-001 | specs.md:45-50 | file.py:120-135 | ✅ | ✅ | Exact match |
| REQ-002 | specs.md:52-58 | file.py:140-160 | ✅ | ✅ | Exact match |
| REQ-003 | specs.md:60-65 | file.py:165-180 | ✅ | ⚠️ | Minor deviation: [explain] |
```

**Why this matters:** This checklist forces you to verify each requirement against specs as you implement.

---

## The Implementation Loop (For EACH Requirement)

```
┌─────────────────────────────────────────────────────────────────┐
│  STOP. READ. VERIFY. CODE. VERIFY AGAIN.                        │
└─────────────────────────────────────────────────────────────────┘
```

For EACH requirement you implement, follow this process:

### 1. READ the Requirement

- Locate exact section and line numbers in specs.md
- Read requirement word-for-word
- Understand expected output/behavior

### 2. VERIFY BEFORE Coding

Ask yourself:
- [ ] Can I describe the expected output?
- [ ] Do I know what structure/fields are required?
- [ ] Do I know what "correct" looks like?
- [ ] Do I have an example from specs?

**If NO to any question → Re-read specs before coding**

### 3. CODE the Implementation

- Reference spec line numbers in comments
- Use exact field names from specs
- Follow exact structure from specs
- Use exact mappings from specs

Example:
```python
def build_player_json(self, player):
    """
    Build JSON structure for player.

    Spec: specs.md lines 44-56 (Common Player Fields)
    """
    return {
        # Required fields from specs.md:44-56
        "id": player.id,
        "name": player.name,
        "team": player.team,
        # ... all 11 required fields
    }
```

### 4. VERIFY AFTER Coding

Ask yourself:
- [ ] Structure matches spec example?
- [ ] All required fields present?
- [ ] Field types correct?
- [ ] Arrays correct length?
- [ ] Mappings match spec table?

**If NO to any question → Fix before proceeding**

### 5. CHECK OFF Requirement

Mark requirement complete in implementation checklist:
- Document: "Implemented [requirement] per specs.md lines X-Y"

---

## Self-Audit Questions (Answer Frequently)

Ask yourself these questions FREQUENTLY (every 5-10 minutes):

- [ ] "Did I consult specs.md in the last 5 minutes?" (YES required)
- [ ] "Can I point to the exact spec line this code satisfies?" (Must be specific)
- [ ] "If I showed user ONLY this code and the spec, would they match?" (YES required)
- [ ] "Am I working from memory or documentation?" (Documentation required)
- [ ] "Have I checked off this requirement in my implementation checklist?" (YES required)

**If you answer NO to any question → STOP and consult specs before proceeding.**

---

## Red Flags (STOP if any are true)

- ⛔ "I don't remember what the spec said, but I think it's..."
- ⛔ "The spec is probably similar to..."
- ⛔ "I'm sure this is what they want..."
- ⛔ "I'll verify against specs later during QC..."
- ⛔ "The tests pass, so it must be right..."
- ⛔ "I've been coding for 15 minutes without reading specs"

**If you catch yourself thinking any of these → IMMEDIATELY consult specs.**

---

## Mini-QC Checkpoints (MANDATORY)

QA must happen THROUGHOUT development, not just at the end.

**After completing each major component (10-15% of implementation):**

1. **STOP implementation**
2. **Review that component against specs:**
   - Read spec section for this component
   - Compare your code to spec requirements
   - Verify all acceptance criteria satisfied
3. **Document any deviations:**
   - Why did you deviate?
   - Is deviation acceptable?
   - Get user approval if significant
4. **DO NOT PROCEED** to next component until current component verified against specs

**Mini-QC Frequency:**
- After Phase 1 complete
- After Phase 2 complete
- After Phase 3 complete
- etc.

**Mini-QC Checklist:**
- [ ] Read spec section for this phase
- [ ] All requirements from specs implemented?
- [ ] All TODO acceptance criteria satisfied?
- [ ] Any deviations documented and justified?
- [ ] Tests passing for this phase?

**Mini-QC Failure Protocol:**

```
╔═════════════════════════════════════════════════════════════════╗
║  🛑 🛑 🛑 MINI-QC CHECKPOINT FAILED - STOP HERE 🛑 🛑 🛑        ║
╠═════════════════════════════════════════════════════════════════╣
║                                                                 ║
║  A mini-QC checkpoint failure means your code does NOT match   ║
║  the specs. Do NOT proceed to the next phase.                  ║
║                                                                 ║
║  VERIFICATION QUESTIONS (All must be YES):                      ║
║  □ Have I identified the exact mismatch with specs?            ║
║  □ Do I understand WHY the mismatch occurred?                  ║
║  □ Have I fixed the code to match specs?                       ║
║  □ Have I re-verified against specs after the fix?             ║
║  □ Have I documented the issue in lessons_learned.md?          ║
║                                                                 ║
║  CONSEQUENCES OF PROCEEDING WITHOUT FIXING:                    ║
║  ❌ Future code will build on broken foundation                ║
║  ❌ Issues compound and become harder to fix                   ║
║  ❌ Post-implementation QC will fail catastrophically          ║
║  ❌ You'll need to redo multiple phases, not just one          ║
║                                                                 ║
║  MANDATORY ACTIONS:                                            ║
║  1. Fix the issue immediately (consult specs)                  ║
║  2. Re-run all unit tests                                      ║
║  3. Re-run mini-QC checkpoint                                  ║
║  4. Document in lessons_learned.md                             ║
║  5. Only proceed when checkpoint shows PASSED                  ║
║                                                                 ║
╚═════════════════════════════════════════════════════════════════╝
```

**Why this matters:** QA at the end can only verify that bugs still exist. QA during development catches bugs when they're introduced.

---

```
╔═════════════════════════════════════════════════════════════════╗
║  ⏸️  PERIODIC SELF-AUDIT: Run Every 30-60 Minutes              ║
╠═════════════════════════════════════════════════════════════════╣
║                                                                 ║
║  Set a timer. Every 30-60 minutes, PAUSE and audit yourself:   ║
║                                                                 ║
║  Spec Consultation Check:                                      ║
║  □ When was the last time I opened specs.md? (Should be <5min) ║
║  □ Can I point to the exact spec line for my current code?     ║
║  □ Am I implementing from specs or from memory?                ║
║  □ Have I consulted specs BEFORE writing this component?       ║
║  □ Will I consult specs AFTER finishing this component?        ║
║                                                                 ║
║  Implementation Checklist Check:                               ║
║  □ Have I been checking off items as I implement them?         ║
║  □ Or am I implementing without tracking completion?           ║
║  □ Can I name the last 3 requirements I implemented?           ║
║                                                                 ║
║  Documentation Check:                                          ║
║  □ Have I updated code_changes.md in last 30 minutes?          ║
║  □ Or am I batching documentation for "later"?                 ║
║  □ Can I describe what I changed in this period?               ║
║                                                                 ║
║  Testing Check:                                                ║
║  □ When was the last time I ran tests? (Should be <15min)      ║
║  □ Do all tests still pass?                                    ║
║  □ Have I written tests for new code?                          ║
║                                                                 ║
║  Process Adherence Check:                                      ║
║  □ Am I following the Implementation Loop for each task?       ║
║  □ Or am I just "writing code"?                                ║
║  □ Have I run mini-QC after each major component?              ║
║  □ Am I working from TODO + specs, or just TODO?               ║
║                                                                 ║
║  Red Flags (If YES to any, STOP and correct immediately):      ║
║  □ Haven't opened specs.md in >10 minutes                      ║
║  □ Can't point to spec line for current code                   ║
║  □ Haven't run tests in >15 minutes                            ║
║  □ Haven't updated documentation in >30 minutes                ║
║  □ Implementing from memory instead of specs                   ║
║  □ Skipping mini-QC checkpoints                                ║
║  □ Not checking off implementation checklist                   ║
║                                                                 ║
║  SELF-CORRECTION:                                              ║
║  If ANY red flag is present:                                   ║
║  1. STOP coding immediately                                    ║
║  2. Open specs.md and verify current work matches              ║
║  3. Run tests: python tests/run_all_tests.py                   ║
║  4. Update code_changes.md with recent changes                 ║
║  5. Check off completed items in implementation checklist      ║
║  6. Only resume coding after all red flags cleared             ║
║                                                                 ║
║  REMEMBER: Catching drift early (every 30-60 min) prevents     ║
║  major rework later. This 2-minute pause saves hours of work.  ║
║                                                                 ║
╚═════════════════════════════════════════════════════════════════╝
```

---

## Example: Right vs Wrong Implementation

### WRONG (What typically happens):
```
Agent: "I need to create export_json_player_data method"
Agent: *writes method from memory/assumptions*
Agent: "Method complete, tests pass, moving on"
```

**Result:** Wrong structure, missing fields, incorrect mappings discovered during QC

### RIGHT (What MUST happen):
```
Agent: "I need to create export_json_player_data method"
Agent: *Opens specs.md, reads Section 1 (File Structure)*
Agent: "Spec says root structure is {qb_data: [...]}, let me verify my code does this"
Agent: *Writes _build_position_json() method*
Agent: *Checks output structure against spec*
Agent: "Output is {qb_data: [player1, player2]}, matches spec lines 24-33 ✓"
Agent: *Checks off REQ-001 in implementation checklist*
Agent: *Moves to Section 2 (Common Fields)*
Agent: "Spec requires: id, name, team, position, injury_status, drafted_by, locked, average_draft_position, player_rating, projected_points, actual_points"
Agent: "Let me verify each field is in my JSON output..."
Agent: *Verifies all 11 fields present with correct types*
Agent: "All fields present, matches specs.md lines 44-56 ✓"
Agent: *Checks off REQ-002 in implementation checklist*
Agent: *Continues this pattern for every requirement...*
```

**Result:** Code matches specs exactly, zero issues found during QC

---

## Rollback Point Planning (Before Implementation Begins)

Before starting implementation, identify natural rollback points. This makes it safer to advance because you know how to retreat.

### Step 1: Identify Reversible Checkpoints

List the natural stopping points where you can safely roll back:
```
| Checkpoint | Description | Rollback Command |
|------------|-------------|------------------|
| Clean state | Before any changes | git checkout -- . |
| Phase 1 complete | Core classes created | git checkout {phase1_commit} |
| Phase 2 complete | Integration wired up | git checkout {phase2_commit} |
```

### Step 2: Identify "Point of No Return" Changes

Some changes are harder to reverse. Identify these early:
- Database schema changes
- API contract changes (if external consumers exist)
- Config file format changes that affect other tools
- File/folder structure changes that affect other scripts

### Step 3: Plan Commit Strategy

- Commit after each phase completes successfully
- Use descriptive commit messages that explain the checkpoint
- Consider WIP commits for long phases: "WIP: Phase 2 - integration partial"

**Rollback Commands Reference:**
```bash
# Revert all uncommitted changes
git checkout -- .

# Revert to specific commit (keeps history)
git revert HEAD

# View recent commits for rollback targets
git log --oneline -10
```

**Why this matters:** Knowing how to retreat makes it safer to advance. If implementation fails, you can quickly return to a known-good state.

---

## Interface and Data Model Verification (Pre-Implementation)

Before writing any implementation code, complete these verification steps:

### Step 1: List All External Dependencies

For each class the new code will use, document:
- Class name
- Methods to be called
- Expected parameters (including types)
- Return values

### Step 2: Verify Interfaces Against Source

For each dependency:
1. Read the actual class definition (not just mocks or docstrings)
2. Verify method signatures match your expectations
3. Check required vs optional parameters
4. Look for existing usage patterns: `grep -r "ClassName(" .`

### Step 3: Verify Data Model Attributes

For each data model (dataclass, domain object) you'll access:
1. Read the actual class definition
2. List all attributes you plan to use
3. Verify each attribute exists in the definition
4. Check attribute semantics (e.g., does `fantasy_points` mean projected or actual?)

**Why this matters:** Interface mismatches cause bugs during implementation. Catch them beforehand.

**Interface Verification Checklist:**
```
□ All external dependencies listed
□ Each dependency's methods verified against source code
□ Parameter names and types confirmed
□ Return values documented
□ Data model attributes verified to exist
□ Attribute semantics understood (not assumed)
```

---

## Reference Existing Usage (MANDATORY)

Before implementing code that uses existing modules:

1. **Find existing usage examples**: `grep -r "module_name\." .`
2. **Read actual method signatures**: Check the real `def` lines, not just docstrings
3. **Verify against existing tests**: See how the class is used in its own unit tests
4. **Copy the pattern**: Don't invent new method names that might not exist

**Example:**
```bash
# Before using ConfigGenerator in new code:
grep -r "config_generator\." simulation/
# Find: SimulationManager.py shows correct usage pattern
# Use that pattern, don't assume different methods exist
```

---

## Bridge Adapter Pattern Best Practices

```
┌─────────────────────────────────────────────────────────────────┐
│  ⚠️  CRITICAL: VERIFY RETURN FORMATS WHEN WRAPPING METHODS      │
│                                                                 │
│  Real bug example: Bridge adapter wrapped stat extraction      │
│  methods but assumed wrong return format:                      │
│  - Assumed: {'passing': {'completions': [...]}}  (nested)     │
│  - Reality: {'completions': [...], 'attempts': [...]} (flat)  │
│  - Result: 100% test pass rate but missing all stats in prod  │
│                                                                 │
│  Root cause: Mocks returned expected format, not actual format │
│  Prevention: Verify return format from source before wrapping  │
└─────────────────────────────────────────────────────────────────┘
```

When creating bridge adapters, facades, or wrappers around external methods:

### 1. ALWAYS Verify Return Format From Source

Don't assume or remember - verify the actual return format:

```python
# ❌ WRONG: Assume format based on intuition
def get_player_stats(self, player):
    """Extract player stats"""
    stats = self.exporter.extract_stats(player)
    return stats  # What format does this return? Unknown!

# ✅ RIGHT: Verify format and document explicitly
def get_player_stats(self, player):
    """
    Extract player stats via bridge to DataExporter.

    VERIFIED RETURN FORMAT (from DataExporter source):
    - extract_passing_stats(): Dict[str, List[float]]
      Returns FLAT dict: {'completions': [30.0, ...], 'attempts': [45.0, ...]}
      NOT nested dict: {'passing': {...}}

    Source: player_data_exporter.py:245-280 (verified 2025-12-26)
    """
    stats = self.exporter.extract_passing_stats(player)
    # Returns flat dict, need to wrap in 'passing' key
    return {'passing': stats}
```

**How to verify:**
1. Read the actual source code of the method you're wrapping
2. Look at what it actually `return`s (not what you think it returns)
3. Check for existing usage: `grep -r "method_name(" .`
4. Document the VERIFIED format with source location and date

### 2. Add Explicit Tests With REAL Objects (Not Just Mocks)

Mock-only tests can pass while real integration fails. Always include at least one test with real objects:

```python
# ❌ INSUFFICIENT: Mock-only test
def test_bridge_adapter_with_mock(self):
    """Test adapter with mocked exporter"""
    mock_exporter = Mock()
    # Mock returns what I EXPECT (may be wrong!)
    mock_exporter.extract_stats.return_value = {'passing': {...}}

    adapter = PlayerDataAdapter(player)
    result = adapter.get_stats(mock_exporter)

    # Passes even if real exporter returns different format
    assert 'passing' in result

# ✅ REQUIRED: At least one real-object test
def test_bridge_adapter_with_real_exporter(self):
    """Test adapter with ACTUAL exporter instance (no mocks)"""
    # Use real class, not mock
    real_exporter = DataExporter(data_folder=self.test_data)
    test_player = PlayerData(id="1001", name="Test QB", position="QB", ...)

    adapter = PlayerDataAdapter(test_player)

    # Call real method (will fail if format assumption is wrong)
    result = real_exporter.extract_passing_stats(adapter)

    # Verify ACTUAL return format (not assumed format)
    assert isinstance(result, dict)
    assert 'completions' in result  # Flat dict, NOT nested 'passing' key!
    assert isinstance(result['completions'], list)
```

**Why this matters:**
- Mocks test your expectations
- Real objects test reality
- Expectations ≠ Reality leads to prod bugs

### 3. Document Expected Formats In Adapter Class Docstring

Make return format assumptions explicit for future maintainers:

```python
class PlayerDataAdapter:
    """
    Adapts PlayerData objects for use with DataExporter.

    This adapter implements the interface expected by DataExporter methods.

    VERIFIED RETURN FORMATS (from DataExporter source):

    DataExporter._extract_passing_stats(adapter) returns:
        Dict[str, List[float]] - FLAT dict structure
        {
            'completions': [30.0, 25.0, ...],  # 17 weeks
            'attempts': [45.0, 38.0, ...],     # 17 weeks
            'pass_yds': [320.0, 285.0, ...],   # 17 weeks
            'pass_tds': [2.0, 1.0, ...]        # 17 weeks
        }
        NOTE: Returns FLAT dict (stat_name -> array)
        NOT nested dict ({'passing': {...}})

    DataExporter._extract_rushing_stats(adapter) returns:
        Dict[str, List[float]] - FLAT dict structure
        {
            'rush_att': [5.0, 3.0, ...],
            'rush_yds': [25.0, 18.0, ...],
            'rush_tds': [0.0, 1.0, ...]
        }

    Source Verification:
    - File: player_data_exporter.py
    - Methods: _extract_passing_stats (lines 245-280)
    - Verified: 2025-12-26
    - Existing usage: historical_data_compiler/csv_exporter.py:156

    Common Mistake:
        Assuming methods return nested {'passing': {...}} because that's
        what makes logical sense. Always verify actual return format.
    """

    def __init__(self, player_data: PlayerData):
        self.player_data = player_data
```

**Why this matters:**
- Documents assumptions for code reviews
- Prevents future developers from making same wrong assumption
- Provides verification trail (source location, date)

### 4. Verification Checklist For Bridge Adapters

Before implementing any bridge adapter or wrapper:

```
□ Read source code of ALL methods being wrapped
□ Document actual return format (not assumed format)
□ Include source file and line numbers
□ Write at least ONE test with real objects (not mocks)
□ Document return format in adapter class docstring
□ Verify existing usage matches your understanding
□ Test integration with real method calls before production
```

**Red Flags (Stop and verify):**
- "I remember this method returns..."
- "It should logically return..."
- "The mock returns X, so the real method must too"
- "I'll verify the format during QC"
- All tests use mocks, none use real objects

**Key Principle: Don't assume - verify and document.**

---

## Standard Implementation Steps

### 1. Create Code Changes File

Create `{feature_name}_code_changes.md` using template from `templates.md`

### 2. Verify Dependency Ordering

Before implementing, ensure TODO tasks are correctly ordered:

**Dependency Ordering Checklist:**
```
□ Data models/classes created before code that uses them
□ Utility functions created before callers
□ Tests created after implementations they test
□ Configuration changes before code that reads config
□ No circular dependencies between tasks
```

**How to verify:**
- For each TODO task, ask: "What must exist before I can implement this?"
- If dependency exists as a later task, reorder
- If dependency doesn't exist in TODO, add it

### 3. Execute TODO Tasks Phase by Phase

**For each TODO task:**

1. **Read the task** including all acceptance criteria
2. **Read corresponding spec section** to refresh understanding
3. **Implement the task** following the Implementation Loop (above)
4. **Verify against specs** using acceptance criteria
5. **Update code_changes.md** IMMEDIATELY (don't batch)
6. **Run unit tests** for affected modules
7. **Check off task** in TODO when verified

**After each phase:**
- Run all unit tests: `python tests/run_all_tests.py`
- 100% pass rate required at all times
- Execute Mini-QC Checkpoint (see above)
- **Execute Configuration Change Checkpoint (if config files modified)**

---

## 🚦 Configuration Change Checkpoint

**When to Use:** After modifying any configuration file (config.py, settings files, etc.) during Phase 1 or any phase.

**Purpose:** Prevent configuration-related bugs by reviewing ALL related settings, not just the ones you added.

### Mandatory Review Process

**Step 1: List Related Settings**
- What other config settings relate to this feature?
- Group by category: paths, caps, toggles, limits, defaults

**Step 2: Review Each Related Setting**
Ask for EACH setting:
- "Does this setting need adjustment for my feature?"
- "Will my feature conflict with this setting?"
- "Is the current value appropriate for my feature's scale?"

**Step 3: Common Configuration Pitfalls**

**File Caps:**
- Feature creates N files → caps must be ≥ N
- Consider multiple runs: cap should be multiple of N
- Example: 6 position files → cap should be 12, 18, 24, etc.

**Output Paths:**
- Do new paths conflict with existing paths?
- Are paths relative or absolute?
- Do paths exist or need creation?

**Default Values:**
- Is default TRUE or FALSE appropriate for production?
- Should feature be opt-in or opt-out?
- Does default match user's needs?

**Limits and Thresholds:**
- Does feature scale exceed existing limits?
- Do timeouts accommodate feature's operations?
- Do buffer sizes handle feature's data volume?

### Example Configuration Review

```python
# FEATURE: Add position JSON export (creates 6 files)

# NEW SETTINGS ADDED:
CREATE_POSITION_JSON = True  ← Added
POSITION_JSON_OUTPUT = "../data/player_data"  ← Added

# RELATED SETTINGS TO REVIEW:
DEFAULT_FILE_CAPS = {'json': 5, ...}  ← PROBLEM! Creates 6, cap is 5
OUTPUT_DIRECTORY = "./data"  ← Different path, OK
CREATE_JSON = False  ← Different feature, OK

# ACTION REQUIRED:
DEFAULT_FILE_CAPS = {'json': 18, ...}  ← Fixed (6 files × 3 runs)
```

### Checkpoint Completion Criteria

- [ ] All related config settings identified
- [ ] Each setting reviewed for compatibility
- [ ] Any conflicts resolved
- [ ] Configuration changes documented in code_changes.md
- [ ] Related settings updated as needed

**Why This Matters:**
Real bug example: Feature created 6 position JSON files, but file cap was set to 5. The 6th file (QB) was created then immediately auto-deleted by the file manager. Feature appeared to work (exit code 0) but was missing critical output. This happened because only NEW config settings were added without reviewing RELATED existing settings.

**If checkpoint fails:** Fix configuration issues before proceeding to next phase.

---

### 4. Consider Test-First for Algorithms

For calculation/algorithm tasks, consider Test-First Implementation:

**When to use Test-First:**
- Implementing scoring algorithms
- Implementing data transformations
- Implementing statistical calculations
- Any logic with clear inputs/outputs

**Test-First Process:**
1. Write failing test with expected output
2. Implement minimal code to pass test
3. Verify against spec acceptance criteria
4. Refactor if needed (tests still pass)

See `protocols/README.md` → Test-First Implementation Principle for details.

### 5. Update Lessons Learned When Issues Found

When you encounter ANY issue during implementation:
- Edge case missed during planning
- Verification failure
- Interface mismatch
- Assumption that was wrong

**IMMEDIATELY document in `{feature_name}_lessons_learned.md`:**
```markdown
## Issue: [Brief description]

**When:** [Phase/task when discovered]
**What happened:** [Detailed description]
**Root cause:** [5-whys analysis]
**Prevention:** [How to prevent in future]
**Guide update needed:** [Yes/No - which guide, what change]
```

---

## Incremental QA Checkpoints (MANDATORY Throughout)

QA must happen CONTINUOUSLY, not just at the end.

**Checkpoint Structure in TODO:**
```
Phase 1: Core Implementation
- [ ] 1.1 Implement AccuracyCalculator
- [ ] 1.2 Implement AccuracyResultsManager
- [ ] 1.3 QA CHECKPOINT: Test calculators with real player data
      Expected: MAE > 0, player_count > 0 for test data

Phase 2: Integration
- [ ] 2.1 Implement AccuracySimulationManager
- [ ] 2.2 Wire up to runner script
- [ ] 2.3 QA CHECKPOINT: Run script end-to-end
      Expected: Script completes, outputs written to disk
```

**QA Checkpoint Requirements:**
1. Run all existing unit tests
2. Run E2E test with real data (whatever is testable so far)
3. Verify output is meaningful (non-zero values, expected format)
4. Document any issues found before proceeding

**QA Checkpoint Failure Protocol:**
1. **STOP development**
2. **Fix the issue** before proceeding
3. **Re-run checkpoint** to verify fix
4. **Document** what went wrong in lessons learned
5. **Only proceed** after checkpoint passes

---

## Testing Guidelines

### Test Naming Conventions

Use descriptive test names that explain what is being tested:

```python
# GOOD
def test_scoring_with_normal_stats(self):
    """Test scoring calculation with typical player stats"""

# BAD
def test_1(self):
    """Test player scoring"""
```

### Avoiding Testing Anti-Patterns

See `todo_creation_guide.md` → Critical Warning: Testing Anti-Patterns for complete list.

**Key reminders during implementation:**
- Write at least ONE integration test with real objects
- Validate output CONTENT, not just file existence
- Test private methods with branching logic through their callers
- Document parameter dependencies and test them
- Use `spec=RealClass` when mocking to catch interface mismatches

---

## Session Handoff (If Context Running Low)

When context is running low or session is ending, complete this checklist:

```
┌─────────────────────────────────────────────────────────────────┐
│  SESSION HANDOFF CHECKLIST                                       │
│  Complete ALL items before session ends                          │
└─────────────────────────────────────────────────────────────────┘

□ Commit any working code (even partial) with message: "WIP: {task} - session handoff"
□ Update TODO to mark current task status:
  - [x] Complete tasks
  - [ ] Pending tasks
  - [~] IN PROGRESS - partial completion (document what's done)
□ Update implementation checklist with verification status
□ Update code_changes.md with latest changes
□ Update README Agent Status section with:
  - Current Phase: IMPLEMENTATION
  - Current Step: Phase X, Task Y
  - Next Action: Continue with Task Z
□ Update Progress Notes in TODO:
  - Current status (what's done)
  - Next steps (what remains)
  - Any blockers or issues
□ Summary message sent to user:
  "Session ending. State preserved:
   - Current: Phase X, Task Y ({description})
   - Progress: {X}% complete
   - Next: {what to do next}
   - All state documented in README Agent Status."
```

**Context Window Emergency Protocol:**

If context runs out DURING implementation (mid-task):

1. **STOP** the current task immediately
2. **Commit** any working code (even partial) with message: "WIP: {task description} - session handoff"
3. **Update TODO** to mark task as "IN PROGRESS - partial completion"
4. **Document** in Progress Notes exactly where you stopped:
   ```
   EMERGENCY HANDOFF:
   - Task: 2.3 - Implement AccuracyCalculator
   - Progress: Method signatures done, MAE calculation partial
   - Next: Complete _calculate_error() method starting line 145
   - File state: Compiles but tests will fail until complete
   ```
5. **Inform user** of the partial state

---

## Communication Guidelines

How often to update the user during implementation:

| Phase | Communication Level | What to Report |
|-------|---------------------|----------------|
| **Implementation Phases** | Per phase | "Completed phase 2. Tests passing. Moving to phase 3." |
| **Mini-QC Checkpoints** | When complete | "Mini-QC for phase 2 passed. Output validated." |
| **Test Failures** | Immediately | "Tests failing in module X. Investigating..." |
| **Blockers** | Immediately | Any issue that prevents progress |
| **Deviations from Spec** | Immediately | "Found issue in spec section X. Need clarification..." |

**Do NOT:**
- Stay silent for entire phases
- Wait until end to reveal problems
- Implement without communicating blockers

**DO:**
- Summarize at natural checkpoints (end of phases)
- Report blockers immediately
- Ask for clarification when specs are unclear

---

## Resuming Work Mid-Implementation

If you're picking up implementation work started by a previous agent:

1. **Read the TODO file**: Check which tasks are `[x]` vs `[ ]` vs `[~]`
2. **Read code_changes.md**: See what was already implemented
3. **Read implementation checklist**: See which requirements were verified
4. **Run all unit tests**: `python tests/run_all_tests.py`
5. **Check for WIP commits**: `git log --oneline -5` (look for "WIP:" messages)
6. **Read lessons_learned.md**: Note any issues encountered so far
7. **Continue from current task**: Pick up exactly where left off

**Determine current state:**
| TODO State | Current Status | Next Action |
|------------|---------------|-------------|
| Task marked `[~]` | Partially complete | Read Progress Notes, complete the task |
| Task marked `[ ]` | Not started | Implement following the Implementation Loop |
| Last task marked `[x]` | Previous task complete | Continue with next `[ ]` task |
| All tasks marked `[x]` | Implementation complete | Proceed to post_implementation_guide.md |

---

## Completion Criteria

Implementation is complete when:

- [ ] All TODO tasks marked `[x]`
- [ ] All implementation checklist items verified
- [ ] All acceptance criteria satisfied
- [ ] All unit tests passing (100% pass rate)
- [ ] All mini-QC checkpoints passed
- [ ] code_changes.md updated with all changes
- [ ] lessons_learned.md updated with all issues
- [ ] No deviations from specs without documentation

**Next Step:** → Proceed to `post_implementation_guide.md` for QC and validation

**⚡ UPDATE README Agent Status:** Phase=POST-IMPLEMENTATION, Step=Implementation complete

---

## Quick Commands Reference

Common commands you'll need during implementation:

```bash
# Run all tests (after each phase)
python tests/run_all_tests.py

# Run specific test file
python -m pytest tests/path/to/test_file.py -v

# Check git status
git status

# View unstaged changes
git diff

# Commit changes
git add -A
git commit -m "Phase X complete: {description}"

# Search for method usage
grep -r "method_name(" .

# Search for class usage
grep -r "ClassName" . --include="*.py"
```

**File Operations (use tools, not bash):**
- Read files: Use the `Read` tool
- Search files by name: Use the `Glob` tool
- Search file contents: Use the `Grep` tool
- Edit files: Use the `Edit` tool
- Write files: Use the `Write` tool

---

```
╔═════════════════════════════════════════════════════════════════╗
║  🛑 🛑 🛑 CRITICAL STOP - BEFORE PROCEEDING TO QC 🛑 🛑 🛑      ║
╠═════════════════════════════════════════════════════════════════╣
║                                                                 ║
║  You are about to transition from IMPLEMENTATION to QC.        ║
║  Do NOT proceed unless implementation is 100% complete.        ║
║                                                                 ║
║  MANDATORY VERIFICATION QUESTIONS (All must be YES):           ║
║                                                                 ║
║  □ Are ALL TODO tasks marked [x]?                              ║
║  □ Are ALL mini-QC checkpoints marked PASSED?                  ║
║  □ Do all unit tests pass (100% pass rate)?                    ║
║  □ Is implementation_checklist.md complete?                    ║
║  □ Is code_changes.md updated with all changes?                ║
║  □ Have I verified EVERY requirement from specs?               ║
║  □ Is there ZERO placeholder code or "TODO" comments?          ║
║  □ Can I run the feature end-to-end right now successfully?    ║
║                                                                 ║
║  SELF-VERIFICATION QUESTIONS:                                  ║
║  1. "Did I consult specs.md BEFORE implementing each item?"    ║
║  2. "Does the feature work end-to-end with real data?"         ║
║                                                                 ║
║  CONSEQUENCES OF PROCEEDING WITH INCOMPLETE CODE:              ║
║  ❌ QC will find incomplete implementation                     ║
║  ❌ You'll need to return to implementation phase              ║
║  ❌ Smoke tests will fail catastrophically                     ║
║  ❌ Time wasted on QC for non-functional code                  ║
║  ❌ User will lose confidence in the process                   ║
║                                                                 ║
║  RULE: If you answer "NO" or "UNCERTAIN" to ANY question       ║
║  above, you MUST NOT proceed to QC. Complete the missing       ║
║  items, re-verify, then check this gate again.                 ║
║                                                                 ║
╚═════════════════════════════════════════════════════════════════╝
```

---

## Exit Criteria - Ready to Leave This Guide

```
┌─────────────────────────────────────────────────────────────────┐
│  EXIT CRITERIA: Complete ALL items before proceeding to QC     │
└─────────────────────────────────────────────────────────────────┘
```

**You may ONLY proceed to `post_implementation_guide.md` when ALL of the following are true:**

✅ **All Tasks Complete:**
- [ ] Every TODO task marked `[x]` in `{feature_name}_todo.md`
- [ ] No tasks remain with `[ ]` or `[~]` status
- [ ] All phases complete (Phase 1, 2, 3, etc.)

✅ **Verification Complete:**
- [ ] Every requirement in implementation checklist checked off
- [ ] All acceptance criteria from TODO satisfied
- [ ] All mini-QC checkpoints show: **PASSED**
- [ ] No deviations from specs without documentation

✅ **Testing Complete:**
- [ ] All unit tests passing: `python tests/run_all_tests.py` exits code 0
- [ ] **100% pass rate** (not 99%, not "mostly passing")
- [ ] Tests run after EVERY phase showed passing
- [ ] No commented-out tests or `@skip` decorators added

✅ **Documentation Complete:**
- [ ] `{feature_name}_code_changes.md` contains ALL changes made
- [ ] Each change has description, file path, and justification
- [ ] `{feature_name}_lessons_learned.md` updated with any issues found
- [ ] All code has spec line references in comments

✅ **Code Quality:**
- [ ] No `# TODO` or `# FIXME` comments remain in code
- [ ] All methods have docstrings
- [ ] All edge cases from specs are handled
- [ ] Error handling matches spec requirements

✅ **Readiness Confirmed:**
- [ ] README.md Agent Status updated to: **"Implementation complete - Ready for QC"**
- [ ] README.md shows next action: "Proceed to post_implementation_guide.md"
- [ ] Git status shows no uncommitted changes OR all committed as WIP

**Self-Verification Questions (answer honestly):**

> Q1: "Did I consult specs.md CONTINUOUSLY during implementation?"
- **YES, constantly** → Proceed ✅
- **Mostly** → Warning: Re-verify against specs now ⚠️
- **Not really** → STOP: Code likely wrong, re-verify everything ❌

> Q2: "If I run the actual feature script right now, will it work end-to-end?"
- **YES, confident** → Proceed ✅
- **Probably** → Run it now to verify ⚠️
- **Not sure** → STOP: Implementation incomplete ❌

**If ANY checkbox above is unchecked OR any answer is not ✅:**
- ❌ DO NOT proceed to QC
- Complete the missing item(s)
- Fix any issues found
- Re-verify this entire checklist

**When ALL checkboxes are checked and verification passes:**
- ✅ Update README Agent Status: "Proceeding to Post-Implementation Phase"
- ✅ Close this guide
- ✅ Open `post_implementation_guide.md`
- ✅ Begin with "Verify Implementation Complete" section

---

## Related Guides

| Guide | When to Use | Link |
|-------|-------------|------|
| **TODO Creation Guide** | Previous guide - create TODO with 24 iterations | `todo_creation_guide.md` |
| **Post-Implementation Guide** | Next guide - QC and validation | `post_implementation_guide.md` |
| **Planning Guide** | If scope changes - return to planning | `feature_planning_guide.md` |
| **Protocols Reference** | Detailed protocol definitions | `protocols/README.md` |
| **Templates** | File templates for features | `templates.md` |
| **Prompts Reference** | Conversation prompts | `prompts_reference.md` |
| **Guides README** | Overview of all guides | `README.md` |

### Transition Points

**From TODO Creation Guide → This guide:**
- All 24 iterations complete
- Iteration 24 (Implementation Readiness) passed
- Interface verification complete

**This guide → Post-Implementation Guide:**
- All TODO tasks complete
- All tests passing
- All mini-QC checkpoints passed

**Back to Planning Guide:**
- If major scope changes discovered during implementation
- If specs need significant updates

---

*This guide assumes TODO creation (24 iterations) is complete. If verification is not complete, use `todo_creation_guide.md` first.*
