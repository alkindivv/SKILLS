# Source catalog and synthesis decisions

Review date: **20 September 2026**. Scope: **16 public source projects**, including
several related implementations and two marketing skills in one repository.
This is a curated map, not a claim to have collected every anti-slop skill or
plugin on the internet. A surfaced project is not automatically an adopted rule.

## Contents

1. Method and access limits
2. Public skill/plugin source records
3. Supporting editorial and platform references
4. Conflict-resolution decisions
5. Reuse and licensing boundary

## Method and access limits

Search public skill repositories for humanizer, anti-slop, deslop, clear writing,
copy-editing, and language-specific variants; inspect primary material where
available; separate duplicate families; compare rules against the intended tasks.
Also search the connected plugin directory for anti-slop/writing/localization and
for Humanizer, Grammarly, LanguageTool, and DeepL. The latter returned no matching
plugins in this session. That does not establish absence from every marketplace.
No external editing service was connected, installed, or used.

Some sources were accessible only as indexed primary-source excerpts. Each entry
states its access level. Do not describe excerpt-only sources as fully reviewed.
No upstream commit hashes were verified, so this is not a reproducible pinned
snapshot of all upstream code. Humanizer's raw and GitHub representations exposed
different version labels; no "latest version" assertion is made here. Repository
popularity, marketing promises, and claimed detector success are not evidence of
writing quality. No third-party repository code was run.

The resulting workflow is original synthesis. The source projects inform design
choices; they are not installed dependencies. Full upstream rulebooks, code,
examples, images, and licenses are not copied into this archive.

## Public skill/plugin source records
### S01 - blader/humanizer

Type: Writing humanizer.

Source: https://github.com/blader/humanizer/blob/main/SKILL.md
Related entrypoint: https://raw.githubusercontent.com/blader/humanizer/main/SKILL.md

Access: Primary SKILL.md inspected; GitHub and raw representations differed in version.

Selected idea: Pattern diagnosis, meaning preservation, voice-aware editing, and suppression of chatbot residue.

Boundary: Do not inherit blanket punctuation bans, detector claims, default draft/audit/final triplication, or examples that introduce unsupported detail.

License observation: MIT stated in skill frontmatter; full license audit not performed.

### S02 - adewale/anti-slop-writing

Type: Editorial skill.

Source: https://raw.githubusercontent.com/adewale/anti-slop-writing/main/skills/anti-slop-writing/SKILL.md

Access: Primary SKILL.md sections inspected.

Selected idea: Relate paragraphs through actual reasoning; inspect whether rhetoric substitutes for a supported point.

Boundary: Do not enforce one syntax or conclusion template across genres.

License observation: MIT stated in skill frontmatter; full license audit not performed.

### S03 - jalaalrd/anti-ai-slop-writing

Type: Universal writing directive.

Source: https://raw.githubusercontent.com/jalaalrd/anti-ai-slop-writing/main/skills/anti-ai-slop-writing/SKILL.md

Access: Primary SKILL.md inspected.

Selected idea: Broad coverage and warnings against fake anecdotes and fabricated data.

Boundary: Reject universal word bans, sentence-length recipes, one-sentence counterargument limits, and prohibition of passive voice.

License observation: Repository README states MIT; license file not independently inspected.

### S04 - adenaufal/anti-slop-writing

Type: Indonesian/English writing rules.

Source: https://github.com/adenaufal/anti-slop-writing/blob/main/indonesian/SKILL.md

Access: Primary Indonesian SKILL.md sections inspected.

Selected idea: Separate Indonesian registers and inspect locally unnatural phrasing rather than translating an English blacklist.

Boundary: Reject detector optimization, forced register mixing, blanket dash bans, and unsupported statistical claims about authorship.

License observation: A license is listed by the repository; terms not independently audited.

### S05 - dharmawan-id/anti-ai-slop

Type: Bilingual standard with skill/MCP/CLI.

Source: https://github.com/dharmawan-id/anti-ai-slop

Access: Primary repository description/README material inspected; runtime and full ruleset not audited.

Selected idea: Check Indonesian-specific bureaucratic wording and source-language calques; distinguish editorial diagnostics from detection.

Boundary: No MCP server, CLI, code, thresholds, or source text is bundled or executed.

License observation: Not independently verified.

### S06 - hap-team/deslop

