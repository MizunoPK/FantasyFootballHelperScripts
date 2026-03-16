# Known Exceptions - Prerequisites/Exit Criteria

**Purpose:** Documents files that intentionally lack formal "## Prerequisites" or "## Exit Criteria" sections

**Last Updated:** 2026-02-25

**Why This Document Exists:**
Audit Dimension D8 (Documentation Quality) checks for "## Prerequisites" and "## Exit Criteria" sections in workflow guides. However, certain file types intentionally use alternative patterns. This document prevents these files from being flagged as violations in future audits.

---

## Exception Categories

### Category A: S5 Iteration Files (14 files)

**Pattern:** Lightweight iteration guides with inline prerequisites, exit criteria inherited from parent round

**⚠️ NOTE: All 14 files in this category have been DELETED from the filesystem** as part of the S5 v1 → S5 v2 migration. S5 v2 consolidates all iteration content into a single `s5_v2_validation_loop.md` file using an 11-dimension Validation Loop approach. These entries are retained for historical reference only — they cannot produce D8 false positives since the files no longer exist.

**Design Rationale (historical):**
- Iteration files were sequential steps within S5 v1 rounds (Round 1, Round 2, Round 3)
- Prerequisites were simple: "Previous iteration complete" (stated inline)
- Exit criteria defined at round level (s5_v2_validation_loop.md consolidates all rounds)
- Formal sections would have been redundant
- Files followed "router + detailed iteration" pattern for focused reference

**Missing Sections:** Prerequisites (inline instead), Exit Criteria (inherited from parent)

**Files (DELETED — S5 v1 only, no longer in filesystem):**

#### S5.P1 (Round 1) Iteration Files (7 files)

1. **stages/s5/s5_p1_i3_integration.md**
   - Type: Router for Iterations 5-7
   - Prerequisites: Line 8 - "**Prerequisites:** Iterations 1-4 + Gate 4a complete"
   - Exit Criteria: Inherited from s5_v2_validation_loop.md
   - Design: Navigation hub to 6 sub-iteration files

2. **stages/s5/s5_p1_i3_iter5_dataflow.md**
   - Type: Iteration 5 - End-to-End Data Flow
   - Prerequisites: Line 6 - "**Prerequisites:** Previous iterations complete"
   - Exit Criteria: Inherited from s5_v2_validation_loop.md
   - Design: Focused single-iteration guide (109 lines)

3. **stages/s5/s5_p1_i3_iter5a_downstream.md**
   - Type: Iteration 5a - Downstream Data Consumption Tracing
   - Prerequisites: Line 6 - "**Prerequisites:** Previous iterations complete"
   - Exit Criteria: Inherited from s5_v2_validation_loop.md
   - Design: Focused single-iteration guide (352 lines)

4. **stages/s5/s5_p1_i3_iter6_errorhandling.md**
   - Type: Iteration 6 - Error Handling Scenarios
   - Prerequisites: Line 6 - "**Prerequisites:** Previous iterations complete"
   - Exit Criteria: Inherited from s5_v2_validation_loop.md
   - Design: Focused single-iteration guide (132 lines)

5. **stages/s5/s5_p1_i3_iter6a_dependencies.md**
   - Type: Iteration 6a - External Dependency Final Verification
   - Prerequisites: Line 6 - "**Prerequisites:** Previous iterations complete"
   - Exit Criteria: Inherited from s5_v2_validation_loop.md
   - Design: Focused single-iteration guide (157 lines)

6. **stages/s5/s5_p1_i3_iter7_integration.md**
   - Type: Iteration 7 - Integration Gap Check
   - Prerequisites: Inline statement
   - Exit Criteria: Inherited from s5_v2_validation_loop.md
   - Design: Focused single-iteration guide

7. **stages/s5/s5_p1_i3_iter7a_compatibility.md**
   - Type: Iteration 7a - Backward Compatibility Check
   - Prerequisites: Inline statement
   - Exit Criteria: Inherited from s5_v2_validation_loop.md
   - Design: Focused single-iteration guide

#### S5.P3 (Round 3) Iteration Files (7 files)

8. **stages/s5/s5_p3_i1_preparation.md**
   - Type: Round 3 Part 1 - Preparation
   - Prerequisites: Inline statement
   - Exit Criteria: Inherited from s5_v2_validation_loop.md (Round 3 section)
   - Design: Preparation phase guide for Round 3

