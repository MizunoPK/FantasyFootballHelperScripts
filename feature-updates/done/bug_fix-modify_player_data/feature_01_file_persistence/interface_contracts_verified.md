# Feature 01: File Persistence Issues - Verified Interface Contracts

**Purpose:** Document ALL external interfaces verified from source code BEFORE implementation

**Verification Date:** 2025-12-31
**Verified By:** Reading actual source code (not assumptions)

---

## Interface Verification Summary

**Total Interfaces:** 3 (production code) + 2 (testing frameworks)
**All Verified:** ✅ YES
**Source:** Iteration 2 (Component Dependency Mapping) + actual source code

---

## Production Code Interfaces

### Interface 1: pathlib.Path.with_suffix()

**Source:** Python Standard Library (pathlib module)

**Signature:**
```python
Path.with_suffix(suffix: str) -> Path
```

**Parameters:**
- `suffix` (str): New suffix (e.g., '.bak', '.tmp', '.json')
  - Must include leading dot
  - Replaces existing suffix

**Returns:**
- `Path`: New Path object with replaced suffix

**Current Usage in PlayerManager.py:**
```python
# Line 553 (TO BE REMOVED)
backup_path = json_path.with_suffix('.bak')

# Line 561 (PRESERVE)
tmp_path = json_path.with_suffix('.tmp')
```

**Verification:** ✅ Interface confirmed from Python 3.x pathlib documentation
**Action:** Remove line 553 usage, preserve line 561 usage

---

### Interface 2: shutil.copy2()

**Source:** Python Standard Library (shutil module)

**Signature:**
```python
shutil.copy2(src, dst, *, follow_symlinks=True)
```

**Parameters:**
- `src`: Source file path (str or Path)
- `dst`: Destination file path (str or Path)
- `follow_symlinks`: Whether to follow symbolic links (default: True)

**Returns:**
- `str`: Destination path

**Current Usage in PlayerManager.py:**
```python
# Lines 554-556 (TO BE REMOVED)
if json_path.exists():
    import shutil
    shutil.copy2(json_path, backup_path)
```

**Verification:** ✅ Interface confirmed from Python 3.x shutil documentation
**Action:** Remove lines 554-556 entirely (including import)

---

### Interface 3: Path.replace()

**Source:** Python Standard Library (pathlib module)

**Signature:**
```python
Path.replace(target) -> Path
```

**Parameters:**
- `target`: Destination path (str or Path)

**Returns:**
- `Path`: The new path (destination)

**Platform Behavior:**
- POSIX: Atomic replacement (guaranteed)
- Windows: NOT guaranteed atomic (may fail if file locked)

**Current Usage in PlayerManager.py:**
```python
# Line 566 (PRESERVE)
tmp_path.replace(json_path)
```

**Verification:** ✅ Interface confirmed - Windows behavior tested in Task 9
**Action:** PRESERVE (no changes to atomic write pattern)

---

## Testing Framework Interfaces

### Interface 4: pytest Framework

**Source:** External package (pytest)

**Test Discovery:**
- File naming: `test_*.py` or `*_test.py`
- Function naming: `test_*()`
- Class naming: `Test*`

**Fixture Usage:**
```python
@pytest.fixture
def fixture_name():
    return value
```

**Assertion:**
```python
assert condition, "message"
pytest.raises(ExceptionType)
```

**Verification:** ✅ Standard pytest conventions (used throughout tests/ directory)
**Action:** Follow existing test patterns in tests/league_helper/util/

---

### Interface 5: unittest.mock

**Source:** Python Standard Library (unittest.mock module)

**Mock Classes:**
```python
from unittest.mock import Mock, MagicMock, patch

# Basic mock
mock_obj = Mock()
mock_obj.method.return_value = value

# Patch decorator
@patch('module.path.Class')
def test_function(mock_class):
    pass
```

**Mock Verification:**
```python
mock_obj.method.assert_called_once()
mock_obj.method.assert_called_with(args)
assert mock_obj.method.call_count == N
```

**Verification:** ✅ Standard unittest.mock usage (used in test_PlayerManager_json_loading.py)
**Action:** Follow existing mock patterns

---

## Interface Contract Table

| Interface | Type | Source | Line | Action | Verified |
|-----------|------|--------|------|--------|----------|
| Path.with_suffix('.bak') | Method | pathlib | 553 | REMOVE | ✅ |
| shutil.copy2() | Function | shutil | 555-556 | REMOVE | ✅ |
| Path.with_suffix('.tmp') | Method | pathlib | 561 | PRESERVE | ✅ |
| Path.replace() | Method | pathlib | 566 | PRESERVE | ✅ |
| pytest fixtures | Framework | pytest | N/A | USE | ✅ |
| unittest.mock | Module | unittest | N/A | USE | ✅ |

---

## Assumptions Verified

**Assumption 1:** Removing lines 553-556 will not break compilation
**Verification:** ✅ Lines are self-contained (no return values used elsewhere)

**Assumption 2:** Atomic write pattern (lines 558-566) will continue to work
**Verification:** ✅ No dependencies on removed .bak code

**Assumption 3:** Existing update_players_file() callers will not be affected
**Verification:** ✅ Method signature unchanged, return type unchanged

**Assumption 4:** pytest will discover new test file
**Verification:** ✅ File location and naming follow conventions

---

## Interface Verification Complete

**All interfaces verified from actual source code:** ✅ YES

**Ready to proceed with implementation:** ✅ YES

**Next Step:** Create implementation_checklist.md

---

**END OF INTERFACE VERIFICATION**
