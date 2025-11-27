# Questions: League Config Auto Update

These questions arose during the first verification round (5 iterations) of researching the codebase and understanding the requirements.

---

## Question 1: Trigger Mechanism

**Context**: This feature updates `data/league_config.json` from an `optimal_*.json` file. The trigger mechanism needs to be decided.

**Question**: How should this update be triggered?

**Options**:
- **A) Standalone script**: Create `update_league_config.py` at project root that can be run manually
- **B) Automatic after simulation**: Automatically update league_config.json when iterative simulation completes and saves a new optimal config
- **C) Both**: Provide standalone script AND optionally auto-update after simulation (with flag)

**Recommendation**: Option A - Standalone script. Keeps control in user's hands and avoids unexpected config changes.

Answer: Option B

---

## Question 2: Optimal Config Selection

**Context**: Multiple `optimal_*.json` files may exist in `simulation/simulation_configs/`.

**Question**: Which optimal config file should be used?

**Options**:
- **A) Most recent**: Automatically select the newest `optimal_iterative_*.json` by timestamp
- **B) User-specified**: Require user to specify the exact file path as argument
- **C) Interactive**: Show list of available optimal configs and let user choose

**Recommendation**: Option A - Most recent. Simpler UX, typically what user wants after running simulation.

Answer: Option A

---

## Question 3: Backup Strategy

**Context**: Updating league_config.json is potentially destructive.

**Question**: How should we handle backups?

**Options**:
- **A) Always backup**: Create `league_config.json.bak` before every update
- **B) Timestamped backup**: Create `league_config_YYYYMMDD_HHMMSS.json.bak`
- **C) No backup**: Trust user to use git for version control

**Recommendation**: Option B - Timestamped backup. Allows multiple updates without overwriting previous backups.

Answer: Option C

---

## Question 4: config_name and description Fields

**Context**: The optimal config files have `config_name` (source config) and `description` (win rate). When updating league_config.json, should these be preserved?

**Question**: What should happen to config_name and description fields?

**Options**:
- **A) Copy from optimal**: Use the config_name and description from the optimal file
- **B) Update with source info**: Set config_name to the optimal file path, update description with timestamp
- **C) Preserve original**: Keep whatever was in the original league_config.json

**Recommendation**: Option B - Provides traceability of which optimal config was applied.

Answer: Option A

---

## Question 5: Validation and Dry Run

**Context**: Users may want to preview changes before applying them.

**Question**: Should we include a dry-run/preview mode?

**Options**:
- **A) Yes**: Add `--dry-run` flag that shows what would change without modifying files
- **B) No**: Just update the file (with backup)

**Recommendation**: Option A - Dry run is helpful for verification before applying.

---

## Summary of Clarifications from Original Requirements

- **PRESERVE from original**: CURRENT_NFL_WEEK, NFL_SEASON, MAX_POSITIONS, FLEX_ELIGIBLE_POSITIONS
- **COPY from MATCHUP to SCHEDULE**: MIN_WEEKS, IMPACT_SCALE, WEIGHT
- **ALL OTHER parameters**: From optimal_*.json

---

## Your Answers

Please provide your answers below:

### Q1 Answer:


### Q2 Answer:


### Q3 Answer:


### Q4 Answer:


### Q5 Answer:

