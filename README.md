# SKILLS

A collection of reusable AI agent skills for debugging, deep research, and implementation workflows.

## Skills

| Skill | Description |
|-------|-------------|
| [debug](debug/) | Systematic debugging with root cause analysis, failure chain reconstruction, and hypothesis falsification |
| [deep-research](deep-research/) | Comprehensive research with primary sources, uncertainty mapping, and synthesis (Indonesian) |
| [implementing](implementing/) | Code implementation with KISS, YAGNI, TDD principles |
| [forcing-questions](forcing-questions/) | Push back on hidden assumptions, scope creep, and overengineering before decomposing tasks |

## Installation

### One-liner (Auto-detect)

```bash
curl -sSL https://raw.githubusercontent.com/alkindivv/SKILLS/main/install.sh | bash
```

The installer automatically detects:
- **Claude Code** — installs to `~/.claude/skills/`
- **Hermes Agent** — installs to all profiles:
  - Default profile: `~/.hermes/skills/`
  - Named profiles: `~/.hermes/profiles/<name>/skills/`

### Manual Install

```bash
git clone https://github.com/alkindivv/SKILLS.git /tmp/skills

# Claude Code
cp -r /tmp/skills/{debug,deep-research,implementing,forcing-questions} ~/.claude/skills/

# Hermes default profile
cp -r /tmp/skills/{debug,deep-research,implementing,forcing-questions} ~/.hermes/skills/

# Hermes named profile
cp -r /tmp/skills/{debug,deep-research,implementing,forcing-questions} ~/.hermes/profiles/<name>/skills/
```

### Update

```bash
curl -sSL https://raw.githubusercontent.com/alkindivv/SKILLS/main/install.sh | bash
```

## Usage

### In Claude Code

Skills are auto-discovered from `~/.claude/skills/`. Trigger with:

```
/debug <your issue>
/research <your topic>
/implement <your task>
```

Or describe naturally:

- "Debug this error in my auth flow"
- "Research the best database for this use case"
- "Implement user authentication with JWT"

### In Other Agents

Each skill is a standalone `SKILL.md` file with:

- `name` - Skill identifier
- `description` - When to trigger the skill
- Full instructions for the AI agent

Load the `SKILL.md` content into your agent's system prompt or skill registry.

## Skill Structure

```
skills/
├── debug/
│   └── SKILL.md          # Debug workflow with root cause analysis
├── deep-research/
│   └── SKILL.md          # Research workflow in Indonesian
├── implementing/
│   └── SKILL.md          # Implementation with KISS/YAGNI/TDD
├── forcing-questions/
│   └── SKILL.md          # Pre-task pushback on framing, scope, and reversibility
├── AGENTS.md             # Agent configuration
└── README.md             # This file
```

## Philosophy

These skills share a common philosophy:

- **Completeness** - Don't table work when the answer is within reach
- **Evidence-based** - Trace before concluding, verify before asserting
- **Hypothesis falsification** - Test competing explanations, not just the first one
- **Anti-patterns** - Explicit guidance on what NOT to do

## License

MIT
