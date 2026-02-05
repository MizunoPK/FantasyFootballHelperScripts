# Shell Script Best Practices

**Created:** 2026-01-30 (from KAI-1 lessons)
**Applicability:** Limited - This project is primarily Python-based
**When to use:** Only if creating .sh files for deployment, CI/CD, or automation

---

## Overview

This project is primarily Python-based. These guidelines apply only if you create shell scripts (.sh files) for:
- Deployment automation
- CI/CD pipelines
- Environment setup
- Build processes

For Python code, see `CODING_STANDARDS.md` instead.

---

## Critical Error Handling (MANDATORY)

When creating any shell script, **ALWAYS include at the top:**

```bash
#!/bin/bash
set -e  # Exit immediately if any command fails
set -u  # Exit if undefined variable used
set -o pipefail  # Exit if any command in pipeline fails
```markdown

**Why this matters:**
- **Without `set -e`:** Script continues after failures, reports success incorrectly
- **Without `set -u`:** Undefined variables silently become empty strings
- **Without `set -o pipefail`:** Pipeline failures (cmd1 | cmd2) go undetected

**Historical Context (KAI-1 Feature 01):**
- Shell script created without `set -e`
- Script could continue after command failures
- Reported success even when operations failed
- Caused silent failures and mysterious test failures
- Issue passed through 3 QC rounds undetected
- Caught only during PR review

---

## Example - Incorrect Script (Dangerous)

```bash
#!/bin/bash
# Missing set -e, set -u, set -o pipefail

# Create directory
mkdir /tmp/data

# Copy files (this might fail silently)
cp important_file.txt /tmp/data/

# Deploy (runs even if copy failed!)
./deploy.sh

echo "Success!"  # Prints even if commands failed
```bash

**Problem:**
- If `cp` fails (file missing, no permissions), script continues to `deploy.sh`
- Script reports "Success!" even though critical steps failed
- Downstream processes break mysteriously because files aren't where expected

---

## Example - Correct Script (Safe)

```bash
#!/bin/bash
set -e  # Exit on any failure
set -u  # Exit on undefined variable
set -o pipefail  # Exit if pipeline fails

# Create directory (-p doesn't fail if exists)
mkdir -p /tmp/data

# Verify file exists before copying
if [ ! -f "important_file.txt" ]; then
    echo "ERROR: important_file.txt not found"
    exit 1
fi

# Copy files
cp important_file.txt /tmp/data/

# Deploy (only runs if previous commands succeeded)
./deploy.sh

echo "Success!"  # Only prints if all commands succeeded
```markdown

**Why this is safe:**
- Script exits immediately on any error
- Prevents cascading failures
- "Success!" only prints if everything actually succeeded
- Debugging is easier (failure point is clear)

---

## Verification Checklist

Before committing any shell script:

- [ ] Line 2: `set -e` present
- [ ] Line 3: `set -u` present
- [ ] Line 4: `set -o pipefail` present
- [ ] Critical operations have explicit error checking
- [ ] Success messages only print if all commands succeed
- [ ] Script tested with intentional failures (does it exit correctly?)

---

## Real Example from KAI-1

**Actual Bug (Shell Script Missing `set -e`):**

```bash
#!/bin/bash
# Missing set -e

awslocal s3 mb s3://bucket1
awslocal s3 mb s3://bucket2  # This fails (already exists)
awslocal s3 mb s3://bucket3

echo "All buckets created!"  # Prints even though bucket2 failed
```markdown

**Result:**
- Script reports "All buckets created!"
- But bucket2 creation actually failed silently
- Tests mysteriously fail later because bucket2 doesn't exist
- Debugging is difficult (success message misleading)

**Fix:**

```bash
#!/bin/bash
set -e  # Added this line

awslocal s3 mb s3://bucket1
awslocal s3 mb s3://bucket2  # Script exits HERE if this fails
awslocal s3 mb s3://bucket3

echo "All buckets created!"  # Only prints if all 3 succeeded
```markdown

**Result:**
- Script exits immediately on first failure
- No misleading success message
- Problem is immediately visible
- Debugging is straightforward

---

## Additional Best Practices

### 1. Use Explicit Error Checks for Critical Operations

```bash
#!/bin/bash
set -e

# Download file
if ! curl -o data.json https://api.example.com/data; then
    echo "ERROR: Failed to download data"
    exit 1
fi

# Verify file is not empty
if [ ! -s data.json ]; then
    echo "ERROR: Downloaded file is empty"
    exit 1
fi

echo "Download successful"
```markdown

### 2. Use Safe Directory Creation

```bash
# Good: -p doesn't fail if directory exists
mkdir -p /path/to/directory

# Bad: Fails if directory exists
mkdir /path/to/directory
```markdown

### 3. Quote Variables to Handle Spaces

```bash
# Good: Handles paths with spaces
FILE_PATH="/path with spaces/file.txt"
cp "$FILE_PATH" /destination/

# Bad: Breaks on paths with spaces
cp $FILE_PATH /destination/
```markdown

### 4. Use Descriptive Error Messages

```bash
#!/bin/bash
set -e

if [ ! -f "config.json" ]; then
    echo "ERROR: config.json not found in $(pwd)"
    echo "Expected location: $(pwd)/config.json"
    exit 1
fi
```markdown

---

## Common Mistakes to Avoid

### Mistake 1: Forgetting `set -e`
- **Impact:** Silent failures
- **Fix:** Always add `set -e` on line 2

### Mistake 2: Using Exit 0 After Failures
```bash
# Bad: Masks failures
command_that_might_fail || exit 0

# Good: Let it fail
command_that_might_fail
```markdown

### Mistake 3: Not Testing Failure Scenarios
```bash
# Test your script with intentional failures
# Does it exit correctly?
# Are error messages clear?
```markdown

---

## When to Use Shell Scripts in This Project

**Appropriate use cases:**
- Environment setup scripts
- Deployment automation
- CI/CD pipeline steps
- Build process orchestration
- Database initialization

**Not appropriate:**
- Data processing (use Python)
- Business logic (use Python)
- Complex calculations (use Python)
- Testing (use `python tests/run_all_tests.py`)

**Rule of Thumb:** If logic is more than 20 lines, consider using Python instead.

---

## Integration with CODING_STANDARDS.md

For Python code standards, see `CODING_STANDARDS.md`:
- Error handling (use error_context)
- Logging standards
- Docstring format
- Type hints
- Testing standards

This guide only applies to .sh files (shell scripts).

---

## Quick Reference

**Mandatory first 4 lines of every shell script:**

```bash
#!/bin/bash
set -e          # Exit on error
set -u          # Exit on undefined variable
set -o pipefail # Exit on pipeline failure
```

**Remember:** If you're creating a shell script in this Python project, ask yourself: "Should this be Python instead?"

---

**Last Updated:** 2026-01-30
**Source:** Lessons learned from KAI-1 Feature 01 (external project)
**Applicability:** Limited (Python-heavy project, shell scripts rare)