9. **stages/s5/s5_p3_i1_iter17_phasing.md**
   - Type: Iteration 17 - Phasing
   - Prerequisites: Inline statement
   - Exit Criteria: Inherited from s5_v2_validation_loop.md (Round 3 section)
   - Design: Focused single-iteration guide

10. **stages/s5/s5_p3_i1_iter18_rollback.md**
    - Type: Iteration 18 - Rollback
    - Prerequisites: Inline statement
    - Exit Criteria: Inherited from s5_v2_validation_loop.md (Round 3 section)
    - Design: Focused single-iteration guide

11. **stages/s5/s5_p3_i1_iter19_traceability.md**
    - Type: Iteration 19 - Traceability
    - Prerequisites: Inline statement
    - Exit Criteria: Inherited from s5_v2_validation_loop.md (Round 3 section)
    - Design: Focused single-iteration guide

12. **stages/s5/s5_p3_i1_iter20_performance.md** (DEPRECATED - S5 v1)
    - Type: S5 v1 Iteration 20 - Performance (now Dimension 9)
    - Prerequisites: Inline statement
    - Exit Criteria: Inherited from s5_v2_validation_loop.md
    - Design: Focused single-iteration guide (S5 v1 only)

13. **stages/s5/s5_p3_i1_iter21_mockaudit.md** (DEPRECATED - S5 v1)
    - Type: S5 v1 Iteration 21 - Mock Audit (now part of Dimension 11)
    - Prerequisites: Inline statement
    - Exit Criteria: Inherited from s5_v2_validation_loop.md
    - Design: Focused single-iteration guide (S5 v1 only)

14. **stages/s5/s5_p3_i1_iter22_consumers.md** (DEPRECATED - S5 v1)
    - Type: S5 v1 Iteration 22 - Consumers (now Dimension 10)
    - Prerequisites: Inline statement
    - Exit Criteria: Inherited from s5_v2_validation_loop.md
    - Design: Focused single-iteration guide (S5 v1 only)

**Audit Action:** SKIP these files when checking D8 (Documentation Quality) - Prerequisites/Exit Criteria

---

### Category B: S5 Design and Migration Documents (INACTIVE — files deleted)

**Pattern:** Design plans and migration guides (not workflow execution guides)

**Status:** These 2 files no longer exist in the repository. The S5 v1→v2 migration guide and S5 v2 design plan were deleted during S5 cleanup. This exception category is now inactive.

**Historical Note:** These were reference documents for the S5 v1 (22 iterations) → S5 v2 (Validation Loop) transition. The files lacked Prerequisites/Exit Criteria by design (not workflow execution guides).

**Audit Action:** No action needed — files do not exist, exception is inactive.

---

### Category C: Optional/Auxiliary Files (4 files)

**Pattern:** Support guides used conditionally or as reference material, not standard sequential workflows

**Design Rationale:**
- Files serve specific auxiliary purposes
- Prerequisites/exit criteria handled inline or not applicable
- Not part of standard epic workflow sequence

**Files:**

15. **stages/s3/s3_parallel_work_sync.md**
    - **Type:** Optional synchronization checklist
    - **When Used:** Only when S2 executed in parallel mode (Primary + Secondary agents)
    - **Skipped:** When S2 done sequentially (single agent)
    - **Prerequisites:** None (conditional usage based on S2 execution mode)
    - **Exit Criteria:** Inline completion verification in Step 0.2 - STATUS file checks
    - **Missing Sections:** Prerequisites (not applicable), Exit Criteria (inline instead)
    - **Design Rationale:** Conditional auxiliary workflow, not standard stage progression
    - **Audit Action:** SKIP - not a standard workflow guide

16. **stages/s4/archive/s4_feature_testing_card.md** *(ARCHIVED — SHAMT-7)*
    - **Type:** Quick reference card / cheat sheet
    - **Status:** Archived. S4 deprecated in SHAMT-6; files moved to archive/ in SHAMT-7.
    - **Audit Action:** SKIP — archived file, not in active guide tree

