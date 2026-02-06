#!/bin/bash
# Pre-Audit Automated Checks
# Runs before manual audit to catch common structural issues
#
# Coverage: 7 of 16 dimensions (D1, D8, D10, D11, D13, D14, D16)
# Estimated: 40-50% of typical issues (based on KAI-7 Round 1-2 data)
# NOT Checked: D2 (Terminology - requires pattern-specific search, see dimension guide)
#
# Last Updated: 2026-02-05 (Round 3 audit)
# Changes:
#   - Simplified file size threshold from 3-tier (600/800/1000) to 1000-line baseline
#   - Added 17 known exceptions for Prerequisites/Exit Criteria checks
#   - Exceptions documented in audit/reference/known_exceptions.md

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
# CHECK 1: File Size Assessment (D10)
# ============================================================================

echo -e "${BLUE}=== File Size Assessment (D10) ===${NC}"
echo ""

TOO_LARGE=0
LARGE=0

for file in $(find stages -name "*.md"); do
  lines=$(wc -l < "$file")

  if [ "$lines" -gt 1000 ]; then
    echo -e "${RED}❌ TOO LARGE:${NC} $file ($lines lines) - exceeds 1000-line baseline"
    ((TOO_LARGE++))
    ((CRITICAL_ISSUES++))
    ((TOTAL_ISSUES++))
  fi
done

if [ $TOO_LARGE -eq 0 ]; then
  echo -e "${GREEN}✅ All files within 1000-line baseline${NC}"
fi

echo ""
echo "Files >1000 lines: $TOO_LARGE"
echo ""
echo "Note: Files ≤1000 lines are acceptable if content is non-duplicated."
echo "      Updated policy (2026-02-05): Simplified from 3-tier to single 1000-line baseline."
echo ""

# ============================================================================
# CHECK 1b: Policy Compliance - CLAUDE.md Character Limit (D10)
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
# CHECK 2: Structure Validation (D11)
# ============================================================================

echo -e "${BLUE}=== Structure Validation (D11) ===${NC}"
echo ""

MISSING_PREREQ=0
MISSING_EXIT=0

required_sections=("Prerequisites" "Exit Criteria" "Overview")

# Known exceptions (documented in audit/reference/known_exceptions.md)
# Category A: S5 iteration files (14 files)
declare -a known_exceptions=(
  "stages/s5/s5_p1_i3_integration.md"
  "stages/s5/s5_p1_i3_iter5_dataflow.md"
  "stages/s5/s5_p1_i3_iter5a_downstream.md"
  "stages/s5/s5_p1_i3_iter6_errorhandling.md"
  "stages/s5/s5_p1_i3_iter6a_dependencies.md"
  "stages/s5/s5_p1_i3_iter7_integration.md"
  "stages/s5/s5_p1_i3_iter7a_compatibility.md"
  "stages/s5/s5_p3_i1_preparation.md"
  "stages/s5/s5_p3_i1_iter17_phasing.md"
  "stages/s5/s5_p3_i1_iter18_rollback.md"
  "stages/s5/s5_p3_i1_iter19_traceability.md"
  "stages/s5/s5_p3_i1_iter20_performance.md"
  "stages/s5/s5_p3_i1_iter21_mockaudit.md"
  "stages/s5/s5_p3_i1_iter22_consumers.md"
  # Category B: Optional/auxiliary files (3 files)
  "stages/s3/s3_parallel_work_sync.md"
  "stages/s4/s4_feature_testing_card.md"
  "stages/s4/s4_test_strategy_development.md"
)

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
  echo -e "${GREEN}✅ All required sections present (excluding 17 known exceptions)${NC}"
fi

echo ""
echo "Missing Prerequisites: $MISSING_PREREQ"
echo "Missing Exit Criteria: $MISSING_EXIT"
echo "Known exceptions skipped: 17 (see audit/reference/known_exceptions.md)"
echo ""

# ============================================================================
# CHECK 3: Documentation Quality (D13)
# ============================================================================

echo -e "${BLUE}=== Documentation Quality (D13) ===${NC}"
echo ""

TODO_COUNT=$(grep -rc "TODO\|TBD\|FIXME" stages templates prompts reference 2>/dev/null | grep -v ":0" | wc -l)
PLACEHOLDER_COUNT=$(grep -rc "\[placeholder\]\|\.\.\." stages templates prompts 2>/dev/null | grep -v ":0" | wc -l)

if [ "$TODO_COUNT" -gt 0 ]; then
  echo -e "${RED}❌ TODOs found:${NC}"
  grep -rn "TODO\|TBD\|FIXME" stages templates prompts reference 2>/dev/null | grep -v ":0" | head -10
  echo ""
  ((CRITICAL_ISSUES += TODO_COUNT))
  ((TOTAL_ISSUES += TODO_COUNT))
else
  echo -e "${GREEN}✅ No TODOs remaining${NC}"
fi

if [ "$PLACEHOLDER_COUNT" -gt 0 ]; then
  echo -e "${YELLOW}⚠️  Placeholders found:${NC}"
  grep -rn "\[placeholder\]" stages templates prompts 2>/dev/null | grep -v ":0" | head -10
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
# CHECK 4: Content Accuracy - File Counts (D14)
# ============================================================================

echo -e "${BLUE}=== Content Accuracy - File Counts (D14) ===${NC}"
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
# CHECK 5: Accessibility - TOC for Long Files (D16)
# ============================================================================

echo -e "${BLUE}=== Accessibility - TOC Check (D16) ===${NC}"
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
# CHECK 7: Code Block Language Tags (D16)
# ============================================================================

echo -e "${BLUE}=== Code Block Language Tags (D16) ===${NC}"
echo ""

UNTAGGED_BLOCKS=$(grep -rn "^\`\`\`$" stages templates prompts 2>/dev/null | wc -l)

if [ "$UNTAGGED_BLOCKS" -gt 0 ]; then
  echo -e "${YELLOW}⚠️  Code blocks without language tags: $UNTAGGED_BLOCKS${NC}"
  echo "   (First 5 examples:)"
  grep -rn "^\`\`\`$" stages templates prompts 2>/dev/null | head -5
  ((WARNING_ISSUES += UNTAGGED_BLOCKS))
  ((TOTAL_ISSUES += UNTAGGED_BLOCKS))
else
  echo -e "${GREEN}✅ All code blocks have language tags${NC}"
fi

echo ""

# ============================================================================
# CHECK 8: CLAUDE.md Sync Quick Check (D8)
# ============================================================================

echo -e "${BLUE}=== CLAUDE.md Sync Check (D8) ===${NC}"
echo ""

# Check if CLAUDE.md exists
if [ -f "../../CLAUDE.md" ]; then
  # Quick check for common issues
  STAGE_REFS=$(grep -c "S[0-9]\+:" ../../CLAUDE.md 2>/dev/null || echo "0")

  if [ "$STAGE_REFS" -gt 0 ]; then
    echo -e "${GREEN}✅ CLAUDE.md found with $STAGE_REFS stage references${NC}"
    echo "   (Full D8 validation required in manual audit)"
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
