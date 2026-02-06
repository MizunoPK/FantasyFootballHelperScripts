# Feature 02: league_helper_logging

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
**Next Action:** Begin S2.P1 (Research Phase) after Feature 1 complete
**Blockers:** None (will depend on Feature 1 being implemented first)

---

## Feature Overview

**What:** Add --enable-log-file CLI flag to run_league_helper.py and improve log quality in league_helper/ modules

**Why:** Enable user control over file logging and improve debugging/awareness for league helper functionality

**Scope:**
- Add --enable-log-file flag to run_league_helper.py (subprocess wrapper)
- Forward flag using sys.argv[1:] to league_helper.py
- Apply DEBUG/INFO quality criteria to league_helper/ modules
- Review shared utilities: PlayerManager, ConfigManager, TeamDataManager, DraftedRosterManager, csv_utils, data_file_manager
- Update affected test assertions

**Dependencies:** Feature 1 (core infrastructure)

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

**Consumes from Feature 1:**
- LineBasedRotatingHandler class
- Modified setup_logger() with enable_log_file parameter
- logs/league_helper/ folder structure

**Provides to:**
- End users (CLI flag control over file logging)

---

## Notes

League helper has the most modules and shared utilities - log quality improvements may be substantial. Subprocess wrapper requires sys.argv[1:] forwarding pattern.
