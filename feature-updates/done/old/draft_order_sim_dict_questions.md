# Draft Order Simulation Dictionary - Questions

Based on comprehensive codebase research (5 verification iterations), I have several clarifying questions before implementation:

---

## Question 1: Number of Simulations Per Draft Order

**Context**: The system will test all 75 draft order strategies. More simulations = more accuracy but longer runtime.

**Estimated Runtime**:
- 5 simulations per file: ~3-5 minutes total (75 × 5 = 375 sims)
- 15 simulations per file: ~10-15 minutes total (75 × 15 = 1,125 sims)
- 50 simulations per file: ~30-45 minutes total (75 × 50 = 3,750 sims)

**Question**: How many simulations should we run per draft order strategy?

**Options**:
- **A**: 5 simulations (fast, less accurate)
- **B**: 15 simulations (balanced - RECOMMENDED based on run_simulation.py default)
- **C**: 50 simulations (slow, more accurate)
- **D**: Custom number (please specify)

**Recommendation**: Option B (15 simulations) - provides good balance between accuracy and runtime, matches the system's default for parameter optimization.

---

## Question 2: Output File Format

**Context**: The original requirement specifies `{"1": 70.2, "2": 80.1}` but we could include more information for analysis.

**Question**: Should the output JSON include additional metadata?

**Option A - Simple Format (matches requirement exactly)**:
```json
{
  "1": 70.2,
  "2": 80.1,
  ...
}
```

**Option B - Format with Metadata (more informative)**:
```json
{
  "metadata": {
    "timestamp": "2025-11-24 12:34:56",
    "num_simulations_per_file": 15,
    "total_files_tested": 75,
    "baseline_config": "simulation/simulation_configs/optimal_20251124_120000.json"
  },
  "results": {
    "1": 70.2,
    "2": 80.1,
    ...
  }
}
```

**Recommendation**: Option B - Metadata is helpful for tracking which baseline config was used and when the test was run. Easy to extract just the results if needed.

---

## Question 3: Strategy Names in Output

**Context**: Draft order files have names like "2_zero_rb.json" (Zero RB strategy) but the requirement shows numeric keys.

**Question**: Should we include strategy names in the output?

**Option A - Numbers Only (matches requirement)**:
```json
{
  "1": 70.2,
  "2": 80.1
}
```

**Option B - Include Strategy Names**:
```json
{
  "1": 70.2,
  "2_zero_rb": 80.1,
  "3_hero_rb": 75.3
}
```

**Option C - Separate Mapping**:
```json
{
  "results": {"1": 70.2, "2": 80.1},
  "strategy_names": {"1": "Baseline", "2": "Zero RB", "3": "Hero RB"}
}
```

**Recommendation**: Option A - Keep it simple as specified in the requirement. Strategy names can be looked up from the files if needed.

---

## Question 4: Progress Logging Frequency

**Context**: The script will run for 10-15 minutes. Users should see progress updates.

**Question**: How often should progress be logged to console?

**Options**:
- **A**: Every file (75 updates) - verbose
- **B**: Every 5 files (15 updates) - RECOMMENDED
- **C**: Every 10 files (7-8 updates) - minimal
- **D**: Only start/end messages - very minimal

**Recommendation**: Option B - Every 5 files provides good feedback without spamming the console.

---

## Question 5: Error Handling Strategy

**Context**: If a simulation fails (e.g., corrupted file, out of memory), we need to decide how to proceed.

**Question**: If simulations fail for a specific draft order file, what should we do?

**Options**:
- **A**: Retry once, then skip if it fails again (RECOMMENDED)
- **B**: Skip immediately and continue to next file
- **C**: Abort entire run and report error
- **D**: Retry multiple times (specify how many)

**Recommendation**: Option B - Skip and continue. Log the error clearly so the user knows which files failed. Don't block the entire run on one bad file.

---

## Question 6: Output Directory Location

**Context**: Need to decide where to save the results JSON file.

**Question**: Where should the results file be saved?

**Options**:
- **A**: `simulation/draft_order_results/` (new directory) - RECOMMENDED
- **B**: `simulation/simulation_configs/` (with other configs)
- **C**: Project root directory
- **D**: Custom location (please specify)

**Recommendation**: Option A - Create dedicated directory for draft order analysis results, keeps things organized.

---

## Summary of Recommendations

Based on codebase patterns and best practices, I recommend:
1. **15 simulations per draft order** (Question 1, Option B)
2. **Include metadata in output** (Question 2, Option B)
3. **Numbers only in results** (Question 3, Option A)
4. **Log every 5 files** (Question 4, Option B)
5. **Skip failed files** (Question 5, Option B)
6. **Save to `simulation/draft_order_results/`** (Question 6, Option A)

Please confirm these choices or specify different preferences!
