## Feature Spec: league_helper_cli

## Discovery Context

**Discovery Document:** `../DISCOVERY.md`

### This Feature's Scope (from Discovery)

Wave 2 — Add comprehensive argparse (12+ args), refactor mode managers to accept parameters, debug/E2E modes. References Feature 01 spec for design patterns.

**Key scope items:**
- Add to run_league_helper.py: ~12 new args + 3 universal args
  - From constants.py: --my-team-name, --recommendation-count, --min-waiver-improvement, --num-runners-up, --min-trade-improvement
  - New args: --mode, --config-path, --data-folder, --league-id, --week, --season, --team-id, --logging-to-file, --logging-file
  - Universal: --debug, --e2e-test, --log-level
- Remove CLI-configurable constants from league_helper/constants.py
- Refactor 10+ mode manager modules to accept parameters instead of importing constants
- Implement --e2e-test mode: run all 5 modes automatically with debug-sized datasets, no user prompts, ≤180 seconds total
- Implement --debug mode (DEBUG logging + reduced recommendations/trades)
- Note: LARGE SCOPE — 45+ code references to Constants across mode managers

### Relevant Discovery Decisions

- **Solution Approach:** Constructor parameter pattern; argparse defaults are single source of truth; all 5 mode managers need refactoring
- **Key Constraints:** Largest scope of all Wave 2 features; 10+ modules import from constants; --my-team-name consistent with player_fetcher
- **Dependencies:** None (Wave 2 — references Feature 01 spec for design patterns after it completes S2)

### Relevant User Answers (from Discovery)

| Question | Answer | Impact on This Feature |
|----------|--------|----------------------|
| league_helper team name arg naming | --my-team-name (consistent with player_fetcher) | Use --my-team-name, not --team-name |
| Documentation as separate feature? | No — integrated into S7.P3 + S10 | README.md updates handled in S7.P3 |

---

## Feature Requirements

{To be completed in S2}
