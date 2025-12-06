## OBJECTIVE PLANNING WORKFLOW

**🚨 MANDATORY: 3 VERIFICATION ROUNDS BEFORE DEVELOPMENT** - The agent must complete 3 full rounds of verification iterations before beginning any implementation work.

Before starting changes, follow this mandatory workflow:

### **STEP 1: Create Draft TODO File**

Create an initial TODO file that maps out all the tasks needed to accomplish the objective. This draft is based solely on the original specification file (`updates/{objective_name}.txt`). The TODO file should be named `updates/todo-files/{objective_name}_todo.md`.

The draft TODO should include:
- High-level phases and tasks
- Anticipated file modifications
- Testing requirements
- Documentation updates

As you complete tasks, keep the file updated with your progress in case a new Claude agent in a new session needs to finish the work. Ensure this TODO file has everything it needs to maintain consistent work - including a note about keeping the file up to date on progress made.

### **STEP 2: First Verification Round (7 Iterations)**

Execute the TODO FILE VERIFICATION AND REFINEMENT PROTOCOL (detailed below) with **7 complete iterations** to research the codebase, identify patterns, and refine the draft TODO file. This happens BEFORE creating the questions file.

**Iteration Breakdown**:
- **Iterations 1-3**: Standard verification (research, cross-reference, refine)
- **Iteration 4**: Continue refinement with deeper technical details + **ALGORITHM TRACEABILITY MATRIX**
- **Iteration 5**: **END-TO-END DATA FLOW VERIFICATION** - For each requirement, trace from entry point to output. Identify what calls each new method. Document integration points.
- **Iteration 6**: **SKEPTICAL RE-VERIFICATION** - Assume nothing written so far is accurate. Re-verify ALL claims, assumptions, file paths, method names, patterns, and implementation strategies from scratch. Question everything and validate with fresh codebase research.
- **Iteration 7**: **INTEGRATION GAP CHECK** - Review all new methods/classes planned. For each one, verify the TODO includes a task to modify the CALLER. If a new method has no caller modification task, add one.

### **STEP 3: Create Questions File**

After completing the first 7 verification iterations (including skeptical re-verification and integration gap check), create a questions file based on ambiguities, implementation choices, and user preference decisions discovered during codebase research. The questions file should be named `updates/{objective_name}_questions.md`.

This file should contain:
- Clarifying questions about requirements
- Implementation approach options (with recommendations based on codebase research)
- User preference questions
- Questions that arose during the first verification round

**IMPORTANT**: Wait for the user to answer these questions before proceeding to Step 4.

---

## QUESTIONS FILE TEMPLATE

The questions file (`updates/{objective_name}_questions.md`) must follow this structured format for EVERY question:

```markdown
# {Objective Name} - Questions

## Question 1: {Brief Title}

### Context
{Explain the background and why this question is being asked. Include relevant findings from codebase research, constraints discovered, or ambiguities in the original specification that necessitate clarification.}

### Question
{State the specific question or problem that needs to be resolved. Be clear and direct about what decision needs to be made.}

### Options

**Option A: {Option Title}**
- Description: {What this option entails}
- Pros: {Benefits of this approach}
- Cons: {Drawbacks or risks}

**Option B: {Option Title}**
- Description: {What this option entails}
- Pros: {Benefits of this approach}
- Cons: {Drawbacks or risks}

**Option C: {Option Title}** (if applicable)
- Description: {What this option entails}
- Pros: {Benefits of this approach}
- Cons: {Drawbacks or risks}

### Agent Recommendation
{State the agent's recommended option and provide clear reasoning for why this option is preferred based on codebase research, existing patterns, and technical considerations.}

### User Answer
> **Selected Option:**
>
> **Additional Notes/Elaboration:**
>
>

---

## Question 2: {Brief Title}

{Repeat the same structure for each additional question}
```

### TEMPLATE REQUIREMENTS:

1. **Context Section**: Must explain WHY this question arose - reference specific findings from codebase research, conflicts in requirements, or gaps in the specification
2. **Question Section**: Must be a clear, answerable question - not vague or open-ended
3. **Options Section**: Must provide at least 2 concrete options with pros/cons for each
4. **Agent Recommendation**: Must state a clear preference with technical justification
5. **User Answer Section**: Must include dedicated, clearly marked space for:
   - The selected option
   - Room for elaboration or additional context from the user

### EXAMPLE:

