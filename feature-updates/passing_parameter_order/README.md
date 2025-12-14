# Passing Parameter Order - Work in Progress

---

## AGENT STATUS (Read This First)

**Current Phase:** COMPLETE
**Current Step:** Done
**Next Action:** Commit and move to done/

### Full Workflow Checklist

> **Instructions:** Update this checklist as you complete each step. This is your persistent state across sessions.

**PLANNING PHASE** (feature_planning_guide.md)
- [x] Phase 1: Initial Setup
  - [x] Create folder structure
  - [x] Move notes file
  - [x] Create README.md (this file)
  - [x] Create passing_parameter_order_specs.md
  - [x] Create passing_parameter_order_checklist.md
  - [x] Create passing_parameter_order_lessons_learned.md
- [x] Phase 2: Deep Investigation
  - [x] Analyze notes thoroughly
  - [x] Research codebase patterns
  - [x] Populate checklist with questions
  - [x] Update specs with context
- [x] Phase 3: Report and Pause
  - [x] Present findings to user
  - [x] Wait for user direction
- [x] Phase 4: Resolve Questions
  - [x] All checklist items resolved [x]
  - [x] Specs updated with all decisions
- [x] Planning Complete - Ready for Implementation

**DEVELOPMENT PHASE** (feature_development_guide.md)
- [x] Step 1: Create TODO file
- [x] 24 Verification Iterations complete
- [x] Implementation complete
- [x] Tests passing (100% - 2221 tests)

**POST-IMPLEMENTATION PHASE**
- [x] QC Round 1 - No issues found
- [x] QC Round 2 - Added 2 missing validation tests
- [x] QC Round 3 - Fixed 5 outdated docstring examples
- [ ] Commit changes
- [ ] Move folder to done/

---

## What This Is

Allow runner scripts (`run_simulation.py`, `run_draft_order_loop.py`) to define their own `PARAMETER_ORDER` variable and pass it to the simulation system. This enables different scripts to optimize different sets of parameters in different orders without modifying the core simulation code.

## Why We Need This

1. **Different Use Cases:** `run_simulation.py` focuses on general parameter optimization, while `run_draft_order_loop.py` focuses on draft order strategies - they may need different parameter orderings
2. **Flexibility:** Allows experimentation with optimization order without modifying core simulation code
3. **Script-Level Control:** Runner scripts can define exactly which parameters to optimize and in what order

## Scope

**IN SCOPE:**
- Define `PARAMETER_ORDER` at the top of each runner script
- Pass `PARAMETER_ORDER` from runner scripts to `SimulationManager`
- Pass `PARAMETER_ORDER` from `SimulationManager` to `ConfigGenerator`
- Update `ConfigGenerator` to use instance variable instead of class constant
- Update tests that rely on the current class constant pattern

**OUT OF SCOPE:**
- Changing the actual parameters available for optimization
- Changing the parameter optimization algorithm
- Adding new parameters to the system

### Files in This Folder

| File | Purpose |
|------|---------|
| `README.md` | This file - context and status for agents |
| `passing_parameter_order_notes.txt` | Original scratchwork notes from user |
| `passing_parameter_order_specs.md` | Main specification with detailed requirements |
| `passing_parameter_order_checklist.md` | Tracks open questions and decisions |
| `passing_parameter_order_lessons_learned.md` | Captures issues to improve the guides |

## Key Context for Future Agents

### Current Architecture

**PARAMETER_ORDER is currently a class constant in ConfigGenerator:**
```python
# simulation/ConfigGenerator.py lines 191-225
class ConfigGenerator:
    PARAMETER_ORDER = [
        'NORMALIZATION_MAX_SCALE',
        'SAME_POS_BYE_WEIGHT',
        # ... 22 more parameters
    ]
```

**Accessed via instance variable pattern:**
- `SimulationManager._detect_resume_state()` at line 547: `self.config_generator.PARAMETER_ORDER`
- `SimulationManager.run_iterative_optimization()` at line 649: `self.config_generator.PARAMETER_ORDER`
- `ConfigGenerator.generate_iterative_combinations()` at line 800: `self.PARAMETER_ORDER`

**Tests access via class attribute:**
- `tests/simulation/test_config_generator.py` lines 726-850: Multiple tests use `ConfigGenerator.PARAMETER_ORDER`

### Data Flow

```
run_simulation.py
  → SimulationManager.__init__(baseline_config_path, ...)
    → ConfigGenerator.__init__(baseline_config_path, num_test_values, num_parameters_to_test)
      → Uses class constant: PARAMETER_ORDER
  → SimulationManager.run_iterative_optimization()
    → Uses: self.config_generator.PARAMETER_ORDER
```

### Key Files

| File | Line Numbers | Purpose |
|------|--------------|---------|
| `simulation/ConfigGenerator.py` | 191-225 | Defines PARAMETER_ORDER class constant |
| `simulation/ConfigGenerator.py` | 800 | Validates param_name against PARAMETER_ORDER |
| `simulation/ConfigGenerator.py` | 809, 831 | Uses PARAMETER_ORDER for capping/sampling |
| `simulation/SimulationManager.py` | 547, 649 | Accesses PARAMETER_ORDER via config_generator |
| `run_simulation.py` | 327, 385 | Creates SimulationManager (would pass PARAMETER_ORDER) |
| `run_draft_order_loop.py` | 484 | Creates SimulationManager (would pass PARAMETER_ORDER) |
| `tests/simulation/test_config_generator.py` | 726-850 | Tests that use ConfigGenerator.PARAMETER_ORDER |

## What's Resolved

1. **Q1 - Default Value Strategy:** Require explicit passing (no default) - `parameter_order` is a required parameter
2. **Q2 - Backward Compatibility:** Deprecate class constant, update all tests - only instance variable exists
3. **Q3 - Validation:** Validate at init time - check all param names exist in PARAM_DEFINITIONS

## What's Still Pending

(None - planning complete, ready for implementation)

## How to Continue This Work

1. **Check the AGENT STATUS section above** for current phase and step
2. Read `passing_parameter_order_specs.md` for complete specifications
3. Read `passing_parameter_order_checklist.md` to see what's resolved vs pending
4. Continue from the current step in the workflow checklist
5. **Update the AGENT STATUS section** as you complete steps
