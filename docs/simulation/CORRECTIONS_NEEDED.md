# WIN_RATE_SIMULATION_FLOW.md - Critical Corrections Required

## Verification Status: **FAILED - Major Errors Found**

This document lists all errors found after verification against actual source code.

---

## CRITICAL ERRORS

### 1. **WRONG ENTRY POINT SCRIPT NAME** (Throughout Document)

**Error**: Document consistently uses `run_simulation.py`
**Actual**: `run_win_rate_simulation.py`

**Locations to Fix**:
- All command examples
- All references to the entry point
- Usage instructions

**Correct Examples**:
```bash
# WRONG (in document):
python run_simulation.py iterative --sims 100

# CORRECT:
python run_win_rate_simulation.py iterative --sims 100
```

---

### 2. **WRONG PARAMETER COUNT** (Multiple Sections)

**Error**: Document states "24 parameters (5 draft strategy + 16 accuracy)"
**Actual**: **7 parameters** for win rate simulation only

**Source**: `run_win_rate_simulation.py` lines 54-66:
```python
PARAMETER_ORDER = [
    'DRAFT_NORMALIZATION_MAX_SCALE',      # 1
    'SAME_POS_BYE_WEIGHT',                # 2
    'DIFF_POS_BYE_WEIGHT',                # 3
    'PRIMARY_BONUS',                       # 4
    'SECONDARY_BONUS',                     # 5
    'ADP_SCORING_WEIGHT',                  # 6
    'PLAYER_RATING_SCORING_WEIGHT',        # 7
]
```

**Clarification Needed**:
- Win Rate Simulation optimizes **7 BASE_CONFIG_PARAMS** (draft strategy parameters)
- Accuracy Simulation optimizes **16 WEEK_SPECIFIC_PARAMS** (prediction parameters)
- These are **separate simulations** with separate entry points
- ConfigGenerator.py defines 24 total parameters, but win rate only uses 7

**Locations to Fix**:
- Overview section
- Configuration System section
- Parameter listings
- All calculations based on parameter count

---

### 3. **WRONG FORMULA IN FULL MODE** (Section: Execution Modes)

**Error**: Document states formula as `(test_values + 1)^24`
**Actual**: `(test_values + 1)^6`

**Source**: `run_win_rate_simulation.py` line 360:
```python
total_configs = (args.test_values + 1) ** 6
```

**Comment in code** (SimulationManager.py line 6):
> "Generate 46,656 parameter combinations"

**Verification**: 6^6 = 46,656 ✓

**Impact**:
- Changes total config count dramatically
- With test_values=5: (5+1)^6 = 46,656 NOT (5+1)^24 = 4.7 × 10^18

---

### 4. **WRONG ITERATIVE MODE CALCULATIONS** (Section: Complete Execution Flow)

**Error**: Document states:
- "num_params = 24"
- "Total configurations: 168" (24 × 7)

**Actual**:
- num_params = len(PARAMETER_ORDER) = **7**
- configs_per_param = test_values + 1 = **6** (default)
- Total configurations = 7 × 6 = **42 configs**

**Source**: `run_win_rate_simulation.py` lines 388-395:
```python
num_params = 24  # 4 scalars + 20 multipliers  ← COMMENT IS STALE/WRONG
configs_per_param = args.test_values + 1
total_configs = num_params * configs_per_param
```

**Note**: The code comment says "24" but uses actual PARAMETER_ORDER length (7) in practice.

---

### 5. **UNCLEAR SEPARATION** (Section: Architecture)

**Error**: Document mixes win rate and accuracy parameters without clear separation

**Actual Structure**:

**Win Rate Simulation** (`run_win_rate_simulation.py`):
- Optimizes: **DRAFT STRATEGY** parameters (7 total)
- Goal: Maximize league win rate
- Parameters:
  1. DRAFT_NORMALIZATION_MAX_SCALE
  2. SAME_POS_BYE_WEIGHT
  3. DIFF_POS_BYE_WEIGHT
  4. PRIMARY_BONUS
  5. SECONDARY_BONUS
  6. ADP_SCORING_WEIGHT
  7. PLAYER_RATING_SCORING_WEIGHT

