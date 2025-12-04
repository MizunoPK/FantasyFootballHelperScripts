# Questions: Derive Bye Week Data from Season Schedule

**Related TODO**: `updates/todo-files/player-fetcher-bye-week-from-schedule_todo.md`
**Objective File**: `updates/player-fetcher-bye-week-from-schedule.txt`

---

## Question 1: NFL Scores Exporter

**Discovery**: During codebase research, I found that `nfl-scores-fetcher/nfl_scores_exporter.py` also references `bye_weeks.csv` at line 200. It looks for the file at `shared_files/bye_weeks.csv` and uses it to identify which teams are on bye for a specific week.

**Current Behavior**: The code is wrapped in a try/except and silently fails if the file is missing - it's optional functionality.

**Options**:

A) **Leave as-is** - The nfl_scores_exporter will continue to look for `bye_weeks.csv` at `shared_files/bye_weeks.csv` and silently fail if missing. Bye teams won't be marked in the output.

B) **Update to derive from season_schedule.csv** - Modify nfl_scores_exporter to also derive bye weeks from the season schedule, similar to the player-data-fetcher changes. This would make bye team identification work consistently.

C) **Remove the bye week functionality** - Remove the try/except block entirely since it's not working anyway (the file doesn't exist).

**Recommendation**: Option B (update to use season_schedule.csv) for consistency, but this adds scope to the task.

Answer: Option A. Do not bother with updating the scores fetcher

---

## Question 2: Error Handling Strictness

**Context**: The original `_load_bye_weeks()` was **optional** - if the file was missing, it logged a warning and continued with an empty dict. Players just wouldn't have bye week data.

The requirement says season_schedule.csv should be **required** with a fatal error if missing.

**Options**:

A) **Fatal error** (as specified) - Raise `FileNotFoundError` and halt execution if season_schedule.csv is missing. User must run schedule-data-fetcher first.

B) **Warning with empty fallback** (like before) - Log a warning but continue, returning empty bye_weeks dict. Players won't have bye week data but fetcher still works.

**Recommendation**: Option A (fatal error) as specified in the requirements - this ensures data integrity and makes the dependency explicit.

Answer: Option A


---

## Answers

Please provide your answers below:

### Q1: NFL Scores Exporter
**Answer**:

### Q2: Error Handling Strictness
**Answer**:

---

*Once you provide answers, I will update the TODO file and continue with the second verification round (9 more iterations) before implementation.*
