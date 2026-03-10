#!/bin/bash
# Pre-Audit Automated Checks
# Runs before manual audit to catch common structural issues
#
# Coverage: 12 of 20 dimensions (D1, D3, D4, D8, D9, D10, D11, D12, D14, D17, D18, D20 partial)
# Estimated: 45-55% of typical issues (based on SHAMT-2 Round 1-2 data)
# NOT Checked: D2 (Terminology - requires pattern-specific search, see dimension guide)
# NOT Checked: D5, D6, D7, D13, D15, D16, D19 (require manual audit); D20 mostly manual
#
# Last Updated: 2026-02-25 (SHAMT-3: D20 added, sync/ scope extended, CHECK 13 gitignore check)
# Changes:
#   - Round 3: Simplified file size threshold from 3-tier (600/800/1000) to 1000-line baseline
#   - Round 3: Added 17 known exceptions for Prerequisites/Exit Criteria checks (now 19 -- see known_exceptions.md)
#   - Meta-Audit: Increased baseline from 1000 -> 1250 lines for comprehensive reference guides
#   - Exceptions documented in audit/reference/known_exceptions.md
#   - 2026-02-19: Added D14 Character and Format Compliance check (banned Unicode chars)
#   - 2026-02-24: SHAMT-2 dimension renumbering; D19 Rules File Template Alignment added (manual only)
#   - 2026-02-25: SHAMT-3 Phase 3 — D8/D11/D14 extended to cover sync/, D14 scans RULES_FILE.template.md, CHECK 13 gitignore verification (partial D20)

# set -e  # Exit on error - DISABLED: causes premature exit in file size check loop

# Colors for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Counters
TOTAL_ISSUES=0
CRITICAL_ISSUES=0
WARNING_ISSUES=0

echo "=================================="
echo "Pre-Audit Automated Checks"
echo "=================================="
echo ""

# Change to guides_v2 directory (from audit/scripts/ up to guides_v2/)
cd "$(dirname "$0")/../.." || exit 1

# ============================================================================
# CHECK 1: File Size Assessment (D11)
# ============================================================================

echo -e "${BLUE}=== File Size Assessment (D11) ===${NC}"
echo ""

TOO_LARGE=0
LARGE=0

for file in $(find stages sync -name "*.md" 2>/dev/null); do
  lines=$(wc -l < "$file")

  if [ "$lines" -gt 1250 ]; then
    echo -e "${RED}❌ TOO LARGE:${NC} $file ($lines lines) - exceeds 1250-line baseline"
    ((TOO_LARGE++))
    ((CRITICAL_ISSUES++))
    ((TOTAL_ISSUES++))
  fi
done

if [ $TOO_LARGE -eq 0 ]; then
  echo -e "${GREEN}✅ All files within 1250-line baseline${NC}"
fi

echo ""
echo "Files >1250 lines: $TOO_LARGE"
echo ""
echo "Note: Files ≤1250 lines are acceptable if content is non-duplicated."
echo "      Updated policy:"
echo "        - Round 3 (2026-02-05): Simplified from 3-tier to single 1000-line baseline"
echo "        - Meta-Audit (2026-02-05): Increased baseline to 1250 lines for comprehensive reference guides"
echo ""

# ============================================================================
# CHECK 1b: Policy Compliance - CLAUDE.md Character Limit (D11)
# ============================================================================

echo -e "${BLUE}=== Policy Compliance Check ===${NC}"
echo ""

# Check CLAUDE.md size
claude_md="../../CLAUDE.md"
if [ -f "$claude_md" ]; then
    claude_size=$(wc -c < "$claude_md")
    if [ $claude_size -gt 40000 ]; then
        echo -e "${RED}❌ POLICY VIOLATION:${NC} CLAUDE.md ($claude_size chars) exceeds 40,000 character limit"
        echo "   Overage: $((claude_size - 40000)) characters"
        echo "   Reason: Large files create barriers for agent comprehension"
        echo "   Action: Extract ~$((claude_size - 40000)) characters to separate files"
        ((CRITICAL_ISSUES++))
        ((TOTAL_ISSUES++))
    else
        echo -e "${GREEN}✅ PASS:${NC} CLAUDE.md ($claude_size chars) within 40,000 character limit"
    fi
