#!/bin/bash
# SKILLS Installer — Auto-detect Claude Code & Hermes Agent profiles
# Usage: curl -sSL https://raw.githubusercontent.com/alkindivv/SKILLS/main/install.sh | bash

REPO="https://github.com/alkindivv/SKILLS.git"
SKILLS=("debug" "deep-research" "implementing")
TEMP_DIR=$(mktemp -d)

cleanup() { rm -rf "$TEMP_DIR"; }
trap cleanup EXIT

echo "=== SKILLS Installer ==="
echo ""

# Clone repo
echo "Cloning $REPO..."
if ! git clone --depth 1 "$REPO" "$TEMP_DIR/skills" 2>/dev/null; then
    echo "Error: Failed to clone repository"
    exit 1
fi
echo ""

INSTALLED=0

install_skills() {
    local target="$1"
    local label="$2"
    mkdir -p "$target" || return 0
    for skill in "${SKILLS[@]}"; do
        [ -d "$TEMP_DIR/skills/$skill" ] && cp -r "$TEMP_DIR/skills/$skill" "$target/"
    done
    echo "  ✓ $label → $target"
    INSTALLED=$((INSTALLED + 1))
}

# ──────────────────────────────────────────────
# 1. Claude Code
# ──────────────────────────────────────────────
if [ -d "$HOME/.claude" ]; then
    install_skills "$HOME/.claude/skills" "Claude Code"
fi

# ──────────────────────────────────────────────
# 2. Hermes Agent
# ──────────────────────────────────────────────
if [ -d "$HOME/.hermes" ]; then
    echo "Hermes Agent detected at $HOME/.hermes"

    # Default profile
    install_skills "$HOME/.hermes/skills" "Hermes [default]"

    # Named profiles: ~/.hermes/profiles/<name>/
    PROFILES_DIR="$HOME/.hermes/profiles"
    if [ -d "$PROFILES_DIR" ]; then
        for profile_dir in "$PROFILES_DIR"/*/; do
            # Skip if glob didn't match (no directories)
            [ -d "$profile_dir" ] || continue
            profile_name=$(basename "$profile_dir")
            install_skills "${profile_dir}skills" "Hermes [$profile_name]"
        done
    else
        echo "  (no profiles directory at $PROFILES_DIR)"
    fi
else
    echo "Hermes Agent not found at $HOME/.hermes (skipped)"
fi

# ──────────────────────────────────────────────
# Summary
# ──────────────────────────────────────────────
echo ""

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
