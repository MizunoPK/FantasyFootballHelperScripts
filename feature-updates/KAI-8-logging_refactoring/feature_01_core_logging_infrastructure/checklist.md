# Feature Checklist: core_logging_infrastructure

**Part of Epic:** KAI-8-logging_refactoring
**Feature Number:** 01
**Created:** 2026-02-06
**Last Updated:** 2026-02-06

---

## Purpose

This checklist tracks questions and user decisions needed to finalize the feature specification. All items must be marked ANSWERED before proceeding to S2.P1.I3 (Refinement & Gate 3).

**CRITICAL:** Agent must NEVER mark items [x] or RESOLVED autonomously. Only after user explicitly approves can items be marked complete.

---

## Functional Questions

### [x] Q1: Backward Compatibility - max_file_size and backup_count Parameters

**Status:** RESOLVED

**Context:**
Current `setup_logger()` signature includes `max_file_size` and `backup_count` parameters for `RotatingFileHandler`. With `LineBasedRotatingHandler`, these parameters become unused (handler uses max_lines=500 and max_files=50 instead).

**Options:**
- **Option A (Recommended):** Keep parameters in signature (accepted but ignored) - No breaking changes
- **Option B:** Remove parameters from signature - Clean API but breaks existing callers

**Question:** Should we keep max_file_size and backup_count parameters for backward compatibility?

**Agent Recommendation:** Option A (keep parameters) - prevents breaking existing code

**User Answer:** Option A - Keep parameters for backward compatibility

---

## Technical Questions

### [x] Q2: Configurability - max_lines and max_files

**Status:** RESOLVED

**Context:**
Epic specifies "500-line cap" and "max 50 logs" as exact requirements. Current spec hardcodes these values (not configurable per-call).

**Options:**
- **Option A (Recommended):** Hardcode 500/50 - Simpler, matches epic requirements
- **Option B:** Add parameters to setup_logger() - Flexible but over-engineered

**Question:** Should max_lines (500) and max_files (50) be hardcoded constants or configurable?

**Agent Recommendation:** Option A (hardcode) - user specified exact values, no configurability mentioned

**User Answer:** Option A - Hardcode 500/50 as constants

---

### [x] Q3: Timestamp Collision Handling

**Status:** RESOLVED

**Context:**
If rotation occurs twice within the same second, second rotation creates duplicate filename. Current spec uses `mode='a'` (append), merging both rotations into one file.

**Options:**
- **Option A (Recommended):** Append to existing file (prevents data loss, file may have >500 lines)
- **Option B:** Add milliseconds to timestamp (YYYYMMDD_HHMMSS_fff format)
- **Option C:** Overwrite existing file (data loss on collision)

**Question:** How should we handle timestamp collisions (rotation within same second)?

**Agent Recommendation:** Option A (append) - prevents data loss, collision rare

**User Answer:** Option A - Append to existing file (prevents data loss)

---

## Integration Questions

### [x] Q4: Logger Name Validation

**Status:** RESOLVED

**Context:**
Logger name is used for folder structure (`logs/{logger_name}/`). If name contains path separators (e.g., "../evil"), files could be created outside logs/ folder.

**Options:**
- **Option A (Recommended):** No validation (trust callers, document requirement)
- **Option B:** Sanitize logger name (strip invalid chars)
- **Option C:** Validate and raise ValueError if invalid

**Question:** Should we validate logger names to prevent directory traversal?

**Agent Recommendation:** Option A (no validation) - trust internal code, document requirement in Features 2-7

**User Answer:** Option A - No validation, trust internal callers, document requirement

---

### [x] Q5: .gitignore Entry Placement

**Status:** RESOLVED

**Context:**
Need to add `logs/` entry to `.gitignore`. Current file has `*.log` at line 70.

**Options:**
- **Option A (Recommended):** After `*.log` pattern (line 71) - logical grouping
- **Option B:** Project-specific section (line 6) - groups with other project entries

**Question:** Where should we add `logs/` entry in .gitignore?

**Agent Recommendation:** Option A (after *.log) - logical grouping