else
    echo -e "${YELLOW}⚠️  WARNING:${NC} CLAUDE.md not found at expected location"
    ((WARNING_ISSUES++))
    ((TOTAL_ISSUES++))
fi

echo ""

# ============================================================================
# CHECK 2: Structure Validation (D12)
# ============================================================================

echo -e "${BLUE}=== Structure Validation (D12) ===${NC}"
echo ""

MISSING_PREREQ=0
MISSING_EXIT=0

required_sections=("Prerequisites" "Exit Criteria" "Overview")

# Known exceptions (documented in audit/reference/known_exceptions.md)
declare -a known_exceptions=(
  # Category C: Optional/auxiliary files (3 files)
  "stages/s3/s3_parallel_work_sync.md"
  "stages/s4/s4_feature_testing_card.md"
  "stages/s4/s4_test_strategy_development.md"
)

# Self-check: warn if any known_exceptions entry no longer exists on disk.
# Stale entries skew the "Known exceptions skipped" count and mislead future maintainers.
STALE_EXCEPTIONS=0
for exception in "${known_exceptions[@]}"; do
  if [ ! -f "$exception" ]; then
    echo -e "${YELLOW}⚠️  STALE EXCEPTION:${NC} '$exception' is listed in known_exceptions but does not exist on disk"
    ((STALE_EXCEPTIONS++))
  fi
done
if [ $STALE_EXCEPTIONS -gt 0 ]; then
  echo -e "${RED}❌ $STALE_EXCEPTIONS stale known_exception(s) found — remove from pre_audit_checks.sh${NC}"
  ((CRITICAL_ISSUES += STALE_EXCEPTIONS))
  ((TOTAL_ISSUES += STALE_EXCEPTIONS))
fi

