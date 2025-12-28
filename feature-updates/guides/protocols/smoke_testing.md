# Smoke Testing Protocol

**When:** Before declaring any feature complete

**Related:** [README.md](README.md) - Protocol index

---


**Purpose:** Verify code actually runs, not just that tests pass

**Required Tests:**
1. Import test - All modules can be imported
2. Entry point test - Scripts/CLIs start without errors
3. Execution test - Basic functionality works end-to-end

**Pass Criteria:** All 3 test types must pass before feature is "complete"

**See:** feature_development_guide.md "Post-Implementation Smoke Testing" for details

---

### Quality Control Review Protocol

**Purpose:** Catch issues through multiple independent review rounds.

**Execute:** After implementation appears complete, minimum 3 rounds required.

```
┌─────────────────────────────────────────────────────────────────┐
│  ALL 3 QC ROUNDS ARE MANDATORY - NO EXCEPTIONS                  │
│  Do NOT skip rounds for "simple" features or time pressure      │
│  Each round catches different issue types                       │
└─────────────────────────────────────────────────────────────────┘
```

**Round 1: Script Execution Test (MANDATORY)**

If the feature includes a runner script (`run_*.py`), you MUST:

1. **Execute the script with --help** to verify argument parsing works:
   ```bash
   python run_feature.py --help
   # Should display help text without errors
   ```

2. **Execute the script in dry-run mode** (if available) or with minimal input:
   ```bash
   python run_feature.py --mode test --iterations 1
   # Should complete without crashing
   ```

3. **Execute the script end-to-end** with real data:
   - Not mocked dependencies
   - Not simulated paths
   - Actual file system interactions
   ```bash
   python run_feature.py --mode full
   # Should produce expected output files
   ```

4. **Verify output:**
   - Check output files exist
   - Check output content is valid (non-zero values, correct format)
   - Check no error messages in output

**Scripts without execution tests must not pass QC Round 1.**

**When E2E tests reveal errors:**
1. Fix the immediate error
2. Before continuing, perform root cause analysis:
   - Why was this error created in the first place?
   - Why wasn't it caught during unit testing?
   - Why wasn't it caught during verification iterations?
3. Document findings in the lessons learned file
4. Only proceed after documenting the lesson

Then proceed with document review:
5. Re-read the specification file (`{feature_name}_specs.md`)
6. Re-read the TODO file (`{feature_name}_todo.md`)
7. Re-read the code changes file (`{feature_name}_code_changes.md`)
8. Cross-reference all three documents
9. Identify any discrepancies, missing items, or incorrect implementations
10. Document findings and fix any issues found

**Round 2: Deep Verification Review**
1. With fresh perspective, repeat the same review process
2. Focus on algorithm correctness and edge cases
3. Verify conditional logic matches spec exactly
4. Check that tests actually validate the behavior (not just structure)
5. Execute **Semantic Diff Check** (see below)
6. Document findings and fix any issues found

**Semantic Diff Check (Round 2):**

Before completing Round 2, verify changes are minimal and intentional:

1. **Run `git diff` and review each change:**
   - Are there whitespace-only changes? → Remove them
   - Are there reformatting changes unrelated to the feature? → Remove them
   - Are there "while I'm here" improvements? → Should have been scoped earlier

2. **For each changed file, verify:**
   ```
   □ File was listed in TODO's "Files to Modify" section
   □ If NOT listed, document why it needed changes
   □ Changes are minimal - only what's needed for the feature
   ```

3. **Check for scope creep in code:**
   - Did you refactor code that didn't need refactoring?
   - Did you add logging/comments beyond what was specified?
   - Did you "improve" adjacent code that was working fine?

4. **If unexpected changes exist:**
   - Either remove them (revert to original)
   - Or document why they were necessary and get user approval

**Why this matters:** Minimal diffs are:
- Easier to review (less noise)
- Easier to rollback (fewer side effects)
- Less likely to cause merge conflicts
- Easier to understand in git history

**Round 3: Final Skeptical Review**
1. Assume previous reviews missed something
   > *Rationale: Confirmation bias causes us to see what we expect. Round 3 exists specifically to counteract this - actively look for what's WRONG, not what's right.*
2. Re-read spec with "adversarial" mindset - actively look for gaps
   > *Rationale: If you look for problems, you'll find them. If you look for confirmation that everything works, you'll miss issues.*
3. Verify every algorithm, calculation, and conditional
4. Confirm all requirements have corresponding tests
5. Document final verification status

### What to Check in Each Round

| Document | What to Verify |
|----------|---------------|
| Original Requirements | Every line has been addressed |
| TODO File | All tasks marked complete, no orphan items |
| Code Changes | All changes documented, line numbers accurate |
| Algorithm Logic | Conditional logic matches spec exactly |
| Test Coverage | Behavior tests exist (not just structure tests) |

### Round Documentation

After each round, document in the code changes file:
```
