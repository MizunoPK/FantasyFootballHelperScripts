# ACCURACY_SIMULATION_FLOW.md - Critical Corrections Required

## Verification Status: **FAILED - Major Errors and Omissions Found**

This document lists all errors found after verification against actual source code.

---

## CRITICAL ERRORS AND OMISSIONS

### 1. **INFINITE LOOP - NOT DOCUMENTED** (run_accuracy_simulation.py)

**MISSING FROM DOCUMENTATION**: The simulation runs in an **infinite loop**!

**Source**: `run_accuracy_simulation.py` lines 316-318:
```python
if __name__ == "__main__":
    while True:
        main()
```

**What This Means**:
- The simulation **NEVER STOPS** automatically
- After each full tournament optimization (all 16 parameters), it:
  1. Uses the just-created `accuracy_optimal_*` folder as the new baseline
  2. Starts optimization again from parameter 1
  3. Repeats forever until manually interrupted (Ctrl+C)
- This is for **continuous improvement** - each iteration refines from the previous optimal

**Impact**: CRITICAL OMISSION - completely changes user expectations
- Users expect: "Run once and done"
- Reality: "Runs forever, improving continuously"

**Document Should Include**:
- Section on "Infinite Loop Behavior"
- How to stop gracefully (Ctrl+C)
- What happens to intermediate results
- Use case for continuous optimization

---

### 2. **PRIMARY METRIC IS WRONG** (Throughout Document)

**Error**: Document states "MAE (Mean Absolute Error)" is the primary metric
**Actual**: **Pairwise Accuracy** is the primary metric, MAE is fallback only

**Source**: `AccuracyResultsManager.py` lines 115-146:
```python
def is_better_than(self, other: 'AccuracyConfigPerformance') -> bool:
    # Use ranking metrics if available (Q12: pairwise_accuracy is primary)
    if self.overall_metrics and other.overall_metrics:
        return self.overall_metrics.pairwise_accuracy > other.overall_metrics.pairwise_accuracy

    # Fallback to MAE for backward compatibility (Q25)
    return self.mae < other.mae
```

**Hierarchy of Metrics**:
1. **Primary**: Pairwise Accuracy (% of player pairs correctly ranked) - HIGHER is better
2. **Fallback**: MAE (Mean Absolute Error) - LOWER is better

**Locations to Fix**:
- Overview section: "Key Metrics"
- AccuracyCalculator section
- All mentions of "minimize MAE" should be "maximize pairwise accuracy (or minimize MAE as fallback)"
- Tournament optimization explanation

**Correct Description**:
- Primary goal: Maximize pairwise accuracy (correct ranking of player pairs)
- MAE calculated for diagnostics and backward compatibility
- When ranking metrics unavailable, falls back to MAE comparison

---

### 3. **CLI OUTPUT BUG NOT MENTIONED** (run_accuracy_simulation.py)

**Issue**: The CLI prints misleading information to users

**Source**: `run_accuracy_simulation.py` line 268:
```python
total_configs = (args.test_values + 1) ** 6  # 46,656 with default test_values=5
print(f"Configs per parameter: {total_configs:,}")
```

**Problem**:
- Prints: "Configs per parameter: 46,656" (WRONG formula from full mode)
- Actual: **24 configs per parameter** (4 horizons × 6 test values)

**Verification**: `AccuracySimulationManager.py` line 762:
```python
total_configs = sum(len(vals) for vals in test_values_dict.values())
# For accuracy sim with all week-specific params: 4 * 6 = 24
```

**Impact**: User sees "46,656 configs/param" but only 24 are actually tested
- Total configs: 16 params × 24 = **384** (not 16 × 46,656)
- This is a **BUG in the CLI output**, not an error in my documentation

**Document Should Note**:
- Known issue: CLI displays incorrect formula (46,656 instead of 24)
- Actual behavior: 24 configs per parameter (verified)
- Total execution: 384 configs across all 16 parameters

---

### 4. **RANKING METRICS NOT FULLY EXPLAINED** (Throughout)

**Omission**: Document mentions ranking metrics but doesn't explain:
- What they are
- How they're calculated
- Why pairwise accuracy is primary
- When MAE fallback is used

