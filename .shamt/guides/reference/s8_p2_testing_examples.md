# S8.P2: Epic Testing Update - Real-World Examples

**Reference File:** Detailed examples of how to update epic_smoke_test_plan.md after feature completion

**Main Guide:** stages/s8/s8_p2_epic_testing_update.md

**When to use:** Reference these examples when updating testing plan in S8.P2

---

## Examples

### Example 1: Adding Integration Point Test

**Just completed:** feature_01_rank_integration

**Implementation review reveals:**
```python
## File: [module]/util/RecordManager.py

def calculate_total_score(self, item: DataRecord) -> float:
    """Calculate final item score with all multipliers."""

    # Start with projected points
    score = item.projected_value

    # Apply rank multiplier (NEW in feature_01)
    rank_multiplier, rank_score = self.config.get_rank_multiplier(item.rank)
    item.rank_multiplier = rank_multiplier  # Store for display
    item.rank_score = rank_score  # Store for debugging
    score *= rank_multiplier  # Apply to final score

    return score
```

**Current test plan (from S4):**
```markdown
### Scenario 3: Scoring Calculation

**What to test:** Verify item scores calculated correctly

**How to test:**
- Load items
- Calculate scores
- Check scores are reasonable

**Expected result:** Items have scores
```

**S8.P2 (Epic Testing Update) updates:**

**Update existing scenario:**
```markdown
### Scenario 3: Scoring Calculation

**What to test:** Verify item scores calculated correctly

**How to test:**
1. Load items:
   ```
   python run_[module].py --mode draft
   ```markdown

2. Review recommendations output:
   - Open data/recommendations.csv
   - **[UPDATED S8.P2 (Epic Testing Update) - feature_01]:** Verify all items have rank_multiplier column
   - **[UPDATED S8.P2 (Epic Testing Update) - feature_01]:** Verify all items have rank_score column
   - **[UPDATED S8.P2 (Epic Testing Update) - feature_01]:** Verify final_score = projected_value * rank_multiplier

**Expected result:**
- Items have scores
- **[UPDATED S8.P2 (Epic Testing Update) - feature_01]:** All rank_multiplier values between 0.85-1.50
- **[UPDATED S8.P2 (Epic Testing Update) - feature_01]:** All rank_score values between 0-100
- **[UPDATED S8.P2 (Epic Testing Update) - feature_01]:** Math verifies: final_score = projected * multiplier
```

**Add new integration scenario:**
```markdown
### Scenario 9: RecordManager → ConfigManager Integration

**Added:** S8.P2 (Epic Testing Update) (feature_01_rank_integration)

**What to test:** Verify RecordManager correctly integrates with ConfigManager for rank multipliers

**How to test:**
1. Create test item with known rank priority:
   - Item: "Test Item"
   - Position: QB
   - Projected Points: 300.0
   - rank priority: 10 (elite pick)

2. Run scoring calculation:
   ```
   python -c "
   from [module].util.RecordManager import RecordManager
   from [module].util.ConfigManager import ConfigManager
   from [module].util.DataRecord import DataRecord

   config = ConfigManager('data/')
   manager = RecordManager(config)

   item = DataRecord('Test-Item', 'A', projected_value=300.0, rank=10)
   score = manager.calculate_total_score(item)

   print(f'Final score: {score}')
   print(f'rank multiplier: {item.rank_multiplier}')
   print(f'rank score: {item.rank_score}')
   print(f'Math check: {300.0 * item.rank_multiplier}')
   "
   ```text

3. Verify integration:
   - ConfigManager.get_rank_multiplier() was called
   - Returned tuple was unpacked correctly
   - Multiplier was stored in item.rank_multiplier
   - Score was stored in item.rank_score
   - Final score = 300.0 * multiplier

**Expected result:**
- rank multiplier ≈ 1.45 (elite pick gets high multiplier)
- rank score ≈ 95 (elite rating)
- Final score ≈ 435.0 (300 * 1.45)
- Math check matches final score

**Why added:** Implementation revealed specific integration pattern (ConfigManager → tuple return → RecordManager unpacks and stores). S4 plan didn't specify this interaction. Need explicit test to ensure it works correctly.
```

