# Documents and output formats

## Separate editorial work from rendering

This skill edits content. Pair it with the appropriate PDF, DOCX, presentation,
website, or data-format capability for construction, layout, export, and testing.
Use the host's available tools; do not claim that this bundle includes them.

For a new artifact, stabilize structure and high-risk content before fine layout.
After rendering, inspect the exported artifact, not just its source. Check that
headings, captions, tables, references, symbols, page breaks, and text order
survive. Recheck after final text edits, since copy length can change layout.

For an existing artifact, read the actual relevant content. Do not reconstruct
unseen pages from search snippets. Preserve the user's edit scope and original
file; create a revised copy unless an authorized in-place workflow is requested.

## PDF and DOCX

Use real heading/list/table structures where supported rather than manually
simulating structure with spaces. Keep numbering, footnote relationships, table
values, captions, citations, running text, and required disclosures intact.
Check for clipping, accidental blank pages, broken characters, and orphaned
headings. Accessibility and reading order require separate format-specific QA.

Distinguish prose improvement from redaction, conversion, OCR, or legal review.
Scanned or badly extracted text may need visual inspection. Do not repair an
uncertain number or name by guessing. Report what could not be read or verified.

## Slides and presentation text

Use a slide's text to support the speaker or decision, not to squeeze an article
into boxes. Keep chart titles, axis labels, units, dates, and caveats aligned with
the data. Do not improve a headline by overstating a finding. Keep notes and
visible copy in their intended roles. Use a separate slide-rendering workflow.

## HTML, Markdown, and structured text

Edit text nodes within the allowed scope; preserve IDs, classes, routes,
attributes, component names, and functionality. Treat alt text, labels, captions,
and meta descriptions as editorial content only when in scope. Preserve code
fences, link destinations, frontmatter, keys, and citation identifiers.

For JSON/YAML or localization catalogs, change only authorized values and run
a format-aware parser. Do not add a friendly preamble to machine-readable output.
For ICU plurals or rich-text placeholders, validate the actual syntax and all
required branches. The optional checker does not parse those formats fully.

## Optional integrity script

Run `python scripts/check_integrity.py --help` to see its limited checks. Supply
an explicit manifest for exact names, URLs, quotations, or other protected spans.
It also compares simple placeholder multisets, fenced code blocks, and numeric
tokens. Numeric differences are review flags because translation or authorized
editing may change display conventions without changing value.

Do not interpret a clean run as proof of factual accuracy, semantic equivalence,
valid HTML/JSON, correct layout, or good style. Reversed negation, swapped units,
and unsupported causation can pass a literal checker. Review meaning separately.
