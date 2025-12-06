# Week-by-Week Config - Questions for User

**Objective File**: `updates/week-by-week-config.txt`
**Created**: 2025-12-01
**Status**: Awaiting user response

---

## Context

After 5 iterations of verification and analysis, I have a clear understanding of the implementation requirements. However, there are 4 design decisions that need your input to proceed correctly.

---

## Question 1: Config Behavior During Simulation

**Background**: Currently, each simulation runs a full 16-week season using a single merged config. The spec mentions "determines which config produced the best win rate for each block of weeks."

**Question**: Should the simulation:

- **A) Single config per simulation**: Run the full 16 weeks with ONE merged config, then analyze which configs performed best in each week range (1-5, 6-11, 12-17)?
- **B) Config switching mid-season**: Actually switch configs at week 6 and week 12 boundaries during the simulation?

**Recommendation**: Option A is simpler and matches the current simulation architecture. The "best per week block" analysis happens after simulations complete.

Answer: Option A

---

## Question 2: Performance Tracking Granularity

**Background**: The spec says to determine "best win rate for each block of weeks." This requires tracking wins/losses separately for weeks 1-5, 6-11, and 12-17.

**Question**: Should the output folder contain:

- **A) Potentially different configs per week range**: The week1-5.json, week6-11.json, and week12-17.json files could each come from DIFFERENT source configs (e.g., config_A's params for weeks 1-5, config_B's params for weeks 6-11)?
- **B) Same config all week ranges**: All 3 week files come from the same overall best-performing config?

**Recommendation**: Option A provides more optimization but is more complex. Please confirm which approach you intended.

Answer: Option A

---

## Question 3: Base Config in Output Folder

**Background**: The output folder will contain 4 files: `league_config.json` (base), `week1-5.json`, `week6-11.json`, `week12-17.json`.

**Question**: For the base `league_config.json` in output:

- **A) Shared static base**: Use the same base config (without week-specific scoring params) regardless of which week configs are selected?
- **B) From best overall config**: Extract base params from the overall best-performing config?

**Recommendation**: Option A - the base config contains static params (NFL_SEASON, MAX_POSITIONS, etc.) that shouldn't vary between configs.

Answer: Option B - The base league_config.json file will still contain parameters that are being tested via the simulation such as DRAFT_ORDER, and those values should be determined by the config that has the best win rate for all 17 weeks.

---

## Question 4: League Helper vs Simulation Behavior

**Background**: There are two use cases:
1. **League Helper** (interactive mode): Loads config based on CURRENT_NFL_WEEK
2. **Simulation** (optimization mode): Tests configs across all weeks

**Question**: For the league helper, when a user runs it at week 7:

- **A) Auto-merge week-specific**: ConfigManager automatically loads base + week6-11.json and merges them
- **B) Pre-merged expected**: User is expected to have a fully merged config already

**Recommendation**: Option A - ConfigManager should handle the merging transparently based on CURRENT_NFL_WEEK.

Answer: Option A

---

## Your Responses

Please answer each question by indicating A or B (or provide an alternative approach):

1. Config Behavior During Simulation: ___
2. Performance Tracking Granularity: ___
3. Base Config in Output Folder: ___
4. League Helper vs Simulation Behavior: ___

---

## Next Steps

After you answer these questions:
1. I will update the TODO file with your answers
2. Run 7 more verification iterations (as per rules.md)
3. Begin implementation

---

## Summary of Verified Understanding

- **ConfigManager**: Will load from `data/configs/` folder, merge base + week-specific configs
- **Simulation output**: Will create folders containing 4 config files instead of single files
- **Tests**: ~100+ test files will need fixture updates for new folder structure
- **Original `data/league_config.json`**: Will be deleted (no backward compatibility needed)
- **Week ranges**: Fixed at 1-5, 6-11, 12-17
