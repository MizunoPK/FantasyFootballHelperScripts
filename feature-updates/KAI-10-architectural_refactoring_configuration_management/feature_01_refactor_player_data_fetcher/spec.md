## Feature Spec: refactor_player_data_fetcher

## Discovery Context

**Discovery Document:** `../DISCOVERY.md`

### This Feature's Scope (from Discovery)

Wave 1 (solo) — Internal dependency injection refactoring (5 modules) + 14 CLI args + debug/E2E modes. Sets design precedents for all other scripts.

**Key scope items:**
- Refactor 5 internal modules from direct config imports to constructor parameters: player_data_fetcher_main.py, espn_client.py, game_data_fetcher.py, fantasy_points_calculator.py, player_data_exporter.py
- Add 14 CLI args to run_player_fetcher.py (replacing 11 constants + LOGGING_LEVEL + 3 optional args)
- Add universal args: --debug, --e2e-test, --log-level
- Remove all CLI-configurable constants from player-data-fetcher/config.py
- Implement --e2e-test mode completing in ≤180 seconds
- Implement --debug mode (DEBUG logging + reduced data scope)

### Relevant Discovery Decisions

- **Solution Approach:** Constructor parameter pattern — pass configuration via runner → main() → internal modules via settings dict/class; argparse defaults are single source of truth
- **Key Constraints:** Zero CLI constants in config.py after epic; all 2,744 existing tests must continue to pass; behavioral equivalence preserved
- **Dependencies:** None (Wave 1 solo — this feature sets the precedent)
- **Verification:** player_data_fetcher_main.py uses DIRECT imports (from config import ...), NOT importlib override

### Relevant User Answers (from Discovery)

| Question | Answer | Impact on This Feature |
|----------|--------|----------------------|
| Merge internal refactoring and argparse into single feature? | Yes — single refactor_player_data_fetcher feature | This feature covers both DI refactoring AND CLI args |
| Documentation as separate feature? | No — integrated into S7.P3 + S10 | README.md updates handled in S7.P3 for this feature |
| Team name arg naming? | --my-team-name | Consistent across player_fetcher and league_helper |

---

## Feature Requirements

{To be completed in S2}
