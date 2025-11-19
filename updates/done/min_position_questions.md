# Minimum Positions Implementation - Clarification Questions

## Context

I'm implementing MIN_POSITIONS validation for the waiver optimizer to ensure suggested trades don't leave the user's team below minimum position thresholds. After researching the codebase, I have identified several areas that need clarification.

---

## Question 1: FLEX Position Handling

**Context**: The specification provides MIN_POSITIONS without a FLEX entry:
```python
MIN_POSITIONS = {
    QB: 1,
    RB: 3,
    WR: 3,
    TE: 1,
    K: 1,
    DST: 1
}
```

However, the codebase has MAX_POSITIONS which includes FLEX:
```python
MAX_POSITIONS = {
    "QB": 2,
    "RB": 3,
    "WR": 3,
    "FLEX": 3,  # <-- FLEX included
    "TE": 2,
    "K": 1,
    "DST": 1
}
```

**Question**: Should MIN_POSITIONS include a FLEX entry?

**Options**:

**A. No FLEX in MIN_POSITIONS (as specified)**
- Description: Keep MIN_POSITIONS without FLEX. When counting positions for minimum validation, only count players in their natural position slots (RB slot, WR slot), not FLEX.
- Pros: Matches the specification exactly, simpler implementation
- Cons: Might allow edge case where user has enough RB/WR total but below minimum in natural slots

**B. Add FLEX: 0 to MIN_POSITIONS**
- Description: Explicitly set FLEX minimum to 0 for completeness
- Pros: Makes it clear FLEX has no minimum requirement
- Cons: Adds entry that doesn't enforce anything

**Recommendation**: Option A - No FLEX entry. The minimum positions should refer to natural position slots only.

**Your Answer**: Option A

---

## Question 2: Position Counting Strategy

**Context**: The FantasyTeam class uses `slot_assignments` to track which players are in which slots (natural position vs FLEX). When validating MIN_POSITIONS, I need to decide how to count positions.

**Question**: When checking if a roster meets MIN_POSITIONS[RB]=3, should we count:

**Options**:

**A. Natural position slots only**
- Description: Count only RBs assigned to RB slots (not RBs in FLEX slot). Use `slot_assignments[RB]` count.
- Example: User has 2 RBs in RB slots + 1 RB in FLEX = counts as 2 RBs (fails MIN of 3)
- Pros: Enforces minimum in natural positions, prevents roster imbalance
- Cons: Stricter validation might reject valid trades

**B. Total position count (natural + FLEX)**
- Description: Count all RBs regardless of slot assignment. Use `count_positions()` which counts by player.position.
- Example: User has 2 RBs in RB slots + 1 RB in FLEX = counts as 3 RBs (passes MIN of 3)
- Pros: More lenient, focuses on total roster composition
- Cons: Might allow scenarios where natural slots are too empty

**Recommendation**: Option B - Total position count. This is more intuitive and aligns with how users think about their roster ("I have 3 RBs total").

**Your Answer**: Option B

---

## Question 3: Scope of Minimum Validation

**Context**: The specification states "This will only be relevant for the waiver optimizer". The codebase has three trade modes:
1. Waiver Optimizer (`is_waivers=True`)
2. Trade Suggestor (`is_waivers=False`)
3. Manual Trade Visualizer (`ignore_max_positions=True`)

**Question**: Should MIN_POSITIONS validation apply to other modes beyond waiver optimizer?

**Options**:

**A. Waiver Optimizer only (as specified)**
- Description: Add MIN check only when `is_waivers=True` in `get_trade_combinations()`
- Pros: Follows specification exactly, minimal changes
- Cons: Trade Suggestor and Manual Visualizer could suggest trades that violate minimums

**B. Waiver Optimizer + Trade Suggestor**
- Description: Add MIN check when `is_waivers=True OR not ignore_max_positions`
- Pros: Prevents minimum violations in automatic trade suggestions
- Cons: Goes beyond specification

**C. All trade modes**
- Description: Add MIN check universally (even Manual Trade Visualizer)
- Pros: Complete protection against minimum violations
- Cons: Might be too restrictive for manual trades

