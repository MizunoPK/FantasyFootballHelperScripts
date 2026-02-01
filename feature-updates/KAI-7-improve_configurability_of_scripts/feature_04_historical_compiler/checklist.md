# Feature 04 Checklist: Historical Compiler Configurability

**Status:** ✅ APPROVED (Gate 3 PASSED)
**Created:** 2026-01-29
**Last Updated:** 2026-01-30

---

## Checklist Purpose

This checklist contains QUESTIONS ONLY. These are genuine unknowns about user preferences, edge cases, and design decisions that were not specified in the epic request.

**IMPORTANT:** Agents cannot autonomously mark items as [x]. Only the user can resolve checklist items.

---

## Functional Questions

### Q1: Debug + E2E Mode Conflict Handling ✅

**[x] Status:** RESOLVED

**Context:**
Both --debug and --e2e-test flags can be set simultaneously, but they have conflicting behaviors:
- Debug mode: Single week (week 1), single year, preserve output on error
- E2E mode: Weeks 1-2, fixed year (2024), fast timeouts

**Options:**
1. **Option A: E2E takes precedence** - If both flags set, use E2E mode settings entirely
2. **Option B: Debug takes precedence** - If both flags set, use debug mode settings entirely
3. **Option C: Mutual exclusion** - Make flags mutually exclusive (argparse error if both set)
4. **Option D: Merge behaviors** - Use debug logging + E2E scope (weeks 1-2, fast timeouts)

**Epic Reference:**
- Discovery mentions both flags (lines 206-207, 308-309) but doesn't specify conflict resolution
- User Answer Q4: Debug = behavioral + logging changes
- User Answer Q3: E2E = limited data for speed

**Recommendation:** **Option D (Merge behaviors)** - Most flexible for debugging E2E mode itself

**User Answer:** Option D (Merge behaviors)

**Resolution:**
- When both --debug and --e2e-test are set:
  - Use DEBUG log level (from --debug)
  - Use E2E scope: weeks 1-2, fixed year 2024, fast timeouts (from --e2e-test)
  - Skip cleanup on error (from --debug)
- This allows debugging the E2E mode itself

**Spec Updated:**
- ✅ Requirement 1 (--debug) updated with interaction logic
- ✅ Requirement 2 (--e2e-test) updated with interaction logic
- ✅ Debug Mode Algorithm updated with merge behavior
- ✅ E2E Test Mode Algorithm updated with merge behavior
- Test case added: test_debug_and_e2e_both_set()

---

### Q2: E2E Mode Output Directory Naming ✅

**[x] Status:** RESOLVED

**Context:**
E2E mode compiles to default output directory `simulation/sim_data/{YEAR}/`. If user runs E2E mode with same year as production data, it will overwrite production compilation.

**Options:**
1. **Option A: Append "_e2e" suffix** - Output to `simulation/sim_data/2024_e2e/`
2. **Option B: Separate e2e_data folder** - Output to `simulation/e2e_data/2024/`
3. **Option C: No special handling** - Use default output, user responsible for avoiding overwrites
4. **Option D: Require --output-dir** - Make --output-dir mandatory when --e2e-test is set

**Epic Reference:**
- Discovery line 309: "Add E2E test mode (compile minimal dataset, ≤3 min)"
- No mention of output directory handling for E2E mode

**Recommendation:** **Option A (Append "_e2e" suffix)** - Simple, safe, doesn't break existing patterns

**User Answer:** Option A (Append "_e2e" suffix)

**Resolution:**
- E2E mode will output to `simulation/sim_data/2024_e2e/` (instead of `simulation/sim_data/2024/`)
- Appends "_e2e" suffix to year directory name
- Prevents overwriting production compilation data
- Simple, safe approach that maintains existing directory structure patterns

**Spec Updated:**
- ✅ Requirement 2 (--e2e-test) updated with output directory handling
- ✅ E2E Test Mode Algorithm updated with output_dir logic
- Test case added: E2E output directory verification

---

