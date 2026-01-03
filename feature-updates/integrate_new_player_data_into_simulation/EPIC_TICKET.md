# Epic Ticket: integrate_new_player_data_into_simulation

**Created:** 2026-01-02
**Status:** VALIDATED (user approved 2026-01-02)

---

## Description

This epic verifies and completes the integration of JSON player data files into both Win Rate Simulation and Accuracy Simulation systems. The league helper recently transitioned from CSV to JSON player data (deprecation date: 2025-12-30), but the simulation modules have incomplete and buggy JSON integration. After this epic, both simulations will correctly load player data from positional JSON files (qb_data.json, rb_data.json, etc.) in week-specific folders, properly handle the week_N+1 logic for Week 17, and have all deprecated CSV code removed.

---

## Acceptance Criteria (Epic-Level)

**The epic is successful when ALL of these are true:**

- [ ] Both Win Rate Sim and Accuracy Sim load player data from JSON files (not CSV files)
- [ ] All 18 weeks of data are accessible and used correctly in both simulations
- [ ] Week 17 correctly uses week_17 folder for projected_points and week_18 folder for actual_points
- [ ] Both simulations handle new JSON field structure (arrays for projected_points, actual_points, drafted_by, locked)
- [ ] No references to players.csv or players_projected.csv remain in simulation code
- [ ] All deprecated CSV parsing methods are removed from simulation code
- [ ] Both simulations produce equivalent or better results compared to CSV baseline
- [ ] All 2,200+ unit tests pass (100% pass rate)
- [ ] Documentation and docstrings updated to reflect JSON-based data loading

---

## Success Indicators

**Measurable metrics that show epic succeeded:**

- Week coverage: 18/18 weeks accessible in both simulations (100% coverage)
- Data quality: <1% of actual_points are 0.0 for completed weeks (indicates proper data loading)
- Test pass rate: 2,200+/2,200+ tests passing (100%)
- Code cleanliness: Zero references to "players.csv" or "players_projected.csv" in simulation/ directory
- Functionality parity: Both simulations execute without errors using JSON data
- Week 17 verification: Week 17 actual_points loaded from week_18 folder (not week_17)

---

## Failure Patterns (How We'd Know Epic Failed)

**These symptoms indicate the epic FAILED its goals:**

❌ >90% of actual_points are 0.0 (data loading broken - week offset bug)
❌ Only weeks 1-16 work while week 17-18 have all zeros (week_N+1 logic missing)
❌ Simulations crash with "FileNotFoundError: players.csv" (CSV dependency not removed)
❌ Tests fail when using JSON files but pass with CSV (incomplete migration)
❌ Week 17 uses week_17 actual_points instead of week_18 (week offset bug)
❌ Documentation still references CSV files (incomplete cleanup)
❌ Deprecated `_parse_players_csv()` method still exists and callable
❌ Field mismatches: Code expects single values but JSON has arrays

---

## Scope Boundaries

✅ **In Scope (What IS included):**
- Verifying Win Rate Sim `_parse_players_json()` implementation correctness
- Verifying Accuracy Sim JSON player data loading through PlayerManager
- Verifying week_N+1 logic for Week 17 (projected from week_17, actual from week_18)
- Removing deprecated `_parse_players_csv()` method
- Updating all docstrings and comments referencing CSV files
- Updating tests to verify JSON loading correctness
- Running full simulations to verify functionality parity with CSV baseline
- Verifying proper handling of JSON array fields (projected_points, actual_points)

❌ **Out of Scope (What is NOT included):**
- Generating NEW JSON files from ESPN API (uses existing sim_data/ files)
- Changes to PlayerManager JSON loading logic (already implemented in league_helper)
- Changing JSON file structure or format (structure is established)
- Performance optimization beyond maintaining parity
- Support for seasons other than 2024/2025 (uses existing data only)
- Changes to league_helper module (already migrated to JSON)

---

## User Validation

**This section filled out by USER - agent presents ticket and asks user to verify/approve**

**User comments:**
None - epic ticket approved as written

**User approval:** YES
**Approved by:** User
**Approved date:** 2026-01-02

---

## Notes

**Why this ticket matters:**
This ticket serves as the source of truth for epic-level outcomes. It validates that the agent understands the epic's goals: verify existing JSON integration, fix bugs, remove deprecated CSV code, and ensure both simulations work correctly with JSON data for all 18 weeks including the Week 17 edge case.

**Key insight from epic request:**
The user explicitly stated "assume all previous work is incorrect or incomplete and verify everything for correctness and completeness." This epic is about verification and cleanup of partially-completed work, not greenfield development.
