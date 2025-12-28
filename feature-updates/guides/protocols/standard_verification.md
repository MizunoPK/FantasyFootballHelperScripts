# Standard Verification Protocol

**Purpose:** Systematic verification through reading, questioning, researching, and updating.

**Related:** [README.md](README.md) - Protocol index

---


**Execute during:** Iterations 1-3, 8-10, 15-16

**Steps:**

1. **Re-read source documents**
   - `{feature_name}_specs.md` (line by line)
   - Current TODO file
   - User answers (if iterations 8+)

2. **Ask focus questions for this iteration:**

   | Iteration | Focus Questions |
   |-----------|-----------------|
   | 1 | What files need modification? What patterns exist in codebase? |
   | 2 | What error handling is needed? What logging should be added? |
   | 3 | What integration points exist? What mocking needed for tests? |
   | 8 | How do user answers change the plan? Any new tasks needed? |
   | 9 | Are dependencies correctly identified? Any imports missing? |
   | 10 | Is the task breakdown granular enough? Any tasks too large? |
   | 15 | Are all file paths confirmed? Any placeholders remaining? |
   | 16 | Is the integration checklist complete? Ready to implement? |

3. **Research codebase**
   - Use Glob/Grep to find relevant code
   - Look for similar implementations
   - Find test patterns to follow
   - Verify file paths exist

4. **"Same As X" Reference Verification (MANDATORY if spec references existing files/folders)**
   When the spec says "same as X", "same structure as X", "mirror X", or "like existing Y":
   - **READ the actual file/folder X** - do not interpret abstractly
   - **LIST every file** contained in X
   - **READ internal structure** of each file in X
   - **CREATE explicit TODO tasks** for each file with exact structure
   - **VERIFY consumer requirements** if X serves as input elsewhere

   **Red flag:** If your TODO says "create same format as X" but you haven't actually read X, STOP and read it now.

5. **Update TODO file**
   - Add missing requirements discovered
   - Add specific file paths with line numbers
   - Add code references for patterns to follow
   - Mark iteration complete in tracker

5. **Scope Creep Check (EVERY iteration)**
   Before marking the iteration complete, ask yourself:
   - "Am I adding tasks that weren't in the original spec?"
   - "Am I expanding the feature beyond what was requested?"
   - "Am I adding 'nice to have' items that weren't required?"

   **If YES to any:**
   - Document the potential addition
   - Mark it as "SCOPE QUESTION" in TODO
   - Ask user before including: "I found {X} could be improved. Should I include this in scope, or defer to a future feature?"

   **Valid additions (don't need user approval):**
   - Tasks required to implement spec items (discovered dependencies)
   - Error handling for spec requirements
   - Tests for spec requirements

   **Invalid additions (need user approval):**
   - "While I'm here, I could also..."
   - "This would be better if we also..."
   - "The codebase would benefit from..."

**Output:** Updated TODO file with iteration marked complete.

---

