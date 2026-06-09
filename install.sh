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
install_claude_code() {
    local target="$HOME/.claude/skills"
    mkdir -p "$target"
    for skill in "${SKILLS[@]}"; do
        cp -r "$TEMP_DIR/skills/$skill" "$target/"
    done
    echo "  ✓ Claude Code → $target"
    ((INSTALLED++))
}

if [ -d "$HOME/.claude" ]; then
    install_claude_code
fi

# ──────────────────────────────────────────────
# 2. Hermes Agent Detection
# ──────────────────────────────────────────────
install_hermes_profile() {
    local profile_name="$1"
    local profile_dir="$2"

    mkdir -p "$profile_dir/skills"
    for skill in "${SKILLS[@]}"; do
        cp -r "$TEMP_DIR/skills/$skill" "$profile_dir/skills/"
    done
    echo "  ✓ Hermes [$profile_name] → $profile_dir/skills"
    ((INSTALLED++))
}

if command -v hermes &>/dev/null; then
    echo "Hermes Agent detected. Detecting profiles..."

    # Default profile: ~/.hermes/
    if [ -d "$HOME/.hermes" ]; then
        install_hermes_profile "default" "$HOME/.hermes"
    fi

    # Named profiles: ~/.hermes-<name>/
    # Method 1: hermes profile list (if available)
    PROFILES=$(hermes profile list 2>/dev/null | grep -oE '^\S+' | tail -n +2 || true)

    if [ -n "$PROFILES" ]; then
        while IFS= read -r profile; do
            [ -z "$profile" ] && continue
            [ "$profile" = "default" ] && continue
            profile_dir="$HOME/.hermes-$profile"
            if [ -d "$profile_dir" ]; then
                install_hermes_profile "$profile" "$profile_dir"
            fi
        done <<< "$PROFILES"
    else
        # Method 2: Scan ~/.hermes-* directories as fallback
        for dir in "$HOME"/.hermes-*/; do
            [ -d "$dir" ] || continue
            profile_name=$(basename "$dir" | sed 's/^\.hermes-//')
            [ "$profile_name" = "*" ] && continue
            install_hermes_profile "$profile_name" "$dir"
        done
    fi

    # External skill dirs from config.yaml
    if [ -f "$HOME/.hermes/config.yaml" ]; then
        EXTERNAL_DIRS=$(grep -A 10 'external_dirs:' "$HOME/.hermes/config.yaml" 2>/dev/null | grep '^\s*-' | sed 's/^\s*-\s*//' | sed "s|~|$HOME|g" || true)
        if [ -n "$EXTERNAL_DIRS" ]; then
            while IFS= read -r ext_dir; do
                [ -z "$ext_dir" ] && continue
                ext_dir=$(eval echo "$ext_dir")
                if [ -d "$ext_dir" ]; then
                    mkdir -p "$ext_dir"
                    for skill in "${SKILLS[@]}"; do
                        cp -r "$TEMP_DIR/skills/$skill" "$ext_dir/"
                    done
                    echo "  ✓ Hermes [external] → $ext_dir"
                    ((INSTALLED++))
                fi
            done <<< "$EXTERNAL_DIRS"
        fi
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
