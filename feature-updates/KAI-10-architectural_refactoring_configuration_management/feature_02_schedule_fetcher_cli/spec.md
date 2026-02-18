## Feature Spec: schedule_fetcher_cli

## Discovery Context

**Discovery Document:** `../DISCOVERY.md`

### This Feature's Scope (from Discovery)

Wave 2 — Add 5 new CLI args to run_schedule_fetcher.py + debug/E2E modes. References Feature 01 spec for design patterns.

**Key scope items:**
- Add argparse to run_schedule_fetcher.py: --season, --output-path, --data-folder, --output-format
- Add universal args: --debug, --e2e-test, --log-level
- Remove NFL_SEASON=2025 hardcoded in runner (replace with argparse default)
- No config file to strip from (schedule-data-fetcher/ has no config.py)
- Implement --e2e-test mode completing in ≤180 seconds
- Implement --debug mode (DEBUG logging + reduced data scope)

### Relevant Discovery Decisions

- **Solution Approach:** Constructor parameter pattern; argparse defaults are single source of truth
- **Key Constraints:** schedule-data-fetcher/ has only ScheduleFetcher.py — no config.py to strip; NFL_SEASON is directly in runner
- **Dependencies:** None (Wave 2 — references Feature 01 spec for design patterns after it completes S2)
- **Note:** Feature 01 completed S2 first to establish design precedents for all Wave 2 features

### Relevant User Answers (from Discovery)

| Question | Answer | Impact on This Feature |
|----------|--------|----------------------|
| Documentation as separate feature? | No — integrated into S7.P3 + S10 | README.md updates handled in S7.P3 |

---

## Feature Requirements

{To be completed in S2}
