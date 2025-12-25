# Feature Development Guides

This folder contains workflow guides for agents implementing new features in the Fantasy Football Helper Scripts project.

## Quick Decision: Which File Do I Need?

| Situation | File to Use |
|-----------|-------------|
| User says "help me develop the {feature} feature" | Start with **Planning Guide** |
| User provides a `.txt` file with feature requirements | Start with **Planning Guide** |
| User says "prepare for updates based on {feature}" | Use **TODO Creation Guide** |
| Planning is complete, specs approved, need to create TODO | Use **TODO Creation Guide** |
| TODO creation complete (24 iterations), ready to code | Use **Implementation Execution Guide** |
| Implementation complete, need QC and validation | Use **Post-Implementation Guide** |
| Need to execute a specific protocol | Use **Protocols Reference** |
| Need to create a new feature file | Use **Templates** |
| Need conversation prompts for user discussions | Use **Prompts Reference** |
| Resuming work on an existing feature | Check the feature's README.md for status |

---

## Where Am I? Quick Reference

Use this table to quickly determine your current location when resuming work:

### Planning Phase

| README Status Shows | Current Phase | Next Action |
|---------------------|---------------|-------------|
| "Phase 1: Creating Structure" | Phase 1 | Finish creating files |
| "Phase 2: Investigation" | Phase 2 | Continue codebase research |
| "Phase 3: Awaiting User Input" | Phase 3 STOP | Wait for user direction |
| "Phase 4: Resolving Items" | Phase 4 | Check checklist for next `[ ]` item |
| "Ready for Implementation" | Planning done | Switch to Development Guide |

### Development Phase

#### TODO Creation (Verification)

| TODO Shows | Current Stage | Guide to Use | Next Action |
|------------|---------------|--------------|-------------|
| No TODO file exists | Pre-TODO Creation | **TODO Creation Guide** | Create TODO from specs |
| "First Round: X/7" | Verification Round 1 | **TODO Creation Guide** | Continue to iteration X+1 |
| "Questions created" waiting | Step 3 pause | **TODO Creation Guide** | Wait for user answers |
| "Second Round: X/9" | Verification Round 2 | **TODO Creation Guide** | Continue to iteration X+1 |
| "Third Round: X/8" | Verification Round 3 | **TODO Creation Guide** | Continue to iteration X+1 |
| "24/24 complete" | Verification Complete | **Implementation Execution Guide** | Begin implementation |

#### Implementation Execution

| TODO Shows | Current Stage | Guide to Use | Next Action |
|------------|---------------|--------------|-------------|
| Phase X in progress | Implementation | **Implementation Execution Guide** | Execute TODO tasks |
| All tasks `[x]` | Implementation Complete | **Post-Implementation Guide** | Run QC rounds |

#### Post-Implementation (QC & Validation)

| Status Shows | Current Stage | Guide to Use | Next Action |
|--------------|---------------|--------------|-------------|
| "Smoke test complete" | QC not started | **Post-Implementation Guide** | Start QC Round 1 |
| "QC Round 1 in progress" | QC Round 1 | **Post-Implementation Guide** | Complete Round 1 |
| "QC Round 2 in progress" | QC Round 2 | **Post-Implementation Guide** | Complete Round 2 |
| "QC Round 3 in progress" | QC Round 3 | **Post-Implementation Guide** | Complete Round 3 |
| "QC Round 3: PASSED" | Complete | - | Move to `done/` folder and commit |

## Files in This Folder

| File | Purpose |
|------|---------|
| `feature_planning_guide.md` | Planning phase workflow (Phases 1-4) with question generation and codebase verification |
| `todo_creation_guide.md` | TODO creation through 24 verification iterations (BEFORE coding) |
| `implementation_execution_guide.md` | Implementation workflow - executing the TODO file with continuous verification |
| `post_implementation_guide.md` | QC, smoke testing, and validation (AFTER coding) |
| `protocols_reference.md` | Detailed protocol definitions (15+ protocols) including Mock Audit, Test-First, and Rollback |
| `templates.md` | File templates for all feature files with QA checkpoint structure and Round Checkpoint Summary |
| `prompts_reference.md` | Ready-to-use conversation prompts |
| `README.md` | This overview (you are here) |

---

## Guide Overview

### 1. Feature Planning Guide

**Purpose:** Transform a raw feature request (`.txt` file) into a fully-specified, approved plan before any code is written.

**When to use:**
- User has placed a `.txt` file in `feature-updates/` folder
- User requests "help me develop" or "prepare for updates"
- Starting any new feature from scratch

