# S2 Refinement Phase - Phase 5 Examples: Cross-Feature Alignment

**Guide Version:** 1.0
**Created:** 2026-02-05 (Split from refinement_examples.md)
**Purpose:** Detailed examples for Phase 5 (Cross-Feature Alignment)
**Prerequisites:** Read stages/s2/s2_p3_refinement.md Phase 5 first
**Main Guide:** stages/s2/s2_p3_refinement.md
**Parent Reference:** reference/stage_2/refinement_examples.md

---

## Purpose

This reference provides detailed examples specifically for **Phase 5: Cross-Feature Alignment** of the Refinement Phase (S2.P3).

**What's Covered:**
- Complete feature comparison workflows (pairwise comparison)
- Conflict identification and resolution examples
- Alignment without conflicts (clean comparison example)
- Comparison categories and systematic approach

**When to Use:** During S2.P3 Phase 5 when comparing features pairwise to identify and resolve conflicts

**Always read the main guide first.** This is a reference supplement, not a standalone guide.

---

## Phase 5 Examples: Cross-Feature Alignment

### Example 1: Complete Feature Comparison

```markdown
## Alignment Check: Feature 02 vs Feature 01

**Date:** 2026-01-10
**Current Feature:** Feature 02: Injury Risk Assessment
**Comparison Target:** Feature 01: ADP Integration (S2 Complete)

---

## Comparison Categories

### 1. Components Affected

**Feature 02 modifies:**
- PlayerManager (calculate_total_score method)
- FantasyPlayer (add injury_risk field)
- InjuryDataLoader (new file)

**Feature 01 modifies:**
- PlayerManager (calculate_total_score method)
- FantasyPlayer (add adp_value field)
- ADPDataLoader (new file)

**Overlap Analysis:**
- ⚠️ Both modify PlayerManager.calculate_total_score()
  - Feature 01 adds: `total_score *= adp_multiplier`
  - Feature 02 adds: `total_score *= injury_multiplier`
  - **Conflict?** ❌ NO - Different multipliers, can coexist
  - **Resolution:** Both multiply into same total_score, order doesn't matter (multiplication is commutative)

- ⚠️ Both modify FantasyPlayer class
  - Feature 01 adds: adp_value, adp_multiplier fields
  - Feature 02 adds: injury_risk, injury_multiplier fields
  - **Conflict?** ❌ NO - Different fields, no overlap
  - **Resolution:** Both can add fields independently

**Verification:**
```
## After both features, FantasyPlayer will have:
@dataclass
class FantasyPlayer:
    # Existing fields
    name: str
    position: str
    # Feature 01 additions
    adp_value: Optional[int] = None
    adp_multiplier: float = 1.0
    # Feature 02 additions
    injury_risk: Optional[float] = None
    injury_multiplier: float = 1.0