Type: Skill and Claude plugin.

Source: https://github.com/hap-team/deslop

Access: Primary repository README inspected; skill-file fetch did not succeed.

Selected idea: Optional voice profiles and a focused review after rewriting.

Boundary: Reject permanent bans on useful punctuation or legitimate rhetorical forms; no plugin runtime imported.

License observation: MIT stated in repository README; full license audit not performed.

### S07 - stephenturner/skill-deslop

Type: Scientific/professional prose skill.

Source: https://github.com/stephenturner/skill-deslop
Related entrypoint: https://github.com/stephenturner/skills

Access: Primary repository README inspected; related newer collection surfaced separately.

Selected idea: Preserve domain terms and appropriate scientific passive constructions.

Boundary: Do not infer scientific accuracy from removal of stylistic patterns. Related copies are one source family, not independent evidence.

License observation: Not independently verified.

### S08 - sanketagarwal/mega-anti-slop

Type: Context-routed editorial skill.

Source: https://github.com/sanketagarwal/mega-anti-slop

Access: Indexed primary README excerpt only; full-page and SKILL fetches failed.

Selected idea: Consider explicit fidelity protection, medium-specific routing, and transparent evaluation limits.

Boundary: Treat as a corroborating design reference, not a fully audited implementation or evidence of benchmark superiority.

License observation: License file was listed; terms not independently inspected.

### S09 - codeSTACKr/anti-slop-slop-canon

Type: Voice-oriented writing/spoken-output skill.

Source: https://github.com/codeSTACKr/anti-slop-slop-canon

Access: Indexed primary README excerpt only; full-page and SKILL fetches failed.

Selected idea: Separate voice from default cleanup, and distinguish written from spoken output.

Boundary: No automatic onboarding interruption or persistence. Do not claim its profile system was tested.

License observation: Not independently verified.

### S10 - obra/the-elements-of-style

Type: Writing clearly and concisely.

Source: https://github.com/obra/the-elements-of-style/blob/main/skills/writing-clearly-and-concisely/SKILL.md

Access: Primary SKILL.md inspected; underlying book was not imported.

Selected idea: Use concrete wording and remove needless words while maintaining useful structure.

Boundary: Do not universalize English grammar rules, mandatory active voice, or brevity across languages and genres.

License observation: Not independently verified; no book or source prose redistributed.

### S11 - softaworks/agent-toolkit

Type: Writing clearly and concisely variant.

Source: https://raw.githubusercontent.com/softaworks/agent-toolkit/main/skills/writing-clearly-and-concisely/SKILL.md

Access: Primary SKILL.md available and inspected at the workflow/routing level.

Selected idea: Pair positive writing guidance with pattern diagnosis; load only needed references.

Boundary: Treat overlap with obra as a source family rather than independent validation.

License observation: Not independently verified.

### S12 - coreyhaines31/marketingskills

Type: Copywriting and copy-editing skills.

Source: https://github.com/coreyhaines31/marketingskills/blob/main/skills/copy-editing/SKILL.md
Related entrypoint: https://raw.githubusercontent.com/coreyhaines31/marketingskills/main/skills/copywriting/SKILL.md

Access: Primary copy-editing sections inspected; primary copywriting entrypoint retrieved.

Selected idea: Use page purpose, audience, focused editing passes, and proof checks for product copy.

Boundary: Keep persuasion scoped to marketing. Never invent benefits, figures, risk reversals, testimonials, or guarantees from illustrative examples.

License observation: Not independently verified in this review.

### S13 - jiji262/humanizer-chinese

Type: Chinese-localized humanizer.

Source: https://github.com/jiji262/humanizer-chinese/blob/main/SKILL.md

Access: Primary SKILL.md sections inspected; not validated by a native-language evaluator.

Selected idea: Adapt the editorial test to the target language and preserve register and source meaning.

Boundary: No Chinese lexicon, numerical detection claims, forced rhythm, or native-level competence claim imported.

License observation: MIT stated in skill frontmatter; full license audit not performed.

### S14 - seulkikaang/writing-deslop

Type: Korean/English writing patterns.

Source: https://github.com/seulkikaang/writing-deslop

Access: Indexed primary README excerpt only; full-page fetch failed.

Selected idea: Use as a multilingual coverage check for formulaic drama, not as validation of Korean output.

