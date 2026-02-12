# Pattern Library

**Purpose:** Pre-built search patterns organized by category for efficient audit discovery
**Audience:** Agents conducting quality audits
**Last Updated:** 2026-02-06

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [File Path Patterns (D1)](#file-path-patterns-d1)
3. [Notation Patterns (D2)](#notation-patterns-d2)
4. [Stage Reference Patterns (D3)](#stage-reference-patterns-d3)
5. [Count Verification Patterns (D4)](#count-verification-patterns-d4)
6. [Template Patterns (D6)](#template-patterns-d6)
7. [File Size Patterns (D10)](#file-size-patterns-d10)
8. [Documentation Patterns (D13)](#documentation-patterns-d13)
9. [Content Accuracy Patterns (D14)](#content-accuracy-patterns-d14)
10. [Navigation Patterns (D16)](#navigation-patterns-d16)
11. [Workflow Description Patterns (D3, D17)](#workflow-description-patterns-d3-d17)
12. [Contradiction Detection Patterns (D15, D17)](#contradiction-detection-patterns-d15-d17)
13. [Stage Flow Consistency Patterns (D17)](#stage-flow-consistency-patterns-d17)

---

## Quick Start

### How to Use This Library

**Copy-paste patterns directly into your shell:**
```bash
# Navigate to guides_v2 directory first
cd feature-updates/guides_v2/audit

# Then run any pattern from this library
```

**Pattern Categories:**
- **High Frequency:** D1, D2, D13 (use every audit round)
- **Medium Frequency:** D3, D4, D6, D10, D14, D16 (use based on trigger event)
- **Context-Specific:** D7, D9, D11, D12, D15 (use when issues suspected)

**Round-by-Round Strategy:**
- **Round 1:** Use exact patterns (Type 1 from each category)
- **Round 2:** Add variations (Type 2, punctuation, context)
- **Round 3:** Manual reading + spot-checks

---

## File Path Patterns (D1)

### Pattern 1.0: Root-Level Files (CRITICAL - Often Missed)

**Check these files specifically:**
```bash
# Root files contain high-density cross-references
grep -n "stages/s[0-9].*\.md\|templates/.*\.md\|reference/.*\.md" \
  ../README.md ../EPIC_WORKFLOW_USAGE.md ../prompts_reference_v2.md
```

### Pattern 1.1: All File Path References

```bash
# Extract all .md file paths from all guides
grep -rh "stages/s[0-9].*\.md\|templates/.*\.md\|reference/.*\.md\|parallel_work/.*\.md\|debugging/.*\.md\|missed_requirement/.*\.md" \
  --include="*.md" . | \
  grep -o "[a-z_/]*\.md" | \
  sort -u
```

### Pattern 1.2: Validate All Paths Exist

```bash
# Check that all referenced files actually exist
grep -rh "stages/s[0-9].*\.md\|templates/.*\.md\|reference/.*\.md" \
  --include="*.md" . | \
  grep -o "[a-z_/]*\.md" | \
  sort -u | \
  while read path; do
    # Adjust path relative to audit directory
    check_path="../$path"
    [ ! -f "$check_path" ] && echo "BROKEN: $path"
  done
```

### Pattern 1.3: Specific Directory Checks

```bash
# Check stages/ references
grep -rn "stages/s[0-9]" --include="*.md" . | head -20

# Check templates/ references
grep -rn "templates/" --include="*.md" . | head -20

# Check reference/ references
grep -rn "reference/" --include="*.md" . | head -20
```

### Pattern 1.4: Relative Path Validation

```bash
# Find all ../ relative paths
grep -rn "\.\./.*\.md" --include="*.md" . | head -30
```

---

## Notation Patterns (D2)

### Pattern 2.0: Root-Level Files Notation Check

```bash
# Check root files for old notation (HIGH PRIORITY)
cd ..  # Move to guides_v2
grep -n "\bS[0-9][a-z]\b\|Stage [0-9][a-z]" \
  README.md EPIC_WORKFLOW_USAGE.md prompts_reference_v2.md
cd audit  # Return to audit
```

### Pattern 2.1: Old Notation - Basic Forms

```bash
# Old letter suffix notation (S5a, S6a, etc.)
grep -rn "\bS[0-9][a-z]\b" --include="*.md" .

# Old "Stage Xa" format
grep -rn "Stage [0-9][a-z]" --include="*.md" .

# Bare number+letter (5a, 6b, etc.)
grep -rn "\b[0-9][a-z]\b" --include="*.md" . | grep -v "2026\|2025"  # Filter out dates
```

### Pattern 2.2: Old Notation - With Punctuation

```bash
# Colon after old notation (S5a:, S6a:)
grep -rn "S[0-9][a-z]:" --include="*.md" .

# Dash after old notation (S5a-S5b)
grep -rn "S[0-9][a-z]-" --include="*.md" .

# Parentheses around old notation
grep -rn "(S[0-9][a-z])" --include="*.md" .
```

### Pattern 2.3: Old Notation - All Caps

```bash
# STAGE_5a format
grep -rn "STAGE_[0-9][a-z]" --include="*.md" .

# STAGE-5a format
grep -rn "STAGE-[0-9][a-z]" --include="*.md" .
```

### Pattern 2.4: Current Notation Validation

```bash
# Find all S#.P# notation (should be present)
grep -rn "S[0-9]\.[A-Z]" --include="*.md" . | head -20

# Find all S#.P#.I# notation
grep -rn "S[0-9]\.[A-Z][0-9]\.I[0-9]" --include="*.md" . | head -20
```

### Pattern 2.5: Mixed Notation Detection

```bash
# Files using BOTH old and new notation (inconsistency)
for file in $(find . -name "*.md"); do
  old=$(grep -c "S[0-9][a-z]" "$file" 2>/dev/null || echo 0)
  new=$(grep -c "S[0-9]\.[A-Z]" "$file" 2>/dev/null || echo 0)
  if [ $old -gt 0 ] && [ $new -gt 0 ]; then
    echo "MIXED: $file (old=$old, new=$new)"
  fi
done
```

---

## Stage Reference Patterns (D3)

### Pattern 3.1: Prerequisites References

```bash
# Find all prerequisite mentions
grep -rn "Prerequisite\|prerequisite\|Before.*stage\|Requires.*S[0-9]" --include="*.md" .
```

### Pattern 3.2: Next Stage References

```bash
# Find "next stage" references
grep -rn "Next.*stage\|Proceed to.*S[0-9]\|Continue to.*S[0-9]" --include="*.md" .
```

### Pattern 3.3: Stage Transition Words

```bash
# Find workflow transition language
grep -rn "After completing.*S[0-9]\|Before starting.*S[0-9]\|Once.*S[0-9].*complete" --include="*.md" .
```

---

## Count Verification Patterns (D4)

### Pattern 4.1: Explicit Counts

```bash
# Find number claims
grep -rn "[0-9]+ files\|[0-9]+ stages\|[0-9]+ iterations\|[0-9]+ rounds" --include="*.md" .
```

### Pattern 4.2: Dimension Count Claims

```bash
# Should be 17 dimensions
grep -rn "17 dimensions\|all 17\|17 critical" --include="*.md" .

# Check for old counts (if previously different)
grep -rn "14 dimensions\|15 dimensions" --include="*.md" .
```

### Pattern 4.3: Stage Count Claims

```bash
# Should be 10 stages (S1-S10)
grep -rn "10 stages\|S1-S10\|stages 1-10" --include="*.md" .

# Check for old counts (if previously different)
grep -rn "7 stages\|8 stages\|9 stages" --include="*.md" .
```

### Pattern 4.4: Iteration Count Claims

```bash
# S5 has 22 iterations across 3 rounds
grep -rn "22 iterations" --include="*.md" .
```

---

## Template Patterns (D6)

### Pattern 6.1: Template File References

```bash
# Find all template references
grep -rn "template.*\.md\|TEMPLATE\|Template" --include="*.md" . | head -30
```

### Pattern 6.2: Template Synchronization Check

```bash
# List all actual templates
ls -1 ../templates/*.md

# Compare to references in guides
grep -rh "templates/.*\.md" --include="*.md" . | grep -o "templates/[^)]*\.md" | sort -u
```

---

## File Size Patterns (D10)

### Pattern 10.1: Files Exceeding Line Limit

```bash
# CLAUDE.md character count (must be <40,000)
wc -c ../../../CLAUDE.md

# Workflow guides line count (should be <1250)
for file in ../stages/**/*.md; do
  lines=$(wc -l < "$file")
  if [ $lines -gt 1250 ]; then
    echo "⚠️  $file: $lines lines (exceeds 1250)"
  fi
done
```

### Pattern 10.2: Audit System File Sizes

```bash
# Check audit system files
for file in dimensions/*.md stages/*.md reference/*.md; do
  lines=$(wc -l < "$file")
  if [ $lines -gt 1250 ]; then
    echo "⚠️  $file: $lines lines (exceeds 1250)"
  fi
done
```

---

## Documentation Patterns (D13)

### Pattern 13.1: Missing TOC

```bash
# Files without Table of Contents
for file in $(find . -name "*.md"); do
  if ! grep -q "Table of Contents" "$file" 2>/dev/null; then
    lines=$(wc -l < "$file")
    if [ $lines -gt 200 ]; then  # Only flag files >200 lines
      echo "NO TOC: $file ($lines lines)"
    fi
  fi
done
```

### Pattern 13.2: TODO and TBD Markers

```bash
# Find placeholder content
grep -rn "TODO\|TBD\|FIXME\|XXX\|PLACEHOLDER" --include="*.md" .
```

### Pattern 13.3: Coming Soon Markers

```bash
# Find "coming soon" markers
grep -rn "⏳\|COMING SOON\|⏳ COMING SOON" --include="*.md" .
```

### Pattern 13.4: Required Sections

```bash
# Check for standard sections
for section in "Purpose" "Prerequisites" "Exit Criteria" "Table of Contents"; do
  echo "=== Files missing: $section ==="
  for file in stages/*.md; do
    if ! grep -q "$section" "$file" 2>/dev/null; then
      echo "  - $file"
    fi
  done
done
```

---

## Content Accuracy Patterns (D14)

### Pattern 14.1: Duration Claims

```bash
# Find time estimates
grep -rn "[0-9]+ minutes\|[0-9]+ hours\|[0-9]+-[0-9]+ min" --include="*.md" .
```

### Pattern 14.2: Step Number Claims

```bash
# Find step count claims
grep -rn "[0-9]+ steps\|Step [0-9]+\|steps [0-9]+-[0-9]+" --include="*.md" .
```

---

## Navigation Patterns (D16)

### Pattern 16.1: Broken Anchors

```bash
# Find internal link anchors
grep -rn "\[.*\](#[^)]*)" --include="*.md" . | head -30
```

### Pattern 16.2: Missing Links

```bash
# Find "See:" references without links
grep -rn "See:.*[^(]$\|See \`.*\`" --include="*.md" .
```

---

## Pattern Diversity Strategy

### Round 1: Exact Patterns
Use basic patterns from each category:
- 1.1 (all file paths)
- 2.1 (old notation basic)
- 13.2 (TODO markers)
- 10.1 (file sizes)

### Round 2: Variations
Add punctuation and context patterns:
- 1.4 (relative paths)
- 2.2 (notation with punctuation)
- 2.5 (mixed notation)
- 3.1-3.3 (stage transitions)

### Round 3: Manual + Spot Checks
- Random file selection
- Manual section reading
- Cross-reference validation
- Template synchronization checks

---

## Common Combinations

### After Stage Renumbering
```bash
# Run these 5 patterns in sequence
Pattern 1.1  # File paths
Pattern 2.1  # Old notation
Pattern 2.2  # Notation punctuation
Pattern 3.2  # Next stage references
Pattern 4.3  # Stage count claims
```

### After Terminology Changes
```bash
# Run these 4 patterns in sequence
Pattern 2.0  # Root files notation
Pattern 2.1  # Old notation basic
Pattern 2.2  # Notation punctuation
Pattern 2.5  # Mixed notation
```

### After S10.P1 Guide Updates
```bash
# Run these 6 patterns in sequence
Pattern 1.0  # Root files
Pattern 1.1  # All file paths
Pattern 2.0  # Root files notation
Pattern 6.2  # Template sync
Pattern 13.3 # Coming soon markers
Pattern 14.1 # Duration claims
```

---

## Pattern Customization

### Creating Your Own Patterns

**Template:**
```bash
# [Pattern Name] - [What it finds]
grep -rn "[YOUR_REGEX]" --include="*.md" [DIRECTORY]
```

**Tips:**
1. Start broad, refine narrow
2. Test on one file first
3. Use `head -N` to limit output
4. Combine with `wc -l` for counts
5. Pipe to file for large result sets

**Example Evolution:**
```bash
# Too broad - finds everything
grep -rn "stage" --include="*.md" .

# Better - specific pattern
grep -rn "\bstage [0-9]\b" --include="*.md" .

# Best - with context
grep -rn -i "next.*stage [0-9]" --include="*.md" .
```

---

---

## Workflow Description Patterns (D3, D17)

### Pattern W1: Stage Sequence Descriptions

```bash
# Find text describing stage sequences
grep -rn "S[0-9].*->.*S[0-9]\|S[0-9].*then.*S[0-9]" --include="*.md" ../stages/

# Find cycle/loop descriptions
grep -rn "complete.*cycle\|cycle.*complete" --include="*.md" ../stages/
```

### Pattern W2: Group Workflow Descriptions

```bash
# Find text about when groups matter
grep -rn "group.*complete\|group.*S[0-9]\|S[0-9].*group" --include="*.md" ../stages/

# Find parallel work descriptions
grep -rn "parallel.*S[0-9]\|S[0-9].*parallel\|wave" --include="*.md" ../stages/
```

### Pattern W3: Scope Descriptions

```bash
# Find scope language
grep -rn "epic.level\|feature.level\|group.level\|all features\|per feature" --include="*.md" ../stages/

# Find scope transitions
grep -rn "proceed to.*level\|transition to.*level" --include="*.md" ../stages/
```

### Pattern W4: Cross-Stage Comparison

```bash
# Extract workflow claims for comparison
for stage in {1..10}; do
  echo "=== S$stage workflow claims ==="
  grep -n "group\|parallel\|scope\|level" ../stages/s$stage/*.md | head -10
done
```

---

## Contradiction Detection Patterns (D15, D17)

### Pattern C1: Find Contradictory Keywords

```bash
# Find "ALL" claims
grep -rn "ALL features\|all.*complete\|every feature" --include="*.md" ../stages/

# Find "per group" claims
grep -rn "Group [0-9]\|per group\|Round [0-9]:.*Group" --include="*.md" ../stages/

# If both exist for same topic -> potential contradiction
```

### Pattern C2: Prerequisite-Content Conflicts

```bash
# For each file, check prerequisite scope vs content scope
for file in ../stages/**/*.md; do
  prereq=$(grep -A 10 "^## Prerequisites" "$file" 2>/dev/null | grep -i "ALL\|every\|all features")
  content=$(grep -i "Round [0-9]:.*Group\|Group [0-9].*only\|per group" "$file" 2>/dev/null)

  if [ -n "$prereq" ] && [ -n "$content" ]; then
    echo "POTENTIAL CONFLICT: $file"
  fi
done
```

### Pattern C3: Stage Transition Consistency

```bash
# Compare exit descriptions with entry prerequisites
for stage in {1..9}; do
  echo "=== S$stage -> S$((stage+1)) ==="
  echo "S$stage exit:"
  grep -A 5 "^## Next" ../stages/s$stage/*.md | head -5
  echo "S$((stage+1)) entry:"
  grep -A 5 "^## Prerequisites" ../stages/s$((stage+1))/*.md | head -5
done
```

---

## Stage Flow Consistency Patterns (D17)

### Pattern D17.1: Handoff Promise Validation

```bash
# Extract what Stage N promises
grep -A 15 "^## Next Stage\|^## Outputs\|^## Exit Criteria" ../stages/sN/*.md

# Extract what Stage N+1 expects
grep -A 15 "^## Prerequisites\|^## Inputs\|^## Entry" ../stages/s(N+1)/*.md
```

### Pattern D17.2: Workflow Behavior Alignment

```bash
# Extract workflow descriptions from all stages
grep -rn "proceed\|after.*complete\|when.*done\|workflow" --include="*.md" ../stages/

# Compare: Do connected stages describe same workflow?
```

### Pattern D17.3: Conditional Logic Coverage

```bash
# Find all conditional logic
grep -rn "if\|when\|scenario\|mode\|option" --include="*.md" ../stages/

# Check S1 modes vs S2 router handling
echo "=== S1 parallelization modes ==="
grep -n "sequential\|parallel\|group" ../stages/s1/*.md | grep -i "mode\|option\|scenario"

echo "=== S2 router handling ==="
grep -n "Sequential\|Parallel\|Group" ../stages/s2/s2_feature_deep_dive.md
```

### Pattern D17.4: Scope Alignment Validation

```bash
# Check scope at each stage exit
for stage in {1..9}; do
  echo "=== S$stage exit scope ==="
  grep -n "proceed.*S$((stage+1))\|epic.level\|feature.level\|all features" ../stages/s$stage/*.md | head -3
done
```

---

## See Also

- **Dimension Guides:** `dimensions/d*.md` - Detailed validation for each dimension
- **Verification Commands:** `reference/verification_commands.md` - Post-fix validation
- **Stage 1 Discovery:** `stages/stage_1_discovery.md` - How to use patterns in discovery phase
