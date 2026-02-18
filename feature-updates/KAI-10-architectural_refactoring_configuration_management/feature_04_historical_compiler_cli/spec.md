## Feature Spec: historical_compiler_cli

## Discovery Context

**Discovery Document:** `../DISCOVERY.md`

### This Feature's Scope (from Discovery)

Wave 2 — Enhance existing argparse with 5 new args + debug/E2E modes. References Feature 01 spec for design patterns.

**Key scope items:**
- Enhance compile_historical_data.py: add --debug, --e2e-test, --log-level, --timeout, --rate-limit-delay
- Existing args: --year, --verbose, --enable-log-file, --output-dir
- Move REQUEST_TIMEOUT=30.0 and RATE_LIMIT_DELAY=0.3 from historical_data_compiler/constants.py to argparse defaults
- Refactor http_client.py (or equivalent) to accept timeout/rate_limit via constructor params
- Implement --e2e-test mode completing in ≤180 seconds (compile 1 season, skip backups, minimal validation)
- Implement --debug mode (DEBUG logging + reduced scope)
- Backward compatibility: --verbose flag preserved (maps to --log-level debug)

### Relevant Discovery Decisions

- **Solution Approach:** Constructor parameter pattern; argparse defaults are single source of truth
- **Key Constraints:** REQUEST_TIMEOUT and RATE_LIMIT_DELAY are in historical_data_compiler/constants.py (not a runner-level config.py); backward compatibility for --verbose
- **Dependencies:** None (Wave 2 — references Feature 01 spec for design patterns after it completes S2)

### Relevant User Answers (from Discovery)

| Question | Answer | Impact on This Feature |
|----------|--------|----------------------|
| Documentation as separate feature? | No — integrated into S7.P3 + S10 | README.md updates handled in S7.P3 |

---

## Feature Requirements

{To be completed in S2}
