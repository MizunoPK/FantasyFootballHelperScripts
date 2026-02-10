# Handoff Package: Feature 03 (player_data_fetcher_logging)

**Generated:** 2026-02-06
**Epic:** KAI-8-logging_refactoring
**Dependency Group:** Group 2 (Wave 2)
**Primary Agent Status:** Group 1 S2 complete, coordinating Group 2 parallel work

---

I'm joining as a secondary agent to help with S2 parallelization for the logging_refactoring epic.

## Agent Configuration

**My Agent ID:** Secondary-B
**My Feature Assignment:** Feature 03: player_data_fetcher_logging
**My Role:** Execute S2.P1 (3 iterations), then wait for Primary to run S2.P2
**Dependency Group:** Group 2 (Dependent on Group 1)

---

## Group Context

### Why I'm Starting Now

**Group 1 has completed S2:**
- Feature 01 (core_logging_infrastructure) finished S2.P1 + S2.P2 on 2026-02-06
- Feature 01's spec is approved and available for reference
- My feature depends on Feature 01's spec to write its own spec
- I can now specify my feature with knowledge of Feature 01's APIs

**What Group 1 Provides:**
- LineBasedRotatingHandler class (custom logging handler with 500-line rotation)
- Modified setup_logger() API (integrates new handler)
- Centralized logs/{script_name}/ folder structure
- Timestamped filenames: {script_name}-{YYYYMMDD_HHMMSS}.log
- Max 50 files cleanup per subfolder

### Group 1 Specs Available

**Feature 01: core_logging_infrastructure**
- **File:** `feature-updates/KAI-8-logging_refactoring/feature_01_core_logging_infrastructure/spec.md`
- **Key Content:**
  - LineBasedRotatingHandler API (500-line rotation, 50-file cleanup)
  - Modified setup_logger() function signature and usage
  - logs/{script_name}/ folder structure
  - Integration contracts for Features 2-7

**Key API Reference from Feature 01:**
```python
# How to use the new logging infrastructure (from Feature 01 spec):
from utils.LoggingManager import setup_logger

logger = setup_logger(
    name="player_data_fetcher",     # Script name (becomes folder name)
    level="INFO",                    # Log level
    log_to_file=True,               # Enable file logging (CLI-driven)
    log_file_path=None,             # Let LoggingManager auto-generate path
    log_format="standard"           # Format style
)
# Result: logs/player_data_fetcher/player_data_fetcher-{timestamp}.log with 500-line rotation
```

**Integration Contracts (must follow):**
1. **Logger name = folder name:** Use consistent name "player_data_fetcher" (not variations)
2. **log_file_path=None:** Don't specify custom paths (let LoggingManager generate)
3. **log_to_file from CLI:** Wire --enable-log-file flag to log_to_file parameter

### Group 2 Features (parallel with me)

All 6 Group 2 features execute S2 in parallel after Group 1 completes:

- Feature 02: league_helper_logging (Secondary-A)
- **Feature 03: player_data_fetcher_logging** (Secondary-B - **THIS IS ME**)
- Feature 04: accuracy_sim_logging (Secondary-C)
- Feature 05: win_rate_sim_logging (Secondary-D)
- Feature 06: historical_data_compiler_logging (Secondary-E)
- Feature 07: schedule_fetcher_logging (Secondary-F)

---

## My Task

### Execute S2.P1 for Feature 03

**Three iterations required:**
1. **S2.P1.I1 - Discovery:** Research player-data-fetcher script and modules, create RESEARCH_NOTES.md, draft spec.md
2. **S2.P1.I2 - Checklist Resolution:** Create checklist.md with questions, get user answers
3. **S2.P1.I3 - Refinement:** Polish spec based on user feedback, pass Gates 1-3

**Reference Group 1 spec as needed:**
- File path: `feature_01_core_logging_infrastructure/spec.md`
- Focus on LineBasedRotatingHandler API, setup_logger() usage, integration contracts

**What to do:**
1. Read guide: `stages/s2/s2_p1_spec_creation_refinement.md`
2. Execute 3 iterations systematically
3. Mark complete in coordination STATUS file
4. **STOP after S2.P1** - Wait for Primary to run S2.P2 across all Group 2 features
5. Follow coordination protocols (checkpoints every 15 min, check inbox, escalate if blocked)

**What to read:**
- `parallel_work/s2_secondary_agent_guide.md` (my complete workflow)
- `feature_03_player_data_fetcher_logging/HANDOFF.md` (feature-specific context - see below)
- `feature_01_core_logging_infrastructure/spec.md` (Group 1 dependency)

**Coordination:**
- Update `parallel_work/coordination/agent_checkpoints/secondary_b_checkpoint.md` every 15 minutes
- Check `parallel_work/coordination/inboxes/from_primary/` for messages from Primary
- Update `feature_03_player_data_fetcher_logging/STATUS` at phase transitions
- Escalate to `parallel_work/coordination/inboxes/from_secondary_b/` if blocked

---

## Epic Context

### Epic Goal

Improve logging infrastructure across all major scripts with:
- Centralized log management (logs/ folder with script-specific subfolders)
- Automated log rotation (500-line cap, create new file when exceeded)
- Automated cleanup (max 50 logs per folder, auto-delete oldest)
- Quality improvements to Debug/Info logs
- CLI toggle for file logging on/off per script

### Total Features: 7

**Group 1 (Foundation - S2 Complete):**
1. Feature 01: core_logging_infrastructure ✅ S2 Complete

