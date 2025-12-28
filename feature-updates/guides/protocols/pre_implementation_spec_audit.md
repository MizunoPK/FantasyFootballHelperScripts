# Pre-Implementation Spec Audit Protocol

**Purpose:** Comprehensive spec-to-TODO audit with fresh eyes to catch all mismatches, missing details, and vague instructions before implementation begins. This is the final quality gate before code is written.

**Related:** [README.md](README.md) - Protocol index

---


**Execute during:** Iteration 23a (immediately after Integration Gap Check, before Implementation Readiness)

**Historical Context:** Added after feature implementation passed all 24 iterations but failed QC Round 1 with 40% failure rate. This audit would have caught ALL 8 issues found in QC (wrong structure, missing fields, incorrect mappings) BEFORE any code was written.

**Critical Mindset:** Pretend you're a QA reviewer who's never seen this feature before. You have:
- ✅ The specs.md file
- ✅ The TODO.md file
- ❌ NO OTHER CONTEXT

Your job: Find every mismatch, missing detail, and vague instruction.

**Four-Part Audit:**

#### Part 1: Spec Coverage Audit (Completeness)

For EACH section in specs.md:

1. **Read spec section** (e.g., "Section 2: Common Player Fields")
2. **Extract all requirements** from that section (list them individually)
3. **Find corresponding TODO items** that implement those requirements
4. **Verify each requirement has:**
   - [ ] A TODO item that addresses it
   - [ ] Acceptance criteria that matches the spec exactly
   - [ ] Spec line reference
   - [ ] Example of correct output

**Red flags:**
- ⛔ Spec requirement with no TODO item
- ⛔ TODO item exists but no acceptance criteria
- ⛔ Acceptance criteria doesn't match spec
- ⛔ No example showing what "correct" looks like

**Example audit finding:**
```
SPEC SECTION: Common Player Fields (specs.md lines 44-56)

Requirements extracted:
1. id (number) - converted from string
2. name (string)
3. team (string)
4. position (string)
5. injury_status (string)
6. drafted_by (string)
7. locked (boolean)
8. average_draft_position (number or null)
9. player_rating (number or null)
10. projected_points (array[17])
11. actual_points (array[17])

TODO items found:
- Phase 4.3: Build position JSON

Acceptance criteria in TODO:
- "Include all fields" ❌ VAGUE
- No list of 11 fields ❌ INCOMPLETE
- No types specified ❌ MISSING
- No spec reference ❌ MISSING

STATUS: ❌ FAIL - TODO incomplete
ACTION REQUIRED: Add all 11 fields with types and spec reference
```

#### Part 2: TODO Clarity Audit (Actionability)

For EACH TODO item:

