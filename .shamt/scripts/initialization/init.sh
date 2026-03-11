#!/usr/bin/env bash
# =============================================================================
# Shamt Initialization Script (Bash — Linux / Mac)
# =============================================================================
# Run this script from the root of the project you want to initialize Shamt in.
# Usage: bash /path/to/shamt-ai-dev/.shamt/scripts/initialization/init.sh
# =============================================================================

set -e

SHAMT_SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
TARGET_DIR="$(pwd)"
SHAMT_DIR="$TARGET_DIR/.shamt"

echo ""
echo "============================================================"
echo "  Shamt Initialization"
echo "============================================================"
echo "  Source: $SHAMT_SOURCE_DIR"
echo "  Target: $TARGET_DIR"
echo "============================================================"
echo ""

# --- Helpers -----------------------------------------------------------------

prompt() {
    local question="$1"
    local default="$2"
    local answer
    if [ -n "$default" ]; then
        read -rp "$question [$default]: " answer
        echo "${answer:-$default}"
    else
        read -rp "$question: " answer
        echo "$answer"
    fi
}

prompt_required() {
    local question="$1"
    local answer=""
    while [ -z "$answer" ]; do
        read -rp "$question: " answer
        if [ -z "$answer" ]; then
            echo "  (This field is required)" >&2
        fi
    done
    echo "$answer"
}

separator() {
    echo ""
    echo "------------------------------------------------------------"
    echo "  $1"
    echo "------------------------------------------------------------"
}

# --- AI Service Selection ----------------------------------------------------

separator "AI Service"
echo "Which AI coding assistant will you use with this project?"
echo ""
echo "  1) Claude Code (Anthropic)       → CLAUDE.md at project root"
echo "  2) GitHub Copilot                → .github/copilot-instructions.md"
echo "  3) Cursor                        → .cursorrules at project root"
echo "  4) Windsurf (Codeium)            → .windsurfrules at project root"
echo "  5) Amazon Q Developer            → (setup TBD)"
echo "  6) Other                         → you will specify"
echo ""
read -rp "Enter choice [1]: " ai_choice
ai_choice="${ai_choice:-1}"

case "$ai_choice" in
    1)
        AI_SERVICE="claude_code"
        RULES_FILE_NAME="CLAUDE.md"
        RULES_FILE_DIR="$TARGET_DIR"
        ;;
    2)
        AI_SERVICE="github_copilot"
        RULES_FILE_NAME="copilot-instructions.md"
        RULES_FILE_DIR="$TARGET_DIR/.github"
        ;;
    3)
        AI_SERVICE="cursor"
        RULES_FILE_NAME=".cursorrules"
        RULES_FILE_DIR="$TARGET_DIR"
        ;;
    4)
        AI_SERVICE="windsurf"
        RULES_FILE_NAME=".windsurfrules"
        RULES_FILE_DIR="$TARGET_DIR"
        ;;
    5)
        AI_SERVICE="amazon_q"
        RULES_FILE_NAME="TBD"
        RULES_FILE_DIR="$TARGET_DIR"
        echo ""
        echo "  ⚠  Amazon Q rules file convention is not yet confirmed."
        echo "  The agent will help you determine the correct setup."
        ;;
    6)
        AI_SERVICE="other"
        echo ""
        RULES_FILE_NAME=$(prompt_required "  Rules file name (e.g. .myrules)")
        RULES_FILE_LOCATION=$(prompt "  Rules file location relative to project root" ".")
        if [ "$RULES_FILE_LOCATION" = "." ]; then
            RULES_FILE_DIR="$TARGET_DIR"
        else
            RULES_FILE_DIR="$TARGET_DIR/$RULES_FILE_LOCATION"
        fi
        ;;
    *)
        echo "Invalid choice. Defaulting to Claude Code."
        AI_SERVICE="claude_code"
        RULES_FILE_NAME="CLAUDE.md"
        RULES_FILE_DIR="$TARGET_DIR"
        ;;
esac

echo "  ✓ AI service: $AI_SERVICE"

# --- Project Details ---------------------------------------------------------

separator "Project Details"

PROJECT_NAME=$(prompt_required "  Project name")
EPIC_TAG=$(prompt "  Epic tag (identifier for epics, e.g. SHAMT, MYPROJ)" "SHAMT")
EPIC_TAG=$(echo "$EPIC_TAG" | tr '[:lower:]' '[:upper:]')
SHAMT_NAME=$(prompt "  Agent name (your version of Shamt)" "Shamt")
STARTING_EPIC=$(prompt "  Starting epic number" "1")

