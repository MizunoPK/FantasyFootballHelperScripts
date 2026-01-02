# Feature 02: Accuracy Simulation JSON Integration - Lessons Learned

**Purpose:** Document issues encountered and solutions for this feature

---

## Planning Phase Lessons (Stage 2)

### ✅ Lesson 1: Leverage Previous Feature Findings

**Approach:** Instead of re-investigating shared questions, leveraged Feature 1's findings
**Result:** All 7 questions answered immediately using Feature 1's CODEBASE_INVESTIGATION_FINDINGS.md
**Time saved:** Significant - avoided duplicate investigation of PlayerManager, FantasyPlayer, array indexing
**Key insight:** Cross-feature alignment starts early - reuse research when features share infrastructure

### ✅ Lesson 2: Simpler ≠ Less Important

**Discovery:** Feature 2 is simpler than Feature 1 (~40-50 LOC vs ~150 LOC)
**Reason:** Different use case (on-demand loading vs pre-loading/caching)
**Takeaway:** Simplicity doesn't mean less planning rigor - still requires full Stage 2 deep dive
**Impact:** Avoided assumption-based errors by following full protocol

### ✅ Lesson 3: Epic Requests May Include Validation Tasks

**Epic mentioned:** "Use week_17 folders for projected, week_18 for actual in week 17"
**Investigation found:** JSON arrays already handle this (projected_points[16], actual_points[16])
**Conclusion:** Epic was asking to VERIFY this works, not implement new logic
**Same for:** DEF/K evaluation - no special code needed, just validation during QC
**Lesson:** Distinguish between "implement new feature" vs "verify existing behavior"

### ✅ Lesson 4: Feature 1's Patterns Directly Applicable

**Reused from Feature 1:**
- Same player_data/ subfolder requirement
- Same array indexing (week_num - 1)
- Same field type handling (FantasyPlayer.from_json())
- Same error handling pattern (return None if missing)

**Not applicable:**
- JSON parsing method (Feature 2 doesn't need it - just file copying)
- Week data caching (Feature 2 loads on-demand)

**Lesson:** Identify which patterns transfer and which are use-case specific

### ✅ Lesson 5: Intentional Differences Are Valid

**Feature 1 approach:** Pre-load and cache all 17 weeks
**Feature 2 approach:** Load 1 week per evaluation

**Initially seemed inconsistent, but investigation showed:**
- Win Rate Sim runs thousands of iterations across all weeks → caching essential
- Accuracy Sim runs once per config per week → caching unnecessary overhead

**Lesson:** Document WHY implementations differ (intentional vs inconsistent)

---

## Implementation Phase Lessons

{Will be populated during Stage 5b implementation}

---

## Post-Implementation Lessons

{Will be populated during Stage 5c QC}

---

## Patterns to Reuse

**For future JSON integration features:**
1. Always check how data is created/written first (compile_historical_data.py)
2. Leverage PlayerManager's existing JSON handling (don't reinvent)
3. Rely on FantasyPlayer.from_json() for validation and type conversion
4. player_data/ subfolder is MANDATORY for PlayerManager compatibility
5. Array indexing: index 0 = Week 1, index N-1 = Week N
6. Distinguish "implement new logic" from "verify existing behavior" in epic requests
