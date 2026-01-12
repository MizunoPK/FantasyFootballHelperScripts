# STAGE 5ac Part 1: Iterations 17-18 - Implementation Phasing & Rollback

**Part of:** Epic-Driven Development Workflow v2
**Stage:** 5ac - Implementation Planning Round 3 Part 1
**Iterations:** 17-18
**Purpose:** Define implementation phasing and rollback strategy
**Prerequisites:** Round 2 complete, confidence >= MEDIUM, test coverage >90%
**Main Guide:** stages/stage_5/round3_part1_preparation.md

---

## Overview

Iterations 17-18 prepare for safe, incremental implementation:
- **Iteration 17:** Break implementation into phases with checkpoints (prevents "big bang" failures)
- **Iteration 18:** Define rollback strategy if critical issues found

**Time estimate:** 10-15 minutes (both iterations)

---

## Iteration 17: Implementation Phasing

**Purpose:** Break implementation into phases for incremental validation

**Why this matters:** "Big bang" integration (implementing everything at once) causes failures. Phasing allows checkpoint validation after each phase.

### Process

**1. Group implementation tasks from implementation_plan.md into logical phases:**

**Example Phasing:**

```markdown
## Implementation Phasing

**Phase 1: Core Data Loading (Foundation)**
- Task 1: Load ADP data from CSV
- Task 2: Add FantasyPlayer.adp_value field
- Task 3: Add FantasyPlayer.adp_rank field
- Tests: test_load_adp_data_*, test_player_fields_*
- **Checkpoint:** All loading tests pass, data structure validated

**Phase 2: Matching Logic**
- Task 4: Implement PlayerManager._match_player_to_adp()
- Task 5: Handle player not found in ADP data (edge case)
- Tests: test_match_player_*, test_unmatched_player_*
- **Checkpoint:** Matching tests pass, edge cases handled

**Phase 3: Multiplier Calculation**
- Task 6: Implement ConfigManager.get_adp_multiplier()
- Task 7: Implement PlayerManager._calculate_adp_multiplier()
- Task 8: Handle invalid ADP values (edge case)
- Tests: test_calculate_adp_*, test_invalid_adp_*
- **Checkpoint:** Calculation tests pass, all edge cases covered

**Phase 4: Score Integration**
- Task 9: Update FantasyPlayer.calculate_total_score()
- Task 10: Apply adp_multiplier to score
- Tests: test_scoring_*, test_integration_*
- **Checkpoint:** All integration tests pass, scores correct

**Phase 5: Error Handling & Edge Cases**
- Task 11: Handle ADP file missing (edge case)
- Task 12: Handle duplicate players in ADP data (edge case)
- Task 13: Validate config ADP ranges (edge case)
- Tests: test_error_*, test_edge_case_*
- **Checkpoint:** All error tests pass, graceful degradation verified

**Phase 6: Integration & Documentation**
- Task 14: Integration tests with real objects (no mocks)
- Task 15: Update documentation
- Task 16: Update league_config.json with ADP settings
- Tests: test_integration_*, test_e2e_*
- **Checkpoint:** ALL tests pass (100%), documentation complete

---

**Phasing Rules:**
1. Must complete Phase N before starting Phase N+1
2. All phase tests must pass before proceeding
3. If phase fails → Fix issues → Re-run phase tests → Proceed
4. No "skipping ahead" to later phases
```

**2. Define phase boundaries and checkpoints:**

Each phase ends with:
- **Test Validation:** All phase tests must pass
- **Mini-QC:** Quick review of phase code
- **Agent Status Update:** Document phase completion

**3. Add "Implementation Phasing" section to implementation_plan.md:**

Add phasing section to implementation_plan.md:

```markdown
---

## Implementation Phasing

[Paste phasing plan from step 1]

---
```

### Iteration 17 Output

**Output:** Implementation phasing plan with 4-6 phases added to implementation_plan.md

### After Iteration Checkpoint - questions.md Review

After completing this iteration, check if you have questions or found answers:

1. **If you discovered NEW uncertainties during this iteration:**
   - Add them to `questions.md` with context
   - Format: Question, context, impact on implementation

2. **If you found ANSWERS to existing questions in questions.md:**
   - Update questions.md to mark question as answered
   - Document the answer and source

3. **If no new questions and no answers found:**
   - No action needed, proceed to next iteration

