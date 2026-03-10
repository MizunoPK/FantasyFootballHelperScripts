#!/usr/bin/env bash
# =============================================================================
# Shamt Import Script (Bash — Linux / Mac)
# =============================================================================
# Run this script from the root of your child project.
# Usage: bash .shamt/scripts/import/import.sh
#
# Syncs guides/ and scripts/ from the master shamt-ai-dev repo into this
# project's .shamt/. Generates a diff file for agent review afterward.
# =============================================================================

set -e

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
echo "  Shamt Import"
echo "============================================================"
echo "  From: $MASTER_DIR"
echo "  To:   $CHILD_ROOT"
echo "============================================================"
echo ""

# --- Freshness check ---------------------------------------------------------

if git -C "$MASTER_DIR" fetch origin main --quiet 2>/dev/null; then
    FRESHNESS_LOCAL=$(git -C "$MASTER_DIR" rev-parse main 2>/dev/null || echo "")
    FRESHNESS_REMOTE=$(git -C "$MASTER_DIR" rev-parse origin/main 2>/dev/null || echo "")
    if [ -n "$FRESHNESS_LOCAL" ] && [ -n "$FRESHNESS_REMOTE" ] && [ "$FRESHNESS_LOCAL" != "$FRESHNESS_REMOTE" ]; then
        echo "  Warning: master repo's 'main' branch appears to be behind origin/main."
        echo "  Consider running 'git pull' in: $MASTER_DIR"
        echo ""
        read -rp "  Proceed anyway? [y/N]: " _proceed
        _proceed="${_proceed:-N}"
        if [[ ! "$_proceed" =~ ^[Yy]$ ]]; then
            echo "  Import cancelled."
            echo ""
            echo "============================================================"
            echo ""
            exit 0
        fi
        echo ""
    fi
else
    echo "  No remote configured or fetch unavailable — skipping freshness check."
    echo ""
fi

# --- Track changes -----------------------------------------------------------

COPIED=()
DELETED=()
DIFF_DIR="$(mktemp -d)"
SECTION_NUM=0

cleanup() {
    rm -rf "$DIFF_DIR"
}
trap cleanup EXIT

write_last_sync() {
    local _sync_date _master_hash
    _sync_date="$(date +%Y-%m-%d)"
    _master_hash="$(git -C "$MASTER_DIR" rev-parse --short HEAD 2>/dev/null || echo "unknown")"
    printf '%s | %s\n' "$_sync_date" "$_master_hash" > "$CHILD_SHAMT_DIR/last_sync.conf"
}

# --- Import from master (copy + track diffs) ---------------------------------

import_dir() {
    local master_dir="$1"  # master's guides/ or scripts/
    local child_dir="$2"   # child's guides/ or scripts/
    local skip_prefix="$3" # subpath to skip (e.g. "guides/audit/outputs")

    [ -d "$master_dir" ] || return 0

    while IFS= read -r -d '' master_file; do
        local rel_path="${master_file#"$MASTER_SHAMT_DIR/"}"

        # Skip excluded subpaths
        if [ -n "$skip_prefix" ] && [[ "$rel_path" == "$skip_prefix"* ]]; then
            continue
        fi

        local child_file="$CHILD_SHAMT_DIR/$rel_path"

        if [ ! -f "$child_file" ]; then
            # New file from master
            mkdir -p "$(dirname "$child_file")"
            cp "$master_file" "$child_file"
            COPIED+=("$rel_path (new)")
        elif ! diff -q "$master_file" "$child_file" > /dev/null 2>&1; then
            # Files differ — record diff then apply
            local section_file
            section_file="$DIFF_DIR/$(printf '%06d' "$SECTION_NUM").md"
            SECTION_NUM=$((SECTION_NUM + 1))
            {
                printf '## %s\n\n' "$rel_path"
                printf '```diff\n'
                diff -u "$child_file" "$master_file" || true
                printf '```\n\n'
                printf -- '---\n\n'
            } > "$section_file"
            cp "$master_file" "$child_file"
            COPIED+=("$rel_path")
        fi
    done < <(find "$master_dir" -type f -print0 | sort -z)
}

import_dir "$MASTER_SHAMT_DIR/guides" "$CHILD_SHAMT_DIR/guides" "guides/audit/outputs"
import_dir "$MASTER_SHAMT_DIR/scripts" "$CHILD_SHAMT_DIR/scripts" ""

# --- Remove files deleted from master ----------------------------------------

remove_deleted() {
    local child_dir="$1"
    local master_dir="$2"
    local skip_prefix="$3"

    [ -d "$child_dir" ] || return 0

    while IFS= read -r -d '' child_file; do
        local rel_path="${child_file#"$CHILD_SHAMT_DIR/"}"

        # Skip excluded subpaths
        if [ -n "$skip_prefix" ] && [[ "$rel_path" == "$skip_prefix"* ]]; then
            continue
        fi

        local master_file="$MASTER_SHAMT_DIR/$rel_path"
        if [ ! -f "$master_file" ]; then
            rm "$child_file"
            DELETED+=("$rel_path")
            # Remove empty parent directories
            local dir
            dir="$(dirname "$child_file")"
            while [ "$dir" != "$CHILD_SHAMT_DIR" ] && [ -d "$dir" ] && [ -z "$(ls -A "$dir")" ]; do
                rmdir "$dir"
                dir="$(dirname "$dir")"
            done
        fi
    done < <(find "$child_dir" -type f -print0 | sort -z)
}

