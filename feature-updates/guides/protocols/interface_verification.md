# Interface Verification Protocol

**Purpose:** Verify all dependency interfaces and data model attributes before writing implementation code.

**Related:** [README.md](README.md) - Protocol index

---


**Execute:** Before starting any implementation work, after iteration 24.

**Steps:**

**Step 1: List All External Dependencies**
For each class the new code will use, document:
```
| Dependency | File | Methods to Call | Verified? |
|------------|------|-----------------|-----------|
| ConfigGenerator | shared/ConfigGenerator.py | generate_iterative_combinations() | [ ] |
| ProgressTracker | shared/ProgressTracker.py | update(), complete() | [ ] |
| PlayerManager | util/PlayerManager.py | load_players(), get_player() | [ ] |
```

**Step 2: Verify Interfaces Against Source**

**CRITICAL: Copy-Paste Requirement**

DO NOT verify interfaces from memory or documentation. ALWAYS:

1. **Open Actual Source File**
   - Navigate to the module containing the interface
   - Find the exact class/function definition
   - Scroll to the method you're calling

2. **Copy Exact Signature**
   ```python
   # EXAMPLE: Verifying DataFileManager.save_json_data()
   # From utils/data_file_manager.py line 365:
   def save_json_data(self, data: Any, prefix: str,
                      create_latest: bool = True, **json_kwargs) -> Tuple[Path, Optional[Path]]:
   ```

3. **Compare to Your Usage**
   ```python
   # YOUR CODE:
   file_path, _ = manager.save_json_data(output_data, prefix, create_latest=False)
   #                                      ^^^^^^^^^  ^^^^^^
   #                                      1st param  2nd param

   # SIGNATURE:
   def save_json_data(self, data: Any, prefix: str, ...)
   #                        ^^^^^^^^^  ^^^^^^^^^^^
   #                        1st param  2nd param

   # ✅ MATCH: output_data is data, prefix is prefix
   ```

4. **Check Return Type**
   - Signature returns: `Tuple[Path, Optional[Path]]`
   - Your code expects: tuple unpacking with 2 elements
   - ✅ Compatible

5. **Verify method signatures match expectations:**
   ```
   Expected: generate_configs_for_parameter(param_idx)
   Actual:   generate_iterative_combinations(param_name, base_config)
   MISMATCH! → Update expectations to match actual
   ```

6. **Check required vs optional parameters**

7. **Look for existing usage patterns:** `grep -r "dependency_name\." .`

**Red Flags (DO NOT PROCEED if any are true):**
- [ ] Parameter order doesn't match signature
- [ ] Parameter types incompatible
- [ ] Return type incompatible
- [ ] Required parameters missing
- [ ] Method doesn't exist in source

**Why This Matters:**
Bug example from real feature: Called `save_json_data(prefix, data)` instead of `save_json_data(data, prefix)` because parameter order was assumed from memory. Unit tests mocked the dependency, so incorrect call succeeded in tests but failed in production.

**Step 3: Verify Data Model Attributes**
For each data model (dataclass, domain object) you'll access:
```
| Model | File | Attributes Needed | Exists? | Semantics |
|-------|------|-------------------|---------|-----------|
| FantasyPlayer | util/FantasyPlayer.py | actual_points | [ ] | Total actual season points |
| FantasyPlayer | util/FantasyPlayer.py | week_1_points | [x] | Week 1 actual points |
```

1. Read the actual class definition
2. List all attributes you plan to use
3. Verify each attribute exists in the definition
4. Check attribute semantics (e.g., does `fantasy_points` mean projected or actual?)

**Step 4: Document Interface Contracts**
Create a summary of verified interfaces:
```markdown
## Interface Contracts (Verified)

### ConfigGenerator
- Method: `generate_iterative_combinations(param_name: str, base_config: dict) -> Iterator[dict]`
- Source: simulation/shared/ConfigGenerator.py:145
- Existing usage: SimulationManager.py:180

### FantasyPlayer
- Attribute: `week_N_points` (N=1-17) - actual points for week N
- Attribute: `fantasy_points` - projected total points
- Note: NO `actual_points` attribute - must sum week_N_points
- Source: league_helper/util/FantasyPlayer.py:15
```

**Interface Verification Checklist:**
```
□ All external dependencies listed
□ Each dependency's methods verified against source code
□ Method signatures COPY-PASTED from source (not verified from memory)
□ Parameter order verified by side-by-side comparison
□ Parameter names and types confirmed
□ Return values documented
□ Data model attributes verified to exist
□ Attribute semantics understood (not assumed)
□ Interface contracts documented in TODO file
□ Quick E2E validation planned (minimal script run to verify interfaces)
```

**Step 5: Plan Quick E2E Validation**
Before implementation, plan a minimal E2E test to validate interfaces:
1. Identify the simplest possible E2E path through the new code
2. Plan to run this BEFORE writing all implementation code
3. This catches interface mismatches early, not after days of development

**Example:**
```
Quick E2E Plan:
1. Create minimal AccuracyCalculator with just calculate_mae()
2. Run: python -c "from accuracy import AccuracyCalculator; ac = AccuracyCalculator(); print(ac.calculate_mae([]))"
3. Expected: Should return 0.0 or raise clear error
4. If import fails: Interface mismatch detected early
```

**Output:** Interface contract documentation in TODO file, all dependencies verified, quick E2E plan documented.

---

## Post-Implementation Protocols

