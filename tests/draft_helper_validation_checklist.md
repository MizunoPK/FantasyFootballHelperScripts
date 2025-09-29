# Draft Helper Integration Test Validation Checklist

**Purpose**: Comprehensive validation guide for verifying draft helper functionality
**Target**: Other agents or testers validating the draft helper system
**Duration**: ~5-10 minutes to complete all tests

## 🚀 **Quick Setup**

Before starting, ensure:
- [ ] You're in the project root directory: `/home/kai/code/FantasyFootballHelperScripts`
- [ ] Python virtual environment is activated
- [ ] **Startup Validation**: Core applications start without errors
- [ ] Draft helper can be launched with: `python run_draft_helper.py`

### **Core Application Startup Tests**
```bash
# Test player data fetcher startup (10 second timeout)
timeout 10 python run_player_data_fetcher.py
# Expected: Shows startup message, loads config, no import errors

# Test NFL scores fetcher startup (10 second timeout)
timeout 10 python run_nfl_scores_fetcher.py
# Expected: Shows startup message, begins operation, no import errors

# Test draft helper startup
python run_draft_helper.py
# Expected: Shows "Draft Helper!" with "Waiver Optimizer" option in menu
```

**✅ Startup Requirements**:
- [ ] Player data fetcher starts without import/config errors
- [ ] NFL scores fetcher starts without import/config errors
- [ ] Draft helper displays main menu properly

---

## 📋 **Test Execution Steps**

### **Test 1: Mark Drafted Player (Steps 1-4)**

**🎯 Objective**: Verify player search and draft status modification

**Input Sequence**:
```bash
python run_draft_helper.py
2              # Mark Drafted Player
[SEARCH_NAME]  # Search for any available player (drafted=0)
1              # Select first result
exit           # Return to main menu
```

**✅ Expected Results**:
- [ ] Search finds available players (drafted=0)
- [ ] Successfully marks selected player as drafted by another team
- [ ] Returns to main menu without errors
- [ ] **CSV Validation**: Selected player shows `drafted=1` in CSV

**📋 How to Choose Test Player**:
- Use any common name fragment like "Smith", "Johnson", or "Brown"
- Look for players showing as available in the search results
- First result is usually fine for testing purposes

---

### **Test 2: Waiver Optimizer Verification (Steps 5-7)**

**🎯 Objective**: Verify waiver recommendations exclude drafted players

**Input Sequence**:
```bash
3              # Waiver Optimizer
[Enter]        # Acknowledge results
```

**✅ Expected Results**:
- [ ] Waiver optimizer completes without errors
- [ ] Shows current roster with accurate fantasy points (calculated scores, not raw fantasy points)
- [ ] **CRITICAL**: Player marked in Test 1 does NOT appear in waiver recommendations
- [ ] Returns to main menu after pressing Enter

---

### **Test 3: Drop Player Functionality (Steps 8-11)**

**🎯 Objective**: Verify player removal from draft status and roster

**Input Sequence**:
```bash
4              # Drop Player Mode
[SEARCH_NAME1] # Search for player marked in Test 1
1              # Select first result (no confirmation needed)
[SEARCH_NAME2] # Search for any roster player (drafted=2)
1              # Select first result (no confirmation needed)
exit           # Return to main menu
```

**✅ Expected Results**:
- [ ] Successfully finds and drops Test 1 player (drafted=1 → drafted=0) - **NO CONFIRMATION PROMPT**
- [ ] Successfully finds and drops roster player (drafted=2 → drafted=0) - **NO CONFIRMATION PROMPT**
- [ ] Roster display updates showing roster player removed
- [ ] **Roster Count**: Main menu shows updated roster count (decreases by 1)
- [ ] **CSV Validation**: Both players show `drafted=0` in CSV

**📋 How to Choose Test Players**:
- First player: Use same search term from Test 1
- Second player: Use any partial name from current roster display

---

### **Test 4: Add to Roster Functionality (Steps 12-13)**

**🎯 Objective**: Verify roster addition and recommendations

**Input Sequence**:
```bash
1              # Add to Roster
1              # Select first recommendation
```

