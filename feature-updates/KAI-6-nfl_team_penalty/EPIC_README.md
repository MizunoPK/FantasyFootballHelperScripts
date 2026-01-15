# Epic: nfl_team_penalty

**Created:** 2026-01-12
**Status:** IN PROGRESS
**Total Features:** 2

---

## 🎯 Quick Reference Card (Always Visible)

**Current Stage:** Stage 2 - Feature Deep Dive
**Active Guide:** `guides_v2/stages/s2/s2_p1_research.md`
**Last Guide Read:** 2026-01-12

**Stage Workflow:**
```
S1 → S2 → S3 → S4 → S5 → S6 → S7 → S8 → S9 → S10
  ↓         ↓         ↓         ↓         ↓         ↓         ↓         ↓         ↓         ↓
Epic    Features  Sanity   Testing   Plan    Impl    Test   Align   Epic     Done
Plan    Deep Dive  Check   Strategy                          QC
```

**You are here:** ➜ Stage 2 (Feature 01 - Research Phase)

**Critical Rules for Current Stage:**
1. Read ENTIRE S2.P1 guide before starting
2. Zero autonomous resolution (ask user for ALL decisions)
3. Update feature README Agent Status after each phase
4. Create spec.md with traceability to epic request
5. Mark ALL unknowns in checklist.md (user must answer)

**Before Proceeding to Next Step:**
- [ ] Read guide: `guides_v2/stages/s2/s2_p1_research.md`
- [ ] Acknowledge critical requirements
- [ ] Verify prerequisites from guide
- [ ] Update feature_01 README Agent Status

---

## Agent Status

**Last Updated:** 2026-01-13
**Current Stage:** Stage 5 - Feature Implementation (Feature 01)
**Current Phase:** IMPLEMENTATION_PLANNING
**Current Step:** Ready to begin S5.P1 Round 1 for Feature 01
**Current Guide:** stages/s5/s5_p1_planning_round1.md
**Guide Last Read:** NOT YET (will read when starting S5.P1 Round 1)

**Critical Rules from Next Guide:**
- Execute 28 verification iterations (Rounds 1-3)
- ONE iteration at a time, IN ORDER (no batching, no skipping)
- Round 1: Iterations 1-7 + Gates 4a, 7a
- Round 2: Iterations 8-16 (>90% test coverage)
- Round 3: Part 1 (Iterations 17-22), Part 2a (23, 23a), Part 2b (25, 24)
- Gate 5: User approval of implementation_plan.md MANDATORY

**Progress:** S1-S4 complete, Gate 4.5 PASSED, starting S5 for Feature 01
**Next Action:** Begin S5.P1 Round 1 for feature_01_config_infrastructure
**Blockers:** None

---

## Epic Overview

**Epic Goal:**
Add NFL team penalty system to Add to Roster mode, allowing users to penalize players from specific NFL teams they want to avoid drafting.

**Epic Scope:**
- Config infrastructure: Add NFL_TEAM_PENALTY (list) and NFL_TEAM_PENALTY_WEIGHT (multiplier) settings
- Score penalty application: Multiply final player scores by penalty weight for penalized teams
- User-specific setting: league_config.json uses actual teams, simulation configs use defaults
- Transparency: Scoring reasons show when penalty is applied
- Validation: Prevent invalid team abbreviations and weight values outside 0.0-1.0 range