# --- Git Configuration -------------------------------------------------------

separator "Git Configuration"

echo "Which git platform will you use?"
echo "  1) GitHub"
echo "  2) GitLab"
echo "  3) Other / none"
read -rp "Enter choice [1]: " git_choice
git_choice="${git_choice:-1}"

case "$git_choice" in
    2)  GIT_PLATFORM="gitlab" ;;
    3)  GIT_PLATFORM="other" ;;
    *)  GIT_PLATFORM="github" ;;
esac

DEFAULT_BRANCH=$(prompt "  Default/main branch name" "main")

echo "  ✓ Git platform: $GIT_PLATFORM"
echo "  ✓ Default branch: $DEFAULT_BRANCH"

# --- Repository Configuration ------------------------------------------------

separator "Repository Configuration"

echo "  Should .shamt/ and the rules file be gitignored in this project?"
echo "  Choose 'yes' for solo/local-only tooling, 'no' to track them in the repo."
echo ""
read -rp "  Gitignore .shamt/ and rules file? [y/N]: " gitignore_choice
gitignore_choice="${gitignore_choice:-N}"
if [[ "$gitignore_choice" =~ ^[Yy]$ ]]; then
    GITIGNORE_SHAMT="true"
else
    GITIGNORE_SHAMT="false"
fi

echo "  ✓ Gitignore .shamt/ and rules file: $GITIGNORE_SHAMT"

# --- Confirmation ------------------------------------------------------------

separator "Review"
echo "  Project name:          $PROJECT_NAME"
echo "  Epic tag:              $EPIC_TAG"
echo "  Agent name:            $SHAMT_NAME"
echo "  Starting epic #:       $STARTING_EPIC"
echo "  AI service:            $AI_SERVICE"
echo "  Rules file:            $RULES_FILE_NAME"
echo "  Rules file path:       $RULES_FILE_DIR/"
echo "  Git platform:          $GIT_PLATFORM"
echo "  Default branch:        $DEFAULT_BRANCH"
echo "  Gitignore .shamt/:     $GITIGNORE_SHAMT"
echo "  Epic directory:        .shamt/epics/"
echo ""
read -rp "Proceed with initialization? [Y/n]: " confirm
confirm="${confirm:-Y}"
if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
    echo "Initialization cancelled."
    exit 0
fi

# --- Create Folder Structure -------------------------------------------------

separator "Creating folder structure"

mkdir -p "$SHAMT_DIR/guides"
mkdir -p "$SHAMT_DIR/scripts"
mkdir -p "$SHAMT_DIR/project-specific-configs"
mkdir -p "$SHAMT_DIR/epics/requests"
mkdir -p "$SHAMT_DIR/epics/done"
mkdir -p "$RULES_FILE_DIR"

echo "  ✓ .shamt/ structure created"

# --- Write Config Files ------------------------------------------------------

separator "Writing config files"

echo "$SHAMT_SOURCE_DIR" > "$SHAMT_DIR/shamt_master_path.conf"
echo "  ✓ Master path written to .shamt/shamt_master_path.conf"

echo "$RULES_FILE_DIR/$RULES_FILE_NAME" > "$SHAMT_DIR/rules_file_path.conf"
echo "  ✓ Rules file path written to .shamt/rules_file_path.conf"

_sync_date="$(date +%Y-%m-%d)"
_master_hash="$(git -C "$SHAMT_SOURCE_DIR" rev-parse --short HEAD 2>/dev/null || echo "unknown")"
printf '%s | %s\n' "$_sync_date" "$_master_hash" > "$SHAMT_DIR/last_sync.conf"
echo "  ✓ Sync state written to .shamt/last_sync.conf"

# --- Configure .gitignore ----------------------------------------------------

separator "Configuring .gitignore"

GITIGNORE_FILE="$TARGET_DIR/.gitignore"

# Always add *.conf wildcard (covers shamt_master_path.conf, last_sync.conf, rules_file_path.conf, etc.)
if [ -f "$GITIGNORE_FILE" ]; then
    if ! grep -qF ".shamt/*.conf" "$GITIGNORE_FILE"; then
        echo ".shamt/*.conf" >> "$GITIGNORE_FILE"
    fi
else
    echo ".shamt/*.conf" > "$GITIGNORE_FILE"
fi
echo "  ✓ .shamt/*.conf added to .gitignore (always)"

# Always add import_diff*.md (transient diff files — never commit)
if ! grep -qF ".shamt/import_diff" "$GITIGNORE_FILE"; then
    echo ".shamt/import_diff*.md" >> "$GITIGNORE_FILE"