17. **stages/s4/archive/s4_test_strategy_development.md** *(ARCHIVED — SHAMT-7)*
    - **Type:** Detailed iteration guide (Iterations 1-3)
    - **Status:** Archived. S4 deprecated in SHAMT-6; files moved to archive/ in SHAMT-7.
    - **Audit Action:** SKIP — archived file, not in active guide tree

18. **stages/s4/s4_feature_testing_strategy.md** *(Added — SHAMT-7)*
    - **Type:** Deprecation redirect stub
    - **When Used:** Agents encountering S4 guidance are redirected here
    - **Status:** Active (redirect only — not a workflow guide)
    - **Prerequisites:** Not applicable (redirect stub, not a workflow stage)
    - **Exit Criteria:** Not applicable (redirect stub with "Proceed To" pointer to S5)
    - **Missing Sections:** Prerequisites, Exit Criteria (neither apply to redirect stubs)
    - **Design Rationale:** Redirect stubs exist only to point agents/users to the replacement. Requiring formal Prerequisites/Exit Criteria would add confusing structure to a one-purpose document.
    - **Audit Action:** SKIP — deprecation redirect, not a workflow guide

---

### Category D: Emoji Heading Anchor Patterns

**Purpose:** Documents the correct GFM anchor format for headings that start with emoji.

**Why anchors look "wrong" but are correct:**
GFM (GitHub Flavored Markdown) strips emoji characters during anchor generation. A heading like
`## 🔢 Understanding Gate Numbering` produces anchor `#-understanding-gate-numbering`, NOT
`#🔢-understanding-gate-numbering`. The leading hyphen comes from the space character that
follows the emoji (space → hyphen after stripping the emoji).

**Pattern:** `#-kebab-case-title` is correct for all emoji-prefixed headings.

**🚨 Do NOT "fix" these anchors** — they are already correct. Changing them from `#-name` to
`#emoji-name` is a regression (introduced in Round 12 SR12.3 and reverted in Round 13).

**Verified correct anchors:**

| File | Heading | Correct Anchor | Wrong Form (do not use) |
|------|---------|----------------|------------------------|
| `reference/mandatory_gates.md` | `## 🔢 Understanding Gate Numbering` | `#-understanding-gate-numbering` | `#🔢-understanding-gate-numbering` |
| `stages/s2/s2_feature_deep_dive.md` | `## 🔀 Parallel Work Check (FIRST PRIORITY)` | `#-parallel-work-check-first-priority` | `#🔀-parallel-work-check-first-priority` |
| `stages/s2/s2_feature_deep_dive.md` | `## 📖 Terminology Note` | `#-terminology-note` | `#📖-terminology-note` |
| `stages/s10/s10_epic_cleanup.md` | `## 🚨 MANDATORY READING PROTOCOL` | `#-mandatory-reading-protocol` | `#🚨-mandatory-reading-protocol` |
| `stages/s10/s10_epic_cleanup.md` | `## 🛑 Critical Rules` | `#-critical-rules` | `#🛑-critical-rules` |

**Algorithm (for deriving anchors for new emoji headings):**
1. Take heading text, lowercase it
2. Strip all non-alphanumeric, non-space, non-hyphen characters (including the emoji)
3. Replace spaces with hyphens — the space after the stripped emoji becomes a leading `-`
4. Do not trim leading hyphens — `#-name` is valid

**Related:** See D10 Context-Sensitive Rule 5 for full specification.

---

## Category E: Pre-Audit Script Recurring False Positives

**Purpose:** Documents recurring false positives from `pre_audit_checks.sh` that are not covered by the D12 Prerequisites/Exit Criteria check above. These appear every run and must be excluded from fix counts.

---

### E1: D8 TODO/Placeholder Instances (24 Critical)

**Dimension:** D8 (Documentation Quality)
**Check:** `pre_audit_checks.sh` TODO/placeholder scan
**Every-run count:** 25 critical, ~35 placeholder matches

**Root Cause:** The D8 check scans all of `.shamt/guides/` including the epic workflow stage guides (s1–s10). Those guides intentionally contain TODO/TBD/placeholder text as instructional examples and checklist items — they teach users to avoid placeholders, so they must reference them.

