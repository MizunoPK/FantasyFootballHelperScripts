# Documentation Feature

## Objective

Ensure all project documentation is accurate, comprehensive, and up-to-date, plus create a new QUICK_START_GUIDE.md that provides a seasonal workflow guide for using the project over the course of a fantasy football season.

---

## Investigation Summary

### Key Findings from Codebase Audit

#### Test Count
- **README says:** 1,811 tests
- **Actual count:** 2,255 test functions across 70 test files
- **Action needed:** Update test count

#### Missing Scripts from README
| Script | Purpose | Currently Documented? |
|--------|---------|----------------------|
| `run_schedule_fetcher.py` | Fetches NFL season schedule from ESPN API → `data/season_schedule.csv` | **NO** |
| `run_game_data_fetcher.py` | Fetches game data (venue, weather, scores) from ESPN/Open-Meteo → `data/game_data.csv` | **NO** |
| `run_draft_order_loop.py` | Loops through all draft order strategies running iterative optimization | **NO** |

#### Missing Component from README
| Component | Purpose | Currently Documented? |
|-----------|---------|----------------------|
| `nfl-fantasy-exporter-extension/` | Chrome extension to extract player ownership data from NFL Fantasy | **NO** |

#### Incorrect Paths in README
| README Says | Actual Path | Issue |
|-------------|-------------|-------|
| `docs/scoring/` | `docs/scoring_v2/` | Wrong directory name |
| `data/drafted_players.csv` | `data/drafted_data.csv` | Wrong filename |
| `data/teams_week_N.csv` | `data/team_data/*.csv` (folder with per-team files) | Different structure |

#### Additional Data Files Not Documented
- `data/configs/` - Configuration folder
- `data/game_data.csv` - Game data with weather
- `data/players_projected.csv` - Projected player data
- `data/historical_data/` - Historical data archive

#### ARCHITECTURE.md Status
- Generally accurate for core components
- May need updates for new managers: `GameDataManager`, `SeasonScheduleManager`, `ProjectedPointsManager`
- Mode count (4) is correct: Add to Roster, Starter Helper, Trade Simulator, Modify Player Data
- Note: `ReserveAssessmentModeManager` exists in code but is NOT integrated (orphan code - don't document)

---

## Proposed Answers to Open Questions

### Q1: Verification Depth
**Question:** How thoroughly should we verify existing docs?

**Proposed Answer: Option B - Line-by-line verification with targeted updates**

Reasoning:
- Investigation already identified specific discrepancies
- Full audit would be overkill; most content is accurate
- Focus on fixing known issues rather than exhaustive review

---

### Q2: QUICK_START_GUIDE Scope
**Question:** What level of detail for the quick start guide?

**Proposed Answer: Option B - Moderate (3-5 pages)**

Reasoning:
- Brief enough to be a "quick" start
- Comprehensive enough to cover the full seasonal workflow
- Includes exact commands but not exhaustive explanation
- References main README for detailed information

---

### Q3: Missing Scripts
**Question:** Should we add the missing scripts to README?

**Proposed Answer: YES - Add all three**

| Script | Add to Section |
|--------|---------------|
| `run_schedule_fetcher.py` | "Data Fetchers" subsection |
| `run_game_data_fetcher.py` | "Data Fetchers" subsection |
| `run_draft_order_loop.py` | "Simulation System" subsection (advanced usage) |

---

### Q4: Test Count
**Question:** Update test count?

**Proposed Answer: YES - Update to 2,255 tests**

Also update:
- "70 test files"
- Mention test count may grow as features are added

---

### Q5: ARCHITECTURE.md Verification Level
**Question:** How deep should we verify class diagrams and data flows?

**Proposed Answer: Moderate verification**

- Verify core components mentioned are still accurate
- Don't do exhaustive line-by-line code audit
- Focus on adding missing managers to documentation
- Update any obviously incorrect diagrams

---

### Q6: QUICK_START_GUIDE Target Audience
**Question:** Who is this guide for?

**Proposed Answer: Fantasy football users wanting to use the tools**

Reasoning:
- Developers can read ARCHITECTURE.md
- Users need a practical workflow guide
- Focus on "how to use" not "how it works"

---

### Q7: Seasonal Phases
**Question:** What phases should be covered?

**Proposed Answer: All four phases**

1. **Pre-Season Setup** - Install, fetch data, run simulations
2. **Draft Day** - Use league helper in draft mode
3. **Weekly In-Season** - Update data, optimize lineup, evaluate trades
4. **End of Season** - Archive data (brief mention)

---

### Q8: Command Examples
**Question:** Include exact `python run_*.py` examples?

**Proposed Answer: YES**

- Include exact commands for each phase
- Show common flags/options
- Keep explanations brief

---

### Q9: Output Examples
**Question:** Include sample terminal output?

**Proposed Answer: NO - Keep it concise**

Reasoning:
- Output examples add bulk without much value
- Users will see real output when they run commands
- Reference main README if detailed output examples needed

---

## Implementation Plan

### README.md Updates

1. **Fix test count:** 1,811 → 2,255 (70 test files)
2. **Add missing scripts:**
   - `run_schedule_fetcher.py`
   - `run_game_data_fetcher.py`
   - `run_draft_order_loop.py`
3. **Add Chrome extension:** `nfl-fantasy-exporter-extension/`
4. **Fix paths:**
   - `docs/scoring/` → `docs/scoring_v2/`
   - `drafted_players.csv` → `drafted_data.csv`
5. **Update data files section:** Add missing files
6. **Update project structure tree:** Reflect current state

### ARCHITECTURE.md Updates

1. **Add missing managers:**
   - `GameDataManager`
   - `SeasonScheduleManager`
   - `ProjectedPointsManager`
2. **Verify and update test count**
3. **Verify data flow diagrams still accurate**

### QUICK_START_GUIDE.md Creation

**Proposed Structure:**
```
# Quick Start Guide

## Overview (1 paragraph)

## Pre-Season Setup
### 1. Installation
### 2. Fetch Player Data
### 3. (Optional) Run Simulations

## Draft Day
### Using the Draft Helper

## Weekly In-Season
### 1. Update Player Data
### 2. Optimize Your Lineup
### 3. Evaluate Trades

## Reference
### All Scripts Quick Reference
### Common Commands
```

---

## Status: ✅ APPROVED - Ready for Implementation

All proposed answers approved by user on 2025-12-09.
