#!/usr/bin/env bash
# =============================================================================
# Shamt Export Script (Bash — Linux / Mac)
# =============================================================================
# Run this script from the root of your child project.
# Usage: bash .shamt/scripts/export/export.sh
#
# Copies all modified shared files (guides/ and scripts/) from this project
# to the local shamt-ai-dev master repo. Open a PR after running.
# =============================================================================

set -e

# --- Parse arguments ---------------------------------------------------------

DRY_RUN=false
for arg in "$@"; do
    case "$arg" in
        --dry-run) DRY_RUN=true ;;
        *) echo "Unknown argument: $arg"; echo "Usage: export.sh [--dry-run]"; exit 1 ;;
    esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CHILD_SHAMT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
CHILD_ROOT="$(cd "$CHILD_SHAMT_DIR/.." && pwd)"

# --- Read master path --------------------------------------------------------

MASTER_PATH_CONF="$CHILD_SHAMT_DIR/shamt_master_path.conf"
if [ ! -f "$MASTER_PATH_CONF" ]; then
    echo ""
    echo "  Error: .shamt/shamt_master_path.conf not found."
    echo "  Run the init script to set up the master path."
    echo ""
    exit 1
fi

MASTER_DIR="$(tr -d '[:space:]' < "$MASTER_PATH_CONF")"
if [ ! -d "$MASTER_DIR" ]; then
    echo ""
    echo "  Error: Master directory not found: $MASTER_DIR"
    echo "  Update .shamt/shamt_master_path.conf with the correct path."
    echo ""
    exit 1
fi

MASTER_SHAMT_DIR="$MASTER_DIR/.shamt"

echo ""
echo "============================================================"
echo "  Shamt Export"
echo "============================================================"
echo "  From: $CHILD_ROOT"
echo "  To:   $MASTER_DIR"
echo "============================================================"
echo ""

# --- Dirty tree check --------------------------------------------------------

if ! git -C "$MASTER_DIR" diff --quiet 2>/dev/null || ! git -C "$MASTER_DIR" diff --cached --quiet 2>/dev/null; then
    echo "  Warning: master working tree has uncommitted changes."
    echo "  Exported files will be mixed with existing changes. Proceed with care."
    echo ""
fi

# --- Compare and copy changed files ------------------------------------------

EXPORTED=()
DELETED=()

export_dir() {
    local source_dir="$1"  # child's guides/ or scripts/
    local master_dir="$2"  # master's guides/ or scripts/
    local rel_prefix="$3"  # e.g. "guides" or "scripts"

    [ -d "$source_dir" ] || return 0

    while IFS= read -r -d '' src_file; do
        local rel_path="${src_file#"$CHILD_SHAMT_DIR/"}"

        # Never export audit outputs — child-specific, not relevant to master
        if [[ "$rel_path" == "guides/audit/outputs/"* ]]; then
            continue
        fi

        local dst_file="$MASTER_SHAMT_DIR/$rel_path"

        if [ ! -f "$dst_file" ]; then
            # New file in child — copy to master
            if [ "$DRY_RUN" = "false" ]; then
                mkdir -p "$(dirname "$dst_file")"
                cp "$src_file" "$dst_file"
            fi
            EXPORTED+=("$rel_path (new)")
        elif ! diff -q "$src_file" "$dst_file" > /dev/null 2>&1; then
            # Files differ — copy to master
            if [ "$DRY_RUN" = "false" ]; then
                cp "$src_file" "$dst_file"
            fi
            EXPORTED+=("$rel_path")
        fi
    done < <(find "$source_dir" -type f -print0 | sort -z)
}

remove_from_master() {
    local master_dir="$1"  # master's guides/ or scripts/

    [ -d "$master_dir" ] || return 0

    while IFS= read -r -d '' master_file; do
        local rel_path="${master_file#"$MASTER_SHAMT_DIR/"}"

        # Never touch audit outputs
        if [[ "$rel_path" == "guides/audit/outputs/"* ]]; then
            continue
        fi

        local child_file="$CHILD_SHAMT_DIR/$rel_path"
        if [ ! -f "$child_file" ]; then
            if [ "$DRY_RUN" = "false" ]; then
                rm "$master_file"
            fi
            DELETED+=("$rel_path")
        fi
    done < <(find "$master_dir" -type f -print0 | sort -z)
}

