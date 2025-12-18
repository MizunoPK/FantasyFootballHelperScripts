# Fix 'both' Mode Behavior - Lessons Learned

> **Purpose:** This file captures issues discovered during development that indicate gaps in the planning or development guides. These lessons are used to improve the guides for future features.

---

## Issues Discovered During Planning

### Issue 1: Assumption About Parameter Type (2025-12-17)

**What happened:**
- Initially assumed accuracy simulation optimized BASE_CONFIG_PARAMS (shared params)
- Resolved Q9 with "Option B: optimize for shared params"
- User clarified: "Not all params should be shared for accuracy sim. We will primarily be running sims on parameters that are horizon specific"
- Investigation revealed ALL 16 accuracy params are WEEK_SPECIFIC_PARAMS

**Root cause:**
- Did not verify parameter types against ResultsManager.WEEK_SPECIFIC_PARAMS during initial investigation
- Made assumption based on win-rate simulation pattern without checking accuracy sim's PARAMETER_ORDER
- Feature planning guide Phase 2.2 (Research Codebase Patterns) did not emphasize verifying parameter classifications

**Impact:**
- Q9 resolution was incorrect (needed to be reset)
- Multiple other questions (Q10, Q11, Q13, Q18, Q23) require revision based on week-specific assumption
- Implementation approach significantly different:
  - 5× configs per parameter (one set per horizon)
  - Each horizon optimizes independently
  - True tournament model (not shared optimization)

**How detected:**
- User statement: "actually I think there's been a misunderstanding that may affect the previous checklist items"
- Prompted investigation of PARAMETER_ORDER in run_accuracy_simulation.py
- Cross-referenced with ResultsManager.WEEK_SPECIFIC_PARAMS

**How fixed:**
- Added CRITICAL CONTEXT section to checklist with parameter type classification
- Reset Q9 to unresolved
- Updated specs.md Assumptions section with evidence
- Documented in lessons_learned.md (this file)
- Prepared to revise all affected questions with correct understanding

**Lesson for guides:**
- **Planning guide enhancement needed**: Phase 2.2 should include explicit step to verify parameter classifications
- Add checkpoint: "If feature involves parameters, verify against BASE_CONFIG_PARAMS vs WEEK_SPECIFIC_PARAMS"
- Emphasize cross-referencing between different simulation modes (don't assume same pattern)

---

## Issues Discovered During Development

*(To be populated if issues found during development phase)*

---

## Issues Discovered During QC

*(To be populated if issues found during QC rounds)*

---

## Proposed Guide Updates

*(To be populated based on lessons learned)*
