# Epic Folder Naming Convention Updated to Include KAI Number

**Date:** 2026-01-04
**Purpose:** Document the architectural change to include KAI numbers in epic folder names

---

## Summary of Change

**BEFORE:** Epic folders named `feature-updates/{epic_name}/`

**AFTER:** Epic folders named `feature-updates/KAI-{N}-{epic_name}/`

**Example:**
- Before: `feature-updates/improve_draft_helper/`
- After: `feature-updates/KAI-1-improve_draft_helper/`

---

## Rationale for Change

**Including KAI number in folder name provides:**

1. **Unique Folder Names** - Prevents conflicts if epic names are similar or reused
2. **Consistency with Branch Naming** - Matches branch convention (`epic/KAI-{N}`)
3. **Quick Identification** - Epic number visible in file system, easier to reference
4. **Better Organization** - Epic number provides chronological ordering
5. **Clearer Git History** - Folder name matches branch and commit messages

---

## What Changed

### Folder Naming Format

**Epic Folder:** `feature-updates/KAI-{N}-{epic_name}/`
- Example: `feature-updates/KAI-1-improve_draft_helper/`
- Example: `feature-updates/KAI-3-integrate_new_player_data_into_simulation/`

**Original Request File:** `feature-updates/{epic_name}.txt` (NO KAI number)
- Remains unchanged to allow user flexibility in naming

**Feature Folders:** `feature-updates/KAI-{N}-{epic_name}/feature_XX_{name}/`
- Example: `feature-updates/KAI-1-improve_draft_helper/feature_01_adp_integration/`

**Research Folder:** `feature-updates/KAI-{N}-{epic_name}/research/`
- Example: `feature-updates/KAI-1-improve_draft_helper/research/`

**Debugging Folder:** `feature-updates/KAI-{N}-{epic_name}/debugging/`
- Example: `feature-updates/KAI-1-improve_draft_helper/debugging/`

**Done Folder:** `feature-updates/done/KAI-{N}-{epic_name}/`
- Example: `feature-updates/done/KAI-1-improve_draft_helper/`

### Git Branch and Commit Format (Unchanged)

**Branch:** `{work_type}/KAI-{N}`
- Example: `epic/KAI-1`, `feat/KAI-2`, `fix/KAI-3`

**Commit:** `{commit_type}/KAI-{N}: {message}`
- Example: `feat/KAI-1: Add ADP integration to PlayerManager`

---

## Files Modified

### 1. CLAUDE.md

**Changes:**
- Added "KAI Number" to Terminology section
- Updated Stage 1 workflow to include KAI number assignment
- Updated epic folder structure examples
- Added new subsection "Epic Folder Naming Convention" with format and examples
- Updated debugging protocol file structure paths

**New Section Added:**
```markdown
### Epic Folder Naming Convention

**Format:** `feature-updates/KAI-{N}-{epic_name}/`
**Examples:**
- `feature-updates/KAI-1-improve_draft_helper/`
- `feature-updates/KAI-3-integrate_new_player_data_into_simulation/`

**Original Request File:** `feature-updates/{epic_name}.txt` (no KAI number)
**Why include KAI number:** Ensures unique folder names, matches branch naming, enables quick identification
```

### 2. stages/stage_1/epic_planning.md

**Changes:**

**Step 1.1: Create Epic Folder**
- Updated `mkdir` command: `mkdir -p feature-updates/KAI-{N}-{epic_name}/`
- Added example: `mkdir -p feature-updates/KAI-1-improve_draft_helper/`
- Updated folder naming rules to explain KAI number format
- Added "Why include KAI number in folder name" section

**Step 1.2: Move Epic Request File**
- Updated `mv` command: `mv feature-updates/{epic_name}.txt feature-updates/KAI-{N}-{epic_name}/{epic_name}_notes.txt`
- Added example
- Added note explaining original request file does NOT include KAI number

**Step 4.1: Create Feature Folders**
- Updated `mkdir` command: `mkdir -p feature-updates/KAI-{N}-{epic_name}/feature_{N}_{descriptive_name}/`
- Updated `cd` command: `cd feature-updates/KAI-{N}-{epic_name}/feature_{N}_{name}/`
- Added examples for both commands

**Step 4.4: Create research/ Folder**
- Updated `mkdir` command: `mkdir -p feature-updates/KAI-{N}-{epic_name}/research/`
- Added example

### 3. stages/stage_7/epic_cleanup.md

**Changes:**

**Step 4a: Find ALL Lessons Learned Files**
- Updated all `find` commands to use `KAI-{N}-{epic_name}` format
- Added example: `find feature-updates/done/KAI-1-improve_draft_helper -name "lessons_learned.md" -type f`
- Updated expected results paths