**Group 2 (Scripts - S2 In Progress):**
2. Feature 02: league_helper_logging
3. **Feature 03: player_data_fetcher_logging** ← **I'M WORKING ON THIS**
4. Feature 04: accuracy_sim_logging
5. Feature 05: win_rate_sim_logging
6. Feature 06: historical_data_compiler_logging
7. Feature 07: schedule_fetcher_logging

### Discovery Summary

**From DISCOVERY.md:**
- Epic size: MEDIUM (7 features determined after Discovery)
- All 7 user questions answered (timestamp format, eager counter, CLI defaults, etc.)
- 5 discovery iterations + 3 validation rounds (Validation Loop passed)
- Custom LineBasedRotatingHandler recommended (Solution Option 1)
- Log quality criteria defined for DEBUG/INFO levels

**Key User Decisions:**
- Q1: Full timestamp format (YYYYMMDD_HHMMSS)
- Q2: Eager counter in memory (better performance)
- Q4: File logging OFF by default, --enable-log-file flag to enable
- Q6: Log quality improvements system-wide (all modules)
- Q7: Counter resets on restart (new file per run)

---

## Feature 03 Specific Context

### My Feature Scope (from DISCOVERY.md)

**Feature 3: player_data_fetcher_logging**

**Purpose:** CLI integration and log quality improvements for player-data-fetcher script

**Scope:**
- Add --enable-log-file flag to run_player_fetcher.py
- Modify subprocess wrapper to forward sys.argv[1:]
- Apply DEBUG/INFO criteria to player-data-fetcher/ modules logs
- Review and improve logs in:
  - player_data_fetcher_main
  - espn_client
  - player_data_exporter
  - progress_tracker
  - game_data_fetcher
- Update affected test assertions

**Dependencies:** Feature 01 (core infrastructure) - **COMPLETE ✅**

**Discovery Basis:**
- Based on Iteration 2 (run_player_fetcher.py is subprocess wrapper)
- Based on Iteration 3 (log quality criteria)
- Based on Iteration 5 (subprocess wrapper forwarding via sys.argv[1:])

**Estimated Size:** SMALL-MEDIUM

### Key Files to Research

**Script Entry Point:**
- `run_player_fetcher.py` - Subprocess wrapper, needs --enable-log-file flag + sys.argv forwarding

**Main Module:**
- `player-data-fetcher/player_data_fetcher_main.py` - Main entry point, logging setup

**Core Modules:**
- `player-data-fetcher/espn_client.py` - ESPN API client
- `player-data-fetcher/player_data_exporter.py` - Data export logic
- `player-data-fetcher/progress_tracker.py` - Progress tracking
- `player-data-fetcher/game_data_fetcher.py` - Game data fetching

**Tests:**
- `tests/player-data-fetcher/` - May need updates if log assertions change

### Log Quality Criteria (from Discovery Iteration 3)

**DEBUG Level:**
- ✅ Function entry/exit with parameters (not excessive - only for complex flows)
- ✅ Data transformations with before/after values
- ✅ Conditional branch taken (which if/else path executed)
- ❌ NOT every variable assignment
- ❌ NOT logging inside tight loops without throttling

**INFO Level:**
- ✅ Script start/complete with configuration
- ✅ Major phase transitions (e.g., "Starting player data fetch")
- ✅ Significant outcomes (e.g., "Fetched 150 players")
- ❌ NOT implementation details (that's DEBUG)
- ❌ NOT every function call

---

## Getting Started

### First Actions (in order)

1. **Read the secondary agent guide:**
   - `parallel_work/s2_secondary_agent_guide.md` (complete workflow for secondary agents)

2. **Read the S2.P1 guide:**
   - `stages/s2/s2_p1_spec_creation_refinement.md` (3 iterations: Discovery, Checklist, Refinement)

3. **Read Group 1 dependency:**
   - `feature_01_core_logging_infrastructure/spec.md` (understand LineBasedRotatingHandler API, setup_logger() usage, integration contracts)

4. **Update Agent Status:**
   - File: `feature_03_player_data_fetcher_logging/README.md`
   - Update "Agent Status" section with current guide, step, timestamp

5. **Initialize coordination:**
   - Create `parallel_work/coordination/agent_checkpoints/secondary_b_checkpoint.md`
   - Initial status: STARTUP, feature: 03, timestamp

6. **Begin S2.P1.I1 (Discovery):**
   - Research run_player_fetcher.py (subprocess wrapper)
   - Research player-data-fetcher/ modules
   - Identify all logger.debug/info calls in player-data-fetcher scope
   - Create RESEARCH_NOTES.md with findings
   - Draft spec.md based on research

### Coordination Reminders

**Every 15 minutes:**
- Update `agent_checkpoints/secondary_b_checkpoint.md` with current status
- Check `inboxes/from_primary/` for messages
- Report progress or blockers

**When blocked:**
- Create escalation file in `inboxes/from_secondary_b/`
- Wait for Primary response (< 15 min expected)

**When complete:**
- Update STATUS file: `STAGE: S2.P1`, `READY_FOR_SYNC: true`
- Update checkpoint: `Status: READY_FOR_SYNC`
- Wait for Primary to run S2.P2 for all Group 2 features

### Remember

**You're in Group 2:**
- Group 1 (Feature 01) is COMPLETE ✅
- I can reference Feature 01's spec to understand the logging infrastructure I'll integrate with
- I'm working in parallel with 5 other secondary agents (Features 02, 04-07)
- Primary agent coordinates all 6 of us

**After S2.P1:**
- Primary will run S2.P2 (cross-feature alignment) for all Group 2 features
- I don't run S2.P2 myself - that's Primary's job
- After S2.P2 → Groups no longer matter, proceed to S3 (epic-level)

---

**Good luck with Feature 03! If you have questions, escalate to Primary via inbox.**
