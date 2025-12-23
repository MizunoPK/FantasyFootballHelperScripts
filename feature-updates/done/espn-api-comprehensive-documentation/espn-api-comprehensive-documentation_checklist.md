# ESPN API Comprehensive Documentation - Requirements Checklist

> **IMPORTANT**: When marking items as resolved, also update `espn-api-comprehensive-documentation_specs.md`
> with full implementation details. The checklist tracks status; the specs file is
> the implementation specification.

---

## General Decisions

- [x] **Testing weeks selection:** Weeks 1, 8, 15, 17 (covers early/mid/late/final regular season)
- [x] **Cross-reference sample size:** 10 players per position (industry standard, good balance)
- [x] **Confidence threshold:** 95%+ = confirmed, 70-94% = probable, <70% = unknown
- [x] **Unknown stat IDs:** Document all observed stat IDs with confidence levels (comprehensive transparency)

---

## Research Methodology

- [x] **Endpoint testing coverage:** Test all identified endpoints (player stats, scoreboard, team stats, + check if roster exists) ✓
- [x] **Multi-week testing:** Test Weeks 1, 8, 15, 17 for variety ✓
- [x] **Position coverage:** Test stat IDs across ALL positions (QB, RB, WR, TE, K, DST) ✓
- [x] **Source ID testing:** Test actuals only (statSourceId=0) - projections use same stat IDs ✓

---

## Stat ID Mapping

### Confirmed Stat IDs (Ready to Document)

| Stat ID | Metric | Positions | Validation |
|---------|--------|-----------|------------|
| 58 | Targets | WR, TE, RB | [x] 100% (23/23 players) |
| 53 | Receptions | WR, TE, RB | [x] 100% (23/23 players) |
| 42 | Receiving Yards | WR, TE, RB | [x] 100% (23/23 players) |
| 23 | Rushing Attempts | RB, QB | [x] 100% (10/10 RBs) |
| 24 | Rushing Yards | RB, QB | [x] 100% (10/10 RBs) |

### Stat IDs Needing Research

**Passing Stats (QB):**
- [ ] **stat_41:** Suspected completions - need validation
- [ ] **stat_43:** Suspected passing TDs - need validation
- [ ] **stat_44-46:** Unknown passing stats - need identification

**Scoring Breakdown:**
- [ ] **stat_47-52:** Suspected TD scoring types - need validation
  - Question: Do these differentiate rushing TD vs receiving TD vs passing TD?

**Additional Stats:**
- [ ] **stat_59-61:** Unknown - appear for WRs in testing
- [ ] **stat_67-68:** Unknown - appear for WRs in testing
- [ ] **stat_71-73:** Unknown - appear for WRs in testing
- [ ] **stat_156, 158, 210, 213:** Unknown - scattered appearances

**Kicker Stats:**
- [ ] **FG attempts stat ID:** Not yet identified
- [ ] **FG made stat ID:** Not yet identified
- [ ] **FG by distance stat IDs:** 0-39, 40-49, 50+ (likely 3 separate stat IDs)
- [ ] **XP attempts stat ID:** Not yet identified
- [ ] **XP made stat ID:** Not yet identified

**Defensive Stats (DST):**
- [ ] **Sacks stat ID:** Not yet identified
- [ ] **Interceptions stat ID:** Not yet identified
- [ ] **Fumble recoveries stat ID:** Not yet identified
- [ ] **Defensive TDs stat ID:** Not yet identified
- [ ] **Points allowed stat ID:** Not yet identified

---

## Documentation Structure

### New Documentation Files

- [ ] **docs/espn/README.md:** Main authoritative reference
- [ ] **docs/espn/MIGRATION_GUIDE.md:** Migration from old docs
- [ ] **docs/espn/endpoints/player_stats.md:** Player stats endpoint
- [ ] **docs/espn/endpoints/scoreboard.md:** Scoreboard endpoint
- [ ] **docs/espn/endpoints/team_stats.md:** Team stats endpoint
- [ ] **docs/espn/endpoints/team_roster.md:** (If endpoint exists)
- [ ] **docs/espn/reference/stat_ids.md:** Complete stat ID reference
- [ ] **docs/espn/reference/team_mappings.md:** Team ID mappings
- [ ] **docs/espn/reference/position_mappings.md:** Position ID mappings
- [ ] **docs/espn/reference/response_examples.md:** Response examples