## Technical Questions

### Q3: Timeout Argument Validation ✅

**[x] Status:** RESOLVED

**Context:**
The --timeout argument controls HTTP request timeout. Need to determine validation rules.

**Options:**
1. **Option A: Strict validation** - Require timeout > 0 and timeout <= 300 (5 minutes max)
2. **Option B: Loose validation** - Only require timeout > 0, no upper limit
3. **Option C: No validation** - Accept any float value, let httpx handle invalid values
4. **Option D: Warn on extremes** - Accept any > 0 but warn if < 5 or > 120

**Epic Reference:**
- Discovery Iteration 2 identified REQUEST_TIMEOUT constant (default 30.0)
- User Answer Q1: Expose constants as CLI args
- No validation requirements specified

**Recommendation:** **Option A (Strict validation)** - Prevents unreasonable values, safer defaults

**User Answer:** Option A (Strict validation)

**Resolution:**
- Validate timeout: timeout > 0 and timeout <= 300 (5 minutes max)
- Validation occurs in parse_args() or early in main()
- Error message if validation fails: "Timeout must be between 0 and 300 seconds"
- Prevents unreasonable timeout values while allowing flexibility within safe range

**Spec Updated:**
- ✅ Requirement 3 (--timeout) updated with validation logic
- Test case added: test_timeout_validation()

---

### Q4: Rate Limit Delay Validation ✅

**[x] Status:** RESOLVED

**Context:**
The --rate-limit-delay argument controls delay between API requests. Need to determine validation rules.

**Options:**
1. **Option A: Allow zero** - Require rate_limit_delay >= 0 (allow 0 for no delay)
2. **Option B: Require minimum** - Require rate_limit_delay >= 0.05 (50ms minimum to avoid hammering API)
3. **Option C: Strict range** - Require 0.05 <= rate_limit_delay <= 10.0
4. **Option D: No validation** - Accept any float value

**Epic Reference:**
- Discovery Iteration 2 identified RATE_LIMIT_DELAY constant (default 0.3)
- User Answer Q1: Expose constants as CLI args
- No validation requirements specified

**Recommendation:** **Option B (Require minimum 0.05s)** - Prevents API abuse while allowing fast testing

**User Answer:** Option B (Require minimum 0.05s)

**Resolution:**
- Validate rate_limit_delay: rate_limit_delay >= 0.05 (50ms minimum)
- Validation occurs in parse_args() or early in main()
- Error message if validation fails: "Rate limit delay must be at least 0.05 seconds"
- Prevents API abuse by enforcing minimum delay, while allowing fast testing

**Spec Updated:**
- ✅ Requirement 4 (--rate-limit-delay) updated with validation logic
- Test case added: test_rate_limit_delay_validation()

---

### Q5: --verbose Flag Backward Compatibility ✅

**[x] Status:** RESOLVED

**Context:**
compile_historical_data.py currently has --verbose/-v flag (line 85-87) that sets log level to DEBUG. We're adding new --log-level argument. Need to decide on backward compatibility.

**Options:**
1. **Option A: Deprecate --verbose** - Remove --verbose flag, require --log-level DEBUG instead
2. **Option B: Keep --verbose as alias** - Keep --verbose as shorthand for --log-level DEBUG
3. **Option C: Make mutually exclusive** - Allow either --verbose OR --log-level, not both
4. **Option D: Precedence rule** - If both set, --log-level takes precedence

**Epic Reference:**
- Discovery doesn't mention existing --verbose flag
- Research found existing --verbose flag (compile_historical_data.py:85-87)
- No backward compatibility requirements specified

**Recommendation:** **Option B (Keep as alias)** - Maintains backward compatibility, user-friendly

**User Answer:** Option B (Keep --verbose as alias)

**Resolution:**
- Keep existing --verbose/-v flag for backward compatibility
- When --verbose is set, treat it as shorthand for --log-level DEBUG
- Implementation logic:
  - If args.verbose: use DEBUG level
  - Elif args.debug: use DEBUG level
  - Else: use args.log_level
