## Feature Spec: accuracy_simulation_e2e

## Discovery Context

**Discovery Document:** `../DISCOVERY.md`

### This Feature's Scope (from Discovery)

Wave 2 — Add --e2e-test and --debug to existing argparse (already has --log-level). References Feature 01 spec for design patterns.

**Key scope items:**
- Add to run_accuracy_simulation.py: --e2e-test, --debug (currently has 10 args including --log-level)
- --log-level already exists with choices: debug/info/warning/error — preserve existing behavior
- Implement --e2e-test mode: single horizon, single run, minimal dataset, ≤180 seconds
- Implement --debug mode (DEBUG logging + reduced scope; --debug forces debug log level)

### Relevant Discovery Decisions

- **Solution Approach:** Enhance existing argparse; accuracy_simulation already has --log-level unlike win_rate
- **Key Constraints:** --log-level already implemented and working; --debug is new and must force DEBUG level (precedence: --debug overrides --log-level)
- **Dependencies:** None (Wave 2 — references Feature 01 spec for design patterns after it completes S2)

### Relevant User Answers (from Discovery)

| Question | Answer | Impact on This Feature |
|----------|--------|----------------------|
| Documentation as separate feature? | No — integrated into S7.P3 + S10 | README.md updates handled in S7.P3 |

---

## Feature Requirements

{To be completed in S2}
