#!/bin/bash
# SKILLS Installer — Auto-detect Claude Code & Hermes Agent profiles
# Usage: curl -sSL https://raw.githubusercontent.com/alkindivv/SKILLS/main/install.sh | bash

set -e

REPO="https://github.com/alkindivv/SKILLS.git"
SKILLS=("debug" "deep-research" "implementing")
TEMP_DIR=$(mktemp -d)

cleanup() { rm -rf "$TEMP_DIR"; }
trap cleanup EXIT

echo "=== SKILLS Installer ==="
echo ""

# Clone repo
echo "Cloning $REPO..."
git clone --depth 1 "$REPO" "$TEMP_DIR/skills" 2>/dev/null || {
    echo "Error: Failed to clone repository"
    exit 1
}
echo ""

INSTALLED=0

# ──────────────────────────────────────────────
# 1. Claude Code Detection
# ──────────────────────────────────────────────
if [ -d "$HOME/.claude" ]; then
    mkdir -p "$HOME/.claude/skills"
    for skill in "${SKILLS[@]}"; do
        cp -r "$TEMP_DIR/skills/$skill" "$HOME/.claude/skills/"
    done
    echo "  ✓ Claude Code → $HOME/.claude/skills/"
    ((INSTALLED++))
fi

# ──────────────────────────────────────────────
# 2. Hermes Agent Detection
# ──────────────────────────────────────────────
if command -v hermes &>/dev/null || [ -d "$HOME/.hermes" ]; then
    echo "Hermes Agent detected."

    # Default profile: ~/.hermes/
    if [ -d "$HOME/.hermes" ]; then
        mkdir -p "$HOME/.hermes/skills"
        for skill in "${SKILLS[@]}"; do
            cp -r "$TEMP_DIR/skills/$skill" "$HOME/.hermes/skills/"
        done
        echo "  ✓ Hermes [default] → $HOME/.hermes/skills/"
        ((INSTALLED++))
    fi

    # Named profiles: ~/.hermes/profiles/<name>/
    if [ -d "$HOME/.hermes/profiles" ]; then
        for profile_dir in "$HOME/.hermes/profiles"/*/; do
            [ -d "$profile_dir" ] || continue
            profile_name=$(basename "$profile_dir")
            [ "$profile_name" = "*" ] && continue
            mkdir -p "$profile_dir/skills"
            for skill in "${SKILLS[@]}"; do
                cp -r "$TEMP_DIR/skills/$skill" "$profile_dir/skills/"
            done
            echo "  ✓ Hermes [$profile_name] → ${profile_dir}skills/"
            ((INSTALLED++))
        done
    fi
else
    echo "Hermes Agent not found (skipped)."
fi

echo ""

# ──────────────────────────────────────────────
# Summary
# ──────────────────────────────────────────────
if [ "$INSTALLED" -eq 0 ]; then
    echo "No supported agents found."
    echo ""
    echo "Supported agents:"
    echo "  - Claude Code:  ~/.claude/skills/"
    echo "  - Hermes Agent: ~/.hermes/skills/"
    echo "                 ~/.hermes/profiles/<name>/skills/"
    echo ""
    echo "Manual install:"
    echo "  git clone $REPO /tmp/skills"
    echo "  cp -r /tmp/skills/{debug,deep-research,implementing} /your/skills/dir/"
    exit 1
fi

echo "Done! Installed ${#SKILLS[@]} skills to $INSTALLED location(s)."
echo ""
echo "Skills: ${SKILLS[*]}"
echo ""
echo "Usage:"
echo "  /debug <issue>        — Debug with root cause analysis"
echo "  /research <topic>     — Deep research (Indonesian)"
echo "  /implement <task>     — Implement with KISS/YAGNI/TDD"