```markdown
## Question 1: Configuration Storage Format

### Context
During codebase research, I found that the project currently stores configuration in JSON files (`data/configs/*.json`). The new feature requires storing additional nested configuration data. The existing JSON structure uses flat key-value pairs, which may not accommodate the hierarchical data cleanly. I also noticed the simulation module uses a similar pattern in `sim_data/` that could be referenced.

### Question
What format should be used for storing the new hierarchical configuration data?

### Options

**Option A: Extend Existing JSON Structure**
- Description: Add nested objects to the existing JSON files
- Pros: Maintains consistency with current approach, no new dependencies
- Cons: May make files harder to read, requires updating all JSON parsers

**Option B: Create Separate YAML Files**
- Description: Use YAML format for new hierarchical configs
- Pros: Better readability for nested data, supports comments
- Cons: Introduces new dependency, mixed config formats in project

**Option C: Use Python Dataclasses with JSON Serialization**
- Description: Define config structure in Python, serialize to JSON
- Pros: Type safety, IDE support, validation built-in
- Cons: More initial setup, requires migration of existing configs

### Agent Recommendation
I recommend **Option A: Extend Existing JSON Structure** because the codebase already has established patterns for JSON handling in `ConfigManager.py` (lines 45-89), and the additional complexity of nested objects is manageable. This maintains consistency and avoids introducing new dependencies.

### User Answer
> **Selected Option:**
>
> **Additional Notes/Elaboration:**
>
>
```

### ENFORCEMENT:
- **ALL questions must follow this template** - incomplete questions are not acceptable
- **Context is mandatory** - questions without context lack the information needed for informed decisions
- **Options are mandatory** - never present a question without proposed solutions
- **Recommendations are mandatory** - the agent must provide informed guidance
- **User answer space is mandatory** - must be clearly marked and easy to fill in

### **STEP 4: Update TODO with Question Answers**

After receiving user answers, update the TODO file to reflect:
- User's chosen implementation approaches
- Clarified requirements from answers
- Adjusted task priorities based on answers
- Any new tasks revealed by the answers

### **STEP 5: Second Verification Round (9 Iterations)**

Execute the TODO FILE VERIFICATION AND REFINEMENT PROTOCOL again with **9 additional complete iterations** to:
- Validate that question answers are fully integrated
- Research any new patterns needed based on answers
- Refine implementation details
- Finalize task order and dependencies
- Verify end-to-end integration

**Iteration Breakdown**:
- **Iterations 8-10**: Verification with user answers integrated
- **Iteration 11**: Continue refinement with implementation-specific details + **ALGORITHM TRACEABILITY MATRIX** update
- **Iteration 12**: **END-TO-END DATA FLOW VERIFICATION** - Re-trace from entry point to output for each requirement with user answers integrated. Update integration points based on chosen approaches.
- **Iteration 13**: **SKEPTICAL RE-VERIFICATION** - Again, assume nothing is accurate. Re-verify ALL claims, especially those based on user answers. Validate that answers are correctly interpreted and integrated. Fresh codebase research required.
- **Iteration 14**: **INTEGRATION GAP CHECK** - Final review of all new methods/classes. For EACH new component, document: (1) what file it's in, (2) what existing code will call it, (3) what modification is needed in the caller. Flag any orphan code.
- **Iterations 15-16**: Final refinement, preparation for implementation, and creation of integration verification checklist

### **STEP 6: Third Verification Round (8 Iterations) - FINAL PRE-IMPLEMENTATION CHECK**

**🚨 CRITICAL**: Execute a THIRD verification round with **8 additional iterations** focusing on algorithm correctness and implementation readiness. This round catches issues that slipped through the first two rounds.

**Iteration Breakdown**:
- **Iterations 17-18**: **FRESH EYES REVIEW** - Re-read the original spec as if seeing it for the first time. Compare every line against the TODO. Look for subtle requirements that may have been overlooked or simplified.
- **Iteration 19**: **ALGORITHM DEEP DIVE** - For EVERY algorithm, calculation, or conditional logic in the spec:
  - Quote the exact spec text
  - Document the planned implementation approach
  - Verify conditional branches match exactly (if week < X then A, else B)
  - Flag any simplifications or deviations
- **Iteration 20**: **EDGE CASE VERIFICATION** - Identify all edge cases mentioned in spec. Verify each has a corresponding implementation task and test case.
- **Iteration 21**: **TEST COVERAGE PLANNING** - For each algorithm, plan behavior tests (not just structure tests). Tests must verify the algorithm produces correct outputs, not just that code exists.
- **Iteration 22**: **SKEPTICAL RE-VERIFICATION #3** - Final skeptical pass. Assume Rounds 1 and 2 both missed something. Re-verify with adversarial mindset.
- **Iteration 23**: **INTEGRATION GAP CHECK #3** - Final integration verification. Every new component must have an identified caller.
- **Iteration 24**: **IMPLEMENTATION READINESS CHECKLIST** - Create final checklist confirming:
  - All requirements mapped to tasks
  - All algorithms documented with exact logic
  - All integration points identified
  - All test cases planned
  - Ready to begin implementation

After completing all three verification rounds (**24 total iterations**), the TODO file should be comprehensive, thoroughly validated, and ready for implementation.

**WHY 3 ROUNDS?**: Experience shows that algorithm-level bugs (like incorrect conditional logic or missing per-iteration recalculations) often slip through 2 rounds of verification. The third round with its focus on algorithm deep-dive and adversarial review catches these subtle issues before implementation begins.

---

## TODO FILE VERIFICATION AND REFINEMENT PROTOCOL

**🚨 MANDATORY** - This iterative verification protocol must be executed:
1. After creating the draft TODO file (7 iterations - including data flow verification, skeptical re-verification, and integration gap check)
2. After receiving user's answers to questions (9 more iterations - including data flow verification, skeptical re-verification, and integration gap check)

### **WHEN TO EXECUTE**:
- ✅ Immediately after generating the draft TODO file (STEP 2 - First 7 iterations)
- ✅ After updating TODO with user's question answers (STEP 5 - Second 9 iterations)
- ✅ Before beginning any implementation work

### **ITERATIVE REFINEMENT PROCESS (16 TOTAL ITERATIONS)**:

**📋 ITERATION 1: Initial Verification**

1. **Re-read ALL Source Documents**:
   - Open and carefully read the original `updates/{objective_name}.txt` file line-by-line
   - Open and carefully read the `updates/{objective_name}_questions.md` answers section (if Step 5 - second verification round)
   - Open and carefully read your TODO file `updates/todo-files/{objective_name}_todo.md`

2. **Cross-Reference Requirements**:
   - Extract EVERY requirement from the original updates file (explicit and implied)
   - Extract EVERY requirement from the question answers (if Step 5 - second verification round)
   - Compare against TODO file to verify ALL requirements are covered
   - Mark any missing requirements: ❌ MISSING FROM TODO
   - During first verification round (Step 2): Identify ambiguities to ask about in questions file

3. **Ask Clarifying Questions to Self**:
   - What specific files will need to be modified for each task?
   - What existing patterns or utilities in the codebase can be leveraged?
   - Are there any edge cases or error scenarios not covered?
   - What test files will need to be created or modified?
   - Are there any dependencies between tasks that need ordering?
   - What existing code should be examined before implementation?

4. **Research Codebase**:
   - Use Glob/Grep to find relevant existing code
   - Look for similar implementations to maintain consistency
   - Identify utility classes or helper functions to reuse
   - Find test file patterns to follow
   - Locate configuration files that may need updates

5. **Update TODO File**:
   - Add missing requirements as new tasks
   - Add specific file paths to each task
   - Add code references (e.g., "Similar to ClassName.method_name in file.py:line")
   - Add test requirements for each implementation task
   - Refine task descriptions with more technical specificity
   - Add prerequisite relationships between tasks

**📋 ITERATION 2: Deep Dive Verification**

1. **Re-read Updated TODO File**:
   - Review all changes made in Iteration 1
   - Check if new questions emerged from codebase research

2. **Ask Additional Clarifying Questions**:
   - What data structures will be passed between functions?
   - What error handling strategies should be used?
   - Are there any performance considerations?
   - What logging should be added for debugging?
   - Should any constants be extracted to configuration files?
   - What documentation needs to be updated?
   - Are there any backward compatibility concerns?

3. **Research Additional Code Patterns**:
   - Find error handling patterns used in similar code
   - Identify logging patterns and conventions
   - Check configuration file structures
   - Review existing documentation formats
   - Look for data validation patterns

4. **Update TODO File Again**:
   - Add error handling tasks
   - Add logging requirements
   - Add documentation update tasks
   - Add data validation requirements
   - Refine implementation order based on dependencies
   - Add code review checkpoints

**📋 ITERATION 3: Deep Dive Verification**

1. **Re-read ALL Documents One More Time**:
   - Original updates file
   - Question answers (if Step 5 - second verification round)
   - Fully refined TODO file (for this round)

2. **Ask Final Technical Questions**:
   - Are there any integration points with other modules not addressed?
   - What mock objects will be needed for testing?
   - Are there any circular dependency risks?
   - What happens if operations fail midway through?
   - Are all file paths absolute or properly constructed?
   - What cleanup operations are needed if errors occur?

3. **Research Integration Points**:
   - Use Grep to find all places existing code is called
   - Identify all modules that might be affected
   - Check for potential circular imports
   - Review existing test mock patterns

4. **TODO Update**:
   - Add integration testing tasks
   - Add cleanup/rollback requirements
   - Add verification steps for each phase
   - Add pre-commit validation checkpoints
   - Ensure every task has specific, actionable steps
   - Confirm task order prevents breaking the system

**📋 ITERATION 4: Enhanced Technical Detail**

1. **Implementation-Specific Research**:
   - Research exact method signatures needed
   - Identify return types and data structures
   - Find example usages of similar patterns in codebase
   - Document edge cases with code examples

2. **Performance and Optimization**:
   - Consider performance implications of approach
   - Identify potential bottlenecks
   - Research caching strategies if needed
   - Document any async/await patterns needed

3. **TODO Enhancement**:
   - Add specific code examples to tasks
   - Document exact API endpoints/parameters
   - Add performance considerations
   - Include optimization opportunities

4. **🚨 ALGORITHM TRACEABILITY MATRIX** (NEW):
   - For each calculation, formula, or algorithm in the spec:
     - Extract the EXACT logic from the spec (quote it word-for-word)
     - Document which code file/method will implement it
     - Note any conditional logic (e.g., "if week < X then A, else B")
   - Create matrix in TODO file:
     ```
     | Spec Section | Algorithm Description | Code Location | Conditional Logic |
     |--------------|----------------------|---------------|-------------------|
     | Lines 158-186 | players_projected week columns | weekly_snapshot_generator.py | week < X: historical, week >= X: current |
     | Lines 241-276 | player_rating calculation | weekly_snapshot_generator.py | week 1: draft rank, week 2+: cumulative points |
     ```
   - This matrix will be verified during implementation

**📋 ITERATION 5 (First Round) / ITERATION 12 (Second Round): END-TO-END DATA FLOW VERIFICATION**

🚨 **CRITICAL**: Trace the complete path from user action to system output.

1. **Identify Entry Points**:
   - List ALL user-facing scripts (run_*.py)
   - List ALL manager classes that orchestrate operations
   - For EACH requirement, identify which entry point triggers it

2. **Trace Data Flow**:
   - For EACH requirement, document the complete path:
     ```
     Entry: run_simulation.py
       → SimulationManager.run_iterative_optimization()
       → ParallelLeagueRunner.run_simulations_for_config()
       → ResultsManager.save_optimal_config()  ← CURRENT
       → ResultsManager.save_optimal_configs_folder()  ← REQUIRED
     ```
   - Identify WHERE in the flow the new code fits
   - Identify WHAT existing code needs to change

3. **Document Integration Points**:
   - For EACH new method/class, document:
     - What file it will be in
     - What existing method will CALL it
     - What line in the caller needs to change
   - Add these as explicit TODO tasks

4. **Verify No Orphan Code**:
   - Review each new component planned
   - Confirm each has a caller identified
   - If any new code has no caller → add integration task

**📋 ITERATION 6 (First Round) / ITERATION 13 (Second Round): SKEPTICAL RE-VERIFICATION**

🚨 **CRITICAL**: Assume NOTHING written so far is accurate. Start fresh.

1. **Question Everything**:
   - Is the file path I documented actually correct? (Verify with Read/Glob)
   - Does that method I referenced actually exist? (Verify with Grep)
   - Is that pattern I identified actually used? (Re-search codebase)
   - Are my assumptions about data flow correct? (Re-trace through code)
   - Did I misunderstand the original requirement? (Re-read specification)

2. **Fresh Codebase Validation**:
   - Re-search for ALL file paths mentioned in TODO
   - Re-verify ALL method names and line numbers
   - Re-validate ALL code patterns claimed
   - Re-check ALL dependencies and imports
   - Re-examine ALL test patterns documented

3. **Requirement Re-Verification**:
   - Re-read original specification word-by-word
   - Re-read user question answers (if second round)
   - List requirements again from scratch
   - Compare new list against TODO
   - Identify discrepancies or misinterpretations

4. **Comprehensive Corrections**:
   - Fix any incorrect file paths
   - Correct any wrong method names
   - Update any misunderstood patterns
   - Revise any flawed implementation strategies
   - **Add missing integration tasks** (caller modifications)
   - Document what was corrected and why

5. **Document Re-Verification**:
   - Add "Skeptical Re-Verification Results" section to TODO
   - List what was verified as correct
   - List what was found to be incorrect and corrected
   - Document confidence level in current plan

**📋 ITERATION 7 (First Round) / ITERATION 14 (Second Round): INTEGRATION GAP CHECK**

🚨 **CRITICAL**: Final check that all new code will actually be used.

1. **Create Integration Matrix**:
   For EACH new component, fill out:
   ```
   | New Component | File | Called By | Caller File:Line | Caller Modification Task |
   |---------------|------|-----------|------------------|--------------------------|
   | save_optimal_configs_folder() | ResultsManager.py | run_iterative_optimization() | SimulationManager.py:261 | Task 4.2 |
   ```

2. **Verify Caller Modifications in TODO**:
   - For each row in the matrix, confirm a TODO task exists to modify the caller
   - If missing → add the task immediately
   - Flag with ⚠️ if integration was previously overlooked

3. **Check for Orphan Code**:
   - Any new component without a caller = orphan code
   - Either add caller modification task OR remove the orphan component
   - Document decision in TODO

4. **Verify Entry Point Coverage**:
   - For each entry point affected by requirements
   - Trace through to output
   - Confirm all new code is in the execution path

5. **🚨 Check Entry Script File Discovery Patterns** (NEW):
   - If output format changes (e.g., JSON → folder, single file → multiple files):
     - List all `run_*.py` scripts that auto-detect or find these files
     - Verify glob patterns match new output format
     - Verify file validation logic matches new structure
     - Add TODO tasks for any entry script updates needed
   - Create Entry Script Update Matrix:
     ```
     | Output Change | Entry Script | Discovery Pattern | Needs Update? | TODO Task |
     |---------------|--------------|-------------------|---------------|-----------|
     | JSON → folder | run_simulation.py | glob("optimal_*.json") | YES | Task 5.1 |
     ```

**📋 ITERATIONS 8-11 (Second Round): Standard Verification with Answers**

Continue with standard verification process (same as Iterations 1-4) but with user answers integrated.

**📋 ITERATIONS 15-16 (Second Round): Final Preparation**

1. **Final Integration Check**:
   - Verify all user answers are reflected in implementation plan
   - Cross-check dependencies one final time
   - Validate testing strategy is comprehensive
   - Confirm documentation updates are complete

2. **Implementation Readiness**:
   - Ensure every task is actionable and clear
   - Verify no ambiguities remain
   - Confirm all code references are accurate
   - Validate execution order is optimal

3. **Create Integration Verification Checklist**:
   - List every new method/class with its caller
   - Create a checklist to verify during implementation:
     ```
     □ New method created: save_optimal_configs_folder()
     □ Caller modified: SimulationManager.py:261
     □ Entry point tested: python run_simulation.py --mode iterative
     □ Output verified: folder with 4 files created
     ```

4. **Risk Assessment**:
   - Document remaining risks
   - Identify potential blockers
   - Plan mitigation strategies
   - Set success criteria

### **DOCUMENTATION REQUIREMENTS**:

After completing each verification round, add/update a "Verification Summary" section to the TODO file documenting:
- ✅ Number of iterations completed (7 for first round, 16 after second round, 24 total after third round)
- ✅ Number of requirements added after initial draft
- ✅ Key codebase patterns/utilities identified for reuse
- ✅ Critical dependencies or ordering requirements
- ✅ Risk areas identified during research
- ✅ Questions identified for user clarification (first round)
- ✅ Question answers integrated into plan (second round)
- ✅ **Data flow traces** for each requirement (entry point → output)
- ✅ **Integration matrix** showing new components and their callers
- ✅ **Skeptical re-verification results** (corrections made, confidence level)
- ✅ **Algorithm traceability matrix** for calculations/formulas with conditional logic

### **ACCEPTANCE CRITERIA** (before beginning implementation):
- ✅ First verification round complete (7 iterations on draft TODO, including data flow, skeptical re-verification, and integration gap check)
- ✅ Questions file created with thoughtful, research-backed questions
- ✅ User answers received for all questions
- ✅ Second verification round complete (9 more iterations with answers integrated, including second data flow, skeptical re-verification, and integration gap check)
- ✅ **Third verification round complete** (8 iterations with algorithm deep-dive, edge case verification, test planning, and final skeptical review)
- ✅ **Total: 24 complete verification iterations performed** (3 rounds with 3 data flow verifications, 3 skeptical re-verifications, 3 integration gap checks)
- ✅ Every requirement from original file covered in TODO
- ✅ Every question answer reflected in TODO tasks
- ✅ Specific file paths identified for each task (verified multiple times)
- ✅ Existing code patterns researched and documented (validated in skeptical phases)
- ✅ Test requirements specified for each implementation
- ✅ Task dependencies and ordering verified
- ✅ Edge cases and error scenarios addressed
- ✅ Documentation update tasks included
- ✅ Pre-commit validation checkpoints added
- ✅ **All claims and assumptions verified through skeptical re-verification**
- ✅ **Data flow traced from entry point to output for each requirement**
- ✅ **Integration matrix created showing all new components and their callers**
- ✅ **Caller modifications included in TODO (not just new method creation)**
- ✅ **Integration verification checklist created for implementation phase**
- ✅ **Algorithm traceability matrix created for all calculations/formulas in spec**
- ✅ **Conditional logic from spec documented explicitly (if X then A, else B)**

### **ENFORCEMENT**:
- **NO SHORTCUTS**: Cannot skip iterations or rush through verification
- **THREE ROUNDS REQUIRED**: Must complete all three verification rounds (7 + 9 + 8 = 24 total iterations)
- **DATA FLOW PHASES MANDATORY**: Must complete iterations 5, 12 as end-to-end data flow verification
- **SKEPTICAL PHASES MANDATORY**: Must complete iterations 6, 13, and 22 as skeptical re-verifications
- **INTEGRATION GAP PHASES MANDATORY**: Must complete iterations 7, 14, and 23 as integration gap checks
- **ALGORITHM DEEP DIVE MANDATORY**: Must complete iteration 19 with exact spec-to-code comparison
- **ALGORITHM TRACEABILITY MANDATORY**: Must create matrix for all calculations with conditional logic
- **QUESTIONS REQUIRED**: Must create questions file after first verification round
- **NO ASSUMPTIONS**: Must research codebase to validate approach
- **NO VAGUE TASKS**: Each task must have specific technical details
- **ITERATIVE IS MANDATORY**: Minimum 24 total cycles of read-question-research-update
- **DOCUMENT THE PROCESS**: Verification summary required in TODO file after each round
- **FRESH EYES REQUIRED**: Skeptical iterations must approach verification as if seeing the plan for the first time
- **INTEGRATION MATRIX REQUIRED**: Must create matrix showing new components and their callers
- **NO SIMPLIFIED ALGORITHMS**: If spec has conditional logic, implementation must have matching conditions

### **WHY THIS MATTERS**:
Thorough TODO preparation with skeptical re-verification prevents:
- ❌ Discovering missing requirements mid-implementation
- ❌ Breaking existing functionality due to unforeseen dependencies
- ❌ Inconsistent code that doesn't match project patterns
- ❌ Incomplete implementations that miss edge cases
- ❌ Failed tests due to inadequate test planning
- ❌ Rework and refactoring caused by poor initial planning
- ❌ **Incorrect assumptions about code structure or API behavior**
- ❌ **Pursuing implementation strategies based on misunderstood patterns**
- ❌ **Building on top of incorrect file paths or method references**
- ❌ **Creating infrastructure methods that are never called from entry points**
- ❌ **Building components without wiring them into the actual system**
- ❌ **Changing output formats without updating entry script file discovery patterns**
- ❌ **Implementing simplified logic that ignores conditional requirements in the spec**
- ❌ **Writing code that "looks right" structurally but calculates incorrectly**

**The specialized verification phases are critical**:

**Data Flow Verification (iterations 5, 12)** forces the agent to:
1. Trace the complete path from user action to system output
2. Identify where new code fits in the execution flow
3. Document what existing code needs to change to use new code
4. Prevent orphan code that is never called

**Skeptical Re-Verification (iterations 6, 13, 22)** forces the agent to:
1. Challenge its own assumptions
2. Re-validate all claims with fresh codebase research
3. Catch errors that might have been overlooked in earlier iterations
4. Ensure the plan is built on accurate, verified information

**Integration Gap Check (iterations 7, 14, 23)** forces the agent to:
1. Create a matrix of new components and their callers
2. Verify every new method has a corresponding caller modification task
3. Flag and fix any orphan code before implementation begins
4. Ensure the TODO includes both infrastructure AND integration tasks

**Algorithm Traceability Matrix (iterations 4, 11, 19)** forces the agent to:
1. Extract EXACT algorithm descriptions from the spec (not paraphrased)
2. Document conditional logic explicitly (if week < X, then A; else B)
3. Map each algorithm to a specific code location
4. Prevent "simplified implementations" that ignore spec conditions
5. Catch cases where code structure is right but calculation logic is wrong

**Third Round Algorithm Deep Dive (iteration 19)** forces the agent to:
1. Quote exact spec text for every algorithm and calculation
2. Verify each conditional branch matches spec exactly
3. Flag any simplifications or deviations from spec
4. Ensure behavior tests are planned (not just structure tests)

A well-researched, thoroughly verified, and integration-validated TODO file is the foundation of successful implementation.
Immediately after creating the TODO file, create a code changes documentation file in the updates folder (NOT the done folder yet) named `{objective_name}_code_changes.md`. This file should be updated incrementally as you work through each task in the TODO file. After completing each significant change, immediately document it in the code changes file with: file paths, line numbers, before/after code snippets, rationale, and impact. This ensures the documentation stays current and accurate throughout the implementation process. The file will be moved to updates/done when the objective is complete.
After updates are complete, verify that all unit tests still pass and test the system to ensure it is functional. Test ALL unit tests across the entire repo. All tests across the entire repo must pass before we can mark an objective as complete. Make this a very clear and important TODO item.
Create any new unit tests to cover the new implementations, and modify any relevant unit tests and test them to ensure they pass.
Update rules files and readme files according to the new changes.
When the objective is complete, ensure the code changes documentation file is comprehensive and finalized. It should detail all code modifications made during the implementation, including: specific file paths and line numbers, before/after code snippets, rationale for each change, impact analysis, configuration changes, test modifications, and verification of files that were checked but not modified. This serves as a complete technical reference for understanding exactly what changed and why. Move this file from updates/ to updates/done/ along with the objective file.
Once the objective is completely done, then move the associated file in updates to the 'done' folder contained within the same updates directory. Also delete the questions file once the objective is complete.
Be VERY systematic when creating the TODO file and proceeding with the implementation. Break the objective up into modualized components. Each phase that is outlined in the todo file should leave the repo is a state that is still testable and functional, and should run the pre-commit checklist in its entirety. Do not skip any unit tests or interactive integration tests just because you think that the tests will not be effected by the change - assume everything is at risk of breaking no matter what you do.

## END-TO-END DATA FLOW VERIFICATION PROTOCOL

**🚨 CRITICAL: INFRASTRUCTURE vs INTEGRATION** - Creating helper methods, utility functions, or infrastructure components is NOT the same as integrating them into the system. This protocol ensures new code is actually USED, not just created.

### **THE INFRASTRUCTURE TRAP**:
A common failure pattern is:
1. ✅ Create new methods/classes that implement required functionality
2. ✅ Write tests for those new methods
3. ✅ Tests pass
4. ❌ **BUT**: The new methods are never called from entry points
5. ❌ **RESULT**: Feature appears complete but doesn't actually work for users

**Example of this failure**:
- Requirement: "Simulation should output folders instead of single files"
- What was done: Created `save_optimal_configs_folder()` method with tests
- What was missed: `SimulationManager.run_iterative_optimization()` still calls `save_optimal_config()` (single file)
- Result: Method exists, tests pass, but simulation still outputs single files

### **WHEN TO EXECUTE**:
- ✅ During TODO file creation (identify entry points that need modification)
- ✅ During skeptical re-verification (trace data flow for each requirement)
- ✅ After implementation (verify new code is called from entry points)
- ✅ Before marking objective complete (final integration check)

### **MANDATORY VERIFICATION STEPS**:

**📋 STEP 1: Identify ALL Entry Points**

Entry points are user-facing scripts or functions where execution begins:
- Root scripts: `run_*.py` files
- Main functions: `if __name__ == "__main__"` blocks
- Manager classes: Top-level orchestrators (e.g., `SimulationManager`, `LeagueHelperManager`)
- CLI commands: User-invoked operations

For each requirement, ask:
- "What script/function does the user run to trigger this?"
- "What is the entry point for this feature?"

**📋 STEP 2: Trace Data Flow from Entry to Output**

For each requirement, trace the COMPLETE path:
```
Entry Point → Manager/Controller → Service/Helper → Output
```

Document this flow in the TODO file:
```
Requirement: "Simulation outputs folders"
Entry Point: run_simulation.py → SimulationManager.run_iterative_optimization()
Current Flow: ... → ResultsManager.save_optimal_config() → single file
Required Flow: ... → ResultsManager.save_optimal_configs_folder() → folder with 4 files
Files to Modify: SimulationManager.py (change method call)
```

**📋 STEP 3: Verify Integration Points**

For each NEW method/class created, answer:
- "What existing code will CALL this new code?"
- "Is there a modification needed in the caller?"
- "Have I added the call, or just created the method?"

Create an integration checklist:
```
New Method: ResultsManager.save_optimal_configs_folder()
Called By: SimulationManager.run_iterative_optimization() ← NEEDS MODIFICATION
Current Call: save_optimal_config()
New Call: save_optimal_configs_folder()
Status: ❌ NOT INTEGRATED (method exists but not called)
```

**📋 STEP 4: Test from Entry Point**

After implementation, verify by starting from the entry point:
1. Run the actual user-facing script
2. Verify the output matches requirements
3. Don't just run unit tests - run the actual feature

```bash
# Don't just run: pytest tests/simulation/test_ResultsManager.py
# Also run: python run_simulation.py --mode iterative
# Then verify: ls simulation/optimal_configs/  # Should show folders, not files
```

### **INTEGRATION CHECKLIST TEMPLATE**:

Add this to TODO file for each new component:

```markdown
## Integration Verification

### New Component: [ClassName.method_name()]
- [ ] Method implemented
- [ ] Unit tests pass
- [ ] Called from: [CallerClass.caller_method()]
- [ ] Caller modified to use new method
- [ ] Entry point tested: [script_name.py]
- [ ] Output verified: [expected output description]

### Data Flow Trace:
Entry: [entry_point]
  → [step 1]
  → [step 2]
  → [NEW: step using new component]
  → Output: [expected output]
```

### **RED FLAGS TO WATCH FOR**:

🚩 "I created a new method but didn't modify any existing code to call it"
🚩 "The tests pass but I haven't run the actual script"
🚩 "I built the infrastructure but the manager/controller still uses the old approach"
🚩 "I added capability but didn't wire it into the execution path"
🚩 "I changed the output format but entry scripts still look for the old format"
🚩 "I changed file structure but CLI auto-detection still uses old patterns"

### **ENTRY POINT FILE DISCOVERY CHECKLIST**:

🚨 **CRITICAL**: When output formats change (e.g., single file → folder, JSON → CSV), entry point scripts often have file discovery logic that must be updated.

**Common Entry Script Patterns That Need Updating**:
1. **Auto-detection patterns**: `glob("optimal_*.json")` → `glob("optimal_*/")` with `.is_dir()` check
2. **File validation logic**: Checking for `.json` extension → checking for folder with required files
3. **Path resolution**: Loading single file → loading folder with multiple files
4. **Error messages**: "No .json files found" → "No config folders found"
5. **Help text and documentation**: Describing old format → describing new format

