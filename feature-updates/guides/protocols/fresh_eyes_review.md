# Fresh Eyes Review Protocol

**Purpose:** Re-read specification with fresh perspective to catch missed requirements.

**Related:** [README.md](README.md) - Protocol index

---


**Execute during:** Iterations 17 and 18

**Steps:**

1. **Clear mental state**
   - Pretend you haven't read the spec before
   - Set aside all assumptions from previous iterations
   - Approach with beginner's mindset

2. **Read spec from start to finish**
   - Read `{feature_name}_specs.md` word by word
   - Note anything that seems unclear or incomplete
   - Mark any requirements you don't remember seeing in TODO

3. **"Same As X" Language Audit (CRITICAL)**
   Search spec for these phrases and verify each one:
   - "same as", "same structure as", "same format as"
   - "like existing", "mirror", "follow pattern of"
   - "similar to", "matches", "consistent with"

   For EACH match found:
   - Have you actually READ the referenced file/folder X?
   - Can you list EVERY file in X?
   - Is there a TODO task for EACH file with its EXACT structure?
   - If X serves as input elsewhere, have you verified consumer requirements?

   **If ANY answer is "no", this is a missed requirement - add to TODO immediately.**

4. **List all requirements fresh**
   - Write requirements from scratch based on this reading
   - Don't reference your TODO while doing this
   - Number each requirement

5. **Compare to TODO**
   - Match fresh list against existing TODO tasks
   - Identify any requirements missing from TODO
   - Identify any TODO tasks not tied to requirements

6. **Document findings**
   - Add missed requirements to TODO immediately
   - Remove or question orphan tasks
   - Note confidence level in completeness

**Output:** Updated TODO with any missed requirements added.

---

