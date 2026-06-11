#!/bin/bash
# SKILLS Installer — Auto-detect Claude Code & Hermes Agent profiles
# Usage: curl -sSL https://raw.githubusercontent.com/alkindivv/SKILLS/main/install.sh | bash
#
# Override Hermes location: HERMES_HOME=/path/to/root bash install.sh
# Override target user:     INSTALL_USER=alkindivv bash install.sh

REPO="https://github.com/alkindivv/SKILLS.git"
TEMP_DIR=$(mktemp -d)

cleanup() { rm -rf "$TEMP_DIR"; }
trap cleanup EXIT

# ──────────────────────────────────────────────
# Resolve Hermes home directory
# ──────────────────────────────────────────────
# In agent sessions, $HERMES_HOME points to the ACTIVE profile
# (e.g. /root/.hermes/profiles/general), NOT the real Hermes root.
# We walk up from there to find the outermost .hermes (the one with
# profiles/ as a subdirectory) so we can install to all profiles at once.
#
# Override: HERMES_HOME=/path/to/outermost-root bash install.sh

resolve_hermes_home() {
    # Find the OUTERMOST .hermes — the one whose parent contains profiles/<name>/
    # subdirectories. This is the real Hermes root, NOT a profile-internal home.
    #
    # $HERMES_HOME is intentionally ignored: in agent sessions it's set to the
    # ACTIVE profile (e.g. /root/.hermes/profiles/general), which would cause
    # the installer to update only one profile. We want all profiles updated.
    #
    # Override explicitly with HERMES_HOME=... if you need a different root.

    local start_dir="${HERMES_HOME:-$HOME}"
    local dir="$start_dir"
    local outermost=""

    # Walk up looking for any directory that contains a .hermes/profiles/
    while [ "$dir" != "/" ]; do
        if [ -d "$dir/.hermes/profiles" ]; then
            outermost="$dir"
        fi
        dir=$(dirname "$dir")
    done

    if [ -n "$outermost" ]; then
        echo "$outermost"
        return
    fi

    # VPS default — user 'root' SSHs in
    if [ -d "/root/.hermes/profiles" ]; then
        echo "/root"
        return
    fi

    # Last resort
    echo "$start_dir"
}

USER_HOME=$(resolve_hermes_home)
HERMES_DIR="$USER_HOME/.hermes"
CLAUDE_DIR="$USER_HOME/.claude"

SKILLS=()

echo "=== SKILLS Installer ==="
echo ""
echo "Resolved USER_HOME: $USER_HOME"
echo ""

# Clone repo
echo "Cloning $REPO..."
if ! git clone --depth 1 "$REPO" "$TEMP_DIR/skills" 2>/dev/null; then
    echo "Error: Failed to clone repository"
    exit 1
fi
echo ""

# Auto-derive skill list from cloned repo (no hardcoding, no maintenance)
for d in "$TEMP_DIR/skills"/*/; do
    [ -d "$d" ] || continue
    [ -f "$d/SKILL.md" ] || continue
    SKILLS+=("$(basename "$d")")
done

if [ ${#SKILLS[@]} -eq 0 ]; then
    echo "Error: No skills with SKILL.md found in repo"
    exit 1
fi

INSTALLED=0

install_skills() {
    local target="$1"
    local label="$2"
    mkdir -p "$target" || return 0
    local installed_count=0
    for skill in "${SKILLS[@]}"; do
        if [ -d "$TEMP_DIR/skills/$skill" ]; then
            cp -r "$TEMP_DIR/skills/$skill" "$target/" && installed_count=$((installed_count + 1))
        fi
    done
    if [ "$installed_count" -gt 0 ]; then
        echo "  ✓ $label → $target ($installed_count skills)"
        INSTALLED=$((INSTALLED + 1))
    fi
}

# ──────────────────────────────────────────────
# 1. Claude Code
# ──────────────────────────────────────────────
if [ -d "$CLAUDE_DIR" ]; then
    install_skills "$CLAUDE_DIR/skills" "Claude Code"
fi

# ──────────────────────────────────────────────
# 2. Hermes Agent
# ──────────────────────────────────────────────
if [ -d "$HERMES_DIR" ]; then
    echo "Hermes Agent detected at $HERMES_DIR"

    # Default profile
    install_skills "$HERMES_DIR/skills" "Hermes [default]"

    # Named profiles: ~/.hermes/profiles/<name>/
    if [ -d "$HERMES_DIR/profiles" ]; then
        for profile_dir in "$HERMES_DIR/profiles"/*/; do
            # Skip if glob didn't match (no directories)
            [ -d "$profile_dir" ] || continue
            profile_name=$(basename "$profile_dir")
            install_skills "${profile_dir}skills" "Hermes [$profile_name]"
        done
    else
        echo "  (no profiles directory at $HERMES_DIR/profiles)"
    fi
else
    echo "Hermes Agent not found at $HERMES_DIR (skipped)"
fi

# ──────────────────────────────────────────────
# Summary
# ──────────────────────────────────────────────
echo ""

if [ "$INSTALLED" -eq 0 ]; then
    echo "No supported agents found."
    echo ""
    echo "Supported agents:"
    echo "  - Claude Code:  $CLAUDE_DIR/skills/"
    echo "  - Hermes Agent: $HERMES_DIR/skills/"
    echo "                 $HERMES_DIR/profiles/<name>/skills/"
    echo ""
    echo "Manual install:"
    echo "  git clone $REPO /tmp/skills"
    echo "  cp -r /tmp/skills/* /your/skills/dir/"
    exit 1
fi

echo "Done! Installed ${#SKILLS[@]} skills to $INSTALLED location(s)."
echo ""
echo "Skills: ${SKILLS[*]}"
echo ""
echo "Usage:"
echo "  /debug <issue>          — Debug with root cause analysis"
echo "  /research <topic>       — Deep research (Indonesian)"
echo "  /implement <task>       — Implement with KISS/YAGNI/TDD"
echo "  /force <ambiguity>      — Force pushback on framing, scope, and reversibility"
