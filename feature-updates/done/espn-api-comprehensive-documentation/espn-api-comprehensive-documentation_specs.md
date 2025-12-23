# ESPN API Comprehensive Documentation

## Objective

Conduct thorough research into ALL ESPN API endpoints used in the Fantasy Football Helper Scripts, map all undocumented stat IDs (40+ total), cross-reference with NFL.com official stats, and create comprehensive, accurate documentation to replace the existing incomplete/inaccurate docs.

**Why:** Recent testing revealed that existing documentation incorrectly stated targets and carries were unavailable in ESPN API, when they actually exist via stat_58 and stat_23. This prevents wasted effort on workarounds and enables accurate feature implementation.

---

## High-Level Requirements

### 1. Comprehensive Endpoint Testing

**Endpoints to Document:**
- Player Stats Endpoint: `GET https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{SEASON}/segments/0/leaguedefaults/{PPR_ID}`
- Scoreboard Endpoint: `GET https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard`
- Team Stats Endpoint: `GET https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{TEAM_ID}/statistics`
- Team Roster Endpoint: `GET https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{TEAM_ID}/roster` (check if exists)

**For Each Endpoint:**
- Test with multiple weeks of data (Weeks 1, 8, 15, 17 for variety)
- Test all 6 positions (QB, RB, WR, TE, K, DST)
- Use statSourceId=0 (actuals only) - projections use same stat IDs
- Document complete response structure
- Save raw responses to JSON files for analysis
- Cross-reference data with NFL.com official stats

### 2. Complete Stat ID Mapping

**Confirmed Stat IDs (from testing 2025-12-22):**
- stat_58 = Targets (WR/TE/RB receiving)
- stat_53 = Receptions (WR/TE/RB)
- stat_42 = Receiving Yards (WR/TE/RB)
- stat_23 = Rushing Attempts/Carries (RB/QB)
- stat_24 = Rushing Yards (RB/QB)

**Unconfirmed Stat IDs (need research):**
- stat_41: Suspected passing completions (QB)
- stat_43-46: Suspected passing stats (QB)
- stat_47-52: Suspected TD scoring types (all positions)
- stat_59-61: Unknown (WR?)
- stat_67-68, 71-73: Unknown (various)
- stat_156, 158, 210, 213: Unknown

**Mapping Strategy:**
1. Cross-reference stat values with NFL.com stats for same player/week
2. Validate consistency across multiple players per position
3. Test across multiple weeks to confirm stability
4. Document confidence level (confirmed, probable, unknown)

### 3. Cross-Reference Validation

**Process:**
1. Query ESPN API for Week 15 actuals (statSourceId=0)
2. Query NFL.com for same player/week
3. Compare stat values to identify stat ID mappings
4. Validate with pattern recognition (e.g., targets >= receptions)

**Validation Criteria:**
- Targets >= Receptions (receiving stats)
- Pass Attempts >= Completions (passing stats)
- Carries > 0 → Yards value makes sense (realistic YPC)

### 4. Documentation Structure

**New Documentation Location:**
```
docs/espn/
├── README.md                      (New authoritative reference)
├── MIGRATION_GUIDE.md             (How to migrate from old docs)
├── endpoints/
│   ├── player_stats.md           (Player stats endpoint)
│   ├── scoreboard.md             (Scoreboard endpoint)
│   ├── team_stats.md             (Team stats endpoint)
│   └── team_roster.md            (If endpoint exists)
├── reference/
│   ├── stat_ids.md               (Complete stat ID reference)
│   ├── team_mappings.md          (Team ID → abbreviation)
│   ├── position_mappings.md      (Position ID → position name)
│   └── response_examples.md      (Full response examples)
└── testing/
    ├── validation_scripts.md     (How to validate stat IDs)
    └── cross_reference.md        (Cross-referencing with NFL.com)
```

**Stat ID Reference Format (for each stat ID):**
- Category (Receiving, Rushing, Passing, etc.)
- Positions that have this stat
- Data type (Integer, Float)
- Typical range
- Validation criteria
- Testing results (% validated)
- Cross-reference sources
- First confirmed date
- Code examples showing how to extract (e.g., `player['stats'][58]  # Targets`)
- **Note:** Historical stability NOT included (difficult to verify without multi-year data)

### 5. Deprecation Strategy

**Old Documentation (mark as deprecated):**
- `docs/espn/espn_player_data.md` → Rename to `DEPRECATED_espn_player_data.md`
- `docs/espn/espn_team_data.md` → Rename to `DEPRECATED_espn_team_data.md`
- `docs/espn/espn_api_endpoints.md` → Rename to `DEPRECATED_espn_api_endpoints.md`

