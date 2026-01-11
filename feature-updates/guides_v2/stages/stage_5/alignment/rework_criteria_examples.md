# Stage 5d: Significant Rework Criteria & Real-World Examples

**Purpose:** Decision framework and examples for routing features needing changes back to appropriate stages
**Prerequisites:** Completed alignment review for features in post_feature_alignment.md
**Main Guide:** `stages/stage_5/post_feature_alignment.md`

---

## Overview

When reviewing remaining features during Stage 5d, you'll discover misalignments between specs and actual implementation. This reference provides clear criteria for deciding:
- Which features can continue with minor updates
- Which features need to return to Stage 5a, Stage 2, or Stage 1
- How to communicate rework needs to users

---

## Significant Rework Criteria (Detailed)

**Purpose:** Clear decision tree for routing features that need changes

---

### Criteria Table

| Condition | Return To | Reason | Example |
|-----------|-----------|--------|---------|
| Feature should be split into 2+ features | **Stage 1** | Epic structure changes | "Player rating" became "rating_collection", "rating_processing", "rating_application" |
| Feature no longer needed | **Stage 1** | Epic scope changes | Implementation revealed feature is redundant with existing system |
| NEW feature discovered | **Stage 1** | Epic expansion | "Need authentication feature we didn't plan for" |
| Core approach fundamentally wrong | **Stage 2** | Requires redesign | "Player rating API deprecated, need different source" |
| Spec assumptions invalid | **Stage 2** | Research needed | "Assumed CSV format, but API returns JSON only" |
| External dependency missing | **Stage 2** | Alternative needed | "Required library no longer maintained" |
| Algorithm needs major change | **Stage 2** | Approach redesign | "Linear scaling won't work, need ML model" |
| >3 new implementation tasks needed | **Stage 5a** | TODO list rework | "Interface change affects 7 callsites" |
| Algorithm change (same approach) | **Stage 5a** | TODO updates | "Add caching layer, 4 new implementation tasks" |
| Interface signature changes | **Stage 5a** | Integration updates | "Method now returns Tuple not float, update callers" |
| ≤3 TODO adjustments | **Continue** | Minor updates | "Update file path, add 2 tasks" |
| Pattern following | **Continue** | Consistency | "Follow established ConfigManager pattern" |
| No algorithm changes | **Continue** | Clarification only | "Column name updated in spec" |

---

### Decision Tree

```
Did implementation reveal changes needed?
    │
    ├─ NO → Continue with feature (no rework needed)
    │
    └─ YES → Evaluate impact:
         │
         ├─ Should feature be split into multiple features?
         │   └─ YES → Return to Stage 1 (Epic Planning)
         │
         ├─ Is feature no longer needed?
         │   └─ YES → Return to Stage 1 (get user approval to remove)
         │
         ├─ Are spec assumptions fundamentally wrong?
         │   └─ YES → Return to Stage 2 (Deep Dive)
         │
         ├─ Is external dependency missing/changed?
         │   └─ YES → Return to Stage 2 (find alternative)
         │
         ├─ Does algorithm need complete redesign?
         │   └─ YES → Return to Stage 2 (rethink approach)
         │
         ├─ Will spec changes require >3 new implementation tasks?
         │   └─ YES → Return to Stage 5a (Implementation Planning)
         │
         ├─ Did algorithm change significantly (but approach valid)?
         │   └─ YES → Return to Stage 5a (update implementation plan)
         │
         └─ Minor updates (≤3 implementation tasks, no algorithm change)?
             └─ YES → Continue (update spec, proceed normally)
```

---

### Quick Examples by Rework Type

**Example 1: Return to Stage 1**
```
Just completed: feature_01_adp_integration

Reviewing: feature_02_player_rating_integration

Finding: Rating integration actually needs 3 separate features:
  1. rating_data_collection (fetch from API)
  2. rating_calculation (compute ratings from stats)
  3. rating_integration (apply to scoring)

Original spec tried to do all 3 in one feature (too large, complex).

Decision: RETURN TO STAGE 1
- Split feature_02 into 3 features
- Update epic structure
- User approves split
- Continue with new feature breakdown
```