for file in stages/*/*.md; do
  # Skip known exceptions (documented design patterns)
  skip=false
  for exception in "${known_exceptions[@]}"; do
    if [ "$file" == "$exception" ]; then
      skip=true
      break
    fi
  done

  if [ "$skip" = true ]; then
    continue
  fi

  for section in "${required_sections[@]}"; do
    if ! grep -qi "^## $section\|^### $section" "$file"; then
      echo -e "${RED}❌ MISSING $section:${NC} $file"

      if [ "$section" == "Prerequisites" ]; then
        ((MISSING_PREREQ++))
      elif [ "$section" == "Exit Criteria" ]; then
        ((MISSING_EXIT++))
      fi

      ((CRITICAL_ISSUES++))
      ((TOTAL_ISSUES++))
    fi
  done
done

if [ $MISSING_PREREQ -eq 0 ] && [ $MISSING_EXIT -eq 0 ]; then
  echo -e "${GREEN}✅ All required sections present (excluding 3 known exceptions)${NC}"
fi

echo ""
echo "Missing Prerequisites: $MISSING_PREREQ"
echo "Missing Exit Criteria: $MISSING_EXIT"
echo "Known exceptions skipped: 3 (see audit/reference/known_exceptions.md)"
echo ""

# ============================================================================
# CHECK 3: Documentation Quality (D8)
# ============================================================================

echo -e "${BLUE}=== Documentation Quality (D8) ===${NC}"
echo ""

TODO_COUNT=$(grep -rc "TODO\|TBD\|FIXME" stages templates prompts reference sync 2>/dev/null | grep -v ":0" | wc -l)
PLACEHOLDER_COUNT=$(grep -rc "\[placeholder\]\|\.\.\." stages templates prompts sync 2>/dev/null | grep -v ":0" | wc -l)

if [ "$TODO_COUNT" -gt 0 ]; then
  echo -e "${RED}❌ TODOs found:${NC}"
  grep -rn "TODO\|TBD\|FIXME" stages templates prompts reference sync 2>/dev/null | grep -v ":0" | head -10
  echo ""
  ((CRITICAL_ISSUES += TODO_COUNT))
  ((TOTAL_ISSUES += TODO_COUNT))
else
  echo -e "${GREEN}✅ No TODOs remaining${NC}"
fi

if [ "$PLACEHOLDER_COUNT" -gt 0 ]; then
  echo -e "${YELLOW}⚠️  Placeholders found:${NC}"
  grep -rn "\[placeholder\]" stages templates prompts sync 2>/dev/null | grep -v ":0" | head -10
  echo ""
  ((WARNING_ISSUES += PLACEHOLDER_COUNT))
  ((TOTAL_ISSUES += PLACEHOLDER_COUNT))
else
  echo -e "${GREEN}✅ No placeholders found${NC}"
fi

echo ""
echo "TODOs remaining: $TODO_COUNT"
echo "Placeholders found: $PLACEHOLDER_COUNT"
echo ""

# ============================================================================
# CHECK 4: Content Accuracy - File Counts (D9)
# ============================================================================

echo -e "${BLUE}=== Content Accuracy - File Counts (D9) ===${NC}"
echo ""

# Count actual templates
ACTUAL_TEMPLATES=$(find templates -name "*.md" -o -name "*.txt" | wc -l)

# Check if any files claim different count
CLAIMED_COUNT=$(grep -rn "19 template" stages templates 2>/dev/null | wc -l)

if [ "$CLAIMED_COUNT" -gt 0 ]; then
  echo "Checking template count claims..."
  if [ "$ACTUAL_TEMPLATES" -ne 19 ]; then
    echo -e "${YELLOW}⚠️  Template count mismatch:${NC}"
    echo "   Actual: $ACTUAL_TEMPLATES"
    echo "   Claimed: 19 (in $CLAIMED_COUNT locations)"
    ((WARNING_ISSUES++))
    ((TOTAL_ISSUES++))
  else
    echo -e "${GREEN}✅ Template count accurate: $ACTUAL_TEMPLATES${NC}"
  fi
else
  echo -e "${GREEN}✅ No template count claims to verify${NC}"
fi

echo ""

# ============================================================================
# CHECK 5: Accessibility - TOC for Long Files (D17)
# ============================================================================

echo -e "${BLUE}=== Accessibility - TOC Check (D17) ===${NC}"
echo ""

MISSING_TOC=0

for file in $(find stages reference -name "*.md"); do
  lines=$(wc -l < "$file")

  if [ "$lines" -gt 500 ]; then
    if ! grep -qi "table of contents\|## contents\|## table of contents" "$file"; then
      echo -e "${YELLOW}⚠️  MISSING TOC:${NC} $file ($lines lines)"
      ((MISSING_TOC++))
      ((WARNING_ISSUES++))
      ((TOTAL_ISSUES++))
    fi
  fi
done

if [ $MISSING_TOC -eq 0 ]; then
  echo -e "${GREEN}✅ All long files have TOC${NC}"
fi

echo ""
echo "Large files missing TOC: $MISSING_TOC"
echo ""

# ============================================================================
# CHECK 6: Cross-Reference Quick Check (D1)
# ============================================================================

echo -e "${BLUE}=== Cross-Reference Quick Check (D1) ===${NC}"
echo ""

# Extract and check a sample of file paths
BROKEN_REFS=0

# Check stages/ references
grep -rh "stages/s[0-9].*\.md" stages templates prompts 2>/dev/null | \
  grep -o "stages/s[0-9][^) ]*\.md" | \
  sort -u | head -20 | while read ref; do
    if [ ! -f "$ref" ]; then
      echo -e "${RED}❌ BROKEN REF:${NC} $ref"
      ((BROKEN_REFS++))
    fi
  done

# Note: This is a quick sample check, not exhaustive
# Full D1 validation requires manual audit

if [ $BROKEN_REFS -eq 0 ]; then
  echo -e "${GREEN}✅ Sample file references valid${NC}"
  echo "(Full D1 validation required in manual audit)"
fi

echo ""

# ============================================================================
# CHECK 7: Code Block Language Tags (D17)
# ============================================================================

echo -e "${BLUE}=== Code Block Language Tags (D17) ===${NC}"
echo ""

# NOTE: Do NOT use `grep "^\`\`\`$"` — it matches closing fences (always bare ```),
# producing 100% false positives. This Python approach tracks fence pairs and only
# flags OPENING fences without a language tag.
UNTAGGED_BLOCKS=$(python3 -c "
import glob
count = 0
examples = []
for fname in glob.glob('stages/**/*.md', recursive=True) + \
             glob.glob('templates/**/*.md', recursive=True) + \
             glob.glob('prompts/**/*.md', recursive=True) + \
             glob.glob('reference/**/*.md', recursive=True):
    try:
        in_block = False
        for i, line in enumerate(open(fname), 1):
            s = line.rstrip()
            if not in_block:
                if s == '\`\`\`':
                    count += 1
                    if len(examples) < 5:
                        examples.append(f'{fname}:{i}')
                    in_block = True
                elif s.startswith('\`\`\`') and len(s) > 3:
                    in_block = True
            elif s == '\`\`\`':
                in_block = False
    except: pass