- Maintains backward compatibility with existing scripts/workflows
- User-friendly approach (simpler --verbose vs --log-level DEBUG)

**Spec Updated:**
- ✅ Requirement 5 (--log-level) updated with --verbose backward compatibility handling
- Test case added: test_verbose_backward_compatibility()

---

## Edge Cases & Error Handling

### Q6: E2E Mode --year Argument Override ✅

**[x] Status:** RESOLVED

**Context:**
E2E mode is designed to use fixed year (2024) for reproducibility. But users can also provide --year argument. Need to decide override behavior.

**Options:**
1. **Option A: E2E overrides --year** - Always use 2024 when --e2e-test is set, ignore --year
2. **Option B: --year overrides E2E** - Use --year value if provided with --e2e-test
3. **Option C: Make mutually exclusive** - Error if both --e2e-test and --year are provided
4. **Option D: Warn and use E2E** - Print warning if both set, use E2E year (2024)

**Epic Reference:**
- Discovery line 309: "Add E2E test mode (compile minimal dataset, ≤3 min)"
- Research shows E2E mode uses fixed year 2024 for reproducibility
- No interaction specified between E2E mode and --year arg

**Recommendation:** **Option D (Warn and use E2E)** - Provides feedback while maintaining E2E reproducibility

**User Answer:** Option D (Warn and use E2E)

**Resolution:**
- When both --e2e-test and --year are set:
  - Print warning: "Warning: --year argument ignored when --e2e-test is set. Using fixed year 2024 for E2E reproducibility."
  - Use E2E fixed year (2024), ignore --year value
  - Maintains E2E reproducibility while providing user feedback
  - User is informed their --year argument was ignored

**Spec Updated:**
- ✅ Requirement 2 (--e2e-test) updated with --year interaction handling
- ✅ E2E Test Mode Algorithm updated with warning logic
- Test case added: test_e2e_with_year_argument()

---

## Checklist Summary

**Total Questions:** 6

**By Category:**
- Functional Questions: 2 (Q1, Q2)
- Technical Questions: 3 (Q3, Q4, Q5)
- Edge Cases & Error Handling: 1 (Q6)

**Status:**
- Open: 0
- Answered: 6
- Resolved: 6

**All questions answered:** ✅

---

## User Approval

**Status:** ✅ APPROVED (Gate 3 PASSED)

**Timestamp:** 2026-01-30

**Approval Summary:**
- All 6 questions answered by user
- All answers incorporated into spec.md
- Gate 3 (User Checklist Approval) status: ✅ PASSED

**User Answers:**
- Q1: Option D (Merge behaviors for --debug + --e2e-test)
- Q2: Option A (Append "_e2e" suffix to output directory)
- Q3: Option A (Strict validation for --timeout: 0 < timeout <= 300)
- Q4: Option B (Require minimum --rate-limit-delay >= 0.05s)
- Q5: Option B (Keep --verbose as alias for backward compatibility)
- Q6: Option D (Warn and use E2E year when both --e2e-test and --year set)

**Next Steps:**
- spec.md has been updated with all user answers
- checklist.md shows all questions resolved (0 pending)
- Ready to proceed to S2.P3 (Refinement Phase)

---

## S2 Completion Summary

**S2.P3 (Refinement Phase) Status:** ✅ COMPLETE

**Phase Completion:**
- Phase 3: Interactive Question Resolution - ✅ COMPLETE (all 6 questions resolved)
- Phase 4: Dynamic Scope Adjustment - ✅ COMPLETE (6 items - straightforward complexity)
- Phase 5: Cross-Feature Alignment - ✅ COMPLETE (compared to 4 features, zero conflicts)
- Phase 6: Acceptance Criteria & User Approval - ✅ COMPLETE (user approved 2026-01-30)

**Gate 4 (Acceptance Criteria Approval):** ✅ PASSED

**Feature 04 S2 Complete:** 2026-01-30

---

**End of Checklist**
