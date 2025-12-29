# Feature Development Guides

This folder contains workflow guides for agents implementing new features in the Fantasy Football Helper Scripts project.

## Quick Decision: Which File Do I Need?

| Situation | File to Use |
|-----------|-------------|
| User says "help me develop the {feature} feature" | Start with **Feature Creation Guide** |
| User provides a `.txt` file with feature requirements | Start with **Feature Creation Guide** |
| After deciding on sub-features, need detailed planning | Use **Feature Deep Dive Guide** (per sub-feature) |
| All sub-features planned, ready for implementation | Use **TODO Creation Guide** (per sub-feature) |
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

#### Single Feature Projects

| README Status Shows | Current Phase | Next Action |
|---------------------|---------------|-------------|
| "Phase 1: Creating Structure" | Phase 1 | Finish creating files |
| "Phase 2: Investigation" | Phase 2 | Continue codebase research |
| "Phase 3: Awaiting User Input" | Phase 3 STOP | Wait for user direction |
| "Phase 4: Resolving Items" | Phase 4 | Check checklist for next `[ ]` item |
| "Ready for Implementation" | Planning done | Switch to Development Guide |

#### Multi-Sub-Feature Projects

| Status Shows | What It Means | Next Action |
|--------------|---------------|-------------|
| **"Sub-feature 1 of 8 in Phase 2"** | Deep dive for sub-feature 1 | Continue Phase 2 for sub-feature 1 |
| **Check SUB_FEATURES_PHASE_TRACKER.md** | Master progress tracker | Review tracker to see all sub-feature progress |
| **"Phase 3: User Questions (Sub-feature 2)"** | Awaiting user decisions | Present next question ONE AT A TIME |
| **"Phase 6: Alignment Review"** | All sub-features complete Phase 4 | Review all specs together for conflicts |
| **"Ready for Implementation - Sub-feature 1"** | All sub-features aligned (Phase 7) | Start TODO creation for sub-feature 1 |
| **"Sub-feature 3: Implementation"** | Coding sub-feature 3 | Execute TODO items, run tests |
| **"Sub-feature 5: QC Round 2"** | QC for sub-feature 5 | Complete QC Round 2 then Round 3 |

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

| File | Purpose | Status |
|------|---------|--------|
| `feature_creation_guide.md` | **NEW** - Initial setup, broad reconnaissance, sub-feature breakdown decision | **CURRENT** |
| `feature_deep_dive_guide.md` | **NEW** - Detailed planning per sub-feature with interactive question resolution | **CURRENT** |
| `feature_planning_guide.md` | Legacy monolithic planning guide | **DEPRECATED** |
| `todo_creation_guide.md` | TODO creation through 24 verification iterations (execute per sub-feature) | **CURRENT** |
| `implementation_execution_guide.md` | Implementation workflow (execute per sub-feature) | **CURRENT** |
| `post_implementation_guide.md` | QC, smoke testing, validation (execute per sub-feature) | **CURRENT** |
| `protocols/README.md` | Detailed protocol definitions (15+ protocols) | **CURRENT** |
| `templates.md` | File templates for all feature files | **CURRENT** |
| `prompts_reference.md` | Ready-to-use conversation prompts including new phase transitions | **CURRENT** |
| `README.md` | This overview (you are here) | **CURRENT** |

---

## Guide Overview

### NEW WORKFLOW (Two-Guide Approach)

**⚠️ Important Change:** Planning has been split into two guides based on lessons learned from large features.

### 1. Feature Creation Guide (NEW)

**Purpose:** Initial setup, broad reconnaissance, and sub-feature breakdown decision.

**When to use:**
- User says "help me develop {feature}" or provides `.txt` file
- Starting any new feature from scratch

**What it produces:**
- Feature folder: `feature-updates/{feature_name}/`
- Either:
  - **Single feature:** `_specs.md`, `_checklist.md`, `research/` folder
  - **Sub-features:** `SUB_FEATURES_README.md`, multiple `sub_feature_{N}_spec.md` files, `research/` folder
- **NO global spec/checklist if using sub-features**

**Key phases:**
1. Create folder structure
2. Broad reconnaissance (identify major components, estimate scope)
3. **CRITICAL: Sub-feature breakdown decision** (triggers: 3+ components, 30+ items)
4. Create appropriate file structure
5. Transition to deep dive

---

### 2. Feature Deep Dive Guide (NEW)

**Purpose:** Detailed research and question resolution for ONE sub-feature at a time.

**When to use:**
- After feature creation guide completes
- Execute ONCE per sub-feature (or once for single feature)

**What it produces:**
- Complete spec with implementation-level detail
- Fully resolved checklist (all items `[x]`)
- Research documents in `research/` folder
- Cross-sub-feature alignment verification

