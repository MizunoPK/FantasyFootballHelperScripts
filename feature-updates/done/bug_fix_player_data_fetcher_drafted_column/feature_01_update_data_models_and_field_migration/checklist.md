# Feature 1: Update Data Models and Field Migration - Planning Checklist (REVISED)

**Purpose:** Track open questions and decisions for this feature

**Instructions:**
- [ ] = Open question (needs user answer)
- [x] = Resolved (answer documented below)

**Status:** REVISED after user clarification - Only 2 questions remain!

---

## Open Questions

---

## Resolved Questions

### Question 1: Remove PRESERVE_DRAFTED_VALUES Config Option? ✅ RESOLVED
- [x] **Decision:** Option A - Remove entirely

**User's Response:**
"A - remove this entirely. It has never been used since the introduction of drafted_data.csv anyway"

**Implementation Impact:**
- Delete `PRESERVE_DRAFTED_VALUES = False` from config.py (line 17)
- Remove from imports in player_data_exporter.py (line 32)
- Remove initialization: `self.existing_drafted_values = {}` (line 58)
- Remove if-statement: `if PRESERVE_DRAFTED_VALUES: self._load_existing_drafted_values()` (lines 60-61)
- Delete `_load_existing_drafted_values()` method entirely (lines 236-240)
- Total: ~10 lines removed

**Rationale:** Config never used since drafted_data.csv was introduced, clean removal preferred.

---

### Question 2: Simplify `_get_drafted_by()` Method ✅ RESOLVED
- [x] **Decision:** Option A - Simplify to return field directly

**Agent's Rationale:**
Keep the method as a simple wrapper that returns `player.drafted_by`. This maintains the abstraction layer (already being called in line 500) while fixing the broken int→str conversion logic.

**Implementation:**
```python
def _get_drafted_by(self, player: FantasyPlayer) -> str:
    """Get drafted_by value from player (team name or empty string)"""
    return player.drafted_by
```

**Why Option A over Option B:**
- Method already has a caller (line 500: `"drafted_by": self._get_drafted_by(player)`)
- Provides abstraction point if logic changes in future
- Simpler change (modify method, not caller)

---

## Deprecated Questions (No Longer Relevant)

### ~~Question: CSV Backward Compatibility~~
**Status:** NOT APPLICABLE
**Reason:** players.csv is deprecated (Feature 2 removes it), no CSV preservation needed

### ~~Question: Dictionary Rename~~
**Status:** NOT APPLICABLE
**Reason:** `existing_drafted_values` dictionary is being removed entirely (preservation from deprecated CSV)

### ~~Question: String Validation~~
**Status:** NOT CRITICAL
**Reason:** Values already validated by DraftedRosterManager, no additional validation needed

### ~~Question: Error Handling Strategy~~
**Status:** NOT CRITICAL
**Reason:** No CSV reading for preservation, standard error handling sufficient

---

## Additional Scope Discovered

**SCOPE REDUCTION!**
- Original estimate: ~35 lines across 6 files with complex preservation
- Revised estimate: ~20 lines modified, ~18 removed across 6 files (SIMPLER!)
- Complexity: LOW (down from MEDIUM)
- Risk: LOW (down from MEDIUM)

---

## Checklist Status

**Total Questions:** 2 (down from 5!)
**Open:** 0
**Resolved:** 2

---

**Phase 3 Complete:** All questions resolved (Question 1: user answer, Question 2: agent decision)

---

## Phase 4: Dynamic Scope Adjustment

**Scope Count:**
- High-level tasks: 10
- Estimated detailed items: ~15
- Threshold: 35 items

**Scope Assessment:** ✅ PASS - Well under 35 items, no split needed

**Complexity:** LOW
**Risk:** LOW

---

## Phase 5: Cross-Feature Alignment

**Features to Compare:** None (this is Feature 1, Feature 2 hasn't been deep-dived yet)

**Alignment Check:** ✅ N/A - First feature, no conflicts possible

**Next:** Mark Stage 2 complete for Feature 1