**Affected files:**
- `stages/s1/s1_p3_discovery_phase.md` — mentions "TBD" as example of vague description to avoid
- `stages/s3/s3_epic_planning_approval.md` — checklist item: "no TBD" as acceptance criterion
- `stages/s5/s5_bugfix_workflow.md` — "Bug Fix TODO: Authentication Error" as a template example
- `stages/s5/s5_v2_validation_loop.md` — "no TBD" completeness check
- `stages/s7/s7_p2_qc_rounds.md` — "NO TODOs" as QC requirement (×2 lines)
- `stages/s10/s10_epic_cleanup.md` — "No placeholder text (e.g., 'TODO', '{fill in later}')" as checklist

**Why acceptable:** All occurrences are meta-content: teaching that real work products must not have TODOs. The stage guides themselves have no incomplete sections. The text is definitionally required to describe the standard.

**Action:** When pre_audit_checks.sh reports "TODOs remaining: 25" — this is the expected baseline. Only investigate if the count rises above 25 or if new files appear in the list.

**Note:** Baseline updated from 23 → 24 on 2026-03-07 after confirming `stages/s7/s7_p2_qc_rounds.md` contributes 2 lines (83: "✅ Zero tech debt (no TODOs...)" and 133: "NO TODOs, NO temporary solutions") that are pre-existing meta-content. Updated 24 → 25 on 2026-03-14 after SHAMT-7 audit confirmed `stages/s1/s1_epic_planning.md:533` contributes 1 line (template showing `Integration Test Convention: [TBD — will be set in S5]`) that is instructional placeholder content.

---

### E2: D10 Prerequisite-Content Conflicts (2 Warnings)

**Dimension:** D10 (Prerequisite-Content Consistency)
**Check:** `pre_audit_checks.sh` prerequisite-content conflict scan
**Every-run count:** 2 warnings, always the same file

**Root Cause:** `stages/s2/s2_p2_cross_feature_alignment.md` uses a group-based parallel work pattern where prerequisites define "all features completed S2.P1" but the content describes running on each group after its Group 1 features complete S2.P1. This is correct and intentional — it's a phased parallel execution model, not an inconsistency.

**Affected file:**
- `stages/s2/s2_p2_cross_feature_alignment.md` — appears twice in the conflict list (same file, two different pattern matches)

**Why acceptable:** The prerequisite says "all features in current group completed S2.P1" and the content describes exactly that pattern applied per-group. The check misidentifies the scoping language as a conflict.

**Action:** When pre_audit_checks.sh reports "Found 2 potential prerequisite-content conflicts" pointing at s2_p2_cross_feature_alignment.md — expected baseline. Only investigate if new files appear in the conflict list.

---

---

## Category F: D11 Pre-Existing File Size Exceptions

**Purpose:** Documents stage guide files that exceed the 1250-line D11 baseline but cannot be split within the current SHAMT work scope. These require a dedicated file-splitting SHAMT-N.

**Design Rationale:**
- Both files are primary stage guides that consolidate what used to be multiple smaller files
- They were already over the 1250-line threshold before SHAMT-7 (which added only 4–14 lines each)
- Proper splitting requires creating router files + sub-files + updating all cross-references — a separate refactoring scope

**Files:**

**F1. stages/s1/s1_epic_planning.md (1332 lines)**
- **D11 Status:** Exceeds 1250-line baseline by 82 lines
- **Pre-existing:** Yes — was 1304 lines before SHAMT-9 (P2+P3 added ~28 lines: Step 0, parallel play note, reference card update)
- **Split candidates:** S1.P1–P3 are each large enough to warrant standalone files
- **Why deferred:** Splitting requires updating all "read s1_epic_planning.md" references across the guide tree; out of SHAMT-9 scope
- **Audit Action:** SKIP D11 violation — tracked for future file-splitting SHAMT-N

**F2. stages/s5/s5_v2_validation_loop.md (1392 lines)**
- **D11 Status:** Exceeds 1250-line baseline by 142 lines
- **Pre-existing:** Yes — was 1327 lines before SHAMT-9 (P4 added ~65 lines: Dependency Re-Validation Protocol section)
- **Split candidates:** Phase 1 (Draft), Phase 2 (Validation Loop), dimension reference sections
- **Why deferred:** Splitting requires updating all "read s5_v2_validation_loop.md" references and agent prompts; out of SHAMT-9 scope
- **Audit Action:** SKIP D11 violation — tracked for future file-splitting SHAMT-N

