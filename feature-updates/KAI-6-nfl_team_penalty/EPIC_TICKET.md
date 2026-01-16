# Epic Ticket: nfl_team_penalty

**Created:** 2026-01-12
**Status:** VALIDATED

---

## Description

This epic adds an NFL team penalty system to Add to Roster mode, allowing users to penalize players from specific NFL teams they want to avoid drafting. Users configure a list of team abbreviations (e.g., ["LV", "NYJ", "NYG", "KC"]) and a penalty weight multiplier (e.g., 0.75), and the system automatically reduces the final scores of all players from those teams by the specified percentage. This is a user-specific strategy setting that helps enforce personal team preferences during draft recommendations, while simulations continue to use objective scoring without team bias.

---

## Acceptance Criteria (Epic-Level)

**The epic is successful when ALL of these are true:**

- [ ] Users can configure NFL_TEAM_PENALTY list in league_config.json with team abbreviations
- [ ] Users can configure NFL_TEAM_PENALTY_WEIGHT in league_config.json (0.0-1.0 range)
- [ ] Players from penalized teams have their final scores multiplied by the penalty weight in Add to Roster mode
- [ ] Simulation config files use default values (empty list, 1.0 weight) to maintain objective scoring
- [ ] Config validation prevents invalid team abbreviations and weight values outside 0.0-1.0 range
- [ ] Score penalty is applied AFTER the 10-step scoring algorithm completes
- [ ] Scoring reasons display "NFL Team Penalty Applied" when penalty is applied
- [ ] All unit tests pass (100% pass rate)
- [ ] Epic smoke testing passes (all scenarios)
- [ ] Feature works correctly with empty penalty list (no penalties applied)

---

## Success Indicators

**Measurable metrics that show epic succeeded:**

- Config coverage: NFL_TEAM_PENALTY and NFL_TEAM_PENALTY_WEIGHT exist in league_config.json and all simulation configs
- Penalty accuracy: Players from penalized teams show scores exactly equal to (original_score × penalty_weight)
- Penalty visibility: Scoring reasons include "NFL Team Penalty Applied" for 100% of penalized players
- Default behavior: Players NOT in penalty list show unchanged scores
- Simulation neutrality: All simulation configs use empty list and 1.0 weight (no team bias)
- Test coverage: 100% test pass rate maintained
- Mode isolation: Penalty only affects Add to Roster mode, not other modes

---

## Failure Patterns (How We'd Know Epic Failed)

**These symptoms indicate the epic FAILED its goals:**

❌ Penalty applied to players NOT in the configured team list (logic error)
❌ Penalty applied in simulation results (should only affect user's Add to Roster mode)
❌ Score penalty applied at wrong step (before 10-step algorithm instead of after)
❌ Config accepts invalid values (weight > 1.0, weight < 0.0, or invalid team abbreviations)
❌ Scoring reasons don't show penalty was applied (transparency issue)
❌ Empty penalty list causes crashes or errors (should gracefully handle)
❌ Penalty multiplies existing penalties instead of final score (double-penalty bug)

---

## Scope Boundaries

✅ **In Scope (What IS included):**
- NFL_TEAM_PENALTY config setting (list of team abbreviations)
- NFL_TEAM_PENALTY_WEIGHT config setting (float multiplier 0.0-1.0)
- Score penalty application in Add to Roster mode
- Config validation (valid teams, valid weight range)
- Updating league_config.json with user's team preferences
- Updating all simulation configs with defaults (empty list, 1.0 weight)
- Logging and scoring reasons for penalty application
- Unit tests for config loading and penalty application

❌ **Out of Scope (What is NOT included):**
- Applying penalties in simulation modes (simulations remain objective)
- UI changes for configuring team penalties (users edit JSON manually)
- Dynamic team suggestions based on performance (static user preference only)
- Position-specific team penalties (applies to ALL positions from penalized teams)
- Historical analysis of team performance (user decides which teams to penalize)
- Penalty application in other league helper modes (Trade Simulator, Reserve Assessment)

---

## User Validation

**This section filled out by USER - agent presents ticket and asks user to verify/approve**

**User comments:**
None - epic ticket approved as written

**User approval:** YES
**Approved by:** User
**Approved date:** 2026-01-12

---

## Notes

**Why this ticket matters:**
This ticket serves as the source of truth for epic-level outcomes. It's created BEFORE folder structure to ensure agent understands WHAT the epic achieves. During Iteration 25 (Spec Validation Against Validated Documents), spec.md will be validated against this ticket to catch misinterpretation.

**Key outcome:**
Users can enforce their team preferences during draft by automatically penalizing players from specific NFL teams, while keeping simulations objective and unbiased.