Boundary: No Korean rule list or unsupported example claims copied.

License observation: Not independently verified.

### S15 - ch040602/anti-ai-slop

Type: Cross-artifact review skill.

Source: https://github.com/ch040602/anti-ai-slop/blob/main/SKILL.md

Access: Indexed primary SKILL.md excerpt only; full-page fetch failed.

Selected idea: Evaluate fit to purpose without attributing authorship; separate text review from artifact-specific QA.

Boundary: Do not expand this writing skill into an untested universal UI/code/design replacement.

License observation: Not independently verified.

### S16 - fayerman-source/deslop

Type: Plain legal/professional writing.

Source: https://github.com/fayerman-source/deslop

Access: Primary repository README inspected; complete skill implementation not audited.

Selected idea: Consider plain wording while protecting terms of art.

Boundary: No legal advice, legal certification, or blanket removal of contract language.

License observation: Not independently verified.

## Supporting editorial and platform references

**Translation quality:** MQM Community Group material distinguishes source-target
accuracy from fluency and flags additions, omissions, and variable loss. The MQM
Council describes project-specific quality evaluation. This bundle borrows the
category distinction, not a certified MQM score.
https://www.w3.org/community/mqmcg/
https://www.themqm.org/mqm-pillars/the-mqm-scoring-models/

**Indonesian spelling:** The official Badan Bahasa EYD page points to the current
spelling resource. Use it for spelling questions, not to override every author's
register or substitute for a style guide.
https://badanbahasa.kemendikdasmen.go.id/produk-detail/3685/ejaan-yang-disempurnakan-eyd
https://ejaan.kemendikdasmen.go.id/

**Product language:** Microsoft's style guide describes a simple, human voice;
this is supporting editorial context rather than a mandatory brand persona.
https://learn.microsoft.com/en-us/style-guide/brand-voice-above-all-simple-human

**Web content:** Google's people-first guidance supports reader-focused,
trustworthy content rather than keyword padding or manufactured experience.
https://developers.google.com/search/docs/fundamentals/creating-helpful-content

**Packaging:** The Agent Skills specification defines a directory with SKILL.md
and optional support resources. Host discovery and execution still differ.
https://agentskills.io/specification

**ChatGPT:** The official Skills help page documents upload through the Skills
page and notes availability and workspace differences.
https://help.openai.com/en/articles/20001066

**Codex:** Official OpenAI documentation describes reusable skills and AGENTS.md
instruction layering. Some English documentation fetches failed during this
review; the corresponding official localized pages were available.
https://developers.openai.com/fr-FR/docs/build-skills
https://developers.openai.com/fr-FR/docs/agent-configuration/agents-md

**Hermes:** Official guides document installed skills, slash-command invocation,
on-demand loading, and the local skills directory.
https://hermes-agent.nousresearch.com/docs/guides/work-with-skills
https://hermes-agent.nousresearch.com/docs/user-guide/features/skills

## Conflict-resolution decisions

| Conflicting advice | Decision in this bundle |
| --- | --- |
| Ban punctuation vs match voice | Preserve useful punctuation; honor explicit house style. |
| Add specificity vs avoid fabrication | Use only available facts; expose the gap otherwise. |
| Remove hedging vs preserve evidence | Remove redundant hedges, retain meaningful uncertainty. |
| Take a side vs summarize faithfully | Preserve source position and material disagreement. |
| Shorten everything vs preserve usefulness | Remove waste, not necessary explanation or detail. |
| Add personality vs protect authorship | Match authorized voice; invent no real personal experience. |
| Apply marketing everywhere vs fit purpose | Confine conversion tactics to appropriate pages. |
| Detect AI vs edit well | Evaluate reader-facing defects, never certify authorship. |
| English pattern rules vs multilingual output | Adapt by language and register; protect semantics first. |
| Always load everything vs context efficiency | Keep one entrypoint with selective references. |

## Reuse and licensing boundary

The MIT license in this package covers its newly authored instructions, code,
examples, and documentation only. It does not relicense upstream repositories.
Source-license observations above are not a legal audit or permission to copy
those projects. Review each upstream license separately before redistribution.
No endorsement by the cited authors, OpenAI, Nous Research, Microsoft, Google,
Badan Bahasa, or MQM is implied. See NOTICE.md for the same boundary.
