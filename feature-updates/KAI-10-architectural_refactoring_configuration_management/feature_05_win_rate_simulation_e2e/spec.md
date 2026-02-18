## Feature Spec: win_rate_simulation_e2e

## Discovery Context

**Discovery Document:** `../DISCOVERY.md`

### This Feature's Scope (from Discovery)

Wave 2 — Add --e2e-test, --debug, and --log-level to existing comprehensive argparse. References Feature 01 spec for design patterns.

**Key scope items:**
- Add to run_win_rate_simulation.py: --e2e-test, --debug, --log-level (currently has 17 args, missing all 3)
- Implement --e2e-test mode: single run, 0-1 random configs, minimal dataset, no parameter sweeps, ≤180 seconds
- Implement --debug mode (DEBUG logging + reduced iterations)
- Remove LOGGING_LEVEL module constant (replace with --log-level)

### Relevant Discovery Decisions

- **Solution Approach:** Enhance existing comprehensive argparse; argparse defaults are single source of truth
- **Key Constraints:** win_rate_simulation already has 17 args (comprehensive) — only adding 3 new args; preserve all existing arg behavior
- **Dependencies:** None (Wave 2 — references Feature 01 spec for design patterns after it completes S2)

### Relevant User Answers (from Discovery)

| Question | Answer | Impact on This Feature |
|----------|--------|----------------------|
| Documentation as separate feature? | No — integrated into S7.P3 + S10 | README.md updates handled in S7.P3 |

---

## Feature Requirements

{To be completed in S2}
