# ESPN API Metric Research Feature

## Overview

This feature involves systematically researching 58 potential metrics identified in `docs/research/scoring_gap_analysis.md` (Version 3.0) to determine data availability and feasibility for integration into the fantasy football scoring system.

## Purpose

Provide comprehensive research documentation for each metric to support informed decisions about which metrics to implement. Each metric will have a dedicated research document answering:
- Can we calculate it from existing data?
- Is it available via ESPN API?
- What free alternatives exist?
- **CRITICAL:** Can we obtain historical snapshots for simulation validation?
- What is the implementation complexity?
- Should we pursue it?

## Why This Matters

The current 13-step scoring algorithm lacks several advanced metrics that proved valuable in streaming research:
- Target Volume/Share
- QB Context
- Vegas Lines/Game Environment
- Position-specific metrics (K, TE, RB, QB, WR)
- **Historical data requirement:** All metrics must support simulation validation via `simulation/sim_data/{YEAR}/weeks/week_{NN}/` structure

## Scope

**Total Metrics:** 58 (increased from 38)

**Sections:**
1. Original gap metrics (1-11)
2. Additional review metrics (12-19)
3. Projection calculation metrics (20-38)
4. **Position-specific metrics (39-58)** - Added Dec 17, 2025

**Output:** Individual research documents in `docs/research/potential_metrics/` named `{metric_number}_{metric_name}.md`

---

## Agent Status

**Current Phase:** PLANNING COMPLETE ✅
**Current Step:** Ready for Implementation
**Last Updated:** 2025-12-20

### Planning Progress

- [x] Phase 1: Create folder structure
- [x] Phase 2: Investigation
- [x] Phase 3: Report & Pause
- [x] Phase 4: Iterative Resolution (ALL 47 items resolved systematically)
- [x] Planning Complete - Ready for Implementation

### What's Resolved

- Feature folder created (Phase 1)
- Notes file moved to folder (Phase 1)
- Planning files initialized (Phase 1)
- **Codebase investigation complete** (Phase 2)
  - Analyzed existing data files (players.csv, team_data/, game_data.csv)
  - Reviewed existing data fetchers (player-data-fetcher/ patterns)
  - Examined documentation patterns (docs/research/ examples)
  - Verified simulation data structure (sim_data/2024/)
- **Checklist populated with 47 open questions** (Phase 2)
  - 13 categories across 3 iterations
  - Core research questions (template, verification, historical data)
  - Operational aspects (quality, documentation, integration)
  - Edge cases (multi-season, dependencies, maintenance)

### What's Resolved (Added 2025-12-20)

- ✅ ALL 47 checklist items systematically resolved
- ✅ Research methodology finalized
- ✅ Data source verification approach defined
- ✅ Historical data acquisition strategy established
- ✅ Documentation template structure decided
- ✅ Complete decisions documented in `RESOLUTION_DECISIONS.md` (456 lines)

### Next Action

**For Next Agent:** Begin implementation phase. Create template and progress tracker, then start researching HIGH priority metrics (14 metrics).

---

## Files in This Folder

| File | Purpose | Status |
|------|---------|--------|
| `README.md` | This file - context for agents | ✓ Created |
| `espn-api-metric-research_notes.txt` | Original research plan (reference) | ✓ Moved |
| `espn-api-metric-research_specs.md` | Detailed specification | ✓ Created |
| `espn-api-metric-research_checklist.md` | Open questions tracker | ✓ Created |
| `espn-api-metric-research_lessons_learned.md` | Process improvements | ✓ Created |

---

## Key Context

### Historical Data Structure

```
simulation/sim_data/
├── 2021/
├── 2022/
├── 2024/
│   ├── game_data.csv
│   ├── season_schedule.csv
│   ├── team_data/{TEAM}.csv (week-by-week stats)
│   └── weeks/
│       ├── week_01/
│       │   ├── players.csv (week 1 actual, 2-17 projected)
│       │   └── players_projected.csv
│       └── week_05/ (weeks 1-5 actual, 6-17 projected)
```

**Critical Requirement:** Each metric must be assessed for historical data availability to support simulation validation.

### Priority Tiers

**Phase 1 (14 HIGH priority metrics):**
- Metrics 1, 2, 4, 12, 21, 22 (original)
- Metrics 39, 40, 42, 46, 49, 50, 52, 53 (position-specific)

**Phase 2 (MEDIUM):** 15 metrics
**Phase 3 (LOW):** 29 metrics

---

## Related Documents

- `docs/research/scoring_gap_analysis.md` - Source of 58 metrics (Version 3.0)
- `docs/espn/` - ESPN API documentation
- `data/` - Current data files to check for existing metrics
- `simulation/sim_data/` - Historical data structure for validation
