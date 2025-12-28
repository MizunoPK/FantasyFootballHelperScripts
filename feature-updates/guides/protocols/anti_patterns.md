# Anti-Pattern Gallery

Visual examples of what NOT to do. Learn from these common mistakes.

**Related:** [README.md](README.md) - Protocol index

---

### Anti-Pattern 1: The Orphan Method

**What happened:**
```python
# Created this method...
class ResultsManager:
    def save_optimal_configs_folder(self):
        """Save configs to folder structure."""
        # Great implementation!
        self._create_folder_structure()
        self._write_config_files()
        return folder_path

# But forgot to update the caller...
class SimulationManager:
    def run_iterative(self):
        # ... simulation logic ...

        # Still calls the old method!
        self.results_manager.save_optimal_config()  # ← OLD METHOD

        # Should call:
        # self.results_manager.save_optimal_configs_folder()  # ← NEW METHOD
```

**Result:** Feature "complete" but doesn't work for users. Tests pass because they test the new method in isolation.

**How to catch:** Integration Gap Check (iterations 7, 14, 23) - verify every new method has a caller in the Integration Matrix.

---

### Anti-Pattern 2: The Interface Assumption

**What happened:**
```python
# Assumed the interface was:
class AccuracyCalculator:
    def calculate_score(self, player, week):
        return player.actual_points  # ← Assumed this attribute exists

# But the actual FantasyPlayer class has:
class FantasyPlayer:
    # actual_points doesn't exist!
    week_1_points: float
    week_2_points: float
    # ... week_3 through week_17 ...

    # Must use: sum([getattr(self, f'week_{i}_points', 0) for i in range(1, 18)])
```

**Result:** `AttributeError: 'FantasyPlayer' object has no attribute 'actual_points'` at runtime.

**How to catch:** Interface Verification Protocol - read actual class definitions with the Read tool before implementing. Don't trust similar class patterns.

---

### Anti-Pattern 3: The Mock Mask

**What happened:**
```python
# Test with heavy mocking...
@patch('module.ConfigGenerator')
def test_simulation(mock_gen):
    # Mock accepts ANY arguments!
    mock_gen.return_value.generate.return_value = []

    manager = SimulationManager()
    result = manager.run()

    # Test passes! But...

# Real interface is different:
class ConfigGenerator:
    def generate_iterative_combinations(self, param_name: str, base_config: dict):
        # Different method name! Different parameters!
        pass
```

**Result:** Tests pass, production crashes with `AttributeError: 'ConfigGenerator' object has no attribute 'generate'`.

**How to catch:** Mock Audit (iteration 21) - verify mocks match real interfaces. Use `spec=RealClass` in `@patch` decorators.

---

### Anti-Pattern 4: The Silent Default

**What happened:**
```python
# Code silently handles missing attributes:
def process_players(players):
    results = []
    for player in players:
        actual = getattr(player, 'actual_points', None)  # ← Silent default
        if actual is not None:
            results.append(player)
    return results

# But 'actual_points' never exists on any player!
# Result: Empty results list, no error, no warning
```

**Result:** Feature runs but produces empty/wrong output. No error messages to debug.

**How to catch:**
- Use explicit attribute access for required attributes (fails fast)
- Add logging when default values are used
- Verify attribute names exist in class definitions

---

### Anti-Pattern 5: The Existence Test

**What happened:**
```python
# Test only checks file exists:
def test_output_generation():
    manager.run_simulation()

    # BAD: Only checks existence
    assert (output_path / 'config.json').exists()
    assert (output_path / 'results.csv').exists()
    # Tests pass!

# But the files contain:
# config.json: {}  ← Empty!
# results.csv: "header\n"  ← No data!
```

**Result:** Tests pass but output is useless.

**How to catch:** Write content validation tests:
```python
# GOOD: Validates content
config = json.load(open(output_path / 'config.json'))
assert 'DRAFT_ORDER' in config
assert len(config['DRAFT_ORDER']) == 12

results = pd.read_csv(output_path / 'results.csv')
assert len(results) > 0
assert results['score'].mean() > 0
```

---