**When Output Format Changes, Check These Files**:
- `run_*.py` - All CLI entry scripts
- Argument parser help text
- Default path constants
- File/folder discovery functions
- Validation and error handling
- README and documentation examples

**Verification Template**:
```
Output Format Change: Single JSON → Folder with 4 files
Files Creating Output: ResultsManager.save_optimal_configs_folder()
Entry Scripts Affected: run_simulation.py
Discovery Pattern Change: glob("optimal_*.json") → glob("optimal_*/") + folder validation
Error Message Update: "No optimal config files" → "No optimal config folders"
Help Text Update: --baseline accepts folder path, not JSON file
✅ All entry script patterns updated to match new output format
```

### **ENFORCEMENT**:
- **NO ORPHAN CODE**: Every new method must have an identified caller
- **TRACE REQUIRED**: Data flow must be documented from entry point to output
- **INTEGRATION MANDATORY**: Creating infrastructure without integration = incomplete
- **END-TO-END TEST**: Must verify from user entry point, not just unit tests

---

## REQUIREMENT VERIFICATION PROTOCOL

**🚨 CRITICAL: FINAL VERIFICATION BEFORE MARKING OBJECTIVE COMPLETE** - This protocol must be executed before claiming an objective is complete:

### **WHEN TO EXECUTE**:
- ✅ After all implementation work appears to be complete
- ✅ Before moving objective files to updates/done/
- ✅ Before deleting questions files
- ✅ Before claiming "objective complete" to the user