**Accuracy Simulation** (`run_accuracy_simulation.py`):
- Optimizes: **PREDICTION** parameters (16 total)
- Goal: Minimize Mean Absolute Error (MAE)
- Parameters: NORMALIZATION_MAX_SCALE, TEAM_QUALITY_*, PERFORMANCE_*, MATCHUP_*, TEMPERATURE_*, WIND_*, LOCATION_*

**These are SEPARATE simulations with DIFFERENT purposes.**

---

### 6. **INCORRECT DEFAULT VALUES** (Need Verification)

**Document Claims**:
- DEFAULT_SIMS = 5 ✓ **CORRECT**
- DEFAULT_WORKERS = 8 ✓ **CORRECT**
- DEFAULT_TEST_VALUES = 5 ✓ **CORRECT** (from line 45 in run_win_rate_simulation.py)

---

### 7. **TIMING ESTIMATES MAY BE WRONG** (Section: Performance Characteristics)

**Document States**:
- Iterative mode: ~11.2 minutes (for 168 configs)

**Needs Recalculation**:
- Actual configs: 42 (not 168)
- 42 × 4s per config = 168 seconds = **2.8 minutes** (not 11.2 minutes)

**Verification Needed**: Run actual timing tests

---

## MINOR ERRORS / CLARIFICATIONS NEEDED

### 8. **Team Distribution** ✓ **VERIFIED CORRECT**

**Document States**:
- 1 DraftHelperTeam
- 2 adp_aggressive
- 2 projected_points_aggressive
- 2 adp_with_draft_order
- 3 projected_points_with_draft_order

**Source**: `SimulatedLeague.py` lines 77-83:
```python
TEAM_STRATEGIES = {
    'draft_helper': 1,
    'adp_aggressive': 2,
    'projected_points_aggressive': 2,
    'adp_with_draft_order': 2,
    'projected_points_with_draft_order': 3
}
```

✓ **CORRECT**

---

### 9. **Data Structure** (Needs Verification)

**Document describes**:
```
simulation/sim_data/
├─ 2021/
│   └─ weeks/
│       └─ week_01/
│           ├─ players_projected.json
│           ├─ players_actual.json
│           └─ teams_week_01.csv
```

**Actual structure** (from SimulatedLeague.py lines 230-232):
```
simulation/sim_data/
├─ 2021/
│   └─ weeks/
│       └─ week_01/
│           ├─ qb_data.json      ← 6 position files
│           ├─ rb_data.json
│           ├─ wr_data.json
│           ├─ te_data.json
│           ├─ k_data.json
│           └─ dst_data.json
```

**Status**: **INCORRECT** - Uses position-specific JSON files, not players_projected/actual

---

### 10. **Missing Information**

**Document should include**:
- Clarification that THIS document is about **WIN RATE simulation only**
- Accuracy simulation has its own separate documentation
- The relationship between the two simulations (win rate = draft strategy, accuracy = prediction)
- Week-by-week horizon optimization for win rate params (document mentions it but not clearly)

---

## SUMMARY OF CORRECTIONS NEEDED

| Section | Error Type | Severity |
|---------|-----------|----------|
| Entry Point | Wrong script name | **CRITICAL** |
| Parameter Count | Wrong count (24 vs 7) | **CRITICAL** |
| Full Mode Formula | Wrong exponent (24 vs 6) | **CRITICAL** |
| Iterative Calculations | Wrong total (168 vs 42) | **CRITICAL** |
| Architecture | Mixed win rate & accuracy | **HIGH** |
| Data Structure | Wrong file names | **HIGH** |
| Timing Estimates | Based on wrong config count | **MEDIUM** |

---

## NEXT STEPS

1. Create corrected version of WIN_RATE_SIMULATION_FLOW.md
2. Clearly separate win rate vs accuracy concerns
3. Verify all code references against actual source
4. Add disclaimers about what this document covers
5. Consider creating separate ACCURACY_SIMULATION_FLOW.md document
6. Update all command examples
7. Recalculate all performance estimates

---

**Verification Date**: 2026-01-05
**Verified Against**: Latest main branch code
**Status**: **CORRECTIONS REQUIRED BEFORE DOCUMENT IS USABLE**