**Key Outcomes:**
1. Users can configure team penalty list and weight in league_config.json
2. Players from penalized teams have reduced scores in Add to Roster mode
3. Simulations remain objective (not affected by user's team preferences)
4. System validates config values and provides clear scoring transparency

**Original Request:** `feature-updates/KAI-6-nfl_team_penalty/nfl_team_penalty_notes.txt`

---

## Epic Progress Tracker

**Overall Status:** 0/2 features complete (2/2 S2 complete)

| Feature | S1 | S2 | S3 | S4 | S5 | S6 | S7 | S8.P1 | S8.P2 |
|---------|---------|---------|---------|---------|----------|----------|----------|----------|----------|
| feature_01_config_infrastructure | ✅ | ✅ 2026-01-12 | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ |
| feature_02_score_penalty_application | ✅ | ✅ 2026-01-13 | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ |

**Legend:**
- ✅ = Complete
- ◻️ = Not started or in progress

**S9 - Epic Final QC:** ◻️ NOT STARTED
- Epic smoke testing passed: ◻️
- Epic QC rounds passed: ◻️
- Epic PR review passed: ◻️
- End-to-end validation passed: ◻️
- Date completed: Not complete

**S10 - Epic Cleanup:** ◻️ NOT STARTED
- Final commits made: ◻️
- Epic moved to done/ folder: ◻️
- Date completed: Not complete

---

## Feature Summary

### Feature 01: config_infrastructure
**Folder:** `feature_01_config_infrastructure/`
**Purpose:** Add NFL team penalty configuration settings to ConfigManager and update all config files
**Status:** S1 complete - ready for S2
**Dependencies:** None (first feature)

### Feature 02: score_penalty_application
**Folder:** `feature_02_score_penalty_application/`
**Purpose:** Apply NFL team penalty multiplier to player scores in Add to Roster mode after 10-step algorithm
**Status:** S1 complete - ready for S2
**Dependencies:** Feature 01 (config infrastructure)

---

## Bug Fix Summary

**Bug Fixes Created:** 0

No bug fixes created yet.

---

## Missed Requirements Summary

**Missed Requirements Created:** 0

No missed requirements created yet.

---

## Epic Completion Checklist

**S1 - Epic Planning:**
- [x] Git branch created (`epic/KAI-6`)
- [x] EPIC_TRACKER.md updated
- [x] Epic folder created
- [x] Epic request file moved
- [x] Feature breakdown proposed and approved
- [x] Epic ticket created and validated
- [x] Feature folders created (2 features)
- [x] Core feature files created (README, spec, checklist, lessons_learned per feature)
- [x] Epic-level files created (EPIC_README, test plan, lessons learned)
- [x] research/ folder created
- [x] GUIDE_ANCHOR.md created
- [x] Agent Status updated for S2
- [x] S1 COMPLETE ✅

**S2 - Feature Deep Dives:**
- [x] Feature 01 deep dive complete (2026-01-12)
- [x] Feature 02 deep dive complete (2026-01-13)
- [x] All feature specs complete and validated
- [x] All feature checklists complete
- [x] S2 COMPLETE ✅ (2026-01-13)

**S3 - Cross-Feature Sanity Check:**
- [x] Pairwise feature comparison complete (SANITY_CHECK_2026-01-13.md)
- [x] Conflicts resolved (zero conflicts found)
- [x] User sign-off received (2026-01-13)

**S4 - Epic Testing Strategy:**
- [x] epic_smoke_test_plan.md updated with detailed scenarios (2026-01-13)
  - 10 measurable success criteria
  - 8 specific test scenarios
  - 5 integration points documented
- [x] 🚨 Gate 4.5: User approved test plan ✅ PASSED (2026-01-13)

**S5-S8 - Feature Loop (per feature):**
- [ ] Feature 01: S5 (Planning) → S6 (Implementation) → S7 (Testing) → S8 (Alignment)
- [ ] Feature 02: S5 (Planning) → S6 (Implementation) → S7 (Testing) → S8 (Alignment)

**S9 - Epic Final QC:**
- [ ] Epic smoke testing passed
- [ ] Epic QC rounds passed (3 rounds)
- [ ] User testing passed

**S10 - Epic Cleanup:**
- [ ] All unit tests passing (100%)
- [ ] Guide updates applied (S10.P1)
- [ ] Final commit made
- [ ] PR created and merged
- [ ] EPIC_TRACKER.md updated
- [ ] Epic moved to done/ folder

---

## Notes

**S1 Phase Progress:**
- Phase 1 (Initial Setup): ✅ COMPLETE
- Phase 2 (Epic Analysis): ✅ COMPLETE
- Phase 3 (Feature Breakdown): ✅ COMPLETE (2 features approved)
- Phase 4 (Epic Structure Creation): ✅ COMPLETE
- Phase 5 (Transition to S2): ✅ COMPLETE

**S1 COMPLETE - Ready for S2**
- All epic folder structure created
- All feature folders created with required files
- Epic ticket validated by user
- Agent Status updated for S2 transition