### **MANDATORY VERIFICATION STEPS**:

**📋 STEP 1: Re-read Original Requirements File**
- Open and read EVERY LINE of the original `updates/{objective_name}.txt` file
- Create a checklist of EVERY requirement mentioned (numbered or implied)
- For each requirement, verify it has been implemented
- Mark each requirement as ✅ DONE or ❌ MISSING

**📋 STEP 2: Re-read Question Answers File**
- Open and read EVERY ANSWER in `updates/{objective_name}_questions.md`
- Create a checklist of EVERY answer that implies implementation work
- For each answer, verify the implementation matches what was answered
- Mark each answer as ✅ IMPLEMENTED or ❌ NOT IMPLEMENTED

**📋 STEP 3: Search Codebase for Implementation**
- Use Grep/Glob tools to search for evidence of each requirement
- Verify files were actually modified as required
- Check that new files were created if specified
- Confirm no placeholder code or TODOs remain

**📋 STEP 3.5: 🚨 ALGORITHM VERIFICATION (NEW - CRITICAL)**

For each algorithm/calculation in the spec, verify the implementation matches **exactly**:

1. **Extract Algorithm from Spec**:
   - Quote the exact algorithm description from the original spec file
   - Note any conditional logic (if/else, week-specific, position-specific)
   - Identify edge cases mentioned in the spec

