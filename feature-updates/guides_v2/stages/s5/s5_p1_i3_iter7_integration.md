# S5: Feature Implementation
## S5.P1: Planning Round 1
### S5.P1.I3: Integration Gap Check

**Purpose:** Integration Gap Check
**Prerequisites:** Previous iterations complete
**Main Guide:** `stages/s5/s5_p1_planning_round1.md`
**Router:** `stages/s5/s5_p1_i3_integration.md`

---

## Iteration 7: Integration Gap Check (CRITICAL)

**Purpose:** Verify EVERY new method has an identified caller (no orphan code)

**⚠️ CRITICAL:** "If nothing calls it, it's not integrated"

**Process:**

### Step 1: List All NEW Methods/Functions This Feature Creates

Extract from implementation tasks:
- Example: load_adp_data(), _match_player_to_adp(), _calculate_adp_multiplier()

### Step 2: For EACH New Method, Identify Caller

**Example Integration Verification:**

```markdown
## Integration Verification

### Method: PlayerManager.load_adp_data()

**Caller:** PlayerManager.load_players() (existing method)
**Integration Point:** Line ~180 in load_players()
**Call Signature:** `self.adp_data = self.load_adp_data()`
**Verified:** ✅ Method will be called

**Call Chain:**
run_league_helper.py (entry point)
   → LeagueHelperManager.__init__()
   → PlayerManager.load_players()
   → PlayerManager.load_adp_data() ← NEW METHOD

**Orphan Check:** ✅ NOT ORPHANED (clear caller)

---

### Method: PlayerManager._match_player_to_adp(player)

**Caller:** PlayerManager.load_players() (existing method)
**Integration Point:** Line ~210 in load_players() loop
**Call Signature:** `self._match_player_to_adp(player)`
**Verified:** ✅ Method will be called for each player

**Call Chain:**
run_league_helper.py
   → LeagueHelperManager.__init__()
   → PlayerManager.load_players()
   → for player in players: ← LOOP
      → PlayerManager._match_player_to_adp(player) ← NEW METHOD

**Orphan Check:** ✅ NOT ORPHANED (called in loop)

---

### Method: PlayerManager._calculate_adp_multiplier(player)

**Caller:** FantasyPlayer.calculate_total_score()
**Integration Point:** Line ~235 in calculate_total_score()
**Call Signature:** `score *= self.adp_multiplier`
**Verified:** ✅ Field used in calculation

**Call Chain:**
AddToRosterModeManager.get_recommendations()
   → FantasyPlayer.calculate_total_score()
   → Uses: self.adp_multiplier ← NEW FIELD (set by Task 3)

**Orphan Check:** ✅ NOT ORPHANED (field consumed)
```

### Step 3: Verify Integration for ALL New Code

**Count:**
- New methods created: {N}
- Methods with identified caller: {M}

**Result:**
- ❌ **FAIL** if M < N (orphan methods exist)
- ✅ **PASS** if M == N (all integrated)

**If orphan methods found:**
- STOP - Fix integration
- Options:
  - Add caller (integrate the method)
  - Remove method (not needed)
- Document decision in implementation_plan.md

### Step 4: Create Integration Matrix

| New Method | Caller | Call Location | Verified |
|------------|--------|---------------|----------|
| load_adp_data() | PlayerManager.load_players() | PlayerManager.py:180 | ✅ |
| _match_player_to_adp() | PlayerManager.load_players() | PlayerManager.py:210 | ✅ |
| _calculate_adp_multiplier() | PlayerManager.load_players() | PlayerManager.py:215 | ✅ |

**Output:** Integration matrix added to implementation_plan.md, no orphan code

**🔄 After Iteration Checkpoint - questions.md Review:**

After completing this iteration, check if you have questions or found answers:

1. **If you discovered NEW uncertainties during this iteration:**
   - Add them to `questions.md` with context
   - Format: Question, context, impact on implementation

2. **If you found ANSWERS to existing questions in questions.md:**
   - Update questions.md to mark question as answered
   - Document the answer and source

3. **If no new questions and no answers found:**
   - No action needed, proceed to next iteration

**Note:** This is a quick check (1-2 minutes). questions.md will be presented to user at Gate 5.

**Update Agent Status:**
```text
Progress: Iteration 7/9 (Planning Round 1) complete
Next Action: Iteration 7a - Backward Compatibility Analysis
```

---