**User Answer:** Option A - Add after *.log pattern (line 71)

---

## Error Handling Questions

### [x] Q6: Empty Logger Name Handling

**Status:** RESOLVED

**Context:**
If caller passes empty string (`setup_logger("", ...)`), folder becomes `logs//`.

**Options:**
- **Option A (Recommended):** Trust callers (document requirement) - unlikely edge case
- **Option B:** Validate and raise ValueError

**Question:** Should we handle empty logger name as edge case or trust callers?

**Agent Recommendation:** Option A (trust callers) - internal code unlikely to pass empty string

**User Answer:** Option A - Trust callers, no validation for empty names

---

### [x] Q7: Extremely Long Logger Names

**Status:** RESOLVED

**Context:**
Filesystem filename limits (255 characters). Very long logger names may exceed limit.

**Options:**
- **Option A (Recommended):** Trust callers (document recommendation: <50 chars)
- **Option B:** Truncate logger names at 50 characters

**Question:** Should we truncate long logger names or trust callers to use reasonable lengths?

**Agent Recommendation:** Option A (trust callers) - realistic script names won't hit limit

**User Answer:** Option A - Trust callers, document <50 char recommendation

---

## Testing Questions

### [x] Q8: Test Coverage for Edge Cases

**Status:** RESOLVED

**Context:**
Spec includes edge cases (timestamp collision, folder deletion, permission denied).

**Options:**
- **Option A:** Comprehensive edge case tests (timestamp collision, folder deletion, permissions)
- **Option B (Recommended):** Happy path + critical errors only (faster tests, focused coverage)

**Question:** What level of edge case test coverage do you want?

**Agent Recommendation:** Option B (happy path + critical) - edge cases documented but rare

**User Answer:** Option B - Focus on happy path + critical errors, skip rare edge cases

---

## Design Clarifications

### [x] DC1: Script Name Consistency Enforcement

**Status:** RESOLVED

**Context:**
Folder structure uses logger name for subfolders. Scripts must use consistent names (e.g., "league_helper" not "LeagueHelper").

**Question:** Document requirement in Features 2-7, or enforce in Feature 1?

**Agent Recommendation:** Document in Features 2-7 - script responsibility

**User Answer:** Confirmed - Document in Features 2-7 (script responsibility, no enforcement in Feature 1)

---

### [x] DC2: Cross-Platform Path Handling

**Status:** RESOLVED

**Context:**
Spec uses `pathlib.Path` for cross-platform compatibility (Windows `\` vs Unix `/`).

**Question:** Confirm pathlib.Path is sufficient (no explicit separator handling needed)?

**Agent Recommendation:** Yes - pathlib.Path handles platform differences automatically

**User Answer:** Confirmed - pathlib.Path is sufficient for cross-platform compatibility

---

### [x] DC3: Cleanup Performance Optimization

**Status:** RESOLVED

**Context:**
High-frequency rotation (>50/second) runs cleanup 50 times/second. Each cleanup scans folder.

**Question:** Is this performance scenario realistic? Should we optimize cleanup (cache file list)?

**Agent Recommendation:** No optimization - unrealistic for fantasy football scripts

**User Answer:** Confirmed - No optimization needed (unrealistic scenario for our use case)

---

## Summary

**Total Questions:** 11
**Answered:** 11/11
**Remaining:** 0

**Status:** ✅ ALL QUESTIONS RESOLVED - Gate 3 Approved

**Breakdown:**
- Functional: 1
- Technical: 2
- Integration: 2
- Error Handling: 2
- Testing: 1
- Design Clarifications: 3

---

## Status Progression Protocol

**Agent follows "Correct Status Progression" protocol:**

1. Agent asks question → Status: OPEN
2. Agent investigates (if needed) → Status: PENDING
3. User provides answer → Status: ANSWERED
4. User approves spec (Gate 3) → Agent marks [x] and RESOLVED

**DO NOT mark [x] or RESOLVED until Gate 3 approval!**

---

## User Approval

**User Status:** ✅ APPROVED
**Approved:** 2026-02-06
**Gate 3:** PASSED - Spec and checklist approved by user
