# S5: Feature Implementation
## S5.P3: Planning Round 3
### S5.P3.I1: Output Consumer Validation

**Purpose:** Output Consumer Validation
**Prerequisites:** Previous iterations complete
**Main Guide:** `stages/s5/s5_p3_planning_round3.md`
**Router:** `stages/s5/s5_p3_i1_preparation.md`

---

## Iteration 22: Output Consumer Validation

**Purpose:** Verify feature outputs are consumable by downstream code

**Why this matters:** Feature can work in isolation but fail when consumed by other modules → Integration failures

### Process

**1. Identify output consumers:**

```markdown
## Output Consumer Analysis

**Feature Output:** Updated FantasyPlayer objects with:
- player.adp_value (int): ADP ranking
- player.adp_rank (int): Rank in ADP list
- player.adp_multiplier (float): Score multiplier from ADP

**Downstream Consumers:**

1. **AddToRosterModeManager.get_recommendations()**
   - Consumes: FantasyPlayer objects with adp_multiplier
   - Usage: Generates draft recommendations sorted by score
   - Impact: Must handle players with adp_multiplier applied

2. **StarterHelperModeManager.get_optimal_lineup()**
   - Consumes: Roster FantasyPlayer objects with adp_multiplier
   - Usage: Selects optimal lineup based on scores
   - Impact: Must use ADP-adjusted scores for lineup decisions

3. **TradeAnalyzerModeManager.analyze_trade()**
   - Consumes: FantasyPlayer objects for trade analysis
   - Usage: Compares player values
   - Impact: Should use ADP-adjusted scores for trade value

---
```

**2. Plan roundtrip validation tests:**

```markdown
## Output Consumer Validation Tests

### Consumer 1: AddToRosterModeManager (Draft Mode)

**Roundtrip Test:** test_adp_output_consumed_by_draft_mode()

**Steps:**
1. Load players with ADP integration (REAL PlayerManager)
2. Verify: Players have adp_value, adp_rank, adp_multiplier set
3. Call: AddToRosterModeManager.get_recommendations() with ADP-enabled players
4. Verify: Recommendations generated successfully (no errors)
5. Verify: Recommendations use ADP-adjusted scores
6. Verify: Top recommendations include high-ADP players (logic check)
7. Verify: Low-ADP players ranked lower

**Expected Behavior:** Draft recommendations prioritize high-ADP players

**Acceptance Criteria:**
- [ ] Consumer code runs without errors
- [ ] Recommendations use adp_multiplier in scoring
- [ ] Top 10 recommendations include players with ADP <20
- [ ] No AttributeError or KeyError

---

### Consumer 2: StarterHelperModeManager (Starter Mode)

**Roundtrip Test:** test_adp_output_consumed_by_starter_mode()

**Steps:**
1. Load roster players with ADP integration
2. Verify: Roster players have adp_multiplier set
3. Call: StarterHelperModeManager.get_optimal_lineup()
4. Verify: Lineup selection successful (no errors)
5. Verify: Lineup scores include ADP contribution
6. Verify: Optimal lineup selects high-ADP players when scores close

**Expected Behavior:** Lineup optimizer uses ADP-adjusted scores

**Acceptance Criteria:**
- [ ] Consumer code runs without errors
- [ ] Lineup scores reflect adp_multiplier
- [ ] No AttributeError or KeyError

---

### Consumer 3: TradeAnalyzerModeManager (Trade Mode)

**Roundtrip Test:** test_adp_output_consumed_by_trade_analyzer()

**Steps:**
1. Load players with ADP integration
2. Create mock trade: Give player A, Receive player B
3. Call: TradeAnalyzerModeManager.analyze_trade()
4. Verify: Trade analysis successful (no errors)
5. Verify: Trade value uses ADP-adjusted scores
6. Verify: Analysis shows "fair" when ADP values similar

**Expected Behavior:** Trade analysis uses ADP-adjusted values

**Acceptance Criteria:**
- [ ] Consumer code runs without errors
- [ ] Trade values reflect adp_multiplier
- [ ] No AttributeError or KeyError

---
```

**3. Add consumer validation tasks to implementation_plan.md "Implementation Tasks" section:**

```markdown
## Task 40: Consumer Validation - Draft Mode

**Requirement:** Verify AddToRosterModeManager consumes ADP-adjusted scores

**Test:** test_adp_output_consumed_by_draft_mode()

**Acceptance Criteria:**
- [ ] Load players with ADP integration
- [ ] Call AddToRosterModeManager.get_recommendations()
- [ ] Verify recommendations use ADP-adjusted scores
- [ ] Verify top recommendations include high-ADP players
- [ ] No errors in consumer code

---

## Task 41: Consumer Validation - Starter Mode

**Requirement:** Verify StarterHelperModeManager consumes ADP-adjusted scores

**Test:** test_adp_output_consumed_by_starter_mode()

**Acceptance Criteria:**
- [ ] Load roster with ADP integration
- [ ] Call StarterHelperModeManager.get_optimal_lineup()
- [ ] Verify lineup selection works
- [ ] Verify lineup scores include ADP contribution
- [ ] No errors in consumer code

---

## Task 42: Consumer Validation - Trade Analyzer

**Requirement:** Verify TradeAnalyzerModeManager consumes ADP-adjusted scores

**Test:** test_adp_output_consumed_by_trade_analyzer()

**Acceptance Criteria:**
- [ ] Load players with ADP integration
- [ ] Call TradeAnalyzerModeManager.analyze_trade()
- [ ] Verify trade analysis works
- [ ] Verify trade values use ADP-adjusted scores
- [ ] No errors in consumer code

---
```

### Iteration 22 Output

**Output:** Output consumer validation plan with roundtrip tests

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
Progress: Iteration 22/24 (Planning Round 3 Part 1) complete
Consumer Validation: 3 consumers identified, roundtrip tests planned
Part 1 COMPLETE - Ready for Part 2
Next Action: Read stages/s5/s5_p3_i3_gates_part2.md
```

---

## Summary - Iterations 21-22

**Completed:**
- [ ] Iteration 21: Mock audit (5 mocks verified, 1 fixed) + integration tests (3 planned)
- [ ] Iteration 22: Output consumer validation (3 consumers, roundtrip tests)

**Key Outputs:**
- Mock audit prevents interface mismatch bugs
- Integration tests prove feature works with real objects
- Consumer validation ensures downstream compatibility
- All added to implementation_plan.md

**Part 1 COMPLETE - Next:** Read `stages/s5/s5_p3_i3_gates_part2.md` for Part 2


## Exit Criteria

**Iteration 14-19 complete when ALL of these are true:**

- [ ] All tasks in this iteration complete
- [ ] implementation_plan.md updated
- [ ] Agent Status updated
- [ ] Ready for next iteration

**If any criterion unchecked:** Complete missing items first

---
---

**END OF ITERATIONS 21-22 GUIDE**