**Ranking Metrics Calculated** (`AccuracyResultsManager.py` lines 38-54):
```python
@dataclass
class RankingMetrics:
    pairwise_accuracy: float      # % of pairwise comparisons correct (0.0-1.0)
    top_5_accuracy: float          # % overlap in top-5 predictions (0.0-1.0)
    top_10_accuracy: float         # % overlap in top-10 predictions (0.0-1.0)
    top_20_accuracy: float         # % overlap in top-20 predictions (0.0-1.0)
    spearman_correlation: float    # Rank correlation coefficient (-1.0 to +1.0)
```

**Document Should Add**:
- Dedicated "Ranking Metrics" section
- Explanation of each metric
- Why pairwise accuracy is most important (correctly ranks player pairs)
- How Spearman correlation is calculated (Fisher z-transform for aggregation)
- Threshold warnings (Q34, Q35):
  - Pairwise accuracy < 65% → Warning
  - Top-10 accuracy < 70% → Warning

---

### 5. **EXECUTION MODE NAME CONFUSION** (Section: Entry Point)

**Error**: Document calls it "Tournament Optimization" mode
**Actual**: The only mode is `run_both()` - no "mode" parameter exists

**Source**: `run_accuracy_simulation.py` lines 297-298:
```python
# Run simulation
optimal_path = manager.run_both()  # No mode parameter!
```

**Clarification Needed**:
- There is NO mode selection (unlike win rate with single/full/iterative)
- `run_both()` is the ONLY execution path
- "Tournament optimization" describes the ALGORITHM, not a mode choice

**Document Should Clarify**:
- Remove "Single Execution Mode" header (implies there are other modes)
- Title: "Execution Method: Tournament Optimization"
- Note: No mode selection needed - always runs tournament optimization

---

### 6. **DEFAULT VALUES NEED VERIFICATION** (Various Sections)

**Need to verify against code**:

From `run_accuracy_simulation.py` lines 53-68:
- ✅ DEFAULT_TEST_VALUES = 5 (6 values including baseline) - CORRECT
- ✅ DEFAULT_MAX_WORKERS = 8 - CORRECT
- ✅ DEFAULT_USE_PROCESSES = True - CORRECT
- ✅ NUM_PARAMETERS_TO_TEST = 1 - CORRECT (not used in tournament mode)

---

### 7. **WEEK OFFSET EXPLANATION INCOMPLETE** (Data Flow section)

**Document States**:
> "Projections: Use week_N folder (data 'as of' week N start)"
> "Actuals: Use week_N+1 folder (week N results available)"

**More Accurate Explanation Needed**:

Each week folder contains TWO sets of data in the JSON files:
- `projected_points[0..16]` - Projections for weeks 1-17
- `actual_points[0..16]` - Actual results for weeks 1-17

**Week Offset Logic** (`AccuracySimulationManager.py` lines 293-338):
- **For projections**: Use week_N folder → projected_points[week_N - 1]
- **For actuals**: Use week_N+1 folder → actual_points[week_N - 1]

**Why the offset?**
- Week N folder created at START of week N (before games)
- Contains: projected_points[N-1] = week N projections
- Does NOT contain: actual_points[N-1] = week N actuals (games not played yet)
- Week N+1 folder created AFTER week N games complete
- Contains: actual_points[N-1] = week N actuals (games finished)

**Document Needs**:
- Clearer explanation of array indexing
- Why week_02 folder is needed for week_01 actuals
- Code references to support explanation

---

### 8. **TIMING ESTIMATES MAY BE WRONG** (Performance section)

**Document States**: "~4 minutes for 384 configs"

**Calculation to Verify**:
```
Per-config evaluation:
- 1 config × 4 horizons = 4 evaluations
- 1 evaluation = 1 horizon × 3 seasons × weeks in range
- Weeks in range: 1-5 (5 weeks), 6-9 (4 weeks), 10-13 (4 weeks), 14-17 (4 weeks)
- Average: ~4 weeks per horizon
- 1 evaluation ≈ 4 weeks × 3 seasons × ~500 players × scoring calc
- Estimate: ~2s per evaluation
- 1 config = 4 evaluations × 2s = 8s
- With 8 workers: 8s / 7 ≈ 1.1s per config (accounting for overhead)

24 configs per parameter:
- Serial: 24 × 1.1s ≈ 26s per parameter
- With batching (8 parallel): 24 / 8 × 8s ≈ 24s per parameter

16 parameters:
- 16 × 24s = 384s ≈ 6.4 minutes
```

