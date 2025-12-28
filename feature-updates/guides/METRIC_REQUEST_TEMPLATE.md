# Feature Request: [Metric Name]

**Metric ID:** [e.g., M##]
**Priority:** [HIGH / MEDIUM / LOW]
**Positions:** [QB, RB, WR, TE, K, DST - or specific positions]
**Effort Estimate:** [X-Y hours]
**Expected Impact:** [Brief description of expected improvement]

---

## What This Metric Is

[1-2 sentence clear definition of what the metric measures]

---

## What We're Trying to Accomplish

[Bulleted list of specific goals and use cases]

**Goals:**
- **[Goal 1]**: [Explanation with context]
- **[Goal 2]**: [Explanation with context]
- **[Goal 3]**: [Explanation with context]

**Example Use Case:**
[Concrete real-world example showing how this metric helps make better decisions. Use actual player names and scenarios when possible.]

Example:
> Player X with [metric value] indicates [interpretation], making them [actionable insight] compared to Player Y with [different metric value].

---

## Data Requirements

### Available Data Sources

**Status:** ✅ FULLY AVAILABLE / ⚠️ PARTIALLY AVAILABLE / ❌ NOT AVAILABLE

**Data Location:** `data/player_data/[position]_data.json`

**Required Fields:**

| Field Name | Data Type | Weekly Array? | Source | Example Value |
|------------|-----------|---------------|--------|---------------|
| `field_name` | int/float | Yes/No | JSON path | 8.5 |

**Example Data Structure:**
```json
{
  "id": "player_id",
  "name": "Player Name",
  "position": "RB",
  "category": {
    "stat_field": [0.0, 0.0, 0.0, ...]  // 17 weeks
  }
}
```

### Data Validation
- ✅ Data verified in: `[file paths]`
- ✅ Weekly granularity: [Yes/No]
- ✅ Historical availability: [2021-2024]
- ⚠️ Known limitations: [List any gaps or issues]

---

## Calculation Formula

### Mathematical Definition

```python
def calculate_[metric_name](player: FantasyPlayer, week: int) -> float:
    """
    Calculate [metric name] for a player.

    Args:
        player: FantasyPlayer object with stats
        week: Current NFL week (1-17)

    Returns:
        float: [Metric value with units]

    Example:
        >>> player = FantasyPlayer(name="Example", stats={...})
        >>> result = calculate_[metric_name](player, week=8)
        >>> result
        15.7  # [units]
    """
    # Step 1: Extract required data
    stat_a = player.stats['category']['field_a']
    stat_b = player.stats['category']['field_b']

    # Step 2: Calculate derived values
    derived_value = stat_a / stat_b if stat_b > 0 else 0.0

    # Step 3: Apply position-specific logic (if applicable)
    if player.position == 'RB':
        # RB-specific calculation
        pass

    # Step 4: Return final metric
    return derived_value
```

### Thresholds & Tiers

**Position-Specific Thresholds:**

**[Position] (e.g., RB):**

| Tier | Threshold | Description | Multiplier | Example Player |
|------|-----------|-------------|------------|----------------|
| EXCELLENT | ≥ [value] | [Description] | 1.05 | [Name] |
| GOOD | [range] | [Description] | 1.025 | [Name] |
| AVERAGE | [range] | [Description] | 1.0 | [Name] |
| POOR | < [value] | [Description] | 0.975 | [Name] |

**[Position] (e.g., WR):**
[Repeat structure for each applicable position]

### Edge Cases

**1. [Edge Case Name]**
- **Scenario:** [Description]
- **Handling:** [How to handle it]
- **Example:** [Concrete example]

**2. [Edge Case Name]**
- **Scenario:** [Description]
- **Handling:** [How to handle it]
- **Example:** [Concrete example]

---

## Implementation Plan

### Phase 1: Data Pipeline (Estimated: X hours)

**1.1 Verify Data Availability**
- [ ] Confirm all required fields exist in `data/player_data/*.json`
- [ ] Test data extraction with sample players
- [ ] Validate data ranges and types

**1.2 Create Calculation Module**

**File:** `league_helper/util/[MetricName]Calculator.py`

```python
from typing import Tuple
from league_helper/util/FantasyPlayer import FantasyPlayer
from utils.LoggingManager import get_logger

class [MetricName]Calculator:
    """Calculate [metric name] for players"""

    def __init__(self, config_manager):
        self.config = config_manager
        self.logger = get_logger()

    def calculate(self, player: FantasyPlayer) -> Tuple[float, str]:
        """
        Calculate metric value and tier.

        Returns:
            Tuple[float, str]: (metric_value, tier_classification)
        """
        # Implementation
        pass
```

---

### Phase 2: Configuration (Estimated: X hours)

**2.1 Add to league_config.json**

```json
{
  "[METRIC_NAME]_SCORING": {
    "ENABLED": true,
    "POSITION_SPECIFIC": {
      "[POSITION]": {
        "THRESHOLDS": {
          "BASE_POSITION": [value],
          "DIRECTION": "INCREASING/DECREASING",
          "STEPS": [value]
        },
        "MULTIPLIERS": {
          "VERY_POOR": 0.95,
          "POOR": 0.975,
          "GOOD": 1.025,
          "EXCELLENT": 1.05
        },
        "WEIGHT": [value]
      }
    },
    "MIN_WEEKS": 3,
    "IMPACT_SCALE": [value if additive],
    "DESCRIPTION": "[Brief description for documentation]"
  }
}
```

**2.2 Configuration Parameters**

| Parameter | Default | Description | Typical Range |
|-----------|---------|-------------|---------------|
| `WEIGHT` | 1.0 | Multiplier exponent | 0.5 - 3.0 |
| `MIN_WEEKS` | 3 | Minimum weeks of data | 1 - 6 |
| `IMPACT_SCALE` | [value] | Additive bonus scale | 20.0 - 100.0 |

---

### Phase 3: Scoring Integration (Estimated: X hours)

**3.1 Add Scoring Step**

**File:** `league_helper/util/player_scoring.py`

**Method:** `_apply_[metric_name]_scoring()` (insert at appropriate line number)

```python
def _apply_[metric_name]_scoring(self, p: FantasyPlayer, player_score: float) -> Tuple[float, str]:
    """
    Apply [metric name] adjustment to player score.

    Args:
        p: FantasyPlayer object
        player_score: Current player score

    Returns:
        Tuple[float, str]: (adjusted_score, reason_string)
    """
    # Skip if not applicable
    if p.position not in ['RB', 'WR', 'TE']:  # Adjust positions as needed
        return player_score, ""

    # Skip if disabled
    if not self.config.[metric_name]_scoring.get('ENABLED', False):
        return player_score, ""

    # Calculate metric
    calculator = [MetricName]Calculator(self.config)
    metric_value, tier = calculator.calculate(p)

    # Get multiplier/bonus
    multiplier, rating = self.config.get_[metric_name]_multiplier(metric_value)

    # Apply to score
    # OPTION A: Multiplier-based (Pattern 1)
    adjusted_score = player_score * multiplier

    # OPTION B: Additive bonus (Pattern 2)
    # impact_scale = self.config.[metric_name]_scoring.get('IMPACT_SCALE', 50.0)
    # weight = self.config.[metric_name]_scoring.get('WEIGHT', 1.0)
    # bonus = ((impact_scale * multiplier) - impact_scale) * weight
    # adjusted_score = player_score + bonus

    # Build reason string
    reason = f"[Metric Name] ({rating}): {metric_value:.1f} [units]"

    return adjusted_score, reason
```

**3.2 Update ConfigManager**

**File:** `league_helper/util/ConfigManager.py`

Add method (insert at appropriate line number):

```python
def get_[metric_name]_multiplier(self, metric_value: float) -> Tuple[float, str]:
    """
    Get multiplier for [metric name].

    Args:
        metric_value: Calculated metric value

    Returns:
        Tuple[float, str]: (multiplier, rating)
    """
    return self._get_multiplier(
        self.[metric_name]_scoring,
        metric_value,
        rising_thresholds=True  # or False if DECREASING
    )
```

---

### Phase 4: Testing (Estimated: X hours)

**4.1 Unit Tests**

**File:** `tests/league_helper/util/test_[MetricName]Calculator.py`

```python
import pytest
from league_helper.util.[MetricName]Calculator import [MetricName]Calculator
from league_helper.util.FantasyPlayer import FantasyPlayer

class Test[MetricName]Calculator:
    """Test [metric name] calculation"""

    @pytest.fixture
    def calculator(self, mock_config):
        return [MetricName]Calculator(mock_config)

    def test_calculation_normal_case(self, calculator):
        """Test metric calculation with typical values"""
        player = FantasyPlayer(
            name="Test Player",
            position="RB",
            stats={...}
        )

        result, tier = calculator.calculate(player)

        assert result == pytest.approx(expected_value, rel=0.01)
        assert tier == "EXPECTED_TIER"

    def test_edge_case_zero_denominator(self, calculator):
        """Test handling of division by zero"""
        player = FantasyPlayer(...)

        result, tier = calculator.calculate(player)

        assert result == 0.0
        assert tier == "N/A"

    def test_position_filtering(self, calculator):
        """Test metric only applies to correct positions"""
        # Test with applicable position
        rb_player = FantasyPlayer(position="RB", ...)
        rb_result, _ = calculator.calculate(rb_player)
        assert rb_result > 0

        # Test with non-applicable position
        qb_player = FantasyPlayer(position="QB", ...)
        qb_result, _ = calculator.calculate(qb_player)
        assert qb_result == 0.0  # or appropriate default
```

**4.2 Integration Tests**

**File:** `tests/integration/test_[metric_name]_integration.py`

```python
def test_[metric_name]_end_to_end():
    """Test full workflow from data load to score adjustment"""
    # 1. Load player data
    # 2. Calculate metric
    # 3. Apply to score
    # 4. Verify adjustment
    pass
```

**4.3 Validation Test Cases**

Use real player data from 2024 season to validate:

```python
validation_cases = [
    {
        'player_name': 'Player Name',
        'position': 'RB',
        'expected_metric_value': 15.7,
        'expected_tier': 'EXCELLENT',
        'rationale': 'Known high performer in this metric'
    },
    # Add 3-5 validation cases
]
```

---

### Phase 5: Documentation (Estimated: 1 hour)

**5.1 Create Scoring Documentation**

**File:** `docs/scoring/[NN]_[metric_name]_scoring.md`

Follow the pattern from existing scoring docs (e.g., `11_temperature_scoring.md`):

- Overview table
- Purpose and rationale
- Mode usage table
- Calculation details
- Configuration parameters
- Real player examples
- Edge cases
- Implementation references

**5.2 Update Checklist**

Update `docs/research/metrics_implementation_checklist.md`:

```markdown
### ✅ [N]. [Metric Name]

**Status:**
- [x] Feature Request file created
- [x] Metric has been implemented

**Details:**
- Positions: [RB, WR, etc.]
- Data Required: [fields]
- Expected bonus range: ±X.X pts
```

---

## Expected Impact

### Mode-Specific Impact

**Add To Roster Mode:**
- Expected improvement: [X-Y%]
- Rationale: [Why this metric helps draft decisions]

**Starter Helper Mode:**
- Expected improvement: [X-Y%]
- Rationale: [Why this metric helps weekly lineup decisions]

**Trade Simulator Mode:**
- Expected improvement: [X-Y%]
- Rationale: [Why this metric helps trade evaluation]

### Accuracy Metrics

**Target Improvements:**
- Overall prediction accuracy: +[X-Y%]
- [Position] projections: +[X-Y%]
- Reduce prediction error: -[X-Y%]

**Success Criteria:**
- ✅ Metric calculates correctly for 100% of applicable players
- ✅ Unit tests: 100% pass rate
- ✅ Integration tests: End-to-end workflow verified
- ✅ Validation: Real player examples match expected values
- ✅ Documentation: Complete scoring step documentation created

---

## Real-World Examples

### Example 1: [High Tier Player]

**[Player Name] ([Team], [Position])** - [Season/Week]:

| Metric | Value |
|--------|-------|
| [Stat 1] | [value] |
| [Stat 2] | [value] |
| [Calculated Metric] | [value] |
| Tier | EXCELLENT |
| Multiplier | 1.05 |
| Base Score | 150.0 |
| Adjusted Score | 157.5 (+7.5 pts) |

**Reason String:** `"[Metric Name] (EXCELLENT): [value] [units]"`

### Example 2: [Low Tier Player]

**[Player Name] ([Team], [Position])** - [Season/Week]:

| Metric | Value |
|--------|-------|
| [Stat 1] | [value] |
| [Stat 2] | [value] |
| [Calculated Metric] | [value] |
| Tier | POOR |
| Multiplier | 0.975 |
| Base Score | 130.0 |
| Adjusted Score | 126.8 (-3.2 pts) |

**Reason String:** `"[Metric Name] (POOR): [value] [units]"`

### Example 3: [Edge Case]

[Description of edge case scenario with concrete example]

---

## Dependencies

### Data Dependencies
- ✅ [Required field 1] - Available in `[file path]`
- ✅ [Required field 2] - Available in `[file path]`
- ⚠️ [Optional field] - Would enhance metric if available

### Code Dependencies
- ✅ `ConfigManager` - Existing
- ✅ `PlayerManager` - Existing
- ✅ `FantasyPlayer` - Existing
- 🆕 `[MetricName]Calculator` - To be created

### External Dependencies
- None / [List any external libraries needed]

---

## Risks & Mitigations

### Risk 1: [Risk Name]

**Likelihood:** [High/Medium/Low]
**Impact:** [High/Medium/Low]

**Description:** [What could go wrong]

**Mitigation:**
- [Mitigation strategy 1]
- [Mitigation strategy 2]

### Risk 2: [Risk Name]

**Likelihood:** [High/Medium/Low]
**Impact:** [High/Medium/Low]

**Description:** [What could go wrong]

**Mitigation:**
- [Mitigation strategy 1]
- [Mitigation strategy 2]

---

## Open Questions

**Questions for User:**
1. [Question 1 about requirements or implementation approach]
2. [Question 2 about thresholds or configurations]
3. [Question 3 about priorities or scope]

**Technical Questions:**
1. [Question 1 about implementation details]
2. [Question 2 about data availability]

---

## Related Metrics

**Complementary Metrics:**
- [Metric Name 1] - [How they work together]
- [Metric Name 2] - [How they work together]

**Overlapping Metrics:**
- [Metric Name] - [How this differs or improves upon it]

**Prerequisites:**
- [Metric Name] - [Must be implemented first if dependency exists]

---

## Future Enhancements

**Phase 2 Potential Additions:**
1. [Enhancement 1] - [What it would add]
2. [Enhancement 2] - [What it would add]
3. [Enhancement 3] - [What it would add]

**Research Needed:**
- [Research area 1 that could improve the metric]
- [Research area 2 that could improve the metric]

---

## Implementation Checklist

**Pre-Implementation:**
- [ ] Data availability verified
- [ ] Formula validated with sample calculations
- [ ] Configuration structure designed
- [ ] User questions answered

**Implementation:**
- [ ] Calculator module created
- [ ] Scoring integration added
- [ ] ConfigManager methods added
- [ ] Configuration file updated

**Testing:**
- [ ] Unit tests written and passing
- [ ] Integration tests written and passing
- [ ] Validation against real player data complete
- [ ] Edge cases tested

**Documentation:**
- [ ] Scoring step documentation created
- [ ] Implementation checklist updated
- [ ] Code comments added
- [ ] User guide updated (if needed)

**Completion:**
- [ ] All tests passing (100% pass rate)
- [ ] Code reviewed
- [ ] Feature request file moved to `done/`
- [ ] Committed with descriptive message

---

**END OF FEATURE REQUEST**
