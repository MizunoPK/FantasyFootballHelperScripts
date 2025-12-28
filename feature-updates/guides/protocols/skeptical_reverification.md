# Skeptical Re-verification Protocol

**Purpose:** Challenge all assumptions and re-validate all claims with fresh codebase research.

**Related:** [README.md](README.md) - Protocol index

---


> *Rationale: Assumptions are the root cause of most bugs. "I assumed this method existed" and "I assumed this attribute was available" cause runtime crashes. This protocol forces you to verify, not assume.*

**Execute during:** Iterations 6, 13, and 22

**Steps:**

1. **Question Everything** - Assume nothing written so far is accurate:
   - Is the file path I documented actually correct? (Verify with Read/Glob)
   - Does that method I referenced actually exist? (Verify with Grep)
   - Is that pattern I identified actually used? (Re-search codebase)
   - Are my assumptions about data flow correct? (Re-trace through code)
   - Did I misunderstand the original requirement? (Re-read specification)

2. **Fresh Codebase Validation:**
   - Re-search for ALL file paths mentioned in TODO
   - Re-verify ALL method names and line numbers
   - Re-validate ALL code patterns claimed
   - Re-check ALL dependencies and imports

3. **Requirement Re-Verification:**
   - Re-read original specification word-by-word
   - Re-read user question answers (if applicable)
   - List requirements again from scratch
   - Compare new list against TODO
   - Identify discrepancies or misinterpretations

4. **Mirror Pattern Verification** (if spec says "mirror X" or "similar to X"):
   - Read ENTIRE file X from start to finish
   - Document ALL organizational patterns:
     - Constants at top of file (what constants, what order)
     - Where key variables are defined (runner script vs manager class)
     - Import organization
     - File structure (docstring, constants, functions, main block)
   - Compare your TODO against these patterns
   - If patterns don't match, update TODO to match

   **Why this matters:** "Mirror run_simulation.py" was interpreted as "copy the CLI args and mode handling" but missed:
   - `DEFAULT_MODE`, `DEFAULT_SIMS`, `DEFAULT_WORKERS` constants at top
   - `PARAMETER_ORDER` defined in runner script, not manager class

   These omissions required post-implementation fixes.

5. **Method Call Parameter Verification** (if feature optimizes or uses configurable parameters):
   - For each parameter the feature optimizes/uses:
     - Identify the method that applies this parameter
     - Check if that method has an enable flag for the parameter
     - Verify the method call has that flag set to True
   - Compare method call signature to similar/consuming features:
     - If feature "optimizes weekly scoring", compare to StarterHelperModeManager
     - If feature "optimizes draft scoring", compare to AddToRosterModeManager
   - Add test that parameter changes actually affect output

   **Why this matters:** The accuracy simulation optimized 17 parameters but called `score_player(player)` with all default flags. Defaults had `temperature=False`, `wind=False`, `matchup=False`, so 11 of 17 parameters had **no effect** - they were optimized but never used!

   **Verification test to add:**
   ```python
   def test_parameter_changes_affect_output(self):
       result1 = calculate_with_config(param_value=10)
       result2 = calculate_with_config(param_value=100)
       assert result1 != result2, "Parameter change had no effect - check flags"
   ```

6. **Document Results:**
   - Add "Skeptical Re-Verification Results" section to TODO
   - List what was verified as correct
   - List what was found to be incorrect and corrected
   - Document confidence level in current plan

7. **Confidence Calibration:**
   Use these criteria to set your confidence level:

   | Level | Criteria |
   |-------|----------|
   | **High** | All file paths verified to exist, all method signatures confirmed, no assumptions remaining, similar patterns found in codebase |
   | **Medium** | Most paths verified, some method signatures assumed based on patterns, 1-2 minor assumptions remaining |
   | **Low** | Multiple paths unverified, method signatures based on documentation only, significant assumptions remaining |

   **Detailed Confidence Criteria:**

   | Area | High Confidence | Medium Confidence | Low Confidence |
   |------|-----------------|-------------------|----------------|
   | **File Paths** | All verified with Read/Glob | Most verified, 1-2 assumed | Multiple unverified |
   | **Method Signatures** | All confirmed from source | Most confirmed, some from docs | Based on docs/patterns only |
   | **Integration Points** | All callers identified and verified | Most callers known | Callers unclear |
   | **Data Flow** | Complete trace from entry to output | Most steps traced | Significant gaps |
   | **Similar Patterns** | Found and referenced in codebase | Found similar, not exact | No similar patterns |
   | **Edge Cases** | All identified and documented | Most identified | Several unknown |

   **Example Evidence for High Confidence:**
   ```
   Confidence: HIGH
   - File path: simulation/shared/ConfigGenerator.py (verified with Read)
   - Method: generate_iterative_combinations() at line 145 (read actual definition)
   - Caller: SimulationManager.run_iterative_optimization() at line 261 (verified with Grep)
   - Similar pattern: SimulationManager already calls generate_full_combinations() same way
   ```

   **Example Evidence for Medium Confidence:**
   ```
   Confidence: MEDIUM
   - File path: simulation/shared/ConfigGenerator.py (verified)
   - Method: generate_iterative_combinations() (signature inferred from docstring)
   - Caller: SimulationManager (likely run_iterative_optimization, need to verify)
   - Assumption: Return type matches existing generate_* methods
   ```

   **Example Evidence for Low Confidence:**
   ```
   Confidence: LOW - DO NOT PROCEED
   - File path: Assumed to be in simulation/ folder
   - Method: Described in architecture docs but not found in code
   - Caller: Unknown - need to investigate where this fits
   - Multiple assumptions about parameter types and return values
   ```

   **Confidence Level Actions:**
   - **High:** Proceed to next iteration
   - **Medium:** Note assumptions explicitly, proceed cautiously, plan to verify during implementation
   - **Low:** **STOP** - Resolve uncertainties before proceeding. Low confidence at iteration 24 = DO NOT implement.

   **If confidence is Low:** Do NOT proceed to implementation. Return to verification and resolve uncertainties first.

---