for ex in examples:
    print(f'EXAMPLE:{ex}', flush=True)
print(count)
" 2>/dev/null)

UNTAGGED_EXAMPLES=$(echo "$UNTAGGED_BLOCKS" | grep "^EXAMPLE:" | sed 's/^EXAMPLE://')
UNTAGGED_COUNT=$(echo "$UNTAGGED_BLOCKS" | tail -1)

if [ "${UNTAGGED_COUNT:-0}" -gt 0 ]; then
  echo -e "${YELLOW}⚠️  Opening code blocks without language tags: $UNTAGGED_COUNT${NC}"
  echo "   (First 5 examples:)"
  echo "$UNTAGGED_EXAMPLES" | head -5 | sed 's/^/   /'
  ((WARNING_ISSUES += UNTAGGED_COUNT))
  ((TOTAL_ISSUES += UNTAGGED_COUNT))
else
  echo -e "${GREEN}✅ All code blocks have language tags (opening fences)${NC}"
fi

echo ""

# ============================================================================
# CHECK 8: CLAUDE.md Sync Quick Check (D4)
# ============================================================================

echo -e "${BLUE}=== CLAUDE.md Sync Check (D4) ===${NC}"
echo ""

# Check if CLAUDE.md exists
if [ -f "../../CLAUDE.md" ]; then
  # Quick check for common issues
  STAGE_REFS=$(grep -c "S[0-9]\+:" ../../CLAUDE.md 2>/dev/null || echo "0")

  if [ "$STAGE_REFS" -gt 0 ]; then
    echo -e "${GREEN}✅ CLAUDE.md found with $STAGE_REFS stage references${NC}"
    echo "   (Full D4 validation required in manual audit)"
  else
    echo -e "${YELLOW}⚠️  CLAUDE.md found but no stage references detected${NC}"
    ((WARNING_ISSUES++))
    ((TOTAL_ISSUES++))
  fi
else
  echo -e "${RED}❌ CLAUDE.md not found in expected location${NC}"
  ((CRITICAL_ISSUES++))
  ((TOTAL_ISSUES++))
fi

echo ""

# ============================================================================
# CHECK 9: Workflow Description Consistency (D3, D18)
# ============================================================================

echo -e "${BLUE}=== Workflow Description Consistency (D3, D18) ===${NC}"
echo ""

# Find all workflow sequence claims
echo "Checking workflow sequence claims..."
SEQUENCE_CLAIMS=$(grep -rn "S[0-9].*->.*S[0-9]" stages 2>/dev/null | wc -l)