2. **Read Implementation Code**:
   - Open the file that implements this algorithm
   - Read the actual code line-by-line
   - Compare each condition and calculation to the spec

3. **Verify Logic Matches**:
   - For each conditional in the spec, find the corresponding code condition
   - For each calculation formula, verify the code implements it correctly
   - Check that edge cases are handled as specified

4. **Create Algorithm Verification Matrix**:
   ```
   | Spec Line | Algorithm | Code File:Line | Spec Says | Code Does | Match? |
   |-----------|-----------|----------------|-----------|-----------|--------|
   | 158-186 | projected weeks | generator.py:195 | week >= X: use current week projection | uses current_week_projection | ✅ |
   | 241-276 | player_rating | generator.py:147 | week 2+: cumulative points | copies same rating | ❌ MISMATCH |
   ```

5. **Fix Mismatches Immediately**:
   - Any ❌ MISMATCH requires immediate correction
   - Re-verify after fixing
   - Update tests to cover the algorithm behavior

**Common Algorithm Verification Failures**:
- ❌ Spec says "recalculate per iteration" but code calculates once
- ❌ Spec says "use value A for condition X, value B for condition Y" but code uses same value
- ❌ Spec describes conditional logic but code uses simplified unconditional logic
- ❌ Spec mentions edge cases but code doesn't handle them