1. **Cover up the specs.md file** (pretend you can't see it)
2. **Read ONLY the TODO item**
3. **Ask: "Could I implement this correctly right now?"**
4. **If NO, identify what's missing:**
   - Missing data structure?
   - Missing field list?
   - Missing constraints (array length, type, etc.)?
   - Missing examples?
   - Ambiguous wording?

**Red flags:**
- ⛔ "Transform to..." without showing structure
- ⛔ "Build..." without listing components
- ⛔ "Include all..." without enumerating
- ⛔ "Handle..." without specifying behavior
- ⛔ No examples of correct output
- ⛔ No anti-examples of common mistakes

#### Part 3: Data Structure Audit (Exactness)

For EACH data structure mentioned in specs:

1. **Find the structure in specs** (e.g., JSON root structure)
2. **Find corresponding TODO item**
3. **Verify TODO shows EXACT structure:**
   - Same field names
   - Same nesting
   - Same types
   - Same array lengths
   - Same null handling

**Red flags:**
- ⛔ Structure described in words, not shown
- ⛔ Field names differ from spec
- ⛔ Nesting level differs
- ⛔ Missing required fields
- ⛔ Wrong types

#### Part 4: Mapping Audit (Correctness)

For EACH mapping in specs (e.g., ESPN stat IDs to fields):

1. **Find mapping table in specs**
2. **Find corresponding TODO item**
3. **Verify TODO includes complete mapping:**
   - All source values listed
   - All target values listed
   - Transformation logic specified
   - Edge cases handled

**Red flags:**
- ⛔ Mapping mentioned but not shown
- ⛔ Incomplete mapping (some items missing)
- ⛔ No transformation logic
- ⛔ No edge case handling

**Completion Criteria:**

All four audits must pass:

- [ ] **Part 1 (Coverage):** Every spec requirement has TODO item with acceptance criteria
- [ ] **Part 2 (Clarity):** Every TODO item is implementable without reading specs
- [ ] **Part 3 (Structure):** Every data structure in specs is shown exactly in TODO
- [ ] **Part 4 (Mapping):** Every mapping in specs is documented in TODO

**If ANY audit fails:**
1. Document all findings in audit report
2. Update TODO with missing details from specs
3. Re-run audit until all parts pass
4. **DO NOT proceed to Iteration 24** until audit passes

**Audit Output Template:**

```markdown
## Iteration 23a: Pre-Implementation Spec Audit

**Audit Date:** [Date]
**Auditor Mindset:** Fresh eyes, never seen this feature before

### Part 1: Spec Coverage Audit
- [ ] Section 1 (File Structure): X requirements, Y TODO items ✅/❌
- [ ] Section 2 (Common Fields): X requirements, Y TODO items ✅/❌
- [ ] Section 3 (Position Stats): X requirements, Y TODO items ✅/❌
...

**Findings:**
1. [Issue found]
2. [Issue found]

**Status:** ✅ PASS / ❌ FAIL (X issues found)

### Part 2: TODO Clarity Audit
- [ ] Phase 1: All items actionable without specs? ✅/❌
- [ ] Phase 2: All items actionable without specs? ✅/❌
...

**Findings:**
1. [Vague item]
2. [Missing details]

**Status:** ✅ PASS / ❌ FAIL (X items need clarification)

### Part 3: Data Structure Audit
- [ ] Root JSON structure matches specs exactly? ✅/❌
- [ ] Player object structure matches specs exactly? ✅/❌
- [ ] Stat structure matches specs exactly? ✅/❌
...

**Findings:**
1. [Structure mismatch]
2. [Missing fields]

**Status:** ✅ PASS / ❌ FAIL (X mismatches found)

### Part 4: Mapping Audit
- [ ] ESPN stat ID mappings complete? ✅/❌
- [ ] drafted (0/1/2) → drafted_by mapping complete? ✅/❌
- [ ] locked (0/1) → boolean mapping complete? ✅/❌
...

**Findings:**
1. [Missing mapping]
2. [Incomplete mapping]

**Status:** ✅ PASS / ❌ FAIL (X mappings incomplete)

### OVERALL AUDIT RESULT: ✅ PASS / ❌ FAIL

**Total Issues Found:** X

**Actions Required Before Implementation:**
1. [Fix 1]
2. [Fix 2]
...

**Ready for Iteration 24 (Implementation Readiness)?** ✅ YES / ❌ NO
```

**Key Insight:** The audit must be done with "fresh eyes" - pretending you've never seen the feature before. This forces you to rely ONLY on the TODO, which reveals gaps that familiarity would hide.

**What This Audit Would Have Caught:**

Historical evidence from feature that failed QC Round 1:
- ✅ Wrong root structure (Structure Audit Part 3)
- ✅ Missing 3 common fields (Coverage Audit Part 1)
- ✅ Wrong stat structure (Structure Audit Part 3)
- ✅ Wrong stat mappings (Mapping Audit Part 4)
- ✅ Missing field types (Clarity Audit Part 2)
- ✅ Vague acceptance criteria (Clarity Audit Part 2)

**Result:** Would have prevented all rework, saved 2+ hours of implementation time.

**Output:** Audit report with pass/fail for all 4 parts, list of required fixes before implementation.

---