**Deprecation Notice Template:**
```markdown
# ⚠️ DEPRECATED DOCUMENTATION ⚠️

**Deprecation Date:** 2025-12-22
**Replacement:** See `docs/espn/README.md` for current documentation

**Reason for Deprecation:**
This documentation was found to be incomplete and contained inaccuracies. Comprehensive
testing revealed additional stat IDs and endpoint behaviors not documented here.

**What Changed:**
1. Stat IDs 58 (targets) and 23 (carries) were incorrectly documented as unavailable
2. Complete stat ID mapping now available in `docs/espn/reference/stat_ids.md`
3. Validated response structures with real examples
4. Confirmed absence of odds/betting data in scoreboard endpoint

**Migration Guide:**
See `docs/espn/MIGRATION_GUIDE.md` for updating code to use new documentation.
```

### 6. Testing Scripts

**Scripts to Create (located at root level):**

1. `test_espn_api_comprehensive.py` - Master testing script
   - Query all endpoints for multiple weeks (Weeks 1, 8, 15, 17)
   - Test all 6 positions (QB, RB, WR, TE, K, DST)
   - Save raw responses to `raw_responses/` directory as JSON files
   - Extract all stat IDs from responses
   - Generate field documentation
   - **Rate limiting:** sleep(2) between requests to respect ESPN API

2. `validate_stat_ids.py` - Stat ID validation script
   - Cross-reference with NFL.com (manual process, script assists with organization)
   - Validate consistency across players (10 per position)
   - Apply validation criteria (targets >= receptions, reasonable YPC, etc.)
   - Generate validation reports with confidence levels (confirmed/probable/unknown)
   - Track validation rates for each stat ID

3. ~~`cross_reference_nfl.py`~~ - NOT NEEDED
   - Decision: Manual cross-reference only (no automated scraping of NFL.com)

---

## Open Questions (To Be Resolved)

### Research Methodology Questions



### Documentation Organization Questions

4. **Should we document ALL stat IDs even if unknown?** PENDING
   - Option A: Document only confirmed + probable stat IDs
   - Option B: Document all observed stat IDs with confidence levels

5. **How detailed should response examples be?** PENDING
   - Option A: Complete raw JSON responses
   - Option B: Annotated excerpts showing key fields

### Testing Script Questions

6. **Should testing scripts be in main repo or docs?** PENDING
   - Option A: `tests/espn_api/` (main repo)
   - Option B: `docs/espn/testing/scripts/` (with docs)

7. **How should we handle rate limiting for testing?** PENDING
   - Option A: Manual delays between requests
   - Option B: Automatic rate limiting with configurable delays

### Deprecation Timeline Questions

8. **When should old docs be removed entirely?** PENDING
   - Option A: 1 month after new docs are published
   - Option B: 3 months after new docs
   - Option C: 6 months after new docs

---

## Resolved Implementation Details

### Confirmed Stat IDs (2025-12-22)

**stat_58: Targets**
- **Decision:** Confirmed as Targets (100% validation)
- **Reasoning:** Tested on 10 WR, 5 TE, 8 RB; targets always >= receptions
- **Source:** ESPN API stats{} object, statSourceId=0 for actuals
- **Example:** Amon-Ra St. Brown Week 15: stat_58=18, stat_53=14 (18 targets, 14 receptions ✓)

**stat_23: Rushing Attempts (Carries)**
- **Decision:** Confirmed as Carries (100% validation)
- **Reasoning:** Tested on 10 RBs; realistic YPC calculations (1.9-5.7 YPC)
- **Source:** ESPN API stats{} object, statSourceId=0 for actuals
- **Example:** Bijan Robinson Week 15: stat_23=22, stat_24=125 (5.7 YPC ✓)

### Testing Weeks

**Decision:** Test Weeks 1, 8, 15, 17
**Reasoning:**
- Covers early season (Week 1), mid-season (Week 8), late season (Week 15), and final regular season (Week 17)
- Provides seasonal variety to catch edge cases
- 4 weeks is manageable testing scope
- Validates stat ID consistency throughout season
**Implementation:** Query ESPN API for these 4 weeks when running comprehensive test script

### Cross-Reference Sample Size

**Decision:** 10 players per position
**Reasoning:**
- Industry standard for validation testing
- Good balance of confidence and efficiency
- Sufficient sample size to catch inconsistencies
- Already achieved for stat_58 (23 players), stat_23 (10 RBs) from previous testing
**Implementation:** For each new stat ID to validate, test with 10 players of the appropriate position(s)