**📋 STEP 4: Verify End-to-End Integration**
- For each NEW method/function created:
  - Search codebase to find what CALLS this method
  - If nothing calls it → ❌ INTEGRATION MISSING
  - Verify the caller is in the execution path from entry point
- For each requirement:
  - Trace from entry point (run_*.py) to output
  - Verify the new code is in the execution path
  - Run the actual script to confirm behavior (not just unit tests)
- Create integration evidence:
  ```
  Requirement: "Simulation outputs folders"
  New Method: save_optimal_configs_folder()
  Called By: SimulationManager.run_iterative_optimization() line 261
  Entry Point: run_simulation.py --mode iterative
  Verified: ✅ Running script produces folder output
  ```

**📋 STEP 5: Identify Missing Requirements**
- If ANY requirement is ❌ MISSING or ❌ NOT IMPLEMENTED or ❌ INTEGRATION MISSING:
  - STOP immediately
  - Create a new completion TODO file: `updates/todo-files/{objective_name}_completion_todo.md`
  - Document ALL missing requirements and integration gaps
  - Implement missing requirements before proceeding
  - Re-run this verification protocol

**📋 STEP 6: Document Verification**
- Add a "Requirements Verification" section to the code changes file
- List each requirement and its implementation status
- Include file paths and line numbers as evidence
- Confirm 100% requirement coverage

