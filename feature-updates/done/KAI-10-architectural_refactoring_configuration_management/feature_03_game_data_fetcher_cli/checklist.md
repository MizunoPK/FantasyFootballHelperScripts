## Feature Checklist: game_data_fetcher_cli

**Status:** ALL RESOLVED — user-approved (Gate 3: 2026-02-18)
**Last Updated:** 2026-02-18

---

## Questions (All Resolved)

### Q1: --request-timeout and --rate-limit-delay as CLI args?

**Context:**
- Feature 01 REQ-09 will refactor `player-data-fetcher/game_data_fetcher.py` to accept `request_timeout` and `rate_limit_delay` as parameters to `fetch_game_data()`
- After Feature 01, the runner will need to pass these values explicitly
- DISCOVERY.md is silent on these args for Feature 03 (Feature 04 explicitly adds them for historical_compiler)
- Current values: REQUEST_TIMEOUT=30, RATE_LIMIT_DELAY=0.2 (from config)
- Note: RATE_LIMIT_DELAY is currently imported but not actually used in game_data_fetcher.py

**Options:**
- A: Add both `--request-timeout` (int, default=30) and `--rate-limit-delay` (float, default=0.2) to run_game_data_fetcher.py — consistent with Feature 04's approach
- B: Pass hardcoded defaults (30 and 0.2) to fetch_game_data() without exposing as CLI args — simpler, fewer args to document
- C: Add only `--request-timeout` (skip RATE_LIMIT_DELAY since it's unused)

**Status:** [x] RESOLVED — Option C (add --request-timeout only; skip --rate-limit-delay since it's unused in code)

---

### Q2: --data-folder, --validate, --clean args in scope?

**Context:**
- The seeded feature_03 README lists: "3 additional script-specific args to add: --data-folder, --validate, --clean"
- DISCOVERY.md Feature breakdown for Feature 03 says: "Enhance existing argparse (+--e2e-test, --log-level) + E2E modes" — no mention of these 3 args
- Current run_game_data_fetcher.py has no --data-folder, --validate, or --clean args

**Options:**
- A: Add all 3 args (--data-folder, --validate, --clean) — expands scope beyond DISCOVERY
- B: Skip all 3 args — follow DISCOVERY scope strictly
- C: Add only --data-folder (most useful, minimal scope expansion)

**Status:** [x] RESOLVED — Option B (skip all 3; follow DISCOVERY scope strictly; --output already covers custom paths)

---

### Q3: E2E test data limiting — which week?

**Options:**
- A: Always fetch Week 1 of the specified season — reliable (past data, always exists), fast, deterministic
- B: Fetch only the current week (`args.current_week`) — tests the actual current state, but may be slower mid-season

**Status:** [x] RESOLVED — Option A (always fetch Week 1; reliable past data, deterministic)

---

### Q4: ~~Debug mode data scope~~ — REMOVED

**Status:** [x] N/A — REMOVED per handoff correction 2026-02-18. No `--debug` flag in this epic.

---

### Q5: Historical season detection after config removal

**Options:**
- A: Hard-code comparison against 2025: `if args.season < 2025: current_week = 18`
- B: Remove auto-detection entirely — user must pass `--current-week 18` explicitly
- C: Add a `--historical-season` flag — explicit opt-in that sets `current_week=18`

**Status:** [x] RESOLVED — Option C (add --historical-season flag; replaces implicit year-comparison logic)