**What it produces:**
- Feature folder: `feature-updates/{feature_name}/`
- 5 files total:
  - 4 created: `README.md`, `_specs.md`, `_checklist.md`, `_lessons_learned.md`
  - 1 moved: `_notes.txt` (original scratchwork)
- User-approved specification ready for implementation

**Key phases:**
1. Create folder structure
2. Investigate codebase (with 3-iteration question generation + codebase verification rounds)
3. Report findings and STOP for user approval
4. Iterate until fully specified

**Critical rule:** Phase 3 requires a FULL STOP. Do not proceed to TODO creation without explicit user approval.

**Next guide:** → `todo_creation_guide.md`

---

### 2. TODO Creation Guide

**Purpose:** Create comprehensive TODO file through 24 verification iterations BEFORE writing any code.

**When to use:**
- Planning is complete (feature folder exists with approved `_specs.md`)
- User says "prepare for updates based on {feature}"
- The feature's README.md shows "Ready for Implementation"

**What it produces:**
- `{feature_name}_todo.md` with complete implementation plan
- Interface verification documentation
- Integration matrix
- Questions file (if needed)
- Implementation readiness confirmation

**Key steps:**
1. Sub-feature analysis (if needed)
2. Create draft TODO from specs
3. Complete Round 1 (iterations 1-7 + 4a)
4. Create questions file (if needed) and wait for answers
5. Complete Round 2 (iterations 8-16)
6. Complete Round 3 (iterations 17-24 + 23a)

**Critical protocols** (defined in `protocols_reference.md`):
- Algorithm Traceability Matrix (iterations 4, 11, 19)
- TODO Specification Audit (iteration 4a)
- End-to-End Data Flow (iterations 5, 12)
- Skeptical Re-verification (iterations 6, 13, 22)
- Integration Gap Check (iterations 7, 14, 23)
- Pre-Implementation Spec Audit (iteration 23a)
- Interface Verification (before declaring complete)

**Next guide:** → `implementation_execution_guide.md`

---

### 3. Implementation Execution Guide

**Purpose:** Execute the TODO file and build the feature with continuous spec verification.

**When to use:**
- TODO creation complete (all 24 iterations done)
- Interface verification complete
- Iteration 24 (Implementation Readiness) passed

**What it produces:**
- Working code changes
- Updated tests (100% pass rate required)
- `{feature_name}_implementation_checklist.md` with all requirements verified
- `{feature_name}_code_changes.md` with all changes documented
- Updated `_lessons_learned.md`

**Key steps:**
1. Create implementation checklist
2. Execute TODO tasks phase by phase
3. Continuous spec verification (before AND after each requirement)
4. Incremental QA checkpoints after each major component
5. Update documentation throughout

**Critical rules:**
- Keep specs.md VISIBLE at all times during coding
- Verify EACH requirement BEFORE implementing
- Verify EACH requirement AFTER implementing
- Run tests after EVERY phase (100% pass required)
- Mini-QC checkpoints after each major component

**Next guide:** → `post_implementation_guide.md`

---

### 4. Post-Implementation Guide

**Purpose:** Quality control, smoke testing, and validation AFTER implementation complete.

**When to use:**
- All TODO tasks marked `[x]`
- All unit tests passing (100% pass rate)
- All mini-QC checkpoints passed

**What it produces:**
- Requirement verification report
- Smoke testing report (3 parts: import, entry point, execution)
- 3 QC round reports in code_changes.md
- Lessons learned review
- Guide update recommendations
- Feature moved to `done/` folder
- Git commit with changes

**Key steps:**
1. Run all unit tests (100% pass required)
2. Execute Requirement Verification Protocol
3. Execute Smoke Testing Protocol (MANDATORY)
4. Complete QC Round 1 (initial review)
5. Complete QC Round 2 (deep verification)
6. Complete QC Round 3 (final skeptical review)
7. Review lessons learned and update guides
8. Move to done/ and commit

**Critical rules:**
- ALL 3 QC rounds are MANDATORY
- Smoke testing CANNOT be skipped
- Test ALL execution modes, not just --help
- Verify output CONTENT, not just file existence
- Compare to baseline/similar features

**Result:** Feature complete and ready for production

---

### 5. Protocols Reference

**Purpose:** Detailed definitions of all verification and quality protocols.

**When to use:**
- During development iterations when executing a specific protocol
- When you need the exact steps for a protocol
- For reference on acceptance criteria