### **ACCEPTANCE CRITERIA**:
- ✅ ALL requirements from original file implemented (100% coverage)
- ✅ ALL question answers reflected in implementation
- ✅ NO missing functionality or partial implementations
- ✅ NO half-measures or "mostly complete" status
- ✅ Evidence of implementation exists in codebase (files, code, tests)
- ✅ All unit tests pass (100%)
- ✅ Manual testing confirms functionality works
- ✅ **ALL new methods have identified callers (no orphan code)**
- ✅ **Integration verified from entry point to output**
- ✅ **Actual scripts run and produce expected behavior (not just unit tests)**
- ✅ **Minimum 3 quality control review rounds completed and documented**

### **ENFORCEMENT**:
- **NO EXCEPTIONS**: If even ONE requirement is missing, objective is NOT complete
- **NO PARTIAL CREDIT**: "90% complete" = incomplete, must finish remaining 10%
- **NO ASSUMPTIONS**: Just because something seems done doesn't mean it is - verify with code
- **RE-VERIFICATION REQUIRED**: If new requirements discovered, re-run entire protocol
- **NO ORPHAN CODE**: Methods that exist but are never called = incomplete implementation
- **INTEGRATION REQUIRED**: Infrastructure without integration = feature doesn't work
- **3 QC ROUNDS REQUIRED**: Must complete and document 3 quality control review rounds

### **FAILURE TO VERIFY = INCOMPLETE OBJECTIVE**:
If this protocol is not executed, or if missing requirements are discovered after claiming completion, the objective must be reopened and completed properly. The user must be notified of any missing requirements immediately.

**Common Integration Failures to Check**:
- ❌ Created helper method but manager still uses old method
- ❌ Added new output format but save function still uses old format
- ❌ Built infrastructure but controller not updated to use it
- ❌ Tests pass but running actual script shows old behavior
- ❌ Changed output format (JSON → folder) but entry script still looks for old format
- ❌ Entry script glob patterns don't match new file/folder structure
- ❌ Error messages reference old format instead of new format

---

## QUALITY CONTROL REVIEW PROTOCOL

**🚨 MANDATORY: MINIMUM 3 REVIEW ROUNDS** - After implementation appears complete, the agent must perform at least 3 independent quality control review rounds before marking an objective as complete.

### **THE REVIEW PROMPT**:

For each round, the agent must execute this review:

> **"Review the TODO file, code changes, and original requirements to ensure nothing was skipped, left out, or done incorrectly."**

### **REVIEW ROUND REQUIREMENTS**:

**📋 ROUND 1: Initial Quality Review**
1. Re-read the original requirements file (`updates/{objective_name}.txt`)
2. Re-read the TODO file (`updates/todo-files/{objective_name}_todo.md`)
3. Re-read the code changes file (`updates/{objective_name}_code_changes.md`)
4. Cross-reference all three documents
5. Identify any discrepancies, missing items, or incorrect implementations
6. Document findings and fix any issues found