---

**Example 2: Return to Stage 2**
```
Just completed: feature_01_adp_integration

Reviewing: feature_03_schedule_strength

Finding: Spec assumes NFL schedule data available via API endpoint
Implementation check: API endpoint returns 404 (no longer exists)

Root cause: NFL changed API in 2025, old endpoint deprecated

Decision: RETURN TO STAGE 2
- Research alternative schedule data sources
- Identify web scraping vs paid API options
- Get user decision on approach
- Update spec with new source
- Then proceed to Stage 5a
```

---

**Example 3: Return to Stage 5a**
```
Just completed: feature_01_adp_integration

Reviewing: feature_04_injury_risk_assessment

Finding: Spec assumes ConfigManager.get_injury_penalty(status: str) -> float
Actual: ConfigManager methods return Tuple[float, int] (established by ADP)

Impact analysis:
- Need to update 7 callsites to handle tuple unpacking
- Need to add injury_score display in UI (new)
- Need to add injury_score to CSV output (new)
- Need to add injury_score to tests (new)
Total: 6 new implementation tasks

Decision: RETURN TO STAGE 5a
- Update spec with correct interface
- Recreate TODO list with 6 additional tasks
- Then proceed with implementation
```

---

**Example 4: Continue (Minor Updates)**
```
Just completed: feature_01_adp_integration

Reviewing: feature_05_bye_week_penalties

Finding: Spec has data file at `data/bye_weeks.csv`
Pattern: ADP used `data/player_data/adp_data.csv`
Update: Should be `data/player_data/bye_week_data.csv` for consistency

Impact analysis:
- File path change in 2 places (load and save)
- Column names stay same
- No algorithm changes
Total: 2 minor TODO adjustments

Decision: CONTINUE (Minor Updates)
- Update spec.md with correct file path
- Note in spec: "Following data/player_data/ pattern from feature_01"
- Proceed to Stage 5a normally
- Existing TODO list still mostly valid
```

---

## Real-World Examples (Detailed)

### Example 1: Interface Pattern Discovered During Implementation

**Just completed:** feature_01_adp_integration

**Reviewing:** feature_02_player_rating_integration, feature_03_schedule_strength, feature_04_injury_risk

**Finding:**

Original specs assumed each feature would call ConfigManager with simple method:
```python
# feature_02 spec:
rating = config.get_rating(player.id)

# feature_03 spec:
strength = config.get_schedule_strength(player.team)

# feature_04 spec:
risk = config.get_injury_risk(player.injury_status)
```

**Actual implementation in feature_01:**
```python
# Actual code in ConfigManager.py:
def get_adp_multiplier(self, adp_value: float) -> Tuple[float, int]:
    """
    Calculate ADP multiplier and rating score.

    Returns:
        Tuple[float, int]: (multiplier, rating_score)
            - multiplier: Applied to player score
            - rating_score: 0-100 for debugging/display
    """
    # Implementation...
```

**Insight:** ConfigManager methods return Tuple[multiplier, score] for transparency and debugging.

**Action for feature_02:**
```markdown
## Configuration Integration

**[UPDATED based on feature_01_adp_integration implementation - 2025-12-30]**

ConfigManager methods follow pattern of returning Tuple[float, int] where:
- First value: multiplier to apply to score
- Second value: 0-100 rating for debugging/transparency

Updated interface:
```python
def get_rating_multiplier(self, player_id: int) -> Tuple[float, int]:
    """
    Calculate player rating multiplier.

    Returns:
        Tuple[float, int]: (rating_multiplier, rating_score)
    """