if [ "$SEQUENCE_CLAIMS" -gt 0 ]; then
  echo "Found $SEQUENCE_CLAIMS workflow sequence claims"
  echo "(First 5 examples:)"
  grep -rn "S[0-9].*->.*S[0-9]" stages 2>/dev/null | head -5
  echo ""
  echo -e "${YELLOW}Review above for contradictions (different stages describing same workflow differently)${NC}"
else
  echo -e "${GREEN}✅ No workflow sequence claims to verify${NC}"
fi

echo ""

# ============================================================================
# CHECK 10: Prerequisite-Content Consistency (D10)
# ============================================================================

echo -e "${BLUE}=== Prerequisite-Content Consistency (D10) ===${NC}"
echo ""

PREREQ_CONFLICTS=0

for file in stages/**/*.md stages/*/*.md; do
  if [ -f "$file" ]; then
    prereq_all=$(grep -A 10 "^## Prerequisites" "$file" 2>/dev/null | grep -i "ALL features\|all.*complete\|every feature")
    content_group=$(grep -i "Round [0-9]:.*Group\|Group [0-9].*only\|per group" "$file" 2>/dev/null)

    if [ -n "$prereq_all" ] && [ -n "$content_group" ]; then
      echo -e "${YELLOW}⚠️  POTENTIAL CONFLICT:${NC} $file"
      echo "   Prerequisites: $(echo $prereq_all | head -c 80)..."
      echo "   Content: $(echo $content_group | head -c 80)..."
      ((PREREQ_CONFLICTS++))
      ((WARNING_ISSUES++))
      ((TOTAL_ISSUES++))
    fi
  fi
done

if [ $PREREQ_CONFLICTS -eq 0 ]; then
  echo -e "${GREEN}✅ No prerequisite-content conflicts detected${NC}"
else
  echo ""
  echo "Found $PREREQ_CONFLICTS potential prerequisite-content conflicts"
fi

echo ""

# ============================================================================
# CHECK 11: Stage Flow Consistency (D18)
# ============================================================================

echo -e "${BLUE}=== Stage Flow Consistency (D18) ===${NC}"
echo ""

echo "Checking S1 parallelization modes vs S2 router handling..."
echo ""

# Check what modes S1 can produce
echo "S1 parallelization modes:"
grep -n "sequential\|parallel\|group" stages/s1/*.md 2>/dev/null | grep -i "mode\|option\|scenario" | head -5

echo ""
echo "S2 router handles:"
grep -n "Sequential\|Parallel\|Group" stages/s2/s2_feature_deep_dive.md 2>/dev/null | head -5

echo ""
echo -e "${YELLOW}Verify all S1 modes are handled in S2 router${NC}"
echo "(Full D18 validation required in manual audit)"

echo ""

# ============================================================================
# CHECK 12: Character and Format Compliance (D14)
# ============================================================================

echo -e "${BLUE}=== Character and Format Compliance (D14) ===${NC}"
echo ""

BANNED_CHAR_FILES=0
REVIEW_CHAR_FILES=0

# Use python3 to scan for banned Unicode characters
# Category A/B: BANNED (checkboxes, curly quotes) -> Critical violation
# Category C: REVIEW (em/en dashes) -> Warning only (acceptable in prose)
# PYTHONUTF8=1: force UTF-8 stdout on Windows (avoid cp1252 encoding errors with emoji/special chars)
PYTHONUTF8=1 python3 - <<'PYEOF'
import os
import sys

# Category A/B: Fully banned — must be replaced
BANNED = {
    '\u25a1': ('□', 'U+25A1 WHITE SQUARE', '- [ ]'),
    '\u2610': ('☐', 'U+2610 BALLOT BOX', '- [ ]'),
    '\u2611': ('☑', 'U+2611 BALLOT BOX WITH CHECK', '- [x]'),
    '\u2612': ('☒', 'U+2612 BALLOT BOX WITH X', '- [x]'),
    '\u201c': ('\u201c', 'U+201C LEFT DOUBLE QUOTE', '"'),
    '\u201d': ('\u201d', 'U+201D RIGHT DOUBLE QUOTE', '"'),
    '\u2018': ('\u2018', 'U+2018 LEFT SINGLE QUOTE', "'"),
    '\u2019': ('\u2019', 'U+2019 RIGHT SINGLE QUOTE', "'"),
}

# Category C: Review — acceptable in prose, flag for human inspection
REVIEW = {
    '\u2013': ('\u2013', 'U+2013 EN DASH', '--'),
    '\u2014': ('\u2014', 'U+2014 EM DASH', '--'),
}

RED = '\033[0;31m'
YELLOW = '\033[1;33m'
GREEN = '\033[0;32m'
NC = '\033[0m'

banned_files = 0
review_files = 0
banned_total = 0
review_total = 0

# Known exceptions: files that intentionally contain banned chars as examples
EXCEPTIONS = {
    './audit/dimensions/d14_character_format_compliance.md',  # D14 guide shows the chars it bans
}

for root, dirs, files in os.walk('.'):
    # Skip hidden dirs and audit/outputs/ (transient historical files)
    dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'outputs']
    for fname in files:
        if not fname.endswith('.md'):
            continue
        fpath = os.path.join(root, fname)
        if fpath.replace('\\', '/') in EXCEPTIONS:
            continue
        try:
            with open(fpath, encoding='utf-8') as f:
                content = f.read()
        except Exception:
            continue

        banned_hits = []
        for char, (display, name, replacement) in BANNED.items():
            count = content.count(char)
            if count > 0:
                banned_hits.append(f"  {count}x {name} -> replace with '{replacement}'")
                banned_total += count

        if banned_hits:
            banned_files += 1
            print(f"{RED}❌ BANNED CHARS:{NC} {fpath}")
            for hit in banned_hits:
                print(hit)

        review_hits = []
        for char, (display, name, replacement) in REVIEW.items():
            count = content.count(char)
            if count > 0:
                review_hits.append(f"  {count}x {name} (review - OK in prose, replace in lists/code)")
                review_total += count

        if review_hits:
            review_files += 1
            print(f"{YELLOW}⚠️  REVIEW CHARS:{NC} {fpath}")
            for hit in review_hits:
                print(hit)

# Also scan extra files outside the guides tree
EXTRA_FILES = ['../../scripts/initialization/RULES_FILE.template.md']
for fpath in EXTRA_FILES:
    if not os.path.isfile(fpath):
        continue
    if fpath in EXCEPTIONS:
        continue
    try:
        with open(fpath, encoding='utf-8') as f:
            content = f.read()
    except Exception:
        continue
    banned_hits = []
    for char, (display, name, replacement) in BANNED.items():
        count = content.count(char)
        if count > 0:
            banned_hits.append(f"  {count}x {name} -> replace with '{replacement}'")
            banned_total += count
    if banned_hits:
        banned_files += 1
        print(f"{RED}❌ BANNED CHARS:{NC} {fpath}")
        for hit in banned_hits:
            print(hit)
    review_hits = []
    for char, (display, name, replacement) in REVIEW.items():
        count = content.count(char)
        if count > 0:
            review_hits.append(f"  {count}x {name} (review - OK in prose, replace in lists/code)")
            review_total += count
    if review_hits:
        review_files += 1
        print(f"{YELLOW}⚠️  REVIEW CHARS:{NC} {fpath}")
        for hit in review_hits:
            print(hit)

if banned_files == 0 and review_files == 0:
    print(f"{GREEN}✅ No banned or review Unicode characters found{NC}")
elif banned_files == 0:
    print(f"{YELLOW}⚠️  No banned chars found, but {review_files} file(s) have review chars (em/en dash){NC}")
    print("Review each occurrence — acceptable in prose, should be replaced in lists/code")
else:
    print(f"\nFiles with banned chars (CRITICAL): {banned_files}")
    print(f"Files with review chars (WARNING): {review_files}")
    print("Fix: See audit/dimensions/d14_character_format_compliance.md for bulk replacement script")
    sys.exit(1)

# Signal review-only to caller
if banned_files == 0 and review_files > 0:
    sys.exit(2)
PYEOF

D18_EXIT=$?
if [ $D18_EXIT -eq 1 ]; then
  ((CRITICAL_ISSUES++))
  ((TOTAL_ISSUES++))
  ((BANNED_CHAR_FILES++))
elif [ $D18_EXIT -eq 2 ]; then
  ((WARNING_ISSUES++))
  ((TOTAL_ISSUES++))
  ((REVIEW_CHAR_FILES++))
fi

echo ""
echo "Files with banned chars (critical): $BANNED_CHAR_FILES"
echo "(See output above for full list of review-level chars)"
echo ""

# ============================================================================
# CHECK 13: Gitignore Completeness (D20 partial)
# ============================================================================

echo -e "${BLUE}=== Gitignore Completeness (D20) ===${NC}"
echo ""

GITIGNORE_FILE="../../.gitignore"
GITIGNORE_ISSUES=0

if [ ! -f "$GITIGNORE_FILE" ]; then
  echo -e "${YELLOW}⚠️  No .gitignore found at project root — cannot verify transient file entries${NC}"
  ((WARNING_ISSUES++))
  ((TOTAL_ISSUES++))
  GITIGNORE_ISSUES=1
else
  if ! grep -qF ".shamt/import_diff" "$GITIGNORE_FILE"; then
    echo -e "${RED}❌ .shamt/import_diff*.md is not in .gitignore${NC}"
    echo "   Add: .shamt/import_diff*.md"
    ((CRITICAL_ISSUES++))
    ((TOTAL_ISSUES++))
    GITIGNORE_ISSUES=1
  fi

  if ! grep -qF ".shamt/shamt_master_path.conf" "$GITIGNORE_FILE"; then
    echo -e "${RED}❌ .shamt/shamt_master_path.conf is not in .gitignore${NC}"
    echo "   Add: .shamt/shamt_master_path.conf"
    ((CRITICAL_ISSUES++))
    ((TOTAL_ISSUES++))
    GITIGNORE_ISSUES=1
  fi

  if ! grep -qF ".shamt/last_sync.conf" "$GITIGNORE_FILE"; then
    echo -e "${RED}❌ .shamt/last_sync.conf is not in .gitignore${NC}"
    echo "   Add: .shamt/last_sync.conf"
    ((CRITICAL_ISSUES++))
    ((TOTAL_ISSUES++))
    GITIGNORE_ISSUES=1
  fi

  if [ $GITIGNORE_ISSUES -eq 0 ]; then
    echo -e "${GREEN}✅ All transient Shamt files are gitignored${NC}"
  fi
fi

echo ""

# ============================================================================
# SUMMARY
# ============================================================================

echo "=================================="
echo "Pre-Audit Summary"
echo "=================================="
echo ""

echo "Total Issues Found: $TOTAL_ISSUES"
echo "  Critical: $CRITICAL_ISSUES"
echo "  Warnings: $WARNING_ISSUES"
echo ""

if [ $TOTAL_ISSUES -eq 0 ]; then
  echo -e "${GREEN}✅ No automated issues found - ready for manual audit${NC}"
  echo ""
  echo "Next steps:"
  echo "1. Read audit/audit_overview.md"
  echo "2. Start Round 1: Read audit/stages/stage_1_discovery.md"
  exit 0
else
  echo -e "${YELLOW}⚠️  Found $TOTAL_ISSUES issues - address before manual audit${NC}"
  echo ""
  echo "Recommended actions:"
  echo "1. Fix critical issues ($CRITICAL_ISSUES found)"
  echo "2. Review warnings ($WARNING_ISSUES found)"
  echo "3. Re-run this script"
  echo "4. Then proceed to manual audit"
  exit 1
fi