### Testing Documentation

- [ ] **docs/espn/testing/validation_scripts.md:** Validation methodology
- [ ] **docs/espn/testing/cross_reference.md:** Cross-referencing guide

---

## Testing Scripts

### Scripts to Create

- [ ] **test_espn_api_comprehensive.py:** Master testing script
  - [ ] Query all endpoints for multiple weeks
  - [ ] Save raw responses to raw_responses/
  - [ ] Extract all stat IDs from responses
  - [ ] Generate field documentation

- [ ] **validate_stat_ids.py:** Stat ID validation script
  - [ ] Cross-reference with NFL.com
  - [ ] Validate consistency across players
  - [ ] Generate validation reports

- [ ] **cross_reference_nfl.py:** ~~NFL.com cross-reference script~~ NOT NEEDED
  - Decision: Manual cross-reference only (resolved in Question 8)

### Script Location Decision

- [x] **Where should testing scripts live?**
  - ✓ Root level (e.g., `test_espn_api_comprehensive.py`)
  - Consistent with existing root scripts pattern
  - Easy to find and execute

### Rate Limiting Strategy

- [x] **How to handle rate limiting?**
  - ✓ Manual delays (sleep(2) between requests)
  - Simple, predictable, respectful of ESPN API
  - Can adjust if rate limiting occurs

---

## Documentation Content Decisions

### Response Example Detail Level

- [x] **How detailed should response examples be?**
  - ✓ Save response examples to JSON files (in `raw_responses/` or similar)
  - ✓ Reference JSON files in documentation
  - ✓ Include brief annotated excerpts inline in reports

### Stat ID Documentation Format

- [x] **What to include for each stat ID?**
  - [x] Category (Receiving, Rushing, Passing, etc.)
  - [x] Positions that have this stat
  - [x] Data type (Integer, Float)
  - [x] Typical range
  - [x] Validation criteria
  - [x] Testing results (% validated)
  - [x] Cross-reference sources
  - [x] First confirmed date
  - [x] Code examples showing how to extract (YES - include)
  - [x] Historical stability (NO - not included, hard to verify)

### Unknown Stat IDs

- [x] **Document unknown stat IDs?** ✓ DUPLICATE - Already resolved in General Decisions
  - Decision: Document all observed stat IDs with confidence levels (Question 4)

---

## Deprecation Strategy

### Old Documentation Files

- [ ] **Rename old docs to DEPRECATED_*:**
  - [ ] espn_player_data.md → DEPRECATED_espn_player_data.md
  - [ ] espn_team_data.md → DEPRECATED_espn_team_data.md
  - [ ] espn_api_endpoints.md → DEPRECATED_espn_api_endpoints.md

- [ ] **Add deprecation notices to old docs**
- [ ] **Update all internal references to point to new docs**

### Deprecation Timeline

- [x] **When to remove old docs entirely?**
  - ✓ 3 months after new docs published
  - Provides reasonable migration window while avoiding long-term clutter

---

## Cross-Reference Validation

### NFL.com Cross-Reference Process

- [x] **Manual vs Automated:**
  - ✓ Manual cross-reference (check NFL.com, record values)
  - Avoids web scraping complexity, suitable for initial research project
  - Can add automation later if quarterly re-validation is needed

- [x] **Sample size per stat ID:**
  - ✓ 10 players per position (already resolved in General Decisions)
  - Sufficient for 95% confidence threshold

### Validation Criteria

- [x] **Receiving stats:** Targets >= Receptions >= 0 ✓
- [x] **Rushing stats:** Reasonable YPC (0-20 range) ✓
- [x] **Passing stats:** Attempts >= Completions >= 0 ✓
- [x] **Scoring stats:** TDs <= Total scores ✓

---

## Edge Cases & Error Handling

