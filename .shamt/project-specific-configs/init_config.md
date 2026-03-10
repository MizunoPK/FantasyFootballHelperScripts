# Shamt Initialization Config

**Generated:** 2026-03-09
**Status:** COMPLETE

## Project Configuration
- **Project Name:** FantasyFootballHelperScripts
- **Epic Tag:** FF
- **Shamt Agent Name:** Shamt
- **Starting Epic Number:** 1
- **Epic Working Directory:** .shamt/epics/

## AI Service
- **Service:** claude_code
- **Rules File Name:** CLAUDE.md
- **Rules File Path:** /home/kai/code/FantasyFootballHelperScriptsRefactored/
- **Rules File Template:** .shamt/scripts/initialization/RULES_FILE.template.md
- **Needs AI Discovery:** false

## Git Configuration
- **Platform:** github
- **Default Branch:** main

## Script Actions Completed
- [x] Created .shamt/ folder structure (including project-specific-configs/)
- [x] Copied guides from master Shamt (audit/outputs/ cleared for fresh start)
- [x] Copied scripts from master Shamt
- [x] Placed rules file at /home/kai/code/FantasyFootballHelperScriptsRefactored/CLAUDE.md
- [x] Created EPIC_TRACKER.md at .shamt/epics/EPIC_TRACKER.md
- [x] Written .shamt/shamt_master_path.conf
- [x] Written .shamt/rules_file_path.conf
- [x] Written .shamt/last_sync.conf (initialized from master HEAD)
- [x] Applied configuration substitutions to guides and rules file

## Agent Remaining Tasks

**Before beginning:** Re-read the validation loop protocol at:
`.shamt/guides/reference/validation_loop_master_protocol.md`

Then run a validation loop to complete initialization:

- [x] Handle AI service discovery (if Needs AI Discovery = true) — N/A (false)
- [x] Analyze codebase structure, languages, frameworks
- [x] Ask clarifying questions until codebase is fully understood
- [x] Write ARCHITECTURE.md to `.shamt/project-specific-configs/`
- [x] Write CODING_STANDARDS.md to `.shamt/project-specific-configs/`
- [x] Add 3-5 key coding rules to rules file summary section
- [x] Validate all outputs meet quality bar (3 consecutive clean validation rounds — 11 rounds total, rounds 9-11 clean)
- [x] Mark this file complete: change Status to COMPLETE

## Notes
- Existing rules file was preserved — agent should incorporate it into the new rules file content.

- ARCHITECTURE.md and CODING_STANDARDS.md belong in `.shamt/project-specific-configs/`, not the project root.
- Shared guide files in `.shamt/guides/` must remain generic — never write project-specific content into them.
- The only exception: a pointer note in a shared guide directing the agent to check `.shamt/project-specific-configs/` for a supplement.