```markdown

**Status:** ✅ No conflicts

---

### 2. Data Structures

**Feature 02 introduces:**
- Injury CSV format: Name, Position, InjuryStatus, RiskScore
- injury_risk field on FantasyPlayer (float, 0.0-1.0 range)

**Feature 01 introduces:**
- ADP CSV format: Name, Position, OverallRank
- adp_value field on FantasyPlayer (int, 1-300 range)

**Overlap Analysis:**
- ⚠️ Both use CSV files from data/ directory
  - Feature 01: data/adp_rankings.csv
  - Feature 02: data/injury_report.csv
  - **Conflict?** ❌ NO - Different files, different formats
  - **Resolution:** No overlap

- ⚠️ Both need to match players from CSV to player list
  - Feature 01: Uses player name matching (depends on Feature 05)
  - Feature 02: Uses player name matching (depends on Feature 05)
  - **Conflict?** ❌ NO - Both use same utility
  - **Resolution:** Both depend on Feature 05, consistent matching

**Status:** ✅ No conflicts

---

### 3. Requirements

**Feature 02 requirements:**
- Load injury data from CSV
- Calculate injury risk multiplier
- Apply multiplier in scoring

**Feature 01 requirements:**
- Load ADP data from CSV
- Calculate ADP multiplier
- Apply multiplier in scoring

**Overlap Analysis:**
- ✅ No duplicate requirements
- ✅ Similar patterns (both add multipliers) - this is intentional consistency
- ⚠️ Both depend on Feature 05 (player matching)
  - **Conflict?** ❌ NO - Both correctly specify dependency
  - **Resolution:** Feature 05 must be implemented first

**Status:** ✅ No conflicts, good consistency

---

### 4. Assumptions

**Feature 02 assumptions:**
- Injury CSV will be updated weekly (user responsibility)
- Missing injury data defaults to "healthy" (risk = 0.0, multiplier = 1.0)
- Injury risk calculated as: multiplier = 1.0 - (risk * 0.3)

**Feature 01 assumptions:**
- ADP CSV provided manually by user (no auto-updates)
- Missing ADP data defaults to neutral (multiplier = 1.0)
- ADP impact defined in config file

**Compatibility Check:**
- ✅ Compatible assumptions
- ⚠️ Both assume CSV files updated by user
  - This is consistent across features
  - Could suggest unified data update process (future enhancement)

**Status:** ✅ Compatible, no conflicts

---

### 5. Integration Points

**Does Feature 02 depend on Feature 01?**
- ❌ NO - Independent data sources, independent multipliers

**Does Feature 01 depend on Feature 02?**
- ❌ NO - Independent

**Do both depend on Feature 05?**
- ✅ YES - Both use player name matching utility

**Circular dependency?**
- ❌ NO

**Implementation order:**
1. Feature 05 (Player Matching) - FIRST (blocks both)
2. Features 01 and 02 can be parallel (after Feature 05)
3. No required sequence between 01 and 02

**Status:** ✅ No circular dependencies, clear order

---

## Summary

**Total Conflicts Found:** 0

**Critical Conflicts (must resolve):** NONE

**Minor Conflicts (nice to resolve):** NONE

**No Conflicts:**
- ✅ Components - Both modify PlayerManager but different logic
- ✅ Data Structures - Different CSV files, different fields
- ✅ Requirements - No duplicates, intentional consistency
- ✅ Assumptions - Compatible approaches
- ✅ Integration - Clear dependencies, no circular

**Action Items:**
- [ ] ✅ No changes needed to Feature 02 spec.md
- [ ] ✅ No changes needed to Feature 01 spec.md
- [ ] ✅ Document alignment verification in Feature 02 spec

**Alignment Status:** ✅ PASS - Zero conflicts, features are fully compatible
```

---

### Example 2: Alignment with Conflicts Found