### Confidence Threshold

**Decision:** 95%+ = confirmed, 70-94% = probable, <70% = unknown
**Reasoning:**
- 95% is industry standard for statistical confidence
- With 10 samples: 95% = 9-10 matches, 70% = 7-8 matches
- Allows for rare edge cases or data timing issues without marking stat ID as uncertain
- Three clear tiers for documentation
**Implementation:**
- **Confirmed:** 9-10 out of 10 players match NFL.com (95-100% validation rate)
- **Probable:** 7-8 out of 10 players match (70-94% validation rate)
- **Unknown:** <7 out of 10 players match (<70% validation rate)

### Unknown Stat IDs Documentation Strategy

**Decision:** Document all observed stat IDs with confidence levels
**Reasoning:**
- Comprehensive documentation shows completeness of research
- Future researchers can build on our work without re-discovering stat IDs
- Clear confidence labeling (Confirmed/Probable/Unknown) prevents confusion
- Transparency is valuable for a research/documentation project
- Users can filter to confirmed/probable if they want only validated stat IDs
**Implementation:**
- Stat ID reference will list ALL observed stat IDs in stats{} responses
- Each stat ID entry includes confidence level badge: [CONFIRMED], [PROBABLE], or [UNKNOWN]
- Unknown stat IDs show: observed positions, data type, typical range, but no validated meaning
- Example: "stat_156: [UNKNOWN] - Observed in WR responses, Integer, range 0-2, meaning unidentified"

### Response Example Detail Level

**Decision:** Save response examples as JSON files, reference them in documentation, include brief annotated excerpts inline
**Reasoning:**
- Keeps documentation files readable and scannable
- Preserves complete raw data for deep analysis
- JSON files can be used directly for testing/validation
- Brief excerpts provide quick reference without leaving the docs
- Separates presentation (markdown) from data (JSON)
**Implementation:**
- Save raw API responses to `raw_responses/` directory (or `docs/espn/examples/` if preferred)
- File naming: `{endpoint}_{week}_{source}.json` (e.g., `player_stats_week15_actuals.json`)
- Documentation includes:
  - Brief annotated excerpts showing key fields (inline in markdown)
  - References to full JSON files for complete structure
  - Example: "See `raw_responses/player_stats_week15_actuals.json` for full response"

### Deprecation Timeline

**Decision:** Remove old documentation files 3 months after new docs are published
**Reasoning:**
- Provides reasonable migration window for users to update
- Deprecation notices will warn users immediately upon access
- 3 months balances cleanup needs with pragmatic user migration time
- Can extend timeline if feedback indicates users need more time
- Avoids long-term repository clutter from outdated documentation
**Implementation:**
- Day 0: Rename old docs to `DEPRECATED_*`, add deprecation notices
- Month 3: Remove deprecated files entirely
- Timeline starts when new documentation is merged to main branch
- Migration guide remains available to help users transition

### NFL.com Cross-Reference Method

**Decision:** Manual cross-reference only (no automated scraping)
**Reasoning:**
- This is an initial research project, not an ongoing monitoring system
- 10 players per stat ID is manageable manually (~30-40 total validations for unknown stat IDs)
- Avoids complexity and maintenance burden of web scraping
- Avoids potential Terms of Service issues with automated NFL.com scraping
- Manual validation provides high confidence through human verification
- Can add automation later if quarterly re-validation becomes necessary
**Implementation:**
- Researcher manually visits NFL.com for each player/week combination
- Records stat values in validation spreadsheet or notes
- Compares ESPN API values against NFL.com values
- Documents match/mismatch for validation rate calculation
- Process documented in `docs/espn/testing/cross_reference.md`

### Validation Criteria

**Decision:** Use standard logical validation rules to catch stat ID mapping errors
**Validation Rules:**
1. **Receiving stats:** Targets >= Receptions >= 0
   - A player cannot catch more passes than they were targeted for
2. **Rushing stats:** Reasonable YPC (yards per carry) in 0-20 range
   - YPC outside this range likely indicates incorrect stat ID mapping
3. **Passing stats:** Attempts >= Completions >= 0
   - Cannot complete more passes than attempted
4. **Scoring stats:** TDs <= Total scores
   - Touchdowns are a subset of all scoring plays
**Reasoning:**
- These are standard logical constraints that catch obvious errors
- Violations indicate either wrong stat ID mapping or data quality issues
- Provides automated sanity checking during validation process
**Implementation:**
- Apply validation rules during cross-reference process
- Flag violations for manual review
- Document in validation reports whether each stat ID passes all applicable criteria