**F3. reference/validation_loop_master_protocol.md (1544 lines)**
- **D11 Status:** Exceeds 1250-line baseline by 294 lines
- **Pre-existing:** Yes — consolidated master protocol predates SHAMT-7; SHAMT-7 did not modify this file
- **Split candidates:** Could be split into protocol core + dimension-specific appendices
- **Why deferred:** This is the central reference document for all validation loop scenarios; splitting requires updating all scenario files (`validation_loop_*.md`) that defer to it; out of SHAMT-7 scope
- **Note:** `pre_audit_checks.sh` does not scan `reference/` for D11, so this exception is for manual audit rounds only
- **Audit Action:** SKIP D11 violation — tracked for future file-splitting SHAMT-N

---

## Category G: D22 Lightweight MRP Exceptions (Router and Optional Guides)

**Purpose:** Documents guides that have lightweight MRP (missing FS block) as an intentional design choice.

**D22 Context:** Dimension 22 (Guide Bypass Risk) requires three enforcement mechanisms: MRP with resumption clause, FORBIDDEN SHORTCUTS block, and phase commitment gates. For router guides and optional conditional guides, FORBIDDEN SHORTCUTS are not applicable because there are no procedural steps that could be skipped — the entire guide IS the routing decision or check.

**Files:**

**G1. stages/s2/s2_feature_deep_dive.md** *(Added SHAMT-11 audit)*
- **Type:** Router guide
- **MRP:** Present (lightweight — added SHAMT-11 audit) with resumption clause
- **FORBIDDEN SHORTCUTS:** Not applicable — guide contains routing decision logic only (parallel work check, phase navigation); no procedural steps to shortcut
- **Audit Action:** PASS D22 — lightweight MRP is the correct pattern for router guides

**G2. stages/s9/s9_epic_final_qc.md** *(Added SHAMT-11 audit)*
- **Type:** Router guide
- **MRP:** Present (lightweight — added SHAMT-11 audit) with resumption clause
- **FORBIDDEN SHORTCUTS:** Not applicable — guide contains routing decision logic only (sub-stage navigation, single-feature shortcut); no procedural steps to shortcut
- **Audit Action:** PASS D22 — lightweight MRP is the correct pattern for router guides

**G3. stages/s3/s3_parallel_work_sync.md** *(Added SHAMT-11 audit)*
- **Type:** Optional conditional guide (only when S2 executed in parallel mode)
- **MRP:** Present (lightweight — added SHAMT-11 audit) with resumption clause
- **FORBIDDEN SHORTCUTS:** Not present — guide is short (265 lines) and has explicit "Skip this" instructions at the top; FS would be redundant
- **Audit Action:** PASS D22 — lightweight MRP sufficient for optional auxiliary guides

**G4. stages/s4/s4_feature_testing_strategy.md** *(Added SHAMT-11 audit)*
- **Type:** Deprecation redirect stub
- **MRP:** Not present — redirect stub only; no workflow steps to read or follow
- **FORBIDDEN SHORTCUTS:** Not applicable — redirect stubs have no procedural steps
- **Design Rationale:** Redirect stubs exist only to point agents to the replacement (stages/s5/s5_v2_validation_loop.md). Requiring MRP/FS would add confusing structure to a one-purpose document.
- **Audit Action:** SKIP D22 — deprecation redirect stub, not a workflow guide

---

## How to Use This Document

### For Future Audits

**When running D8 (Documentation Quality) Prerequisites/Exit Criteria checks:**

1. **Generate violation list** using automated pattern search
2. **Cross-reference with this document** before flagging as issues
3. **Filter out known exceptions** (19 files total — Categories A–D)
4. **Investigate remaining violations** as potential real issues

**When running `pre_audit_checks.sh` and seeing recurring script output:**

- "TODOs remaining: 25" — expected baseline; see Category E1 above
- "Found 2 potential prerequisite-content conflicts" pointing at s2_p2_cross_feature_alignment.md — expected; see Category E2 above
- "⚠️ CLAUDE.md found but no stage references detected" — known script integer-parsing bug (line 370); not a real issue