fi
echo "  ✓ .shamt/import_diff*.md added to .gitignore (always)"

# Optionally gitignore .shamt/ and rules file
if [ "$GITIGNORE_SHAMT" = "true" ]; then
    if ! grep -qF ".shamt/" "$GITIGNORE_FILE"; then
        echo ".shamt/" >> "$GITIGNORE_FILE"
    fi
    if [ "$RULES_FILE_DIR" = "$TARGET_DIR" ]; then
        RULES_GITIGNORE_PATH="$RULES_FILE_NAME"
    else
        RULES_GITIGNORE_PATH="${RULES_FILE_DIR#"$TARGET_DIR"/}/$RULES_FILE_NAME"
    fi
    if ! grep -qF "$RULES_GITIGNORE_PATH" "$GITIGNORE_FILE"; then
        echo "$RULES_GITIGNORE_PATH" >> "$GITIGNORE_FILE"
    fi
    echo "  ✓ .shamt/ and $RULES_GITIGNORE_PATH added to .gitignore"
fi

# --- Copy Guides -------------------------------------------------------------

separator "Copying guides"

cp -r "$SHAMT_SOURCE_DIR/.shamt/guides/"* "$SHAMT_DIR/guides/"
# Exclude master's audit output history — child projects start fresh
rm -rf "$SHAMT_DIR/guides/audit/outputs"
mkdir -p "$SHAMT_DIR/guides/audit/outputs"
echo "  ✓ Guides copied (audit/outputs/ cleared for fresh start)"

# --- Copy Scripts ------------------------------------------------------------

separator "Copying scripts"

cp -r "$SHAMT_SOURCE_DIR/.shamt/scripts/"* "$SHAMT_DIR/scripts/"
echo "  ✓ Scripts copied"

# --- Configure Rules File ----------------------------------------------------

separator "Configuring rules file"

RULES_TEMPLATE="$SHAMT_DIR/scripts/initialization/RULES_FILE.template.md"
RULES_DEST="$RULES_FILE_DIR/$RULES_FILE_NAME"

if [ -f "$RULES_DEST" ]; then
    echo "  ⚠  $RULES_FILE_NAME already exists at $RULES_FILE_DIR/"
    read -rp "  Overwrite? [y/N]: " overwrite
    overwrite="${overwrite:-N}"
    if [[ ! "$overwrite" =~ ^[Yy]$ ]]; then
        echo "  Skipping rules file — agent will incorporate existing file."
        RULES_FILE_EXISTS="true"
    else
        RULES_FILE_EXISTS="false"
    fi
else
    RULES_FILE_EXISTS="false"
fi

if [ "$RULES_FILE_EXISTS" = "false" ]; then
    cp "$RULES_TEMPLATE" "$RULES_DEST"
    echo "  ✓ Rules file written to $RULES_DEST"
fi

# --- Apply Substitutions to Templates ----------------------------------------

separator "Applying configuration"

do_substitutions() {
    local file="$1"
    sed -i \
        -e "s/{{PROJECT_NAME}}/$PROJECT_NAME/g" \
        -e "s/{{EPIC_TAG}}/$EPIC_TAG/g" \
        -e "s/{{SHAMT_NAME}}/$SHAMT_NAME/g" \
        -e "s/{{GIT_PLATFORM}}/$GIT_PLATFORM/g" \
        -e "s/{{DEFAULT_BRANCH}}/$DEFAULT_BRANCH/g" \
        "$file"
}

# Apply substitutions to guides
find "$SHAMT_DIR/guides" -name "*.md" -exec sed -i \
    -e "s/{{EPIC_TAG}}/$EPIC_TAG/g" \
    -e "s/SHAMT-{N}/$EPIC_TAG-{N}/g" \
    -e "s/{{DEFAULT_BRANCH}}/$DEFAULT_BRANCH/g" \
    -e "s/{{GIT_PLATFORM}}/$GIT_PLATFORM/g" \
    {} +

# Apply to rules file
if [ "$RULES_FILE_EXISTS" = "false" ]; then
    do_substitutions "$RULES_DEST"
fi

# Copy and configure EPIC_TRACKER
EPIC_TRACKER_TEMPLATE="$SHAMT_DIR/scripts/initialization/EPIC_TRACKER.template.md"
EPIC_TRACKER_DEST="$SHAMT_DIR/epics/EPIC_TRACKER.md"
cp "$EPIC_TRACKER_TEMPLATE" "$EPIC_TRACKER_DEST"
do_substitutions "$EPIC_TRACKER_DEST"
# Set starting epic number
sed -i "s/$EPIC_TAG-1/$EPIC_TAG-$STARTING_EPIC/g" "$EPIC_TRACKER_DEST"

