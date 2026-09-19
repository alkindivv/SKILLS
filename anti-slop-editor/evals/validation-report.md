# Validation report

Build: 1.0.0. Review date: 20 September 2026.

## Checks and their meaning

This report distinguishes packaging and program tests from editorial efficacy.
The machine-readable local run is stored in `validation-results.json`.

- The literal-integrity checker has 22 unit tests, including deliberate examples
  of semantic and unit changes it cannot detect. Those limitation cases passing
  do not certify the corresponding bad translations.
- Four command-line smoke cases check pass, review, failure, and invalid-input
  status/exit-code behavior with temporary files.
- Twelve worked examples have explicit constraints checked mechanically. Seven
  eligible source/target pairs also receive limited literal checks. The JSON
  example is parsed; the seven-word headline and growth calculation are checked.
- Twenty-four regression prompts have their schema and unique identifiers
  checked. They have NOT been executed as a controlled cross-model evaluation.
- Relative Markdown links, a single SKILL.md entrypoint, the core length, required
  agent metadata, and 16 distinct source records are checked locally.

All listed executable checks passed in the construction-time local run. Run
`python evals/run_checks.py` from the skill root to reproduce these checks.

## Editorial review performed

The twelve worked outputs were authored and reviewed during construction against
stated risks: unsupported homepage claims, revenue/profit confusion, uncertainty,
exceptions, justified passive voice, access restrictions, tentative deadlines,
placeholders, material dissent, creative repetition, structured output, and
length. This is a self-review, not an independent bilingual or blind evaluation.
The examples are instructional cases, not records of a deployed agent's output.

## Packaging

The skill-creator validator and packager were used for the delivery archive.
Packaging validates the skill's structural contract, not writing quality or
perfect compatibility with every host. The archive contains one skill and no
vendored upstream runtimes, external APIs, or credentials.

## What was not verified

No with/without-skill model benchmark, independent reviewer study, native review
of every language, live ChatGPT/Hermes/Codex installation, or automated activation
on the user's account was performed. No upstream repository code was executed;
source access is recorded individually and some entries are excerpt-only.
Upstream commit hashes were not pinned. This is not a security audit of external
plugins and not a detector-bypass, authorship, or zero-error guarantee.

Use fresh holdouts and the same model/settings for future comparisons, report
fidelity failures separately from style, and retain unfavorable results.
