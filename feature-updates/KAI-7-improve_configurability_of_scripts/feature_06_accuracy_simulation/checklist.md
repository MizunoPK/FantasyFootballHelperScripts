# Feature 06 Checklist: Accuracy Simulation Configurability

**Purpose:** Track user questions and decisions for this feature

**Status:** APPROVED (All questions resolved)
**Created:** 2026-01-29
**Last Updated:** 2026-01-30

---

## Questions for User

### Q1: Flag Conflict Handling (--e2e-test and --debug)

**Status:** [x] RESOLVED (User approved Option D - 2026-01-30)

**Context:**
Users may provide both `--e2e-test` and `--debug` flags simultaneously:
```bash
python run_accuracy_simulation.py --e2e-test --debug
```

These modes have conflicting settings:
- E2E mode: test_values=0, horizons=['week_1_5'], run once
- Debug mode: test_values=1, horizons=['week_1_5', 'week_6_9'], DEBUG logging

**Options:**

**Option A: E2E Mode Takes Precedence**
- If both flags: use E2E settings entirely
- Ignore --debug flag with warning message
- Pros: Clear precedence, E2E guarantees ≤3 min
- Cons: User loses DEBUG logging if they wanted both

**Option B: Debug Mode Takes Precedence**
- If both flags: use Debug settings entirely
- Ignore --e2e-test flag with warning message
- Pros: Clear precedence, user gets DEBUG logs
- Cons: User loses E2E speed if they wanted fast test

**Option C: Mutual Exclusion (Error)**
- If both flags: exit with error message
- Require user to choose one flag only
- Pros: Forces explicit choice, no ambiguity
- Cons: Slightly less convenient

**Option D: Combine Both Modes**
- If both flags: E2E settings + DEBUG logging
- E2E mode (test_values=0, single horizon, run once) with DEBUG log level
- Pros: User gets both benefits, flexible
- Cons: Slight complexity in implementation

**Epic Reference:**
- Discovery does not specify flag interaction behavior
- Both flags are independent features

**Recommendation:** **Option D (Combine Both Modes)**
- Rationale: Maximizes user flexibility without forcing mutual exclusion
- Implementation: Simple - set log_level='debug' when --debug is set, use E2E settings when --e2e-test is set
- If both set: E2E settings (fast) + DEBUG logging (verbose)

**Why This Is a Question:**
- Genuine unknown: Discovery doesn't specify flag interaction
- User preference: Trade-off between strictness (mutual exclusion) and flexibility (combination)
- Not a research gap: Implementation is straightforward once decision is made

**Impact on spec.md:**
- Will add requirement for chosen approach
- Source: User Answer to Checklist Q1
- Affects: run_accuracy_simulation.py flag handling logic (lines 227+)

---

## User Approval

**Gate 2 Status:** ✅ APPROVED (2026-01-30)

**User Decision:**
- Q1: Option D (Combine Both Modes) - Approved

**Approval Summary:**
- User approved combining E2E and debug modes when both flags set
- E2E settings (fast) + DEBUG logging (verbose) when both --e2e-test and --debug provided
- Maximizes flexibility without mutual exclusion

---

**Total Questions:** 1
**Open:** 0
**Resolved:** 1

---

**Note:** This checklist contains QUESTIONS ONLY. Agents create questions, users provide answers. Do NOT mark items as resolved without explicit user approval.