echo "  ✓ Configuration applied"

# --- Write init_config.md Handoff File ---------------------------------------

separator "Writing handoff file for agent"

NEEDS_AI_DISCOVERY="false"
if [ "$AI_SERVICE" = "other" ] || [ "$AI_SERVICE" = "amazon_q" ]; then
    NEEDS_AI_DISCOVERY="true"
fi

cat > "$SHAMT_DIR/project-specific-configs/init_config.md" << EOF
# Shamt Initialization Config

**Generated:** $(date +%Y-%m-%d)
**Status:** PENDING_AGENT_COMPLETION

## Project Configuration
- **Project Name:** $PROJECT_NAME
- **Epic Tag:** $EPIC_TAG
- **Shamt Agent Name:** $SHAMT_NAME
- **Starting Epic Number:** $STARTING_EPIC
- **Epic Working Directory:** .shamt/epics/

## AI Service
- **Service:** $AI_SERVICE
- **Rules File Name:** $RULES_FILE_NAME
- **Rules File Path:** $RULES_FILE_DIR/
- **Rules File Template:** .shamt/scripts/initialization/RULES_FILE.template.md
- **Needs AI Discovery:** $NEEDS_AI_DISCOVERY

## Git Configuration
- **Platform:** $GIT_PLATFORM
- **Default Branch:** $DEFAULT_BRANCH

## Script Actions Completed
- [x] Created .shamt/ folder structure (including project-specific-configs/)
- [x] Copied guides from master Shamt (audit/outputs/ cleared for fresh start)
- [x] Copied scripts from master Shamt
- [x] Placed rules file at $RULES_FILE_DIR/$RULES_FILE_NAME
- [x] Created EPIC_TRACKER.md at .shamt/epics/EPIC_TRACKER.md
- [x] Written .shamt/shamt_master_path.conf
- [x] Written .shamt/rules_file_path.conf
- [x] Written .shamt/last_sync.conf (initialized from master HEAD)
- [x] Applied configuration substitutions to guides and rules file

## Agent Remaining Tasks

**Before beginning:** Re-read the validation loop protocol at:
\`.shamt/guides/reference/validation_loop_master_protocol.md\`

Then run a validation loop to complete initialization:

- [ ] Handle AI service discovery (if Needs AI Discovery = true)
- [ ] Analyze codebase structure, languages, frameworks
- [ ] Ask clarifying questions until codebase is fully understood
- [ ] Write ARCHITECTURE.md to \`.shamt/project-specific-configs/\`
- [ ] Write CODING_STANDARDS.md to \`.shamt/project-specific-configs/\`
- [ ] Add 3-5 key coding rules to rules file summary section
- [ ] Validate all outputs meet quality bar (3 consecutive clean validation rounds)
- [ ] Mark this file complete: change Status to COMPLETE

## Notes
$( [ "$RULES_FILE_EXISTS" = "true" ] && echo "- Existing rules file was preserved — agent should incorporate it into the new rules file content." || echo "- Rules file written fresh from template." )
$( [ "$NEEDS_AI_DISCOVERY" = "true" ] && echo "- AI service '$AI_SERVICE' needs rules file convention confirmed. Agent should research and update ai_services.md." )
- ARCHITECTURE.md and CODING_STANDARDS.md belong in \`.shamt/project-specific-configs/\`, not the project root.
- Shared guide files in \`.shamt/guides/\` must remain generic — never write project-specific content into them.
- The only exception: a pointer note in a shared guide directing the agent to check \`.shamt/project-specific-configs/\` for a supplement.
EOF

echo "  ✓ Handoff file written to .shamt/project-specific-configs/init_config.md"

# --- Done --------------------------------------------------------------------

separator "Done!"
echo ""
echo "  Shamt has been initialized in: $TARGET_DIR"
echo ""
echo "  Next step: open your project in $SHAMT_NAME (your AI assistant) and say:"
echo ""
echo "    \"Read .shamt/project-specific-configs/init_config.md and complete the Shamt initialization.\""
echo ""
echo "  The agent will analyze your codebase and finish setup."
echo ""
echo "  To sync with master later:"
echo "    Import updates from master: bash .shamt/scripts/import/import.sh"
echo "    Export changes to master:   bash .shamt/scripts/export/export.sh"
echo ""
echo "============================================================"
echo ""