**Note:** This is a quick check (1-2 minutes). questions.md will be presented to user at Gate 5.

### Update Agent Status

```markdown
Progress: Iteration 17/24 (Round 3 Part 1) complete
Next Action: Iteration 18 - Rollback Strategy
```

---

## Iteration 18: Rollback Strategy

**Purpose:** Define how to rollback if implementation has critical issues

**Why this matters:** Production bugs happen. Having a rollback plan enables quick recovery.

### Process

**1. Identify rollback mechanism:**
   - **Option 1:** Feature flag / config toggle (fastest, preferred)
   - **Option 2:** Git revert (clean, but slower)
   - **Option 3:** Disable code path (quick fix)

**2. Document rollback procedure:**

```markdown
## Rollback Strategy

**If critical bug discovered after implementation:**

### Option 1: Config Toggle (Recommended - 1 minute downtime)

**Procedure:**
1. Open `data/league_config.json`
2. Set: `"enable_adp_integration": false`
3. Restart league helper: `python run_league_helper.py`
4. Verify: Old scoring restored (check recommendations.csv)

**Rollback Time:** ~1 minute
**Impact:** Feature disabled, old behavior restored

---

### Option 2: Git Revert (Complete rollback - 5 minutes)

**Procedure:**
1. Identify commit hash: `git log --oneline` (find "feat/KAI-X: Add ADP integration")
2. Revert commit: `git revert <commit_hash>`
3. Remove ADP data file: `rm data/player_data/adp_data.csv`
4. Run tests: `python tests/run_all_tests.py` (verify clean revert)
5. Restart league helper

**Rollback Time:** ~5 minutes
**Impact:** Code reverted to pre-feature state

---

### Option 3: Code Path Disable (Emergency - 30 seconds)

**Procedure:**
1. Open `league_helper/util/PlayerManager.py`
2. Find: `if self.config.enable_adp_integration:`
3. Change to: `if False:  # EMERGENCY ROLLBACK`
4. Restart league helper

**Rollback Time:** ~30 seconds
**Impact:** ADP code path disabled, old behavior restored

---

**Rollback Decision Criteria:**
- **Critical bug (data corruption, crashes):** Use Option 1 or 2
- **Performance issue:** Use Option 1, investigate later
- **Minor bug (cosmetic issue):** Create bug fix, no rollback needed

**Testing Rollback:**
- Task 18: Add test_feature_can_be_disabled()
  - Verify: Setting enable_adp_integration=false works
  - Verify: No residual state after rollback
  - Verify: Old scoring behavior restored

---
```

**3. Add rollback test task if needed:**

```markdown
## Task 18: Test Feature Rollback

**Requirement:** Verify feature can be cleanly disabled

**Test:** test_feature_can_be_disabled()

**Acceptance Criteria:**
- [ ] Set config.enable_adp_integration = False
- [ ] Run scoring
- [ ] Verify: Old behavior restored (no ADP multiplier applied)
- [ ] Verify: No errors or warnings
- [ ] Verify: No residual ADP data in output
```

### Iteration 18 Output

**Output:** Rollback strategy documented, rollback test task added

### After Iteration Checkpoint - questions.md Review

After completing this iteration, check if you have questions or found answers:

1. **If you discovered NEW uncertainties during this iteration:**
   - Add them to `questions.md` with context
   - Format: Question, context, impact on implementation

2. **If you found ANSWERS to existing questions in questions.md:**
   - Update questions.md to mark question as answered
   - Document the answer and source

3. **If no new questions and no answers found:**
   - No action needed, proceed to next iteration

**Note:** This is a quick check (1-2 minutes). questions.md will be presented to user at Gate 5.

### Update Agent Status

```markdown
Progress: Iteration 18/24 (Round 3 Part 1) complete
Next Action: Iteration 19 - Algorithm Traceability Matrix (Final)
```

---

## Summary - Iterations 17-18

**Completed:**
- [ ] Iteration 17: Implementation phasing plan (4-6 phases with checkpoints)
- [ ] Iteration 18: Rollback strategy (3 options documented)

**Key Outputs:**
- Implementation phasing prevents "big bang" integration failures
- Rollback strategy enables quick recovery from critical bugs
- Both added to implementation_plan.md

**Next:** Read `stages/stage_5/round3_part1/iterations_19_20_algorithms.md` for Iterations 19-20

---

**END OF ITERATIONS 17-18 GUIDE**