**📋 ROUND 2: Deep Verification Review**
1. With fresh perspective, repeat the same review process
2. Focus on algorithm correctness and edge cases
3. Verify conditional logic matches spec exactly
4. Check that tests actually validate the behavior (not just structure)
5. Document findings and fix any issues found

**📋 ROUND 3: Final Skeptical Review**
1. Assume previous reviews missed something
2. Re-read spec with "adversarial" mindset - actively look for gaps
3. Verify every algorithm, calculation, and conditional
4. Confirm all requirements have corresponding tests
5. Document final verification status

### **WHAT TO CHECK IN EACH ROUND**:

| Document | What to Verify |
|----------|---------------|
| Original Requirements | Every line has been addressed |
| TODO File | All tasks marked complete, no orphan items |
| Code Changes | All changes documented, line numbers accurate |
| Algorithm Logic | Conditional logic matches spec exactly |
| Test Coverage | Behavior tests exist (not just structure tests) |

### **ROUND DOCUMENTATION**:

After each round, document in the code changes file:
```
## Quality Control Round [N]
- Reviewed: [date/time]
- Issues Found: [list or "None"]
- Issues Fixed: [list or "N/A"]
- Status: ✅ PASSED / ❌ ISSUES FOUND (fixed)
```

### **ENFORCEMENT**:

- **MINIMUM 3 ROUNDS**: Cannot mark objective complete with fewer than 3 review rounds
- **DOCUMENT EACH ROUND**: Each round must be documented in code changes file
- **FIX BEFORE PROCEEDING**: If issues found in round N, fix them before round N+1
- **FRESH PERSPECTIVE**: Each round should approach review as if seeing it for first time
- **NO RUSHING**: Each round must be thorough, not a cursory check

### **WHY 3 ROUNDS?**:

Experience shows that:
- Round 1 catches obvious issues
- Round 2 catches algorithm/logic issues missed in Round 1
- Round 3 catches subtle issues that require "adversarial" thinking

The `players_projected.csv` week logic and `player_rating` recalculation issues were both caught on review rounds after initial implementation appeared complete. Multiple review rounds are essential for quality.

---

## PRE-COMMIT VALIDATION PROTOCOL

**🚨 MANDATORY FOR EVERY STAGE COMPLETION** - This protocol must be executed at the completion of EVERY phase, step, or significant change before proceeding to the next stage:

### **WHEN TO EXECUTE**:
- ✅ After completing ANY phase step (e.g., Phase 2 Step 2.1)
- ✅ Before moving to the next phase or step
- ✅ When instructed to "validate and commit" or "commit changes"
- ✅ At any major milestone or completion point
- ✅ Before asking user for validation to proceed

### **MANDATORY EXECUTION STEPS**:

**🚀 REQUIRED: Run Unit Tests**

Run the unit test suite to validate all changes:

```bash
python tests/run_all_tests.py
```

This command executes ALL unit tests:
- ✅ Complete unit test suite in tests/ directory
- ✅ Strict 100% pass requirement
- ✅ Returns exit code 0 for success, 1 for failure

**Exit Codes**:
- `0` = All tests passed (100%), safe to commit
- `1` = Some tests failed, DO NOT COMMIT until issues are fixed

**Test Options**:
```bash
python tests/run_all_tests.py --verbose    # Show individual test names
python tests/run_all_tests.py --detailed   # Full test output
python tests/run_all_tests.py --single     # Faster single command mode
```

**Validation Steps**:

1. **ANALYZE CHANGES**:
   ```bash
   git status
   git diff
   ```
   - Review ALL changed files
   - Understand impact of changes

2. **ADD/UPDATE UNIT TESTS**:
   - Add tests for new functionality in `tests/` directory
   - Follow test structure: `tests/module_path/test_FileName.py`
   - Use proper mocking to isolate functionality
   - Ensure tests follow Arrange-Act-Assert pattern

   **🚨 ALGORITHM BEHAVIOR TESTS (CRITICAL)**:
   - For each algorithm/calculation in the spec, write tests that verify:
     - The calculation produces expected output for known inputs
     - Conditional logic works correctly (test both branches)
     - Edge cases are handled as specified
   - Example: If spec says "week 1 uses draft rank, week 2+ uses cumulative points":
     - Test that week 1 output uses draft-based values
     - Test that week 5 output differs from week 1 (uses performance-based values)
     - Test the boundary case (week 2 transition)
   - **Structure tests don't catch algorithm bugs** - a file can exist with wrong logic
   - Write tests that would FAIL if the algorithm is implemented incorrectly

3. **RUN ALL UNIT TESTS** (MANDATORY):
   ```bash
   python tests/run_all_tests.py
   ```
   - **100% pass rate required**
   - Fix any failing tests before proceeding
   - Re-run until all tests pass

4. **MANUAL TESTING** (if applicable):
   - Test the affected functionality manually
   - Run the main scripts to verify behavior:
     ```bash
     python run_league_helper.py   # League helper mode
     python run_player_fetcher.py  # Player data fetcher
     python run_simulation.py      # Simulation system
     ```

5. **UPDATE DOCUMENTATION**:
   - Update README.md if functionality changed
   - Update CLAUDE.md if workflow or architecture changed
   - Update rules.md if development process changed
   - Update module-specific documentation as needed

6. **COMMIT STANDARDS**:
   - Format: "Brief description of change"
   - Keep under 50 characters when possible
   - NO emojis or icons
   - Do NOT include "Generated with Claude Code" footer
   - List major changes in commit body if needed

### **FAILURE PROTOCOL**:
- **If ANY test fails**: STOP immediately, fix the issue, re-run tests
- **If unit tests fail**: Fix failing tests, ensure 100% pass rate before proceeding
- **No exceptions**: Cannot proceed to next phase without 100% test success
- **Cannot commit**: Do NOT commit code with failing tests

### **ENFORCEMENT**:
- This protocol is MANDATORY and NON-NEGOTIABLE for every stage completion
- Violation of this protocol requires immediate correction and re-validation
- The user should be notified if this protocol was not followed properly
