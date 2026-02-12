#!/bin/bash
# Parallel S2 Structure Validation Script
#
# Purpose: Validates coordination infrastructure for parallel S2 work
# Usage: bash validate_structure.sh [epic_path]
# Exit: 0 if valid, 1 if errors found

set -uo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

EPIC_PATH="${1:-.}"
ERRORS=0
WARNINGS=0

echo "=================================================="
echo "Parallel S2 Structure Validation"
echo "=================================================="
echo "Epic Path: $EPIC_PATH"
echo ""

# Function to report errors
error() {
    echo -e "${RED}❌ ERROR:${NC} $1"
    ((ERRORS++))
}

# Function to report warnings
warning() {
    echo -e "${YELLOW}⚠️  WARNING:${NC} $1"
    ((WARNINGS++))
}

# Function to report success
success() {
    echo -e "${GREEN}✅${NC} $1"
}

# Check if epic path exists
if [ ! -d "$EPIC_PATH" ]; then
    error "Epic path does not exist: $EPIC_PATH"
    exit 1
fi

echo "📁 Checking Required Directories..."
echo "--------------------------------------------------"

# Check required directories exist
REQUIRED_DIRS=(".epic_locks" "agent_comms" "agent_checkpoints")
for dir in "${REQUIRED_DIRS[@]}"; do
    if [ ! -d "$EPIC_PATH/$dir" ]; then
        error "Missing required directory: $dir"
    else
        success "Required directory exists: $dir"
    fi
done

echo ""
echo "🚫 Checking Prohibited Directories..."
echo "--------------------------------------------------"

# Check prohibited directories don't exist
PROHIBITED_DIRS=(
    "parallel_work"
    "coordination"
    "agent_comms/inboxes"
    "agent_comms/agent_checkpoints"
    "agent_comms/coordination"
    "agent_comms/parallel_work"
)

for dir in "${PROHIBITED_DIRS[@]}"; do
    if [ -d "$EPIC_PATH/$dir" ]; then
        error "Prohibited directory found: $dir (should not exist)"
    else
        success "Prohibited directory absent: $dir"
    fi
done

echo ""
echo "📄 Checking Checkpoint Files..."
echo "--------------------------------------------------"