**Step 6c: Move Entire Epic Folder to done/**
- Updated Windows command: `move feature-updates\KAI-{N}-{epic_name} feature-updates\done\KAI-{N}-{epic_name}`
- Updated Linux/Mac command: `mv feature-updates/KAI-{N}-{epic_name} feature-updates/done/KAI-{N}-{epic_name}`
- Added examples for both platforms

**Step 6d: Verify Move Successful**
- Updated `ls` command: `ls feature-updates/done/KAI-{N}-{epic_name}/`
- Added example

**Step 7d: Update EPIC_README.md One Final Time**
- Updated completion summary template: `feature-updates/done/KAI-{N}-{epic_name}/`

### 4. templates/epic_lessons_learned_template.md

**Changes:**
- Updated Location field: `feature-updates/KAI-{N}-{epic_name}/epic_lessons_learned.md`

---

## Impact on Other Files

### Files that may need updates:

1. **epic_readme_template.md**
   - Update file location paths to include KAI number

2. **epic_smoke_test_plan_template.md**
   - Update file location paths to include KAI number

3. **Other stage guides (2-6)**
   - Update any references to epic folder paths
   - Update examples that show folder structure

4. **Reference cards**
   - Update folder naming examples
   - Update workflow diagrams if they show folder structure

5. **Debugging protocol guides**
   - Update any epic folder path references

---

## Workflow Changes

### Stage 1 (Epic Planning) - Step Order

**Updated workflow:**
1. Verify on main branch
2. Pull latest changes
3. **Assign KAI number from EPIC_TRACKER.md** ← Used in next steps
4. Determine work type (epic/feat/fix)
5. Create branch: `{work_type}/KAI-{N}`
6. Update EPIC_TRACKER.md
7. Commit EPIC_TRACKER.md update
8. **Create epic folder: `KAI-{N}-{epic_name}/`** ← Uses KAI number from step 3
9. Move epic request file into epic folder
10. Create EPIC_README.md
11. Continue with epic planning...

**Key Point:** KAI number is assigned BEFORE folder creation, ensuring consistent numbering

---

## Examples

### Complete Example: KAI-1

**1. User creates:** `feature-updates/improve_draft_helper.txt`

**2. Agent assigns:** KAI number 1

**3. Agent creates branch:** `epic/KAI-1`

**4. Agent creates folder:** `feature-updates/KAI-1-improve_draft_helper/`

**5. Agent moves request file:**
- From: `feature-updates/improve_draft_helper.txt`
- To: `feature-updates/KAI-1-improve_draft_helper/improve_draft_helper_notes.txt`

**6. Agent creates features:**
- `feature-updates/KAI-1-improve_draft_helper/feature_01_adp_integration/`
- `feature-updates/KAI-1-improve_draft_helper/feature_02_matchup_difficulty/`

**7. Agent creates research:** `feature-updates/KAI-1-improve_draft_helper/research/`

**8. After completion, moves to done:** `feature-updates/done/KAI-1-improve_draft_helper/`

**9. Original request remains:** `feature-updates/improve_draft_helper.txt` (for reference)

---

## Migration Strategy

### For New Epics

Starting immediately, all new epics MUST use the new naming convention:
- `feature-updates/KAI-{N}-{epic_name}/`

### For In-Progress Epics

**If epic is currently in Stage 1-7:**
- Complete using old naming convention
- Do NOT rename mid-epic (risk of breaking references)
- Apply new convention to next epic

### For Completed Epics in done/

**Do NOT rename:**
- Completed epics in `done/` folder remain as-is
- Older naming is preserved in git history
- No need to retroactively update

---

## Verification Checklist

**To verify this change is complete:**

- [x] CLAUDE.md updated with terminology and folder naming convention
- [x] stages/stage_1/epic_planning.md updated (folder creation steps)
- [x] stages/stage_7/epic_cleanup.md updated (move commands, find commands)
- [x] templates/epic_lessons_learned_template.md updated
- [ ] templates/epic_readme_template.md (if applicable)
- [ ] templates/epic_smoke_test_plan_template.md (if applicable)
- [ ] Other stage guides (2-6) updated if they reference folder paths
- [ ] Reference cards updated
- [ ] Debugging protocol guides updated if they reference epic folder paths

---

## Benefits of This Change

1. **Eliminates Ambiguity**
   - Epic folders have unique identifiers
   - No confusion when epic names are similar

2. **Improves Traceability**
   - Easy to match folder to branch and commits
   - KAI number provides chronological order

3. **Better User Experience**
   - Quick identification: "Check epic KAI-3" instead of "Check improve_draft_helper"
   - File system shows epic number at a glance

4. **Consistency Across System**
   - Branches: `epic/KAI-{N}`
   - Folders: `KAI-{N}-{epic_name}/`
   - Commits: `feat/KAI-{N}: message`
   - All use same numbering scheme

5. **Future-Proof**
   - Supports epic name reuse without conflicts
   - Enables better epic management tools

---

## FAQ

**Q: Why doesn't the original request file include the KAI number?**
A: User creates `{epic_name}.txt` BEFORE KAI number is assigned. Agent assigns KAI number during Stage 1 setup, then creates the epic folder with the KAI number.

**Q: What if user creates a file named `KAI-1-improve_draft_helper.txt`?**
A: Agent should still assign the correct KAI number and create folder `KAI-{N}-improve_draft_helper/` based on EPIC_TRACKER.md, regardless of user's filename.

**Q: Do bugfix folders also include KAI numbers?**
A: Bugfix folders within an epic follow format: `KAI-{N}-{epic_name}/bugfix_{priority}_{name}/` - they're inside the KAI-numbered epic folder.

**Q: What about single-feature work (feat/ branch)?**
A: Single features still get a KAI number and folder: `feature-updates/KAI-{N}-{feature_name}/`

**Q: Should I update old epics in done/ folder?**
A: No. Leave completed epics as-is. Only use new convention for new epics starting from this point forward.

---

*End of EPIC_FOLDER_NAMING_WITH_KAI_NUMBER.md*