### Edge Case Documentation Strategy

**Decision:** Document edge cases as discovered during normal testing (don't seek them out specifically)
**Reasoning:**
- Primary goal is stat ID mapping, not comprehensive edge case documentation
- Seeking out edge cases adds significant scope (bye weeks, injuries, etc.)
- Edge cases encountered during normal testing are still valuable to document
- Keeps project focused and manageable
- Comprehensive edge case testing can be added later if needed
**Implementation:**
- Focus testing on normal scenarios (active players with stats)
- When edge cases are encountered, document the behavior:
  - **Missing stat IDs:** Document as "Not applicable for this position/situation"
  - **Week-to-week differences:** Note if stat ID structure changes between weeks
  - **Bye weeks:** If encountered, document how stats are represented
  - **Injured players (DNP):** If encountered, document how OUT/IR players appear
- Add edge case notes to relevant documentation sections
- Don't create specific test cases to trigger edge conditions

### Testing Methodology

**Cross-Reference Process:**
1. Query ESPN API for Week 15 actuals (statSourceId=0)
2. Extract stat values from stats{} object
3. Compare with known NFL stats (e.g., ESPN shows 18 targets, NFL.com confirms 18 targets)
4. Validate pattern (targets >= receptions)
5. Mark as confirmed if 95%+ validation rate

### Data Storage

**Raw Responses:**
- Location: `raw_responses/` directory (to be created)
- Format: JSON files with naming convention `{endpoint}_{week}_{source}.json`
- Examples:
  - `player_stats_week15_actuals.json`
  - `scoreboard_week16.json`
  - `team_stats_KC.json`

---

## Implementation Notes

### Files to Create

**Documentation Files (10 files):**
1. `docs/espn/README.md`
2. `docs/espn/MIGRATION_GUIDE.md`
3. `docs/espn/endpoints/player_stats.md`
4. `docs/espn/endpoints/scoreboard.md`
5. `docs/espn/endpoints/team_stats.md`
6. `docs/espn/reference/stat_ids.md`
7. `docs/espn/reference/team_mappings.md`
8. `docs/espn/reference/position_mappings.md`
9. `docs/espn/testing/validation_scripts.md`
10. `docs/espn/testing/cross_reference.md`

**Testing Scripts (2 files, located at root level):**
1. `test_espn_api_comprehensive.py` - Master testing script
2. `validate_stat_ids.py` - Stat ID validation script
3. ~~`cross_reference_nfl.py`~~ - NOT NEEDED (manual cross-reference only)

### Files to Modify

**Deprecate Old Docs (3 files):**
1. `docs/espn/espn_player_data.md` → Rename + add deprecation notice
2. `docs/espn/espn_team_data.md` → Rename + add deprecation notice
3. `docs/espn/espn_api_endpoints.md` → Rename + add deprecation notice

### Dependencies

- `httpx` - HTTP client (already in use)
- `pandas` - Data analysis (already in use)
- `beautifulsoup4` - For NFL.com scraping (if automated cross-reference)

### Reusable Code

- Existing ESPN API client code in `player-data-fetcher/espn_client.py`
- Existing test scripts: `test_espn_api_data_availability.py`, `test_stat_id_mapping.py`

### Testing Strategy

**Validation Approach:**
1. Run comprehensive test script for multiple weeks
2. Cross-reference 20+ players with NFL.com
3. Validate pattern consistency across positions
4. Document confidence levels for each stat ID
5. Run validation quarterly to ensure stat IDs remain stable

**Acceptance Criteria:**
- **Stat ID Coverage:** 80%+ of all observed stat IDs identified and validated
- **Core Stats Coverage:** 100% of receiving/rushing/passing core stats documented
- **Cross-Reference Validation:** 20+ players cross-referenced successfully with NFL.com
- **Validation Rate:** 95%+ validation rate for confirmed stat IDs
- **Position Coverage:** All 6 positions tested (QB, RB, WR, TE, K, DST)
- **Testing Quality:** All examples tested with real API responses

**Ongoing Validation Strategy:**
- **Quarterly Validation:** Re-validate stat IDs every 3 months to ensure ESPN hasn't changed API
- **Season Start Validation:** Full re-validation at the start of each NFL season
- **Process:** Run validation scripts, check for new stat IDs, verify existing mappings still accurate
- **Documentation Updates:** Update docs if stat IDs change or new ones are discovered

---

## Status: PLANNING - PHASE 1 COMPLETE (README, SPECS CREATED)

Next: Create checklist and lessons_learned files, then begin Phase 2 investigation
