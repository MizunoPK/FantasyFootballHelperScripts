# Feature 06: historical_data_compiler_logging

**Part of Epic:** KAI-8-logging_refactoring
**Created:** 2026-02-06
**Status:** NOT STARTED

---

## Agent Status

**Last Updated:** 2026-02-08 12:20 (S8.P1 alignment complete)
**Current Stage:** Ready for S4 (Feature Testing Strategy)
**Current Step:** S8.P1 alignment complete, spec updated based on Feature 01 actual implementation
**Current Guide:** Next: `feature-updates/guides_v2/stages/s4/s4_feature_testing_strategy.md`
**Guide Last Read:** S2 guide (2026-02-06)

**Progress Summary:**
- ✅ S2 COMPLETE (spec approved, Gate 3 passed)
- ✅ S3 COMPLETE (epic-level sanity check)
- ✅ S8.P1 COMPLETE (spec aligned with Feature 01 actual implementation - 2026-02-08)
- 🔄 S4 NOT STARTED (awaiting Feature 01 to complete S8.P2, then Features 02-07 start S4)

**S8.P1 Updates Applied:**
- Updated setup_logger() signature (added enable_console, max_file_size, backup_count parameters)
- Updated type hints (Union types for level and log_file_path)
- Updated return type (returns logging.Logger, not None)
- Documented filename formats (initial vs rotated files with microseconds)

**Progress:** Ready for S4 after Feature 01 completes S8.P2
**Next Action:** Wait for Feature 01 to complete S8.P2 (Epic Testing Plan Update)
**Blockers:** None

---

## Feature Overview

**What:** Add --enable-log-file CLI flag to compile_historical_data.py and improve log quality in historical_data_compiler/ modules

**Why:** Enable user control over file logging and improve debugging/awareness for historical data compilation

**Scope:**
- Add --enable-log-file flag to compile_historical_data.py (direct entry)
- Apply DEBUG/INFO quality criteria to historical_data_compiler/ modules
- Review and improve logs in: json_exporter, player_data_fetcher, weekly_snapshot_generator, game_data_fetcher, http_client, schedule_fetcher
- Update affected test assertions

**Dependencies:** Feature 1 (core infrastructure)

**Estimated Size:** SMALL-MEDIUM

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
- logs/historical_data_compiler/ folder structure

**Provides to:**
- End users (CLI flag control over file logging)

---

## Notes

Direct entry script (compile_historical_data.py). Has multiple submodules that may need log quality attention.