**✅ Expected Results**:
- [ ] **CRITICAL**: Player dropped in Test 3 should appear in top recommendations
- [ ] **Point Display**: All recommendations show calculated scores (used for ranking), not raw fantasy points
- [ ] Successfully adds selected player back to roster
- [ ] Roster display shows player back in lineup
- [ ] **Roster Count**: Main menu shows updated roster count (increases by 1)
- [ ] **CSV Validation**: Added player shows `drafted=2` in CSV

**📋 Expected Behavior**:
- Player removed in Test 3 should be prioritized in recommendations
- Recommendations are sorted by calculated score (highest first)

---

### **Test 5: Lock/Unlock Player System (Steps 14-19)**

**🎯 Objective**: Verify player locking affects trade recommendations

**Input Sequence**:
```bash
5              # Lock/Unlock Player
[ROSTER_NUM]   # Select any roster player number - NO CONFIRMATION
[BACK_NUM]     # Back to main menu (check menu for correct number)
3              # Waiver Optimizer
[Enter]        # Return to main menu
5              # Lock/Unlock Player
[ROSTER_NUM]   # Select same player - NO CONFIRMATION
[BACK_NUM]     # Back to main menu
```

**✅ Expected Results**:
- [ ] Shows current lock status for all roster players
- [ ] Successfully toggles lock status - **NO CONFIRMATION PROMPT**
- [ ] **CRITICAL**: Lock status affects waiver optimizer suggestions
- [ ] Successfully toggles lock status back - **NO CONFIRMATION PROMPT**
- [ ] **CSV Validation**: Lock status changes reflected in CSV

**📋 How to Choose Test Player**:
- Look at the Lock/Unlock menu to see which players are listed
- Choose any roster player number from the displayed list
- Note the "Back to main menu" option number (usually last option)

---

### **Test 6: Starter Helper Integration (Steps 20-22)**

**🎯 Objective**: Verify optimal lineup generation

**Input Sequence**:
```bash
6              # Starter Helper
[Enter]        # Return to main menu
```

**✅ Expected Results**:
- [ ] Generates optimal starting lineup without errors
- [ ] Shows accurate fantasy points for each position
- [ ] **FLEX Validation**: FLEX position shows a player (not empty)
- [ ] **Position Validation**: All starting positions filled appropriately
- [ ] Shows bench alternatives with points
- [ ] Creates timestamped results file

---

### **Test 7: Trade Simulator Validation (Steps 20-22)**

**🎯 Objective**: Verify trade simulation functionality (NEW)

**Input Sequence**:
```bash
7              # Trade Simulator
4              # Exit Trade Simulator
```

**✅ Expected Results**:
- [ ] **Trade Simulator Menu**: Shows as option 7 (Quit moved to option 8)
- [ ] **Roster Display**: Shows numbered list 1-15 with fantasy points
- [ ] **Score Display**: Shows current total score and difference (should be +0.00 initially)
- [ ] **Menu Options**: Shows 4 trade simulator options
- [ ] **Exit**: Successfully returns to main menu
- [ ] **State Preservation**: Original roster unchanged after exit

---

### **Test 8: Clean Exit (Step 23)**

**🎯 Objective**: Verify proper application termination

**Input Sequence**:
```bash
8              # Quit (moved from option 7 to 8)
```

**✅ Expected Results**:
- [ ] Displays "Goodbye!" message
- [ ] Application terminates cleanly
- [ ] No error messages or exceptions

---

## 🔍 **Critical Validations**

### **FLEX System Validation**
- [ ] **Display Check**: Roster shows WR (4/4) and FLEX (1/1), not WR (5/4)
- [ ] **Functionality Check**: FLEX position properly used in starter helper
- [ ] **Assignment Check**: 5th WR automatically assigned to FLEX slot

### **Data Persistence Validation**
- [ ] **CSV Updates**: All player status changes reflected in `shared_files/players.csv`
- [ ] **Lock Status**: Player locking persists in CSV with `locked=1/0`
- [ ] **Draft Status**: Proper values: `drafted=0` (available), `drafted=1` (other team), `drafted=2` (your team)