export_dir "$CHILD_SHAMT_DIR/guides" "$MASTER_SHAMT_DIR/guides" "guides"
export_dir "$CHILD_SHAMT_DIR/scripts" "$MASTER_SHAMT_DIR/scripts" "scripts"
remove_from_master "$MASTER_SHAMT_DIR/guides"
remove_from_master "$MASTER_SHAMT_DIR/scripts"

# --- Summary -----------------------------------------------------------------

if [ ${#EXPORTED[@]} -eq 0 ] && [ ${#DELETED[@]} -eq 0 ]; then
    echo "  No differences found. Child is in sync with master."
    echo ""
    echo "============================================================"
    echo ""
    exit 0
fi

if [ ${#EXPORTED[@]} -gt 0 ]; then
    if [ "$DRY_RUN" = "true" ]; then
        echo "  Would export ${#EXPORTED[@]} file(s) to master:"
    else
        echo "  Exported ${#EXPORTED[@]} file(s) to master:"
    fi
    echo ""
    for f in "${EXPORTED[@]}"; do
        echo "    + $f"
    done
    echo ""
fi

if [ ${#DELETED[@]} -gt 0 ]; then
    if [ "$DRY_RUN" = "true" ]; then
        echo "  Would delete ${#DELETED[@]} file(s) from master (not present in child):"
    else
        echo "  Deleted ${#DELETED[@]} file(s) from master (not present in child):"
    fi
    echo ""
    for f in "${DELETED[@]}"; do
        echo "    - $f"
    done
    echo ""
fi

if [ "$DRY_RUN" = "true" ]; then
    echo "------------------------------------------------------------"
    echo "  DRY RUN — no changes were made to master."
    echo "  Re-run without --dry-run to apply."
    echo ""
    echo "============================================================"
    echo ""
    exit 0
fi

# --- Generate commit message -------------------------------------------------

if [ ${#EXPORTED[@]} -le 3 ] && [ ${#DELETED[@]} -eq 0 ]; then
    NAMES=()
    for f in "${EXPORTED[@]}"; do
        NAMES+=("$(basename "${f% (new)}")")
    done
    JOINED=$(printf '%s, ' "${NAMES[@]}")
    COMMIT_MSG="sync: ${JOINED%, }"
elif [ ${#DELETED[@]} -gt 0 ]; then
    COMMIT_MSG="sync: ${#EXPORTED[@]} file(s) updated, ${#DELETED[@]} deleted"
else
    COMMIT_MSG="sync: ${#EXPORTED[@]} guide/script improvements"
fi

# --- Next steps --------------------------------------------------------------

echo "------------------------------------------------------------"
echo "  Next steps"
echo "------------------------------------------------------------"
echo ""
echo "  1. Go to the shamt-ai-dev directory:"
echo "       cd $MASTER_DIR"
echo ""
echo "  2. Create a new branch and commit:"
echo "       git checkout main"
echo "       git checkout -b feat/child-sync-$(date +%Y%m%d)"
echo "       git add -A .shamt/guides/ .shamt/scripts/"
echo "       git commit -m \"$COMMIT_MSG\""
echo ""
echo "  3. Push and open a PR against main:"
echo "       git push origin feat/child-sync-$(date +%Y%m%d)"
echo ""
if command -v gh &>/dev/null; then
    echo "  gh is available — open the PR directly:"
    echo "       gh pr create --title \"$COMMIT_MSG\" --body \"<paste .shamt/CHANGES.md entries>\""
    echo ""
fi
echo "  Tip: Include content from .shamt/CHANGES.md in the PR description"
echo "  to give reviewers context on what changed and why."
echo ""
echo "============================================================"
echo ""
