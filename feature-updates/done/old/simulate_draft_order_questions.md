# Questions: Add DRAFT_ORDER as Simulation Parameter

## Questions for User

### 1. Parameter Position in PARAMETER_ORDER

**Question**: Where should DRAFT_ORDER_FILE be placed in the optimization order?

**Options**:
- **A) After SECONDARY_BONUS (position 6)** - Groups all draft-related parameters together
- **B) At the end of PARAMETER_ORDER** - Tests it last after all other optimizations
- **C) At the beginning** - Optimizes it first

**Recommendation**: Option A - keeps draft-related parameters (PRIMARY_BONUS, SECONDARY_BONUS, DRAFT_ORDER_FILE) together for logical grouping.

---

### 2. Value Generation Strategy

**Question**: How should test values be generated for DRAFT_ORDER_FILE?

**Options**:
- **A) Random sample** - Select `num_test_values + 1` random integers from 1-30 (e.g., [5, 12, 23, 3, 18, 27] for 6 values)
- **B) Include optimal + random** - Keep current best file number + random selection
- **C) Test all 30** - Always test all 30 strategies regardless of `num_test_values`

**Recommendation**: Option B - consistent with how other parameters work (baseline optimal + random variations). This balances thoroughness with efficiency.

---

### 3. Optimal Value Tracking

**Question**: What should be the default/baseline DRAFT_ORDER_FILE value?

**Options**:
- **A) File 1** - The original strategy
- **B) User-configurable** - Add to baseline config file
- **C) Random starting point** - Let simulation discover optimal

Answer: Use whatever is in the config file that is used as the baseline for the simulation. Whatever optimal/intermediate file is used as the base should contain a DRAFT_ORDER value that should be used as the baseline

---

### 4. Config Metadata Storage

**Question**: How should we track which draft order file was used in a config?

**Options**:
- **A) Add DRAFT_ORDER_FILE field** - Store file number as integer (e.g., `"DRAFT_ORDER_FILE": 5`)
- **B) Add DRAFT_ORDER_SOURCE field** - Store filename (e.g., `"DRAFT_ORDER_SOURCE": "5_wr_first.json"`)
- **C) Both** - Store both file number and filename for clarity

**Recommendation**: Option A - simpler, and the file number can be mapped to filename when needed for reporting.

---

### 5. Error Handling for Missing Files

**Question**: What should happen if a draft order file is not found?

**Options**:
- **A) Raise error** - Fail fast if file doesn't exist
- **B) Skip and log warning** - Skip this test value and continue
- **C) Fall back to default** - Use file 1 as fallback

**Recommendation**: Option A - fail fast to catch configuration issues early. Missing files indicate a setup problem that should be fixed.

---

### 6. File Number Naming Flexibility

**Question**: The files are named with patterns like `1.json`, `2_zero_rb.json`, etc. How strict should matching be?

**Options**:
- **A) Exact prefix match** - Use glob pattern `f"{num}_*.json"` or `f"{num}.json"`
- **B) Any file starting with number** - More flexible but potentially ambiguous
- **C) Require exact naming convention** - Only `{num}.json` allowed (would require renaming files)

**Recommendation**: Option A - use glob pattern `f"{num}_*.json"` with fallback to `f"{num}.json"` for file 1.

---

### 7. Full Grid Search Support

**Question**: Should DRAFT_ORDER_FILE also be optimized in full grid search mode (run_full_optimization)?

**Options**:
- **A) Yes - include in grid search** - Adds significant combinations (30x more configs)
- **B) No - iterative only** - Keep grid search faster, optimize only in iterative mode

**Recommendation**: Option B - full grid search already generates many combinations. DRAFT_ORDER is better suited for iterative optimization due to its discrete nature.

---

## User Answers

*(Please provide your answers below)*

1. Parameter Position:
2. Value Generation Strategy:
3. Optimal Value Tracking:
4. Config Metadata Storage:
5. Error Handling:
6. File Naming:
7. Full Grid Search:

---

## Additional Comments

*(Add any additional requirements or clarifications here)*