remove_deleted "$CHILD_SHAMT_DIR/guides" "$MASTER_SHAMT_DIR/guides" "guides/audit/outputs"
remove_deleted "$CHILD_SHAMT_DIR/scripts" "$MASTER_SHAMT_DIR/scripts" ""

# Record sync state now — before diff generation and output, so a script
# interruption after syncing still produces an accurate last_sync.conf.
write_last_sync

# --- Write diff file(s) ------------------------------------------------------

DIFF_FILES=()
DIFF_HEADER="# Shamt Import Diff

**Generated:** $(date +%Y-%m-%d)

Files with changes are shown below as unified diffs (child → master).

---

"

if [ "$SECTION_NUM" -gt 0 ]; then
    # Pack sections into chunks of ≤ 1000 lines (split at section boundaries)
    CHUNK_FILE="$DIFF_DIR/chunk_000.tmp"
    printf '%s' "$DIFF_HEADER" > "$CHUNK_FILE"
    CHUNK_LINES=$(wc -l < "$CHUNK_FILE")
    CHUNK_NUM=0

    for section_file in "$DIFF_DIR"/[0-9]*.md; do
        sec_lines=$(wc -l < "$section_file")
        if [ "$CHUNK_LINES" -gt 0 ] && [ $((CHUNK_LINES + sec_lines)) -gt 1000 ]; then
            # Flush current chunk and start a new one
            CHUNK_NUM=$((CHUNK_NUM + 1))
            CHUNK_FILE="$DIFF_DIR/chunk_$(printf '%03d' "$CHUNK_NUM").tmp"
            printf '%s' "$DIFF_HEADER" > "$CHUNK_FILE"
            CHUNK_LINES=$(wc -l < "$CHUNK_FILE")
        fi
        cat "$section_file" >> "$CHUNK_FILE"
        CHUNK_LINES=$((CHUNK_LINES + sec_lines))
    done

    TOTAL_CHUNKS=$((CHUNK_NUM + 1))

    if [ "$TOTAL_CHUNKS" -eq 1 ]; then
        cp "$DIFF_DIR/chunk_000.tmp" "$CHILD_SHAMT_DIR/import_diff.md"
        DIFF_FILES=("import_diff.md")
    else
        for i in $(seq 0 "$CHUNK_NUM"); do
            dest="$CHILD_SHAMT_DIR/import_diff_$((i + 1)).md"
            cp "$DIFF_DIR/chunk_$(printf '%03d' "$i").tmp" "$dest"
            DIFF_FILES+=("import_diff_$((i + 1)).md")
        done
    fi
fi

# --- Summary -----------------------------------------------------------------

if [ ${#COPIED[@]} -eq 0 ] && [ ${#DELETED[@]} -eq 0 ]; then
    write_last_sync
    echo "  Already up to date. No changes from master."
    echo ""
    echo "============================================================"
    echo ""
    exit 0
fi

if [ ${#COPIED[@]} -gt 0 ]; then
    echo "  Updated ${#COPIED[@]} file(s):"
    for f in "${COPIED[@]}"; do
        echo "    + $f"
    done
    echo ""
fi

if [ ${#DELETED[@]} -gt 0 ]; then
    echo "  Removed ${#DELETED[@]} file(s) (deleted from master):"
    for f in "${DELETED[@]}"; do
        echo "    - $f"
    done
    echo ""
fi

# --- Agent prompt ------------------------------------------------------------

echo "------------------------------------------------------------"
echo "  Agent Prompt"
echo "------------------------------------------------------------"
echo ""
echo "Copy and send the following to your AI agent:"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Shamt has been updated from master (guides and/or scripts). To complete the import:"
echo ""
echo "1. Re-read the validation loop protocol before proceeding:"
echo "   \`.shamt/guides/reference/validation_loop_master_protocol.md\`"
echo ""
if [ ${#DIFF_FILES[@]} -eq 0 ]; then
    echo "2. No content diffs to review (only new files or deletions)."
elif [ ${#DIFF_FILES[@]} -eq 1 ]; then
    echo "2. Read the import diff: \`.shamt/${DIFF_FILES[0]}\`"
else
    echo "2. Read the import diffs (split due to size):"
    for f in "${DIFF_FILES[@]}"; do
        echo "     \`.shamt/$f\`"
    done
fi
echo ""
echo "3. For each changed file, check whether your \`project-specific-configs/\`"
echo "   supplements are still accurate and consistent with the new content."
echo ""
echo "4. Check whether any existing pointers in the changed guide files are"
echo "   still accurately placed."
echo ""
echo "5. Check whether any new pointers should be added to the changed files."
echo ""
echo "6. Update any affected project-specific files as needed."
echo ""
echo "7. Run a validation loop until 3 consecutive clean rounds are achieved."
echo ""
echo "8. Delete all import diff files when complete."
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "============================================================"
echo ""