**Result:** Test plan now has specific, executable test for integration point discovered during implementation.

---

### Example 2: Adding Edge Case Test

**Just completed:** feature_01_rank_integration

**Implementation review reveals:**
```python
## File: [module]/util/ConfigManager.py

def get_rank_multiplier(self, rank_value: float) -> Tuple[float, int]:
    """Calculate rank multiplier."""

    # Handle missing rank data
    if rank_value is None or rank_value == 0:
        self.logger.info(f"rank value missing or zero, using neutral multiplier")
        return (1.0, 50)  # Neutral multiplier, mid-range score

    # Handle undrafted items (rank > 250)
    if rank_value > 250:
        rank_value = 250  # Cap at 250

    # Calculate multiplier...
```

**Current test plan (from S4):**
- No edge case scenarios for missing data or boundary conditions

**S8.P2 (Epic Testing Update) update - Add new scenario:**
```markdown
### Scenario 10: Edge Case - Missing rank priority Data

**Added:** S8.P2 (Epic Testing Update) (feature_01_rank_integration)

**What to test:** Verify system handles items with missing rank data gracefully

**How to test:**
1. Create test scenario:
   - Edit data/rankings/priority.csv
   - Remove entry for "Record-A"
   - Ensure "Record-A" exists in data/items.csv

2. Run draft mode:
   ```
   python run_[module].py --mode draft
   ```bash

3. Check output:
   - Open data/recommendations.csv
   - Find "Record-A" row
   - Verify rank_multiplier = 1.0 (neutral)
   - Verify rank_score = 50 (mid-range)
   - Verify final_score = projected_value * 1.0 (no advantage/penalty)

4. Check logs:
   - Should have INFO log: "rank value missing or zero, using neutral multiplier"
   - Should NOT have ERROR or WARNING

**Expected result:**
- "Record-A" appears in recommendations (not excluded)
- rank_multiplier = 1.0 exactly
- rank_score = 50 exactly
- No crashes, exceptions, or errors
- Missing rank priority doesn't advantage or penalize item

**Why added:** Implementation discovered fallback behavior for missing rank data (returns neutral multiplier 1.0). This wasn't specified in original spec and needs explicit testing to ensure it works correctly. Important for data quality scenarios where rank data is incomplete.
```

**Add another edge case scenario:**
```markdown
### Scenario 11: Edge Case - rank priority Rank > 250

**Added:** S8.P2 (Epic Testing Update) (feature_01_rank_integration)

**What to test:** Verify system caps rank priority ranks above 250 to prevent extreme penalties

**How to test:**
1. Create test scenario:
   - Edit data/rankings/priority.csv
   - Add test item: "Test-Item,A,TEST,500,500.0"
   - rank priority rank 500 (very late pick)

2. Run draft mode:
   ```
   python run_[module].py --mode draft
   ```bash

3. Check output:
   - Open data/recommendations.csv
   - Find "Test-Item" row
   - Verify rank_multiplier ≈ 0.85 (minimum, capped)
   - Verify rank_score ≈ 0 (lowest rating)
   - Compare to item with rank priority rank 250 (should have same multiplier)

**Expected result:**
- rank priority rank 500 gets same multiplier as rank 250 (both capped at 0.85)
- No extreme penalties for very late picks
- Multiplier doesn't go below 0.85

**Why added:** Implementation discovered capping behavior for rank priority > 250. Prevents extreme penalties for late-round picks. Need test to verify cap is applied correctly and consistently.
```

**Result:** Test plan now covers edge cases discovered during implementation that weren't anticipated in S4.

---

### Example 3: Updating Success Criteria

**Just completed:** feature_01_rank_integration

**Implementation reveals:** System must handle missing data gracefully (wasn't in original epic success criteria)

**Original Epic Success Criteria (from S1):**
```markdown
## Epic Success Criteria
```

*Example 3 is a stub — content not yet written.*