**Protocols included:**
- Standard Verification Protocol
- Algorithm Traceability Matrix Protocol
- End-to-End Data Flow Protocol
- Skeptical Re-verification Protocol
- Integration Gap Check Protocol
- Fresh Eyes Review Protocol
- Edge Case Verification Protocol
- Test Coverage Planning Protocol
- Implementation Readiness Protocol
- Requirement Verification Protocol
- Quality Control Review Protocol
- Lessons Learned Protocol
- Guide Update Protocol
- Pre-commit Validation Protocol

---

### 6. Templates

**Purpose:** Ready-to-use file templates for all feature documentation.

**When to use:**
- Phase 1: Creating feature folder structure
- Step 3: Creating questions file
- Step 1: Creating TODO file
- During implementation: Creating code changes documentation

**Templates included:**
- Feature README template
- Specification template
- Checklist template
- Lessons learned template
- Questions file template
- TODO file template (with iteration tracker)
- Code changes template

---

### 7. Prompts Reference

**Purpose:** Ready-to-use conversation prompts for guiding discussions with users.

**When to use:**
- During planning conversations when you need to present options
- When scope is creeping and you need to refocus
- When presenting technical decisions or trade-offs
- When asking for clarification or direction

**Prompts included:**
- Suggesting options when user has vague ideas
- Surfacing missing details
- Managing scope creep
- Presenting technical decisions
- Discussing edge cases
- Progress updates
- Problem situation responses

---

## Workflow Summary

```
┌─────────────────────────────────────────────────────────────────┐
│                    FEATURE LIFECYCLE                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  updates/{feature}.txt  ──────►  1. PLANNING GUIDE              │
│                                       │                         │
│                                       ▼                         │
│                              feature-updates/                   │
│                              {feature_name}/                    │
│                              _specs.md (approved)               │
│                                       │                         │
│                                       ▼                         │
│                              2. TODO CREATION GUIDE             │
│                              (24 verification iterations)       │
│                                       │                         │
│                                       ▼                         │
│                              {feature_name}_todo.md             │
│                              (ready to implement)               │
│                                       │                         │
│                                       ▼                         │
│                              3. IMPLEMENTATION GUIDE            │
│                              (execute TODO with                 │
│                               continuous verification)          │
│                                       │                         │
│                                       ▼                         │
│                              Working Code                       │
│                              + Tests Passing                    │
│                                       │                         │
│                                       ▼                         │
│                              4. POST-IMPLEMENTATION GUIDE       │
│                              (smoke tests + 3 QC rounds)        │
│                                       │                         │
│                                       ▼                         │
│                              Complete Feature                   │
│                              → done/ folder                     │
│                              → git commit                       │
│                                                                 │
│  All guides reference protocols_reference.md and templates.md  │
│  as needed throughout the process                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Important Notes for Agents

1. **Never skip planning.** Even if a feature seems simple, go through the planning workflow first.

2. **Respect the STOP points.** Both guides have mandatory pause points requiring user approval.

3. **Use the checklists.** Each guide has an Agent Quick Reference Checklist - use it to track progress.

4. **Update lessons learned.** After completing a feature, always document what you learned in `_lessons_learned.md`.

5. **100% test pass rate required.** Never commit code with failing tests.

6. **Reference protocols as needed.** The development guide is streamlined; detailed protocol steps are in `protocols_reference.md`.

## File Locations

```
feature-updates/
├── guides/                              # This folder
│   ├── README.md                        # You are here
│   ├── feature_planning_guide.md        # 1. Planning workflow
│   ├── todo_creation_guide.md           # 2. TODO creation (24 iterations)
│   ├── implementation_execution_guide.md # 3. Implementation workflow
│   ├── post_implementation_guide.md     # 4. QC and validation
│   ├── protocols_reference.md           # Detailed protocol definitions
│   ├── templates.md                     # File templates
│   └── prompts_reference.md             # Conversation prompts
├── {feature_name}/                      # Feature folders created during planning
│   ├── README.md                        # Created in planning
│   ├── {feature_name}_specs.md          # Created in planning
│   ├── {feature_name}_checklist.md      # Created in planning
│   ├── {feature_name}_lessons_learned.md # Created in planning
│   ├── {feature_name}_notes.txt         # Moved during planning
│   ├── {feature_name}_questions.md      # Created during TODO creation
│   ├── {feature_name}_todo.md           # Created during TODO creation
│   ├── {feature_name}_implementation_checklist.md # Created during implementation
│   └── {feature_name}_code_changes.md   # Created during implementation
├── done/                                # Completed features
└── *.txt                                # Raw feature requests (input)
```

## Questions?

If a guide seems unclear or you encounter a situation not covered, document it in the feature's `_lessons_learned.md` file. This helps improve the guides for future agents.
