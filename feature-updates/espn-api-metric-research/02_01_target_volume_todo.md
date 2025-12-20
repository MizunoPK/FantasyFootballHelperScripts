# ESPN API Metric Research - Phase 2.1: Target Volume/Share

**Sub-Feature:** Metric 1 - Target Volume/Share Research
**Created:** 2025-12-20
**Status:** Pre-Implementation (Starting 24 verification iterations)

---

## Purpose

Research Metric 1 (Target Volume/Share) to determine:
1. Can we calculate from existing data?
2. Is it available via ESPN API?
3. What free alternatives exist? (minimum 2-3)
4. **Historical data availability** (CRITICAL)
5. Implementation complexity
6. Recommendation (pursue/defer/skip)

**Why HIGH Priority:** Critical for weekly WR/TE/RB decisions - target volume is a key predictor of fantasy performance.

---

## Iteration Progress Tracker

**First Round (7 iterations):**
- [x] 1. Files & Patterns - Identified data files to check, ESPN API docs, free sources
- [x] 2. Error Handling - N/A (research only, no code)
- [x] 3. Integration Points - Output doc integrates with implementation phase
- [x] 4. Algorithm Traceability Matrix - N/A (no algorithms)
- [x] 5. End-to-End Data Flow - Mapped research workflow
- [x] 6. Skeptical Re-verification - Verified metric 1 definition in scoring_gap_analysis.md
- [x] 7. Integration Gap Check - Research doc standalone, no callers

**Second Round (9 iterations):**
- [x] 8. Answer Integration - N/A (no questions file)
- [x] 9. Answer Verification - Verified research tasks cover all 7 template sections
- [x] 10. Dependency Check - Depends on TEMPLATE.md, scoring_gap_analysis.md
- [x] 11. Algorithm Re-verify - N/A (no algorithms)
- [x] 12. Data Flow Re-trace - Confirmed research → document → tracker update flow
- [x] 13. Assumption Re-check - Assumes target data exists somewhere (will verify)
- [x] 14. Caller Re-check - N/A (documentation)
- [x] 15. Final Preparation - Research tasks detailed and ready
- [x] 16. Integration Checklist - Verified TEMPLATE.md and tracker available

**Third Round (8 iterations):**
- [x] 17. Fresh Eyes #1 - Re-read metric 1 definition: targets = QB pass attempts to player
- [x] 18. Fresh Eyes #2 - Target share = player targets / team total targets
- [x] 19. Algorithm Deep Dive - N/A (research only)
- [x] 20. Edge Cases - RBs have lower targets, TEs vary widely, slot WRs high volume
- [x] 21. Test Planning - No tests (research doc, not code)
- [x] 22. Final Assumption Check - Target data is standard NFL stat (should be available)
- [x] 23. Final Caller Check - N/A (standalone doc)
- [x] 24. Readiness Check - READY to begin research

---

## Metric Details (from scoring_gap_analysis.md)

**Metric Number:** 1
**Name:** Target Volume / Target Share
**Position Applicability:** WR, TE, RB (receiving)
**Priority:** HIGH

**Description:** Number of times a player is targeted by the QB (volume) and percentage of team targets (share)

**Why Important:**
- Volume = opportunity
- High target share = locked-in role
- Predicts weekly floor and ceiling

**Current System Coverage:** Not currently tracked in scoring algorithm

---

## Research Tasks

### Task 1: Check Existing Data
**Files to examine:**
- `data/players.csv` - Check for target-related columns
- `data/players_projected.csv` - Check for projected targets
- `simulation/sim_data/{YEAR}/weeks/week_{NN}/players.csv` - Historical target data

**Questions:**
- Do we have target counts in any existing files?
- Do we have target share percentages?
- Is this data weekly or season-level?

### Task 2: ESPN API Research
**Documentation to review:**
- `docs/espn/espn_player_data.md` - Player data fields
- ESPN API stat IDs list (if available)

**Questions:**
- Does ESPN API provide target counts?
- Is target share calculated or provided directly?
- What stat ID represents targets?
- Is this available for historical seasons?

