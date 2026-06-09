# SKILLS

A collection of reusable AI agent skills for debugging, deep research, and implementation workflows.

## Skills

| Skill | Description |
|-------|-------------|
| [debug](debug/) | Systematic debugging with root cause analysis, failure chain reconstruction, and hypothesis falsification |
| [deep-research](deep-research/) | Comprehensive research with primary sources, uncertainty mapping, and synthesis (Indonesian) |
| [implementing](implementing/) | Code implementation with KISS, YAGNI, TDD principles |

## Installation

### Claude Code

```bash
# Clone to skills directory
git clone https://github.com/alkindivv/SKILLS.git ~/.claude/skills/skills

# Or install individual skills
git clone https://github.com/alkindivv/SKILLS.git /tmp/skills
cp -r /tmp/skills/debug ~/.claude/skills/
cp -r /tmp/skills/deep-research ~/.claude/skills/
cp -r /tmp/skills/implementing ~/.claude/skills/
```

### Claude Code (One-liner)

```bash
git clone https://github.com/alkindivv/SKILLS.git /tmp/skills && mkdir -p ~/.claude/skills && cp -r /tmp/skills/debug /tmp/skills/deep-research /tmp/skills/implementing ~/.claude/skills/
```

### Hermes AI Agent / Other Agents

```bash
# Generic installation - copy to your agent's skills/plugins directory
git clone https://github.com/alkindivv/SKILLS.git /tmp/skills

# Adjust path to your agent's configuration
cp -r /tmp/skills/debug /path/to/your/agent/skills/
cp -r /tmp/skills/deep-research /path/to/your/agent/skills/
cp -r /tmp/skills/implementing /path/to/your/agent/skills/
```

### Update

```bash
cd ~/.claude/skills/skills && git pull
# Or for individual installs
cd /tmp/skills && git pull && cp -r debug deep-research implementing ~/.claude/skills/
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
