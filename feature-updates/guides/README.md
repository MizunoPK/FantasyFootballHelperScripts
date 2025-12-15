# Feature Development Guides

This folder contains workflow guides for agents implementing new features in the Fantasy Football Helper Scripts project.

## Quick Decision: Which File Do I Need?

| Situation | File to Use |
|-----------|-------------|
| User says "help me develop the {feature} feature" | Start with **Planning Guide** |
| User provides a `.txt` file with feature requirements | Start with **Planning Guide** |
| User says "prepare for updates based on {feature}" | Use **Development Guide** |
| Planning is complete, specs approved, ready to code | Use **Development Guide** |
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

| TODO Shows | Current Stage | Next Action |
|------------|---------------|-------------|
| No TODO file exists | Pre-development | Create TODO from specs |
| "First Round: X/7" | Verification Round 1 | Continue to iteration X+1 |
| "Questions created" waiting | Step 3 pause | Wait for user answers |
| "Second Round: X/9" | Verification Round 2 | Continue to iteration X+1 |
| "Third Round: X/8" | Verification Round 3 | Continue to iteration X+1 |
| "24/24 complete" | Implementation | Execute TODO tasks |
| All tasks `[x]` | Post-implementation | Run QC rounds |
| "QC Round 3: PASSED" | Complete | Move to `done/` folder |

## Files in This Folder

| File | Purpose |
|------|---------|
| `feature_planning_guide.md` | Planning phase workflow (Phases 1-4) with question generation and codebase verification |
| `feature_development_guide.md` | Development workflow (24 iterations + implementation) with interface verification and incremental QA |
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

**Critical rule:** Phase 3 requires a FULL STOP. Do not proceed to implementation without explicit user approval.

---

### 2. Feature Development Guide

**Purpose:** Implement an approved feature specification through 24 rigorous verification iterations.

**When to use:**
- Planning is complete (feature folder exists with approved `_specs.md`)
- User says "implement" or "start development"
- The feature's README.md shows "Ready for Implementation"

**What it produces:**
- Working code changes
- Updated tests (100% pass rate required)
- Updated documentation
- Completed `_lessons_learned.md`

**Key phases:**
1. Pre-implementation: 24 verification iterations (3 rounds: 7 + 9 + 8) with interface verification
2. Implementation: Code + test + document with incremental QA checkpoints
3. Post-implementation: E2E script execution + 3 QC rounds + lessons learned

**Critical protocols** (defined in `protocols_reference.md`):
- Skeptical Re-verification (iterations 6, 13, 22)
- End-to-End Data Flow checks (iterations 5, 12)
- Integration Gap Check (iterations 7, 14, 23) - with unresolved alternatives check
- Algorithm Traceability Matrix (iterations 4, 11, 19)
- Interface Verification (pre-implementation)
- Mock Audit (iteration 21)

---

### 3. Protocols Reference

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

### 4. Templates

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

### 5. Prompts Reference

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
│  updates/{feature}.txt  ──────►  PLANNING GUIDE                 │
│                                       │                         │
│                                       ▼                         │
│                              feature-updates/                   │
│                              {feature_name}/                    │
│                                       │                         │
│                                       ▼                         │
│                              User Approval                      │
│                                       │                         │
│                                       ▼                         │
│                              DEVELOPMENT GUIDE                  │
│                              (references protocols_reference.md │
│                               and templates.md as needed)       │
│                                       │                         │
│                                       ▼                         │
│                              Working Feature                    │
│                              + Tests + Docs                     │
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
│   ├── feature_planning_guide.md        # Planning workflow
│   ├── feature_development_guide.md     # Development workflow
│   ├── protocols_reference.md           # Detailed protocol definitions
│   ├── templates.md                     # File templates
│   └── prompts_reference.md             # Conversation prompts
├── {feature_name}/                      # Feature folders created during planning
│   ├── README.md
│   ├── {feature_name}_specs.md
│   ├── {feature_name}_checklist.md
│   ├── {feature_name}_lessons_learned.md
│   ├── {feature_name}_notes.txt
│   ├── {feature_name}_questions.md      # Created during development
│   ├── {feature_name}_todo.md           # Created during development
│   └── {feature_name}_code_changes.md   # Created during development
├── done/                                # Completed features
└── *.txt                                # Raw feature requests (input)
```

## Questions?

If a guide seems unclear or you encounter a situation not covered, document it in the feature's `_lessons_learned.md` file. This helps improve the guides for future agents.