**Revised Estimate**: ~6-7 minutes (not 4 minutes)

**Need to verify with actual timing tests**

---

### 9. **AUTO-RESUME EXPLANATION INCOMPLETE** (Execution Flow)

**Document Mentions**: Auto-resume support
**Missing**: How it works in detail

**From** `AccuracySimulationManager.py` lines 187-291:
```python
def _detect_resume_state(self) -> Tuple[bool, int, Optional[Path]]:
    """
    Detect if optimization should resume from a previous run.

    Scans for accuracy_intermediate_*/ folders.

    Returns:
        (should_resume, start_idx, last_config_path)
    """
```

**Resume Logic**:
1. Scans for `accuracy_intermediate_*` folders
2. Parses folder names to extract parameter index
3. Finds highest completed parameter index
4. If all params complete: cleans up and starts fresh
5. If partially complete: loads intermediate results and resumes from next param

**Document Should Add**:
- Detailed resume logic explanation
- Folder naming pattern: `accuracy_intermediate_{idx}_{param_name}/`
- What happens on interrupt (saves intermediate)
- How to force fresh start (delete intermediate folders)

---

### 10. **CONFIGURATION COUNT DISCREPANCY** (CLI Output vs Actual)

**Summary of Config Counts**:

| What | Formula | Value |
|------|---------|-------|
| **CLI Displays** (WRONG) | `(test_values+1)^6` | 46,656 |
| **Actual Per Param** | `4 horizons × (test_values+1)` | 24 |
| **Total Configs** | `16 params × 24` | 384 ✓ |
| **Total Evaluations** | `384 configs × 4 horizons` | 1,536 ✓ |

**My documentation correctly states 384 total configs**, but should note the CLI bug.

---

## MINOR ISSUES

### 11. **Section Headers Could Be Clearer**

**"Entry Point and Execution Mode"** suggests multiple modes exist
- Change to: "Entry Point and Tournament Optimization"

**"Single Execution Mode: Tournament Optimization"** is confusing
- Change to: "Tournament Optimization Algorithm"

### 12. **Formula in Run File Needs Explanation**

Line 268 in `run_accuracy_simulation.py`:
```python
total_configs = (args.test_values + 1) ** 6
```

This formula is:
- Copied from win-rate simulation
- Represents full-mode grid search (6 parameters varied simultaneously)
- **NOT APPLICABLE** to accuracy simulation (varies 1 param at a time with horizon-specific values)
- Should be: `4 * (args.test_values + 1)` for week-specific params
- Or better: Calculate dynamically from actual test_values_dict

---

## SUMMARY OF CORRECTIONS NEEDED

| Issue | Severity | Type |
|-------|----------|------|
| Infinite loop not documented | **CRITICAL** | Omission |
| Wrong primary metric (MAE vs pairwise) | **CRITICAL** | Error |
| CLI output bug not mentioned | **HIGH** | Omission |
| Ranking metrics under-explained | **HIGH** | Incomplete |
| "Mode" terminology misleading | **MEDIUM** | Clarity |
| Week offset explanation incomplete | **MEDIUM** | Incomplete |
| Timing estimates unverified | **MEDIUM** | Accuracy |
| Auto-resume logic under-explained | **LOW** | Incomplete |

---

## NEXT STEPS

1. Add "Infinite Loop Behavior" section
2. Correct all "MAE is primary" statements to "Pairwise accuracy is primary, MAE is fallback"
3. Add comprehensive "Ranking Metrics" section
4. Note CLI output bug (46,656 displayed but 24 actual)
5. Clarify "Tournament Optimization" is algorithm, not a mode choice
6. Expand week offset explanation with array indexing details
7. Verify and update timing estimates
8. Add detailed auto-resume section

---

**Verification Date**: 2026-01-05
**Verified Against**: Latest main branch code
**Status**: **CORRECTIONS REQUIRED BEFORE DOCUMENT IS USABLE**
