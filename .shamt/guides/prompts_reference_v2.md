# Shamt Phase Transition Prompts — Index

This file is the index for all phase transition prompts. Prompts are organized by stage in the `prompts/` directory.

**Using prompts is MANDATORY** at every stage transition. Using the correct prompt ensures the agent reads the full guide and acknowledges critical requirements before proceeding.

---

## Prompt Files by Stage

| Stage | Prompt File | Key Prompts |
|-------|-------------|-------------|
| S1 | `prompts/s1_prompts.md` | Starting Epic Planning, Starting Discovery Phase |
| S2 | `prompts/s2_prompts.md` | Starting Feature Deep Dive, Starting Spec Creation |
| S3 | `prompts/s3_prompts.md` | Starting Epic Planning and Approval |
| S4 | `prompts/s4_prompts.md` | Starting Feature Testing Strategy |
| S5 | `prompts/s5_s8_prompts.md` | Implementation Plan (S5 v2 Validation Loop), Gate 5 Approval |
| S6 | `prompts/s5_s8_prompts.md` | Starting Execution, Resuming After Compaction |
| S7 | `prompts/s5_s8_prompts.md` | Smoke Testing, QC Rounds, Final Review |
| S8 | `prompts/s5_s8_prompts.md` | Cross-Feature Alignment, Testing Plan Update |
| S9 | `prompts/s9_prompts.md` | Epic Final QC prompts |
| S10 | `prompts/s10_prompts.md` | Starting Epic Cleanup, Guide Updates |
| Guide Updates | `prompts/guide_update_prompts.md` | Presenting proposals, after applying changes |
| Problem Situations | `prompts/problem_situations_prompts.md` | Debugging, missed requirements, resuming after compaction |
| Special Workflows | `prompts/special_workflows_prompts.md` | Parallel work, conflict handling |

---

## Most-Used Prompts

### Starting a Stage
→ Read `prompts/s{N}_prompts.md` for the relevant stage

### Resuming In-Progress Epic (After Session Compaction)
→ See `prompts/problem_situations_prompts.md` → "Resuming In-Progress Epic"

### Creating a Missed Requirement
→ See `prompts/problem_situations_prompts.md` → "Creating Missed Requirement"

### Starting Debugging Protocol
→ See `prompts/problem_situations_prompts.md` → "Starting Debugging Protocol"

### S5 Complete — Implementation Plan Approval
→ See `prompts/s5_s8_prompts.md` → "S5 Complete - Implementation Plan Approval"

### Starting S10.P1 Guide Updates
→ See `prompts/guide_update_prompts.md` → "Starting Guide Update Workflow"

---

## How to Use a Prompt

1. Identify which stage/situation you're in
2. Read the relevant prompt file
3. Copy the prompt text and output it to the user (or use it as your acknowledgment)
4. The prompt confirms you've read the guide and understand requirements

**Never skip prompts** — they are a mandatory checkpoint, not a suggestion.