### Anti-Pattern 6: The Partial Mirror

**What happened:**
```python
# Spec said: "Mirror run_simulation.py structure"

# Developer created run_accuracy_simulation.py with:
# ✓ Same CLI arguments (--mode, --baseline, --output, etc.)
# ✓ Same mode handling (ros, weekly, both)
# ✓ Same logging setup
# ✓ Same error handling

# But MISSED these patterns from run_simulation.py:

# 1. Constants at top of file:
DEFAULT_MODE = 'both'
DEFAULT_SIMS = 100
DEFAULT_WORKERS = 4
PARAMETER_ORDER = [...]  # ← Defined here, not in manager class!

# 2. Where PARAMETER_ORDER is defined:
# In run_simulation.py: PARAMETER_ORDER at line 56
# In AccuracySimulationManager.py: ACCURACY_PARAMETER_ORDER at line 62  # ← WRONG LOCATION
```

**Result:** Inconsistent code organization. Required post-implementation refactoring to move constants to runner script.

**How to catch:** Mirror Pattern Verification (added to Skeptical Re-verification Protocol):
1. When spec says "mirror X", read ENTIRE file X
2. Document ALL organizational patterns (constants, where vars defined, file structure)
3. Compare your implementation against these patterns
4. Don't just copy obvious elements (CLI args) - copy everything

---

### Anti-Pattern Recognition Checklist

Before marking any implementation complete, verify NONE of these patterns are present:

```
□ Every new method has a caller (not orphan)
□ Every interface call verified against actual class definition
□ Mocks use spec=RealClass or are verified against real interface
□ No getattr with silent defaults on required attributes
□ Output tests validate content, not just existence
□ If spec said "mirror X", ALL patterns from X are matched (not just obvious ones)
```

---

## Common Failure Patterns by Phase

Use this reference to anticipate and prevent failures at each workflow stage:

### Planning Phase Failures

| Pattern | Symptoms | Prevention |
|---------|----------|------------|
| **Vague specs** | "Handle errors appropriately" with no details | Require specific error messages and behaviors |
| **Missing edge cases** | Only happy path documented | Ask "what if X is empty/null/invalid?" |
| **Unresolved alternatives** | "Option A OR Option B" in specs | Force choice before development |
| **Assumed interfaces** | "Call the save method" without verification | Verify exact method signatures |
| **Scope creep** | Requirements expand during planning | Document explicit in-scope/out-of-scope |

### Verification Phase Failures

| Pattern | Symptoms | Prevention |
|---------|----------|------------|
| **Rushing iterations** | "This is simple, skip to 24" | Complete ALL iterations - complexity hides |
| **Interface assumptions** | "Similar class X has this method" | Read actual class definitions |
| **Data model assumptions** | "Object probably has this attribute" | Verify attributes exist and semantics |
| **Orphan code planning** | Tasks create methods but no callers | Integration Gap Check (7, 14, 23) |
| **Mock-first thinking** | "I'll mock this and figure it out later" | Verify real interfaces during planning |

### Implementation Phase Failures

| Pattern | Symptoms | Prevention |
|---------|----------|------------|
| **Wrong dependency order** | Import errors, undefined classes | Verify dependency ordering before coding |
| **Test-last approach** | "I'll add tests after it works" | Write tests alongside or before code |
| **QA-at-end only** | All bugs discovered in final QC | Incremental QA checkpoints |
| **Silent failures** | Code runs but produces wrong output | Output content validation tests |
| **Breaking unrelated tests** | Changes cascade unexpectedly | Run full test suite after each phase |

### QC Phase Failures

| Pattern | Symptoms | Prevention |
|---------|----------|------------|
| **Existence testing only** | "File exists" but content wrong | Content validation in tests |
| **Mock masking** | Heavy mocking hides real bugs | At least one integration test with real objects |
| **Skipping E2E execution** | Unit tests pass, script fails | Always execute scripts end-to-end |
| **Ignoring warnings** | Deprecation/type warnings dismissed | Address all warnings before completion |

**How to use this table:** Before each phase transition, review the relevant failure patterns and verify none are present.

---
