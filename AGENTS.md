# Agent Configuration

## Available Skills

### debug
- **Trigger**: "debug", "fix bug", "error", "broken", "not working", "crash", "fail", "issue", "problem", "troubleshoot", "diagnose", "investigate"
- **Purpose**: Systematic debugging with root cause analysis
- **File**: `debug/SKILL.md`

### deep-research
- **Trigger**: "research", "analyze", "investigate", "deep dive", "look into", "find out", "study", "examine", "explore", "tell me about"
- **Purpose**: Comprehensive research with primary sources
- **Language**: Indonesian (Bahasa Indonesia)
- **File**: `deep-research/SKILL.md`

### implementing
- **Trigger**: "implement", "add feature", "fix", "change", "update", "refactor", "write code", "build", "create", "make"
- **Purpose**: Code implementation with KISS, YAGNI, TDD
- **File**: `implementing/SKILL.md`

### forcing-questions
- **Trigger**: "should we", "build me", "let's add", "what if we", "I want to", "I'm thinking about", or any high-stakes/ambiguous request
- **Purpose**: Pre-task pushback — surface hidden assumptions, scope creep, overengineering, and reversibility costs before decomposing
- **File**: `forcing-questions/SKILL.md`

### legal-crawler
- **Trigger**: "crawl", "peraturan", "regulation", "BPK", "JDIH", "legal knowledge base", "Indonesian law", "undang-undang", "peraturan daerah", "SOCKS5 tunnel", "geo-blocked"
- **Purpose**: Indonesian legal regulation crawler — dual-source (peraturan.go.id + peraturan.bpk.go.id) with stealth VPS tunnel
- **File**: `legal-crawler/SKILL.md`

## Integration Guide

### Claude Code

Skills in `~/.claude/skills/` are auto-discovered. Each skill needs:
- A folder with `SKILL.md`
- Frontmatter with `name` and `description`

### Custom Agent Integration

```python
# Example: Loading skills in a custom agent
import os

def load_skills(skills_dir="./skills"):
    skills = {}
    for skill_name in os.listdir(skills_dir):
        skill_path = os.path.join(skills_dir, skill_name, "SKILL.md")
        if os.path.exists(skill_path):
            with open(skill_path) as f:
                content = f.read()
                # Parse frontmatter
                name = parse_frontmatter(content, "name")
                description = parse_frontmatter(content, "description")
                skills[name] = {
                    "description": description,
                    "content": content
                }
    return skills

def match_skill(user_message, skills):
    for name, skill in skills.items():
        triggers = skill["description"].lower()
        if any(word in user_message.lower() for word in triggers.split()):
            return name
    return None
```

### System Prompt Template

```markdown
You have access to the following skills:

{for each skill}
## {skill.name}
{skill.description}

{skill.content}
{end for}

When the user's request matches a skill's trigger, follow that skill's instructions exactly.
```

## Skill Format

Each `SKILL.md` follows this structure:

```markdown
---
name: skill-name
description: "When to trigger this skill"
---

# Skill Title

[Instructions for the AI agent]
```
