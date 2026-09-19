# Install and invoke

Reviewed against available official documentation on 20 September 2026.
Host interfaces and discovery paths can change. Check the source links below
before prescribing a different host's installation commands.

## ChatGPT

Open **Plugins > Skills > Create > Upload from your computer**, then choose
`skill.zip`. Availability depends on account/workspace settings. Review the
archive before upload. Follow the interface's scan and installation steps.
Then ask ChatGPT to use **Anti-Slop Editor** for the task, or select the installed
skill where the interface offers a picker.

Official reference: https://help.openai.com/en/articles/20001066

The archive contains one skill. This delivery does not establish that it is
already installed or enabled in the user's account.

## Hermes

Extract `skill.zip`, then place the `anti-slop-editor` folder in the active
profile's skills directory. The default location documented by Hermes is
`~/.hermes/skills/`. Preserve any existing folder of the same name; review an
update before replacement. Custom profiles may use a different home location.

Check the result with `hermes skills list` or `/skills`. Invoke the installed
skill with `/anti-slop-editor` followed by the task, or ask Hermes to load it by
name. A new session or skill refresh may be needed according to the host version.

Official references:
https://hermes-agent.nousresearch.com/docs/guides/work-with-skills
https://hermes-agent.nousresearch.com/docs/user-guide/features/skills

## Codex and other Agent Skills hosts

For a Codex project, place the extracted folder at
`.agents/skills/anti-slop-editor/` within the relevant project. Check discovery
with the host's skill picker and invoke `$anti-slop-editor` explicitly for a test.
Review current host documentation for other scopes or installation methods.

For other agents, register the complete skill folder using their supported
mechanism. SKILL.md readability is not proof of identical discovery, script
permissions, persistent activation, or integration behavior across all agents.
Do not assume a Claude plugin command also works in ChatGPT or Hermes.

Official references consulted:
https://developers.openai.com/fr-FR/docs/build-skills
https://agentskills.io/specification

## Make it the default editorial policy

Merge `assets/DEFAULT_INSTRUCTIONS.txt` into the host's supported persistent
instructions, project instructions, or AGENTS.md. Do not replace an existing
instruction file wholesale. In Codex, global and project AGENTS.md layers have
precedence rules; local instructions may override general guidance.

Reference: https://developers.openai.com/fr-FR/docs/agent-configuration/agents-md

The snippet asks the host to load the skill for reader-facing prose. It is not
an activation hook or technical guarantee. `allow_implicit_invocation: true`
in openai.yaml permits compatible implicit invocation; it does not force every
response to use the skill. Explicit invocation is the clearest activation test.

For a chat or API setup without file-based skills, use
`assets/PORTABLE_INSTRUCTIONS.md` as a standalone policy in an authorized
instruction field. That reduced version does not load the other modules and
must fit the host's instruction limits.

## Test installation

Use the explicit skill name with this task:
"Translate into Indonesian: The update may reduce processing time by up to 18%
in internal tests. Return only the translation."

Check that the result preserves uncertainty, the upper bound, the measured
quantity, and the internal-test context. A good answer alone does not prove the
skill was loaded: use the host's visible skill/tool activity where available.
Never invent an activation log.

## Dependencies and permissions

Routine editing requires no Python, API key, third-party service, or network.
Optional literal checks and bundled unit tests need Python 3.10+ and its standard
library. They read local files and print results; they do not send drafts
elsewhere. Research and artifact rendering use the host's separately authorized
tools when the actual task requires them.