**Recommendation**: Option A - Waiver Optimizer only. Follow the specification, but we can extend later if needed.

**Your Answer**: Option B

---

## Question 4: Validation Strictness (Lenient vs Strict)

**Context**: The codebase has `validate_roster_lenient()` which allows trades even if position violations already exist, as long as the trade doesn't make them worse. This is used for MAX_POSITIONS validation.

**Question**: Should MIN_POSITIONS validation be lenient (like MAX) or strict?

**Options**:

**A. Strict validation**
- Description: Reject any trade that results in below-minimum positions, even if roster was already below minimum
- Example: User has 2 RBs (below MIN of 3), trades RB for QB → Rejected (now 1 RB)
- Example: User has 2 RBs (below MIN of 3), trades QB for RB → Allowed (now 3 RBs)
- Pros: Prevents making bad rosters worse, simple to implement
- Cons: Might block trades that improve the situation

**B. Lenient validation**
- Description: Allow trades as long as they don't worsen minimum violations (similar to MAX_POSITIONS)
- Example: User has 2 RBs (1 violation), trades RB for QB → Rejected (now 2 violations)
- Example: User has 2 RBs (1 violation), trades QB for WR → Allowed (still 1 violation, different position)
- Pros: More flexible, allows fixing roster issues
- Cons: More complex logic, might allow perpetually non-compliant rosters

**Recommendation**: Option A - Strict validation. MIN_POSITIONS is a safety threshold that should always be maintained. If user's roster is already below minimum, they should fix that before making more trades.

**Your Answer**: Option B

---

## Question 5: Error Messaging and User Feedback

**Context**: When trades are rejected due to MIN_POSITIONS violations, the waiver optimizer needs to provide feedback.

**Question**: What level of detail should be shown to users about minimum position rejections?

**Options**:

**A. Silent filtering (DEBUG logging only)**
- Description: Silently skip trades that violate minimums, log at DEBUG level
- User sees: Fewer trade suggestions (no explanation why)
- Pros: Clean user experience, doesn't clutter output
- Cons: Users might wonder why certain trades aren't suggested

**B. Summary message after filtering**
- Description: Show count of rejected trades at the end
- Example: "Note: 15 potential trades were filtered due to minimum position requirements"
- Pros: User awareness without overwhelming detail
- Cons: Still doesn't explain which positions are the issue

**C. Detailed per-position summary**
- Description: Show which positions caused rejections
- Example: "Note: 10 trades filtered (would drop QB below minimum of 1), 5 trades filtered (would drop RB below minimum of 3)"
- Pros: Full transparency, helps user understand constraints
- Cons: Might be verbose

**Recommendation**: Option B - Summary message. Users should know filtering occurred but don't need per-trade details.

**Your Answer**: Option A

---

## Question 6: Configuration Validation

**Context**: MIN_POSITIONS and MAX_POSITIONS are defined separately (MIN in constants.py, MAX in league_config.json). There could be conflicts.

**Question**: Should we validate that MIN_POSITIONS <= MAX_POSITIONS for each position?

**Options**:

**A. No validation**
- Description: Assume constants are correct, no runtime checks
- Pros: Simpler, faster
- Cons: Could have nonsensical configuration (MIN > MAX)

**B. Validation with warning**
- Description: Check MIN <= MAX at startup, log warning if violated
- Example: `logger.warning("MIN_POSITIONS[QB]=3 exceeds MAX_POSITIONS[QB]=2")`
- Pros: Catches configuration errors, non-blocking
- Cons: Warning might be ignored

**C. Validation with error**
- Description: Check MIN <= MAX at startup, raise exception if violated
- Pros: Forces valid configuration
- Cons: Could break application if config is wrong

**Recommendation**: Option B - Validation with warning. Log a clear warning but allow application to continue.

**Your Answer**: Option B

---

## Summary

Please answer each question with your chosen option (A, B, or C) or provide alternative guidance. Your answers will be integrated into the implementation plan.

**Example response format:**
```
Q1: A
Q2: B
Q3: A
Q4: A
Q5: B
Q6: B
```

Or provide detailed explanations if you prefer a different approach for any question.