# Check checkpoint files are .json
if [ -d "$EPIC_PATH/agent_checkpoints" ]; then
    CHECKPOINT_COUNT=0
    for file in "$EPIC_PATH"/agent_checkpoints/*; do
        # Skip if no files found (glob didn't match)
        [ -e "$file" ] || continue

        CHECKPOINT_COUNT=$((CHECKPOINT_COUNT + 1))
        filename=$(basename "$file")

        if [[ ! "$file" =~ \.json$ ]]; then
            error "Checkpoint file not .json format: $filename (must use .json extension)"
        else
            success "Valid checkpoint file: $filename"
        fi

        # Check naming convention
        if [[ ! "$filename" =~ ^(primary|secondary_[a-z]+)\.json$ ]]; then
            warning "Checkpoint filename doesn't follow convention: $filename (expected: primary.json or secondary_a.json)"
        fi
    done

    if [ $CHECKPOINT_COUNT -eq 0 ]; then
        warning "No checkpoint files found in agent_checkpoints/"
    else
        success "Found $CHECKPOINT_COUNT checkpoint file(s)"
    fi
else
    error "agent_checkpoints/ directory does not exist"
fi

echo ""
echo "💬 Checking Communication Files..."
echo "--------------------------------------------------"

# Check agent_comms has only .md files (no subdirs)
if [ -d "$EPIC_PATH/agent_comms" ]; then
    COMM_FILE_COUNT=0
    COMM_DIR_COUNT=0

    for item in "$EPIC_PATH"/agent_comms/*; do
        # Skip if no items found
        [ -e "$item" ] || continue

        if [ -d "$item" ]; then
            COMM_DIR_COUNT=$((COMM_DIR_COUNT + 1))
            error "Subdirectory in agent_comms/: $(basename "$item") (only .md files allowed)"
        elif [ -f "$item" ]; then
            COMM_FILE_COUNT=$((COMM_FILE_COUNT + 1))
            filename=$(basename "$item")

            if [[ ! "$filename" =~ \.md$ ]]; then
                error "Non-.md file in agent_comms/: $filename (communication files must use .md extension)"
            else
                # Check naming convention for communication files
                if [[ "$filename" =~ ^(primary_to_secondary_[a-z]+|secondary_[a-z]+_to_primary)\.md$ ]]; then
                    success "Valid communication file: $filename"
                else
                    warning "Communication file doesn't follow convention: $filename"
                fi
            fi
        fi
    done

    if [ $COMM_DIR_COUNT -eq 0 ]; then
        success "No subdirectories in agent_comms/ (correct)"
    fi

    if [ $COMM_FILE_COUNT -eq 0 ]; then
        warning "No communication files found in agent_comms/"
    else
        success "Found $COMM_FILE_COUNT communication file(s)"
    fi
else
    error "agent_comms/ directory does not exist"
fi

echo ""
echo "📋 Checking Feature STATUS Files..."
echo "--------------------------------------------------"

# Check all features have STATUS
FEATURE_COUNT=0
MISSING_STATUS_COUNT=0

for feature in "$EPIC_PATH"/feature_*; do
    # Skip if no features found
    [ -d "$feature" ] || continue

    FEATURE_COUNT=$((FEATURE_COUNT + 1))
    feature_name=$(basename "$feature")

    if [ ! -f "$feature/STATUS" ]; then
        error "Missing STATUS file: $feature_name/STATUS"
        MISSING_STATUS_COUNT=$((MISSING_STATUS_COUNT + 1))
    else
        success "STATUS file exists: $feature_name/STATUS"

        # Validate STATUS file format (key-value pairs)
        # Required fields: STAGE, PHASE, AGENT, UPDATED, STATUS, BLOCKERS, READY_FOR_SYNC
        REQUIRED_FIELDS=("STAGE" "PHASE" "AGENT" "UPDATED" "STATUS" "BLOCKERS" "READY_FOR_SYNC")

        for field in "${REQUIRED_FIELDS[@]}"; do
            if ! grep -q "^$field:" "$feature/STATUS" 2>/dev/null; then
                warning "STATUS file missing required field: $feature_name/STATUS ($field:)"
            fi
        done

        # Check format is key-value (contains colons)
        if ! grep -q ":" "$feature/STATUS" 2>/dev/null; then
            error "STATUS file not in key-value format: $feature_name/STATUS (expected KEY: value)"
        fi
    fi
done

if [ $FEATURE_COUNT -eq 0 ]; then
    warning "No feature folders found (feature_*)"
else
    success "Found $FEATURE_COUNT feature folder(s)"
    if [ $MISSING_STATUS_COUNT -eq 0 ]; then
        success "All features have STATUS files"
    fi
fi

echo ""
echo "🔒 Checking Lock Files..."
echo "--------------------------------------------------"

# Check lock files structure
if [ -d "$EPIC_PATH/.epic_locks" ]; then
    LOCK_COUNT=0
    for lock in "$EPIC_PATH"/.epic_locks/*; do
        [ -e "$lock" ] || continue
        LOCK_COUNT=$((LOCK_COUNT + 1))

        lock_name=$(basename "$lock")
        if [[ "$lock_name" =~ \.lock$ ]]; then
            success "Valid lock file: $lock_name"
        else
            warning "Lock file missing .lock extension: $lock_name"
        fi
    done

    if [ $LOCK_COUNT -eq 0 ]; then
        success "No active locks (clean state)"
    else
        warning "Found $LOCK_COUNT lock file(s) (check if stale)"
    fi
fi

echo ""
echo "=================================================="
echo "Validation Summary"
echo "=================================================="

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}✅ PASSED${NC} - Parallel S2 structure is valid"
    echo ""
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW}⚠️  PASSED WITH WARNINGS${NC}"
    echo "Errors: 0"
    echo "Warnings: $WARNINGS"
    echo ""
    echo "Structure is functional but has style/convention issues."
    exit 0
else
    echo -e "${RED}❌ FAILED${NC}"
    echo "Errors: $ERRORS"
    echo "Warnings: $WARNINGS"
    echo ""
    echo "Structure has critical issues that must be fixed."
    echo ""
    echo "See analysis: feature-updates/KAI-8-logging_refactoring/research/"
    echo "             PARALLEL_S2_STRUCTURE_INCONSISTENCY_ANALYSIS.md"
    exit 1
fi