```

Integration in PlayerManager:
```python
rating_multiplier, rating_score = self.config.get_rating_multiplier(player.id)
player.rating_multiplier = rating_multiplier  # For scoring
player.rating_score = rating_score  # For display/debugging
final_score *= rating_multiplier
```

See feature_01 implementation in ConfigManager.py:234 for pattern reference.
```

**Result:**
- feature_02: Minor update (continue to Stage 5a normally)
- feature_03: Minor update (continue to Stage 5a normally)
- feature_04: Minor update (continue to Stage 5a normally)
- All 3 features now aligned with established pattern
- Saves hours of rework during implementation

---

### Example 2: Data Source Unavailable - Major Rework Needed

**Just completed:** feature_01_adp_integration (used ESPN API)

**Reviewing:** feature_03_schedule_strength

**Original spec assumption:**
```markdown
## Data Source

Schedule strength data will be fetched from NFL Official Stats API:
- Endpoint: https://api.nfl.com/stats/schedule
- Authentication: API key from user config
- Format: JSON with team schedules and opponent rankings
```

**Verification during alignment review:**
```bash
# Test API endpoint
curl https://api.nfl.com/stats/schedule
# Result: 404 Not Found

# Research: API was deprecated in 2024
# NFL now requires paid subscription for official stats
```

**Impact:**
- Original approach not viable
- Need alternative data source
- Spec assumptions fundamentally wrong

**Decision:** Return to Stage 2 (Deep Dive)

**User communication:**
```markdown
After reviewing feature_03 spec based on feature_01 implementation, I discovered:

## feature_03_schedule_strength REQUIRES MAJOR REWORK

**Issue:** NFL Official Stats API (spec's assumed data source) was deprecated in 2024.
Current endpoint returns 404. NFL now requires paid subscription ($500/month) for official data.

**Impact:** Cannot implement as spec currently written

**Recommendation:** Return to Stage 2 (Deep Dive) to research alternatives:

**Option 1:** Use ESPN API (same source as feature_01 uses for ADP data)
- Pros: Free, accessible, already integrated
- Cons: Less detailed than NFL official stats

**Option 2:** Use Pro Football Reference web scraping
- Pros: Comprehensive data, free
- Cons: Fragile (HTML changes break scraper), legally grey

**Option 3:** Use paid API subscription
- Pros: Official data, reliable
- Cons: $500/month cost

What would you like to do?
1. Return to Stage 2 to research ESPN API option (recommended)
2. Return to Stage 2 to evaluate web scraping
3. Defer feature_03 until budget available for paid API
4. Remove feature_03 from epic entirely
```

**User response:** "Go with Option 1, use ESPN API"

