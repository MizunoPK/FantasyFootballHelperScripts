# Iterative Simulation Resume - Questions for User

## Overview
I've completed the first verification round (3 iterations) and researched the codebase thoroughly. Before proceeding with implementation, I have some questions about your preferences and requirements for the resume functionality.

---

## Question 1: Parameter Order Validation

**Context:** When resuming, we can detect if the PARAMETER_ORDER has changed by comparing the parameter name in the intermediate file name against the expected parameter at that index.

**Question:** Should we validate that the parameter name in the intermediate file matches the expected parameter at that index in PARAMETER_ORDER?

**Options:**
1. **Strict validation (recommended):** Compare param_name from filename against PARAMETER_ORDER[idx-1]. If mismatch, log warning and start fresh. This prevents resuming with an incompatible parameter sequence.
2. **Lenient approach:** Only check the param_idx exists within valid range, don't validate the actual parameter name. Faster but riskier if PARAMETER_ORDER changes.

**My Recommendation:** Option 1 (strict validation) - safer and prevents subtle bugs if parameter order changes between runs.

**Your preference:** Option 1

---

## Question 2: Resume Detection Logging Detail

**Context:** When the simulation starts, we can log varying levels of detail about what we found and what action we're taking.

**Question:** How much logging detail would you like when resume detection occurs?

**Options:**
1. **Minimal:** Just log "Resuming from parameter X" or "Starting fresh"
2. **Moderate (recommended):** Log number of intermediate files found, which parameters are complete, and what action is being taken
3. **Verbose:** Log every intermediate file found, its idx, param_name, and full resume decision logic

**My Recommendation:** Option 2 (moderate) - provides good visibility without overwhelming the logs.

**Your preference:** Option 2

---

## Question 3: Handling Corrupted Intermediate Files

**Context:** If an intermediate JSON file is corrupted (invalid JSON or missing required fields), we need to decide what to do.

**Question:** What should happen if we encounter a corrupted intermediate file during resume detection?

**Options:**
1. **Skip it and continue (recommended):** Log a warning, skip that file, and use the highest valid idx found among remaining files
2. **Fail fast:** Log error and start fresh from the beginning (treat as if no intermediate files exist)
3. **Prompt user:** Stop execution and ask user whether to resume or restart (interactive)

**My Recommendation:** Option 1 (skip and continue) - most resilient, allows recovery from single file corruption.

**Your preference:** Option 1

---

## Question 4: Resume Summary at Startup

**Context:** When resuming, we could display a summary of what's already been completed.

**Question:** Would you like a summary showing which parameters have already been optimized when resuming?

**Options:**
1. **Yes - show summary:** Display a list of completed parameters (e.g., "Already optimized: NORMALIZATION_MAX_SCALE, SAME_POS_BYE_WEIGHT")
2. **No - just show resume point:** Only log "Resuming from parameter X of Y" without listing what's done

**My Recommendation:** Option 1 (show summary) - helpful for understanding progress, especially after long runs.

**Your preference:** Option 2

---

## Question 5: Command-Line Control (Optional Enhancement)

**Context:** Currently, the resume behavior would be fully automatic. We could add command-line flags for manual control.

**Question:** Should we add optional command-line flags to force resume/restart behavior?

**Options:**
1. **Fully automatic (recommended):** Resume detection is always automatic based on intermediate files. User can manually delete files to force restart.
2. **Add --force-resume flag:** Add flag to force resume even if files look suspicious (skip validation)
3. **Add --force-restart flag:** Add flag to force restart (ignore intermediate files)
4. **Add both flags:** Maximum flexibility with both --force-resume and --force-restart

**My Recommendation:** Option 1 (fully automatic) - simpler and covers 99% of use cases. User can delete intermediate files manually if needed.

**Your preference:** Option 1

---

## Question 6: Infinite Loop Behavior Confirmation

**Context:** The iterative mode runs in an infinite loop (run_simulation.py lines 334-349). Each loop iteration creates a new SimulationManager instance.

**Question:** Confirming expected behavior - is this correct?

**Expected behavior:**
- **Within one loop iteration:** If interrupted partway, resume from last completed parameter
- **Between loop iterations:** After completing a full run (all parameters optimized), cleanup intermediate files and start fresh with the new optimal config as baseline
- **Result:** Resume works within an iteration, but each iteration starts fresh

**Is this the correct understanding?** Yes

---

## Summary

Please answer each question above. Your responses will help me finalize the implementation approach before starting the second verification round (3 more iterations) and then coding.

**Total verification progress:** 3/6 iterations complete (first round done)
**Next steps after receiving answers:**
1. Update TODO file with your chosen approaches
2. Execute second verification round (3 more iterations)
3. Begin implementation with full clarity on requirements
