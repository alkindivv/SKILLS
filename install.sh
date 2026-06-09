#!/bin/bash
# SKILLS Installer
# Usage: curl -sSL https://raw.githubusercontent.com/alkindivv/SKILLS/main/install.sh | bash

set -e

REPO="https://github.com/alkindivv/SKILLS.git"
SKILLS_DIR="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
TEMP_DIR=$(mktemp -d)

echo "Installing SKILLS from $REPO..."

# Clone repo
git clone --depth 1 "$REPO" "$TEMP_DIR/skills" 2>/dev/null || {
    echo "Error: Failed to clone repository"
    exit 1
}

# Create skills directory
mkdir -p "$SKILLS_DIR"

# Copy skills
for skill in debug deep-research implementing; do
    if [ -d "$TEMP_DIR/skills/$skill" ]; then
        cp -r "$TEMP_DIR/skills/$skill" "$SKILLS_DIR/"
        echo "  ✓ Installed $skill"
    fi
done

# Cleanup
rm -rf "$TEMP_DIR"

echo ""
echo "Installation complete! Skills installed to: $SKILLS_DIR"
echo ""
echo "Usage in Claude Code:"
echo "  /debug <issue>"
echo "  /research <topic>"
echo "  /implement <task>"