### Task 3: Free Alternatives Research
**Sources to investigate (minimum 2-3):**
1. **Pro Football Reference**
   - URL: https://www.pro-football-reference.com/
   - Check: Weekly target data exportable?
   - Historical: How far back does data go?

2. **NFL Official Stats API**
   - Check: Public access to target data?
   - Format: JSON/CSV?

3. **FantasyPros / Sleeper / Other**
   - Identify other free sources with target data

**For each source, document:**
- Data availability (targets/target share)
- Update frequency
- Free tier limits
- Historical data availability
- Data quality

### Task 4: Historical Data Assessment
**Critical questions:**
- Can we get weekly target data for 2021, 2022, 2024?
- Does the data represent "what we knew going INTO that week"?
- Can we obtain both actuals (weeks 1-N) and projections (weeks N+1 onwards)?

**Test with sample:**
- Pick week 5 of 2024
- Verify data shows: actuals for weeks 1-4, projections for weeks 5-17

### Task 5: Implementation Complexity
**Assess:**
- If existing data: Just need calculation logic (EASY)
- If ESPN API: Need to identify stat ID and integrate (MEDIUM)
- If free alternative: Need new data fetcher, authentication, rate limiting (MEDIUM-HARD)

**Schema design:**
- Column name: `targets` (int), `target_share` (float)
- Location: `players.csv` and `players_projected.csv`
- Null handling: 0 for non-pass catchers

### Task 6: Create Research Document
**Output:** `docs/research/potential_metrics/01_target_volume.md`

**Use TEMPLATE.md structure:**
1. Existing Data Analysis
2. ESPN API Availability
3. Free Alternative Sources
4. Data Quality Assessment
5. Historical Data Availability (CRITICAL)
6. Implementation Complexity
7. Recommendation

### Task 7: Update Progress Tracker
**File:** `docs/research/potential_metrics/RESEARCH_PROGRESS.md`

**Update metric 1 row:**
```
| 1 | Target Volume/Share | WR, TE, RB | ✅ Complete | [Source] | [Yes/No] | [View](01_target_volume.md) |
```

---

## Protocol Execution Tracker

### Algorithm Traceability Matrix (Iterations 4, 11, 19)
*No algorithms - research/documentation only*

### End-to-End Data Flow (Iterations 5, 12)
```
Input: Metric 1 requirements from scoring_gap_analysis.md
  ↓
Research existing data (data/players.csv, etc.)
  ↓
Research ESPN API (docs/espn/)
  ↓
Research free alternatives (Pro Football Reference, etc.)
  ↓
Assess historical data (simulation/sim_data/)
  ↓
Evaluate complexity
  ↓
Create research document (01_target_volume.md)
  ↓
Update progress tracker
  ↓
Output: Complete research doc with recommendation
```

### Integration Matrix (Iterations 7, 14, 23)

| New Component | Caller/Consumer | Integration Point |
|---------------|-----------------|-------------------|
| 01_target_volume.md | Future implementation | Spec for target data fetching |
| RESEARCH_PROGRESS.md update | Users/agents | Track metric 1 completion |
| Recommendation | Implementation prioritization | Pursue/defer/skip decision |

---

## Progress Notes

**Last Updated:** 2025-12-20
**Current Status:** Created TODO, ready to start verification iterations
**Next Steps:** Complete 24 verification iterations, then research metric 1
**Blockers:** None

---

## Integration Checklist

- [ ] TEMPLATE.md available for structure
- [ ] RESEARCH_PROGRESS.md ready for update
- [ ] scoring_gap_analysis.md has metric 1 definition
- [ ] Existing data files accessible (data/players.csv, etc.)
- [ ] ESPN API docs available (docs/espn/)

---

## Expected Outcome

**After this sub-phase:**
- ✅ Complete research document for Target Volume/Share
- ✅ Clear understanding of data availability
- ✅ Recommendation on pursue/defer/skip
- ✅ Historical data feasibility assessment
- ✅ Implementation complexity estimate
- ✅ Progress tracker updated (1/14 HIGH priority metrics complete)

---

*Pre-implementation verification to begin: 2025-12-20*