**Example Audit Workflow:**
```bash
# Step 1: Find files missing Prerequisites
for file in stages/*/*.md; do
  grep -q "^## Prerequisites" "$file" || echo "$file"
done > missing_prereqs.txt

# Step 2: Filter out known exceptions
# Remove lines matching: s5/s5_p1_i3_*, s5/s5_p3_i1_*, s3/s3_parallel_work_sync.md, s4/s4_feature_testing_card.md, s4/s4_test_strategy_development.md
grep -v -E "(s5_p1_i3_|s5_p3_i1_|s3_parallel_work_sync|s4_feature_testing_card|s4_test_strategy_development)" missing_prereqs.txt > real_violations.txt

# Step 3: Investigate remaining files
wc -l real_violations.txt  # Should be low count
```

### For Guide Authors

**When creating new iteration guides in S5:**
- Use inline prerequisites: "**Prerequisites:** Previous iterations complete"
- Rely on parent round guide for exit criteria
- Follow established pattern (see Category A files above)
- File size: Keep focused and lightweight (100-400 lines)

**When creating auxiliary/optional guides:**
- Consider if Prerequisites/Exit Criteria apply
- If guide is conditional or reference material, inline may be appropriate
- Add entry to this document if creating new exception pattern

**When creating standard workflow guides:**
- **DO include formal "## Prerequisites" section** (h2 level)
- **DO include formal "## Exit Criteria" section** (h2 level)
- Exceptions are rare - default to formal sections

---

## Audit History

**Round 2 (2026-02-05):** Identified 34 files missing Prerequisites/Exit Criteria
**Round 3 (2026-02-05):** Investigated all 34 files, categorized as:
- 4 real issues (fixed)
- 30 intentional exceptions (documented here)

**Known Audit Tools:**
- D8 dimension automated checks
- audit/scripts/pre_audit_checks.sh

**Future Updates:**
- Add new exceptions as patterns emerge
- Update category descriptions if design patterns change
- Maintain audit tool compatibility

---

## Summary Statistics

**Total Known Exceptions:** 22 files (historical count)

**Active Exceptions (files that still exist):**
- Category C (Optional/Auxiliary — Prerequisites/Exit Criteria): **2 active files**
  - stages/s3/s3_parallel_work_sync.md (conditional sync guide)
  - stages/s4/s4_feature_testing_strategy.md (deprecation redirect stub)
- Category F (D11 File Size — pre-existing, deferred splitting): **3 active files**
  - stages/s1/s1_epic_planning.md (1332 lines, 82 over 1250 baseline)
  - stages/s5/s5_v2_validation_loop.md (1392 lines, 142 over 1250 baseline)
  - reference/validation_loop_master_protocol.md (1544 lines, 294 over 1250 baseline)
- Category G (D22 Lightweight MRP — Router and Optional Guides): **4 active files**
  - stages/s2/s2_feature_deep_dive.md (router guide — lightweight MRP only, no FS)
  - stages/s9/s9_epic_final_qc.md (router guide — lightweight MRP only, no FS)
  - stages/s3/s3_parallel_work_sync.md (optional conditional — lightweight MRP only, no FS)
  - stages/s4/s4_feature_testing_strategy.md (redirect stub — no MRP or FS)

**Inactive Exceptions (files deleted from filesystem):**
- Category A (S5 Iteration Files): 14 files — DELETED (S5 v1 → v2 migration)
- Category B (S5 Design/Migration Documents): 2 files — DELETED (no longer exist)

**Missing Sections (historical — based on deleted files):**
- Missing Prerequisites only: 5 files (s5 iterations 5, 5a, 6, 6a, 7 with inline statements)
- Missing Exit Criteria only: 3 files (s3_parallel_work_sync, s4_feature_testing_card, s4_test_strategy_development)
- Missing BOTH: 11 files (remaining s5 iteration files + 2 design docs)

**Design Patterns (active only):**
- Optional/Conditional: 1 file (s3_parallel_work_sync)
- Reference Material: 2 files (s4_feature_testing_card, s4_test_strategy_development)
- Router (lightweight MRP): 2 files (s2_feature_deep_dive, s9_epic_final_qc)

---

**Last Verified:** 2026-03-15 (Category G added — D22 lightweight MRP exceptions for router and optional guides; SHAMT-11 audit)
**Next Review:** When new stage/iteration guides added, or if D8/D10/D22 check patterns change

