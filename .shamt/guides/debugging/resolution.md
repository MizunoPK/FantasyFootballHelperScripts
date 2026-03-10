# PHASE 3 & 4: Solution Design, Implementation, and User Verification

**Purpose:** Design and implement fix based on confirmed root cause, get user confirmation

**When to Use:** After PHASE 2 complete, root cause confirmed with evidence

**Previous Phase:** PHASE 2 (Investigation) - See `debugging/investigation.md`

**Next Phase:** PHASE 5 (Loop Back) - See `debugging/loop_back.md` (after ALL issues resolved)

---

## Table of Contents

1. [PHASE 3: Solution Design & Implementation](#phase-3-solution-design--implementation)
   - [Step 1: Update Status](#step-1-update-status)
1. [Completed Investigations](#completed-investigations)
1. [Active Investigations](#active-investigations)
   - [Step 2: Design Solution](#step-2-design-solution)
1. [Solution Implementation](#solution-implementation)
   - [Solution Design ({YYYY-MM-DD HH:MM})](#solution-design-yyyy-mm-dd-hhmm)
   - [Step 3: Implement Solution](#step-3-implement-solution)
   - [Implementation ({YYYY-MM-DD HH:MM})](#implementation-yyyy-mm-dd-hhmm)
1. [PHASE 4: User Verification - MANDATORY](#phase-4-user-verification---mandatory)
   - [Step 1: Present to User](#step-1-present-to-user)
1. [User Verification Required: Issue #{number}](#user-verification-required-issue-number)
   - [Before State (BROKEN)](#before-state-broken)
   - [After State (FIXED)](#after-state-fixed)
   - [Test Results](#test-results)
   - [Verification Steps for You](#verification-steps-for-you)
1. [Question](#question)
   - [Step 2: Process User Response](#step-2-process-user-response)
1. [User Verification](#user-verification)
1. [User Verification - Attempt 1](#user-verification---attempt-1)
   - [Investigation Round 4 (or Revised Solution)](#investigation-round-4-or-revised-solution)
1. [Common Resolution Patterns](#common-resolution-patterns)
   - [Pattern 1: Data Validation Fix](#pattern-1-data-validation-fix)
   - [Pattern 2: Null Handling Fix](#pattern-2-null-handling-fix)
   - [Pattern 3: Integration Interface Fix](#pattern-3-integration-interface-fix)
1. [Next Steps](#next-steps)

---

## PHASE 3: Solution Design & Implementation

**Goal:** Design and implement fix based on confirmed root cause

---

### Step 1: Update Status

#### 1.1: Update ISSUES_CHECKLIST.md

```markdown
| 1 | player_scoring_returns_null | 🟡 INVESTIGATING | Phase 3 (Solution Design) | ❌ NO | Smoke Part 3 | Designing solution |
```

**Current Phase:** "Phase 3 (Solution Design & Implementation)"

---

#### 1.2: Update investigation_rounds.md

```markdown
## Completed Investigations

| Issue # | Issue Name | Total Rounds | Time | Root Cause | Status |
|---------|------------|--------------|------|------------|--------|
| 1 | player_scoring_returns_null | 3 | ~90 min | Name format mismatch | Solution in progress |

## Active Investigations

{Empty if this was the only active investigation}
```

---

### Step 2: Design Solution

**Document in issue_{number}_{name}.md:**

Add "Solution Implementation" section:

```markdown
## Solution Implementation

### Solution Design ({YYYY-MM-DD HH:MM})

**Confirmed Root Cause:**
Item name format mismatch - CSV uses "Record-A" but code uses "Record-A"

**Solution Approach:**
Add name normalization in _load_stats() to handle both formats

**Implementation Plan:**

**Part 1: Code Changes**
- [ ] Update _load_stats() to normalize item names before lookup
- [ ] Create helper method _normalize_item_name()
- [ ] Handle formats: "Record-A" → "Record-A" OR vice versa
- [ ] Preserve original name in self.name for display purposes

**Part 2: Testing**
- [ ] Add unit test: test_normalize_item_name()
- [ ] Add unit test: test_load_stats_with_full_name()
- [ ] Add unit test: test_load_stats_with_abbreviated_name()
- [ ] Update existing tests if needed
- [ ] Run full test suite (100% pass required)

**Part 3: Verification**
- [ ] Run original reproduction scenario (should work now)
- [ ] Run all DataRecord tests (should pass)
- [ ] Re-run smoke test Part 3 (should pass)

**Alternative Approaches Considered:**

**Approach A: Modify CSV to use full names**
- Rejected: CSV is external data source, shouldn't modify
- Rejected: Other parts of system might rely on current format

**Approach B: Only support abbreviated names throughout codebase**
- Rejected: Code uses full names in many places
- Rejected: Would require changes in multiple modules

**Chosen Approach Reasoning:**
Normalize names in code to handle both formats - most flexible, no external dependencies, localized change
```

---

### Step 3: Implement Solution

#### 3.1: Make code changes incrementally

**Best practices:**
- Make one change at a time
- Test after each change
- Commit frequently (or at least before final commit)
- Keep changes focused on the root cause

**Example implementation:**

```python
- utils/DataRecord.py

def _normalize_item_name(self, name):
    """Convert full name to CSV format (abbreviated first name).

    Args:
        name (str): Item name in any format

    Returns:
        str: Normalized name (e.g., "Record-A" → "Record-A")
    """
    parts = name.split()
    if len(parts) == 2:
        return f"{parts[0][0]}.{parts[1]}"  # "Record-A" → "Record-A"
    return name  # Already in correct format or single name

def _load_stats(self, csv_path):
    """Load item stats from CSV file.

    Args:
        csv_path (str): Path to CSV file
    """
    df = pd.read_csv(csv_path)
    normalized_name = self._normalize_item_name(self.name)
    player_stats = df[df['ItemName'] == normalized_name]

    if player_stats.empty:
        self.stats = {}
    else:
        self.stats = player_stats.to_dict('records')[0]
```

---

#### 3.2: Add/update tests

**Add new tests for the fix:**

```python
- tests/utils/test_DataRecord.py

def test_normalize_item_name():
    """Test that item names are normalized correctly."""
    item = DataRecord(name="Record-A")
    assert item._normalize_item_name("Record-A") == "Record-A"
    assert item._normalize_item_name("Item-B") == "J.Allen"
    assert item._normalize_item_name("Record-A") == "Record-A"  # Already normalized

def test_load_stats_with_full_name():
    """Test that stats load correctly with full item name."""
    item = DataRecord(name="Record-A")
    item._load_stats("data/item_stats.csv")
    assert item.stats != {}
    assert 'StatValue' in item.stats

def test_load_stats_with_abbreviated_name():
    """Test that stats load correctly with abbreviated item name."""
    item = DataRecord(name="Record-A")
    item._load_stats("data/item_stats.csv")
    assert item.stats != {}
    assert 'StatValue' in item.stats
```

---

#### 3.3: Run tests

```bash
- Run full test suite
{TEST_COMMAND}

- Expected: 100% pass rate
- If tests fail: Fix issues before proceeding
```

**If tests fail:**
- Review test failures
- Fix implementation or tests
- Re-run until 100% pass rate achieved
- **Do NOT proceed to user verification with failing tests**

---

#### 3.5: Remove diagnostic logging

**Remove all diagnostic logging added during investigation:**

```python
- REMOVE these lines added during investigation:
- logger.info(f"Loading stats from: {csv_path}")
- logger.info(f"CSV columns: {df.columns.tolist()}")
- logger.info(f"Looking for item: {self.name}")
- etc.
```

**Why remove diagnostic logging?**
- Clutters production logs
- Already have evidence in diagnostic_logs/ folder
- Production code should be clean

**Exception:** Keep logging if it provides value for production debugging (rare)

---

#### 3.6: Update issue_{number}_{name}.md

**Add implementation section:**

```markdown
### Implementation ({YYYY-MM-DD HH:MM})

**Status:** COMPLETE

**Changes Made:**
- Modified: utils/DataRecord.py (added _normalize_item_name() method)
- Updated: utils/DataRecord.py:156 (_load_stats to use normalization)
- Added: tests/utils/test_DataRecord.py (3 new tests)

**Test Results:**
- Reproduction scenario: ✅ FIXED (returns 24.5, not None)
- New unit tests: ✅ 3/3 passed
- Existing tests: ✅ All passed (no regressions)
- Full test suite: ✅ 2,203/2,203 passed

**Before State:**
```
item = RecordManager.load_item("Record-A")
score = item.calculate_score(week=1)
- Returns: None ❌
```markdown

**After State:**
```
item = RecordManager.load_item("Record-A")
score = item.calculate_score(week=1)
- Returns: 24.5 ✅
```markdown

**Diagnostic Logging Removed:** Yes (lines 156-162 in DataRecord.py)

**Next:** Phase 4 - User Verification
```

---

#### 3.7: Update ISSUES_CHECKLIST.md

```markdown
| 1 | player_scoring_returns_null | 🟠 SOLUTION_READY | Phase 4 (User Verification) | ❌ NO | Smoke Part 3 | Fix implemented, awaiting user confirmation |
```

---

## PHASE 4: User Verification - MANDATORY

**Goal:** Get user confirmation that issue is truly resolved

**Critical:** Agent CANNOT self-declare victory. User MUST confirm.

---

### Step 1: Present to User

**Use this template to present the fix:**

```markdown
## User Verification Required: Issue #{number}

**Issue:** {issue name}

**Investigation Summary:**
- Rounds: {count}
- Time: {duration}
- Root Cause: {brief summary}

**Solution Summary:**
- {brief description of fix}
- {what was changed}

**Files Modified:**
- {list files}

---

### Before State (BROKEN)

**Symptom:** {what was wrong}

**Example:**
```
{code example showing bug}
- Result: {wrong output} ❌
```markdown

**Error:** {error message if any}

---

### After State (FIXED)

**Behavior:** {what should happen now}

**Example:**
```
{same code example}
- Result: {correct output} ✅
```markdown

---

### Test Results

**Reproduction Scenario:**
- Original bug scenario: ✅ FIXED

**Unit Tests:**
- All tests: ✅ {count}/{count} passed
- New tests: ✅ {count} tests added, all passing

**Smoke Test:**
- Part 3 E2E test: ✅ Now passing (was failing before)

---

### Verification Steps for You

To verify this issue is resolved, you can:

1. Run the test scenario:
   ```
   {command to reproduce original bug}
   ```text

2. Expected result: {what should happen}

3. Or check manually:
   ```
   {manual verification code}
   ```markdown

---

## Question

**Is Issue #{number} fully resolved?**

Options:
1. **YES** - Issue is fixed as expected
2. **PARTIALLY** - Better but still some issues
3. **NO** - Issue still exists or new problems

If PARTIALLY or NO, please describe:
- What behavior is still wrong?
- What's the expected behavior?
```

**Wait for user response before proceeding.**

---

### Step 2: Process User Response

#### If user says YES

**1. Update ISSUES_CHECKLIST.md:**

```markdown
| 1 | player_scoring_returns_null | 🟢 FIXED | Phase 4 | ✅ YES | Smoke Part 3 | User confirmed - name normalization added |
```

**2. Update issue_{number}_{name}.md:**

```markdown
## User Verification

**User Verification:** ✅ CONFIRMED FIXED
**Verified By:** User
**Verified Date:** {YYYY-MM-DD HH:MM}
**User Feedback:** {any comments user provided}

**Status:** COMPLETE ✅
```

**3. Move to Phase 4b (Root Cause Analysis) - MANDATORY:**

**CRITICAL:** Before moving to next issue, you MUST perform root cause analysis.

```text
Proceed to Phase 4b: Root Cause Analysis
└─ Read debugging/root_cause_analysis.md
   Analyze WHY bug existed (5-why analysis)
   Draft guide improvement proposal
   Get user confirmation of root cause
   Document in guide_update_recommendations.md
```

**See:** `debugging/root_cause_analysis.md` for complete Phase 4b workflow

**After Phase 4b complete:**

```text
Are there more issues in ISSUES_CHECKLIST.md with status NOT 🟢 FIXED?
├─ YES (more issues to resolve)
│  └─ Move to next issue (back to Phase 2 for that issue)
│     Update "Current Focus" in ISSUES_CHECKLIST.md
│     Read debugging/investigation.md for next issue
│
└─ NO (all issues resolved)
   └─ Move to Phase 5 (Loop Back to Testing)
      Read debugging/loop_back.md
```

---

#### If user says PARTIALLY or NO

**1. Gather details from user**

Ask clarifying questions:
- What behavior is still wrong?
- What's the expected behavior?
- Is this the same issue or a different one?

**2. Assess situation:**

```text
Is this the same root cause with incomplete fix?
├─ YES (same root cause, fix incomplete)
│  └─ Update solution (stay in Phase 3)
│     - Revise implementation
│     - Add more tests
│     - Re-run tests
│     - Present to user again
│
└─ NO (different root cause OR new issue)
   ├─ Different root cause for same symptom
   │  └─ Back to Phase 2 (Investigation)
   │     - New investigation rounds
   │     - Form new hypotheses
   │     - Find actual root cause
   │
   └─ Entirely new issue
      └─ Add to ISSUES_CHECKLIST.md as new issue
         - Give new issue number
         - Mark current issue as resolved (if original symptom is fixed)
         - Investigate new issue separately
```

**3. Update ISSUES_CHECKLIST.md:**

If same issue, incomplete fix:
```markdown
| 1 | player_scoring_returns_null | 🟡 INVESTIGATING | Phase 3 (Revising Solution) | ❌ NO | Smoke Part 3 | User feedback: {summary} |
```

If different root cause:
```markdown
| 1 | player_scoring_returns_null | 🟡 INVESTIGATING | Phase 2 (New Investigation) | ❌ NO | Smoke Part 3 | Previous fix insufficient, re-investigating |
```

**4. Update issue_{number}_{name}.md:**

```markdown
## User Verification - Attempt 1

**User Verification:** ❌ NOT RESOLVED
**User Feedback:** {what user reported}
**Next Action:** {Back to Phase 2 / Update Phase 3 solution / Add new issue}

---

{Continue investigation/solution below}

### Investigation Round 4 (or Revised Solution)
{Continue from here}
```

---

## Common Resolution Patterns

### Pattern 1: Data Validation Fix

**Root cause:** Missing data validation
**Solution:** Add validation at boundary (input, API, file load)

```python
- Before
def load_data(filepath):
    return pd.read_csv(filepath)

- After
def load_data(filepath):
    df = pd.read_csv(filepath)
    required_columns = ['PlayerName', 'StatValue']
    missing = set(required_columns) - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns in CSV: {missing}")
    return df
```

---

### Pattern 2: Null Handling Fix

**Root cause:** No null checks
**Solution:** Add null checks with appropriate defaults or errors

```python
- Before
def calculate_score(stats):
    return stats['points'] * stats['multiplier']

- After
def calculate_score(stats):
    if stats.get('points') is None or stats.get('multiplier') is None:
        raise ValueError("Cannot calculate score: missing points or multiplier")
    return stats['points'] * stats['multiplier']
```

---

### Pattern 3: Integration Interface Fix

**Root cause:** Interface mismatch between components
**Solution:** Align interfaces or add adapter layer

```python
- Before: ComponentA sends dict, ComponentB expects object
def component_b_method(player_obj):
    return player_obj.name

- After: Add adapter
def component_b_method(record_data):
    if isinstance(record_data, dict):
        item_obj = Item.from_dict(record_data)
    else:
        item_obj = record_data
    return player_obj.name
```

---

## Next Steps

**After user confirms issue is resolved:**

**If more issues remain in checklist:**
- Move to next issue
- Back to Phase 2 (Investigation) for that issue
- Update "Current Focus" in ISSUES_CHECKLIST.md

**If all issues resolved (all 🟢 FIXED with user confirmation):**
- Move to Phase 5 (Loop Back to Testing)
- Read `debugging/loop_back.md`

---

**END OF PHASE 3 & 4 GUIDE**
