# Feature 01: core_logging_infrastructure

**Part of Epic:** KAI-8-logging_refactoring
**Created:** 2026-02-06
**Status:** NOT STARTED

---

## Agent Status

**Last Updated:** 2026-02-06
**Current Phase:** SETUP
**Current Step:** Feature folder created in S1
**Current Guide:** stages/s1/s1_epic_planning.md
**Guide Last Read:** 2026-02-06 20:05

**Critical Rules from Current Stage:**
- Feature folders created in S1, specs completed in S2
- Discovery Context seeded in spec.md
- User approval required before S5 implementation
- 100% test pass rate required before commits

**Progress:** Feature folder created, waiting for S2 (Feature Deep Dive)
**Next Action:** Begin S2.P1 (Research Phase) after S1 complete
**Blockers:** None

---

## Feature Overview

**What:** Custom LineBasedRotatingHandler, centralized logs/ folder structure, 500-line rotation, max 50 files cleanup, .gitignore update

**Why:** Provides foundation for all script-specific logging features

**Scope:**
- Custom LineBasedRotatingHandler (subclass logging.FileHandler)
- LoggingManager.py integration (modify setup_logger())
- logs/{script_name}/ folder structure with auto-creation
- Timestamped filenames: {script_name}-{YYYYMMDD_HHMMSS}.log
- 500-line rotation with eager counter
- Max 50 files per subfolder with oldest-file deletion
- .gitignore update to exclude logs/ folder
- Unit tests for new handler

**Dependencies:** None (foundation feature)

**Estimated Size:** MEDIUM

---

## Progress Tracker

**S2 - Feature Deep Dive:** Not started
**S3 - Cross-Feature Sanity Check:** Not started
**S4 - Epic Testing Strategy:** Not started
**S5 - Implementation Planning:** Not started
**S6 - Implementation Execution:** Not started
**S7 - Post-Implementation:** Not started
**S8 - Cross-Feature Alignment:** Not started

---

## Feature Files

- [x] README.md (this file)
- [x] spec.md (seeded with Discovery Context)
- [x] checklist.md (empty until S2)
- [x] lessons_learned.md (empty until S2)
- [ ] test_strategy.md (created in S4)
- [ ] implementation_plan.md (created in S5)
- [ ] implementation_checklist.md (created in S6)

---

## Key Decisions

{To be populated during S2 deep dive}

---

## Integration Points

**Provides to Features 2-7:**
- LineBasedRotatingHandler class
- Modified setup_logger() with enable_log_file parameter
- Centralized logs/ folder structure

**Consumes from:**
- None (foundation feature)

---

## Notes

This is the foundation feature that all other features depend on. Must be completed first in implementation order.
