# D19: Rules File Template Alignment

**Dimension Number:** 19
**Category:** Advanced Dimensions
**Context:** Child context only (skip in master context)
**Automation Level:** 30% automated
**Priority:** LOW
**Last Updated:** 2026-02-24

**Focus:** Verify the child project's rules file retains the structural sections and key guidance inherited from RULES_FILE.template.md
**Typical Issues Found:** 0-5 per audit

---

## Table of Contents

1. [What This Checks](#what-this-checks)
2. [Why This Matters](#why-this-matters)
3. [When This Applies](#when-this-applies)
4. [How to Locate the Rules File](#how-to-locate-the-rules-file)
5. [Pattern Types](#pattern-types)
6. [Automated Validation](#automated-validation)
7. [Manual Validation](#manual-validation)
8. [Severity Levels](#severity-levels)
9. [Real Examples](#real-examples)
10. [Integration with Other Dimensions](#integration-with-other-dimensions)
11. [See Also](#see-also)

---

## What This Checks

**D19: Rules File Template Alignment** verifies that a child project's AI rules file has not drifted significantly from the structure provided by `RULES_FILE.template.md`:

1. **Rules file locatable** — `.shamt/rules_file_path.conf` exists and points to a valid file
2. **Shamt Sync section present** — The rules file contains a Shamt Sync section with import guidance
3. **Git Conventions section present** — The rules file contains a Git Conventions section
4. **Key guidance retained** — Critical Shamt-specific guidance (sync workflow, when to import) has not been removed

**Coverage:**
- Child project's rules file only (CLAUDE.md, AGENTS.md, or equivalent)
- Not the template itself (D7 handles template currency)
- Not project-specific additions (those are intentional customizations)

**Key Purpose:**
Child projects inherit their rules file from `RULES_FILE.template.md` at init time and then customize it. Over time, Shamt-specific sections may be accidentally deleted or overwritten. This dimension flags structural drift before it causes workflow failures.

---

## Why This Matters

Child projects initialize their rules file from `RULES_FILE.template.md` and then customize it over time. Critical Shamt-specific sections — particularly the Shamt Sync section (import guidance, when to import, `last_sync.conf` reference) and Git Conventions section — may be accidentally deleted during large rules file restructurings or overwritten when following non-Shamt templates.

Without these sections, agents operating in the child project:
- May not know how or when to run the import script, causing guides to go stale
- May not follow the correct branch and commit format for Shamt projects
- May produce contributions that fail PR review due to missing git convention adherence

This dimension catches structural drift before it causes workflow failures.

---

## When This Applies

**D19 is child context only.**

To determine your context, check whether `.shamt/shamt_master_path.conf` exists:
- **File present** → you are in a child project → **D19 applies**
- **File absent** → you are in the master Shamt repo → **skip D19**

If you are in the master context, mark D19 as N/A and proceed to round exit.

---

## How to Locate the Rules File

**Step 1: Read rules_file_path.conf**

```bash
cat .shamt/rules_file_path.conf
```

This file is written by `init.sh` / `init.ps1` at initialization time. It stores the full path to the project's AI rules file (e.g., `/absolute/path/to/CLAUDE.md` or `/absolute/path/to/AGENTS.md`).

**Step 2: Verify the path is valid**

```bash
RULES_PATH=$(cat .shamt/rules_file_path.conf 2>/dev/null)
if [ -z "$RULES_PATH" ]; then
    echo "rules_file_path.conf is empty or missing"
elif [ ! -f "$RULES_PATH" ]; then
    echo "Rules file not found at stored path: $RULES_PATH"
else
    echo "Rules file located: $RULES_PATH"
fi
```

**If rules_file_path.conf is missing or the path is invalid:**
- Flag as LOW severity (see Severity Levels below)
- D19 cannot complete the full check until the path is valid
- Suggested fix: re-run `init.sh` / `init.ps1` to update `rules_file_path.conf`

---

## Pattern Types

Once the rules file is located, perform these checks:

### Check 1: Shamt Sync Section

**What to look for:** A section covering the Shamt sync workflow — import instructions, when to import, and guide freshness.

```bash
RULES_PATH=$(cat .shamt/rules_file_path.conf)
grep -n "Shamt Sync\|shamt sync\|import.sh\|import.ps1\|last_sync" "$RULES_PATH"
```

**Pass:** One or more matches found.
**Fail:** No matches — the Shamt Sync section may have been removed.

### Check 2: Git Conventions Section

**What to look for:** A section covering branch naming, commit format, or Git workflow conventions.

```bash
RULES_PATH=$(cat .shamt/rules_file_path.conf)
grep -n "Git Conventions\|git conventions\|Branch format\|Commit format\|branch format\|commit format" "$RULES_PATH"
```

**Pass:** One or more matches found.
**Fail:** No matches — the Git Conventions section may have been removed.

### Check 3: Import Guidance Present

**What to look for:** Specific guidance on running the import script.

```bash
RULES_PATH=$(cat .shamt/rules_file_path.conf)
grep -n "import.sh\|import.ps1\|\.shamt/scripts/import" "$RULES_PATH"
```

**Pass:** At least one reference to the import script.
**Fail:** No reference — agents may not know how to trigger a sync.

### Check 4: shamt_master_path.conf Mentioned

**What to look for:** A note about the master path configuration file (so agents know how to fix stale path errors).

```bash
RULES_PATH=$(cat .shamt/rules_file_path.conf)
grep -n "shamt_master_path" "$RULES_PATH"
```

**Pass:** Reference found.
**Fail:** Reference missing. This is informational — LOW severity only.

---

## Automated Validation

**Pre-audit script coverage:** D19 is not included in `scripts/pre_audit_checks.sh` because it requires reading `.shamt/rules_file_path.conf`, applying child-context detection logic, and reaching outside the audit directory. Run manually.

**Partial automation (30%):**
- ✅ Check for `rules_file_path.conf` existence and non-empty path
- ✅ Verify the file at the stored path exists
- ✅ Grep for section keywords (Shamt Sync, Git Conventions, import.sh)
- ❌ Evaluate whether remaining content is substantively equivalent to the template (requires human judgment)
- ❌ Assess whether gaps are intentional customizations vs accidental deletions

---

## Manual Validation

### Full D19 Process

**Step 1: Determine context**

```bash
[ -f .shamt/shamt_master_path.conf ] && echo "CHILD context — D19 applies" || echo "MASTER context — skip D19"
```

**Step 2: Locate the rules file**

```bash
cat .shamt/rules_file_path.conf
```

If missing or invalid, file a LOW severity finding and stop. D19 cannot complete without a valid path.

**Step 3: Run all four checks**

Run the grep commands from the Validation Checks section above for each of the four checks.

**Step 4: Read the Shamt Sync section manually**

Open the rules file and read the Shamt Sync section. Verify:

- [ ] Import command is present and correct (`.shamt/scripts/import/import.sh` or equivalent)
- [ ] "When to import" guidance is present (at least a mention of `last_sync.conf` or a trigger condition)
- [ ] Reference to `guides/sync/README.md` or equivalent sync guide is present

**Step 5: Assess severity of any gaps**

See Severity Levels below.

**Step 6: Document findings**

For each missing section, create an audit finding following the standard template. Severity is typically LOW unless a complete section is missing (HIGH).

---

## Severity Levels

| Condition | Severity | Rationale |
|-----------|----------|-----------|
| `rules_file_path.conf` missing or path invalid | LOW | Agent cannot verify — needs investigation, not blocking |
| Shamt Sync section entirely absent | HIGH | Agent has no sync workflow guidance |
| Git Conventions section entirely absent | HIGH | Agent has no commit/branch format guidance |
| Import command missing from Shamt Sync section | MEDIUM | Agent may not know how to trigger a sync |
| `last_sync.conf` or "when to import" guidance missing | MEDIUM | Agent cannot make informed sync decisions |
| `shamt_master_path.conf` note missing | LOW | Informational — reduces discoverability of fix procedure |

**Note:** Project-specific additions (extra sections, customized wording) are NOT issues — they are intentional customizations. Only flag when Shamt-specific sections or guidance are absent.

---

## Real Examples

### Example 1: Rules File Path Stale After Machine Change

**Situation:** User moved to a new machine. `rules_file_path.conf` still contains the old absolute path.

**Check output:**
```bash
$ cat .shamt/rules_file_path.conf
/old/machine/path/to/project/CLAUDE.md

$ [ -f "/old/machine/path/to/project/CLAUDE.md" ] && echo "exists" || echo "missing"
missing
```

**Finding:**
```text
D19: Rules File Template Alignment
File: .shamt/rules_file_path.conf
Severity: LOW
Issue: rules_file_path.conf contains stale path — rules file not found at stored location
Fix: Re-run init.sh / init.ps1 to update rules_file_path.conf with current path
```

---

### Example 2: Shamt Sync Section Accidentally Deleted

**Situation:** During a large cleanup of the rules file, the Shamt Sync section was deleted.

**Check output:**
```bash
$ RULES_PATH=$(cat .shamt/rules_file_path.conf)
$ grep -n "Shamt Sync\|import.sh\|last_sync" "$RULES_PATH"
[no output]
```

**Finding:**
```text
D19: Rules File Template Alignment
File: CLAUDE.md
Severity: HIGH
Issue: Shamt Sync section appears to be missing — no references to import script or sync workflow found
Fix: Re-add Shamt Sync section from RULES_FILE.template.md
```

---

### Example 3: All Sections Present, Minor Customization

**Situation:** The project has customized the Shamt Sync section with project-specific notes but retains all key guidance.

**Check output:**
```bash
$ RULES_PATH=$(cat .shamt/rules_file_path.conf)
$ grep -n "Shamt Sync\|import.sh\|last_sync\|guides/sync" "$RULES_PATH"
45: ## Shamt Sync
48: bash .shamt/scripts/import/import.sh
51: Check `.shamt/last_sync.conf` for the date of the last import
54: See `.shamt/guides/sync/README.md` for the full sync workflow
```

**Finding:** No issues. All key guidance present; customization is intentional. Mark D19 as clean.

---

## Integration with Other Dimensions

**D4: CLAUDE.md Synchronization** — D4 checks whether quick references in the root CLAUDE.md match actual guide content. D19 is distinct: it checks whether Shamt-specific structural sections have been retained, not whether references within them are accurate.

**D7: Template Currency** — D7 checks whether `RULES_FILE.template.md` itself is up to date. D19 checks whether the child's rules file is structurally aligned with the template — a complementary check from the opposite direction.

**D6: Content Completeness** — D6 catches missing sections in guide files generally. D19 specifically targets Shamt structural sections in the rules file. If D6 already flagged the rules file for missing sections, D19 provides additional context about which template sections are expected.

---

## See Also

- `../stages/stage_1_discovery.md` - How to identify audit context (master vs child) before starting discovery
- `../stages/stage_4_verification.md` - Re-verify D19 compliance after fixes
- `d7_template_currency.md` - D7 checks whether `RULES_FILE.template.md` itself is current (complementary direction)
- `d4_claude_md_sync.md` - D4 checks cross-reference accuracy within the rules file

---

**Last Updated:** 2026-02-24
**Version:** 1.0
**Status:** New (SHAMT-2)
