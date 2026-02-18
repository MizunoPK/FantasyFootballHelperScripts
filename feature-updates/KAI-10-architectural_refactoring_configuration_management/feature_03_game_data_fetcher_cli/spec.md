## Feature Spec: game_data_fetcher_cli

## Discovery Context

**Discovery Document:** `../DISCOVERY.md`

### This Feature's Scope (from Discovery)

Wave 2 — Enhance existing argparse with universal args + debug/E2E modes. References Feature 01 spec for design patterns.

**Key scope items:**
- Enhance run_game_data_fetcher.py: add --debug, --e2e-test, --log-level to existing 4 args
- Existing args: --season, --output, --weeks, --current-week
- run_game_data_fetcher.py imports `from config import NFL_SEASON, CURRENT_NFL_WEEK` as fallback — remove these
- Implement --e2e-test mode completing in ≤180 seconds
- Implement --debug mode (DEBUG logging + reduced data scope)

### Relevant Discovery Decisions

- **Solution Approach:** Constructor parameter pattern; argparse defaults are single source of truth
- **Key Constraints:** Existing --season and --current-week args already exist; --log-level and --debug are new; preserve backward compatibility of existing args
- **Dependencies:** None (Wave 2 — references Feature 01 spec for design patterns after it completes S2)

### Relevant User Answers (from Discovery)

| Question | Answer | Impact on This Feature |
|----------|--------|----------------------|
| Documentation as separate feature? | No — integrated into S7.P3 + S10 | README.md updates handled in S7.P3 |

---

## Feature Requirements

{To be completed in S2}