**Key phases:**
1. Targeted research (only this sub-feature's scope)
2. Update spec and checklist
3. **Interactive question resolution (ONE at a time)**
4. Sub-feature complete + dynamic scope adjustment check
5. Next sub-feature or alignment review
6. **Cross-sub-feature alignment review** (MANDATORY for multi-sub-feature)
7. Ready for sequential implementation

---

### 3. Legacy Planning Guide (DEPRECATED)

**Purpose:** Old monolithic planning approach.

**When to use:** Only for reference or maintaining features that used the old approach.

**Why deprecated:** Lessons learned showed that large features (30+ items) become unmanageable without early sub-feature breakdown. The new two-guide approach addresses this.

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

**Critical protocols** (defined in `protocols/README.md`):
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
│  updates/{feature}.txt  ──────►  1a. FEATURE CREATION GUIDE     │
│                                       │                         │
│                                       ▼                         │
│                              Broad reconnaissance               │
│                              Sub-feature decision?              │
│                                       │                         │
│                    ┌──────────────────┴──────────────────┐      │
│                    │                                     │      │
│               Single Feature                   Multi-Sub-Feature│
│                    │                                     │      │
│                    ▼                                     ▼      │
│            _specs.md                        SUB_FEATURES_       │
│            _checklist.md                    README.md           │
│            research/                        🚨 PHASE_TRACKER.md │
│                    │                        sub_feature_*.md    │
│                    │                        research/           │
│                    └──────────────────┬──────────────────┘      │
│                                       ▼                         │
│                              1b. FEATURE DEEP DIVE GUIDE        │
│                              (per sub-feature)                  │
│                              - Targeted research                │
│                              - Interactive questions            │
│                              - Alignment review (Phase 6)       │
│                                       │                         │
│                                       ▼                         │
│                              Specs complete & aligned           │
│                              → Ready for Implementation         │
│                                       │                         │
│                                       ▼                         │
│                              2. TODO CREATION GUIDE             │
│                              (24 verification iterations)       │
│                              (per sub-feature)                  │
│                                       │                         │
│                                       ▼                         │
│                              {name}_todo.md (ready)             │
│                                       │                         │
│                                       ▼                         │
│                              3. IMPLEMENTATION GUIDE            │
│                              (execute TODO with                 │
│                               continuous verification)          │
│                              (per sub-feature)                  │
│                                       │                         │
│                                       ▼                         │
│                              Working Code + Tests Passing       │
│                                       │                         │
│                                       ▼                         │
│                              4. POST-IMPLEMENTATION GUIDE       │
│                              (smoke tests + 3 QC rounds)        │
│                              (per sub-feature)                  │
│                                       │                         │
│                                       ▼                         │
│                              Complete Feature                   │
│                              → done/ folder                     │
│                              → git commit                       │
│                                                                 │
│  All guides reference protocols/README.md and templates.md      │
│  Multi-sub-feature: Check PHASE_TRACKER.md at every session   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Important Notes for Agents

1. **Never skip planning.** Even if a feature seems simple, go through the planning workflow first.

2. **Respect the STOP points.** Both guides have mandatory pause points requiring user approval.

3. **Use the checklists.** Each guide has an Agent Quick Reference Checklist - use it to track progress.

4. **Update lessons learned.** After completing a feature, always document what you learned in `_lessons_learned.md`.

5. **100% test pass rate required.** Never commit code with failing tests.

6. **Reference protocols as needed.** The development guide is streamlined; detailed protocol steps are in `protocols/README.md`.

7. **🚨 Use the phase tracker for multi-sub-feature projects.** Check `SUB_FEATURES_PHASE_TRACKER.md` at the START of EVERY session to see exact progress across all sub-features. Update it immediately after completing each phase. Re-read the corresponding guide BEFORE marking any phase complete.

## File Locations

```
feature-updates/
├── guides/                              # This folder
│   ├── README.md                        # You are here
│   ├── feature_creation_guide.md        # 1a. Initial setup & sub-feature decision
│   ├── feature_deep_dive_guide.md       # 1b. Detailed planning per sub-feature
│   ├── feature_planning_guide.md        # LEGACY - deprecated (use creation + deep dive)
│   ├── todo_creation_guide.md           # 2. TODO creation (24 iterations)
│   ├── implementation_execution_guide.md # 3. Implementation workflow
│   ├── post_implementation_guide.md     # 4. QC and validation
│   ├── protocols/README.md              # Detailed protocol definitions
│   ├── templates.md                     # File templates (includes PHASE_TRACKER)
│   └── prompts_reference.md             # Conversation prompts
├── {feature_name}/                      # Single feature folders
│   ├── README.md                        # Created in creation phase
│   ├── {feature_name}_specs.md          # Created in creation, populated in deep dive
│   ├── {feature_name}_checklist.md      # Created in creation, populated in deep dive
│   ├── {feature_name}_lessons_learned.md # Created in creation
│   ├── {feature_name}_notes.txt         # Moved during creation phase
│   ├── {feature_name}_questions.md      # Created during TODO creation (if needed)
│   ├── {feature_name}_todo.md           # Created during TODO creation
│   ├── {feature_name}_implementation_checklist.md # Created during implementation
│   ├── {feature_name}_code_changes.md   # Created during implementation
│   └── research/                        # Research documents folder
├── {feature_name}/                      # Multi-sub-feature folders
│   ├── README.md                        # Created in creation phase
│   ├── SUB_FEATURES_README.md           # Overview of all sub-features
│   ├── 🚨 SUB_FEATURES_PHASE_TRACKER.md # MANDATORY master progress tracker
│   ├── sub_feature_01_{name}_spec.md    # Per sub-feature specs
│   ├── sub_feature_01_{name}_checklist.md # Per sub-feature checklists
│   ├── sub_feature_02_{name}_spec.md    # (repeat for each sub-feature)
│   ├── sub_feature_02_{name}_checklist.md
│   ├── {feature_name}_lessons_learned.md # Shared across all sub-features
│   ├── {feature_name}_notes.txt         # Original notes
│   └── research/                        # Shared research folder
├── done/                                # Completed features
└── *.txt                                # Raw feature requests (input)
```

## Questions?

If a guide seems unclear or you encounter a situation not covered, document it in the feature's `_lessons_learned.md` file. This helps improve the guides for future agents.