```markdown
## Alignment Check: Feature 03 vs Feature 01 - CONFLICTS FOUND

**Date:** 2026-01-10
**Current Feature:** Feature 03: Schedule Strength Analysis
**Comparison Target:** Feature 01: ADP Integration (S2 Complete)

---

## Comparison Categories

### 1. Components Affected

**Feature 03 modifies:**
- PlayerManager (calculate_total_score method)
- FantasyPlayer (add schedule_strength field)
- ScheduleDataLoader (new file)
- **ConfigManager (add schedule multiplier config)**

**Feature 01 modifies:**
- PlayerManager (calculate_total_score method)
- FantasyPlayer (add adp_value field)
- ADPDataLoader (new file)
- **ConfigManager (add ADP multiplier config)**

**Overlap Analysis:**
- ⚠️ **CONFLICT: Both modify ConfigManager config structure**
  - Feature 01 spec: Add `adp_multipliers` section to league_config.json
  - Feature 03 spec: Add `schedule_multipliers` section to league_config.json
  - **Conflict?** ⚠️ POTENTIAL - Need to ensure compatible JSON structure
  - **Resolution:** Both features add separate sections, but need to coordinate format

**Feature 01 config format:**
```
{
  "adp_multipliers": {
    "ranges": [
      {"min": 1, "max": 50, "multiplier": 1.2}
    ]
  }
}
```markdown

**Feature 03 config format (from spec):**
```
{
  "schedule_strength": {
    "ranges": [
      {"min": 0.0, "max": 0.3, "bonus": 1.15}
    ]
  }
}
```markdown

**Issue:** Different field names for multiplier value:
- Feature 01 uses: `"multiplier": 1.2`
- Feature 03 uses: `"bonus": 1.15`

**Resolution:**
→ Standardize on `"multiplier"` field name for consistency
→ Update Feature 03 spec to use `"multiplier"` instead of `"bonus"`
→ This ensures consistent config pattern across all features

---

### 3. Requirements

**Feature 03 requirement:**
- Requirement 4: "Cache schedule data to avoid recalculating for each scoring call"

**Feature 01 requirement:**
- (No caching mentioned)

**Overlap Analysis:**
- ⚠️ **MINOR CONFLICT: Inconsistent caching strategy**
  - Feature 03 caches schedule data
  - Feature 01 doesn't mention caching for ADP data
  - **Impact:** Inconsistent performance characteristics

**Resolution Options:**

A. Add caching to Feature 01 (update spec)
   - Pros: Consistent performance across features
   - Cons: More complex implementation for Feature 01

B. Keep Feature 03 caching, Feature 01 without
   - Pros: Simpler for Feature 01
   - Cons: Inconsistent patterns
   - Justification: ADP data loaded once at startup, schedule data queried per player

**Recommendation:** Option B with justification:
- ADP data is static per session (loaded once)
- Schedule data may be dynamic (updated weekly)
- Caching makes sense for schedule, not necessary for ADP

**Action:** Add justification note to Feature 01 spec explaining why no caching

---

## Summary

**Total Conflicts Found:** 2

**Critical Conflicts (must resolve):**
1. **Config field name inconsistency**
   - Feature 01 uses "multiplier", Feature 03 uses "bonus"
   - Resolution: Update Feature 03 to use "multiplier" for consistency
   - Impact: Medium (affects implementation and config format)

**Minor Conflicts (nice to resolve):**
1. **Caching strategy inconsistency**
   - Feature 03 caches, Feature 01 doesn't
   - Resolution: Document justification (different use cases)
   - Impact: Low (explainable difference)

**Action Items:**
- [ ] Update Feature 03 spec.md: Change "bonus" field to "multiplier" in config format
- [ ] Update Feature 03 spec.md: Document why different from Feature 01 approach
- [ ] Update Feature 01 spec.md: Add note explaining no caching (static data)
- [ ] Verify both features after changes

**Alignment Status:** ⚠️ CONFLICTS FOUND - Must resolve before proceeding
```

**After resolving conflicts:**

```markdown
## Conflict Resolution - Feature 03 vs Feature 01

**Date:** 2026-01-10
**Status:** ✅ RESOLVED

**Conflict 1: Config field name - RESOLVED**
- Original conflict: Feature 01 used "multiplier", Feature 03 used "bonus"
- Resolution chosen: Standardize on "multiplier"
- Changes made:
  - Feature 03: Updated spec.md config format to use "multiplier" field
  - Updated ConfigManager section to match pattern
- Verified by: Agent
- Date: 2026-01-10 15:45

**Conflict 2: Caching strategy - RESOLVED**
- Original conflict: Feature 03 caches, Feature 01 doesn't
- Resolution chosen: Document justification (different use cases)
- Changes made:
  - Feature 01: Added note explaining no caching needed (static data loaded once)
  - Feature 03: Added note explaining caching needed (dynamic data queried frequently)
- Verified by: Agent
- Date: 2026-01-10 15:50

**Final Alignment Status:** ✅ PASS - All conflicts resolved, features now compatible
```

---

## Phase 6 Examples: Acceptance Criteria & User Approval