- [x] **Edge case documentation approach:**
  - ✓ Document edge cases as discovered during normal testing
  - Don't seek out edge cases specifically (keeps scope manageable)
  - Focus testing effort on primary goal (stat ID mapping)
  - Note behaviors when encountered:
    - Missing stat IDs: Document as "Not applicable for this position/situation"
    - Week 1 vs Week 17 differences: Note if structure changes
    - Bye weeks: Document representation if encountered
    - Injured players (DNP): Document representation if encountered

---

## Testing & Validation

### Validation Metrics

- [x] **Target stat ID coverage:**
  - ✓ Goal: 80%+ of all stat IDs identified
  - ✓ Goal: 100% of core stats (receiving, rushing, passing) documented

- [x] **Cross-reference validation:**
  - ✓ Goal: 20+ players cross-referenced with NFL.com
  - ✓ Goal: 95%+ validation rate for confirmed stat IDs

- [x] **Position coverage:**
  - ✓ Goal: All 6 positions tested (QB, RB, WR, TE, K, DST)

### Ongoing Validation

- [x] **How often to re-validate stat IDs?**
  - ✓ Quarterly validation to ensure stat IDs remain stable
  - ✓ Full re-validation at start of each season

---

## Data Source Summary

| Data | Source | Status |
|------|--------|--------|
| Player stats | ESPN Fantasy API | ✓ Tested |
| Scoreboard | ESPN Scoreboard API | ✓ Tested (no odds data confirmed) |
| Team stats | ESPN Team Stats API | Pending |
| Team roster | ESPN API (unknown endpoint) | Pending (may not exist) |
| Cross-reference validation | NFL.com | Manual process |

---

## Resolution Log

| Item | Resolution | Date |
|------|------------|------|
| Targets (stat_58) | Confirmed via testing | 2025-12-22 |
| Carries (stat_23) | Confirmed via testing | 2025-12-22 |
| Vegas lines availability | Confirmed NOT in ESPN API | 2025-12-22 |
| Testing weeks selection | Weeks 1, 8, 15, 17 (early/mid/late/final regular season) | 2025-12-22 |
| Cross-reference sample size | 10 players per position (industry standard) | 2025-12-22 |
| Confidence threshold | 95%+ = confirmed, 70-94% = probable, <70% = unknown | 2025-12-22 |
| Unknown stat IDs documentation | Document all observed stat IDs with confidence levels | 2025-12-22 |
| Response example detail level | Save as JSON files, reference in docs, brief annotated excerpts inline | 2025-12-22 |
| Stat ID documentation format | Include code examples, exclude historical stability | 2025-12-22 |
| Deprecation timeline | Remove old docs 3 months after new docs published | 2025-12-22 |
| NFL.com cross-reference method | Manual cross-reference (no automated scraping) | 2025-12-22 |
| Validation criteria | Approved receiving/rushing/passing/scoring validation rules | 2025-12-22 |
| Edge case documentation | Document as discovered during normal testing (don't seek out) | 2025-12-22 |
| Validation metrics | 80%+ stat ID coverage, 100% core stats, 20+ players, all positions | 2025-12-22 |
| Ongoing validation frequency | Quarterly validation, full re-validation at season start | 2025-12-22 |
| Endpoint testing coverage | Test all 4 endpoints (player stats, scoreboard, team stats, check roster) | 2025-12-22 |
| Source ID testing | Test actuals only (statSourceId=0), projections use same IDs | 2025-12-22 |
| Testing script location | Root level (consistent with run_*.py pattern) | 2025-12-22 |
| Rate limiting strategy | Manual delays (sleep(2) between requests) | 2025-12-22 |

---

## Progress Tracking

**Stat ID Mapping Progress:**
- Confirmed: 5 stat IDs (receiving, rushing core stats)
- Probable: 0 stat IDs
- Needs Research: 30+ stat IDs

**Documentation Progress:**
- Files Created: 0/10 (0%)
- Old Docs Deprecated: 0/3 (0%)
- Testing Scripts Created: 0/3 (0%)

**Phase Status:** PLANNING - Phase 1 complete, Phase 2 (investigation) next