**Action:**
1. Mark feature_03 spec with rework status
2. Update epic README showing feature_03 returned to Stage 2
3. Continue reviewing feature_04 (don't let rework block other reviews)
4. After completing Stage 5d for all features, return to feature_03 Stage 2

---

### Example 3: Minor Updates Applied Proactively

**Just completed:** feature_01_adp_integration

**Reviewing:** feature_05_bye_week_penalties

**Original spec:**
```markdown
## Data Files

Bye week data stored in:
- Location: `data/bye_weeks.csv`
- Columns: `[team, bye_week]`
- Format: CSV with header row

## Configuration

Bye week penalty stored in:
- Config key: `penalties.bye_week`
- Type: float (negative value)
- Default: -5.0
```

**Actual implementation from feature_01:**
```python
# File location pattern established:
ADP_DATA_FILE = data_folder / "player_data" / "adp_data.csv"

# Config key pattern established:
self.config['scoring']['adp']['multiplier_curve']
```

**Comparison:**
- File location: Spec has `data/bye_weeks.csv`, pattern is `data/player_data/`
- Config key: Spec has `penalties.bye_week`, pattern is `scoring.{feature}.{setting}`

**Impact:** MINOR - just following established patterns for consistency

**Updates applied:**
```markdown
## Data Files

**[UPDATED based on feature_01_adp_integration implementation - 2025-12-30]**

Following established pattern from feature_01, bye week data stored in:
- Location: `data/player_data/bye_week_data.csv` (not `data/bye_weeks.csv`)
- Columns: `[team, bye_week]`
- Format: CSV with header row

Rationale: All player-related data in `data/player_data/` subdirectory for organization.

## Configuration

**[UPDATED based on feature_01_adp_integration implementation - 2025-12-30]**

Following established pattern from feature_01, bye week configuration:
- Config key: `scoring.bye_week.penalty` (not `penalties.bye_week`)
- Type: float (negative value)
- Default: -5.0

Rationale: All scoring-related settings under `scoring` namespace for consistency.
```

**Checklist.md updates:**
```markdown
## Configuration Questions
- [x] What config key structure? → **RESOLVED:** Follow `scoring.{feature}.{setting}` pattern from feature_01
- [x] Where to store data files? → **RESOLVED:** Use `data/player_data/` pattern from feature_01
```

**Result:**
- feature_05: Minor updates, continue to Stage 5a normally
- Spec now aligned with established patterns
- Prevents "why is this different?" questions during implementation

**Commit:**
```bash
git commit -m "Update feature_05 spec to follow feature_01 patterns

- Data file location: data/player_data/bye_week_data.csv
- Config key: scoring.bye_week.penalty
- Ensures consistency across epic features"
```

---

## User Communication Templates

### Template 1: Major Rework (Return to Stage 1 or 2)

```markdown
After reviewing remaining feature specs based on feature_{completed} implementation, I found:

## feature_{X}_{name} REQUIRES MAJOR REWORK

**Issue:** {Clear description of what's wrong}

**Impact:** {Why it can't be implemented as currently spec'd}

**Recommendation:** Return to Stage {1 or 2} ({Stage name})
- {Step 1: What needs to be done}
- {Step 2: What needs to be done}
- {Step 3: What needs to be done}

**Options:**
1. {Primary recommendation with rationale}
2. {Alternative option}
3. {Defer or remove option}

What would you like to do?
```

### Template 2: Moderate Rework (Return to Stage 5a)

```markdown
During Stage 5d alignment review, I found feature_{X}_{name} needs significant updates:

**Changes needed:**
- {Change 1 with impact}
- {Change 2 with impact}
- {Change 3 with impact}

**Impact analysis:**
- {N} new implementation tasks required
- {Describe scope of changes}

**Recommendation:** Return to Stage 5a (Implementation Planning) to:
- Update spec.md with corrected interfaces/algorithms
- Recreate implementation_plan.md with additional tasks
- Then proceed to Stage 5b implementation

This will take approximately {time estimate} before we can begin implementation.

Does this approach work for you?
```

### Template 3: Minor Updates (No Rework)

```markdown
Reviewed feature_{X}_{name} spec - found minor alignment updates needed:

**Updates:**
- {Update 1: Follow established pattern from feature_{completed}}
- {Update 2: Clarify interface to match actual implementation}

These are minor spec clarifications (≤3 implementation task changes).
Feature can proceed to Stage 5a normally after spec updates.

I'll update the spec now and continue with alignment review.
```

---

## Summary

**Rework Decision Framework:**
1. **Count new implementation tasks needed:** >3 = Stage 5a minimum
2. **Check if spec assumptions valid:** Invalid = Stage 2
3. **Check if feature scope changed:** Split/remove = Stage 1
4. **Minor updates only:** Continue normally with spec updates

**User Approval Required For:**
- Any return to Stage 1 or Stage 2
- Any feature removal or split
- Any approach that requires significant additional time/effort

**Agent Can Proceed Without User Approval For:**
- Minor spec clarifications (≤3 tasks)
- Following established patterns from completed features
- Updating specs to match actual implementation details

**Key Principle:** Better to catch misalignments NOW during Stage 5d than discover them mid-implementation during Stage 5b.

---

**END OF REWORK CRITERIA & EXAMPLES**
