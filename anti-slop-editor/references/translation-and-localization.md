# Translation and localization

## Set the translation contract

Establish source and target language, locale, audience, register, terminology,
format, and whether the task is translation, localization, or transcreation.
Default to faithful, idiomatic translation. Do not turn translation into summary,
copywriting, fact correction, or adaptation without permission.

Translate what the source communicates, not the source's word order. Natural
syntax may require splitting or combining sentences. Do not omit information
just because the original is repetitive or stylistically weak; substantial
editing requires authorization. When asked to translate and de-slop, remove
verbal padding while retaining every distinct assertion and qualification.

## Two-pass method

First produce a meaning-complete target version. Then improve target-language
syntax, collocations, reference clarity, and register. Compare the revised target
against the source again; a fluent sentence can still be a wrong translation.
For consequential material, align propositions or segments to avoid dropped
conditions, footnotes, captions, and table entries.

Check these categories separately:
- Accuracy: addition, omission, wrong referent, reversed negation, altered scope,
  changed obligation, wrong relationship, or overstated certainty.
- Terminology: accepted domain meaning, approved glossary, product names, and
  consistent labels for the same concept.
- Fluency and style: idiomatic target wording, natural grammar and register,
  without forced slang or source-language syntax.
- Locale and format: number separators, dates, units, currencies, punctuation,
  variables, markup, and layout requirements.

This is an editorial checklist informed by MQM categories, not an MQM-certified
assessment or a calibrated score. Reference:
https://www.w3.org/community/mqmcg/
https://www.themqm.org/mqm-pillars/the-mqm-scoring-models/

## Preserve high-risk details

Recheck names, numerals, signs, units, ranges, inclusive/exclusive limits,
conditions, exceptions, permissions, prohibitions, and deadlines. Do not change
currency or units merely because the target language uses different ones.
Localize the display of a number only when its value remains identical and the
locale is established. Flag ambiguous dates such as 04/05/2026 rather than
silently choosing a month/day convention.

Keep placeholders such as `{name}`, `{{count}}`, `%s`, `%1$s`, and `${total}` exact.
Preserve markup, links, keys, ICU message structure, and escape sequences. Use a
format-aware parser for JSON, HTML, ICU, or rich-text structures; the optional
integrity script is only a limited safeguard. Do not translate executable tokens.

Keep quoted passages quoted. Where their translation is requested, preserve
meaning and attribution; do not falsely label a translation as the speaker's
verbatim original-language words. Follow any provided approved translation.

## Ambiguity and source errors

Prefer the established glossary and context over a dictionary's first meaning.
Preserve deliberate ambiguity where possible. When an ambiguity changes rights,
obligations, safety, or a central claim, ask or separate a concise translator's
note. Do not invent source certainty. Preserve a suspected factual error in a
faithful translation and flag it separately unless correction was authorized.

Back-translation may reveal a problem but cannot certify quality. For a language
outside the model's reliable competence, disclose that limitation when material
and recommend review by a proficient speaker. Do not claim native-level review
for languages that were not actually reviewed.

## Original EN to ID examples

Source: "The update may reduce processing time by up to 18% in internal tests."
Target: "Dalam pengujian internal, pembaruan ini mungkin mengurangi waktu
pemrosesan hingga 18%."
Keep uncertainty, upper bound, measured quantity, and test context.

Source: "You may cancel unless the invoice has already been paid."
Target: "Anda boleh membatalkan, kecuali jika tagihan sudah dibayar."
Do not translate permission as an obligation or remove the exception.

Source: "Save changes to {project_name}?"
Target: "Simpan perubahan pada {project_name}?"
Keep the placeholder intact. Do not add a claim about autosaving.
