#!/bin/bash
# Tag untagged code blocks with appropriate language identifiers

set -euo pipefail

GUIDES_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$GUIDES_DIR"

echo "Tagging untagged code blocks..."
echo

# Count before
BEFORE=$(grep -rc '^```$' . --include="*.md" | grep -v ':0$' | cut -d: -f2 | awk '{sum+=$1} END {print sum}')
echo "Untagged blocks before: $BEFORE"
echo

# Pattern 1: Blocks containing bash commands → ```bash
find . -name "*.md" -type f | while read -r file; do
    # Create temp file
    tmp_file="${file}.tmp"

    # Process file looking for untagged blocks with bash content
    awk '
    BEGIN { in_block = 0; block_content = ""; line_num = 0 }
    {
        line_num++

        # Opening fence
        if ($0 == "```") {
            if (in_block == 0) {
                # Starting new block
                in_block = 1
                block_start = line_num
                block_content = ""
                print $0
            } else {
                # Closing block - check content and tag if needed
                in_block = 0

                # Determine tag based on content
                tag = ""
                if (block_content ~ /^\$|^cd |^ls |^grep |^git |^bash|^echo |^cat |^mkdir|^rm |^mv |^cp |^chmod/) {
                    tag = "bash"
                } else if (block_content ~ /^#|^##|^\*|^-|^\[|^>/) {
                    tag = "markdown"
                } else if (block_content ~ /^{|^}|^"|^  |^    /) {
                    tag = "json"
                } else if (block_content ~ /^\||^┌|^│|^└|^├|^─|^═|^║/) {
                    tag = "text"
                } else if (block_content ~ /[A-Z_]+:/ && block_content ~ /=/) {
                    tag = "text"
                } else {
                    tag = "text"
                }

                # Print with tag
                print "```" tag
            }
        } else {
            # Regular line
            if (in_block == 1) {
                block_content = block_content "\n" $0
            }
            print $0
        }
    }
    ' "$file" > "$tmp_file"

    # Replace original if changes made
    if ! cmp -s "$file" "$tmp_file"; then
        mv "$tmp_file" "$file"
        echo "✓ Tagged blocks in: $file"
    else
        rm "$tmp_file"
    fi
done

echo
echo "Tagging complete!"
echo

# Count after
AFTER=$(grep -rc '^```$' . --include="*.md" | grep -v ':0$' | cut -d: -f2 | awk '{sum+=$1} END {print sum}' || echo "0")
echo "Untagged blocks after: ${AFTER:-0}"
echo "Tagged: $((BEFORE - ${AFTER:-0})) blocks"
