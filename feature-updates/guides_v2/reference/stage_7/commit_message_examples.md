# Commit Message Examples - Stage 7

**Purpose:** Reference examples for epic completion commits
**When to use:** Step 6 of Stage 7 (Creating Commit Message)
**Main Guide:** `stages/stage_7/epic_cleanup.md`

---

## Commit Message Format

**Format:** `{commit_type}/KAI-{number}: {message}`
- commit_type: "feat" or "fix"
- KAI-{number}: From EPIC_TRACKER.md
- message: 100 chars or less, imperative mood

**Rules:**
- First line: 100 characters or less
- Brief but descriptive
- Imperative mood ("Add feature" not "Added feature")
- Body: List major features and changes
- Include testing summary
- No emojis or subjective prefixes

---

## Example 1: Multi-Feature Epic (3 features)

**Scenario:** Epic with multiple features that enhance existing system

```bash
git commit -m "$(cat <<'EOF'
feat/KAI-1: Complete improve_draft_helper epic

Major features:
- ADP integration: Adds market wisdom via Average Draft Position data
- Matchup system: Incorporates opponent strength into projections
- Performance tracking: Tracks player accuracy vs projections

Key changes:
- PlayerManager.py: Added calculate_adp_multiplier() method
- AddToRosterModeManager.py: Integrated matchup difficulty into scoring
- league_config.json: Added adp_weights and matchup_weights parameters

Testing:
- All unit tests passing (2200/2200)
- Epic smoke testing passed (4/4 parts)
- Epic QC rounds passed (3/3)
EOF
)"
```

**Why this works:**
- Clear epic name in subject line
- Lists all 3 major features with brief descriptions
- Documents key file changes with what changed
- Shows testing validation
- Uses feat/ prefix for feature epic

---

## Example 2: Single Feature Epic

**Scenario:** Epic with one substantial feature

```bash
git commit -m "$(cat <<'EOF'
feat/KAI-2: Complete data_export_system epic

Major features:
- Data export system: Exports league data to CSV/JSON formats

Key changes:
- DataExporter.py: New class for exporting league data
- league_helper_main.py: Added export mode to main menu
- data/export_templates/: Added CSV/JSON export templates

Testing:
- All unit tests passing (2250/2250)
- Epic smoke testing passed (4/4 parts)
- Epic QC rounds passed (3/3)
EOF
)"
```

**Why this works:**
- Single feature clearly described
- Key changes listed with context
- Testing results included
- Concise but complete

---

## Example 3: Bug Fix Epic

**Scenario:** Epic that fixes critical bugs

```bash
git commit -m "$(cat <<'EOF'
fix/KAI-3: Fix ADP data loading issues

Bug fixes:
- Fixed null pointer exception when ADP data missing
- Corrected off-by-one error in ADP ranking calculation
- Fixed encoding issue with special characters in player names

Key changes:
- PlayerManager.py: Added null checks for ADP data
- adp_csv_loader.py: Fixed ranking calculation logic
- utils/csv_utils.py: Changed encoding to utf-8-sig

Testing:
- All unit tests passing (2250/2250)
- Epic smoke testing passed (4/4 parts)
- Epic QC rounds passed (3/3)
- User testing passed with ZERO bugs
EOF
)"
```

**Why this works:**
- Uses fix/ prefix for bug fix epic
- Lists all bugs fixed
- Documents what was changed and why
- Shows user testing validation

---

## Example 4: Epic with Bug Fixes During Development

**Scenario:** Epic with features + bug fixes discovered during user testing

```bash
git commit -m "$(cat <<'EOF'
feat/KAI-4: Complete trade_analyzer epic

Major features:
- Trade analyzer: Evaluates trade fairness and value
- Trade history: Tracks past trades and outcomes

Bug fixes (found during user testing):
- Fixed incorrect point calculation in trade evaluation
- Corrected display formatting for multi-player trades

Key changes:
- TradeAnalyzer.py: New class for trade evaluation logic
- TradeHistoryManager.py: New class for tracking trade history
- league_helper_main.py: Added trade analyzer mode to menu
- bugfix_high_point_calculation/: Fixed calculation bug

Testing:
- All unit tests passing (2300/2300)
- Epic smoke testing passed (4/4 parts)
- Epic QC rounds passed (3/3)
- User testing passed after bug fixes
EOF
)"
```

**Why this works:**
- Clearly separates features from bug fixes
- Documents bug fixes found during user testing
- Shows iterative improvement process
- Includes bug fix folder reference

---

## Commit Message Anti-Patterns

**❌ DON'T DO THIS:**

```bash
# Too vague
git commit -m "updates"
git commit -m "changes"
git commit -m "fixes"

# No context
git commit -m "updated PlayerManager"

# Emojis and subjective language
git commit -m "✨ Amazing new feature! 🎉"
git commit -m "Fixed super annoying bug"

# Missing testing information
git commit -m "Complete epic"  # No mention of test status

# Wrong format (not using KAI numbering)
git commit -m "feat: Complete epic"  # Missing KAI-{number}
git commit -m "epic/KAI-1: Complete epic"  # Wrong prefix (should be feat or fix)
```

**✅ DO THIS INSTEAD:**

```bash
# Clear, descriptive, includes testing
git commit -m "$(cat <<'EOF'
feat/KAI-5: Complete player_comparison epic

Major features:
- Player comparison tool: Side-by-side stats comparison

Key changes:
- PlayerComparer.py: New comparison logic
- league_helper_main.py: Added comparison mode

Testing:
- All unit tests passing (2320/2320)
- Epic smoke testing passed (4/4 parts)
EOF
)"
```

---

## Using HEREDOC for Commit Messages

**Why use HEREDOC:**
- Preserves multi-line formatting
- Handles special characters correctly
- Ensures commit message body is formatted properly

**Syntax:**

```bash
git commit -m "$(cat <<'EOF'
{Commit message subject line}

{Commit message body with multiple lines}
- Bullet point 1
- Bullet point 2

{More sections as needed}
EOF
)"
```

**Important:**
- Use `<<'EOF'` (single quotes) to prevent variable expansion
- Close with `EOF` on its own line
- Don't indent the closing `EOF`

---

## Commit Message Checklist

Before committing, verify your commit message has:

- [ ] **Subject line** with format: `{commit_type}/KAI-{number}: {message}`
- [ ] **Subject line** is 100 characters or less
- [ ] **commit_type** is either "feat" or "fix" (NOT "epic")
- [ ] **KAI number** matches branch and EPIC_TRACKER.md
- [ ] **Major features** section listing all features
- [ ] **Key changes** section documenting file changes
- [ ] **Testing** section showing test results
- [ ] **No emojis** or subjective language
- [ ] **Imperative mood** ("Add" not "Added")
- [ ] **Clear and descriptive** (future agents can understand)

---

**END OF COMMIT MESSAGE EXAMPLES**