### **UI Enhancement Validation (NEW)**
- [ ] **Roster Count**: Main menu accurately shows current roster count and updates after changes
- [ ] **Point Display**: Add to Roster mode shows calculated scores (ranking values), not raw fantasy points
- [ ] **No Confirmations**: Drop Player and Lock/Unlock modes proceed immediately without (y/n) prompts
- [ ] **Fuzzy Search**: Empty input in Mark Drafted/Drop Player modes returns to main menu
- [ ] **Waiver Optimizer**: Menu shows "Waiver Optimizer" instead of "Trade Analysis"

### **Point Calculation Validation**
- [ ] **Consistency**: Fantasy points consistent across all modes
- [ ] **Accuracy**: Points match expected ranges (200+ for top players)
- [ ] **Waiver Optimizer**: Points properly calculated for waiver recommendations
- [ ] **Ranking Logic**: Add to Roster recommendations show calculated scores used for ranking

---

## 🚨 **Automated Validation Command**

For quick verification, run this automated test sequence:

```bash
echo -e "2\nSmith\n1\nexit\n3\n\n4\nSmith\n1\nWalker\n1\nexit\n1\n1\n5\n1\n[BACK_NUM]\n3\n\n5\n1\n[BACK_NUM]\n6\n\n7\n4\n8\n" | python run_draft_helper.py
```

**Expected Result**: Should complete without errors and show proper roster changes.

**📋 Command Explanation**:
- Uses generic search terms that should find players in most data states
- Adapts to current roster composition
- Tests all core functionality including new Trade Simulator
- Replace `[BACK_NUM]` with actual back menu option number

**Alternative Simple Test**:
```bash
echo -e "7\n4\n8\n" | python run_draft_helper.py
```
This tests Trade Simulator access and clean exit functionality.

---

## ❌ **Common Failure Points**

### **Known Issues to Watch For**:
- [ ] **FLEX Display Bug**: If roster shows WR (5/4), FLEX assignment is broken
- [ ] **CSV Permission Errors**: Ensure write permissions to `shared_files/players.csv`
- [ ] **Search Failures**: Player name search should be case-insensitive and partial-match
- [ ] **Lock State Persistence**: Lock changes should persist across menu actions
- [ ] **Confirmation Prompts**: Should NOT appear in Drop Player or Lock/Unlock modes
- [ ] **Point Display**: Add to Roster should show calculated scores, not raw fantasy points
- [ ] **Roster Count**: Should update immediately after roster changes

### **If Tests Fail**:
1. Check CSV file permissions and write access
2. Verify virtual environment is activated
3. Ensure no other processes are using the CSV file
4. Check that `shared_files/players.csv` exists and is properly formatted

---

## 📊 **Success Criteria**

**✅ ALL TESTS PASSED**: Draft helper is fully functional
- All 24 test steps completed without errors (including Trade Simulator)
- CSV file updates correctly reflect all changes
- FLEX system working properly (4/4 WR + 1/1 FLEX)
- Waiver optimizer excludes locked and drafted players
- Starter helper generates valid lineups
- Trade Simulator accessible as option 7 with full functionality
- UI enhancements working: no confirmations, empty input exits, calculated scores shown
- Roster count updates correctly after changes

**❌ TESTS FAILED**: Issues require investigation
- Note specific failure points for debugging
- Check error messages and CSV file state
- Verify FLEX assignment logic if roster display is incorrect
- Check Trade Simulator menu integration and functionality

---

## 📝 **Test Results Log Template**

```
DRAFT HELPER VALIDATION RESULTS
================================
Date: [DATE]
Tester: [NAME]
Duration: [MINUTES]

Test 1 - Mark Drafted Player: ✅/❌
Test 2 - Waiver Optimizer: ✅/❌
Test 3 - Drop Player: ✅/❌
Test 4 - Add to Roster: ✅/❌
Test 5 - Lock/Unlock: ✅/❌
Test 6 - Starter Helper: ✅/❌
Test 7 - Trade Simulator: ✅/❌
Test 8 - Clean Exit: ✅/❌

FLEX System: ✅/❌
CSV Updates: ✅/❌
Point Accuracy: ✅/❌
Trade Simulator: ✅/❌

Overall Result: ✅ PASS / ❌ FAIL
Notes: [ADDITIONAL OBSERVATIONS]
```

---

*This checklist validates all core draft helper functionality including the FLEX assignment system and the new Trade Simulator feature. The test procedures are designed to be adaptive to any player data state.*